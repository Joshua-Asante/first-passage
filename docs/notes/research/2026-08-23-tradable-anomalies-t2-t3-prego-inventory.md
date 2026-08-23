# Tradable-anomalies T2/T3 pre-GO inventory

**Date:** 2026-08-23
**Plans:** [`t2`](../../superpowers/plans/2026-08-23-tradable-anomalies-t2-implementation.md) · [`t3`](../../superpowers/plans/2026-08-23-tradable-anomalies-t3-implementation.md)
**Owner ADR:** [`2026-07-11-tradable-anomalies-statistics-adoption.md`](../../adr/2026-07-11-tradable-anomalies-statistics-adoption.md)
**Authorization:** still PENDING OPERATOR GO. This note is inventory only.

Catalog attestation (this session, before writing): `lab/CATALOG.md` / `docs/briefs/INDEX.md` / `docs/rejected_candidates.md` have no T2/T3 harness slug.

---

## T2 — event-study + cheap detector kit

`rg` over `lab/**/*.py` for `variance_ratio|vr_test|ljungbox|acorr_ljungbox|het_arch|cov_hac|NeweyWest|event.study|Lo.?MacKinlay`: **empty**.

`n_eff_*` in `lab/research_utils/` is participation-ratio / covariance breadth (`breadth.py`, `cov_prekill.py`) — not autocorrelation-corrected `n_eff`.

**Owed after GO:** new helpers (do not duplicate the breadth PR). First family remains constraint/flow. Do not restore `guardian_signal.py`.

**Stop.** No tests, no CLI, no lock decision.

---

## T3 — scanner calibration + admission tooling

Read: [`lab/research_utils/breadth.py`](../../../lab/research_utils/breadth.py) (this session). Cited Q-NEFF-1 closure path `docs/briefs/Q-NEFF-1-closure-resolved-benign.md` is **absent** on this clone (Great Prune / LTM). Computation the T3 goal names as “recover Q-NEFF-1 into ENB” already lives here:

| Present | Absent (T3 still names) |
|---|---|
| `participation_ratio`, `effective_number_of_bets`, `compute_breadth` + dependence/risk deltas | GARCH-fitted null / surrogate calibration |
| CME + historical Pepperstone self-test anchors (owner: this module) | downside-correlation helper |

Prefer extending `breadth.py` after GO (plan). No silent IID-Gaussian swap. No `portfolio_mc` extraction. No new `lab/analysis/` slug from this note.

**Stop.**

---

## T4 (plan Task 1)

Kept in the T4 plan. No new prereg. No `lifecycle_state.json` write. Fill-gated σ-source stays fill-gated.
