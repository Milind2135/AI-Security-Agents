# Vulnerability Triage Report — {CVE-ID}

**Generated (UTC):** {timestamp}
**Agent:** vm-triage
**Report type:** Public vulnerability intelligence (no internal exposure or priority assessment)

<!--
RULES (delete this comment block in the final report)
- Keep all 26 headings exactly as written, in this order.
- First line under each heading: **Status:** COMPLETE | PARTIAL | NOT_AVAILABLE | NOT_APPLICABLE
- If not COMPLETE, second line: **Reason:** what was attempted and why it is incomplete.
- Cite every factual statement with [S#]. Every S# must appear in Section 23.
- Replace every {placeholder}. Remove example rows you do not use.
-->

## 1. Executive Summary
**Status:** COMPLETE
{3–6 sentences: what it is, what is affected, severity per sources, exploitation/KEV status, whether a fix exists. Cite.}

## 2. CVE Identity
**Status:** COMPLETE
- **CVE ID:** {CVE-ID}
- **Record State:** {PUBLISHED | REJECTED} [S1]
- **CNA:** {assigner} [S1]
- **Title:** {title} [S1]
- **CWE:** {CWE-xxx (name)} [S1][S2]
- **Aliases:** {GHSA-…, vendor IDs, nicknames} [S#]
- **Reserved / Published / Updated:** {dates} [S1]

## 3. Affected Products/Versions
**Status:** COMPLETE
| Vendor | Product / Package | Affected | Fixed | Source |
|---|---|---|---|---|
| {vendor} | {product} | {range} | {version} | [S#] |

{Note configuration prerequisites (feature enabled, default/non-default config). Cite.}

## 4. Vulnerability Description
**Status:** COMPLETE
{Technical root cause in plain language. Cite.}

## 5. Severity/Scoring
**Status:** COMPLETE
| Source | Version | Base Score | Severity | Vector | Cite |
|---|---|---|---|---|---|
| {NVD / CNA / ADP} | {3.1} | {x.x} | {HIGH} | `{CVSS:3.1/…}` | [S#] |

{Scoring rationale; note which vector is authoritative for which purpose. SSVC if present.}

## 6. EPSS
**Status:** COMPLETE
- **EPSS Score:** {0.00000} [S3]
- **EPSS Percentile:** {0.00000} [S3]
- **EPSS Date:** {YYYY-MM-DD} [S3]
- **30-day trend:** {range / direction} [S3]
- **Interpretation:** {what the probability means; EPSS is a 30-day exploitation-activity likelihood, not severity}

## 7. CISA KEV
**Status:** COMPLETE
- **KEV Listed:** {Yes | No} [S4]
- **Date Added:** {YYYY-MM-DD or N/A} [S4]
- **Due Date (FCEB):** {YYYY-MM-DD or N/A} [S4]
- **Known Ransomware Campaign Use:** {Known | Unknown | N/A} [S4]
- **Required Action:** {text or N/A} [S4]

## 8. Exploitation Status
**Status:** COMPLETE
- **In-the-wild exploitation:** {Confirmed | Reported (unconfirmed) | No public reports found}
- **Classification:** {Demonstrated | Theoretical}
{Evidence with dates and reporters. Cite.}
**Confidence:** {High | Medium | Low} — {basis}

## 9. Exploit Availability
**Status:** COMPLETE
| Type | Reference | Maturity | Date | Source |
|---|---|---|---|---|
| {PoC / weaponized / Metasploit / scanner template} | {name or URL} | {functional / partial / unverified} | {date} | [S#] |

## 10. Exploitation Mechanics
**Status:** COMPLETE
{How the flaw is triggered, at a conceptual level (inputs, components, conditions). Do not include working exploit payloads. Cite.}

## 11. Attack Path
**Status:** COMPLETE
- **Attack vector / access required:** {network, adjacent, local, physical} [S#]
- **Authentication / privileges:** {…} [S#]
- **User interaction:** {…} [S#]
- **Preconditions:** {…} [S#]
- **Typical sequence:** {initial access → execution → follow-on activity observed} [S#]

## 12. Threat Intelligence
**Status:** COMPLETE
| Actor / Campaign | Activity | Reported By | Date | Source |
|---|---|---|---|---|
| {name} | {what they did} | {org} | {date} | [S#] |

**Confidence:** {High | Medium | Low} — {basis}

## 13. IOCs
**Status:** COMPLETE
**IOC Extraction Status:** {EXTRACTED | NO_INDICATORS_FOUND | SOURCE_UNAVAILABLE | SNIPPET_ONLY}

| Type | Value | Context | Source | First Seen | Confidence |
|---|---|---|---|---|---|
| {ipv4} | {203.0.113[.]10} | {observed as callback for …} | [S#] | {YYYY-MM-DD} | {High} |

{Staleness note: reporting dates of infrastructure IOCs.}
**Confidence:** {High | Medium | Low} — {basis}

## 14. Detection Intelligence
**Status:** COMPLETE

### D1
**Origin:** PUBLISHED
**Platform:** {Sigma}
**Source:** [S#]
**Rule ID / Path:** {rules/…/rule.yml}
**Telemetry:** {log source}
**Limitations:** {…}
```yaml
{rule copied verbatim}
```

### D2
**Origin:** ANALYST-GENERATED
**Platform:** {Microsoft KQL}
**Rule ID / Path:** N/A
**Telemetry:** {table / log source}
**Assumptions:** {…}
**False Positives:** {…}
**Validation Required:** {…}
**Limitations:** {…}
```kql
{query}
```

## 15. Threat Hunting
**Status:** COMPLETE
| Hypothesis | Telemetry | Query Ref | Origin |
|---|---|---|---|
| {behaviour to look for} | {source} | {D# or inline} | {PUBLISHED [S#] / ANALYST-GENERATED} |

## 16. MITRE ATT&CK
**Status:** COMPLETE
| Tactic | Technique ID | Technique | Evidence | Mapping Origin |
|---|---|---|---|---|
| {Initial Access} | {T1190} | {Exploit Public-Facing Application} | [S#] | {SOURCE-STATED} |

**Confidence:** {High | Medium | Low} — {basis}

## 17. Vendor Remediation
**Status:** COMPLETE
| Product | Fixed Version / Patch | Advisory | Date | Source |
|---|---|---|---|---|
| {product} | {version} | {ID} | {date} | [S#] |

## 18. Temporary Mitigations/Workarounds
**Status:** COMPLETE
{Vendor-supported interim measures only, with their limitations. Cite.}

## 19. Compensating Controls
**Status:** COMPLETE
| Control | Risk Reduced | Limitation | Source / Origin |
|---|---|---|---|
| {WAF rule / segmentation / disable feature} | {…} | {…} | {[S#] or ANALYST-GENERATED} |

## 20. Technology Ecosystem
**Status:** COMPLETE
{Products/platforms that embed or bundle the affected component; vendor statements. Cite.}

## 21. Supply Chain
**Status:** COMPLETE
| Ecosystem | Package | Affected | Fixed | Advisory ID | Source |
|---|---|---|---|---|---|
| {Maven} | {group:artifact} | {range} | {version} | {GHSA-…} | [S#] |

## 22. Vulnerability Lifecycle
**Status:** COMPLETE
| Date | Event | Source |
|---|---|---|
| {YYYY-MM-DD} | {Reserved / disclosed / patched / KEV-added / exploitation first reported / revised} | [S#] |

## 23. Evidence/Sources
**Status:** COMPLETE
| S# | URL | Publisher | Type | Retrieval | Retrieved (UTC) |
|---|---|---|---|---|---|
| S1 | https://cveawg.mitre.org/api/cve/{CVE-ID} | CVE Program (CVE.org) | Authoritative API | API | {timestamp} |
| S2 | https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={CVE-ID} | NIST NVD | Authoritative API | API | {timestamp} |
| S3 | https://api.first.org/data/v1/epss?cve={CVE-ID}&scope=time-series | FIRST EPSS | Authoritative API | API | {timestamp} |
| S4 | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | CISA | Authoritative API | API | {timestamp} |

Retrieval values: API, FETCHED_FULL, FETCHED_PARTIAL, SNIPPET_ONLY, FAILED.

## 24. Source Conflicts
**Status:** COMPLETE
| Field | Source A | Source B | Resolution / Note |
|---|---|---|---|
| {CVSS} | {value [S#]} | {value [S#]} | {which is used and why, or "unresolved"} |

## 25. Unknowns/Gaps
**Status:** COMPLETE
- {What could not be retrieved or verified, which sources were attempted, and what would close the gap.}

## 26. Triage Conclusion
**Status:** COMPLETE
{Evidence-based summary: severity per sources, exploitation status, KEV, exploit maturity, remediation availability, key gaps. Cite.}
**Confidence:** {High | Medium | Low} — {basis}

Scope note: This report contains public vulnerability intelligence only. Exposure, business impact and remediation priority are determined downstream.
