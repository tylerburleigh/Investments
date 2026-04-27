---
date: "{{date}}"
last_updated: "{{date}}"
type: review
period: ""  # weekly, monthly, quarterly
status: active
tags: [review]
---

# {{period}} Review — {{date}}

## Portfolio Performance

| Metric | Start | End | Change |
|--------|-------|-----|--------|
| Total Value | | | |
| S&P 500 | | | |
| Benchmark Delta | | | |

## Allocation Drift
<!-- Compare current allocation to target. Where are you overweight/underweight? -->

## Scan Summary
<!-- Wikilink the scan(s) that informed this review. Weekly: latest scan. Monthly: all scans in the period. -->

**Scan(s):** [[scans/YYYY-MM-DD]]

## Decisions This Period
<!-- Link to all decisions made since the last review: [[decisions/...]] -->

## Winners & Losers

### Top Performers
| Ticker | Return | Why? |
|--------|--------|------|
| | | |

### Worst Performers
| Ticker | Return | Why? |
|--------|--------|------|
| | | |

## Thesis Health
<!-- For monthly/quarterly: any holdings where the thesis has weakened, changed, or needs revisiting?
     Flag if conviction should be revised up or down. -->

## Bear Case / Disconfirming Evidence
<!-- Required counterweight. What evidence this period weakens the current portfolio narrative?
     Include "none found" only after naming the areas checked. Convert real thesis-breaking items into action items, kill-criteria reviews, or decisions. -->

## Lint Agenda (monthly+)
<!-- Run: python3 scripts/lint.py --write-index
     Paste staleness warnings and unresolved-holding warnings here to drive the agenda. -->

<!-- Dataview queries below render as live tables in Obsidian. Agent: use lint.py output instead. -->

### Holdings not updated in 90+ days
```dataview
TABLE ticker, conviction, last_updated AS "Updated"
FROM "holdings"
WHERE type = "holding" AND file.name != "index"
AND date(today) - date(last_updated) > dur(90 days)
SORT last_updated ASC
```

### Open hypothesis checkboxes
```dataview
TASK
FROM "strategy"
WHERE !completed
```

## Open Questions Carry-Forward
<!-- Unresolved questions from Investment Strategy.md or prior reviews that are still open. -->

## Action Items
- [ ]

## Thoughts
<!-- General reflections, market observations, strategy adjustments -->
