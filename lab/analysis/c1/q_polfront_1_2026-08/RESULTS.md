# Q-POLFRONT-1 — RESULTS (policy-augmented seed-target frontier)

**Run:** 2026-08-16 · instrument = recovered `tradeify_seed_target_spec_2026-08-04` harness
(tag `pre-prune-2026-08-08`, engine cross-check 0.000pp vs `core/mc/simulation.py`, anchor
`(0.55,2.0,k=1)`/`(0.55,2.0,k=3)` bit-identical to `RESULTS.json` — no environment drift).
**Pre-registration:** [frozen brief](../../../../docs/briefs/Q-POLFRONT-1-policy-augmented-seed-frontier.md), §4/§6 byte-unedited; [OPERATIONALIZATION](OPERATIONALIZATION.md) (grid resolution + sweep-range amendment, both frozen pre-read).
**Verdict:** `RESOLVED-QUANTIFIED` — median R_max ratio (policy/flat) = **5.107×** across 24 defined cells ≥ the 1.25× bar; pass-floor ≥50% held in every counted cell by construction (the `max_risk` acceptance rule); no reversal at any tested quantum. H holds.
**Machine row:** `median_ratio 5.107 >= 1.25 | min_ratio 1.526 | n_defined 24/30 | newly_admitted 2 | pass_floor_violations 0 | RESOLVED-QUANTIFIED`
**Spend / K:** $0 · K=0 · measurement only · no candidate, no admission, no deployment surface.

## Grid and arms (frozen — see OPERATIONALIZATION.md)

30 cells: 10 `(w,b)` pairs (union of seed-spec §2+§4) × `k ∈ {1,2,4}`. Arm (i) constant-R
control = the seed-spec's own `max_risk()`, unmodified. Arm (ii) policy `P_c`: `r_t = R_base ·
min(1, cushion_t/3000)` at cap 1.0, day-indexed port of the Q-EVALSEQ-1 winner. Same seed (101)
both arms per cell (common-random-numbers). `n_sims=6000`, `inactivity=False`, `duty=1.0` —
identical to the seed-spec's own T7/§4 configuration.

**Sweep-range finding (recorded before any number was read, full account in
OPERATIONALIZATION.md):** the policy sweep's true ceiling is theoretically bounded at
`R_base < ROPE ($3,000)` for every cell, because at `R_base ≥ ROPE` a single losing trade on
any day the path sits at its own running peak (`m=1`) breaches the floor by itself —
confirmed numerically (bust saturates at 83.7–95.8% at `r=ROPE` across every probed cell). The
policy sweep range was widened to `[50, ROPE)` accordingly (flat arm's `[50,1600)` unchanged).
`policy_near_ceiling` computed per cell: **0/30** — the theoretical bound held everywhere,
no residual boundary artifact.

## Headline: policy dominates the flat frontier

| Statistic | Value |
|---|---|
| Cells with both arms defined | 24 / 30 |
| **Median ratio (policy/flat)** | **5.107×** |
| Min / max ratio | 1.526× / 12.667× |
| Cells newly admitted by policy (flat = none) | 2 — `(w=0.35,b=2.0,k=2)` R=$200; `(w=0.35,b=2.0,k=4)` R=$225 |
| Cells admissible under neither arm | 4 — `(0.35,2.0,k=1)`, `(0.45,1.2,k=1/2/4)` (matches the parent spec's own "— none —" cells) |
| Quantized median ratio at Q=$25/$50/$85 | 5.107 / 5.322 / 5.000 — **no reversal at any quantum** |

Representative rows (full 30-cell table in `out/polfront_results.json`):

| w | b | k | R_flat | flat pass/bust | R_policy | policy pass/bust | ratio |
|---|---|---|---|---|---|---|---|
| 0.55 | 2.0 | 1 | $350 | 97.4% / 2.7% | $1,825 | 97.2% / 2.5% | 5.21× |
| 0.60 | 2.0 | 1 | $475 | 97.2% / 2.8% | $2,150 | 97.4% / 2.5% | 4.53× |
| 0.50 | 1.2 | 1 | $75 | 96.1% / 1.4% | $775 | 50.7% / 0.0% | 10.33× |
| 0.40 | 2.0 | 1 | $75 | 99.4% / 0.6% | $950 | 52.2% / 0.0% | 12.67× |
| 0.55 | 2.0 | 4 | $350 | 98.5% / 1.5% | $725 | 100.0% / 0.0% | 2.07× |
| 0.60 | 2.0 | 4 | $475 | 98.1% / 1.9% | $725 | 100.0% / 0.0% | 1.53× (min) |

Pattern: the ratio is **largest at k=1 and shrinks as k rises** — the policy's day-level
throttle has more room to work when there are fewer, larger trades per day; at k=4 the
within-day loss granularity (multiple trades per day) erodes the advantage toward the flat
arm's own headroom, though it never falls below 1.5×.

## ⚠ The load-bearing caveat: the policy's edge is far more EOD-clock-fragile than the flat arm's

Mandatory intraday-sensitivity disclosure (day's within-day low excursion doubled at each
arm's own R_max, no re-sweep — exploratory, does not feed the §4 verdict):

| Statistic | Flat arm | Policy arm |
|---|---|---|
| Median bust-rate increase under stress | **+1.63pp** | **+55.2pp** |
| Max bust-rate increase under stress | +13.83pp | +84.1pp |

**This is not a footnote.** The flat arm's bust barely moves under the stress test — its
admissible R already carries real margin against the 3.0% ceiling. The policy arm's bust rate
explodes: a construct sized to the policy's frontier R and then measured on a clock that
enforces intraday excursions **degrades toward its raw, unthrottled bust rate**, because the
policy's near-zero-bust result depends on the multiplier reacting to a drawdown *before* the
day's worst excursion happens — exactly the ordering the EOD-close proxy gets right and a true
intraday clock does not guarantee. The standing lesson (`lesson_tradeify_trail_enforced_intraday`
— every EOD bust figure is a lower bound, and the venue enforces breach intraday) applies with
far more force to the policy arm than it ever did to constant-R sizing. **The 5.1× headline
ratio is an EOD-clock number; an intraday-honest remeasurement of the policy arm — not
attempted here — could close most or all of the gap in the worst-affected cells.**

## What this does NOT establish

Per §5 (frozen, forbidden moves): no cell here is an admission, a candidate, or a WATCH-rung
change. This is candidate-independent geometry for the deep-iteration lane's family selection
(GO-1), not a strategy result. The instrument-agnostic `(w,b,r,k)` model carries every
disclosed bound the parent seed-spec RESULTS.md names in its own §5 (independence assumed;
strategy-class not any construct; eval-clearance ≠ edge; single-tier only) — none of those are
re-litigated or re-measured here.

## Files

`run_polfront.py` (frozen-grid runner; reuses `max_risk` unmodified for the control arm) ·
`OPERATIONALIZATION.md` (grid resolution + sweep-range amendment, both pre-read) ·
`out/polfront_results.json` (full 30-cell raw output incl. quantized + stress arms) · seed-spec
harness recovered working-only (not re-committed; the Great Prune stands).
