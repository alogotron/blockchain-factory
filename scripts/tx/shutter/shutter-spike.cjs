/**
 * Shutter Network API + SDK Integration Spike (CJS)
 * Full encrypt -> wait -> decrypt flow on Chiado testnet (Gnosis)
 */

const { randomBytes } = require('crypto');
const fs = require('fs');

const API_BASE = 'https://shutter-api.chiado.staging.shutter.network/api';
const MESSAGE = 'shutter-spike: identity-gated front-run-proof tx by alogotron';

function log(label, value) {
  console.log(`\n[${label}]`);
  if (typeof value === 'object') {
    console.log(JSON.stringify(value, null, 2));
  } else {
    console.log(value);
  }
}

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  const text = await res.text();
  if (!res.ok) throw new Error(`GET ${path} => ${res.status}: ${text}`);
  return JSON.parse(text);
}

async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`POST ${path} => ${res.status}: ${text}`);
  return JSON.parse(text);
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function main() {
  // Lazy load SDK via require (CJS path)
  const sdk = require('@shutter-network/shutter-sdk');
  const encryptData = sdk.encryptData;
  const decrypt = sdk.decrypt;

  console.log('=== Shutter Network SDK Spike ===');
  console.log(`Message: "${MESSAGE}"`);

  // Step 1: Register identity
  const identityPrefix = '0x' + randomBytes(32).toString('hex');
  const decryptionTimestamp = Math.floor(Date.now() / 1000) + 90;
  log('Step 1: Register Identity', { identityPrefix, decryptionTimestamp });

  const reg = await apiPost('/register_identity', { decryptionTimestamp, identityPrefix });
  log('Registration response', reg);

  const regMsg = reg.message || reg;
  log('Using identity from registration', regMsg.identity);

  // Step 2: Use identity_prefix as the preimage (not the computed identity)
  log('Step 2: Prepare Encryption Params', 'Using identity_prefix as preimage for SDK...');
  const eonKey = regMsg.eon_key;
  // identityPrefix is the PREIMAGE — what we submitted
  // identity (computed hash) is returned by API but NOT used directly in encryptData
  log('eon_key', eonKey.substring(0, 40) + '...');
  log('identityPrefix (preimage)', identityPrefix);
  log('computed identity (for key retrieval)', regMsg.identity);

  // Step 3: Encrypt — SDK signature: encryptData(messageHex, eonKeyHex, identityPreimageHex, sigmaHex)
  log('Step 3: Encrypt Message', 'Using @shutter-network/shutter-sdk...');
  const sigma = '0x' + randomBytes(32).toString('hex');
  const msgHex = '0x' + Buffer.from(MESSAGE, 'utf8').toString('hex');
  let encryptedHex;
  try {
    // Correct order: message, eonKey, identityPreimage (prefix), sigma
    encryptedHex = await encryptData(msgHex, eonKey, identityPrefix, sigma);
  } catch(e) {
    console.log('SDK encryptData failed:', e.message);
    throw e;
  }
  // Step 4: Wait
  const nowSec = Math.floor(Date.now() / 1000);
  const waitSec = Math.max(decryptionTimestamp - nowSec + 5, 0);
  log('Step 4: Waiting for Decryption Timestamp', `${waitSec} seconds...`);
  for (let remaining = waitSec; remaining > 0; remaining -= 10) {
    console.log(`  ${remaining}s remaining...`);
    await sleep(Math.min(10000, remaining * 1000));
  }
  // Step 5: Get decryption key using computed identity hash
  log('Step 5: Fetching Decryption Key', '');
  const computedIdentity = regMsg.identity;
  let keyData;
  for (let attempt = 1; attempt <= 6; attempt++) {
    try {
      keyData = await apiGet(`/get_decryption_key?identity=${encodeURIComponent(computedIdentity)}`);
      const key = (keyData.message || keyData).decryption_key;
      if (key) { log('Got decryption key', key.substring(0, 40) + '...'); break; }
    } catch(e) {
      console.log(`  Attempt ${attempt}/6 failed: ${e.message}`);
    }
    if (attempt < 6) { console.log('  Retrying in 10s...'); await sleep(10000); }
  }
  log('Key data', keyData);

  const decryptionKey = (keyData.message || keyData).decryption_key;
  if (!decryptionKey) throw new Error('Could not obtain decryption key after retries');

  // Step 6: Decrypt
  log('Step 6: Decrypt', '');
  const decryptedHex = await decrypt(encryptedHex, decryptionKey);
  const decryptedStr = Buffer.from(decryptedHex.replace('0x', ''), 'hex').toString('utf8');
  log('Decrypted result', decryptedStr);

  const success = decryptedStr === MESSAGE || decryptedStr === msgHex;
  console.log(success
    ? '\n✅ SUCCESS: Full Shutter encrypt/decrypt cycle works!'
    : `\n⚠️  Result: "${decryptedStr}" (check hex vs string encoding)`);

  // Save summary
  const summary = {
    timestamp: new Date().toISOString(),
    network: 'chiado-testnet',
    message: MESSAGE,
    identityPrefix,
    decryptionTimestamp,
    eonKey: eonKey.substring(0, 40) + '...',
    identity: computedIdentity,
    encryptedLengthBytes: encryptedHex.replace('0x','').length / 2,
    decryptedResult: decryptedStr,
    success,
  };
  const logDir = '/a0/usr/projects/blockchain-factory/logs/2026-04-14';
  fs.mkdirSync(logDir, { recursive: true });
  fs.writeFileSync(`${logDir}/shutter-spike-result.json`, JSON.stringify(summary, null, 2));
  console.log(`\nResult saved to ${logDir}/shutter-spike-result.json`);
  console.log('\n=== Spike complete ===');
}

main().catch(err => { console.error('Fatal:', err); process.exit(1); });
