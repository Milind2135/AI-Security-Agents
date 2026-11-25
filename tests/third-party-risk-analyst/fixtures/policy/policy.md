# TPRM policy file (SYNTHETIC TEST DATA)

## 1. Identity
| Field | Value |
|---|---|
| Policy name | Example Bank Third-Party Risk Management Policy |
| Version | 3.0 |
| Effective date | 2026-07-01 |
| Owner | Head of TPRM |
| Sector | financial |
| Regimes in scope | EU-DORA, IN-RBI, IN-DPDP, EU-GDPR |
| Local add-ons | India: IN-RBI, IN-DPDP, IN-CERT-In |

## 3. Automatic Tier 1 rules
| Rule | Ref |
|---|---|
| Supports a critical business service and harm within 4 hours | §4.2 |
| Privileged access to core banking, payments or identity systems | §4.2 |
| Card data stored or more than 1,000,000 customer records | §4.2 |

## 6. Per tier
| Tier | Reassess every | Evidence required | Questionnaire | Approver | Ref |
|---|---|---|---|---|---|
| 1 | 12 months + quarterly check | SOC 2 Type II or ISO 27001:2022 in scope; pen test ≤ 12 months; BC/DR test ≤ 12 months; screening; financials | Key | TPRM Committee | §5.1 |
| 2 | 24 months | SOC 2 Type II or ISO 27001:2022; screening | Key | Head of TPRM | §5.1 |
| 3 | 36 months | Certificate if available; screening | High-level + Key | TPRM Manager | §5.1 |
| 4 | On trigger only | Screening basics | High-level | TPRM Analyst Lead | §5.1 |

## 7. Risk appetite, exceptions and acceptance
| Item | Value | Ref |
|---|---|---|
| Maximum exception / acceptance period | 12 months | §6.3 |
| Remediation due dates (Critical / High / Medium) | 30 / 90 / 180 days | §6.4 |

## 8. Mandatory contract clauses
| Clause | Required for | Ref |
|---|---|---|
| Incident notification within 72 hours | Tier 1–2 | §7.2 |
| Right to audit, including regulators | Tier 1–2 | §7.3 |
| Subcontractor prior approval | Tier 1–2 | §7.4 |
| Data return and certified deletion | all with data | §7.5 |
| Exit and termination assistance (6 months) | Tier 1 | §7.6 |
