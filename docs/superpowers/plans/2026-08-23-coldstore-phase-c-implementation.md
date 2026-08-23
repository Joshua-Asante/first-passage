# Coldstore Phase C — hot-path code retirement (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: GO 2026-08-23.** Fresh admitting ADR [`2026-08-23-strategy-coldstore-phase-c.md`](../../adr/2026-08-23-strategy-coldstore-phase-c.md). Phase A Accept is still not C authority.

**Goal:** After GO, retire Guardian / Aegis (and only what the GO names) from living `BASE_RISK` / `firm_rules._BASE_RISK` / CLAUDE Strategy Reference — the CFD code-retirement limb scoped in [`2026-08-03-claude-md-futures-refocus.md`](../../adr/2026-08-03-claude-md-futures-refocus.md) §7 and deferred.

**Architecture:** New admitting ADR first (Rule 0 on `dd_protection.py` + `firm_rules.py` + `LEG_MAP` + Call-4 keys). Then a sequenced delete: docs pointer → tests → `BASE_RISK` keys → CLAUDE table. Striker futures keys stay until F2 says otherwise.

**Tech Stack:** Python constants + tests. No Pine parameter edits (hash-pin path moves already Phase A).

## Global Constraints

- No execution without admitting ADR + GO.
- Do not delete `LEG_MAP` Striker rows (F2 / rail).
- Do not touch `DD_TRIGGER` / `DD_SCALE`.
- Engine-support pre-flight if any firm class is removed from a path the MC still imports.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Phase A ADR non-touch | `027a729` | `BASE_RISK` / `_BASE_RISK` / `LEG_MAP` / lifecycle untouched in A |
| `core/dd_protection.py` `BASE_RISK` | `027a729` | Guardian / Striker / Aegis / Striker NAS100 still present |
| Futures-refocus ADR §7 | (related) | CFD code retirement scoped, not executed |

---

### Task 1: Pre-GO — admitting ADR outline (this campaign may draft `Proposed` only if asked)

- [x] **Step 1:** Subscript consumers were two test files (cheap falsifier). Derived: MC ALLOCATIONS, verify_lock_anchors, recall denylist, CLAUDE table.
- [x] **Step 2:** Operator GO 2026-08-23. Admitting ADR `Accepted` in the same session.

### Task 2: On GO only — delete in test-first slices

- [x] **Step 1:** `tests/test_coldstore_phase_c.py` + firm-constants split.
- [x] **Step 2:** Living keys removed. CLAUDE CFD rows pointer-only. Call-4 stays `STRATEGY_KEYS`.
- [x] **Step 3:** Targeted pytest green (see verification).

### Task 3: Verification

```bash
grep -n 'Guardian\|Aegis' core/dd_protection.py core/firm_rules.py
# expect: only comments / historical, or empty, per GO
grep -n 'LEG_MAP' ops/c1_rail/c1_sizing_host_reference.py
# Striker rows still present unless F2 GO said otherwise
```

## Forbidden moves

- Executing C from Phase A Accept.
- Deleting Striker `LEG_MAP` / rail host.
- Editing locked Pine parameters.
- Bundling F2 rail teardown.
