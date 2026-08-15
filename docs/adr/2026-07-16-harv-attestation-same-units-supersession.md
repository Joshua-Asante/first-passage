# ADR 2026-07-16 — HARV §R attestation: same-units, per-gate, panel-basis reachability (supersession after two firings)

**Status:** Accepted (operator, 2026-07-16 — same-day as drafting; the two campaign closures
**Decision date:** 2026-07-16
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
it cites were already final)
**Date:** 2026-07-16
**Supersedes (in part):** [`2026-07-13-harv-discovery-lane-ratification.md`](2026-07-13-harv-discovery-lane-ratification.md)
— the §2 attestation *specification* only. The mechanism-first lane itself, the HARD gate
(attestation blocks `register_search open`), and the register wiring all STAND.
**Trigger:** the parent ADR's own §4 falsifier **FIRED** on the H-OD-1 closure (2026-07-16),
with the same defect retro-diagnosed in the D5 closure (2026-07-16) — per its §Revert action
("superseding ADR citing the dated campaign closure; do not edit §2 in place").

---

## §1 — Context (what fired)

Both mechanism-first campaigns frozen since the parent ADR closed at the **Stage-2 cost-law**
under gates that were **structurally unreachable for their cohort-cited plausible-true
worlds**, and in both cases the frozen §R reachability simulation failed to flag the clause:

| Campaign | Cohort-implied true edge | Frozen 4× hurdle (panel basis) | §R defect |
|---|---|---|---|
| **D5** (`d5_nq_intraday_mom`, closed 2026-07-16) | ≈ 2.97 bp/session (δ/σ 0.113 × measured σ 26.26 bp) | **11.06 bp** | Stage-2 clause never simulated — §R argued Sharpe-space Stage-6 floor (0.65 vs gross 1.79) only |
| **H-OD-1** (`h_od_1_es_overnight_drift`, closed 2026-07-16) | 1.5 bp/session (SR917 Table I) | **5.05 bp** | Simulated in the wrong basis: recent index 4400 instead of the IS panel (median 1942, ~2.3× cost fraction) **plus** a ×10 commission mis-scaling ("≤0.03 bp" vs actual 0.27 bp @4400 / 0.62 bp @IS) |

"RESOLVED was unreachable *before data arrived*, again — and the simulation failed to flag
the clause": both conjuncts of the parent §4 falsifier, satisfied twice. Full arithmetic:
[`h_od_1 RESULTS.md`](../../lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md).

**Load-bearing nuance:** the mechanisms *transferred*. H-OD-1 reproduced the SR917 effect
almost exactly (+1.444 vs +1.5 bp, t≈5.0, positive all 9 IS years); D5's footprint was present
(ρ=+0.081, sign correct). What failed twice is the attestation method — it reasoned in
annualized-Sharpe space against the Stage-6 confirm floor while the campaigns died in bp space
at the Stage-2 cost gate. Neither closure therefore counts toward the **harvest-intake** ADR's
§4 doctrine falsifier (its parenthetical routes gate-geometry failures here): that count is
**0-of-2**, correcting the earlier STATE "1-of-2" line.

## §2 — Decision (the strengthened attestation specification)

The parent §2 HARD gate stands, with the attestation requirement re-specified:

1. **Per-gate, same-units.** §R must simulate **every** gate the campaign can die at —
   Stage-2 cost-law, Stage-6 confirm, placebo, temporal battery where bundled — **in that
   gate's own units**. A Sharpe-space argument discharges only a Sharpe-denominated gate.
2. **Cost-law clause (mandatory formula).** The attestation must exhibit the inequality
   `cohort δ (bp/event) ≥ 4 × RT_frac(panel-era median price)` with `RT_frac` computed from
   the frozen execution model **plus commissions — never waived as negligible without the
   division shown**. If the inequality fails at the adjudication panel's price basis, the
   clause is UNREACHABLE: redesign the gate/instrument or do not open the campaign.
3. **Adjudication-basis rule.** Every reachability quantity is computed at the basis the gate
   will actually be scored on (IS panel for Stage-2; OOS panel for Stage-6) — never a
   present-day or convenience basis.
4. **Two-defect provenance.** PD-1 (×10 commission mis-scaling) and PD-2 (price-basis
   mismatch) are named defect classes; future §R reviews check for both explicitly.

## §4 — Falsifier (for this amendment)

**H:** same-units, per-gate, panel-basis attestation is sufficient for the checklist form of
the HARD gate. **Falsified if** a future mechanism-first campaign closes on a clause that was
structurally unreachable at freeze **and** the rules above, correctly applied, would have
caught it (i.e. the failure is checklist non-application, not a new defect class): then the
checklist form is dead — supersede again with a **mechanical** gate (a `register_search open`
pre-flight that computes the §2.2 inequality from declared manifest fields and refuses).
**AMBIGUOUS** if no mechanism-first campaign freezes by 2027-02-08 — fold into the quarterly.

## §6 — Consequences / downstream artifacts (on acceptance)

- [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md): add the §2.2
  cost-law reachability inequality to the admission requirements (seeds whose event-scale
  cannot clear 4× RT at panel basis die at admission for the cost of one division — D5 and
  H-OD-1 would both have died there, saving two campaigns).
- Discovery-campaign template §R checklist: add rows for §2.1–§2.3.
- `.claude/skills/futures-anomaly-discovery/SKILL.md`: note the same-units rule.
- Optional later handoff: the §4 mechanical pre-flight in `register_search open`.
- Lesson: **M-20 (candidate)** in
  [`methodology_lessons.md`](../methodology/lessons/methodology_lessons.md).

**Cost of the miss (why this matters):** two campaigns' full freeze→GO→register→pull→screen
cycles (≈ $0 data, but two operator GO reviews, two Cursor/CC execution passes, and 2 family-K
banked — NQ/MNQ family 1, ES family 2) spent adjudicating gates that arithmetic available at
Stage-0 already decided.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Initial `Proposed` draft — same-units/per-gate/panel-basis §R attestation specification, triggered by the parent HARV-lane ADR's §4 falsifier firing twice (D5 + H-OD-1 Stage-2 cost-law kills under unreachable gates) | Claude Code (drafting) |
| 2026-07-16 | `Proposed` → `Accepted` (operator). Acceptance sweep executed same session: §2.2's cost-law inequality landed as **Requirement 5** in [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) §1 admission requirements (was previously non-binding sourcing guidance pending this acceptance); discovery-campaign template §R checklist rows added; same-units rule noted in `.claude/skills/futures-anomaly-discovery/SKILL.md`; M-20 lesson already CANDIDATE-status in `methodology_lessons.md` from same-day drafting, unchanged by acceptance | Joshua (accept) + Claude Code (sweep) |
