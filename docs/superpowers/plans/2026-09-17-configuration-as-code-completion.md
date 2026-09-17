# Configuration as Code Completion Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the configuration deduplication audit by removing repeated definitions and the machinery that synchronizes them, preserving observable behavior and reporting honest net byte changes.

**Architecture:** Use small immutable configuration objects owned by the subsystem that consumes them. Share processing only where configuration captures real differences; retain independent verification, historical evidence and public entrypoints. The coordinating implementer owns integration and the final accounting; the packets below are independently acceptable changes, not one mandatory bulk refactor.

**Tech Stack:** Python 3.11+, existing operations launcher and pytest, PowerShell wrappers, existing JSON hook configuration. No new configuration framework or dependencies.

**Spec:** User's configuration-as-code instruction in `AGENTS.md`, the two follow-up opportunity audits and final byte-saving pass in this task, reconciled against [PR 417](https://github.com/Joshua-Asante/first-passage/pull/417). This is a planning deliverable, not implementation or deployment authorization.

**Requirements review:** [2026-09-17 requirements analysis](../specs/2026-09-17-configuration-as-code-requirements-analysis.md), against merged main `6a3d4b37c9ce24e3726765d01a6804cae1976f59`. Read its packet acceptance matrix with this plan. Packets 1–7 have bounded requirements; Packet 8 remains a design/feasibility decision before implementation.

## Global Constraints

- Define reusable configuration once; consumers reference or compose it. Overrides must be explicit and resolved configuration validated at consumption.
- Keep secrets outside versioned configuration. Preserve deployment configuration identity/version whenever deployment inputs change.
- Preserve accepted policy behavior, numeric values and types, CLI contracts, failure severity, scan scope, ordering and independence of expected test results.
- Do not delete independent tests or frozen expectations merely to meet a byte target. Remove comparisons only when they compare redundant authored sources that no longer exist; retain schema and behavioral checks.
- Do not create generators with tracked duplicate output unless the measured benefit justifies the extra machinery. Ordinary Python objects are configuration as code.
- Before project Python work, run `.\fp.ps1 doctor` from the checkout being tested. Use `.\fp.ps1 python ...`, `.\fp.ps1 test`, `.\fp.ps1 test-ops`, and `.\fp.ps1 check`. Without PowerShell 7.3+, use `python -I scripts/fp.py <command>`.
- Use the checkout's own launcher; do not bypass an environment validation failure. Child Python processes use `sys.executable`. Keep the separately pinned research environment separate.
- Report tested revision/working-tree state, command, interpreter and actual results. Disclose pre-existing failures and skips.
- Preserve merged main's launcher evidence requirements: cite `.cache/fp-verification/.../record.json`, require completed status, exit zero, stable source, complete capture and valid expected reports; require successful Docker cleanup where applicable. Keep source/Git state unchanged during each recorded run. Use `tools/local_verification/run.ps1` for Docker sequence checks.
- New shared modules must work through direct script execution, repository imports and existing file-spec test imports without relying on a developer's `PYTHONPATH`. Preserve intentional monkeypatch seams or replace tests with equivalent independent mutation cases; frozen records do not imply every existing public mapping can become immutable without review.
- Preserve `core`/`lab`/`ops` import boundaries. Reusable instrument facts belong in `core`; governance helpers belong in `scripts`.
- Preserve the existing modified `AGENTS.md` and unrelated untracked work. No account, credentials, live service, skill installation or arming changes are part of this plan.

## Baseline and PR 417 reconciliation

Initial planning reads used local checkout `c2e6eb2cbe159b60fdff7873b9e96aef943c46df`. Requirements analysis confirmed PR 417 **MERGED** at `2026-09-17T14:06:17Z`, merge commit `6a3d4b37c9ce24e3726765d01a6804cae1976f59`. `origin/main` was fetched to that commit and relevant source inspected with `git show`; the working checkout was not changed. Use this merged baseline or a verified descendant. This analysis does not independently certify PR 417's test claims.

| Earlier finding | Disposition for this plan |
|---|---|
| Layer-map authority and synchronization checker | Covered by PR 417; consume its YAML/schema approach, do not rebuild it. |
| Image-validation workflow matrix | Covered by PR 417; preserve its matrix/check names. |
| Firm-tier composition | Covered by PR 417; preserve independent typed expectations and account-product distinctions. |
| Shared CI Python setup | Covered by PR 417; no duplicate setup action. |
| Fly hosting profile | Remains deferred: generator plus tracked outputs adds machinery for little repetition. |
| Packaging manifest/generator | Remains deferred: preserve explicit privacy allow-list and Dockerfiles. Sharing test machinery below is a separate change. |

PR 417 reports smaller repeated definitions but larger total tracked source after guards and records. Its accounting is a warning against treating gross deletions as net savings, not a reason to remove its correctness checks.

### Entry gate and accounting

- [ ] At execution, verify the base contains merge `6a3d4b37c9ce24e3726765d01a6804cae1976f59`. Create an isolated execution worktree using the worktree skill. Do not copy the old checkout's files over newer implementations. Carry forward the user's configuration-as-code instructions without overwriting newer launcher/evidence instructions in `AGENTS.md`.
- [ ] Re-read each packet's files on that base; close already-resolved findings without reimplementation. Inspect applicable `AGENTS.md` files.
- [ ] Run the launcher doctor, relevant focused baseline suites and the standard check gate. Record existing failures once in the execution record.
- [ ] Capture baseline bytes from Git blobs, not platform-dependent checkout line endings. For each changed path, compare UTF-8/raw blob lengths at the packet's base and candidate; count added files in full and deleted files as zero. An execution helper may read blobs with `subprocess.check_output(["git", "show", f"{revision}:{path}"])` using the launcher.
- [ ] Record four categories: production/configuration; tests/fixtures; generated or packaged copies; documentation/records. Include this plan in program-level accounting, separately from each implementation packet. Report gross removed bytes and net total; do not count worktree copies, caches or compression gains.

**Acceptance rule:** A byte-saving packet must reduce total changed tracked bytes after required validation code. A byte-neutral or larger consolidation may still improve ownership, but must be labeled as such and presented separately rather than counted as savings. Stop a speculative abstraction when its overhead exceeds its benefit; record a justified deferral as its disposition.

## Packet 1 — Retrieval corpus objects

**Outcome:** Changing one source declaration changes the collector's source selection and any retained internal corpus inventory; no hand-synchronized `HOT_FILES` list remains.

**Files:** modify `scripts/repo_retrieve.py` and `tests/test_repo_retrieve.py`. Keep objects in the existing module unless reuse warrants a separate file.

**Proposed interface:** frozen `CorpusSource(pattern: str, mode: str, limit: int | None = None, exclude_names: tuple[str, ...] = (), omit_section: str | None = None)`; ordered `CORPUS_SOURCES`; private `_collect_source(repo: Path, source: CorpusSource) -> list[dict[str, str]]`. Keep `collect_chunks(repo)` and returned `path/heading/text` fields unchanged. `mode` accepts only `catalog`, `heading_h2`, `heading_h3`, `header_lines`.

The ordered declarations follow `collect_chunks`, not the differently ordered documentation-only `HOT_FILES`: catalog, brief index, rejected candidates, sessions, state, ADRs, closures, top-level briefs, programs, audits, methodology, specs. `limit` means chunks for heading modes and lines for header mode. ADR filename exclusions remain case-insensitive. Validate mode/limit combinations once at consumption. Do not add a new displayed inventory feature: the existing inventory is an internal declaration.

**Contract:** declarations produce source selection, existing chunk helpers produce chunks, and existing rebuild/search code owns SQLite persistence. Preserve ordered chunks, duplicates already produced by overlapping inputs, missing-file behavior, catalog ACTIVE/HOLD row extraction after omitting In flight, newest 24 session chunks, ADR INDEX/TOMBSTONES exclusions, 20-line closure excerpts and 24-line ordinary excerpts. Cold archives remain excluded. Do not change ranking or index staleness behavior.

- [ ] Add a compact synthetic-corpus regression to `tests/test_repo_retrieve.py`: distinct marker text for every source category, an omitted catalog section, 25 session chunks, excluded ADR names and cold paths. Assert expected chunk contents/order and truncation independently of `CORPUS_SOURCES`.
- [ ] Run `.\fp.ps1 python -m pytest tests/test_repo_retrieve.py -q` before editing; record the baseline. Add rejection cases for unsupported mode and nonpositive limits with the new interface.
- [ ] Replace repeated collection branches with the ordered source objects and one dispatcher, retaining the special catalog handler. Derive `HOT_FILES` from the objects if external callers need it; otherwise remove it after checking references.
- [ ] Run the same suite and compare old/new chunk sequences on the synthetic corpus. Confirm rebuilding and querying still exercise the actual collector. Measure net bytes.

## Packet 2 — Link-checker policies

**Outcome:** Common link parsing and ignore handling have one owner; root-doc, nested-doc and skill checks retain their distinct contracts.

**Files:** create `scripts/link_policy.py`; modify `scripts/check_root_doc_liveness.py`, `scripts/check_md_relative_links.py`, `scripts/check_skill_refs.py`; extend `tests/test_check_md_relative_links.py`, `tests/test_check_skill_refs.py`, `tests/test_check_skill_refs_navdirs.py`; create focused `tests/test_link_policy.py` only for cross-consumer cases not covered there.

**Proposed interface:** frozen `LinkPolicy(extensions: tuple[str, ...], require_path_shape: bool, resolution: str)` with `resolution` restricted to `repo` or `document`; shared markdown extraction and historical-line patterns; `link_target(doc: Path, repo: Path, target: str, policy: LinkPolicy) -> Path`. Keep CLI severity, messages and skill-specific reference classification in their owners. Shared extension base plus explicit `.txt`/`.html` additions reproduces current lists.

**Contract:** callers supply document text/location and policy; the common module resolves ordinary markdown links; consumers decide scope and severity. Skill inline-code, template, tombstone, vendor-data and bundled-asset rules remain explicit skill behavior, not a universal permissive fallback. Root-doc missing links still fail; nested default warnings and `--strict` behavior stay unchanged.

Scope correction: share ignore plumbing only where semantics match. Skill checks have a `.gitignore`-pattern fallback when Git is unavailable, while the root/nested helpers return false; keep that difference. Preserve Git exit-code handling, case/URL treatment, fenced-code handling and the skill's repo-or-bundle resolution. `link_target` serves root/nested checks only; the skill resolver stays separate. Validate `resolution` before use, and keep ignore caches repository-scoped. Add a direct root-doc CLI case to the focused acceptance set.

- [ ] Capture existing expectations for relative links, anchors, URL/mailto/tel, titles, historical retrieval lines, ignored missing files, malformed/non-path tokens, skill references and missing scripts. Preserve each consumer's differing interpretation instead of normalizing it away.
- [ ] Run `.\fp.ps1 python -m pytest tests/test_check_md_relative_links.py tests/test_check_skill_refs.py tests/test_check_skill_refs_navdirs.py -q`.
- [ ] Extract only demonstrated shared parsing/configuration; retain consumer-specific loops if merging them requires many switches. Delete duplicated constants and helper bodies actually replaced by imports.
- [ ] Run those suites plus `tests/test_link_policy.py` if created. Compare each old/new CLI's output and exit status on the same temporary repository. Verify importing one checker does not execute another check or widen scope. Measure net bytes including the helper.

## Packet 3 — Instrument facts and explicit commission bindings

**Outcome:** Shared instrument geometry is defined once; research commission classification and operations leg mappings compose that geometry without importing across forbidden layers.

**Files:** create `core/instrument_specs.py`; modify `lab/discovery/cost_model.py`, `ops/c1_rail/c1_rail_slippage.py`; extend `tests/test_cost_model.py`, `tests/ops/test_c1_rail_slippage.py`. Update `deploy/c1_rail/Dockerfile`, `.dockerignore`, and `scripts/c1_image_validation.sh`'s `LISTENER_FILES` inventory for the new transitive core module, with existing image tests. Inspect other production users before moving a fact.

**Proposed interfaces:** frozen `InstrumentSpec(symbol: str, multiplier: float, tick_size: float, tick_value: float)` and `INSTRUMENT_SPECS` in core, preserving explicit recorded values; research-owned `COMMISSION_BINDINGS: Mapping[str, str]` with explicit categories `index_micro` and `unavailable`. Keep explicitly unsupported symbols even if they have no geometry row. Operations derives its existing leg-keyed `TICK_SIZE_PTS` through an explicit leg-to-instrument mapping.

**Contract:** core owns geometry only; firm rules own available fee values; the research resolver owns the instrument's eligibility to use a fee row. Keep `resolve_commission(firm_key, instrument)` behavior and errors unchanged, including explicit commission overrides and unknown firms. Preserve `closed_world_findings()` coverage. Do not infer that every USD-quoted symbol has index-micro fees.

Reject invalid commission categories rather than classifying them as unavailable. Preserve detection of geometry without classification and priced instruments without geometry. A single-valued binding eliminates representable category overlap; replace the old derived-set overlap mutation with invalid/conflicting input coverage rather than retaining a second authored set merely to keep that mutation possible. Known symbols with no geometry remain explicitly unpriced. Retain typed numeric expectations and existing caller-visible error behavior.

- [ ] Apply Rule 0: re-read current production rules, resolver, slippage consumer and packaging before edits. Compare the base's resolved instrument rows and classifications, including types, against the proposed objects.
- [ ] Run `.\fp.ps1 python -m pytest tests/test_cost_model.py tests/ops/test_c1_rail_slippage.py -q` and add boundary regressions only where existing tests lack them: unavailable geometry/fees, unknown firm, unknown instrument, MYM versus MNQ tick sizes.
- [ ] Move geometry to core and replace authored partition lists with explicit bindings and derived views. Preserve public names used by callers where necessary; no second literal table in compatibility exports.
- [ ] Connect slippage to core geometry; preserve panel add offsets and actionable thresholds in their existing owners. Do not rewrite frozen `cost_es.py`, `cost_mgc.py`, `cost_mnq.py`, historical campaign results or independent fixture expectations.
- [ ] Include the new module in the existing explicit image packaging. Run focused cost/slippage suites and both image-manifest suites; run the existing listener image validation in its supported Linux/Docker environment before accepting the packaging change. If that environment is unavailable, report the unverified boundary.
- [ ] Measure total bytes. If moving a few tick facts grows the repository materially, retain that cross-layer move as a separately priced ownership improvement or defer it; do not count it as byte savings.

## Packet 4 — Test-only configuration factories

**Outcome:** Repeated setup dictionaries become scenario-specific factory calls while tests retain independent behavioral expectations.

**Files:** modify `tests/conftest.py`, `tests/ops/test_c1_rail_listener.py`, `tests/ops/test_m1_acceptance_drills.py`, `tests/ops/test_c1_signal_daemon_inject.py`, `tests/ops/test_m1_stage1_integration.py`. Do not expand into unrelated tests.

**Proposed fixtures:** `rail_config_factory` and `daemon_config_factory`, each returning a function that creates a fresh dict. Rail caller supplies `account`, `dry_run`, `armed_until`; daemon caller supplies `listener_base_url`, `emit_enabled`, `strategy` and `bar_period_s`. Remaining overrides are explicit keyword arguments. Factories contain test-only placeholder credentials and no production config imports.

Do not merge unrelated schemas: the listener transport dictionary and HTTP/server file-backed dictionary have different required fields. Start with transport setup and daemon setup; retain file-backed setup unless a separate named variant actually removes duplication. Overrides replace entire nested values, not recursive merge. Copy caller-supplied nested mutable values before returning. Factory inputs are not production-validated, so negative tests can still construct invalid values; omission cases keep literal dictionaries or explicit deletion after construction.

- [ ] Run `.\fp.ps1 python -m pytest tests/ops/test_c1_rail_listener.py tests/ops/test_m1_acceptance_drills.py tests/ops/test_c1_signal_daemon_inject.py tests/ops/test_m1_stage1_integration.py -q` and retain existing results.
- [ ] Extract shared fixture setup. Keep expiry clocks supplied by scenarios; do not hide `now()` or an armed default in the factory. Each call returns independent nested objects.
- [ ] Replace repeated setup, retaining malformed/raw configuration tests and expected payloads as literal independent expectations. Tests for omitted fields must actually omit those fields rather than silently inherit factory defaults.
- [ ] Run the same four suites; exercise two configurations in one test where existing mutation scenarios can prove isolation. Measure net bytes; avoid a large generic builder API.

## Packet 5 — Composable scan exclusions

**Outcome:** Repeated exclusion groups are reusable, while each scanner retains its original path matching and tracked/untracked scope.

**Files:** create `scripts/scan_profiles.py`; modify `scripts/check_md_relative_links.py`, `scripts/check_falsifier_reachability.py`, `scripts/check_boundaries.py`; extend their existing tests and create `tests/test_scan_profiles.py` for the filesystem membership matrix.

**Proposed interface:** immutable `ScanProfile(excluded_parts: frozenset[str], excluded_prefixes: tuple[str, ...])`; named per-tool profiles assembled from genuinely shared groups. Consumers continue to own traversal. Do not replace prefix checks with basename checks or vice versa.

**Contract:** the boundary scanner's exemptions, markdown scanner's directory-part filtering, and falsifier's union of tracked plus local inputs are different. In particular, preserve tracked-path handling and locally present ignored Pine/vendor inputs for falsifiers. A new generalized exclusion must not silently make a gate inspect fewer files. PR 417's classification YAML remains its own authority; this packet concerns scan membership only.

Validate profile field types and normalized relative prefixes, without broadening the base lists. Preserve exact prefix versus component matching: for example, the existing falsifier excludes `.claude/worktrees` by prefix but does not use the boundary scanner's whole `.worktrees/` exemption. Do not repair that asymmetry in this consolidation. Add tracked-cache and similarly named sibling-directory cases to the membership matrix.

- [ ] Record expected membership of a small temporary tree containing root/nested caches, `.venv-research`, `.worktrees`, `.claude/worktrees`, ordinary `.claude` content, tracked files and ignored local data. Derive expected sets from the existing consumer contracts, not the new shared profile.
- [ ] Write differential membership tests against the unmodified consumers; inventory any differences already present without fixing them in this refactor.
- [ ] Compose exact existing lists from shared groups; keep profile constants local if extracting them would cost more than it removes. Do not add a `.rgignore`/Cursor generator for three entries.
- [ ] Run `.\fp.ps1 python -m pytest tests/test_scan_profiles.py tests/test_check_md_relative_links.py tests/test_check_boundaries.py -q`. Exercise `build_universe()` with an injected temporary `ROOT` and controlled Git results so tracked/untracked behavior is tested. Compare output sets before/after and measure net bytes.

## Packet 6 — One hook matcher

**Outcome:** The two identical `PostToolUse` matchers in `.claude/settings.json` become one matcher with the same two independently scheduled handlers. Array order is not an execution-order guarantee.

**Files:** modify only `.claude/settings.json`.

- [ ] Parse and capture the existing `PostToolUse` matcher and command sequence with PowerShell `ConvertFrom-Json`. Read no machine-local settings.
- [ ] Put the existing `lock_event_hook.py` and `sync_skills_hook.py` command objects into one `hooks` array under `Edit|Write|MultiEdit`. Preserve all other JSON values, permissions and session hooks.
- [ ] Parse the result; compare complete handler objects and matchers, not only command strings, and all untouched sections including merged main's `PreToolUse` shell guard. Official [hook-handler documentation](https://code.claude.com/docs/en/hooks#hook-handler-fields), checked 2026-09-17, says matching hooks run in parallel. Preserve separate handler invocations, failure reporting and defaults; do not combine commands into a serial shell command. Record compatibility with the installed runner at execution; no live hooks need to be fired for the static refactor.
- [ ] Run `git diff --check` and record exact byte delta. No permanent test or generator is needed for this small reversible configuration edit.

## Packet 7 — Image-test service profiles (final-pass addition)

**Outcome:** Image-manifest tests share Dockerfile parsing and import traversal, configured by service-specific roots/entrypoints. Independent packaging assertions remain.

**Files:** create `tests/ops/image_manifest_support.py`; modify `tests/ops/test_c1_rail_image_manifest.py` and `tests/ops/test_c1_signal_daemon_image_manifest.py`.

**Proposed interface:** frozen `ImageTestProfile(dockerfile: Path, entrypoints: tuple[Path, ...], copy_prefixes: tuple[str, ...], imported_names: Callable[[Path], set[str]], resolve_module: Callable[[str], Path | None])`; shared `copied_python_paths(profile) -> set[str]` and `import_closure(profile) -> set[Path]`. Keep distinct import-name extraction and resolution functions where their semantics differ. Merged main's daemon extractor resolves relative imports using the importing file's package; the listener extractor does not. Sharing only a resolver would lose this distinction. Preserve both current entrypoint lists, including daemon `book_evaluate_loop.py`.

- [ ] Run both existing suites through `.\fp.ps1 python -m pytest tests/ops/test_c1_rail_image_manifest.py tests/ops/test_c1_signal_daemon_image_manifest.py -q`.
- [ ] Extract the shared COPY parser and traversal into the test helper. Retain per-service import-resolution rules, known nonempty closure assertions and the historical missing-module regression pins.
- [ ] Add or retain a negative miniature packaging case: a reachable imported module absent from COPY must fail. Do not derive the expected packaging set from the same manifest or resolver under test.
- [ ] Retain merged main's isolated packaged-book subprocess test and the `LISTENER_FILES` coverage assertion. Add relative-import and package-initializer cases to prove daemon behavior survives extraction. Preserve filesystem path normalization and missing-file behavior separately where consumers differ; no resolver hardening is included.
- [ ] Run both suites, check helper imports under normal pytest invocation, and measure net bytes. Previous inspected footprint: 10.3 KB combined, including a 2.27 KB daemon helper block; these are source measurements, not promised savings. Do not revive the deferred Dockerfile generator.

## Packet 8 — Brief validators: bounded consolidation decision

**Outcome:** Determine whether a shared implementation with explicit coverage profiles can reduce bytes while preserving both checker contracts and independent skill deployment; implement only the behavior-preserving, net-saving design.

**Files:** inspect `scripts/check_brief.py`, `.claude/skills/brief-authoring/scripts/check_brief.py`, `.claude/skills/brief-authoring/SKILL.md`, `tests/test_check_brief.py`, `tests/test_check_brief_skill.py`, and the skill packaging/release tooling. If feasible, add `.claude/skills/brief-authoring/scripts/brief_checks.py` as the canonical shared engine and keep both current CLI entrypoints as wrappers.

**Proposed contract:** canonical skill wrapper requests the full supported profile; repo wrapper requests its existing narrower profile. The repo wrapper loads the repo-local canonical engine, never a mutable installed home-directory copy. The skill package includes the engine and works when copied to a temporary directory with no repository imports. Unsupported repo-side types still produce their exact `NOT CHECKED` disposition. No promotion of coverage or gate severity.

Requirements-stage boundary: define the explicit check/type/format matrix and import strategy before implementation of this packet. Preserve `--list-checks`, `--self-test` and all shipped template paths in the standalone skill copy. Both existing CLIs only print `DELEGATED` instructions for closure and return zero; do not begin executing the closure checker or call that result a pass. Preserve missing/directory input errors and type-inference precedence. No requirement to share nonidentical checks just because their names match.

- [ ] Run `.\fp.ps1 python -m pytest tests/test_check_brief.py tests/test_check_brief_skill.py -q`; enumerate current type, alias, format and CLI results on compact synthetic documents.
- [ ] Map shared checks versus intentionally different checks and compare an engine-plus-profiles design to the current two files. Count packaging copies and import/bootstrap code. The 73.6 KB combined footprint is not removable duplication; no savings percentage is assumed.
- [ ] If feasible, extract only common parsing/check functions and type configuration; keep wrappers' report formatting, exits, aliases and decline behavior. Define the engine's concrete profile fields from the audited check map before editing wrappers; do not start with a generic rule language.
- [ ] Prove unchanged outputs/status for valid, invalid, concise/light, handoff, notice, lesson, audit, lock and closure cases; keep closure delegation. Test the standalone skill copy as well as repository invocation. Package changes stay local—do not publish the skill.
- [ ] Accept only after measured net reduction and both contract suites pass. Otherwise record the exact coverage/packaging cost and close as deferred. Changing checker authority or widening coverage would be a separate proposal, not completion of this refactor.

## Explicitly deferred remainder

- Dispatch wrappers: 857 bytes of overlapping forwarding measured in one wrapper; likely under 0.5 KB net after a helper. Retain current code until another real provider makes shared argument configuration worthwhile. Do not unify provider permissions or worktree behavior to save lines.
- Historical cost modules, frozen manifests, independent expected values and published results: retain their original evidence semantics.
- Fly and packaging generators: keep PR 417's deferral; reconsider only when actual service/account growth makes measured total savings positive.
- No new firm/product, account onboarding flow, risk policy or live operational capability is introduced here.

## Integration order and completion

Recommended order: baseline -> retrieval -> link policies -> scan profiles -> hook matcher -> test factories -> image-test profiles -> instrument facts -> brief-validator decision. Link/scan changes share ownership of markdown consumers and should be integrated sequentially. Image tests precede the instrument packaging change. Each packet receives its own focused acceptance and byte record; no subagent delegation is authorized by this planning request.

- [ ] For each packet, record accepted/deferred status, base/candidate revision, one canonical configuration owner, removed copies/guards, preserved independent checks, focused results and gross/net byte counts.
- [ ] Search the affected consumers for the retired definitions; verify no second literal authority or now-useless equality checker remains. Compatibility names may reference the canonical object, not restate it.
- [ ] On the integrated candidate, run `.\fp.ps1 test`, `.\fp.ps1 check`, and `git diff --check`. Run `.\fp.ps1 test-ops` separately only if it supplies coverage not already exercised or an operations change requires a focused rerun. Preserve required repository checks discovered at execution.
- [ ] Complete independent review of shared scanner/validator behavior and any image packaging changes through the authorized review workflow. Preserve the exact revision and environment behind each result.
- [ ] Publish one final accounting table: implemented savings, byte-neutral ownership improvements, rejected/deferred abstractions and remaining verification gaps. Report total tracked-byte delta including tests and records, separately from the reduction in authored configuration.

Completion means every listed opportunity has an evidence-backed disposition and every accepted change preserves its contract. It does not require implementing an abstraction that costs more than it removes. PR/merge actions remain subject to the user's execution authorization.

## Planning verification

Original planning record: prepared from read-only source inspection and PR 417 metadata. No project Python, tests, research runs, production probes or deployment actions were executed. Implementation interfaces were proposed; the original planning turn added only this plan.

Requirements-analysis update: refreshed merged source through Git objects and corrected requirements and interfaces as recorded in the linked analysis. No implementation files were changed and no test pass is claimed. The remaining environment/runner checks are execution prerequisites, not unanswered user preferences.
