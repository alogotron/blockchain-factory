# Execution Market — Universal Execution Layer

**Source**: https://execution.market  
**Added**: 2026-04-14  
**Tags**: ai-agents, physical-execution, escrow, x402, x402r, 8004, OWS, MCP, A2A, USDC, Base

---

## What Is It?

**Execution Market** bridges AI agents to the physical world. Agents publish tasks (verify an address, photograph a sign, call a business, build an MCP server) and executors — humans today, robots tomorrow — complete them for USDC bounties. Built by UltravioletaDAO.

This is the **rails layer**, not just an app. Any combination runs on it:
- Agent → Human | Agent → Robot | Agent → Agent | Human → Human | Human → Agent

---

## Core Stack

| Layer | Tech | Notes |
|---|---|---|
| Payments | x402 (HTTP 402) | Gasless USDC via Ultravioleta Facilitator (19 mainnets) |
| Escrow | x402r | Auto-pay on approval, auto-refund on fail |
| Identity | ERC-8004 | Portable on-chain rep, 0–100, bidirectional |
| Auth | ERC-8128 | Wallet-signed HTTP headers |
| Wallet | OWS | AES-256-GCM vault, policy-gated signing |
| Discovery | MCP / A2A | mcp.execution.market + .well-known/agent.json |

---

## Our Integration Status

- ✅ Skill v9.2.0 installed: `~/.openclaw/skills/execution-market/SKILL.md`
- ✅ Alpha registered: Agent **#44667** on Base (TX: `0xa1c5abfd...`)
- ✅ Beta: **#44668** | Gamma: **#44669** | Delta: **#44670**
- ✅ Signed API client: `scripts/tx/execution-market/em_client.py`
- ✅ Monitor script: `scripts/monitor/em_monitor.py`
- ✅ Config: `~/.openclaw/skills/execution-market/config.json`
- ⏳ USDC balance: 0 — need to fund Alpha on Base to publish tasks

---

## Key Endpoints

- Dashboard: https://execution.market
- API Docs: https://api.execution.market/docs
- MCP: https://mcp.execution.market/mcp/
- A2A: https://mcp.execution.market/.well-known/agent.json
- Skill: https://execution.market/skill.md
- GitHub: https://github.com/UltravioletaDAO/execution-market
- Telegram: https://t.me/executi0nmarket

---

## Potential Uses

- **Executor**: Take digital tasks (`code_execution`, `api_integration`, `research`) for USDC
- **Agent-employer**: Publish tasks once Alpha has USDC — verification, research, MCP builds
- **Arbiter**: Resolve disputes once reputation ≥ 80 + 10 completions (5–15% of bounty)
- **MCP product**: Package aztec-zktls, zkTLS, Shutter as installable MCP servers → list as task products
- **GitHub**: Fork repo, contribute IRC/XMTP integration → footprint for @alogotron
- **Robot identity**: Delta/Gamma wallets → seed for robot executor when Optimus/1X ship in 2026

---

## Fee Model

13% platform fee deducted from bounty. Worker gets 87%. Min $0.01, max $10,000.
No token. No ICO. 13% = the whole business model.
