"""Call-4 beta-cohesion diagnostic — synthetic lead-lag + public-clone skip.

Does not write lifecycle_state.json. Does not re-implement beta_death_assessment.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent


def test_lagged_copy_recovers_known_lag():
    from research_utils.beta_cohesion import pairwise_lead_lag

    rng = np.random.default_rng(7)
    x = rng.normal(size=400)
    lag = 3
    y = np.concatenate([np.zeros(lag), x[:-lag]])
    pairs = pairwise_lead_lag({"X": x, "Y": y}, max_lag=8)
    hit = pairs[("X", "Y")]
    assert hit.lag == lag
    assert hit.corr > 0.9


def test_independent_noise_raises_no_cohesion_flag():
    from research_utils.beta_cohesion import cohesion_flag, pairwise_lead_lag

    rng = np.random.default_rng(11)
    series = {
        "A": rng.normal(size=500),
        "B": rng.normal(size=500),
        "C": rng.normal(size=500),
        "D": rng.normal(size=500),
    }
    pairs = pairwise_lead_lag(series, max_lag=8)
    assert cohesion_flag(pairs) is False


def test_missing_csv_skips_without_crash(tmp_path):
    from research_utils.beta_cohesion import load_close_series

    missing = tmp_path / "no_such_panel.csv"
    series, reason = load_close_series("MNQ", missing)
    assert series is None
    assert "missing" in reason.lower()


def test_cli_missing_vendor_csv_skips(tmp_path):
    script = REPO / "scripts" / "beta_cohesion_read.py"
    out = tmp_path / "report.json"
    missing = tmp_path / "absent_BAR_EXPORT.csv"
    proc = subprocess.run(
        [
            sys.executable,
            str(script),
            "--series",
            f"MNQ={missing}",
            "--out",
            str(out),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONPATH": "lab"},
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(out.read_text())
    assert payload["skipped"]
    assert payload["wrote_lifecycle_state"] is False
    assert "beta_death_assessment" not in payload


def test_module_does_not_own_call4_counts_or_state():
    import research_utils.beta_cohesion as bc

    source = Path(bc.__file__).read_text()
    assert "import lifecycle" not in source
    assert "from lifecycle" not in source
    assert "lifecycle_state.json" not in source


def test_simple_ohlcv_csv_loads(tmp_path):
    from research_utils.beta_cohesion import load_close_series

    csv = tmp_path / "panel.csv"
    csv.write_text("time,open,high,low,close,volume\n" + "\n".join(
        f"2026-01-01T00:{i:02d}:00Z,1,1,1,{100 + i},1" for i in range(20)
    ))
    series, reason = load_close_series("SYN", csv)
    assert reason == ""
    assert series is not None
    assert series.size == 20
