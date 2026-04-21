---
date: 2026-04-19
type: decision
ticker: [VOO, QQQM, VXUS, NVDA, META, GOOG, MSFT, TSM]
action: add
conviction: 4
time_horizon: medium
status: active
tags: [allocation, dca, core, tech-conviction, rebalancing]
---

# Decision: Redirect Paused Crypto DCA to Core + Tech — 2026-04-19

## What

Redirect $1,000 bi-weekly (formerly crypto DCA) into the REGISTERED (non-registered) account, split between core ETFs and tech conviction. Adds roughly ~$71 per trading day to the pre-existing schedule before the same-day cash-flow rebalance.

**Core (+$40/day):**
| Ticker | Current DCA | New DCA | Change |
|--------|------------|---------|--------|
| VOO | $25/day | $39/day | +$14 |
| QQQM | $25/day | $38/day | +$13 |
| VXUS | $25/day | $38/day | +$13 |

**Tech Conviction (+$31/day):**
| Ticker | Current DCA | New DCA | Change |
|--------|------------|---------|--------|
| NVDA | $5/day | $15/day | +$10 |
| META | $12/day | $19/day | +$7 |
| GOOG | $10/day | $15/day | +$5 |
| MSFT | $15/day | $20/day | +$5 |
| TSM | $3/day | $7/day | +$4 |

REGISTERED scheduled total: ~$181 → ~$252 per trading day (~$1,260/week before the same-day cash-flow rebalance).

> Same-day follow-up: [[decisions/2026-04-19-registered-dca-rebalance]] resized the actual buy schedule from ~$252 to ~$143 per trading day so the redirect fit real cash flow.

## Why

- Crypto allocation at 37% vs 25% target — DCA paused, not resuming until allocation drifts down
- Core ETFs underweight (46.5% vs 50% target) — adding $40/day closes the gap over time
- Tech conviction underweight (7.7% vs 10% target) — adding $31/day, with NVDA getting the largest bump (currently $5/day was disproportionately low for the highest-conviction name)
- REGISTERED account is non-registered — US-listed securities only (PFIC rules). Canadian equity gap (6% vs 10%) can't be filled here; RRSP DCAs cover that separately
- Proportional split (core ~56%, tech ~44% of new money) reflects the relative size of each gap

## Holdings Affected

- Tech conviction: [[holdings/NVDA]], [[holdings/META]], [[holdings/GOOG]], [[holdings/MSFT]], [[holdings/TSM]]

## What Would Change My Mind

- If crypto allocation drops below 25%, resume crypto DCA and reduce this redirect proportionally
- If a tech conviction name deteriorates (earnings miss, thesis break), pause that individual DCA and redistribute within the bucket
- If core ETF allocation reaches 50%, consider redirecting the core portion to Canadian equity (via RRSP) or thematic

## Supporting Research

- [[decisions/2026-04-18-crypto-pause-dca]] — original pause decision, this is the follow-up
- [[strategy/Investment Strategy]] — allocation targets and capital flows
- [[portfolio/2026-04-18]] — snapshot showing current allocations

## Follow-up

- [x] Resize the redirected schedule to fit real cash flow — [[decisions/2026-04-19-registered-dca-rebalance]]
- [ ] Update WealthSimple recurring buys to match new daily amounts
- [ ] Verify first week of buys executed correctly
- [ ] Review allocation impact at next monthly review
