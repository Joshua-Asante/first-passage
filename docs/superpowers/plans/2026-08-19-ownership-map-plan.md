# Ownership Map Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan phase-by-phase. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Divide the entire First Passage repo among the persona hierarchy, so any future decision,
investigation, or new artifact has a clear first-line owner without re-deriving one from scratch.

**Architecture:** Three layers, each independently useful and separately executable — a directory
skeleton (coarse, fast), a pursuit-level refinement (medium, fans out over 38 records), and a
standing classification rule for anything new (never "done," a repeatable procedure). Layer 1 is
already drafted (this plan documents what shipped and what's still open); Layers 2-3 are specified
here for later execution, not run in this pass.

**Tech Stack:** Markdown content + the Workflow tool's `parallel()` fan-out pattern, matching the
pattern already proven against the 11 Q-briefs from PR #53 (session-internal precedent, not part of
this repo's own tooling).

## Global Constraints

- "Owner" means first-line reviewer/delegate, not modification authority — this plan never touches
  who is allowed to *edit* anything (locked-parameter authority is untouched, per CLAUDE.md §Key
  Principle).
- No file gets assigned to more than one *primary* persona. Secondary stakeholders are named only
  where they have real work to do, not everyone tangentially related — this was a hard-won discipline
  from the original persona-hierarchy design (§5.2's own "sized to real current standing work, not
  padded" principle) and applies here too.
- Every classification must be grounded in the artifact's actual content (its stated Aim/H/falsifiable
  question), never inferred from a filename or directory location alone, once Layer 2 or 3 is doing
  the classifying — Layer 1's directory-level assignment is the one place a location-based default is
  acceptable, precisely because it's the coarse skeleton later layers refine.
- `docs/personas/ownership-map.md` is the single durable artifact all three layers write into —
  no parallel ownership-tracking file gets created.

## File Structure

```
docs/personas/ownership-map.md         <- exists (Layer 1 shipped); Layers 2-3 append here
```

---

### Phase 1: Directory skeleton — SHIPPED

**Status:** Done, same commit as this plan. `docs/personas/ownership-map.md` Layer 1 covers `core/`,
`lab/`, `ops/`, `docs/`, `.claude/`, `scripts/`, and root files, each with a primary + (where real)
secondary persona and a one-line rationale.

**Known gaps, deferred rather than guessed at now:**
- `docs/analytics/` — flagged unconfirmed pending a content check (assigned Head of Validation
  provisionally).
- `core/lib/`, `lab/research_utils/` vs `lab/tools/` — assigned by inference from directory naming,
  not by reading actual import graphs; Phase 2 or a dedicated cheap follow-up should confirm rather
  than let the guess calcify.

No task checkboxes here — this phase is complete, not pending.

---

### Phase 2: Pursuit refinement — SHIPPED

**Status:** Done, same commit as this update. All 38 pursuits classified via the exact Workflow
pattern specified below; 18/38 diverged from their Layer-1 directory default, 28/38 flagged
cross-cutting. One manual correction made on review (e1 → CEO, not Head of Governance, per the
roster's own Aim-ownership charter line). See `docs/personas/ownership-map.md` Layer 2 for the full
table and the divergence/cross-cutting synthesis.

**Known rough edge carried into Layer 3**: the `confirmedOffice` schema's `Cross-office` value
overlapped conceptually with the separate `crossCuttingFlag` boolean in this run — worth tightening
before reusing this schema shape again.

<details>
<summary>Original task spec (superseded by the above — preserved for provenance)</summary>

**Files:**
- Modify: `docs/personas/ownership-map.md` (append a "Layer 2" results table, replacing the current
  "not yet run" placeholder)

**Interfaces:**
- Consumes: the 38 records under `docs/pursuits/*.md`, each already carrying an Aim tag from the
  GSUB-1 GRAND-tier inventory; the Layer 1 directory skeleton above as the default a pursuit inherits
  from unless its content says otherwise.
- Produces: one row per pursuit — `{pursuitId, title, inheritedOffice, confirmedOffice,
  primaryPersona, secondaryPersonas, crossCuttingFlag, rationale}` — appended to
  `docs/personas/ownership-map.md`.

- [ ] **Step 1: Fan out a classification Workflow over all 38 pursuits**

Mirror the pattern already run for the 11 Q-briefs (this session, `wf_81e9d906-e67` — see that run's
journal for the exact schema/prompt shape if resuming the pattern verbatim). One agent per pursuit,
`parallel()` fan-out, each agent:
1. Reads `docs/pursuits/<file>.md` in full.
2. Reads whichever Layer-1 directory row(s) the pursuit's own content most directly touches (e.g.
   a pursuit whose Aim cites `lab/discovery/` inherits Head of Research by default).
3. Confirms the inherited office/persona, or names a different one with a one-sentence reason if the
   pursuit's actual content doesn't match the directory-level default.
4. Flags `crossCuttingFlag: true` for any pursuit that genuinely doesn't fit one office (expect a
   small number — most of the 38 should inherit cleanly).

Structured-output schema (JSON Schema, pass via the Workflow tool's `agent()` `schema` option):
```json
{
  "type": "object",
  "properties": {
    "pursuitId": { "type": "string" },
    "title": { "type": "string" },
    "inheritedOffice": { "type": "string", "enum": ["Front", "Middle", "Back", "Cross-office"] },
    "confirmedOffice": { "type": "string", "enum": ["Front", "Middle", "Back", "Cross-office"] },
    "primaryPersona": { "type": "string" },
    "secondaryPersonas": { "type": "array", "items": { "type": "string" } },
    "crossCuttingFlag": { "type": "boolean" },
    "rationale": { "type": "string" }
  },
  "required": ["pursuitId", "title", "inheritedOffice", "confirmedOffice", "primaryPersona", "secondaryPersonas", "crossCuttingFlag", "rationale"]
}
```

- [ ] **Step 2: Reconcile disagreements between inherited and confirmed office**

Any pursuit where `inheritedOffice != confirmedOffice` is a real signal the Layer-1 directory default
was wrong for that specific pursuit (not a Layer-2 error) — note these explicitly in the appended
table rather than silently overwriting Layer 1's rationale, so a future reader can see where the
coarse skeleton and the content-level read diverged and why.

- [ ] **Step 3: Append the Layer 2 table to `docs/personas/ownership-map.md`, replacing the
  "not yet run" placeholder**

- [ ] **Step 4: Commit**

```bash
git add docs/personas/ownership-map.md
git commit -m "docs(personas): ownership map Layer 2 -- all 38 pursuits classified"
```

</details>

---

### Phase 3: Standing classification procedure — SPECIFIED, ONGOING (not a one-time task)

**Status:** The procedure itself is already written (`docs/personas/ownership-map.md` "Layer 3"
section) and has already been exercised for real once (the 11 Q-briefs from PR #53, done earlier
this session, before this plan existed). There is no discrete "finish Phase 3" task — it's a standing
convention applied each time a new Q/ADR/pursuit is opened and doesn't cleanly inherit from Layers
1-2.

**The one legitimate follow-up task**, if this is ever revisited:
- [ ] Consider whether Layer 3's procedure should be wired into a Staff-tier gate (e.g., a
  Documentation Analyst or Research Registry Analyst check that a new artifact carries an ownership
  classification before it's considered fully opened) rather than staying a manually-applied
  convention. **Deliberately not built now** — this would be new infrastructure on top of a
  three-hour-old, once-exercised procedure; matches this design's own §8 "Full bespoke build" rejected
  alternative (highest cost, unproven need). Revisit only if the manual procedure is skipped or
  misapplied often enough to justify it.

---

## Out of scope for this plan

- Assigning ownership below the pursuit level (individual files inside a pursuit's own working
  directory, e.g. everything under one `lab/analysis/<theme>/<slug>/` body) — Layer 2's pursuit-level
  grain is the intended floor; going finer is exactly the "assign every file individually" scope the
  brainstorming session's own scope-check rejected as disproportionate.
- Retrofitting ownership onto closed/terminal pursuits beyond naming Head of Governance as their
  custodian (already done in Layer 1's terminal-register row) — dead things don't need an active
  owner, just someone who knows where they're buried.
- Building any automation/gate around this map (see Phase 3's one deferred follow-up) — this plan
  produces a reference document, not new tooling.
