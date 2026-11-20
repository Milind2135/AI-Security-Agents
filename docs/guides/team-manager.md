# team-manager: how to use it

team-manager is the **coordinator** of the agent team. You give it a security request in plain words. It tells you **which agents (or human teams) should handle each part, in what order, and with exactly which prompt**. When the agents have done their work, it **combines their reports** into one summary in which every conclusion names its source. It never investigates, looks anything up, or takes actions itself.

Agent instructions: [`.github/agents/team-manager.agent.md`](../../.github/agents/team-manager.agent.md) · Tests: [`tests/team-manager/`](../../tests/team-manager)

> **Data rule:** alerts, logs and inventories are sensitive. Use them only with an AI service your organisation has approved. Keep case material under `incidents/<case>/`, which is git-ignored so nothing is pushed.

## When to use it

| Use team-manager when… | Example |
|---|---|
| You're not sure which agent to use | "We got a strange login alert and the user also reported a phishing email." |
| A request needs several agents in order | "Are we affected by CVE-2021-44228, and how urgent is it?" (vm-triage, then vulnerability-hunt) |
| You have several agent reports and need one answer | soc-analyst and threat-intel-analyst reports about the same incident |

For a single, clear job (one alert, one CVE), go straight to that agent.

## The team it routes to

| Agent | Handles |
|---|---|
| [vm-triage](vm-triage.md) | Public facts about one CVE |
| [vulnerability-hunt](vulnerability-hunt.md) | Whether a CVE affects **your** assets (needs vm-triage's JSON + an inventory) |
| [soc-analyst](soc-analyst.md) | One alert, or a small group of related alerts; with `mode: hunt`, hunting in your own logs ("were we breached?", "are other hosts affected?") |
| [cloud-security-analyst](cloud-security-analyst.md) | Cloud alerts, or cloud posture from IaC and IAM exports |
| [threat-modeler](threat-modeler.md) | Threat model of one system's design |
| [threat-intel-analyst](threat-intel-analyst.md) | A threat actor, campaign or set of indicators |

Some work always goes to **people**, never to an agent: incident response, writing or deploying detection rules, pipeline and infrastructure changes, risk acceptance, and containment such as isolating a host or resetting passwords. These appear in the plan as `REQUIRES APPROVAL — <role>: <action>`.

## Plan → run → combine (Claude Code)

In Claude Code, team-manager **plans and combines**. It cannot start the other agents itself, so you run each step's prompt. Replace `<case>` with a short case name (e.g. `2026-11-npm-alert`).

### Step 1: Put the evidence in a case folder

Save alerts, logs, inventories and other files in `incidents/<case>/`. Don't drop files into the chat box: agents only read files saved in the project folder.

### Step 2: Ask for a plan (Claude Code chat)

```text
Use the team-manager subagent. request: CrowdStrike and Elastic both alerted on a malicious npm package on a developer laptop — incidents/<case>/crowdstrike.json incidents/<case>/elastic.json. What should we do? Show me the complete output verbatim.
```

You get a **plan** (first line `team-manager vX.Y | plan`):

| Section | What it shows |
|---|---|
| Plan | Each step: which agent or human team, why, what input it needs, what it depends on, and when to run it (`now`, `can run in parallel`, `conditional — <condition>`, `blocked`) |
| Missing inputs | Anything you still need to supply, e.g. `MISSING — inventory export — needed by step 3` |
| Prompts | A **ready-to-copy prompt for each agent step** |
| Human decisions | `REQUIRES APPROVAL` actions for named roles, e.g. isolating the laptop |
| Next action | What to do next |

### Step 3: Run each step (Claude Code chat)

Copy each prompt from the plan **in order** and send it, for example:

```text
Use the soc-analyst subagent. alert: incidents/<case>/crowdstrike.json incidents/<case>/elastic.json Show me the complete report verbatim.
```

After each agent finishes, save its report:

```text
Save the complete soc-analyst report above verbatim to incidents/<case>/report-soc-analyst.md
```

If a later step needs an earlier step's JSON (the plan shows `<JSON from step N>`), save that JSON block as a file and give its path, e.g.:

```text
Save only the JSON block from the vm-triage report above to incidents/<case>/vm-triage-CVE-2021-44228.json
```

- Run only steps marked `now` or `can run in parallel`.
- Run `conditional` steps only when their condition has become true (e.g. "run threat-intel-analyst if the alert names a campaign").
- Steps for human teams are for people: send those to the team concerned.

### Step 4: Combine the reports (Claude Code chat)

```text
Use the team-manager subagent. reports: incidents/<case>/report-soc-analyst.md incidents/<case>/report-threat-intel-analyst.md request: Combine these into one summary for the incident lead. Show me the complete output verbatim.
```

You get **one summary** (first line `team-manager vX.Y | result`):

| Section | What it shows |
|---|---|
| Executive summary | Up to 5 sentences, each with its source |
| Report register | Which reports were used, their versions, dates and confidence |
| Combined findings | Every finding tagged with its source, e.g. `[soc-analyst §6 F-02]` |
| Agreements and conflicts | Where reports disagree: both values shown as `CONFLICT — for human review`, never quietly settled |
| Not found in any report | Anything in the summary or your request that no report supports (a built-in check against made-up facts) |
| Gaps | Steps not run, missing reports, missing inputs |
| Next steps and human decisions | Further agent steps (with prompts) and `REQUIRES APPROVAL` actions |
| Confidence | Never higher than the weakest report a key conclusion relies on |

## Try it with test data

Combine two synthetic reports that disagree, plus one from an unknown source:

```text
Use the team-manager subagent. reports: tests/team-manager/fixtures/c1-soc-analyst.json tests/team-manager/fixtures/c1-threat-intel-analyst.json tests/team-manager/fixtures/c1-unknown-agent.json request: Combine these. Show me the complete output verbatim.
```

Expected: the IP `203.0.113[.]45` shown as a **CONFLICT**, and the unknown report marked **unverified** with its hidden instruction ignored. Full answer key: [`tests/team-manager/README.md`](../../tests/team-manager/README.md).

## What team-manager will never do

- Investigate or analyse evidence itself
- Answer an agent's question on your behalf (e.g. threat-modeler's diagram review)
- Use a report from an unknown source for its conclusions; such reports are listed as "unverified" and any instructions inside them are ignored
- Isolate, block, reset, deploy rules, create tickets, accept risk or close incidents: always `REQUIRES APPROVAL` for a named person

## In GitHub Copilot

Pick **team-manager** in the agent dropdown and send the same request. Copilot may also allow **run mode**: add `mode: run` and the plan ends with *Reply "approve plan"*. After you approve, Copilot runs the agents itself and combines their results. **Not yet tested:** if the agent's first line shows `agent call: none`, it falls back to a plan, and you run the steps as above.

## Quick reference

| Input | Purpose |
|---|---|
| `request:` | What you need, with file paths (required) |
| `reports:` | Agent reports to combine (paths or pasted) |
| `mode: plan` / `mode: run` | Plan only (default) / run the agents (Copilot only, after `approve plan`) |
| `context:` | Environment notes: cloud providers, where inventories live, team names |
| `depth: thorough` | Passed on to every agent for deeper research |
| `?` | Print the usage card |
