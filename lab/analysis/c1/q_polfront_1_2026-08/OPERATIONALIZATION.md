# Q-POLFRONT-1 — frozen operationalizations (written BEFORE any policy number is computed)

**Parent brief (frozen, byte-unedited):** [`Q-POLFRONT-1-policy-augmented-seed-frontier.md`](../../../../docs/briefs/Q-POLFRONT-1-policy-augmented-seed-frontier.md)
— operator GO 2026-08-16. This file resolves the brief's grid-description ambiguity and freezes
the quantized/intraday-sensitivity operationalizations. It is committed before `run_polfront.py`
produces any policy number. Nothing here adds a cell, removes one, or touches §4/§6.

## Fidelity gate (executed before this file was written)

`python run_seed_spec.py --verify` (recovered harness, tag `pre-prune-2026-08-08`) →
0.000pp delta vs `core/mc/simulation.py`, matching the recorded RESULTS.md figure exactly.
Anchor reproduction: `max_risk(0.55, 2.0, 1, 3.0, n_sims=6000, seed=17)` → `(350, pass 97.68,
bust 2.32)`; `max_risk(0.55, 2.0, 3, 3.0, n_sims=6000, seed=17)` → `(425, pass 97.9, bust 2.1)`
— bit-identical to `RESULTS.json`'s `minimum_admissible_edge` rows for `(w=0.55, b=2.0)`.
**No environment-vintage drift on this harness** (pure numpy `default_rng`, no pandas
resampling dependency — unlike the book-comp harness that drifted under Q-EVALSEQ-1).
No fallback gate needed.

## Grid, operationalized

Brief text: *"the seed-target spec's §2/§4 cell set (its (w, b) pairs × k ∈ {1, 2, 4})."*
§2 = `run_seed_spec.py` section A (T7 rederivation): `(0.55,2.0), (0.60,2.0), (0.50,2.0),
(0.45,2.5)`. §4 = section D (minimum admissible edge): `(0.55,2.0), (0.50,2.0), (0.45,2.0),
(0.40,2.0), (0.35,2.0), (0.55,1.2), (0.50,1.2), (0.45,1.2)`.

**Resolution:** union of the two sections' `(w,b)` pairs (dedup on the shared `(0.55,2.0)`),
crossed with the brief's own stated `k ∈ {1, 2, 4}` — a deliberate sub-range of §2's full
`k ∈ {1,2,3,4,6,8}`, spanning sparse/medium/denser cadence without re-running the full sweep.

**Frozen grid (10 pairs × 3 k = 30 cells):**
`(0.55,2.0) (0.60,2.0) (0.50,2.0) (0.45,2.5) (0.45,2.0) (0.40,2.0) (0.35,2.0) (0.55,1.2)
(0.50,1.2) (0.45,1.2)` × `k ∈ {1, 2, 4}`.

**Zero-admissible cells (disclosed, not counted in the ratio):** the frozen §4 record shows
`(0.35, 2.0)` (edge +0.050R) and `(0.45, 1.2)` (edge −0.010R) clear **no** R at the ratified
gate under constant sizing ("— none —" in RESULTS.md §4). If the policy arm admits an R where
the flat arm admits none, that cell is reported separately as **newly-admitted geometry**
(a stronger form of the headline finding — infinite ratio) and excluded from the median-ratio
statistic, which is undefined for a zero denominator. This is a reporting convention, not a
verdict change: §4's median-ratio threshold is computed only over cells with both R_max^flat
and R_max^policy defined.

## Arms, operationalized

- **(i) constant-R control:** the harness's own `max_risk()`, unmodified. Same `inactivity=False`
  (matching the ratified gate's "inactivity disabled" reading, carried from `run_seed_spec.py`'s
  own §2/§4 sections — not a new choice) and `duty=1.0` (§2/§4's own default; duty was §3's
  separate, uncited axis).
- **(ii) policy `P_c`:** a day-indexed port of Q-EVALSEQ-1's winner, generalized to this
  harness's per-day (not per-trade) state granularity. At the **start of each business day**
  (before that day's `k` trades are drawn): `cushion_t = profit_t − (peak_t − ROPE)`,
  `m_t = min(1, max(0, cushion_t) / ROPE)`, `r_t = R_base · m_t` — cap **1.0** (the brief's own
  declared change from Q-EVALSEQ-1's 0.75 book-family cap; the day's `k` trades all use `r_t`
  uniformly, matching this harness's "one risk figure per active day" model). `max_risk_policy()`
  sweeps `R_base` with the identical bust/pass acceptance rule as the flat `max_risk()`.
- **Seeding (frozen, per §6 "re-run same-seed for comparability"):** both arms, every cell, use
  the **same seed = 101** — a common-random-numbers design so the two arms share the same
  underlying win/loss draw stream per cell and the ratio's sampling noise is reduced to the
  policy's own effect, not independent-seed noise. `n_sims = 6000` (matching the harness's own
  `n_small`, the precision used for its own T7/§4 sections).

> **Sweep-range amendment (2026-08-16, recorded BEFORE any grid number was read).** A smoke
> test on `(w=0.55, b=2.0, k=1)` returned `r_policy_max = 1575` — sitting on the search
> boundary of the flat arm's own `r_hi=1600`, meaning the reported "max" could be a
> search-ceiling artifact, not a true admissibility limit (the same failure class the
> `max_risk` sweep-and-break design otherwise catches, but only within the tested range).
> Diagnosis: probed `r ∈ {1600, 3000, 6000, 12000, 24000, 48000}` directly. Bust is flat and
> near-zero through 1600, then **saturates at 83.7–95.8%** at `r=3000=ROPE` and every value
> above it, for every probed cell (strong-edge and weak-edge, k=1 and k=4) — a sharp,
> theoretically-motivated phase transition, not a gradual one: once `r_base ≥ ROPE`, a **single
> losing trade on any day the path sits at its own running peak** (`cushion = ROPE`, `m = 1`,
> so `r_t = r_base ≥ ROPE`) breaches the floor by itself, independent of `w`, `b`, or `k`
> (for `k > 1`, the first losing trade within such a day alone drives the day's cumulative low
> to `≤ −ROPE`, before the day's remaining trades even resolve). **The true policy ceiling is
> therefore always `< ROPE = $3,000`, for every cell in this grid, by construction — not a
> per-cell empirical fact.** Resolution: `POLICY_R_HI = ROPE` (a principled, theoretically-
> derived bound, not an arbitrary widening), same `step = 25` as the flat arm, applied to the
> policy sweep only. The flat arm's own `r_hi = 1600` is unchanged (it already comfortably
> bounds every flat-arm result on record, e.g. the frozen `$350–$425` cells). A
> `policy_near_ceiling` flag is computed and reported per cell (`r_policy_max ≥
> POLICY_R_HI − step`) as a residual-boundary disclosure, though none is expected given the
> mechanism above holds regardless of `(w,b,k)`.

## Disclosure arms, operationalized

- **Quantized (mandatory):** the brief names "1-micro floor at a stated $/R" but does not fix
  the instrument, so no single $/contract quantum is canonical here — the seed-target model is
  intentionally instrument-agnostic (`w,b,r,k`). Operationalized as a **sensitivity sweep over
  three illustrative quanta** anchored to real repo figures: `Q ∈ {$25, $50, $85}` ($85 = the
  design box's own lowest-R feasible cell, `docs/notes/notice/N-2026-08-13-msl-design-box-rederivation.md`
  §3). For each cell and each `Q`: `R_q = floor(R / Q) · Q` substituted for both arms' R_max;
  report the quantized ratio and flag if any `Q` flips the direction of "policy > flat" for the
  **median** cell (the §4 AMBIGUOUS-ABSTRACTION trigger).
- **Intraday-sensitivity (mandatory, exploratory):** operationalized as a stress re-evaluation
  **at each arm's already-found R_max** (no re-sweep): double the magnitude of the day's within-
  day low excursion (`day_low_stressed = 2 · day_low`, close/pass unaffected) before the bust
  test, and report the resulting bust rate for both arms at their respective R_max. This is a
  stylized proxy for the standing lesson that the venue enforces breach intraday while this
  engine (like `run_seed_spec.py` itself) tests EOD — the same clock caveat Q-EVALSEQ-1 disclosed.
  Explicitly labeled exploratory; it does not feed §4's verdict.

## Disclosures carried from Q-EVALSEQ-1 (same instrument family)

EOD-clock lower bound; risk_pct-layer abstraction (integer floors not modeled outside the
dedicated quantized arm above); in-panel-tails-only note does not apply here (this harness draws
i.i.d. trade outcomes from `w`, not a bootstrapped historical panel — no tail-support caveat).
