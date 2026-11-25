# TPRM policy file — template

The agent reads this short file on every run instead of your full policy document. Copy it to `docs/vendors/_policy/policy.md` (private; never pushed to GitHub) and fill it in from your company's TPRM policy. Keep the full policy (PDF or Word) in `docs/vendors/_policy/original/` and put the section reference next to every rule (e.g. `§4.2`), so auditors can trace it.

**Leave a row empty to use the agent's built-in default.** Values below in *italics* are examples, not recommendations. A human (TPRM lead) must check and approve this file — it is the rulebook.

## 1. Identity
| Field | Value |
|---|---|
| Policy name | *Example Corp Third-Party Risk Management Policy* |
| Version | *3.0* |
| Effective date (YYYY-MM-DD) | *2026-07-01* |
| Owner | *Head of TPRM* |
| Sector (financial · general) | *financial* |
| Regimes in scope | *EU-DORA, UK-PRA, IN-RBI, IN-DPDP, EU-GDPR* |
| Local add-ons (country → extra rules) | *India: IN-RBI, IN-DPDP, IN-CERT-In* |

## 2. Tiers
| Tier | Name | Ref |
|---|---|---|
| 1 | *Critical* | *§4.1* |
| 2 | *High* | |
| 3 | *Medium* | |
| 4 | *Low* | |

## 3. Automatic Tier 1 rules (add or remove)
| Rule | Ref |
|---|---|
| *Supports a critical business service and harm within 4 hours* | *§4.2* |
| *Privileged access to core banking, payments or identity systems* | |
| *Card data stored or more than 1,000,000 customer records* | |
| *Regulated critical or important function / material outsourcing* | |

## 4. Thresholds
| Item | Value | Ref |
|---|---|---|
| Large volume of customer records (High / Critical) | *100,000 / 1,000,000* | |
| Sensitive personal data — Critical from | *10,000 records* | |
| Time to harm (Critical / High / Medium) | *4 h / 24 h / 1 week* | |
| Time to replace (Critical / High / Medium) | *12 / 6 / 1 months* | |
| Ownership disclosure threshold | *10%* | |

## 5. Weights for the ranking score (optional; never lowers a tier)
| Group | Weight |
|---|---|
| Data (A) | *30* |
| Access (B) | *25* |
| Business impact (C) | *30* |
| Regulatory (D) | *10* |
| Technology (E) | *5* |

## 6. Per tier: review frequency, evidence, questionnaire, approver
| Tier | Reassess every | Evidence required | Questionnaire | Approver | Ref |
|---|---|---|---|---|---|
| 1 | *12 months + quarterly check* | *SOC 2 Type II or ISO 27001:2022 in scope; pen test ≤ 12 months; BC/DR test ≤ 12 months; screening; financials* | *Full (Key until v1.1)* | *TPRM Committee* | |
| 2 | *24 months* | *SOC 2 Type II or ISO 27001:2022; screening* | *Key* | *Head of TPRM* | |
| 3 | *36 months* | *Certificate if available; screening* | *High-level + Key in Full domains* | *TPRM Manager* | |
| 4 | *On trigger only* | *Screening basics* | *High-level* | *TPRM Analyst Lead* | |

## 7. Risk appetite, exceptions and acceptance
| Item | Value | Ref |
|---|---|---|
| Residual risk allowed without escalation | *Medium for Tier 3–4; Low for Tier 1–2* | |
| Who may accept residual risk (by level) | *High: CRO; Medium: Head of TPRM* | |
| Maximum exception / acceptance period | *12 months* | |
| Remediation due dates (Critical / High / Medium) | *30 / 90 / 180 days* | |
| Second-line QA required for | *Tier 1–2* | |

## 8. Mandatory contract clauses
| Clause | Required for | Ref |
|---|---|---|
| *Security requirements and standards* | *all* | |
| *Incident notification within 6 hours (India) / 24 hours (others)* | *Tier 1–2* | |
| *Right to audit, including regulators* | *Tier 1–2; regulated* | |
| *Subcontractor prior approval* | *Tier 1–2* | |
| *Data location and transfer restrictions* | *where A8 applies* | |
| *Data return and certified deletion* | *all with data* | |
| *Exit and termination assistance (period)* | *Tier 1–2* | |
| *Business continuity and testing participation* | *Tier 1* | |
| *Cooperation with regulators* | *regulated* | |

## 9. Domains always in scope (optional)
*e.g. 22 ESG and conduct for Tier 1–2*

## 10. Extra questions (optional)
Company-specific questions go in `docs/vendors/_policy/extra-questions.csv` with the same columns as `templates/tprm/question-bank.csv`; use IDs starting with `X-`.
