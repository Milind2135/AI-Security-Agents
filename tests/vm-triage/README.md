# vm-triage golden tests

Run each input in **Claude Code** (`@` → **vm-triage (agent)**, then the input) and, later, in **GitHub Copilot** (agent dropdown → **vm-triage**). Record which runtime and model you used.
Re-run all five after any change to the agent file or the model.

| # | Input | What a passing output must show |
|---|---|---|
| 1 | `CVE-2021-44228` | Marker `vm-triage v5.4 \| preflight`; 26 sections in order; EPSS ≈ 0.99999 [S4], or `NOT_AVAILABLE [S4 FAILED]` plus a labelled, dated secondary EPSS from a fetched page; KEV listed, date added 2021-12-10 [S2/S1]; CVSS 3.1 vector with `S:C`; Section 24 notes the 2.15.0 conflict between the CNA version data and the description, and the CNA/NVD CWE difference (CWE-917); Section 17 names the follow-on CVEs (CVE-2021-45046, CVE-2021-45105, CVE-2021-44832) and the vendor's recommended version; IOC status EXTRACTED with fetched sources, or an honest SOURCE_UNAVAILABLE. |
| 2 | `CVE-2024-3400` | Configuration preconditions stated in Sections 3/11 with citations; vendor fixed versions per release train; vendor and researcher IOCs cited to separate sources. |
| 3 | A CVE published in the last 30 days with low EPSS, not in KEV | No invented actors, IOCs or rules; Sections 8/12 say "no public reports found" with Low/Medium confidence; KEV says "No KEV entry shown by NVD". |
| 4 | A REJECTED CVE | Section 2 states REJECTED with reason; all other sections NOT_APPLICABLE; stops early. |
| 5 | `CVE-2099-99999` (does not exist) | Reports not found; no CVSS, EPSS, IOC or actor content. |
| 6 | `Log4Shell` (no CVE ID) | Asks for the CVE ID; does not guess; suggests typing `?` for usage. |
| 7 | `?` (or `help`) | Prints the help/usage card headed `vm-triage v5.4 \| help`; no 26-section report, no preflight run, no tool/fetch calls; card names the required CVE input, optional `depth`, examples, scope boundaries (points to vulnerability-hunt / threat-hunter) and how to start. A real request like `help me triage CVE-2024-3400` must NOT trigger help mode — it runs a normal triage. |

## Additional checks since v4.1 (apply to every run)
| Check | Pass condition |
|---|---|
| Core-fact precedence | No section contradicts S1–S4 on KEV, EPSS or CVSS; any disagreement appears in Section 24. |
| Not retrieved ≠ zero | If S4 failed, Section 6 and the JSON show `NOT_AVAILABLE` / `null`, not 0. To force this, re-run row 1 with the EPSS URL unreachable or ask the agent to skip S4. |
| Scoped negatives | Every "not found" names the sources checked. |
| Manipulation report | Section 25 has either flagged sources or "No manipulation attempts observed in fetched sources." |
| Handoff | Version, configuration, exposure and compromise-evidence conditions listed separately. |
| JSON block | Parses as JSON; values identical to the report (spot-check KEV, EPSS, 3 IOCs, finding statuses). |
| Freshness | `Data as of` timestamp and re-run triggers present. |
| ATT&CK | Mapping Origin exactly SOURCE-STATED/ANALYST-INFERRED; every ANALYST-INFERRED row is Medium or Low confidence with a reason. |
| Size and budget (v4.3) | No stall; search calls ≤ budget; `tool_calls_used` in JSON within budget. |
| Snippets (v4.3) | No fact, table value or JSON value comes from a SNIPPET_ONLY source. |
| Status words (v4.3) | Every section, including 23–25, starts with one of the four status values. |
| Detections (v4.3) | No paraphrase inside a PUBLISHED code block. |
| Conflict-check sourcing (v4.3) | If S3 (JSON) is unreadable, Section 24 conflict checks 1–2 cite S3-alt (`cve.org` HTML record) or the vendor advisory and name the sources tried; the checks are never silently dropped, and no JSON FAILED stops the run. |
| Core sources (v5.2) | S2, S3, S4 fetched first; S1 fetched only if S2 failed or lacked KEV/CVSS/references, otherwise listed as `NOT_FETCHED (S2 sufficient)`. |
| JSON IDs (v5.2) | JSON detection ids are D1/D2…; each IOC's `sources` lists every S# cited in Section 13. |
| Complete relay (v5.2) | The report shown in the main chat starts with `vm-triage v5.4 \| result` and ends with `Validation: NOT RUN (chat mode).` |
| Help mode (v5.3) | Input `?`/`help`/empty prints only the usage card headed `vm-triage v5.4 \| help` and stops; no preflight, no sections, no tool calls. A help word inside a real request (`help me triage CVE-…`) does not trigger it. |
| Handoff remediation (v5.4) | JSON `fixed_versions` and `workarounds` match Sections 17 and 18 row for row with the same statuses (for CVE-2021-44228 the `formatMsgNoLookups`/`LOG4J_FORMAT_MSG_NO_LOOKUPS` workaround is `later declared insufficient`); `exploit_public` matches Section 9; `ssvc` quoted from a fetched source or all `null`. |
| Description-vs-data check (v5.1) | Section 24 check 1 quotes the CVE description ("through 2.15.0") and the CNA data (2.15.0 `unaffected`) and records the difference. |
| Version status (v5.1) | Every Section 17 version is `Verbatim` or `Unverified`; CVE-2021-44832 shows 2.17.1 (Java 8+) as Verbatim, or is marked Unverified — never an unmarked 2.17.0. |
| Runtime tools (v5.0) | Preflight names the tool used for each role (page fetch, web search); JSON `runtime_tools` matches. |
| Verbatim values (v5.0) | Scores, vectors, version ranges, IOCs and rule bodies are verbatim; any source that returned only a summary is FETCHED_PARTIAL and not quoted as exact. |
| Complete report (v5.0) | The final message is the whole 26-section report (in Claude Code, check the subagent transcript if the main chat shows a summary). |
| No-search mode (v5.0, Copilot without search) | Preflight says `web search: none`; Section 25 states it; sources come only from core-record references, GitHub Advisory and OSV. |

Record results in `tests/vm-triage/results.md`: date, runtime (Claude Code / Copilot), model, depth, tools used, pass/fail per row, notes. Keep the best Claude Code report as the **baseline** for the Copilot comparison.

Expected values in row 1 come from a live enrichment run on 2026-10-20 and can change over time (EPSS updates daily).
