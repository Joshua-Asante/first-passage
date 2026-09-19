# S2 local candidate and bounded return

Accepted predecessor: `430fc72186a0e642c8811be17d459fd87cbf7533`. Coordinator owns acceptance. This work stops at an INCOMPLETE / NOT ACCEPTED diagnostic candidate; no executable activation, publication or S3.

## Implemented candidate

The installed v3 profile/release uses request v2, budget profile v2, observation v2 and snapshot v3. The canonical phase producer reserves 120 CPU seconds and 300 BOOTTIME seconds per installed phase, with a 20 CPU-second orchestration component inside that ceiling. Payload raw CPU plus the full orchestration component is settled exactly once. Unknown raw CPU consumes the full reservation. Strict `termination_known=false` independently bars authority without replacing immutable prior settlement. Old v1 observations/profiles retain their semantics.

An enrolled guardian service has LimitCPU=13, TasksMax=1, fixed single-thread environment, original absolute BOOTTIME SIGKILL timer, and a payload slice bound to guardian lifetime. Three durable one-use slots cover the start owner, fixed bus client and recovery owner. Recovery claims before active observation; it commits store recovery before cleanup. The proposed arithmetic is guardian 13 + one-second margin, plus three controls each 1 + one-second margin = 20. This is a configured candidate requiring Linux proof, not an established enforcement bound.

A persistent host slice shares MemoryMax, swap=0 and group OOM across qexec, schedulers, clients, guardians and Docker payloads. Memory peak/OOM facts conservatively include other campaigns and survive work completion. Shared platform daemons outside the accounting scope are excluded under the coordinator's explicit interpretation. Fixed Docker requests only inspect/info/create/start/kill/delete installed probe images; no build/archive/exec processing is outsourced.

## Bounded handoffs and return boundary

- Versioned accounting, immutable recovery arithmetic, diagnostic custody and fresh authenticated clock binding are implemented with local persistence tests.
- Fixed Linux controller/probe/configuration and seven targeted harness cases are implemented candidates only; no real-host run or installed image/release identity exists.
- Recovery claim-before-observation fix is locally verified. Spent claims refuse active retry. Crash-after-claim authority gating remains a demonstrated source gap to review.
- Final selected tests, affected regression tests, standard check and whitespace check are run against frozen runtime/test bytes. Final identities and actual results belong in the external return packet and post-recorder ledger entry.

## Remaining source defects and proposed follow-up

The private scheduler constructs ExecutionService before reserving work; hard per-process limits do not charge failed pre-reservation launches to the campaign lifetime. A spent recovery claim survives crashes but does not itself invalidate authority: a crash before recover_work may leave BOUND state, and the private scheduling path does not inspect pending recovery issues. Duplicate SUBMIT/status are bounded historical transport, but repeated post-admission VOID performs campaign authentication without a reservation or control timer. These are source-level issues, separate from missing Linux proof. The smallest follow-up must move construction behind a durable metered intent, make interrupted claims block positive authority transactionally, and move cancellation authentication under charged work while keeping cheap historical transport bounded.

The coordinator requested freezing this reviewable candidate rather than extending its architecture indefinitely. No claim of complete supervision or S2 acceptance is made. Preserve complete source/config/docs and all records outside the disposable checkout.


## S2-R1 bounded repair (2026-09-19)

The coordinator assigned only interrupted-recovery durable authority and completion. All 2,076 frozen S2 source hashes matched before edits; doctor passed with the original operations interpreter. The frozen S2 packet remains untouched. The failing interrupted-claim reproduction is now a test that requires refusal after reopen.

First RECOVERY_OWNER claim atomically adds a snapshot/v4 recovery row and its one-use control object. The row holds claim identity, only a hash of the live ephemeral owner token, claim-bound observations, immutable completion, and a strict continuation-required marker. Accounting events carry temporary barriers without gratuitously changing fixed-intent authority tokens. Every new store authority decision checks pending/continuation state; the runtime checks v4 pending state too. Exact historical retries remain historical, and legacy v3 recovery-control objects without a projection are readable but block store authority rather than inventing completion.

Recovery claim, recover_work, and complete_recovery require independent transactions. Owner-bound observations commit before cleanup. Completion requires the same live token and durable matching facts/owned-absence event; it clears only its own temporary barrier and never clears terminal budget facts or VOID. A claim made without an owner token is deliberately uncompletable. Production generates a random token in memory and never persists it. Losing it leaves the attempt safely blocked. No new active restart continuation is provided, even with spare budget; it requires a separate already-funded design.

A genuinely new active recovery request after successful completion encounters the spent slot. Before raising refusal, it commits continuation_required in a standalone transaction; no runtime construction, counter inspection or cleanup occurs. The old completion remains immutable and replay cannot clear that marker. Historical reads/replays never call the active claim API. This covers RESERVED -> recovery completed -> legitimate start -> new recovery need -> durable spent-slot refusal -> reopen -> positive authority blocked. This is a liveness restriction, not a new allowance.

The other S2 source blockers remain open: scheduler construction before reservation, VOID authentication accounting, and original deadline coverage before bootstrap timer installation. Linux proof remains absent. Final source-bound results and repair packet identity will be recorded after recorder closure; neither R1 delivery nor local tests accept S2 or authorize activation/S3.


### R1 physical dispatch boundary and acyclic acknowledgement

The coordinator extended this same repair to serialize the actual system-manager and Docker start request against recovery. A snapshot/v4 dispatch row is committed BEFORE the external effect. Only its live random owner token may acknowledge the bounded request. Lost acknowledgement or persistent post-effect database failures leave a durable pending marker after reopen, even if recovery cannot write. No automatic relaunch, recovered owner token, or fresh allowance is supplied. Recovery and dispatch markers independently block every new positive decision. Exact historical acknowledgement is idempotent; a delayed acknowledgement clears only its own marker and cannot undo recovery, VOID, terminal facts or charges.

A second transaction samples a fresh clock and rechecks current authority immediately before the bounded OS request. Popen occurs under that lock; communicate does not. The fixed busctl StartTransientUnit method acknowledges a queued system-manager job, not guardian application readiness or qualification completion. The parent validates the bounded returned job path and commits acknowledgement. The guardian waits for that commit only AFTER its existing absolute BOOTTIME timer is installed, under its already charged process CPU limit. It sleeps outside any store transaction. Docker's bounded start HTTP response acknowledges that request; it does not wait for qualification callbacks, and the caller then acknowledges only its payload marker. This adds no process or allowance and does not repair the separately open pre-timer bootstrap interval.

Reference semantics are checked against systemd v255 primary source: [StartTransientUnit](https://raw.githubusercontent.com/systemd/systemd/v255/src/core/dbus-manager.c) queues JOB_START; [bus_unit_queue_job](https://raw.githubusercontent.com/systemd/systemd/v255/src/core/dbus-unit.c) constructs and sends its method reply after queueing. Therefore guardian acknowledgement waiting is not on the manager reply dependency path. The installed Linux release/version remains unverified. A local concurrent regression models a guardian already waiting while the bus client returns the queued-job acknowledgement, then observes the parent commit releasing the guardian. This is scheduling/persistence evidence, not Linux enforcement proof.

Fault tests cover recovery-first/no-start, launch-first/recovery-next, fresh in-lock clocks, original deadline refusal, lost acknowledgement, post-effect commit failure, persistent database failure including failed recovery, error chaining, reopen refusal, wrong owners, delayed acknowledgement after recovery/VOID/terminal facts, no relaunch, strict snapshot parsing and positive authority gates. Final records and coordinator review determine R1 acceptance; S2 remains incomplete.
