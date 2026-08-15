"""Q-P2-MEASURE-1.b cheap falsifier: is DJ30's E1 PF miss (5.642 -> 3.491) a
few-trade/selection artifact or a systematic per-trade transfer cost?

Reproduces the E1 anchor first (reconcile discipline), then decomposes:
  - gross win / loss, win/loss counts, avg win/loss per feed
  - drop-top-k winners: how fragile is each PF to its biggest winners?
  - loss-side: is CME's gross_loss inflated by a few big losers the CFD lacks?
  - biggest winners/losers side by side

No cross-feed trade pairing yet (that's the next cut if this is inconclusive).
"""
import os
import sys
from pathlib import Path

# This driver lives alongside p2_ingest/p2_envelope_e1 — import relatively so it
# runs from any clone, not just the worktree it was authored in.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import pandas as pd
from p2_ingest import load_export
import p2_envelope_e1 as env

# Vendor exports are gitignored (public-clone posture); default to the operator's
# Downloads, overridable via P2_EXPORT_DIR on other machines.
DL = Path(os.environ.get("P2_EXPORT_DIR", str(Path.home() / "Downloads")))
PEP = DL / "Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-07-03_70416.csv"
CME = DL / "Striker_DJ30_v4.5_CBOT_MINI_MYM1!_2026-07-03_b5a41.csv"
START, END = "2025-07-03", "2026-07-03"


def exit_pnl(csv):
    df = load_export(csv)
    win = env.filter_window(df, START, END)
    exits = win[win["Type"].str.startswith("Exit", na=False)]
    return exits["Net P&L USD"].astype(float).reset_index(drop=True)


def decompose(label, pnl):
    wins = pnl[pnl > 0]
    losses = pnl[pnl <= 0]
    gw, gl = wins.sum(), losses.sum()
    pf = gw / abs(gl) if gl != 0 else float("inf")
    print(f"\n=== {label} ===")
    print(f"  n_exit_rows : {len(pnl)}")
    print(f"  wins/losses : {len(wins)} / {len(losses)}  (WR {100*len(wins)/len(pnl):.1f}%)")
    print(f"  gross_win   : {gw:,.2f}")
    print(f"  gross_loss  : {gl:,.2f}")
    print(f"  PF          : {pf:.3f}")
    print(f"  net         : {pnl.sum():,.2f}")
    print(f"  avg_win     : {gw/len(wins):,.2f}" if len(wins) else "  avg_win     : n/a")
    print(f"  avg_loss    : {gl/len(losses):,.2f}" if len(losses) else "  avg_loss    : n/a")
    top_w = wins.sort_values(ascending=False).head(5).tolist()
    top_l = losses.sort_values().head(5).tolist()
    print(f"  top 5 wins  : {[round(x) for x in top_w]}")
    print(f"  top 5 losses: {[round(x) for x in top_l]}")
    # drop-top-k winners
    print("  drop-top-k winners -> PF:")
    for k in (1, 2, 3):
        w_sorted = wins.sort_values(ascending=False)
        gw_k = w_sorted.iloc[k:].sum()
        pf_k = gw_k / abs(gl) if gl != 0 else float("inf")
        print(f"    drop {k}: PF={pf_k:.3f}  (gross_win {gw_k:,.0f})")
    return dict(n=len(pnl), pf=pf, gw=gw, gl=gl, wins=wins, losses=losses)


print("Q-P2-MEASURE-1.b — DJ30 E1 PF decomposition")
print(f"window {START} -> {END}")
pep = exit_pnl(PEP)
cme = exit_pnl(CME)

# reconcile against the published E1 anchor before decomposing
def pf_of(pnl):
    gw = pnl[pnl > 0].sum(); gl = pnl[pnl <= 0].sum()
    return gw / abs(gl)
print("\n--- E1 anchor reconciliation (must match RESULTS.md) ---")
print(f"  PEP: PF={pf_of(pep):.3f} net={pep.sum():,.2f}  (expect 5.642 / 117,349.57)")
print(f"  CME: PF={pf_of(cme):.3f} net={cme.sum():,.2f}  (expect 3.491 / 30,097.00)")

p = decompose("DJ30 PEPPERSTONE (US30)", pep)
c = decompose("DJ30 CME (MYM1!)", cme)

print("\n=== SUMMARY ===")
print(f"  PF ratio cme/pep = {c['pf']/p['pf']:.3f}  (E1 floor 0.8x -> {'PASS' if c['pf']/p['pf']>=0.8 else 'MISS'})")
print(f"  win-count delta  : pep {len(p['wins'])} vs cme {len(c['wins'])}")
print(f"  loss-count delta : pep {len(p['losses'])} vs cme {len(c['losses'])}")
print(f"  gross_loss ratio cme/pep = {abs(c['gl'])/abs(p['gl']):.3f}")
print(f"  gross_win  ratio cme/pep = {c['gw']/p['gw']:.3f}")
