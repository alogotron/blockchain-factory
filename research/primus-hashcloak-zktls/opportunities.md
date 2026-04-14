# Primus + HashCloak zkTLS — Opportunities & Gaps

**Research Date:** 2026-04-09  
**Repo:** https://github.com/primus-labs/zktls-verification-noir  

---

## Gaps — What's Missing

### Technical Gaps

1. **Hardcoded array sizes in `verify_attestation_hashing`**  
   The function signature fixes `request_urls: [BoundedVec; 2]` and `allowed_urls: [BoundedVec; 3]` — not fully generic like the commitment version.  
   → Contribution: make it fully parameterized with const generics (like `verify_attestation_comm` already does)

2. **No ZK-native JSON parsing inside circuits**  
   Currently, JSON parsing is done off-chain in `att_verifier_parsing` TypeScript. Inside the Noir circuit, the `contents` are treated as raw byte arrays.  
   → HashCloak's own `noir_json_parser` (v0.4.1-hc.5) exists and supports vectors — integrate it for in-circuit JSON field extraction

3. **No unit tests for `att_verifier_lib`**  
   Only E2E tests exist in `example/js_test/`. The Noir library itself has no `#[test]` annotated circuit tests.  
   → Add Nargo unit tests for edge cases: wrong signature, URL not in allowlist, hash mismatch, padding

4. **No multi-attestor or aggregated proofs**  
   Each attestation is verified independently. No way to batch-verify 5 attestations from different endpoints in a single tx.  
   → Recursive proof aggregation using Aztec's recursive verification primitives

5. **No proof of NON-membership**  
   Can prove "I have X" but not "I do NOT have X" (e.g., not on sanctions list).  
   → Requires commitment + ZK set membership circuits

6. **Circuit size is large (~280K constraints)**  
   secp256k1 ECDSA is expensive in Noir. Limited optimization done.  
   → Profile and optimize with Aztec's CHONK prover; explore using Grumpkin-native signatures

7. **Aztec version is RC**  
   `4.2.0-aztecnr-rc.2` — not stable. API will change with Aztec v5 (expected July 2026).  
   → Track stable release, maintain upgrade branch

8. **No npm/yarn package published**  
   `aztec-attestation-sdk` and `att_verifier_parsing` are source-only — no registry package.  
   → Publish to npm; add CI/CD for automated versioned releases

9. **Only `proxytls` and `mpctls` modes**  
   No support for TLSN (TLS Notary) proofs or other zkTLS standards as input format.  
   → Adapter layer for other attestation formats

10. **No mainnet deployment or attestor registry**  
    The Primus attestor public key is hardcoded/passed at deployment. No on-chain registry of trusted attestors.  
    → Multi-sig attestor registry contract; governance for adding/removing attestors

---

## Use Case Gaps (Low-hanging fruit for new examples)

Only GitHub contributors and OKX trading pairs are implemented. Massive surface area:

| Data Source | What to Verify | Mode |
|------------|----------------|------|
| Twitter/X API | Follower count, account age | Hash |
| LinkedIn API | Job title, employer | Commitment |
| Stripe/PayPal | Payment history, revenue band | Commitment |
| CoinGecko/DeFiLlama | Token price at time T | Hash |
| OpenSea | NFT ownership at block N | Hash |
| Reddit | Karma score, subreddit membership | Hash |
| Discord | Server membership, role | Hash |
| Farcaster API | Fid, follower count | Hash |
| Any REST API | Any JSON field | Either |

---

## Contribution Opportunities (Ranked by Impact)

### High Impact

**A. New example: Farcaster / social identity verifier**  
- Fork `contract_template`, attest Farcaster profile data via Primus DVC  
- Enables private social-proof gating on Aztec (only people with >1000 followers can participate)  
- Contributes to both Primus and Aztec ecosystems, highly visible  
- Effort: 2-3 days  

**B. Generalize `verify_attestation_hashing` const generics**  
- Remove hardcoded `[2]`/`[3]` array sizes  
- Makes library usable for APIs with 1, 3, 4+ response fields  
- Clean PR, likely merged  
- Effort: 1 day  

**C. In-circuit JSON parsing via `noir_json_parser`**  
- Integrate `hashcloak/noir_json_parser` into `att_verifier_lib`  
- Allow verifying a specific JSON key inside the ZK circuit (not just hashing the whole plaintext)  
- Significantly more expressive — can verify `$.user.verified == true` inside ZK  
- Effort: 3-5 days  

**D. Aztec v5 upgrade branch**  
- Track Aztec stable release (v5 expected July 2026)  
- Maintain compatibility branch  
- Very useful for ecosystem, shows long-term commitment  
- Effort: 1-2 days when v5 drops  

### Medium Impact

**E. Add Noir unit tests for `att_verifier_lib`**  
- Write `#[test]` functions in `lib.nr` for all verification paths  
- Good engineering hygiene, makes repo more trustworthy  
- Effort: 1-2 days  

**F. Publish npm packages**  
- Publish `aztec-attestation-sdk` and `att_verifier_parsing` to npm  
- Create GitHub Actions CI for automated versioned releases  
- Dramatically improves DX for integrators  
- Effort: 1 day  

**G. Benchmarking + optimization report**  
- Profile circuit gate counts by component (ECDSA vs SHA256 vs URL matching)  
- Identify optimization targets, open issue or PR with findings  
- Effort: 1 day  

**H. Multi-attestor registry contract**  
- Deploy a public registry contract on Aztec Sepolia  
- Admin-governed list of trusted Primus attestor public keys  
- Contracts consume from registry instead of hardcoding  
- Effort: 2-3 days  

### Lower Impact / Longer Term

**I. Recursive aggregation for batch attestations**  
- Verify N attestations in a single tx using Aztec recursive proofs  
- Complex but highly valuable for multi-step identity systems  
- Effort: 1-2 weeks  

**J. ZK set membership / non-membership proofs**  
- Prove a verified field is NOT in a banned set (sanctions, blocklists)  
- Requires Sparse Merkle Tree or similar in Noir  
- Effort: 1-2 weeks  

---

## Integration Ideas for Blockchain Factory

### Quick wins
- Attest Aztec wallet → GitHub account link (prove alogotron GitHub is the deployer)
- Attest Farcaster or X account ownership → use in contract gating
- Build a 'zkTLS proof of human' demo: prove you have a real GitHub/Twitter without revealing identity

### Longer arcs
- Privacy-preserving airdrop gate: prove GitHub stars > 100 on any repo, receive tokens
- zkTLS-gated Noir contract: only verified contributors can call admin functions
- Cross-chain identity bridge: Aztec attestation → Base contract via message passing

---

## Contact / Engagement

- Primary dev: `@ewynx` on GitHub (HashCloak team)
- HashCloak Twitter: @hashcloak (posted tutorial ~recent)
- Primus Labs Twitter: @primus_labs
- Open issues: 0 — team is receptive, low volume repo
- Good PR targets: const generic fix, new examples, unit tests
- Aztec grants program active — zkTLS tooling is exactly what Aztec wants
