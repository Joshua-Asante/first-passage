import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from payout_sim import first_payout
from programs import tradeify, others50
o=others50(); t=tradeify(50)
for name,prog in [("TFY Select Flex 50K",t["TFY Select Flex 50K"]),("Topstep 50K",o["Topstep 50K (no-act path)"]),("FundedNext Flex 50K",o["FundedNext Flex 50K"]),("TFY Lightning 50K",t["TFY Lightning 50K"])]:
    for S in [0.0,0.5]:
        for sd in [400,800]:
            r=first_payout(prog,S,sd,take=750,H=120,N=3000,min_net=1000)
            print(f"{name:22s} S={S} sd={sd} P={r['p_pay']:.2f} cost=${r['cost']:.0f} $/payout={r['cost']/max(r['p_pay'],1e-9):.0f} evpass/attempt={r['ev_pass']:.2f} net(first pay - cost)=${r['net']:.0f}")
