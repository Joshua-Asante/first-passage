# First Passage Architecture Improvement Roadmap

**Status:** Proposed implementation sequence; documentation only.

**Goal:** Strengthen the monorepo's enforceable boundaries, dependency-aware validation, runtime interfaces, and service verification.

**Companion:** [Installable core implementation plan](2026-09-10-installable-core.md). Its PR 1 / PR 2 labels refer to the two sequenced packaging deliveries (a conditional PR 3 is deferred design), not the total number of changes in this roadmap.

## Delivery order

| Order | Deliverable | Dependency / acceptance boundary |
|---|---|---|
| 1 | Complete import-boundary resolution | Land before TB-I2 dispatch and import-layout changes |
| 2 | Dependency-aware research CI triggers | Independent; land before changing shared core behavior |
| 3 | Installable core wheel | Execute the companion plan's first slice |
| 4 | Offline service harness and rail artifact consumption | Dry-run pytest baseline first; image migration deferred through Track B closure |
| 5 | Structured authority interfaces | Separate change preserving current denylist behavior |
| 6 | Explicit Monte Carlo compatibility exports | Separate change preserving supported historical imports |

Each deliverable should be a separately reviewable change with its own regression evidence. This roadmap does not authorize production deployment or alter strategy/risk policy. Namespace modernization remains deferred as described in the packaging plan.

## Sequencing against Tracks A and B

The [Track A plan](2026-09-10-track-a-m1-stage1-completion.md) and [Track B umbrella](../../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) own execution sequencing. **Planning disposition: defer packaging PR 2 until Track B closes and a fresh operator decision authorizes a new image qualification cycle.** Closure alone does not authorize changing the sealed execution. Earlier adoption requires an explicit operator ruling recorded with the umbrella and TB-S3, with TB-S3 deliberately specified against the wheel layout before implementation. This roadmap records the deferral, not a new operator ruling.

- This roadmap lands no listener image-assembly change and no `ops/c1_rail/*.py` byte change between A5 Step 2.5 (deploy) and A8 Step 2.4b (final re-bake). Track A's own A1b pin move is carried by its explaining commit and the A8 re-bake, not by this roadmap; after the Step 2.3 redeploy the ops bytes stay unchanged until 2.4b.
- No executable change may land between the TB-I3 live test and the B7 seal, or after that seal within this attempt. “After A8, before TB-S3” is not a window: TB-S3 is wave 1a; Track A delivery is in wave 3 of the same graph.
- Land boundary resolution before TB-I2: a replay under `lab/` can currently import a flat ops module without a gate failure. TB-S2 must assign the shared state machine to a permitted owner. Any resulting ops source repair obeys the A5→A8 restriction.
- Respect “No two live packets share a file.” PR 2 overlaps TB-I3's deployment/manifest-test footprint. Consumer migrations must avoid TB-I2's reserved `lab/analysis/c1/tradeify_book_replay_2026-09/` files. The recall migration lands as a non-`tb-` PR at an orchestrator integration point; the umbrella reserves `CLAUDE.md` and its §10 hook flags such edits in Track B PRs.
- Route governed `core/*` code edits, including the MC facade, to Claude Code under [surface-allocation ADR test 1](../../adr/2026-07-14-cc-cursor-surface-allocation.md). Tooling-only frozen implementations may use the implementation lane; any discovered core fix must be routed separately. Test 1 also covers ADRs, Pre-Qs, pre-registrations, closures, lifecycle state, and `CLAUDE.md`/`STATE.md`/memory: edits to CLAUDE.md, STATE.md, any ADR (including the §1 boundaries-ADR amendment), and `docs/operational_rules.md` are Claude-Code-only surfaces, not just `core/*` code. Capture recall fixtures wholly before TB-I1 or re-capture wholly after it.

The companion's second-slice section lists the COPY contracts, evidence pins, and shared fingerprint components that must change together if PR 2 is eventually admitted.

## 1. Complete import-boundary resolution

**Observed gap:** `scripts/check_boundaries.py` indexes immediate children of `core/`, `lab/`, and `ops/`, then resolves imports by their first component. A read-only probe recognized `from research_utils import step0_battery` as lab-owned, but returned no targets for `from lab.research_utils import step0_battery`, `from ops.c1_rail import c1_rail_listener`, or `import c1_rail_listener`. These forms are runtime-valid: the layer directories are namespace packages, the repo root is on the path, and pytest also exposes both nested ops roots. A lab import of `c1_sizing_host_reference` can therefore run while escaping the gate. These are coverage gaps, not evidence that those edges currently exist in production.

**Files:** `scripts/check_boundaries.py`, `tests/test_check_boundaries.py`, `scripts/repo_map_layers.yml`, `scripts/check_repo_map_layers.py`, its regression tests, `REPO_MAP.md`, and the owning [boundaries ADR §2.3](../../adr/2026-06-05-monorepo-layer-boundaries.md). Any new flat-roots map must be checked against its YAML mirror in the same change; the current mirror checker only compares three existing maps.

- [ ] Add synthetic fixture tests putting each import form in a forbidden source layer; require detection of the intended target layer.
- [ ] Resolve both root-qualified names and the documented flat import roots, including `ops/c1_rail`. Resolve `from package import module` against actual module paths rather than assuming the first token is the complete identity.
- [ ] Preserve legal same-layer relative imports, including `core/mc` imports of core modules. Do not invent a runtime-valid cross-layer fixture: `from ...ops.other import z` in `lab/pkg/mod3.py` raises beyond-top-level `ImportError` under the supported roots. If relative resolution is extended, diagnose beyond-top-level imports as invalid imports separately from illegal layer edges.
- [ ] Preserve alias and lazy-import coverage. Preserve the existing hard error for cross-layer collisions and report candidate paths. Ambiguity means candidates in more than one layer; same-layer duplicate stems such as the two ops `m1_stage1_control.py` files must pass. Keep third-party imports distinct from unresolved first-party paths.
- [ ] Keep the existing legal-edge set unchanged. Document dynamic imports and filesystem reads as separate coverage limitations; do not claim an AST import scanner validates those dependencies.
- [ ] Run `python -m pytest tests/test_check_boundaries.py tests/test_repo_map_layers.py -q`, `python scripts/check_boundaries.py`, and `python scripts/check_repo_map_layers.py`. Extend both the AST-based map loader and the checker's stdlib-YAML fallback if a new flat-roots map is added; the fallback currently knows only the three existing sections.

**Acceptance:** All supported syntactic forms of the same dependency receive the same layer verdict; allowed edges still pass; forbidden edges and ambiguity fail. If the improved resolver exposes existing violations, classify and fix those explicitly rather than expanding the allowed edges.

## 2. Trigger research validation when shared dependencies change

**Observed gap:** `.github/workflows/validation-controls.yml` triggers on `lab/**` and its own workflow file. Lab code consumes core code, so a core-only change can skip the tests located under `lab/`. The main `tests/` job still runs. None of the five currently tracked lab test files imports core; scheduling the suite does not prove core coverage. This becomes load-bearing when TB-I2 adds core-consuming lab tests.

**Files:** `.github/workflows/validation-controls.yml`, `tests/test_validation_workflow_paths.py` (new), and the invocation owner `scripts/archive_lab_analysis.py` (its `_CATALOG_HEADER` constant) if the command changes; `lab/CATALOG.md` is a rendered copy regenerated from that script, not a second owner — regenerate rather than hand-edit it. Do not add a third invocation copy to `scripts/README.md`.

- [ ] Add only `core/**`, `pyproject.toml`, and `requirements-ops.lock` to both push and pull-request filters, retaining `lab/**` and the workflow path. The job installs the ops lock; the research environment is deliberately isolated. Neither research dependency files nor `scripts/layer_bootstrap.py` are current dependencies of these tests.
- [ ] Inspect the workflow's actual setup and lab imports for other shared governance executables. Add only those concrete dependencies; do not trigger this job for every documentation edit.
- [ ] Add a semantic trigger test using representative changed paths: core engine, core utility, lab source, ops lock, workflow file, and negative cases for research dependencies, bootstrap script, and unrelated Markdown. Test both event filters so they cannot drift independently.
- [ ] Prune the nine absent paths from the eleven-entry `--ignore` roster and remove the stale coverage example. Retain only present, justified manual/archive exclusions; verify the count against the implementation revision. Keep this a non-required check under the Q-GATESTACK-1 closure.
- [ ] Run the new trigger tests and the existing validation-controls job's exact command in its supported environment. Verify on GitHub that a shared-source change schedules the consumer job and an unrelated docs-only change does not.

**Acceptance:** Changes to the named dependencies schedule the research suite; coverage claims require actual consumer tests. Keep the trigger list small and explicit until dependency complexity justifies automation.

### Trigger reachability to verify at implementation

| Check | Positive paths | Negative / required-check boundary |
|---|---|---|
| validation-controls | `lab/**`, `core/**`, `pyproject.toml`, `requirements-ops.lock`, own workflow | Research lock/bootstrap changes and docs-only changes outside `core/**` do not trigger (`core/**` matches the 35 tracked `core/**/*.md` files today, including `core/mc/README.md`); non-required |
| A2 image validation | Shared core/root metadata/ops-lock paths above, plus A2's image, ops, validator, acceptance and test inputs | A2 brief owns its complete predicate; test representative inputs against that owner |
| core-package | `core/**`, root metadata, ops/build locks, builder, packaging tests, own workflow | Dedicated non-required workflow; no registration in required manifest and no unrelated docs trigger |

## 3. Separate structured authority from prose formatting

**Observed gap:** `ops/recall/guard.py::load_denylist` regex-reads Python source and historical values from `CLAUDE.md`. Formatting and prose placement therefore affect a machine-consumed guard. Existing root instructions explicitly preserve a historical statement for that parser.

**Files:** `ops/recall/guard.py`, its existing tests (locate by `load_denylist` / `Denylist`), a historical-record JSON artifact under `docs/`, `docs/operational_rules.md`, `tests/test_docs_runtime_inventory.py`, `docs/notes/audits/docs-runtime-inventory.md`, `ops/recall/README.md`, `ops/sentinel/scan.py` and `tests/governance/test_sentinel_memory.py`, and the historical-record/root-document owners. Read production sources before specifying any risk-related values, following Rule 0.

`ops/sentinel/scan.py::_stale_anchor_findings` is a second machine reader of the CLAUDE.md anchor triple: it regex-matches the slash form (`_ANCHOR_TRIPLE`) to flag memory files that assert a different triple. That pattern does not match the current CLAUDE.md prose, so this tripwire is already dark. Decide, as part of this migration, whether to point sentinel at the new schema-versioned record (reviving the check) or to record the dark state explicitly rather than silently carrying it forward.

- [ ] Capture the current denylist values, source provenance, and representative accept/reject outcomes at one revision before extraction changes. The `firm_rules` regex currently yields no values from its dict comprehension; historical allocations enter through `historical_challenge.py`. Preserve the float-repr strings `0.33999999999999997` and `0.7000000000000001` for equivalence; any cleanup or newly admitted live allocation is a separately reviewed behavior change. Do not capture across TB-I1.
- [ ] For code-owned values, consume their canonical exported definitions through a narrow read-only adapter. Importing `dd_protection` executes `_validate_protection_rule()` and imports `lifecycle`; the recall CLI does not put `core/` on its path. Specify and test explicit bootstrap/import-time behavior or a validated static adapter before implementation. Keep the adapter outside core if it also consumes governance artifacts; never introduce a core-to-governance dependency.
- [ ] Give historical values a schema-versioned record with explicit historical scope and provenance. Validate required fields and reject malformed or missing required sources with an explicit error; do not silently return an incomplete guard.
- [ ] Switch the consumer and document owner together. Preserve existing numeric normalization and context-matching behavior. Do not reinterpret historical records as current operating authority.
- [ ] Test prose reordering and formatting changes: they must no longer change the denylist. Test malformed records and missing sources, and compare the full behavioral fixture against the old extractor.
- [ ] Remove the root document's formatting constraint only after the new consumer passes equivalence tests. Update the runtime-inventory assertion and audit, recall README, and operational rules in the same PR: the latter currently calls the CLAUDE triple a canonical owner. If the prose literals remain, label them a derived mirror. Confine the CLAUDE edit to Strategy Reference; preserve Live-execution posture and use the integration point above.

**Acceptance:** Machine behavior is independent of narrative wording, while the accepted/rejected note corpus remains unchanged. Review any desired behavior change separately from this interface migration. Define the exact schema and adapter API in this slice's design before implementation.

## 4. Verify the assembled rail through an offline service harness

**Observed gap:** The rail HTTP adapter and listener explicitly describe socket/process wiring as untested. Existing integration tests drive handlers through `BytesIO`. This fast, no-Docker pytest harness complements A2, which owns in-image HTTP checks L3–L8. A2 D9 already collects `tests/ops/test_c1_rail_*.py`. Deliberately duplicate disarmed boot, refused POST decisions, invalid acceptance and implicit-disarm behavior where reachable without enabling live mode.

**Files:** `tests/ops/test_c1_rail_service.py` (new), reusable fixtures under `tests/ops/`, and the deployment-image checks in the companion plan.

- [ ] Start the actual service process on loopback with an ephemeral port, a temporary configuration, and synthetic state. Wait for readiness with a bounded deadline; capture diagnostic output and terminate the process in test cleanup, including failure paths.
- [ ] Scope this first harness to `dry_run=true` and refusal paths; exclude `dry_run=false` execution. Deny external networking and assert zero downstream traffic. No fake-downstream seam is needed. A later live-mode synthetic harness needs a separately designed sender seam: `make_handler` does not forward the lower-layer injected sender, and URLs are hardcoded. Any such ops edit obeys both freeze windows.
- [ ] Exercise health, authentication failures, malformed payloads, and missing/invalid state through HTTP. Assert response semantics and side effects, including zero downstream calls on refused paths.
- [ ] Add concurrent-request cases that assert ledger validity and documented shared-state invariants. Do not invent exactly-once delivery guarantees. Per-request `exec_state.load_into(host.open_leg_state)` under `ThreadingHTTPServer` may expose a shared-dict race; route a finding through c1-rail/Rule 0, not a fixture workaround.
- [ ] Restart against the same temporary state and verify documented recovery/refusal behavior. Reuse existing telemetry and transport-unknown contracts as the expected behavior rather than designing new retry policies.
- [ ] Run equivalent behavioral scenarios against the current and eventual wheel images on GitHub Actions Docker; the operator desk has no Docker. Wheel subprocesses must strip the `PYTHONPATH` exported by `tests/conftest.py`, run with `-I`, and use a temporary pytest config without source roots; verify origins. Name the owning runner explicitly at implementation: either extend A2's `c1-image-validation.yml` (amending the A2 brief as owner) or add a dedicated non-required image workflow; add the chosen workflow's predicate to the reachability table above. The fast harness itself stays separate from A2 image validation.

**Acceptance:** The real HTTP/process path passes offline with bounded startup/shutdown, valid persisted state, and no external side effects. Establish this baseline before accepting the packaging plan's rail-image migration. Detailed fixture schemas and expected responses belong in that slice's implementation plan.

## 5. Freeze an explicit Monte Carlo compatibility interface

**Observed gap:** `core/portfolio_mc.py` re-exports every non-dunder name from `mc.modes`, including private helpers needed by historical scripts. Internal changes can consequently change the facade's apparent API. The current loop leaks every non-dunder name of `mc.modes` (83 at the time of writing, on CPython 3.12/3.13/3.14 with `core` on the path — the exact count is revision- and interpreter-dependent), including `np`, `pd`, `argparse`, `Path`, and other scientific-library/typing imports. Priority is low: active lab consumers already use `mc.*`; remaining facade consumers are tests and the already broken `lab/analysis/time_to_pass.py` (`pmc.HORIZON_DAYS` is absent).

**Files:** `core/portfolio_mc.py`, `core/mc/modes.py` if required, the existing `tests/core/test_mc_module_facade.py`, `tests/core/test_firm_constants_single_source.py`, the documentation owners `core/mc/README.md` and `PIPELINES.md`, and individually identified active consumers.

- [ ] Before narrowing exports, reconcile or explicitly supersede the prohibition in [the dead-code-prune handoff](../../briefs/handoffs/2026-07-24-cc-handoff-core-dead-code-prune.md); this roadmap does not override it. Route implementation to Claude Code.
- [ ] Inventory current imports and reflective uses of `portfolio_mc`, including private helpers. Use the research catalog and historical retrieval instructions when classifying consumers; an empty ordinary search is not proof of no consumer. Enumerate archived callers from this repository's own history using `lab/ARCHIVED.json`'s `baseline_commit` (`git grep -l portfolio_mc <baseline_commit> -- lab`, then `git show <baseline_commit>:<path>` for each hit); the archive mirror named in that file's `retrieval` field is a fallback, not the primary source. Record the resulting private-helper set in this inventory step before choosing supported private helpers.
- [ ] Record the current compatibility export set and intentionally supported monkeypatch/global behavior, including the facade-owned simulation count forwarded by `_run_seeds` and identity/concurrency coverage already in the facade test. Preserve every name the facade test (`tests/core/test_mc_module_facade.py`) and constants test (`tests/core/test_firm_constants_single_source.py`, which also reads `portfolio_mc.ALLOCATIONS`) import at the time of writing, including `PINE_SHRINK_ALLOCATIONS`, `SWEEP_CONFIGS`, `GA4_ALLOCATIONS`, `ALLOCATIONS`, `load_trades`, `build_daily_panel`, `build_week_blocks`, `_simulate_path`, `run_seed`, `report_default`, and `SIMS_PER_SEED` — plus the archived-caller helpers identified by the inventory step above.
- [ ] Replace unrestricted `dir(_modes)` export copying with an explicit compatibility export list. Preserve required object identity and wrapper behavior; `__all__` alone is insufficient because it does not constrain direct attribute access or remove the current copying loop.
- [ ] Add regression tests for existing named imports, deliberately supported private helpers, the `_run_seeds` forwarding contract, and absence of an unrelated newly added internal symbol from the facade.
- [ ] Scope consumer migration to tests and `time_to_pass.py`, whose broken assumption needs explicit treatment. Route new consumers to focused `mc` modules; respect Track B file reservations. Keep legacy imports working; do not rewrite archived campaigns solely to enforce a modern interface.

**Acceptance:** Internal symbols added to `mc.modes` no longer become facade exports automatically. The extended facade and constants tests prove compatibility. Synthetic engine tests import `mc.*` directly and provide additional engine coverage, not evidence of facade compatibility. Any deliberate compatibility removal requires its own consumer migration and review.

## Scope and verification

This document records the five architecture improvements alongside the existing packaging plan. It is a roadmap with concrete acceptance boundaries, not a claim that implementations or tests already exist. Each follow-up design must name exact interfaces and executable regression cases before code changes begin. Run relevant tests and the repository gate manifest for each implementation; report unavailable integrations or skipped coverage explicitly.

Do not bundle changes to risk constants, authorization policy, private-data handling, or operational rollout into these structural improvements. Preserve independent rollback boundaries so a packaging or tooling regression can be reverted without reverting runtime state or research evidence.
