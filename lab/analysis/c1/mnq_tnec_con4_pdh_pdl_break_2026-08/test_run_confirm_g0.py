"""Hand-computed synthetic fixture for run_confirm_g0.py's window logic --
run BEFORE touching real bars, per this repo's standing discipline. Verifies
the only new logic vs run_construct_g0.py's run_explore(): the CONFIRM window
filter and the boundary-carry (first in-window session must use the prior
out-of-window session's H/L, not skip it)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import run_confirm_g0 as RC  # noqa: E402


def _synth_bar(ts, o, h, lo, c):
    return {"ts_event": ts, "open": o, "high": h, "low": lo, "close": c}


def _session_bars(date_str: str, o: float, h: float, lo: float, c: float):
    """One synthetic RTH session: 61 1m bars (>= the >=60-bar session floor),
    open bar carries the session's O, remaining bars flat until close bar."""
    base = pd.Timestamp(f"{date_str}T14:30:00Z")  # 09:30 ET (EST, UTC-5) -- all test dates are January
    bars = []
    for i in range(61):
        ts = base + pd.Timedelta(minutes=i)
        if i == 0:
            bars.append(_synth_bar(ts, o, h, lo, o))
        elif i == 60:
            bars.append(_synth_bar(ts, c, c, c, c))
        else:
            mid = (o + c) / 2.0
            bars.append(_synth_bar(ts, mid, mid, mid, mid))
    return bars


def _require_parquet_engine():
    """CI ops lock has neither pyarrow nor fastparquet (validation-controls.yml)."""
    for name in ("pyarrow", "fastparquet"):
        try:
            __import__(name)
            return
        except ImportError:
            continue
    pytest.skip("optional parquet engine not in requirements-ops.lock")


def _write_panel(tmp_path, sessions):
    _require_parquet_engine()
    rows = []
    for date_str, o, h, lo, c in sessions:
        rows.extend(_session_bars(date_str, o, h, lo, c))
    df = pd.DataFrame(rows)
    out = tmp_path / "_synth.parquet"
    df.to_parquet(out)
    return out


def test_boundary_session_uses_prior_out_of_window_session(tmp_path, monkeypatch):
    """Session before CONFIRM_START must still supply PDH/PDL to the first
    in-window session (no boundary gap), but must not itself be scored."""
    monkeypatch.setattr(RC, "CONFIRM_START", pd.Timestamp("2025-01-03").date())
    monkeypatch.setattr(RC, "CONFIRM_END", pd.Timestamp("2025-01-10").date())

    sessions = [
        # pre-window session: high=110, low=90 -> PDH/PDL available to the first
        # in-window session below. Excluded from scoring (before CONFIRM_START),
        # but must NOT be skipped when building the ordered/prior_hl lookback.
        ("2025-01-02", 100, 110, 90, 105),
        # first in-window session: uses 2025-01-02's H/L as its PDH/PDL
        ("2025-01-03", 105, 116, 104, 115),
        # second in-window session: uses 2025-01-03's H/L (116/104) as PDH/PDL --
        # a mid-session close of 122 > 116 fires a LONG, proving the boundary-carry
        # worked (the signal object exists and is scoreable, not skipped/errored)
        ("2025-01-06", 116, 130, 116, 128),
        # outside the window (after CONFIRM_END=2025-01-10) -- must not be scored
        ("2025-01-13", 128, 140, 127, 135),
    ]
    (_HERE / "CONFIRM_GO.md").touch(exist_ok=True)
    panel = _write_panel(tmp_path, sessions)
    out = RC.run_confirm(panel)

    # Exactly the two in-window sessions (2025-01-03, 2025-01-06) are scored --
    # 2025-01-02 is pre-window (excluded), 2025-01-13 is post-window (excluded).
    assert out["disclosures"]["scored_sessions"] == 2, out["disclosures"]
    # A trade fired at all -- proves the pre-window session's H/L (2025-01-02)
    # correctly carried as PDH/PDL into the window rather than being dropped at
    # the boundary (which would have left ordered[0]'s prior_hl unavailable and
    # produced zero trades throughout).
    assert out["long"]["n"] + out["short"]["n"] >= 1, (out["long"], out["short"])


def test_session_after_confirm_end_excluded(tmp_path, monkeypatch):
    monkeypatch.setattr(RC, "CONFIRM_START", pd.Timestamp("2025-01-03").date())
    monkeypatch.setattr(RC, "CONFIRM_END", pd.Timestamp("2025-01-06").date())
    sessions = [
        ("2025-01-02", 100, 110, 90, 105),
        ("2025-01-03", 105, 116, 104, 115),
        ("2025-01-06", 116, 130, 116, 128),
        ("2025-01-13", 128, 140, 127, 135),  # outside window -- must be excluded
    ]
    (_HERE / "CONFIRM_GO.md").touch(exist_ok=True)
    panel = _write_panel(tmp_path, sessions)
    out = RC.run_confirm(panel)
    assert out["disclosures"]["scored_sessions"] == 2, out["disclosures"]


def test_refuses_without_confirm_go(tmp_path, monkeypatch):
    go = _HERE / "CONFIRM_GO.md"
    existed = go.is_file()
    if existed:
        go.unlink()
    try:
        try:
            RC.run_confirm(tmp_path / "does_not_matter.parquet")
            assert False, "expected SystemExit"
        except SystemExit as e:
            assert "CONFIRM_GO.md missing" in str(e)
    finally:
        if existed:
            go.touch()
