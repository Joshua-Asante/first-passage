"""Deterministic cross-strategy event union and calendar-week exit blocks."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from typing import Mapping

import pandas as pd

from research_utils.trade_reconciliation import micro_equivalent_multiplier


_NAIVE_DOMAIN = "SOURCE_NAIVE_AMERICA_NEW_YORK"


def _validate_strategy_frame(
    strategy_id: str,
    frame: pd.DataFrame,
    *,
    required_columns: set[str],
) -> None:
    missing = sorted(required_columns - set(frame.columns))
    if missing:
        raise ValueError(f"{strategy_id} frame missing columns: {missing}")
    observed = set(frame["strategy_id"].drop_duplicates())
    if observed and observed != {strategy_id}:
        raise ValueError(
            f"strategy_id mismatch for {strategy_id}: observed={sorted(observed)}"
        )


def build_joint_events(
    events_by_strategy: Mapping[str, pd.DataFrame],
    *,
    encoded_instruments_by_strategy: Mapping[str, str] | None = None,
) -> pd.DataFrame:
    """Union canonical events with stable ties and per-event cap-unit quantities."""
    required = {
        "strategy_id",
        "encoded_instrument",
        "source_row_number",
        "timestamp_naive",
        "timestamp_utc",
        "quantity",
    }
    frames: list[pd.DataFrame] = []
    for strategy_id in sorted(events_by_strategy):
        source = events_by_strategy[strategy_id]
        _validate_strategy_frame(strategy_id, source, required_columns=required)
        frame = source.copy()
        instruments = tuple(frame["encoded_instrument"].drop_duplicates())
        if not instruments:
            if encoded_instruments_by_strategy is None:
                raise ValueError(
                    f"{strategy_id} has no events and no configured encoded instrument"
                )
            instruments = (encoded_instruments_by_strategy[strategy_id],)
        if len(instruments) != 1:
            raise ValueError(
                f"{strategy_id} must contain exactly one encoded_instrument"
            )
        multiplier = micro_equivalent_multiplier(str(instruments[0]))
        frame["micro_equivalent_quantity"] = frame["quantity"].map(
            lambda value: int(value) * multiplier
        )
        frames.append(frame)

    if not frames:
        return pd.DataFrame(
            columns=[
                *sorted(required),
                "micro_equivalent_quantity",
                "concurrent_cross_strategy",
                "timestamp_domain",
            ]
        )
    joint = pd.concat(frames, ignore_index=True, sort=False)
    use_utc = bool(joint["timestamp_utc"].notna().all())
    timestamp_column = "timestamp_utc" if use_utc else "timestamp_naive"
    domain = "UTC" if use_utc else _NAIVE_DOMAIN
    joint = joint.sort_values(
        [timestamp_column, "strategy_id", "source_row_number"],
        kind="stable",
        ignore_index=True,
    )
    strategy_counts = joint.groupby(timestamp_column, sort=False)["strategy_id"].transform(
        "nunique"
    )
    joint["concurrent_cross_strategy"] = strategy_counts > 1
    joint["timestamp_domain"] = domain
    return joint


def _week_start(value: pd.Timestamp) -> object:
    timestamp = pd.Timestamp(value)
    return (timestamp - timedelta(days=timestamp.weekday())).date()


def build_weekly_exit_blocks(
    trades_by_strategy: Mapping[str, pd.DataFrame],
) -> pd.DataFrame:
    """Aggregate exits into a complete Monday-start calendar-week range."""
    required = {
        "strategy_id",
        "exit_timestamp_naive",
        "exit_timestamp_utc",
        "net_pnl_usd",
    }
    strategies = sorted(trades_by_strategy)
    frames: list[pd.DataFrame] = []
    for strategy_id in strategies:
        frame = trades_by_strategy[strategy_id]
        _validate_strategy_frame(strategy_id, frame, required_columns=required)
        frames.append(frame)
    all_trades = pd.concat(frames, ignore_index=True, sort=False) if frames else pd.DataFrame()
    use_utc = not all_trades.empty and bool(all_trades["exit_timestamp_utc"].notna().all())
    timestamp_column = "exit_timestamp_utc" if use_utc else "exit_timestamp_naive"
    domain = "UTC" if use_utc else _NAIVE_DOMAIN

    output_columns = ["week_start", "timestamp_domain"]
    for strategy_id in strategies:
        output_columns.extend(
            [f"{strategy_id}_net_pnl_usd", f"{strategy_id}_trade_count"]
        )
    output_columns.extend(["joint_net_pnl_usd", "joint_trade_count"])
    if all_trades.empty:
        return pd.DataFrame(columns=output_columns)

    all_trades = all_trades.copy()
    all_trades["week_start"] = all_trades[timestamp_column].map(_week_start)
    first_week = min(all_trades["week_start"])
    last_week = max(all_trades["week_start"])
    weeks = [timestamp.date() for timestamp in pd.date_range(first_week, last_week, freq="7D")]
    result = pd.DataFrame({"week_start": weeks, "timestamp_domain": domain})

    net_columns: list[str] = []
    count_columns: list[str] = []
    for strategy_id in strategies:
        strategy = all_trades[all_trades["strategy_id"] == strategy_id]
        grouped = strategy.groupby("week_start", sort=False)
        pnl_by_week = grouped["net_pnl_usd"].sum().to_dict()
        count_by_week = grouped.size().to_dict()
        net_column = f"{strategy_id}_net_pnl_usd"
        count_column = f"{strategy_id}_trade_count"
        result[net_column] = result["week_start"].map(
            lambda week: pnl_by_week.get(week, Decimal("0.00"))
        )
        result[count_column] = result["week_start"].map(
            lambda week: int(count_by_week.get(week, 0))
        )
        net_columns.append(net_column)
        count_columns.append(count_column)
    result["joint_net_pnl_usd"] = result[net_columns].apply(
        lambda row: sum(row, Decimal("0.00")),
        axis=1,
    )
    result["joint_trade_count"] = result[count_columns].sum(axis=1).astype(int)
    return result[output_columns]
