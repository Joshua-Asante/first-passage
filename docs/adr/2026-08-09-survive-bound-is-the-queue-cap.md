# ADR 2026-08-09 — The GRAND Survive bound is the ≤5 queue cap, not an hours budget

**Status:** `Accepted` — ratified by operator (JA) 2026-08-09, in-session instruction ("make your best calls on … The Survive bound")
**Decision date:** 2026-08-09
**Supersedes:** `2026-06-30-state-md-role-reduction.md` in part - the "only 2 headers" hook, re: the OPERATOR QUEUE section this ADR introduced.
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

## Addendum 2026-08-23 — Out-of-order serving is the live defect

**Does not amend** the concurrency-denominated ≤5 cap, the no-hours Boundary, or the 2026-11-08 first-check date. **$0 / K=0.**

**Rule 0 (this addendum):** [`STATE.md`](../../STATE.md) OPERATOR QUEUE @ `b378361` (2026-08-23) — two live rows, both waits (F1; B7/M1). This file @ `027a729` Gate — falsifier clause includes "work repeatedly served out of order". Cheap falsifier (plan Task 2): `rg -n "carry the prior|Carry the prior" .cursor/rules/session-discipline.mdc .cursor/rules/session-log.mdc .claude/hookify.session-log.local.md` — **3 hits**, one per wrap-up surface; [`docs/SESSIONS.md`](../SESSIONS.md) header L20–26 still tells the next session to resume from the prior Open/next; newest merged entry `2026-08-24n` leads with leftover names and only tags the queue as "unchanged."

**Live defect:** the ≤5 cap is intact; work is still served out of order. #1 and #2 cannot be executed (do-not-decide-early; wait on a strategy), so agents execute carried leftover names.

**Repair:** (1) Open/next lead line is the live STATE queue (`#1` … `#N`); (2) while #1/#2 stay waits, row 3 is a doable next step on an **existing** channel owner — operator GO 2026-08-23: blind / no-counterparty channel, name or decline the next construct on the reopened 6A/M6A or GC/MGC doors ([channel ADR](2026-08-15-no-counterparty-statistical-sourcing-channel.md)). Mechanical limb: `scripts/check_sessions_queue_bind.py` (newest SESSIONS Open/next vs live row numbers only).

**Succession:** when row 3 leaves, do not auto-open a channel or promote a leftover. Cite remaining rows until the operator promotes a replacement. Row 3 closed the same day — scoped decline of the reopened 6A/M6A and GC/MGC cell; last pre-G0 slot unspent ([channel ADR](2026-08-15-no-counterparty-statistical-sourcing-channel.md#addendum-2026-08-23--scoped-decline-of-the-reopened-6am6a-and-gcmgc-entry-geometry--dense-1m-cell)).

**Forbidden:** leftover names leading Open/next; a new generation channel to fill the doable slot; `tier: soft` on the checker; an hours figure (Boundary unchanged).

## Addendum 2026-08-24 — The blocker of B7/M1 is queue #1

**Does not amend** the concurrency-denominated ≤5 cap, the no-hours Boundary, or the 2026-11-08 first-check date. **Does not GO** any viable-strategy phase. **$0 / K=0.**

**Rule 0 (this addendum):** [`STATE.md`](../../STATE.md) OPERATOR QUEUE @ `57d8100` (2026-08-24) — sole live row is B7/M1, which names its own blocker (no book on the ruled host). Standing lead (same file) already pointed at the [`viable-strategy sequence`](../superpowers/plans/2026-08-23-viable-strategy-sequence-overview.md) (`AWAITING GO` @ `3ea7988`). This file's 2026-08-23 addendum still said #1/#2 "cannot be executed (wait on a strategy)."

**Live defect:** dependency order was inverted. The wait sat on the queue; the work that clears the wait sat off it as a "standing lead."

**Repair:** operator 2026-08-24 — promote the existing mechanism-supply owner to `#1`; B7/M1 is `#2` and waits on `#1`. Queue placement is not Phase A (or any phase) GO. 2026-08-23 repair (1) (Open/next is the live queue) stands. Repair (2) (row 3 while #1/#2 stay waits) is not the live repair.

**Forbidden:** treating this row as a phase GO; starting B7-REFIRE / arming; a new generation channel; an hours figure (Boundary unchanged).

## Addendum 2026-08-24 — M1 item 5 no longer waits on queue #1

**Does not amend** the concurrency-denominated ≤5 cap, the no-hours Boundary, or the 2026-11-08 first-check date. **Does not GO** any viable-strategy phase. **Does not** arm. **$0 / K=0.**

**Rule 0 (this addendum):** prior addendum on this file (blocker of B7/M1 is queue #1) @ `b855b4a`. [`STATE.md`](../../STATE.md) OPERATOR QUEUE @ `e7d2c8d` — `#2` still read “waits on #1.” [M1 addendum](2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24) — operator licensed a test strategy for item 5 and dated it 2026-08-24.

**Repair:** operator 2026-08-24 — M1 item 5 / B7 Stage 1 (unarmed) no longer waits on `#1`. `#1` stays the acceptable-strategy sequence. `#2` is dated 08-24 and is doable via the licensed test strategy. B7 Stage 2 / `dry_run=false` still waits on M1 `RESOLVED` + a separate arm GO.

**Forbidden:** treating the test-strategy license as an arm; collapsing Stage 1 into Stage 2; a new generation channel; an hours figure (Boundary unchanged).
