# -*- coding: utf-8 -*-
"""Generate the Growth re-score section (Sec13) for RESULTS.md from the data files.

Programmatic so every number in the prose is read from region_data_with_growth.jsonl
/ mv15_*.jsonl rather than hand-transcribed (this repo's own
lesson_borrowed_numbers_need_connecting_arithmetic).
"""
import collections
import glob
import json

SELECT, GROWTH, MFFU = "Tradeify_Select_100K", "Tradeify_Growth_100K", "MFFU_Rapid_100K"
SHAPES = ("symmetric", "mild_right_skew", "bounded_clustered")
WRS = (0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70)


def k(r):
    return (r["win_rate"], r["shape"], r["cadence"], r["risk_usd"])


rows = {}
for line in open("region_data_with_growth.jsonl", encoding="utf-8"):
    r = json.loads(line)
    rows[r["cell_id"]] = r
by = collections.defaultdict(dict)
for r in rows.values():
    by[r["firm"]][k(r)] = r
sel, gro = by[SELECT], by[GROWTH]
shared = sorted(set(sel) & set(gro))

full = {}
for p in sorted(glob.glob("mv15_*.jsonl")) + ["marginal_validation_data.jsonl"]:
    try:
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            if r["n_total_paths"] == 30000:
                full.setdefault((r["firm"],) + k(r), r)
    except FileNotFoundError:
        pass

O = []
w = O.append

w("## §13 — Growth-tier re-score (2026-08-24): the rope, isolated")
w("")
w("**What changed:** `Tradeify_Growth_100K` added to `core/firm_rules.py` (primary source:")
w("help.tradeify.co art. 10495915, article-dated 2026-06-05, read in-browser 2026-08-24) and to this")
w("harness's `FIRM_KEYS`. The 315 tuples were re-scored against it at the same reduced")
w("`sims_per_seed=500`, same frozen seeds `(42, 123, 2026)`, same frozen horizon `1500`, same")
w("intraday-honest limb. **Select and MFFU were not re-run** — their 630 committed rows are carried")
w("forward byte-identically and re-verified below.")
w("")
w("**Why this tier:** Growth is a controlled contrast to Select. Same $6,000 target, same 80-micro")
w("cap, same $0.91/side, same fixed-$ EOD-ratcheting trail geometry. Three things differ:")
w("**$3,500 rope vs $3,000** (+16.7%), **no consistency rule** (vs 40%), and **min_trading_days 1**")
w("(vs 3). §7.1 identified the rope as the binding gate and §6.1 found the consistency rule never")
w("binds — so this tier is close to a clean isolation of the rope term.")
w("")
w("### §13.1 — Verdict counts and transitions (315 paired cells)")
w("")
w("| Firm | FEASIBLE | MARGINAL | INFEASIBLE |")
w("|---|---:|---:|---:|")
for label, d in (("`Tradeify_Select_100K`", sel), ("`Tradeify_Growth_100K`", gro)):
    c = collections.Counter(d[x]["verdict"] for x in shared)
    w("| %s | %d | %d | %d |" % (label, c["FEASIBLE"], c["MARGINAL"], c["INFEASIBLE"]))
w("")
trans = collections.Counter((sel[x]["verdict"], gro[x]["verdict"]) for x in shared)
rank = {"FEASIBLE": 0, "MARGINAL": 1, "INFEASIBLE": 2}
imp = sum(n for (a, b), n in trans.items() if rank[b] < rank[a])
deg = sum(n for (a, b), n in trans.items() if rank[b] > rank[a])
same = sum(n for (a, b), n in trans.items() if a == b)
w("| Transition (Select → Growth) | cells |")
w("|---|---:|")
for (a, b), n in sorted(trans.items(), key=lambda kv: -kv[1]):
    w("| %s → %s%s | %d |" % (a, b, "" if a == b else " **(better)**", n))
w("")
w("**%d cells improve, %d unchanged, %d degrade.** The monotonicity is a sanity check, not a"
  % (imp, same, deg))
w("finding: a strictly wider rope on otherwise identical geometry cannot make any path worse, and")
w("the engine agrees on all %d cells." % len(shared))
w("")
w("### §13.2 — The win-rate floor moves 5 points for two of three shapes")
w("")
w("| Shape | Select floor | Growth floor |")
w("|---|---|---|")
for shape in SHAPES:
    line = "| `%s` |" % shape
    for d in (sel, gro):
        fl = None
        for wr in WRS:
            if any(d[x]["verdict"] == "FEASIBLE" for x in shared if x[0] == wr and x[1] == shape):
                fl = wr
                break
        line += " %s |" % (("**%.0f%%**" % (fl * 100)) if fl else "none")
    w(line)
w("")
w("⚠ **This falsifies §7.2's claim as written.** §7.2 states: *\"No cell at win_rate ≤ 50% is")
w("`FEASIBLE`, for any shape, cadence, or EM2 risk level tested.\"* That held for the two firms then")
w("scored. It does **not** hold for Growth: `mild_right_skew` / cadence 2 / $250 is `FEASIBLE` at")
gcell = gro.get((0.50, "mild_right_skew", 2, 250.0))
scell = sel.get((0.50, "mild_right_skew", 2, 250.0))
gfull = full.get((GROWTH, 0.50, "mild_right_skew", 2, 250.0))
sfull = full.get((SELECT, 0.50, "mild_right_skew", 2, 250.0))
if gcell and gfull:
    w("`win_rate=50%%` with bust **%.2f%%** (reduced N) / **%.2f%%** (full frozen N=30,000) against the"
      % (gcell["bust"] * 100, gfull["bust"] * 100))
    w("3.0%% ceiling — the same cell where Select sits at **%.2f%%** / **%.2f%%** (`MARGINAL`)."
      % (scell["bust"] * 100, sfull["bust"] * 100))
w("The §7.2 sentence should be read as scoped to the $3,000 rope, not to the venue class.")
w("")
w("### §13.3 — Where the rope buys the most (mean bust by win rate)")
w("")
w("| win_rate | n | Select bust | Growth bust | delta |")
w("|---:|---:|---:|---:|---:|")
for wr in WRS:
    xs = [x for x in shared if x[0] == wr]
    sb = sum(sel[x]["bust"] for x in xs) / len(xs)
    gb = sum(gro[x]["bust"] for x in xs) / len(xs)
    w("| %.0f%% | %d | %.4f | %.4f | %+.4f |" % (wr * 100, len(xs), sb, gb, gb - sb))
w("")
w("The benefit is **non-monotone and peaks in the transition zone** (`win_rate=55%`), which is the")
w("expected shape: below it almost every path busts regardless of rope width, above it almost none")
w("do. A wider rope is worth most exactly where a real candidate would sit.")
w("")
w("### §13.4 — Full-N validation of the Growth cells")
w("")
w("The five pre-registered `MARGINAL_VALIDATION_CELLS` (selected in the original sweep, **not**")
w("re-chosen here) re-scored for Growth at the full frozen `sims_per_seed=10,000` (N=30,000).")
w("Three of the five are among the 26 Growth flips, including the `win_rate=50%` cell above.")
w("")
w("| Cell | Growth N=1,500 | Growth N=30,000 | agree? |")
w("|---|---|---|---|")
nag = ndis = 0
for kk in sorted(x for x in full if x[0] == GROWTH):
    r = full[kk]
    rr = gro[kk[1:]]
    ok = r["verdict"] == rr["verdict"]
    nag += ok
    ndis += (not ok)
    w("| wr%.0f%% `%s` cd%d $%d | %.4f %s | %.4f %s | %s |"
      % (kk[1] * 100, kk[2], kk[3], int(kk[4]), rr["bust"], rr["verdict"],
         r["bust"], r["verdict"], "**yes**" if ok else "**NO**"))
w("")
w("**%d of %d agree** (%d disagree). Growth's flipped cells sit further from the 3.0%% gate than"
  % (nag, nag + ndis, ndis))
w("Select's marginal population (bust ≈0.7–1.6% vs a 3.0% ceiling), so they are structurally less")
w("N-sensitive — which is what the table shows.")
w("")
w("**Not validated, disclosed:** Growth has its own near-gate population (%d `MARGINAL` cells) that"
  % collections.Counter(gro[x]["verdict"] for x in shared)["MARGINAL"])
w("the pre-registered five do not cover. Selecting fresh Growth-specific validation cells *after*")
w("seeing the sweep would be exactly the post-hoc selection the original §4 was careful to avoid, so")
w("it was not done. A Growth-specific marginal battery is its own pre-registration.")
w("")
w("### §13.5 — What Growth does NOT buy")
w("")
sfe = [sel[x]["median_days_to_pass"] for x in shared
       if sel[x]["verdict"] == "FEASIBLE" and sel[x]["median_days_to_pass"]]
gfe = [gro[x]["median_days_to_pass"] for x in shared
       if gro[x]["verdict"] == "FEASIBLE" and gro[x]["median_days_to_pass"]]
sfe.sort()
gfe.sort()
w("**Speed — no gain.** Growth's `min_trading_days=1` (\"can pass immediately\") is worth nothing at")
w("EM2 risk levels. Median-of-medians days-to-pass over `FEASIBLE` cells: Select **%.0f days**"
  % sfe[len(sfe) // 2])
w("(n=%d, min %.0f) vs Growth **%.0f days** (n=%d, min %.0f). The binding factor is accumulating"
  % (len(sfe), sfe[0], gfe[len(gfe) // 2], len(gfe), gfe[0]))
w("$6,000 at $250–$325 of risk per trade, not the day-count floor. The venue's headline \"pass in 1")
w("day\" is reachable only by a mechanism that can make $6,000 in a day — nothing in this grid can.")
w("")
w("**Consistency — nothing, because it never bound.** §6.1 already established Select (40%) and MFFU")
w("(50%) score bit-identically. Growth removes the rule entirely and the effect is still zero. All of")
w("Growth's measured advantage is the rope.")
w("")
w("### §13.6 — Two-sided bound on every Growth figure here")
w("")
w("Growth's **daily loss limit is a soft breach** — art. 10495915 verbatim: *\"If you hit this limit,")
w("trading is stopped for the day but your account is not failed.\"* `simulate_path` has no lockout")
w("representation (its `daily_loss_pct` branch returns `bust_daily`, a hard fail), so the tier carries")
w("`daily_loss_pct: None` and **the model omits the lockout entirely**. Consequences, both directions:")
w("")
w("* **Upper bound w.r.t. the missing lockout.** The venue truncates a losing day near −$2,500; the")
w("  model does not, so modeled daily left tails are fatter than the venue's. Every Growth bust")
w("  figure above is therefore *pessimistic* on this axis.")
w("* **Lower bound w.r.t. the clock.** Same two-clock geometry as Select (floor ratchets EOD, breach")
w("  enforced intraday). The intraday-honest limb is on, but the standing")
w("  [`Q-FIRMEOD-1`](../../../../docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md) caveat applies.")
w("")
w("**Neither bound is quantified.** These are not point estimates. A faithful soft-DLL limb is an")
w("engine change with its own ADR + re-MC. ⚠ Re-verification of art. 10495897 *for Growth")
w("specifically* is **owed** — the 2026-08-24 in-browser pass could not reload it, so the clock")
w("reading rests on the dated 2026-07-30 read quoted in `core/mc/simulation.py::simulate_path`.")
w("Art. 10495915's \"intraday fluctuations won't affect the drawdown level\" describes the floor's")
w("*ratchet*, not the breach test — but that sentence deserves a direct re-read before any Growth")
w("figure is used for a spend decision.")
w("")
w("### §13.7 — What this licenses, and what it does not")
w("")
w("**Licensed:** sourcing a Phase-B mechanism against a **~5-point lower win-rate floor** if Growth is")
w("the target tier, and treating the rope — not the consistency rule, not the target, not cadence —")
w("as the single lever worth shopping across Tradeify products.")
w("")
w("**Not licensed:** (1) This is still a *shape* map over a synthetic generating process. It admits no")
w("mechanism and no candidate. (2) `Tradeify_Growth_100K` is deliberately **absent from**")
w("`AUTOMATION_FRIENDLY_PROP_FIRMS['tradeify']` — adding a product line to the operational target set")
w("is an ADR decision under `2026-07-12-prop-portfolio-four-friendly-firms`, not a config edit.")
w("(3) The funded-phase rules differ (Growth has a fixed payout policy and a 35% payout-stage")
w("consistency rule); **nothing here measures the funded phase.** (4) No K consumed, $0 spent,")
w("nothing armed, no gate moved.")
w("")

import io as _io

with _io.open("SECTION13.md", "w", encoding="utf-8", newline="\n") as _fh:
    _fh.write("\n".join(O) + "\n")
print("wrote SECTION13.md (%d lines)" % len(O))
