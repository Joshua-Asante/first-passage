"""Render grid JSON (screen / alt / final) into ranked tables + a dominance check.

Dominance: cell A dominates B on a tier when bust_A <= bust_B, pass_A >= pass_B,
median_days_A <= median_days_B, and at least one of bust/pass differs by more than
2 SE (pooled). Cells not dominated by any other cell form the Pareto set. A
"clear winner" is a Pareto set of size one whose margins over the runner-up
exceed 2 SE on bust AND pass.
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
EVAL_PRICE, RESET_PRICE = 265.0, 169.0


def label(sizing):
    return " + ".join(f"{k.upper()}x{v}" for k, v in sizing.items() if v > 0)


def load(name):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        return None
    with open(p) as fh:
        return json.load(fh)


def row(r, key="boot_intraday"):
    b = r[key]
    h1, h2 = r["halves"]["h1"], r["halves"]["h2"]
    med = b["median_days_to_pass"]
    fee = r["fee"]["expected_fee_to_first_pass"] if r.get("fee") else None
    rl = r["rolling"]["intraday"]
    return (
        f"| {label(r['sizing'])} | {r['micro_eq']} | {b['bust_pct']:.1f} ± {b['se_bust_pp']:.1f} | "
        f"{b['pass_pct']:.1f} | {b['unresolved_pct']:.1f} | {('%.0f' % med) if med else '—'} | "
        f"{h1['bust_pct']:.1f} / {h1['pass_pct']:.1f} | {h2['bust_pct']:.1f} / {h2['pass_pct']:.1f} | "
        f"{rl['pass_pct']:.0f} / {rl['bust_pct']:.0f} / {rl['unresolved_pct']:.0f} | "
        f"{r['weekly_coverage']*100:.0f}% | {('$%.0f' % fee) if fee else '—'} |"
    )


HEADER = ("| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | "
          "rolling pass/bust/unres | weekly cov | E[fee] |\n"
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")


def dominance(results):
    """Return (pareto_set, dominated_by) for one tier's results using boot_intraday."""
    def m(r):
        b = r["boot_intraday"]
        return b["bust_pct"], b["pass_pct"], (b["median_days_to_pass"] or 1e9), b["se_bust_pp"], b["se_pass_pp"]
    pareto, dominated_by = [], {}
    for i, a in enumerate(results):
        ba, pa, da, sba, spa = m(a)
        dom = None
        for j, b in enumerate(results):
            if i == j:
                continue
            bb, pb, db, sbb, spb = m(b)
            se_b = math.sqrt(sba ** 2 + sbb ** 2); se_p = math.sqrt(spa ** 2 + spb ** 2)
            weak = bb <= ba and pb >= pa and db <= da
            strict = (ba - bb) > 2 * se_b or (pb - pa) > 2 * se_p
            if weak and strict:
                dom = label(b["sizing"]); break
        if dom is None:
            pareto.append(a)
        else:
            dominated_by[label(a["sizing"])] = dom
    return pareto, dominated_by


def render(data, title):
    out = [f"## {title}", "",
           f"n_sims={data['n_sims']} × seeds {data['seeds']} = {data['n_sims']*len(data['seeds']):,} bootstrap paths per cell; "
           f"elapsed {data['elapsed_s']}s. Bootstrap = 5-day block resample through `run_seed`, intraday-honest channel "
           f"(timestamp-sequenced trade-level floor). Halves split at the window's business-day midpoint. "
           f"Rolling = deterministic replay from every start day (intraday clock). E[fee] = $265 + $169 × (1−p)/p on resolved paths.", ""]
    tiers = sorted({r["tier"] for r in data["results"]})
    for tier in tiers:
        rs = [r for r in data["results"] if r["tier"] == tier]
        rs.sort(key=lambda r: (-r["boot_intraday"]["pass_pct"], r["boot_intraday"]["bust_pct"]))
        w = rs[0]["window"]
        out += [f"### {tier} — window {w[0]} → {w[1]} ({rs[0]['n_days']} business days)", "", HEADER]
        out += [row(r) for r in rs]
        pareto, dom = dominance(rs)
        out += ["", f"**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** "
                    + "; ".join(label(p["sizing"]) for p in pareto)]
        if len(pareto) == 1:
            p = pareto[0]
            out.append(f"**Single Pareto cell: {label(p['sizing'])}.** Check the margin over the runner-up in the table above before calling it a clear winner.")
        out.append("")
        # standalone legs summary
        solo = [r for r in rs if len(r["active_legs"]) == 1]
        if solo:
            out += ["Standalone legs on this tier:", ""]
            for r in sorted(solo, key=lambda r: label(r["sizing"])):
                b = r["boot_intraday"]
                out.append(f"- {label(r['sizing'])}: bust {b['bust_pct']:.1f}%, pass {b['pass_pct']:.1f}%, median {b['median_days_to_pass']} days, weekly coverage {r['weekly_coverage']*100:.0f}%")
            out.append("")
    return "\n".join(out)


def render_controls(data):
    out = ["## Controls", ""]
    res = data["results"]
    co = data["comovement"]
    out += ["### (A) Shuffled-Aegis control — is Aegis's benefit co-movement or just positive drift?", "",
            "Every Aegis trade moved to another Aegis trade-date within the same calendar year (clock times kept): "
            "drift, count and per-year P&L preserved, day alignment with MNQ destroyed. Five permutations. "
            "If shuffled ≈ real, the benefit is drift, not diversification.", "",
            "| Tier | Book | Real bust / pass / median | Shuffled bust (5 perms) | Shuffled mean bust | Real H1 / H2 bust | Shuffled mean H1 / H2 |",
            "|---|---|---:|---|---:|---:|---:|"]
    for tier in sorted({r["tier"] for r in res}):
        for k in (2, 3):
            real = [r for r in res if r["tier"] == tier and r["tag"] == "real" and r["sizing"].get("aegis") == k]
            sh = [r for r in res if r["tier"] == tier and r["tag"].startswith("shuffled") and r["sizing"].get("aegis") == k]
            if not real or not sh:
                continue
            rb = real[0]["boot"]
            shb = [s["boot"]["bust_pct"] for s in sh]
            out.append(f"| {tier} | MNQx1 + AEGISx{k} | {rb['bust_pct']:.1f} / {rb['pass_pct']:.1f} / {rb['median_days_to_pass']:.0f} | "
                       f"{', '.join('%.1f' % x for x in shb)} | {sum(shb)/len(shb):.1f} | "
                       f"{real[0]['h1']['bust_pct']:.1f} / {real[0]['h2']['bust_pct']:.1f} | "
                       f"{sum(s['h1']['bust_pct'] for s in sh)/len(sh):.1f} / {sum(s['h2']['bust_pct'] for s in sh)/len(sh):.1f} |")
    out += ["", "### (B) Aegis alone on the regime the grid cannot see — 2020-02-24 → 2022-07-31 (sanctioned 1-tick panel)", "",
            "| Tier | Book | bust % | pass % | unresolved % | median days (passes) | H1 bust | H2 bust |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for r in res:
        if r["tag"].startswith("aegis 2020"):
            b = r["boot"]
            out.append(f"| {r['tier']} | AEGISx{r['sizing']['aegis']} | {b['bust_pct']:.1f} | {b['pass_pct']:.2f} | {b['unresolved_pct']:.1f} | "
                       f"{b['median_days_to_pass'] if b['median_days_to_pass'] else '—'} | {r['h1']['bust_pct']:.1f} | {r['h2']['bust_pct']:.1f} |")
    out += ["", "### (C) Daily P&L co-movement on the common window (per contract)", "",
            "| Pair | corr (active days) | P(both lose) | P(independent) | ratio |", "|---|---:|---:|---:|---:|"]
    for pair, v in co["joint_loss_days"].items():
        a, b = pair.split("-")
        out.append(f"| {a.upper()}–{b.upper()} | {co['corr_active_days'][a][b]:.3f} | {v['p_both_lose']:.3f} | {v['p_independent']:.3f} | {v['ratio']} |")
    out += ["", "| Leg | trade days | mean $/trade-day per contract | worst day per contract | skew (active days) |", "|---|---:|---:|---:|---:|"]
    for leg, v in co["per_leg"].items():
        out.append(f"| {leg.upper()} | {v['trade_days']} | ${v['mean_pc_per_trade_day']:.0f} | ${v['worst_day_pc']:.0f} | {v['skew_active']:.2f} |")
    out.append("")
    return "\n".join(out)


VERDICT = """## Verdict (2026-09-01)

**No configuration is a clear winner on all three axes (bust, pass, time).** The grid has a genuine bust-versus-speed
frontier, and the two controls change how the Aegis cells should be read. What the 88-cell screen, the six full-N finalists
(30,000 paths each) and the controls do settle:

1. **Any leg at 2 contracts is out.** Every book containing MNQ×2 or MYM×2 busts 40% to 66% on both tiers. Sizing, not
   composition, is the first-order variable; the second is the tier.
2. **Growth beats Select by more than any composition change.** Same books, same clock: MNQ×1 18.9% → 10.8% bust,
   MNQ×1+Aegis×2 14.8% → 7.8%, with identical medians. The $500 wider rope is the biggest lever in the grid.
3. **MYM v0.4 hurts every book it joins.** It buys 40 to 50 days of median time at +9 to +11 points of bust
   (MNQ×1 → MNQ×1+MYM×1: 10.8% → 22.3% on Growth). Its losses coincide with MNQ's 25% more often than independence
   (joint-loss ratio 1.25), its per-trade-day expectancy is a quarter of MNQ's ($12 vs $50 per contract), and its
   active-day skew is 4.5 (rare big wins, many small losses). Drop it as a leg. The measured v0.3 long-only export is
   no better (Growth pair 31.9% bust vs the 19.5% rolling-start figure in MYM.md M9, which this bootstrap does not
   reproduce).
4. **Aegis as ballast improves MNQ×1 on all three axes, but for the wrong reason.** MNQ×1+Aegis×2 vs MNQ×1 on Growth:
   bust 7.8% vs 10.8%, pass 92.2% vs 89.2%, median 161 vs 190 days, all well beyond 2 SE. The shuffled-Aegis control
   (dates permuted within year, drift kept, co-movement destroyed) busts the same or less than the real book on both
   tiers at both sizes. So the gain is Aegis's positive drift over 2022-2026, not diversification. On its excluded
   2020-02 → 2022-07 regime Aegis×2 passes 0.03% of paths in 2.4 years (95% unresolved) and busts 5% (Growth) / 11%
   (Select); ×3 busts 27% / 41%. Aegis×2 beside MNQ×1 is therefore a bet that the 2022+ yen regime persists, with a
   short-side rail change and a 6J Python port as its price. It fits the 30-micro funded start (21 micro-equivalents);
   Aegis×3 (31) does not until the first ladder step.
5. **Aegis alone is the only thing under the frozen 5% ceiling, and only on the favourable window.** Aegis×3 on Growth:
   2.3% bust, 95.4% pass, median 602 days, 47% of weeks with no trade (token trade every other week). On the excluded
   regime the same size busts 27%.

**Defensible picks, in order, under the fee-priced criterion (pass ≥ 60%, median ≤ 200 days, worse half ≥ 50%):**

| Pick | Tier | bust | pass | median days | worse half | Why / cost |
|---|---|---:|---:|---:|---:|---|
| MNQ×1 + Aegis×2 | Growth | 7.8% | 92.2% | 161 | 84% pass | Best bust/pass among fast books; gain is drift, regime-conditional; needs short-side rail + 6J port |
| MNQ×1 | Growth | 10.8% | 89.2% | 190 | 77% pass | Simplest; one port, one leg, no Aegis regime bet; 99% weekly coverage |
| MNQ×1 + Aegis×2 | Select | 14.8% | 85.2% | 154 | 74% pass | Same book on the live account; no Growth purchase |
| MNQ×1 + MYM×1 + Aegis×2 | Growth | 19.2% | 80.8% | 108 | 76% pass | Fastest; pays 11 points of bust for 53 days |

**Bounds, stated plainly.** The bootstrap breaks the realized sequence and is the pessimistic read (every finalist's realized
path passes, day 79 to 156, max drawdown 1.9% to 2.2%, and rolling starts never bust). The intraday channel is a trade-level
sweep-line from TradingView's own adverse-excursion figures, not a bar replay. The window starts 2022-08-01 because MYM v0.4
does; MNQ's own 2020-2021 (the recon_v2 six-year export busts its realized path in 2020 at one contract on Select) and
Aegis's 2020-2022 are outside it. The MNQ recon lineage and MYM v0.4 are tuned charts with no untouched holdout. Export
slippage and commission are whatever the operator set in TradingView; Aegis uses the sanctioned 1-tick `76620` panel
(the 08-28 `cbcc9` export fills one tick better on every shared trade and was not used). Growth's soft $2,500 daily
lockout is not modeled (pessimistic on the rope); Select's 40% consistency rule is.
"""


def main():
    parts = ["# Three-leg Tradeify book grid — ORB-MNQ recon × ORB-MYM × Aegis-6J1", "",
             "**Status:** EXPLORATORY — informal Downloads-lane measurement, not pre-registered, no K entry; "
             "the harness reuses `core/mc/simulation.py` and `core/mc/preflight.py` verbatim. "
             "Inputs are operator TradingView exports (uncommitted). See `book_grid.py` docstring for the exact files and unit conventions.", "",
             VERDICT]
    for name, title in (("grid_final.json", "Finalists at full N"),
                        ("grid_screen.json", "Screen grid — MNQ {0,1,2} × MYM v0.4 {0,1,2} × Aegis {0..4}"),
                        ("grid_alt_mym_v03.json", "Reference cells with the measured MYM v0.3 export (long-only, MYM.md M9)")):
        d = load(name)
        if d:
            parts.append(render(d, title))
    c = load("controls.json")
    if c:
        parts.append(render_controls(c))
    md = "\n".join(parts)
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    sys.stdout.reconfigure(encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
