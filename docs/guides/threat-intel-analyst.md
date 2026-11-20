# threat-intel-analyst: how to use it

threat-intel-analyst researches **one threat subject** from public sources (a threat actor, a campaign or a set of indicators) and writes a cited intelligence brief: profile, timeline, ATT&CK techniques, malware and tools, indicators of compromise (defanged), attribution with competing hypotheses, published detection rules, hunting ideas, and STIX-style JSON for other agents.

Agent instructions: [`.github/agents/threat-intel-analyst.agent.md`](../../.github/agents/threat-intel-analyst.agent.md) · Tests: [`tests/threat-intel-analyst/`](../../tests/threat-intel-analyst)

> **Data rule:** only **public** indicators are looked up. Do not put internal IPs, internal hostnames, user names or incident details in the subject. If you do, the agent removes them and lists them as "Not looked up".

## What you need

| Input | Required | Example |
|---|---|---|
| `subject:` | Yes | A threat actor (`APT29`), a campaign (`Shai-Hulud npm worm`) or a set of public indicators (IPs, domains, hashes, package names) |
| `scope:` | Optional | `actor`, `campaign` or `indicator` (inferred; it asks if unclear) |
| `depth:` | Optional | `thorough` when you need exact detection-rule text (uses more of your usage quota) |
| `upstream:` | Optional | vm-triage JSON for a CVE the campaign used |

No files and no installation. It needs **web access**: approve the page-fetch prompts.

## Steps (Claude Code chat)

**1. Run it** (pick one):

```text
Use the threat-intel-analyst subagent. subject: Shai-Hulud npm worm scope: campaign Show me the complete report verbatim.
```
```text
Use the threat-intel-analyst subagent. subject: APT29 scope: actor Show me the complete report verbatim.
```
```text
Use the threat-intel-analyst subagent. subject: 203.0.113.45, malicious-update[.]example scope: indicator Show me the complete report verbatim.
```

**2. Read the brief** (16 sections + JSON). The first line is `threat-intel-analyst vX.Y | result`, followed by the handling marking (TLP:CLEAR). Useful sections:
- **Executive summary** and **confidence and gaps**: how sure it is, and what it could not find
- **ATT&CK techniques** and **IOCs**: defanged (e.g. `example[.]com`), so they are safe to paste
- **Attribution**: competing hypotheses with confidence, never a single unsupported claim
- **Published detection rules** and **hunting ideas**: for your detection and hunting teams
- **Sources**: graded for reliability (A–F) and credibility (1–6)

**Hunt for it in your own logs** (hand-off to soc-analyst):
1. Save the JSON block: `Save only the JSON block from the threat-intel-analyst report above to incidents/notes/intel-<subject>.json`
2. Select **@soc-analyst** and give the file **plus your environment**:
   ```text
   mode: hunt intel: incidents/notes/intel-<subject>.json siem: kql sources: incidents/notes/sources.md context: incidents/notes/context.md scope: <what, with a count> window: last 30 days
   ```
   Without `siem:`, `sources:`, `context:` and `scope:` the hunt queries are generic. Full walkthrough: [soc-analyst guide, Hunting from another agent's report](soc-analyst.md#hunting-from-another-agents-report).

**3. (Optional) Save it:**

```text
Save the complete threat-intel-analyst report above verbatim to incidents/<case>/report-threat-intel-analyst.md
```

## What it will not do

- Research a single CVE → [vm-triage](vm-triage.md) (a subject that is just a CVE ID is sent there)
- Check your own systems or logs → [soc-analyst](soc-analyst.md) for one alert
- Rate business impact or priority for your organisation
- Use paid or dark-web feeds (unless such a tool is connected), or open, block or change anything; it never visits a suspected malicious URL itself

## In GitHub Copilot

Pick **threat-intel-analyst** in the agent dropdown and type the subject. Approve `web/fetch` calls. Without a web-search tool, it starts from public trackers (MITRE ATT&CK, CISA, Malpedia, GitHub Advisory Database, OSV) and says so in the brief.

## Quick reference

| Input | Purpose |
|---|---|
| `subject:` | Actor, campaign or indicators (required) |
| `scope:` | `actor` / `campaign` / `indicator` |
| `depth: thorough` | More research; exact rule text |
| `upstream:` | Related vm-triage JSON |
| `?` | Print the usage card |
