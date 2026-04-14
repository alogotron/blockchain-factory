# Aztec Alpha Network — Research Overview

**Researched**: 2026-04-08  
**Status**: Alpha Mainnet LIVE (launched ~March 31, 2026)  
**TGE**: February 11, 2026  
**Website**: https://aztec.network  
**Docs**: https://docs.aztec.network  
**GitHub**: https://github.com/AztecProtocol  
**Forum**: https://forum.aztec.network  

---

## 1. What Is Aztec Alpha

Aztec Alpha is the **first Layer 2 on Ethereum with a full execution environment for private smart contracts**. It is the culmination of years of ZK research, launched following a unanimous community governance vote and running on top of the Aztec Ignition Chain (live since November 2025).

### Key Differentiators

- **Privacy-native by design** — not a bolt-on. The only L2 combining Ethereum programmability with Zcash-level privacy in a single execution environment.
- **Fully decentralized from day one** — Aztec Labs runs zero sequencers and has no governance power. 3,500+ sequencers and 50+ provers across 5 continents with zero downtime since Ignition.
- **No backdoor** — no centralized entity can pause the network, censor txs, or access private data.
- **L1 escape hatch** — user funds always recoverable even if the L2 fails.
- **Compliance-friendly** — selective disclosure controls enable regulated use cases on a private chain.

### Roadmap Phases

| Phase | Status | Criteria |
|-------|--------|----------|
| Ignition | DONE (Nov 2025) | Decentralized block building live on Ethereum mainnet |
| Alpha | LIVE | 1 TPS, ~6s blocks, security audit in progress |
| Beta | Planned | >10 TPS, reduced block times, 99.9% uptime, zero critical bugs for 3 months |
| v5 Release | July 2026 | Package + distribute fixes from Alpha disclosures |

### Alpha Network Stats
- **Throughput**: 1 TPS, ~6-second block times
- **Consensus**: 48-validator re-execution committee; 33/48 required per 72-second checkpoint
- **Sequencers**: 3,500+ active, stake-weighted governance
- **Provers**: 50+ globally distributed
- **Minimum stake** to run sequencer: 200,000 AZTEC

---

## 2. Tech Stack

### Dual State Model

```
Private State (PXE)              Public State (AVM)
─────────────────────            ──────────────────────────
Client-side (browser/phone)      Network-side (Aztec nodes)
Noir smart contracts             Aztec Virtual Machine
Notes + Nullifiers (UTXO)        Public data tree (like EVM)
ZK proofs generated locally      Transparent execution
Data NEVER leaves user device     Ethereum-like public state
```

**Execution is directional**: private functions run first on device → can enqueue public functions → public functions CANNOT call private functions.

### CHONK Proving System
"Client-side Highly Optimized ploNK" — enables ZK proof generation on consumer devices and browsers without specialized hardware. This is what makes client-side privacy practical.

### Key Cryptographic Primitives
- **Notes**: UTXO chunks of private state data
- **Commitments**: Stored in append-only UTXO tree
- **Nullifiers**: Created when notes are spent/deleted, stored in nullifier tree — keeps deletions private
- **Key pairs per account** (3):
  - Nullifier key pair (compute note nullifiers)
  - Incoming viewing key pair (decrypt notes you receive)
  - Outgoing viewing key pair (decrypt notes you send)

### Noir Language

- **Type**: ZK domain-specific language (DSL), Rust-like syntax
- **Purpose**: Write ZK circuits AND smart contracts
- **Reference**: https://noir-lang.org
- **Verifiable**: on-chain or off-chain
- **Note**: Performance requires careful attention — ZK proof intuitions differ from regular program execution. Poorly written private functions can be severely unoptimized.

### Aztec.nr Framework

- Noir library that adds smart contract functionality on top of raw Noir
- Without it: no events, no contract calls, no msg.sender, no addresses, no blockchain access
- Provides: contract/address abstraction, event emission, cross-contract calls, historic state access
- Docs: https://docs.aztec.network/developers/docs/aztec-nr

### Aztec.js SDK

- TypeScript library (equivalent to ethers.js for Aztec)
- Includes the PXE (Private Execution Environment)
- Runs in **Node.js or the browser**
- Handles: account management, contract interaction, proof generation
- Primary interface for all dApp development

### Account Abstraction

Every account IS a smart contract — native account abstraction. Developers can write custom account contracts defining:
- Transaction authorization logic
- Nonce management
- Fee payment mechanisms

---

## 3. Token ($AZTEC)

- **TGE**: February 11, 2026
- **Use cases**:
  - Network fees (pay for proof generation)
  - Staking (sequencers + provers)
  - Governance (AZIPs — Aztec Improvement Proposals)
- **Sequencer threshold**: 200,000 AZTEC minimum stake
- **Governance**: stake defaults to "yea" on signaling-path proposals; must actively re-delegate to oppose
- **Gate Launchpool**: ran Feb 12–22, 2026 (2.587M AZTEC distributed)

---

## 4. Developer Ecosystem

### Core Resources

| Resource | URL | Notes |
|----------|-----|-------|
| Developer Docs | https://docs.aztec.network/developers/overview | Primary reference |
| Noir Docs | https://noir-lang.org/docs/ | Language reference |
| Aztec.nr Docs | https://docs.aztec.network/developers/docs/aztec-nr | Framework reference |
| Aztec Examples | https://github.com/AztecProtocol/aztec-examples | Contract examples repo |
| Aztec Monorepo | https://github.com/AztecProtocol/aztec-packages | Full protocol source |
| Aztec Starter | https://github.com/AztecProtocol/aztec-starter | Getting started repo |
| Awesome Aztec | GitHub search "awesome-aztec" | Community examples |

### Token Standards (delivered by Wonderland team)
- **AIP-20**: Fungible token standard (equivalent to ERC-20)
- **AIP-721**: NFT standard (equivalent to ERC-721)
- Plus: escrow contracts and logic libraries as production-ready primitives

### Tooling
- `aztec` CLI for compiling contracts
- Aztec Language Server (LSP) for IDE support
- Local sandbox for development
- AI tooling resources referenced in docs sidebar
- OpenZeppelin has published a developer guide for safe Noir circuits

### Trivia: First Public Log on Aztec Alpha
Tx `0x199fa3c3a8a7269f88f2cc757ce29d5b7714145f07ae81d56d060abfd5522afd` (block 1395):
> "Wonderland was here. First public log on Aztec Alpha. https://wonderland.xyz"

---

## 5. Governance

- **AZIPs** (Aztec Improvement Proposals) — submitted on GitHub, debated publicly
- Forum: https://forum.aztec.network
- Aztec Foundation runs governance, not Aztec Labs
- Sequencer stake = voting power (delegatable)
- Upgrades follow signaling path → on-chain vote

---

## 6. Competitive Landscape

| Network | Privacy | EVM Compat | Language | Sequencer | Status (2026) |
|---------|---------|------------|----------|-----------|---------------|
| **Aztec** | Native, full | Custom AVM | Noir | Decentralized (3500+) | Alpha Mainnet |
| zkSync Era | None (transparent) | Type 3 | Solidity/zkSync bytecode | Centralized | Mainnet |
| Polygon zkEVM | None | Type 2 | Solidity | Centralized | Mainnet |
| Scroll | None | Type 1 | Solidity | Centralized | Mainnet ($748M TVL) |
| StarkNet | None | Custom VM | Cairo | Centralized | Mainnet |
| Manta | Partial | EVM | Solidity | Centralized | Mainnet |

**Aztec's moat**: Only L2 with programmable privacy. Every other major L2 is fully transparent. The 2026 trend is privacy-readiness — Aztec is years ahead of any competitor on this dimension.

**Aztec's limitations (Alpha)**: 1 TPS only, known bugs not yet disclosed, ~6s block times, Noir learning curve, no EVM compatibility (requires rewriting contracts).

---

## 7. Security

- Active audit process ongoing during Alpha
- Bug bounty program launching as audits progress
- Security policy: https://github.com/AztecProtocol/aztec-packages/blob/next/SECURITY.md
- Known vulnerabilities will be packaged and disclosed at v5 (July 2026)
- Alpha is explicitly a security-in-progress phase — not for production high-value deployments

---

## Sources

- https://aztec.network/blog/announcing-the-alpha-network
- https://docs.aztec.network/developers/overview
- https://aztec.network/blog/introducing-aztec-nr-aztecs-private-smart-contract-framework
- https://noir-lang.org/docs/
- https://forum.aztec.network/t/request-for-grant-proposals-application-state-migration/8298
- https://taikai.network/en/aztecnetwork/hackathons
- https://icodrops.com/aztec/
- https://ventureburn.com/what-is-aztec/
