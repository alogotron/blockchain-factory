# PlasmaBlind — Research Overview

**Date:** 2026-04-09  
**Status:** Active R&D (PSE / Ethereum Foundation)  
**Website:** https://www.plasmablind.xyz/  
**Paper:** https://eprint.iacr.org/2026/634  
**PSE Page:** https://pse.dev/projects/plasma-fold  
**Twitter:** @xyz_pierre (Pierre Daix-Moreux)  

---

## What Is It?

PlasmaBlind is a **privacy-preserving, scalable Layer-2 protocol** for Ethereum built at PSE (Privacy & Scaling Explorations), the Ethereum Foundation's ZK research group. It achieves sub-100ms client-side ZK proving **without SNARKs**, using a novel architecture based on **folding schemes and IVC**.

---

## Authors

- **Pierre Daix-Moreux** — Ethereum Foundation (PSE)
- **Chengru Zhang** — University of Hong Kong + Ethereum Foundation

---

## Core Architecture

### The BlindFold / Nova Folding Approach

| Stage | Actor | What Happens |
|---|---|---|
| Client Proof | User device | Generates a **partially folded circuit instance** using blinding property of folding schemes. Sub-100ms on consumer hardware. |
| Wire Transfer | Network | Sends non-succinct folded instance (large blob) to aggregator |
| Aggregation | Server (IVC prover) | Folds all user instances into a **constant-size proof of block validity**. Sub-300ms per-tx. |
| L1 Finality | L1 (Ethereum) | Final compact proof posted to Layer 1 |

### Key Innovation
- Uses the **blinding property** of folding schemes for privacy (no expensive ZK SNARKs client-side)
- Uses the **low accumulation cost** of folding schemes for aggregation efficiency
- Proposes optimization: **shared-input circuit linking** to eliminate non-uniform circuit composition
- No recursive SNARKs, no PCD setups — aggregator is an IVC prover (verifiable, not trusted)

---

## Performance

| Metric | Target |
|---|---|
| Client-side proof time | **< 100ms** (consumer hardware) |
| Aggregator per-tx time | **< 300ms** (consumer hardware) |
| Proof compression | Not yet implemented (SNARKs can be added eventually for L1) |

---

## Tech Stack

- **Folding scheme:** NIFS (Non-Interactive Folding Scheme) — Nova-style
- **IVC:** Used for incremental aggregation of user proofs
- **Circuit model:** R1CS / relaxed R1CS (standard for Nova-based systems)
- **Target L1:** Ethereum (implied by EF affiliation)
- **Hash function:** Configurable (affects proof size)

---

## Relationship to PlasmaFold

PSE's project page lists this as **Plasma Fold** — likely the same project or a closely related predecessor. PlasmaFold paper: https://eprint.iacr.org/2025/1300.pdf

---

## Context from Twitter Discussion

From Pierre's thread (Apr 7, 2026):
- Client sends **partially folded instance** (not a final proof — it's large)
- Server aggregates without needing to trust: it's an IVC prover, work is verifiable
- SNARK compression can still be added eventually for L1 posting
- Main gains: no recursive SNARKs client-side, no PCD setups for aggregation
- Proof size varies by: hash function, txs/block, I/O per tx, constraint optimization

---

## Links

- Paper (ePrint 2026/634): https://eprint.iacr.org/2026/634
- Paper (ePrint 2025/1300 PlasmaFold): https://eprint.iacr.org/2025/1300.pdf
- PSE Project: https://pse.dev/projects/plasma-fold
- IPTF Ethereum writeup: https://iptf.ethereum.org/private-stablecoins-with-plasma/
- Twitter announcement: https://x.com/xyz_pierre/status/2041416160361803817
