# Threat model intake form

> New to threat-modeler? Read the step-by-step guide first: [docs/threat-modeler-guide.md](threat-modeler-guide.md).

Fill in what you have and give this file to the `threat-modeler` agent as `intake: <path to this file>`. One pass is enough — leave anything you do not have as `not available`; the agent records it honestly as **Not provided** and works from the material instead.

**Do not include:** production secrets, real credentials, `.env` files with live values, real customer data or production logs. Give file paths for long material.

| Field | Answer |
|---|---|
| System / feature name | |
| Requested by (team) | |
| Date | |
| Material supplied (`system:` paths) | |


## Tier 1 — minimum (the review cannot start well without these)

| Q# | What to provide | Your answer (paste, file path, or "not available") |
|---|---|---|
| Q1 | Business requirement and scope: what it does, what is in and out of scope, release date | |
| Q2 | Architecture or data-flow diagram (file path; images accepted) | |
| Q3 | Data inventory and classification: data collected, stored, sent and logged, and its sensitivity | |
| Q4 | User types and roles, incl. administrators, support staff, service accounts, partners, anonymous users | |
| Q5 | Hosting and deployment model: cloud / on-premises / hybrid, regions, internet exposure, single- or multi-tenant | |
| Q6 | Third-party integrations and dependencies: external APIs, SaaS, identity provider, payment provider, AI model provider | |

## Tier 2 — evidence (turns "Claimed" controls into "In place")

| Q# | What to provide | Your answer (paste, file path, or "not available") |
|---|---|---|
| Q7 | Source code: repository or paths (entry points, auth middleware, data-access layer) | |
| Q8 | Infrastructure-as-code and network / security-group rules | |
| Q9 | API specifications (OpenAPI, GraphQL schema, gRPC protos) | |
| Q10 | Authentication and authorisation design: identity provider, token types, session lifetime, MFA, role model | |
| Q11 | CI/CD pipeline definition and secrets-management approach | |
| Q12 | Dependency list or SBOM | |
| Q13 | Logging, monitoring and audit design: what is logged, where, retention | |

## Tier 3 — context (makes the priorities right)

| Q# | What to provide | Your answer (paste, file path, or "not available") |
|---|---|---|
| Q14 | Compliance and regulatory scope (e.g. PCI DSS, HIPAA, GDPR, SOC 2, sector rules) | |
| Q15 | Organisation's security standards / control baseline (file paths) | |
| Q16 | Risk owner (name or role) and risk appetite (e.g. "owner may accept Low") | |
| Q17 | Business criticality: revenue impact, users affected, uptime requirement, which functions are essential | |
| Q18 | Previous threat model, penetration-test report, scanner findings, bug-bounty reports | |
| Q19 | Incident history for this product or similar ones | |
| Q20 | Threat intelligence for this industry or technology (e.g. a `threat-intel-analyst` handoff) | |

## Tier 4 — specialist / follow-up

| Q# | What to provide | Your answer (paste, file path, or "not available") |
|---|---|---|
| Q21 | AI/LLM features: system prompts; tools/functions and their permissions; retrieval sources and who can write to them; model provider and data-retention terms; human approval points; evaluation or red-team results | |
| Q22 | Operational processes: support and admin procedures, account recovery, break-glass access, data deletion and retention | |
| Q23 | For an update: what is changing (the change delta) | |
| Q24 | Feature flags and rollout plan: what is exposed to whom, and when | |
| Q25 | Mobile, desktop or embedded client specifics: local storage, certificate pinning, update mechanism | |

---
Template for `threat-modeler` v1.1 (`.github/agents/threat-modeler.agent.md`, Intake section). Keep the question numbers unchanged so answers map to the report's intake checklist.
