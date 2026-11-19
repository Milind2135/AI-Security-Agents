# soc-analyst: how to use it

soc-analyst triages **one security alert**, or a small group of alerts that may be one incident: sign-in, endpoint / EDR, email or phishing, network, CI/CD. It builds an evidence log and timeline, weighs the benign and malicious readings, and recommends **one of seven dispositions** with confidence and next steps. **You** confirm or override the decision.

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

## In GitHub Copilot

Pick **soc-analyst** in the agent dropdown and send the Step 2 input (without "Use the … subagent."). Approve page-fetch calls for public lookups.

## Quick reference

| Input | Purpose |
|---|---|
| `alert:` | One alert, or several that may be one incident (required) |
| `context:` | Known-good ranges, allowlists, tickets, time zone |
| `category:` | Force a category |
| `depth: thorough` | More queries and lookups |
| `?` | Print the usage card |
