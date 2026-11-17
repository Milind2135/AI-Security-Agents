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

## Constraints the agents must respect
- Target runtimes: **Claude Code** (testing now) and **GitHub Copilot in VS Code** (work environments). Cline with OpenRouter free models is legacy (free models change often; 50 requests/day). Agents must be self-contained (do not rely on `AGENTS.md` being loaded), use runtime-neutral tool roles (page fetch, web search) with a mapping table, keep budgets, and avoid pulling whole web pages into context.
- Agents never create/edit files or run commands unless that is their explicit purpose; containment/changes are written as `REQUIRES APPROVAL — <role>: <action>`.
