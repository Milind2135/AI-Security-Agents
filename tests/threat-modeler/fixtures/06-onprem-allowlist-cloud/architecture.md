# Partner pricing API — architecture (SYNTHETIC TEST SYSTEM)

The pricing API was moved from the on-premises data centre to a cloud function in 2026.
It returns confidential partner price lists (contract prices, discounts).

## Security
- Access is restricted to partner networks by the corporate perimeter firewall allow-list FW-ALLOW-12 (partner IP ranges 198.51.100.0/24 and 203.0.113.0/24). This control was in place for the on-premises deployment and is carried over unchanged.
- Partners authenticate with a shared API key sent in the `x-api-key` header.
