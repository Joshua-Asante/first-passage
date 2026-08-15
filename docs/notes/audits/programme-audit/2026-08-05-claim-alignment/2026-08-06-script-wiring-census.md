# Script wiring census (FU-17)

**Audit:** [`2026-08-05-claim-alignment`](README.md) · **Task:** 1.9 / FU-17
**Anchor:** claim-alignment-phase1 worktree, 2026-08-06

Mechanical floor (**R21**): `16` scripts named in neither `Makefile`,
`scripts/githooks/pre-commit`, `.github/workflows`, nor `.claude/settings*.json`.
Audit union **22 unwired ∪ mis-scoped** adds **6** scripts that *are* wired but
read the wrong surface — established by hand (e.g. **R8**, **R16**, **H4**), not
by pattern grep alone.

**Dispositions:** TBD at 2026-11-08 operator wire-or-retire ruling. This artifact
does not execute repairs (per FU-17).

## Worked example — vacuous green (unwired + mis-scoped)

| Script | Invoked by | Declared scope | Measured scope | Disposition |
|---|---|---|---|---|
| `pine_check_audit.sh` | nothing | Oracle regression on locked `.pine` paths | Prints `== audit PASS ==` with **0/4** oracles present (coldstore paths); exit 0 | TBD |
| `pine_check_audit.ps1` | nothing | Same (Windows entry) | Same vacuity on operator platform | TBD |

See **A24 / A25** in [`03-agent-facing.md`](03-agent-facing.md).

## `scripts/*.py` census (37 files)

| Script | Invoked by | Declared scope | Measured scope | Disposition |
|---|---|---|---|---|
| `archive_lab_analysis.py` | pre-commit; skills-check.yml | archive_lab_analysis.py — STM/LTM archive for lab/analysis studies. | Aligned (no audit flag at census date) | TBD |
| `archive_strategy.py` | nothing | archive_strategy.py — Phase A cold-store helper for strategy Pine + docs. | Unwired (floor census) | TBD |
| `check_adr_graph.py` | pre-commit; skills-check.yml | check_adr_graph.py — ADR lifecycle graph gate (governance tier). | A7 check exists but excluded from DEFAULT_ENABLED_CHECKS (FU-7) | TBD |
| `check_advisor_dedup.py` | nothing | check_advisor_dedup.py — prior-art search for a staged advisor/handoff artifact. | Unwired (floor census) | TBD |
| `check_boundaries.py` | pre-commit; tests.yml | check_boundaries.py — AST import-boundary scanner for the 4-layer monorepo. | Aligned (no audit flag at census date) | TBD |
| `check_brief.py` | nothing | check_brief.py — brief well-formedness validator. | Unwired (floor census) | TBD |
| `check_closure_disposition.py` | pre-commit | docs/briefs/closures/*.md, minus the GRANDFATHERED set (the 34 closures | Aligned (no audit flag at census date) | TBD |
| `check_data_manifests.py` | pre-commit; manifest-check.yml | Verify or regenerate SHA256SUMS manifests for gitignored vendor CSV trees. | Aligned (no audit flag at census date) | TBD |
| `check_falsifier_reachability.py` | settings.json / docs (grep) | WARN-tier gate: do standing ADR falsifiers still have inputs that exist? | WARN-tier; ~26% anchored; not in make check / pre-commit by design | TBD |
| `check_md_relative_links.py` | settings.json / docs (grep) | check_md_relative_links.py — file-relative markdown link liveness (warn-only). | Aligned (no audit flag at census date) | TBD |
| `check_path_liveness.py` | pre-commit; skills-check.yml | check_path_liveness.py — committed-path liveness gate (governance tier). | Mis-scoped: MANIFEST parents only; path literals in docs/lab invisible (FU-19) | TBD |
| `check_pine_manifest.py` | pre-commit; manifest-check.yml | check_pine_manifest.py — verify the strategies/ hash manifests against on-disk Pine. | Aligned (no audit flag at census date) | TBD |
| `check_push_collision.py` | nothing | check_push_collision.py — governance-surface push collision gate (governance tier). | Unwired (floor census) | TBD |
| `check_root_doc_liveness.py` | pre-commit | check_root_doc_liveness.py — root orientation-doc link gate (governance tier). | Resolves markdown links only; dead backtick paths pass (H7) | TBD |
| `check_skill_refs.py` | pre-commit; skills-check.yml | check_skill_refs.py — path-reference linter for `.claude/skills/*/SKILL.md`. | Aligned (no audit flag at census date) | TBD |
| `check_skills_no_constants.py` | pre-commit; skills-check.yml | check_skills_no_constants.py — methodology-skill no-constants guard. | Aligned (no audit flag at census date) | TBD |
| `check_status_consistency.py` | pre-commit; skills-check.yml | check_status_consistency.py — cross-surface study-status gate (governance tier). | Aligned (no audit flag at census date) | TBD |
| `check_supersession_placement.py` | pre-commit | docs/notes/rail_build/*DESK_CARD*.md; lab/analysis/*/RESULTS*.md          (lab/archive/ is LTM — excluded) | Was mis-scoped (flat glob 5/76 RESULTS); repaired FU-5 2026-08-06 | TBD |
| `cost_geometry_pregate.py` | nothing | cost_geometry_pregate.py — instrument-ledger Phase-0 cost-geometry pre-gate. | Unwired (floor census) | TBD |
| `import_skill_from_cache.py` | nothing | import_skill_from_cache.py — ONE-TIME seed of a skill from the deployed bundle. | Unwired (floor census) | TBD |
| `instrument_profiles.py` | pre-commit; skills-check.yml | instrument_profiles.py — mechanism x instrument verdict index (governance tier). | Aligned (no audit flag at census date) | TBD |
| `layer_bootstrap.py` | nothing | Shared direct-script bootstrap for repository layer roots. | Unwired (floor census) | TBD |
| `lock_event_hook.py` | settings.json / docs (grep) | PostToolUse hook — fire verify_lock_anchors.py only on lock-event edits. | Aligned (no audit flag at census date) | TBD |
| `m1_item5_capture.py` | nothing | M1 §4 item 5 capture helper — non-zero admitted-leg dry_run strategy entry. | Unwired (floor census) | TBD |
| `mc_user_guardian.py` | nothing | One-off: run portfolio_mc with the user's Guardian CSV in the Guardian slot, | Unwired (floor census) | TBD |
| `parse_bar_export.py` | nothing | Parse BAR EXPORT v0.1/v0.2 List-of-Trades CSV(s) into core/data/bar_data/<SYMBOL>_M15.csv. | Unwired (floor census) | TBD |
| `pine_check.py` | nothing | pine_check.py - standalone Pine Script compile checker. | Operator-run; unwired from make/pre-commit/CI | TBD |
| `pine_lint.py` | nothing | §2.3 — pine_lint.py: static linter for codification-stage candidate .pine. | Unwired (floor census) | TBD |
| `repo_hygiene.py` | nothing | repo_hygiene.py — report-only git/worktree prune candidates (squash-aware). | Operator-run; unwired | TBD |
| `retire_adr.py` | nothing | retire_adr.py \u2014 ADR lifecycle retire helper. | Operator-run ADR helper; unwired (intentional tool) | TBD |
| `roll_sessions.py` | pre-commit | roll_sessions.py — roll old docs/SESSIONS.md entries into quarterly archives. | Aligned (no audit flag at census date) | TBD |
| `session_divergence_hook.py` | settings.json / docs (grep) | session_divergence_hook.py — SessionStart context injection: how stale is this base? | Aligned (no audit flag at census date) | TBD |
| `sync_pine_to_worktree.py` | nothing | Make the locked Pine source available inside a git worktree. | Unwired (floor census) | TBD |
| `sync_skills.py` | settings.json / docs (grep) | sync_skills.py — one-way deploy of in-repo skills to the deployed bundle. | Aligned (no audit flag at census date) | TBD |
| `sync_skills_hook.py` | settings.json / docs (grep) | PostToolUse hook — deploy in-repo skills to the bundle when a skill file changes. | Aligned (no audit flag at census date) | TBD |
| `validate_c1_monitoring_acceptance.py` | nothing | Validate the M1 monitoring acceptance artifact (secret-free). | Unwired (floor census) | TBD |
| `verify_lock_anchors.py` | settings.json / docs (grep) | verify_lock_anchors.py — surface Closed / Forward / Error routing. | Aligned (no audit flag at census date) | TBD |

## Reproduce floor count

```bash
ls scripts/*.py | wc -l
# R21 snippet in 08-hooks.md §R21
```

Floor unwired count at generation: **16** — `archive_strategy`, `check_advisor_dedup`, `check_brief`, `check_push_collision`, `cost_geometry_pregate`, `import_skill_from_cache`, `layer_bootstrap`, `m1_item5_capture`…
