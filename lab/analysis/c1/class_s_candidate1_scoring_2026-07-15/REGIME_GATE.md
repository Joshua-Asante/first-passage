# Class-S candidate #1 — regime-robustness rider (gate §7(7))

**Status:** `COMPLETE`
**Date:** 2026-07-15

## Citations

- Candidate pre-reg: [`docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md`](../../../docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md) (§6 rider)
- Frozen gate: [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) (§7(7))
- Methodology: [`docs/methodology/regime_robustness_gate.md`](../../../docs/methodology/regime_robustness_gate.md)
- G0–G8 RESULTS: [`RESULTS.md`](RESULTS.md) (`RESOLVED (DISCHARGED)`)
- Driver: [`run_class_s_c1_regime_gate.py`](run_class_s_c1_regime_gate.py)

## Locked posture

- Floor = Part A: bust ≤ 3.0% + P(pass) ≥ 50%
- Geometry = Run-2 on `Tradeify_Select_100K` + `MFFU_Rapid_100K`
- FAIL does **not** overturn mechanical Part A DISCHARGED — standing G8 caveat only
- Historical fixture `ACTIVE_FIRM` = `FXIFY` (FXIFY venue retired; untouched)

## Detail

Part A floors applied per partition (bust≤3.0%, pass≥50%). Discharge tiers=['Tradeify_Select_100K', 'MFFU_Rapid_100K']. DISCHARGED mechanical read stands regardless of rider outcome.

## Verdict

**GATE FAIL (regime-fragile) — standing G8 caveat; does NOT overturn Part A DISCHARGED**

Overall gate pass: `False`

### Tradeify_Select_100K

- Full-panel: bust=2.65% pass=97.34% → PASS
- Bootstrap: pass 5th=89.20% bust 95th=10.37% → FAIL
- H1: bust=4.37% pass=95.47% → FAIL
- H2: bust=1.70% pass=98.30% → PASS
- **Tier gate:** `FAIL`

### MFFU_Rapid_100K

- Full-panel: bust=2.64% pass=97.35% → PASS
- Bootstrap: pass 5th=89.50% bust 95th=10.33% → FAIL
- H1: bust=4.36% pass=95.58% → FAIL
- H2: bust=1.70% pass=98.30% → PASS
- **Tier gate:** `FAIL`

## G8 intake note

DISCHARGED stands (mechanical Part A unchanged). Regime rider **FAIL (regime-fragile)** — admit to G8 with **standing caveat** only; do not re-open Part A. Rail / account / go-live stay gated.

