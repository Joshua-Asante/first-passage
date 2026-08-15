"""MYM-3FPS-1 Phase-0 third-Friday settlement-reversal delta extraction.

The frozen candidate shorts MYM at the 09:30 ET open on each third Friday and
covers at 12:00 ET.  K=0: this measures the native-micro cohort before any
registered confirmation campaign.
"""
from __future__ import annotations

import argparse
import calendar
import json
import math
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

ET = "America/New_York"
START_DATE = date(2019, 5, 6)
END_DATE_EXCLUSIVE = date(2026, 7, 21)
MIN_COVERAGE_RATE = 0.90
POWER_Z = 1.96
COST_MULTIPLE = 4.0
MYM_MULTIPLIER_USD = 0.50
MYM_TICK_SLIPPAGE_USD_PER_SIDE = 0.50
TRADEIFY_COST_PER_SIDE_USD = 0.91
MFFU_COST_PER_SIDE_USD = 0.95


@dataclass(frozen=True)
class Summary:
    n: int
    mean_bp: float
    sigma_bp: float
    delta_over_sigma: float
    t_stat: float
    confirm_power: float


def third_fridays(start: date, end_exclusive: date) -> list[date]:
    """Return calendar third Fridays in [start, end_exclusive)."""
    dates: list[date] = []
    year, month = start.year, start.month
    while (year, month) <= (end_exclusive.year, end_exclusive.month):
        month_days = calendar.Calendar().monthdatescalendar(year, month)
        fridays = [
            day
            for week in month_days
            for day in week
            if day.month == month and day.weekday() == calendar.FRIDAY
        ]
        candidate = fridays[2]
        if start <= candidate < end_exclusive:
            dates.append(candidate)
        month += 1
        if month == 13:
            year += 1
            month = 1
    return dates


def _exact_bar(frame: pd.DataFrame, timestamp: pd.Timestamp) -> pd.Series | None:
    try:
        row = frame.loc[timestamp]
    except KeyError:
        return None
    if isinstance(row, pd.DataFrame):
        row = row.iloc[-1]
    return row


def build_events(frame: pd.DataFrame, event_dates: list[date]) -> pd.DataFrame:
    """Extract Thursday 15:59 close, Friday 09:30 open, and Friday noon open."""
    rows: list[dict[str, object]] = []
    for event_date in event_dates:
        friday = pd.Timestamp(event_date, tz=ET)
        thursday = friday - pd.Timedelta(days=1)
        close_bar = _exact_bar(
            frame,
            thursday + pd.Timedelta(hours=15, minutes=59),
        )
        open_bar = _exact_bar(frame, friday + pd.Timedelta(hours=9, minutes=30))
        noon_bar = _exact_bar(frame, friday + pd.Timedelta(hours=12))
        if close_bar is None or open_bar is None or noon_bar is None:
            continue
        prices = {
            "thursday_close": float(close_bar["close"]),
            "friday_open": float(open_bar["open"]),
            "friday_noon": float(noon_bar["open"]),
        }
        if any(not np.isfinite(value) or value <= 0 for value in prices.values()):
            continue
        overnight_bp = math.log(prices["friday_open"] / prices["thursday_close"]) * 1e4
        short_reversal_bp = -math.log(prices["friday_noon"] / prices["friday_open"]) * 1e4
        rows.append(
            {
                "event_date": event_date.isoformat(),
                **prices,
                "overnight_spike_bp": overnight_bp,
                "short_reversal_bp": short_reversal_bp,
            }
        )
    return pd.DataFrame(rows)


def summarize(values: pd.Series | np.ndarray) -> Summary:
    clean = np.asarray(values, dtype=float)
    clean = clean[np.isfinite(clean)]
    n = int(clean.size)
    if n < 2:
        return Summary(n, math.nan, math.nan, math.nan, math.nan, math.nan)
    mean = float(clean.mean())
    sigma = float(clean.std(ddof=1))
    ratio = mean / sigma if sigma > 0 else math.nan
    t_stat = ratio * math.sqrt(n) if np.isfinite(ratio) else math.nan
    power = NormalDist().cdf(math.sqrt(n) * abs(ratio) - POWER_Z)
    return Summary(n, mean, sigma, ratio, t_stat, power)


def round_trip_cost_bp(
    price: float,
    cost_per_side_usd: float,
    *,
    slippage_usd_per_side: float = MYM_TICK_SLIPPAGE_USD_PER_SIDE,
) -> float:
    notional_usd = price * MYM_MULTIPLIER_USD
    return 2.0 * (cost_per_side_usd + slippage_usd_per_side) / notional_usd * 1e4


def evaluate(
    events: pd.DataFrame,
    expected_event_count: int,
) -> dict[str, object]:
    coverage_rate = len(events) / expected_event_count if expected_event_count else 0.0
    overnight = summarize(events["overnight_spike_bp"])
    reversal = summarize(events["short_reversal_bp"])
    power_floor = POWER_Z / math.sqrt(reversal.n) if reversal.n else math.inf
    median_open = float(events["friday_open"].median()) if len(events) else math.nan
    tradeify_rt = round_trip_cost_bp(median_open, TRADEIFY_COST_PER_SIDE_USD)
    mffu_rt = round_trip_cost_bp(median_open, MFFU_COST_PER_SIDE_USD)

    gates = {
        "P0_0_coverage": coverage_rate >= MIN_COVERAGE_RATE,
        "P0_1_overnight_spike": (
            overnight.mean_bp > 0
            and overnight.delta_over_sigma >= power_floor
        ),
        "P0_2_intraday_reversal": (
            reversal.mean_bp > 0
            and reversal.delta_over_sigma >= power_floor
        ),
        "P0_3_cost_law": reversal.mean_bp >= COST_MULTIPLE * tradeify_rt,
    }
    if not gates["P0_0_coverage"]:
        verdict = "AMBIGUOUS"
    elif all(gates.values()):
        verdict = "RESOLVED"
    else:
        verdict = "FALSIFIED"

    return {
        "verdict": verdict,
        "expected_event_count": expected_event_count,
        "observed_event_count": len(events),
        "coverage_rate": coverage_rate,
        "power_floor_delta_over_sigma": power_floor,
        "overnight": asdict(overnight),
        "reversal": asdict(reversal),
        "median_friday_open": median_open,
        "costs": {
            "tradeify_round_trip_bp": tradeify_rt,
            "tradeify_4x_hurdle_bp": COST_MULTIPLE * tradeify_rt,
            "mffu_round_trip_bp": mffu_rt,
            "mffu_4x_hurdle_bp": COST_MULTIPLE * mffu_rt,
        },
        "gates": gates,
    }


def load_dbn(path: Path) -> pd.DataFrame:
    import databento as db

    frame = db.DBNStore.from_file(str(path)).to_df()
    index = frame.index
    if not isinstance(index, pd.DatetimeIndex):
        index = pd.to_datetime(frame["ts_event"])
    if index.tz is None:
        index = index.tz_localize("UTC")
    else:
        index = index.tz_convert("UTC")
    frame = frame.assign(time=index).set_index("time").sort_index()
    frame = frame[~frame.index.duplicated(keep="last")]
    frame.index = frame.index.tz_convert(ET)
    return frame


def render_results(result: dict[str, object]) -> str:
    overnight = result["overnight"]
    reversal = result["reversal"]
    costs = result["costs"]
    gates = result["gates"]
    return f"""# MYM-3FPS-1 Phase-0 RESULTS

**Verdict: `{result['verdict']}`**

## Frozen construct

Short MYM at 09:30 ET on each calendar third Friday; cover at 12:00 ET.
Native-micro panel: 2019-05-06 through 2026-07-21. K=0 delta extraction.

## Measurements

| Quantity | Value |
|---|---:|
| Event coverage | {result['observed_event_count']}/{result['expected_event_count']} ({result['coverage_rate']:.1%}) |
| Overnight spike | {overnight['mean_bp']:+.3f} bp; sigma {overnight['sigma_bp']:.3f}; delta/sigma {overnight['delta_over_sigma']:.4f}; power {overnight['confirm_power']:.3f} |
| Open-to-noon short reversal | {reversal['mean_bp']:+.3f} bp; sigma {reversal['sigma_bp']:.3f}; delta/sigma {reversal['delta_over_sigma']:.4f}; power {reversal['confirm_power']:.3f} |
| Required delta/sigma | {result['power_floor_delta_over_sigma']:.4f} |
| Tradeify RT / 4x hurdle | {costs['tradeify_round_trip_bp']:.3f} / {costs['tradeify_4x_hurdle_bp']:.3f} bp |
| MFFU RT / 4x hurdle | {costs['mffu_round_trip_bp']:.3f} / {costs['mffu_4x_hurdle_bp']:.3f} bp |

## Gates

| Gate | Result |
|---|---|
| P0.0 coverage >= {MIN_COVERAGE_RATE:.0%} | {'PASS' if gates['P0_0_coverage'] else 'FAIL'} |
| P0.1 positive, powered overnight spike | {'PASS' if gates['P0_1_overnight_spike'] else 'FAIL'} |
| P0.2 positive, powered open-to-noon reversal | {'PASS' if gates['P0_2_intraday_reversal'] else 'FAIL'} |
| P0.3 reversal >= {COST_MULTIPLE:.0f}x Tradeify RT cost | {'PASS' if gates['P0_3_cost_law'] else 'FAIL'} |

## Disposition

`RESOLVED` licenses a separately frozen K-bearing confirmation campaign only.
`FALSIFIED` closes this construct without K spend. `AMBIGUOUS` means data
coverage failed and no return verdict is valid.
"""


def run(dbn_path: Path, output_dir: Path) -> dict[str, object]:
    event_dates = third_fridays(START_DATE, END_DATE_EXCLUSIVE)
    events = build_events(load_dbn(dbn_path), event_dates)
    result = evaluate(events, len(event_dates))
    output_dir.mkdir(parents=True, exist_ok=True)
    events.to_csv(output_dir / "primary_events.csv", index=False)
    (output_dir / "phase0_results.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "RESULTS.md").write_text(render_results(result), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbn", type=Path, required=True)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
    )
    args = parser.parse_args()
    result = run(args.dbn, args.output_dir)
    print(json.dumps(result, indent=2))
    return 0 if result["verdict"] == "RESOLVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
