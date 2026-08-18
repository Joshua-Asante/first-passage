# Q-POLFRONT-1 — intraday-honest remeasurement, frozen operationalization

**Fork executed:** [closure §7](../../../../docs/briefs/closures/Q-POLFRONT-1-closure-resolved-quantified.md#7--fork-named-not-opened)
— "Re-run the policy arm ... on an intraday-honest clock (same discipline as the W1 ADR /
`RESULTS_INTRADAY_W1.md` precedent for the book), to learn how much of the 5.1× ratio survives."
**Authorized:** operator GO, 2026-08-17 ("GO on item 1, open the intraday-honest remeasurement").
**Written BEFORE any intraday-honest bust number is computed** — same discipline as
`OPERATIONALIZATION.md` (this camp's own parent freeze) and the W1 ADR itself.

## §0 — Rule-0 reads (this session)

| Path | Anchor | Supplies |
|---|---|---|
| [`run_polfront.py`](run_polfront.py) | worktree HEAD | The frozen grid/arms this remeasurement re-scores; `simulate_policy`'s `day_low = min(cum.min(axis=1),0)` architecture, identical in shape to W1's `intraday_low` injection point |
| [`OPERATIONALIZATION.md`](OPERATIONALIZATION.md) | worktree HEAD | The existing `stress=True` (×2 day_low) arm is explicitly labeled "a stylized proxy... does not feed §4's verdict" — confirms this fork exists because that proxy was never meant to be load-bearing |
| [`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_w1_intraday_both_halves.py`](../class_s_c1_haircut_regime_remc_2026-07-16/run_w1_intraday_both_halves.py) | worktree HEAD | W1's actual method: `_leg_daily_excursion` derives, per real trade, the day's worst MTM point **below that day's own opening mark** from 15m bars, ET-localized, clipped ≤0 — the technique this fork generalizes |
| `core/data/bar_data/MYM_M15.csv` | SHA256 `24e169528f7...` matches `core/data/bar_data/SHA256SUMS` | Real, on-hand, already-used-by-W1 15m panel (141,477 rows, 2020-07-01→2026-07-02 ET) — the only real intraday panel present in this worktree; reused, not re-pulled |
| `git show pre-prune-2026-08-08:lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/run_seed_spec.py` | tag `pre-prune-2026-08-08` | `ROPE=3000.0 · TARGET=6000.0 · MIN_DAYS=3 · CONSIST=0.40 · EVAL_BUST_CEILING=3.0 · PASS_FLOOR=50.0 · HORIZON_BDAYS=1500` — cross-checked against **production** `core/firm_rules.py::Tradeify_Select_100K` (`max_dd_pct=3.0`, `profit_target_pct=6.0`, `min_trading_days=3`, `consistency_rule_pct=40.0`) — exact match, no drift |

**Why a new panel-derivation, not a literal W1 port:** W1's method needs a specific book's real
trade timestamps (entry/exit) to place each trade's MTM path on the bar timeline. Q-POLFRONT-1
tests candidate-independent `(w,b,r,k)` geometry with no trade timestamps at all — there is no
book to port. The closure's own §7 text anticipates this ("same discipline... for the book" —
not "same code"). The generalization below extracts the **session-level shape** of real
intraday excursion (how much deeper a session's low goes relative to its net close-to-open
move) from real MYM bars, and injects that shape onto the synthetic day-loop's outcomes —
the same architectural injection point (`day_low`, pre-breach-test) W1 used, fed from a
different (necessarily panel-only, not trade-only) derivation.

## §1 — Method (frozen)

**Session excursion-deepening ratio**, computed once from `MYM_M15.csv` (ET-localized,
grouped by calendar day — matching W1's own `_load_bars` convention):

```
open  = session's first bar open
close = session's last bar close
low   = session's min(low)
net     = close - open
low_exc = min(0, low - open)          # ≤ 0 by construction
ratio   = low_exc / net               # only where net != 0
```

Split by sign of `net`:
- **`LOSS_RATIOS`** (net < 0): by construction ≥ 1.0 — "how much deeper the session traded,
  relative to its own net loss, before closing."
- **`WIN_RATIOS`** (net > 0): by construction ≤ 0.0 — "how far the session dipped below open,
  relative to its own net gain, before recovering."

**Instability found and fixed before any grid number is read (same discipline as this camp's own
sweep-range amendment):** raw ratios explode for near-zero-`net` sessions (max loss_ratio 171×,
min win_ratio −309× on the raw 1,867-session pull) — an artifact of dividing by a small
denominator, not a real signal. **Fix: winsorize both distributions at the 2.5th/97.5th
percentile** (`loss_ratio ∈ [1.027, 13.782]`, `win_ratio ∈ [−24.233, −0.004]` on this panel) —
a standard, disclosed bound, not a per-cell fit. Winsorizing preserves the full session count
(no session is dropped) and preserves genuine tail shape up to the disclosed bound.

**Injection (replaces the existing `stress=True: day_low × 2` proxy for this arm only; the
original ×2 proxy stays in `run_polfront.py` untouched — this is an additional, separate arm):**
for each simulated (path, business-day) with synthetic `day_pnl` already computed by the
existing loop:

```
if day_pnl < 0: ratio_sample = draw from winsorized LOSS_RATIOS
if day_pnl > 0: ratio_sample = draw from winsorized WIN_RATIOS
if day_pnl == 0: no adjustment
day_low_real  = day_pnl * ratio_sample
day_low_final = min(day_low_synthetic, day_low_real)   # deeper of the two wins
```

`day_low_final` replaces `day_low` in the existing breach test
(`breach = min(pf + day_low_final, pf + day_pnl) <= floor`) — same formula, same injection
point as `simulate_policy`/`simulate_flat_stress` already use for the crude stress arm.

**Sampling:** one independent draw per (path, business-day) per arm, `np.random.default_rng`
seeded separately from the CRN seed (101) used for the win/loss draws themselves — the ratio
draw is a nuisance/measurement dimension, not part of the (w,b,k) outcome being measured, so it
does not need to share seed with the control-vs-policy comparison. Seed = **4177** (arbitrary,
fixed, disclosed; not tuned against any result).

## §2 — Scope (frozen, not a re-sweep)

**Re-evaluate only, at each cell's already-found `R_max` (both arms) from the original
Q-POLFRONT-1 run** — no new sweep, no new admissibility search. This directly answers the
closure's own question ("how much of the 5.1× ratio survives") without opening a new K/search
surface. `R_max` values are **recomputed fresh in this worktree** (the original
`out/polfront_results.json` was not committed) using `run_polfront.py`'s own frozen
`max_risk_flat`/`max_risk_policy` logic, same seed (101), same `n_sims=6000` — and
**fidelity-checked** against two anchors RESULTS.md already published
(`(w=0.55,b=2.0,k=1)`: R_flat=$350, R_policy=$1,825) before any new number is trusted.

**Grid:** identical 30-cell frozen grid (10 `(w,b)` pairs × `k∈{1,2,4}`), unchanged.

**Output:** per cell — `bust_intraday_honest_flat`, `bust_intraday_honest_policy`, deltas vs
each arm's own EOD-clock bust at that same R, and a side-by-side vs the existing crude ×2 stress
deltas (+1.63pp flat / +55.2pp policy median) already on record.

## §3 — What this does NOT do

- Does not re-open §4/§5/§6 of the frozen Q-POLFRONT-1 brief (byte-unedited).
- Does not re-sweep for a new R_max under the intraday-honest clock — that is a *further*,
  not-yet-opened fork (a genuinely intraday-honest admissible frontier would need its own
  sweep; this measurement only tests survival of the already-claimed EOD-clock frontier).
- Does not read this as an admission, a candidate, or a WATCH-rung change (inherits the parent
  brief's §5 forbidden-move class).
- Does not touch `core/`, `dd_protection.py`, or any locked/allocation constant.
- Does not commit `MYM_M15.csv` or any gitignored vendor byte — only the derived winsorized
  ratio arrays (small, non-vendor, derived numbers) land in the committed artifact.

$0 spend · K=0 · panel already on hand (no pull) · measurement only.

---

## §4 — v1 executed 2026-08-17; INVALIDATED same session (unit-conflation defect caught pre-report)

**Result of v1 (as designed above):** fidelity gate PASS (`(0.55,2.0,k=1)` reproduced $350
flat / $1,825 policy exactly). But every grid cell then showed bust collapsing to **75–99%**
under the real-bar injection — for **both** arms, including the flat arm, which the existing
crude ×2 stress test had shown was barely sensitive (+1.63pp median). Full row-by-row output:
`out/polfront_intraday_honest_results.json` (retained for the record, **not** a usable finding
— see below).

**Diagnosed before write-up, not after (adversarial self-check on an implausible result):** the
magnitude was implausible on its face — a *median* ratio of 1.65× should not produce near-total
collapse when the existing ×2 stress arm (a strictly larger deterministic multiplier on the
*same* k=1 cells, where `day_low_synth == day_pnl` exactly, so ×2 stress applies directly to
`day_pnl` too) showed mild degradation. Root cause: **`ratio` was derived as a property of the
*instrument* (MYM's own intrabar range relative to its own net daily move, in raw index
points) and then applied directly to `day_pnl`, a *strategy-defined*, R-denominated quantity
with no natural relationship to the instrument's raw point range that session.** These are not
commensurable — multiplying them conflates "how far does MYM wiggle in points" with "how far
does a stop-sized synthetic trade wiggle in R," which have no fixed ratio to each other. A
second, compounding effect: independently redrawing `ratio` **every simulated business day**
over a 1,500-day horizon × 6,000 paths (~9M day-draws) means tail values near the winsorized
bound get sampled often enough to dominate bust outcomes — a resampling-saturation effect the
deterministic ×2 stress arm never had to contend with.

**Why this is not merely "a stricter finding":** W1's actual method avoids exactly this trap —
it derives per-day excursion **in the specific real trade's own realized-P&L scale**
(`mtm_at`, interpolating between that trade's entry/exit price and its realized `pnl_scaled`),
never in raw instrument points. A faithful port needs an R-relative (stop-normalized) MAE
distribution, not an instrument-price-shape ratio. The only real, already-measured source of
that in this estate is W1's own per-trade excursion series (Striker/NAS100 legs, real stops,
real fills) — but the raw per-day series is not persisted (only aggregate `exc_sum`/`exc_min`
land in `w1_intraday_both_halves_report.json`), and the underlying trade CSVs
(`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/inputs/`) are gitignored vendor/locked
data **not present in this worktree** (confirmed: only `.gitignore`/`*.md` files exist there,
matching the established worktree-lacks-vendor-bytes pattern from the six-lead pursuit CF).

**Status at v1 discharge:** fork remained OPEN. v1's numbers were not cited, quoted, or carried
into any campaign prereg. Two live paths were named, neither taken without a fresh steer: (a)
re-run from the primary checkout where the Striker/NAS100 trade CSVs are on hand, deriving a
genuinely R-relative MAE distribution the way W1 did; or (b) design a v2 that avoids needing
real trade data at all. Operator elected (a).

---

## §5 — v2 executed (primary checkout); INVALIDATED same session (resampling-saturation, caught before write-up)

**⚠ Documentation-discipline note, disclosed honestly rather than silently repaired:** this §5
and §6 were **not** written before v2/v3 were run, breaking this file's own "written BEFORE any
bust number is computed" discipline one layer down from the parent brief's Trap #12 — the design
moved from v1 → v2 → v3 in rapid same-session iteration (each triggered by the previous attempt's
own diagnosed failure) faster than the freeze-then-run discipline was re-applied. Caught by the
2026-08-17 adversarial-verification pass (doctrine-scope lens), not self-caught. Recorded here
**post-hoc, dated as such** — this is the honest repair (document what was actually run, when),
not a backdated pretense of prior registration. The upstream code
(`run_polfront_intraday_honest.py`'s `_inject_real_excursion` docstring) cited "v3 (frozen,
OPERATIONALIZATION_INTRADAY_HONEST.md §5)" before this section existed; that citation is now true.

**Method:** switched to the primary checkout (`C:/Users/joshu/multi_firm_operations`, real trade
CSVs on hand under `core/data/tv_exports/cme/`) and re-derived a genuinely **R-relative** ratio:
reused W1's own `_leg_daily_excursion`/`_paired_trades_scaled` (imported, not re-derived) against
the REAL Striker DJ30 (MYM, 267 trades) and Striker NAS100 (MNQ, 284 trades) trade histories,
pairing each real trading day's bar-derived worst MTM excursion against that **same** day's own
realized scaled P&L — both quantities in the same dollar-scaled units, fixing v1's points-vs-
dollars conflation. Pooled both legs (230 loss-day observations, 173 win-day), winsorized at
2.5/97.5th percentile (`loss_ratio_clip=[-0.000,51.55]`, `win_ratio_clip=[-46.13,0.00]`),
**independently resampled** one ratio draw per simulated business day (matching v1's sampling
scheme, now with correct units). Script: `derive_real_mae_ratios.py` (run from the primary
checkout only — needs gitignored vendor trade CSVs; temporarily restored the two pruned harness
files `run_class_s_c1_scoring.py`/`run_class_s_c1_regime_gate.py` from
`git show pre-prune-2026-08-08:...` into the primary checkout to reuse `run_w1_intraday_both_halves.py`'s
imports unmodified, deleted them after use — the sanctioned Great Prune recovery pattern, verified
by adversarial review not to leave vendor bytes or restored files behind in either checkout).

**Result: INVALIDATED, same session, before any write-up.** Every grid cell collapsed to 75–99%
bust for **both** arms uniformly — including the flat arm, which the original crude ×2 stress
arm had shown was barely sensitive (+1.63pp median). That divergence was the tell.

**Diagnosis: resampling-saturation.** Even with correct units, the pooled ratio distribution is
heavy-tailed (winsorized loss up to 51.55×, win down to −46.13×; median only 1.389×/−2.049×).
Independently redrawing this distribution **every simulated business day** over a 1,500-day
horizon × 6,000 paths (~9M draws) means near-tail values get sampled often enough that almost
every simulated path eventually hits one — at these R levels (many cells' R_max sits within a
few multiples of ROPE=$3,000), a single near-tail draw single-handedly breaches regardless of
`(w,b,k)`. A deterministic ×2 (the original crude stress arm) has no such saturation channel;
an i.i.d.-resampled heavy-tailed distribution does. This is a distinct defect from v1's — v1 was
a units error, v2 was a sampling-design error — and both were caught by the same discipline: an
implausible, uniform, arm-insensitive result triggering a stop-and-diagnose before write-up.

---

## §6 — v3 executed; adversarially verified 2026-08-17; landed as this fork's finding

**Method (frozen, retroactively, per the §5 note above):** same real, R-relative ratio source as
v2, but **deterministic** instead of resampled — the empirical **median** of each sign-split
distribution (`loss_mult=1.389`, `win_mult=−2.049`) applied identically to every simulated
business day: `day_low_real = day_pnl × mult`; `day_low_final = min(day_low_synth, day_low_real)`
(deeper of the two wins), replacing v1/v2's resampling entirely. A secondary **P90 stress arm**
(`loss_mult=4.141`, `win_mult=−13.620`) is computed for context, not as the primary finding.
Re-evaluated only at each cell's already-found EOD-clock `R_max` (no re-sweep — same scope
discipline as §2 above).

**Result:** median flat-arm bust delta **+18.0pp** (range 0.61–98.47pp, monotonically worse as
`R_max` approaches `ROPE`); median policy-arm delta **+98.1pp** (near-uniform collapse). Only
**2/24** flat cells and **1/26** policy cells still clear the frozen 3.0% ceiling. Full table:
[`RESULTS_INTRADAY_HONEST.md`](RESULTS_INTRADAY_HONEST.md).

**Adversarial verification (2026-08-17, 4 reviewers + synthesis + a re-run on connection
failure):**
- **Code-correctness: CLEAN.** Byte-faithful vs the recovered `run_seed_spec.py`/`run_polfront.py`
  logic; injection sign arithmetic verified correct on both loss and win days; no leakage of the
  injected excursion into the pass/consistency gates. One cosmetic dead parameter (`inactivity`
  on `simulate()`, zero behavioral effect) — harmless, not fixed (matches the recovered source's
  own signature; removing it would diverge from the reused reference unnecessarily).
- **Independent reimplementation: strong corroboration.** A fresh, from-scratch implementation
  (never read this file's actual code) reproduced both target numbers closely (flat 26.87% claim
  vs 27.4–28.1% reproduced across 5 seeds and a 5×-larger sample; policy 100.00% reproduced
  **exactly** in every seed and two alternative day-loop reinterpretations tried) and derived a
  **closed-form proof** that the policy-arm collapse is a near-mathematical certainty, not an MC
  artifact: any winning day breaches once `r_base > ROPE / (|win_mult| × b)` — for `(w=0.55,
  b=2.0)` that threshold is ≈$732, and the claimed `R_policy_max=$1,825` sits **2.5×** over it,
  independent of current drawdown level. Two minor notes: the design doc alone under-specifies
  the day-loop mechanics (self-contained by cross-reference to `run_polfront.py`, per this repo's
  pointer-not-retelling convention — judged intentional, not a defect); the exact consistency-rule
  reconstruction swings the **EOD** fidelity-anchor ~24pp relatively (1.67–2.50%) without moving
  either intraday-honest headline number at all.
- **Methodology/units (re-run once after a connection failure): two CONFIRMED biases, both
  pushing the same direction.**
  1. **Pyramiding contamination (dominant).** `mtm_at()` (inside the reused `_leg_daily_excursion`)
     applies one constant $/point rate — calibrated to the trade's *final, pyramid-inflated*
     `pnl_scaled` — across the **entire** price path, including the early pre-pyramid low where
     the account actually carried only base size (Striker pyramids up to 750%/1000% on continued
     favorable movement, i.e., pyramid adds land **late** in a winning trade's life). This
     retroactively inflates the measured dollar excursion at the point where a smaller position
     was actually on. In-repo corroboration: NAS100's base-only (non-pyramided) PF is 0.31 — the
     edge is structurally inseparable from pyramiding in this trade record, so no clean
     "fixed-1R" reading of these specific real trades exists to fully correct this. **Specifically
     inflates the win side — `win_mult=−2.049` is very likely an overstatement of the true
     fixed-size risk a non-pyramided synthetic trade would show.**
  2. **Multi-trade-day additive summing.** Roughly half of the 267/284 real trades share an exit
     day with a second, independently-timed trade (197/206 distinct trade-days). `_leg_daily_
     excursion` sums each trade's own dip (measured from its own entry) additively into one
     day-level `exc` — a reasonable simplification for W1's original book-level daily-low feed,
     but it overstates the true combined-equity worst point once repurposed as a per-day ratio
     numerator (two trades' individual worst moments rarely coincide exactly). **Inflates both
     ratios' magnitudes, pushing the finding harsher.**
  3. Two of four adversarially-posed concerns were investigated and **refuted**: unit consistency
     is clean (`exc/day_pnl` is dimensionless — cancels any $200K/$100K or Striker-R-vs-
     Q-POLFRONT-1-R scale difference); the reference-point concern (excursion-below-open vs
     excursion-below-day's-own-zero) is moot — confirmed `n_overnight_holds: 0` for both legs
     across three independently-committed reports, so every trade is same-day and the two
     reference points coincide.

**Verdict: SAFE_WITH_CAVEATS (synthesis of all four reviews).** No coding-level defect found; the
qualitative finding (both arms fail far more than the crude ×2 stress arm suggested; policy is
dramatically more fragile than flat; the collapse has a closed-form mechanism, not just an
empirical one) is corroborated by an independent reimplementation. But **both surviving biases
push toward overstating risk, with no offsetting bias found** — so v3's numbers, especially
`win_mult=−2.049` and everything downstream of it, should be read as a **credible upper bound /
conservative proxy**, not a tight point estimate. A bias-corrected re-measurement was not
attempted this session (the pyramiding contamination may not be cleanly correctable from this
specific trade record at all, per the PF-0.31 finding above) — named as a further, unopened fork,
not resolved here.

**What this does not do:** does not re-open §4/§5/§6 of the frozen Q-POLFRONT-1 brief; does not
admit, demote, or re-rung anything; does not touch `core/`, `dd_protection.py`, or any locked
constant (confirmed by the doctrine-scope review — no vendor bytes or restored harness files
persisted in either checkout, no new sweep opened under the intraday-honest clock).

$0 spend · K=0 · panels/trade CSVs already on hand (no pull) · measurement only.
