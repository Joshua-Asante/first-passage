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
