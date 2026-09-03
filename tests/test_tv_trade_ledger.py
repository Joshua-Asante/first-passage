"""Behavior tests for the frozen Tradeify Phase 1 intake boundary."""

from hashlib import sha256
import json
from pathlib import Path

from decimal import Decimal

import pytest

from research_utils.tv_trade_ledger import (
    SourceIdentityError,
    load_fee_schedule,
    load_source_specs,
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
