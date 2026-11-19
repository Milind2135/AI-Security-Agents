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
- When a subagent returns its report, **show the user the complete report verbatim** — copy its final message exactly, from its first line (`<name> vX.Y | result`) through its last line (e.g. `Validation: NOT RUN (chat mode).`), including the JSON block, open questions and improvement proposals. Do not summarise, shorten, reformat or add commentary inside it; put any comments after it. Then, only if asked, compare it with `tests/<name>/README.md`.
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

## Constraints the agents must respect
- Target runtimes: **Claude Code** (testing now) and **GitHub Copilot in VS Code** (work environments). Cline with OpenRouter free models is legacy (free models change often; 50 requests/day). Agents must be self-contained (do not rely on `AGENTS.md` being loaded), use runtime-neutral tool roles (page fetch, web search) with a mapping table, keep budgets, and avoid pulling whole web pages into context.
- Agents never create/edit files or run commands unless that is their explicit purpose; containment/changes are written as `REQUIRES APPROVAL — <role>: <action>`.
