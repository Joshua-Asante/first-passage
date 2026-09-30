# T00 source-only contract: design (Phase A)

**Date:** 2026-09-30.
**Status:** DRAFT for review. This is a design only. It adds no code, and no file below is admitted for editing until a later amendment to the [dispatch card](../../briefs/handoffs/2026-09-30-t00-p7-tasks-3-4-dispatch.md) admits it.
**Authority:**
- the operator's 2026-09-30 Ruling 1, "Source-only contract" ([P7-closure packet §7, Operator rulings 2026-09-30](../../briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md#operator-rulings-2026-09-30));
- the coordinator's sequencing in [card §8.1](../../briefs/handoffs/2026-09-30-t00-p7-tasks-3-4-dispatch.md#81--coordinator-sequencing-after-the-checkpoint-1-return-2026-09-30).

**Review path:** the coordinator reviews, then Codex, then Joshua accepts.
**Code read at:** `claude/t00-p7-tasks-3-4` @ `e3d95b3`, whose production code equals the Task 2 head `672d49f`.

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
| `source_trust` | `{source_key_ids, trusted_key_sha256}` | a sorted nonempty list of key IDs, each carrying the `source:` prefix, and exactly one fingerprint per enrolled ID |
| `refusals` | `["QUALIFICATION_STAGES","BUDGET","DECISION_RULES","SCREEN","MONTE_CARLO","SEAL","ADMISSION","DEPLOYMENT"]` | exact list; it is declarative, and enforcement is §2.6 |

There is no `replay`, `result_plan`, `approval_policy`, `coverage`, `clocks`, `trust_domain_sha256` or `policy_sha256` field. A document carrying any F1 field is refused, and so is a document missing any field above.

### 2.3 Signing scope, approval name and key-class separation

**Envelope.** The existing detached-approval envelope and verifier, `contract.verify_detached_approval`, is reused unchanged: `qualification_approval/v1`, Ed25519, with a canonical payload.

**Scope.** The scope is **`APPROVE_T00_SOURCE_CONTRACT`**, and `subject_sha256 == contract_sha256 ==` the SHA-256 of the canonical contract bytes. It is distinct from `FREEZE_F1` and `BIND_QUALIFICATION_TRUST_DOMAIN`, and because the scope is inside the signed payload, a signature for one scope never verifies for another.

**Authority.** `authority_class` is `OPERATOR`. `verify_detached_approval` is called with `allow_test_authority=False`, so no TEST_ONLY key verifies.

**Key-class separation.** There are two directions, both enforced in code:
- **Source validator:** every signing key ID must start with `source:`, must be listed in `source_trust.source_key_ids`, and its public-key SHA-256 must equal `trusted_key_sha256[key_id]`.
- **Qualification validator:** `trust_domain.validate_qualification_trust_domain` and `contract.validate_frozen_contract` refuse any enrolled key ID that starts with `source:`, raising `SOURCE_KEY_IN_QUALIFICATION_DOMAIN`. This is the one edit to the qualification path.

**Residual.** No shared registry exists, so code cannot stop the operator from enrolling the *same public key* under a non-`source:` ID in a later qualification domain. The ceremony therefore requires a **dedicated operator key**, generated only for source contracts. This rests on procedure, not code, and is recorded as such.

**Trust root.** The `trusted_keys` mapping is supplied by the caller, as it is for F1: it is the operator's public-key registry (`qualification_trusted_keys/v1`, `authority_class` OPERATOR). The contract's `source_trust` fingerprints must match it. A contract that self-enrolls a key without a matching registry entry fails.

**Validity window.** `issued_at <= now < expires_at` is checked at build. Task 4 must run inside the window.

### 2.4 Role set (closed)

The set is exactly 25 roles. There are no optional roles, and any extra or missing role is refused.

| Group | Roles | Bytes and check at build |
|---|---|---|
| Historical pins (11) | `step6_admission_contract`, `step6_independent_review`, `step6_accepted_run`, `step3_admission_contract`, `step3_evidence_index`, `step3_independent_acceptance`, `aegis_runtime_port`, `striker_runtime_port`, `vanguard_runtime_port`, `orb_runtime_port`, `historical_effective_inputs` | SHA-256 equals `ACCEPTED_HISTORICAL_PINS`; `parse_historical_admission`; the seven-bundle Step 6 format |
| Admitted panels (4) | `panel_aegis_6j`, `panel_dj30_mym_p250`, `panel_vanguard_mgc`, `panel_orb_mnq_v7` | each digest equals the Step 3 admission's panel digest for that leg (the Aegis attested prefix is `8ae083d0…`); `decode_admitted_csv`; interval bounds |
| Settings successor (1) | `effective_settings_successor` | SHA-256 equals `RUNTIME_EFFECTIVE_INPUTS_SHA256`; `_qualification_snapshots` checks (ORB `qty == 1`) |
| Deadline facts (1) | `calendar_producer` | the Ruling-2 fact record (`t00-p7-calendar-deadline-facts/v1`); every calendar `fact` must bind this role and digest |
| Source roles (8) | `source_startup_policy`, `source_calendar`, `source_calendar_review`, `population_index`, `population_index_review`, `schedule_execution_evidence`, `schedule_execution_evidence_review`, `cost_model` | the existing parsers in `production_source.py`, unchanged |

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

### 2.6 What `ProductionSource.build` does and refuses

**Dispatch.** `build(contract, *, artifact_root)` dispatches on the exact type of `contract`:
- `ValidatedFrozenContract`: the existing path, unchanged.
- `ValidatedSourceContract`: the new path, below.
- Anything else: refused.

**New path.** Once the source domain is resolved (`book_adapters._source_domain(contract)`, a sibling of `_qualification_domain` that requires the source receipt), it runs the **same** steps as today, `_prepare_domain_inputs` → `_build_from_prepared`, with the same parsers and checks: reviews, calendar, population index, `validate_calendar` / `validate_provider_generation` / `validate_coverage`, `UNKNOWN_SOURCE_DATE` refusal, adapter-capital equality, `build_panel`, schedule evidence and costs. The only differences are:
- the domain object (`SourceTrustDomain`) and the loader entry (`_load_domain_adapters` accepts either validated domain, dispatching on its type);
- the issued source records `evidence_class = "T00_P7_SOURCE_ONLY"`.

**Refused for a source-only source.**
- `ProductionSource.verify_for(contract)` raises `SOURCE_ONLY_NOT_QUALIFICATION` when `self.contract` is a `ValidatedSourceContract`. That covers every current qualification consumer: `production.py` executor binding, `execution/compute.py` and `execution/evidence.py`. None of them runs.
- The source-only path calls no stage, Part A, budget, adjudication, seal or screen code. `replay`, `replay_bracket` and `proof` stay available, because each checks the path against its own issued sessions.
- `_build_composition` and the TEST_ONLY domain are untouched, and a `TEST_ONLY` key cannot sign a source contract.

**Invariants kept.**
- `candidate_book_protection_policy()` stays at 1%/0.40, and `core/dd_protection.py` is not touched.
- R1 and R2 each run on a fresh engine.
- The frozen Task 2 interface is unchanged.

### 2.6a Typed truncation disposition (replaces the POLICY_DENIED stand-in)

**Problem.** A panel that ends or starts mid-session leaves a source date with no active-window bar, like the 2026-09-03 tail. Today the only way to exclude it is `policy_denied`, which the coordinator accepted on 2026-09-30 as a stand-in, not a venue fact.

**Change.**
- Add `SourceDayStatus.SOURCE_TRUNCATED = 'source_truncated'` in `clock.py`.
- Add `'source_truncated'` to the exclusion reasons `parse_population_index` allows.
- `ProductionSource._build_from_prepared` already relabels denied dates with their typed status, so no further change is needed there.

**Rules.**
- A `source_truncated` row must carry an empty `venue_deadlines` and a reason naming the truncated slots.
- It may appear only at `coverage_start` or `coverage_end`. An interior truncation is refused as `UNKNOWN_SOURCE_DATE`.
- At the source-only contract build, a `policy_denied` row whose reason begins `panel truncated` is refused, which retires the stand-in. The source pack is regenerated with the typed status before signing.

### 2.6b Review companions are reviewer-authored

**The rule.** A review companion is written by the reviewer, after the review, over the exact reviewed digest. A producer may emit only a template, named `*.UNREVIEWED-TEMPLATE.json`, and a template never satisfies a review role.

**Schema.** The companion schema becomes `qualification-source-review/v2` and adds three fields to the v1 fields:
- `reviewer`: a nonempty identity, such as the coordinator session or a named reviewer;
- `reviewed_at`: a UTC instant;
- `notes`: a nonempty list of statements. For the source calendar and population index these must include the truncation, head-partial and residual statements.

**Validation.** `_review` in `production_source.py` accepts v2 only on the source-only path, and requires `reviewer` to differ from the artifact's producer identity recorded in the contract's `artifacts[].producer`. v1 stays unchanged for the F1 path. Self-certification (a producer equal to the reviewer) is refused as `REVIEW_NOT_INDEPENDENT`.

### 2.7 Labelling of P7 evidence

Every artifact produced under a source-only contract carries:
- `evidence_class: "T00_P7_SOURCE_ONLY"`, the contract SHA-256 and the approval SHA-256;
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
| 11 | `build` succeeds | The issued `ProductionSource` has `evidence_class == "T00_P7_SOURCE_ONLY"`; `replay_bracket` returns `BracketReplayResult(r1, r2)` from two fresh engines |
| 12 | `now` is outside the approval window at build | Refused; re-signing is an operator act |
| 13 | A calendar row is `source_truncated` at an interval end | Excluded with a typed reason; FULL omits it |
| 14 | A `source_truncated` row falls in the interior, or a `panel truncated` `policy_denied` stand-in appears on the source-only path | Refused |
| 15 | A review companion is a template, or v1 on the source-only path, or has reviewer equal to producer | Refused (`REVIEW_NOT_INDEPENDENT` for self-review) |
| 16 | `path_start_date` in the contract differs from the startup policy, or is not a weekday | Refused |

## 4. Files it would touch (admitted only by a later amendment)

| File | Change |
|---|---|
| `ops/c1_rail/qualification/contract.py` | Adds `SOURCE_CONTRACT_SCHEMA`, `SOURCE_SCOPE`, `ValidatedSourceContract`, `validate_source_contract`, `require_validated_source_contract` and a separate issuance registry. `validate_frozen_contract` gains the `source:` key-ID refusal. No existing F1 rule changes. |
| `ops/c1_rail/qualification/trust_domain.py` | Adds `SourceTrustDomain` (compiled from constants, with no signed domain bytes). `validate_qualification_trust_domain` refuses `source:` key IDs. |
| `ops/c1_signal_daemon/book_adapters.py` | Adds `_source_domain(contract)`. `_load_domain_adapters` accepts either validated domain type. Historical and qualification loaders are unchanged. |
| `ops/c1_rail/qualification/production_source.py` | `build` dispatches on type, the issued source records `evidence_class`, and `verify_for` refuses source-only for qualification consumers. `parse_population_index` allows `source_truncated`. `_review` accepts v2 on the source-only path (§2.6b). The other parsers are unchanged. |
| `ops/c1_rail/qualification/clock.py` | Adds `SourceDayStatus.SOURCE_TRUNCATED` (§2.6a) |
| `tests/ops/qualification/test_source_contract.py` (new) | Acceptance tests A1–A10 below |
| `tests/ops/qualification/test_production_source.py` | A11–A12, plus Task 4's real-path wiring |
| `tests/ops/qualification/test_trust_domain.py` / `test_contract.py` (existing) | The `source:` refusal cases, A7 |

`clock.py` changes only by the new enum member. No change to `replay.py`, `model.py`, `book_policy.py`, `core/dd_protection.py`, runner, screen, seal or execution code.

## 5. Acceptance tests and falsifiers

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
| A13 | `test_source_truncated_disposition_only_at_interval_ends` | An end-of-interval truncated date is excluded as `source_truncated`; an interior one and a `policy_denied` truncation stand-in are refused | The stand-in or an interior truncation builds |
| A14 | `test_review_companion_v2_reviewer_authored` | A v2 companion with an independent reviewer passes; a template, a v1 companion on the source path, or reviewer == producer are refused | Self-certified or template reviews bind |
| A15 | `test_path_start_date_signed_and_consistent` | A mismatch with the startup policy, or a weekend date, is refused | An unsigned or inconsistent origin passes |
| A12 | `test_source_only_replay_bracket_fresh_engines_and_label` | `replay_bracket` returns two results from separate engines; the issued source's `evidence_class == "T00_P7_SOURCE_ONLY"`; the policy is 1%/0.40 | Shared state, a missing label or a changed policy |

**Regression.** The Task 2 acceptance nodes named on the card, the full `tests/ops/qualification` suite, `tests/ops/test_book_adapters_parity.py` and `fp.ps1 check` all stay green.

## 6. Open items for review

1. **Tail session, RULED 2026-09-30.** The coordinator ruled (a) now and (b) in the design. The r2 pack carries the `policy_denied` stand-in; §2.6a retires it.
2. **Same-key reuse.** Key separation is code-enforced by ID and scope only; reusing the same public key across classes is prevented by procedure (§2.3).
3. **`path_start_date`, ACCEPTED as proposed.** It is an explicit signed contract field (§2.2).
4. **Review companions, CORRECTED.** The first pack's producer-written `ACCEPTED` companions are UNREVIEWED drafts. The r2 pack emits templates plus producer notes only; §2.6b makes companions reviewer-authored.
5. **Words in v1 companions.** The v1 `_review` schema is closed, so the statements the coordinator required cannot live inside the v1 companion bytes. They are in the r2 `reviewer-notes.json` for the reviewer, and §2.6b's `notes` field carries them in the signed companion.
