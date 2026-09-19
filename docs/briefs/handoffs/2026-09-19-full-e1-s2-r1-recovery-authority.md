# S2-R1 — Interrupted recovery must block positive authority

> Execute with superpowers:executing-plans. This is one repair within the existing Protected Full E1 roadmap; combined acceptance remains with the coordinator.

**Selected outcome:** A durable recovery claim blocks every new positive authority action until a trusted, durably completed recovery resolves it. Crash/reopen cannot bypass that block, reuse a spent controller slot, erase uncertainty or gain an uncharged continuation.

**Prerequisites:** Frozen S2 candidate is INCOMPLETE / NOT ACCEPTED. Read recovery/full-e1-s2-20260919/README.md, the governing S2 handoff, and candidate spec/plan. Accepted S1 remains 430fc72186a0e642c8811be17d459fd87cbf7533. Candidate source.zip SHA256 a6129041940bcb8749c5a0a9a7d72e11ca1323b45f9331faf3d44ff498917c91; manifest SHA256 8631c315093f20fcc412dad950873eca250ebe03a915632d1303ec9b37ed7ec9. Coordinator verified all 316 SHA256SUMS entries. Existing isolated checkout is C:/Users/joshu/.codex/worktrees/full-e1-s2-supervision/multi_firm_operations; verify relevant source bytes against the frozen packet before changes. Preserve that packet.

**Ownership:** Existing S2 executor owns the repair and all affected consumers. Coordinate protected E1 execution owns repair acceptance and combined S2/E1 acceptance. No parallel writers.

**Verification:** Run the checkout's fp.ps1 doctor first. Retain the interrupted-claim reproduction as a failing regression before repair. Run focused supervision/recovery/budget tests through fp.ps1 python -m pytest, affected snapshot/model/service tests, the original seven-file selection, fp.ps1 check and git diff --check. Record exact commands, interpreter, source identities and actual results. The frozen final check failed on STATE.md's 2026-09-18 deadline; disclose this and do not change policy/status deadlines just to pass. Linux proof remains pending.

**Checkpoint:** Before coding, report a compact producer/state/consumer trace identifying the durable pending/completion representation, transaction boundaries, all positive-authority gates, and how any continuation is reserved and charged. Routine choices within this outcome are authorized. Return a concrete conflict if safe continuation requires solving a separate bootstrap accounting blocker.

**Return boundary:** Return a new checksummed repair packet after source-bound verification or a concrete interface conflict. This does not accept S2 or authorize S3, Linux activation, publication, commits, pushes, deployment or paid provisioning. Do not repair the other three S2 blockers in this handoff.

## Actual defect and behavior contract

In ops/c1_rail/qualification/execution/campaign_store.py, claim_supervision_control stores a one-use object transactionally but does not put recovery in the authority contract. In campaign_supervisor.py, recover_campaign_work claims RECOVERY_OWNER before entering active recovery. A crash in between leaves BOUND VALID; the retained interrupted-claim-result.json confirms reserve_work succeeds after reopen. An in-memory recovery_issues flag cannot close this gap.

Use the existing ExecutionStore transaction/authority owner. Claim and pending authority state must become durable together before active observation. Positive operations must consult this state in their own serialized authority decision, including reserve/dispatch, candidate acceptance, diagnostic receipt and future result/seal interfaces already present. Historical reads and negative/VOID actions must remain available. Preserve immutable settlement, fresh independent recovery observations, sticky uncertainty and fixed-intent token semantics. Do not turn a successful routine recovery into unconditional terminal failure merely to hide missing completion semantics.

A trusted completion may clear only its own pending barrier after required facts are durably recorded. It cannot clear VOID, BUDGET_UNCERTAIN, overrun or other terminal facts. A crash leaves the barrier effective after reopen. The spent controller slot remains spent. Any active continuation requires a distinct, already-funded bounded operation under the original allowance; insufficient resources leave authority blocked. If that continuation cannot be provided inside this repair, retain a safe blocked state and report the remaining liveness limitation explicitly rather than inventing a retry or new allowance.

## Bounded implementation and acceptance sequence

- [ ] Convert the retained reproduction into a regression: captured/settled work, durable RECOVERY_OWNER claim, simulated death before observation, reopen store, attempt a new reservation; assert rejection with the durable recovery barrier.
- [ ] Trace and implement the canonical pending/completed recovery representation and serialized authority gates in campaign_store.py and campaign_supervisor.py. Update campaign_budget.py, qualification/journal_snapshot.py, service.py and lifecycle model only where this shared contract requires it; preserve historical schemas through explicit versioning where necessary.
- [ ] Test two competing claimants, crash before claim commit, crash after claim commit, crash after observations before completion, and crash after completion. No duplicate owner, charge refund or authority window may result.
- [ ] Test successful complete recovery, unknown termination/counters, existing terminal uncertainty, both VOID orderings, exact historical retries, insufficient continuation allowance and a spent slot after restart. Enumerate each existing positive authority entry point and exercise its pending-state rejection; retain old-version readability and fixed-intent tests.
- [ ] Run final source-bound checks, update the candidate ledger and return a separate packet with changed interfaces, exact hashes, limitations and evidence. Keep scheduler-before-reservation, VOID authentication accounting, pre-timer deadline/bootstrap coverage and missing Linux proof open.
