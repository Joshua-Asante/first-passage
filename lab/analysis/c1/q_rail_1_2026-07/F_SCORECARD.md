# Q-RAIL-1 — Fidelity precondition scorecard (F1–F5)

**Date:** 2026-07-17  
**Parent brief:** [`docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md`](../../../docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md) §4 / §7 Phase 2  
**Phase 0 evidence:** [`PHASE0.md`](PHASE0.md)  
**F2 numbers:** [`f2_floors.json`](f2_floors.json) (driver [`f2_floors.py`](f2_floors.py))

Scoring vocabulary (brief §4): `PASS` / `FAIL` / `BLOCKED-ON-INPUT`. F1 already scored before this session.

---

## Scoreboard

| Limb | Score | Tier scope | One-line |
|---|---|---|---|
| **F1** WATCH-1 injection | **`PASS-via-fallback`** | book (both tiers) | Q-PYRPARITY-1 `FALSIFIED-NONPROPORTIONAL`; haircut at account-multiplier layer |
| **F2** Integer-sizing feasibility | **`PASS`** | both legs @ $100K × 0.50× | Floors ≪ $100K; base ≥1; pyramid adds survive RESERVE flooring |
| **F3** Deployable expression | **`PASS`** | both tiers | Locate+re-param+Step-2+C3+compile-implied **DONE** 2026-07-17 |
| **F4** Session/EOD semantics | **`PASS`** | both tiers (binding = MFFU) | E1 16:00 ET force-flat is implementable inside MFFU 16:10; Bulenox 16:45 fill is a Phase-1 retune, not a chain impossibility |
| **F5** ToS re-verification | **`PASS`** | both tiers | Automation posture unchanged at Tradeify FTA §6.6 + MFFU 8444599 (2026-07-17 fetch) |

**H-RAIL-1 status after this pass:** **cost clause still PENDING (Phase 4)** — F1–F5 fidelity limbs clear (F3 PASS 2026-07-17). Pre-registered AMBIGUOUS-HOLD check date **2026-08-01** applies only if a fidelity limb re-blocks; cost ceiling still owed before GO.

---

## F1 — WATCH-1 injection (prior)

**Score:** `PASS-via-fallback` (2026-07-17)  
**Evidence:** [`docs/briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md`](../../../docs/briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md)  
**Mechanism:** account-multiplier-layer haircut for DJ30/MYM + NAS100/MNQ (not TV `riskPerTrade` scaling).

---

## F2 — Integer-sizing feasibility

**Score:** `PASS`

Method: roll-seam-masked RMA ATR(11)×1.20 on `core/data/bar_data/{MYM,MNQ}_M15.csv` (SHA256SUMS: MYM `298ab8c8900f…`, MNQ `ddb14f569fb0…`). Floor = `(sl_pts · $/pt) / risk_frac`. WATCH-1 uses 0.50× locked risk (DJ30 **0.35%**, NAS100 **0.185%**). RESERVE policy: `base ≤ floor(cap / (1+pyr%))` so the add fits under the 80-micro firm cap.

| Leg | Window | ATR med | Floor @1.00× | Floor @0.50× | Base@100K W1 | Add (RESERVE) | Total | Base≥1 | Add survives |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| MYM | full-median | 37.73 | $3,234 | **$6,468** | 15 → capped 9 | 67 | 76 | yes | yes |
| MYM | recent-90d | 50.68 | $4,344 | **$8,689** | 11 → capped 9 | 67 | 76 | yes | yes |
| MNQ | full-median | 24.04 | $15,591 | **$31,183** | 3 | 30 | 33 | yes | yes |
| MNQ | recent-90d | 45.51 | $29,520 | **$59,039** | 1 | 10 | 11 | yes | yes |

Matches the brief's provisional band (STATE floors ×2: MNQ ≈$59K / MYM ≈$8.7K). Both legs afford ≥1 micro at $100K under the haircut; NAS100's add cohort survives integer flooring under RESERVE (10 micros at the binding recent-90d ATR — not zero). Cap headroom remains at both legs.

**Not scored here:** live TV qty-ceiling effects (already owned by Q-PYRPARITY-1 / F1 fallback). F2 asks whether the *integer micro math* clears, not whether TV risk%-scaling is proportional.

---

## F3 — Deployable expression exists and matches panel of record

**Score:** `PASS` 2026-07-17 — locate/re-param + Step-2 + C3 + compile-implied ([`PHASE1B.md`](PHASE1B.md), [`STEP2_PARITY.md`](STEP2_PARITY.md), [`STEP3_1C.md`](STEP3_1C.md))

| Check | Status |
|---|---|
| `striker_dj30_v4.5_mym.pine` on disk | **PRESENT** · pin `f89178d2…` · `pine_check` OK · D1–D5 applied |
| `striker_nas100_v1_mnq.pine` on disk | **PRESENT** (re-authored) · pin `a67fd3b4…` · `pine_check` OK · D1–D5 applied |
| Venue constants vs Tradeify/MFFU | **ALIGNED** (commission 0.91 / cap 80 / account 100K / EOD 15:45 ET); MFFU cost override 0.95 documented |
| Per-candle CFD parity (Step 2) | **PASS** — MNQ clean; MYM **PASS-via-operator-override**, re-affirmed 2026-07-18 against a corrected exit-lag census (9 lags, not 3; max +10 bars/2.5h, not "1–3 bars") — see [`STEP2_PARITY.md`](STEP2_PARITY.md) |
| C3 ladder 1a→1c | **PASS** — bands clear both $0.91/$0.95; MYM 1b short-window retention caveat carried |
| TV-native compile | **PASS-implied** by CME 1a–1c Strategy Tester exports |

**Carried caveat:** MYM 1b Net retention 72.6% vs C4 ~89% on the short 2025-09→2026-07 window — mechanism OK (winner EOD clips); not a port defect.

**Carried caveat (2026-07-18):** MYM Step-2 parity override re-affirmed against a corrected exit-lag census — see [`STEP2_PARITY.md`](STEP2_PARITY.md) for the full 9-row table and the operator re-affirmation quote. The discharging same-size control stays the open revisit condition, unchanged by the re-affirmation.

---

## F4 — Session / EOD semantics

**Score:** `PASS` (implementable)

| Fact | Source |
|---|---|
| Binding firm deadline | MFFU **16:10 ET** auto-liq (re-fetched 2026-07-17, article 9558251) |
| Envelope E1 build target | **16:00 ET** (≥10 min buffer) — [`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md) |
| Tradeify deadline | **16:59 ET** (envelope 2026-07-13 primary; help article body not re-rendered this session) |
| Current Bulenox editions | Force-flat on **16:30 ET bar → ~16:45 ET fill** — **too late for MFFU**; must retune in Phase 1 |

F4 asks whether EOD-flat + firm calendar are *implementable* on the chosen chain inside the binding minimum — not whether the Bulenox-parameterized editions already comply. A 16:00 ET (or earlier) force-flat trigger on the TV→CrossTrade→NT8 path satisfies E1 at both tiers. Record the Bulenox 16:45 fill as a **Phase-1 mandatory delta**, not an F4 FAIL.

---

## F5 — ToS re-verification

**Score:** `PASS` — see [`PHASE0.md`](PHASE0.md) §1.

No automation-posture change at either firm → no AMBIGUOUS escalation.

---

## Next

1. **Phase 4:** cost table (incl. CrossTrade Pro $49/mo floor) → operator §8 ceiling → GO/NO-GO packet.  
2. Optional: full-history 1a/1b pair if operator wants to re-test MYM ~89% retention outside the short window.
