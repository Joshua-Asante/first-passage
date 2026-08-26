# ORB-MNQ-1 cushion-proportional sizing probe (2026-08-20)

**Status:** ACTIVE — Informal $0/K=0 probe (not pre-registered) — cushion-proportional sizing eliminates ORB-MNQ-1's bust intraday-honestly (mathematically real, regime-agnostic); a real 2021-09-28 pass-rate regime break survives a thirds split but its trailing-vol mechanism is REFUTED. Formalized as [`Q-ORBCUSH-1`](../../../docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md), which itself closed `FALSIFIED` 2026-08-20 (trailing mean-R also refuted — `ops/instruments/MNQ.md` N17).

Not a pre-registered campaign -- an informal $0/K=0 probe, preserved for provenance and
re-derivation. The write-up notice this README originally pointed to
(`N-2026-08-20-orbmnq1-cushion-sizing-regime-break-unexplained.md`) was never committed --
dangling reference, caught and corrected 2026-08-20. Findings and routing decision instead
live at [`ops/instruments/MNQ.md`](../../../../ops/instruments/MNQ.md) N17/N18 and
[`docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md`](../../../../docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md)
(regime-break mechanism, `FALSIFIED`/`STOP`) -- read those first. Follow-on gate work:
[`Q-ORBSURV-1`](../../../../docs/briefs/Q-ORBSURV-1-cushion-sizing-gate-configurations.md).

## What's here

Scripts were authored and independently, adversarially verified in a session scratchpad
(three rounds: build the intraday-honest harness → thirds regime-split robustness → trailing-vol
mechanism test) and copied here afterward so the evidence outlives the scratch directory. They
were **not re-tested for portability from this location** -- paths (the cached `MNQ.v.0` panel,
the python interpreter) were resolved relative to the original scratch working directory and may
need adjustment to re-run from here. The logic itself was independently re-derived (a second,
completely separate implementation, not just a re-read) during verification and is trustworthy;
treat these files as an audit record and a re-derivation starting point, not a one-command rerun.

- `run_evalseq_orb_intraday.py` -- the core harness. Ports Q-EVALSEQ-1's `pol_cushion` policy
  (`lab/analysis/c1/q_evalseq_1_2026-08/run_evalseq.py`) onto ORB-MNQ-1's own already-validated
  intraday-honest engine (`core/mc/simulation.py::simulate_path`'s `intraday_low=` mechanism, the
  same one `lab/analysis/orb/orb_mnq_2026-07/run_t2_intraday_bust.py` uses). Fidelity control
  reproduces the published `RESULTS_t2_intraday_bust.md` bust rates (67.67%/77.01% at k=1/k=2) to
  ~0.00pp before any policy read -- independently re-verified via a from-scratch scalar
  reimplementation, zero mismatches across 1,200 cross-checked paths.
- `run_evalseq_orb_thirds.py` -- imports the harness above unchanged; re-runs the same check on a
  three-way (not two-way) split of the panel to test whether the halves-level regime finding was
  boundary-luck. It wasn't -- see the Notice for the corrected regime-break date this surfaced.
- `stage1_characterize.py` / `stage2_regime_gate.py` -- characterizes what actually changes around
  the regime break (realized vol +67-71%, three corroborating measures) and tests a trailing
  (causal, `.shift(1)`, no look-ahead) volatility-regime classifier against it. REFUTED as the
  mechanism -- see the Notice for why (window-instability, no clean date correlation).

## Result JSONs

`evalseq_orb_intraday_results.json`, `evalseq_orb_thirds_results.json`,
`stage1_characterization.json`, `stage2_regime_gate_results.json` -- raw output backing every
number cited in the Notice.
