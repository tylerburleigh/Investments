"""Lint the investment vault against the conventions in CLAUDE.md.

Checks:
  - Frontmatter schema (required fields per type, allowed values)
  - Wikilinks resolve to existing files
  - Decision → holding backlink reciprocity
  - Staleness thresholds (holdings 90d, theses 180d, strategy hub 30d)
  - Log coverage (every decision file has a log.md entry)
  - Orphaned holdings (no linked thesis)
  - Hypothesis timeframes past due (open hypotheses whose evaluation date has passed)
  - Unresolved [!gap] and [!unverified] callouts in strategy docs
  - Research backlog overdue items
  - Source callout quality (citation present, date/year attached)
  - Untyped market-size figures in strategy doc prose
  - Calendar table parser contracts (five columns, canonical header, task status)
  - Parser contracts for documented note types, content folders, templates, and automation tables

Usage:
    python3 scripts/lint.py                 # full report
    python3 scripts/lint.py --write-index   # also regenerate holdings/index.md
    python3 scripts/lint.py --today 2026-04-18  # override for deterministic tests

Exit codes: 0 = no errors, 1 = errors found, 2 = script failure.
"""

from __future__ import annotations

import argparse
import subprocess
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import yaml

_DOC = __doc__ or ""


VAULT_ROOT = Path(__file__).resolve().parent.parent

ALLOWED_TYPES = {
    "holding", "decision", "snapshot", "review", "watchlist",
    "strategy", "reference", "scan",
}

ALLOWED_STATUS_BY_TYPE = {
    "holding": {"active", "watching", "closed"},
    "decision": {"active", "closed"},
    "watchlist": {"watching", "active", "closed"},
    "strategy": {"active", "closed"},
    "review": {"active", "closed"},
    "snapshot": {"active", "closed"},
    "reference": {"active", "closed"},
    "scan": {"active", "closed"},
}

REQUIRED_FIELDS = {
    "holding":   {"date", "type", "ticker", "status"},
    "decision":  {"date", "type", "action", "status"},
    "snapshot":  {"date", "type"},
    "review":    {"date", "type", "period"},
    "watchlist": {"date", "type", "ticker", "status"},
    "strategy":  {"date", "type", "last_updated", "status"},
    "reference": {"date", "type"},
    "scan":      {"date", "type", "status", "theses_scanned", "signals_found"},
}

STALENESS_DAYS = {
    "holding": 90,
    "strategy_thesis": 180,  # strategy/thesis-* and strategy/theme-*
    "strategy_hub": 30,      # strategy/Investment Strategy.md
}

CONTENT_FOLDERS = ["holdings", "decisions", "portfolio", "reviews",
                   "strategy", "watchlist", "docs", "scans"]

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
CALLOUT_GAP_RE = re.compile(r">\s*\[!(gap|unverified)\]([^\n]*)", re.IGNORECASE)
BACKLOG_ROW_RE = re.compile(r"^\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|")
CALENDAR_HEADER = ["Date", "Event", "Thesis / Theme", "Hypothesis", "Status"]
CALENDAR_STATUS_RE = re.compile(r"- \[[ xX]\]")

CALLOUT_SOURCE_RE = re.compile(r">\s*\[!source\]([^\n]*)", re.IGNORECASE)
MARKET_SIZE_FIGURE_RE = re.compile(
    r"\$[\d,.]+[BMT]"
    r"|\d+\.?\d*%\s*CAGR"
    r"|\$[\d,.]+\s*(?:billion|million|trillion)",
    re.IGNORECASE,
)
CITATION_RE = re.compile(
    r"https?://\S+"
    r"|\[\[docs/[^\]]+\]\]"
    r"|\[\[strategy/[^\]]+\]\]"
    r"|(?:McKinsey|Goldman|Sachs|Morgan|Stanley|IDC|Gartner|Forrester"
    r"|IAEA|Sprott|NREL|EIA|BIS|IMF|FRED|CoinGecko|Glassnode"
    r"|SEC|EDGAR|NRC|DOE|NASA|SpaceNews|SemiAnalysis"
    r"|BofA|Morningstar|VanEck|BlackRock|Chainalysis|WNN|BEA|BLS)",
)
DATE_YEAR_RE = re.compile(
    r"\b20[12]\d\b"
    r"|\b203[0-9]\b"
    r"|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+20\d{2}"
    r"|\b20\d{2}-\d{2}-\d{2}\b"
    r"|\bQ[1-4]\s+20\d{2}\b"
    r"|\bH[12]\s+20\d{2}\b",
)

ROOT_LEVEL_FILES = {"CLAUDE"}  # bare wikilinks to these are valid


@dataclass
class Issue:
    severity: str  # "error" | "warn"
    category: str
    path: str
    message: str


@dataclass
class Note:
    path: Path
    rel_path: str           # "holdings/BTC.md"
    stem: str               # "BTC"
    folder: str             # "holdings"
    frontmatter: dict = field(default_factory=dict)
    body: str = ""
    frontmatter_ok: bool = True
    parse_error: str | None = None

    @property
    def type(self) -> str | None:
        return self.frontmatter.get("type")

    @property
    def last_updated(self) -> date | None:
        return _parse_date(self.frontmatter.get("last_updated"))

    @property
    def date(self) -> date | None:
        return _parse_date(self.frontmatter.get("date"))


def _parse_date(val) -> date | None:
    if val is None:
        return None
    if isinstance(val, date):
        return val
    try:
        return datetime.strptime(str(val).strip('"\''), "%Y-%m-%d").date()
    except ValueError:
        return None


def load_notes() -> list[Note]:
    notes: list[Note] = []
    for folder in CONTENT_FOLDERS:
        folder_path = VAULT_ROOT / folder
        if not folder_path.exists():
            continue
        for md in folder_path.rglob("*.md"):
            rel = md.relative_to(VAULT_ROOT).as_posix()
            note = Note(path=md, rel_path=rel, stem=md.stem, folder=folder)
            raw = md.read_text(encoding="utf-8")
            fm, body = _split_frontmatter(raw)
            if fm is None:
                note.frontmatter_ok = False
                note.parse_error = "no frontmatter block"
            else:
                try:
                    note.frontmatter = yaml.safe_load(fm) or {}
                except yaml.YAMLError as e:
                    note.frontmatter_ok = False
                    note.parse_error = f"YAML error: {e}"
            note.body = body
            notes.append(note)
    return notes


def _split_frontmatter(raw: str) -> tuple[str | None, str]:
    if not raw.startswith("---"):
        return None, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return None, raw
    fm = raw[3:end].strip()
    body = raw[end + 4:]
    return fm, body


# ---------- checks ----------

def check_frontmatter(notes: list[Note]) -> list[Issue]:
    issues: list[Issue] = []
    for n in notes:
        if not n.frontmatter_ok:
            issues.append(Issue("error", "schema", n.rel_path,
                                f"frontmatter parse failed: {n.parse_error}"))
            continue
        t = n.frontmatter.get("type")
        if not t:
            # log.md and index.md lack strict type requirements
            if n.stem in {"log", "index"}:
                continue
            issues.append(Issue("error", "schema", n.rel_path, "missing `type`"))
            continue
        if t not in ALLOWED_TYPES:
            issues.append(Issue("error", "schema", n.rel_path,
                                f"unknown type: {t!r} (allowed: {sorted(ALLOWED_TYPES)})"))
            continue
        required = REQUIRED_FIELDS.get(t, set())
        missing = required - n.frontmatter.keys()
        if missing:
            issues.append(Issue("error", "schema", n.rel_path,
                                f"missing required fields for type={t}: {sorted(missing)}"))
        status = n.frontmatter.get("status")
        if status and status not in ALLOWED_STATUS_BY_TYPE.get(t, set()):
            issues.append(Issue("warn", "schema", n.rel_path,
                                f"unusual status {status!r} for type={t}"))
        # Holding-specific: conviction 1-5, time_horizon in set
        if t == "holding":
            conv = n.frontmatter.get("conviction")
            if conv is not None and (not isinstance(conv, int) or not 1 <= conv <= 5):
                issues.append(Issue("warn", "schema", n.rel_path,
                                    f"conviction must be int 1-5, got {conv!r}"))
            th = n.frontmatter.get("time_horizon")
            if th and th not in {"short", "medium", "long"}:
                issues.append(Issue("warn", "schema", n.rel_path,
                                    f"time_horizon should be short|medium|long, got {th!r}"))
    return issues


def _strip_code(body: str) -> str:
    """Remove fenced and inline code so wikilink scanning doesn't hit placeholders."""
    body = FENCED_CODE_RE.sub("", body)
    body = INLINE_CODE_RE.sub("", body)
    return body


def _split_table_row(line: str) -> list[str]:
    """Split a markdown table row while preserving escaped pipes in wikilinks."""
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|"):
        return []
    placeholder = "__ESCAPED_PIPE__"
    s = s.replace(r"\|", placeholder)
    return [c.strip().replace(placeholder, "|") for c in s.split("|")[1:-1]]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(set(c.replace(" ", "")) <= {"-", ":"} for c in cells)


def _display_wikilinks(text: str) -> str:
    """Convert Obsidian wikilinks to display text for parser smoke checks."""
    def repl(match: re.Match) -> str:
        raw = match.group(1).replace(r"\|", "|")
        if "|" in raw:
            return raw.rsplit("|", 1)[1]
        return raw.split("#", 1)[0].rsplit("/", 1)[-1]

    return WIKILINK_RE.sub(repl, text)


def _section_body(body: str, heading: str) -> str:
    """Extract content between '## heading' and the next ## heading."""
    lines = body.split("\n")
    in_section = False
    out = []
    for line in lines:
        s = line.strip()
        if s.startswith("## "):
            if in_section:
                break
            if s == f"## {heading}":
                in_section = True
            continue
        if in_section:
            out.append(line)
    return "\n".join(out)


def check_wikilinks(notes: list[Note]) -> list[Issue]:
    """Wikilinks resolve to a real file (errors) or a plausible pending file (warnings).

    Unresolved `holdings/TICKER` links are warnings — Obsidian treats these as
    unresolved links, and they usefully surface pending holdings. Anything else
    that doesn't resolve is an error (likely a typo or stale reference).
    """
    issues: list[Issue] = []
    known_stems = {n.rel_path[:-3]: n for n in notes}
    known_bare = {n.stem: n for n in notes}
    for n in notes:
        scan_body = _strip_code(n.body)
        for m in WIKILINK_RE.finditer(scan_body):
            raw = m.group(1).strip()
            target = raw.split("#")[0].strip().rstrip("\\")  # handle \| escape in table cells
            if not target:
                continue
            target = target[:-3] if target.endswith(".md") else target
            if target.endswith("/"):
                issues.append(Issue("warn", "wikilink", n.rel_path,
                                    f"placeholder link: [[{raw}]]"))
                continue
            if target in known_stems:
                continue
            if "/" not in target:
                if target in known_bare or target in ROOT_LEVEL_FILES:
                    continue
            # Unresolved. Grade by prefix.
            if target.startswith("holdings/"):
                issues.append(Issue("warn", "wikilink", n.rel_path,
                                    f"unresolved (pending holding): [[{raw}]]"))
            else:
                issues.append(Issue("error", "wikilink", n.rel_path,
                                    f"broken link: [[{raw}]]"))
    return issues


def check_backlinks(notes: list[Note]) -> list[Issue]:
    """If a decision links [[holdings/TICKER]], that holding should link the decision."""
    issues: list[Issue] = []
    holdings = {n.rel_path[:-3]: n for n in notes if n.folder == "holdings"}
    decisions = [n for n in notes if n.folder == "decisions" and n.stem != "log"]

    for dec in decisions:
        dec_key = dec.rel_path[:-3]  # "decisions/2026-04-18-xxx"
        targets: set[str] = set()
        for m in WIKILINK_RE.finditer(_strip_code(dec.body)):
            t = m.group(1).split("#")[0].strip()
            t = t[:-3] if t.endswith(".md") else t
            if t.startswith("holdings/"):
                targets.add(t)
        for h_key in targets:
            holding = holdings.get(h_key)
            if not holding:
                # Already caught by wikilink check
                continue
            # Look for a link back to this decision in the holding body
            back_found = any(
                _link_match(m.group(1), dec_key)
                for m in WIKILINK_RE.finditer(_strip_code(holding.body))
            )
            if not back_found:
                issues.append(Issue("warn", "backlink", holding.rel_path,
                                    f"no backlink to {dec.rel_path} "
                                    f"(decision references this holding)"))
    return issues


def _link_match(raw: str, target: str) -> bool:
    t = raw.split("#")[0].strip()
    t = t[:-3] if t.endswith(".md") else t
    return t == target


def check_staleness(notes: list[Note], today: date) -> list[Issue]:
    issues: list[Issue] = []
    for n in notes:
        if not n.frontmatter_ok or not n.type:
            continue
        lu = n.last_updated or n.date
        if lu is None:
            continue
        days = (today - lu).days
        threshold = None
        label = None
        if n.folder == "holdings" and n.type == "holding":
            threshold, label = STALENESS_DAYS["holding"], "holding (90d)"
        elif n.rel_path == "strategy/Investment Strategy.md":
            threshold, label = STALENESS_DAYS["strategy_hub"], "strategy hub (30d)"
        elif n.folder == "strategy" and n.type == "strategy":
            threshold, label = STALENESS_DAYS["strategy_thesis"], "thesis/theme (180d)"
        if threshold is not None and days > threshold:
            issues.append(Issue("warn", "staleness", n.rel_path,
                                f"last_updated {lu} ({days}d ago, {label} threshold)"))
    return issues


def check_log_coverage(notes: list[Note]) -> list[Issue]:
    """Every decision file should appear in decisions/log.md."""
    issues: list[Issue] = []
    log = next((n for n in notes if n.rel_path == "decisions/log.md"), None)
    if log is None:
        issues.append(Issue("error", "log", "decisions/log.md",
                            "log.md is missing"))
        return issues
    decisions = [n for n in notes
                 if n.folder == "decisions" and n.stem not in {"log", "index"}]
    log_scan = _strip_code(log.body)
    for dec in decisions:
        key = dec.rel_path[:-3]
        # Match either [[decisions/...]] or [[2026-04-18-xxx]]
        patterns = [f"[[{key}]]", f"[[{dec.stem}]]"]
        if not any(p in log_scan for p in patterns):
            issues.append(Issue("warn", "log", "decisions/log.md",
                                f"no entry for {dec.rel_path}"))
    return issues


_MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def _parse_timeframe(s: str) -> date | None:
    """Parse a hypothesis timeframe string → latest expected evaluation date."""
    import calendar
    s = re.sub(r"\(.*?\)", "", s).strip().lower()
    if not s or s in ("—", "-") or "ongoing" in s or "n/a" in s:
        return None
    parts = re.split(r"[–—/]", s)
    s = parts[-1].strip() if len(parts) > 1 else s
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return _parse_date(m.group(1))
    m = re.search(r"q([1-4])\s*(\d{4})", s)
    if m:
        q, yr = int(m.group(1)), int(m.group(2))
        mo = q * 3
        return date(yr, mo, calendar.monthrange(yr, mo)[1])
    m = re.search(r"h([12])\s*(\d{4})", s)
    if m:
        half, yr = int(m.group(1)), int(m.group(2))
        mo = 6 if half == 1 else 12
        return date(yr, mo, calendar.monthrange(yr, mo)[1])
    m = re.search(r"([a-z]{3})\s+(\d{4})", s)
    if m:
        mo = _MONTH_MAP.get(m.group(1))
        yr = int(m.group(2))
        if mo:
            import calendar as cal
            return date(yr, mo, cal.monthrange(yr, mo)[1])
    m = re.search(r"\b(20\d{2})\b", s)
    if m:
        return date(int(m.group(1)), 12, 31)
    return None


def _parse_hypothesis_table(body: str) -> list[dict]:
    """Extract open hypothesis rows from a ## Hypotheses table."""
    # Find ## Hypotheses section
    lines = body.split("\n")
    in_section = False
    rows = []
    for line in lines:
        s = line.strip()
        if s.startswith("## "):
            if in_section:
                break
            if s == "## Hypotheses":
                in_section = True
            continue
        if not in_section or not s.startswith("|"):
            continue
        cells = _split_table_row(s)
        if len(cells) < 8:
            continue
        num = cells[0]
        if not num or num == "#" or set(num.replace(":", "")) <= {"-"}:
            continue
        rows.append({
            "num": num,
            "text": cells[1][:50] if cells[1:] else "",
            "timeframe": cells[4] if len(cells) > 4 else "",
            "status": cells[7].lower().strip() if len(cells) > 7 else "open",
        })
    return rows


def check_hypothesis_due(notes: list[Note], today: date) -> list[Issue]:
    """Warn on open hypotheses whose evaluation timeframe has passed."""
    issues: list[Issue] = []
    for n in notes:
        if n.folder != "strategy" or n.type != "strategy":
            continue
        scan = _strip_code(n.body)
        for row in _parse_hypothesis_table(scan):
            if row["status"] in ("confirmed", "disconfirmed", "expired"):
                continue
            tf = _parse_timeframe(row["timeframe"])
            if tf and (today - tf).days > 0:
                issues.append(Issue(
                    "warn", "hypotheses", n.rel_path,
                    f"{row['num']} overdue {(today - tf).days}d "
                    f"(timeframe: {row['timeframe']}): {row['text'][:45]}...",
                ))
    return issues


def check_callout_gaps(notes: list[Note]) -> list[Issue]:
    """Warn on [!gap] and [!unverified] callouts in strategy docs — they should be in the research backlog."""
    issues: list[Issue] = []
    for n in notes:
        if n.folder != "strategy" or n.type != "strategy":
            continue
        scan = _strip_code(n.body)
        for m in CALLOUT_GAP_RE.finditer(scan):
            kind = m.group(1).lower()
            snippet = m.group(2).strip()[:60]
            issues.append(Issue("warn", "gaps", n.rel_path,
                                f"unresolved [{kind}]: {snippet}"))
    return issues


def _callout_continuation(lines: list[str], line_idx: int) -> str:
    """Return the continuation line (next >-prefixed line) after a callout, or ''."""
    if line_idx + 1 < len(lines) and lines[line_idx + 1].strip().startswith(">"):
        return lines[line_idx + 1].strip().lstrip("> ")
    return ""


def check_source_callouts(notes: list[Note]) -> list[Issue]:
    """Warn on [!source] callouts missing citations or date references."""
    issues: list[Issue] = []
    for n in notes:
        if n.folder != "strategy" or n.type != "strategy":
            continue
        scan = _strip_code(n.body)
        lines = scan.splitlines()
        for i, line in enumerate(lines):
            m = CALLOUT_SOURCE_RE.search(line)
            if not m:
                continue
            claim = m.group(1).strip()
            cont = _callout_continuation(lines, i)
            has_citation = bool(CITATION_RE.search(claim)) or bool(CITATION_RE.search(cont))
            if not has_citation:
                issues.append(Issue("warn", "sources", n.rel_path,
                                    f"[!source] without citation (line ~{i+1}): {claim[:60]}"))
                continue
            has_date = bool(DATE_YEAR_RE.search(claim)) or bool(DATE_YEAR_RE.search(cont))
            if not has_date:
                issues.append(Issue("warn", "sources", n.rel_path,
                                    f"[!source] without date/year (line ~{i+1}): {claim[:60]}"))
    return issues


def check_untyped_figures(notes: list[Note]) -> list[Issue]:
    """Warn on market-size figures in strategy doc prose that aren't inside any callout block."""
    issues: list[Issue] = []
    for n in notes:
        if n.folder != "strategy" or n.type != "strategy":
            continue
        scan = _strip_code(n.body)
        for i, line in enumerate(scan.splitlines()):
            s = line.strip()
            if s.startswith(">") or s.startswith("|") or s.startswith("#"):
                continue
            for fm in MARKET_SIZE_FIGURE_RE.finditer(line):
                issues.append(Issue("warn", "figures", n.rel_path,
                                    f"untyped figure '{fm.group(0)}' (line ~{i+1}): {s[:70]}"))
                break
    return issues


def check_research_backlog(notes: list[Note], today: date) -> list[Issue]:
    """Flag overdue open items in docs/research-backlog.md."""
    issues: list[Issue] = []
    backlog = next((n for n in notes if n.rel_path == "docs/research-backlog.md"), None)
    if backlog is None:
        return issues
    for line in backlog.body.splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        parts = _split_table_row(line)
        if len(parts) < 7:
            continue
        num = parts[0]
        # Skip header and separator rows
        if num in ("#", "---", ":---", "") or set(num) <= {"-", ":"}:
            continue
        question, _, _, priority, review_by, status = parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
        if status.lower() in ("resolved", "status"):
            continue
        review_date = _parse_date(review_by)
        if review_date and (today - review_date).days > 0:
            issues.append(Issue("warn", "backlog", "docs/research-backlog.md",
                                f"overdue #{num} [{priority}] (was {review_by}): "
                                f"{question[:55]}..."))
    return issues


def check_orphan_holdings(notes: list[Note]) -> list[Issue]:
    """Holdings should link at least one thesis or theme doc."""
    issues: list[Issue] = []
    for n in notes:
        if n.folder != "holdings" or n.stem == "index":
            continue
        linked_strategy = any(
            m.group(1).split("#")[0].strip().startswith("strategy/")
            for m in WIKILINK_RE.finditer(_strip_code(n.body))
        )
        if not linked_strategy:
            issues.append(Issue("warn", "orphan", n.rel_path,
                                "no link to any strategy/thesis-* or strategy/theme-*"))
    return issues


def check_decision_outcomes(notes: list[Note], today: date) -> list[Issue]:
    """Flag active decisions older than 30 days with no Outcome section content."""
    issues: list[Issue] = []
    for n in notes:
        if n.folder != "decisions" or n.stem in {"log", "index"}:
            continue
        if n.type != "decision":
            continue
        status = n.frontmatter.get("status")
        if status != "active":
            continue
        dec_date = n.date
        if dec_date is None:
            continue
        days = (today - dec_date).days
        if days < 30:
            continue
        # Check if Outcome section has real content (more than just comments)
        outcome_section = _section_body(_strip_code(n.body), "Outcome")
        has_content = any(
            line.strip() and not line.strip().startswith("<!--")
            for line in outcome_section.splitlines()
        )
        if not has_content:
            issues.append(Issue("warn", "decisions", n.rel_path,
                                f"active for {days}d with no outcome recorded"))
    return issues


def check_cross_thesis_conviction(notes: list[Note]) -> list[Issue]:
    """Flag positions appearing in multiple thesis/theme docs with different conviction."""
    issues: list[Issue] = []
    ticker_convictions: dict[str, list[tuple[str, str]]] = {}

    for n in notes:
        if n.folder != "strategy" or n.type != "strategy":
            continue
        scan = _strip_code(n.body)
        for m in WIKILINK_RE.finditer(scan):
            target = m.group(1).split("|")[0].strip()
            if not target.startswith("holdings/"):
                continue
            ticker = target.split("/", 1)[1]
            # Find conviction in the same table row as this wikilink
            # Look backward from the wikilink position to find the table row
            row_start = scan.rfind("|", 0, m.start())
            if row_start == -1:
                continue
            row_end = scan.find("\n", m.start())
            if row_end == -1:
                row_end = len(scan)
            row = scan[row_start:row_end]
            cells = _split_table_row(row)
            # Conviction is typically the last numeric cell in position tables
            conv = None
            for cell in reversed(cells):
                try:
                    val = int(cell)
                    if 1 <= val <= 5:
                        conv = val
                        break
                except (ValueError, TypeError):
                    continue
            if conv is not None:
                ticker_convictions.setdefault(ticker, []).append(
                    (n.stem, str(conv))
                )

    for ticker, entries in sorted(ticker_convictions.items()):
        if len(entries) < 2:
            continue
        conv_values = set(c for _, c in entries)
        if len(conv_values) > 1:
            sources = ", ".join(f"{doc}={conv}" for doc, conv in entries)
            issues.append(Issue("warn", "consistency", f"holdings/{ticker}",
                                f"conviction mismatch: {sources}"))
    return issues


def check_event_calendar(notes: list[Note], today: date) -> list[Issue]:
    """Flag past events in docs/calendar.md that haven't been evaluated."""
    issues: list[Issue] = []
    cal = next((n for n in notes if n.rel_path == "docs/calendar.md"), None)
    if cal is None:
        return issues
    scan = _strip_code(cal.body)
    for line in scan.splitlines():
        line = line.strip()
        # Look for date patterns in event rows: | 2026-04-19 | ... |
        cells = _split_table_row(line)
        if len(cells) < 5 or "- [ ]" not in cells[4]:
            continue
        event_date = _parse_date(cells[0])
        if event_date and (today - event_date).days > 7:
            desc = " | ".join(cells[:3])[:60]
            issues.append(Issue("warn", "calendar", "docs/calendar.md",
                                f"unchecked past event ({event_date}): {desc}"))
    return issues


def _check_calendar_parser_contract(calendar: Note) -> list[Issue]:
    """Validate docs/calendar.md table rows before calendar parsers consume them."""
    issues: list[Issue] = []
    expected_cols = len(CALENDAR_HEADER)
    expected_header = f"| {' | '.join(CALENDAR_HEADER)} |"

    for idx, line in enumerate(calendar.body.splitlines(), start=1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        if not s.endswith("|"):
            issues.append(Issue(
                "error", "parser", "docs/calendar.md",
                f"calendar table row body line {idx} is missing a trailing `|`",
            ))
            continue

        cells = _split_table_row(s)
        if not cells:
            continue
        if _is_separator_row(cells):
            if len(cells) != expected_cols:
                issues.append(Issue(
                    "error", "parser", "docs/calendar.md",
                    f"calendar separator body line {idx} parsed {len(cells)} columns, expected {expected_cols}",
                ))
            continue
        if cells[0] == "Date":
            if cells != CALENDAR_HEADER:
                issues.append(Issue(
                    "error", "parser", "docs/calendar.md",
                    f"calendar header body line {idx} must be: {expected_header}",
                ))
            continue
        if len(cells) != expected_cols:
            issues.append(Issue(
                "error", "parser", "docs/calendar.md",
                f"calendar table row body line {idx} parsed {len(cells)} columns, expected {expected_cols}",
            ))
            continue

        if _parse_date(cells[0]) is None:
            issues.append(Issue(
                "warn", "parser", "docs/calendar.md",
                f"calendar table row body line {idx} has an unparsable date: {cells[0]!r}",
            ))
            continue
        if not CALENDAR_STATUS_RE.search(cells[4]):
            issues.append(Issue(
                "warn", "parser", "docs/calendar.md",
                f"calendar table row body line {idx} has no task status cell",
            ))

    return issues


def check_parser_contracts(notes: list[Note], today: date) -> list[Issue]:
    """Catch drift between vault conventions and the parsers that depend on them."""
    issues: list[Issue] = []

    guide_path = VAULT_ROOT / "CLAUDE.md"
    if guide_path.exists():
        guide = guide_path.read_text(encoding="utf-8")
        folder_section = _section_body(guide, "Folder Structure")
        documented_folders = {
            item.split("/", 1)[0]
            for item in re.findall(r"`([^`]+/)`", folder_section)
        }
        note_folders = documented_folders - {"scripts", "templates", "bases"}
        missing_folders = sorted(note_folders - set(CONTENT_FOLDERS))
        if missing_folders:
            issues.append(Issue(
                "error", "parser", "scripts/lint.py",
                f"CONTENT_FOLDERS missing documented note folder(s): {missing_folders}",
            ))

        m = re.search(r"`type`\s+—\s+one of:\s+([^\n]+)", guide)
        if m:
            documented_types = set(re.findall(r"`([^`]+)`", m.group(1)))
            missing_types = sorted(documented_types - ALLOWED_TYPES)
            extra_types = sorted(ALLOWED_TYPES - documented_types)
            if missing_types:
                issues.append(Issue(
                    "error", "parser", "scripts/lint.py",
                    f"ALLOWED_TYPES missing documented type(s): {missing_types}",
                ))
            if extra_types:
                issues.append(Issue(
                    "warn", "parser", "scripts/lint.py",
                    f"ALLOWED_TYPES contains undocumented type(s): {extra_types}",
                ))
            for t in sorted(documented_types | ALLOWED_TYPES):
                if t not in REQUIRED_FIELDS:
                    issues.append(Issue("error", "parser", "scripts/lint.py",
                                        f"REQUIRED_FIELDS missing type={t!r}"))
                if t not in ALLOWED_STATUS_BY_TYPE:
                    issues.append(Issue("error", "parser", "scripts/lint.py",
                                        f"ALLOWED_STATUS_BY_TYPE missing type={t!r}"))
        else:
            issues.append(Issue("warn", "parser", "CLAUDE.md",
                                "could not parse documented frontmatter type list"))

    templates_dir = VAULT_ROOT / "templates"
    if templates_dir.exists():
        for tmpl in sorted(templates_dir.glob("*.md")):
            raw = tmpl.read_text(encoding="utf-8")
            fm_text, _ = _split_frontmatter(raw)
            rel = tmpl.relative_to(VAULT_ROOT).as_posix()
            if fm_text is None:
                issues.append(Issue("error", "parser", rel,
                                    "template missing frontmatter block"))
                continue
            try:
                fm = yaml.safe_load(fm_text) or {}
            except yaml.YAMLError as e:
                issues.append(Issue("error", "parser", rel,
                                    f"template YAML parse failed: {e}"))
                continue
            t = fm.get("type")
            if not t:
                issues.append(Issue("error", "parser", rel,
                                    "template missing `type`"))
                continue
            if t not in ALLOWED_TYPES:
                issues.append(Issue("error", "parser", rel,
                                    f"template type {t!r} not in ALLOWED_TYPES"))
                continue
            missing = REQUIRED_FIELDS.get(t, set()) - fm.keys()
            if missing:
                issues.append(Issue("error", "parser", rel,
                                    f"template missing required fields for type={t}: {sorted(missing)}"))

    calendar = next((n for n in notes if n.rel_path == "docs/calendar.md"), None)
    if calendar:
        issues.extend(_check_calendar_parser_contract(calendar))

    backlog = next((n for n in notes if n.rel_path == "docs/research-backlog.md"), None)
    if backlog:
        section = None
        for idx, line in enumerate(backlog.body.splitlines(), start=1):
            s = line.strip()
            if s == "## Open":
                section = "open"
                continue
            if s == "## Resolved":
                section = "resolved"
                continue
            cells = _split_table_row(line)
            if not cells or _is_separator_row(cells) or cells[0] in {"#", "—"}:
                continue
            if section == "open" and len(cells) != 7:
                issues.append(Issue("error", "parser", "docs/research-backlog.md",
                                    f"open backlog row line {idx} parsed {len(cells)} columns, expected 7"))
            if section == "resolved" and len(cells) != 4:
                issues.append(Issue("error", "parser", "docs/research-backlog.md",
                                    f"resolved backlog row line {idx} parsed {len(cells)} columns, expected 4"))

    for n in notes:
        if n.folder != "strategy" or n.type != "strategy":
            continue
        hyp = _section_body(_strip_code(n.body), "Hypotheses")
        if not hyp.strip():
            continue
        for idx, line in enumerate(hyp.splitlines(), start=1):
            cells = _split_table_row(line)
            if not cells or _is_separator_row(cells) or cells[0] == "#":
                continue
            if len(cells) != 9:
                issues.append(Issue("error", "parser", n.rel_path,
                                    f"hypothesis row parsed {len(cells)} columns, expected 9 near section line {idx}"))

    try:
        result = subprocess.run(
            [sys.executable, str(VAULT_ROOT / "scripts" / "briefing.py"),
             "--today", today.isoformat()],
            cwd=VAULT_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as e:
        issues.append(Issue("warn", "parser", "scripts/briefing.py",
                            f"briefing smoke test failed to run: {e}"))
    else:
        output = result.stdout + result.stderr
        if result.returncode != 0:
            issues.append(Issue("error", "parser", "scripts/briefing.py",
                                f"briefing smoke test exited {result.returncode}"))
        for bad in ("[[strategy/", r"\|", "{{"):
            if bad in output:
                sample = next((ln.strip() for ln in output.splitlines() if bad in ln), bad)
                issues.append(Issue("warn", "parser", "scripts/briefing.py",
                                    f"briefing output may be mangled: {sample[:90]}"))

    return issues


# ---------- holdings index ----------

def generate_holdings_index(notes: list[Note], today: date) -> str:
    """Generate markdown content for holdings/index.md."""
    holdings = [n for n in notes
                if n.folder == "holdings" and n.stem != "index"]
    holdings.sort(key=lambda n: n.stem)

    # Count decisions per holding
    decisions = [n for n in notes
                 if n.folder == "decisions" and n.stem not in {"log", "index"}]
    decision_count: dict[str, int] = {}
    for dec in decisions:
        for m in WIKILINK_RE.finditer(_strip_code(dec.body)):
            t = m.group(1).split("#")[0].strip()
            t = t[:-3] if t.endswith(".md") else t
            if t.startswith("holdings/"):
                ticker = t.split("/", 1)[1]
                decision_count[ticker] = decision_count.get(ticker, 0) + 1

    lines: list[str] = []
    lines.append("---")
    lines.append(f"date: {today.isoformat()}")
    lines.append(f"last_updated: {today.isoformat()}")
    lines.append("type: reference")
    lines.append("tags: [index, holdings, generated]")
    lines.append("---")
    lines.append("")
    lines.append("# Holdings Index")
    lines.append("")
    lines.append(f"> Auto-generated by `scripts/lint.py --write-index` on {today.isoformat()}. "
                 f"Do not edit by hand — re-run lint to refresh.")
    lines.append("")

    if not holdings:
        lines.append("_No holdings files yet._")
        return "\n".join(lines) + "\n"

    lines.append("| Ticker | Status | Conviction | Theme | Decisions | Last Updated | Days Stale |")
    lines.append("|--------|--------|:---:|-------|:---:|--------------|:---:|")
    for h in holdings:
        fm = h.frontmatter
        ticker = f"[[{h.rel_path[:-3]}|{fm.get('ticker', h.stem)}]]"
        status = fm.get("status", "—")
        conv = fm.get("conviction", "—")
        theme = fm.get("theme", "—")
        dcount = decision_count.get(h.stem, 0)
        lu = h.last_updated or h.date
        lu_str = lu.isoformat() if lu else "—"
        days = f"{(today - lu).days}" if lu else "—"
        lines.append(f"| {ticker} | {status} | {conv} | {theme} | {dcount} | {lu_str} | {days} |")

    lines.append("")
    lines.append(f"**Total: {len(holdings)} holdings** "
                 f"(with {sum(decision_count.values())} decisions backlinked).")
    lines.append("")
    return "\n".join(lines) + "\n"


# ---------- reporting ----------

def print_report(issues: list[Issue], file_count: int, today: date) -> int:
    buckets: dict[str, list[Issue]] = {}
    for i in issues:
        buckets.setdefault(i.category, []).append(i)

    order = ["schema", "parser", "wikilink", "backlink", "staleness", "log", "orphan",
             "hypotheses", "decisions", "consistency", "gaps", "backlog", "calendar",
             "sources", "figures"]
    labels = {
        "schema": "SCHEMA",
        "parser": "PARSER CONTRACTS",
        "wikilink": "WIKILINKS",
        "backlink": "BACKLINKS",
        "staleness": "STALENESS",
        "log": "LOG COVERAGE",
        "orphan": "ORPHAN HOLDINGS",
        "hypotheses": "HYPOTHESES OVERDUE",
        "decisions": "STALE DECISIONS",
        "consistency": "CROSS-THESIS CONSISTENCY",
        "gaps": "UNRESOLVED GAPS / UNVERIFIED",
        "backlog": "RESEARCH BACKLOG",
        "calendar": "EVENT CALENDAR",
        "sources": "SOURCE CALLOUT QUALITY",
        "figures": "UNTYPED MARKET FIGURES",
    }

    print(f"Lint Report — {today.isoformat()}")
    print("=" * 40)
    print()

    errors = warns = 0
    for cat in order:
        items = buckets.get(cat, [])
        e = sum(1 for i in items if i.severity == "error")
        w = sum(1 for i in items if i.severity == "warn")
        errors += e
        warns += w
        print(f"{labels[cat]} ({e} errors, {w} warnings)")
        for i in items:
            tag = "err " if i.severity == "error" else "warn"
            print(f"  [{tag}] {i.path}: {i.message}")
        if not items:
            print("  ok")
        print()

    print("-" * 40)
    print(f"Summary: {errors} errors, {warns} warnings across {file_count} files.")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=_DOC.splitlines()[0] if _DOC else "")
    parser.add_argument("--write-index", action="store_true",
                        help="regenerate holdings/index.md")
    parser.add_argument("--today", default=None,
                        help="override today's date (YYYY-MM-DD) for testing")
    args = parser.parse_args()

    today = (datetime.strptime(args.today, "%Y-%m-%d").date()
             if args.today else date.today())

    notes = load_notes()

    all_issues: list[Issue] = []
    all_issues += check_frontmatter(notes)
    all_issues += check_parser_contracts(notes, today)
    all_issues += check_wikilinks(notes)
    all_issues += check_backlinks(notes)
    all_issues += check_staleness(notes, today)
    all_issues += check_log_coverage(notes)
    all_issues += check_orphan_holdings(notes)
    all_issues += check_hypothesis_due(notes, today)
    all_issues += check_decision_outcomes(notes, today)
    all_issues += check_cross_thesis_conviction(notes)
    all_issues += check_callout_gaps(notes)
    all_issues += check_source_callouts(notes)
    all_issues += check_untyped_figures(notes)
    all_issues += check_research_backlog(notes, today)
    all_issues += check_event_calendar(notes, today)

    exit_code = print_report(all_issues, len(notes), today)

    if args.write_index:
        content = generate_holdings_index(notes, today)
        index_path = VAULT_ROOT / "holdings" / "index.md"
        index_path.write_text(content, encoding="utf-8")
        print(f"\nWrote {index_path.relative_to(VAULT_ROOT)}")

    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"lint.py failed: {e}", file=sys.stderr)
        sys.exit(2)
