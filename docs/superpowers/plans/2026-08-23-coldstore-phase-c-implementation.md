# Coldstore Phase C — hot-path code retirement (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: PENDING OPERATOR GO.** Phase A ADR does not authorize Phase C. Requires a **fresh admitting ADR + operator GO** (Phase A §5 / T2). This file is not that ADR and not that GO.

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

- [ ] **Step 1:** List every import of `BASE_RISK["Guardian"]` / `["Aegis"]` in `core/`, `ops/`, `tests/`. That list **is** the Phase C blast radius.
- [ ] **Step 2:** Do not apply the delete in the same session as a `Proposed` draft unless the operator GOs.

### Task 2: On GO only — delete in test-first slices

- [ ] **Step 1:** Failing tests that expect Guardian/Aegis keys **gone** (or moved to `historical_challenge`).
- [ ] **Step 2:** Remove keys. Update CLAUDE Strategy Reference to pointer-only historical.
- [ ] **Step 3:** `pytest tests/test_lifecycle.py tests/core/test_firm_constants_single_source.py -q` plus any newly failing consumers.

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
