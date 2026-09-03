"""Strict simple-trade reconstruction and accounting for Tradeify Phase 1."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import re
from types import MappingProxyType
from typing import Mapping
from urllib.parse import urlsplit

import pandas as pd

from discovery.cost_model import INSTRUMENT_SPECS
from research_utils.tv_trade_ledger import ContinuousContractRollPolicy, FeeSchedule, Issue, SourceSpec


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
    "duration_bars",
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


@dataclass(frozen=True)
class VenueMetrics:
    trade_count: int
    intended_instrument: str
    encoded_instrument: str
    venue_commission_per_side_usd: Decimal
    pine_commission_per_side_usd: Decimal
    export_implied_commission_per_side_usd: Decimal | None
    export_implied_commission_per_side_values_usd: tuple[Decimal, ...]
    micro_equivalent_multiplier: int
    peak_open_micro_equivalent_quantity_min: int
    peak_open_micro_equivalent_quantity_max: int
    micro_equivalent_contract_cap: int
    cross_date_holds: int
    overnight_holds: int
    friday_to_sunday_holds: int
    holiday_short_deadline_status: str
    contract_month_attribution_status: str
    roll_seam_attribution_status: str
    bid_ask_spread_status: str
    pine_slippage_ticks_per_side: Decimal
    slippage_basis: str
    issues: tuple[Issue, ...]


@dataclass(frozen=True)
class EarlyCloseCalendar:
    """Primary-source CME early-close dates over the campaign evidence span."""

    source_url: str
    page_date: date | None
    observed_date: date
    coverage_start: date
    coverage_end: date
    coverage_status: str
    coverage_note: str
    early_close_dates: frozenset[date]
    sources: tuple[Mapping[str, object], ...] = ()
    input_sha256: str = ""


def _calendar_date(value: object, field: str, *, nullable: bool = False) -> date | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO date") from exc
    if parsed.isoformat() != value:
        raise ValueError(f"{field} must be an ISO date")
    return parsed


def _cme_url(value: object) -> None:
    if not isinstance(value, str):
        raise ValueError("source_url must be a primary CME HTTPS URL")
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or parsed.hostname not in {"cmegroup.com", "www.cmegroup.com"}
            or parsed.username or parsed.password or parsed.port not in {None, 443}):
        raise ValueError("source_url must be a primary CME HTTPS URL")


def _capture_rows(rows: object, year: int) -> set[date]:
    if not isinstance(rows, list):
        raise ValueError("capture rows must be an array")
    dates: set[date] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"date", "deadline_local"}:
            raise ValueError("capture row keys mismatch")
        day = _calendar_date(row["date"], "capture date")
        if day.year != year or day in dates:
            raise ValueError("capture row year mismatch or duplicate date")
        if row["deadline_local"] != "12:59 America/New_York":
            raise ValueError("capture deadline must be 12:59 America/New_York")
        dates.add(day)
    return dates


def _load_calendar_sources(sources: object, capture_dir: Path) -> tuple[dict[int, dict], dict[int, set[date]]]:
    if not isinstance(sources, list):
        raise ValueError("sources must be an array")
    records, dates = {}, {}
    root = capture_dir.resolve()
    for source in sources:
        if not isinstance(source, dict) or set(source) != {"year", "source_url", "page_date", "capture_basename", "sha256"}:
            raise ValueError("calendar source keys mismatch")
        year = source["year"]
        if type(year) is not int or not 1 <= year <= 9999 or year in records:
            raise ValueError("calendar source year must be unique integer")
        _cme_url(source["source_url"])
        _calendar_date(source["page_date"], "source page_date")
        if not isinstance(source["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
            raise ValueError("calendar source sha256 must be lowercase SHA256")
        name = source["capture_basename"]
        if (not isinstance(name, str) or not name or name in {".", ".."}
                or any(c in name for c in '/\\:') or Path(name).name != name):
            raise ValueError("capture_basename must be a safe basename")
        target = (root / name).resolve()
        if not target.is_relative_to(root):
            raise ValueError("calendar capture escapes capture directory")
        try:
            raw = target.read_bytes()
            if sha256(raw).hexdigest() != source["sha256"]:
                raise ValueError("calendar capture SHA256 mismatch")
            capture = json.loads(raw.decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("cannot load yearly CME JSON capture") from exc
        if not isinstance(capture, dict) or set(capture) != {"year", "source_url", "page_date", "rows"}:
            raise ValueError("yearly CME JSON capture keys mismatch")
        if type(capture["year"]) is not int or any(capture[k] != source[k] for k in ("year", "source_url", "page_date")):
            raise ValueError("yearly capture year/source metadata mismatch")
        records[year] = dict(source)
        dates[year] = _capture_rows(capture["rows"], year)
    return records, dates


def load_early_close_calendar(path: str | Path, *, capture_dir: str | Path | None = None) -> EarlyCloseCalendar:
    """Load the frozen CME early-close capture, including explicit coverage gaps."""
    try:
        raw = Path(path).read_bytes()
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load CME early-close calendar: {path}") from exc
    expected_keys = {
        "source_url",
        "page_date",
        "observed_date",
        "coverage_start",
        "coverage_end",
        "coverage_status",
        "coverage_note",
        "rows",
        "sources",
    }
    if not isinstance(payload, dict) or set(payload) != expected_keys:
        raise ValueError("CME early-close calendar keys mismatch")
    for field in ("source_url", "coverage_status", "coverage_note"):
        if not isinstance(payload[field], str) or not payload[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    status = payload["coverage_status"]
    if status not in {"COMPLETE", "NEEDS_CONTEXT"}:
        raise ValueError("coverage_status must be COMPLETE or NEEDS_CONTEXT")
    page_date = _calendar_date(payload["page_date"], "page_date", nullable=True)
    observed_date = _calendar_date(payload["observed_date"], "observed_date")
    coverage_start = _calendar_date(payload["coverage_start"], "coverage_start")
    coverage_end = _calendar_date(payload["coverage_end"], "coverage_end")
    assert observed_date is not None
    assert coverage_start is not None
    assert coverage_end is not None
    if coverage_start > coverage_end:
        raise ValueError("coverage_start must not be after coverage_end")
    _cme_url(payload["source_url"])
    sources, captured_dates = _load_calendar_sources(
        payload["sources"], Path(capture_dir) if capture_dir is not None
        else Path(path).parent / "local_artifacts" / "calendar_captures",
    )
    rows = payload["rows"]
    if not isinstance(rows, list):
        raise ValueError("rows must be an array")
    if (
        status == "COMPLETE"
        and coverage_start.year != coverage_end.year
        and not rows
    ):
        raise ValueError("COMPLETE multi-year calendar requires non-empty rows")
    early_dates: set[date] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"date", "deadline_local", "source_year"}:
            raise ValueError(f"rows[{index}] keys mismatch")
        row_date = _calendar_date(row["date"], f"rows[{index}].date")
        assert row_date is not None
        if type(row["source_year"]) is not int or row["source_year"] not in sources or row["source_year"] != row_date.year:
            raise ValueError("row source_year must resolve to its declared year")
        if not coverage_start <= row_date <= coverage_end:
            raise ValueError(f"rows[{index}].date is outside the coverage span")
        if row["deadline_local"] != "12:59 America/New_York":
            raise ValueError(f"rows[{index}].deadline_local must be 12:59 America/New_York")
        if row_date in early_dates:
            raise ValueError(f"duplicate CME early-close date: {row_date.isoformat()}")
        early_dates.add(row_date)
    for year, captured in captured_dates.items():
        expected = {day for day in captured if coverage_start <= day <= coverage_end}
        if {day for day in early_dates if day.year == year} != expected:
            raise ValueError("calendar rows differ from yearly capture within coverage")
    if status == "COMPLETE":
        if set(range(coverage_start.year, coverage_end.year + 1)) - sources.keys():
            raise ValueError("COMPLETE calendar requires a source for every covered year")
        for year in range(coverage_start.year, coverage_end.year + 1):
            if coverage_start <= date(year, 1, 1) and coverage_end >= date(year, 12, 31):
                if not any(day.year == year for day in early_dates):
                    raise ValueError("COMPLETE calendar requires rows for every fully covered year")
    return EarlyCloseCalendar(
        source_url=payload["source_url"],
        page_date=page_date,
        observed_date=observed_date,
        coverage_start=coverage_start,
        coverage_end=coverage_end,
        coverage_status=status,
        coverage_note=payload["coverage_note"],
        early_close_dates=frozenset(early_dates),
        sources=tuple(MappingProxyType(source) for source in sources.values()),
        input_sha256=sha256(raw).hexdigest(),
    )


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


def micro_equivalent_multiplier(symbol: str) -> int:
    """Return the Tradeify account-cap weight for one campaign contract."""
    if symbol == "6J":
        return 10
    if symbol in {"MNQ", "MYM", "MGC"}:
        return 1
    raise ValueError("unsupported Tradeify Phase 1 instrument: " + repr(symbol))


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
        if Decimal(entry[field]) != Decimal(exit_[field])
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
    for raw_trade_id, group in events.groupby("source_trade_id", sort=False):
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
                "duration_bars": Decimal(entry["duration_bars"]),
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


def _venue_issue(
    code: str,
    spec: SourceSpec,
    detail: Mapping[str, object],
    *,
    severity: str = "BLOCKER",
    trade_id: int | None = None,
    source_rows: tuple[int, ...] = (),
) -> Issue:
    return Issue(
        code=code,
        severity=severity,
        strategy_id=spec.strategy_id,
        detail=detail,
        trade_id=trade_id,
        source_rows=source_rows,
    )


def _commission_issues(
    trades: pd.DataFrame,
    spec: SourceSpec,
    venue_fee: Decimal,
) -> tuple[Decimal | None, tuple[Decimal, ...], list[Issue]]:
    values = tuple(
        sorted(
            {
                Decimal(trade["commission_usd"])
                / (Decimal("2") * Decimal(int(trade["quantity"])))
                for _, trade in trades.iterrows()
            }
        )
    )
    export_fee = values[0] if len(values) == 1 else None
    issues: list[Issue] = []
    source_rows = tuple(int(value) for value in trades.get("exit_source_row", ()))
    if len(values) > 1:
        issues.append(
            _venue_issue(
                "VARIABLE_EXPORT_COMMISSION",
                spec,
                {"per_side_values_usd": values},
                source_rows=source_rows,
            )
        )

    if values and any(value != venue_fee for value in values):
        issues.append(
            _venue_issue(
                "EXPORT_VENUE_COMMISSION_MISMATCH",
                spec,
                {
                    "export_per_side_values_usd": values,
                    "venue_per_side_usd": venue_fee,
                },
                source_rows=source_rows,
            )
        )
    export_matches_venue = bool(values) and all(value == venue_fee for value in values)
    pine_mismatch_severity = "WARNING" if export_matches_venue else "BLOCKER"
    if values and any(
        value != spec.pine_commission_per_side_usd
        for value in values
    ):
        issues.append(
            _venue_issue(
                "PINE_EXPORT_COMMISSION_MISMATCH",
                spec,
                {
                    "pine_per_side_usd": spec.pine_commission_per_side_usd,
                    "export_per_side_values_usd": values,
                },
                severity=pine_mismatch_severity,
                source_rows=source_rows,
            )
        )
    if spec.pine_commission_per_side_usd != venue_fee:
        issues.append(
            _venue_issue(
                "PINE_VENUE_COMMISSION_MISMATCH",
                spec,
                {
                    "pine_per_side_usd": spec.pine_commission_per_side_usd,
                    "venue_per_side_usd": venue_fee,
                },
                severity=pine_mismatch_severity,
            )
        )
    return export_fee, values, issues


def _exposure_bounds(trades: pd.DataFrame, *, quantity_multiplier: int) -> tuple[int, int]:
    events: dict[pd.Timestamp, dict[str, int]] = {}
    for _, trade in trades.iterrows():
        quantity = int(trade["quantity"]) * quantity_multiplier
        entry_time = pd.Timestamp(trade["entry_timestamp_naive"])
        exit_time = pd.Timestamp(trade["exit_timestamp_naive"])
        events.setdefault(entry_time, {"entries": 0, "prior_exits": 0, "zero_exits": 0})[
            "entries"
        ] += quantity
        exit_kind = "zero_exits" if entry_time == exit_time else "prior_exits"
        events.setdefault(exit_time, {"entries": 0, "prior_exits": 0, "zero_exits": 0})[
            exit_kind
        ] += quantity

    def peak(*, upper_bound: bool) -> int:
        current = 0
        maximum = 0
        for timestamp in sorted(events):
            event = events[timestamp]
            if upper_bound:
                deltas = (
                    event["entries"],
                    -event["prior_exits"] - event["zero_exits"],
                )
            else:
                current -= event["prior_exits"]
                maximum = max(maximum, current)
                for _, trade in trades.iterrows():
                    entry_time = pd.Timestamp(trade["entry_timestamp_naive"])
                    exit_time = pd.Timestamp(trade["exit_timestamp_naive"])
                    if entry_time == timestamp and exit_time == timestamp:
                        quantity = int(trade["quantity"]) * quantity_multiplier
                        current += quantity
                        maximum = max(maximum, current)
                        current -= quantity
                current += event["entries"] - event["zero_exits"]
                maximum = max(maximum, current)
                continue
            for delta in deltas:
                current += delta
                maximum = max(maximum, current)
        return maximum

    return peak(upper_bound=False), peak(upper_bound=True)


def _spans_friday_to_sunday(entry: pd.Timestamp, exit_: pd.Timestamp) -> bool:
    day = entry.normalize()
    end = exit_.normalize()
    while day <= end:
        if day.weekday() == 4 and day + pd.Timedelta(days=2) <= end:
            return True
        day += pd.Timedelta(days=1)
    return False


def _local_timestamp(trade: pd.Series, leg: str, source_timezone: str | None) -> pd.Timestamp:
    utc_value = trade[f"{leg}_timestamp_utc"]
    if not pd.isna(utc_value):
        value = pd.Timestamp(utc_value)
        if value.tzinfo is None:
            value = value.tz_localize("UTC")
        return value.tz_convert("America/New_York")
    if source_timezone is None:
        raise ValueError("source_timezone is required for Tradeify venue deadlines")
    naive = pd.Timestamp(trade[f"{leg}_timestamp_naive"])
    if naive.tzinfo is not None:
        localized = naive.tz_convert(source_timezone)
    else:
        localized = naive.tz_localize(
            source_timezone,
            ambiguous="raise",
            nonexistent="raise",
        )
    return localized.tz_convert("America/New_York")


def _deadline_timestamps(
    entry: pd.Timestamp,
    exit_: pd.Timestamp,
    early_close_dates: frozenset[date],
) -> tuple[pd.Timestamp, ...]:
    deadlines: list[pd.Timestamp] = []
    day = entry.date()
    while day <= exit_.date():
        clock = "12:59" if day in early_close_dates else "16:45"
        deadline = pd.Timestamp(f"{day.isoformat()} {clock}").tz_localize(
            "America/New_York",
            ambiguous="raise",
            nonexistent="raise",
        )
        if entry < deadline <= exit_:
            deadlines.append(deadline)
        day += pd.Timedelta(days=1)
    return tuple(deadlines)


def analyze_venue(
    trades: pd.DataFrame,
    spec: SourceSpec,
    fee_schedule: FeeSchedule,
    *,
    early_close_calendar: EarlyCloseCalendar | None = None,
    continuous_contract_roll_policy: ContinuousContractRollPolicy | None = None,
) -> VenueMetrics:
    """Audit instrument and venue constraints without changing source trades."""
    geometry = instrument_geometry(spec.encoded_instrument)
    venue_fee = fee_schedule.per_side_usd[spec.encoded_instrument]
    export_fee, export_values, issues = _commission_issues(trades, spec, venue_fee)

    if spec.intended_instrument != spec.encoded_instrument:
        issues.append(
            _venue_issue(
                "INSTRUMENT_MISMATCH",
                spec,
                {
                    "intended_instrument": spec.intended_instrument,
                    "encoded_instrument": spec.encoded_instrument,
                },
            )
        )

    tick_tolerance = Decimal("1e-9")
    for _, trade in trades.iterrows():
        trade_id = int(trade["source_trade_id"])
        for leg, price_field, row_field in (
            ("ENTRY", "entry_price", "entry_source_row"),
            ("EXIT", "exit_price", "exit_source_row"),
        ):
            price = Decimal(trade[price_field])
            tick_count = price / geometry.tick_size
            distance = abs(tick_count - tick_count.to_integral_value())
            if distance > tick_tolerance:
                issues.append(
                    _venue_issue(
                        "OFF_TICK_PRICE",
                        spec,
                        {
                            "leg": leg,
                            "price": price,
                            "tick_size": geometry.tick_size,
                            "distance_to_nearest_tick": distance,
                        },
                        trade_id=trade_id,
                        source_rows=(int(trade[row_field]),),
                    )
                )

    quantity_multiplier = micro_equivalent_multiplier(spec.encoded_instrument)
    peak_min, peak_max = _exposure_bounds(
        trades,
        quantity_multiplier=quantity_multiplier,
    )
    if peak_min > spec.contract_cap:
        issues.append(
            _venue_issue(
                "CONTRACT_CAP_BREACH",
                spec,
                {
                    "micro_equivalent_contract_cap": spec.contract_cap,
                    "peak_open_micro_equivalent_quantity_min": peak_min,
                    "peak_open_micro_equivalent_quantity_max": peak_max,
                },
            )
        )
    elif peak_max > spec.contract_cap:
        issues.append(
            _venue_issue(
                "CAP_STATUS_AMBIGUOUS_AT_TIMESTAMP_TIE",
                spec,
                {
                    "micro_equivalent_contract_cap": spec.contract_cap,
                    "peak_open_micro_equivalent_quantity_min": peak_min,
                    "peak_open_micro_equivalent_quantity_max": peak_max,
                },
            )
        )

    if early_close_calendar is None:
        holiday_status = "NEEDS_CONTEXT"
        early_close_dates: frozenset[date] = frozenset()
        holiday_note = "CME early-close calendar was not supplied"
    else:
        holiday_status = early_close_calendar.coverage_status
        early_close_dates = early_close_calendar.early_close_dates
        holiday_note = early_close_calendar.coverage_note
    if holiday_status != "COMPLETE":
        issues.append(
            _venue_issue(
                "EARLY_CLOSE_CALENDAR_INCOMPLETE",
                spec,
                {
                    "status": holiday_status,
                    "coverage_note": holiday_note,
                },
                severity="WARNING",
            )
        )

    cross_date_holds = 0
    deadline_spanning_holds = 0
    friday_to_sunday_holds = 0
    for _, trade in trades.iterrows():
        entry = _local_timestamp(trade, "entry", spec.source_timezone)
        exit_ = _local_timestamp(trade, "exit", spec.source_timezone)
        trade_id = int(trade["source_trade_id"])
        source_rows = (int(trade["entry_source_row"]), int(trade["exit_source_row"]))
        if entry.date() != exit_.date():
            cross_date_holds += 1
            issues.append(
                _venue_issue(
                    "CROSS_DATE_HOLD",
                    spec,
                    {"entry_date": entry.date(), "exit_date": exit_.date()},
                    severity="WARNING",
                    trade_id=trade_id,
                    source_rows=source_rows,
                )
            )
        if _spans_friday_to_sunday(entry, exit_):
            friday_to_sunday_holds += 1
        deadline_timestamps = _deadline_timestamps(entry, exit_, early_close_dates)
        if deadline_timestamps:
            deadline_spanning_holds += 1
            issues.append(
                _venue_issue(
                    "FORCE_FLAT_VIOLATION",
                    spec,
                    {
                        "entry_timestamp": entry,
                        "exit_timestamp": exit_,
                        "deadline_timestamps": deadline_timestamps,
                    },
                    trade_id=trade_id,
                    source_rows=source_rows,
                )
            )

    if spec.continuous_symbol:
        contract_month_status = "UNAVAILABLE"
        roll_seam_status = "UNAVAILABLE"
        roll_policy = continuous_contract_roll_policy
        accepted = roll_policy is not None and roll_policy.disposition == "ACCEPTED_UNMODELED"
        issues.append(
            _venue_issue(
                "CONTINUOUS_CONTRACT_ROLL_UNRESOLVED",
                spec,
                {
                    "contract_month_attribution": contract_month_status,
                    "roll_seam_attribution": roll_seam_status,
                    "disposition": roll_policy.disposition if roll_policy else "UNRESOLVED",
                    "ruling_date": roll_policy.ruling_date if roll_policy else None,
                    "ruling_ref": roll_policy.ruling_ref if roll_policy else None,
                    "obligations": roll_policy.obligations if roll_policy else (),
                },
                severity="WARNING" if accepted else "BLOCKER",
            )
        )
    else:
        contract_month_status = "SOURCE_ENCODED_INSTRUMENT"
        roll_seam_status = "NOT_APPLICABLE"

    return VenueMetrics(
        trade_count=len(trades),
        intended_instrument=spec.intended_instrument,
        encoded_instrument=spec.encoded_instrument,
        venue_commission_per_side_usd=venue_fee,
        pine_commission_per_side_usd=spec.pine_commission_per_side_usd,
        export_implied_commission_per_side_usd=export_fee,
        export_implied_commission_per_side_values_usd=export_values,
        micro_equivalent_multiplier=quantity_multiplier,
        peak_open_micro_equivalent_quantity_min=peak_min,
        peak_open_micro_equivalent_quantity_max=peak_max,
        micro_equivalent_contract_cap=spec.contract_cap,
        cross_date_holds=cross_date_holds,
        overnight_holds=deadline_spanning_holds,
        friday_to_sunday_holds=friday_to_sunday_holds,
        holiday_short_deadline_status=holiday_status,
        contract_month_attribution_status=contract_month_status,
        roll_seam_attribution_status=roll_seam_status,
        bid_ask_spread_status="NOT_SEPARATELY_OBSERVABLE",
        pine_slippage_ticks_per_side=spec.pine_slippage_ticks_per_side,
        slippage_basis="PINE_DECLARED_TICKS_AND_FILL_PRICES",
        issues=tuple(issues),
    )
