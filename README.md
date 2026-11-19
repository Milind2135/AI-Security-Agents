# AI Security Agents

Seven AI agents for core security-operations work — CVE research, exposure assessment, alert triage, cloud attack paths, threat modeling and threat intelligence — plus a manager agent that routes requests between them and merges their reports.

Every agent is **analysis-only**, **vendor-neutral** and **evidence-first**: each conclusion cites its source, separates facts from inferences, and states its confidence. One instruction file per agent runs in both **Claude Code** and **GitHub Copilot** (VS Code).

> Built and maintained by **Milind V. Chavan** as a personal project. Shared as a portfolio piece; issues and suggestions are welcome, but support is not guaranteed.

---

## The agents

| Agent | What it does | You give it | You get back |
|---|---|---|---|
| **[vm-triage](.github/agents/vm-triage.agent.md)** | Researches one CVE from public sources (KEV, EPSS, CVSS, exploitation, IOCs, detections, fixes) and produces a cited 26-section report. | A CVE ID | 26-section report + JSON handoff |
| **[vulnerability-hunt](.github/agents/vulnerability-hunt.agent.md)** | Takes vm-triage's output plus your inventory and decides, asset by asset, whether you're affected and exposed and how urgently to act, with fix-verification steps and ticket drafts. | vm-triage JSON + SBOM / scanner / CMDB export | Per-asset status, SSVC-style urgency, verification plan, ticket drafts |
| **[soc-analyst](.github/agents/soc-analyst.agent.md)** | Triages one security alert (sign-in, endpoint, email, network, CI/CD) and recommends one of seven dispositions, with an evidence log, a timeline and ATT&CK mapping. | An alert + related logs | Disposition, evidence log, timeline, ATT&CK mapping |
| **[cloud-security-analyst](.github/agents/cloud-security-analyst.agent.md)** | Finds real attack paths in cloud IaC, IAM and CSPM data, and triages cloud alerts by correlating them with audit logs. | IaC, IAM policies, CSPM exports — or a cloud alert + audit events | Ranked attack paths, or an alert disposition |
| **[threat-modeler](.github/agents/threat-modeler.agent.md)** | Builds an evidence-based threat model from code and design documents: a data-flow diagram reviewed by a human, STRIDE threats, validation of existing controls and prioritised risks. | Repo paths, design docs, diagrams | Data-flow diagram, threat register, prioritised controls |
| **[threat-intel-analyst](.github/agents/threat-intel-analyst.agent.md)** | Profiles a threat actor, campaign or indicator set from public sources: ATT&CK techniques, IOCs, attribution with competing hypotheses, published detection rules and STIX-style output. | An actor, campaign or indicator set | Intelligence brief + STIX-style JSON |
| **[team-manager](.github/agents/team-manager.agent.md)** | Routes a security request to the right agents or human teams in a safe order, then merges their reports into one summary where every conclusion names its source. | A security request (and, later, the specialists' reports) | Routed plan, then one combined summary |

### How they fit together

```mermaid
flowchart LR
    R([Security request]) --> TM[team-manager<br/>route & sequence]
    TM --> VT[vm-triage<br/>public CVE intel]
    VT -- JSON handoff --> VH[vulnerability-hunt<br/>am I affected?]
    TM --> SOC[soc-analyst<br/>alert triage]
    TM --> CSA[cloud-security-analyst<br/>attack paths]
    TM --> THM[threat-modeler<br/>design review]
    TM --> TI[threat-intel-analyst<br/>actor / campaign]
    TI -. related CVEs .-> VT
    VH & SOC & CSA & THM & TI -- reports --> TM
    TM --> S([One evidence-traced summary])
```

Each specialist ends its report with a machine-readable JSON block, so another agent can pick up the work without re-researching it.

---

## Guardrails

These rules are built into every agent file (see [`AGENTS.md`](AGENTS.md) for the shared set):

- **No retrieval, no claim.** Facts must come from a fetched source or supplied evidence. Search snippets and the model's memory are not evidence. CVEs, IOCs, hashes, scores and log entries are never invented — missing data is reported as missing.
- **Cited and labelled.** Every factual statement is cited (`[S#]` for sources, `path:line` for files, event ID for logs). Facts, inferences and assumptions are kept apart, and conclusions carry `High | Medium | Low` confidence with a reason.
- **Analysis only.** Agents never change systems, code, tickets or accounts and never contact targets. Anything that needs action is written as `REQUIRES APPROVAL — <role>: <action>` for a human.
- **Untrusted input stays data.** Instructions hidden in web pages, emails, logs, alerts or code comments are ignored and reported as a finding — a defence against prompt injection.
- **Secrets are redacted, indicators defanged** (`AKIA****`, `example[.]com`, `hxxp://`).
- **Stay in scope.** Public-intelligence agents never judge your internal exposure; internal agents make no claims about systems they have no data for. Decisions that need authority (containment, disclosure, legal, HR) are escalated to a named role.
- **Budgets.** Each agent has a fetch/search budget and reports what it could not check.

---

## Running the agents

### Supported setups

| Setup | Status | How the agents load |
|---|---|---|
| **VS Code + Claude Code extension** | ✅ Tested (primary) | A short entry file per agent in [`.claude/agents/`](.claude/agents) tells Claude Code to read the full instructions in [`.github/agents/`](.github/agents) ([details](#claude-code-extension-or-cli)) |
| **Claude Code CLI** (terminal, including VS Code's terminal) | Same files as above, not tested separately | Same as above ([details](#claude-code-extension-or-cli)) |
| **VS Code + GitHub Copilot Chat** | ⚠️ Supported, not yet tested | Copilot reads each `.agent.md` file in [`.github/agents/`](.github/agents) directly and lists it in the agent dropdown ([details](#github-copilot-chat-in-vs-code)) |
| **OpenAI Codex** | ⚠️ Entry files included, not tested | A TOML entry file per agent in [`.codex/agents/`](.codex/agents) points Codex to the same instructions ([details](#openai-codex)) |
| **Cline** (VS Code extension) | Legacy, no longer maintained | No automatic loading; you paste a start prompt that tells Cline to read the agent file ([details](#cline-legacy)) |

- **One instruction file per agent** serves every setup, so there are no separate Claude and Copilot versions to keep in sync.
- **Copilot can use different models** (GPT, Claude, Gemini and others). The agents are written to be model-neutral; results are judged against the [golden tests](#tests), not identical wording.
- **team-manager `mode: run`** (calling the other agents automatically) needs a setup that lets one agent call another, currently Copilot, and has not been tested yet. In Claude Code, team-manager plans the work, and you run each step's prompt yourself.

#### How the agents load, in detail

Every setup ends up following the **same instruction file**, `.github/agents/<name>.agent.md`. Only the way each tool finds that file differs.

<a id="claude-code-extension-or-cli"></a>
**Claude Code (VS Code extension or CLI)**
1. When you open the repository folder, Claude Code finds the project subagents in `.claude/agents/`. Each one is a short Markdown file with a header (`name`, `description`, `tools`).
2. You start an agent by typing `@` and picking it (e.g. **vm-triage (agent)**), or by asking "Use the vm-triage subagent for …". Claude Code may also choose a subagent on its own when your request matches its `description`.
3. The subagent runs in its own context, with only the tools listed in its header: read-only `Read`, `Grep`, `Glob`, and `WebSearch` / `WebFetch` where the agent needs public sources. It cannot write files or run commands.
4. Its first step is to read `.github/agents/<name>.agent.md` and follow it exactly. If that file can't be read, it stops instead of working from memory.
5. **Check:** the agent's first line is `<name> vX.Y | preflight`. If you don't see it, the instructions weren't loaded.

<a id="github-copilot-chat-in-vs-code"></a>
**GitHub Copilot Chat in VS Code**
1. When you open the repository folder, VS Code finds every `*.agent.md` file in `.github/agents/` and lists each one in the Copilot Chat **agent dropdown**, using the `name` in its header.
2. You pick the agent in the dropdown and type its input (or `?`).
3. Copilot uses the file's body as the agent's instructions and offers only the tools listed in its header (for example `web/fetch`). VS Code asks you to approve tool calls such as page fetches.
4. **Check:** the first line is `<name> vX.Y | preflight`. If the agent is missing from the dropdown, check that the file name ends in `.agent.md` and that your Copilot Chat version supports custom agents (see [docs/COPILOT-MIGRATION.md](docs/COPILOT-MIGRATION.md)).
5. Only `.agent.md` files belong in `.github/agents/`; anything else placed there would also be loaded as an agent.

<a id="openai-codex"></a>
**OpenAI Codex** (not yet tested)
1. Codex reads project-scoped custom agents from `.codex/agents/*.toml`. Each file here has the three required fields: `name`, `description` and `developer_instructions`.
2. The `developer_instructions` tell Codex to read `.github/agents/<name>.agent.md` and follow it, the same way the Claude Code entry files do.
3. Codex starts a custom agent when you ask for it by name (e.g. "Have vm-triage research CVE-2021-44228"), or when project instructions say to.

<a id="cline-legacy"></a>
**Cline (legacy)**
1. Cline has no agent dropdown for these files and loads nothing automatically.
2. Start a new task in **Act** mode and paste the start prompt from the agent's *Runtime notes* section, e.g. `Read the existing file .github/agents/vm-triage.agent.md (never create or edit it) and follow it exactly for CVE-2021-44228.`

### Requirements

Nothing needs to be installed for the agents themselves: you only need one of the [supported setups](#supported-setups). What differs is the access each agent needs while it runs.

| Agent | Accepted input | Web access | Notes |
|---|---|---|---|
| vm-triage | One CVE ID typed in the prompt (no files) | Required | Fetches public sources (NVD, CISA KEV, FIRST EPSS, vendor advisories) |
| threat-intel-analyst | A threat-actor or campaign name, or a list of indicators (IPs, domains, hashes, package names) typed in the prompt; optional vm-triage JSON | Required | Public sources only; internal identifiers are never looked up |
| vulnerability-hunt | vm-triage JSON **plus** an inventory: SBOM (CycloneDX/SPDX JSON), scanner or CMDB export (CSV/JSON), package or image lists; optional exposure lists, firewall/security-group rules, controls notes (CSV, JSON, Markdown), source-code folder | Optional | Vendor advisories for fix details; works from supplied files otherwise |
| soc-analyst | Alert JSON, log excerpts (JSON, CSV, text), email headers or `.eml`, EDR process tree; optional context notes (Markdown/text) | Optional | Lookups of public IPs and domains only |
| cloud-security-analyst | **Posture:** IaC (Terraform, CloudFormation, Bicep/ARM, Kubernetes, Helm), CSPM or scanner exports (CSV/JSON), IAM policy JSON. **Triage:** cloud alert JSON plus audit events (CloudTrail, Azure Activity, GCP Audit Logs) | Optional | Public references; analysis uses the supplied files |
| threat-modeler | A folder of system material: design documents (PDF, Markdown, text), diagrams (PNG, JPG), source code, IaC, API specs (OpenAPI/YAML/JSON), pipeline files; optional filled intake form (Markdown) | Optional | Framework references; analysis uses the supplied code and documents |
| team-manager | A request in plain words with file paths; optional agent reports or their JSON to combine | None | Reads only the request and the reports you give it |

**File formats:** give files by **path** inside the project folder. Files attached in the chat box reach only the main session, not the agent. Text-based formats (JSON, CSV, YAML, Markdown, code, `.eml`), PDF and PNG/JPG images can be read directly. Save **Word (.docx)**, **Excel (.xlsx)**, **Visio** and **draw.io** files as PDF, CSV or PNG first. Use only synthetic data or data your organisation allows for the AI service you use.

Approve page-fetch prompts when an agent asks. In Copilot, page fetch works out of the box; web search needs an approved search tool (see [docs/COPILOT-MIGRATION.md](docs/COPILOT-MIGRATION.md)).

### Try it

Every example below uses **synthetic data that is already in this repository**. No real systems or data are needed. Paste a prompt into Claude Code, or pick the agent in Copilot and paste everything after `Use the <agent> subagent.`

| Agent | Prompt |
|---|---|
| vm-triage | `@vm-triage CVE-2021-44228` |
| vulnerability-hunt | `Use the vulnerability-hunt subagent. handoff: tests/vulnerability-hunt/fixtures/handoff-CVE-2021-44228.json inventory: tests/vulnerability-hunt/fixtures/sbom-2026-11-02.cdx.json` |
| soc-analyst | `Use the soc-analyst subagent. alert: tests/soc-analyst/fixtures/01-auth-signin.json` |
| cloud-security-analyst | `Use the cloud-security-analyst subagent. mode: triage alert: tests/cloud-security-analyst/fixtures/t1-credential-theft/` |
| threat-modeler | `Use the threat-modeler subagent. system: tests/threat-modeler/fixtures/01-api-missing-ownership/ intake: skip checkpoint: skip` |
| threat-intel-analyst | `Use the threat-intel-analyst subagent. subject: Log4Shell exploitation campaigns scope: campaign` |
| team-manager | `Use the team-manager subagent. reports: tests/team-manager/fixtures/c1-soc-analyst.json tests/team-manager/fixtures/c1-threat-intel-analyst.json` |

Expected results for each example are in [`tests/<agent>/`](tests). In Claude Code, add `Show me the complete report verbatim.` so the full report is shown rather than a summary.

### Optional: export a threat model to images, Excel and Word

threat-modeler writes its report, diagrams (as Mermaid text), CSV and JSON in the chat. The included exporter turns a saved report into **diagram images** (PNG, JPG, SVG), an **Excel threat register** and a **Word report**. It runs locally and sends nothing online. It needs Python; Node.js with Mermaid CLI for the images and pandoc for Word are optional, and the script still produces everything else if they are missing. Setup and usage: [tools/threat-modeler-export/README.md](tools/threat-modeler-export/README.md). The other agents need no exporter: their report and JSON are the output.

### Using threat-modeler on a real project

For a real application, the usual flow is:

1. Collect the application team's material (design documents, diagrams, code, IaC, API specs) in one folder.
2. Send the team the **intake questionnaire**: either the blank form [`docs/threat-model-intake.md`](docs/threat-model-intake.md), or the questions the agent prints on its first run.
3. Collect their answers **in one go**, with `not available` for anything they don't have, and save them as a file.
4. Run the agent with `intake: <their answers file>`, review and approve the data-flow diagram, then get the full report.

Each unanswered question shows up in the report as a **named weakness the team can fix later, not a silent guess**: the intake checklist marks it `Not provided` with its effect, and readiness and confidence are adjusted. Step-by-step prompts are in the **[threat-modeler guide](docs/threat-modeler-guide.md)**.

### Getting help: `?` or `help`

Not sure what an agent needs? Select the agent, then send **`?`** or **`help`** on its own. It replies with a short **usage card**: what it does, the inputs it needs, optional settings, copy-and-edit examples, and what it does *not* do (with the agent to use instead). It does no research and uses none of its budget.

| Runtime | How |
|---|---|
| **Claude Code** | Type `@`, pick the agent (e.g. **vm-triage (agent)**), then `?` → `@vm-triage ?` |
| **GitHub Copilot** (VS Code) | Choose the agent in the Copilot Chat **agent dropdown**, then send `?` or `help` |

Also accepted: `--help`, `usage`, "how do I use this", or an empty message. A real request that happens to contain the word help — e.g. "help me triage CVE-2024-3400" — runs normally.

Example — `@vm-triage ?` returns:

```text
vm-triage v5.4 | help

What I do: Research ONE public CVE and produce a 26-section intelligence report —
KEV, EPSS, CVSS, exploitation status, IOCs, detections, remediation. Stage 1 of the
vulnerability pipeline.

I need (required):
- one CVE ID, format CVE-YYYY-NNNNN

Optional:
- depth: standard (default) | thorough (more research budget)

Example — copy, edit, send:
    CVE-2024-3400
    CVE-2021-44228  depth: thorough

I do NOT:
- say whether YOUR systems are affected, exposed, or how urgent it is -> vulnerability-hunt (give it my output)
- scan, patch or touch any system — public intelligence only, read-only
...
```

### Claude Code (tested runtime)

1. Clone the repository and open the folder in Claude Code:
   ```bash
   git clone https://github.com/Milind2135/AI-Security-Agents.git
   cd AI-Security-Agents
   claude
   ```
2. Start an agent by typing `@` and choosing it from the list (for example **vm-triage (agent)**), then give its input:
   ```text
   @vm-triage CVE-2021-44228
   ```
   or ask in plain language:
   ```text
   Use the soc-analyst subagent. alert: tests/soc-analyst/fixtures/01-auth-signin.json
   ```
3. Not sure what to type? Send `@<agent-name> ?` to see its usage card (see [Getting help](#getting-help--or-help)).

The files in [`.claude/agents/`](.claude/agents) are thin entry points: each one tells Claude Code to read the matching instruction file in `.github/agents/` and limits the agent to read-only tools (Read, Grep, Glob, WebSearch, WebFetch). Equivalent entry points for **OpenAI Codex** are in [`.codex/agents/`](.codex/agents).

### GitHub Copilot in VS Code

1. Open the repository folder in VS Code with an up-to-date **GitHub Copilot Chat** extension.
2. In Copilot Chat, open the **agent dropdown** and pick an agent (for example **vm-triage**). Copilot loads the files in `.github/agents/` directly.
3. Enter the agent's input, e.g. `CVE: CVE-2024-3400` — or send `?` first to see what it needs.
4. Approve page fetches when asked; reject anything that would edit files or run commands.

Requirements and checks (custom-agent support, model choice, network access to NVD / CISA / FIRST, optional web search through an approved MCP server) are in **[docs/COPILOT-MIGRATION.md](docs/COPILOT-MIGRATION.md)**.

> Claude Code is the runtime the agents have been tested in so far. Copilot uses the same instruction files; Copilot runs should be checked against the same golden tests. Wording can differ between models, so results are judged by the test checklist rather than identical text.

---

## Sample output

An excerpt from a real `vm-triage` run on **CVE-2021-44228 (Log4Shell)** in Claude Code — the full 26-section report is in [`tests/vm-triage/baselines/`](tests/vm-triage/baselines).

```text
1. Executive Summary
Status: COMPLETE
Confidence: High — core facts confirmed by NVD JSON, MITRE CNA, EPSS API and Apache's own advisory.
CVE-2021-44228 ("Log4Shell") is an unauthenticated remote code execution flaw in Apache Log4j2 ...

5. Severity/Scoring
Source                              Version   Vector                                         Base Score
NVD / nvd@nist.gov (Primary) [S2]   CVSS 3.1  CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H   10.0
CISA-ADP [S3]                       CVSS 3.1  CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H   10.0
CISA-ADP SSVC [S3]: Exploitation = active; Automatable = yes; Technical Impact = total.

6. EPSS
EPSS Score: 0.999990000 [S4]    EPSS Percentile: 1.000000000 [S4]    EPSS Date: 2026-11-01 [S4]

7. CISA KEV
KEV Listed: Yes [S2]    Date Added: 2021-12-10 [S2]    Due Date (FCEB): 2021-12-24 [S2]
Known Ransomware Campaign Use: NOT_AVAILABLE — the KEV catalog's ransomware flag was not fetched ...
```

Note the last line: when a value could not be retrieved, the agent says so instead of guessing.

---

## Tests

Each agent has **golden tests** in [`tests/<agent>/`](tests) — scenarios, expected results and recorded runs. All test data is synthetic: documentation IP ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`), `example.com` identities, AWS documentation account IDs and placeholder keys marked `NOT-REAL`.

## Repository layout

```text
.github/agents/     The seven agent instruction files (single source of truth; Copilot loads these)
.claude/agents/     Claude Code entry points (read-only tools)
.codex/agents/      OpenAI Codex entry points
AGENTS.md           Shared rules every agent follows
docs/               Agent template, per-agent changelogs, Copilot setup, threat-modeler guide and intake form
tests/              Golden tests, fixtures and baseline reports
tools/              threat-modeler-export: turns a threat-model report into diagram, spreadsheet and JSON files
```

## Limitations

- These agents assist analysts; they do not replace them. A person should review every disposition, priority and recommendation before acting on it.
- Output quality depends on the model, the tools available (page fetch, web search) and the evidence supplied.
- Agents that read internal data (soc-analyst, vulnerability-hunt, cloud-security-analyst) should only receive what your organisation's data policy allows for the AI service you use.

## License

[MIT](LICENSE) © 2026 Milind V. Chavan
