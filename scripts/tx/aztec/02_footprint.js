/**
 * Aztec Alpha mainnet footprint script
 * Reads credentials from env vars: ALPHA_PRIVATE_KEY
 */
import { createAztecNodeClient, waitForNode } from '@aztec/aztec.js/node';
import { AccountManager } from '@aztec/aztec.js/wallet';
import { Fr } from '@aztec/aztec.js/fields';
import { EcdsaKAccountContract } from '@aztec/accounts/ecdsa';
import { createHash } from 'crypto';

const NODE_URL = 'https://aztec-mainnet.drpc.org';

const rawKey = process.env.ALPHA_PRIVATE_KEY;
if (!rawKey) { console.error('Missing ALPHA_PRIVATE_KEY env var'); process.exit(1); }

const privateKeyHex = rawKey.replace('0x', '');
const privateKeyBytes = Buffer.from(privateKeyHex, 'hex');
const signingKey = privateKeyBytes;

// BN254 Fr secret key — must be < field modulus, derive via SHA256 + mask
function deriveSecretKey(pkBytes) {
  const hash = createHash('sha256').update(pkBytes).digest();
  hash[0] = hash[0] & 0x1f; // zero top 3 bits to guarantee < BN254 modulus
  return Fr.fromBuffer(hash);
}

const secretKey = deriveSecretKey(privateKeyBytes);

async function main() {
  console.log('=== Aztec Alpha Mainnet Footprint ===');
  console.log('Node:', NODE_URL);

  const node = createAztecNodeClient(NODE_URL);
  await waitForNode(node);

  const blockNumber = await node.getBlockNumber();
  console.log('Block:', blockNumber);

  // Create account contract and manager
  const accountContract = new EcdsaKAccountContract(signingKey);
  const accountManager = await AccountManager.create(node, secretKey, accountContract);

  const completeAddress = await accountManager.getCompleteAddress();
  const accountAddress = completeAddress.address;
  console.log('\nAztec account address:', accountAddress.toString());

  // Check if already deployed
  const isDeployed = await node.isContractInstanceDeployed(accountAddress);
  console.log('Account deployed:', isDeployed);

  // Show fee juice info
  const nodeInfo = await node.getNodeInfo();
  console.log('\nFee juice info:');
  console.log('  FeeJuicePortal (L1):', nodeInfo.l1ContractAddresses.feeJuicePortalAddress);
  console.log('  AZTEC token (L1):   ', nodeInfo.l1ContractAddresses.feeJuiceAddress);
  console.log('  StakingAsset (L1):  ', nodeInfo.l1ContractAddresses.stakingAssetAddress);

  if (!isDeployed) {
    console.log('\n⚠️  Account not deployed. Steps to get fee juice and deploy:');
    console.log('  1. Buy or acquire AZTEC tokens on Ethereum mainnet');
    console.log('  2. Approve FeeJuicePortal (' + nodeInfo.l1ContractAddresses.feeJuicePortalAddress + ')');
    console.log('  3. Call depositToAztecPublic(recipient=' + accountAddress.toString() + ', amount, nonce)');
    console.log('  4. Wait ~2 L2 blocks for L1->L2 message');
    console.log('  5. Run deployment with fee juice claim');
  } else {
    console.log('\n✅ Account deployed and ready!');
  }
}

main().catch(console.error);
