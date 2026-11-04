"""Markdown tables for RESULTS.md from results_series.json and results_bar.json (DESIGN.md criteria)."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

D = Path(__file__).parent
SH = (0.0, 0.5, 0.85, 0.89, 1.0, 1.5)


def f(x):
    return "—" if x is None else f"{x:.3f}"


def series() -> None:
    cs = json.loads((D / "results_series.json").read_text())["cells"]
    main = [c for c in cs if c["rho"] == 0.0]
    print("## Series layer: whole-stack pass (5a, 5c, 5f, holdout), by true annual Sharpe\n")
    for n in (1510, 2350):
        print(f"### n = {n} development sessions\n")
        print("| q | shape | K | " + " | ".join(f"S={s}" for s in SH) + " | 5f closed form at 0.85 / 0.89 |")
        print("|---|---|---|" + "---|" * len(SH) + "---|")
        for q in (0.15, 0.40, 0.85):
            for shape in ("normal", "orb_skew"):
                for k in ("1", "2", "4"):
                    row = {c["S"]: c for c in main if c["n"] == n and c["q"] == q and c["shape"] == shape}
                    cf = f"{row[0.85]['by_k'][k]['5f_closed_form']:.3f} / {row[0.89]['by_k'][k]['5f_closed_form']:.3f}"
                    print(f"| {q} | {shape} | {k} | " + " | ".join(f(row[s]["by_k"][k]["stack_pass"]) for s in SH)
                          + f" | {cf} |")
        print()
    # V1
    worst, bad = 0.0, []
    for c in main:
        if c["shape"] == "normal" and c["q"] == 0.85:
            for k, b in c["by_k"].items():
                p = b["5f_closed_form"]
                tol = 3 * math.sqrt(max(p * (1 - p), 1e-4) / c["paths"]) + 0.02
                gap = abs(b["5f_standalone"] - p)
                worst = max(worst, gap)
                if gap > tol:
                    bad.append((c["S"], c["n"], k, b["5f_standalone"], p))
    print(f"**V1:** worst |measured 5f − closed form| = {worst:.3f}; cells outside tolerance: {bad or 'none'}\n")
    print("### Kill shares (first fail, engine order) and 5f measured vs closed form, K = 1 / 2 / 4\n")
    print("| n | q | shape | S | 5a | 5c | 5f (K=1/2/4) | holdout (K=1/2/4) | 5f measured (1/2/4) | 5f closed (1/2/4) |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for c in main:
        if c["S"] in (0.0, 0.85, 0.89, 1.5):
            b = c["by_k"]
            j = lambda key, sub=None: " / ".join(f"{(b[k]['kill_share'][sub] if sub else b[k][key]):.3f}" for k in ("1", "2", "4"))  # noqa: E731
            print(f"| {c['n']} | {c['q']} | {c['shape']} | {c['S']} | {b['1']['kill_share']['5a']:.3f} | "
                  f"{b['1']['kill_share']['5c']:.3f} | {j(None, '5f')} | {j(None, 'holdout')} | "
                  f"{j('5f_standalone')} | {j('5f_closed_form')} |")
    print("\n### Standalone pass rates (K-free gates) and 5g placement\n")
    print("| n | q | shape | ρ | S | trades | 5a | 5c | holdout | 5g clear (all paths) | 5g clear given stack pass (K=1/2/4) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for c in cs:
        if c["S"] in (0.0, 0.85, 1.5) and (c["rho"] > 0 or (c["q"] == 0.40 and c["shape"] == "orb_skew") or c["q"] == 0.15):
            s = c["standalone"]
            g = " / ".join(f(c["by_k"][k]["5g_clear_given_pass"]) for k in ("1", "2", "4"))
            print(f"| {c['n']} | {c['q']} | {c['shape']} | {c['rho']} | {c['S']} | {c['mean_trades']:.0f} | {s['5a']:.3f} | "
                  f"{s['5c']:.3f} | {s['holdout']:.3f} | {s['5g_clear_any']:.3f} | {g} |")
    print()


def bar() -> None:
    p = D / "results_bar.json"
    if not p.exists():
        print("## Bar layer: not run\n")
        return
    r = json.loads(p.read_text())
    print("## Bar layer\n")
    print("Calibration (fresh-seed re-estimate at the chosen drift):\n")
    print("| target S | drift (points/bar) | achieved S | SE | V2 |")
    print("|---|---|---|---|---|")
    for S, v in r["calibration"]["chosen"].items():
        print(f"| {S} | {v['drift']:.3f} | {v['annual_sharpe']:.3f} | {v['se']:.3f} | {'pass' if v['v2_pass'] else 'MISS'} |")
    print("\n| target S | n | trades | unresolved | 5a | 5c | 5d | 5e | 5f K=1 | holdout | stack K=1 / 2 / 4 | kill 5a/5c/5d/5e/5f/holdout (K=1) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for c in r["cells"]:
        s, b = c["standalone_reached"], c["by_k"]
        ks = b["1"]["kill_share"]
        print(f"| {c['target_S']} | {c['n']} | {c['mean_trades']:.0f} | {c['unresolved']} | {s['5a']:.3f} | {s['5c']:.3f} | "
              f"{s['5d']:.3f} | {s['5e']:.3f} | {b['1']['5f_standalone']:.3f} | {s['holdout']:.3f} | "
              + " / ".join(f"{b[k]['stack_pass']:.3f}" for k in ("1", "2", "4")) + " | "
              + " / ".join(f"{ks[g]:.3f}" for g in ("5a", "5c", "5d", "5e", "5f", "holdout")) + " |")
    print()


if __name__ == "__main__":
    {"series": series, "bar": bar}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: (series(), bar()))()
