# Account and daemon orchestration candidate

Stage 3 of the PR365 extraction consumes the durable primitive stage and implements
PR360 rev6 §2e A1. **Unaccepted offline candidate.** It does not accept or hide the
consumer findings recorded in `KERNEL_CONTRACT.md`.

`AccountKernel` extends `Kernel` with takeover, EOD, kill/disarm, session latches,
feed-loss intents and daemon-loss handling. Primitive state, account control time,
reservations and all planned effects commit in one snapshot. The completion hook
plans required disarm work automatically during reconciliation/progress; status
queries remain pure. `Daemon` uses the same primitive bracket classifier for typed
reissues. Account tests use `account_harness`; primitive tests retain their own
harness and cannot accidentally rely on the daemon layer.

| Sequence | Expected outcome |
|---|---|
| Two displaced scopes, crash between dispatches | Both scopes remain durably owned; actual partial broker effects are preserved. |
| Bounded close executes but residual protection fails | Queued recovery can proceed without repeating the bounded quantity. |
| Kill, unresolved external request, later evidence | No premature completion; disarm follows actual quiescence automatically. |
| Feed or daemon loss, working remainder, racing fill | Cancellation and subsequent exposure remain owned through confirmation. |
| Session rollover during unfinished recovery | Session latch clears; primitive obligations remain. |
| Typed bracket reissue with stale control | Tightening/attach and loosening use their correct shared action classes. |

Account schema 5 and primitive schema 4 are intentionally incompatible offline
snapshots. Either direction refuses recovery rather than dropping account state.
This supplies no production migration or configuration acknowledgment protocol.

Acceptance requires the primitive blockers to close, integrated review, CI and
revision-bound sequence evidence. L1 producer equivalence, L2 validation, actual
disarm acknowledgment, feed-loss ratification and existing live gates remain owed.
