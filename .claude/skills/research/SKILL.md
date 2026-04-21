---
name: research
description: Research a specific item from docs/research-backlog.md using trusted sources defined in docs/research-methodology.md. Fetches evidence, summarizes findings with proper claim typing, updates the relevant thesis/theme doc, and marks the item resolved. Use when the user says "research B001", "work through the backlog", "resolve item B005", "look into [claim]", or similar.
---

# /research

Research one item from [[docs/research-backlog]] and integrate the findings into the vault.

## Step 1 — Identify the item

- If the user gave a backlog ID (e.g., `B004`), read `docs/research-backlog.md` and find that row.
- If the user said "highest priority" or "work through the backlog", pick the highest-priority open item that is overdue or closest to its Review By date.
- Extract from the row: **Question**, **Thesis / Theme** link, **Surfaced From**, **Priority**.
- If the item is already `resolved`, tell the user and stop.

## Step 2 — Read context

Read these files before searching:
1. The thesis or theme doc linked in the backlog row — understand what claim this question is trying to verify or fill.
2. `docs/research-methodology.md` — identify the trusted sources for this domain (crypto → Glassnode/CoinGecko; AI → SemiAnalysis/EDGAR; nuclear → IAEA/WNN/Sprott; macro → FRED/BIS; etc.).

## Step 3 — Search

Use `mcp__tavily-mcp__tavily_search` or `mcp__tavily-mcp__tavily_research` to find answers.

**Search strategy:**
- Start with the most authoritative source for the domain (per methodology doc). If the question asks for a specific report (e.g., "McKinsey data center infra"), search for that report directly.
- Aim for 2–3 independent sources that corroborate the finding before treating it as verified.
- For market size figures: note the source name, publication date, and what's included/excluded in the market definition.
- For quotes or specific claims: find the original source, not a secondary article about it.

**Do not use:**
- Crypto Twitter / financial social media
- Anonymous or unattributed blog posts
- AI-generated summaries without primary sources

## Step 4 — Present findings

Before writing anything to disk, show the user:

1. **What you found** — the answer (or partial answer) with sources cited
2. **Confidence level** — which callout type applies:
   - `[!source]` — if you have a specific, citable source
   - `[!analysis]` — if it's your inference from multiple sources
   - `[!unverified]` — if you found a figure but couldn't confirm the primary source
   - `[!gap]` — if the question remains genuinely unanswerable
3. **Proposed edit** — the exact text change to the thesis doc (new callout or updated callout)
4. **Whether to archive a source doc** — if the source is substantive enough to save in `docs/`

End with: "Update the vault with these findings?"

## Step 5 — Update (with user approval)

On approval, make these changes:

**In the thesis/theme doc:**
- Replace the existing `[!unverified]` or `[!gap]` callout with the appropriate typed callout including source citation.
- Add a dated entry to `## Updates` section noting what was resolved and what it means for the thesis.
- Bump `last_updated` in frontmatter to today.

**In `docs/research-backlog.md`:**
- Change the item's `Status` from `open` to `resolved`.
- Add a brief entry to the `## Resolved` table at the bottom: item number, resolution date, and a link to where the answer landed (thesis doc section or new docs/ file).
- Check off the `- [ ]` item in the thesis doc's `## Open Research Questions` section if this item addressed it.

**In `decisions/log.md`:**
- Append an `action` log entry: `### [YYYY-MM-DD] action | resolved research [item] — [[strategy/thesis-xxx]]`

**Scan cross-reference:**
- If the research item was surfaced from a scan, add `[[scans/YYYY-MM-DD]]` to the thesis doc's `## Updates` entry so the provenance chain is traceable: scan found the clue → research resolved it.

**Optionally, in `docs/`:**
- If the source is a substantial report worth referencing again, save a summary as `docs/YYYY-source-name.md` with `type: reference` frontmatter and a `[!source]` callout linking to the URL.

## Step 6 — Summarize

Report:
- What question was answered
- What the finding was and at what confidence level
- Which files were changed
- Whether any related open questions in the thesis doc are now unblocked

## Constraints

- **One item per invocation.** Don't chain research items without user direction.
- **Don't update conviction levels** based on research alone. Surface the finding; the human decides if it changes conviction.
- **Don't rewrite thesis framings.** Update the specific claim; don't reorganize the thesis doc.
- **Don't fill a `[!gap]` with a guess.** If you can't find a reliable source, update the callout to `[!unverified]` with your best finding, or leave it as `[!gap]` and note in the backlog what you tried.
- **Cite dates on all figures.** Market sizes, valuations, and statistics are time-sensitive.
