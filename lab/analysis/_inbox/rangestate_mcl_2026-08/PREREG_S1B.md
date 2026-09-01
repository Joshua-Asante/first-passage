# PREREG — `H-RANGESTATE-CL-1` (S1b): daily range-state persistence, CL train era

**Class:** Tier-1 mechanism screen, per [Step-0 slate](../../../../docs/briefs/programs/2026-08-18-step0-daily-geometry-mechanism-slate.md)
§2 row S1b. Measurement only — no candidate is produced by any outcome.
**Date frozen:** 2026-08-18, committed **before** the runner reads a single real bar.
**Operator context:** GO'd this session ("GO S1b") off the Step-0 slate queue, following
[S1a (GC) → `NULL`, near-miss](../rangestate_gc_2026-08/RESULTS_S1A.md) — placebo cleared
(p=0.0095), CI lower bound fell 4.55pp short. Per §4 there, S1b is a genuine replication
opportunity, not a blind re-test.
**Spend:** disclosed **K=1** (one frozen object, on a **different instrument** — S1a and S1b are
two separate single-instrument screens sharing one mechanism family per the slate's own §2
framing, each disclosed independently, not a shared K). Data: `CL.v.0` `ohlcv-1d`, priced
**$0.0000** (charter addendum). Estimate re-run and pasted in §7 before pull, Rule 1.

---

## §1 — Object (byte-identical to S1a — no parameter changed)

**This is a replication, not a redesign.** Every frozen constant below is copied verbatim from
[`PREREG_S1A.md`](../rangestate_gc_2026-08/PREREG_S1A.md) §1–§3 (the adversarially-verified,
corrected version). The only things that change are the instrument and its Step-0 panel facts.

**Instrument & window — train-only, confirm reserved.** `CL.v.0` (parent, volume-led continuous
— **not** `CL.c.0`, same roll-convention rule as S1a) on `ohlcv-1d`, session-days
**2010-06-06 → 2019-01-01**. `MCL.v.0` 2019-01-01→present stays **unread**.

**Roll-day exclusion:** identical mechanism to S1a — `instrument_id` transition vs the
immediately preceding valid session-day, `TR` undefined on the roll day, all windowing over the
filtered valid-`TR` sequence. **MCL.md's own W1 warning is directly engaged here and confirmed
live, not assumed:** MCL rolls **monthly** (vs GC's roughly-quarterly-active cadence) —
measured this session at **103 roll days over 2010-06-08→2018-12-31 (~12.0/year)**, roughly
**2.5× GC's 42 (~4.9/year)**. This is expected per W1 and disclosed, not treated as a defect.

**True Range, bias, outcome, verdict cell, disclosure cell:** identical formulas to
`PREREG_S1A.md` §1 (Wilder's TR; `bias_d = 1{TR_d ≥ P80(strictly-prior-60)}`;
`y_{d+1} = 1{TR_{d+1} > P50(through-today-60)}`; conditional `gateHit = P(y_{d+1}=1|bias_d=1)`).

## §2 — Frozen claim (identical to S1a)

`P(TR_{d+1} > trailing-median | TR_d in top quintile of trailing 60d)` exceeds its
block-shuffled null. Same evidence-robustness grounding (volatility clustering), now tested on
a second, unrelated commodity (energy vs metals) — the strongest form of replication this
program can cheaply run.

## §3 — Frozen limbs (identical to S1a, post-correction)

Same four-limb battery, same parameters: n-floor (population ≥400, conditional ≥100),
**60-day circular** block-bootstrap CI (4,000 draws, seed 42 — reusing the corrected S1a
convention from the start, not the original 10-day draft), both-halves, and the primary
**60-day contiguous-block placebo** (2,000 permutations, seed 7). Verdict taxonomy identical:
`SIGNAL` (all four) / `NULL` (any limb fails, n-floor holds) / `AMBIGUOUS` (either n-floor fails
or a panel/roll defect).

## §4 — Predictions (frozen before compute)

- Unconditional `P(y=1)` expected **[0.46, 0.54]** (same construction-driven near-median
  expectation as S1a; S1a measured 0.4778).
- `bias=1` share expected **[0.15, 0.25]** (S1a measured 0.2131).
- **Directional prediction, stated honestly given S1a's result:** S1a's placebo cleared
  decisively (p=0.0095) while only the CI-precision limb failed, by a modest margin (4.55pp).
  If the underlying mechanism is real and instrument-general, S1b should show a qualitatively
  similar shape (placebo clearing, conditional rate meaningfully above 0.50) — possibly clearing
  the CI limb too if MCL's larger `n_cond` (expect proportionally similar share, ~2,100 scored
  days after the heavier roll-exclusion) tightens the interval enough. If S1b instead shows no
  separation from its placebo, the S1a result is better read as this-instrument/this-window
  noise, not a generalizable mechanism. **This prediction is stated to bind the read, not to
  justify moving the gate afterward** — the frozen §3 limbs govern regardless of which of these
  two readings the data supports.

## §5 — Dedup & bar-adjacency (executed this session)

- Same dedup sweep as S1a, re-run for CL/MCL specifically:
  `grep -niE "volatility.cluster|range.persist|true.range|GARCH|ATR" docs/rejected_candidates.md
  ops/instruments/MCL.md ops/instruments/MECHANISMS.md` → no prior daily range-persistence
  conditioner test on CL/MCL. `MECHANISMS.md`'s `daily-range-state-persistence` heading (created
  this session for S1a) is this exact class — S1b is its second class finding, not a new class.
- **MCL.md read in full.** Standing warnings W1 (monthly roll — engaged above), W2 (weekend-bar
  UTC bucketing — same fix applied), W3 (session-window ambiguity — **not engaged**: this screen
  consumes databento's own pre-aggregated daily bars directly, it never defines an intraday
  session window the way an ORB-style construct would, so W3's equity-RTH-vs-Energy-23h concern
  doesn't bind here), W4 (FOMC exclusion — **not engaged**, that warning is scoped to the
  `CONFIG-B-MCL` fade construct's specific hold-horizon, not this unconditional daily screen).
  MCL ledger status "OPEN — geometry-cleared, mechanism-owed" — this screen is exactly the
  mechanism-owed gap that status names, though it does not by itself discharge it (a NULL/near-
  miss screen doesn't supply a mechanism; only a SIGNAL would move that status).
- No prior CL/MCL daily-TR-quintile-persistence test exists in `lab/CATALOG.md`, the discovery
  manifests, or any archived campaign.

## §6 — Forbidden moves

Identical to `PREREG_S1A.md` §6: no second quantile cut, window length, or horizon (this is a
replication — changing any parameter here would void the comparison, not just double-count K).
No reading past 2019-01-01 (`MCL.v.0` confirm window reserved). No re-run with more placebo
permutations on a near-miss. No promoting SIGNAL to a candidate. No comparing S1a and S1b's
point estimates as if pooling them into one statistic — each stands on its own frozen gate; a
cross-instrument synthesis (if both come back the same way) is a §4-slate-level read, not a
per-screen one.

## §7 — Data pull record

```
$ python lab/databento_fetch/db_fetch.py estimate --symbols CL.v.0 --stype continuous \
    --schema ohlcv-1d --start 2010-06-06 --end 2019-01-01 --phase discovery
[estimate] cost      : $0.0000 USD (streaming)
[estimate] billable  : 148,736 bytes  (~0.0001 GB)
[estimate] records   : 2,656
```

Confirmed $0.0000. Pulled: 2,656 rows, `cl_1d.parquet` (2010-06-07→2018-12-31).

**Step-0 panel-integrity battery (executed before any TR/roll computation):**

- **Day-of-week census:** 435 phantom Sunday bars (weekday=6) — median volume 2,622 vs
  Monday's 269,968.5 (**0.97%**, even thinner than GC's 2.3%). Zero Saturday bars. **Same fix
  applied:** drop `weekday ∈ {5, 6}`. Post-filter: 2,221 rows, weekday census Mon 448 / Tue 446
  / Wed 446 / Thu 446 / Fri 435, zero Sat/Sun.
- **Duplicate `ts_event`:** 0. **Nulls (O/H/L/C/volume):** 0.
- **Roll-day census (post weekend-filter):** **103 roll days**, ~12.0/year — matches MCL.md W1's
  warning directly, measured rather than assumed. First few: 2010-06-21, 2010-07-21,
  2010-08-20, 2010-09-20, 2010-10-20 (persisted in full to
  `s1b_results.json.roll_dates`, not hand-copied — the S1a lesson applied from the start).
- **Gap-day census (≥4 calendar days, post weekend-filter):** 13 gaps, **dates identical to
  S1a's GC census** (2010-12-27, 2011-04-25, 2012-04-09, 2013-04-01, 2014-04-21, 2014-06-16,
  2014-09-26, 2015-04-06, 2015-12-28, 2016-01-04, 2016-03-28, 2017-04-17, 2018-04-02) — a useful
  cross-instrument corroboration that these are genuine venue-wide/vendor-wide closures rather
  than an instrument-specific data defect (two unrelated commodities, identical gap dates, is
  much more consistent with a shared exchange-holiday or data-vendor-side gap than coincidence).
  Same bounded-materiality disclosure as S1a applies (≤13 of ~2,117 valid TR observations,
  well under both n-floors); not excluded, per the same "doesn't warrant a mid-campaign design
  change to a frozen object" reasoning.
- **Date-span coverage:** matches the requested window exactly, no truncation.
