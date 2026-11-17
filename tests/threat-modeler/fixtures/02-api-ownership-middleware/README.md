# Orders API (SYNTHETIC TEST SYSTEM)

Customers sign in on the web shop and view their past orders. Order records contain name, delivery address, phone number and the last four digits of the payment card.

- Runtime: Node.js (Express) behind a public HTTPS load balancer.
- Database: PostgreSQL table `orders` (customer_id, items, address, phone, card_last4).
- Authentication: JWT issued by the shop's sign-in service.
