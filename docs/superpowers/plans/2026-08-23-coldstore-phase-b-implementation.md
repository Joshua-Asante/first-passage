# Coldstore Phase B — lifecycle disposition (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: GO 2026-08-23.** Operator named this plan. Design body unrestored; Tasks 2+ executed from Phase A Approach 2 + frozen inventory. Owner ADR [`2026-08-23-strategy-coldstore-phase-b.md`](../../adr/2026-08-23-strategy-coldstore-phase-b.md).

**Goal:** After GO, record lifecycle (authorization-axis) consequences of catalog dispositions **without** collapsing venue-fit into book decay. Striker stays `AUTHORIZED · MECHANISM @ 1.00×` at book level unless the GO says otherwise.

**Architecture:** Likely an admitting ADR **or** a dated GO addendum on Phase A, plus a small `lifecycle_state.json` / methodology note. Catalog `VENUE_WITHDRAWN` ≠ `RETIRED`. Design spec was pruned from the public tree — retrieve `git show pre-prune-2026-08-08:docs/superpowers/specs/2026-08-04-strategy-coldstore-retirement-design.md` before inventing a B schema.

**Tech Stack:** Markdown + existing `core/lifecycle.py` API. No Pine parameter edits.

## Global Constraints

- No execution without GO.
- No `LEG_MAP` / `BASE_RISK` / Pine parameter change (those are Phase C / F2).
- Venue-binding registry (sibling plan) owns edition WITHDRAWN; Phase B must not write book `RETIRED` for Tradeify de-scope.
- Do not start Phase C from this plan.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Phase A ADR | `027a729` | B/C separately GO'd; non-touch list |
| Venue-binding ADR | `2c3b3c5` | WITHDRAWN is edition-level |
| 08-04 de-scope | `2c3b3c5` | Book AUTHORIZED intact |
| Design spec | pruned | Retrieve before schema invention |

---

### Task 1: Pre-GO (this campaign may do now)

- [x] **Step 1:** Retrieve failed (public clone + archive 404). Approach 3 not invented. Phase A Approach 2 + inventory used.
- [x] **Step 2:** Operator GO 2026-08-23. Admitting ADR `Accepted`.

### Task 2: On GO only — disposition table

- [x] **Step 1:** Disposition table on the Phase B ADR — **none** for every class.
- [x] **Step 2:** `tests/test_coldstore_phase_b.py` pins DD_*/TIER_MULTIPLIER / default AUTHORIZED.

### Task 3: Verification

```bash
git diff --stat -- core/dd_protection.py core/firm_rules.py ops/c1_rail/c1_sizing_host_reference.py
# expect empty unless GO explicitly named a file
grep -n "AUTHORIZED" docs/methodology/strategy_lifecycle.md | head -3
```

## Forbidden moves

- Executing B because Phase A is Accepted.
- Demoting Striker because Tradeify was de-scoped.
- Editing `LEG_MAP` or `BASE_RISK`.
- Starting Phase C.
