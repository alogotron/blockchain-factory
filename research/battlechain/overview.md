# BattleChain — Overview

**Source:** https://www.cyfrin.io/blog/announcing-battlechain-testnet  
**Docs:** https://docs.battlechain.com  
**GitHub:** https://github.com/Cyfrin/battlechain-contracts  
**Explorer:** https://explorer.testnet.battlechain.com  
**Date researched:** 2026-04-07  
**Status:** Testnet LIVE

---

## What Is It?

BattleChain is a **pre-mainnet, post-testnet blockchain** by Cyfrin — a "staging environment" for smart contract security that has been missing from Web3. It sits between testnet and mainnet in the deployment lifecycle:

```
Dev → Testnet → BattleChain → Mainnet
```

Protocols deploy audited contracts with **real liquidity**. Whitehats legally attack them under Safe Harbor. Survivors graduate to mainnet.

---

## Why It Exists

- $3.4B lost to hacks in 2025 (Chainalysis)
- 80% of exploited protocols had no audit; 70% of exploits came from *audited* contracts
- Median bug bounty payout: $2K vs median hack: $2.2M (460x gap)
- LLMs produce insecure Solidity 45% of the time
- AI can exploit contracts at $1.22/scan with exploit revenue doubling every 1.3 months

---

## How It Works

1. Protocol deploys audited contracts with real liquidity to BattleChain
2. On-chain Safe Harbor agreement is created (legal whitehat protection)
3. DAO approves contract for **Attack Mode**
4. Whitehats, AI agents, security researchers attack freely
5. Whitehats keep **10%** of exploited funds, return 90% to recovery address
6. Surviving contracts promoted to **Production Mode** → deploy to mainnet

---

## Technical Stack

| Parameter | Value |
|---|---|
| Chain Type | ZKSync-based L2 |
| Testnet Chain ID | 627 |
| Attack Mode Chain ID | 626 |
| RPC URL | https://testnet.battlechain.com |
| Explorer | https://explorer.testnet.battlechain.com |
| Currency | ETH |
| Bridge | https://portal.battlechain.com/bridge (from Sepolia) |
| Faucet path | Get Sepolia ETH (Google Cloud) → bridge to BattleChain |

---

## AI-Native Design

- Add one instruction to `CLAUDE.md` / `.cursor/rules` / `AGENTS.md` → every AI tool auto-deploys to BattleChain first
- Full docs fit in any AI context window: `docs.battlechain.com/llms-full.txt`
- Installable skills: `npx skills add cyfrin/solskill`
- **BattleBot** (coming): AI framework for non-technical users to attack contracts via chat
- **AI Desktop Support** (coming): browser wallet approval for agents without terminal access

---

## Roadmap

- ✅ Testnet LIVE
- 🔜 Prediction markets on attack periods
- 🔜 Prividium (private attack transactions to prevent MEV/frontrunning)
- 🔜 AI Desktop support
- 🔮 Mainnet

---

## Key Contracts (Testnet)

- `MockRegistryModerator`: `0x1bC64E6F187a47D136106784f4E9182801535BD3` — simulates DAO governance for attack mode

---

## Ecosystem Links

- Discord: https://discord.gg/cyfrin
- Docs GitHub: https://github.com/Cyfrin/docs-battlechain
- Contracts GitHub: https://github.com/Cyfrin/battlechain-contracts
- Skills: https://skillsmp.com/skills/cyfrin-solskill-skills-battlechain-skill-md
- CodeHawks (competitive audits): https://codehawks.cyfrin.io
