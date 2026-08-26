# ORB-MNQ-1 skew-derived sizing ceiling probe (2026-08-20)

**Status:** ACTIVE — Skew-derived `pol_cushion` sizing ceiling vs the borrowed 0.75 constant — informal $0/K=0 null, neither derived candidate beats the borrowed constant on pass rate. See [MNQ.md](../../../ops/instruments/MNQ.md) N18.

Informal $0/K=0 probe, not pre-registered (parameter-search null on an already-verified
mechanism, not a mechanism-family question -- same class as Q-GEOFIT-1, no formal Pre-Q
warranted per that precedent). Tests whether a `pol_cushion`-shaped sizing ceiling derived
from ORB-MNQ-1's own loss-tail (rather than borrowed unchanged from Q-EVALSEQ-1's 2-leg book)
beats the borrowed `0.75` constant on the intraday-honest cushion-sizing gate check.

**Finding (independently verified, CONFIRMED, no defects beyond one 0.01pp rounding slip):**
ORB-MNQ-1's own loss tail structurally licenses a much higher ceiling than 0.75 on pure
floor-safety grounds (breakeven `DD/(|L_worst|*k) = 2.41` at k=1, vs the borrowed 0.75 -- bust
stays 0.00% for any ceiling in that range, not a close call). That headroom is **not**
actionable on the metric that actually differentiates the candidates: pushing to the licensed
max (ceiling=1.00) roughly matches-to-slightly-underperforms the borrowed 0.75 on pass rate
(worse on 4/6 tested slices); pulling to a conservative half (ceiling=0.50) underperforms on
all 6 slices, sometimes substantially. Neither derived candidate measurably beats the borrowed
constant. Full comparison table, exact derivation, and script: see the workflow transcript this
probe was run under, or re-run `run_evalseq_orb_derived_ceiling.py` directly (~3.5 min, $0).

Recorded as `ops/instruments/MNQ.md` finding N18.

**Script:** `run_evalseq_orb_derived_ceiling.py` -- imports `day_loop_intraday`/`build_paths_orb`/
`run_policy_orb`/`pol_const`/`pol_cushion`/`DD` unchanged from
`../orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py`. Fidelity-controlled
(reproduces published 67.67% bust at k=1 before trusting anything downstream). Rerun:
`python lab/analysis/c1/orbmnq1_skew_sizing_probe_2026-08-20/run_evalseq_orb_derived_ceiling.py`.

**Result JSON:** `evalseq_orb_derived_ceiling_results.json`.
