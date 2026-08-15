# Striker NAS100 v1.0 — MNQ Edition (FUTURES_LOCK)

**Status:** JSON-ONLY ALERT PATH 2026-07-21 (informational `alert()` removal — rail alert-shadowing fix) after ALERT-PAYLOAD CONTRACT ADDED 2026-07-17 (Q-RAIL-1 B1, GO ADR [`2026-07-17-c1-rail-build-account-registration-go.md`](../../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md)). Supersedes B1 pin `139eb43d…` (prior re-authored pin `a67fd3b4…`; earlier 2026-07-06 pin `4bb37729…` lost locally). **F3 acceptance PASS (2026-07-17) was scored against `a67fd3b4…`; both the B1 add and the 2026-07-21 JSON-only delta are alert-only — no `strategy.entry`/`strategy.exit`/`strategy.close_all`/sizing/DD/session logic changed, so F3's compile+parity+C3 evidence stands unmodified.** **NOT live.**
**Source:** `striker_nas100_v1.pine`, hash-verified vs `core/strategies/MANIFEST.sha256` at Gate B0 (2026-07-03).
**Edition file:** `striker_nas100_v1_mnq.pine` (gitignored; hash pinned in [`PORT_MANIFEST.sha256`](../PORT_MANIFEST.sha256) — **`72b18a6d…`**, supersedes `139eb43d…`).

**⚠ EDGE-TRANSFER CAVEAT (Class-S context):** Q-P2-MEASURE-1 measured 29.82% CME-vs-Pepperstone signal divergence under the Bulenox residual program. c1's Class-S discharge is bust-geometry survival, not CFD-edge preservation ([Class-S ADR](../../docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md)). This edition is the deployable expression candidate for Q-RAIL-1 — acceptance checklists below remain mandatory before live use.

## Venue deltas (the ONLY changes vs the locked CFD source)

1. **Integer MNQ sizing, static account basis** — `qty = floor(accountSize·risk% / (slDist·$2/pt))`. **RESERVE cap policy:** base capped at `floor(cap/(1+pyr%))` so the pyramid add fits at full ratio under the firm contract cap.
2. **Flooring visibility (R9)** — qty==0 signals emit `plotshape` + `alert()` and still consume the daily cap.
3. **EOD force-flat, ET-pinned** — input-gated (default ON); closes on the **15:45** `America/New_York` bar (executes ~**16:00 ET** — envelope E1; ≥10 min inside MFFU 16:10). Entry session stays `hour(time,"UTC")` per source.
4. **Discharge-tier costs (Q-RAIL-1 D1)** — `cash_per_contract` **$0.91**/side (Tradeify Select default) + `slippage=1` tick. **MFFU TV override: $0.95**/side (`firm_rules.MFFU_Rapid_100K`).
5. **Discharge-tier account/cap (Q-RAIL-1 D2–D3)** — `accountSize` default **$100,000**; `microCap` default **80** (Tradeify Select / MFFU Rapid 100K).
6. No other change. All entry/exit/filter/session/risk% / pyramid% constants byte-carried from source defaults (day soft-stop remains source **−1.5%**).
7. **Alert-payload contract (Q-RAIL-1 B1, 2026-07-17; JSON-only 2026-07-21)** — additive JSON `alert()` calls only, no order/sizing/DD logic touched: `leg_id="nas100_mnq"`, `signal_type` (`entry`/`add`/`exit`/`flat`), `bar_time` (Pine `time`, epoch UTC), `close`, `stop_dist_pts` (`close - currentStop`, tick-rounded), per [`docs/spec/c1_watch_realization_multiplier_layer.md`](../../../docs/spec/c1_watch_realization_multiplier_layer.md) §2. `exit` (passive stop/limit) vs `flat` (Max Hold / EOD Flat / DD Limit) distinguished via a `lastCloseReason` marker set at each forced-close site, read once at the position-flat transition, then cleared. **2026-07-21:** plain-text informational `alert()` calls (entry/DD/trail/pyramid/BE/day-stop/floored) were **removed** — a single TradingView "Any alert() function call" alert delivers only one `alert()` message/bar (`freq_once_per_bar`), so the informational alerts had shadowed the B1 JSON payloads and the rail routed no order. See [`PORT_MANIFEST.sha256`](../PORT_MANIFEST.sha256) header.

## Venue constants (Q-RAIL-1 Phase 1 → 2026-07-17 apply)

MNQ **$2/index-pt/contract**, tick 0.25 ($0.50). Target tiers: Tradeify Select 100K / MFFU Rapid 100K (`firm_rules.py` `a53ee99`). RESERVE at cap 80 → base max `floor(80/11)=7`.

## Acceptance checklist (operator-owed before any live use)

- [x] TV-native compile clean (paste into Pine editor on a CME_MINI:MNQ1! 15m chart) — **PASS-implied 2026-07-17** via C3 1a–1c Strategy Tester exports.
- [x] **Per-candle parity vs CFD original:** **PASS 2026-07-17** — vs corrected CFD `4709d` on PEPPERSTONE:NAS100; 48/48 entry+exit times + signals identical (size differs by construction). Evidence: [`lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md`](../../../lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md).
- [x] C3 attribution ladder rungs 1a→1c — **PASS 2026-07-17** ([`STEP3_1C.md`](../../../lab/analysis/q_rail_1_2026-07/STEP3_1C.md)).
- [x] Hash re-pin in `PORT_MANIFEST.sha256` after edit — **done 2026-07-21** (`72b18a6d…`, supersedes `139eb43d…` B1 pin).
- [x] Alert-payload contract (B1) — **landed 2026-07-17**; JSON-only path **2026-07-21**; F3 evidence unaffected (alert-only diffs, verified by construction — no re-run of Step-2/C3).

## Linkage

Q-RAIL-1 Phase 1 deltas: [`lab/analysis/c1/q_rail_1_2026-07/PHASE1.md`](../../../lab/analysis/c1/q_rail_1_2026-07/PHASE1.md). Re-author driver: [`reauthor_editions.py`](../../../lab/analysis/q_rail_1_2026-07/reauthor_editions.py).
