"""Generate Markdown content for portfolio snapshots and reports."""

from .models import PortfolioSnapshot, Position


def position_table(positions: list[Position], sort_by: str = "value") -> str:
    """Render positions as a Markdown table."""
    key_funcs = {
        "value": lambda p: p.market_value,
        "ticker": lambda p: p.ticker,
        "pnl": lambda p: p.unrealized_pnl,
        "return": lambda p: p.return_pct,
    }
    sorted_positions = sorted(positions, key=key_funcs.get(sort_by, key_funcs["value"]), reverse=True)

    lines = [
        "| Ticker | Description | Units | Price | Value | Avg Cost | P&L | Return % |",
        "|--------|-------------|------:|------:|------:|--------:|----:|--------:|",
    ]
    for p in sorted_positions:
        lines.append(
            f"| {p.ticker} | {p.description[:30]} | {p.units:.4f} | "
            f"{p.price:,.2f} | {p.market_value:,.2f} | {p.average_cost:,.2f} | "
            f"{p.unrealized_pnl:,.2f} | {p.return_pct:.1f}% |"
        )
    return "\n".join(lines)


def allocation_table(alloc: dict[str, float]) -> str:
    """Render an allocation dict as a Markdown table."""
    lines = [
        "| Category | Allocation |",
        "|----------|----------:|",
    ]
    for k, v in sorted(alloc.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {k} | {v:.1f}% |")
    return "\n".join(lines)


def snapshot_markdown(snapshot: PortfolioSnapshot) -> str:
    """Generate a full snapshot Markdown document."""
    lines = [
        f"# Portfolio Snapshot — {snapshot.date}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Total Value | {snapshot.total_value:,.2f} |",
        f"| Total Cost Basis | {snapshot.total_cost_basis:,.2f} |",
        f"| Unrealized P&L | {snapshot.total_unrealized_pnl:,.2f} |",
        f"| # Positions | {snapshot.position_count} |",
        "",
        "## Top Holdings",
        "",
        position_table(snapshot.top_holdings(10)),
        "",
        "## Allocation by Type",
        "",
        allocation_table(snapshot.allocation_by_type()),
        "",
        "## Allocation by Geography",
        "",
        allocation_table(snapshot.allocation_by_geography()),
        "",
        "## All Positions",
        "",
        position_table(snapshot.positions),
    ]
    return "\n".join(lines)
