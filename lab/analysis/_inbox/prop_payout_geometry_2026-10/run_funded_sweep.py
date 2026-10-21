import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eval_barrier_sim import *
print("eval finer grid")
for S in [0,1.0,2.0,2.7,3.5]:
    rows=[]
    for sd in [150,200,250,300,400,600,1000]:
        p,tm,b=eval_sim(S,sd,N=8000); rows.append((sd,p,tm,b))
    print(S, [(r[0],round(r[1],3),r[2],round(r[3],3)) for r in rows])
print("funded Select Flex model, 250d horizon: mean net paid, P(>=1 payout), P(>=5 payouts), P(alive)")
for S in [0,0.7,1.0,2.0,2.7]:
    rows=[]
    for sd in [250,400,600,800,1000]:
        rows.append((sd,)+tuple(round(v,3) for v in funded_sim(S,sd,N=8000)))
    print(S, rows)
