"""Strict reconstruction and accounting tests for Tradeify Phase 1."""

from decimal import Decimal
import json
from pathlib import Path

import pandas as pd
import pytest

from research_utils.trade_reconciliation import (
    EarlyCloseCalendar,
    TRADE_COLUMNS,
    analyze_venue,
    calculate_accounting,
    instrument_geometry,
    load_early_close_calendar,
    micro_equivalent_multiplier,
    reconstruct_trades,
)
from research_utils.tv_trade_ledger import SourceSpec, load_fee_schedule


def _spec(
    *,
    instrument: str = "MNQ",
    intended_instrument: str | None = None,
    contract_cap: int = 80,
    continuous_symbol: bool = True,
    pine_commission: str = "0.91",
) -> SourceSpec:
    return SourceSpec(
        strategy_id="fixture",
        intended_instrument=intended_instrument or instrument,
        encoded_instrument=instrument,
        export_filename="source.csv",
        export_sha256="0" * 64,
        pine_filename="source.pine",
        pine_sha256="1" * 64,
        source_timezone="America/New_York",
        session_timezone="America/New_York",
        declared_bar_size_minutes=15,
        declared_session="09:30-16:00 America/New_York",
        direction_evidence="long-only",
        quantity_convention="integer contracts",
        continuous_symbol=continuous_symbol,
        synchronized_intraday_path_available=False,
        lineage_notes=("fixture",),
        pine_commission_per_side_usd=Decimal(pine_commission),
        pine_slippage_ticks_per_side=Decimal("1"),
        pine_pyramiding_pct=Decimal("100"),
        pine_pin_status="NOT_IN_PORT_MANIFEST",
        pin_divergence=None,
        contract_cap=contract_cap,
    )


@pytest.fixture
def fee_schedule():
    return load_fee_schedule(
        Path(__file__).parents[1]
        / "lab"
        / "analysis"
        / "c1"
        / "tradeify_seven_strategy_phase1_2026-09"
        / "tradeify_commission_schedule.json"
    )


@pytest.fixture
def campaign_early_close_calendar():
    return load_early_close_calendar(
        Path(__file__).parents[1]
        / "lab"
        / "analysis"
        / "c1"
        / "tradeify_seven_strategy_phase1_2026-09"
        / "cme_early_close_calendar.json"
    )


def _event(
    trade_id: int,
    event_type: str,
    *,
    row: int,
    direction: str = "LONG",
    timestamp: str | None = None,
    price: str | None = None,
    qty: int = 2,
    net: str = "2.18",
    commission: str = "1.82",
    favorable: str = "5.00",
    adverse: str = "-1.00",
    cumulative: str = "2.18",
) -> dict[str, object]:
    default_timestamp = "2026-01-05 10:00" if event_type == "ENTRY" else "2026-01-05 10:15"
    default_price = "100.00" if event_type == "ENTRY" else "101.00"
    timestamp_naive = pd.Timestamp(timestamp or default_timestamp)
    return {
        "strategy_id": "fixture",
        "source_trade_id": trade_id,
        "source_row_number": row,
        "timestamp_raw": timestamp_naive.strftime("%Y-%m-%d %H:%M"),
        "timestamp_naive": timestamp_naive,
        "timestamp_utc": pd.NaT,
        "exchange_session_date": None,
        "type_raw": f"{event_type.title()} {direction.title()}",
        "event_type": event_type,
        "direction": direction,
        "signal": "fixture",
        "price_usd": Decimal(price or default_price),
        "quantity": qty,
        "size_value_usd": Decimal("200.00"),
        "net_pnl_usd": Decimal(net),
        "return_pct": Decimal("1.00"),
        "commission_usd": Decimal(commission),
        "favorable_excursion_usd": Decimal(favorable),
        "favorable_excursion_pct": Decimal("2.00"),
        "adverse_excursion_usd": Decimal(adverse),
        "adverse_excursion_pct": Decimal("0.50"),
        "cumulative_pnl_usd": Decimal(cumulative),
        "cumulative_pnl_pct": Decimal("1.00"),
        "duration_bars": Decimal("1"),
        "concurrent_timestamp": False,
    }


def _events(*rows: dict[str, object]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def _round_trip(**event_overrides: object) -> pd.DataFrame:
    trade_id = int(event_overrides.pop("trade_id", 1))
    entry = event_overrides.pop("entry", "100.00")
    exit_ = event_overrides.pop("exit", "101.00")
    return _events(
        _event(trade_id, "ENTRY", row=1, price=str(entry), **event_overrides),
        _event(trade_id, "EXIT", row=2, price=str(exit_), **event_overrides),
    )


def test_reconstruct_requires_exactly_one_entry_and_exit():
    """Choosing the first duplicate leg would conceal unsupported pyramiding."""
    events = _events(
        _event(7, "ENTRY", row=1),
        _event(7, "ENTRY", row=2),
        _event(7, "EXIT", row=3),
    )

    result = reconstruct_trades(events, _spec())

    assert list(result.trades.columns) == TRADE_COLUMNS
    assert result.trades.empty
    assert [(i.code, i.trade_id, i.source_rows) for i in result.issues] == [
        ("UNSUPPORTED_TRADE_LEG_CARDINALITY", 7, (1, 2, 3))
    ]


def test_reconstruct_does_not_silently_skip_orphan_exit():
    """Dropping a zero-entry trade ID would lose a source accounting event."""
    result = reconstruct_trades(_events(_event(9, "EXIT", row=4)), _spec())

    assert result.trades.empty
    assert result.issues[0].code == "ORPHAN_EXIT"
    assert result.issues[0].severity == "BLOCKER"
    assert result.issues[0].source_rows == (4,)


def test_reconstruct_reports_orphan_entry():
    """Dropping a zero-exit trade ID would hide an unclosed source position."""
    result = reconstruct_trades(_events(_event(10, "ENTRY", row=8)), _spec())

    assert result.trades.empty
    assert result.issues[0].code == "ORPHAN_ENTRY"
    assert result.issues[0].source_rows == (8,)


def test_reconstruct_validates_price_pnl_identity():
    """Using float geometry would weaken exact source-dollar reconciliation."""
    events = _round_trip(entry="100.00", exit="101.00", qty=2, net="2.18", commission="1.82")

    result = reconstruct_trades(events, _spec(instrument="MNQ"))

    trade = result.trades.iloc[0]
    assert trade["gross_pnl_usd"] == Decimal("4.00")
    assert not result.issues


def test_reconstruct_retains_trade_when_gross_identity_is_unknown():
    """A price/P&L mismatch must not erase an otherwise structural source trade."""
    result = reconstruct_trades(
        _round_trip(entry="100.00", exit="102.00", qty=2, net="2.18", commission="1.82"),
        _spec(),
    )

    assert len(result.trades) == 1
    assert result.trades.iloc[0]["gross_pnl_usd"] is None
    assert [(issue.code, issue.severity) for issue in result.issues] == [
        ("GROSS_IDENTITY_MISMATCH", "BLOCKER")
    ]


def test_6j_campaign_geometry_supports_price_identity_without_changing_cost_model():
    """Omitting campaign-local 6J geometry would make Aegis unreconstructable."""
    geometry = instrument_geometry("6J")

    assert geometry.multiplier == Decimal("12500000")
    assert geometry.tick_size == Decimal("0.0000005")
    assert geometry.tick_value == Decimal("6.25")


def test_instrument_geometry_converts_existing_specs_to_decimal():
    """Returning float-backed MNQ/MYM/MGC geometry would contaminate Decimal arithmetic."""
    assert instrument_geometry("MNQ").multiplier == Decimal("2.0")
    assert instrument_geometry("MYM").tick_size == Decimal("1.0")
    assert instrument_geometry("MGC").tick_value == Decimal("1.0")


def test_reconstruct_rejects_direction_disagreement():
    """Pairing opposed leg directions would fabricate a coherent round trip."""
    events = _events(
        _event(1, "ENTRY", row=1, direction="LONG"),
        _event(1, "EXIT", row=2, direction="SHORT"),
    )

    result = reconstruct_trades(events, _spec())

    assert result.trades.empty
    assert result.issues[0].code == "DIRECTION_MISMATCH"
    assert result.issues[0].source_rows == (1, 2)


def test_reconstruct_rejects_exit_before_entry():
    """Sorting legs within a trade would silently repair reversed source timestamps."""
    events = _events(
        _event(1, "ENTRY", row=1, timestamp="2026-01-05 10:15"),
        _event(1, "EXIT", row=2, timestamp="2026-01-05 10:00"),
    )

    result = reconstruct_trades(events, _spec())

    assert result.trades.empty
    assert result.issues[0].code == "EXIT_BEFORE_ENTRY"


def test_reconstruct_rejects_unequal_quantities():
    """Treating unequal legs as a simple trade would conceal a partial exit."""
    events = _events(
        _event(1, "ENTRY", row=1, qty=2),
        _event(1, "EXIT", row=2, qty=1),
    )

    result = reconstruct_trades(events, _spec())

    assert result.trades.empty
    assert result.issues[0].code == "QUANTITY_MISMATCH"


def test_reconstruct_rejects_nonpositive_quantity_even_when_legs_match():
    """Trusting structural equality alone would admit an impossible flat position."""
    result = reconstruct_trades(
        _events(_event(1, "ENTRY", row=1, qty=0), _event(1, "EXIT", row=2, qty=0)),
        _spec(),
    )

    assert result.trades.empty
    assert result.issues[0].code == "INVALID_QUANTITY"


def test_reconstruct_rejects_fractional_quantity_even_when_legs_match():
    """Integer coercion would silently truncate an unsupported fractional contract."""
    result = reconstruct_trades(
        _events(
            _event(1, "ENTRY", row=1, qty=Decimal("1.5")),
            _event(1, "EXIT", row=2, qty=Decimal("1.5")),
        ),
        _spec(),
    )

    assert result.trades.empty
    assert result.issues[0].code == "INVALID_QUANTITY"


def test_reconstruct_rejects_duplicated_trade_summary_mismatch():
    """Selecting one disagreeing summary copy would silently repair the source export."""
    entry = _event(1, "ENTRY", row=1)
    exit_ = _event(1, "EXIT", row=2)
    exit_["favorable_excursion_usd"] = Decimal("5.02")

    result = reconstruct_trades(_events(entry, exit_), _spec())

    assert result.trades.empty
    assert [(issue.code, issue.severity, issue.source_rows) for issue in result.issues] == [
        ("DUPLICATED_TRADE_SUMMARY_MISMATCH", "BLOCKER", (1, 2))
    ]


def test_reconstruct_rejects_one_cent_duplicated_trade_summary_mismatch():
    """The aggregate cent tolerance must not weaken exact duplicated source fields."""
    entry = _event(1, "ENTRY", row=1)
    exit_ = _event(1, "EXIT", row=2)
    exit_["commission_usd"] = Decimal("1.83")

    result = reconstruct_trades(_events(entry, exit_), _spec())

    assert result.trades.empty
    assert result.issues[0].code == "DUPLICATED_TRADE_SUMMARY_MISMATCH"
    assert result.issues[0].detail["fields"] == ("commission_usd",)


def test_reconstruct_keeps_scalar_excursions_explicitly_bounded():
    """Scalar TradingView excursions must not be promoted into a timestamped path."""
    result = reconstruct_trades(
        _round_trip(favorable="7.25", adverse="-3.50"),
        _spec(),
    )

    trade = result.trades.iloc[0]
    assert trade["mae_usd"] == Decimal("-3.50")
    assert trade["mfe_usd"] == Decimal("7.25")
    assert trade["excursion_bound"] == "excursion-bounded"


def test_reconstruct_retains_valid_decimal_duration_bars_in_canonical_trade():
    """Dropping a validated duplicated duration loses source timing inventory."""
    events = _round_trip()
    events.loc[:, "duration_bars"] = Decimal("12")

    result = reconstruct_trades(events, _spec())

    assert "duration_bars" in TRADE_COLUMNS
    assert result.trades.iloc[0]["duration_bars"] == Decimal("12")


def test_reconstruct_preserves_first_source_appearance_for_rows_and_issues():
    """Sorting non-monotonic trade IDs would reorder canonical rows and diagnostics."""
    events = _events(
        _event(30, "ENTRY", row=1, timestamp="2026-01-05 10:00"),
        _event(30, "EXIT", row=2, timestamp="2026-01-05 10:01"),
        _event(20, "EXIT", row=3, timestamp="2026-01-05 10:02"),
        _event(10, "ENTRY", row=4, timestamp="2026-01-05 10:03"),
        _event(10, "EXIT", row=5, timestamp="2026-01-05 10:04"),
        _event(5, "ENTRY", row=6, timestamp="2026-01-05 10:05"),
    )

    result = reconstruct_trades(events, _spec())

    assert result.trades["source_trade_id"].tolist() == [30, 10]
    assert [(issue.trade_id, issue.code) for issue in result.issues] == [
        (20, "ORPHAN_EXIT"),
        (5, "ORPHAN_ENTRY"),
    ]


def _trade(
    trade_id: int,
    exit_timestamp: str = "2026-01-05 10:00",
    net: str = "0.18",
    commission: str = "1.82",
    *,
    qty: int = 1,
    exit_row: int | None = None,
    cumulative: str | None = None,
    gross: str | None = "derived",
) -> dict[str, object]:
    exit_time = pd.Timestamp(exit_timestamp)
    net_pnl = Decimal(net)
    commission_usd = Decimal(commission)
    if gross == "derived":
        gross_pnl: Decimal | None = net_pnl + commission_usd
    elif gross is None:
        gross_pnl = None
    else:
        gross_pnl = Decimal(gross)
    return {
        "strategy_id": "fixture",
        "source_trade_id": trade_id,
        "direction": "LONG",
        "entry_timestamp_naive": exit_time - pd.Timedelta(minutes=15),
        "exit_timestamp_naive": exit_time,
        "entry_timestamp_utc": pd.NaT,
        "exit_timestamp_utc": pd.NaT,
        "entry_price": Decimal("100.00"),
        "exit_price": Decimal("101.00"),
        "quantity": qty,
        "net_pnl_usd": net_pnl,
        "commission_usd": commission_usd,
        "gross_pnl_usd": gross_pnl,
        "source_cumulative_pnl_usd": Decimal(cumulative if cumulative is not None else net),
        "mae_usd": Decimal("-1.00"),
        "mfe_usd": Decimal("2.00"),
        "excursion_bound": "excursion-bounded",
        "entry_source_row": (exit_row if exit_row is not None else trade_id) * 2 - 1,
        "exit_source_row": exit_row if exit_row is not None else trade_id * 2,
    }


def _trades(*rows: dict[str, object]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=TRADE_COLUMNS)


def _trade_between(
    trade_id: int,
    entry_timestamp: str,
    exit_timestamp: str,
    commission: str = "1.82",
    *,
    qty: int = 1,
) -> dict[str, object]:
    trade = _trade(trade_id, exit_timestamp, commission=commission, qty=qty)
    trade["entry_timestamp_naive"] = pd.Timestamp(entry_timestamp)
    return trade


def _overlapping_trades_same_boundary(*, qty: int) -> pd.DataFrame:
    return _trades(
        _trade_between(1, "2026-01-05 09:00", "2026-01-05 10:00", qty=qty),
        _trade_between(2, "2026-01-05 10:00", "2026-01-05 11:00", qty=qty),
    )


def _issue_codes(metrics: object) -> set[str]:
    return {issue.code for issue in metrics.issues}


def _early_close_calendar(
    *dates: str,
    coverage_status: str = "COMPLETE",
) -> EarlyCloseCalendar:
    return EarlyCloseCalendar(
        source_url="https://www.cmegroup.com/trading-hours.html",
        page_date=None,
        observed_date=pd.Timestamp("2026-09-03").date(),
        coverage_start=pd.Timestamp("2022-09-01").date(),
        coverage_end=pd.Timestamp("2026-09-01").date(),
        coverage_status=coverage_status,
        coverage_note="fixture",
        early_close_dates=frozenset(pd.Timestamp(value).date() for value in dates),
    )


@pytest.mark.parametrize(
    ("symbol", "commission", "per_side"),
    [
        ("6J", "6.20", "3.10"),
        ("MNQ", "1.82", "0.91"),
        ("MYM", "1.82", "0.91"),
        ("MGC", "2.12", "1.06"),
    ],
)
def test_primary_schedule_drives_phase1_fee_reconciliation(
    fee_schedule, symbol, commission, per_side
):
    """A non-primary resolver would misprice one or more campaign instruments."""
    trades = _trades(_trade(1, commission=commission, qty=1))

    venue = analyze_venue(trades, _spec(instrument=symbol), fee_schedule)

    assert venue.venue_commission_per_side_usd == Decimal(per_side)
    assert "EXPORT_VENUE_COMMISSION_MISMATCH" not in _issue_codes(venue)


def test_one_cent_export_venue_fee_mismatch_is_a_blocker(fee_schedule):
    """The aggregate cent tolerance must not be applied to fee provenance."""
    venue = analyze_venue(
        _trades(_trade(1, commission="1.84", qty=1)),
        _spec(instrument="MNQ", pine_commission="0.92"),
        fee_schedule,
    )

    issue = next(
        issue
        for issue in venue.issues
        if issue.code == "EXPORT_VENUE_COMMISSION_MISMATCH"
    )
    assert issue.severity == "BLOCKER"
    assert issue.detail["export_per_side_values_usd"] == (Decimal("0.92"),)
    assert issue.detail["venue_per_side_usd"] == Decimal("0.91")


def test_exposure_reports_tie_order_bounds(fee_schedule):
    """Choosing one same-timestamp order would conceal cap-status ambiguity."""
    trades = _overlapping_trades_same_boundary(qty=50)

    venue = analyze_venue(
        trades, _spec(instrument="MNQ", contract_cap=80), fee_schedule
    )

    assert venue.peak_open_micro_equivalent_quantity_min == 50
    assert venue.peak_open_micro_equivalent_quantity_max == 100
    assert "CAP_STATUS_AMBIGUOUS_AT_TIMESTAMP_TIE" in _issue_codes(venue)


def test_exposure_preserves_own_exit_causality_for_zero_duration_trade(fee_schedule):
    """Aggregated same-time deltas would turn a confirmed 81-unit peak into ambiguity."""
    trades = _trades(
        _trade_between(1, "2026-01-05 10:00", "2026-01-05 10:00", qty=81),
    )

    venue = analyze_venue(trades, _spec(contract_cap=80), fee_schedule)

    assert venue.peak_open_micro_equivalent_quantity_min == 81
    assert venue.peak_open_micro_equivalent_quantity_max == 81
    assert "CONTRACT_CAP_BREACH" in _issue_codes(venue)
    assert "CAP_STATUS_AMBIGUOUS_AT_TIMESTAMP_TIE" not in _issue_codes(venue)


def test_exposure_mixed_tie_never_goes_negative_and_keeps_distinct_bounds(fee_schedule):
    """Earlier exits must precede same-time entries while zero-duration exits follow them."""
    trades = _trades(
        _trade_between(1, "2026-01-05 09:00", "2026-01-05 10:00", qty=50),
        _trade_between(2, "2026-01-05 10:00", "2026-01-05 10:00", qty=70),
        _trade_between(3, "2026-01-05 10:00", "2026-01-05 11:00", qty=60),
    )

    venue = analyze_venue(trades, _spec(contract_cap=80), fee_schedule)

    assert venue.peak_open_micro_equivalent_quantity_min == 130
    assert venue.peak_open_micro_equivalent_quantity_max == 180


def test_6j_exposure_is_measured_in_micro_equivalents(fee_schedule):
    """The account cap counts one 6J contract as ten micros, not one unit."""
    assert micro_equivalent_multiplier("6J") == 10
    assert micro_equivalent_multiplier("MNQ") == 1

    at_cap = analyze_venue(
        _trades(_trade_between(1, "2026-01-05 09:00", "2026-01-05 10:00", qty=8)),
        _spec(instrument="6J", contract_cap=80, pine_commission="3.10"),
        fee_schedule,
    )
    over_cap = analyze_venue(
        _trades(_trade_between(2, "2026-01-05 09:00", "2026-01-05 10:00", qty=9)),
        _spec(instrument="6J", contract_cap=80, pine_commission="3.10"),
        fee_schedule,
    )

    assert at_cap.peak_open_micro_equivalent_quantity_max == 80
    assert "CONTRACT_CAP_BREACH" not in _issue_codes(at_cap)
    assert over_cap.peak_open_micro_equivalent_quantity_min == 90
    assert "CONTRACT_CAP_BREACH" in _issue_codes(over_cap)


def test_friday_to_sunday_hold_is_a_blocker_and_trade_is_retained(fee_schedule):
    """Force-flat auditing must report, rather than delete, a source trade."""
    trades = _trades(
        _trade_between(41, "2026-01-09 10:00", "2026-01-11 18:00", "1.82")
    )

    venue = analyze_venue(trades, _spec(), fee_schedule)

    assert venue.trade_count == 1
    assert venue.friday_to_sunday_holds == 1
    assert venue.overnight_holds == 1
    issue = next(i for i in venue.issues if i.code == "FORCE_FLAT_VIOLATION")
    assert issue.trade_id == 41
    assert issue.severity == "BLOCKER"


def test_aegis_pine_export_and_venue_commissions_stay_separate(fee_schedule):
    """Replacing observed export fees with Pine settings would hide Aegis drift."""
    trades = _trades(
        _trade(1, "2026-01-05 10:00", "50.20", "24.80", qty=4)
    )

    venue = analyze_venue(
        trades, _spec(instrument="6J", pine_commission="1.30"), fee_schedule
    )

    assert venue.export_implied_commission_per_side_usd == Decimal("3.10")
    assert venue.venue_commission_per_side_usd == Decimal("3.10")
    assert "PINE_EXPORT_COMMISSION_MISMATCH" in _issue_codes(venue)
    assert "PINE_VENUE_COMMISSION_MISMATCH" in _issue_codes(venue)
    assert "EXPORT_VENUE_COMMISSION_MISMATCH" not in _issue_codes(venue)
    pine_issues = {
        issue.code: issue.severity
        for issue in venue.issues
        if issue.code.startswith("PINE_") and issue.code.endswith("_COMMISSION_MISMATCH")
    }
    assert pine_issues == {
        "PINE_EXPORT_COMMISSION_MISMATCH": "WARNING",
        "PINE_VENUE_COMMISSION_MISMATCH": "WARNING",
    }


def test_continuous_contract_and_unobservable_spread_are_explicit(fee_schedule):
    """Continuous fills must not imply contract attribution or an observed spread."""
    venue = analyze_venue(
        _trades(_trade(1)), _spec(continuous_symbol=True), fee_schedule
    )

    assert "CONTINUOUS_CONTRACT_ROLL_UNRESOLVED" in _issue_codes(venue)
    assert venue.contract_month_attribution_status == "UNAVAILABLE"
    assert venue.roll_seam_attribution_status == "UNAVAILABLE"
    assert venue.bid_ask_spread_status == "NOT_SEPARATELY_OBSERVABLE"
    assert venue.slippage_basis == "PINE_DECLARED_TICKS_AND_FILL_PRICES"
    assert venue.pine_slippage_ticks_per_side == Decimal("1")


def test_off_tick_entry_and_exit_prices_are_reported_without_removing_trade(
    fee_schedule,
):
    """Rounding source fills onto the MNQ grid would silently repair evidence."""
    trade = _trade(7)
    trade["entry_price"] = Decimal("100.125")
    trade["exit_price"] = Decimal("101.0000000005")

    venue = analyze_venue(_trades(trade), _spec(), fee_schedule)

    assert venue.trade_count == 1
    issues = [issue for issue in venue.issues if issue.code == "OFF_TICK_PRICE"]
    assert [(issue.trade_id, issue.detail["leg"]) for issue in issues] == [
        (7, "ENTRY"),
        (7, "EXIT"),
    ]


def test_tick_grid_accepts_the_frozen_one_billionth_tick_tolerance(fee_schedule):
    """A stricter comparison would reject the explicitly accepted rounding boundary."""
    trade = _trade(8)
    trade["entry_price"] = Decimal("100.00000000025")

    venue = analyze_venue(_trades(trade), _spec(), fee_schedule)

    assert not [issue for issue in venue.issues if issue.code == "OFF_TICK_PRICE"]


def test_intended_and_encoded_instrument_mismatch_is_explicit(fee_schedule):
    """Analyzing encoded geometry must not certify a different intended instrument."""
    venue = analyze_venue(
        _trades(_trade(1)),
        _spec(instrument="MNQ", intended_instrument="MYM"),
        fee_schedule,
    )

    issue = next(i for i in venue.issues if i.code == "INSTRUMENT_MISMATCH")
    assert issue.detail == {
        "intended_instrument": "MYM",
        "encoded_instrument": "MNQ",
    }


def test_exposure_reports_confirmed_contract_cap_breach(fee_schedule):
    """A trade individually over cap is a breach under every tie ordering."""
    venue = analyze_venue(
        _trades(_trade_between(1, "2026-01-05 09:00", "2026-01-05 10:00", qty=81)),
        _spec(contract_cap=80),
        fee_schedule,
    )

    assert venue.peak_open_micro_equivalent_quantity_min == 81
    assert venue.peak_open_micro_equivalent_quantity_max == 81
    assert "CONTRACT_CAP_BREACH" in _issue_codes(venue)
    assert "CAP_STATUS_AMBIGUOUS_AT_TIMESTAMP_TIE" not in _issue_codes(venue)


def test_non_overlapping_trades_do_not_inflate_exposure(fee_schedule):
    """Summing all trade quantities would invent a cap breach without overlap."""
    venue = analyze_venue(
        _trades(
            _trade_between(1, "2026-01-05 09:00", "2026-01-05 10:00", qty=50),
            _trade_between(2, "2026-01-05 10:01", "2026-01-05 11:00", qty=50),
        ),
        _spec(contract_cap=80),
        fee_schedule,
    )

    assert venue.peak_open_micro_equivalent_quantity_min == 50
    assert venue.peak_open_micro_equivalent_quantity_max == 50
    assert not (
        {"CONTRACT_CAP_BREACH", "CAP_STATUS_AMBIGUOUS_AT_TIMESTAMP_TIE"}
        & _issue_codes(venue)
    )


def test_variable_export_commissions_are_reported_without_averaging(fee_schedule):
    """A mean could falsely agree with the primary fee while individual rows vary."""
    venue = analyze_venue(
        _trades(
            _trade(1, commission="1.82"),
            _trade(2, "2026-01-05 10:30", commission="2.00"),
        ),
        _spec(),
        fee_schedule,
    )

    assert venue.export_implied_commission_per_side_usd is None
    assert venue.export_implied_commission_per_side_values_usd == (
        Decimal("0.91"),
        Decimal("1.00"),
    )
    assert "VARIABLE_EXPORT_COMMISSION" in _issue_codes(venue)


def test_non_continuous_source_has_no_roll_attribution_issue(fee_schedule):
    """Specific-contract sources must not inherit the continuous-symbol blocker."""
    venue = analyze_venue(
        _trades(_trade(1)), _spec(continuous_symbol=False), fee_schedule
    )

    assert "CONTINUOUS_CONTRACT_ROLL_UNRESOLVED" not in _issue_codes(venue)
    assert venue.contract_month_attribution_status == "SOURCE_ENCODED_INSTRUMENT"
    assert venue.roll_seam_attribution_status == "NOT_APPLICABLE"


def test_force_flat_uses_daily_deadline_not_cross_date_or_weekend_proxy(fee_schedule):
    """The venue deadline, not the calendar boundary, defines the violation."""
    overnight = analyze_venue(
        _trades(
            _trade_between(3, "2026-01-05 23:00", "2026-01-06 01:00")
        ),
        _spec(),
        fee_schedule,
    )
    same_date = analyze_venue(
        _trades(
            _trade_between(4, "2026-01-05 15:00", "2026-01-05 18:30")
        ),
        _spec(),
        fee_schedule,
    )

    assert overnight.cross_date_holds == 1
    assert overnight.overnight_holds == 0
    assert overnight.friday_to_sunday_holds == 0
    assert "CROSS_DATE_HOLD" in _issue_codes(overnight)
    assert "FORCE_FLAT_VIOLATION" not in _issue_codes(overnight)
    assert same_date.cross_date_holds == 0
    assert same_date.overnight_holds == 1
    assert "FORCE_FLAT_VIOLATION" in _issue_codes(same_date)


def test_holiday_short_date_uses_1259_eastern_deadline(fee_schedule):
    """Applying the regular close on a CME early-close date would miss the breach."""
    calendar = _early_close_calendar("2026-07-03")
    venue = analyze_venue(
        _trades(
            _trade_between(5, "2026-07-03 12:30", "2026-07-03 13:30")
        ),
        _spec(),
        fee_schedule,
        early_close_calendar=calendar,
    )

    issue = next(i for i in venue.issues if i.code == "FORCE_FLAT_VIOLATION")
    assert issue.detail["deadline_timestamps"] == (
        pd.Timestamp("2026-07-03 12:59", tz="America/New_York"),
    )


def test_incomplete_holiday_calendar_sets_needs_context_cap(fee_schedule):
    """Unavailable primary-source history must remain visible in every venue report."""
    venue = analyze_venue(
        _trades(_trade(1)),
        _spec(),
        fee_schedule,
        early_close_calendar=_early_close_calendar(coverage_status="NEEDS_CONTEXT"),
    )

    assert venue.holiday_short_deadline_status == "NEEDS_CONTEXT"
    issue = next(i for i in venue.issues if i.code == "EARLY_CLOSE_CALENDAR_INCOMPLETE")
    assert issue.severity == "WARNING"


def test_campaign_calendar_freezes_primary_source_capture_gap(
    campaign_early_close_calendar,
):
    """A missing historical CME extract must be hashed and explicit, not inferred."""
    calendar = campaign_early_close_calendar

    assert calendar.source_url == "https://www.cmegroup.com/trading-hours.html"
    assert calendar.observed_date.isoformat() == "2026-09-03"
    assert calendar.coverage_start.isoformat() == "2022-09-01"
    assert calendar.coverage_end.isoformat() == "2026-09-01"
    assert calendar.coverage_status == "NEEDS_CONTEXT"
    assert calendar.early_close_dates == frozenset()


def test_complete_multiyear_calendar_requires_observed_early_close_rows(tmp_path):
    """A status label alone cannot certify a multi-year CME early-close capture."""
    path = tmp_path / "calendar.json"
    path.write_text(
        json.dumps(
            {
                "source_url": "https://www.cmegroup.com/trading-hours.html",
                "page_date": None,
                "observed_date": "2026-09-03",
                "coverage_start": "2022-09-01",
                "coverage_end": "2026-09-01",
                "coverage_status": "COMPLETE",
                "coverage_note": "unsupported empty complete fixture",
                "rows": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="COMPLETE multi-year.*rows"):
        load_early_close_calendar(path)


def test_calculate_accounting_uses_exit_chronology_and_decimal_money():
    """Float sums or entry chronology would change frozen accounting outputs."""
    trades = _trades(
        _trade(1, "2026-01-05 10:00", "10.00", "1.82", cumulative="10.00"),
        _trade(2, "2026-01-05 10:00", "-4.00", "1.82", cumulative="6.00"),
        _trade(3, "2026-02-02 10:00", "2.00", "1.82", cumulative="8.00"),
    )

    metrics = calculate_accounting(trades)

    assert metrics.trade_count == 3
    assert metrics.net_pnl_usd == Decimal("8.00")
    assert metrics.commission_usd == Decimal("5.46")
    assert metrics.profit_factor == Decimal("3.0000000000")
    assert metrics.max_drawdown_usd == Decimal("4.00")
    assert metrics.monthly_net_pnl == {
        "2026-01": Decimal("6.00"),
        "2026-02": Decimal("2.00"),
    }
    assert metrics.final_source_cumulative_pnl_usd == Decimal("8.00")
    assert not metrics.issues


def test_calculate_accounting_breaks_timestamp_ties_by_exit_source_row():
    """Using DataFrame order for simultaneous exits would make drawdown nondeterministic."""
    trades = _trades(
        _trade(2, "2026-01-05 10:00", "-4.00", "1.82", exit_row=2, cumulative="6.00"),
        _trade(1, "2026-01-05 10:00", "10.00", "1.82", exit_row=1, cumulative="10.00"),
        _trade(3, "2026-01-05 10:15", "-10.00", "1.82", exit_row=3, cumulative="-4.00"),
    )

    metrics = calculate_accounting(trades)

    assert metrics.max_drawdown_usd == Decimal("14.00")
    assert metrics.final_source_cumulative_pnl_usd == Decimal("-4.00")


def test_calculate_accounting_classifies_exact_zero_as_flat():
    """Quantized or sign-only classification could turn a flat into a win or loss."""
    metrics = calculate_accounting(
        _trades(
            _trade(1, "2026-01-05 10:00", "1.00", "0.10", cumulative="1.00"),
            _trade(2, "2026-01-05 10:15", "0.00", "0.10", cumulative="1.00"),
            _trade(3, "2026-01-05 10:30", "-0.25", "0.10", cumulative="0.75"),
        )
    )

    assert (metrics.wins, metrics.losses, metrics.flats) == (1, 1, 1)
    assert metrics.win_rate == Decimal("0.3333333333")


def test_calculate_accounting_reports_undefined_profit_factor_without_losses():
    """Inventing infinity or zero would conceal that profit factor is undefined."""
    metrics = calculate_accounting(
        _trades(_trade(1, "2026-01-05 10:00", "1.00", "0.10", cumulative="1.00"))
    )

    assert metrics.profit_factor is None
    assert [(issue.code, issue.severity) for issue in metrics.issues] == [
        ("NO_GROSS_LOSSES", "INFO")
    ]


def test_calculate_accounting_leaves_total_gross_unknown_if_any_trade_is_unknown():
    """Summing known gross rows would misstate an incomplete gross total as complete."""
    metrics = calculate_accounting(
        _trades(
            _trade(1, "2026-01-05 10:00", "1.00", "0.10", cumulative="1.00"),
            _trade(2, "2026-01-05 10:15", "-1.00", "0.10", cumulative="0.00", gross=None),
        )
    )

    assert metrics.gross_pnl_usd is None


def test_calculate_accounting_checks_only_final_source_cumulative_value():
    """A final mismatch must block even though intermediate interleaving is permitted."""
    metrics = calculate_accounting(
        _trades(
            _trade(1, "2026-01-05 10:00", "10.00", "1.82", cumulative="999.00"),
            _trade(2, "2026-01-05 10:15", "-4.00", "1.82", cumulative="6.02"),
        )
    )

    assert [(issue.code, issue.severity) for issue in metrics.issues] == [
        ("FINAL_CUMULATIVE_PNL_MISMATCH", "BLOCKER")
    ]
