"""Tests for core/csv_parser.

Regression coverage for three verified defects:
1. _parse_datetime format ordering — day-first is the documented DXTrade
   convention (dxtrade_pdf_to_csv emits DD/MM/YYYY), so ambiguous dates must
   resolve day-first, and the 2-digit-year WITH-seconds variant must parse
   at all.
2. Trade.__post_init__ swap sign — swap is signed (credits positive, per
   docs/external/fxify_swap_rates_2026-05-25.md and reconcile.py's signed add);
   commission is always a cost.
3. _try_trade_level_parse silent row-dropping — skipped rows must be counted
   and warned to stderr, never dropped silently.
"""

from datetime import datetime

import pytest

from csv_parser import Trade, _get_val, _parse_datetime, parse_dxtrade_csv


# ---------------------------------------------------------------------------
# 1. Datetime format ordering (day-first before month-first)
# ---------------------------------------------------------------------------

def test_ambiguous_date_with_seconds_parses_day_first():
    """'01/04/2026 08:30:00' is April 1 (DXTrade DD/MM), not January 4."""
    assert _parse_datetime("01/04/2026 08:30:00") == datetime(2026, 4, 1, 8, 30, 0)


def test_unambiguous_day_first_with_seconds_parses():
    """day > 12 forces day-first — must parse and land on the right date."""
    assert _parse_datetime("25/04/2026 08:30:00") == datetime(2026, 4, 25, 8, 30, 0)


def test_two_digit_year_with_seconds_parses_day_first():
    """'01/04/26 08:30:00' (2-digit year WITH seconds) previously matched no
    format usefully — must parse as 2026-04-01, not year 26 or ValueError."""
    assert _parse_datetime("01/04/26 08:30:00") == datetime(2026, 4, 1, 8, 30, 0)


def test_two_digit_year_no_seconds_still_parses():
    """Existing DXTrade FXIFY format keeps working."""
    assert _parse_datetime("01/04/26 08:30") == datetime(2026, 4, 1, 8, 30)


def test_iso_formats_still_parse():
    assert _parse_datetime("2026-04-01 08:30:00") == datetime(2026, 4, 1, 8, 30, 0)
    assert _parse_datetime("2026-04-01T08:30:00") == datetime(2026, 4, 1, 8, 30, 0)
    assert _parse_datetime("2026-04-01 08:30") == datetime(2026, 4, 1, 8, 30)


def test_month_first_remains_last_resort():
    """A string only a month-first format can match must still parse
    (month > 12 in the day slot rules out day-first)."""
    assert _parse_datetime("04/25/2026 08:30:00") == datetime(2026, 4, 25, 8, 30, 0)


def test_unparseable_datetime_raises():
    with pytest.raises(ValueError):
        _parse_datetime("not a date")


# ---------------------------------------------------------------------------
# 2. Swap sign in Trade.__post_init__
# ---------------------------------------------------------------------------

def _make_trade(pnl: float, commission: float = 0.0, swap: float = 0.0,
                net_pnl: float = 0.0) -> Trade:
    return Trade(
        trade_id="1",
        instrument="XAUUSD",
        direction="short",
        lots=0.1,
        entry_time=datetime(2026, 4, 1, 8, 30),
        entry_price=2000.0,
        exit_time=datetime(2026, 4, 2, 8, 30),
        exit_price=1990.0,
        pnl=pnl,
        commission=commission,
        swap=swap,
        net_pnl=net_pnl,
    )


def test_swap_credit_increases_net_pnl():
    """Signed convention: XAUUSD short swap is a CREDIT (+43.84 per
    fxify_swap_rates_2026-05-25.md) and must add to net P&L."""
    t = _make_trade(pnl=100.0, commission=5.0, swap=43.84)
    assert t.net_pnl == pytest.approx(100.0 - 5.0 + 43.84)


def test_swap_charge_decreases_net_pnl():
    t = _make_trade(pnl=100.0, commission=5.0, swap=-10.0)
    assert t.net_pnl == pytest.approx(100.0 - 5.0 - 10.0)


def test_commission_always_a_cost_even_if_exported_negative():
    """Brokers export commission with inconsistent sign — always a cost."""
    t = _make_trade(pnl=100.0, commission=-5.0, swap=0.0)
    assert t.net_pnl == pytest.approx(95.0)


def test_post_init_bypassed_when_net_pnl_provided():
    """Order-level parse supplies net_pnl directly — __post_init__ must not
    recompute over it."""
    t = _make_trade(pnl=100.0, commission=5.0, swap=-10.0, net_pnl=77.7)
    assert t.net_pnl == 77.7


# ---------------------------------------------------------------------------
# 3. Unparseable-row counting in the trade-level parse loop
# ---------------------------------------------------------------------------

_TRADE_LEVEL_HEADER = (
    "Symbol,Side,Volume,Open Time,Open Price,Close Time,Close Price,"
    "Profit,Commission,Swap\n"
)


def test_unparseable_rows_warn_and_drop_only_bad_rows(tmp_path, capsys):
    csv_path = tmp_path / "export.csv"
    csv_path.write_text(
        _TRADE_LEVEL_HEADER
        + "XAUUSD,Sell,0.5,01/04/2026 08:30:00,2000.0,01/04/2026 12:30:00,1990.0,500.0,5.0,0.0\n"
        # Bad row: datetime garbage passes the essential-data check but fails parse
        + "XAUUSD,Sell,0.5,garbage,2000.0,also garbage,1990.0,500.0,5.0,0.0\n"
        + "USDJPY,Buy,1.0,02/04/2026 09:00:00,150.0,02/04/2026 10:00:00,150.5,300.0,3.0,0.0\n",
        encoding="utf-8",
    )
    trades = parse_dxtrade_csv(str(csv_path))
    assert len(trades) == 2
    assert {t.instrument for t in trades} == {"XAUUSD", "USDJPY"}
    captured = capsys.readouterr()
    assert "skipped 1 unparseable rows (of 3)" in captured.err


def test_no_warning_when_all_rows_parse(tmp_path, capsys):
    csv_path = tmp_path / "export.csv"
    csv_path.write_text(
        _TRADE_LEVEL_HEADER
        + "XAUUSD,Sell,0.5,01/04/2026 08:30:00,2000.0,01/04/2026 12:30:00,1990.0,500.0,5.0,0.0\n",
        encoding="utf-8",
    )
    trades = parse_dxtrade_csv(str(csv_path))
    assert len(trades) == 1
    captured = capsys.readouterr()
    assert "unparseable" not in captured.err


# ---------------------------------------------------------------------------
# 4. Order-level matching and deterministic header resolution
# ---------------------------------------------------------------------------

_ORDER_LEVEL_HEADER = (
    "Position Effect,Symbol,Date and Time,Side,Trade Volume,Trade Price,"
    "Trade Code,Closed P&L,Net Closed P&L,Commission\n"
)


def test_order_level_pairing_is_chronological_fifo(tmp_path):
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text(
        _ORDER_LEVEL_HEADER
        + "Opening,DJ30,2026-07-11 10:30:00,Buy,1.0,102,open-b,,,0\n"
        + "Opening,DJ30,2026-07-11 10:00:00,Buy,1.0,101,open-a,,,0\n"
        + "Closing,DJ30,2026-07-11 11:00:00,Sell,1.0,103,close,50,50,0\n",
        encoding="utf-8",
    )

    trades = parse_dxtrade_csv(str(csv_path))

    assert len(trades) == 1
    assert trades[0].entry_time == datetime(2026, 7, 11, 10, 0)
    assert trades[0].entry_price == 101.0


def test_order_level_orphan_close_is_rejected(tmp_path, capsys):
    csv_path = tmp_path / "orphan.csv"
    csv_path.write_text(
        _ORDER_LEVEL_HEADER
        + "Closing,DJ30,2026-07-11 11:00:00,Sell,1.0,103,close,50,50,0\n",
        encoding="utf-8",
    )

    assert parse_dxtrade_csv(str(csv_path)) == []
    assert "skipped 1 unmatched close rows" in capsys.readouterr().err


def test_header_matching_rejects_ambiguous_partial_matches():
    row = {"Gross Profit": "100", "Net Profit": "90"}

    with pytest.raises(ValueError, match="Ambiguous CSV headers"):
        _get_val(row, list(row), ["profit"])
