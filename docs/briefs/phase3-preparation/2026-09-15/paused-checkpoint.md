# Phase 3 paused checkpoint

**Paused by user instruction: “let's aim to complete phase 2 and stop there”.**
No further Phase 3 implementation, qualification composition, benchmark refresh,
freeze or approval work is authorized by this checkpoint. All delegated Phase 3
agents are finished. Existing work is preserved in the isolated worktree.

## Location and revision

- Branch: `codex/phase3-qualification-tooling`.
- Worktree: `C:\Users\joshu\multi_firm_operations\.worktrees\phase3-f1-preparation`.
- Starting base: `d107ebdfaec194ac4b4448d1d121331ff7128e1a`.
- Last engineering commit: `8f09a6266be671890cf4e0693664612eeded7a8a`.
- The documentation commit containing this file preserves the remaining packet
  edits. No main merge, PR, actual qualification, F1 freeze, final depth decision,
  admission, ORB GO, B7, n3 or live action was performed.

## Exact current evidence

| Checkpoint | Tested/reviewed scope | Limit |
|---|---|---|
| `b7209ed` | Independent 83 passes: 62 replay and 21 source tests; additional chained live-position split vector. Requires intrabar evidence only for exposed/pending legs and validates supplied source claims. | Two signed-source cases then awaited G1; later source run below covers them. No coverage-rule amendment or actual finer market evidence. |
| `28e5067` (Phase 2 `f6a1426`) | Owner reported 76 focused G1/journal/composition/driver/controller passes and two additional contract mutation/buffer regressions. Signed domain and validator-issued G1; journal domain persisted across reopen. | This does not finish domain-aware preflight or G5. |
| `8f09a62` | Source owner ran 50 source/loader/signed-fixture tests: all passed in 90.95s. Includes genuine signed G1, eight source mutation/copy cases, flat replay without unused quotes, supplied-evidence contradictions and public production refusal of TEST_ONLY inputs. | Synthetic source fixtures only; no historical production acceptance. |
| `8f09a62` | Independent reviewer ran all 11 driver tests, then the updated single-initialization regression: one pass. Reviewed source/loader/executor state guards with no remaining bounded findings. | Full pipeline and combined final suite have not run at this revision. |
| Commit hooks | Latest commit passed configured governance, path, dependency-boundary and monitoring checks; 631 first-party modules checked. | Private Pine files absent locally; hook warning does not certify those files. |

The source guard binds exact factory issuance and a typed digest of all derived
state. The executor binds its original contract/source/store/domain, prohibits
reinitialization, derives fresh initial state from G1 and keeps its provider and
budget clocks outside writable instance fields. Source verification traverses
the full derived graph and rehashes retained bytes; old bare-replay timings do
not measure this cost.

## Explicitly unfinished

The signed TEST_ONLY **full source-to-dispatch-to-replay-to-G5-to-seal pipeline is
not accepted and has not passed**. Component positives are not a substitute.

`test_composition_route.py` contains the positive route and negatives for real
receipt-persistence failure/reopen/no redraw, retained byte changes, valid
replacement-key signatures using enrolled IDs, actual import aliases and
cross-wired independently signed domains. The updated tests have been reviewed
by inspection but have not executed end to end. They require the pending
domain-aware preflight and G5 interfaces from the Phase 2 owner; that work is now
deferred under the scope change, not a prerequisite to original Phase 2 closure.

No final combined qualification suite, final Phase 1 full-flow review, final
representative measurement or control-cost profile was completed after these
changes. Prior timing observations remain provisional historical engineering
measurements, not current accepted budgets. Draft n1=200, n2=n3=970 per population,
Part A depth200 and horizon500 remain proposals.

## Narrow handoff to original Phase 2

The owner already has its canonical import repairs (`b4bbfb4`, integrated here as
`7d72408`) and runtime-bound adjudicator repair (`afdf69c`, here `299a56f`). The
adjudicator is qualification work and does not itself gate original runtime
closure.

Potentially relevant shared runtime history is the shared schedule classifier
`9a1a91c` and the native empty-scope exit fix in `bb21d77`. The latter commit also
contains qualification changes: if needed, the original runtime owner should
take only its native-emulator change and affected tests, or verify its existing
equivalent. No broad cherry-pick is prescribed. The qualification loader append,
source factory, Part A, signed domain and G1–G5 additions are deferred Phase 3
work; the historical loader remains distinct.

No additional original-Phase-2 runtime fix is currently requested from this task.
The Phase 2 owner determines its actual dependencies and independent acceptance.

## Restart only on later authorization

1. Reconcile this branch with the final accepted Phase 2 revision and inspect
   any paused owner edits before taking further commits.
2. Finish the domain-aware preflight/G5 interface integration; preserve G1
   issuance and existing Phase 1 mutation regressions without weakening them.
3. Run the genuine signed full composition and its substitution/recovery tests,
   then obtain independent whole-flow review and appropriate combined checks.
4. Refresh representative single-process timings and separately measure source
   verification, proofs, controller, runtime capture and durable G5 costs.
5. Update the packet with those actual results. Missing source/settings/calendar
   facts and F1/exact-depth decisions remain their named consuming gates.

This is a preservation and restart inventory, not permission to perform those
steps now.
