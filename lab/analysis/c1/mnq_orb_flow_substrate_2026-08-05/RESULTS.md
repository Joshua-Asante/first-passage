# `MNQFLOW-1` (re-aimed) — RESULTS: ORB-MNQ-1's trigger boundary *does* carry an L1 signature, and it leans **against** the break

**Status:** `RESOLVED` (W1) — the less likely branch.
**§8 pre-registered no-signature as the more probable outcome, and that prediction was wrong.**
At ORB-MNQ-1's own frozen trigger moments the top-of-book size
asymmetry differs from matched same-session controls by **−0.009367** (95% session-block CI
**[−0.013430, −0.005354]**, excludes 0) against a within-session label-shuffle placebo whose |.|
p95 is **0.004166** (**p_emp = 0.000**, 0 of 1,000). Both halves agree in sign and both exclude 0,
so the by-half rider does **not** fire.

**The sign is the finding.** `A` is signed *toward* the breakout direction, so a **negative** value
means that in the 60 s before the touch the book carries **more resting size on the side price is
about to break through**. The boundary does not look like a book leaning into a break; it looks
like a level with liquidity stacked against it.

**Date:** 2026-08-05 · **Pre-registration:** [`PREREG.md`](PREREG.md), frozen at **`2c1ff11`**
("FREEZE MNQFLOW-1"), operator pull sign-off landed at **`f7c5bec`** — both strictly before any
book-state quantity existed for this construct. Ordering is git-auditable:
`git log --oneline -- lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md | tail -1`.

**Cost:** **$0.00.** The full-S1 `tbbo` estimate reproduced the frozen §4 table exactly this session
— **$0.0000 / 20,734,224,240 bytes / 259,177,803 records**. **`K_intrinsic = 0`** (§6 — this
measures a structural property and, with outcomes never read, can emit no tradeable rule).
`K_banked(MNQ) = 5` disclosed, not summed ([ADR 2026-08-04](../../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)).
**No `core/`, lock, allocation, `dd_protection`, lifecycle, Pine, rail, or `LEG_MAP` change.**

> ⚠ **This opens nothing.** PREREG §7's W1 disposition is **watchlist + forward tripwire**, named as
> a candidate companion to the existing PF-CUSUM decay monitor — never an overlay, filter, or gate
> (FM-3). ORB-MNQ-1 remains **re-PARKED with its payability target FALSIFIED** (2026-08-03); nothing
> here disturbs that, and lifecycle moves are operator GO. **Any conversion of this result into a
> gate or filter is a fresh K-bound axis** requiring its own pre-registration — it does **not**
> inherit this `K=0` (§6).

---

## 1. Verdict — the frozen gates, evaluated literally in their frozen precedence

| # | Frozen trigger | Actual | Fired? |
|---|---|---|---|
| W4 | coverage < 90% | coverage **100.0%** (255/255) | ✗ |
| W3 | CI includes 0 | CI **[−0.013430, −0.005354]** excludes 0 | ✗ |
| W2 | CI excludes 0 ∧ \|effect\| ≤ placebo p95 | \|−0.009367\| = **0.009367** > **0.004166** | ✗ |
| **W1** | **CI excludes 0 ∧ \|effect\| > placebo p95** | **both limbs hold** | **✓ `RESOLVED`** |
| rider | W1 ∧ halves disagree in sign → `RESOLVED-NONSTATIONARY` | H1 **−0.008133**, H2 **−0.010592** — same sign, both CIs exclude 0 | ✗ |

| | value |
|---|---|
| ORB triggers (S2, engine `n`) | **255** |
| Matched controls (S4, k=5) | **1,275** |
| TBBO quotes measured | **4,220,030** (≈2,758 per window) |
| Coverage — triggers with ≥1 quote in the 60 s window | **255/255 = 100.0%** |
| Sessions dropped (no trigger quote / no control quote) | **0 / 0** |
| mean `A_trigger` | **−0.008797** |
| mean `A_control` | **+0.000570** |
| **difference** | **−0.009367** |
| 95% session-block bootstrap CI (10,000 reps, seed 20260805) | **[−0.013430, −0.005354]** |
| placebo \|.\| p95 (1,000 within-session label shuffles, same seed) | **0.004166** |
| placebo p_emp | **0.000** (0 of 1,000) |
| H1 / H2 | **−0.008133** [−0.014280, −0.002021] (n=127) / **−0.010592** [−0.016064, −0.005115] (n=128) |

**Effect size, stated plainly so `RESOLVED` is not over-read.** −0.009367 sits on a scale whose
range is [−1, +1]. At the median L1 total of **7 contracts**, it corresponds to roughly
**0.07 contracts** of mean imbalance — a systematic tilt, not a large one. It is *precisely
estimated* (the CI is ~0.008 wide) because each event averages ~2,758 quotes and there are 1,530
events; it is not *economically large* at any single quote.

## 2. Mandatory disclosed context — the depth census, and the argument against it

The [2026-08-05 ruling](../../../../docs/notes/2026-08-05-order-flow-probe-governance-question.md)
§7 limb 5 makes the blind probe's census binding context here: *"any size-derived feature,
including the sanctioned L1-asymmetry diagnostic, must argue against it."* The census said NQ's
displayed book is too thin to carry a fine signal — **median 67 contracts across all twenty levels
(≈3.4/level), 78.1% of imbalance values tied**.

Measured on **this** feature's own data:

| | value |
|---|---|
| L1 total size, both sides (p05 / p50 / p95) | **2 / 7 / 17 contracts** |
| Distinct `A` values in 4,220,030 quotes | **2,456** |
| Observations inside a tie group (>1) | **99.98%** |
| Exactly `A` = 0 | **14.08%** |

**The census's warning is confirmed, not evaded: per-quote, this feature is coarse — coarser than
the blind probe's, by every column.** MNQ's L1 carries a median of 7 contracts across both sides
(≈3.5/side), comparable per-level to NQ's ≈3.4, and essentially every observation sits in a tie
group.

**The argument that the result survives it anyway** — offered as an argument, with the numbers above
supplied so a reader can reject it: the census bars a **per-observation predictive** feature, which
is what the blind probe built (n=1,167 single-minute observations, one value per minute). This
construct's unit of analysis is a **window mean over ~2,758 quotes**, aggregated across 1,530
windows. Coarseness of the individual draw limits the resolution of one observation; it does not
bound the precision of a mean over thousands of them, and the placebo — computed on the *same*
tied, coarse values — is what certifies that. A tied feature can still support a precisely measured
contrast. It could not support a fine per-minute prediction, and nothing here claims it could.

## 3. What this does NOT say (the F2 guard's operative content)

- **It says nothing about whether `A` separates ORB winners from losers.** FM-1 removed outcome data
  from the design; trade results were never read, never joined, never emitted. That is exactly the
  question the MNQ **F2 guard** forbids ("highest-risk laundering move on this instrument") and
  exactly why the construct cannot become a fifth conditioning gate wearing a new label. The four
  FALSIFIED conditioning gates are **not** rescued, addressed, or reopened by this.
- **It is L1 only.** §4 flagged that a null would not have excluded a deeper signature; the converse
  binds equally — this is a top-of-book fact and says nothing about depth beyond it.
- **It is not a fill or slippage claim.** Measured on a window ending *before* the touch minute; no
  fill price, no comparison to the 1-tick model (§3 condition 2).

## 4. Limitations — the largest one first

1. **Level-proximity is not controlled, and this is the main caveat.** By construction a trigger
   moment is a moment when price sits at the session's opening-range extreme; a control is an
   arbitrary same-session moment matched **only on time-of-day**. S4's stated job was the intraday
   liquidity U-shape, and it does that job. It does **not** separate *"the book at the ORB level"*
   from *"the book at any salient level price is about to cross."* The measured signature may well
   be the generic microstructure of an approached level rather than anything specific to ORB-MNQ-1.
   **Distinguishing the two is a new cell (FM-4) and needs fresh authorization** — it is named in §6
   as a gated re-proposal route, not run here.
2. **Four sessions carry a Databento `degraded` quality flag** — 2025-09-24, 2025-11-28, 2026-03-16,
   2026-04-10. They are **retained**: dropping them and re-running would be a second cut of a frozen
   design (FM-4) chosen after seeing the result (FM-6). Disclosed instead. The by-half split (127 vs
   128 sessions, both significant, same sign) is the frozen evidence against any single-session
   artifact driving the effect.
3. **The trigger timestamp is a resolution choice, declared before data.** The engine resolves a
   breakout to a 15m bar; S3 measures "at the touch". The touch was localized to the 1m bar inside
   the engine's entry bar that first crosses the OR level, and the window is `[t−60s, t)` — strictly
   before the minute containing the touch, so no look-ahead. The coarser reading (15m bar open) was
   **not** also computed; that would have been a second cell.
4. **Two-sidedness.** The CI limb is two-sided, so the placebo limb was taken two-sided too
   (|observed| vs p95 of |placebo|). Declared in `flow_lib` before the run, not chosen after.

## 5. Process disclosures

- **A frozen-element conflict, resolved and recorded.** S1's window runs to 2026-08-04; the on-disk
  1m panel S2 names ended **2026-07-15** — a 14-session shortfall. The panel was refreshed across
  S1's exact window (`ohlcv-1m`, cheapest schema, **$0.0000**, same symbology, strictly *inside* S1
  and never beyond it) so the run matches its own frozen design instead of silently shrinking it.
  This is a second pull the sign-off did not name, so it was logged as a **recorded interpretation**
  in the PREREG amendment log and put to the operator. ✅ **RATIFIED 2026-08-05** — operator, in
  session: *"the panel refresh is fine, keep it."* The event set therefore stands at the full frozen
  window **2025-08-06 → 2026-08-04** (255 triggers) and the re-scoping branch is closed. Every
  number in this document was computed on the accepted window and is unaffected.
- **Transport.** The frozen design reads ~0.09 GB of the 20.73 GB S1 window, so the pull was
  transported as 1,530 60-second windows — a strict subset of the authorized window, per §4's
  explicit "day-chunking is an operational detail, not a cost or governance one". Two `504` gateway
  timeouts were auto-retried and recovered. The whole-window cost gate was taken **once**, upfront,
  because every window is a subset of an already-priced $0.0000 request.
- **A defect found before the run and fixed in code, never by editing the frozen PREREG.** A
  synthetic dry-run (no real quote) exposed that `DataFrame.map()` coerces Python `None` to `NaN`,
  so the "uncovered window" filter admitted empty windows as NaN. That is worse than dropping them:
  `nansum` contributes 0 to the control numerator while the count still divides by it, dragging the
  control mean toward zero and **manufacturing a difference out of missing data**. Fixed by
  filtering on finiteness in `flow_lib.assemble_sessions`, with a hard `_pad` backstop and **five
  regression tests** pinning the exact coercion. The original suite missed it because no test
  combined ragged sessions with the placebo. **27 unit tests green before the runner read a real
  quote** (§9 step 3).
- **Engine faithfulness.** `orb_lib.orb_backtest` was called unmodified (`or_bars=2`, filters off);
  the engine emits no date index, so trade days were recovered by replaying only its day-inclusion
  predicate and were **asserted elementwise** against its own `range` array before use. Outcome
  arrays were used for that assertion and then discarded — no outcome column exists on
  `events.parquet`.

## 6. Iterate

- **Next:** **STOP** for this thread. §7's W1 disposition is explicit that a positive **opens
  nothing**; the deliverable is the watchlist registration below, not a successor run.
- **Deliverable:** register `A` at the ORB boundary as a **watchlist observable with a forward
  tripwire**, named as a candidate companion to the existing PF-CUSUM decay monitor (2021+ baseline
  PF 1.1691, floor 1.0855, `block_size=2`), which fires on realized P&L and therefore only *after*
  decay has been paid for. This is the structural observable that monitor lacks. It is a *candidate*
  companion — wiring it to anything is a separate decision.
- **Entry packet for the one named re-proposal route (gated, not open):** the level-proximity
  discriminator of §4 limitation 1 — contrast the ORB trigger boundary against *other* approached
  levels in the same sessions. Requires its **own pre-registration, its own K, and an operator GO**;
  it is not authorized by this run.
- **Stop rule:** do **not** re-cut this design — no alternate window, threshold, normalization,
  second instrument, MBP-10 arm, or degraded-day exclusion (FM-4/FM-6). Do not convert `A` into a
  gate or filter without a fresh K-bound pre-registration (§6). Do not read ORB outcomes against `A`
  under any framing (FM-1 / F2 guard).
- **Board write:** owed in every branch — STATE.md, `ops/instruments/MNQ.md` (N14 + session log),
  `docs/SESSIONS.md`, `lab/CATALOG.md`, PREREG amendment log.

## 7. Audit hooks

```bash
# Freeze ordering (expect 2c1ff11 FREEZE as the first commit touching the PREREG)
git log --oneline -- lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md | tail -1

# Cost dry-run reproduction (FREE; never add `pull`) — expect $0.0000, ~20.73 GB, ~259M records
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate --symbols MNQ.v.0 \
  --stype continuous --schema tbbo --start 2025-08-06 --end 2026-08-04

# The tests that had to pass before the runner read a real quote (expect 27 passed)
.venv-research/Scripts/python.exe -m pytest \
  lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/test_flow_lib.py -q

# Rebuild the event set from the free panel (expect 255 triggers / 1,275 controls, assertion OK)
.venv-research/Scripts/python.exe lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/build_events.py

# The F2 guard that FM-1 exists to satisfy
grep -n "F2 GUARD" ops/instruments/MNQ.md

# The census this feature had to argue against (expect 40 / 67 / 94 and 78.1%)
grep -n "across all twenty" lab/archive/mnq_orderflow_probe_2026-08-04/RESULTS.md
```
