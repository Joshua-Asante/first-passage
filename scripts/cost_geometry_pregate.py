#!/usr/bin/env python3
"""cost_geometry_pregate.py — instrument-ledger Phase-0 cost-geometry pre-gate.

A *mechanical pre-flight* that makes the L-COST-GEOMETRY lesson a gate instead of
a post-hoc finding. Run it on a candidate instrument's canonical TV/Pepperstone
15m series **before any backtest** (operational rule 10 / instrument-ledger
Phase-0 — see `docs/adr/2026-06-22-cost-geometry-pregate.md`).

Why this exists
---------------
The 5th-leg search repeatedly surfaces tight-RANGE mean-reversion candidates
(EURGBP/EURCHF-class crosses) whose edge-style fits the chop regime but whose
cost geometry kills them: a small 15m ATR relative to the spread swamps the
mean-reversion edge. Same failure mode that killed the USOIL spike-fader
(`docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md`,
`lab/analysis/usoil_rdm/RESULTS.md`: realized round-trip cost 0.090R, gross
negative at every target cell — a sub-ATR stop on a wide-spread instrument) and
the USDCAD 15m cost-law finding (`ops/instruments/USDCAD.md` durable finding #1:
0.097R round-trip at a 1.42xATR stop).

The gate
--------
    cost_R = round_trip_cost_price / realized_stop_distance      (geometry only)

with `realized_stop_distance = stop_atr * median(ATR15m)` (or an explicit
`--realized-stop` in price units for confirmation/structural-stop designs). The
headline cost-geometry ratio reported is `median(spread) / median(ATR15m)` — the
cost in R the design would pay at a 1xATR stop; dividing by the stop ATR-multiple
gives the realized `cost_R`.

PASS iff `cost_R < ceiling` (default 0.05R). The 0.05R ceiling is the round-trip
cost a PF~2.0, after-cost leg can absorb with margin: it is consistent with the
standing 4x-median-cost hurdle (post-cost E[R] must clear 4*median_cost ->
0.05R cost implies a 0.20R hurdle, comfortable against a >=0.2R gross edge).
Tune with `--ceiling`.

THE LOAD-BEARING CAVEAT (use the REALIZED stop, not the assumed one)
--------------------------------------------------------------------
The USOIL kill is the worked example of the trap this gate closes: an *assumed*
k*ATR stop reads "comfortable" at the pre-flight, but the *realized* stop of a
confirmation re-entry (stop = spike high) is sub-ATR, so the realized hurdle is
~8x the assumed figure. **`--stop-atr` must be the stop the strategy actually
uses, computed from its realized geometry** — for a confirmation-fade entry whose
stop sits just above a structural level, pass the realized distance via
`--realized-stop`. The report always echoes the implied stop-in-ATR so a sub-ATR
stop is glaringly visible.

Feed-sourcing
-------------
`median(ATR15m)` is computed from the OHLC bars you pass — use the **canonical**
TV-export / Pepperstone 15m series (`core/data/bar_data/<SYMBOL>_M15.csv`, or a
raw BAR EXPORT v0.1 List-of-Trades CSV), per the 2026-06-12 canonical-feed ADR.
`median(spread)` is a broker fact: pass the typical round-trip spread in price
units with `--spread`, or `--spread-col NAME` to take the median of a per-bar
spread column if the export carries one. Slippage / commission are optional
additive terms (`--slippage` per side, `--commission-bps` per side, doubled for
the round trip — mirrors `lab/analysis/ict_cascade_2026-06-18/harness_1m.py`).

Usage
-----
    # Range FX cross candidate, 2xATR stop, 1.2-pip round-trip spread:
    python scripts/cost_geometry_pregate.py \
        --csv core/data/bar_data/EURGBP_M15.csv \
        --symbol EURGBP --spread 0.00012 --stop-atr 2.0

    # Confirmation-fade design with a realized sub-ATR structural stop:
    python scripts/cost_geometry_pregate.py \
        --csv panel.csv --spread 0.08 --realized-stop 0.9

Exit codes: 0 PASS (cost_R < ceiling) · 1 FAIL · 2 usage / data error.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

# BAR EXPORT v0.1 Signal field: epoch_ms|open|high|low|close|volume (volume optional).
# Mirrors core/bar_export_loader.SIGNAL_PIPE_RE, but volume-tolerant so a raw
# OHLC-only export still parses.
_SIGNAL_PIPE_RE = re.compile(
    r"^(?P<epoch>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)(?:\|(?P<v>\d+))?$"
)
_COMMENT_RE = re.compile(
    r"^BAR\|o=(?P<o>[-\d.]+)\|h=(?P<h>[-\d.]+)\|l=(?P<l>[-\d.]+)\|c=(?P<c>[-\d.]+)(?:\|v=(?P<v>\d+))?$"
)

# Cost-geometry bands (price-units round-trip cost in R). Identical thresholds to
# lab/analysis/usoil_rdm/costlaw.py so the two reads agree.
_BANDS = (
    (0.03, "comfortable"),
    (0.06, "acceptable"),
    (0.10, "marginal"),
)


@dataclass
class Bars:
    """Parsed OHLC series + the optional per-bar spread column."""
    high: list[float]
    low: list[float]
    close: list[float]
    spread: Optional[list[float]]  # None unless --spread-col resolved


@dataclass
class GateResult:
    symbol: str
    n_bars: int
    n_atr: int
    atr_period: int
    median_atr: float
    round_trip_spread: float        # the spread term used (price units)
    slippage_per_side: float
    commission_bps_per_side: float
    ref_price: float                # median close (commission notional basis)
    round_trip_cost_price: float    # spread + 2*slip + 2*comm_bps*ref
    stop_atr_mult: Optional[float]  # None when --realized-stop given
    realized_stop: float            # price units
    realized_stop_in_atr: float     # realized_stop / median_atr (sub-ATR flag)
    cost_ratio_1x_atr: float        # median(spread)/median(ATR15m)
    cost_r: float                   # round_trip_cost_price / realized_stop
    ceiling: float
    band: str
    verdict: str                    # PASS | FAIL

    def to_dict(self) -> dict:
        return asdict(self)


# ── feed parsing ───────────────────────────────────────────────

def _decode_signal(text: str) -> Optional[tuple[float, float, float]]:
    """Return (high, low, close) from a BAR EXPORT Signal field, or None."""
    text = str(text).strip()
    m = _SIGNAL_PIPE_RE.match(text) or _COMMENT_RE.match(text)
    if not m:
        return None
    return float(m.group("h")), float(m.group("l")), float(m.group("c"))


def _find_col(fieldnames: list[str], *candidates: str) -> Optional[str]:
    """Case-insensitive lookup of the first present column among candidates."""
    lower = {c.lower().strip(): c for c in fieldnames}
    for cand in candidates:
        if cand.lower() in lower:
            return lower[cand.lower()]
    return None


def parse_ohlc(path: Path, spread_col: Optional[str] = None) -> Bars:
    """Parse a canonical M15 OHLC CSV or a raw BAR EXPORT v0.1 List-of-Trades CSV.

    Accepts either schema:
      * canonical bar feed: time,open,high,low,close[,volume]  (core/data/bar_data/<SYMBOL>_M15.csv)
      * BAR EXPORT v0.1:    a `Signal` (or `Comment`) column = epoch|o|h|l|c[|v]
    Raises ValueError if neither shape is found.
    """
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValueError(f"empty CSV: {path}")
        fields = [f.strip() for f in reader.fieldnames]

        high_c = _find_col(fields, "high", "h")
        low_c = _find_col(fields, "low", "l")
        close_c = _find_col(fields, "close", "c")
        signal_c = _find_col(fields, "Signal", "Comment")
        sp_c = _find_col(fields, spread_col) if spread_col else None
        if spread_col and sp_c is None:
            raise ValueError(f"--spread-col {spread_col!r} not found; columns: {fields}")

        highs: list[float] = []
        lows: list[float] = []
        closes: list[float] = []
        spreads: list[float] = []
        for raw in reader:
            row = {(k.strip() if k else k): v for k, v in raw.items()}
            if high_c and low_c and close_c:
                try:
                    h, l, c = float(row[high_c]), float(row[low_c]), float(row[close_c])
                except (TypeError, ValueError):
                    continue
            elif signal_c:
                dec = _decode_signal(row.get(signal_c, ""))
                if dec is None:
                    continue
                h, l, c = dec
            else:
                raise ValueError(
                    f"CSV has neither high/low/close columns nor a Signal column: {fields}"
                )
            highs.append(h)
            lows.append(l)
            closes.append(c)
            if sp_c is not None:
                try:
                    spreads.append(float(row[sp_c]))
                except (TypeError, ValueError):
                    spreads.append(math.nan)

    if not closes:
        raise ValueError(f"no decodable OHLC rows in {path}")
    return Bars(high=highs, low=lows, close=closes,
                spread=(spreads if sp_c is not None else None))


# ── geometry ───────────────────────────────────────────────────

def wilder_atr(high: list[float], low: list[float], close: list[float],
               period: int = 14) -> list[Optional[float]]:
    """Wilder's ATR. atr[i] is None until index `period`; seeded as the mean of the
    first `period` true ranges, then Wilder-smoothed. Matches the ATR engine used in
    lab/analysis/usoil_rdm/probe4h_canonical.py."""
    n = len(close)
    if n <= period:
        return [None] * n
    tr = [high[0] - low[0]]
    for i in range(1, n):
        tr.append(max(high[i] - low[i],
                      abs(high[i] - close[i - 1]),
                      abs(low[i] - close[i - 1])))
    atr: list[Optional[float]] = [None] * n
    atr[period] = sum(tr[1:period + 1]) / period
    for i in range(period + 1, n):
        atr[i] = (atr[i - 1] * (period - 1) + tr[i]) / period
    return atr


def median_atr(bars: Bars, period: int = 14) -> tuple[float, int]:
    """Median of the defined Wilder-ATR series + the count of defined values."""
    series = wilder_atr(bars.high, bars.low, bars.close, period)
    defined = [a for a in series if a is not None and not math.isnan(a)]
    if not defined:
        raise ValueError("ATR undefined (too few bars for the chosen --atr-period)")
    return statistics.median(defined), len(defined)


def round_trip_cost_price(spread: float, slippage_per_side: float,
                          commission_bps_per_side: float, ref_price: float) -> float:
    """Round-trip execution cost in PRICE units.

    cost = spread + 2*slippage + 2*(commission_bps/10000)*ref_price
    The quoted bid-ask `spread` is already the round-trip crossing cost; slippage
    and commission are per-side and doubled (entry+exit), mirroring the
    `2*comm_pct*entry + 2*slip_tk*mintick` numerator in harness_1m.cost_r.
    """
    return (spread
            + 2.0 * slippage_per_side
            + 2.0 * (commission_bps_per_side / 10_000.0) * ref_price)


def cost_r(round_trip_cost: float, stop_dist: float) -> float:
    """Geometry cost in R = round-trip cost / stop distance. No outcome is read.
    Non-positive stop -> inf (a sub-tick stop is uncapturable)."""
    if stop_dist is None or (isinstance(stop_dist, float) and math.isnan(stop_dist)):
        return math.nan
    if stop_dist <= 0:
        return math.inf
    return round_trip_cost / stop_dist


def classify_band(cr: float) -> str:
    for hi, name in _BANDS:
        if cr <= hi:
            return name
    return "crippling"


# ── evaluation ─────────────────────────────────────────────────

def evaluate(
    bars: Bars,
    *,
    spread: Optional[float],
    stop_atr: Optional[float],
    realized_stop: Optional[float],
    slippage_per_side: float = 0.0,
    commission_bps_per_side: float = 0.0,
    ceiling: float = 0.05,
    atr_period: int = 14,
    symbol: str = "",
) -> GateResult:
    """Run the cost-geometry pre-gate and return a verdict record.

    Exactly one of `spread` (scalar, price units) or `bars.spread` (a per-bar
    column) supplies the spread term; exactly one of `stop_atr` or `realized_stop`
    fixes the stop distance.
    """
    med_atr, n_atr = median_atr(bars, atr_period)
    ref_price = statistics.median(bars.close)

    if bars.spread is not None:
        col = [s for s in bars.spread if not math.isnan(s)]
        if not col:
            raise ValueError("--spread-col resolved but every value was empty/NaN")
        rt_spread = statistics.median(col)
    elif spread is not None:
        rt_spread = spread
    else:
        raise ValueError("supply the spread via --spread or --spread-col")

    if realized_stop is not None:
        stop_dist = realized_stop
        stop_mult: Optional[float] = None
    elif stop_atr is not None:
        stop_dist = stop_atr * med_atr
        stop_mult = stop_atr
    else:
        raise ValueError("supply the stop via --stop-atr or --realized-stop")

    rt_cost = round_trip_cost_price(rt_spread, slippage_per_side,
                                    commission_bps_per_side, ref_price)
    cr = cost_r(rt_cost, stop_dist)
    verdict = "PASS" if (not math.isnan(cr) and not math.isinf(cr) and cr < ceiling) else "FAIL"

    return GateResult(
        symbol=symbol,
        n_bars=len(bars.close),
        n_atr=n_atr,
        atr_period=atr_period,
        median_atr=med_atr,
        round_trip_spread=rt_spread,
        slippage_per_side=slippage_per_side,
        commission_bps_per_side=commission_bps_per_side,
        ref_price=ref_price,
        round_trip_cost_price=rt_cost,
        stop_atr_mult=stop_mult,
        realized_stop=stop_dist,
        realized_stop_in_atr=(stop_dist / med_atr if med_atr else math.inf),
        cost_ratio_1x_atr=(rt_spread / med_atr if med_atr else math.inf),
        cost_r=cr,
        ceiling=ceiling,
        band=classify_band(cr),
        verdict=verdict,
    )


def format_report(r: GateResult) -> str:
    sym = f" [{r.symbol}]" if r.symbol else ""
    lines = [
        f"COST-GEOMETRY PRE-GATE{sym}  (instrument-ledger Phase-0)",
        "=" * 64,
        f"  bars                 : {r.n_bars}  (ATR defined on {r.n_atr}, period {r.atr_period})",
        f"  median ATR15m        : {r.median_atr:.6g}  (price units, feed-sourced)",
        f"  round-trip spread    : {r.round_trip_spread:.6g}",
    ]
    if r.slippage_per_side or r.commission_bps_per_side:
        lines.append(
            f"  + slippage/side      : {r.slippage_per_side:.6g}   "
            f"+ commission/side    : {r.commission_bps_per_side:.6g} bps  (ref {r.ref_price:.6g})"
        )
    lines += [
        f"  round-trip cost      : {r.round_trip_cost_price:.6g}  (price units)",
        f"  cost ratio @1xATR    : {r.cost_ratio_1x_atr:.4f}   = median(spread)/median(ATR15m)",
    ]
    if r.stop_atr_mult is not None:
        lines.append(f"  stop                 : {r.stop_atr_mult:g} x ATR = {r.realized_stop:.6g}")
    else:
        lines.append(
            f"  stop (realized)      : {r.realized_stop:.6g}  "
            f"= {r.realized_stop_in_atr:.2f} x ATR"
        )
    if r.realized_stop_in_atr < 1.0:
        lines.append(
            f"  !! SUB-ATR STOP ({r.realized_stop_in_atr:.2f} x ATR) — the USOIL trap: an "
            "assumed kxATR stop understates this; confirm the REALIZED geometry."
        )
    lines += [
        f"  realized cost_R      : {r.cost_r:.4f} R   [{r.band}]",
        f"  ceiling              : {r.ceiling:.4f} R   (PF~2.0 after-cost; 4x-hurdle-consistent)",
        "-" * 64,
        f"  VERDICT: {r.verdict}"
        + ("" if r.verdict == "PASS"
           else "  — cost geometry swamps the edge; do NOT backtest as specified."),
    ]
    return "\n".join(lines)


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--csv", required=True, type=Path,
                    help="canonical 15m OHLC CSV (core/data/bar_data/<SYMBOL>_M15.csv) "
                         "or a raw BAR EXPORT v0.1 List-of-Trades CSV")
    ap.add_argument("--spread", type=float, default=None,
                    help="round-trip (bid-ask) spread in price units")
    ap.add_argument("--spread-col", default=None,
                    help="instead of --spread: a per-bar spread column to take the median of")
    ap.add_argument("--stop-atr", type=float, default=None,
                    help="REALIZED stop as a multiple of median ATR15m (default 2.0 if "
                         "neither --stop-atr nor --realized-stop given)")
    ap.add_argument("--realized-stop", type=float, default=None,
                    help="realized stop in absolute price units (overrides --stop-atr; "
                         "use for confirmation/structural-stop designs)")
    ap.add_argument("--slippage", type=float, default=0.0,
                    help="per-side slippage in price units (round-trip = 2x)")
    ap.add_argument("--commission-bps", type=float, default=0.0,
                    help="per-side commission in bps of notional (round-trip = 2x)")
    ap.add_argument("--ceiling", type=float, default=0.05,
                    help="cost_R ceiling; PASS iff realized cost_R < ceiling (default 0.05)")
    ap.add_argument("--atr-period", type=int, default=14, help="ATR period (default 14)")
    ap.add_argument("--symbol", default="", help="label for the report")
    ap.add_argument("--json", action="store_true", help="emit the result record as JSON")
    args = ap.parse_args(argv)

    if not args.csv.exists():
        print(f"csv not found: {args.csv}", file=sys.stderr)
        return 2
    if args.spread is None and args.spread_col is None:
        ap.error("supply the spread: --spread <price> or --spread-col <name>")

    stop_atr = args.stop_atr
    if stop_atr is None and args.realized_stop is None:
        stop_atr = 2.0  # documented default stop geometry

    try:
        bars = parse_ohlc(args.csv, spread_col=args.spread_col)
        result = evaluate(
            bars,
            spread=args.spread,
            stop_atr=stop_atr,
            realized_stop=args.realized_stop,
            slippage_per_side=args.slippage,
            commission_bps_per_side=args.commission_bps,
            ceiling=args.ceiling,
            atr_period=args.atr_period,
            symbol=args.symbol,
        )
    except ValueError as exc:
        print(f"cost-geometry pre-gate error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(format_report(result))
    return 0 if result.verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
