# Tradable-anomalies T4 — Call-1 kill-line OC + rolling-PF σ-source (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: PENDING OPERATOR GO.** Owning ADR [`2026-07-11-tradable-anomalies-statistics-adoption.md`](../../adr/2026-07-11-tradable-anomalies-statistics-adoption.md) §7 T4 **and** lifecycle ADR pending item (a). Live-PF σ-source is **fill-gated** ([`STATE.md`](../../../STATE.md)). This plan is not a GO and does not arm a book.

**Goal:** After GO **and** a live-PF source exists (or a dated synthetic/historical substitute the GO names): compute Call-1 kill-line operating characteristics (false-kill rate, detection lag vs horizon); build the rolling-PF σ-source harness + tier-demotion state writer that `decay_breach` / `autonomous_demote` already implement as pure logic.

**Architecture:** Reuse `core/lifecycle.py` `decay_breach` / `next_tier_down` / `autonomous_demote`. New harness **reads** `baselines.md` + a PF series and **may** write `lifecycle_state.json` only under GO. Until a strategy is on the book, the GO should authorize a **historical/synthetic OC study only** (no state writer).

**Tech Stack:** Existing lifecycle module + pytest. No Pine edits.

## Global Constraints

- No execution without GO.
- No `lifecycle_state.json` writes unless the GO explicitly names the writer.
- Do not touch `BASE_RISK` / ladder pins / Pine.
- Do not claim the 2026-08-08 first evaluation happened.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Adoption ADR §7 T4 | `027a729` | OC + σ-source + state writer |
| `core/lifecycle.py` | `027a729` | Pure Call-1 logic already landed |
| `strategy_lifecycle.md` pending (a) | `0723587` | σ-source design in flight |
| STATE gated-on-fill note | 2026-08-22 | Call-1 has no live data |

---

### Task 1: Pre-GO — OC design box

- [ ] **Step 1:** Write the OC experiment (N, horizon, σ, false-kill target) as a short prereg **if** the GO wants a lab slug. Otherwise keep it in this plan.
- [ ] **Step 2:** Stop. Do not write `lifecycle_state.json`.

### Task 2: On GO — OC study (historical/synthetic)

- [ ] **Step 1:** Tests on synthetic PF paths: known-decay series trips `decay_breach`; flat series does not at the ratified k=1.0.
- [ ] **Step 2:** Publish RESULTS. No demotion write.

### Task 3: On a **separate** GO — state writer

- [ ] **Step 1:** Only when a live-PF source exists (or the GO names a substitute). Wire `autonomous_demote` → `lifecycle_state.json`. Cap at WATCH-2. RETIRED stays operator-gated.

## Forbidden moves

- Executing T4 from Tranche-1 Accept.
- Writing demotions "to see if it works."
- Bundling Call-4 beta-cohesion (sibling plan).
- Restoring `guardian_signal.py`.
- Arming / `dry_run=false`.
