# Audit Note — [Short audit title]

**Audit ID:** AUDIT-YYYY-MM-DD-[short-slug]
**Date:** YYYY-MM-DD
**Triggered by:** [methodology failure | unexpected outcome | scheduled audit | external observation]
**Authors:** Joshua + claude.ai
**Scope:** [single brief | brief family | skill | framework layer | portfolio decision]
**Lives in:** `docs/notes/audits/AUDIT-YYYY-MM-DD-slug.md` or Notion

---

## §0 — Source anchors

What artifacts are being audited. Audits cite specific commits / page IDs / chat URLs — vague audits produce vague repairs.

- `docs/briefs/Q-X-name.md` — commit `<hash>` (the brief being audited, or where the failure originated)
- `<chat URL>` — the session where the failure surfaced
- `Notion: <page>` — page ID `<id>` (state at audit time)
- `data/...` — commit `<hash>` (data referenced by the audited artifact)

---

## §1 — Trigger (what prompted this audit)

The specific event that opened the audit. Not abstract — name the dated incident.

[2–4 sentences. "On 2026-04-29 the dd_protection Pre-Q cited MC anchor 98.13/0.22/4.49 from memory; CC's Phase 0 read against production showed 97.88/0.22/4.55. The discrepancy halted the brief at Pre-A and required re-authoring §1 motivation."]

**Failure class (one of):**
- Methodology failure (discipline check didn't fire when it should have)
- Decision failure (correct discipline, wrong call)
- Source-of-truth fracture (canonical artifact drift)
- Skill drift (SKILL.md no longer matches actual practice)
- Investigation degeneration (SNAG / belt-only-grows / falsifier creep)
- Other: [specify]

---

## §2 — What actually happened

Sequence of events, in order. Distinguish facts from interpretation.

1. [Event 1 — what was attempted / authored / decided]
2. [Event 2 — what surfaced the failure]
3. [Event 3 — how the failure was contained / addressed in-session]

If multiple parties / sessions / artifacts were involved, name each.

---

## §3 — Discipline checks that should have caught it

Cross-reference to brief-authoring SKILL.md §1-10 (the six general checks + checks 7-10 for CC handoffs). For each check that was relevant, mark whether it fired, failed silently, or wasn't applicable.

| Check | Should have caught | Actual behavior |
|---|---|---|
| §1 Rule 0 reads | [yes — §0 anchor would have surfaced the discrepancy] | [missed — §0 cited memory not commit hash] |
| §2 Falsifiable hypothesis | [N/A — pre-data phase] | — |
| §3 Forbidden moves | [yes — citing memory anchor was on the list] | [list was generic, didn't name this specific failure] |
| §4 Gate criteria binary | — | — |
| §5 Question form | — | — |
| §6 Audit hooks runnable | — | — |
| §7-10 CC handoff checks | — | — |

If a check that should have fired didn't, the audit's first repair target is that check.

---

## §4 — Root cause analysis

Why did the failure get through? Push past first-cause to structural cause.

- **Immediate cause:** [what directly caused the failure — usually a single missed check or assumption]
- **Contributing factor:** [what made the immediate cause likely — pattern, schedule pressure, tool limitation]
- **Structural cause:** [what about the framework or skill or convention allowed this — the load-bearing repair target]

Five-whys is a useful frame but stop at the first structurally repairable layer; don't chase to first principles when a concrete repair surface exists.

---

## §5 — Repair plan

Two layers: immediate (close out this specific instance) and structural (prevent next instance).

### Immediate

- [ ] [Specific action — re-author the affected brief / correct the stale Notion page / re-run analysis with correct anchor]
- [ ] [Specific action]

### Structural

- [ ] [Skill update — which SKILL.md, which section]
- [ ] [Template update — which references/*.md, which section]
- [ ] [Validator update — which check in check_brief.py]
- [ ] [Calendar / Todoist trigger — what recurring check would have surfaced this]
- [ ] [Notion page restructure — if source-of-truth fracture]

If no structural repair exists, the failure is likely to recur. Flag this explicitly — sometimes the right call is to accept the recurrence rather than over-engineer; sometimes it surfaces a deeper architectural gap.

---

## §6 — Lessons to capture

Candidate lessons emerging from this audit. Per Known Trap #9, lessons need dated anchor + dollar cost / counterfactual to graduate. This section seeds lesson_capture entries.

- **Candidate lesson 1:** [pattern statement]
  - Anchor: [this audit]
  - Cost: $[N] OR counterfactual
  - Lesson registry destination: `references/[type]_lessons.md`
  - Promotion status: Candidate (needs [N-1] more firings or structural-argument approval)

- **Candidate lesson 2:** [pattern statement]
  - Anchor: [this audit]
  - ...

If existing lessons already cover the pattern, cite them rather than creating duplicates:
- Already covered by: E-N, M-K, etc.

---

## §7 — Programme-audit signal check (cross-skill)

The programme-audit skill watches for degeneration signals. This audit MAY indicate degeneration of the framework/portfolio it touched. Check explicitly:

- [ ] Belt-patches without independent corroboration?
- [ ] Belt that only grows, never prunes?
- [ ] Falsifier thresholds drifting toward "we'd never hit this"?
- [ ] Methodology invoked to rationalize a decision already made?
- [ ] SNAG pattern (multiple null/ambiguous loops same domain)?
- [ ] Cross-layer contamination (methodology citing portfolio evidence or vice versa)?
- [ ] Negative heuristic crossed without repair?

If any box is checked, escalate to programme-audit for the affected layer (meta or object). This audit then becomes input to that larger audit; do not close it here.

---

## §10 — Audit hooks (forward-looking)

How will we detect the next instance of this failure mode?

```bash
# Mechanical detector for the specific failure pattern
[ specific grep / script / assertion ]

# Recurrence check schedule
# Quarterly review: YYYY-MM-DD — re-run §10 hooks against current state

# Cross-reference to spawned lesson entries
grep -rn "AUDIT-YYYY-MM-DD-slug" references/*lessons.md
# Expected: matches §6 candidate lessons that graduated
```

---

## §11 — Closure

- **Status:** `Open` | `Repair-in-flight` | `Closed (immediate + structural complete)` | `Closed (immediate only — structural deferred to YYYY-MM-DD)`
- **Immediate repair completed:** YYYY-MM-DD
- **Structural repair completed:** YYYY-MM-DD
- **Lessons graduated to standing rule:** [list of lesson IDs that promoted]
- **Follow-up audits triggered:** [list]

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py <this-file>.md --type audit
# Expected: RESULT: NOT CHECKED (audit is an unmodeled contract type)

# Confirm §5 structural repair list is actually executed
$ <grep / git log commands confirming each structural-repair line shipped>

# Confirm §6 candidate lessons exist in registry
$ grep -l "AUDIT-YYYY-MM-DD-slug" references/*lessons.md
```

Audit notes fail by capturing the trigger without naming the structural cause. The check: would running §10 hooks next quarter actually detect a recurrence? If no, §4 root cause didn't reach far enough — push deeper.
