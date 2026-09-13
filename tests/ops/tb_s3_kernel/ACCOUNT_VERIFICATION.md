# Account integration verification — PR #370

Starting head: `b5637231cd73360fceb9a36533ba9675eb3896ba`.
Merged dependency: main `880a8b89d7f63b231e83174c451d4f1387c226f1` (#369).
Review candidate: merge head `56f4deb0f07720843ec79e6f0007d296d4eb1b61`
plus the changes committed with this record. No production modules were changed.

## Local evidence — 2026-09-13

- Combined primitive/account/producer tests: **468 passed**, including 19 new
  account integration sequences with literal/event-derived expectations.
- Full ops and final static-check results are recorded below after completion.
- Independent review reproduced findings before correction and exercised the
  trigger outcome matrix: accepted with lost acknowledgment, unknown not reached,
  rejection/retry and deferred execution, with/without listener restart. Each
  retained FIFO base0/add2 and exactly one reduction.

New cases cover FIFO owner identity, expired cached-flat loss, repeated EOD,
retired versus unfinished run expansion, source restart/ordering/conflicts,
delayed and continuing healthy bars, unacknowledged emissions, configuration
failure/read-back, pure daemon acknowledgment status and post-restart disarm
fencing. Two inherited assertions changed to match rev7: ongoing loss retains
the next-session latch; planned disarm requires post-restart evidence.

## Boundary

Account schema7, primitive schema6 and daemon schema1 are offline snapshots;
there is no migration or deployed config/heartbeat implementation. The offline
configuration owner is separate from listener durable state. Source-health
reports follow ordered episode recovery so the listener does not mistake an old
recovery timestamp for continuously refreshed health. Historical report replay
preserves current expired-source latches and sequence-gap ownership.

The extension adds durable close-time triggered-protection semantics; partial
trigger execution is refused, and explicit-close limits remain as documented.
See `ACCOUNT_CONTRACT.md`. Acceptance is bounded to this model. Policy ratification,
production capability qualification, source-feed authorization and live deployment
remain separate. Hosting CI and user approval are external merge gates.

Final local full ops: **1,045 passed, 13 skipped**, with two existing seaborn
deprecation warnings. Errors-only pylint on the model/account suite passed with
the repository and ops import roots configured. Final diff whitespace check passed.

Independent final review accepted the offline account model at the candidate
revision above plus the reviewed changes: **no remaining blocking findings**;
independently **468 passed**, clean whitespace checks, and trigger retry/restart
outcomes. The additional ordered `health` observation is an offline shape beyond
rev7 R-N's episode envelope; deployed transport mapping/qualification remains owed.
