# Environment context (SYNTHETIC TEST DATA)

- chat-app-02.corp.example.com runs the customer support chatbot (owner: Support Platform team).
- Approved outbound destinations for chat-app-02: `ai-model-api.example.com` (AI model API, contract CR-2026-114, approved 2026-09-01). Normal volume: 300–600 requests per hour during business hours.
- Service account svc-supportbot is used only by the support-bot process.
