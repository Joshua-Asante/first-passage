# Q-VOLREGIME-1 — Packet C1: pilot acceptance bands (frozen before simulation)

**Status:** `FROZEN, NOT YET EXECUTED` — this document declares C1's own required bands, counts, and
disposition rules. **No simulation has been run.** No real L5 statistic, on either instrument, has
been inspected. Nothing here executes anything; it exists so C2–C5 (the actual pilot studies) have
nothing left to decide once real data is touched.

⚠ **A right-sizing amendment is PROPOSED and awaiting operator ratification — see §7.** It changes
the inner replicate count `B` for the pilot studies only, and names one implementation identity;
it changes no band, no cell, no `N_outer`, no gate, and no disposition rule in §§1–5, which stand
exactly as frozen. Until §7 is ratified, §§1–5 as written remain the controlling spec.

**Operator GO:** received for Packet C1 specifically — 2026-08-31. Per the plan doc's own gate
table, this GO authorizes *freezing* the pilot's own acceptance criteria; it does **not** authorize
running C2 (null-size study), C3 (power study), or C4 (adequacy checks) — those each still need
their own execution to actually happen, and Packet D (real execution) needs a further, separate
GO plus a K declaration on top of a passing C5.

**Entry gate satisfied:** Packet B (B1–B5) is complete —
[`volregime_l5_design_2026-08-31/DESIGN.md`](../volregime_l5_design_2026-08-31/DESIGN.md), frozen
2026-08-31, five Codex review rounds, the fifth returning no findings.

---

## 1. Replicate counts and seeds

**Two distinct replicate counts, for two distinct purposes — not one number reused.**

- **`B = 4000`** — the frozen inner null-replicate count for the real L5 attribution statistic
  itself (`DESIGN.md` §4.1), unchanged. This is what Packet D would eventually use, and what C3's
  own power study also uses per synthetic panel (below) — the pilot must exercise the exact
  machinery Packet D would run, not a scaled-down version of it, or the pilot proves nothing about
  the real thing.
- **`N_outer = 100`** (new, frozen here) — the number of independent synthetic null panels
  generated per instrument, per comparison, for C2's own null-size study. Each synthetic panel is
  scored by the **full** `B=4000`-replicate pipeline (`DESIGN.md` §4.2–§4.4), so C2 alone requires
  `100 × 4000 = 400,000` full-pipeline replicate-equivalent computations per (instrument,
  comparison) — a disclosed, deliberate computational-budget choice, not a number chosen for
  convenience without consequence: under a true 5% Type-I rate, 100 outer draws gives a binomial
  standard error of `sqrt(0.05 × 0.95 / 100) ≈ 2.2 percentage points`, which resolves a true rate
  of 5% from `Q-RANGEXFER-1`'s own measured failure magnitude (5% → 25%) with high confidence, but
  is **not** sized to detect a smaller, subtler miscalibration (e.g. 5% → 8%) — a limitation
  disclosed here, not hidden, and the reason C4's own absolute-adequacy checks exist as an
  independent line of defense rather than relying on C2's own power alone.
- **Seeds — frozen per instrument, per comparison, per study, not drawn ad hoc at execution
  time:** `seed_base = 20260831` (matching this design's own freeze date, following
  `c3_stratified_rerun.py`'s own precedent of a dated seed rather than an arbitrary one). Each of
  the four (instrument × comparison) cells uses `seed_base` offset by a fixed, disclosed integer
  (MNQ Comparison 1: `+0`; MNQ Comparison 2: `+1`; MYM Comparison 1: `+2`; MYM Comparison 2: `+3`),
  so every cell's own random draws are reproducible and distinct, and no cell's own seed is chosen
  after seeing that cell's own results.

## 2. Empirical Type-I acceptance band (C2's own pass rule)

**Frozen method, not a single point estimate, and not a number picked after seeing the count.**
Across `N_outer = 100` synthetic null panels (§1) for a given (instrument, comparison) cell, count
the number of panels whose own `p_upper ≤ 0.05`. This observed count must fall inside the **exact
two-sided 95% Clopper–Pearson confidence interval for `Binomial(100, 0.05)`** — computed exactly,
not via a normal approximation (`n=100, p=0.05` is small enough that a normal approximation can
misstate the tail) — for the cell to individually clear. **All four cells** (MNQ × Comparison 1,
MNQ × Comparison 2, MYM × Comparison 1, MYM × Comparison 2) must clear independently; one cell's
own pass does not carry another's, matching this design's own per-instrument, per-comparison
independence throughout (`DESIGN.md` §2).

## 3. Minimum useful power at a planted effect (C3's own pass rule)

**Planted-effect magnitude — calibrated to each instrument's own already-observed minimum
stratified lift, not a shared or invented number.** Per the parent brief's own H-VOLREGIME text:
MNQ's own minimum within-stratum lift is **+22.3pp** (the low-range stratum, the smaller of its
own two strata); MYM's own is **+16.5pp** (the block-bootstrap mean minimum stratified lift). Each
instrument's own power study plants an incremental probability shift **no larger than its own
already-observed minimum** — using each instrument's own real number, not the smaller of the two
applied to both, consistent with this design's own no-pooling principle.

- **Primary planted effect:** exactly each instrument's own minimum stratified lift above (MNQ
  +22.3pp, MYM +16.5pp).
- **Secondary, stricter planted effect (disclosed as an additional check, not a required
  minimum):** half of the primary — MNQ +11.15pp, MYM +8.25pp — to see whether power degrades
  gracefully or falls off a cliff.
- **Minimum useful power: 80%** at the primary planted effect, per (instrument, comparison) cell,
  measured across `N_outer = 100` synthetic planted-effect panels (same count and seeding
  convention as §1, offset by a further fixed, disclosed integer per cell so planted-effect draws
  never reuse the null-study's own seeds) each scored by the full `B=4000` pipeline: the fraction
  of these 100 panels whose own `p_upper ≤ 0.05` must be `≥ 0.80`. No minimum power requirement is
  frozen for the secondary (half-magnitude) effect — it is diagnostic, reported but not gating.

## 4. Absolute calibration / adequacy diagnostics and pass rules (C4)

**Two layers, not one — `DESIGN.md` §4.6's own confound-preservation diagnostics, plus C4's own,
broader model-calibration battery this document adds.**

- **Layer 1 (already frozen, unchanged):** `DESIGN.md` §4.6's own per-replicate adequacy gate
  (same-bar Spearman correlation, conditional volume distribution across range quantiles, volume
  and range autocorrelation, cross-correlation at lags −4 through +4, time-of-day distribution),
  each checked per replicate against a 90% day-blocked bootstrap CI, requiring ≥95% of sampled
  replicates to individually clear. This layer checks whether the *null* is well-constructed; it
  does not check whether the *fitted model* is well-calibrated, which is C4's own distinct concern.
- **Layer 2 (new, frozen here) — model calibration, stratified.** For each of `baseline_1` and
  `augmented_1`'s own real-data (not null-replicate) OOS predictions, pooled across folds
  (`DESIGN.md` §4.1): bin predicted probabilities into deciles, and within each of the following
  strata independently — time-of-day (four buckets: the four calendar quarters of the ToD cycle,
  a coarser split than the raw slot, frozen now to avoid a sparse-bin problem at 96 slots), own-range
  stratum (`bias_range ∈ {0,1}`), calendar year, chronological half (matching L3's own midpoint
  split, `volregime_l3_2026-08-31/RESULTS.md`), and instrument — compute the maximum absolute gap
  between each decile bin's own mean predicted probability and its own observed outcome rate.
  **Pass rule: the maximum absolute calibration gap, across every decile bin within every stratum
  independently, must not exceed 5 percentage points.** A stratum with fewer than 30 scored bars in
  a given decile bin is excluded from that specific check and disclosed as excluded, not silently
  passed or failed. This is an **absolute** criterion (§ per the plan doc's own C4 language,
  "being relatively best among candidate models is insufficient") — `augmented_1` failing this gate
  is a design failure regardless of how it compares to `baseline_1`.

## 5. Bounded escalation and terminal failure disposition (C5's own gate, operationalized)

**Exactly one permitted escalation, narrowly scoped — not an open-ended retry.** If, and only if,
§2's own Type-I acceptance band is the gate that fails (power, §3, or calibration, §4, failing has
no escalation — see below): the **sole** permitted adjustment is widening `DESIGN.md` §3.4's own
frozen embargo from 4 to **8 trading days**, then re-running C2 (§2) **once** with that single
change and no other. If the widened-embargo re-run also fails §2's own band, or if the *original*
run failed §3 (power) or §4 (calibration) in the first place, the pilot **terminates immediately** —
no further escalation, no parameter search, no repeated tuning against the observed pilot result
(this design's own D8: "a pilot failure is a designed outcome").

**Terminal disposition on failure:** the affected (instrument, comparison) cell is marked
`AMBIGUOUS-PARKED`, per the plan doc's own C5 disposition table. This is recorded as a **design
failure**, not a negative empirical verdict on volume itself — the parent brief's own H-VOLREGIME
hypothesis is not falsified by a pilot failure; it remains open, with the machinery that would have
tested it disclosed as not yet trustworthy enough to run. No retune of §§1–4 above is permitted
after seeing which cell failed, beyond the one named embargo-widening escalation.

**Terminal disposition on success:** if all four (instrument × comparison) cells clear §§2–4, C5's
own joint pilot gate passes, and a frozen L5 execution packet is produced — Packet D still requires
its own separate operator GO and K declaration before the real, one-shot L5 statistic is ever
computed.

---

## 6. PROPOSED right-sizing amendment (2026-09-01) — awaiting operator ratification

**Status:** `PROPOSED`. Authored before any pilot execution and before any outcome-bearing byte, on
either instrument, was read — this is a prospective cost amendment, not a response to a result.
The original §§1–5 freeze carried its own operator GO; this amendment therefore needs its own
ratification before it governs anything.

**Motivation — the plan doc's own R4, discharged with a measurement rather than an estimate.**
`docs/superpowers/plans/2026-09-01-q-volregime-bounded-translation-campaign.md` §2 R4 requires a
synthetic timing dry-run and a published CPU-hour figure before a cost GO. Measured on the
operator's own machine (8 cores), on a synthetic panel matched to the real frame shape (139,605
rows, 12 baseline features, 10 expanding folds), executing the full §4.2–§4.4 replicate recipe —
global OLS residualization, global rotation, causal pseudo-volume reconstruction, then fold-local
`baseline_1`/`augmented_1` fits and OOS scoring:

- **1.002 s per replicate** with `baseline_1` refit inside every replicate;
- **0.689 s per replicate** with `baseline_1` cached per outer panel (Change 1 below).

At the frozen sizing that is **1,336 core-hours** (≈56 core-days) across C2, C3-primary and
C3-half — about 9 days of pinned CPU on the operator's laptop. No synthetic or real pilot data was
scored; the dry-run computes a wall-clock number and nothing else.

### Change 1 — cache `baseline_1` per outer panel (an identity, not a design change)

`baseline_1` contains **no volume feature** (§3.3 of `DESIGN.md`). Under a null replicate, only the
rotation of the volume residual changes; the outcome labels, the fold boundaries, and every
`baseline_1` feature are untouched. Its fitted coefficients are therefore *identical* across all
`B` replicates within a given outer panel, and refitting it `B` times recomputes the same numbers.
Caching it per (cell, outer panel) is output-preserving by construction, not an approximation.

This does **not** weaken §4.4's "every other object is refit fresh for every replicate" rule, whose
purpose is to forbid *nuisance-parameter* shortcuts of the kind that broke `Q-RANGEXFER-1`. The
residualization regression, the causal `pseudo_tod_threshold` reconstruction, and `augmented_1`
itself all remain refit per replicate, unchanged. **Required disclosure:** a P2 test must assert
that the cached `baseline_1` coefficients and OOS predictions are bitwise equal to a refit
`baseline_1` on at least one replicate per cell; if that test fails, the cache is abandoned and the
full-refit cost is paid.

Measured saving: **31%**.

### Change 2 — `B = 999` for the pilot studies (C2, C3) only; Packet D keeps `B = 4000`

§1's `B = 4000` is retained verbatim **for the real L5 statistic** (Packet D) and for the observed
run. For the pilot's own inner loops, `B` drops to 999.

**Why this costs no calibration sensitivity.** A Monte-Carlo permutation p-value
`p̂ = (1 + #{T_j ≥ T_obs}) / (B + 1)` is exactly size-calibrated for *any* `B` when exchangeability
holds. C2 measures the rate at which `p̂ ≤ 0.05` under a constructed null; that rate is not a
function of `B`. And when exchangeability is *broken* — which is precisely what C2 exists to
detect, and precisely how `Q-RANGEXFER-1` failed — the breakage manifests as `T_obs` sitting
systematically high in the replicate distribution, a location property that does not depend on `B`
either. Reducing `B` changes the *granularity* of achievable p-values (smallest attainable p moves
from 1/4001 to 1/1000, both far below `alpha = 0.05`), not the α=0.05 decision the study scores.

**Disclosed limit of this argument:** it holds for a failure that shifts the bulk or the 5th
percentile of the replicate distribution. A pathology confined to the extreme tail (below p≈0.001)
would be resolved less finely at `B = 999`. C2's gate is fixed at `alpha = 0.05`, so that region is
not where its verdict is decided — but the caveat is stated rather than assumed away.

**Power (C3) is the one place `B` can genuinely bite**, since a smaller `B` slightly coarsens
p-values under a true effect. At the planted magnitudes (§3: MNQ +22.3pp, MYM +16.5pp) p-values are
expected far into the tail, where the coarsening is immaterial. **Pre-declared bounded escalation,
frozen here rather than decided later:** if a C3-primary cell's observed power lands in
**[0.70, 0.90]** — i.e. near enough to the 80% gate that `B` granularity could plausibly matter —
that cell alone is re-run once at `B = 4000`, and the re-run's result governs. Power landing
outside that window is decided at `B = 999` with no re-run. This escalation is additional to, and
independent of, §5's own embargo-widening escalation, which is unchanged.

Measured saving: **75%**.

### Explicitly NOT changed

- **`N_outer = 100` stands.** An earlier draft of this amendment proposed cutting it to 40. The
  exact Clopper–Pearson detection arithmetic refutes that, and the rejected option is recorded here
  rather than dropped silently. Probability the C2 check flags a cell whose true Type-I rate is:

  | `N_outer` | accept band | true 10% | true 15% | true 25% |
  |---:|---|---:|---:|---:|
  | **100 (frozen, retained)** | [1, 10] | 41.7% | 90.1% | 100% |
  | 60 | [0, 7] | 24.8% | 69.5% | 99.1% |
  | 40 (rejected) | [0, 5] | 20.6% | 56.7% | 95.7% |

  `N_outer` is the *only* parameter that buys detection sensitivity, and §1 already discloses that
  n=100 cannot resolve a subtle miscalibration; the table shows it is in fact effectively blind
  below ~15%. Cutting to 40 would move that blind spot up against 25% — the exact magnitude
  `Q-RANGEXFER-1` actually exhibited, i.e. it would degrade the one thing the study exists to catch.
  After Changes 1–2, `N_outer` is no longer a material cost driver, so there is nothing to buy by
  cutting it.
- **The §3 half-magnitude power cell is retained**, though §3 itself marks it non-gating and it
  would be the easiest thing to delete. After Changes 1–2 it costs ~76 core-hours; it is kept as
  the disclosed graceful-degradation diagnostic it was frozen to be.
- Every band, cell, seed convention, gate, escalation and terminal disposition in §§1–5 is
  unchanged, as is `DESIGN.md` in full. Comparison 2 remains scheduled in parallel; whether it
  gates is reconciliation item R1's question, not this amendment's.

### Resulting budget

| Study | Frozen | Proposed | |
|---|---:|---:|---|
| C2 null-size | 445 core-h | 76 core-h | `N_outer` 100, `B` 999, cached |
| C3 power, primary | 445 core-h | 76 core-h | as above |
| C3 power, half-effect (non-gating) | 445 core-h | 76 core-h | as above |
| **Total** | **1,336 core-h** | **229 core-h** | **83% cut** |
| Escalation reserve (C3-primary re-run at `B`=4000) | — | +306 core-h | only if power ∈ [0.70, 0.90] |

Wall clock: ~1.6 days pinned on the operator's laptop at 6 usable cores, or ~3.6 hours on a
64-core box. C4's own diagnostics are not in this budget and remain to be costed separately.

### Reproducing every number in this section

Both scripts are synthetic-only: they read no vendor panel, score no pilot or observed statistic,
and touch nothing under `core/data/`. Numbers above are their output, not estimates.

```bash
# per-replicate wall clock (regenerates 1.002 s / 0.689 s on an 8-core machine)
python lab/analysis/_inbox/volregime_l5_pilot_2026-08-31/bench_replicate_timing.py

# Clopper-Pearson bands, detection power, and the core-hour budget table
python lab/analysis/_inbox/volregime_l5_pilot_2026-08-31/rightsize_arithmetic.py
```

Timings are hardware-relative; re-run `bench_replicate_timing.py` on whatever machine actually
executes the pilot before quoting a wall-clock or dollar figure for it.

### Ratification conditions

This amendment is legitimate only because it is prospective. If any pilot or observed L5 result has
been inspected on either instrument before ratification, it must be withdrawn rather than applied —
a post-result reduction in replicate count is a retune, whatever its statistical merit.

## 7. Amendment log

| Date | Change | By |
|---|---|---|
| 2026-08-31 | Initial freeze — Packet C1, following operator GO. No simulation run, no real data touched beyond citing already-published L1–L4/H-VOLREGIME figures from the parent brief. | Claude Code |
| 2026-09-01 | **§6 added: right-sizing amendment, `PROPOSED`, awaiting operator ratification.** Discharges the plan doc's own R4 with a measured synthetic timing dry-run (1.002 s/replicate refit, 0.689 s cached, on a shape-matched 139,605-row synthetic panel) rather than an estimate, putting the frozen sizing at 1,336 core-hours. Proposes exactly two changes — cache the volume-free `baseline_1` per outer panel (an output-preserving identity, gated on a bitwise-equality test), and drop `B` to 999 **for the pilot studies only** (permutation p-values are size-calibrated for any `B`; Packet D and the observed run keep `B=4000`), with a pre-declared bounded re-run at `B=4000` for any C3-primary cell whose power lands in [0.70, 0.90]. Net 1,336 → 229 core-hours (83%). **Explicitly rejects** an earlier draft's `N_outer` 100→40 cut, recording the Clopper–Pearson detection arithmetic that refutes it (at n=40 the check flags a true 25% rate only 95.7% of the time and a 15% rate 56.7%, versus 100%/90.1% at n=100) — `N_outer` is the only parameter buying detection sensitivity and is no longer a material cost driver once the other two changes land. No band, cell, seed, gate, escalation, or disposition in §§1–5 is altered, and `DESIGN.md` is untouched. Authored before any pilot or observed L5 statistic, on either instrument, was inspected; §6's own ratification conditions require withdrawal rather than application if that ceases to be true. | Claude Code |
