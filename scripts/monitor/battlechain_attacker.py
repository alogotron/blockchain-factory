#!/usr/bin/env python3
"""
battlechain_attacker.py — BattleChain Attack Mode Monitor & Opportunity Scanner

Scans BattleChain for contracts in Attack Mode, checks their balances,
logs opportunities, and alerts when profitable targets appear.

Usage:
    python3 battlechain_attacker.py [--once] [--interval 60]
"""

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from web3 import Web3

# ─── Config ───────────────────────────────────────────────────────────────────

BC_RPC      = 'https://testnet.battlechain.com'
BC_EXPLORER = 'https://block-explorer-api.testnet.battlechain.com/api'
BC_CHAIN_ID = 627

ATTACK_REGISTRY    = '0xdD029a6374095EEb4c47a2364Ce1D0f47f007350'
SAFE_HARBOR_REG    = '0x0A652e265336a0296816ac4D8400880E3e537c24'
AGREEMENT_FACTORY  = '0x2BEe2970f10FDc2aeA28662Bb6f6a501278eBd46'
BC_DEPLOYER        = '0x74269804941119554460956f16Fe82Fbe4B90448'
MOCK_MODERATOR     = '0x1bC64E6F187a47D136106784f4E9182801535BD3'

# Our wallets (recovery address)
ALPHA_ADDR = '0xaAB80bC6B6040aE845cE225181fD72297bA71b13'

LOGS_DIR   = Path(__file__).parent.parent.parent / 'logs'

# ─── Web3 setup ───────────────────────────────────────────────────────────────

w3 = Web3(Web3.HTTPProvider(BC_RPC, request_kwargs={'timeout': 20}))

# ─── Helpers ──────────────────────────────────────────────────────────────────

def log(msg: str):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f'[{ts}] {msg}')

def explorer_get(params: dict) -> dict:
    try:
        r = requests.get(BC_EXPLORER, params=params, timeout=15)
        return r.json()
    except Exception as e:
        return {'status': '0', 'message': str(e)}

def get_contract_balance_eth(addr: str) -> float:
    try:
        bal = w3.eth.get_balance(Web3.to_checksum_address(addr))
        return float(w3.from_wei(bal, 'ether'))
    except:
        return 0.0

def get_verified_contracts(page: int = 1, limit: int = 25) -> list:
    """Fetch verified contracts from BattleChain explorer."""
    d = explorer_get({
        'module': 'contract',
        'action': 'listverifiedcontracts',
        'page': page,
        'offset': limit,
        'sort': 'desc'
    })
    if d.get('status') == '1' and isinstance(d.get('result'), list):
        return d['result']
    return []

def get_recent_contracts(page: int = 1) -> list:
    """Fetch recently deployed contracts via account txs to BattleChainDeployer."""
    d = explorer_get({
        'module': 'account',
        'action': 'txlist',
        'address': BC_DEPLOYER,
        'sort': 'desc',
        'page': page,
        'offset': 20
    })
    if d.get('status') == '1' and isinstance(d.get('result'), list):
        return d['result']
    return []

def get_attacker_txs_from_registry() -> list:
    """Get recent txs to AttackRegistry (requestUnderAttack calls)."""
    d = explorer_get({
        'module': 'account',
        'action': 'txlist',
        'address': ATTACK_REGISTRY,
        'sort': 'desc',
        'page': 1,
        'offset': 20
    })
    if d.get('status') == '1' and isinstance(d.get('result'), list):
        return d['result']
    return []

def scan_attack_mode_targets() -> list:
    """Find contracts that have requested Attack Mode."""
    targets = []
    txs = get_attacker_txs_from_registry()
    
    for tx in txs:
        if tx.get('isError') == '1':
            continue
        method_id = tx.get('input', '')[:10]
        # requestUnderAttack(address) = 0x...
        # We look for any successful call to AttackRegistry
        from_addr = tx.get('from', '')
        timestamp = int(tx.get('timeStamp', 0))
        age_hours = (time.time() - timestamp) / 3600
        
        if from_addr.lower() != ALPHA_ADDR.lower():  # Not our own deployment
            targets.append({
                'deployer': from_addr,
                'tx_hash': tx.get('hash', ''),
                'age_hours': round(age_hours, 1),
                'block': tx.get('blockNumber', '?')
            })
    
    return targets

def check_network_stats() -> dict:
    """Get basic BattleChain network stats."""
    try:
        block = w3.eth.block_number
        alpha_bal = get_contract_balance_eth(ALPHA_ADDR)
        deployer_bal = get_contract_balance_eth(BC_DEPLOYER)
        return {
            'block': block,
            'alpha_balance_eth': alpha_bal,
            'bc_deployer_balance_eth': deployer_bal
        }
    except Exception as e:
        return {'error': str(e)}

def scan_funded_contracts() -> list:
    """Find contracts deployed via BattleChainDeployer that have ETH balance."""
    funded = []
    txs = get_recent_contracts()
    
    seen = set()
    for tx in txs:
        if tx.get('isError') == '1':
            continue
        # Contract address is in the 'contractAddress' field or derived from input
        contract_addr = tx.get('to', '')  # Deployer receives the call
        from_addr = tx.get('from', '')
        tx_hash = tx.get('hash', '')
        
        if tx_hash in seen:
            continue
        seen.add(tx_hash)
        
        # Look for contracts created from deployer txs
        # Parse the internal txs to find created contracts
        d = explorer_get({
            'module': 'account',
            'action': 'txlistinternal',
            'txhash': tx_hash,
            'page': 1,
            'offset': 10
        })
        
        if d.get('status') == '1' and isinstance(d.get('result'), list):
            for internal_tx in d['result']:
                created = internal_tx.get('contractAddress', '')
                if created and created not in seen:
                    seen.add(created)
                    bal = get_contract_balance_eth(created)
                    if bal > 0:
                        funded.append({
                            'address': created,
                            'balance_eth': bal,
                            'bounty_10pct_eth': round(bal * 0.1, 6),
                            'deployer': from_addr,
                            'deploy_tx': tx_hash,
                            'our_contract': from_addr.lower() == ALPHA_ADDR.lower()
                        })
    
    return funded

def save_report(data: dict):
    """Save scan report to logs."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    log_dir = LOGS_DIR / today
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / 'battlechain_scan.json'
    
    # Append to existing or create new
    history = []
    if path.exists():
        try:
            history = json.loads(path.read_text())
        except:
            history = []
    history.append(data)
    path.write_text(json.dumps(history, indent=2))
    return path

def run_scan():
    """Run one complete scan cycle."""
    log('=== BattleChain Attack Monitor Scan ===')
    
    # Network stats
    stats = check_network_stats()
    log(f"Block: {stats.get('block', '?')} | Alpha: {stats.get('alpha_balance_eth', '?')} ETH")
    
    # Attack Mode targets (from AttackRegistry)
    log('Scanning AttackRegistry for recent requestUnderAttack txs...')
    attack_targets = scan_attack_mode_targets()
    
    if attack_targets:
        log(f'Found {len(attack_targets)} Attack Mode registrations (excluding ours):')
        for t in attack_targets:
            log(f"  Deployer: {t['deployer']} | TX: {t['tx_hash'][:16]}... | Age: {t['age_hours']}h")
    else:
        log('No external Attack Mode targets found in recent txs')
    
    # Funded contracts
    log('Scanning for funded contracts deployed via BattleChainDeployer...')
    funded = scan_funded_contracts()
    
    opportunities = []
    for c in funded:
        status = '🟢 OUR TARGET' if c['our_contract'] else '🔴 ATTACK OPPORTUNITY'
        log(f"{status}: {c['address']} | {c['balance_eth']} ETH (bounty: {c['bounty_10pct_eth']} ETH)")
        if not c['our_contract'] and c['balance_eth'] > 0.001:
            opportunities.append(c)
    
    if opportunities:
        log(f'\n🎯 {len(opportunities)} EXTERNAL ATTACK OPPORTUNITIES FOUND!')
        for opp in opportunities:
            log(f"  Target: {opp['address']}")
            log(f"  Balance: {opp['balance_eth']} ETH")
            log(f"  Bounty (10%): {opp['bounty_10pct_eth']} ETH")
            log(f"  Explorer: https://explorer.testnet.battlechain.com/address/{opp['address']}")
    else:
        log('No external attack opportunities detected this scan')
    
    # Save report
    report = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'block': stats.get('block'),
        'alpha_balance_eth': stats.get('alpha_balance_eth'),
        'attack_targets_found': len(attack_targets),
        'funded_contracts': funded,
        'external_opportunities': opportunities
    }
    path = save_report(report)
    log(f'Report saved to {path}')
    log('=== Scan complete ===')
    return opportunities

def main():
    parser = argparse.ArgumentParser(description='BattleChain Attack Mode Monitor')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--interval', type=int, default=300, help='Scan interval in seconds (default: 300)')
    args = parser.parse_args()
    
    log('BattleChain Attack Monitor starting...')
    log(f'RPC: {BC_RPC}')
    log(f'Alpha wallet: {ALPHA_ADDR}')
    
    if args.once:
        run_scan()
    else:
        log(f'Running every {args.interval}s. Press Ctrl+C to stop.')
        while True:
            try:
                run_scan()
                log(f'Next scan in {args.interval}s...')
                time.sleep(args.interval)
            except KeyboardInterrupt:
                log('Stopped by user')
                break
            except Exception as e:
                log(f'Scan error: {e}')
                time.sleep(30)

if __name__ == '__main__':
    main()
