"""LAYER W harness -- Weekly directional-bias structure-only gateHitRate verdict.

Q-ICT-CASCADE-1, W layer. Pre-registered by PREREG-W.md (this directory). The
verdict instrument and EVERY frozen threshold below are transcribed from that file;
the §-citations point back to it. NOTHING here may diverge from PREREG-W -- if a
value disagrees with the PREREG, the PREREG wins and this is a bug.

WHAT THIS LAYER MEASURES (PREREG-W "Two-leg scope"): the weekly-close structure-only
hit-rate (`gateBias = vStruct`, W-DRAFT L116), NOT composite `bias` (forbidden #1)
and NOT per-entry gate accuracy (leg b, separate probe). The composite `hitRate` is
research/report-only and never enters the verdict.

CONSUMES (PREREG-W frozen-config / W-DRAFT export L159-173): the Weekly indicator's
TV data-window export, one row per week:
    time, bias, outcome, vStruct, vSeason, vRates, vEarn, hit,
    gateBias, gateHit, gateScored, scored
A small SCHEMA-ADAPTER (COLMAP) maps TV column names -> canonical names so a minor
TV rename is a one-line fix.

FROZEN CONFIG (PREREG-W "Test object" table + "Genuine choices" GC-1/GC-2/GC-3):
  * Object under test  : structure-only gateHitRate (W-DRAFT L116, L125)
  * Denominator        : recompute from gateScored flags -- NEVER mean(hit)
                         (forbidden #3; the hit/gateHit columns collapse
                          miss+stand-down+flat into 0).
  * De-overlap         : one row per CONFIRMED scored week (gateScored==1); drop
                         the live (last) bar (PREREG-W "Resampling unit").
  * CI method          : moving-block bootstrap (NOT binomial; forbidden #2).
  * Block length L_W   : GC-1 -- autocorr_block_len(outcome, cutoff=0.10, floor=1,
                         cap=8) on the step-1 outcome series.
  * n-floor            : GC-2 -- effective N = nGateScored / L_W; if < 30 ->
                         INSUFFICIENT-N (dominates FALSIFIED).
  * Stationarity       : halves AND thirds (chronological); all point estimates
                         must exceed 0.50 for RESOLVED.
  * Vote importance    : GC-3 -- 4 inputs (vStruct,vSeason,vRates,vEarn) solo vs
                         structure-only baseline, max-statistic label-permutation
                         B=10000. Pre-condition: all-votes-on, W-2-fixed export.
  * emaLen=20 desync   : LOCKED; W emaLen MUST == 1M wEmaLen == 20 or the W number
                         transfers nothing (forbidden #5). Operator-asserted upstream
                         (it lives in Pine, not the export); this harness records the
                         assumption in its report but cannot read the Pine value.

VERDICT GATE (PREREG-W §"Verdict gate"; maps to TEST_PLAN §6 W row):
  RESOLVED        : block-CI lower bound > 0.50 AND both halves' point est > 0.50
                    AND all three thirds' point est > 0.50 AND eff_N >= 30.
  FALSIFIED       : block-CI straddles 0.50 (lower bound <= 0.50) AND eff_N >= 30.
  AMBIGUOUS-HOLD  : CI lower bound > 0.50 BUT non-stationary (a half or third
                    <= 0.50) -> HOLD + name the regime the edge is absent in.
  INSUFFICIENT-N  : eff_N < 30 -> claim unfalsifiable on this data. Dominates
                    FALSIFIED (a straddling CI under the floor is NOT a falsification).

Vote sub-verdict (separate from the structure-only headline; §4 H-W
"vote-adds-nothing"): the COMPOSITE-vote claim is KILLED if no single input
solo-beats the structure-only baseline after the max-stat label-permutation penalty
(B=10000). Killing it does NOT change the structure-only headline.

Conventions (repo + PREREG): look-ahead-free, ET=America/New_York (DST-aware), TV
BAR_EXPORT epoch is UTC. ASCII only. The real-export entrypoint (main / run_layer_w)
SKIPS cleanly when the export CSV is absent (operator has not run TV yet) and prints
exactly which export it needs. Unit tests run on synthetic in-test fixtures.

Rule-0 source (gitignored, outside the repo): C:/Users/joshu/Downloads/
ict_weekly_bias_DRAFT.pine (9405 bytes / LastWriteUTC 2026-06-18T17:53:06Z) and
ict_1m_execution_DRAFT.pine (22182 bytes / 2026-06-18T18:42:43Z). A resuming session
MUST re-anchor (Downloads is mutable; line numbers drift) -- see PREREG-W §0.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

import _ict_offline as M

# -----------------------------------------------------------------------------
# FROZEN PRE-REGISTERED CONSTANTS (PREREG-W; do not edit without re-locking it).
# -----------------------------------------------------------------------------
# GC-1 block-length rule (PREREG-W frozen-config "Block length L_W" + GC-1):
AUTOCORR_CUTOFF = 0.10
BLOCK_FLOOR = 1
BLOCK_CAP = 8
# GC-2 n-floor (PREREG-W frozen-config "n-floor" + GC-2):
N_EFF_FLOOR = 30
# GC-3 vote-importance permutation count (PREREG-W frozen-config "Importance
# penalty" + GC-3) and the importance significance threshold (§"Verdict gate"
# vote sub-verdict: "solo-beats ... after the penalty" at the conventional 0.05):
PERM_B = 10000
IMPORTANCE_ALPHA = 0.05
# CI level (PREREG-W: 95% block-CI):
CI_ALPHA = 0.05
# Bootstrap resample count for the block CI (not pre-registered as a value; a large
# fixed count so the percentile CI is stable -- the verdict reads its LOWER BOUND):
CI_B = 20000
# The four importance inputs, in W-DRAFT line order (L69/73/78/82):
VOTE_INPUTS = ("vStruct", "vSeason", "vRates", "vEarn")
# emaLen desync invariant (PREREG-W forbidden #5; W-DRAFT L26 == 1M-DRAFT L62):
EMALEN_REQUIRED = 20

# Default real export location (operator drops the TV data-window CSV here). Absent
# until the operator runs TV; main() skips cleanly and prints this path.
DEFAULT_CSV = Path(
    r"C:/Users/joshu/Downloads/ICT_WEEKLY_BIAS_data_window.csv"
)

# -----------------------------------------------------------------------------
# SCHEMA ADAPTER (PREREG-W CONSUMES: "Build a small schema-adapter (column-name
# map) so a minor TV rename is a 1-line fix."). Canonical name -> list of accepted
# source header spellings (first match wins, case-insensitive after strip). To
# absorb a TV rename, add the new spelling to the relevant list -- one line.
# -----------------------------------------------------------------------------
COLMAP = {
    "time": ["time", "datetime", "date"],
    "bias": ["bias"],
    "outcome": ["outcome", "realized"],
    "vStruct": ["vStruct", "v_struct", "vstruct"],
    "vSeason": ["vSeason", "v_season", "vseason"],
    "vRates": ["vRates", "v_rates", "vrates"],
    "vEarn": ["vEarn", "v_earn", "vearn"],
    "hit": ["hit"],
    "gateBias": ["gateBias", "gate_bias", "gatebias"],
    "gateHit": ["gateHit", "gate_hit", "gatehit"],
    "gateScored": ["gateScored", "gate_scored", "gatescored"],
    "scored": ["scored"],
}
# Columns the harness strictly requires to produce the verdict. (Vote columns are
# only required for the importance sub-verdict; absence of all-votes-on is reported,
# not fatal, per forbidden #4 -- you simply cannot run importance on a votes-off file.)
# gateHit is REQUIRED (R3-2): it is the PRIOR-paired hit column (W-DRAFT L119/L171,
# a guaranteed data_window plot), so a faithful export always carries it. Requiring
# it makes a gateHit-absent export raise (clean skip) rather than routing through a
# same-row fallback that would compute a DIFFERENT statistic than Pine's gateHit.
REQUIRED_CANON = ["time", "gateBias", "gateHit", "gateScored", "outcome"]


def _norm(s: str) -> str:
    return str(s).strip().lower()


def resolve_columns(headers, colmap=COLMAP):
    """Map raw TV headers -> {canonical: raw}. Missing canonicals are omitted.

    First accepted spelling that appears (case-insensitive) wins. Returns a dict so
    a minor rename is a one-line COLMAP edit, not a harness change.
    """
    norm_to_raw = {}
    for h in headers:
        norm_to_raw.setdefault(_norm(h), h)
    resolved = {}
    for canon, spellings in colmap.items():
        for sp in spellings:
            if _norm(sp) in norm_to_raw:
                resolved[canon] = norm_to_raw[_norm(sp)]
                break
    return resolved


# -----------------------------------------------------------------------------
# RESULT CONTAINERS
# -----------------------------------------------------------------------------
@dataclass
class WeeklyVerdict:
    """The W-layer headline (structure-only gateHitRate)."""
    verdict: str                 # RESOLVED / FALSIFIED / AMBIGUOUS-HOLD / INSUFFICIENT-N
    n_gate_scored: int           # confirmed scored weeks (denominator)
    n_gate_hit: int
    point_estimate: float        # nGateHit / nGateScored
    block_len: int               # L_W (GC-1)
    eff_n: float                 # nGateScored / L_W (GC-2 effective N)
    ci_lo: float
    ci_hi: float
    halves: tuple                # (h1_rate, h2_rate)
    thirds: tuple                # (t1_rate, t2_rate, t3_rate)
    n_flat: int                  # weeks excluded as realized==0 (reported separately)
    n_live_dropped: int          # rows dropped as live/unconfirmed
    notes: list = field(default_factory=list)


@dataclass
class VoteSubVerdict:
    """The vote-importance sub-verdict (separate from the headline)."""
    sub_verdict: str             # COMPOSITE-KILLED / COMPOSITE-SURVIVES / NOT-RUN
    baseline_rate: float         # structure-only gateHitRate (the bar to beat)
    per_input_rate: dict         # input -> its solo directional hit-rate
    observed_max: float          # max over inputs of (solo_rate - baseline)
    best_input: str
    p_value: float               # max-stat label-permutation p (GC-3)
    perm_b: int
    notes: list = field(default_factory=list)


# -----------------------------------------------------------------------------
# DE-OVERLAP + DENOMINATOR (PREREG-W "Resampling unit"; forbidden #3).
# -----------------------------------------------------------------------------
def de_overlap_scored(df, cols, drop_live=True):
    """One row per CONFIRMED scored week; drop the live (last) bar.

    Returns (scored_df, n_flat, n_live_dropped) where scored_df has ONLY weeks with
    gateScored==1, chronologically ordered by `time`. PREREG-W frozen-config:
      * the resampling unit is the confirmed scored week (gateScored==1);
      * the export is already one row per week (W-DRAFT L94/L118) so there is no
        within-week pseudo-replication -- this function just filters to scored;
      * drop the live bar (the last row -- the in-progress, unconfirmed week).

    NEVER trust mean(hit): gateScored is the denominator source. We recompute it
    defensively from gateBias/outcome when the column is missing (see notes), but
    when present we use the script's own flag.
    """
    time_c = cols["time"]
    gscored_c = cols["gateScored"]
    out_c = cols["outcome"]
    work = df.copy()
    # chronological order (PREREG-W stationarity halves/thirds need true order):
    work = work.sort_values(time_c, kind="stable").reset_index(drop=True)
    n_live_dropped = 0
    if drop_live and len(work) > 0:
        # the last row is the in-progress (live, unconfirmed) week -> drop it.
        work = work.iloc[:-1].reset_index(drop=True)
        n_live_dropped = 1
    # flat weeks (realized==0) are NOT scored (frozen); count them for the report.
    out = pd.to_numeric(work[out_c], errors="coerce").to_numpy()
    n_flat = int(np.sum(out == 0))
    gs = pd.to_numeric(work[gscored_c], errors="coerce").fillna(0).to_numpy()
    scored = work[gs == 1].reset_index(drop=True)
    return scored, n_flat, n_live_dropped


def chrono_frame_drop_live(df, cols, drop_live=True):
    """FULL chronological per-week frame, live bar dropped, NOT scored-filtered.

    Returns (work, scored_mask) where `work` is one contiguous row per CALENDAR
    week ordered by `time` (the live/last bar dropped), and `scored_mask` is the
    boolean gateScored==1 selector aligned to `work`'s rows.

    This is the basis for PRIOR-paired vote signs (R3-1): the prior calendar week
    of a scored row may itself be unscored (flat/stand-down), so the shift MUST be
    taken on the contiguous calendar frame BEFORE the scored filter -- filtering
    first would pair against the prior *scored* row, not the prior *calendar* week
    (the pairing Pine's gateBias[1] performs, W-DRAFT L117).
    """
    time_c = cols["time"]
    gscored_c = cols["gateScored"]
    work = df.copy()
    work = work.sort_values(time_c, kind="stable").reset_index(drop=True)
    if drop_live and len(work) > 0:
        work = work.iloc[:-1].reset_index(drop=True)
    gs = pd.to_numeric(work[gscored_c], errors="coerce").fillna(0).to_numpy()
    scored_mask = gs == 1
    return work, scored_mask


def structure_gate_hit_rate(scored_df, cols):
    """Structure-only gateHitRate over CONFIRMED scored weeks (PREREG-W object).

    Point estimate = nGateHit / nGateScored. The numerator counts weeks where the
    structure-only prior bias matched the realized direction:
        gateHit = (gateBias_prior == sign(outcome))  on scored weeks.
    The export already carries gateHit (W-DRAFT L171), but PREREG-W forbids trusting
    its collapsed denominator -- so we recompute the hit vector from gateBias vs
    outcome whenever both columns exist, and fall back to the gateHit column only if
    gateBias is unavailable (recorded as a note). Returns (hit_vec, n_scored, n_hit).

    NOTE on gateBias semantics (W-DRAFT L116-119): the export's gateScored already
    encodes `priorGateBias != 0 AND outcome != 0`, and gateHit = (priorGateBias ==
    realized) on those weeks. In the data-window export, the per-row gateBias column
    is the CURRENT week's structBias; the SCORED comparison the script performs is
    against the PRIOR week's bias. Because we filter to gateScored==1 (the script's
    own confirmed-and-directional flag) the gateHit column on those rows is the
    script-correct PRIOR-paired hit/miss; we use it as the hit vector. This keeps
    the denominator from gateScored (never mean(hit)) while honoring the script's
    prior-vs-realized pairing.

    gateHit is a REQUIRED_CANON column (R3-2): load_export raises (clean skip) on a
    gateHit-absent export, so there is no same-row fallback here -- a same-row
    sign(gateBias)==realized recompute would be a DIFFERENT statistic than Pine's
    prior-paired gateHit and must never reach the verdict.
    """
    gh = pd.to_numeric(scored_df[cols["gateHit"]], errors="coerce").fillna(0).to_numpy()
    hit_vec = (gh != 0).astype(float)
    n_scored = int(len(hit_vec))
    n_hit = int(hit_vec.sum())
    return hit_vec, n_scored, n_hit


# -----------------------------------------------------------------------------
# STATIONARITY (PREREG-W: halves AND thirds, chronological).
# -----------------------------------------------------------------------------
def _chrono_split_rates(hit_vec, n_parts):
    """Point-estimate hit-rate per chronological part. NaN for an empty part."""
    n = len(hit_vec)
    if n == 0:
        return tuple(np.nan for _ in range(n_parts))
    edges = np.linspace(0, n, n_parts + 1).astype(int)
    rates = []
    for k in range(n_parts):
        seg = hit_vec[edges[k]:edges[k + 1]]
        rates.append(float(seg.mean()) if len(seg) > 0 else np.nan)
    return tuple(rates)


# -----------------------------------------------------------------------------
# HEADLINE VERDICT (PREREG-W §"Verdict gate").
# -----------------------------------------------------------------------------
def evaluate_weekly(df, cols, *, seed=20260618):
    """Compute the structure-only gateHitRate headline verdict (PREREG-W).

    df   : the loaded export (already column-resolved by the caller; pass `cols`).
    cols : {canonical: raw} from resolve_columns.
    seed : RNG seed for the block bootstrap (reproducible).
    Returns a WeeklyVerdict.
    """
    notes = []
    scored, n_flat, n_live = de_overlap_scored(df, cols, drop_live=True)
    hit_vec, n_scored, n_hit = structure_gate_hit_rate(scored, cols)

    if n_scored == 0:
        return WeeklyVerdict(
            verdict="INSUFFICIENT-N", n_gate_scored=0, n_gate_hit=0,
            point_estimate=np.nan, block_len=BLOCK_FLOOR, eff_n=0.0,
            ci_lo=np.nan, ci_hi=np.nan, halves=(np.nan, np.nan),
            thirds=(np.nan, np.nan, np.nan), n_flat=n_flat, n_live_dropped=n_live,
            notes=["no confirmed scored weeks after de-overlap"],
        )

    point = n_hit / n_scored

    # GC-1 block length from the OUTCOME series (PREREG-W: step-1 outcome autocorr).
    # The outcome series is the per-scored-week realized-direction sign (the thing
    # whose cross-week autocorrelation the block bootstrap absorbs).
    # R3-3: block_len is measured on the SCORED-week outcome series (the de-overlapped
    # `scored` frame), which is internally consistent with what the block bootstrap
    # resamples below -- the moving-block CI runs on hit_vec over those same scored
    # rows, so the autocorrelation horizon and the resampled series share one index.
    out_series = np.sign(pd.to_numeric(scored[cols["outcome"]], errors="coerce").to_numpy())
    block_len = M.autocorr_block_len(out_series, cutoff=AUTOCORR_CUTOFF,
                                     floor=BLOCK_FLOOR, cap=BLOCK_CAP)

    # GC-2 effective N = nGateScored / L_W (block-reduced).
    eff_n = n_scored / float(block_len)

    # moving-block bootstrap 95% CI on the structure-only hit-rate (NOT binomial).
    ci_lo, ci_hi = M.moving_block_bootstrap_ci(hit_vec, block_len=block_len,
                                               B=CI_B, seed=seed, alpha=CI_ALPHA)

    halves = _chrono_split_rates(hit_vec, 2)
    thirds = _chrono_split_rates(hit_vec, 3)

    # ---- verdict gate (exact PREREG-W mapping; INSUFFICIENT-N dominates) --------
    if eff_n < N_EFF_FLOOR:
        verdict = "INSUFFICIENT-N"
        notes.append(
            f"effective N {eff_n:.1f} (= {n_scored}/{block_len}) < n_floor {N_EFF_FLOOR}: "
            "claim unfalsifiable on this data; extend the export window (independent "
            "period / independent price path, NOT a different feed of the same weeks)."
        )
    else:
        lb_above = ci_lo > 0.50
        halves_ok = all((not np.isnan(r)) and r > 0.50 for r in halves)
        thirds_ok = all((not np.isnan(r)) and r > 0.50 for r in thirds)
        if lb_above and halves_ok and thirds_ok:
            verdict = "RESOLVED"
            notes.append(
                "RESOLVED routes to CONTINUED USE + a downstream per-entry transfer "
                "probe (PREREG-W W-6); it does NOT lock/deploy or license the 1M gate "
                "by itself (cascade-transfer pre-gate H-CASCADE is separate)."
            )
        elif lb_above and not (halves_ok and thirds_ok):
            verdict = "AMBIGUOUS-HOLD"
            absent = []
            if not (halves[0] > 0.50):
                absent.append("half-1")
            if not (halves[1] > 0.50):
                absent.append("half-2")
            for i, r in enumerate(thirds, 1):
                if not (r > 0.50):
                    absent.append(f"third-{i}")
            notes.append(
                "CI lower bound > 0.50 but non-stationary: edge absent in "
                + ", ".join(absent) + ". HOLD; re-test in that regime/window."
            )
        else:  # lb_above is False -> straddles 0.50
            verdict = "FALSIFIED"
            notes.append("block-CI straddles 0.50 (lower bound <= 0.50) with eff_N "
                         "above the floor: structure-only weekly bias not supported.")

    return WeeklyVerdict(
        verdict=verdict, n_gate_scored=n_scored, n_gate_hit=n_hit,
        point_estimate=point, block_len=block_len, eff_n=eff_n,
        ci_lo=ci_lo, ci_hi=ci_hi, halves=halves, thirds=thirds,
        n_flat=n_flat, n_live_dropped=n_live, notes=notes,
    )


# -----------------------------------------------------------------------------
# VOTE-IMPORTANCE SUB-VERDICT (PREREG-W GC-3; §"Verdict gate" vote sub-verdict).
# -----------------------------------------------------------------------------
def _solo_vote_hit_rate(prior_vote_sign, realized):
    """Directional solo hit-rate of one vote input, PRIOR-paired (R3-1).

    A solo vote 'hits' on a scored week when the PRIOR calendar week's vote sign
    matches THIS week's realized direction: sign(vote[1]) == sign(realized). This
    is the SAME prior-vs-realized pairing Pine performs for gateHit (priorGateBias
    = gateBias[1]; gateHit = priorGateBias == realized -- W-DRAFT L117-119), so for
    vStruct (== gateBias) the solo rate reproduces the prior-paired baseline exactly
    and delta[vStruct] == 0. `prior_vote_sign` is already sign-of-prior-week (the
    caller shifts on the full calendar frame before the scored filter); `realized`
    is sign(outcome) on the same scored rows. Weeks where the prior vote is flat
    (sign 0) are MISSES (no usable directional read).
    """
    return (prior_vote_sign == realized).astype(float)


def evaluate_vote_importance(df, cols, baseline_rate, *, all_votes_on,
                             perm_b=PERM_B, seed=20260618):
    """Best-of-K vote-importance sub-verdict (PREREG-W GC-3, B=10000).

    The COMPOSITE-vote claim is KILLED if NO single input (vStruct,vSeason,vRates,
    vEarn) solo-beats the structure-only baseline after the max-statistic
    label-permutation penalty over the 4 inputs.

    Pre-condition (forbidden #4): importance must run on an ALL-VOTES-ON, W-2-fixed
    export. `all_votes_on` is the operator/caller assertion that the export was
    generated with every vote enabled and vRates regenerated non-repaint (close[1]).
    If False, this returns NOT-RUN (running importance on a votes-off default export
    tests nothing).

    Pairing (R3-1): every vote solo-rate is PRIOR-paired (sign(vote[1]) ==
    sign(realized)) to MATCH the prior-paired headline baseline (Pine gateHit;
    W-DRAFT L117-119). The shift is taken on the FULL chronological calendar frame
    (live bar dropped, NOT scored-filtered) BEFORE restricting to gateScored==1, so
    the prior week is the prior CALENDAR week (not the prior scored row). Because
    gateBias == vStruct (W-DRAFT L116), this reproduces gateHit exactly on the
    scored rows -> delta[vStruct] == 0.

    Statistic per input (observed): solo_rate(input) - baseline_rate, on the scored
    weeks. observed_max = max over the 4 inputs. Null: permute the realized-direction
    LABELS (shuffle the outcome signs) and recompute each input's solo_rate - baseline
    under the permuted labels using the SAME prior-paired vote signs, take the MAX
    across inputs; repeat B times. p = P(null max >= observed max) with the add-one
    correction (offline primitive).
    """
    notes = []
    if not all_votes_on:
        notes.append(
            "PRE-CONDITION FAILED: importance requires an ALL-VOTES-ON, W-2-fixed "
            "(vRates non-repaint close[1]) export. Votes default off (W-DRAFT "
            "L31/38/46) and vRates repaints (W-DRAFT L76). A default/votes-off "
            "export tests nothing (forbidden #4). NOT-RUN."
        )
        return VoteSubVerdict("NOT-RUN", baseline_rate, {}, np.nan, "", np.nan,
                              perm_b, notes)

    # FULL calendar frame (live dropped, NOT scored-filtered) so the prior-week
    # shift below pairs against the prior CALENDAR week, matching Pine gateBias[1].
    work, scored_mask = chrono_frame_drop_live(df, cols, drop_live=True)
    if int(scored_mask.sum()) == 0:
        notes.append("no scored weeks; importance NOT-RUN.")
        return VoteSubVerdict("NOT-RUN", baseline_rate, {}, np.nan, "", np.nan,
                              perm_b, notes)
    realized_full = np.sign(pd.to_numeric(work[cols["outcome"]],
                                          errors="coerce").to_numpy())
    realized = realized_full[scored_mask]

    # collect the solo hit vectors for whichever vote inputs are present.
    present = [v for v in VOTE_INPUTS if v in cols]
    missing = [v for v in VOTE_INPUTS if v not in cols]
    if missing:
        notes.append("vote columns missing (cannot run all-4 importance): "
                     + ", ".join(missing) + ".")
        return VoteSubVerdict("NOT-RUN", baseline_rate, {}, np.nan, "", np.nan,
                              perm_b, notes)

    # PRIOR-paired vote signs: shift sign(vote) by one CALENDAR week on the full
    # frame (prior-week NaN -> 0 so it cannot match any +/-1 realized), THEN restrict
    # to the scored rows. This is the same gateBias[1] pairing as the baseline.
    vote_signs = {}
    hit_vecs = {}
    per_input_rate = {}
    for v in present:
        sig_full = np.sign(pd.to_numeric(work[cols[v]], errors="coerce")
                           .fillna(0).to_numpy())
        prior_full = np.concatenate([[0.0], sig_full[:-1]])  # sign(vote[1])
        prior_scored = prior_full[scored_mask]
        vote_signs[v] = prior_scored
        hv = _solo_vote_hit_rate(prior_scored, realized)
        hit_vecs[v] = hv
        per_input_rate[v] = float(hv.mean())

    deltas = {v: per_input_rate[v] - baseline_rate for v in present}
    best_input = max(deltas, key=deltas.get)
    observed_max = float(deltas[best_input])

    # Null distribution via the offline max-stat primitive. The per-input statistic
    # under a permuted label set = mean(prior_vote_sign == permuted_realized) -
    # baseline. We pre-extracted the prior-paired vote signs once (above); each
    # permutation reshuffles the scored-row realized labels.
    n = len(realized)
    # cache the permuted labels per draw inside the closure so all 4 inputs in one
    # permutation share the SAME shuffle (max-stat over a common permuted label set).
    state = {"perm": None}

    def per_input_stat(j, rng):
        if j == 0:
            state["perm"] = rng.permutation(realized)
        perm = state["perm"]
        v = present[j]
        return float((vote_signs[v] == perm).mean()) - baseline_rate

    p = M.max_stat_label_permutation(per_input_stat, n_inputs=len(present),
                                     observed_max=observed_max, B=perm_b, seed=seed)

    if p < IMPORTANCE_ALPHA and observed_max > 0:
        sub = "COMPOSITE-SURVIVES"
        notes.append(
            f"input '{best_input}' solo-beats structure baseline by "
            f"{observed_max:+.4f} (p={p:.4f} < {IMPORTANCE_ALPHA}) after the "
            "max-stat penalty: at least one vote adds signal beyond structure-only."
        )
    else:
        sub = "COMPOSITE-KILLED"
        notes.append(
            f"no input solo-beats the structure baseline after the max-stat penalty "
            f"(best '{best_input}' delta {observed_max:+.4f}, p={p:.4f} >= "
            f"{IMPORTANCE_ALPHA}). The composite-vote claim is KILLED; this does NOT "
            "change the structure-only headline (which stands on its own block-CI)."
        )
    return VoteSubVerdict(sub, baseline_rate, per_input_rate, observed_max,
                          best_input, p, perm_b, notes)


# -----------------------------------------------------------------------------
# REAL-EXPORT LOADER (column-resolved; skips cleanly when absent).
# -----------------------------------------------------------------------------
def load_export(path=DEFAULT_CSV):
    """Load + column-resolve the Weekly data-window export.

    Returns (df, cols). Raises FileNotFoundError if the CSV is absent (main() guards
    this and skips). Raises ValueError if a REQUIRED_CANON column cannot be resolved.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(str(path))
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    cols = resolve_columns(raw.columns)
    missing = [c for c in REQUIRED_CANON if c not in cols]
    if missing:
        raise ValueError(
            "export is missing required columns "
            + ", ".join(missing)
            + f"; resolved={sorted(cols)}; raw headers={list(raw.columns)}. "
            "Add the TV spelling to COLMAP (one-line fix)."
        )
    return raw, cols


# -----------------------------------------------------------------------------
# MAIN -- skips gracefully when the real export is absent.
# -----------------------------------------------------------------------------
def _print_needed_export(path):
    print("=" * 78)
    print("LAYER W -- Weekly directional-bias structure-only gateHitRate")
    print("=" * 78)
    print("NO EXPORT YET. This layer needs the Weekly indicator's TV data-window CSV:")
    print(f"  expected at : {path}")
    print("  source      : ict_weekly_bias_DRAFT.pine, data_window plots L159-173")
    print("  columns     : time, bias, outcome, vStruct, vSeason, vRates, vEarn,")
    print("                hit, gateBias, gateHit, gateScored, scored")
    print("  REQUIRED    : " + ", ".join(REQUIRED_CANON))
    print("  for the vote sub-verdict ALSO need an ALL-VOTES-ON, W-2-fixed export")
    print("  (vRates regenerated non-repaint close[1]; see PREREG-W forbidden #4).")
    print()
    print("Run TV -> export the data window -> drop the CSV at the path above, then")
    print("re-run:  python lab/analysis/ict_cascade_2026-06-18/harness_w.py")
    print("(A minor TV header rename is a one-line edit in harness_w.COLMAP.)")
    print("=" * 78)


def run_layer_w(path=DEFAULT_CSV, *, all_votes_on=False, seed=20260618):
    """End-to-end W-layer run on a real export. Returns (WeeklyVerdict, VoteSubVerdict)
    or None when the export is absent (caller/main skips). Honors PREREG-W exactly."""
    try:
        df, cols = load_export(path)
    except FileNotFoundError:
        _print_needed_export(path)
        return None

    print("emaLen desync invariant (PREREG-W forbidden #5): W emaLen MUST == 1M "
          f"wEmaLen == {EMALEN_REQUIRED}. This lives in Pine, not the export -- "
          "operator must confirm before trusting transfer.")
    headline = evaluate_weekly(df, cols, seed=seed)
    print("-" * 78)
    print("HEADLINE (structure-only gateHitRate):")
    print(f"  verdict        : {headline.verdict}")
    print(f"  nGateScored    : {headline.n_gate_scored}  (denominator from gateScored,"
          " NEVER mean(hit))")
    print(f"  nGateHit       : {headline.n_gate_hit}")
    print(f"  point estimate : {headline.point_estimate:.4f}")
    print(f"  block_len L_W  : {headline.block_len}  (GC-1: outcome autocorr<0.10,"
          " floor 1, cap 8)")
    print(f"  effective N    : {headline.eff_n:.1f}  (GC-2 floor {N_EFF_FLOOR})")
    print(f"  95% block-CI   : [{headline.ci_lo:.4f}, {headline.ci_hi:.4f}]")
    print(f"  halves         : {tuple(round(x, 4) for x in headline.halves)}")
    print(f"  thirds         : {tuple(round(x, 4) for x in headline.thirds)}")
    print(f"  flat weeks     : {headline.n_flat} (excluded)   live dropped:"
          f" {headline.n_live_dropped}")
    for nt in headline.notes:
        print(f"    - {nt}")

    sub = evaluate_vote_importance(df, cols, headline.point_estimate,
                                   all_votes_on=all_votes_on, seed=seed)
    print("-" * 78)
    print("VOTE SUB-VERDICT (best-of-4 importance; max-stat permutation B=10000):")
    print(f"  sub-verdict    : {sub.sub_verdict}")
    if sub.per_input_rate:
        print(f"  baseline       : {sub.baseline_rate:.4f}")
        for k, v in sub.per_input_rate.items():
            print(f"    {k:<8} solo rate {v:.4f}  (delta {v - sub.baseline_rate:+.4f})")
        print(f"  best input     : {sub.best_input}  observed_max"
              f" {sub.observed_max:+.4f}  p={sub.p_value:.4f}")
    for nt in sub.notes:
        print(f"    - {nt}")
    print("=" * 78)
    return headline, sub


def main():
    run_layer_w(DEFAULT_CSV, all_votes_on=False)


if __name__ == "__main__":
    main()
