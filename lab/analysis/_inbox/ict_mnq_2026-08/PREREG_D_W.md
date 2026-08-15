# Q-ICT-MNQ-1 / Layers D + W — VERDICT PRE-REGISTRATION (Part A)

**Registered before either layer's offline analysis is run on the delivered NQ/MNQ
exports. No criterion below may be moved after the first real-population run. The
commit of this file is the lock that lifts the firewall for the D and W layers.**

**Part A only** — this pre-registration covers the D (Daily) and W (Weekly) layers,
whose export data is already in hand. 1H and 1M are covered by a **separate**
`PREREG_1H_1M.md`, frozen before the databento pull (their data has not been
touched yet, so nothing is lost by deferring their freeze to that later commit).

Parent: [`docs/superpowers/specs/2026-08-03-q-ict-mnq-1-session-plan-design.md`](../../../../docs/superpowers/specs/2026-08-03-q-ict-mnq-1-session-plan-design.md)
(the approved session design). Sibling format: the archived
[`lab/archive/ict_cascade_2026-06-18/PREREG-D.md`](../../archive/ict_cascade_2026-06-18/PREREG-D.md) /
[`PREREG-W.md`](../../archive/ict_cascade_2026-06-18/PREREG-W.md), whose frozen
thresholds this pre-registration inherits **verbatim** — nothing below re-derives
or loosens either gate.

Authored: 2026-08-03. **Lock date: RATIFIED on this file's introducing commit.**

---

## §0 — Rule-0 + governance citations (verified this session)

| Source | What it grounds |
|---|---|
| `lab/archive/ict_cascade_2026-06-18/harness_d.py` (read in full, this session) | D-layer FROZEN constants (`DRAW_K=10`, `DISP_MLT=1.5`, `ATR_LEN=14`, `PV_LEN=3`, `USE_BODY=False`, `MC_DRAWS=5000`, `N_FLOOR=30`, D-4 grid `dispMlt{0,1.5,3.0} x pvLen{2,3,5}`), the verdict gate (`verdict_for_side`), and the loader (`load_daily_ohlc`) — accepts BAR_EXPORT-style pipe CSV or plain OHLC, used **unmodified** |
| `lab/archive/ict_cascade_2026-06-18/PREREG-W.md` §0 (read in full, this session) | W-layer object formula, transcribed in prose independent of the missing `.pine` bytes: `wEma = ta.ema(close, 20)`; `vStruct = gateBias = close > wEma ? 1 : close < wEma ? -1 : 0` (L28); `realized = sign(close - close[1])` (L92); `priorGateBias = gateBias[1]`; `gateScored = priorGateBias != 0 AND realized != 0` (L117-119); `gateHit = priorGateBias == realized` |
| `lab/archive/ict_cascade_2026-06-18/harness_w.py` (read in full, this session) | W-layer verdict gate (`evaluate_weekly`), used **unmodified**; only the loader is new (see §3) |
| `docs/notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md` | **`CONFIRM-FREE-NODEPLOY-2026-08-03`** — this campaign is a free statistical replication, not K-bound mechanism-first work; hard-committed to no deployment; covers **W and D confirmation only**, not 1H/1M |
| `docs/superpowers/specs/2026-08-03-q-ict-mnq-1-session-plan-design.md` §5 | Empirical roll-splice finding + exclusion rule (§4 below) |

**Dedup attestation (executed this session, pasted, not merely claimed):**

```
$ grep -inE "ICT|fair.?value.?gap|\bFVG\b|draw.on.liquidity|\bDOL\b|premium.discount|raid|sweep" ops/instruments/MECHANISMS.md
77:## ict-liquidity
79:ICT-style liquidity-sweep / fair-value-gap geometry (sweep -> FVG -> opposing-pool draw) used as an entry signal.
81:- Class finding: Sweep->same-direction-FVG->opposing-pool-draw direction is real on SPX500
  (p=0.0144) but fails robustness (drop-top-3 = -0.152R); the 1M 0%-fill wall is feed-general.

$ grep -rilE "ICT.*MNQ|MNQ.*ICT" docs/briefs/         -> no hits
$ grep -rilE "\bFVG\b|fair.value.gap" docs/briefs/     -> WSTRUCT-M2K-1, SLR-MYM-1 (both read
  in full this session; see the governance ruling doc for how they bear)
```

The registered `ict-liquidity` mechanism class describes a **different construct**
(sweep→FVG→opposing-pool entry signal, DEAD on SPX500) than either layer here (W =
weekly-close structural bias; D = draw-on-liquidity reachability rate) — this
pre-registration does **not** declare `ict-liquidity` as its vocabulary, and does
not need to (per the `CONFIRM-FREE-NODEPLOY` ruling, no `MECHANISMS.md` entry is
required for a non-candidate-generating confirmation).

**MNQ ledger** (`ops/instruments/MNQ.md`) read this session in full — no existing
ICT-family entry in its DEAD/ACTIVE lists; W1/W3/W4 standing warnings (roll-existence,
1m-fill wall, micro-era proxy discipline) are honored throughout (see §2, §4).

---

## §1 — Delivered data (operator TV exports, 2026-08-03)

| File (as delivered) | Instrument | Timeframe | Span (epoch-verified) | Bars |
|---|---|---|---|---|
| `BAR_EXPORT_v0.2_CME_MINI_NQ1!_2026-08-03_74b3d.csv` | NQ1! | Daily | 2016-07-05 → 2026-08-03 | 2,537 |
| `BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-08-03_88b46.csv` | MNQ1! | Daily | 2019-05-06 → 2026-08-03 | 1,823 |
| `BAR_EXPORT_v0.2_CME_MINI_NQ1!_2026-08-03_a9506.csv` | NQ1! | Weekly | 2016-07-05 → 2026-08-03 | 526 |
| `BAR_EXPORT_v0.2_CME_MINI_DL_MNQ1!_2026-08-03_03862.csv` | MNQ1! | Weekly | 2019-05-06 → 2026-08-03 | 378 |

Format identity (BAR_EXPORT pipe field) and timeframe were **verified from the
`Signal` column content**, not trusted from filename — the fourth file's "DL"
filename prefix does not match its actual `1W` timeframe field.

**Primary/secondary declaration (frozen, not chosen after seeing either result):**
**NQ is primary** for both D and W (full history, statistical power — NQ Daily has
2,537 bars vs MNQ's 1,823; NQ Weekly has 526 vs MNQ's 378). **MNQ is secondary**
(venue check on the instrument the live c1 leg actually trades, micro-era span
only, per MNQ ledger W4 — never used to rescue a NQ-primary null).

---

## §2 — Roll-exclusion rule (frozen, empirically derived)

**Measured this session** on `74b3d` (NQ Daily): a day-over-day open-vs-prior-close
gap scan found **17 gaps of +0.8% to +1.6%**, nearly all positive, each within **±4
calendar days of a 3rd-Friday-of-(Mar/Jun/Sep/Dec) CME quarterly expiry**, recurring
in **every quarter from 2022-09 through 2026-03** (magnitude trending up with index
level — the signature of an unadjusted front-month contango splice). The two
largest all-time gaps (2025-04, 2020-03) are genuine macro moves and fall **outside**
any roll week, confirming the roll-week cluster is a distinct, separate phenomenon.
TV's `1!` continuous series for NQ1!/MNQ1! is therefore **not back-adjusted**.

**Rule:** any D-layer pool/FVG object (§3) or W-layer scored week (§4) whose
**origin bar** falls within **±4 calendar days of the 3rd Friday of March, June,
September, or December** is excluded before scoring. For D, this is applied at
object-origin time (before the `drawK`-window scan); for W, the affected calendar
week is dropped from `gateScored` before the block-bootstrap CI (i.e. treated as
`gateScored=0` for that week, never imputed).

**Declared cost:** a seasonal (quarterly), not random, exclusion — the surviving
panel is a statement about non-roll weeks only, same shape as the precedent
`ROLL-EXCLUDE-2026-07-31` caveat, though this rule addresses a different mechanism
(within-series unadjusted splice, not a cross-feed seam — that ruling does not
itself apply here, see the design doc §5 correction).

---

## §3 — Layer D: frozen configuration (inherited verbatim from `PREREG-D.md` / `harness_d.py`)

No value below is re-derived or loosened. Cited to `harness_d.py`'s own docstring,
itself cited to the archived `PREREG-D.md` row.

| Parameter | Value | Status |
|---|---|---|
| K-window (`drawK`) | **10 days** | LOCKED |
| FVG basis | wicks (`useBody=false`) | REPORT-ONLY |
| Displacement filter | `dispMlt=1.5 × ATR`, `atrLen=14` | LOCKED headline |
| Pool pivot length (`pvLen`) | **3** | provisional headline |
| Pool t0 | true pivot bar | LOCKED |
| FVG t0 / touch guard | registration bar; touch scanned from `f.bar+1` | LOCKED (D-1 guard) |
| Base-rate null | radius-matched MC, **≥5000 draws/side** | LOCKED |
| PASS band | `real_rate > base_rate + 95% bootstrap CI half-width` | LOCKED |
| n-floor | **30 effective blocks** per side | LOCKED |
| D-4 selectivity grid | `dispMlt{0,1.5,3.0} × pvLen{2,3,5}` = 9 cells | LOCKED (report n-per-cell) |
| Verdict | **per side** (BSL/SSL), never pooled | LOCKED |

**Verdict gate** (unchanged from `PREREG-D.md` §6): `INSUFFICIENT-N` if no object
reaches the 30-block floor; `RESOLVED` if a qualifying object clears base+half-width,
both halves stay above base (stationary), and selectivity survives; `AMBIGUOUS-HOLD`
if it clears but is one-regime or selectivity-explained; `FALSIFIED` if an object
reaches the floor but none clears.

**Confirmation framing:** the original US500 run found **SSL bear-FVG RESOLVED**
(0.795 vs base 0.712) and **BSL + both pools FALSIFIED**. This run tests whether the
SSL.fvg side reproduces on NQ (primary) / MNQ (secondary) — per-side, so a BSL/pool
result here does not "rescue" or "contaminate" the already-settled US500 sides;
each side's verdict here stands alone.

**Runner:** a small new script, `run_d_layer.py` in this directory, that (a) loads
each CSV via `harness_d.load_daily_ohlc` unmodified, (b) applies the §2 roll
exclusion to the reconstructed bar set before calling `harness_d.evaluate`, (c)
writes the full per-side report. No change to `harness_d.py` itself.

---

## §4 — Layer W: frozen configuration (inherited verbatim from `PREREG-W.md` / `harness_w.py`)

| Parameter | Value | Status |
|---|---|---|
| Object under test | structure-only `gateHitRate` (`gateBias = vStruct`) | LOCKED |
| Structure definition | `close > EMA(close, 20)` → +1 / `<` → −1 / `==` → 0 | LOCKED |
| `emaLen` | **20** | LOCKED |
| Denominator | recompute from `gateScored`, never `mean(hit)` | LOCKED |
| Outcome | `realized = sign(close − close[1])`; one row per confirmed week; drop live bar | LOCKED |
| CI method | moving-block bootstrap (NOT binomial) | LOCKED |
| Block length `L_W` | smallest lag where step-1 outcome autocorr < 0.10, floor 1, cap 8 | LOCKED (GC-1, ratified) |
| n-floor | **30** scored weeks (block-reduced effective N) | LOCKED (GC-2, ratified) |
| Stationarity | halves AND thirds, chronological | LOCKED |
| Vote importance | **NOT-RUN** — see §5 | — |

**Verdict gate** (unchanged from `PREREG-W.md`): `RESOLVED` if block-CI lower bound
> 0.50 AND both halves > 0.50 AND all three thirds > 0.50 AND eff_N ≥ 30;
`FALSIFIED` if CI straddles 0.50 with eff_N ≥ 30; `AMBIGUOUS-HOLD` if CI lb > 0.50
but non-stationary; `INSUFFICIENT-N` if eff_N < 30.

**Confirmation framing:** the US500 run found structure-only `gateHitRate` **RESOLVED**
(0.5571, CI [0.5242, 0.5901], eff_N 910). This run tests whether the same
structure-only headline reproduces on NQ (primary) / MNQ (secondary).

---

## §5 — New W-layer adapter (the one genuinely new component)

`harness_w.py`'s `evaluate_weekly()` is used **completely unmodified** — only the
*loader* is new, because no Weekly-indicator data-window export exists (the source
`.pine` is lost). A new script, `build_w_export.py` in this directory, computes the
required columns (`time, gateBias, gateHit, gateScored, outcome`) directly from raw
Weekly OHLC, per the formula transcribed in §0:

1. `wEma[i] = EMA(close, 20)` — Pine's `ta.ema` convention: **not** SMA-seeded (that
   is `ta.rma`/Wilder, used elsewhere in this codebase for ATR); `ta.ema` is a plain
   recursive EMA starting at the first bar, `ema[0] = close[0]`, `ema[i] = α·close[i]
   + (1−α)·ema[i−1]` for `i>0`, `α = 2/(20+1)`. **Disclosed limitation:** the first
   ~60-80 bars (≈4× the length) carry a converging, less-reliable EMA — reported
   separately, not excluded, since PREREG-W declares no such warmup exclusion and
   inventing one now would be an undeclared, post-hoc rule.
2. `gateBias[i] = vStruct[i] = sign(close[i] − wEma[i])` (0 if equal).
3. `realized[i] = sign(close[i] − close[i−1])`.
4. `priorGateBias[i] = gateBias[i−1]`.
5. `gateScored[i] = (priorGateBias[i] != 0) AND (realized[i] != 0)`, **AND** the §2
   roll-exclusion (the calendar week's origin bar is not within a roll window).
6. `gateHit[i] = (priorGateBias[i] == realized[i])` — reported for scored rows only.
7. `outcome[i] = realized[i]` (satisfies `harness_w`'s `REQUIRED_CANON`).
8. Drop the live (last, unconfirmed) bar, exactly as `harness_w.de_overlap_scored`
   already does downstream — the adapter does not pre-drop it a second time.

**Vote-importance sub-verdict: `NOT-RUN` by construction.** The other three votes
(`vSeason`, `vRates`, `vEarn`) are only line-cited to the lost `.pine` file in
`PREREG-W.md`, never transcribed in prose — they cannot be faithfully reconstructed.
`harness_w.evaluate_vote_importance` already handles a votes-absent export correctly
(returns `NOT-RUN`, does not affect the structure-only headline) — this is the
existing, intended code path, not a new gap.

**Unit test obligation (before real data):** `build_w_export.py` must be tested
against a small synthetic OHLC fixture with a hand-computed expected `gateBias`
sequence, mirroring the archived `test_harness_w.py`'s own fixture discipline,
before it touches the real NQ/MNQ exports.

---

## §6 — Forbidden moves

1. **Citing this confirmation's result, if RESOLVED, as a deployability gate** for
   any future tradable expression — forbidden by the `CONFIRM-FREE-NODEPLOY-2026-08-03`
   ruling; any deploy attempt needs its own, fresh, K-bound proposal.
2. **Changing `emaLen` away from 20**, the D-layer's `drawK`/`dispMlt`/`pvLen`, or
   any other LOCKED value in §3/§4 after outcomes are seen.
3. **Re-tuning the §2 roll-exclusion window** (the ±4-day band) after seeing its
   effect on either verdict.
4. **Treating a votes-absent `NOT-RUN` sub-verdict as evidence for or against**
   the composite-vote claim — it is simply unmeasurable here.
5. **Cherry-picking NQ vs MNQ** after seeing which clears — §1 fixes NQ primary /
   MNQ secondary before either is scored.
6. **Extending this confirmation's scope to 1H or 1M** — those are separately
   pre-registered (`PREREG_1H_1M.md`) and the no-deploy ruling explicitly excludes
   them (they are fresh verdicts, not confirmations of a closed finding).
7. No `core/`, lock, allocation, `dd_protection`, Pine, or rail change.

---

## §7 — Audit hooks (runnable)

```bash
# This file's lock commit anchors the registration:
git log --oneline -- lab/analysis/_inbox/ict_mnq_2026-08/PREREG_D_W.md | tail -1

# Confirm the archived D/W harnesses are unmodified (byte-identical detectors):
git diff HEAD -- lab/archive/ict_cascade_2026-06-18/harness_d.py lab/archive/ict_cascade_2026-06-18/harness_w.py lab/archive/ict_cascade_2026-06-18/_ict_offline.py

# Confirm the governance ruling this pre-registration depends on:
grep -n "CONFIRM-FREE-NODEPLOY-2026-08-03" docs/notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md

# Confirm the frozen W formula transcription against its source line citation:
grep -n "vStruct = close > wEma" lab/archive/ict_cascade_2026-06-18/PREREG-W.md
```

---

## Amendment log (append-only)

- **2026-08-03 — RATIFIED.** Frozen on this file's introducing commit. No value
  changed from the archived `PREREG-D.md`/`PREREG-W.md`; §2 (roll exclusion) and
  §5 (W adapter) are the only genuinely new content, both fully specified before
  any NQ/MNQ verdict is computed.
