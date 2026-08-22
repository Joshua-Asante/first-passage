# REPO_MAP — the standing layer map (`core / governance / lab / ops`)

> **Status:** authoritative path→layer partition for the monorepo-boundaries restructure (ADR `docs/adr/2026-06-05-monorepo-layer-boundaries.md`, ACCEPTED 2026-06-05). This is the **human-readable source of truth for `check_boundaries.py`** — note the coupling is by hand, not by code: the scanner **never opens this file** (its own docstring says so), it hard-codes the equivalent mapping in `APP_LAYER_PREFIX` / `GOVERNANCE_PREFIXES` / `SCRIPTS_LAYER`, and **no gate compares the two**. Edit both together. It is also the spec the Phase-C `git mv` executes against — **NOT** a deletion feed (the deletion instrument was retired on main, `a9d16d0`).
> **Authored:** Phase C, Step C2 (before the move), so the partition is written-then-executed, not inferred.
> **Coverage rule:** every `git ls-files` path resolves to exactly one layer via the rules below. Zero unmapped (verified — see §Coverage check).

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
| `core/data/tv_exports/` `core/data/bar_data/` `core/data/external/` | `data/tv_exports/` `data/bar_data/` `data/external/` (backtest panels — immutable shared inputs). Live trade-lists: `tv_exports/cme/`. `bar_data/` = **frozen CME micros only** (`6J`/`MNQ`/`MYM_M15`; producer dead since Pepperstone retirement). Dukascopy / OANDA deleted Phase 5 (`tombstone` (pruned; `git show pre-prune-2026-08-08:docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md`)); CFD-era `bar_data` + `tv_exports/candidates/` deleted 2026-08-03 ([ADR](docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md) · `tombstone` (pruned; `git show pre-prune-2026-08-08:docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md`)) |

### `lab/` — free-churn research (imports core+governance). Tier P2/P3.

| New path | From |
|---|---|
| `lab/analysis/` | `analysis/` **minus `oanda_stage1/tv_export_loader.py`** (→core). Dated campaign evidence. **STM layout (2026-08-03):** nested hot bodies at `lab/analysis/<theme>/<slug>/`; flat CARD stubs at `lab/analysis/<slug>/CARD.md`; cold bodies at `lab/archive/<slug>/` — open [`lab/CATALOG.md`](lab/CATALOG.md) first. **NON-RUNNABLE Gen-1 leftovers** (still `import validation.*`; CI `--ignore`): `legacy/guardian_parity_2026-06-23/`, `legacy/usoil_regime_capture/` — plus `gbpusd_rank_cert/`, whose runnable body now lives at **`lab/archive/gbpusd_rank_cert/`** (flat `CARD.md` stub only under `lab/analysis/`, so the CI `--ignore` for the old flat path is a no-op). Keep as evidence; do not re-run without restore-from-git of retired Gen-1 or a re-point ADR. |
| `lab/archive/` | cold bodies for archived `lab/analysis/<slug>/` studies (STM/LTM; hot stubs remain at `lab/analysis/<slug>/CARD.md`) |
| `lab/CATALOG.md` | generated index — open first for lab decisions (`make lab-catalog` / `scripts/archive_lab_analysis.py --regenerate-catalog`; freshness gated by `make lab-catalog-check` / pre-commit `--check --catalog-only`) |
| `lab/validation/` | `validation/` — **retired 2026-07-11**, see [`docs/adr/2026-07-11-gen1-pipeline-retirement.md`](docs/adr/2026-07-11-gen1-pipeline-retirement.md); row kept for move-provenance history |
| `lab/validation_selftest.py` | extracted from `validation/controls.py` (Gen-1 self-test generators; DSR gate wired 2026-07-11 — `tests/test_validation_selftest_dsr_gate.py`; full §8 universe-gate `--self-test` wired 2026-07-12 — `research_utils/universe_gate.py`) |
| `lab/research_utils/` | stable research primitives: permutation + Gen-2 DSR / step0 / selection / plateau (relocated from `.claude/skills/strategy-validation/scripts/` 2026-07-11; see ``docs/superpowers/specs/2026-07-11-lab-research-stack-relocation-design.md`` (public-seed omitted; `git show pre-prune-2026-08-08:docs/superpowers/specs/2026-07-11-lab-research-stack-relocation-design.md`)) + `universe_gate.py`. **W4 2026-08-07:** SPA/StepM/PBO **dormant** (named re-arm); plateau **archived**; breadth **tombstoned** as live producer — [`W4 ADR`](docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md) |
| `lab/discovery/` | Gen-2 K-ledger (`register_search.py`); canonical home as of 2026-07-11 relocation |
| `lab/databento_fetch/` | Gen-2 cost-gated Databento client (`db_fetch.py`); canonical home as of 2026-07-11 relocation |
| `lab/codification/` | `strategies/codification/` — **RETIRED 2026-08-02** (operator ruling #3 / prune Packet D; was parked ADR 2026-07-11; retrieve via git history; future bridge = fresh build) |

### `ops/` — operational (imports core+governance). Tier P1.

| New path | From |
|---|---|
| ~~`ops/accounts.py`~~ `ops/cli.py` | `accounts.py` retired substrate Phase 2 (multiplier spine); `cli.py` retained as **tearsheet-only** historical entry point. FXIFY-challenge path excised 2026-07-11 per [`docs/adr/2026-07-11-fxify-ops-surface-retirement.md`](docs/adr/2026-07-11-fxify-ops-surface-retirement.md); full spine delete [`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`](docs/adr/2026-07-22-challenge-era-substrate-retirement.md) §2-D |
| ~~`ops/fxify_rule_validator.py`~~ ~~`ops/parity_check.py`~~ ~~`ops/tv_mt5_pnl_reconciliation.py`~~ | root — `fxify_rule_validator.py` + `tv_mt5_pnl_reconciliation.py` **retired 2026-07-11** per [`docs/adr/2026-07-11-fxify-ops-surface-retirement.md`](docs/adr/2026-07-11-fxify-ops-surface-retirement.md); `parity_check.py` **retired 2026-07-11** per [`docs/adr/2026-07-11-ops-cfd-estate-retirement.md`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md); rows kept for move-provenance |
| `ops/live_journal/` — **retired in full 2026-07-11** per [`docs/adr/2026-07-11-ops-cfd-estate-retirement.md`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md) (the reconcile-subsystem disposition the fxify-ops-surface ADR deferred/parked); `references/execution_lessons.md` relocated to `docs/methodology/lessons/` (not lost); row kept for move-provenance history | `live_journal/` (incl. canonical `journal_review.py`) |
| `ops/weekly_review_feeder/` | `weekly_review_feeder/` — **retired 2026-07-06**, see ``docs/ltm/briefs/2026-07-06-weekly-review-feeder-retirement.md`` (pruned; `git show pre-prune-2026-08-08:docs/ltm/briefs/2026-07-06-weekly-review-feeder-retirement.md`); row kept for move-provenance history |
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

`scripts/` stays at root but its files are classified. `check_boundaries.py` hard-codes the equivalent mapping in its own `SCRIPTS_LAYER` dict — it does **not** load this table, and nothing gates the two against each other, so a change here must be mirrored there by hand. ⚠ **This list is incomplete:** `git ls-files 'scripts/*.py'` returns 48 files (was 35 — 2026-08-21 re-count; a run of gate-script landings between 2026-08-17 and 2026-08-21 widened the gap, see below) and 19 are unlisted (`archive_strategy`, `check_adr_graph`, `check_advisor_dedup`, `check_instrument_ledger_coverage`, `check_personas`, `check_push_collision`, `check_status_consistency`, `gate_fire_log`, `import_skill_from_cache`, `instrument_profiles`, `layer_bootstrap`, `m1_item5_capture`, ~~`migrate_adr_headers_m1`~~ (retired 2026-08-02), `repo_hygiene`, `repo_retrieve`, `retire_adr`, `session_divergence_hook`, `sync_liveness_indexes`, `sync_skills_hook`, `validate_c1_monitoring_acceptance`). All 19 active entries are stdlib-only today (a couple import sibling `scripts/` modules, e.g. `repo_retrieve`/`sync_liveness_indexes` → `gate_fire_log` — same root-resident file, not a layer-crossing import), so `check_boundaries.py` stays green and the gap is latent — but any of them gaining a first-party `core/lab/ops` import would be classified `governance` by the fallback and could be flagged an illegal edge.

- **governance** (discipline/gates): `check_brief.py`, `check_boundaries.py`, `check_data_manifests.py`, `check_pine_manifest.py`, `check_path_liveness.py`, `check_root_doc_liveness.py` (markdown-link liveness over the five root orientation docs, 2026-07-15 — sibling of `check_path_liveness.py`; wired into pre-commit + `make check`), `check_lab_path_relocation.py` (WARN — `docs/**/*.md` cites of relocated `lab/…` paths; `make lab-path-relocation`; not in `gates.yml`), `check_md_relative_links.py` (WARN — file-relative link liveness under `docs/`/`ops/`/`lab/`, sibling of `check_path_liveness.py`/`check_root_doc_liveness.py`; `make md-relative-links`; manual forensic tool, not in `gates.yml`), `check_falsifier_reachability.py` (WARN — do standing ADR falsifiers still have inputs that can accrue, operational_rules.md Rule 11; `make falsifier-reachability`; not in `gates.yml`), `check_skill_refs.py`, `check_skills_no_constants.py` (methodology-skill no-constants; extracted 2026-08-03 from retired `validate_params`), `check_closure_disposition.py` (every new closure carries a typed Iterate block — ADR `2026-08-04-iterate-closure-exit-mandatory`; wired `gates.yml` path-conditional on `docs/briefs/closures/`, `docs/briefs/INDEX.md`, `lab/CATALOG.md`), `check_supersession_placement.py` (a withdrawing addendum needs an upstream warning — `operational_rules.md` Rule 14; wired `gates.yml` path-conditional on `docs/adr/`), `check_governance_prose_control_chars.py` (rejects stray C0 controls in high-traffic governance prose — 2026-08-11 SESSIONS incident; wired `gates.yml` path-conditional on `SESSIONS.md`/`rejected_candidates.md`/`mc_anchor_history.md`), `check_pursuit_records.py` (GRAND-tier pursuit-record limbs — ADR `2026-08-09-grand-tier-quintessentials-binding`; WARN/report-only, wired `gates.yml` data-conditional on `docs/pursuits/`), `gate_manifest.py` (single owner for pre-commit/`make` gate composition, reads `gates.yml` — [W5 ADR](docs/adr/2026-08-07-w5-governance-diet.md); the `make check`/`validate`/`pre-commit`/`--list` entry point cited above), ~~`validate_params.py`~~ (**retired 2026-08-03** — derived `params.toml` hub; [`docs/adr/2026-08-03-params-toml-gate-retirement.md`](docs/adr/2026-08-03-params-toml-gate-retirement.md)), ~~`validate_alert_payloads.py`~~ (**retired 2026-08-02** — Copygram→FXIFY estate; see [`docs/adr/2026-07-11-fxify-ops-surface-retirement.md`](docs/adr/2026-07-11-fxify-ops-surface-retirement.md) Addendum 2026-08-02), `verify_lock_anchors.py`, `sync_pine_to_worktree.py`, `sync_skills.py`, `roll_sessions.py` (SESSIONS.md roll-off — ADR/spec `docs/spec/2026-06-27-session-log-rolloff-design.md`; stdlib-only), `parse_bar_export.py` (vendor-bar parse; imports `core/bar_export_loader` → core-only, governance-legal), `pine_check.py` (+ `pine_check_audit.sh`/`.ps1` — zero-auth Pine compile pre-flight, validated 2026-06-23; LOCAL/manual, not CI), `archive_lab_analysis.py` (lab STM/LTM archive — design ``docs/superpowers/specs/2026-07-11-lab-analysis-stm-ltm-archive-design.md`` (public-seed omitted; `git show pre-prune-2026-08-08:docs/superpowers/specs/2026-07-11-lab-analysis-stm-ltm-archive-design.md`); `--check --catalog-only` wired into pre-commit + `make check` / CI; stdlib-only), `githooks/`, `install_hooks.sh`, `install_hooks.bat` (`check_brief_evidence_coverage.py` retired 2026-06-08 — ADR `2026-05-16-fixture-test-requirement` Amendment)
- **lab** (research): `mc_user_guardian.py`, `pine_lint.py`, `cost_geometry_pregate.py` (instrument-ledger Phase-0 cost-geometry pre-gate — ADR `2026-06-22-cost-geometry-pregate.md`); `parse_econ_export.py`, `diff_econ_calendar.py` (ECON EXPORT v0.1 — owner [`docs/spec/2026-08-18-econ-export-v01.md`](docs/spec/2026-08-18-econ-export-v01.md)); ~~`validate_candidate.py`~~, ~~`run_corpus_fdr.py`~~, ~~`wfo/`~~ — **retired 2026-07-11** per [`docs/adr/2026-07-11-gen1-pipeline-retirement.md`](docs/adr/2026-07-11-gen1-pipeline-retirement.md)
- **ops** (live-ops tooling): `lock_event_hook.py`, ~~`inactivity_simulator.py`~~ (**retired 2026-08-02** — Q-MCTO-1 shadow; production `bust_inactivity` in `core/mc/simulation.py`) (`run_ecr.py` + `preprocess_pine_ecr_logs.py` **retired 2026-07-11** with the ECR estate, ADR [`2026-07-11-ops-cfd-estate-retirement`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md))

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
  | grep -vE '^(CLAUDE|README|STATE|PIPELINES)\.md$|^(pyproject\.toml|Makefile|REPO_MAP\.md|LICENSE|\.markdownlint\.json|\.gitattributes|\.gitignore|\.dockerignore|\.rgignore|\.cursorignore|\.cursorindexingignore|requirements-ops\.lock|requirements-research\.txt)$' \
  && echo "UNMAPPED PATHS ABOVE" || echo "zero unmapped OK"
# (run post-move: scripts/ root-resident, the rest under the three layer roots)
```

> **2026-08-21 audit (second pass):** the check was **failing as written** again
> — two unmapped paths (`LICENSE`, `.markdownlint.json`), both landed 2026-08-17
> with the public-transition config drop (PR #29) and never added to the
> exemption regex. Both are root-resident governance (row added to §2); the
> regex above is corrected. `REPO_MAP.md` sat outside the 2026-08-21 root-doc
> coherence campaign's edited scope
> ([campaign note](docs/notes/audits/2026-08-21-coherence-campaign.md)) — this
> was a separate, direct verification pass against production bytes.

> **2026-07-31 audit:** the check was **failing as written** — five unmapped
> paths (`.dockerignore` + the four `deploy/c1_rail/` files), the c1 rail's
> deployment tree having been added with no §2 row. Both are now classified in
> §2 (`deploy/` → ops P1; `.dockerignore` → governance) and added to the regex.
> The same pass retired three **dead exemption tokens** the regex still carried:
> `ea` and `migration` (both trees deleted 2026-07-16 — §2 records the deletions
> itself, so the exemptions outlived their targets) and `governance` (never a
> directory — §1 states the layer is entirely root-resident, and
> `check_boundaries.py`'s `APP_LAYER_PREFIX` has no such prefix). The stale
> `governance` path token was also removed from `pyproject.toml`'s pytest
> `pythonpath` and from §2.2 / §3, which had both propagated it.
>
> **2026-07-15 audit:** seven more root-resident paths appeared since the prior
> audit and were tripping the check: `PIPELINES.md` (a root doc, joins the
> `CLAUDE|README|STATE` group), `discovery_manifests/` (Gen-2 K-ledger output,
> §2), `requirements-ops.lock` + `requirements-research.txt` (per-env
> lockfiles, §2), `.rgignore` + `.cursorindexingignore` + `.cursorignore`
> (agent search/index-exclusion policy, §2), and `telemetry.jsonl` (orphan
> artifact). Six remain classified in §2; `telemetry.jsonl` was investigated
> the same day, confirmed orphan (Cursor user-rule leak, not repo tooling),
> then `git rm`'d + gitignored — struck from this regex and marked removed in §2.
>
> **2026-06-22 audit:** the first exempt group gained `.cursor|migration` — two
> root-resident trees that appeared after the original Phase-C verification and
> were tripping the check (`.cursor/rules/*.mdc`,
> `migration/{REPORT.md,inventory.json}`); both are now classified in §2. A third
> tripping path, `reports/regime_time_cost/RESULTS.md`, was **relocated** to the
> then-canonical `ops/reports/regime_time_cost/` (covered by the `ops/` prefix), so
> root `reports/` holds no tracked content and `reports` was dropped from this
> regex — completing the `reports/`→`ops/reports/` move (§1). **2026-08-03:** that
> RESULTS.md moved again to `lab/analysis/regime/regime_time_cost_2026-06-09/`; `ops/reports/`
> deleted.
