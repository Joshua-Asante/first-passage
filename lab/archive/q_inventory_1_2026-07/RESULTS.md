# Q-INVENTORY-1 — RESULTS

**Date:** 2026-07-17 · **Verdict: `FALSIFIED` — the admissible band is empty at the cost of one bounded pass.**

| Phase | Status |
|---|---|
| 0 — dedup + bank re-read | DONE ([`PHASE0.md`](PHASE0.md)) — banks GC/MGC 3,177 · ES 2 · NQ 1+1(open) · others 0; dead-class wall emitted |
| 1 — rank-1 citation traversal (Baltussen 2021) | DONE — S2 + OpenAlex, ≈90 unique citing works screened, 0 admissible |
| 2 — rank-2/3 passes (surveys + futures-native journals, Q1–Q6 by reference) | DONE — 22 searches across two passes, 0 admissible |
| 3 — sniff arithmetic | DONE ([`CANDIDATE_ROWS.md`](CANDIDATE_ROWS.md)) — 8 row-groups detail-sniffed, every kill inside the measured pattern |
| 4 — verdict + closure | **FALSIFIED** → [`closure`](lab/archive/../../docs/briefs/closures/Q-INVENTORY-1-closure-falsified.md); accept-idle recorded as the default |

**H-INVENTORY-1 rejected:** the frozen scope completed with **0 seeds** passing Req 1–5 at sniff level. Kill distribution: power-wall ×3 (pre-FOMC, announcement-day premium, post-FOMC Treasuries), cost-wall ×1 at the 4× multiple (FX fixing-window drift — published net-positive on CME futures, still <4×RT gross), informed-flow/leakage ×1 (macro pre-release drift — "Drift Begone" causal shutoff), venue-wall ×5 (VIX/KC/Nikkei/Deribit/China), K-wall ×1 (gold fixes). **No novel kill mode** → no new lesson entry per §9 (the 4×-kills-published-net-positive nuance is recorded in CANDIDATE_ROWS R3 as a sharpening of the standing cost-law lesson, not a new registry entry).

**Three UNSCREENABLE stubs** with named recovery routes recorded below-the-line (ZN auction δ · CL EIA unconditional δ · carry timing-δ) — priced in the closure as operator probe-funding forks; none funded by this brief (§4 pre-declared).

**Disposition:** accept-idle is the recorded default — the 2026-11-08 idle guard fires as designed; discovery stays parked pending new external evidence; the deployment axis (Q-RAIL-1) is unaffected. The SESSIONS zero-survivor board line is DISCHARGED.
