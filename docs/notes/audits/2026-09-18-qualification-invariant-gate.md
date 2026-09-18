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
The manifest has `text eol=lf` pinned in `.gitattributes`: its SHA-256 is
`84c35fb57d708eb1785996a95a5fd21dce11dcf843d73f7a82a377242b081e30`.
This avoids Windows checkout translation changing offline evidence comparisons.
The local LF bytes and the tested Linux commit's manifest have the same Git blob
`358698b9fe857443176fa44f95cb1236ef9b9ce4`; the EOL pin changes no Linux bytes.

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
  Broad-run source fingerprint:
  `a2b9cd6acca7b9f059c3a50a8c4c5de76b1fd37ca9026de79cf2fea19a4b44c0`;
  corrected-selection fingerprint:
  `2fe480611614dd3e3192d40b00adb97814f2a77b0fb4a83e3735ad6f22038052`.
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

[Run 35358450882](https://github.com/Joshua-Asante/first-passage/actions/runs/35358450882)
passed on both fresh Ubuntu hosts at **`f3099bb5a1675e8cee8177656d0fa24502ce6a86`**.
Each host: **621 collected, 621 passed, zero failures/errors/skips**. Both records
are completed, zero-exit, source-stable, capture-complete, free of capture/report
errors, and have successful owned cleanup. Both source checkouts were clean with
fingerprint `b24cfe4a35a585b9c9f7b5ba8fa1cc422b3232c4ceb2e94144aad74477bf6cab`.

| Host | Record | Journal SHA-256 |
| --- | --- | --- |
| 1 | [b9632b17ef644cdb91f71eccee242752](../../../.cache/qualification-linux/35358450882/qualification-host-readiness-1/b9632b17ef644cdb91f71eccee242752/record.json) | `44d2a680fdf03fa9d1956cb02ee8d6ba3947155d7278d303d010c8ab4b98966e` |
| 2 | [468e5d5c45314eeaa3a366f21175b98b](../../../.cache/qualification-linux/35358450882/qualification-host-readiness-2/468e5d5c45314eeaa3a366f21175b98b/record.json) | `ebf59ed8b6f48d27c82ee11766dde832dcba5e3f1b3506cd5119887ea4def0e3` |

The workflow used operations Python **3.12.3**, selected by each checkout's
launcher after doctor, and ran:

```sh
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" python \
  scripts/qualification_boundary_verification.py --test-only --manifest "$manifest"
```

The owned-process-group child invoked `python -m pytest -c <checkout>/pyproject.toml
--rootdir=<checkout> -o addopts= -n 0 -p scripts.pytest_qualification_inventory
-p scripts.pytest_junit_subtests --qualification-collection=<record>/collection.json
<manifest-selected-files> -q --tb=short --junitxml=<record>/junit.xml`.
Each record retains the full argv and exact interpreter path. The retained
collection, manifest, JUnit and invariant decision all agree.

The offline CLI returned `passed: true` separately for each downloaded record:

```text
C:/Python314/python.exe -I scripts/fp.py python -m scripts.check_qualification_invariants
  --record .cache/qualification-linux/35358450882/<host>/<record>/record.json
  --expected-revision f3099bb5a1675e8cee8177656d0fa24502ce6a86
```

The [combined retained-evidence audit](../../../.cache/qualification-linux/35358450882/invariant-lifecycle-audit.json)
also passed via `C:/Python314/python.exe -I scripts/fp.py python
.cache/audit_invariant_lifecycle.py .cache/qualification-linux/35358450882
f3099bb5a1675e8cee8177656d0fa24502ce6a86`. Per host it checked 27 executions,
one reservation and at most one actual start per attempt, complete event chains
and object hashes, original receipt/authentication bindings, 11 attempt-bound
checkpoint controls, all four writer orders, and both permission identities.
Actual client UID 61000 had 10 probes; actual worker UID 65532 had 12 probes,
including positive reads and denied key/journal/code/socket access as applicable.

Both hosts used profile SHA-256
`f238d5a1ff126fbe289c69e6c6022f82c5bea24969c6b9833181eebccb379348`, policy SHA-256
`41646a3ce77f03a83ba8a4ad4dd9d0aa865f150cab7b6f1928895cbc60c0d4df`, and base image
`python@sha256:afc139a0a640942491ec481ad8dda10f2c5b753f5c969393b12480155fe15a63`.
The audit recomputed profile identity, located the hash-verified retained policy,
and matched every worker-image/release code hash to the recorded candidate source.

| Host | Worker image | Environment report SHA-256 |
| --- | --- | --- |
| 1 | `sha256:4684d7f889919256fc434a82d4b5a7bc22f5565c1f99947ba85a5fd321429731` | `9fd40bd0960fdd8f8017bf5bde6a25b1c1c919e06b3c14b5d8695f87c49f26f1` |
| 2 | `sha256:22c33ce8f86cbeaa36d8eac5eadda6d753623571cb29c1fa65aaf103ba3d9c30` | `e2077e635f8ba8022ad67ab7491d99a57743d1f5d499a8ceef6ee5b85af50526` |

Raw records, collection, reports, journals, objects, controls and permission
reports remain under `.cache/qualification-linux/35358450882`; both workflow
artifacts retain the same non-secret host evidence for 14 days. Local evidence
and both mutation copies are preserved. The final documentation/EOL-pin commit
changes no runtime/test/manifest blob verified by this Linux run.

The selected invariant-gate outcome is verified. Full-campaign and production
prerequisites remain open. No PR, merge or deployment was performed.
