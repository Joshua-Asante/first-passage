# ADR 2026-08-31 — Persona-hierarchy system fully retired

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-31, in-session direct instruction ("I
have changed my mind on the personas, I want them deleted completely"); scope confirmed via
`AskUserQuestion` (full cross-reference scrub, not just `docs/personas/`; formal-retirement
convention over a silent hard delete; companion PR #235 closed unmerged rather than landed first).
**Decision date:** 2026-08-31
**Authors:** Joshua + Claude Code
**Supersedes:** `2026-08-19-loop-persona-hierarchy-review-panel.md` full
**Supersedes:** `2026-08-21-persona-hierarchy-front-office-only.md` full
Both ADRs' underlying decisions — that a review-panel mechanism should exist, and that it should be
narrowed to Front Office — are fully reversed by this ADR, not merely extended. Their text is left
as-is (historical record of what was ratified and when); this ADR is the current-state pointer per
this repo's own Trap-#12/change-history discipline.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [persona hierarchy](2026-08-19-loop-persona-hierarchy-review-panel.md) (`Accepted`,
fully superseded by this ADR) · [Front-Office-only narrowing](2026-08-21-persona-hierarchy-front-office-only.md)
(`Accepted`, fully superseded by this ADR) · [ceremony tiering](2026-08-08-adr-ceremony-tiering.md)
(limb 4 fires — see §0) · [Great Prune ADR](2026-08-08-great-prune.md) (the retention-test /
git-history-is-the-archive convention this ADR's deletion approach follows)
**Layer:** meta-process (governance-of-what-governs, same class as the two ADRs this supersedes).
**$0 / K=0.**
**Loop-of-Record:** STRATEGIC — retiring a review mechanism bound to the GRAND/STRATEGIC tiers is
the same LoR class as the two ADRs it supersedes.

---

## §0 — Rule 0 reads (this worktree, 2026-08-31)

- Persona hierarchy ADR — `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md` — read in
  full, including its own addenda. The original decision this ADR fully supersedes.
- Front-Office-only narrowing ADR — `docs/adr/2026-08-21-persona-hierarchy-front-office-only.md` —
  read in full. The narrowing decision this ADR fully supersedes (rendering it moot rather than
  reversing it a second time — narrowing an apparatus that no longer exists is vacuous).
- `docs/personas/ownership-map.md` — read before deletion. Confirmed its Layer 1 (directory
  ownership) and Layer 2 (38-pursuit table) content has no load-bearing consumer outside the
  persona system itself — first-line-reviewer assignment, not modification authority (its own
  opening line), and no script or gate reads it programmatically (confirmed via
  `grep -rn "ownership-map" --include='*.py' .` at authoring time: zero hits).
- `.claude/workflows/pre-ratification-adversarial-panel.js` — read in full. Confirmed the
  persona-mode branch (`PERSONA_REGISTRY`, `personaMode`, the `PERSONAS` lens builder, the
  precondition check, and `safetyInvariantHardBlockFires`) is structurally separable from the
  original generic 6-lens review pipeline — the file predates persona mode (2026-08-21 ADR's own
  §6 downstream-artifacts list describes persona mode as an *addition* to an existing workflow,
  not a rewrite of it) and every non-persona code path is untouched by removing it.
- `scripts/gates.yml` — confirmed `check_personas.py` was never wired in (REPO_MAP.md's own
  scripts table already noted "manual/local only, not in gates.yml" at authoring time) — no gate
  removal needed, only the script and its REPO_MAP.md row.

---

## §1 — Context

The 2026-08-19 ADR stood up a spawnable persona review panel (front/middle/back-office) over
GRAND/STRATEGIC-tier ratifications. The 2026-08-21 ADR narrowed it to a 9-seat Front-Office-only
roster after a governance-friction audit found 13 of 18 spawnable personas had never fired,
retiring the other 8 (CRO, COO, Head of Risk & Sizing, Head of Validation, Head of Engineering,
Head of Governance, Documentation Analyst, Research Registry Analyst) to mechanical gates.

The operator has now directly instructed full retirement of the remaining apparatus — the 9
surviving seats (CEO, CIO, CFO, Head of Research, Head of Execution, and the 4 Staff analysts),
the roster/ownership-map/panel-mechanics machinery, and every file under `docs/personas/` —
without qualification. No further rationale was elicited or is required: per this repo's own
established pattern for ratifying a direct, unambiguous operator instruction (e.g. the 2026-08-21
ADR's own ratification note), a terse reversal is a legitimate and sufficient decision on its own.

This is not a second narrowing pass — it is a full reversal of both prior ADRs' central premise
(that a dedicated persona-review layer earns its keep). Nothing about the 2026-08-21 ADR's own §4
falsifier (whether the 8 mechanically-gated retirements hold up) is implicated; that decision
already stands on its own mechanical-gate evidence, independent of whether the remaining 9 seats
continue to exist.

---

## §2 — Decision

**Delete, not archive**, per direct operator instruction (not this repo's default retire-via-`git
mv`-to-`archive/` convention — see §3 for why that convention was considered and declined here).
Nothing is recoverable from the live tree; git history remains the recovery path, per this repo's
own Great Prune precedent (content deleted from the live tree, retrievable via `git log --follow`
or `git show`, with a dated ADR recording the event — exactly this ADR).

1. **All 34 files under `docs/personas/`** (22 live + 12 already-archived) are deleted: `INDEX.md`,
   `README.md`, `ownership-map.md`, every charter (`ceo.md`, `cio.md`, `cfo.md`,
   `head-of-research.md`, `head-of-execution.md`, `falsifier-analyst.md`,
   `pre-registration-analyst.md`, `research-analyst.md`, `tca-analyst.md`), every decision log
   (`*-log.md`, 8 files), and the entire `archive/` subtree (the 8 mechanically-gated retirements'
   charters — their retirement is unaffected; only the historical charter text is removed from the
   live tree).
2. **The design spec and its supporting plans** are deleted: `docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md`,
   `docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`,
   `docs/superpowers/plans/2026-08-18-persona-roster.md`,
   `docs/superpowers/plans/2026-08-18-validation.md`,
   `docs/superpowers/plans/2026-08-18-panel-mechanics.md`,
   `docs/superpowers/plans/2026-08-19-ownership-map-plan.md`.
3. **`scripts/check_personas.py`** is deleted — nothing left for it to validate.
4. **`.claude/workflows/pre-ratification-adversarial-panel.js`** keeps its original generic 6-lens
   review pipeline (form check → 6 independent adversarial lenses → skeptic verify → synthesis) —
   this is load-bearing, general-purpose infrastructure predating persona mode, used for any
   brief/ADR/closure ratification, not persona-specific. Only the persona-mode branch is removed:
   `PERSONA_REGISTRY`, the `tier`/`personas` args path, the `PERSONAS` lens builder, the
   commit-precondition check gated on persona mode, and `safetyInvariantHardBlockFires` /
   `citesSafetyInvariant` (the standalone safety-invariant scan the 2026-08-21 ADR's own D3
   re-targeted away from a spawned CRO). No caller outside persona mode ever passed `tier` or
   `personas` args, so no non-persona invocation is affected.
5. **No mechanical-gate replacement is commissioned** for the 9 seats retired by this ADR. The 8
   seats the 2026-08-21 ADR retired already have standing mechanical equivalents (that ADR's own §2
   D2 table) which are **unchanged and continue to stand** — this ADR does not touch them. The 9
   seats retired here (CEO conceptual apex aside — never a spawned persona) had no mechanical-gate
   equivalent commissioned, because the 2026-08-21 ADR never anticipated their retirement. This ADR
   does not manufacture one retroactively; see §6 Consequences for what that means going forward.
6. **The two prior ADRs are marked `Superseded-by` this ADR** (header field on each) with a short
   top-of-file addendum pointing here — their decision text is left untouched, per this repo's
   Trap-#12 discipline (a frozen ADR's ratified text is never rewritten in place).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Archive to `docs/personas/archive/` (this repo's default retirement convention) instead of deleting | Operator explicitly said "deleted completely," not "retired" — confirmed directly via `AskUserQuestion` rather than assumed. The 8 already-archived personas stay archived-then-deleted here, same as the 22 live ones; no special-casing. |
| Partial retirement (keep CFO/CIO, drop the rest) | Operator's instruction ("the personas") and the `AskUserQuestion` scope confirmation ("Everything, including all cross-references") both point at total retirement, not a second narrowing pass. |
| Delete the two ratifying ADRs themselves, per the operator's broadest stated option | Declined by design: every retirement in this repo's history (including the 8-seat retirement this very system performed 2026-08-21) marks the superseded ADR `Superseded-by`, never deletes it — ADRs are the permanent decision record (CLAUDE.md: "ADRs are canonical for every decision"). Flagged to the operator before proceeding; not silently overridden. |
| Merge PR #235 (the in-flight `docs/personas/` staleness-fix PR) first, then delete on top | The PR's entire diff was corrections to files this ADR deletes wholesale — landing it first would add a no-op merge commit for no benefit. Closed unmerged instead, with a comment pointing here. |
| Leave the generic (non-persona) 6-lens adversarial-panel pipeline retired along with persona mode | The pipeline predates persona mode and has no dependency on `docs/personas/`; retiring it would remove a load-bearing, still-useful general review tool over an unrelated feature's removal. Kept, persona-mode branch stripped instead (§2 item 4). |

---

## §4 — Falsifier (revert trigger)

**Revert trigger:** a genuinely recurring judgment-call class inside one of the 9 retired seats'
former Domains (capital-allocation rulings, cross-office coordination, research-synthesis
dedup-and-characterization work, execution-quality review) demonstrably goes unaddressed — not
merely "nobody happened to ask," but a real decision that needed that seat's independence property
(reviewer isolated from the proposer's live reasoning) and didn't get it — within three such
decisions after this ADR, or by the next quarterly programme-audit gate (2026-11-08), whichever
comes first.

**Revert action:** author a new ADR that supersedes this one in part, restoring the specific
seat(s) whose absence caused the gap. Never silently re-add a persona file without a superseding
ADR (§5).

**Trigger check schedule:** 2026-11-08 quarterly gate, or the 3rd qualifying gap, whichever is
first — matching the cadence convention the two superseded ADRs already used.

---

## §5 — Forbidden moves (genuinely tempting)

- **Quietly re-adding a persona file, the roster, or the ownership-map without a superseding
  ADR** — matches this repo's standing discipline for locked constants and prior persona
  retirements: change-control runs through re-registration, not a casual re-add.
- **Deleting the two now-superseded ADRs themselves** — considered and explicitly declined (§3).
  They stay, `Superseded-by` this one, exactly like every other superseded decision in this corpus.
- **Weakening or removing any of the 2026-08-21 ADR's own D2 mechanical gates** on the theory that
  "personas are fully gone now anyway" — those 8 gates were already the sole enforcement for their
  function as of 2026-08-21; this ADR changes nothing about that. Touching them needs their own
  ADR, unrelated to this one.
- **Retroactively inventing a mechanical-gate replacement for one of the 9 newly-retired seats**
  as part of this ADR's own implementation — that is new-decision work, not a mechanical
  consequence of retirement; do it as its own ADR if it's ever actually needed (§4).
- **Treating the generic 6-lens adversarial-panel pipeline as retired** because persona mode was
  stripped from the same file — it is a distinct, still-live tool (§2 item 4); do not remove or
  stop using it under the mistaken belief this ADR touches it.

---

## §6 — Consequences

**Gate verdict (binary, ties to §4):** this ADR reads **RESOLVED** if no §4 revert trigger fires
through the falsifier window; **FALSIFIED-IN-PART** for a specific seat if §4 fires and a
superseding ADR restores it.

**Positive consequences:**
- Removes the full remaining spawn cost/latency/maintenance surface of the persona-hierarchy
  system (roster upkeep, log-field validation, `INDEX.md` sync) for zero ongoing benefit the
  operator still wants.
- Matches the operator's now-stated preference directly, without an intermediate half-state.
- Simplifies `.claude/workflows/pre-ratification-adversarial-panel.js` back to a single,
  well-tested generic review pipeline — one mode to reason about, not two.

**Negative consequences (real cost, not theatrical):**
- Any judgment call that would have fallen inside one of the 9 retired seats' Domains — most
  notably CFO's subscription-ledger standing check and capital-allocation-ruling awareness, and
  Research Analyst's cross-campaign dedup/characterization function — now has no dedicated,
  independence-isolated reviewer. Falls to direct operator judgment or Claude Code's own review,
  same as anything that was already outside every persona's stated Domain.
- `docs/pursuits/SUBSCRIPTION_LEDGER.md`'s CFO-owned standing-check convention (added 2026-08-21,
  D3) loses its named executor; the monthly reconfirm cadence itself is unaffected (`STATE.md` §
  Scheduled forward triggers still fires it), but nothing now enforces the "flag any
  un-reconfirmed row whenever spawned for any reason" proactive trigger, since nothing is spawned.
- The two superseded ADRs' own downstream-artifact lists (mechanical gates, `check_personas.py`
  `EXPECTED_COUNT`, etc.) describe a system that fully no longer exists — read them as pure
  historical record from this ADR's date forward, not as a current description of anything live.

**Risks (probabilistic, distinct from costs):**
- The §4 falsifier depends on the operator or Claude Code noticing a gap in real time, since no
  mechanical gate is being added to detect it. Mitigation: the 2026-11-08 quarterly programme-audit
  gate is a scheduled backstop independent of anyone noticing anything in between.

**Downstream artifacts updated (this commit):**
- `docs/personas/` — entire tree deleted (34 files).
- `docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md`,
  `docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`,
  `docs/superpowers/plans/{2026-08-18-persona-roster,2026-08-18-validation,2026-08-18-panel-mechanics,2026-08-19-ownership-map-plan}.md`
  — deleted.
- `scripts/check_personas.py` — deleted.
- `.claude/workflows/pre-ratification-adversarial-panel.js` — persona-mode branch stripped; generic
  6-lens pipeline unchanged.
- `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md`,
  `docs/adr/2026-08-21-persona-hierarchy-front-office-only.md` — gain `Superseded-by` header field
  + a top-of-file addendum pointing here. Body text unchanged.
- `docs/adr/INDEX.md` — regenerated via `check_adr_graph.py --regenerate-index` (never hand-edited).
- `CLAUDE.md` — §Standing decision table row reworded to record full retirement, pointing here
  alongside the two original ADRs.
- `STATE.md` — dead links to `docs/personas/cfo.md` / `cfo-log.md` removed from the subscription
  reconfirm forward-trigger row; forward-obligation row's `docs/personas/*.md` sweep-scope mention
  removed (moot — the files no longer exist to sweep).
- `REPO_MAP.md` — `check_personas.py` row removed via `check_repo_map_scripts_table.py --write`.
- `docs/notes/audits/docs-runtime-inventory.md` — regenerated via
  `check_docs_runtime_inventory.py --write` (generated file, never hand-edited).
- `docs/notes/audits/2026-08-31-pursuits-personas-reversed-evidence-audit.md` (this session's own
  prior audit note) — gains a dated addendum pointing here, since its entire subject matter is now
  deleted; left in place as historical record of the audit work performed, not deleted itself.
- Every other file found to restate a persona-system claim as current (rather than historical) is
  fixed in the same commit — see the audit note this ADR's own implementation produces.
- `docs/SESSIONS.md` — new entry.

---

## §7 — Implementation plan

- **Phase 0** — §0 reads confirmed current at implementation time.
- **Phase 1** — mechanical deletions + the two ADR supersession headers, this commit.
- **Phase 2** — grep-sweep, two limbs (Known Trap #7 — source-of-truth fracture):
  - **(i) live claims** — any file asserting a persona/panel/roster fact as currently true (not
    historical narration of what happened) gets a fix, matching each file's own existing
    correction convention (append-only for logs that still exist elsewhere, inline dated note
    otherwise).
  - **(ii) generated mirrors** — `docs/adr/INDEX.md`, `REPO_MAP.md`'s scripts table, and
    `docs/notes/audits/docs-runtime-inventory.md` are regenerated via their own scripts, never
    hand-edited, per this repo's generated-mirror discipline.
  - Historical audit notes, closure docs, and prior ADR bodies describing what the persona system
    did *at the time* are left untouched — accurate history, not a live claim.
- **Phase 3** — full gate suite (`scripts/gate_manifest.py --tier check`) run clean before commit.

---

## §10 — Audit hooks (runnable)

```bash
# Discipline checks
python scripts/check_brief.py docs/adr/2026-08-31-persona-hierarchy-full-retirement.md --type adr
python scripts/check_adr_graph.py

# docs/personas/ fully gone
test ! -d docs/personas && echo "OK: docs/personas/ removed"

# check_personas.py fully gone
test ! -f scripts/check_personas.py && echo "OK: check_personas.py removed"

# No live PERSONA_REGISTRY / persona-mode code remains in the panel workflow
grep -n "PERSONA_REGISTRY\|personaMode" .claude/workflows/pre-ratification-adversarial-panel.js
# Expected: no hits

# Both prior ADRs point here
grep -l "Superseded-by.*2026-08-31-persona-hierarchy-full-retirement" \
  docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md \
  docs/adr/2026-08-21-persona-hierarchy-front-office-only.md
# Expected: both files listed

# Full gate suite
python scripts/gate_manifest.py --tier check
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-31 | Initial authoring + acceptance (operator: "I have changed my mind on the personas, I want them deleted completely") | Joshua + Claude Code |
| 2026-09-01 | `Supersedes` header field split into one parseable edge per line, scope word normalized "in full" → "full" — the original single-line multi-target form was invisible to `check_adr_graph.py` (FIELD_RE takes only the first filename per field line; scope vocabulary is `full`/`in part` — the exact §8 parser limitation the 2026-08-31 corpus audit flagged), so A2 never saw either edge and neither prior ADR could pass `retire_adr.py`'s supersede precondition. No semantic change: same two targets, same full scope the ratified prose above already declares. §2 item 6's marking executed the same day via `scripts/retire_adr.py` on both prior ADRs (stubs + `docs/ltm/adr/` bodies). | Claude Code (ADR-corpus reconciliation sweep) |
