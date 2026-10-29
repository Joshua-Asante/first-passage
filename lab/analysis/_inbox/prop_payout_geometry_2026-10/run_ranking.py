import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
from payout_sim import first_payout
from programs import tradeify, others50
progs = {k:v for k,v in tradeify(50).items()}
progs.update(others50())
progs["TFY Select Flex 100K"] = tradeify(100)["TFY Select Flex 100K"]
res = {}
for name, prog in progs.items():
    big = "100K" in name
    tgt = 6000 if big else (prog.ev.target if prog.ev else 3000)
    for S in [1.0, 2.0, 2.7]:
        rows = []
        for sd in ([400,600,900,1200] if big else [250,400,600,800]):
            for take in [None, 0.25, 0.35]:
                tk = None if take is None else take * tgt
                r = first_payout(prog, S, sd, take=tk, H=120, N=2500, min_net=1000)
                rows.append(dict(sd=sd, take=tk, **{k: float(v) for k, v in r.items()}))
        res[f"{name}|{S}"] = rows
        bp = max(rows, key=lambda r: r['p_pay'])
        bc = min((r for r in rows if r['p_pay'] > 0.05), key=lambda r: r['cost'] / r['p_pay'], default=bp)
        print(f"{name:26s} S={S}  maxP: P={bp['p_pay']:.2f} cost=${bp['cost']:.0f} days={bp['days_med']:.0f} sd={bp['sd']} take={bp['take']} | min$/payout: ${bc['cost']/bc['p_pay']:.0f} (P={bc['p_pay']:.2f}, sd={bc['sd']}, take={bc['take']})", flush=True)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ranking_results.json'),'w'))
