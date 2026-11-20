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

### Do I need an API integration with my SIEM or EDR?

**No. An integration is optional.** The agent works fully without one; an integration only saves you copy-and-paste work.

| | **Without integration (OFFLINE, default)** | **With integration (LIVE, optional)** |
|---|---|---|
| How it works | The agent writes the queries, **you** run them in your SIEM or EDR console and export the results (CSV/JSON) | The agent runs the queries **itself** through a connected tool and reads the results directly |
| Setup | Nothing | A **read-only** API connection (an MCP server) to your SIEM or EDR, with read-only credentials |
| Approvals | Only for using the AI service with your data | Also **security and IT approval** to connect the AI to the SIEM/EDR, plus an API account |
| Effort per hunt | You run 3–6 queries and save the result files | One prompt |
| Risk | Lowest: you see and control every query and result | Higher: the AI queries live data, so read-only access and limits are essential |

**Adding LIVE later**
1. Get an **MCP server** for your platform; many SIEM and EDR vendors and communities publish one (check your vendor's documentation).
2. Create **read-only API credentials**: a dedicated account that can only search, never isolate, block or change anything.
3. Add the tool:
   - **Claude Code:** add it to the `tools:` line in `.claude/agents/soc-analyst.md`.
   - **Copilot:** add it to the agent's `tools:` and to `.vscode/mcp.json`, with the API key entered at runtime via `${input:…}`; never save keys in the repository.
4. The agent's own safety checks still apply:
   - it refuses any tool that can change, delete, isolate or block, and falls back to OFFLINE;
   - every query is time-bounded and limited to 200 rows;
   - at most 10 queries per hunt (20 with `depth: thorough`);
   - Claude Code and Copilot ask your permission before each tool call.

**Recommendation:** start **OFFLINE**. You need no integration, and you see every query before it runs, which is also the best way to learn what the agent does. Consider LIVE only after a few hunts, with your security team's approval. The agent's first line always shows which one it is using (`data access: OFFLINE` or `LIVE`).

### Before your first hunt: write two short notes (one-time)

The agent writes queries for **your** environment, so it needs to know what logs you have and what is normal for you. Write these two notes once, keep them in `incidents/` (git-ignored), and reuse them for every hunt. Only the hypothesis changes each time.

**1. Data sources note (`sources:`): what logs you have**

| Put in it | Where to find it |
|---|---|
| Your SIEM / EDR platform and query language | You know it (e.g. Elastic, Sentinel, Splunk, CrowdStrike) |
| Which logs are collected, with their **index / table names** | Elastic: *Discover* → index patterns. Sentinel: the *Tables* list in Logs. Splunk: indexes / sourcetypes. |
| **Field names** for the key data (host, user, process, command line, IP, domain) | Open one event of each type and copy its field names, or export 5–10 sample events with sensitive values removed |
| **Coverage**: how many machines send these logs | EDR console (hosts with the sensor) and CMDB / asset list (total machines) |
| **Approved outbound destinations** (e.g. package registries, code hosting, update servers) | Network / proxy team, developer tooling owners |
| **Identity mapping**: how a device account relates to a sign-in name (e.g. `j.doe` on a laptop = `j.doe@example.com`) | IAM team |
| **Known telemetry limits** (e.g. file reads not recorded, no DNS logs) | Your EDR / SIEM documentation |

Example `incidents/notes/sources.md`:

```markdown
Platform: Microsoft Sentinel (KQL). Time zone: UTC.
EDR process events: DeviceProcessEvents — DeviceName, AccountName, FileName, ProcessCommandLine, InitiatingProcessFileName
EDR network events: DeviceNetworkEvents — DeviceName, RemoteIP, RemoteUrl, RemotePort
Sign-ins: SigninLogs — UserPrincipalName, IPAddress, Location, ResultType
Coverage: 1,180 of 1,250 laptops have Defender for Endpoint; servers 300 of 310. Developer laptops (lap-04xx): 142 of 150 onboarded.
Approved destinations for node/npm: registry.npmjs.org, github.com, githubusercontent.com, nodejs.org.
Identity mapping: device AccountName j.doe = UPN j.doe@example.com.
Limits: DeviceFileEvents records created/modified/renamed/deleted files, not reads; no DNS or proxy logs.
```

A complete synthetic example (Elastic) is in [`tests/soc-analyst/fixtures/hunt-01/sources.md`](../../tests/soc-analyst/fixtures/hunt-01/sources.md).

**2. Context note (`context:`): what is normal for you**

| Put in it | Usually from |
|---|---|
| VPN and office IP ranges | Network team |
| Admin and IT tools normally used (e.g. remote-admin tools, software deployment) | IT / desktop team |
| Service accounts and what they do | IAM / platform team |
| Change windows, pentests, known noisy sources | Change calendar, SOC wiki |
| Critical assets (domain controllers, payment servers) | CMDB / asset owners |

Example `incidents/notes/context.md`:

```markdown
VPN range: 198.51.100.0/24. Office: 192.0.2.0/24. Time zone: Europe/London.
IT uses remote-admin tool X and software-deployment tool Y on all laptops.
Service accounts: svc-backup (nightly backups 01:00–03:00), ci-bot (CI/CD only).
Change window: Tuesdays 22:00–23:00. Pentest scheduled 2026-12-01 to 2026-12-05.
Critical assets: domain controllers dc-01, dc-02; payroll server pay-01.
```

A synthetic example is in [`tests/soc-analyst/fixtures/hunt-01/context.md`](../../tests/soc-analyst/fixtures/hunt-01/context.md).

**Save the notes inside your project folder** (e.g. `incidents/notes/`), not just in Downloads: the agent can only read files in the project. If the files are missing, Claude stops and asks rather than guessing.

**No notes yet?** The agent still works: it uses generic field names marked `ADJUST FIELD NAMES`, and you fix them before running the queries. Writing the notes once saves that work every time.

> **Data rule:** use real environment details only with an AI service your organisation has approved; keep the notes in `incidents/` (never in the public repository); never put passwords, keys or customer data in them.

### What each part of the hunt prompt means

| Part | Meaning | Why it matters |
|---|---|---|
| `mode: hunt` | Hunt instead of triaging an alert | Switches the job |
| `hypothesis: …` | What you suspect, in plain words | Each hunt tests a suspicion |
| `siem: esql` | Your platform or query language | A Splunk search won't run in Elastic |
| `sources: <file>` | Your data sources note | Real index and field names; what you can't see (e.g. hosts without EDR) |
| `context: <file>` | Your context note | Normal activity isn't flagged as suspicious |
| `scope: developer and build hosts (120)` | Where to look, **with a count** | The count lets the agent state coverage (e.g. "112 of 120 = 93%") |
| `window: last 30 days` | How far back to search | Limits the queries |


### Steps (Claude Code chat)

**1. Ask for a hunt plan**

```text
Use the soc-analyst subagent. mode: hunt hypothesis: a malicious npm package is stealing developer credentials siem: esql sources: incidents/notes/sources.md context: incidents/notes/context.md scope: developer and build hosts (120) window: last 30 days
```

To try it with the synthetic test data instead, use `sources: tests/soc-analyst/fixtures/hunt-01/sources.md context: tests/soc-analyst/fixtures/hunt-01/context.md`.

Or start from another agent's output, e.g. `mode: hunt intel: incidents/case-12/threat-intel.json siem: kql`.

You get a **hunt plan** (`soc-analyst vX.Y | hunt plan`): up to 3 hypotheses, each with an **ABLE** table (Actor, Behaviour, Location, Evidence), a data check, and **ready-to-run queries**. Each query comes with *what a hit means*, *what no hit means* and the file name to export to (`Q1.csv`, …). Claude saves the plan as `hunt-plan.md` in the hunt folder.

**2. Run the queries in your SIEM.** Export each result as `Q1.csv`, `Q2.csv`, … into the hunt folder Claude names, `incidents/hunts/<hunt ID>/` (it also holds `hunt-plan.md`; keep your reusable notes separately in `incidents/notes/`). Note **how many of the in-scope hosts or users each query covered** (e.g. "112 of 120 hosts; 8 have no EDR").

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
