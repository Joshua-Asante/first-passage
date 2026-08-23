# Substrate Phase 6 — consolidated documentation and completion checklist

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** Accepted ADR [`2026-07-22-challenge-era-substrate-retirement.md`](../../adr/2026-07-22-challenge-era-substrate-retirement.md) — docs slice is executable. **Destroying the offline rollback copy is operator confirm only** — this plan writes the checklist, it does not destroy bytes.

**Goal:** Close Phase 6 as *documentation + verification*, so Phases 1–5 are recorded complete on `main` without rewriting historical ADR bodies. Produce a dated completion note and run the ADR's own §10 suite.

**Architecture:** One new completion note under `docs/ltm/notes/` (or `docs/notes/` if the owner already lives there). Pointers only in `REPO_MAP.md` / `PIPELINES.md` / `CLAUDE.md` if they still claim FXIFY / `ACTIVE_FIRM` / Pepperstone-as-canonical as living. No historical body rewrite (Trap #12).

**Tech Stack:** Markdown + existing §10 commands.

## Global Constraints

- Phases 1–5 already CODE_LANDED / MERGED. Do not re-do them.
- Do not delete OANDA/Dukascopy tombstone hashes.
- Do not introduce `ACTIVE_FIRM`.
- Do not destroy the offline rollback copy.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Owning ADR header + §7 Phase 6 | `027a729` | Phase 6 = docs + §10 + point-of-no-return; destroy-copy separately gated |
| `docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md` | (Phase 5) | Tombstone owner |
| `core/historical_challenge.py` | Phase 4 | Historical FXIFY semantics |

## File Structure

| File | Change |
|---|---|
| `docs/ltm/notes/2026-08-23-substrate-phase-6-completion.md` | **Create.** Checklist: §10 commands, which passed, which skipped (and why), destroy-copy still owed |
| Root orientation docs | Pointer-only if they still treat substrate surfaces as live |
| Owning ADR Change History | Phase 6 docs landed; destroy-copy still operator-gated |

---

### Task 1: Run §10 as evidence, do not "fix" by deleting the hook

- [ ] **Step 1:** Execute the owning ADR §10 block (graph, rg for `ACTIVE_FIRM` / `FIRM_RULES["FXIFY"]` / Pepperstone anchors / OANDA manifest owners, `make check` subset that is cheap). Paste outcomes into the completion note.
- [ ] **Step 2:** If a §10 rg is non-empty in **active** code, stop and escalate — that is a Phase 1–5 defect, not a docs tidy.

### Task 2: Completion note

- [ ] **Step 1:** Write the note. State Phase 6 docs `DONE`, destroy-copy `NOT DONE`. Link tombstone + Phases 1–5 PRs already named in the ADR header.
- [ ] **Step 2:** Add Change History row on the owning ADR. No §2 edit.

### Task 3: Root-doc pointers only

- [ ] **Step 1:** Grep `ACTIVE_FIRM`, `canonical CFD feed`, `Pepperstone/TV is the sole` in `README.md` `REPO_MAP.md` `PIPELINES.md` `CLAUDE.md`. Fix only silent restatements of *living* substrate. Leave historical ADR text.

## Forbidden moves

- Destroying the offline copy.
- Rewriting Phase 1–5 historical bodies.
- Reintroducing `ACTIVE_FIRM`.
- Skipping a red §10 via "docs-only so it's fine."
