# Qualification invariant gate evidence

Scope: structural-closure Task 9's invariant gate, protected synthetic N1_ONLY.
The canonical manifest contains 621 distinct exact test IDs across nine invariant
families. It selects test files; the inventory plugin records actual collection,
and the strict JUnit parser requires completed execution of every listed case.
Missing, renamed, skipped, failed and setup-error cases fail the gate. Duplicate
passes cannot erase adverse outcomes; successful subtests cannot replace their
parent's completion. Hash-bound child reports retain the existing recorder rules.

Both fresh Linux CI hosts run this gate for code changes. The workflow no longer
offers a host-readiness-only substitute. Final record acceptance additionally
requires completion, zero exits, unchanged source, complete capture, valid report
and artifact hashes, canonical manifest identity and successful owned cleanup.
Offline exact-revision verification also requires a clean checkout at that SHA.

## Review-family dispositions

| Invariant | Trigger and related consumers | Disposition/evidence |
| --- | --- | --- |
| QPOL | Coherently signed wrong product; policy and G1 admission | Structural rejection, plus controlled removal of basis comparison. |
| QLEG | Bound nonempty registry; legality, source and service admission | Rejected before reservation/dispatch; controlled registry-validation removal. |
| QART | Valid-shaped substituted role content; builder, G5 and proposed result | Compare against independently reconstructed capture, including coherent inventory rehash; controlled final-comparison removal. |
| QPLAN | N1/N2/Part B/Part A schemas, plans and seed consumers | Exact counts, typed outcomes and literal seed vectors cover existing library consumers; protected later-stage execution remains unsupported. |
| QEXEC | Raw claims, worker failure and interrupted capture | Service-owned launch/capture/attestation; public claims cannot confer execution authority; real Linux negative controls required. |
| QKEY | Release/domain/result binding and TEST_ONLY/OPERATOR consumers | Domain/key mismatch tests and post-admission unit refusal at service, worker and G5. These unit guards do not establish an installed OPERATOR route. |
| QSTATE | Concurrent submit, restart, expiry, VOID and public exact retry | Model/store/service checks plus actual Linux lifecycle and both writer orders; original receipt preserved separately from current eligibility. |
| QISOL | Client and running worker access | Actual UID denials and positive reads on Linux; existing trusted administrator/privileged qexec model retained. |
| QGATE | Missing/renamed/skipped/failed reports, legacy public paths and invalid records | Actual pytest subprocess negative controls, strict parser, clean-revision validation; retired v1/full-PASS/later-stage paths reject. |

Matching OPERATOR installation metadata with production execution disabled is
schema-valid. The N1 execution consumers still refuse OPERATOR execution. This
gate does not claim full-campaign execution, production activation, private-source
verification, malicious-qexec confinement, merge or deployment.

## Local verification

Implementation checkout: `.worktrees/qualification-lifecycle-coverage`, branch
`codex/qualification-lifecycle-coverage`, working tree based on `8d48bd9`.
Doctor passed: operations Python 3.13.2 at
`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, 62 locked
packages, cryptography 50.0.1. The launcher bootstrap/recorder and Git hook use
Python 3.14.3 separately; that is not the operations interpreter.

- Initial process-test RED: 12 failed because manifest execution was absent,
  record `20260918T140343Z-2d6b4a9fbe11`.
- Parser/runner GREEN: 55 passed, one Windows symlink-privilege skip,
  `20260918T140526Z-ce8cc749b01a`. Expanded selection: 74 passed, same skip,
  `20260918T140952Z-bd896e8f1d86`.
- Dirty exact-revision regression reproduced the gap before its guard was added:
  `20260918T141509Z-0defe19d195f`, one intended failure.
- Planned broad command, with the new gate and boundary-wrapper tests added:
  `./fp.ps1 --workers 2 python -m pytest tests/ops/qualification
  tests/ops/test_phase3_provenance_acceptance.py tests/ops/test_qualification_isolation.py
  tests/test_certification_power.py tests/test_qualification_authority_boundaries.py
  tests/test_qualification_invariant_manifest.py tests/test_qualification_invariant_gate.py
  tests/test_qualification_boundary_verification.py -q --tb=short`.
  Record `20260918T141820Z-54367d90ae6f`: **1096 passed, one failed, one skipped**.
  The sole failure was the new G5 unit fixture's empty snapshot being rejected
  before its intended authority guard; this run remains failed.
- Corrected fixture uses the real snapshot encoder. Affected service, gate,
  parser, boundary-wrapper and seed tests reran using the checkout launcher
  (`C:/Python314/python.exe -I scripts/fp.py --workers 2 python -m pytest ...`):
  **97 passed, one Windows symlink-privilege skip**, record
  `20260918T144248Z-0fd831db136f`. Unchanged broad-suite results remain applicable;
  no all-green rerun of the full 1098-case command is claimed.
- `./fp.ps1 check`: exit 0, record `20260918T141541Z-f71f7403c46f`;
  72 evidence-store cases, three existing skips, private Pine/heavy-data absence
  disclosed by the gates. No private-data acceptance is claimed.
  Repeated after both corrections using `C:/Python314/python.exe -I scripts/fp.py check`:
  exit 0, stable complete record `20260918T144501Z-1e047ebf2a52`, same 72/3 result
  and private-artifact limitations.

Records are retained under `.cache/fp-verification/<record>/record.json` with
commands, source inventories/fingerprints, actual reports and logs. Completed
local runs above have stable source and complete capture; deliberate RED records
retain their nonzero exits. Linux acceptance requires zero skips.

## Controlled mutations

`tests/ops/qualification/mutation_check.py` copies the candidate into a retained
disposable Git checkout, runs an unchanged control, changes one validation, and
requires the named test call to fail with `DID NOT RAISE`. Collection/setup errors
are inconclusive. Each source file is restored and compared byte for byte.

| Mutation | Required test |
| --- | --- |
| Disable `basis != policy.original_basis` in `policy.py` | `test_semantic_admission.py::test_resigned_wrong_product_reaches_semantic_rejection` |
| Disable `validate_registry(..., expected_rows={})` in `legality.py` | `test_legality_evidence.py::test_bound_nonempty_registry_is_not_legality_pass` |
| Disable final envelope/role-content equality in `evidence.py` | `test_artifact_acceptance.py::test_coherent_valid_role_content_still_must_equal_captured_reconstruction` |

The first run in `.cache/qualification-mutations/20260918-invariant-gate` killed
all three mutations with valid controls, but its summary hashed LF strings while
Windows retained CRLF patch files. It is preserved as superseded evidence, not a
valid patch-hash inventory. The runner now writes patch bytes, hashes retained
bytes and restores original source bytes. Fresh evidence is recorded separately
under `.cache/qualification-mutations/20260918-invariant-gate-bytes`.

Fresh command: `C:/Python314/python.exe -I scripts/fp.py python
tests/ops/qualification/mutation_check.py --output
.cache/qualification-mutations/20260918-invariant-gate-bytes`, exit 0. All three
controls passed; each mutation produced exactly one failed call, zero setup
errors/skips, and the intended `DID NOT RAISE` assertion. All six records have
stable source and complete capture. Retained patch hashes were independently
recomputed, and all three restored files match the implementation bytes.
Disposable source copy: `C:/Temp/fp-qualification-mutations-5jl3kp20`.
Common control fingerprint:
`8ee3e3a0a4d1fd7cd2075c151f90e26ccaf9cc7e57f56d588891bc02d9b832b4`.

| Mutation | Retained patch SHA-256 |
| --- | --- |
| Product basis | `1a01143feb09b0c1d85a4e6a5f2b7fbbbf2d21e1e37cffe1f1e703ab933b5204` |
| Registry | `c6cb0fd8ac1d477ac6cfe47fb3045813e408a467f109ccdb45998e33783de1b3` |
| Role content | `2056a8df9cc4a8c16d4a640641bcd4acbaa61e572303d54dec6ba16849774409` |

Independent read-only review examined the gate and affected consumers, recomputed
all eight seed vectors independently, and identified the G5 fixture and dirty
revision issues. Those findings and the patch-byte correction are resolved in
code; final remote acceptance remains subject to the records below.

## Linux acceptance

Pending the identified candidate's two-host run and retained-record audit.
