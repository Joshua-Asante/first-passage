# K3/RC-4: service salt and client plan view (dispatch card, DRAFT)

**Type:** cc_handoff (worker dispatch card for the qualification slice "K3/RC-4 — service salt and client plan view")

**Status:** DRAFT, 2026-10-02. **Not frozen and not dispatched.**
- Prepared by a cloud worker under the deployment coordinator's Ticket I, so that implementation can start once the H9 lane releases the store-file lock after R1.
- Freezing it is the coordinator's act, after the §3.1 pre-freeze decisions. Committing this draft dispatches nothing ([handoffs README](README.md)).

**Owner record.** The execution-slices ledger ([`docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md)):
- the RC-4 entry (`:895-907`) defines the slice scope and the F1 admission check;
- CP-1a decision (5) (`:979`) is the operator's acceptance of the slice;
- the C3 ruling (3) (`:1914`) adds S5 Q9 to the slice.

Umbrella row O-10 routes K3 here, and TB-F1 no longer owns it (`docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md:115`).

**Seats.**
- **Executor:** a worker in a detached worktree cut from the freeze commit, with no `.env`. The lane is chosen at dispatch; §0.5 rules out the GLM lane.
- **Coordinator:** owns review, integration, every push and Linux dispatch, Codex, and the ledger.

**What this card is.** It is the frozen-to-be instruction set for one slice. The slice:
- builds the salted recipe `tb-s2-rng-v3`, with a service-generated salt, its commitment and its reveal;
- serves the client a digests-only plan view, bound into the admission receipt;
- refuses a v3 admission on a release without that view;
- lands the S5 draft §1.6 tests, including the negative client cases already written test-first in [`tests/ops/qualification/execution/test_k3_rc4_client_view.py`](../../../tests/ops/qualification/execution/test_k3_rc4_client_view.py);
- encodes the operator's Q9 decision ([Q9 note](../../notes/2026-10-02-s5-q9-in-doubt-closure-and-salt-reveal.md)).

It lands before S8/T06 dispatch, and before F1 in every case (CP-6, checklist `:492`).

```yaml authority
seat: worker
parent: docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write]
constraints:
  - no_main_write
  - no_merge
  - no_push
  - no_linux_or_ci_dispatch
  - card_section2_files_only
  - no_crypto_choice_beyond_owner_text_and_section3_decisions
  - no_budget_or_limit_change
  - v2_seed_bytes_unchanged
  - stop_at_coordinator_return
acceptance:
  - tests/ops/qualification/execution/test_k3_rc4_client_view.py
  - tests/ops/qualification/execution/test_campaign_admission.py
  - tests/ops/qualification/execution/test_campaign_cancellation.py
  - tests/ops/qualification/execution/test_campaign_plan.py
  - tests/ops/qualification/execution/test_campaign_n1.py
  - tests/ops/qualification/execution/test_campaign_n2.py
  - tests/ops/qualification/execution/test_campaign_part_a.py
  - tests/ops/qualification/execution/test_campaign_recovery.py
  - tests/test_qualification_invariant_manifest.py
  - tests/test_qualification_boundary_verification.py
```

The slice's other new unit files (§4, items W-2 to W-4) and its Linux node file (§4, item L-1) join this list when the coordinator freezes the card.

## 0. Phase 0: premise check, then Rule 0 reads, before any edit

1. **Premise.**
   - The worktree HEAD is the freeze commit, and it descends from a `main` that includes H9 R1's merge.
   - The H9 lane has released the single-writer lock on `campaign_store.py` and the service and store files under `ops/c1_rail/qualification/execution/`.
   - The coordinator has recorded the order against the D3 slice (H9 R2).
   - `test ! -e .env`.
2. **Re-anchor.** Every line number below is at `main@bd30646`, so re-read each one at the freeze commit. A citation that no longer holds is a §7 stop, not a guess.
3. **Rule 0 reads.** Read these yourself; do not infer them.
   - `regime.py:10-24` (`domain_seed`, the `tb-s2-rng-v2` payload) and `seed_identity.py:29-41` (`seed_input`, the `seed` field).
   - `checkpoint_plan.py:70` and `:280-392`: `mechanics_version` and where the campaign plan embeds the seed records.
   - `contract.py:147-156` (`ReplayConfiguration`) and `:660-663`, the closed `replay` field set.
   - `execution/compute.py:26,119`, `runner.py:95` and `part_a.py:141`: the worker derives its seeds from the root in its read-only input.
   - `execution/worker.py:48-69` and `execution/plan.py:16`.
   - `evidence.py:414,1004,1192,1384,2512` (G5 re-derivation and the `tb-s2-rng-v2` checks) and `execution/g5.py:695-698` (G5 reads the plan as a checkpoint member).
   - `execution/campaign_supervisor.py:1459-1517`, the admission body: binding at `:1471`, plan derived at `:1500`, then `finish_diagnostic_admission`.
   - `execution/campaign_store.py`:
     - `bind_budget` (`:2906-2957`, deadline at `:2941-2943`);
     - `finish_diagnostic_admission` (`:2358`, receipt at `:2504-2520`);
     - `diagnostic_status` (`:2280-2357`);
     - `chunk` (`:2565-2590`);
     - the dormant `admit` (`:1264`, receipt at `:1304-1305`).
   - `execution/service.py:368-430` (dormant route) and `:462-530` (diagnostic route, SUBMIT before `begin_admission`).
   - `execution/campaign_protocol.py:88-94` (roles) and `execution/client.py:55-94` (`fetch_campaign_plan`).
   - `execution/release_schema.py`, the closed release documents.
4. **T05 receipt binding (UNVERIFIED in the host-obligations note §B.2/§D.4).** Trace whether the integrated result and seal chain binds the **admission** receipt's bytes or schema. If it does, the receipt change in §3 is an interface change to the accepted R1 identity: stop under §7.

## 0.5. Routing

This is security-relevant custody code: salt generation, commitment, a keyed digest and reveal timing, in the protected qualification path. So the GLM ticket lane is not used, by the standing dispatch rule for security work. No secrets, `.env`, Pine or account data are involved. The executor runs no Linux or CI dispatch; the coordinator holds `ci.dispatch` and dispatches the §4 Linux run.

## 1. Selected outcome

For a `tb-s2-rng-v3` campaign:
- the service generates the attempt salt in the transaction that first binds the F1 contract's budget;
- the client receives only the commitment and a digests-only plan view, bound in the admission receipt, until the campaign is irrevocably closed;
- G5 and the worker derive seeds through their authorized private access;
- a release without the digests-only view refuses a v3 admission before anything durable.

`tb-s2-rng-v2` campaigns keep byte-identical seeds, plans and behavior.

## 2. Scope

The edit set is expected and is re-confirmed in Phase 0. `[C]` marks a module in the 68-module Stage 1c measured closure (`docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/`); see §3.1 item D-4.

| File | Purpose |
|---|---|
| `ops/c1_rail/qualification/regime.py` [C] | The v3 seed recipe with the salt input (the construction is §3.1 item c1) |
| `ops/c1_rail/qualification/seed_identity.py` [C] | The v3 seed record |
| `ops/c1_rail/qualification/contract.py` [C] | The frozen contract names its recipe (§3.2) |
| `ops/c1_rail/qualification/checkpoint_plan.py` [C] | `mechanics_version` v3, plan derivation from the bound salt, client-view construction |
| `ops/c1_rail/qualification/evidence.py` [C] | G5 re-derivation accepts v3 and checks the salt against the commitment before each use |
| `ops/c1_rail/qualification/runner.py`, `part_a.py` [C]; `execution/compute.py`, `execution/worker.py`, `execution/plan.py` [C] | The worker receives the salt in its read-only input, where it receives the root today |
| `ops/c1_rail/qualification/execution/release_schema.py` [C] | The release's client plan-view mode |
| `ops/c1_rail/qualification/execution/campaign_protocol.py` [C] | Only if the §3.1 item D-2 route needs a member or an operation |
| `ops/c1_rail/qualification/execution/campaign_store.py` | Salt generation in `bind_budget`, the receipt fields, the client-view object, the client chunk route, the reveal projection |
| `ops/c1_rail/qualification/execution/campaign_supervisor.py` | Admission body: plan derived after the binding, from the salt; the worker input; the G5 salt route |
| `ops/c1_rail/qualification/execution/service.py` | Condition-1 refusal at SUBMIT, before `begin_admission` |
| `ops/c1_rail/qualification/execution/client.py` | Fetch and verify the client view |
| `ops/c1_rail/qualification/execution/g5.py` | G5 reads the salt through its private route and checks the commitment |
| `tests/ops/qualification/execution/test_k3_rc4_client_view.py` | Remove every `xfail` marker. Re-point only the two seam functions (§3.2). The detectors may move into a shared helper module unchanged, for reuse by item L-1 |
| `tests/ops/qualification/execution/bundle_fixture.py` | `rng_recipe=` and `client_plan_view_mode=` (§3.2) |
| New unit files under `tests/ops/qualification/execution/` | §4, items W-2 to W-4 |
| New Linux node file under `tests/integration/qualification_boundary/`, plus `fixture_producer.py` | §4, item L-1 |
| `tests/ops/qualification/invariant_manifest.json`; `scripts/qualification_boundary_verification.py` | Register item L-1 and add it to the selection (§4) |

## 3. Design

**Owner text it implements (applied; cite, do not restate):**
- full-E1 spec §2.2a (`docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:84`): the client view, its digest, and `client_view_sha256`/`client_view_byte_length`;
- §2.4 (`:113`): `tb-s2-rng-v3`, custody, admission crash and private access;
- §2.6 (`:157`): no reveal while a re-execution remains possible;
- boundary spec §3.1 (`docs/superpowers/specs/2026-09-17-qualification-execution-boundary-design.md:102`): B-3 and OF-7;
- the F1 admission check (ledger `:897-903`). The slice implements condition 1 and the receipt half of condition 3. Conditions 2 and 4 are F1-packet items checked at CP-6 and CP-8 (host-obligations note §B.4, "Where it lands").

Cryptographic material **fixed by the owners**:
- a CSPRNG salt of 32 bytes (256 bits), with one canonical form of 64 lowercase hex, refused otherwise at generation and at reveal (delta K3 row, `docs/notes/audits/2026-09-25-qualification-assurance-contract-delta.md:238-250`; S5 draft §1.4 `:120`);
- the commitment `sha256(salt)`, published in the admission receipt (`:120`);
- the seed digest, "HMAC-SHA256 keyed by the attempt salt over the seed record's canonical bytes" (spec §2.2a).

### 3.1 Pre-freeze decisions (open; the card is not frozen until each is recorded)

| # | Decision | Owner | Note |
|---|---|---|---|
| Q9 | Closing a never-retried, retry-eligible IN_DOUBT, and the salt-reveal timing | Operator | [Q9 note](../../notes/2026-10-02-s5-q9-in-doubt-closure-and-salt-reveal.md). It recommends **A**: automatic closure once no re-execution can fit (`BUDGET_EXHAUSTED`), with the reveal projected from the commit that irrevocably closes the campaign. Before D3 lands, the predicate reduces to "terminal, settled, no recovery barrier pending" |
| D-2 | G5's private salt route (S5 draft Q8, `:408`) | Coordinator, then operator | (i) A new checkpoint member served to the `g5` role over the existing authenticated member route; G5 already reads the canonical plan this way (`g5.py:698`). (ii) A `qg5`-private staged object. (i) keeps custody in `qexec`'s store under the `0700` data tree. (ii) adds a filesystem object to the OF-7 read. The draft leans to (i) but decides nothing |
| c1 | How the salt enters the v3 seed payload. The owner text says only "`tb-s2-rng-v2` with the service-generated attempt salt added" | Coordinator routes to the owner text (operator-accepted) | **Not chosen here** |
| c2 | The commitment's preimage bytes: the 32 raw bytes or the 64-hex text | Same | Not chosen. The test detectors accept either; if another encoding is chosen, extend `_salt_leaks` and its self-test first |
| c3 | The HMAC inputs: which v3 seed record is "the seed record's canonical bytes" (its schema, and whether it carries the salt or the commitment), and the key's encoding | Same | Not chosen |
| c4 | The seed digest's output encoding in the client view | Same | Not chosen. The tests do not depend on it |
| D-4 | Re-measurement trigger 1, "a change to the worker runtime closure or the lock" (r2 §9, `docs/notes/2026-09-27-s5-part-a-measurement-proposal-r2.md:395-401`). Every `[C]` file changes, so trigger 1 fires for the slice's release. The trigger list says such a change "invalidates the application for the next release or profile" (r1, `docs/notes/2026-09-26-s5-part-a-measurement-proposal.md:385`) | Operator | Either re-measure PART_A on the slice head, or rule that a v2-byte-identical change does not fire trigger 1. Decide before any measured TEST_ONLY PART_A run or S8 relies on the slice's release |
| D-5 | Order against the D3 slice (H9 R2). Both edit `campaign_store.py`, so the two are strictly sequential (ledger `:895`) | Coordinator | Under Q9 option A either order works: K3 implements the reveal predicate, and D3 adds the eligibility term |
| D-6 | The §3.2 names | Coordinator | Proposed below |

### 3.2 Proposed interface names (not cryptographic; the coordinator freezes or replaces them)

- **Contract.** The frozen contract names its recipe explicitly: `replay.rng_recipe` in {`tb-s2-rng-v2`, `tb-s2-rng-v3`}, under a new contract schema version. Existing v2 contracts parse unchanged.
- **Release.** `client_plan_view_mode`, the name the OF-7 attestation already uses (host-obligations note §A.2), with value `client_view_digests_only` (owner text). A v3 SUBMIT on a release without it is refused before `begin_admission`, so no admission work, binding or salt exists, and the attempt ID stays admissible.
- **Admission receipt.** A new schema version carrying:
  - `salt_sha256` (the commitment);
  - `client_view_sha256` and `client_view_byte_length` (owner text);
  - `plan_sha256` and `plan_byte_length`, which stay the canonical plan's.
- **Client plan route.** For the `client` role before closure, `FETCH_PLAN_CHUNK` serves only `object_sha256 = client_view_sha256`, and a request for `plan_sha256` is refused. `client.fetch_campaign_plan` fetches and verifies the client view whenever the receipt carries `client_view_*`, and is unchanged otherwise.
- **Canonical plan.** It keeps today's shape: integer `seed` fields in its seed records, and `mechanics_version` naming the recipe (`tb-s2-rng-v3`). The test-first file reads both through `qexec`'s store, and it fails loudly, not vacuously, if either is missing.
- **Reveal.** The client's STATUS carries `salt` (64 lowercase hex) from the commit that irrevocably closes the campaign, and never before. The receipt is immutable and keeps only the commitment.
- **Test seam.** `bundle_fixture.build_bundle` gains `rng_recipe=` (default `tb-s2-rng-v2`) and `client_plan_view_mode=` (default absent; `None` means absent). Seam 1 (`_v3_service`) and seam 2 (`_admit`, a simulated admission tail that derives the plan **after** the salt binding) are the only functions in the test-first file that may change.

## 4. Verification (falsifier-first)

**H:** For a v3 campaign:
- no salt or seed value reaches the `client` role through STATUS, `FETCH_PLAN_CHUNK` or the receipt before closure;
- the receipt binds the client view;
- a release without the digests-only view refuses admission and consumes nothing;
- G5 and the worker reproduce the v3 seeds from authorized access;
- v2 is byte-identical.

**Reject if** any item below fails on the slice head, or any existing qualification test changes outcome.

**Revert trigger:** any v2 seed, plan or receipt byte differs from the base.

Every new test is shown to fail on the base, with a launcher record, before it passes on the slice.

**Windows (launcher records; zero skips, zero xfails):**
- **W-1, the test-first file.** Remove every marker and change no assertion (`grep -rn "awaits K3/RC-4" tests` is empty), then all 8 tests pass. The test-first file covers:
  - the receipt binding (F1 condition 3);
  - no-leak tests on `receipt`, `status` and `plan_chunks` (§1.6);
  - client-view-only serving, with the canonical plan refused;
  - client-side verification;
  - the condition-1 refusal, which also shows that no attempt is consumed;
  - the detector self-test.

  On the base, 6 cases fail at the fixture seam (`build_bundle() got an unexpected keyword argument 'rng_recipe'`), and the client-side case fails its first assertion (the client gets the canonical plan).
- **W-2, the §1.6 salt tests** (S5 draft `:151-157`):
  - a v3 contract with no bound salt cannot derive seeds;
  - the salt must hash to the commitment at G5 use and at reveal;
  - a non-canonical salt is refused at generation and at reveal;
  - G5 adjudicates N1 and N2 before reveal through its private route (D-2);
  - the campaign reveals once it is closed, under the Q9 ruling.

  "A retry-eligible IN_DOUBT does not reveal" lands with whichever of K3 and D3 lands second.
- **W-3, the crash-safe admission tests** (`:158-162`):
  - no plan derivation, dispatch or G5 fetch before the salt-binding commit;
  - a crash before that commit leaves no salt, and the same identity retries;
  - a crash after the commit and before the ADMISSION capture gives the same commitment and attempt, closed IN_DOUBT; admission does not continue, and the salt is revealed once recovery completes;
  - a repeated binding returns the stored salt.
- **W-4, the abandonment tests** (`:163-165`): a second admission under the same authorization is refused, and a VOID after salt generation leaves a visible, counted closed record.
- **W-5, v2 invariance.** The `acceptance` files above pass unchanged, including the seed-vector test in `test_campaign_plan.py:94` (`fixtures/seed_consumer_vectors.json`).
- **W-6.** The delta's §10 K3 hook prints a salt or commitment field (`grep -n "root_rng_namespace\|salt\|commitment" ops/c1_rail/qualification/regime.py ops/c1_rail/qualification/seed_identity.py`). The per-row loop still prints no `UNROUTED: K3`.
- **Final frozen tree:** Windows lines and `check`, and `git diff --check`.

**Linux (the slice's own S2 run, dispatched by the coordinator under the [`s2-linux-run`](../../../.claude/skills/s2-linux-run/SKILL.md) skill):**
- **L-1, a new node file.**
  - A v3 TEST_ONLY campaign is admitted through the real service.
  - The real `qclient` UID makes these requests:
    - STATUS;
    - an identical SUBMIT re-submission (the receipt);
    - every client-view chunk;
    - `FETCH_PLAN_CHUNK` on `plan_sha256`, which must be refused.
  - It asserts that no seed value and no salt is visible, using the same detectors.
  - The nodes are registered in `tests/ops/qualification/invariant_manifest.json`; this card proposes **`QISOL-01`**, "real distinct client/worker identities denied …".
  - This is the evidence F1 condition 2 later requires on the production release's own bytes.
- **The run.**
  - It is one full selection on the slice head: the selection current on `main` at dispatch (`s5`, or the R1 combined set, `docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md:561`), with item L-1 added.
  - Read it with `python scripts/s2_run_evidence.py <id> --expect-head <sha> --expect-scope <that selection's scope>`.
  - The required nodes include item L-1's, and skipped must be 0. A pytest xfail is reported as skipped in JUnit, which is one more reason W-1 removes every marker.

**Then, by the coordinator:**
- a Codex review at the head;
- the Stage 1c closure re-run, which will report the `[C]` modules changed and is routed under D-4;
- the ledger entry.

## 5. Forbidden

- Any cryptographic construction, encoding or parameter beyond the owner text in §3 and the recorded §3.1 decisions (c1–c4). If one is needed and is not recorded, stop.
- Any change to v2 seed derivation, plan bytes or receipts. Any change to an accepted formula, tolerance, budget, profile ceiling, limit, `size=` or memory value.
- D3 re-execution (H9 R2), G5 adjudication semantics beyond the salt route, and any production-authority literal or production planning (`_campaign_inputs` stays TEST_ONLY).
- `core/`, `lab/`, Stage 1c harness files, ledger and owner-text edits. Pushing, PRs, merges and any workflow dispatch.

## 6. Output and return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. The coordinator rules RESOLVED (every §4 item holds) or FALSIFIED (a named item fails). The return contains:
- `git diff --stat` and the full diff;
- each new test's fail-on-base and pass-on-slice launcher records;
- the Phase-0 T05 finding;
- the list of `[C]` files touched, for D-4;
- the concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- A Phase-0 premise fails, or a cited line no longer holds at the freeze commit.
- T05 binds the admission receipt (§0.4).
- A needed choice is not recorded in §3.1 (Q9, D-2, c1–c4).
- A W-1 assertion would have to change, or a new test cannot be made to fail on the base.
- A v2 byte changes, or a file outside §2 would need to change.
- Two failed corrections of the same issue (AGENTS.md).

## 8. Decision unlocked

With W-1 to W-6 green, a green Linux run read ok, Codex RESOLVED and D-4 ruled, the coordinator can propose:
- the slice's acceptance;
- the ledger record that "the RC-4 change landed, K3 built" (the Before-F1 row, ledger `:853`);
- the checklist sequencing note for S8/T06.

F1 itself still needs conditions 2 and 4 at CP-6 and CP-8, including the OF-7 attestation at G-F1.

## 9. Dispatch record

- Base: to be recorded at freeze (a `main` that includes H9 R1).
- Freeze commit: the commit that turns this DRAFT into a frozen card. The coordinator records it in the ledger.

## 10. Audit hooks (runnable)

```bash
# Card form and authority.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-02-k3-rc4-service-salt-client-view-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-k3-rc4-service-salt-client-view-DRAFT.md
# Test-first file: collects clean; 1 passed, 7 xfailed before the slice; 8 passed, 0 xfailed after it.
python -I scripts/fp.py python -m pytest tests/ops/qualification/execution/test_k3_rc4_client_view.py -q -rxX
grep -rn "awaits K3/RC-4" tests   # before: the marker definition; after: empty
# Premise, in the executor worktree.
test ! -e .env && echo "no .env" || echo "FAIL: .env present"
grep -n "tb-s2-rng-v2" ops/c1_rail/qualification/regime.py ops/c1_rail/qualification/checkpoint_plan.py ops/c1_rail/qualification/evidence.py
```
