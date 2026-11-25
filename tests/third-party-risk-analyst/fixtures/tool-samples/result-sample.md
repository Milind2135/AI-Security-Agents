third-party-risk-analyst v1.0 | result

> TOOL TEST SAMPLE (SYNTHETIC) — hand-made record used only to test tools/tprm/tprm.py; not an expected agent output.

```json
{
 "agent": "third-party-risk-analyst",
 "version": "1.0",
 "stage": "result",
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
  "residual_risk": "High",
  "residual_if_conditions_met": "Medium"
 },
 "tier_confirmation": {
  "status": "confirmed",
  "by": "A. Example, Head of TPRM (as given \u2014 not verified)",
  "date": "2026-11-26",
  "reason": null
 },
 "tier_history": [
  {
   "date": "2026-11-26",
   "tier": 1,
   "reason": "automatic rules C1+C2, A1/A4",
   "confirmed_by": "A. Example, Head of TPRM",
   "policy_version": "3.0"
  }
 ],
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
 "evidence": [
  {
   "id": "E-1",
   "path": "evidence/questionnaire-payflow.converted.md",
   "type": "questionnaire",
   "issuer": "vendor",
   "date": null,
   "period_end": null,
   "expires": null,
   "scope_ok": null,
   "status": "Claimed"
  },
  {
   "id": "E-2",
   "path": "evidence/soc2-type2-summary.md",
   "type": "SOC 2 Type II",
   "issuer": "Example Assurance LLP",
   "date": null,
   "period_end": "2026-06-30",
   "expires": null,
   "scope_ok": true,
   "status": "Verified"
  },
  {
   "id": "E-3",
   "path": "evidence/iso27001-certificate.md",
   "type": "ISO/IEC 27001:2013 certificate",
   "issuer": "Example Certification Body",
   "date": "2022-11-01",
   "period_end": null,
   "expires": "2025-10-31",
   "scope_ok": false,
   "status": "Expired"
  }
 ],
 "documents": [],
 "screening": [
  {
   "check": "Sanctions, PEP, adverse media",
   "status": "Red flag",
   "detail": "Potential match on owner R.K. pending screening team",
   "evidence": [
    "screening-results.md"
   ]
  }
 ],
 "controls": [
  {
   "q": "VP-01",
   "domain": "00",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "VP-01.1",
   "domain": "00",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "VP-01.2",
   "domain": "00",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "VP-01.3",
   "domain": "00",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "DOC-01",
   "domain": "01",
   "answer": "Yes",
   "evidence_status": "Expired",
   "result": "Not satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": "ISO certificate is the 2013 edition and expired 2025-10-31"
  },
  {
   "q": "DOC-01.1",
   "domain": "01",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "DOC-01.2",
   "domain": "01",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "DOC-01.3",
   "domain": "01",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "GOV-01",
   "domain": "02",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "GOV-01.1",
   "domain": "02",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "GOV-01.2",
   "domain": "02",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "GOV-01.3",
   "domain": "02",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "AST-01",
   "domain": "03",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "AST-01.1",
   "domain": "03",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "AST-01.2",
   "domain": "03",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "AST-01.3",
   "domain": "03",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "PPL-01",
   "domain": "04",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "PPL-01.1",
   "domain": "04",
   "answer": "Yes",
   "evidence_status": "Contradicted",
   "result": "Not satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": "SOC 2 exception CC6.2: 4\u20139 days"
  },
  {
   "q": "PPL-01.2",
   "domain": "04",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "PPL-01.3",
   "domain": "04",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "OPS-01",
   "domain": "06",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "OPS-01.1",
   "domain": "06",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "OPS-01.2",
   "domain": "06",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "OPS-01.3",
   "domain": "06",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "NET-01",
   "domain": "07",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "NET-01.1",
   "domain": "07",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "NET-01.2",
   "domain": "07",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "NET-01.3",
   "domain": "07",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "END-01",
   "domain": "08",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "END-01.1",
   "domain": "08",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "END-01.2",
   "domain": "08",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "SRV-01",
   "domain": "09",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "SRV-01.1",
   "domain": "09",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "SRV-01.2",
   "domain": "09",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "LOG-01",
   "domain": "10",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "LOG-01.1",
   "domain": "10",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "LOG-01.2",
   "domain": "10",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "LOG-01.3",
   "domain": "10",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "IAM-01",
   "domain": "11",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "IAM-01.1",
   "domain": "11",
   "answer": "Yes",
   "evidence_status": "Verified",
   "result": "Satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "IAM-01.2",
   "domain": "11",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "IAM-01.3",
   "domain": "11",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "IAM-01.4",
   "domain": "11",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "DEV-01",
   "domain": "12",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "DEV-01.1",
   "domain": "12",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "DEV-01.2",
   "domain": "12",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "DEV-01.3",
   "domain": "12",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "INC-01",
   "domain": "13",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "INC-01.1",
   "domain": "13",
   "answer": "Yes",
   "evidence_status": "Claimed",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": "72 hours does not meet IN-RBI"
  },
  {
   "q": "INC-01.2",
   "domain": "13",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "INC-01.3",
   "domain": "13",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "RES-01",
   "domain": "14",
   "answer": "Yes",
   "evidence_status": "Claimed",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": "No test report"
  },
  {
   "q": "RES-01.1",
   "domain": "14",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "RES-01.2",
   "domain": "14",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "RES-01.3",
   "domain": "14",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "CMP-01",
   "domain": "15",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "CMP-01.1",
   "domain": "15",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "CMP-01.2",
   "domain": "15",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "PRV-01",
   "domain": "16",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "PRV-01.1",
   "domain": "16",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "PRV-01.2",
   "domain": "16",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "PRV-01.3",
   "domain": "16",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "CRY-01",
   "domain": "17",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "CRY-01.1",
   "domain": "17",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "CRY-01.2",
   "domain": "17",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "TVM-01",
   "domain": "18",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "TVM-01.1",
   "domain": "18",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "TVM-01.2",
   "domain": "18",
   "answer": "Yes",
   "evidence_status": "Expired",
   "result": "Not satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": "Test August 2025; 1 High open"
  },
  {
   "q": "TVM-01.3",
   "domain": "18",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "CLD-01",
   "domain": "19",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "CLD-01.1",
   "domain": "19",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "CLD-01.2",
   "domain": "19",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "SCM-01",
   "domain": "20",
   "answer": "Yes",
   "evidence_status": "Contradicted",
   "result": "Not satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": "SOC 2 carve-out and subprocessor list"
  },
  {
   "q": "SCM-01.1",
   "domain": "20",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "SCM-01.2",
   "domain": "20",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "SCM-01.3",
   "domain": "20",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "AI-01",
   "domain": "21",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "AI-01.1",
   "domain": "21",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "AI-01.2",
   "domain": "21",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "AI-01.3",
   "domain": "21",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "ESG-01",
   "domain": "22",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "ESG-01.1",
   "domain": "22",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "FIN-01",
   "domain": "23",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "FIN-01.1",
   "domain": "23",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "FIN-01.2",
   "domain": "23",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "EXT-01",
   "domain": "24",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "EXT-01.1",
   "domain": "24",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "EXT-01.2",
   "domain": "24",
   "answer": "Yes",
   "evidence_status": "Documented",
   "result": "Partly satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": null
  },
  {
   "q": "EXT-01.3",
   "domain": "24",
   "answer": "Yes",
   "evidence_status": "Missing",
   "result": "Not satisfactory",
   "evidence": [
    "E-1"
   ],
   "further_work": "No answer"
  }
 ],
 "mismatches": [],
 "findings": [
  {
   "id": "F-1",
   "severity": "High",
   "domain": "20",
   "questions": [
    "SCM-01"
   ],
   "finding": "Vendor says no subcontractors; SOC 2 and subprocessor list show three",
   "evidence": [
    "E-1",
    "E-2"
   ],
   "why": "Card and customer data handled by undisclosed fourth parties",
   "recommendation": "REQUIRES APPROVAL \u2014 TPRM: obtain full subprocessor list and assurance",
   "status": "Open",
   "previous_status": null
  },
  {
   "id": "F-2",
   "severity": "High",
   "domain": "13",
   "questions": [
    "INC-01.1"
   ],
   "finding": "72-hour incident notice",
   "evidence": [
    "E-1"
   ],
   "why": "Cannot meet 6-hour reporting",
   "recommendation": "REQUIRES APPROVAL \u2014 Legal: 6-hour notice clause",
   "status": "Open",
   "previous_status": null
  }
 ],
 "fourth_parties": [
  {
   "id": "FP-1",
   "name": "CloudHost Example",
   "service": "Hosting",
   "data_access": "all",
   "location": "IN, DE",
   "evidence": [
    "E-2"
   ]
  }
 ],
 "regime_checks": [
  {
   "regime": "IN-RBI",
   "item": "Incident reporting fast enough for 6-hour RBI reporting",
   "status": "Gap",
   "evidence": [
    "contract-draft.md \u00a79"
   ]
  }
 ],
 "contract_clauses": [
  {
   "id": "CL-1",
   "clause": "Right to audit incl. regulators",
   "required_by": "policy \u00a77.3; IN-RBI; EU-DORA",
   "status": "Missing",
   "evidence": "contract-draft.md"
  }
 ],
 "exit": {
  "plan": null,
  "data_return": null,
  "deletion": null,
  "transition": null,
  "replacement_time": null,
  "status": ""
 },
 "actions": [
  {
   "id": "ACT-1",
   "for": [
    "F-1"
   ],
   "action": "Obtain subprocessor list and their assurance",
   "owner_role": "TPRM analyst",
   "due": "2027-02-23",
   "status": "Open"
  }
 ],
 "conditions": [
  {
   "id": "CON-1",
   "condition": "6-hour incident notice clause before signature",
   "due": "before signature",
   "status": "Proposed"
  }
 ],
 "complementary_controls": [],
 "specialist_requests": [
  {
   "id": "SR-1",
   "team": "Privacy",
   "question": "Transfer to Singapore support and US email relay",
   "status": "Open",
   "answer": null
  }
 ],
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
  "next_review_due": "2027-11-26",
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
