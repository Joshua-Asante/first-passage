# Explore-confirm — `expiry-oi-strike-convergence` (MGC) — `AMBIGUOUS-HOLD`

**Date:** 2026-08-21
**Token:** [`EXPLORE_GO.md`](EXPLORE_GO.md) (ISSUED 2026-08-21, gitignored — promoted from
[`EXPLORE_GO.DRAFT.md`](EXPLORE_GO.DRAFT.md) per its own Promote rule)
**Cost / K:** $0.00 · K unchanged (`K_intrinsic` stays 1 — this is the pre-registered scoring pass
for the one already-spent construct class, not a new K)
**Driver:** [`explore_confirm_driver.py`](explore_confirm_driver.py) (Phase 1-3: pull) ·
[`explore_confirm_score.py`](explore_confirm_score.py) (Phase 4-5: pilot calibration + score) ·
statistical core [`explore_confirm_lib.py`](explore_confirm_lib.py) (23/23 unit tests, re-verified
this session — see below)
**Raw:** [`_explore_confirm_2026-08-21_RESULTS.json`](_explore_confirm_2026-08-21_RESULTS.json)
(full null-stat array, both pilot delta arrays, per-cycle list — 66KB, committed in full per the
operator's own re-verification request)
**Panel:** not cached/committed — `_explore_confirm_2026-08-21_RAW.json` and the weekly-definitions
parquet cache are gitignored (regenerable at $0.00 from this driver; same convention as the
repo's other Databento vendor-bar caches)

**Pre-flight (executed before any pull, this session):**
- Read `EXPLORE_GO.DRAFT.md`, `explore_confirm_lib.py`, `test_explore_confirm_lib.py` in full.
- Re-ran the unit suite independently rather than trusting the commit message's "23/23 passing"
  claim: `PYTHONPATH=lab python -m pytest .../test_explore_confirm_lib.py -q` → **23 passed**,
  reproduced.
- Databento cost `estimate` run before every pull (Rule 1), even though every schema used here
  (`definition`/`statistics`/`ohlcv-1d`) has priced at $0 in every precedent this repo has run:
  OG.OPT weekly roots (OG1-4) definitions over the full IS window: **$0.0000**, ~0.36GB, 688,702
  records. GC.c.0 daily bars: **$0.0000**, ~19KB, 336 records (IS-window estimate; actual pull
  padded further back for the DELETE test's lookback, see below).

---

## Universe discovered (weekly + monthly, not hardcoded)

- **Weekly** (`OG1`/`OG2`/`OG3`/`OG4` roots — CME's rolling-label weekly Gold options; confirmed
  empirically this session that Databento's `OG.OPT` parent symbol does **not** include these
  weeklies under the `OG` root itself — they resolve only under separate `OG{1,2,3,4}.OPT` parent
  symbols, discovered by probing candidate roots since the DRAFT didn't name the exact tickers):
  one bulk `definition` pull across the full IS window (2024-01-01→2025-03-31, $0, 358MB, 688,702
  rows) — **64 distinct weekly expirations** found in-window; 60 scored (4 dropped by the
  arm-window/OI-availability checks below, see Skipped).
- **Monthly** (`OG` root): one discovery snapshot at IS_START (monthlies list years ahead, so a
  single snapshot reveals every in-window expiry without dating-out risk) — **15 distinct monthly
  cycles**, all 15 scored.
- **Total: 75 candidate cycles, 75 scored, 0 skipped** (well past the `n_floor=20` VOID line, and
  past the DRAFT's own "order of 60-90" estimate — landed at 75).

## Per-cycle procedure (per `PREREG_G0.md` §1 / `EXPLORE_GO.md`, unchanged)

For each cycle: `definition` snapshot at arm_start (3 sessions before expiry) → real strikes/
instrument_ids at that time (weeklies: sliced from the one bulk pull already in memory; monthlies:
a small per-cycle re-pull, mirroring the 2026-08-21 cheap falsifier's own proven pattern) →
`statistics` (`stype_in=instrument_id`, narrow, cheap) for OI-by-strike, summed call+put →
`strike_star` = max-OI strike.

---

## Phase 4 — pilot calibration (fresh; NOT the corrected-null-battery's own numbers)

Two disjoint pilot batches, both inside the reserved pilot seed range
(`default_rng([20260821, 990000+i])`), disjoint from the official `i=0..999` block:

| Batch | i-range | n | n_iter | median max\|Δrank-ACF\| (lags 1,2,3,5,10,20) | p95 |
|---|---|---:|---:|---:|---:|
| Calibration | 0–199 | 200 | 100 | 0.03458 | 0.05377 |
| Gate-check | 200–249 | 50 | 100 | 0.03185 | 0.05586 |

**Tolerance frozen from the calibration batch, 1.4× headroom** (same margin convention as
`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`, freshly measured on this
series, not its numbers): **tol_median = 0.04841, tol_p95 = 0.07528**.

**Gate-check result: median 0.03185 ≤ 0.04841 ✓ AND p95 0.05586 ≤ 0.07528 ✓ → PASS at n_iter=100
(no escalation to 500 needed).** `diagnostic_ok = True`.

**Disclosed gap:** the DRAFT's third escalation rung ("Schreiber end-matching trim") is not
implemented in `explore_confirm_lib.py`. Not reached this run (gate passed at the first rung), but
if a future re-run ever needs it, that rung is a real gap, not a silent no-op.

## Phase 5 — official IAAFT-surrogate significance test (seed block `[20260821, i]`, i=0..999)

| Quantity | Value |
|---|---|
| `real_stat` (mean displacement reduction, pts) | **−5.5213** (net **divergence**, not convergence) |
| Null distribution (M=1000) | mean −4.4623, sd 4.6345 |
| Null percentiles | 2.5%: −12.951 · 5%: −11.591 · 25%: −7.796 · 50%: −4.603 · 75%: −1.523 · 95%: 3.538 · 97.5%: 5.551 |
| `p_upper` | **0.5724** |
| `p_lower` | 0.4286 |
| Real stat's percentile in the null | **42.8th** |

The real statistic sits just below the null's own median — indistinguishable from what generic
autocorrelated GC price dynamics produce on their own, with no expiry-specific mechanism. Neither
`p_upper > 0.95` (FALSIFIED line) nor `p_upper ≤ 0.05` (SHAPE-CLEAR line) is crossed.

## Req 1a — Delete / Flip

| Check | Real strike | Sham (60-session trailing median) |
|---|---:|---:|
| Stat (mean displacement reduction) | −5.5213 | −8.2013 |

**DELETE: PASS** (−5.5213 > −8.2013, strict) — but both are negative; the real strike is simply
*less divergent on average* than a generic level, not convergent in an absolute sense. A weak pass,
not a ringing endorsement of the OI-selection mechanism.

**FLIP: FAIL** (converge_stat −5.5213 is **not** greater than diverge_stat +5.5213) — betting on
**divergence** would have beaten betting on convergence over this sample. This directly contradicts
the construct's own central directional claim (Γ-driven pinning toward the strike).

**Disclosed, non-gating:** real `convergence_rate` = **0.48** (36 of 75 cycles converged) — under
half.

## Disclosure — naive fixed-offset control, re-run at full n=75 (non-gating, continuity only)

The 2026-08-21 cheap falsifier's own check (arm vs. a fixed 10-session-earlier control window),
re-run on the full IS universe rather than n=7:

| | n=7 (cheap falsifier) | n=75 (this run) |
|---|---:|---:|
| arm converge rate | 4/7 = 0.571 | **36/75 = 0.480** |
| ctrl converge rate | 4/7 = 0.571 | **45/75 = 0.600** |
| outcome-correlated frac (same cycle converges/diverges in both windows) | 7/7 = 1.00 | **36/75 = 0.480** |

At full n, the naive control window converges *more* than the true arm window (0.60 vs 0.48) — the
opposite of what an expiry-specific effect would predict — and the outcome-correlation that looked
like a clean trend-confound signature at n=7 (100% correlated) drops to 48% at n=75, close to a
coin flip. **Read:** the n=7 cheap falsifier's "same cycles converge/diverge in both windows"
finding does not replicate at full sample size — it was very likely a small-sample coincidence, not
the robust trend-confound the falsifier's own addendum reasoned toward. The IAAFT-surrogate result
above (not the naive control) is the primary, trustworthy read; this row is continuity disclosure
only, exactly as `EXPLORE_GO.md`'s Disclose row specifies.

---

## Verdict

```
diagnostic_ok = True
n_cycles_is   = 75  (>= n_floor 20)
p_upper       = 0.5724   (not > 0.95 -> not FALSIFIED)
delete_passed = True
flip_passed   = False    (-> not SHAPE-CLEAR even if p_upper had cleared 0.05)
```

**`AMBIGUOUS-HOLD`** per `explore_confirm_lib.explore_verdict`'s frozen gate table — the honest
result of applying the pre-registered rules, not an editorial softening. Substantively this leans
hard toward dead: the real effect is not just non-significant but **negative-signed** (net
divergence, not convergence) and **FLIP explicitly fails** (divergence beats convergence
empirically). The frozen `FALSIFIED` line (`p_upper > 0.95`) requires the real statistic to sit in
the *bottom* 5% of the null — here it merely sits at an unremarkable 42.8th percentile, so the rule
does not cross that line even though the qualitative story (wrong sign, flip fails) reads the same
as most FALSIFIED cases this program has produced. Rules govern; the verdict string is
`AMBIGUOUS-HOLD`, reported as such.

## Disposition

- **Not** SHAPE-CLEAR: no second Pine version, no re-TV, no survivor-MC step licensed by this run
  (`EXPLORE_GO.md` §5 forbidden moves, unaffected).
- **Not** FALSIFIED under the frozen gate's own literal threshold — recorded as `AMBIGUOUS-HOLD`,
  not upgraded or downgraded from what the rules produce.
- `K_intrinsic` unchanged (still 1). No second instrument, no θ-retune, no new K spend.
- CONFIRM (2025-04-01→2025-09-29) was never read — no function in `explore_confirm_driver.py` or
  `explore_confirm_score.py` accepts a date argument reaching past `IS_END`. Verified directly
  against the pulled RAW panel this session: max price date **2025-03-30**, max scored cycle expiry
  **2025-03-28** — both before `CONFIRM_START` (2025-04-01) (`python -c "import json; d=json.load
  (open('lab/analysis/c1/msl_s4_mgc_2026-08/_explore_confirm_2026-08-21_RAW.json')); print(max(d
  ['price_dates']), max(c['exp_date'] for c in d['scored_cycles']))"` — RAW.json is gitignored,
  regenerate locally via `explore_confirm_driver.py` to re-check).
- Recommend to the operator: given the negative sign + FLIP-FAIL combination, treat this
  `AMBIGUOUS-HOLD` as functionally close to a kill for build-out purposes, while leaving the formal
  card disposition (`candidates_CARD.md` / a closure brief) to an explicit operator decision rather
  than this session unilaterally parking it — `AMBIGUOUS-HOLD` has a defined ITERATE/HOLD path in
  this program's own vocabulary (see the `Q-TNEC-CON-*` closures), and which of those applies here
  is an operator call, not a driver-script call.
