"""Behavior tests for the frozen Tradeify Phase 1 intake boundary."""

from hashlib import sha256
import json
from pathlib import Path
import csv
import subprocess

from decimal import Decimal
from uuid import uuid4

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
        "export_bytes": len(b"export"),
        "pine_filename": pine_filename,
        "pine_sha256": sha256(b"pine").hexdigest(),
        "pine_input_overrides_sha256": "a" * 64,
        "pine_bytes": len(b"pine"),
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
        "pine_pyramiding_pct": "100",
        "pine_pin_status": "NOT_IN_PORT_MANIFEST",
        "pin_ref": None,
        "pin_divergence": None,
        "contract_cap": 80,
    }


def _unresolved_roll_policy():
    return {"disposition": "UNRESOLVED", "ruling_date": "2026-09-03",
            "ruling_ref": "Synthetic fixture has no acceptance ruling", "obligations": []}


def _source_spec(**overrides: object):
    payload = _spec_dict("fixture", "source.csv", "source.pine")
    payload.update(overrides)
    path = Path.cwd() / f".pytest_tv_trade_ledger_fixture_{uuid4().hex}.json"
    # The helper uses the loader so the identity test exercises the same real boundary.
    path.write_text(
        json.dumps(
            {
                "claim_class": "EXPLORATORY",
                "platform": "TradingView Strategy Tester over a continuous futures chart",
                "strategies": [payload],
                "dropped_sources": [],
                "continuous_contract_roll_policy": _unresolved_roll_policy(),
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
        "dropped_sources": [],
        "continuous_contract_roll_policy": _unresolved_roll_policy(),
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate strategy_id: same"):
        load_source_specs(path)


@pytest.mark.parametrize("capture_name", ["capture.json", "capture.png", "capture.txt", "nested/capture.json"])
def test_private_override_captures_are_ignored_before_normal_staging(tmp_path, capture_name):
    """Removing private-directory coverage must expose a normal-staging leak."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True, capture_output=True)
    empty_excludes = tmp_path / "empty-excludes"
    empty_excludes.write_text("", encoding="utf-8")
    git = ["git", "-c", f"core.excludesFile={empty_excludes}", "-C", str(repo)]
    (repo / ".gitignore").write_bytes((_CONFIG_PATH.parent / ".gitignore").read_bytes())
    relative = f"inputs/private_overrides/{capture_name}"
    artifact = repo / relative
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("synthetic ignore probe; not a capture", encoding="utf-8")

    ignored = subprocess.run(git + ["check-ignore", "-v", relative], capture_output=True, text=True)
    assert ignored.returncode == 0, "private non-CSV capture is not ignored"
    assert "inputs/private_overrides/" in ignored.stdout
    status = subprocess.run(
        git + ["status", "--porcelain", "--ignored", "--untracked-files=all", "--", relative],
        check=True, capture_output=True, text=True,
    )
    assert status.stdout == f"!! {relative}\n"
    subprocess.run(git + ["add", "--all"], check=True, capture_output=True)
    tracked = subprocess.run(git + ["ls-files", "--", relative], check=True, capture_output=True, text=True)
    assert tracked.stdout == ""


@pytest.mark.parametrize(
    "digest",
    [None, "", "a" * 63, "a" * 65, "A" * 64, "g" * 64, "a" * 64 + "\n", 7, {}],
)
def test_input_override_digest_rejects_malformed_values(digest):
    with pytest.raises(ValueError, match="pine_input_overrides_sha256"):
        _source_spec(pine_input_overrides_sha256=digest)


def test_input_override_digest_is_required(tmp_path):
    from test_tradeify_phase1_identity_policy import configuration
    path, payload = configuration(tmp_path)
    payload["strategies"][0].pop("pine_input_overrides_sha256")
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="pine_input_overrides_sha256"):
        load_source_specs(path)


def test_input_override_raw_map_is_rejected():
    with pytest.raises(ValueError, match="pine_input_overrides"):
        _source_spec(pine_input_overrides={})


def test_populated_configuration_binds_five_distinct_private_capture_digests():
    """Missing or reused capture pins must not satisfy the populated intake."""
    specs = load_source_specs(_CONFIG_PATH)

    assert len(specs) == 5
    assert len({spec.pine_input_overrides_sha256 for spec in specs}) == 5


def test_load_source_specs_rejects_platformless_configuration(tmp_path):
    """Removing the frozen platform provenance must make the config invalid."""
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps(
            {
                "claim_class": "EXPLORATORY",
                "strategies": [_spec_dict("fixture", "source.csv", "source.pine")],
                "dropped_sources": [],
                "continuous_contract_roll_policy": _unresolved_roll_policy(),
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
        export_bytes=len(b"changed"),
        pine_bytes=len(b"pine"),
    )

    with pytest.raises(SourceIdentityError, match="source.csv.*SHA-256"):
        verify_source_pair(tmp_path, spec)


@pytest.mark.parametrize("state", ["match", "mismatch", "absent"])
def test_verify_private_override_artifact_hashes_exact_bytes(tmp_path, state):
    """Missing, changed or decoded/re-encoded evidence must never satisfy the pin."""
    from research_utils import tv_trade_ledger
    verify = getattr(tv_trade_ledger, "verify_input_overrides", None)
    assert callable(verify), "private input overrides need a runtime verification boundary"
    raw = b"opaque synthetic evidence\r\n\xff"
    digest = sha256(raw).hexdigest()
    spec = _source_spec(pine_input_overrides_sha256=digest)
    directory = tmp_path / "inputs" / "private_overrides"
    directory.mkdir(parents=True)
    if state != "absent":
        (directory / "fixture.json").write_bytes(raw if state == "match" else raw.replace(b"\r\n", b"\n"))
    if state == "match":
        assert verify(tmp_path, spec) == digest
    else:
        with pytest.raises(SourceIdentityError, match="private input overrides") as error:
            verify(tmp_path, spec)
        assert "opaque synthetic evidence" not in str(error.value)


def test_frozen_configuration_has_five_continuous_source_specs():
    """A changed campaign pin, session inventory, or source count must be observable."""
    specs = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))["strategies"]

    assert [spec["strategy_id"] for spec in specs] == [
        "aegis_6j1",
        "orb_mnq_recon_v7",
        "striker_dj30_mym_pyramid_250",
        "striker_nas100_mnq_dow_wed_excluded",
        "vanguard_mgc_v04",
    ]
    assert all(spec["source_timezone"] == "America/New_York" for spec in specs)
    assert all(spec["declared_bar_size_minutes"] == 15 for spec in specs)
    assert all(spec["continuous_symbol"] for spec in specs)
    assert all(not spec["synchronized_intraday_path_available"] for spec in specs)
    assert all(spec["contract_cap"] == 80 for spec in specs)
    assert specs[0]["declared_session"] == "10:00-13:45 America/New_York, Mon-Wed; force-flat 16:30 America/New_York"
    assert specs[2]["intended_instrument"] == "MYM"
    assert specs[2]["encoded_instrument"] == "MYM"
    assert specs[3]["intended_instrument"] == "MNQ"
    assert specs[3]["encoded_instrument"] == "MNQ"


def test_frozen_configuration_records_pine_pyramiding_from_each_source():
    """Losing the source-grounded add-size inventory would hide the one reduced cell."""
    specs = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))["strategies"]

    assert {spec["strategy_id"]: spec["pine_pyramiding_pct"] for spec in specs} == {
        "aegis_6j1": "0",
        "orb_mnq_recon_v7": "100",
        "striker_dj30_mym_pyramid_250": "250",
        "striker_nas100_mnq_dow_wed_excluded": "1000",
        "vanguard_mgc_v04": "80",
    }
    assert [spec["pine_pyramiding_pct"] for spec in specs].count("250") == 1


def test_frozen_configuration_preserves_exact_populated_inventory_bytes():
    """The populated snapshot pins all metadata without restating private inputs."""
    assert sha256(_CONFIG_PATH.read_bytes()).hexdigest() == (
        "a00bdd32687744b729510efe16704b0eb2c094d8551a7d91e87c5d6b878d9acb"
    )


def test_frozen_configuration_records_manifest_derived_pin_status_and_body_identity():
    """Mislabeling a supplied Pine as locked, swapped, or pyramid-down must be visible."""
    specs = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))["strategies"]
    by_hash = {spec["pine_sha256"]: spec for spec in specs}

    assert {
        pine_hash: spec["pine_pin_status"]
        for pine_hash, spec in by_hash.items()
    } == {
        "db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c": "NOT_IN_PORT_MANIFEST",
        "176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3": "NOT_IN_PORT_MANIFEST",
        "712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7": "UNPINNED_MODIFIED",
        "fa6a70cde002131bbd266bee70defb01e32deae2de79fdc327d661f829115c39": "UNPINNED_MODIFIED",
        "af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15": "NOT_IN_PORT_MANIFEST",
    }
    dj_modified = by_hash[
        "712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7"
    ]
    assert dj_modified["strategy_id"] == "striker_dj30_mym_pyramid_250"
    assert dj_modified["pine_pyramiding_pct"] == "250"
    assert dj_modified["pin_divergence"] == "pyramid 250% vs locked 750%; initial_capital 100000 vs research-variant pin 200000"
    assert dj_modified["pin_ref"].endswith("striker_dj30_v4.5_mym_pyramid_250.pine")
    nas_modified = by_hash["fa6a70cde002131bbd266bee70defb01e32deae2de79fdc327d661f829115c39"]
    assert nas_modified["strategy_id"] == "striker_nas100_mnq_dow_wed_excluded"
    assert nas_modified["pine_pyramiding_pct"] == "1000"
    assert nas_modified["pine_pin_status"] == "UNPINNED_MODIFIED"
    assert nas_modified["pin_divergence"] == "day-of-week set {Mon,Tue,Thu,Fri} vs locked {Mon,Tue}; initial_capital 100000 vs research-variant pin 200000"
    assert nas_modified["pin_ref"].endswith("striker_nas100_v1_mnq_dow_wed_excluded.pine")
    assert all(
        "_v45" not in spec["strategy_id"] and "_v1" not in spec["strategy_id"]
        for spec in specs
        if spec["strategy_id"].startswith("striker_")
    )


def test_load_source_specs_rejects_unknown_pine_pin_status(tmp_path):
    """Accepting an arbitrary manifest label would make the identity audit non-closed."""
    payload = {
        "claim_class": "EXPLORATORY",
        "platform": "TradingView Strategy Tester over a continuous futures chart",
        "strategies": [_spec_dict("fixture", "source.csv", "source.pine")],
        "dropped_sources": [],
        "continuous_contract_roll_policy": _unresolved_roll_policy(),
    }
    payload["strategies"][0]["pine_pin_status"] = "PINNED_LOCKED_EDITION"
    path = tmp_path / "config.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="pine_pin_status must be one of"):
        load_source_specs(path)


@pytest.mark.parametrize(
    ("pine_pin_status", "pin_divergence", "match"),
    [
        ("UNPINNED_MODIFIED", None, "UNPINNED_MODIFIED requires a non-empty pin_divergence"),
        ("UNPINNED_MODIFIED", "", "UNPINNED_MODIFIED requires a non-empty pin_divergence"),
        ("NOT_IN_PORT_MANIFEST", "body changed", "NOT_IN_PORT_MANIFEST requires null"),
        ("PINNED_SWAP_PROTOTYPE", "body changed", "pin_divergence must be null"),
    ],
)
def test_load_source_specs_couples_pin_status_to_divergence(
    tmp_path, pine_pin_status, pin_divergence, match
):
    """A modified-body label without facts, or facts on another label, corrupts identity."""
    payload = {
        "claim_class": "EXPLORATORY",
        "platform": "TradingView Strategy Tester over a continuous futures chart",
        "strategies": [
            _spec_dict("fixture", "source.csv", "source.pine")
        ],
        "dropped_sources": [],
        "continuous_contract_roll_policy": _unresolved_roll_policy(),
    }
    payload["strategies"][0]["pine_pin_status"] = pine_pin_status
    payload["strategies"][0]["pin_divergence"] = pin_divergence
    path = tmp_path / "config.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match=match):
        load_source_specs(path)


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


def test_load_fee_schedule_requires_the_complete_frozen_symbol_set(tmp_path):
    """A missing or unrelated fee symbol must fail during configuration loading."""
    payload = {
        "source_url": "https://help.tradeify.co/en/articles/10468315-trading-commission-fees",
        "page_date": "2026-04-28",
        "observed_date": "2026-09-02",
        "totals_include": "exchange, NFA, clearing, and commission",
        "rows": [
            {"symbol": "6J", "round_trip_usd": "6.20"},
            {"symbol": "MNQ", "round_trip_usd": "1.82"},
            {"symbol": "MYM", "round_trip_usd": "1.82"},
        ],
    }
    path = tmp_path / "fees.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="fee schedule symbols mismatch.*MGC"):
        load_fee_schedule(path)

    payload["rows"].append({"symbol": "MGC", "round_trip_usd": "2.12"})
    payload["rows"].append({"symbol": "ES", "round_trip_usd": "2.50"})
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="fee schedule symbols mismatch.*ES"):
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
    omit_final_field: bool = False,
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
    if omit_final_field:
        export.write_bytes(export.read_bytes().rsplit(b",", 1)[0])
    pine.write_text("pine", encoding="utf-8")
    spec = _source_spec(
        export_sha256=sha256(export.read_bytes()).hexdigest(),
        pine_sha256=sha256(pine.read_bytes()).hexdigest(),
        export_bytes=len(export.read_bytes()),
        pine_bytes=len(pine.read_bytes()),
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


def test_normalize_uses_the_export_bytes_verified_before_file_replacement(tmp_path):
    """Reading the pathname after hash verification would permit a TOCTOU export swap."""
    source = _verified_csv(
        tmp_path,
        rows=[_row(1, "Entry long", "2026-01-05 10:00", Signal="verified")],
    )
    replacement = _row(2, "Entry long", "2026-01-05 11:00", Signal="replaced")
    with source.export_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=_TV_HEADERS)
        writer.writeheader()
        writer.writerow(replacement)

    events = normalize_export(source).events

    assert events["source_trade_id"].tolist() == [1]
    assert events["signal"].tolist() == ["verified"]


def test_normalize_maps_hash_pinned_malformed_utf8_to_schema_error(tmp_path):
    """A decode failure at the CSV intake boundary must be typed, not leak a traceback."""
    export = tmp_path / "source.csv"
    pine = tmp_path / "source.pine"
    export.write_bytes(b"\xff")
    pine.write_bytes(b"pine")
    source = verify_source_pair(
        tmp_path,
        _source_spec(
            export_sha256=sha256(export.read_bytes()).hexdigest(),
            pine_sha256=sha256(pine.read_bytes()).hexdigest(),
            export_bytes=len(export.read_bytes()),
            pine_bytes=len(pine.read_bytes()),
        ),
    )

    with pytest.raises(TradeExportSchemaError, match="UTF-8"):
        normalize_export(source)


def test_normalize_empty_canonical_export_retains_typed_event_columns(tmp_path):
    """A header-only valid export is an empty typed ledger, not an untyped frame."""
    source = _verified_csv(tmp_path, rows=[])

    events = normalize_export(source).events

    assert list(events.columns) == [
        "strategy_id", "encoded_instrument", "source_trade_id", "source_row_number", "source_row_sha256",
        "timestamp_raw", "timestamp_naive", "timestamp_utc", "exchange_session_date",
        "type_raw", "event_type", "direction", "signal", "price_usd", "quantity",
        "size_value_usd", "net_pnl_usd", "return_pct", "commission_usd",
        "favorable_excursion_usd", "favorable_excursion_pct", "adverse_excursion_usd",
        "adverse_excursion_pct", "cumulative_pnl_usd", "cumulative_pnl_pct",
        "duration_bars", "concurrent_timestamp",
    ]
    assert events.empty
    assert str(events["source_trade_id"].dtype) == "int64"
    assert str(events["source_row_number"].dtype) == "int64"
    assert str(events["quantity"].dtype) == "int64"
    assert str(events["timestamp_naive"].dtype) == "datetime64[ns]"
    assert str(events["timestamp_utc"].dtype) == "datetime64[ns, UTC]"
    assert str(events["concurrent_timestamp"].dtype) == "bool"
    assert events["price_usd"].dtype == object
    assert events["exchange_session_date"].dtype == object


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


def test_normalize_rejects_short_record_as_schema_error(tmp_path):
    """A truncated final field must not surface as an internal mapping KeyError."""
    source = _verified_csv(
        tmp_path,
        rows=[_row(1, "Entry long", "2026-01-05 09:30")],
        omit_final_field=True,
    )

    with pytest.raises(TradeExportSchemaError, match="source row 1 has 16 fields; expected 17"):
        normalize_export(source)


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
