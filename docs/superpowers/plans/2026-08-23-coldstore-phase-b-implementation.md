# Coldstore Phase B — lifecycle disposition (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: PENDING OPERATOR GO.** Owning Phase A ADR [`2026-08-04-strategy-coldstore-phase-a.md`](../../adr/2026-08-04-strategy-coldstore-phase-a.md) **forbids** treating Accept as Phase B authority. This file is a plan, not a GO. Do not execute Tasks 2+ until a dated operator GO names this plan.

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

- [ ] **Step 1:** Retrieve the pruned design. Quote the Phase B section into the GO packet. If retrieve fails, STOP — do not invent Approach 3.
- [ ] **Step 2:** Draft the GO ask: what B writes, what it will not write. Leave Status of any new ADR `Proposed` until the operator speaks.

### Task 2: On GO only — disposition table

- [ ] **Step 1:** For each Phase A catalog row (`VENUE_LESS_CFD`, `VENUE_WITHDRAWN`, `PARKED_PROTOTYPE`, `FALSIFIED_PARKED`), write the authorization-axis action (usually **none** for VENUE_WITHDRAWN).
- [ ] **Step 2:** Tests: axis-separation — a B write does not change `BASE_RISK` / `DD_SCALE` / `TIER_MULTIPLIER`.

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
