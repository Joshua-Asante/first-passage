# REPO_MAP — the standing layer map (`core / governance / lab / ops`)

Present path ownership and import rules. [PIPELINES.md](PIPELINES.md) describes
handoffs; [STATE.md](STATE.md) carries current priorities. The
[boundaries ADR](docs/adr/2026-06-05-monorepo-layer-boundaries.md) owns the design.

`scripts/check_boundaries.py` enforces the layer maps it loads from
`scripts/repo_map_layers.yml` — the single definition — not this prose;
`scripts/check_repo_map_layers.py` validates that file's schema.
For removed paths, use [lab/ARCHIVED.json](lab/ARCHIVED.json) and
[archive retrieval](docs/ltm/README.md). Old migration tables remain in Git history.

## The contract (from ADR §2.2)

```text
governance → core
lab → core + governance
ops → core + governance
core imports nothing from other internal layers
lab ↔ ops is forbidden
```

Same-layer imports are legal. Tests are exempt so they can exercise integrations.
The scanner also checks cross-layer module-name uniqueness and reports parse
failures separately from illegal edges. Source must parse on Python 3.11+.

## Mission-tier rubric (P0–P3) — orthogonal to layer

P0 marks frozen/mission-critical controls; P1 operational safeguards and gates;
P2 active research/support; P3 candidates for review. These are review priorities,
not deletion permissions. Apply the [retention test](docs/operational_rules.md#16-retention--an-artifact-must-earn-its-place-and-deletion-is-classified-by-execution-not-by-folder)
to actual consumers before removing an artifact.

## §1 — Moved layers (physically relocated by `git mv`)

The heading is retained for existing references; the table describes current ownership.

| Layer | Current contents | Entry point |
|---|---|---|
| `core/` | Shared MC engine, ingestion, firm rules, lifecycle and frozen risk controls | [core README](core/README.md), `core/mc/`, `core/firm_rules.py`, `core/dd_protection.py` |
| `core/data/` | Shared private inputs and tracked integrity manifests | [data README](core/data/README.md) |
| `core/strategies/` | Strategy dispositions, parameter mirror, source/port pins; private bodies under `_archive/` | [strategy catalog](core/strategies/CATALOG.md) |
| `lab/analysis/` | Campaign harnesses and evidence at `<theme>/<slug>/` | [lab catalog](lab/CATALOG.md), In flight first |
| `lab/research_utils/` | Shared research primitives | [research utilities](lab/research_utils/README.md) |
| `lab/discovery/`, `lab/databento_fetch/` | Search contracts, scoring and cost-gated data acquisition | [discovery](lab/discovery/README.md), [data client](lab/databento_fetch/README.md) |
| `ops/c1_rail/` | Listener, sizing, payload, telemetry, arm/disarm interfaces; Track B book owner/protection/halt/settlement modules (`book_*`, `account_close_*`); offline qualification package `qualification/` with its separately installed `execution/` service | [rail README](ops/c1_rail/README.md), `qualification_cli.py` |
| `ops/c1_signal_daemon/` | Python signal-host package | [daemon README](ops/c1_signal_daemon/README.md) |
| `ops/instruments/`, `ops/venue_editions/`, `ops/calendars/` | Instrument evidence, venue binding and calendar records | [ops README](ops/README.md) |
| `ops/sentinel/`, `ops/recall/` | Governance diagnostics and assistive retrieval safeguards | [sentinel](ops/sentinel/README.md), [recall](ops/recall/README.md) |
| `ops/cli.py`, `ops/data/` | Historical tearsheet CLI and reconciliations | [ops README](ops/README.md) |

Governance is a logical layer: `docs/`, `.claude/`, `.github/`, and discipline
scripts remain at the root. There is no physical `governance/` import root.
Private data and frozen bars are not regenerable merely because a catalog entry exists.

## §2 — Root-resident (classified, **NOT physically moved** — tooling necessity)

| Paths | Ownership / placement constraint |
|---|---|
| Five root docs, `docs/` | Governance orientation, methodology and evidence navigation |
| `pyproject.toml`, `Makefile`, requirements files | Dependency/build configuration; editable install supplies dependencies, not layer packages |
| `scripts/` | Mixed layers, listed below; direct scripts resolve repository-relative paths from this location |
| `tests/` | Cross-layer integration suite, exempt from application import boundaries |
| `discovery_manifests/` | Lab search-contract output, anchored at repository root |
| `deploy/` | Fly packaging for listener and daemon (root build context) plus `qualification/bootstrap.py`, the isolated-Python role launcher for installed qualification processes; classified governance in the layer map — its only static first-party import is `tools/`, its `ops` imports are dynamic and outside the scanner |
| `tools/` | Verification tooling: `qualification_verification/` (disposable Linux TEST_ONLY host) and `local_verification/` (Docker sequence runner); classified governance in the layer map, imports `scripts/` discipline modules only |
| `.claude/`, `.agents/`, `.github/` | Harness, skill and CI entry points at their expected locations |
| `.gitignore`, `.gitattributes`, `LICENSE`, `.markdownlint.json` | VCS, publication and formatting policy |
| `.rgignore` | Search exclusion, sole owner since the 2026-09-15 Cursor retirement; absence in default search is not absence of evidence |
| `.dockerignore` | Root-context allow-list excluding private sources, vendor data, research and Git history from hosted images |

The listener and daemon have separate deployment definitions and volumes under
`deploy/`; see their READMEs before operational work. `deploy/` and `tools/` are
listed in `governance_prefixes` (2026-09-20); Python added beneath either that
statically imports `ops/` or `lab/` needs a different classification in the
same change, since governance may import only `core/`.

### §2.1 — `scripts/` per-file layer (root-resident; recorded for the scanner)

`scripts/` stays at root but its files are classified. Layer comes from
`scripts_layer` in [`repo_map_layers.yml`](scripts/repo_map_layers.yml) — the
single definition `check_boundaries.py` loads as `SCRIPTS_LAYER`; anything not
listed there falls back to **governance** via `layer_of_file()`. The scanner
does **not** load this table. The layer gate
([`check_repo_map_layers.py`](scripts/check_repo_map_layers.py)) validates that
file's schema, not this table. Gate composition is owned by
[`gates.yml`](scripts/gates.yml) and is not changed by regenerating this section.

Regenerate: `python scripts/check_repo_map_scripts_table.py --write`.
`--check` exits 1 on drift; it is **not** wired into `gates.yml`.

<!-- BEGIN generated: scripts-table -->
_97 tracked `scripts/*.py` files (`git ls-files 'scripts/*.py'`)._

| Script | Layer | Gate id (tier) | Notes |
|---|---|---|---|
| `scripts/_build_lessons_index.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/_shell_tokens.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/agent_handoff.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/archive_lab_analysis.py` | governance | `lab-catalog` (path-conditional) | — |
| `scripts/archive_strategy.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/audit_notice_grade_k_correction.py` | lab | `notice-grade-k-correction` (audit) | — |
| `scripts/author_book_session_calendar.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/beta_cohesion_read.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/certification_power.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_adr_graph.py` | governance | `adr-graph` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_advisor_dedup.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_boundaries.py` | governance | `boundaries` (always) | — |
| `scripts/check_brief.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/check_closure_disposition.py` | governance | `closure-disposition` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_cost_model_closed_world.py` | lab | `cost-model-closed-world` (path-conditional) | — |
| `scripts/check_data_manifests.py` | governance | `data-manifests` (data-conditional) | — |
| `scripts/check_docs_runtime_inventory.py` | governance | `docs-runtime-inventory` (audit) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_durable_store_pragmas.py` | governance | `durable-store-pragmas` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_falsifier_reachability.py` | governance | `falsifier-reachability-census` (audit) | --stats (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_governance_prose_control_chars.py` | governance | `governance-prose-control-chars` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_handoff_authority.py` | governance | `handoff-authority` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_instrument_ledger_coverage.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_instrument_rejection_coverage.py` | governance | `instrument-rejection-coverage` (audit) | WARN, --exit-zero; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_lab_path_relocation.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_lifecycle_consistency.py` | governance | `lifecycle-consistency` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_md_relative_links.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_path_liveness.py` | governance | `path-liveness` (always) | — |
| `scripts/check_pine_manifest.py` | governance | `pine-manifest` (always); `pine-pin-provenance` (always) | — |
| `scripts/check_pursuit_records.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_push_collision.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_qualification_invariants.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_repo_map_layers.py` | governance | `repo-map-layers` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_repo_map_scripts_table.py` | governance | `repo-map-scripts-table` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_root_doc_liveness.py` | governance | `root-doc-liveness` (always) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_rule2_trip_log_liveness.py` | governance | `rule2-trip-log-liveness` (audit) | --stats (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_sessions_queue_bind.py` | governance | `sessions-queue-bind` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_skill_deploy_sync.py` | governance | `skill-deploy-sync` (always) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_skill_refs.py` | governance | `skill-refs` (always) | — |
| `scripts/check_skills_no_constants.py` | governance | `skills-no-constants` (always) | — |
| `scripts/check_spec_provenance.py` | governance | `spec-provenance` (audit) | --stats (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_staged_debris.py` | governance | `staged-debris` (always) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_state_currency.py` | governance | `state-currency` (always) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_status_consistency.py` | governance | `status-consistency` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_supersession_placement.py` | governance | `supersession-placement` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/cost_geometry_pregate.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/diff_econ_calendar.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/docker_verification.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/event_study_read.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/evidence_archive.py` | governance | `evidence-archive` (audit) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/evidence_store/__init__.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/evidence_store/__main__.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/evidence_store/audit.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/evidence_store/beliefs.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/evidence_store/model.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/evidence_store/retrieval.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/evidence_store/store.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/find_owner.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/fp.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/gate_fire_log.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/gate_manifest.py` | governance | — | gate runner (reads gates.yml); not itself a gated id; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/guard_open_verification_record.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/guard_operator_acts.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/guard_s2_runs.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/guard_shell_command.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/import_skill_from_cache.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/instrument_profiles.py` | governance | `instrument-profiles` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/layer_bootstrap.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/link_policy.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/lock_event_hook.py` | ops | — | manual/local only, not in gates.yml |
| `scripts/m1_item5_capture.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/mc_user_guardian.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/parse_bar_export.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/parse_econ_export.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/pine_check.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/pine_lint.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/pytest_junit_subtests.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/pytest_progress.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/pytest_qualification_collection.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/qualification_boundary_environment.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/qualification_boundary_verification.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/record_verification.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/repo_hygiene.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/repo_retrieve.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/research_asset_registry.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/retire_adr.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/roll_sessions.py` | governance | `sessions-order` (path-conditional); `sessions-append-only` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/s2_run_evidence.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/seal_account_snapshot.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/session_divergence_hook.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/state_roll.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/sync_liveness_indexes.py` | governance | `sync-liveness` (audit) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/sync_pine_to_worktree.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/sync_skills.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/sync_skills_hook.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/validate_bar_export_v2.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/validate_c1_monitoring_acceptance.py` | governance | `m1-artifact-structure` (always); `m1-tree-skew` (audit) | --check-tree-skew (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/verify_lock_anchors.py` | governance | — | manual/local only, not in gates.yml |
<!-- END generated: scripts-table -->

---


### §2.2 — Running a layer module via `python -m` (the PYTHONPATH convention)

Layer roots are import roots. Pytest configures them in `pyproject.toml`;
standalone module commands need the relevant root on `PYTHONPATH`.

The import-boundary scanner resolves repository-qualified imports and the flat
roots `core`, `lab`, `ops`, `ops/c1_rail`, `ops/c1_signal_daemon`, and `scripts`
(the latter supports direct script execution). These roots mirror pytest and
script bootstraps; `flat_import_roots` in `scripts/repo_map_layers.yml` is the
definition `scripts/check_boundaries.py` loads. Imported submodules are resolved to their
actual paths, including mixed-layer scripts. Cross-layer name collisions fail
with candidate paths; same-layer duplicates remain legal. Unknown external
roots are ignored, while unresolved imports under known first-party roots fail.
Relative imports resolve from their source package and use the same legal edges.
Dynamic imports and filesystem reads remain outside the AST scanner's coverage.

| Module / use | Required import root |
|---|---|
| `c1_rail_arm`, other flat listener tools | `ops/c1_rail` (follow the rail runbook for commands) |
| `c1_signal_daemon` package | `ops` |
| `research_utils.deflated_sharpe`, `research_utils.step0_battery`, `research_utils.selection_tests` | `lab` |
| `discovery.register_search` | `lab` |
| `databento_fetch.db_fetch` | `lab`, research dependencies |

For a read-only entry-point check:

```powershell
$env:PYTHONPATH = "lab"
python -m discovery.register_search --help
```

POSIX equivalent: `PYTHONPATH=lab python -m discovery.register_search --help`.
Multiple roots use `;` on Windows and `:` on POSIX. Direct scripts may instead
use `scripts/layer_bootstrap.py`; skill wrappers launch subprocesses to preserve
the governance→lab import prohibition.

## §3 — How `check_boundaries.py` resolves a file's layer

Application prefixes select core/lab/ops. Governance prefixes (`docs/`, `.claude/`,
`.github/`, `deploy/`, `tools/`) and the default select governance; `scripts_layer`
supplies exceptions for root-resident scripts.
`tests/` is exempt. All four maps are read from `scripts/repo_map_layers.yml` at
import; edit that file to change a classification. The generated table above is
a view, not scanner input.

## §4 — Seam dispositions (settled; ADR §8)

Current seams are represented in the layer table and enforced maps. Historical
Gen-1, CFD, codification, Notion and migration dispositions remain in the
[boundaries ADR](docs/adr/2026-06-05-monorepo-layer-boundaries.md), linked retirement
decisions, and Git history. This section preserves the old navigation anchor.

## §5 — Coverage check (zero unmapped)

The heading is historical; use current executable checks instead of a manually
maintained root-file exemption regex:

```text
python scripts/check_boundaries.py
python scripts/check_repo_map_layers.py
python scripts/check_repo_map_scripts_table.py --check
```

These check Python boundaries, the layer-map file's schema, and freshness of
the script inventory respectively. They do not classify
every non-Python artifact or certify that a path may be deleted.
