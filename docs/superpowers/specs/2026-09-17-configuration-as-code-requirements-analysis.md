# Configuration as Code Completion — Requirements Analysis

**Date:** 2026-09-17
**Reviewed plan:** [completion plan](../plans/2026-09-17-configuration-as-code-completion.md)
**Source baseline:** merged main `6a3d4b37c9ce24e3726765d01a6804cae1976f59`; PR 417 merged at `2026-09-17T14:06:17Z`.
**Method:** GitHub merge metadata, fetched Git objects, comparison against the earlier planning checkout `c2e6eb2`, and focused source/consumer reads. No Python or test execution. The active checkout remains unchanged; documentation edits are local.

## Verdict

The objective is clear and all six requested opportunities are represented. The original plan was not ready for unrestricted execution: two cross-component requirements were incomplete, and several proposed abstractions hid intentional differences. These have been corrected in the plan. Packets 1–7 can enter bounded implementation after the ordinary baseline checks; Packet 8 is a feasibility/design task until its coverage matrix and import strategy are established. No additional user preference is needed to begin those bounded packets when implementation is authorized.

PR 417 closes layer maps, CI matrix, firm-tier composition and shared CI setup. It does not close the remaining packets, and its merged status does not establish test acceptance for future refactors. Do not reopen its deferred Fly/packaging generators.

## Required outcomes and priorities

| ID | Requirement | Acceptance evidence |
|---|---|---|
| R1 | One authored owner for each genuinely shared configuration fact; consumers reference or compose it. | Retired-definition search plus producer-to-consumer trace; derived compatibility views contain no second literal authority. |
| R2 | Remove synchronization code only when the redundant authored sources it compared are removed. | Inventory each removed guard and the invariant still enforced by schema/behavior tests. Packaging inclusion checks remain independent verification. |
| R3 | Preserve behavior and evidence integrity. | Old/new results on independent fixtures: values/types, output ordering, CLI status/messages, scan membership, unknown-input refusal and isolated mutations. No retrospective changes to frozen research inputs. |
| R4 | Show actual net size impact. | Baseline/candidate Git blob lengths over the union of changed paths, separated into implementation, tests, generated copies and documentation. Include additions, deletions and plan/report bytes; classify renames once. |
| R5 | Preserve import and packaging boundaries. | Direct CLI, module/file-spec imports, standalone skill copy and isolated image imports; explicit image inventory and privacy checks. |
| R6 | Preserve account/risk/operational authority. | No changed numeric policy, fee eligibility, arming, permissions, deployment or skill publication. |
| R7 | Validate configuration where consumed without inventing permissive defaults. | Invalid mode/category/profile cases fail explicitly; consumer-specific fallback behavior remains where already contractual. |
| R8 | Bind verification to the actual merged base and candidate. | Launcher doctor and completed verification records with interpreter, source stability, captured reports, exit status and Docker cleanup where applicable. |

Priority order: behavioral correctness and evidence integrity; one canonical owner; removal of duplicate definitions/maintenance machinery; measured total-byte reduction. A larger result cannot be called byte savings. A proposed ownership improvement with positive net bytes gets a separate explicit disposition rather than quietly entering the savings total. No fixed savings quota is supported by the audit.

## Confirmed findings and resolutions

### F1 — Missing image inventory dependency (high)

**Trigger:** Packet 3 moves geometry into `core/instrument_specs.py` and makes the packaged slippage CLI import it.

**Evidence:** merged `tests/ops/test_c1_rail_image_manifest.py::test_ci_exact_inventory_includes_packaged_python_modules` compares Dockerfile Python paths against `scripts/c1_image_validation.sh`'s `LISTENER_FILES`; the shell also validates exact image inventory. The original plan named only Dockerfile and `.dockerignore`.

**Required result:** the new module must be present in COPY, context allow-list and shell inventory, and isolated imports must work. Updated Packet 3's footprint and Packet 7's retained checks. Removing the inventory assertion to force a pass is not an acceptable resolution.

### F2 — Shared image walker loses relative-import semantics (high)

**Trigger:** Packet 7 extracts one import walker configured only with a module-name resolver.

**Evidence:** the merged daemon test's `_repo_import_names(path)` resolves relative imports using the source file's package, unlike the listener extractor. The daemon entrypoint set now includes `book_evaluate_loop.py`; the listener includes an isolated packaged-book test added since the earlier audit.

**Required result:** profile both import-name extraction and resolution, preserving entrypoint sets and independent assertions. The revised interface includes `imported_names(path)`. Relative import, package initializer, missing dependency and isolated-import acceptance are explicit.

### F3 — Link policies cannot unify all ignore/resolution behavior (medium)

**Evidence:** skill checks have a pattern-based Git-ignore fallback, remove fenced code, classify templates/tombstones and resolve against repository or skill bundle. Root/nested checkers have different ignore-failure handling and path-shape filters. A `repo/document` switch cannot describe the skill contract.

**Resolution:** restrict shared target resolution to root/nested checks; share only equivalent primitives with skill checks. Preserve fallback, cache scope, status/message and path classification differences. Include Git-unavailable and file-spec-import tests as well as root-doc CLI coverage.

### F4 — Hook ordering is not a runtime guarantee (medium)

**Evidence:** [official Claude Code hook reference](https://code.claude.com/docs/en/hooks#hook-handler-fields), consulted 2026-09-17, specifies parallel matching handlers. Merged `.claude/settings.json` also contains a `PreToolUse` shell guard absent from the old planning checkout.

**Resolution:** preserve two independent handler objects and their matching behavior. Compare full fields and leave the shell guard/permissions unchanged. Do not combine commands serially or claim execution ordering from JSON order. Installed runner compatibility is an execution check, not authorization to invoke live hooks now.

### F5 — Newly shared modules have multiple launch contexts (medium)

**Evidence:** existing tests use `importlib.util.spec_from_file_location`; pytest's configured roots include repository/layer directories but not `scripts` as a universal import root. Standalone skill deployments must carry their own support modules.

**Resolution:** acceptance must exercise direct CLI, repository import and existing test import styles from outside the checkout where appropriate, without ambient `PYTHONPATH`. Choose a deterministic repo-local import for the narrow brief wrapper and a package-local import for the standalone skill. Never resolve a shared engine from a mutable home-directory installation.

### F6 — Interface validation and mutation behavior need explicit limits (medium)

**Evidence:** retrieval collection order differs from `HOT_FILES` documentation order; cost-model tests mutate public mappings to expose unclassified geometry and overlapping categories; fixture dictionaries differ between listener transport and HTTP/file-backed setup.

**Resolution:** ordered corpus objects follow the collector, with mode-specific limits. Bindings reject invalid categories and preserve missing classification coverage; derived views cannot become a second authoritative table. Fixture variants remain explicit, with whole-value nested overrides and independent copies; invalid-input tests bypass production validation. Scanner profiles preserve exact existing scope, including asymmetries.

### F7 — Brief consolidation is still a design decision (medium)

**Evidence:** repo and skill validators intentionally differ in supported types, CLI flags, inference and reported dispositions. Both print a closure delegation instruction; neither executes the closure checker. Their combined source size is not a measurement of removable duplication.

**Resolution:** Packet 8 first produces a coverage/import/byte decision. It may proceed only with separate profiles preserving that matrix and standalone template access. It must not silently broaden the repo checker or turn `DELEGATED`/`NOT CHECKED` into PASS. A documented infeasibility result completes the decision task, not the proposed refactor.

## Packet acceptance matrix

| Packet | Required behavioral evidence | Status after requirements corrections |
|---|---|---|
| 1 Retrieval | Exact ordered chunk sequence, catalog special rows, duplicated index coverage, filename exclusions, line/chunk limits, cold exclusions; rebuild and query through real collector. | Bounded requirements ready. |
| 2 Link policies | Root/nested/skill outputs and exits unchanged for live, missing, ignored, templated, fenced and historical references; Git-unavailable behavior retained. | Bounded requirements ready; extraction scope deliberately narrow. |
| 3 Instrument facts | Numeric/type equivalence, missing/unavailable fee refusal, category validation, MYM/MNQ geometry, isolated slippage import and complete image inventories. | Bounded requirements ready; Docker evidence owed at execution. |
| 4 Test factories | Fresh nested state, explicit clocks/arming, transport versus file-backed distinction, unchanged malformed/omission cases and independent expected payloads. | Bounded requirements ready; net savings measured after migration. |
| 5 Scan profiles | Per-tool exact membership including tracked caches, ignored local inputs, root/nested exclusions and similarly named paths; same prefix/component semantics. | Bounded requirements ready; no incidental scanner fixes. |
| 6 Hook matcher | Same matching handler objects/defaults, parallel eligibility, unrelated guard and permissions preserved; runner compatibility recorded. | Static change specified; compatibility remains an execution prerequisite. |
| 7 Image tests | Existing entrypoints and closure sets; daemon relative imports; negative missing-COPY case; isolated package and shell inventory regressions. | Bounded requirements ready after adding extraction callback. |
| 8 Brief validators | Explicit old/new coverage matrix, standalone package including templates, exact disposition/exit behavior, measured net savings. | Feasibility/design only until matrix and import implementation are specified. |

## Execution and completion boundaries

Implement from a worktree based on merge `6a3d4b3` or a verified descendant. Root checkout `c2e6eb2` is not that base. The user's local configuration-as-code instructions must travel with the work without replacing merged main's newer verification-record instructions.

The plan remains scoped to configuration and necessary consumer extraction. General parser fixes, scanner hardening, new instrument support, universal policy engines and live deployment are excluded. Preserve known differences and report an independently discovered defect separately; a behavior-preserving refactor must not quietly repair it.

Completion requires per-packet implementation or justified deferral, confirmed contracts for accepted work and honest accounting. Unavailable environments mean verification pending, not PASS or an automatic design deferral. Existing equality machinery is removable only when it maintained duplicate authorship; schema, packaging and historical expected-value checks still establish independent facts.

No implementation tests were run for this requirements analysis. No runtime correctness, savings total or deployment readiness is asserted. Documentation was checked for scope coverage and the affected producer/consumer requirements re-traced after correction.
