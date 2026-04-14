# x402r — Error Detector Arbiter

**Source**: https://www.x402r.org/blog/open-sourcing-error-detector-arbiter  
**Added**: 2026-04-07  
**Tags**: payments, escrow, API, arbiter, Base, open-source

---

## What Is It?

**x402r (x402 Refund Protocol)** is a decentralized payment protection protocol for API transactions. When a customer pays for an API response, funds are held in on-chain escrow — not sent directly to the merchant. An independent arbiter evaluates the response and either:
- Releases funds to the merchant (PASS)
- Refunds the customer (FAIL)

No dispute process, no trust required — all enforced on-chain with immutable escrow rules.

---

## The Error Detector Arbiter

Open-source component that auto-evaluates API responses. Uses a **two-tiered system**:

1. **Heuristic pass** (instant, no LLM): Catches empty bodies, 500/404 error JSON, HTML error pages, placeholder text ("lorem ipsum", "coming soon")
2. **AI pass**: For anything passing heuristics, an LLM reads the response body to confirm it's real, substantive content (not quality check — just "is this broken?")

On evaluation:
- PASS → calls `release()` on operator → funds to merchant
- FAIL → calls `refundInEscrow()` → funds back to customer

Also stores every evaluated response body — customers can detect merchant cheating by comparing hashes and retrieving payloads via wallet signature.

---

## Key Technical Details

| Component | Value |
|-----------|-------|
| Escrow Contract | `AuthCaptureEscrow` (protocol-wide singleton) |
| Operator Contract | `0x673Dd1f107cDa8E992b4DBd5cB61f5b6c017f3B7` (Base + Base Sepolia) |
| Payment Scheme | `CommerceServerScheme` (ERC-3009 `transferWithAuthorization`) |
| Max Fee | Set via `maxFeeBps` (e.g. 500 = 5%) |
| Attestation | `/attest/identity` endpoint for verifying arbiter before payment |
| Facilitator | https://facilitator.ultravioletadao.xyz |
| Arbiter URL | https://ai-arbiter.up.railway.app |
| Live on | Base Sepolia + Base Mainnet (beta) |

---

## Links

- **Docs**: https://docs.x402r.org
- **SDK**: https://docs.x402r.org/sdk
- **Deploy Operator**: https://app.x402r.org
- **GitHub**: https://github.com/BackTrackCo
- **Discord**: https://discord.gg/4JdMGUyu9Z
- **Twitter**: https://x.com/x402rorg
- **Contact**: hi@x402r.org

---

## Potential Uses / Ideas

- Hook into x402r as a merchant: deploy an API that charges per call with escrow protection
- Use as inspiration for arbiter patterns in other escrow contracts
- Integrate arbiter logic into contract test suites (heuristic pass ideas)
- Explore ERC-3009 `transferWithAuthorization` for gasless payment flows
- Contribution opportunities via GitHub (BackTrackCo)
