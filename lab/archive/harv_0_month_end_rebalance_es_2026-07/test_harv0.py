"""Minimal unit tests for HARV-0 panel + §6 verdict (synthetic; no Databento).

Run: python -m pytest lab/analysis/harv_0_month_end_rebalance_es_2026-07/test_harv0.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from build_panel import (  # noqa: E402
    R_SPREAD_THRESHOLD_LOG,
    build_monthly_panel,
    load_symbol_frame,
    log_ret,
    prev_calendar_month,
    signal_from_r_spread,
    t_offsets,
)
from run_harv0 import (  # noqa: E402
    EffectResult,
    deployability_annotation,
    micro_same_sign_oos,
    perm_test_signed,
    verdict_from,
)


def _ohlc_frame(dates: pd.DatetimeIndex, closes: np.ndarray) -> pd.DataFrame:
    """Synthetic OHLC; open ≈ prior close for C/G decomposition."""
    opens = np.empty_like(closes)
    opens[0] = closes[0]
    opens[1:] = closes[:-1]
    return pd.DataFrame(
        {"open": opens, "high": closes, "low": closes, "close": closes},
        index=dates,
    )


def _business_days(start: str, end: str) -> pd.DatetimeIndex:
    return pd.bdate_range(start, end, freq="B")


def test_t_offsets_last_is_t1():
    days = pd.DatetimeIndex(pd.bdate_range("2024-01-01", "2024-01-31"))
    t = t_offsets(days)
    assert t[1] == days[-1]
    assert t[3] == days[-3]
    assert t[4] == days[-4]
    assert t[13] == days[-13]


def test_prev_calendar_month():
    assert prev_calendar_month(2024, 1) == (2023, 12)
    assert prev_calendar_month(2024, 7) == (2024, 6)


def test_signal_threshold_100bp():
    thr = R_SPREAD_THRESHOLD_LOG
    assert signal_from_r_spread(thr) == -1
    assert signal_from_r_spread(-thr) == +1
    assert signal_from_r_spread(thr * 0.5) == 0
    assert signal_from_r_spread(0.0) == 0


def test_synthetic_panel_known_effect():
    """Construct months where large positive R_spread predicts negative window."""
    dates = _business_days("2020-01-01", "2022-12-31")
    n = len(dates)
    zn_close = np.full(n, 100.0)
    es_close = np.full(n, 4000.0)

    by_month: dict[tuple[int, int], list[int]] = {}
    for i, d in enumerate(dates):
        by_month.setdefault((d.year, d.month), []).append(i)

    months_sorted = sorted(by_month)
    # Walk calendar months; set levels so R_spread ≈ +200bp and window ≈ −50bp.
    level = 4000.0
    for mi, key in enumerate(months_sorted):
        idxs = by_month[key]
        if len(idxs) < 13:
            continue
        t4, t3, t1 = idxs[-4], idxs[-3], idxs[-1]
        # Hold flat until T-4, then drop through T-1 (negative window).
        for i in idxs:
            es_close[i] = level
        # Ensure prior month's T-1 is `level` and this T-4 is level * exp(+0.02)
        # so R_spread (ES only; ZN flat) ≈ +200bp → short signal.
        if mi > 0:
            prev_idxs = by_month[months_sorted[mi - 1]]
            if len(prev_idxs) >= 1:
                es_close[prev_idxs[-1]] = level
            es_close[t4] = level * np.exp(0.02)
            # Window close(T-3)→close(T-1): negative
            es_close[t3] = es_close[t4]
            es_close[t1] = es_close[t3] * np.exp(-0.005)
            # Carry forward next month's base from this T-1
            level = float(es_close[t1])
        else:
            level = float(es_close[t1])

    es = _ohlc_frame(dates, es_close)
    zn = _ohlc_frame(dates, zn_close)
    panel = build_monthly_panel(es, zn, end_year=2022, end_month=12)
    assert len(panel) >= 20
    q = panel.loc[panel["qualifying"]]
    assert len(q) > 0, f"R_spread sample: {panel['R_spread_bp'].describe().to_dict()}"
    mean_signed = float(q["signed_window"].mean())
    assert mean_signed > 0


def test_perm_shuffles_labels_not_returns():
    """Observed effect from aligned labels should beat random shuffles."""
    rng = np.random.default_rng(0)
    n = 80
    window = rng.normal(0, 0.01, size=n)
    signal = np.zeros(n)
    # Plant a real edge: when signal=+1, window positive; signal=-1 → window negative.
    signal[:30] = 1
    signal[30:60] = -1
    window[:30] = np.abs(window[:30]) + 0.002
    window[30:60] = -np.abs(window[30:60]) - 0.002
    observed = float(np.mean(signal[signal != 0] * window[signal != 0]))
    p = perm_test_signed(window, signal, observed, n_perm=2000, rng=rng)
    assert observed > 0
    assert p <= 0.05


def test_verdict_falsified_wrong_sign():
    h1 = EffectResult("H1", 50, -0.001, 0.01, -0.002, 0.0, 0.01, 0.6)
    placebo = EffectResult("P", 50, 0.0, 0.01, 0.0, 0.0, 0.5, 0.6)
    inst = EffectResult("I", 50, 0.0, 0.01, 0.0, 0.0, 0.5, 0.6)
    verd, _ = verdict_from(h1, 4.0, 1.0, placebo, inst, {"pass": True}, True, 0.6)
    assert verd == "FALSIFIED"


def test_verdict_falsified_weak_p():
    h1 = EffectResult("H1", 50, 0.002, 0.01, 0.001, 0.003, 0.25, 0.6)  # 20bp, p=0.25
    placebo = EffectResult("P", 50, 0.0, 0.01, 0.0, 0.0, 0.5, 0.6)
    inst = EffectResult("I", 50, 0.0, 0.01, 0.0, 0.0, 0.5, 0.6)
    verd, _ = verdict_from(h1, 4.0, 1.0, placebo, inst, {"pass": True}, True, 0.6)
    assert verd == "FALSIFIED"


def test_verdict_ambiguous_thin():
    # 2bp effect, p=0.02, hurdles 1x=1bp 4x=4bp → thin AMBIGUOUS
    h1 = EffectResult("H1", 50, 0.0002, 0.01, 0.0, 0.0004, 0.02, 0.6)
    placebo = EffectResult("P", 50, 0.0, 0.01, 0.0, 0.0, 0.5, 0.6)
    inst = EffectResult("I", 50, 0.0, 0.01, 0.0, 0.0, 0.5, 0.6)
    verd, notes = verdict_from(h1, 4.0, 1.0, placebo, inst, {"pass": True}, True, 0.6)
    assert verd == "AMBIGUOUS"
    assert any("thin" in n for n in notes)


def test_verdict_resolved():
    h1 = EffectResult("H1", 100, 0.001, 0.01, 0.0005, 0.0015, 0.01, 0.65)  # 10bp
    placebo = EffectResult("P", 100, 0.0001, 0.01, 0.0, 0.0, 0.40, 0.65)  # |est|<50% of H1, p>0.10
    inst = EffectResult("I", 100, 0.0001, 0.01, 0.0, 0.0, 0.50, 0.65)
    verd, _ = verdict_from(h1, 4.0, 1.0, placebo, inst, {"pass": True}, True, 0.65)
    assert verd == "RESOLVED"


def test_verdict_ambiguous_micro_flip():
    h1 = EffectResult("H1", 100, 0.001, 0.01, 0.0005, 0.0015, 0.01, 0.65)
    placebo = EffectResult("P", 100, 0.0001, 0.01, 0.0, 0.0, 0.40, 0.65)
    inst = EffectResult("I", 100, 0.0001, 0.01, 0.0, 0.0, 0.50, 0.65)
    verd, notes = verdict_from(h1, 4.0, 1.0, placebo, inst, {"pass": True}, False, 0.65)
    assert verd == "AMBIGUOUS"
    assert any("micro" in n.lower() for n in notes)


def test_deployability_and_micro_helpers():
    assert deployability_annotation(0.001, 0.001, 5.0) == "YES"  # 10bp >= 5bp
    assert deployability_annotation(0.0001, 0.001, 5.0) == "NO"  # 1bp < 5bp
    assert deployability_annotation(-0.001, 0.001, 1.0) == "NO"  # wrong sign
    assert micro_same_sign_oos(0.01, 0.005) is True
    assert micro_same_sign_oos(0.01, -0.005) is False
    assert micro_same_sign_oos(0.01, None) is False


def test_log_ret_identity():
    assert log_ret(100.0, 100.0) == pytest.approx(0.0)
    assert log_ret(100.0, 101.0) == pytest.approx(np.log(1.01))


def test_load_symbol_frame_drops_weekend_bars(tmp_path):
    """Databento GLBX ohlcv-1d emits a thin Sunday-evening reopen bar (UTC-day
    bucketing). It is not a CME trade date and must not become a trading day, or the
    month-end T-k offsets shift. Regression for the settle_date=Sunday contamination.
    """
    # ts_event at 00:00 UTC on Fri / Sun / Mon (settle -> Fri / Sun / Mon).
    ts = pd.to_datetime(["2024-03-15", "2024-03-17", "2024-03-18"], utc=True)
    df = pd.DataFrame(
        {
            "ts_event": ts,
            "symbol": "ES.c.0",
            "open": [1.0, 2.0, 3.0],
            "high": [1.0, 2.0, 3.0],
            "low": [1.0, 2.0, 3.0],
            "close": [10.0, 20.0, 30.0],
        }
    )
    p = tmp_path / "es.parquet"
    df.to_parquet(p, index=False)
    out = load_symbol_frame(p, "ES.c.0")
    assert (out.index.dayofweek <= 4).all(), f"weekend day survived: {list(out.index)}"
    assert pd.Timestamp("2024-03-17") not in out.index  # Sunday dropped
    assert pd.Timestamp("2024-03-15") in out.index  # Friday kept
    assert pd.Timestamp("2024-03-18") in out.index  # Monday kept
