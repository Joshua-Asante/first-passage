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


def test_campaign_report_renders_accepted_cme_early_close_fallback_note(tmp_path):
    """A generic NEEDS_CONTEXT label must not hide the accepted early-close risk."""
    expected_coverage_note = (
        "If the primary-source 2022–2026 CME early-close dates cannot be captured, "
        "report a NEEDS_CONTEXT cap, never a silent omission; an early-close hold may "
        "go undetected."
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


def test_report_missing_monthly_anchor_roundtrips_with_plain_decimal_display(tmp_path):
    """An in-memory Decimal map and its published JSON must render identical evidence."""
    source_dir, config, _ = _five_source_fixture(tmp_path)
    result = run_phase1.run_campaign(config, source_dir, tmp_path / "rows")
    manifest = json.loads(result.manifest_bytes)

    assert result.report_bytes == run_phase1._render_report(manifest)
    assert (
        b"| monthly_net_pnl_usd | {'2026-01': '0.18'} | None | None | 0.01 | MISSING_ANCHOR |"
        in result.report_bytes
    )
    assert b"Decimal(" not in result.report_bytes


def test_committed_manifest_matches_frozen_five_strategy_acceptance():
    manifest = json.loads(
        (_CAMPAIGN_DIR / "reconciliation_manifest.json").read_text(encoding="utf-8")
    )
    expected = {
        "aegis_6j1": (244, 122, "28702.75"),
        "orb_mnq_recon_v7": (1362, 681, "47533.16"),
        "striker_dj30_mym_pyramid_250": (406, 203, "31770.36"),
        "striker_nas100_mnq_dow_wed_excluded": (756, 378, "112253.42"),
        "vanguard_mgc_v04": (686, 343, "20388.04"),
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
    assert manifest["runner_version"] == "tradeify-phase1-normalization-v2"
    assert manifest["continuous_contract_roll_policy"] == accepted_policy()
    for row in manifest["strategies"]:
        assert row["continuous_contract_roll_policy"] == accepted_policy()
        roll = next(issue for issue in row["issues"] if issue["code"] == "CONTINUOUS_CONTRACT_ROLL_UNRESOLVED")
        assert roll["severity"] == "WARNING"
    assert manifest["campaign_status"] == "BLOCKED_EXPLORATORY"
    assert manifest["phase1_verdict_cap"] == "NEEDS_CONTEXT"
    assert manifest["inputs"] == {
        "config_sha256": "bc806ace41f899f17fa9cd54960bcd7c6ee6f3b02b28f8574c5b600997667e87",
        "tradeify_commission_schedule_sha256": "61c8957a4adfabf6b8e8c4eb984e6d9388a223145f90b0b9ca66b3dd7ca28750",
        "cme_early_close_calendar_sha256": "742e83508a3addf034ce6536e42553522bea28c96f8e3718629cf5495c405277",
        "tv_summary_anchors_sha256": "a3c3ae0c102adf15199a2f68cebe07a97c4cae1b0b5b4f7c07f73c1093c96ff2",
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
            "c04e2cc8b07a21abb47b70f6c195ea0336ec76087c0e76fb26f37e64f2c945ee"
        ),
        "canonical_trades_sha256": (
            "0336cf3836055fbc951c995725c718e15aaff03e064bfade5f8310a5c382e257"
        ),
        "source_row_sha256": {
            "algorithm": "SHA-256",
            "input": "exact raw CSV record bytes including original record terminator when present",
        },
        "timestamp_domain": "UTC",
        "weekly_exit_blocks_sha256": (
            "e33f48c13c3fd4c6438bb755fb6ac070bebbbf308ad0377320468a1a6ef8850e"
        ),
    }
    assert manifest["local_strategy_report_sha256"] == {
        "aegis_6j1": "9b40524e9c06870161ed77fde5cb1cea4a2501d7696cc6899607a2ab0e25b7c5",
        "orb_mnq_recon_v7": "3cdf75dfc2821279f90dbafc0ac100ad227deefe9ab96360db157f880df7b8af",
        "striker_dj30_mym_pyramid_250": "a762cc3b255f879ee3b92c77d6dc27a3de9d443a8c8219b94797e4833eff904e",
        "striker_nas100_mnq_dow_wed_excluded": "c5c3d8f431b4ecdda6943e562ee9f152a924132d9f2d82e286c0293933187a8a",
        "vanguard_mgc_v04": "ab61978d7dc7c6f1428c7d945d6258e0bcab5c5fdd276a84a1cea05bfba73af7",
    }
    assert sha256((_CAMPAIGN_DIR / "reconciliation_manifest.json").read_bytes()).hexdigest() == (
        "89a0d42e97b38ddd12fca29a151e17d26e6395a7d85502482c125303b7cd479c"
    )
    assert sha256((_CAMPAIGN_DIR / "RESULTS.md").read_bytes()).hexdigest() == (
        "ab69e3a70b461356edfe4218bef6177ae919730c72cab59cb0e8e27310e5b8cc"
    )
    assert [source["strategy_id_as_named_before"] for source in manifest["dropped_sources"]] == [
        "striker_dj30_qtxg1_swap_body_on_mym",
        "striker_nas100_qtxg1_swap_body_on_mnq",
    ]
    config = json.loads((_CAMPAIGN_DIR / "phase1_config.json").read_bytes())
    assert manifest["dropped_sources"] == config["dropped_sources"]
    rows = {row["strategy_id"]: row for row in manifest["strategies"]}
    assert rows["orb_mnq_recon_v7"]["friday_to_sunday_holds"] == 3
    assert rows["orb_mnq_recon_v7"]["issue_counts"]["FORCE_FLAT_VIOLATION"] == 310
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
