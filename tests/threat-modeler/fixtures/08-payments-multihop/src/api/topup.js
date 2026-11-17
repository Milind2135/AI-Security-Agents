const express = require('express');
const { requireAuth } = require('./auth');
const queue = require('./queue');
const db = require('./db');
const router = express.Router();

router.post('/wallets/:walletId/topup', requireAuth, async (req, res) => {
  console.log('topup request', JSON.stringify(req.body));
  const wallet = await db.query('SELECT owner_id FROM wallets WHERE id = $1', [req.params.walletId]);
  if (!wallet.rows.length || wallet.rows[0].owner_id !== req.user.sub) return res.status(404).end();
  await queue.publish('settlement', {
    walletId: req.params.walletId,
    amount: req.body.amount,
    cardNumber: req.body.cardNumber,
    expiry: req.body.expiry
  });
  await fetch('https://collect.analytics-vendor.example/v1/events', {
    method: 'POST',
    body: JSON.stringify({ event: 'topup', email: req.user.email, amount: req.body.amount })
  });
  return res.status(202).json({ status: 'accepted' });
});

module.exports = router;
