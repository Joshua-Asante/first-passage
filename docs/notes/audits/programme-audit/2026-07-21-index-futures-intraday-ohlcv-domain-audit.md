# Programme audit (object layer) — "single-instrument index-futures intraday OHLCV directional timing" discovery domain

**Layer:** OBJECT (empirical claims about market behaviour in a discovery domain; not a methodology).
**Audit window:** 2026-06-20 (first NAS100 ORB work) → 2026-07-21.
**Trigger:** degeneration-signal **#5 (SNAG pattern — multiple consecutive nulls in one domain)**, raised after the 2026-07-21 cross-index RV probe closed DROP; the operator asked whether the domain should be **domain-SNAG-closed** (like the 2026-07-01 free-data 5th-leg search).
**This audit's job:** decide the disposition **on the evidence**, not to ratify the requested closure. Per the protocol (Trap #1), §3 (seven questions + evidence) is written **before** §4 (verdict).

---

## §0 — Rule-0 reads (production/artifact source, verified 2026-07-21)

- [`docs/rejected_candidates.md`](../../../rejected_candidates.md) @ `82e338e` — the domain-SNAG **precedent** (5th-leg free-data search, "≈17–22 consecutive terminal closures with 0 admissions", the ~17–22 **bar**) + the same-week **ZF calibration** (2026-07-21: 3 Treasury constructs = "INQHIORI §6 tail-exhaustion, **NOT** a formal domain-SNAG closure — that bar in this file is calibrated to ~17–22 candidates, a different scale") + the exogenous-ORB-gate tail-exhaustion note (GEX/T10Y3M, "4 features … at tail-exhaustion").
- [`lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md`](../../../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md) @ `9620138` — **ORB-MNQ-1 admitted lifecycle `CANDIDATE @1.00×` 2026-07-16** (the domain's **survivor**; operator "admit it", full Stage 2–8 pipeline).
- [`lab/archive/d5_recost_2026-07/RESULTS.md`](../../../../lab/archive/d5_recost_2026-07/RESULTS.md) @ `e2658bf` — D5-RECOST FALSIFIED (Baltussen edge decayed OOS).
- [`lab/archive/xindex_rv_recon_2026-07/RESULTS.md`](../../../../lab/archive/xindex_rv_recon_2026-07/RESULTS.md) @ `82e338e` — cross-index RV DROP (dominated by ORB-MNQ).
- [`docs/briefs/rnd-pipeline/H-TSMOM-1-ES-tsmom-scoping.md`](../../../briefs/rnd-pipeline/H-TSMOM-1-ES-tsmom-scoping.md) @ `a6fd861` — H-TSMOM-1 Clause-N power FAIL (screen stage).
- [`docs/briefs/rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md`](../../../briefs/rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md) — H-OD-1 (ES **overnight** drift) Stage-2 cost-law KILL 2026-07-16 — noted as **adjacent** (overnight subdomain, venue-walled by flat-by-close), not core in-domain.

---

## §1 — Domain definition (scope discipline)

**In-domain:** a *directional intraday timing* edge on a **single liquid US equity-index future**, generated from **price/volume (OHLCV) structure alone**, deployable **flat-by-close**. Census of own closures + the survivor:

| # | Candidate | Verdict | Date | Failure mode |
|---|---|---|---|---|
| 1 | **ORB-MNQ-1** (opening-range breakout, native MNQ) | **ADMITTED — lifecycle CANDIDATE @1.00×** | 2026-07-16 | *survivor* (marginal, regime-conditional) |
| 2 | D5 (Baltussen last-30-min momentum, NQ/MNQ) | FALSIFIED — Stage-2 cost-law KILL | 2026-07-16 | edge real (+1.46 bp) but sub-cost |
| 3 | D5-RECOST (same, OOS re-derivation) | FALSIFIED — edge decayed | 2026-07-21 | OOS edge negative (−0.33 bp) |
| 4 | H-TSMOM-1 (ES time-series momentum) | Screen FAIL (Clause-N power) | 2026-07-16 | underpowered at Default-#1 N |
| 5 | Cross-index RV ranking (rotation over index futures) | DROP (necessary-condition) | 2026-07-21 | dominated by incumbent ORB-MNQ |

**Own in-domain closures = 4; admissions = 1 (ORB-MNQ).**

**Adjacent, NOT counted in-domain** (distinct sub-thread or subdomain, each with its own disposition): the **exogenous-ORB-gate** thread — Q-ORB-GEX-1 (2026-06-25), Q-ORB-T10Y3M-1 (2026-06-27), Q-ORB-FRIDAY-1 (2026-06-27), Q-ORB-VIXTS-1 (retired 2026-07-10) — is *conditioning on exogenous/calendar signals*, not OHLCV timing, and is **already recorded at tail-exhaustion** in `rejected_candidates.md`; and **H-OD-1** (ES overnight drift) is an **overnight** mechanism (venue-walled), not intraday-deployable. Even folding the 4 exogenous-gate closures in as a wide reading yields **≤8** closures — still ≈⅓ of the ~17–22 bar.

**External corroboration (not our closures):** two 2026-07-21 literature deep-searches (no stronger futures-native intraday candidate exists; the strong ones are venue-walled) + an independent MNQ 14-signal-family falsification (0/14 survive a 2-pt cost, arXiv 2605.04004).

---

## §2 — Prior art / lineage

- **Domain-SNAG precedent** (`rejected_candidates.md` §Domain-level SNAG closures): the free-data 5th-leg search, SNAG-CLOSED 2026-07-01 on **≈17–22 consecutive terminal closures with 0 admissions**. That is the calibrated bar and the only prior domain-SNAG in the registry.
- **Same-week tail-exhaustion precedent** (ZF closure, 2026-07-21): 3 distinct Treasury-complex directional constructs, 0 survivors → explicitly ruled **INQHIORI §6 tail-exhaustion, NOT a domain-SNAG**, because "that bar … is calibrated to ~17–22 candidates." Directly on point: a 3–4-closure exhaustion at this repo is tail-exhaustion, not SNAG.
- **Exogenous-ORB-gate tail-exhaustion** (already recorded): a related conditioning sub-thread noted at tail-exhaustion after 4 features — a raised bar, not a domain closure.

---

## §3 — The seven diagnostic questions (evidence first)

**1. Hard-core integrity.** Domain hard core = "a cost-surviving directional intraday OHLCV edge exists on a single index future." **Preserved and non-empty:** ORB-MNQ-1 (`9620138`) is a live admitted instance. The core has been *tested*, never violated under the domain's name — each closure is a specific-instance falsification, not a core abandonment. **Intact.**

**2. Belt-churn balance.** The "belt" = live candidate directions. Audit window: **4 removes** (D5, D5-RECOST, H-TSMOM-1, cross-index) + **1 durable add** (ORB-MNQ). **Net pruning**, and every remove is a recorded rejection with a re-proposal bar. This is convergence, not ceremony accretion — the *healthy* direction (Q2 green).

**3. Progressive evidence.** Predicted-and-corroborated results in-window: **(a)** ORB-MNQ predicted (opening-range breakout on native MNQ carries a cost-surviving edge) → cleared Stage 2–8 → admitted; **(b)** D5-RECOST predicted OOS edge decay (from the deep-search decay flags: post-publication decay + NY-Fed E-mini drift ~0 since 2021) → confirmed (−0.33 bp). The domain is **still producing corroborated predictions**, including sharp negative ones. **Progressive on its own evidence.**

**4. Degeneration evidence.** Any belt-patch existing only to rescue a prior conclusion? **None.** Every closure is an honest falsification on a pre-registered gate (cost-law, power, OOS decay, necessary-condition). D5-RECOST *strengthened* the parent rather than rescuing it; cross-index explicitly avoided best-of-window. **No degeneration.**

**5. Boundary respected.** Forbidden moves (re-tune, best-of-window, re-proposal without new mechanism)? **Respected and load-bearing:** D5-RECOST §5 forbade window-shopping and the full-OOS freeze held (git-auditable `2dad8f9`→`e2658bf`); the cross-index probe declared one RV window / one ORB, no sweep; no rejected candidate was re-proposed without new mechanism. **Boundary intact.**

**6. Theory-comparison performance.** Where alternatives existed, did the chosen test correctly rank them? **Yes:** the cost/edge-ratio levers were competed — price-level (D5-RECOST: moot, edge decayed), instrument-selection (cross-index: dominated, +2.64 vs +5.19 bp always-MNQ), hold-time (ORB-MNQ exit-at-close: the survivor). The counterfactuals were measured, not assumed; the dominated options were correctly identified as dominated. **Tracked.**

**7. Falsifier check.** Is there a pre-committed **domain-level** falsifier, and did it trip? **No domain-level falsifier exists** for this discovery domain. The nearest pre-committed falsifier is the portfolio-level prop §4 (11-08) — which was **DISCHARGED** (a survivor was admitted / Class-S c1 cleared), i.e. it fired *in favour*, not against. **No falsifier basis for a "Falsified" verdict.** (No threshold drift to report — there was no threshold to drift.)

---

## §4 — Disposition: **STABLE (saturating) — NOT a domain-SNAG. Requested closure DECLINED.**

The requested domain-SNAG closure is **not supported by the evidence**, on three independent grounds:

1. **A domain-SNAG requires 0 admissions; this domain has 1** (ORB-MNQ, `9620138`). A SNAG describes a domain that produced *nothing*; this one produced — and retains — a survivor. Closing a domain that contains our live candidate would be self-contradictory.
2. **The count is an order of magnitude below the calibrated bar.** 4 own in-domain closures (≤8 on the widest reading incl. the already-tail-exhausted exogenous-gate sub-thread) vs the registry's ~17–22 domain-SNAG bar. The **same-week ZF closure** already ruled a 3-construct exhaustion at this scale to be **INQHIORI §6 tail-exhaustion, not SNAG** — declining here is the *consistent* call; drafting a SNAG here would be the falsifier-drift the protocol (Q7 / Trap #5) forbids.
3. **Q1–Q6 are all green** (core intact, net pruning, progressive, no degeneration, boundary respected, counterfactuals tracked) and **Q7 has no tripped falsifier.** Nothing in the seven questions supports Degenerating or Falsified.

**Verdict = STABLE (saturating):** the domain is *mature and productive* — it delivered ORB-MNQ and is now yielding no *new* survivor per recent loop, with external evidence (two searches + MNQ 0/14) independently bounding it. That is Stable-with-watch, not exhausted-and-closed. Expected marginal yield of further *same-space* mining is low, but the correct response is a **raised re-proposal bar on new candidates**, not a domain closure that would also wall off the survivor.

---

## §5 — Follow-up actions (named)

1. **Land an INQHIORI §6 tail-exhaustion raised-bar note** (NOT a domain-SNAG entry) in `rejected_candidates.md` for *new* single-instrument index-futures intraday OHLCV directional-timing candidates. **Proposed bar** (a new candidate is not admitted for a full Pre-Q unless it clears one):
   - a **mechanism outside the mapped cost-ratio-lever set** (price / instrument-selection / hold-time are all mapped — a re-tune of any is the exhausted move); OR
   - a **different modality** (order-flow / microstructure — untouched per "don't buy explanatory data before a survivor") or a **venue** that relaxes a binding wall; OR
   - evidence it **beats the incumbent ORB-MNQ** net-of-cost, not merely clears the cost floor.
   Explicitly **preserves** ORB-MNQ (the survivor) and leaves the **session-confluence longer-hold** thread open (untested, low-priority). Owner: operator; ratify at/before **2026-08-08**.
2. **No portfolio/`core`/allocation/`dd_protection`/Pine action** — object-layer discovery-domain audit only; lock untouched.
3. **Deployment note (not a discovery action):** the domain's value now flows through the **c1 rail → B7** (ORB-MNQ / Class-S c1 already in hand), not through more mining — recorded here as context, not a spawned action.

---

## §10 — Audit hooks (runnable at next cycle)

```bash
# 1. Census integrity — the 4 in-domain closures + 1 survivor still resolve.
grep -c "cross-index-relative-volume-ranking" docs/rejected_candidates.md   # expect >=1
ls lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md lab/archive/d5_recost_2026-07/RESULTS.md \
   lab/archive/xindex_rv_recon_2026-07/RESULTS.md

# 2. Survivor still sole admission (SNAG would require this to become 0 AND count to reach ~17-22).
grep -n "CANDIDATE @1.00\|CANDIDATE @ 1.00" lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md

# 3. Re-audit trigger: if own in-domain closures reach ~17-22 AND ORB-MNQ is retired to 0,
#    re-open this audit for a genuine domain-SNAG verdict. Until then the raised bar governs.
grep -c "rejected 2026" docs/rejected_candidates.md   # tracks total registry growth (context)

# 4. Raised-bar landed (follow-up #1 discharged) — a domain-level guardrail entry exists.
grep -n "index-futures intraday" docs/rejected_candidates.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/notes/audits/programme-audit/2026-07-21-index-futures-intraday-ohlcv-domain-audit.md --type audit

# §0 anchors
git log -1 --format='%h %ci' -- lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md   # 9620138
git log -1 --format='%h %ci' -- docs/rejected_candidates.md                  # 82e338e (or later)
```

---

**Discipline-check summary:** seven questions answered with anchors ✓ · belt churn counted (4 removes / 1 add) ✓ · falsifier check executed (none pre-committed; portfolio-level discharged not tripped) ✓ · cross-layer contamination check — object-layer only, no methodology-performance citations ✓ · verdict assigned (STABLE, 1 of 5) with reasoning ✓ · follow-up named with owner + date ✓ · §10 hooks runnable ✓.
