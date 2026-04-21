"""Session briefing — surface what needs attention at session start.

Reads only local vault files. No SnapTrade or external calls.

Usage:
    python3 scripts/briefing.py
    python3 scripts/briefing.py --today 2026-04-19
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import yaml

VAULT_ROOT = Path(__file__).resolve().parent.parent

STALENESS_THRESHOLDS = {
    "strategy_hub": 30,
    "strategy": 180,
    "holding": 90,
}

MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
WIKILINK_HOLDING_RE = re.compile(r"\[\[holdings/([^\]|/]+)")


# ---------- helpers ----------

def _parse_date(val) -> date | None:
    if val is None:
        return None
    if isinstance(val, date) and not isinstance(val, datetime):
        return val
    if isinstance(val, datetime):
        return val.date()
    try:
        return datetime.strptime(str(val).strip('"\''), "%Y-%m-%d").date()
    except ValueError:
        return None


def _load_frontmatter(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    try:
        fm = yaml.safe_load(raw[3:end].strip()) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, raw[end + 4:]


def _strip_code(body: str) -> str:
    return FENCED_CODE_RE.sub("", body)


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


def parse_timeframe(s: str) -> date | None:
    """Parse a hypothesis timeframe string → latest expected evaluation date."""
    import calendar
    s = re.sub(r"\(.*?\)", "", s).strip().lower()
    if not s or s in ("—", "-") or "ongoing" in s or "n/a" in s:
        return None
    # Take the last component of a range "Q3–Q4 2026" → "Q4 2026"
    parts = re.split(r"[–—/]", s)
    s = parts[-1].strip() if len(parts) > 1 else s
    # YYYY-MM-DD
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return _parse_date(m.group(1))
    # Qn YYYY
    m = re.search(r"q([1-4])\s*(\d{4})", s)
    if m:
        q, yr = int(m.group(1)), int(m.group(2))
        mo = q * 3
        return date(yr, mo, calendar.monthrange(yr, mo)[1])
    # Hn YYYY (half-year)
    m = re.search(r"h([12])\s*(\d{4})", s)
    if m:
        half, yr = int(m.group(1)), int(m.group(2))
        mo = 6 if half == 1 else 12
        return date(yr, mo, calendar.monthrange(yr, mo)[1])
    # Mon YYYY ("dec 2026")
    m = re.search(r"([a-z]{3})\s+(\d{4})", s)
    if m:
        mon_str, yr = m.group(1), int(m.group(2))
        mo = MONTH_MAP.get(mon_str)
        if mo:
            return date(yr, mo, calendar.monthrange(yr, mo)[1])
    # bare year
    m = re.search(r"\b(20\d{2})\b", s)
    if m:
        return date(int(m.group(1)), 12, 31)
    return None


def parse_hypothesis_rows(section_text: str) -> list[dict]:
    """Parse Hypotheses table rows → list of {num, text, timeframe, status}."""
    rows = []
    for line in section_text.splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 8:
            continue
        num = cells[0]
        if not num or num == "#" or set(num.replace(":", "")) <= {"-"}:
            continue
        rows.append({
            "num": num,
            "text": cells[1][:55] if len(cells) > 1 else "",
            "timeframe": cells[4] if len(cells) > 4 else "",
            "status": cells[7].lower().strip() if len(cells) > 7 else "open",
        })
    return rows


# ---------- checks ----------

@dataclass
class Item:
    severity: str   # "warn" | "info"
    section: str
    message: str


def check_reviews(today: date) -> list[Item]:
    items = []
    reviews_dir = VAULT_ROOT / "reviews"
    last: dict[str, date | None] = {"weekly": None, "monthly": None, "quarterly": None}

    for rf in sorted(reviews_dir.glob("*.md"), reverse=True):
        fm, _ = _load_frontmatter(rf)
        period = fm.get("period", "")
        d = _parse_date(fm.get("date"))
        if d and period in last and last[period] is None:
            last[period] = d

    def quarter(d: date) -> tuple:
        return (d.year, (d.month - 1) // 3 + 1)

    lw, lm, lq = last["weekly"], last["monthly"], last["quarterly"]

    if lw is None:
        items.append(Item("warn", "reviews", "No weekly review on file"))
    elif (today - lw).days > 7:
        items.append(Item("warn", "reviews", f"Weekly overdue — last was {lw} ({(today - lw).days}d ago)"))
    else:
        items.append(Item("info", "reviews", f"Weekly: {lw} ({(today - lw).days}d ago) ✓"))

    if lm is None:
        items.append(Item("warn", "reviews", "No monthly review on file"))
    elif today.year != lm.year or today.month != lm.month:
        items.append(Item("warn", "reviews", f"Monthly review due — last was {lm}"))
    else:
        items.append(Item("info", "reviews", f"Monthly: {lm} ✓"))

    if lq is None:
        items.append(Item("info", "reviews", "No quarterly review on file"))
    elif quarter(today) != quarter(lq):
        items.append(Item("warn", "reviews", f"Quarterly review due — last was {lq}"))
    else:
        items.append(Item("info", "reviews", f"Quarterly: {lq} ✓"))

    return items


def check_staleness(today: date) -> list[Item]:
    items = []
    stale = []

    hub = VAULT_ROOT / "strategy" / "Investment Strategy.md"
    if hub.exists():
        fm, _ = _load_frontmatter(hub)
        lu = _parse_date(fm.get("last_updated") or fm.get("date"))
        if lu:
            days = (today - lu).days
            if days > STALENESS_THRESHOLDS["strategy_hub"]:
                stale.append(f"Investment Strategy.md ({days}d, threshold {STALENESS_THRESHOLDS['strategy_hub']}d)")

    for path in sorted((VAULT_ROOT / "strategy").glob("*.md")):
        if path.name == "Investment Strategy.md":
            continue
        fm, _ = _load_frontmatter(path)
        if fm.get("type") != "strategy":
            continue
        lu = _parse_date(fm.get("last_updated") or fm.get("date"))
        if lu and (today - lu).days > STALENESS_THRESHOLDS["strategy"]:
            stale.append(f"strategy/{path.name} ({(today - lu).days}d)")

    holdings_stale = 0
    for path in (VAULT_ROOT / "holdings").glob("*.md"):
        if path.stem == "index":
            continue
        fm, _ = _load_frontmatter(path)
        if fm.get("type") != "holding":
            continue
        lu = _parse_date(fm.get("last_updated") or fm.get("date"))
        if lu and (today - lu).days > STALENESS_THRESHOLDS["holding"]:
            holdings_stale += 1

    if stale:
        for s in stale:
            items.append(Item("warn", "staleness", s))
    else:
        items.append(Item("info", "staleness", "All strategy docs within staleness threshold ✓"))

    if holdings_stale:
        items.append(Item("warn", "staleness", f"{holdings_stale} holding(s) not updated in >{STALENESS_THRESHOLDS['holding']}d"))
    elif any(True for _ in (VAULT_ROOT / "holdings").glob("*.md")):
        items.append(Item("info", "staleness", "All holdings within staleness threshold ✓"))

    return items


def check_hypotheses_due(today: date) -> list[Item]:
    items = []
    overdue: list[tuple[int, str]] = []
    upcoming: list[tuple[int, str]] = []

    for path in sorted((VAULT_ROOT / "strategy").glob("*.md")):
        fm, body = _load_frontmatter(path)
        if fm.get("type") != "strategy":
            continue
        section = _section_body(_strip_code(body), "Hypotheses")
        if not section.strip():
            continue
        for row in parse_hypothesis_rows(section):
            if row["status"] in ("confirmed", "disconfirmed", "expired"):
                continue
            tf = parse_timeframe(row["timeframe"])
            if tf is None:
                continue
            delta = (today - tf).days
            label = (f"{path.stem} {row['num']}: {row['text'][:45]}..."
                     f"  [timeframe: {row['timeframe']}]")
            if delta > 0:
                overdue.append((delta, label))
            elif -delta <= 90:
                upcoming.append((-delta, label))

    if overdue:
        for d, label in sorted(overdue, reverse=True):
            items.append(Item("warn", "hypotheses", f"OVERDUE {d}d — {label}"))
    if upcoming:
        for d, label in sorted(upcoming):
            items.append(Item("info", "hypotheses", f"Due in {d}d — {label}"))
    if not overdue and not upcoming:
        items.append(Item("info", "hypotheses", "No hypotheses due within 90 days"))

    return items


def check_backlog(today: date) -> list[Item]:
    items = []
    backlog_path = VAULT_ROOT / "docs" / "research-backlog.md"
    if not backlog_path.exists():
        items.append(Item("warn", "backlog", "docs/research-backlog.md not found"))
        return items

    _, body = _load_frontmatter(backlog_path)
    overdue = []
    upcoming: list[tuple[date, str]] = []

    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 7:
            continue
        num, question = cells[0], cells[1]
        if not num or num == "#" or set(num.replace(":", "")) <= {"-"}:
            continue
        priority, review_by, status = cells[4], cells[5], cells[6]
        if status.lower() in ("resolved", "status"):
            continue
        rd = _parse_date(review_by)
        if rd is None:
            continue
        delta = (today - rd).days
        label = f"#{num} [{priority}] {question[:50]}..."
        if delta > 0:
            overdue.append(f"{label} (was due {review_by})")
        else:
            upcoming.append((rd, f"{label} (due {review_by}, {-delta}d)"))

    if overdue:
        for o in overdue:
            items.append(Item("warn", "backlog", f"Overdue: {o}"))
    else:
        items.append(Item("info", "backlog", "No overdue backlog items ✓"))

    upcoming.sort(key=lambda x: x[0])
    for _, msg in upcoming[:3]:
        items.append(Item("info", "backlog", f"Upcoming: {msg}"))

    return items


def check_snapshot(today: date) -> list[Item]:
    items = []
    snapshots = sorted((VAULT_ROOT / "portfolio").glob("????-??-??.md"), reverse=True)
    if not snapshots:
        items.append(Item("warn", "snapshot", "No portfolio snapshots found"))
        return items

    latest = snapshots[0]
    fm, _ = _load_frontmatter(latest)
    snap_date = _parse_date(fm.get("date") or latest.stem)
    if snap_date:
        days = (today - snap_date).days
        total = fm.get("total_value")
        msg = f"Last: {latest.name} ({days}d ago)"
        if total:
            msg += f"  total ~${float(total):,.0f}"
        sev = "warn" if days > 14 else "info"
        items.append(Item(sev, "snapshot", msg))
    items.append(Item("info", "snapshot",
                       "SnapTrade is opt-in — call mcp__snaptrade__list_positions to refresh"))
    return items


def check_scans(today: date) -> list[Item]:
    items = []
    scans_dir = VAULT_ROOT / "scans"
    if not scans_dir.exists():
        items.append(Item("info", "scans", "scans/ directory not found"))
        return items
    scans = sorted(scans_dir.glob("????-??-??.md"), reverse=True)
    if not scans:
        items.append(Item("warn", "scans", "No scans found — run /weekly-scan"))
        return items
    latest = scans[0]
    scan_date = _parse_date(latest.stem)
    if scan_date:
        days = (today - scan_date).days
        msg = f"Last scan: {latest.name} ({days}d ago)"
        sev = "warn" if days > 7 else "info"
        items.append(Item(sev, "scans", msg))
    return items


def check_session_log(today: date) -> list[Item]:
    items = []
    log_path = VAULT_ROOT / "docs" / "session-log.md"
    if not log_path.exists():
        items.append(Item("info", "session", "docs/session-log.md not found"))
        return items
    _, body = _load_frontmatter(log_path)
    # Find most recent session entry
    last_date = None
    for m in re.finditer(r"### \[(\d{4}-\d{2}-\d{2})\] session", body):
        d = _parse_date(m.group(1))
        if d:
            last_date = d
    if last_date:
        days = (today - last_date).days
        items.append(Item("info", "session", f"Last session: {last_date} ({days}d ago)"))
    else:
        items.append(Item("info", "session", "No session entries found"))
    return items


def check_calendar(today: date) -> list[Item]:
    items = []
    cal_path = VAULT_ROOT / "docs" / "calendar.md"
    if not cal_path.exists():
        return items
    _, body = _load_frontmatter(cal_path)
    upcoming = []
    for line in body.splitlines():
        line = line.strip()
        m = re.match(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|.*- \[ \].*\|", line)
        if not m:
            continue
        event_date = _parse_date(m.group(1))
        if event_date is None:
            continue
        delta = (event_date - today).days
        if 0 <= delta <= 30:
            desc = re.sub(r"\|", "—", line).strip("| ")[:55]
            upcoming.append((delta, desc))
    if upcoming:
        for delta, desc in sorted(upcoming):
            items.append(Item("info", "calendar", f"In {delta}d — {desc}"))
    return items


def count_missing_holdings() -> int:
    existing = {p.stem for p in (VAULT_ROOT / "holdings").glob("*.md")}
    missing = set()
    for path in (VAULT_ROOT / "strategy").glob("*.md"):
        _, body = _load_frontmatter(path)
        for m in WIKILINK_HOLDING_RE.finditer(_strip_code(body)):
            ticker = m.group(1).split("|")[0].strip()
            if ticker and ticker != "index" and ticker not in existing:
                missing.add(ticker)
    return len(missing)


# ---------- report ----------

SECTION_LABELS = {
    "reviews":     "REVIEWS",
    "staleness":   "STALENESS",
    "hypotheses":  "HYPOTHESES DUE",
    "backlog":     "RESEARCH BACKLOG",
    "scans":       "WEEKLY SCAN",
    "snapshot":    "PORTFOLIO SNAPSHOT",
    "session":     "LAST SESSION",
    "calendar":    "UPCOMING EVENTS",
}

SECTION_ORDER = ["reviews", "staleness", "hypotheses", "backlog",
                 "scans", "snapshot", "session", "calendar"]


def print_briefing(items: list[Item], today: date) -> None:
    print(f"Session Briefing — {today}")
    print("=" * 44)

    has_warnings = any(i.severity == "warn" for i in items)

    for section in SECTION_ORDER:
        section_items = [i for i in items if i.section == section]
        if not section_items:
            continue
        warns = sum(1 for i in section_items if i.severity == "warn")
        header = SECTION_LABELS[section]
        if warns:
            header += f"  ⚠  {warns} issue(s)"
        print(f"\n{header}")
        for item in section_items:
            prefix = "  ⚠ " if item.severity == "warn" else "    "
            print(f"{prefix}{item.message}")

    missing = count_missing_holdings()
    if missing:
        print(f"\nMISSING HOLDINGS FILES")
        print(f"    {missing} tickers in thesis docs without holdings/ files")
        print(f"    (normal — create with `python3 scripts/lint.py` to see full list)")

    print(f"\n{'─' * 44}")
    if has_warnings:
        print("Status: ⚠  ACTION NEEDED — address warnings above before proceeding")
    else:
        print("Status: ✓  All clear")
    print("Full validation: python3 scripts/lint.py --write-index")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--today", default=None, help="Override today (YYYY-MM-DD)")
    args = parser.parse_args()
    today = (datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today())

    all_items: list[Item] = []
    all_items += check_reviews(today)
    all_items += check_staleness(today)
    all_items += check_hypotheses_due(today)
    all_items += check_backlog(today)
    all_items += check_scans(today)
    all_items += check_snapshot(today)
    all_items += check_session_log(today)
    all_items += check_calendar(today)

    print_briefing(all_items, today)


if __name__ == "__main__":
    main()
