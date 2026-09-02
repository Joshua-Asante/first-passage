"""Summarise third_leg_sweep.json: average realisations, delta vs the re-scored base book,
marginal effect of each shape axis, the fit frontier, and the offenders."""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def key(p):
    return (p["edge_r"], p["wr"], p["risk"], p["cadence"], p["rho"])


def main(name="third_leg_sweep.json", out="THIRD_LEG.md"):
    d = json.load(open(os.path.join(DATA, name)))
    tiers = sorted({r["tier"] for r in d["results"]})
    md = ["# Third-leg shape sweep — what fits MNQ×1 + Aegis×2", "",
          "> ⚠ **Superseded for quantitative use by `THIRD_LEG_MINIMUM.md`.** This first sweep drew per-trade Bernoulli outcomes "
          "with two seeds shared across every cell; the realized edge wandered up to ±0.15R from target per seed and moved whole "
          "win-rate rows together (the 55% rows ran about +0.05R lucky), and the copula sign was inverted (rho labels flipped; realized "
          "correlation columns are correct). Directions hold; magnitudes do not. The exact-edge re-run is the reference.", "",
          f"Synthetic third leg added to the real base book on the real date index (window 2022-08-01 → 2026-07-01); "
          f"{d['n_sims']} sims × {len(d['seeds'])} seeds per run, {len(d['realisations'])} panel realisations per cell averaged; "
          "intraday-honest block bootstrap through `run_seed`. Δ = cell − base at the same N. See `third_leg_shape.py` for the generator.", ""]
    for tier in tiers:
        base = d["base"][tier]["boot"]
        md += [f"## {tier}", "",
               f"Base book MNQ×1 + Aegis×2 at this N: bust {base['bust_pct']:.1f}%, pass {base['pass_pct']:.1f}%, median {base['median_days_to_pass']:.0f} days, p75 {base['p75_days_to_pass']:.0f}.", ""]
        cells = defaultdict(list)
        for r in d["results"]:
            if r["tier"] == tier:
                cells[key(r["params"])].append(r)
        rows = []
        for k, rs in cells.items():
            b = np.mean([r["boot"]["bust_pct"] for r in rs]); p = np.mean([r["boot"]["pass_pct"] for r in rs])
            med = np.mean([r["boot"]["median_days_to_pass"] or np.nan for r in rs])
            p75 = np.mean([r["boot"]["p75_days_to_pass"] or np.nan for r in rs])
            corr = np.mean([r["realized_corr_mnq"] for r in rs if r["realized_corr_mnq"] is not None] or [np.nan])
            drift = np.mean([r["annual_drift_usd"] for r in rs])
            W = rs[0]["params"]["W"]
            rows.append({"k": k, "W": W, "bust": b, "pass": p, "med": med, "p75": p75, "corr": corr, "drift": drift,
                         "d_bust": b - base["bust_pct"], "d_pass": p - base["pass_pct"], "d_med": med - base["median_days_to_pass"]})
        # marginal effects
        md += ["### Marginal effect of each axis (mean Δ over all other cells)", "",
               "| Axis | Level | Δ bust (pp) | Δ pass (pp) | Δ median days | mean annual drift $ |", "|---|---:|---:|---:|---:|---:|"]
        names = ("edge_r", "wr", "risk", "cadence", "rho")
        for i, nm in enumerate(names):
            for lvl in sorted({r["k"][i] for r in rows}):
                sub = [r for r in rows if r["k"][i] == lvl]
                lvl_label = f"{lvl}" if nm != "rho" else f"realized corr {np.nanmean([r['corr'] for r in sub]):+.2f}"
                md.append(f"| {nm if nm != 'rho' else 'corr with MNQ'} | {lvl_label} | {np.mean([r['d_bust'] for r in sub]):+.1f} | {np.mean([r['d_pass'] for r in sub]):+.1f} | "
                          f"{np.nanmean([r['d_med'] for r in sub]):+.0f} | {np.mean([r['drift'] for r in sub]):,.0f} |")
        md.append("")
        md += ["⚠ The generator's copula sign was inverted in this sweep, so the `rho` *labels* are flipped relative to the "
               "realized correlation; every table here reports the realized correlation, which is the number that matters.", ""]
        # realistic band: MNQ-class edge or less, moderate risk
        band = sorted([r for r in rows if r["k"][0] <= 0.15 and r["k"][2] <= 200], key=lambda r: r["d_med"])
        md += ["### Realistic band — edge ≤ 0.15 R per trade (MNQ-class or weaker) and risk ≤ $200 per stop", "",
               "| edge R | win rate | mean win R | $ risk | trades/wk | realized corr | annual drift $ | bust % (Δ) | pass % (Δ) | median days (Δ) |",
               "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in band:
            e, wr, risk, cad, rho = r["k"]
            md.append(f"| {e:.2f} | {wr:.2f} | {r['W']:.2f} | {risk} | {cad} | {r['corr']:+.2f} | {r['drift']:,.0f} | "
                      f"{r['bust']:.1f} ({r['d_bust']:+.1f}) | {r['pass']:.1f} ({r['d_pass']:+.1f}) | {r['med']:.0f} ({r['d_med']:+.0f}) |")
        md.append("")
        # fit frontier: does not raise bust by more than 0.5pp, ranked by time saved
        fit = sorted([r for r in rows if r["d_bust"] <= 0.5], key=lambda r: r["d_med"])
        md += ["### Shapes that fit (Δ bust ≤ +0.5 pp), ranked by time saved", "",
               "| edge R | win rate | mean win R | $ risk | trades/wk | realized corr with MNQ | annual drift $ | bust % (Δ) | pass % (Δ) | median days (Δ) |",
               "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in fit[:25]:
            e, wr, risk, cad, rho = r["k"]
            md.append(f"| {e:.2f} | {wr:.2f} | {r['W']:.2f} | {risk} | {cad} | {r['corr']:+.2f} | {r['drift']:,.0f} | "
                      f"{r['bust']:.1f} ({r['d_bust']:+.1f}) | {r['pass']:.1f} ({r['d_pass']:+.1f}) | {r['med']:.0f} ({r['d_med']:+.0f}) |")
        md += ["", f"{len(fit)} of {len(rows)} shapes fit the ≤ +0.5 pp bust bar.", ""]
        # best time-savers that also LOWER bust
        both = sorted([r for r in rows if r["d_bust"] < 0 and r["d_med"] < 0], key=lambda r: (r["d_med"], r["d_bust"]))
        md += ["### Shapes that lower bust AND shorten time", "", "| edge R | win rate | mean win R | $ risk | trades/wk | realized corr | drift $ | Δ bust | Δ median |", "|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in both[:15]:
            e, wr, risk, cad, rho = r["k"]
            md.append(f"| {e:.2f} | {wr:.2f} | {r['W']:.2f} | {risk} | {cad} | {r['corr']:+.2f} | {r['drift']:,.0f} | {r['d_bust']:+.1f} | {r['d_med']:+.0f} |")
        md += ["", f"{len(both)} of {len(rows)} shapes do both.", ""]
        # offenders
        bad = sorted(rows, key=lambda r: -r["d_bust"])[:10]
        md += ["### Worst offenders (largest bust increase)", "", "| edge R | win rate | mean win R | $ risk | trades/wk | realized corr | Δ bust | Δ median |", "|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in bad:
            e, wr, risk, cad, rho = r["k"]
            md.append(f"| {e:.2f} | {wr:.2f} | {r['W']:.2f} | {risk} | {cad} | {r['corr']:+.2f} | {r['d_bust']:+.1f} | {r['d_med']:+.0f} |")
        md.append("")
        # zero-edge check: pure variance effect
        z = [r for r in rows if r["k"][0] == 0.0]
        md += ["### Zero-edge legs (pure variance, no drift): what shape alone does", "",
               f"mean Δ bust {np.mean([r['d_bust'] for r in z]):+.1f} pp (range {min(r['d_bust'] for r in z):+.1f} to {max(r['d_bust'] for r in z):+.1f}); "
               f"mean Δ median {np.nanmean([r['d_med'] for r in z]):+.0f} days. "
               f"zero-edge legs moving WITH MNQ (realized corr ≈ +0.25): Δ bust {np.mean([r['d_bust'] for r in z if r['k'][4] < 0]):+.1f}; moving AGAINST MNQ (≈ −0.2): {np.mean([r['d_bust'] for r in z if r['k'][4] > 0]):+.1f}; uncorrelated: {np.mean([r['d_bust'] for r in z if r['k'][4] == 0]):+.1f}.", ""]
    text = "\n".join(md)
    open(os.path.join(HERE, out), "w", encoding="utf-8").write(text)
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(*sys.argv[1:])
