# SPEC S7: repo alignment (Posture-A propagation)

Status: PROPOSED · 2026-08-07 · authorizes nothing ($0 · K=0) · depends: consumes S1–S6 +
the W1/W3/W4/W5/W6 rulings as they land
Objective: Every Posture-A ruling lands with its propagation sweep executed in the same PR,
from the pre-built [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md)
— no surface left silently restating the superseded state.

**Progress (2026-08-07 Phase 7; tombstone 2026-08-21):** W1 ADR `Proposed` (method freeze + re-run authorized;
RESULTS owed) · W3 **blocked/deferred** (gated on first S3 family TV anchor) · W4/W5/W6
ADRs `Accepted` with same-PR sweeps · CI re-enable + `requirements-research.lock` + W1
RESULTS remain owed. The row-body manifest is a **tombstone** on this public tree
([`docs/notes/2026-08-07-posture-a-alignment-manifest.md`](../notes/2026-08-07-posture-a-alignment-manifest.md))
— do not treat missing `✔` rows as discharged. S7 `RESOLVED` is blocked until restore.

Steps:
1. At each trigger ADR/build's landing, discharge that trigger's manifest section in the
   same PR: Superseded-in-part edges on the named owner ADRs (express, never silent — the
   M1 item-5 operative forbids silent redefinition by name); mirrors/pointers refreshed;
   frozen artifacts (survivor-scoring prereg, LOCKED specs) only via close+reopen.
2. Immediate $0 items, no trigger owed: `stage24_runner.py:6` spent docstring limb ·
   `operational_rules.md:170` retired-`params.toml` owner-table row (+ edit-log line) ·
   brief-authoring reference-files list missing `closure_record.md`.
3. After each landing, re-run the blast-radius skill and append dated `✔` + commit to the
   discharged manifest rows.

Gate: RESOLVED when every manifest row carries a dated discharge or reclassification;
FALSIFIED if any trigger ADR merges without its manifest section swept in the same PR.
Boundary: nothing edits ahead of its trigger · historical ADR bodies stay byte-frozen
(addenda/Superseded-by only) · reflex layer and locked constants untouched.
Reads (at HEAD `a6a5fe6` 2026-08-07): the manifest · `.claude/skills/blast-radius/SKILL.md`.
Owner: [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md) (rows) ·
this spec (discipline).
