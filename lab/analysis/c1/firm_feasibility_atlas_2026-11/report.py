"""Render the generated tables of RESULTS.md from atlas.csv (between the GENERATED markers).

    python -I scripts/fp.py python lab/analysis/c1/firm_feasibility_atlas_2026-11/report.py
"""
from __future__ import annotations

import math
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
for p in (ROOT / "core", ROOT / "lab"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from discovery.prop_survivor_scoring import load_scoring_thresholds  # noqa: E402
from firm_rules import AUTOMATION_FRIENDLY_PROP_FIRMS, FIRM_RULES  # noqa: E402
from research_utils.camp_import import load_camp_sibling  # noqa: E402

A = load_camp_sibling("atlas", __file__)
BEGIN, END = "<!-- GENERATED:BEGIN (report.py) -->", "<!-- GENERATED:END -->"
REF = {"p": 0.50, "lam": 1.0, "mae": "mid"}   # reference slice for the compact tables


def pct(x: float) -> str:
    return "—" if math.isnan(x) else f"{100 * x:.1f}"


def worst_by_shape(rows):
    """{tier: {(f,e,p,lam,mae): worst row over the tier's configs}} — what lookup() returns."""
    out: dict = defaultdict(dict)
    for r in rows:
        k = (r["f"], r["e"], r["p"], r["lam"], r["mae"])
        cur = out[r["tier"]].get(k)
        if cur is None:
            out[r["tier"]][k] = dict(r)
            continue
        cur["pass"] = min(cur["pass"], r["pass"])
        cur["bust"] = max(cur["bust"], r["bust"])
        cur["unresolved"] = max(cur["unresolved"], r["unresolved"])
        for t in ("ttp_p50", "ttp_p90"):
            vals = [v for v in (cur[t], r[t]) if not math.isnan(v)]
            cur[t] = max(vals) if vals else math.nan
        cur["p_pass_22"] = min(cur["p_pass_22"], r["p_pass_22"])
    return out


def feasible(r, thr) -> bool:
    return r["bust"] <= thr.eval_bust_ceiling and r["pass"] >= thr.pass_floor


def render(rows) -> str:
    thr = load_scoring_thresholds()
    W = worst_by_shape(rows)
    tiers = [t for fam in AUTOMATION_FRIENDLY_PROP_FIRMS.values() for t in fam]
    mark = {r["tier"]: r["mark"] for r in rows}
    L = [BEGIN, ""]
    L.append(f"Feasibility label: bust ≤ {thr.eval_bust_ceiling:.2f} and pass ≥ {thr.pass_floor:.2f}, "
             f"parsed at render time from `{Path(thr.source_path).name}` "
             f"(+ {len(thr.addenda)} addendum) by `load_scoring_thresholds()`. "
             "Every figure is synthetic; MEDIUM tiers read worst over their sensitivity configs.")
    L += ["", "### Coverage", "",
          "| Tier | Mark | DD $ | Target / DD | Consistency | Min days | Configs | FEASIBLE shapes / 540 |",
          "|---|---|---|---|---|---|---|---|"]
    for t in tiers:
        f = FIRM_RULES[t]
        dd = f["max_dd_pct"] * f["starting_balance"] / 100
        ratio = f["profit_target_pct"] / f["max_dd_pct"]
        cfgs = sorted({r["config"] for r in rows if r["tier"] == t})
        n_ok = sum(feasible(r, thr) for r in W[t].values())
        note = " (bust is a lower bound)" if mark[t] == "EXCLUDED" else ""
        L.append(f"| `{t}` | {mark[t]} | {dd:,.0f} | {ratio:.2f} | "
                 f"{f.get('consistency_rule_pct') or '—'} | {f['min_trading_days']} | {len(cfgs)} | "
                 f"{n_ok}{note} |")

    L += ["", "### Largest FEASIBLE risk fraction `f` by expectancy",
          "", "Cell: largest FEASIBLE `f` over all (p, λ, MAE), then in brackets how many of the 27 "
          "(p, λ, MAE) combinations have any FEASIBLE `f`.", "",
          "| Tier | " + " | ".join(f"E={e:.2f}" for e in A.EXPECTANCIES) + " |",
          "|---|" + "---|" * len(A.EXPECTANCIES)]
    for t in tiers:
        cells = []
        for e in A.EXPECTANCIES:
            best, combos = None, 0
            for p in A.WIN_RATES:
                for lam in A.TRADES_PER_SESSION:
                    for m in A.MAE_ORDER:
                        ok = [f for f in A.RISK_FRACS if feasible(W[t][(f, e, p, lam, m)], thr)]
                        if ok:
                            combos += 1
                            best = max(best or 0, max(ok))
            cells.append("none" if best is None else f"{best:.2f} ({combos}/27)")
        L.append(f"| `{t}` | " + " | ".join(cells) + " |")

    L += ["", "### Cross-tier at one shape (E = 0.10, p = 0.50, λ = 1, MAE mid)", "",
          "| Tier | Mark | f | pass % | bust % | unresolved % | median / p90 days | P(pass ≤ 22) % | P(pass ≤ 63) % |",
          "|---|---|---|---|---|---|---|---|---|"]
    for f in (0.05, 0.10):
        for t in tiers:
            r = W[t][(f, 0.10, 0.50, 1.0, "mid")]
            L.append(f"| `{t}` | {mark[t]} | {f:.2f} | {pct(r['pass'])} | {pct(r['bust'])} | "
                     f"{pct(r['unresolved'])} | {r['ttp_p50']:.0f} / {r['ttp_p90']:.0f} | "
                     f"{pct(r['p_pass_22'])} | {pct(r['p_pass_63'])} |")

    L += ["", f"### Per tier at the reference slice (p = {REF['p']}, λ = {REF['lam']}, MAE {REF['mae']})",
          "", "Cell: pass % / bust % / median business days to pass. **Bold** = FEASIBLE.", ""]
    for t in tiers:
        L.append(f"**`{t}`** ({mark[t]}" + ("; bust is a LOWER BOUND" if mark[t] == "EXCLUDED" else "")
                 + ")")
        L.append("")
        L.append("| f \\ E | " + " | ".join(f"{e:.2f}" for e in A.EXPECTANCIES) + " |")
        L.append("|---|" + "---|" * len(A.EXPECTANCIES))
        for f in A.RISK_FRACS:
            cells = []
            for e in A.EXPECTANCIES:
                r = W[t][(f, e, REF["p"], REF["lam"], REF["mae"])]
                s = f"{pct(r['pass'])} / {pct(r['bust'])} / " + (
                    "—" if math.isnan(r["ttp_p50"]) else f"{r['ttp_p50']:.0f}")
                cells.append(f"**{s}**" if feasible(r, thr) else s)
            L.append(f"| {f:.2f} | " + " | ".join(cells) + " |")
        L.append("")

    # Axis effects on the HIGH reference tier
    ref_tier = "Tradeify_Select_100K"
    L += [f"### Axis effects on `{ref_tier}` (E = 0.10, f = 0.15): bust % by win rate × MAE, "
          "then by trades per session", "",
          "| p \\ MAE | " + " | ".join(A.MAE_ORDER) + " |", "|---|---|---|---|"]
    for p in A.WIN_RATES:
        L.append(f"| {p:.2f} | " + " | ".join(
            pct(W[ref_tier][(0.15, 0.10, p, 1.0, m)]["bust"]) for m in A.MAE_ORDER) + " |")
    L += ["", "| λ | bust % | pass % | median days | P(pass ≤ 22 bdays) % |", "|---|---|---|---|---|"]
    for lam in A.TRADES_PER_SESSION:
        r = W[ref_tier][(0.15, 0.10, 0.50, lam, "mid")]
        L.append(f"| {lam} | {pct(r['bust'])} | {pct(r['pass'])} | {r['ttp_p50']:.0f} | "
                 f"{pct(r['p_pass_22'])} |")

    # Sensitivity deltas (paired, same paths)
    L += ["", "### Sensitivity configs vs their row (paired over all 540 shapes)", "",
          "| Sensitivity | Mean Δbust (pp) | Max Δbust (pp) | Mean Δpass (pp) | Shapes whose label flips |",
          "|---|---|---|---|---|"]
    by_cfg = defaultdict(dict)
    for r in rows:
        by_cfg[r["config"]][(r["f"], r["e"], r["p"], r["lam"], r["mae"])] = r
    for name in sorted(by_cfg):
        if "@" not in name:
            continue
        base = by_cfg[name.split("@")[0]]
        sens = by_cfg[name]
        db = [sens[k]["bust"] - base[k]["bust"] for k in base]
        dp = [sens[k]["pass"] - base[k]["pass"] for k in base]
        flips = sum(feasible(sens[k], thr) != feasible(base[k], thr) for k in base)
        L.append(f"| `{name}` | {100 * sum(db) / len(db):+.2f} | {100 * max(db, key=abs):+.2f} | "
                 f"{100 * sum(dp) / len(dp):+.2f} | {flips} |")

    # Paired identity checks between same-geometry tiers
    L += ["", "### Same-geometry tiers (paired, same paths)", "",
          "| Pair | Max |Δpass| (pp) | Max |Δbust| (pp) |", "|---|---|---|"]
    for a_, b_ in (("Tradeify_Select_25K", "Tradeify_Select_50K"),
                   ("Tradeify_Select_100K", "Tradeify_Select_150K"),
                   ("Bulenox_100K", "Bulenox_150K")):
        ka, kb = by_cfg[a_], by_cfg[b_]
        L.append(f"| `{a_}` vs `{b_}` | {100 * max(abs(ka[k]['pass'] - kb[k]['pass']) for k in ka):.2f} | "
                 f"{100 * max(abs(ka[k]['bust'] - kb[k]['bust']) for k in ka):.2f} |")
    L += ["", END]
    return "\n".join(L)


def main() -> None:
    rows = A.load()
    for r in rows:
        r["ttp_p50"] = float(r["ttp_p50"])
    block = render(rows)
    res = HERE / "RESULTS.md"
    text = res.read_text(encoding="utf-8")
    i, j = text.index(BEGIN), text.index(END) + len(END)
    res.write_text(text[:i] + block + text[j:], encoding="utf-8")
    print(f"updated {res}")


if __name__ == "__main__":
    main()
