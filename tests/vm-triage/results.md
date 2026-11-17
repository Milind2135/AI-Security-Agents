# vm-triage — test results

Golden tests: `README.md` in this folder. Full reports: `baselines/`.

## Summary
| Date | Agent version | Runtime | Model | Depth | Tools | Input | Result | Baseline file |
|---|---|---|---|---|---|---|---|---|
| 2026-11-02 | 5.0 | Claude Code (subagent) | Opus 4.8 | thorough | WebFetch, WebSearch | CVE-2021-44228 (test 1) | **Pass with 3 partials** | `baselines/CVE-2021-44228_claude-code_v5.0_2026-11-02.md` |
| 2026-11-02 | 5.1 | Claude Code (subagent) | not recorded | standard | WebFetch, WebSearch | CVE-2024-3400 (test 2) | **Pass** | `baselines/CVE-2024-3400_claude-code_v5.1_2026-11-02.md` |

Earlier runs in Cline with OpenRouter free models (v4.2–4.3, October 2026) did not complete reliably and are not baselines.

## Run 1 — CVE-2021-44228, v5.0
Passed: 26 sections with status lines; EPSS 0.99999 read from the EPSS API (S4); KEV added 2021-12-10, due 2021-12-24; CVSS 3.1 `S:C` 10.0 from NVD, Apache and CISA-ADP; CWE-917 difference recorded; follow-on CVEs listed; `formatMsgNoLookups` workaround marked later declared insufficient; SigmaHQ rule copied verbatim from the raw file; defanged IOCs with justified exclusions; snippets kept as SNIPPET_ONLY; within budget; handoff split; JSON consistent.

Partial / failed:
- Conflict check 1 compared CNA data with vendor prose instead of the CVE description ("through 2.15.0") → fixed in v5.1.
- CVE-2021-44832 fixed version given as 2.17.0 (2.17.1 expected); the agent flagged its own uncertainty → verbatim/Unverified rule added in v5.1.
- Vendor's current recommended release not stated (CISA minimum given instead).
- First line `vm-triage … | result`, Improvement proposals and final `Validation` line not present in the copied text.

## Run 2 — CVE-2024-3400, v5.1
Passed: configuration preconditions quoted from the vendor; fixed versions per release line all `Verbatim`; vendor and researcher IOCs cited to separate sources (Volexity, Unit 42), defanged, benign items excluded; conflict check 1 compared CNA data with the CVE description (no version boundaries in the description — correctly noted); EPSS from S4; KEV dates; CVSS 3.1 and vendor CVSS 4.0; telemetry workaround marked later declared insufficient; detections honestly `Content not retrieved` when the fetch tool limited quotes; ATT&CK all ANALYST-INFERRED at Medium; Improvement proposals present; within budget (4 searches, 11 calls).

Minor:
- First line `vm-triage … | result` and final `Validation` line not present in the copied text → relay rule tightened in `CLAUDE.md` (v5.2 change set).
- JSON detection IDs used rule UUIDs instead of D1/D2; IOCs cited to two sources listed only one in JSON → JSON rule tightened in v5.2.

## Runtime observations
- Claude Code `WebFetch` can read the JSON core sources (NVD API, CVE Services, EPSS) that Tavily in Cline could not.
- The NVD detail page (S1) returned the NVD home page in both runs → v5.2 makes the NVD JSON (S2) primary.
- `WebFetch` limits quoted passages (~125 characters), so long rule bodies cannot be copied verbatim in Claude Code; the agent correctly reports `Content not retrieved`. Copilot's `web/fetch` may behave differently — check during migration.
- The full CISA KEV JSON feed is too large for `WebFetch`; the KEV "Known Ransomware Campaign Use" field stays `NOT_AVAILABLE` in Claude Code.

## Copilot comparison (to fill in later)
| Date | Agent version | Model | Tools | Input | Result vs baseline | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |
