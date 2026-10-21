import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from payout_sim import Program, Phase
# Tradeify, current-purchase terms, 21 Oct 2026 (help centre). Funded floor locks at start+100.
def tradeify(size):
    k = {50: 0, 100: 1, 150: 2}[size]
    pick = lambda *v: v[k]
    wthr = pick(150, 200, 250)
    P = {}
    P[f"TFY Select Flex {size}K"] = Program(f"TFY Select Flex {size}K", pick(165,265,369), pick(109,169,239), 0,
        Phase(target=pick(3000,6000,9000), dd=pick(2000,3000,4500), dd_type="eod", cons=0.4, min_days=3),
        Phase(dd=pick(2000,3000,4500), dd_type="eod", lock=100, win_days=5, win_thr=wthr, cap=pick(2500,3500,4500), frac=0.5, min_pay=250))
    P[f"TFY Select Daily {size}K"] = Program(f"TFY Select Daily {size}K", pick(165,265,369), pick(109,169,239), 0,
        Phase(target=pick(3000,6000,9000), dd=pick(2000,3000,4500), dd_type="eod", cons=0.4, min_days=3),
        Phase(dd=pick(2000,2500,3500), dd_type="eod", lock=100, dll=pick(1000,1250,1750), buffer=pick(2100,2600,3600),
              excess=True, cap=pick(1250,1750,2500), min_pay=250))
    P[f"TFY Growth {size}K"] = Program(f"TFY Growth {size}K", pick(145,255,369), pick(95,169,229), 0,
        Phase(target=pick(3000,6000,9000), dd=pick(2000,3500,5000), dd_type="eod", dll=pick(1250,2500,3750), min_days=1),
        Phase(dd=pick(2000,3500,5000), dd_type="eod", lock=100, dll=pick(1250,2500,3750), cons=0.35, win_days=5, win_thr=wthr,
              buffer=pick(3000,4500,6500), cap=pick(1500,2000,2500), min_pay=pick(500,1000,1500)))
    P[f"TFY Lightning {size}K"] = Program(f"TFY Lightning {size}K", pick(492,660,796), 0, 0, None,
        Phase(dd=pick(2000,4000,5250), dd_type="eod", lock=100, dll=pick(1250,2500,3000), cons=0.20,
              buffer=pick(3000,6000,9000), cap=pick(2000,2500,3000), min_pay=1000))
    return P

# Other firms, 50K, current purchase terms as surveyed 21 Oct 2026. [F]=firm page, [3P]=third party.
def others50():
    P = {}
    # Topstep Combine (no-activation-fee path $95/mo [F]); 55% consistency; DLL $1,000 soft (assumed);
    # XFA standard path: MLL $2K EODT locks at 0; 5 winning days >= $150; 50% of balance up to $2K; min $125.
    P["Topstep 50K (no-act path)"] = Program("Topstep 50K", 95, 95, 0,
        Phase(target=3000, dd=2000, dd_type="eod", lock=0, dll=1000, cons=0.55, min_days=2),
        Phase(dd=2000, dd_type="eod", lock=0, win_days=5, win_thr=150, cap=2000, frac=0.5, min_pay=125), monthly=95)
    # MFFU Rapid [F]: $209 one-time, no reset (rebuy); eval EODT, 50% cons, 2 days; funded IDT lock +100,
    # daily payouts above $2,100 buffer, min $500, 90/10; cap not stated.
    P["MFFU Rapid 50K"] = Program("MFFU Rapid 50K", 209, 209, 0,
        Phase(target=3000, dd=2000, dd_type="eod", cons=0.5, min_days=2),
        Phase(dd=2000, dd_type="intraday", lock=100, buffer=2100, excess=True, min_pay=500))
    # MFFU Pro [F]: $265; funded EODT, first payout after 14 calendar days (~10 trading), min $1,000,
    # up to 60% before buffer clears (modelled as 60% of profit), split 80/20.
    P["MFFU Pro 50K"] = Program("MFFU Pro 50K", 265, 265, 0,
        Phase(target=3000, dd=2000, dd_type="eod", cons=0.5, min_days=2),
        Phase(dd=2000, dd_type="eod", lock=100, min_days=10, frac=0.6, min_pay=1000, split=0.8))
    # Lucid Flex [F rules, 3P price $140, reset assumed = rebuy]: eval 40% cons, 3 days; funded no cons,
    # 5 days >= $150, 50% of profit up to $2K, min $500, lock +100.
    P["Lucid Flex 50K"] = Program("Lucid Flex 50K", 140, 140, 0,
        Phase(target=3000, dd=2000, dd_type="eod", cons=0.4, min_days=3),
        Phase(dd=2000, dd_type="eod", lock=100, win_days=5, win_thr=150, cap=2000, frac=0.5, min_pay=500))
    # Alpha Standard [F]: $129/mo, reset $109; eval 50% cons; qualified: Guard $1K soft, 40% cons,
    # 5 winning days >= $200, 50% of profit, $500-$3K, 90%. MLL locks at start.
    P["Alpha Standard 50K"] = Program("Alpha Standard 50K", 129, 109, 0,
        Phase(target=3000, dd=2000, dd_type="eod", lock=0, cons=0.5),
        Phase(dd=2000, dd_type="eod", lock=0, dll=1000, cons=0.4, win_days=5, win_thr=200, cap=3000, frac=0.5, min_pay=500), monthly=129)
    # FundedNext Flex [F, verified 2026-10-21 at helpfutures.fundednext.com art. 17229848]: $74.99 first two
    # purchases, reset $82.99 (landing-page FAQ conflicts); PT $2.5K / MLL $1.5K EODT, eval 40% cons.
    # Funded: MLL $1.5K EODT locking at start+$100; 5 benchmark days >= $200 and >= $500 cycle profit;
    # 50% of profit up to $1.5K, min $250, 95%; account ends after the 5th payout.
    P["FundedNext Flex 50K"] = Program("FundedNext Flex 50K", 75, 83, 0,
        Phase(target=2500, dd=1500, dd_type="eod", cons=0.4),
        Phase(dd=1500, dd_type="eod", lock=100, win_days=5, win_thr=200, buffer=500, cap=1500, frac=0.5, min_pay=250, split=0.95))
    # TradeDay Fast Pass [F]: $95/mo promo, reset $95; eval 45% cons, 3 days; funded EODT, 45% cons,
    # 5 winning days >= $150, 50% of balance up to $1.5K, min $250, 80/20; DD locks at start.
    P["TradeDay FastPass 50K"] = Program("TradeDay FastPass 50K", 95, 95, 0,
        Phase(target=3000, dd=2000, dd_type="eod", lock=0, cons=0.45, min_days=3),
        Phase(dd=2000, dd_type="eod", lock=0, cons=0.45, win_days=5, win_thr=150, cap=1500, frac=0.5, min_pay=250, split=0.8), monthly=95)
    # Alpha Direct [F]: $519, no eval; Guard $1K; 20% cons; first goal $3K; withdrawal $500-$2K; 90%.
    P["Alpha Direct 50K"] = Program("Alpha Direct 50K", 519, 0, 0, None,
        Phase(dd=2000, dd_type="eod", lock=0, dll=1000, cons=0.2, buffer=3000, cap=2000, min_pay=500))
    return P
