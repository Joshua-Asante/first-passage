"""Q-ORPREM-1 Phase 0 acceptance tests (a)–(j).

Run from the repo root::

    python -I scripts/fp.py python -m pytest lab/analysis/orb/orprem_mnq_2026-10 -q

Synthetic data only (pytest tmp_path; no core/data access, no network).  The
vendored ``orb_lib.py``, ``__init__.py`` and ``.gitattributes`` in this camp
are read-only inputs.  Every hand-computed expectation below is traceable to
the pre-registration: §4.2 (trade rule), §4.4 (worked examples), §4.3 (band,
cutpoints, renormalisation), §4.1 (eligibility), §7 Phase 0 items (a)–(e).

Tests:
  (a) reference parity — a verbatim copy of orb_lib's ``exec_win`` closure vs
      ``exec_win_h`` at H = remaining bars, zero cost (plus a cost check).
  (b) both §4.4 examples: Example 1 engine values + the day-2 pooling
      (Δ₃, N̄, Δ₂), Example 2 both-touch −1R and the undefined window.
  (c) decoding a synthetic v0.2 export: Entry-row count, dedup, decode rate,
      the immediate ≤ 2025-08-31 date cut.
  (d) cutpoints, trim and renormalisation (§4.3 steps 1–2, 5–6).
  (e) bootstrap determinism + equality with ``orb_lib.block_bootstrap_ci`` to
      1e-12, and a brute-force replicate check of ``bootstrap_delta``.
  (f) ``orb_backtest`` parity at w = 0 and the vendored-engine sha256 pin.
  (g) §4.1 eligibility: completeness, the Aₐ lookback (including donors
      before the window start and guard-failing donors), the 0.5%
      intra-RTH discontinuity guard, the no-prior-bar rule.
  (h) horizon/offset geometry and the frozen constants.
  (i) cost application: gross vs net (Δ₀ charges 1.11 in the window's own
      range) with a hand-computed 26-bar trade.
  (j) the CLI: FROZEN-status guard returns 2 on the real draft prereg; a
      synthetic frozen prereg drives a full g0 + score round trip.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from research_utils.camp_import import load_camp_sibling

orprem = load_camp_sibling("orprem", __file__)
run_orprem = load_camp_sibling("run_orprem", __file__)
ol = orprem.ol          # the exact vendored engine module the harness imports
CAMP = Path(__file__).resolve().parent

D1 = date(2021, 6, 1)
D2 = date(2021, 6, 2)


# ---------------------------------------------------------------- helpers
def sess(bars, a_prev, d=D1):
    o = np.array([b[0] for b in bars], float)
    h = np.array([b[1] for b in bars], float)
    l = np.array([b[2] for b in bars], float)
    c = np.array([b[3] for b in bars], float)
    return orprem.Session(date=d, o=o, h=h, l=l, c=c, a_prev=float(a_prev))


def gen_session(d, seed, n=26, base=15000.0, scale=6.0, drift=0.0):
    """Deterministic guard-passing session: every open equals the prior close."""
    rng = np.random.default_rng(seed)
    steps = rng.normal(0.0, scale, n)
    c = base + np.cumsum(steps) + drift * np.arange(1, n + 1)
    o = np.empty(n)
    o[0] = base
    o[1:] = c[:-1]
    spread = np.abs(rng.normal(0.0, scale, n)) + 0.5
    h = np.maximum(o, c) + spread
    l = np.minimum(o, c) - spread
    return orprem.Session(date=d, o=o, h=h, l=l, c=c,
                          a_prev=float(np.mean(h - l)))


# ---- verbatim reference: the exec_win closure of orb_lib.placebo_within_day.
# Copied verbatim from this camp's vendored orb_lib.py; only the closure's
# free variables (HH/LL/OO/CL, n_tods, or_bars, rt) become parameters.
def reference_exec_win(day, w0, rt, HH, LL, OO, CL, n_tods, or_bars=2):
    Ha, La, Oa, cl = HH[day], LL[day], OO[day], CL[day]
    or_idx = list(range(w0, w0 + or_bars))
    rest = range(w0 + or_bars, n_tods)
    or_hi = np.nanmax(Ha[or_idx]); or_lo = np.nanmin(La[or_idx])
    if not (np.isfinite(or_hi) and np.isfinite(or_lo)):
        return np.nan
    rng_ = or_hi - or_lo
    if rng_ <= 0:
        return np.nan
    entry = side = None
    for j in rest:
        bh, bl = Ha[j], La[j]
        if not np.isfinite(bh):
            continue
        up = bh >= or_hi; dn = bl <= or_lo
        if up and dn:
            side = 1 if Oa[j] <= (or_hi + or_lo) / 2 else -1
            entry = or_hi if side == 1 else or_lo; break
        if up:
            side, entry = 1, or_hi; break
        if dn:
            side, entry = -1, or_lo; break
    if entry is None:
        return np.nan
    rest_idx = list(rest)
    lo_rest = np.nanmin(La[rest_idx]); hi_rest = np.nanmax(Ha[rest_idx])
    if side == 1:
        stopped = lo_rest <= or_lo
        pnl = (or_lo if stopped else cl) - entry
    else:
        stopped = hi_rest >= or_hi
        pnl = entry - (or_hi if stopped else cl)
    return (pnl - rt) / rng_


# §4.4 Example 1 (7-bar day; H = 2)
EX1_BARS = [
    (100.0, 104.0, 98.0, 102.0),
    (102.0, 105.0, 99.0, 103.0),
    (103.0, 106.0, 102.0, 105.0),
    (105.0, 109.0, 104.0, 108.0),
    (108.0, 110.0, 107.0, 109.0),
    (109.0, 109.5, 101.0, 102.0),
    (102.0, 103.0, 100.0, 101.0),
]
# §4.4 Example 2 (window hi 10 / lo 8; Aₐ = 4 → x = ln 0.5)
EX2_TOUCH = [  # (a): both-touch entry bar, stopped on the entry bar
    (9.5, 10.0, 8.0, 9.0), (9.2, 9.8, 8.2, 9.4),
    (8.8, 10.5, 7.5, 9.0), (9.0, 9.5, 8.5, 9.2),
]
EX2_NOTOUCH = [  # (b): neither horizon bar touches a level
    (9.5, 10.0, 8.0, 9.0), (9.2, 9.8, 8.2, 9.4),
    (9.0, 9.5, 8.5, 9.2), (9.1, 9.4, 8.6, 9.3),
]


def i_bars():
    """26-bar session for test (i): long at 10 on bar 2, never stopped,
    exit at the 15:45 close 15.4 → gross R = 2.7 exactly."""
    bars = [(9.5, 10.0, 8.0, 9.0), (9.2, 9.8, 8.2, 9.4),
            (9.0, 11.0, 8.5, 10.8), (10.8, 11.2, 10.5, 11.0)]
    o = 11.0
    for _ in range(22):
        cbar = o + 0.2
        bars.append((o, cbar + 0.1, o - 0.1, cbar))
        o = cbar
    return bars


def flat(base, r, first_open=None, n=orprem.N_RTH_BARS):
    """n flat bars at one level with bar range r; opens = prior closes."""
    lvl = base if first_open is None else first_open
    bars, o = [], lvl
    for _ in range(n):
        bars.append((o, max(o, lvl) + r / 2.0, min(o, lvl) - r / 2.0, lvl))
        o = lvl
    return bars


def _epoch_ms(d, tod):
    ts = pd.Timestamp(year=d.year, month=d.month, day=d.day,
                      hour=tod // 60, minute=tod % 60, tz="America/New_York")
    return int(ts.value // 1_000_000)


def write_export(path, days, *, globex=True, globex_close=None, dup=None,
                 extra_rows=()):
    """Synthetic BAR_EXPORT v0.2 CSV (Type/Signal/Price USD) via tmp_path.

    ``days``: (date, bars) pairs, bars as (o, h, l, c).  With ``globex`` a
    09:15 bar precedes each session (close = the 09:30 open by default, or
    ``globex_close[date]``), which is what the §4.1 guard compares against.
    ``dup`` = (date, bar_index, close) emits a second Entry row for that
    epoch immediately after the original (adjacent in file order, so the
    loader's sort+keep-last dedup deterministically keeps it).
    """
    lines = ["Type,Signal,Price USD"]

    def emit(epoch, o, h, l, c):
        o, h, l, c = float(o), float(h), float(l), float(c)
        lines.append(f"Entry,{epoch}|{o!r}|{h!r}|{l!r}|{c!r}|100,{c!r}")

    for d, bars in days:
        if globex:
            g = bars[0][0] if globex_close is None else globex_close.get(d, bars[0][0])
            emit(_epoch_ms(d, orprem.OPEN_TOD - 15), g, g, g, g)
        for i, (o, h, l, c) in enumerate(bars):
            e = _epoch_ms(d, orprem.OPEN_TOD + 15 * i)
            emit(e, o, h, l, c)
            if dup is not None and dup[0] == d and dup[1] == i:
                emit(e, o + 0.1, h + 6.1, l - 5.9, dup[2])
    lines.extend(extra_rows)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def ex1_pool_records():
    """§4.4 pooling inputs: day 1 from the engine, day 2 given directly.

    Strata per the worked example: day1 OR and w=2 in A, day1 w=3 in B; day2
    OR in B, its nulls in A.  With band (−1, 4) and cuts (−0.1, 0.5, 2.0,
    3.0), A = stratum 2 = [−0.1, 0.5) and B = stratum 1 = [−1.0, −0.1):
    x(day1 OR) = x(day1 w=2) = ln(7/7) = 0 ∈ A, x(day1 w=3) = ln(6/7) =
    −0.1542 ∈ B, x(day2 OR) = −0.5 ∈ B, x(day2 nulls) ∈ {0.2, 0.3} ⊂ A.
    """
    s1 = sess(EX1_BARS, a_prev=7.0, d=D1)
    outs = {rec.w: rec for rec in orprem.score_session(s1, (0, 2, 3), 2)}

    def given(w, x, r):
        return orprem.WindowOutcome(D2, w, 2, 1.0, x, -1, True, True,
                                    0.0, 0.0, r)

    or_recs = [outs[0], given(0, -0.5, -1.0)]
    null_recs = [outs[2], outs[3], given(2, 0.2, 0.2), given(3, 0.3, -0.4)]
    return or_recs, null_recs


EX1_BAND, EX1_CUTS = (-1.0, 4.0), (-0.1, 0.5, 2.0, 3.0)


# ----------------------------------------------------------------- test (a)
def test_a_reference_exec_win_parity():
    sessions = [gen_session(date(2021, 6, 1 + k), seed=100 + k) for k in range(4)]
    sessions.append(sess(EX1_BARS, a_prev=7.0))          # 7-bar §4.4 day
    nan_day = gen_session(date(2021, 6, 9), seed=7)
    nan_day = orprem.Session(nan_day.date, nan_day.o, nan_day.h.copy(),
                             nan_day.l, nan_day.c, nan_day.a_prev)
    nan_day.h[10] = np.nan                                # skipped entry bar
    sessions.append(nan_day)

    checked = entered = 0
    for s in sessions:
        n = len(s.o)
        HH = {s.date: s.h}; LL = {s.date: s.l}
        OO = {s.date: s.o}; CL = {s.date: float(s.c[-1])}
        for w0 in range(0, n - 2):
            # H = the remaining bars, zero cost → the §4.4 placebo construct
            ref = reference_exec_win(s.date, w0, 0.0, HH, LL, OO, CL, n)
            out = orprem.exec_win_h(s, w0, n - 2 - w0, cost_pt=0.0)
            hi = float(np.nanmax(s.h[w0:w0 + 2]))
            lo = float(np.nanmin(s.l[w0:w0 + 2]))
            omega = hi - lo
            checked += 1
            if not np.isfinite(omega) or omega <= 0:
                assert out is None and np.isnan(ref)      # window skipped
            elif np.isnan(ref):
                assert out is not None and out.entered is False
                assert math.isnan(out.r)                  # R undefined
            else:
                entered += 1
                assert out is not None and out.entered
                assert out.r == pytest.approx(ref, rel=1e-12, abs=1e-12)
    assert checked >= 120 and entered >= 60

    # cost plumbing: rt charged in the window's own range, as in placebo_within_day
    s = sessions[0]
    n = len(s.o)
    HH = {s.date: s.h}; LL = {s.date: s.l}
    OO = {s.date: s.o}; CL = {s.date: float(s.c[-1])}
    for w0 in (0, 5, 11, 19):
        ref = reference_exec_win(s.date, w0, 1.41, HH, LL, OO, CL, n)
        out = orprem.exec_win_h(s, w0, n - 2 - w0, cost_pt=1.41)
        if np.isnan(ref):
            assert out is None or not out.entered or math.isnan(out.r)
        else:
            assert out.r == pytest.approx(ref, rel=1e-12, abs=1e-12)


# ----------------------------------------------------------------- test (b)
def test_b_worked_examples_s44():
    # Example 1, H = 2: entry/exit/R by hand from the §4.4 table
    s1 = sess(EX1_BARS, a_prev=7.0)
    outs = {rec.w: rec for rec in orprem.score_session(s1, (0, 2, 3), 2)}
    assert set(outs) == {0, 2, 3}
    or0 = outs[0]                                          # OR w=0
    assert or0.omega == pytest.approx(7.0) and or0.x == pytest.approx(0.0)
    assert or0.side == 1 and or0.entered and not or0.stopped
    assert or0.entry_px == pytest.approx(105.0)
    assert or0.exit_px == pytest.approx(108.0)             # b3 close
    assert or0.r == pytest.approx(3.0 / 7.0, rel=1e-12)    # +0.4286
    w2 = outs[2]
    assert w2.omega == pytest.approx(7.0) and w2.side == 1 and w2.stopped
    assert w2.exit_px == pytest.approx(102.0)
    assert w2.r == pytest.approx(-1.0)                     # −1.0000
    w3 = outs[3]
    assert w3.omega == pytest.approx(6.0) and w3.side == -1 and not w3.stopped
    assert w3.exit_px == pytest.approx(101.0)              # b6 close
    assert w3.r == pytest.approx(0.5)                      # +0.5000
    assert w3.x == pytest.approx(math.log(6.0 / 7.0), rel=1e-12)

    # Pooling with day 2 (§4.4): R̄_OR, p_OR, N̄, Δ₃, and the Δ₂ contrast
    or_recs, null_recs = ex1_pool_records()
    res = orprem.delta3(or_recs, null_recs, EX1_BAND, EX1_CUTS)
    assert res["or_mean"] == pytest.approx((3.0 / 7.0 - 1.0) / 2.0, rel=1e-12)
    assert res["p_or"] == pytest.approx([0.5, 0.5, 0.0, 0.0, 0.0])
    assert res["matched_null"] == pytest.approx(0.05)      # N̄ = +0.0500
    assert res["delta3"] == pytest.approx(-0.3357142857142857, rel=1e-9)
    assert res["renormalised_strata"] == []
    assert res["n_null_by_stratum"] == [1, 3, 0, 0, 0]
    # the unweighted null mean −0.1750 and Δ₂ = −0.1107 (§4.4), by hand
    null_rs = [-1.0, 0.5, 0.2, -0.4]
    assert sum(null_rs) / 4 == pytest.approx(-0.175)
    assert res["or_mean"] - (-0.175) == pytest.approx(-0.1107142857142857,
                                                      rel=1e-9)

    # Example 2(a): both-touch bar, open 8.8 ≤ midpoint 9 → long at 10,
    # stop 8 touched on the entry bar → R = (8 − 10)/2 = −1.0000
    out = orprem.exec_win_h(sess(EX2_TOUCH, a_prev=4.0), 0, 2)
    assert out.omega == pytest.approx(2.0)
    assert out.x == pytest.approx(math.log(0.5), rel=1e-12)   # −0.6931
    assert out.side == 1 and out.entered and out.stopped
    assert out.entry_px == pytest.approx(10.0)
    assert out.exit_px == pytest.approx(8.0)
    assert out.r == pytest.approx(-1.0)
    # Example 2(b): no touch → R undefined, the window leaves every mean
    outb = orprem.exec_win_h(sess(EX2_NOTOUCH, a_prev=4.0), 0, 2)
    assert outb is not None and outb.entered is False and math.isnan(outb.r)


# ----------------------------------------------------------------- test (c)
def test_c_decode_synthetic_v02_export(tmp_path):
    d1, d2, d3 = date(2025, 8, 27), date(2025, 8, 28), date(2025, 8, 29)
    d4 = date(2025, 9, 10)                                  # after the cut
    days = [(d1, flat(15000.0, 2.0)), (d2, flat(15000.0, 3.0)),
            (d3, flat(15100.0, 4.0)), (d4, flat(15200.0, 2.0))]
    dup_epoch = _epoch_ms(d1, orprem.OPEN_TOD + 15 * 5)
    dup_close = 15005.1
    csv = tmp_path / "syn_v02.csv"
    write_export(csv, days, dup=(d1, 5, dup_close), extra_rows=[
        "Header,synthetic v0.2 fixture,0",
        "Entry,not-a-signal,0",                             # undecodable Entry
    ])
    df, info = orprem.decode_export(csv)

    # Entry rows: 4 sessions × (26 RTH + 1 globex) + undecodable + duplicate
    assert info["n_entry_rows"] == 4 * 27 + 2
    # the loader returns its dedup rows: the duplicate collapses, the bad row
    # is skipped → 108 of 110 decode (the §6 gate counts rows only)
    assert info["rows_decoded"] == 108
    assert info["decode_rate"] == pytest.approx(108.0 / 110.0)
    assert info["max_date_before_cut"] == "2025-09-10"
    # the immediate date cut (§4.1): d4's 27 rows dropped, nothing later kept
    assert info["rows_after_cut"] == 81
    assert info["max_session_date"] == "2025-08-29"
    assert info["max_session_date"] <= "2025-08-31"
    assert len(df) == 81
    assert df["d"].max() == d3
    # dedup keeps the last row for a repeated epoch (keep="last")
    row = df[df["epoch"] == dup_epoch]
    assert len(row) == 1 and row["close"].iloc[0] == dup_close
    # the decoded frame carries the engine's ET session tagging
    assert {"et", "d", "tod"}.issubset(df.columns)
    tods = set(df[df["d"] == d1]["tod"])
    assert tods == set(orprem.RTH_TODS) | {orprem.OPEN_TOD - 15}


# ----------------------------------------------------------------- test (d)
def test_d_cutpoints_trim_renormalisation():
    # §4.3 steps 1–2 on x = 0..9: numpy linear quantiles, hand-computed
    band, cuts = orprem.fit_band_and_cuts([float(i) for i in range(10)])
    assert band == pytest.approx((0.45, 8.55), abs=1e-12)   # p5, p95
    assert cuts == pytest.approx((2.4, 3.8, 5.2, 6.6), abs=1e-12)  # c1..c4

    def rec(x, r):
        return orprem.WindowOutcome(D1, 0, 8, 1.0, x, 1, True, False,
                                    0.0, 0.0, r)

    # stratum edges: cutpoints belong upward; band edges are inclusive.  The
    # probe x values sit clear of the cutpoints, because numpy's linear
    # quantiles differ from the decimal literals by ~1e-16 (c1 is
    # 2.4000000000000004, c3 is 5.199999999999999): the §4.3 half-open rule
    # is exact, and boundary membership is pinned below with a literal band.
    # Strata here: [0.45,2.4) [2.4,3.8) [3.8,5.2) [5.2,6.6) [6.6,8.55].
    or_recs = [rec(x, 1.0) for x in (0.46, 2.5, 3.9, 5.4, 6.7, 8.54)]
    null_recs = [rec(x, r) for x, r in
                 zip((0.46, 2.5, 3.9, 5.4, 6.7), (-0.1, -0.2, -0.3, -0.4, -0.5))]
    res = orprem.delta3(or_recs, null_recs, band, cuts)
    assert res["p_or"] == pytest.approx([1 / 6, 1 / 6, 1 / 6, 1 / 6, 2 / 6])
    assert res["or_mean"] == pytest.approx(1.0)
    assert res["n_null_by_stratum"] == [1, 1, 1, 1, 1]
    assert res["matched_null"] == pytest.approx(-2.0 / 6.0)
    assert res["delta3"] == pytest.approx(1.0 + 2.0 / 6.0)
    assert res["renormalised_strata"] == []
    # inclusive band edges, pinned with a literal band (both edges stay in Δ₃)
    lit_cuts = (2.4, 3.8, 5.2, 6.6)
    assert orprem._stratum_of(0.45, (0.45, 8.55), lit_cuts) == 1
    assert orprem._stratum_of(8.55, (0.45, 8.55), lit_cuts) == 5

    # trim: inside-band x stays in Δ₃, out-of-band x leaves it (x only)
    res2 = orprem.delta3([rec(0.5, 1.0), rec(8.5, 1.0), rec(0.44, 5.0)],
                         [], band, cuts)
    assert res2["n_or"] == 2 and res2["n_or_untrimmed"] == 3
    assert res2["or_mean"] == pytest.approx(1.0)
    assert res2["untrimmed_or_mean"] == pytest.approx(7.0 / 3.0)  # reported
    # §4.4 Example 2(c): x = ln 0.5 under a −0.5 band low leaves Δ₃, any arm
    assert orprem._stratum_of(math.log(0.5), (-0.5, 1.0), (0.0, 0.5, 1.5, 2.0)) == 0
    assert orprem._stratum_of(-0.5, (-0.5, 1.0), (0.0, 0.5, 1.5, 2.0)) == 1

    # renormalisation (§4.3 step 6): stratum B loses its only null → p_OR is
    # renormalised over stratum A and the event is reported
    or_recs, null_recs = ex1_pool_records()
    assert null_recs[1].date == D1 and null_recs[1].w == 3   # the B-stratum null
    res3 = orprem.delta3(or_recs, [null_recs[0], *null_recs[2:]],
                         EX1_BAND, EX1_CUTS)
    assert res3["renormalised_strata"] == [1]
    assert res3["matched_null"] == pytest.approx(-0.4)        # A only
    assert res3["delta3"] == pytest.approx(-0.2857142857142857 + 0.4, rel=1e-9)


# ----------------------------------------------------------------- test (e)
def test_e_bootstrap_determinism_and_engine_parity():
    x = np.sin(np.arange(50.0) / 3.0) + np.arange(50.0) / 100.0
    # orb_lib.block_bootstrap_ci parity, to 1e-12 (identical rng scheme)
    lo, hi, ple = orprem.bootstrap_mean(x, block=5, n=4000, seed=42,
                                        q=(2.5, 97.5))
    lo2, hi2, ple2 = ol.block_bootstrap_ci(x, block=5, n=4000, seed=42,
                                           q=(2.5, 97.5))
    assert lo == pytest.approx(lo2, abs=1e-12)
    assert hi == pytest.approx(hi2, abs=1e-12)
    assert ple == pytest.approx(ple2, abs=1e-12)
    # determinism, and the frozen one-sided default q = (2.5, 95)
    a = orprem.bootstrap_mean(x, block=5, n=4000, seed=42)
    b = orprem.bootstrap_mean(x, block=5, n=4000, seed=42)
    assert a == b
    c = orprem.bootstrap_mean(x, block=5, n=4000, seed=43)
    assert c[:2] != a[:2]
    assert a[:2] == orprem.bootstrap_mean(x, block=5, n=4000, seed=42,
                                          q=(2.5, 95.0))[:2]

    # bootstrap_delta: determinism, seed sensitivity, brute-force replicates
    sessions = [gen_session(date(2021, 6, 1 + k), seed=200 + k) for k in range(8)]
    offs = tuple(range(2, 17))
    kw = dict(null_offsets=offs, H_or=8, H_null=8, weighted=False,
              block=5, n=300, seed=7)
    r1 = orprem.bootstrap_delta(sessions, **kw)
    r2 = orprem.bootstrap_delta(sessions, **kw)
    assert np.array_equal(r1["stats"], r2["stats"], equal_nan=True)
    assert r1["lo"] == r2["lo"] and r1["hi"] == r2["hi"]
    r3 = orprem.bootstrap_delta(sessions, **{**kw, "seed": 8})
    assert not np.array_equal(r1["stats"], r3["stats"], equal_nan=True)

    or_by = [[rec.r for rec in orprem.score_session(s, (0,), 8) if rec.entered]
             for s in sessions]
    nu_by = [[rec.r for rec in orprem.score_session(s, offs, 8) if rec.entered]
             for s in sessions]
    rng = np.random.default_rng(7)
    N = len(sessions)
    pool = np.arange(0, N - 5 + 1)
    nblocks = int(np.ceil(N / 5))
    expect = np.full(300, np.nan)
    for i in range(300):
        st = rng.choice(pool, size=nblocks)
        idx = (st[:, None] + np.arange(5)[None, :]).ravel()[:N]
        ors = [v for j in idx for v in or_by[j]]
        nus = [v for j in idx for v in nu_by[j]]
        if ors and nus:
            expect[i] = float(np.mean(ors)) - float(np.mean(nus))
    assert np.allclose(r1["stats"], expect, rtol=1e-12, atol=1e-12,
                       equal_nan=True)

    # the weighted (Δ₃) bootstrap is deterministic too, with fixed band/cuts
    xs = [rec.x for s in sessions
          for rec in orprem.score_session(s, (0,), 8)]
    band, cuts = orprem.fit_band_and_cuts(xs)
    wkw = dict(null_offsets=offs, H_or=8, H_null=8, weighted=True,
               band=band, cuts=cuts, block=5, n=250, seed=42)
    w1 = orprem.bootstrap_delta(sessions, **wkw)
    w2 = orprem.bootstrap_delta(sessions, **wkw)
    assert np.array_equal(w1["stats"], w2["stats"], equal_nan=True)
    assert w1["lo"] == w2["lo"] and w1["hi"] == w2["hi"]


# ----------------------------------------------------------------- test (f)
def test_f_orb_backtest_parity_and_engine_pin(tmp_path):
    drifts = (4.0, -4.0, 2.0, -2.0, 0.0)
    days = []
    for k, drift in enumerate(drifts):
        d = date(2021, 5, 28) if k == 0 else date(2021, 6, k)
        s = gen_session(d, seed=300 + k, drift=drift)
        days.append((d, list(zip(s.o, s.h, s.l, s.c))))
    csv = tmp_path / "panel.csv"
    write_export(csv, days)
    df, info = orprem.decode_export(csv)
    assert info["max_session_date"] == "2021-06-04"

    # the vendored engine, pinned: only this camp's copy, exact archive sha
    assert Path(ol.__file__).resolve().parent == CAMP
    assert hashlib.sha256(Path(ol.__file__).read_bytes()).hexdigest() \
        == orprem.ORB_LIB_SHA256
    assert orprem.ORB_LIB_SHA256 == \
        "e8b0caf8032439ced8b565df9ce3a3077c7b685c0ddfe6e093493d78f25e9259"
    assert orprem._engine_sha256() == orprem.ORB_LIB_SHA256

    inst = ol.Instrument("MNQ_syn", csv, "bar_export", "TradingView",
                         tick=0.25, spread_pt=0.5, rt_cost_pt=1.11)
    piv, meta = ol.session_panel(df, inst)
    bt = ol.orb_backtest(piv, meta, inst, or_bars=2, entry_slip_pt=0.0)
    by_day = dict(zip(bt["day"], bt["R"]))

    rep = orprem.eligible_sessions(df, date(2021, 5, 28), date(2021, 6, 30))
    # the first session has no earlier complete session → Aₐ missing (§4.1)
    assert rep["excluded"] == [[date(2021, 5, 28), "no_prior_complete_session"]]
    assert len(rep["sessions"]) == 4

    entered = 0
    for s in rep["sessions"]:
        # w = 0, exit at close (H = 24), net 1.11 → the certified ORB arm
        out = orprem.exec_win_h(s, 0, 24, cost_pt=1.11)
        if out is None or not out.entered:
            assert s.date not in by_day        # orb_backtest skipped it too
        else:
            entered += 1
            assert by_day[s.date] == pytest.approx(out.r, rel=1e-12, abs=1e-12)
    assert entered == sum(1 for s in rep["sessions"] if s.date in by_day)
    assert entered >= 2                        # the comparison is non-vacuous


# ----------------------------------------------------------------- test (g)
def test_g_session_eligibility_aa_and_guard(tmp_path):
    d0 = date(2021, 5, 28)
    d1, d2, d3 = date(2021, 6, 1), date(2021, 6, 2), date(2021, 6, 3)
    d4, d5 = date(2021, 6, 4), date(2021, 6, 7)
    csv = tmp_path / "elig.csv"
    write_export(csv, [
        (d0, flat(15000.0, 2.0)),                     # Aₐ donor only
        (d1, flat(15000.0, 2.0)),
        (d2, flat(15000.0, 2.0)[:25]),                # 25 RTH bars → incomplete
        (d3, flat(15000.0, 2.0)),
        (d4, flat(15000.0, 2.0, first_open=15151.0)),  # 1.0067% gap at 09:30
        (d5, flat(15000.0, 4.0)),
    ], globex_close={d4: 15000.0})
    df, _ = orprem.decode_export(csv)

    rep = orprem.eligible_sessions(df, d1, d5)
    assert [s.date for s in rep["sessions"]] == [d1, d3, d5]
    assert rep["excluded"] == [[d2, "incomplete_rth"],
                               [d4, "intra_rth_discontinuity"]]
    # Aₐ: most recent earlier complete session, even before the window start,
    # skipping incomplete sessions; guard-failing sessions still qualify as
    # donors (§4.1 words the lookback as completeness only)
    assert rep["complete_dates"] == [d0, d1, d3, d4, d5]
    assert rep["sessions"][0].a_prev == pytest.approx(2.0)   # from d0
    assert rep["sessions"][1].a_prev == pytest.approx(2.0)   # from d1, not d2
    assert rep["sessions"][2].a_prev == pytest.approx(2.0)   # from d4
    s = rep["sessions"][0]
    assert len(s.o) == 26 and s.o[0] == pytest.approx(15000.0)
    assert s.c[25] == pytest.approx(15000.0)

    # a session with no earlier complete session is ineligible
    rep2 = orprem.eligible_sessions(df, d0, d0)
    assert rep2["sessions"] == []
    assert rep2["excluded"] == [[d0, "no_prior_complete_session"]]

    # a 09:30 bar with no predecessor row in the export is ineligible (§4.1)
    mini = tmp_path / "mini.csv"
    write_export(mini, [(d0, flat(15000.0, 2.0))], globex=False)
    dfm, _ = orprem.decode_export(mini)
    repm = orprem.eligible_sessions(dfm, d0, d0)
    assert repm["excluded"] == [[d0, "no_prior_bar"]]


# ----------------------------------------------------------------- test (h)
def test_h_geometry_and_constants():
    o = orprem
    # frozen constants (§4.1–§4.3, §6, §7)
    assert o.OR_BARS == 2 and o.N_RTH_BARS == 26 and len(o.RTH_TODS) == 26
    assert o.OPEN_TOD == 570 and o.CLOSE_TOD == 945 and o.BAR_MINUTES == 15
    assert o.RTH_TODS[0] == 570 and o.RTH_TODS[-1] == 945
    assert o.H_PRIMARY == 8 and o.W_OR == 0
    assert o.W_NULL_D0 == tuple(range(1, 24))     # Δ₀: {1..23}
    assert o.W_NULL_D1 == tuple(range(2, 24))     # Δ₁: {2..23}
    assert o.W_NULL_D2 == tuple(range(2, 17))     # Δ₂/Δ₃: {2..16}
    assert 1 in o.W_NULL_D0 and 1 not in o.W_NULL_D1 and 1 not in o.W_NULL_D2
    assert max(o.W_NULL_D2) == 16 and max(o.W_NULL_D1) == 23
    assert o.RT_COST_PT_BULENOX == 1.11 and o.RT_COST_PT_TRADEIFY == 1.41
    assert o.M_PREMIUM == 0.032 and o.FEED_SCOPE_BAND == (0.05, 0.15)
    assert o.TRIM_Q == (0.05, 0.95)
    assert o.STRATA_Q == (0.20, 0.40, 0.60, 0.80) and o.N_STRATA == 5
    assert o.BOOT_BLOCK == 5 and o.BOOT_N == 10_000 and o.BOOT_SEED == 42
    assert o.BOOT_SEEDS_REPORTED == (123, 2026) and o.BOOT_BLOCK_REPORTED == 10
    assert o.Q_LOWER == 2.5 and o.Q_UPPER == 95.0
    assert o.GUARD_MAX_JUMP == 0.005 and o.DECODE_RATE_MIN == 0.99
    assert (o.SUPPORT_MIN_WINDOWS, o.SUPPORT_MIN_SESSIONS,
            o.SUPPORT_MIN_OFFSETS, o.SUPPORT_MAX_X_GAP) == (200, 100, 5, 0.10)
    assert o.DATE_CUT == date(2025, 8, 31)
    assert o.PANEL_E2 == (date(2021, 1, 1), date(2025, 8, 31))
    assert o.PANEL_E1 == (date(2019, 9, 1), date(2020, 12, 31))
    assert o.E1_BLEND_SPLIT == date(2020, 6, 30)
    assert o.PREREG_NAME == "2026-10-19-q-orprem-1-matched-null-prereg-DRAFT.md"

    # horizon geometry (§4.2 "Why H = 8"): bar index w+1+H is the last
    # horizon bar; its bar-open tod plus 15 minutes is the exit time
    assert o.OPEN_TOD + 15 * (0 + 1 + 8) == 11 * 60 + 45    # OR ends 12:00
    assert o.OPEN_TOD + 15 * (16 + 1 + 8) == o.CLOSE_TOD    # w=16 ends 16:00
    assert o.OPEN_TOD + 15 * (17 + 1 + 8) > o.CLOSE_TOD     # w=17 would not
    assert o._h_close(0) == 24 and o._h_close(23) == 1
    s26 = sess(EX2_TOUCH + [(9.2, 9.4, 9.0, 9.2)] * 22, a_prev=4.0)
    assert len(s26.o) == 26
    assert orprem.exec_win_h(s26, 0, 8).H == 8
    assert orprem.exec_win_h(s26, 16, 8) is not None
    with pytest.raises(ValueError):
        orprem.exec_win_h(s26, 17, 8)                       # past the session
    scored = {r.w: r for r in
              orprem.score_session(s26, (0, 23), o.EXIT_CLOSE)}
    assert scored[0].H == 24 and scored[23].H == 1


# ----------------------------------------------------------------- test (i)
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_i_cost_application_delta0():
    s = sess(i_bars(), a_prev=2.0)
    gross = orprem.exec_win_h(s, 0, 24, cost_pt=0.0)
    net = orprem.exec_win_h(s, 0, 24, cost_pt=orprem.RT_COST_PT_BULENOX)
    assert gross.side == 1 and gross.entered and not gross.stopped
    assert gross.omega == pytest.approx(2.0)
    assert gross.entry_px == pytest.approx(10.0)            # window high
    assert gross.exit_px == pytest.approx(15.4)             # 15:45 close
    assert gross.r == pytest.approx(2.7)                    # 5.4 / 2
    assert net.r == pytest.approx(2.145)                    # (5.4 − 1.11)/2
    assert net.r - gross.r == pytest.approx(-orprem.RT_COST_PT_BULENOX / 2.0)

    # the ladder's Δ₀ charges 1.11 in each window's own range; Δ₁ is gross.
    # band/cuts are supplied (E1-style reuse) so the tiny two-session panel
    # need not fit its own band.
    s2 = sess([(2 * o, 2 * h, 2 * l, 2 * c) for o, h, l, c in i_bars()],
              a_prev=2.0)
    lad = orprem.ladder([s, s2], band=(-1.0, 2.0), cuts=(-0.5, 0.0, 0.3, 0.5),
                        n=50)
    assert lad["rungs"]["delta0"]["n_or"] == 2
    assert lad["rungs"]["delta0"]["or_mean"] == pytest.approx((2.145 + 2.4225) / 2)
    assert lad["rungs"]["delta1"]["or_mean"] == pytest.approx(2.7)  # scale-free
    assert (lad["rungs"]["delta0"]["or_mean"]
            - lad["rungs"]["delta1"]["or_mean"]) == pytest.approx(-0.41625)
    assert set(lad["attribution"]) == {"d0_minus_d1", "d1_minus_d2",
                                       "d2_minus_d3"}


# ----------------------------------------------------------------- test (j)
FROZEN_MD = ("# synthetic frozen pre-registration fixture (Phase 0 tests)\n\n"
             "**Status:** `FROZEN 2026-10-24` (synthetic fixture; test-only).\n")


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_j_cli_frozen_guard_and_synthetic_g0(tmp_path):
    # (1) the real draft refuses: the guard reads the prereg only, never data
    assert run_orprem.main(["g0"]) == 2
    assert run_orprem.main(["score", "--v7-gate", "ruling:synthetic"]) == 2
    assert not (CAMP / "G0.json").exists()
    proc = subprocess.run([sys.executable, str(CAMP / "run_orprem.py"), "g0"],
                          capture_output=True, text=True, timeout=180)
    assert proc.returncode == 2
    assert "refusing" in proc.stderr and "FROZEN" in proc.stderr

    # (2) a frozen synthetic prereg + synthetic export drive g0 end to end
    frozen = tmp_path / "frozen_prereg.md"
    frozen.write_text(FROZEN_MD, encoding="utf-8")
    csv = tmp_path / "e2.csv"
    write_export(csv, [(d, flat(15000.0 + 10 * k, 2.0 + 0.5 * k))
                       for k, d in enumerate(
                           (date(2025, 8, 22), date(2025, 8, 25),
                            date(2025, 8, 26), date(2025, 8, 27)))])
    g0_path = tmp_path / "G0.json"
    assert run_orprem.main(["g0", "--prereg", str(frozen),
                            "--e2-csv", str(csv), "--out", str(g0_path)]) == 0
    g0 = json.loads(g0_path.read_text(encoding="utf-8"))
    e2 = g0["panels"]["E2"]
    assert g0["phase"] == "G0"
    assert g0["prereg"] == str(frozen)
    assert g0["prereg_sha256"] == hashlib.sha256(frozen.read_bytes()).hexdigest()
    assert g0["inputs"]["e2"]["sha256"] == \
        hashlib.sha256(csv.read_bytes()).hexdigest()
    assert g0["orb_lib_sha256"] == orprem.ORB_LIB_SHA256
    assert g0["max_session_date"] == "2025-08-27"   # top level, for the §10 hook
    assert e2["max_session_date"] == "2025-08-27"   # ≤ 2025-08-31 asserted
    assert e2["decode_rate"] == pytest.approx(1.0)
    assert e2["n_sessions"] == 3                    # the first day lacks Aₐ
    assert e2["excluded"] == [["2025-08-22", "no_prior_complete_session"]]
    assert len(e2["band"]) == 2 and len(e2["cuts"]) == 4
    assert set(e2["support"]) == {"1", "2", "3", "4", "5"}
    assert all(v["pass"] is False for v in e2["support"].values())
    assert e2["routing"] == "width_unmatched"       # tiny synthetic support

    # (3) score: the v7 gate is required (a commit must be an ancestor of HEAD;
    # a bare/unknown value refuses), inputs must match G0, then a round trip
    rec_path = tmp_path / "record.json"
    base = ["score", "--prereg", str(frozen), "--e2-csv", str(csv),
            "--g0", str(g0_path), "--out", str(rec_path), "--boot-n", "200"]
    assert run_orprem.main(base) == 2                               # no gate
    assert run_orprem.main(base + ["--v7-gate", "f" * 40]) == 2     # not an ancestor
    assert run_orprem.main(base + ["--v7-gate", "ruling:"]) == 2    # empty ruling
    other = tmp_path / "other.csv"
    other.write_bytes(csv.read_bytes() + b"\n")
    assert run_orprem.main(["score", "--prereg", str(frozen), "--e2-csv",
                            str(other), "--g0", str(g0_path), "--out",
                            str(rec_path), "--v7-gate", "ruling:synthetic"]) == 2
    assert not rec_path.exists()
    assert run_orprem.main(base + ["--v7-gate", "ruling:synthetic"]) == 0
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    assert rec["phase"] == "score"
    assert rec["seed"] == 42 and rec["block"] == 5 and rec["n_boot"] == 200
    assert rec["orb_lib_sha256"] == orprem.ORB_LIB_SHA256
    assert rec["v7_gate"] == "ruling:synthetic"
    assert set(rec["sensitivity"]) == {"seed_123", "seed_2026", "block_10"}
    assert rec["max_session_date"] <= "2025-08-31"
    assert rec["routing"] == "width_unmatched"
    assert rec["e1_report"] is None
    assert set(rec["ladder"]["rungs"]) == {"delta0", "delta1", "delta2",
                                           "delta3"}
    assert set(rec["ladder"]["attribution"]) == {"d0_minus_d1", "d1_minus_d2",
                                                 "d2_minus_d3"}
    assert rec["gate_read"]["primary"] == "delta2"  # Δ₂ under width-unmatched
    assert isinstance(rec["code_commit"], (str, type(None)))

    # (4) a missing/not-frozen prereg refuses even with the v7 gate recorded
    assert run_orprem.main(["score", "--prereg", str(tmp_path / "nope.md"),
                            "--v7-gate", "ruling:synthetic"]) == 2
    draft = tmp_path / "draft.md"
    draft.write_text("**Status:** `OPEN - DRAFT (pre-lock)`. Not frozen.\n",
                     encoding="utf-8")
    assert run_orprem.main(["score", "--prereg", str(draft),
                            "--v7-gate", "ruling:synthetic"]) == 2
