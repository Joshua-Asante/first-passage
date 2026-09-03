# REPO_MAP — the standing layer map (`core / governance / lab / ops`)

> **Status:** authoritative path→layer partition for the monorepo-boundaries restructure (ADR `docs/adr/2026-06-05-monorepo-layer-boundaries.md`, ACCEPTED 2026-06-05). Human-readable map for operators. The scanner (`scripts/check_boundaries.py`) **never opens this file** — it hard-codes `APP_LAYER_PREFIX` / `GOVERNANCE_PREFIXES` / `SCRIPTS_LAYER`. Those three maps are mirrored in [`scripts/repo_map_layers.yml`](scripts/repo_map_layers.yml) and compared by [`scripts/check_repo_map_layers.py`](scripts/check_repo_map_layers.py) (P5). Edit the Python dicts and the YAML together. This file is **NOT** a deletion feed (the deletion instrument was retired on main, `a9d16d0`).
> **Authored:** Phase C, Step C2 (before the move), so the partition is written-then-executed, not inferred.
> **Coverage rule:** every `git ls-files` path resolves to exactly one layer via the rules below. Zero unmapped (verified — see §Coverage check).
> **(pruned)** below = deleted at the 2026-08-08 Great Prune; retrieve with `git show pre-prune-2026-08-08:<path>` using the path cited just before the tag. **(public-seed omitted)** = present in the private archive, absent on this public clone; same retrieval command.

```yaml
# MACHINE BLOCK POINTER (do not paste free prose here — edit scripts/repo_map_layers.yml)
# compared by: python scripts/check_repo_map_layers.py
```

---

## The contract (from ADR §2.2)

```text
governance ──▶ core ;  lab ──▶ core (+governance) ;  ops ──▶ core (+governance)
core imports NOTHING internal.   lab ↔ ops : FORBIDDEN (the load-bearing invariant).
```

`check_boundaries.py` maps each `*.py` to its layer (by the rules below), asserts no import crosses an illegal edge, and asserts cross-layer module-name uniqueness. `tests/` and root-resident tooling are exempt (see §Root-resident). **Gate floor is Python 3.11** (`pyproject.toml` `requires-python`, CI `tests.yml` matrix, `.venv-research`) — sources must AST-parse under that floor; a parse failure is reported as `UNPARSEABLE`, distinct from an `ILLEGAL` edge (ADR H1).

## Mission-tier rubric (P0–P3) — orthogonal to layer

| Tier | Meaning | Typical action if flagged |
|---|---|---|
| **P0** | Locked / mission-critical: production risk controls + locked strategy source-of-truth. Never delete; change only via the lock cycle. | none — protect |
| **P1** | Operational / load-bearing: live-ops surface + governance gates. | repair, don't drop |
| **P2** | Active research / supporting: in-flight harnesses, active briefs, methodology. | keep while active |
| **P3** | Candidate-for-review: low-coupling, possibly prunable in a future sweep. | review on a future pass |

---

## §1 — Moved layers (physically relocated by `git mv`)

### `core/` — locked sink (imports nothing internal). Tier P0.

| New path | From |
|---|---|
| `core/portfolio_mc.py` | `portfolio_mc.py` |
| `core/dd_protection.py` | `dd_protection.py` |
| `core/firm_rules.py` | `firm_rules.py` |
| `core/csv_parser.py` | `csv_parser.py` |
| `core/tv_export_loader.py` | `analysis/oanda_stage1/tv_export_loader.py` (**widened**, ADR §8 Q-d) |
| `core/lib/` | `lib/` |
| ~~`core/config/`~~ | `config/` (data-only; imported by nothing) — **RETIRED 2026-08-03** with `params.toml` hub gates ([`docs/adr/2026-08-03-params-toml-gate-retirement.md`](docs/adr/2026-08-03-params-toml-gate-retirement.md)); retrieve via git history |
| `core/strategies/` | `strategies/` **minus `codification/`** — hot tree = [`CATALOG.md`](core/strategies/CATALOG.md) + `*_CARD.md` stubs; Pine + full LOCK/CHANGELOG/CANDIDATE bodies under `_archive/<family>/`; `MANIFEST.sha256` / `PORT_MANIFEST.sha256` pin archive paths |
| `core/data/tv_exports/` `core/data/bar_data/` `core/data/external/` | `data/tv_exports/` `data/bar_data/` `data/external/` (backtest panels — immutable shared inputs). Live trade-lists: `tv_exports/cme/`. `bar_data/` = **frozen CME micros only** (`6J`/`MNQ`/`MYM_M15`; producer dead since Pepperstone retirement). Dukascopy / OANDA deleted Phase 5 (`docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md`, pruned); CFD-era `bar_data` + `tv_exports/candidates/` deleted 2026-08-03 ([ADR](docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md), `docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md` pruned) |

### `lab/` — free-churn research (imports core+governance). Tier P2/P3.

| New path | From |
|---|---|
| `lab/analysis/` | `analysis/` **minus `oanda_stage1/tv_export_loader.py`** (→core). Dated campaign evidence. **STM layout (2026-08-03):** nested hot bodies at `lab/analysis/<theme>/<slug>/`; flat CARD stubs at `lab/analysis/<slug>/CARD.md`; cold bodies at `lab/archive/<slug>/` — open [`lab/CATALOG.md`](lab/CATALOG.md) first. **NON-RUNNABLE Gen-1 leftovers** (still `import validation.*`; CI `--ignore`): `legacy/guardian_parity_2026-06-23/`, `legacy/usoil_regime_capture/` — plus `gbpusd_rank_cert/`, whose runnable body now lives at **`lab/archive/gbpusd_rank_cert/`** (flat `CARD.md` stub only under `lab/analysis/`, so the CI `--ignore` for the old flat path is a no-op). Keep as evidence; do not re-run without restore-from-git of retired Gen-1 or a re-point ADR. |
| `lab/archive/` | cold bodies for archived `lab/analysis/<slug>/` studies (STM/LTM; hot stubs remain at `lab/analysis/<slug>/CARD.md`) |
| `lab/CATALOG.md` | generated index — open first for lab decisions (`make lab-catalog` / `scripts/archive_lab_analysis.py --regenerate-catalog`; freshness gated by `make lab-catalog-check` / pre-commit `--check --catalog-only`) |
| `lab/validation/` | `validation/` — **retired 2026-07-11**, see [`docs/adr/2026-07-11-gen1-pipeline-retirement.md`](docs/adr/2026-07-11-gen1-pipeline-retirement.md); row kept for move-provenance history |
| `lab/validation_selftest.py` | extracted from `validation/controls.py` (Gen-1 self-test generators; DSR gate wired 2026-07-11 — `tests/test_validation_selftest_dsr_gate.py`; full §8 universe-gate `--self-test` wired 2026-07-12 — `research_utils/universe_gate.py`) |
| `lab/research_utils/` | stable research primitives: permutation + Gen-2 DSR / step0 / selection / plateau (relocated from `.claude/skills/strategy-validation/scripts/` 2026-07-11; design: `docs/superpowers/specs/2026-07-11-lab-research-stack-relocation-design.md`, public-seed omitted) + `universe_gate.py`. **W4 2026-08-07:** SPA/StepM/PBO **dormant** (named re-arm); plateau **archived**; breadth **tombstoned** as live producer — [`W4 ADR`](docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md) |
| `lab/discovery/` | Gen-2 K-ledger (`register_search.py`); canonical home as of 2026-07-11 relocation |
| `lab/databento_fetch/` | Gen-2 cost-gated Databento client (`db_fetch.py`); canonical home as of 2026-07-11 relocation |
| `lab/codification/` | `strategies/codification/` — **RETIRED 2026-08-02** (operator ruling #3 / prune Packet D; was parked ADR 2026-07-11; retrieve via git history; future bridge = fresh build) |

### `ops/` — operational (imports core+governance). Tier P1.

| New path | From |
|---|---|
| ~~`ops/accounts.py`~~ `ops/cli.py` | `accounts.py` retired substrate Phase 2 (multiplier spine); `cli.py` retained as **tearsheet-only** historical entry point. FXIFY-challenge path excised 2026-07-11 per [`docs/adr/2026-07-11-fxify-ops-surface-retirement.md`](docs/adr/2026-07-11-fxify-ops-surface-retirement.md); full spine delete [`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`](docs/adr/2026-07-22-challenge-era-substrate-retirement.md) §2-D |
| ~~`ops/fxify_rule_validator.py`~~ ~~`ops/parity_check.py`~~ ~~`ops/tv_mt5_pnl_reconciliation.py`~~ | root — `fxify_rule_validator.py` + `tv_mt5_pnl_reconciliation.py` **retired 2026-07-11** per [`docs/adr/2026-07-11-fxify-ops-surface-retirement.md`](docs/adr/2026-07-11-fxify-ops-surface-retirement.md); `parity_check.py` **retired 2026-07-11** per [`docs/adr/2026-07-11-ops-cfd-estate-retirement.md`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md); rows kept for move-provenance |
| `ops/live_journal/` — **retired in full 2026-07-11** per [`docs/adr/2026-07-11-ops-cfd-estate-retirement.md`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md) (the reconcile-subsystem disposition the fxify-ops-surface ADR deferred/parked); `references/execution_lessons.md` relocated to `docs/methodology/lessons/` (not lost); row kept for move-provenance history | `live_journal/` (incl. canonical `journal_review.py`) |
| `ops/weekly_review_feeder/` | `weekly_review_feeder/` — **retired 2026-07-06**, see `docs/ltm/briefs/2026-07-06-weekly-review-feeder-retirement.md` (pruned); row kept for move-provenance history |
| `ops/mc_runs/` — retired 2026-07-11 (empty orphan output dir; same ADR) | `mc_runs/` (transient MC state) |
| ~~`ops/reports/`~~ — deleted 2026-08-03; sole survivor `regime_time_cost/RESULTS.md` relocated to `lab/analysis/regime/regime_time_cost_2026-06-09/` (Q-PERSIST-1 gating read); `ecr/` + `corpus_fdr/` already retired 2026-07-11 | `reports/` (ECR output dir) |
| `ops/data/reconciles/` · ~~`ops/data/audits/`~~ — audits deleted 2026-08-03; `issue_54_ulp_audit.*` relocated to `docs/notes/audits/` | `data/audits/` `data/reconciles/` (former gitignored `accounts.json` retired with multiplier spine, substrate Phase 2) |
| `ops/c1_rail/` | Flat `ops/c1_*.py` + `ops/crosstrade_payload.py` **relocated 2026-08-03** into this package dir (Fly COPY + CMD + operator CLIs track the nested paths) |
| `ops/c1_signal_daemon/` | S2b Python signal daemon (B1 POST client of the listener; warm / `emit_enabled=false` until strategy GO) — [build ADR](docs/adr/2026-08-08-s2b-signal-daemon-build.md) |

### `governance/` — meta-layer (imports core). Tier P1/P2. **Entirely root-resident — NOT physically moved (no `governance/` dir).**

Governance content (docs, skills, CI, discipline scripts) joins no import contract among application code, so physically relocating `docs/` → `governance/docs/` would break hundreds of cross-links (CLAUDE.md→`docs/adr/`, brief cross-refs, skill refs) for zero contract benefit. It stays at root, classified governance: `docs/` (adr, briefs, methodology, methodology_audit, spec, operational_rules, SESSIONS, mc_anchor_history, …), **`docs/ltm/`** (search/index-excluded LTM cold store — closed briefs, rolled SESSIONS, spent plans; see `docs/ltm/README.md`; not a new import layer), `.claude/skills/`, `.github/`, discipline `scripts/` (§2.1), root files (§2). The four-layer scheme is physically `core/ lab/ ops/` + root-resident governance.

---

## §2 — Root-resident (classified, **NOT physically moved** — tooling necessity)

These cannot relocate without breaking the harness, the build, GitHub, or `REPO_ROOT` computation. They stay at repo root, are **classified** for ownership, and are **exempt** from `check_boundaries.py` path-prefix mapping (the scanner special-cases them — see §3).

| Path | Layer | Why it stays at root |
|---|---|---|
| `pyproject.toml`, `Makefile` | governance | editable install + `make` targets resolve from root |
| `CLAUDE.md`, `README.md`, `STATE.md`, `PIPELINES.md` | governance | session-loaded / repo-root docs; `verify_lock_anchors` reads `CLAUDE.md` at root for MC-anchor denylist/context elsewhere |
| `.gitattributes`, `.gitignore` | governance | VCS policy must be at root |
| `LICENSE`, `.markdownlint.json` | governance | landed 2026-08-17 with the public-transition config drop (PR #29). `LICENSE` (view-only, all-rights-reserved) sits at root per GitHub's repo-level license-detection convention; `.markdownlint.json` configures the root markdownlint pass and sits at root per that tool's own discovery convention — same policy class as `.gitattributes`/`.gitignore`. Both were **absent from the §5 coverage-check exemption regex** until this pass (fixed below) — the "Zero unmapped" claim at the top of this file was silently failing against production. |
| `.claude/` (`settings.json`, `commands/`, `skills/`) | governance | the Claude Code harness requires these at exactly `.claude/skills`, `.claude/settings.json`, `.claude/commands` — moving them de-registers the skills/commands |
| `.github/` (`workflows/`) | governance | GitHub requires `.github/workflows/` at root |
| `scripts/` (all) | **mixed — see §2.1** | every `check_*`/`validate_*` script computes `REPO_ROOT = Path(__file__).resolve().parent.parent`; the pre-commit hook, CI, and `make validate` invoke `python scripts/<x>.py` from root. Relocating breaks `REPO_ROOT` + every invocation path. |
| `tests/` | **tests (exempt)** | a single suite imports core+lab+ops at once (ADR §8 Q-c); contract-exempt by design |
| `.cursor/` (`rules/*.mdc`) | governance | tracked editor agent-conduct / code-style rules — same policy class as `.claude/`, must sit at root for the Cursor harness |
| ~~`migration/`~~ | **removed 2026-07-16** (was governance historical) | Notion Phase-2 retirement audit dump (`REPORT.md` + `inventory.json`, 2026-06-13). Operator deleted. Retrieve via `git show` of pre-deletion tree; durable outcomes live in [`docs/governance/notion-redirect-map.md`](docs/governance/notion-redirect-map.md) + `docs/methodology/archive/notion/` + ADR [`docs/adr/2026-06-12-notion-surface-retirement.md`](docs/adr/2026-06-12-notion-surface-retirement.md). |
| ~~`ea/`~~ | **removed 2026-07-16** (was lab Tier P3) | historical Pine→MQL parity prototype + harness; CFD/OANDA retired, no EA authorized. Operator deleted the tree. Retrieve via `git show` of pre-deletion commits (`85a7325` scaffold / `4da6a60` Aegis tooling). Design record: [`docs/superpowers/specs/2026-06-28-pine-mql5-ea-conversion-design.md`](docs/superpowers/specs/2026-06-28-pine-mql5-ea-conversion-design.md). |
| `discovery_manifests/` (`README.md` + committed `<run_id>.json` pre-registrations) | **lab, Tier P2** | Gen-2 discovery K-ledger output (`lab/discovery/register_search.py` `open`/`close`); repo-root-anchored via `from research_utils.repo_root import repo_root` (a module, not an attribute — `research_utils.repo_root()` raises `AttributeError`) so runs land here regardless of invocation cwd — moving it breaks that anchor. Committed for auditability (PIPELINES.md §Data stores). |
| `deploy/` (`c1_rail/` listener + `c1_signal_daemon/` S2b second app) | **ops, Tier P1** | c1 rail Fly.io packaging (classified 2026-07-31; daemon app 2026-08-08). Build context = repo root; listener: `fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile`; daemon: `… deploy/c1_signal_daemon/…`. **Holds no `.py` today.** If one ever lands here, add a `deploy/` entry to `check_boundaries.py`'s `APP_LAYER_PREFIX` in the same commit: the current fallback (last line of `layer_of_file`, `check_boundaries.py:109`) would classify it **governance**, and any import of `ops/c1_rail_*` would then be flagged an illegal governance→ops edge. Never collapse daemon into the listener volume. |
| `requirements-ops.lock`, `requirements-research.txt`, `requirements-research.lock` | governance | ops lockfile + research **pin list** (ADR `2026-07-10-databento-research-stack.md`) + research **hash-locked pins**, generated 2026-08-22 per the recipe in [`W6 ADR`](docs/adr/2026-08-07-w6-rail-infra-closures.md) (obligation discharged). `.txt` stays the human-readable source of truth for version bumps; `.lock` is regenerated from it, not hand-edited. |
| `.rgignore`, `.cursorindexingignore`, `.cursorignore` | governance | agent search/index-exclusion policy for the `docs/ltm/` + `lab/archive/` cold store (CLAUDE.md "Docs/agent LTM", 2026-07-14) — must sit at root for `rg`/Cursor to auto-discover them, same policy class as `.gitignore`. |
| `.dockerignore` | governance | c1 rail build-context policy (classified 2026-07-31). `docker build` reads it **only from the context root**, and that context is the repo root (row above) — so it cannot move. Default-exclude allow-list keeping gitignored proprietary bytes (Pine, vendor CSVs, research, `.git`) out of the image shipped to Fly's remote builder; LF-pinned in `.gitattributes` because a CRLF checkout makes its patterns silently stop matching. Same policy class as `.gitignore`. |
| ~~`telemetry.jsonl`~~ | **removed 2026-07-15** (was orphan Tier P3) | leaked Cursor user-rule audit log (SOE Labs / SOPHIE "Audit Everything" → emit `telemetry.jsonl`); rode into `4441c72` as a side effect. Zero in-repo producers/consumers; `.cursor/hooks/` untouched. `git rm` + `.gitignore`; SOE Labs Cursor user rules deleted same day. Retrieve via `git show 4441c72:telemetry.jsonl`. |

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
_63 tracked `scripts/*.py` files (`git ls-files 'scripts/*.py'`)._

| Script | Layer | Gate id (tier) | Notes |
|---|---|---|---|
| `scripts/_build_lessons_index.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/archive_lab_analysis.py` | governance | `lab-catalog` (path-conditional) | — |
| `scripts/archive_strategy.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/audit_notice_grade_k_correction.py` | lab | `notice-grade-k-correction` (always) | — |
| `scripts/beta_cohesion_read.py` | lab | — | manual/local only, not in gates.yml |
| `scripts/check_adr_graph.py` | governance | `adr-graph` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_advisor_dedup.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_boundaries.py` | governance | `boundaries` (always) | — |
| `scripts/check_brief.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/check_closure_disposition.py` | governance | `closure-disposition` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_cost_model_closed_world.py` | lab | `cost-model-closed-world` (path-conditional) | — |
| `scripts/check_data_manifests.py` | governance | `data-manifests` (data-conditional) | — |
| `scripts/check_docs_runtime_inventory.py` | governance | `docs-runtime-inventory` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_falsifier_reachability.py` | governance | `falsifier-reachability-census` (always) | --stats (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_governance_prose_control_chars.py` | governance | `governance-prose-control-chars` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_instrument_ledger_coverage.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_instrument_rejection_coverage.py` | governance | `instrument-rejection-coverage` (path-conditional) | WARN, --exit-zero; layer fallback (not in SCRIPTS_LAYER) |
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
| `scripts/check_rule2_trip_log_liveness.py` | governance | `rule2-trip-log-liveness` (always) | --stats (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_sessions_queue_bind.py` | governance | `sessions-queue-bind` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_skill_deploy_sync.py` | governance | `skill-deploy-sync` (always) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/check_skill_refs.py` | governance | `skill-refs` (always) | — |
| `scripts/check_skills_no_constants.py` | governance | `skills-no-constants` (always) | — |
| `scripts/check_spec_provenance.py` | governance | `spec-provenance` (always) | --stats (report-only); layer fallback (not in SCRIPTS_LAYER) |
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
| `scripts/retire_adr.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/roll_sessions.py` | governance | `sessions-order` (path-conditional); `sessions-append-only` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/session_divergence_hook.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/sync_liveness_indexes.py` | governance | `sync-liveness` (path-conditional) | layer fallback (not in SCRIPTS_LAYER) |
| `scripts/sync_pine_to_worktree.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/sync_skills.py` | governance | — | manual/local only, not in gates.yml |
| `scripts/sync_skills_hook.py` | governance | — | manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER) |
| `scripts/validate_c1_monitoring_acceptance.py` | governance | `m1-tree-skew` (always) | --check-tree-skew (report-only); layer fallback (not in SCRIPTS_LAYER) |
| `scripts/verify_lock_anchors.py` | governance | — | manual/local only, not in gates.yml |
<!-- END generated: scripts-table -->

---

### §2.2 — Running a layer module via `python -m` (the PYTHONPATH convention)

The layer roots (`core/ lab/ ops/`) are **import roots, not packages** — modules inside a layer import each other as top-level (e.g. `from research_utils.repo_root import repo_root`, `from research_utils import breadth`). Phase C pinned this via `sys.path`/`pythonpath` (ADR `2026-06-05-monorepo-layer-boundaries` §rev.3 #4), **not** package-ification, so there is no `ops.live_journal` / `lab.codification` dotted path.

`pytest` puts the roots on `sys.path` automatically (`pyproject.toml` `[tool.pytest.ini_options] pythonpath = ["core","lab","ops","ops/c1_rail","ops/c1_signal_daemon","."]` — **there is no `governance` entry: the layer is root-resident and has no directory**, §1). A standalone `python -m <module>` does **not** — so prefix the invocation with the owning import root on `PYTHONPATH`:

| To run | Use |
|--------|-----|
| ~~ECR rolling report~~ | **RETIRED 2026-07-11** with `ops/live_journal/` ([estate ADR](docs/adr/2026-07-11-ops-cfd-estate-retirement.md)); `make ecr` removed |
| ~~DXTrade↔TV reconciler~~ | **RETIRED 2026-07-11** (same estate ADR) |
| ~~Codification emit~~ | **RETIRED 2026-08-02** with `lab/codification/` (ruling #3 / prune Packet D) |
| c1 rail (flat modules) | `PYTHONPATH=ops/c1_rail python -m c1_rail_arm …` (same root for `c1_rail_listener`, `c1_sizing_host_reference`, …) |
| c1 signal daemon (package) | `PYTHONPATH=ops/c1_signal_daemon python -m c1_signal_daemon` |
| Deflated Sharpe | `PYTHONPATH=lab python -m research_utils.deflated_sharpe …` |
| Step-0 battery | `PYTHONPATH=lab python -m research_utils.step0_battery …` |
| Selection tests | `PYTHONPATH=lab python -m research_utils.selection_tests …` |
| Discovery K-ledger | `PYTHONPATH=lab python -m discovery.register_search …` |
| Databento fetch | `PYTHONPATH=lab python -m databento_fetch.db_fetch …` (research venv) |

Skill wrappers under `.claude/skills/*/scripts/` remain as **stdlib subprocess launchers** (no lab imports — governance→lab is illegal); they forward to the `-m` forms above.

**Use the single owning root** (one dir, so no path-separator ambiguity — works identically on Windows and POSIX). Only if a module reaches across layers at runtime do you list several roots, and then the separator is `;` on Windows, `:` on POSIX — which is exactly why the single-root form is preferred. A bare `python -m <layer_module>…` from the repo root without `PYTHONPATH` is the recurring Phase-C footgun; this table is the fix.

---

## §3 — How `check_boundaries.py` resolves a file's layer

1. Path under `core/`, `lab/`, `ops/` → that layer (`APP_LAYER_PREFIX`). **There is no `governance/` prefix** — the layer is root-resident (§1), so governance is resolved instead by `GOVERNANCE_PREFIXES` (`docs/`, `.claude/`, `.github/`) and by the final fallback in rule 3.
2. Path under `tests/` or any §2 root-resident **non-`.py`** (docs/config/tooling) → **exempt**.
3. Root-resident `.py` (`scripts/**`, the root-level `.py` that stay — none after the move; all root `.py` relocate) → layer from §2.1.
4. The root-level flat modules (`portfolio_mc.py` etc.) → after the move they live under `core/`/`ops/`; resolved by rule 1.

Illegal-edge set: `core→{≠core}`, `governance→{lab,ops}`, `lab→ops`, `ops→lab`. Same-layer + `→core` + `→governance` (from lab/ops) legal. Relative imports (`from . import`) are same-layer → legal.

---

## §4 — Seam dispositions (settled; ADR §8)

| Path | Disposition |
|---|---|
| `tv_export_loader.py` | **core** (widen) — dissolves the `parity_check.py:222` ops→lab edge |
| ~~`validate_candidate.py`~~ | **retired** 2026-07-11 — Gen-1 harness CLI; see [`docs/adr/2026-07-11-gen1-pipeline-retirement.md`](docs/adr/2026-07-11-gen1-pipeline-retirement.md) |
| `strategies/codification/` → `lab/codification/` | **RETIRED 2026-08-02** — Python→Pine bridge deleted (ruling #3); severed `validation` import was 2026-07-11 |
| `accounts.py`+`cli.py` | **ops** — `accounts.py` deleted substrate Phase 2; `cli.py` tearsheet-only |
| ~~`journal_review.py`~~ | was **ops** canonical (the `.claude/skills/.../scripts/` duplicate `git rm`-ed); **retired 2026-07-11** with all of `ops/live_journal/` per [`docs/adr/2026-07-11-ops-cfd-estate-retirement.md`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md) — no such file exists; row kept for seam-provenance |
| `docs/`, `.claude/`, `.github/`, `scripts/`, `pyproject.toml`, root docs | **root-resident** governance/tooling (§2) — classified, not moved. **No physical `governance/` dir** — governance content joins no import contract, so moving it would break hundreds of cross-links for zero benefit. |

> The `trade_to_signal_event()` relocation row and the `check_skill_enum_mirror`/`check_skill_notion_schema` ops-discipline row were removed 2026-06-25 with the Notion ingest-subsystem retirement (commit `c6af48f`).

`?`-tier (contested at execution, resolve before declaring RESOLVED): **none** — all paths classified. Execution-time refinements vs the rev-1 REPO_MAP: governance stayed root-resident (not moved to `governance/`); `trade_to_signal_event` + the two skill validators reclassified per the edges `check_boundaries` surfaced.

---

## §5 — Coverage check (zero unmapped)

```bash
# every tracked path matches a layer rule (moved-prefix OR root-resident OR tests)
git ls-files | grep -vE '^(core|lab|ops|tests|scripts|docs|deploy|\.claude|\.github|\.cursor|discovery_manifests)/' \
  | grep -vE '^(CLAUDE|README|STATE|PIPELINES)\.md$|^(pyproject\.toml|Makefile|REPO_MAP\.md|LICENSE|\.markdownlint\.json|\.gitattributes|\.gitignore|\.dockerignore|\.rgignore|\.cursorignore|\.cursorindexingignore|requirements-ops\.lock|requirements-research\.txt|requirements-research\.lock)$' \
  && echo "UNMAPPED PATHS ABOVE" || echo "zero unmapped OK"
# (run post-move: scripts/ root-resident, the rest under the three layer roots)
```

> **Current state (2026-08-31):** the regex above passes clean. `requirements-research.lock` (added
> 2026-08-24, PR #166 — the hash-locked companion to `requirements-research.txt`, §2 row above) was
> the most recent gap, found and closed this pass. Before that, `LICENSE` and `.markdownlint.json`
> were the last unmapped paths (added 2026-08-17, closed the same day found). The exemption regex
> has been repaired five times since Phase C as new root-resident paths and dead tokens appeared
> (2026-06-22, 2026-07-15, 2026-07-31, 2026-08-21, 2026-08-31); each repair's detail is in `git log -p`
> on this file, not restated here.
