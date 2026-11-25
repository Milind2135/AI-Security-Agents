third-party-risk-analyst v1.0 | plan

> TOOL TEST SAMPLE (SYNTHETIC) — a hand-made plan used only to test tools/tprm/tprm.py; not an expected agent output.

## 1. Summary
(abridged)

```json
{
 "agent": "third-party-risk-analyst",
 "version": "1.0",
 "stage": "plan",
 "round": null,
 "as_of": "2026-11-25",
 "vendor": {
  "name": "PayFlow Example",
  "legal_entity": "PayFlow Example Ltd",
  "registration": null,
  "country": null
 },
 "engagements": [
  {
   "id": "ENG-1",
   "service": "Card payment processing for the retail mobile app",
   "business_owner": "R. Example, Head of Digital Payments",
   "regimes": [
    "EU-DORA",
    "IN-RBI",
    "IN-DPDP",
    "EU-GDPR",
    "PCI-DSS"
   ]
  }
 ],
 "policy": {
  "source": "tests/third-party-risk-analyst/fixtures/policy/policy.md",
  "name": "Example Bank Third-Party Risk Management Policy",
  "version": "3.0",
  "effective": "2026-07-01",
  "conflicts": [
   "PC-1: policy \u00a77.2 incident notice 72 hours; IN-RBI requires provider reporting fast enough for 6-hour reporting"
  ]
 },
 "standards_as_of": "2026-11-25",
 "sector": "financial",
 "regimes": [
  "baseline",
  "EU-DORA",
  "IN-RBI",
  "IN-DPDP",
  "EU-GDPR",
  "PCI-DSS"
 ],
 "factors": [
  {
   "engagement": "ENG-1",
   "id": "A1",
   "rating": "Critical",
   "basis": "intake A1: 1.8 million records",
   "status": "Provided",
   "unverified_owner": null
  },
  {
   "engagement": "ENG-1",
   "id": "A4",
   "rating": "Critical",
   "basis": "intake A4: stores card numbers",
   "status": "Provided",
   "unverified_owner": null
  },
  {
   "engagement": "ENG-1",
   "id": "A9",
   "rating": "High",
   "basis": "intake A9: Don't know",
   "status": "Not provided",
   "unverified_owner": "business owner"
  },
  {
   "engagement": "ENG-1",
   "id": "C2",
   "rating": "Critical",
   "basis": "intake C2: within 1 hour",
   "status": "Provided",
   "unverified_owner": null
  }
 ],
 "ratings": {
  "inherent_risk": "Critical",
  "criticality": "Critical",
  "auto_rules_fired": [
   "C1 with C2 <= 4 hours",
   "A1/A4 Critical"
  ],
  "tier": 1,
  "previous_tier": null,
  "weighted_score": 88,
  "quadrant": "High risk / High criticality",
  "residual_risk": null,
  "residual_if_conditions_met": null
 },
 "tier_confirmation": {
  "status": "pending",
  "by": null,
  "date": null,
  "reason": null
 },
 "tier_history": [],
 "regulatory_flags": [],
 "scoping": [
  {
   "domain": "00 Vendor profile",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "01 Documents and assurance",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "02 Governance and risk management",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "03 Assets and information management",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "04 People security",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "05 Physical security",
   "depth": "N/A",
   "reason": "No physical access; data hosted by subprocessor CloudHost Example (covered by domain 20)"
  },
  {
   "domain": "06 IT operations",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "07 Network security",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "08 Endpoint security",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "09 Servers and platforms",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "10 Logging and monitoring",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "11 Identity and access management",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "12 Secure development",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "13 Incident management",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "14 Operational resilience",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "15 Compliance and audit",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "16 Privacy and data protection",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "17 Cryptography and key management",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "18 Threat and vulnerability management",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "19 Cloud services",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "20 Supply chain and fourth parties",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "21 Artificial intelligence",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "22 ESG and conduct",
   "depth": "Key",
   "reason": "Tier 1\u20132 default"
  },
  {
   "domain": "23 Financial health",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  },
  {
   "domain": "24 Exit and termination",
   "depth": "Full",
   "reason": "Tier 1 \u2014 applies"
  }
 ],
 "questionnaire": {
  "preset": "Key questions in every in-scope domain (Full until question bank v1.1)",
  "accepted_existing": []
 },
 "document_requests": [
  {
   "document": "SOC 2 Type II report covering the service, with bridge letter",
   "why": "Independent evidence of operating controls",
   "validity": "period end <= 12 months"
  },
  {
   "document": "ISO/IEC 27001:2022 certificate with scope",
   "why": "Independent certification",
   "validity": "in date, 2022 edition"
  },
  {
   "document": "Penetration test executive summary",
   "why": "Tier 1 evidence",
   "validity": "<= 12 months"
  },
  {
   "document": "PCI DSS 4.0.1 AOC for service providers",
   "why": "Card data (A4)",
   "validity": "in date"
  },
  {
   "document": "Subprocessor list with locations",
   "why": "Fourth parties, data location",
   "validity": "current"
  }
 ],
 "evidence": [],
 "documents": [],
 "screening": [],
 "controls": [],
 "mismatches": [],
 "findings": [],
 "fourth_parties": [],
 "regime_checks": [],
 "contract_clauses": [],
 "exit": {
  "plan": null,
  "data_return": null,
  "deletion": null,
  "transition": null,
  "replacement_time": null,
  "status": ""
 },
 "actions": [],
 "conditions": [],
 "complementary_controls": [],
 "specialist_requests": [],
 "exceptions": [],
 "decision": {
  "status": "pending",
  "option": null,
  "by": null,
  "role": null,
  "date": null,
  "conditions": [],
  "state": null
 },
 "monitoring": {
  "next_review_due": null,
  "quarterly_check": true,
  "expiring": [],
  "triggers": [],
  "overdue": []
 },
 "qa": {
  "status": "QA pending",
  "reviewer": null
 },
 "assumptions": [],
 "coverage": {
  "read": [],
  "not_read": []
 },
 "suspicious_input": [],
 "handoffs": [],
 "runtime_tools": {
  "file_read": "Read",
  "web_search": "WebSearch",
  "page_fetch": "WebFetch"
 }
}
```
Validation: NOT RUN (chat mode).
