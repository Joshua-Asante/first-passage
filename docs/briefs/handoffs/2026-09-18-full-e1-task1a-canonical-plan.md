# Codex handoff: full E1 canonical planning contract (Task 1a)

**Selected outcome:** implement a deterministic, strictly validated FULL_E1 planning artifact derived from verified frozen inputs. It describes N1, the single joint N2/Part B batch, and potential Part A panels. It carries no execution, admission, result or seal authority. Return this contract and its tests as one reviewable checkpoint; durable service admission is Task 1b, outside this handoff.

**Prerequisites:** accepted PR425 merge `1e4928360b95812b04725dc1e8da97709d670ff4`. PR415 was closed without merging; PR425 includes the foundation. Read the [successor specification](../../superpowers/specs/2026-09-17-protected-full-e1-campaign.md) and [roadmap](../../superpowers/plans/2026-09-17-protected-full-e1-campaign.md). Their twelve Linux scenarios govern eventual combined acceptance, not this pure-planning checkpoint. Baseline evidence is the successful [two-host boundary run](https://github.com/Joshua-Asante/first-passage/actions/runs/35401263108), [final hosted pytest](https://github.com/Joshua-Asante/first-passage/actions/runs/35401263099), and `docs/notes/audits/2026-09-18-qualification-combined-verification.md`. No broker work is a prerequisite.

**Ownership:** the receiving Codex agent owns Task 1a implementation and verification. The coordinating full-E1 agent reviews the returned changes and retains Task 1 and combined-campaign acceptance. Do not create another Codex task or delegate merely because tools are available.

**Verification:** use this checkout's operations launcher after doctor. Add meaningful positive and rejection tests against signed retained-bundle fixtures, deterministic seed vectors and unchanged N1 behavior; commands and assertions are below. Report exact revision/dirty state, interpreter, commands, actual results, verification record paths and any skips/failures. Pure tests establish plan consistency only; do not claim Linux execution, source replay, resource enforcement or full E1 acceptance.

**Checkpoint:** return once the canonical producer, validating consumer and selected regressions pass and you have reviewed the diff. Also return on a load-bearing conflict requiring changed statistics, an authority-boundary change or an expanded footprint. Record findings and checks in the roadmap's Task 1a progress entry. A discovered issue is not permission to take on the later tasks.

**Return boundary:** deliver local reviewable edits, the evidence summary and remaining Task 1b interface obligations; do not commit, push, open a PR or merge in this handoff. Do not implement or enable SUBMIT_E1, durable campaign admission, dispatch, resource reservations, G5 continuation, results or seals. Do not alter accepted N1 authority or repair historical PR425 failures. Return to the coordinator rather than selecting Task 1b or Task 2.

## Coordinator correction after scope-conflict return

The equal-panel positive case in the original handoff was incorrect and is superseded. At base `1e4928360b95812b04725dc1e8da97709d670ff4`, `QualificationWorkloadPolicy.__post_init__` requires expanded panels strictly greater than initial panels and sorted unique PART_A depths. Preserve that policy. Reuse the verified signed fixture workload to test both direct validator rejections; no equal-count admitted context is required or permitted. Expansion-tolerance equality remains inclusive and is a different condition. The reported scope conflict is resolved within the existing documentation/implementation footprint; Task 1a may resume under this corrected handoff, with its original return boundary and without Task 1b work. The coordinator is not claiming implementation or dispatching an agent through this amendment.

## Workspace and task sizing

Use `C:/Users/joshu/.codex/worktrees/full-e1-spec-baseline/multi_firm_operations`, already isolated at the merge above in detached HEAD. Verify HEAD and status first. The successor specification, roadmap and this handoff are intentional local untracked documents; preserve them. Do not reset, clean, switch the shared main checkout or use the old dirty structural-closure worktree. Reuse existing isolation under the worktree skill.

This is deliberately smaller than roadmap Task 1. At the merged revision, `execution/service.py` handles SUBMIT_N1 by reserving and scheduling work; `ExecutionStore.reserve()` creates a DISPATCHED execution. Extending that flow safely requires durable no-dispatch admission, status/retry/VOID semantics and later budget integration. Do not pull those into a first pure-contract checkpoint. Task 1a is complete when a future admission owner can consume exact, validated plan bytes without trusting caller-supplied declarations. It does not complete Task 1's durable campaign identity outcome.

Use `superpowers:executing-plans` and `superpowers:test-driven-development`, with verification-before-completion for final claims. Consult rule-0 before changing any risk/calibration premise; this handoff authorizes no such change.

## Read first and preserve canonical ownership

Inspect these production files before tests or edits:

- `ops/c1_rail/qualification/checkpoint_plan.py`: current pure N1 plan producer.
- `ops/c1_rail/qualification/seed_identity.py`, `runner.py`, `part_a.py`, `regime.py`: actual RNG addressing, probe separation and panel mechanics.
- `ops/c1_rail/qualification/policy.py`: canonical populations, stage order and checkpoint grouping; PART_B belongs to N2.
- `ops/c1_rail/qualification/execution/plan.py` and `admission.py`: active N1 adapter and verified ExecutionContext producer.
- `ops/c1_rail/qualification/execution/release_schema.py`, `protocol.py`, `service.py`, `store.py`: N1_ONLY boundary that stays closed.

Tests/fixtures to reuse:

- `tests/ops/qualification/execution/bundle_fixture.py::build_bundle` and `test_bundle.py` reconstruct a signed TEST_ONLY context through `verify_bundle`.
- `tests/ops/qualification/test_seed_probability_vectors.py` and `execution/fixtures/seed_consumer_vectors.json` supply independent existing vectors.
- `tests/ops/qualification/test_checkpoint_validation.py` and `execution/fixtures/n1_plan.json` constrain inherited plans.

Allowed implementation footprint:

- Extend `ops/c1_rail/qualification/checkpoint_plan.py` for shared pure campaign production and validation.
- Extend `ops/c1_rail/qualification/execution/plan.py` only for a pure context-to-plan adapter; no service hookup.
- Add `tests/ops/qualification/execution/test_campaign_plan.py`. Add a narrowly scoped helper to `bundle_fixture.py` only if a genuine signed fixture variation is necessary; do not weaken existing validation or fixture provenance.
- Update the roadmap progress/interface notes to match the final implementation. Keep the governing spec unchanged unless documenting a non-semantic clarification.

Do not create `execution/campaign_plan.py` or a second policy owner. A necessary dependency outside this footprint must be identified to the coordinator before expanding it; read-only inspection remains allowed.

## Producer and consumer contract

Implement these proposed pure interfaces; their names align with the roadmap. Do not implement the roadmap's other future APIs in this slice.

```python
# qualification/checkpoint_plan.py

def derive_campaign_plan(contract, *, policy, execution_release_sha256: str,
                         source_bundle_sha256: str, attempt_id: str,
                         exact_depth_approval_sha256: str) -> bytes:
    """Return canonical planning bytes; never reserve, sample or grant authority."""


def validate_campaign_plan(raw: bytes, *, contract, policy,
                           execution_release_sha256: str,
                           source_bundle_sha256: str, attempt_id: str,
                           exact_depth_approval_sha256: str) -> dict:
    """Reject malformed/noncanonical or differently bound declarations."""

# execution/plan.py

def derive_campaign_plan_from_context(context) -> bytes:
    """Compose verified ExecutionContext inputs; no dispatch or persistence."""
```

The adapter receives the actual ExecutionContext from `verify_bundle`: contract, canonical policy, installed release digest, retained bundle digest, attempt ID and exact-depth approval digest. It checks cross-bindings before invoking the pure producer. Type checks alone do not establish execution authority. A pure caller can construct planning bytes; no authority consumer accepts those bytes in this slice.

Use a closed schema named `qualification_campaign_plan/v1` with `purpose='PLANNING_ONLY'`, `target_capability='FULL_E1'`, `authorizes_dispatch=false`, and explicit TEST_ONLY authority. Those fields describe a plan, not a registered execution release. An accepted N1_ONLY signed fixture may be used to test planning: bind its actual release digest unchanged and never pretend that release authorizes FULL_E1. OPERATOR context/authority is rejected by this new planning adapter for this slice. Preserve all existing N1 parsing/behavior.

The document must bind:

1. Attempt, contract, trust domain, canonical policy, execution release, retained source bundle and exact-depth approval digests.
2. Frozen initial-state and replay identities, RNG namespace/mechanics identity, the exact frozen budget and its canonical digest. This is budget configuration binding, not a clock origin, allowance reservation or measurement.
3. Ordered compute checkpoint groups N1, N2 and PART_A, derived from canonical policy. CUTOFF is a deterministic control record with no compute seeds; do not invent a Part B dispatch.
4. Ordered N1 FULL/H1/H2 counts and seeds, preserving the existing N1 plan meaning. Compare its subplan to `derive_n1_plan` rather than maintaining a second implementation.
5. One N2 FULL/H1/H2 seed inventory: FULL depth from N2, H1/H2 depths from PART_B. Map FULL to N2 statistics and half populations to Part B without additional seed addresses for either speed or Part B.
6. Part A frozen parameters and the potential ordered outer/path seed inventory through expanded_panels. Distinguish the initial prefix and possible appended range. Do not generate source-session panels, choose expansion, draw paths, include outcomes or invent panel identities that depend on actual sampling. All Part A data remains a planned inventory, not an executed one.
7. Explicit existing probe addresses per compute checkpoint, separate from qualification paths. Read actual runner/Part A call sites and existing vectors; do not assume that probes are globally unique across checkpoints or rename RNG domains to force uniqueness. If existing addresses repeat, retain their actual semantics and identify them by checkpoint.

Use canonical JSON and existing validators, integer rules and seed producer. Reject invalid bindings, bool-as-depth, unsupported population order/counts, noncanonical/unknown fields and missing/extra/reordered seed entries. Validation must derive the expected plan independently from the frozen inputs, then require exact canonical equality; accepting a caller's self-consistent edited digest is insufficient. Signature/current-validity checking belongs to the verified-context producer and later admission service, not to a new planning authority.

Any eager materialization must remain bounded by the supported frozen input/profile sizes. Do not allocate an unbounded caller-selected seed list. If supported real depths cannot fit the planned representation/limits, return measured evidence of the conflict instead of introducing an unreviewed compact schema or relaxing limits. Do not change frozen statistical constants.

## Test cycle and concrete assertions

Start from a signed fixture and actual validation, not a SimpleNamespace pretending to be an admitted contract. This producer test should fail first because the adapter is absent:

```python
from bundle_fixture import build_bundle
from test_contract import NOW
from c1_rail.qualification.execution.admission import verify_bundle
from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context
from c1_rail.qualification.contract import parse_canonical_json


def test_verified_context_yields_stable_non_authoritative_campaign_plan(tmp_path):
    case = build_bundle(tmp_path / 'bundle')
    context = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    first = derive_campaign_plan_from_context(context)
    assert first == derive_campaign_plan_from_context(context)
    doc = parse_canonical_json(first, label='campaign plan')
    assert doc['schema'] == 'qualification_campaign_plan/v1'
    assert doc['purpose'] == 'PLANNING_ONLY'
    assert doc['target_capability'] == 'FULL_E1'
    assert doc['authorizes_dispatch'] is False
    assert doc['attempt_id'] == context.attempt_id
    assert doc['execution_release_sha256'] == context.release.sha256
```

Add tests for each distinct invariant:

- A freshly reconstructed context from the same retained bytes yields identical plan bytes. Different valid attempt/bundle/release/approval identity cannot validate against the first context.
- Changing just the caller's plan seeds, population counts, ordering, budget, declared digest or probe inventory fails validation against frozen inputs; include coherently rehashed edits.
- N1 subplan equals the established producer. N2 has exactly one FULL/H1/H2 batch; no PART_B checkpoint, extra FULL speed trials or separate Part B seeds.
- Initial Part A seed-address prefix is unchanged in the potential expanded inventory; test first/last initial and appended addresses for admitted workloads with expanded_panels > initial_panels, and probe/path domain distinctions with independently established expected vectors. Equal panel limits are an unsupported frozen configuration and must reject at canonical workload validation; they are not a positive plan-generation case. Retain separate rejection of duplicate PART_A/REGIME depths. Do not bypass validation or modify trust_domain.py to produce an equal-count context.
- Noncanonical bytes, unknown fields, wrong type, malformed digest and cross-domain inputs reject. For invalid frozen configurations, use appropriately signed fixtures or directly test validators; do not mutate a validated immutable object and call that admission evidence.
- New planning adapter rejects OPERATOR authority. Existing release parser still rejects FULL_E1 executable capability, request parser still rejects SUBMIT_E1, and legacy authority rejection remains unchanged.
- Plan construction invokes no source replay, sampling, worker launcher, store mutation or signing. Instrument prohibited calls to fail if invoked; also inspect the production diff/imports. These are library side-effect tests, not Linux isolation evidence.

Run from this checkout, using its launcher:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python -m pytest tests/ops/qualification/execution/test_campaign_plan.py -q --tb=short
.\fp.ps1 python -m pytest tests/ops/qualification/execution/test_bundle.py tests/ops/qualification/execution/test_release.py tests/ops/qualification/execution/test_protocol.py tests/ops/qualification/test_checkpoint_validation.py tests/ops/qualification/test_seed_probability_vectors.py tests/ops/qualification/test_semantic_policy.py -q --tb=short
.\fp.ps1 check
```

Use test-driven development: observe the relevant failure, implement the minimum producer/consumer contract, then pass the new tests and regressions. If a related consumer is affected, add its relevant tests. Inspect recorder status, verification_exit_code, source_stable and capture completeness; a file existing is not a pass. Disclose existing gate advisories/failures. This slice has no reason to provision a Linux host, launch a campaign, modify CI/manifest inventories or rerun the full two-host suite.

## Delivery to coordinator

Return the exact workspace/base, changed-file summary, final public function signatures/schema, passed/failed checks with recorder paths, a concise review of canonical ownership and authority closure, and any remaining representation/binding concerns. Record Task 1a as implemented/verified only when supported; leave Task 1 and full E1 incomplete.

Task 1b remains: versioned FULL_E1 release admission, closed SUBMIT_E1 protocol, service-owned durable identity/receipt, duplicate/conflict handling, status and invalidation without worker launch. Budget lifecycle, dispatch and restart are subsequent handoffs. Task 1a's plan bytes are not migration or dispatch authority for any existing N1_ONLY attempt.
