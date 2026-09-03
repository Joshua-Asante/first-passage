"""Strict reconstruction and accounting tests for Tradeify Phase 1."""

from decimal import Decimal

import pandas as pd

from research_utils.trade_reconciliation import (
    TRADE_COLUMNS,
    calculate_accounting,
    instrument_geometry,
    reconstruct_trades,
)
from research_utils.tv_trade_ledger import SourceSpec


def _spec(*, instrument: str = "MNQ") -> SourceSpec:
    return SourceSpec(
        strategy_id="fixture",
        intended_instrument=instrument,
        encoded_instrument=instrument,
        export_filename="source.csv",
        export_sha256="0" * 64,
        pine_filename="source.pine",
        pine_sha256="1" * 64,
        source_timezone=None,
        session_timezone="America/New_York",
        declared_bar_size_minutes=15,
        declared_session="09:30-16:00 America/New_York",
        direction_evidence="long-only",
        quantity_convention="integer contracts",
        continuous_symbol=True,
        synchronized_intraday_path_available=False,
        lineage_notes=("fixture",),
        pine_commission_per_side_usd=Decimal("0.91"),
        pine_slippage_ticks_per_side=Decimal("1"),
        contract_cap=80,
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
    exit_timestamp: str,
    net: str,
    commission: str,
    *,
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
        "quantity": 1,
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
