# blockchain-factory

Blockchain infrastructure research, smart contract development, and onchain footprint work by [@alogotron](https://github.com/alogotron).

This repo is a living workspace for exploring protocols, building integrations, and producing real onchain activity across multiple chains and privacy stacks.

---

## Active Projects

### 🔐 Shutter + zkTLS: Front-run-proof Identity-gated Transactions
> `contracts/shutter-zktls-gateway/` · `scripts/tx/shutter/`

Integrates [Shutter Network](https://shutter.network) threshold encryption with [Aztec zkTLS](https://github.com/alogotron/aztec-zktls-contracts) identity proofs.

Transactions are:
- **Encrypted** via Shutter before submission (front-run proof)
- **Identity-gated** via Noir/zkTLS circuits (only valid claimants can succeed)
- **Verified onchain** after Keypers release the decryption key

Status: ✅ Chiado testnet integration working · 🔨 Solidity gateway contract in progress

### 🧪 Aztec zkTLS Circuits
> `contracts/aztec-zktls/`

Noir smart contracts using Primus Labs + HashCloak zkTLS toolkit:
- `01_price-threshold` — CoinGecko price settlement via hash-based attestation
- `02_github-identity` — GitHub identity linking to Aztec addresses
- `03_contributor-gate` — Access control based on GitHub public repo count
- `04_proof-of-contributor` — Anonymous contribution proof via commitments

### ⚗️ Plasma Fold
> `contracts/plasma-fold/`

ZK folding scheme circuits in Rust/arkworks.

### 🔒 BattleChain Targets
> `contracts/battlechain-targets/`

Solidity CTF-style vulnerable contracts for security research.

---

## Scripts

| Path | Description |
|---|---|
| `scripts/tx/shutter/shutter_crypto.py` | Pure Python Shutter BLS12-381 encrypt/decrypt (fixes npm SDK WASM bug) |
| `scripts/tx/aztec/` | Aztec account deployment and footprint scripts |
| `scripts/tx/x402/` | x402 HTTP payment protocol client/server |
| `scripts/monitor/` | Balance and tx monitoring tools |

---

## Chains

- Ethereum Mainnet + Sepolia
- Base Mainnet + Base Sepolia
- Gnosis Chiado (Shutter testnet)
- Aztec Alpha Network
- ChaosChain (chainId 919)

---

## Research

See [`research/`](./research/) for protocol deep-dives and opportunity analyses:
- Shutter Network
- Aztec Alpha
- Execution Market
- Plasma Blind
- Primus/HashCloak zkTLS
