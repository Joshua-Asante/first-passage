#!/usr/bin/env python3
"""Independent re-derivation + confound stress of the Q-NAS-4 surviving graded tendency.
Re-derives the quarter table from the panel CSV (does NOT trust the ground-truth JSON for
the leg classification or per-quarter tallies). Uses the GT JSON ONLY for the 8 proxy-sign
quarters (2022-2023) where real bars aren't on hand, so signs match the audited table exactly.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/tender-perlman-7824ea")
DL = Path(r"C:/Users/joshu/Downloads")
PANEL = DL / "Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-24_11605.csv"
GT = REPO / "lab" / "analysis" / "q_nas_4_2026-06-20" / "qnas4_results.json"
rng = np.random.default_rng(424242)

# ---- 1. Re-derive legs + quarter table from panel ----
df = pd.read_csv(PANEL, encoding="utf-8-sig"); df.columns = [c.strip() for c in df.columns]
tid, pnl, px = "Trade #", "Net P&L USD", "Price USD"
df[tid] = df[tid].astype(int)
en = df[df["Type"].str.startswith("Entry")].copy()
ex = df[df["Type"].str.startswith("Exit")].copy()
legs = en[[tid, "Date and time", "Signal", px]].rename(columns={"Date and time": "edt", "Signal": "esig", px: "epx"}).merge(
    ex[[tid, "Date and time", "Signal", px, pnl]].rename(columns={"Date and time": "xdt", "Signal": "xsig", px: "xpx", pnl: "pnl"}),
    on=tid, how="inner").sort_values(tid).reset_index(drop=True)
legs["leg_type"] = np.where(legs["esig"].str.contains("Add"), "pyramid_add", "base")
legs["xdt"] = pd.to_datetime(legs["xdt"])
legs["q"] = legs["xdt"].dt.to_period("Q").astype(str)
legs["is_mh_add"] = (legs["xsig"] == "Max Hold") & (legs["leg_type"] == "pyramid_add")

print(f"RECONCILE: n_legs={len(legs)} net={legs['pnl'].sum():.2f} "
      f"PF={legs[legs.pnl>0].pnl.sum()/abs(legs[legs.pnl<=0].pnl.sum()):.3f} "
      f"WR={ (legs.pnl>0).mean()*100:.2f}%")

# ---- 2. Build per-quarter tally (n_trades, monster_present) from panel; signs from GT ----
gt = json.loads(GT.read_text())
sign_map = {}
for q, v in gt["real_bar_quarters"].items():
    sign_map[q] = int(np.sign(v))
# proxy signs for 2022-2023 from the GT quarter_table
for r in gt["quarter_table"]:
    if r["idx_src"] == "panel_proxy" and r["q"] not in sign_map and r["idx_sign"] is not None:
        sign_map[r["q"]] = int(r["idx_sign"])

agg = legs.groupby("q").agg(n_trades=("pnl", "size"), n_mh_add=("is_mh_add", "sum")).reset_index()
agg["monster_present"] = agg["n_mh_add"] >= 1
agg["sign"] = agg["q"].map(sign_map)
agg = agg[agg["sign"].notna()].copy()
agg["sign"] = agg["sign"].astype(int)
agg = agg.sort_values("q").reset_index(drop=True)
print("\nQUARTER TABLE (re-derived):")
print(agg.to_string(index=False))

pos = agg[agg["sign"] > 0]; neg = agg[agg["sign"] < 0]
a = int(pos["monster_present"].sum()); b = int((~pos["monster_present"]).sum())
c = int(neg["monster_present"].sum()); d = int((~neg["monster_present"]).sum())
table = [[a, b], [c, d]]
odds, p_fish = stats.fisher_exact(table, alternative="greater")
print(f"\nBASE GATE: pos {a}/{b} (present/absent), neg {c}/{d}; concordance={a+d}/{len(agg)}; Fisher p_greater={p_fish:.4f}")

# ---------------------------------------------------------------------------
# PROBE 1: trade-frequency confound — is sign-association independent of n_trades?
# ---------------------------------------------------------------------------
print("\n" + "="*70 + "\nPROBE 1: TRADE-FREQUENCY CONFOUND")
# (a) does n_trades predict monster_present? (logistic-style: point-biserial / Mann-Whitney)
mp = agg["monster_present"].astype(int).to_numpy(); nt = agg["n_trades"].to_numpy(); sg = agg["sign"].to_numpy()
print(f"  n_trades: monster-present mean={nt[mp==1].mean():.2f} (n={mp.sum()}), "
      f"absent mean={nt[mp==0].mean():.2f} (n={(mp==0).sum()})")
rho_nt_mp = stats.spearmanr(nt, mp)
print(f"  Spearman(n_trades, monster_present) = {rho_nt_mp.statistic:.3f}  p={rho_nt_mp.pvalue:.3f}")
rho_nt_sg = stats.spearmanr(nt, sg)
print(f"  Spearman(n_trades, sign)            = {rho_nt_sg.statistic:.3f}  p={rho_nt_sg.pvalue:.3f}")
# (b) PARTIAL association: condition the permutation on n_trades.
#     Null model: monster_present arises purely from trade count. P(monster|n) increases with n
#     because more legs -> more chances of a MH-add. So shuffle SIGN labels but STRATIFY by n_trades
#     tertiles, so the null preserves any n_trades structure that monster_present rides on.
# Stratified permutation: permute signs WITHIN n_trades tertiles, recompute concordance.
agg["nt_bin"] = pd.qcut(agg["n_trades"], 3, labels=False, duplicates="drop")
obs_conc = a + d
N = 50000
def strat_perm_p():
    perm = np.empty(N)
    sg_arr = agg["sign"].to_numpy(); mp_arr = mp; bins = agg["nt_bin"].to_numpy()
    for i in range(N):
        s = sg_arr.copy()
        for bv in np.unique(bins):
            idx = np.where(bins == bv)[0]
            s[idx] = rng.permutation(s[idx])
        perm[i] = ((mp_arr == 1) & (s > 0)).sum() + ((mp_arr == 0) & (s < 0)).sum()
    return (perm >= obs_conc).mean(), perm
p_strat, perm_strat = strat_perm_p()
# unstratified for comparison
def unstrat_perm_p():
    perm = np.empty(N); sg_arr = agg["sign"].to_numpy()
    for i in range(N):
        s = rng.permutation(sg_arr)
        perm[i] = ((mp == 1) & (s > 0)).sum() + ((mp == 0) & (s < 0)).sum()
    return (perm >= obs_conc).mean()
p_unstrat = unstrat_perm_p()
print(f"  Permutation concordance>={obs_conc}: unstratified p={p_unstrat:.4f} | "
      f"STRATIFIED-by-n_trades p={p_strat:.4f}")
# (c) The cleanest model-free partial: does the gate survive among quarters of SIMILAR n_trades?
#     Restrict to quarters within the central n_trades band [9,14] (drops extremes) and re-test.
band = agg[(agg["n_trades"] >= 9) & (agg["n_trades"] <= 14)]
bp = band[band.sign>0]; bn = band[band.sign<0]
ba=int(bp.monster_present.sum()); bb=int((~bp.monster_present).sum())
bc=int(bn.monster_present.sum()); bd=int((~bn.monster_present).sum())
if (ba+bb)>0 and (bc+bd)>0:
    _, p_band = stats.fisher_exact([[ba,bb],[bc,bd]], alternative="greater")
else:
    p_band = float("nan")
print(f"  n_trades-band [9,14] (n={len(band)}): pos {ba}/{bb}, neg {bc}/{bd}; Fisher p={p_band:.4f}")

# ---------------------------------------------------------------------------
# PROBE 2: leverage — drop the 2 biggest-monster quarters, re-test
# ---------------------------------------------------------------------------
print("\n" + "="*70 + "\nPROBE 2: LEVERAGE (drop 2 biggest-monster quarters)")
big2 = agg.sort_values("n_mh_add", ascending=False).head(2)
print(f"  Two biggest-monster quarters: {list(zip(big2.q, big2.n_mh_add, big2.sign))}")
drop = agg[~agg["q"].isin(big2["q"])]
dp = drop[drop.sign>0]; dn = drop[drop.sign<0]
da=int(dp.monster_present.sum()); db=int((~dp.monster_present).sum())
dc=int(dn.monster_present.sum()); dd=int((~dn.monster_present).sum())
_, p_drop = stats.fisher_exact([[da,db],[dc,dd]], alternative="greater")
print(f"  After drop (n={len(drop)}): pos {da}/{db}, neg {dc}/{dd}; concordance={da+dd}/{len(drop)}; Fisher p={p_drop:.4f}")
# also drop the two biggest-monster POSITIVE quarters specifically (the ones carrying the assoc)
big2pos = pos.sort_values("n_mh_add", ascending=False).head(2)
print(f"  Two biggest-monster POSITIVE quarters: {list(zip(big2pos.q, big2pos.n_mh_add))}")
drop2 = agg[~agg["q"].isin(big2pos["q"])]
d2p = drop2[drop2.sign>0]; d2n = drop2[drop2.sign<0]
e_a=int(d2p.monster_present.sum()); e_b=int((~d2p.monster_present).sum())
e_c=int(d2n.monster_present.sum()); e_d=int((~d2n.monster_present).sum())
_, p_drop2 = stats.fisher_exact([[e_a,e_b],[e_c,e_d]], alternative="greater")
print(f"  After drop-2-pos (n={len(drop2)}): pos {e_a}/{e_b}, neg {e_c}/{e_d}; Fisher p={p_drop2:.4f}")
# jackknife: drop each quarter once, range of p
jk = []
for qq in agg["q"]:
    sub = agg[agg["q"] != qq]
    sp = sub[sub.sign>0]; sn = sub[sub.sign<0]
    _, pj = stats.fisher_exact([[int(sp.monster_present.sum()), int((~sp.monster_present).sum())],
                                 [int(sn.monster_present.sum()), int((~sn.monster_present).sum())]], alternative="greater")
    jk.append((qq, pj))
jk.sort(key=lambda z: z[1])
print(f"  Jackknife (drop-1) p range: min={jk[0]} ... max={jk[-1]}")

# ---------------------------------------------------------------------------
# PROBE 3: multiplicity / post-hoc selection — Bonferroni over the gate family + prior-cost
# ---------------------------------------------------------------------------
print("\n" + "="*70 + "\nPROBE 3: MULTIPLICITY / POST-HOC SELECTION")
# Family of monster definitions actually examined in the GT: {mh_add, any_add, any_mh}. 3 tests.
fam = {"mh_add(primary)": p_fish}
for key, col in [("any_add", "n_add"), ("any_mh", "n_mh")]:
    pass
# rebuild any_add / any_mh from panel
legs["is_add"] = legs["leg_type"] == "pyramid_add"
legs["is_mh"] = legs["xsig"] == "Max Hold"
agg2 = legs.groupby("q").agg(any_add=("is_add", "max"), any_mh=("is_mh", "max")).reset_index()
agg2["sign"] = agg2["q"].map(sign_map); agg2 = agg2[agg2.sign.notna()]; agg2["sign"]=agg2.sign.astype(int)
for nm, col in [("any_add", "any_add"), ("any_mh", "any_mh")]:
    p = agg2[agg2.sign>0]; n = agg2[agg2.sign<0]
    _, pp = stats.fisher_exact([[int(p[col].sum()), int((~p[col].astype(bool)).sum())],
                                 [int(n[col].sum()), int((~n[col].astype(bool)).sum())]], alternative="greater")
    fam[nm] = pp
print(f"  Gate family p-values: {{ {', '.join(f'{k}={v:.4f}' for k,v in fam.items())} }}")
m = len(fam)
print(f"  Family size m={m}. Bonferroni-adjusted primary p = min(1, {p_fish:.4f}*{m}) = {min(1, p_fish*m):.4f}")
# also: this gate def was SELECTED on the 2y subset. Honest accounting: the def survived because
# the 2y subset showed a CLEAN split. Test: is the 4y result simply re-confirming the same quarters?
# The 2y/96 subset ~ which quarters? (the most recent ~8 quarters). Show the OUT-OF-PRIOR-WINDOW test:
# fit the gate on 2022-2023 (8 proxy q) ONLY, then the 2024-2026 real-bar q as held-out.
in_prior = agg[agg["q"] >= "2024Q1"]   # the real-bar half ~ where the 2y prior lived
held = agg[agg["q"] < "2024Q1"]        # the older proxy half = genuinely added by going to 4y
for nm, sub in [("2024-2026 (real, near prior)", in_prior), ("2022-2023 (proxy, newly added)", held)]:
    p = sub[sub.sign>0]; n = sub[sub.sign<0]
    if len(p)>0 and len(n)>0:
        _, pp = stats.fisher_exact([[int(p.monster_present.sum()), int((~p.monster_present).sum())],
                                     [int(n.monster_present.sum()), int((~n.monster_present).sum())]], alternative="greater")
    else:
        pp = float("nan")
    print(f"  Half-test {nm} (n={len(sub)}): pos {int(p.monster_present.sum())}/{int((~p.monster_present).sum())}, "
          f"neg {int(n.monster_present.sum())}/{int((~n.monster_present).sum())}; Fisher p={pp:.4f}")
