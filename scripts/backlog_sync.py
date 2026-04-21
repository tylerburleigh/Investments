"""Sync research backlog with gap/unverified callouts in strategy docs.

Scans all strategy docs for [!gap] and [!unverified] callouts, cross-references
against docs/research-backlog.md, and reports:
  - New callouts not yet tracked in the backlog (candidates for entry)
  - Backlog items whose originating callout has been upgraded to [!source]
    or [!analysis] (candidates for closure)

Usage:
    python3 scripts/backlog_sync.py              # dry run (print report only)
    python3 scripts/backlog_sync.py --apply      # write new entries to backlog
    python3 scripts/backlog_sync.py --today 2026-04-19

Exit codes: 0 = no changes needed, 1 = changes available (or applied), 2 = failure.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

VAULT_ROOT = Path(__file__).resolve().parent.parent

FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")

CALLOUT_GAP_RE = re.compile(r">\s*\[!(gap|unverified)\]([^\n]*)", re.IGNORECASE)
CALLOUT_ANY_RE = re.compile(
    r">\s*\[!(source|analysis|gap|unverified)\]([^\n]*)", re.IGNORECASE,
)

CONTENT_FOLDERS = ["holdings", "decisions", "portfolio", "reviews",
                   "strategy", "watchlist", "docs"]


@dataclass
class Note:
    path: Path
    rel_path: str
    stem: str
    folder: str
    frontmatter: dict = field(default_factory=dict)
    body: str = ""
    frontmatter_ok: bool = True
    parse_error: str | None = None

    @property
    def type(self) -> str | None:
        return self.frontmatter.get("type")


@dataclass
class Callout:
    callout_type: str   # "gap", "unverified", "source", "analysis"
    claim_text: str
    note_rel_path: str
    line_number: int


@dataclass
class BacklogEntry:
    item_id: str
    question: str
    thesis_theme: str
    surfaced_from: str
    priority: str
    review_by: str
    status: str
    raw_line: str
    line_number: int


@dataclass
class SyncResult:
    new_callouts: list[tuple[Callout, str]]     # (callout, suggested_id)
    orphaned_entries: list[BacklogEntry]
    matched: list[tuple[Callout, BacklogEntry]]


# --- helpers (standalone copies matching lint.py pattern) ---

def _split_frontmatter(raw: str) -> tuple[str | None, str]:
    if not raw.startswith("---"):
        return None, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return None, raw
    return raw[3:end].strip(), raw[end + 4:]


def _strip_code(body: str) -> str:
    body = FENCED_CODE_RE.sub("", body)
    body = INLINE_CODE_RE.sub("", body)
    return body


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


# --- core logic ---

def _display_name(stem: str) -> str:
    """Convert 'thesis-ai' or 'theme-nuclear' to a display name like 'AI' or 'Nuclear'."""
    parts = stem.split("-", 1)
    if len(parts) == 2:
        name = parts[1]
    else:
        name = stem
    # Map known stems to display names
    names = {
        "ai": "AI", "crypto": "Crypto", "space": "Space",
        "energy-transition": "Energy Transition", "tech-conviction": "Tech Conviction",
        "nuclear": "Nuclear", "ev": "EV", "quantum": "Quantum", "robotics": "Robotics",
    }
    return names.get(name, name.replace("-", " ").title())


def scan_callouts(notes: list[Note]) -> list[Callout]:
    callouts: list[Callout] = []
    for n in notes:
        if n.folder != "strategy" or n.type != "strategy":
            continue
        scan = _strip_code(n.body)
        for i, line in enumerate(scan.splitlines()):
            m = CALLOUT_ANY_RE.search(line)
            if not m:
                continue
            callouts.append(Callout(
                callout_type=m.group(1).lower(),
                claim_text=m.group(2).strip()[:120],
                note_rel_path=n.rel_path,
                line_number=i + 1,
            ))
    return callouts


def _split_table_row(line: str) -> list[str]:
    """Split a markdown table row, handling \\| escapes inside wikilinks."""
    placeholder = "\x00PIPE\x00"
    # Replace \| that appears between [[ and ]] with placeholder
    result = []
    in_wikilink = False
    i = 0
    while i < len(line):
        if line[i:i+2] == "[[":
            in_wikilink = True
            result.append(line[i:i+2])
            i += 2
        elif line[i:i+2] == "]]":
            in_wikilink = False
            result.append(line[i:i+2])
            i += 2
        elif in_wikilink and line[i:i+2] == "\\|":
            result.append(placeholder)
            i += 2
        else:
            result.append(line[i])
            i += 1
    cleaned = "".join(result)
    cells = [c.strip().replace(placeholder, "|") for c in cleaned.split("|")[1:-1]]
    return cells


def parse_backlog() -> tuple[list[BacklogEntry], list[BacklogEntry]]:
    backlog_path = VAULT_ROOT / "docs" / "research-backlog.md"
    if not backlog_path.exists():
        return [], []
    raw = backlog_path.read_text(encoding="utf-8")
    _, body = _split_frontmatter(raw)
    if body is None:
        body = raw

    open_entries: list[BacklogEntry] = []
    resolved_entries: list[BacklogEntry] = []

    current_section = None
    for i, line in enumerate(body.splitlines()):
        s = line.strip()
        if s == "## Open":
            current_section = "open"
            continue
        elif s == "## Resolved":
            current_section = "resolved"
            continue
        elif s.startswith("## "):
            current_section = None
            continue
        if not s.startswith("|") or not s.endswith("|"):
            continue
        cells = _split_table_row(s)
        if len(cells) < 7:
            continue
        item_id = cells[0]
        if not item_id or item_id == "#" or set(item_id.replace(":", "")) <= {"-"}:
            continue
        entry = BacklogEntry(
            item_id=item_id,
            question=cells[1],
            thesis_theme=cells[2],
            surfaced_from=cells[3],
            priority=cells[4],
            review_by=cells[5],
            status=cells[6].lower().strip(),
            raw_line=s,
            line_number=i + 1,
        )
        if current_section == "open":
            open_entries.append(entry)
        elif current_section == "resolved":
            resolved_entries.append(entry)
    return open_entries, resolved_entries


def next_backlog_id(open_entries: list[BacklogEntry],
                    resolved_entries: list[BacklogEntry]) -> str:
    max_num = 0
    for entries in (open_entries, resolved_entries):
        for e in entries:
            m = re.match(r"B(\d+)", e.item_id)
            if m:
                max_num = max(max_num, int(m.group(1)))
    return f"B{max_num + 1:03d}"


def _thesis_wikilink(callout: Callout) -> str:
    """Build the wikilink form for the callout's source doc, e.g. [[strategy/thesis-ai|AI]]."""
    rel = callout.note_rel_path
    if rel.endswith(".md"):
        rel = rel[:-3]
    stem = rel.split("/", 1)[-1] if "/" in rel else rel
    display = _display_name(stem)
    return f"[[{rel}|{display}]]"


def _keyword_overlap(a: str, b: str) -> float:
    """Simple word-overlap score between two strings (0-1)."""
    stop = {"the", "a", "an", "of", "in", "to", "for", "by", "is", "at", "and",
            "or", "from", "with", "this", "that", "not", "but", "its", "it",
            "has", "been", "was", "were", "be", "are", "on", "as", "if"}
    wa = {w.lower() for w in re.findall(r"[a-zA-Z]{3,}", a)} - stop
    wb = {w.lower() for w in re.findall(r"[a-zA-Z]{3,}", b)} - stop
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))


def _match_callout_to_entry(callout: Callout,
                            entries: list[BacklogEntry]) -> BacklogEntry | None:
    """Find the backlog entry matching a callout, or None."""
    wikilink = _thesis_wikilink(callout)
    best: BacklogEntry | None = None
    best_score = 0.0
    for entry in entries:
        if entry.status != "open":
            continue
        # Must match thesis/theme
        thesis_match = wikilink in entry.thesis_theme or callout.note_rel_path.replace(".md", "") in entry.thesis_theme
        if not thesis_match:
            continue
        # Must match callout type
        type_match = f"[!{callout.callout_type}]" in entry.surfaced_from.lower()
        if not type_match:
            continue
        # Score by keyword overlap
        score = _keyword_overlap(callout.claim_text, entry.question)
        if score > best_score:
            best_score = score
            best = entry
    return best


def _find_upgraded_callout(entry: BacklogEntry,
                           callouts: list[Callout]) -> Callout | None:
    """Check if a backlog entry's originating callout was upgraded to [!source] or [!analysis]."""
    for c in callouts:
        if c.callout_type not in ("source", "analysis"):
            continue
        # Must be in the same doc
        entry_stem = entry.thesis_theme
        if not c.note_rel_path.replace(".md", "").split("/")[-1].replace("thesis-", "").replace("theme-", "") in entry_stem:
            # Try wikilink match
            c_rel = c.note_rel_path.replace(".md", "")
            if c_rel not in entry.thesis_theme:
                continue
        # Keyword overlap with the question
        score = _keyword_overlap(c.claim_text, entry.question)
        if score > 0.3:
            return c
    return None


def compute_sync(callouts: list[Callout],
                 open_entries: list[BacklogEntry],
                 next_id: str) -> SyncResult:
    result = SyncResult(new_callouts=[], orphaned_entries=[], matched=[])
    current_id = int(next_id[1:])

    # Match gap/unverified callouts to backlog entries
    for c in callouts:
        if c.callout_type not in ("gap", "unverified"):
            continue
        entry = _match_callout_to_entry(c, open_entries)
        if entry:
            result.matched.append((c, entry))
        else:
            sid = f"B{current_id:03d}"
            current_id += 1
            result.new_callouts.append((c, sid))

    # Check for orphaned entries (backlog items whose callout was upgraded)
    matched_questions = {e.question for _, e in result.matched}
    for entry in open_entries:
        if entry.question in matched_questions:
            continue
        if "[!gap]" not in entry.surfaced_from.lower() and "[!unverified]" not in entry.surfaced_from.lower():
            continue
        upgraded = _find_upgraded_callout(entry, callouts)
        if upgraded:
            result.orphaned_entries.append(entry)

    return result


def format_new_entry(item_id: str, callout: Callout, today: date) -> str:
    wikilink = _thesis_wikilink(callout)
    review_by = (today + timedelta(days=30)).isoformat()
    question = callout.claim_text.replace("|", "-")[:90]
    return (f"| {item_id} | {question} | {wikilink} | "
            f"`[!{callout.callout_type}]` callout | medium | {review_by} | open |")


def apply_new_entries(new_entries: list[tuple[Callout, str]],
                      today: date) -> None:
    backlog_path = VAULT_ROOT / "docs" / "research-backlog.md"
    raw = backlog_path.read_text(encoding="utf-8")
    fm_raw, body = _split_frontmatter(raw)
    body = body if body is not None else raw

    lines = body.splitlines()
    # Find the last row in the Open table (before ## Resolved or end)
    insert_idx = None
    in_open = False
    for i, line in enumerate(lines):
        if line.strip() == "## Open":
            in_open = True
            continue
        if line.strip().startswith("## "):
            if in_open:
                insert_idx = i
                break
            continue
        if in_open and line.strip().startswith("|") and not set(line.strip().replace("|", "").replace("-", "").replace(":", "").replace(" ", "")) <= {""}:
            insert_idx = i + 1

    if insert_idx is None:
        print("Could not find insertion point in backlog", file=sys.stderr)
        return

    new_rows = [format_new_entry(sid, c, today) for c, sid in new_entries]
    for row in reversed(new_rows):
        lines.insert(insert_idx, row)

    new_body = "\n".join(lines)
    if fm_raw is not None:
        new_raw = f"---\n{fm_raw}\n---{new_body}"
    else:
        new_raw = new_body
    backlog_path.write_text(new_raw, encoding="utf-8")


def print_report(result: SyncResult, today: date) -> None:
    print(f"Backlog Sync Report — {today.isoformat()}")
    print("=" * 50)
    print()

    if result.new_callouts:
        print("NEW CALLOUTS (not in backlog)")
        for callout, sid in result.new_callouts:
            review_by = (today + timedelta(days=30)).isoformat()
            print(f"  {callout.note_rel_path}:{callout.line_number} "
                  f"— [!{callout.callout_type}] \"{callout.claim_text[:70]}\"")
            print(f"    Suggested: {sid} | medium | review by {review_by}")
        print()

    if result.orphaned_entries:
        print("ORPHANED BACKLOG ITEMS (callout upgraded)")
        for entry in result.orphaned_entries:
            print(f"  #{entry.item_id} — \"{entry.question[:70]}\"")
            print(f"    Status: {entry.status} | Surfaced from: {entry.surfaced_from}")
        print()

    print(f"ALREADY TRACKED ({len(result.matched)} callouts matched to backlog entries)")
    print()

    print("=" * 50)
    counts = f"{len(result.new_callouts)} new, {len(result.orphaned_entries)} orphaned, {len(result.matched)} matched"
    print(f"Summary: {counts}")


def main() -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--apply", action="store_true",
                        help="write new entries to research-backlog.md")
    parser.add_argument("--today", default=None,
                        help="override today's date (YYYY-MM-DD) for testing")
    args = parser.parse_args()

    today = (datetime.strptime(args.today, "%Y-%m-%d").date()
             if args.today else date.today())

    notes = load_notes()
    callouts = scan_callouts(notes)
    open_entries, resolved_entries = parse_backlog()
    nid = next_backlog_id(open_entries, resolved_entries)
    result = compute_sync(callouts, open_entries, nid)

    print_report(result, today)

    if args.apply and result.new_callouts:
        apply_new_entries(result.new_callouts, today)
        print(f"\nApplied {len(result.new_callouts)} new entries to docs/research-backlog.md")

    has_changes = bool(result.new_callouts or result.orphaned_entries)
    return 1 if has_changes else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"backlog_sync.py failed: {e}", file=sys.stderr)
        sys.exit(2)
