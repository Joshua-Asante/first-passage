# Execution, tooling gaps and adjudication inventory


> Current engineering status: see the 2026-09-16 post-413 update at the end of this document; the original dated material below is historical.

**Preparation only.** No outcome-bearing command below is executed. The initial
`c86a0a0` tooling-gap inventory is superseded by the coordinator-authorized
implementation on `codex/phase3-qualification-tooling`. G1–G5, continuous replay,
block construction, Part A, the concrete source factory and stage orchestration
now have implementations. Final combined acceptance is pending: G5 security
repairs, a segregated synthetic full-route test, runtime closure review and actual
source/settings/calendar evidence remain required. See
[production-readiness.md](production-readiness.md) for scope and evidence limits.
Implementation presence does not authorize F1, exact-depth ratification or E1.

## Real command inventory

Working directory for preparation commands:
`C:\Users\joshu\multi_firm_operations\.worktrees\phase3-f1-preparation`.
Interpreter used is recorded in [compute-depth.md](compute-depth.md), not presumed
to be the final qualification runtime. All paths below must be reverified after
integration; no command can promote this Markdown candidate to a frozen manifest.

| Operation | Verified interface / command | Input, output and precondition |
|---|---|---|
| Read base/changes | `git rev-parse HEAD`; `git status --short`; `git diff --check`; `git ls-remote origin refs/heads/main` | Read-only; preserve primary and other worktrees; compare selected head and current remote |
| Design sizing | `python scripts/certification_power.py --true-rate 0.03 --true-pass-rate 0.65 --power 0.80 --dependence frechet --ceiling 0.05 --alpha 0.05 --pass-target 0.5 --step 10 --n-max 8000` | Declared assumptions only; stdout design size/power; actual flags verified in source/help/tests |
| Design cutoff | `python scripts/certification_power.py --true-rate 0.03 --true-pass-rate 0.65 --n 970` | Pure binomial design output; no portfolio input |
| Focused engineering verification | `python -m pytest tests/test_certification_power.py tests/ops/test_policy_fingerprint.py -q -p no:cacheprovider` | Set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONDONTWRITEBYTECODE=1`; synthetic/public fixtures; isolated temp directory;150 passed on recorded bytes |
| Synthetic component timing | `python ops/c1_rail/qualification/prepare_compute.py` | No private arguments accepted, stdout explicitly draft; fresh primary `tmp/phase3-preparation-*.json` output; single-process |
| Governance prose | `python scripts/check_governance_prose_control_chars.py` | Read-only prose validator; does not establish F1 readiness |
| Current repo check composition | `python scripts/gate_manifest.py --tier check` | Real entry point; selected manifest owns checks. Not run/claimed merely because listed |
| Fingerprint | Python library only: `build_shared_manifest(*,policy_row,geometry_source,registry_rows,components,tool_source,dependency_artifacts)` and `verify_shared_manifest(expected,**observed)` | Exact bytes plus authenticated expected inventory; output shared identity, no freeze/approval; include actual runtime distribution and full transitive inputs |
| Registry/config | `validate_registry(source,expected_rows=...)`; `canonical_config_bytes(config)`; `validate_initial_arm_delta(before,after,authorized_deadline=...)` | Pure library; expected approvals independent; pre-D0 registry `{}`; no arm performed |
| Ratified calendar | `load_ratified_calendar(path,overlay_path=...,ratified_path=...,repo_root=...)` | Actual library signature from source; operator-pinned calendar/evidence/overlay; output bounded `SessionCalendar`, no account close |
| Snapshot, later only | `python scripts/seal_account_snapshot.py --manifest <private-manifest> --e1 <dashboard> --e2 <flatness> --e3 <history> --output <ignored-private-seal>` | Flags verified by `--help`, tool not run. E1/E2/E3 here are **evidence role names**, not qualification stages. Caller authenticates facts. Fresh B7 after required chain; no seal for this pristine-E1 preparation |

Snapshot defaults `--freshness-minutes=30`, `--seal-hours=24` do not extend C10
beyond the actual close/reopen boundary. Source file hashes and an attestation
tool cannot fill missing account facts. Snapshot output and later qualification
numbers belong under the primary ignored private root, never this worktree.

## Required execution sequence and owned gaps

| Stage | Exact preconditions and required input→output | Present tooling / bounded missing interface | Owner and acceptance evidence |
|---|---|---|---|
| Final F1 validation | All F01–F50 relevant gates; accepted merged integrated revision; complete source/runtime/calendars/configs and every proposed field resolved→authenticated immutable contract and complete shared manifest | G1 `contract.validate_frozen_contract` verifies canonical bytes, complete observed inventory and external freeze approval. It does not issue approval. Final context/closure integration pending. | Phase2 / independent combined acceptance; actual identities and operator approval remain absent |
| Exact-depth second decision | Frozen F1+actual d+budget/timing+tool/runtime/vectors→dated operator addendum bound to those identities | Human governance decision, no automatic ratifier. [Draft text](compute-depth.md) not sent for approval | Operator/coordinator; authenticate second addendum separately from first; withheld→BLOCKED context |
| E1 legality screen | F1 and both decisions, registry empty, exact accepted inputs→terminal screen verdict/evidence | G2 `preflight` validates external depth approval and reserves a fresh output root; `AttemptStore` owns durable one-attempt checkpoints. | Phase2 / combined acceptance and actual approval; failures terminal |
| n1 | Screen PASS; frozen namespaces/depth/initial state/cutoff. Draft proposal:200 per population and failure≤10. | G3 `ProductionSource`, `ProductionExecutor` and `run_production_e1` wire retained sources through continuous replay and the shared kernel. Depth comes from the validated contract. | Phase3 / source and combined composition acceptance; no outcome-bearing run performed |
| n2 + Part B | n1 PASS; disjoint n2. Draft proposal:970 per FULL/H1/H2, three exact failure bounds and FULL speed lower. | One joint G3 draw yields N2 FULL and PART_B halves; controller prevents separate redraw and preserves stage identities. | Phase3 / integrated acceptance; exact-depth proposal is not ratification |
| Part A within E1 | Frozen positive depth+second decision; reserved n2/REGIME children→100 panels, prescribed200 expansion, p5/sanity | G4 `part_a` and `regime` implement six-month outer selection, fresh continuous alternate-panel proof and rebuilt five-session inner blocks. | Phase3 / construction, source/schedule and combined acceptance; depth read from frozen contract |
| E1 seal | Every required screen/n1/n2/PartA condition PASS on same contract; Part B already included→FBR containing exact contract+n2+PartA digests | G5 result validator, adjudicator, external producer authentication and sealer are implemented. Receipt mutation at1465c36 was repaired and independently verified atb8f929d; runtime binding and signed test-domain composition remain pending. | Phase2 / Phase1 independent combined acceptance; no production seal issued |
| D0, future | E1 PASS/FBR; both dated ratifications, policy/cell/provenance equal→one exact registry row | No automatic admission command claimed; source/governance change belongs D0 | D0 owner; non-vacuous chain tests, no `reference_mode_for_dd_type` dispatch for this row, normalized hash equality plus independent provenance validation |
| D1 ORB GO, future | Prescribed E1 book-level PASS and ORB-specific supersession evidence→separate operator ORB decision | Human approval/owning ORB ADR; no request sent | Operator/coordinator; missing GO blocks V1, not a failed result or reason to remove ORB |
| V1/image/live/B7, later | D0+D1, actual route/source readiness and accepted dry-run image→runtime binding/EF1/fresh S | Existing component tools are not combined release acceptance | V1/I3/T1; later separately authorized work |
| sole n3, later | Fresh B7 S + unchanged FBR/EF shared identity + retained D1 + still-valid no-activity chain→four conditions once | G3/G5 require a final stage with reserved n3 and no Part A | E2; after prescribed PASS only D2/GO reseal; no n3/B7 here |

Required G1–G5 interface fields, **not command-line flags**: immutable contract input;
approved source/runtime manifest; accepted private evidence root; distinct new
private output root; authenticated approval records; explicit stage and persistent
attempt ID; expected prior stage result digests; budget/timing identity; observed
runtime/tool/dependency bytes; stop/status diagnostics with no result values on
public stdout. Stages must reject this preparation's Markdown/JSON class, unknown
schema, partial manifests, unaccepted source generation, populated registry before
D0, stale integration evidence, invalid RNG allocation, missing budget, and
unapproved exact depth. They must never infer permission from a path name or
`status=PASS` supplied by the caller.

The implementation lives in `ops/c1_rail/qualification`. Source-free construction,
statistics, attempt-state and seal tests remain distinct from private parity.
Before any real qualification, obtain independent combined review, measured
compute approval, accepted source/schedule parity and all F1 gates. The final
invocation inventory must match the reviewed successor APIs; the moving security
and test-context interfaces are not presented as approved execution commands.

## Output locations and immutable evidence

- Existing accepted private inputs remain under primary
  `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/`.
- Proposed future result root: primary
  `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/qualification/<frozen-contract-digest>/<attempt-id>/`;
  its owner must verify `git check-ignore` and create a new nonexisting root before
  running. This is a location proposal, not an issued attempt or created result.
- Bounds, curves, replay/stress statistics, account values and source code remain
  private. Public contract/digest/verdict and permitted exclusion/idle counts only.
  Synthetic design power/timing in this preparation is labeled and uses no portfolio
  outcomes. Retain original evidence; never overwrite admitted manifests to repair
  a digest. Retried engineering checks never become replacement qualification draws.

## Adjudication table (P1 §4; P2 §4/T0–T11; SNAP C10)

| Event | Required disposition | Forbidden inference |
|---|---|---|
| Missing/unaccepted implementation, evidence, first/exact-depth approval or GO | BLOCKED at its named consuming gate; pending decision is context-problem | Not FALSIFIED; do not bypass or invent acceptance |
| Failed legality screen, n1 cutoff, n2 limb or Part A | R1a: attempt ends, no qualifying configuration/admission; closure supersedes proposed admission | No runner-up, grid, extra paths, diagnostic relabel or new stream |
| Failed sole n3 | R1b: terminal failure; retire admitted row under owning process; no deployment | No repeated n3 or expanded sample |
| Required field genuinely unfreezable during F1 or later | AMBIGUOUS; attempt closes; successor requires new operator decision | Pending integration field in this preparation is not automatically unfreezable |
| Snapshot expired or intervening fill/order/adjustment | C10/R1c: seal and dependent evidence void, stop for operator; remove/revoke any dependent GO via owning process | Fresh seal alone cannot validate old result; no automatic replacement draw, even if called continuation |
| Permitted non-shared build-context change | Only P2 T10/R1c's narrow process; new B7/continuation authority as required | Shared or non-GO layer change is not covered by that exception |
| Shared-component/non-GO image-layer drift after sealed chain | T10 failure ends attempt as specified; stop, no silent rehash | No changing private inputs, substitutions or independent normalizer |
| Part A sanity discrepancy / corrupt artifact / incomplete output | Stop and preserve evidence; coordinator adjudicates integrity/contract failure under frozen contract before any continuation | Never discard offending panels or draw replacements; failed criterion remains terminal |
| Runtime exceeds budget | S2 RC-3 NEEDS_CONTEXT before batch; no approximate/spliced substitute | No silent depth/horizon reduction or extra compute fan-out |
| Missing bar/coverage versus deadline failure | Predefined missing coverage may exclude source sessions with counts; scheduled flat failure is a path failure/T=∞ | Do not exclude bad outcomes to improve bounds |

The frozen command controller must preserve these distinctions on crash/restart,
ambiguous dispatch and partial output. Idempotent status/read is permitted;
rerunning an outcome-bearing stage is not authorized merely because its receipt
was lost. Final n3 belongs after fresh B7 in Phase 6, and Part A is not rerun there.
## 2026-09-16 post-413 engineering update

Tasks 1-4 of the post-413 integration handoff are accepted for synthetic engineering only. Earlier text in this dated document remains historical. See [post-413 integration acceptance](../2026-09-16/post413-integration-acceptance.md) for the selective integration inventory, actual commands/interpreters, exact base and dirty-tree evidence, failures and repairs, complete signed source-to-seal route, rejection/restart coverage and independent whole-flow review.

Direct checks passed 6 signed composition cases, 350 qualification cases and 44 independent provenance cases. Final operations passed 2,841 parent tests with 15 private-input skips, plus all 394 qualification/provenance child cases without skips. Repository gates passed with disclosed host-capability/private-artifact limits; 23 focused Linux image checks passed. All accepted records completed with stable source, complete capture and verification exit zero. PR409 behavior and PR413 launcher/recorder remain preserved. Windows operations used the checkout's validated Python 3.13.2 interpreter; Linux image tests used the recorded Python 3.11.16 environment. Tested HEAD is b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac with the integrated dirty tree.

This does not accept private source/settings/schedule inputs or authorize F1, exact-depth approval, production E1/n3, D0, ORB GO, B7, deployment or arming. Representative compute preparation and remaining operator decisions stay at their later gates. Historical bare-Python recipes above are not operative: use this checkout's validated fp.ps1 launcher for operations work. Work remains an uncommitted local integration; no publication or deployment occurred.
