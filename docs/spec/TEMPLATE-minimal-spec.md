# Minimal spec template (standing convention, 2026-08-07)

Style rule: fewest steps, fewest words. Objective ≤1 sentence; every apparatus line is one
line. Anything longer belongs in an ADR or brief — link it, never restate it.

```
# SPEC: <title>
Status: PROPOSED · <date> · authorizes nothing ($0 · K=0) · depends: <S-refs or —>
Objective: <one sentence>

Steps:
1. <fewest possible; name the actor when not obvious>

Gate: RESOLVED if <binary>; FALSIFIED if <binary>.
Boundary: <what stays forbidden — genuinely tempting moves only>
Reads: <path> @ <anchor> · …
Owner: <docking Q-/ADR/spec thread, or "new">
```

Keeps the load-bearing minimum of the brief discipline — read-anchors, binary gate,
forbidden moves — at one line each; drops the rest of the §0–§10 apparatus. A spec in this
form decides nothing: ratification still runs through an ADR or an explicit operator block —
at the tier [ADR 2026-08-08](../adr/2026-08-08-adr-ceremony-tiering.md) assigns (limb-free
decisions take the ≤300-word light record form).
Ratified as the standing spec style by JA 2026-08-07. Worked examples: the
`2026-08-07-loop-s*` series ([index](2026-08-07-loop-spec-index.md)).
