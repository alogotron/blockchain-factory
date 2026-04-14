# Aztec Alpha — Opportunities & Action Items

**Researched**: 2026-04-08  
**Priority**: HIGH — Alpha just launched, early-mover advantage window is open

---

## 1. Grants Program (ACTIVE)

**URL**: https://aztec.network/blog/introducing-aztec-grants-funding-a-community-led-privacy-ecosystem  
**Format**: Wave-based (opens → closes → repeat)  
**Active RFP**: Application State Migration — https://forum.aztec.network/t/request-for-grant-proposals-application-state-migration/8298

### What Gets Funded
- Noir ecosystem tooling (Wave 3 explicitly targeted Noir dev tools)
- Privacy libraries (e.g., private voting, generalized ZK libraries)
- Ecosystem applications (DeFi, gaming, identity)
- Cross-chain integrations
- Documentation and developer education

### Action Items
- [ ] Monitor https://forum.aztec.network for new RFPs and wave announcements
- [ ] Prepare grant application for a Noir-based tool or contract library
- [ ] Check if Application State Migration RFP is still open

---

## 2. Hackathons (TAIKAI Platform)

**URL**: https://taikai.network/en/aztecnetwork/hackathons  
**Previous**: 4-day ZK hacking week July 15–18 (year unspecified)  
**Focus**: ZK technology, blockchain infrastructure, cryptography

### Action Items
- [ ] Watch TAIKAI page for 2026 hackathon announcements
- [ ] Prepare Noir contract templates in advance for rapid hackathon deployment
- [ ] Identify a compelling use case (private DeFi, private gaming, ZKPassport identity)

---

## 3. Noir Smart Contract Development

Highest leverage opportunity — very few developers know Noir. Early contracts become reference implementations.

### High-Value Contract Ideas

| Idea | Complexity | Value |
|------|-----------|-------|
| Private ERC-20 using AIP-20 | Low | Good starting point, learning |
| Private NFT collection (AIP-721) | Low-Med | Visible, demonstrable |
| Private escrow/payment channel | Medium | Real utility, grant-worthy |
| ZKPassport identity gate | Medium | Compliance + identity angle |
| Private DAO voting contract | Medium-High | High grant potential (AZKR precedent) |
| Private token vesting contract | Medium | DeFi primitive |
| Private game state (poker, chess) | High | Showcase use case |
| Cross-chain private bridge | High | Major infrastructure |

### Dev Stack to Set Up
```bash
# Install Aztec toolchain
npm install -g @aztec/cli
# Or follow: https://docs.aztec.network/developers/overview

# Key repos to clone
git clone https://github.com/AztecProtocol/aztec-starter
git clone https://github.com/AztecProtocol/aztec-examples
```

### Action Items
- [ ] Install Aztec sandbox locally
- [ ] Clone aztec-starter and run hello world contract
- [ ] Build a simple private token using AIP-20
- [ ] Push to alogotron GitHub for footprint

---

## 4. GitHub Contributions (Footprint)

**Monorepo**: https://github.com/AztecProtocol/aztec-packages  
**Examples**: https://github.com/AztecProtocol/aztec-examples  
**Awesome Aztec**: search GitHub for community curated list

### Contribution Angles
- Add examples to aztec-examples (new contract patterns)
- Fix documentation issues (typos, clarifications, missing examples)
- Submit Noir circuit optimization tips
- Add to Awesome Aztec list
- Respond to open issues in aztec-packages

### Action Items
- [ ] Fork aztec-examples and contribute a new contract type
- [ ] Open issues/PRs for documentation gaps found during development
- [ ] Star + watch aztec-packages for contribution opportunities

---

## 5. Governance Participation (AZIPs)

**Forum**: https://forum.aztec.network  
**GitHub**: AZIPs submitted as PRs to aztec-packages

### Low-Effort, High-Visibility Actions
- Participate in forum discussions on open AZIPs
- Comment on RFP threads (signals engagement to Aztec Foundation)
- Submit an AZIP for a new token standard extension or primitive

### Action Items
- [ ] Create account on forum.aztec.network
- [ ] Comment on active discussions (Application State Migration RFP at minimum)
- [ ] Identify a small protocol improvement to propose as AZIP

---

## 6. Bug Bounty / Security Research

**Policy**: https://github.com/AztecProtocol/aztec-packages/blob/next/SECURITY.md  
**Status**: Main bounty program launching as audits progress (Q2-Q3 2026 likely)

### Notes
- Alpha explicitly has known undisclosed bugs — risky to test with real value
- Responsible disclosure rewarded
- Noir circuit security is a niche area — OpenZeppelin has published guidance
- Good angle if Noir expertise develops through contract work

### Action Items
- [ ] Watch for official bug bounty program announcement
- [ ] Review OpenZeppelin's "Developer Guide to Building Safe Noir Circuits"

---

## 7. Airdrop / Incentive Participation

**Status**: AZTEC token LIVE (TGE Feb 11, 2026) — retroactive airdrop window may have passed  
**Ongoing incentives**:
- Sequencer staking rewards (requires 200K AZTEC min stake)
- Prover rewards
- Network fee revenue for active sequencers

### CryptoRank Checklist (from research)
Tasks that may still be eligible for future distributions:
- [ ] Connect wallet to Aztec testnet
- [ ] Request test tokens (ZKPassport verification required)
- [ ] Stake test tokens
- [ ] Execute transactions on Alpha mainnet
- [ ] Get a Discord/community role

### Action Items
- [ ] Send transactions through Alpha mainnet with wallet(s)
- [ ] Execute variety of contract interactions (private transfers, note creation)
- [ ] If holding AZTEC: consider staking or delegating for governance weight

---

## 8. Integration / Partnership Angle

Aztec blog mentions a **contact form for integration support** — relevant if building something that could be showcased as an Aztec ecosystem project.

Potential integration ideas with existing blockchain-factory projects:
- Bring ChaosChain experiments to Aztec (private chaos?)
- Explore x402 payment protocol with Aztec privacy layer
- AgentCash + Aztec: private agent payments

---

## Priority Matrix

| Opportunity | Effort | Potential Reward | Timeline |
|-------------|--------|-----------------|----------|
| Build + push Noir contract to GitHub | Low | Footprint + grant eligibility | This week |
| Forum participation / AZIP commenting | Very Low | Visibility + network | This week |
| Hackathon (TAIKAI) | Medium | Prize + grants + visibility | Watch for dates |
| Grant application | High | Direct funding | 2-4 weeks |
| Mainnet tx activity | Low | Potential future incentives | This week |
| Bug bounty | Medium-High | Variable | When program launches |
| Sequencer operation | Very High (capital) | Staking rewards | If 200K AZTEC available |
