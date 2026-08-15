"""W6 write_volume_config — refuses armed writes by default."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "ops" / "c1_rail" / "write_volume_config.py"


def _cfg(path: Path, *, dry_run: bool = True) -> None:
    path.write_text(
        json.dumps({"dry_run": dry_run, "events_log_path": "/data/old.jsonl"}) + "\n",
        encoding="utf-8",
    )


def test_dry_run_merge_prints_plan(tmp_path: Path):
    cfg = tmp_path / "c1_rail_config.json"
    _cfg(cfg)
    out = subprocess.check_output(
        [
            sys.executable,
            str(SCRIPT),
            "--config",
            str(cfg),
            "--set",
            "events_log_path=/data/c1_rail_events.jsonl",
            "--dry-run",
        ],
        text=True,
    )
    assert "DRY-RUN" in out
    assert json.loads(cfg.read_text(encoding="utf-8"))["events_log_path"] == "/data/old.jsonl"


def test_apply_merges_when_disarmed(tmp_path: Path):
    cfg = tmp_path / "c1_rail_config.json"
    _cfg(cfg, dry_run=True)
    subprocess.check_call(
        [
            sys.executable,
            str(SCRIPT),
            "--config",
            str(cfg),
            "--set",
            "events_log_path=/data/c1_rail_events.jsonl",
        ],
    )
    data = json.loads(cfg.read_text(encoding="utf-8"))
    assert data["events_log_path"] == "/data/c1_rail_events.jsonl"
    assert data["dry_run"] is True


def test_refuses_armed_without_force(tmp_path: Path):
    cfg = tmp_path / "c1_rail_config.json"
    _cfg(cfg, dry_run=False)
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--config",
            str(cfg),
            "--set",
            "events_log_path=/data/x.jsonl",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
    assert "refusing" in proc.stderr.lower()
