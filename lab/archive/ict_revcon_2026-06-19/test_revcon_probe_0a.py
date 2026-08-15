"""Synthetic-fixture unit tests for revcon_probe_0a.py (Q-ICT-1H-REVCON-1 / Phase 0a).

TDD for the EXPLORATORY continuation / regime-conditional probe (Q-ICT-REVCON-PLAN
sec 7 Phase 0a). EVERY fixture is hand-built in-test: NO external export is read, so
these pass with no vendor data. The probe is hypothesis-generating only (parent sec 5,
PREREG-0B); these tests pin its MEASUREMENT correctness, not any verdict.

The load-bearing guard is the same failure mode that produced M-ICT-1H-OFFSET (M-15):
the continuation direction must be the TRUE decision-bar complement of reversion (not a
forward-index inversion), and the regime label (efficiency ratio) must be
decision-time-observable (no look-ahead).

Run directly (the repo default `pytest tests/` does NOT collect lab/):
    python -m pytest lab/analysis/ict_revcon_2026-06-19/test_revcon_probe_0a.py -q
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_CASCADE = _HERE.parent / "ict_cascade_2026-06-18"
sys.path.insert(0, str(_CASCADE))
sys.path.insert(0, str(_HERE))
import revcon_probe_0a as P  # noqa: E402
import harness_1h as H  # noqa: E402
import _ict_offline as M  # noqa: E402


def approx(a, b, tol=1e-9):
    assert abs(a - b) < tol, f"{a} != {b}"


H1_MS = 3_600_000
BASE_MS = int(pd.Timestamp("2026-01-05T14:00:00Z").value // 1_000_000)  # 09:00 EST


def hour_epochs(n, start=BASE_MS, step=H1_MS):
    return np.array([start + i * step for i in range(n)], dtype="int64")


# =============================================================================
# CONTINUATION RECOMPUTE (decision-bar complement of reversion; M-15 polarity)
# =============================================================================
def test_continuation_prem_up_on_rise():
    # premium NOW (zone[i]==+1) AND price RESOLVES UP over fwd bars
    # (close[i+fwd] > close[i]) -> prem_up (continuation) at decision bar i.
    fwd = 2
    zone = np.array([1, 1, 0, 0, 0, 0], float)
    close = np.array([10, 11, 12, 13, 14, 15], float)   # rising -> continues UP
    pu, dd, sc = P.recompute_continuation(zone, close, fwd)
    assert pu[0] and pu[1] and sc[0]
    assert dd.sum() == 0
    # tail not scorable
    assert not sc[4] and not sc[5]


def test_continuation_disc_down_on_fall():
    # discount NOW (zone[i]==-1) AND price RESOLVES DOWN -> disc_down (continuation).
    fwd = 2
    zone = np.array([-1, -1, 0, 0, 0, 0], float)
    close = np.array([15, 14, 13, 12, 11, 10], float)   # falling -> continues DOWN
    pu, dd, sc = P.recompute_continuation(zone, close, fwd)
    assert dd[0] and dd[1]
    assert pu.sum() == 0


def test_continuation_is_decision_bar_complement_of_reversion():
    # On a STRICTLY MONOTONE series (no ties), every scorable premium bar is EITHER
    # reversion-down XOR continuation-up -- never both, never neither. This is the
    # explicit guard that continuation scores the genuine complement DIRECTION at the
    # SAME decision bar, not a forward-index inversion (M-ICT-1H-OFFSET).
    fwd = H.FWDK
    n = 400
    close = (np.arange(n, dtype=float) + 100.0)          # strictly rising
    zone = H.zone_series(close + 1.0, close - 1.0, close, H.LOOKN_LOCK, H.EQBAND_LOCK)
    zone = zone.astype(float)
    pd_, dd_rev, sc = H.recompute_hits(zone, close, fwd)        # reversion
    pu, dd_cont, sc2 = P.recompute_continuation(zone, close, fwd)  # continuation
    assert np.array_equal(sc, sc2)                              # same scorable set
    prem_rows = sc & (zone == 1)
    # reversion-down and continuation-up are exact complements on premium rows
    assert np.array_equal(pu[prem_rows], ~pd_[prem_rows])
    # strictly rising => premium continues up, never reverts down
    assert pu[prem_rows].all()
    assert not pd_[prem_rows].any()


def test_continuation_falling_series_premium_reverts_not_continues():
    # strictly falling -> premium bars revert DOWN, continuation-up never fires.
    fwd = H.FWDK
    n = 400
    close = (1000.0 - np.arange(n, dtype=float))         # strictly falling
    zone = H.zone_series(close + 1.0, close - 1.0, close, H.LOOKN_LOCK, H.EQBAND_LOCK)
    zone = zone.astype(float)
    pd_, _dd, sc = H.recompute_hits(zone, close, fwd)
    pu, _dc, _sc = P.recompute_continuation(zone, close, fwd)
    prem_rows = sc & (zone == 1)
    # discount-heavy falling series: premium rows may be sparse, but where present,
    # continuation-up must NOT fire (price fell) and reversion-down must.
    if prem_rows.any():
        assert not pu[prem_rows].any()
        assert pd_[prem_rows].all()


# =============================================================================
# EFFICIENCY RATIO (regime proxy; Kaufman ER, decision-time-observable)
# =============================================================================
def test_efficiency_ratio_trend_is_one():
    # constant up-step -> |net| == sum(|steps|) -> ER == 1.0 (pure trend).
    close = np.arange(20, dtype=float) * 2.0 + 100.0
    er = P.efficiency_ratio(close, look_n=5)
    # warmup (i < look_n) is NaN
    assert np.isnan(er[:5]).all()
    approx(er[5], 1.0)
    approx(er[19], 1.0)


def test_efficiency_ratio_oscillation_near_zero():
    # zig-zag that returns to the same level over look_n -> net ~ 0 -> ER ~ 0 (chop).
    close = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], float) + 100.0
    er = P.efficiency_ratio(close, look_n=4)   # even window -> net 0 at aligned bars
    # at i=8: net = |close[8]-close[4]| = 0 ; sum |steps| = 4 -> ER 0
    approx(er[8], 0.0)
    assert er[8] < 0.25


def test_efficiency_ratio_decision_time_observable():
    # ER[i] uses ONLY close[i-look_n .. i]. Mutating a FUTURE bar must not change ER[i]
    # (look-ahead guard -- the partition variable must be computable at the decision bar).
    rng = np.random.default_rng(0)
    close = 100.0 + np.cumsum(rng.normal(0, 1, 60))
    er1 = P.efficiency_ratio(close, look_n=5)
    close2 = close.copy()
    close2[40] += 100.0                          # perturb a future bar
    er2 = P.efficiency_ratio(close2, look_n=5)
    # bars strictly before the perturbation window are untouched
    assert np.allclose(er1[:35], er2[:35], equal_nan=True)
    # the perturbed bar's own ER does change (sanity that the perturbation is real)
    assert not np.isclose(er1[40], er2[40], equal_nan=True)


# =============================================================================
# UNCONDITIONAL DIRECTION RATES (reversion + continuation; complement documented)
# =============================================================================
def test_direction_rates_complement_sums_to_one_no_ties():
    # On a strictly monotone series with no ties, per zone the de-overlapped reversion
    # and continuation rates sum to 1.0 -- documenting that the UNCONDITIONAL flip is
    # the near-trivial complement (parent sec 4 / PREREG-0B note); the test is conditional.
    n = 400
    close = np.arange(n, dtype=float) + 100.0
    zone = H.zone_series(close + 1, close - 1, close, H.LOOKN_LOCK, H.EQBAND_LOCK).astype(float)
    ex = _mk_export(close, zone)
    dr = P.direction_rates(ex.zone, ex.c, H.FWDK)
    # premium has rows here (rising -> close near range top). rev_down + cont_up == 1.
    if not np.isnan(dr["reversion"]["prem"]["rate"]):
        approx(dr["reversion"]["prem"]["rate"] + dr["continuation"]["prem"]["rate"], 1.0,
               tol=1e-9)


def test_direction_rates_reports_floor_n_distinct_from_stride_n():
    # F3/F5 fix: the unconditional block must expose the FLOOR-basis effective-N (the
    # n-floor=30 gate basis, floor(N_scored/fwdK)) distinctly from stride_rate_ci's
    # greedy-kept count, so the two are never conflated under one 'n_eff' label.
    n = 400
    close = np.arange(n, dtype=float) + 100.0
    zone = H.zone_series(close + 1, close - 1, close, H.LOOKN_LOCK, H.EQBAND_LOCK).astype(float)
    dr = P.direction_rates(zone, close, H.FWDK)
    _pd, _du, sc = H.recompute_hits(zone, close, H.FWDK)
    assert dr["n_floor"]["prem"] == H.effective_n(zone, sc, 1)
    assert dr["n_floor"]["disc"] == H.effective_n(zone, sc, -1)


# =============================================================================
# REGIME-CONDITIONAL SPLIT (the load-bearing 0a probe: does direction FLIP?)
# =============================================================================
def _chop_then_trend(fwd=3, look_n=6, amp=50.0, l1=360, slope=10.0, l2=360):
    """close = [mean-reverting sine chop] ++ [steady up-ramp trend].
    Chop premium bars revert DOWN (sine top -> trough fwd bars later);
    trend premium bars continue UP (ramp). ER cleanly separates the two."""
    i1 = np.arange(l1, dtype=float)
    chop = 1000.0 + amp * np.sin(2.0 * np.pi * i1 / (2 * fwd))    # period 2*fwd
    start = chop[-1]
    trend = start + slope * (np.arange(1, l2 + 1, dtype=float))
    close = np.concatenate([chop, trend])
    return close, fwd, look_n


def test_regime_split_recovers_direction_flip():
    # MECHANISM test only: this synthetic fixture has a flip BUILT IN (chop = mean-
    # reverting premium-down ; trend = ramp premium-up) and asserts the split RECOVERS
    # that built-in flip. The fixture's direction is illustrative-of-mechanism and is NOT
    # a claim about real US500 data -- on the real 6.5-mo export the weak pattern is the
    # REVERSE (chop-prem continuation-dominant, trend-prem reversion-dominant & starved;
    # audit F4). Do not read this green test as evidence for the motivating economic story.
    close, fwd, look_n = _chop_then_trend()
    zone = H.zone_series(close + 1, close - 1, close, look_n, H.EQBAND_LOCK).astype(float)
    res = P.regime_split_rates(zone, close, look_n=look_n, er_threshold=0.5, fwd_k=fwd)
    chop = res["chop"]
    trend = res["trend"]
    # chop premium: reversion(down) beats continuation(up)
    assert chop["reversion"]["prem"]["rate"] > 0.6, chop
    assert chop["continuation"]["prem"]["rate"] < 0.4, chop
    # trend premium: continuation(up) beats reversion(down) -- the FLIP
    assert trend["continuation"]["prem"]["rate"] > 0.6, trend
    assert trend["reversion"]["prem"]["rate"] < 0.4, trend


def test_regime_split_reports_effective_n_per_bucket():
    close, fwd, look_n = _chop_then_trend()
    zone = H.zone_series(close + 1, close - 1, close, look_n, H.EQBAND_LOCK).astype(float)
    res = P.regime_split_rates(zone, close, look_n=look_n, er_threshold=0.5, fwd_k=fwd)
    for bucket in ("chop", "trend"):
        for which in ("prem", "disc"):
            assert "n_eff" in res[bucket][which]
            assert res[bucket][which]["n_eff"] >= 0


def test_regime_split_threshold_partitions_all_scorable():
    # every scorable bar lands in exactly one of {chop, trend} (NaN-ER warmup excluded).
    close, fwd, look_n = _chop_then_trend()
    zone = H.zone_series(close + 1, close - 1, close, look_n, H.EQBAND_LOCK).astype(float)
    res = P.regime_split_rates(zone, close, look_n=look_n, er_threshold=0.5, fwd_k=fwd)
    # diagnostic counts exposed for the audit: chop + trend premium scorable rows ==
    # total non-warmup scorable premium rows
    assert res["chop"]["prem"]["n_scored"] + res["trend"]["prem"]["n_scored"] == \
        res["n_scored_total"]["prem"]


# =============================================================================
# EMA + WEEKLY BIAS PROXY (explicitly a PROXY for the exported structBias)
# =============================================================================
def test_ema_constant_is_constant():
    x = np.full(10, 7.0)
    e = P.ema(x, length=4)
    assert np.allclose(e, 7.0)


def test_ema_matches_recursive_formula():
    x = np.array([1.0, 2.0, 3.0, 10.0])
    length = 3
    alpha = 2.0 / (length + 1)
    expect = [1.0]
    for v in x[1:]:
        expect.append(alpha * v + (1 - alpha) * expect[-1])
    e = P.ema(x, length=length)
    assert np.allclose(e, expect)


def test_weekly_bias_proxy_sign_and_consumable():
    # Many ET weeks of 1H bars; weekly close ramps up so the weeks sit ABOVE their EMA ->
    # bias +1. PRIOR-WEEK lag (LA-1 fix): the last anchor carries the SECOND-to-last
    # week's sign, still +1 on a rising series. The proxy must return a (epoch, val)
    # tuple H.bias_conditioned_rates consumes WITHOUT error (same interface as the real
    # structBias export). n spans many real ISO weeks (~168 consecutive hours per week),
    # so the trailing weeks have a defined +1 prior-week sign (week-0 EMA-seed sign is 0).
    n = 2000                                     # ~12 ISO weeks of hourly bars
    close = np.arange(n, dtype=float) + 100.0    # rising
    epoch = hour_epochs(n)
    wb = P.weekly_bias_proxy_ema(epoch, close, ema_len=3)
    wb_epoch, wb_val = wb
    assert len(wb_epoch) == len(wb_val)
    # prior-week sign on a rising series is still +1
    assert wb_val[-1] == 1
    # the FIRST week has no prior week -> stand-down (0), never a same-week label
    assert wb_val[0] == 0
    # consumable by the cascade harness bias join
    zone = H.zone_series(close + 1, close - 1, close, H.LOOKN_LOCK, H.EQBAND_LOCK).astype(float)
    ex = _mk_export(close, zone, epoch=epoch)
    bc = H.bias_conditioned_rates(ex, wb)
    assert "prem" in bc and "disc" in bc


def _bias_per_bar(epoch, wb):
    """Replicate H.bias_conditioned_rates' internal week-join so a test can read the
    per-bar bias label the proxy induces."""
    wb_epoch, wb_val = wb
    wk_map = {}
    for k, v in zip(H._week_key_et(wb_epoch), np.asarray(wb_val, float)):
        wk_map[k] = int(np.sign(v)) if v != 0 else 0
    bar_weeks = H._week_key_et(np.asarray(epoch))
    return np.array([wk_map.get(w, 0) for w in bar_weeks], float)


def test_weekly_bias_proxy_is_decision_time_observable():
    # LA-1 GUARD (mirrors test_efficiency_ratio_decision_time_observable for the bias
    # axis). The leak the un-lagged proxy had: a week's END-OF-WEEK close labeled that
    # same week's EARLIER (e.g. Monday) bars. Perturb a target week's CLOSING bar; under
    # the prior-week lag NO bar in that week or earlier may change label (a week's close
    # may only move LATER weeks' labels). n spans many real ISO weeks.
    n = 2000                                                  # ~12 ISO weeks of hourly bars
    close = np.arange(n, dtype=float) + 1000.0               # strictly rising -> every week +1
    epoch = hour_epochs(n)
    bar_weeks = H._week_key_et(epoch)
    mid_week = bar_weeks[n // 2]
    close_bar = max(i for i, w in enumerate(bar_weeks) if w == mid_week)   # that week's last bar
    labels1 = _bias_per_bar(epoch, P.weekly_bias_proxy_ema(epoch, close, ema_len=3))
    close2 = close.copy(); close2[close_bar] -= 1e9          # crash the week-closing bar -> sign flips
    labels2 = _bias_per_bar(epoch, P.weekly_bias_proxy_ema(epoch, close2, ema_len=3))
    same_or_earlier = np.array([w <= mid_week for w in bar_weeks])   # (year,week) lexicographic
    # no look-ahead: a week's CLOSING bar cannot move any same-week-or-earlier label
    assert np.array_equal(labels1[same_or_earlier], labels2[same_or_earlier])
    # sanity: the perturbation is real -- a LATER week's label DID move (forward only)
    assert not np.array_equal(labels1, labels2)


# =============================================================================
# ORCHESTRATOR (skip-clean + returns the exploratory dict)
# =============================================================================
def _mk_export(close, zone, epoch=None):
    close = np.asarray(close, float)
    n = len(close)
    if epoch is None:
        epoch = hour_epochs(n)
    hh, _mm, _dow, date = M.et_fields(epoch)
    return H.HourExport(
        epoch_ms=epoch, o=close, h=close + 1, l=close - 1, c=close,
        zone=np.asarray(zone, float), eq=close,
        prem_hit=np.zeros(n), disc_hit=np.zeros(n),
        zone_gate=np.asarray(zone, float), zone_agree=np.ones(n),
        et_hour=hh, et_date=date, n=n,
    )


def test_run_probe_skips_when_absent(tmp_path, capsys):
    res = P.run_probe_0a(hour_csv=str(tmp_path / "nope.csv"))
    assert res is None
    out = capsys.readouterr().out
    assert "[SKIP]" in out


def test_run_probe_returns_exploratory_dict(tmp_path):
    close, fwd, look_n = _chop_then_trend()
    zone = H.zone_series(close + 1, close - 1, close, H.LOOKN_LOCK, H.EQBAND_LOCK).astype(float)
    n = len(close)
    df = pd.DataFrame({
        "time": hour_epochs(n), "open": close, "high": close + 1, "low": close - 1,
        "close": close, "zone": zone, "eq": close,
        "premHit": np.zeros(n), "discHit": np.zeros(n),
        "zoneGate": zone, "zoneAgree": np.ones(n),
    })
    p = tmp_path / "h.csv"
    df.to_csv(p, index=False)
    res = P.run_probe_0a(hour_csv=str(p), er_thresholds=(0.3, 0.5), ema_len=3)
    assert res is not None
    assert res["exploratory"] is True            # never a verdict
    assert "unconditional" in res
    assert "regime" in res and 0.3 in res["regime"] and 0.5 in res["regime"]
    assert "bias_proxy" in res


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            import inspect
            params = inspect.signature(fn).parameters
            kwargs = {}
            if "tmp_path" in params:
                import tempfile
                kwargs["tmp_path"] = Path(tempfile.mkdtemp())
            if "capsys" in params:
                continue
            fn(**kwargs)
            print(f"PASS {fn.__name__}"); passed += 1
        except AssertionError as ex:
            print(f"FAIL {fn.__name__}: {ex}")
        except Exception as ex:
            print(f"ERROR {fn.__name__}: {type(ex).__name__}: {ex}")
    print(f"\n{passed} passed (capsys tests skipped in direct-run mode)")
