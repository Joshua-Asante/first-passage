# T00 source-only contract: design (Phase A)

**Date:** 2026-09-30.
**Status:** A10b rebuilt 2026-10-01 (operator ruling "do the one clean rework on a simpler rule"): deny-by-default lexical scan of every `.replay`/`.replay_bracket`/`.proof` call and `.contract` load in `ops/`, each passing only by an explicit reviewed allowlist entry; dominance reasoning removed. Named residual: dynamic access (`getattr`, `operator.attrgetter`, string-built names) is outside a lexical scan; the runtime `verify_for` refusal and A10 remain the enforcing guard. 4.3 correction accepted by the operator 2026-09-30 (implementation conflict: production_source imports runner/mc.simulation). **Design ACCEPTED 2026-09-30 by the operator (option 1), on revision 4.2.** The final Codex review, `task_e_6abd4caf4cb0832c9b6d12ea9b58d3a4`, resolved the record-authentication and stale-input P1s; the pre-hook P1 is closed by the `-S` fix and A23, without a further design review.

This is a design only. It adds no code, and no file below is admitted for editing until a later amendment to the [dispatch card](../../briefs/handoffs/2026-09-30-t00-p7-tasks-3-4-dispatch.md) admits it.
**Authority:**
- the operator's 2026-09-30 Ruling 1, "Source-only contract" ([P7-closure packet §7, Operator rulings 2026-09-30](../../briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md#operator-rulings-2026-09-30));
- the coordinator's sequencing in [card §8.1](../../briefs/handoffs/2026-09-30-t00-p7-tasks-3-4-dispatch.md#81--coordinator-sequencing-after-the-checkpoint-1-return-2026-09-30).

**Review path:** the coordinator reviews, then Codex, then Joshua accepts.
**Code read at:** `claude/t00-p7-tasks-3-4` @ `e3d95b3` (revisions 1–2), `7e0c49c` (revision 3), `e6fad26` (revision 4) and `a6ab1e2` (revision 4.1); production code equals the Task 2 head `672d49f`.

## Revision 4.3 — forbidden-load correction (operator ruling 2026-09-30, "I accept")

**Why.** Implementation found that `c1_rail.qualification.production_source` itself imports `c1_rail.qualification.runner`, for `NeedsContext` at module top, and `mc.simulation`, for `EvaluationState` in `_engine`. Under the revision 4.2 refusal list, every P7 run would therefore refuse itself, and removing those imports would need edits to `runner.py` or `core/`, both forbidden. Joshua accepted this correction, which is limited to §2.5a "Refusal", §2.5b, state row 20 and A16c. The §2.6c procedural rule is unchanged.

**(a) Refusal list.** The load-refusal list is exactly `c1_rail.qualification.` + `part_a`, `bracket`, `benchmark`, `benchmark_part_a`, `production`, `orchestration`, `result_adjudication`, `seal` and `execution` (with all of `execution.*`). A name matches when `name == m or name.startswith(m + ".")`. It never matches by string prefix, so `production_source` is **not** matched by `production`. A test asserts this.

**(b) Entry-point stubs.** `runner` and `mc.simulation` may load, for their exception and dataclass types, and both are recorded in the loaded closure like any other module.
- **Replacement.** Before `runpy`, the bootstrap imports both through the recording finder. It replaces these attributes in the P7 process only with stubs that record `P7_FORBIDDEN_CALL` and raise, so a call means no record:
  - `runner.evaluate_replay`, `runner.run_synthetic_stage` and `runner._run_stage`;
  - `mc.simulation.simulate_path`;
  - `runner.simulate_path`, runner's own import-time binding of the kernel. This one goes beyond the four named in the ruling; it closes `evaluate_replay`'s default `kernel=`.
- **Record-time check.** When writing the record, the driver confirms by identity that every stub is still the bound attribute. A replaced-back attribute refuses with `P7_FORBIDDEN_CALL`.

**(c) A16c.** The test gains these cases, each with an unmodified twin:
- importing `part_a` is refused as `P7_FORBIDDEN_IMPORT`;
- calling `evaluate_replay` is refused as `P7_FORBIDDEN_CALL`;
- calling `simulate_path` is refused as `P7_FORBIDDEN_CALL`;
- restoring an original attribute is refused at record time as `P7_FORBIDDEN_CALL`.

A separate test proves `production_source` loads while `production` is refused.

## Revision 4.2 — the `-S` correction (operator ruling 2026-09-30, "option 1")

Codex's final review of revision 4.1 (`35f233e`, `task_e_6abd4caf4cb0832c9b6d12ea9b58d3a4`) left one P1. The revision 4.1 claim that `-I` excludes `site` is false: `-I` implies `-E -P -s`, not `-S`. So the global `site` module, `.pth` processing and `sitecustomize` could run before the hook.

Joshua accepted the design on this one-flag correction, without a further review round. It is an explicit exception to the stop rule, because the finding was a factual error with a one-flag fix.

| Change | Section / test |
|---|---|
| The launch becomes `python -I -S -B -c P7_BOOTSTRAP`, and the false sentence is corrected | §2.5b(1) |
| The bootstrap inserts the locked ops-env `site-packages` itself, after the hook and before `runpy`. It processes no `.pth` and runs no `sitecustomize` / `usercustomize`, and it records the inserted path and each present `.pth` file's hash without executing it. | §2.5b(1) |
| A23 falsifier: a planted `sitecustomize.py` and a `.pth` file with an import line must not execute, while third-party packages still load | §5 A23 |
| The startup residual is narrowed to the frozen stdlib init under `-I -S` | §2.5b(1) |

## Revision 4.1 — three binding requirements (operator ruling 2026-09-30)

Codex's narrow review of revision 4 (`a6ab1e2`, task `task_e_6abd41a3f030832cb583866d33d63406`) resolved cuts 1 and 4 but not cuts 2 and 3. It raised three new P1s:
- code runs before the hook is installed;
- the evidence record is unauthenticated;
- acceptance trusts the record's artifact digests.

Joshua ruled on 2026-09-30 ("yes") to fold three targeted fixes in as **binding requirements**, in an additive revision. They are specified in §2.5b, which **supersedes** the conflicting parts of §2.5a.

| P1 | Binding requirement | Section / tests |
|---|---|---|
| Pre-hook code is unrecorded (the driver file and interpreter startup) | **Pinned bootstrap.** P7 starts as `python -I -B -c P7_BOOTSTRAP`. The pinned constant installs the hook and finder, then runs `p7_driver` through `runpy`, so the driver is recorded. The only residual is interpreter startup, bound by the executable hash and version. | §2.5b(1); A20 |
| The record is unauthenticated | **Acceptance by reconstruction.** `accept_p7_record` re-executes P7 in a fresh process through the pinned bootstrap against the current artifact root. The regenerated record must equal the presented one byte for byte, outside an enumerated set of volatile fields; otherwise `P7_RECORD_NOT_REPRODUCED`. Determinism is required. | §2.5b(2); A19, A21 |
| Acceptance trusts the record's artifact digests | **Current bytes first.** Acceptance re-hashes every contract artifact, ports included, from the current artifact root before anything else; `P7_EVIDENCE_STALE` on a mismatch | §2.5b(3); A22 |

**Pre-committed stop.** Codex gets one narrow review of these three requirements. A further P1 **parks** the source-only route and returns it to Joshua with the fallback of waiting for the T10 F1 freeze. There is no revision 5.

## Revision 4 — scope simplification (operator-approved 2026-09-30)

Codex re-reviewed revision 3 (`e6fad26`, cloud task `task_e_6abd361aed38832c9c9f2b847e08c267`) and returned NOT RESOLVED:
- prior findings 1, 5 and 7 are resolved; 2, 3, 4 and 6 are not;
- there are two new P1s: result taint is removable by copying, and dynamically imported code escapes the closure.

Joshua approved revision 4 on 2026-09-30 ("I approve revision 4"), as a scope simplification rather than a fourth hardening round. Each change below removes a guarantee that in-process Python cannot provide in general, and substitutes a boundary that can be checked.

| Cut | Change | Replaces | Section |
|---|---|---|---|
| 1. Remove result taint | P7 runs as a one-shot separate interpreter that imports no runner, MC or qualification code and writes only its evidence file. The sealed wrapper types and the `verify_for` refusal stay. The P7-never-feeds-MC prohibition becomes a named procedural rule. The evidence file carries only hashes, counts and labels. | §2.6c registry, copy-resistance claim, A10c, A10d | §2.6c, §5 |
| 2. The closure is the loaded set | An import audit hook, installed before any first-party import, records every module as it loads, with origin and SHA-256. Outside-root origins are refused; third-party packages are recorded. `code_closure_sha256` is computed over the loaded set. | AST-predicted closure, start/origin/stability checks | §2.5a, §5 A16/A16c |
| 3. Accept from bytes | A P7 record carries the canonical contract bytes, approval bytes and closure table. `accept_p7_record` re-validates them against the pinned root at acceptance time and re-hashes the closure files. It is a required step of the coordinator's acceptance and of the post-rebase re-check. The lexical AST reader rule is dropped. | In-process receipt dependence, AST reader rule | §2.5a, §5 A17 |
| 4. Finding-6 residue | The source-only calendar validator requires a `source_truncated` row's reason to name the truncated slots | — | §2.6a, §5 A13 |

## Revision 3 — Codex review of `7e0c49c` (2026-09-30)

Codex made seven findings, all accepted. This revision is an additive commit.

| # | Finding | Change | Section |
|---|---|---|---|
| 1 | [P1] The source-only path cannot build or replay: `_qualification_domain` rejects the type, and `_check_path` calls `verify_for`, which refuses source-only | Integrity is split from authorization. `_resolve_domain` dispatches by exact type through preparation and loading. `replay` / `replay_bracket` / `proof` call `_verify_integrity`, never `verify_for`. A12 becomes an end-to-end positive with the guards intact. | §2.6, §5 A12 |
| 2 | [P1] Source-only `ReplayResult`s can reach `runner.evaluate_replay` / the MC kernel unseen by A10b | The source-only API returns sealed `SourceOnlyReplay` wrappers that are not `ReplayResult`. Inner results are registered, and `evaluate_replay`, the first-party route to the MC kernel, refuses them. An import-separation test forbids the P7 driver from importing runner, MC or stage code. | §2.6c, §5 A10c/A10d |
| 3 | [P1] The closure hashes files, not the code executed | Execution-origin validation (every closure module is first imported after the start check, with origin inside the code root) plus start/end source stability | §2.5a, §5 A16/A16c |
| 4 | [P1] Re-verification is only documentary | Named gate `accept_p7_record` recomputes the current closure and refuses stale evidence | §2.5a, §5 A17 |
| 5 | [P2] Revocation lacks an authoritative input and a receipt-lifecycle test | The pin carries `revoked_at`. Every use of an issued receipt re-checks the window, the pin membership and revocation. | §2.3, §2.5, §5 A6c/A12b |
| 6 | [P2] "Unchanged parsers" do not enforce the new source constraints | A named source-only calendar validator enforces the fact role, interior-truncation refusal and stand-in refusal | §2.6a, §5 A13/A18 |
| 7 | [P2] State-table refusals are untested | Explicit tests for rows 3, 7 and 18. Every negative asserts its own refusal code against a fixture whose unmodified twin passes. | §5 |

## Revision 2 — coordinator design review 2026-09-30

The review was made at `35fe1a80…` (`48bf30a`), and its verdict was REVISE. Some items were already applied in `c9742f0`. This revision is an additive commit.

| Finding | Change | Section |
|---|---|---|
| BLOCKING 1: caller-supplied trust root | The operator source-key fingerprint(s) are pinned in a tracked, compiled constant that only an operator-merged PR changes. A caller registry is accepted only if byte-equal to the pin. Test A6b is the self-signed forgery falsifier. | §2.3, §4, §5 |
| BLOCKING 2: P7 evidence does not bind code | Every P7 evidence record carries the git HEAD and the executed module closure (the `runtime.source_closure` rule) with its digest. P7 MET holds for that closure only. | §2.5a, §2.7, §5 A16 |
| 3: consumer refusal relies on `verify_for` alone | Test A10b: an AST scan of `ops/` for `ProductionSource` / `.contract` use outside the allowlist or without `verify_for` | §2.6, §5 |
| 4: typed truncation disposition | Already in `c9742f0`: §2.6a, `SourceDayStatus` in `clock.py`, which is named in §4. The stand-in is retired by this build. | §2.6a, §4 |
| 5: reviewer-authored companions | Already in `c9742f0`: §2.6b. This revision makes the reviewer identity and reviewed digest explicit and names the refusal test. | §2.6b, §5 A14 |
| 6: `path_start_date` and the signing packet | The explicit field was already in `c9742f0`. This revision adds §2.8, the signing packet. | §2.2, §2.8 |

## 1. Problem

`ProductionSource.build(contract, artifact_root=...)` accepts only a `ValidatedFrozenContract` from `validate_frozen_contract`, under a signed production `QualificationTrustDomain` (`book_adapters._qualification_domain`). That contract is the complete F1 qualification freeze:
- its role set is fixed at `REQUIRED_ARTIFACT_ROLES` plus every production code role (`contract.py:509`);
- it requires horizons, six stage specs, Part A, budget, decision rules, a result plan and a freeze approval (`contract.py:436ff`).

Choosing those values is T10 phase-2 and T00 step-2 work, which the P7-closure packet §6 forbids. The P7 question needs much less: *is candidate 3′ a faithful producer on the exact retained bytes?* That needs:
- the source identity: ports, panels, settings, historical admissions and the eight reviewed source roles;
- a PRISTINE initial account state;
- one operator signature over exactly those bytes.

This design adds that narrower contract. It cannot be mistaken for the F1 contract, and it cannot be substituted for it.

## 2. Behavioral contract

### 2.1 What it is

A **source-only contract** is a canonical JSON document with schema `t00_source_contract/v1`. One operator signature, in a new scope, turns it into a `ValidatedSourceContract` receipt. That receipt authorizes exactly one consumer path: `ProductionSource.build` → `replay` / `replay_bracket` / `proof`, used for P7 verification. It authorizes no qualification stage, screen, Monte Carlo, seal, admission, deployment or arm.

### 2.2 Schema and canonical bytes

Canonical bytes are `contract.canonical_json_bytes(doc)`: sorted keys, `(",", ":")` separators, UTF-8, `ensure_ascii=False`, NaN refused. `parse_canonical_json` must round-trip them to identical bytes; anything else is refused. The contract SHA-256 is the SHA-256 of those bytes. The field set is closed, and exactly these fields exist:

| Field | Content | Validation |
|---|---|---|
| `schema` | `"t00_source_contract/v1"` | exact |
| `contract_id` | nonempty text | text |
| `purpose` | `"T00_P7_SOURCE_VERIFICATION"` | exact |
| `artifacts` | list of `{role, path, sha256, producer, authority_class}` | the role set is exactly §2.4; paths are unique, relative to the artifact root and non-aliasing; `authority_class == "PRODUCTION_REVIEWED"` |
| `historical_pins` | the role → digest map | equals `contract.ACCEPTED_HISTORICAL_PINS` exactly |
| `port_runtime_pins` | leg → `{runtime_sha256, pine_sha256}` | equals the `book_adapters.ADAPTERS` pins exactly; the corrected Striker is `efd479b6…`, and `c81aa59c…` is refused |
| `effective_settings` | `{settings_sha256, orb_normal_base}` | `settings_sha256 == book_adapters.RUNTIME_EFFECTIVE_INPUTS_SHA256` (the loader-derived reviewed successor), never `66406dee…`; `orb_normal_base == 1` |
| `populations` | `{FULL, H1, H2}` lists of session ids | the same ordered ceil-partition law as `contract.py`; must equal the population index's pools (checked at build) |
| `initial_state` | the same six fields as the F1 contract | PRISTINE only, with the same rule as `contract.py:841` |
| `path_start_date` | ISO weekday date; a PROPOSED path-label origin | must be a weekday and must equal the `source_startup_policy` value, so the operator signs it knowingly |
| `source_trust` | `{key_id: {sha256, revoked_at}}` | must equal the pinned `SOURCE_SIGNING_KEYS` exactly (revision 3), including `revoked_at` |
| `refusals` | `["QUALIFICATION_STAGES","BUDGET","DECISION_RULES","SCREEN","MONTE_CARLO","SEAL","ADMISSION","DEPLOYMENT"]` | exact list; it is declarative, and enforcement is §2.6 |

There is no `replay`, `result_plan`, `approval_policy`, `coverage`, `clocks`, `trust_domain_sha256` or `policy_sha256` field. A document carrying any F1 field is refused, and so is a document missing any field above.

### 2.3 Signing scope, approval name and key-class separation

**Envelope.** The existing detached-approval envelope and verifier, `contract.verify_detached_approval`, is reused unchanged: `qualification_approval/v1`, Ed25519, with a canonical payload.

**Scope.** The scope is **`APPROVE_T00_SOURCE_CONTRACT`**, and `subject_sha256 == contract_sha256 ==` the SHA-256 of the canonical contract bytes. It is distinct from `FREEZE_F1` and `BIND_QUALIFICATION_TRUST_DOMAIN`, and because the scope is inside the signed payload, a signature for one scope never verifies for another.

**Authority.** `authority_class` is `OPERATOR`. `verify_detached_approval` is called with `allow_test_authority=False`, so no TEST_ONLY key verifies.

**Key-class separation.** There are two directions, both enforced in code:
- **Source validator:** every signing key ID must start with `source:`, must be listed in `source_trust.source_key_ids`, and its public-key SHA-256 must equal `trusted_key_sha256[key_id]`.
- **Qualification validator:** `trust_domain.validate_qualification_trust_domain` and `contract.validate_frozen_contract` refuse any enrolled key ID that starts with `source:`, raising `SOURCE_KEY_IN_QUALIFICATION_DOMAIN`. This is the one edit to the qualification path.

**Residual (accepted by the coordinator, 2026-09-30).** Code cannot stop the operator from enrolling the *same public key* under a non-`source:` ID in a later qualification domain. The ceremony uses a **dedicated operator key**, generated only for source contracts, and the P7 return records that key's fingerprint. With the pinned root, this residual is procedural and narrow.

**Trust root (revision 2, BLOCKING 1).** The trust root is **pinned in tracked code**, never supplied by the caller.
- `contract.py` gains the compiled constant `SOURCE_SIGNING_KEYS: Mapping[str, SourceKeyPin]`, mapping a `source:` key ID to `SourceKeyPin(sha256, revoked_at)`. `sha256` is the SHA-256 of the 32-byte Ed25519 public key, and `revoked_at` is a UTC instant or `None`. It ships **empty**, and an empty pin refuses every source contract (`SOURCE_TRUST_ROOT_UNENROLLED`).
- **Revocation (revision 3).** The authoritative revocation input is the pin's `revoked_at`, set only by an operator-merged PR. The validator builds each `TrustedApprovalKey` with `revoked_at` taken from the pin, never from the caller, so the reused verifier's revocation check reads the authoritative value.
- Joshua's dedicated source key is enrolled by its own PR, which **only the operator merges**. That PR changes only this constant and its test expectation.
- `validate_source_contract(contract_bytes, approval_bytes, public_keys, observed, *, now)` receives public key *bytes*. Each key it uses must hash to the pinned fingerprint for that ID.
- `source_trust` in the contract must equal the pinned map exactly. A registry the caller passes is accepted only if it is byte-equal to the pinned set; any extra, missing or different key is refused.
- The TEST_ONLY authority path does not exist for source contracts.
- Tests exercise signing by monkeypatching `SOURCE_SIGNING_KEYS` **inside the test process only**. The pinned constant in the tree never holds a test key; a test asserts that the shipped constant holds only operator-enrolled IDs.
- **Falsifier (A6b):** a well-formed contract, signed by a freshly generated key and presented with a matching self-supplied registry and `source_trust`, is REFUSED.

**Validity window and receipt lifecycle (revision 3).** `issued_at <= now < expires_at` is checked at validation.

Every later use of the receipt re-checks three conditions through `require_validated_source_contract(contract, now=...)`:
- `now` is still before `expires_at`;
- the signer's key ID is still in the *current* pin, with the same fingerprint;
- that pin entry's `revoked_at` is `None` or later than `now`.

"Every later use" means `build` and each `replay` / `replay_bracket` / `proof` call. A failure raises `SOURCE_APPROVAL_EXPIRED`, `SOURCE_KEY_REMOVED` or `SOURCE_KEY_REVOKED`. `now` comes from a single module seam, `production_source._now()`, which tests patch. Task 4 must run inside the window.

### 2.4 Role set (closed)

The set is exactly 25 roles. There are no optional roles, and any extra or missing role is refused.

| Group | Roles | Bytes and check at build |
|---|---|---|
| Historical pins (11) | `step6_admission_contract`, `step6_independent_review`, `step6_accepted_run`, `step3_admission_contract`, `step3_evidence_index`, `step3_independent_acceptance`, `aegis_runtime_port`, `striker_runtime_port`, `vanguard_runtime_port`, `orb_runtime_port`, `historical_effective_inputs` | SHA-256 equals `ACCEPTED_HISTORICAL_PINS`; `parse_historical_admission`; the seven-bundle Step 6 format |
| Admitted panels (4) | `panel_aegis_6j`, `panel_dj30_mym_p250`, `panel_vanguard_mgc`, `panel_orb_mnq_v7` | each digest equals the Step 3 admission's panel digest for that leg (the Aegis attested prefix is `8ae083d0…`); `decode_admitted_csv`; interval bounds |
| Settings successor (1) | `effective_settings_successor` | SHA-256 equals `RUNTIME_EFFECTIVE_INPUTS_SHA256`; `_qualification_snapshots` checks (ORB `qty == 1`) |
| Deadline facts (1) | `calendar_producer` | the Ruling-2 fact record (`t00-p7-calendar-deadline-facts/v1`); every calendar `fact` must bind this role and digest |
| Source roles (8) | `source_startup_policy`, `source_calendar`, `source_calendar_review`, `population_index`, `population_index_review`, `schedule_execution_evidence`, `schedule_execution_evidence_review`, `cost_model` | the existing parsers, plus the source-only checks: `validate_source_only_calendar` (§2.6a) and v2 reviews (§2.6b) |

The panels are named roles, not F1 roles. `_derive_retained_inputs` already finds panels by digest, which stays the check. The role names make the inventory readable, and the uniqueness check refuses a second artifact with the same digest.

**Artifact root.** The artifact root is the operator's primary checkout. Every path is checkout-relative, private paths stay gitignored, and `_read_retained_artifacts` refuses root escapes and aliases. No private byte is copied into a worktree.

### 2.5 Validation and receipt

`validate_source_contract(contract_bytes, approval_bytes, trusted_keys, observed, *, now) -> ValidatedSourceContract`:
1. Parse the canonical bytes and require the round-trip. Check the closed field set and exact values from §2.2.
2. Check the role set from §2.4 and the uniqueness of paths and roles.
3. Check that `observed.artifact_sha256` equals the declared path → digest map. The caller hashes retained bytes; the validator does not trust the caller's labels.
4. Check that `historical_pins`, `port_runtime_pins` and `effective_settings` equal the compiled constants.
5. Verify the key registry against `source_trust`, then `verify_detached_approval(..., expected_scope="APPROVE_T00_SOURCE_CONTRACT", allow_test_authority=False)`. The signer must be an enrolled `source:` key.
6. Issue a `ValidatedSourceContract`: a frozen dataclass whose type is distinct from `ValidatedFrozenContract`. Record it in a separate issuance registry keyed by identity with a receipt snapshot, following the `_ISSUED_CONTRACTS` pattern. `require_validated_source_contract` rejects any mutated or unissued object.

The receipt exposes the attributes `ProductionSource` reads:
- `contract_sha256`, `artifacts`, `runtime_load_sha256` (derived as role → digest; there is no separate runtime trace, because the source contract loads nothing it does not list);
- `effective_settings_sha256`, `populations`, `initial_state`, `approval`.

It also carries a **`SourceTrustDomain`** built from compiled constants, with `authority_class="OPERATOR"`, `permits_synthetic=False`, `accepted_historical_pins`, `port_runtime_pins`, `effective_settings_sha256` and `required_artifact_roles` (the §2.4 set). It carries no freeze/result/seal/execution key sets and no workload policy.

### 2.5a Producer-code binding (revision 2, BLOCKING 2)

P7 answers whether *specific code* is a faithful producer, so every P7 evidence record binds that code.

**Process boundary (revision 4; the launch form is superseded by §2.5b).** P7 runs as its own process: `python -I -B <p7_driver> <contract> <approval> <artifact_root> <out>`, launched through the checkout's validated operations interpreter. The process validates, builds, replays, writes one evidence file and exits. It imports no runner, MC, stage, Part A, adjudication, seal or execution code. Any such import is refused by the loaded-set rule below, because those modules are named in a refusal list checked by the hook.

**The closure is the loaded set (revision 4).** The driver's first statements, before any first-party import, install an import audit hook with `sys.addaudithook`, observing the `import` event. A `sys.meta_path` recording finder is an acceptable equivalent.
- **Recording.** The hook records every module **as it loads**: name, origin path and the SHA-256 of the origin file's bytes, read at load. A module later removed from `sys.modules` is still recorded, so removing it does not hide it.
- **Classification.** Each origin is classified as:
  - (a) under the repo code root, which is first-party and recorded;
  - (b) the interpreter's stdlib, recorded by name only;
  - (c) the locked ops-env site-packages, where each third-party distribution is recorded with name, version and file SHA-256 and is **not refused**;
  - (d) a pinned private port, loaded from retained bytes and recorded by its pinned digest.
- **Refusal.**
  - Any origin outside (a)–(d), including a first-party-named module loaded from another tree, refuses with `P7_ORIGIN_OUTSIDE_ROOT`.
  - Loading a module on the refusal list (`c1_rail.qualification.runner`, `part_a`, `bracket`, `benchmark*`, `production`, `orchestration`, `result_adjudication`, `seal`, `execution.*`, `mc.simulation`) refuses with `P7_FORBIDDEN_IMPORT`. *(Corrected in revision 4.3: `runner` and `mc.simulation` load with their kernel entry points stubbed, and matching is by exact name or package prefix.)*
  - A first-party file whose bytes at exit differ from its recorded load hash refuses with `P7_SOURCE_CHANGED_DURING_RUN`.
- **Why this covers dynamic imports.** Nothing is predicted: `importlib.import_module`, `__import__` and lazy imports all pass through the audited import path. Code executed through `exec` / `compile` of first-party file bytes, which would bypass import, is covered by the audit events `exec` and `compile`: any such event whose source is not the pinned port loader refuses with `P7_UNAUDITED_EXEC`.

`code_head` and a clean tree for every recorded first-party path are required at start and again at exit (`P7_TREE_DIRTY`).

Any refusal writes no P7 record. The shared `runtime.source_closure` AST traversal is no longer used for P7.

**Each P7 record carries:**
- `code_head` and `code_tree_clean: true`;
- `loaded_closure`: the recorded table of first-party modules (path, SHA-256), third-party distributions (name, version, file SHA-256), stdlib names and port digests;
- `code_closure_sha256`, the SHA-256 of the canonical JSON of `loaded_closure`;
- the **canonical contract bytes** and the **approval bytes** (base64), and their SHA-256s;
- the hashes, counts and equality/verdict labels of the P7 result. It carries no ReplayResult-shaped data, no per-session values and no private strategy values.

The Task 4 return names `code_closure_sha256`.

**Scope of a P7 result.** P7 MET holds **only for that loaded closure**. Any later change to a recorded first-party file or third-party distribution, including the rebase onto post-S5 `main` required by the merge hold, requires re-verification. Reuse is not allowed. A change to a file that was never loaded does not void it.

**Acceptance from bytes (revision 4; superseded where it conflicts by §2.5b).** `p7_evidence.accept_p7_record(record_bytes, *, code_root, now) -> AcceptedP7Record` is a standalone check. It uses no in-process receipt or issuance registry.
1. It re-validates the embedded contract and approval bytes with `validate_source_contract` against the pinned `SOURCE_SIGNING_KEYS` at `now`, including expiry and pin revocation. Observed artifact digests come from the record's inventory; retained bytes are not re-read.
2. It re-hashes every recorded first-party path under `code_root`, and every recorded third-party distribution file in the current interpreter. Any difference refuses with `P7_EVIDENCE_STALE`.
3. It requires a clean tree for those paths (`P7_TREE_DIRTY`) and `code_closure_sha256` to recompute exactly.

**Required procedure.** Calling `accept_p7_record` is a **required step** of the coordinator's P7 acceptance and of the post-S5 rebase re-check. Both procedures record the call's result, with its `code_closure_sha256` and the acceptance time. A P7 verdict not accepted this way is not accepted. This is enforced by procedure, not by a lexical code scan: the revision-3 AST reader rule is dropped.

### 2.5b Binding requirements (revision 4.1)

These requirements bind the implementation. Where §2.5a conflicts with them, this section governs.

**(1) Pinned bootstrap.**
- **Launch (revision 4.2).** P7 is launched only as `<ops-env python> -I -S -B -c <P7_BOOTSTRAP> <args>`. `P7_BOOTSTRAP` is a compiled string constant in `p7_evidence.py`, and `P7_BOOTSTRAP_SHA256`, the SHA-256 of its UTF-8 bytes, is a second compiled constant. A test asserts that they agree.
- **What the bootstrap does.** Its source, in order:
  1. installs the `sys.addaudithook` recorder (events `import`, `exec`, `compile`);
  2. inserts the recording `sys.meta_path` finder at position 0;
  3. sets `sys.dont_write_bytecode = True`;
  4. **(revision 4.2; site path derivation per the 4.3 implementation note below)** inserts the locked ops-env `site-packages` directory into `sys.path`. The path comes from the pinned constant `P7_SITE_PACKAGES_RELATIVE`, resolved against `sys.prefix` of the bound interpreter. The bootstrap processes **no** `.pth` file and runs **no** `sitecustomize` or `usercustomize`, because `site` is never imported. It records the inserted path, and each `.pth` file present in that directory with its SHA-256 (listed, never executed), under the record's interpreter binding as `site_packages_path` and `unexecuted_pth`. It also inserts the code roots, since `-I` ignores `PYTHONPATH`;
  5. **(revision 4.3)** imports `c1_rail.qualification.runner` and `mc.simulation` through the recording finder and installs the `P7_FORBIDDEN_CALL` stubs of revision 4.3(b);
  6. runs `runpy.run_module('c1_rail.qualification.p7_driver', run_name='__main__')`.

  *Implementation note (4.3):* under `-S`, `pyvenv.cfg` is never applied to `sys.prefix`, so the environment root is derived from the interpreter binding: the directory above `sys.executable`'s directory when it holds `pyvenv.cfg`, else `sys.prefix`.

  The order is fixed: hook, then finder, then path insertion, then `runpy`.

  The driver, and everything it imports, is therefore loaded through the recorded path, and `p7_driver.py` appears in `loaded_closure` like any other first-party module. `p7_evidence` itself is the only first-party module imported by the bootstrap before the hook exists. The bootstrap therefore installs the hook from inline code first, and imports `p7_evidence` afterwards, so it is recorded too.
- **Launcher.** The command string is built only from the constant. The bootstrap cannot hash its own `-c` source, so the record's `bootstrap_sha256` is written by the launcher, which is `p7_evidence.run_p7`. A forged value fails reconstruction (2), because the acceptor always launches with its own pinned constant.
- **What the flags exclude (corrected in revision 4.2).** `-I` implies `-E` (ignore `PYTHON*` environment variables), `-P` (no script or current directory on `sys.path`) and `-s` (no user site-packages). It does **not** suppress the global `site` module. Revision 4.1 wrongly said it did. **`-S`** is what suppresses `site`, and with it global `.pth` processing and `sitecustomize`. `-B` prevents bytecode writes.
- **Residual (named; narrowed in revision 4.2).** The only unrecorded pre-bootstrap code is the frozen and built-in stdlib initialization that runs under `-I -S`. No `site`, `.pth` or customization module runs. It is bound by recording `interpreter_sha256` (the SHA-256 of `sys.executable`'s bytes), `sys.version` and `sys.implementation.cache_tag`. The record additionally binds the locked environment's `requirements-ops.lock` SHA-256, `site_packages_path` and `unexecuted_pth`, and acceptance requires all of these to be equal (`P7_INTERPRETER_MISMATCH`).

**(2) Acceptance by reconstruction.** `accept_p7_record(record_bytes, *, code_root, artifact_root, now)`:
1. **Current-bytes check (3)** runs first.
2. **Re-validation.** It re-validates the embedded canonical contract and approval with `validate_source_contract` against the pinned `SOURCE_SIGNING_KEYS` at `now`, with expiry and pin revocation. An approval that has expired means acceptance needs a fresh operator signature; it is never reused.
3. **Re-execution.** It re-executes P7 through `run_p7` in a **fresh process**, with the pinned bootstrap, against the current `code_root` and `artifact_root`, into a temporary output.
4. **Comparison.** It requires the regenerated record to equal the presented record **byte for byte** after removing exactly the volatile fields below. Any other difference refuses with `P7_RECORD_NOT_REPRODUCED`.

The **volatile fields** are the complete list; no other field may vary.

| Field | Why it varies | Why it is safe to exclude |
|---|---|---|
| `run_started_at`, `run_finished_at` | Wall-clock instants of the run | No verdict, count or hash depends on them; the approval window is re-checked at acceptance with the acceptor's own `now` |
| `host_run_id` | A random per-process identifier used to name the temporary output | It names a file and binds no content |
| `accepted_at` / acceptor identity | Present only in the acceptor's own record of acceptance, never in the P7 record | Not part of the compared bytes |

**Everything else is compared**, including:
- `code_head`, `loaded_closure`, `code_closure_sha256` and `bootstrap_sha256`;
- the interpreter binding;
- the contract and approval bytes;
- the artifact inventory digests;
- the result hashes, counts and labels.

**Determinism requirement.** The P7 run must be a pure function of (code closure, interpreter binding, contract, approval, retained artifact bytes):
- no RNG, or only a seeded RNG whose seed is in the contract (P7 has none today);
- no wall-clock reads outside the volatile fields;
- no dependence on dict or set iteration order, filesystem listing order, the process ID, the hostname or environment variables;
- every emitted collection is sorted, and records are canonical JSON, with floats encoded as `float.hex` inside result digests;
- the source-only receipt check at run time uses the approval window with the run's `now`, which is not recorded.

Because a forged or hand-edited record cannot be reproduced by a real run over the current inputs, reconstruction authenticates the record. No separate signature over the record is needed.

**(3) Current bytes first.** Before re-validation and re-execution, acceptance re-reads every artifact named in the embedded contract, including the four pinned ports, the panels, the historical pins and the source roles, from the **current** `artifact_root`, and compares each SHA-256 with the contract's declared digest. It also re-hashes every recorded first-party and third-party closure file. Any mismatch refuses with `P7_EVIDENCE_STALE` before the process is launched. The record's own inventory is never trusted for this check.

### 2.6 What `ProductionSource.build` does and refuses

**Dispatch.** `build(contract, *, artifact_root)` dispatches on the exact type of `contract`:
- `ValidatedFrozenContract`: the existing path, unchanged.
- `ValidatedSourceContract`: the new path, below.
- Anything else: refused.

**New path (revision 3: integrity separated from authorization).** Today every internal step calls `_qualification_domain(contract)`: `_derive_retained_inputs`, `_build_from_prepared`, `_load_domain_adapters`, `verify_for` and, through `_check_path`, `replay`. Each of those rejects the new type. The design therefore replaces each internal call with **`book_adapters._resolve_domain(contract)`**, which dispatches on the exact receipt type:
- `ValidatedFrozenContract` goes to `_qualification_domain`, unchanged;
- `ValidatedSourceContract` goes to `_source_domain`, which calls `require_validated_source_contract(contract, now=_now())`;
- anything else is refused.

The callers switched are exactly:
- `production_source`: `_derive_retained_inputs`, `_build_from_prepared`, `_engine` (via `_load_domain_adapters`) and the new `_verify_integrity`;
- `book_adapters`: `_load_domain_adapters`.

`prepare_production_inputs`, `load_qualification_adapters` and `_build_composition` keep their current exact-domain checks, so they stay qualification-only or TEST_ONLY-only.

The build then runs the **same** checks as today: reviews, calendar, population index, `validate_calendar` / `validate_provider_generation` / `validate_coverage`, `UNKNOWN_SOURCE_DATE` refusal, adapter-capital equality, `build_panel`, schedule evidence and costs. It adds the source-only checks of §2.6a–§2.6b, and the issued source records `evidence_class = "T00_P7_SOURCE_ONLY"`.

**Integrity versus authorization.** The current `verify_for` body is split in two.
- **`_verify_integrity()`** checks:
  - the issuance registry and the execution snapshot;
  - `_resolve_domain(self.contract) is self._domain`;
  - the retained-byte re-hash (`_qualification_snapshots`);
  - for source-only, the receipt lifecycle of §2.3.
  It authorizes nothing.
- **`verify_for(contract)`** is `_verify_integrity()` plus qualification authorization. It requires `type(self.contract) is ValidatedFrozenContract` and `self.contract is contract`, and otherwise raises `SOURCE_ONLY_NOT_QUALIFICATION`.
- `_check_path`, and therefore `replay`, `replay_bracket` and `proof`, call `_verify_integrity()` only. Qualification consumers keep calling `verify_for`, which refuses a source-only source.

**Refused for a source-only source.**
- `ProductionSource.verify_for(contract)` raises `SOURCE_ONLY_NOT_QUALIFICATION` when `self.contract` is a `ValidatedSourceContract`. That covers every current qualification consumer: `production.py` executor binding, `execution/compute.py` and `execution/evidence.py`. None of them runs.
- The source-only path calls no stage, Part A, budget, adjudication, seal or screen code. `replay`, `replay_bracket` and `proof` stay available through `_verify_integrity`, and each checks the path against its own issued sessions. Their outputs are sealed (§2.6c).
- `_build_composition` and the TEST_ONLY domain are untouched, and a `TEST_ONLY` key cannot sign a source contract.
- **Structural guard (A10b).** Refusal does not depend on `verify_for` alone. A test scans every module under `ops/` by AST for references to `ProductionSource` or a `.contract` attribute read on one. Outside `production_source.py`, each reference must be either on an explicit source-only allowlist (the Task 4 driver) or dominated by a `verify_for(...)` call in the same function before use. A new consumer that skips `verify_for` fails the test.

### 2.6c Source-only results: sealed types, process boundary and procedural rule (revisions 3–4)

Refusing the source object does not stop its *results* from travelling: `runner.evaluate_replay` accepts any `ReplayResult` and calls the MC kernel. Revision 4 bounds result use by the P7 process boundary and a named procedural rule, not by in-process taint.

1. **Sealed return types.** On a source-only source:
   - `replay` returns `SourceOnlyReplay`;
   - `replay_bracket` returns `SourceOnlyBracket(r1: SourceOnlyReplay, r2: SourceOnlyReplay)`;
   - `proof` returns its edges and joins wrapped in the same seal.

   Neither type is a `ReplayResult` or a subclass. Each exposes for the hand recompute only primitive per-session tuples: source date, occurrence, start and end edges, daily P&L, `intraday_low`, and an events digest. It carries `evidence_class`, the contract SHA-256 and the approval SHA-256. The F1 path still returns `ReplayResult` / `BracketReplayResult`, unchanged.
2. **Process and procedure bound result use (revision 4).** The identity registry and the copy-resistance claim of revision 3 are **removed**. Data can always be copied, so no in-process taint is claimed. Instead:
   - the P7 process cannot reach MC or qualification code, because a load refuses with `P7_FORBIDDEN_IMPORT` (§2.5a);
   - the P7 process writes only its evidence file, whose schema holds hashes, counts and labels and no ReplayResult-shaped or per-session data;
   - the private hand-recompute worksheet for Task 4 is written separately under the private root by the executor. It is never a P7 evidence file and never an input to any runner.
3. **Named procedural rule (P7-closure packet §6).** **P7 output is never fed to MC, the screen or any qualification stage.** This restates packet §6's "Forbidden: any screen or Monte Carlo run" for P7 output specifically. A breach is a procedural violation, reported as such. It is not claimed to be prevented by code.

**Invariants kept.**
- `candidate_book_protection_policy()` stays at 1%/0.40, and `core/dd_protection.py` is not touched.
- R1 and R2 each run on a fresh engine.
- The frozen Task 2 interface is unchanged.

### 2.6a Typed truncation disposition (replaces the POLICY_DENIED stand-in)

**Problem.** A panel that ends or starts mid-session leaves a source date with no active-window bar, like the 2026-09-03 tail. Today the only way to exclude it is `policy_denied`, which the coordinator accepted on 2026-09-30 as a stand-in, not a venue fact.

**Change.**
- Add `SourceDayStatus.SOURCE_TRUNCATED = 'source_truncated'` in `clock.py`.
- Add `'source_truncated'` to the exclusion reasons `parse_population_index` allows.
- `_build_from_prepared` already relabels denied dates with their typed status. That relabel is **not** a guard. The guards are in the new validator below.

**Rules.**
- A `source_truncated` row must carry an empty `venue_deadlines` and a reason naming the truncated slots.
- It may appear only at `coverage_start` or `coverage_end`. An interior truncation is refused as `UNKNOWN_SOURCE_DATE`.
- At the source-only contract build, a `policy_denied` row whose reason begins `panel truncated` is refused, which retires the stand-in. The source pack is regenerated with the typed status before signing.

**Where these rules are enforced (revision 3).** A new function, `production_source.validate_source_only_calendar(raw, *, contract)`, runs in `_build_from_prepared` on the source-only path **before** `parse_source_calendar`. It re-reads the calendar JSON and refuses:
- any `facts[]` entry or `venue_deadlines[*].fact` whose `role` is not exactly `calendar_producer`, or whose digest differs from the contract's `calendar_producer` artifact (`CALENDAR_FACT_ROLE`). This closes the gap that `_fact` accepts any retained role with a matching digest;
- a `source_truncated` row with non-empty `venue_deadlines`, or at a date other than `coverage_start` / `coverage_end` (`SOURCE_TRUNCATION_INTERIOR`);
- a `source_truncated` row whose reason does not name the truncated slots, as an ET slot range matching the population index's recorded slots for that date (`SOURCE_TRUNCATION_REASON`) (revision 4);
- a `policy_denied` row whose reason begins `panel truncated` (`TRUNCATION_STAND_IN_RETIRED`).

The F1 path does not call it, so F1 behavior is unchanged.

### 2.6b Review companions are reviewer-authored

**The rule.** A review companion is written by the reviewer, after the review, over the exact reviewed digest. A producer may emit only a template, named `*.UNREVIEWED-TEMPLATE.json`, and a template never satisfies a review role.

**Schema.** The companion schema becomes `qualification-source-review/v2` and adds three fields to the v1 fields:
- `reviewer`: a nonempty identity, such as the coordinator session or a named reviewer;
- `reviewed_at`: a UTC instant;
- `notes`: a nonempty list of statements. For the source calendar and population index these must include the truncation, head-partial and residual statements.

**Reviewed digest.** `artifact_sha256` is the digest of the exact bytes the reviewer reviewed. A companion missing `reviewer`, `reviewed_at`, `notes` or `artifact_sha256` is refused.

**Validation.** `_review` in `production_source.py` accepts v2 only on the source-only path, and requires `reviewer` to differ from the artifact's producer identity recorded in the contract's `artifacts[].producer`. v1 stays unchanged for the F1 path. Self-certification (a producer equal to the reviewer) is refused as `REVIEW_NOT_INDEPENDENT`.

### 2.8 Signing packet (revision 2)

Before the operator signs, the executor assembles a **signing packet** under the private root and the coordinator reviews it:
1. the contract's canonical bytes and their SHA-256;
2. a human-readable listing of every role's path and digest, grouped as in §2.4;
3. the populations' counts (FULL, H1, H2 and exclusions by reason);
4. `initial_state`;
5. `path_start_date`, marked PROPOSED;
6. the Ruling-2 deadline model (12:59 ET on D19 venue-flat dates, 16:45 ET otherwise, for all legs) and its two named residuals;
7. the tail disposition (`source_truncated` at 2026-09-03);
8. the dedicated source key's ID and fingerprint, matching the pinned constant.

Joshua signs the canonical bytes only after reading the listing. The approval's `subject_sha256` must equal the packet's contract SHA-256. The packet holds no private strategy values: paper capitals appear only as `== constructor` / `== Step 3` equality labels.

### 2.7 Labelling of P7 evidence

Every artifact produced under a source-only contract carries:
- `evidence_class: "T00_P7_SOURCE_ONLY"`, the contract SHA-256 and the approval SHA-256;
- `code_head`, `code_closure_sha256` and the closure table (§2.5a);
- the label **"P7 producer-faithfulness evidence; not qualification, screen, GO/NO-GO or F1 evidence"**.

The `calendar_producer` record's label, `RULED_MODEL_DEADLINES_NOT_OBSERVED_VENUE_HISTORY`, and the schedule evidence's model-convention status carry into the Task 4 return. The public return contains only hashes, counts and equality/verdict labels.

## 3. State and event table

| # | State / event | Required outcome |
|---|---|---|
| 1 | Canonical bytes are not canonical, or have an unknown or missing field, or carry an F1 field | `ContractValidationError`, before any signature check |
| 2 | The role set differs from §2.4 (extra, missing or renamed) | Refused |
| 3 | An observed artifact digest differs from the declared one | Refused |
| 4 | Historical, port or settings pins differ from the compiled constants (including `c81aa59c…` or `66406dee…`) | Refused |
| 5 | The approval scope is `FREEZE_F1` or `BIND_QUALIFICATION_TRUST_DOMAIN` | Refused (scope mismatch) |
| 6 | The signer is a TEST_ONLY key, a non-`source:` ID, not enrolled, revoked, expired or has a mismatched fingerprint | Refused |
| 7 | A valid source approval is presented to `validate_frozen_contract` or the trust-domain validator | Refused: wrong scope, and the `source:` key ID is refused there |
| 8 | A `ValidatedSourceContract` is passed to a qualification consumer (`ProductionExecutor`, compute, evidence) | `verify_for` raises `SOURCE_ONLY_NOT_QUALIFICATION` |
| 9 | A receipt is mutated after issuance, or a lookalike is constructed | `require_validated_source_contract` refuses it |
| 10 | Source roles are missing, a review mismatches, a date is UNKNOWN, or coverage/population disagree | The existing `ProductionSourceNeedsContext` / `ValueError`, unchanged |
| 11 | `build` succeeds | The issued `ProductionSource` has `evidence_class == "T00_P7_SOURCE_ONLY"`; `replay_bracket` passes `_verify_integrity` and returns `SourceOnlyBracket(r1, r2)` from two fresh engines |
| 12 | `now` is outside the approval window at build, **or at any later replay call after a valid build**, or the key was removed from or revoked in the pin after issuance | Refused (`SOURCE_APPROVAL_EXPIRED` / `SOURCE_KEY_REMOVED` / `SOURCE_KEY_REVOKED`); re-signing is an operator act |
| 13 | A calendar row is `source_truncated` at an interval end | Excluded with a typed reason; FULL omits it |
| 14 | A `source_truncated` row falls in the interior, or a `panel truncated` `policy_denied` stand-in appears on the source-only path | Refused |
| 15 | A review companion is a template, or v1 on the source-only path, or has reviewer equal to producer | Refused (`REVIEW_NOT_INDEPENDENT` for self-review) |
| 16 | `path_start_date` in the contract differs from the startup policy, or is not a weekday | Refused |
| 17 | The signer's key is not in the pinned `SOURCE_SIGNING_KEYS`, or the caller's registry differs from the pin, or the pin is empty | Refused (`SOURCE_TRUST_ROOT_UNENROLLED` / `SOURCE_TRUST_ROOT_MISMATCH`) |
| 18 | P7 evidence is emitted from a dirty tree, or without a closure digest | Refused; no P7 record is written |
| 19 | A recorded first-party file or third-party distribution changes after P7 MET, and the old record is presented to `accept_p7_record` | Refused (`P7_EVIDENCE_STALE`); the embedded contract and approval are also re-validated at acceptance time |
| 20 | The P7 process loads a module on the 4.3 refusal list (`part_a`, `bracket`, `benchmark*`, `production`, `orchestration`, `result_adjudication`, `seal`, `execution.*`), or calls a stubbed kernel entry point, or restores one | Refused (`P7_FORBIDDEN_IMPORT` / `P7_FORBIDDEN_CALL`); no record |
| 21 | A loaded module's origin is outside {code root, stdlib, locked site-packages, pinned ports}; a first-party file changes during the run; an unaudited `exec` / `compile` of first-party bytes occurs | No record (`P7_ORIGIN_OUTSIDE_ROOT` / `P7_SOURCE_CHANGED_DURING_RUN` / `P7_UNAUDITED_EXEC`) |
| 23 | The driver, or a module it imports, runs without passing through the bootstrap's recorder; or the bootstrap constant and its pinned hash disagree | No record (`P7_BOOTSTRAP_MISMATCH`); the run is refused unless launched by `run_p7` with the pinned constant |
| 24 | A presented record differs from the reconstructed record in any non-volatile field | Refused (`P7_RECORD_NOT_REPRODUCED`) |
| 25 | Any current artifact or closure file differs from the contract's digest or the recorded hash at acceptance | Refused (`P7_EVIDENCE_STALE`) before re-execution |
| 26 | The interpreter executable hash, version, cache tag or lock hash differs at acceptance | Refused (`P7_INTERPRETER_MISMATCH`) |
| 22 | A calendar fact names a role other than `calendar_producer`, a truncation is interior, its reason does not name the slots, or the stand-in appears | Refused (`CALENDAR_FACT_ROLE` / `SOURCE_TRUNCATION_INTERIOR` / `SOURCE_TRUNCATION_REASON` / `TRUNCATION_STAND_IN_RETIRED`) |

## 4. Files it would touch (admitted only by a later amendment)

| File | Change |
|---|---|
| `ops/c1_rail/qualification/contract.py` | Adds `SOURCE_SIGNING_KEYS` (the pinned root, shipped empty; enrolled only by an operator-merged PR), `SOURCE_CONTRACT_SCHEMA`, `SOURCE_SCOPE`, `ValidatedSourceContract`, `validate_source_contract`, `require_validated_source_contract` and a separate issuance registry. `validate_frozen_contract` gains the `source:` key-ID refusal. No existing F1 rule changes. |
| `ops/c1_rail/qualification/trust_domain.py` | Adds `SourceTrustDomain` (compiled from constants, with no signed domain bytes). `validate_qualification_trust_domain` refuses `source:` key IDs. |
| `ops/c1_signal_daemon/book_adapters.py` | Adds `_source_domain(contract)` and `_resolve_domain(contract)`. `_load_domain_adapters` resolves through `_resolve_domain`. `load_qualification_adapters`, `_load_composition_adapters` and the historical loader are unchanged. |
| `ops/c1_rail/qualification/runner.py` | **Not changed** (revision 4 removes the result registry) |
| `ops/c1_rail/qualification/p7_evidence.py` (new) | `P7_BOOTSTRAP` and `P7_BOOTSTRAP_SHA256`, the audit hook and recording finder, `run_p7` (the launcher), the P7 record writer, and `accept_p7_record` (current-bytes check, re-validation, re-execution, byte comparison) (§2.5a–§2.5b) |
| `ops/c1_rail/qualification/production_source.py` | `_resolve_domain` callers, `_verify_integrity` / `verify_for` split, sealed source-only results and the inner-result registry *(status 2026-09-30, card amendment 2: revision 4 governs; no inner-result registry is built, per §2.6c)*, `validate_source_only_calendar`, `_now()` seam. `build` dispatches on type, the issued source records `evidence_class`, and `verify_for` refuses source-only for qualification consumers. `parse_population_index` allows `source_truncated`. `_review` accepts v2 on the source-only path (§2.6b). The other parsers are unchanged. |
| `ops/c1_rail/qualification/clock.py` | Adds `SourceDayStatus.SOURCE_TRUNCATED` (§2.6a) |
| `ops/c1_rail/qualification/p7_driver.py` (new) | The P7 body, run only via `runpy` from the pinned bootstrap: validates, builds, replays and writes the record (§2.5b) |
| `tests/ops/qualification/test_source_consumers.py` (new) | A10b AST consumer scan |
| `tests/ops/qualification/test_source_contract.py` (new) | Acceptance tests A1–A10 below |
| `tests/ops/qualification/test_production_source.py` | A11–A12, plus Task 4's real-path wiring |
| `tests/ops/qualification/test_trust_domain.py` / `test_contract.py` (existing) | The `source:` refusal cases, A7 |

`clock.py` changes only by the new enum member. No change to `replay.py`, `model.py`, `book_policy.py`, `core/dd_protection.py`, runner, screen, seal or execution code.

## 5. Acceptance tests and falsifiers

**Attribution rule (revision 3).** Every negative test asserts its **own** refusal code or message, and each is paired with a positive twin: the same fixture, unmodified, which passes the same call. A refusal raised earlier, by an unrelated check, fails the test. Negatives reach their intended boundary by mutating only the one input under test.

Tests use TEST_ONLY-generated Ed25519 keys **only inside the test process**, to exercise the verifier. The production signature is the operator's act, and no test key is ever written to the artifact root.

| ID | Test | Passes when | Falsifier |
|---|---|---|---|
| A1 | `test_source_contract_canonical_roundtrip_and_closed_fields` | Canonical bytes validate; a reordered, whitespace-changed or extra-field variant is refused | Any non-canonical or extra-field variant validates |
| A2 | `test_source_contract_refuses_every_f1_field` | Each of `replay`, `result_plan`, `approval_policy`, `coverage`, `clocks`, `trust_domain_sha256` and `policy_sha256` is refused | Any F1 field is accepted |
| A3 | `test_source_contract_role_set_is_exact` | The exact 25 roles validate; each single removal, addition or rename is refused | Any variant validates |
| A4 | `test_source_contract_pins_are_compiled_constants` | Changing any historical, port or settings pin is refused; `c81aa59c…` and `66406dee…` are named refusals | A substituted pin validates |
| A5 | `test_source_approval_scope_is_exclusive` | A `FREEZE_F1` or `BIND_QUALIFICATION_TRUST_DOMAIN` signature over the same digest is refused | A foreign-scope signature verifies |
| A6 | `test_source_signer_must_be_enrolled_source_key` | TEST_ONLY, non-`source:`, unenrolled, revoked, expired and fingerprint-mismatched signers are all refused | Any of them verifies |
| A7 | `test_qualification_validators_refuse_source_key_ids` | Both qualification validators raise `SOURCE_KEY_IN_QUALIFICATION_DOMAIN` | A `source:` key enrolls in a qualification domain |
| A8 | `test_source_receipt_mutation_and_lookalike_refused` | A mutated or hand-constructed `ValidatedSourceContract` is refused | A non-issued receipt passes |
| A9 | `test_build_dispatches_on_exact_contract_type` | `build` accepts both validated types and refuses a subclass, a duck-typed object or the TEST_ONLY composition contract on the source path | A wrong type builds |
| A10 | `test_source_only_source_is_refused_by_qualification_consumers` | `verify_for` with a `ValidatedFrozenContract`, `ProductionExecutor` binding, `execution.compute` and `execution.evidence` all refuse a source-only source | Any consumer proceeds |
| A11 | `test_source_only_build_runs_the_same_source_checks` | With a synthetic source-only fixture signed in the test process: each existing source-pack negative (missing role, review mismatch, UNKNOWN date, population mismatch, capital mismatch) fails identically to the F1 path | Any negative passes on the source path |
| A6b | `test_self_signed_source_contract_with_matching_self_registry_is_refused` | A freshly generated key, a matching self-supplied registry and `source_trust`, and a valid signature are REFUSED against the pinned root; the shipped pin holds no test key | Any self-enrolled key validates |
| A10b | `test_every_production_source_consumer_is_allowlisted_or_verified` | The AST scan of `ops/` finds each `ProductionSource` / `.contract` use outside `production_source.py` either on the allowlist or preceded by `verify_for` in the same function; a planted unguarded consumer in a temp module fails the scan | An unguarded consumer passes |
| A16 | `test_p7_loaded_set_is_the_closure` | In a subprocess run of the driver on a synthetic fixture, the record's `loaded_closure` equals the set of modules actually loaded, including a module imported dynamically via `importlib.import_module` and a module imported and then deleted from `sys.modules`. Third-party distributions are recorded with version and hash, and `code_closure_sha256` recomputes. | A loaded module is missing, or a deleted module escapes |
| A13 | `test_source_truncated_disposition_only_at_interval_ends` | An end-of-interval truncated date is excluded as `source_truncated`; an interior one (`SOURCE_TRUNCATION_INTERIOR`), one whose reason does not name its slots (`SOURCE_TRUNCATION_REASON`) and a `policy_denied` truncation stand-in (`TRUNCATION_STAND_IN_RETIRED`) are refused by `validate_source_only_calendar` | The stand-in or an interior truncation builds |
| A14 | `test_review_companion_v2_reviewer_authored` | A v2 companion with an independent reviewer passes; a template, a v1 companion on the source path, or reviewer == producer, or a companion missing `reviewer` / `reviewed_at` / `notes` / `artifact_sha256` are refused | Self-certified or template reviews bind |
| A15 | `test_path_start_date_signed_and_consistent` | A mismatch with the startup policy, or a weekend date, is refused | An unsigned or inconsistent origin passes |
| A3b | `test_observed_digest_mismatch_refused_at_digest_check` | With the correct role set, the observed digest of one retained artifact is changed; the refusal is the observed-digest error (row 3), and the twin passes | The mismatch validates, or fails elsewhere |
| A6c | `test_revoked_or_removed_pin_key_refused` | A pin entry with `revoked_at <= now` refuses at validation (`SOURCE_KEY_REVOKED`); removing the key from the pin after issuance refuses the next `replay` (`SOURCE_KEY_REMOVED`) | A revoked or removed key is honored |
| A7b | `test_real_source_approval_refused_by_both_qualification_validators` | An otherwise-valid F1 contract and trust-domain fixture (the existing test fixtures) is re-signed with a genuine `APPROVE_T00_SOURCE_CONTRACT` source approval; `validate_frozen_contract` and `validate_qualification_trust_domain` each refuse with the scope mismatch or `SOURCE_KEY_IN_QUALIFICATION_DOMAIN`, and the twin passes | Either validator accepts, or refuses before reaching the approval |
| A10c | *Retired in revision 4* (the result registry was removed; see §2.6c) | — | — |
| A10d | *Retired in revision 4* (replaced by the hook's `P7_FORBIDDEN_IMPORT`, tested in A16c) | — | — |
| A12b | `test_receipt_expires_between_build_and_replay` | Validation and build succeed inside the window; with `_now()` advanced past `expires_at`, the next `replay_bracket` is refused (`SOURCE_APPROVAL_EXPIRED`) | A replay runs on an expired receipt |
| A16b | `test_dirty_tree_writes_no_p7_record` | A dirty closure path at start refuses with `P7_TREE_DIRTY`, and no record file exists afterwards | A record is written from a dirty tree |
| A16c | `test_p7_loaded_set_negatives` | Each case refuses with its own code and leaves no record: a first-party-named module loaded from a tree outside the code root (`P7_ORIGIN_OUTSIDE_ROOT`); an import of `c1_rail.qualification.part_a` (`P7_FORBIDDEN_IMPORT`); a call of `evaluate_replay` or of `simulate_path`, and a restored original attribute (`P7_FORBIDDEN_CALL`) *(revision 4.3)*; a first-party file edited mid-run (`P7_SOURCE_CHANGED_DURING_RUN`); `exec` of first-party bytes (`P7_UNAUDITED_EXEC`). Each has an unmodified twin that yields a record. | Any case yields a record |
| A17 | `test_accept_p7_record_from_bytes` | In a fresh process with no receipts, a MET record at closure A is accepted. After changing one recorded module to B, it is refused (`P7_EVIDENCE_STALE`). After advancing `now` past approval expiry, or revoking the key in the pin, it is refused at acceptance. A record produced at B is accepted. | Stale, expired or revoked evidence is accepted, or acceptance needs an in-process receipt |
| A19 | `test_two_independent_p7_runs_produce_identical_records` | Two fresh-process runs through `run_p7` on the same synthetic fixture produce records that are byte-identical after removing exactly the enumerated volatile fields | Any other field differs between runs |
| A20 | `test_driver_edit_is_reflected_or_refused` | Editing `p7_driver.py` changes its recorded hash and `code_closure_sha256`. An old record presented after the edit is refused (`P7_EVIDENCE_STALE`). A launch that bypasses the bootstrap, running the driver directly, or a bootstrap string whose hash differs from `P7_BOOTSTRAP_SHA256`, yields no record (`P7_BOOTSTRAP_MISMATCH`). Each case has an unmodified twin that yields and accepts a record. | A driver edit is absent from the closure, or a bypassed launch yields a record |
| A21 | `test_hand_constructed_record_over_valid_contract_is_not_reproduced` | A record built by hand around a valid signed contract and approval, with plausible hashes and labels, or with one result label altered, or with a forged `bootstrap_sha256`, is refused by `accept_p7_record` (`P7_RECORD_NOT_REPRODUCED`); the genuine twin is accepted | A constructed record is accepted |
| A22 | `test_artifact_changed_after_run_is_stale` | After a genuine MET record, changing one retained artifact (a source-role byte, a panel byte, and separately a pinned port byte) in the current artifact root makes acceptance refuse `P7_EVIDENCE_STALE` **before** any re-execution. A spy asserts that no process was launched. | A stale artifact is accepted, or acceptance re-executes first |
| A23 | `test_bootstrap_runs_no_site_pth_or_sitecustomize` | In a temporary copy of the interpreter's global site-packages layout (or a venv made for the test), plant a `sitecustomize.py` and a `.pth` file with an `import` line; each writes a marker file when executed. Launching through `run_p7` with the pinned bootstrap leaves no marker from either and does not execute them. Third-party packages still import from the inserted `site-packages`, and the record lists the `.pth` file's hash under `unexecuted_pth`. The unmodified twin (the same layout with no planted files) yields a record. A control launch **without** `-S` shows that the markers do fire, proving the planted files are live. | Any marker is written under the bootstrap, third-party imports fail, or the control shows the plant is inert |
| A18 | `test_calendar_fact_must_bind_calendar_producer` | A calendar whose fact names another retained role with that role's correct digest is refused (`CALENDAR_FACT_ROLE`), although `_fact` alone would accept it | A non-producer fact binds |
| A12 | `test_source_only_replay_bracket_fresh_engines_and_label` | **End to end, with the guards intact.** A synthetic source-only contract, signed in-process with only the pinned root monkeypatched, validates. `build` succeeds, and `replay_bracket` on a path with a consumed intrabar split passes `_verify_integrity` and returns a `SourceOnlyBracket` from two separate engines. The label is `T00_P7_SOURCE_ONLY`, the policy is 1%/0.40, and `verify_for` on the same source still raises `SOURCE_ONLY_NOT_QUALIFICATION`. No guard function is patched. | Shared state, a missing label, a changed policy, a patched guard, or a build/replay failure |

**Regression.** The Task 2 acceptance nodes named on the card, the full `tests/ops/qualification` suite, `tests/ops/test_book_adapters_parity.py` and `fp.ps1 check` all stay green.

## 6. Open items for review

1. **Tail session, RULED 2026-09-30.** The coordinator ruled (a) now and (b) in the design. The r2 pack carries the `policy_denied` stand-in; §2.6a retires it.
2. **Same-key reuse.** Key separation is code-enforced by ID and scope only; reusing the same public key across classes is prevented by procedure (§2.3).
3. **`path_start_date`, ACCEPTED as proposed.** It is an explicit signed contract field (§2.2).
4. **Review companions, CORRECTED.** The first pack's producer-written `ACCEPTED` companions are UNREVIEWED drafts. The r2 pack emits templates plus producer notes only; §2.6b makes companions reviewer-authored.
5. **Words in v1 companions.** The v1 `_review` schema is closed, so the statements the coordinator required cannot live inside the v1 companion bytes. They are in the r2 `reviewer-notes.json` for the reviewer, and §2.6b's `notes` field carries them in the signed companion.
