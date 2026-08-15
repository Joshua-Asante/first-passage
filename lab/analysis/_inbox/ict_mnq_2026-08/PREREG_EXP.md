# `Q-ICTEXP-1` — VERDICT PRE-REGISTRATION (gross-expectancy ceiling, native MNQ 1m)

**FROZEN ON THIS FILE'S INTRODUCING COMMIT. No criterion below may move after the first
real-population number exists. Zero expectancy figures have been computed at freeze time —
the chain population from Part C is known (55,604 raid-paired FVGs), but no P&L, no
excursion, and no R has ever been computed on this chain, anywhere, by anyone.**

**Scope:** [`Q-ICTEXP-1` scoping](../../../../docs/briefs/rnd-pipeline/Q-ICTEXP-1-ict-chain-gross-expectancy-scoping.md).
**K:** `0` — **operator-affirmed 2026-08-04**: *"run the probe, it's K-free"*, discharging scope §9.
**Cost:** `$0.00` (MNQ 1m regenerable at $0.0000, demonstrated twice). **No manifest. Cap seat untouched.**
**Class:** order-free, zero-run, zero-K — same class as [`ORB-MNQ-1`'s excursion-bounded kill tests](../orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md).
**Authored:** 2026-08-04 · Claude Code (Opus 5), operator-directed.

---

## §0 — Rule-0 reads, and the one that changed the design

All read in full this session. The load-bearing one is last.

- **`PREREG-1M.md` @ `47cc3eb`** — frozen 1M config. Transcribed and usable: `pvLen=2`, `raidWin=8`, `dispMlt=1.5`, `atrLen=14`, `useBody=false`, entry `limit-on-return` at **FVG mid** with `retraceK=6`, `dolMode="range-extreme"` (gate-bearing; `nearest-pool` REPORT-ONLY), `useDOL=true`, `minRmult=4.0`, `minAbsR=2.0`, `commPct=0.00002`, `slipTk=1`, `hurdleR=(2*commPct*entryEst + 2*slipTk*mintick)/stopDist`, tradeability floor `stop_dist >= max(1pt, cost)`, n-floor **100**, and the **block-resample-by-entry-event** rule (iid is *not* the verdict instrument).
- **`B2_B3_CHANGES.md` L90-97, L180 @ `47cc3eb`** — **the DOL target, transcribed in prose**: `dolPx = dolMode == "nearest-pool" ? nearestPoolPx(...) : h1High` for LONG, symmetric on `h1Low` for SHORT; *"`h1High`/`h1Low` are `[1]`-lagged HTF values (non-repaint)"*; skip rule `noDraw = useDOL and (na(dolPx) or dolPx <= entryEst)` long / `>= entryEst` short; orientation independently reviewed (*"correct orientation (long→high, short→low)"*).
- **`PREREG-1H.md` L28/L32/L45 @ `47cc3eb`** — the 1H range those extremes come from: **`lookN = 60` LOCKED** (*"must equal 1M `pdLookN=60`"*), computed as `ta.highest(high,lookN)[1]` / `ta.lowest(low,lookN)[1]`. So `h1High/h1Low` are fully determined.
- **`run_1m_diag.py` + `run_1m_probe.py` @ `9aaa578`** — the chain detector this probe extends: heap raid scan (`raid_bars`), `pair_fvgs_to_raids`, `build_fvgs`, `delayed_fill_stats`. **42 unit tests, re-run green this session.**
- **`core/firm_rules.py` @ `2345095`** — Tradeify `cost_per_side_usd = 0.91` (L304), the binding basis (live account).
- **`ops/instruments/MNQ.md` @ `71ad728`** — `$2.00/pt`; **N1** Tradeify `rt_pt 1.41`; **N10** the K arithmetic motivating a free probe; **W4** micro-era proxy discipline (satisfied: native MNQ).
- **`ops/prop_envelope_default.md` @ `cd8b617`** — **E1** EOD-flat, build target **16:00 ET**. Bounds the holding window (§1.3).

**⚠ THE READ THAT CHANGED THE DESIGN — the stop rule does not exist in prose.**
An exhaustive search found **no stop-placement definition anywhere in the ICT corpus**:

    $ grep -rn "stopDist|stop_dist|stopPx" lab/archive/ict_cascade_2026-06-18/*.md
      -> only inside the hurdleR formula and the tradeability-floor rule; never a definition
    $ grep -rln "stop below|stop beyond|stop at the raid|stop placed" lab/archive/ict_cascade_2026-06-18/ docs/
      -> 3 hits, all unrelated (c1 disaster-stop ADR, SLR-MYM-1's own stop, the fade design)

`stopDist` is line-cited to the lost `ict_1m_execution_DRAFT.pine` only — **the same class as
`netBias`**. The export column list (`raidSellPx, raidBuyPx`) *suggests* a raid-extreme anchor,
but suggestion is not transcription, and this pre-registration will not manufacture a locked
constant by inference.

**Consequence — every tier below is re-specified STOP-FREE.** `R` is `(price move)/stopDist`,
so any R-denominated quantity inherits the unknown. The fix is to run the whole probe in
**points**, where `stopDist` never appears. This is not a workaround: it removes an
unreconstructable constant from every verdict, so the conclusive limb is **stronger** than as
scoped, not weaker. It also mirrors the repo's own precedent — MYM D3 was closed by an
arithmetic in which *"contracts and stop-width cancel out."*

---

## §1 — Frozen design (stop-free, three tiers, one pass)

### 1.1 Population (T0)

Inherited verbatim from Part B/C, detectors unmodified: displacement FVGs (`dispMlt=1.5×ATR`,
`atrLen=14`, wick basis) with roll-window origins excluded (±4 days of 3rd-Friday
Mar/Jun/Sep/Dec), **raid-paired** per the declared mapping (SSL raid → bull FVG, BSL raid →
bear FVG, `0 <= i_fvg - i_raid <= 8`, `pvLen=2`).

An event **arms** at its FVG registration bar and **fills** iff the FVG mid is touched within
`retraceK=6` bars (bar-level touch, `bar+1` onward — the D-1 guard). Fill price = FVG mid.
Unfilled arms are **excluded from expectancy** (they are not trades) and reported separately.

**Applied:** the `noDraw` skip — an event is dropped if `dolPx` is `na`, or `dolPx <= fill`
(long) / `dolPx >= fill` (short). This needs only the target and the fill price: **stop-free.**

**NOT applied, by declaration:** `minRmult=4.0`, `minAbsR=2.0`, and the tradeability floor. All
three are R-denominated and therefore unreconstructable. **Their omission is generous** — each
only ever *removes* events — which is the direction this probe's whole design commits to. This
is the identical declared omission Part C made, for the identical reason.

### 1.2 The DOL target (frozen, transcribed)

`dolMode = range-extreme`. Resample 1m → 1H (UTC-hour buckets, OHLC). For a fill in 1H bucket
`b`: `h1High = max(high_1h[b-60 .. b-1])`, `h1Low = min(low_1h[b-60 .. b-1])` — 60 **completed**
buckets, the `[1]` lag, non-repaint by construction. LONG target `h1High`, SHORT `h1Low`.
Insufficient history (`b < 60`) ⇒ event dropped.

### 1.3 Holding window (frozen)

From the fill bar to whichever comes first: (a) the DOL target is touched, or (b) the **E1
flat deadline, 16:00 ET** (`America/New_York`, DST-correct), or (c) the panel ends. E1 is used
rather than an invented max-hold because any deployable expression must flatten by then — so the
window is generous *within the binding constraint*, and invents no parameter.

### 1.4 The three tiers — all in POINTS

| Tier | Quantity | What it bounds |
|---|---|---|
| **T1 — ceiling** | mean **maximum favorable excursion** in points from fill, over the §1.3 window (long: `max(high) − fill`; short: `fill − min(low)`) | **A strict upper bound on every possible exit rule** — any target, any stop, any trailing logic, any fill improvement is bounded above by exiting at the single best price in the window. Perfect foresight. |
| **T2 — frozen target, no stop** | mean **signed** move in points: exit at the DOL target if touched, else at the window close | The frozen construct's own exit, minus the one unreconstructable element. Generous on risk (no stop-out). |
| **T3 — disclosure** | median/quartiles of both, per-year, plus fill rate and drop-counts per filter | Context. **Never a verdict.** |

### 1.5 The bar (derived, not chosen; triple-confirmed)

Round-trip cost at the **Tradeify** basis (the live account):

    commission : 2 x $0.91            = $1.82  = 0.910 pt   (MNQ $2.00/pt)
    slippage   : 2 x 1 tick x 0.25 pt =         0.500 pt
    ROUND TRIP                        = $2.82  = 1.410 pt

Confirmed three independent ways: recomputed here; `MNQ.md` **N1** states Tradeify `rt_pt 1.41`;
ST-EH-1's frozen hypothesis states the costed 4× Tradeify hurdle as `>= $11.28/trade`, and
`4 × $2.82 = $11.28` exactly.

**BAR = 4.0 × 1.410 = 5.640 points ($11.28) of mean expectancy per filled event.** The 4.0×
multiple is the standing Stage-2 cost-law factor, not a choice made here.

> **The two-`4×` trap (PREREG-1M L57), honored:** this is the **verdict-gate** 4× — population
> mean expectancy vs 4 × round-trip cost. It is *not* the arm-time `minRmult=4.0` geometry
> filter, which is R-denominated and NOT APPLIED (§1.1). They are different objects and neither
> pre-satisfies the other.

### 1.6 Uncertainty

95% CI by **moving-block bootstrap resampled by entry event**, per PREREG-1M's frozen rule that
iid is not the verdict instrument for this family. Block = calendar day (an entry-event block;
same-day arms share the raid/FVG structure that F8's pseudo-replication dissent names).
`B = 2000`, `seed = 20260804`.

---

## §4 — Falsifiable hypothesis

**H-ICTEXP-1 (hypothesis under test).** The ICT raid→FVG→DOL chain on native MNQ 1m produces a
**perfect-foresight ceiling** (T1) whose entry-event block-bootstrap **CI upper bound** reaches
**5.640 points**, on **n ≥ 100** filled events.

**Falsifier — frozen trigger/threshold table. If a trigger fires, then the stated verdict
follows and no later tier is read for the verdict.**

| # | Trigger | Threshold | Verdict |
|---|---|---|---|
| X1 | `n` filled events after §1.1 | **< 100** | **`INSUFFICIENT-N`** — the identical PREREG-1M n-floor would bind the paid campaign. NO-GO stands. |
| X2 | **T1** mean MFE, block-CI **upper** bound | **< 5.640 pt** | **`FALSIFIED`** — conclusive. Perfect foresight already granted, so no exit rule, stop placement, target, or fill improvement can rescue it. `Q-ICT-1MEXEC-1` dies before opening; MNQ seat preserved. |
| X3 | T1 clears **and** **T2** mean signed move, block-CI **lower** bound | **< 5.640 pt** | **`AMBIGUOUS`** — real but unharvestable by the frozen exit. NO-GO stands (changing the exit is a new parameter, i.e. K). |
| X4 | T1 and T2 both clear | — | **`RESOLVED`** — the cheapest kill did not fire. **Licenses nothing** (§5 FM-1). |

**One line:** *if* a perfect-foresight ceiling cannot reach 4× round-trip cost, *then* the ICT
1M line is dead on expectancy at $0 and the seat is saved; *if* it can, *then* we have learned
only that the cheapest kill did not fire.

**Pre-registered expectation, recorded so a pass cannot be over-read.** T1 is a *perfect-foresight*
bound over a multi-hour window on a 1m instrument; **it is expected to clear 5.640 pt comfortably**,
and a T1 pass is therefore **not** evidence of edge and **not** a surprise. The informative cells
are **T2** and the T1↔T2 gap. Writing this down before measuring is the point: it makes X4
uninformative *by prior agreement* rather than by post-hoc concession.

---

## §5 — Forbidden moves

- **FM-1 — Reading `RESOLVED` (X4) as GO, as a reachability discharge, or as evidence the 0.980 annSR floor is attainable.** The highest-risk move in this document. A gross points ceiling is not a net annualized risk-adjusted Sharpe. X4 removes exactly one of the four NO-GO reasons; the `K_eff=3` floor vs Cap 1.0, the permanent MNQ foreclosure at `K_eff=4`, and the directive ADR 2026-07-12 clause all survive it untouched.
- **FM-2 — Any grid, sweep, or variant** on `pvLen`, `raidWin`, `dispMlt`, `atrLen`, `retraceK`, `lookN`, the block length, or the holding window. One frozen construct, one measurement. A grid is candidate generation and **consumes K**, destroying the reason this runs instead of `Q-ICT-1MEXEC-1`.
- **FM-3 — Switching `dolMode` to `nearest-pool`** after seeing `range-extreme` fail. PREREG-1M fixes `range-extreme` as gate-bearing and requires a *different pre-registration* for the alternative.
- **FM-4 — Inventing a stop.** The stop is unreconstructable (§0). Reintroducing an R-denominated quantity by assuming a stop anchor would smuggle a fabricated locked constant into a verdict. If a stop is ever needed, it is a new pre-registration.
- **FM-5 — Tuning any filter after seeing `n`.** `n < 100` is `INSUFFICIENT-N`, not an invitation to loosen `noDraw` or the roll exclusion.
- **FM-6 — Reporting T1 without T2**, or quoting either without the generosity ledger. A ceiling quoted alone reads as an estimate.
- **FM-7 — Any `core/`, lock, allocation, `dd_protection`, Pine, rail, `LEG_MAP`, K-ledger or manifest change**; no edit to `lab/archive/` (the byte-identity pin must keep returning empty). The c1 rail stays **disarmed**.

---

## §6 — Verdict gate (binary)

| Verdict | Trigger | Consequence for `Q-ICT-1MEXEC-1` |
|---|---|---|
| `INSUFFICIENT-N` | X1 | NO-GO permanent |
| `FALSIFIED` | X2 | NO-GO permanent; ICT 1M line closed on expectancy; MNQ ledger DEAD entry |
| `AMBIGUOUS` | X3 | NO-GO stands; record as a second "real but unharvestable" alongside `ORB-MNQ-1` **N3** |
| `RESOLVED` | X4 | NO-GO stands on reasons 1, 2 and 4; reason 3 discharged |

**No outcome promotes anything. The probe has no GO state.**

---

## §10 — Audit hooks (runnable)

```bash
# Freeze ordering must be git-auditable: this file's commit precedes RESULTS_EXP.md's.
git log --format='%h %cs' -- lab/analysis/_inbox/ict_mnq_2026-08/PREREG_EXP.md | tail -1
git log --format='%h %cs' -- lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_EXP.md | tail -1

# No K bound, no manifest opened (expect no match):
ls discovery_manifests/ | grep -icE "ict|exp"

# MNQ K bank still 2 (expect 1, then "2 operator-stopped"):
python -c "import json;print(json.load(open('discovery_manifests/d5_nq_intraday_mom.json'))['K'])"
python -c "import json;d=json.load(open('discovery_manifests/st_eh_supertrend_grid.json'));print(d['K'],d['closure_mode'])"

# Archived detectors byte-identical -- this probe extends, never edits:
git --no-pager diff HEAD -- lab/archive/ict_cascade_2026-06-18/

# The bar must reproduce from first principles (expect 1.410 pt / 5.640 pt):
python -c "print('rt=%.3f bar=%.3f' % (2*0.91/2.00 + 2*1*0.25, 4*(2*0.91/2.00 + 2*1*0.25)))"

# The transcribed target must still be transcribed (expect hits on h1High/h1Low + lookN 60):
grep -n "h1High" lab/archive/ict_cascade_2026-06-18/B2_B3_CHANGES.md
grep -n "lookN" lab/archive/ict_cascade_2026-06-18/PREREG-1H.md | head -3

# The stop must still be ABSENT in prose -- if this ever returns a definition, §1 can be revisited:
grep -rn "stopDist" lab/archive/ict_cascade_2026-06-18/PREREG-1M.md
```

---

## Amendment log (append-only)

- **2026-08-04 — RATIFIED/FROZEN** on this file's introducing commit. Zero expectancy numbers
  existed at freeze. The stop-free re-specification (§0, §1) was made **before** any measurement,
  as a consequence of a Rule-0 read, not in response to a result.
