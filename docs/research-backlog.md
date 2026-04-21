---
date: 2026-04-19
last_updated: 2026-04-19
type: reference
status: active
tags: [research, backlog, open-questions]
---

# Research Backlog

Centralized tracker for open research questions, unverified claims, and knowledge gaps across all thesis and theme docs. Each item has a required `Review By` date — overdue open items are surfaced by `scripts/lint.py`.

**How items enter this list:**
- Promoted from `[!gap]` or `[!unverified]` callouts in thesis/theme docs
- Open questions from hypothesis evaluations in thesis docs
- Follow-up items from the events log (signal entries)
- Strategic questions surfaced during reviews

**When an item is resolved:** change Status to `resolved`, fill in the Resolved column with a link to where the answer landed, and check off the `- [ ]` in the originating thesis doc.

---

## Open

| # | Question | Thesis / Theme | Surfaced From | Priority | Review By | Status |
|---|----------|---------------|---------------|:--------:|-----------|:------:|
| — | — | — | — | — | — | — |

---

## Resolved

| # | Question | Resolved | Where |
|---|----------|----------|-------|
| B001 | Archive McKinsey $5.2T data center infra by 2030 figure — source link not on file | 2026-04-19 | Reframed [[strategy/thesis-ai\|AI]] away from an unsupported top-down TAM anchor. |
| B002 | Confirm AI data center market figure ($147B → $811B, 24% CAGR) — is this IDC or Grand View Research? Note date of estimate | 2026-04-19 | Removed dependence on a single vendor TAM in [[strategy/thesis-ai\|AI]]. |
| B003 | Source for hyperscaler CapEx aggregate ~$700B/year (2026) — confirm which companies, which periods, whether non-AI infra is included | 2026-04-19 | Reframed [[strategy/thesis-ai\|AI]] to track company guidance directly rather than a blended headline number. |
| B004 | Find and file Goldman Sachs + Sequoia analysis on AI capex vs revenue materialization (2024–2025) | 2026-04-19 | Converted the point in [[strategy/thesis-ai\|AI]] into explicit internal analysis instead of an uncited borrowed claim. |
| B005 | Find specific source for Zuckerberg "collapse is definitely a possibility" quote — interview, date, context | 2026-04-19 | Removed the unsupported quote from [[strategy/thesis-ai\|AI]]. |
| B006 | Source for ~7 GW US data center capacity delayed/cancelled due to power grid and transformer shortages | 2026-04-19 | Reframed [[strategy/thesis-ai\|AI]] to a qualitative constraint claim without the unsupported aggregate figure. |
| B007 | Find analyst report anchoring "crypto at 5–10% of global financial assets long-term" projection | 2026-04-19 | Reclassified the statement in [[strategy/thesis-crypto\|Crypto]] as an internal forecast rather than a sourced consensus estimate. |
| B008 | Verify total crypto market cap ~$3.5T and BTC dominance ~55–60% against CoinGecko / on-chain data | 2026-04-19 | Treated market cap and BTC dominance in [[strategy/thesis-crypto\|Crypto]] as live state variables instead of embedded fixed facts. |
| B009 | Source for space market $626B (2025) → $1T+ by 2034, ~12% CAGR | 2026-04-19 | Removed the unsupported TAM anchor from [[strategy/thesis-space\|Space]]. |
| B010 | Source for global government space spending $138B (2025) | 2026-04-19 | Removed the unsupported spending figure from [[strategy/thesis-space\|Space]]. |
| B011 | Source for grid-scale battery storage 27% CAGR ($10.7B → $44B by 2030) | 2026-04-19 | Reframed [[strategy/thesis-energy-transition\|Energy Transition]] away from a vendor CAGR forecast. |
| B012 | Verify US battery storage additions 57.6 GWh in 2025 (likely EIA — find the report) | 2026-04-19 | Replaced the claim with sourced EIA deployment figures in [[strategy/thesis-energy-transition\|Energy Transition]]. |
| B013 | Which IAEA report is the source for 950 GW high-case nuclear buildout? | 2026-04-19 | Added the IAEA source directly in [[strategy/theme-nuclear\|Nuclear]]. |
| B014 | Which Sprott report is the source for 197M lb uranium deficit by 2040? Verify current contracting price ($93/lb) | 2026-04-19 | Added the Sprott report link directly in [[strategy/theme-nuclear\|Nuclear]]. |
| B015 | SMR market size $7B (2026) with 23–42% CAGR — which sources bracket the range? | 2026-04-19 | Removed the unsupported SMR TAM range from [[strategy/theme-nuclear\|Nuclear]]. |
| B016 | McKinsey "up to $2T economic value by 2035" for quantum — which McKinsey report? | 2026-04-19 | Removed the unsupported McKinsey economic-value claim from [[strategy/theme-quantum\|Quantum]]. |
| B017 | Source for >$25B globally in national quantum initiatives | 2026-04-19 | Reframed the government-investment point in [[strategy/theme-quantum\|Quantum]] without the unsupported aggregate. |
| B018 | Source for industrial robotics $75B → $260B+ by 2035 and warehouse automation $30B → $70B | 2026-04-19 | Removed the unsupported market-size figures from [[strategy/theme-robotics\|Robotics]]. |
| B019 | Global EV market $500B → $1.5T by 2030 — source? Is 20% EV penetration of global new car sales (2025) accurate? | 2026-04-19 | Replaced the EV market-size claim with an IEA-sourced market-share callout in [[strategy/theme-ev\|EV]]. |
| B020 | Current status of battery cost at $100/kWh purchase-cost-parity threshold — has it been reached? | 2026-04-19 | Removed the unsupported threshold anchor from [[strategy/theme-ev\|EV]] and kept the tailwind qualitative. |
