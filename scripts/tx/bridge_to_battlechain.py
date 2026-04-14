#!/usr/bin/env python3
"""
Bridge ETH from Sepolia to BattleChain Testnet (Chain ID 627)
via the ZKSync L1 Bridgehub contract using requestL2TransactionDirect.
"""

import os
from web3 import Web3
from eth_account import Account

# Config
SEPOLIA_RPC = 'https://ethereum-sepolia-rpc.publicnode.com'
BRIDGEHUB = '0xcea5c0ade89389dd5fc461f69ccbd812cfb7fbd8'   # Bridgehub on Sepolia
ZK_CHAIN  = '0x564ca3000EfF59D9a647A1B8c871f27236201D1D'   # ZK Chain diamond on Sepolia
BATTLECHAIN_ID = 627
ALPHA_ADDRESS = '0xaAB80bC6B6040aE845cE225181fD72297bA71b13'
PRIVATE_KEY = os.environ['AGENT_ALPHA_PRIVATE_KEY']

# Bridge params
L2_BRIDGE_AMOUNT = Web3.to_wei(0.05, 'ether')
L2_GAS_LIMIT = 300000
L2_GAS_PER_PUBDATA = 800

# Connect
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))
print(f'Connected: {w3.is_connected()}')
print(f'Sepolia block: {w3.eth.block_number}')
balance = w3.eth.get_balance(ALPHA_ADDRESS)
print(f'Alpha balance (Sepolia): {Web3.from_wei(balance, "ether")} ETH')

gas_price = w3.eth.gas_price
print(f'Gas price: {gas_price} wei')

# Get L2 base cost from ZK chain diamond (3-arg version, no chainId)
base_cost_abi = [{
    'inputs': [
        {'name': '_gasPrice', 'type': 'uint256'},
        {'name': '_l2GasLimit', 'type': 'uint256'},
        {'name': '_l2GasPerPubdataByteLimit', 'type': 'uint256'}
    ],
    'name': 'l2TransactionBaseCost',
    'outputs': [{'name': '', 'type': 'uint256'}],
    'stateMutability': 'view',
    'type': 'function'
}]
zk_contract = w3.eth.contract(address=Web3.to_checksum_address(ZK_CHAIN), abi=base_cost_abi)
base_cost = zk_contract.functions.l2TransactionBaseCost(gas_price, L2_GAS_LIMIT, L2_GAS_PER_PUBDATA).call()
print(f'L2 base cost: {base_cost} wei ({Web3.from_wei(base_cost, "ether")} ETH)')

mint_value = base_cost + L2_BRIDGE_AMOUNT
print(f'Total ETH (mintValue): {Web3.from_wei(mint_value, "ether")} ETH')

# Bridgehub requestL2TransactionDirect ABI
# struct L2TransactionRequestDirect {
#   uint256 chainId; uint256 mintValue; address l2Contract;
#   uint256 l2Value; bytes l2Calldata; uint256 l2GasLimit;
#   uint256 l2GasPerPubdataByteLimit; bytes[] factoryDeps; address refundRecipient;
# }
bridgehub_abi = [
    {
        'inputs': [{
            'components': [
                {'name': 'chainId',                  'type': 'uint256'},
                {'name': 'mintValue',                'type': 'uint256'},
                {'name': 'l2Contract',               'type': 'address'},
                {'name': 'l2Value',                  'type': 'uint256'},
                {'name': 'l2Calldata',               'type': 'bytes'},
                {'name': 'l2GasLimit',               'type': 'uint256'},
                {'name': 'l2GasPerPubdataByteLimit', 'type': 'uint256'},
                {'name': 'factoryDeps',              'type': 'bytes[]'},
                {'name': 'refundRecipient',           'type': 'address'}
            ],
            'name': 'transaction',
            'type': 'tuple'
        }],
        'name': 'requestL2TransactionDirect',
        'outputs': [{'name': 'canonicalTxHash', 'type': 'bytes32'}],
        'stateMutability': 'payable',
        'type': 'function'
    }
]

bridgehub = w3.eth.contract(address=Web3.to_checksum_address(BRIDGEHUB), abi=bridgehub_abi)

nonce = w3.eth.get_transaction_count(ALPHA_ADDRESS)
tx = bridgehub.functions.requestL2TransactionDirect((
    BATTLECHAIN_ID,           # chainId
    mint_value,               # mintValue
    ALPHA_ADDRESS,            # l2Contract (recipient on L2)
    L2_BRIDGE_AMOUNT,         # l2Value
    b'',                      # l2Calldata
    L2_GAS_LIMIT,             # l2GasLimit
    L2_GAS_PER_PUBDATA,       # l2GasPerPubdataByteLimit
    [],                       # factoryDeps
    ALPHA_ADDRESS             # refundRecipient
)).build_transaction({
    'from': ALPHA_ADDRESS,
    'value': mint_value,
    'gas': 250000,
    'gasPrice': int(gas_price * 1.2),
    'nonce': nonce,
    'chainId': 11155111
})

print(f'\nSending bridge tx via Bridgehub...')
account = Account.from_key(PRIVATE_KEY)
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f'Tx hash: 0x{tx_hash.hex()}')
print(f'Sepolia explorer: https://sepolia.etherscan.io/tx/0x{tx_hash.hex()}')

print('Waiting for confirmation...')
receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
print(f'Status: {"SUCCESS" if receipt.status == 1 else "FAILED"}')
print(f'Gas used: {receipt.gasUsed}')
print(f'Block: {receipt.blockNumber}')
