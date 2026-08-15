# Q-ICT-1M-ENTRY-1 / 5M execution substitution — CLOSURE: INSUFFICIENT-N

**Verdict:** `INSUFFICIENT-N` (the 5M entry produces a fillable but un-powerable population; HALT per the Q-ICT-REVCON plan §6 Phase-1 gate).
**Date:** 2026-06-20 · **Layer:** Q-ICT-1M-ENTRY-1 (TF-agnostic entry redesign, 5M chosen at the gate)
**Parent plan:** [`Q-ICT-REVCON-PLAN.md`](Q-ICT-REVCON-PLAN.md) (§6 Phase-1 table, INSUFFICIENT-N row) · **Inherits:** Q-ICT-CASCADE-1 1M closure ([`../ict_cascade_2026-06-18/CLOSURE-1M-INSUFFICIENT-N.md`](lab/archive/ict_cascade_2026-06-18/CLOSURE-1M-INSUFFICIENT-N.md), F9).

**Posture note.** The Q-ICT-REVCON plan gated Phase 1 (Q-ICT-1M-ENTRY-1) on Phase 0 = `RESOLVED-CONDITIONAL`. Phase 0 (Q-ICT-1H-REVCON-1) closed `NOT-CONFIRMED` (2026-06-19), which does **not** license Phase 1 under the plan's own gate. The operator nonetheless directed a Phase-1 probe as a **timeframe substitution** (1H P/D → 4H deferred; 1M execution → 5M). That is operator authority over the plan gate, logged. The probe independently lands at INSUFFICIENT-N, so the gate-skip did not manufacture a result.

---

## 1. Verdict — the substitution moved the wall but did not clear it

The 5M substitution was motivated by the 1M layer's two documented walls (F9): the `limit-on-return/mid/retraceK=6` entry filled **0/247** on 1m, and TV serves only ~2 days of 1m history. 5M addresses both in principle (`retraceK=6` → 30 min of fill-window; deeper 5m history). The operator ran the strategy on a **5M chart, all gates OFF, `useBody=false`** (the most-permissive cell) and exported the List-of-Trades (`ICT·X_PEPPERSTONE_US500_2026-06-19_73576.csv`).

| Question | Result |
|---|---|
| Does 5M break the 0%-fill wall? | **Yes** — real fills, 23 closed round-trips (vs 1M's 0/247). |
| Does it reach the n≥100 floor (PREREG-1M)? | **No** — n=23 over ~3.9 yr → **INSUFFICIENT-N** (frequency-starved, not fill-starved). |
| Is the point estimate robust? | **No** — **drop-top-1 → net −$3,051 (negative).** |
| Can F8 multi-regime be met from the canonical feed? | **No** — 5M × multi-year ≫ TV's tester bar cap; a ~2-yr trade gap is that wall (or trend-degeneration). |

---

## 2. The 23-trade sample (reconciled)

Internal-consistency gate (trade-csv-reconcile): Exit-row pairing sums to **+$3,654.81**, matching the file's final `Cumulative PnL USD` 3654.8 → no Entry+Exit double-count (trap #3). No Pine-header baseline exists for the ICT execution strategy (`references/baselines.md` has no entry), so this is an internal reconcile, not an anchor reconcile.

```
=== ICT execution (raid→FVG→DOL) — Pepperstone US500 5M, all-gates-off, useBody=false ===
Span      : 2022-05-11 → 2026-03-31  (~3.9 yr wall-clock; ~2-yr trade gap 2023-02 → 2025-03)
N         : 23 closed trades
WR        : 21.7%  (5 wins / 18 losses)
PF        : 1.262  (gross win 17,616 / gross loss 13,961)
Net       : +$3,654.81  (+1.83% on $200K)
Max DD    : ~$7,940 (-3.97%)  → RF 0.46
Sizing    : ~0.5%/trade fixed-R (losses cluster ~$1,000); ~static-$200K
Drop-top-1: T13 (+$6,706, 38% of gross profit) → net −$3,051 (NEGATIVE)
Drop-top-3: → −$9,474
TF check  : every entry/exit timestamp on a 5-minute grid (10:05, 09:50, 08:05…) → 5M confirmed
```

Low-WR / high-RR ICT profile: five wins carry the entire net; removing the single largest flips it negative. On n=23 that is not an edge — it is the D2/F8 drop-top-k fragility (D2 flipped on drop-top-3; this flips on drop-top-**1**).

---

## 3. The ~2-year trade gap — both readings close the same way

Operator confirmed **gates off** and **2023–24 loaded**, so the dead zone (2023-02 → 2025-03, zero trades) is not a gates-on or missing-data artifact. Two live explanations remain:

1. **TV bar-count wall, reasserted one tier up.** A contiguous 4-yr 5M backtest is ~300k bars; the Strategy Tester holds ~10–20k (~3–4 months of 5M). Even if 2023–24 was visible, the tester evaluates a bounded bar window — a true contiguous multi-year 5M backtest is not physically available from the canonical feed. This is F9's data wall, milder (1M ≈ 2 days → 5M ≈ months) but still short of the F8 multi-regime span.
2. **Trend-regime degeneration.** If every bar *was* evaluated, the raid→FVG entry produced zero setups across the entire 2023–24 bull trend — the structural tension flagged in the cascade closure (the P/D mean-reversion flavor fights a trend; bias∧PD goes near-contradictory). A finding, not a fluke.

Either way: the execution layer does not yield a powered, multi-regime, robust population on 5M from the canonical feed.

---

## 4. The offline-sim path — funded, then cancelled (operator)

The only path to a powered (n≥100, multi-regime) 5M test was a faithful **offline execution simulator** (port the order logic from Pine per Rule 0 / M-15; parity-validate byte-identical against this export on the overlap; then run over deep 5M `BAR_EXPORT` history). Cost: TV's 5M bar cap means deep history comes in ~3.5-month pages → ~13 stitched operator exports, against a drop-top-1-negative prior on a 3-null SNAG instrument whose same geometry family is already FALSIFIED (D2).

The operator **funded** this path (AskUserQuestion 2026-06-20), then **cancelled** it the same session and directed closure as INSUFFICIENT-N. No simulator was built; no Pine was re-anchored for the port; no further exports were requested.

---

## 5. Forbidden moves NOT taken (audit-clean)

- Did **not** re-tune the locked entry (`entryMode`/`fillEdge`/`retraceK`) or gate/target params to lift the trade count or the point estimate (PREREG-1M Forbidden; cascade closure §6).
- Did **not** read the 23-trade net/PF as a PASS — n=23 ≪ 100 and drop-top-1-negative; it is INSUFFICIENT-N, not a positive verdict.
- Did **not** port any of this to NAS100 (path-independence; the plan §5 forbids it; NAS100 has no ledger).

---

## 6. Lesson candidate (→ SPX500 ledger F10)

**A minute-class ICT execution layer is un-powerable on TV's canonical feed at 5M as well as 1m — for stacked reasons.** 1m starves on 0% fill (F9); 5m fills but starves on frequency (~6 trades/yr) *and* re-hits the tester's bar cap (no contiguous multi-year 5m backtest). The one time the execution family produced a measurable US500 sample, it was **drop-top-1-negative** — corroborating D2's robustness failure on the same geometry (belt evidence, n=23, not dispositive). Re-attempting native-feed 5m validation is closed; the only un-blocked path is an offline simulator over deep multi-page `BAR_EXPORT` history, which carries a negative prior and was operator-declined.

---

## 7. Disposition & follow-ups

- **Q-ICT-1M-ENTRY-1 → CLOSED INSUFFICIENT-N.** With Q-ICT-1H-REVCON-1 already NOT-CONFIRMED (2026-06-19), the **Q-ICT-REVCON re-investigation is fully closed** — neither fork produced a confirmed/deployable result.
- **Anti-SNAG:** INSUFFICIENT-N is not a falsification; the SPX500 null count stays **3/3 families**. This is additional un-deployability evidence on the ICT execution family, not a 4th null.
- **No re-run** on a wider/new-params 5m window (still sub-floor + bar-capped; re-proposing the same key returns DUPLICATE). The offline-sim path is the only re-entry, gated on a deep multi-page `BAR_EXPORT` corpus + a new mechanism reason to expect post-cost positive R (the n=23 prior is negative).
- **No `core/` / lock / allocation / dd_protection change.** Lock stands 99.83/0.17/4.37.
