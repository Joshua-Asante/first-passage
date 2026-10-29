import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import itertools
from payout_sim import first_payout
from programs import tradeify
H=120
for size in [50,100]:
  for name,prog in tradeify(size).items():
    for S in [1.0,2.0,2.7]:
      best=[]
      scale = size/100
      for sd in [x*scale for x in (300,500,800,1200)]:
        for stop,take in [(None,None),(None,0.25),(None,0.4),(0.5,0.4)]:
          tk = None if take is None else take*{50:3000,100:6000}[size]
          st = None if stop is None else stop*{50:2000,100:3000}[size]
          r=first_payout(prog,S,sd,stop=st,take=tk,H=H,N=2500)
          best.append((r['p_pay'],sd,st,tk,r))
      # report max P and also best P per $ (P/cost)
      bp=max(best,key=lambda b:b[0]); be=max(best,key=lambda b:b[0]/b[4]['cost'])
      for tag,b in (("maxP",bp),("P/$",be)):
        r=b[4]
        print(f"{name:24s} S={S} {tag:5s} sd={b[1]:6.0f} stop={b[2]} take={b[3]}  P={r['p_pay']:.2f} cost=${r['cost']:.0f} days={r['days_med']} pay1=${r['first_pay']:.0f} evpass={r['ev_pass']:.2f}")
