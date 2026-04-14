# Execution Market — Overview

**Source**: https://execution.market  
**Added**: 2026-04-14  
**Status**: ACTIVE — wallets registered, client live  
**Tags**: ai-agents, physical-execution, escrow, x402, 8004, USDC, Base, MCP

---

## What Is It?

**Execution Market** is the Universal Execution Layer — infrastructure that connects AI agents to the physical world. Agents publish tasks (verify an address, take a photo, call a business) and executors (humans today, robots tomorrow) complete them for USDC bounties.

Built by **UltravioletaDAO** (`@0xultravioleta`).

---

## Core Stack

| Layer | Technology | Details |
|---|---|---|
| Payments | x402 (HTTP 402) | Gasless USDC via Ultravioleta Facilitator |
| Escrow | x402r | Auto-pay on approval, auto-refund on failure |
| Identity | ERC-8004 | On-chain portable reputation, 0-100 scale |
| Auth | ERC-8128 | Wallet-signed HTTP requests |
| Wallet | OWS | AES-256-GCM vault, policy-gated signing |
| Agent protocol | MCP | `mcp.execution.market/mcp/` |
| Agent discovery | A2A | `mcp.execution.market/.well-known/agent.json` |

---

## Live Stats (2026-04-14)

- Total tasks: 952 | Completed: 282 | Expired: 603
- Total volume: $105.09 USDC
- Registered workers: 73 | Registered agents: 3
- Skill version: 9.2.0 (production)

---

## Our Position

| Wallet | ERC-8004 ID (Base) | Role |
|---|---|---|
| Alpha | #44667 | Primary agent + executor |
| Beta  | #44668 | Secondary |
| Gamma | #44669 | Secondary |
| Delta | #44670 | Secondary |

**First registration TX (Alpha)**: `0xa1c5abfd76d51fb6a0f85ca8b9bf2576e4d79b2dcbcc0171f4e30f3e92b7b7a1`

---

## Key Links

- Dashboard: https://execution.market
- API Docs: https://api.execution.market/docs
- MCP Server: https://mcp.execution.market/mcp/
- Skill: https://execution.market/skill.md
- A2A: https://mcp.execution.market/.well-known/agent.json
- GitHub: https://github.com/UltravioletaDAO/execution-market
- Telegram: https://t.me/executi0nmarket
- Twitter: https://x.com/executi0nmarket

---

## Supported Chains (Execution Market)

Base, Ethereum, Polygon, Arbitrum, Avalanche, Optimism, Celo, Monad, SKALE

## Supported Tokens

USDC, EURC, PYUSD, AUSD, USDT

---

## Task Categories (21)

physical_presence, knowledge_access, human_authority, simple_action, digital_physical,
location_based, verification, social_proof, data_collection, sensory, social, proxy,
bureaucratic, emergency, creative, data_processing, api_integration, content_generation,
code_execution, research, multi_step_workflow

---

## Fee Model

- Platform fee: 11–13% (deducted from bounty)
- physical/social: 13% | human_authority: 11% | knowledge/digital: 12%
- Minimum bounty: $0.01 | Maximum: $10,000
- Worker receives: 87% of bounty

---

## Local Files

- Client: `scripts/tx/execution-market/em_client.py`
- Monitor: `scripts/monitor/em_monitor.py`
- Config: `~/.openclaw/skills/execution-market/config.json`
- Skill: `~/.openclaw/skills/execution-market/SKILL.md`
- Tracker: `~/.openclaw/skills/execution-market/active-tasks.json`
