# Independent provenance and acceptance review — G1–G5

**Disposition: historical admission preserved; new runtime/tooling acceptance
not established.** Review baseline `d107ebdfaec194ac4b4448d1d121331ff7128e1a`;
historical admission runtime `c86a0a0a17b433e690b700914662868c0d5f7ece`.
This is an engineering review, not F1 freeze or a qualification result.

## Ownership and evidence classes

Coordinator task `01a0a70d-9f04-7162-8b19-09e94c059ac4` assigned this bounded
review. Phase 2 task `01a0a71c-3bb5-78d2-9558-8950a9d04a42` owns G1/G2/G5 and
runtime/account serialization; Phase 3 task `01a0a758-94ce-7301-bb6e-af5c88d50d9f`
owns G3/G4 and tooling integration. Phase 3 explicitly assigned this document
and `tests/ops/test_phase3_provenance_acceptance.py` exclusively to this reviewer.
The review worktree is `.worktrees/phase1-provenance-review`, branch
`codex/phase1-provenance-review`; the original Phase 1 workspace is preserved.
No shared production source is edited here.

The preparation packet was read at its recorded `c86a0a0` baseline before
implementation. Its draft depths, horizon, calendars and budget are not approval.
Governing clauses below refer to:

- **S2:** `docs/spec/2026-09-12-tradeify-synchronized-replay-spec.md`, including
  sizing and attended-incident amendments.
- **P1:** `docs/briefs/pre-registration/2026-09-12-track-b-final-validation-prereg.md`,
  especially §§2–6, 9 and 10a, with subsequent ratifications preserved.
- **SET:** `docs/spec/2026-09-15-tradeify-attended-settlement-contract.md`.
- **PH1:** retained formal Step 6 contract/review/run and accepted Step 3 contract.

Historical accepted replay, new synthetic component verification and actual
source qualification are separate evidence classes throughout this review.

## Identity impact at d107ebd

The admitted seven manifests, original private sources and panels are unchanged.
The reviewer freshly compared the 19 supplementary runtime pins: **18 unchanged**;
only `ops/c1_signal_daemon/book_adapters.py` changed from
`83830d5e10e50c06a2ebd37511146d5f0e47f0fd467155693279a704a17beec5` to
`16bf5045540f169be12e69acc90ec4f9809dd0fff67a1f3ae4f71f8323771aef`.

| Leg | Accepted executable-port identity adopted at d107ebd |
|---|---|
| Aegis | `11763740bc3fdcc8b9e94cb0b465823aec202cd8333379c46878185db5e9e84f` |
| Striker | `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4` |
| Vanguard | `e6a03d04c65a19e7fde71103560a229630c3663f445676f06622feec4e9157a3` |
| ORB | `b1f4e573009e62b976013e08e7ef2784497d840f490f04e3878fdaef553f317d` |

The preserved original Striker `c81aa59c…` is not an alternative admitted runtime.
Aegis's accepted panel is the separately attested 88-bar-prefix derivative,
`8ae083d07b6870aa427dc69009434da0f3cab2d6818ca356e441ad40f3648fd2`.
Vanguard's installed-body capture hash and registry Pine identity are distinct
evidence roles; retain the accepted source/settings interpretation, not a false
assertion that those raw bodies have the same hash.

The six calendar artifacts in the preparation identity ledger are unchanged.
`book_session_calendar.py:248` now carries flatten/deadline fields into
`BookSession`; it grants no new date coverage. Outside the old 19-file closure,
`book_sizing_context.py:267` changes potential top-priority takeover treatment;
the new owner/runtime/scheduler must be added to a complete new dependency binding.

**Reuse decision:** retain old nine-reference Step 3 and seven-bundle Step 6
acceptance for their exact source/settings/cold-origin domain. Do not reissue
their contract with new runtime hashes. New loader, effective settings, owner,
schedule and path assembly require separate affected acceptance; successful
construction or no-action bars do not transfer strategy behavior evidence.

## Actionable findings

### I1 — verified source can differ from executed code

At `book_adapters.py:116–127`, importlib executes the module before the source
hash check. A timestamp-based cache can execute old code while the subsequent
hash matches accepted new source. `effective_inputs.json` is also hashed and
then independently reread at lines 137–139.

Three independently authored synthetic tests reproduce this at d107ebd:

1. Unaccepted module writes a marker before its digest refusal.
2. Same-length/same-mtime accepted source executes old cached code.
3. File replacement after the verified read changes consumed effective settings.

Required owner repair: execute/parse the already-verified immutable byte buffer;
refuse wrong source before execution; avoid cache/path rereads. The historical
`run_bundle_parity` byte-snapshot route supplies the relevant existing pattern.

### I2 — historical ORB settings do not satisfy the new owner input contract

`load_book_adapters` uses historical effective-input digest `66406dee…` and passes
its ORB quantity to the corrected port. That port emits the configured quantity;
`book_account_owner.py:999` passes it as `normal_base`. Shared policy
`book_policy.py:309–311` rejects it because it differs from the fixed base and
both admitted ORB comparison settings. The existing private-loader test
`test_four_leg_runtime.py:256–277` intentionally produces no actions.

Required disposition: a separately reviewed settings binding for this new
consumer and actual-trigger sizing/feedback evidence. Preserve historical inputs;
neither repinning the original file nor a synthetic no-action barrier proves
the runtime configuration accepted.

### I3 — local refusal feedback boundary is missing

At `book_account_owner.py:1043–1051`, size/authorization refusals return no events;
`book_runtime.py:224–235` only delivers confirmed events. An adapter that already
recorded an intended entry can retain it despite no broker submission. The
historical `BundleExecution` route explicitly supplies zero-size rejection.

Required disposition: durable, separately labeled local-refusal feedback through
adapter checkpoint/recovery, with zero-size/capacity refusal tests using the real
ORB pending-state behavior. Do not manufacture a broker-confirmed fact.

### I4 — schedule driver remains an integration dependency

`FourLegEvaluateLoop.step` (`book_evaluate_loop.py:29–48`) never calls
`FourLegRuntime.advance_schedule`. Tests that call that method manually prove
the operation, not its delivery without incoming bars. A named clock driver
must deliver cutoff/flatten/deadline events independently of feed activity and
share the serialized owner. S2 RC-8 requires failure at the deadline to remain
a path failure, not a dropped observation.

## Independent acceptance vectors for G1–G5

| Vector / clause | Concrete fixture or mutation | Required observation |
|---|---|---|
| CLOCK-1 / S2 RC-3, RC-9 | Source order A, A, B with B chronologically earlier | Unique increasing path times/occurrence IDs; unchanged source date/TOD; second A retained; calendar/Pine use source clock, barrier/equity use path clock |
| CLOCK-2 / S2 RC-3, P1 §§5,9 | Historical source pool, synthetic 500-session path and bounded September permission artifact | Three explicit clock/coverage classes; no deployment-calendar extrapolation or relabeling historical dates as live permission |
| COVER-1 / S2 RC-7 | One leg lacks a union-grid timestamp inside its own active Pine window, while flat | Exclude source session with reason/count; no last-close imputation; test outside-window absence separately |
| COVER-2 / S2 RC-8 | Working order or residual position at own-flat deadline | Path failure/T=infinity; never source exclusion to improve results |
| WARM-1 / accepted Step 3, S2 RC-1/3 | Replace prefixed Aegis input with original unprefixed panel; shorten recursive history | Identity/origin refusal; full-origin evidence never silently authorizes shortened warmup |
| STATE-1 / S2 RC-3 | Reverse/repeated block splice during continuous replay | Preserve adapter indicator/paper state; reset session-specific state by occurrence; no splice of all-normal/all-protected cashflows |
| BLOCK-1 / S2 JointFlatBlocks | Flat positions plus resting ORB add/reservation at edge | Refuse as non-joint-flat; require every leg's position and working-order/uncertain reservation evidence |
| POOL-1 / P1 §§3a,5 | Five usable chronological sessions | H1 contains first three, H2 final two; disjoint union equals full after frozen exclusions |
| POOL-2 / P1 §2 | Same requested depth n for full/H1/H2 | Three independent populations of n; no division of n among pools; speed reuses full trials |
| PARTA-1 / P1 §3a | Repeated six-month outer blocks with final truncation | Exactly original venue-session length under frozen indices; preserve occurrence provenance |
| PARTA-2 / P1 §3a | Two alternate panels with different outer order/seams | Rebuild five-session inner blocks separately against each new panel; validate joint-flat edges in that composition; no original inner index reuse |
| PARTA-3 / P1 §3a | Frozen close-call expansion from first 100 to 200 | Preserve first 100 panel identities/results; reserve expansion domains beforehand; no replacement panels; no Part A in n3 |
| STREAM-1 / P1 §2 | Cross product of stage, population, outer panel and inner path IDs | Deterministic disjoint namespace allocation; n3 untouched by n1/n2/Part A; distinct seed labels alone do not prove isolation |
| INIT-1 / P1 §9 | Pristine E1 without actual account close/B7 | Allowed explicit pristine state; no invented fresh-B7-before-E1 prerequisite |
| INIT-2 / P1 §9, SET | Simulated path close supplied as live settlement, or pristine state labeled B7 | Refuse authority-class substitution; final n3 requires separately authenticated B7 and validity chain |
| G1-ID / P1 §§6,10a | Missing runtime dependency or original Striker substituted | Refuse draft/incomplete/unreviewed identity; pin original admission as evidence, new runtime closure independently |
| G2-ATTEMPT / P1 §4 | Crash after stage begins or lost successful receipt | Durable stage identity/status recovery; no new RNG draw or new attempt inferred from missing response |
| G5-SEAL / P1 §§3a,6 | Missing half, wrong stream, omitted Part A panel or partial result | No result seal; exact expected stage/population/panel set and digests required |
| CLAIM-1 / P1 §10a, SET | Passing synthetic/component tests attached as actual close evidence | No promotion; source qualification remains independently blocked |

`500`, Part A indexing/percentile/truncation details and depth remain proposal
fields until their owning freeze decisions. These vectors constrain honest
construction; they do not ratify unspecified policies. If calendar/source/path
composition cannot meet S2 RC-3/7/8 and P1 §§3a/5/9, identify the exact missing
mapping/coverage authority for the coordinator before freeze. Do not invent it.

## Checks and limitations

At d107ebd plus this test file, Python 3.13, with plugin autoload and bytecode
writes disabled, ran:

```text
py -3.13 -m pytest tests/ops/test_phase3_provenance_acceptance.py -q -p no:cacheprovider
```

Result: **3 failed assertions in 0.63 seconds**, reproducing I1's three cases.
The local test-only pygments dependency came from the preserved Phase 1 test
directory through `PYTHONPATH`. Tests contain synthetic source only. No private
panel replay, qualification draw, output statistic or actual account submission
ran. Owner fixes and ready G1–G5 interfaces will receive targeted follow-up review.

Independent reviewer `/root/step6_review` accepted this documentation/test-only
contribution for a local review-evidence commit, explicitly retaining the red
baseline. That review confirms the three synthetic reproductions and bounded
identity claims; it does not certify the future G1–G5 implementation.

Three actual source blockers remain unchanged: CSV/query timezone/endpoints,
September 14 boundary equity or contemporaneous flatness, and close correction/
acceptance status. They remain at their consuming gates, without substituting a
manufactured close, skipping a predecessor or resetting the chain.

## Synthetic model follow-up

Added 21 independent model cases covering complete four-leg gross edge proofs,
position/order/reservation flatness, source-date and schedule binding, immutable
path/diagnostic collections, and non-pass outcomes with no finite pass time.
At model SHA256
`3b4a51723dee0c18461c0f958e0963ac6e91ac9f4b5cc798dcee0db6a4b6d916`,
19 passed and two failed: `PathSession` accepted a mutable bar list and
`PathOutcome` accepted mutable inner diagnostic pairs. Both permit changes after
validation. The Phase 3 owner repaired collection validation.

Fresh independent rerun against the owner's uncommitted successor model SHA256
`f056360bcde1fb8a2599992d0aa9ab7ed6d51a72619639e23d0a788569447af6`:
**21 passed, 3 deselected in 0.22 seconds**. This selected the model cases and
excluded the three separately owned loader regressions. The invocation used
`-c NUL --confcutdir=<independent-worktree>/tests/ops` and explicit owner
`ops`, `ops/c1_rail`, and `core` import roots to test the successor rather than
the independent worktree's baseline. This is a bounded model verdict, not
integrated replay or G1–G5 acceptance.

Intra-bar acceptance remains separate: an M15 bar spanning an exact flatten
boundary cannot contribute post-boundary extrema before that boundary. The
replay must consume sufficient evidence-bound execution chronology or report
`NEEDS_CONTEXT`. Synthetic OHLC subdivisions, even if aggregate-consistent,
are not source provenance or proof of intra-segment ordering. Preserve the
15-minute signal cadence and account for pending-order lifetime, costs and
fills exactly once. No historical fill model or new data source is accepted
by these tests.

### Loader successor

The three I1 regressions were independently rerun against the Phase 2 owner's
uncommitted `phase3-qualification-control` successor, with explicit imports
from that worktree. `book_adapters.py` SHA256:
`2299a1aa19c0b4c8aa947dafe01cf78e2bbc449edf55484c4ef218356b8b5fa4`.
Result: **3 passed, 21 model cases deselected in 0.15 seconds**. This closes
the three reproduced byte-loading defects at this file identity only. The
runtime settings binding, local-refusal feedback, schedule driver and full
transitive runtime acceptance remain separately owned integration obligations.

## Controller checkpoint 1465c36: G5 blocked

Independent synthetic authentication probes reproduced four assertion failures
against checkpoint `1465c36`: after normal result validation and a valid test
Ed25519 producer signature, replacing the receipt's verdict, completion,
canonical envelope bytes, or Part A stage digest still passed
`authenticate_result`. The original envelope digest/signature remained unchanged.
No crypto verifier was mocked. The independent cases use the owner's normal
synthetic validation fixture, then mutate the returned receipt.

`authenticate_result` checks the signature's claimed digest without rebuilding
the receipt fields from those signed bytes. `_reauthenticate` repeats this
operation, comparing the altered object with itself; journal claims consume its
verdict and seal payloads consume its stage digests. A frozen dataclass does not
establish the required correspondence. G5 is blocked until authentication and
consuming boundaries rebind every derived field to the canonical signed envelope.
The owner and coordinator received the reproduction; production files are outside
this review lane.

Completed checks, using explicit target import roots and the independent test
file with `-c NUL` and plugin/bytecode writes disabled:

- `-k test_result_authentication`: **4 failed, 24 deselected in 1.49 seconds**.
- `-k boundary`: **8 passed, 28 deselected in 1.72 seconds**. These compare each
  FULL/H1/H2 confirmation failure cutoff and its adjacent failing count against
  an independent exact-rational binomial oracle. Speed cases check its exact
  success threshold and one below, day 200 inclusion versus day 201, with a
  failed account attempt retained in the full denominator. Completed unresolved
  attempts count as failures; statistical stage PASS does not require every
  path to pass.

Independent review caught an initially nondiscriminating speed denominator
fixture: dropping one failure from 100 paths leaves the same integer cutoff.
The final fixture uses 101 paths and asserts that dropping its failed attempt
changes the exact cutoff by one. The fresh result above verifies that strengthened
test; the earlier eight-pass run does not establish denominator protection.

The tested seal/fixture and adjudication/calculator files had no diff from
`1465c36` before their respective runs. A first sandboxed authentication launch
failed to import the local test dependency and is not test evidence; the completed
run above used the readable dependency environment. No qualification paths,
account evidence submissions, actual signing authority or outcome draws ran.

### Authentication repair verified at b8f929d

The owner repaired the receipt boundary with verifier-issued provenance,
canonical-envelope digest/field reconstruction, output revalidation and durable
journal binding. Independently reran the original four mutation tests unchanged:
**4 passed, 32 deselected in 1.59 seconds**.

Added eight consuming-boundary cases: valid signed synthetic results first pass
normal validation, authentication and journal commit; unchanged journal-claim and
final-seal calls succeed. Each case then changes one field on the original
receipt object and requires a canonical/receipt mismatch rejection. This tests
the field comparison rather than only rejection of a replacement object. Verdict,
completion, canonical bytes and Part A stage digest are covered at both consumers.
Result: **8 passed, 36 deselected in 3.33 seconds**. Test signatures and output
journals are synthetic; no actual qualification authority was used.

Seal, journal and fixture files had no diff from `b8f929d` after the runs. The
reported G5 receipt-authentication defect is closed at this checkpoint. This does
not accept the still-pending complete TEST_ONLY factory/controller route, source
qualification, historical intrabar evidence, Phase 1 or F1 authorization.
