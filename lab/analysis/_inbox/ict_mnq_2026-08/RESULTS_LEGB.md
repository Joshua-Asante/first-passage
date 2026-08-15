# `Q-WLEGB-1` — RESULTS: the W-layer bias does NOT transfer below the weekly close

**Date:** 2026-08-04
**Pre-registration:** [`PREREG_LEGB.md`](PREREG_LEGB.md) — frozen at commit `b509d4f`, **before any
conditional hit rate existed**. Leg (b) had never been measured, on any instrument.
**Cost:** **$0.00** (MNQ 1m already on disk from `Q-ICTEXP-1`; daily and weekly resampled from it) ·
**K=0** · **no manifest** · **Cap seat untouched**.
**Runner:** [`run_legb.py`](run_legb.py) · **23 new unit tests** (90 in this directory), hand-computed
and passing **before** the runner read a real bar.

---

## 1. Verdict — `FALSIFIED`, by 0.05 percentage points

| | close-to-close (**verdict cell**) | open-to-close (disclosure) |
|---|---|---|
| scored days / week-blocks | 2,018 / **349** | 2,018 / 349 |
| `gateHit` | **53.7661%** | 53.3697% |
| block-CI 95% | [51.4881%, 55.8129%] | [51.1457%, 55.4015%] |
| sign-shuffle placebo mean / **p95** | 52.3031% / **53.8157%** | 52.3104% / 53.8157% |
| **beats placebo?** | **NO — margin −0.0496 pp** | **NO — margin −0.4460 pp** |
| halves | (55.0940%, 52.4330%) | (54.8961%, 51.8371%) |
| thirds | (56.1300%, 51.9345%, 53.2138%) | (56.1300%, 50.8929%, 53.0643%) |

**`FALSIFIED` per the frozen gate (L2): the measured rate does not beat its own base-rate-matched
null.** The margin is −0.0496 pp — the measured value sits **essentially on** the placebo's 95th
percentile, not decisively below it. The honest reading is **"indistinguishable from the null"**,
not "clearly worse than it".

---

## 2. The load-bearing fact: without the placebo, this would have PASSED

Four of the five pre-registered limbs clear comfortably:

| Limb | Result |
|---|---|
| n-floor ≥ 30 week-blocks | **349** — clears 11× |
| block-CI lower bound > 0.50 | **51.49%** — clears, entire CI above 0.50 |
| both halves > 0.50 | 55.09% / 52.43% — **clears** |
| all three thirds > 0.50 | 56.13% / 51.93% / 53.21% — **clears** |
| **beats sign-shuffle placebo** | **53.77% vs p95 53.82% — FAILS** |

A leg-(a)-shaped test — the exact gate `PREREG-W.md` uses, which measures a rate against 0.50 with
stationarity limbs — would have returned **RESOLVED** on this data and reported "the W bias predicts
daily direction at 53.8%, CI entirely above 0.50, stable across halves and thirds." **That claim
would have been an artifact.**

**Why:** 76.22% of scored weeks carry `vStruct = +1` (MNQ's secular uptrend), and 54.31% of days are
up. Pairing those marginals alone yields

    base rate = 0.7622 × 0.5431 + 0.2378 × 0.4569 = 0.5226

against a measured 0.5377 — an excess of just **+1.51 pp**, which is inside the sampling spread of
349 week-blocks. The placebo's measured mean, **0.52303**, reproduces that closed form to within
0.0005 — an independent check that the shuffle is correctly base-rate-matched rather than merely
plausible.

This is the same instrument, and the same failure shape, that killed the 1H layer (discount→up
0.5394 against its own placebo at 0.5485). Making the placebo the **primary** bar was a §0 design
decision taken from that precedent, before any number here existed. It is the only limb that fired.

---

## 3. Per-side decomposition — the gate is a filter, not a direction-flipper

Disclosure of the verdict cell's own two arms (the same per-side reporting leg (a) and the 1H layer
used). **The verdict reads the pooled cell; this does not change it.**

| Prior week | scored days | `gateHit` | up-day rate in those weeks |
|---|---|---|---|
| `vStruct = +1` | 1,539 | 55.30% | **55.30%** |
| `vStruct = −1` | 479 | **48.85%** | **51.15%** |
| *(unconditional)* | 2,018 | — | 54.31% |

Two readings, and the second is the useful one:

1. **The bullish arm barely moves anything.** After an up-week, days are up 55.30% vs 54.31%
   unconditionally — **+0.99 pp**. Almost the entire apparent "edge" is the uptrend itself.
2. **The bearish arm is real but wrong-signed for trading.** After a down-week, the up-day rate
   falls to 51.15% — a **−3.16 pp** shift, three times the bullish arm's effect and the larger of
   the two. **But it does not cross 50%.** Days after a down-week are still more likely up than
   down, so betting *down* on that signal is a 48.85% proposition.

**Consequence for any future construct:** `vStruct` can tell you **when to be less long**. It cannot
tell you **when to be short**. This is the identical asymmetry the 1H layer found — premium resolved
*upward* (0.4537 down-rate) in the same secular uptrend — and it is now confirmed on a second layer
of the same cascade.

---

## 4. The pre-registered expectation held (no defect indicated)

`PREREG_LEGB.md` §4 recorded, before measuring: *"daily returns are noisier than weekly ones, so if
the content is real it should be **weaker** at daily granularity, not stronger. A daily rate
materially above leg (a)'s weekly rate would be a red flag for a construction defect."*

Measured **53.77% daily** against leg (a)'s **57.51% weekly** — weaker, as predicted. No defect
investigation is triggered.

The **disclosure cell is worse than the verdict cell** (−0.4460 pp vs −0.0496 pp), and that
direction matters: open-to-close is the granularity an E1-compliant construct could actually trade,
since the overnight gap is unholdable under a 16:00 ET flat rule. On the tradeable granularity the
signal is *more* clearly null, not less.

**Time profile:** thirds run 56.13% → 51.93% → 53.21%, i.e. front-loaded and decaying. Reported as
disclosure; no trend test was pre-registered and none is claimed.

---

## 5. Disposition (discharging the pre-registered §6 branch)

**Verdict used:** `FALSIFIED`
**Model update:** the W-layer's RESOLVED finding is a statement about **weekly bars**, not a
general directional bias with sub-weekly reach. Its apparent daily-granularity content is
base-rate arithmetic on a long-biased instrument. What survives is narrower and more precise than
"a weekly bias exists": a *long-side filter* with a ~1 pp effect and a bearish arm that does not
cross 50%.

**Next: `STOP`** — the branch §6 pre-registered for `FALSIFIED`, discharged as frozen.

**Routing:** the "W/D as a gate for an intraday MNQ construct" idea dies here, at $0. It was the one
live ICT residual after the 2026-08-04 audit found every other follow-up `BLOCKED-LOST-PINE`.

**Stop rule / re-proposal bar (as pre-registered):** re-opening requires a **mechanism argument for
why weekly structure should carry intraday** — not a re-test at another horizon, another `emaLen`,
or another lag. Those are the FM-4 moves and they are forbidden. A bare "try 4H next" does not clear
this bar.

**Board write:** MNQ ledger — **N8 scope-narrowed** (leg (a) stands at the weekly close; leg (b)
FALSIFIED) + a **DEAD row**; `STATE.md` decision-index line; `SESSIONS.md` entry.

**What this does NOT touch:** leg (a) remains **RESOLVED** on NQ (0.5880) and MNQ (0.5751) at the
weekly close, and N8/N9 stand. This probe **bounds the finding's scope**; it does not overturn it.
`SLR-MYM-1` §6 bullet 3 — *"NOT established: anything about `vStruct`'s per-entry transfer"* — is now
**partly** established: not per-*entry* (that form is still `BLOCKED-LOST-PINE`), but the sub-weekly
transfer question it stood for is answered negative.

---

## 6. Scope limits — read before citing any number

1. **This is not the archived W-6.** W-6 is a 1M bias-gate ablation on per-entry records and remains permanently `BLOCKED-LOST-PINE` (`netBias` survives only in the lost Pine). This probe answers the same underlying question strategy-free. A construct's entries could in principle behave differently from calendar days — that specific form is untested and untestable.
2. **Strategy-free by design, not by convenience.** The ORB-entry version was rejected under the MNQ ledger's **F2 guard** (`PREREG_LEGB.md` §1) — it would have been a fifth ORB conditioning gate wearing a different label.
3. **One instrument.** MNQ only. Leg (a) replicated on NQ and US500; leg (b) has not been run elsewhere, and the base-rate arithmetic that dominates here is instrument-specific (it turns on the +1-week fraction and the up-day rate).
4. **The margin is thin and the verdict is a frozen threshold call.** −0.0496 pp is well inside the sampling error of a p95 estimated from 2,000 shuffles. Read this as *"the effect does not separate from its null"*, not as a precise measurement of how far below it sits. It would be equally wrong to re-run with more shuffles hoping to flip the sign — that is outcome-conditional re-testing.
5. **Daily bars, not intraday paths.** Direction is measured close-to-close and open-to-close; nothing here speaks to intrabar behaviour, fills, or costs.
6. **No outcome promotes anything.** The probe had no GO state by construction.

---

## 7. Reproduce

```bash
python -m pytest lab/analysis/_inbox/ict_mnq_2026-08/ -q          # 90 passed
python lab/analysis/_inbox/ict_mnq_2026-08/run_legb.py <mnq_1m.parquet>
git --no-pager diff HEAD -- lab/archive/ict_cascade_2026-06-18/   # must be EMPTY
```

Data (gitignored, regenerable at $0.00 — estimate first, always):

```bash
python lab/databento_fetch/db_fetch.py estimate --symbols MNQ.v.0 --stype continuous \
  --schema ohlcv-1m --start 2019-05-06 --end 2026-08-04 --phase oos
python lab/databento_fetch/db_fetch.py pull --symbols MNQ.v.0 --stype continuous \
  --schema ohlcv-1m --start 2019-05-06 --end 2026-08-04 --phase oos \
  --max-cost 1.00 --out mnq_1m.parquet
```

**Two test bugs caught before the runner read real data** (both mine, both in the tests rather than
the code): an arithmetic slip asserting `max(11, 25, 31) == 25`; and a placebo tolerance that
compared the shuffle mean to the *realized* raw rate with a ±0.03 band, ignoring that labels are
constant within a week — so the effective sample is the **week** count, not the day count, and a
~0.6σ gap is expected. The second was repaired by asserting against the **closed form**
`f(+1)·P(up) + f(−1)·P(down)` instead, which is exact and tests the property that actually matters:
that the placebo centres on the base rate rather than on 0.50.
