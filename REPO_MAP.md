# REPO_MAP — the standing layer map (`core / governance / lab / ops`)

Present path ownership and import rules. [PIPELINES.md](PIPELINES.md) describes
handoffs; [STATE.md](STATE.md) carries current priorities. The
[boundaries ADR](docs/adr/2026-06-05-monorepo-layer-boundaries.md) owns the design.

`scripts/check_boundaries.py` enforces its Python maps, not this prose.
`scripts/repo_map_layers.yml` mirrors those maps and
`scripts/check_repo_map_layers.py` checks equality; update both in one change.
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
| `ops/c1_rail/` | Listener, sizing, payload, telemetry, arm/disarm interfaces | [rail README](ops/c1_rail/README.md) |
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
| `deploy/` | Ops packaging for listener and daemon, using root build context; no Python files currently |
| `.claude/`, `.cursor/`, `.agents/`, `.github/` | Harness, editor, skill and CI entry points at their expected locations |
| `.gitignore`, `.gitattributes`, `LICENSE`, `.markdownlint.json` | VCS, publication and formatting policy |
| `.rgignore`, `.cursorignore`, `.cursorindexingignore` | Search/index exclusions; absence in default search is not absence of evidence |
| `.dockerignore` | Root-context allow-list excluding private sources, vendor data, research and Git history from hosted images |

The listener and daemon have separate deployment definitions and volumes under
`deploy/`; see their READMEs before operational work. Adding Python beneath
`deploy/` requires explicitly classifying it in the boundary maps in the same
change: the scanner's default is governance.

### §2.1 — `scripts/` per-file layer (root-resident; recorded for the scanner)

`scripts/` stays at root but its files are classified. Layer comes from
`check_boundaries.py`'s `SCRIPTS_LAYER`; anything not in that dict falls back
to **governance** via `layer_of_file()`. The scanner does **not** load this
table. The P5 gate ([`check_repo_map_layers.py`](scripts/check_repo_map_layers.py))
compares `SCRIPTS_LAYER` to [`repo_map_layers.yml`](scripts/repo_map_layers.yml),
not this table. Gate composition is owned by [`gates.yml`](scripts/gates.yml)
and is not changed by regenerating this section.

Regenerate: `python scripts/check_repo_map_scripts_table.py --write`.
`--check` exits 1 on drift; it is **not** wired into `gates.yml`.

<!-- BEGIN generated: scripts-table -->
_66 tracked `scripts/*.py` files (`git ls-files 'scripts/*.py'`)._

| Script | Layer | Gate id (tier) | Notes |
|---|---|---|---|
| `scripts/_build_lessons_index.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/archive_lab_analysis.py` | governance | `lab-catalog` (path-conditional) | — |
| `scripts/archive_strategy.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/audit_notice_grade_k_correction.py` | lab | `notice-grade-k-correction` (audit) | — |
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
| `scripts/check_falsifier_reachability.py` | governance | `falsifier-reachability-census` (audit) | --stats (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_governance_prose_control_chars.py` | governance | `governance-prose-control-chars` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_instrument_ledger_coverage.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_instrument_rejection_coverage.py` | governance | `instrument-rejection-coverage` (audit) | WARN, --exit-zero; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_lab_path_relocation.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_lifecycle_consistency.py` | governance | `lifecycle-consistency` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_md_relative_links.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_path_liveness.py` | governance | `path-liveness` (always) | — |
| `scripts/check_pine_manifest.py` | governance | `pine-manifest` (always); `pine-pin-provenance` (always) | — |
| `scripts/check_pursuit_records.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_push_collision.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_repo_map_layers.py` | governance | `repo-map-layers` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_repo_map_scripts_table.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_root_doc_liveness.py` | governance | `root-doc-liveness` (always) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_rule2_trip_log_liveness.py` | governance | `rule2-trip-log-liveness` (audit) | --stats (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_sessions_queue_bind.py` | governance | `sessions-queue-bind` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_skill_deploy_sync.py` | governance | `skill-deploy-sync` (always) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_skill_refs.py` | governance | `skill-refs` (always) | — |
| `scripts/check_skills_no_constants.py` | governance | `skills-no-constants` (always) | — |
| `scripts/check_spec_provenance.py` | governance | `spec-provenance` (audit) | --stats (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_state_currency.py` | governance | `state-currency` (always) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_status_consistency.py` | governance | `status-consistency` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_supersession_placement.py` | governance | `supersession-placement` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/cost_geometry_pregate.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/diff_econ_calendar.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/event_study_read.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/find_owner.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/gate_fire_log.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/gate_manifest.py` | governance | — | gate runner (reads gates.yml); not itself a gated id; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/import_skill_from_cache.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/instrument_profiles.py` | governance | `instrument-profiles` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/layer_bootstrap.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/lock_event_hook.py` | ops | — | manual/local only, not in gates.yml |
| `scripts/m1_item5_capture.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/mc_user_guardian.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/parse_bar_export.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/parse_econ_export.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/pine_check.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/pine_lint.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/repo_hygiene.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/repo_retrieve.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/research_asset_registry.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/retire_adr.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/roll_sessions.py` | governance | `sessions-order` (path-conditional); `sessions-append-only` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/session_divergence_hook.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
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
script bootstraps; `FLAT_IMPORT_ROOTS` in `scripts/check_boundaries.py` is checked
against `scripts/repo_map_layers.yml`. Imported submodules are resolved to their
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

Application prefixes select core/lab/ops. Governance prefixes and the default
select governance; `SCRIPTS_LAYER` supplies exceptions for root-resident scripts.
`tests/` is exempt. Read the actual Python maps and their YAML mirror before
changing classification; the generated table above is a view, not scanner input.

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

These check Python boundaries, equality of the enforced maps and their YAML
mirror, and freshness of the script inventory respectively. They do not classify
every non-Python artifact or certify that a path may be deleted.
