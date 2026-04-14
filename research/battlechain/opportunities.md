# BattleChain — Contribution & Footprint Opportunities

**Updated:** 2026-04-07  
**Priority:** 🔴 High | 🟡 Medium | 🟢 Low / exploratory

---

## 🔴 1. Whitehat Attacker (On-chain footprint + potential earnings)

**What:** Bridge ETH to BattleChain testnet and attack deployed contracts in Attack Mode. Keep 10% of successfully exploited funds.

**Why:** Direct on-chain activity, real security credibility, potential earnings on mainnet.

**How:**
1. Get Sepolia ETH from Google Cloud faucet
2. Bridge via https://portal.battlechain.com/bridge (Sepolia → BattleChain Testnet, Chain ID 627)
3. Monitor contracts entering Attack Mode on explorer
4. Craft exploits using Foundry, submit on-chain
5. Keep 10%, return 90% to recovery address

**Tools:** Foundry, our Alpha wallet, BattleChain RPC (`https://testnet.battlechain.com`)

---

## 🔴 2. Deploy Intentionally Vulnerable Contracts (Platform stress testing)

**What:** Deploy vulnerable Solidity contracts to BattleChain, create Safe Harbor agreements, request Attack Mode — invite the community to find bugs.

**Why:** GitHub footprint (contracts pushed to alogotron), on-chain footprint, community engagement. Cyfrin explicitly asks for this during testnet.

**Ideas for vulnerable contracts:**
- Classic reentrancy vault
- Flash loan manipulation target
- Integer overflow ERC20
- Sandwich attack DEX
- Improper access control ownable

**How:**
1. Write contracts in `contracts/battlechain-targets/src/`
2. Use Foundry to deploy to Chain ID 627
3. Create on-chain Safe Harbor agreement
4. Call `MockRegistryModerator` (`0x1bC64E6F187a47D136106784f4E9182801535BD3`) to request Attack Mode
5. Push contracts to GitHub repo under alogotron

---

## 🔴 3. AI Agent Attacker (Our strongest angle)

**What:** Use Agent Zero as a BattleBot — autonomously scan contracts in Attack Mode, write exploit code, execute on-chain.

**Why:** BattleChain is explicitly AI-native. They're building BattleBot but it's not live yet — we can build our own version now. This is a massive first-mover opportunity.

**How:**
1. Load `docs.battlechain.com/llms-full.txt` into context
2. Install cyfrin/solskill: `npx skills add cyfrin/solskill`
3. Monitor explorer for contracts in Attack Mode
4. Use subordinate developer agent to analyze contract bytecode/source
5. Generate exploit scripts with Foundry
6. Execute with our wallets
7. Document the process → publish as GitHub repo `battlebot-agent`

**GitHub opportunity:** Open source our attack agent as `alogotron/battlebot-agent` — could get traction since Cyfrin is building toward this anyway.

---

## 🟡 4. Prediction Market Contracts (Open design space)

**What:** Build prediction market contracts for BattleChain attack periods. Cyfrin explicitly invites community to design/deploy this.

**Why:** Roadmap item they haven't shipped yet. Being early = recognition, potential integration into official stack.

**Design:**
- Market: "Will [protocol X] survive its 7-day attack window?"
- Participants stake ETH on yes/no
- Resolved by on-chain contract state (Attack Mode → Production Mode transition)
- Oracle: BattleChain's own state tracking

**How:**
1. Design spec in `contracts/battlechain-prediction/`
2. Build in Solidity + Foundry
3. Deploy to BattleChain testnet
4. Open GitHub PR or Discord post to Cyfrin team

---

## 🟡 5. Open Source Doc Contributions (GitHub footprint)

**What:** PR to https://github.com/Cyfrin/docs-battlechain — fix typos, add examples, improve AI agent integration guides.

**Why:** Easy footprint on a high-visibility repo. Cyfrin explicitly asks for PRs.

**Ideas:**
- Add an `AGENTS.md` example template for AI-native deployment
- Add a `foundry.toml` snippet for BattleChain network config
- Write a guide for using Agent Zero / autonomous agents with BattleChain
- Fix or expand Safe Harbor explanation

---

## 🟡 6. battlechain-contracts Contributions (MIT license, open PRs)

**What:** Code contributions to https://github.com/Cyfrin/battlechain-contracts

**Ideas:**
- Add test coverage for edge cases
- Add scripts/helpers for common workflows
- Add Foundry deployment scripts for quick setup

---

## 🟢 7. CodeHawks Competitive Audits

**What:** Participate in competitive audit contests on https://codehawks.cyfrin.io

**Why:** GitHub + on-chain footprint, security credibility, USDC earnings.

**How:** Browse active contests, submit findings, earn from pool.

---

## 🟢 8. Monitoring & Tooling

**What:** Build a BattleChain monitor that alerts when contracts enter Attack Mode.

**How:**
- Poll BattleChain RPC for state-change events
- Script in `scripts/monitor/battlechain_watch.py`
- Alert via notification when a juicy contract goes live for attack

**GitHub:** Publish as `alogotron/battlechain-monitor`

---

## Quick Start Actions (Do First)

| # | Action | Wallet | Est. Time |
|---|---|---|---|
| 1 | Get Sepolia ETH from Google Cloud faucet | Alpha | 5 min |
| 2 | Bridge Sepolia ETH to BattleChain (Chain 627) | Alpha | 10 min |
| 3 | Deploy a simple vulnerable contract | Alpha | 30 min |
| 4 | Install cyfrin/solskill | — | 5 min |
| 5 | Load llms-full.txt, scan for Attack Mode contracts | — | ongoing |
| 6 | Open first PR on docs-battlechain repo | — | 30 min |
