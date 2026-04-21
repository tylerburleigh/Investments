---
date: 2026-04-19
last_updated: 2026-04-19
type: reference
status: active
tags: [research, methodology, sources]
---

# Research Methodology

Reference doc covering when to research, how to research, and which sources to trust or discount by domain. See [[docs/research-backlog]] for the open question queue.

---

## Research Cadence

### Weekly (~15–30 min)
- Scan news for thesis-relevant events (Tavily search by thesis tag)
- Check hypothesis tables in thesis docs for triggered conditions
- If something significant occurred: append to `decisions/log.md` as a `signal` entry and note in the relevant thesis doc's Updates section
- No deep dives required unless a hypothesis is triggered or a major position moves >10%

### Monthly (~2–4 hrs, aligned with monthly review)
- Run `python3 scripts/lint.py --write-index` — errors first, then work through warnings
- Review `docs/research-backlog.md` for overdue items; resolve or push dates with a note
- Pick 1–3 backlog items to research deeply; update thesis docs with findings
- Evaluate any hypotheses whose timeframes have passed
- Update `last_updated` on any thesis/theme docs touched

### Quarterly (~half day, aligned with quarterly review)
- Full thesis stress test: re-read each thesis doc and ask "does this thesis still hold?"
- Evaluate all open hypotheses — confirmed, disconfirmed, or expired?
- Update conviction levels in the active positions tables
- Review trusted-sources list below — add new sources discovered, retire ones that proved unreliable

---

## Research Methods

| Method | Use For | Tool |
|--------|---------|------|
| News search | Thesis-relevant events, hypothesis triggers, macro | Tavily `tavily_search` |
| Deep web research | Sourcing specific claims, finding analyst reports | Tavily `tavily_research` |
| Earnings transcripts | Position-specific thesis checks, management tone | SEC EDGAR (full text), Motley Fool, Seeking Alpha |
| SEC filings | Factual company data (revenue, debt, risk factors) | SEC EDGAR `edgar.sec.gov` |
| Macro data | Rate environment, GDP, inflation, employment | FRED `fred.stlouisfed.org` |
| On-chain data | Crypto flows, exchange balances, miner activity | Glassnode, CoinGecko |
| Fed policy signals | Rate path, balance sheet, FOMC minutes | `federalreserve.gov` |

---

## Trusted Sources by Domain

### Crypto

| Source | Trust Level | Notes |
|--------|------------|-------|
| Glassnode | High | On-chain metrics — authoritative for exchange flows, SOPR, MVRV |
| CoinGecko | High | Market cap, dominance, volume — live data, cite with date |
| Chainalysis | High | Institutional/compliance-focused on-chain research |
| Federal Reserve research papers | High | Macroeconomic analysis of crypto markets |
| Crypto Twitter / X | Discount | High noise, survivorship bias, frequent undisclosed conflicts of interest |
| Price prediction accounts | Ignore | Not research |

### AI / Semiconductors

| Source | Trust Level | Notes |
|--------|------------|-------|
| TSMC earnings calls | High | Authoritative on packaging capacity, demand signals |
| SEC filings (10-K, 10-Q) | High | Factual — use for revenue, debt, risk factors |
| SemiAnalysis | High | Deep technical analysis on chip architecture and supply chain |
| Fabricated Knowledge | High | Supply chain and semiconductor industry depth |
| Goldman Sachs / Morgan Stanley research | Medium | Directionally useful; models are opaque, sell-side bias |
| IDC / Grand View Research | Medium | Market size estimates — wide ranges, methodology varies; cite with caveats |
| McKinsey / BCG | Medium | Useful for market sizing frameworks; often lagged, directional only |
| Tech press (The Verge, Wired, Ars) | Low | Consumer framing, rarely models the business |
| AI hype media | Discount | Narrative-driven, not analytical |

### Space

| Source | Trust Level | Notes |
|--------|------------|-------|
| SpaceNews | High | Industry trade press — factual, no hype |
| NASASpaceflight.com | High | Launch and mission coverage — detailed and accurate |
| Company investor days / SEC filings | High | For backlog, revenue, program milestones |
| Morgan Stanley / BofA space research | Medium | Market size estimates only; space sector coverage is thin |
| Space enthusiast blogs | Low | Often accurate on technical detail, poor on business |

### Energy / Nuclear

| Source | Trust Level | Notes |
|--------|------------|-------|
| IAEA publications | High | Authoritative on global nuclear capacity, safety, projections |
| EIA (US Energy Information Administration) | High | US energy data — generation, storage, consumption |
| WNN (World Nuclear News) | High | Nuclear industry trade press — factual |
| NREL (National Renewable Energy Laboratory) | High | Renewable + storage cost data |
| Sprott | Medium-High | Uranium supply/demand — authoritative on uranium specifically; bullish bias on uranium price |
| Morningstar | Medium | ETF analysis is useful; sector coverage variable quality |
| Nuclear advocacy sites | Discount | Directionally pro-nuclear; not objective |
| Anti-nuclear activism | Discount | Directionally anti-nuclear; not objective |

### Macro

| Source | Trust Level | Notes |
|--------|------------|-------|
| FRED (Federal Reserve Economic Data) | High | Primary source for US macro data |
| BIS (Bank for International Settlements) | High | Global macro, credit, cross-border flows |
| IMF / World Bank | High | Global economic projections; useful for emerging market context |
| BEA / BLS (US government statistics) | High | GDP, employment, inflation — primary data |
| FOMC minutes | High | Fed policy signals — read the actual minutes, not summaries |
| Goldman Sachs / JPMorgan macro research | Medium | Useful directional reads; sell-side incentive to be optimistic |
| CNBC / Bloomberg opinion | Discount | Entertainment, not analysis — useful for knowing what the consensus narrative is |
| Financial Twitter | Discount | Same issues as crypto Twitter |

### General Principles

- **Primary over secondary.** File the original report, not a summary article about it.
- **Date every market-size figure.** Markets move; a 2022 estimate isn't a 2026 estimate.
- **Cite methodology caveats.** "24% CAGR" means nothing without knowing whether it's base/bull/bear case and what's included in the market definition.
- **When in doubt, use `[!unverified]`.** It's better to flag uncertainty than to let a guess harden into assumed fact.
- **Analyst price targets.** Ignore the target; understand the model and assumptions if available.

---

## Claim Typing Quick Reference

Applied to factual claims in thesis/theme docs where provenance matters:

| Callout | Use When |
|---------|----------|
| `> [!source]` | Cited from a specific source — include `[[docs/...]]` or URL |
| `> [!analysis]` | Your inference or interpretation — show the reasoning |
| `> [!unverified]` | Recalled or assumed figure not yet double-checked |
| `> [!gap]` | Something you know you don't know — flags for backlog |

Promote `[!gap]` and `[!unverified]` items to [[docs/research-backlog]] with a `Review By` date.
