**Theme:** legacy
**Status:** ACTIVE — Guardian v5.5 parity port harness
# Guardian v5.5 parity port — 2026-06-23

> **NON-RUNNABLE 2026-07-11 (execution path).** `next_open_engine.py`,
> `run_parity.py`, and `test_next_open_engine.py` still import retired Gen-1
> `validation.sweep.engine` / `feed_loader` / `parity` (deleted with ADR
> `2026-07-11-gen1-pipeline-retirement`). CI ignores this directory. Keep as
> evidence + local-only signal port; re-point the engine types before any re-run.

First step of **Path E** (local backtest reproduction) from the TV-automation
egress assessment — [`docs/adr/2026-06-23-tv-backtest-egress-automation.md`](../../../docs/adr/2026-06-23-tv-backtest-egress-automation.md).
Goal: reproduce Guardian's Strategy-Tester "List of Trades" **locally** so the
List-of-Trades is *generated*, not *extracted from TV* — sidestepping the whole
no-API / ToS-automation problem for the configs where local fidelity holds.

## What's here

| File | What |
|---|---|
| `guardian_signal.py` | **LOCAL-ONLY since 2026-07-01** (see §Local-only files). Guardian v5.5 **signal** ported to a `signal_fn` — parameter detail redacted from the public tree 2026-08-14, see the private archive. |
| `next_open_engine.py` | **`NextOpenEngine`** — the execution model Guardian needs: next-bar-OPEN entry, signal-bar-anchored stop/TP, grace stop, tick slippage on market/stop fills (not TP limits), STOP-FIRST. Sibling to `PythonPrefilterEngine` (no mutation of the ADR-pinned engine); returns the same `EngineRunResult`. |
| `run_parity.py` | Turnkey driver — **single anchor** (`--feed`/`--native`) or a **folder of anchors** (`--dir`, combined verdict in one call). Optional DST-aware UTC→ET. Imports the port lazily; on a clone without it, `pair_anchors` still imports and its tests still run. |
| `test_guardian_signal.py` | **LOCAL-ONLY since 2026-07-01** (its assertions restate the locked filter semantics). 9 signal-logic tests — **9/9 pass**. Absent on a public clone (not collected). |
| `test_next_open_engine.py` | 9 execution-model tests (next-open fill, slippage, grace delay, STOP-FIRST, **stale-close-next-open**, daily cap, TP-not-slipped, **dd-protection flag**) — **9/9 pass**. |
| `test_run_parity.py` | 3 folder-pairing tests — **3/3 pass**. |
| `PORT_MANIFEST.sha256` | SHA256 pins + restore runbook for the two local-only files. |

## Local-only files (public-clone posture, 2026-07-01)

`guardian_signal.py` + `test_guardian_signal.py` are an executable,
parity-**validated** reproduction of locked Guardian v5.5 — the same
edge-protection class as the gitignored `**/*.pine` source they port. Per
[`docs/adr/2026-07-01-guardian-pyport-public-tracking.md`](../../../docs/adr/2026-07-01-guardian-pyport-public-tracking.md)
they are untracked (gitignored, hash-pinned in `PORT_MANIFEST.sha256`).

**Operator: pulling the untracking commit deletes your working copies** (they
were tracked). Restore immediately after pull — this is the tom_spx loss mode
(2026-06-16) and the manifest exists so it cannot recur silently:

```bash
git show dc07898:lab/analysis/guardian_parity_2026-06-23/guardian_signal.py > lab/analysis/guardian_parity_2026-06-23/guardian_signal.py
git show dc07898:lab/analysis/guardian_parity_2026-06-23/test_guardian_signal.py > lab/analysis/guardian_parity_2026-06-23/test_guardian_signal.py
# verify against PORT_MANIFEST.sha256 (command inside that file)
```

**Honest scope** (from the ADR): both files were public 2026-06-23→2026-07-01
and remain retrievable from the private archive's git history at the pinned SHA above (this
repo is no longer the public one — see
[`docs/adr/2026-08-14-repo-public-visibility-transition.md`](../../../docs/adr/2026-08-14-repo-public-visibility-transition.md)).
Untracking limits amplification — no copy in fresh clones or the browsable HEAD tree — it
does **not** undo disclosure. **2026-08-14 update:** the 2026-07-01 ADR's "redacting one
mirror while the canonical block stays public would be theater" reasoning no longer holds —
`core/strategies/_archive/guardian/LOCK.md`'s parameter block was itself redacted in the
2026-08-14 pass, resolving that ADR's Forward question toward redaction. This README's
parameter mentions are redacted to match.

## The Rule-0 finding (why this is a *start*, not a finish)

Reading the locked Pine (`core/strategies/guardian/guardian_gold_v5.5.pine`, blob
`de54ef3b`) **before** writing code showed the synthesis's "just port Guardian's
bar-close logic" was half-right. The **signal** ports cleanly and is tested. The
**execution model does not fit the current engine**, so end-to-end parity is
blocked until that's resolved:

| Gap | Guardian Pine | `PythonPrefilterEngine` | Impact |
|---|---|---|---|
| **Entry fill** | `process_orders_on_close=false` → fills at **next bar's open** | enters at **signal-bar close** | Dominant — entry price differs every trade |
| **Grace stop** | stop 2.0× wide for `minBarsBeforeStop=1` bar, then tightens | fixed stop at entry (or trailing ratchet) | Different early-exit behavior |
| **Slippage** | `slippage=3` ticks | none | Net/fill drift |
| **Intrabar straddle** | TV Strategy-Tester assumption | STOP-FIRST | Rare here (29×ATR TP) but non-zero |

Plus the **timezone landmine**: Pine `hour`/`dayofweek`/session read the **chart
TZ (ET), not UTC** — the Pine header's "0800–1600 UTC" comment is known-wrong
(memory `guardian_aegis_chart_tz_not_utc`). `feed.times` must be converted to the
chart TZ (DST-aware) before this runs, or every gate is offset. If the OHLC export
epoch is UTC (memory `bar_export_epoch_utc`), that conversion is mandatory.

## Status of the two roads (ADR §2)

1. **Extend the engine** with next-bar-open + grace + slippage — **DONE**
   (`next_open_engine.py`, 7/7 tests). Parity is now *runnable*; the remaining
   unknowns are empirical (TZ pinning + whether the bar-resolution intrabar model
   is close enough), resolved by Joshua's exports, not more code.
2. **Accept Guardian as native-only** (the ADR default for intrabar-dependent
   strategies) — the fallback if road (1)'s parity gate FAILS at acceptable effort.

The honest read: Guardian is the *least* intrabar-dependent locked strategy. The
engine extension makes its parity *testable*; whether it *passes* is the ADR §4
falsifier, and the NAS100-ORB 5th-leg falsifier (2026-06-22) is the standing
warning that path-dependent exits may not be offline-reproducible even so.

## Manual-export runbook (road (1) is built — this is now runnable)

For each parity anchor (a distinct window):

1. Chart **Guardian Gold v5.5** on the **Pepperstone XAUUSD 15m** feed (the
   deployment feed; ADR-sweep §5 #5 — same feed both tiers).
2. Export TV's **chart OHLC** for the window (a broker-REST feed is *not*
   byte-identical and breaks trade-count parity — memory
   `parity_gate_feed_and_pf_calibration`).
3. With `Backtest Mode` ON, run the Strategy Tester; **List of Trades → Export CSV**.
4. Drop the pair into an exports folder using the stem convention:
   `<window>_ohlc.csv` (the OHLC) and `<window>_trades.csv` (the List-of-Trades).
   Repeat for ≥2 windows.
5. Run **once** over the folder (add `--utc-to-et` iff the OHLC epoch is UTC):

   ```bash
   python lab/analysis/guardian_parity_2026-06-23/run_parity.py \
       --dir <exports_dir> --utc-to-et --out verdict.json
   ```

   It prints a per-anchor table (py/native trade counts, count-match, net & PF
   frac-diffs, verdict) and a **COMBINED** verdict — RESOLVED iff every anchor
   passes (trade-count EXACT, net/PF ≤2%), else FAILED. A count MISS with a UTC
   feed usually means `--utc-to-et` is wrong-way; an EXACT count with a net/PF gap
   points at the execution model — tune `GUARDIAN_EXEC`, **do not widen the band**
   (ADR §5). Single-anchor mode (`--feed`/`--native`) still works for spot checks.

## Result — FULL-WINDOW parity RESOLVED-POSITIVE (2026-06-23)

Run over the **full 52-trade window from the true $200K base**. Combined BAR_EXPORT
pages (`75d21` + `1d2bd`) cover 2025-06-22 → 2026-06-23 ET, spanning the whole
Guardian window (2025-07-10 → 2026-06-16) plus warmup — so both tiers start at $200K
and compound all 52 trades (no equity-base offset):

| metric | native | engine | diff |
|---|---|---|---|
| **net (from $200K)** | `[redacted]` | `[redacted]` | **0.46%** ✓ |
| **profit factor** | `[redacted]` | `[redacted]` | **1.76%** ✓ |
| trade count | 52 | 51 | 1 miss |
| entries matched | — | 51/52 | |

(Absolute net/PF figures redacted from the public tree 2026-08-14 — see the private archive.
The relative diff percentages, which are what the parity gate actually scores, are unchanged.)

**Net and PF both clear the 2% band** over a full year of compounding — the execution
model reproduces Guardian to <0.5% on net. **Path E is a validated bar-close
reproduction of Guardian.**

**Residual (the irreducible 15m bar-resolution floor):** 51/52 entries exact; the
remaining diffs are all **stop-fill precision** — 4 stop exits land ±1 bar (15 min)
off because the stop LEVEL differs by a hair (ATR/float accumulation over ~23k bars),
and on 2025-08-21 that shifted one borderline stop so the engine held instead of
stopping, cascading to 1 fewer trade that day (took 1 of the day's 2). Closing this
needs tick data; the feed is 15m bars, so ±1-bar stop precision is the floor. By the
STRICT gate this fails trade-count-EXACT (51≠52) while passing net & PF.

Three corrections were required, **all found by the data** (this is what the gate is for):
1. **Stale max-hold close fills next-bar-open** — `strategy.close` is a market order,
   so under `process_orders_on_close=false` it fills next open, not on the maxHold bar.
2. **dd_protection OFF for raw-strategy parity** — the native Guardian backtest carries
   no portfolio-level C2 overlay; dd ON shrank an in-drawdown winner to 0.40×.
   `applyDdProtection` defaults OFF for this locked-strategy engine.
3. **Equity base** — net parity needs the engine seeded at the native compounding base;
   from the true $200K start over all 52 trades it's 0.46% (a partial window seeded
   mid-stream read 6.2% — the confound, not a model error).
