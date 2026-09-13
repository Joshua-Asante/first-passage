# Account and daemon orchestration — rev7 offline boundary

Stage 3 composes the merged producer (#368) and primitives (#369) under TB-S3
rev7 §2e A1. This model is separate from the production listener and daemon.
Ratification, L1/L2 qualification, deployed configuration ownership and live gates
remain prerequisites for production implementation/operation.

## Account work

Takeover publishes every displaced scope before dispatch and rechecks admission
and fresh quiescence at settlement. EOD, kill and daemon-loss runs have durable
identities and include both owned and observed symbols. New locations expand an
active run. Session/liveness recovery retires completed runs; unfinished runs
retain responsibility for outstanding requests and their later locations. A new
session's EOD gets new work; a completed retired EOD cannot flatten unrelated
next-session exposure. Primitive obligations survive latch clearing.

Kill completion automatically journals a configuration-owner disarm. The offline
`ConfigOwner` models idempotent writes, failure, lost acknowledgment and read-back
of `dry_run=true` and `armed_until=None`. Unknown outcomes do not disarm the
listener. A planned effect waits for fresh post-restart account evidence, and
status queries never execute it. Each kill uses its own effect identity.
`acknowledge_daemon_control` is a command that verifies an offline heartbeat for
an explicit daemon config command and persists the outcome. `kill_status` ignores
its legacy reachability argument and reports only persisted acknowledgment.
This is an offline port, not a deployed Fly config/heartbeat implementation.

## Loss episodes and ordered reports

The daemon persists its initial observation time, source observations, episode
identities/boundaries and report outbox before delivery. Each leg has a contiguous
sequence domain. Listener acknowledgment publishes the episode/latch and close
work atomically; duplicates require identical retained payloads, gaps remain
owned through their highwater, and conflicting history retains an independent
block across rollover/restart. Unacknowledged reports suppress risk-add emission.

Expired source and daemon episodes own work even if cached evidence is flat.
Only post-preparation evidence can establish a no-op. Source recovery requires a
resumed observation after the episode boundary; delayed stale bars cannot discard
an episode. Historical reports are validated at their recorded time, while an
expired latest observation retains the current session latch. A successful
control GET proves daemon liveness only. A missing/unparseable control timestamp
is expired. Rollover clears recovered session latches while ongoing episodes and
unfinished primitive owners remain. Timers are explicit model events, not services.

## Close-time protection integration

The daemon validates the caller's leg/owner and complete bracket shape before
classifying a crossed fixed level. The durable close records `triggered_protection`
and the owner identity separately from explicit accounting-fill scope. The offline
producer atomically issues/triggers that owner and records request-attributed FIFO
reductions; surviving sibling protection/anchors remain. Bare first protection is
created and consumed within that single event. Explicit and triggered demands
cannot reuse an operation identity. Unknown outcomes reconcile before retry.
Partial close-time trigger execution is unsupported and refused before mutation;
no explicit-lot-close substitute is made. Existing bounded explicit-close limits
from #369 remain in force.

## Persistence and evidence

Account schema **7**, primitive schema **6**, and daemon snapshot schema **1** are
separate offline formats. Incompatible/missing fields are refused; no production
or historical-snapshot migration is supplied. Configuration owner state is external
to the listener snapshot and survives listener restart in the harness.

`ACCOUNT_VERIFICATION.md` records acceptance evidence. The historical extraction
record remains traceability only. No acceptance of superseded #365 transfers here.

After recovery, ordered health reports refresh the listener's source observation;
they cannot recover an active episode. This keeps a continuously healthy source
from aging the historical recovery event into a false outage.
