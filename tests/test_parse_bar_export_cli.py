"""Smoke test for scripts/parse_bar_export.py."""
import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "scripts" / "parse_bar_export.py"


def _make_tv_csv(path, rows):
    df = pd.DataFrame(rows, columns=["Trade #", "Type", "Date and time", "Signal", "Price JPY"])
    df.to_csv(path, index=False, encoding="utf-8-sig")


def test_cli_parses_to_bar_data(tmp_path):
    src = tmp_path / "USDJPY_M15_pep.csv"
    _make_tv_csv(src, [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 156.574),
        (2, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.58|2000", 156.58),
    ])
    out = tmp_path / "USDJPY_M15.csv"
    result = subprocess.run(
        [sys.executable, str(CLI), "--symbol", "USDJPY", "--in", str(src), "--out", str(out)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert out.exists()
    lines = out.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "time,open,high,low,close,volume"
    assert len(lines) == 3  # header + 2 bars
    # v0.1 export -> no metadata sidecar
    assert not (out.parent / "USDJPY_M15.meta.json").exists()


def test_cli_writes_meta_sidecar_for_v2_export(tmp_path):
    src = tmp_path / "USDJPY_M15_pep.csv"
    _make_tv_csv(src, [
        (1, "Entry long", "2026-03-02 00:00",
         "1772409600000|156.64|156.806|156.572|156.574|3915|1772410499999|2|M"
         "|PEPPERSTONE:USDJPY|forex|JPY|USD|0.001|1000|America/New_York|15", 156.574),
    ])
    out = tmp_path / "USDJPY_M15.csv"
    result = subprocess.run(
        [sys.executable, str(CLI), "--symbol", "USDJPY", "--in", str(src), "--out", str(out)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    sidecar = out.parent / "USDJPY_M15.meta.json"
    assert sidecar.exists()
    import json
    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    assert payload["pointvalue"] == 1000.0
    assert payload["timezone"] == "America/New_York"
