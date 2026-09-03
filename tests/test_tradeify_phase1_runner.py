"""Synthetic end-to-end tests for the seven-strategy Phase 1 runner."""

import csv
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


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
    "striker_dj30_qtxg1_swap_body_on_mym",
    "striker_dj30_native_pyramid_down_on_mym",
    "striker_nas100_native_dow_modified_on_mnq",
    "striker_nas100_qtxg1_swap_body_on_mnq",
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


def _seven_source_fixture(root: Path) -> tuple[Path, Path, list[str]]:
    source_dir = root / "sources"
    campaign_dir = root / "campaign"
    source_dir.mkdir()
    campaign_dir.mkdir()
    strategy_ids = _FROZEN_STRATEGY_IDS
    strategies = []
    for index, strategy_id in enumerate(strategy_ids):
        export_name = f"source_{index}.csv"
        pine_name = f"source_{index}.pine"
        export_bytes = _csv_bytes(index)
        pine_bytes = f"// fixture {index}\n".encode()
        (source_dir / export_name).write_bytes(export_bytes)
        (source_dir / pine_name).write_bytes(pine_bytes)
        strategies.append(
            {
                "strategy_id": strategy_id,
                "intended_instrument": "MNQ",
                "encoded_instrument": "MNQ",
                "export_filename": export_name,
                "export_sha256": sha256(export_bytes).hexdigest(),
                "pine_filename": pine_name,
                "pine_sha256": sha256(pine_bytes).hexdigest(),
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
                "pine_pin_status": "NOT_IN_PORT_MANIFEST",
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
            }
        ),
        encoding="utf-8",
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
                "rows": [],
            }
        ),
        encoding="utf-8",
    )
    return source_dir, config, strategy_ids


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
    detailed = json.loads(report_paths[0].read_text(encoding="utf-8"))
    assert detailed["strategy_id"] == report_paths[0].stem
    assert detailed["claim_class"] == "EXPLORATORY"
    assert detailed["source_identity"]["pine_pin_status"] == "NOT_IN_PORT_MANIFEST"
    assert detailed["issues"]
    assert set(detailed["issues"][0]) == {
        "code",
        "detail",
        "severity",
        "source_rows",
        "trade_id",
    }
    assert str(source_dir.resolve()) not in manifest_text
    assert "EXPLORATORY" in manifest_text
    assert manifest["phase1_verdict_cap"] == "NEEDS_CONTEXT"
    assert manifest["git_base_commit"] == "ed181233afd01d8fc128bc76ac626e43c3761f87"
    assert [row["strategy_id"] for row in manifest["strategies"]] == strategy_ids
    assert all(row["pine_pin_status"] == "NOT_IN_PORT_MANIFEST" for row in manifest["strategies"])
    assert all(
        row["source_identity"]["pine_pin_status"] == "NOT_IN_PORT_MANIFEST"
        for row in manifest["strategies"]
    )
    assert set(manifest["local_strategy_report_sha256"]) == set(strategy_ids)
    assert manifest["local_strategy_report_sha256"] == {
        path.stem: sha256(path.read_bytes()).hexdigest() for path in report_paths
    }


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
    config.write_text(json.dumps(payload), encoding="utf-8")

    assert run_phase1.main(
        ["--config", str(config), "--source-dir", str(source_dir)]
    ) == 3
    assert "intake failure:" in capsys.readouterr().err


def test_header_only_exports_complete_without_key_error_and_write_zero_trade_ledger(tmp_path):
    """The runner must obtain each empty source's instrument from its spec, not row zero."""
    source_dir, config, strategy_ids = _seven_source_fixture(tmp_path)
    payload = json.loads(config.read_text(encoding="utf-8"))
    for index, strategy in enumerate(payload["strategies"]):
        export = source_dir / f"source_{index}.csv"
        export.write_bytes((",".join(_HEADERS) + "\n").encode("utf-8"))
        strategy["export_sha256"] = sha256(export.read_bytes()).hexdigest()
    config.write_text(json.dumps(payload), encoding="utf-8")

    result = run_phase1.run_campaign(config, source_dir, tmp_path / "local_artifacts")
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    trades = (tmp_path / "local_artifacts" / "canonical_trades.csv").read_text(encoding="utf-8")

    assert [row["trade_count"] for row in manifest["strategies"]] == [0] * 7
    assert all(row["strategy_id"] in strategy_ids for row in manifest["strategies"])
    assert trades.splitlines()[0].split(",")[10] == "duration_bars"


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
    source_dir, config, _ = _seven_source_fixture(tmp_path)
    calendar_path = config.parent / "cme_early_close_calendar.json"
    calendar = json.loads(calendar_path.read_text(encoding="utf-8"))
    calendar.update(
        {
            "coverage_start": "2025-01-01",
            "coverage_end": "2025-12-31",
            "coverage_status": "COMPLETE",
            "coverage_note": "synthetic complete but out-of-span calendar",
        }
    )
    calendar_path.write_text(json.dumps(calendar), encoding="utf-8")

    with pytest.raises(ValueError, match="does not cover observed source span"):
        run_phase1.run_campaign(config, source_dir, tmp_path / "local_artifacts")


def test_invalid_invocation_returns_two():
    assert run_phase1.main([]) == 2


def test_output_failure_returns_four(tmp_path, monkeypatch):
    source_dir, config, _ = _seven_source_fixture(tmp_path)

    def fail_write(path, payload):
        raise OSError("fixture write failure")

    monkeypatch.setattr(run_phase1, "_atomic_write_bytes", fail_write)
    assert run_phase1.main(
        ["--config", str(config), "--source-dir", str(source_dir)]
    ) == 4


def test_direct_script_entrypoint_bootstraps_repo_imports(tmp_path):
    source_dir, config, _ = _seven_source_fixture(tmp_path)
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [
            sys.executable,
            str(_RUNNER_PATH),
            "--config",
            str(config),
            "--source-dir",
            str(source_dir),
            "--output-dir",
            str(tmp_path / "rows"),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_committed_manifest_matches_frozen_seven_strategy_acceptance():
    manifest = json.loads(
        (_CAMPAIGN_DIR / "reconciliation_manifest.json").read_text(encoding="utf-8")
    )
    expected = {
        "aegis_6j1": (244, 122, "28702.75"),
        "orb_mnq_recon_v7": (1362, 681, "47533.16"),
        "striker_dj30_mym_v45": (406, 203, "10208.62"),
        "striker_dj30_mym_pyramid_down": (406, 203, "31770.36"),
        "striker_nas100_mnq_v1": (756, 378, "112253.42"),
        "striker_nas100_mnq_native_variant": (368, 184, "170250.58"),
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
    assert manifest["campaign_status"] == "BLOCKED_EXPLORATORY"
    assert manifest["phase1_verdict_cap"] == "NEEDS_CONTEXT"
    assert manifest["inputs"]["config_sha256"] == (
        "8881a2af5ab63cb7abec7028d22832ed647cfef10d484eba7d97515fcb0ea227"
    )
    assert manifest["ledgers"] == {
        "canonical_events_sha256": (
            "03efac85c4cf67ef9a577ec0844383015eed5d85a5b3239ec47a2c38643d84bf"
        ),
        "canonical_trades_sha256": (
            "900002b84762299273cdfe0dad75e5ab06324b884a22ef1f81e28fa8e3145105"
        ),
        "timestamp_domain": "UTC",
        "weekly_exit_blocks_sha256": (
            "5bdcef07a717bf32b816c595cfbf6066e1f94a7ca9ad35e31b749bc8bc72cb0a"
        ),
    }
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
