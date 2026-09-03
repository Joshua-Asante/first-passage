"""Behavior tests for the frozen Tradeify Phase 1 intake boundary."""

from hashlib import sha256
import json
from pathlib import Path
import csv

from decimal import Decimal

import pytest

from research_utils.tv_trade_ledger import (
    SourceIdentityError,
    TradeExportSchemaError,
    load_fee_schedule,
    load_source_specs,
    normalize_export,
    verify_source_pair,
)


_CONFIG_PATH = Path(
    "lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json"
)
_FEE_PATH = Path(
    "lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/"
    "tradeify_commission_schedule.json"
)


def _spec_dict(strategy_id: str, export_filename: str, pine_filename: str) -> dict[str, object]:
    return {
        "strategy_id": strategy_id,
        "intended_instrument": "MNQ",
        "encoded_instrument": "MNQ",
        "export_filename": export_filename,
        "export_sha256": sha256(b"export").hexdigest(),
        "pine_filename": pine_filename,
        "pine_sha256": sha256(b"pine").hexdigest(),
        "source_timezone": None,
        "session_timezone": "America/New_York",
        "declared_bar_size_minutes": 15,
        "declared_session": "09:15-16:55 America/New_York",
        "direction_evidence": "long-only",
        "quantity_convention": "integer contracts",
        "continuous_symbol": True,
        "synchronized_intraday_path_available": False,
        "lineage_notes": ["development fixture"],
        "pine_commission_per_side_usd": "0.91",
        "pine_slippage_ticks_per_side": "1",
        "contract_cap": 80,
    }


def _source_spec(**overrides: object):
    payload = _spec_dict("fixture", "source.csv", "source.pine")
    payload.update(overrides)
    path = Path.cwd() / ".pytest_tv_trade_ledger_fixture_config.json"
    # The helper uses the loader so the identity test exercises the same real boundary.
    path.write_text(
        json.dumps(
            {
                "claim_class": "EXPLORATORY",
                "platform": "TradingView Strategy Tester over a continuous futures chart",
                "strategies": [payload],
            }
        ),
        encoding="utf-8",
    )
    try:
        return load_source_specs(path)[0]
    finally:
        path.unlink(missing_ok=True)


def test_load_source_specs_rejects_duplicate_strategy_id(tmp_path):
    """Removing identifier uniqueness must make the configuration invalid."""
    payload = {
        "claim_class": "EXPLORATORY",
        "platform": "TradingView Strategy Tester over a continuous futures chart",
        "strategies": [
            _spec_dict("same", "one.csv", "one.pine"),
            _spec_dict("same", "two.csv", "two.pine"),
        ],
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate strategy_id: same"):
        load_source_specs(path)


def test_load_source_specs_rejects_platformless_configuration(tmp_path):
    """Removing the frozen platform provenance must make the config invalid."""
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps(
            {
                "claim_class": "EXPLORATORY",
                "strategies": [_spec_dict("fixture", "source.csv", "source.pine")],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="source configuration keys mismatch"):
        load_source_specs(path)


def test_verify_source_pair_rejects_changed_export(tmp_path):
    """Removing byte-level export verification must surface a hard identity error."""
    export = tmp_path / "source.csv"
    pine = tmp_path / "source.pine"
    export.write_bytes(b"changed")
    pine.write_bytes(b"pine")
    spec = _source_spec(
        export_sha256=sha256(b"expected").hexdigest(),
        pine_sha256=sha256(b"pine").hexdigest(),
    )

    with pytest.raises(SourceIdentityError, match="source.csv.*SHA-256"):
        verify_source_pair(tmp_path, spec)


def test_frozen_configuration_has_seven_continuous_source_specs():
    """A changed campaign pin, session inventory, or source count must be observable."""
    specs = load_source_specs(_CONFIG_PATH)

    assert [spec.strategy_id for spec in specs] == [
        "aegis_6j1",
        "orb_mnq_recon_v7",
        "striker_dj30_mnq_prototype",
        "striker_dj30_mym_v45",
        "striker_nas100_mnq_v1",
        "striker_nas100_mym_prototype",
        "vanguard_mgc_v04",
    ]
    assert all(spec.source_timezone is None for spec in specs)
    assert all(spec.declared_bar_size_minutes == 15 for spec in specs)
    assert all(spec.continuous_symbol for spec in specs)
    assert all(not spec.synchronized_intraday_path_available for spec in specs)
    assert specs[0].declared_session == "10:00-13:45 America/New_York, Mon-Wed; force-flat 16:30 America/New_York"
    assert specs[2].intended_instrument == "MNQ"
    assert specs[2].encoded_instrument == "MYM"
    assert specs[5].intended_instrument == "MYM"
    assert specs[5].encoded_instrument == "MNQ"


def test_fee_schedule_uses_primary_round_trip_values_and_derives_per_side_values():
    """Changing a primary fee row or its per-side derivation must fail visibly."""
    schedule = load_fee_schedule(_FEE_PATH)

    assert schedule.round_trip_usd == {
        "6J": Decimal("6.20"),
        "MNQ": Decimal("1.82"),
        "MYM": Decimal("1.82"),
        "MGC": Decimal("2.12"),
    }
    assert schedule.per_side_usd == {
        "6J": Decimal("3.10"),
        "MNQ": Decimal("0.91"),
        "MYM": Decimal("0.91"),
        "MGC": Decimal("1.06"),
    }


def test_load_fee_schedule_rejects_duplicate_or_non_cent_rows(tmp_path):
    """Dropping unique-symbol or exact-cent validation must reject malformed fee evidence."""
    payload = {
        "source_url": "https://help.tradeify.co/en/articles/10468315-trading-commission-fees",
        "page_date": "2026-04-28",
        "observed_date": "2026-09-02",
        "totals_include": "exchange, NFA, clearing, and commission",
        "rows": [
            {"symbol": "MNQ", "round_trip_usd": "1.82"},
            {"symbol": "MNQ", "round_trip_usd": "1.823"},
        ],
    }
    path = tmp_path / "fees.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate fee symbol: MNQ"):
        load_fee_schedule(path)

    payload["rows"] = [{"symbol": "MNQ", "round_trip_usd": "1.823"}]
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="two decimal places"):
        load_fee_schedule(path)


_TV_HEADERS = [
    "Trade number", "Type", "Date and time", "Signal", "Price USD",
    "Size (qty)", "Size (value)", "Net PnL USD", "Return %", "Commission USD",
    "Favorable excursion USD", "Favorable excursion %", "Adverse excursion USD",
    "Adverse excursion %", "Cumulative PnL USD", "Cumulative PnL %", "Duration (bars)",
]


def _row(
    trade_number: object,
    type_: str,
    timestamp: str,
    *,
    net: str = "0.00",
    commission: str = "0.91",
    quantity: str = "1",
    **overrides: object,
) -> dict[str, object]:
    row: dict[str, object] = {
        "Trade number": trade_number,
        "Type": type_,
        "Date and time": timestamp,
        "Signal": "fixture signal",
        "Price USD": "100.00",
        "Size (qty)": quantity,
        "Size (value)": "100.00",
        "Net PnL USD": net,
        "Return %": "0.00",
        "Commission USD": commission,
        "Favorable excursion USD": "0.00",
        "Favorable excursion %": "0.00",
        "Adverse excursion USD": "0.00",
        "Adverse excursion %": "0.00",
        "Cumulative PnL USD": net,
        "Cumulative PnL %": "0.00",
        "Duration (bars)": "0",
    }
    row.update(overrides)
    return row


def _verified_csv(
    tmp_path: Path,
    *,
    rows: list[dict[str, object]],
    source_timezone: str | None = None,
    headers: list[str] | None = None,
    bom: bool = False,
):
    tmp_path.mkdir(parents=True, exist_ok=True)
    export = tmp_path / "source.csv"
    pine = tmp_path / "source.pine"
    headers = headers or _TV_HEADERS
    with export.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    if bom:
        export.write_bytes(b"\xef\xbb\xbf" + export.read_bytes())
    pine.write_text("pine", encoding="utf-8")
    spec = _source_spec(
        export_sha256=sha256(export.read_bytes()).hexdigest(),
        pine_sha256=sha256(pine.read_bytes()).hexdigest(),
        source_timezone=source_timezone,
    )
    return verify_source_pair(tmp_path, spec)


def test_normalize_retains_exit_first_source_order_and_flags_timestamp_tie(tmp_path):
    """Removing source-row tie breaking would reorder same-minute exit/entry data."""
    source = _verified_csv(
        tmp_path,
        rows=[
            _row(1, "Exit long", "2026-01-05 10:00", net="8.18", commission="1.82"),
            _row(1, "Entry long", "2026-01-05 10:00", net="8.18", commission="1.82"),
        ],
    )

    result = normalize_export(source)

    assert result.events["source_row_number"].tolist() == [1, 2]
    assert result.events["event_type"].tolist() == ["EXIT", "ENTRY"]
    assert result.events["timestamp_utc"].isna().all()
    assert result.events["exchange_session_date"].isna().all()
    assert result.events["concurrent_timestamp"].tolist() == [True, True]


def test_normalize_localizes_only_with_explicit_timezone(tmp_path):
    """Ignoring configured source timezones would produce the wrong UTC instant."""
    source = _verified_csv(
        tmp_path,
        rows=[_row(1, "Entry long", "2026-01-05 09:30")],
        source_timezone="America/New_York",
    )

    event = normalize_export(source).events.iloc[0]

    assert event["timestamp_utc"].isoformat() == "2026-01-05T14:30:00+00:00"
    assert str(event["exchange_session_date"]) == "2026-01-05"


def test_normalize_rejects_unknown_type_instead_of_guessing(tmp_path):
    """Broad type matching would turn an unsupported source label into a trade event."""
    source = _verified_csv(tmp_path, rows=[_row(1, "Buy maybe", "2026-01-05 09:30")])

    with pytest.raises(TradeExportSchemaError, match="unknown Type.*Buy maybe"):
        normalize_export(source)


def test_normalize_rejects_noncanonical_timestamp_text(tmp_path):
    """Permitting unpadded fields would silently repair the source timestamp text."""
    source = _verified_csv(tmp_path, rows=[_row(1, "Entry long", "2026-1-5 9:03")])

    with pytest.raises(TradeExportSchemaError, match="Date and time must match"):
        normalize_export(source)


def test_normalize_accepts_bom_and_accounting_parentheses(tmp_path):
    """Dropping BOM or accounting-negative handling would reject valid source CSV syntax."""
    source = _verified_csv(
        tmp_path,
        rows=[_row(1, "Exit short", "2026-01-05 09:30", net="($12.34)")],
        bom=True,
    )

    event = normalize_export(source).events.iloc[0]

    assert event["net_pnl_usd"] == Decimal("-12.34")
    assert event["source_trade_id"] == 1


def test_normalize_rejects_missing_or_duplicate_canonical_columns(tmp_path):
    """Relaxing exact canonical headers would hide incompatible export schemas."""
    missing = _verified_csv(
        tmp_path / "missing",
        rows=[_row(1, "Entry long", "2026-01-05 09:30")],
        headers=[header for header in _TV_HEADERS if header != "Signal"],
    )
    with pytest.raises(TradeExportSchemaError, match="missing required columns.*Signal"):
        normalize_export(missing)

    duplicate_headers = ["Trade #", *_TV_HEADERS]
    duplicate = _verified_csv(
        tmp_path / "duplicate",
        rows=[_row(1, "Entry long", "2026-01-05 09:30", **{"Trade #": "1"})],
        headers=duplicate_headers,
    )
    with pytest.raises(TradeExportSchemaError, match="duplicate canonical columns.*Trade number"):
        normalize_export(duplicate)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("Net PnL USD", "", "Net PnL USD"),
        ("Size (qty)", "1.5", r"Size \(qty\).*positive integral"),
        ("Price USD", "NaN", "Price USD.*finite"),
        ("Price USD", "1,000.00", "Price USD.*decimal"),
    ],
)
def test_normalize_rejects_invalid_required_numeric_values(tmp_path, field, value, message):
    """Permitting blank, fractional, non-finite, or comma-formatted numerics corrupts accounting."""
    source = _verified_csv(
        tmp_path,
        rows=[_row(1, "Entry long", "2026-01-05 09:30", **{field: value})],
    )

    with pytest.raises(TradeExportSchemaError, match=message):
        normalize_export(source)


@pytest.mark.parametrize("wall_time", ["2026-03-08 02:30", "2026-11-01 01:30"])
def test_normalize_rejects_nonexistent_and_ambiguous_dst_wall_times(tmp_path, wall_time):
    """Accepting DST gaps or folds would silently choose a distinct instant."""
    source = _verified_csv(
        tmp_path,
        rows=[_row(1, "Entry long", wall_time)],
        source_timezone="America/New_York",
    )

    with pytest.raises(TradeExportSchemaError, match="ambiguous or nonexistent"):
        normalize_export(source)
