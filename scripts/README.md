# `scripts/` — gates and discipline CLIs

## Gate composition and admission

Composition authority is [`gates.yml`](gates.yml) via
[`gate_manifest.py`](gate_manifest.py).
Do not hand-maintain a parallel list.

The manifest's complete tier set is `always`, `path-conditional`,
`data-conditional`, and `audit`. The runner refuses unknown tiers (including the
retired `soft`) and declared/parsed gate-count mismatches, so bad indentation or
an unclaimed tier cannot silently remove a gate.

| Entry point | Selection |
|---|---|
| pre-commit | `always`, plus path/data-conditional gates whose staged-path regex matches |
| `make check` / `--tier check` | All `always` and `path-conditional` gates, plus forced `data-manifests` |
| `make validate` / `--tier validate` | `data-manifests` (forced) and `pine-manifest` only |
| `make audit` / `--tier audit` | `audit` diagnostics only |

[`pre-commit`](githooks/pre-commit), [Make](../Makefile) and the
[CI workflow](../.github/workflows/gate-manifest.yml) call the runner. H6's CI
composition work was discharged on 2026-08-23; CI invokes `--tier check`.
Separate CI checks and the public clone's absent-data handling remain with their
workflows/checkers; composition is not a claim about every merge requirement.

A blocking commit/required-CI gate must protect executable correctness,
non-regenerable evidence, a live-money invariant or the integrity of a changed
artifact; the violating change must select the check; and a finding must return
non-zero and change the verdict. A report-only command belongs in `audit`, however
important its subject. Audit promotion requires a clean baseline, a non-zero
failure mode and a reachable trigger; a gate that becomes report-only moves back
to audit. The original W5 no-gate-dropped landing criterion is completed history,
not a permanent requirement to retain every gate.

Reachability includes every path class that can introduce the violation, including
moving/deleting a referenced target. Matching only the file containing its link
is insufficient. Before a path-conditional re-tier, add the relevant probes to
[`test_path_conditional_gates_are_reachable`](../tests/test_gate_manifest.py).

`m1-artifact-structure` stays blocking (`always`): the
[acceptance validator](validate_c1_monitoring_acceptance.py) rejects unreadable or
invalid artifacts, missing required fields, invalid status and secret violations.
`m1-tree-skew` uses `--check-tree-skew` as a report-only audit; ordinary deployed
versus main drift does not fail a commit. Neither check substitutes for arm-time
validation or grants permission. The [M1 owner](../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md)
and [arm implementation](../ops/c1_rail/c1_rail_arm.py) govern the separate execution
boundary, including the recorded attended-override path for a structurally valid
unresolved artifact; invalid/forged artifacts cannot use that path. The
[item-5 test-strategy license](../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24)
does not grant arm authority.

```text
python scripts/gate_manifest.py --list
python scripts/gate_manifest.py --list --all-tiers
make check          # same runner, check tier
make audit          # report-only diagnostics
make validate       # data manifests + pine
```

Install hooks once per clone: `bash scripts/install_hooks.sh`.

Per-script layer classification is owned by
`check_boundaries.py`'s `SCRIPTS_LAYER` (fallback **governance**). The
human-readable table in [`REPO_MAP.md`](../REPO_MAP.md) §2.1 is generated
from that dict + [`gates.yml`](gates.yml) + `git ls-files 'scripts/*.py'`:

```text
python scripts/check_repo_map_scripts_table.py --write
python scripts/check_repo_map_scripts_table.py --check
```

Do not hand-edit the table. `--check` is not wired into `gates.yml`.

## Skill lifecycle

Project-authored skills are canonical in [`.claude/skills/`](../.claude/skills/).
Edit that source, run the applicable gates, then deploy repository → bundle with
[`sync_skills.py`](sync_skills.py). Its default destinations are the resolved
primary bundle and `~/.claude/skills/`; an explicit `--target` selects only that
destination. `--check` reports missing, differing and extra deployed content without
writing. Cloud sync can overwrite the primary bundle, so this check does not prove
the external sync layer enforces repository ownership.

[`gates.yml`](gates.yml) owns composition. `skill-refs` and `skills-no-constants`
are `always` gates. [`check_skill_refs.py`](check_skill_refs.py) checks eligible
repository references; its documented template/vendor/local-path exceptions apply.
[`check_skills_no_constants.py`](check_skills_no_constants.py) scans only the
`SKILL.md` of `inqhiori`, `ooda-loop`, `programme-audit` and `brief-authoring`.
Operational-reference skills and `pinescript-v6` are exempt. Guarded skills point
to operational sources instead of restating their constants.

The [PostToolUse hook](sync_skills_hook.py), registered in
[settings](../.claude/settings.json), checks references before deploying. A missing
or failing reference checker prevents deployment; a sync failure is surfaced.
The hook does not run the no-constants guard; that check remains in the commit
battery. Both sync and hook recognize `.claude/worktrees/`, but currently miss
`.worktrees/`. Do not deploy from a worktree: deployment follows integration in
the primary checkout.

[`import_skill_from_cache.py`](import_skill_from_cache.py) is a missing-source
recovery exception: it copies one named skill byte-for-byte only when the repository
destination is absent and the source contains `SKILL.md`. It refuses an existing
destination, with no overwrite option. After import, repository ownership and the
gates apply. This is not a reverse-sync lane. Deployed-only extras require triage;
stock exemptions are explicit in the implementation.

[`check_skill_deploy_sync.py`](check_skill_deploy_sync.py) checks existence of
literal ADR-cited deployed scripts, not byte equality: absent deployment root means
`SKIP` / `NOT CHECKED`; an existing root missing a cited script fails. The drift
check covers content differences.

The June 4 quarterly keeper-count/old-name reread is **retired on 2026-09-08**, not
passed. Its fixed “10 skills” census is obsolete; live gates and broken-reference /
restated-constant failure tests remain. The [removed decision](../docs/adr/TOMBSTONES.md#2026-09-08-brief-and-skill-governance)
preserves the migration history, including the superseded three-skill plan.

## Validation maintenance

### Brief checker ownership

The [brief-authoring skill](../.claude/skills/brief-authoring/SKILL.md#checker-ownership)
owns the canonical checker source, type contracts and repo-subset limits. Follow
the artifact's verification contract; a `NOT CHECKED` or delegation notice is not
a full validation pass. Checker/template unification remains unresolved and is
not commissioned here. Neither brief checker is in the gate manifest.

The separate unresolved 26-letter session-label ceiling remains with the
[SESSIONS header](../docs/SESSIONS.md) and [`roll_sessions.py`](roll_sessions.py).

## Independent review

[The pre-ratification workflow](../.claude/workflows/pre-ratification-adversarial-panel.js)
owns its review mechanics. Reviewers assess the source independently of the proposer's
reasoning; synthesis is advisory and cannot supply operator ratification or execution
authority. Reviewer/delegate assignment never grants permission to edit locked surfaces.

Its existing GRAND-only safety scan reads committed target text. A safety-invariant
citation flags a hard block on synthesis; missing text flags a coverage failure, also
blocked. Keep its fail-closed, deliberately sensitive behavior; STRATEGIC calls do not
gain this scan. The implementation owns the matching rules. This review check does not
replace [M1 acceptance validation](validate_c1_monitoring_acceptance.py), live execution
authorization, or the [production protection checks](../core/dd_protection.py).

Risk/sizing, validation, gate composition, brief compliance, research dedup and operational
oversight remain with their existing code/skill/rule owners. Removing a review mechanism
does not weaken those controls or commission new reviewer roles. New functions need
demonstrated coverage; do not assume every judgment can be reduced to a mechanical check.
