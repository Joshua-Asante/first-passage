# RESULTS — mc_mdd_closed_form_2026-08

**Disposition:** ACTIVE — Magdon-Ismail (2004) closed-form G_D vs `simulate_path` absolute-$ trailing bust rates
**Status:** MEASURED — validation only; not calibration  
**Date:** 2026-08-13  
**Notice anchor:** [`docs/notes/notice/N-2026-08-13-external-eval-population-data.md`](../../../../docs/notes/notice/N-2026-08-13-external-eval-population-data.md) §4  
**Paper:** Magdon-Ismail, Atiya, Pratap & Abu-Mostafa (2004), JAP 41:147–161  
**Runner / raw:** [`run_validation.py`](run_validation.py) · [`validation_raw.json`](validation_raw.json)

---

## Appendix B

`check_appendix_b` (asymptotic small/large vs transcribed fixtures; `include_integral=False`) — all checks PASS for `qp` and `qn`. See `validation_raw.json` → `appendix_b`.

---

## G_D vs `simulate_path` grid (20k paths each)

| case | p_mc | G_D | \|err\| | verdict |
|---|---:|---:|---:|---|
| driftless_A | 0.0966 | 0.0894 | 0.0072 | AGREE |
| driftless_B | 0.2658 | 0.2656 | 0.0002 | AGREE |
| pos_drift_A | 0.3422 | 0.3312 | 0.0110 | AGREE |
| pos_drift_B | 0.0379 | 0.0371 | 0.0008 | AGREE |

**mean_signed_err** = +0.0048 · **equiv_gate** = PASS

Tolerance: `max(0.02, 3×SE)` per cell; all four cells agree.

---

## MC bias characterisation

All signed errors are **positive** (MC bust rate slightly above continuous \(G_D\)). Likely contributors, in order:

1. **Six-decimal floor test** — `round((equity_test - floor) / S0, 6) <= 0` in `simulate_path` makes the effective absorbing barrier about **h − $0.05** on \(S_0 = \$100{,}000\) (one rounding quantum in pct-of-starting-equity space).
2. **EOD-only barrier** — `intraday_low=None`; no intraday excursion test (legacy anchor geometry).
3. **Peak update order** — high-water mark ratchets **after** the bust check on each day.
4. **Discrete BM steps vs diffusion** — Atiya & Magdon-Ismail (2018) bound discrete-time drawdown effects; here \(\sigma\sqrt{\Delta t}/h \approx 0.01\)–0.016, so discretisation is **not** the dominant gap.

---

## Trail → static equivalence (gated)

Gate passed → [`trail_static_equiv.csv`](trail_static_equiv.csv) written (12 rows).

**Assumptions:** continuous BM closed forms only (\(G_{\bar D}\), \(G_H\)); **not** a gate input and not a production calibration artifact.

---

## What this does **not** license

- No threshold, gate, or `core/` edits.
- Population pass rates from N-2026-08-13 §2–§3 are a different estimand.
- Equivalence mapping is exploratory lab output until separately pre-registered.

---

## Realistic-granularity extension: EOD-only vs. intraday-honest at real trading-day scale

**Added 2026-08-13 (same-day follow-on).** The grid above tests `simulate_path` against
\(G_D\) in the **fine-discretization limit** — `n_steps` = 2000-5000 substeps standing in
for the horizon, i.e. it validates the engine's barrier arithmetic *converges to
continuous theory as step count grows* (an engine-fidelity check; it passes). It does
**not** test the granularity the repo actually reports bust rates at: one barrier test
per real **business day**, horizon ~20-60 days — nor does it exercise `intraday_low`
(§ "MC bias characterisation" above lists `intraday_low=None` as an untested,
unranked candidate contributor to the small measured bias).

**Runner:** [`intraday_realistic_grid.py`](intraday_realistic_grid.py) · **Raw:**
[`intraday_realistic_grid_raw.json`](intraday_realistic_grid_raw.json)

Method: `simulate_path` run three ways per cell (40,000 paths, Tradeify Select 100K's
real `h=$3,000` trail, daily Gaussian P&L at (μ,σ) in real dollars) — (a) EOD-only, no
`intraday_low`, the repo's current default; (b) `intraday_low` fed an **exact** sample
of each day's continuous-time minimum via the Brownian-bridge reflection formula
(given a day's realized P&L \(x\), diffusion \(\sigma\), the minimum over that day has
\(P(\min \le y) = e^{-2y(y-x)/\sigma^2}\) for \(y \le \min(0,x)\), independent of drift
— inverted for exact sampling, not a fine-grid approximation); (c) this study's own
`g_d(h,\mu,\sigma,T)` as the pure-continuous-peak theoretical reference.

| Case | Horizon | P(EOD) | P(continuous-MC) | \(G_D\) (theory) | EOD ÷ continuous-MC |
|---|---:|---:|---:|---:|---:|
| No edge | 20d | 11.30% | 14.61% | 18.55% | 77.4% |
| No edge | 40d | 34.92% | 40.64% | 46.90% | 85.9% |
| Modest edge ($40/day on $400/day σ) | 20d | 5.44% | 7.35% | 9.98% | 74.0% |
| Modest edge | 40d | 18.45% | 22.93% | 27.87% | 80.5% |
| Modest edge | 60d | 29.53% | 35.36% | 42.49% | 83.5% |

All three tiers land in the expected order `P(EOD) < P(continuous-MC) < G_D` in every
cell (a correctness check in itself — an EOD-anchored floor tested continuously must
expose *more* risk than testing only at EOD, and a fully continuous peak more still).

**Finding: EOD ÷ continuous-MC = 74.0% to 85.9%.** `simulate_path`'s `intraday_low`
mechanism, tested against an *exact* continuous signal rather than left untested, is
doing the right thing — it lands strictly between the EOD-only and pure-continuous
tiers, as it should, given the floor still only ratchets at EOD (`peak` updates once
per day) while breach is tested continuously — exactly Tradeify's own documented rule
(`core/firm_rules.py` L299-303, `core/mc/simulation.py` L78-84). **The repo's current
EOD-only bust-rate convention captures only three-quarters to five-sixths of the bust
probability Tradeify's own rule implies** — every EOD-only figure needs roughly a
**1.16-1.35×** correction to approximate the honest number, worse at shorter horizons
(fewer EOD samples relative to the continuous path means a larger fraction of what
decides the outcome happens between samples). `G_D` (pure continuous peak, no
EOD-anchoring at all) is a useful independent ceiling, confirming direction and rough
magnitude, but is **not** itself Tradeify's rule and should not be quoted as an
intraday-honest bust figure.

This is the first analytic (not another empirical MC re-run) answer to the "every bust
figure is a LOWER BOUND" claim named in `core/firm_rules.py` and the still-open
[W1 ADR](../../../../docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md) — it
does not close that ADR (its four named decisions-of-record on the real c1 book are
untouched), but supplies a validated tool and a first-cut magnitude estimate.

### What this extension does NOT establish

1. Gaussian synthetic P&L only, same as the grid above — says nothing about a real
   candidate's realized skew (Q-GEOFIT-1 measured the withdrawn c1 book at skew
   +3.633; that gap is untouched by this extension).
2. Five cells at one barrier ($3,000) and one starting equity ($100K) — not a fitted
   general correction factor. The horizon-dependence direction (worse at short
   horizons) is consistent with discretization-bias theory generally but not fit here.
3. i.i.d. daily draws, no serial correlation — same optimistic-bias caveat this
   study's own grid section and the repo's sibling `eval_inverse_requirements`/
   `tradeify_seed_target_spec` studies already carry.

### Reproduce

```bash
cd lab/analysis/mc/mc_mdd_closed_form_2026-08
python intraday_realistic_grid.py   # ~4 min, n=40,000/cell
```

Stdlib + numpy + scipy only (imports this directory's own `closed_form.g_d` and
`harness.firm_kwargs_absolute_trail` — no new closed-form implementation).
