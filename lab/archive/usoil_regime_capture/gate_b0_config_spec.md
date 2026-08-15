# Gate B-0 — native-parity config spec (operator-manual TradingView run)

**Status:** EMITTED for operator native run. CC cannot run TradingView (Gate B-0
is operator-manual). This file is the frozen input set Joshua runs in the
TradingView Strategy Tester; CC ingests the exports afterward and runs
`parity_check` + `rank_correlation_falsifier`.

**Pre-reg (FROZEN):** `docs/ltm/briefs/pre-registration/PREREG-USOIL-RGC-GATEB-2026-06-14.md`
(freeze commit `21c538b`). Grid = §3, N=36. Frozen B-0 thresholds (verified on
disk in `lab/validation/sweep/__init__.py`): `PARITY_NET_PF_BAND = 0.02`,
`PREFILTER_RANK_RHO_FLOOR = 0.70`.

**Candidate (emitted, gitignored):**
`core/strategies/candidates/concept-usoil-rgc-001.pine` (lint-clean; long-short
Donchian + chandelier trailing, no fixed TP; `useTrailing = true`). Sidecar:
`core/strategies/candidates/concept-usoil-rgc-001.sweep.yaml`.

**Feed / symbol:** `PEPPERSTONE:SPOTCRUDE`, 15m base bars, span 2020-01-01 →
2023-12-29. Canonical panel `BAR_EXPORT_v0.1_PEPPERSTONE_SPOTCRUDE_2026-06-13_c35c1.csv`
(SHA `256780f0…`; bar count 94,507, first bar 2020-01-01 23:00, last 2023-12-29
21:15). **Copied into the worktree `core/data/tv_exports/pepperstone/` 2026-06-14**
(gitignored vendor bytes — present for the Python sweep; the formal `SHA256SUMS`
line is added in a full-vendor environment, not the worktree, which lacks the
other 27 vendor CSVs).

---

## ✅ D-1 / D-2 RESOLVED by WI-5 (2026-06-14) — native run is no longer blocked

Both divergences below were found running this handoff and fixed in the codifier
(WI-5, commit `e1f7270`; TDD-green, full `lab/` 248 passed, zero `core/` mutation).
The candidate was **re-emitted** and is now §3-faithful — verified on disk:

- **(D-1) no entry filter** — `FILTER_REGISTRY` keys now require explicit "… filter"/
  "… gate" intent, so "volatility-targeted sizing"/"ATR exit" no longer attach a
  gate. Re-emitted Pine has **`signalFilterOK = true`** (no `atrLength`/`atrMaLength`/
  `atrExpansion` inputs). The frozen §3 "no entry filter" is now expressed.
- **(D-2) independent trail width** — `chandelier_exit()` now exposes a separate
  **`trailAtr`** input; `stopDist = exitAtr*stopAtr` (initial stop / sizing),
  `curTrailDist = exitAtr*trailAtr` (ratchet). The full N=36 (channelLen×stopAtr×
  trailAtr) is expressible; all sample cells below are runnable.

Pre-reg re-frozen **r2** (pre-data §3-table correction; original freeze `21c538b`
superseded). Historical detail of the original divergences is in the WI-5 commit /
codifier spec §8b — retained here only as the resolution record.

---

## Anchor config (Gate B-0 parity_check) — FROZEN, grid centre

Grid centre, confirmed a real cell of the N=36 cartesian product (cell index 13,
0-based, over `channelLen × entry_stopAtr × trailAtr`):

| §3 axis | value |
|---|---|
| `channelLen` (Donchian) | **384** |
| entry structure/vol stop `stopAtr` (×ATR14) | **3.0** |
| chandelier trail multiple | **3.5** |

Frozen (not swept), per §3: long-short symmetric · chandelier trailing only (no
fixed TP) · inverse-vol sizing via ATR stop · 24h / session-unconditional ·
oil-event gate OFF · **`exitAtrLength = 22`** (the single stop+trail ATR length —
⚠ the Pine input **defaults to 14**, so SET it to 22 in the Strategy Tester) · no
entry filter (D-1 resolved → no `atrLength`/`atrMaLength`/`atrExpansion` inputs
exist) · `riskPerTrade` left at the scaffold default 0.5 · `backtestMode = true`.

**Parity gate (anchor):** trade-count EXACT AND net-profit within `±0.02` AND
profit-factor within `±0.02` vs the native TradingView Strategy-Tester run on the
SAME `PEPPERSTONE:SPOTCRUDE` feed. (First-pass FAIL is *likely* for a fresh
execution model → operator iterates the execution model — do NOT tune the frozen
band.)

---

## Representative sample (rank_correlation_falsifier) — ≥8 cells spanning the grid

10 cells: all 8 extreme corners' worth of span (min/max on each axis) plus the
two centre cells, all unique, all real N=36 cells. Spearman ρ(Python-prefilter
rank, native rank) over this set must be ≥ `0.70`.

| # | `channelLen` | entry `stopAtr` | trail mult | grid idx | role |
|---|---|---|---|---|---|
| 1 | 192 | 2.5 | 2.5 | 0  | min-min-min corner |
| 2 | 960 | 3.5 | 4.5 | 35 | max-max-max corner |
| 3 | 192 | 3.5 | 4.5 | 8  | short channel / wide stops |
| 4 | 960 | 2.5 | 2.5 | 27 | long channel / tight stops |
| 5 | 384 | 3.0 | 3.5 | 13 | **anchor (centre)** |
| 6 | 576 | 3.0 | 3.5 | 22 | centre, longer channel |
| 7 | 384 | 2.5 | 4.5 | 11 | centre channel, tight entry / wide trail |
| 8 | 576 | 3.5 | 2.5 | 24 | tight trail / wide entry |
| 9 | 192 | 3.0 | 3.5 | 4  | min channel, centre stops |
| 10| 960 | 3.0 | 3.5 | 31 | max channel, centre stops |

> NOTE: all 10 cells are runnable as-is — **D-2 resolved (WI-5)**, the candidate
> now has an independent `trailAtr` input. Set `channelLen`, `stopAtr` ("Initial
> Stop (ATR)"), and `trailAtr` ("Trailing Stop (ATR)") per the row. The sample was
> frozen-before-native per pre-reg §7.

---

## Operator run instructions (per config)

1. Open the candidate Pine `concept-usoil-rgc-001.pine` in TradingView on
   **`PEPPERSTONE:SPOTCRUDE`, 15m**. Set the backtest date range to span the
   panel: **`startDate = 2020-01-01`, `endDate = 2023-12-29`** (load enough
   history that all 94,507 bars are present — parity needs the same bars the
   Python pre-filter uses).
2. Set the SIGNAL `input.*` values per the table for that config:
   `channelLen`, `stopAtr` (Initial Stop), `trailAtr` (Trailing Stop), and the
   frozen **`exitAtrLength = 22`** (Pine default is 14 — change it). Leave
   `riskPerTrade = 0.5` and `backtestMode = true`.
3. Run the Strategy Tester; export **"List of Trades"** to CSV.
4. Name each export so the config is unambiguous, e.g.
   `nativeB0_anchor_cl384_s3.0_t3.5.csv`, and drop them where CC ingests via
   `validation.ingest.ingest_trial` (the same parser the harness uses).
5. Return the CSVs; CC runs `parity_check` (anchor) + `rank_correlation_falsifier`
   (sample) and records the Gate B-0 verdict in `gate_b0_parity.md`.

Run the **anchor (cell 5 / idx 13)** first — if its `parity_check` fails (likely
on a fresh execution model), iterate the execution model (NOT the frozen 0.02
band) before running the other 9 sample cells for the rank cert.
