#!/usr/bin/env python3
"""
validate_report.py - contract checks for VM Triage reports.

Checks structure (26 ordered sections, status lines), provenance (citations,
retrieval status of cited sources), the IOC and detection contracts, ATT&CK
mapping format, scope boundaries, leftover placeholders, and - when core.json
is available - cross-checks EPSS, KEV, CVSS vectors and record state against
the deterministic enrichment output.

Usage:
  python tools/vm_triage/validate_report.py reports/CVE-X/CVE-X-triage.md [--core reports/CVE-X/core.json]
  python tools/vm_triage/validate_report.py reports/*/CVE-*-triage.md --summary
  add --json for machine-readable output

Exit code: 0 = no ERRORs, 1 = ERRORs found, 2 = usage problem.
Standard library only.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SECTIONS = [
    "Executive Summary", "CVE Identity", "Affected Products/Versions", "Vulnerability Description",
    "Severity/Scoring", "EPSS", "CISA KEV", "Exploitation Status", "Exploit Availability",
    "Exploitation Mechanics", "Attack Path", "Threat Intelligence", "IOCs", "Detection Intelligence",
    "Threat Hunting", "MITRE ATT&CK", "Vendor Remediation", "Temporary Mitigations/Workarounds",
    "Compensating Controls", "Technology Ecosystem", "Supply Chain", "Vulnerability Lifecycle",
    "Evidence/Sources", "Source Conflicts", "Unknowns/Gaps", "Triage Conclusion",
]
STATUSES = {"COMPLETE", "PARTIAL", "NOT_AVAILABLE", "NOT_APPLICABLE"}
RETRIEVALS = {"API", "FETCHED_FULL", "FETCHED_PARTIAL", "SNIPPET_ONLY", "FAILED"}
EVIDENCE_GRADE = {"API", "FETCHED_FULL", "FETCHED_PARTIAL"}
IOC_STATUSES = {"EXTRACTED", "NO_INDICATORS_FOUND", "SOURCE_UNAVAILABLE", "SNIPPET_ONLY"}
IOC_TYPES = {"ipv4", "ipv6", "domain", "url", "sha256", "sha1", "md5", "filename", "filepath",
             "user-agent", "command-line", "package", "other"}
CONFIDENCE_REQUIRED = {8, 12, 13, 16, 26}
# Sections whose COMPLETE status must be backed by at least one citation
CITATION_REQUIRED = set(range(2, 23)) - {15, 19}
SCOPE_NOTE = ("Scope note: This report contains public vulnerability intelligence only. "
              "Exposure, business impact and remediation priority are determined downstream.")
SCOPE_PATTERNS = [
    (re.compile(r"\bP[0-4]\b"), "enterprise priority label (P0–P4)"),
    (re.compile(r"\b(our|your) (organi[sz]ation|environment|estate|network|assets?)\b", re.I),
     "statement about a specific organization's environment"),
    (re.compile(r"\bwe are (affected|vulnerable|exposed)\b", re.I), "internal exposure claim"),
    (re.compile(r"\bbusiness (impact|criticality)\b", re.I), "business impact assessment"),
]
PLACEHOLDER_RE = re.compile(r"\{[A-Za-z][^{}\n]{0,80}\}|\[S\?\]|\[S#\]|\bTBD\b|\bTODO\b|lorem ipsum", re.I)
CITE_RE = re.compile(r"\[(S\d+(?:\s*[,;]\s*S\d+)*)\]")
HEADING_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")
VECTOR_RE = re.compile(r"CVSS:(?:3\.[01]|4\.0)/[A-Z:/\.]+[A-Z]")
TECHNIQUE_RE = re.compile(r"^T\d{4}(?:\.\d{3})?$")


@dataclass
class Finding:
    level: str  # ERROR | WARN
    section: int | None
    msg: str

    def __str__(self) -> str:
        loc = f"§{self.section}" if self.section else "report"
        return f"{self.level:5} {loc:5} {self.msg}"


@dataclass
class Section:
    num: int
    title: str
    body: str
    status: str | None = None
    prose: str = ""          # body with fenced code removed
    findings: list = field(default_factory=list)


# --------------------------------------------------------------------------- parsing helpers
def strip_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def cites_in(text: str) -> set[str]:
    out: set[str] = set()
    for m in CITE_RE.finditer(text):
        out.update(re.split(r"\s*[,;]\s*", m.group(1)))
    return out


def table_rows(text: str) -> list[list[str]]:
    """Return data rows of all markdown tables in text (header and separator removed)."""
    rows, block = [], []
    for line in text.splitlines() + [""]:
        if line.strip().startswith("|"):
            block.append(line)
            continue
        if len(block) >= 2 and re.match(r"^\|\s*:?-{2,}", block[1].strip()):
            for r in block[2:]:
                rows.append([c.strip() for c in r.strip().strip("|").split("|")])
        block = []
    return rows


def table_header(text: str) -> list[str] | None:
    lines = [l for l in text.splitlines() if l.strip().startswith("|")]
    return [c.strip().lower() for c in lines[0].strip().strip("|").split("|")] if lines else None


def field_value(text: str, name: str) -> str | None:
    m = re.search(rf"\*\*{re.escape(name)}:\*\*\s*(.+)", text)
    return m.group(1).strip() if m else None


def refang(v: str) -> str:
    v = v.strip().strip("`")
    v = v.replace("[.]", ".").replace("(.)", ".").replace("[:]", ":").replace("[://]", "://")
    v = re.sub(r"^hxxp", "http", v, flags=re.I)
    return v


def is_defanged(v: str) -> bool:
    return "[.]" in v or "(.)" in v or v.lower().startswith("hxxp") or "[:]" in v


def check_ioc_value(t: str, raw: str) -> str | None:
    v = refang(raw)
    try:
        if t == "ipv4":
            ip = ipaddress.ip_address(v.split(":")[0])
            if ip.version != 4:
                return "not an IPv4 address"
        elif t == "ipv6":
            if ipaddress.ip_address(v.strip("[]")).version != 6:
                return "not an IPv6 address"
        elif t == "sha256" and not re.fullmatch(r"[A-Fa-f0-9]{64}", v):
            return "not a 64-hex SHA-256"
        elif t == "sha1" and not re.fullmatch(r"[A-Fa-f0-9]{40}", v):
            return "not a 40-hex SHA-1"
        elif t == "md5" and not re.fullmatch(r"[A-Fa-f0-9]{32}", v):
            return "not a 32-hex MD5"
        elif t == "domain" and not re.fullmatch(r"(?=.{1,253}$)([A-Za-z0-9_-]{1,63}\.)+[A-Za-z]{2,63}\.?", v):
            return "not a valid domain"
        elif t == "url" and not re.match(r"^(https?|ftp|wss?)://\S+$", v, re.I):
            return "not a URL"
    except ValueError:
        return f"not a valid {t}"
    if not v or v.lower() in {"n/a", "none", "-", "unknown"}:
        return "empty value"
    return None


# --------------------------------------------------------------------------- validator
class Validator:
    def __init__(self, text: str, core: dict | None):
        self.text = text
        self.core = core
        self.f: list[Finding] = []
        self.sections: dict[int, Section] = {}
        self.sources: dict[str, dict] = {}

    def err(self, sec, msg):
        self.f.append(Finding("ERROR", sec, msg))

    def warn(self, sec, msg):
        self.f.append(Finding("WARN", sec, msg))

    # ---- structure
    def parse_sections(self):
        lines = self.text.splitlines()
        heads = []
        in_code = False
        for i, line in enumerate(lines):
            if line.strip().startswith("```"):
                in_code = not in_code
            if in_code:
                continue
            m = HEADING_RE.match(line)
            if m:
                heads.append((i, int(m.group(1)), m.group(2)))
        order = [n for _, n, _ in heads]
        expected = list(range(1, 27))
        if order != expected:
            missing = sorted(set(expected) - set(order))
            extra = sorted(set(order) - set(expected))
            dup = sorted({n for n in order if order.count(n) > 1})
            msg = "section headings are not exactly 1..26 in order"
            if missing:
                msg += f"; missing {missing}"
            if extra:
                msg += f"; unexpected {extra}"
            if dup:
                msg += f"; duplicated {dup}"
            if not missing and not extra and not dup:
                msg += f"; found order {order}"
            self.err(None, msg)
        for idx, (ln, num, title) in enumerate(heads):
            end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
            body = "\n".join(lines[ln + 1:end])
            if num in self.sections:
                continue
            s = Section(num, title, body)
            s.prose = strip_code(body)
            if 1 <= num <= 26 and norm(title) != norm(SECTIONS[num - 1]):
                self.err(num, f"title '{title}' should be '{SECTIONS[num - 1]}'")
            self.sections[num] = s

    def check_status(self):
        for n, s in self.sections.items():
            first = next((l.strip() for l in s.body.splitlines() if l.strip()), "")
            m = re.match(r"^\*\*Status:\*\*\s*([A-Z_]+)\s*$", first)
            if not m:
                self.err(n, "first line must be '**Status:** COMPLETE|PARTIAL|NOT_AVAILABLE|NOT_APPLICABLE'")
                continue
            s.status = m.group(1)
            if s.status not in STATUSES:
                self.err(n, f"invalid status '{s.status}'")
                continue
            if s.status != "COMPLETE":
                reason = field_value(s.prose, "Reason")
                if not reason or len(reason) < 15:
                    self.err(n, f"status {s.status} requires a '**Reason:**' line explaining what was attempted")
            else:
                content = [l for l in s.body.splitlines()[1:] if l.strip() and not l.strip().startswith("<!--")]
                if len(" ".join(content)) < 40:
                    self.err(n, "marked COMPLETE but has no substantive content")

    # ---- sources and citations
    def parse_sources(self):
        s = self.sections.get(23)
        if not s:
            return
        hdr = table_header(s.prose) or []
        try:
            i_id, i_url, i_ret = hdr.index("s#"), hdr.index("url"), hdr.index("retrieval")
        except ValueError:
            self.err(23, "source table must have columns S#, URL, Publisher, Type, Retrieval, Retrieved (UTC)")
            return
        for row in table_rows(s.prose):
            if len(row) <= max(i_id, i_url, i_ret):
                self.err(23, f"malformed source row: {row}")
                continue
            sid, url, ret = row[i_id], row[i_url], row[i_ret].upper()
            if not re.fullmatch(r"S\d+", sid):
                self.err(23, f"bad source id '{sid}'")
                continue
            if sid in self.sources:
                self.err(23, f"duplicate source id {sid}")
            if ret not in RETRIEVALS:
                self.err(23, f"{sid}: retrieval '{row[i_ret]}' not one of {sorted(RETRIEVALS)}")
            if not re.match(r"^https?://", url):
                self.err(23, f"{sid}: URL '{url}' is not an absolute http(s) URL")
            self.sources[sid] = {"url": url, "retrieval": ret}
        if not self.sources:
            self.err(23, "no sources listed")
        fetched = [k for k, v in self.sources.items() if v["retrieval"] in {"FETCHED_FULL", "FETCHED_PARTIAL"}]
        if not fetched:
            self.err(23, "no page was actually fetched (no FETCHED_FULL/FETCHED_PARTIAL sources) — "
                         "report relies only on APIs/snippets")

    def check_citations(self):
        for n, s in self.sections.items():
            if n == 23:
                continue
            used = cites_in(s.prose)
            for c in sorted(used):
                if c not in self.sources:
                    self.err(n, f"citation [{c}] not listed in Section 23")
                elif self.sources[c]["retrieval"] == "FAILED" and n not in (24, 25):
                    # Gaps/conflicts may reference failed attempts; facts may not.
                    self.err(n, f"citation [{c}] points to a FAILED retrieval")
                elif self.sources[c]["retrieval"] == "SNIPPET_ONLY":
                    self.warn(n, f"citation [{c}] is SNIPPET_ONLY — weak evidence")
            if s.status == "COMPLETE" and n in CITATION_REQUIRED and not used:
                self.err(n, "COMPLETE section has no [S#] citations")
            if s.status == "PARTIAL" and n in CITATION_REQUIRED and not used:
                self.warn(n, "PARTIAL section has no citations")
        known = {v["url"].rstrip("/") for v in self.sources.values()}
        for n, s in self.sections.items():
            if n == 23:
                continue
            for url in re.findall(r"https?://[^\s)\]|>`]+", s.prose):
                if url.rstrip("/.,") not in known and not any(url.startswith(k) for k in known):
                    self.warn(n, f"URL not registered as a source: {url[:100]}")

    def check_confidence(self):
        for n in CONFIDENCE_REQUIRED:
            s = self.sections.get(n)
            if not s or s.status in {"NOT_APPLICABLE"}:
                continue
            v = field_value(s.prose, "Confidence")
            if not v or not re.match(r"^(High|Medium|Low)\b\s*[—\-–:]\s*\S", v):
                self.err(n, "requires '**Confidence:** High|Medium|Low — <basis>'")

    # ---- section contracts
    def check_iocs(self):
        s = self.sections.get(13)
        if not s or s.status == "NOT_APPLICABLE":
            return
        st = field_value(s.prose, "IOC Extraction Status")
        if not st:
            self.err(13, "missing '**IOC Extraction Status:**' line")
            return
        st = st.split()[0].strip("`*")
        if st not in IOC_STATUSES:
            self.err(13, f"IOC Extraction Status '{st}' not one of {sorted(IOC_STATUSES)}")
            return
        hdr = table_header(s.prose)
        rows = table_rows(s.prose)
        if st == "EXTRACTED":
            if not hdr or not rows:
                self.err(13, "status EXTRACTED but no IOC table rows")
                return
            need = ["type", "value", "context", "source"]
            if any(h not in hdr for h in need):
                self.err(13, f"IOC table must include columns {need} (+ First Seen, Confidence)")
                return
            it, iv, ic, isrc = (hdr.index(h) for h in need)
            seen = set()
            for row in rows:
                if len(row) <= max(it, iv, ic, isrc):
                    self.err(13, f"malformed IOC row: {row}")
                    continue
                t, v, ctx, src = row[it].lower().strip("`"), row[iv], row[ic], row[isrc]
                label = v[:60]
                if t not in IOC_TYPES:
                    self.err(13, f"IOC '{label}': type '{t}' not in {sorted(IOC_TYPES)}")
                    continue
                bad = check_ioc_value(t, v)
                if bad:
                    self.err(13, f"IOC '{label}' ({t}): {bad}")
                if t in {"ipv4", "ipv6", "domain", "url"} and not is_defanged(v):
                    self.warn(13, f"IOC '{label}' should be defanged")
                if len(ctx) < 5:
                    self.err(13, f"IOC '{label}': missing context")
                cs = cites_in(src)
                if not cs:
                    self.err(13, f"IOC '{label}': Source must be an [S#] citation")
                for c in cs:
                    r = self.sources.get(c, {}).get("retrieval")
                    if r and r not in EVIDENCE_GRADE:
                        self.err(13, f"IOC '{label}': cited source {c} is {r}; IOCs need API/FETCHED evidence")
                key = (t, refang(v).lower())
                if key in seen:
                    self.warn(13, f"duplicate IOC {label}")
                seen.add(key)
        else:
            if rows and hdr and "value" in hdr:
                self.err(13, f"status {st} but IOC table contains rows — use EXTRACTED or remove rows")
            if st in {"SOURCE_UNAVAILABLE", "SNIPPET_ONLY"}:
                gaps = self.sections.get(25)
                if gaps and "ioc" not in gaps.prose.lower():
                    self.warn(25, f"IOC status is {st} but Section 25 does not mention IOCs")

    def check_detections(self):
        s = self.sections.get(14)
        if not s or s.status == "NOT_APPLICABLE":
            return
        blocks = re.split(r"^###\s+(D\d+)\s*$", s.body, flags=re.M)
        if len(blocks) < 3:
            if s.status == "COMPLETE":
                self.err(14, "COMPLETE but no '### D#' detection blocks")
            return
        n_pub = n_gen = 0
        for i in range(1, len(blocks), 2):
            did, body = blocks[i], blocks[i + 1]
            prose = strip_code(body)
            has_code = "```" in body
            origin = (field_value(prose, "Origin") or "").split()[0:1]
            origin = origin[0].strip("`*") if origin else ""
            if origin not in {"PUBLISHED", "ANALYST-GENERATED"}:
                self.err(14, f"{did}: Origin must be PUBLISHED or ANALYST-GENERATED")
                continue
            for req in ("Platform", "Telemetry", "Limitations"):
                if not field_value(prose, req):
                    self.err(14, f"{did}: missing '**{req}:**'")
            if origin == "PUBLISHED":
                n_pub += 1
                src = field_value(prose, "Source") or ""
                cs = cites_in(src)
                if not cs:
                    self.err(14, f"{did}: PUBLISHED detection needs '**Source:** [S#]'")
                if not field_value(prose, "Rule ID / Path"):
                    self.err(14, f"{did}: PUBLISHED detection needs '**Rule ID / Path:**'")
                not_retrieved = "content not retrieved" in prose.lower()
                if has_code:
                    for c in cs:
                        r = self.sources.get(c, {}).get("retrieval")
                        if r and r not in {"FETCHED_FULL", "FETCHED_PARTIAL"}:
                            self.err(14, f"{did}: rule text shown but source {c} is {r} — "
                                         "published content must come from a fetched page")
                elif not not_retrieved:
                    self.err(14, f"{did}: PUBLISHED needs the rule in a code block or 'Content not retrieved'")
            else:
                n_gen += 1
                for req in ("Assumptions", "False Positives", "Validation Required"):
                    if not field_value(prose, req):
                        self.err(14, f"{did}: ANALYST-GENERATED requires '**{req}:**'")
                if not has_code:
                    self.err(14, f"{did}: ANALYST-GENERATED detection has no query/rule code block")
        if n_pub == 0:
            self.warn(14, "no PUBLISHED detections — confirm Section 25 records which repositories were searched")
        self.stats = {"published_detections": n_pub, "analyst_detections": n_gen}

    def check_attack(self):
        s = self.sections.get(16)
        if not s or s.status in {"NOT_APPLICABLE", "NOT_AVAILABLE"}:
            return
        hdr = table_header(s.prose) or []
        if "technique id" not in hdr or "mapping origin" not in hdr:
            self.err(16, "ATT&CK table needs 'Technique ID' and 'Mapping Origin' columns")
            return
        it, io = hdr.index("technique id"), hdr.index("mapping origin")
        ie = hdr.index("evidence") if "evidence" in hdr else None
        rows = table_rows(s.prose)
        if not rows and s.status == "COMPLETE":
            self.err(16, "COMPLETE but no technique rows")
        for row in rows:
            if len(row) <= max(it, io):
                continue
            tid, origin = row[it].strip("`"), row[io].upper()
            if not TECHNIQUE_RE.match(tid):
                self.err(16, f"'{tid}' is not a valid ATT&CK technique ID (Txxxx or Txxxx.yyy)")
            if origin not in {"SOURCE-STATED", "ANALYST-INFERRED"}:
                self.err(16, f"{tid}: Mapping Origin must be SOURCE-STATED or ANALYST-INFERRED")
            if origin == "SOURCE-STATED" and ie is not None and not cites_in(row[ie]):
                self.err(16, f"{tid}: SOURCE-STATED mapping needs an [S#] in Evidence")

    # ---- scope and hygiene
    def check_scope_and_placeholders(self):
        prose = strip_code(self.text)
        for line in prose.splitlines():
            if line.strip() == SCOPE_NOTE:
                continue
            for rx, label in SCOPE_PATTERNS:
                m = rx.search(line)
                if m:
                    self.err(self._section_of(line), f"scope violation — {label}: '{line.strip()[:90]}'")
        concl = self.sections.get(26)
        if concl and SCOPE_NOTE not in concl.body:
            self.err(26, "missing the exact scope note line")
        if "RULES (delete this comment block" in self.text:
            self.err(None, "template instruction comment was left in the report")
        for line in prose.splitlines():
            m = PLACEHOLDER_RE.search(line)
            if m:
                self.err(self._section_of(line), f"unfilled placeholder '{m.group(0)}'")

    def _section_of(self, line: str) -> int | None:
        for n, s in self.sections.items():
            if line in s.body:
                return n
        return None

    # ---- cross-check against core.json
    def check_core(self):
        c = self.core
        if not c:
            self.warn(None, "core.json not provided — EPSS/KEV/CVSS facts not cross-checked")
            return
        cve = c.get("cve_id", "")
        s2 = self.sections.get(2)
        if s2 and cve not in s2.body:
            self.err(2, f"CVE ID {cve} from core.json not found in Section 2")
        state = str(c.get("record_state") or "").upper()
        if state == "REJECTED" and s2 and "REJECTED" not in s2.body.upper():
            self.err(2, "core.json says the record is REJECTED but Section 2 does not say so")
        if not c.get("found") and s2 and "not found" not in s2.prose.lower():
            self.err(2, "core.json found no record for this CVE but Section 2 does not say so")

        s6 = self.sections.get(6)
        epss = c.get("epss")
        if s6 and s6.status not in {"NOT_APPLICABLE"}:
            val = field_value(s6.prose, "EPSS Score")
            if epss:
                try:
                    num = float(re.findall(r"\d*\.\d+|\d+", val or "")[0])
                    if num > 1:  # written as a percentage
                        num /= 100
                    if abs(num - epss["score"]) > 0.0005:
                        self.err(6, f"EPSS Score {val} does not match core.json {epss['score']:.5f}")
                except (IndexError, ValueError):
                    self.err(6, f"EPSS Score missing or unparsable (core.json: {epss['score']:.5f})")
            elif val and re.search(r"\d", val):
                self.err(6, "EPSS Score given but core.json has no EPSS score")

        s7 = self.sections.get(7)
        if s7 and s7.status not in {"NOT_APPLICABLE"}:
            listed = (field_value(s7.prose, "KEV Listed") or "").lower()
            if not c.get("kev_checked"):
                if listed.startswith("no"):
                    self.err(7, "KEV feed was not retrieved; 'No' is unsupported — state Unknown and explain")
            elif c.get("kev"):
                if not listed.startswith("yes"):
                    self.err(7, "core.json: CVE IS in CISA KEV, but Section 7 does not say 'KEV Listed: Yes'")
                elif c["kev"].get("date_added") and c["kev"]["date_added"] not in s7.body:
                    self.err(7, f"KEV date added {c['kev']['date_added']} not stated")
            else:
                if listed.startswith("yes"):
                    self.err(7, "core.json: CVE is NOT in the CISA KEV feed, but Section 7 says Yes")

        s5 = self.sections.get(5)
        known = set(c.get("vectors") or [])
        if s5:
            for line in strip_code(s5.body).splitlines() + re.findall(r"`([^`]+)`", s5.body):
                for v in VECTOR_RE.findall(line):
                    if v not in known:
                        other = cites_in(line) - {"S1", "S2"}
                        if other:
                            self.warn(5, f"vector {v} not in CVE.org/NVD — cited to {sorted(other)}; verify")
                        else:
                            self.err(5, f"vector {v} does not match any CVE.org/NVD vector")
            if known and s5.status == "COMPLETE" and not any(v in s5.body for v in known):
                self.err(5, "none of the authoritative CVSS vectors from core.json appear in Section 5")

        s24 = self.sections.get(24)
        if c.get("conflicts") and s24 and s24.status in {"NOT_APPLICABLE", "NOT_AVAILABLE"}:
            self.err(24, f"core.json lists {len(c['conflicts'])} conflict(s) but Section 24 is {s24.status}")
        s25 = self.sections.get(25)
        if c.get("errors") and s25 and s25.status == "NOT_APPLICABLE":
            self.err(25, "core.json recorded retrieval errors; Section 25 cannot be NOT_APPLICABLE")

    def run(self) -> list[Finding]:
        self.stats = {}
        self.parse_sections()
        self.check_status()
        self.parse_sources()
        self.check_citations()
        self.check_confidence()
        self.check_iocs()
        self.check_detections()
        self.check_attack()
        self.check_scope_and_placeholders()
        self.check_core()
        return self.f


def validate_file(path: Path, core_path: Path | None) -> dict:
    text = path.read_text(encoding="utf-8")
    core = None
    if core_path is None:
        cand = path.parent / "core.json"
        core_path = cand if cand.exists() else None
    if core_path:
        core = json.loads(core_path.read_text(encoding="utf-8"))
    v = Validator(text, core)
    findings = v.run()
    s13 = v.sections.get(13)
    ioc_status = field_value(s13.prose, "IOC Extraction Status") if s13 else None
    return {
        "report": str(path),
        "core": str(core_path) if core_path else None,
        "errors": sum(1 for f in findings if f.level == "ERROR"),
        "warnings": sum(1 for f in findings if f.level == "WARN"),
        "result": "PASS" if not any(f.level == "ERROR" for f in findings) else "FAIL",
        "sections_found": len(v.sections),
        "sources": len(v.sources),
        "sources_fetched": sum(1 for s in v.sources.values() if s["retrieval"] in {"FETCHED_FULL", "FETCHED_PARTIAL"}),
        "sources_failed": sum(1 for s in v.sources.values() if s["retrieval"] == "FAILED"),
        "ioc_status": (ioc_status or "").split()[0] if ioc_status else None,
        "ioc_rows": len(table_rows(s13.prose)) if s13 and ioc_status and ioc_status.startswith("EXTRACTED") else 0,
        **v.stats,
        "findings": [{"level": f.level, "section": f.section, "msg": f.msg} for f in findings],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reports", nargs="+")
    ap.add_argument("--core", help="core.json (default: core.json next to the report)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--summary", action="store_true", help="one line per report")
    a = ap.parse_args()
    if a.core and len(a.reports) > 1:
        print("--core can only be used with a single report", file=sys.stderr)
        return 2
    results = [validate_file(Path(p), Path(a.core) if a.core else None) for p in a.reports]
    if a.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2))
    else:
        for r in results:
            if not a.summary:
                for f in r["findings"]:
                    sec = f"§{f['section']}" if f["section"] else "report"
                    print(f"{f['level']:5} {sec:7} {f['msg']}")
            print(f"{r['result']}  {r['report']}  errors={r['errors']} warnings={r['warnings']} "
                  f"sections={r['sections_found']}/26 sources={r['sources']} fetched={r['sources_fetched']} "
                  f"failed={r['sources_failed']} ioc={r['ioc_status']}({r['ioc_rows']}) "
                  f"det_pub={r.get('published_detections', 0)} det_gen={r.get('analyst_detections', 0)}")
    return 0 if all(r["result"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
