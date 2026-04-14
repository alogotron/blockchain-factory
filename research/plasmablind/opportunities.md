# PlasmaBlind — Contribution Opportunities

**Updated:** 2026-04-09  
**Repos:** https://github.com/dmpierre/plasma-fold | https://github.com/winderica/plasma-blind  
**Discord:** https://discord.gg/5vv7bk5u5y (@PrivacyEthereum)  
**Twitter:** @PrivacyEthereum  

---

## 🔥 Highest Impact (Immediate Gaps in Repo)

### 1. Write Tests
- The `dmpierre/plasma-fold` repo has an empty `Tests` section in the README
- No tests visible in the repo — a full test suite would be a high-value PR
- Focus: client proving correctness, aggregator folding, NIFS computation, edge cases
- Language: Rust

### 2. Aggregator Benchmarks
- Client benchmarks exist (SHA + Poseidon accumulators, various tx batch sizes)
- Aggregator benchmarks section is present but **completely empty**
- Run aggregator at different load levels, document throughput, memory, latency
- Would directly validate the <300ms/tx claim from the paper

### 3. Documentation & CONTRIBUTING.md
- No contribution guidelines, no CONTRIBUTING.md
- Could write onboarding docs: how to run locally, how to run client prover in WASM/Chrome
- Low barrier, visible, appreciated by PSE teams

---

## 🧪 Technical Contributions

### 4. WASM Client Prover Improvements
- WASM prover already runs in Chrome — optimize bundle size, memory usage
- Add browser demo / playground (interactive proving demo page)
- Improve WASM bindings ergonomics for JS/TS developers

### 5. Sonobe Integration
- PSE's `Sonobe` is the folding library that PlasmaBlind builds on
- Sonobe dev→main merge is in progress (critical milestone)
- Contributing to Sonobe benefits PlasmaBlind directly
- Repo: https://github.com/privacy-scaling-explorations/sonobe

### 6. Alternative Hash Function Benchmarks
- Proof size/speed varies by hash function (Pierre's own words)
- Run systematic benchmarks: SHA vs Poseidon vs others (e.g., Pedersen, Rescue)
- Publish comparative analysis — useful research artifact

---

## 🔬 Research Contributions

### 7. Proof Compression (SNARK on top of IVC)
- Currently unimplemented — Pierre acknowledged it openly
- Research: which SNARK backend fits best as final compression step for L1
- Could be a full paper contribution or implementation PR

### 8. Wormholes v2
- Listed as open research: redesign leveraging beacon chain deposits
- Security goals need re-derivation — good formal methods / cryptography task

### 9. OTP / Stealth Mixers
- One-time programs with garbled circuits + extractable witness encryption
- Very early stage — ideation and research contributions welcome

---

## 🤝 Community & Soft Contributions

| Action | Where |
|---|---|
| Join Discord | https://discord.gg/5vv7bk5u5y |
| Star + watch repos | dmpierre/plasma-fold, winderica/plasma-blind |
| Open issues with questions/bugs | GitHub |
| Write a technical blog post / explainer | Medium / Mirror / HackMD |
| Apply for EF PSE role | https://jobs.ashbyhq.com/ethereum-foundation |

---

## 📋 Suggested First PR

**Target:** `dmpierre/plasma-fold`  
**Task:** Add basic Rust tests for the client prover + a CONTRIBUTING.md  
**Effort:** 1-2 days  
**Impact:** High visibility, sets up relationship with Pierre/PSE team  

Steps:
1. Fork repo, clone locally
2. Explore `client/` directory structure
3. Write unit tests for core proving functions
4. Add `CONTRIBUTING.md` with build/test/run instructions
5. Open PR with clear description referencing the paper
