# Q-GEOFIT-1 — trailing-DD funding-envelope map — RESULTS

**Verdict:** `AMBIGUOUS-PARAMETERIZATION`
**Brief:** [`docs/briefs/Q-GEOFIT-1-trailing-dd-funding-envelope.md`](lab/archive/../../docs/briefs/Q-GEOFIT-1-trailing-dd-funding-envelope.md) · **Signature:** `SIGNED / FROZEN: 2026-07-25 / JA`
**Gate pre-registration:** [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
**Geometry:** CORRECTED (dd_lock_offset_usd -> 1_000_000.0) · **Tier:** `Tradeify_Select_100K` · **Floor:** bust ≤ 3.0%, pass ≥ 50%
**Sims:** 10,000/seed × 3 seeds · **cells scored:** 0

## Validation anchors (§2) — gate the interpretation of every grid cell

| anchor | measured | published pin | Δ | verdict |
|---|---|---|---|---|
| A1 engine repro 1.00x | 4.74% | 4.74% | 0.003pp | **MATCH** |
| A1 engine repro 0.50x | 0.11% | 0.11% | 0.003pp | **MATCH** |
| A2 profile sufficiency (nearest cell) | 35.89% | 4.74% (real c1) | 31.150pp | **MISS** |
| A2 off-grid exact fit (diagnostic) | 28.38% | 4.74% (real c1) | 23.633pp | miss |

> **The c1 fit falls OUTSIDE the declared grid** on: sigma_d_pct, mu_sigma, z. The nearest-cell row is therefore a *clamped* comparison, not a faithful fit — which is why the off-grid exact row is reported alongside it. Both miss, so the failure is not attributable to clamping. Book positions relative to the declared ranges are in §(iii).

**Anchors hold:** `False`

## Why A2 missed — the family defect

The A2 residual is not a range problem — it survives an **exact** parameter match. Re-drawing the fitted 4-tuple and comparing the moments the family does *not* parameterize shows why:

| moment | real c1 (active days) | synthetic at identical (σ_d, μ/σ, shape, z) |
|---|---|---|
| skewness | **+3.633** | **-0.345** |
| excess kurtosis | 17.92 | 3.85 |
| win fraction | 0.4286 | 0.6143 |
| worst single day | $-744 | $-3,067 |

The real book is a **positively-skewed trend-rider** (skew +3.63): frequent small losses, rare very large wins. Its losses never approach the $3,000 EOD trail. The declared shape axis cannot express that — `student_t4` is **symmetric**, so it returns single days of $-3,067 that exhaust the entire drawdown allowance on their own, and the two-point mixtures have bounded kurtosis by construction and cannot reach 18.

**Load-bearing conclusion — the 4-tuple omits skew.** For a path-dependent fixed-$ trailing barrier, survival is governed by the *loss-side* shape of the daily distribution, which `(σ_d, μ/σ, shape, z)` does not parameterize. Any successor family must carry an explicit skew / loss-tail dimension; matching the first two moments plus a symmetric tail class is demonstrably not sufficient (23.63pp error at exact fit).

## (i) Boundary table — minimum μ/σ that clears, per (σ_d, shape, z)

**NOT EXECUTED.** This is *not* a finding of "nothing clears" — the grid was never scored, so no cell has a bust/pass value at all. The two states are different claims and must not be conflated.

> Validation anchors MISSED (§2), so §6 admits no envelope claim from any cell. Operator elected 2026-07-25 to close on the anchor evidence rather than spend ~8h scoring a surface that cannot be published as an envelope. The 288-cell grid remains declared and unrun; re-running it is a matter of executing this same frozen runner, not of re-deciding the grid.

## (ii) σ_d ceiling — max daily vol fundable at any declared μ/σ

**NOT EXECUTED** — same reason as (i). No σ_d ceiling is claimed in either direction.

## Interpretive readings the brief did not fix (declared at execution)

§2 fixes the axes; these mechanics were chosen by the runner and are recorded so the successor brief can adopt or overturn them deliberately:

- **R1 — μ and σ are ACTIVE-day moments.** §2 defines σ_d as "daily vol on active days", and μ/σ is the ratio of the same distribution's moments. This is what makes §2's own identity hold (0.10 × √252 ≈ 1.59 ≈ "annualized Sharpe ≳ 1.6"). Book positions are published on **both** readings in §(iii) rather than collapsing to one.
- **R2 — active-day draws are affinely standardized** to hit (μ, σ) exactly. The MC block-bootstraps the empirical series, so empirical moments are the effective cell parameters; unstandardized, the sampling error on μ (≈0.03σ at n≈1000) is the size of the whole μ/σ grid spacing (0.025) and would mislabel cells. Affine ⇒ skew/kurtosis preserved.
- **R3 — exact-count z mask** (`floor(N(1−z))` via permutation), so realized z equals declared z instead of carrying binomial noise.
- **R4 — zero-day PLACEMENT is uniform at random, and the brief never declared it.** `build_week_blocks` takes fixed Mon-anchored 5-day slices, so placement determines the within-block active count. A real sparse book *clusters* its idleness (a quiet week is five consecutive zeros), so **temporal clustering of inactivity is a second unparameterized dimension** alongside skew. A successor family must declare a placement law. **Direction unmeasured:** measured directly at frozen sims and the real book's parameters, the placement effect is −0.29pp (clustered − uniform), combined SE ≈1.37pp = **0.21σ, indistinguishable from zero** — see `lab/archive/geofit_skew_probe_2026-07-25/`. An earlier directional claim (that uniform is the higher-bust, anti-clearing, therefore conservative choice) rested on a 2,000-sim proxy at non-c1 parameters and is **withdrawn**; no conservatism may be claimed from R4.

## (iii) Book profile positions relative to the grid (context only — no re-scoring claim)

Declared grid ranges — σ_d ∈ [0.05, 0.45]%, μ/σ ∈ [0.0, 0.15], z ∈ [0.0, 0.4].

| book | reading | σ_d (% acct) | μ/σ | z | inside grid? |
|---|---|---|---|---|---|
| c1 | active-day | 0.5907 ❌ | +0.2162 ❌ | 0.7931 ❌ | **no** |
| c1 | all-day | 0.2733 ✅ | +0.0967 ✅ | 0.7931 ❌ | **no** |
| CFD | active-day | 2.1961 ❌ | +0.2404 ❌ | 0.6111 ❌ | **no** |
| CFD | all-day | 1.3928 ❌ | +0.1474 ✅ | 0.6111 ❌ | **no** |

## §4 accept/reject accounting

**H-GEOFIT is neither accepted nor rejected.** §4's accept/reject rule is conditioned on "**and** the validation anchors hold" — they do not. No count of clearing cells exists, and none may be inferred. The hypothesis returns to the successor brief intact.

> **Brief arithmetic slip recorded (independent of this closure).** §4 states "192 practical / 96 diagnostic", but the declared predicate `μ/σ ≤ 0.10` partitions the 288 declared cells as **240 practical / 48 diagnostic** — the stated counts require a strict `< 0.10`. §2's prose ("a persistent daily edge ratio **above** 0.10 …") settles it in favour of `≤`, which is what the runner executes. This is a defect in the frozen text, not in the run; it does not affect the accept rule (≥1 clears) unless every clearer sits exactly on μ/σ = 0.10. The successor brief should state the predicate and the counts consistently.

**Geometry guard:** not exercised — no grid cells were scored. It was proven live during smoke testing (6/6 workers attested `dd_lock_offset_usd = 1e6` under the process pool), and the anchor runs above were executed under the same corrected patch in-process.

