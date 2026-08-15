# Q-BOOKFIT-1 — projection run record

**Run:** 2026-07-20, single session · pre-reg `0fc1e05` (frozen 19:18 ET, before this script existed)
**Driver:** `run_projection.py` · output `projection_results.json` · venv `.venv` (core primitives)
**Verdict: CLOSED — RESOLVED (3/3 forks PASS: `ρ < 1.0` AND `n_eff_risk_delta > 0` @ 0.37%). Canonical closure: [`docs/briefs/closures/Q-BOOKFIT-1-closure-resolved.md`](lab/archive/../../docs/briefs/closures/Q-BOOKFIT-1-closure-resolved.md).**


## Book (frozen Class-S primitives, zero edits)

- Panel: Striker MYM @0.70% + Striker-NAS MNQ @0.37%, sha-pinned CSVs, 1R guards intact
- Span 2020-01-06 → 2026-06-30, 1692 bdays
- **Reconcile: daily $-std $273.28 vs Q-COMPOSE anchor $273 (dev 0.1%, tol ±10%) — PASS**
- Weekly cov eigs {162,742; 214,449} $² · risk PR 1.9631 (precedent 1.96)

## Fork projections (σ_R = 1.0, corr = 0 injection — upper bound)

| Fork | N_b | σ_d | ρ | Δ risk-N_eff | w*(ρ=1) | PASS |
|---|---|---|---|---|---|---|
| F-A ZN auction unwind | 36 | $139.85 | 0.512 | +0.787 | 0.72% | ✔ |
| F-B CL EIA expression | 52 | $168.08 | 0.615 | +0.945 | 0.60% | ✔ |
| F-C carry timing (H=21) | 12 | $80.74 | 0.295 | +0.321 | 1.25% | ✔ |

Sensitivity annex (σ_R ∈ {0.5, 1.0, 1.5}; F-C H ∈ {5, 21, 63}) in `projection_results.json` —
no annex point flips F-A or F-C at σ_R ≤ 1.5; F-B crosses ρ=1.0 only at σ_R ≈ 1.63.

## Phase-1b — JPY micro symbology (discharged)

`M6J.FUT` → 422 on GLBX.MDP3 (does not exist). `MJY.FUT` → MJYU6/MJYZ6 live.
MJYU6 vs 6JU6 closes byte-adjacent (0.006188/0.006194 vs 0.006188/0.006195):
same JPY/USD convention, 1/10 clone, no inversion. Pull estimated + billed $0.00.

## Reproduce

```bash
.venv/Scripts/python.exe lab/archive/q_bookfit_1_2026-07/run_projection.py
# expect: reconcile 273.28 / PR 1.9631 / 3x PASS / RESOLVED
```

Closure: `docs/briefs/closures/Q-BOOKFIT-1-closure-resolved.md`
