**Theme:** c1
**Verdict:** CLOSED — c1 rail Phases 0–4 CLOSED RESOLVED
**Status:** ACTIVE — c1 rail Phases 0–4 CLOSED RESOLVED; ceiling $700 operator-signed
# Q-RAIL-1 — Phase 0–3 + 1b RESULTS

**Date:** 2026-07-17  
**Branch:** `cursor/q-rail-1-f3-tv-acceptance` (Phase 3 rev 2 + orphan rescue)  
**Parent brief:** [`docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md`](../../../docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md)  
**Sizing spec:** [`docs/spec/c1_watch_realization_multiplier_layer.md`](../../../docs/spec/c1_watch_realization_multiplier_layer.md)

## Verdict

| Phase | Status |
|---|---|
| 0 — ToS / pricing / EOD re-verify | **DONE** |
| 1 — expression inventory + venue deltas | **DONE** |
| 1b — MNQ re-author + D1–D5 apply | **DONE** (operator GO) |
| 2 — F1–F5 scoring | **DONE** (F3 **PASS** 2026-07-17) |
| 3 — rail architecture | **DONE (rev 2)** — connection spine OK; §4 bridge screen PASS via NT8 host; DST calendar fixed |
| 4 — GO/NO-GO packet + §8 ceiling | **DONE** ([`PHASE4.md`](PHASE4.md)) — cost table complete; **ceiling $700 operator-signed** → cost clause ACCEPTS both tiers → **brief CLOSED `RESOLVED`** ([closure](../../../docs/briefs/closures/Q-RAIL-1-closure-resolved.md)) |

| F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|
| PASS-via-fallback | PASS | **PASS** | PASS | PASS |

**F3:** **PASS** 2026-07-17 — Step-2 parity ([`STEP2_PARITY.md`](STEP2_PARITY.md)) + C3 1a→1c ([`STEP3_1C.md`](STEP3_1C.md)) + compile-implied. MYM 1b short-window retention caveat carried. **Also owed for F1-realization:** alert-payload contract fields (spec §2) — Phase 1b did not land them.

**Phase 3 (rev 2 after adversarial REFUTE):** [`PHASE3.md`](PHASE3.md) — DST-aware presence (EDT 09:00–13:15 ET); bridge §2d screen vs [`c1_watch_realization_multiplier_layer.md`](../../../docs/spec/c1_watch_realization_multiplier_layer.md); E1 bridge floor **$49/mo Pro**; connection hops clear, implementability preconditions named (payload + NT8 sizing host + Pro AM).

**Phase 4 (2026-07-17):** [`PHASE4.md`](PHASE4.md) — all-in cost-to-first-live-fill (eval + 3 mo run-rate): Tradeify Select **$328** list / $258 promo · MFFU Rapid **$414**; worst case + one reset **$681**; shared run-rate **$49/mo** (CrossTrade Pro; NT8 $0; data $0-expected-UNVERIFIED). Tier recommendation: **Tradeify Select primary** (cost + softer EOD failure mode), MFFU fallback. Cost clause resolves on the operator's ceiling sign-off; until then PENDING.

## Artifacts

| File | Role |
|---|---|
| [`PHASE0.md`](PHASE0.md) | ToS quotes, eval prices, EOD re-check |
| [`PHASE1.md`](PHASE1.md) | Locate + venue-constant delta list |
| [`PHASE1B.md`](PHASE1B.md) | Re-author + D1–D5 + new pins |
| [`STEP2_PARITY.md`](STEP2_PARITY.md) | CFD timing parity + MYM operator override |
| [`STEP3_1A.md`](STEP3_1A.md) | C3 rung 1a CME baseline |
| [`STEP3_1B.md`](STEP3_1B.md) | C3 rung 1b force-flat retention |
| [`STEP3_1C.md`](STEP3_1C.md) | C3 rung 1c discharge costs + F3 PASS |
| [`PHASE3.md`](PHASE3.md) | Rail chain, DST attendance, §2d bridge screen, failure modes |
| [`F_SCORECARD.md`](F_SCORECARD.md) | F1–F5 scores |
| [`f2_floors.py`](f2_floors.py) / [`f2_floors.json`](f2_floors.json) | WATCH-1 floors |
| [`reauthor_editions.py`](reauthor_editions.py) | MNQ port + MYM delta driver |

## Forbidden moves honored

No account registration, no CrossTrade/NT8 wiring, no `ACTIVE_FIRM` switch. Pine edits limited to gitignored venue editions + FUTURES_LOCK / PORT_MANIFEST.
