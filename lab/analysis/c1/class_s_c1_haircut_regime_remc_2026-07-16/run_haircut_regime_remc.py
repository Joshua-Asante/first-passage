"""Class-S candidate #1 — reversible lifecycle-haircut regime re-MC.

Pre-reg (FROZEN 2026-07-16):
  docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md

Reuses the FROZEN 2026-07-15 regime-gate primitives verbatim
(``run_class_s_c1_regime_gate`` + ``run_class_s_c1_scoring``); the ONLY change is a
book-level lifecycle multiplier applied to ``daily_100k`` (pre-reg §2 PRIMARY injection —
confirmed faithful: ``core/mc/simulation.py`` consistency clause is ratio-based
(max_day/total), hence scale-invariant under a uniform daily haircut). This does NOT edit
any locked parameter, does NOT re-weight the book, and does NOT write ``lifecycle_state.json``
for the CFD legs (book-level, per the G8 intake note).

Implemented as a sibling runner (not an in-place edit to the dated 2026-07-15 driver) so the
scored artifact is untouched; the ``1.00x`` arm is the reproduction control that must match
``class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md`` before the haircut arms are trusted
(pre-reg §6 precondition).

Arms (pre-reg §2, FIXED): 1.00x reproduction control · 0.50x WATCH-1 · 0.25x WATCH-2 —
the ratified ``core/lifecycle.py`` TIER_MULTIPLIER rungs; no fractional value.

median_days_to_pass (pre-reg §2 diagnostic) is NOT surfaced by ``summarize_outcomes``;
pass_rate is reported as the practicality proxy (documented §8 Phase-0 deviation — the
diagnostic is non-gating, so the §6 verdict is unaffected).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
_SCORING = _ROOT / "lab" / "analysis" / "c1" / "class_s_candidate1_scoring_2026-07-15"
for _p in (_ROOT / "core", _ROOT / "lab", str(_SCORING), str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from discovery.prop_survivor_scoring import load_scoring_thresholds  # noqa: E402
import run_class_s_c1_scoring as S  # noqa: E402  (frozen panel build + phase0)
import run_class_s_c1_regime_gate as R  # noqa: E402  (frozen regime primitives)

# Ratified ladder rungs (core/lifecycle.py TIER_MULTIPLIER) — no fractional invention.
ARMS = {"1.00x": 1.00, "0.50x": 0.50, "0.25x": 0.25}

# Frozen 2026-07-15 baseline (REGIME_GATE.md) the 1.00x reproduction control must match.
BASELINE_1P00 = {
    "Tradeify_Select_100K": {"H1_bust": 0.0437, "boot_bust_95th": 0.1037},
    "MFFU_Rapid_100K": {"H1_bust": 0.0436, "boot_bust_95th": 0.1033},
}


def run_arm(name, mult, daily, thr, *, n_sims, n_panels, n_jobs):
    dh = daily * mult
    full = R.full_panel_reference(dh, thr, n_sims=n_sims)
    half = R.part_b_half_panel(dh, thr, n_sims=n_sims)
    boot = R.part_a_bootstrap(
        dh, thr, n_panels=n_panels, n_sims=n_sims, n_jobs=n_jobs
    )
    verdict = R.compose_verdict(full, half, boot, thr)
    return {
        "arm": name,
        "lifecycle_mult": mult,
        "full_panel": full,
        "half_panel": half,
        "bootstrap": {
            k: {kk: vv for kk, vv in v.items() if kk != "panels"}
            for k, v in boot["tiers"].items()
        },
        "verdict": verdict,
    }


def _repro_check(v1p00_tiers) -> dict:
    """1.00x arm vs frozen 2026-07-15 baseline (pre-reg §6 precondition).

    Tolerance: |Δ| ≤ 1.0pp on H1 bust, ≤ 2.0pp on bootstrap-95th (n=100 tail is noisier).
    The gate is fully seeded (thr seeds + BOOT_SEED), so near-exact match is expected;
    the band only absorbs numpy-version drift. A miss routes to AMBIGUOUS (harness defect).
    """
    out = {"ok": True, "tiers": {}}
    for tk, exp in BASELINE_1P00.items():
        h1 = float(v1p00_tiers[tk]["half"]["H1"]["headline_bust"])
        b95 = float(v1p00_tiers[tk]["bootstrap_summary"]["bust_95th"])
        ok = abs(h1 - exp["H1_bust"]) <= 0.010 and abs(b95 - exp["boot_bust_95th"]) <= 0.020
        out["ok"] = out["ok"] and ok
        out["tiers"][tk] = {
            "H1_bust": h1, "H1_baseline": exp["H1_bust"],
            "boot95_bust": b95, "boot95_baseline": exp["boot_bust_95th"], "ok": ok,
        }
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--arms", default="1.00x,0.50x,0.25x")
    ap.add_argument("--smoke", action="store_true", help="n_panels=5, n_sims=200 wiring check")
    ap.add_argument("--n-panels", type=int, default=None)
    ap.add_argument("--n-sims", type=int, default=None)
    ap.add_argument("--n-jobs", type=int, default=-1)
    ap.add_argument("--out-dir", type=Path, default=_HERE)
    args = ap.parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    n_sims = 200 if (args.smoke and args.n_sims is None) else args.n_sims
    n_panels = (5 if args.smoke else 100) if args.n_panels is None else args.n_panels

    # Phase 0 — candidate 2026-07-15 signature + ACTIVE_FIRM + gate ceilings byte-stable.
    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    daily = S.book_daily_at_100k(panel)
    thr = load_scoring_thresholds(S.GATE_PREREG)
    print(
        f"[haircut] panel {meta['panel_span']} n_bdays={meta['n_bdays']} "
        f"daily_len={len(daily)} floor(bust<={thr.eval_bust_ceiling:.1%},pass>={thr.pass_floor:.0%}) "
        f"n_sims={n_sims or thr.sims_per_seed} n_panels={n_panels} smoke={args.smoke} "
        f"arms={args.arms}",
        flush=True,
    )

    arms = [a.strip() for a in args.arms.split(",")]
    results = {}
    for name in arms:
        if name not in ARMS:
            raise SystemExit(f"unknown arm {name!r}; allowed {list(ARMS)}")
        t0 = time.time()
        print(f"[haircut] ===== ARM {name} (x{ARMS[name]}) =====", flush=True)
        res = run_arm(
            name, ARMS[name], daily, thr,
            n_sims=n_sims, n_panels=n_panels, n_jobs=args.n_jobs,
        )
        res["wall_s"] = round(time.time() - t0, 1)
        results[name] = res
        (args.out_dir / f"arm_{name}.json").write_text(
            json.dumps(res, indent=2) + "\n", encoding="utf-8"
        )
        v = res["verdict"]
        print(
            f"[haircut] ARM {name}: overall_gate_pass={v['overall_gate_pass']} "
            f"verdict={v['verdict']!r} ({res['wall_s']:.0f}s)",
            flush=True,
        )
        for tk, t in v["tiers"].items():
            print(
                f"[haircut]   {tk}: full {t['full']['headline_bust']:.2%}/{t['full']['pass_rate']:.1%} "
                f"| H1 {t['half']['H1']['headline_bust']:.2%}/{t['half']['H1']['pass_rate']:.1%} "
                f"| H2 {t['half']['H2']['headline_bust']:.2%} "
                f"| boot95 {t['bootstrap_summary']['bust_95th']:.2%} pass5 {t['bootstrap_summary']['pass_5th']:.1%} "
                f"-> tier_gate={'PASS' if t['gate_pass'] else 'FAIL'}",
                flush=True,
            )

    repro = _repro_check(results["1.00x"]["verdict"]["tiers"]) if "1.00x" in results else None
    if repro is not None:
        print(f"[haircut] reproduction-control (1.00x vs 2026-07-15 baseline): "
              f"{'OK' if repro['ok'] else 'MISMATCH -> AMBIGUOUS (harness defect)'}", flush=True)

    # Least-haircut passing arm (0.50x preferred over 0.25x); 1.00x is control, never a pass.
    passing = [a for a in ("0.50x", "0.25x")
               if a in results and results[a]["verdict"]["overall_gate_pass"]]
    disposition = (
        "RESOLVED-DEPLOYABLE" if passing
        else "FALSIFIED-FRAGILE (accept-with-caveat)"
    )
    chosen = passing[0] if passing else None

    report = {
        "pre_reg": "docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md",
        "candidate_prereg": "docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md",
        "gate_prereg": "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md",
        "arms_run": arms,
        "n_sims": n_sims or thr.sims_per_seed,
        "n_panels": n_panels,
        "smoke": bool(args.smoke),
        "floor": {"bust_ceiling": thr.eval_bust_ceiling, "pass_floor": thr.pass_floor},
        "reproduction_control": repro,
        "panel_meta": meta,
        "arm_verdicts": {k: v["verdict"] for k, v in results.items()},
        "passing_arms": passing,
        "least_haircut_passing_arm": chosen,
        "disposition": (
            disposition if (repro is None or repro["ok"])
            else "AMBIGUOUS (reproduction-control mismatch)"
        ),
        "median_days_note": (
            "median_days_to_pass not surfaced by summarize_outcomes; pass_rate reported as "
            "the practicality proxy (pre-reg §8 Phase-0 documented deviation; non-gating)."
        ),
    }
    (args.out_dir / "haircut_remc_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(f"[haircut] DONE disposition={report['disposition']} chosen_arm={chosen}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
