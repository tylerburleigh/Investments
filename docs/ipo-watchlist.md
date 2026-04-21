---
date: 2026-04-21
last_updated: 2026-04-21
type: reference
status: active
tags: [ipo, watchlist, process]
---

# IPO Watchlist

Purpose: track IPO candidates only when they are relevant to an existing thesis/theme or could become a real portfolio candidate. This is not a general IPO calendar.

## Relevance Filter

Track an IPO candidate only if at least one applies:

- It maps directly to an active thesis or theme.
- It is a direct competitor, benchmark, or better expression of an existing holding.
- Its listing would materially affect public comps or liquidity for a theme we own.

Do not track:

- Generic SPAC shells unless the target is already thesis-relevant.
- Consumer, REIT, or financial IPOs outside the current strategy unless there is a clear portfolio reason.
- Rumor-only names with no filing, reported confidential filing, or near-term catalyst.

## Workflow

| Stage | Trigger | Action |
|-------|---------|--------|
| Rumor / broad pipeline | Mentioned by reliable source, no filing | Capture in weekly scan only if thesis-relevant. No watchlist note yet. |
| Reported confidential filing or public S-1 | Reputable wire/source or SEC filing | Create `watchlist/{TICKER-OR-SLUG}.md` with entry criteria and related holdings. |
| Terms set / pricing window | Price range, deal size, expected market cap | Add a calendar row for pricing/first-week follow-up. Update key metrics. |
| Trading begins | Public ticker active | Wait for first-week trading, first earnings, and lockup context before any decision note unless valuation is clearly compelling. |
| Post-IPO evidence | First earnings, lockup expiry, material guidance | Promote to holding candidate, keep watching, or close the watchlist note. |

## What To Capture

Every IPO watchlist note should answer:

- Which thesis/theme does this improve, threaten, or benchmark?
- Is it better risk/reward than the current expression we own?
- What valuation is being asked relative to public comps?
- Is revenue recurring, contracted, or speculative?
- What are the cash runway, capex needs, debt, dilution, and lockup risks?
- Are governance, related-party transactions, or dual-class controls material?
- What would make us buy, wait, or close the note?

## Current IPO Candidates

| Candidate | Stage | Thesis / Theme | Tracking Note | Posture |
|-----------|-------|----------------|---------------|---------|
| SpaceX / xAI | Reported confidential filing | [[strategy/thesis-space\|Space]] / [[strategy/thesis-ai\|AI]] | [[watchlist/SPACEX]] | Track public S-1 and structure. Potential portfolio candidate, but do not act before financials and governance are visible. |
| X-Energy | Terms set | [[strategy/theme-nuclear\|Nuclear]] | [[watchlist/XE]] | Track as an SMR benchmark versus OKLO and the broader nuclear basket. Wait for valuation and execution evidence. |
| The Elmet Group | Terms set | AI/space-adjacent industrials | [[watchlist/ELMT]] | Track as a critical-materials/defense supplier. Must prove liquidity, margin quality, and thesis fit. |
| OpenAI | Pipeline only | [[strategy/thesis-ai\|AI]] | No note yet | Create a watchlist note only when a public S-1 or credible filing window appears. |
| Anthropic | Pipeline only | [[strategy/thesis-ai\|AI]] | No note yet | Same rule as OpenAI. Avoid headline tracking until filing evidence exists. |

## Source Priority

| Source | Use |
|--------|-----|
| SEC EDGAR / S-1 | Primary financials, risks, share structure, use of proceeds |
| Company investor relations | Prospectus links, official roadshow materials, first earnings |
| Renaissance Capital / Nasdaq IPO calendar | Calendar, terms, deal size, pricing window |
| Reuters / Bloomberg | Confidential filing reports and banker/source-based pipeline context |
| Commentary / social media | Narrative only; do not use for investment criteria without primary support |
