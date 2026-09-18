# Task 9 invariant gate handoff — 2026-09-18

Implementation base: `0cc800f8b2197465a6e3f2caef32afacb13fb6d4`.
Executor: `/root/invariant_gate`; combined acceptance stays with `/root`.
Scope remains N1_ONLY / TEST_ONLY. No production start or E1 acceptance is authorized.

The canonical manifest records exact pytest node IDs for QPOL, QLEG, QART,
QPLAN, QEXEC, QKEY, QSTATE, QISOL and QGATE. The boundary recorder executes
those cases plus the full real boundary directory, records actual same-session
collection, and validates retained JUnit. Collection alone cannot satisfy a case.
Missing, renamed, skipped, failed and errored critical cases fail the run. Existing
source stability, complete output capture, report integrity and cleanup gates
remain in force. Cleanup now additionally requires explicit `ok: true`.

The two-host workflow always uses `--test-only`; host readiness cannot replace it.
There are no pull-request path filters or optional boundary inputs. Repository
branch protection must require `Qualification execution boundary (1)` and `(2)`;
workflow YAML cannot establish that external setting. No Linux run is claimed here.

## Local evidence

Both isolated checkouts passed `./fp.ps1 doctor`, selecting
`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python 3.13.2,
62 matched locked packages, cryptography 50.0.1. All Python used those launchers.
Records are retained in each checkout's `.cache/fp-verification`.

- Gate RED: `20260918T153227Z-d85f40cd5a4c`: 2 failed, 43 passed, 1 skipped;
  canonical manifest and collection plugin absent. Wrapper RED:
  `20260918T153355Z-d232242574a4`: 4 failed, 5 passed; required invariant/cleanup
  helpers absent.
- Gate GREEN: `20260918T153439Z-2e79ca8bcede`: 54 passed, 1 skipped. The skip is
  an existing Windows symlink-creation capability test, not Linux acceptance.
- Required non-integration manifest files plus both gate test files:
  `20260918T153749Z-4882fa18f593`: 330 passed, the same 1 skip, exit 0,
  completed, stable source. Exact command and source fingerprint are in the record.
- Collection `20260918T153312Z-8994f0f09514` supplied exact manifest spellings;
  this is selector verification, not evidence of Linux execution.

## Controlled mutation evidence

The separate disposable checkout `.worktrees/task9-mutations`, also based on
`0cc800f`, retained exact unified diffs, stdout/stderr and commands under
`.cache/task9-mutations/{basis,registry,role-content}.{diff,txt}` and `results.json`.
Each mutation was restored byte-for-byte in a finally block before the next.
No import/setup error counts as mutation detection.

| Mutation | Required behavioral test | Result / record |
|---|---|---|
| `policy.py`: change `if basis != policy.original_basis:` to `if False:` | `test_semantic_policy.py::test_pristine_50k_cannot_describe_fixed_100k_product` | 1 failed, DID NOT RAISE ValueError; `20260918T153606Z-b3db17adc6f7` |
| `legality.py`: replace `validate_registry(geometry_bytes, expected_rows={})` with `pass` | `test_legality_evidence.py::test_resigned_nonempty_registry_rejected_before_source_construction` | 1 failed, DID NOT RAISE ValueError; `20260918T153657Z-0279bebee711` |
| `evidence.py`: return at entry to `compare_n1_evidence` | `test_evidence_reconstruction.py::test_consistently_rehashed_artifact_is_not_equivalent` for all five roles | 5 failed, DID NOT RAISE ValueError; `20260918T153728Z-b6e0ee666e41` |

All test paths in the table are under `tests/ops/qualification/`. The production
paths are under `ops/c1_rail/qualification/`. The third mutation bypasses the
entire role-content comparator, including internal projection checks; the required
coherently rehashed substitutions all escape and their assertions fail.

After restoration, `git diff --exit-code` was clean and the same seven tests
passed: `20260918T153813Z-407c6b90584c`, completed, exit 0, stable source.

## Family disposition and return boundary

- QPOL/QLEG: wrong product and retained registry triggers are covered by independent
  negative tests and nearby positives; controlled mutations prove those tests detect
  removed checks. Admission still precedes source construction and replay.
- QART: all five N1 roles and N1/N2/Part B/Part A prefix schema tests are pinned;
  consistent byte substitution is detected. Future prefix schema tests confer no E1
  execution authority.
- QPLAN: coherent N1/N2/Part A seed substitutions and signed Decimal boundaries are
  pinned. The existing fixed vector covers one N1 stream, not every seed/probability
  consumer requested by the spec. Broader independent exact vectors remain an
  acceptance obligation; this manifest does not claim they already exist.
- QEXEC/QSTATE/QISOL: real Linux launch, capture, G5, retry, interruption, expiry,
  VOID and permission cases are mandatory. This Windows run cannot discharge them.
  Coordinator-owned lifecycle/archive and credential additions must be appended
  by exact collected IDs at integration and executed on the final source.
- QKEY/QGATE: domain/release/result role checks and all legacy active entry guards
  are pinned. Missing attestation and full PASS/seal cannot gain authority from a
  report; final integration review remains required.

Return boundary: provide reviewable local commit and evidence to coordinator.
Combined Linux acceptance, complete seed/probability vector coverage, new lifecycle
selector integration and branch-protection configuration are not claimed complete.

Repository gates: `./fp.ps1 check`, record `20260918T154103Z-3405c90336be`,
completed, exit 0, stable source and complete capture. Evidence-store tests: 72
run, 3 existing skips. Missing private Pine sources/data/heavy artifacts remain
unverified; the gate emitted its existing absent-tree advisories. No gate failure
was observed. `git diff --check` passed.

## Bounded QPLAN vector follow-up

The coordinator authorized a separate missing-vector follow-up after the initial
handoff. No production code or seed/probability formula changed. New fixed seed
fixtures retain literal ASCII preimages and SHA-256-derived integer seeds, generated
independently with standard-library hashing and no imports from qualification code.
Tests consume frozen integers; they do not generate expected values by calling the
production seed helper.

`test_seed_probability_vectors.py` now checks the actual stage runner's separate
probe/FULL/H1/H2 seeds for N1/N2/N3 under both synthetic and qualification domain
discriminators, retained seed identities and source-population digests, orchestration
stage plans, Part A pilot outer/inner and four-panel outer/path streams, retained
Part A plans, and the representative Part A benchmark's outer/inner streams.
All are consistency-only fixtures; internal qualification-domain mechanics tests
confer no production execution authority and do not enable N3 or E1.

New probability vectors exercise actual N1 screening and N2/N3 confirmation
consumers. At n=4,p=1/2 the exact binomial coefficients are (1,4,6,4,1)/16;
alpha=5/16 therefore permits one failure and requires three fast passes. Cases
pin each cutoff and the adjacent failure/speed outcome. N1 checks the exact
one-quarter boundary and a Decimal value immediately below it. Existing fixed
calculator/binomial, retained-result Decimal, Part B separation and Part A
percentile/expansion vectors are selected for mandatory QPLAN inclusion rather
than duplicated.

`./fp.ps1 python -m pytest tests/ops/qualification/test_seed_probability_vectors.py
 tests/ops/qualification/test_part_a.py tests/ops/qualification/test_adjudication.py
 tests/ops/qualification/test_result_adjudication.py tests/test_certification_power.py
 -q --tb=short -p scripts.pytest_qualification_collection
 --qualification-collection=.cache/task9-vectors-collected.json`:
169 passed, zero skips, record `20260918T154725Z-06d69e2ca564`, completed,
exit 0, stable source, complete capture. Interpreter remains launcher Python 3.13.2.
Initial test record `20260918T154621Z-9a47815d4ac8` had six failures from a
transcription error in the H2 literal digest; independent SHA-256 of the literal
ASCII `["b"]` corrected that fixture. This was not a production defect.

Coordinator integration owns merging `.cache/task9-qplan-additions.json` into
QPLAN-01: those exact IDs came from the passing execution above. This closes the
specific missing qualification seed/probability consumer vectors identified in
the initial handoff, subject to final manifest integration and independent review.
The preparation-only `prepare_compute` report is not a qualification seed producer;
its probability helper behavior is covered by the existing calculator vectors.

Branch-protection clarification: the workflow schedules real boundary jobs for all
PRs and makes their status fail closed. Successful final jobs are evidence for PR
readiness without changing settings. Enforcing a merge prohibition additionally
requires a repository administrator's ruleset/branch-protection setting requiring
`Qualification execution boundary (1)` and `Qualification execution boundary (2)`.
No branch-protection setting was inspected or changed in this handoff.

Follow-up repository gate `./fp.ps1 check`: record
`20260918T154855Z-28559e1c4a78`, completed, exit 0, stable source and complete
capture; 72 evidence-store tests with 3 existing skips and unchanged absent
private-source/data/heavy-artifact advisories. `git diff --check` passed.
