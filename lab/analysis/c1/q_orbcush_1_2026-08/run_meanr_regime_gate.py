#!/usr/bin/env python3
"""Q-ORBCUSH-1 Phase 0-1: trailing (causal) mean-R classifier of ORB-MNQ-1's own
realized trades -> re-run the cushion-proportional-sizing Tradeify survivor-scoring
gate on each of the two buckets (higher-edge / lower-edge), at each of the three
pre-registered windows (20/63/126 trades), k=1.

Frozen spec (authoritative): docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md
Brief (context, not authoritative on numbers): docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md

$0/K=0. Imports lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/
run_evalseq_orb_intraday.py UNCHANGED (day_loop_intraday / build_paths_orb /
run_policy_orb / pol_cushion / pol_const / blocks_from_panel / build_k_panel /
orb_days_with_excursion / resolve_panel / make_inst / assert_mirror_matches_engine
are NOT retyped here -- already independently, adversarially verified across two
prior rounds, per this brief's own Phase-0 instructions). Also imports
stage2_regime_gate.py's contiguous_runs/build_regime_blocks helpers UNCHANGED --
same regime-bucket-block-construction discipline the prior (REFUTED) vol-regime
round used, reused here as instructed rather than retyped.

Writes only under this directory (the brief's own execution home). Touches no
locked/frozen repo file.

--------------------------------------------------------------------------------
CLASSIFIER DESIGN NOTE -- reconciling the two descriptions of "daily granularity"
--------------------------------------------------------------------------------
The pre-registration file (authoritative) specifies a TRADE-INDEXED rolling window:
"rolling window over the trade sequence (not calendar days ...) ... the classifier
is trade-indexed to match how mean-R is naturally computed", with a `.shift(1)`-
equivalent causal lag and an EXPANDING, causal running-median threshold computed
over that trailing series itself ("never a full-sample statistic").

The orchestrating task prompt's own restatement of Phase 1 says: "build this at
daily granularity (one classification value per calendar/session day, using all
realized trade R's strictly before that day), which naturally tracks the trade
sequence too -- state explicitly if you interpret this differently and why."

These are reconciled, not contradictory, but the reconciliation is NOT a literal
identity and is stated here explicitly per both documents' own instruction to flag
any interpretation delta:

  1. The classification VALUE at trade i is a rolling mean over the trailing W
     trades (W in {20, 63, 126}), NOT an expanding mean over ALL trades before
     that day. The pre-registration's window table (rationale tied 1:1 to the
     prior vol-regime round's own rolling-window design, e.g. `tr.rolling(63)
     .mean().shift(1)`) is unambiguous on this point and is treated as
     authoritative over the orchestrator's looser paraphrase ("using all realized
     trade R's strictly before that day" would describe an ever-widening expanding
     window, which is a different, and untested, construct).
  2. This value is computed at TRADE granularity (ORB-MNQ-1 fires ~1 trade/
     triggering day), then mapped onto the full business-day panel by (a) indexing
     the trade-level label by its trade's calendar date, (b) reindexing onto the
     full `pd.bdate_range` panel, (c) forward-filling -- so every non-trigger day
     (the ~1% with no ORB trade) inherits the most recent PRIOR trade's
     classification, never a future one. This IS "one classification value per
     calendar/session day" and IS strictly causal, so it satisfies the
     orchestrator's daily-granularity framing without changing what the rolling
     window itself measures. No future information enters via the forward-fill
     step (ffill only ever copies a value backward in TIME never forward).

The bucket-split threshold is the expanding (causal), NEVER full-sample, running
median of the trailing series itself -- `roll.expanding(min_periods=1).median()`,
which pandas computes skipping not-yet-valid (NaN, pre-warmup) entries, verified
empirically before use (see report's `expanding_median_spotcheck`). This is the
literal implementation of "the trailing series' own running median up to that
point" (pre-registration, verbatim) and explicitly NOT stage2_regime_gate.py's own
full-sample `roll_full[valid].median()` (that file's own docstring flags this as a
descriptive-only shortcut, "NOT a live-tradeable rule as-is" -- Q-ORBCUSH-1's own
§5 Forbidden Moves rules this out entirely for this Q, hence the change).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/tradeify-bottleneck-solutions-84e1e6")
PROBE_DIR = REPO / "lab" / "analysis" / "c1" / "orbmnq1_cushion_sizing_probe_2026-08-20"
OUT_DIR = Path(__file__).resolve().parent

if str(PROBE_DIR) not in sys.path:
    sys.path.insert(0, str(PROBE_DIR))

import run_evalseq_orb_intraday as H  # noqa: E402  (harness, imported unchanged)
import stage2_regime_gate as S2  # noqa: E402  (regime-block-building helpers, imported unchanged)

CUTOFF = pd.Timestamp("2021-09-28")
WINDOWS = {"W1": 20, "W2": 63, "W3": 126}  # trades, per pre-registration
K = 1
MIN_TRADES = 30  # sparsity floor per §4 Ambiguous-hold clause

DATE_CORR_HIGH_FLOOR = 0.75   # higher-edge bucket post-cutoff frac must be >= this
DATE_CORR_LOW_CEIL = 0.40     # lower-edge bucket post-cutoff frac must be <= this


def build_classifier(recon: pd.DataFrame, window: int) -> dict:
    """Trade-indexed, strictly causal rolling-mean-R classifier + expanding causal
    running-median bucket threshold. Returns per-trade label series (date-indexed)
    plus the full-panel (business-day, ffilled) label series, and diagnostics."""
    recon_sorted = recon.sort_values("date", kind="mergesort").reset_index(drop=True)
    assert recon_sorted["date"].is_unique, "recon has duplicate trade dates -- classifier assumes 1 trade/day"

    Rser = recon_sorted["R"]
    # trailing mean over the W trades strictly BEFORE trade i (i-W .. i-1); shift(1)
    # applied to a rolling(W) window already ending at i-1 is what makes trade i's
    # OWN R excluded from its own classification value -- no look-ahead.
    roll_meanR = Rser.rolling(window, min_periods=window).mean().shift(1)

    # expanding, causal running median of the trailing series itself. pandas skips
    # not-yet-valid (NaN) entries when accumulating -- verified below.
    running_median = roll_meanR.expanding(min_periods=1).median()

    valid = roll_meanR.notna()
    label = pd.Series("WARMUP", index=roll_meanR.index)
    label[valid & (roll_meanR > running_median)] = "HIGHER"
    label[valid & (roll_meanR <= running_median)] = "LOWER"

    # spot-check: expanding median at trade i (valid) must equal median of every
    # PRIOR valid roll_meanR value up to and including i -- computed independently
    # via a plain python loop (not pandas) at 5 spot positions, to catch a pandas
    # NaN-handling surprise before trusting it.
    valid_positions = np.flatnonzero(valid.to_numpy())
    spot_positions = valid_positions[:: max(1, len(valid_positions) // 5)][:5] if len(valid_positions) else []
    spot_ok = True
    for pos in spot_positions:
        seen = roll_meanR.to_numpy()[: pos + 1]
        seen_valid = seen[~np.isnan(seen)]
        expect = float(np.median(seen_valid))
        got = float(running_median.iloc[pos])
        if not np.isclose(expect, got, rtol=1e-9, atol=1e-9):
            spot_ok = False

    trade_label = pd.Series(label.to_numpy(), index=pd.DatetimeIndex(recon_sorted["date"]))

    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    daily_label = trade_label.reindex(full_idx).ffill()
    daily_label = daily_label.fillna("WARMUP")  # any leading gap before first valid label

    n_warmup_trades = int((label == "WARMUP").sum())
    n_higher_trades = int((label == "HIGHER").sum())
    n_lower_trades = int((label == "LOWER").sum())

    return dict(
        window=window,
        recon_sorted=recon_sorted,
        roll_meanR=roll_meanR,
        running_median=running_median,
        trade_label=trade_label,
        daily_label=daily_label,
        full_idx=full_idx,
        expanding_median_spotcheck_pass=bool(spot_ok),
        n_spot_checked=len(spot_positions),
        n_trades_total=len(recon_sorted),
        n_warmup_trades=n_warmup_trades,
        n_higher_trades=n_higher_trades,
        n_lower_trades=n_lower_trades,
    )


def date_correlation(clf: dict) -> dict:
    """Fraction of each bucket's DAYS (full business-day panel, post-ffill,
    WARMUP days excluded from both buckets) that fall on/after 2021-09-28."""
    daily_label = clf["daily_label"]
    idx_higher = daily_label.index[daily_label == "HIGHER"]
    idx_lower = daily_label.index[daily_label == "LOWER"]
    frac_higher_post = float((idx_higher >= CUTOFF).mean()) if len(idx_higher) else float("nan")
    frac_lower_post = float((idx_lower >= CUTOFF).mean()) if len(idx_lower) else float("nan")
    return dict(
        n_higher_days=int(len(idx_higher)),
        n_lower_days=int(len(idx_lower)),
        frac_higher_days_post_cutoff=frac_higher_post,
        frac_lower_days_post_cutoff=frac_lower_post,
        date_corr_pass=bool(
            (frac_higher_post >= DATE_CORR_HIGH_FLOOR) and (frac_lower_post <= DATE_CORR_LOW_CEIL)
        ) if len(idx_higher) and len(idx_lower) else False,
    )


def gate_check_bucket(panel_full: pd.DataFrame, daily_label: pd.Series, bucket_name: str,
                       thr, fkw) -> dict:
    """Reuses stage2_regime_gate.build_regime_blocks (contiguous-run splitting +
    blocks_from_panel per run) UNCHANGED, then H.run_policy_orb UNCHANGED, for
    flat(k=1) and cushion(k=1)."""
    label_full = daily_label.reindex(panel_full.index)
    bpnl, blow, meta = S2.build_regime_blocks(panel_full, label_full, bucket_name)

    flat = H.run_policy_orb(bpnl, blow, H.pol_const(1.0), use_intraday=True,
                             horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
    cush = H.run_policy_orb(bpnl, blow, H.pol_cushion, use_intraday=True,
                             horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)

    def gate(bust_pct, pass_pct):
        return bool(bust_pct <= thr.eval_bust_ceiling * 100.0 and pass_pct >= thr.pass_floor * 100.0)

    flat_pass = gate(flat["bust_pct"], flat["pass_pct"])
    cush_pass = gate(cush["bust_pct"], cush["pass_pct"])

    return dict(
        meta=meta,
        flat=dict(bust_pct=flat["bust_pct"], pass_pct=flat["pass_pct"], gate_pass=flat_pass),
        cushion=dict(bust_pct=cush["bust_pct"], pass_pct=cush["pass_pct"], gate_pass=cush_pass),
    )


def main():
    t0 = time.time()
    report: dict = {"cutoff": str(CUTOFF.date()), "K": K, "windows_trades": WINDOWS,
                     "min_trades_sparsity_floor": MIN_TRADES}

    print("=" * 100)
    print("Q-ORBCUSH-1 Phase 0-1 -- trailing mean-R causal classifier vs cushion-sizing gate")
    print("=" * 100)

    thr = H.load_scoring_thresholds()
    print(f"[gate ] {thr.source_path}")
    print(f"[gate ] horizon={thr.horizon}  seeds={thr.seeds}  sims/seed={thr.sims_per_seed}  "
          f"eval_bust_ceiling={thr.eval_bust_ceiling:.1%}  pass_floor={thr.pass_floor:.0%}")
    report["gate_thresholds"] = dict(eval_bust_ceiling_pct=thr.eval_bust_ceiling * 100.0,
                                      pass_floor_pct=thr.pass_floor * 100.0,
                                      horizon=thr.horizon, seeds=list(thr.seeds),
                                      sims_per_seed=thr.sims_per_seed)

    # ---------------------------------------------------------------- data + Control B mirror
    inst = H.make_inst()
    panel_pkl = H.resolve_panel()
    df = pd.read_pickle(panel_pkl)
    print(f"[data ] {panel_pkl}")
    print(f"[data ] rows={len(df):,}  span={df['et'].min()} -> {df['et'].max()}")

    piv, meta = H.ol.session_panel(df, inst)
    bt = H.ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = H.orb_days_with_excursion(piv, meta, inst, entry_bar="include")

    print("\n--- Control B (reused unchanged): mirror vs orb_lib.orb_backtest ---")
    H.assert_mirror_matches_engine(recon, bt)
    print(f"  PASS -- n={len(recon)} triggering days")
    report["n_triggering_days"] = len(recon)

    H.assert_engine_ready(H.TIER)
    fkw_base = H.firm_kwargs(H.TIER, inactivity_off=True, consistency=H.CONSISTENCY_FRAC)
    if fkw_base["dd_lock_offset_usd"] == H.LOCK_AS_PUBLISHED:
        fkw = dict(fkw_base, dd_lock_offset_usd=H.LOCK_UNREACHABLE)
        print("[firm ] FIRM_RULES still ships the as-published lock; overriding to unreachable (matches published headline).")
    else:
        fkw = dict(fkw_base)
        print(f"[firm ] FIRM_RULES already ships dd_lock_offset_usd={fkw_base['dd_lock_offset_usd']:,.0f} (no override needed).")
    assert fkw["profit_target"] == H.TARGET
    assert fkw["starting_equity"] == H.START
    assert fkw["trailing_dd_pct"] == -H.DD / H.START

    # ---------------------------------------------------------------- (1) FIDELITY CONTROL
    print("\n" + "=" * 100)
    print("(1) FIDELITY CONTROL -- flat (non-cushion) policy, m=1.0, full panel, k=1 and k=2")
    print("=" * 100)
    PUBLISHED = {1: 67.67, 2: 77.01}
    TOL_PP = 2.0
    control = {}
    flat_ok_k1 = True
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
        print(f"  k={k}  bust={r['bust_pct']:.2f}%  pass={r['pass_pct']:.2f}%  "
              f"published={PUBLISHED[k]:.2f}%  delta={delta:+.2f}pp  {'PASS' if ok else 'FAIL'}  "
              f"(elapsed {time.time()-t0:.0f}s)")

    report["fidelity_control"] = control
    report["fidelity_control_pass_k1"] = bool(flat_ok_k1)
    print(f"\nFIDELITY CONTROL (k=1, the required check): {'PASS' if flat_ok_k1 else 'FAIL'}")

    if not flat_ok_k1:
        print("STOPPING -- fidelity control at k=1 did not reproduce the published intraday-honest "
              "bust rate within tolerance. Not proceeding to the regime classifier on an unvalidated harness.")
        out = OUT_DIR / "results_meanr_regime_gate.json"
        out.write_text(json.dumps(report, indent=2, default=str))
        print(f"[write] {out}")
        return 2

    # ---------------------------------------------------------------- (2) classifier + gate, per window
    panel_full_k1 = H.build_k_panel(recon, K)

    windows_report = {}
    for wname, wsize in WINDOWS.items():
        print("\n" + "=" * 100)
        print(f"{wname} -- window={wsize} trades")
        print("=" * 100)

        clf = build_classifier(recon, wsize)
        print(f"[classifier] n_trades_total={clf['n_trades_total']}  "
              f"WARMUP={clf['n_warmup_trades']}  HIGHER={clf['n_higher_trades']}  LOWER={clf['n_lower_trades']}  "
              f"expanding-median spot-check ({clf['n_spot_checked']} pts): "
              f"{'PASS' if clf['expanding_median_spotcheck_pass'] else 'FAIL'}")

        dc = date_correlation(clf)
        print(f"[date-corr] HIGHER bucket: n_days={dc['n_higher_days']}  "
              f"post-cutoff frac={dc['frac_higher_days_post_cutoff']:.1%}  (need >= {DATE_CORR_HIGH_FLOOR:.0%})")
        print(f"[date-corr] LOWER  bucket: n_days={dc['n_lower_days']}  "
              f"post-cutoff frac={dc['frac_lower_days_post_cutoff']:.1%}  (need <= {DATE_CORR_LOW_CEIL:.0%})")
        print(f"[date-corr] window date-correlation condition: {'FIRES (pass)' if dc['date_corr_pass'] else 'does not fire (fail)'}")

        gate_higher = gate_check_bucket(panel_full_k1, clf["daily_label"], "HIGHER", thr, fkw)
        gate_lower = gate_check_bucket(panel_full_k1, clf["daily_label"], "LOWER", thr, fkw)

        print(f"[gate] HIGHER  n_blocks={gate_higher['meta']['n_blocks']}  "
              f"flat: bust={gate_higher['flat']['bust_pct']:.2f}% pass={gate_higher['flat']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_higher['flat']['gate_pass'] else 'FAIL'}  |  "
              f"cushion: bust={gate_higher['cushion']['bust_pct']:.2f}% pass={gate_higher['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_higher['cushion']['gate_pass'] else 'FAIL'}")
        print(f"[gate] LOWER   n_blocks={gate_lower['meta']['n_blocks']}  "
              f"flat: bust={gate_lower['flat']['bust_pct']:.2f}% pass={gate_lower['flat']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_lower['flat']['gate_pass'] else 'FAIL'}  |  "
              f"cushion: bust={gate_lower['cushion']['bust_pct']:.2f}% pass={gate_lower['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_lower['cushion']['gate_pass'] else 'FAIL'}   (elapsed {time.time()-t0:.0f}s)")

        direction_higher_clears_lower_does_not = bool(
            gate_higher["cushion"]["gate_pass"] and not gate_lower["cushion"]["gate_pass"]
        )
        direction_lower_clears_higher_does_not = bool(
            gate_lower["cushion"]["gate_pass"] and not gate_higher["cushion"]["gate_pass"]
        )
        both_clear = bool(gate_higher["cushion"]["gate_pass"] and gate_lower["cushion"]["gate_pass"])
        neither_clears = bool(not gate_higher["cushion"]["gate_pass"] and not gate_lower["cushion"]["gate_pass"])
        if direction_higher_clears_lower_does_not:
            direction = "HIGHER_CLEARS_LOWER_DOES_NOT"
        elif direction_lower_clears_higher_does_not:
            direction = "LOWER_CLEARS_HIGHER_DOES_NOT"
        elif both_clear:
            direction = "BOTH_CLEAR"
        elif neither_clears:
            direction = "NEITHER_CLEARS"
        else:
            direction = "UNDEFINED"
        print(f"[direction] {wname}: {direction}")

        sparse_flag = (clf["n_higher_trades"] < MIN_TRADES) or (clf["n_lower_trades"] < MIN_TRADES)
        if sparse_flag:
            print(f"[sparsity] {wname}: FLAGGED -- HIGHER n_trades={clf['n_higher_trades']}  "
                  f"LOWER n_trades={clf['n_lower_trades']}  (floor={MIN_TRADES})")

        windows_report[wname] = dict(
            window_trades=wsize,
            classifier=dict(
                n_trades_total=clf["n_trades_total"], n_warmup_trades=clf["n_warmup_trades"],
                n_higher_trades=clf["n_higher_trades"], n_lower_trades=clf["n_lower_trades"],
                expanding_median_spotcheck_pass=clf["expanding_median_spotcheck_pass"],
            ),
            date_correlation=dc,
            gate={"HIGHER": gate_higher, "LOWER": gate_lower},
            direction=direction,
            sparsity_flag=bool(sparse_flag),
        )

    report["windows"] = windows_report

    # ---------------------------------------------------------------- (3) frozen trigger facts
    n_date_corr_pass = sum(1 for w in windows_report.values() if w["date_correlation"]["date_corr_pass"])
    directions = [w["direction"] for w in windows_report.values()]
    directional_signs = {d for d in directions if d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT")}
    direction_stable = len(directional_signs) <= 1 and all(
        d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT") for d in directions
    )
    any_sparse = any(w["sparsity_flag"] for w in windows_report.values())

    report["summary"] = dict(
        date_correlation_windows_passing=n_date_corr_pass,
        date_correlation_fires_at_ge2_of_3=bool(n_date_corr_pass >= 2),
        directions_by_window={wn: w["direction"] for wn, w in windows_report.items()},
        direction_stable_no_sign_flip=bool(direction_stable),
        any_window_sparse=bool(any_sparse),
    )

    print("\n" + "=" * 100)
    print("FROZEN TRIGGER FACTS (raw -- no Accept/Reject verdict computed here, per task scope)")
    print("=" * 100)
    print(f"  date-correlation clears (>=2 of 3 windows)?  {n_date_corr_pass}/3  -> "
          f"{'FIRES' if n_date_corr_pass >= 2 else 'does not fire'}")
    print(f"  direction stable (no sign-flip across all 3)? {'YES' if direction_stable else 'NO'}  "
          f"(per-window: {report['summary']['directions_by_window']})")
    print(f"  any window bucket-sparse (n<{MIN_TRADES} trades)? {'YES' if any_sparse else 'NO'}")

    out = OUT_DIR / "results_meanr_regime_gate.json"
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
