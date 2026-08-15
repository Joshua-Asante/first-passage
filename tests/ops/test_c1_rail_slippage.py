"""Tests for ops/c1_rail/c1_rail_slippage.py — B7 Stage 2b read-only fill capture.

Pure join + cohort-split + panel-baseline comparison. The CLI never appends
to the ledger (unlike the reconciler) — that property is tested explicitly.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import c1_rail_slippage as slip
from c1_rail_slippage import (
    MYM_ADD_EXCESS_TICK_THRESHOLD,
    PANEL_ADD_OFFSET_PTS,
    collect_fill_slippage,
    compute_fill_slippage,
    format_report,
    panel_add_basis,
    summarize_by_cohort,
)
from c1_rail_telemetry import (
    BrokerEvidence,
    EventLedger,
    append_broker_evidence,
    load_evidence_overlay,
    make_request_received,
)


def _write_triad(
    ledger: EventLedger,
    *,
    event_id: str,
    leg_id: str,
    signal_type: str,
    close: float,
    qty_out: int = 60,
    stop_dist_pts: float = 60.8201,
) -> None:
    parsed = {
        "leg_id": leg_id,
        "signal_type": signal_type,
        "bar_time": 1_785_000_000_000,
        "close": close,
        "stop_dist_pts": stop_dist_pts,
    }
    order_id = f"{leg_id}-{signal_type}-test"
    ledger.append(
        "request_received",
        make_request_received(
            event_id=event_id,
            auth_ok=True,
            body_category="b1_json",
            body_hash="abc",
            order_id=order_id,
            parsed_fields=parsed,
        ),
        event_id=event_id,
        order_id=order_id,
    )
    ledger.append(
        "decision",
        {
            "leg_id": leg_id,
            "signal_type": signal_type,
            "qty_out": qty_out,
            "submit": True,
            "halt": False,
        },
        event_id=event_id,
        order_id=order_id,
    )
    ledger.append(
        "transport_result",
        {
            "transport_state": "accepted",
            "http_status": 200,
            "dry_run": False,
            "execution_verified": False,
        },
        event_id=event_id,
        order_id=order_id,
    )


def _evidence(
    event_id: str,
    *,
    fill_price: float,
    fill_qty: int = 60,
    tradovate_order_id: str = "TV-1",
) -> BrokerEvidence:
    return BrokerEvidence(
        event_id=event_id,
        order_id=f"order-{event_id}",
        crosstrade_receive=True,
        crosstrade_validate=True,
        crosstrade_execute=True,
        tradovate_order_id=tradovate_order_id,
        tradovate_status="Filled",
        fill_qty=fill_qty,
        fill_price=fill_price,
        position_after=fill_qty,
        attested_utc="2026-07-28T14:00:00+00:00",
    )


# ── panel baselines are the RUNBOOK pins ───────────────────────────────────

def test_panel_baselines_match_runbook():
    assert PANEL_ADD_OFFSET_PTS["dj30_mym"] == 1.00
    assert PANEL_ADD_OFFSET_PTS["nas100_mnq"] == 0.50
    assert panel_add_basis("dj30_mym") == 1.00
    assert panel_add_basis("nas100_mnq") == 0.50
    assert panel_add_basis("unknown") is None


# ── pure compute ──────────────────────────────────────────────────────────

def test_mym_add_at_panel_basis_zero_excess():
    """Panel-exact fill: close+1.00 → excess 0."""
    records = [
        {
            "kind": "request_received",
            "parsed": {
                "leg_id": "dj30_mym",
                "signal_type": "add",
                "close": 44000.0,
            },
        }
    ]
    row = compute_fill_slippage(
        event_id="e1",
        records=records,
        evidence=_evidence("e1", fill_price=44001.0),
    )
    assert row.is_complete
    assert row.is_add
    assert row.delta_pts == pytest.approx(1.00)
    assert row.panel_basis_pts == 1.00
    assert row.excess_pts == pytest.approx(0.0)
    assert row.excess_ticks == pytest.approx(0.0)


def test_mym_add_one_extra_tick_flags_actionable_threshold():
    """close+2.00 = 1 tick excess — the declared MYM actionable signal."""
    records = [
        {
            "kind": "request_received",
            "parsed": {
                "leg_id": "dj30_mym",
                "signal_type": "add",
                "close": 44000.0,
            },
        }
    ]
    row = compute_fill_slippage(
        event_id="e2",
        records=records,
        evidence=_evidence("e2", fill_price=44002.0),
    )
    assert row.excess_pts == pytest.approx(1.00)
    assert row.excess_ticks == pytest.approx(MYM_ADD_EXCESS_TICK_THRESHOLD)


def test_mnq_add_panel_basis_is_two_ticks():
    records = [
        {
            "kind": "request_received",
            "parsed": {
                "leg_id": "nas100_mnq",
                "signal_type": "add",
                "close": 28000.0,
            },
        }
    ]
    row = compute_fill_slippage(
        event_id="e3",
        records=records,
        evidence=_evidence("e3", fill_price=28000.5, fill_qty=10),
    )
    assert row.delta_pts == pytest.approx(0.50)
    assert row.panel_basis_pts == 0.50
    assert row.excess_pts == pytest.approx(0.0)
    assert row.excess_ticks == pytest.approx(0.0)


def test_entry_cohort_carries_delta_but_not_add_excess():
    """Base entries are recorded (free) but are not the Stage 2b gate."""
    records = [
        {
            "kind": "request_received",
            "parsed": {
                "leg_id": "dj30_mym",
                "signal_type": "entry",
                "close": 44000.0,
            },
        }
    ]
    row = compute_fill_slippage(
        event_id="e4",
        records=records,
        evidence=_evidence("e4", fill_price=44001.0, fill_qty=8),
    )
    assert row.is_complete
    assert row.delta_pts == pytest.approx(1.00)
    assert row.panel_basis_pts is None
    assert row.excess_pts is None
    assert not row.is_add


def test_incomplete_without_evidence():
    records = [
        {
            "kind": "request_received",
            "parsed": {
                "leg_id": "dj30_mym",
                "signal_type": "add",
                "close": 44000.0,
            },
        }
    ]
    row = compute_fill_slippage(event_id="e5", records=records, evidence=None)
    assert not row.is_complete
    assert row.incomplete_reason == "no_broker_evidence"


def test_incomplete_without_parsed_close():
    """The pre-34435e6 gap shape — evidence lands, close was dropped."""
    records = [
        {
            "kind": "request_received",
            "parsed": {
                "leg_id": "dj30_mym",
                "signal_type": "add",
                # close intentionally absent
            },
        }
    ]
    row = compute_fill_slippage(
        event_id="e6",
        records=records,
        evidence=_evidence("e6", fill_price=44001.0),
    )
    assert row.incomplete_reason == "missing_parsed_close"


def test_incomplete_without_fill_price():
    evidence = BrokerEvidence(
        event_id="e7",
        crosstrade_receive=True,
        crosstrade_validate=True,
        crosstrade_execute=True,
        fill_qty=60,
        fill_price=None,
    )
    records = [
        {
            "kind": "request_received",
            "parsed": {
                "leg_id": "dj30_mym",
                "signal_type": "add",
                "close": 44000.0,
            },
        }
    ]
    row = compute_fill_slippage(
        event_id="e7", records=records, evidence=evidence
    )
    assert row.incomplete_reason == "missing_fill_price"


# ── ledger join + cohort summary ──────────────────────────────────────────

def test_collect_joins_overlay_evidence(tmp_path: Path):
    events = tmp_path / "events.jsonl"
    overlay = tmp_path / "evidence.jsonl"
    ledger = EventLedger(events)

    _write_triad(
        ledger, event_id="add-1", leg_id="dj30_mym",
        signal_type="add", close=44000.0, qty_out=60,
    )
    _write_triad(
        ledger, event_id="base-1", leg_id="dj30_mym",
        signal_type="entry", close=43900.0, qty_out=8,
    )
    _write_triad(
        ledger, event_id="add-mnq", leg_id="nas100_mnq",
        signal_type="add", close=28000.0, qty_out=10,
    )

    # Overlay only — not yet appended into the ledger stream.
    for eid, px, qty in (
        ("add-1", 44002.0, 60),   # +1 tick excess
        ("base-1", 43901.0, 8),
        ("add-mnq", 28000.5, 10),  # exact panel
    ):
        line = json.dumps(
            _evidence(eid, fill_price=px, fill_qty=qty).to_dict(),
            separators=(",", ":"), sort_keys=True,
        ) + "\n"
        with overlay.open("a", encoding="utf-8") as f:
            f.write(line)

    rows = collect_fill_slippage(
        ledger, overlay=load_evidence_overlay(overlay)
    )
    assert len(rows) == 3
    assert all(r.is_complete for r in rows)

    summary = summarize_by_cohort(rows)
    assert summary["n_complete"] == 3
    assert summary["n_incomplete"] == 0

    # Cohort-split is mandatory: three distinct cells, no aggregate.
    cells = {(c["leg_id"], c["signal_type"]): c for c in summary["cohorts"]}
    assert set(cells) == {
        ("dj30_mym", "add"),
        ("dj30_mym", "entry"),
        ("nas100_mnq", "add"),
    }
    assert cells[("dj30_mym", "add")]["excess_pts_median"] == pytest.approx(1.0)
    assert cells[("dj30_mym", "add")]["mym_add_excess_ge_1_tick"] is True
    assert cells[("nas100_mnq", "add")]["excess_pts_median"] == pytest.approx(0.0)
    # Entry cell has no excess fields.
    assert "excess_pts_median" not in cells[("dj30_mym", "entry")]


def test_collect_prefers_overlay_over_ledger_evidence(tmp_path: Path):
    events = tmp_path / "events.jsonl"
    overlay = tmp_path / "evidence.jsonl"
    ledger = EventLedger(events)
    _write_triad(
        ledger, event_id="e1", leg_id="dj30_mym",
        signal_type="add", close=44000.0,
    )
    # Stale ledger evidence (exact panel).
    append_broker_evidence(ledger, _evidence("e1", fill_price=44001.0))
    # Fresher overlay (1-tick excess) — must win.
    with overlay.open("w", encoding="utf-8") as f:
        f.write(json.dumps(
            _evidence("e1", fill_price=44002.0).to_dict(),
            separators=(",", ":"), sort_keys=True,
        ) + "\n")

    rows = collect_fill_slippage(
        ledger, overlay=load_evidence_overlay(overlay), event_ids=["e1"]
    )
    assert len(rows) == 1
    assert rows[0].fill_price == 44002.0
    assert rows[0].excess_pts == pytest.approx(1.0)


def test_collect_uses_ledger_broker_evidence_when_no_overlay(tmp_path: Path):
    events = tmp_path / "events.jsonl"
    ledger = EventLedger(events)
    _write_triad(
        ledger, event_id="e1", leg_id="dj30_mym",
        signal_type="add", close=44000.0,
    )
    append_broker_evidence(ledger, _evidence("e1", fill_price=44001.0))

    rows = collect_fill_slippage(ledger)
    assert len(rows) == 1
    assert rows[0].excess_pts == pytest.approx(0.0)


# ── report + CLI read-only guarantee ──────────────────────────────────────

def test_format_report_is_cohort_split_not_aggregate():
    rows = [
        compute_fill_slippage(
            event_id="a",
            records=[{
                "kind": "request_received",
                "parsed": {
                    "leg_id": "dj30_mym",
                    "signal_type": "add",
                    "close": 44000.0,
                },
            }],
            evidence=_evidence("a", fill_price=44001.0),
        ),
        compute_fill_slippage(
            event_id="b",
            records=[{
                "kind": "request_received",
                "parsed": {
                    "leg_id": "dj30_mym",
                    "signal_type": "entry",
                    "close": 43900.0,
                },
            }],
            evidence=_evidence("b", fill_price=43901.0, fill_qty=8),
        ),
    ]
    text = format_report(rows, summarize_by_cohort(rows))
    assert "no aggregate" in text
    assert "dj30_mym/add" in text
    assert "dj30_mym/entry" in text
    assert "order_type=market" in text


def test_cli_does_not_append_to_ledger(tmp_path: Path):
    """Load-bearing: this CLI is read-only (unlike the reconciler)."""
    events = tmp_path / "events.jsonl"
    overlay = tmp_path / "evidence.jsonl"
    ledger = EventLedger(events)
    _write_triad(
        ledger, event_id="e1", leg_id="dj30_mym",
        signal_type="add", close=44000.0,
    )
    with overlay.open("w", encoding="utf-8") as f:
        f.write(json.dumps(
            _evidence("e1", fill_price=44001.0).to_dict(),
            separators=(",", ":"), sort_keys=True,
        ) + "\n")

    before = events.read_text(encoding="utf-8")
    before_lines = [ln for ln in before.splitlines() if ln.strip()]
    rc = slip._cli([
        "--events", str(events),
        "--evidence", str(overlay),
        "--json",
    ])
    assert rc == 0
    after = events.read_text(encoding="utf-8")
    after_lines = [ln for ln in after.splitlines() if ln.strip()]
    assert after == before
    assert len(after_lines) == len(before_lines)


def test_cli_json_shape(tmp_path: Path, capsys):
    events = tmp_path / "events.jsonl"
    overlay = tmp_path / "evidence.jsonl"
    ledger = EventLedger(events)
    _write_triad(
        ledger, event_id="e1", leg_id="dj30_mym",
        signal_type="add", close=44000.0,
    )
    with overlay.open("w", encoding="utf-8") as f:
        f.write(json.dumps(
            _evidence("e1", fill_price=44002.0).to_dict(),
            separators=(",", ":"), sort_keys=True,
        ) + "\n")

    rc = slip._cli([
        "--events", str(events),
        "--evidence", str(overlay),
        "--json",
    ])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert "rows" in payload and "summary" in payload
    assert payload["rows"][0]["excess_pts"] == pytest.approx(1.0)
    assert payload["summary"]["cohorts"][0]["mym_add_excess_ge_1_tick"] is True
