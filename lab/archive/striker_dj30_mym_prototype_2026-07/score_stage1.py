"""Stage-1 edge-preservation scoring for the DJ30->MYM v0.1 prototype.

Reuses the FROZEN p2_replay E1 scorer logic (p2_envelope_e1.e1_ratios /
score_e1) verbatim. It bypasses ONLY run_p2_replay.py's CLI `first_trade_sanity`
guard, which is a +/-3x magnitude check built for the 153x JPY-conversion
corruption class and is incompatible with a commission-laden futures export:
MYM trade #1 is a tiny 2-pt move whose net is dominated by the $0.61/side
commission (gross ~+$17 -> net -$3.74, ratio 0.22 < 0.33). That is a legitimate
cost effect, not corruption. Gate thresholds (PF>=0.8x AND net>=0.7x) and the
e1_ratios math are UNCHANGED.

CAVEAT (read the verdict accordingly): net_ratio = cme.net/pep.net compares raw
dollars. The MYM edition is $0.50/pt, commission-laden, integer-sized off a
$150K basis; the CFD baseline is $1/pt, commission-free, percent-of-equity off
$200K. So net_ratio is confounded by point value + sizing basis + costs. PF
ratio is exposure-insensitive and is the clean edge-transfer signal (per the
P2 RESULTS Observation #2).

Pre-registration: docs/briefs/pre-registration/2026-07-08-striker-dj30-mym-prototype-prereg.md
"""
import sys
from pathlib import Path

P2 = Path("C:/Users/joshu/multi_firm_operations/lab/analysis/p2_replay_2026-07")
sys.path.insert(0, str(P2))

from p2_ingest import load_export  # noqa: E402
import p2_envelope_e1 as env  # noqa: E402

BASE = Path("C:/Users/joshu/multi_firm_operations/core/data/tv_exports")
PEP = BASE / "pepperstone" / "Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-07-08_f5f5b.csv"
CME = BASE / "cme" / "Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv"

WINDOWS = [
    ("OOS HOLDOUT", "2023-01-01", "2026-06-30"),
    ("IN-SAMPLE regime cross-check", "2020-01-01", "2022-12-31"),
]

df_pep = load_export(str(PEP), source_tz="America/New_York")
df_cme = load_export(str(CME), source_tz="America/New_York")

overall = []
for label, start, end in WINDOWS:
    r = env.e1_ratios("dj30", df_pep, df_cme, start, end)
    verdict = env.score_e1(r, 0.8, 0.7)
    overall.append((label, r, verdict))
    print(f"\n########## STAGE-1 {label} ({start} -> {end}) ##########")
    print(env.format_ratios(r))
    print(f"E1 VERDICT (PF>=0.8x AND net>=0.7x): {verdict}")

print("\n========== STAGE-1 SUMMARY ==========")
for label, r, verdict in overall:
    print(f"{label:<32} PF_ratio={r.pf_ratio:.3f}  net_ratio={r.net_ratio:.3f}  -> {verdict}")
both_pass = all(v == "PASS" for _, _, v in overall)
print(f"\nStage-1 gate (BOTH windows PASS required): {'CLEARED' if both_pass else 'NOT CLEARED'}")
