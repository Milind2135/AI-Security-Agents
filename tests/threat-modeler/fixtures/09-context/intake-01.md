# Threat model intake form (SYNTHETIC TEST DATA — for fixture 01-api-missing-ownership)

| Field | Answer |
|---|---|
| System / feature name | Orders API |
| Requested by (team) | Web Shop team |
| Material supplied (`system:` paths) | tests/threat-modeler/fixtures/01-api-missing-ownership/ |

| Q# | What to provide | Your answer |
|---|---|---|
| Q1 | Business requirement and scope | Customers view their own past orders. In scope: Orders API. Out of scope: payment processing, sign-in service. |
| Q2 | Architecture or data-flow diagram | not available |
| Q3 | Data inventory and classification | Orders: name, delivery address, phone (personal data, Confidential); card last 4 digits. |
| Q4 | User types and roles | Customers (external, signed in); support agents use a separate admin tool (out of scope). |
| Q5 | Hosting and deployment model | not available |
| Q6 | Third-party integrations | Sign-in service (internal) issues JWTs. |
| Q7 | Source code | see material supplied |
| Q8 | IaC / network rules | not available |
| Q9 | API specifications | not available |
| Q10 | AuthN / AuthZ design | JWT RS256 from the sign-in service; no roles in the Orders API. |
| Q11 | CI/CD and secrets | not available |
| Q12 | Dependency list / SBOM | not available |
| Q13 | Logging design | not available |
| Q14 | Compliance scope | GDPR |
| Q15 | Security standards | tests/threat-modeler/fixtures/09-context/secure-coding-standard.md |
| Q16 | Risk owner and appetite | Owner: Head of Web Shop Engineering. Appetite: owner may accept Low risks. |
| Q17 | Business criticality | Order history is a supporting function; checkout (out of scope) is essential. |
| Q18 | Previous findings | tests/threat-modeler/fixtures/09-context/pentest-2026-07.md |
| Q19 | Incident history | not available |
| Q20 | Threat intelligence | not available |
| Q21 | AI/LLM features | none |
| Q22 | Operational processes | not available |
| Q23 | Change being made | not available |
| Q24 | Feature flags / rollout | not available |
| Q25 | Client specifics | not available |
