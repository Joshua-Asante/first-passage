# REPO_MAP — the standing layer map (`core / governance / lab / ops`)

The [boundaries ADR](docs/adr/2026-06-05-monorepo-layer-boundaries.md) owns the design;
[PIPELINES.md](PIPELINES.md) describes handoffs; [STATE.md](STATE.md) carries current
priorities. Removed paths: [lab/ARCHIVED.json](lab/ARCHIVED.json) and
[archive retrieval](docs/ltm/README.md); old migration tables remain in Git history.

## The contract (from ADR §2.2)

```text
governance → core
lab → core + governance
ops → core + governance
core imports nothing from other internal layers
lab ↔ ops is forbidden
```

Same-layer imports are legal; `tests/` is exempt.
`scripts/check_boundaries.py` enforces the contract using the four layer maps in
[`scripts/repo_map_layers.yml`](scripts/repo_map_layers.yml), not this prose; that
file is their only definition, so edit it to change a classification.
`app_layer_prefix` selects core/lab/ops; `governance_prefixes` and the default select
governance; `scripts_layer` supplies the exceptions for root-resident scripts. Parse
failures are reported separately from illegal edges; source must parse on Python 3.11+.

## Mission-tier rubric (P0–P3) — orthogonal to layer

P0 frozen/mission-critical controls; P1 operational safeguards and gates; P2 active
research/support; P3 review candidates. Tiers set review priority, not deletion
permission: apply the [retention test](docs/operational_rules.md#16-retention--an-artifact-must-earn-its-place-and-deletion-is-classified-by-execution-not-by-folder)
to actual consumers before removing an artifact.

## §1 — Moved layers (physically relocated by `git mv`)

Heading kept for existing references; the table shows current ownership, not `git mv` history.

| Layer | Current contents | Entry point |
|---|---|---|
| `core/` | Shared MC engine, ingestion, firm rules, lifecycle, frozen risk controls | [core README](core/README.md), `core/mc/`, `core/firm_rules.py`, `core/dd_protection.py` |
| `core/data/` | Shared private inputs, tracked integrity manifests | [data README](core/data/README.md) |
| `core/strategies/` | Strategy dispositions, parameter mirror, source/port pins; private bodies under `_archive/` | [strategy catalog](core/strategies/CATALOG.md) |
| `lab/analysis/` | Campaign harnesses and evidence at `<theme>/<slug>/` | [lab catalog](lab/CATALOG.md), In flight first |
| `lab/research_utils/` | Shared research primitives | [research utilities](lab/research_utils/README.md) |
| `lab/discovery/`, `lab/databento_fetch/` | Search contracts, scoring, cost-gated data acquisition | [discovery](lab/discovery/README.md), [data client](lab/databento_fetch/README.md) |
| `ops/c1_rail/` | Listener, sizing, payload, telemetry, arm/disarm interfaces; Track B book owner/protection/halt/settlement (`book_*`, `account_close_*`); offline `qualification/` package with its separately installed `execution/` service | [rail README](ops/c1_rail/README.md), `qualification_cli.py` |
| `ops/c1_signal_daemon/` | Python signal-host package | [daemon README](ops/c1_signal_daemon/README.md) |
| `ops/instruments/`, `ops/venue_editions/`, `ops/calendars/` | Instrument evidence, venue binding, calendar records | [ops README](ops/README.md) |
| `ops/sentinel/`, `ops/recall/` | Governance diagnostics, assistive retrieval safeguards | [sentinel](ops/sentinel/README.md), [recall](ops/recall/README.md) |
| `ops/cli.py`, `ops/data/` | Historical tearsheet CLI, reconciliations | [ops README](ops/README.md) |

Governance is a logical layer: `docs/`, `.claude/`, `.github/` and discipline scripts
stay at the root, with no physical `governance/` import root. A catalog entry does
not make private data or frozen bars regenerable.

## §2 — Root-resident (classified, **NOT physically moved** — tooling necessity)

| Paths | Ownership / placement constraint |
|---|---|
| Five root docs, `docs/` | Governance orientation, methodology, evidence navigation |
| `pyproject.toml`, `Makefile`, requirements files | Dependency/build configuration; editable install supplies dependencies, not layer packages |
| `scripts/` | Mixed layers (§2.1); direct scripts resolve repository-relative paths from here |
| `tests/` | Cross-layer integration suite |
| `discovery_manifests/` | Lab search-contract output, anchored at repository root |
| `deploy/` | Fly packaging (root build context) for listener and daemon, with separate definitions and volumes (read their READMEs before operational work), plus `qualification/bootstrap.py`, the isolated-Python role launcher for installed qualification processes. Only static first-party import is `tools/`; `ops` imports are dynamic, outside the scanner |
| `tools/` | Verification tooling: `qualification_verification/` (disposable Linux TEST_ONLY host), `local_verification/` (Docker sequence runner); imports only `scripts/` discipline modules |
| `.claude/`, `.agents/`, `.github/` | Harness, skill and CI entry points at their expected locations |
| `.gitignore`, `.gitattributes`, `LICENSE`, `.markdownlint.json` | VCS, publication and formatting policy |
| `.rgignore` | Search exclusion, sole owner since the 2026-09-15 Cursor retirement; absence in default search is not absence of evidence |
| `.dockerignore` | Root-context allow-list excluding private sources, vendor data, research and Git history from hosted images |

`deploy/` and `tools/` are in `governance_prefixes` (2026-09-20); new Python under
either that statically imports `ops/` or `lab/` needs a different classification in
the same change.

### §2.1 — `scripts/` per-file layer (root-resident; recorded for the scanner)

Generated from `scripts_layer` in
[`repo_map_layers.yml`](scripts/repo_map_layers.yml) (loaded by
`check_boundaries.py` as `SCRIPTS_LAYER`; unlisted files fall back to
**governance** via `layer_of_file()`) and [`gates.yml`](scripts/gates.yml).
Neither the scanner nor [`check_repo_map_layers.py`](scripts/check_repo_map_layers.py)
reads this table. Regenerate with
`python scripts/check_repo_map_scripts_table.py --write`; `--check` exits 1 on drift.

<!-- BEGIN generated: scripts-table -->
_99 tracked `scripts/*.py` files (`git ls-files 'scripts/*.py'`)._

† = layer fallback (not in `scripts_layer`); Gate — = no `gates.yml` command runs the file and no module-run gate triggers on it (it may still run inside another gate's script).

| Script | Layer | Gate id (tier) | Notes |
|---|---|---|---|
| `scripts/_build_lessons_index.py` | governance† | — | — |
| `scripts/_shell_tokens.py` | governance† | — | — |
| `scripts/agent_handoff.py` | governance† | — | — |
| `scripts/archive_lab_analysis.py` | governance | `lab-catalog` (path-conditional) | — |
| `scripts/archive_strategy.py` | governance† | — | — |
| `scripts/audit_notice_grade_k_correction.py` | lab | `notice-grade-k-correction` (audit) | — |
| `scripts/author_book_session_calendar.py` | governance† | — | — |
| `scripts/beta_cohesion_read.py` | lab | — | — |
| `scripts/certification_power.py` | governance† | — | — |
| `scripts/check_adr_graph.py` | governance† | `adr-graph` (path-conditional) | — |
| `scripts/check_advisor_dedup.py` | governance† | — | — |
| `scripts/check_boundaries.py` | governance | `boundaries` (always) | — |
| `scripts/check_brief.py` | governance | — | — |
| `scripts/check_closure_disposition.py` | governance† | `closure-disposition` (path-conditional) | — |
| `scripts/check_cost_model_closed_world.py` | lab | `cost-model-closed-world` (path-conditional) | — |
| `scripts/check_data_manifests.py` | governance | `data-manifests` (data-conditional) | — |
| `scripts/check_docs_runtime_inventory.py` | governance† | `docs-runtime-inventory` (audit) | — |
| `scripts/check_durable_store_pragmas.py` | governance† | `durable-store-pragmas` (path-conditional) | — |
| `scripts/check_falsifier_reachability.py` | governance† | `falsifier-reachability-census` (audit) | --stats (report-only) |
| `scripts/check_governance_prose_control_chars.py` | governance† | `governance-prose-control-chars` (path-conditional) | — |
| `scripts/check_handoff_authority.py` | governance† | `handoff-authority` (path-conditional) | — |
| `scripts/check_handoff_brief_form.py` | governance† | `handoff-brief-form` (path-conditional) | — |
| `scripts/check_instrument_ledger_coverage.py` | governance† | — | — |
| `scripts/check_instrument_rejection_coverage.py` | governance† | `instrument-rejection-coverage` (audit) | WARN, --exit-zero |
| `scripts/check_lab_path_relocation.py` | governance† | — | — |
| `scripts/check_lifecycle_consistency.py` | governance† | `lifecycle-consistency` (path-conditional) | — |
| `scripts/check_md_relative_links.py` | governance† | — | — |
| `scripts/check_path_liveness.py` | governance | `path-liveness` (always) | — |
| `scripts/check_pine_manifest.py` | governance | `pine-manifest` (always); `pine-pin-provenance` (always) | — |
| `scripts/check_pursuit_records.py` | governance† | — | — |
| `scripts/check_push_collision.py` | governance† | — | — |
| `scripts/check_qualification_invariants.py` | governance† | — | — |
| `scripts/check_repo_map_layers.py` | governance† | `repo-map-layers` (path-conditional) | — |
| `scripts/check_repo_map_scripts_table.py` | governance† | `repo-map-scripts-table` (path-conditional) | — |
| `scripts/check_root_doc_liveness.py` | governance† | `root-doc-liveness` (always) | — |
| `scripts/check_rule2_trip_log_liveness.py` | governance† | `rule2-trip-log-liveness` (audit) | --stats (report-only) |
| `scripts/check_sessions_queue_bind.py` | governance† | `sessions-queue-bind` (path-conditional) | — |
| `scripts/check_skill_deploy_sync.py` | governance† | `skill-deploy-sync` (always) | — |
| `scripts/check_skill_refs.py` | governance | `skill-refs` (always) | — |
| `scripts/check_skills_no_constants.py` | governance | `skills-no-constants` (always) | — |
| `scripts/check_spec_provenance.py` | governance† | `spec-provenance` (audit) | --stats (report-only) |
| `scripts/check_staged_debris.py` | governance† | `staged-debris` (always) | — |
| `scripts/check_state_currency.py` | governance† | `state-currency` (always) | — |
| `scripts/check_status_consistency.py` | governance† | `status-consistency` (path-conditional) | — |
| `scripts/check_supersession_placement.py` | governance† | `supersession-placement` (path-conditional) | — |
| `scripts/cost_geometry_pregate.py` | lab | — | — |
| `scripts/diff_econ_calendar.py` | lab | — | — |
| `scripts/docker_verification.py` | governance† | — | — |
| `scripts/event_study_read.py` | lab | — | — |
| `scripts/evidence_archive.py` | governance† | `evidence-archive` (audit) | — |
| `scripts/evidence_store/__init__.py` | governance† | `evidence-store` (path-conditional) | — |
| `scripts/evidence_store/__main__.py` | governance† | `evidence-store` (path-conditional) | — |
| `scripts/evidence_store/audit.py` | governance† | `evidence-store` (path-conditional) | — |
| `scripts/evidence_store/beliefs.py` | governance† | `evidence-store` (path-conditional) | — |
| `scripts/evidence_store/model.py` | governance† | `evidence-store` (path-conditional) | — |
| `scripts/evidence_store/retrieval.py` | governance† | `evidence-store` (path-conditional) | — |
| `scripts/evidence_store/store.py` | governance† | `evidence-store` (path-conditional) | — |
| `scripts/find_owner.py` | governance† | — | — |
| `scripts/fp.py` | governance† | — | — |
| `scripts/gate_fire_log.py` | governance† | — | — |
| `scripts/gate_manifest.py` | governance† | — | gate runner (reads gates.yml); not itself a gated id |
| `scripts/guard_open_verification_record.py` | governance† | — | — |
| `scripts/guard_operator_acts.py` | governance† | — | — |
| `scripts/guard_s2_runs.py` | governance† | — | — |
| `scripts/guard_shell_command.py` | governance† | — | — |
| `scripts/import_skill_from_cache.py` | governance† | — | — |
| `scripts/instrument_profiles.py` | governance† | `instrument-profiles` (path-conditional) | — |
| `scripts/layer_bootstrap.py` | governance† | — | — |
| `scripts/link_policy.py` | governance† | — | — |
| `scripts/lock_event_hook.py` | ops | — | — |
| `scripts/m1_item5_capture.py` | governance† | — | — |
| `scripts/mc_user_guardian.py` | lab | — | — |
| `scripts/parse_bar_export.py` | governance | — | — |
| `scripts/parse_econ_export.py` | lab | — | — |
| `scripts/pine_check.py` | governance | — | — |
| `scripts/pine_lint.py` | lab | — | — |
| `scripts/pytest_junit_subtests.py` | governance† | — | — |
| `scripts/pytest_progress.py` | governance† | — | — |
| `scripts/pytest_qualification_collection.py` | governance† | — | — |
| `scripts/qualification_boundary_environment.py` | governance† | — | — |
| `scripts/qualification_boundary_verification.py` | governance† | — | — |
| `scripts/record_verification.py` | governance† | — | — |
| `scripts/repo_hygiene.py` | governance† | — | — |
| `scripts/repo_retrieve.py` | governance† | — | — |
| `scripts/research_asset_registry.py` | governance† | — | — |
| `scripts/retire_adr.py` | governance† | — | — |
| `scripts/roll_sessions.py` | governance† | `sessions-order` (path-conditional); `sessions-append-only` (path-conditional) | — |
| `scripts/s2_run_evidence.py` | governance† | — | — |
| `scripts/seal_account_snapshot.py` | governance† | — | — |
| `scripts/session_divergence_hook.py` | governance† | — | — |
| `scripts/state_roll.py` | governance† | — | — |
| `scripts/sync_liveness_indexes.py` | governance† | `sync-liveness` (audit) | — |
| `scripts/sync_pine_to_worktree.py` | governance | — | — |
| `scripts/sync_skills.py` | governance | — | — |
| `scripts/sync_skills_hook.py` | governance† | — | — |
| `scripts/track_b_register.py` | governance | `track-b-register` (path-conditional) | — |
| `scripts/validate_bar_export_v2.py` | governance† | — | — |
| `scripts/validate_c1_monitoring_acceptance.py` | governance† | `m1-artifact-structure` (always); `m1-tree-skew` (audit) | --check-tree-skew (report-only) |
| `scripts/verify_lock_anchors.py` | governance | — | — |
<!-- END generated: scripts-table -->

---

### §2.2 — Running a layer module via `python -m` (the PYTHONPATH convention)

Layer roots are import roots: pytest sets them in `pyproject.toml`; standalone
module commands need the root on `PYTHONPATH`. The scanner resolves
repository-qualified imports and the flat roots in `flat_import_roots`
([`scripts/repo_map_layers.yml`](scripts/repo_map_layers.yml)), which mirror pytest
and script bootstraps. Imported submodules resolve to their actual paths, including
mixed-layer scripts; relative imports resolve from their source package under the
same legal edges. Cross-layer name collisions fail with candidate paths; same-layer
duplicates are legal. Unknown external roots are ignored; unresolved imports under
known first-party roots fail. Dynamic imports and filesystem reads are outside the
AST scanner.

| Module / use | Required import root |
|---|---|
| `c1_rail_arm`, other flat listener tools | `ops/c1_rail` (follow the rail runbook for commands) |
| `c1_signal_daemon` package | `ops` |
| `research_utils.deflated_sharpe`, `research_utils.step0_battery`, `research_utils.selection_tests` | `lab` |
| `discovery.register_search` | `lab` |
| `databento_fetch.db_fetch` | `lab`, research dependencies |

Read-only entry-point check — PowerShell:
`$env:PYTHONPATH = "lab"; python -m discovery.register_search --help`; POSIX:
`PYTHONPATH=lab python -m discovery.register_search --help`. Separate multiple roots
with `;` on Windows and `:` on POSIX. Direct scripts may instead use
`scripts/layer_bootstrap.py`; skill wrappers launch subprocesses to preserve the
governance→lab import prohibition.

## §4 — Seam dispositions (settled; ADR §8)

Current seams are in the layer table and enforced maps. Historical Gen-1, CFD,
codification, Notion and migration dispositions are in the
[boundaries ADR](docs/adr/2026-06-05-monorepo-layer-boundaries.md) (§8 for seams
Q-a to Q-e), linked retirement decisions and Git history.

## §5 — Coverage check (zero unmapped)

The heading is historical. These executable checks replace the old manual root-file
exemption regex; together they do not classify every non-Python artifact or certify
that a path may be deleted.

```text
python scripts/check_boundaries.py                       # import boundaries
python scripts/check_repo_map_layers.py                  # layer-map schema
python scripts/check_repo_map_scripts_table.py --check   # §2.1 freshness
```
