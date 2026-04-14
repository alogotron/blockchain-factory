import { wrapFetchWithPayment, x402Client } from '@x402/fetch';
import { registerExactEvmScheme } from '@x402/evm/exact/client';
import { privateKeyToAccount } from 'viem/accounts';

const BETA_KEY = '0x4a9f3fbbfacb6a842d2b5ac728de7cf951f0b0ccf527f65a60f447a06552800e';
const SERVER_URL = 'http://localhost:4021';

if (!BETA_KEY) {
  console.error('ERROR: AGENT_BETA_PRIVATE_KEY not set');
  process.exit(1);
}

// Normalize key - ensure 0x prefix
const privateKey = BETA_KEY.startsWith('0x') ? BETA_KEY : `0x${BETA_KEY}`;

const signer = privateKeyToAccount(privateKey);
console.log(`[x402 Client] Payer wallet (Beta): ${signer.address}`);
console.log(`[x402 Client] Target server: ${SERVER_URL}`);
console.log(`[x402 Client] Network: Base Sepolia\n`);

// Setup x402 client with EVM scheme
const client = new x402Client();
registerExactEvmScheme(client, { signer });
const fetchWithPayment = wrapFetchWithPayment(fetch, client);

async function run() {
  // Step 1: Free health check
  console.log('--- Step 1: Free /health endpoint ---');
  const health = await fetch(`${SERVER_URL}/health`);
  const healthData = await health.json();
  console.log('Response:', JSON.stringify(healthData, null, 2));

  // Step 2: Paid /ping ($0.0001 USDC)
  console.log('\n--- Step 2: Paid /ping ($0.0001 USDC) ---');
  console.log('Sending request... x402 client will auto-handle 402 flow');
  const ping = await fetchWithPayment(`${SERVER_URL}/ping`);
  const pingData = await ping.json();
  console.log('Status:', ping.status);
  console.log('Response:', JSON.stringify(pingData, null, 2));
  const pingReceipt = ping.headers.get('PAYMENT-RESPONSE');
  if (pingReceipt) {
    const receipt = JSON.parse(Buffer.from(pingReceipt, 'base64').toString());
    console.log('Payment receipt:', JSON.stringify(receipt, null, 2));
  }

  // Step 3: Paid /info ($0.001 USDC)
  console.log('\n--- Step 3: Paid /info ($0.001 USDC) ---');
  console.log('Sending request...');
  const info = await fetchWithPayment(`${SERVER_URL}/info`);
  const infoData = await info.json();
  console.log('Status:', info.status);
  console.log('Response:', JSON.stringify(infoData, null, 2));
  const infoReceipt = info.headers.get('PAYMENT-RESPONSE');
  if (infoReceipt) {
    const receipt = JSON.parse(Buffer.from(infoReceipt, 'base64').toString());
    console.log('Payment receipt:', JSON.stringify(receipt, null, 2));
  }

  console.log('\n✅ Done. All x402 calls completed.');
}

run().catch(err => {
  console.error('ERROR:', err.message);
  process.exit(1);
});
