# Installable Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a tested, installable shared-code artifact within the monorepo, then make the rail consume that artifact without changing operational behavior.

**Architecture:** Keep `core/`, `lab/`, and `ops/` as the source ownership boundaries. Add a `first-passage-core` wheel with explicit public-source membership and existing import names; test it outside the checkout. Introduce wheel consumption into the rail build only after artifact and runtime compatibility tests pass.

**Tech Stack:** Python 3.11+, setuptools, wheel, pip, pytest, existing gate manifest, Docker.

**Spec:** The proposed design in this document is the specification for the first slice. Later slices below are a sequenced roadmap, not independently approved execution specifications.

**Status:** Proposed for review. Planning only; no application changes, dependency installation, publication, or deployment performed.

**Related roadmap:** [Architecture improvements](2026-09-11-architecture-improvements.md) sequences boundary-checker coverage and dependency-aware CI ahead of packaging, adds the service verification baseline for the rail migration, and defines separate authority-data and compatibility-API follow-ups. PR 1 / PR 2 below are the two packaging deliveries within that broader sequence.

## Design decision

Use an incremental packaging migration. First make code distributable without moving it or renaming imports. Then prove the deployment can consume the artifact. Namespace and state-path modernization follow separately if their benefits justify the migration.

Alternatives considered:

| Approach | Benefit | Cost / decision |
|---|---|---|
| Package current import names | Small compatibility surface; code can stay byte-identical | Retains generic names such as `lib` and `mc`; recommended for the first internal release |
| Rename everything to `first_passage.core.*` immediately | Clear public namespace | Cross-repository import, scanner, test, script, and path migration; defer |
| Extract a new repository first | Independent access and release ownership | Adds version coordination before artifact contracts exist; reject for this work |

The wheel is internal and is not published to PyPI. A distribution name is not a Python import namespace. `first-passage-core` initially provides imports such as `firm_rules`, `lifecycle`, `lib.validation`, and `mc.simulation`. Do not load the same source under both flat and qualified names: module globals and class identity could diverge.

## Evidence and constraints

- Root `pyproject.toml` currently installs dependencies only (`packages = []`, `py-modules = []`). Keep that development setup working during the first slice.
- `scripts/check_boundaries.py` owns the layer contract; `scripts/repo_map_layers.yml` mirrors it. Keep `core` independent of other internal layers and keep `lab ↔ ops` forbidden.
- `deploy/c1_rail/Dockerfile` currently copies four core modules and four `lib` modules. Its runtime is standard-library-only. The daemon has its own Dockerfile and does not currently require the core wheel.
- `tests/ops/test_c1_rail_image_manifest.py` checks source COPY coverage. A wheel migration must replace that assumption with installed-artifact coverage, not remove the protection.
- `core/lifecycle.py` and `core/dd_protection.py` resolve default state beside their source. `core/mc/modes.py` resolves default datasets relative to its source. Installing into site-packages changes those locations; it does not make stateful CLIs automatically portable.
- `ops/c1_rail/c1_sizing_host_reference.py` receives explicit state paths and rejects missing lifecycle entries. Do not substitute the core helper's missing-state behavior.
- `ops/c1_rail/c1_rail_arm.py` resolves the acceptance JSON and validator from the application tree. They remain explicit deployment artifacts with their current semantics.
- Private strategy bodies, vendor inputs, local state, credentials, and historical research are not package inputs. No package discovery across `core/strategies/` or `core/data/`.

## Global Constraints

- Python 3.11 is the compatibility floor; verify the package on Python 3.11 and 3.12.
- Windows and Linux installation must work.
- Preserve public core source bytes, risk constants, arithmetic, and state defaults in the first slice.
- Preserve existing imports and checkout-based tests in the first slice.
- The base wheel declares no third-party runtime dependencies; scientific functionality uses explicit extras.
- No state, datasets, strategy bodies, or governance artifacts inside the core wheel.
- A normal installed-package smoke test must run outside the checkout with `PYTHONPATH` removed and must verify module origins.
- No production deployment, arming, credential use, or broker traffic is part of implementation verification.
- Reuse `scripts/gates.yml` for blocking gate composition; do not create a competing gate registry.

## Delivery sequence

1. **PR 1: Build and verify the core wheel.** Independently useful: a clean environment can install and import shared code, and CI catches incomplete or contaminated artifacts. Detailed tasks follow.
2. **PR 2: Consume the wheel in the rail image.** Preserve existing state and governance paths. Build and test the image offline; operational rollout is separate.
3. **PR 3, conditional: Make installed CLIs and imports fully portable.** Explicit resource/state interfaces and a project namespace require a separate design. Do not make this a prerequisite for the first two deliveries.

## First-slice file map

| File | Responsibility |
|---|---|
| `core/pyproject.toml` (new) | Core distribution metadata, explicit module/package names, optional scientific dependencies |
| `scripts/build_core_wheel.py` (new) | Build from a temporary directory containing only approved source files; verify resulting wheel membership |
| `tests/packaging/test_core_wheel.py` (new) | Artifact contents, clean install, module-origin, dependency, and missing-file regression tests |
| `requirements-build.lock` (new) | Hash-locked build dependencies, generated by the repository's established lock workflow |
| `scripts/gates.yml` | Admit the bounded packaging tests on relevant changes |
| `.github/workflows/gate-manifest.yml` | Install the build lock before the manifest invokes packaging tests |
| `.github/workflows/tests.yml` | Provide build dependencies for the new tests and add package platform coverage |
| `core/README.md`, `REPO_MAP.md`, `scripts/README.md` | Describe the distribution and the distinction between installable APIs and checkout-dependent CLIs |

New build tooling is governance-owned and must not import the core application. It may inspect and copy source files. If added to `SCRIPTS_LAYER`, update the YAML mirror in the same change; otherwise its existing governance default is appropriate. Regenerate the REPO_MAP scripts table when adding the script.

### Task 1: Build an explicitly bounded wheel

**Consumes:** Existing public sources under `core/`.

**Produces:** `python scripts/build_core_wheel.py --output-dir <directory>`; exactly one `first_passage_core-*.whl` plus `core-wheel.json` recording wheel name, SHA256, source revision, dirty-tree indicator, and source-file hashes. A dirty build is marked, not misrepresented as the clean commit. Deployment builds later require a clean source revision.

- [ ] Add the content test first. It must assert exact Python member equality, rather than merely searching for prohibited extensions.
- [ ] Use this proposed setuptools configuration in `core/pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "first-passage-core"
version = "0.1.0"
requires-python = ">=3.11"
description = "Shared First Passage engines and controls"
dependencies = []

[project.optional-dependencies]
research = ["numpy>=2.0,<2.5", "pandas"]
analysis = ["numpy>=2.0,<2.5", "nolds<0.6", "setuptools<81"]
mc = ["numpy>=2.0,<2.5", "pandas", "joblib"]
report = ["pandas", "quantstats"]

[tool.setuptools]
include-package-data = false
py-modules = [
  "bar_export_loader", "csv_parser", "dd_geometry", "dd_protection",
  "firm_rules", "historical_challenge", "lifecycle", "portfolio_mc",
  "tv_export_loader", "tv_schema"
]
packages = ["lib", "mc"]
```

- [ ] The build script owns one explicit source-file tuple: the ten modules above; `lib/atomic_io.py`, `lib/correlation.py`, `lib/file_lock.py`, `lib/mvd.py`, `lib/nonlinear.py`, `lib/regime_bootstrap.py`, `lib/tearsheet.py`, `lib/validation.py`; and `mc/__init__.py`, `mc/ingest.py`, `mc/modes.py`, `mc/preflight.py`, `mc/simulation.py`. Preserve `lib` as the existing implicit namespace; do not invent an initializer in application source.
- [ ] Copy only that tuple, the build metadata, and the repository license into a temporary build directory. Do not use recursive copies or VCS package discovery. A missing listed file is a hard error before build.
- [ ] Generate `requirements-build.lock` for setuptools and wheel with hashes using the current repository workflow. Use the lock in CI and the build environment; the broad metadata range is not the reproducibility mechanism.
- [ ] Build with `sys.executable -m pip wheel --no-deps --no-build-isolation --wheel-dir <temporary-output> <staged-source>`. Check the wheel before writing final outputs. Refuse ambiguous/multiple wheel results and refuse overwriting an existing output artifact silently.
- [ ] Verify every non-metadata wheel member is in the exact Python allow-list and that every listed source matches its wheel member byte-for-byte. Permit only expected `.dist-info` metadata and license files beyond the source list; reject traversal paths and unexpected data members.
- [ ] Test with synthetic private decoys in a temporary source fixture: `strategies/private.py`, `data/vendor.csv`, `lifecycle_state.json`, `.env`, and an unlisted `lib/private.py`. None may enter staging or the wheel. Do not create decoys in the actual private directories.
- [ ] Test a listed source missing from the fixture: the builder must fail rather than emit a partial wheel.
- [ ] Run `python -m pytest tests/packaging/test_core_wheel.py -q` and commit only this task's files when passing.

### Task 2: Prove installed behavior independently of the checkout

**Consumes:** The validated wheel and build receipt from Task 1.

**Produces:** Installed-artifact tests that cannot pass through pytest's checkout `pythonpath` settings.

- [ ] Create a fresh temporary venv without system site packages. Install the absolute wheel path using `pip install --no-index --no-deps <wheel>`. Run subprocesses from a separate temporary directory with `PYTHONPATH` removed and Python `-I` enabled.
- [ ] Use this probe for the standard-library surface:

```python
import importlib
import importlib.metadata
import importlib.util
from pathlib import Path
import sys

assert importlib.metadata.version("first-passage-core") == "0.1.0"
for name in ("firm_rules", "historical_challenge", "lifecycle",
             "dd_protection", "lib.atomic_io", "lib.file_lock",
             "lib.mvd", "lib.validation"):
    module = importlib.import_module(name)
    assert Path(module.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
assert importlib.util.find_spec("numpy") is None
assert importlib.util.find_spec("pandas") is None
```

- [ ] Assert wheel metadata has no unconditional `Requires-Dist` entries. Optional dependencies must have extra markers. Do not use a development environment's installed dependencies as proof of the base contract.
- [ ] In a second clean environment with scientific dependencies from existing hashed locks, install the same wheel and import `portfolio_mc`, `mc.preflight`, all public core modules, and all `lib` modules. Exercise the nonlinear helper separately with its analysis extra dependencies. Check metadata for the lazy `joblib` and `quantstats` dependencies under the `mc` and `report` extras; use offline synthetic parallel/report fixtures if those optional features are exercised.
- [ ] Run the synthetic MC regression suite against the installed artifact: copy `tests/core/test_mc_synthetic_engine.py` and only its required fixtures into a temporary test tree, use a temporary pytest config with no source `pythonpath`, and assert imported core module origins remain under the venv. Keep checkout tests as an additional test path, not as a substitute.
- [ ] Compare pure, synthetic API results for checkout and wheel imports in separate subprocesses. Reuse the regression suite's input cases; compare structured results, not console output. No vendor data is needed.
- [ ] Verify no state/data files are embedded or created merely by importing. Explicitly document that source-relative CLI defaults are unchanged and installed stateful CLIs are not yet a supported workflow.
- [ ] Run the packaging suite on Windows and Linux under Python 3.11 and 3.12; commit after the relevant checks pass.

### Task 3: Admit the artifact checks and document consumption

**Consumes:** Tasks 1–2.

**Produces:** A reproducible wheel build and a packaging regression gate in the existing workflow.

- [ ] Add a `core-package` path-conditional gate with the command below and a trigger covering `core/`, root `pyproject.toml`, `requirements*.lock`, `scripts/build_core_wheel.py`, `tests/packaging/`, `scripts/gates.yml`, and the affected CI workflows.

```yaml
cmd:
  - python
  - -m
  - pytest
  - tests/packaging/test_core_wheel.py
  - -q
```

- [ ] Install `requirements-build.lock` in both current CI jobs that may run these tests. Add the four-cell package platform matrix to the existing tests workflow. Reuse the current pinned checkout/setup-python actions. Use no production secrets.
- [ ] Keep the root dependency project and the ordinary test suite operational. Do not add a same-named dependency resolved from public PyPI; local consumers install the built artifact explicitly.
- [ ] Document build, local wheel install, optional scientific dependencies, receipt verification, and source-relative CLI limitations. Describe generic module names as a compatibility phase, not the eventual external API.
- [ ] Run `python scripts/check_repo_map_scripts_table.py --write`, then its `--check` mode. Update the affected documentation without rewriting root instructions or current operational state.
- [ ] Run `python -m pytest tests/packaging/test_core_wheel.py tests/test_check_boundaries.py tests/ops/test_c1_rail_image_manifest.py -q`, the existing core regression suite, and `python scripts/gate_manifest.py --tier check`. Record environmental skips or pre-existing failures explicitly.
- [ ] Verify `git diff -- core` contains only the proposed metadata/documentation additions; existing Python source bytes must be unchanged. Commit the gate and documentation task.

## Second-slice design: rail artifact consumption

Write the detailed execution plan after PR 1 establishes the artifact contract. The intended changes are bounded to these surfaces:

- `deploy/c1_rail/Dockerfile` and `.dockerignore`: install the validated wheel instead of individually copying core source. Preserve the explicit ops files, acceptance JSON, and schema validator.
- `scripts/build_core_wheel.py` or a separate governance build-context script: create an isolated deployment context from approved files. Build receipts must identify the same clean revision as ops and acceptance inputs; verify the wheel SHA256 before installation. Do not upload an arbitrary contents wildcard from a local output directory.
- `tests/ops/test_c1_rail_image_manifest.py`: change the coverage model to core wheel members plus explicit ops COPY members. Retain the historical missing-transitive-import regression. Add arm and slippage CLI coverage alongside server/listener coverage.
- `deploy/c1_rail/README.md`: document the artifact-based build and rollback by complete previous image, not by downgrading only the wheel.

For the first image migration, install the wheel with `pip install --no-index --no-deps --target /app/core <wheel>`. This deliberately preserves core-relative paths and the current ops bootstrap. It proves artifact consumption without simultaneously changing state locations. The wheel contains additional public scientific source modules, but scientific dependencies are not installed or imported by the rail. Acceptance requires an actual image test proving the runtime import closure remains standard-library-only.

The M1 JSON stays at `/app/docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`; its validator remains at `/app/scripts/validate_c1_monitoring_acceptance.py`. Neither belongs in the core wheel. Never rewrite evidence/status to make a packaging test pass. Verify provenance logic against the installed layout before merging.

Image acceptance tests must run without network access and with temporary synthetic configuration/state. Exercise startup, invalid/missing state, incomplete/forged M1 records, and the operator CLIs' read-only paths. Missing lifecycle entries must still refuse sizing; missing/invalid acceptance must still refuse arming. Reuse current behavioral tests and compare old/new images' structured responses. Do not call a production endpoint or arm a host.

The signal daemon remains independent. Its existing build must keep passing when the root build-context rules change; do not add a core dependency it does not need.

## Deferred design: portability and namespacing

Only pursue after the installed artifact and image checks provide a baseline. Inventory every `__file__` resource/state lookup; distinguish immutable resources from mutable operator state. Introduce explicit caller-owned paths with compatibility adapters, then migrate callers in batches. A namespaced import migration must update the AST boundary resolver and negative boundary tests before consumers change. Avoid alias shims that import the same source twice.

Do not split repositories, package lab campaigns, add a package registry, or create independent service releases merely to complete this improvement. Those are later choices tied to actual consumers and ownership needs.

## Completion and rollback

PR 1 is complete when the wheel's content is bounded, source bytes match, clean installs pass on the supported platforms, scientific synthetic tests use installed code, and the existing checkout checks still pass. PR 2 is complete when the built image consumes that exact artifact and its offline behavioral checks pass. Neither completion claim implies a production rollout.

Each PR must be independently revertible. Reverting PR 1 removes additive build tooling without application source rollback. Reverting PR 2 restores the previous deployment build; preserve the previous full image identity for any separately authorized operational rollback. Never revert or overwrite mutable runtime state as part of package rollback.

## Packaging references

- [Setuptools pyproject configuration](https://setuptools.pypa.io/en/stable/userguide/pyproject_config.html): explicit modules/packages and metadata.
- [Setuptools distribution contents](https://setuptools.pypa.io/en/stable/userguide/miscellaneous.html): why artifact inspection and staging are needed in addition to disabling package data.
- [pip install reference](https://pip.pypa.io/en/stable/cli/pip_install/): local wheel installation, `--no-index`, `--no-deps`, and `--target`.
