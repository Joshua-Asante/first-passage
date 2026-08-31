# Private Companion Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a private, versioned authority for protected strategy source
and sensitive operational records without splitting First Passage's active public
methodology, evidence, or validation surface.

**Architecture:** Keep `first-passage` public and authoritative for code,
methodology, aggregate evidence, decisions, tests, and SHA-256 pins. Create a
private sibling repository, `first-passage-private`, authoritative only for the
protected bytes behind those pins. Bind the repositories with a versioned,
machine-checked compatibility manifest; do not introduce runtime imports across
the repository boundary.

**Tech Stack:** Git/GitHub private repository, Python 3.11+, YAML, SHA-256,
pytest, existing First Passage manifest and gate tooling.

**Spec:** [`docs/adr/2026-08-14-repo-public-visibility-transition.md`](../../adr/2026-08-14-repo-public-visibility-transition.md)
plus the design lock below. This plan is a follow-on to that ADR's public-clone
posture; implementation begins by adding a ratified addendum rather than silently
changing the posture.

## Global Constraints

- `first-passage` remains public and retains active ADRs, briefs, methodology,
  specs, aggregate results, tests, manifests, `lab/analysis/`, and the existing
  search-excluded public cold store.
- `first-passage-private` is private from its first remote commit. Never create it
  public and change visibility afterward.
- Private Git may contain durable proprietary source and sensitive records. It
  must not contain credentials, `.env` files, access tokens, live runtime state,
  bulk vendor-licensed datasets, regenerable caches, generated reports, or scratch
  logs.
- No code in `first-passage` may import, execute, or require files from the private
  repository. Private verification is an optional operator command; public CI and
  a fresh public clone remain green without the companion checkout.
- Public paths, sanitized summaries, and current SHA-256 pins remain stable. Do
  not expose previously redacted values in compatibility metadata, commit
  messages, PR text, issue text, CI logs, or test fixtures.
- The private checkout defaults to a sibling of the public checkout, never a
  nested directory: `../first-passage-private/`. An explicit CLI argument may
  override this path; no user-specific absolute path is committed.
- Copy and hash-verify protected bytes into the private repository before changing
  their local canonical location. Deletion of any original local copy requires a
  separate operator confirmation after remote recovery has been tested.
- `first-passage-archive` remains the immutable pre-transition history archive.
  The new companion is not a replacement, rewrite, or rename of that repository.

---

## Design lock: what moves and what does not

| Class | Destination | Rule |
|---|---|---|
| Locked and archived `*.pine` source | Private companion | Versioned, hash-matched to public `MANIFEST.sha256` / `PORT_MANIFEST.sha256` |
| Executable locked-strategy Python ports and their tests | Private companion | Versioned under the same relative public-era path |
| Unredacted strategy parameters and sensitive durable operating records | Private companion | Admit only through the inventory review in Task 2 |
| Promoted private authorization records such as `EXPLORE_GO.md` | Private companion when they are authoritative | Preserve a sanitized public outcome; never make the ignored file the only decision record |
| Active ADRs, briefs, methodology, specs, aggregate results, and tests | Public First Passage | Stay co-located with the code/evidence they explain |
| `lab/archive/`, `docs/ltm/`, `core/strategies/_archive/` public cold material | Public First Passage | Stay tracked and search-excluded by `.rgignore` / Cursor indexing policy |
| Vendor bars and licensed exports | Neither Git repository | Keep in licensed local/object storage; retain public integrity manifests where permitted |
| Secrets and live runtime state | Neither Git repository | Keep in the existing secrets/runtime system |
| Caches, reports, logs, worktrees, and scratch | Neither Git repository | Regenerate or expire |

## Target file structure

### Public `first-passage`

- Create `docs/governance/private-companion-repository.md`: sanitized operating
  contract, setup instructions, failure modes, and recovery procedure.
- Create `docs/governance/private-companion.schema.yml`: schema and allowed
  artifact classes for the public/private compatibility file.
- Create `scripts/check_private_companion.py`: optional cross-repo checker with a
  public-only structural mode.
- Create `tests/test_check_private_companion.py`: parser, path safety, mismatch,
  missing-checkout, and happy-path tests.
- Modify `scripts/gates.yml` and `tests/test_gate_manifest.py`: bind structural
  checks to compatibility-contract changes without requiring a private checkout.
- Modify `scripts/check_boundaries.py` and `scripts/repo_map_layers.yml`: classify
  the new checker as governance.
- Modify `.gitignore`, `.dockerignore`, `CLAUDE.md`, `README.md`, `REPO_MAP.md`,
  and `docs/operational_rules.md`: document the sibling-only boundary and prevent
  accidental nesting or remote-build inclusion.
- Modify `.github/workflows/manifest-check.yml`: run public structural validation
  only; never clone the private repository in public CI.
- Modify the existing Pine/port manifests only when a verified source hash truly
  differs; migration alone is not a reason to re-pin.

### Private `first-passage-private`

- Create `README.md`: classification policy, access model, bootstrap, and recovery.
- Create `COMPATIBILITY.yml`: schema version, compatible public commit, public
  manifest digests, and protected artifact inventory.
- Create `.gitignore`: deny secrets, runtime state, vendor data, caches, reports,
  logs, and nested repositories.
- Create `.gitattributes`: text/binary and line-ending policy matching public hash
  semantics.
- Create `.github/workflows/verify.yml`: validate compatibility shape, hashes, and
  forbidden-file policy on private PRs.
- Create `scripts/verify_private_repository.py` and
  `tests/test_verify_private_repository.py`: private-side validation.
- Create `strategies/`, `ports/`, `operations/`, and `research_evidence/`: the four
  admitted artifact classes; preserve original relative paths below each class.

---

### Task 1: Ratify the boundary before creating the private remote

**Phase:** 0 — authority and stop conditions

**Files:**
- Modify: `docs/adr/2026-08-14-repo-public-visibility-transition.md`
- Modify: `STATE.md` (decision-index line and normal retention roll only)
- Generated: `docs/adr/INDEX.md` through its existing generator

**Interfaces:**
- Consumes: the design lock and global constraints in this plan.
- Produces: an accepted addendum authorizing the named repository, admitted
  classes, sibling-checkout contract, copy-before-retire sequence, and operator
  deletion gate.

- [ ] **Step 1:** Add an ADR addendum recording the narrow companion decision.
  Explicitly reject a broad `docs/` or `lab/archive/` split, Git storage for
  secrets/vendor bars/generated files, runtime cross-repo imports, and reuse of
  `first-passage-archive`.
- [ ] **Step 2:** Record these stop conditions: stop if GitHub cannot prove the new
  repository is private before the first push; stop on any source-to-public-pin
  mismatch; stop if public CI needs private credentials; stop before deleting a
  local original until remote recovery passes.
- [ ] **Step 3:** Add the decision-index line to `STATE.md`; do not open an
  implementation queue row unless the repository's then-current queue policy
  requires one.
- [ ] **Step 4:** Validate the ADR and regenerate its index.

```powershell
python scripts/check_brief.py docs/adr/2026-08-14-repo-public-visibility-transition.md --type adr
python scripts/check_adr_graph.py --regenerate-index
python scripts/check_adr_graph.py
```

Expected: the form check and final graph check exit 0; the regenerated index is
included in the commit when its derived row changes.

- [ ] **Step 5:** Commit the authority change.

```powershell
git add docs/adr/2026-08-14-repo-public-visibility-transition.md docs/adr/INDEX.md STATE.md
git commit -m "docs(adr): authorize private companion repository"
```

---

### Task 2: Build and review the migration inventory

**Phase:** 1 — classify before copying

**Files:**
- Create: `docs/notes/audits/private-companion-migration-inventory.md`
- Read: `.gitignore`, `core/strategies/MANIFEST.sha256`,
  `core/strategies/PORT_MANIFEST.sha256`
- Read: all locally present ignored candidates selected by the inventory command

**Interfaces:**
- Consumes: admitted/excluded classes from Task 1.
- Produces: one row per candidate with `source_path`, `class`, `authority`,
  `public_pin`, `license`, `sensitivity`, `destination`, and `disposition`.

- [ ] **Step 1:** Enumerate locally present ignored files without reading secret
  contents into logs.

```powershell
git status --ignored --short --untracked-files=all > $env:TEMP\first-passage-ignored-paths.txt
```

- [ ] **Step 2:** Populate the audit table using only path and metadata reads.
  Assign exactly one disposition: `MIGRATE`, `LOCAL_OR_OBJECT_STORAGE`,
  `SECRET_OR_RUNTIME`, or `REGENERABLE_DELETE_CANDIDATE`.
- [ ] **Step 3:** For every `MIGRATE` row, record an existing public SHA-256 pin or
  compute a proposed pin without changing a manifest. For every vendor-data row,
  record the governing manifest and license restriction. Never paste protected
  bytes into the audit.
- [ ] **Step 4:** Review the table mechanically.

```powershell
rg -n "\.env|token|secret|accounts\.json|dd_protection_state|lifecycle_state|\.csv|\.parquet|\.pkl|reports/|\.cache/" docs/notes/audits/private-companion-migration-inventory.md
```

Expected: every match is explicitly classified outside `MIGRATE`, except a small
restricted research artifact whose license and necessity are both recorded.

- [ ] **Step 5:** Commit the sanitized inventory.

```powershell
git add docs/notes/audits/private-companion-migration-inventory.md
git commit -m "docs(audit): classify private companion migration set"
```

---

### Task 3: Create the private repository with deny-by-default controls

**Phase:** 2 — private foundation

**Files (private repository):**
- Create: `README.md`, `COMPATIBILITY.yml`, `.gitignore`, `.gitattributes`
- Create: `scripts/verify_private_repository.py`
- Create: `tests/test_verify_private_repository.py`
- Create: `.github/workflows/verify.yml`
- Create: empty tracked sentinels under `strategies/`, `ports/`, `operations/`,
  and `research_evidence/`

**Interfaces:**
- Consumes: sanitized Task 2 inventory and public manifest formats.
- Produces: private remote `Joshua-Asante/first-passage-private`, schema version
  `1`, and `verify_repository(root: Path) -> list[str]`.

- [ ] **Step 1:** Create the local sibling and initial branch.

```powershell
New-Item -ItemType Directory -Path ..\first-passage-private
git -C ..\first-passage-private init -b main
```

- [ ] **Step 2:** Write failing private-side tests for forbidden basenames,
  forbidden extensions/trees, escaping relative paths, duplicate inventory paths,
  malformed SHA-256 values, missing protected files, and hash mismatches.
- [ ] **Step 3:** Run the tests and verify they fail because
  `verify_private_repository.py` does not exist.

```powershell
python -m pytest ..\first-passage-private\tests\test_verify_private_repository.py -q
```

- [ ] **Step 4:** Implement the minimal verifier and deny rules. The verifier must
  print paths and finding codes only, never file content or credential-like values.
- [ ] **Step 5:** Run the private tests and verifier.

```powershell
python -m pytest ..\first-passage-private\tests\test_verify_private_repository.py -q
python ..\first-passage-private\scripts\verify_private_repository.py --root ..\first-passage-private
```

Expected: all tests pass and the verifier exits 0.

- [ ] **Step 6:** Commit locally, create the remote as private, verify visibility,
  and only then push.

```powershell
git -C ..\first-passage-private add README.md COMPATIBILITY.yml .gitignore .gitattributes .github scripts tests strategies ports operations research_evidence
git -C ..\first-passage-private commit -m "chore: initialize protected companion repository"
gh repo create Joshua-Asante/first-passage-private --private --source ..\first-passage-private --remote origin
gh repo view Joshua-Asante/first-passage-private --json visibility --jq .visibility
git -C ..\first-passage-private push -u origin main
```

Expected: visibility prints `PRIVATE` before the push.

---

### Task 4: Add the public/private compatibility checker

**Phase:** 3 — machine-checked bridge

**Files (public repository):**
- Create: `docs/governance/private-companion-repository.md`
- Create: `docs/governance/private-companion.schema.yml`
- Create: `scripts/check_private_companion.py`
- Create: `tests/test_check_private_companion.py`
- Modify: `scripts/check_boundaries.py`
- Modify: `scripts/repo_map_layers.yml`
- Modify: `scripts/gates.yml`
- Modify: `tests/test_gate_manifest.py`
- Modify: `.github/workflows/manifest-check.yml`

**Interfaces:**
- Consumes: private `COMPATIBILITY.yml` schema version `1`, public Pine/port
  manifests, and optional `--private-root PATH`.
- Produces: `validate_public_contract(public_root: Path) -> list[str]` and
  `validate_pair(public_root: Path, private_root: Path) -> list[str]`.

- [ ] **Step 1:** Write failing tests for public-only success, missing sibling as a
  warning/exit 0, explicit missing `--private-root` as an error, incompatible
  schema, wrong public repository identity, stale public-manifest digest, escaping
  private path, missing private artifact, and artifact hash mismatch.
- [ ] **Step 2:** Run the focused tests and verify they fail because the checker is
  absent.

```powershell
python -m pytest tests/test_check_private_companion.py -q
```

- [ ] **Step 3:** Implement YAML parsing with `yaml.safe_load`, canonical POSIX
  relative paths, `Path.resolve()` containment checks, streaming SHA-256, and
  content-free diagnostics. With no explicit private path, missing sibling is
  `WARN PRIVATE_COMPANION_ABSENT` and exit 0; with `--private-root`, absence is a
  hard failure.
- [ ] **Step 4:** Classify the script as governance in both boundary maps and add a
  path-conditional gate covering the checker, schema, public manifests, and its
  tests. Public CI invokes `--public-only`; it receives no private token.
- [ ] **Step 5:** Run focused and structural verification.

```powershell
python -m pytest tests/test_check_private_companion.py tests/test_gate_manifest.py -q
python scripts/check_private_companion.py --public-only
python scripts/check_boundaries.py
python scripts/check_repo_map_layers.py
```

Expected: all commands exit 0.

- [ ] **Step 6:** Commit the bridge.

```powershell
git add docs/governance/private-companion-repository.md docs/governance/private-companion.schema.yml scripts/check_private_companion.py tests/test_check_private_companion.py scripts/check_boundaries.py scripts/repo_map_layers.yml scripts/gates.yml tests/test_gate_manifest.py .github/workflows/manifest-check.yml
git commit -m "feat(governance): verify private companion compatibility"
```

---

### Task 5: Copy protected artifacts and prove byte identity

**Phase:** 4 — non-destructive migration

**Files:**
- Copy only Task 2 `MIGRATE` rows into the matching private artifact class.
- Modify: private `COMPATIBILITY.yml`
- Modify only if mismatched after investigation: public
  `core/strategies/MANIFEST.sha256` or `PORT_MANIFEST.sha256`

**Interfaces:**
- Consumes: approved inventory and both repository verifiers.
- Produces: private commit containing every approved protected byte and a
  compatibility record for the exact public commit/manifests.

- [ ] **Step 1:** Copy, do not move, each approved artifact. Preserve the original
  repository-relative path below its private class directory.
- [ ] **Step 2:** Populate `COMPATIBILITY.yml` with `schema_version: 1`, public
  repository identity, public base commit, SHA-256 of each public manifest, and
  one artifact row containing class, private relative path, public pin path, and
  expected digest.
- [ ] **Step 3:** Run both sides against the explicit sibling path.

```powershell
python ..\first-passage-private\scripts\verify_private_repository.py --root ..\first-passage-private
python scripts/check_private_companion.py --private-root ..\first-passage-private
python scripts/check_pine_manifest.py
```

Expected: all commands exit 0. Stop on any mismatch; determine whether the local
source is wrong or the public pin is stale before changing either repository.

- [ ] **Step 4:** Commit and push the private migration first.

```powershell
git -C ..\first-passage-private add COMPATIBILITY.yml strategies ports operations research_evidence
git -C ..\first-passage-private commit -m "feat: preserve protected First Passage authority"
git -C ..\first-passage-private push
```

- [ ] **Step 5:** Re-clone the private remote into a temporary directory and verify
  recovery against the public checkout.

```powershell
$recovery = Join-Path $env:TEMP 'first-passage-private-recovery'
git clone git@github.com:Joshua-Asante/first-passage-private.git $recovery
python scripts/check_private_companion.py --private-root $recovery
python "$recovery\scripts\verify_private_repository.py" --root $recovery
```

Expected: both verifiers exit 0 from remote-recovered bytes.

---

### Task 6: Update the public operating contract without broad extraction

**Phase:** 5 — workflow cutover

**Files (public repository):**
- Modify: `.gitignore`, `.dockerignore`, `CLAUDE.md`, `README.md`, `REPO_MAP.md`
- Modify: `docs/operational_rules.md`
- Modify: `scripts/check_pine_manifest.py`, `scripts/sync_pine_to_worktree.py`
- Modify: `tests/test_pine_manifest_guard.py`
- Create: `tests/test_sync_pine_to_worktree.py`

**Interfaces:**
- Consumes: verified companion and public checker from Tasks 4–5.
- Produces: documented sibling bootstrap and explicit companion-source option for
  existing Pine synchronization, while preserving public-clone soft degradation.

- [ ] **Step 1:** Add `first-passage-private/` as a defense-in-depth nested-repo
  ignore and Docker exclusion. State that nesting is unsupported; the supported
  default remains the sibling path.
- [ ] **Step 2:** Replace “bytes live only on Joshua's local disk” language with
  “bytes are recoverable from the private companion; local absence is permitted.”
  Keep the public/private/archive roles distinct.
- [ ] **Step 3:** Extend `sync_pine_to_worktree.py` with explicit
  `--companion-root PATH`; do not auto-clone, auto-pull, read credentials, or turn
  companion absence into a public-clone failure.
- [ ] **Step 4:** Add tests for explicit-source copy, mismatch refusal, escaping
  paths, absent companion, and unchanged current local-source behavior.
- [ ] **Step 5:** Verify focused tests, manifests, links, and Docker exclusions.

```powershell
python -m pytest tests/test_pine_manifest_guard.py tests/test_sync_pine_to_worktree.py tests/test_check_private_companion.py -q
python scripts/check_pine_manifest.py
python scripts/check_md_relative_links.py
git check-ignore first-passage-private/probe.txt
```

Expected: tests and checks exit 0; `git check-ignore` identifies the root ignore
rule.

- [ ] **Step 6:** Commit the public cutover.

```powershell
git add .gitignore .dockerignore CLAUDE.md README.md REPO_MAP.md docs/operational_rules.md scripts/check_pine_manifest.py scripts/sync_pine_to_worktree.py tests
git commit -m "docs(ops): adopt private companion recovery workflow"
```

---

### Task 7: Retire duplicate local authority only after operator approval

**Phase:** 6 — optional destructive cleanup

**Files:**
- Original local ignored files copied in Task 5
- Modify: `docs/notes/audits/private-companion-migration-inventory.md`

**Interfaces:**
- Consumes: successful remote recovery evidence and explicit operator approval.
- Produces: either retained local working copies marked `CACHE`, or removed
  duplicates recoverable from the private remote.

- [ ] **Step 1:** Paste commit IDs and verifier outputs—not protected content—into
  the migration inventory. Mark every migrated row `REMOTE_RECOVERY_VERIFIED`.
- [ ] **Step 2:** Present the exact local paths proposed for removal and request
  explicit operator confirmation. No implementation agent may infer approval from
  approval of this plan or earlier phases.
- [ ] **Step 3:** If approval is granted, move each confirmed file to the operating
  system recycle bin where supported. If recoverable deletion is unavailable,
  stop and obtain separate approval for permanent deletion.
- [ ] **Step 4:** Re-run both verifiers from a checkout with no original ignored
  copies and rehydrate one test worktree through `--companion-root`.

```powershell
python scripts/check_private_companion.py --private-root ..\first-passage-private
python scripts/sync_pine_to_worktree.py --companion-root ..\first-passage-private --verify
python scripts/check_pine_manifest.py
```

Expected: all commands exit 0 without relying on the retired duplicate paths.

- [ ] **Step 5:** Commit only the sanitized audit disposition; local ignored-file
  removal itself produces no public Git change.

```powershell
git add docs/notes/audits/private-companion-migration-inventory.md
git commit -m "docs(audit): close private companion migration"
```

---

### Task 8: Final validation and rollout handoff

**Phase:** 7 — prove both independent and paired operation

**Files:**
- Modify if required by actual rollout: `docs/governance/private-companion-repository.md`
- Modify: private `README.md`

**Interfaces:**
- Consumes: completed public and private repositories.
- Produces: three proven modes: public-only clone, paired operator checkout, and
  private-remote disaster recovery.

- [ ] **Step 1:** In a fresh public-only clone, run the full public suite and
  public-only compatibility check. Confirm no private credentials are requested.
- [ ] **Step 2:** In the paired checkout, run the full public suite, explicit pair
  check, private suite, and both repository verifiers.
- [ ] **Step 3:** Inspect GitHub Actions for both repositories and confirm no
  protected value or private artifact path content appears in logs.
- [ ] **Step 4:** Record the exact bootstrap, rotation, access-revocation, and
  recovery commands in the two READMEs. Require two-person review if private repo
  membership later expands beyond the operator.
- [ ] **Step 5:** Commit documentation corrections separately in each repository,
  push, and open linked PRs. Merge the private PR first when a public compatibility
  record depends on its commit; otherwise either order is safe.

```powershell
python -m pytest -q
python scripts/check_private_companion.py --public-only
python scripts/check_private_companion.py --private-root ..\first-passage-private
python ..\first-passage-private\scripts\verify_private_repository.py --root ..\first-passage-private
python -m pytest ..\first-passage-private\tests -q
```

Expected: every command exits 0. Report exact pass/skip counts and both commit IDs
in the rollout record.

---

## Phase gates and rollback

| Gate | Evidence required to advance | Rollback |
|---|---|---|
| 0 → 1 | Ratified ADR addendum | Revert docs only; no remote exists |
| 1 → 2 | Sanitized inventory with every candidate classified | Amend inventory; no bytes copied |
| 2 → 3 | GitHub reports `PRIVATE`; private verifier green | Delete empty private remote/local repo only with operator approval |
| 3 → 4 | Public structural checker green without private access | Revert checker/gate commit |
| 4 → 5 | Private push plus fresh-clone recovery passes every hash | Keep public local originals; fix private copy or compatibility record |
| 5 → 6 | Public suite green in public-only and paired modes | Revert workflow docs/sync changes; private archive remains additive |
| 6 → 7 | Explicit operator approval and post-cleanup rehydration pass | Restore local copies from verified private remote |

## Explicit non-goals

- Moving all of `docs/`, `docs/briefs/`, `docs/adr/`, `lab/analysis/`,
  `lab/archive/`, or `docs/ltm/`.
- Rewriting public Git history or changing the public repository's visibility.
- Adding Git LFS or copying licensed vendor datasets into the companion.
- Creating a package dependency, submodule, subtree, or nested checkout.
- Giving public GitHub Actions access to the private repository.
- Migrating secrets or replacing the deployment secrets system.
- Deleting local originals as part of the copy phase.

## Plan verification

Run before approving this plan for execution:

```powershell
python scripts/check_md_relative_links.py --strict --glob docs/superpowers/plans/2026-08-31-private-companion-repository-implementation.md
rg -n "T[B]D|T[O]DO|implement[ ]later|fill[ ]in|appropriate[ ]error[ ]handling|write[ ]tests[ ]for[ ]the[ ]above|Similar[ ]to[ ]Task" docs/superpowers/plans/2026-08-31-private-companion-repository-implementation.md
git diff --check
```

Expected: the link checker and `git diff --check` exit 0; the placeholder scan has
no matches.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-31 | Initial phased implementation plan based on the narrow private-companion boundary | Codex |
