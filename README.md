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
3. Type `?` after any agent name to see its usage card (inputs, options, examples).

The files in [`.claude/agents/`](.claude/agents) are thin entry points: each one tells Claude Code to read the matching instruction file in `.github/agents/` and limits the agent to read-only tools (Read, Grep, Glob, WebSearch, WebFetch). Equivalent entry points for **OpenAI Codex** are in [`.codex/agents/`](.codex/agents).

### GitHub Copilot in VS Code

1. Open the repository folder in VS Code with an up-to-date **GitHub Copilot Chat** extension.
2. In Copilot Chat, open the **agent dropdown** and pick an agent (for example **vm-triage**). Copilot loads the files in `.github/agents/` directly.
3. Enter the agent's input, e.g. `CVE: CVE-2024-3400`.
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
docs/               Agent template, per-agent changelogs, Copilot setup, threat-model intake form
tests/              Golden tests, fixtures and baseline reports
tools/              threat-modeler-export: turns a threat-model report into diagram, spreadsheet and JSON files
```

## Limitations

- These agents assist analysts; they do not replace them. A person should review every disposition, priority and recommendation before acting on it.
- Output quality depends on the model, the tools available (page fetch, web search) and the evidence supplied.
- Agents that read internal data (soc-analyst, vulnerability-hunt, cloud-security-analyst) should only receive what your organisation's data policy allows for the AI service you use.

## License

[MIT](LICENSE) © 2026 Milind V. Chavan
