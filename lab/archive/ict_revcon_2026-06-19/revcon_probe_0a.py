"""Q-ICT-1H-REVCON-1 / Phase 0a -- EXPLORATORY continuation / regime-conditional probe.

THIS IS NOT A VERDICT INSTRUMENT. Per Q-ICT-REVCON-PLAN sec 5 and PREREG-0B, Phase 0a
runs on the EXISTING 6.5-month `PEPPERSTONE_US500, 60_a6b6b.csv` -- the exact data that
already produced the 1H reversion FALSIFIED. A second hypothesis (continuation /
regime-conditional follow-through) scored on that same data is HYPOTHESIS-GENERATING
only; it may NOT be read as confirmation. The confirmatory run is Phase 0b on a fresh
multi-regime export, pre-registered (PREREG-0B) before scoring. `run_probe_0a` stamps
every result `exploratory=True` so the output cannot be mistaken for a gate.

WHAT IT MEASURES (the genuinely NEW surface -- parent sec 2):
  Unconditionally, continuation ~= 1 - reversion - ties, so the UNCONDITIONAL direction
  flip is near-trivial (documented, not the test). The real question is CONDITIONAL:
  does the WINNING follow-through direction FLIP across a decision-time-observable
  regime partition (premium reverts DOWN in chop but continues UP in trend)?

FAITHFULNESS (M-ICT-1H-OFFSET / M-15 is the load-bearing prior):
  * reversion is the cascade's M-15-fixed decision-bar `recompute_hits` (REUSED, not
    re-ported) -- premium->down = (zone[i]==+1) AND (close[i+fwd_k] < close[i]).
  * continuation here is its TRUE decision-bar complement DIRECTION (same bar i, same
    forward window, inequality flipped) -- NOT a forward-index inversion. The unit test
    test_continuation_is_decision_bar_complement_of_reversion pins this against the
    M-15 failure mode.
  * the regime label (Kaufman efficiency ratio over lookN) is DECISION-TIME-OBSERVABLE
    (uses only close[i-lookN .. i]); test_efficiency_ratio_decision_time_observable is
    the look-ahead guard. A hindsight regime label is forbidden (parent sec 5).

REUSED from the cascade harness (do NOT re-port): H.recompute_hits, H.stride_rate_ci
(de-overlap by fwdK), H.zone_series, H.bias_conditioned_rates, H._week_key_et,
H.load_hour_export, H.FWDK / LOOKN_LOCK / EQBAND_LOCK. The cascade harness_1h.py is
left BYTE-IDENTICAL (it is a committed verdict artifact for the CLOSED cascade).

BIAS NOTE: the weekly structBias column was a transient input, not committed, and the
W-layer Pine computes it (EMA-20 + structure), not this script. `weekly_bias_proxy_ema`
is an EXPLICIT close-vs-weekly-EMA PROXY, faithfulness-unverified vs the real exported
`structBias`. It applies a PRIOR-WEEK lag (a week's bars carry the previous closed week's
sign) so the label is DECISION-TIME-OBSERVABLE, mirroring the live gate's gateBias[1] /
ta.ema(..)[1] convention (LA-1 fix; the un-lagged form labeled a week's Monday bars with
that week's Friday close -- a look-ahead). Phase 0b's bias partition (PREREG-0B partition
#1) MUST use the real exported column joined with the SAME [1]-lag, not this proxy.

Run the unit tests (synthetic, no vendor data):
  python -m pytest lab/analysis/ict_revcon_2026-06-19/test_revcon_probe_0a.py -q
Run the exploratory probe on the real export:
  python lab/analysis/ict_revcon_2026-06-19/revcon_probe_0a.py \
      --hour-csv "C:/Users/joshu/Downloads/PEPPERSTONE_US500, 60_a6b6b.csv"
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_CASCADE = _HERE.parent / "ict_cascade_2026-06-18"
sys.path.insert(0, str(_CASCADE))
sys.path.insert(0, str(_HERE))
import harness_1h as H  # noqa: E402  (REUSE the M-15-fixed verdict primitives)
import _ict_offline as M  # noqa: E402  (shared detectors; do not re-port)

FWDK = H.FWDK              # 12 (measurement horizon = de-overlap unit; inherited)
LOOKN = H.LOOKN_LOCK       # 60 (PREREG-1H frozen; the ER window matches the zone window)
EQBAND = H.EQBAND_LOCK     # 0.05 (frozen)
ER_THRESHOLDS_DEFAULT = (0.30, 0.50)   # PREREG-0B proposes 0.30; 0.50 reported for sensitivity
EMALEN_DEFAULT = 20        # PREREG-0B partition #1 cites weekly EMA-20 (W emaLen invariant)


# =============================================================================
# CONTINUATION RECOMPUTE -- decision-bar complement DIRECTION of reversion
# =============================================================================
def recompute_continuation(zone, close, fwd_k=FWDK):
    """Continuation hits at the DECISION bar i (the M-15 complement of recompute_hits):
        prem_up[i]   = (zone[i]==+1) AND (close[i+fwd_k] > close[i])   # premium CONTINUES up
        disc_down[i] = (zone[i]==-1) AND (close[i+fwd_k] < close[i])   # discount CONTINUES down

    Identical indexing to H.recompute_hits (decision bar i, outcome at i+fwd_k); ONLY the
    inequality is flipped. This is the genuine complement DIRECTION, NOT the forward-index
    inversion that produced M-ICT-1H-OFFSET. Returns (prem_up, disc_down, scorable) of
    length n; the last fwd_k bars are non-scorable (0/False)."""
    zone = np.asarray(zone, float)
    close = np.asarray(close, float)
    n = len(zone)
    pu = np.zeros(n, bool)
    dd = np.zeros(n, bool)
    sc = np.zeros(n, bool)
    for i in range(n - fwd_k):
        j = i + fwd_k
        sc[i] = True
        if zone[i] == 1 and close[j] > close[i]:     # premium NOW -> price HIGHER -> continues UP
            pu[i] = True
        if zone[i] == -1 and close[j] < close[i]:    # discount NOW -> price LOWER -> continues DOWN
            dd[i] = True
    return pu, dd, sc


# =============================================================================
# EFFICIENCY RATIO -- regime proxy (Kaufman ER; decision-time-observable)
# =============================================================================
def efficiency_ratio(close, look_n):
    """Kaufman efficiency ratio over look_n bars (PREREG-0B partition #2 proposed proxy):
        ER[i] = |close[i] - close[i-look_n]| / sum_{k=i-look_n+1..i} |close[k] - close[k-1]|
    ER -> 1 in a clean trend, -> 0 in chop. DECISION-TIME-OBSERVABLE: uses only
    close[i-look_n .. i] (no future bars). Warmup (i < look_n) -> NaN. vol==0 -> ER 0."""
    close = np.asarray(close, float)
    n = len(close)
    er = np.full(n, np.nan)
    if n == 0:
        return er
    abs_steps = np.abs(np.diff(close, prepend=close[0]))   # abs_steps[k] = |c[k]-c[k-1]|, [0]=0
    csum = np.cumsum(abs_steps)
    i = np.arange(look_n, n)
    vol = csum[i] - csum[i - look_n]                        # sum |steps| over (i-look_n, i]
    net = np.abs(close[i] - close[i - look_n])
    er[i] = np.where(vol > 0, net / vol, 0.0)
    return er


# =============================================================================
# UNCONDITIONAL DIRECTION RATES (reversion + continuation; de-overlapped)
# =============================================================================
def _zone_idx(zone, scorable, target):
    return np.where(np.asarray(scorable, bool) & (np.asarray(zone, float) == target))[0]


def direction_rates(zone, close, fwd_k=FWDK):
    """De-overlapped (stride-by-fwdK) reversion AND continuation rates per zone, over the
    WHOLE series (unconditional). Returns
        {"reversion": {"prem": ci, "disc": ci}, "continuation": {"prem": ci, "disc": ci}}
    where each ci is H.stride_rate_ci(...). Unconditionally rev+cont sums to ~1 minus the
    tie fraction -- the near-trivial complement (documented; the conditional split is the
    actual test)."""
    zone = np.asarray(zone, float)
    close = np.asarray(close, float)
    p_down, d_up, sc = H.recompute_hits(zone, close, fwd_k)        # reversion
    p_up, d_down, _sc = recompute_continuation(zone, close, fwd_k)  # continuation
    pidx = _zone_idx(zone, sc, 1)
    didx = _zone_idx(zone, sc, -1)
    return {
        "reversion": {
            "prem": H.stride_rate_ci(p_down[pidx].astype(float), pidx),
            "disc": H.stride_rate_ci(d_up[didx].astype(float), didx),
        },
        "continuation": {
            "prem": H.stride_rate_ci(p_up[pidx].astype(float), pidx),
            "disc": H.stride_rate_ci(d_down[didx].astype(float), didx),
        },
        # n_floor = floor(N_scored/fwdK) = the n-floor=30 gate basis (PREREG-0B), reported
        # DISTINCTLY from stride_rate_ci's greedy-kept count (the CI sample size). The two
        # diverge when zones cluster; conflating them under one 'n_eff' label overstated
        # power ~17% on the real export (audit F3/F5).
        "n_floor": {"prem": H.effective_n(zone, sc, 1), "disc": H.effective_n(zone, sc, -1)},
    }


# =============================================================================
# REGIME-CONDITIONAL SPLIT -- the load-bearing 0a probe (does direction FLIP?)
# =============================================================================
def regime_split_rates(zone, close, look_n=LOOKN, er_threshold=0.30, fwd_k=FWDK):
    """Within each decision-time-observable regime bucket (trend: ER>=threshold ; chop:
    ER<threshold), the de-overlapped reversion AND continuation rate per zone.

    Structure (dual-nested so both the direction view and the per-zone n view are direct):
        out["chop"|"trend"]["reversion"|"continuation"]["prem"|"disc"] -> stride ci dict
        out["chop"|"trend"]["prem"|"disc"] -> {"n_scored", "n_eff"}     (per-zone power)
        out["n_scored_total"]["prem"|"disc"] -> int (non-warmup scorable rows that split)

    The regime label for a scored window is ER at the DECISION bar i (observable then).
    Warmup (NaN ER) bars are scorable but excluded from BOTH buckets, so
    chop.n_scored + trend.n_scored == n_scored_total per zone."""
    zone = np.asarray(zone, float)
    close = np.asarray(close, float)
    p_down, d_up, sc = H.recompute_hits(zone, close, fwd_k)
    p_up, d_down, _sc = recompute_continuation(zone, close, fwd_k)
    er = efficiency_ratio(close, look_n)
    valid = ~np.isnan(er)
    trend_mask = valid & (er >= er_threshold)
    chop_mask = valid & (er < er_threshold)
    hits = {"prem": (1, p_down, p_up), "disc": (-1, d_up, d_down)}  # (target, rev_hit, cont_hit)
    out = {}
    for name, rmask in (("chop", chop_mask), ("trend", trend_mask)):
        bucket = {"reversion": {}, "continuation": {}}
        for which, (target, rev_hit, cont_hit) in hits.items():
            idx = np.where(sc & (zone == target) & rmask)[0]
            bucket["reversion"][which] = H.stride_rate_ci(rev_hit[idx].astype(float), idx)
            bucket["continuation"][which] = H.stride_rate_ci(cont_hit[idx].astype(float), idx)
            bucket[which] = {"n_scored": int(len(idx)), "n_eff": int(len(idx) // fwd_k)}
        out[name] = bucket
    out["n_scored_total"] = {
        "prem": int(np.sum(sc & (zone == 1) & valid)),
        "disc": int(np.sum(sc & (zone == -1) & valid)),
    }
    out["er_threshold"] = er_threshold
    out["look_n"] = look_n
    return out


# =============================================================================
# EMA + WEEKLY BIAS PROXY (EXPLICIT proxy for the exported structBias)
# =============================================================================
def ema(x, length):
    """Standard exponential moving average, alpha = 2/(length+1), seeded at x[0]."""
    x = np.asarray(x, float)
    n = len(x)
    e = np.empty(n)
    if n == 0:
        return e
    alpha = 2.0 / (length + 1.0)
    e[0] = x[0]
    for i in range(1, n):
        e[i] = alpha * x[i] + (1.0 - alpha) * e[i - 1]
    return e


def weekly_bias_proxy_ema(epoch_ms, close, ema_len=EMALEN_DEFAULT):
    """PROXY ONLY (NOT the exported structBias): collapse the 1H closes to ET-week last
    close, EMA-`ema_len` the weekly series, take sign(weekly_close - weekly_ema), and
    apply a PRIOR-WEEK lag so a week's bars carry the sign of the previous (fully-closed)
    week. Returns (wb_epoch, wb_val) -- the SAME tuple interface H.bias_conditioned_rates
    consumes.

    DECISION-TIME-OBSERVABILITY (LA-1 fix): the prior-week lag mirrors the live gate's
    convention (W-layer scores gateBias[1]; the 1M gate reads ta.ema(close, wEmaLen)[1]),
    so the bias label at a 1H decision bar uses ONLY the prior week's closed information --
    NOT that week's own end-of-week close (which would label its Monday bars with Friday's
    move, a look-ahead the audit confirmed; test_weekly_bias_proxy_is_decision_time_observable
    is the guard). Week 0 has no prior -> stand-down (0).

    FAITHFULNESS is still UNVERIFIED vs the real Pine structBias (EMA-20 + market
    structure); Phase 0b uses the real exported column joined with the SAME [1]-lag
    (PREREG-0B partition #1)."""
    epoch_ms = np.asarray(epoch_ms)
    close = np.asarray(close, float)
    wk = H._week_key_et(epoch_ms)
    week_order = []
    last_close = {}
    last_epoch = {}
    for k, t, c in zip(wk, epoch_ms, close):
        if k not in last_close:
            week_order.append(k)
        last_close[k] = float(c)        # overwrite -> last (chronological) close of the week
        last_epoch[k] = int(t)
    wclose = np.array([last_close[k] for k in week_order], float)
    wepoch = np.array([last_epoch[k] for k in week_order], dtype="int64")
    we = ema(wclose, ema_len)
    sign = np.sign(wclose - we).astype(float)
    # PRIOR-week lag: week_order[k]'s anchor carries the sign of week_order[k-1]. Week 0
    # stands down (no prior). Without this, the end-of-week close labels its own earlier
    # decision bars (a within-week look-ahead -- audit LA-1).
    lagged = np.empty_like(sign)
    if len(lagged):
        lagged[0] = 0.0
        lagged[1:] = sign[:-1]
    return (wepoch, lagged)


# =============================================================================
# ORCHESTRATOR (exploratory; skip-clean; never a verdict)
# =============================================================================
DEFAULT_HOUR_CSV = "ict_1h_premium_discount_export.csv"


def _fmt(x):
    return "  nan" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.4f}"


def run_probe_0a(hour_csv=None, er_thresholds=ER_THRESHOLDS_DEFAULT,
                 ema_len=EMALEN_DEFAULT):
    """Run the EXPLORATORY 0a probe on a 1H indicator export. Returns a dict stamped
    exploratory=True (or None if the export is absent). NEVER a verdict (parent sec 5)."""
    path = Path(hour_csv) if hour_csv else (_HERE / DEFAULT_HOUR_CSV)
    if not path.exists():
        print("[SKIP] 1H export not found -- Phase 0a needs the existing "
              "`PEPPERSTONE_US500, 60_a6b6b.csv` (the 6.5-mo cascade export of record).")
        print(f"       expected at: {path}")
        print("       pass --hour-csv <path> (it is gitignored, lives in Downloads).")
        return None
    ex = H.load_hour_export(path)
    uncond = direction_rates(ex.zone, ex.c, FWDK)
    regime = {thr: regime_split_rates(ex.zone, ex.c, LOOKN, thr, FWDK)
              for thr in er_thresholds}
    wb = weekly_bias_proxy_ema(ex.epoch_ms, ex.c, ema_len)
    bias_proxy = H.bias_conditioned_rates(ex, wb)
    res = {
        "exploratory": True,
        "n_bars": int(ex.n),
        "unconditional": uncond,
        "regime": regime,
        "bias_proxy": bias_proxy,
        "bias_proxy_note": ("close-vs-weekly-EMA proxy with PRIOR-week lag "
                            "(decision-time-observable, LA-1); NOT the exported structBias "
                            "(faithfulness-unverified); 0b uses the real column + same [1]-lag"),
    }
    print_report_0a(res)
    return res


def print_report_0a(res):
    print("=" * 74)
    print("Q-ICT-1H-REVCON-1 / Phase 0a -- EXPLORATORY probe (NOT a verdict)")
    print("  hypothesis-generating only; scored on the data that already produced the")
    print("  1H reversion FALSIFIED. Confirmatory evidence = Phase 0b (PREREG-0B).")
    print("=" * 74)
    print(f"bars: {res['n_bars']}")
    u = res["unconditional"]
    nf = u["n_floor"]
    print("\n[UNCONDITIONAL] de-overlapped (stride=fwdK) rates -- rev+cont ~ 1 (trivial):")
    print("  (n_ci = stride-CI sample size; n_floor = floor(N/fwdK) = the n-floor=30 gate basis)")
    for z in ("prem", "disc"):
        rv = u["reversion"][z]
        ct = u["continuation"][z]
        print(f"  {z}: reversion rate={_fmt(rv['rate'])}  continuation rate={_fmt(ct['rate'])}  "
              f"(n_ci={rv['n_eff']} n_floor={nf[z]})")
    print("\n[REGIME-CONDITIONAL] the actual probe -- does the winning direction FLIP?")
    for thr, rs in res["regime"].items():
        print(f"  ER threshold {thr} (look_n={rs['look_n']}):")
        for bucket in ("chop", "trend"):
            b = rs[bucket]
            for z in ("prem", "disc"):
                rv = b["reversion"][z]["rate"]
                ct = b["continuation"][z]["rate"]
                neff = b[z]["n_eff"]
                # blank the win= word when the bucket is below the n-floor (audit F6): a
                # starved cell's extreme rate must not read as the strongest signal.
                if neff < H.N_FLOOR:
                    win = "--"
                elif not np.isnan(rv) and not np.isnan(ct):
                    win = "rev" if rv > ct else "cont"
                else:
                    win = "n/a"
                starved = " STARVED" if neff < H.N_FLOOR else ""
                print(f"    {bucket:5s} {z}: rev={_fmt(rv)} cont={_fmt(ct)} "
                      f"win={win:4s} (n_floor={neff}{starved})")
        tot = rs["n_scored_total"]
        print(f"    n_scored_total: prem={tot['prem']} disc={tot['disc']}")
    bp = res["bias_proxy"]
    print(f"\n[BIAS PROXY] {res['bias_proxy_note']}")
    print(f"  prem|bias+1={_fmt(bp['prem'].get(1))} prem|bias-1={_fmt(bp['prem'].get(-1))} "
          f"disc|bias+1={_fmt(bp['disc'].get(1))} disc|bias-1={_fmt(bp['disc'].get(-1))}")
    print("=" * 74)
    print("EXPLORATORY -- generates the PREREG-0B partition hypothesis; NOT confirmation.")
    print("=" * 74)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Q-ICT-1H-REVCON-1 Phase 0a exploratory probe")
    ap.add_argument("--hour-csv", default=None)
    ap.add_argument("--ema-len", type=int, default=EMALEN_DEFAULT)
    args = ap.parse_args()
    run_probe_0a(hour_csv=args.hour_csv, ema_len=args.ema_len)
