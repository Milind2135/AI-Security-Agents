# threat-intel-analyst test results

> Runs dated before 2026-11-17 were made against `intelligence-analyst` v2.0 (renamed `threat-intel-analyst` in v3.0). Their section numbers follow v2.0, which has the same 16 sections.

Runs are manual best-effort stand-ins executed in Claude Code using `WebSearch`/`WebFetch` in place of Tavily — closest to the Copilot `web/fetch` path, **not** the Cline+Tavily runtime. Treat as design validation, not a Cline golden-run.

## 2026-10-27 — v2.0 — Claude Code (web/fetch stand-in)

**Row 1 (campaign): Shai-Hulud 2.0 npm worm** — budget: 1 search + 3 retrievals (standard).

| Criterion | Result | Note |
|---|---|---|
| Preflight marker + TLP + 16 sections in order | PASS | |
| Timeline (§4) + affected set with cited counts (§5) | PASS | Correctly surfaced the 796 vs >700 package / 14k vs 27k repo disagreement in §16 rather than picking one. |
| Propagation mechanism stated | PASS | |
| IOCs defanged, EXTRACTED, sourced (§8) | PASS | File hashes + host artefacts corroborated across S1/S3. |
| Related CVEs handed off, not triaged (§10) | PASS | Returned `NOT_APPLICABLE`; did not invent a CVE. |
| ATT&CK Mapping-Origin discipline (§6) | PASS | All `ANALYST-INFERRED`, capped at Medium. |
| Attribution by competing hypotheses (§9) | PASS | H1/H2 with disconfirming evidence; named-actor "unresolved". |
| STIX JSON parses | PASS | |
| Scope boundary / no actions | PASS | §11 only `REQUIRES APPROVAL` lines. |

Sources: S1 Datadog (B2, FETCHED_FULL), S2 StepSecurity (B2, v1 only), S3 Zscaler (B2, FETCHED_FULL). No FAILED.
Observations: evidence discipline held (conflicts, no-CVE case surfaced honestly). `web/fetch` summarises — one source paraphrased its own base64 claim and file/workflow names varied slightly; fine here with two sources, risky single-source → prefer `thorough`. Admiralty grading coarse (all B2) without a documented rubric.

**§12-focus run (campaign): Shai-Hulud 2.0 published detection rules** — budget: 2 searches + 5 retrievals (thorough; 2 raw 404, 1 timeout, 1 partial).

| §12 criterion | Result | Note |
|---|---|---|
| Coverage matrix across all named platforms | PASS | Sigma/Sentinel/YARA/Elastic/Splunk/Suricata-Snort/Defender/CrowdStrike/other all accounted for. |
| PUBLISHED rule body copied exactly | PASS | Rule 1 (Sigma `0aba5685…`) verbatim; no paraphrase in any code block. |
| Unfetched body → `Content not retrieved` | PASS | Rule 2 (`540703fb…`) metadata in prose, body left `Content not retrieved`. |
| Proprietary EDR → `SOURCE_UNAVAILABLE (vendor-internal)` | PASS | Defender + CrowdStrike, not invented. |
| Scoped negatives name platforms checked | PASS | YARA/Elastic/Splunk/Suricata = NO_RULES_FOUND. |
| SNIPPET_ONLY never used as a rule body | PASS | Sentinel/SOC Prime/Sumo listed in matrix, no body claimed. |

Detection sources: DS1 detection.fyi mirror (C2, FETCHED_FULL), DS2 controlassurance mirror (C2, PARTIAL — metadata only), canonical raw SigmaHQ 404 (A2, FAILED), others SNIPPET_ONLY.
Observations: section forced out a real finding — the main public Sigma rule keys on the **v1** workflow filename and would likely miss 2.0's renamed workflows; the command-line rule (`SHA1HULUD`) does catch a 2.0 artefact. Friction: raw SigmaHQ paths 404 via `web/fetch` (needs a GitHub-aware fetch or accept graded mirror bodies); exact-copy depends on the retriever not summarising (DS2 refused → correctly degraded).

**Not yet tested:** rows 2 (actor), 3 (indicator), 4 (ambiguous scope), 5 (CVE-misroute), 6 (no-reporting); and any Cline+Tavily run. Open carry-overs: raw-rule fetch reliability; Admiralty rubric; verbatim preservation under `web/fetch`.
