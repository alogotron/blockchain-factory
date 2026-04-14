/**
 * Deploy Aztec account using SponsoredFPC (free fees)
 * Alpha wallet -> Aztec mainnet footprint
 */
import { createAztecNodeClient, waitForNode, waitForTx } from '@aztec/aztec.js/node';
import { AccountManager } from '@aztec/aztec.js/wallet';
import { Fr } from '@aztec/aztec.js/fields';
import { SponsoredFeePaymentMethod } from '@aztec/aztec.js/fee';
import { EcdsaKAccountContract } from '@aztec/accounts/ecdsa';
import { getContractInstanceFromInstantiationParams } from '@aztec/aztec.js/contracts';
import { createHash } from 'crypto';

const NODE_URL = 'https://aztec-mainnet.drpc.org';

const rawKey = process.env.ALPHA_PRIVATE_KEY;
if (!rawKey) { console.error('Missing ALPHA_PRIVATE_KEY'); process.exit(1); }
const privateKeyBytes = Buffer.from(rawKey.replace('0x',''), 'hex');

function deriveSecretKey(pkBytes) {
  const hash = createHash('sha256').update(pkBytes).digest();
  hash[0] = hash[0] & 0x1f;
  return Fr.fromBuffer(hash);
}

async function main() {
  console.log('=== Aztec Alpha — Account Deployment ===');
  const node = createAztecNodeClient(NODE_URL);
  await waitForNode(node);
  const block = await node.getBlockNumber();
  console.log('Block:', block);

  const secretKey = deriveSecretKey(privateKeyBytes);
  const accountContract = new EcdsaKAccountContract(privateKeyBytes);
  const accountManager = await AccountManager.create(node, secretKey, accountContract);
  const completeAddress = await accountManager.getCompleteAddress();
  const accountAddress = completeAddress.address;
  console.log('Account address:', accountAddress.toString());

  // Get SponsoredFPC - deployed at deterministic address with salt=0
  // First check if it's in protocol contracts or needs to be fetched
  let sponsoredFPCAddress;
  try {
    // Try to import SponsoredFPC artifact
    const { default: SponsoredFPCJson } = await import(
      './node_modules/@aztec/accounts/dest/testing/sponsored_fpc/SponsoredFPC.json',
      { assert: { type: 'json' } }
    );
    const { loadContractArtifact } = await import('@aztec/aztec.js/abi');
    const artifact = loadContractArtifact(SponsoredFPCJson);
    const fpcInstance = await getContractInstanceFromInstantiationParams(artifact, { salt: Fr.ZERO });
    sponsoredFPCAddress = fpcInstance.address;
    console.log('SponsoredFPC address (computed):', sponsoredFPCAddress.toString());
  } catch(e) {
    console.log('Could not compute FPC address:', e.message);
    // Fallback: use known mainnet SponsoredFPC address if available
    console.log('Checking if account needs fee juice...');
  }

  if (sponsoredFPCAddress) {
    const feeMethod = new SponsoredFeePaymentMethod(sponsoredFPCAddress);
    console.log('\nDeploying account with sponsored fees...');
    try {
      const deployMethod = await accountManager.getDeployMethod();
      const tx = await deployMethod.send({ fee: { paymentMethod: feeMethod } });
      console.log('Tx sent! Hash:', tx.getTxHash().toString());
      console.log('Waiting for confirmation...');
      const receipt = await tx.wait();
      console.log('✅ Account deployed! Status:', receipt.status);
      console.log('Block:', receipt.blockNumber);
    } catch(e) {
      console.error('Deploy failed:', e.message);
    }
  }
}

main().catch(console.error);
