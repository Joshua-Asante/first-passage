# Q-INVENTORY-1 — verdict pre-registration (FROZEN)

**Frozen:** 2026-07-17, at operator ratification, before Phase 1 (per brief §8).
**Parent brief:** [`../Q-INVENTORY-1-zero-survivor-replenishment-disposition.md`](../Q-INVENTORY-1-zero-survivor-replenishment-disposition.md)
**Ratification record:** operator chat directive 2026-07-17 — "proceed with Q-RAIL 1 Phase 4 and Q-INVENTORY 1" — discharging the brief's sole pending gate (`OPEN — DRAFT (operator ratification owed)`). §8 carries no operator-set numbers; constants below are inherited by reference from the Q-KBUDGET-1 screen freeze `b304f2c` and the harvest doctrine, never re-derived.

---

## §4 — Falsifiable hypothesis (verbatim from brief)

**H-INVENTORY-1:** One bounded burst (scope frozen in §7: rank-1 citation traversal seeded from D5's paper + rank-2/rank-3 passes under the inherited Q1–Q6 families; ≤ 1 session; staging only) stages **≥ 1 seed** whose §1 requirements 1–5 all pass at sniff-arithmetic level (manifest block fully populated, screen-ready).

**Reject H-INVENTORY-1 if:** the burst completes its frozen scope with **0** admissible seeds → `FALSIFIED` and **accept-idle becomes the recorded default** (the 11-08 guard then fires as designed; that is the ADR's own success-eligible outcome, not a failure of this brief).
**Accept H-INVENTORY-1 if:** ≥ 1 seed stages with all five requirements passing and the §5 manifest block complete → inventory replenishes; seed(s) route to operator ratification then the standing screen.
**Ambiguous-hold if:** every staged candidate is `UNSCREENABLE` (missing input with a named recovery route — e.g., the carry timing-δ) and none is admissible outright → the disposition escalates to the operator as a **probe-funding fork**, not a silent re-run.

**Carry timing-δ sub-limb (pre-declared):** if carry re-surfaces as the best candidate and Req-2 remains UNSCREENABLE, this brief does NOT fund the δ-extraction probe — it prices it and hands the GO/NO-GO to the operator as a named fork in the closure.

## §6 — Gate criteria (verbatim from brief)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` (inventory replenished) | ≥ 1 staged seed passes §1 Req 1–5 at sniff level, manifest block complete | Seed(s) → operator ratification → standing screen. Idle guard becomes moot if any later reaches screen-PASS |
| `FALSIFIED` (band empty at this cost) | Frozen scope completes with 0 admissible seeds | **Accept-idle recorded as the default**: the 11-08 idle guard fires as designed; discovery effort stays parked pending new external evidence; deployment axis (Q-RAIL-1) unaffected. SESSIONS zero-survivor line DISCHARGED either way |
| `AMBIGUOUS-HOLD` | Only UNSCREENABLE candidates staged | Probe-funding fork to operator (carry timing-δ priced, not funded); re-check at the 08-08 packet |

## Phase-1 traversal scoping constants (frozen here, per brief §8)

- **Rank-1 seed paper:** Baltussen, Da, Lammers & Martens 2021, *JFE*, "Hedging demand and market intraday momentum" (D5's source — the only screen-PASS lineage).
- **Traversal method:** Semantic Scholar forward-citation graph; **influential-citation filter ON**; futures-cohort keyword requirement (`futures | E-mini | CME | per-contract`); review cap **≤ 50** influential citations (spec's tractability scoping).
- **Rank-2 scope:** survey / replication meta-studies (McLean-Pontiff-class; Q6 family verbatim: instrument-level futures δ or net Sharpe, not SPX-only).
- **Rank-3 scope:** futures-native journals (*JFM*, *JBF*, *JFQA*) under Q1–Q5 families verbatim (freeze `b304f2c` lineage via Q-KBUDGET-HARVEST-1 §E).
- **Sniff constants (inherited by reference, never re-derived):** Clause-K floors K_eff 1→0.65 · 2→0.85 · 3→0.98 · 4→1.06(FAIL), Cap 1.0; Clause-N `power = Φ(√N·|δ|/σ − 1.96) ≥ 0.50` at Default-#1 statistical OOS (2019-05-06→present: N≈86 monthly · ≈374 weekly · ≈1,800 daily); Req-5 `δ ≥ 4 × RT_frac(panel-era median price, commissions explicit)` — measured hurdles ES **5.05bp** / NQ **11.06bp** (IS-panel basis); other instruments computed per row at their own panel basis.
- **K-banks re-read 2026-07-17 (Phase 0):** GC/MGC **3,177** · ES **2** (h_od_1 + harv2026_001) · NQ-family **1 closed** (d5) **+1 open** (orb_mnq — conservatively counts: any new NQ seed sniffs at bank 2) · 6J/6E/CL/YM/others **0**.
- **Dead-class wall (Phase 0 emit — the burst must not re-stage):** month-end / turn-of-month (D3, D7, Q-HARV-1 §R DECLINED); monthly TSMOM at Default-#1 N (H-TSMOM-1, H-TSMOM-6J); intraday last-30m/ROD momentum on index micros (D5); overnight-drift / session-drift Tier-C siblings (H-OD-1; no size carve-out); any GC/MGC design; XAGUSD Guardian-family; EURUSD fixing-reversal; EURGBP Aegis port; USOIL spike-fader; micro-Treasury intraday MR; SPX dispersion; GEX/T10Y3M/Friday exogenous gates; carry-timing **as an admissible row** (stays UNSCREENABLE stub unless a per-instrument timing δ is found published — probe fork otherwise).
- **Stop rule:** Phases 1–3 fit one session; whatever is staged when the frozen scope completes is the answer. Zero manifest opens, zero `register_search`, zero pulls, zero K inside the burst.

Pre-registration commit hash: the commit landing this file (see `git log --oneline -- docs/briefs/pre-registration/Q-INVENTORY-1-verdict-preregistration.md`) · Date: 2026-07-17
