"""Show actual DCA buys from recent trading days.

Useful for verifying recurring buy amounts match your targets, since
WealthSimple may spread buys across days and amounts can differ from
the recurring setting due to currency conversion (CAD vs USD).

Usage:
    python3 scripts/recent_buys.py              # last 5 trading days
    python3 scripts/recent_buys.py --days 3     # last 3 trading days
    python3 scripts/recent_buys.py --account REGISTERED
    python3 scripts/recent_buys.py --summary    # aggregate by ticker across days
"""

import argparse
import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from snaptrade_client import SnapTrade

CONFIG_PATH = Path.home() / ".config" / "snaptrade" / "settings.json"


def load_client():
    raw = json.loads(CONFIG_PATH.read_text())
    p = raw["profiles"]["default"]
    st = SnapTrade(client_id=p["clientId"], consumer_key=p["consumerKey"])
    return st, p["userId"], p["userSecret"]


def fetch_recent_buys(days: int = 5, account_filter: str | None = None):
    st, user_id, user_secret = load_client()

    resp = st.account_information.list_user_accounts(user_id=user_id, user_secret=user_secret)
    accounts = resp.body

    buys = []
    cutoff = (date.today() - timedelta(days=days + 2)).isoformat()

    for acct in accounts:
        acct_id = acct["id"]
        acct_name = acct["name"]
        balance = float(acct.get("balance", {}).get("total", {}).get("amount", 0))

        if account_filter and account_filter.lower() not in acct_name.lower():
            continue
        if not balance:
            continue

        try:
            resp = st.account_information.get_account_activities(
                user_id=user_id,
                user_secret=user_secret,
                account_id=acct_id,
                limit=100,
            )
            body = resp.body
            acts = body.get("data", body) if isinstance(body, dict) else body
        except Exception:
            continue

        for a in acts:
            if a.get("type") not in ("BUY", "REI"):
                continue
            td = a.get("trade_date", "")[:10]
            if td < cutoff:
                continue
            sym = a.get("symbol", {})
            ticker = sym.get("symbol", "?") if isinstance(sym, dict) else "?"
            buys.append({
                "date": td,
                "ticker": ticker,
                "quantity": float(a.get("quantity", 0)),
                "price": float(a.get("price", 0)),
                "amount": abs(float(a.get("amount", 0))),
                "account": acct_name,
            })

    return sorted(buys, key=lambda x: (x["date"], x["account"], x["ticker"]), reverse=True)


def print_daily(buys):
    by_date = defaultdict(list)
    for b in buys:
        by_date[b["date"]].append(b)

    for d in sorted(by_date, reverse=True):
        day_buys = by_date[d]
        print(f"\n=== {d} ({len(day_buys)} buys) ===")

        current_acct = None
        day_total = 0
        acct_total = 0

        for b in sorted(day_buys, key=lambda x: (x["account"], x["ticker"])):
            if b["account"] != current_acct:
                if current_acct is not None:
                    print(f"  {'':>10s}  {'':>8s}  {'':>9s}  ${acct_total:>8.2f}  ({current_acct} subtotal)")
                current_acct = b["account"]
                acct_total = 0
            print(f"  {b['ticker']:10s}  {b['quantity']:>8.4f}  @ ${b['price']:>9.2f}  = ${b['amount']:>8.2f}")
            acct_total += b["amount"]
            day_total += b["amount"]

        print(f"  {'':>10s}  {'':>8s}  {'':>9s}  ${acct_total:>8.2f}  ({current_acct} subtotal)")
        print(f"  {'':>10s}  {'':>8s}  {'':>9s}  ${day_total:>8.2f}  (DAY TOTAL)")


def print_summary(buys):
    ticker_stats = defaultdict(lambda: {"amounts": [], "count": 0, "account": None})
    for b in buys:
        key = b["ticker"]
        ticker_stats[key]["amounts"].append(b["amount"])
        ticker_stats[key]["count"] += 1
        ticker_stats[key]["account"] = b["account"]

    print("\n=== Aggregated by ticker (sorted by total $) ===\n")
    print(f"  {'Ticker':10s}  {'Avg $/day':>10s}  {'Median':>8s}  {'Min':>8s}  {'Max':>8s}  {'Buys':>5s}  Account")
    print(f"  {'---':10s}  {'---':>10s}  {'---':>8s}  {'---':>8s}  {'---':>8s}  {'---':>5s}  ---")

    rows = []
    for ticker, stats in ticker_stats.items():
        amounts = stats["amounts"]
        avg = sum(amounts) / len(amounts)
        median = sorted(amounts)[len(amounts) // 2]
        rows.append((ticker, avg, median, min(amounts), max(amounts), stats["count"], stats["account"]))

    rows.sort(key=lambda x: x[1], reverse=True)
    grand_total = 0
    for ticker, avg, median, mn, mx, count, acct in rows:
        print(f"  {ticker:10s}  ${avg:>9.2f}  ${median:>7.2f}  ${mn:>7.2f}  ${mx:>7.2f}  {count:>5d}  {acct}")
        grand_total += avg

    print(f"\n  Estimated daily total: ${grand_total:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Show recent DCA buys from SnapTrade")
    parser.add_argument("--days", type=int, default=5, help="Look back N calendar days (default 5)")
    parser.add_argument("--account", help="Filter by account name (substring match)")
    parser.add_argument("--summary", action="store_true", help="Aggregate by ticker instead of daily view")
    args = parser.parse_args()

    buys = fetch_recent_buys(days=args.days, account_filter=args.account)

    if not buys:
        print("No buys found in the period.")
        return

    if args.summary:
        print_summary(buys)
    else:
        print_daily(buys)


if __name__ == "__main__":
    main()
