#!/usr/bin/env python3
"""Register GasChecker on Base Mainnet ERC-8004 Identity Registry"""

from web3 import Web3
import json, base64, os, sys

# ============================================================
# CONFIG
# ============================================================
RPC      = 'https://base-rpc.publicnode.com'
CHAIN_ID = 8453  # Base Mainnet

# Known Base Mainnet ERC-8004 Identity Registry
IDENTITY_REGISTRY = '0x8004A169FB4a3325136EB29fA0ceB6D2e539a432'

ALPHA_ADDR = '0xaAB80bC6B6040aE845cE225181fD72297bA71b13'
ALPHA_KEY  = '0x60a82dd2e459d47bce0ea3f94987a07855b76c8f25bb0fad8a4ff1ecea76ea28'

# ============================================================
# SETUP
# ============================================================
w3 = Web3(Web3.HTTPProvider(RPC, request_kwargs={'headers': {'User-Agent': 'Mozilla/5.0'}}))
assert w3.is_connected(), 'RPC connection failed'
print(f'✅ Connected to Base Mainnet (chain {w3.eth.chain_id})')

ALPHA_ADDR = Web3.to_checksum_address(ALPHA_ADDR)
bal = w3.from_wei(w3.eth.get_balance(ALPHA_ADDR), 'ether')
print(f'💰 Alpha: {ALPHA_ADDR} | Balance: {float(bal):.6f} ETH')

# ============================================================
# ABI - try both setAgentUri and setAgentURI selectors
# ============================================================
ID_ABI = [
    # register with simple string URI
    {"inputs": [{"name": "tokenURI_", "type": "string"}],
     "name": "register", "outputs": [{"name": "agentId", "type": "uint256"}],
     "stateMutability": "nonpayable", "type": "function"},
    # setAgentUri (lowercase) - used in ChaosChain SDK
    {"inputs": [{"name": "agentId", "type": "uint256"}, {"name": "newUri", "type": "string"}],
     "name": "setAgentUri", "outputs": [],
     "stateMutability": "nonpayable", "type": "function"},
    # setAgentURI (uppercase) - used in Sepolia deployed contract
    {"inputs": [{"name": "agentId", "type": "uint256"}, {"name": "newUri", "type": "string"}],
     "name": "setAgentURI", "outputs": [],
     "stateMutability": "nonpayable", "type": "function"},
    # read functions
    {"inputs": [{"name": "tokenId", "type": "uint256"}],
     "name": "tokenURI", "outputs": [{"name": "", "type": "string"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [{"name": "owner", "type": "address"}],
     "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [],
     "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function"},
    # Events
    {"anonymous": False, "inputs": [
        {"indexed": True, "name": "agentId", "type": "uint256"},
        {"indexed": False, "name": "tokenURI", "type": "string"},
        {"indexed": True, "name": "owner", "type": "address"}],
     "name": "Registered", "type": "event"},
]

registry = w3.eth.contract(
    address=Web3.to_checksum_address(IDENTITY_REGISTRY),
    abi=ID_ABI
)

# ============================================================
# CHECK REGISTRY STATE
# ============================================================
try:
    total = registry.functions.totalSupply().call()
    print(f'📊 Registry total agents: {total}')
except Exception as e:
    print(f'⚠️  totalSupply not available: {e}')

try:
    alpha_count = registry.functions.balanceOf(ALPHA_ADDR).call()
    print(f'📊 Alpha already has {alpha_count} agents on Base')
except Exception as e:
    print(f'⚠️  balanceOf error: {e}')

# ============================================================
# LOAD GASCHECKER REGISTRATION JSON
# ============================================================
REG_JSON_PATH = '/a0/usr/projects/chaoschain-8004scan/updated-gaschecker-registration.json'
with open(REG_JSON_PATH) as f:
    reg_data = json.load(f)

print(f'\n📦 Agent: {reg_data["name"]}')
print(f'   Endpoints: {[e["url"][:50]+"..." for e in reg_data.get("endpoints", [])]}')

# Encode as data URI (base64)
json_str = json.dumps(reg_data, separators=(',', ':'))
b64 = base64.b64encode(json_str.encode()).decode()
data_uri = f'data:application/json;base64,{b64}'
print(f'   Data URI length: {len(data_uri)} chars')

# ============================================================
# SEND TRANSACTION
# ============================================================
def send_tx(fn, label, gas=2_000_000):
    nonce = w3.eth.get_transaction_count(ALPHA_ADDR)
    gas_price = max(w3.eth.gas_price, Web3.to_wei(0.001, 'gwei'))
    tx = fn.build_transaction({
        'from': ALPHA_ADDR,
        'nonce': nonce,
        'gas': gas,
        'gasPrice': gas_price,
        'chainId': CHAIN_ID,
    })
    signed = w3.eth.account.sign_transaction(tx, ALPHA_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f'\n🚀 [{label}] TX: {tx_hash.hex()}')
    print(f'   Explorer: https://basescan.org/tx/{tx_hash.hex()}')
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    status = '✅ SUCCESS' if receipt.status == 1 else '❌ FAILED'
    print(f'   {status} | Gas used: {receipt.gasUsed:,} | Block: {receipt.blockNumber}')
    return receipt

print('\n' + '='*60)
print('REGISTERING GasChecker on Base Mainnet')
print('='*60)

try:
    receipt = send_tx(
        registry.functions.register(data_uri),
        'register GasChecker',
        gas=2_000_000
    )
    
    if receipt.status == 1:
        # Extract agent ID from Registered event
        try:
            logs = registry.events.Registered().process_receipt(receipt)
            if logs:
                agent_id = logs[0]['args']['agentId']
                print(f'\n🎉 GasChecker registered!')
                print(f'   Agent ID: #{agent_id}')
                print(f'   Registry: {IDENTITY_REGISTRY}')
                print(f'   Chain: Base Mainnet (8453)')
                print(f'   8004scan: https://8004scan.io/agent/{agent_id}')
                print(f'   daiscan: https://www.daiscan.io/agent/{agent_id}')
        except Exception as e:
            print(f'Event parsing error: {e}')
            print('Check basescan for agent ID')
except Exception as e:
    print(f'❌ Registration failed: {e}')
