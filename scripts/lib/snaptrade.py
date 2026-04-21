"""Parse SnapTrade MCP position data into structured models.

This module handles converting raw SnapTrade JSON responses into Position objects.
When used from Claude Code, position data is passed directly. For standalone use,
data can be read from the MCP tool result files.
"""

import json
from pathlib import Path

from .models import Position, PortfolioSnapshot


def parse_positions(raw_positions: list[dict]) -> list[Position]:
    """Parse raw SnapTrade position dicts into Position models."""
    positions = []
    for item in raw_positions:
        text = item.get("text", "")
        d = json.loads(text) if isinstance(text, str) else text

        sym = d.get("symbol", {})
        sym_detail = sym.get("symbol", {})
        ticker = sym_detail.get("symbol", "?")
        description = sym.get("description", "") or sym_detail.get("description", "")
        exchange = sym_detail.get("exchange", {}).get("code", "")
        sec_type = sym_detail.get("type", {}).get("code", "")
        currency = d.get("currency", {}).get("code", "CAD")

        positions.append(Position(
            ticker=ticker,
            description=description,
            units=float(d.get("units") or d.get("fractional_units") or 0),
            price=float(d.get("price") or 0),
            average_cost=float(d.get("average_purchase_price") or 0),
            unrealized_pnl=float(d.get("open_pnl") or 0),
            currency=currency,
            exchange=exchange,
            security_type=sec_type,
            cash_equivalent=d.get("cash_equivalent", False),
        ))
    return positions


def load_from_file(path: str | Path) -> PortfolioSnapshot:
    """Load positions from a SnapTrade MCP tool result file."""
    path = Path(path)
    raw = json.loads(path.read_text())
    positions = parse_positions(raw)
    return PortfolioSnapshot(
        date=path.stat().st_mtime,
        positions=positions,
    )
