"""Compare current SnapTrade positions against the most recent portfolio snapshot.

Usage:
    # Pass current MCP positions JSON; diff against most recent snapshot
    python3 scripts/portfolio_diff.py current_positions.json

    # Diff against a specific snapshot
    python3 scripts/portfolio_diff.py current_positions.json --from portfolio/2026-04-18.md

    # Write the diff as a markdown section to stdout
    python3 scripts/portfolio_diff.py current_positions.json --markdown

The current positions JSON file should contain the raw list_positions MCP result
(same format accepted by scripts/snapshot.py).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent

try:
    from lib.snaptrade import parse_positions
    from lib.models import Position
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from lib.snaptrade import parse_positions
    from lib.models import Position


# ---------- snapshot parsing ----------

def _parse_float(s: str) -> float:
    return float(s.strip().replace(",", "").replace("%", ""))


def positions_from_snapshot_md(path: Path) -> dict[str, float]:
    """Extract {ticker: market_value} from a snapshot markdown file."""
    text = path.read_text(encoding="utf-8")
    in_positions = False
    result: dict[str, float] = {}
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## All Positions"):
            in_positions = True
            continue
        if in_positions and s.startswith("##"):
            break
        if not in_positions or not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.split("|")[1:-1]]
        if len(cells) < 5:
            continue
        ticker = cells[0]
        if not ticker or ticker in ("Ticker", "---", ""):
            continue
        try:
            result[ticker] = _parse_float(cells[4])
        except (ValueError, IndexError):
            continue
    return result


def positions_from_json_sidecar(path: Path) -> dict[str, float]:
    """Read {ticker: market_value} from a snapshot JSON sidecar."""
    data = json.loads(path.read_text())
    return {item["ticker"]: item["market_value"] for item in data}


def load_last_snapshot() -> tuple[Path, dict[str, float]]:
    """Find the most recent snapshot and return its positions."""
    snapshots = sorted((VAULT_ROOT / "portfolio").glob("????-??-??.md"), reverse=True)
    if not snapshots:
        raise FileNotFoundError("No portfolio snapshots found in portfolio/")
    path = snapshots[0]
    # Prefer JSON sidecar if it exists
    sidecar = path.with_suffix(".json")
    if sidecar.exists():
        return path, positions_from_json_sidecar(sidecar)
    return path, positions_from_snapshot_md(path)


# ---------- diff ----------

CHANGE_THRESHOLD = 0.05  # 5%


@dataclass
class PositionChange:
    ticker: str
    old_value: float | None
    new_value: float | None

    @property
    def is_new(self) -> bool:
        return self.old_value is None

    @property
    def is_closed(self) -> bool:
        return self.new_value is None

    @property
    def change_pct(self) -> float:
        if self.old_value and self.new_value:
            return (self.new_value - self.old_value) / self.old_value
        return 0.0

    @property
    def change_abs(self) -> float:
        if self.old_value is None:
            return self.new_value or 0
        if self.new_value is None:
            return -(self.old_value or 0)
        return self.new_value - self.old_value


def compute_diff(
    prev: dict[str, float],
    curr: dict[str, float],
) -> list[PositionChange]:
    changes = []
    all_tickers = set(prev) | set(curr)
    for ticker in sorted(all_tickers):
        old = prev.get(ticker)
        new = curr.get(ticker)
        if old is None:
            changes.append(PositionChange(ticker, None, new))
        elif new is None:
            changes.append(PositionChange(ticker, old, None))
        else:
            pct = abs((new - old) / old) if old else 0
            if pct >= CHANGE_THRESHOLD:
                changes.append(PositionChange(ticker, old, new))
    return changes


# ---------- output ----------

def print_diff(changes: list[PositionChange], from_path: Path,
               prev: dict[str, float], curr: dict[str, float],
               markdown: bool = False) -> None:
    new_pos = [c for c in changes if c.is_new]
    closed = [c for c in changes if c.is_closed]
    moved = [c for c in changes if not c.is_new and not c.is_closed]

    prev_total = sum(prev.values())
    curr_total = sum(curr.values())
    total_change = curr_total - prev_total
    total_pct = (total_change / prev_total * 100) if prev_total else 0

    if markdown:
        lines = [
            f"## Portfolio Diff vs {from_path.name}",
            "",
            f"| Metric | Before | After | Change |",
            f"|--------|-------:|------:|-------:|",
            f"| Total Value | ${prev_total:,.0f} | ${curr_total:,.0f} | "
            f"{'+'if total_change>=0 else ''}{total_change:,.0f} ({total_pct:+.1f}%) |",
            f"| Positions | {len(prev)} | {len(curr)} | {len(curr)-len(prev):+d} |",
        ]
        if new_pos:
            lines += ["", "### New Positions", ""]
            for c in new_pos:
                lines.append(f"- **{c.ticker}** — ${c.new_value:,.0f}")
        if closed:
            lines += ["", "### Closed Positions", ""]
            for c in closed:
                lines.append(f"- **{c.ticker}** — was ${c.old_value:,.0f}")
        if moved:
            lines += ["", f"### Significant Changes (>{CHANGE_THRESHOLD:.0%})", "",
                      "| Ticker | Before | After | Change |",
                      "|--------|-------:|------:|-------:|"]
            for c in sorted(moved, key=lambda x: abs(x.change_pct), reverse=True):
                lines.append(
                    f"| {c.ticker} | ${c.old_value:,.0f} | ${c.new_value:,.0f} | "
                    f"{c.change_pct:+.1f}% |"
                )
        print("\n".join(lines))
        return

    # Plain text
    print(f"Portfolio Diff — vs {from_path.name}")
    print("=" * 44)
    print(f"  Total: ${prev_total:,.0f} → ${curr_total:,.0f}  "
          f"({'+' if total_change >= 0 else ''}{total_change:,.0f}, {total_pct:+.1f}%)")
    print(f"  Positions: {len(prev)} → {len(curr)}")

    if new_pos:
        print(f"\nNEW ({len(new_pos)})")
        for c in new_pos:
            print(f"  + {c.ticker:<12} ${c.new_value:>10,.0f}")
    if closed:
        print(f"\nCLOSED ({len(closed)})")
        for c in closed:
            print(f"  - {c.ticker:<12} was ${c.old_value:>10,.0f}")
    if moved:
        print(f"\nCHANGED >{CHANGE_THRESHOLD:.0%} ({len(moved)})")
        for c in sorted(moved, key=lambda x: abs(x.change_pct), reverse=True):
            arrow = "↑" if c.change_abs >= 0 else "↓"
            print(f"  {arrow} {c.ticker:<12} ${c.old_value:>10,.0f} → ${c.new_value:>10,.0f}"
                  f"  ({c.change_pct:+.1f}%)")
    if not changes:
        print("\n  No significant changes detected.")


# ---------- main ----------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("current", help="Path to current positions JSON (MCP result)")
    parser.add_argument("--from", dest="from_snapshot",
                        help="Snapshot to diff against (default: most recent)")
    parser.add_argument("--markdown", action="store_true",
                        help="Output as markdown section")
    args = parser.parse_args()

    # Load current positions
    raw = json.loads(Path(args.current).read_text())
    current_positions_list = parse_positions(raw)
    curr = {p.ticker: p.market_value for p in current_positions_list}

    # Load previous snapshot
    if args.from_snapshot:
        from_path = VAULT_ROOT / args.from_snapshot
        sidecar = from_path.with_suffix(".json")
        prev = positions_from_json_sidecar(sidecar) if sidecar.exists() \
            else positions_from_snapshot_md(from_path)
    else:
        from_path, prev = load_last_snapshot()

    changes = compute_diff(prev, curr)
    print_diff(changes, from_path, prev, curr, markdown=args.markdown)


if __name__ == "__main__":
    main()
