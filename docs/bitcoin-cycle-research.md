---
date: 2026-04-18
type: reference
tags: [research, crypto, bitcoin, cycle-theory, dca-strategy]
status: active
---

# Bitcoin Cycle Research — DCA Strategy Implications

## The Historical Cycle Pattern

Bitcoin has often followed a halving-adjacent boom/bust pattern, but the sample is small and each cycle had different macro and liquidity conditions.

- 2012-2015: post-halving rally followed by a deep drawdown
- 2016-2018: similar pattern, with the peak arriving roughly 18 months after the halving
- 2020-2022: another boom/bust cycle, amplified by COVID-era liquidity and then rapid tightening
- 2024-present: the first full ETF-era cycle; so far the drawdown has been shallower than prior major cycles

## The ETF Structural Break (Jan 2024)

Spot Bitcoin ETFs launched in January 2024 — before the April 2024 halving. This is the key variable that may have changed the cycle dynamics.

### What Changed

- **Regulated access broadened** — advisors and institutions now have a standard brokerage wrapper for BTC exposure
- **Market structure changed** — ETF flows, basis trades, and macro liquidity now matter more than in earlier retail-dominated cycles
- **Turnover may be lower** — ETF wrappers likely reduce some forced turnover versus exchange-held retail coins, though I do not yet have a primary-source dataset quantifying that effect
- **Drawdowns may be dampening** — the current cycle has been less violent than prior major BTC drawdowns, which is directionally consistent with a maturing market

### What Hasn't Changed

- **BTC still trades as a risk asset** when liquidity tightens
- **Reflexive sentiment still matters** — euphoric momentum and panic selling have not disappeared
- **On-chain frameworks still help** — realized price, MVRV, and exchange reserve trends remain useful context even if they are no longer sufficient on their own

## The Core Question

Is the cycle **attenuating** (still exists but with smaller drawdowns and slower recoveries) or **breaking** (institutions have fundamentally changed the market structure)?

**Evidence for attenuating:**
- The current drawdown has been shallower than prior major BTC bear markets
- On-chain metrics (MVRV, realized price) still show cyclical behavior
- Halving-driven supply changes still exist, even if they matter less than before

**Evidence for breaking:**
- First-ever pre-halving all-time high in March 2024
- ETF demand created a structural bid that did not exist in earlier cycles
- Macro liquidity and institutional positioning now matter more than the old retail-only cycle template

**Pragmatic read:** Probably attenuating. Cycles are not dead, but the old "copy the last three charts" approach is weaker than before. Institutional access likely raises the floor, but it does not remove the possibility of large corrections.

## DCA Strategy Implications

Given this analysis, where does that leave your $1,000 bi-weekly DCA?

### Option 1: Flat DCA Forever

- **Pros**: Simplest. Works regardless of whether cycles exist. Over long periods, time in market beats timing.
- **Cons**: Buying through local tops is expensive. If cycles still matter, flat DCA will overpay during euphoric phases.
- **Best if**: You believe cycles are fully broken or you do not want to manage actively.

### Option 2: Value-Averaging (target allocation %)

- **Pros**: Naturally reduces crypto buying when it grows beyond target, increases buying when it shrinks. No cycle view required. If your target is 25% crypto and it drifts to 37%, you slow down. If it crashes to 15%, you speed up.
- **Cons**: Requires defining a target %. It does not trim the position itself — just the rate of new buying.
- **Best if**: You believe crypto is a permanent allocation but want a mechanical guard against overconcentration.

### Option 3: Cycle-Aware DCA

- **Pros**: Adjust buy amounts based on estimated cycle position. Buy more aggressively in weak phases, reduce in euphoric phases.
- **Cons**: Requires defining "where are we in the cycle" — which is materially less reliable post-ETF. Risk of being wrong and either overpaying or under-accumulating.
- **Best if**: You believe cycles are real (even attenuated) and want to lean into them without fully trading.

### Option 4: Cycle-Trading (trim at tops)

- **Pros**: Maximum return if you can identify cycle peaks.
- **Cons**: Hardest to execute. Requires selling into euphoria and buying into fear. Tax implications for non-reg account. Risk of being wrong is high.
- **Best if**: You have high conviction in cycle timing and discipline to execute mechanically.

## Suggested Framework

Given that:
- Cycles appear to be attenuating, not eliminated
- Institutional adoption provides a higher-quality ownership base
- You're in a non-registered account (tax implications for selling)
- Your thesis is "permanent allocation" not "trade"

**A reasonable position**: Option 2 (value-averaging) as the default, with Option 3 (cycle-aware adjustments) as an overlay when cycle signals are unusually clear.

Practical implementation:
1. Set a target crypto allocation (e.g., 25%)
2. When crypto drifts modestly above target, reduce DCA; when it is materially above target, pausing new buys is reasonable
3. When crypto drifts below target, increase DCA amount
4. Only trim the position itself (Option 4) if crypto exceeds a hard cap (e.g., 40%) and multiple independent signals point to euphoric conditions
5. Revisit after each halving (next one ~2028) to see if the attenuation thesis still holds

## Key Signals to Watch

- MVRV Z-score
- Realized price vs spot price
- Exchange reserve balance
- ETF net flows
- Strategy capital-raising and treasury-buy activity
- Tether issuance, redemptions, reserve disclosures, and regulation
- Short-term-holder cost basis

## Open Questions

- [ ] Define target crypto allocation %
- [ ] Define hard cap above which you'd trim
- [ ] Decide if cycle adjustments are worth the complexity
- [ ] Revisit after this cycle's bottom forms to validate the attenuation thesis

## Sources

- [SEC: Statement on the Approval of Spot Bitcoin Exchange-Traded Products](https://www.sec.gov/newsroom/speeches-statements/gensler-statement-spot-bitcoin-011023)
- [CoinGecko Bitcoin](https://www.coingecko.com/en/coins/bitcoin) — historical price context and current market data
- [[strategy/thesis-crypto]] — portfolio-level crypto sizing framework
- [[portfolio/2026-04-18]] — current BTC position sizing context
