# MNQTAPE-1 synthetic-signal power check — is N=126 powered to read the Stage-G near-miss?

**Status:** apparatus / power-validity check only — **not** a new candidate test, **not** a CONFIRM
read, **not** a re-run of the frozen Stage-G statistic on real data. No new position/order-flow data
is read in a new way: the only "real" ingredient is the r_pm(s) target series computed by the actual
MNQTAPE-1 Stage-G EXPLORATION execution (below); every predictor used against it in this check is
synthetic. Written 2026-08-23. Does not modify, supersede, or re-open
[`docs/briefs/pre-registration/2026-08-22-mnq-tape-imbalance-prereg.md`](../../../../docs/briefs/pre-registration/2026-08-22-mnq-tape-imbalance-prereg.md)
or its execution artifact.

**Question:** the pre-reg's own §5 power table was computed for the CONFIRM-stage sample size
(Fisher-z, N≈62). Stage-G actually ran at N=126 (double that), against the deliberately loose
`p_emp<0.20` screening gate, not the CONFIRM `p<0.05` bar. At N=126, what is the actual power of
that specific `p_emp<0.20` screen to detect a true effect near the observed magnitude (ρ≈0.075)? Does
the near-miss (`ρ_observed=+0.0751`, `p_emp=0.2054`, missing by 11/2000 permutation draws) read more
like "a real, modest effect that N=126 has limited power to detect" or "no real effect, and this was
a somewhat-lucky-looking draw"?

---

## §1 — What actually happened at Stage-G (real execution artifact, reused not re-derived)

No committed repo artifact for the real Stage-G run exists (`git`-tracked tree has no MNQTAPE-1
directory as of this check — Stage-G execution was scratchpad-only per the pre-reg's own drafting
convention for unopened/pre-registry campaigns). The real execution artifact **does** exist in this
session's own scratchpad history:

- `scratchpad/mnqtape1/mnqtape1_g2.py` — the frozen S1–S13 construction, implemented verbatim
- `scratchpad/mnqtape1/RESULTS_g2.json` — the real result
- `scratchpad/mnqtape1/run.log` — the real run's console log

Real result (`RESULTS_g2.json`, `run_utc: 2026-08-23T04:53:18Z`):

| Field | Value |
|---|---|
| `n_day_files` | 155 |
| `n_sessions_scored_pre_roll` | 128 (27 dropped: `no_rth_trades`) |
| `n_roll_excluded` | 2 (`2026-03-19`, `2026-06-17` — front-month volume-lead change, S13) |
| **`n_usable`** | **126** |
| `rho_observed` | **+0.07513760779902512** |
| `p_emp` | **0.20539730134932535** (410/2000 null draws ≥ observed, one-sided) |
| `gate_c_p_emp_lt_0_20` | **False** — missed by 11 permutation draws (needed ≤399, got 410) |
| `PROMOTE` | **False** |

This check **reused** that real result rather than re-deriving a fresh judgment call about which
sessions are "usable": `scratchpad/mnqtape1_g2_dump_rpm.py` is an unmodified copy of the frozen
harness with one addition — it dumps the final per-session `(date, LTI_norm, r_pm)` arrays actually
used to reach the verdict above. Re-running it against the same cache reproduced
`n_usable=126`, `rho_observed`, `p_emp`, and both roll-excluded dates **exactly** (bit-identical,
`reproduction_check` block in `r_pm_series.json`) before anything downstream was trusted. This
re-run is $0 / cache-reuse-only, matching the EXPLORATION GO already on record (pre-reg §8 item 2) —
no new Databento pull, no CONFIRM byte read.

The 126 `r_pm` values extracted this way — in their real chronological session order, real values,
untouched — are the fixed backdrop for the entire power check below.

---

## §2 — Design (frozen before any result in §3/§4 was inspected)

### 2.1 Why a synthetic-predictor check, and what stays real

The observed `rho_observed=0.0751` came within 11 permutation draws (out of 2000) of clearing a
**deliberately loose** `p<0.20` screening gate, on a construction whose CONFIRM-stage power table
(pre-reg §5) was never computed for the N=126 sample size that actually ran. That gap is exactly an
apparatus question — "is N=126 even capable of distinguishing a real ρ≈0.075–0.20 effect from noise
at this specific p<0.20 threshold?" — answerable **without** touching CONFIRM data or forming any
new belief about `LTI_norm` itself: inject *known*, synthetic predictors against the *real* r_pm
series and measure how often the exact frozen test recovers them.

- **Real, unmodified:** the r_pm(s) target series (§1) — 126 real session values, real order, real
  distribution, real (if any) autocorrelation.
- **Synthetic:** every predictor series tested against it. None claims to *be* `LTI_norm`; each is a
  constructed object with a **known, dialed-in** population-level Spearman correlation to the real
  r_pm series, used purely to measure the test apparatus's detection rate at that correlation.

### 2.2 Synthetic predictor construction (NORTA / Gaussian-copula rank coupling)

For a target "true" Spearman correlation `ρ_S`:

1. Compute the rankit (normal-scores) transform of the fixed real r_pm vector:
   `z_R[i] = Φ⁻¹((rank_i − 0.5) / N)`, average-rank tie handling (N=126; continuous log-returns, no
   ties in practice).
2. Convert `ρ_S` to the generating Pearson parameter via the **exact** bivariate-normal relation
   (Pearson/Greiner): `ρ_S = (6/π)·arcsin(ρ_N/2)` ⟺ `ρ_N = 2·sin(π·ρ_S/6)`.
3. Each synthetic draw: `X = ρ_N·z_R + √(1−ρ_N²)·Z`, with `Z` fresh i.i.d. `N(0,1)` noise per draw.
   `X`'s own marginal is irrelevant — Spearman ρ is invariant to any strictly monotone transform of
   either input, so only `X`'s rank-coupling to `z_R` (≡ to r_pm's own ranks) matters. No further
   transform of `X` into an "`LTI_norm`-shaped" bounded value range is needed or done.
4. **Empirical calibration, not just the asymptotic formula:** a first batch of 2,000 draws at the
   nominal `ρ_N` is used to measure the realized mean sample Spearman ρ against the real r_pm series;
   if it deviates from the target by more than 0.005, `ρ_N` is corrected once via a local-derivative
   step and the draws are regenerated. This removes reliance on the bivariate-normal formula being
   exact at finite N=126 against a *specific, fixed, non-Gaussian* real series rather than a fresh
   Gaussian sample. The realized mean ρ actually achieved is reported alongside the nominal target
   for every level (§3).

"True ρ" in this design means: the expected (generating-process) Spearman correlation between a
freshly drawn synthetic predictor and the fixed real r_pm vector, calibrated so the empirical mean
over many draws matches the stated value. Each individual draw's own realized correlation varies
around that target from finite-N sampling noise — exactly the quantity a power calculation needs to
average over.

### 2.3 The exact frozen test, re-run per draw

Identical to pre-reg S9–S12, applied fresh to every synthetic draw — no shortcut, no re-used
permutation bank across draws:

- **Statistic:** Spearman ρ(X, r_pm)
- **Null:** permutation of the session-date **pairing** between X and r_pm (S10) — each series' own
  within-window order preserved, only the cross-series alignment shuffled
- **M = 2,000** permutations **per draw**, fresh random permutation each time (independent
  `SeedSequence` stream per draw — realistic to how the real single-study procedure would draw its
  own M=2,000 shuffles)
- **p_emp = (1 + #{ρ_null ≥ ρ_obs}) / (M + 1)** — one-sided, predicted-positive, per S12
- **Screening gate scored:** `p_emp < 0.20` — the actual real Stage-G threshold that governed the
  real near-miss decision (pre-reg §7 step 2c), **not** the CONFIRM `p<0.05` bar

### 2.4 Grid and replicate count

| True ρ grid | 0.00 (calibration/null sanity check) · 0.05 · **0.075** (≈observed) · 0.10 · 0.15 · 0.20 · 0.25 · 0.30 · 0.35 |
|---|---|
| Replicates per level | 2,500 (within the task's suggested 2,000–5,000 range) |
| Base seed | 20260823 (this check's own freeze date — deliberately distinct from the pre-reg's frozen `20260822`, never reused across a different apparatus) |
| Empirical power | fraction of the 2,500 replicates at that level with `p_emp < 0.20` |
| Reported alongside | binomial SE of the power estimate; realized mean/median/dispersion of `p_emp`; the calibration diagnostic (nominal vs. realized mean ρ) |

**ρ=0.00 is included as an apparatus-validity check, not a task requirement**: if the permutation
test is exactly calibrated, empirical "power" at ρ_true=0 (the Type-I rate of the p<0.20 screen) must
sit at 0.20 within sampling noise. This is checked **before** trusting the nonzero-ρ power numbers.

### 2.5 What this check does NOT do (forbidden-move discipline carried over from the pre-reg)

- Does not read, estimate, or infer anything about the CONFIRM window (2025-05-01→2025-07-31).
- Does not treat any result below as a re-measurement of `LTI_norm`'s own correlation with r_pm —
  that number is fixed at the real, already-computed 0.0751 and is never re-estimated here.
- Does not retune the ≥10-contract threshold, the 09:30/12:00/16:00 ET boundaries, the real Stage-G
  permutation seed, or its M — none of those objects are touched; this check runs an entirely
  separate synthetic-predictor experiment against the *output* (r_pm) of that frozen construction.
- Does not license promotion, demotion, or any change to `PROMOTE=False`. Stage-G's own verdict
  stands; this document answers a different question (how much should that verdict move anyone's
  belief).

---

## §3 — Empirical power curve

*(filled in from `power_check_results.json`, produced by `power_check.py` against the real,
reproduction-verified `r_pm_series.json` from §1 — 2,500 replicates/level, M=2,000 permutations/draw,
base seed 20260823)*

**Real r_pm(s) backdrop, descriptive stats (N=126):**

| Stat | Value |
|---|---|
| mean | +0.000250 |
| std (sample) | 0.006145 |
| skewness | +0.094 (near-symmetric) |
| excess kurtosis | +1.836 (fatter-than-normal tails — a Gaussian-shape assumption on r_pm would have understated tail risk; this is exactly why the check draws its "true" backdrop from the real series rather than assuming Normality) |
| lag-1 autocorrelation (real session order) | −0.106 (mild negative day-to-day dependence, not zero) |

**Apparatus-validity check (ρ_true = 0):** empirical Type-I rate at the p<0.20 screen = **0.1936 (SE 0.0079)** —
statistically indistinguishable from the nominal 0.20 (z ≈ 0.81, well inside normal sampling
variation). The permutation test is correctly calibrated at N=126 against this real, non-Gaussian,
mildly autocorrelated r_pm backdrop — the power numbers below can be trusted.

**Power table** (2,500 replicates/level, M=2,000 fresh permutations/replicate, base seed 20260823):

| True ρ (target) | ρ_N used (generating param) | Realized mean ρ (calibration check) | Empirical power: P(p_emp<0.20) | SE | Median p_emp |
|---|---|---|---|---|---|
| 0.00 (sanity) | 0.0000 | −0.0019 | 0.1936 | 0.0079 | 0.519 |
| 0.05 | 0.0524 | 0.0506 | 0.3864 | 0.0097 | 0.285 |
| **0.075 (≈observed)** | 0.0785 | 0.0741 | **0.4992** | 0.0100 | **0.201** |
| 0.10 | 0.1047 | 0.0999 | 0.6092 | 0.0098 | 0.131 |
| 0.15 | 0.1569 | 0.1513 | 0.8100 | 0.0078 | 0.041 |
| 0.20 (pre-reg CONFIRM floor) | 0.2091 | 0.1995 | 0.9252 | 0.0053 | 0.012 |
| 0.25 | 0.2611 | 0.2484 | 0.9828 | 0.0026 | 0.003 |
| 0.30 | 0.3129 | 0.3006 | 0.9980 | 0.0009 | 0.001 |
| 0.35 | 0.3645 | 0.3491 | 0.9992 | 0.0006 | 0.0005 |

Every "realized mean ρ" sits within ~0.005 of its target (worst case: target 0.05 → realized 0.0506;
target 0.35 → realized 0.3491) — the empirical calibration held without needing the correction step
to fire at more than the first-decimal level, confirming the NORTA construction is behaving as
designed against this specific, real, non-Gaussian r_pm vector.

For reference, the pre-reg's own §5 table (Fisher-z, N≈62, testing the CONFIRM `p<0.05` bar — a
**different N and a different, much stricter gate** than this table):

| True ρ | Power (N≈62, p<0.05) |
|---|---|
| 0.20 | ≈0.47 |
| 0.25 | ≈0.62 |
| 0.30 | ≈0.77 |
| 0.35 | ≈0.88 |

---

## §4 — Interpretation (honest, quantitative)

### 4.1 The direct answer

**At the observed effect size (ρ≈0.075), the empirical power of the real Stage-G screen at N=126 is
49.9% (SE 1.0pp) — essentially a coin flip.** If the true `LTI_norm`→r_pm relationship really sits at
the magnitude actually observed, the deliberately loose `p<0.20` screen would clear only about half
the time at this sample size. **Missing it, as actually happened, is not meaningfully surprising under
that hypothesis** — it is not evidence of "no effect." But by the identical logic it is **not** evidence
*for* a real effect either: a coin flip that lands tails is not evidence the coin is fair *or* biased.
The near-miss, taken alone, cannot discriminate between "a real ρ≈0.075 effect" and "nothing" at this N
— that IS the power problem the pre-reg's own §5 table gestured at (for a different N and a different,
stricter gate) but never quantified for the gate that actually ran.

### 4.2 A sharper comparison: does the *specific* near-miss favor one hypothesis over the other?

Power alone (a forward-looking, "how often would this design succeed" number) doesn't fully answer
"given the *one* result we actually got, which hypothesis does it favor." Two more precise looks at
that question, both computed from the same simulation, both modest in what they claim:

**(a) Where the near-miss typically lands under each hypothesis.** The *median* simulated `p_emp`
under the pure-null draws (ρ_true=0) is **0.519** — a typical null miss lands nowhere near the 0.20
boundary. The *median* simulated `p_emp` under a ρ_true=0.075 generating process is **0.201** —
almost exactly the observed **0.2054**. The real result landed exactly where a *typical* draw from
the "modest real effect" hypothesis would land, and nowhere near where a *typical* draw from the
"nothing" hypothesis would land.

**(b) A likelihood-ratio read at the exact observed value.** Approximating each hypothesis's sampling
distribution of the realized correlation as Gaussian (using this simulation's own measured mean/SD,
not an assumed textbook one — realized mean/SD of −0.0019/0.0873 under the null and +0.0741/0.0879
under ρ_true=0.075), the relative density at the actual observed `rho_observed=0.07514` is:

```
f(0.07514 | true ρ=0.075) / f(0.07514 | true ρ=0)  ≈  1.46
```

**A likelihood ratio of ~1.5:1 is real, directionally consistent, and weak.** It says the observed
value is about 1.5× more probable under "a modest ρ≈0.075 effect" than under "no effect" — a small
lean, not a case. By any conventional evidence scale (e.g. Jeffreys'), a Bayes factor under 3 is
"barely worth mentioning" on its own. **This check does not resolve the near-miss; it bounds how much
it should move anyone's belief, and the honest bound is "not much."**

### 4.3 The near-miss is more informative about *magnitude* than about *existence*

The power curve is far from flat: power is 92.5% at ρ=0.20 (the pre-reg's own CONFIRM floor,
`|ρ_confirm|≥0.20`) and 99.8% at ρ=0.30. **If the true effect really were as large as the CONFIRM
floor, this specific Stage-G screen would have cleared comfortably (~93% of the time) — landing in a
razor-thin miss instead (as actually happened) is itself a ~7.5%-probability outcome under that
hypothesis.** That disfavors "the true effect is as large as 0.20" relative to "the true effect, if
real at all, is closer to the observed ~0.05–0.15 range" — where a near-miss at this specific loose
gate is the *typical*, unremarkable outcome (power 39–81% across that band, median `p_emp` clustering
right around the 0.20 boundary).

This has a direct, sobering implication for the CONFIRM decision this pre-reg would eventually need
to make: **the pre-reg's own §5 power table already discloses only ≈47% power to confirm an effect
sitting exactly at its own `|ρ|≥0.20` floor, at N≈62.** This check's own finding — that a near-miss of
this specific shape is itself mild evidence *against* the effect being that large — means CONFIRM
would be trying to detect, at relatively low power, an effect size that this apparatus check has
independent (weak) reason to think is smaller than the floor CONFIRM requires. Two power problems
compound rather than offset.

### 4.4 Bottom line

Read honestly and quantitatively: the Stage-G near-miss is **weakly more consistent with "a real,
modest effect near the observed magnitude, underpowered by a loose N=126 screen" than with "no effect
and a lucky-looking draw"** — the median-outcome match (§4.2a) and the ~1.5:1 likelihood lean (§4.2b)
both point the same direction, however faintly. It is **not** strong enough evidence to treat the
candidate as anything other than what Stage-G already called it: a miss, `PROMOTE=False`, no CONFIRM
spend licensed by this document (§9 forbidden moves, carried forward unchanged). What this check adds
is a number where the pre-reg had none: **at the real N and the real gate, ~50% power at the observed
effect size means the near-miss is close to uninformative on its own, and what modest signal it does
carry points toward a small effect (if any), not one as large as CONFIRM's own 0.20 floor** — which,
if anyone eventually asks for the CONFIRM spend GO (pre-reg §8 item 3), is a materially different risk
picture than "a good candidate that barely missed a fluke."

---

## §5 — Reproducibility

| Artifact | Location |
|---|---|
| Real Stage-G execution (unmodified, untouched by this check) | this session's own scratchpad (`mnqtape1/{mnqtape1_g2.py,RESULTS_g2.json,run.log}`) — genuinely scratchpad-only per the pre-reg's own stated convention ("one-off Stage-G execution artifact... not a repo commit"); not copied into the repo here, since registry admission is a separate, reviewable step this check does not take |
| Reproduction + r_pm dump (separate copy of the harness, not an edit of the original; reproduced `n_usable=126`, `rho_observed`, `p_emp`, both roll-excluded dates bit-identically before anything downstream was trusted — see `reproduction_check` inside `r_pm_series.json`) | [`mnqtape1_g2_dump_rpm.py`](./mnqtape1_g2_dump_rpm.py) → [`r_pm_series.json`](./r_pm_series.json), console log [`rerun_log.txt`](./rerun_log.txt) |
| Power-check simulation (this check's actual deliverable — design frozen in §2 before `power_check_results.json` was inspected) | [`power_check.py`](./power_check.py) → [`power_check_results.json`](./power_check_results.json), console log [`power_check_log.txt`](./power_check_log.txt) |
| This document | `lab/analysis/c1/mnqtape1_power_check_2026-08-23/RESULTS.md` |

To re-run end-to-end (cache-reuse only, $0, no new Databento pull): `python mnqtape1_g2_dump_rpm.py --workers 6`
(requires the EXPLORATION cache at `~/.databento_cache/q_ofchan_1_exploration_tbbo/`, aborts with a
loud reproduction-check failure if it does not bit-match the real Stage-G artifact) followed by
`python power_check.py`.

Seeds: real Stage-G permutation seed `20260822` (untouched, reused only for the reproduction check);
this power check's own base seed `20260822` + 1 = `20260823`, `SeedSequence`-spawned per level and
per replicate (synthetic-predictor generation and permutation-null draws use independent streams).

**Forbidden-move / scope discipline carried forward:** no CONFIRM byte read; no retuning of any S2–S13
frozen element; no promotion/demotion decision implied; original pre-registration and its execution
artifacts are unmodified by this check.
