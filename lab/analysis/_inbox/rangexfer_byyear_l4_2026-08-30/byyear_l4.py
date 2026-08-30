"""By-year presence limb (L4) for Q-RANGEXFER-1's five hypotheses.

Rule 0: read before writing this script --
  lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate1_range_persistence.py
    (the by-year L4 convention this ports: qualifying year = n_cond>=YEAR_MIN_NCOND=20;
    n_valid = count of qualifying years; AMBIGUOUS if n_valid<7; else required=n_valid-2
    years must show the effect positive)
  lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate2_overnight_rth_transfer.py
    (bias_overnight/bias_dayhist/y definitions -- confirmed bit-identical to
    candidate24_joint_frame.csv's own columns by reproducing its pooled +57.7pp/+38.7pp
    figures exactly from that cached CSV, this session, before writing this script)
  docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md sec6/sec7
    (L4's own definition: "incremental lift > 0 in >= N_valid-2 of N_valid qualifying
    years (n>=20/year); AMBIGUOUS if N_valid<7")

Motivation (2026-08-30, parallel to the ratified bounded Phase 1 round, not part of
it): every one of Q-RANGEXFER-1's five hypotheses currently carries L4 as an
UNCOMPUTED PREDICTION, not a result -- the verdict pre-registration's own SS E predicts
AMBIGUOUS on the parent hypotheses "same structural wall candidate 1 hit... only 6 of
the required 7 full calendar years qualify." L4 is a presence limb computed directly
from observed data -- it needs no surrogate-null model and is therefore fully
independent of Phase 1's own joint-surrogation design work. If L4 comes back AMBIGUOUS
on hypotheses this session is about to spend a bounded design round on, that is
material information: a certified Phase 1 design still cannot produce RESOLVED for a
hypothesis whose own L4 is structurally unresolvable at this panel length.

No vendor bar data required -- both source CSVs are git-tracked, cached joint frames
already used (and pooled-figure-verified in this exploration) by candidate24_joint_gate.py
/ c24_joint_gate.py and c2_c4_stratified_rerun.py. Pooled-figure cross-checks (run
interactively before writing this script, not repeated here) matched the brief's own
cited numbers exactly (MNQ overnight-range +0.5774/+0.3870; MNQ gap-magnitude
+0.1053/-0.0810; MYM overnight-range +0.3169/+0.2170; MYM gap-magnitude (overnight-calm
split) +0.0848/-0.0724; MYM gap-magnitude (day-history split) +0.1394/+0.0637 --
this last one vs the brief's own +0.1404/+0.0637-ish figures, small n=1304-vs-1307
panel difference, the same disclosed 3-day gap already on record in this repo for the
sibling overnight-range figure).

Disclosure: this is a NEW, exploratory diagnostic, not yet Codex-reviewed or
operator-ratified. Report the numbers plainly; do not silently promote them into a
brief's own scored verdict without that review.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
MNQ_FRAME = HERE.parent / "mnq_dailygeom_notice_2026-08-29" / "candidate24_joint_frame.csv"
MYM_FRAME = HERE.parent / "mym_mechanism_harvest_2026-08-29" / "c24_joint_frame.csv"

YEAR_MIN_NCOND = 20  # ported verbatim from candidate1_range_persistence.py


def _year_of(trading_day: pd.Series) -> pd.Series:
    return pd.to_datetime(trading_day).dt.year


def l4_single_stratum(df: pd.DataFrame, predictor: str, outcome: str = "y") -> dict:
    """Candidate 1's exact convention: qualifying year = count of predictor==1 rows
    that year >= YEAR_MIN_NCOND; per-year "pass" = lift(predictor) > 0 that year."""
    years = _year_of(df["trading_day"])
    by_year: dict[int, dict] = {}
    for yr in sorted(years.unique()):
        sub = df[years == yr]
        hi = sub.loc[sub[predictor] == 1, outcome]
        lo = sub.loc[sub[predictor] == 0, outcome]
        n_cond = len(hi)
        lift = float(hi.mean() - lo.mean()) if len(hi) and len(lo) else None
        by_year[int(yr)] = dict(n_cond=n_cond, n_ref=len(lo), lift=lift)
    valid = {yr: v for yr, v in by_year.items() if v["n_cond"] >= YEAR_MIN_NCOND}
    n_valid = len(valid)
    n_pass = sum(1 for v in valid.values() if v["lift"] is not None and v["lift"] > 0)
    if n_valid < 7:
        verdict = dict(n_valid=n_valid, n_pass=n_pass, required=None, verdict="AMBIGUOUS")
    else:
        required = n_valid - 2
        verdict = dict(n_valid=n_valid, n_pass=n_pass, required=required,
                       verdict="PASS" if n_pass >= required else "FAIL")
    return dict(by_year=by_year, l4=verdict)


def l4_min_stratified(df: pd.DataFrame, predictor: str, stratify_by: str,
                       outcome: str = "y") -> dict:
    """For the two parent (min-across-day-history-strata) hypotheses. The
    per-year statistic is the MIN across two stratum-specific lift estimates,
    so a year only "qualifies" if EVERY populated stratum independently clears
    YEAR_MIN_NCOND on predictor==1 count -- gating on the POOLED count (as an
    earlier version of this function did) lets a stratum with a handful of
    conditional observations silently drive the year's min-lift while still
    being counted as qualifying (Codex review, PR #224: MNQ 2023/2024/2026 and
    MYM's own analogous years had one stratum as low as 7-19 conditional
    observations under the pooled gate). Per-year "pass" = min-across-populated-
    strata lift > 0."""
    years = _year_of(df["trading_day"])
    by_year: dict[int, dict] = {}
    for yr in sorted(years.unique()):
        sub = df[years == yr]
        n_cond = int((sub[predictor] == 1).sum())
        lifts = {}
        stratum_n_cond = {}
        for s in sorted(sub[stratify_by].unique()):
            ss = sub[sub[stratify_by] == s]
            stratum_n_cond[int(s)] = int((ss[predictor] == 1).sum())
            hi = ss.loc[ss[predictor] == 1, outcome]
            lo = ss.loc[ss[predictor] == 0, outcome]
            if len(hi) and len(lo):
                lifts[int(s)] = float(hi.mean() - lo.mean())
        min_lift = min(lifts.values()) if lifts else None
        qualifies = bool(stratum_n_cond) and all(
            v >= YEAR_MIN_NCOND for v in stratum_n_cond.values()
        )
        by_year[int(yr)] = dict(n_cond=n_cond, stratum_n_cond=stratum_n_cond,
                                 populated_strata=lifts, min_lift=min_lift,
                                 qualifies=qualifies)
    valid = {yr: v for yr, v in by_year.items() if v["qualifies"]}
    n_valid = len(valid)
    n_pass = sum(1 for v in valid.values() if v["min_lift"] is not None and v["min_lift"] > 0)
    if n_valid < 7:
        verdict = dict(n_valid=n_valid, n_pass=n_pass, required=None, verdict="AMBIGUOUS")
    else:
        required = n_valid - 2
        verdict = dict(n_valid=n_valid, n_pass=n_pass, required=required,
                       verdict="PASS" if n_pass >= required else "FAIL")
    return dict(by_year=by_year, l4=verdict)


def main() -> None:
    mnq = pd.read_csv(MNQ_FRAME)
    mym = pd.read_csv(MYM_FRAME)

    results = {}

    # H-RANGEXFER-1 (MNQ, overnight-range, min across bias_dayhist strata)
    results["H-RANGEXFER-1"] = l4_min_stratified(mnq, "bias_overnight", "bias_dayhist")

    # H-RANGEXFER-1.a (MNQ, gap-magnitude, restricted to overnight-calm: bias_overnight==0)
    mnq_calm = mnq[mnq["bias_overnight"] == 0]
    results["H-RANGEXFER-1.a"] = l4_single_stratum(mnq_calm, "bias_gap")

    # H-RANGEXFER-1-MYM (MYM, overnight-range, min across bias_dayhist strata)
    results["H-RANGEXFER-1-MYM"] = l4_min_stratified(mym, "bias_overnight", "bias_dayhist")

    # H-RANGEXFER-1.a-MYM (MYM, gap-magnitude, restricted to overnight-calm)
    mym_calm = mym[mym["bias_overnight"] == 0]
    results["H-RANGEXFER-1.a-MYM"] = l4_single_stratum(mym_calm, "bias_gap")

    # H-RANGEXFER-1.b-MYM (MYM, gap-magnitude, restricted to bprime=0 i.e. bias_dayhist==0)
    mym_bp0 = mym[mym["bias_dayhist"] == 0]
    results["H-RANGEXFER-1.b-MYM"] = l4_single_stratum(mym_bp0, "bias_gap")

    for hyp, r in results.items():
        l4 = r["l4"]
        print(f"{hyp}: n_valid={l4['n_valid']} n_pass={l4['n_pass']} "
              f"required={l4['required']} -> L4={l4['verdict']}")

    (HERE / "byyear_l4_results.json").write_text(json.dumps(results, indent=1, default=str))
    print(f"\nWrote {HERE / 'byyear_l4_results.json'}")


if __name__ == "__main__":
    main()
