"""W1 4th partition -- intraday-honest 6mo-block bootstrap at the 0.50x arm.

Completes the one cell the 2026-08-09 W1 packet declared out of scope. Quoting its own
RESULTS: *"Bootstrap-95th remains unmeasured on the honest clock."* The frozen gate scores
{full, H1, H2, bootstrap-95th} x {Tradeify_Select_100K, MFFU_Rapid_100K}; W1 landed six of
those eight cells (all PASS) and dropped the bootstrap for the Cursor packet's wall-clock.

This run scores each resampled panel on BOTH clocks from one shared draw:
  * EOD control  -- must reproduce the published corrected-geometry bootstrap-95th
                    (Tradeify 1.20%, eval_shape_diagnostics_2026-07-28 §(a)).
  * Honest       -- the new measurement.
A control that does not reproduce is a harness defect, not a finding.

NOTHING is re-decided here. Ceiling / pass floor / seeds / sims / horizon are parsed from
the pre-registration by ``load_scoring_thresholds``; block size (126 bd), panel count (100)
and BOOT_SEED (20260715) are imported from the retrieved regime-gate module, never retyped.

Owner ADR : docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md
Contract  : docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md (P3)
Prereg    : docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md
Gate      : parsed at runtime from prop_survivor_scoring.DEFAULT_PREREG

$0 / K=0. No locked surface, no allocation, no Pine, no dd_protection constant, no arming.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

for _k, _v in (
    ("OMP_NUM_THREADS", "1"),
    ("MKL_NUM_THREADS", "1"),
    ("OPENBLAS_NUM_THREADS", "1"),
    ("NUMEXPR_NUM_THREADS", "1"),
):
    os.environ.setdefault(_k, _v)

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
_W1 = _ROOT / "lab" / "analysis" / "c1" / "class_s_c1_haircut_regime_remc_2026-07-16"
# _HERE first: the vendored (byte-identical, retrieved) frozen primitives must win.
for _p in (str(_HERE), str(_ROOT / "core"), str(_ROOT / "lab"), str(_W1)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import firm_rules  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    assert_intraday_channel_nonvacuous,
    load_scoring_thresholds,
    paired_blocks_from_daily,
)

_argv_saved = list(sys.argv)
sys.argv = [sys.argv[0]]
import run_class_s_c1_scoring as S  # noqa: E402
import run_class_s_c1_regime_gate as R  # noqa: E402
import run_w1_intraday_both_halves as W1  # noqa: E402  (honest-clock derivation)
sys.argv = _argv_saved

import _boot_paired as BP  # noqa: E402

LOCKING_TIERS = ("Tradeify_Select_100K", "MFFU_Rapid_100K")
UNREACHABLE = 1_000_000.0
ARM_MULT = 0.50

# Published pins this run must reproduce / is compared against (NOT thresholds).
PUBLISHED = {
    "eod_corrected_bust_95th": 0.0120,  # eval_shape_diagnostics_2026-07-28 §(a), Tradeify
    "eod_corrected_pass_5th": 0.955,    # same source
    "eod_defective_bust_95th": 0.007686666666666665,  # haircut_remc_report.json (dd_lock=100)
}
CONTROL_TOL_BUST = 0.020  # same tolerance the haircut runner used on boot-95th (n=100 tail)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--smoke", action="store_true", help="n_panels=5, n_sims=200 wiring check")
    ap.add_argument("--n-panels", type=int, default=None)
    ap.add_argument("--n-sims", type=int, default=None)
    ap.add_argument("--n-jobs", type=int, default=-1)
    ap.add_argument("--tiers", default=",".join(LOCKING_TIERS))
    ap.add_argument("--out", type=Path, default=_HERE / "w1_bootstrap_honest_report.json")
    args = ap.parse_args(argv)

    n_panels = (5 if args.smoke else R.N_PANELS_DEFAULT) if args.n_panels is None else args.n_panels
    n_sims = 200 if (args.smoke and args.n_sims is None) else args.n_sims
    tiers = tuple(t for t in args.tiers.split(",") if t)

    # ---- Phase 0 (frozen): panel signature + live-tier + prereg intactness -------------
    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    daily = S.book_daily_at_100k(panel)
    thr = load_scoring_thresholds(S.GATE_PREREG)
    print(
        f"[w1b] panel {meta['panel_span']} n={meta['n_bdays']} | gate "
        f"bust<={thr.eval_bust_ceiling:.1%} pass>={thr.pass_floor:.0%} "
        f"seeds={thr.seeds} sims={thr.sims_per_seed} horizon={thr.horizon} | arm={ARM_MULT}x",
        flush=True,
    )
    print(
        f"[w1b] bootstrap frozen params: n_panels={n_panels} "
        f"block={R.BLOCK_SIZE_BDAYS}bd seed={R.BOOT_SEED}",
        flush=True,
    )

    # ---- Honest-clock channel (reuses the W1 derivation verbatim) ----------------------
    print("[w1b] deriving bar-level intraday_low (W1 derivation, unmodified) ...", flush=True)
    t0 = time.time()
    intraday, cov = W1.build_book_intraday_low(panel, meta)
    print(
        f"[w1b] intraday_low ready in {time.time() - t0:.1f}s "
        f"min={float(intraday.min()):.2f} neg_days={int(np.sum(intraday < 0))}",
        flush=True,
    )
    assert len(intraday) == len(daily)

    # Production default geometry (never restore-to-100).
    for t in LOCKING_TIERS:
        firm_rules.FIRM_RULES[t]["dd_lock_offset_usd"] = UNREACHABLE

    # ---- Mandatory non-vacuity guard (frozen Phase-4 §1), same params as W1 -----------
    print("[w1b] non-vacuity guard (1.00x book, short horizon) ...", flush=True)
    from dataclasses import replace

    thr_nv = replace(thr, horizon=W1.NONVAC_HORIZON)
    b_p, b_l = paired_blocks_from_daily(daily, intraday)
    nv = assert_intraday_channel_nonvacuous(
        b_p, b_l, thresholds=thr_nv, firm_key="Tradeify_Select_100K",
        n_sims=W1.NONVAC_SIMS, horizon=W1.NONVAC_HORIZON,
    )
    print(
        f"[w1b] non-vacuity OK -- eod bust={nv['eod']['headline_bust']:.4f} "
        f"real bust={nv['real']['headline_bust']:.4f}",
        flush=True,
    )

    # ---- Haircut co-moves BOTH channels (book size), never dd_scale -------------------
    dh = daily * ARM_MULT
    ih = intraday * ARM_MULT

    # ---- Guard: the paired draw reproduces the EOD draw's P&L series exactly ----------
    draw_guard = BP.assert_paired_draw_matches_eod(
        dh, ih,
        target_len=int(dh.size), block_size=R.BLOCK_SIZE_BDAYS, boot_seed=R.BOOT_SEED,
        pids=range(min(10, n_panels)),
    )
    print(f"[w1b] paired-draw equivalence OK on pids {draw_guard['pids_checked']}", flush=True)

    out = {
        "run": "W1 4th partition -- intraday-honest 6mo-block bootstrap, 0.50x arm",
        "date": "2026-09-02",
        "adr": "docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md",
        "contract": "docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md",
        "prereg": str(S.GATE_PREREG.relative_to(_ROOT)).replace("\\", "/"),
        "geometry": "intraday_low from 15m bars; dd_lock_offset_usd unreachable (worker-attested)",
        "arm": ARM_MULT,
        "gate": {
            "bust_ceiling": thr.eval_bust_ceiling,
            "pass_floor": thr.pass_floor,
            "seeds": list(thr.seeds),
            "sims_per_seed": thr.sims_per_seed,
            "horizon": thr.horizon,
        },
        "bootstrap_params": {
            "n_panels": int(n_panels),
            "block_size_bdays": int(R.BLOCK_SIZE_BDAYS),
            "boot_seed": int(R.BOOT_SEED),
            "n_sims_override": n_sims,
        },
        "panel_meta": meta,
        "intraday_coverage": cov,
        "nonvacuity": {
            "eod_bust": float(nv["eod"]["headline_bust"]),
            "eod_pass": float(nv["eod"]["pass_rate"]),
            "real_bust": float(nv["real"]["headline_bust"]),
            "real_pass": float(nv["real"]["pass_rate"]),
            "ok": True,
        },
        "paired_draw_guard": draw_guard,
        "published_pins": PUBLISHED,
        "smoke": bool(args.smoke),
        "tiers": {},
    }

    for firm_key in tiers:
        print(f"[w1b] ===== {firm_key} =====", flush=True)
        ck = _HERE / f"ckpt_{firm_key}{'_smoke' if args.smoke else ''}.json"
        res = BP.part_a_bootstrap_paired(
            dh, ih, thr, firm_key,
            n_panels=n_panels, block_size=R.BLOCK_SIZE_BDAYS, boot_seed=R.BOOT_SEED,
            n_sims=n_sims, n_jobs=args.n_jobs, checkpoint_path=ck,
        )
        eod, hon = res["eod"], res["honest"]
        # Explicit control comparison (published pin vs this run's EOD arm).
        ctrl = {
            "published_bust_95th": PUBLISHED["eod_corrected_bust_95th"],
            "measured_bust_95th": eod["bust_95th"],
            "abs_delta": abs(eod["bust_95th"] - PUBLISHED["eod_corrected_bust_95th"]),
            "tol": CONTROL_TOL_BUST,
            "ok": abs(eod["bust_95th"] - PUBLISHED["eod_corrected_bust_95th"]) <= CONTROL_TOL_BUST,
            "note": "published pin is Tradeify_Select_100K; MFFU historically returns the same series",
        }
        res["control_vs_published_eod"] = ctrl
        res["floor_verdict"] = {
            "eod_bootstrap_ok": eod["bootstrap_ok"],
            "honest_bootstrap_ok": hon["bootstrap_ok"],
            "delta_bust_95th_pp": (hon["bust_95th"] - eod["bust_95th"]) * 100.0,
        }
        out["tiers"][firm_key] = res
        print(
            f"[w1b] {firm_key} EOD    bust95={eod['bust_95th']:.4%} pass5={eod['pass_5th']:.2%} "
            f"-> {'PASS' if eod['bootstrap_ok'] else 'FAIL'} "
            f"(control vs published {PUBLISHED['eod_corrected_bust_95th']:.2%}: "
            f"{'MATCH' if ctrl['ok'] else 'MISMATCH'})",
            flush=True,
        )
        print(
            f"[w1b] {firm_key} HONEST bust95={hon['bust_95th']:.4%} pass5={hon['pass_5th']:.2%} "
            f"-> {'PASS' if hon['bootstrap_ok'] else 'FAIL'} "
            f"(delta {res['floor_verdict']['delta_bust_95th_pp']:+.2f}pp, "
            f"{res['n_panels_arms_differ']}/{n_panels} panels differ)",
            flush=True,
        )

    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"[w1b] written {args.out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
