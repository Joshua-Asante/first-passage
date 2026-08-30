# By-year presence limb (L4) for Q-RANGEXFER-1's five hypotheses — 2026-08-30

**Run in parallel to the ratified bounded Phase 1 round, not part of it.** L4 is a
presence limb computed directly from observed data — it needs no surrogate-null
model, so it is fully independent of whatever Phase 1's joint-surrogation design
work concludes.

**Corrected 2026-08-30, same day, responding to Codex's PR #224 review — see
"Codex review" section below for the full account.** The two parent hypotheses'
`n_valid` moved from 6 to 3 (a real bug in the first version's qualifying-year
gate, now fixed); the "final verdict is guaranteed `AMBIGUOUS-HOLD`" framing was
overstated and is corrected; the MYM panel-gap caveat is strengthened; one
proposed correction (re-deriving `H-RANGEXFER-1.a`/`.a-MYM` as a further
day-history-stratified statistic) was investigated and found to compute a
*different* statistic than the one the brief actually cites — not applied,
reasoning below.

## Headline

**All five hypotheses land L4=AMBIGUOUS.** Every one has `n_valid < 7` qualifying
calendar years, confirming the verdict pre-registration's own ex-ante prediction
(§E: "same structural wall `daily-range-state-persistence` hit... only 6 of the
required 7 full calendar years qualify") rather than merely speculating it.

**What this means for Phase 1, stated precisely (corrected — see finding 3
below): `RESOLVED` is unreachable for any of these five hypotheses at this panel
length, regardless of how Phase 1's design work turns out. `AMBIGUOUS-HOLD` is
the *best reachable* verdict — not a guaranteed one** — per `Q-RANGEXFER-1`'s own
§6 table, `AMBIGUOUS-HOLD` requires presence limbs L1-L3 to also pass; this
diagnostic computes L4 only. If L1-L3 turn out to fail for a given hypothesis,
that hypothesis's actual verdict is `FALSIFIED`, not `AMBIGUOUS-HOLD` — L1-L3
have not been checked here.

## Method

Ported `candidate1_range_persistence.py`'s own by-year convention verbatim
(`YEAR_MIN_NCOND=20`; `AMBIGUOUS` if `n_valid<7`; else required = `n_valid-2`
years must show the effect positive). Source data: the already-cached,
git-tracked joint frames (`candidate24_joint_frame.csv` for MNQ, `c24_joint_frame.csv`
for MYM) — no vendor bar data needed (confirmed unavailable in this environment
for both instruments). Column semantics were cross-checked against the brief's
own cited pooled figures before writing the by-year script (all five reproduced
exactly, or within the already-disclosed 1304-vs-1307-day MYM panel gap):

| Hypothesis | Pooled figure reproduced | Cited in brief |
|---|---|---|
| H-RANGEXFER-1 (MNQ) | +0.5774 / +0.3870 | "+57.7pp / +38.7pp" |
| H-RANGEXFER-1.a (MNQ) | +0.1053, n=175/973 | "+10.5pp... n=175/973" — n reproduced exactly, not just the lift |
| H-RANGEXFER-1-MYM | +0.3169 / +0.2170 | "+31.8pp / +22.1pp" (n=1304 vs 1307, disclosed gap) |
| H-RANGEXFER-1.a-MYM | +0.0848, n=991 | "+0.0848... n=991" — n reproduced exactly |
| H-RANGEXFER-1.b-MYM | +0.1394 / +0.0637 | "+0.1404 / +0.0672" (same disclosed panel gap) |

**Qualifying-year rule, corrected (see finding 1 below):** for the two parent
hypotheses (min-across-day-history-strata designs), a year now qualifies only if
**every populated stratum independently** has `n_cond>=20` — not the pooled
`bias_overnight==1` count across both strata, which the first version of this
script used and which let a near-empty stratum silently drive a year's min-lift
while still counting as qualifying. For the three single-stratum-restricted
hypotheses, the target stratum is filtered first, then candidate 1's own
single-comparison convention applies directly within it (unaffected by this fix
— see finding 4 below for why these three are pooled two-way comparisons, not
further-stratified ones).

## Per-hypothesis detail

- **H-RANGEXFER-1** (MNQ overnight-range, parent): `n_valid=3` (2021, 2022,
  2025 — 2020/2023/2024/2026 excluded because their `bias_dayhist=1` stratum
  alone has only 2/7/19/12 conditional observations even though the pooled
  count looked adequate), **3/3 qualifying years positive** (min-stratified-lift
  0.24–0.45). Still unanimous under the stricter, corrected gate — if anything
  this strengthens the "fails purely on panel length, not consistency" reading,
  on a thinner base.
- **H-RANGEXFER-1.a** (MNQ gap-magnitude, overnight-calm-restricted, pooled
  two-way): `n_valid=5` (2020, 2026 excluded), **5/5 positive** (0.01–0.21).
  Unanimous, two years short of 7.
- **H-RANGEXFER-1-MYM** (MYM overnight-range, parent): `n_valid=3` (2021, 2022,
  2024 — same per-stratum-floor correction as MNQ's own), **3/3 positive**
  (0.03–0.22). Same clean, now-thinner pattern as its MNQ sibling.
- **H-RANGEXFER-1.a-MYM** (MYM gap-magnitude, overnight-calm-restricted, pooled
  two-way): `n_valid=4` (2020, 2026 excluded), **only 3/4 positive** — 2024
  shows essentially zero (−0.0059). The one hypothesis where the by-year
  picture is not unanimous, independently corroborating the brief's own
  characterization of this cell as "the weakest, least-decisive cell in the
  whole batch" (p=0.0495, barely clears 0.05). **MYM-specific caveat (finding 2
  below): computed on the disclosed 1304-day cache, not the frozen 1307-day
  panel — no year here sits exactly at the n=20 boundary the way
  H-RANGEXFER-1.b-MYM's 2026 does, but treat as provisional pending a
  vendor-data re-run, same as every other MYM figure in this diagnostic.**
- **H-RANGEXFER-1.b-MYM** (MYM gap-magnitude, `bprime=0`-restricted, pooled
  two-way): `n_valid=6` (2020 excluded), **only 4/6 positive** — 2022 (−0.013)
  and 2024 (−0.019) show essentially no effect. Despite the pooled per-stratum
  null-calibrated p=0.00099 reading as decisive, the year-by-year picture shows
  the effect is not uniformly present. **MYM panel-gap caveat, sharpened
  (finding 2): 2026 has exactly 20 conditional cases (lift +0.007, barely
  positive) — the single most boundary-sensitive result in this entire
  diagnostic. The 1304-day cache used here excludes 3 days present in the
  frozen 1307-day candidate panel (rows missing a gap/overnight predictor,
  unrelated to `bprime`); if even one of those 3 excluded days would have
  landed in 2026 as a `bprime=0` conditional case, this year's qualification
  or sign could flip. Treat 2026's own qualification and the resulting
  `n_pass=4/6` as provisional pending a re-run against the frozen 1307-day
  panel once vendor bars are available — not yet done in this environment.**

## What this changes

Nothing in any brief's own scored verdict — this is a new, exploratory
diagnostic, and L4 alone was already a named live risk (the pre-registration
named it explicitly). What it changes is the **expected value of the ratified
bounded Phase 1 round**: even a fully successful Phase 1 design cannot deliver
`RESOLVED` for any of these five hypotheses today — `RESOLVED` requires L4 to
resolve, and it structurally cannot at this panel length. The best reachable
outcome via this exact panel is `AMBIGUOUS-HOLD` on all five, **conditional on
L1-L3 also passing (not checked here)**. The two paths already named in
`Q-RANGEXFER-1`'s own §6 `AMBIGUOUS-HOLD` disposition (`ITERATE — re-score when
that instrument's panel extends to >=7 full calendar years, or a fresh
surrogate-class design is adopted for the by-year-independent limbs`) remain
the actual routes past this wall — panel growth or an L4-independent limb
redesign, neither of which Phase 1 addresses.

## Codex review (PR #224) — four findings, each independently re-verified

1. **(Confirmed, fixed) Apply the yearly sample floor to every minimized
   stratum.** The first version gated a year's qualification on the *pooled*
   `bias_overnight==1` count across both `bias_dayhist` strata, even though the
   year's own statistic is the *minimum* of two separately-estimated stratum
   lifts. Verified directly: MNQ 2023/2024/2026 have only 7/19/12 conditional
   observations in `bias_dayhist=1` alone, MYM's own 2020/2023/2026 similarly
   thin — all were counted as qualifying under the pooled gate. **Fixed:**
   `l4_min_stratified` now requires every populated stratum to independently
   clear `YEAR_MIN_NCOND`. `n_valid` for both parent hypotheses moved from 6 to
   3; both remain unanimous (3/3) under the corrected, stricter gate.
2. **(Confirmed, cannot fully fix here — caveat strengthened) Score MYM limbs
   on the frozen 1,307-day panel.** Verified: `MYM_M15.csv` is not present in
   this environment (same vendor-data gap already disclosed throughout this
   repo for every MYM script this session touched), so the 1304-day cache is
   the only data available here, not a choice. Sharpened the specific
   boundary-sensitive case Codex named (`H-RANGEXFER-1.b-MYM`'s 2026, exactly
   20 conditional cases, lift +0.007) into its own explicit caveat above rather
   than leaving it implicit in the general disclosure. A re-run against the
   frozen 1307-day panel once vendor bars are available is named as owed,
   explicitly, not silently assumed equivalent.
3. **(Confirmed, fixed) Condition the final verdict on the uncomputed L1-L3
   limbs.** The original framing asserted every hypothesis's final verdict
   "lands `AMBIGUOUS-HOLD`" — true only if L1-L3 also pass, which this
   diagnostic never checked. Corrected throughout this file (Headline, "What
   this changes") to state `RESOLVED` is unreachable and `AMBIGUOUS-HOLD` is
   the *best reachable*, not guaranteed, outcome.
4. **(Investigated, not applied) Compute the nested L4 limbs on the stratified
   estimand.** Codex's proposal: `H-RANGEXFER-1.a`/`H-RANGEXFER-1.a-MYM` should
   be computed as the minimum of gap-lift after *further* splitting the
   overnight-calm panel by `bias_dayhist`, not a pooled two-way comparison.
   Investigated directly: the brief's own cited statistic for
   `H-RANGEXFER-1.a` is "+10.5pp... n=175/973" and for `H-RANGEXFER-1.a-MYM` is
   "+0.0848... n=991." Reproducing the POOLED two-way comparison (gap=1 vs
   gap=0, within the overnight-calm restriction, no further day-history split)
   gives exactly n=175/973 (175 = gap-positive count, 973 = 1148-175 = the
   pooled reference count) and lift=+0.1053 for MNQ, and exactly n=991 and
   lift=+0.0848 for MYM — matching the brief's own citations exactly, including
   the sample sizes, not just the lift. The further day-history-stratified
   version Codex describes gives different n's (940/208 split for MNQ, neither
   matching 973) and a different lift (min(0.086, 0.096)=0.086, not 0.1053) —
   it computes a genuinely different, not-yet-established statistic. **Not
   applied**, since faithfully reproducing L4 for *this brief's own
   already-cited hypothesis* requires matching its already-established
   statistic, not substituting a different (arguably more conservative, but
   uncited) one. If the brief's own hypothesis definition should be tightened
   to require day-history-matching within the overnight-calm restriction, that
   is a separate, larger change to the hypothesis's own definition in
   `Q-RANGEXFER-1` itself — out of scope for a diagnostic that probes an
   already-defined statistic — and would need its own review, not a silent
   substitution here.

## Caveats / disclosure

- This is a first-pass exploratory diagnostic, independently reviewed once
  (Codex, PR #224, this pass) — not yet operator-ratified.
- No K declared for this diagnostic — it re-derives a presence limb from an
  already-scored, already-cited panel; it does not touch a fresh look at
  outcome data beyond what the cited pooled figures already used.
