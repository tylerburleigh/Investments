---
name: review
description: Run a structured periodic review (weekly, monthly, or quarterly). Orchestrates the full review workflow — pull data, validate structure, work through checklist, write the review note. Use when the user says "run a weekly review", "time for the monthly review", "let's do the quarterly", or when briefing.py flags an overdue review.
---

# /review

Run a structured portfolio review. The depth depends on the period.

## Step 1 — Determine period and scope

Ask the user which period (weekly, monthly, quarterly) if not specified. Use the one that briefing.py flagged as overdue if ambiguous.

| Period | Depth | Time | When |
|--------|-------|------|------|
| Weekly | Light | 15–30 min | Every 7 days |
| Monthly | Full | 2–4 hrs | Start of each calendar month |
| Quarterly | Deep | Half day | Start of each quarter (Jan, Apr, Jul, Oct) |

## Step 2 — Pre-work (all periods)

Run these before writing anything:

1. **Lint:** `python3 scripts/lint.py --write-index`
   - Errors: fix before continuing
   - Warnings: note them for the review agenda
2. **Pull live data (if user approves):** call `mcp__snaptrade__list_positions`
   - Run `scripts/snapshot.py` to create today's snapshot (if none exists)
   - Run `scripts/portfolio_diff.py` to diff against last snapshot
3. **Read context:** `strategy/Investment Strategy.md` and `docs/session-log.md` (last 2–3 entries)
4. **Read latest scan:** if a scan exists from the past 7 days in `scans/`, read it. If not, recommend running `/weekly-scan` first (or run it as part of the review).

## Step 3 — Period-specific checks

### Weekly (light)

- [ ] Report portfolio value and change since last snapshot
- [ ] Flag any positions that moved >10% in the past week
- [ ] Read the latest scan artifact (`scans/YYYY-MM-DD.md`). Note any hypothesis triggers or directional signals.
- [ ] Scan `decisions/log.md` for any new decisions or actions since last review
- [ ] Ask: any action needed?

### Monthly (full)

All weekly checks, plus:

- [ ] **Allocation drift:** compare actual allocation (from snapshot) vs targets in Investment Strategy. Compute percentages.
- [ ] **Staleness tour:** work through lint staleness warnings. Update any holding or thesis docs that are stale.
- [ ] **Backlog review:** read `docs/research-backlog.md`. Resolve 1–3 items using `/research` or push dates with a note.
- [ ] **Scan sweep:** read all scans from the prior month. For each thesis with accumulated directional signals, synthesize into a dated `## Updates` entry in the thesis doc.
- [ ] **Hypothesis check:** read each thesis doc's `## Hypotheses` table. Evaluate any whose timeframes have passed. Update Status, Evaluated date, and append reasoning to `## Updates`.
- [ ] **Decision audit:** surface all `status: active` decisions older than 30 days. Ask the user whether each should be closed or revisited.
- [ ] **Research questions:** check `- [ ]` items in each thesis doc's `## Open Research Questions`. Promote any that have become urgent to the backlog.

### Quarterly (deep)

All monthly checks, plus:

- [ ] **Full thesis re-read:** re-read every thesis and theme doc end-to-end. Ask: does this thesis still hold? Has conviction changed?
- [ ] **Cross-thesis consistency:** flag positions that appear in multiple theses with different conviction levels. Reconcile.
- [ ] **Conviction review:** for each position, ask whether conviction should change. Update the holdings file and thesis table.
- [ ] **Strategy refresh:** re-read `Investment Strategy.md`. Are allocation targets still right? Are there new open questions?
- [ ] **Event calendar update:** add or remove items from `docs/calendar.md` based on thesis changes.
- [ ] **Methodology review:** is the trusted sources list in `docs/research-methodology.md` still accurate? Any new sources to add?
- [ ] **Remaining scan sweep:** promote any unprocessed directional signals from the quarter's scans into thesis docs.

## Step 4 — Write the review note

Create `reviews/YYYY-MM-DD-{period}.md` from the review template. Fill in all sections. Link to decisions, snapshots, and scans. Record action items with `- [ ]` checkboxes.

## Step 5 — Post-work

1. **Update session log:** append to `docs/session-log.md` with what was covered and what was deferred.
2. **Bump `last_updated`** on any docs that were touched during the review.
3. **Report:** summarize key findings and action items to the user.

Note: Reviews are self-documenting — the review file in `reviews/` is the permanent record. No entry in `decisions/log.md` is needed (only portfolio actions go in the log).

## Constraints

- Don't pull SnapTrade data unless the user approves (it's opt-in per CLAUDE.md).
- Don't change conviction levels without asking the user — surface findings, let them decide.
- Don't create holdings files during the review unless the user explicitly asks — just flag them as pending.
- Fix lint errors before proceeding with the review content. Errors mean broken structure.
