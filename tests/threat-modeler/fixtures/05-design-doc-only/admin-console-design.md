# Admin console — design (SYNTHETIC TEST SYSTEM)

## Purpose
Support staff use the admin console to look up customer accounts, reset customer passwords and issue refunds up to 500 EUR.

## Users
- Support agents (about 40), internal.
- Support team leads (5) can also change refund limits.

## Architecture
- Web UI served from the internal network and published to the internet through the company's reverse proxy so that remote support staff can work from home.
- Back end calls the customer database and the payments API.

## Security
- Sign-in with username and password against the company directory.
- **MFA is planned for the admin console in Q1 next year.**
- All admin actions will be logged to the SIEM (to be implemented).
