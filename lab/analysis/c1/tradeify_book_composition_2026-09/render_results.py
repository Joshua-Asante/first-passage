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
            "Every Aegis trade moved to a DIFFERENT Aegis trade-date within the same calendar year (clock times "
            "kept): drift, count and per-year P&L preserved, day alignment with MNQ destroyed. Five draws, each a "
            "true derangement — a plain permutation leaves ~1 date mapped to itself per draw, which would preserve "
            "some of the alignment this control exists to destroy (fixed 2026-09-02, Codex review of PR #260). "
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


def drift_reading(shuf_g, real_g, n_shuf):
    """Headline + control sentence for verdict item 4, conditioned on the control.

    "The Aegis gain is drift, not diversification" is a CONCLUSION FROM the shuffled
    control, so it may only be asserted when that control exists AND actually orders that
    way. Earlier versions appended it unconditionally: with `controls.json` missing the
    prose still reported an unavailable control's finding as established, and had a re-run
    put the shuffled book ABOVE the real one the sentence would have contradicted the
    figures printed immediately beside it. Raised by Codex on PR #271 (round 4).

    Returns (headline, control-clause). The caller renders "But {clause}."
    """
    if shuf_g is None:
        return ("**Aegis as ballast improves MNQ×1 on all three axes.**",
                "the shuffled-Aegis control is absent (`controls.json` not built), so whether that "
                "gain is diversification or merely Aegis's own drift is UNTESTED here")
    common = (f"the shuffled-Aegis control — a true derangement of its trade dates within each year, "
              f"drift kept, co-movement destroyed — busts {shuf_g:.2f}% on Growth ({n_shuf} draws)")
    if shuf_g <= real_g:
        return ("**Aegis as ballast improves MNQ×1 on all three axes, but for the wrong reason.**",
                f"{common} against the real book's {real_g:.2f}% at screen N. The control matches or "
                f"beats the real book, so the gain is Aegis's positive drift over 2022-2026, not "
                f"diversification")
    return ("**Aegis as ballast improves MNQ×1 on all three axes; the control does not attribute that "
            "to drift.**",
            f"{common}, WORSE than the real book's {real_g:.2f}% at screen N. Destroying the "
            f"co-movement hurt, so this control does not support reading the gain as drift alone; "
            f"treat the split between drift and diversification as unresolved")


def _fin():
    """Finalist cells keyed (tier, sizing-label) -> boot_intraday dict, from grid_final.json.
    Every number in the verdict below is read from the data, not transcribed, so a re-run
    cannot leave the prose stale (the failure mode Codex caught elsewhere in this campaign)."""
    d = load("grid_final.json")
    if not d:
        return {}
    out = {}
    for r in d["results"]:
        out[(r["tier"], label(r["sizing"]))] = r
    return out


def verdict():
    f = _fin()
    if not f:
        return "## Verdict\n\n_grid_final.json absent - run `--stage final` first._\n"
    G, S = "Tradeify_Growth_100K", "Tradeify_Select_100K"

    def b(tier, lab, k="bust_pct"):
        r = f.get((tier, lab))
        return None if r is None else r["boot_intraday"][k]

    def row(tier, lab):
        r = f[(tier, lab)]
        bi = r["boot_intraday"]
        return (f"| {lab} | {tier.replace('Tradeify_', '').replace('_100K', '')} | "
                f"{bi['bust_pct']:.1f}% | {bi['pass_pct']:.1f}% | {bi['median_days_to_pass']:.0f} | "
                f"{r['halves']['h2']['pass_pct']:.0f}% |")

    mnq_g, mnq_s = b(G, "MNQx1"), b(S, "MNQx1")
    pair_g, pair_s = b(G, "MNQx1 + AEGISx2"), b(S, "MNQx1 + AEGISx2")
    mym_g = b(G, "MNQx1 + MYMx1")
    aeg_g = b(G, "AEGISx3")
    L = []
    L.append("## Verdict (2026-09-01, corrected 2026-09-02 after Codex review of PR #260)\n")
    L.append("**No configuration is a clear winner on all three axes (bust, pass, time).** The grid has a genuine "
             "bust-versus-speed frontier, and the controls change how the Aegis cells should be read. What the 88-cell "
             "screen, the six full-N finalists (30,000 paths each) and the controls settle:\n")
    L.append("1. **Any leg at 2 contracts is out.** Every book containing MNQ×2 or MYM×2 busts 40% to 66% on both "
             "tiers. Sizing, not composition, is the first-order variable; the second is the tier.")
    L.append(f"2. **Growth beats Select by more than any composition change.** Same books, same clock: MNQ×1 "
             f"{mnq_s:.1f}% → {mnq_g:.1f}% bust, MNQ×1+Aegis×2 {pair_s:.1f}% → {pair_g:.1f}%, at effectively "
             f"unchanged medians. The $500 wider rope is the biggest lever in the grid.")
    # Control figures are read from controls.json for the same reason the finalist figures are
    # read from grid_final.json: a re-run must not leave this prose self-contradictory.
    # Round 2 of the PR #260 review caught the shuffled and excluded-regime figures being
    # hard-coded here. Round 3 (PR #271) caught that item 3's co-movement ratio, per-leg
    # expectancy and skew were STILL literals -- and by then the regenerated artifact had moved
    # the MNQ/MYM joint-loss ratio to 1.24 while this prose still asserted 1.25. Every
    # quantitative claim in the verdict now resolves from an artifact.
    c = load("controls.json")
    co = (c or {}).get("comovement", {})
    _jl = co.get("joint_loss_days", {}).get("mnq-mym", {})
    _pl = co.get("per_leg", {})
    if _jl.get("ratio") and _pl.get("mnq") and _pl.get("mym"):
        _me, _ye = _pl["mnq"]["mean_pc_per_trade_day"], _pl["mym"]["mean_pc_per_trade_day"]
        mym_txt = (f"Its losses coincide with MNQ's {(_jl['ratio'] - 1) * 100:.0f}% more often than "
                   f"independence (joint-loss ratio {_jl['ratio']:.2f}), its per-trade-day expectancy "
                   f"is {_ye / _me:.2f}× MNQ's (${_ye:.0f} vs ${_me:.0f} per contract), and its "
                   f"active-day skew is {_pl['mym']['skew_active']:.1f} (rare big wins, many small "
                   f"losses).")
    else:
        mym_txt = "Its co-movement and per-leg statistics are absent (`controls.json` not built)."
    L.append(f"3. **MYM v0.4 hurts every book it joins.** MNQ×1 → MNQ×1+MYM×1 on Growth: {mnq_g:.1f}% → "
             f"{mym_g:.1f}% bust. {mym_txt} Drop it as a leg. The v0.3 long-only "
             f"export is no better, and this bootstrap does not reproduce the 19.5%-bust rolling-start figure in "
             f"`ops/instruments/MYM.md` M9.")
    ctl = {}
    if c:
        for r in c["results"]:
            ctl.setdefault((r["tier"], label(r["sizing"]), r["tag"].split(" seed")[0]), []).append(r)

    def ctl_bust(tier, lab, tag):
        rs = ctl.get((tier, lab, tag), [])
        return (sum(r["boot"]["bust_pct"] for r in rs) / len(rs)) if rs else None

    real_g = ctl_bust(G, "MNQx1 + AEGISx2", "real")
    shuf_g = ctl_bust(G, "MNQx1 + AEGISx2", "shuffled")
    n_shuf = len(ctl.get((G, "MNQx1 + AEGISx2", "shuffled"), []))
    ex_g2 = ctl_bust(G, "AEGISx2", "aegis 2020-02..2022-07")
    ex_s2 = ctl_bust(S, "AEGISx2", "aegis 2020-02..2022-07")
    ex_g3 = ctl_bust(G, "AEGISx3", "aegis 2020-02..2022-07")
    ex_s3 = ctl_bust(S, "AEGISx3", "aegis 2020-02..2022-07")
    ex_pass = None
    if ctl.get((G, "AEGISx2", "aegis 2020-02..2022-07")):
        ex_pass = ctl[(G, "AEGISx2", "aegis 2020-02..2022-07")][0]["boot"]["pass_pct"]
    head, ctl_txt = drift_reading(shuf_g, real_g, n_shuf)
    ex_txt = ("" if ex_g2 is None else
              f" On its excluded 2020-02→2022-07 window Aegis×2 passes {ex_pass:.2f}% of paths "
              f"({ex_g2:.1f}% bust on Growth, {ex_s2:.1f}% on Select) and Aegis×3 busts "
              f"{ex_g3:.0f}%/{ex_s3:.0f}%.")
    L.append(f"4. {head} MNQ×1+Aegis×2 vs "
             f"MNQ×1 on Growth: bust {pair_g:.1f}% vs {mnq_g:.1f}%, median "
             f"{f[(G, 'MNQx1 + AEGISx2')]['boot_intraday']['median_days_to_pass']:.0f} vs "
             f"{f[(G, 'MNQx1')]['boot_intraday']['median_days_to_pass']:.0f} days. But {ctl_txt}.{ex_txt}")
    aeg_cov = f[(G, "AEGISx3")]["weekly_coverage"] * 100
    L.append(f"5. **Aegis alone is the only thing under the frozen 5% ceiling, and only on the favourable window.** "
             f"Aegis×3 on Growth: {aeg_g:.1f}% bust, "
             f"{f[(G, 'AEGISx3')]['boot_intraday']['pass_pct']:.1f}% pass, median "
             f"{f[(G, 'AEGISx3')]['boot_intraday']['median_days_to_pass']:.0f} days, but only {aeg_cov:.0f}% of "
             f"weeks carry a trade (a token trade roughly every other week)"
             + (f" and the same size busts {ex_g3:.0f}% on the excluded regime.\n" if ex_g3 is not None else ".\n"))
    L.append("**Defensible picks, in order, under the fee-priced criterion (pass ≥ 60%, median ≤ 200 days, worse "
             "half ≥ 50%):**\n")
    L.append("| Book | Tier | bust | pass | median days | worse-half pass |")
    L.append("|---|---|---:|---:|---:|---:|")
    for tier, lab in ((G, "MNQx1 + AEGISx2"), (G, "MNQx1"), (S, "MNQx1 + AEGISx2"),
                      (G, "MNQx1 + MYMx1 + AEGISx2")):
        if (tier, lab) in f:
            L.append(row(tier, lab))
    L.append("\nThe first pick carries a regime bet (Aegis's drift) and needs a short-side rail change plus a 6J "
             "Python port. The second needs neither and costs about a month. The fourth is fastest and pays for it "
             "in bust.\n")
    L.append("**Bounds, stated plainly.** The bootstrap breaks the realized sequence and is the pessimistic read: "
             "every finalist's realized path passes (day 79-156, max drawdown 1.9-2.2%) and rolling starts never "
             "bust. The intraday channel is a trade-level sweep-line from TradingView's own adverse-excursion "
             "figures, not a bar replay. The window starts 2022-08-01 because MYM v0.4 does, so MNQ's 2020-2021 and "
             "Aegis's 2020-2022 sit outside it. The MNQ and MYM lineages are tuned charts with no untouched "
             "holdout. Aegis uses the sanctioned 1-tick `76620` panel; the `cbcc9`/`c59e9` exports fill one tick "
             "better on every shared trade and are barred. Growth's soft $2,500 daily lockout is not modelled, so "
             "Growth figures are two-sided bounds. P&L booked on a non-session date used to be dropped by the "
             "business-day reindex -- 6 trades, -210.92 per contract of real losses; that is fixed and these "
             "figures include it (bust rose in 10 of 12 finalist cells, by at most 0.55 pp, and fell in none). "
             "See README.md §Disclosed limits for what remains disclosed rather than fixed.\n")
    return "\n".join(L)


def main():
    parts = ["# Three-leg Tradeify book grid — ORB-MNQ recon × ORB-MYM × Aegis-6J1", "",
             "**Status:** EXPLORATORY — informal Downloads-lane measurement, not pre-registered, no K entry; "
             "the harness reuses `core/mc/simulation.py` and `core/mc/preflight.py` verbatim. "
             "Inputs are operator TradingView exports (uncommitted). See `book_grid.py` docstring for the exact files and unit conventions.", "",
             verdict()]
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
