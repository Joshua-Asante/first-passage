import json, collections, sys, pathlib
SP = str(pathlib.Path(__file__).resolve().parent)
new={}
for l in open(f'{SP}/longpanel_ropematched.jsonl'):
    r=json.loads(l); new[r['cell_id']]=r
old={}
for l in open(str(pathlib.Path(SP).parents[0]/'shape_feasibility_map_2026-08'/'region_data_with_growth.jsonl')):
    r=json.loads(l); old[r['cell_id']]=r
print(f"long-panel rows: {len(new)}\n")
print("!! READ THIS FIRST: longpanel_ropematched.jsonl scales risk by rope/3000 per tier, so its")
print("!! Growth/50K/25K columns are NOT comparable to the committed map (which holds risk fixed).")
print("!! For the matched-risk comparison use longpanel_growth_matchedrisk.jsonl and")
print("!! longpanel_select50k_matchedrisk.jsonl -- see RESULTS.md section 6.\n")

FIRMS=['Tradeify_Select_100K','Tradeify_Growth_100K','Tradeify_Select_50K','Tradeify_Select_25K']
print("A. Verdict counts at 520wk (committed) vs 5,200wk (this pass)")
print(f"{'tier':24s} {'520wk  FEAS / MARG / INFEAS':>30} {'5200wk  FEAS / MARG / INFEAS':>32}")
for f in FIRMS:
    n=[r for r in new.values() if r['firm']==f]
    cn=collections.Counter(r['verdict'] for r in n)
    o=[r for r in old.values() if r['firm']==f]
    co=collections.Counter(r['verdict'] for r in o) if o else None
    olds = f"{co['FEASIBLE']:>6} / {co['MARGINAL']:>4} / {co['INFEASIBLE']:>6}" if co else f"{'not scored':>22}"
    print(f"{f:24s} {olds:>30} {cn['FEASIBLE']:>10} / {cn['MARGINAL']:>4} / {cn['INFEASIBLE']:>6}")

print("\nB. Verdict transitions 520wk -> 5,200wk (only tiers A2 actually scored)")
for f in ['Tradeify_Select_100K','Tradeify_Growth_100K']:
    t=collections.Counter()
    for cid,r in new.items():
        if r['firm']!=f or cid not in old: continue
        t[(old[cid]['verdict'], r['verdict'])]+=1
    print(f"  {f}")
    order=['FEASIBLE','MARGINAL','INFEASIBLE']
    worse=better=same=0
    rank={'FEASIBLE':2,'MARGINAL':1,'INFEASIBLE':0}
    for (a,b),c in sorted(t.items()):
        tag = 'unchanged' if a==b else ('WORSE' if rank[b]<rank[a] else 'better')
        if a==b: same+=c
        elif rank[b]<rank[a]: worse+=c
        else: better+=c
        print(f"     {a:11s} -> {b:11s} {c:>4}   {tag}")
    print(f"     TOTAL: {same} unchanged, {worse} degrade, {better} improve\n")

print("C. Lowest win rate with any FEASIBLE cell, by shape and tier (the 'floor')")
print(f"{'tier':24s} {'symmetric':>12} {'mild_right_skew':>17} {'bounded_clustered':>19}")
for f in FIRMS:
    row=[]
    for sh in ['symmetric','mild_right_skew','bounded_clustered']:
        wrs=[r['win_rate'] for r in new.values() if r['firm']==f and r['shape']==sh and r['verdict']=='FEASIBLE']
        row.append(f"{min(wrs)*100:.0f}%" if wrs else "none")
    print(f"{f:24s} {row[0]:>12} {row[1]:>17} {row[2]:>19}")
print("\n   (committed A2 at 520wk, for comparison: Select100K 65/55/60, Growth100K 60/50/60)")

print("\nD. The section 13.2 headline cell at 5,200 weeks")
for f in ['Tradeify_Select_100K','Tradeify_Growth_100K']:
    cid=f"wr0.50_mild_right_skew_cd2_rk250_{f}"
    if cid in new:
        print(f"   {f:24s} committed {old[cid]['verdict']:>10} (bust {old[cid]['bust']:.4f})  ->  "
              f"long panel {new[cid]['verdict']:>10} (bust {new[cid]['bust']:.4f})")

print("\nE. Does any win_rate <= 50% cell clear at a long panel, on any tier?")
for f in FIRMS:
    hits=[r['cell_id'] for r in new.values() if r['firm']==f and r['win_rate']<=0.50 and r['verdict']=='FEASIBLE']
    print(f"   {f:24s} {len(hits)} cell(s)" + (f"  {hits[:3]}" if hits else ""))
