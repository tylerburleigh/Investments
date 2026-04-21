---
date: 2026-04-18
type: reference
tags: [snaptrade, docs]
---

# SnapTrade MCP Reference

## Overview
SnapTrade is a middleware API that connects to brokerages (WealthSimple in our case) and exposes account data through MCP tools in Claude Code. It provides read access to positions, balances, and account info.

## Connection Details
- **Brokerage**: Wealthsimple Trade (Canadian brokerage)
- **Connection ID**: `a3b6f093-144e-4e9b-944a-57c19bfac95d`
- **Auth Type**: Read-only (UNOFFICIAL_API with 2FA)
- **Connected**: 2026-04-18

## Available MCP Tools

### `mcp__snaptrade__list_connections`
Returns connection details including broker info, auth status, and sync state.

### `mcp__snaptrade__list_accounts`
Returns all accounts with:
- Account name, number, type
- Balance (total value in account currency)
- Sync status (last successful sync for holdings and transactions)
- Account metadata (currency, status, type)

**Our account**: "Wealthsimple Trade CRYPTO" — non-registered, CAD, ~$172K balance reported (but total positions value is higher due to multi-currency holdings)

### `mcp__snaptrade__list_positions`
Returns all open positions with:
- `symbol` — ticker, description, exchange, currency, type (crypto/equity/ETF)
- `price` — current market price
- `units` / `fractional_units` — quantity held
- `average_purchase_price` — cost basis per unit
- `open_pnl` — unrealized profit/loss in position currency
- `currency` — position currency (CAD)
- `cash_equivalent` — whether it's a cash position

## Data Characteristics

### Position Response Structure
```json
{
  "symbol": {
    "symbol": {"symbol": "NVDA", "description": "...", "currency": {...}, "exchange": {...}},
    "description": "...",
    "is_quotable": true,
    "is_tradable": true
  },
  "price": 200.96,
  "units": 51.168,
  "fractional_units": 51.168300,
  "average_purchase_price": 92.28,
  "open_pnl": 5561.05,
  "currency": {"code": "CAD"},
  "cash_equivalent": false
}
```

### Notes
- Position `currency` is the actual trading currency (USD for US-listed, CAD for Canadian-listed). Market values are in position currency — don't sum across currencies without FX conversion.
- WealthSimple supports fractional shares
- Crypto positions are in the same account as equities/ETFs
- Symbols with `.TO` suffix are TSX-listed (Canadian)
- Symbols with `.VN` suffix are TSX Venture
- Symbols with `.NE` suffix are NEO Exchange
- First transaction history goes back to 2022-03-11

## What We Can Do With This Data

### Portfolio Analysis
- Calculate total portfolio value and daily change
- Asset allocation (crypto vs equities vs ETFs, by sector, by geography)
- Concentration analysis (top N holdings as % of portfolio)
- Cost basis tracking and unrealized P&L

### Temporal Tracking
- Snapshot current state into `portfolio/YYYY-MM-DD.md`
- Compare snapshots over time to track drift
- Feed data into review templates

### Decision Support
- Pull current position data before making decisions
- Calculate impact of proposed trades on allocation
- Track conviction against performance

## Limitations
- Read-only access (cannot execute trades through MCP)
- Data freshness depends on SnapTrade sync (real-time connection per WealthSimple)
- No direct access to transaction history through MCP tools (only sync status)
- No options data visible in current positions (only equity, ETF, crypto supported)
- Position amounts are in CAD; US-listed securities may have FX considerations

## Future Enhancements
- Python scripts to automate snapshot creation from position data
- Scheduled snapshots for temporal tracking
- Custom analysis scripts leveraging position data

## Working with MCP Data in Python

When `mcp__snaptrade__list_positions` returns data through Claude Code, the MCP tool result is saved as a JSON file containing `[{type: "text", text: "<json>"}]` — one entry per position. Each `text` field is a JSON string with a deeply nested structure.

**Do not parse this by hand.** Use the existing library:

```python
# From scripts/ directory:
from lib.snaptrade import parse_positions, load_from_file
from lib.models import Position

# From MCP result (the raw list[dict] from the MCP tool):
positions = parse_positions(raw_mcp_result)

# From a saved MCP tool result file (e.g., from .claude/projects/...):
snapshot = load_from_file("/path/to/tool-result-file.txt")
```

### Position model fields
Each `Position` (see `scripts/lib/models.py`) has:
- `.ticker` — e.g., "NVDA", "VIU.TO"
- `.description` — human-readable name
- `.units` — quantity held (float, supports fractional)
- `.price` — current market price
- `.average_cost` — cost basis per unit
- `.market_value` — `units * price` (computed property)
- `.cost_basis` — `units * average_cost` (computed property)
- `.currency` — "USD" or "CAD"
- `.unrealized_pnl` — open profit/loss
- `.return_pct` — percentage return (computed property)
- `.exchange` — exchange code (e.g., "COIN", "TSX")
- `.security_type` — "crypto", "cs" (equity), "et" (ETF)

### Standard pipeline
1. Pull positions via `mcp__snaptrade__list_positions`
2. Save result file path from tool output
3. For snapshots: `python3 scripts/snapshot.py <mcp_result_file> --output portfolio/YYYY-MM-DD.md`
4. For diffs: `python3 scripts/portfolio_diff.py <mcp_result_file>` (value-level, >5% threshold)
5. For DCA verification: use `parse_positions()` and compare `.units` against prior snapshot at the unit level (not value level — daily DCAs are too small to trigger the 5% threshold)
