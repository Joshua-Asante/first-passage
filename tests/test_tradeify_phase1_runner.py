"""Synthetic end-to-end tests for the five-active-source Phase 1 runner."""

import csv
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from research_utils import tv_trade_ledger
from test_tv_trade_ledger import _unresolved_roll_policy


_RUNNER_PATH = (
    Path(__file__).parents[1]
    / "lab"
    / "analysis"
    / "c1"
    / "tradeify_seven_strategy_phase1_2026-09"
    / "run_phase1.py"
)
_CAMPAIGN_DIR = _RUNNER_PATH.parent
_SPEC = importlib.util.spec_from_file_location("tradeify_phase1_runner", _RUNNER_PATH)
assert _SPEC is not None and _SPEC.loader is not None
run_phase1 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(run_phase1)

_FROZEN_STRATEGY_IDS = [
    "aegis_6j1",
    "orb_mnq_recon_v7",
    "striker_dj30_mym_pyramid_250",
    "striker_nas100_mnq_dow_wed_excluded",
    "vanguard_mgc_v04",
]


_HEADERS = [
    "Trade number",
    "Type",
    "Date and time",
    "Signal",
    "Price USD",
    "Size (qty)",
    "Size (value)",
    "Net PnL USD",
    "Return %",
    "Commission USD",
    "Favorable excursion USD",
    "Favorable excursion %",
    "Adverse excursion USD",
    "Adverse excursion %",
    "Cumulative PnL USD",
    "Cumulative PnL %",
    "Duration (bars)",
]


def _csv_bytes(index: int) -> bytes:
    rows = [
        [
            "1",
            "Entry long",
            f"2026-01-{index + 1:02d} 10:00",
            "fixture",
            "100.00",
            "1",
            "100.00",
            "0.18",
            "1.00",
            "1.82",
            "2.00",
            "2.00",
            "-1.00",
            "-1.00",
            "0.18",
            "1.00",
            "1",
        ],
        [
            "1",
            "Exit long",
            f"2026-01-{index + 1:02d} 10:15",
            "fixture",
            "101.00",
            "1",
            "100.00",
            "0.18",
            "1.00",
            "1.82",
            "2.00",
            "2.00",
            "-1.00",
            "-1.00",
            "0.18",
            "1.00",
            "1",
        ],
    ]
    from io import StringIO

    stream = StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(_HEADERS)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


@pytest.fixture(autouse=True)
def synthetic_pin_manifest(tmp_path, monkeypatch):
    """Use a real synthetic pin file at the explicit loader dependency boundary."""
    monkeypatch.setattr(tv_trade_ledger, "_PORT_MANIFEST_PATH", tmp_path / "PORT_MANIFEST.sha256")


def _five_source_fixture(root: Path) -> tuple[Path, Path, list[str]]:
    source_dir = root / "sources"
    campaign_dir = root / "campaign"
    source_dir.mkdir()
    campaign_dir.mkdir()
    strategy_ids = _FROZEN_STRATEGY_IDS
    strategies = []
    for index, strategy_id in enumerate(strategy_ids):
        export_name = f"source_{index}.csv"
        pine_name = {
            "striker_dj30_mym_pyramid_250": "striker_dj30_v4.5_mym_pyramid_250.pine",
            "striker_nas100_mnq_dow_wed_excluded": "striker_nas100_v1_mnq_dow_wed_excluded.pine",
        }.get(strategy_id, f"source_{index}.pine")
        export_bytes = _csv_bytes(index)
        pine_bytes = f"// fixture {index}\n".encode()
        (source_dir / export_name).write_bytes(export_bytes)
        (source_dir / pine_name).write_bytes(pine_bytes)
        research_variant = {
            "striker_dj30_mym_pyramid_250": (
                "pyramid 250% vs locked 750%",
                "core/strategies/PORT_MANIFEST.sha256:core/strategies/candidates/"
                "striker_dj30_v4.5_mym_pyramid_250.pine",
            ),
            "striker_nas100_mnq_dow_wed_excluded": (
                "day-of-week set {Mon,Tue,Thu,Fri} vs locked {Mon,Tue}",
                "core/strategies/PORT_MANIFEST.sha256:core/strategies/candidates/"
                "striker_nas100_v1_mnq_dow_wed_excluded.pine",
            ),
        }.get(strategy_id)
        pin_divergence = research_variant[0] if research_variant else None
        pin_ref = research_variant[1] if research_variant else None
        strategies.append(
            {
                "strategy_id": strategy_id,
                "intended_instrument": "MNQ",
                "encoded_instrument": "MNQ",
                "export_filename": export_name,
                "export_sha256": sha256(export_bytes).hexdigest(),
                "export_bytes": len(export_bytes),
                "pine_filename": pine_name,
                "pine_sha256": sha256(pine_bytes).hexdigest(),
                "pine_bytes": len(pine_bytes),
                "source_timezone": "America/New_York",
                "session_timezone": "America/New_York",
                "declared_bar_size_minutes": 15,
                "declared_session": "09:30-16:00 America/New_York",
                "direction_evidence": "long-only",
                "quantity_convention": "integer contracts",
                "continuous_symbol": True,
                "synchronized_intraday_path_available": False,
                "lineage_notes": ["synthetic fixture"],
                "pine_commission_per_side_usd": "0.91",
                "pine_slippage_ticks_per_side": "1",
                "pine_pyramiding_pct": "100",
                "pine_pin_status": (
                    "PINNED_RESEARCH_VARIANT"
                    if pin_divergence
                    else "NOT_IN_PORT_MANIFEST"
                ),
                "pin_ref": pin_ref,
                "pin_divergence": pin_divergence,
                "contract_cap": 80,
            }
        )
    config = campaign_dir / "phase1_config.json"
    config.write_text(
        json.dumps(
            {
                "claim_class": "EXPLORATORY",
                "platform": "TradingView Strategy Tester over a continuous futures chart",
                "strategies": strategies,
                "continuous_contract_roll_policy": _unresolved_roll_policy(),
                "dropped_sources": [
                    {
                        "strategy_id_as_named_before": "striker_dj30_qtxg1_swap_body_on_mym",
                        "export_filename": "dropped_dj.csv",
                        "export_sha256": "a" * 64,
                        "pine_filename": "dropped_dj.pine",
                        "pine_sha256": "b" * 64,
                        "pin_ref": "core/strategies/PORT_MANIFEST.sha256:core/strategies/_archive/striker/dropped_dj.pine",
                        "reason": "SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN",
                    },
                    {
                        "strategy_id_as_named_before": "striker_nas100_qtxg1_swap_body_on_mnq",
                        "export_filename": "dropped_nas.csv",
                        "export_sha256": "c" * 64,
                        "pine_filename": "dropped_nas.pine",
                        "pine_sha256": "d" * 64,
                        "pin_ref": "core/strategies/PORT_MANIFEST.sha256:core/strategies/_archive/nas/dropped_nas.pine",
                        "reason": "SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    payload = json.loads(config.read_bytes())
    pinned = [row for row in payload["strategies"] if row["pin_ref"]] + payload["dropped_sources"]
    (root / "PORT_MANIFEST.sha256").write_text(
        "# Real synthetic manifest, no source files needed for dropped metadata\n" + "".join(
            f"{row['pine_sha256']}  {row['pin_ref'].split(':', 1)[1]}\n" for row in pinned
        ), encoding="utf-8",
    )
    (campaign_dir / "tradeify_commission_schedule.json").write_text(
        json.dumps(
            {
                "source_url": "https://help.tradeify.co/en/articles/10468315-trading-commission-fees",
                "page_date": "2026-04-28",
                "observed_date": "2026-09-02",
                "totals_include": "exchange, NFA, clearing, and commission",
                "rows": [
                    {"symbol": "6J", "round_trip_usd": "6.20"},
                    {"symbol": "MNQ", "round_trip_usd": "1.82"},
                    {"symbol": "MYM", "round_trip_usd": "1.82"},
                    {"symbol": "MGC", "round_trip_usd": "2.12"},
                ],
            }
        ),
        encoding="utf-8",
    )
    (campaign_dir / "cme_early_close_calendar.json").write_text(
        json.dumps(
            {
                "source_url": "https://www.cmegroup.com/trading-hours.html",
                "page_date": None,
                "observed_date": "2026-09-03",
                "coverage_start": "2022-09-01",
                "coverage_end": "2026-09-01",
                "coverage_status": "NEEDS_CONTEXT",
                "coverage_note": "synthetic incomplete calendar",
                "sources": [],
                "rows": [],
            }
        ),
        encoding="utf-8",
    )
    return source_dir, config, strategy_ids


# Keep the established fixture call sites readable while its active inventory is five.
_seven_source_fixture = _five_source_fixture


def test_campaign_writes_local_rows_but_aggregate_contains_no_absolute_path(tmp_path):
    source_dir, config, strategy_ids = _seven_source_fixture(tmp_path)
    output_dir = tmp_path / "local_artifacts"

    result = run_phase1.run_campaign(config, source_dir, output_dir)
    manifest_text = result.manifest_path.read_text(encoding="utf-8")
    manifest = json.loads(manifest_text)

    assert result.status == "BLOCKED_EXPLORATORY"
    assert (output_dir / "canonical_events.csv").exists()
    assert (output_dir / "canonical_trades.csv").exists()
    assert (output_dir / "weekly_exit_blocks.csv").exists()
    report_paths = sorted((output_dir / "strategy_reports").glob("*.json"))
    assert [path.stem for path in report_paths] == sorted(strategy_ids)
    detail = json.loads(report_paths[0].read_text(encoding="utf-8"))
    assert detail["strategy_id"] == report_paths[0].stem
    assert detail["claim_class"] == "EXPLORATORY"
    assert detail["source_identity"]["pine_pin_status"] == "NOT_IN_PORT_MANIFEST"
    assert detail["source_identity"]["pin_divergence"] is None
    assert detail["issues"]
    assert set(detail["issues"][0]) == {
        "code",
        "detail",
        "severity",
        "source_rows",
        "trade_id",
    }
    assert str(source_dir.resolve()) not in manifest_text
    assert "EXPLORATORY" in manifest_text
    assert manifest["phase1_verdict_cap"] == "NEEDS_CONTEXT"
    rendered = result.report_path.read_text(encoding="utf-8")
    assert "| Strategy | Status | Pine pin status |" in rendered
    assert "| aegis_6j1 | BLOCKED_EXPLORATORY | NOT_IN_PORT_MANIFEST |" in rendered
    assert "| striker_nas100_mnq_dow_wed_excluded | BLOCKED_EXPLORATORY | PINNED_RESEARCH_VARIANT |" in rendered
    assert manifest["ledgers"]["source_row_sha256"] == {
        "algorithm": "SHA-256",
        "input": "exact raw CSV record bytes including original record terminator when present",
    }
    assert manifest["git_base_commit"] == "ed181233afd01d8fc128bc76ac626e43c3761f87"
    assert [row["strategy_id"] for row in manifest["strategies"]] == strategy_ids
    modified_id = "striker_nas100_mnq_dow_wed_excluded"
    modified_divergence = "day-of-week set {Mon,Tue,Thu,Fri} vs locked {Mon,Tue}"
    modified_record = next(row for row in manifest["strategies"] if row["strategy_id"] == modified_id)
    assert modified_record["pine_pin_status"] == "PINNED_RESEARCH_VARIANT"
    assert modified_record["pin_divergence"] == modified_divergence
    assert modified_record["pin_ref"].endswith(
        "striker_nas100_v1_mnq_dow_wed_excluded.pine"
    )
    assert modified_record["source_identity"]["pine_pin_status"] == "PINNED_RESEARCH_VARIANT"
    assert modified_record["source_identity"]["pin_divergence"] == modified_divergence
    modified_detail = json.loads(
        (output_dir / "strategy_reports" / f"{modified_id}.json").read_text(encoding="utf-8")
    )
    assert modified_detail["source_identity"]["pine_pin_status"] == "PINNED_RESEARCH_VARIANT"
    assert modified_detail["source_identity"]["pin_divergence"] == modified_divergence
    assert set(manifest["local_strategy_report_sha256"]) == set(strategy_ids)
    assert manifest["local_strategy_report_sha256"] == {
        path.stem: sha256(path.read_bytes()).hexdigest() for path in report_paths
    }
    assert [
        source["strategy_id_as_named_before"] for source in manifest["dropped_sources"]
    ] == [
        "striker_dj30_qtxg1_swap_body_on_mym",
        "striker_nas100_qtxg1_swap_body_on_mnq",
    ]
    assert all(
        source["reason"] == "SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN"
        for source in manifest["dropped_sources"]
    )


def test_campaign_output_is_byte_deterministic(tmp_path):
    source_dir, config, _ = _seven_source_fixture(tmp_path)

    first = run_phase1.run_campaign(config, source_dir, tmp_path / "one")
    second = run_phase1.run_campaign(config, source_dir, tmp_path / "two")

    assert first.manifest_bytes == second.manifest_bytes
    assert first.report_bytes == second.report_bytes


def test_hash_failure_returns_intake_exit_code(tmp_path):
    source_dir, config, _ = _seven_source_fixture(tmp_path)
    (source_dir / "source_0.csv").write_text("changed", encoding="utf-8")

    assert run_phase1.main(
        ["--config", str(config), "--source-dir", str(source_dir)]
    ) == 3


def test_malformed_utf8_hash_pinned_export_returns_intake_exit_code(tmp_path, capsys):
    """A pinned invalid CSV must be reported as intake failure rather than a decode traceback."""
    source_dir, config, _ = _seven_source_fixture(tmp_path)
    export = source_dir / "source_0.csv"
    export.write_bytes(b"\xff")
    payload = json.loads(config.read_text(encoding="utf-8"))
    payload["strategies"][0]["export_sha256"] = sha256(export.read_bytes()).hexdigest()
    payload["strategies"][0]["export_bytes"] = len(export.read_bytes())
    config.write_text(json.dumps(payload), encoding="utf-8")

    assert run_phase1.main(
        ["--config", str(config), "--source-dir", str(source_dir)]
    ) == 3
    diagnostic = capsys.readouterr().err
    assert "intake failure:" in diagnostic
    assert "UTF-8" in diagnostic


def test_short_hash_pinned_export_returns_intake_exit_code(tmp_path, capsys):
    """A short logical CSV record is an intake/schema failure, not a runner traceback."""
    source_dir, config, _ = _five_source_fixture(tmp_path)
    export = source_dir / "source_0.csv"
    short_record = export.read_bytes().rsplit(b",", 1)[0]
    export.write_bytes(short_record)
    payload = json.loads(config.read_text(encoding="utf-8"))
    payload["strategies"][0]["export_sha256"] = sha256(short_record).hexdigest()
    payload["strategies"][0]["export_bytes"] = len(short_record)
    config.write_text(json.dumps(payload), encoding="utf-8")

    assert run_phase1.main(
        ["--config", str(config), "--source-dir", str(source_dir)]
    ) == 3
    assert "intake failure: source row 2 has 16 fields; expected 17" in capsys.readouterr().err


def test_header_only_exports_complete_without_key_error_and_write_zero_trade_ledger(tmp_path):
    """The runner must obtain each empty source's instrument from its spec, not row zero."""
    source_dir, config, strategy_ids = _seven_source_fixture(tmp_path)
    payload = json.loads(config.read_text(encoding="utf-8"))
    for index, strategy in enumerate(payload["strategies"]):
        export = source_dir / f"source_{index}.csv"
        export.write_bytes((",".join(_HEADERS) + "\n").encode("utf-8"))
        strategy["export_sha256"] = sha256(export.read_bytes()).hexdigest()
        strategy["export_bytes"] = len(export.read_bytes())
    config.write_text(json.dumps(payload), encoding="utf-8")

    result = run_phase1.run_campaign(config, source_dir, tmp_path / "local_artifacts")
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    trades = (tmp_path / "local_artifacts" / "canonical_trades.csv").read_text(encoding="utf-8")

    assert [row["trade_count"] for row in manifest["strategies"]] == [0] * 5
    assert all(row["strategy_id"] in strategy_ids for row in manifest["strategies"])
    assert trades.splitlines()[0].split(",")[10] == "duration_bars"
    events = (tmp_path / "local_artifacts" / "canonical_events.csv").read_text(encoding="utf-8")
    assert "source_row_sha256" in events.splitlines()[0]


def test_event_hashes_exact_raw_multiline_csv_records_with_original_terminators(tmp_path):
    """Record hashes bind the input bytes, rather than a reconstructed CSV representation."""
    source_dir, config, _ = _five_source_fixture(tmp_path)
    header = (",".join(_HEADERS) + "\r\n").encode("utf-8")
    entry = (
        b'1,Entry long,2026-01-01 10:00,"fixture\r\nline",100.00,1,100.00,0.18,'
        b'1.00,1.82,2.00,2.00,-1.00,-1.00,0.18,1.00,1\r\n'
    )
    exit = (
        b'1,Exit long,2026-01-01 10:15,fixture,101.00,1,100.00,0.18,1.00,'
        b'1.82,2.00,2.00,-1.00,-1.00,0.18,1.00,1'
    )
    payload = b"\xef\xbb\xbf" + header + entry + exit
    export = source_dir / "source_0.csv"
    export.write_bytes(payload)
    config_payload = json.loads(config.read_text(encoding="utf-8"))
    config_payload["strategies"][0]["export_sha256"] = sha256(payload).hexdigest()
    config_payload["strategies"][0]["export_bytes"] = len(payload)
    config.write_text(json.dumps(config_payload), encoding="utf-8")

    spec = run_phase1.load_source_specs(config)[0]
    events = run_phase1.normalize_export(run_phase1.verify_source_pair(source_dir, spec)).events

    assert events["source_row_number"].tolist() == [1, 2]
    assert events["source_row_sha256"].tolist() == [
        sha256(entry).hexdigest(),
        sha256(exit).hexdigest(),
    ]
    assert events["signal"].iloc[0] == "fixture\r\nline"


def test_campaign_publication_rolls_back_all_targets_after_late_replace_failure(tmp_path, monkeypatch):
    """A late publication failure must preserve every old artifact, not a mixed generation."""
    source_dir, config, strategy_ids = _seven_source_fixture(tmp_path)
    output_dir = tmp_path / "local_artifacts"
    targets = [
        output_dir / "canonical_events.csv",
        output_dir / "canonical_trades.csv",
        output_dir / "weekly_exit_blocks.csv",
        *(output_dir / "strategy_reports" / f"{strategy_id}.json" for strategy_id in strategy_ids),
        config.parent / "reconciliation_manifest.json",
        config.parent / "RESULTS.md",
    ]
    old_bytes = {target: f"old:{target.name}".encode("utf-8") for target in targets}
    for target, payload in old_bytes.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)

    real_replace = run_phase1.os.replace
    published = 0

    def fail_fourth_candidate_replace(source, destination):
        nonlocal published
        if str(source).endswith(".stage") and Path(destination) in old_bytes:
            published += 1
            if published == 4:
                raise OSError("late fixture publication failure")
        return real_replace(source, destination)

    monkeypatch.setattr(run_phase1.os, "replace", fail_fourth_candidate_replace)

    with pytest.raises(OSError, match="late fixture publication failure"):
        run_phase1.run_campaign(config, source_dir, output_dir)

    assert {target: target.read_bytes() for target in targets} == old_bytes
    assert not list(tmp_path.rglob(".*.phase1-*"))


def test_campaign_staging_replace_failure_cleans_inner_temp_and_preserves_old_targets(
    tmp_path, monkeypatch,
):
    """A failed stage finalization must not leak its inner temp or touch a target generation."""
    source_dir, config, strategy_ids = _seven_source_fixture(tmp_path)
    output_dir = tmp_path / "local_artifacts"
    targets = [
        output_dir / "canonical_events.csv",
        output_dir / "canonical_trades.csv",
        output_dir / "weekly_exit_blocks.csv",
        *(output_dir / "strategy_reports" / f"{strategy_id}.json" for strategy_id in strategy_ids),
        config.parent / "reconciliation_manifest.json",
        config.parent / "RESULTS.md",
    ]
    old_bytes = {target: f"old:{target.name}".encode("utf-8") for target in targets}
    for target, payload in old_bytes.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)

    real_replace = run_phase1.os.replace

    def fail_stage_finalization(source, destination):
        if str(source).endswith(".tmp") and str(destination).endswith(".stage"):
            raise OSError("fixture stage finalization failure")
        return real_replace(source, destination)

    monkeypatch.setattr(run_phase1.os, "replace", fail_stage_finalization)

    with pytest.raises(OSError, match="fixture stage finalization failure"):
        run_phase1.run_campaign(config, source_dir, output_dir)

    assert {target: target.read_bytes() for target in targets} == old_bytes
    assert not [
        path
        for path in tmp_path.rglob("*")
        if path.name.startswith(".")
        and (path.name.endswith(".tmp") or ".phase1-" in path.name)
    ]


def test_publication_restore_failure_preserves_backup_and_restores_other_targets(tmp_path, monkeypatch):
    """A rollback error must not erase the only recoverable old-generation bytes."""
    targets = [tmp_path / f"artifact_{index}.json" for index in range(3)]
    old_bytes = {target: f"old:{target.name}".encode() for target in targets}
    for target, payload in old_bytes.items():
        target.write_bytes(payload)
    publication_error = OSError("late publication failure")
    real_replace = run_phase1.os.replace

    def fail_publication_then_one_restore(source, destination):
        if str(source).endswith(".stage") and Path(destination) == targets[2]:
            raise publication_error
        if str(source).endswith(".backup") and Path(destination) == targets[0]:
            raise OSError("first restore is unavailable")
        return real_replace(source, destination)

    monkeypatch.setattr(run_phase1.os, "replace", fail_publication_then_one_restore)
    with pytest.raises(OSError) as caught:
        run_phase1._publish_payloads({target: b"new" for target in targets})

    backups = list(tmp_path.glob("*.backup"))
    assert len(backups) == 1
    assert backups[0].read_bytes() == old_bytes[targets[0]]
    assert all(target.read_bytes() == old_bytes[target] for target in targets[1:])
    assert str(backups[0]) in str(caught.value)
    assert "first restore is unavailable" in str(caught.value)
    assert "late publication failure" in str(caught.value)
    assert caught.value.__cause__ is publication_error
    assert not list(tmp_path.glob("*.stage"))


def test_publication_unlink_failure_does_not_abort_other_restorations(tmp_path, monkeypatch):
    """An undeletable newly published file must not strand unrelated old artifacts."""
    new_target = tmp_path / "new.json"
    old_targets = [tmp_path / "old_1.json", tmp_path / "old_2.json"]
    for target in old_targets:
        target.write_bytes(b"old")
    publication_error = OSError("late publication failure")
    real_replace = run_phase1.os.replace
    real_unlink = Path.unlink

    def fail_third_publication(source, destination):
        if str(source).endswith(".stage") and Path(destination) == old_targets[1]:
            raise publication_error
        return real_replace(source, destination)

    def fail_new_target_unlink(path, *args, **kwargs):
        if path == new_target:
            raise OSError("new target cannot be unlinked")
        return real_unlink(path, *args, **kwargs)

    monkeypatch.setattr(run_phase1.os, "replace", fail_third_publication)
    monkeypatch.setattr(Path, "unlink", fail_new_target_unlink)
    with pytest.raises(OSError) as caught:
        run_phase1._publish_payloads({new_target: b"new", **{target: b"new" for target in old_targets}})

    assert all(target.exists() and target.read_bytes() == b"old" for target in old_targets)
    assert new_target.read_bytes() == b"new"
    assert str(new_target) in str(caught.value)
    assert "new target cannot be unlinked" in str(caught.value)
    assert "late publication failure" in str(caught.value)
    assert caught.value.__cause__ is publication_error
    assert not list(tmp_path.glob("*.backup"))
    assert not list(tmp_path.glob("*.stage"))


def test_campaign_rejects_non_frozen_strategy_roster_before_source_reads(tmp_path):
    source_dir, config, _ = _seven_source_fixture(tmp_path)
    payload = json.loads(config.read_text(encoding="utf-8"))
    payload["strategies"].pop()
    config.write_text(json.dumps(payload), encoding="utf-8")
    for source in source_dir.iterdir():
        source.unlink()

    with pytest.raises(ValueError, match="frozen strategy roster mismatch"):
        run_phase1.run_campaign(config, source_dir, tmp_path / "local_artifacts")


def test_campaign_rejects_repo_output_outside_campaign_local_artifacts(tmp_path):
    source_dir, config, _ = _seven_source_fixture(tmp_path)
    unsafe = _CAMPAIGN_DIR / "unsafe_phase1_rows"

    with pytest.raises(ValueError, match="output directory inside the repository"):
        run_phase1.run_campaign(config, source_dir, unsafe)

    assert not unsafe.exists()


def test_alternate_in_repo_config_cannot_authorize_an_output_directory(tmp_path):
    source_dir, _, _ = _seven_source_fixture(tmp_path)
    alternate_campaign = _CAMPAIGN_DIR.parent / "alternate_phase1_campaign_fixture"

    with pytest.raises(ValueError, match="output directory inside the repository"):
        run_phase1.run_campaign(
            alternate_campaign / "phase1_config.json",
            source_dir,
            alternate_campaign / "local_artifacts",
        )

    assert not alternate_campaign.exists()


def test_complete_calendar_must_cover_observed_source_span(tmp_path):
    from test_cme_calendar_evidence import calendar_fixture
    source_dir, config, _ = _seven_source_fixture(tmp_path)
    calendar_path = config.parent / "cme_early_close_calendar.json"
    _, calendar, _ = calendar_fixture(config.parent)
    calendar.update(
        {
            "coverage_start": "2025-01-01",
            "coverage_end": "2025-12-31",
            "coverage_status": "COMPLETE",
            "coverage_note": "synthetic complete but out-of-span calendar",
        }
    )
    calendar["sources"] = calendar["sources"][:1]
    calendar["rows"] = calendar["rows"][:1]
    calendar_path.write_text(json.dumps(calendar), encoding="utf-8")

    with pytest.raises(ValueError, match="does not cover observed source span"):
        run_phase1.run_campaign(config, source_dir, tmp_path / "local_artifacts")


def test_campaign_report_renders_d19_secondary_calendar_residual_note(tmp_path):
    """D19 completion must retain the secondary venue-date residual rather than hide it."""
    expected_coverage_note = (
        "D19 accepts this SECONDARY venue-date membership evidence only over the declared 2022-09-01 "
        "through 2026-09-02 window, not product close-time or exchange-session modeling. The "
        "2025-11-28 scheduled-half-day/outage classification "
        "is conservatively included; possible ad-hoc closures from 2026-05-28 through 2026-09-02 "
        "may be missing and are not conservative. The preserved secondary metadata retains 13 "
        "unresolved items and 3 sub-deadline close notes."
    )
    checked_in_calendar = json.loads(
        (_CAMPAIGN_DIR / "cme_early_close_calendar.json").read_text(encoding="utf-8")
    )
    assert checked_in_calendar["coverage_note"] == expected_coverage_note

    source_dir, config, _ = _seven_source_fixture(tmp_path)
    calendar_path = config.parent / "cme_early_close_calendar.json"
    calendar = json.loads(calendar_path.read_text(encoding="utf-8"))
    calendar["coverage_note"] = checked_in_calendar["coverage_note"]
    calendar_path.write_text(json.dumps(calendar), encoding="utf-8")

    result = run_phase1.run_campaign(config, source_dir, tmp_path / "local_artifacts")
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))

    assert manifest["cme_early_close_coverage_note"] == expected_coverage_note
    assert expected_coverage_note in result.report_path.read_text(encoding="utf-8")


def test_invalid_invocation_returns_two():
    assert run_phase1.main([]) == 2


@pytest.mark.parametrize("kind", ["export", "pine"])
def test_correct_hash_wrong_source_byte_length_returns_intake_three(tmp_path, capsys, kind):
    source_dir, config, _ = _five_source_fixture(tmp_path)
    payload = json.loads(config.read_bytes())
    source = payload["strategies"][0]
    assert sha256((source_dir / source[f"{kind}_filename"]).read_bytes()).hexdigest() == source[f"{kind}_sha256"]
    source[f"{kind}_bytes"] += 1
    config.write_text(json.dumps(payload), encoding="utf-8")
    assert run_phase1.main(["--config", str(config), "--source-dir", str(source_dir)]) == 3
    diagnostic = capsys.readouterr().err
    assert "byte length mismatch: expected" in diagnostic
    assert source[f"{kind}_filename"] in diagnostic


def test_output_failure_returns_four(tmp_path, monkeypatch):
    source_dir, config, _ = _seven_source_fixture(tmp_path)

    def fail_write(path, payload):
        raise OSError("fixture write failure")

    monkeypatch.setattr(run_phase1, "_atomic_write_bytes", fail_write)
    assert run_phase1.main(
        ["--config", str(config), "--source-dir", str(source_dir)]
    ) == 4


def test_direct_script_entrypoint_bootstraps_repo_imports(tmp_path):
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [
            sys.executable,
            str(_RUNNER_PATH),
            "--help",
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "--source-dir" in result.stdout


def test_report_publishes_every_input_ledger_and_detail_digest(tmp_path):
    """Omitting a frozen evidence or detail digest must be visible to report consumers."""
    source_dir, config, _ = _five_source_fixture(tmp_path)
    result = run_phase1.run_campaign(config, source_dir, tmp_path / "rows")
    manifest = json.loads(result.manifest_bytes)
    rendered = result.report_bytes.decode("utf-8")

    for digest in manifest["inputs"].values():
        assert f"`{digest}`" in rendered
    for name, digest in manifest["ledgers"].items():
        if name.endswith("_sha256") and isinstance(digest, str):
            assert f"`{digest}`" in rendered
    for strategy_id, digest in manifest["local_strategy_report_sha256"].items():
        assert f"- Detail report {strategy_id}: `{digest}`" in rendered


def test_report_omits_nonindependent_monthly_map_from_tracked_output(tmp_path):
    """A published monthly map would expose non-independent reconciliation data as an anchor."""
    source_dir, config, _ = _five_source_fixture(tmp_path)
    result = run_phase1.run_campaign(config, source_dir, tmp_path / "rows")
    manifest = json.loads(result.manifest_bytes)

    assert result.report_bytes == run_phase1._render_report(manifest)
    assert b"monthly_net_pnl" not in result.report_bytes
    assert b"Decimal(" not in result.report_bytes


def test_committed_manifest_matches_frozen_five_strategy_acceptance():
    manifest = json.loads(
        (_CAMPAIGN_DIR / "reconciliation_manifest.json").read_text(encoding="utf-8")
    )
    expected = {
        "aegis_6j1": (242, 121, "27996.05"),
        "orb_mnq_recon_v7": (1362, 681, "48118.16"),
        "striker_dj30_mym_pyramid_250": (406, 203, "32057.36"),
        "striker_nas100_mnq_dow_wed_excluded": (756, 378, "112253.42"),
        "vanguard_mgc_v04": (676, 338, "18709.48"),
    }
    observed = {
        row["strategy_id"]: (
            row["source_row_count"],
            row["trade_count"],
            row["net_pnl_usd"],
        )
        for row in manifest["strategies"]
    }

    assert observed == expected
    from test_tradeify_phase1_identity_policy import accepted_policy
    assert manifest["runner_version"] == "tradeify-phase1-normalization-v3"
    assert manifest["continuous_contract_roll_policy"] == accepted_policy()
    for row in manifest["strategies"]:
        assert row["continuous_contract_roll_policy"] == accepted_policy()
        roll = next(issue for issue in row["issues"] if issue["code"] == "CONTINUOUS_CONTRACT_ROLL_UNRESOLVED")
        assert roll["severity"] == "WARNING"
    assert manifest["campaign_status"] == "RECONCILED_EXPLORATORY"
    assert manifest["phase1_verdict_cap"] == "NEEDS_CONTEXT"
    assert manifest["inputs"] == {
        "config_sha256": "df238cd78fc0a381fdb86466ef3dfca5522dd8db7ae0cf245165f370df9f3892",
        "tradeify_commission_schedule_sha256": "61c8957a4adfabf6b8e8c4eb984e6d9388a223145f90b0b9ca66b3dd7ca28750",
        "cme_early_close_calendar_sha256": "6eeb3b9d198eabf0a5a2115c4648f69629720a500616f38e219dff7bc57d0334",
        "tv_summary_anchors_sha256": "481e9bb2227578497dbc506d336377a5d51c366161dae6dd7d534c9c2ef88979",
    }
    for input_name, filename in {
        "config": "phase1_config.json",
        "tradeify_commission_schedule": "tradeify_commission_schedule.json",
        "cme_early_close_calendar": "cme_early_close_calendar.json",
        "tv_summary_anchors": "tv_summary_anchors.json",
    }.items():
        assert sha256((_CAMPAIGN_DIR / filename).read_bytes()).hexdigest() == (
            manifest["inputs"][f"{input_name}_sha256"]
        )
    assert manifest["ledgers"] == {
        "canonical_events_sha256": (
            "3a6b754ec145db0e5c09ce18413d7d42d60fa1ce8ac034bd6d6878ae4251d3ac"
        ),
        "canonical_trades_sha256": (
            "7e650599241b8150d0ee31ea04a7406c200e1f009c9530908a9644e56bed765a"
        ),
        "source_row_sha256": {
            "algorithm": "SHA-256",
            "input": "exact raw CSV record bytes including original record terminator when present",
        },
        "timestamp_domain": "UTC",
        "weekly_exit_blocks_sha256": (
            "d0b3e5ab840ef0a88c9f7b4b2c7254b3774142b85a55a9cfaeaa04fa5fe7934a"
        ),
    }
    assert manifest["local_strategy_report_sha256"] == {
        "aegis_6j1": "546cf0e0b1b9fe3d26793f0dc87ea53cb7990decd744bb5ec261110b32c964bc",
        "orb_mnq_recon_v7": "a0ea8a6b27aba3aa6f292322d82c3e38029e1c89cb8bbefbcb329305fcff81ea",
        "striker_dj30_mym_pyramid_250": "c7bbab4867e381428da31116c61ea4cb224d8b2b848cf328ce105443988871e3",
        "striker_nas100_mnq_dow_wed_excluded": "4d2807e40f946f708e270ad66be01451ca0a05d6c05099ac811663532615b5d4",
        "vanguard_mgc_v04": "a0a9564b1f598f04e68a1a6d56cf2e49d4ef25c7e3b67305a4ddfd2ca142e4d1",
    }
    assert manifest["local_monthly_reconciliation_sha256"] == {
        "aegis_6j1": "5242591bbb40a93480e5356011f31a4d6fd0575d1d0f1f73ee1236926c343ca1",
        "orb_mnq_recon_v7": "632382c8bffea9644486b961e706d5f94a7f782235ecc4b7d5b9bab29070e2ad",
        "striker_dj30_mym_pyramid_250": "bd34b13a72d6c771cdbb654d3798bb53307f60ac144e1553141efe5df4303070",
        "striker_nas100_mnq_dow_wed_excluded": "7163605aeddd8953d73e44b46162ec051d4d45587c508701079acbd4a6e7568a",
        "vanguard_mgc_v04": "5b1f2a5872aac49ef4988b423bc3d042232c16f5056c1816bddc4eeebde56acb",
    }
    assert sha256((_CAMPAIGN_DIR / "reconciliation_manifest.json").read_bytes()).hexdigest() == (
        "90281c7a28ddb28a7be84985b61a0fdd5c399f1bd8d3106d10490266585d209e"
    )
    assert sha256((_CAMPAIGN_DIR / "RESULTS.md").read_bytes()).hexdigest() == (
        "7918ebeb80fdc6a9182d61ad1b71f2f168aadf85c82e34c3aeb682f3a768b084"
    )
    assert [source["strategy_id_as_named_before"] for source in manifest["dropped_sources"]] == [
        "striker_dj30_qtxg1_swap_body_on_mym",
        "striker_nas100_qtxg1_swap_body_on_mnq",
    ]
    config = json.loads((_CAMPAIGN_DIR / "phase1_config.json").read_bytes())
    assert manifest["dropped_sources"] == config["dropped_sources"]
    rows = {row["strategy_id"]: row for row in manifest["strategies"]}
    assert all(row["friday_to_sunday_holds"] == 0 for row in rows.values())
    assert all(row["issue_counts"].get("FORCE_FLAT_VIOLATION", 0) == 0 for row in rows.values())
    assert {
        strategy_id: (
            row["peak_open_micro_equivalent_quantity_min"],
            row["peak_open_micro_equivalent_quantity_max"],
        )
        for strategy_id, row in rows.items()
    } == {
        "aegis_6j1": (80, 80),
        "orb_mnq_recon_v7": (4, 6),
        "striker_dj30_mym_pyramid_250": (77, 77),
        "striker_nas100_mnq_dow_wed_excluded": (77, 77),
        "vanguard_mgc_v04": (6, 6),
    }
    assert {
        strategy_id: row["monthly_reconciliation"]["bucket_count"]
        for strategy_id, row in rows.items()
    } == {
        "aegis_6j1": 45,
        "orb_mnq_recon_v7": 49,
        "striker_dj30_mym_pyramid_250": 48,
        "striker_nas100_mnq_dow_wed_excluded": 49,
        "vanguard_mgc_v04": 48,
    }
    aegis_pine = {
        issue["code"]: issue["severity"]
        for issue in rows["aegis_6j1"]["issues"]
        if issue["code"].startswith("PINE_")
        and issue["code"].endswith("_COMMISSION_MISMATCH")
    }
    assert aegis_pine == {
        "PINE_EXPORT_COMMISSION_MISMATCH": "WARNING",
        "PINE_VENUE_COMMISSION_MISMATCH": "WARNING",
    }
    assert all(
        row["issue_counts"].get("CONTRACT_CAP_BREACH", 0) == 0
        for row in rows.values()
    )
    assert all(
        row["contract_month_attribution_status"] == "UNAVAILABLE"
        for row in rows.values()
    )


def test_committed_results_match_the_deterministic_renderer():
    manifest = json.loads(
        (_CAMPAIGN_DIR / "reconciliation_manifest.json").read_text(encoding="utf-8")
    )

    assert (_CAMPAIGN_DIR / "RESULTS.md").read_bytes() == run_phase1._render_report(
        manifest
    )
