# First Passage Architecture Improvement Roadmap

**Status:** Proposed implementation sequence; documentation only.

**Goal:** Strengthen the monorepo's enforceable boundaries, dependency-aware validation, runtime interfaces, and service verification.

**Companion:** [Installable core implementation plan](2026-09-10-installable-core.md). Its PR 1 / PR 2 labels refer to the two packaging deliveries, not the total number of changes in this roadmap.

## Delivery order

| Order | Deliverable | Dependency / acceptance boundary |
|---|---|---|
| 1 | Complete import-boundary resolution | Independent; land before import-layout changes |
| 2 | Dependency-aware research CI triggers | Independent; land before changing shared core behavior |
| 3 | Installable core wheel | Execute the companion plan's first slice |
| 4 | Offline service harness and rail artifact consumption | Establish the service baseline before switching the rail image to the wheel |
| 5 | Structured authority interfaces | Separate change preserving current denylist behavior |
| 6 | Explicit Monte Carlo compatibility exports | Separate change preserving supported historical imports |

Each deliverable should be a separately reviewable change with its own regression evidence. This roadmap does not authorize production deployment or alter strategy/risk policy. Namespace modernization remains deferred as described in the packaging plan.

## 1. Complete import-boundary resolution

**Observed gap:** `scripts/check_boundaries.py` indexes immediate children of `core/`, `lab/`, and `ops/`, then resolves imports by their first component. A read-only probe recognized `from research_utils import step0_battery` as lab-owned, but returned no targets for `from lab.research_utils import step0_battery`, `from ops.c1_rail import c1_rail_listener`, or `import c1_rail_listener`. These are resolver coverage gaps, not evidence that those illegal edges currently exist in production.

**Files:** `scripts/check_boundaries.py`, `tests/test_check_boundaries.py`, `scripts/repo_map_layers.yml` if ownership changes, and `REPO_MAP.md`.

- [ ] Add synthetic fixture tests putting each import form in a forbidden source layer; require detection of the intended target layer.
- [ ] Resolve both root-qualified names and the documented flat import roots, including `ops/c1_rail`. Resolve `from package import module` against actual module paths rather than assuming the first token is the complete identity.
- [ ] Resolve relative imports from the importing file's package context; remove the blanket assumption that every relative import is same-layer. Test a multi-level relative import that crosses a layer boundary.
- [ ] Preserve alias and lazy-import coverage. Reject ambiguous first-party resolution with candidate paths instead of silently choosing one. Keep third-party imports distinct from unresolved first-party paths.
- [ ] Keep the existing legal-edge set unchanged. Document dynamic imports and filesystem reads as separate coverage limitations; do not claim an AST import scanner validates those dependencies.
- [ ] Run `python -m pytest tests/test_check_boundaries.py -q`, `python scripts/check_boundaries.py`, and `python scripts/check_repo_map_layers.py`.

**Acceptance:** All supported syntactic forms of the same dependency receive the same layer verdict; allowed edges still pass; forbidden edges and ambiguity fail. If the improved resolver exposes existing violations, classify and fix those explicitly rather than expanding the allowed edges.

## 2. Trigger research validation when shared dependencies change

**Observed gap:** `.github/workflows/validation-controls.yml` triggers on `lab/**` and its own workflow file. Lab code consumes core code, so a core-only change can skip the tests located under `lab/`. The main `tests/` job still runs; the gap is the omitted consumer suite.

**Files:** `.github/workflows/validation-controls.yml`, `tests/test_validation_workflow_paths.py` (new), and `scripts/README.md` if the documented invocation changes.

- [ ] Add `core/**`, `pyproject.toml`, `requirements*.lock`, and `requirements-research.txt` to both push and pull-request filters. Include `scripts/layer_bootstrap.py` as shared import setup. Retain the current lab and workflow triggers.
- [ ] Inspect the workflow's actual setup and lab imports for other shared governance executables. Add only those concrete dependencies; do not trigger this job for every documentation edit.
- [ ] Add a semantic trigger test using representative changed paths: core engine, core utility, lab source, dependency lock, bootstrap script, workflow file, and an unrelated Markdown file. Test both event filters so they cannot drift independently.
- [ ] Preserve explicit exclusions for archived/manual campaigns. This change does not make every historical experiment runnable or promote dormant checks to live gates.
- [ ] Run the new trigger tests and the existing validation-controls job's exact command in its supported environment. Verify on GitHub that a shared-source change schedules the consumer job and an unrelated docs-only change does not.

**Acceptance:** A change to shared executable code or dependency configuration cannot silently bypass the relevant research suite. Keep the trigger list small and explicit until dependency complexity justifies automation.

## 3. Separate structured authority from prose formatting

**Observed gap:** `ops/recall/guard.py::load_denylist` regex-reads Python source and historical values from `CLAUDE.md`. Formatting and prose placement therefore affect a machine-consumed guard. Existing root instructions explicitly preserve a historical statement for that parser.

**Files:** `ops/recall/guard.py`, its existing tests (locate by `load_denylist` / `Denylist`), a historical-record JSON artifact under `docs/`, and the historical-record/root-document owners. Read production sources before specifying any risk-related values, following Rule 0.

- [ ] Capture the current denylist values, source provenance, and representative accept/reject outcomes as regression fixtures before changing extraction.
- [ ] For code-owned values, consume their canonical exported definitions through a narrow read-only adapter. Keep the adapter outside core if it also consumes governance artifacts; never introduce a core-to-governance dependency.
- [ ] Give historical values a schema-versioned record with explicit historical scope and provenance. Validate required fields and reject malformed or missing required sources with an explicit error; do not silently return an incomplete guard.
- [ ] Switch the consumer and document owner together. Preserve existing numeric normalization and context-matching behavior. Do not reinterpret historical records as current operating authority.
- [ ] Test prose reordering and formatting changes: they must no longer change the denylist. Test malformed records and missing sources, and compare the full behavioral fixture against the old extractor.
- [ ] Remove the root document's formatting constraint only after the new consumer passes equivalence tests. Keep documentation pointing to the canonical owner rather than adding another maintained copy.

**Acceptance:** Machine behavior is independent of narrative wording, while the accepted/rejected note corpus remains unchanged. Review any desired behavior change separately from this interface migration. Define the exact schema and adapter API in this slice's design before implementation.

## 4. Verify the assembled rail through an offline service harness

**Observed gap:** The rail HTTP adapter and listener explicitly describe socket/process wiring as untested. Helper tests cannot prove the assembled service starts and preserves behavior over real HTTP and restart.

**Files:** `tests/ops/test_c1_rail_service.py` (new), reusable fixtures under `tests/ops/`, `ops/c1_rail/c1_rail_http_server.py` only if a narrow transport-injection seam is needed, and the deployment-image checks in the companion plan.

- [ ] Start the actual service process on loopback with an ephemeral port, a temporary configuration, and synthetic state. Wait for readiness with a bounded deadline; capture diagnostic output and terminate the process in test cleanup, including failure paths.
- [ ] Substitute an in-process or loopback fake downstream transport. Restrict external networking. Do not use production credentials, endpoints, state, or an actual broker.
- [ ] Exercise health, authentication failures, malformed payloads, and missing/invalid state through HTTP. Assert response semantics and side effects, including zero downstream calls on refused paths.
- [ ] Add concurrent-request cases that assert ledger validity and documented shared-state invariants. Do not invent exactly-once delivery guarantees that the system does not provide.
- [ ] Restart against the same temporary state and verify documented recovery/refusal behavior. Reuse existing telemetry and transport-unknown contracts as the expected behavior rather than designing new retry policies.
- [ ] Run the same behavioral scenarios against the current layout and the wheel-based image. Keep pure tests as fast feedback; the service harness covers process assembly.

**Acceptance:** The real HTTP/process path passes offline with bounded startup/shutdown, valid persisted state, and no external side effects. Establish this baseline before accepting the packaging plan's rail-image migration. Detailed fixture schemas and expected responses belong in that slice's implementation plan.

## 5. Freeze an explicit Monte Carlo compatibility interface

**Observed gap:** `core/portfolio_mc.py` re-exports every non-dunder name from `mc.modes`, including private helpers needed by historical scripts. Internal changes can consequently change the facade's apparent API.

**Files:** `core/portfolio_mc.py`, `core/mc/modes.py` if required, a facade compatibility test under `tests/core/`, `core/README.md`, and individually identified active consumers.

- [ ] Inventory current imports and reflective uses of `portfolio_mc`, including private helpers. Use the research catalog and historical retrieval instructions when classifying consumers; an empty ordinary search is not proof of no consumer.
- [ ] Record the current compatibility export set and intentionally supported monkeypatch/global behavior, including the facade-owned simulation count forwarded by `_run_seeds`.
- [ ] Replace unrestricted `dir(_modes)` export copying with an explicit compatibility export list. Preserve required object identity and wrapper behavior; `__all__` alone is insufficient because it does not constrain direct attribute access or remove the current copying loop.
- [ ] Add regression tests for existing named imports, deliberately supported private helpers, the `_run_seeds` forwarding contract, and absence of an unrelated newly added internal symbol from the facade.
- [ ] Route new and actively maintained consumers to focused `mc` modules in small batches. Keep legacy imports working; do not rewrite archived campaigns solely to enforce a modern interface.

**Acceptance:** Internal symbols added to `mc.modes` no longer become facade exports automatically. Supported historical callers and synthetic engine regressions continue to pass. Any deliberate compatibility removal requires its own consumer migration and review.

## Scope and verification

This document records the five architecture improvements alongside the existing packaging plan. It is a roadmap with concrete acceptance boundaries, not a claim that implementations or tests already exist. Each follow-up design must name exact interfaces and executable regression cases before code changes begin. Run relevant tests and the repository gate manifest for each implementation; report unavailable integrations or skipped coverage explicitly.

Do not bundle changes to risk constants, authorization policy, private-data handling, or operational rollout into these structural improvements. Preserve independent rollback boundaries so a packaging or tooling regression can be reverted without reverting runtime state or research evidence.
