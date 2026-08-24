#!/usr/bin/env python3
"""Q-ORBCUSH-1 re-test under the corrected (anchored) date-correlation method.

Trigger: `POSITIVE_CONTROL_METHOD_FIX.md` §6.3 (q_orbpos_1_2026-08) names this
explicitly as a worthwhile, separately-scoped follow-on -- the expanding-median
bucket-construction defect diagnosed there is decisively fixed (0/3 -> 3/3
date-correlation clearance on a synthetic positive control), so a real candidate
that clears the corrected test now means something it did not before. Operator
GO: 2026-08-24 in-session instruction ("Run the ORB-MNQ regime-break re-test
under the fixed method").

Candidate: trailing mean-R of ORB-MNQ-1's own realized trades -- the SAME
classifier `run_meanr_regime_gate.py` (Q-ORBCUSH-1, FALSIFIED 2026-08-20, 0/3
date-correlation clearance) built and tested. Only the threshold-construction
and date-correlation-test steps change; everything else (rolling-mean-R
construction WITH its `.shift(1)` self-referential-outcome exclusion, WINDOWS,
CUTOFF, gate_check_bucket, the cushion-sizing survivor gate) is reused
byte-for-byte via `_imported_run_meanr_regime_gate.py` (a copy of the frozen
script with exactly ONE line changed: the stale absolute path to a
since-deleted worktree, corrected to this worktree -- same handling
`run_orbpos_tff_probe.py` documented for the identical defect in the harness
it imports).

Two frozen-fix pieces imported UNCHANGED from `run_orbpos_positive_control_v2_anchored.py`
(POSITIVE_CONTROL_METHOD_FIX.md §3, run+verified 2026-08-23):
  - `print_level_association` -- Fisher's-exact + separation-floor criterion,
    ASSOC_ALPHA=0.01 / MIN_SEPARATION_PP=0.35 (frozen, not touched here).
  - `ASSOC_ALPHA`, `MIN_SEPARATION_PP` module constants (read, not redefined).

ONE new function is written here: `build_classifier_anchored_meanr`. This is
NOT a novel design -- it is the mechanical combination of two already-frozen,
already-verified constructions: mean-R's own `roll_meanR = R.rolling(W).mean()
.shift(1)` (preserving the self-referential-outcome exclusion TFF's own
`build_classifier_anchored` explicitly does NOT need) and the anchor-freeze
threshold logic `build_classifier_anchored` uses (freeze the expanding median
at its last pre-CUTOFF value). Reusing `build_classifier_anchored` directly
would silently drop the `.shift(1)` and reintroduce look-ahead into mean-R's
own realized-outcome classifier -- checked and avoided here, not overlooked.

Reports BOTH axes separately, per POSITIVE_CONTROL_METHOD_FIX.md §6.3's own
explicit instruction: corrected date-correlation-equivalent clearance
(>=2/3 windows) and gate-clearance-direction stability (same sign, all 3
windows) are NOT collapsed into one composite verdict.

Does NOT edit: Q-ORBCUSH-1-closure-falsified.md, its pre-registration, or
ops/instruments/MNQ.md. This is new, additional evidence under a corrected
apparatus -- it supersedes nothing on its own; see this directory's RESULTS.md
for how it is meant to be read alongside the standing closure.

$0/K=0 -- diagnostic/explanatory re-measurement of an already-real historical
pattern under a corrected measurement apparatus, same class as Q-ORBCUSH-1
itself ("not a strategy-candidate proposal"). No real economic/positioning
data pulled by this file (mean-R uses only ORB-MNQ-1's own realized trades,
already on disk). Writes only to this directory.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
MEANR_DIR = HERE.parent / "q_orbcush_1_2026-08" if (HERE.parent / "q_orbcush_1_2026-08").is_dir() else None
ARCHIVE_MEANR_DIR = HERE.parent.parent.parent / "archive" / "q_orbcush_1_2026-08"
PROBE_DIR = HERE.parent / "orbmnq1_cushion_sizing_probe_2026-08-20"
ORBPOS_DIR = HERE.parent / "q_orbpos_1_2026-08"

for p in (PROBE_DIR, ORBPOS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import run_evalseq_orb_intraday as H  # noqa: E402  (harness, imported unchanged)
import stage2_regime_gate as S2  # noqa: E402  (regime-block-building helpers, imported unchanged)
import run_orbpos_tff_probe as A  # noqa: E402  (classify_direction is call-compatible; imported unchanged)
import run_orbpos_positive_control_v2_anchored as V2  # noqa: E402  (the frozen fix; imported unchanged)

# ---------------------------------------------------------------------------
# Recover mean-R's own frozen `build_classifier` without re-typing it: the
# archived script is byte-identical except one stale absolute path (a
# since-deleted worktree). Read it, patch that one line in memory, exec it
# into a private namespace -- never write a modified copy to disk, and never
# touch the archived file itself.
# ---------------------------------------------------------------------------
_MEANR_SRC_PATH = ARCHIVE_MEANR_DIR / "run_meanr_regime_gate.py"
_STALE = 'REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/tradeify-bottleneck-solutions-84e1e6")'
_FIXED = f'REPO = Path(r"{HERE.parent.parent.parent.parent}")'
_src = _MEANR_SRC_PATH.read_text(encoding="utf-8")
assert _src.count(_STALE) == 1, "stale REPO path line not found byte-for-byte -- refusing to patch blind"
_src = _src.replace(_STALE, _FIXED, 1)
_src = _src.replace("if __name__ == \"__main__\":\n    raise SystemExit(main())\n", "")  # do not auto-run on exec
_meanr_ns: dict = {"__name__": "_imported_meanr_regime_gate", "__file__": str(_MEANR_SRC_PATH)}
exec(compile(_src, str(_MEANR_SRC_PATH), "exec"), _meanr_ns)  # noqa: S102 -- trusted local repo file, patched one literal path
M = type("M", (), _meanr_ns)  # attribute-style access, mirrors `import ... as M`

CUTOFF = M.CUTOFF
WINDOWS = M.WINDOWS  # {"W1": 20, "W2": 63, "W3": 126} trades, per Q-ORBCUSH-1's own frozen pre-reg
K = M.K
MIN_TRADES = M.MIN_TRADES
ASSOC_ALPHA = V2.ASSOC_ALPHA
MIN_SEPARATION_PP = V2.MIN_SEPARATION_PP


def build_classifier_anchored_meanr(recon: pd.DataFrame, window: int) -> dict:
    """mean-R's own `roll_meanR` (WITH its `.shift(1)`), anchored (frozen-at-
    CUTOFF) threshold construction (v2_anchored's algorithm, applied here)."""
    recon_sorted = recon.sort_values("date", kind="mergesort").reset_index(drop=True)
    assert recon_sorted["date"].is_unique, "recon has duplicate trade dates"

    Rser = recon_sorted["R"]
    roll_meanR = Rser.rolling(window, min_periods=window).mean().shift(1)  # mean-R's OWN construction, unchanged
    running_median = roll_meanR.expanding(min_periods=1).median()
    valid = roll_meanR.notna()

    dates = pd.DatetimeIndex(recon_sorted["date"])
    pre_mask = np.asarray(dates < CUTOFF)  # DatetimeIndex comparison already returns a plain ndarray
    valid_np = valid.to_numpy()
    pre_valid_positions = np.flatnonzero(pre_mask & valid_np)

    threshold = running_median.copy()
    if len(pre_valid_positions) == 0:
        i_freeze, frozen_value = None, None
    else:
        i_freeze = int(pre_valid_positions[-1])
        frozen_value = float(running_median.iloc[i_freeze])
        threshold[~pre_mask] = frozen_value

    label = pd.Series("WARMUP", index=roll_meanR.index)
    label[valid & (roll_meanR > threshold)] = "HIGHER"
    label[valid & (roll_meanR <= threshold)] = "LOWER"

    # Independent spot-check of the pre-break expanding median (same discipline
    # both source files use) + confirmation the post-break segment is exactly
    # the frozen constant.
    spot_pos = pre_valid_positions[:: max(1, len(pre_valid_positions) // 5)][:5] if len(pre_valid_positions) else np.array([], dtype=int)
    spot_ok = True
    for pos in spot_pos:
        seen = roll_meanR.to_numpy()[: pos + 1]
        seen_valid = seen[~np.isnan(seen)]
        expect = float(np.median(seen_valid))
        got = float(running_median.iloc[pos])
        if not np.isclose(expect, got, rtol=1e-9, atol=1e-9):
            spot_ok = False
    post_valid_thresholds = threshold[valid & pd.Series(~pre_mask, index=roll_meanR.index)].to_numpy()
    freeze_ok = bool(
        frozen_value is None or len(post_valid_thresholds) == 0
        or np.allclose(post_valid_thresholds, frozen_value, rtol=1e-9, atol=1e-9)
    )

    trade_label = pd.Series(label.to_numpy(), index=dates)
    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    daily_label = trade_label.reindex(full_idx).ffill().fillna("WARMUP")

    return dict(
        window=window, recon_sorted=recon_sorted, roll_meanR=roll_meanR, label=label,
        daily_label=daily_label, i_freeze=i_freeze, frozen_value=frozen_value,
        spotcheck_pass=bool(spot_ok and freeze_ok), n_spot_checked=int(len(spot_pos)),
        n_warmup=int((label == "WARMUP").sum()), n_higher=int((label == "HIGHER").sum()),
        n_lower=int((label == "LOWER").sum()),
    )


def main() -> int:
    t0 = time.time()
    report: dict = {"cutoff": str(CUTOFF.date()), "K": K, "windows_trades": WINDOWS,
                     "assoc_alpha": ASSOC_ALPHA, "min_separation_pp": MIN_SEPARATION_PP}

    print("=" * 100)
    print("Q-ORBCUSH-1 REFIT -- trailing mean-R under the corrected (anchored) date-correlation method")
    print("=" * 100)

    thr = H.load_scoring_thresholds()
    print(f"[gate ] {thr.source_path}")
    print(f"[gate ] horizon={thr.horizon}  seeds={thr.seeds}  sims/seed={thr.sims_per_seed}  "
          f"eval_bust_ceiling={thr.eval_bust_ceiling:.1%}  pass_floor={thr.pass_floor:.0%}")

    inst = H.make_inst()
    panel_pkl = H.resolve_panel()
    df = pd.read_pickle(panel_pkl)
    print(f"[data ] {panel_pkl}  rows={len(df):,}  span={df['et'].min()} -> {df['et'].max()}")

    piv, meta = H.ol.session_panel(df, inst)
    bt = H.ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = H.orb_days_with_excursion(piv, meta, inst, entry_bar="include")
    H.assert_mirror_matches_engine(recon, bt)
    print(f"[ctrl ] Control B mirror PASS -- n={len(recon)} triggering days")
    report["n_triggering_days"] = len(recon)

    H.assert_engine_ready(H.TIER)
    fkw_base = H.firm_kwargs(H.TIER, inactivity_off=True, consistency=H.CONSISTENCY_FRAC)
    if fkw_base["dd_lock_offset_usd"] == H.LOCK_AS_PUBLISHED:
        fkw = dict(fkw_base, dd_lock_offset_usd=H.LOCK_UNREACHABLE)
    else:
        fkw = dict(fkw_base)
    assert fkw["profit_target"] == H.TARGET
    assert fkw["starting_equity"] == H.START
    assert fkw["trailing_dd_pct"] == -H.DD / H.START

    print("\n" + "=" * 100)
    print("(1) FIDELITY CONTROL -- flat policy, m=1.0, full panel, k=1/k=2")
    print("=" * 100)
    PUBLISHED = {1: 67.67, 2: 77.01}
    TOL_PP = 2.0
    control, flat_ok_k1 = {}, True
    for k in (1, 2):
        panel_full_k = H.build_k_panel(recon, k)
        bpnl, blow = H.blocks_from_panel(panel_full_k)
        r = H.run_policy_orb(bpnl, blow, H.pol_const(1.0), use_intraday=True,
                              horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
        delta = r["bust_pct"] - PUBLISHED[k]
        ok = abs(delta) <= TOL_PP
        if k == 1:
            flat_ok_k1 = ok
        control[k] = dict(bust_pct=r["bust_pct"], pass_pct=r["pass_pct"], published=PUBLISHED[k],
                           delta_pp=delta, within_tol=ok)
        print(f"  k={k}  bust={r['bust_pct']:.2f}%  published={PUBLISHED[k]:.2f}%  delta={delta:+.2f}pp  "
              f"{'PASS' if ok else 'FAIL'}")
    report["fidelity_control"] = control
    report["fidelity_control_pass_k1"] = bool(flat_ok_k1)
    if not flat_ok_k1:
        print("STOPPING -- fidelity control failed.")
        (HERE / "results_meanr_refit_anchored.json").write_text(json.dumps(report, indent=2, default=str))
        return 2

    panel_full_k1 = H.build_k_panel(recon, K)

    windows_report = {}
    for wname, wsize in WINDOWS.items():
        print("\n" + "=" * 100)
        print(f"{wname} -- window={wsize} trades")
        print("=" * 100)

        clf = build_classifier_anchored_meanr(recon, wsize)
        print(f"[classifier] WARMUP={clf['n_warmup']} HIGHER={clf['n_higher']} LOWER={clf['n_lower']} "
              f"i_freeze={clf['i_freeze']} frozen_value={clf['frozen_value']} "
              f"spotcheck={'PASS' if clf['spotcheck_pass'] else 'FAIL'}")

        avail_date_df = pd.DataFrame({"available_date": clf["recon_sorted"]["date"]})
        assoc = V2.print_level_association(avail_date_df, clf["label"], clf["roll_meanR"])
        print(f"[assoc] n_higher={assoc['n_higher']} n_lower={assoc['n_lower']} "
              f"frac_higher_post={assoc['frac_higher_post']:.1%} frac_lower_post={assoc['frac_lower_post']:.1%} "
              f"separation={assoc['separation_pp']:+.1%} fisher_p={assoc['fisher_p']:.3g} "
              f"point_biserial_r={assoc['point_biserial_r']:.3f} (p={assoc['point_biserial_p']:.3g}) "
              f"corrected_pass={'YES' if assoc['corrected_pass'] else 'NO'}")

        gate_higher = M.gate_check_bucket(panel_full_k1, clf["daily_label"], "HIGHER", thr, fkw)
        gate_lower = M.gate_check_bucket(panel_full_k1, clf["daily_label"], "LOWER", thr, fkw)
        direction = A.classify_direction(gate_higher, gate_lower)
        print(f"[gate] HIGHER cushion pass={gate_higher['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_higher['cushion']['gate_pass'] else 'FAIL'}  |  "
              f"LOWER cushion pass={gate_lower['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_lower['cushion']['gate_pass'] else 'FAIL'}  direction={direction}  "
              f"(elapsed {time.time()-t0:.0f}s)")

        windows_report[wname] = dict(
            window_trades=wsize,
            classifier=dict(n_warmup=clf["n_warmup"], n_higher=clf["n_higher"], n_lower=clf["n_lower"],
                             i_freeze=clf["i_freeze"], frozen_value=clf["frozen_value"],
                             spotcheck_pass=clf["spotcheck_pass"]),
            association=assoc,
            gate={"HIGHER": gate_higher, "LOWER": gate_lower},
            direction=direction,
        )

    report["windows"] = windows_report

    n_corrected_pass = sum(1 for w in windows_report.values() if w["association"]["corrected_pass"])
    directions = [w["direction"] for w in windows_report.values()]
    signed = {d for d in directions if d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT")}
    direction_stable = len(signed) == 1 and all(
        d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT") for d in directions
    )

    report["summary"] = dict(
        corrected_association_windows_passing=n_corrected_pass,
        corrected_association_fires_at_ge2_of_3=bool(n_corrected_pass >= 2),
        directions_by_window={wn: w["direction"] for wn, w in windows_report.items()},
        direction_same_sign_every_window=bool(direction_stable),
    )

    print("\n" + "=" * 100)
    print("SUMMARY -- TWO AXES REPORTED SEPARATELY (per POSITIVE_CONTROL_METHOD_FIX.md Sec6.3)")
    print("=" * 100)
    print(f"  AXIS 1 -- corrected date-correlation-equivalent clears (>=2 of 3)?  {n_corrected_pass}/3  -> "
          f"{'FIRES' if n_corrected_pass >= 2 else 'does not fire'}")
    print(f"  AXIS 2 -- gate-clearance direction same sign, every window?  {'YES' if direction_stable else 'NO'}  "
          f"({report['summary']['directions_by_window']})")

    out = HERE / "results_meanr_refit_anchored.json"
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
