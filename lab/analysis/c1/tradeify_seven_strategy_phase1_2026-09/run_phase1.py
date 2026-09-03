"""Run strict, exploratory Phase 1 normalization for the seven frozen exports."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import date, datetime
from decimal import Decimal
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
from typing import NamedTuple, Sequence

import pandas as pd


_REPO = Path(__file__).resolve().parents[4]
_LAB = _REPO / "lab"
_CORE = _REPO / "core"
for _import_root in (_REPO, _LAB, _CORE):
    if str(_import_root) not in sys.path:
        sys.path.insert(0, str(_import_root))

from research_utils.joint_trade_blocks import (  # noqa: E402
    build_joint_events,
    build_weekly_exit_blocks,
)
from research_utils.trade_reconciliation import (  # noqa: E402
    analyze_venue,
    calculate_accounting,
    load_early_close_calendar,
    reconstruct_trades,
)
from research_utils.tv_trade_ledger import (  # noqa: E402
    SourceIdentityError,
    TradeExportSchemaError,
    load_fee_schedule,
    load_source_specs,
    normalize_export,
    sha256_file,
    verify_source_pair,
)


_RUNNER_VERSION = "tradeify-phase1-normalization-v1"
_SEVERITY_ORDER = {"INFO": 0, "WARNING": 1, "BLOCKER": 2, "FATAL": 3}


class CampaignResult(NamedTuple):
    status: str
    manifest_path: Path
    report_path: Path
    manifest_bytes: bytes
    report_bytes: bytes


def _atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("wb") as handle:
        handle.write(payload)
        handle.flush()
    temporary.replace(path)


def _csv_bytes(frame: pd.DataFrame) -> bytes:
    stream = StringIO(newline="")
    frame.to_csv(
        stream,
        index=False,
        lineterminator="\n",
        na_rep="",
        quoting=csv.QUOTE_MINIMAL,
    )
    return stream.getvalue().encode("utf-8")


def _json_default(value: object) -> object:
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, tuple):
        return list(value)
    raise TypeError(f"cannot serialize {type(value).__name__}")


def _json_bytes(payload: object) -> bytes:
    return (
        json.dumps(
            payload,
            default=_json_default,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")


def _digest(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def _git_ref(ref: str) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", ref],
            cwd=_REPO,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"
    return result.stdout.strip()


def _issue_summary(issues: Sequence[object]) -> tuple[dict[str, int], list[dict[str, object]]]:
    counts = Counter(issue.code for issue in issues)
    grouped = Counter((issue.severity, issue.code) for issue in issues)
    rows = [
        {"severity": severity, "code": code, "count": count}
        for (severity, code), count in sorted(
            grouped.items(),
            key=lambda item: (
                -_SEVERITY_ORDER[item[0][0]],
                item[0][1],
            ),
        )
    ]
    return dict(sorted(counts.items())), rows


def _strategy_record(
    spec: object,
    events: pd.DataFrame,
    trades: pd.DataFrame,
    accounting: object,
    venue: object,
    issues: Sequence[object],
) -> dict[str, object]:
    blocker = any(issue.severity in {"BLOCKER", "FATAL"} for issue in issues)
    issue_counts, issue_summary = _issue_summary(issues)
    return {
        "strategy_id": spec.strategy_id,
        "status": "BLOCKED_EXPLORATORY" if blocker else "RECONCILED_EXPLORATORY",
        "claim_class": "EXPLORATORY",
        "intended_instrument": spec.intended_instrument,
        "encoded_instrument": spec.encoded_instrument,
        "source_row_count": len(events),
        "trade_count": accounting.trade_count,
        "first_entry_timestamp": accounting.first_entry_timestamp,
        "last_exit_timestamp": accounting.last_exit_timestamp,
        "net_pnl_usd": accounting.net_pnl_usd,
        "commission_usd": accounting.commission_usd,
        "gross_pnl_usd": accounting.gross_pnl_usd,
        "wins": accounting.wins,
        "losses": accounting.losses,
        "flats": accounting.flats,
        "win_rate": accounting.win_rate,
        "profit_factor": accounting.profit_factor,
        "max_drawdown_usd": accounting.max_drawdown_usd,
        "monthly_net_pnl": dict(accounting.monthly_net_pnl),
        "final_source_cumulative_pnl_usd": accounting.final_source_cumulative_pnl_usd,
        "pine_pyramiding_pct": spec.pine_pyramiding_pct,
        "micro_equivalent_multiplier": venue.micro_equivalent_multiplier,
        "peak_open_micro_equivalent_quantity_min": (
            venue.peak_open_micro_equivalent_quantity_min
        ),
        "peak_open_micro_equivalent_quantity_max": (
            venue.peak_open_micro_equivalent_quantity_max
        ),
        "micro_equivalent_contract_cap": venue.micro_equivalent_contract_cap,
        "cross_date_holds": venue.cross_date_holds,
        "overnight_holds": venue.overnight_holds,
        "friday_to_sunday_holds": venue.friday_to_sunday_holds,
        "holiday_short_deadline_status": venue.holiday_short_deadline_status,
        "venue_commission_per_side_usd": venue.venue_commission_per_side_usd,
        "pine_commission_per_side_usd": venue.pine_commission_per_side_usd,
        "export_implied_commission_per_side_usd": (
            venue.export_implied_commission_per_side_usd
        ),
        "contract_month_attribution_status": venue.contract_month_attribution_status,
        "roll_seam_attribution_status": venue.roll_seam_attribution_status,
        "bid_ask_spread_status": venue.bid_ask_spread_status,
        "issue_counts": issue_counts,
        "issues": issue_summary,
        "source_identity": {
            "export_filename": spec.export_filename,
            "export_sha256": spec.export_sha256,
            "pine_filename": spec.pine_filename,
            "pine_sha256": spec.pine_sha256,
        },
    }


def _render_report(manifest: dict[str, object]) -> bytes:
    lines = [
        "# Tradeify seven-strategy Phase 1 reconciliation",
        "",
        "**Theme:** c1",
        "",
        "**In-flight:** yes",
        "",
        "**Status:** ACTIVE — strict seven-strategy Tradeify source, accounting, deadline, cap, and provenance normalization",
        "",
        "> **EXPLORATORY — Phase 0 was skipped.** All supplied history is development data; this report is not confirmatory, qualified, admitted, or deployable.",
        "",
        f"Campaign status: `{manifest['campaign_status']}`",
        "",
        f"Holiday-short verdict cap: `{manifest['phase1_verdict_cap']}`",
        "",
        "## Strategy inventory",
        "",
        "| Strategy | Status | Rows | Trades | Net P&L | Daily-deadline holds | Fri→Sun sub-count |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in manifest["strategies"]:
        lines.append(
            "| {strategy_id} | {status} | {source_row_count} | {trade_count} | "
            "${net_pnl_usd} | {overnight_holds} | {friday_to_sunday_holds} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Evidence boundaries",
            "",
            "- The source CSV/Pine bytes and all row-level event/trade/weekly ledgers remain local and gitignored.",
            "- No source row was repaired, dropped for an outcome, re-ranked, composed, simulated, or rerun in Pine.",
            "- Scalar MAE/MFE values are inventory-only excursion bounds, not timestamped paths.",
            "- Per-strategy caps are measured against 80 micro-equivalents; the joint book-cap verdict is deferred to Phase 4.",
            "- CME holiday-short coverage is `NEEDS_CONTEXT`; no historical early-close date was inferred.",
            "",
            "## Frozen hashes",
            "",
            f"- Config: `{manifest['inputs']['config_sha256']}`",
            f"- CME calendar capture: `{manifest['inputs']['cme_early_close_calendar_sha256']}`",
            f"- Canonical events: `{manifest['ledgers']['canonical_events_sha256']}`",
            f"- Canonical trades: `{manifest['ledgers']['canonical_trades_sha256']}`",
            f"- Weekly exit blocks: `{manifest['ledgers']['weekly_exit_blocks_sha256']}`",
            "",
            "## Issues by strategy",
            "",
        ]
    )
    for row in manifest["strategies"]:
        lines.append(f"### {row['strategy_id']}")
        lines.append("")
        if row["issues"]:
            for issue in row["issues"]:
                lines.append(
                    f"- `{issue['severity']}` `{issue['code']}` × {issue['count']}"
                )
        else:
            lines.append("- No issues.")
        lines.append("")
    lines.extend(
        [
            "## Reproduce",
            "",
            "Provide the frozen source directory at runtime and run `python run_phase1.py --config phase1_config.json --source-dir <source-dir> --output-dir local_artifacts`.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def run_campaign(
    config_path: str | Path,
    source_dir: str | Path,
    output_dir: str | Path,
) -> CampaignResult:
    """Verify every source first, then normalize and publish deterministic outputs."""
    config_path = Path(config_path).resolve()
    source_dir = Path(source_dir).resolve()
    output_dir = Path(output_dir).resolve()
    campaign_dir = config_path.parent
    fee_path = campaign_dir / "tradeify_commission_schedule.json"
    calendar_path = campaign_dir / "cme_early_close_calendar.json"

    specs = load_source_specs(config_path)
    fee_schedule = load_fee_schedule(fee_path)
    early_close_calendar = load_early_close_calendar(calendar_path)
    verified = [verify_source_pair(source_dir, spec) for spec in specs]

    events_by_strategy: dict[str, pd.DataFrame] = {}
    trades_by_strategy: dict[str, pd.DataFrame] = {}
    strategy_records: list[dict[str, object]] = []
    for source in verified:
        normalized = normalize_export(source)
        reconstruction = reconstruct_trades(normalized.events, source.spec)
        accounting = calculate_accounting(reconstruction.trades)
        venue = analyze_venue(
            reconstruction.trades,
            source.spec,
            fee_schedule,
            early_close_calendar=early_close_calendar,
        )
        issues = (*normalized.issues, *reconstruction.issues, *accounting.issues, *venue.issues)
        events_by_strategy[source.spec.strategy_id] = normalized.events
        trades_by_strategy[source.spec.strategy_id] = reconstruction.trades
        strategy_records.append(
            _strategy_record(
                source.spec,
                normalized.events,
                reconstruction.trades,
                accounting,
                venue,
                issues,
            )
        )

    joint_events = build_joint_events(events_by_strategy)
    canonical_trades = pd.concat(
        [trades_by_strategy[spec.strategy_id] for spec in specs],
        ignore_index=True,
        sort=False,
    )
    weekly_blocks = build_weekly_exit_blocks(trades_by_strategy)
    event_bytes = _csv_bytes(joint_events)
    trade_bytes = _csv_bytes(canonical_trades)
    weekly_bytes = _csv_bytes(weekly_blocks)
    _atomic_write_bytes(output_dir / "canonical_events.csv", event_bytes)
    _atomic_write_bytes(output_dir / "canonical_trades.csv", trade_bytes)
    _atomic_write_bytes(output_dir / "weekly_exit_blocks.csv", weekly_bytes)

    campaign_status = (
        "BLOCKED_EXPLORATORY"
        if any(row["status"] == "BLOCKED_EXPLORATORY" for row in strategy_records)
        else "RECONCILED_EXPLORATORY"
    )
    manifest: dict[str, object] = {
        "claim_class": "EXPLORATORY",
        "phase0_status": "SKIPPED_BY_OPERATOR",
        "campaign_status": campaign_status,
        "phase1_verdict_cap": early_close_calendar.coverage_status,
        "runner_version": _RUNNER_VERSION,
        "git_base_commit": _git_ref("origin/main"),
        "inputs": {
            "config_sha256": sha256_file(config_path),
            "tradeify_commission_schedule_sha256": sha256_file(fee_path),
            "cme_early_close_calendar_sha256": sha256_file(calendar_path),
        },
        "ledgers": {
            "timestamp_domain": (
                joint_events["timestamp_domain"].iloc[0]
                if not joint_events.empty
                else "UTC"
            ),
            "canonical_events_sha256": _digest(event_bytes),
            "canonical_trades_sha256": _digest(trade_bytes),
            "weekly_exit_blocks_sha256": _digest(weekly_bytes),
        },
        "tolerances": {
            "aggregate_money_usd": "0.01",
            "tick_grid_ticks": "1e-9",
            "pairing_and_source_identity": "exact",
        },
        "strategies": strategy_records,
    }
    manifest_bytes = _json_bytes(manifest)
    report_bytes = _render_report(manifest)
    manifest_path = campaign_dir / "reconciliation_manifest.json"
    report_path = campaign_dir / "RESULTS.md"
    _atomic_write_bytes(manifest_path, manifest_bytes)
    _atomic_write_bytes(report_path, report_bytes)
    return CampaignResult(
        status=campaign_status,
        manifest_path=manifest_path,
        report_path=report_path,
        manifest_bytes=manifest_bytes,
        report_bytes=report_bytes,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output-dir")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    config = Path(args.config)
    output = Path(args.output_dir) if args.output_dir else config.parent / "local_artifacts"
    try:
        run_campaign(config, args.source_dir, output)
    except (SourceIdentityError, TradeExportSchemaError) as exc:
        print(f"intake failure: {exc}", file=sys.stderr)
        return 3
    except ValueError as exc:
        print(f"configuration failure: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"output failure: {exc}", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
