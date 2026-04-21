---
name: weekly-scan
description: Run a weekly thesis-relevant news scan. Reads all active thesis/theme docs, runs targeted Tavily searches per thesis, checks for hypothesis triggers, and writes a dated scan artifact to scans/. Use when the user says "run the weekly scan", "scan for news", "check thesis triggers", "what happened this week", or when the research methodology weekly cadence is due.
---

# /weekly-scan

Scan thesis-relevant news and check for hypothesis triggers across all active positions.

## Step 1 — Read active theses

Read all active thesis and theme docs from `strategy/` to understand current positions and open hypotheses.

For each file matching `strategy/thesis-*.md` or `strategy/theme-*.md`:
1. Read the file
2. Extract the thesis name (from the `#` heading)
3. Extract the `## Active Positions` table — list of tickers and roles
4. Extract the `## Hypotheses` table — focus on rows with Status "open" and their Timeframe, If Confirmed/Disconfirmed columns
5. Extract any `[!unverified]` or `[!gap]` callouts that might be resolved by recent news
6. Note the thesis tags from frontmatter for search query construction

Organize a summary: for each thesis, you should have its name, key tickers, 2-3 top open hypotheses, any claims awaiting verification, and any near-term catalysts that should be added to `docs/calendar.md`.

## Step 2 — Build search queries

For each thesis, construct 1-2 recurring targeted search queries based on:
- The thesis subject area (e.g., "AI infrastructure spending", "space economy launch")
- Active positions and their near-term catalysts (earnings, product launches, regulatory events)
- Open hypotheses nearing their timeframe deadlines
- Unverified claims or gaps that recent news might resolve

**Query construction rules:**
- Use specific entity names where possible (company names, tickers, program names)
- Keep queries concise (5-8 words is ideal for search relevance)
- Do NOT search for price movements or trading signals
- Prefer stable recurring queries week to week, so scans are comparable over time. Only add ad hoc queries when a specific catalyst or hypothesis needs it.

Recurring query plan:

| Thesis / Theme | Recurring queries |
|----------------|-------------------|
| AI | `hyperscaler capex AI infrastructure Amazon Microsoft Google Meta`; `AMKR NVTS AI data center advanced packaging power semiconductor` |
| Crypto | `Bitcoin ETF flows weekly Farside BlackRock IBIT`; `G20 crypto regulation exchange ban stablecoin` |
| Energy Transition | `Vistra data center PPA hyperscaler`; `spodumene lithium price AMPX commercial battery contract IRA storage tax credit` |
| Space | `AST SpaceMobile commercial service BlueBird launch`; `Rocket Lab Neutron Intuitive Machines IM-3 MDA government contract` |
| Tech Conviction | `NVIDIA AMD AI GPU market share TSMC A16 N2`; `Google Meta antitrust remedy regulatory action` |
| Nuclear | `Oklo Aurora INL criticality NRC ADVANCE Act`; `uranium spot price Sprott hyperscaler nuclear PPA` |
| EV | `NIO Li Auto deliveries gross operating margin`; `China EV price war BYD NIO Li Auto` |
| Quantum | `IonQ logical qubits SkyWater acquisition`; `Infleqtion revenue guidance quantum advantage` |
| Robotics | `Symbotic Walmart deployment customer diversification`; `Intuitive Surgical procedure growth Ion systems earnings` |

## Step 3 — Run targeted searches

Use `mcp__tavily-mcp__tavily_search` for each query.

**Search parameters:**
- `search_depth`: "basic" (this is a scan, not deep research)
- `max_results`: 5 per query
- `time_range`: "week" (last 7 days — this is a weekly scan, not a monthly catch-up)
- `topic`: "general"

**Rules:**
- Run 1-2 searches per thesis (no more)
- Process theses in order: AI, Crypto, Energy Transition, Space, Tech Conviction, then themes (Nuclear, EV, Quantum, Robotics)
- If a search returns no relevant results, note it and move on — silence is fine
- **Check article dates.** Tavily's `time_range` filter is approximate. Before surfacing a finding, verify the article publication date falls within the scan window (last 7 days). Discard or clearly label anything older as "prior context, not new this week."

**Do NOT use:**
- `mcp__snaptrade__list_positions` or any SnapTrade tools
- `mcp__tavily-mcp__tavily_research` (that's for deep research, not scanning)

## Step 4 — Evaluate findings

For each search result that is relevant to a thesis, filter by source quality FIRST, then evaluate.

**Source quality filter (apply before evaluating):**
- **filing:** SEC/SEDAR filings, regulatory filings, official government releases. Highest trust.
- **primary/company:** company investor releases, earnings materials, official product or mission updates.
- **trade/wire:** Reuters, Bloomberg, industry trade publications (DigiTimes, SpaceNews, NucNet, S&P Global, WNN).
- **data provider:** Farside, CoinGecko, Sprott, EIA, FRED, etc. Use with date and methodology caveat where relevant.
- **commentary:** Motley Fool, SimplyWallSt, analyst blogs, crypto-native publications. Only surface if the underlying data is verifiable.
- **discard:** social media — LinkedIn posts, X/Twitter, Reddit, Instagram — unless they link directly to a primary source.

**Evaluation:**

1. **Check against the Hypotheses table** in the relevant thesis doc:
   - Does the news confirm, disconfirm, or relate to any open hypothesis?
   - A hypothesis is "triggered" if the news provides conclusive evidence that would change its Status from "open" to "confirmed" or "disconfirmed"
   - Partial evidence (directional but not conclusive) is a directional signal, not a trigger

2. **Check against open backlog items** in `docs/research-backlog.md`:
   - Does any result answer an open research question?
   - Flag items that might be resolvable, but do NOT resolve them — that is what `/research` is for

3. **Check against unverified claims** (`[!unverified]` and `[!gap]` callouts):
   - Does any result provide source material for an unverified claim?
   - Note it for the user but do NOT update the callout — that requires `/research`

4. **Check against existing records**:
   - Search `decisions/log.md`, recent `reviews/`, and existing `scans/` for the same signal.
   - Label each finding as **New this week** or **Carried from prior log/review**.
   - Do not duplicate a carried signal in the summary unless it remains thesis-relevant and no scan artifact has captured it yet.

5. **Check for calendar items**:
   - If a search surfaces an upcoming earnings date, mission window, regulatory deadline, or other catalyst tied to a hypothesis, add it to `docs/calendar.md`.
   - Calendar additions should link the relevant thesis/theme and hypothesis when possible.

## Step 5 — Present findings to user

Present a structured summary of findings. Categorize each finding by type:

**Hypothesis triggers (conclusive evidence):**
- Present the finding with source citation
- Ask the user for confirmation before updating the thesis doc
- If confirmed: update the thesis doc (Hypotheses table Status + Evaluated, `## Updates` dated entry). The thesis doc is the permanent record — no separate log entry needed.

**Directional signals (partial evidence):**
- Summarize in 1-2 sentences with source citation
- These will be written to the scan artifact and accumulate for monthly review
- Label `New this week` vs. `Carried from prior log/review`
- Include the source tier

**Potential backlog resolutions:**
- Note which backlog item and what the finding is
- Recommend running `/research {item_id}` to properly resolve it

**If nothing significant was found for a thesis:**
- Say so explicitly: "No significant developments for {thesis name}."

## Step 6 — Write scan artifact

Write the scan results to `scans/YYYY-MM-DD.md` using the template at `templates/scan.md`. Fill in every thesis section — even if the content is "Nothing significant."

**Structure per thesis:**
- **Hypothesis Triggers** — any conclusive evidence with source citation (publication + article date)
- **Directional Signals** — partial evidence with source citation
- **Potential Backlog Resolutions** — which backlog items have new source material

**Every finding must include:**
- Newness label: `New this week` or `Carried from prior log/review`
- Source tier: `filing`, `primary/company`, `trade/wire`, `data provider`, or `commentary`
- Source publication name
- Article publication date (verified against the scan window)
- 1-2 sentence explanation of what it means directionally

**Frontmatter:** fill in `theses_scanned` (count of active thesis/theme docs scanned), `signals_found` (count of hypothesis triggers + directional signals).

**Summary denominator:** count active `strategy/thesis-*.md` and `strategy/theme-*.md` files. Do not hard-code `10`.

## Step 7 — Report scan summary

Report the final scan results to the user:

```
Weekly Scan Summary — YYYY-MM-DD
Scan written to: scans/YYYY-MM-DD.md
Theses/themes scanned: X/Y
Hypothesis triggers: N (list them)
Directional signals: M (list them)
Nothing significant: K theses

Next steps: [any recommended actions — research items, hypothesis evaluations to watch]
```

## Constraints

- **Don't pull SnapTrade data.** This is a news scan, not a portfolio valuation.
- **Don't change conviction levels.** Surface findings; the human decides if conviction changes.
- **Don't deep-dive into any single item.** If something needs deep investigation, recommend `/research` for it.
- **Don't update callout types.** Changing `[!unverified]` to `[!source]` requires the full `/research` workflow with source archiving.
- **Don't log to decisions/log.md.** Signals live in the scan artifact. Hypothesis triggers update the thesis doc directly. Only portfolio actions go in the log.
- **Do update `docs/calendar.md` for upcoming catalysts** found during the scan when they are tied to a thesis/hypothesis.
- **Keep total search time under 30 minutes.** 1-2 searches per thesis, max 5 results each. Prioritize theses with nearer-term hypothesis deadlines.
- **Silence is fine.** If nothing significant happened for a thesis, say so — no need to manufacture findings.
- **Cite sources explicitly.** Every finding must include source publication, article date, link, source tier, and newness label. Filter by quality before presenting: primary sources over commentary, discard social media. If a finding only appears in low-quality sources, flag the provenance gap rather than presenting it as fact.
