#!/usr/bin/env python3
"""Backtest-proxy: does the NAS100 edge survive realistic fill friction, WHERE it is concentrated?

Applies round-trip execution cost to every leg of the LOCK-anchor 4y/196-leg panel and recomputes
net / PF / pyramid-share, under (A) LINEAR cost (cost = c_points x qty) and (B) SIZE-AWARE cost
(slippage grows with order size ~ market impact, penalizing the large pyramid adds specifically).
P&L identity in the TV export: Net P&L USD = (exit-entry) x qty  (qty in $1/point units; lots=qty/10).
So a round-trip cost of c index-points costs c x qty dollars on a leg. CHARACTERIZATION-ONLY.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/tender-perlman-7824ea")
DL = Path(r"C:/Users/joshu/Downloads")
PANEL = DL / "Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-24_11605.csv"   # LOCK anchor n=196
OUT = REPO / "lab" / "analysis" / "q_nas_4_2026-06-20"; OUT.mkdir(parents=True, exist_ok=True)
def jr(x, n=2):
    if isinstance(x,(np.floating,np.integer)): x=x.item()
    if isinstance(x,float) and (np.isnan(x) or np.isinf(x)): return None
    return round(x,n)

# ---- load + pair ----
df = pd.read_csv(PANEL, encoding="utf-8-sig"); df.columns=[c.strip() for c in df.columns]
tid,pnl,px,qty="Trade #","Net P&L USD","Price USD","Size (qty)"
df[tid]=df[tid].astype(int)
en=df[df["Type"].str.startswith("Entry")]; ex=df[df["Type"].str.startswith("Exit")]
L=en[[tid,"Signal",px,qty]].rename(columns={"Signal":"esig",px:"epx",qty:"qty"}).merge(
   ex[[tid,"Signal",px,pnl]].rename(columns={"Signal":"xsig",px:"xpx",pnl:"pnl"}),on=tid).sort_values(tid).reset_index(drop=True)
L["leg_type"]=np.where(L["esig"].str.contains("Add"),"pyramid_add","base")
L["lots"]=L["qty"]/10.0
base_mask=L.leg_type=="base"; add_mask=L.leg_type=="pyramid_add"

# baseline identity check
def cohort(p):
    net=p.sum(); w=p[p>0]; l=p[p<=0]; pf=w.sum()/abs(l.sum()) if l.sum()!=0 else np.inf
    return net, pf, (p>0).mean()*100
net0,pf0,wr0=cohort(L["pnl"])
print(f"BASELINE (c=0): n={len(L)} net={net0:,.2f} PF={pf0:.3f} WR={wr0:.2f}%  "
      f"base_net={L.loc[base_mask,'pnl'].sum():,.0f} add_net={L.loc[add_mask,'pnl'].sum():,.0f} "
      f"pyr_share={L.loc[add_mask,'pnl'].sum()/net0:.4f}")
qmed_base=L.loc[base_mask,"qty"].median()
print(f"qty: base median={qmed_base:.1f} ({qmed_base/10:.1f} lots) | add median={L.loc[add_mask,'qty'].median():.1f} "
      f"({L.loc[add_mask,'qty'].median()/10:.1f} lots) | add max={L['qty'].max():.0f} ({L['qty'].max()/10:.0f} lots)")

def metrics_after(cost_leg):
    pa=L["pnl"]-cost_leg
    net=pa.sum(); w=pa[pa>0]; l=pa[pa<=0]; pf=w.sum()/abs(l.sum()) if l.sum()!=0 else np.inf
    return dict(net=jr(net), pf=jr(pf,3), wr=jr((pa>0).mean()*100,1),
               base_net=jr(pa[base_mask.values].sum()), add_net=jr(pa[add_mask.values].sum()),
               pyr_share=jr(pa[add_mask.values].sum()/net,4) if net>0 else None,
               total_cost=jr(cost_leg.sum()))

# ---------- A) LINEAR cost: c index-points round-trip, cost=c*qty ----------
print("\n=== A) LINEAR cost (round-trip points x qty) ===")
print(f"{'c_pts':>6}{'net':>13}{'PF':>7}{'WR%':>7}{'base_net':>11}{'add_net':>12}{'pyr_share':>10}{'tot_cost':>12}")
gridA={}
for c in [0,1,2,3.5,5,6.5,8,10,12,15,20]:
    m=metrics_after(c*L["qty"]); gridA[c]=m
    print(f"{c:>6}{m['net']:>13,.0f}{m['pf']:>7.3f}{m['wr']:>7.1f}{m['base_net']:>11,.0f}{m['add_net']:>12,.0f}"
          f"{str(m['pyr_share']):>10}{m['total_cost']:>12,.0f}")

# breakeven c (linear) for total / base / add cohorts
def breakeven(mask=None):
    q=L["qty"] if mask is None else L["qty"].where(mask,0)
    p=L["pnl"] if mask is None else L["pnl"].where(mask,0)
    # net(c)=sum(p) - c*sum(q_applied); but cost applies to ALL legs' qty even for a cohort's pnl?
    # cohort breakeven: cost on that cohort's legs only -> c* = sum(p_cohort)/sum(q_cohort)
    if mask is None:
        return p.sum()/L["qty"].sum()
    return p[mask].sum()/L.loc[mask,"qty"].sum()
print(f"\nLINEAR breakeven round-trip cost (points):")
print(f"  total net->0 : {breakeven():.2f} pts   (cost on all legs)")
print(f"  base cohort->0: {breakeven(base_mask):.2f} pts")
print(f"  ADD cohort->0 : {breakeven(add_mask):.2f} pts   <-- friction headroom of the EDGE")

# cost_in_R context: representative base stop distance in points (full-stop-ish base losers)
base_losers=L[base_mask & (L.pnl<0)].copy(); base_losers["mv"]=base_losers["pnl"].abs()/base_losers["qty"]
stop_pts=base_losers["mv"].quantile(0.75)  # upper quartile of base adverse moves ~ near full stop
print(f"\nrepresentative base stop distance ~ {stop_pts:.1f} pts (p75 of base-loser |move|)")
for c in [2,4,7]:
    print(f"  round-trip {c} pts ~ cost_in_R = {c/stop_pts:.3f}R (per base leg)")

# ---------- B) SIZE-AWARE cost: slippage grows with order size (market impact on big adds) ----------
# cost_pts(leg) = spread + 2*slip_base*(qty/qref)^alpha ; qref=base median qty
print("\n=== B) SIZE-AWARE cost (slippage ~ size^alpha; penalizes large adds) ===")
qref=qmed_base
def size_cost(spread, slip_base, alpha):
    cpts = spread + 2.0*slip_base*(L["qty"]/qref)**alpha
    return cpts*L["qty"], cpts
gridB={}
for (spread,slip,alpha,label) in [
    (1.0,0.5,0.0,"linear-tight (a=0)"),
    (2.0,1.0,0.0,"linear-real (a=0)"),
    (2.0,1.0,0.5,"impact sqrt (a=.5)"),
    (2.0,1.0,1.0,"impact linear-size (a=1)"),
    (3.0,2.0,0.5,"impact-stress (a=.5)"),
]:
    cost_leg,cpts=size_cost(spread,slip,alpha); m=metrics_after(cost_leg)
    add_cpts=cpts[add_mask.values]; base_cpts=cpts[base_mask.values]
    gridB[label]=dict(**m, add_cost_pts_median=jr(np.median(add_cpts),1), base_cost_pts_median=jr(np.median(base_cpts),1))
    print(f"  {label:22} net={m['net']:>11,.0f} PF={m['pf']:>6.3f} add_net={m['add_net']:>11,.0f} "
          f"pyr_share={str(m['pyr_share']):>8} | add_cost~{np.median(add_cpts):4.1f}pts base_cost~{np.median(base_cpts):4.1f}pts")

out={"baseline":dict(n=len(L),net=jr(net0),pf=jr(pf0,3),wr=jr(wr0),
        base_net=jr(L.loc[base_mask,'pnl'].sum()),add_net=jr(L.loc[add_mask,'pnl'].sum()),
        pyr_share=jr(L.loc[add_mask,'pnl'].sum()/net0,4)),
     "linear_grid":gridA,
     "linear_breakeven_pts":{"total":jr(breakeven(),2),"base":jr(breakeven(base_mask),2),"add":jr(breakeven(add_mask),2)},
     "rep_base_stop_pts":jr(stop_pts,1),"size_aware":gridB,
     "qty_lots":{"base_median":jr(qmed_base/10,1),"add_median":jr(L.loc[add_mask,'qty'].median()/10,1),"add_max":jr(L['qty'].max()/10,1)}}
json.dump(out, open(OUT/"cost_proxy_results.json","w"), indent=2)
print(f"\n=== wrote {OUT}/cost_proxy_results.json")
