# Futures-anomaly-discovery skill skew — pointer repairs (ready-to-execute-on-GO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION: PENDING OPERATOR GO.** Owning notice [`N-2026-08-23-ox-alpha-futures-anomaly-discovery-skill-review.md`](../../notes/notice/N-2026-08-23-ox-alpha-futures-anomaly-discovery-skill-review.md) §4 routed apply-on-GO. This plan is not a GO and does not edit the skill. No new ADR — the repairs mirror ratified owners; they do not amend them.

**Goal:** After GO, stop the skill from restating withdrawn harvest doctrine, name machinery that already exists, and collapse “promote / hand-off” to one vocabulary. `$0 / K=0`.

**Architecture:** Pointer-only skill text. Harvest Req-1..5 stay in [`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) §1. Admission refuse reasons stay in `lab/discovery/admission_schema.py`. Deep-lane predicate stays in the charter. Do not copy those lists into the skill.

**Tech Stack:** Markdown only. Existing `check_skill_refs.py` / `check_skills_no_constants.py`. No Python behavior change.

## Global Constraints

- No execution without GO.
- `$0 / K=0`. No Databento. No campaign `open`. No Pine / `dd_protection` / allocations.
- Do not paste harvest Req-1..5, TNEC numerals, bank snapshots, or `floor_at_k` tables into the skill.
- Do not edit `lab/discovery/register_search.py`.
- Do not open a Pre-Q. Do not treat this file as a GO.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Skill `SKILL.md` | `3c6745a` (2026-08-20) | Four-req list; “kills the seed regardless of quality”; no `--lane deep`; “no admission gate” on blind |
| `reference/tool-discipline.md` | `027a729` (2026-08-14) | “promoted to an Inquire-phase falsifiable hypothesis”; no restart/seed K |
| `strategy_harvest.md` §1 / §2 | `fd0e6ee` (2026-08-18) | Five requirements; Req-3 disclosure-not-gate; §2 still says “four” |
| Family K-bank ADR | `6608339` (2026-08-18) | `Accepted` — disclosure, cannot fail a seed |
| `register_search.py` | `a5ee05e` (2026-08-22) | `--lane` `blind \| mechanism-first \| deep`; `_require_admission` optional-on-blind-but-still-refuses |
| `admission_schema.py` | `027a729` (2026-08-14) | Schema + refuse reasons |
| `instrument_profiles.py` `CONSULT_NOTE` | `d7a8a7f` (2026-08-22) | `DEAD` / `AMBIGUOUS-PARKED` / `CONTINGENT-FORWARD` BLOCKING; `LIVE` is a note |
| Deep-lane charter | `b301e44` (2026-08-22) | `--prereg`, `--grammar-file` / `--grammar-sha256`, `--confirm-years`, `--target-sr` |
| Owning notice | `7da8286` (2026-08-23) | Five surviving findings; DROP as a Q |

## File Structure

| File | Change (on GO only) |
|---|---|
| `.claude/skills/futures-anomaly-discovery/SKILL.md` | Harvest pointer; Req-3 disclosure; admission_schema pointer; bound-cell action; `--lane deep` stub; blind admission correction; pipeline wording |
| `.claude/skills/futures-anomaly-discovery/reference/tool-discipline.md` | “routed as” not “promoted to”; restart/seed K under HMM and symbolic regression |
| `docs/methodology/strategy_harvest.md` §2 | “four admission requirements (§1)” → “five admission requirements (§1)” |
| Owning notice | Addendum: repairs landed / still DROP as a Q |
| `docs/SESSIONS.md` | One line: GO executed; skill edited |

Out of scope (explicitly not findings / new machinery): prereg body hash-pin, refusal ledger, orphan-open expiry, family-taxonomy registry, feature fingerprint, daily-loss restatement, peek-before-open enforcement, `register_search.py` behavior.

---

### Task 1: SKILL.md — harvest pointer + existing machinery

On GO only.

- [ ] **Step 1 — Findings 1+2.** Replace the inlined “four admission requirements” block (current L52–66, including “kills the seed regardless of quality”) with a pointer-only harvest intake:
  - Externally-published mechanisms enter only via the five requirements in [`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) §1.
  - Req-3 is mandatory disclosure, not a gate ([`2026-08-04-family-k-bank-disclosure-not-gate.md`](../../adr/2026-08-04-family-k-bank-disclosure-not-gate.md)). Do not restate bank snapshots or floors.
  - Keep the existing same-units sentence (current L75–82) as a one-line reminder that Req-5 is checked at sourcing and admission — do not re-derive the inequality.
- [ ] **Step 2 — Finding 3 + reconciliation-side.** In the Rule-1 / CLI section:
  - Point `--admission-file` at `lab/discovery/admission_schema.py` (schema + refuse reasons). Do not copy EM/N-EDGE constants.
  - Bound-cell action: a `python scripts/instrument_profiles.py cell` consult that prints BLOCKING (`DEAD`, `AMBIGUOUS-PARKED`, `CONTINGENT-FORWARD`) must be addressed in the prereg or the open does not proceed. `LIVE` is a note, not a refuse.
  - Document `--lane deep` (charter [`2026-08-16-deep-iteration-lane-charter.md`](../../adr/2026-08-16-deep-iteration-lane-charter.md)). Required flags only: `--prereg`, `--grammar-file` / `--grammar-sha256`, `--confirm-years`, `--target-sr`. One short CLI stub; do not restate §2.2 arithmetic.
  - Correct the blind-lane sentence: admission file is **not required**; if supplied, Cap/EM0 / N-EDGE / power refusals still abort with no manifest (matches `_require_admission`).
- [ ] **Step 3 — Finding 4 (skill half).** Pipeline sentence (current L37–40): after K is registered, the cheap floor **filters** which p-values are worth carrying; the manifest verdict remains a hand-off to `strategy-validation`. Reserve **promotion** for strategy graduation. Keep “never a promotion” on the manifest verdict (current L156–157). Crossing into Inquire is **route / license a hypothesis**, never “promote”.

### Task 2: tool-discipline.md

On GO only.

- [ ] **Step 1 — Finding 4 (companion half).** In “The unifying rule” (current L97–101), replace “promoted to an Inquire-phase falsifiable hypothesis” with “routed as an Inquire-phase falsifiable hypothesis”.
- [ ] **Step 2 — Finding 5.** Under HMM and under symbolic regression: declared K includes restart / seed / init attempts (HMM random inits, PySR/gplearn independent runs). A re-run with a new seed is a new search increment, not a free peek. Place next to the existing “population/generation budget” line. No new script.

### Task 3: harvest.md §2 one-token pointer

On GO only.

- [ ] **Step 1.** In [`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) §2 “Why this section exists”, change “the four admission requirements (§1)” to “the five admission requirements (§1)”. Do not touch the §1 table.

### Task 4: Notice + session log after the repairs land

On GO only (this file’s landing addendum is a different, already-done pointer).

- [ ] **Step 1.** Notice addendum: repairs landed against this plan; status still `DROP` as a Q; skill now points at the owners.
- [ ] **Step 2.** `docs/SESSIONS.md` one line: GO executed; link this plan + the skill diff. Carry prior Open/next (DL-2 step 2; campaign-plan queue).

### Task 5: Verification (post-GO)

```bash
# Finding 1 gone from the skill; harvest owner remains the list
grep -n "kills the seed regardless of quality" .claude/skills/futures-anomaly-discovery/SKILL.md
# Expected: empty

# Finding 2: no restated four-req list in the skill
grep -n "four admission" .claude/skills/futures-anomaly-discovery/SKILL.md
# Expected: empty

# Deep lane named
grep -n "lane deep" .claude/skills/futures-anomaly-discovery/SKILL.md
# Expected: a hit

# Harvest §2 token
grep -n "the five admission requirements (§1)" docs/methodology/strategy_harvest.md
# Expected: a hit in §2

# Wording
grep -n "promoted to an Inquire-phase" .claude/skills/futures-anomaly-discovery/reference/tool-discipline.md
# Expected: empty
grep -n "routed as an Inquire-phase" .claude/skills/futures-anomaly-discovery/reference/tool-discipline.md
# Expected: a hit

python scripts/check_skill_refs.py --all
python scripts/check_skills_no_constants.py
```

- [ ] **Step 1:** Run the block. `check_skill_refs` / `check_skills_no_constants` exit 0.
- [ ] **Step 2:** One commit unless review asks to split. Suggested message: `docs(skill): stop restating withdrawn harvest Req-3; point at live machinery`.

## Forbidden moves

- Restating harvest Req-1..5 (or their numerals) in the skill.
- Adding numeric floors, bank snapshots, or `floor_at_k` tables to the skill.
- Editing `register_search.py` or any admission/consult implementation.
- Treating this plan file as a GO.
- Opening a Pre-Q to re-decide ratified harvest doctrine.
- Bundling prereg hash-pin, refusal ledger, or other non-findings from the notice’s discharged list.
