"""Strict simple-trade reconstruction and accounting for Tradeify Phase 1."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from types import MappingProxyType
from typing import Mapping

import pandas as pd

from discovery.cost_model import INSTRUMENT_SPECS
from research_utils.tv_trade_ledger import Issue, SourceSpec


_CENT_TOLERANCE = Decimal("0.01")
_CENT_SUMMARY_FIELDS = (
    "net_pnl_usd",
    "commission_usd",
    "favorable_excursion_usd",
    "adverse_excursion_usd",
    "cumulative_pnl_usd",
    "size_value_usd",
)
_EXACT_SUMMARY_FIELDS = (
    "return_pct",
    "favorable_excursion_pct",
    "adverse_excursion_pct",
    "cumulative_pnl_pct",
)

TRADE_COLUMNS = [
    "strategy_id",
    "source_trade_id",
    "direction",
    "entry_timestamp_naive",
    "exit_timestamp_naive",
    "entry_timestamp_utc",
    "exit_timestamp_utc",
    "entry_price",
    "exit_price",
    "quantity",
    "net_pnl_usd",
    "commission_usd",
    "gross_pnl_usd",
    "source_cumulative_pnl_usd",
    "mae_usd",
    "mfe_usd",
    "excursion_bound",
    "entry_source_row",
    "exit_source_row",
]


@dataclass(frozen=True)
class InstrumentGeometry:
    multiplier: Decimal
    tick_size: Decimal
    tick_value: Decimal


@dataclass(frozen=True)
class ReconstructionResult:
    trades: pd.DataFrame
    issues: tuple[Issue, ...]


@dataclass(frozen=True)
class AccountingMetrics:
    trade_count: int
    first_entry_timestamp: pd.Timestamp | None
    last_exit_timestamp: pd.Timestamp | None
    net_pnl_usd: Decimal
    commission_usd: Decimal
    gross_pnl_usd: Decimal | None
    wins: int
    losses: int
    flats: int
    win_rate: Decimal | None
    profit_factor: Decimal | None
    max_drawdown_usd: Decimal
    monthly_net_pnl: Mapping[str, Decimal]
    final_source_cumulative_pnl_usd: Decimal | None
    issues: tuple[Issue, ...]


_CAMPAIGN_GEOMETRY: Mapping[str, InstrumentGeometry] = {
    "6J": InstrumentGeometry(
        multiplier=Decimal("12500000"),
        tick_size=Decimal("0.0000005"),
        tick_value=Decimal("6.25"),
    )
}


def instrument_geometry(symbol: str) -> InstrumentGeometry:
    """Return Decimal geometry, adding campaign-local 6J to existing specs."""
    if symbol in _CAMPAIGN_GEOMETRY:
        return _CAMPAIGN_GEOMETRY[symbol]
    if symbol not in {"MNQ", "MYM", "MGC"}:
        raise ValueError("unsupported Tradeify Phase 1 instrument: " + repr(symbol))
    spec = INSTRUMENT_SPECS[symbol]
    return InstrumentGeometry(
        multiplier=Decimal(str(spec.multiplier)),
        tick_size=Decimal(str(spec.tick_size)),
        tick_value=Decimal(str(spec.tick_value)),
    )


def _issue(
    code: str,
    spec: SourceSpec,
    trade_id: int,
    source_rows: tuple[int, ...],
    detail: Mapping[str, object],
) -> Issue:
    return Issue(
        code=code,
        severity="BLOCKER",
        strategy_id=spec.strategy_id,
        detail=detail,
        trade_id=trade_id,
        source_rows=source_rows,
    )


def _summary_mismatches(entry: pd.Series, exit_: pd.Series) -> tuple[str, ...]:
    mismatches = [
        field
        for field in _CENT_SUMMARY_FIELDS
        if abs(Decimal(entry[field]) - Decimal(exit_[field])) > _CENT_TOLERANCE
    ]
    mismatches.extend(
        field
        for field in _EXACT_SUMMARY_FIELDS
        if Decimal(entry[field]) != Decimal(exit_[field])
    )
    entry_duration = Decimal(entry["duration_bars"])
    exit_duration = Decimal(exit_["duration_bars"])
    if (
        entry_duration != exit_duration
        or entry_duration != entry_duration.to_integral_value()
        or exit_duration != exit_duration.to_integral_value()
    ):
        mismatches.append("duration_bars")
    return tuple(mismatches)


def reconstruct_trades(events: pd.DataFrame, spec: SourceSpec) -> ReconstructionResult:
    """Reconstruct only exact one-entry/one-exit source trade IDs."""
    trades: list[dict[str, object]] = []
    issues: list[Issue] = []
    if events.empty:
        return ReconstructionResult(pd.DataFrame(columns=TRADE_COLUMNS), ())

    geometry = instrument_geometry(spec.encoded_instrument)
    for raw_trade_id, group in events.groupby("source_trade_id", sort=True):
        trade_id = int(raw_trade_id)
        group = group.sort_values("source_row_number", kind="stable")
        source_rows = tuple(int(value) for value in group["source_row_number"])
        entries = group[group["event_type"] == "ENTRY"]
        exits = group[group["event_type"] == "EXIT"]

        if entries.empty:
            issues.append(
                _issue(
                    "ORPHAN_EXIT",
                    spec,
                    trade_id,
                    source_rows,
                    {"entry_count": 0, "exit_count": len(exits)},
                )
            )
            continue
        if exits.empty:
            issues.append(
                _issue(
                    "ORPHAN_ENTRY",
                    spec,
                    trade_id,
                    source_rows,
                    {"entry_count": len(entries), "exit_count": 0},
                )
            )
            continue
        if len(entries) != 1 or len(exits) != 1 or len(group) != 2:
            issues.append(
                _issue(
                    "UNSUPPORTED_TRADE_LEG_CARDINALITY",
                    spec,
                    trade_id,
                    source_rows,
                    {"entry_count": len(entries), "exit_count": len(exits)},
                )
            )
            continue

        entry = entries.iloc[0]
        exit_ = exits.iloc[0]
        structural_issues: list[Issue] = []
        if entry["direction"] != exit_["direction"]:
            structural_issues.append(
                _issue(
                    "DIRECTION_MISMATCH",
                    spec,
                    trade_id,
                    source_rows,
                    {"entry_direction": entry["direction"], "exit_direction": exit_["direction"]},
                )
            )
        entry_quantity_decimal = Decimal(str(entry["quantity"]))
        exit_quantity_decimal = Decimal(str(exit_["quantity"]))
        quantities_are_integral = (
            entry_quantity_decimal == entry_quantity_decimal.to_integral_value()
            and exit_quantity_decimal == exit_quantity_decimal.to_integral_value()
        )
        if (
            entry_quantity_decimal <= 0
            or exit_quantity_decimal <= 0
            or not quantities_are_integral
        ):
            structural_issues.append(
                _issue(
                    "INVALID_QUANTITY",
                    spec,
                    trade_id,
                    source_rows,
                    {
                        "entry_quantity": entry_quantity_decimal,
                        "exit_quantity": exit_quantity_decimal,
                    },
                )
            )
        elif entry_quantity_decimal != exit_quantity_decimal:
            structural_issues.append(
                _issue(
                    "QUANTITY_MISMATCH",
                    spec,
                    trade_id,
                    source_rows,
                    {
                        "entry_quantity": entry_quantity_decimal,
                        "exit_quantity": exit_quantity_decimal,
                    },
                )
            )
        if entry["timestamp_naive"] > exit_["timestamp_naive"]:
            structural_issues.append(
                _issue(
                    "EXIT_BEFORE_ENTRY",
                    spec,
                    trade_id,
                    source_rows,
                    {
                        "entry_timestamp": entry["timestamp_naive"],
                        "exit_timestamp": exit_["timestamp_naive"],
                    },
                )
            )
        mismatches = _summary_mismatches(entry, exit_)
        if mismatches:
            structural_issues.append(
                _issue(
                    "DUPLICATED_TRADE_SUMMARY_MISMATCH",
                    spec,
                    trade_id,
                    source_rows,
                    {"fields": mismatches},
                )
            )
        if structural_issues:
            issues.extend(structural_issues)
            continue

        entry_quantity = int(entry_quantity_decimal)
        direction = str(entry["direction"])
        entry_price = Decimal(entry["price_usd"])
        exit_price = Decimal(exit_["price_usd"])
        net_pnl = Decimal(exit_["net_pnl_usd"])
        commission = Decimal(exit_["commission_usd"])
        source_gross = net_pnl + commission
        direction_sign = Decimal("1") if direction == "LONG" else Decimal("-1")
        price_implied_gross = (
            (exit_price - entry_price)
            * geometry.multiplier
            * Decimal(entry_quantity)
            * direction_sign
        )
        gross_pnl: Decimal | None = source_gross
        if abs(price_implied_gross - source_gross) > _CENT_TOLERANCE:
            gross_pnl = None
            issues.append(
                _issue(
                    "GROSS_IDENTITY_MISMATCH",
                    spec,
                    trade_id,
                    source_rows,
                    {
                        "price_implied_gross_pnl_usd": price_implied_gross,
                        "net_plus_commission_usd": source_gross,
                    },
                )
            )

        trades.append(
            {
                "strategy_id": spec.strategy_id,
                "source_trade_id": trade_id,
                "direction": direction,
                "entry_timestamp_naive": entry["timestamp_naive"],
                "exit_timestamp_naive": exit_["timestamp_naive"],
                "entry_timestamp_utc": entry["timestamp_utc"],
                "exit_timestamp_utc": exit_["timestamp_utc"],
                "entry_price": entry_price,
                "exit_price": exit_price,
                "quantity": entry_quantity,
                "net_pnl_usd": net_pnl,
                "commission_usd": commission,
                "gross_pnl_usd": gross_pnl,
                "source_cumulative_pnl_usd": Decimal(exit_["cumulative_pnl_usd"]),
                "mae_usd": Decimal(exit_["adverse_excursion_usd"]),
                "mfe_usd": Decimal(exit_["favorable_excursion_usd"]),
                "excursion_bound": "excursion-bounded",
                "entry_source_row": int(entry["source_row_number"]),
                "exit_source_row": int(exit_["source_row_number"]),
            }
        )

    return ReconstructionResult(pd.DataFrame(trades, columns=TRADE_COLUMNS), tuple(issues))


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"))


def calculate_accounting(trades: pd.DataFrame) -> AccountingMetrics:
    """Calculate deterministic exit-led accounting without repairing source summaries."""
    ordered = trades.sort_values(
        ["exit_timestamp_naive", "exit_source_row"], kind="stable"
    ).reset_index(drop=True)
    trade_count = len(ordered)
    strategy_id = str(ordered.iloc[0]["strategy_id"]) if trade_count else ""
    issues: list[Issue] = []

    net_values = [Decimal(value) for value in ordered["net_pnl_usd"]]
    commission_values = [Decimal(value) for value in ordered["commission_usd"]]
    net_total_exact = sum(net_values, Decimal("0"))
    commission_total_exact = sum(commission_values, Decimal("0"))

    wins = sum(value > 0 for value in net_values)
    losses = sum(value < 0 for value in net_values)
    flats = sum(value == 0 for value in net_values)
    win_rate = (
        (Decimal(wins) / Decimal(trade_count)).quantize(Decimal("0.0000000001"))
        if trade_count
        else None
    )
    gross_profits = sum((value for value in net_values if value > 0), Decimal("0"))
    gross_losses = -sum((value for value in net_values if value < 0), Decimal("0"))
    if gross_losses == 0:
        profit_factor = None
        issues.append(
            Issue(
                code="NO_GROSS_LOSSES",
                severity="INFO",
                strategy_id=strategy_id,
                detail={"gross_losses_usd": Decimal("0.00")},
            )
        )
    else:
        profit_factor = (gross_profits / gross_losses).quantize(Decimal("0.0000000001"))

    equity = Decimal("0")
    peak = Decimal("0")
    max_drawdown = Decimal("0")
    for value in net_values:
        equity += value
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, peak - equity)

    monthly: dict[str, Decimal] = {}
    for _, trade in ordered.iterrows():
        month = pd.Timestamp(trade["exit_timestamp_naive"]).strftime("%Y-%m")
        monthly[month] = monthly.get(month, Decimal("0")) + Decimal(trade["net_pnl_usd"])
    monthly = {month: _money(value) for month, value in monthly.items()}

    gross_values = ordered["gross_pnl_usd"].tolist()
    gross_is_complete = all(value is not None and not pd.isna(value) for value in gross_values)
    gross_total = (
        _money(sum((Decimal(value) for value in gross_values), Decimal("0")))
        if gross_is_complete
        else None
    )

    final_source_cumulative: Decimal | None = None
    if trade_count:
        final_trade = ordered.iloc[-1]
        final_source_cumulative = _money(Decimal(final_trade["source_cumulative_pnl_usd"]))
        if abs(Decimal(final_trade["source_cumulative_pnl_usd"]) - net_total_exact) > _CENT_TOLERANCE:
            issues.append(
                Issue(
                    code="FINAL_CUMULATIVE_PNL_MISMATCH",
                    severity="BLOCKER",
                    strategy_id=strategy_id,
                    detail={
                        "source_cumulative_pnl_usd": Decimal(
                            final_trade["source_cumulative_pnl_usd"]
                        ),
                        "summed_exit_net_pnl_usd": net_total_exact,
                    },
                    source_rows=(int(final_trade["exit_source_row"]),),
                )
            )

    return AccountingMetrics(
        trade_count=trade_count,
        first_entry_timestamp=(
            pd.Timestamp(ordered["entry_timestamp_naive"].min()) if trade_count else None
        ),
        last_exit_timestamp=(
            pd.Timestamp(ordered.iloc[-1]["exit_timestamp_naive"]) if trade_count else None
        ),
        net_pnl_usd=_money(net_total_exact),
        commission_usd=_money(commission_total_exact),
        gross_pnl_usd=gross_total,
        wins=wins,
        losses=losses,
        flats=flats,
        win_rate=win_rate,
        profit_factor=profit_factor,
        max_drawdown_usd=_money(max_drawdown),
        monthly_net_pnl=MappingProxyType(monthly),
        final_source_cumulative_pnl_usd=final_source_cumulative,
        issues=tuple(issues),
    )
