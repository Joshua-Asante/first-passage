"""Q-FUNNEL-1 — 36-cell funnel EV sweep + mechanical §6 gate application.

Grid (frozen pre-reg): 3 rungs × 2 retry policies × 3 edge scenarios × 2 regime
halves = 36 cells. Writes ``sweep_results.json`` + ``RESULTS.md``.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import funnel as F  # noqa: E402


def _ev_to_dict(ev: F.EvDayResult) -> dict:
    return {
        "ev_day": ev.ev_day,
        "mean_net": ev.mean_net,
        "mean_days": ev.mean_days,
        "n_lineages": ev.n_lineages,
        "boot_5th": ev.boot_5th,
        "boot_95th": ev.boot_95th,
    }


def run_sweep(
    *,
    n_lineages: int = 500,
    seed: int = 42,
    smoke: bool = False,
) -> dict:
    panel, meta, _daily_hist = F.load_c1_panel()
    if smoke:
        n_lineages = min(n_lineages, 40)

    cells: dict = {}
    rows = []
    t0 = time.time()
    cell_i = 0
    total = len(F.RUNGS) * len(F.RETRY_POLICIES) * len(F.EDGE_SCENARIOS) * 2

    for edge in F.EDGE_SCENARIOS:
        edged = F.apply_edge_scenario(panel, edge)
        for half in ("H1", "H2"):
            daily = F.regime_half_slice(edged, half)
            for policy in F.RETRY_POLICIES:
                for rung in F.RUNGS:
                    cell_i += 1
                    print(
                        f"[funnel] cell {cell_i}/{total} "
                        f"rung={rung} policy={policy} edge={edge} half={half} "
                        f"n={n_lineages}",
                        flush=True,
                    )
                    ev = F.run_cell(
                        daily,
                        rung=rung,
                        policy=policy,
                        n_lineages=n_lineages,
                        seed=seed + cell_i,
                    )
                    key = (rung, policy, edge, half)
                    cells[key] = ev
                    rows.append(
                        {
                            "rung": rung,
                            "policy": policy,
                            "edge": edge,
                            "half": half,
                            **_ev_to_dict(ev),
                        }
                    )

    gate = F.apply_section6_gate(cells)
    report = {
        "pre_reg": "docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md",
        "panel_meta": meta,
        "eval_fee_usd": F.EVAL_FEE_USD,
        "eval_fee_promo_usd": F.EVAL_FEE_PROMO_USD,
        "max_retries": F.MAX_RETRIES,
        "materiality_relative": F.MATERIALITY_RELATIVE,
        "n_lineages": n_lineages,
        "smoke": smoke,
        "wall_s": round(time.time() - t0, 1),
        "cells": rows,
        "gate": gate,
        "section05_resolutions": {
            "A": "no_clawback_prior_payouts",
            "B": "same_week_block_bootstrap_continuation",
            "C": "winning_day_counter_resets_after_payout",
            "D": "per_leg_demean_before_recombine",
        },
    }
    return report


def write_results_md(report: dict, path: Path) -> None:
    g = report["gate"]
    lines = [
        "# Q-FUNNEL-1 — funnel EV sweep RESULTS",
        "",
        f"**Status:** `{g['verdict']}` — mechanical readout of pre-reg §6 "
        f"(not the study closure-of-record; that is operator/CC-side §9).",
        f"**Pre-registration (FROZEN):** [`Q-FUNNEL-1-verdict-preregistration.md`]"
        f"(../../../docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md)",
        f"**Eval fee pin (Q-RAIL-1 Phase 4):** ${report['eval_fee_usd']:.0f} list "
        f"/ ${report['eval_fee_promo_usd']:.0f} promo (list used).",
        f"**MAX_RETRIES:** {report['max_retries']} · **§3(a) floor:** "
        f"{report['materiality_relative']:.0%} relative",
        f"**n_lineages/cell:** {report['n_lineages']} · wall {report['wall_s']}s"
        f"{' · SMOKE' if report.get('smoke') else ''}",
        "",
        "## §0.5 resolutions applied",
        "",
        "- **A** — busted-post-funding keeps prior payouts (no clawback)",
        "- **B** — funded continuation from same week-block-bootstrap panel",
        "- **C** — winning-day counter resets after each payout (cycle-based)",
        "- **D** — per-leg de-mean before recombine",
        "",
        "## §6 gate application (mechanical)",
        "",
        f"**Verdict: `{g['verdict']}`**",
        "",
        f"- Resolved points (a+b+c): {len(g['resolved_points'])}",
        f"- Ambiguous points (a+b but not c): {len(g['ambiguous_points'])}",
        "",
    ]
    if g["resolved_points"]:
        lines += ["### RESOLVED triggers", ""]
        for p in g["resolved_points"]:
            lines.append(
                f"- edge=`{p['edge']}` policy=`{p['policy']}` "
                f"better_rung=`{p['better_rung']}` "
                f"H1_lift={p['H1']['relative_lift']:.1%} "
                f"H2_lift={p['H2']['relative_lift']:.1%}"
            )
        lines.append("")
    if g["ambiguous_points"]:
        lines += ["### AMBIGUOUS-HOLD triggers", ""]
        for p in g["ambiguous_points"]:
            lines.append(
                f"- edge=`{p.get('edge')}` policy=`{p.get('policy')}` "
                f"H1_better=`{p.get('H1_better', p.get('H1', {}).get('better_rung'))}` "
                f"H2_better=`{p.get('H2_better', p.get('H2', {}).get('better_rung'))}` "
                f"(direction reverses H1↔H2)"
            )
        lines.append("")

    lines += [
        "## Cell table (EV/day + bootstrap 5th–95th)",
        "",
        "| rung | policy | edge | half | EV/day | boot 5th | boot 95th | mean days |",
        "|---|---|---|---|---:|---:|---:|---:|",
    ]
    for r in report["cells"]:
        lines.append(
            f"| {r['rung']:.2f}× | {r['policy']} | {r['edge']} | {r['half']} | "
            f"{r['ev_day']:.4f} | {r['boot_5th']:.4f} | {r['boot_95th']:.4f} | "
            f"{r['mean_days']:.1f} |"
        )
    lines += [
        "",
        "## Sanity — edge ordering",
        "",
        "Per Step 2.4 gate: for each (rung, policy, half), "
        "`edge_0` EV/day should be ≤ `edge_panel_historical` "
        "(more edge must not produce less EV). Failures listed below "
        "(empty = pass).",
        "",
    ]
    fails = []
    by = {}
    for r in report["cells"]:
        by.setdefault((r["rung"], r["policy"], r["half"]), {})[r["edge"]] = r["ev_day"]
    for key, evs in sorted(by.items()):
        e0 = evs.get("edge_0")
        eh = evs.get("edge_panel_historical")
        if e0 is not None and eh is not None and e0 > eh + 1e-9:
            fails.append(f"- {key}: edge_0={e0:.4f} > historical={eh:.4f}")
    lines.extend(fails if fails else ["_(none)_", ""])
    lines += [
        "",
        "## Artifacts",
        "",
        "- Raw JSON: [`sweep_results.json`](sweep_results.json)",
        "- Harness: [`funnel.py`](funnel.py) · [`run_funnel_sweep.py`](run_funnel_sweep.py)",
        "- Regression pin: `test_funnel.py::test_regression_pin_matches_watch1_ratification`",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-lineages", type=int, default=500)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out-dir", type=Path, default=_HERE)
    args = ap.parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    report = run_sweep(
        n_lineages=args.n_lineages, seed=args.seed, smoke=args.smoke
    )
    # JSON-safe cells already plain dicts
    (args.out_dir / "sweep_results.json").write_text(
        json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8"
    )
    write_results_md(report, args.out_dir / "RESULTS.md")
    print(
        f"[funnel] DONE verdict={report['gate']['verdict']} "
        f"wall={report['wall_s']}s -> {args.out_dir / 'RESULTS.md'}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
