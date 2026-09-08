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

## Validation maintenance

Brief-checker/template unification remains unresolved and is not commissioned by
this consolidation. [`scripts/check_brief.py`](check_brief.py) is a subset checker;
the [skill-side checker](../.claude/skills/brief-authoring/scripts/check_brief.py)
owns the fuller type-aware contract, including concise ADR shape. Follow each
artifact's current template; do not treat a subset result as full validation.
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
