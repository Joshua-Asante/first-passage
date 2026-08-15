---
name: warn-blast-radius
enabled: true
event: stop
action: warn
conditions:
  - field: transcript
    operator: regex_match
    pattern: "Write|Edit|MultiEdit"
  - field: transcript
    operator: not_contains
    pattern: "BLAST-RADIUS:"
---

📐 **Blast-radius sweep owed before you stop.**

This turn wrote/edited files. Before ending, run the `blast-radius` skill
(`.claude/skills/blast-radius/SKILL.md`) on the diff:

1. Extract old→new tokens from `git diff`
2. Grep hot surfaces for the **old** tokens (CLAUDE / STATE / PIPELINES /
   ADRs / skills / CATALOG / instruments)
3. Emit a `BLAST-RADIUS: CLEAN|OWED|REPAIRED` report table

Report-first. Fix clear silent restatements and stale one-line pointers owed
by this change. Do **not** restate canonical values (Rule 7). Skip if the turn
was read-only or only touched the blast-radius skill/hooks themselves.

Cursor mirrors this via `.cursor/hooks/blast_radius_stop.py` (stop follow-up).
