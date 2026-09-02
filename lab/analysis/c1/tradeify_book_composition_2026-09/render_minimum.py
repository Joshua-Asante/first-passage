"""Pivot the exact-edge minimum-attribute grid (third_leg_minimum.json) into edge x win-rate
tables of delta-bust and delta-median at $100 and $200 stops, plus the correlation and cadence checks."""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def main():
    d = json.load(open(os.path.join(DATA, "third_leg_minimum.json")))
    tier = "Tradeify_Growth_100K"
    base = d["base"][tier]["boot"]
    cells = defaultdict(list)
    for r in d["results"]:
        p = r["params"]
        cells[(p["edge_r"], p["wr"], p["risk"], p["cadence"], p["rho"])].append(r)

    def agg(k):
        rs = cells[k]
        return {"bust": np.mean([r["boot"]["bust_pct"] for r in rs]), "pass": np.mean([r["boot"]["pass_pct"] for r in rs]),
                "med": np.mean([r["boot"]["median_days_to_pass"] or np.nan for r in rs]),
                "sd_bust": np.std([r["boot"]["bust_pct"] for r in rs]),
                "corr": np.mean([r["realized_corr_mnq"] for r in rs if r["realized_corr_mnq"] is not None] or [np.nan]),
                "edge": np.mean([r["realized_edge_r"] for r in rs]), "drift": np.mean([r["annual_drift_usd"] for r in rs]),
                "n": len(rs)}

    md = ["# Minimum attributes of a third leg beside MNQ×1 + Aegis×2 (exact-edge generator)", "",
          f"Growth 100K, window 2022-08-01 → 2026-07-01. {d['n_sims']}×{len(d['seeds'])} bootstrap paths per run, "
          f"{len(d['realisations'])} realisations per cell (only the win/loss ORDER varies; win fraction and edge are exact). "
          f"Base book at this N: bust {base['bust_pct']:.1f}%, pass {base['pass_pct']:.1f}%, median {base['median_days_to_pass']:.0f} days.", ""]
    edges = sorted({k[0] for k in cells if k[3] == 5 and k[4] == 0.0})
    wrs = sorted({k[1] for k in cells if k[3] == 5 and k[4] == 0.0})
    for risk in (100, 200):
        for metric, label in (("bust", "Δ bust (pp) vs base"), ("med", "Δ median days vs base")):
            md += [f"## {label}, stop ${risk}, 5 trades/week, uncorrelated", "",
                   "| edge R \\ win rate | " + " | ".join(f"{w:.0%}" for w in wrs) + " |", "|---|" + "---:|" * len(wrs)]
            for e in edges:
                row = []
                for w in wrs:
                    k = (e, w, risk, 5, 0.0)
                    if k in cells:
                        a = agg(k)
                        v = a[metric] - (base["bust_pct"] if metric == "bust" else base["median_days_to_pass"])
                        row.append(f"{v:+.1f}" if metric == "bust" else f"{v:+.0f}")
                    else:
                        row.append("·")
                md.append(f"| {e:.2f} | " + " | ".join(row) + " |")
            md.append("")
    # fit map: cells with Δbust <= +0.5 and Δmed <= -30
    md += ["## Cells that FIT (Δ bust ≤ +0.5 pp and at least 30 days saved), 5/week uncorrelated", "",
           "| edge R | win rate | mean win R | stop $ | bust % (Δ) | median days (Δ) | drift $/yr | sd bust across realisations |", "|---:|---:|---:|---:|---:|---:|---:|---:|"]
    fits = []
    for k in sorted(cells):
        if k[3] != 5 or k[4] != 0.0:
            continue
        a = agg(k)
        db, dm = a["bust"] - base["bust_pct"], a["med"] - base["median_days_to_pass"]
        if db <= 0.5 and dm <= -30:
            W = (k[0] + 1 - k[1]) / k[1]
            fits.append((k, a, db, dm, W))
    for k, a, db, dm, W in sorted(fits, key=lambda x: x[3]):
        md.append(f"| {k[0]:.2f} | {k[1]:.0%} | {W:.2f} | {k[2]} | {a['bust']:.1f} ({db:+.1f}) | {a['med']:.0f} ({dm:+.0f}) | {a['drift']:,.0f} | {a['sd_bust']:.1f} |")
    md.append("")
    # correlation check
    md += ["## Correlation check at the frontier (5/week)", "", "| edge R | win rate | stop $ | realized corr | bust % (Δ) | median (Δ) |", "|---:|---:|---:|---:|---:|---:|"]
    for k in sorted(cells):
        if k[3] == 5 and k[0] in (0.10, 0.15) and k[1] in (0.45, 0.55, 0.75) and k[2] in (100, 200):
            a = agg(k)
            md.append(f"| {k[0]:.2f} | {k[1]:.0%} | {k[2]} | {a['corr']:+.2f} | {a['bust']:.1f} ({a['bust']-base['bust_pct']:+.1f}) | {a['med']:.0f} ({a['med']-base['median_days_to_pass']:+.0f}) |")
    md.append("")
    md += ["## Cadence check: 2/week vs 5/week, uncorrelated", "", "| edge R | win rate | stop $ | trades/wk | bust % (Δ) | median (Δ) | drift $/yr |", "|---:|---:|---:|---:|---:|---:|---:|"]
    for k in sorted(cells):
        if k[4] == 0.0 and k[0] in (0.10, 0.15) and k[1] in (0.55, 0.75) and k[2] in (100, 200):
            a = agg(k)
            md.append(f"| {k[0]:.2f} | {k[1]:.0%} | {k[2]} | {k[3]} | {a['bust']:.1f} ({a['bust']-base['bust_pct']:+.1f}) | {a['med']:.0f} ({a['med']-base['median_days_to_pass']:+.0f}) | {a['drift']:,.0f} |")
    text = "\n".join(md)
    open(os.path.join(HERE, "THIRD_LEG_MINIMUM.md"), "w", encoding="utf-8").write(text)
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
