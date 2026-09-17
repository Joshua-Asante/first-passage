# Local Linux sequence verification

Run from this checkout using PowerShell 7.3 or newer:

```powershell
.\tools\local_verification\run.ps1 -Build
```

Evidence is automatically stored in a unique ignored
`.cache/fp-docker-verification/<timestamp-id>/` directory. Alternatively provide
`-EvidencePath <new external directory>`; existing evidence is never overwritten.
Omit `-Build` to reuse the local image. Add `-Workers 2` to opt into the already
installed pytest-xdist runner (0/default is serial; maximum 8; `loadscope`
distribution). Measure the same selection before choosing a worker count.
Use `-TestPath @('tests/ops/test_book_takeover_phases.py')`
to select tests. The PowerShell entry point delegates to the standard-library
`scripts/docker_verification.py` runner, which locates per-user Docker Desktop
even with an older PATH and exposes its credential helper only to child processes.
Start Docker Desktop before running it. Tests use the cached local image; the
runner does not use Docker Build Cloud, Scout, hosted runners or paid services.
Only explicit `-Build` requests build/pull dependencies.

The build context contains only the Dockerfile and two dependency files. Tests
run with networking disabled and source mounted read-only. Temporary SQLite
databases use Linux `/tmp`, avoiding the Windows shared pytest-directory ACL
and filesystem-lock differences. Only the evidence directory is writable on
the host. No live broker, credentials, service ports, or deployment are used.

The base image is pinned by digest; project dependencies use the existing
hash-locked operations requirements. Test-only supplements are version-pinned.
Debian package resolution is not fully locked; the resulting image ID and full
Python package versions are retained. This is Linux/Python 3.11 verification,
not an exact reproduction of GitHub's `ubuntu-latest` runner.

`record.json` retains the commit, git diff hash, tracked/nonignored untracked file
hashes, source fingerprints before/after, lockfile hash, command, image/runtime
metadata, timestamps, process exit code, JUnit counts and artifact hashes.
`stdout.txt`, `stderr.txt`, `junit.xml` and `coverage.json` retain raw results.
Records are reserved before Docker preflight and atomically finalized. Setup
failures are `not_started`; only `completed` is acceptance. Exit zero additionally
requires complete output, valid fresh JUnit, stable source and confirmed cleanup.
Do not edit, stage or commit during a recorded run.

Each container gets a unique run label; the test container ID is retained in
`container.cid`. On completion, failure or handled interruption, the runner checks
ownership before removing exact IDs and asks Docker to confirm their absence.
It can recover by label when creation's response/CID was lost. Cleanup failure is
recorded and cannot pass. A hard kill cannot run cleanup: its last `running` record
remains incomplete and may require removing the matching owned container manually.
`setup.log` and `setup_commands` retain preflight, creation and cleanup evidence.
These records never authorize removing containers belonging to another run.
Ignored files are outside the source fingerprint; these tests must not rely on
ignored data. The recorder does not snapshot external services or secrets.

The generated tests are opt-in under tests/sequence_verification (without the default test_ filename prefix) so default operations CI
does not silently gain an unpinned Hypothesis dependency. They use deterministic
Hypothesis settings (20 examples per test, no persistent example database), real
owner/runtime interfaces, and the existing offline synthetic broker. They cover
delayed cancellation, late fills, repeated/duplicate inventory, partial closes,
restart fencing, ordinary exits and scheduled flattening. A passing run is
bounded evidence, not proof that every execution sequence or PR behavior is safe.

For an arbitrary local command, invoke `scripts/record_verification.py --repo
<checkout> --output <new external directory> -- <command> <arguments>` using the
operations launcher where available. It uses only the Python standard library.

## Baseline attribution and local feedback

Use the [separate baseline/implementation workflow](../../scripts/README.md#separate-baseline-and-implementation-checkouts)
for fixed-revision comparisons. Each checkout validates its own lock with doctor;
shared environments remain unchanged during runs. Baseline results are reusable
only for recorded inputs and never qualify the candidate. Keep the measured
source, index and HEAD unchanged; retain evidence before removing any owned clean
worktree with `git worktree remove`.

The shared recorder emits a 30-second supervisor heartbeat separately from child
logs. This direct Docker pytest route does not load the local launcher's progress
plugin, so its heartbeat reports test activity unavailable. JUnit, source stability,
complete capture and confirmed owned cleanup still determine acceptance. Generic
recorded commands likewise gain no pytest-only argument injection.
