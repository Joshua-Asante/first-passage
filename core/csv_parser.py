"""
DXTrade CSV trade history parser.
Ingests raw exports and normalizes to a standard trade format.

ARCHIVAL (2026-07-11, docs/adr/2026-07-11-challenge-era-claims-rescope.md):
the emitting venue (FXIFY DXTrade) closed 2026-07-10 — no new exports can
be produced. Retained as a live core module: it backs the ``tearsheet``
command (quantstats tearsheets on archived CSVs, via core/lib/tearsheet.py)
and its STRATEGY_DAYS table remains the live DOW weekday set for archival
DXTrade tearsheets. (Its former live_journal reconciliation reader
was retired 2026-07-11 — docs/adr/2026-07-11-ops-cfd-estate-retirement.md;
the validate_params DOW-vs-manifest check retired with params.toml
2026-08-03.)

DXTrade exports vary slightly by broker — this parser handles the
Alchemy Markets (FXIFY) format and can be extended for others.

Usage:
    trades = parse_dxtrade_csv("path/to/export.csv")

This core module contains DXTrade parsing only; the ECR/reconcile bridge that
consumed it (ops-owned) was retired 2026-07-11
(docs/adr/2026-07-11-ops-cfd-estate-retirement.md).
"""

import csv
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Trade:
    """A single completed trade (entry + exit)."""
    trade_id: str                    # DXTrade Trade # or deal ID
    instrument: str                  # e.g., XAUUSD, DJ30, USDJPY
    direction: str                   # "long" or "short"
    lots: float                      # position size in lots
    entry_time: datetime
    entry_price: float
    exit_time: datetime
    exit_price: float
    pnl: float                       # realized P&L in account currency
    commission: float = 0.0          # commissions/fees (always a cost)
    swap: float = 0.0               # swap/financing, signed (credits positive)
    net_pnl: float = 0.0            # pnl - |commission| + swap
    strategy: Optional[str] = None   # assigned strategy (Guardian/Striker/Aegis)

    def __post_init__(self):
        if self.net_pnl == 0.0:
            # Swap is signed — credits are positive and must add, not subtract
            # (per docs/external/fxify_swap_rates_2026-05-25.md).
            self.net_pnl = self.pnl - abs(self.commission) + self.swap


# Strategy assignment based on instrument + time
STRATEGY_MAP = {
    "XAUUSD": "Guardian",
    "XAUUSDm": "Guardian",
    "XAUUSDXX": "Guardian",  # DXTrade FXIFY format
    "DJ30": "Striker",
    "DJ30X": "Striker",      # DXTrade FXIFY format
    "US30": "Striker",       # some brokers label it US30
    "US30.cash": "Striker",
    "USDJPY": "Aegis",
    "USDJPYm": "Aegis",
    "USDJPYX": "Aegis",     # DXTrade FXIFY format
    "NAS100": "NAS100",
    "USTEC": "NAS100",      # Pepperstone legacy NASDAQ symbol
    "NDX": "NAS100",
}

# Day-of-week validation (0=Mon, 4=Fri)
STRATEGY_DAYS = {
    "Guardian": {0, 1, 3},       # Mon, Tue, Thu
    "Striker": {1, 4},           # Tue, Fri
    "Aegis": {0, 1, 2},         # Mon, Tue, Wed
    "NAS100": {0, 1},            # Mon, Tue (per v1.0 locked DOW)
}


def _normalize_instrument(raw: str) -> str:
    """Normalize instrument names across brokers."""
    clean = raw.strip().upper().replace("/", "")
    # Strip trailing .X, .XX, .x suffixes (DXTrade convention)
    clean = re.sub(r'\.X+$', '', clean, flags=re.IGNORECASE)
    clean = clean.replace(".", "")
    # Common aliases
    aliases = {
        "US30": "DJ30",
        "US30CASH": "DJ30",
        "WALLSTREET30": "DJ30",
        "GOLDUSD": "XAUUSD",
    }
    return aliases.get(clean, clean)


def _detect_strategy(instrument: str, entry_time: datetime) -> Optional[str]:
    """Auto-detect strategy from instrument and entry time."""
    normalized = _normalize_instrument(instrument)
    strategy = STRATEGY_MAP.get(normalized)

    if strategy and entry_time:
        day = entry_time.weekday()
        expected_days = STRATEGY_DAYS.get(strategy, set())
        if day not in expected_days:
            # Trade on unexpected day — flag but still assign
            print(f"  ⚠ {strategy} trade on {entry_time.strftime('%A')} "
                  f"(expected: {expected_days})")
    return strategy


def _parse_datetime(s: str) -> datetime:
    """Parse datetime from various DXTrade formats."""
    s = s.strip()
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        # Day-first is the documented DXTrade convention (historical
        # dxtrade_pdf_to_csv emitter, retired 2026-07-11 with the CFD estate;
        # DD/MM/YYYY) — all day-first formats before month-first. %y
        # variants before %Y: strptime's %Y accepts 2-digit years, so
        # "01/04/26" would otherwise become year 26.
        "%d/%m/%y %H:%M:%S",    # DXTrade FXIFY: 01/04/26 08:30:00
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%y %H:%M",       # DXTrade FXIFY: 01/04/26 08:30
        "%d/%m/%Y %H:%M",
        # Month-first last-resort only (unambiguous strings with day > 12).
        "%m/%d/%Y %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: '{s}'")


def _parse_float(s: str) -> float:
    """Parse float, handling commas, currency symbols, and em dashes."""
    if not s or s.strip() in ("", "-", "N/A", "—", "\u2014"):
        return 0.0
    clean = re.sub(r'[,$€£¥\s]', '', s.strip())
    # Handle K suffix for volume (e.g., "1,080 K" -> 1080000)
    if clean.upper().endswith('K'):
        return float(clean[:-1]) * 1000
    return float(clean)


def parse_dxtrade_csv(filepath: str) -> list[Trade]:
    """
    Parse a DXTrade CSV export into normalized Trade objects.

    Handles two common export formats:
    1. Trade-level (one row per completed trade with P&L)
    2. Order-level (separate open/close rows that need matching)

    Returns list of Trade objects sorted by exit_time.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {filepath}")

    with open(path, 'r', encoding='utf-8-sig') as f:
        # Sniff delimiter
        sample = f.read(2048)
        f.seek(0)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
        except csv.Error:
            dialect = csv.excel

        reader = csv.DictReader(f, dialect=dialect)
        headers = [h.strip().lower() for h in (reader.fieldnames or [])]

        if not headers:
            raise ValueError("CSV has no headers")

        # Detect format based on headers
        rows = list(reader)

    print(f"Loaded {len(rows)} rows from {path.name}")
    print(f"Headers: {headers}")

    # Try trade-level parsing first (most common DXTrade export)
    trades = _try_trade_level_parse(rows, headers)

    if not trades:
        # Try order-level matching
        trades = _try_order_level_parse(rows, headers)

    if not trades:
        print("\n⚠ Could not parse trades. Detected headers:")
        for i, h in enumerate(headers):
            print(f"  [{i}] {h}")
        print("\nPlease share a sample row so the parser can be calibrated.")
        return []

    # Assign strategies
    for t in trades:
        if not t.strategy:
            t.strategy = _detect_strategy(t.instrument, t.entry_time)

    trades.sort(key=lambda t: t.exit_time)
    print(f"Parsed {len(trades)} completed trades")
    return trades


def _find_header(headers: list[str], candidates: list[str]) -> Optional[str]:
    """Find a header matching any candidate (case-insensitive partial match)."""
    for candidate in candidates:
        for h in headers:
            if candidate.lower() in h.lower():
                return h
    return None


def _normalize_header(header: str) -> str:
    """Normalize punctuation and spacing for deterministic header matching."""
    return " ".join(re.findall(r"[a-z0-9]+", header.casefold()))


def _get_val(row: dict, headers: list[str], candidates: list[str]) -> str:
    """Get a value using prioritized exact matching, then unambiguous partial matching."""
    del headers  # Retained in the signature for parser-call compatibility.
    normalized_keys = {key: _normalize_header(key) for key in row}

    for candidate in candidates:
        normalized_candidate = _normalize_header(candidate)
        matches = [
            key for key, normalized in normalized_keys.items()
            if normalized == normalized_candidate
        ]
        if len(matches) == 1:
            value = row[matches[0]]
            return value.strip() if value else ""
        if len(matches) > 1:
            raise ValueError(
                f"Ambiguous exact CSV headers for {candidate!r}: {matches}"
            )

    for candidate in candidates:
        normalized_candidate = _normalize_header(candidate)
        matches = [
            key for key, normalized in normalized_keys.items()
            if normalized_candidate in normalized
        ]
        if len(matches) == 1:
            value = row[matches[0]]
            return value.strip() if value else ""
        if len(matches) > 1:
            raise ValueError(
                f"Ambiguous CSV headers for {candidate!r}: {matches}"
            )
    return ""


def _try_trade_level_parse(rows: list[dict], headers: list[str]) -> list[Trade]:
    """Parse format where each row is a completed trade."""
    trades = []
    skipped = 0

    for row in rows:
        try:
            # Flexible field extraction
            trade_id = (_get_val(row, headers, ["trade #", "trade_id", "deal", "position", "ticket", "order"])
                       or str(len(trades) + 1))
            instrument = _get_val(row, headers, ["symbol", "instrument", "asset", "pair", "market"])
            direction_raw = _get_val(row, headers, ["side", "direction", "type", "action", "buy/sell"])
            lots_raw = _get_val(row, headers, ["volume", "lots", "qty", "quantity", "size", "amount"])
            entry_time_raw = _get_val(row, headers, ["open time", "entry time", "open date", "entry_time"])
            entry_price_raw = _get_val(row, headers, ["open price", "entry price", "entry_price"])
            exit_time_raw = _get_val(row, headers, ["close time", "exit time", "close date", "exit_time"])
            exit_price_raw = _get_val(row, headers, ["close price", "exit price", "exit_price"])
            pnl_raw = _get_val(row, headers, ["profit", "p&l", "pnl", "p/l", "result", "net_pnl", "gross"])
            commission_raw = _get_val(row, headers, ["commission", "comm", "fee"])
            swap_raw = _get_val(row, headers, ["swap", "financing", "rollover"])

            # Skip rows without essential data
            if not instrument or not entry_time_raw or not exit_time_raw:
                continue

            # Parse direction
            direction = "long"
            if direction_raw.lower() in ("sell", "short", "s"):
                direction = "short"

            trade = Trade(
                trade_id=trade_id.strip(),
                instrument=instrument,
                direction=direction,
                lots=_parse_float(lots_raw),
                entry_time=_parse_datetime(entry_time_raw),
                entry_price=_parse_float(entry_price_raw),
                exit_time=_parse_datetime(exit_time_raw),
                exit_price=_parse_float(exit_price_raw),
                pnl=_parse_float(pnl_raw),
                commission=_parse_float(commission_raw),
                swap=_parse_float(swap_raw),
            )
            trades.append(trade)

        except (ValueError, KeyError):
            # Could be summary rows — but never drop silently
            skipped += 1
            continue

    if skipped:
        print(f"  ⚠ skipped {skipped} unparseable rows (of {len(rows)})",
              file=sys.stderr)
    return trades


def _try_order_level_parse(rows: list[dict], headers: list[str]) -> list[Trade]:
    """
    Parse DXTrade order-level format with separate Opening/Closing rows.

    Each row has a Position effect (Opening/Closing) and a Trade Code like
    "16859801:361012". Opening and Closing rows are matched by instrument,
    volume, and chronological order (FIFO within each instrument+volume bucket).

    P&L only appears on Closing rows (Closed P&L / Net Closed P&L columns).
    Commission shows "—" (em dash) when zero.
    """
    # Check if this looks like an order-level format
    has_position_effect = any("position" in h.lower() for h in headers)
    if not has_position_effect:
        return []

    openings: dict[str, list[dict]] = {}  # key: instrument -> list of opening rows
    closings: list[dict] = []

    for row in rows:
        pos_effect = _get_val(row, headers, ["position effect", "position_effect"]).lower().strip()
        if not pos_effect:
            continue

        if pos_effect == "opening":
            instrument = _get_val(row, headers, ["symbol", "instrument"])
            openings.setdefault(instrument, []).append(row)
        elif pos_effect == "closing":
            closings.append(row)

    if not openings and not closings:
        return []

    print(f"  Order-level format: {sum(len(v) for v in openings.values())} opens, "
          f"{len(closings)} closes")

    trades = []
    # Track which openings have been matched
    used_openings: set[int] = set()  # index by id(row)

    def close_time_key(row: dict) -> datetime:
        try:
            raw = _get_val(row, headers, ["date and time", "date", "time"])
            return _parse_datetime(raw)
        except ValueError:
            return datetime.max

    skipped_unmatched = 0
    for close_row in sorted(closings, key=close_time_key):
        try:
            instrument = _get_val(close_row, headers, ["symbol", "instrument"])
            close_time_raw = _get_val(close_row, headers, ["date and time", "date", "time"])
            close_side = _get_val(close_row, headers, ["side"]).lower().strip()
            close_volume = _parse_float(_get_val(close_row, headers, ["trade volume", "volume", "lots"]))
            close_price = _parse_float(_get_val(close_row, headers, ["trade price", "price"]))
            trade_code = _get_val(close_row, headers, ["trade code"])
            pnl_raw = _get_val(close_row, headers, ["closed p&l", "closed pnl", "profit", "p&l"])
            net_pnl_raw = _get_val(close_row, headers, ["net closed p&l", "net closed pnl", "net_pnl"])
            commission_raw = _get_val(close_row, headers, ["commission", "comm", "fee"])

            if not instrument or not close_time_raw:
                continue

            close_time = _parse_datetime(close_time_raw)
            pnl = _parse_float(pnl_raw)
            net_pnl = _parse_float(net_pnl_raw) if net_pnl_raw else pnl
            commission = _parse_float(commission_raw)

            # Find matching opening row: same instrument, same volume, FIFO
            candidates = []
            for open_row in openings.get(instrument, []):
                if id(open_row) in used_openings:
                    continue
                open_volume = _parse_float(_get_val(open_row, headers, ["trade volume", "volume", "lots"]))
                if abs(open_volume - close_volume) < 0.001:
                    open_time_raw = _get_val(open_row, headers, ["date and time", "date", "time"])
                    open_time = _parse_datetime(open_time_raw)
                    if open_time <= close_time:
                        candidates.append((open_time, open_row))

            if not candidates:
                skipped_unmatched += 1
                print(
                    f"  ⚠ Skipping unmatched close row for {instrument} at "
                    f"{close_time.isoformat()}",
                    file=sys.stderr,
                )
                continue

            open_time, matched_open = min(candidates, key=lambda candidate: candidate[0])
            used_openings.add(id(matched_open))
            open_price = _parse_float(_get_val(matched_open, headers, ["trade price", "price"]))
            open_side = _get_val(matched_open, headers, ["side"]).lower().strip()

            # Determine direction: if the opening side is Buy, it's a long trade
            direction = "long" if open_side == "buy" else "short"

            trade_id = trade_code or _get_val(close_row, headers, ["order id", "order_id"])

            trade = Trade(
                trade_id=trade_id,
                instrument=instrument,
                direction=direction,
                lots=close_volume,
                entry_time=open_time,
                entry_price=open_price,
                exit_time=close_time,
                exit_price=close_price,
                pnl=pnl,
                commission=abs(commission),
                net_pnl=net_pnl,
            )
            trades.append(trade)

        except (ValueError, KeyError) as e:
            print(f"  ⚠ Skipping close row: {e}")
            continue

    if skipped_unmatched:
        print(
            f"  ⚠ skipped {skipped_unmatched} unmatched close rows",
            file=sys.stderr,
        )
    return trades


def summarize_trades(trades: list[Trade]) -> dict:
    """Quick summary statistics for a list of trades."""
    if not trades:
        return {"error": "No trades to summarize"}

    wins = [t for t in trades if t.net_pnl > 0]
    losses = [t for t in trades if t.net_pnl <= 0]
    total_pnl = sum(t.net_pnl for t in trades)
    gross_wins = sum(t.net_pnl for t in wins) if wins else 0
    gross_losses = abs(sum(t.net_pnl for t in losses)) if losses else 0

    # Daily P&L for drawdown calc
    daily_pnl: dict[str, float] = {}
    for t in trades:
        day = t.exit_time.strftime("%Y-%m-%d")
        daily_pnl[day] = daily_pnl.get(day, 0) + t.net_pnl

    # Max drawdown from cumulative daily P&L
    cumulative = 0.0
    peak = 0.0
    max_dd = 0.0
    for day in sorted(daily_pnl.keys()):
        cumulative += daily_pnl[day]
        peak = max(peak, cumulative)
        dd = peak - cumulative
        max_dd = max(max_dd, dd)

    # Strategy breakdown
    by_strategy: dict[str, list[Trade]] = {}
    for t in trades:
        s = t.strategy or "Unknown"
        by_strategy.setdefault(s, []).append(t)

    # Trading days
    trading_days = set()
    for t in trades:
        trading_days.add(t.entry_time.strftime("%Y-%m-%d"))

    return {
        "total_trades": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": len(wins) / len(trades) * 100 if trades else 0,
        "total_pnl": total_pnl,
        "profit_factor": gross_wins / gross_losses if gross_losses > 0 else float('inf'),
        "avg_win": gross_wins / len(wins) if wins else 0,
        "avg_loss": gross_losses / len(losses) if losses else 0,
        "max_drawdown": max_dd,
        "worst_daily_pnl": min(daily_pnl.values()) if daily_pnl else 0,
        "best_daily_pnl": max(daily_pnl.values()) if daily_pnl else 0,
        "trading_days": len(trading_days),
        "strategies": list(by_strategy.keys()),
        "date_range": (
            min(t.entry_time for t in trades).strftime("%Y-%m-%d"),
            max(t.exit_time for t in trades).strftime("%Y-%m-%d"),
        ),
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python dxtrade_parser.py <csv_path>")
        print("  Parses a DXTrade CSV export and prints trade summary.")
        sys.exit(1)

    trades = parse_dxtrade_csv(sys.argv[1])
    if trades:
        summary = summarize_trades(trades)
        print(f"\n{'='*50}")
        print(f"TRADE SUMMARY")
        print(f"{'='*50}")
        print(f"  Period: {summary['date_range'][0]} to {summary['date_range'][1]}")
        print(f"  Trading days: {summary['trading_days']}")
        print(f"  Total trades: {summary['total_trades']}")
        print(f"  Win rate: {summary['win_rate']:.1f}%")
        print(f"  Total P&L: ${summary['total_pnl']:,.2f}")
        print(f"  Profit factor: {summary['profit_factor']:.2f}")
        print(f"  Avg win: ${summary['avg_win']:,.2f}")
        print(f"  Avg loss: ${summary['avg_loss']:,.2f}")
        print(f"  Max DD: ${summary['max_drawdown']:,.2f}")
        print(f"  Worst day: ${summary['worst_daily_pnl']:,.2f}")
        print(f"  Best day: ${summary['best_daily_pnl']:,.2f}")
        print(f"  Strategies: {', '.join(summary['strategies'])}")
