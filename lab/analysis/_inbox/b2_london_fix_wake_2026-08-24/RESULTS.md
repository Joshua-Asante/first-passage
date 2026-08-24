# B2.2 placebo/orthogonality battery — London-fix wake (6E, 6B)

**Slug:** `b2_london_fix_wake_2026-08-24`
**Task:** B2.2, Lane B2, [`Phase B mechanism supply`](../../../../docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md)
**Task-level writeup:** [`docs/notes/research/2026-08-24-phase-b-lane-b2-placebo-battery-results.md`](../../../../docs/notes/research/2026-08-24-phase-b-lane-b2-placebo-battery-results.md)
(the plan-facing narrative, disposition, and runnable Verification section live there — this
file is the harness's own detailed numeric record)
**Harness:** [`run_b22_placebo_battery.py`](run_b22_placebo_battery.py) · raw log [`run_output.txt`](run_output.txt)
**Status:** CLOSED — B2.2 battery: 6E and 6B both DEAD via orthogonality (|t|<2/wrong-signed); placebo leg decisive only for 6B (rank 4.9)
**Date:** 2026-08-24

---

## Mechanism under test

Benchmark-mandated fix flow (10:58–11:04 ET cluster) creates dealer inventory whose normalization
is faded 11:10–13:00 ET; sign read from the mechanically-defined fix-window impulse. Full mechanism
provenance: [`N-2026-08-24-b2-london-fix-wake-cost-arithmetic.md`](../../../../docs/notes/notice/N-2026-08-24-b2-london-fix-wake-cost-arithmetic.md) §4.

## Data

Databento GLBX.MDP3, continuous `.v.0` (volume-rolled), 2024-08-24→2026-08-24 (2 years), 6E and
6B. Both schemas Rule-1 dry-run confirmed **$0.0000** before pulling:

| Schema | Records | Billable bytes | Cost | Use |
|---|---|---|---|---|
| `ohlcv-1h` | 23,619 | 1,322,664 (~1.3MB) | $0.0000 | controls + hourly-clock placebo family |
| `ohlcv-1m` | 1,337,317 | 74,889,752 (~75MB) | $0.0000 | precise 10:58–11:04 impulse + 11:10 entry anchor |

Roll integrity confirmed per-symbol: `instrument_id` shows 9 distinct contracts over the 2-year
span for each symbol, each holding ~1,140–1,492 hourly bars/quarter (a clean quarterly Mar/Jun/Sep/
Dec roll cadence) — no dead-contract undercounting artifact of the `.c.0` kind (`6J.c.0` 2021-09
precedent: 335 vs 734 expected). The `symbol` alias column was **not** trusted for this (per repo
lesson); `instrument_id` was.

## Clock-resolution design

Hourly bars cannot resolve the literal 6-minute 10:58–11:04 ET cluster (it straddles the
10:00–11:00 and 11:00–12:00 hourly bars). Escalated to `ohlcv-1m` for the impulse + entry anchor
(own Rule-1 estimate run before pulling, confirmed $0.0000 above):

- **PRIMARY (precise):** impulse = open(11:04 1m) − open(10:58 1m); target = open(13:00 1m) −
  open(11:10 1m). This is the primary point estimate and feeds the decisive orthogonality
  regression.
- **ROBUSTNESS (hourly-proxy):** impulse ≡ `prior_hour_return` = open(11:00h) − open(10:00h);
  outcome = open(13:00h) − open(11:00h). Identical to the `prior_hour_return` control (so it
  cannot also serve as the orthogonality regression's own regressor — perfect collinearity); used
  only for the placebo-comparable statistic and as a sign/magnitude cross-check on the precise
  version.

CME Globex daily halt (16:00–17:00 CT = 17:00–18:00 ET) confirmed empirically: the `h17` hourly
column is absent for **all 624** ET calendar dates in the panel — a genuine, consistent daily
halt, not a data gap. This is why placebo candidate hour 14 (whose +3h outcome-end needs `h17`)
was dropped from the candidate menu (6 candidates used, not 7).

## Panel sizes

| Symbol | ET calendar dates in range | Valid fix-observations | Degraded-quality days (included) |
|---|---|---|---|
| 6E.v.0 | 624 | 469 | 2 |
| 6B.v.0 | 624 | 447 | 2 |

## Step 3 — mean 11:10–13:00 ET return conditioned on impulse sign (not pooled)

| Symbol | impulse UP: n / mean_target / t | impulse DOWN: n / mean_target / t | R_precise mean / t | R_hourly mean / t |
|---|---|---|---|---|
| 6E.v.0 | 224 / −0.000110 / −1.27 | 245 / +0.000024 / +0.24 | +0.000065 / +0.97 | −0.000030 / −0.43 |
| 6B.v.0 | 217 / +0.000079 / +0.69 | 230 / −0.000179 / −1.64 | −0.000131 / −1.65 | −0.000094 / −1.09 |

`R_precise`/`R_hourly` = strategy-signed return (fade the impulse: `-sign(impulse)*target`).
Neither symbol's fade PnL clears even a bare `|t|≈2` on its own, before any control or placebo is
applied. **6E's precise and hourly-proxy point estimates disagree in sign** (+0.000065 vs
−0.000030) — a real fragility signal: a genuine mechanism should not flip sign under a ~10-minute
clock perturbation (11:00 vs 11:10 entry). 6B's two clock versions agree in sign (both negative =
fade loses / momentum, not reversal) — internally consistent, but consistently **wrong-signed**
against the fade hypothesis. (This same 6E sign-fragility resurfaces in the placebo-rank comparison
below, Step 4b: the minute-resolution null ranks 6E's *positive* `R_precise` far higher than the
hourly null ranks its *negative* `R_hourly`.)

## Step 5 — orthogonality regression (decisive gate)

`target_precise ~ 1 + trailing_vol + prior_hour_return + imp_sign` (adapted from the gamma-family
precedent's `partial_out_t`, sign-flipped: this lane is a reversal/fade hypothesis, so the correct
sign is **negative**, vs. the precedent's momentum-continuation `coef>0`).

| Symbol | Model A: bare imp_sign t | Model B: prior_hour_return t (generic-reversal baseline) | Model C: imp_sign coef | Model C: imp_sign t | corr(imp_sign, prior_hour_return) | Orthogonal? |
|---|---|---|---|---|---|---|
| 6E.v.0 | −1.00 | +0.27 | −0.000060 | **−0.90** | −0.017 | NO (\|t\|<2) |
| 6B.v.0 | +1.63 | +0.34 | +0.000130 | **+1.63** | −0.009 | NO (wrong sign AND \|t\|<2) |

6E: correctly signed (negative) but far short of `|t|≥2`. 6B: wrong-signed (positive = momentum,
not fade) regardless of magnitude. Robustness (excluding the 2 degraded-quality days per symbol)
leaves both numbers materially unchanged (6E: t=−0.92 vs −0.90; 6B: t=+1.64 vs +1.63).

## Step 4/4b — placebo null (1,000 replicates each; two clock resolutions)

Candidate anchor hours (ET): 06,07,08,09,12,13 — identical menu for both resolutions. Each
replicate draws an i.i.d. random anchor-hour offset per trading day, applied to the **same**
day-set as the real sample — day-of-week and trailing-vol composition are matched **by
construction** for both resolutions (verified below, not merely assumed; the check depends only on
the shared per-day index/offset-sampling mechanism, not on which `R` matrix is sampled, so one
check covers both).

**Step 4 (original) — hourly-proxy null:** `R_hourly` (built from `ohlcv-1h` bars) ranked against a
placebo null also built from `ohlcv-1h` bars. **Step 4b (added on adversarial review of the first
B2.2 pass) — minute-resolution null:** the decisive orthogonality leg (Step 5) scores
`target_precise`, built from `ohlcv-1m` bars — but Step 4 ranked that leg's real-world counterpart
(Step 3's `R_precise`) against a coarser `R_hourly`-based null. That mismatch was disclosed as a
design choice (comparability with the hourly-only candidate menu), not silently assumed, but a
same-resolution test was feasible since the 1-minute panel was already pulled and had not been run.
Step 4b replaces the hourly-bar placebo construction with the literal minute-offset structure of
the real window (−2min/+4min impulse, +10min/+2h00m outcome) at each of the same 6 candidate
anchor hours, using `ohlcv-1m` opens throughout — so `R_precise`'s own mean is now ranked against a
matched-resolution null. **Step 4b is the decisive placebo comparison as of this revision; Step 4
is retained as a documented cross-check, not removed or silently dropped.**

| Symbol | Resolution | real stat mean | null mean | null p60 | real rank in null (pctile) | Kill (real ≤ p60)? |
|---|---|---|---|---|---|---|
| 6E.v.0 | 4b minute-resolution — **decisive** | +0.000065 | +0.000035 | +0.000051 | 67.1 | **NO** |
| 6E.v.0 | 4 hourly-proxy — cross-check | −0.000030 | +0.000036 | +0.000054 | 20.9 | YES |
| 6B.v.0 | 4b minute-resolution — **decisive** | −0.000131 | +0.000013 | +0.000035 | 4.9 | YES |
| 6B.v.0 | 4 hourly-proxy — cross-check | −0.000094 | +0.000086 | +0.000113 | 3.9 | YES |

**6E's placebo leg flips under the matched-resolution test.** The coarse hourly-proxy null (Step 4)
ranks 6E's real statistic at the 20.9th percentile — kill-eligible. The minute-resolution null
(Step 4b), matched to the same clock resolution as the decisive orthogonality leg, ranks it at the
67.1th percentile — **clears** the 60th-percentile bar. This is the same sign-fragility already
flagged in Step 3 (6E's precise vs hourly-proxy point estimates disagree in sign, +0.000065 vs
−0.000030) propagating into the placebo-rank space — not a new or independent anomaly, and not a
result any subset/direction search produced (both nulls apply the identical pre-specified
construction to the identical whole sample). **It does not change 6E's overall verdict**: the
frozen kill criterion is an OR of two legs, and 6E's orthogonality leg (Step 5) independently fails
on its own (`|t|=0.90 < 2`, computed identically before and after this revision — unaffected by
the placebo-resolution change). It does mean 6E's DEAD verdict now rests on the orthogonality leg
**alone**, not on two independently-corroborating legs, which the first B2.2 pass's "both legs
fail independently" framing overstated for this symbol. 6B's placebo leg is unaffected in
direction by the resolution change — both nulls kill it (4.9th and 3.9th percentile) — so 6B's DEAD
verdict remains corroborated by both legs at both clock resolutions, the more robust of the two
symbols' kills.

Both Step-4 (hourly) real statistics, and 6B's Step-4b (minute) real statistic, sit **below the
respective null's own median** (p50), let alone its 60th percentile — 6B's real statistic is worse
than 96.1% of hourly-resolution placebo draws and 95.1% of minute-resolution placebo draws. The
placebo null itself being centered comfortably above zero at hourly resolution (mean
+0.000036/+0.000086) — and near zero at minute resolution (mean +0.000035/+0.000013) — is a
genuine finding: some form of generic "fade the last window's move" pattern has positive-or-near-
zero gross expectancy at *various* clock times in this 2-year 6E/6B panel. For 6B the fix-specific
clock is not merely unremarkable against that backdrop, it *underperforms* the generic version at
both resolutions; for 6E's Step-4b null the real statistic sits above the null's own median, inside
the ordinary range of the generic pattern rather than below it. (Caveat: `ohlcv-1m`/`ohlcv-1h` bar
opens are trade prints, not midpoints — per the databento-data skill's own data-hygiene note, part
of this generic-reversal magnitude could be bid-ask-bounce microstructure rather than pure economic
mean reversion; the measured effect sizes here, ~$0.00001–0.00013 across both resolutions, are the
same order of magnitude as a single tick, 0.00005. This does not change 6B's kill verdict — a
mechanism that cannot even clear microstructure-noise-scale placebo variation is dead either way —
but it means the "generic reversal exists and is economically real" framing should not be
over-claimed.)

**Verification (placebo day-of-week + trailing-vol match):** confirmed for both symbols — max
day-of-week frequency deviation ≤0.2pp, trailing-vol quartile relative deviation ≤0.3% (see
`run_output.txt` for the full per-weekday table). One check covers both resolutions (see above).

## Frozen kill criterion

> "Kill if the fix dummy adds nothing over generic reversal or sits ≤ placebo 60th percentile."

The placebo leg below uses Step 4b (minute-resolution, decisive); Step 4 (hourly, cross-check) is
shown in the Step 4/4b table above. Both legs still fail independently for **6B**; **6E** is now a
single-leg kill (orthogonality only) — the frozen criterion's OR still kills it, but this is a
materially different (weaker, single-leg) finding than the first B2.2 pass reported for 6E, and is
disclosed as such rather than restated unchanged:

| Symbol | Orthogonality leg | Placebo leg (4b, decisive) | Verdict |
|---|---|---|---|
| 6E.v.0 | FAIL (\|t\|=0.90 < 2) | PASS (rank 67.1 > 60) | **DEAD** (orthogonality leg alone) |
| 6B.v.0 | FAIL (wrong sign, \|t\|=1.63) | FAIL (rank 4.9 ≤ 60) | **DEAD** (both legs) |

## What was deliberately not done

No post-hoc subset/direction search for a rescuing cut (e.g., "maybe it only works on impulse-up
days," or a different placebo-hour menu) was run after the whole-sample test failed. Per repo
discipline (`lesson_snag_best_of_k_anchor_graveyard`, `feedback_adversarial_review_before_ratification`),
hunting for a surviving cut after a pre-specified test kills the whole sample is exactly the
degenerate move the frozen kill criterion exists to foreclose.

6E's Step 4b placebo leg clearing the bar (above) is **not** treated as grounds to reopen or
re-litigate the verdict, run a third placebo resolution, or search for a cut where both legs pass —
the frozen criterion is an explicit OR of two legs, one failing leg is sufficient by its own text,
and 6E's orthogonality leg fails on a computation this revision left untouched. Reporting the
single-leg nuance honestly (rather than silently re-asserting "both legs fail" for 6E) is disclosure,
not an invitation to keep searching until some cut clears both legs at once.

## Verification

```bash
# Reproduce the pulls (both Rule-1 dry-run $0.0000; cache-hit if already pulled on this machine)
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
    --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1h --start 2024-08-24 --end 2026-08-24
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
    --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1m --start 2024-08-24 --end 2026-08-24
PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
    --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1h --start 2024-08-24 --end 2026-08-24 \
    --max-cost 0.01 --out lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/data/6E_6B_ohlcv1h_2y.parquet
PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
    --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1m --start 2024-08-24 --end 2026-08-24 \
    --max-cost 0.01 --out lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/data/6E_6B_ohlcv1m_2y.parquet

# Run the battery (reproduces run_output.txt byte-identically -- fixed SEED=20260824)
python lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/run_b22_placebo_battery.py

# Roll-integrity spot-check (instrument_id, not the symbol alias, per repo lesson)
python -c "
import pandas as pd
df = pd.read_parquet('lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/data/6E_6B_ohlcv1h_2y.parquet').reset_index()
for sym in ['6E.v.0','6B.v.0']:
    sub = df[df['symbol']==sym]
    print(sym, sub['instrument_id'].nunique(), 'distinct contracts over the 2y span')
"
```
