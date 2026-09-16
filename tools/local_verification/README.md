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
to select tests. The wrapper locates per-user Docker Desktop even when the
current shell has an older PATH, temporarily exposes its credential helper,
and restores PATH when it finishes. Start Docker Desktop before running it.

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
Exit zero is accepted only if the command succeeds, output capture completes,
and the source stays stable. Do not edit, stage or commit during a recorded run.
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
