# Aegis disconnected decision experiment proposal

**Status:** PROPOSED - docs-only review; no experiment has been run.

**Date:** 2026-10-12. **Decision owner:** Joshua. **Acceptance owner:** the existing Deployment Coordinator.

**Companion:** [Conditional native-runtime proposal](../../notes/2026-10-12-native-ninjatrader-runtime-PROPOSAL.md).

**Disposition:** retain for the next native-runtime decision; implementation and installed-platform work require separate grants.

The proposed experiment asks whether one bounded Aegis decision/state slice can be translated from the accepted Python port to platform-neutral C# with equivalent observable results on a frozen synthetic corpus. Two disconnected batch runners consume the same immutable event tape and emit inert trace files. A separate comparator evaluates them. Neither runner drives the other, connects to NinjaTrader or has an order gateway.

**Smallest next step:** a read-only dependency and existing-toolchain assessment. This PR does not authorize reference execution, fixture generation, a C# translation, compilation or platform tests.

## Source and authority boundary

Reviewed public dependencies are pinned to `0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1`; publication was refreshed onto main `158bf2a871540bb8cd78353c2996662ce216cdd9` (#806), whose only changes curate STATE and its archive. Public [source identities][manifest], [BookStrategy protocol][protocol], [indicator arithmetic][ta], [adapter contract][adapters] and [sizing law][policy] identify the relevant contracts. The companion proposal reconciles current portfolio, personal-lane and safety decisions; those owners retain authority.

The coordinating agent independently verified an authenticated Tradeify support reply dated **2026-10-12 20:19 UTC**. It names NinjaTrader/NinjaScript for in-platform strategy logic, calculations and signal generation and prohibits external Python-generated signals for evaluation/sim-funded accounts, including Add-On/SDK and direct API routes. The [proposal's support boundary](../../notes/2026-10-12-native-ninjatrader-runtime-PROPOSAL.md#1--context-and-support-boundary) records the remaining questions about offline preparation, the particular static artifact and data rights. This attributed summary supplies no implementation approval.

The accepted private Aegis source and effective settings must be read in place under their existing access rules. Their exact private references belong in the future private handoff, not this public document. The public manifest supplies already-public source pins. No private source copy is permitted by this plan; a later authorized C# translation would itself remain private. Synthetic prices do not make strategy-derived fixtures or traces public.

Existing personal-account Python owners continue their work. This experiment introduces no gate for that lane and does not reopen frozen survival, feed-equivalence or retained-vector requirements.

## Claim, verdicts and smallest slice

**Claim C1:** for a frozen source/settings identity and admitted synthetic corpus, the independent implementations produce the same ordered actions, eligibility/refusal decisions, sizing results and agreed state transitions. C1 is a finite-corpus portability claim, not equivalence over all possible inputs.

| Verdict | Meaning |
|---|---|
| PASS-C1 | Every mandatory case satisfies the reviewed comparison policy, coverage and reproducibility obligations; an independent reviewer accepts the capability/evidence audit |
| FAIL-C1 | An unexplained semantic mismatch occurs on an admitted case |
| BLOCKED | Permission, source dependency, oracle, required coverage, existing toolchain or credible order-isolation evidence is missing |

An unexercised case cannot pass. A reachable order capability invalidates the experiment regardless of signal agreement. A reachable prohibited network or runtime process-launch path fails the proposed capability criterion. Changing expected output, source/settings identity, generator or comparison policy after comparison begins invalidates that batch; retain the evidence and obtain a newly reviewed batch. A demonstrated C# translation defect can be corrected and rerun against the unchanged frozen corpus, retaining the failed revision.

The smallest slice is one Aegis instance: flat start, completed-bar warm-up, entry eligibility, entry intent, explicit simulated full-fill feedback, protective bracket-amend decision if the selected lifecycle exercises it, simulated exit/full-close feedback and return to flat. Include rejected-entry feedback and size-zero/OFF refusal. Preserve the source's real guards and timing; do not inject state or invent an entry rule to obtain a trade.

This scope excludes an autonomous fill engine, partial-fill execution qualification, real account ledger, four-leg allocator, live durable recovery, takeover, performance scoring and optimization. If the required lifecycle cannot be reached within the bounded synthetic corpus, return BLOCKED or seek an explicit narrower claim before running it. Do not silently drop coverage.

## Dependencies and proposed interfaces

The reference runner would use the accepted Python port plus a minimal audited adapter implementing the existing protocol: `on_bar`, `on_execution`, `set_mode` and `checkpoint`. The owner supplies the exact effective-settings identity under the existing loader contract. No unverified defaults or alternative settings generation may substitute.

The assessment must inventory actual transitive imports before any reference import executes. Do not import the production daemon, execution rail, account owner or a loader that activates all four strategies. If the unchanged reference cannot be isolated without production edits or execution dependencies, return the precise conflict.

| Boundary | Producer to consumer | Closed proposed contract |
|---|---|---|
| Manifest | Reviewed packet to both runners | Source/settings/code/toolchain identities; synthetic profile ID; fixture, feedback and time-map hashes; comparison policy; corpus budget; coverage obligations |
| Event tape | Frozen generator to both runners | Sequence ID, explicit UTC instant and event kind. Bar: interval-open time, OHLC integer ticks and integer volume. Mode: explicit mode. Feedback: protocol-shaped fill/reject/cancel, deterministic IDs, quantity, tick price and decimal commission |
| Trace | Each runner to comparator | Event ID; ordered action DTOs with kind/side/timing/scope/IDs, quantity and tick stop/target; guard/eligibility/refusal codes; warm-up, mode and position state; agreed per-event projection and final digest |
| Verdict | Comparator to owner/reviewer | First differing event/field, mismatch counts, coverage, capability evidence and source-bound PASS/FAIL/BLOCKED |

Action DTOs are inert local records. There is no dispatcher, broker client or merely disabled execution implementation.

Today's `checkpoint()` must not be presumed complete restart state. Read-only assessment defines the minimum comparison-state projection and whether it can be obtained without changing source behavior. Missing safe introspection is a blocker or a proposed narrower claim; invented expected state is not an oracle.

## Frozen synthetic corpus

The future fixture author freezes generator, cases, explicit feedback and expected outputs before inspecting C# comparison results. Prefer deterministic, hand-described segments: constant prices, rising/falling ramps, pulses and reversals around inspected thresholds. Threshold-derived cases remain private. Use no captured bars, market-data API, TradingView export, account facts or personal-study output.

**Proposed resource budget:** at most 12 named tapes, each at most 4,096 completed bars, and one bounded fixture-construction pass. These limits are not strategy settings. Warm-up follows the inspected dependency closure; if it exceeds the budget, return the conflict for review.

| Mandatory case group | Required evidence |
|---|---|
| Initialization | Constant-price/no-signal behavior, warm-up and first initialized state |
| Filled lifecycle | Eligible entry, predetermined accepted full fill, next-bar state/protection decision, predetermined full exit, flat |
| Rejection | Entry rejected; no phantom position or fill-dependent follow-on action |
| Sizing and lifecycle | Clearly labelled synthetic nonzero/zero/OFF cases; correct refusal and no accepted fill for zero/OFF |
| Arithmetic | Half-tick and adjacent representable values, threshold approaches from each side, seed/window boundaries |
| Time | Session boundary, day rollover and DST; denied holiday/early-close inputs under a miniature rule-derived calendar |
| Invalid tape | Duplicate, backward, missing-slot and corrected-bar inputs rejected by the boundary validator before evaluation; wrapper behavior distinguished from port behavior |
| Determinism | Fresh-process replay gives the same trace; truncation/corruption rejects without partial success |

For the filled lifecycle, establish a valid synthetic sequence against the reference and freeze feedback tied to stable expected intent IDs. Both runners receive that same tape. Feedback generated independently from each runner's outputs could conceal divergence and is forbidden. A missing or mismatched intent ID stops the case at its first divergence.

Keep the four logical leg IDs in profile metadata, but use **SYNTHETIC_ONLY** Aegis sizing profiles. Do not infer, reconstruct or publish retained R0/R1 quantities. Preserve adds-OFF, zero-refusal and OFF-leg invariants. The experiment establishes no retained-vector fidelity.

Fresh replay from the beginning demonstrates deterministic reconstruction only. It does not demonstrate live checkpoint/resume safety, broker/account reconciliation or restart recovery.

## Comparison policy requiring review

Discrete fields compare exactly: OHLC integer ticks, rounded stops/targets, sizes, IDs, enums, action order and time keys. Match the accepted binary64 evaluation order, missing-value rules, indicator seeds and `pine_round`/`tick_round` semantics. Do not substitute C# `Math.Round` or NinjaTrader indicators by convention.

**Proposed experiment criterion, not an adopted deployment gate:** require bit-identical finite binary64 values in an agreed intermediate-state projection for the first batch. The owner and reviewer must decide whether this is the appropriate diagnostic criterion before implementation or comparison. Encode IEEE-754 bits with readable values, tag missing values explicitly and reject nonfinite external inputs. There is no proposed blanket epsilon.

If that criterion is adopted for a batch, an intermediate mismatch stops its parity verdict even when the final action agrees. Diagnose representation versus semantic cause; do not relax tolerances after observing results. Any alternative reviewed policy must specify fields, bounds, justification and how threshold/sign/rounding changes are prevented before a new batch begins. This numerical question does not alter existing deployed or frozen qualification requirements.

Integer/rational sizing follows the existing law and operation order. The explicit synthetic fill/commission tape is an input assumption, not evidence of executable prices, transaction costs or real fills.

Time semantics are also bound before a run:

- Records carry explicit UTC offsets; naive timestamps reject. Completed-bar time denotes interval open; sequence ID breaks equal-time ties.
- Freeze and independently check a finite UTC-to-ET/session-key table covering all fixtures. Check the unchanged Python helpers against that table for every fixture instant.
- The Python port keeps its existing helpers; the C# test dependency uses the frozen lookup table. Compare emitted day/session keys. Neither runner consults wall time or an implicit local timezone.
- If checking the Python helper requires altering the port, report that dependency conflict. This experiment excludes platform/OS timezone verification, which belongs to separately authorized native integration.

## Capability and build isolation

A future implementation grant must identify a private experiment directory isolated from production, public synchronization and uploads. Proposed components are a manifest, fixture generator, reference adapter, C# decision library, C# batch replay executable, comparator and evidence directory. They are planning components; this PR creates none of them.

Allowlist local reads/writes and the read-in-place source/settings exceptions. Keep outputs away from every daemon, watcher and platform configuration consumer. A possible instruction consumer blocks the run. The C# runner cannot start Python or consume a Python live stream; both are independent finite batch processes.

Use existing approved Python and .NET/C# toolchains and standard libraries. Bind interpreter, SDK, compiler, reference assemblies and runtime identities. Use empty package sources and no third-party packages or network restore. No installation/download, NinjaTrader/Tradovate/CrossTrade assembly, plugin, credential, account configuration or inherited production environment belongs in this experiment.

The proposed runtime restrictions are:

- No order gateway, execution interface or broker service.
- No C# reflection/dynamic loading or native interop; Python imports only the fixed audited closure, with no arbitrary discovery, evaluation or executable deserialization.
- No runtime subprocess launch, socket/HTTP use, service discovery or file watching.
- A separately audited harness may launch only the allowlisted local compiler and batch runners.

Capability evidence combines source/transitive-dependency inspection, build-reference/import inventory, compiled call-site/IL inspection, and an existing credential-free execution boundary with explicit read/write and network restrictions. Record process/module/file and denied-network observations where the existing host supports them. Lack of an adequate existing boundary is BLOCKED, not authority to provision infrastructure or change host security.

“No traffic observed” alone is insufficient. The claim is limited to the reviewed binaries, dependencies, inputs and boundary; it is not a universal operating-system or .NET security proof. Build/restore behavior is part of the review.

## Separately authorized stages

### Stage A: read-only dependency and toolchain assessment

**Proposed next grant only.** One named assessor examines the accepted source/settings identity in place, actual imports, selected state/operations, source-derived warm-up needs and existing toolchain/isolation inventory. File inspection and bounded toolchain identity/version commands are allowed by that future grant; strategy imports/execution, generators, builds and tests are excluded.

Return a small assessment packet: dependency closure, proposed state projection, required numeric/time operations, existing toolchain/boundary availability, unresolved blockers and the exact implementation packet that could follow. Record hashes from actual bytes privately where required. Do not copy private source or settings into the public packet. Assessment can report a blocked design without executing it.

### Stage B: disconnected implementation and comparison

A **new implementation grant** is required after Stage A. It must name executor, independent reviewer, private output boundary, exact source/settings references, existing toolchain/isolation identities, reviewed numerical policy, corpus limits and return criteria. Missing fields block execution; the executor cannot choose substitutes.

The proposed work sequence is:

1. Freeze the manifest, comparison projection and capability inventory before executing reference imports.
2. Author the finite synthetic corpus and explicit feedback. Run the approved reference; independently check simple arithmetic and required lifecycle coverage. Freeze generator, inputs and expected outputs before C# tuning.
3. Implement the minimal private C# decision slice and independent replay runner. Verify that known mutants such as a wrong tick tie, skipped feedback, ignored OFF refusal and shifted session boundary are rejected by the comparator.
4. Compare the unchanged corpus. Preserve failed revisions and first differences; fix demonstrated translation defects within scope.
5. Have a fresh reviewer with appropriate private access inspect source fidelity, oracle independence, coverage, comparison semantics, capability and privacy. Reproduce the reviewed corpus only within the execution grant. The author cannot self-certify independent acceptance.
6. Return the revision-bound verdict and unresolved findings to the existing coordinator.

Any need for production edits, new packages, installation, real inputs, broader access, increased corpus budget, relaxed comparison policy or an execution API stops the handoff for a concrete owner decision.

### Stage C: later native integration and execution qualification

| Later stage | Can establish | Does not establish |
|---|---|---|
| Platform-neutral synthetic experiment | Finite-corpus decision/state agreement, deterministic DTO boundaries and bounded absence of order capability | NinjaScript compatibility, native bars/clocks, feed equivalence, retained-vector performance or live recovery |
| Separately authorized installed-NT decision host | Build/API compatibility and callback/normalization behavior on explicitly authorized inputs | Venue fills, partials, account reconciliation, all-leg emergency behavior, licensing or trading permission |
| Separately permitted execution/recovery qualification | The specific account/build/route behaviors actually tested | Approval transferable to other accounts, builds, feeds or policies |

Installed NinjaTrader, fixed `AddDataSeries` topology, historical/realtime callbacks, partial-fill protection, strategy/account reconciliation and all-leg emergency handling remain separate work. The [official multi-series guide](https://static.ninjatrader.com/support/helpGuides/nt8/multi-time_frame__instruments.htm) and [AddDataSeries restrictions](https://static.ninjatrader.com/support/helpGuides/nt8/adddataseries.htm) constrain that design. The companion proposal retains the conflicting official `CloseStrategy` descriptions and requires installed-build verification.

Synthetic signal/state agreement does not replace frozen Q-SFCLEAR-2, feed-equivalence, survival, licensing or execution/recovery evidence.

## Acceptance, evidence and handoff

| Proposed assessment/experiment obligation | Stage | Owner decision or evidence |
|---|---|---|
| Read-in-place scope and exact input identities | A | Coordinator supplies existing access and source authority |
| Existing toolchain and isolated boundary availability | A | Read-only inventory; unresolved capability is BLOCKED |
| State projection and binary64 criterion | A to B | Explicit review before implementation/run |
| Mandatory corpus and oracle freeze | B | Frozen cases, explicit feedback, independent checks |
| Exact discrete and agreed numerical comparison | B | First-difference trace, coverage and comparator mutant evidence |
| Repeatability | B | Same exact artifacts reproduce trace/verdict |
| No reachable order capability | B | Source, dependency, build and boundary audit |
| Independent acceptance | B | Reviewer findings and coordinator's narrow verdict |
| Native/execution equivalence | Later | Separate grant and evidence; never inferred from C1 |

Evidence remains private: source/settings identities, manifest, toolchain/dependency inventory, fixture/feedback hashes, expected and actual traces, exact code/binary revisions, process exit status, first differences, coverage, mutant results, capability audit and reviewer disposition. Hash actual bytes. Public summaries require a separate privacy review; parameter-derived traces and code stay private.

The coordinator owns integration and acceptance. A future implementation uses one named executor and one fresh reviewer who did not author the implementation or oracle. Report immediately on a blocking dependency or scope conflict; otherwise report after assessment, corpus freeze and final evidence. No existing personal-lane ownership transfers.

Planning effort is uncertain: assessment is a small source/toolchain review; a viable prototype may take several focused working days and could extend to one or two weeks if state projection, exact arithmetic or isolation needs investigation. A source, permission or capability blocker may stop before coding. Native integration and four-leg execution/recovery are substantially larger efforts that should be estimated only after the assessment.

**Recommended next authorization, if Joshua chooses to proceed:**

> Authorize Stage A only: read-only Aegis dependency, state-projection and existing-toolchain/isolation assessment under the existing private-source access rules. Return a bounded implementation packet and blockers to the current Deployment Coordinator. Do not run strategy imports, generators, compilers, tests or platform experiments. Do not copy private inputs, install/download software, alter production or configure credentials.

Stage B requires its own later decision. Publication of this draft is neither that decision nor adoption of the proposed comparison criteria.

[manifest]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/core/strategies/BOOK_SOURCES.sha256
[protocol]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_signal_daemon/book_protocol.py
[adapters]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_signal_daemon/book_adapters.py
[ta]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_signal_daemon/pine_ta.py
[policy]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_rail/book_policy.py
