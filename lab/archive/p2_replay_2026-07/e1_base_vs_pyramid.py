"""Q-P2-MEASURE-1.b mechanism probe: split DJ30 E1 exit-row P&L into BASE vs
PYRAMID-ADD legs on each feed, windowed. Tests whether the win-side shrinkage
(gross_win ratio 0.296 vs gross_loss ratio 0.478) is concentrated in the
pyramid legs -- the signature of a pyramid-sizing artifact of running the
unmodified CFD Pine on a $0.50/pt MYM chart, vs a real edge decay that would
show up in the BASE trades too.
"""
import os
import sys
from pathlib import Path

# This driver lives alongside p2_ingest/p2_envelope_e1 — import relatively so it
# runs from any clone, not just the worktree it was authored in.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from p2_ingest import load_export
import p2_envelope_e1 as env

# Vendor exports are gitignored (public-clone posture); default to the operator's
# Downloads, overridable via P2_EXPORT_DIR on other machines.
DL = Path(os.environ.get("P2_EXPORT_DIR", str(Path.home() / "Downloads")))
PEP = DL / "Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-07-03_70416.csv"
CME = DL / "Striker_DJ30_v4.5_CBOT_MINI_MYM1!_2026-07-03_b5a41.csv"
START, END = "2025-07-03", "2026-07-03"


def split(csv):
    df = load_export(csv)
    win = env.filter_window(df, START, END)
    exits = win[win["Type"].str.startswith("Exit", na=False)].copy()
    exits["is_add"] = exits["Signal"].astype(str).str.contains("Add", case=False)
    exits["pnl"] = exits["Net P&L USD"].astype(float)
    return exits


def stats(pnl):
    gw = pnl[pnl > 0].sum(); gl = pnl[pnl <= 0].sum()
    return dict(n=len(pnl), nw=(pnl > 0).sum(), nl=(pnl <= 0).sum(),
               gw=gw, gl=gl, pf=(gw/abs(gl) if gl else float("inf")), net=pnl.sum())


def show(label, ex):
    base = ex[~ex["is_add"]]["pnl"]
    add = ex[ex["is_add"]]["pnl"]
    print(f"\n=== {label} ===")
    for tag, s in (("BASE", stats(base)), ("PYRAMID-ADD", stats(add)), ("ALL", stats(ex['pnl']))):
        print(f"  {tag:12s}: n={s['n']:2d} (W{s['nw']}/L{s['nl']})  "
              f"gw={s['gw']:>11,.0f}  gl={s['gl']:>10,.0f}  PF={s['pf']:.3f}  net={s['net']:>11,.0f}")
    return dict(base=stats(base), add=stats(add), all=stats(ex["pnl"]))


p = show("DJ30 PEPPERSTONE (US30)", split(PEP))
c = show("DJ30 CME (MYM1!)", split(CME))

print("\n=== CME/PEP RATIOS (the diagnostic) ===")
print(f"  BASE gross_loss ratio  : {abs(c['base']['gl'])/abs(p['base']['gl']):.3f}   <- ~ point-value factor (base losses, no pyramid)")
print(f"  BASE gross_win  ratio  : {c['base']['gw']/p['base']['gw']:.3f}")
print(f"  BASE PF: pep {p['base']['pf']:.3f} -> cme {c['base']['pf']:.3f}  (ratio {c['base']['pf']/p['base']['pf']:.3f})")
print(f"  PYRAMID gross_win ratio: {c['add']['gw']/p['add']['gw']:.3f}   <- if << base ratio, pyramid winners truncated on MYM")
print(f"  PYRAMID net: pep {p['add']['net']:,.0f} -> cme {c['add']['net']:,.0f}")
print()
print(f"  ALL PF: pep {p['all']['pf']:.3f} -> cme {c['all']['pf']:.3f} (ratio {c['all']['pf']/p['all']['pf']:.3f}, E1 floor 0.8)")
print(f"  --> If BASE-only PF ratio >= 0.8 but ALL < 0.8, the miss lives in the")
print(f"      pyramid-sizing layer (fixable by the B2 MYM integer/RESERVE port),")
print(f"      NOT in the base edge (which would be real transfer decay).")
