# Q-VOLREGIME-1 — Packet C1: pilot acceptance bands (frozen before simulation)

**Status:** `FROZEN, NOT YET EXECUTED` — this document declares C1's own required bands, counts, and
disposition rules. **No simulation has been run.** No real L5 statistic, on either instrument, has
been inspected. Nothing here executes anything; it exists so C2–C5 (the actual pilot studies) have
nothing left to decide once real data is touched.

⚠ **A right-sizing amendment is PROPOSED and awaiting operator ratification — see §6.** As revised
2026-09-02 it makes exactly two changes: it caches the volume-free baseline models per outer panel
(an output-preserving identity, gated on a bitwise-equality test), and drops `B` to 999 for the
single **non-gating** C3 half-effect diagnostic cell. Every gating study keeps `B = 4000`, and no
band, cell, `N_outer`, seed, gate, escalation or disposition rule in §§1–5 changes. Until §6 is
ratified, §§1–5 as written remain the controlling spec regardless.

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

## 6. PROPOSED right-sizing amendment (2026-09-01, revised 2026-09-02) — awaiting operator ratification

**Status:** `PROPOSED`. Authored before any pilot execution and before any outcome-bearing byte, on
either instrument, was read — this is a prospective cost amendment, not a response to a result.
The original §§1–5 freeze carried its own operator GO; this amendment therefore needs its own
ratification before it governs anything.

**⚠ Revision 2026-09-02, after Codex review (PR #258): the first draft was materially wrong and
this section is substantially narrower than it was.** That draft proposed `B = 999` for *every*
pilot study and added a power re-run escalation window. Review returned three P1 findings and four
P2s; **all seven were accepted**, two of them fatal to the draft's central claims. The `B`
reduction now applies to one non-gating diagnostic cell instead of all three studies, the
escalation window is withdrawn outright, and the budget is recomputed in CPU-seconds rather than
wall time. The saving drops from a claimed 83% to a measured **45%**. §6.5 records each finding and
its disposition; the superseded draft is in this PR's own history, not silently overwritten.

### Motivation — the plan doc's own R4, discharged with a measurement

`docs/superpowers/plans/2026-09-01-q-volregime-bounded-translation-campaign.md` §2 R4 requires a
synthetic timing dry-run and published CPU-hour, memory and cost figures before a cost GO.
Measured by [`bench_replicate_timing.py`](bench_replicate_timing.py) on the operator's own machine
(8 cores), on a synthetic panel matched to the real frame shape (139,605 rows, 12 baseline
features, 10 expanding folds), executing the full `DESIGN.md` §4.2–§4.4 replicate recipe:

| Quantity | Measured |
|---|---|
| CPU per replicate, baseline refit each time | **0.953 core-seconds** |
| CPU per replicate, volume-free baseline cached | **0.703 core-seconds** |
| Peak working set, one worker process | **258 MB** |
| CPU/wall ratio with thread pools *unpinned* | **1.64** |

**The budget unit is CPU-seconds, not wall time.** With BLAS threading left native, one replicate
consumes ~1.64 cores while appearing to take 0.90 s of wall clock — so a wall-time figure divided
across N workers double-counts cores that a single replicate is already using. Pinning every thread
pool to 1 makes wall and CPU coincide (ratio 0.96–0.98) *and* is marginally faster in aggregate;
the pilot runner should pin threads and parallelize across replicates rather than within them.

At the frozen sizing this is **1,271 core-hours** — about 8.8 days pinned at 6 workers on the
operator's laptop, or ~20 hours on a 64-core box at ~16 GB resident.

### Change 1 — cache the volume-free baseline per outer panel (an identity, not a design change)

Neither `baseline_1` nor `baseline_2` contains a volume-derived feature (`DESIGN.md` §3.1/§3.3):
`baseline_2` differs from `baseline_1` only by the prior-day range-regime control. Under a null
replicate, only the rotation of the volume residual changes; the outcome labels, the fold
boundaries, and every baseline feature are untouched. Both baselines' fitted coefficients are
therefore *identical* across all `B` replicates within a given outer panel, and refitting them `B`
times recomputes the same numbers. Caching per (cell, outer panel) is output-preserving by
construction, not an approximation.

This does **not** weaken §4.4's "every other object is refit fresh for every replicate" rule, whose
purpose is to forbid *nuisance-parameter* shortcuts of the kind that broke `Q-RANGEXFER-1`. The
residualization regression, the causal `pseudo_tod_threshold` reconstruction, and
`augmented_1`/`augmented_2` all remain refit per replicate, unchanged.

**Required disclosure and test.** A P2 test must assert, for **both** `baseline_1` and
`baseline_2`, that the cached coefficients and OOS predictions are bitwise equal to a refit on at
least one replicate per cell. If either fails, the cache is abandoned for that model and the
full-refit cost is paid. The measured 0.703 core-s figure was benchmarked on `baseline_1`'s
12-feature set; `baseline_2` carries one additional control, so the Comparison-2 budget rows below
are a close approximation rather than a direct measurement — a re-benchmark on `baseline_2`'s own
feature set is owed before the cost GO, not after.

Measured saving: **26.2%**.

### Change 2 — `B = 999` for the non-gating C3 half-effect cell only

§3 freezes the half-magnitude planted effect as explicitly **"diagnostic, reported but not
gating"** — no minimum power requirement attaches to it, and no pilot disposition turns on its
value. Monte-Carlo precision on a quantity that gates nothing buys nothing, so this one cell drops
to `B = 999`.

**Everything that gates keeps `B = 4000`:** C2's null-size study, C3's primary power study, and
Packet D's own observed run are all unchanged. This is a deliberate retreat from the first draft —
see §6.5 findings P1-1 and P1-3 for why the broader reduction was wrong.

### Explicitly NOT changed

- **`N_outer = 100` stands.** An earlier draft proposed cutting it to 40. The exact
  Clopper–Pearson detection arithmetic refutes that, and the rejected option is recorded here
  rather than dropped silently. Probability the C2 check flags a cell whose true Type-I rate is:

  | `N_outer` | accept band | true 8% | true 10% | true 15% | true 25% |
  |---:|---|---:|---:|---:|---:|
  | **100 (frozen, retained)** | [1, 10] | 17.6% | 41.7% | 90.1% | 100% |
  | 60 | [0, 7] | 10.4% | 24.8% | 69.5% | 99.1% |
  | 40 (rejected) | [0, 5] | 9.7% | 20.6% | 56.7% | 95.7% |

  `N_outer` is the *only* parameter buying detection sensitivity, and §1 already discloses that
  n=100 cannot resolve a subtle miscalibration; the table shows it is in fact effectively blind
  below ~15%. Cutting to 40 would move that blind spot up against 25% — the exact magnitude
  `Q-RANGEXFER-1` actually exhibited, i.e. it would degrade the one thing the study exists to catch.
- **`B` for both gating studies.** Withdrawn from the first draft — see §6.5.
- **No new escalation.** The first draft added a `B = 4000` re-run for C3-primary cells landing in
  [0.70, 0.90]. Withdrawn: §5 states that a §3 power failure has **no** escalation and terminates
  immediately, so that rule silently contradicted a frozen disposition while this section claimed
  §§1–5 were untouched. **§5 stands exactly as frozen**, and its embargo-widening remains the sole
  permitted escalation in the pilot.
- The §3 half-magnitude cell is **retained**, not deleted, despite being non-gating.
- Every band, cell, seed convention, gate and terminal disposition in §§1–5 is unchanged, as is
  `DESIGN.md` in full. Comparison 2 remains scheduled in parallel; whether it gates is
  reconciliation item R1's question, not this amendment's.

### Resulting budget

| Study | Frozen | Proposed | Change |
|---|---:|---:|---|
| C2 null-size (gating) | 424 core-h | 312 core-h | cached; `B` unchanged |
| C3 power, primary (gating) | 424 core-h | 312 core-h | cached; `B` unchanged |
| C3 power, half-effect (non-gating) | 424 core-h | 78 core-h | cached; `B` 4000 → 999 |
| **Total** | **1,271 core-h** | **703 core-h** | **44.7% cut** |

Wall clock at 6 pinned workers: 8.8 days → **4.9 days**. At 64 pinned workers: 19.9 h → **11.0 h**,
at ~16 GB resident. C4's own diagnostics are not in this budget and remain to be costed separately.

### §6.5 — Codex review response (PR #258, 2026-09-02)

Seven findings, all accepted. Two invalidated the first draft's headline claims.

| # | Finding | Disposition |
|---|---|---|
| P1-1 | Reducing `B` can change **C2's own detection power** under *broken* exchangeability — the case C2 exists to detect — because MC error near the 0.05 boundary is `B`-dependent (SE ≈0.0069 at 999 vs ≈0.0034 at 4000). The draft's exactness argument holds only under the null it is trying to test. | **Accepted.** `B = 4000` restored for C2. The draft's disclosed caveat covered only the extreme tail (p≈0.001), not this threshold-local mode. |
| P1-2 | The [0.70, 0.90] power re-run **contradicts §5**, which gives a §3 power failure no escalation and terminates immediately — so the draft changed a frozen disposition while claiming it hadn't. | **Accepted.** Escalation withdrawn entirely; §5 stands as frozen. |
| P1-3 | Justifying `B = 999` for C3 by "planted p-values will sit deep in the tail" **assumes R2/R3, which are open** — the row-level effect generator is undefined and the lift→Brier-improvement mapping unestablished, so panels could land near the boundary. | **Accepted.** `B = 4000` restored for C3-primary. The reduction survives only on the non-gating half-effect cell, where no decision rides on precision. |
| P2-1 | The benchmark reported **wall time as core time**; with native BLAS threading a replicate consumes 1.64 cores, so the budget was understated and the divide-by-workers arithmetic double-counted. | **Accepted and measured.** Script now pins thread pools, reports CPU time and the CPU/wall ratio, and the budget is recomputed in CPU-seconds. |
| P2-2 | The committed reproducer **still printed the rejected plan** (`N_outer=40`, conditional Comparison 2, no half-effect cell) — 107 core-hours, not the section's figure. The "reproduces every number" claim was false. | **Accepted.** [`rightsize_arithmetic.py`](rightsize_arithmetic.py) rewritten to compute exactly the proposal above; its output is the source of every number in this section. |
| P2-3 | The **memory bound was asserted, not measured** (~15 MB claimed; `df`+`X`+`Xa` alone exceed 45 MB). | **Accepted and measured.** Peak working set is **258 MB per worker** (~16 GB at 64 concurrent workers). The plan doc's R4 note is corrected to match. |
| P2-4 | The cache rule authorized **`baseline_1` only** while the budget applied cached timing to all four cells, including Comparison 2 (whose model is `baseline_2`). | **Accepted.** Change 1 now covers both baselines explicitly, with the bitwise test required for each; the `baseline_2` re-benchmark is named as owed before the cost GO. |

### Reproducing every number in this section

Both scripts are synthetic-only: they read no vendor panel, score no pilot or observed statistic,
and touch nothing under `core/data/`. Numbers above are their output, not estimates.

```bash
# CPU-seconds/replicate, CPU/wall ratio, peak working set
python lab/analysis/_inbox/volregime_l5_pilot_2026-08-31/bench_replicate_timing.py --reps 9

# same, without thread pinning, to reproduce the 1.64 CPU/wall figure
python lab/analysis/_inbox/volregime_l5_pilot_2026-08-31/bench_replicate_timing.py --native-threads

# Clopper-Pearson bands, detection power, and the budget table
python lab/analysis/_inbox/volregime_l5_pilot_2026-08-31/rightsize_arithmetic.py
```

Timings are hardware-relative and vary ~15% run to run on a laptop. Re-run
`bench_replicate_timing.py` on whatever machine actually executes the pilot — and on
`baseline_2`'s own feature set — before quoting a wall-clock or dollar figure for it.

### Ratification conditions

This amendment is legitimate only because it is prospective. If any pilot or observed L5 result has
been inspected on either instrument before ratification, it must be withdrawn rather than applied —
a post-result reduction in replicate count is a retune, whatever its statistical merit.

## 7. Amendment log

| Date | Change | By |
|---|---|---|
| 2026-08-31 | Initial freeze — Packet C1, following operator GO. No simulation run, no real data touched beyond citing already-published L1–L4/H-VOLREGIME figures from the parent brief. | Claude Code |
| 2026-09-01 | **§6 added: right-sizing amendment, `PROPOSED`, awaiting operator ratification.** Discharges the plan doc's own R4 with a measured synthetic timing dry-run (1.002 s/replicate refit, 0.689 s cached, on a shape-matched 139,605-row synthetic panel) rather than an estimate, putting the frozen sizing at 1,336 core-hours. Proposes exactly two changes — cache the volume-free `baseline_1` per outer panel (an output-preserving identity, gated on a bitwise-equality test), and drop `B` to 999 **for the pilot studies only** (permutation p-values are size-calibrated for any `B`; Packet D and the observed run keep `B=4000`), with a pre-declared bounded re-run at `B=4000` for any C3-primary cell whose power lands in [0.70, 0.90]. Net 1,336 → 229 core-hours (83%). **Explicitly rejects** an earlier draft's `N_outer` 100→40 cut, recording the Clopper–Pearson detection arithmetic that refutes it (at n=40 the check flags a true 25% rate only 95.7% of the time and a 15% rate 56.7%, versus 100%/90.1% at n=100) — `N_outer` is the only parameter buying detection sensitivity and is no longer a material cost driver once the other two changes land. No band, cell, seed, gate, escalation, or disposition in §§1–5 is altered, and `DESIGN.md` is untouched. Authored before any pilot or observed L5 statistic, on either instrument, was inspected; §6's own ratification conditions require withdrawal rather than application if that ceases to be true. | Claude Code |
| 2026-09-02 | **§6 substantially narrowed after Codex review (PR #258) — seven findings, all accepted, two fatal to the prior day's draft.** (1) Reducing `B` can change **C2's own detection power** under broken exchangeability, the very case C2 exists to detect, because Monte-Carlo error near the 0.05 boundary is `B`-dependent — the prior draft's exactness argument holds only under the null being tested. `B = 4000` restored for C2. (2) The prior draft's [0.70, 0.90] power re-run **contradicted §5**, which gives a §3 power failure no escalation at all — so it silently changed a frozen disposition while claiming §§1–5 were untouched. Escalation withdrawn entirely. (3) The `B = 999`-for-C3 justification rested on planted p-values landing deep in the tail, which **presumes R2/R3, both open** — restored to `B = 4000` for C3-primary. (4) The benchmark reported **wall time as core time**; unpinned BLAS makes one replicate consume 1.64 cores, so the published budget was understated — script now pins thread pools and reports CPU-seconds. (5) The committed reproducer **still printed the rejected plan** (107 core-hours, `N_outer=40`), falsifying the "reproduces every number" claim — rewritten. (6) The **memory bound was asserted, not measured** — peak working set is **258 MB per worker**, not the ~15 MB claimed. (7) The cache rule covered `baseline_1` only while the budget assumed caching for Comparison 2's `baseline_2` — extended to both, with a `baseline_2` re-benchmark named as owed. **Surviving proposal: cache both volume-free baselines, and `B = 999` for the one non-gating diagnostic cell.** Budget 1,271 → 703 core-hours (44.7%), down from the withdrawn draft's claimed 83%. No band, cell, `N_outer`, seed, gate, escalation or disposition in §§1–5 changes; `DESIGN.md` untouched. Still `PROPOSED`; no pilot or observed L5 statistic inspected. | Claude Code, responding to Codex's PR #258 review |
