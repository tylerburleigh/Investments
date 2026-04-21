---
date: 2026-04-18
last_updated: 2026-04-21
type: strategy
status: active
tags: [thesis, crypto, bitcoin, ethereum, digital-assets]
---

# Crypto Thesis

## Thesis

Structural long-term allocation. Crypto represents a fundamental evolution of the financial system — the transition to on-chain money and decentralized settlement. BTC is the settlement layer (digital gold); ETH is the programmable layer (decentralized compute). Spot ETFs, institutional adoption, and declining exchange supply are symptoms of this larger shift.

**"Permanent" means never fully exiting the position, not that the allocation is never adjusted.** Value-averaging toward a 25% target weight is the active stance: DCA pauses when overweight, resumes when underweight, and cycle-aware trimming remains on the table if the 4-year halving cycle still holds (see [[docs/bitcoin-cycle-research]]). The thesis is structural; the sizing is managed.

## Variant View

- **Market view**: crypto is still mostly a volatile risk asset whose cycles dominate long-term outcomes.
- **My view**: BTC is becoming a permanent institutional allocation bucket, while ETH remains an option on decentralized compute and settlement infrastructure.
- **Why this matters**: if the institutional bid is durable, drawdowns may still be severe but the long-term floor should rise; if it is only cycle liquidity, the current overweight needs more aggressive trimming discipline.

## Market Size

> [!analysis] Total crypto market cap and BTC dominance are useful monitoring variables, but they move too quickly to serve as thesis anchors.
> I will treat them as state variables checked against live market data rather than fixed facts embedded in the document.

> [!analysis] The idea that crypto could one day represent a meaningful share of global financial assets is my own portfolio-level forecast, not a sourced consensus estimate.
> I am no longer treating the old "5-10%" framing as borrowed external research.

## Secular Tailwinds

1. **Spot ETF inflows** — pensions, endowments, sovereign wealth gaining regulated access
2. **Nation-state adoption** — sovereign reserve allocations (El Salvador, discussions in US, others)
3. **Exchange liquid supply declining** — institutional "diamond handing" reducing available float
4. **Regulatory clarity** — US moving toward pro-crypto framework
5. **DeFi maturation** — decentralized finance protocols gaining real usage
6. **Ethereum scaling** — L2 solutions reducing fees and increasing throughput

## Major Risks

- **Macro headwinds** — high rates limit upside momentum; crypto remains risk-on
- **Regulatory reversal** — policy shifts could crater institutional demand
- **Concentration risk** — BTC at 29% of portfolio is the single largest position; 50%+ drawdowns are normal. A 50% drawdown in the BTC position from roughly $131K of market value would imply about a $66K portfolio hit (~14% total portfolio decline). This is the cost of the overweight — acceptable within the barbell structure but would be painful.
- **Technological** — protocol-level issues, quantum computing threat long-term
- **Narrative risk** — if "digital gold" thesis doesn't hold, the floor drops
- **Cycle uncertainty** — 4-year halving cycle may be attenuating post-ETF institutional adoption

## Active Positions

| Ticker | Role | Conviction |
|--------|------|-----------|
| [[holdings/BTC]] | Settlement layer, digital gold | 4 |
| [[holdings/ETH]] | Programmable layer, decentralized compute | 3 |
| IBIT | BTC ETF (indirect exposure) | 2* |

\* IBIT conviction 2 reflects redundancy with direct BTC, not a weakening thesis. IBIT is held in the RRSP to get crypto exposure in a tax-sheltered account. No active DCA, no plan to add. Would only sell to simplify the position structure.

## Key Position Details

**BTC** (1.27 BTC; ~$131K position value, spot ~$104K, 29% of portfolio): Permanent allocation, financial system evolution thesis. DCA **paused** Apr 2026 — allocation at 37% vs 25% target. Resume when allocation drifts toward target or cycle bottom confirms. See [[decisions/2026-04-18-crypto-pause-dca]].

**ETH** (position held): Ethereum. Programmable blockchain with smart contracts, DeFi, and L2 ecosystem. The ETH thesis is distinct from BTC: BTC is money/settlement, ETH is decentralized compute infrastructure. ETH's value accrual comes from gas fees on the world's most used smart contract platform + staking yield. L2 scaling (Arbitrum, Optimism, Base) is a dual-edged sword: it grows the ecosystem but reduces L1 fee revenue. Conviction 3 (vs BTC at 4) reflects ETH's weaker monetary premium and ongoing questions about value accrual at scale. DCA paused alongside BTC.

**IBIT** (position held, no DCA): iShares Bitcoin Trust ETF. BlackRock spot BTC ETF. Provides regulated BTC exposure. Existing position, no active DCA.

## Allocation / Sizing

Value-averaging with cycle awareness:
- **Target**: 25% of portfolio
- **Current**: 37% — DCA paused
- **Operating band**: 20-30%
- **Review band**: above 35% or below 15%
- **Hard review**: above 40% requires explicit trim/no-trim decision
- **Resume criteria**: allocation drops below 20%, or BTC has significant drawdown with cycle-bottom evidence
- **Trim criteria**: allocation remains above 35% while ETF flows weaken, cycle-top indicators flash, or portfolio core falls below target
- **Framework**: see [[docs/bitcoin-cycle-research]]

## Monitoring Signals

- **ETF net flows / market structure** — the cleanest read on whether institutional demand is still providing a structural bid
- **Strategy capital raises and treasury purchases** — leverage, convert issuance, ATM equity, and treasury-buy cadence can amplify BTC reflexivity and sentiment
- **Tether reserves, redemptions, and regulation** — USDT is system plumbing; any confidence or regulatory shock would hit crypto liquidity broadly, not just BTC
- **Cycle / valuation state** — MVRV z-score, funding-rate extremes, exchange inflows, and realized-cap behavior
- **ETH value accrual** — L1 fees, staking yield, L2 settlement activity, and whether scaling accrues value back to ETH holders

## Decision Rules

These are operating rules, not automatic orders. Any material action still gets a decision note.

| Condition | Action |
|-----------|--------|
| Crypto above 30% of portfolio | Keep DCA paused; redirect new cash to core, tech conviction, or underweight themes |
| Crypto above 35% | Monthly trim/no-trim review; do not add unless a prior decision explicitly overrides |
| Crypto above 40% | Write a decision note choosing between trim, continued pause, or revised target |
| Crypto falls into 20-25% band | Resume normal DCA if ETF flows and regulatory signals remain healthy |
| Crypto below 20% | Consider accelerated DCA unless thesis-specific risks caused the drawdown |
| H2 disconfirms | De-emphasize cycle-aware timing; use target-weight value averaging as default |
| ETF flows turn negative for two straight monthly reviews plus regulation/liquidity worsens | Reassess 25% target and long-term floor allocation |

## Bull / Base / Bear Cases

| Case | What Happens | Portfolio Action |
|------|--------------|------------------|
| Bull | ETF demand stays positive, cycle drawdowns attenuate, BTC becomes accepted institutional collateral/reserve exposure | Let gains run inside the review band; trim only if allocation breaks hard limits |
| Base | Structural thesis intact but volatility remains high; crypto mean-reverts toward 25% as other assets receive DCA | Keep DCA paused while overweight; resume below 20-25% based on signal quality |
| Bear | ETF demand fades, regulation tightens, stablecoin liquidity breaks, or BTC fails the digital-gold narrative | Stop DCA, reassess target allocation, and consider cutting to a smaller permanent floor |

## Hypotheses

| # | Hypothesis | Basis / Source | Date Made | Timeframe | If Confirmed → | If Disconfirmed → | Status | Evaluated |
|---|-----------|----------------|:---------:|-----------|----------------|-------------------|:------:|:---------:|
| H1 | BTC ETF net inflows remain positive on a rolling 4-week basis through 2026 | ETF flow data trend since Jan 2024 launch; structural institutional demand thesis | 2026-04-19 | Ongoing — check monthly | Confirms institutional adoption thesis; maintain/grow allocation | Weakens institutional narrative; review DCA pause rationale | open | — |
| H2 | BTC 4-year halving cycle produces a cycle top in H2 2025–H1 2026 followed by >40% correction | Historical halving cycles (2013, 2017, 2021); [[docs/bitcoin-cycle-research]] | 2026-04-19 | H2 2026 | Cycle-aware DCA strategy validates; resume buying at correction | Cycle has structurally changed post-ETF; flat DCA or value-averaging is the right approach | open | — |
| H3 | No G20 nation implements materially restrictive crypto regulation (exchange bans, asset seizure) through end of 2026 | US moving pro-crypto (SEC, White House); EU MiCA framework; global regulatory trend | 2026-04-19 | Dec 2026 | Regulatory environment confirms; maintain permanent allocation | Re-examine thesis floor and sizing | open | — |
| H4 | BTC allocation drifts from 37% to ≤30% by end of 2026 without active selling (portfolio growth + DCA pause) | Value-averaging model; current DCA paused; other positions DCA-ing | 2026-04-19 | Dec 2026 | Mean-reversion working as intended; resume DCA | Crypto outperforming so fast that trimming required to hit 25% target | open | — |

> [!analysis] H2 is actively testable now (Apr 2026). BTC spot is roughly $104K and the BTC position is worth roughly $131K. If the halving cycle still matters, a cycle top should be forming or have formed. Watch for: declining exchange inflows, funding-rate extremes, and MVRV z-score > 7. If no >40% correction occurs by H2 2026, the cycle thesis is disconfirming in real time.

## Open Research Questions

- [ ] Does the 4-year halving cycle still hold as a predictive framework post-institutional ETF adoption? → see [[docs/bitcoin-cycle-research]]
- [ ] What is the right long-term floor allocation for crypto given the barbell strategy? Does 25% target still hold at portfolio scale?
- [ ] Find analyst report anchoring "crypto at 5–10% of global financial assets" projection → [[docs/research-backlog|B007]]

## Updates

### 2026-04-18 — Initial theme research
Crypto is the largest active position in the portfolio. Created dedicated theme file to complement the BTC holding note and strategy doc crypto section. Key near-term action: hold position, wait for allocation to drift toward 25% target before resuming DCA.
