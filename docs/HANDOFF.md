# Handoff — agent work status (updated 2026-11-17)

Summary of the work done in a Claude.ai session, so a new session (e.g. Claude Code) can continue. Details are in each agent's changelog under `docs/changelog/`.

## Agents
| Agent | Version | State | Notes |
|---|---|---|---|
| `vm-triage` | 5.4 | Live after move (5.3 added help mode `?`; 5.4 adds remediation and SSVC inputs to the JSON handoff); **passed** Claude Code tests (CVE-2021-44228 on v5.0, CVE-2024-3400 on v5.1) | Portable: `.github/agents/vm-triage.agent.md` + Claude Code entry `.claude/agents/vm-triage.md`. NVD JSON primary. Baselines in `tests/vm-triage/baselines/`, results in `tests/vm-triage/results.md`. |
| `soc-analyst` | 2.2 | Live (2.2 adds the fixed usage card), untested | Entry `.claude/agents/soc-analyst.md`. Vendor-neutral alert triage; LIVE/OFFLINE; E# evidence log; 7-row disposition decision table (adds MALICIOUS BLOCKED — CLOSE); human confirms. Synthetic fixtures + answer key in `tests/soc-analyst/`. |
| `vulnerability-hunt` | 1.5 | Live, portable; re-test pending (1.4 usage card; 1.5 business impact → system or risk owner) | Entry `.claude/agents/vulnerability-hunt.md`. Stage 2 after vm-triage: installed / affected / exposed; six asset statuses; SSVC-style decision; ticket drafts, creation only with `ticketing: create`. Scenario 1 history: v1.1 took fix data from memory → fixed in 1.2; v1.2 marked uncovered assets NOT DETECTED → fixed in 1.3. Replaced `vulnerability-analyst` (archived). |
| `team-manager` | 2.0 | Live after move, **untested** | Renamed from `team-lead` and rebuilt 2026-11-17: roster of 6 agents + human teams; 13-row routing table; modes plan (default) / run (Copilot `agent` tool, untested) / combine (`reports:`) with grounding check and conflicts for human review. Entries `.claude/agents/`, `.codex/agents/`. 9 golden tests in `tests/team-lead/`. |
| `threat-intel-analyst` | 3.0 | Live after move, **untested** (renamed from `intelligence-analyst` 2026-11-17) | Portable (core rules in file, tool roles, verbatim fetch, no-search fallback), usage card, entries `.claude/agents/` and `.codex/agents/`. Scope modes actor/campaign/indicator; STIX-aligned handoff; Admiralty grading; estimative language; only public identifiers looked up. Live feeds (TAXII/MISP/dark-web) remain a tool-gated extension. 8 golden tests in `tests/threat-intel-analyst/`. |
| `threat-modeler` | 1.5 | Live, untested (1.4 usage card; 1.5 business impact → risk owner) | Intake → crown jewels/entry points → readiness → DFD + deployment diagram + tiers + critical interactions → human DFD review → threats → vulnerabilities → control validation (9 tests) → risks → classify → prioritise → treatment/residual → 14-section report + CSV + JSON; assumptions register; agent self-protection guardrails. Exporter `tools/threat-modeler-export/` (PNG/JPEG/SVG, xlsx, docx). 18 golden tests. |
| `cloud-security-analyst` | 2.1 | Live, untested (2.1 business impact → system or risk owner) | Two modes: posture (attack paths: factor table E/W/P/D/L/X, IAM privilege escalation with prerequisites and role chains, guardrail validation, logging gaps) and triage (correlate first, always-escalate categories, 7-row disposition, exposure state). Usage card. Entries `.claude/agents/`, `.codex/agents/`. 8 golden tests in `tests/cloud-security-analyst/`. |
| `detection-engineer` | – | **Removed** from GitHub 2026-11-17 (kept locally, git-ignored) | Detection work goes to the detection / SOC engineering team (team-manager 2.0 routes it there). Other agents' handoff lines still name it until the planned repoint. |
| `threat-hunter`, `devsecops-engineer` | – | **Deleted** from the repository | Still named in some handoffs (threat-hunter is planned for rebuild). |
| `risk-analyst` | – | **Removed** from GitHub 2026-11-17 (kept locally, git-ignored) | Business-impact questions now go to the system or risk owner (threat-modeler 1.5, cloud-security-analyst 2.1, vulnerability-hunt 1.5). team-manager 2.0 routes it to the owner. |

Pipeline: `vm-triage` → `vulnerability-hunt` → `threat-hunter` (planned; affected + exposed assets only) → system or risk owner (business impact).

## Runtimes (decided 2026-11-02)
- **Claude Code** in VS Code for testing now; **GitHub Copilot** in VS Code for the office later (see `docs/COPILOT-MIGRATION.md`).
- Cline + OpenRouter free models is legacy: `poolside/laguna-s-2.1:free` was retired on 2026-10-31 and other free models did not work reliably.
- Pattern for every agent: instructions only in `.github/agents/<name>.agent.md`; a thin entry `.claude/agents/<name>.md` for Claude Code.

## vm-triage test history (CVE-2021-44228)
- Free models `nvidia/nemotron-3.5-lightning:free` and `liquid/lfm-2.5-2.6b:free` could not follow the workflow.
- With `poolside/laguna-s-2.1:free` and size limits in the prompt, v4.2 produced all 26 sections. Strengths: correct KEV and CVSS, honest EPSS NOT_AVAILABLE. Problems that led to v4.3: missed the 2.15.0 CNA-data-vs-description conflict and CWE-917; outdated fix advice (no follow-on CVEs); snippets cited as facts; non-standard status words; paraphrased "published" rule; weak ATT&CK mappings; 2× over budget.
- An earlier run stalled at ~125k tokens of fetched pages; Cline shows ~65.5k context for this model.

## Known runtime behaviour (Cline)
- Start agents with: `Read the existing file .github/agents/<name>.agent.md (never create or edit it) and follow it exactly for <input>. No terminal commands.` Or paste the file contents into the prompt.
- Reject any command or file creation the agent attempts; approve only its listed tools (vm-triage: `tavily_search`, `tavily_extract`).
- When correcting a run, always restate the input (e.g. the CVE ID).
- `tavily_extract` cannot read JSON API endpoints (e.g. the FIRST EPSS API).
- Use synthetic data only with free models.

## Next steps (in order)
1. ~~Test `vm-triage` in Claude Code~~ **Done 2026-11-02** (two passing baselines). Optional: quick re-run of v5.2 to confirm the S2-primary change and the complete relay.
2. Convert ~~`soc-analyst`~~ (done, v2.1), ~~`vulnerability-hunt`~~ (done, v1.3) and ~~`intelligence-analyst`~~ (done 2026-11-17 as `threat-intel-analyst` v3.0) to the portable pattern (tool roles, self-contained rules, `.claude/agents` entry), then test each in Claude Code.
3. ~~Restructure `intelligence-analyst`~~ **Done 2026-10-27 (v2.0).** Now test it with its golden tests (`tests/threat-intel-analyst/`: campaign/actor/indicator, help, internal identifiers), alongside soc-analyst and vulnerability-hunt.
4. ~~Rebuild `team-lead`~~ (now `team-manager`) **Done 2026-11-17 (v2.0).** Test plan and combine modes in Claude Code; test `mode: run` in Copilot at the office.
5. Later: orchestration via team-manager once individual agents pass their tests.

## Housekeeping to check
- `README.md` at the repo root (6,252 bytes) appears to be a copied kit README; the original may need recovering from git history.
- `check_core.py` at the repo root and the old `tools/`, `templates/`, `tests/` items from an earlier kit — confirm whether still needed (earlier kit files are in `archive/vm-triage-kit-unused/`).

## Lesson (2026-11-03)
Before an agent's first test, review every rule for wording a model could read two ways (statuses, decisions, controls, numbering). In vulnerability-hunt, five such rules gave different results between two identical runs.
