# Handoff — Parallel Phase 1: input acceptance

## Assignment

Own Phase 1 completion for the fixed Tradeify portfolio: qualify actual account evidence, connect authenticated settlement to its real listener consumer, finish Step 6 shared-sizing/finite-margin parity, and obtain combined admission of the seven strategy bundles. Include the bounded calendar prerequisite wherever these consumers need it.

Work alongside the runtime session. Deliver an independently reviewable Phase 1 packet and an explicit interface handoff to the runtime integration owner. Continue independent work when a particular evidence item is blocked. This handoff is a draft for the receiving session; no session was started or message sent by preparing it.

## First actions and baseline

1. Read applicable repository instructions and verify current main, open changes and active writers before choosing the execution base. Use an isolated `codex/` worktree; do not reset or implement in the primary checkout.
2. Inspect the existing Packet 1 worktree before redoing anything: `C:/Users/joshu/multi_firm_operations/.worktrees/tradeify-attended-release`. At handoff preparation it was on `codex/tradeify-packet1-startup-coverage`, commit `1cdfafe`. This is a discovery anchor, not a claim of current remote state or a grant to take over that checkout.
3. Locate the concurrent runtime owner and agree shared-file ownership, exact base revisions and the settlement-consumer contract. Existing discovery anchors include `.worktrees/stage2-runtime-owner` and `.worktrees/tradeify-runtime-resume`; do not assume either is idle or authoritative from its name.
4. Record a short starting ledger: already accepted, remaining implementation, missing actual evidence, shared dependencies. Reuse recorded approvals; ask only for genuinely missing facts or decisions.

The primary checkout was `133f043` at preparation and contains untracked plans. Newer Packet 1 records live in the worktree above. Read the following paths there or in their verified merged successors:

- `docs/superpowers/plans/2026-09-14-tradeify-attended-release.md`, especially **Packet 1 completion sequence — 2026-09-15**.
- `docs/spec/2026-09-15-tradeify-attended-settlement-contract.md` — operator-approved design; read in full, including authenticated submission, historical catch-up and durable acceptance.
- `docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md` and accepted TB-S1/session/calendar contracts.
- `docs/notes/2026-09-15-packet1-producer-feasibility.md`.
- `docs/notes/2026-09-15-calendar-account-contract-resolution.md`.
- `docs/notes/2026-09-15-calendar-parity-separation-amendment.md`.
- `docs/notes/2026-09-15-packet1-step3-acceptance.md` and `2026-09-15-packet1-execution-domain.md`.
- `docs/briefs/handoffs/2026-09-14-seven-bundle-runtime-interface-plan.md` and the current Track B umbrella.

The phase summary is at `C:/Users/joshu/multi_firm_operations/docs/superpowers/plans/2026-09-15-deployment-phase-breakdown.md`. Specific approved contracts govern over its shorthand. In particular, its generic “peak reconstruction” language must not be interpreted as permission to reconstruct the initial peak from statements.

## Preserve completed work

The inspected Packet 1 record states:

- Producer route/design feasibility is complete; actual account producer acceptance remains separate.
- Step 2 ORB reconciliation is complete; all seven reconciliation records PASS.
- Step 3 startup/provider coverage is independently accepted: nine reference replays, 3,632 matched trades, zero exclusions and resolved terminal state. These are recorded results, not tests rerun for this handoff.
- Step 6 must use the reviewed candidate runtime/input identities. Preserve original private ports and exports, corrected O-N provenance, and separately recorded later volume revisions.
- The listed next steps are Step 4 calendar, Step 5 settlement and Step 6 combined admission. Verify newer progress before treating any of these as wholly unimplemented.

Do not repeat the completed export collection or reopen accepted source changes without a concrete regression. Matching reference trades is not final shared-law or bundle admission.

## Work package A — Qualify real account evidence

- Establish actual account identity and inception, report query completeness, displayed timezone, raw/normalized timestamps, account-session mapping and historical closing-equity capability.
- Preserve effective-close, publication when supplied, capture, signing and receipt times separately. Never infer close time from file creation or receipt time.
- Initial B7 peak comes from the Tradeify dashboard threshold and kernel width under D23. Subsequent peaks follow the approved EOD ratchet. Statements do not supply the initial peak.
- Historical balance can stand for close equity only with evidence of flatness at that same boundary. A later flat snapshot does not establish it. Carried or uncertain positions require venue-backed close equity and valuation evidence.
- Qualify complete account-wide cash history with bounded overlapping queries, retained empty-query evidence and correction/revision detection. Do not infer inactivity from missing rows or instrument-filtered results.
- Apply the approved transaction-linked cost classification once; unknown fees and external adjustments remain blocking. Reconcile using decimal currency arithmetic without treating arithmetic agreement as proof of completeness.
- Produce a fact-to-source matrix identifying each verified fact, consumer, retained evidence digest and exact missing fact. Request only the deficient report/range/timezone/attestation if existing evidence cannot resolve it.

**Acceptance:** the actual account can satisfy the approved evidence protocol, or each unsupported fact is explicitly blocked. Synthetic records and report access alone cannot close this package.

## Work package B — Calendar and settlement through the listener

### Calendar prerequisite

Verify whether Step 4 has since landed; extend/reuse accepted work. Preserve D19 as historical date membership and separate typed policy overlays. Implement the approved bounded September 3–30, 2026 forward permission artifact, allowing qualified ordinary sessions and denying holiday, shortened and uncertain adjacent sessions. Bind product/account boundaries, deadlines and preceding account sessions across denied days. Missing or expired coverage refuses new risk without losing outstanding protective/recovery obligations.

Read current official evidence when qualifying calendar facts. Do not revive the superseded universal historical archive prerequisite for provider-data coverage or invent bars/closures to fill provider gaps.

### End-to-end settlement contract

Trace retained account evidence -> authenticated submission -> verifier -> durable accepted-close chain -> `SettledClose` -> trusted account context -> listener sizing consumer.

- Reuse the approved signing/challenge protocol and historical `record_only` scope. Preserve its freshness, one-use, account, boot/generation, predecessor and digest bindings; do not design substitute authentication.
- Validate source contents before constructing trusted state. `book_sizing_context.py` compares bound records/digests; it does not verify signatures, persist settlements or authorize dispatch.
- Persist settlement identity/order coherently so a restart cannot accept replayed, conflicting or regressive records. Keep simulated replay closes distinctly labeled and ineligible as live evidence.
- Exercise valid, missing, stale, wrong-account/session, incomplete, tampered, duplicate, conflicting-revision and out-of-order inputs through the actual consumer. Include restart and historical catch-up behavior under the full approved contract.
- Demonstrate that accepted settlement does not itself resume, arm, replay missed signals or alter an already-active session's mode.

**Ownership:** Phase 1 owns evidence qualification, accepted producer/verifier and settlement tests. The runtime session owns general account serialization, broker dispatch and execution recovery. Agree one writer for listener/account-owner files. If the runtime owner implements the final hook, Phase 1 supplies the concrete contract, fixtures and rejection cases and retains joint acceptance of the complete path. A producer-only patch cannot close Phase 1.

**Acceptance:** verified calendar/session and accepted settlement reach the real listener sizing path, with durable rejection/restart evidence and no new dispatch authority.

## Work package C — Step 6 and combined bundle admission

Read production shared policy/sizing/capacity code first under Rule 0. Use the reviewed candidate generation and existing `entry_quantities`, `add_quantity`, `size_book_request` and accepted feedback interfaces; do not implement a second sizing law.

1. Assemble candidate evidence binding each actual panel, source/settings/properties, startup, provider coverage and runtime identity.
2. Complete panel/runtime-bound shared-law checks across the required quantity/mode/lifecycle domain, including confirmed-base add sizing and zero/refusal behavior.
3. Complete the required finite-margin evidence over the declared acceptance domain; matching CSV trades alone does not prove unsupported margin-call paths unreachable.
4. Obtain independent review of the complete candidate evidence before issuing the admission contract.
5. Execute all seven admitted bundles through `run_bundle_parity` at quantity scale 1, with no excluded trades, retained finite-margin checks and resolved final state.
6. Run relevant regressions and the current repository-required gates on the exact candidate revision. Record private evidence separately from public verdict/digest records.

**Acceptance:** seven formally admitted PASS bundles, accepted calendar and settlement interface, and final combined Packet 1 review. Partial diagnostics, skipped private tests or a merged component do not substitute for this gate.

## Parallel-work boundaries

- Before any shared-file change, coordinate ownership with the runtime session. Prefer bounded commits and an explicit integration base; do not edit another session's worktree or overwrite its changes.
- Publish interface changes promptly: actual type/signature, producer, verifier, durable owner, accepted/rejected inputs and revision. Resolve conflicts through the integration owner rather than creating a parallel account-state authority.
- Keep original/private artifacts in approved ignored primary roots; verify ignored status before writing. An isolated worktree may not contain those inputs. Public records carry only permitted digests/verdicts.
- This assignment does not include F1/E1/n3 runs, policy-registry admission, funding/provider selection, live trades, deployment or activation. Preserve separate operator gates and existing merge authority.
- A missing external fact blocks its dependent acceptance, not unrelated Phase 1 work. Present the specific evidence gap and concrete completed packet rather than asking for blanket permission to continue.

## Return packet

Return one concise coordinator handoff containing:

1. Exact base/head, branch, commit/PR locations and changed-file ownership.
2. An acceptance table for account evidence, calendar, settlement-to-listener, shared-law/finite-margin and seven-bundle admission, each marked accepted or blocked with evidence.
3. Commands actually run, results, private-input availability and review disposition; distinguish inherited evidence from fresh verification.
4. The exact runtime consumer contract and any integration commit still required, naming its owner.
5. Only remaining operator inputs, stated precisely, plus any unresolved contract conflict.
6. A truthful final verdict: **Phase 1 accepted** only when all packages and combined review pass; otherwise name each outstanding condition.

Start with the baseline/ownership check and actual account-evidence inventory. Continue from accepted Step 3; close Steps 4–6 using the current implementation state.
