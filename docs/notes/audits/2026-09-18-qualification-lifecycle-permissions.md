# Qualification lifecycle and permission verification

Scope: structural-closure Task 8, protected synthetic N1_ONLY. The service now
handles up to four peer connections concurrently, with bounded admission. Existing
peer credentials, request limits, reservation locking and transactional journal
guards remain the authority boundary. Test-only administrator checkpoints change
timing, not outcomes, signatures or transitions; they are outside the worker image
and normal service entrypoint.

Implementation base: `0cc800f`. Verified code/test revision: `9cd2e99` on
`codex/qualification-lifecycle-coverage`. Overall qualification acceptance, Task 9,
full-campaign execution, production activation and merge are outside this outcome.

## Covered behavior

| Case | Required retained outcome |
| --- | --- |
| Simultaneous submissions and changed binding | One reservation/execution/start; conflicting binding cannot alter history. |
| Death after reservation, before scheduling | Durable IN_DOUBT, no container or start, exact retry cannot schedule. |
| Death after container creation or start intent | Same execution/container/plan; no start after recovery. |
| Death during partial output or while worker is stopped | Exact owned worker stopped; IN_DOUBT; no attestation/result/redraw. |
| Death after durable capture, including signer denial | Recovery signs retained capture; one start and one attestation. |
| VOID/publication, both writer orders | VOID first prevents publication; publication first remains historical. |
| VOID/first commit, both writer orders | VOID first prevents assessment/CUTOFF; commit first preserves historical receipt. |
| Lost commit acknowledgment and service death | Exact original receipt/authentication after restart, including with result credential denied. |
| Expiry before actual start or new authority | No accepted execution/result; current eligibility false after expiry. |
| Exact commit retry after expiry or VOID | Original receipt, unchanged history, current validity/eligibility separately visible. |
| Changed authentication | Conflict; original authentication and receipt unchanged. |
| Client and running worker permissions | Actual UIDs cannot read keys/journal or write code; client cannot remove service socket; worker has no host sockets and cannot write inputs. Positive code/input reads also checked. |

Race checkpoints use real SQLite trace callbacks for the second BEGIN IMMEDIATE
attempt, a distinct lock-acquired observation, and administrator release files.
Each checkpoint/control is bound to the attempt and retained with PID, UID, thread
and monotonic time. No sleep determines which transaction wins. Reopening the
supervisor revalidates the persisted journal before final assertions.

## Verification records

- Windows operations Python **3.13.2**:
  `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`.
  Checkout `fp.ps1 doctor`: 62 locked packages matched.
- `./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution -q --tb=short`:
  **226 passed**, clean `605c23a`; [record](../../../.cache/fp-verification/20260918T041142Z-27225522003c/record.json).
  Subsequent changes affect only Linux test assertions/checkpoint evidence and
  documentation; the production dispatcher and local execution tests are unchanged.
- `./fp.ps1 check`: exit 0 on the implementation working tree based at `0cc800f`,
  72 evidence-store cases with three existing skips;
  private Pine/data artifacts absent as disclosed by the gates.
  [Record](../../../.cache/fp-verification/20260918T040526Z-175b8b56f607/record.json).
  Git's configured hook separately used Python 3.14.3; it is not the operations
  interpreter evidence above.
- Linux collection: 34 cases, no collection errors;
  [record](../../../.cache/fp-verification/20260918T042936Z-47090970ff6c/record.json).
  Collection is not Linux execution acceptance.

The initial two-host [run 35306380360](https://github.com/Joshua-Asante/first-passage/actions/runs/35306380360)
at `82ee3ef` remains **failed**: each host reported 33 passed, one failed, no skips.
The single failure was an incorrect diagnostic substring in the new expiry test.
Retained events show the real approval rejection and IN_DOUBT disposition. The
correction compares intent, expiry and actual daemon-start times plus the complete
event sequence. Both failed records are stable/complete and cleanup succeeded.
The [diagnostic audit](../../../.cache/qualification-linux/35306380360/lifecycle-diagnostic-audit.json)
checks 27 attempts, four race orders, both permission identities and all retained
event/object hashes per host; it explicitly does not confer acceptance.

The corrected [run 35307206216](https://github.com/Joshua-Asante/first-passage/actions/runs/35307206216)
at **`9cd2e99f58a13136e89f3b29c83cbedad41aee9a` passed on both fresh Ubuntu hosts**:
34 passed, zero failures/errors/skips per host. Both records are completed, exit 0,
source-stable, capture-complete and free of capture/report errors; both owned
cleanup reports are successful. Each checkout was clean, with source fingerprint
`3406d048ffc98ad2a2b861d369b4e43aff6618fd7388b986874aa63231ef20eb`.

The workflow used operations Python **3.12.3**, selected and checked by its own
checkout launcher, and invoked:

```sh
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" python \
  scripts/qualification_boundary_verification.py --test-only --manifest "$manifest"
```

The recorder ran `python -m pytest tests/integration/qualification_boundary -q
--tb=short --junitxml=...` inside its owned process group. Exact interpreter paths
and argv are retained in the records:

| Host | Record | Journal SHA-256 |
| --- | --- | --- |
| 1 | [1e2740e0f76b4364a185edbbe9068b11](../../../.cache/qualification-linux/35307206216/qualification-host-readiness-1/1e2740e0f76b4364a185edbbe9068b11/record.json) | `b56b8a624f6d37bdba743b3901d204d34d401465c33ad5bf2d615207fcff1c6c` |
| 2 | [ec5a48c668974779813b0370cbd7e91f](../../../.cache/qualification-linux/35307206216/qualification-host-readiness-2/ec5a48c668974779813b0370cbd7e91f/record.json) | `3c8a8c769dd31342e07c8d9550de22e5632d1ebaf71cb4aef8c8229cda696cba` |

The [retained-artifact audit](../../../.cache/qualification-linux/35307206216/lifecycle-audit.json)
passed using `./fp.ps1 python .cache/audit_lifecycle.py
.cache/qualification-linux/35307206216 9cd2e99f58a13136e89f3b29c83cbedad41aee9a`.
It inspected 27 attempts per host: one reservation and at most one actual start,
complete event hash chains and object hashes, consistent original receipt/result/
authentication identities, all four real writer orders, and both actual permission
identities. Each host retained 11 attempt-bound checkpoint control records. This
is a focused evidence audit, not the future Task 9 invariant gate.

Raw records, JUnit, journals, objects, checkpoint observations and permission
reports are downloaded under `.cache/qualification-linux/35307206216`; the run's
two `qualification-host-readiness-*` artifacts retain the same host evidence for
14 days. The local evidence is preserved. These final documentation changes do
not change the code or tests verified at `9cd2e99`.

The selected lifecycle/permission outcome is verified. User authorization for the
public branch push and two-host TEST_ONLY execution was explicit; no PR, merge or
deployment is part of this task.

The permission result uses the existing trusted-administrator/privileged-qexec
model. It verifies client/worker denial, not confinement of a malicious qexec with
Docker authority. Focused self-review was performed; independent combined review
remains with the structural-closure coordinator.
