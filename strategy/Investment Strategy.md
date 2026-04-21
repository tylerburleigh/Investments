---
date: 2026-04-18
last_updated: 2026-04-21
type: strategy
status: active
tags: [strategy, foundation]
---

# Investment Strategy

## Approach

Barbell strategy: low-cost indexed core with concentrated conviction bets. ESG-screened broad market for the base, heavy crypto allocation as the primary active position, and small asymmetric bets on emerging themes.

## Investor Profile

Canadian resident, US taxpayer. Non-registered accounts are kept to US-listed securities to avoid PFIC complexity. RRSP available; TFSA not currently used. Both registered and non-registered accounts in use.

**Income:** $4,800 CAD bi-weekly (~$9,600/month, ~$115K/year).

## Crypto Thesis

Structural long-term allocation. BTC and ETH represent a fundamental evolution of the financial system — the transition to on-chain money and decentralized settlement. "Permanent" means never fully exiting — the allocation is actively managed toward a target weight. See [[strategy/thesis-crypto]] for the full thesis.

Crypto is 37% of portfolio. Open questions:
- Does this thesis justify the current allocation size and DCA rate, or should crypto's share be smaller as a long-term floor?
- **Crypto DCA strategy** — options on a spectrum:
  1. Flat DCA forever — ignore cycles, simplest, matches "permanent allocation" thesis
  2. Value-averaging — set target %, buy less when over, more when under. Works without cycle view
  3. Cycle-aware DCA — adjust buy amounts based on estimated cycle position. Requires a cycle view
  4. Cycle-trading — trim position at cycle tops with intent to rebuy in bear phase. Most active, highest conviction in cycles required
  - Options 3-4 require believing the 4-year halving cycle still holds, which is disputed (institutional adoption may have changed the structure)
  - Option 2 is the pragmatic middle ground

## ESG Approach

Values-driven but pragmatic. Chose ESGV/VSGX for the passive core because alignment matters, but not dogmatic about ESG screening being strictly "more ethical." Applied to core holdings; active individual picks are exempt from this filter.

## Current Allocation

| Category | Target | Actual (Apr 2026) | Notes |
|----------|--------|-------------------|-------|
| Core ETFs | 50% | 46.5% | **Non-reg (REGISTERED):** VOO, QQQM, VXUS. **RRSP:** VIU.TO, VCN.TO, VFV.TO, VEE.TO. Existing (no active DCA): ESGV, XUSR.TO, VSGX. |
| Crypto | 25% | 37.2% | BTC (29%), ETH (9%), IBIT (6%). Overweight — DCA paused. See [[strategy/thesis-crypto]] |
| Tech Conviction | 10% | 7.7% | NVDA, META, GOOG, MSFT, AMD, TSM, MU. See [[strategy/thesis-tech-conviction]] |
| Canadian Equity | 10% | 6.0% | XCSR.TO, XDSR.TO, POW.TO. Underweight — RRSP can hold Canadian securities. |
| Thematic Bets | 5% | 2.5% | See theses below. Room to grow current positions. |

## Theses, Themes & Positions

### Theses

**[[strategy/thesis-crypto|Crypto]]** — On-chain money and decentralized settlement. BTC, ETH, IBIT. 37% of portfolio (target 25%); DCA currently paused while the position mean-reverts toward target.

**[[strategy/thesis-ai|AI]]** — Biggest capex cycle since the internet. NBIS, AMKR, IREN, APLD, NVTS.
- Themes: [[strategy/theme-quantum|Quantum]] (IONQ, INFQ), [[strategy/theme-robotics|Robotics]] (SYM, ISRG)

**[[strategy/thesis-space|Space]]** — Commercial space industry emerging. RKLB, LUNR, ASTS, MDA.TO.

**[[strategy/thesis-energy-transition|Energy Transition]]** — Electrification and decarbonization. AMPX, ELVR, VST.
- Themes: [[strategy/theme-nuclear|Nuclear]] (OKLO, NLR, CCO.TO), [[strategy/theme-ev|EV]] (NIO)

### DCA Summary

> Daily figures below are trading-day run rates, not calendar-day cash math.

| Thesis / Theme | Tickers | Value | % | Daily DCA |
|----------------|---------|-------:|---|-----------|
| Crypto | BTC, ETH, IBIT | ~$170K | 37% | **Paused** |
| AI Thesis | NBIS, AMKR, IREN, APLD, NVTS | ~$3,270 | 0.7% | $11/day |
| → Quantum | IONQ, INFQ | ~$180 | <0.1% | $4/day |
| → Robotics | SYM, ISRG | ~$1,500 | 0.3% | $9/day |
| Space Thesis | RKLB, LUNR, ASTS, MDA.TO | ~$3,960 | 0.9% | $19/day |
| Energy Transition | AMPX, ELVR, VST | ~$1,100 | 0.2% | $9/day |
| → Nuclear | OKLO, NLR, CCO.TO | ~$627 | 0.1% | $6/day |
| → EV | NIO | ~$860 | 0.2% | $5/day |
| **Total** | | | ~39% | ~$63/day |

> Targets: 5% thematic, 25% crypto. Thematic is currently below target, so sizing can grow selectively as conviction improves. See `decisions/log.md` for history.

### Cross-Thesis Exposure Map

The thesis docs are separate for clarity, but several risks cut across them. When one of these shared signals triggers, review the linked theses together rather than one file at a time.

| Shared Driver | Exposed Theses / Themes | Review Trigger |
|---------------|-------------------------|----------------|
| AI capex cycle | [[strategy/thesis-ai]], [[strategy/thesis-tech-conviction]], [[strategy/thesis-energy-transition]], [[strategy/theme-nuclear]], [[strategy/theme-robotics]], [[strategy/theme-quantum]] | Hyperscaler capex guidance cut >20%, GPU pricing down >30% for a quarter, or major AI cloud distress |
| Power scarcity / data centers | [[strategy/thesis-ai]], [[strategy/thesis-energy-transition]], [[strategy/theme-nuclear]] | New data center PPAs slow, interconnection bottlenecks ease materially, or power prices reset lower |
| Risk-on liquidity | [[strategy/thesis-crypto]], [[strategy/thesis-space]], [[strategy/thesis-ai]], [[strategy/theme-quantum]] | Crypto drawdown, speculative growth multiple compression, or funding markets tightening |
| China exposure | [[strategy/theme-ev]], [[strategy/thesis-energy-transition]], [[strategy/thesis-tech-conviction]] | Tariff escalation, China EV price war intensifies, Taiwan risk escalates, or battery supply chain policy changes |
| Government / defense budgets | [[strategy/thesis-space]], [[strategy/theme-nuclear]], [[strategy/thesis-energy-transition]] | Major program cancellation, budget delay, or policy shift changes backlog quality |

## Capital Flows

Scheduled buys are spread across 3 WealthSimple accounts:

| WealthSimple Label | Actual Type | Frequency | Positions | Scheduled Buy Rate | Weekly Cash Flow |
|--------------------|-------------|-----------|-----------|--------------------|-----------------|
| CRYPTO | Non-registered | Bi-weekly (payday) | BTC, ETH | Paused | $0 |
| REGISTERED | **Non-registered** | Trading days | ~25 (core ETFs, tech, thematic) | ~$143 USD / trading day | ~$715 USD/week (~$1,000 CAD/week at ~0.715 FX) |
| RRSP | RRSP (registered) | Trading days | ~8 (Canadian ETFs, thematic) | ~$131 CAD / trading day | ~$653 CAD/week |

> **Account naming caveat**: The WealthSimple account labeled "REGISTERED" is actually a non-registered taxable account (not an RRSP or TFSA). Only the account labeled "RRSP" has registered tax status. Both registered and non-registered accounts are subject to different PFIC constraints — see Investor Profile above.

**CRYPTO account** (non-registered, crypto-only): DCA currently paused; the $1,000 bi-weekly redirects to the REGISTERED account until crypto allocation mean-reverts toward 25%.

**REGISTERED account** (non-registered, mislabeled): Daily buys on trading days. Receives ~$1K CAD/week deposit. Using ~0.715 USD/CAD, that supports roughly ~$715 USD/week, or about $143 USD per trading day. See [[decisions/2026-04-19-registered-dca-rebalance]].
- Core: VOO ($22), QQQM ($20), VXUS ($20)
- Tech: META ($11), MSFT ($11), GOOG ($8), NVDA ($8), TSM ($4)
- Space: RKLB ($3), LUNR ($2), ASTS ($3)
- AI: NBIS ($1), AMKR ($1), MU ($2), NVTS ($2), IREN ($2), APLD ($1)
- Robotics: SYM ($2), ISRG ($4)
- Energy: AMPX ($2), ELVR ($3), VST ($1)
- Nuclear: OKLO ($2), NLR ($2)
- Quantum: IONQ ($1), INFQ ($1)
- EV: NIO ($3)

**RRSP** ($179K): Daily buys on trading days. Base run rate is ~$131 CAD per trading day (~$653 CAD/week), with temporary accelerated deployment layered on via [[decisions/2026-04-19-rrsp-cash-deployment]].
- Core: VIU.TO ($45), VCN.TO ($35), VFV.TO ($25), VEE.TO ($17.50)
- Thematic: MDA.TO ($5), CCO.TO (position only, no active DCA)
- Canadian Equity: POW.TO ($3)

> **Note on currency**: Some recurring buys were set in CAD for US-listed securities (e.g. VXUS), causing the actual USD amount to differ from the target. Switching these to USD where applicable.

Note: CRYPTO account also holds ESGV, XUSR.TO, IBIT, NVDA, AMD and other US-listed positions (from before the current DCA schedule was set up). MSB accounts are savings, not investment accounts — excluded from portfolio analysis.

## Live Views

> These are Dataview queries — they render as live tables when you open this file in Obsidian. The agent does not use or interpret these blocks.

### Holdings by Conviction
```dataview
TABLE ticker, status, conviction, theme, last_updated AS "Updated"
FROM "holdings"
WHERE type = "holding" AND file.name != "index"
SORT conviction DESC, last_updated ASC
```

### Thesis / Theme Staleness
```dataview
TABLE last_updated AS "Updated", status
FROM "strategy"
WHERE type = "strategy"
SORT last_updated ASC
```

### Recent Decisions
```dataview
TABLE ticker, action, conviction, date
FROM "decisions"
WHERE type = "decision"
SORT date DESC
LIMIT 10
```

## Review Cadence

- **Weekly**: Quick check — portfolio value, notable moves, any action needed
- **Monthly deep dive**: Full allocation review, thesis checks, drift analysis, decision log review

## Position Sizing Rules

These are operating guardrails, not automatic orders. A material buy/sell still gets a decision note, and tax/account constraints can override mechanics when explicitly documented.

- **Core ETF floor**: keep broad-market core near 50% target; review if core falls below 45% or rises above 55%.
- **Crypto band**: 25% target, 20-30% operating band. No new crypto DCA above 30%. Review trim strategy above 35%; require explicit decision note above 40%.
- **Tech conviction band**: 10% target, 7-13% operating band. DCA toward target while thesis intact; pause or redirect if above 13%.
- **Canadian equity band**: 10% target, 7-13% operating band, mostly account/tax-structure driven.
- **Thematic band**: 5% target, 3-7% operating band. Treat as venture-style exposure: many small positions, few allowed to scale.
- **Single-name default cap**: 5% of portfolio for individual equities unless a thesis explicitly grants an exception. BTC is the existing exception and is governed by the crypto band.
- **Speculative / pre-revenue cap**: default 0.5-1.0% per name until revenue, contract, or milestone evidence improves. Examples: ASTS, LUNR, OKLO, IONQ, INFQ, NVTS.
- **Quality anchor cap**: profitable or cash-generative thesis anchors can scale larger than speculative names, but review above 2% within thematic or 5% portfolio-wide.
- **Minimum position rule**: sub-$100 positions should be closed unless actively DCA'd or explicitly kept as a tracking position. Sub-$500 inactive positions need a reason to stay.
- **Trim order**: when a thesis is above target but intact, pause DCA first, redirect new cash second, trim only when allocation exceeds the review band or the thesis weakens.
- **Exit rule**: if a primary hypothesis disconfirms and there is no clear recovery path, stop DCA immediately and decide between trim, tracking-size hold, or exit.

## Open Questions

- [x] Define target allocation percentages *(50/25/10/10/5 — Apr 2026)*
- [x] Decide on crypto DCA strategy *(value-averaging with cycle awareness — paused until allocation drifts to 25%)*
- [x] Set max position size rules *(draft operating guardrails — Apr 2026)*
- [x] Define trim/exit criteria *(pause DCA → redirect cash → trim/exit on thesis break — Apr 2026)*
- [x] Decide on thematic sizing approach *(venture-style exposure with small pre-revenue caps — Apr 2026)*
- [ ] Clean up sub-$100 positions — keep or close?
- [ ] Resize daily DCAs to align with new target allocations
