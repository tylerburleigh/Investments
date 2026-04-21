---
date: 2026-04-18
last_updated: 2026-04-19
type: reference
tags: [log, decisions, actions]
---

# Decision & Action Log

Append-only chronological log of portfolio actions. **Newest on top.**

## Format

```
### [YYYY-MM-DD] {kind} | short description — [[link-if-any]]
```

**Kinds:**
- **decision** — full decision file in `decisions/`. Link is required.
- **action** — lightweight change without a separate decision file (routine DCA tweaks, cleanup of sub-$100 positions, etc.). No link needed.

See [[CLAUDE|the vault guide]] for when to write a full decision vs. a log-only action.

**Deprecated kinds (pre-2026-04-20 only):** `review`, `thesis-update`, `snapshot`, `signal`. These are now self-documenting: reviews → `reviews/`, snapshots → `portfolio/`, thesis updates → thesis doc `## Updates` sections, signals → `scans/`.

---

### [2026-04-20] snapshot | portfolio snapshot — [[portfolio/2026-04-20]]
### [2026-04-20] review | weekly review — [[reviews/2026-04-20-weekly]]
### [2026-04-20] signal | Crypto H1: BTC ETF ~$1B weekly inflows (week ending Apr 17), ETH ETF $276M — [[strategy/thesis-crypto]]
  Source: CoinDesk (Apr 20). Institutional flows clearly positive on 4-week rolling basis. Morgan Stanley BTC ETF launched with $100M first-week inflows. Directional confirmation of H1 (ongoing — not formally evaluated).
### [2026-04-20] signal | SYM new customer win: Associated Wholesale Grocers deploying automation at Gulf Coast DC (114K sq ft) — [[strategy/theme-robotics]]
  Source: Yahoo Finance / SYM press release (~Apr 12). Reduces Walmart concentration risk. Also acquired Veo Robotics FreeMove assets (Q1 earnings). Not a hypothesis trigger but positive for H1 direction (customer diversification).
### [2026-04-20] action | verified first trading day of new DCA plan: all 27 REGISTERED positions (~$142 vs $143 target) and 7 RRSP positions (~$1,073 vs $1,072 target) within rounding. New positions ISRG and CCO.TO started correctly. KSTR appeared ($3, not in plan — needs investigation)
### [2026-04-19] signal | BlueBird 7 launch failure — New Glenn upper stage anomaly, satellite de-orbited. Negative for H3 cadence but AST still targets 45 sats by YE — [[strategy/thesis-space]]
### [2026-04-19] thesis-update | sourced strategy docs, resolved backlog research gaps, and added source trails across holding notes
### [2026-04-19] decision | rebalanced REGISTERED DCA from $252/day to $143/day to match $1K CAD/weekly cash inflow (proportional cut across all positions) — [[decisions/2026-04-19-registered-dca-rebalance]]
### [2026-04-19] decision | redirected $1K bi-weekly crypto DCA to core ETFs (+$40/day) and tech conviction (+$31/day) in REGISTERED account — [[decisions/2026-04-19-crypto-dca-redirect]]
### [2026-04-19] decision | deploying $40K RRSP cash over 6 weeks via accelerated DCA, 5% to CCO.TO — [[decisions/2026-04-19-rrsp-cash-deployment]]
### [2026-04-18] action | sold orphaned positions: HOOD, SOFI, MVST, UFO, XCG.TO, LLY, PNG.VN, USDC (no thesis, sub-$250 bags except XCG.TO legacy)
### [2026-04-18] decision | rebalanced thematic DCA ($39→$26/day), sold QBTS, EOSE, BABA, CRSP, IBKR — [[decisions/2026-04-18-thematic-rebalance]]
### [2026-04-18] decision | paused $1,000 bi-weekly crypto DCA (BTC, ETH); redirecting to non-reg or RRSP — [[decisions/2026-04-18-crypto-pause-dca]]
### [2026-04-18] decision | sold Harvest covered-call products in RRSP (HBTE.NE, GOGY.TO, NVHE.TO, HBIX.NE, HUTE.TO) — [[decisions/2026-04-18-harvest-sell]]
### [2026-04-18] action | stopped DOL.TO DCA in RRSP (routine cleanup, no standalone thesis)
### [2026-04-18] action | cut PNG.TO from RRSP daily DCA (routine cleanup, small position, no standalone thesis)
### [2026-04-18] snapshot | first portfolio snapshot — [[portfolio/2026-04-18]]
