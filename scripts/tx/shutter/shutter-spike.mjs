/**
 * Shutter Network API + SDK Integration Spike
 * Demonstrates full encrypt → wait → decrypt flow on Chiado testnet (Gnosis)
 * 
 * Flow:
 *   1. Register identity (decryptionTimestamp = now + 90s)
 *   2. Get encryption params (eon_key, identity)
 *   3. Encrypt a message using @shutter-network/shutter-sdk
 *   4. Wait for decryptionTimestamp
 *   5. Retrieve decryption key
 *   6. Decrypt and verify
 */

import { encryptData, decrypt } from '@shutter-network/shutter-sdk';
import { randomBytes } from 'crypto';

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
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status} ${await res.text()}`);
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST ${path} failed: ${res.status} ${await res.text()}`);
  return res.json();
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function main() {
  console.log('=== Shutter Network SDK Spike ===');
  console.log(`Message to encrypt: "${MESSAGE}"`);

  // 1. Generate identity prefix
  const identityPrefix = '0x' + randomBytes(32).toString('hex');
  const decryptionTimestamp = Math.floor(Date.now() / 1000) + 90; // 90 seconds from now
  log('Step 1: Register Identity', { identityPrefix, decryptionTimestamp });

  const registration = await apiPost('/register_identity', {
    decryptionTimestamp,
    identityPrefix,
  });
  log('Registration response', registration);

  // 2. Get encryption data
  log('Step 2: Get Encryption Data', 'Fetching eon_key and identity...');
  
  // Use address from registration or a test address
  const address = registration.address || '0x0000000000000000000000000000000000000001';
  const encData = await apiGet(
    `/get_data_for_encryption?address=${address}&identityPrefix=${encodeURIComponent(identityPrefix)}`
  );
  log('Encryption data', encData);

  const eonKey = encData.eon_key;
  const identity = encData.identity;

  // 3. Encrypt the message
  log('Step 3: Encrypt Message', 'Using @shutter-network/shutter-sdk...');
  const sigma = '0x' + randomBytes(32).toString('hex');
  const encryptedHex = await encryptData(MESSAGE, eonKey, identity, sigma);
  log('Encrypted commitment (hex)', encryptedHex.substring(0, 80) + '...');

  // 4. Wait for decryption timestamp
  const now = Math.floor(Date.now() / 1000);
  const waitSec = decryptionTimestamp - now + 5;
  log('Step 4: Wait for Decryption Window', `Waiting ${waitSec} seconds...`);
  
  for (let i = waitSec; i > 0; i -= 10) {
    console.log(`  ${i}s remaining...`);
    await sleep(Math.min(10000, i * 1000));
  }

  // 5. Get decryption key
  log('Step 5: Get Decryption Key', 'Requesting key from Keypers...');
  let keyData;
  for (let attempt = 0; attempt < 5; attempt++) {
    try {
      keyData = await apiGet(`/get_decryption_key?identity=${encodeURIComponent(identity)}`);
      if (keyData.decryption_key) break;
    } catch (e) {
      console.log(`  Attempt ${attempt + 1} failed: ${e.message}. Retrying in 10s...`);
      await sleep(10000);
    }
  }
  log('Decryption key data', keyData);

  // 6. Decrypt
  log('Step 6: Decrypt Commitment', 'Decrypting using SDK...');
  const decryptedHex = await decrypt(encryptedHex, keyData.decryption_key);
  const decryptedStr = Buffer.from(decryptedHex.replace('0x', ''), 'hex').toString('utf8');
  log('Decrypted result', decryptedStr);

  if (decryptedStr === MESSAGE) {
    console.log('\n✅ SUCCESS: Message encrypted and decrypted correctly via Shutter Network!');
  } else {
    console.log('\n❌ MISMATCH: Decrypted message does not match original.');
    console.log('Original:', MESSAGE);
    console.log('Got:     ', decryptedStr);
  }

  // Save result summary
  const summary = {
    timestamp: new Date().toISOString(),
    network: 'chiado-testnet',
    message: MESSAGE,
    identityPrefix,
    decryptionTimestamp,
    eonKey,
    identity,
    encryptedLength: encryptedHex.length,
    decryptedResult: decryptedStr,
    success: decryptedStr === MESSAGE,
  };
  console.log('\n=== Spike Summary ===');
  console.log(JSON.stringify(summary, null, 2));
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
