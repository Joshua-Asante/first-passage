#!/usr/bin/env python3
"""Q-NAS-4 PROBE: adversarially try to RESCUE the strict sign-gate.
Independent re-derivation of the quarter monster tally from the panel CSV, then:
  (a) flat-bin reframe: exclude |idx_ret|<theta quarters, recompute gate on strong-trend remainder
      -- swept over ALL theta in {1.0,1.5,2.0,2.5,3.0} to expose bin-tuning multiplicity
  (b) magnitude threshold reframe: monster ~ |ret| instead of sign
Cites exact Fisher + permutation p-values. Re-uses the VERIFIED idx_ret/idx_sign per quarter
(real bars 2024-2026 + validated proxy 2022-2023) read from qnas4_quarter_table.csv, but RE-DERIVES
the monster tally from the raw panel to confirm n_mh_add per quarter independently.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from itertools import combinations

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/tender-perlman-7824ea")
DL = Path(r"C:/Users/joshu/Downloads")
PANEL = DL / "Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-24_11605.csv"
QTBL = REPO / "lab/analysis/q_nas_4_2026-06-20/qnas4_quarter_table.csv"
rng = np.random.default_rng(424242)  # different seed than ground-truth to confirm perm stability

# ---- 1. INDEPENDENT re-derivation of monster tally from raw panel ----
df = pd.read_csv(PANEL, encoding="utf-8-sig"); df.columns = [c.strip() for c in df.columns]
tid, pnl, px = "Trade #", "Net P&L USD", "Price USD"
df[tid] = df[tid].astype(int)
en = df[df["Type"].str.startswith("Entry")].copy()
ex = df[df["Type"].str.startswith("Exit")].copy()
legs = en[[tid, "Date and time", "Signal"]].rename(columns={"Date and time": "edt", "Signal": "esig"}).merge(
    ex[[tid, "Date and time", "Signal", pnl]].rename(columns={"Date and time": "xdt", "Signal": "xsig", pnl: "pnl"}),
    on=tid, how="inner").sort_values(tid).reset_index(drop=True)
legs["leg_type"] = np.where(legs["esig"].str.contains("Add"), "pyramid_add", "base")
legs["xdt"] = pd.to_datetime(legs["xdt"])
legs["q"] = legs["xdt"].dt.to_period("Q").astype(str)
legs["is_mh_add"] = (legs["xsig"] == "Max Hold") & (legs["leg_type"] == "pyramid_add")

n_legs = len(legs); net = legs["pnl"].sum()
print(f"INDEP RECONCILE: n_legs={n_legs} net={net:.2f}  (LOCK target n=196 net=369698.40)  "
      f"match={'YES' if n_legs==196 and abs(net-369698.40)<1.0 else 'NO'}")

mtally = legs.groupby("q")["is_mh_add"].sum().astype(int)

# ---- 2. join verified idx_ret/idx_sign ----
qt = pd.read_csv(QTBL)
qt = qt[qt["idx_sign"].notna()].copy()
qt["idx_sign"] = qt["idx_sign"].astype(int)
# cross-check the precomputed n_mh_add against MY independent tally
qt["my_n_mh_add"] = qt["q"].map(mtally).fillna(0).astype(int)
mismatch = qt[qt["n_mh_add"] != qt["my_n_mh_add"]]
print(f"MONSTER-TALLY cross-check vs precomputed: "
      f"{'ALL MATCH' if len(mismatch)==0 else 'MISMATCH:'}")
if len(mismatch): print(mismatch[["q","n_mh_add","my_n_mh_add"]].to_string(index=False))
qt["monster_present"] = qt["my_n_mh_add"] >= 1

# ---- gate engine ----
def gate(sub, label):
    pos = sub[sub["idx_sign"] > 0]; neg = sub[sub["idx_sign"] < 0]
    a = int(pos["monster_present"].sum()); b = int((~pos["monster_present"]).sum())
    c = int(neg["monster_present"].sum()); d = int((~neg["monster_present"]).sum())
    table = [[a, b], [c, d]]
    _, pf = stats.fisher_exact(table, alternative="greater")
    obs = a + d
    signs = sub["idx_sign"].to_numpy(); present = sub["monster_present"].to_numpy().astype(bool)
    N = 50000; perm = np.empty(N)
    for i in range(N):
        s = rng.permutation(signs)
        perm[i] = (present & (s > 0)).sum() + (~present & (s < 0)).sum()
    pp = (perm >= obs).mean()
    clean = (b == 0 and c == 0)   # clean gate = monster in EVERY pos, NONE in any neg
    return {"label": label, "n_q": len(sub), "n_pos": len(pos), "n_neg": len(neg),
            "pos_present": a, "pos_absent": b, "neg_present": c, "neg_absent": d,
            "concordance": f"{obs}/{len(sub)}", "clean_gate": clean,
            "fisher_p": round(float(pf), 4), "perm_p": round(float(pp), 4)}

print("\n=== BASELINE (all 18 q, sign gate) ===")
base = gate(qt, "all18_sign")
print(json.dumps(base, indent=2))

# ---- (a) FLAT-BIN sweep ----
print("\n=== (a) FLAT-BIN reframe sweep (exclude |idx_ret|<theta) -- POST-HOC BIN-TUNING ===")
flat_rows = []
for theta in [1.0, 1.5, 2.0, 2.5, 3.0]:
    sub = qt[qt["idx_ret_pct"].abs() >= theta].copy()
    excluded = sorted(qt.loc[qt["idx_ret_pct"].abs() < theta, "q"].tolist())
    g = gate(sub, f"flat>={theta}")
    g["excluded_quarters"] = excluded
    flat_rows.append(g)
    print(f"theta={theta}: n_q={g['n_q']} (excl {len(excluded)}: {excluded}) "
          f"pos[pres/abs]={g['pos_present']}/{g['pos_absent']} neg[pres/abs]={g['neg_present']}/{g['neg_absent']} "
          f"CLEAN={g['clean_gate']} fisher_p={g['fisher_p']} perm_p={g['perm_p']}")

# ---- (b) MAGNITUDE threshold reframe: monster ~ |ret| ----
print("\n=== (b) MAGNITUDE reframe: does monster track |ret| rather than sign? ===")
qt["abs_ret"] = qt["idx_ret_pct"].abs()
sp_abs = stats.spearmanr(qt["abs_ret"], qt["monster_present"].astype(int))
sp_sgn = stats.spearmanr(qt["idx_ret_pct"], qt["monster_present"].astype(int))
print(f"Spearman(|ret|, monster)    rho={sp_abs.statistic:.3f}  p={sp_abs.pvalue:.4f}")
print(f"Spearman(signed ret, monster) rho={sp_sgn.statistic:.3f}  p={sp_sgn.pvalue:.4f}")
# point-biserial: mean |ret| present vs absent; mean signed ret present vs absent
pres = qt[qt["monster_present"]]; abst = qt[~qt["monster_present"]]
print(f"mean |ret|: monster-present={pres['abs_ret'].mean():.2f}  monster-absent={abst['abs_ret'].mean():.2f}")
print(f"mean signed ret: present={pres['idx_ret_pct'].mean():.2f}  absent={abst['idx_ret_pct'].mean():.2f}")
mw_abs = stats.mannwhitneyu(pres["abs_ret"], abst["abs_ret"], alternative="greater")
mw_sgn = stats.mannwhitneyu(pres["idx_ret_pct"], abst["idx_ret_pct"], alternative="greater")
print(f"Mann-Whitney present>absent on |ret|:    U p={mw_abs.pvalue:.4f}")
print(f"Mann-Whitney present>absent on signed ret: U p={mw_sgn.pvalue:.4f}")

# ---- (c) multiplicity honesty: how many of the swept reframes 'go clean'? ----
n_clean_flat = sum(1 for g in flat_rows if g["clean_gate"])
print(f"\n=== MULTIPLICITY: flat-bin reframes that go CLEAN: {n_clean_flat}/{len(flat_rows)} "
      f"(any 'clean' here is selected from {len(flat_rows)} theta tries + sign/mag axis = post-hoc) ===")

# ---- best-case adversarial: the SINGLE most favorable theta ----
best = max(flat_rows, key=lambda g: (g["clean_gate"], -g["fisher_p"]))
print(f"BEST adversarial flat reframe: {best['label']} clean={best['clean_gate']} fisher_p={best['fisher_p']}")

out = {"indep_reconcile": {"n_legs": n_legs, "net": round(float(net),2),
                           "match": bool(n_legs==196 and abs(net-369698.40)<1.0)},
       "tally_crosscheck_mismatches": int(len(mismatch)),
       "baseline_sign_gate": base, "flat_bin_sweep": flat_rows,
       "magnitude": {"spearman_absret": round(float(sp_abs.statistic),3), "spearman_absret_p": round(float(sp_abs.pvalue),4),
                     "spearman_signed": round(float(sp_sgn.statistic),3), "spearman_signed_p": round(float(sp_sgn.pvalue),4),
                     "mean_absret_present": round(float(pres['abs_ret'].mean()),2), "mean_absret_absent": round(float(abst['abs_ret'].mean()),2),
                     "mw_absret_p": round(float(mw_abs.pvalue),4), "mw_signed_p": round(float(mw_sgn.pvalue),4)},
       "n_clean_flat_reframes": n_clean_flat, "best_flat": best}
with open(REPO / "lab/analysis/q_nas_4_2026-06-20/probe_rescue_results.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nwrote probe_rescue_results.json")
