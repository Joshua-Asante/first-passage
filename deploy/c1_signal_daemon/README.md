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

## 2026-09-10 - source unavailable

Databento is retired and unsubscribed by operator report. No replacement is
approved. The daemon image has no Databento adapter or dependency; startup uses
NullStrategy and an unavailable bar source even if old ceremony flags are true.
Prepare/enable commands refuse without writing state. Close/status remain usable.
No fixture or replay is licensed as M1 item-5 evidence. See the
[M1 contract](../../docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md).
The daemon remains a separate app/volume; preserve its journal and tombstones.
This is offline infrastructure only, with no deployment or emission authorization.
