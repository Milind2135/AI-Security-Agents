# soc-analyst: how to use it

soc-analyst has **two jobs**: **triage** (default), described first, and **[hunt mode](#hunt-mode)**, further down.

In triage, soc-analyst triages **one security alert**, or a small group of alerts that may be one incident: sign-in, endpoint / EDR, email or phishing, network, CI/CD. It builds an evidence log and timeline, weighs the benign and malicious readings, and recommends **one of seven dispositions** with confidence and next steps. **You** confirm or override the decision.

Agent instructions: [`.github/agents/soc-analyst.agent.md`](../../.github/agents/soc-analyst.agent.md) · Tests: [`tests/soc-analyst/`](../../tests/soc-analyst)

> **Data rule:** alerts and logs contain user names, hosts and internal IPs. Use them only with an AI service your organisation has approved, keep them in `incidents/<case>/` (git-ignored), and never include passwords, tokens or session cookies.

## What you need

| Input | Required | What to give |
|---|---|---|
| `alert:` | Yes | Alert JSON exported from your EDR or SIEM, a log excerpt, email headers or the `.eml` file, a process tree |
| Related events | Recommended | Events for the same user / host / IP around the alert time (about ±24 hours), exported from your SIEM |
| `context:` | Recommended | A short notes file: VPN and office IP ranges, known allowlists, change tickets, known admin tasks, asset criticality, time zone |
| `category:` | Optional | `auth`, `endpoint`, `cloud`, `email`, `network`, `cicd`, `other` (detected automatically if left out) |

No installation needed. Web access is optional: only **public** IPs and domains are looked up, never internal ones.

**Why context matters:** without it, the agent cannot tell "admin logging in from the office VPN" from "attacker logging in from somewhere new". A short context file often turns an `UNDETERMINED` into a confident answer.

Example `incidents/<case>/context.md`:

```markdown
Office and VPN ranges: 198.51.100.0/24 (VPN), 192.0.2.0/24 (office)
Time zone: Europe/London
Known admin tasks: patching every Tuesday 22:00-23:00
Change tickets: CHG-1042 firewall change 2026-11-18 09:30-11:00 UTC
Critical assets: payroll server, domain controllers
```

## Steps (Claude Code chat)

**1. Put the alert and context in a case folder**, e.g. `incidents/<case>/alert.json` and `incidents/<case>/context.md`. Save files in the folder, not in the chat box.

**2. Run it:**

```text
Use the soc-analyst subagent. alert: incidents/<case>/alert.json context: incidents/<case>/context.md Show me the complete report verbatim.
```

Two alerts that may be one incident (e.g. EDR and SIEM):

```text
Use the soc-analyst subagent. alert: incidents/<case>/crowdstrike.json incidents/<case>/elastic.json context: incidents/<case>/context.md These may be one incident. Show me the complete report verbatim.
```

**3. Read the disposition:**

| Disposition | Meaning |
|---|---|
| CONFIRMED INCIDENT — ESCALATE NOW | Malicious and successful; escalate immediately |
| PROBABLE MALICIOUS — ESCALATE | Most likely malicious; escalate |
| MALICIOUS BLOCKED — CLOSE | Malicious, but blocked with no further impact |
| AUTHORISED ACTIVITY — CLOSE | Matches positive evidence of authorisation (ticket, known automation) |
| BENIGN — CLOSE | Not malicious |
| SUSPICIOUS — INVESTIGATE | Not enough to decide; specific next checks listed |
| UNDETERMINED — ESCALATE | Evidence missing or conflicting; escalate for a human decision |

The report (12 sections + JSON) also gives the evidence log, timeline, findings, ATT&CK techniques, indicators, gaps, next steps marked `REQUIRES APPROVAL`, and an escalation or closure record.

**4. (Optional) Save it:**

```text
Save the complete soc-analyst report above verbatim to incidents/<case>/report-soc-analyst.md
```

Other agents can use it: e.g. [team-manager](team-manager.md) combines it with other reports.

## What it will not do

- Isolate hosts, reset passwords or block anything: it recommends, you approve
- Open suspicious links or attachments
- Look up internal IPs, hostnames or user names on the web
- Deep cloud alert analysis → [cloud-security-analyst](cloud-security-analyst.md); one CVE → [vm-triage](vm-triage.md)

## Hunt mode

Triage answers "is this alert real?". **Hunt mode** answers "is anything bad hiding that **no alert** caught?", e.g. "were we breached by this CVE?", "are other hosts affected?", "is this campaign in our network?".

The agent **writes the queries; you run them** in your SIEM and give back the results. It never needs all your logs: every query **counts and groups** in the SIEM (rarest first) and returns at most **200 rows**.

### What you need

| Input | Required | What to give |
|---|---|---|
| `mode: hunt` | Yes | Switches from triage to hunting |
| Starting point (one) | Yes | `hypothesis:` (plain words), `intel:` (threat-intel-analyst JSON), `vuln:` (vulnerability-hunt JSON), `escalation:` (an escalated soc-analyst report), or `baseline:` ("what is unusual in PowerShell use on servers") |
| `siem:` | Recommended | Your platform or query language (default: `sigma`, vendor-neutral). See the table below. |
| `sources:` | Recommended | A note listing which logs you have, their table/index and field names, and 5–10 sample rows each. Without it, queries use generic field names marked `ADJUST FIELD NAMES`. |
| `scope:` / `window:` | Recommended | What's in scope **with a count** (e.g. `developer hosts (120)`) and the time range (default: last 30 days) |
| `context:` | Recommended | What's normal: admin tools, VPN ranges, service accounts |

**Supported platforms (`siem:`)**

| Support | Platforms (value to type) |
|---|---|
| **Main**: queries written directly | Microsoft Sentinel / Defender (`kql`), Elastic (`esql`), Splunk (`spl`), vendor-neutral Sigma (`sigma`) |
| **Extended**: query marked `SYNTAX UNVERIFIED — test in your console first`, plus a Sigma version to cross-check | CrowdStrike Falcon (`crowdstrike` / `cql`), SentinelOne (`sentinelone`), Palo Alto Cortex XDR (`cortex` / `xql`), Google SecOps / Chronicle (`chronicle` / `udm`), IBM QRadar (`qradar` / `aql`), Sumo Logic (`sumo`), Wazuh (`wazuh`), Carbon Black (`carbonblack`), Datadog (`datadog`) |

For Extended platforms, always test the query in your console before relying on a "no results". The Sigma version can be converted with the official [sigma-cli](https://github.com/SigmaHQ/sigma-cli) and your platform's backend.

Example `sources.md`: see [`tests/soc-analyst/fixtures/hunt-01/sources.md`](../../tests/soc-analyst/fixtures/hunt-01/sources.md).

### Steps (Claude Code chat)

**1. Ask for a hunt plan**

```text
Use the soc-analyst subagent. mode: hunt hypothesis: a malicious npm package is stealing developer credentials siem: esql sources: incidents/hunt-01/sources.md context: incidents/hunt-01/context.md scope: developer and build hosts (120) window: last 30 days
```

Or start from another agent's output, e.g. `mode: hunt intel: incidents/case-12/threat-intel.json siem: kql`.

You get a **hunt plan** (`soc-analyst vX.Y | hunt plan`): up to 3 hypotheses, each with an **ABLE** table (Actor, Behaviour, Location, Evidence), a data check, and **ready-to-run queries**. Each query comes with *what a hit means*, *what no hit means* and the file name to export to (`Q1.csv`, …). Claude saves the plan as `hunt-plan.md` in the hunt folder.

**2. Run the queries in your SIEM.** Export each result as `Q1.csv`, `Q2.csv`, … into the same folder (e.g. `incidents/hunt-01/`). Note **how many of the in-scope hosts or users each query covered** (e.g. "112 of 120 hosts; 8 have no EDR").

**3. Send the results** (Claude Code chat):

```text
results ready — Q1, Q2 and Q4 covered 112 of 120 hosts (8 build servers have no EDR); Q3 covered the whole GitHub org
```

Claude passes the plan and your files to the agent. (Without Claude's help, or in a new chat: `Use the soc-analyst subagent. mode: hunt plan: <the plan's JSON or file> results: Q1.csv Q2.csv … coverage: …`.)

**4. Read the hunt result** (`soc-analyst vX.Y | hunt result`), saved as `hunt-result-<date>.md`. Each hypothesis gets one result:

| Result | Meaning |
|---|---|
| **FOUND** | The results show the suspected behaviour or indicator on named hosts or users: escalate, and triage each host |
| **NOT FOUND** | Every query ran, nothing matched, **and at least 90% of the scope was covered**. Always stated with what was searched, e.g. "not found in 30 days of EDR data on 112 of 120 hosts" |
| **INCONCLUSIVE** | Leads that need a second look, a query that failed or wasn't run, a results file too large, or coverage below 90% (or unknown) |

The report also gives coverage per hypothesis, follow-up (pass-2) queries for the few suspicious hosts, `REQUIRES APPROVAL` actions, and **detection candidates**: queries that worked well, for your detection team to turn into rules.

### Tips

- **Results file over 2,000 rows?** The agent won't read it all. It marks the query `TOO_LARGE` and gives you an aggregated version to run instead.
- **Missing a results file** is never treated as "no results".
- **Repeat or extend a hunt later:** add `previous: <the earlier hunt result's JSON>`.
- **Try it with test data:** the README's "Try it" has a ready-made hunt-analysis prompt using [`tests/soc-analyst/fixtures/hunt-01/`](../../tests/soc-analyst/fixtures/hunt-01/).

## In GitHub Copilot

Pick **soc-analyst** in the agent dropdown and send the Step 2 input (without "Use the … subagent."). Approve page-fetch calls for public lookups. For hunts, send the hunt input, then reply in the same chat with `results: …` after running the queries.

## Quick reference

| Input | Purpose |
|---|---|
| `alert:` | One alert, or several that may be one incident (required) |
| `context:` | Known-good ranges, allowlists, tickets, time zone |
| `category:` | Force a category |
| `depth: thorough` | More queries and lookups |
| `?` | Print the usage card |
| `mode: hunt` + `hypothesis:` / `intel:` / `vuln:` / `escalation:` / `baseline:` | Hunt mode starting point |
| `siem:`, `sources:`, `scope:`, `window:` | Hunt query language, data sources, scope (with a count), time range |
| `results:` + `plan:` | Hunt analysis (Claude passes these for you in Claude Code) |
