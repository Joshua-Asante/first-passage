"""W6 export_session_evidence — dry-run safe."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "ops" / "c1_rail" / "export_session_evidence.py"


def test_dry_run_plans_without_copy(tmp_path: Path):
    src = tmp_path / "data"
    src.mkdir()
    (src / "c1_rail_events.jsonl").write_text('{"k":1}\n', encoding="utf-8")
    (src / "c1_broker_evidence.jsonl").write_text("{}\n", encoding="utf-8")
    dest = tmp_path / "out"
    out = subprocess.check_output(
        [
            sys.executable,
            str(SCRIPT),
            "--src-dir",
            str(src),
            "--dest",
            str(dest),
        ],
        text=True,
    )
    assert "DRY-RUN" in out
    assert not dest.exists()


def test_apply_copies_files(tmp_path: Path):
    src = tmp_path / "data"
    src.mkdir()
    (src / "c1_rail_events.jsonl").write_text('{"k":1}\n', encoding="utf-8")
    dest = tmp_path / "out"
    subprocess.check_call(
        [
            sys.executable,
            str(SCRIPT),
            "--src-dir",
            str(src),
            "--dest",
            str(dest),
            "--apply",
        ],
    )
    assert (dest / "c1_rail_events.jsonl").read_text(encoding="utf-8") == '{"k":1}\n'
