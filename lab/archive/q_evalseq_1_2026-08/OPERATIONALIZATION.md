# Q-EVALSEQ-1 — frozen operationalizations (written BEFORE any policy number is computed)

**Parent pre-registration (frozen, byte-unedited):**
[`2026-07-24-2leg-eval-frontload-schedule-preregistration.md`](../../../../docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md)
— un-dormed scoring-only 2026-08-16 ([P2 closure](../../../../docs/briefs/closures/STATE-POLICY-closure-resolved-p2.md)).
**This file resolves the prereg's two operationalization ambiguities and freezes the at-read
discipline. It is committed before `run_evalseq.py` produces any policy number.** Nothing here
adds a policy, removes one, or touches the §6 gate.

## Instrument

The recovered book-comp harness (tag `pre-prune-2026-08-08`, anchor-verified this session:
`assert_anchors.py` OK; stage-1 winning-day 22.2% matches the de-scope ADR; stage-4 chain
$318/$819 match RESULTS.md). Eval machinery = `gap_stage2.py` `build_paths` + `eval_sim`
(Mon-anchored week-block bootstrap; 10K sims × seeds (11,12,13); h_eval=520; EOD trailing
$3,000 no-lock; target +$6,000; min 3 trading days; 40% consistency; 80-micro cap).

**Fidelity gate (must pass before any policy run):** the policy-capable port
(`eval_sim_policy`, per-day multiplier evaluated on start-of-day state) run with a CONSTANT
multiplier m=1.0 at seeds (11,12,13) must reproduce the recorded 2-leg eval pass **37.78%**
(RESULTS.md: "`pass_pct` 37.78") to 2dp. Fail ⇒ stop and repair; no policy number is read.

> **Gate v2 amendment (2026-08-16, recorded BEFORE any policy number was read).** The v1 gate
> FIRED: port m=1.0 → 38.17% vs anchor 37.78. Diagnosis, run before proceeding: the recovered
> ORIGINAL `gap_stage2.py`, executed unmodified on this environment's regenerated panel, itself
> prints **38.2 ± 0.2** at m=1.0 (and chain $315 vs recorded $318.20) — the port equals the
> original; the drift is environment/panel vintage from the 2026-08-16 rebuild (pandas/numpy
> versions), not a port defect. Gate v2: **port m=1.0 mean must match the regenerated
> original's printed mean (38.2) within ±0.1pp** — the faithfulness property is port≡original
> on the same environment. The 37.78 / $318.20 figures stand as the historical anchors with
> the vintage drift (+0.39pp pass, −~1% chain) disclosed in RESULTS. No policy definition,
> gate criterion, or at-read discipline changes.

## The frozen K=4 family, operationalized

Multipliers are risk_pct-layer factors on the 1.00× book panel (same units as the prereg's
0.50× flat baseline). State is start-of-day: `bal`, `peak` (EOD-updated, as in `eval_sim`),
`cushion = bal − (peak − 3000)`, `profit = bal − 100000`, `t` = trading-day index.

- **(a) flat baseline (control):** m_t = 0.50.
- **(b) linear decay 0.75→0.25:** m_t = clip(0.75 − 0.50·(t / T_b), 0.25, 0.75), with
  **T_b = the control's pooled median pass time** (np.nanmedian of t_pass across the three
  control seeds). Resolution of the prereg's "over the eval" on a venue with no time limit:
  anchored to the control's own median passage — a control statistic, not a policy-selected one.
- **(c) floor-distance-proportional, capped 0.75×:** m_t = 0.75 · min(1, cushion_t / 3000).
  At start cushion = $3,000 ⇒ 0.75; proportional below; no floor (the frozen text names none).
- **(d) step-down-at-cushion:** m_t = 0.75 until **peak ≥ 101,500** (EOD peak ≥ +$1,500,
  literal frozen text), then 0.375 for the rest of the path.

## Gate application (frozen §6, verbatim criteria)

Adopt-eligible ⇔ best non-control policy's eval pass-prob > control + 5.0pt AND bust ≤ control
bust AND the lift survives the both-halves split. Any limb fails ⇒ FALSIFIED (lever spent),
flat WATCH-1 stands. AMBIGUOUS = power short.

- **Selection:** best-of-3 chosen on the FULL panel only; halves verify the selected policy
  (select in-sample only — never re-select per half).
- **Halves:** panel business days split at the midpoint date; week-blocks rebuilt per half;
  same seeds/sims. Survival = on each half, selected policy lift > +5.0pt AND bust ≤ that
  half's control bust.
- **Placebo / selection correction (the prereg's "DSR/placebo … applied to the best-of-K at
  read", operationalized):** 60 sham policies, each an i.i.d. per-day multiplier draw from the
  winner's realized multiplier marginal (destroys state/time-dependence, preserves the
  multiplier distribution). p_placebo = fraction of shams with lift ≥ winner's. Best-of-3
  correction: winner's lift must also exceed the 95th percentile of max-of-3 draws
  (10,000 bootstrap draws from the 60 sham lifts). Both must pass for an adopt-eligible read.
  A Sharpe-form DSR is not defined for a pass-prob lift; this placebo pair is the multiplicity
  instrument, recorded here before the read.

## Disclosures (carried into RESULTS)

- **EOD clock:** the harness tests the trail at EOD close; venue enforces intraday — bust
  figures are lower bounds (standing lesson). The frozen COMPARISON (policy vs flat, same
  clock) is the pre-registered object; absolute bust levels are not decision-grade here.
- **risk_pct-layer abstraction:** multipliers scale daily P&L linearly; integer-contract
  quantization at micro floors is not modeled (the prereg defines policies at the risk_pct
  layer; same abstraction as the flat sweep it extends).
- **Subject book:** the 2-leg Striker book — deployment-barred; this is a lever measurement
  only (P2 closure §2.2).
