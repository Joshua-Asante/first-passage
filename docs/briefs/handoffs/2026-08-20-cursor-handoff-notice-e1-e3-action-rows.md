# Cursor Handoff — Notice E(i)/E(ii)/E(iii) action rows: two frozen text insertions

**Date:** 2026-08-20
**Parent session:** Claude Code
**Spawn target:** Cursor (frozen-spec implementation — `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`, §0.5 Cursor variant)
**Repo:** `first-passage`
**Brief type:** CC handoff (multi-step)
**Parent question:** N/A — executes the E(i)/E(ii)/E(iii) ACTION rows of
`docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md` §4
**Authority:** Joshua (CEO), "hand these mechanical steps off to Cursor". No commit/merge
without operator go.

**Scope note (why this is a single small packet, not a fleet):** two disjoint one-block
text insertions, zero code, zero tests, zero judgment calls — both insertions are
pre-drafted verbatim below. Below the size where `cursor-fleet`'s multi-worker apparatus
(claim manifest, per-packet worktrees, umbrella brief) pays for itself; routed as one
Cursor handoff under the plain ADR flow instead (`cursor-fleet` skill's own routing
table: "One implementation build → Single Cursor handoff... Fleet overhead is pure
waste at N=1"). **Do not decompose into two dispatches.**

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 work)

Report full contents of both target files in your first response before writing anything.

- `.claude/skills/futures-anomaly-discovery/SKILL.md` — report lines 219–244 in full (the
  "Red flags — STOP" section through "## Hand-offs"). Confirm the exact text of the
  existing battery-reuse bullet (starts "Reusing a frozen screen battery on a NEW claim
  family...") is still present verbatim as quoted in §2 Step 2.1 below — if it has
  changed, STOP and return `NEEDS_CONTEXT` quoting the diff, do not insert relative to
  a location that no longer matches.
- `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` — report lines
  1–16 in full (the header metadata block through the `---` separator). Confirm the
  `**Spend at freeze:**` line's exact text matches §2 Step 2.2 below.
- `docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md` §4 — report the E(i),
  E(ii), E(iii) table rows verbatim (context only; you are not editing this file).
- `git log -1 --format='%h %ci' -- .claude/skills/futures-anomaly-discovery/SKILL.md docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` — report both anchors.

After Phase 0: post the read-report, then proceed directly to §2 — both insertions are
frozen verbatim below, so there is no ambiguity to wait on (§0.5 is empty, see below).

---

## §0.75 — Local-only dependency check (required, Spawn target is Cursor)

- **Gitignored vendor data:** neither file nor edit touches `core/data/tv_exports/**`,
  `core/data/bar_data/**`, or `core/data/external/**`. **N/A.**
- **Secrets/API keys:** none needed. **N/A.**

---

## §0.5 — Clarifying questions

None. Both insertions are frozen verbatim text at a named anchor point; if Phase 0
shows the anchor text has drifted from what §2 quotes, that is a `NEEDS_CONTEXT` bounce
(quote the actual current text), never a judgment call about where else to place it.

---

## §1 — Context

`N-2026-08-18-iteration2-identify-notice.md` is a Notice-phase document (INQHIORI) whose
GRADUATE question packets (Q-CONDVAL-1, Q-EXPR-1, Q-TRAINKILL-1) are all `CLOSED`. Its §4
routing table left four small ACTION rows outstanding — process fixes the notice itself
generated, none requiring new research. This packet executes two of them, E(i)+E(ii)
(collapsed into one insertion — the notice's own text says "Same edit as E(i)") and
E(iii). E(iv) (a `STATE.md`/`docs/SESSIONS.md` touch) is explicitly **excluded** from
this packet — those files are orchestrator-reserved (`cursor-fleet` skill: "workers
never write them") and the parent session handles E(iv) directly.

**What CC is being asked to produce:**
- One new bullet appended to the "Red flags — STOP" list in
  `.claude/skills/futures-anomaly-discovery/SKILL.md` (exact text in §2 Step 2.1).
- One new header line appended to
  `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`'s metadata
  block (exact text in §2 Step 2.2).

**What CC is NOT being asked to do:**
- Touch `STATE.md` or `docs/SESSIONS.md` (E(iv), out of scope — see §1 above).
- Edit any frozen decision content (§1–§6 or ADDENDUM-1) in the corrected-null-battery
  spec — the insertion is header metadata only, same class as the existing
  `**Spend at freeze:**` line, not a D1–D6 amendment.
- Reword, shorten, or "improve" either insertion's phrasing — both are frozen verbatim
  text drafted by the parent session against this repo's exact terminology; insert them
  byte-for-byte.
- Touch any other file.

---

## §2 — Execution plan

### Step 2.1 — SKILL.md: valence-blind null-validity bullet (E(i)/E(ii))

- **Inputs:** `.claude/skills/futures-anomaly-discovery/SKILL.md`.
- **Action:** In the "Red flags — STOP" section, immediately AFTER the existing bullet
  that begins "Reusing a frozen screen battery on a NEW claim family..." (ends
  "...`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`.") and
  BEFORE the "## Hand-offs" heading, insert this new bullet verbatim:

  ```
  - **Fresh batteries need the same check reuse gets.** The reuse-only red flag above
    catches a battery *reused* on a new claim family; it does not catch a battery
    *freshly authored* whose null construction was never validated against its own
    family's confound. Every screen's PREREG.md §0 must cite the governing
    null-validity doc for its claim family (e.g. the corrected-null-battery spec above
    for magnitude-persistence; the family's own spec/audit note otherwise) —
    **valence-blind**: cited regardless of whether the screen's expected or landed
    verdict is NULL or SIGNAL. A fresh battery that fails generously toward NULL is
    exactly as unchecked as one that fails toward SIGNAL. Anchor:
    [`N-2026-08-18-iteration2-identify-notice.md`](../../../docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md)
    E(i)/E(ii) — null-validity lensing was valence-scoped (S1a's NULL got the full
    4-lens design review that structurally could not catch an invalid null; only
    S1b's SIGNAL triggered the lens that did).
  ```

  Preserve the blank-line-between-bullets convention already used in that list.
- **Expected output:** a diff to `.claude/skills/futures-anomaly-discovery/SKILL.md`
  only, adding exactly this one bullet, no other line changed.
- **Per-step gate:** DONE requires (a) the inserted text matches the block above
  byte-for-byte, (b) it sits between the named existing bullet and `## Hand-offs`, (c)
  no other line in the file changed (`git diff --stat` shows this file with only
  insertions, no deletions).

### Step 2.2 — corrected-null-battery spec: retention-review header line (E(iii))

- **Inputs:** `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`.
- **Action:** Immediately AFTER the line beginning `**Spend at freeze:**` and BEFORE the
  `---` separator that follows it, insert this new line verbatim:

  ```
  **Retention-review:** 2026-11-08 (riding the standing slate date) — if no third
  magnitude-persistence screen has consumed this battery by then, it gets a retention
  test at the quarterly programme audit. Per
  [`N-2026-08-18-iteration2-identify-notice.md`](../notes/notice/N-2026-08-18-iteration2-identify-notice.md)
  §4 E(iii).
  ```

  This is header/provenance metadata, the same class as the existing `**Spend at
  freeze:**` line — it does not touch any D1–D6 frozen decision content, so it is not
  covered by the file's own "amendments after the official run = new spec" rule (that
  rule governs the frozen §1–§6 decision body, not the provenance preamble; the
  ADDENDUM-1 section already establishes append-only additions as the accepted pattern
  for this file).
- **Expected output:** a diff to
  `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` only, adding
  exactly this one line, no other line changed.
- **Per-step gate:** DONE requires (a) the inserted text matches byte-for-byte, (b) it
  sits between `**Spend at freeze:**` and the `---` separator, (c) no other line in the
  file changed.

### Step 2.3 — Closure

No formal closure artifact required (this is not a Pre-Q). Return the §6 status report
below. Do not touch `STATE.md`, `docs/SESSIONS.md`, `lab/CATALOG.md`, or
`docs/briefs/INDEX.md` — the parent session's own integration commit updates the
notice's §4 table and any board rows once this packet is reviewed.

---

## §4 — Falsifiable hypothesis

N/A (not a Pre-Q investigation) — but this packet's own success claim is falsifiable and
must be checked as such, not merely asserted:

**H:** both insertions land byte-for-byte at their named anchors, and nothing else in
either file changes.
**Falsified if:** `git diff origin/main -- .claude/skills/futures-anomaly-discovery/SKILL.md docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`
shows any line other than the two named additions touched, or either §10 grep hook
misses. If falsified, this is not `DONE_WITH_CONCERNS` — return `NEEDS_CONTEXT` naming
the discrepancy rather than shipping a partial or reworded insertion.
**Accept if:** both §10 audit hooks return exactly one hit each and the diff is
pure-addition, scoped to the two named blocks.

---

## §5 — Forbidden moves

- **Rewording either insertion.** Both are frozen verbatim text; insert byte-for-byte.
- **Placing the insertion anywhere other than the named anchor** if Phase 0 shows the
  anchor text has drifted — return `NEEDS_CONTEXT`, do not guess a new location.
- **Touching E(iv)'s files** (`STATE.md`, `docs/SESSIONS.md`) — explicitly out of scope,
  reserved to the parent session.
- **Editing any frozen §1–§6 or ADDENDUM-1 content** in the corrected-null-battery spec.
- **"While I was in there" fixes** — e.g. noticing the W5 word-cap drift mentioned in
  the notice's E(iv) row and fixing it. Log the observation in `DONE_WITH_CONCERNS` if
  you notice something else off-pattern; do not act on it.

---

## §6 — Gate + status return taxonomy

Report back with exactly one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` /
`BLOCKED — <sub-case>`.

```
Status: <...>
Per-step gates: 2.1 [...], 2.2 [...]
Diffs (files touched): <list — must match exactly: .claude/skills/futures-anomaly-discovery/SKILL.md, docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

Branch: `cursor/notice-e1-e3-action-rows`. PR with the two-file diff. **No commit/merge
without operator go.**

**Completion (2026-08-29):** landed. Cursor returned `DONE_WITH_CONCERNS` (one non-blocking
casing nit in this brief's own audit-hook grep, not a defect in the insertion); merged as PR #69
(`17ebc46`), integrated in `3c6745a` ("docs(notice): discharge E(i)/E(ii)/E(iii) action rows --
valence-blind null-validity + retention-review date") — confirmed landed in
`.claude/skills/futures-anomaly-discovery/SKILL.md` (valence-blind bullet, ~line 270) and
`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` (Retention-review line,
~line 15). The consuming notice, `docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md`,
was not updated by that commit and needs its own correction (see that file).

---

## §10 — Audit hooks (runnable)

```bash
git diff origin/main --name-only
# Expected: exactly .claude/skills/futures-anomaly-discovery/SKILL.md
#           and docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md

grep -n "valence-blind" .claude/skills/futures-anomaly-discovery/SKILL.md
# Expected: one hit (this notice's own §10 audit hook for E(i)/E(ii))

grep -n "retention-review" docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
# Expected: one hit (this notice's own §10 audit hook for E(iii))

git diff origin/main -- .claude/skills/futures-anomaly-discovery/SKILL.md \
  docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
# Expected: pure additions, no deletions, no lines outside the two named blocks touched
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-08-20-cursor-handoff-notice-e1-e3-action-rows.md --type cc_handoff
```
