# SYNTHETIC TEST DATA — context
- app-role is the instance role of web-01 (account 111122223333, production). Normal use: calls from inside the VPC only; besides s3:GetObject/ListBucket it still has an inline policy granting `iam:*`, left over from a 2025 migration (known clean-up item, not yet removed).
- No change tickets exist for IAM changes on 2026-11-16.
