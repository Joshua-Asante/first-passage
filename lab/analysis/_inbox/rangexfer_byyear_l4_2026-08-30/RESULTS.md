# By-year presence limb (L4) for Q-RANGEXFER-1's five hypotheses — 2026-08-30

**Run in parallel to the ratified bounded Phase 1 round, not part of it.** L4 is a
presence limb computed directly from observed data — it needs no surrogate-null
model, so it is fully independent of whatever Phase 1's joint-surrogation design
work concludes.

## Headline

**All five hypotheses land L4=AMBIGUOUS.** Every one has `n_valid < 7` qualifying
calendar years (`n_cond >= 20` that year), confirming the verdict pre-registration's
own ex-ante prediction (§E: "same structural wall `daily-range-state-persistence`
hit... only 6 of the required 7 full calendar years qualify") rather than merely
speculating it.

**This means: even if the ratified bounded Phase 1 round produces a certified
joint-surrogation null AND Phase 3's attribution limb clears at p_upper<=0.05, the
final §6 verdict for every one of these five hypotheses still lands `AMBIGUOUS-HOLD`,
not `RESOLVED`** — per `Q-RANGEXFER-1`'s own §6 table, `AMBIGUOUS-HOLD` fires
whenever presence limbs pass but L4 cannot resolve (`N_valid < 7`), regardless of
what the attribution limb does. L4 is failing on panel length, not effect strength;
Phase 1 cannot fix it.

## Method

Ported `candidate1_range_persistence.py`'s own by-year convention verbatim
(`YEAR_MIN_NCOND=20`; qualifying year = `n_cond>=20`; `AMBIGUOUS` if `n_valid<7`;
else required = `n_valid-2` years must show the effect positive). Source data: the
already-cached, git-tracked joint frames (`candidate24_joint_frame.csv` for MNQ,
`c24_joint_frame.csv` for MYM) — no vendor bar data needed. Column semantics were
cross-checked against the brief's own cited pooled figures before writing the
by-year script (all five reproduced exactly or within the already-disclosed
1304-vs-1307-day panel gap):

| Hypothesis | Pooled figure reproduced | Cited in brief |
|---|---|---|
| H-RANGEXFER-1 (MNQ) | +0.5774 / +0.3870 | "+57.7pp / +38.7pp" |
| H-RANGEXFER-1.a (MNQ) | +0.1053 / −0.0810 | "+10.5pp calm / −8.1pp hot" |
| H-RANGEXFER-1-MYM | +0.3169 / +0.2170 | "+31.8pp / +22.1pp" (n=1304 vs 1307, disclosed gap) |
| H-RANGEXFER-1.a-MYM | +0.0848 / −0.0724 | "+0.0848 / −0.0724" (exact) |
| H-RANGEXFER-1.b-MYM | +0.1394 / +0.0637 | "+0.1404 / +0.0672" (same disclosed panel gap) |

For the two parent hypotheses (min-across-day-history-strata designs), a qualifying
year requires `n_cond>=20` triggered (`bias_overnight==1`) days that year, and a
"pass" year is one where the min-across-populated-strata lift is positive. For the
three single-stratum-restricted hypotheses, the target stratum is filtered first,
then candidate 1's own single-comparison convention applies directly within it.

## Per-hypothesis detail

- **H-RANGEXFER-1** (MNQ overnight-range, parent): `n_valid=6` (2020 excluded,
  `n_cond=11`), **6/6 qualifying years positive** (min-stratified-lift 0.24–0.64).
  Unanimous, consistent — this is the clean case: L4 fails purely on being one year
  short of 7, not on any inconsistency.
- **H-RANGEXFER-1.a** (MNQ gap-magnitude, overnight-calm-restricted): `n_valid=5`
  (2020, 2026 excluded), **5/5 positive** (0.01–0.21). Also unanimous, but two years
  short rather than one.
- **H-RANGEXFER-1-MYM** (MYM overnight-range, parent): `n_valid=6` (2020 excluded),
  **6/6 positive** (0.03–0.37). Same clean pattern as its MNQ sibling.
- **H-RANGEXFER-1.a-MYM** (MYM gap-magnitude, overnight-calm-restricted): `n_valid=4`
  (2020, 2026 excluded, and generally thinner conditional counts than MNQ's own),
  **only 3/4 positive** — 2024 shows essentially zero (−0.0059). This is the one
  hypothesis where the by-year picture is not unanimous, independently corroborating
  the brief's own characterization of this cell as "the weakest, least-decisive cell
  in the whole batch" (p=0.0495, barely clears 0.05).
- **H-RANGEXFER-1.b-MYM** (MYM gap-magnitude, `bprime=0`-restricted): `n_valid=6`
  (2020 excluded), **only 4/6 positive** — 2022 (−0.013) and 2024 (−0.019) show
  essentially no effect. Despite the pooled per-stratum null-calibrated p=0.00099
  reading as decisive, the year-by-year picture shows the effect is not uniformly
  present — worth weighing against how much confidence the pooled figure alone
  should carry.

## What this changes

Nothing in any brief's own scored verdict — this is a new, exploratory diagnostic,
not yet Codex-reviewed or operator-ratified, and L4 alone was already known to be a
live risk (the pre-registration named it explicitly). What it changes is the
**expected value of the ratified bounded Phase 1 round**: a fully successful Phase 1
design, cleared model adequacy and estimation-aware size/power, still cannot deliver
a `RESOLVED` verdict for any of these five hypotheses today — the best reachable
outcome via this exact panel is `AMBIGUOUS-HOLD` on all five, with the by-year table
now on record rather than merely predicted. The two paths already named in
`Q-RANGEXFER-1`'s own §6 `AMBIGUOUS-HOLD` disposition (`ITERATE — re-score when that
instrument's panel extends to >=7 full calendar years, or a fresh surrogate-class
design is adopted for the by-year-independent limbs`) remain the actual routes past
this wall — panel growth or an L4-independent limb redesign, neither of which Phase 1
addresses.

## Caveats / disclosure

- This is a first-pass exploratory diagnostic authored and run in a single session,
  not yet independently (Codex) reviewed. The min-across-strata by-year convention
  for the two parent hypotheses (qualifying year gated on total `bias_overnight==1`
  count, not per-stratum count) is this script's own design choice, ported from but
  not identical to candidate 1's single-series case — worth a second look.
  `byyear_l4.py`'s own docstring names the exact precedent lines read before writing
  it.
- No K declared for this diagnostic — it re-derives a presence limb from an
  already-scored, already-cited panel; it does not touch a fresh look at outcome
  data beyond what the cited pooled figures already used.
