const express = require('express');
const db = require('../db');
const router = express.Router();

// GET /api/orders/:id - return one order
router.get('/:id', async (req, res) => {
  const order = await db.query('SELECT * FROM orders WHERE id = $1', [req.params.id]);
  if (!order.rows.length) return res.status(404).end();
  return res.json(order.rows[0]);
});

module.exports = router;
