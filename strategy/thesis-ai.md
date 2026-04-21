---
date: 2026-04-18
last_updated: 2026-04-21
type: strategy
status: active
tags: [thesis, ai, compute, data-center, semiconductors, gpu]
---

# AI Thesis

> Themes within this thesis: [[strategy/theme-quantum|Quantum]], [[strategy/theme-robotics|Robotics]]

## Thesis

AI is the biggest capex cycle since the internet buildout. Demand for compute, advanced packaging, power, and data center infrastructure vastly exceeds supply and will persist for years.

This thesis has three expressions:
1. **Infrastructure** — GPU cloud compute (NBIS), chip packaging (AMKR), power semiconductors (NVTS), AI data centers (IREN, APLD). The picks-and-shovels of the AI buildout.
2. **Robotics** ([[strategy/theme-robotics]]) — AI-powered autonomous physical systems replacing manual processes. Warehouse automation (SYM) and surgical robotics (ISRG).
3. **Quantum computing** ([[strategy/theme-quantum]]) — a longer-term compute paradigm that could eventually complement or surpass classical AI hardware. Trapped ion (IONQ) and neutral atom (INFQ) approaches. More speculative, but a small asymmetric bet on the next compute frontier.

## Variant View

- **Market view**: the AI trade is crowded, and a capex/ROI mismatch could turn the infrastructure layer into an overbuild.
- **My view**: the better edge is not "AI wins" broadly; it is owning constrained bottlenecks while cutting the weakest expressions quickly if capex demand cracks.
- **Why this matters**: AMKR and power/data-center names should be judged by bottleneck durability and customer commitments, not by generic AI sentiment.

## Market Size

> [!analysis] I am not anchoring this thesis on a single AI infrastructure TAM.
> Definitions diverge across accelerated compute, AI data centers, and broader digital infrastructure, so the thesis rests on observable supply constraints and customer spending behavior rather than one top-down forecast.

> [!analysis] Hyperscaler spending is clearly rising, but any aggregate headline depends on which companies, time periods, and financing commitments are included.
> I will track company filings and guidance updates, not a single blended "market number."

> [!analysis] Advanced packaging remains a real bottleneck.
> TSMC capacity expansion is helping, but packaging and power infrastructure still constrain how fast AI capacity can come online.

## Secular Tailwinds

1. **Compute demand exceeds supply** — capacity sold out through 2026 for most providers
2. **Advanced packaging bottleneck** — TSMC CoWoS is the primary constraint on AI chip supply
3. **Enterprise AI adoption still early** — 21% of S&P 500 cite AI benefits; inference will sustain demand after training buildout
4. **Power consumption rising 165%** (Goldman Sachs) — rack densities moving to 100kW+
5. **U.S. reshoring** — CHIPS Act creating domestic semiconductor manufacturing demand
6. **Power constraints as moat** — grid interconnection delays of years; only ~10% of planned projects past pre-execution

## Major Risks

- **Overbuild / bubble risk**
  > [!analysis] Hyperscaler AI spend is now large enough that a mismatch between capex and monetization would matter at the macro level.
  > The relevant question is not a precise spend total; it is whether revenue and enterprise ROI catch up before capacity overshoots.

  **Trigger criteria**: If any two of the following occur simultaneously, begin reducing AI infrastructure exposure (IREN, APLD, NVTS first; AMKR, NBIS held longer):
  - Aggregate hyperscaler capex guidance cuts >20% from current levels
  - A major AI cloud provider (CoreWeave, Lambda, or equivalent) restructuring or defaulting
  - GPU spot pricing declining >30% from peak for more than one quarter
- **ROI uncertainty**
  > [!analysis] This remains the core unresolved question of the thesis.
  > If enterprise AI monetization keeps lagging infrastructure spend, the lower-quality names in this basket should re-rate first.
- **Physical constraints**
  > [!analysis] Power, transformer, and interconnection constraints are already slowing some U.S. data center projects.
  > I am not carrying a single aggregate gigawatt figure here because I do not have one authoritative source on file.
- **Interest rate sensitivity** — these are capital-intensive businesses with heavy debt loads. Standard sensitivity, no specific figure.

## Active Positions

| Ticker | Layer | Role | Conviction |
|--------|-------|------|-----------|
| [[holdings/NBIS]] | Compute cloud | GPU infrastructure (demand-side) | 3 |
| [[holdings/AMKR]] | Packaging | Advanced chip assembly (supply enabler) | 3 |
| [[holdings/MU]] | Memory | HBM demand for AI training/inference (cyclical) | 2 |
| [[holdings/IREN]] | Data center | AI cloud, renewable-powered | 3 |
| [[holdings/APLD]] | Data center | AI data center leasing | 3 |
| [[holdings/NVTS]] | Power | GaN/SiC power semiconductors | 2 |

## Key Position Details

**NBIS**: AI-native cloud operator with unusually large customer concentration in a small number of hyperscaler-scale relationships. The opportunity is real, but so is the risk that capex outruns durable demand.

**AMKR**: The cleanest way in this basket to express the packaging bottleneck without taking direct GPU demand risk. The thesis is structural capacity tightness, not short-term AI sentiment.

**MU**: Memory exposure sits here because the bet is cyclical AI demand and HBM tightness, not the kind of durable platform lock-in that defines the tech-conviction names.

**IREN**: Higher-risk operating pivot from bitcoin mining into AI infrastructure. The attraction is access to power; the risk is dilution and the difficulty of proving this is more than a narrative rerating.

**APLD**: More real-estate-like than IREN. The core thesis is that scarce powered capacity becomes valuable enough to support landlord economics, but leverage and execution still matter.

**NVTS**: The most fragile position in the set. The NVIDIA tie-up keeps the thesis alive, but until AI-data-center revenue shows up in the numbers this remains a narrative-heavy speculation rather than a fundamentals-backed hold.

## Allocation / Sizing

- **Target**: part of the 5% thematic allocation, with room to grow only while AI infrastructure signals remain healthy
- **Current**: ~$3,270 / 0.7% for the core AI infrastructure basket; related Quantum and Robotics exposures sit in separate theme docs
- **Operating band**: 0.5-2.0% for the AI infrastructure basket before explicit reauthorization
- **Max thesis weight**: 2.5% for AI infrastructure alone; broader AI-linked exposure is monitored in the cross-thesis map
- **Max single-name weight**: 1.0% for speculative infrastructure names; AMKR can scale larger only if packaging evidence remains strong
- **Speculative / pre-revenue cap**: 0.5% for NVTS until material AI data center revenue appears
- **DCA posture**: continue small DCA while H1-H3 remain open/intact; freeze weakest names first if capex signals deteriorate

## Decision Rules

These are operating rules, not automatic orders. Any material action still gets a decision note.

| Condition | Action |
|-----------|--------|
| Hyperscaler capex guidance remains strong and AI basket below 2% | Continue small DCA, with AMKR/NBIS prioritized over weaker narrative names |
| Two overbuild triggers occur at once | Reduce AI infrastructure exposure, starting with NVTS, IREN, and APLD |
| NVTS reports >$10M quarterly AI data center revenue | Permit continued DCA up to speculative cap; reassess conviction after margin/customer quality is known |
| NVTS fails H3 by Q4 2026 | Stop DCA and decide whether to exit or keep tracking-size exposure |
| AMKR advanced packaging growth disconfirms | Stop treating packaging as a durable bottleneck; review AMKR sizing |
| AI infrastructure basket exceeds 2.5% without new evidence | Pause DCA and redirect new cash to core or other underweight theses |

## Bull / Base / Bear Cases

| Case | What Happens | Portfolio Action |
|------|--------------|------------------|
| Bull | Hyperscaler capex stays high, packaging/power bottlenecks persist, and revenue converts into signed customer commitments | Let AMKR/NBIS scale within limits; keep speculative names capped until revenue proves out |
| Base | AI buildout continues but ROI evidence is uneven; bottlenecks remain real but valuations stay volatile | Maintain diversified small basket; prefer proven bottlenecks over narrative-heavy names |
| Bear | Capex guidance cuts, AI cloud distress, or GPU pricing collapse signal overbuild | Freeze DCA, cut weakest infrastructure positions first, and review all AI-linked theses together |

## Monitoring Signals

- **Hyperscaler capex** — Amazon, Microsoft, Google, and Meta guidance and commentary
- **GPU market pricing** — spot/rental pricing, availability, and backlog commentary
- **AI cloud credit quality** — customer concentration, financing terms, restructuring/default signals
- **Packaging bottleneck** — AMKR advanced packaging revenue and TSMC CoWoS/SoIC capacity signals
- **Data center economics** — signed leases, power availability, debt/dilution, and customer commitments at IREN/APLD
- **Power semiconductor proof** — NVTS AI data center revenue, not design-win headlines alone

## Hypotheses

| # | Hypothesis | Basis / Source | Date Made | Timeframe | If Confirmed → | If Disconfirmed → | Status | Evaluated |
|---|-----------|----------------|:---------:|-----------|----------------|-------------------|:------:|:---------:|
| H1 | Aggregate hyperscaler capex guidance (Amazon + Microsoft + Google + Meta) stays ≥$600B for 2026 across their earnings calls | 2025 capex guidance aggregates; structural AI demand thesis | 2026-04-19 | Q2–Q4 2026 earnings | AI capex supercycle intact; maintain infrastructure positions | >20% aggregate guidance cut signals demand pull-forward; review thesis | open | — |
| H2 | AMKR advanced packaging revenue (CoWoS/SoIC) grows >20% YoY in FY2026 | TSMC capacity expansion schedule; structural bottleneck thesis | 2026-04-19 | Feb 2027 (FY2026 earnings) | Packaging bottleneck thesis validates; AMKR positioned correctly | Bottleneck relieved faster than expected; review AMKR sizing | open | — |
| H3 | NVTS reports first quarter of material AI data center revenue (>$10M) by end of 2026 | NVIDIA MGX design win announcement; power delivery thesis | 2026-04-19 | Q4 2026 earnings | Power semiconductor thesis materializing; add to position | Revenue aspirational not real; consider exit | open | — |
| H4 | A major analyst house (Goldman, McKinsey) publishes evidence of measurable AI ROI in enterprise (not just productivity estimates) by end of 2027 | Goldman Sachs / Sequoia "where's the ROI" question; enterprise adoption narrative | 2026-04-19 | Dec 2027 | AI demand sustains beyond training buildout; long-term thesis strengthens | Capex bubble concern validated; revisit thesis and sizing | open | — |

## Open Research Questions

- [ ] Will AI capex ROI materialize before bubble concern overwhelms the thesis? What's the leading indicator to watch? → see [[docs/research-backlog|B004]]
- [ ] Is the advanced packaging (CoWoS) bottleneck structural through 2028, or does TSMC capacity expansion relieve it sooner?
- [ ] Does NVTS earn its allocation? Revenue is still aspirational — at what point is the position a hold vs. an exit?

## Updates

### 2026-04-18 — Created AI thesis
Merged former AI/Compute and AI/Infrastructure theme files into a single thesis. NBIS and AMKR cover the compute/packaging layer. IREN and APLD cover the data center layer. NVTS covers the power delivery layer. The thesis spans the full AI infrastructure stack from chips to buildings.
