# Striker DJ30 v4.5 — MYM Edition (FUTURES_LOCK)

**Status:** JSON-ONLY ALERT PATH 2026-07-21 (informational `alert()` removal — rail alert-shadowing fix) after ALERT-PAYLOAD CONTRACT ADDED 2026-07-17 (Q-RAIL-1 B1, GO ADR [`2026-07-17-c1-rail-build-account-registration-go.md`](../../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md)). Supersedes B1 pin `42166af8…` (prior D1–D5-only pin `f89178d2…`; earlier `fd91f37b…` was already drifted/unrecoverable). **F3 acceptance PASS (2026-07-17) was scored against `f89178d2…`; both the B1 add and the 2026-07-21 JSON-only delta are alert-only — no `strategy.entry`/`strategy.exit`/`strategy.close_all`/sizing/DD/session logic changed, so F3's compile+parity+C3 evidence stands unmodified.** **NOT live.**
**Source:** `striker_dj30_v4.5.pine`, hash-verified vs `core/strategies/MANIFEST.sha256` at Gate B0 (2026-07-03).
**Edition file:** `striker_dj30_v4.5_mym.pine` (gitignored; hash pinned in [`PORT_MANIFEST.sha256`](../PORT_MANIFEST.sha256) — **`9439e3ff…`**, supersedes `42166af8…`).

## Venue deltas (the ONLY changes vs the locked CFD source)

1. **Integer MYM sizing, static account basis** — `qty = floor(accountSize·risk% / (slDist·$0.50/pt))`, RESERVE cap policy (base ≤ `floor(cap/(1+pyr%))` so the 750% add fits at full ratio). **Cap binds at discharge 100K:** `microCap=80` → base max 9 (see Q-RAIL-1 F2).
2. **Flooring visibility (R9)** — as MNQ edition.
3. **EOD force-flat, ET-pinned** — default ON; **15:45 ET** bar (executes ~**16:00 ET** = E1 build target; inside MFFU 16:10). Replaced the Bulenox-era 16:30→16:45 fill.
4. **Discharge-tier costs (Q-RAIL-1 D1)** — **$0.91**/side (Tradeify Select) + 1-tick slippage. **MFFU TV override: $0.95**/side.
5. **Discharge-tier account/cap (Q-RAIL-1 D2–D3)** — `accountSize` **$100,000**; `microCap` **80**.
6. **Promoted default (R8, retained):** day soft-stop default = **−1.15%** (automated-chain rationale; CFD Pine default was −2.00%). `maxDailyDD` 1.15 native. **Default change, not a locked-constant change.**
7. **Alert-payload contract (Q-RAIL-1 B1, 2026-07-17; JSON-only 2026-07-21)** — additive JSON `alert()` calls only, no order/sizing/DD logic touched: `leg_id="dj30_mym"`, `signal_type` (`entry`/`add`/`exit`/`flat`), `bar_time` (Pine `time`, epoch UTC), `close`, `stop_dist_pts` (`close - currentStop`, tick-rounded), per [`docs/spec/c1_watch_realization_multiplier_layer.md`](../../../docs/spec/c1_watch_realization_multiplier_layer.md) §2. `exit` (passive stop/limit) vs `flat` (Max Hold / EOD Flat / DD Limit) distinguished via a `lastCloseReason` marker set at each forced-close site, read once at the position-flat transition, then cleared. **2026-07-21:** plain-text informational `alert()` calls (entry/DD/trail/pyramid/BE/day-stop) were **removed** — a single TradingView "Any alert() function call" alert delivers only one `alert()` message/bar (`freq_once_per_bar`), so the informational alerts had shadowed the B1 JSON payloads and the rail routed no order. See [`PORT_MANIFEST.sha256`](../PORT_MANIFEST.sha256) header.

## Venue constants (Q-RAIL-1 2026-07-17)

MYM **$0.50/index-pt/contract**, tick 1.0 ($0.50). Target: Tradeify Select 100K / MFFU Rapid 100K.

## Acceptance checklist (operator-owed before any live use)

- [x] TV-native compile clean (CBOT_MINI:MYM1! 15m chart) — **PASS-implied 2026-07-17** via C3 1a–1c Strategy Tester exports.
- [x] **Per-candle parity vs CFD original:** **PASS-via-operator-override 2026-07-17** — MNQ-class clean not applicable; MYM vs corrected CFD `30a8e` on PEPPERSTONE:US30. Extra entry after T19 attributed to size→day-stop coupling (larger CFD size soft-halts; MYM still free) — **not** a port defect. Exit lags T9/T11/T12 absorbed under same override. Evidence: [`lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md`](../../../lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md).
- [x] C3 attribution ladder rungs 1a→1c — **PASS 2026-07-17** ([`STEP3_1C.md`](../../../lab/analysis/q_rail_1_2026-07/STEP3_1C.md)); MYM 1b short-window retention 72.6% vs ~89% caveat carried.
- [x] Hash re-pin in `PORT_MANIFEST.sha256` after edit — **done 2026-07-21** (`9439e3ff…`, supersedes `42166af8…` B1 pin).
- [x] Alert-payload contract (B1) — **landed 2026-07-17**; JSON-only path **2026-07-21**; F3 evidence unaffected (alert-only diffs, verified by construction — no re-run of Step-2/C3).

## Linkage

Q-RAIL-1 Phase 1 deltas: [`lab/analysis/c1/q_rail_1_2026-07/PHASE1.md`](../../../lab/analysis/c1/q_rail_1_2026-07/PHASE1.md). Re-author/delta driver: [`reauthor_editions.py`](../../../lab/analysis/q_rail_1_2026-07/reauthor_editions.py).
