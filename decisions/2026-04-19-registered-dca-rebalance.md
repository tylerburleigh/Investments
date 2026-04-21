---
date: 2026-04-19
type: decision
action: rebalance
conviction: null
time_horizon: medium
status: active
tags: [allocation, dca, rebalancing, cash-flow]
---

# Decision: Rebalance REGISTERED DCA to Match Cash Flow — 2026-04-19

## What

Cut REGISTERED account scheduled DCA from ~$252 to ~$143 per trading day (~43% reduction) to match actual deposit inflow of ~$1K CAD/week. Proportional cut across all positions.

## Why

- Original $252/day schedule (from 2026-04-18 restructuring) was set without checking against actual cash inflows
- REGISTERED account receives about $1,000 CAD/week, which is roughly ~$715 USD/week at ~0.715 FX, or about $143 USD per trading day
- Running at ~$252 per trading day would overspend the funding rate by roughly ~$545/week before FX slippage and fees
- Proportional cut preserves the relative allocation intent: core 43%, tech 30%, thematic 27%

## New DCA Schedule

See [[strategy/Investment Strategy]] for full breakdown by ticker.

**Summary:**
- Core ETFs (VOO, QQQM, VXUS): $61/day
- Tech Conviction (NVDA, META, GOOG, MSFT, TSM): $43/day
- Thematic (19 positions across space, AI, robotics, energy, nuclear, quantum, EV): $39/day
- **Total: ~$143/trading day (~$715 USD/week, equivalent to ~$1,000 CAD/week at ~0.715 FX)**

## Holdings Affected

- Tech conviction: [[holdings/NVDA]], [[holdings/META]], [[holdings/GOOG]], [[holdings/MSFT]], [[holdings/TSM]]
- Space: [[holdings/RKLB]], [[holdings/LUNR]], [[holdings/ASTS]]
- AI infrastructure: [[holdings/NBIS]], [[holdings/AMKR]], [[holdings/MU]], [[holdings/NVTS]], [[holdings/IREN]], [[holdings/APLD]]
- Robotics / energy / nuclear / quantum / EV: [[holdings/SYM]], [[holdings/ISRG]], [[holdings/AMPX]], [[holdings/ELVR]], [[holdings/VST]], [[holdings/OKLO]], [[holdings/NLR]], [[holdings/IONQ]], [[holdings/INFQ]], [[holdings/NIO]]

## What Would Change My Mind

- If deposit rate increases (raise, bonus, other income), proportionally increase DCAs
- If we want to draw down existing cash balance in the account, temporarily run above $143/day
- If a specific position warrants accelerated accumulation (thesis change, major dip)

## Supporting Research

- [[strategy/Investment Strategy]] — allocation targets and capital flows
- [[decisions/2026-04-18-thematic-rebalance]] — previous DCA restructuring
- [[decisions/2026-04-19-crypto-dca-redirect]] — concurrent redirect decision

## Follow-up

- [ ] Update WealthSimple recurring buys to match new daily amounts
- [ ] Verify first week of buys executed correctly
- [ ] Set up Norbert's Gambit for monthly CAD→USD conversion (~$4K/month)
