/**
 * Check Alpha wallet L1 ETH + AZTEC token balances
 * for fee juice bridging assessment
 */
import { createPublicClient, http, formatEther } from '@aztec/viem';
import { mainnet } from '@aztec/viem/chains';

const ALPHA_ADDRESS = process.env.ALPHA_ADDRESS;
if (!ALPHA_ADDRESS) { console.error('Missing ALPHA_ADDRESS'); process.exit(1); }

// Aztec L1 contract addresses
const AZTEC_TOKEN_L1 = '0xa27ec0006e59f245217ff08cd52a7e8b169e62d2';
const FEE_JUICE_PORTAL = '0x2891f8b941067f8b5a3f34545a30cf71e3e23617';
const ROLLUP = '0xae2001f7e21d5ecabf6234e9fdd1e76f50f74962';

// ERC20 ABI minimal
const ERC20_ABI = [
  { name: 'balanceOf', type: 'function', stateMutability: 'view',
    inputs: [{ name: 'account', type: 'address' }],
    outputs: [{ name: '', type: 'uint256' }] },
  { name: 'symbol', type: 'function', stateMutability: 'view',
    inputs: [], outputs: [{ name: '', type: 'string' }] },
  { name: 'decimals', type: 'function', stateMutability: 'view',
    inputs: [], outputs: [{ name: '', type: 'uint8' }] },
];

async function main() {
  const client = createPublicClient({
    chain: mainnet,
    transport: http('https://eth.llamarpc.com'),
  });

  console.log('=== Alpha Wallet L1 Balances ===');
  console.log('Address:', ALPHA_ADDRESS);

  // ETH balance
  const ethBal = await client.getBalance({ address: ALPHA_ADDRESS });
  console.log('ETH balance:', formatEther(ethBal), 'ETH');

  // AZTEC token balance
  const aztecBal = await client.readContract({
    address: AZTEC_TOKEN_L1,
    abi: ERC20_ABI,
    functionName: 'balanceOf',
    args: [ALPHA_ADDRESS],
  });
  const aztecDecimals = await client.readContract({
    address: AZTEC_TOKEN_L1,
    abi: ERC20_ABI,
    functionName: 'decimals',
  });
  const aztecFormatted = Number(aztecBal) / (10 ** aztecDecimals);
  console.log('AZTEC balance:', aztecFormatted, 'AZTEC');

  console.log('\n=== Fee Juice Assessment ===');
  console.log('FeeJuicePortal (L1):', FEE_JUICE_PORTAL);
  console.log('AZTEC token (L1):   ', AZTEC_TOKEN_L1);

  if (aztecBal > 0n) {
    console.log('\n✅ Have AZTEC tokens! Can bridge to L2 as fee juice.');
    console.log('Aztec account to fund: 0x11a328e0f152d8fc7ac7f8c2e471ba972f479fd84f67d2ee1732aee79415cfad');
  } else {
    console.log('\n⚠️  No AZTEC tokens on L1. Need to acquire to pay fees.');
    console.log('Options:');
    console.log('  - Buy AZTEC on Gate.io, MEXC, or DEX (Uniswap)');
    console.log('  - Min amount needed: ~1-10 AZTEC for account deploy + txs');
  }
}

main().catch(console.error);
