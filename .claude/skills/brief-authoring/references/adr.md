# [Decision title] — `<slug>`

Filename: `docs/adr/YYYY-MM-DD-slug.md` (the filename slug *is* the identifier —
there is no `ADR-NNN` numbering; back-references use the filename).

---

## Tier test — full ceremony or light record? (read first)

ADR ceremony is stakes-tiered
([ADR 2026-08-08](../../../../docs/adr/2026-08-08-adr-ceremony-tiering.md)).
Use the **FULL** template below (§0–§7) iff any limb holds:

1. Spends K or money (research runs, venue fees, live orders).
2. Touches a live-risk surface: `dd_protection`, allocations, lifecycle state,
   arming/`dry_run` invariants, spend ceilings, or a `firm_rules` field consumed
   by sizing or by an open fork.
3. Alters a LOCKED/frozen surface (Pine, locked params, frozen prereg) —
   including via supersession — or irreversibly deletes a non-regenerable
   surface (vendor data, production-code estates).
4. Creates or amends doctrine: a rule, gate, falsifier threshold, or convention
   that binds future work.

Otherwise write a **LIGHT decision record** in the same path with the same
six header fields below (keeps `check_adr_graph` green), plus
`**Tier:** light`, body capped at **300 words**:

```
Decision: <≤3 sentences>          Grounds: <links, never retellings>
Reads: <path> @ <anchor> · …      Gate: <binary, or "none — record only">
Boundary: <genuinely tempting forbidden move, or "none">
```

Ambiguous tier → FULL. Escalation = supersede with a full ADR
(`escalated-from-light`), never pad in place. Rule 0 reads are tier-independent
(the read always happens; only the §0 table format is dropped for light).

If light: fill the header fields, add `**Tier:** light`, write the five-line
body above, stop — do not fill §0–§7.

---

**Status:** `Proposed` — optional free annotation
**Decision date:** YYYY-MM-DD
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

---

## Status grammar (read before filling in the header)

`**Status:** `<token>`[ — <free annotation>]`

The machine parser (`scripts/check_adr_graph.py`) matches only the **leading
backtick-quoted token**. Everything after an em/en/ASCII dash or parenthetical
is free prose the machine ignores — use it to record dissent, override
provenance, or operator ratification notes. Do not invent new tokens; the
closed vocabulary is:

| Token | Body location | Notes |
|---|---|---|
| `Proposed` | Hot `docs/adr/<slug>.md` | May declare pending `Supersedes` edges (see below) |
| `Accepted` | Hot | Includes partial supersession — see `Superseded-in-part-by` |
| `Superseded` | Cold — stub hot, full body in `docs/ltm/adr/<slug>.md` | Requires an ADR-path `Superseded-by` |
| `Withdrawn` | Cold — same shape as `Superseded` | |
| `Retired` | Cold — same shape | Operator kill with no successor ADR |

There is no `Deprecated` token and no `ADR-NNN` numbering — both were dropped
2026-07-17 (design: `docs/superpowers/specs/2026-07-17-adr-lifecycle-graph-design.md`).
**Partial supersession is not a Status token.** An ADR that is only partially
superseded stays `Accepted`; the partial kill is recorded solely via a non-`none`
`Superseded-in-part-by` field. `docs/adr/INDEX.md` derives its "Partially
superseded" section from that field, not from Status.

---

## Six required header fields

Parsed from the **header region only** — from the start of the file to the
first line matching `^## ` or `^---\s*$`, whichever comes first. `**Status:**`
lines inside an addendum below that boundary (e.g. a later note appended to an
old ADR) are prose, not machine input — the graph parser ignores them.

```markdown
**Status:** `Accepted` — optional free annotation
**Decision date:** YYYY-MM-DD
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
```

Field value forms:

| Field | Allowed values |
|---|---|
| `Supersedes` | `` `YYYY-MM-DD-slug.md` full `` \| `` `YYYY-MM-DD-slug.md` in part — <clause> `` |
| `Superseded-by` | `` `YYYY-MM-DD-slug.md` `` (ADR path only) |
| `Superseded-in-part-by` | `` `YYYY-MM-DD-slug.md` — <clause> `` **or** `` `event:<short-id>` — <note> `` for a non-ADR / merge-reality partial kill |
| `Retain-until` | `YYYY-MM-DD` (future date — escapes the age+graph prune, A5) |

Multiple targets on the same field repeat the bold-key, one target per line:

```markdown
**Supersedes:** `2026-05-14-allocation-refresh.md` full
**Supersedes:** `2026-04-17-portfolio-allocations.md` in part — Striker/NAS rows only
```

---

## Full vs in-part vs `event:` — which edge to declare

- **Full supersede** (`Supersedes: X full`): X is fully dead. X's Status must
  become `Superseded` with `Superseded-by: Y`, and X must be retired to a stub
  (see the accept+retire checklist below) — **X cannot stay a full hot body**
  once Y is `Accepted` with this edge.
- **In-part supersede** (`Supersedes: X in part — <clause>`): X stays hot,
  Status stays `Accepted`, and X gains a `Superseded-in-part-by: Y — <clause>`
  line. The clause text is documentation only — the graph checker's reverse
  match compares `(file, scope)`, never the clause wording, so rephrasing the
  clause never breaks CI.
- **`event:` in-part** (`Superseded-in-part-by: event:<short-id> — <note>`):
  use when a clause died by merge-reality / operational drift with **no
  successor ADR** to point at (e.g. a lock action superseded by a later merge
  while its validator machinery remains live). No reverse ADR edge is required
  or checked for `event:*` targets.

---

## Proposed successors declare pending edges

An ADR's `Supersedes` edges are **pending**, not enforced, while its own Status
token is `Proposed`. Concretely:

- Land a new ADR Y with `Status: Proposed` and `Supersedes: X full` — CI stays
  green. X is untouched; it keeps its current Status and full hot body.
- The reverse-edge check (X must have `Superseded-by: Y` + stub shape) and the
  cold-store shape check **do not fire on X** while Y is `Proposed`.
- Only once Y flips to `Accepted` do X's reverse edge and cold-store shape
  become mandatory — see the accept+retire checklist immediately below.

This lets a superseding decision go through normal review on its own branch
without redlining the whole ADR graph for the file it will eventually retire.

---

## Accept+retire checklist (same PR)

Flipping Y's Status to `Accepted` with a `full` `Supersedes: X` edge is
**incomplete** until X is retired in the same PR (or a hand-equivalent single
change). Before merging:

- [ ] Y's header: Status `Accepted`, `Supersedes: X full` line present.
- [ ] Ran `python scripts/retire_adr.py X --reason superseded --by Y` (or
      performed the equivalent by hand): X's full body moved to
      `docs/ltm/adr/X.md`, X's hot file rewritten to a stub (`**Body:**` link,
      ≤40 lines, no `## ` headings), X's Status token `Superseded` on **both**
      the stub and the LTM body, X's `Superseded-by: Y` set.
- [ ] Regenerated `docs/adr/INDEX.md` (`python scripts/check_adr_graph.py
      --regenerate-index`) and included the diff in this PR.
- [ ] Ran the residual-inbound-refs sweep the retire helper prints and fixed
      any stale hot-doc references to X's old full-body path (Known Trap #7).
- [ ] `python scripts/check_adr_graph.py` exits 0 before pushing.

If X is only partially killed by Y, skip this checklist — use the in-part edge
above instead; X never moves to `docs/ltm/adr/`.

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR. Per SKILL.md: any ADR touching risk
controls, locked parameters, or production code must list production files
read with verification anchors. Reading "during the investigation" is too
late — the decision is already framed by then (anchor: 2026-04-17
dd_protection cycle).

- `path/to/file.py` — anchor: `<commit_hash>` (verified `git log -1 --
  path/to/file.py` on YYYY-MM-DD)
- `path/to/config.yaml` — anchor: `last-modified YYYY-MM-DD`
- `docs/adr/YYYY-MM-DD-prior-decision.md` — anchor: `<commit_hash>` (the prior
  decision this ADR fully or partially supersedes)
- `Notion: <page_title>` — anchor: page ID `<id>`

---

## §1 — Context

The forces at play that make this decision necessary. What changed (in the
world, the data, the methodology) that requires a structural choice now?
Connect to standing doctrine (Core Principles, prior ADRs, lessons
registries) — orphan ADRs accumulate as noise.

[3–6 sentences. Name the dated incident, finding, or constraint that prompted
the decision. Cite the prior ADR being amended/superseded if applicable, by
filename slug — not a number.]

**Decision driver (one sentence):** [What makes this decision unavoidable now
rather than later.]

---

## §2 — Decision

The single decision being recorded. ADRs document ONE decision; if multiple
structural choices are being made simultaneously, split into multiple ADRs
and cross-reference by filename.

**Decision:** [The decision, stated as a present-tense imperative. Example:
"Strategy version locks include both per-strategy backtest anchors AND the
portfolio MC anchor used to validate them, with both anchors carrying commit
hashes."]

**Effective:** [date, or "immediately upon acceptance"]
**Scope:** [what this applies to — e.g., "all strategy version locks from
Guardian v5.5 onward"; "all CC handoff briefs ≥3 mechanical edits in same
defect family"]

---

## §3 — Alternatives considered

Every ADR must list alternatives genuinely weighed. An ADR with no
alternatives section is recording a non-decision — there was nothing to
choose between.

| Alternative | Why ruled out |
|---|---|
| [Alternative A] | [specific reason, with citation to lesson / prior outcome / methodological constraint] |
| [Alternative B] | [reason] |
| [Status quo — no decision] | [why doing nothing is worse than choosing] |

---

## §4 — Falsifier (revert trigger)

ADRs are not permanent; they can be wrong. §4 names the specific observation
that would falsify this decision and trigger a revert or supersede.

This is the binary form (Discipline Check #2 + Discipline Check #4): "If
[specific observation], then this ADR is revoked and [specific next action]."

**Revert trigger:** [Specific numerical / time-bound / event-driven
condition. Examples: "rolling 6-month pass rate <95% across 2 windows
triggers revert to `2026-05-08-dd-trigger-c2-relock.md`"; "quarterly
regime-check on YYYY-MM-DD finds H1↔H2 PF spread >10pp"; "any single trade
exceeds X% account loss".]

**Revert action:** [What happens when the trigger fires — author a new ADR
that fully or in-part supersedes this one (see edge rules above), revert to
prior config, escalate to full re-investigation. Never silently edit this
ADR's decision text — see change-history rule below.]

**Trigger check schedule:** [Calendar trigger — quarterly check date, or "on
every challenge boundary", etc.]

---

## §5 — Forbidden moves (under this ADR)

Moves that are tempting under this decision but explicitly ruled out. §5 must
list moves the author genuinely considered or was tempted by — not
theatrical refusals (Discipline Check #3).

- **[Forbidden move 1]** — ruled out because [specific reason, citing lesson
  or doctrine].
- **[Forbidden move 2 — typical pattern: "loosening §4 trigger without
  superseding ADR"]** — silent amendment of the revert trigger is
  `p`-hacking at the methodology layer (Known Trap #12). If the trigger is
  wrong, author a fresh ADR that supersedes this one (full or in-part per the
  edge rules above); never edit this ADR's header or body in place.
- **[Forbidden alternative — bringing back a rejected §3 alternative without
  new evidence]** — alternatives in §3 are ruled out for stated reasons.
  Re-proposing one requires either new evidence that invalidates the §3
  reason OR a fresh Pre-Q investigation, not a casual revival.

---

## §6 — Consequences

What follows from this decision, separated by direction.

**Positive consequences:**
- [Specific gain — methodology compression, decision speed, error reduction, etc.]
- [Specific gain]

**Negative consequences (real cost, not theatrical):**
- [Specific cost — operational overhead, lost flexibility, etc.]
- [Specific cost]

**Risks (probabilistic, distinct from costs):**
- [Risk — what could go wrong if assumptions don't hold, with mitigation if any]

**Downstream artifacts that need updating:**
- [repo path — what specifically changes]
- [SKILL.md Y — what specifically changes]
- [STATE.md — what specifically changes]

---

## §7 — Implementation plan

If this ADR requires mechanical edits, enumerate them. If it requires a CC
spawn, reference the companion handoff brief at
`docs/briefs/handoffs/YYYY-MM-DD-cc-handoff-<slug>.md`.

- **Phase 0** — [verify §0 reads still current at implementation time]
- **Phase 1** — [edit repo path / SKILL.md per §6 downstream list]
- **Phase 2** — grep-sweep in two limbs (Known Trap #7 — source-of-truth
  fracture): **(i)** stale references to any superseded predecessor (if
  applicable); **(ii)** consumers of the *state* this decision changed,
  discovered by grepping the **pre-decision configuration's own vocabulary**
  — the symbols, cap allocations, tier keys, book composition, and dollar
  figures that were true before the decision. Do not key the sweep only to
  this decision's own words; derived documents often share no token with
  them. If this ADR fully supersedes a predecessor, this phase also includes
  the accept+retire checklist above. **Standing rule:** a decision that
  supersedes no predecessor (`Supersedes: none`) still has Phase-2 work —
  de-scopes, withdrawals, and re-parks invalidate premises without
  superseding any document.
- **Phase 3** — [verification block executes; ADR status moves to `Accepted`]

If the ADR is purely policy (no mechanical edits), §7 reads `Policy only — no
mechanical edits required` and §10 audit hooks check enforcement instead.

---

## §10 — Audit hooks (runnable)

```bash
# Grep for stale references to a fully superseded predecessor (if applicable)
grep -rn "YYYY-MM-DD-predecessor-slug" docs/ 2>/dev/null
# Expected: only this ADR's §1 supersedes-reference and the predecessor's
# retired stub (Superseded-by line + Body pointer)

# §4 trigger check
[ specific command that re-evaluates the revert trigger on schedule ]

# Cross-reference: are all downstream artifacts updated per §6?
diff <(grep -rl "<superseded value>" docs/) /dev/null
# Expected: empty (no remaining stale references)

# Calendar trigger reminder
# Quarterly regime check due: YYYY-MM-DD
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python /path/to/brief-authoring/scripts/check_brief.py <this-file>.md --type adr
# Expected: all 6 checks PASS

# ADR lifecycle graph — header fields, edges, cold-store shape, INDEX sync
$ python scripts/check_adr_graph.py
# Expected: exit 0; A1 (header fields), A2 (edge reverse-match — skipped
# while this ADR is Proposed), A3 (cold-store shape), A6 (INDEX sync) all pass

# Production-source verification (Rule 0 confirmation)
$ <grep / cat / git log commands that confirm §0 anchors>

# Downstream artifact update verification
$ <grep commands that confirm §6 downstream list has all been updated>

# Supersede chain integrity (only if this ADR fully or in-part supersedes another)
$ grep -A1 "Supersedes" docs/adr/<this-slug>.md
$ grep -A1 "Superseded-by\|Superseded-in-part-by" docs/adr/<predecessor-slug>.md
# Expected: bidirectional reference matches (file + scope, not clause wording)
```

The §6 downstream list must be **DERIVED, not recalled**: run the Phase-2
sweep, **paste its raw file-list output into §10**, take §6 as the **union**
of that output and the author's enumeration, and **disposition every hit**
(edited / bannered / explicitly ruled unaffected **with the reason**). If §6
is incomplete or any hit lacks a disposition, the ADR stays `Proposed`, not
`Accepted`. Do not flip status until both the union and the dispositions hold.

---

## Change history

Material amendment to a decision already recorded here is **never** a silent
edit of this file's locked decision text. Amend by authoring a new ADR that
declares `Supersedes: <this-slug>.md full` (kills this decision entirely) or
`Supersedes: <this-slug>.md in part — <clause>` (kills only one clause; this
ADR stays `Accepted` and gains a matching `Superseded-in-part-by` line). Only
non-material edits — typo fixes, dead-link repairs, an appended addendum note
below the header region — belong in this table.

| Date | Change | By |
|---|---|---|
| YYYY-MM-DD | Initial authoring | Joshua + claude.ai |
| YYYY-MM-DD | [Non-material fix only — e.g. dead-link repair. A material change to the decision text requires a new superseding ADR, not a row here] | — |
