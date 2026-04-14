# dAIScan — ERC-8004 Agent Scoring System

**Date researched:** 2026-04-04  
**URL:** https://www.daiscan.io  
**Twitter:** @dAI_scan  
**Powered by:** BNB Attestation (bas.io / bascan.io)  
**Type:** On-chain AI agent health scoring & scanning platform

---

## What It Is

dAIScan is a scoring system that **automatically scans and evaluates every ERC-8004 agent** and generates a publicly accessible "health report" onchain.

Scoring dimensions:
- **Compliance** — follows ERC-8004 spec
- **Availability** — endpoints are live and reachable
- **Execution** — agent actually responds/works
- **Security** — no obvious vulnerabilities

Tagline: *"Whether your agent actually works — is no longer up to you. The score speaks for itself."*

---

## ⚠️ Critical Finding: Chain Mismatch

**daiscan operates on BNB chain (via BNB Attestation), NOT on Ethereum Sepolia.**

Our registered agents:
| Agent | ID | Chain | daiscan status |
|---|---|---|---|
| DataAnalyst Pro | #461 | Sepolia | ❌ NOT visible (wrong chain) |
| WORM Stealth Coordinator | #462 | Sepolia | ❌ NOT visible (wrong chain) |
| ChainSentry | #1581 | Sepolia | ❌ NOT visible (wrong chain) |
| GasChecker | TBD | Sepolia | ❌ NOT visible (wrong chain) |

To get scored on daiscan, agents must be registered on the **BNB chain registry** that daiscan monitors.

---

## Opportunity: Deploy to BNB for daiscan Score

Steps to get scored:
1. Deploy ERC-8004 registries on BNB chain (or use existing BNB-deployed registry)
2. Register agents with live endpoints (A2A/MCP must be reachable)
3. daiscan automatically scans and scores
4. Score appears at `https://www.daiscan.io/agent/<id>`

**Key requirement:** Endpoints must be **live and publicly accessible** (not localhost).  
GasChecker is the best candidate — it already has live endpoints at github raw URLs.

---

## Integration Notes

- Uses BNB Attestation service for on-chain report storage
- Next.js frontend (JavaScript-heavy, hard to scrape directly)
- URL patterns: `daiscan.io/agent/<id>`, `daiscan.io/api/agents/<id>`
- Community: Telegram https://t.me/+On8eyMFa__JjNWY1

---

## Action Items
- [ ] Research BNB chain ERC-8004 registry address used by daiscan
- [ ] Deploy/register GasChecker on BNB chain (it has live endpoints)
- [ ] Deploy our agents on BNB to get official health scores
- [ ] Monitor daiscan Twitter for scoring criteria updates
