"""Compute actual portfolio allocation from latest snapshot and compare to targets.

Reads target allocations from strategy/Investment Strategy.md and actual values
from the most recent portfolio snapshot JSON sidecar.

Usage:
    python3 scripts/allocation_drift.py
    python3 scripts/allocation_drift.py --today 2026-04-19
    python3 scripts/allocation_drift.py --markdown   # output as markdown table
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import yaml

VAULT_ROOT = Path(__file__).resolve().parent.parent


# ---------- category mapping ----------

TICKER_CATEGORY = {
    # Core ETFs
    "VOO": "Core ETFs", "QQQM": "Core ETFs", "VXUS": "Core ETFs",
    "ESGV": "Core ETFs", "XUSR.TO": "Core ETFs", "VSGX": "Core ETFs",
    "VIU.TO": "Core ETFs", "VCN.TO": "Core ETFs", "VFV.TO": "Core ETFs",
    "VEE.TO": "Core ETFs",
    # Crypto
    "BTC": "Crypto", "ETH": "Crypto", "IBIT": "Crypto",
    # Tech Conviction
    "NVDA": "Tech Conviction", "META": "Tech Conviction",
    "GOOG": "Tech Conviction", "MSFT": "Tech Conviction",
    "AMD": "Tech Conviction", "TSM": "Tech Conviction", "MU": "Tech Conviction",
    # Canadian Equity
    "XCSR.TO": "Canadian Equity", "XDSR.TO": "Canadian Equity", "POW.TO": "Canadian Equity",
    # AI Thesis
    "NBIS": "AI", "AMKR": "AI", "IREN": "AI", "APLD": "AI", "NVTS": "AI",
    # Space Thesis
    "RKLB": "Space", "LUNR": "Space", "ASTS": "Space", "MDA.TO": "Space",
    # Energy Transition
    "VST": "Energy Transition", "ELVR": "Energy Transition", "AMPX": "Energy Transition",
    # Nuclear
    "OKLO": "Nuclear", "NLR": "Nuclear", "CCO.TO": "Nuclear",
    # Quantum
    "IONQ": "Quantum", "INFQ": "Quantum",
    # Robotics
    "SYM": "Robotics", "ISRG": "Robotics",
    # EV
    "NIO": "EV",
}

# Map individual thesis categories to the allocation groups in Investment Strategy
CATEGORY_TO_GROUP = {
    "Core ETFs": "Core ETFs",
    "Crypto": "Crypto",
    "Tech Conviction": "Tech Conviction",
    "Canadian Equity": "Canadian Equity",
    "AI": "Thematic Bets",
    "Space": "Thematic Bets",
    "Energy Transition": "Thematic Bets",
    "Nuclear": "Thematic Bets",
    "Quantum": "Thematic Bets",
    "Robotics": "Thematic Bets",
    "EV": "Thematic Bets",
}


# ---------- target parsing ----------

def parse_targets() -> dict[str, float]:
    """Parse target allocation percentages from Investment Strategy.md table."""
    path = VAULT_ROOT / "strategy" / "Investment Strategy.md"
    text = path.read_text(encoding="utf-8")
    targets: dict[str, float] = {}
    in_table = False
    for line in text.splitlines():
        s = line.strip()
        if "| Category | Target |" in s:
            in_table = True
            continue
        if in_table and s.startswith("|"):
            cells = [c.strip() for c in s.split("|")[1:-1]]
            if len(cells) < 3 or cells[0] in ("----------", "---"):
                continue
            if cells[0].lower() in ("category", ""):
                continue
            category = cells[0].split("**")[-1].split("*")[0].strip()
            target_str = cells[1].replace("%", "").strip()
            try:
                targets[category] = float(target_str)
            except ValueError:
                continue
        elif in_table and not s.startswith("|"):
            break
    return targets


# ---------- actual computation ----------

def load_latest_snapshot() -> tuple[str, list[dict]]:
    """Load the most recent snapshot JSON sidecar."""
    snapshots = sorted((VAULT_ROOT / "portfolio").glob("*.json"), reverse=True)
    if not snapshots:
        raise FileNotFoundError("No snapshot JSON sidecars found in portfolio/")
    path = snapshots[0]
    data = json.loads(path.read_text())
    return path.stem, data


def compute_actual(positions: list[dict]) -> dict[str, float]:
    """Compute actual allocation by group."""
    total = sum(p.get("market_value", 0) for p in positions)
    if total == 0:
        return {}
    by_group: dict[str, float] = {}
    unassigned = 0.0
    for p in positions:
        ticker = p.get("ticker", "")
        mv = p.get("market_value", 0)
        cat = TICKER_CATEGORY.get(ticker)
        if cat:
            group = CATEGORY_TO_GROUP.get(cat, "Other")
        else:
            group = "Other"
            unassigned += mv
        by_group[group] = by_group.get(group, 0) + mv

    return {k: round(v / total * 100, 1) for k, v in sorted(by_group.items())}


# ---------- output ----------

@dataclass
class DriftRow:
    group: str
    target: float | None
    actual: float
    drift: float  # actual - target (negative = underweight)

    @property
    def flag(self) -> str:
        if self.target is None:
            return "?"
        if abs(self.drift) > 5:
            return "⚠" if self.drift > 0 else "↓"
        return "✓"


def compute_drift(targets: dict[str, float], actual: dict[str, float]) -> list[DriftRow]:
    all_groups = sorted(set(list(targets.keys()) + list(actual.keys())))
    rows = []
    for g in all_groups:
        t = targets.get(g)
        a = actual.get(g, 0.0)
        d = a - t if t is not None else 0.0
        rows.append(DriftRow(group=g, target=t, actual=a, drift=round(d, 1)))
    return rows


def print_report(rows: list[DriftRow], snapshot_date: str,
                 markdown: bool = False) -> None:
    if markdown:
        print(f"## Allocation Drift (vs {snapshot_date} snapshot)")
        print()
        print("| Category | Target | Actual | Drift | |")
        print("|----------|-------:|-------:|------:|---|")
        for r in rows:
            t_str = f"{r.target:.0f}%" if r.target is not None else "—"
            print(f"| {r.group} | {t_str} | {r.actual:.1f}% | "
                  f"{'+'if r.drift>=0 else ''}{r.drift:.1f}% | {r.flag} |")
        return

    print(f"Allocation Drift — vs {snapshot_date} snapshot")
    print("=" * 50)
    print(f"  {'Category':<18} {'Target':>7} {'Actual':>7} {'Drift':>7}")
    print(f"  {'─'*18} {'─'*7} {'─'*7} {'─'*7}")
    for r in rows:
        t_str = f"{r.target:.0f}%" if r.target is not None else "   —"
        flag = f"  {r.flag}" if r.flag != "✓" else ""
        print(f"  {r.group:<18} {t_str:>7} {r.actual:>6.1f}% "
              f"{'+'if r.drift>=0 else ''}{r.drift:>5.1f}%{flag}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--markdown", action="store_true", help="Output as markdown table")
    args = parser.parse_args()

    targets = parse_targets()
    snapshot_date, positions = load_latest_snapshot()
    actual = compute_actual(positions)
    rows = compute_drift(targets, actual)
    print_report(rows, snapshot_date, markdown=args.markdown)


if __name__ == "__main__":
    main()
