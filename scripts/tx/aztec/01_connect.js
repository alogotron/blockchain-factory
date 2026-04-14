import { createAztecNodeClient, waitForNode } from '@aztec/aztec.js/node';

const NODE_URL = 'https://aztec-mainnet.drpc.org';

async function main() {
  console.log('Connecting to Aztec mainnet...');
  console.log('Node:', NODE_URL);

  const node = createAztecNodeClient(NODE_URL);

  try {
    console.log('Waiting for node...');
    await waitForNode(node);

    const nodeInfo = await node.getNodeInfo();
    console.log('\n=== Node Info ===');
    console.log(JSON.stringify(nodeInfo, null, 2));

    const blockNumber = await node.getBlockNumber();
    console.log('\nCurrent block:', blockNumber);

    console.log('\n✅ Connected to Aztec mainnet!');
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
