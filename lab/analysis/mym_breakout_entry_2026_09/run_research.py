#!/usr/bin/env python3
"""Costed, chronological MYM opening-range breakout entry research."""
from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd


PERIODS = (
    ("development", pd.Timestamp("2019-01-01", tz="UTC"), pd.Timestamp("2023-01-01", tz="UTC")),
    ("validation", pd.Timestamp("2023-01-01", tz="UTC"), pd.Timestamp("2025-01-01", tz="UTC")),
    ("holdout", pd.Timestamp("2025-01-01", tz="UTC"), pd.Timestamp("2026-08-01", tz="UTC")),
)
FAMILIES = ("immediate", "close_confirmed", "buffer_10", "retest_25", "momentum_two_close")


def assign_period(timestamp: pd.Timestamp) -> str:
    """Return the frozen chronological period for a UTC timestamp."""
    ts = pd.Timestamp(timestamp)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    else:
        ts = ts.tz_convert("UTC")
    for name, start, end in PERIODS:
        if start <= ts < end:
            return name
    return "outside"


def evaluate_position(
    *,
    side: str,
    entry_price: float,
    bars: pd.DataFrame,
    stop_points: float,
    target_points: float,
    tick_size: float,
    point_value: float,
    commission_per_side: float,
    slippage_ticks_per_side: float,
) -> dict[str, Any]:
    """Evaluate one position with conservative OHLC sequencing and full costs."""
    if side not in {"long", "short"}:
        raise ValueError(f"invalid side: {side}")
    direction = 1.0 if side == "long" else -1.0
    stop_price = entry_price - direction * stop_points
    target_price = entry_price + direction * target_points
    exit_price = float(bars.iloc[-1]["close"])
    exit_time = bars.iloc[-1]["time"]
    exit_reason = "time"
    for row in bars.itertuples(index=False):
        bar_open = float(row.open)
        if side == "long":
            stop_hit = row.low <= stop_price
            target_hit = row.high >= target_price
            if bar_open <= stop_price:
                exit_price = bar_open
                exit_reason = "stop"
            elif bar_open >= target_price:
                exit_price = target_price
                exit_reason = "target"
            elif stop_hit:
                exit_price = stop_price
                exit_reason = "stop"
            elif target_hit:
                exit_price = target_price
                exit_reason = "target"
        else:
            stop_hit = row.high >= stop_price
            target_hit = row.low <= target_price
            if bar_open >= stop_price:
                exit_price = bar_open
                exit_reason = "stop"
            elif bar_open <= target_price:
                exit_price = target_price
                exit_reason = "target"
            elif stop_hit:
                exit_price = stop_price
                exit_reason = "stop"
            elif target_hit:
                exit_price = target_price
                exit_reason = "target"
        if stop_hit or target_hit:
            exit_time = row.time
            break
    gross_points = direction * (exit_price - entry_price)
    gross_pnl = gross_points * point_value
    execution_cost = 2.0 * commission_per_side + 2.0 * slippage_ticks_per_side * tick_size * point_value
    net_pnl = gross_pnl - execution_cost
    initial_risk = stop_points * point_value
    return {
        "side": side,
        "entry_price_raw": float(entry_price),
        "exit_price_raw": float(exit_price),
        "exit_time": exit_time,
        "exit_reason": exit_reason,
        "gross_pnl_usd": float(gross_pnl),
        "net_pnl_usd": float(net_pnl),
        "gross_r": float(gross_pnl / initial_risk),
        "net_r": float(net_pnl / initial_risk),
        "initial_risk_usd": float(initial_risk),
        "execution_cost_usd": float(execution_cost),
    }


def simulate_session(
    bars: pd.DataFrame,
    *,
    family: str,
    stop_points: float,
    slippage_ticks_per_side: float,
    target_points: float | None = None,
    tick_size: float = 1.0,
    point_value: float = 0.5,
    commission_per_side: float = 0.91,
) -> dict[str, Any] | None:
    """Simulate the first eligible breakout in one RTH session.

    The first two bars form the opening range. Close-based decisions enter at
    the next bar open; intrabar stop families use the trigger price and treat
    two-sided entry bars as unsequenced and therefore unfilled.
    """
    if family not in FAMILIES:
        raise ValueError(f"unknown family: {family}")
    if len(bars) < 4:
        return None
    work = bars.sort_values("time").reset_index(drop=True)
    opening = work.iloc[:2]
    or_high = float(opening["high"].max())
    or_low = float(opening["low"].min())
    target = stop_points if target_points is None else target_points
    signal_index: int | None = None
    entry_index: int | None = None
    entry_price: float | None = None
    side: str | None = None
    if family in {"immediate", "buffer_10"}:
        buffer_points = 10.0 if family == "buffer_10" else 0.0
        long_level = or_high + buffer_points
        short_level = or_low - buffer_points
        for i in range(2, len(work)):
            bar_open = float(work.iloc[i]["open"])
            long_hit = float(work.iloc[i]["high"]) >= long_level
            short_hit = float(work.iloc[i]["low"]) <= short_level
            long_gap = bar_open >= long_level
            short_gap = bar_open <= short_level
            if not long_gap and not short_gap and long_hit and short_hit:
                return None
            if long_hit or short_hit:
                signal_index = entry_index = i
                side = "long" if long_gap or (long_hit and not short_hit) else "short"
                entry_price = max(bar_open, long_level) if side == "long" else min(bar_open, short_level)
                break
    elif family in {"close_confirmed", "momentum_two_close"}:
        required = 1 if family == "close_confirmed" else 2
        long_run = short_run = 0
        for i in range(2, len(work) - 1):
            close = float(work.iloc[i]["close"])
            long_run = long_run + 1 if close > or_high else 0
            short_run = short_run + 1 if close < or_low else 0
            if long_run >= required or short_run >= required:
                signal_index = i
                entry_index = i + 1
                side = "long" if long_run >= required else "short"
                entry_price = float(work.iloc[entry_index]["open"])
                break
    else:  # retest_25
        breakout_side: str | None = None
        for i in range(2, len(work) - 1):
            row = work.iloc[i]
            close = float(row["close"])
            if breakout_side is None:
                if close > or_high:
                    breakout_side = "long"
                elif close < or_low:
                    breakout_side = "short"
                continue
            if breakout_side == "long":
                retest = float(row["low"]) <= or_high + 25.0 and close > or_high
            else:
                retest = float(row["high"]) >= or_low - 25.0 and close < or_low
            if retest:
                signal_index = i
                entry_index = i + 1
                side = breakout_side
                entry_price = float(work.iloc[entry_index]["open"])
                break
    if signal_index is None or entry_index is None or entry_price is None or side is None:
        return None
    trade = evaluate_position(
        side=side,
        entry_price=entry_price,
        bars=work.iloc[entry_index:],
        stop_points=stop_points,
        target_points=target,
        tick_size=tick_size,
        point_value=point_value,
        commission_per_side=commission_per_side,
        slippage_ticks_per_side=slippage_ticks_per_side,
    )
    trade.update(
        {
            "family": family,
            "session_date": work.iloc[0]["time"].date(),
            "signal_time": work.iloc[signal_index]["time"],
            "entry_time": work.iloc[entry_index]["time"],
            "opening_range_high": or_high,
            "opening_range_low": or_low,
        }
    )
    return trade


def _side_summary(trades: pd.DataFrame) -> dict[str, Any]:
    if trades.empty:
        return {
            "trade_count": 0,
            "win_rate": None,
            "gross_expectancy_r": None,
            "net_expectancy_r": None,
            "average_win_r": None,
            "average_loss_r": None,
            "profit_factor": None,
            "max_drawdown_r": None,
        }
    wins = trades.loc[trades["net_pnl_usd"] > 0, "net_pnl_usd"]
    losses = trades.loc[trades["net_pnl_usd"] <= 0, "net_pnl_usd"]
    equity = trades["net_r"].cumsum()
    drawdown = equity.cummax().clip(lower=0) - equity
    loss_sum = float(-losses.sum())
    return {
        "trade_count": int(len(trades)),
        "win_rate": float((trades["net_pnl_usd"] > 0).mean()),
        "gross_expectancy_r": float(trades["gross_r"].mean()),
        "net_expectancy_r": float(trades["net_r"].mean()),
        "average_win_r": float(trades.loc[trades["net_r"] > 0, "net_r"].mean()) if len(wins) else None,
        "average_loss_r": float(trades.loc[trades["net_r"] <= 0, "net_r"].mean()) if len(losses) else None,
        "profit_factor": float(wins.sum() / loss_sum) if loss_sum else None,
        "max_drawdown_r": float(drawdown.max()),
    }


def summarize_trades(trades: pd.DataFrame) -> dict[str, Any]:
    """Return headline metrics and long/short breakdown from trade rows."""
    result = _side_summary(trades)
    result["long"] = _side_summary(trades.loc[trades["side"] == "long"])
    result["short"] = _side_summary(trades.loc[trades["side"] == "short"])
    return result


def validate_inputs(bars: pd.DataFrame, metadata: dict[str, Any]) -> None:
    """Hard-fail on data or instrument identity defects."""
    expected = {
        "schema": "BAR_EXPORT_meta_v0.2",
        "type": "futures",
        "symbol": "MYM",
        "ticker": "MYM1!",
        "mintick": 1.0,
        "pointvalue": 0.5,
        "timeframe": "15",
        "timezone": "America/Chicago",
    }
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise ValueError(f"metadata mismatch: expected {expected}, got {metadata}")
    required = {"time", "open", "high", "low", "close", "volume"}
    if not required.issubset(bars.columns):
        raise ValueError(f"missing columns: {sorted(required - set(bars.columns))}")
    if bars["time"].duplicated().any():
        raise ValueError("duplicate timestamps")
    if not bars["time"].is_monotonic_increasing:
        raise ValueError("timestamps are not chronological")
    invalid = (bars["low"] > bars[["open", "close"]].min(axis=1)) | (bars["high"] < bars[["open", "close"]].max(axis=1)) | (bars["high"] < bars["low"])
    if invalid.any():
        raise ValueError("invalid OHLC geometry")
    if (bars["volume"] < 0).any():
        raise ValueError("negative volume")


def validate_config(config: dict[str, Any]) -> None:
    """Validate the frozen catalogue instead of failing later by incidental KeyError."""
    try:
        study_id = config["study_id"]
        instrument = config["instrument"]
        session = config["session"]
        execution = config["execution"]
        periods = config["periods"]
        catalogue = [row["family"] for row in config["catalogue"]]
        thresholds = config["decision_thresholds"]
        bootstrap = config["bootstrap"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"missing required configuration field: {exc}") from exc
    if study_id != "MYM-BREAKOUT-ENTRY-2026-09":
        raise ValueError("study_id configuration mismatch")
    expected_instrument = {
        "symbol": "MYM", "ticker": "MYM1!", "tick_size": 1.0,
        "tick_value_usd": 0.5, "point_value_usd": 0.5, "contracts": 1,
    }
    if any(instrument.get(key) != value for key, value in expected_instrument.items()):
        raise ValueError("instrument configuration mismatch")
    expected_session = {
        "timezone": "America/Chicago",
        "opening_range_start": "08:30",
        "opening_range_end": "09:00",
        "last_entry": "14:45",
        "force_flat": "15:00",
        "minimum_bars": 27,
    }
    if any(session.get(key) != value for key, value in expected_session.items()):
        raise ValueError(f"session configuration mismatch: expected {expected_session}")
    if catalogue != list(FAMILIES):
        raise ValueError(f"catalogue must equal frozen family order {FAMILIES}")
    expected_periods = {
        "development": ["2019-05-05", "2022-12-31"],
        "validation": ["2023-01-01", "2024-12-31"],
        "holdout": ["2025-01-01", "2026-07-31"],
    }
    if periods != expected_periods:
        raise ValueError("period configuration mismatch")
    if (
        execution.get("stop_points_headline") != 300
        or execution.get("headline_slippage_ticks_per_side") != 1
        or execution.get("stop_points_neighborhood") != [250, 300, 350]
        or execution.get("target_r") != 1.0
    ):
        raise ValueError("execution stop/target configuration mismatch")
    if execution.get("slippage_sensitivity_ticks_per_side") != [0, 1, 2, 4]:
        raise ValueError("execution cost sensitivity mismatch")
    if float(execution.get("commission_per_side_usd", -1)) != 0.91:
        raise ValueError("commission configuration mismatch")
    expected_policies = {
        "ambiguous_intrabar": "stop_first",
        "same_bar_two_sided_entry": "no_fill",
        "gap_through_stop": "worse_of_open_or_stop",
    }
    if any(execution.get(key) != value for key, value in expected_policies.items()):
        raise ValueError("execution policy configuration mismatch")
    expected_thresholds = {
        "minimum_net_expectancy_r": 0.1,
        "minimum_win_rate": 0.45,
        "minimum_validation_trades": 100,
        "minimum_holdout_trades": 75,
    }
    if thresholds != expected_thresholds:
        raise ValueError("decision threshold configuration mismatch")
    if int(bootstrap.get("samples", 0)) <= 0 or "seed" not in bootstrap:
        raise ValueError("bootstrap configuration mismatch")


def bootstrap_expectancy_ci(values: pd.Series, *, samples: int, seed: int) -> tuple[float, float]:
    """Return a deterministic percentile CI for mean trade expectancy."""
    data = values.dropna().to_numpy(dtype=float)
    if not len(data):
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = rng.choice(data, size=(samples, len(data)), replace=True).mean(axis=1)
    low, high = np.quantile(means, [0.025, 0.975])
    return (float(low), float(high))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_sessions(bars: pd.DataFrame, *, minimum_bars: int = 27) -> tuple[list[pd.DataFrame], dict[str, int]]:
    """Return complete Chicago RTH sessions and exclusion counts."""
    local = bars.copy()
    local["time"] = pd.to_datetime(local["time"], utc=True)
    local["local_time"] = local["time"].dt.tz_convert(ZoneInfo("America/Chicago"))
    local["session_date"] = local["local_time"].dt.date
    clock = local["local_time"].dt.strftime("%H:%M")
    rth = local.loc[(clock >= "08:30") & (clock <= "15:00") & (local["local_time"].dt.weekday < 5)].copy()
    sessions: list[pd.DataFrame] = []
    expected_grid = set(pd.date_range("2000-01-01 08:30", "2000-01-01 15:00", freq="15min").strftime("%H:%M"))
    excluded = {"too_few_bars": 0, "missing_opening_range": 0, "incomplete_grid": 0}
    for _, day in rth.groupby("session_date", sort=True):
        times = set(day["local_time"].dt.strftime("%H:%M"))
        if len(day) < minimum_bars:
            excluded["too_few_bars"] += 1
            continue
        if not {"08:30", "08:45"}.issubset(times):
            excluded["missing_opening_range"] += 1
            continue
        if times != expected_grid:
            excluded["incomplete_grid"] += 1
            continue
        eligible = day.loc[day["local_time"].dt.strftime("%H:%M") <= "15:00", ["time", "open", "high", "low", "close", "volume"]]
        sessions.append(eligible.reset_index(drop=True))
    return sessions, excluded


def run_cell(
    sessions: list[pd.DataFrame],
    *,
    family: str,
    stop_points: float,
    slippage_ticks_per_side: float,
    commission_per_side: float,
    target_r: float = 1.0,
) -> pd.DataFrame:
    """Simulate one fully declared catalogue cell over every complete session."""
    rows: list[dict[str, Any]] = []
    for session in sessions:
        trade = simulate_session(
            session,
            family=family,
            stop_points=stop_points,
            slippage_ticks_per_side=slippage_ticks_per_side,
            target_points=stop_points * target_r,
            commission_per_side=commission_per_side,
        )
        if trade is not None:
            trade["period"] = assign_period(pd.Timestamp(trade["entry_time"]))
            trade["year"] = pd.Timestamp(trade["entry_time"]).year
            trade["stop_points"] = stop_points
            trade["slippage_ticks_per_side"] = slippage_ticks_per_side
            rows.append(trade)
    return pd.DataFrame(rows)


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return None if not np.isfinite(value) else float(value)
    if isinstance(value, (pd.Timestamp,)):
        return value.isoformat()
    return value


def _summarize_with_ci(trades: pd.DataFrame, *, samples: int, seed: int) -> dict[str, Any]:
    summary = summarize_trades(trades)
    if trades.empty:
        summary["net_expectancy_r_ci95"] = [None, None]
    else:
        summary["net_expectancy_r_ci95"] = list(bootstrap_expectancy_ci(trades["net_r"], samples=samples, seed=seed))
    return _json_safe(summary)


def create_data_audit(bars: pd.DataFrame, metadata: dict[str, Any], sessions: list[pd.DataFrame], excluded: dict[str, int]) -> dict[str, Any]:
    delta = bars["time"].diff()
    gap_counts = delta.value_counts().head(12)
    return _json_safe(
        {
            "row_count": len(bars),
            "start_utc": bars["time"].iloc[0],
            "end_utc": bars["time"].iloc[-1],
            "chronological": bool(bars["time"].is_monotonic_increasing),
            "duplicate_timestamps": int(bars["time"].duplicated().sum()),
            "metadata": metadata,
            "nominal_interval_minutes": 15,
            "exact_15_minute_intervals": int((delta == pd.Timedelta(minutes=15)).sum()),
            "irregular_intervals": int((delta != pd.Timedelta(minutes=15)).sum() - 1),
            "gaps_over_one_day": int((delta > pd.Timedelta(days=1)).sum()),
            "largest_gap": str(delta.max()),
            "interval_distribution_top": {str(k): int(v) for k, v in gap_counts.items()},
            "utc_dates": int(bars["time"].dt.date.nunique()),
            "complete_rth_sessions": len(sessions),
            "excluded_rth_sessions": excluded,
            "limitations": [
                "Continuous MYM1! is an unadjusted front-contract series and can contain roll gaps.",
                "OHLC bars do not reveal intrabar path; target/stop ties are resolved stop-first.",
                f"The supplied export ends {bars['time'].iloc[-1].date().isoformat()}.",
                "RTH study excludes overnight information and incomplete/holiday sessions.",
                "Commission is repository-authoritative for Tradeify Select; spread/slippage is a declared conservative model, not tick-level measurement.",
            ],
        }
    )


def run_catalogue(
    bars: pd.DataFrame, config: dict[str, Any], *, retain_complete_ledger: bool = False
) -> tuple[dict[str, Any], pd.DataFrame, dict[str, Any]]:
    """Run every frozen family/cost/stop cell and return summaries and headline trades."""
    sessions, excluded = build_sessions(bars, minimum_bars=int(config["session"]["minimum_bars"]))
    execution = config["execution"]
    commission = float(execution["commission_per_side_usd"])
    bootstrap = config["bootstrap"]
    cells: list[dict[str, Any]] = []
    headline_frames: list[pd.DataFrame] = []
    complete_frames: list[pd.DataFrame] = []
    for family_row in config["catalogue"]:
        family = family_row["family"]
        for stop_points in execution["stop_points_neighborhood"]:
            for slippage in execution["slippage_sensitivity_ticks_per_side"]:
                trades = run_cell(
                    sessions,
                    family=family,
                    stop_points=float(stop_points),
                    slippage_ticks_per_side=float(slippage),
                    commission_per_side=commission,
                    target_r=float(execution["target_r"]),
                )
                if retain_complete_ledger and not trades.empty:
                    complete_frames.append(trades.copy())
                period_metrics = {
                    period: _summarize_with_ci(
                        trades.loc[trades["period"] == period],
                        samples=int(bootstrap["samples"]),
                        seed=int(bootstrap["seed"]),
                    )
                    for period in ("development", "validation", "holdout")
                }
                yearly = {
                    str(year): _summarize_with_ci(group, samples=int(bootstrap["samples"]), seed=int(bootstrap["seed"]))
                    for year, group in trades.groupby("year", sort=True)
                }
                cells.append(
                    {
                        "family": family,
                        "stop_points": stop_points,
                        "initial_risk_usd": stop_points * float(config["instrument"]["point_value_usd"]),
                        "slippage_ticks_per_side": slippage,
                        "commission_per_side_usd": commission,
                        "all": _summarize_with_ci(trades, samples=int(bootstrap["samples"]), seed=int(bootstrap["seed"])),
                        "periods": period_metrics,
                        "years": yearly,
                        "period_evidence_status": {
                            "development": "exploratory",
                            "validation": "selection",
                            "holdout": "consumed_exploratory_not_confirmatory",
                        },
                    }
                )
                if stop_points == execution["stop_points_headline"] and slippage == execution["headline_slippage_ticks_per_side"]:
                    headline_frames.append(trades)
    headline = pd.concat(headline_frames, ignore_index=True) if headline_frames else pd.DataFrame()
    complete = pd.concat(complete_frames, ignore_index=True) if complete_frames else pd.DataFrame()
    audit_stub = {"complete_rth_sessions": len(sessions), "excluded_rth_sessions": excluded}
    return {"cells": cells}, complete if retain_complete_ledger else headline, audit_stub


def choose_candidate(results: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    """Choose by validation only, using frozen simplicity order and thresholds."""
    execution = config["execution"]
    thresholds = config["decision_thresholds"]
    headline = [
        cell for cell in results["cells"]
        if cell["stop_points"] == execution["stop_points_headline"]
        and cell["slippage_ticks_per_side"] == execution["headline_slippage_ticks_per_side"]
    ]
    passing = []
    for cell in headline:
        metrics = cell["periods"]["validation"]
        if (
            metrics["trade_count"] >= thresholds["minimum_validation_trades"]
            and metrics["net_expectancy_r"] is not None
            and metrics["net_expectancy_r"] >= thresholds["minimum_net_expectancy_r"]
            and metrics["win_rate"] >= thresholds["minimum_win_rate"]
        ):
            passing.append(cell)
    selected = passing[0] if passing else None
    return {
        "selection_basis": "validation only; catalogue order is frozen simplicity order",
        "selected_family": selected["family"] if selected else None,
        "validation_pass_count": len(passing),
        "holdout_was_not_used_for_selection": True,
        "holdout_access_status": "consumed_exploratory_protocol_deviation",
        "holdout_confirmed_conclusion": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bars", required=True)
    parser.add_argument("--meta", required=True)
    parser.add_argument("--config", default=str(Path(__file__).with_name("config.json")))
    parser.add_argument("--out-dir", default=str(Path(__file__).parent))
    parser.add_argument("--trades-out", default=None, help="Optional local-only detailed trade CSV")
    args = parser.parse_args(argv)
    bars_path, meta_path, config_path = map(Path, (args.bars, args.meta, args.config))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    bars = pd.read_csv(bars_path, parse_dates=["time"])
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    validate_inputs(bars, metadata)
    validate_config(config)
    results, retained_trades, audit_stub = run_catalogue(
        bars, config, retain_complete_ledger=bool(args.trades_out)
    )
    sessions, excluded = build_sessions(bars, minimum_bars=int(config["session"]["minimum_bars"]))
    audit = create_data_audit(bars, metadata, sessions, excluded)
    results.update(
        {
            "study_id": config["study_id"],
            "input_sha256": sha256_file(bars_path),
            "metadata_sha256": sha256_file(meta_path),
            "config_sha256": sha256_file(config_path),
            "declared_cell_count": len(results["cells"]),
            "selection": choose_candidate(results, config),
            "audit_session_counts": audit_stub,
        }
    )
    if args.trades_out:
        trades_path = Path(args.trades_out)
        trades_path.parent.mkdir(parents=True, exist_ok=True)
        retained_trades.to_csv(trades_path, index=False)
        results["complete_trade_ledger"] = {
            "committed": False,
            "local_path": "workspace_outputs/mym_breakout_entry/all_declared_trades.csv",
            "row_count": len(retained_trades),
            "sha256": sha256_file(trades_path),
        }
    else:
        results["complete_trade_ledger"] = {
            "committed": False,
            "local_path": None,
            "row_count": None,
            "sha256": None,
            "warning": "rerun with --trades-out to produce the local-only complete ledger",
        }
    (out_dir / "data_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "results.json").write_text(json.dumps(_json_safe(results), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {len(results['cells'])} declared cells and {len(retained_trades)} retained trade rows to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
