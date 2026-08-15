"""Unit tests for harness_w.py -- LAYER W (Weekly structure-only gateHitRate).

TDD for Q-ICT-CASCADE-1 W layer. All fixtures are synthetic and built IN-TEST: NO
external TV export is touched, so these pass NOW with no vendor data. The real-export
entrypoint (run_layer_w / main) skips cleanly when the CSV is absent -- that skip
path is exercised here against a guaranteed-missing path.

Every assertion ties back to a PREREG-W frozen threshold or verdict-gate row:
  * denominator from gateScored, NEVER mean(hit)            (forbidden #3)
  * moving-block bootstrap CI, NOT binomial                 (forbidden #2)
  * block_len = autocorr_block_len(outcome) GC-1            (cutoff .10/floor 1/cap 8)
  * eff_N = nGateScored / L_W < 30 -> INSUFFICIENT-N        (GC-2, dominates FALSIFIED)
  * halves AND thirds stationarity for RESOLVED             (verdict gate)
  * AMBIGUOUS-HOLD when CI lb>0.5 but a half/third <=0.5    (verdict gate)
  * vote sub-verdict: max-stat permutation B, pre-condition (GC-3, forbidden #4)

Run directly (the repo default `pytest tests/` does NOT collect lab/):
    python -m pytest lab/analysis/ict_cascade_2026-06-18/test_harness_w.py -q
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness_w as W  # noqa: E402


# -----------------------------------------------------------------------------
# Fixture builder: a synthetic Weekly data-window export.
#
# Each row is one week. We control gateBias (the structure-only prior bias used by
# the gate), outcome (realized direction), and gateScored. The harness computes the
# hit vector from the gateHit column (script-correct) when present; we set gateHit
# consistently = (gateBias == sign(outcome)) on scored weeks so the synthetic data
# is internally coherent.
# -----------------------------------------------------------------------------
def make_export(gate_bias, outcome, gate_scored=None, *, add_live=True,
                votes=None, week0="2020-01-06"):
    """Build a DataFrame mimicking the TV data-window export.

    gate_bias  : list of structure-only bias per week (+1/-1/0).
    outcome    : list of realized direction per week (+1/-1/0).
    gate_scored: list of 0/1; default = (gate_bias!=0 AND outcome!=0).
    add_live   : append one extra (live, unconfirmed) row that MUST be dropped.
    votes      : optional dict {vStruct/vSeason/vRates/vEarn: list} for importance.
    """
    n = len(gate_bias)
    gb = np.array(gate_bias, float)
    out = np.array(outcome, float)
    if gate_scored is None:
        gs = ((gb != 0) & (out != 0)).astype(int)
    else:
        gs = np.array(gate_scored, int)
    realized = np.sign(out)
    gate_hit = np.where((gs == 1) & (np.sign(gb) == realized), 1, 0)
    hit = gate_hit.copy()  # collapsed column (the harness must NOT trust its denom)
    times = pd.date_range(week0, periods=n, freq="W").astype(str).tolist()
    data = {
        "time": times,
        "bias": gb,                 # composite (research-only); not the object
        "outcome": out,
        "vStruct": gb,
        "vSeason": np.zeros(n),
        "vRates": np.zeros(n),
        "vEarn": np.zeros(n),
        "hit": hit,
        "gateBias": gb,
        "gateHit": gate_hit,
        "gateScored": gs,
        "scored": gs,
    }
    if votes is not None:
        for k, vlist in votes.items():
            data[k] = np.array(vlist, float)
    df = pd.DataFrame(data)
    if add_live:
        # live row: unconfirmed week, gateScored arbitrary; MUST be dropped.
        live_time = pd.Timestamp(times[-1]) + pd.Timedelta(weeks=1)
        live = {c: (str(live_time) if c == "time" else 0.0) for c in df.columns}
        df = pd.concat([df, pd.DataFrame([live])], ignore_index=True)
    return df


def cols_of(df):
    return W.resolve_columns(df.columns)


# =============================================================================
# SCHEMA ADAPTER (PREREG-W CONSUMES: 1-line-rename column map)
# =============================================================================
def test_schema_adapter_resolves_canonical():
    df = make_export([1, -1, 1], [1, -1, 1], add_live=False)
    cols = cols_of(df)
    for c in W.REQUIRED_CANON:
        assert c in cols, c
    assert cols["gateScored"] == "gateScored"


def test_schema_adapter_absorbs_rename():
    # TV renamed gateScored -> gate_scored and outcome -> realized: one-line COLMAP
    # entries already cover these, so resolution must still succeed.
    df = make_export([1, -1], [1, -1], add_live=False)
    df = df.rename(columns={"gateScored": "gate_scored", "outcome": "realized"})
    cols = cols_of(df)
    assert cols["gateScored"] == "gate_scored"
    assert cols["outcome"] == "realized"


def test_load_export_missing_required_raises():
    df = make_export([1, -1], [1, -1], add_live=False).drop(columns=["gateScored", "scored"])
    cols = W.resolve_columns(df.columns)
    assert "gateScored" not in cols  # cannot resolve -> downstream load_export raises


# =============================================================================
# DE-OVERLAP + DENOMINATOR (PREREG-W forbidden #3: NEVER mean(hit))
# =============================================================================
def test_de_overlap_drops_live_and_filters_scored():
    # 4 confirmed weeks; 2 are flat (outcome 0 -> not scored). +1 live row appended.
    gb = [1, -1, 1, -1]
    out = [1, 0, 1, 0]            # weeks 0,2 scored; weeks 1,3 flat
    df = make_export(gb, out, add_live=True)
    cols = cols_of(df)
    scored, n_flat, n_live = W.de_overlap_scored(df, cols, drop_live=True)
    assert n_live == 1                      # live bar dropped
    assert len(scored) == 2                 # only the 2 directional+confirmed weeks
    assert n_flat == 2                      # the 2 flat weeks reported separately


def test_denominator_is_gatescored_not_mean_hit():
    # 10 weeks; only 4 are gateScored. Of those 4, 3 hit. Among the NON-scored weeks
    # the collapsed `hit` column is 0, so mean(hit) over ALL 10 = 3/10 = 0.30, but
    # the PREREG-correct structure rate is 3/4 = 0.75. The harness MUST report 0.75.
    gb = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    out = [1, 1, 1, -1, 0, 0, 0, 0, 0, 0]   # weeks 0-2 hit, week3 miss; rest flat
    df = make_export(gb, out, add_live=False)
    cols = cols_of(df)
    scored, _, _ = W.de_overlap_scored(df, cols, drop_live=False)
    hit_vec, n_scored, n_hit = W.structure_gate_hit_rate(scored, cols)
    assert n_scored == 4
    assert n_hit == 3
    assert abs(n_hit / n_scored - 0.75) < 1e-9
    # the mean(hit) trap would have given 0.30 -- confirm we did NOT do that:
    mean_hit_all = pd.to_numeric(df[cols["hit"]]).mean()
    assert abs(mean_hit_all - 0.30) < 1e-9
    assert abs(n_hit / n_scored - mean_hit_all) > 0.2  # demonstrably different


# =============================================================================
# BLOCK LENGTH (GC-1) is taken from the OUTCOME series, cutoff .10/floor 1/cap 8
# =============================================================================
def test_block_len_white_noise_outcome_is_floor():
    rng = np.random.default_rng(0)
    n = 400
    gb = rng.choice([-1.0, 1.0], size=n)
    out = rng.choice([-1.0, 1.0], size=n)   # iid -> autocorr ~0 -> block floor 1
    df = make_export(list(gb), list(out), add_live=False)
    cols = cols_of(df)
    v = W.evaluate_weekly(df, cols, seed=1)
    assert v.block_len == 1


def test_block_len_trending_outcome_is_longer():
    # a strongly autocorrelated outcome sign (long runs) -> block_len > 1, <= cap 8.
    out = ([1.0] * 30 + [-1.0] * 30) * 5     # 300 weeks, long runs
    gb = list(out)                           # structure tracks outcome -> high hit
    df = make_export(gb, out, add_live=False)
    cols = cols_of(df)
    v = W.evaluate_weekly(df, cols, seed=1)
    assert 1 < v.block_len <= W.BLOCK_CAP


# =============================================================================
# n-FLOOR (GC-2): eff_N = nGateScored / L_W < 30 -> INSUFFICIENT-N (dominates)
# =============================================================================
def test_insufficient_n_below_floor():
    # 20 scored weeks, white-noise outcome -> block_len 1 -> eff_N=20 < 30.
    rng = np.random.default_rng(2)
    gb = rng.choice([-1.0, 1.0], size=20)
    out = gb.copy()                          # perfect hit, but starved N
    df = make_export(list(gb), list(out), add_live=False)
    cols = cols_of(df)
    v = W.evaluate_weekly(df, cols, seed=3)
    assert v.verdict == "INSUFFICIENT-N"
    assert v.eff_n < W.N_EFF_FLOOR


def test_insufficient_n_dominates_a_straddling_ci():
    # 25 scored weeks at ~50% (a CI that straddles 0.5) but eff_N=25<30 -> the
    # verdict is INSUFFICIENT-N, NOT FALSIFIED (PREREG-W: floor dominates).
    gb = [1, -1] * 13           # 26 weeks
    out = [1, 1, -1, -1] * 6 + [1, -1]  # mixed -> ~50%
    out = out[:26]
    df = make_export(gb[:26], out, add_live=False)
    cols = cols_of(df)
    v = W.evaluate_weekly(df, cols, seed=4)
    assert v.eff_n < W.N_EFF_FLOOR
    assert v.verdict == "INSUFFICIENT-N"


# =============================================================================
# RESOLVED: CI lb>0.5 AND both halves AND all thirds >0.5 AND eff_N>=30
# =============================================================================
def test_resolved_high_stationary_rate():
    # 200 scored weeks, ~80% hit rate, evenly distributed -> all halves/thirds >0.5,
    # block CI lower bound well above 0.5, eff_N >> 30.
    rng = np.random.default_rng(7)
    n = 200
    out = rng.choice([-1.0, 1.0], size=n)
    gb = out.copy().astype(float)
    # inject 20% misses uniformly so every chrono segment stays > 0.5
    miss_idx = np.arange(0, n, 5)            # every 5th week is a miss (20%)
    gb[miss_idx] = -gb[miss_idx]
    df = make_export(list(gb), list(out), add_live=False)
    cols = cols_of(df)
    v = W.evaluate_weekly(df, cols, seed=8)
    assert v.eff_n >= W.N_EFF_FLOOR
    assert v.point_estimate > 0.5
    assert v.ci_lo > 0.5
    assert all(r > 0.5 for r in v.halves)
    assert all(r > 0.5 for r in v.thirds)
    assert v.verdict == "RESOLVED"


# =============================================================================
# FALSIFIED: CI straddles 0.5 with eff_N>=30
# =============================================================================
def test_falsified_coinflip_rate():
    # 300 scored weeks at ~50% (alternating-ish) -> CI straddles 0.5, eff_N>=30.
    rng = np.random.default_rng(11)
    n = 300
    out = rng.choice([-1.0, 1.0], size=n)
    gb = rng.choice([-1.0, 1.0], size=n)     # independent of outcome -> ~50% hit
    df = make_export(list(gb), list(out), add_live=False)
    cols = cols_of(df)
    v = W.evaluate_weekly(df, cols, seed=12)
    assert v.eff_n >= W.N_EFF_FLOOR
    assert v.ci_lo <= 0.5
    assert v.verdict == "FALSIFIED"


# =============================================================================
# AMBIGUOUS-HOLD: CI lb>0.5 overall but a half/third <=0.5 (edge in one regime)
# =============================================================================
def test_ambiguous_hold_regime_split():
    # First half ~95% hit, second half ~50% -> overall rate high enough that the CI
    # lower bound clears 0.5, but the SECOND half (and a third) sits at/below 0.5 ->
    # non-stationary -> AMBIGUOUS-HOLD, and the absent regime is named.
    rng = np.random.default_rng(21)
    n_half = 120
    out1 = rng.choice([-1.0, 1.0], size=n_half)
    gb1 = out1.copy()
    gb1[::20] = -gb1[::20]                    # ~95% hit in first half
    out2 = rng.choice([-1.0, 1.0], size=n_half)
    gb2 = rng.choice([-1.0, 1.0], size=n_half)  # ~50% in second half
    out = np.concatenate([out1, out2])
    gb = np.concatenate([gb1, gb2])
    df = make_export(list(gb), list(out), add_live=False)
    cols = cols_of(df)
    v = W.evaluate_weekly(df, cols, seed=22)
    assert v.eff_n >= W.N_EFF_FLOOR
    assert v.ci_lo > 0.5            # overall edge present
    assert not (all(r > 0.5 for r in v.halves) and all(r > 0.5 for r in v.thirds))
    assert v.verdict == "AMBIGUOUS-HOLD"
    # the note must name the regime the edge is absent in (half-2 here):
    assert any("half-2" in nt or "third-3" in nt for nt in v.notes)


# =============================================================================
# VOTE SUB-VERDICT (PREREG-W GC-3; forbidden #4 pre-condition)
# =============================================================================
def test_vote_importance_not_run_when_votes_off():
    # default export = votes off; importance MUST refuse to run (forbidden #4).
    df = make_export([1, -1, 1, -1] * 30, [1, -1, 1, -1] * 30, add_live=False)
    cols = cols_of(df)
    base = W.evaluate_weekly(df, cols).point_estimate
    sub = W.evaluate_vote_importance(df, cols, base, all_votes_on=False)
    assert sub.sub_verdict == "NOT-RUN"
    assert any("PRE-CONDITION" in nt for nt in sub.notes)


def test_vote_importance_composite_killed_when_votes_noise():
    # all-votes-on, but only vStruct carries signal (== structure baseline); the
    # other three are pure noise. No input solo-beats baseline after the max-stat
    # penalty -> COMPOSITE-KILLED.
    rng = np.random.default_rng(31)
    n = 200
    out = rng.choice([-1.0, 1.0], size=n)
    gb = out.copy()
    gb[::5] = -gb[::5]                        # structure ~80%
    votes = {
        "vStruct": list(gb),                  # == structure baseline
        "vSeason": list(rng.choice([-1.0, 1.0], size=n)),  # noise
        "vRates": list(rng.choice([-1.0, 1.0], size=n)),   # noise
        "vEarn": list(rng.choice([-1.0, 1.0], size=n)),    # noise
    }
    df = make_export(list(gb), list(out), votes=votes, add_live=False)
    cols = cols_of(df)
    base = W.evaluate_weekly(df, cols).point_estimate
    sub = W.evaluate_vote_importance(df, cols, base, all_votes_on=True,
                                     perm_b=2000, seed=33)
    assert sub.sub_verdict == "COMPOSITE-KILLED"
    assert sub.perm_b == 2000
    # vStruct ties the baseline (delta ~0), others are below -> best delta ~<=0.
    assert sub.observed_max <= 0.05


def test_vote_importance_composite_survives_when_a_vote_beats_baseline():
    # all-votes-on; vSeason is a STRONGER predictor than structure-only. It should
    # solo-beat the baseline past the max-stat penalty -> COMPOSITE-SURVIVES.
    # The pairing is PRIOR-paired (R3-1): a SURVIVES vote must PREDICT next week's
    # direction, so vSeason is built so the PRIOR week's vSeason matches THIS week's
    # realized (vSeason[k-1] == realized[k]) ~92% of the time. The export's
    # gateHit/gateScored are prior-paired too (via _make_prior_paired_export), so the
    # baseline and the vote solo-rates are compared on the identical pairing.
    rng = np.random.default_rng(41)
    n = 300
    out = rng.choice([-1.0, 1.0], size=n)
    realized = np.sign(out)
    # structure baseline ~prior-coinflip (weak): gb is contemporaneous (== realized),
    # so its PRIOR-paired rate vs next-week realized is ~0.5.
    gb = realized.copy()
    # vSeason PREDICTS next week: vSeason[j] = realized[j+1] (so prior vSeason[k-1] ==
    # realized[k]); inject ~8% misses uniformly -> prior-paired rate ~0.92.
    vseason = np.concatenate([realized[1:], [realized[-1]]])
    vseason[::12] = -vseason[::12]
    votes = {
        "vStruct": list(gb),
        "vSeason": list(vseason),
        "vRates": list(rng.choice([-1.0, 1.0], size=n)),
        "vEarn": list(rng.choice([-1.0, 1.0], size=n)),
    }
    df = _make_prior_paired_export(list(gb), list(out), votes, add_live=False)
    cols = cols_of(df)
    base = W.evaluate_weekly(df, cols).point_estimate
    sub = W.evaluate_vote_importance(df, cols, base, all_votes_on=True,
                                     perm_b=2000, seed=43)
    assert sub.best_input == "vSeason"
    assert sub.observed_max > 0.1
    assert sub.sub_verdict == "COMPOSITE-SURVIVES"
    assert sub.p_value < W.IMPORTANCE_ALPHA


def test_vote_importance_not_run_when_a_vote_column_missing():
    df = make_export([1, -1] * 50, [1, -1] * 50, add_live=False).drop(columns=["vEarn"])
    cols = cols_of(df)
    sub = W.evaluate_vote_importance(df, cols, 0.6, all_votes_on=True)
    assert sub.sub_verdict == "NOT-RUN"
    assert any("missing" in nt for nt in sub.notes)


# =============================================================================
# R3-1 -- VOTE-IMPORTANCE PRIOR-PAIRING (CRITICAL; flips COMPOSITE sub-verdict)
#
# Pine pairs the PRIOR calendar week's bias against the CURRENT week's realized
# direction (W-DRAFT L117-119: priorGateBias = gateBias[1]; gateHit =
# priorGateBias == realized). The headline baseline is therefore prior-paired.
# Every vote solo-rate AND the permutation null must ALSO be prior-paired, or
# vStruct (== gateBias) is scored under a different pairing than the baseline it
# is differenced against -- delta[vStruct] is then NOT 0 and can flip
# COMPOSITE-KILLED <-> SURVIVES on the "observed_max > 0" gate (L460).
# =============================================================================
def _make_prior_paired_export(gate_bias, outcome, votes, *, add_live=True,
                              week0="2020-01-06"):
    """Build a data-window export whose gateHit/gateScored are PRIOR-paired.

    Mirrors W-DRAFT L117-119 exactly:
      priorGateBias = gateBias[1]
      gateScored    = priorGateBias != 0 AND realized != 0   (confirmed weeks)
      gateHit       = gateScored AND (priorGateBias == realized)
    `votes` MUST include vStruct == gate_bias (Pine gateBias = vStruct).
    """
    n = len(gate_bias)
    gb = np.array(gate_bias, float)
    out = np.array(outcome, float)
    realized = np.sign(out)
    prior_gb = np.concatenate([[np.nan], gb[:-1]])  # gateBias[1]
    gs = ((np.nan_to_num(prior_gb, nan=0.0) != 0) & (realized != 0)).astype(int)
    gate_hit = np.where((gs == 1) & (np.sign(prior_gb) == realized), 1, 0)
    times = pd.date_range(week0, periods=n, freq="W").astype(str).tolist()
    data = {
        "time": times, "bias": gb, "outcome": out,
        "vStruct": np.array(votes["vStruct"], float),
        "vSeason": np.array(votes["vSeason"], float),
        "vRates": np.array(votes["vRates"], float),
        "vEarn": np.array(votes["vEarn"], float),
        "hit": gate_hit.copy(),
        "gateBias": gb, "gateHit": gate_hit, "gateScored": gs, "scored": gs,
    }
    df = pd.DataFrame(data)
    if add_live:
        live_time = pd.Timestamp(times[-1]) + pd.Timedelta(weeks=1)
        live = {c: (str(live_time) if c == "time" else 0.0) for c in df.columns}
        df = pd.concat([df, pd.DataFrame([live])], ignore_index=True)
    return df


def test_vote_importance_vstruct_delta_zero_under_prior_pairing():
    # Build a frame where gateBias[k-1] != gateBias[k] on scored rows so prior-
    # pairing and same-row pairing diverge for vStruct. vStruct is made
    # CONTEMPORANEOUS-but-NOT-PREDICTIVE: gateBias[k] == realized[k] (same-row
    # always "hits" -> the same-row bug reads ~100% for vStruct), but the PRIOR
    # week's bias vs this week's realized is a coinflip (iid outcomes). Under the
    # correct prior pairing vStruct-solo reproduces gateHit exactly, so
    # delta[vStruct] == 0 and the spurious same-row edge vanishes.
    rng = np.random.default_rng(20260618)
    n = 240
    out = rng.choice([-1.0, 1.0], size=n)        # iid realized direction
    gb = out.copy()                               # gateBias == realized (contemporaneous)
    votes = {
        "vStruct": list(gb),                      # Pine: gateBias = vStruct
        "vSeason": list(rng.choice([-1.0, 1.0], size=n)),
        "vRates": list(rng.choice([-1.0, 1.0], size=n)),
        "vEarn": list(rng.choice([-1.0, 1.0], size=n)),
    }
    df = _make_prior_paired_export(list(gb), list(out), votes, add_live=False)
    cols = cols_of(df)
    headline = W.evaluate_weekly(df, cols, seed=7)
    sub = W.evaluate_vote_importance(df, cols, headline.point_estimate,
                                     all_votes_on=True, perm_b=2000, seed=7)
    # 1) vStruct == gateBias under prior pairing -> its solo rate equals the
    #    prior-paired baseline -> delta exactly 0.
    assert abs(sub.per_input_rate["vStruct"] - sub.baseline_rate) < 1e-9
    # 2) a contemporaneous-but-not-predictive structure vote must NOT manufacture
    #    a false SURVIVES; it is KILLED.
    assert sub.sub_verdict == "COMPOSITE-KILLED"


def test_vote_importance_same_row_pairing_would_false_survive():
    # Documents the defect the fix removes: under SAME-row pairing the
    # contemporaneous vStruct reads ~100% solo (gateBias == realized every week),
    # so its same-row delta vs the prior-paired baseline is large and positive --
    # which would flip the verdict to a false SURVIVES. The harness must NOT do
    # this; the prior-paired vStruct delta is ~0 instead.
    rng = np.random.default_rng(99)
    n = 240
    out = rng.choice([-1.0, 1.0], size=n)
    gb = out.copy()
    votes = {
        "vStruct": list(gb),
        "vSeason": list(rng.choice([-1.0, 1.0], size=n)),
        "vRates": list(rng.choice([-1.0, 1.0], size=n)),
        "vEarn": list(rng.choice([-1.0, 1.0], size=n)),
    }
    df = _make_prior_paired_export(list(gb), list(out), votes, add_live=False)
    cols = cols_of(df)
    headline = W.evaluate_weekly(df, cols, seed=5)
    # the SAME-row solo rate for vStruct is ~1.0 (contemporaneous), far above the
    # prior-paired baseline ~0.5 -- confirming the two pairings diverge here.
    scored, _, _ = W.de_overlap_scored(df, cols, drop_live=False)
    realized = np.sign(pd.to_numeric(scored[cols["outcome"]]).to_numpy())
    same_row_vstruct = pd.to_numeric(scored[cols["vStruct"]]).to_numpy()
    same_row_rate = float((np.sign(same_row_vstruct) == realized).mean())
    assert same_row_rate > 0.95
    assert abs(headline.point_estimate - 0.5) < 0.12
    # the harness must report the PRIOR-paired rate (~baseline), not same-row ~1.0:
    sub = W.evaluate_vote_importance(df, cols, headline.point_estimate,
                                     all_votes_on=True, perm_b=1500, seed=5)
    assert sub.per_input_rate["vStruct"] < same_row_rate - 0.3


# =============================================================================
# R3-2 -- gateHit REQUIRED; wrong-pairing same-row fallback removed (HIGH)
#
# gateHit is a guaranteed data_window column (W-DRAFT L171). Requiring it means a
# gateHit-absent export raises (clean skip) instead of routing through a same-row
# fallback that computes a DIFFERENT statistic than Pine's prior-paired gateHit.
# =============================================================================
def test_load_export_raises_when_gatehit_absent():
    df = make_export([1, -1, 1, -1] * 20, [1, -1, 1, -1] * 20,
                     add_live=False).drop(columns=["gateHit"])
    p = Path(__import__("tempfile").mkdtemp()) / "ICT_WEEKLY_no_gatehit.csv"
    df.to_csv(p, index=False)
    raised = False
    try:
        W.load_export(p)
    except ValueError as ex:
        raised = True
        assert "gateHit" in str(ex)
    assert raised, "load_export must raise when gateHit is absent (clean skip)"


def test_gatehit_in_required_canon():
    assert "gateHit" in W.REQUIRED_CANON


# =============================================================================
# CI METHOD is the moving-block bootstrap (NOT binomial) -- forbidden #2.
# A perfectly-alternating outcome (block_len picks up the structure) gives a
# different CI width than the iid binomial would; we assert the harness routes
# through the block-bootstrap primitive by reproducing it with the same seed.
# =============================================================================
def test_ci_is_moving_block_bootstrap_not_binomial():
    rng = np.random.default_rng(51)
    n = 150
    out = rng.choice([-1.0, 1.0], size=n)
    gb = out.copy(); gb[::4] = -gb[::4]       # ~75%
    df = make_export(list(gb), list(out), add_live=False)
    cols = cols_of(df)
    v = W.evaluate_weekly(df, cols, seed=99)
    # reproduce the exact block-bootstrap CI with the same hit vector + L_W + seed.
    # Must use the SAME de-overlap evaluate_weekly uses (drop_live=True) so the hit
    # vector matches element-for-element.
    scored, _, _ = W.de_overlap_scored(df, cols, drop_live=True)
    hit_vec, _, _ = W.structure_gate_hit_rate(scored, cols)
    lo, hi = __import__("_ict_offline").moving_block_bootstrap_ci(
        hit_vec, block_len=v.block_len, B=W.CI_B, seed=99, alpha=W.CI_ALPHA)
    assert abs(lo - v.ci_lo) < 1e-12 and abs(hi - v.ci_hi) < 1e-12


# =============================================================================
# GRACEFUL SKIP: run_layer_w returns None + prints the needed export when absent.
# =============================================================================
def test_run_layer_w_skips_when_export_absent(capsys, tmp_path):
    missing = tmp_path / "definitely_not_here_ICT_WEEKLY.csv"
    res = W.run_layer_w(missing, all_votes_on=False)
    assert res is None
    out = capsys.readouterr().out
    assert "NO EXPORT YET" in out
    assert str(missing) in out


def test_run_layer_w_runs_on_synthetic_csv(tmp_path):
    # round-trip a synthetic export to disk and run end-to-end (no vendor data).
    df = make_export([1, -1, 1] * 70, [1, -1, 1] * 70, add_live=True)
    p = tmp_path / "ICT_WEEKLY_BIAS_data_window.csv"
    df.to_csv(p, index=False)
    res = W.run_layer_w(p, all_votes_on=False, seed=5)
    assert res is not None
    headline, sub = res
    assert headline.verdict in {"RESOLVED", "FALSIFIED", "AMBIGUOUS-HOLD",
                                "INSUFFICIENT-N"}
    assert sub.sub_verdict == "NOT-RUN"   # votes-off default file


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            # crude capsys/tmp_path shims for direct-run mode:
            import inspect
            kw = {}
            sig = inspect.signature(fn)
            if "tmp_path" in sig.parameters:
                import tempfile
                kw["tmp_path"] = Path(tempfile.mkdtemp())
            if "capsys" in sig.parameters:
                class _Cap:
                    def readouterr(self):
                        import io
                        return type("R", (), {"out": "", "err": ""})()
                kw["capsys"] = _Cap()
            fn(**kw)
            print(f"PASS {fn.__name__}"); passed += 1
        except AssertionError as ex:
            print(f"FAIL {fn.__name__}: {ex}")
        except Exception as ex:
            print(f"ERROR {fn.__name__}: {type(ex).__name__}: {ex}")
    print(f"\n{passed}/{len(fns)} passed")
