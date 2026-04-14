# Shutter Champions: Melee 1 — Application Draft

**Forum post target:** https://shutternetwork.discourse.group/c/shutter-champions/melee-1/21  
**Template reference:** https://shutternetwork.discourse.group/t/shutter-champions-melee-1-application-template/814  
**Deadline:** May 4, 2026

---

## 1. Applicant Information

**Applicant Name:** alogotron  
**Applying for:** Myself

---

## 2. Contributor Information

**Contributor Name:** alogotron  
**GitHub:** https://github.com/alogotron  
**Wallet Address:** *(Alpha wallet — to be filled before posting)*

---

## 3. Contribution Category

**Primary:** dApp Developer

---

## 4. Contribution Details

**Title:** Shutter + zkTLS: Front-run-proof, Identity-gated Transactions

**Status:** In Progress

**Description:**

This contribution integrates Shutter Network's threshold encryption with Aztec/zkTLS identity proofs to produce a novel privacy primitive: **transactions that are simultaneously front-run-proof AND identity-gated**.

The flow:
1. A user proves an offchain condition via zkTLS (e.g. "I am a verified GitHub contributor" or "ETH price is below threshold") — using Noir circuits already built on Aztec
2. That claim is bundled into a transaction payload and **encrypted via Shutter** before submission
3. Validators/searchers cannot read or front-run the payload
4. After block inclusion, Keypers release the decryption key and the condition is verified onchain

This is a genuine intersection of two independent privacy protocols — Shutter's MEV-protection and Aztec's zkTLS identity layer — neither of which has been combined before.

**What's already built:**
- ✅ Working Shutter API + SDK integration in Python (`shutter_crypto.py`) — full encrypt/decrypt cycle verified on Chiado testnet
- ✅ Aztec/Noir zkTLS circuits for GitHub identity, price threshold, contributor gate, proof-of-contributor
- ✅ Proof of onchain activity on Gnosis/Chiado testnet (registration tx hashes available)

**Key Milestones:**
1. **Milestone 1 (complete):** Shutter API integration working on Chiado testnet — register identity, encrypt, wait for keypers, decrypt. Verified with tx hash `0x0e5c8b001ab621a54b0e3f30dc66133f77a06b28055bb6941e107b337fd54b67`
2. **Milestone 2:** Solidity gateway contract that accepts Shutter-encrypted payloads and verifies decrypted zkTLS proofs post-decryption
3. **Milestone 3:** End-to-end demo: encrypt a GitHub identity claim → submit encrypted tx → decrypt after inclusion → verify claim onchain
4. **Milestone 4:** Public GitHub repo with documentation, deployed demo on Chiado testnet

**Impact on Shutter Ecosystem:**
- Demonstrates a new use case for Shutter beyond simple MEV protection: **privacy-preserving conditional execution**
- Shows Shutter's API is developer-accessible for novel dApp patterns
- Produces open-source tooling (Python SDK wrapper) that fixes the Node.js WASM incompatibility in the current npm SDK (`P2_Affine` compressed G2 issue)
- Establishes a cross-protocol integration that could attract zkTLS/Aztec developers to Shutter

**Impact Metrics:**
- GitHub repo stars/forks
- Number of Chiado testnet transactions using the integration
- Developer adoption of the Python SDK wrapper
- Forum/social engagement on the zkTLS+Shutter concept

---

## 5. Links & Supporting Evidence

- **Working Shutter crypto implementation:** https://github.com/alogotron/blockchain-factory/tree/main/scripts/tx/shutter/shutter_crypto.py *(to be pushed)*
- **Aztec zkTLS circuits:** https://github.com/alogotron/blockchain-factory/tree/main/contracts/aztec-zktls *(existing work)*
- **Chiado registration tx:** `0x0e5c8b001ab621a54b0e3f30dc66133f77a06b28055bb6941e107b337fd54b67`
- **Identity registered:** `0x5c0035743aebbb7195604feece4a2ee521fe28db5470998524dc66df46cfe15f`
- **Decryption verified:** message `shutter-spike: identity-gated front-run-proof tx by alogotron` successfully encrypted and decrypted via Chiado API

---

## 6. SHU Funding Request

**Amount requested:** $2,500 USD in SHU

**Justification:**
- ~40h development time (Solidity gateway contract, end-to-end demo, documentation)
- Covers Milestone 2–4 (Milestone 1 already complete as proof of capability)
- Funding on milestone completion: contract deployed + demo live + repo public

---

## 7. Additional Information

**Previous contributions to Shutter:** None prior — this is a first-time contribution building on top of the Shutter API.

**Related prior work:**
- Aztec zkTLS circuits (GitHub identity, price threshold, contributor gate) — Noir/Aztec stack
- Plasma Fold ZK circuits (Rust/arkworks)
- BattleChain security research and smart contracts

**Notes:**
- The Python SDK wrapper (`shutter_crypto.py`) will be open-sourced regardless of grant outcome — it fixes a real Node.js WASM bug in the current npm SDK and should be useful to other Shutter developers
- Happy to discuss technical details or demo the working Chiado integration

---

## Pre-post checklist
- [ ] Replace wallet address with Alpha wallet address
- [ ] Push blockchain-factory repo to GitHub (or relevant sub-folder)
- [ ] Update GitHub links above
- [ ] Post to: https://shutternetwork.discourse.group/c/shutter-champions/melee-1/21
