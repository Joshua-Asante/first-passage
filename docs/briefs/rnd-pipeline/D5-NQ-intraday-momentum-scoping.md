# Campaign scoping — D5 NQ/MNQ intraday-momentum footprint

**Status:** `CLOSED — Stage-2 cost-law KILL 2026-07-16` (Stage-0 FROZEN + §R GO + Stage-1 complete; H1 failed 4× MNQ RT hurdle on IS).
**Axis:** D5 (was "gamma-positioning"; confirm-construct pinned to **intraday-momentum footprint**)
**Lane:** mechanism-first (HARV ADR `Accepted` — HARD gate)
**Parents:** [`Q-KBUDGET-1`](../Q-KBUDGET-1-axis-reachability-screen.md) (RESOLVED) · [`d5_clause_n_rescreen.md`](../../../lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md) · Baltussen et al. 2021 *JFE*
**Inheritance:** Campaign-defaults ADR 2026-07-11 + DSR-K supersession 2026-07-12 + HARV lane 2026-07-13

---

## §0 — Operator pins (Day 0, 2026-07-15)

| Pin | Value |
|---|---|
| Confirm construct | Intraday-momentum footprint (literature δ/σ = 0.113, NQ cohort) |
| Declined construct | Gamma-sign / dealer-positioning mechanism (no NDX/Dow cohort → was UNSCREENABLE) |
| Primary instrument | **NQ / MNQ** (NAS100 family expression) |
| DJ30 / MYM | **Drop or down-weight** (DIA/YM liquidity thin vs QQQ/NQ) |
| K_eff ceiling | ≤ 3 (Clause K Cap 1.0) — must match eventual `register_search` bind |
| Screen status | PASS (power 0.947 at N=1000) — licenses scoping only |

---

## §1 — Pre-committed hypotheses (draft; freeze in pre-reg)

Keep K_intrinsic ≤ 3. Draft working set (names only — formulas freeze in pre-reg):

1. **H1 (primary):** MNQ session open intraday-momentum continuation / fade as specified by the Baltussen-style construct adapted to native micro (exact entry/exit window frozen at Stage 0).
2. **H2 (optional):** same construct with a pre-committed alternate session window (must not become a free search).
3. **H3 (optional / placebo):** time-shifted or shuffled session placebo sized so a plausible-true world can still pass (Q-HARV-0 scar — do not nest placebo inside conditioning window).

If H2/H3 cannot carry a reachability attestation, **drop them before freeze** rather than shipping an unreachable bundle.

---

## §2 — HARD gates before any pull (mandatory order)

1. **Author full campaign brief + verdict pre-registration** (template: [`discovery-campaign-template.md`](../../ltm/briefs/rnd-pipeline/discovery-campaign-template.md)).
2. **Reachability attestation** for every bundled clause under a plausible-true world (HARV §2.4 HARD gate) — written file, non-empty.
3. **`register_search open --lane mechanism-first --reachability-attestation <path>`** — binds K; refuses without attestation.
4. **Cost estimate → pull** only after (3); inherit IS/OOS era defaults unless override is justified in §8.
5. **Campaign HARD quality bar:** net-of-cost Sharpe vs Clause-K floor **0.65–0.98** at declared K_eff (Baltussen numbers are **gross**; SPX tick-cost survival does not transfer automatically to MNQ).

---

## §3 — Forbidden moves

- Pulling data before `register_search open` + attestation
- Expanding K after looking (screen PASS voids if bound K exceeds declared band)
- Re-litigating gamma-sign as a silent third hypothesis
- Treating screen PASS as survivor-scoring clearance
- Wide mining / STUMPY tiling on NQ (Clause K FAIL class)

---

## §4 — Next actions

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | Freeze Stage-0 pre-reg (exact H1–H3 formulas, eras, cost gate, attestation) | CC | **DONE 2026-07-15** — [`D5-NQ-intraday-momentum-preregistration.md`](../pre-registration/D5-NQ-intraday-momentum-preregistration.md) (H2 dropped → K_eff=1; §R written) |
| 2 | Review §R attestation → GO/NO-GO | Operator | **DONE 2026-07-15** — §8 GO signed (JA); both clauses REACHABLE |
| 3 | On GO: `register_search open` + first estimate/pull | Operator + Cursor | **DONE 2026-07-16** — both Stage-1 legs cached $0.00 |
| 4 | Stage-2 cost-law → Stage-4 fixed construct | Lab | **DONE 2026-07-16 — KILL** ([`RESULTS.md`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md); mean +1.46 bp < 11.06 bp hurdle; manifest closed) |
| 5 | Stage-5+ (block size / DSR / placebo / realism / breadth) | Lab | **BLOCKED** — Stage-2 kill |

**Note on the frozen H-set:** the pre-reg drops H2 (alternate window) and keeps **H1 as the
sole primary candidate** (K_eff=1, floor 0.65 — the most beatable) + **H3 as a placebo
falsification clause** (disjoint-session, no conditioning overlap — consumes no selection-K).
This is the "drop before freeze rather than ship an unreachable bundle" call from §1.

**08-08 packet:** D5 = Stage-2 cost-law **KILL** (gross footprint present, not tradeable at 4× MNQ RT); not a cleared survivor. Harvest PASSes H-OD-1 / H-TSMOM-1 remain the live scoped axes.
