const express = require('express');
const { requireAuth } = require('./middleware/auth');
const ordersRouter = require('./routes/orders');

const app = express();
app.use(express.json());

// every /api route requires a signed-in customer
app.use('/api', requireAuth);
app.use('/api/orders', ordersRouter);

app.listen(8080);
