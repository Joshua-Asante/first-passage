# c1 signal daemon (Fly app)

Second Fly app for the Python-native signal host ([SPEC S2b](../../docs/spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) ·
[build ADR](../../docs/adr/2026-08-08-s2b-signal-daemon-build.md)).

**Not the listener.** Do not mount `c1_rail_data`. Do not share `peak_equity`.

## Create (once)

```bash
fly apps create c1-signal-daemon
fly volumes create c1_signal_daemon_data --app c1-signal-daemon --region iad --size 1
```

## Config

Copy `c1_signal_daemon_config.fly.example.json` → `/data/c1_signal_daemon_config.json`
with a real listener `path_token` (never commit). Keep `"emit_enabled": false` until
a separate strategy emit GO.

## Deploy

From repo root (listener must stay `dry_run=true` — separate app, but verify anyway):

```bash
fly deploy . --config deploy/c1_signal_daemon/fly.toml \
             --dockerfile deploy/c1_signal_daemon/Dockerfile
```

## Verify

```bash
curl -sS https://c1-signal-daemon.fly.dev/
# expect JSON: ok, feed_healthy, emit_enabled=false
```

## 2026-09-10 - dormant M1 Stage 1 path

See the [M1 test contract](../../docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md).
The example keeps `strategy="null"`, `emit_enabled=false` and
`m1_test.enabled=false`; no SDK connection occurs until a reviewed ceremony is
enabled on the current boot. This daemon remains a separate app and volume.
The image now pins Databento 0.81.0 and databento-dbn 0.62.0. A compatible Linux
Python 3.12 native import/build smoke is a deployment prerequisite, not an offline
test result. Control uses `PYTHONPATH=/app/ops python -m c1_signal_daemon.m1_stage1_control --help`.
Preserve the journal, initialized marker and tombstones through rollback. Close
first and verify effective emit false; a restart cannot renew a spent ceremony.
The contract covers source binding, private manifest, fresh listener preflight and
genuine ledger correlation. No fixture or manual POST discharges item 5.
