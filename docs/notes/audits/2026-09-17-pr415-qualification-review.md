# PR 415 qualification review — 5e935c8

Reviewed 2026-09-17. PR head was refreshed after investigation and remained
`5e935c89e0c004ae76717765f91889e9b8257b7a`, open. Recommendation: hold acceptance.
This is a review, not an implementation change or production qualification.

The three latest GitHub findings are valid. Two further gaps remain in the
checkpoint-to-result contract. The key-role finding also has a public-key alias
variant that an ID-only fix would miss.

## Findings

### P1 — Consuming a dispatch does not prove execution completed

`ops/c1_rail/qualification/attempt.py:781–813,834–835`

The previous repair requires a durable consumed bit before checkpoint completion.
But the caller holding a newly issued dispatch can call
`consume_checkpoint_dispatch()` directly, then `complete_checkpoint()` with
fabricated outcomes. No executor completion receipt binds the actual output of
`ProductionExecutor` to this transition. Consumption happens before computation
even on the normal executor route.

The existing G5 fixture constructs PASS outcomes, starts/consumes/completes the
journal checkpoints itself, and receives a validated PASS without running any
replay. The review probe reproduces this acceptance without changing production
functions or the runtime verifier. This is stronger than simply omitting the
consumption call: it demonstrates why the previous repair does not establish
execution provenance.

The reproduction uses signed TEST_ONLY fixtures, not private OPERATOR sources.
The relevant journal and G5 checks are shared; they do not require a different
execution-completion proof for OPERATOR evidence. The production entry point's
concrete-executor check does not protect callers entering through the journal
and G5 interfaces directly.

Required outcome: the accepted result must bind to the designated execution's
actual completion and outputs. A mutable bit or another caller-accessible
same-process constructor is not independent proof against that caller.

### P1 — Seed evidence is internally consistent but need not match F1

`ops/c1_rail/qualification/seal.py:244–280`

`_validate_checkpoint_plan_inputs()` checks field shapes and matches hashes of
the supplied seed records against the supplied path inventory. It does not
rederive the seed from the frozen namespace/stage/population/indices, compare
the namespace to the contract, or recompute the source-population digest.

A complete G5 validation accepted records with namespace
`not-the-frozen-namespace`, stage `n3` in E1, every seed incremented from its
fixture value, and an all-zero source-population digest. Updating the dependent
hashes consistently is enough. This permits evidence for different streams or
source pools to claim the designated frozen run.

Required outcome: independently derive each expected seed record from the frozen
contract and checkpoint address, and validate the complete ordered inventory,
including Part A outer seeds and panel/source bindings. Hash agreement alone
does not establish that the underlying inputs are the authorized ones.

### P1 — A committed PASS can still seal after VOID

`ops/c1_rail/qualification/seal.py:125–146,1000–1005`

Confirmed latest GitHub finding. The binding helper reads journal status but
does not require current validity for sealing. `result('TB_E1')` continues to
return the historical committed PASS after `void()`. The complete authentication,
commit and seal test still succeeds when VOID is inserted immediately before
the final seal call.

Required outcome: enforce current validity at the authoritative seal transition,
with a defined atomic ordering relative to concurrent invalidation. Merely
adding an early status read leaves a check/use race.

### P1 — Class namespace verification misses data descriptors

`ops/c1_rail/qualification/result_adjudication.py:101–116`

Confirmed latest GitHub finding. The comparator selects functions, static/class
methods and properties, omitting arbitrary descriptors and class data. Injected
descriptors for `PathOutcome.status`, `sessions_to_pass`, `failure_reason` and
`diagnostics` survive the complete model-module verifier. An existing FAILURE
object then reads as PASS while its instance dictionary still contains FAILURE.

The local probe establishes the verifier bypass and changed outcome reads; it
does not separately rerun a complete forged seal for this variant.

Required outcome: cover the relevant class namespace and layout, not only
method-like objects. More generally, checking live Python objects after a run
does not prove those objects were unchanged while that run executed.

### P1 — Signing roles can share the same cryptographic identity

`ops/c1_rail/qualification/trust_domain.py:288–304`

Confirmed latest GitHub finding and an additional variant. The production
validator accepts the same ID in result and seal inventories. It also accepts
disjoint IDs `producer` and `sealer` backed by the identical Ed25519 public key.
The latter means making the ID sets disjoint would still let one private key
perform both jobs.

Both probes run against the actual compiled OPERATOR policy, using generated
test keys. No production key material is used.

Required outcome: enforce separation of result/seal public-key fingerprints as
well as IDs, and preserve that restriction at the consuming boundaries.

## Assessment of the directory as a whole

The package separates useful mechanics: source coverage and calendars; whole
block/path construction; continuous replay; fixed-depth statistical decisions;
and the attempt journal. Current repairs include exact N1/N2 decision
probabilities, broader runtime module closure, stricter cost parsing, and budget
checks after stage computation. These were inspected; this review does not
claim to rerun all their regression suites or establish private-source parity.

The recurring defects concentrate in the authority layer connecting those
mechanics. The code repeatedly treats three different claims as interchangeable:

1. Bytes and declarations agree.
2. The intended execution produced the observations.
3. An independent authority accepted those observations while the attempt was valid.

Hashes primarily support the first claim. A caller-consumed dispatch does not
establish the second. Overlapping keys and stale journal validity undermine the
third. Additional Python reflection checks cannot by themselves create an
independent trust boundary against arbitrary code in the same interpreter.

The intended threat model should be explicit. If the producer process is trusted,
describe runtime introspection as drift detection and do not claim it prevents
that producer from fabricating execution. If it is not trusted, execution and
sealing need independently controlled boundaries, with the executable/runtime
identity and actual outputs bound there. Keeping this distinction explicit would
prevent another sequence of local fixes that leaves the composed guarantee open.

The tests explain why passing CI is insufficient here: several seal tests
deliberately manufacture outcomes and journal receipts to exercise G5 in
isolation. They are useful validation tests, but passing them is not evidence of
execution provenance. Add negative acceptance tests for an internally consistent
fabrication and for consistently substituted seed plans, alongside the positive
real-executor composition. Reuse one canonical seed/plan derivation rather than
maintaining a weaker parallel schema check in the sealer.

## Verification evidence

Checkout: `C:/Users/joshu/multi_firm_operations/.worktrees/phase3-post413-integration`.
Working tree remained clean at the reviewed commit. No implementation files or
PR comments were changed. Review probes are outside that checkout at
`C:/Users/joshu/multi_firm_operations/tmp/pr415_review_probes.py`.

`./fp.ps1 doctor` passed: Python 3.13.2 at
`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, all 62
locked packages matched, signing dependency cryptography 50.0.1.

First command:

```powershell
.\fp.ps1 python -m pytest C:/Users/joshu/multi_firm_operations/tmp/pr415_review_probes.py -q --tb=short
```

Result: 5 passed, 1 failed in 99.67 seconds. The failed seed probe accidentally
created duplicate seed identities and correctly hit that rejection. This was a
probe construction error, not a production fix. Git ignore and pytest-cache
permission warnings were emitted. Verification record
`20260917T161018Z-0978bfa29e9a` reports stable source and exit 1.

After correcting the probe to preserve unique identities, only that case reran:

```powershell
.\fp.ps1 python -m pytest C:/Users/joshu/multi_firm_operations/tmp/pr415_review_probes.py -q --tb=short -k consistently_wrong_seed_contract -p no:cacheprovider
```

Result: 1 passed, 5 deselected in 29.30 seconds. Verification record
`20260917T161311Z-11befa67414b` reports stable source and exit 0.

Thus six distinct probes reproduced the undesirable acceptance behaviors across
the two runs. A passing probe means the defect reproduced, not that the product
passed an acceptance gate. The full repository test/gate suites were not rerun.
No actual-source qualification, signing with production keys, deployment, or
live arming was performed.
