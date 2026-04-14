# Payy Network — Opportunities

> Last updated: 2026-04-07

---

## 🎯 Testnet Participation

### Priority: HIGH

Testnet is live NOW (April 2026). This is early-mover territory.

**Actions:**
- [ ] Install `@payy/viem` and extract RPC/chainId
- [ ] Request testnet access via hello@payy.link
- [ ] Deploy contracts to testnet using Foundry
- [ ] Run private ERC-20 transfers (zero fee)
- [ ] Test PrivacyBridge interaction
- [ ] Document all transactions for onchain footprint

---

## 💡 Integration Ideas

### 1. Privacy-native DEX or Swap
Build a simple private token swap on Payy using the predeployed contracts. Combines PrivacyBridge + zero-fee transfers.

### 2. Private Payroll / Disbursement Contract
Deploy a Solidity contract that splits PUSD among multiple recipients privately — real enterprise use case.

### 3. PUSD Faucet / Dispenser
Build a testnet faucet contract for PUSD (`0x0200...`) — useful for the community, good footprint.

### 4. Private Multisig
Adapt Safe/Gnosis multisig pattern to work with Payy's privacy layer. High-value concept.

### 5. Cross-chain Privacy Bridge
Use the PrivacyBridge contract (`0x3100...`) to move assets from Ethereum → Payy privately.

---

## 🐙 GitHub Footprint Angles

- Fork `polybase/payy` and contribute fixes or documentation
- Create a `payy-testnet-starter` repo: viem + Foundry boilerplate for Payy Network
- Write a guide: "How to deploy contracts to Payy testnet"
- Open issues on their GitHub for missing docs (chainId, RPC, faucet)

---

## 🪂 Potential Airdrop Angles

- Native PAYY token is planned (CEO declined timeline but confirmed)
- Early testnet activity = strong airdrop signal, especially with only ~12 initial design partners
- Multiple wallet addresses active on testnet = stronger footprint
- Deploying contracts = developer-tier activity (highest value for potential airdrop)

**Wallets to activate on testnet:** Alpha, Beta, Gamma, Delta

---

## 📊 Competitive Context

| Project | Privacy Approach | Status |
|---|---|---|
| Payy | ZK privacy pools + EVM L2 | Testnet live |
| Aztec | Full ZK L2 | Testnet |
| Tornado Cash | Mixer (OFAC sanctioned) | Dead |
| Railgun | ZK private balances | Mainnet |
| Nocturne | ZK stealth accounts | Shutdown |

Payy has a unique angle: **privacy by default, EVM compatible, no wallet changes needed**. This is the most approachable privacy L2 for builders.

---

## ⚡ Next Steps

1. Install `@payy/viem` to get actual chainId + RPC endpoint
2. Add Payy testnet to MetaMask/wallet config
3. Request testnet tokens
4. Run first transactions with Alpha wallet
5. Deploy a simple contract (PUSD dispenser or private transfer tester)
6. Log all activity to `logs/`
