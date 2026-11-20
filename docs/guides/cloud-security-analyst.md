# cloud-security-analyst: how to use it

cloud-security-analyst works in **two modes**:

| Mode | Question it answers | Main input |
|---|---|---|
| **posture** | "What could an attacker actually do in our cloud?" It finds real **attack paths**: internet exposure + exploitable weakness + privileged identity + sensitive data, plus IAM privilege escalation and guardrail and logging gaps | IaC, CSPM / scanner exports, IAM exports |
| **triage** | "Is this cloud alert real?" It correlates the alert with audit events, classifies it and gives **one disposition** | The alert + audit events |

It works with AWS, Azure and GCP.

Agent instructions: [`.github/agents/cloud-security-analyst.agent.md`](../../.github/agents/cloud-security-analyst.agent.md) · Tests: [`tests/cloud-security-analyst/`](../../tests/cloud-security-analyst)

> **Data rule:** cloud configurations and IAM exports describe your estate's weaknesses. Use them only with an AI service your organisation has approved, keep them in `incidents/<case>/` or another git-ignored folder, and never include secrets, `.env` files, access keys or private keys.

## Posture mode

### What you need

| Input | Required | What to give |
|---|---|---|
| Material | At least one | IaC (Terraform, CloudFormation, Bicep / ARM, Kubernetes, Helm) **or** a CSPM / scanner export (Prowler, Wiz, Defender for Cloud, Security Hub, Security Command Center; CSV or JSON) |
| IAM export | Strongly advised | Users, roles, policies and trust relationships |
| Data classification | Strongly advised | Which buckets / databases hold personal, card or regulated data (in a context file) |
| Guardrails | Advised | SCPs, Azure Policy, GCP organisation policies |
| Logging set-up | Advised | Trails, diagnostic settings, threat detection |

**Getting exports.** *You* run these, with read-only credentials; flags vary by version, so check `--help`:

| Cloud | IAM export |
|---|---|
| AWS | `aws iam get-account-authorization-details > iam.json` |
| Azure | `az role assignment list --all > role-assignments.json` |
| GCP | `gcloud asset search-all-iam-policies --scope=<scope> > iam-policies.json` |

Scanner and CSPM findings: export as CSV or JSON from the tool's console.

### Steps (Claude Code chat)

1. Put the files in a folder, e.g. `incidents/<case>/terraform/`, `incidents/<case>/exports/`, plus a `context.md` (example below).
2. Run:
   ```text
   Use the cloud-security-analyst subagent. mode: posture material: incidents/<case>/terraform/ incidents/<case>/exports/ context: incidents/<case>/context.md Show me the complete report verbatim.
   ```
3. Read the report: attack paths rated **Critical / High / Medium / Low** and prioritised **P1–P4**, IAM privilege-escalation paths with their prerequisites, guardrail and logging gaps, recommendations (each with what drives it, where to fix it in IaC and how to verify), a diagram, and CSV and JSON blocks.

## Triage mode

### What you need

| Input | Required | What to give |
|---|---|---|
| `alert:` | Yes | The alert (GuardDuty, Defender for Cloud, Security Command Center, CSPM; JSON or text) |
| Audit events | Strongly advised | Events for the same identity / IP / resource around the alert (±24 h): CloudTrail, Azure Activity / Entra sign-in logs, GCP Cloud Audit Logs. **Without them it cannot close an alert.** |
| Context | Advised | Known automation identities, change tickets, relevant IaC |

### Steps (Claude Code chat)

1. Put the alert and events in `incidents/<case>/`.
2. Run:
   ```text
   Use the cloud-security-analyst subagent. mode: triage alert: incidents/<case>/guardduty.json incidents/<case>/cloudtrail-window.json context: incidents/<case>/context.md Show me the complete report verbatim.
   ```
3. Read the disposition, the correlated timeline, the classification (e.g. credential compromise, workload compromise, data exposure, configuration drift, expected change) and next steps marked `REQUIRES APPROVAL`.

## Context file (both modes)

Example `incidents/<case>/context.md`:

```markdown
Scope: AWS accounts …3333 (prod), …4444 (test)
Crown-jewel data: s3://example-customer-exports = PII; rds main-db = card data
Known automation identities: github-deploy = CI/CD deployments; backup-role = nightly backups
Change tickets: CHG-1042 open port 443 on alb, 2026-11-18 09:30-11:00 UTC
Normal behaviour: ops-admin usually signs in from 198.51.100.0/24, eu-west-1
```

## Save the report (optional)

```text
Save the complete cloud-security-analyst report above verbatim to incidents/<case>/report-cloud-security-analyst.md
```

## What it will not do

- Run scanners or cloud CLIs, change resources or apply fixes
- Contact anything found in your data
- Non-cloud alerts → [soc-analyst](soc-analyst.md); is a CVE on our assets → [vulnerability-hunt](vulnerability-hunt.md); one application's design → [threat-modeler](threat-modeler.md)

## In GitHub Copilot

Pick **cloud-security-analyst** in the agent dropdown and send the input (without "Use the … subagent.").

## Quick reference

| Input | Purpose |
|---|---|
| `mode: posture` / `mode: triage` | Which job (detected automatically if left out) |
| `material:` / `alert:` | Required for posture / triage |
| `context:` | Crown jewels, automation identities, tickets, normal behaviour |
| `handoff:` | vm-triage JSON for CVEs found on workloads |
| `previous:` | Earlier report JSON, to see what changed |
| `scope:`, `depth: thorough` | Limit scope / more budget |
| `?` | Print the usage card |
