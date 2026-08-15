# MSL-S2A — Stage G0 PREREG — pullback-failure resumption (MCL)

**Status:** `FROZEN` 2026-08-13 — explore **SCORED `FALSIFIED`** (N-ACT); Pine **not authorized**; CONFIRM unread. [closure](../../../docs/briefs/closures/MSL-S2A-closure-falsified.md) · [`RESULTS_g2`](RESULTS_g2.md)
**Date:** 2026-08-13 (freeze)
**Card / campaign:** MSL-S2A · [`STAGE1.md`](STAGE1.md) (`STAGE-1 PASS`)
**Parent charter:** [`docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md`](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) step 5
**Slate:** [`docs/briefs/2026-08-13-msl-second-slate.md`](../../../docs/briefs/2026-08-13-msl-second-slate.md) §MSL-S2A
**Box:** [`ADR 2026-08-13`](../../../docs/adr/2026-08-13-msl-slate-2-design-box.md) (`rr` ∈ [2, 3]; this freeze elects **rr = 3**)
**Mechanism id:** `pullback-failure-resumption` ([`MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md) NEW 2026-08-13)
**Intake gate:** [`TNEC-1`](../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (downstream of survivor MC; not this freeze)
**`K_intrinsic = 1`**. Cap disclosure-not-gate → DSR floor **0.650** at K=1 ([ADR 2026-08-04](../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)).
**Cost so far:** **$0.0000** · **K spent: 0** (freeze only).
**FROZEN ON THIS FILE'S INTRODUCING COMMIT.** No EXPLORATION path scores at freeze. CONFIRM unread.

---

## §0 — Rule-0 / Stage-1 discharge / door-check (parent-side)

| Check | Result |
|---|---|
| Stage-1 record | [`STAGE1.md`](STAGE1.md) @ `a37dba86` — three $0 limbs PASS at RT **$4.12**; cheap falsifier PASS; session window named before any read |
| Cost basis | `firm_rules.py` Tradeify comment pin `MGC=$1.06` @ `0356be26` + MCL tick_value **$1.00** × 2 sides → RT **$4.12**; 4× = **$16.48** |
| Cell door-check | `instrument_profiles.py cell MCL pullback-failure-resumption` → BINDING BAR `free-data-5th-leg-snag-closed-2026-07-01` answered **CLEAR by domain mismatch** under R-FRAMING **§2.1** |
| Index OHLCV raised bar | Does **not** bind (MCL non-index) |
| Adjacencies | Q-MCLTAS-1 TAS/settlement · CONFIG-B-MCL fade · USOIL spike-fader · CON-5 VWAP reclaim · slate-1 MR-at-level — **not** this construct |
| Implied-SR | Disclosure only ([ADR 2026-08-13](../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)). Not a freeze-time FAIL. Stage-1 placeholder p=0.35 is **not** an assumed-edge region. |
| Delete/flip (Req 1a) | **Declared mandatory; unpaid at freeze** — IS-only; must PASS before Pine/TV (see §4 / §6) |
| Panel | `core/data/bar_data/MCL_M15.csv` pin `5aa504567b943ff68506b8b5c21df293c5a553543fdf1ac606adeb0f5bfbbd23` ([`SHA256SUMS`](../../../core/data/bar_data/SHA256SUMS) @ `7c609ff6`). Bytes **absent** this clone; **unread** at this freeze. |

**Cheap falsifier (parent, 2026-08-13, this freeze):** recompute Stage-1 design point — R/ct **$180** vs 4×RT **$16.48**; all-win **$1,071.76** ≥ $200; all-lose **$368.24** ≤ $750 — **PASS**. Did not invent `p`. Did not read IS/CONFIRM. Door-check path still resolves on disk.

**Verdict:** Stage-1 + B4 license this G0 freeze. **Not** SHAPE-CLEAR. **Not** explore-scored.

---

## §1 — Universe and trade geometry (frozen)

| Element | Frozen value |
|---|---|
| Instrument | NYMEX **MCL** continuous (`MCL1!` / venue-equivalent micro WTI) |
| Signal TF | **15m** bars, exchange TZ mapped to **America/New_York** |
| Session window | **09:00–14:30 ET** (card-scoped; does **not** close the fade-program MCL window question). Start 09:00 is a disclosed dead NYMEX-floor artefact, not a CME-published RTH. |
| Flatten | **14:30 ET** — close of the CL settlement-determination period (14:28–14:30 ET). **Not** 16:00 equity close. |
| Direction | Join **failed-pullback resumption** only (continuation). Not fade, not through-break, not OR continuation, not VWAP reclaim. |
| Independence | **First valid signal per session only** (EM3 / N-SHAPE k=1). If both arms qualify on the same trigger bar, **skip the session**. |
| Cost | Tradeify Energy RT **$4.12**/contract (2×$1.06 + 2×$1.00); R = (pnl_usd − RT×qty) / stop_usd |
| Point / tick | **$1.00**/tick; 1 tick = **1.0 pt** = $1.00 |
| rr | **3** (geometry; inside elected box [2, 3]; not a measured-edge claim) |
| Stop | Structural at the **pullback-window extreme** ± **1 tick** buffer — **not** the Stage-1 $180 screen. $180 / 2-contract / 540-tick target remain the **design-point disclose** for $0 limbs; realized stop distance is a scoring parameter, not a selection axis. |
| Contracts (design disclose) | Stage-1 screen used **2**; live/explore qty is a scoring parameter, not a selection axis |
| Partitions | **IS** = session dates **&lt; 2025-07-01**. **CONFIRM** = **2025-07-01 → 2026-07-02** inclusive — **reserved unread through step 8**. Panel end is 2026-07-02; CONFIRM does **not** extend to “today.” |

**Not licensed:** opening-range reference; session VWAP; PDH/PDL; compression-expansion; TAS/settlement; CONFIG-B fade; additional trigger class (+1 `K_intrinsic` each).

### Calendars (frozen; identical IS and CONFIRM)

**FOMC (W4) — skip the whole session.** Estate 2022–2023 verbatim from `FOMC_DATES_ET` (`git show pre-prune-2026-08-08:lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/stage2_run.py`). 2024–2026 scheduled decision days hand-pinned from the public FOMC calendar (same provenance caveat; 2024-11-07 is Thursday). Unscheduled/emergency actions are **not** in this list.

```
2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-11-05 2025-12-10
2026-01-28 2026-03-18 2026-05-06 2026-06-17
```

**Roll — `ROLL-EXCLUDE-2026-07-31` ([ruling](../../../docs/notes/2026-07-30-tv-databento-roll-window-ruling.md) @ `103bd3fb`).** Same 2-session lead as the ruling (3 Globex sessions per roll). CME-calendar proxy frozen here because this clone lacks panel bytes and both feeds: for each CME CL last-trading day D in the panel span, exclude **D and the two preceding business days**. CME CL LTD = third business day prior to the 25th of the month preceding delivery; if the 25th is a non-business day, third business day prior to the last business day preceding the 25th. Business day = weekday minus the hand-pinned CME full-day closures below. Empty-bar sessions still drop at explore. Disclose: 2023 1m panel paid **14.01%** ([RESULTS_parity](lab/analysis/c1/tradeify_fade_stage0_2026-07-30/RESULTS_parity.md)); this M15 list is **162** dates (~14% of weekdays 2022-01-02→2026-07-02). Measured rate on this panel unpaid until explore enumerates hits against bars.

CME full-day closures used to compute the list (hand-pinned):

```
2022-01-17 2022-02-21 2022-04-15 2022-05-30 2022-06-20 2022-07-04 2022-09-05 2022-11-24 2022-12-26
2023-01-02 2023-01-16 2023-02-20 2023-04-07 2023-05-29 2023-06-19 2023-07-04 2023-09-04 2023-11-23 2023-12-25
2024-01-01 2024-01-15 2024-02-19 2024-03-29 2024-05-27 2024-06-19 2024-07-04 2024-09-02 2024-11-28 2024-12-25
2025-01-01 2025-01-20 2025-02-17 2025-04-18 2025-05-26 2025-06-19 2025-07-04 2025-09-01 2025-11-27 2025-12-25
2026-01-01 2026-01-19 2026-02-16 2026-04-03 2026-05-25 2026-06-19
```

Frozen excluded session dates (162; the load-bearing roll calendar):

```
2022-01-18 2022-01-19 2022-01-20 2022-02-17 2022-02-18 2022-02-22
2022-03-18 2022-03-21 2022-03-22 2022-04-18 2022-04-19 2022-04-20
2022-05-18 2022-05-19 2022-05-20 2022-06-16 2022-06-17 2022-06-21
2022-07-18 2022-07-19 2022-07-20 2022-08-18 2022-08-19 2022-08-22
2022-09-16 2022-09-19 2022-09-20 2022-10-18 2022-10-19 2022-10-20
2022-11-17 2022-11-18 2022-11-21 2022-12-16 2022-12-19 2022-12-20
2023-01-18 2023-01-19 2023-01-20 2023-02-16 2023-02-17 2023-02-21
2023-03-17 2023-03-20 2023-03-21 2023-04-18 2023-04-19 2023-04-20
2023-05-18 2023-05-19 2023-05-22 2023-06-15 2023-06-16 2023-06-20
2023-07-18 2023-07-19 2023-07-20 2023-08-18 2023-08-21 2023-08-22
2023-09-18 2023-09-19 2023-09-20 2023-10-18 2023-10-19 2023-10-20
2023-11-16 2023-11-17 2023-11-20 2023-12-15 2023-12-18 2023-12-19
2024-01-18 2024-01-19 2024-01-22 2024-02-15 2024-02-16 2024-02-20
2024-03-18 2024-03-19 2024-03-20 2024-04-18 2024-04-19 2024-04-22
2024-05-17 2024-05-20 2024-05-21 2024-06-17 2024-06-18 2024-06-20
2024-07-18 2024-07-19 2024-07-22 2024-08-16 2024-08-19 2024-08-20
2024-09-18 2024-09-19 2024-09-20 2024-10-18 2024-10-21 2024-10-22
2024-11-18 2024-11-19 2024-11-20 2024-12-17 2024-12-18 2024-12-19
2025-01-16 2025-01-17 2025-01-21 2025-02-18 2025-02-19 2025-02-20
2025-03-18 2025-03-19 2025-03-20 2025-04-17 2025-04-21 2025-04-22
2025-05-16 2025-05-19 2025-05-20 2025-06-17 2025-06-18 2025-06-20
2025-07-18 2025-07-21 2025-07-22 2025-08-18 2025-08-19 2025-08-20
2025-09-18 2025-09-19 2025-09-22 2025-10-17 2025-10-20 2025-10-21
2025-11-18 2025-11-19 2025-11-20 2025-12-17 2025-12-18 2025-12-19
2026-01-15 2026-01-16 2026-01-20 2026-02-18 2026-02-19 2026-02-20
2026-03-18 2026-03-19 2026-03-20 2026-04-17 2026-04-20 2026-04-21
2026-05-15 2026-05-18 2026-05-19 2026-06-17 2026-06-18 2026-06-22
```

A later TV↔Databento re-measurement that **differs** does not re-select — this list stays frozen. New G0 if the rule itself is replaced.

---

## §2 — ENTRY (causal; all constants a priori)

After each **15m** bar close `t` whose **open** is in **[10:45, 14:00] ET** inclusive (session 09:00–14:30; 7 lookback bars fit; entry at `t+1` open still flattens by 14:30):

Let **I** = the 4 bars immediately preceding **P**, and **P** = the 3 bars immediately preceding `t` (impulse 1h, pullback 45m; clock-structure constants, not scored knobs). All bars of I, P, and `t` must lie inside the same session window.

**Failed-pullback resumption → LONG**

1. Impulse net up: last close of I > first open of I.
2. Impulse made the higher high: max(high of I) > max(high of P).
3. Pullback occurred: min(low of P) < min(low of I).
4. Pullback failed to reverse: close(`t`) > max(high of P) (resumption close back through the pullback range).
5. Pullback did not extend on the trigger: low(`t`) ≥ min(low of P).
6. Enter **LONG** at next 15m open.
7. **Stop** = min(low of P) − **1 tick**.
8. **Target** = entry + **3** × (entry − stop); also flat at **14:30 ET** if still open.

**Failed-pullback resumption → SHORT** (symmetric about I/P highs/lows): impulse net down; impulse lower low vs P; pullback higher high vs I; close(`t`) < min(low of P); high(`t`) ≤ max(high of P); stop = max(high of P) + 1 tick; target = entry − 3 × (stop − entry).

**Arms:** long and short scored **separately**.

**Closed-door clearance:** ≠ `impulse-pullback-vwap-reclaim` (no VWAP) · ≠ `opening-range-continuation` / `opening-pressure` (no OR reference) · ≠ `pdh-pdl-breakout-rth` · ≠ `compression-gated-breakout` · ≠ `london-range-failed-extension-fade` / `pdh-pdl-failed-break-reclaim` (opposite family) · ≠ `event-window-reversal` / Q-MCLTAS-1 · ≠ CONFIG-B-MCL fade · ≠ USOIL spike-fader / `mean-reversion-fade` · ≠ `trend-following` / `band-pierce-continuation`.

---

## §3 — K and robustness probes (not selection)

- **`K_intrinsic = 1`** — single axis: pullback-failure resumption as frozen above.
- **Selection** is IS-only after explore GO; CONFIRM never used for selection.
- **Sweep axes pre-registered as robustness / plateau probes only** (not selection):
  - stop buffer ∈ {0, 1, 2} ticks (center = 1, frozen)
  - impulse window ∈ {3, 4, 5} bars (center = 4, frozen)
  - pullback window ∈ {2, 3, 4} bars (center = 3, frozen)
  - rr ∈ {2, 2.5, 3} (center = 3, frozen)
- Any post-freeze widening of reference class / direction / TF / session window / calendars = **new K** and a new G0.

---

## §4 — Scoring (EXPLORATION only; after operator explore GO)

| Limb | Definition |
|---|---|
| Delete/flip (Req 1a) | Constraint (impulse window + failed pullback) must SELECT the trade on **IS only**. DELETE sham = random in-session bar at matched time-of-day (slate). FLIP = join the pullback instead of its failure (enter with the pullback at the same trigger bar). **Mandatory before Pine/TV.** |
| Primary | Mean net R; session-block bootstrap 95% CI |
| Halves | Older/newer IS session-date halves |
| DSR | ≥ **0.650** at `K_intrinsic=1` (disclosure floor) |
| Cost-law | Gross/trade vs **$16.48** at realized stop distances |
| Disclose | WR · stop_dist · trades/session · coverage · $200/$750 at explored qty · EM six-char · entry-rate honesty (N-ACT) · implied-SR (report-only) |

**Entry-rate / N-ACT:** designed 1 entry/session still clears ≥1/week after ~14% roll-exclude. **If measured rate &lt; ~1/week, N-ACT FAILS as a solo construct: kill or redesign, don’t disclose.**

At G0 freeze: all TNEC N-* limbs **U**. Gate vocabulary at explore: `SHAPE-CLEAR` / `FALSIFIED` / `AMBIGUOUS-HOLD` / `VOID` as specified in explore GO.

**Deferred:** explore GO · delete/flip execution · Pine (CC-solo) · TV seat · survivor MC · Cap · rail/arming.

---

## §5 — Forbidden moves

- Path-scoring CONFIRM before step-8 survivor protocol; any CONFIRM peek voids the holdout.
- Inventing freeze-time `p` to gate implied-SR; treating Stage-1 placeholder p=0.35 as edge; treating Magdon-Ismail as an `R_max` calibration.
- Re-opening CONFIG-B-MCL fade, Q-MCLTAS-1 TAS, CON-5 VWAP reclaim, or slate-1 MR-at-level under this G0.
- Instrument hop after scoring; post-hoc filters after seeing results.
- Using a sweep/plateau probe result for **selection**.
- Self-authorizing Pine/TV without explore GO + delete/flip PASS + runbook links to steps 2–5.
- Closing the fade-program’s still-open MCL session-window question by this card-scoped 09:00–14:30 freeze.
- `dry_run=false` / arming / Striker redeploy.

---

## §6 — Path after this freeze

1. **This G0** — FROZEN on introducing commit (Rule 8.7).
2. Operator **explore GO** (unpaid) → IS harness + **delete/flip** → explore RESULTS. Restore/verify `MCL_M15.csv` sha256 `5aa50456…bbd23` before `--explore-go` if bytes are absent.
3. On explore PASS: **Pine CC-solo** (charter step 6; surface allocation — never fleets) + runbook linking steps 2–5 + this PREREG.
4. Operator TV (B5) → export → `msl_score` / survivor MC → TNEC string (steps 7–8).

---

## §7 — Audit hooks

```text
rg -n "CONFIRM|2025-07-01|K_intrinsic|pullback-failure-resumption|14:30" lab/analysis/c1/msl_s2a_mcl_2026-08/PREREG_G0.md
python3 scripts/instrument_profiles.py cell MCL pullback-failure-resumption
# expected: BINDING BAR free-data-5th-leg… still answered in STAGE1 / this §0 via §2.1
test ! -f lab/analysis/c1/msl_s2a_mcl_2026-08/EXPLORE_GO.md
# expected: explore token absent (GO unpaid)
```
