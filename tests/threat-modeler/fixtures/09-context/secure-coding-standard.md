# Example Corp secure coding standard (SYNTHETIC TEST DATA)

| ID | Requirement |
|---|---|
| SC-03 | Every API request must be authenticated with the shared `requireAuth` middleware. |
| SC-07 | Every API that returns customer data must enforce object-level authorisation in shared middleware (`ownsResource` pattern) before the handler runs. |
| SC-11 | Access to customer data must be logged with the user ID and object ID. |
