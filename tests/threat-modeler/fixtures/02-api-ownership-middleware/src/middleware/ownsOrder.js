const db = require('../db');

// Allows the request only if the order belongs to the signed-in customer.
async function ownsOrder(req, res, next) {
  const r = await db.query('SELECT customer_id FROM orders WHERE id = $1', [req.params.id]);
  if (!r.rows.length) return res.status(404).end();
  if (r.rows[0].customer_id !== req.user.sub) return res.status(404).end();
  return next();
}

module.exports = { ownsOrder };
