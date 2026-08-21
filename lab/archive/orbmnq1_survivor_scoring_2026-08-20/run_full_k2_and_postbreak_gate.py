#!/usr/bin/env python3
"""Q-ORBSURV-1 Phase 1/2 -- cushion-sizing gate check on the three configurations
today's informal probes never measured: full-panel k=2, and the post-2021-09-28
sub-window in isolation at k=1 and k=2.

Frozen per docs/briefs/pre-registration/Q-ORBSURV-1-verdict-preregistration.md
(2026-08-20). Imports pol_cushion / build_paths_orb / day_loop_intraday /
build_k_panel / blocks_from_panel UNCHANGED from
lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py
-- no re-typed logic. The base module's own top-level sys.path insertions point at
a stale worktree (README's own disclosed portability caveat); this script
pre-populates sys.modules with the CURRENT worktree's orb_lib / core.mc.* /
discovery.prop_survivor_scoring BEFORE loading the base module, so the base
module's own (stale) sys.path.insert calls are no-ops -- Python reuses the
already-imported modules rather than re-resolving them.

The k=1 full-panel reference number is REUSED VERBATIM from
orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json
(bust 0.0%, pass 52.27%) -- not re-derived (forbidden move, parent brief §5).

$0, K=0. No dd_protection/allocation/Pine/rail touch. No locked-parameter edit.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/cursor-grok-dispatch-4de91f")
PROBE_DIR = REPO / "lab" / "analysis" / "c1" / "orbmnq1_cushion_sizing_probe_2026-08-20"
ORB_LIB_DIR = REPO / "lab" / "analysis" / "orb" / "orb_universe_2026-06-22"
OUT_DIR = Path(__file__).resolve().parent

BREAK_DATE = "2021-09-28"  # Q-ORBCUSH-1-established break date (docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md)
MIN_BLOCKS = 20            # frozen Ambiguous-hold floor (pre-registration)

# ---------------------------------------------------------------------------------
# Pre-populate sys.modules from the CURRENT worktree, before the base probe module's
# own top-level sys.path.insert(0, STALE_REPO/...) lines can shadow these imports.
# ---------------------------------------------------------------------------------
for _p in (REPO / "core", REPO / "lab", ORB_LIB_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import orb_lib as ol  # noqa: E402
from mc.preflight import assert_engine_ready, firm_kwargs, summarize_outcomes  # noqa: E402  (unused directly, but forces correct-worktree resolution before base loads)
from mc.simulation import simulate_path  # noqa: E402,F401
from discovery.prop_survivor_scoring import DD_SCALE, NO_PROTECTION_TRIGGER, load_scoring_thresholds  # noqa: E402,F401

_spec = importlib.util.spec_from_file_location(
    "orbmnq1_cushion_probe_base", PROBE_DIR / "run_evalseq_orb_intraday.py"
)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

# Confirm the pre-population actually took (no silent fallback to the stale worktree).
assert base.ol is ol, "base module resolved orb_lib from a different location than expected"


def load_recon():
    thr = base.load_scoring_thresholds()
    panel_pkl = base.resolve_panel()
    df = base.pd.read_pickle(panel_pkl)
    inst = base.make_inst()
    piv, meta = base.ol.session_panel(df, inst)
    bt = base.ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = base.orb_days_with_excursion(piv, meta, inst, entry_bar="include")
    base.assert_mirror_matches_engine(recon, bt)
    return thr, recon, panel_pkl


def gate_check(bust_pct: float, pass_pct: float) -> dict:
    return {
        "bust_pct": bust_pct,
        "pass_pct": pass_pct,
        "bust_ok": bust_pct <= 3.0,
        "pass_ok": pass_pct >= 50.0,
        "floor_ok": bust_pct <= 3.0 and pass_pct >= 50.0,
    }


PASS_AXIS_CAVEAT = (
    "The pass-rate axis under magnitude-resampling on this same sizing mechanism showed "
    "sd=24.17pp and only 50% of resampled histories clearing the combined gate "
    "(ops/instruments/MNQ.md N18) -- a single-history pass% above 50% is not, by itself, "
    "strong evidence the mechanism reliably clears the floor."
)


def main() -> int:
    t0 = time.time()
    report: dict = {"break_date": BREAK_DATE, "min_blocks_floor": MIN_BLOCKS, "pass_axis_caveat": PASS_AXIS_CAVEAT}

    print("=" * 96)
    print("Q-ORBSURV-1 Phase 1/2 -- full-panel k=2 + post-break-only k=1/k=2 cushion-sizing gate check")
    print("=" * 96)

    thr, recon, panel_pkl = load_recon()
    print(f"[data ] {panel_pkl}")
    print(f"[recon] n={len(recon)} (Control B mirror PASS)")
    print(f"[gate ] horizon={thr.horizon}  seeds={thr.seeds}  sims/seed={thr.sims_per_seed}")

    fkw = base.firm_kwargs(base.TIER, inactivity_off=True, consistency=base.CONSISTENCY_FRAC)
    if fkw["dd_lock_offset_usd"] == base.LOCK_AS_PUBLISHED:
        fkw = dict(fkw, dd_lock_offset_usd=base.LOCK_UNREACHABLE)

    # ------------------------------------------------------------ Phase 1: full-panel k=2
    print("\n--- Phase 1: full-panel k=2, cushion sizing ---")
    panel_full_k2 = base.build_k_panel(recon, 2)
    bpnl, blow = base.blocks_from_panel(panel_full_k2)
    n_blocks_full_k2 = len(bpnl)
    r_k2 = base.run_policy_orb(bpnl, blow, base.pol_cushion, use_intraday=True,
                                horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
    gate_k2 = gate_check(r_k2["bust_pct"], r_k2["pass_pct"])
    print(f"  n_blocks={n_blocks_full_k2}  bust={r_k2['bust_pct']:.4f}%  pass={r_k2['pass_pct']:.4f}%  "
          f"floor_ok={gate_k2['floor_ok']}  (elapsed {time.time()-t0:.0f}s)")
    report["full_panel_k2"] = {**gate_k2, "n_blocks": n_blocks_full_k2, "per_seed": r_k2["per_seed"]}

    # ------------------------------------------------------------ Phase 2: post-break-only, k=1 and k=2
    print(f"\n--- Phase 2: post-{BREAK_DATE}-only sub-window, k=1 and k=2 ---")
    postbreak_results = {}
    for k in (1, 2):
        panel_full = base.build_k_panel(recon, k)
        panel_post = panel_full.loc[panel_full.index >= BREAK_DATE]
        try:
            bpnl_p, blow_p = base.blocks_from_panel(panel_post)
        except ValueError as exc:
            postbreak_results[f"k{k}"] = {"error": str(exc), "n_blocks": 0, "ambiguous_hold": True}
            print(f"  k={k}  0 blocks formed -- {exc}")
            continue
        n_blocks_p = len(bpnl_p)
        if n_blocks_p < MIN_BLOCKS:
            postbreak_results[f"k{k}"] = {"n_blocks": n_blocks_p, "ambiguous_hold": True}
            print(f"  k={k}  n_blocks={n_blocks_p} < {MIN_BLOCKS} floor -- AMBIGUOUS-HOLD, no gate number reported")
            continue
        r_p = base.run_policy_orb(bpnl_p, blow_p, base.pol_cushion, use_intraday=True,
                                   horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
        gate_p = gate_check(r_p["bust_pct"], r_p["pass_pct"])
        postbreak_results[f"k{k}"] = {**gate_p, "n_blocks": n_blocks_p, "ambiguous_hold": False, "per_seed": r_p["per_seed"]}
        print(f"  k={k}  n_blocks={n_blocks_p}  bust={r_p['bust_pct']:.4f}%  pass={r_p['pass_pct']:.4f}%  "
              f"floor_ok={gate_p['floor_ok']}  (elapsed {time.time()-t0:.0f}s)")
    report["post_break_only"] = postbreak_results

    # ------------------------------------------------------------ Phase 0 reference (reused, not re-derived)
    orb_json = REPO / "lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json"
    ref = json.loads(orb_json.read_text(encoding="utf-8"))["real_single_history_cushion"]["intraday_honest"]
    report["full_panel_k1_reused_reference"] = {"bust_pct": ref["bust_pct"], "pass_pct": ref["pass_pct"], "floor_ok": ref["bust_pct"] <= 3.0 and ref["pass_pct"] >= 50.0}
    print(f"\n[ref  ] full-panel k=1 (reused verbatim, not re-derived): bust={ref['bust_pct']:.4f}%  pass={ref['pass_pct']:.4f}%")

    # ------------------------------------------------------------ §6 verdict
    any_ambiguous = any(v.get("ambiguous_hold") for v in postbreak_results.values())
    checks = [gate_k2["floor_ok"]] + [v["floor_ok"] for v in postbreak_results.values() if not v.get("ambiguous_hold")]
    if any_ambiguous:
        verdict = "AMBIGUOUS-HOLD"
    elif all(checks) and len(checks) == 3:
        verdict = "RESOLVED"
    else:
        verdict = "FALSIFIED"

    print("\n" + "=" * 96)
    print(f"VERDICT (mechanical, per §6): {verdict}")
    print("=" * 96)
    print(f"\n[caveat] {PASS_AXIS_CAVEAT}")

    report["verdict"] = verdict
    out = OUT_DIR / "full_k2_and_postbreak_results.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")

    return {"RESOLVED": 0, "FALSIFIED": 2, "AMBIGUOUS-HOLD": 3}[verdict]


if __name__ == "__main__":
    raise SystemExit(main())
