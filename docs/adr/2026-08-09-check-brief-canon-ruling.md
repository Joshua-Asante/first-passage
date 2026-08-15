# ADR 2026-08-09 — check_brief canon: skill-side governs; repo-side declines what it cannot check

**Status:** `Accepted` — ratified by operator (JA) 2026-08-09, in-session instruction ("make your best calls on … checker-canon split")
**Decision date:** 2026-08-09
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** governance convention. **$0 / K=0.**

## Decision

The **skill-side** `check_brief.py` is canonical for brief discipline; repo-side
`scripts/check_brief.py` is its mechanical subset — this settles the UNRULED question rather than
changing the answer its own docstring already gave. Repo-side now **declines** types whose section
contract it does not model (`lock`, `notice`, `lesson`, `audit`, and `light`-tier records →
`RESULT: NOT CHECKED`) instead of applying the `generic` contract to them, and its §4 check accepts
every canonical framing (`Revert trigger`, if/then, reject/accept-if), not only a literal
`H:`+`falsifi*` pair.

## Grounds

Measured 2026-08-09: repo-side declared **6 of 7** of the skill's own canonical templates MALFORMED
and false-FAILed real artifacts skill-side passes 6/6. Cause was a **wrong section contract**, not
extra strictness — an audit note's §4 is root-cause analysis; a notice log's §0 is explicitly *"one
line, not a verified-commit list"*. A false MALFORMED trains authors to ignore the checker.
Divergence also ran the other way (6 ADRs repo-side blessed and skill-side rejects), so neither is a
safe sole gate. This record is itself the first `light` ADR, and drafting it surfaced that the light
tier was equally unmodeled.

## Reads

`scripts/check_brief.py` @ `47cc3eb` · skill-side checker (untracked; `--self-test` PASS) ·
`.claude/skills/brief-authoring/SKILL.md:145` (canonical §4 form) ·
[`ceremony tiering`](2026-08-08-adr-ceremony-tiering.md) (light-tier definition) · `scripts/gates.yml`
— 15 gates, **neither checker in any tier**, no CI job runs either.

## Gate

RESOLVED — 7/7 canonical templates non-failing repo-side, this light record non-failing, 31/31 tests
green, and [`2026-07-28 ADR`](2026-07-28-c1-disaster-stop-payload-supported.md)`:187` (which asserted
the opposite canon) corrected.

## Boundary

Do **not** promote repo-side to a gate tier on the strength of this fix — it remains a subset and the
2026-08-08 belt-churn watch flag is live. Do not "fix" a declined type by widening `generic` to
swallow it.
