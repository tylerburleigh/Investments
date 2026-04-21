"""Generate a portfolio snapshot from SnapTrade MCP tool result file.

Usage:
    python3 -m scripts.snapshot <path_to_mcp_result_file> [--output portfolio/YYYY-MM-DD.md]
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Allow running as module or directly
try:
    from lib.models import PortfolioSnapshot
    from lib.snaptrade import parse_positions
    from lib.render import snapshot_markdown
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from lib.models import PortfolioSnapshot
    from lib.snaptrade import parse_positions
    from lib.render import snapshot_markdown

VAULT_ROOT = Path(__file__).parent.parent


def main():
    parser = argparse.ArgumentParser(description="Generate portfolio snapshot markdown")
    parser.add_argument("input", help="Path to SnapTrade MCP tool result JSON file")
    parser.add_argument("--output", "-o", help="Output markdown file path")
    parser.add_argument("--date", "-d", default=None, help="Date for snapshot (YYYY-MM-DD)")
    args = parser.parse_args()

    raw = json.loads(Path(args.input).read_text())
    positions = parse_positions(raw)
    snap_date = args.date or date.today().isoformat()

    snapshot = PortfolioSnapshot(date=snap_date, positions=positions)
    md = snapshot_markdown(snapshot)

    if args.output:
        out_path = VAULT_ROOT / args.output
        out_path.parent.mkdir(parents=True, exist_ok=True)
        full_md = f"""---
date: {snap_date}
type: snapshot
total_value: {snapshot.total_value:.2f}
position_count: {snapshot.position_count}
accounts: []
---

{md}
"""
        out_path.write_text(full_md)
        print(f"Snapshot written to {out_path}")

        # Write JSON sidecar for portfolio_diff.py
        import json as _json
        sidecar_path = out_path.with_suffix(".json")
        sidecar_data = [
            {
                "ticker": p.ticker,
                "description": p.description,
                "units": p.units,
                "price": p.price,
                "average_cost": p.average_cost,
                "market_value": p.market_value,
                "unrealized_pnl": p.unrealized_pnl,
                "currency": p.currency,
                "security_type": p.security_type,
            }
            for p in snapshot.positions
        ]
        sidecar_path.write_text(_json.dumps(sidecar_data, indent=2))
        print(f"Sidecar written to {sidecar_path}")
    else:
        print(md)


if __name__ == "__main__":
    main()
