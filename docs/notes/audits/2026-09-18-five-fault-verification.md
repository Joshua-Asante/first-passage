# Five faults verified on both disposable Linux hosts

Scope: PR425 five-fault repair only. Combined qualification acceptance remains with the PR425 coordinator.

Tested and published commit: `0cc800f8b2197465a6e3f2caef32afacb13fb6d4`, branch `codex/qualification-fault-verification`, based on PR425 `6590b61`. The separate structural-closure worktree's unfinished lifecycle edits were preserved. This report is a local post-run artifact, not part of the tested commit. No PR merge or draft-status change occurred.

Run: [35302983875](https://github.com/Joshua-Asante/first-passage/actions/runs/35302983875), dispatched with `boundary=true`. Both jobs ran the real execution-boundary selection, despite the workflow's historical host-readiness name.

| Fault | Host 1 | Host 2 | Observed evidence |
| --- | --- | --- | --- |
| Stop | PASS | PASS | Callback log visible before EOF; exact container received SIGSTOP; host process state T; supervisor death/restart left IN_DOUBT |
| Zero-exit | PASS | PASS | Exit 0 without complete output was rejected |
| CPU | PASS | PASS | CPU/wall budget error, exit 1 |
| Wall | PASS | PASS | CPU/wall budget error, exit 1 |
| Memory | PASS | PASS | Exit 137, OOMKilled=true, OOM event before die, kernel-confirmed memory-cgroup kill |

All ten executions retained one launch intent and one actual Docker start, no attestation or accepted result, and unchanged execution identity/events on restart and exact resubmission. Both memory runs retained an empty Docker kill-event list. Both owned cleanups succeeded with no failures.

## Repair and investigation

The worker already emits the stop marker with `os.write`. The supervisor's buffered `stderr.log` hid it until EOF. The common capture loop now flushes every diagnostic chunk; final fsync and byte limits remain. The regression failed against the old loop with an empty live log and passed after the fix.

Historical run **35299214700**, at `67b93dd`, remains failed. Its host 2 container `27279ed72cff826c7d0f063fcbf8a83837e8077531e14078b3ec684486bf1526` exited 137 after 3.116 seconds with OOMKilled=false. Its retained evidence cannot distinguish an external SIGKILL from an unrecorded OOM; no kernel/cgroup/OOM event evidence was retained. Its cause remains unconfirmed. Host pressure from the former single 1.5 GB allocation was a hypothesis, not a demonstrated root cause.

The synthetic fixture now charges paced 1 MiB resident allocations under the canonical 256,000,000-byte TEST_ONLY limit, capped at roughly twice that limit if enforcement fails. Its contract memory budget derives from the profile. The hosted assertion requires OOMKilled=true and ordered OOM/die events; exit 137 alone remains insufficient. Kernel and systemd-oomd logs are retained for diagnosis.

Fresh kernel evidence independently confirms both memory failures:

- Host 1: container `4e3bbc5ff322a30980b9b2a10f72535ee3bc73a3e0781cb2c92a6e95da6ac6f1`, PID 5502, UID 65532, `CONSTRAINT_MEMCG`, at 03:27:04 UTC.
- Host 2: container `3adcc4f155b376503ab2a2bdaa2fecc57a3fb639d41ba942ced897d2bced9ed2`, PID 6064, UID 65532, `CONSTRAINT_MEMCG`, at 03:27:30 UTC.

## Commands and evidence

On each Ubuntu 24.04 host, the existing workflow provisioned the protected installation, ran its launcher doctor, then:

```sh
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" python scripts/qualification_boundary_verification.py --test-only --manifest "$manifest"
```

Operations Python 3.12.3, 62 matched locked packages. Host 1 interpreter `/var/lib/fp-qualification-tests/a640026cfde446b280e089b4ef14981c/env/bin/python`; host2 `/var/lib/fp-qualification-tests/86cbb1d6e00a486cb342959b25b50077/env/bin/python`. Each ran 19 tests: 19 passed, 0 failed, 0 errors, 0 skipped. Both records completed with exit 0, stable clean source, complete capture, valid reports and cleanup.ok=true. Shared source fingerprint `89839f3334ea4115124f5d3da68d6a0697b4198b8fde2e8ceb1cfdb445ea7429`.

Downloaded evidence is under `.cache/qualification-linux/35302983875/` in this worktree:

- [Audited five-fault summary](../../../.cache/qualification-linux/35302983875/five-fault-audit.json)
- [Host 1 record](../../../.cache/qualification-linux/35302983875/qualification-host-readiness-1/5a89bfa877034b2ca242c2489c54d411/record.json)
- [Host 2 record](../../../.cache/qualification-linux/35302983875/qualification-host-readiness-2/7cc73abd79be49fbb7bbe80b9cb24f38/record.json)

The local audit checked record status, clean exact revision, report hashes, all five named JUnit cases, callback logs, stopped receipts, container inspections, single starts, OOM/die ordering and cleanup. Kernel logs were separately matched to each memory container.

Local Windows validation used the checkout's `fp.ps1` with operations Python 3.13.2 at `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`:

- Doctor: 62 locked packages matched.
- `./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution -q --tb=short`: 219 passed, no skips; clean commit 0cc800f; [record](../../../.cache/fp-verification/20260918T032302Z-f76d8a67ca13/record.json).
- Targeted launcher/profile/fixture selection: 29 passed; [record](../../../.cache/fp-verification/20260918T031851Z-6d15a0e93674/record.json).
- `./fp.ps1 check`:exit 0;72 evidence-store tests with 3 existing skips; private Pine/data artifacts unavailable and disclosed by the gates; [record](../../../.cache/fp-verification/20260918T032028Z-a54f8151627f/record.json). Recorder and Git hook used their configured Python 3.14.3; this does not replace operations-interpreter results.

All three successful local records have completed status, stable source, complete capture and no report errors. This task does not claim the full repository test suites, invariant-gate closure, or combined PR readiness.
