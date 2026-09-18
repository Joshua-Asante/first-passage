# PR 415: why review findings keep recurring

Reviewed 2026-09-17 against `bfad2f187e05980369dbf0e8f75801f621ba998d`.
GitHub head was refreshed after investigation and remained unchanged and open.
This assessment recommends continued acceptance hold. It changes no production
code, policy, PR discussion, or deployment state.

The recurring problem is incomplete enforcement of the qualification contract
across its boundaries. Several repairs correctly reject a reported example but
leave another way to violate the same requirement. Other requirements have never
been implemented, even though their names appear in signed evidence. More review
and more example tests help, but cannot by themselves supply the missing ownership,
semantic validation, or execution boundary.

There is substantial useful work here: genuine replay composition, exact decimal
decisions, canonical seed derivation, role-key separation, transactional sealing
against VOID, and stricter authenticated retries. Preserve these. The evidence
does not justify a wholesale replay/kernel rewrite.

## What the review history establishes

The retrieved GitHub history contains 22 top-level inline findings in six review
submissions: 5, 3, 3, 3, 4, and 4 findings. Counts exclude author replies and the
separate local audit. These are review findings, not 22 independently reproduced
defects in this assessment.

| Family | Observed progression | Structural implication |
| --- | --- | --- |
| Runtime identity | Missing sealer role; executable verification only covered adjudication; omitted execution globals; incomplete module closure; injected descriptors; mutable budget issuance state | An expanding list of Python objects to inspect has been asked to support a stronger guarantee than it can provide against a caller controlling that interpreter. |
| Exact decisions | N1 Decimal-to-float issue, followed by N2/Part B and alpha conversion | First repair stopped at the reported stage instead of tracing the signed probability through all consuming decisions. |
| Execution provenance | Unconsumed dispatch could complete; repair required consumption; caller could consume and fabricate completion anyway | Dispatch authorization and dispatch consumption are not evidence of actual execution completion. |
| Durable authority | Historical PASS remained sealable after VOID; later incomplete retry identity; public retry path needed correction; older composition assertion contradicted the new retry contract | Commit, invalidation, retry, restart and sealing need one explicit transition contract across public APIs. |
| Semantic binding | Coherently substituted seeds; authentication object substitution; latest output-role/content and product-basis gaps | Matching hashes or valid signatures do not establish that the values mean what the qualification requires. |
| Missing requirement | LEGALITY is initialized as empty evidence and adjudicated as PASS | A named stage and its digest were implemented without the underlying screen. |

Representative review links:
[runtime closure](https://github.com/Joshua-Asante/first-passage/pull/415#discussion_r4037776912),
[confirmation decimals](https://github.com/Joshua-Asante/first-passage/pull/415#discussion_r4032747870),
[checkpoint completion](https://github.com/Joshua-Asante/first-passage/pull/415#discussion_r4032747871),
[VOID](https://github.com/Joshua-Asante/first-passage/pull/415#discussion_r4038935380),
[retry identity](https://github.com/Joshua-Asante/first-passage/pull/415#discussion_r4041009342).

The initial PR commit `7ba7844` already contains the hard-coded legality PASS,
positive-but-unpinned initial basis, caller-selected output roles, and separate
output/stage digest validation. These latest issues are latent omissions, not
evidence that the most recent repairs introduced them. The history does show
specific repair-generated integration work: changing retry semantics required
updating the public API and its older full-composition assertion.

## Current findings and evidence

| Current issue | Evidence at reviewed head | Assessment |
| --- | --- | --- |
| LEGALITY without a screen | `orchestration.py:192` creates `{}`; `result_adjudication.py:331-336` requires that empty object and assigns PASS. No qualification call to `policy_fingerprint.validate_registry` was found. The existing validator at `ops/c1_rail/policy_fingerprint.py:181` explicitly supports an empty pre-admission registry expectation. | Latest finding is supported by code. A fresh pure-adjudication probe returns PASS with no legality evidence; a full populated-registry-to-seal reproduction was not run. |
| Wrong product basis | `contract.py:818` checks positive/pristine equality; `runner.py:27` supplies that basis as the explicit account override. `core/firm_rules.py:488` defines the 100K tier's starting balance as 100000; `core/mc/preflight.py:151,176,210` documents and applies the override. | Fresh signed OPERATOR-schema probe accepts 50000 and produces different kernel starting-equity/profit-target arguments. Uses generated test keys and declared fixture bindings, not production sources or credentials. |
| Missing production output inventory | `contract.py:854-862` checks sorted uniqueness, nonemptiness and disjointness; G5 reads those same supplied roles at `seal.py:519-521`. | Fresh signed OPERATOR-schema probe accepts only `placeholder` as a required role. |
| Retained output disconnected from adjudicated facts | `seal.py:481-516` verifies journal/runtime/path evidence separately; `seal.py:548-551` checks each output against its own declaration; stage outcome digests are computed separately at `seal.py:697-702`. Both maps are retained at `seal.py:833-834` without a role-specific semantic comparison. | Latest finding is supported by code tracing. No fresh complete OPERATOR seal reproduction was run for this issue. |
| Caller-manufactured execution completion | Existing G5 fixture explicitly constructs PathOutcome values and journal transitions without invoking replay. | Fresh probe still reaches a validated PASS at the actual G5 validator. This is TEST_ONLY evidence through shared validation; it is not a production qualification or a newly demonstrated production-key exploit. |

Latest review:
[legality](https://github.com/Joshua-Asante/first-passage/pull/415#discussion_r4041535942),
[basis](https://github.com/Joshua-Asante/first-passage/pull/415#discussion_r4041535949),
[retained evidence](https://github.com/Joshua-Asante/first-passage/pull/415#discussion_r4041535965),
[required roles](https://github.com/Joshua-Asante/first-passage/pull/415#discussion_r4041535974).

## Why the existing process has not closed the gaps

**Local correctness has been mistaken for completeness of a requirement.** The
N1-to-N2 decimal sequence is the clearest example. A comment names a location;
the requirement applies to every consumer of the frozen probability. Likewise,
adding a consumption bit answers whether a dispatch was consumed, not whether
the designated computation produced the accepted observations. Some later repairs
do address a family: canonical seed rederivation and the locked seal/VOID transition
are good examples of the approach to retain.

**The schema admits choices that the product does not permit.** A signature
authenticates the selected contract. It does not make an arbitrary positive basis
the correct 100K basis, or turn an arbitrary role list into sufficient qualification
evidence. Closed JSON fields prevent unknown keys, but still need semantic relations
to independently owned product policy.

**The threat model and enforcement mechanism have been mismatched.** In-process
tokens, exact classes, private registries and reflection can catch accidental drift
and particular substitutions. They cannot create an independent execution authority
against arbitrary code in that same interpreter. The PR now explicitly recognizes
this limitation; retain that acceptance pause rather than expanding introspection
as if it closes execution provenance.

**The acceptance fixture changes the contract it ought to exercise.** The genuine
replay composition is valuable, but `composition_fixture.py:241` replaces production
output roles with `private-result` and `public-projection`. The serializer in
`composition_result_fixture.py` implements those two files. The isolated G5 fixture
uses the same alternative roles and deliberately manufactures outcomes. Such tests
can verify consistency, signatures and composition while missing production role
requirements, role-to-content binding and absent execution proof. Synthetic data
is appropriate; changing the evidence obligations needs separate conformance tests.

**Integration scope makes omissions expensive to see.** The current diff contains
107 files and 18,491 added lines spanning computation, authority, journaling,
runtime validation, packaging, fixtures and documentation. This size is a risk
multiplier, not proof of a cause by itself. The source history and missing
producer/consumer relationships provide the stronger evidence. More procedural
instructions alone would still leave these relationships implicit.

## Structural changes, in recommended order

1. **Make the qualification policy executable and canonical.** Extend the existing
   policy ownership rather than introduce another independent list. Represent the
   fixed product identity, canonical firm-rule reference, allowed initial state,
   stage prerequisites, exact decision inputs, required output roles and their
   schemas in one versioned qualification policy. Contracts reference that policy;
   G1 validates their resolved values against it. Orchestration and G5 consume its
   projections. TEST_ONLY may use smaller workloads and generated keys with explicit
   authority separation, while preserving the production evidence structure in the
   conformance route. Reject the 50000 basis and placeholder roles before issuing
   an authoritative contract receipt. Do not change the research account-override
   capability in `firm_kwargs`; enforce the narrower qualification requirement at
   its owner.

2. **Give each accepted claim a real producer and evidence relationship.** Add an
   actual legality check over exact retained geometry bytes, using the canonical
   registry validator and the existing pre-admission requirement. Produce a typed
   legality record; missing evidence cannot imply PASS. Serialize retained stage
   artifacts from the observations adjudicated, and derive the output manifest from
   those exact bytes. G5 validates both the schema and the role-to-evidence binding.
   Specify the journal snapshot point explicitly: pre-result-commit snapshot/event
   identity, result commit and seal publication are distinct records. Requiring a
   digest of a database that changes while recording that digest creates another
   inconsistency. Public projections need a defined derivation, not necessarily
   byte equality with private evidence.

3. **Implement the protected execution boundary for execution claims.** The proposed
   N1 service/worker/G5 design is the right direction under its explicit trusted-host
   assumptions: service-owned dispatch and capture, worker without journal/key
   authority, attestation only after finalized output capture, protected G5 and
   separate signing roles. Keep pure replay and statistical mechanics. Test real
   process/UID isolation, interruption, recovery and inability to fabricate a
   completion. Provisioning a Linux test environment alone does not provide this
   capability. The existing design's source-admission record also needs the actual
   legality semantics: successful source construction is insufficient while the
   current factory lacks the registry check. An isolated worker can faithfully run
   an invalid contract, so changes 1 and 2 remain necessary.

4. **Specify durable transitions once and exercise event sequences.** Keep the
   journal as the transition authority. Define guards and durable identities for
   dispatch, completion, authentication, commit, VOID, seal and exact retry. Verify
   these through public interfaces, including process reconstruction, both orders
   of VOID versus seal, lost acknowledgments, changed authentication, and interrupted
   execution. Use model-based/state-machine tests to explore sequences. Historical
   inspection must remain distinguishable from current acceptance authority.

5. **Change the unit of acceptance from a repaired line to a verified invariant.**
   For each requirement retain a compact record of owner, input, producer, consuming
   transition and decisive rejection test. Missing producer or test means open.
   After a finding, enumerate the related stages/entry points and close that family
   before requesting another review. Add one real execution-to-G5 route retaining
   production-shaped artifacts, plus coherent substitutions that update hashes and
   signatures together. Independently specified vectors must still test canonical
   helpers; deriving expected results from the same helper only proves agreement.
   Deliberately disabling legality, basis validation or artifact binding should
   cause this acceptance route to fail. Independent review remains a final check,
   not the mechanism that enumerates the original requirements one at a time.

For implementation, use bounded vertical changes with one named integration owner:
policy/legality; captured artifact semantics; protected N1 execution; lifecycle
conformance. Each needs a real producer-to-consumer acceptance case. Preserve the
N1-only restriction until later stages are implemented and attested. Do not infer
full E1 readiness from a protected N1 failure path.

## Fresh verification and limits

Read-only inspection used the clean checkout
`C:/Users/joshu/multi_firm_operations/.worktrees/pr415-bounded-repairs` at the head
above. Production files and PR comments were not changed. The scratch probe and
this report are outside that checkout. The main workspace's unrelated edits remain.

`./fp.ps1 doctor` passed with all 62 locked packages and cryptography 50.0.1.
Interpreter: Python 3.13.2 at
`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`.

Command, run from the reviewed checkout:

```powershell
.\fp.ps1 python -m pytest C:/Users/joshu/multi_firm_operations/tmp/pr415_structural_review_probes.py -q --tb=short -p no:cacheprovider
```

Result: **4 diagnostic probes passed in 37.63 seconds**, meaning four undesirable
behaviors reproduced. No production code was monkeypatched by these probes.
Record: `.cache/fp-verification/20260917T213010Z-8e6dc8f9f8c3/record.json`.
Confirmed `status=completed`, `verification_exit_code=0`, `source_stable=true`,
`capture_complete=true`, and no report errors. Git emitted permission warnings
for the user-global ignore file. Checkout remained clean.

This assessment did not rerun the full test suite or repository gates, establish
current hosted CI success, exercise private sources, prove the proposed isolation
design, or reproduce every historic review finding. Prior PR-reported broad test
results are historical context, not fresh acceptance evidence here. No finite
review guarantees elimination of all defects; the recommended structure makes
specific required guarantees enforceable and their omissions detectable earlier.
