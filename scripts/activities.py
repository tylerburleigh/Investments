"""Fetch account activities from SnapTrade and detect recurring investment patterns.

Usage:
    python3 scripts/activities.py --detect-recurring
    python3 scripts/activities.py --detect-recurring --output docs/recurring-investments.md
    python3 scripts/activities.py --type BUY --limit 50
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

from snaptrade_client import SnapTrade

VAULT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = Path.home() / ".config" / "snaptrade" / "settings.json"


def load_client() -> tuple[SnapTrade, str, str]:
    raw = json.loads(CONFIG_PATH.read_text())
    p = raw["profiles"]["default"]
    st = SnapTrade(client_id=p["clientId"], consumer_key=p["consumerKey"])
    return st, p["userId"], p["userSecret"]


def get_all_accounts(st: SnapTrade, user_id: str, user_secret: str) -> list[dict]:
    resp = st.account_information.list_user_accounts(user_id=user_id, user_secret=user_secret)
    return resp.body


def get_activities(
    st: SnapTrade,
    user_id: str,
    user_secret: str,
    account_id: str,
    activity_types: str | None = None,
    limit: int = 1000,
) -> list[dict]:
    kwargs = {
        "user_id": user_id,
        "user_secret": user_secret,
        "account_id": account_id,
        "limit": limit,
    }
    if activity_types:
        kwargs["type"] = activity_types
    resp = st.account_information.get_account_activities(**kwargs)
    body = resp.body
    if isinstance(body, dict) and "data" in body:
        return body["data"]
    return body if isinstance(body, list) else []


def detect_recurring(activities: list[dict]) -> list[dict]:
    buys = [a for a in activities if a.get("type") in ("BUY", "REI")]
    ticker_buys: dict[str, list[dict]] = defaultdict(list)
    for a in buys:
        sym = a.get("symbol", {})
        ticker = sym.get("symbol", "UNKNOWN") if isinstance(sym, dict) else "UNKNOWN"
        ticker_buys[ticker].append(a)

    recurring = []
    for ticker, txns in ticker_buys.items():
        if len(txns) < 3:
            continue

        txns_sorted = sorted(txns, key=lambda a: a.get("trade_date", ""))
        dates = []
        for a in txns_sorted:
            raw = a.get("trade_date", "")
            if raw:
                dates.append(raw[:10])
        if len(dates) < 3:
            continue

        date_objs = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
        gaps = [(date_objs[i + 1] - date_objs[i]).days for i in range(len(date_objs) - 1)]
        median_gap = sorted(gaps)[len(gaps) // 2]
        if median_gap <= 0:
            continue

        amounts = [abs(float(a.get("amount", 0) or 0)) for a in txns_sorted]
        median_amount = sorted(amounts)[len(amounts) // 2]

        if median_gap <= 10:
            freq = "weekly"
        elif median_gap <= 18:
            freq = "biweekly"
        elif median_gap <= 35:
            freq = "monthly"
        elif median_gap <= 75:
            freq = "bimonthly"
        else:
            freq = f"every {median_gap} days"

        sym = txns_sorted[0].get("symbol", {})
        desc = sym.get("description", ticker) if isinstance(sym, dict) else ticker

        recurring.append({
            "ticker": ticker,
            "description": desc,
            "frequency": freq,
            "median_gap_days": median_gap,
            "median_amount": median_amount,
            "count": len(txns_sorted),
            "first_date": dates[0],
            "last_date": dates[-1],
        })

    return sorted(recurring, key=lambda r: r["count"], reverse=True)


def recurring_to_markdown(recurring: list[dict], total_activities: int) -> str:
    lines = [
        "---",
        f"date: {date.today().isoformat()}",
        "type: reference",
        "tags: [recurring, dca]",
        "---",
        "",
        "# Recurring Investment Patterns",
        "",
        f"Detected from {total_activities} transactions across all accounts.",
        "",
        "| Ticker | Description | Frequency | Est. Amount | Count | Period |",
        "|--------|-------------|-----------|----------:|------:|--------|",
    ]
    for r in recurring:
        lines.append(
            f"| {r['ticker']} | {r['description'][:30]} | {r['frequency']} | "
            f"${r['median_amount']:,.0f} | {r['count']} | {r['first_date']} — {r['last_date']} |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch SnapTrade activities and detect recurring patterns")
    parser.add_argument("--account", help="Specific account ID (default: all non-zero)")
    parser.add_argument("--type", help="Activity type filter (BUY, SELL, DIVIDEND, etc.)")
    parser.add_argument("--limit", type=int, default=1000, help="Max activities per account")
    parser.add_argument("--detect-recurring", action="store_true", help="Detect recurring buy patterns")
    parser.add_argument("--output", "-o", help="Output file path (relative to vault root)")
    args = parser.parse_args()

    st, user_id, user_secret = load_client()

    print("Fetching accounts...")
    accounts = get_all_accounts(st, user_id, user_secret)
    print(f"Found {len(accounts)} accounts")

    all_activities = []
    for acct in accounts:
        acct_id = acct["id"]
        acct_name = acct["name"]
        balance = acct.get("balance", {}).get("total", {}).get("amount", 0)

        if args.account and acct_id != args.account:
            continue
        if not args.account and (not balance or float(balance) == 0):
            print(f"  Skipping {acct_name} (zero balance)")
            continue

        print(f"  Fetching {acct_name} (${float(balance):,.2f})...")
        try:
            activities = get_activities(st, user_id, user_secret, acct_id, activity_types=args.type, limit=args.limit)
            for a in activities:
                a["_account_id"] = acct_id
                a["_account_name"] = acct_name
            all_activities.extend(activities)
            print(f"    {len(activities)} activities")
        except Exception as e:
            print(f"    Error: {e}")

    print(f"\nTotal: {len(all_activities)} activities")

    if args.detect_recurring:
        print("\nDetecting recurring patterns...")
        recurring = detect_recurring(all_activities)
        if recurring:
            print(f"\n{len(recurring)} recurring patterns:\n")
            for r in recurring:
                print(f"  {r['ticker']:10s} {r['frequency']:12s} ~${r['median_amount']:>8,.0f}  "
                      f"({r['count']}x  {r['first_date']} — {r['last_date']})")
            if args.output:
                md = recurring_to_markdown(recurring, len(all_activities))
                out_path = VAULT_ROOT / args.output
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(md)
                print(f"\nSaved to {out_path}")
        else:
            print("No recurring patterns found")
    else:
        for a in all_activities[:30]:
            sym = a.get("symbol", {})
            ticker = sym.get("symbol", "?") if isinstance(sym, dict) else "?"
            print(f"  {a.get('trade_date', '?')[:10]}  {a.get('type', '?'):12s}  {ticker:10s}  "
                  f"${a.get('amount', '?')}  {a.get('description', '')[:40]}")
        if len(all_activities) > 30:
            print(f"  ... and {len(all_activities) - 30} more (use --output to save all)")


if __name__ == "__main__":
    main()
