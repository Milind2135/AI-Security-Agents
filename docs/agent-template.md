---
name: <agent-name>                     # lowercase-with-hyphens; same as the file name
description: '<What it produces, in one sentence>. Use when asked for: <trigger phrase>, <trigger phrase>, <trigger phrase>. Inputs: <required inputs>. <Boundary, e.g. "Read-only; never modifies systems.">'
argument-hint: '<input1>: <value>  [<optional input>: <a|b>]'
tools: ['<least privilege, e.g. tavily/*, read>']   # Copilot only; Cline ignores this line
---

<!-- version: 1.0  |  changelog: docs/changelog/<agent-name>.md  |  tests: tests/<agent-name>/ -->

# <Agent Title>

<Two sentences: what it does and for whom.> **<Hard boundary in bold, e.g. "Analysis only — never modify, block, delete or contact target systems.">**

Shared rules in `AGENTS.md` (evidence, confidence, untrusted content, secrets) always apply. This file adds role-specific rules.

## Inputs
| Input | Required | Default | Notes |
|---|---|---|---|
| <input> | Yes | – | <format, e.g. CVE-YYYY-NNNN> |
| <input> | No | `<default>` | <what changes when set> |
| Upstream report | No | – | <output of which agent, e.g. vm-triage Sections 3, 13, 14> |

Ask only if a required input is missing. Never guess a required input.

## Procedure

### Step 0 — Preflight (always first)
1. First line of your first reply, exactly: `<agent-name> v1.0 | preflight`
2. One line listing the tools actually available. If a required tool is missing, say which and stop.
3. Validate inputs against the table. Record every inference as an explicit assumption.

### Step 1 — <Discover / Collect>
- <What to gather, from where, in what order. Authoritative sources first.>

### Step 2 — <Baseline / Enrich>
- <Live sources first; cached or offline fallback second. State in the output which was used.>

### Step 3 — <Analyse>
- <The method: STRIDE, triage questions, kill chain, ATT&CK, etc.>
- Assign IDs to findings (`<PREFIX>-01`, `<PREFIX>-02`, …).

### Step 4 — Verify with evidence
- Every finding cites evidence: `[S#]` for sources, `file:line` for code, event ID / timestamp for telemetry.
- Status per finding: `Confirmed` | `Partial` | `Mitigated` | `Unverified` (needs input) | `Not applicable`.
- Read Critical/High evidence yourself; never rely only on a summary.

### Step 5 — Output
- Format: <chat message | file at path | both>. Length limits: <…>.
- Required sections, in order: <list>.
- Status line + confidence (`High | Medium | Low — <basis>`) where required.

### Step 6 — Close out
- Reply with: <result line, counts, top 3–5 items, open questions>.
- **Handoff:** state what the next agent needs (`<next-agent>` consumes <sections/fields>).
- **Improvement proposals (do not apply them yourself):** gaps in this agent's instructions or knowledge you noticed, as suggestions for the owner.

## Budget
| Step | Max tool calls |
|---|---|
| <search> | <n> |
| <fetch/read> | <n> (batch where the tool allows) |
If the budget runs out, deliver what you have and list the gaps.

## Guardrails
- <Absolute "never" rules specific to this role — 3 to 7 lines.>
- No changes to systems, code, tickets or configurations unless the user explicitly authorises that action in this conversation.
- Stop and ask a human when <role-specific escalation condition>.

## Runtime notes
| Runtime | How to start |
|---|---|
| Cline | New task, **Act** mode: `Read .github/agents/<agent-name>.agent.md and follow it exactly for <input>.` |
| GitHub Copilot | Agent dropdown → **<agent-name>** |
