import express from 'express';
import { paymentMiddleware, x402ResourceServer } from '@x402/express';
import { HTTPFacilitatorClient } from '@x402/core/server';
import { ExactEvmScheme, registerExactEvmScheme } from '@x402/evm/exact/server';

const PORT = 4021;
const PAY_TO = '0xaAB80bC6B6040aE845cE225181fD72297bA71b13'; // Alpha wallet

console.log(`[x402 Server] Starting...`);
console.log(`[x402 Server] payTo: ${PAY_TO}`);
console.log(`[x402 Server] Network: Base Sepolia (eip155:84532)`);

// Free testnet facilitator — no API key needed
const facilitator = new HTTPFacilitatorClient({
  url: 'https://x402.org/facilitator'
});

// Resource server with EVM scheme registered
const server = new x402ResourceServer(facilitator);
registerExactEvmScheme(server);

const routes = {
  'GET /info': {
    accepts: [
      {
        scheme: 'exact',
        price: '$0.001',
        network: 'eip155:84532',
        payTo: PAY_TO,
      },
    ],
    description: 'Blockchain Factory agent info — paid x402 endpoint',
    mimeType: 'application/json',
  },
  'GET /ping': {
    accepts: [
      {
        scheme: 'exact',
        price: '$0.0001',
        network: 'eip155:84532',
        payTo: PAY_TO,
      },
    ],
    description: 'Paid ping — cheapest x402 call',
    mimeType: 'application/json',
  },
};

const app = express();

app.use(paymentMiddleware(routes, server));

app.get('/info', (req, res) => {
  res.json({
    name: 'Blockchain Factory Agent',
    owner: 'alogotron',
    capabilities: ['x402', 'ERC-8004', 'ChaosChain', 'Base'],
    timestamp: new Date().toISOString(),
    network: 'Base Sepolia',
    protocol: 'x402 v2',
  });
});

app.get('/ping', (req, res) => {
  res.json({ pong: true, timestamp: new Date().toISOString() });
});

// Free — no payment required
app.get('/health', (req, res) => {
  res.json({ status: 'ok', payTo: PAY_TO, network: 'eip155:84532' });
});

app.listen(PORT, () => {
  console.log(`\n[x402 Server] Listening on http://localhost:${PORT}`);
  console.log(`  FREE : GET /health`);
  console.log(`  PAID : GET /ping    $0.0001 USDC`);
  console.log(`  PAID : GET /info    $0.001  USDC`);
  console.log(`\nTest 402 response: curl -i http://localhost:${PORT}/info`);
});
