# PREREG — `H-RANGESTATE-GC-1` (S1a): daily range-state persistence, GC train era

**Class:** Tier-1 mechanism screen, per [Step-0 slate](../../../../docs/briefs/2026-08-18-step0-daily-geometry-mechanism-slate.md)
§2 row S1a. Measurement only — no candidate is produced by any outcome.
**Date frozen:** 2026-08-18, committed **before** the runner reads a single real bar.
**Operator context:** GO'd this session ("GO S1a") off the Step-0 slate queue (§3: S1a first).
**Spend:** disclosed **K=1** (one frozen object). Data: GC.v.0 `ohlcv-1d`, priced **$0.0000** per
the [deep-iteration lane charter addendum](../../../../docs/adr/2026-08-16-deep-iteration-lane-charter.md)
(bar schemas on this exact triad/window already dry-run priced free) — estimate re-run and
pasted in §7 before any pull, per databento skill Rule 1. No manifest, no Cap seat, no lane K.

---

## §1 — Object (frozen; no variants)

**Instrument & window — train-only, confirm reserved.** Per the futures-anomaly-discovery Tier-1
screen discipline (train-era only; the native-micro era stays virgin for a future lane confirm):
`GC.v.0` (parent, volume-led continuous — the repo's established TV-`1!`-equivalent roll
convention; **not** `GC.c.0`, per [`MNQ.md` W1](../../../../ops/instruments/MNQ.md): "a wrong
continuous choice changes bar existence, not just levels") on `ohlcv-1d`, session-days
**2010-06-06 → 2019-01-01** (the estate's own `RATIFIED_IS_BOUNDARY`, reused verbatim from
`lab/databento_fetch/db_fetch.py`, not re-derived). `MGC.v.0` 2019-01-01→present stays
**unread** — reserved for a lane confirm if S1a/S1b/S2 signal.

**Roll-day exclusion (frozen).** A session-day is a roll day if its bar's underlying
`instrument_id` differs from the immediately preceding session-day's. `TR` is undefined
(excluded, not imputed) on any roll day — a raw-stitched continuous series carries a genuine
price-level jump at roll that is not a market-range event (ORB campaign precedent: "272
roll-window bars excluded as object origins", `orb_mnq_2026-07/RESULTS.md`). All subsequent
windowing (below) operates on the **filtered valid-`TR` sequence**, skipping excluded days
entirely rather than tolerating gaps at fixed calendar offsets — same convention `run_dstruct.py`
used for its EMA warmup index.

**True Range (Wilder's, frozen):** `TR_d = max(H_d − L_d, |H_d − C_{d-1}|, |L_d − C_{d-1}|)`,
`C_{d-1}` = the immediately preceding **valid** (non-roll-excluded) session's close.

**Bias (top-quintile persistence signal, no self-inclusion):**
`bias_d = 1{ TR_d ≥ P80(TR_{d-60} … TR_{d-1}) }` else `0` — the 80th percentile of the **strictly
prior** 60 valid `TR` observations (excludes `TR_d` itself from its own threshold, avoiding the
self-referential inflation a same-window threshold would cause).

**Outcome (elevated-range indicator, no lookahead):**
`y_{d+1} = 1{ TR_{d+1} > P50(TR_{d-59} … TR_d) }` else `0` — the median of the 60 valid `TR`
observations **through and including day d** (legitimate history relative to `d+1`; `TR_{d+1}`
itself never enters its own reference).

**Scored day (predicting `d+1` from `d`):** both rolling windows have their full 60 valid
observations, `TR_d`, `TR_{d+1}` both valid (non-roll-excluded).

**Verdict cell:** the **conditional** hit rate on the `bias_d = 1` (top-quintile) subset —
`gateHit = P(y_{d+1} = 1 | bias_d = 1)` — matching the frozen claim's explicit conditioning
(§2 below), not a bias-matches-outcome sign test (there is no "sign" here; range persistence is
one-directional by construction).
**Disclosure cell:** the unconditional `P(y_{d+1}=1)` across ALL scored days (both bias arms) —
expected ≈0.50 by construction of the median split; large deviation would itself be a
design-defect signal, checked in §7 before the verdict is trusted.

## §2 — Frozen claim (the slate's S1a row, operationalized)

`P(TR_{d+1} > trailing-median | TR_d in top quintile of trailing 60d)` exceeds its
block-shuffled null. Grounding: volatility-clustering (evidence-robustness limb — ARCH/GARCH
canon, five decades, every asset class), not a WHO claim specific to gold.

## §3 — Frozen limbs (PASS requires ALL FOUR, verdict cell only)

Same four-limb battery as `H-DSTRUCT-MNQ-1` (the established Tier-1 template):

1. **n-floor:** scored days (bias=1 subset) ≥ 100. (Lower than DSTRUCT's 400 because the
   bias=1 subset is itself ~20% of scored days by construction of the quintile cut — the
   *scored-population* floor is 400, same as before; 100 is the conditional-subset floor.)
2. **Block-bootstrap 95% CI lower bound > 0.50** on the bias=1 subset (**60-day** circular
   blocks, 4,000 draws, seed 42). ⚠ **Corrected 2026-08-18, before the trusted run** — the
   first draft copied DSTRUCT's 10-day CI-block convention unexamined; adversarial review (4-lens
   workflow) caught that this contradicts limb 4's own stated rationale below (bias is
   autocorrelated on the 60-day construction scale, so a 10-day block understates clustering and
   inflates the CI's apparent precision toward SIGNAL — confirmed by a live block-size sweep,
   monotonically falling lower bound from 0.4849 at block=1 to 0.4523 at block=120). Fixed to
   match `PL_BLOCK` before any number was quoted downstream. The review also caught that the
   bootstrap was implemented as a non-wrapping moving-block procedure despite being declared
   "circular" — fixed to genuine wraparound indexing in the same pass. Both corrections are
   verdict-preserving on this draw (still NULL) and directionally conservative (wider CI, lower
   bound moves further from 0.50, not toward it).
3. **Both halves > 0.50** (time-ordered split of the bias=1 scored days).
4. **PRIMARY — beats the clustering-preserving placebo:** observed conditional `gateHit` >
   p95 of 2,000 **60-day contiguous-block permutations of the full bias sequence** (order
   permuted, outcome sequence fixed; seed 7), each permutation's conditional hit rate recomputed
   on whichever days land `bias=1` after reshuffling. **60-day blocks are frozen deliberately at
   the persistence horizon itself** — bias is constructed from a 60-day trailing window, so it is
   autocorrelated on that scale; a shorter block would understate the null's own clustering and
   overstate significance (`lesson: block-shuffle time-clustered signals`).

**Verdict:** `SIGNAL` = all four limbs; `NULL` = any limb fails while the n-floor holds
(`Q-WLEGB-1` / `H-DSTRUCT-MNQ-1` precedent: naive limbs can pass on structure alone — here the
asymmetry runs the other way, see §7); `AMBIGUOUS` = population n < 400 **OR conditional n <
100**, or panel/roll defect.

## §4 — Predictions (frozen before compute)

- Unconditional `P(y=1)` expected in **[0.46, 0.54]** (near-exact median split; TR autocorrelation
  could nudge it either way through the roll-exclusion filter, but not by much). A reading
  outside this band is disclosed and investigated as a possible construction defect **before**
  the verdict is read (not a re-freeze — a defect check).
- `bias=1` share expected **[0.15, 0.25]** (top-quintile by construction, some slack from
  discrete 60-obs percentile granularity and roll exclusions).
- **No sign prediction stated for the verdict** (unlike DSTRUCT/WLEGB, which had strong adverse
  priors from adjacent kills) — this is a genuinely open screen; the evidence-robustness
  grounding (§2) argues for SIGNAL, the estate's dense graveyard of daily/intraday direction
  kills argues for caution but does not transfer (this is a **geometry** claim, not a direction
  claim — the two families have not yet had a comparable test on this instrument).

## §5 — Dedup & bar-adjacency (executed this session)

- `grep -niE "volatility.cluster|range.persist|true.range|GARCH|ATR" docs/rejected_candidates.md
  ops/instruments/MGC.md ops/instruments/MCL.md ops/instruments/MECHANISMS.md` → no daily
  range-persistence *conditioner* test on GC/MGC/MCL. `compression-gated-breakout` and
  `htf-compression-breakout-5m` (`MECHANISMS.md`) are **entry-role, index/MNQ-resident**
  constructs testing compression→expansion as a trade trigger — this screen tests range
  persistence as a **standalone geometric fact**, no entry attached, different instrument family.
  Not the same object; adjacency only.
- MGC ledger (`MGC.md`) DEAD table: `event-window-reversal` (direction/flow) — different
  mechanism class, no bearing.
- MCL ledger not consulted for S1a (this screen is MGC/GC-only; S1b is the separate MCL GO).
- No prior GC/MGC daily-TR-quintile-persistence test exists in `lab/CATALOG.md`, the discovery
  manifests, or any archived campaign.

## §8 — Adversarial verification (executed before the trusted run)

4-lens parallel workflow (lookahead/leakage, panel-integrity, statistics, prereg-fidelity) + a
synthesis pass, run against the frozen prereg text and the first-draft `run_s1a.py`, mirroring
this repo's own DL-1 precedent ("adversarially verified against the frozen prereg text... before
this run"). Lookahead/leakage — the highest-risk defect class — came back clean, independently
corroborated by an exact arithmetic identity (`n_scored = len(valid) - 61`, verified to match).
Two real issues surfaced and were fixed before any number was trusted: the CI block size (§3
limb 2, corrected above) and the roll/gap-census prose (corrected above). Synthesis verdict:
**FIX-THEN-RUN**, both fixes applied, verdict confirmed stable (NULL) under the corrected code.
Full transcript: workflow run `wf_7ad6ac61-126`.

## §6 — Forbidden moves

No second quintile cut (`P80`), window length (60d), or horizon (1-day-ahead) — that sweep is
the K this declaration excludes. No reading past 2019-01-01 (the reserved MGC confirm window).
No re-run with more placebo permutations on a near-miss. No promoting SIGNAL to a candidate —
routes to a deep-lane prereg per the charter's own §2 predicates, nothing here licenses a trade.
No quoting the conditional hit rate without the placebo comparison alongside it.

## §7 — Data pull record (filled at execution, before any bar is scored)

```
$ python lab/databento_fetch/db_fetch.py estimate --symbols GC.v.0 --stype continuous \
    --schema ohlcv-1d --start 2010-06-06 --end 2019-01-01 --phase discovery
[estimate] cost      : $0.0000 USD (streaming)
[estimate] billable  : 148,624 bytes  (~0.0001 GB)
[estimate] records   : 2,654
```

Confirmed $0.0000, matches the charter addendum's table. Pull authorized under the S1a GO
(slate §6 M-2: "Pull GOs ride the row GOs"). Pulled: 2,654 rows, `gc_1d.parquet`
(`instrument_id`/`symbol`/OHLCV, `ts_event` UTC-day index, 2010-06-07→2018-12-31).

**Step-0 panel-integrity battery (executed before any TR/roll computation, per
`strategy-validation` §1 — mandatory before metrics):**

- **Day-of-week census: phantom Sunday bars found — the standing
  `databento ohlcv-1d weekend bars` lesson, confirmed live.** 434 rows land on UTC weekday=6
  (Sunday) vs 448/446/445/446/435 on Mon–Fri; **zero** on Saturday. Sunday-bar median volume
  **2,753** vs Monday's **121,533** (2.3%) — thin partial-Globex-reopen bars, UTC-day-bucketed
  off the true Monday session per the lesson's own diagnosis. **Frozen fix (the lesson's own
  remedy, applied verbatim):** drop all `weekday ∈ {5, 6}` rows before any downstream
  computation — the real Monday trade date is carried by its own Monday bar; nothing real is
  lost. Post-filter: 2,220 rows, weekday census Mon 448 / Tue 446 / Wed 445 / Thu 446 / Fri 435,
  zero Sat/Sun.
- **Duplicate `ts_event`:** 0.
- **Nulls (O/H/L/C/volume):** 0.
- **Databento data-quality flag:** 2 "degraded" days per the stream warning (2014-06-11,
  2014-06-12). 2014-06-13 (Friday) was checked incidentally and is **not** flagged — see the gap
  census below, that row is in fact entirely **absent** from the panel, not present-but-unflagged
  (corrected 2026-08-18; the first draft conflated "absent" with "unflagged"). The two genuinely
  flagged days' volumes (72,510 / 113,840) sit inside the normal range — no visible OHLC anomaly.
  **Disclosed, not excluded**; the flag concerns top-of-book/quote quality, not OHLCV bar
  integrity, and 2 days cannot move a 2,220-day panel's verdict either way.
- **Roll-day census (`instrument_id` transitions, post weekend-filter, persisted to
  `s1a_results.json.roll_dates` — not hand-copied):** 42 roll days across
  2010-06-08→2018-12-31 (~4.9/year — consistent with gold's actively-traded contract-month
  cadence). First few: 2010-08-02, 2010-12-01, **2011-01-31**, 2011-03-31, **2011-05-30**.
  ⚠ **Corrected 2026-08-18** — the first draft hand-typed this list and got two of five dates
  wrong by one calendar day (2011-02-01/2011-05-31), despite claiming "not hand-copied"; caught
  by adversarial review, which also found the underlying mechanism: **~40% (17/42) of roll
  transitions occur over a weekend**, where the raw (weekend-included) census flags the
  transition on the phantom Sunday reopen bar (which already carries the new contract's
  `instrument_id`) — dropping that bar per the weekend-filter relocates the flag to the
  following Monday. This is the correct, expected behavior of the frozen fix (the `is_roll`
  mask itself was never wrong — only this prose example list was), now regenerated from the
  script's own output.
- **Gap-day census (missing trading days, ≥4 calendar days between adjacent panel rows,
  persisted to `s1a_results.json.gap_days_ge4_calendar`):** 13 gaps found. 12 match a
  recurring single-holiday-Friday-adjacent-to-a-weekend pattern (Good Friday ×6, Christmas
  Eve/Day, New Year's, and similar COMEX closures) and require no action — TR across a
  Thu→Mon holiday gap is computed the same way it always is for a normal weekend, since the
  weekend-filter already handles the calendar-day arithmetic. **One gap is qualitatively
  different and was missed by the first draft's Step-0 pass:** 2014-09-26 follows a 3-consecutive-
  weekday void (09-23/24/25, no weekend involved, the single largest data void in the panel) —
  TR on 09-26 is computed against 09-22's close (4 calendar / 3 trading days removed) with no
  flag, since `instrument_id` is unchanged across the gap (not a roll). **Materiality: at most
  13 of 2,177 valid TR observations (~0.6%) are gap-adjacent** — an order of magnitude under the
  n≥400 population floor and n≥100 conditional floor, disclosed rather than excluded. A future
  campaign reusing this template should extend `compute_tr_with_roll_exclusion` to NaN any TR
  whose `prev_c` is more than one valid trading day removed (symmetric with the roll-exclusion
  treatment) — not done here since the bounded materiality doesn't warrant a design change to a
  frozen object mid-campaign.
- **Date-span coverage:** matches the requested window exactly (2010-06-07→2018-12-31, no
  truncation).
