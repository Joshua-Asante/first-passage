"""Unit tests for Q-MNQSEL-2 — hand-computed; green before real-bar gate run."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_HERE = Path(__file__).resolve().parent
_SEL1 = _HERE.parent / "mnq_selection_ceiling_2026-08"
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_SEL1))

import run_selection as S1  # noqa: E402
import run_selection_allbars as S  # noqa: E402


def test_frozen_gate_constants():
    assert S.GATE_G == 10.0
    assert S.DIAG_GS == (5.0, 20.0)
    assert S.RT_PT == 1.41
    assert S.EDGE_R == 0.40
    assert S.RANDOM_SEED == 20260808


def test_r_math_clean_target_at_g10():
    assert S1.r_from_pts(10.0, 10.0, 1.41) == pytest.approx(0.859)
    assert S1.r_from_pts(-10.0, 10.0, 1.41) == pytest.approx(-1.141)


def test_dense_clocks_are_every_bar():
    assert list(S.dense_clock_indices(5)) == [0, 1, 2, 3, 4]
    assert len(S.dense_clock_indices(0)) == 0


def test_sessionize_rth_keeps_0930_to_1559():
    # Build UTC stamps that map to one ET RTH day (2024-06-12 is EDT, UTC-4)
    # 09:30 ET = 13:30 UTC; 15:59 ET = 19:59 UTC; 16:00 ET = 20:00 UTC excluded
    idx = pd.date_range("2024-06-12 13:30", periods=400, freq="min", tz="UTC")
    # 390 RTH minutes: 09:30..15:59 — Timestamp.value is always ns
    o = h = l = c = np.linspace(100, 101, len(idx))
    epoch_ms = np.array([int(t.value // 1_000_000) for t in idx], dtype=np.int64)
    df = S.sessionize_rth(epoch_ms, o, h, l, c)
    assert len(df) == 390
    assert df["session"].nunique() == 1


def test_path_stop_wins_same_bar():
    o = 100.0
    h = np.array([120.0])
    l = np.array([50.0])
    c = np.array([100.0])
    pts, kind = S1.path_pts(o, +1, h, l, c, 0, stop_pt=10.0, g_pt=10.0)
    assert kind == "stop"
    assert pts == pytest.approx(-10.0)


def test_verdict_falsified_when_both_s3_below():
    long = {
        "n_sessions": 300,
        "S1_all_take_mean_R": -0.05,
        "S3_oracle_top1_mean_R": 0.39,
    }
    short = {
        "n_sessions": 300,
        "S1_all_take_mean_R": -0.05,
        "S3_oracle_top1_mean_R": 0.38,
    }
    # pad keys used by verdict_for
    for d in (long, short):
        d.setdefault("S2_random_1day_mean_R", 0.0)
    v, _ = S1.verdict_for(long, short)
    assert v == "FALSIFIED"


def test_verdict_resolved_when_s3_clears():
    long = {
        "n_sessions": 300,
        "S1_all_take_mean_R": -0.05,
        "S3_oracle_top1_mean_R": 0.50,
    }
    short = {
        "n_sessions": 300,
        "S1_all_take_mean_R": -0.05,
        "S3_oracle_top1_mean_R": 0.30,
    }
    v, detail = S1.verdict_for(long, short)
    assert v == "RESOLVED"
    assert "long" in detail
