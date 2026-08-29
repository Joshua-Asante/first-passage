# Lesson E-[N] — [Short lesson title]

**Lesson ID:** E-[N] (execution) | M-[N] (methodology) | B-[N] (behavioral) | O-[N] (operational)
**Status:** `Candidate` | `Standing rule` | `Retired (superseded by E-M)` | `Retired (no longer applicable)`
**Captured:** YYYY-MM-DD
**Promoted to standing rule:** YYYY-MM-DD (or `N/A` if Candidate)
**Author:** Joshua | claude.ai
**Registry file:** `references/execution_lessons.md` | `references/methodology_lessons.md` | etc.

---

## Pattern (one sentence)

The recurring failure mode this lesson captures, stated as a pattern not a story.

[One sentence. "Citing the MC anchor from memory rather than from the Notion canonical page produces stale numbers within ~2 weeks of any allocation refresh." — not "On 2026-04-29 we cited stale MC numbers."]

---

## Anchor incidents

Per Known Trap #9: a lesson without a dated incident AND a dollar cost / counterfactual does not graduate. Below the promotion gate (single-incident >$3K, OR three firings across separate windows), the lesson stays `Candidate`.

| Date | Incident | Cost / counterfactual | Source brief |
|---|---|---|---|
| YYYY-MM-DD | [one sentence describing the firing] | $[N] realized OR [counterfactual description] | [path to Pre-Q / ADR / audit note] |
| YYYY-MM-DD | [second firing if applicable] | $[N] OR counterfactual | [source] |
| YYYY-MM-DD | [third firing if applicable] | $[N] OR counterfactual | [source] |

**Promotion gate status:**
- [ ] Single incident >$3K dollar anchor (promotes immediately)
- [ ] OR three firings across separate windows (promotes on third)
- [ ] OR structural argument (rare — must explicitly justify why empirical gate is bypassed; see CC-handoff hygiene 2026-05-15 anchor)

---

## Repair / discipline rule

The specific rule that, if followed, would have prevented the anchor incidents.

**Rule:** [Present-tense imperative. "Before citing MC anchor numbers, fetch from Notion *📊 Portfolio MC Lock Details* (page ID `35cdc0b53c11813e82fdf5f09f36a459`); do not quote from memory."]

**Where the rule lives (canonical enforcement point):**
- [ ] SKILL.md body — which skill, which section
- [ ] Brief template — which template, which section
- [ ] check_brief.py — which check (if mechanically enforceable)
- [ ] Operational checklist — Notion page or Todoist standing task
- [ ] Calendar trigger — recurring check

If the rule has no canonical enforcement point, it's a wish, not a discipline. Flag and either find the enforcement surface or downgrade to Candidate.

---

## Cross-references

- **Briefs citing this lesson:** [list of Pre-Q / ADR / lock decision paths]
- **Skills enforcing this lesson:** [list of skills that load this rule]
- **Related lessons:** [E-M / M-K — sibling lessons in the same failure family]
- **Superseded lesson (if any):** [E-L — what this replaces and why]

---

## Promotion record (if applicable)

Skip unless Status = `Standing rule`.

- **Promoted on:** YYYY-MM-DD
- **Promoted by:** [Joshua decision | structural argument approved | empirical gate met]
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
grep -rn "E-[N]" docs/ /mnt/skills/user/ 2>/dev/null
# Expected: matches "Briefs citing" and "Skills enforcing" lists above

# If Status = Candidate: check for third firing
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
