# SOC 2 Type II report — extract (SYNTHETIC TEST DATA)
Service organisation: PayFlow Example Ltd
Report type: SOC 2 Type II, Trust Services Criteria: Security, Availability, Confidentiality
Period: 2025-07-01 to 2026-06-30
Independent service auditor: Example Assurance LLP
Opinion: Unqualified
Services in scope: Card processing platform and tokenisation service (India and EU regions)

Subservice organisations (carve-out method): CloudHost Example (infrastructure hosting, Mumbai and Frankfurt regions); MailRelay Example (transactional email)

Complementary user entity controls:
1. User entities are responsible for protecting API keys issued to them.
2. User entities are responsible for reviewing their own users' access to the merchant portal quarterly.

Exceptions noted:
- CC6.2 (removal of access): for 3 of 25 leavers sampled, access was removed between 4 and 9 days after the leaving date. Management response: automated de-provisioning implemented on 2026-05-15.
- All other tested controls operated effectively, including MFA for administrative access (CC6.1), change management (CC8.1), backups (A1.2) and incident response (CC7.4).

No bridge letter supplied.
