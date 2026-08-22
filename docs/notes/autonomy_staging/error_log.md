# Autonomy Staging — Error/Catch Log

Governed by [`docs/adr/2026-08-21-stage2-stage3-progression-criteria.md`](../../adr/2026-08-21-stage2-stage3-progression-criteria.md)
§2 Phase 1 (§4 falsifiable hypothesis; §6 gate). Log **every** audited autonomous
session, including clean ones — the clean count is the denominator the §4
hypothesis depends on. Append-only: do not edit rows once logged; a correction
lands as a new row citing the row it corrects, never an in-place edit.

| # | Date | Artifact | Claim checked | Caught? | Error type | How caught |
|---|------|----------|----------------|---------|------------|-------------|
| 1 | 2026-08-21 | PR #86 closure report | Write-back "item 3" needed building; provenance cited as PR #37 (2026-07-14) | Y | Fabricated/wrong citation | `gh pr view 37` — unrelated content, actually merged 2026-08-18. Independently re-confirmed same-day in the authoring CC session (root-caused to a merge-commit misattribution: `2e4d063`/PR #37 is the commit where the files first entered this repo's tracked history, a large unrelated bulk-merge, not their true author; the `a38676d` anchor cited elsewhere for the 2026-07-14 date does not exist as a git object in the public repo — pre-2026-08-14 history was squashed at the public-visibility transition). Public correction posted: PR #86 comment [#5377130526](https://github.com/Joshua-Asante/first-passage/pull/86#issuecomment-5377130526). |
| 2 | 2026-08-21 | PR #86 closure report | Step 2.2 required new implementation | Y (self-corrected by CC pre-report) | Redundant-work belief | Cross-check against `lab/discovery/lifecycle_call1/` found dormant implementation already existed |
| 3 | 2026-08-21 | `main` CI (validation-controls) | Failure isolated to PR #86 | Y | Silent pre-existing drift | Checked last 3 `main` CI runs independently; 2/3 also failing; traced to `date_coverage == 0.80` boundary |

**Running tally:** 3 sessions logged, 3 with ≥1 catch. Consecutive-clean streak: 0. (Needs 10 consecutive with no *new* category to exit Phase 1 — see ADR §4/§6.)

---
*Append new rows below this line.*
