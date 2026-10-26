# Lesson E-[N] — [Short lesson title]

**Lesson ID:** E-[N] (execution) | M-[N] (methodology) | B-[N] (behavioral) | O-[N] (operational)
**Status:** `Candidate` | `Standing rule` | `Retired (superseded by E-M)` | `Retired (no longer applicable)`
**Captured:** YYYY-MM-DD
**Promoted to standing rule:** YYYY-MM-DD (or `N/A` if Candidate)
**Author:** Joshua | claude.ai
**Registry file:** `docs/methodology/lessons/execution_lessons.md` | `docs/methodology/lessons/methodology_lessons.md`

---

## Pattern (one sentence)

The recurring failure mode this lesson captures, stated as a pattern not a story.

[One sentence. "Citing the MC anchor from memory rather than from its owning repo doc produces stale numbers within ~2 weeks of any allocation refresh." — not "On 2026-04-29 we cited stale MC numbers."]

---

## Anchor incidents

Per Known Trap #9: every lesson carries at least one dated incident and its source artifact; there is no dollar field or dollar threshold ([`methodology_lessons.md` §Format spec](../../../../docs/methodology/lessons/methodology_lessons.md#format-spec)). Once written, the lesson is in force as a registry lesson; it becomes a `Standing rule` (standing guidance in a skill, hook, AGENTS.md or rule) only on a high-severity incident or independent recurrence (AGENTS.md §Continuous improvement item 5); otherwise it stays `Candidate`.

| Date | Incident | Impact | Source brief |
|---|---|---|---|
| YYYY-MM-DD | [one sentence describing the firing] | [what it cost: wrong verdict, rework, or counterfactual] | [path to Pre-Q / ADR / audit note] |
| YYYY-MM-DD | [second firing if applicable] | [impact] | [source] |
| YYYY-MM-DD | [third firing if applicable] | [impact] | [source] |

**Standing-guidance bar:**
- [ ] High-severity incident
- [ ] OR independent recurrence

---

## Repair / discipline rule

The specific rule that, if followed, would have prevented the anchor incidents.

**Rule:** [Present-tense imperative. "Before citing MC anchor numbers, read `docs/mc_anchor_history.md`; do not quote from memory."]

**Where the rule lives (canonical enforcement point):**
- [ ] SKILL.md body — which skill, which section
- [ ] Brief template — which template, which section
- [ ] check_brief.py — which check (if mechanically enforceable)
- [ ] Operational checklist — `docs/operational_rules.md` or a Todoist standing task
- [ ] Calendar trigger — recurring check

If the rule has no canonical enforcement point, it's a wish, not a discipline. Flag and either find the enforcement surface or downgrade to Candidate.

---

## Cross-references

- **Briefs citing this lesson:** [list of Pre-Q / ADR / closure paths]
- **Skills enforcing this lesson:** [list of skills that load this rule]
- **Related lessons:** [E-M / M-K — sibling lessons in the same failure family]
- **Superseded lesson (if any):** [E-L — what this replaces and why]

---

## Promotion record (if applicable)

Skip unless Status = `Standing rule`.

- **Promoted on:** YYYY-MM-DD
- **Promoted by:** [Joshua decision | high-severity incident | independent recurrence]
- **Promotion rationale:** [one paragraph — why this earned standing-rule status]
- **Promoting brief / chat / decision:** [path or chat URL]

---

## Retirement (if applicable)

Skip unless Status = `Retired`.

- **Retired on:** YYYY-MM-DD
- **Retirement reason:** [superseded by E-M | no longer applicable due to architectural change | degenerated]
- **Tombstone note:** [one sentence preserving the historical context — what this lesson taught while it was active]

---

## Audit hooks

```bash
# Confirm the lesson is referenced by the briefs/skills it claims to enforce
grep -rn "E-[N]" docs/ .claude/skills/ 2>/dev/null
# Expected: matches "Briefs citing" and "Skills enforcing" lists above

# If Status = Candidate: check for an independent recurrence
# Re-evaluate quarterly: YYYY-MM-DD
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py <this-file>.md --type lesson
# Expected: RESULT: well-formed (canonical skill-side checker — ADR 2026-08-09;
# validates the named-heading contract: Pattern, Anchor incidents, Repair, Audit hooks)
# Candidate lessons pass with empty Promotion record if status is explicitly Candidate

$ python scripts/check_brief.py <this-file>.md --type lesson
# Expected: RESULT: NOT CHECKED (repo-side declines lesson — expected, not a gap;
# the skill-side result above is the one that counts)
```

Lessons fail by being abstract. The check: can you write a grep command in §Audit hooks that mechanically detects the failure mode next time? If no, the lesson is still a hypothesis — keep as Candidate.
