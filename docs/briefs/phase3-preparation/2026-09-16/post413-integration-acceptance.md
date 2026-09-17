# Post-413 Phase 3 integration acceptance

Status: ACCEPTED for Tasks 1-4 synthetic engineering integration only. This record grants no F1,
exact-depth, production E1/n3, D0, ORB, B7, provider, deployment or arming authority.
User authorized execution of the post-413 handoff Tasks 1-4 on 2026-09-16.
Coordinator: the integrating Codex task; component work is not combined acceptance.

## Baseline and preservation

Origin refreshed before creating `codex/phase3-post413-integration` in
`.worktrees/phase3-post413-integration`. Base and current HEAD:
`b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac` (PR413 merge), containing
`845fb13ed2141482649627f5b78a51f4cadbd61d` (PR409 merge). New worktree was clean.
No newer remote main changes were found. Primary checkout remains at `c2e6eb2`;
its untracked work and every pre-existing worktree remain preserved.

Read root AGENTS.md, scripts/README.md launcher/evidence instructions, qualification
control/tooling plans, simplified Phase3 work-package1, PR409 bounded correction
and integration evidence, and both preserved checkpoints. The historical
[paused checkpoint](../2026-09-15/paused-checkpoint.md) remains unchanged history.
The recovered preflight/G5 checkpoint f9ff974 is unreviewed input, not acceptance.

## Integration inventory

| Behavior | Source | Disposition |
| --- | --- | --- |
| Qualification package, CLI/status, source and replay, tests | `35fae36169f056600286081c44edcc53bf618880`; engineering through `8f09a6266be671890cf4e0693664612eeded7a8a` | Retain qualification-only additions, then repair demonstrated integration failures |
| Domain-aware preflight/result/authentication/seal | recovered `f9ff974decef0c7f008fd1998ae0621697283a86` over `6dfca2ba5f73a3b0573c03483d45c2bdf9b4a866` | Reconcile two-file diff; signed fixtures and end-to-end acceptance completed below |
| Qualification adapter loader | `8e5c6ec`, `ee0193e`, `8f09a62` | Append dedicated loader to current main; preserve main historical input identity and reviewed ORB runtime successor logic |
| Three-instant replay schedule classifier | `9a1a91c` | Retain additive classifier; preserve current main account schedule classification, including post-close DEADLINE |
| Native empty/stale close scope | emulator-only hunk of mixed `bb21d77` | Main lacks equivalent; four integrated replay failures reproduce defect. Retain narrowly scoped registration guard and related tests |
| Account owner, capacity, settlement, source identity/feedback fixes | earlier `4abc30a`, `7d72408` and shared history | Current main equivalents/successors retained; old files rejected because replacement would remove409 protection/takeover/bootstrap/settlement fixes |
| Runtime timing dependency | current409 owner imports runtime only for period/slack | Share unchanged constants through pure book protocol; keep runtime exports and consumer timing semantics. Avoid accidental qualification dependency on legacy listener imports |
| Full-suite import isolation | qualification collector versus legacy flat/canonical test imports | Run qualification in a clean serial child during unfiltered ancestor-suite collection; retain child JUnit/output and bind hashes/counts in parent JUnit. Explicit focused qualification runs unchanged; no relaxed alias check |
| Launcher, root instructions, lock/environment, recorder |413 | Retain unchanged; historical bare-Python recipes are not operative |
| Preparation documents |35fae36 | Preserve dated history; update execution/tooling-review only with actual new evidence |


## Repairs and related-case review

- Preflight, result and seal require the validator-issued trust domain and its actual enrolled key bytes. Result verification additionally compares the registry key object's ID with the envelope's key ID; a seal-role key cannot be placed under a producer-role registry label. The shared verifier has reproductions for both result and seal scopes.
- LEGALITY digest producer/consumer now includes the same trust-domain identity. Other checkpoint seed subjects, approval revalidation, result identity and durable attempt bindings were inspected together.
- Adjudicator validation compares live executable definitions against the verified retained source in each decision dependency module, including transitive helpers and generated dataclass methods. Reproductions cover entrypoint code, certification helper and rule/decision constructors both before freezing and after freezing. Matching source labels cannot legitimize changed executable decisions.
- G5/controller/CLI unit fixtures now obtain genuine signed domains and G1-issued contracts; no SimpleNamespace contract or synthetic-authority flag substitutes for issuance. Fixed synthetic clocks and retained runtime inventories remain explicit. The real route signs its actual output-role contract before execution.
- Four replay cases reproduced empty/stale close registration in the native emulator. The minimal guard and four native emulator tests preserve current main's remaining implementation. Schedule classification is additive; existing post-close DEADLINE behavior remains. Period/slack constants move unchanged to the pure protocol to remove the reverse import dependency into the legacy listener.
- Both image import guards reproduced missing qualification contract/trust-domain files. Three stdlib support files (__init__, contract, trust_domain) are now listed explicitly in both Dockerfiles, .dockerignore and both image-validation inventories. No qualification execution or CLI surface was added to the image recipes.
- The operations suite runs qualification serially in a clean child because legacy tests deliberately load flat and canonical module aliases. Child JUnit/output, hashes, command and counts are retained in the parent's evidence directory and parent JUnit. The bridge requires all six signed composition tests to execute without skips. No alias check was relaxed, and sys.modules is not rewritten.

## Rejection and recovery coverage

| Boundary | Executed coverage |
| --- | --- |
| Actual enrolled key bytes and role/registry identity | `test_trust_domain`, `test_result_key_binding`, signed composition replacement-key cases for preflight/result/seal |
| Independently signed foreign domain; contract/source/store/domain cross-wire | signed composition cross-wiring plus `test_production` issuance/replacement cases |
| Retained byte mutation, derived-state mutation/copy, reinitialization | `test_production_source`, `test_production`, signed retained-byte/alias composition cases |
| Receipt persistence failure after actual replay; reopen after possible dispatch | real composition disk-failure case; `test_attempt` checkpoint capabilities, atomic result/receipt rollback, lost receipt, boot fencing and read-only inspection |
| Changed inventory or adjudicator dependency | `test_runtime_inventory` closure/origin/alias cases; eight before/after executable-tampering cases in `test_result_adjudication` |
| Result substitution, wrong scope/attempt and seal-before-commit | `test_seal`, `test_result_key_binding`, signed positive's negative assertions; wrong attempt does not authenticate |
| Duplicate commit/seal and lost response | signed positive refuses duplicate authenticated commit without adding events, reopens identical committed result and repeats identical seal; journal recovery cases |
| Approval expiry before next dispatch | real signed expiry case preserves completed N1, pending later checkpoints and identical checkpoint state across reopen |
| TEST_ONLY refusal at public production boundaries | real signed positive and `test_production`/`test_trust_domain`; all seal capability grants remain false |
| PR409 runtime compatibility | full operations plus native replay/schedule, account owner, takeover, settlement, capacity, feedback, bootstrap and image regression tests |

## Independent review

A separate read-only whole-flow reviewer, `/root/whole_flow_review`, covered retained source -> authority -> durable attempt -> adjudication -> authenticated result -> seal, the rejection matrix and narrow PR409 compatibility changes. It found the executable-binding family described above. After repair and reproducing tests, it accepted the implementation with no remaining actionable runtime findings. Its final test assertion finding was corrected to the actual expiry error. Follow-up review accepted the exact image closure additions. The reviewer did not execute tests; coordinator-owned recorded runs provide test evidence. The retained review disposition is `.cache/phase3-post413/whole-flow-review.md`.

## Evidence interpretation

All local records are relative to the integration checkout. Failed diagnostic records remain preserved; none is reclassified as acceptance. Final Windows commands use `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe` (3.13.2), selected and validated by this checkout's launcher. HEAD remains `b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac` with the integrated dirty tree; no commit, push or PR was performed. Tests and implementation were stable throughout each accepted run. Subsequent edits to this record and the two preparation addenda only describe evidence; they do not change tested executable files.

The positive JUnit retains contract/domain/result/seal/runtime-inventory/event-head digests and hashes of all 98 retained input/runtime roles. JUnit properties are present despite pytest's xunit2 portability warning. Synthetic sources use temporary test directories, so these hashes supplement PR413's exclusion of ignored/external files. Each run generates fresh synthetic signing keys; artifact digests differ between runs by design. This is not private source acceptance.

Additional whole-suite reconciliation: `test_phase3_provenance_acceptance.py` now retains the reviewed ORB runtime-input successor digest and uses actual enrolled producer/seal keys with explicit domain arguments. All 44 tests passed, preserving positive baselines before mutation and each adversarial assertion. The whole-suite child includes this complete file and requires all 13 repaired boundary cases, in addition to the six signed composition cases, to execute without skips. Independent follow-up review accepted the change.

The first bridge retained generated Python fixtures under `.cache`, which the source boundary gate correctly inspected and rejected. The bridge now uses an external `TemporaryDirectory` for child scratch, retaining only JUnit/output/digests in the checkout. The original scratch was preserved at `C:/Users/joshu/multi_firm_operations/tmp/phase3-post413-preserved-pytest/20260917T010832Z-71c5b8fd3f82`; `.cache/phase3-post413/preserved-scratch-location.txt` records the move. No gate exclusion or validation rule was changed. Gate rerun passed, and independent review accepted the scratch lifetime/evidence handling.

## Final verification and limits

Commands ran serially from this integration checkout through its own launcher. Windows interpreter: C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe, Python 3.13.2. Doctor passed before Python work: all 62 locked packages matched; cryptography 50.0.1 present. Accepted records have completed status, verification exit 0, complete capture and stable source.

| Command (prefix ./fp.ps1) | Record under .cache/fp-verification | Result |
| --- | --- | --- |
| python -m pytest tests/ops/qualification/test_composition_route.py -q --tb=short | 20260917T005348Z-b08732938c59 | 6 passed, 0 skipped |
| python -m pytest tests/ops/qualification -q --tb=short | 20260917T005712Z-bbbb20c3b5af | 350 passed, 0 skipped |
| python -m pytest tests/ops/test_phase3_provenance_acceptance.py -q --tb=short --maxfail=3 | 20260917T012409Z-7df813a08992 | 44 passed, 0 skipped |
| check | 20260917T012711Z-b35a35740970 | All selected gates passed |

The check command's evidence-store gate ran 72 tests with 3 Windows symlink/FIFO capability skips. Private Pine sources, three private data trees and eight heavy lab artifact groups were absent; their checks reported warnings or absent-tree skips rather than verifying nonexistent private bytes. Existing advisory instrument/session notes remain in stdout. No ops implementation file changed between the direct 350-test pass and final operations run.

The documented Linux harness command was:

    ./fp.ps1 python -X utf8 scripts/docker_verification.py --test-path tests/ops/test_c1_rail_image_manifest.py --test-path tests/ops/test_c1_signal_daemon_image_manifest.py --test-path tests/scripts/test_c1_image_validation.py

Record .cache/fp-docker-verification/20260917T013314Z-35159a2d60d2/record.json: 23 passed, 0 skipped in 61.36 test seconds; completed, stable source, complete capture, verification exit 0 and confirmed owned-container cleanup. Interpreter /opt/ops/bin/python, Linux/WSL2 Python 3.11.16, all 62 locked dependencies matched. Image sha256:e67ed55b30611698c82a44c992eb291b77bf127dc48f28008e96113c4d3e10c3. Tests ran with networking disabled and a read-only checkout. Generic owner/runtime coverage targets were not exercised by this focused selection, so coverage emitted no-data warnings; no runtime coverage percentage is claimed.

Linux preparation retained two not-started records: dependency fingerprint mismatch (20260917T012818Z-1a25effa8e35), then Windows cp1252 decoding of Docker build output (20260917T012905Z-ecd46bb10e54). Documented --build plus Python -X utf8 resolved setup without changing PR413 tooling. The next executed record (20260917T013118Z-9f2e97eec06f) had 12 passed/11 failed because CRLF shell bytes made Bash reject pipefail. The exact shell script is now LF-pinned in .gitattributes; the 23-test passing rerun verifies that repair. All these records confirmed cleanup.

These are local Windows and focused Linux tests, not hosted CI or an exact ubuntu-latest reproduction. Deployment image builds and the full deployment-image ceremony workflow were not run; focused tests verify import closure, packaged imports and shell fault handling. No deployment, service arming, provider action or private credentials were used.


Final ./fp.ps1 test-ops -q --tb=short: **2,841 passed, 15 skipped**, 0 failures, in 764.15 test seconds. Record 20260917T013451Z-d87e990d94a6. Its clean child passed all **394 qualification/provenance tests**, 0 skipped, in 575.91 seconds. The parent count includes the one bridge test; child cases are reported separately. Parent JUnit records the child's command, report/output paths, hashes and counts. The 15 skips are 8 missing effective-input cases, 4 absent private strategy ports and 3 absent private Striker regressions. None is a decisive signed qualification case.

The final run's positive case retained hashes for all 98 synthetic input/runtime roles and these identities:

| Identity | SHA-256 |
| --- | --- |
| synthetic_contract_sha256 | 2d3499dfff7fc1fb549ebbf8b72765f77db92a1067838fda32fb3da1b88ed52b |
| synthetic_trust_domain_sha256 | 89f9cc5fe0bcc502042fcf93ae8f9008cd63af707377932eb70c3e6e4ec271f1 |
| synthetic_result_sha256 | f4a14fa90fe8076ec90986edac81279e04762428b21bd1c5915bd4a3b1e1ea39 |
| synthetic_seal_sha256 | e7d432ec6743331d2117fa4b01e3c3b1c711b90b4128502024f0e6e07405b5cc |
| synthetic_runtime_inventory_sha256 | a5aa09c8d183122b6f408d0cc554eb5abcfcbe36bafe152ea95c56ab4d22ec36 |
| synthetic_reopened_event_head | a4d1142e02a192c588cfe0b81cd2aeb62d437930ee7dace67d43ac9bf4d2da0d |

Final operations source fingerprint: d8bb3fec99fa1f33ea2cad050818b3342414216fc0bcd059663c62ff3ba2d916. Diff SHA-256: a85731df7f7f62ec27e74b16d08a4f189c565ea43888967b2a3655574f6ece80.

## Diagnostic record ledger

Each row is under .cache/fp-verification/<record>/record.json. Full commands, interpreter metadata, source snapshots, stdout/stderr and JUnit remain retained. Durations are recorder wall time including launcher overhead. Failed diagnostic records remain failed; no historical component result substitutes for integrated acceptance.

| Record | Actual result | Stable source / complete capture | Wall seconds |
| --- | --- | --- | --- |

| 20260917T002419Z-376da6220eaa | 0 passed / 1 failed / 0 skipped | True / True | 33.17 |
| 20260917T002515Z-390e148edfb9 | 0 passed / 1 failed / 0 skipped | True / True | 11.42 |
| 20260917T002635Z-fab0f22ea11a | 298 passed / 40 failed / 0 skipped | True / True | 254.44 |
| 20260917T003439Z-37063a838916 | 3 passed / 5 failed / 0 skipped | True / True | 230.35 |
| 20260917T004001Z-5ce2c6eb9f1c | 15 passed / 10 failed / 0 skipped | True / True | 27.83 |
| 20260917T004153Z-260943833d4e | 22 passed / 3 failed / 0 skipped | True / True | 29.46 |
| 20260917T004338Z-432fdbe1cbc9 | 124 passed / 0 failed / 0 skipped | True / True | 126.72 |
| 20260917T004653Z-b819c87bcee9 | 5 passed / 1 failed / 0 skipped | True / True | 201.53 |
| 20260917T005024Z-8b268b3b29ab | 6 passed / 2 failed / 0 skipped | True / True | 9.17 |
| 20260917T005136Z-9e32eeede082 | 17 passed / 12 failed / 0 skipped | True / True | 111.21 |
| 20260917T005348Z-b08732938c59 | 6 passed / 0 failed / 0 skipped | True / True | 186.35 |
| 20260917T005712Z-bbbb20c3b5af | 350 passed / 0 failed / 0 skipped | True / True | 654.02 |
| 20260917T010832Z-71c5b8fd3f82 | 2872 passed / 13 failed / 15 skipped | True / True | 843 |
| 20260917T012409Z-7df813a08992 | 44 passed / 0 failed / 0 skipped | True / True | 64.95 |
| 20260917T012535Z-132fcb341c72 | failed; verification exit 1 | True / True | 43 |
| 20260917T012711Z-b35a35740970 | completed; verification exit 0 | True / True | 54.17 |
| 20260917T013451Z-d87e990d94a6 | 2841 passed / 0 failed / 15 skipped | True / True | 771.94 |

Early failures reproduced missing schedule/closure integration, stale G5 fixtures, result key identity, executable adjudicator drift and LEGALITY digest mismatch. Mixed Windows image/composition record 20260917T005136Z-9e32eeede082 also captured sandbox-denied Bash directory creation and correctly rejected legacy import aliases; subsequent clean-process qualification and Linux image runs cover these paths without relaxing validation. The first operations failure and source-gate scratch failure were repaired as described above. Failed records remain failed.

## Later preparation remains separate

Actual input/settings/calendar/schedule acceptance, representative full runtime and compute budget, unresolved freeze definitions and separate operator decisions remain prerequisites at their owning later gates. Historical synthetic timings and current test timings do not establish a production-data budget. The historical paused checkpoint is unchanged. This acceptance stops before actual F1, exact-depth approval, production E1/n3, D0, ORB GO, B7, provider actions, deployment or arming.

## Evidence-document closeout

Final ./fp.ps1 check after the three documentation updates also passed: .cache/fp-verification/20260917T014846Z-601c296d97fb/record.json; completed, verification exit 0, stable source and complete capture. Source comparison against the accepted operations run found exactly the three evidence documents changed and no executable/test/configuration changes. This final record reference and table spacing are evidence-only edits. git diff --check passed. Work remains uncommitted on codex/phase3-post413-integration.
