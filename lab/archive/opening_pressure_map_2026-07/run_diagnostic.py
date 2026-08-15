"""Opening volume × directional-efficiency mechanism diagnostic.

K=0 diagnostic only.  It tests whether above-normal opening volume predicts
continuation when the first 30 minutes are directionally efficient and reversal
when that volume is absorbed into a low-efficiency range.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ET = "America/New_York"
RV_LOOKBACK = 14
HAC_MAX_LAGS = 5
DEVELOPMENT_END = pd.Timestamp("2023-12-31").date()
MIN_DEVELOPMENT_SESSIONS = 800
MIN_HOLDOUT_SESSIONS = 500
COST_MULTIPLE = 4.0
TRADEIFY_COST_PER_SIDE_USD = 0.91
SLIPPAGE_PER_SIDE_USD = 0.50

INSTRUMENTS = {
    "MNQ": {
        "multiplier": 2.0,
        "expected_sha256": "ddb14f569fb034b5b422255a762f4b43ab4f9aacfe8e1ba092c5cce8e1f7e3ac",
    },
    "MYM": {
        "multiplier": 0.5,
        "expected_sha256": "298ab8c8900f1144b450537f14e356681aec7448b4787ebc770de88c83f9059c",
    },
}


class InputUnavailable(ValueError):
    """Raised when the exact hash-pinned BAR EXPORT input is unavailable."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_panel(path: Path, instrument: str) -> pd.DataFrame:
    if not path.is_file():
        raise InputUnavailable(f"{instrument} BAR EXPORT input missing: {path}")
    expected = INSTRUMENTS[instrument]["expected_sha256"]
    actual = sha256(path)
    if actual != expected:
        raise InputUnavailable(
            f"{instrument} SHA256 mismatch: expected {expected}, got {actual}"
        )
    frame = pd.read_csv(path, parse_dates=["time"]).set_index("time")
    if frame.index.tz is None:
        frame.index = frame.index.tz_localize("UTC")
    frame.index = frame.index.tz_convert(ET)
    frame["rth_date"] = frame.index.date
    frame["minute"] = frame.index.hour * 60 + frame.index.minute
    return frame


def daily_features(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for rth_date, day in frame.groupby("rth_date", sort=True):
        rth = day[day["minute"].between(570, 945)].sort_index()
        opening = rth[rth["minute"].isin([570, 585])]
        exit_bar = rth[rth["minute"] == 945]
        if len(opening) != 2 or len(exit_bar) != 1:
            continue
        opening_open = float(opening.iloc[0]["open"])
        opening_close = float(opening.iloc[-1]["close"])
        opening_high = float(opening["high"].max())
        opening_low = float(opening["low"].min())
        opening_range = opening_high - opening_low
        opening_volume = float(opening["volume"].sum())
        exit_close = float(exit_bar.iloc[0]["close"])
        if (
            opening_open <= 0
            or opening_close <= 0
            or exit_close <= 0
            or opening_range <= 0
            or opening_volume <= 0
        ):
            continue
        opening_move = opening_close - opening_open
        direction = float(np.sign(opening_move))
        if direction == 0:
            continue
        efficiency = abs(opening_move) / opening_range
        signed_followthrough_bp = direction * math.log(exit_close / opening_close) * 1e4
        rows.append(
            {
                "rth_date": rth_date,
                "opening_open": opening_open,
                "opening_volume": opening_volume,
                "efficiency": efficiency,
                "signed_followthrough_bp": signed_followthrough_bp,
            }
        )
    daily = pd.DataFrame(rows).set_index("rth_date").sort_index()
    volume_baseline = (
        daily["opening_volume"]
        .rolling(RV_LOOKBACK, min_periods=RV_LOOKBACK)
        .median()
        .shift(1)
    )
    daily["relative_volume"] = daily["opening_volume"] / volume_baseline
    above_normal_log_volume = np.log(daily["relative_volume"]).clip(lower=0.0)
    daily["pressure_alignment"] = above_normal_log_volume * (2.0 * daily["efficiency"] - 1.0)
    return daily.replace([np.inf, -np.inf], np.nan).dropna()


def hac_slope(frame: pd.DataFrame) -> dict[str, float]:
    x = frame["pressure_alignment"].to_numpy(float)
    y = frame["signed_followthrough_bp"].to_numpy(float)
    design = np.column_stack([np.ones(len(x)), x])
    inverse = np.linalg.inv(design.T @ design)
    coefficients = inverse @ design.T @ y
    residuals = y - design @ coefficients

    meat = np.zeros((2, 2), dtype=float)
    for row, residual in zip(design, residuals):
        meat += residual**2 * np.outer(row, row)
    for lag in range(1, min(HAC_MAX_LAGS, len(x) - 1) + 1):
        weight = 1.0 - lag / (HAC_MAX_LAGS + 1.0)
        cross = np.zeros((2, 2), dtype=float)
        for index in range(lag, len(x)):
            cross += (
                residuals[index]
                * residuals[index - lag]
                * np.outer(design[index], design[index - lag])
            )
        meat += weight * (cross + cross.T)
    covariance = inverse @ meat @ inverse
    standard_error = math.sqrt(max(float(covariance[1, 1]), 0.0))
    slope = float(coefficients[1])
    return {
        "n": int(len(frame)),
        "slope_bp": slope,
        "hac_standard_error": standard_error,
        "hac_t": slope / standard_error if standard_error > 0 else math.nan,
    }


def round_trip_cost_bp(price: float, multiplier: float) -> float:
    return (
        2.0
        * (TRADEIFY_COST_PER_SIDE_USD + SLIPPAGE_PER_SIDE_USD)
        / (price * multiplier)
        * 1e4
    )


def evaluate_instrument(frame: pd.DataFrame, instrument: str) -> dict[str, object]:
    development = frame.loc[frame.index <= DEVELOPMENT_END]
    holdout = frame.loc[frame.index > DEVELOPMENT_END]
    pooled = hac_slope(frame)
    dev = hac_slope(development)
    oos = hac_slope(holdout)
    score_spread = float(
        frame["pressure_alignment"].quantile(0.90)
        - frame["pressure_alignment"].quantile(0.10)
    )
    predicted_spread_bp = pooled["slope_bp"] * score_spread
    median_price = float(frame["opening_open"].median())
    rt_cost_bp = round_trip_cost_bp(
        median_price,
        INSTRUMENTS[instrument]["multiplier"],
    )
    gates = {
        "coverage": (
            dev["n"] >= MIN_DEVELOPMENT_SESSIONS
            and oos["n"] >= MIN_HOLDOUT_SESSIONS
        ),
        "development": dev["slope_bp"] > 0 and dev["hac_t"] >= 2.0,
        "holdout_sign": oos["slope_bp"] > 0,
        "pooled": pooled["slope_bp"] > 0 and pooled["hac_t"] >= 2.0,
        "economic": predicted_spread_bp >= COST_MULTIPLE * rt_cost_bp,
    }
    return {
        "instrument": instrument,
        "development": dev,
        "holdout": oos,
        "pooled": pooled,
        "score_p90_minus_p10": score_spread,
        "predicted_p90_minus_p10_bp": predicted_spread_bp,
        "median_opening_price": median_price,
        "round_trip_cost_bp": rt_cost_bp,
        "four_x_cost_hurdle_bp": COST_MULTIPLE * rt_cost_bp,
        "gates": gates,
        "passes": all(gates.values()),
    }


def overall_verdict(results: dict[str, dict[str, object]]) -> str:
    passes = [bool(result["passes"]) for result in results.values()]
    if all(passes):
        return "RESOLVED"
    if any(passes):
        return "AMBIGUOUS"
    return "FALSIFIED"


def render_report(verdict: str, results: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Opening pressure-alignment diagnostic RESULTS",
        "",
        f"**Verdict: `{verdict}`**",
        "",
        "K=0 mechanism diagnostic; no strategy or deployment claim.",
        "",
        "| Instrument | Dev slope/t | Holdout slope/t | Pooled slope/t | Predicted P90-P10 | 4x cost | Verdict |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for instrument, result in results.items():
        dev = result["development"]
        oos = result["holdout"]
        pooled = result["pooled"]
        lines.append(
            f"| {instrument} | {dev['slope_bp']:+.3f}/{dev['hac_t']:+.2f} "
            f"| {oos['slope_bp']:+.3f}/{oos['hac_t']:+.2f} "
            f"| {pooled['slope_bp']:+.3f}/{pooled['hac_t']:+.2f} "
            f"| {result['predicted_p90_minus_p10_bp']:+.3f} bp "
            f"| {result['four_x_cost_hurdle_bp']:.3f} bp "
            f"| {'PASS' if result['passes'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "`RESOLVED` requires both instruments to pass every frozen gate. "
            "`AMBIGUOUS` means exactly one passes. `FALSIFIED` means neither passes.",
            "",
        ]
    )
    return "\n".join(lines)


def run(mnq_path: Path, mym_path: Path, output_dir: Path) -> dict[str, object]:
    paths = {"MNQ": mnq_path, "MYM": mym_path}
    results = {
        instrument: evaluate_instrument(
            daily_features(load_panel(path, instrument)),
            instrument,
        )
        for instrument, path in paths.items()
    }
    verdict = overall_verdict(results)
    payload = {"verdict": verdict, "results": results}
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "diagnostic_results.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "RESULTS.md").write_text(
        render_report(verdict, results),
        encoding="utf-8",
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mnq", type=Path, required=True)
    parser.add_argument("--mym", type=Path, required=True)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
    )
    args = parser.parse_args()
    try:
        payload = run(args.mnq, args.mym, args.output_dir)
    except InputUnavailable as exc:
        print(json.dumps({"status": "NEEDS_CONTEXT", "reason": str(exc)}, indent=2))
        return 2
    print(json.dumps(payload, indent=2))
    return 0 if payload["verdict"] == "RESOLVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
