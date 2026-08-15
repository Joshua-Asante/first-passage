# ADR 2026-08-09 — The GRAND Survive bound is the ≤5 queue cap, not an hours budget

**Status:** `Accepted` — ratified by operator (JA) 2026-08-09, in-session instruction ("make your best calls on … The Survive bound")
**Decision date:** 2026-08-09
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** governance convention. **$0 / K=0.**

## Decision

The portfolio-level **Survive bound** required by [`GRAND §2.5`](2026-08-09-grand-tier-quintessentials-binding.md) is the existing **≤5 operator-queue cap** in `STATE.md` — **concurrency-denominated, not hours-denominated**. No hours figure is set, now or later, and GSUB-1's concern **C-2 closes RESOLVED-BY-REFRAMING**: the bound was never missing, its *rationale* had been deleted.

## Grounds

An hours bound crosses [`Rule 2`](2026-06-16-rule-2-budget-before-acting.md) §5 #2 (*"expressing the budget in minutes anywhere in canon or ADR"* — *"neither client can meter wall-clock"*); greps find zero operator-hours quantities. GRAND §2.5 demands a resource ceiling but specifies no unit or number — all 17 KEEPs carry the field, so it is satisfied. Precedent: 4-session review trigger; `promotion_ceilings.json` (`max_concurrency: 2`).

## Reads

`docs/adr/2026-06-16-rule-2-budget-before-acting.md:99` · `STATE.md` OPERATOR QUEUE · GRAND ADR §2.5 · `git show d7b51b7:STATE.md:20-26` (deleted rationale, restored) · `docs/pursuits/` (37 records; 17 KEEPs carry the field, 0 in hours).

## Gate

RESOLVED — rationale restored in `STATE.md`, repairing the runnable check at `docs/notes/2026-07-29-comparative-advantage-thesis.md` (`rg -n "operator-hours" STATE.md`). Stale `(STATE.md L20)` line pointers remain fragile; prefer section refs. **FALSIFIED if** the ≤5 cap fails to ration attention (queue >5 at two consecutive quarterly gates, or work repeatedly served out of order); first check **2026-11-08**.

## Boundary

Do **not** quietly introduce an hours figure into a pursuit Survive-bound line (Rule 2 §5 #2 by the back door), nor build a time-metering subsystem to make an hours bound possible (Rule 2 §5 #6).
