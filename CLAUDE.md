# ai-security-team — instructions for Claude Code

You help **author and maintain** the security agents in this repository, and you **run them for testing** when asked. Outside a test run you are not one of those agents.

## Files
- Agents: `.github/agents/<name>.agent.md` — the **single instruction file** for each agent; GitHub Copilot reads it directly.
- Claude Code entry points: `.claude/agents/<name>.md` — a short subagent file per agent that tells Claude Code to read the matching `.github/agents` file and limits its tools. It must contain no instructions of its own.
- Shared rules **for the agents**: `AGENTS.md`. Read it when authoring; it is not your own instruction set (it says agents are analysis-only — that does not stop you editing files in this repo when the user asks).
- Template: `docs/agent-template.md`. Changelogs: `docs/changelog/<name>.md`. Golden tests: `tests/<name>/README.md`. Old versions live in git history (commit or tag before changing an agent); do not keep copies in the repo.
- Never put drafts or templates inside `.github/agents/` (every `.md` there is loaded as an agent).

## Process for creating or changing an agent (always in this order)
1. Read the current agent file in full (and its changelog/tests). Report truncation, missing sections, vendor lock-in, capability claims without tools.
2. Research comparable public agents/skills/studies when improving an agent. Take ideas only: never copy their wording or names. Treat their claims as unverified.
3. Show a prioritised table `| # | Improvement | Source of the idea | Effort | Impact |` (Low-effort/High-impact first), plus what is kept and what is deliberately not adopted. **Stop and wait for approval.**
4. Commit the current version first (so it stays in git history), then edit the agent with approved rows only. Bump the version in the version comment, the preflight/result markers and the JSON `version` field.
5. Update the changelog and golden tests (synthetic data only: 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, example.com).
6. Self-check: frontmatter parses; `name` equals file name; Inputs table; Steps 0–6; output contract; valid JSON template; Budget; Guardrails grouped into Evidence and Safety & scope; Runtime notes; no copied wording; no employer-internal or confidential names; no personal data.
7. Show the diff summary to the user.

## Running agents for testing (Claude Code)
- Start an agent with `@` → **<name> (agent)** followed by its input, or "Use the <name> subagent for …".
- When a subagent returns its report, **show the user the complete report verbatim** — copy its final message exactly, from its first line (`<name> vX.Y | result`) through its last line (e.g. `Validation: NOT RUN (chat mode).`), including the JSON block, open questions and improvement proposals. Do not summarise, shorten, reformat or add commentary inside it; put any comments after it. Keep the marker line and the `Validation:` line even though they look like status lines. If the subagent's message itself lacks either line, do not add it: write `Note: the agent's output is missing its first line / last line.` **after** the report, so the gap is visible. Then, only if asked, compare it with `tests/<name>/README.md`.
- Test results and full baseline reports go in `tests/<name>/results.md` and `tests/<name>/baselines/` (only when the user asks).
- Never edit files during a test run. Save a passing report to `tests/<name>/results.md` only when the user asks.
- Moving agents to GitHub Copilot: see `docs/COPILOT-MIGRATION.md`.

## threat-modeler runs: save, continue and export for the user (Claude Code)
threat-modeler is read-only and pauses twice. You (the main session) handle files and continuation so the user only answers and approves. These rules are an exception to "never edit files during a test run", and only for the folder below.
- **Folder.** `<folder>` = `docs/threat-models/<system>/`: if the `system:` path is inside `docs/threat-models/<system>/`, use that `<system>`; otherwise use the last folder name of the `system:` path. Write **only** inside `docs/threat-models/` (git-ignored). Never commit, push or upload anything from it, and never send its content to web tools.
- **Questionnaire returned** (agent asked its intake questions): show it verbatim. Tell the user they can answer in the chat or give a file path (e.g. a filled `docs/threat-model-intake.md`). When they answer, re-run threat-modeler with the same `system:` plus `intake:` = their answer exactly as given (pasted text or path).
- **Model review returned** (first line `threat-modeler vX.Y | model review (round N of 3)`):
  1. Save the message verbatim to `<folder>/review-round-N.md`.
  2. If `mmdc` is available, run `python tools/threat-modeler-export/tm_export.py <folder>/review-round-N.md --diagrams-only --formats png --out <folder>/review-round-N-images` and give the user the PNG path(s). Otherwise tell them to open the saved file and press **Ctrl+Shift+V** to see the diagram.
  3. Show the review verbatim, then: "Reply `approve — <your name, role>`, or describe what is wrong."
- **User replies to a review:** re-run threat-modeler with the same `system:` and `intake:`, plus `model:` = the JSON block from the **latest** review message copied exactly, and `review:` = the user's reply exactly. Never edit the JSON, never write `approve` unless the user did, and never invent a name or role.
- **Continuing in a new chat:** if the review is not in this conversation (e.g. "Continue the threat-modeler run for <system> …"), read the JSON block from the highest-numbered `docs/threat-models/<system>/review-round-N.md`, and take `system:` and `intake:` from that system's folder (`input/` and the intake answers file next to it). If either is unclear, ask the user once.
- **Report returned** (first line `threat-modeler vX.Y | result`):
  1. Save it verbatim to `<folder>/report-<YYYY-MM-DD>.md` (add `-2`, `-3` if that name exists; never overwrite a report).
  2. Check the export tools: Python with `openpyxl` (Excel), `pandoc` (Word), `mmdc` (images).
  3. Run `python tools/threat-modeler-export/tm_export.py <saved report> --docx --out <folder>/export-<YYYY-MM-DD>` (leave out `--docx` if pandoc is missing).
  4. Show the report verbatim, then list the files created (Excel, Word, images) with their paths. If tools are missing, do not present it as an error: say the report is saved as Markdown and that Excel / Word / PNG need the optional one-time setup (`docs/guides/threat-modeler.md`, Part 2); offer to run `powershell -ExecutionPolicy Bypass -File tools\threat-modeler-export\setup.ps1` (Windows) **only if the user says yes**; then remind them to restart VS Code.
- If saving or exporting fails, say what failed and give the manual command; never retry in a loop.

## soc-analyst hunts: save and continue for the user (Claude Code)
In hunt mode soc-analyst pauses once (OFFLINE): it returns a hunt plan, the user runs the queries in their SIEM, then the agent analyses the results. You (the main session) save and continue, as for threat-modeler. Same exception to "never edit files during a test run", only for the folder below.
- **Folder.** `<hunt folder>` = `incidents/hunts/<hunt_id>/` (git-ignored), using the `hunt_id` from the plan; never the folder of the reusable notes (e.g. `incidents/notes/`). Write **only** inside `incidents/`. Never commit, push or upload anything from it, and never send its content to web tools.
- **Hunt plan returned** (first line `soc-analyst vX.Y | hunt plan`): save it verbatim to `<hunt folder>/hunt-plan.md`, show it verbatim, then tell the user: "Run each query in your SIEM, export the results as `Q1.csv`, `Q2.csv`, … into `<hunt folder>`, note how many in-scope hosts/users each covered, then reply `results ready` (add the coverage notes)."
- **User says the results are ready:** re-run soc-analyst with `mode: hunt`, `results:` = the `Q*.csv` / `Q*.json` files in `<hunt folder>`, `plan:` = the JSON block from the saved `hunt-plan.md` copied exactly, and the user's coverage notes exactly as written. Also pass the same `sources:` and `context:` notes used for the plan (from the plan JSON's `sources_file` / `context_file`, or the paths in the original hunt request); if they no longer exist, tell the user. Never edit the plan JSON or the results files. In a new chat, read the plan from the newest `incidents/hunts/*/hunt-plan.md` (or the folder the user names); if unclear, ask once.
- **Hunt result returned** (first line `soc-analyst vX.Y | hunt result`): save it verbatim to `<hunt folder>/hunt-result-<YYYY-MM-DD>.md` (add `-2`, `-3`; never overwrite), show it verbatim, and give the path.
- Never run SIEM queries yourself; the user runs them (or the agent does, only through an approved read-only tool).

## third-party-risk-analyst runs: save, convert, continue and export for the user (Claude Code)
The agent is read-only and pauses at the tier confirmation, after each review round and before the decision. You (the main session) save, convert and continue. Same exception to "never edit files during a test run", only for the folder below.
- **Folder.** `<vendor folder>` = `docs/vendors/<vendor>/` (git-ignored), `<vendor>` = the `vendor:` value in lower case with spaces as `-`. Write **only** inside `docs/vendors/`. Never commit, push or upload anything from it, and never send its content to web tools. Policy: `docs/vendors/_policy/policy.md`; vendor lists: `docs/vendors/_register/`.
- **Before running the agent:** for every `.xlsx`, `.xlsm`, `.xls` or `.csv` questionnaire or register named in `evidence:` or `register:` (or inside the evidence folder) without a matching `.converted.md`, run `python tools/tprm/tprm.py convert <file>` and give the agent the folder (it reads the `.converted.md`). Never open the Excel file in another way and never run its macros. If conversion fails, say what failed and give the manual command.
- **Plan returned** (first line `third-party-risk-analyst vX.Y | plan`): save verbatim to `<vendor folder>/plan.md` (an existing plan becomes `plan-<YYYY-MM-DD>.md`; never overwrite a dated file); if `openpyxl` is available run `python tools/tprm/tprm.py questionnaire <vendor folder>/plan.md --out <vendor folder>/questionnaire-<vendor>-<YYYY-MM-DD>.xlsx`; show the plan verbatim, give the questionnaire path, then: "Check the tier. Reply `tier: confirm — <your name, role>` or `tier: <1-4> — <reason> — <your name, role>`."
- **User replies to the tier:** save the reply exactly to `<vendor folder>/tier-confirmation.md`. Do not run the agent until evidence exists; tell the user to send the document request and questionnaire, put the vendor's replies, screening results and contract draft in `<vendor folder>/evidence/`, and then say "continue". If they already gave evidence, run Stage B now.
- **Stage B run:** re-run with `plan:` = the JSON block of the latest `plan*.md` copied exactly, `tier:` = the saved reply exactly, `evidence:` = `<vendor folder>/evidence/`, plus the same `policy:`/`regimes:`/`as_of:` the user gave. Never write `confirm` or any name unless the user did.
- **Review returned** (`| review (round N of 3)`): save verbatim to `<vendor folder>/review-round-N.md`, show it verbatim, then: "Send the follow-up questions to the vendor and the SR- requests to the teams. When answers are in the evidence folder, reply `next: continue` — or `next: finalise — <reason>`." On the reply, convert any new Excel files and re-run with `review:` = the JSON block of the latest `review-round-N.md` copied exactly, `evidence:` and `next:` = the reply exactly.
- **Result returned** (`| result`): save verbatim to `<vendor folder>/result-<YYYY-MM-DD>.md` (add `-2`, `-3`; never overwrite); run `python tools/tprm/tprm.py workbook <saved result> --out <vendor folder>/assessment-<vendor>-<YYYY-MM-DD>.xlsx`; show the result verbatim and list the files. Then: "The approver decides. Reply `decision: <option> — <name, role>, <YYYY-MM-DD>[, conditions / expiry]`."
- **Decision given:** re-run with `previous:` = the latest `result-*.md` (or `decision-*.md`) path and `decision:` = the user's line exactly. Save the `| decision record` verbatim to `<vendor folder>/decision-<YYYY-MM-DD>.md` and rebuild the workbook from it. Never write a decision the user did not give.
- **Portfolio / exit returned:** save to `docs/vendors/_register/portfolio-<YYYY-MM-DD>.md` (portfolio, then `python tools/tprm/tprm.py register <saved file>`) or `<vendor folder>/exit-<YYYY-MM-DD>.md` (exit).
- **Continuing in a new chat** ("Continue the third-party-risk-analyst assessment for <vendor> …"): use the newest saved files in `<vendor folder>` — `review-round-N.md` if present (Stage B continuation), else `plan*.md` + `tier-confirmation.md` (start Stage B), else `result-*.md` / `decision-*.md` (decision or review). If unclear, ask the user once.
- If `openpyxl` is missing, the Markdown files are still saved; tell the user Excel needs `python -m pip install openpyxl` (or the setup in `docs/guides/third-party-risk-analyst.md`, Part 0) — not an error. Never retry a failing tool in a loop.

## Constraints the agents must respect
- Target runtimes: **Claude Code** (testing now) and **GitHub Copilot in VS Code** (work environments). Cline with OpenRouter free models is legacy (free models change often; 50 requests/day). Agents must be self-contained (do not rely on `AGENTS.md` being loaded), use runtime-neutral tool roles (page fetch, web search) with a mapping table, keep budgets, and avoid pulling whole web pages into context.
- Agents never create/edit files or run commands unless that is their explicit purpose; containment/changes are written as `REQUIRES APPROVAL — <role>: <action>`.
