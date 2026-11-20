# Card top-up service — architecture (SYNTHETIC TEST SYSTEM)

Signed-in customers top up their wallet with a payment card.

## Flow
Browser → CDN (HTTPS) → Top-up API → settlement queue → settlement worker → wallet database.

## Security
- All traffic is encrypted with HTTPS end to end.
- The Top-up API checks that the customer owns the wallet.
- The service makes **no calls to external services**.
- Card numbers are never stored or logged.
