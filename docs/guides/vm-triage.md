# vm-triage: how to use it

vm-triage researches **one CVE** from public sources and writes a cited 26-section report: what the vulnerability is, CVSS, whether it is in the CISA KEV catalogue, its EPSS score, exploitation status, affected and fixed versions, workarounds, indicators and detection ideas. It is **stage 1** of the vulnerability pipeline: it does not know your systems. To check whether a CVE affects *your* assets, give its output to [vulnerability-hunt](vulnerability-hunt.md).

Agent instructions: [`.github/agents/vm-triage.agent.md`](../../.github/agents/vm-triage.agent.md) · Tests: [`tests/vm-triage/`](../../tests/vm-triage)

> **Data rule:** vm-triage only looks up public information about the CVE ID. Do not add internal hostnames, IPs or system names to the prompt.

## What you need

| Input | Required | Example |
|---|---|---|
| One CVE ID | Yes | `CVE-2021-44228` (one per run; a product nickname such as "Log4Shell" is not enough, it asks for the ID) |
| `depth:` | No | `thorough` for more research (uses more of your usage quota) |

No files and no installation. It needs **web access**: approve the page-fetch prompts (NVD, CVE.org, FIRST EPSS, CISA, vendor advisories).

## Steps (Claude Code chat)

**1. Run it**

```text
Use the vm-triage subagent. CVE-2021-44228 Show me the complete report verbatim.
```

or type `@`, pick **vm-triage (agent)** and enter the CVE ID.

**2. Read the report.** The first line is `vm-triage vX.Y | result`. The most useful sections for a quick decision: the executive summary, KEV status, EPSS, exploitation status, affected and fixed versions, and remediation. Every fact cites a source `[S#]` listed near the end; anything the agent could not verify is marked as such.

**3. (Optional) Save it and hand it on.** To check your own assets next, save the JSON block for vulnerability-hunt:

```text
Save only the JSON block from the vm-triage report above to incidents/<case>/vm-triage-CVE-2021-44228.json
```

(`incidents/` is git-ignored.) Then continue with the [vulnerability-hunt guide](vulnerability-hunt.md).

## What it will not do

- Say whether **your** systems are affected or how urgent it is for you → [vulnerability-hunt](vulnerability-hunt.md)
- Check whether you have been breached → your threat-hunting / incident-response team
- Scan, patch or touch any system

## In GitHub Copilot

Pick **vm-triage** in the agent dropdown and type the CVE ID. Approve `web/fetch` calls. Without a web-search tool it still works from the core sources (NVD, CVE.org, FIRST EPSS) and their references.

## Quick reference

| Input | Purpose |
|---|---|
| `CVE-YYYY-NNNNN` | The CVE to research (required) |
| `depth: thorough` | More research budget |
| `?` | Print the usage card |
