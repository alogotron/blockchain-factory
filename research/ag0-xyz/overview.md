# ag0.xyz — Agent0 SDK

**Date researched:** 2026-04-04  
**URL:** https://www.ag0.xyz | **Docs:** https://sdk.ag0.xyz  
**Type:** Official ERC-8004 SDK (Python + TypeScript)  
**By:** Marco De Rossi (marco@ag0.xyz) — also referenced in arXiv paper on agent cryptography

---

## What It Is

Agent0 SDK is the **official implementation of ERC-8004** — the Ethereum standard for AI agent coordination. It provides:

- **Portable identity** — register agents with on-chain identity
- **Discoverable capabilities** — advertise what agents can do
- **Verifiable reputation** — give/receive feedback on-chain

Available in both **Python** and **TypeScript**.

---

## Key Features

| Feature | Details |
|---|---|
| ERC-8004 compliance | Full implementation of identity, reputation, validation registries |
| Python SDK | `pip install agent0-sdk` |
| TypeScript SDK | npm package |
| IPFS integration | Agent card storage via ipfshttpclient |
| Web3 integration | Ethereum interaction via web3.py |
| Account management | eth_account |
| Async HTTP | aiohttp |
| Search | scikit-learn + numpy for agent discovery |

---

## Install

```bash
# Python
pip install agent0-sdk

# Dependencies:
# web3, eth_account, requests, ipfshttpclient, pydantic, python-dotenv, aiohttp, numpy, scikit-learn
```

---

## Quick Start

See: https://sdk.ag0.xyz/3-examples/3-1-quick-start/
- Create agent
- Configure capabilities
- Register on-chain
- Retrieve agent by ID

---

## Relevance to Our Work

- **Direct overlap**: We already work with ERC-8004 (agents #461, #462, #1581 on Sepolia)
- **Our chaoschain-sdk-ts** is a TypeScript ERC-8004 SDK — ag0.xyz is the Python equivalent
- **Integration opportunity**: Use ag0.xyz SDK in Python scripts instead of raw web3 calls
- **Collaboration angle**: Contribute examples to their repo using our existing agents
- **GitHub footprint**: Could contribute Python examples showing ChaosChain + ag0.xyz integration

---

## Action Items
- [ ] Install and test Python SDK against our Sepolia registry
- [ ] Try querying our agents #461, #462, #1581 via ag0.xyz SDK
- [ ] Explore contributing ChaosChain examples to chaoschain-sdk-examples repo
