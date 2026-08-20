# Q-TODVOL-1 — D2 pre-G0 falsifier RESULTS: `FAIL`

**Date:** 2026-08-20
**Frozen spec:** [`FREEZE.md`](FREEZE.md), committed `060b13f` before this script ran.
**Driver:** [`run_d2_falsifier.py`](run_d2_falsifier.py) · data [`d2_falsifier_results.json`](d2_falsifier_results.json)

## Verdict: `FAIL` — route ① closes for this construct shape at $0, no Board debate needed

| Metric | Value | Bar | Cleared? |
|---|---:|---:|:---:|
| n signals | 975 | — | — |
| coverage | 54.26% of eligible sessions (n=1,797, after 60-session warm-up) | — | — |
| mean signed gross | **+0.2546 pt** | ≥ 2.8200 pt (0.5 × 4×RT) | **No — 9.0% of the bar** |
| WR | 42.26% | — (informational; rr=2 naive breakeven is 33.3%) | — |
| RT cost | 1.4100 pt | — | — |
| 4×RT hurdle | 5.6400 pt | — | — |

Exit mix: 373 stop (38.3%), 135 target (13.8%), 467 session-flat (47.9%) — no degenerate concentration in any one exit path. Direction split 627 short / 348 long (64%/36%) — noted, not adjusted for; the frozen construct has no direction-selection lever to retune in response.

## What ran

Per `FREEZE.md` §2/§3, unchanged: first RTH 15m bar (excluding the first 2, i.e. the 09:30–10:00
opening-range window) whose range ≥ 2.0× the trailing-60-session median range for that exact
time-of-day slot (causal, strictly prior sessions only), entered in that bar's own close-vs-open
direction, stop at 1.0× the trigger bar's own range, target at 2.0× (rr=2), session-flat exit
using the day's last available close (early-close CME sessions — Labor Day/Thanksgiving/Christmas
half-days — handled by taking the last non-NaN close rather than a fixed final slot). Full IS
panel: `_mnq_15m.pkl`, 1,857 sessions, 2019-05-05 → 2026-07-15; 1,797 sessions eligible after the
60-session warm-up. No CONFIRM split was ever defined for this candidate — moot, given the D2
result.

Two mechanical bugs were caught and fixed **before** trusting any number, neither touching a
frozen construct parameter: (1) a `datetime.date` formatting error in the report writer; (2) five
early-close sessions produced a `NaN` session-flat exit because the nominal last time-of-day slot
has no bar on a half day — fixed by taking the last non-NaN close of the day instead. Both are
data-handling fixes to this script's own bookkeeping, not adjustments to θ, the lookback window,
or the stop/target multiples.

## Disposition

**Closes at $0, no G0, no Board debate** — per `FREEZE.md` §3's own frozen pass/fail rule. The
gross edge measured (+0.25 pt/signal) sits an order of magnitude below the generous 2.82 pt bar,
not a close call the way ORB-MNQ-1's own numbers can be close calls — this is the kind of clean
miss the D2 falsifier is designed to catch conclusively. `tod-baseline-range-trigger` as
constructed here does not clear the estate's cheapest quality bar; the within-instrument
temporal-selectivity door (route ①, ADR 2026-08-10) stays open in principle, but this specific
causal story (volatility-threshold-triggered entry, sized off the trigger bar's own range) does
not supply a candidate through it.

**Re-proposal bar:** a genuinely different causal criterion — not a re-tuned `θ`, lookback
window, or stop/target multiple on this same shape (Known Trap #12; matches every other CON-N
closure's own discipline). `K_intrinsic=1` is spent on this cell; the door stays open for a
structurally different criterion under a fresh Q-ID.

## §10 audit-hook discharge

```bash
$ python -c "import json; d=json.load(open('lab/analysis/c1/todvol_1_2026-08-20/d2_falsifier_results.json', encoding='utf-8')); print(d['passed'], d['mean_signed_gross_pts'], d['pass_bar_pt'])"
False 0.2546... 2.82

$ git log -1 --format='%h' -- lab/analysis/c1/todvol_1_2026-08-20/FREEZE.md
060b13f  # confirms the freeze commit predates this results file

$ python scripts/instrument_profiles.py cell MNQ tod-baseline-range-trigger
# Expected: class finding now reads FAIL, not "pending"
```

## Verification

```bash
python lab/analysis/c1/todvol_1_2026-08-20/run_d2_falsifier.py
# Expected: VERDICT: FAIL, mean_signed_gross ~+0.25pt, n_signals=975
```
