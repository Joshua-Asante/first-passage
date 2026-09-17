# Qualification tooling review record


> Current engineering status: see the 2026-09-16 post-413 update at the end of this document; the original dated material below is historical.

Status: **paused by user scope change**; see [paused-checkpoint.md](paused-checkpoint.md)
for the latest tested revision and unfinished integration. The entries below are
bounded historical review checkpoints; combined G1–G5 review remains pending.
This record grants no F1, source parity, qualification or deployment authority.

## Current integration checkpoint

Source factory/loader checkpoint `8e5c6ec` passed independent bounded review:
43 source, loader and controller tests. The full qualification test directory
passed 240 tests in 20.88 seconds on CPython 3.13.2 before integration of Phase1's
new G5 security regressions. Source generation/date/exclusion accounting,
malformed fact references, exact risk precision and observed-union coverage were
reviewed; private native-port arbitrary-start parity was not claimed.

The runtime collector separately passed 19 tests and independent provenance
review at implementation SHA256
`7c149e4b8c738edf49b99435ec6e5aba806bd978ca3f0dc802f23db7edc35e1f`.
Ordinary imported code resolves under the repository and the four retained ports
under the private artifact root. Four port roles are mandatory even for `.bin`
paths. Module origin, canonical name, aliases, retained source bytes and declared
first-party dependencies are checked. This is source provenance, **not captured
execution authority**; generic mandatory code-role classification and the
executing consumer's code binding remain separate requirements.

Phase1 review commit `f92401f` was integrated unchanged as `d7c2f4c`. It includes
four independently reproduced G5 authentication mutations and eight exact
rational statistical boundary vectors. The authentication cases failed at
`1465c36`. Repair `2e28b5a` plus controller reconciliation `b8f929d` passed all
four unchanged regressions and eight additional same-issued-object claim/seal
mutations independently; follow-up evidence `51db916` is integrated as `9864f65`.
This is bounded defect closure. Final combined review must exercise the
segregated TEST_ONLY full composition and runtime execution binding without
weakening production authority.

Repeated synthetic path and Part A measurements are recorded in
[representative-workloads.md](representative-workloads.md); final budget acceptance
remains pending composition/security acceptance and actual workload bindings.

## Independent findings and resolution

Reviewer `/root/preparation_review` inspected the full new model/panel/session/block/path/regime/replay boundary and reproduced issues independently. Fixes include separate RNG purposes, explicit outer-range adjacency through its exclusive endpoint, deeply immutable nested records, emulator-effective tick-rounded and activated order timing, exit slippage in cross-leg adverse marks, preserved deadline excursions, native per-leg action batches and controller cancellation without extra strategy close calculations.

The reviewer accepted the first repaired scope after 68 focused synthetic tests and independent vectors. It then reviewed deterministic partial-fill accounting: a partial Aegis fill retains both confirmed capacity and unfilled reservation; terminal cancel/reject releases only the remainder; Striker adds use accumulated confirmed base; residual exits preserve brackets. Final review accepted the extension and counter-only optimization at replay SHA-256 `6a2af4e9cda30ced6c77eb0f948dfaf550b538cdde81fe5f8c7abb5c9e83e997`, after 48 focused replay/adjudication/benchmark tests and independent delayed-fill, terminal-rejection and multi-session deadline-counter cases. No residual bounded findings remain.

Phase1 independently authored and reviewed 24 provenance cases: three loader regressions and 21 model vectors. Its commits 6a8b5a0 and 1c5b54a were integrated as 2c595c2 and b919afb. Phase2's runtime precursor 72e3242 was integrated as 4abc30a. Historical admission is unchanged; new runtime and scheduler identities need their own affected acceptance.

Integrator verification checkpoint: 128 tests passed in 1.88 seconds across new qualification modules, Phase1 provenance tests, atomic loader tests and shared schedule tests. This checkpoint precedes final G1/G2/G5 integration. Markdown links passed (9 files, 17 targets); dependency boundaries passed after moving the preparation calculator from documentation into the ops package.

## Subsequent provider and native-order review

The shared three-instant schedule classifier was integrated as `9a1a91c`. Replay and source-clock classification now call that shared law. With explicit Phase2 ownership authorization, the native emulator ignores exit/flat orders whose scope has no confirmed lot at registration time. This preserves same-batch entry/exit ordering and prevents a queued empty exit from closing a future unrelated entry. Replay does not prefilter these actions using an earlier position snapshot.

The independent reviewer found two provider defects: source-proof deadline failures escaped as trial failures, and sampled deadline failures bypassed occurrence identity checks. The provider now reports failed prerequisite proofs as `NeedsContext` and validates the exact designated terminal prefix before propagating a trial deadline failure. Four new regressions failed before the correction; all six provider tests passed afterward.

Independent re-review accepted this bounded extension with 77 tests (provider6, clock2, replay51, native18) plus two independent native-order vectors. Reviewed source SHA-256: provider `c8a3d8083de3ba85752da4f5dc1866c8538e4227fe86fb555b4fe4959e2943b0`; replay `b07e268db6cb776bfa3618e95559e80ee2495d773ed1de08ea51756d52f0e8ce`; native emulator `72bfca1aab2e3cd34065e22a66cc25d23d48f00b13bcc51f38be85367a0c03de`. Evolving result adjudication was excluded. Integrator verification passed139 qualification/native/schedule tests, including seven preliminary result-adjudication tests; this is not combined G1–G5 acceptance.

## Result-adjudication adapter review

Independent review accepted `result_adjudication.py` with ten tests and two extra retained-prefix expansion vectors. The adapter separates n2 FULL from its Part B half-population aliases, permits certified nonzero failure counts, recomputes Part A from every retained inner outcome, and refuses later stages after a failed n1 or joint n2/Part B decision. `FrozenAdjudicator` binds the complete G1 runtime role/hash map and checks its own retained source identity. G1 owns inventory completeness and module-load provenance; G5 must require the exact dispatcher type and validated contract, verify seed/outcome/durable-input bindings, and invoke `verify_for` before accepting it.

Reviewed implementation SHA-256 `dd4b99d30658031be73014cdfcace0ff24e13eff8f45fe894c38ef3227f88507`; tests `9195d52cfb52708f5ede429396d0f4c81bf6933f37c476ffff2c6cbcea89ba3e`. Combined controller acceptance remains pending.

## Counter optimization measurement

Synthetic fixture: seed791946221, 500 sessions, 46,000 path bars, 184,000 adapter bars, all four invented strategy adapters, repeated/reversed source sessions, policy transitions, cap/takeover, venue costs, scheduled flatten, kernel evaluation and serialized replay result. One process, CPython3.12.14. No source panels, private ports or account state were loaded.

The replay replaced cumulative rescans of every historical fill and previous session with a confirmed-fill counter and per-session delta, including the deadline-failure prefix. Before: 6.7728947 seconds, replay source SHA-256 `543d110ee65a6b635081b483001129a98b7926bdba96f407500ff769450da783`. After: 6.5857556 seconds, SHA-256 `6a2af4e9cda30ced6c77eb0f948dfaf550b538cdde81fe5f8c7abb5c9e83e997`.

Both runs produced exactly the same serialized replay digest `58e25c639cdf026bd23da64f7d70274d0872015c936c6434d23b00b10132fee1`, 5,012 fills, 54,022 events and 7,185,415 serialized bytes. All 45 replay tests passed after the change. A single pair observed about 2.8% lower time; it is not a robust speedup estimate or an E1 budget. Full controller/PartA overhead and final repeated integrated measurements are still owed.
## 2026-09-16 post-413 engineering update

Tasks 1-4 of the post-413 integration handoff are accepted for synthetic engineering only. Earlier text in this dated document remains historical. See [post-413 integration acceptance](../2026-09-16/post413-integration-acceptance.md) for the selective integration inventory, actual commands/interpreters, exact base and dirty-tree evidence, failures and repairs, complete signed source-to-seal route, rejection/restart coverage and independent whole-flow review.

Direct checks passed 6 signed composition cases, 350 qualification cases and 44 independent provenance cases. Final operations passed 2,841 parent tests with 15 private-input skips, plus all 394 qualification/provenance child cases without skips. Repository gates passed with disclosed host-capability/private-artifact limits; 23 focused Linux image checks passed. All accepted records completed with stable source, complete capture and verification exit zero. PR409 behavior and PR413 launcher/recorder remain preserved. Windows operations used the checkout's validated Python 3.13.2 interpreter; Linux image tests used the recorded Python 3.11.16 environment. Tested HEAD is b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac with the integrated dirty tree.

This does not accept private source/settings/schedule inputs or authorize F1, exact-depth approval, production E1/n3, D0, ORB GO, B7, deployment or arming. Representative compute preparation and remaining operator decisions stay at their later gates. Historical bare-Python recipes above are not operative: use this checkout's validated fp.ps1 launcher for operations work. Work remains an uncommitted local integration; no publication or deployment occurred.
