# Payy Network — Research Overview

> Last updated: 2026-04-07

---

## What Is Payy Network?

Payy Network is a **privacy-first Ethereum Layer 2** blockchain that makes stablecoin transactions private by default. It uses high-performance **Zero-Knowledge (ZK) proofs** combined with full EVM compatibility — meaning existing contracts and wallets work without modification.

Founded by **Sid Gandhi** and **Calum Moore**, who pivoted from their previous project **Polybase** in 2023. Headquartered in New York City.

---

## Funding

| Round | Amount | Lead Investor | Date |
|---|---|---|---|
| Seed | $6M | FirstMark Capital | March 2026 |
| **Total raised** | **$8M** | — | — |

---

## Technology Stack

### Privacy Architecture
- **Default privacy pools**: Every ERC-20 token automatically gets its own privacy pool
- **Private EVM**: Private smart contracts that compile to standard EVM bytecode
- **ZK proof system**: Shields sender identity, receiver identity, amounts, and asset types
- **Private data storage**: Users own and control where their data is stored
- **RPC upgrade**: The RPC node automatically adds ZK proofs to `eth_sendRawTransaction` calls — no wallet changes needed

### Performance
| Metric | Value |
|---|---|
| Block time | 300ms (deterministic finality) |
| Throughput | 10k TPS initially, up to 100k TPS |
| ERC-20 transfer fee | $0 (zero gas for private transfers) |
| Gas tokens | PUSD, PAYY |
| Countries covered | 100+ |
| Total transactions | 10M+ |

### EVM Compatibility
- Works with MetaMask, Phantom, and all existing wallets
- No changes required to existing contracts
- viem integration via `@payy/viem/chains`

---

## Predeployed Contracts

| Contract | Address |
|---|---|
| PUSD | `0x0200000000000000000000000000000000000000` |
| PrivacyBridge | `0x3100000000000000000000000000000000000000` |
| Poseidon | `0x3300000000000000000000000000000000000000` |
| Rollup | `0x3200000000000000000000000000000000000000` |
| BlockTimestampMs | `0x3400000000000000000000000000000000000000` |
| TransactionBridge | `0x3000000000000000000000000000000000000000` |
| PrivacyVaultRegistry | TBC |
| Multicall3 | TBC |
| Permit2 | TBC |

---

## Product Timeline

| Date | Milestone |
|---|---|
| Jan 2024 | Payy Wallet launched (self-custodial, non-custodial) |
| Aug 2025 | Payy Visa Card launched (spend USDC anywhere Visa is accepted) |
| Feb 2026 | Payy Network L2 announced |
| Mar 2026 | $6M seed + private testnet live (~12 design partners) |
| **Apr 2026** | **Public testnet launched (Privy integration)** ← WE ARE HERE |
| Summer 2026 | Mainnet targeted |
| TBD | Native PAYY token launch |

---

## Testnet Status (April 2026)

- **Status**: Live — Sid Gandhi tweeted: *"PAYY NETWORK TESTNET LIVE WITH PRIVY"*
- **Previous status**: Invite-only with ~12 design partners
- **Current access**: Via Privy embedded wallet integration (public)
- **Faucet**: Not publicly documented yet
- **ChainId / RPC**: Not yet published publicly — imported via `@payy/viem/chains`
- **Contact for access**: hello@payy.link

### How to Integrate (from docs)
```js
import { createWalletClient, http } from "viem";
import { payy } from "@payy/viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const account = privateKeyToAccount(process.env.PRIVATE_KEY);
const walletClient = createWalletClient({
  account,
  chain: payy,
  transport: http(process.env.RPC_URL)
});

// Send private zero-fee ERC-20 transfer
await walletClient.sendTransaction({
  to: "0xRecipient",
  value: parseEther("0.01")
});
```

---

## Key Links

| Resource | URL |
|---|---|
| Website | https://payy.network |
| Docs | https://docs.payy.network |
| GitHub | https://github.com/polybase/payy |
| Twitter/X | https://x.com/payy_link |
| CEO Twitter | https://x.com/sidgandhi_xyz |
| Contact | hello@payy.link |

---

## Backed By
- FirstMark Capital (lead)
- Ethereum Foundation (Ethereum tweeted about Payy with endorsement)
