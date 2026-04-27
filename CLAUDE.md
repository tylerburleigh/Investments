# Investment Research Vault

## What This Is

A personal investment research system connected to WealthSimple via SnapTrade. The vault serves two purposes equally: **building expertise over time** and **making better decisions**. Research feeds decisions; decisions drive what to research next.

## Investor Profile

Barbell strategy: low-cost ESG-indexed core with concentrated conviction bets. Heavy crypto allocation as the primary active position. Small asymmetric bets on emerging themes (space, nuclear, quantum, AI infra). Some large-cap tech conviction names. Canadian dividend/value tilt.

## Tax & Account Constraints

Canadian resident, US taxpayer, investing through Canadian brokerage (WealthSimple). This imposes significant restrictions:
- **Non-registered accounts**: US equities and US-listed ETFs only (Canadian securities trigger PFIC reporting complications)
- **Registered accounts**: RRSP available (US-taxpayer-friendly), TFSA not available (US taxes it as a foreign trust)
- Both registered and non-registered accounts are in use
- SnapTrade currently connected to: WealthSimple Trade non-registered account (CAD)

Account connected via SnapTrade MCP (read-only). Trading since 2022.

## How to Work Here

### Data Flow
1. SnapTrade MCP provides live position data (`list_positions`, `list_accounts`, `list_connections`)
2. Python library at `scripts/lib/` parses and analyzes that data
3. Analysis feeds into markdown notes in the vault

### Scripts

| Script | Who runs it | Purpose |
|--------|------------|---------|
| `python3 scripts/briefing.py` | Agent (session start) | Compact session summary: review cadence, staleness, hypotheses due, backlog, last snapshot, upcoming events |
| `python3 scripts/lint.py --write-index` | Agent (monthly review) | Full structural validation + regenerate holdings/index.md |
| `python3 scripts/backlog_sync.py` | Agent (weekly/monthly) | Sync [!gap]/[!unverified] callouts to research backlog; `--apply` to write new entries |
| `python3 scripts/snapshot.py <mcp_json> --output portfolio/YYYY-MM-DD.md` | Agent (after SnapTrade pull) | Generate snapshot markdown + JSON sidecar |
| `python3 scripts/portfolio_diff.py <current.json>` | Agent (after SnapTrade pull) | Diff current positions against last snapshot |
| `python3 scripts/allocation_drift.py` | Agent (during reviews) | Compare actual allocation vs targets from Investment Strategy |

`briefing.py` is the **first thing the agent runs at every session start** (local files only, no SnapTrade). It surfaces what needs attention before any other work begins.

### When Starting a Session

Run `python3 scripts/briefing.py` first. It performs all local-file checks and produces a structured summary. Report the output to the user and ask what they'd like to work on.

**What briefing.py checks (local files only, no SnapTrade):**
- **Reviews:** last weekly/monthly/quarterly, flag if overdue
- **Staleness:** living documents against thresholds (holdings 90d, theses/themes 180d, Investment Strategy 30d)
- **Hypotheses due:** open hypotheses whose timeframe has passed — need evaluation
- **Research backlog:** overdue items (past their Review By date)
- **Snapshot:** age of last portfolio snapshot
- **Session log:** when the last session was and what was deferred
- **Upcoming events:** calendar events in the next 30 days
- **Snapshot:** age of last portfolio snapshot
- **Missing holdings files:** tickers in thesis docs without a `holdings/TICKER.md`

**SnapTrade is opt-in.** Only pull live data when the user asks to review their portfolio, make a decision, or explicitly requests a position refresh. When pulling, create a snapshot if one doesn't exist for today.

**Working with SnapTrade MCP data:** When `mcp__snaptrade__list_positions` returns data, it arrives as `[{type: "text", text: "<json>"}]` where each `text` is a JSON string for one position with nested dicts (`symbol.symbol.symbol` for ticker, `currency.code` for currency). **Do not parse this manually.** Use the existing library:

```python
from lib.snaptrade import parse_positions, load_from_file
from lib.models import Position

# From MCP result (list of dicts):
positions = parse_positions(raw_mcp_result)

# From saved MCP tool result file:
snapshot = load_from_file("/path/to/tool-result-file.txt")
```

Each `Position` has `.ticker`, `.units`, `.price`, `.average_cost`, `.market_value`, `.currency`, `.unrealized_pnl`, `.return_pct`. See `scripts/lib/models.py` for full API.

For diffing against a prior snapshot: `python3 scripts/portfolio_diff.py <mcp_result_file>` (value-level, >5% threshold). For DCA verification (unit-level comparison against daily targets), compare `Position.units` against the prior snapshot's units — `portfolio_diff.py` doesn't do unit-level diffs.

### Ending a Session

Before closing, append an entry to `docs/session-log.md`:
```
### [YYYY-MM-DD] session | short description
- Worked on: what was accomplished
- Deferred: what was explicitly left for later
- Notes: anything a future session should know
```

### Making Decisions
- Every buy/sell/hold action gets a decision note in `decisions/`
- Must include: thesis, conviction level, what would change your mind
- Link to the snapshot that informed it

### Periodic Reviews
- Weekly/monthly/quarterly reviews in `reviews/`
- Compare allocation to targets, track thesis changes, note winners/losers
- Flag drift (e.g., a thematic position that grew beyond intended sizing)
- **Run lint at the start of each monthly review:** `python3 scripts/lint.py --write-index`
  - Errors mean broken structure — fix before continuing the review
  - Warnings drive the agenda: staleness flags identify holdings/theses to revisit, "unresolved (pending holding)" warnings prioritize which holdings files to promote
  - The regenerated `holdings/index.md` gives a snapshot of every position with conviction, decision count, and days-stale

## Folder Structure

- `holdings/` — Research per ticker (`TICKER.md`)
- `portfolio/` — Snapshots (`YYYY-MM-DD.md`)
- `decisions/` — Decision journal (`YYYY-MM-DD-{ticker-or-slug}.md`)
- `strategy/` — Principles, theses, themes, allocation targets
- `watchlist/` — Monitored but not held (`TICKER.md`)
- `reviews/` — Periodic reviews (`YYYY-MM-DD-{weekly|monthly|quarterly}.md`)
- `scans/` — Weekly scan artifacts (`YYYY-MM-DD.md`)
- `docs/` — Reference material, research write-ups, analysis artifacts
- `docs/snaptrade/` — SnapTrade reference
- `scripts/` — Python tools (library in `scripts/lib/`)
- `templates/` — Obsidian templates
- `bases/` — Obsidian Bases files (live database views; open in Obsidian)

### `strategy/` taxonomy

Strategy uses flat filename prefixes, not subfolders:

- `Investment Strategy.md` — hub note with allocation targets, capital flows, open questions
- `thesis-{name}.md` — top-level conviction buckets tied to allocation targets (e.g., `thesis-crypto`, `thesis-ai`). Each thesis is a pillar of the barbell.
- `theme-{name}.md` — narrower bets. Can be a sub-expression of a thesis (via `parent_thesis` frontmatter, e.g., `theme-nuclear` under `thesis-energy-transition`) or a standalone thematic bet (e.g., `theme-quantum`, `theme-robotics` — kept as themes rather than theses because they're smaller, more speculative, and don't warrant their own allocation target).

**Thesis vs. theme test:** does it have its own allocation target in `Investment Strategy.md`? If yes → thesis. If no → theme.

## Conventions

### Position categories

Every position falls into one of four categories. The category determines sizing, DCA approach, and when/whether it's reviewed actively:

- **Core** — low-cost broad-market ETFs (ESGV, VOO, VXUS, VIU.TO, VCN.TO, etc.). The stable end of the barbell. Set-and-forget DCA. Not per-ticker researched.
- **Conviction** — large-cap individual stocks held for long-term compounding (NVDA, META, GOOG, MSFT, AMD, TSM). Dominant platforms with durable moats. Would hold through normal cycles. Typically conviction 4-5.
- **Thematic** — asymmetric bets on emerging themes (space, nuclear, quantum, robotics, energy transition, EV). Smaller positions, venture-style in nature but conviction-scaled. Tied to a `thesis-*` or `theme-*` document.
- **Crypto** — its own category because of size and distinct thesis (on-chain money, financial system evolution). BTC, ETH, IBIT.

Decisions, holdings, and reviews should be explicit about which category a position is in, since the rules differ.

### Conviction scale (1-5)

Used in holdings frontmatter, decision frontmatter, and thesis-doc position tables. **5 = highest conviction.**

- **5** — Would increase position on any dip. Thesis is core to the portfolio.
- **4** — High conviction long-term hold. Standard DCA, no trimming unless allocation drift forces it.
- **3** — Thesis holds but sizing is venture-style. Will let the winners emerge; small individual positions are fine.
- **2** — Watching-to-exit. Thesis weakening or overtaken by a better expression of the same idea.
- **1** — Exit candidate. In the portfolio for legacy reasons or pending a clean exit.

### Frontmatter

Every note uses YAML frontmatter. Shared fields:

- `date` — creation date (YYYY-MM-DD)
- `type` — one of: `holding`, `decision`, `snapshot`, `review`, `scan`, `watchlist`, `strategy`, `reference`
- `status` — `active` | `watching` | `closed` (meanings vary by type; see below)
- `tags` — free-form list
- `last_updated` — last meaningful edit (YYYY-MM-DD). Optional on short-lived docs, **required on living documents** (holdings, strategy, theses, themes)

Type-specific fields:

- **Holdings** (`type: holding`): `ticker`, `sector`, `theme`, `conviction` (1-5), `time_horizon` (short|medium|long). `status: active|watching|closed`.
- **Decisions** (`type: decision`): `ticker` (single ticker string OR YAML list for multi-ticker decisions; omit or use descriptive slug only when there is genuinely no ticker), `action` (buy|sell|hold|trim|add|pause-dca|rebalance|...), `conviction` (1-5), `time_horizon`. `status: active` until the decision is revisited, then `closed`.
- **Snapshots** (`type: snapshot`): `total_value`, `position_count` or `accounts`.
- **Reviews** (`type: review`): `period` (weekly|monthly|quarterly).
- **Watchlist** (`type: watchlist`): `ticker`, `sector`, `theme`, `entry_price`, `target_price`.
- **Strategy** (`type: strategy`): `last_updated` required. Theme files add `parent_thesis: "[[strategy/thesis-xxx]]"` when they sit under a thesis.
- **Reference** (`type: reference`): research write-ups, analysis artifacts, external reference material. Lives in `docs/`.
- **Scans** (`type: scan`): thesis news scan artifacts. Default is a full weekly scan, but a partial scan is allowed mid-cycle for a thesis-relevant development worth logging before the next weekly review. `theses_scanned` (count) should always reflect the actual number of theses/themes checked, and `signals_found` is the count of findings logged. Lives in `scans/`.

### Decision filenames

Pattern: `YYYY-MM-DD-{slug}.md`

- **Single-ticker decisions**: `YYYY-MM-DD-TICKER-action.md` (e.g., `2026-04-18-NVDA-trim.md`)
- **Multi-ticker / thematic decisions**: `YYYY-MM-DD-{descriptive-slug}.md` (e.g., `2026-04-18-crypto-pause-dca.md`, `2026-04-18-thematic-rebalance.md`). The `ticker` frontmatter field should be a YAML list of affected tickers, or omitted if it's a portfolio-wide decision with no meaningful ticker list.

### When to create a holdings file

Don't pre-create 60+ stub files. A `holdings/TICKER.md` exists when at least one of these is true:
- A decision has been made about the ticker (beyond routine DCA)
- The thesis for the position needs its own home (too detailed for a thesis doc)
- The position is flagged for active review or potential exit

Core ETFs generally don't need holdings files — they're covered by `Investment Strategy.md` and don't have per-ticker theses. Conviction names and thematic bets do get files when they start accumulating history.

### Holding notes as living documents
Holding notes (`holdings/TICKER.md`) are not one-time research — they accumulate over time. Structure:
- **Thesis at the top** — evolves as conviction changes
- **Position details table** — refreshed during reviews with current data
- **Updates section with dated entries** — newest on top, each entry is a snapshot of what you believed at that point in time (use `### YYYY-MM-DD — short title` as the sub-heading)
- **`last_updated` in frontmatter** — enables queries like "what hasn't been touched in 3 months?"

The value is in the history: 6 months from now you should be able to see what you thought in April 2026, what changed, and whether the thesis held. Don't overwrite past thinking — append new thinking below it.

### Linking with Obsidian Wikilinks

Use `[[path/filename]]` or `[[path/filename|display text]]` to cross-link notes. Every link creates a backlink — that's how the vault becomes navigable over time.

**Required bidirectional links:**
- **Decision ↔ affected holdings.** Each decision names every affected ticker as `[[holdings/TICKER]]` in its Supporting Research section (when the holding file exists). Each affected holding adds a dated bullet to its `## Decisions` section. The frontmatter `ticker` field is *not* a substitute — wikilinks are.
- **Decision ↔ informing snapshot.** Decisions cite the `[[portfolio/YYYY-MM-DD]]` snapshot that informed them.
- **Decision ↔ relevant thesis.** If a decision concerns a thesis-level question (allocation, thesis validity), it links `[[strategy/thesis-xxx]]`.
- **Review ↔ decisions in period.** Each review lists the decisions made during its window as wikilinks.
- **Holding → thesis.** Each holding links its parent thesis or theme.

**Other conventions:**
- **Link on mention.** If prose mentions a ticker, thesis, theme, or decision, link it — *if* the target file exists. Don't forward-reference files that don't exist (broken links are silent rot).
- **Display text for readability** inside prose: `[[strategy/thesis-crypto|Crypto Thesis]]`. Bare `[[path/file]]` is fine in list items where the path is already navigable.
- **Link hub docs sparingly.** `Investment Strategy.md` shouldn't be linked from every holding — only where the reference is meaningful.
- **When creating a new note, check for reciprocal links.** If A links B, B should usually link A somehow (directly, or via its `## Decisions` / `## Updates` section).

### Updating notes

- **Append for thinking, overwrite for facts.** Position-details tables (shares, cost basis, prices, allocation %) overwrite — they represent the *current* state. Thesis statements, catalyst/risk reasoning, and observations *append* as dated entries under `## Updates`. Never rewrite past thinking in place.
- **`last_updated` bumps only on meaningful edits.** Typo fixes and formatting cleanups don't bump. Thesis revisions, position refreshes during reviews, and Updates-section additions do.
- **Staleness thresholds (surfaced by reviews, not automated):**
  - Holding not touched in **90 days** → flag during the next monthly review.
  - Thesis or theme doc not touched in **180 days** → re-examine during the next quarterly review.
  - `Investment Strategy.md` not touched in **30 days** → likely out of sync with actual capital flows; refresh it.
- **Session protocol:** at session start, pull live positions via SnapTrade and diff against the most recent snapshot. If anything moved meaningfully (new position, closed position, >5% change in a holding's value), log it and update the affected notes.

### Decision recording

Decisions are recorded in **two tiers**. Both exist for a reason — use the right one.

**Tier 1: `decisions/log.md`** — append-only action log. One line per portfolio action. Only `decision` and `action` kinds. Newest on top. Grep-parseable.

```
### [YYYY-MM-DD] {decision|action} | short description — [[link-if-any]]
```

**Tier 2: full decision file in `decisions/`** — use when:
- The action has a thesis worth explaining
- You'll want to revisit the reasoning later
- It involves conviction judgement or changes allocation strategy
- "What would change my mind" is a meaningful question

Skip the decision file (log-only) when:
- Cleanup of a sub-$100 position with no thesis
- Stopping a small DCA you set up experimentally
- Routine operational changes (e.g., switching a recurring buy from CAD to USD)

**What does NOT go in the log:** snapshots (`portfolio/`), reviews (`reviews/`), thesis updates (thesis doc `## Updates`), signals (`scans/`). These are self-documenting — the file itself is the record.

**Strategy and holding docs describe *current state only*.** They don't contain historical annotations like `~~$1,000~~ **PAUSED Apr 2026**` or `Cut Apr 2026`. If history matters, navigate via `decisions/log.md` or the `decisions/` folder. Reviews ingest from the log.

### Information Flow

Raw findings flow from scans through reviews into permanent thesis docs.

**Weekly (capture + light touch):**
- `/weekly-scan` is the default full weekly capture. It writes `scans/YYYY-MM-DD.md` with findings per thesis (hypothesis triggers, directional signals, potential backlog resolutions)
- Partial scans are allowed between weekly reviews when a material thesis-relevant development lands mid-week. A partial scan must say it is not a full weekly pass, set `theses_scanned` to the actual count checked, and include only the thesis sections actually scanned.
- **Hypothesis triggers** (conclusive evidence): immediately update thesis doc — Status + Evaluated in Hypotheses table, dated entry in `## Updates`. The thesis doc is the permanent record.
- **Directional signals**: stay in scan file. No promotion yet. They accumulate for monthly review.
- Every signal includes a source tier (`filing`, `primary/company`, `trade/wire`, `data provider`, `commentary`) and a newness label (`New this week` or `Carried from prior log/review`).
- Add upcoming thesis catalysts surfaced during scanning to `docs/calendar.md`.
- For IPO candidates, use [[docs/ipo-watchlist]] as the relevance filter: only create watchlist notes and calendar events for names tied to an active thesis/theme or plausible portfolio action.
- **Weekly review** wikilinks the relevant scan file(s) (`[[scans/YYYY-MM-DD]]`), does not duplicate findings.
- If a weekly review already exists from the past 7 days and there is no new portfolio snapshot, hypothesis trigger, decision/action, or material thesis-health change, write the scan only and summarize it. Do not create a duplicate weekly review note just to acknowledge a scan.

**Monthly (synthesis):**
- Read all scans from prior month, including any partial scans
- For each thesis with accumulated directional signals, synthesize into a dated `## Updates` entry in the thesis doc
- Evaluate overdue hypotheses (Status change + `## Updates` entry)
- Resolve 1-3 backlog items via `/research`
- Update stale holdings and thesis docs flagged by lint

**Quarterly (full synthesis):**
- Full thesis re-read end-to-end
- Conviction review — update thesis tables and holdings frontmatter if conviction changes
- Promote any remaining unprocessed scan evidence into thesis docs
- Cross-thesis consistency reconciliation
- Strategy refresh (allocation targets, open questions)

**Where things live:**
| Information type | Permanent home | Self-documenting? |
|-----------------|---------------|-------------------|
| Portfolio actions | `decisions/log.md` + `decisions/` files | Log is the index |
| Portfolio state | `portfolio/YYYY-MM-DD.md` + `.json` | Yes |
| Thesis-relevant news | `scans/YYYY-MM-DD.md` | Yes |
| Periodic reviews | `reviews/YYYY-MM-DD-{period}.md` | Yes |
| Thesis knowledge | `strategy/thesis-*.md` and `theme-*.md` `## Updates` | Yes |
| Research resolutions | Thesis doc callouts + `docs/research-backlog.md` | Yes |

### Claim typing (selective)

For factual claims in thesis/theme docs where provenance matters (market sizes, cycle data, competitor share, growth rates), use Obsidian callout syntax to make the epistemic status explicit:

- `> [!source]` — cited from a specific source. Include `[[docs/...]]` or URL.
- `> [!analysis]` — your inference or interpretation, not a source claim. Show the reasoning.
- `> [!unverified]` — an assumption or recalled figure you haven't double-checked.
- `> [!gap]` — something you know you don't know. Flags it for follow-up.

**Apply to:**
- Market-size figures, adoption stats, cycle data, valuation multiples, growth rates
- Competitor claims ("X dominates Y% of the market")
- Any claim a future reader (you, in 6 months) might mistake for a fact vs. a guess

**Don't bother applying to:**
- Decision-file prose (ephemeral, context-rich, dated-by-filename)
- Personal allocation targets or conviction-level statements
- Thesis *framings* ("AI is a capex cycle") — opinions don't need typing

The goal is to catch "I thought I knew this" failures, not to type every sentence.

### Obsidian tooling

Two audiences use this vault differently: **you** browse it in Obsidian; **the agent** reads raw markdown files and runs scripts. The tools below are split accordingly.

**For you (human, Obsidian UI):**

- **Dataview** (community plugin, installed) — `dataview` code blocks in notes render as live tables when you open them in Obsidian. The agent does not use or interpret these blocks; it reads raw files directly. Live views are embedded in `Investment Strategy.md` (holdings by conviction, thesis staleness, recent decisions) and the review template (stale holdings, open hypothesis tasks).
- **Obsidian Bases** — `.base` files in `bases/` open as live filterable database views in Obsidian. Three bases exist: `Holdings.base` (by conviction/status/staleness), `Strategy.base` (thesis/theme staleness), `Decisions.base` (newest-first, active-only). The agent does not use these files.
- **Graph view, backlinks panel, tag pane, outline** — built-in Obsidian navigation. The wikilink structure throughout the vault makes the graph meaningful. The agent traverses links via grep and lint.py rather than the graph.

**For the agent (terminal / session):**

- **lint.py** — run by the agent at the start of each monthly review (`python3 scripts/lint.py --write-index`). Validates structure, surfaces staleness and broken links, regenerates `holdings/index.md`. You read the output; the agent runs it.
- **Obsidian CLI** (not yet registered — Obsidian → Settings → General → Enable CLI) — gives the agent structured query output from the running Obsidian instance. Useful commands once registered:
  - `obsidian tasks path=strategy todo` — all open hypothesis checkboxes across thesis docs
  - `obsidian search:context query="[!gap]" path=strategy` — gap callouts in strategy docs
  - `obsidian backlinks file=thesis-crypto counts` — backlink count as thesis relevance proxy
  - `obsidian diff file=thesis-crypto from=1` — what changed in a thesis since last version

**Shared (both benefit):**

- **Wikilinks** — you navigate them in Obsidian; the agent validates and traverses them via lint.py
- **Frontmatter** — you see the Properties panel; the agent uses frontmatter in Dataview queries and lint checks
- **Callout typing** (`[!source]`, `[!gap]`, etc.) — you see the rendered callout UI; the agent scans for unresolved gaps during lint

### Skills

Three skills are available as slash commands. Use them rather than ad-hoc workflows for these operations.

**`/weekly-scan`** — weekly thesis-relevant news scan. Invoke when:
- The user says "run the weekly scan", "scan for news", "check thesis triggers", or "what happened this week"
- The research methodology weekly cadence is due (see `docs/research-methodology.md`)

The skill reads all active thesis/theme docs, runs targeted Tavily searches per thesis (1-2 each, max 5 results), evaluates results against hypothesis tables and backlog items, surfaces triggers and findings, and writes a dated scan artifact to `scans/YYYY-MM-DD.md`. This is the default full-pass scan workflow; if a single material development needs to be logged between weekly runs, write a partial scan note instead of pretending a full scan was run. See `.claude/skills/weekly-scan/SKILL.md` for the full workflow.

**`/review`** — structured periodic review. Invoke when:
- The user says "run a weekly/monthly/quarterly review" or similar
- `briefing.py` flags an overdue review at session start
- The user asks to review the portfolio, check allocation, or work through thesis health

The skill runs lint, optionally pulls SnapTrade data, walks through a period-specific checklist (deeper for monthly/quarterly than weekly), writes the review note, and logs it. See `.claude/skills/review/SKILL.md` for the full workflow.

For weekly "review and/or scan" requests, scan first. If a weekly review already exists from the past 7 days, create another review note only when new portfolio data, a hypothesis trigger, a decision/action, or a material thesis-health change warrants it.

**`/research`** — resolve a research backlog item. Invoke when:
- The user says "research B001", "resolve item B005", "look into [claim]"
- The user says "work through the backlog" (pick the highest-priority overdue item)
- During a review, a thesis doc has an unverified claim that needs sourcing

The skill reads context from the thesis doc, searches using domain-appropriate trusted sources (per `docs/research-methodology.md`), presents findings before writing, then updates the callout, marks the backlog item resolved, and logs a `thesis-update` entry. See `.claude/skills/research/SKILL.md` for the full workflow.

### Research system

The research system has three components. See `docs/research-methodology.md` for cadence, trusted sources, and methods.

**Research backlog** (`docs/research-backlog.md`) — centralized prioritized list of open questions, unverified claims, and knowledge gaps. Every item has a required `Review By` date. Overdue open items are surfaced by `lint.py` as warnings. Items enter the backlog by:
- Promotion from `[!gap]` or `[!unverified]` callouts in thesis/theme docs
- Open questions from hypothesis evaluation
- Follow-up items surfaced in weekly scans (`scans/YYYY-MM-DD.md`)

Table format:
```
| # | Question | Thesis / Theme | Surfaced From | Priority | Review By | Status |
```
When resolved: change Status to `resolved` and note the link to where the answer landed in the Resolved section.

**Hypothesis tracking** — each thesis and theme doc has a `## Hypotheses` table for pre-registered predictions. The discipline: write the hypothesis *before* the triggering event, evaluate *after*. Every hypothesis requires:
- A unique `#` within the doc (H1, H2, ...)
- A specific, falsifiable prediction
- `Basis / Source` — the reasoning or source that generated the prediction (wikilink, URL, or brief rationale)
- `Date Made` — when the hypothesis was written
- `Timeframe` — when the prediction should be evaluated
- `If Confirmed →` and `If Disconfirmed →` — what each outcome means for conviction
- `Status` — `open` | `confirmed` | `disconfirmed` | `expired`
- `Evaluated` — date the hypothesis was graded (fill in when Status changes from open)

When a hypothesis triggers: update Status + Evaluated in the table, append a dated entry to the thesis doc's `## Updates` section explaining the reasoning. The thesis doc is the permanent record — no separate log entry is needed.

**Signals** — thesis-relevant news findings live in `scans/YYYY-MM-DD.md`, not in `decisions/log.md`. Each signal includes source publication, article date, and directional context. Partial scans are valid when explicitly labeled as partial and scoped to the theses actually checked. See "Information Flow" below for how signals get promoted into thesis docs during reviews.

**Thesis open research questions** — each thesis/theme doc has an `## Open Research Questions` section for strategic questions about thesis validity (not citation gaps, which go in the backlog). Use `- [ ]` checkboxes; check off when answered and note where the answer landed.

**Session continuity** (`docs/session-log.md`) — append-only, one entry per agent session. Newest on top. Each entry records what was worked on, what was deferred, and any notes a future session should know. The agent reads this via `briefing.py` at session start to pick up where the last session left off. At session end, the agent appends a new entry.

**Event calendar** (`docs/calendar.md`) — upcoming catalysts, earnings, and mission milestones linked to the hypotheses they would test. Table format:
```
| Date | Event | Thesis / Theme | Hypothesis | Status |
```
Use `- [ ]` for unchecked (pending evaluation). When an event occurs and the hypothesis is evaluated, check the box and move the row to the Evaluated section. `lint.py` flags unchecked past events older than 7 days. `briefing.py` surfaces events in the next 30 days.
All calendar sections, including Evaluated, must keep the exact five-column table shape above; `lint.py` treats malformed headers, separators, rows, dates, and status cells as parser-contract issues.

**Allocation drift** — `scripts/allocation_drift.py` reads target allocations from the Investment Strategy table and actual values from the latest snapshot JSON sidecar, then computes drift by category. Run during reviews to flag overweight/underweight positions without manual computation.

**Decision outcome tracking** — `lint.py` surfaces `status: active` decisions older than 30 days that have no content in their `## Outcome` section. These should be revisited during reviews: close the decision, record the outcome, or explicitly keep it open with a note.

**Cross-thesis consistency** — `lint.py` checks positions that appear in multiple thesis/theme docs and flags conviction mismatches (e.g., NVDA at conviction 4 in one thesis and 3 in another). Reconcile during quarterly reviews.

## Conventions Learned

This section captures corrections and patterns discovered during use. When the agent (or I) get something wrong in a way that would likely repeat, file the rule here with a date. When a pattern accumulates enough entries to generalize, promote it into the main spec above and remove the individual entries.

**Format:**
```
### YYYY-MM-DD — short rule
One-sentence explanation of the correction or pattern. Optionally: the example that prompted it.
```

**Housekeeping:** prune or consolidate when a rule has been stable for a few months and is never re-violated — either it's been internalized or it's been promoted into the main spec.

<!-- Entries below, newest on top. -->

### 2026-04-20 — Check article dates — weekly scan means last 7 days
Tavily's time_range filter is approximate. Before surfacing a finding, verify the article date actually falls within the scan window. Label anything older as "prior context" or discard it. Don't present 3-month-old news as a "this week" finding.

### 2026-04-20 — Source provenance matters: always cite and filter
All information presented to the user must have explicit source attribution. During weekly scans and research, filter findings by source quality before surfacing: prefer primary sources (company filings, industry trade pubs, wire services, regulatory bodies) over commentary (Motley Fool, SimplyWallSt, analyst blogs) and discount social media (LinkedIn posts, X/Twitter, Reddit, Instagram) unless they link to a primary. If a finding only appears in low-quality sources, flag the provenance gap rather than presenting it as fact.

### 2026-04-20 — Weekly scan should always be part of weekly review
The `/weekly-scan` skill should be run as a standard step in every weekly review, not skipped. Add to the weekly review checklist.

### 2026-04-21 — Scan first; don't duplicate weekly reviews
When a weekly review already exists from the past 7 days, a fresh scan can stand alone. Create another weekly review note only if there is new portfolio data, a hypothesis trigger, a decision/action, a material thesis-health change, or an explicit user request for another review note.

### 2026-04-21 — Weekly scan findings need source tier and newness labels
Each scan finding should say whether it is `New this week` or `Carried from prior log/review`, and identify the source tier (`filing`, `primary/company`, `trade/wire`, `data provider`, `commentary`).

### 2026-04-20 — Use `scripts/lib/snaptrade.py` for MCP data, don't hand-parse
SnapTrade MCP results have a nested `symbol.symbol.symbol` structure and `currency.code` dicts. The `parse_positions()` function in `scripts/lib/snaptrade.py` handles this. For diffing: `portfolio_diff.py` does value-level (>5% threshold); for unit-level DCA verification, iterate `Position.units` directly.
