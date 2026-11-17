#!/usr/bin/env python3
"""
enrich.py - deterministic core-fact collection for the VM Triage Agent.

Pulls the authoritative, machine-readable records for one CVE so the LLM never
has to recall or re-type scores, dates or KEV status:

  S1  CVE.org record (CNA + ADP containers)   https://cveawg.mitre.org/api/cve/<id>
  S2  NVD CVE API 2.0                          https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=<id>
  S3  FIRST EPSS (+ 30-day time series)        https://api.first.org/data/v1/epss?cve=<id>&scope=time-series
  S4  CISA KEV catalog (full JSON feed)        https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json

Writes <out>/core.json and <out>/core.md. Standard library only (Python 3.9+).

Usage:
  python tools/vm_triage/enrich.py CVE-2021-44228 --out reports/CVE-2021-44228
  python tools/vm_triage/enrich.py CVE-2021-44228 --out x --fixtures tests/fixtures/CVE-2021-44228

Optional environment variables:
  NVD_API_KEY      raises NVD rate limits
  HTTPS_PROXY      honoured automatically by urllib
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,}$")
UA = "vm-triage-enrich/1.0 (+public vulnerability intelligence)"
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
KEV_CACHE_TTL_S = 6 * 3600
SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_DIR = SCRIPT_DIR / ".cache"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- HTTP
def http_get_json(url: str, headers: dict | None = None, retries: int = 3, timeout: int = 45) -> Any:
    hdrs = {"User-Agent": UA, "Accept": "application/json"}
    hdrs.update(headers or {})
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 404:
                raise
            if e.code in (403, 429, 500, 502, 503, 504):
                time.sleep(6 * (attempt + 1))  # NVD asks clients to back off
                continue
            raise
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last_err = e
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"GET {url} failed after {retries} attempts: {last_err}")


class Loader:
    """Fetches live, or reads fixture files when --fixtures is given."""

    def __init__(self, fixtures: Path | None):
        self.fixtures = fixtures

    def get(self, name: str, url: str, headers: dict | None = None) -> Any:
        if self.fixtures:
            p = self.fixtures / f"{name}.json"
            if not p.exists():
                raise FileNotFoundError(f"fixture missing: {p}")
            return json.loads(p.read_text(encoding="utf-8"))
        return http_get_json(url, headers)


# --------------------------------------------------------------------------- CVSS helpers
def _metric_entry(version: str, data: dict, source: str, kind: str) -> dict:
    return {
        "source": source,
        "type": kind,
        "version": version,
        "vector": data.get("vectorString"),
        "base_score": data.get("baseScore"),
        "severity": data.get("baseSeverity"),
    }


def parse_cna_style_metrics(metrics: list, source: str, kind: str) -> list[dict]:
    """CVE JSON 5.x metrics array (used by CNA and ADP containers)."""
    out = []
    for m in metrics or []:
        for key, ver in (("cvssV4_0", "4.0"), ("cvssV3_1", "3.1"), ("cvssV3_0", "3.0"), ("cvssV2_0", "2.0")):
            if key in m and isinstance(m[key], dict):
                out.append(_metric_entry(ver, m[key], source, kind))
    return out


def parse_ssvc(metrics: list) -> dict | None:
    """CISA ADP 'Vulnrichment' SSVC decision points, if present."""
    for m in metrics or []:
        other = m.get("other") or {}
        if str(other.get("type", "")).lower() == "ssvc":
            content = other.get("content") or {}
            opts = {}
            for o in content.get("options") or []:
                if isinstance(o, dict):
                    opts.update(o)
            return {"timestamp": content.get("timestamp"), "decision_points": opts}
    return None


# --------------------------------------------------------------------------- source parsers
def parse_cveorg(rec: dict) -> dict:
    meta = rec.get("cveMetadata", {})
    cont = rec.get("containers", {})
    cna = cont.get("cna", {}) or {}
    adps = cont.get("adp", []) or []

    def en(items, field="value"):
        for d in items or []:
            if str(d.get("lang", "")).lower().startswith("en"):
                return d.get(field)
        return (items or [{}])[0].get(field) if items else None

    cwes = []
    for pt in cna.get("problemTypes", []) or []:
        for d in pt.get("descriptions", []) or []:
            cwes.append(d.get("cweId") or d.get("description"))

    affected = []
    for a in cna.get("affected", []) or []:
        affected.append({
            "vendor": a.get("vendor"),
            "product": a.get("product"),
            "package_name": a.get("packageName"),
            "collection_url": a.get("collectionURL"),
            "default_status": a.get("defaultStatus"),
            "versions": a.get("versions", []),
            "cpes": a.get("cpes", []),
        })

    metrics = parse_cna_style_metrics(cna.get("metrics"), f"CNA:{meta.get('assignerShortName')}", "CNA")
    ssvc = None
    adp_summ = []
    for adp in adps:
        prov = (adp.get("providerMetadata") or {}).get("shortName") or "ADP"
        metrics += parse_cna_style_metrics(adp.get("metrics"), f"ADP:{prov}", "ADP")
        ssvc = ssvc or parse_ssvc(adp.get("metrics"))
        adp_summ.append({"provider": prov, "title": adp.get("title")})

    return {
        "state": meta.get("state"),
        "assigner": meta.get("assignerShortName"),
        "date_reserved": meta.get("dateReserved"),
        "date_published": meta.get("datePublished"),
        "date_updated": meta.get("dateUpdated"),
        "date_rejected": meta.get("dateRejected"),
        "title": cna.get("title"),
        "description": en(cna.get("descriptions")),
        "rejected_reason": en(cna.get("rejectedReasons")),
        "cwes": [c for c in cwes if c],
        "affected": affected,
        "metrics": metrics,
        "ssvc": ssvc,
        "adp": adp_summ,
        "references": [{"url": r.get("url"), "tags": r.get("tags", []), "name": r.get("name")}
                       for r in cna.get("references", []) or []],
    }


def parse_nvd(resp: dict) -> dict | None:
    vulns = resp.get("vulnerabilities") or []
    if not vulns:
        return None
    c = vulns[0].get("cve", {})
    metrics = []
    for key, ver in (("cvssMetricV40", "4.0"), ("cvssMetricV31", "3.1"), ("cvssMetricV30", "3.0"), ("cvssMetricV2", "2.0")):
        for m in (c.get("metrics") or {}).get(key, []) or []:
            metrics.append(_metric_entry(ver, m.get("cvssData", {}), f"NVD:{m.get('source')}", m.get("type", "")))
    cwes = []
    for w in c.get("weaknesses", []) or []:
        for d in w.get("description", []) or []:
            if d.get("value"):
                cwes.append(d["value"])
    cpe_matches = []
    for cfg in c.get("configurations", []) or []:
        for node in cfg.get("nodes", []) or []:
            for cm in node.get("cpeMatch", []) or []:
                cpe_matches.append({k: cm.get(k) for k in (
                    "vulnerable", "criteria", "versionStartIncluding", "versionStartExcluding",
                    "versionEndIncluding", "versionEndExcluding") if cm.get(k) is not None})
    desc = next((d.get("value") for d in c.get("descriptions", []) if d.get("lang") == "en"), None)
    kev_fields = {k: c.get(k) for k in ("cisaExploitAdd", "cisaActionDue", "cisaRequiredAction", "cisaVulnerabilityName")
                  if c.get(k)}
    return {
        "status": c.get("vulnStatus"),
        "published": c.get("published"),
        "last_modified": c.get("lastModified"),
        "description": desc,
        "metrics": metrics,
        "cwes": sorted(set(cwes)),
        "cpe_matches": cpe_matches,
        "kev_fields": kev_fields,
        "references": [{"url": r.get("url"), "tags": r.get("tags", []), "source": r.get("source")}
                       for r in c.get("references", []) or []],
    }


def parse_epss(resp: dict, cve: str) -> dict | None:
    for d in resp.get("data") or []:
        if d.get("cve") == cve:
            series = [{"date": t.get("date"), "epss": float(t["epss"]), "percentile": float(t["percentile"])}
                      for t in d.get("time-series", []) or [] if t.get("epss") is not None]
            return {
                "score": float(d["epss"]),
                "percentile": float(d["percentile"]),
                "date": d.get("date"),
                "model_version": resp.get("model_version") or d.get("model_version"),
                "time_series_30d": sorted(series, key=lambda x: x["date"] or ""),
            }
    return None


def kev_lookup(feed: dict, cve: str) -> tuple[dict | None, dict]:
    meta = {"catalog_version": feed.get("catalogVersion"), "date_released": feed.get("dateReleased"),
            "count": feed.get("count")}
    for v in feed.get("vulnerabilities") or []:
        if v.get("cveID") == cve:
            return ({
                "date_added": v.get("dateAdded"),
                "due_date": v.get("dueDate"),
                "vendor_project": v.get("vendorProject"),
                "product": v.get("product"),
                "vulnerability_name": v.get("vulnerabilityName"),
                "short_description": v.get("shortDescription"),
                "required_action": v.get("requiredAction"),
                "known_ransomware_campaign_use": v.get("knownRansomwareCampaignUse"),
                "cwes": v.get("cwes", []),
                "notes": v.get("notes"),
            }, meta)
    return None, meta


def load_kev(loader: Loader) -> dict:
    if loader.fixtures:
        return loader.get("kev", KEV_URL)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / "kev.json"
    if cache.exists() and time.time() - cache.stat().st_mtime < KEV_CACHE_TTL_S:
        return json.loads(cache.read_text(encoding="utf-8"))
    data = http_get_json(KEV_URL, timeout=90)
    cache.write_text(json.dumps(data), encoding="utf-8")
    return data


# --------------------------------------------------------------------------- conflict detection
def detect_conflicts(cveorg: dict | None, nvd: dict | None, kev: dict | None) -> list[dict]:
    conflicts: list[dict] = []
    all_metrics = (cveorg or {}).get("metrics", []) + (nvd or {}).get("metrics", [])

    # 1. Same CVSS major version, different scores/vectors across sources
    for ver in ("4.0", "3.1", "3.0"):
        group = [m for m in all_metrics if m["version"] == ver and m.get("vector")]
        vectors = {m["vector"] for m in group}
        if len(vectors) > 1:
            conflicts.append({
                "field": f"CVSS v{ver}",
                "detail": "Sources publish different vectors/scores",
                "values": [{"source": m["source"], "vector": m["vector"], "base_score": m["base_score"],
                            "severity": m["severity"]} for m in group],
            })
    # 3.0 vs 3.1 from different sources is common and noteworthy when severities differ
    v3 = [m for m in all_metrics if m["version"] in ("3.0", "3.1") and m.get("severity")]
    if len({m["severity"] for m in v3}) > 1 and not any(c["field"].startswith("CVSS v3") for c in conflicts):
        conflicts.append({"field": "CVSS v3 severity", "detail": "Severity rating differs across sources",
                          "values": [{"source": m["source"], "version": m["version"], "severity": m["severity"],
                                      "base_score": m["base_score"]} for m in v3]})

    # 2. KEV feed vs NVD KEV mirror fields
    nvd_kev = (nvd or {}).get("kev_fields") or {}
    if nvd is not None and (bool(kev) != bool(nvd_kev.get("cisaExploitAdd"))):
        conflicts.append({"field": "CISA KEV status",
                          "detail": "KEV feed and NVD cisa* fields disagree (one may be stale)",
                          "values": [{"source": "CISA KEV feed", "listed": bool(kev),
                                      "date_added": (kev or {}).get("date_added")},
                                     {"source": "NVD", "listed": bool(nvd_kev.get("cisaExploitAdd")),
                                      "date_added": nvd_kev.get("cisaExploitAdd")}]})
    elif kev and nvd_kev.get("cisaExploitAdd") and kev.get("date_added") != nvd_kev.get("cisaExploitAdd"):
        conflicts.append({"field": "CISA KEV date added", "detail": "Date differs between KEV feed and NVD",
                          "values": [{"source": "CISA KEV feed", "date_added": kev.get("date_added")},
                                     {"source": "NVD", "date_added": nvd_kev.get("cisaExploitAdd")}]})

    # 3. Record state
    if cveorg and nvd and str(cveorg.get("state", "")).upper() == "REJECTED" and \
            str(nvd.get("status", "")).lower() != "rejected":
        conflicts.append({"field": "Record state", "detail": "CVE.org REJECTED but NVD status differs",
                          "values": [{"source": "CVE.org", "state": cveorg.get("state")},
                                     {"source": "NVD", "status": nvd.get("status")}]})

    # 4. CWE (informational)
    if cveorg and nvd and cveorg.get("cwes") and nvd.get("cwes"):
        a = {c for c in cveorg["cwes"] if str(c).startswith("CWE-")}
        b = {c for c in nvd["cwes"] if str(c).startswith("CWE-")}
        if a and b and a != b:
            conflicts.append({"field": "CWE", "detail": "CWE assignments differ (informational)",
                              "values": [{"source": "CVE.org CNA", "cwes": sorted(a)},
                                         {"source": "NVD", "cwes": sorted(b)}]})
    return conflicts


# --------------------------------------------------------------------------- markdown summary
def render_md(core: dict) -> str:
    L: list[str] = []
    cve = core["cve_id"]
    L.append(f"# Core facts — {cve}")
    L.append(f"Generated: {core['generated_utc']} by enrich.py (deterministic; do not edit).")
    L.append("")
    L.append("## Sources (copy these rows into Section 23)")
    L.append("| S# | URL | Publisher | Type | Retrieval | Retrieved (UTC) |")
    L.append("|---|---|---|---|---|---|")
    for s in core["sources"]:
        L.append(f"| {s['id']} | {s['url']} | {s['publisher']} | {s['type']} | {s['retrieval']} | {s['retrieved_utc']} |")
    L.append("")

    co, nvd, epss, kev = core.get("cveorg"), core.get("nvd"), core.get("epss"), core.get("kev")
    L.append("## Identity")
    if co:
        L.append(f"- State: {co.get('state')} [S1]; Assigner (CNA): {co.get('assigner')} [S1]")
        L.append(f"- Reserved: {co.get('date_reserved')}; Published: {co.get('date_published')}; Updated: {co.get('date_updated')} [S1]")
        if co.get("title"):
            L.append(f"- CNA title: {co['title']} [S1]")
        if co.get("rejected_reason"):
            L.append(f"- Rejected reason: {co['rejected_reason']} [S1]")
        L.append(f"- CWE (CNA): {', '.join(co.get('cwes') or []) or 'none'} [S1]")
    if nvd:
        L.append(f"- NVD status: {nvd.get('status')}; NVD published: {nvd.get('published')}; last modified: {nvd.get('last_modified')} [S2]")
        L.append(f"- CWE (NVD): {', '.join(nvd.get('cwes') or []) or 'none'} [S2]")
    L.append("")

    L.append("## CVSS (all published vectors)")
    L.append("| Source | Type | Version | Base | Severity | Vector | Cite |")
    L.append("|---|---|---|---|---|---|---|")
    for m in (co or {}).get("metrics", []):
        L.append(f"| {m['source']} | {m['type']} | {m['version']} | {m['base_score']} | {m['severity']} | `{m['vector']}` | [S1] |")
    for m in (nvd or {}).get("metrics", []):
        L.append(f"| {m['source']} | {m['type']} | {m['version']} | {m['base_score']} | {m['severity']} | `{m['vector']}` | [S2] |")
    if co and co.get("ssvc"):
        L.append("")
        L.append(f"- CISA ADP SSVC: {json.dumps(co['ssvc']['decision_points'])} (as of {co['ssvc'].get('timestamp')}) [S1]")
    L.append("")

    L.append("## EPSS")
    if epss:
        L.append(f"- **EPSS Score:** {epss['score']:.5f} [S3]")
        L.append(f"- **EPSS Percentile:** {epss['percentile']:.5f} [S3]")
        L.append(f"- **EPSS Date:** {epss.get('date')} [S3]")
        ts = epss.get("time_series_30d") or []
        if ts:
            lo = min(t["epss"] for t in ts)
            hi = max(t["epss"] for t in ts)
            L.append(f"- 30-day range: {lo:.5f} – {hi:.5f} over {len(ts)} data points [S3]")
    else:
        L.append("- No EPSS score returned.")
    L.append("")

    L.append("## CISA KEV")
    if kev:
        L.append("- **KEV Listed:** Yes [S4]")
        for k in ("date_added", "due_date", "vulnerability_name", "required_action", "known_ransomware_campaign_use"):
            L.append(f"- {k}: {kev.get(k)} [S4]")
    else:
        L.append(f"- **KEV Listed:** No — not present in catalog version {core.get('kev_catalog', {}).get('catalog_version')} [S4]")
    if nvd and nvd.get("kev_fields"):
        L.append(f"- NVD KEV mirror fields: {json.dumps(nvd['kev_fields'])} [S2]")
    L.append("")

    L.append("## Affected (CNA)")
    for a in (co or {}).get("affected", [])[:25]:
        L.append(f"- {a.get('vendor')} / {a.get('product')} (default: {a.get('default_status')}): "
                 f"{json.dumps(a.get('versions'))[:600]} [S1]")
    if nvd and nvd.get("cpe_matches"):
        L.append(f"- NVD CPE match entries: {len(nvd['cpe_matches'])} (see core.json → nvd.cpe_matches) [S2]")
    L.append("")

    L.append("## Conflicts (copy into Section 24)")
    if core["conflicts"]:
        for c in core["conflicts"]:
            L.append(f"- **{c['field']}** — {c['detail']}: {json.dumps(c['values'])}")
    else:
        L.append("- None detected between S1–S4.")
    L.append("")
    L.append("## Errors (copy into Section 25)")
    if core["errors"]:
        for e in core["errors"]:
            L.append(f"- {e}")
    else:
        L.append("- None.")
    L.append("")

    refs = {}
    for r in (co or {}).get("references", []) + (nvd or {}).get("references", []):
        if r.get("url"):
            refs.setdefault(r["url"], set()).update(r.get("tags") or [])
    L.append(f"## References to research ({len(refs)}) — leads only; fetch before citing")
    for url, tags in sorted(refs.items(), key=lambda kv: (0 if kv[1] & {"Vendor Advisory", "Patch", "vendor-advisory", "patch"} else
                                                          1 if kv[1] & {"Exploit", "exploit"} else 2, kv[0])):
        L.append(f"- {url} {('(' + ', '.join(sorted(tags)) + ')') if tags else ''}")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- main
def enrich(cve: str, loader: Loader) -> dict:
    errors: list[str] = []
    sources: list[dict] = []

    def src(sid, url, publisher, ok, note=""):
        sources.append({"id": sid, "url": url, "publisher": publisher, "type": "Authoritative API",
                        "retrieval": "API" if ok else "FAILED", "retrieved_utc": now_utc(), "note": note})

    # S1 CVE.org
    u1 = f"https://cveawg.mitre.org/api/cve/{cve}"
    cveorg = None
    try:
        cveorg = parse_cveorg(loader.get("cveorg", u1))
        src("S1", u1, "CVE Program (CVE.org)", True)
    except urllib.error.HTTPError as e:
        src("S1", u1, "CVE Program (CVE.org)", False, f"HTTP {e.code}")
        errors.append(f"S1 CVE.org: HTTP {e.code}" + (" — CVE ID not found" if e.code == 404 else ""))
    except Exception as e:  # noqa: BLE001
        src("S1", u1, "CVE Program (CVE.org)", False, str(e))
        errors.append(f"S1 CVE.org: {e}")

    # S2 NVD
    u2 = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}"
    nvd = None
    try:
        key = os.environ.get("NVD_API_KEY")
        nvd = parse_nvd(loader.get("nvd", u2, {"apiKey": key} if key else None))
        src("S2", u2, "NIST NVD", True, "" if nvd else "no record returned")
        if nvd is None:
            errors.append("S2 NVD: no record returned for this CVE")
    except Exception as e:  # noqa: BLE001
        src("S2", u2, "NIST NVD", False, str(e))
        errors.append(f"S2 NVD: {e}")

    # S3 EPSS
    u3 = f"https://api.first.org/data/v1/epss?cve={cve}&scope=time-series"
    epss = None
    try:
        epss = parse_epss(loader.get("epss", u3), cve)
        src("S3", u3, "FIRST EPSS", True, "" if epss else "no score returned")
        if epss is None:
            errors.append("S3 EPSS: no score returned (CVE may be too new, rejected, or not scored)")
    except Exception as e:  # noqa: BLE001
        src("S3", u3, "FIRST EPSS", False, str(e))
        errors.append(f"S3 EPSS: {e}")

    # S4 KEV
    kev, kev_meta = None, {}
    try:
        kev, kev_meta = kev_lookup(load_kev(loader), cve)
        src("S4", KEV_URL, "CISA", True, f"catalog {kev_meta.get('catalog_version')}")
    except Exception as e:  # noqa: BLE001
        src("S4", KEV_URL, "CISA", False, str(e))
        errors.append(f"S4 CISA KEV feed: {e} — KEV status must be treated as UNKNOWN")

    core = {
        "schema": "vm-triage-core/1",
        "cve_id": cve,
        "generated_utc": now_utc(),
        "sources": sources,
        "cveorg": cveorg,
        "nvd": nvd,
        "epss": epss,
        "kev": kev,
        "kev_checked": any(s["id"] == "S4" and s["retrieval"] == "API" for s in sources),
        "kev_catalog": kev_meta,
        "record_state": (cveorg or {}).get("state") or ((nvd or {}).get("status")),
        "found": bool(cveorg or nvd),
        "conflicts": detect_conflicts(cveorg, nvd, kev),
        "errors": errors,
    }
    core["vectors"] = sorted({m["vector"] for m in (cveorg or {}).get("metrics", []) + (nvd or {}).get("metrics", [])
                              if m.get("vector")})
    return core


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cve")
    ap.add_argument("--out", required=True, help="output directory, e.g. reports/CVE-2021-44228")
    ap.add_argument("--fixtures", help="read <dir>/{cveorg,nvd,epss,kev}.json instead of the network")
    a = ap.parse_args()

    cve = a.cve.strip().upper()
    if not CVE_RE.match(cve):
        print(f"ERROR: '{a.cve}' is not a CVE ID (CVE-YYYY-NNNN)", file=sys.stderr)
        return 2

    core = enrich(cve, Loader(Path(a.fixtures) if a.fixtures else None))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "core.json").write_text(json.dumps(core, indent=2), encoding="utf-8")
    (out / "core.md").write_text(render_md(core), encoding="utf-8")

    ok = sum(1 for s in core["sources"] if s["retrieval"] == "API")
    print(f"{cve}: found={core['found']} state={core['record_state']} sources_ok={ok}/4 "
          f"kev={'YES' if core['kev'] else ('NO' if core['kev_checked'] else 'UNKNOWN')} "
          f"epss={core['epss']['score'] if core['epss'] else 'n/a'} conflicts={len(core['conflicts'])} "
          f"errors={len(core['errors'])}")
    print(f"wrote {out / 'core.json'} and {out / 'core.md'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
