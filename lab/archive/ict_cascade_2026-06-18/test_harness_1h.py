"""Synthetic-fixture unit tests for harness_1h.py (Q-ICT-CASCADE-1 / LAYER 1H).

TDD for PREREG-1H. Every fixture is hand-built in-test: NO external export is read,
so these pass NOW with no vendor data (the operator has not run TV yet). The harness
main() is the only path that touches a real CSV and it SKIPs cleanly when absent.

Run directly (the repo default `pytest tests/` does NOT collect lab/):
    python -m pytest lab/analysis/ict_cascade_2026-06-18/test_harness_1h.py -q
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness_1h as H  # noqa: E402
import _ict_offline as M  # noqa: E402


def approx(a, b, tol=1e-9):
    assert abs(a - b) < tol, f"{a} != {b}"


# epoch helpers: 1H bars start 2026-01-05 (Mon) 09:00 ET, +1h each (UTC epoch ms).
H1_MS = 3_600_000
BASE_MS = int(pd.Timestamp("2026-01-05T14:00:00Z").value // 1_000_000)  # 09:00 EST


def hour_epochs(n, start=BASE_MS, step=H1_MS):
    return np.array([start + i * step for i in range(n)], dtype="int64")


def make_hour_export(o, h, l, c, zone, zone_gate=None, prem_hit=None, disc_hit=None,
                     eq=None, zone_agree=None, epoch=None):
    n = len(c)
    o = np.asarray(o, float); h = np.asarray(h, float)
    l = np.asarray(l, float); c = np.asarray(c, float)
    zone = np.asarray(zone, float)
    if zone_gate is None:
        zone_gate = zone.copy()
    if eq is None:
        eq = (h + l) / 2.0
    if prem_hit is None or disc_hit is None:
        # exported columns simulate TV's RESOLUTION-bar premHit/discHit (Pine DRAFT
        # L81-86) -- what audit_exported_hits validates against (M-ICT-1H-OFFSET).
        ph, dh, _sc = H._pine_resolution_hits(zone, c, H.FWDK)
        prem_hit = ph.astype(float) if prem_hit is None else np.asarray(prem_hit, float)
        disc_hit = dh.astype(float) if disc_hit is None else np.asarray(disc_hit, float)
    if zone_agree is None:
        zone_agree = (np.sign(zone) == np.sign(zone_gate)).astype(float)
    if epoch is None:
        epoch = hour_epochs(n)
    hh, _mm, _dow, date = M.et_fields(epoch)
    return H.HourExport(
        epoch_ms=epoch, o=o, h=h, l=l, c=c, zone=zone, eq=np.asarray(eq, float),
        prem_hit=np.asarray(prem_hit, float), disc_hit=np.asarray(disc_hit, float),
        zone_gate=np.asarray(zone_gate, float), zone_agree=np.asarray(zone_agree, float),
        et_hour=hh, et_date=date, n=n,
    )


# =============================================================================
# HIT RECOMPUTATION (DRAFT L81-86 polarity + look-ahead offset)
# =============================================================================
def test_recompute_hits_prem_down():
    # DECISION-bar form (M-ICT-1H-OFFSET fix): premium NOW (zone[i]==+1) AND price
    # RESOLVES DOWN over fwd bars (close[i+fwd] < close[i]) -> premHit at decision bar i.
    fwd = 2
    zone = np.array([1, 1, 0, 0, 0, 0], float)   # premium at the DECISION bars 0,1
    close = np.array([15, 14, 13, 12, 11, 10], float)   # falling -> resolves DOWN
    prem, disc, sc = H.recompute_hits(zone, close, fwd)
    # i=0: zone[0]=1, close[2]=13 < close[0]=15 -> premium resolved down -> premHit
    assert prem[0] and sc[0]
    # i=1: zone[1]=1, close[3]=12 < close[1]=14 -> premHit
    assert prem[1]
    # tail (i>=4): not scorable (no forward window)
    assert not sc[4] and not sc[5]
    assert disc.sum() == 0


def test_recompute_hits_disc_up():
    # discount NOW (zone[i]==-1) AND price RESOLVES UP over fwd bars
    # (close[i+fwd] > close[i]) -> discHit at decision bar i. Rising close.
    fwd = 2
    zone = np.array([-1, -1, 0, 0, 0, 0], float)
    close = np.array([10, 11, 12, 13, 14, 15], float)   # rising -> resolves UP
    prem, disc, sc = H.recompute_hits(zone, close, fwd)
    # i=0: zone[0]=-1, close[2]=12 > close[0]=10 -> discount resolved up -> discHit
    assert disc[0] and disc[1]
    assert prem.sum() == 0


def test_recompute_hits_no_hit_wrong_direction():
    # premium NOW but price ROSE (continuation, not the claimed reversion) -> NO premHit.
    # This is the polarity the pre-fix forward-index code WRONGLY counted as a hit.
    fwd = 2
    zone = np.array([1, 1, 0, 0], float)
    close = np.array([10, 11, 12, 13], float)   # rising after premium
    prem, disc, sc = H.recompute_hits(zone, close, fwd)
    # i=0: zone[0]=1 premium, close[2]=12 < close[0]=10? NO (rose) -> not premHit
    assert not prem[0]
    # the claim direction (falling after premium) DOES fire:
    close2 = np.array([13, 12, 10, 9], float)
    prem2, _, _ = H.recompute_hits(zone, close2, fwd)
    assert prem2[0]   # zone[0]=1, close[2]=10 < close[0]=13 -> premium resolved down


def test_recompute_hits_scores_event_not_complement():
    # M-ICT-1H-OFFSET regression guard. Mean-reverting series, period = 2*fwd, so every
    # premium bar's close[i+fwd] is its mirror BELOW it -> premium->down ~1.0; discount
    # ->up ~1.0. The PRE-FIX forward-index bug scored "price ROSE into a future premium
    # zone" -> the COMPLEMENT (~0). This guard fails loudly if the inversion returns.
    fwd = H.FWDK
    n = 600
    i = np.arange(n, dtype=float)
    close = 1000.0 + 50.0 * np.sin(2.0 * np.pi * i / (2 * fwd))
    zone = H.zone_series(close + 1.0, close - 1.0, close,
                         H.LOOKN_LOCK, H.EQBAND_LOCK).astype(float)
    prem, disc, sc = H.recompute_hits(zone, close, fwd)
    pv, dv, _pidx, _didx = H._zone_hit_vectors(zone, prem, disc, sc)
    assert pv.mean() > 0.9, pv.mean()    # premium resolves DOWN (the claim), NOT <0.1
    assert dv.mean() > 0.9, dv.mean()    # discount resolves UP
    # the resolution-bar reproduction (export form) scores the IDENTICAL event:
    pr, _dr, scr = H._pine_resolution_hits(zone, close, fwd)
    zlag = np.concatenate([np.full(fwd, np.nan), zone[:-fwd]])
    approx(pr[scr & (zlag == 1)].mean(), pv.mean(), tol=0.05)


def test_audit_exported_hits_exact_match():
    zone = np.array([1, 1, 1, -1, -1, -1, 0, 0], float)
    close = np.array([10, 11, 9, 8, 12, 7, 5, 6], float)
    # exported columns simulate TV's resolution-bar premHit/discHit (Pine DRAFT L81-86)
    ph2, dh2, _ = H._pine_resolution_hits(zone, close, 2)
    ex = make_hour_export(np.zeros(8), np.ones(8), np.zeros(8), close, zone,
                          prem_hit=ph2.astype(float), disc_hit=dh2.astype(float))
    # the harness audit uses FWDK=12; with only 8 bars nothing is scorable -> ok False
    res = H.audit_exported_hits(ex, fwd_k=12)
    assert res["ok"] is False and "no scorable" in res["reason"]
    # with fwd_k=2 the exported columns match the Pine reproduction exactly
    res2 = H.audit_exported_hits(ex, fwd_k=2)
    assert res2["ok"] is True
    approx(res2["prem_mismatch"], 0.0)


def test_audit_exported_hits_detects_polarity_flip():
    zone = np.array([1, 1, 1, 1, 1, 1, 1, 1], float)
    close = np.array([17, 16, 15, 14, 13, 12, 11, 10], float)  # falling -> premHits exist
    ph, dh, _ = H._pine_resolution_hits(zone, close, 2)
    # corrupt exported premHit (flip all) -> audit must FAIL (mismatch > 0)
    ex = make_hour_export(np.zeros(8), np.ones(8), np.zeros(8), close, zone,
                          prem_hit=(1 - ph).astype(float), disc_hit=dh.astype(float))
    res = H.audit_exported_hits(ex, fwd_k=2)
    assert res["ok"] is False
    assert res["prem_mismatch"] > 0.0


# =============================================================================
# ZONE RECOMPUTATION from OHLC (anchor sweep cells; uses _ict_offline.pd_zone)
# =============================================================================
def test_zone_series_matches_pd_zone():
    # constant range so pd_zone is easy to verify. close above eq -> premium.
    n = 10
    high = np.full(n, 100.0)
    low = np.full(n, 0.0)
    close = np.array([60, 60, 60, 60, 60, 40, 40, 40, 40, 40], float)
    z = H.zone_series(high, low, close, look_n=3, eq_band=0.05)
    # warmup (first 2) -> 0; bar2 onward: range max=100 min=0 eq=50 band=2.5
    assert z[0] == 0 and z[1] == 0
    assert z[2] == 1     # 60 > 52.5 -> premium
    assert z[7] == -1    # 40 < 47.5 -> discount


def test_gate_zone_is_lagged():
    # gate zone uses highest/lowest [1]-lagged (exclude current bar). A fresh new high
    # printed on the CURRENT bar must NOT enter the gate range until the next bar, so
    # the native (includes current) and lagged-gate zones differ on that bar.
    # look_n=2, eqBand=0. At bar3:
    #   native range over bars[2,3] = max(high2,high3); lagged over bars[1,2].
    n = 6
    high = np.array([10, 10, 10, 100, 100, 100], float)  # new high at bar3
    low = np.full(n, 0.0)
    # close chosen so the zone SIGN flips between native and lagged at bar3:
    #   native bar3: range[2,3]=max(10,100)=100, eq=50, close=40 -> discount (-1)
    #   lagged bar3: range[1,2]=max(10,10)=10,  eq=5,  close=40 -> premium  (+1)
    close = np.array([5, 5, 5, 40, 60, 60], float)
    zg = H.gate_zone_series(high, low, close, look_n=2, eq_band=0.0)
    zn = H.zone_series(high, low, close, look_n=2, eq_band=0.0)
    assert zn[3] == -1, (zn.tolist(),)   # native sees the fresh 100 high
    assert zg[3] == 1, (zg.tolist(),)    # lagged gate does NOT yet -> different sign
    assert zn[3] != zg[3]                # the [1]-lag is real and load-bearing


# =============================================================================
# STRIDE DE-OVERLAP CI
# =============================================================================
def test_stride_keeps_one_per_stride():
    # bar indices 0..47, stride 12 -> keep 0,12,24,36 = 4 windows.
    hit = np.ones(48, float)
    idx = np.arange(48)
    res = H.stride_rate_ci(hit, idx, stride=12)
    assert res["n_eff"] == 4
    approx(res["rate"], 1.0)


def test_stride_ci_clears_when_high_rate():
    # 40 independent windows all hits -> rate 1.0, CI clears 0.5+2pp.
    hit = np.ones(40 * 12, float)
    idx = np.arange(40 * 12)
    res = H.stride_rate_ci(hit, idx, stride=12)
    assert res["n_eff"] == 40
    assert res["clears"] is True


def test_stride_ci_does_not_clear_at_coinflip():
    rng = np.random.default_rng(0)
    n = 60 * 12
    hit = rng.integers(0, 2, size=n).astype(float)   # ~0.5
    idx = np.arange(n)
    res = H.stride_rate_ci(hit, idx, stride=12)
    assert res["clears"] is False   # coin flip cannot clear 0.5 by 2pp


def test_stride_empty():
    res = H.stride_rate_ci(np.array([]), np.array([]), stride=12)
    assert res["n_eff"] == 0 and not res["clears"]


# =============================================================================
# BLOCK BOOTSTRAP CI (delegates to _ict_offline; clears on a strong rate)
# =============================================================================
def test_block_ci_clears_on_strong_rate():
    hit = np.array([1.0] * 90 + [0.0] * 10)   # rate 0.90
    res = H.block_rate_ci(hit, block_len=12, B=3000, seed=1)
    assert res["rate"] == 0.90
    assert res["clears"] is True


def test_block_ci_coinflip_no_clear():
    rng = np.random.default_rng(2)
    hit = rng.integers(0, 2, size=400).astype(float)
    res = H.block_rate_ci(hit, block_len=12, B=2000, seed=3)
    assert res["clears"] is False


# =============================================================================
# EFFECTIVE-N (floor basis)
# =============================================================================
def test_effective_n_floor_division():
    # 30 premium scorable rows / fwdK 12 -> 2 effective windows.
    zone = np.array([1] * 30 + [-1] * 24, float)
    sc = np.ones(len(zone), bool)
    assert H.effective_n(zone, sc, 1, fwd_k=12) == 2    # 30//12
    assert H.effective_n(zone, sc, -1, fwd_k=12) == 2   # 24//12


# =============================================================================
# PLACEBO
# =============================================================================
def test_placebo_random_eq_returns_base_rate():
    # If EVERY scorable row is a hit, any random-EQ label assignment also hits at the
    # SAME base frequency -> placebo rate == 1.0 (the regression-to-range floor is the
    # ceiling here, so the real rate cannot beat it -> 1H-E5 confound exposed).
    n = 60
    zone = np.array([1] * 30 + [-1] * 30, float)
    close = np.arange(n, 0, -1).astype(float)  # arbitrary
    prem = np.ones(n, float)
    disc = np.ones(n, float)
    sc = np.ones(n, bool)
    pf = H.placebo_random_eq(zone, prem, disc, sc, "prem", B=200)
    approx(pf, 1.0)


def test_placebo_floor_takes_higher():
    # craft so random_eq > sign_shuffle, floor must equal random_eq.
    n = 48
    zone = np.array(([1] * 24) + ([-1] * 24), float)
    close = np.linspace(100, 50, n)
    prem = np.zeros(n, float); prem[:24] = 1.0   # all premium rows hit
    disc = np.zeros(n, float)
    sc = np.ones(n, bool)
    fl = H.placebo_floor(zone, close, prem, disc, sc, "prem")
    assert not np.isnan(fl["floor"])
    assert fl["floor"] >= max(v for v in (fl["random_eq"], fl["sign_shuffle"])
                              if not np.isnan(v)) - 1e-9


# =============================================================================
# ANCHOR SWEEP + PENALTY
# =============================================================================
def test_anchor_sweep_has_nine_cells():
    n = 200
    rng = np.random.default_rng(0)
    close = np.cumsum(rng.normal(0, 1, n)) + 100
    high = close + 1.0
    low = close - 1.0
    ex = make_hour_export(close, high, low, close,
                          zone=H.zone_series(high, low, close, 60, 0.05))
    cells = H.anchor_sweep(ex, "prem")
    assert len(cells) == 9
    looks = sorted({c["look_n"] for c in cells})
    bands = sorted({c["eq_band"] for c in cells})
    assert looks == [40, 60, 80]
    assert bands == [0.0, 0.05, 0.10]
    # each cell reports n-per-cell (eqBand is an n-throttle, 1H-E6)
    assert all("n_eff" in c for c in cells)


def test_penalty_rejects_coinflip_winner():
    # all cells near 0.5 -> winner must FAIL the deflated max-stat penalty.
    cells = [{"look_n": L, "eq_band": b, "which": "prem", "rate": 0.50 + 0.001,
              "n_eff": 40, "stride": {"ci_lo": 0.45, "ci_hi": 0.56, "clears": False}}
             for L in (40, 60, 80) for b in (0.0, 0.05, 0.10)]
    pen = H.deflated_max_stat_penalty(cells)
    assert pen["pass_dsr"] is False


def test_penalty_passes_strong_winner():
    cells = []
    for L in (40, 60, 80):
        for b in (0.0, 0.05, 0.10):
            rate = 0.51
            ci_lo = 0.49
            if L == 60 and b == 0.05:
                rate, ci_lo = 0.85, 0.75    # strong, tight CI
            cells.append({"look_n": L, "eq_band": b, "which": "prem", "rate": rate,
                          "n_eff": 60,
                          "stride": {"ci_lo": ci_lo, "ci_hi": min(rate + 0.1, 1.0),
                                     "clears": ci_lo > 0.52}})
    pen = H.deflated_max_stat_penalty(cells)
    assert pen["winner"]["look_n"] == 60 and pen["winner"]["eq_band"] == 0.05
    assert pen["pass_dsr"] is True


# =============================================================================
# TRANSFER PRE-GATE
# =============================================================================
def test_transfer_range_lag_clears_when_identical():
    # zone == zone_gate exactly -> 100% agreement, 0 gap -> clears.
    n = 200
    rng = np.random.default_rng(1)
    zone = rng.choice([-1, 0, 1], size=n).astype(float)
    close = np.cumsum(rng.normal(0, 1, n)) + 100
    ex = make_hour_export(close, close + 1, close - 1, close, zone, zone_gate=zone)
    r = H.transfer_range_lag_axis(ex)
    approx(r["agree"], 1.0)
    assert r["clears"] is True


def test_transfer_range_lag_rejects_on_disagreement():
    # zone_gate = -zone on directional rows -> ~0% agreement -> REJECT.
    n = 200
    rng = np.random.default_rng(2)
    zone = rng.choice([-1, 1], size=n).astype(float)
    close = np.cumsum(rng.normal(0, 1, n)) + 100
    ex = make_hour_export(close, close + 1, close - 1, close, zone, zone_gate=-zone)
    r = H.transfer_range_lag_axis(ex)
    assert r["agree"] < 0.10
    assert r["clears"] is False


def test_sign_agreement_raw_equality_counts_eq_eq():
    # FINDING 1H-CRITICAL: Pine agreeRate counts agreement over ALL confirmed
    # valid&gateValid bars and treats 0==0 (EQ==EQ) as AGREE, while a 0-vs-nonzero
    # row is a DISAGREE that STAYS in the denominator. The restrict_nonzero=False
    # path must reproduce that raw-equality semantic exactly.
    #   za/zb: 2 rows 0==0 (agree), 1 row +1==+1 (agree), 7 rows 0 vs +1 (disagree)
    #   -> Pine agreeRate = 3/10 = 0.30 over all 10 bars.
    za = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0], float)
    zb = np.array([0, 0, 1, 1, 1, 1, 1, 1, 1, 1], float)
    agree_raw, n_raw = H._sign_agreement(za, zb, restrict_nonzero=False)
    assert n_raw == 10              # denominator = ALL bars, EQ rows NOT dropped
    approx(agree_raw, 0.30)         # 3 of 10 agree (incl. the two 0==0 rows)
    # the OLD (buggy) restrict_nonzero=True path drops every 0-row from BOTH
    # numerator and denominator -> only the single +1==+1 row survives -> 100%.
    agree_nz, n_nz = H._sign_agreement(za, zb, restrict_nonzero=True)
    assert n_nz == 1
    approx(agree_nz, 1.0)           # the inflation this finding fixes


def test_transfer_range_lag_agreerate_matches_pine_with_eq_rows():
    # FINDING 1H-CRITICAL end-to-end: a fixture where EQ==EQ rows are routine and
    # zone==0 vs zoneGate!=0 rows dominate. Pine agreeRate counts 20 agree of 100
    # valid&gateValid bars -> 20% -> transfer REJECT. The buggy both-nonzero path
    # drops every EQ row and reads ~100% -> would WRONGLY clear.
    look = H.LOOKN_LOCK                       # 60 (locked)
    n_valid = 100
    n = look + n_valid                        # bars [look..n-1] are valid&gateValid
    # rising close so native + lagged-gate lookback ranges are always defined+valid
    close = np.arange(n, dtype=float) + 100.0
    high = close + 1.0
    low = close - 1.0
    zone = np.zeros(n, float)
    zone_gate = np.zeros(n, float)
    v = np.arange(look, n)                     # the 100 valid bars
    # 10 rows agree as EQ==EQ (0==0); 10 rows agree as +1==+1; 80 rows disagree
    # as zone==0 vs zoneGate==+1 (the EQ-vs-nonzero DISAGREE Pine keeps).
    zone[v[10:20]] = 1.0;  zone_gate[v[10:20]] = 1.0          # 10 agree (nonzero)
    zone_gate[v[20:]] = 1.0                                    # 80 disagree (0 vs +1)
    # rows v[0:10] stay 0/0 -> 10 agree as EQ==EQ
    ex = make_hour_export(close, high, low, close, zone, zone_gate=zone_gate)
    r = H.transfer_range_lag_axis(ex)
    approx(r["agree"], 0.20)        # Pine: 20 agree / 100 valid bars
    assert r["n_agree"] == 100      # denominator = all valid&gateValid bars
    assert r["clears"] is False     # 20% < 90% transfer floor -> REJECT


def test_transfer_pregate_rejects_when_minute_absent():
    n = 60
    zone = np.array([1, -1] * 30, float)
    close = np.arange(n, dtype=float)
    ex = make_hour_export(close, close + 1, close - 1, close, zone, zone_gate=zone)
    res = H.transfer_pregate(ex, None)   # no 1M export
    assert res["clears"] is False
    assert "1M export absent" in res["reason"]


def test_transfer_price_basis_clears_when_minute_matches():
    n = 120
    rng = np.random.default_rng(3)
    zone = rng.choice([-1, 0, 1], size=n).astype(float)
    close = np.cumsum(rng.normal(0, 1, n)) + 100
    epoch = hour_epochs(n)
    ex = make_hour_export(close, close + 1, close - 1, close, zone, zone_gate=zone,
                          epoch=epoch)
    # 1M export: same timestamps, same zone (perfect price-basis agreement)
    mn = H.MinuteExport(epoch_ms=epoch, net_bias=np.sign(zone),
                        zone=zone.copy(), in_kz=np.ones(n), close=close, n=n)
    r = H.transfer_price_basis_axis(ex, mn)
    approx(r["agree"], 1.0)
    assert r["clears"] is True


def test_transfer_price_basis_rejects_on_disagreement():
    n = 120
    rng = np.random.default_rng(4)
    zone = rng.choice([-1, 1], size=n).astype(float)
    close = np.cumsum(rng.normal(0, 1, n)) + 100
    epoch = hour_epochs(n)
    ex = make_hour_export(close, close + 1, close - 1, close, zone, zone_gate=zone,
                          epoch=epoch)
    mn = H.MinuteExport(epoch_ms=epoch, net_bias=np.sign(zone),
                        zone=-zone, in_kz=np.ones(n), close=close, n=n)  # flipped
    r = H.transfer_price_basis_axis(ex, mn)
    assert r["agree"] < 0.10
    assert r["clears"] is False


def test_transfer_price_basis_eq_inclusive_counts_disagreements():
    # ALIGN (PR #198 follow-up #1, FOLLOWUP-1H-price-basis-axis.md): the price-BASIS
    # axis must match the range-LAG axis -- EQ-inclusive raw equality over valid &
    # gateValid bars. An EQ-vs-nonzero joined row (1H directional, the 1M-basis the
    # live gate reads in EQ stand-down) is a GENUINE transfer failure and MUST stay in
    # the denominator; EQ==EQ rows count as agreement. The OLD restrict_nonzero=True
    # dropped BOTH -> read ~100% over the both-nonzero subset and FALSELY CLEARED the
    # transfer (licensing the 1M PD gate). Pin the fixed behavior.
    n = 120
    rng = np.random.default_rng(7)
    close = 100.0 + np.cumsum(rng.normal(0, 1, n))      # varied -> ranges valid on [60,120)
    # 1H native zone over the valid region [60,120): 60-89 = +1, 90-99 = 0 (EQ),
    # 100-119 = +1. Warmup bars 0-59 are excluded by the valid mask (left +1).
    zone = np.ones(n)
    zone[90:100] = 0.0
    ex = make_hour_export(close, close + 1, close - 1, close, zone, zone_gate=zone,
                          epoch=hour_epochs(n))
    # 1M gate zone: 60-89 = +1 (agree), 90-99 = 0 (EQ==EQ -> agree),
    # 100-119 = 0 (EQ-vs-nonzero -> DISAGREE; the transfer failure the old code hid).
    mzone = np.ones(n)
    mzone[90:120] = 0.0
    mn = H.MinuteExport(epoch_ms=ex.epoch_ms, net_bias=np.sign(mzone),
                        zone=mzone, in_kz=np.ones(n), close=close, n=n)
    r = H.transfer_price_basis_axis(ex, mn)
    # valid bars 60..119 = 60. agree = 30 (both +1) + 10 (both 0) = 40; disagree = 20.
    assert r["n_agree"] == 60                           # EQ rows STAYED in the denominator
    assert abs(r["agree"] - 40.0 / 60.0) < 1e-9         # 0.667, not the old 1.0 (both-nonzero only)
    assert r["clears"] is False                         # 66.7% < 90% -> correctly REJECT


# =============================================================================
# BIAS-CONDITIONED VARIANT
# =============================================================================
def test_bias_conditioned_split_by_week():
    # 24 bars in one ET week with bias=+1, then a fixture with premium hits.
    fwd = H.FWDK
    n = 40
    zone = np.array([1] * n, float)
    close = np.arange(n, dtype=float) + 100.0   # rising -> premHit fires (close<future)
    epoch = hour_epochs(n)
    ex = make_hour_export(close, close + 1, close - 1, close, zone, epoch=epoch)
    # weekly bias: a single weekly anchor inside the same ET week, value +1
    wb_epoch = np.array([epoch[0]], dtype="int64")
    wb_val = np.array([1.0])
    bc = H.bias_conditioned_rates(ex, (wb_epoch, wb_val))
    # premium under bias=+1 should be the (high) rate; under bias=-1 should be nan
    assert not np.isnan(bc["prem"][1])
    assert np.isnan(bc["prem"][-1])


# =============================================================================
# HALVES STATIONARITY
# =============================================================================
def test_halves_flip_detected():
    # first half all hits, second half all misses -> margin flips (h2 <= 0.5).
    hit = np.array([1.0] * 20 + [0.0] * 20)
    idx = np.arange(40)
    r = H.halves_margin_flip(hit, idx)
    approx(r["h1"], 1.0)
    approx(r["h2"], 0.0)
    assert r["flips"] is True


def test_halves_no_flip_when_both_high():
    hit = np.array([1.0] * 18 + [0.0] * 2 + [1.0] * 18 + [0.0] * 2)
    idx = np.arange(len(hit))
    r = H.halves_margin_flip(hit, idx)
    assert r["flips"] is False   # both halves > 0.5


# =============================================================================
# END-TO-END VERDICTS
# =============================================================================
def _strong_premium_export(n_windows=40, fwd=H.FWDK, bias_week=True):
    """Build a 1H export where BOTH premium->down and discount->up reliably clear 0.5
    AND beat the regression-to-range placebo (1H-E5), with enough effective windows.

    CORRECT premium->down semantics (M-ICT-1H-OFFSET): premium resolving DOWN is a
    MEAN-REVERTING phenomenon. (The old fixture used a premium UPTREND -- but a premium
    uptrend resolves UP, continuation; that fixture only "fired" under the inverted
    pre-fix scoring and is the WRONG shape.) So price is a mean-reverting sine with
    period = 2*fwd: a fwd-bar forward step is exactly a half-period phase flip, so EVERY
    premium bar's close[i+fwd] is its mirror BELOW it (premium->down) and every discount
    bar's mirror is ABOVE (discount->up) -> both rates ~1.0, cleanly clearing stride +
    block. zone is derived from zone_series(...,LOOKN_LOCK,EQBAND_LOCK) so the main
    verdict, the anchor sweep, and zone_gate all see the same premium/discount split
    (range-LAG transfer clears). The random-EQ placebo mixes premium+discount rows ->
    floor ~0.5 < the real ~1.0, so the real rate strictly beats the 1H-E5 confound."""
    n = max(2 * n_windows * fwd, 2400)
    period = 2 * fwd                 # half-period forward step = guaranteed phase flip
    i = np.arange(n, dtype=float)
    close = 1000.0 + 50.0 * np.sin(2.0 * np.pi * i / period)
    high = close + 1.0
    low = close - 1.0
    zone = H.zone_series(high, low, close, H.LOOKN_LOCK, H.EQBAND_LOCK).astype(float)
    epoch = hour_epochs(n)
    ex = make_hour_export(close, high, low, close, zone, zone_gate=zone, epoch=epoch)
    return ex, epoch


def _zone_aligned_weekly_bias(ex):
    """Weekly structBias dict where each ET week's bias = the dominant zone sign of the
    bars in that week. The 1M trades structBias AND PD (never PD alone, 1H-E3), so the
    gate-relevant conditional (premHit|bias=+1, discHit|bias=-1) only clears when the
    weekly bias agrees with the zone -- which is the realistic RESOLVED case."""
    wk = H._week_key_et(ex.epoch_ms)
    sums = {}
    for w, z in zip(wk, ex.zone):
        sums[w] = sums.get(w, 0.0) + z
    return {w: (1 if s >= 0 else -1) for w, s in sums.items()}


def test_verdict_resolved_when_all_gates_clear():
    ex, epoch = _strong_premium_export(40)
    n = ex.n
    # 1M export matches the 1H zone exactly -> price-BASIS axis clears too.
    mn = H.MinuteExport(epoch_ms=epoch, net_bias=np.ones(n), zone=ex.zone.copy(),
                        in_kz=np.ones(n), close=ex.c, n=n)
    # weekly bias aligned to the zone block (prem weeks +1, disc weeks -1) so the
    # gate-relevant conditional (1H-E3) clears for both candidate zones.
    weekly_bias = _zone_aligned_weekly_bias(ex)
    res = H.verdict_1h(ex, mn, weekly_bias, apply_halves_superset=True)
    assert res["verdict"] == "RESOLVED", res
    assert res["licenses_1m_gate"] is True


def test_verdict_resolved_but_licenses_nothing_on_transfer_reject():
    # Same strong premium signal, but the 1M price-basis zone DISAGREES -> transfer
    # REJECT -> RESOLVED-but-licenses-nothing (cascade-licensing rule).
    ex, epoch = _strong_premium_export(40)
    n = ex.n
    mn = H.MinuteExport(epoch_ms=epoch, net_bias=np.ones(n), zone=-ex.zone,  # flipped
                        in_kz=np.ones(n), close=ex.c, n=n)
    weekly_bias = _zone_aligned_weekly_bias(ex)
    res = H.verdict_1h(ex, mn, weekly_bias, apply_halves_superset=True)
    assert res["verdict"] == "RESOLVED"
    assert res["licenses_1m_gate"] is False
    assert "TRANSFER pre-gate REJECTS" in res["reason"]


def test_verdict_insufficient_n():
    # tiny export -> effective-N < 30 in both zones -> INSUFFICIENT-N.
    n = 50
    zone = np.array([1, -1] * 25, float)
    close = np.arange(n, dtype=float)
    ex = make_hour_export(close, close + 1, close - 1, close, zone, zone_gate=zone)
    res = H.verdict_1h(ex, None, None)
    assert res["verdict"] == "INSUFFICIENT-N"
    assert res["licenses_1m_gate"] is False


def test_verdict_falsified_on_coinflip():
    # random zone + random close -> both rates straddle 0.5 -> FALSIFIED.
    # n large enough that EACH zone clears the n-floor (>=30 eff windows = >=360
    # scorable rows / zone; with ~50/50 split need >= ~900 bars).
    rng = np.random.default_rng(7)
    n = 2000
    zone = rng.choice([-1, 1], size=n).astype(float)
    close = np.cumsum(rng.normal(0, 1, n)) + 100
    ex = make_hour_export(close, close + 1, close - 1, close, zone, zone_gate=zone)
    mn = H.MinuteExport(epoch_ms=ex.epoch_ms, net_bias=np.sign(zone),
                        zone=zone.copy(), in_kz=np.ones(n), close=close, n=n)
    wk = H._week_key_et(ex.epoch_ms)
    weekly_bias = {w: 1 for w in set(wk)}
    res = H.verdict_1h(ex, mn, weekly_bias)
    assert res["verdict"] == "FALSIFIED", res
    assert res["licenses_1m_gate"] is False


def test_verdict_ambiguous_hold_on_bias_fail():
    # Strong UNCONDITIONAL premium signal that clears, but bias-conditioned prem|+1
    # fails because the weekly bias for the spanned weeks is -1 (so prem|+1 has no rows
    # / does not clear) -> AMBIGUOUS-HOLD. We make all weeks bias=-1.
    ex, epoch = _strong_premium_export(40)
    n = ex.n
    mn = H.MinuteExport(epoch_ms=epoch, net_bias=np.ones(n), zone=ex.zone.copy(),
                        in_kz=np.ones(n), close=ex.c, n=n)
    wk = H._week_key_et(epoch)
    weekly_bias = {w: -1 for w in set(wk)}   # all weeks bias = -1
    res = H.verdict_1h(ex, mn, weekly_bias, apply_halves_superset=True)
    assert res["verdict"] == "AMBIGUOUS-HOLD", res
    assert res["licenses_1m_gate"] is False


# =============================================================================
# LOADERS + main() SKIP-CLEAN
# =============================================================================
def test_to_epoch_ms_seconds_and_ms():
    sec = pd.Series([1_700_000_000, 1_700_003_600])     # ~2023 in seconds
    ms = H._to_epoch_ms(sec)
    assert ms[0] == 1_700_000_000_000
    already_ms = pd.Series([1_700_000_000_000])
    assert H._to_epoch_ms(already_ms)[0] == 1_700_000_000_000


def test_to_epoch_ms_iso_strings():
    iso = pd.Series(["2026-01-05T14:00:00Z", "2026-01-05T15:00:00Z"])
    ms = H._to_epoch_ms(iso)
    assert ms[0] == BASE_MS


def test_load_hour_export_roundtrip(tmp_path):
    n = 30
    close = np.arange(n, dtype=float) + 100
    zone = np.array([1, -1, 0] * 10, float)
    df = pd.DataFrame({
        "time": hour_epochs(n),
        "open": close, "high": close + 1, "low": close - 1, "close": close,
        "zone": zone, "eq": (close), "premHit": np.zeros(n), "discHit": np.zeros(n),
        "zoneGate": zone, "zoneAgree": np.ones(n),
    })
    p = tmp_path / "h.csv"
    df.to_csv(p, index=False)
    ex = H.load_hour_export(p)
    assert ex.n == n
    assert np.array_equal(ex.zone, zone)
    assert ex.et_hour[0] == 9   # 14:00 UTC = 09:00 EST


def test_load_hour_export_missing_col_raises(tmp_path):
    df = pd.DataFrame({"time": [1, 2], "open": [1, 2]})
    p = tmp_path / "bad.csv"
    df.to_csv(p, index=False)
    try:
        H.load_hour_export(p)
    except ValueError as ex:
        assert "missing" in str(ex)
    else:
        raise AssertionError("expected ValueError on missing columns")


def test_main_skips_when_export_absent(tmp_path, capsys):
    res = H.main(hour_csv=str(tmp_path / "nope.csv"))
    assert res is None
    out = capsys.readouterr().out
    assert "[SKIP]" in out
    assert "has not run TV yet" in out
    assert "time, netBias, zone, inKZ, close" in out   # names the required 1M export


def test_main_runs_on_synthetic_csvs(tmp_path):
    # write a real hour + minute CSV pair and confirm main() produces a verdict.
    ex, epoch = _strong_premium_export(40)
    n = ex.n
    hdf = pd.DataFrame({
        "time": epoch, "open": ex.o, "high": ex.h, "low": ex.l, "close": ex.c,
        "zone": ex.zone, "eq": ex.eq, "premHit": ex.prem_hit, "discHit": ex.disc_hit,
        "zoneGate": ex.zone_gate, "zoneAgree": ex.zone_agree,
    })
    mdf = pd.DataFrame({
        "time": epoch, "netBias": np.ones(n), "zone": ex.zone, "inKZ": np.ones(n),
        "close": ex.c,
    })
    wk = H._week_key_et(epoch)
    # one weekly bias anchor per spanned week, sign aligned to that week's zone block
    # (prem weeks +1, disc weeks -1) so the gate-relevant conditional (1H-E3) clears.
    aligned = _zone_aligned_weekly_bias(ex)
    seen = {}
    for t, w in zip(epoch, wk):
        seen.setdefault(w, t)
    bdf = pd.DataFrame({"time": list(seen.values()),
                        "structBias": [float(aligned[w]) for w in seen]})
    hp = tmp_path / "h.csv"; mp = tmp_path / "m.csv"; bp = tmp_path / "b.csv"
    hdf.to_csv(hp, index=False); mdf.to_csv(mp, index=False); bdf.to_csv(bp, index=False)
    res = H.main(hour_csv=str(hp), min_csv=str(mp), bias_csv=str(bp))
    assert res is not None
    assert res["verdict"] in {"RESOLVED", "AMBIGUOUS-HOLD", "FALSIFIED",
                              "INSUFFICIENT-N"}
    assert res["verdict"] == "RESOLVED"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            # crude tmp_path/capsys shim for direct-run mode
            import inspect
            params = inspect.signature(fn).parameters
            kwargs = {}
            if "tmp_path" in params:
                import tempfile
                kwargs["tmp_path"] = Path(tempfile.mkdtemp())
            if "capsys" in params:
                continue  # skip capsys tests in direct-run mode
            fn(**kwargs)
            print(f"PASS {fn.__name__}"); passed += 1
        except AssertionError as ex:
            print(f"FAIL {fn.__name__}: {ex}")
        except Exception as ex:
            print(f"ERROR {fn.__name__}: {type(ex).__name__}: {ex}")
    print(f"\n{passed} passed (capsys tests skipped in direct-run mode)")
