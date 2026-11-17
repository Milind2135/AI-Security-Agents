"""
Regression tests for the VM Triage kit (stdlib unittest; no network).

Run from the repo root:
    python -m unittest discover -s tests -v

Each mutation test takes the passing synthetic report and injects one known
failure mode observed in earlier agent runs, then asserts the validator catches it.
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "vm_triage"))

import enrich  # noqa: E402
import validate_report as vr  # noqa: E402

FIX = ROOT / "tests" / "fixtures" / "CVE-2099-10001"
CVE = "CVE-2099-10001"


def build_core(fixture_dir: Path = FIX, cve: str = CVE) -> dict:
    return enrich.enrich(cve, enrich.Loader(fixture_dir))


BASE = (FIX / "sample-report.md").read_text(encoding="utf-8")
CORE = build_core()


def run(text: str, core: dict | None = CORE):
    findings = vr.Validator(text, core).run()
    return [f for f in findings if f.level == "ERROR"]


class TestEnrich(unittest.TestCase):
    def test_core_fields(self):
        self.assertTrue(CORE["found"])
        self.assertEqual(CORE["record_state"], "PUBLISHED")
        self.assertAlmostEqual(CORE["epss"]["score"], 0.94321)
        self.assertEqual(CORE["kev"]["date_added"], "2099-01-12")
        self.assertTrue(CORE["kev_checked"])
        self.assertEqual(len(CORE["vectors"]), 2)
        self.assertEqual(CORE["cveorg"]["ssvc"]["decision_points"]["Exploitation"], "active")

    def test_cvss_conflict_detected(self):
        fields = [c["field"] for c in CORE["conflicts"]]
        self.assertIn("CVSS v3.1", fields)

    def test_kev_feed_missing_is_unknown_not_no(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ("cveorg", "nvd", "epss"):
                shutil.copy(FIX / f"{n}.json", d)
            core = build_core(Path(d))
        self.assertFalse(core["kev_checked"])
        self.assertIsNone(core["kev"])
        self.assertTrue(any("KEV" in e for e in core["errors"]))

    def test_kev_feed_vs_nvd_disagreement(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ("cveorg", "nvd", "epss"):
                shutil.copy(FIX / f"{n}.json", d)
            kev = json.loads((FIX / "kev.json").read_text())
            kev["vulnerabilities"] = [v for v in kev["vulnerabilities"] if v["cveID"] != CVE]
            Path(d, "kev.json").write_text(json.dumps(kev))
            core = build_core(Path(d))
        self.assertIn("CISA KEV status", [c["field"] for c in core["conflicts"]])

    def test_rejected_record(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ("nvd", "epss", "kev"):
                shutil.copy(FIX / f"{n}.json", d)
            rec = json.loads((FIX / "cveorg.json").read_text())
            rec["cveMetadata"]["state"] = "REJECTED"
            rec["containers"]["cna"]["rejectedReasons"] = [{"lang": "en", "value": "Duplicate of another CVE."}]
            Path(d, "cveorg.json").write_text(json.dumps(rec))
            core = build_core(Path(d))
        self.assertEqual(core["record_state"], "REJECTED")
        self.assertIn("Record state", [c["field"] for c in core["conflicts"]])

    def test_markdown_renders(self):
        md = enrich.render_md(CORE)
        self.assertIn("**KEV Listed:** Yes", md)
        self.assertIn("| S4 |", md)


class TestValidatorBaseline(unittest.TestCase):
    def test_sample_passes(self):
        errs = run(BASE)
        self.assertEqual(errs, [], "\n".join(map(str, errs)))

    def test_template_fails(self):
        tpl = (ROOT / "templates" / "report-template.md").read_text(encoding="utf-8")
        msgs = " ".join(f.msg for f in run(tpl))
        self.assertIn("placeholder", msgs)
        self.assertIn("template instruction comment", msgs)


class TestValidatorMutations(unittest.TestCase):
    """Each case is one failure mode; the validator must raise at least one matching ERROR."""

    def assertCaught(self, text, needle, core=CORE):
        errs = run(text, core)
        self.assertTrue(any(needle.lower() in f.msg.lower() for f in errs),
                        f"expected ERROR containing '{needle}', got:\n" + "\n".join(map(str, errs)))

    def test_missing_section(self):
        t = BASE.replace("## 15. Threat Hunting", "## Threat hunting notes")
        self.assertCaught(t, "missing [15]")

    def test_wrong_title(self):
        self.assertCaught(BASE.replace("## 13. IOCs", "## 13. Indicators"), "should be 'IOCs'")

    def test_partial_without_reason(self):
        t = BASE.replace("## 18. Temporary Mitigations/Workarounds\n**Status:** COMPLETE",
                         "## 18. Temporary Mitigations/Workarounds\n**Status:** PARTIAL")
        self.assertCaught(t, "requires a '**Reason:**'")

    def test_epss_mismatch(self):
        self.assertCaught(BASE.replace("**EPSS Score:** 0.94321", "**EPSS Score:** 0.51000"), "does not match core.json")

    def test_kev_mismatch(self):
        self.assertCaught(BASE.replace("**KEV Listed:** Yes", "**KEV Listed:** No"), "IS in CISA KEV")

    def test_kev_no_when_feed_unchecked(self):
        core = json.loads(json.dumps(CORE))
        core["kev_checked"], core["kev"] = False, None
        self.assertCaught(BASE.replace("**KEV Listed:** Yes", "**KEV Listed:** No"), "unsupported", core)

    def test_fabricated_vector(self):
        t = BASE.replace("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H")
        self.assertCaught(t, "does not match any CVE.org/NVD vector")

    def test_ioc_from_snippet(self):
        t = BASE.replace("| Threat research | FETCHED_FULL |", "| Threat research | SNIPPET_ONLY |")
        self.assertCaught(t, "IOCs need API/FETCHED evidence")

    def test_ioc_bad_hash(self):
        self.assertCaught(BASE.replace("9f86d081884c7d659a2f", "9f86d081884c7d659a2"), "not a 64-hex SHA-256")

    def test_ioc_generic_statement(self):
        start = BASE.index("| Type | Value | Context")
        end = BASE.index("Infrastructure indicators were")
        t = BASE[:start] + "Hashes are available in the vendor advisory [S6].\n\n" + BASE[end:]
        self.assertCaught(t, "no IOC table rows")

    def test_ioc_rows_with_non_extracted_status(self):
        t = BASE.replace("**IOC Extraction Status:** EXTRACTED", "**IOC Extraction Status:** NO_INDICATORS_FOUND")
        self.assertCaught(t, "contains rows")

    def test_published_detection_without_source(self):
        self.assertCaught(BASE.replace("**Source:** [S8]\n", ""), "needs '**Source:** [S#]'")

    def test_published_rule_text_from_snippet(self):
        t = BASE.replace("| Detection rule | FETCHED_FULL |", "| Detection rule | SNIPPET_ONLY |")
        self.assertCaught(t, "published content must come from a fetched page")

    def test_analyst_query_missing_fields(self):
        t = BASE.replace("**False Positives:** Legitimate admin scripts launched by the service.\n", "")
        self.assertCaught(t, "requires '**False Positives:**'")

    def test_scope_violation_priority(self):
        t = BASE.replace("A fixed release, 2.4.1, is available [S6].",
                         "A fixed release, 2.4.1, is available [S6]. Treat as P1 for our environment.")
        self.assertCaught(t, "scope violation")

    def test_missing_scope_note(self):
        self.assertCaught(BASE.replace("Scope note: This report", "Note: This report"), "scope note")

    def test_placeholder(self):
        self.assertCaught(BASE.replace("| ExampleCorp | ExampleServer | >= 2.0.0", "| {vendor} | ExampleServer | >= 2.0.0"),
                          "placeholder")

    def test_unknown_citation(self):
        self.assertCaught(BASE.replace("allows unauthenticated remote code execution [S1].",
                                       "allows unauthenticated remote code execution [S99]."), "[S99] not listed")

    def test_fact_cited_to_failed_source(self):
        self.assertCaught(BASE.replace("A fixed release, 2.4.1, is available [S6].",
                                       "A fixed release, 2.4.1, is available [S9]."), "FAILED retrieval")

    def test_uncited_complete_section(self):
        t = BASE.replace("are evaluated as template code", "X").replace(
            "runs with the privileges of the service account [S1][S5].", "runs with the privileges of the service account.")
        self.assertCaught(t, "no [S#] citations")

    def test_bad_attack_id(self):
        self.assertCaught(BASE.replace("| T1190 |", "| T190 |"), "not a valid ATT&CK technique ID")

    def test_missing_confidence(self):
        t = BASE.replace("**Confidence:** Medium — single research source; no attribution.\n", "")
        self.assertCaught(t, "Confidence")

    def test_no_fetched_pages(self):
        t = BASE.replace("FETCHED_FULL", "SNIPPET_ONLY").replace("FETCHED_PARTIAL", "SNIPPET_ONLY")
        self.assertCaught(t, "no page was actually fetched")

    def test_conflict_ignored(self):
        start = BASE.index("## 24. Source Conflicts")
        end = BASE.index("## 25. Unknowns/Gaps")
        t = BASE[:start] + "## 24. Source Conflicts\n**Status:** NOT_APPLICABLE\n**Reason:** No conflicts were observed in sources.\n\n" + BASE[end:]
        self.assertCaught(t, "conflict(s) but Section 24")


if __name__ == "__main__":
    unittest.main(verbosity=2)
