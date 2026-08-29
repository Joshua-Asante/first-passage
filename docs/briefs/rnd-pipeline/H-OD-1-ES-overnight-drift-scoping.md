# Campaign scoping — H-OD-1 ES overnight-drift inventory-risk (02:00–03:00 ET)

**Status:** `CLOSED — Stage-2 cost-law KILL 2026-07-16 (gate-geometry defect; mechanism CONFIRMED-IS)` — full lifecycle: Stage-0 FROZEN + §8 GO (JA) → Stage-1 register (Cursor `95178dc`) + ES-parent IS pull ($0.00, local) → Stage-2 KILL: gross **+1.444bp** (t≈5.0, positive all 9 IS years — SR917 transferred) vs 4× passive hurdle **5.046bp** at the IS basis. The frozen gate was structurally unreachable at cohort magnitude (§R.1 PD-1/PD-2 — see the pre-reg's post-closure annotation); **HARV lane §4 falsifier FIRED**, amending ADR `Proposed` ([`2026-07-16-harv-attestation-same-units-supersession.md`](../../adr/2026-07-16-harv-attestation-same-units-supersession.md)); harvest-intake doctrine count **0-of-2**. Closure: [`RESULTS.md`](../../../lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md). Manifest closed, K=1 banked (ES → 2; H-TSMOM-1 keeps K_eff=3, floor 0.98).
**Axis:** harvest **H1** — `H-OD-1` overnight-drift inventory-risk; confirm window **02:00–03:00 ET**
**Lane:** mechanism-first (HARV ADR `Accepted` — HARD gate)
**Parents:** [`Q-KBUDGET-HARVEST-1`](../Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md) (`CLOSED-RESOLVED` 2026-07-16) · [inventory addendum](../Q-KBUDGET-HARVEST-1-inventory-addendum.md) · [`PHASE2_RATIFICATION.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md) (incl. the MNQ-expression amendment) · [`PHASE3_RESULTS.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md) · Boyarchenko/Larsen/Whelan, FRBNY Staff Report **SR917** (*The Overnight Drift*)
**Inheritance:** Campaign-defaults ADR 2026-07-11 + DSR-K supersession 2026-07-12 + HARV lane 2026-07-13 + harvest-intake ADR 2026-07-15
**Sibling precedent:** [`D5-NQ-intraday-momentum-scoping.md`](D5-NQ-intraday-momentum-scoping.md) (this doc follows its shape; D5 Stage-1 complete 2026-07-16)

---

## §0 — Grounding (Rule-0 anchors, read 2026-07-16)

| Source | Anchor | Supplies |
|---|---|---|
| [Inventory addendum](../Q-KBUDGET-HARVEST-1-inventory-addendum.md) §1 row H1 | RATIFIED 2026-07-16 (operator "accept both") | Family **ES → K_banked = 1** (Q-HARV-0); design K_intrinsic **(1, 2)** = unconditional hour + optional BtD (RSV<0); declared **N = 1000** daily OD events (~6.5y OOS); **δ/σ = 0.093** (SR917 Table I, t-scaled); Path **1a** |
| [`PHASE2_RATIFICATION.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md) amendment (same day, operator-directed) | source-verified vs SR917 + Liberty Street 2026-07 | SR917 quantifies **ES only** (Table I: +1.5bp/day, t = 7.1; Table IX: net-of-cost). Any **MNQ/NQ (or MYM) expression is `UNSCREENABLE:nq-native-delta-sigma-not-extracted`** — cross-instrument δ transplant inadmissible (intake ADR req. 2) |
| [`PHASE3_RESULTS.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md) | harvest §6 RESOLVED 2026-07-16 | H1 screen **PASS** — Clause K floor 0.85–0.98 ≤ Cap 1.0; Clause N power **0.837** |
| [`floor_scan.py`](../../../lab/archive/q_kbudget_1_2026-07/floor_scan.py) `floor_at_k` (frozen method, pre-reg §F hook #3) | recomputed this session (hook §5) | **floor(2) = 0.85 · floor(3) = 0.98 · floor(4) = 1.06 > Cap 1.0** — grounds the §0.5 P1 fork |
| [`ops/instruments/ES.md`](../../../ops/instruments/ES.md) | cited by Phase-2 amendment | ES micro sibling = **MES** |

**Honesty riders (ratified campaign-layer, not scoping kills):**
1. **Net-of-cost collapse:** unconditional OD Sharpe collapses net of bid–ask (SR917 **Table IX**). SR917 numbers are **gross**; this is the axis's known primary kill-risk and the §R attestation must model it explicitly (§2.5).
2. **2021+ fade:** RSV-dispersion compression (Liberty Street 2026-07 update) — post-2021 sub-window behavior rides into Stage-6 temporal consistency, not into the confirm clause.

---

## §0.5 — Open operator pins (decide before Stage-0 freeze)

| # | Pin | Options | Consequence |
|---|---|---|---|
| **P1** | **BtD conditional (RSV<0) in or out?** | **(a) H1-only, K_intrinsic = 1 → K_eff = 2, floor 0.85.** ES bank closes at 2; H-TSMOM-1 later screens at K_eff = 3 (floor 0.98 ≤ Cap) — **stays fundable**. **(b) H1 + BtD, K_intrinsic = 2 → K_eff = 3, floor 0.98.** ES bank closes at 3; H-TSMOM-1 later screens at K_eff = 4 (**floor 1.06 > Cap**) — **forecloses H-TSMOM-1** (L-cand-1: banked K forecloses a *family*). | The tension is real: the BtD conditional is the design's named fallback if the unconditional hour cannot clear net-of-cost (§2.5) — but it spends the family budget H-TSMOM-1 needs. If (b), say so knowingly in the pre-reg; if (a), the BtD variant is *gone from this campaign* (adding it after looking = K expansion, §3). |
| **P2** | Pull expression | Default (D5 precedent): **ES parent for IS + MES for OOS**, `.v.0` continuous volume-roll (Q-TVCOV-1 pin), cost-gated estimate first. δ is ES-cohort; MES leg is execution/cost realism only. | Freeze symbols/schema in pre-reg §5; vendor degraded days (2020-02-27/28, 2020-06-30 noted in D5 [`PULL_LOG.md`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/PULL_LOG.md)) → Stage-6 note |
| **P3** | Era split | Default: inherit campaign defaults — IS ≤ 2018-12-31 / OOS 2019+. Coincides with the cohort's published sample end, so OOS is genuinely post-publication and matches the ratified N = 1000 declaration. | Any override justified in pre-reg §8, not silently |

P2/P3 are defaults-unless-objection. **P1 is a genuine fork with a permanent consequence** — it is the one decision this brief exists to put in front of the operator.

> **P1 DECIDED 2026-07-16 (operator): (a) — H1-only.** K_intrinsic = 1, K_eff = 2, floor 0.85; BtD conditional OUT of this campaign (re-introduction = fresh Stage-0 + written foreclosure acceptance); **H-TSMOM-1 fundability preserved** (later screens at K_eff = 3, floor 0.98 ≤ Cap). P2/P3 defaults confirmed by the same directive. Frozen in the pre-reg §2.

---

## §1 — Pre-committed hypotheses (draft; formulas freeze in pre-reg)

Names only — exact entry/exit clocks, sizing, and cost model freeze at Stage 0:

1. **H1 (primary):** long ES during the 02:00–03:00 ET overnight-drift hour, unconditional, daily (SR917 inventory-risk mechanism; the window is the **cohort's**, not a sweep axis).
2. **H2 (optional — default OUT per P1(a)):** same window conditioned on prior-session RSV < 0 (buy-the-dip expression). Include only via P1(b) with the H-TSMOM-1 foreclosure accepted in writing, and only if a cohort-cited conditional δ is extracted from SR917 at pre-reg time — no invented effect sizes.
3. **H3 (placebo falsification clause — consumes no selection-K):** identical construct on a pre-committed disjoint session hour with **no overlap with any conditioning window** (Q-HARV-0 scar: a placebo nested inside the conditioning window is structurally un-passable), sized so a plausible-true world can still pass.

If a bundled clause cannot carry a reachability attestation, **drop it before freeze** rather than shipping an unreachable bundle (D5 precedent: H2 dropped at freeze).

---

## §2 — HARD gates before any pull (mandatory order)

1. **Author full campaign brief + verdict pre-registration** (template: [`discovery-campaign-template.md`](../../ltm/briefs/rnd-pipeline/discovery-campaign-template.md); target path `docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md`).
2. **Reachability attestation for every bundled clause** under a plausible-true world (HARV §2.4 HARD gate) — written file, non-empty. **The net-of-cost clause is the one that must be attested honestly here:** gross δ/σ 0.093 (~annualized 1.48 gross) clears floor 0.85 comfortably, but Table IX says the unconditional edge collapses net of bid–ask — the attestation must show net Sharpe ≥ floor is *reachable* under an explicit ES/MES spread + commission model, or the campaign should not open.
3. **`register_search open --lane mechanism-first --reachability-attestation <path>`** — binds K **onto the shared ES family bank** (P1 consequence becomes permanent here).
4. **Cost estimate → pull** only after (3); inherit P2/P3 pins; `--max-cost` gate on every pull regardless of $0.00 expectation.
5. **Campaign HARD quality bar:** **net-of-cost** Sharpe vs Clause-K floor **0.85** (K_eff = 2) / **0.98** (K_eff = 3) at the bound K_eff. Gross numbers never touch the verdict.

---

## §3 — Forbidden moves

- Pulling data before `register_search open` + attestation
- **NQ/MNQ or MYM expression of this axis** — the unburned-K lure the Phase-2 amendment exists to block; a native δ extraction (SR917 rev. 2022 cross-contract tables first) is a *new axis*, screened separately
- Re-introducing the BtD conditional after P1(a), or any RSV-threshold / window-boundary search — the 02:00–03:00 clock is the cohort's declaration, not a tunable
- Nesting the placebo inside the conditioning window (Q-HARV-0 structural scar)
- Quoting gross Sharpe against the floor (Table IX rider)
- Expanding K after looking (screen PASS voids if bound K exceeds the declared band)
- Treating screen PASS as survivor-scoring clearance — survivors still go to the frozen prop G4 gate
- Wide mining / STUMPY tiling on ES (Clause-K FAIL class; forecloses **both** remaining fundable axes)

---

## §4 — Next actions

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | Decide P1 (BtD in/out — the H-TSMOM-1 fork) + confirm P2/P3 defaults | Operator | **DONE 2026-07-16 — P1(a)** (H1-only; K_eff = 2) |
| 2 | Freeze Stage-0 pre-reg (exact H-set formulas, eras, cost model, §R attestation incl. net-of-cost clause) | CC | **DONE 2026-07-16** — [`H-OD-1-ES-overnight-drift-preregistration.md`](../pre-registration/H-OD-1-ES-overnight-drift-preregistration.md) (passive cost model frozen after §R.1 showed the crossing model un-passable; disjoint-hour placebo 20:00–21:00 ET) |
| 3 | Review §R attestation → GO/NO-GO (pre-reg §8) | Operator | **DONE 2026-07-16 — GO signed (JA)** |
| 4 | On GO: commit freeze artifacts → `register_search open` + cost-gated estimate/pull | Operator + Cursor | **DONE 2026-07-16** — freeze `9d5b2ec`; register (Cursor `95178dc`, then `BLOCKED — capability-problem` on the cloud key); ES-parent IS pull local, $0.00 ([`PULL_LOG.md`](../../../lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/PULL_LOG.md)) |
| 5 | Survivors → frozen prop G4 gate (same as Class-S) | Lab | **MOOT — Stage-2 KILL 2026-07-16** ([`RESULTS.md`](../../../lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md)); manifest closed, no survivor |

**08-08 packet:** H-OD-1 appears as **CLOSED (Stage-2 cost-law KILL, gate-geometry defect — mechanism CONFIRMED-IS)** alongside D5 (same closure class); **H-TSMOM-1 is the sole remaining fundable axis** (K_eff=3, floor 0.98), to be scoped under the corrected same-units attestation (amending ADR `Proposed`).

> **Correction (dated, added 2026-08-29):** the line above predates H-TSMOM-1's own same-day scoping. H-TSMOM-1 was scoped and CLOSED 2026-07-16 (Clause-N FAIL, P1 pinned to reading (c): N≈86, power=0.34, below the 0.50 threshold) — see [`H-TSMOM-1-ES-tsmom-scoping.md`](H-TSMOM-1-ES-tsmom-scoping.md). The harvest's ratified 3-axis fundable set (D5 / H-OD-1 / H-TSMOM-1) closed with zero survivors, not with H-TSMOM-1 pending. (The same-units attestation ADR cited here as Proposed was also Accepted the same day, 2026-07-16.)

---

## §5 — Audit hooks (runnable)

```bash
# Screen state this brief relies on (3 PASS incl. H-OD-1; RESOLVED)
python lab/archive/q_kbudget_1_2026-07/floor_scan.py | tail -3

# P1 fork numbers reproduce from the frozen floor function
python -c "import sys; sys.path.insert(0,'lab'); sys.path.insert(0,'lab/archive/q_kbudget_1_2026-07'); \
from floor_scan import floor_at_k; print([ (k, floor_at_k(k)) for k in (2,3,4) ])"
# expect: [(2, 0.85), (3, 0.98), (4, 1.06)] — 1.06 > Cap 1.0 forecloses H-TSMOM-1 under P1(b)

# Ratification + amendment anchors exist
grep -n 'H-OD-1' docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md | head -5
grep -n 'nq-native-delta-sigma-not-extracted' lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md

# Manifest exists and is CLOSED (post-2026-07-16 state; K=1 banked on the ES family)
python -c "import json; m=json.load(open('discovery_manifests/h_od_1_es_overnight_drift.json')); print(m['status'], m['K'], m['lane'])"
# expect: closed 1 mechanism-first
```
