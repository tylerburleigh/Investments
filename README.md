---
date: 2026-04-19
type: reference
tags: [readme, navigation]
---

# Investment Research Vault

A personal investment research system connected to WealthSimple via SnapTrade. Two purposes: **building conviction over time** and **making better decisions**. Research feeds decisions; decisions drive what to research next.

## Starting a Session

Open Claude Code in this vault. The agent runs `scripts/briefing.py` at the start of every session — it surfaces what needs attention (overdue reviews, stale docs, hypothesis evaluations due) without pulling live data. Tell it what you want to work on.

To pull live portfolio data, ask the agent to refresh from SnapTrade. It will create a snapshot and diff it against the last one.

## Where Things Live

| Folder | What's in it |
|--------|-------------|
| [[strategy/Investment Strategy\|strategy/]] | Hub doc + thesis and theme files — the core investment framework |
| [[holdings/\|holdings/]] | Per-ticker research notes, updated over time |
| [[decisions/log\|decisions/]] | Decision journal + append-only log |
| [[portfolio/\|portfolio/]] | Portfolio snapshots (auto-generated from SnapTrade) |
| [[reviews/\|reviews/]] | Weekly, monthly, and quarterly reviews |
| [[watchlist/\|watchlist/]] | Tickers being monitored but not yet held |
| [[docs/research-backlog\|docs/]] | Reference material, research backlog, methodology |
| [[bases/\|bases/]] | Obsidian database views — open in Obsidian to browse holdings and decisions live |

## The Review Rhythm

- **Weekly** — quick check: portfolio value, notable moves, any action needed
- **Monthly** — run lint, work through the research backlog, check thesis health, review decisions made
- **Quarterly** — full thesis stress test, evaluate open hypotheses, update conviction levels

To start a review, tell the agent: "run a weekly review", "time for the monthly", or "let's do the quarterly". The `/review` skill walks through the full checklist and writes the review note.

## Other Commands

- **"research B001"** — resolve a specific research backlog item using trusted sources
- **"pull positions"** or **"refresh from SnapTrade"** — fetch live portfolio data, create a snapshot, diff against last
- **"work through the backlog"** — the agent picks the highest-priority overdue item and researches it

## How Decisions Work

Every meaningful action gets a note in `decisions/` and a one-liner in [[decisions/log]]. The decision note records what, why, and — most importantly — what would change your mind. The log is the searchable history.

## How Theses Work

Each investment pillar has a `thesis-*.md` in `strategy/`. Each thesis has a `## Hypotheses` table: pre-registered predictions written before the event, evaluated after. When a hypothesis triggers, log a `signal` entry and update the table. This is the main mechanism for keeping conviction honest over time.

## Full Spec

Agent conventions, frontmatter schemas, lint rules, and script documentation: [[CLAUDE]].
