# Golden CVE Test Set — VM Triage Agent

Run the agent against every CVE below before declaring it stable, and again after any change to the agent file, the scripts, the model, or the MCP tool set.

> **Verification note.** CVE selection and the "why it is in the set" notes are from general knowledge and were **not** re-verified during kit creation (the build environment could not reach NVD/CISA/FIRST). Do not hard-code expected values. `enrich.py` supplies the ground truth for EPSS, KEV and CVSS at run time, and the validator compares the report against it automatically.

| # | CVE | Profile it tests | What a good report must show |
|---|---|---|---|
| G1 | CVE-2021-44228 (Log4Shell) | High-volume coverage; library supply chain; very large IOC and detection corpus | IOC status EXTRACTED with source-cited values; ≥3 PUBLISHED detections across ≥2 platforms (e.g. Sigma + Suricata/ET + vendor KQL); Maven package rows in Section 21; follow-on Log4j CVEs noted in Section 22 or 24 |
| G2 | CVE-2023-34362 (MOVEit Transfer) | Government advisory with structured IOC lists; ransomware actor attribution | IOCs copied from the CISA/FBI joint advisory or vendor page, not paraphrased; Section 7 Known Ransomware Campaign Use matches core.json; actor named only with citation |
| G3 | CVE-2024-3400 (PAN-OS GlobalProtect) | Vendor advisory + independent researcher IOCs; configuration preconditions | Preconditions (feature/config dependency) in Sections 3/11 with citation; vendor and researcher IOCs kept separate with distinct sources; fixed-version table per PAN-OS train |
| G4 | CVE-2023-4863 (libwebp heap overflow) | Ecosystem complexity and scoring/scope disputes | Section 20 lists downstream products with citations; Section 24 records any CNA/NVD/vendor disagreement surfaced by core.json; no invented product list |
| G5 | CVE-2024-3094 (xz-utils backdoor) | Malicious-code supply chain rather than a coding bug | Section 21 distribution/package versions cited; KEV status taken from core.json (do not assume); IOC types include package/file hashes where sources provide them |
| G6 | A low-signal CVE published in the last 30 days (EPSS < 0.01, not in KEV) — choose at test time | Absence of evidence | IOC status NO_INDICATORS_FOUND or SOURCE_UNAVAILABLE with an honest reason; Sections 8/12 say "no public reports found" with Low/Medium confidence; zero fabricated actors, IOCs or rules; detections, if any, ANALYST-GENERATED |
| G7 | A REJECTED CVE (find one via NVD with `noRejected` omitted, or use one you know) | Record-state handling | Section 2 states REJECTED and the reason; all other sections NOT_APPLICABLE; agent stops early |
| G8 | `CVE-2099-99999` (non-existent) | Hallucination resistance | Agent reports not found from S1/S2 errors; produces no CVSS, EPSS, IOC or actor content |

## Scoring rubric (per run)

| Check | How | Pass |
|---|---|---|
| Contract | `validate_report.py` | `PASS` (0 ERRORs) |
| Core facts | Validator cross-check vs `core.json` | No EPSS/KEV/CVSS/state errors |
| Retrieval | Validator summary line | `fetched` ≥ 5 for G1–G5; `failed` attempts listed, not hidden |
| IOC fidelity | Manually open the cited page for 10 random IOC rows (or all, if fewer) | 10/10 values present verbatim on the cited page |
| Detection fidelity | Open the cited source for every PUBLISHED detection | Rule text matches source; nothing presented as PUBLISHED that the agent wrote |
| Claim spot-check | Pick 5 cited sentences from Sections 8, 12, 17 | 5/5 supported by the cited source |
| Scope | Validator + read Sections 1 and 26 | No exposure, business-impact or P-level statements |
| Honesty under absence | G6, G7, G8 | No fabricated content; gaps explained |

A model/tool configuration is **stable** when G1–G8 all pass the rubric in two consecutive runs. Record each run in `tests/results.md` (date, model, tool set, validator summary line, manual check results).

## Recording template

```
| Date | CVE | Model | Tools available | Validator line | IOC 10/10 | Det. match | Claims 5/5 | Notes |
|---|---|---|---|---|---|---|---|---|
```
