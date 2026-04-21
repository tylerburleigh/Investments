---
date: 2026-04-18
last_updated: 2026-04-21
type: strategy
status: active
parent_thesis: "[[strategy/thesis-ai]]"
tags: [thematic, quantum-computing, trapped-ion, neutral-atom]
---

# Quantum Computing Theme

> Theme within: [[strategy/thesis-ai]]

## Thesis

Quantum computing is transitioning from lab curiosity to early commercialization — the sector resembles AI in 2018. Real progress is happening (fault-tolerant logical qubits demonstrated), massive long-term potential exists, but timelines are uncertain and valuations are extreme. The key inflection: fault-tolerant quantum computing (FTQC) expected 2028-2030, with commercially useful quantum advantage potentially 2027-2030. This is a small, asymmetric bet on a transformative technology.

## Variant View

- **Market view**: quantum timelines are too uncertain and valuations already price in breakthroughs that may be a decade away.
- **My view**: tiny exposure is justified only as an option on credible fault-tolerance progress, not as a normal growth-stock allocation.
- **Why this matters**: IONQ/INFQ should remain capped until logical-qubit progress, commercial advantage, and revenue mix improve together.

## Market Size

> [!analysis] I am not anchoring this theme on any single near-term quantum TAM.
> Commercial timelines remain too uncertain, and the gap between "economic value" and direct vendor revenue is too large to treat headline market-size numbers as hard evidence.

## Secular Tailwinds

1. **Government investment** — governments are committing billions globally, and DARPA is explicitly targeting utility-scale quantum capability on a defined timeline
2. **AI convergence** — quantum-classical hybrid architectures; NVIDIA building infrastructure bridge (CUDA-Q, DGX Quantum)
3. **Defense/security demand** — post-quantum cryptography migration, quantum sensing, secure networking
4. **Cloud access** — AWS Braket, Azure Quantum, Google Cloud lowering adoption friction

## Major Risks

- **Timeline uncertainty (biggest risk)** — Jensen Huang: useful quantum is 15-30 years away; others say 3 years. Massive range
- **Error correction** — physical-to-logical qubit ratio still very high; IBM revised roadmap after more errors at scale
- **Classical competition** — GPUs keep improving; quantum advantage likely domain-specific, not universal
- **Extreme valuations** — IONQ at 71x P/S, INFQ at 109x P/S; Oct 2025 Huang crash showed how fast these reprice
- **Dilution** — all unprofitable; IonQ burning cash aggressively via M&A
- **Winner-take-most** — 5+ qubit technologies, dozens of companies; most won't survive independently

## Quantum Approach Comparison

| Approach | Leaders | Advantage | Limitation | Scale (2026) |
|----------|---------|-----------|------------|-------------|
| Trapped Ion | IONQ, Quantinuum | Highest fidelity (99.99%), all-to-all connectivity | Slower gates, harder to scale | 36-256 qubits |
| Neutral Atom | INFQ, QuEra, Pasqal | Highly scalable, flexible connectivity | Slower than superconducting | 256-1,225+ qubits |
| Superconducting | IBM, Google | Fastest gates, mature fabrication | Nearest-neighbor only | 100-1,386 qubits |

Current consensus: trapped ion leads in fidelity (most important for fault tolerance); neutral atom leads in scalability. No clear winner — Google pursuing dual-track superconducting + neutral atom.

## Active Positions

| Ticker | Approach | Role | Conviction |
|--------|----------|------|-----------|
| [[holdings/IONQ]] | Trapped ion | Fidelity leader, most advanced commercialization | 3 |
| [[holdings/INFQ]] | Neutral atom | Scalability leader, sensing revenue diversifies | 3 |

## Key Position Details

**IONQ**: The commercialization leader in the theme, but also the company taking the biggest capital-allocation swing. The strategic logic of owning more of the stack is clear; the risk is spending aggressively before the core technology is fully proven at scale.

**INFQ**: Neutral-atom exposure with real sensing revenue, which makes it more grounded operationally but also creates a genuine "is this actually a sensing company?" risk if computing revenue does not ramp.

## Allocation / Sizing

- **Parent allocation**: within [[strategy/thesis-ai]]
- **Current**: ~$180 / <0.1% for Quantum theme positions
- **Operating band**: 0.05-0.5% inside thematic allocation
- **Max theme weight**: 0.75% without explicit reauthorization
- **Max single-name weight**: 0.4% per quantum name until commercial evidence improves
- **Speculative / pre-revenue cap**: both IONQ and INFQ stay capped because valuation depends on future technical milestones
- **DCA posture**: keep DCA token-sized; do not scale materially before H1/H3/H4 evidence improves

## Decision Rules

These are operating rules, not automatic orders. Any material action still gets a decision note.

| Condition | Action |
|-----------|--------|
| IONQ logical-qubit progress confirms | Reassess whether IONQ cap can rise modestly |
| IONQ misses logical-qubit roadmap or acquisition integration worsens | Stop DCA and review tracking-size hold |
| Fortune 500 real-world quantum advantage emerges | Review whole theme; consider raising theme cap only after use case quality is clear |
| No real commercial advantage by end of 2027 | Treat timeline as longer than thesis assumed; reduce or freeze exposure |
| INFQ revenue growth and computing mix improve | Maintain small DCA within cap |
| INFQ remains mostly sensing with slowing growth | Stop DCA and reassess whether it fits the quantum-computing thesis |

## Bull / Base / Bear Cases

| Case | What Happens | Portfolio Action |
|------|--------------|------------------|
| Bull | Logical qubits scale, real commercial advantage appears, and revenue growth accelerates | Raise theme cap modestly, still inside venture-style limits |
| Base | Technical progress continues but commercial timing remains uncertain and valuations stay volatile | Maintain token-sized exposure and wait for proof |
| Bear | Timelines extend, acquisitions destroy capital, or classical compute keeps closing the gap | Stop DCA and cut to tracking-size or exit |

## Monitoring Signals

- **Technical progress** — logical qubits, error rates, correction overhead, and peer benchmarks from IBM/Google/Quantinuum
- **Commercial proof** — real business problem solved, not synthetic benchmark advantage
- **Revenue quality** — IONQ bookings/revenue quality and INFQ computing vs. sensing mix
- **Capital allocation** — acquisition integration, cash burn, dilution, and R&D spend discipline
- **Competitive landscape** — trapped ion vs. neutral atom vs. superconducting progress
- **Valuation** — P/S compression/expansion relative to technical evidence

## Hypotheses

| # | Hypothesis | Basis / Source | Date Made | Timeframe | If Confirmed → | If Disconfirmed → | Status | Evaluated |
|---|-----------|----------------|:---------:|-----------|----------------|-------------------|:------:|:---------:|
| H1 | IONQ demonstrates at least 64 logical qubits (error-corrected) in a published result by end of 2027 | IONQ roadmap; fault-tolerant QC expected 2028-2030; logical qubit demonstrations are the key intermediate milestone | 2026-04-19 | Dec 2027 | FTQC timeline on track; thesis validates | Milestone not reached → Jensen Huang's "15-30 years" view gaining credibility; review conviction | open | — |
| H2 | IONQ SkyWater acquisition closes without major regulatory/integration issues by end of 2026 | $1.8B deal announced; US foundry strategy rationale; IONQ cash position | 2026-04-19 | Dec 2026 | In-house fabrication thesis validates; reduces supply chain dependency | Acquisition fails or integration problems emerge → $1.8B capital destroyed; reassess | open | — |
| H3 | A Fortune 500 company publicly announces quantum advantage for a real business problem (not a benchmark) by end of 2027 | IBM, Google, IonQ all have commercial cloud access; NVIDIA CUDA-Q bridge | 2026-04-19 | Dec 2027 | Commercial viability earlier than pessimists expect; raises sector conviction | No commercial advantage demonstrated → classical GPUs remain superior for all practical tasks; reconsider timing of thesis | open | — |
| H4 | INFQ revenue growth re-accelerates to >30% YoY in FY2026 (from 12.6% deceleration in FY2025) | SPAC listing Feb 2026; NASA contracts; NVIDIA partnership; sensing revenue base provides floor | 2026-04-19 | Feb 2027 (FY2026 earnings) | Growth thesis still alive; sensing + computing dual revenue validates | Growth continues to decelerate → computing revenue not materializing; review sizing | open | — |

## Open Research Questions

- [ ] Does trapped ion's fidelity advantage or neutral atom's scalability win the race to fault-tolerant quantum computing?
- [ ] Is the "quantum in 2018" analogy accurate, or is the timeline to commercial advantage fundamentally longer than AI was?
- [ ] Given IONQ's aggressive acquisition strategy, is integration risk now larger than the core technology risk?
- [ ] **Near-term signals to watch**: IONQ 256-qubit system (Q4 2026), INFQ FY2026 revenue composition (computing vs sensing split), any IBM/Google logical qubit publications that set the benchmark IONQ must beat.

## Updates

### 2026-04-18 — Initial theme research
Two positions provide diversification across the two most promising qubit technologies. IONQ is the commercialization leader; INFQ offers scalability + sensing optionality. Both are extremely early-stage bets with eye-watering valuations. Keep position sizes small. Key question: does trapped ion's fidelity advantage or neutral atom's scalability win the race to FTQC?
