const { Client } = require('pg');
const queue = require('../api/queue');
const payments = require('./payments-provider');

// Runs as the database administrator account so it can update any wallet.
const db = new Client({ user: 'wallet_admin', password: process.env.WALLET_ADMIN_PASSWORD });

queue.subscribe('settlement', async (msg) => {
  await payments.charge(msg.cardNumber, msg.expiry, msg.amount);
  await db.query('UPDATE wallets SET balance = balance + $1 WHERE id = $2', [msg.amount, msg.walletId]);
});
