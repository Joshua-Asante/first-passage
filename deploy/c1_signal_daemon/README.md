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

## 2026-09-11 - Stage 1 input: operator-attended controlled input (option D)

Stage 1 accepts one operator-attended bar for the reviewed ceremony. Databento
remains retired, with no adapter or dependency in the stdlib-only daemon image.
There are no new config keys. Stage `"poll_interval_s": 1` on the daemon volume
before the ceremony and before daemon startup: the loop caches this interval at
startup. `prepare` and `enable` require `0 < poll_interval_s <= 1`.
Startup stays inert even with stale enabled flags.

The reviewed manifest is `/data/m1_manifest_<id>.json`; `source` is the exact
`OPERATOR_INPUT_SOURCE` marker and `venue_contract` is the operator's dated MYM
quarterly contract. The state file's parent determines the input directory
(`/data` for the example config): upload `m1_upload_<id>.json`, published one-shot
`m1_bar_<id>.json`, and exclusive claim `m1_claim_<id>`. The operator creates the
private OHLCV JSON outside the recorded console and transfers it with SFTP.
Never put bar values or secrets in command arguments, logs, or ceremony records.

Run from `/app` inside the daemon image, using the A7 reviewed identifiers:

```bash
python ops/c1_signal_daemon/m1_stage1_control.py prepare --state /data/c1_m1_stage1_state.json --config /data/c1_signal_daemon_config.json --boot-id <boot_id> --manifest /data/m1_manifest_<id>.json
python ops/c1_signal_daemon/m1_stage1_control.py enable --state /data/c1_m1_stage1_state.json --config /data/c1_signal_daemon_config.json --boot-id <boot_id> --manifest /data/m1_manifest_<id>.json --ceremony-id <id>
python ops/c1_signal_daemon/m1_stage1_control.py inject --state /data/c1_m1_stage1_state.json --config /data/c1_signal_daemon_config.json --ceremony-id <id> --boot-id <boot_id> --contract <venue_contract> --time <target> --bar-file /data/m1_upload_<id>.json
python ops/c1_signal_daemon/m1_stage1_control.py close --state /data/c1_m1_stage1_state.json --config /data/c1_signal_daemon_config.json --ceremony-id <id>
```

Under A7, the operator runs `enable` and `inject`. Inject only after the target
minute's bar closes, inside `[target + 60 s, target + 120 s]`. A successful
injection prints a value-free receipt including `bar_sha256`. The upload is
removed on success or refusal; the one-shot publication is consumed once, and
its claim prevents replacement. Close removes the ceremony's input files;
startup removes orphans. Preserve the journal and tombstones, including any
unresolved transport attempt that prevents preparing another ceremony.

`python ops/c1_signal_daemon/m1_stage1_control.py status --state /data/c1_m1_stage1_state.json --config /data/c1_signal_daemon_config.json`
reports boot/ceremony identity, `state`, conservative `effective_emit:false`, and
`source_status` (`disconnected` or `bar_published`), without bar values. `GET /`
reports `feed_mode:"operator_input"`, cached `poll_interval_s`, `ceremony_state`,
`effective_emit`, `connected`, and `feed_healthy`. After prepare, state is `READY`
and health stays `effective_emit:false`; after enable, health becomes
`effective_emit:true`, still `connected:false` until the injected bar is read.
Wait for the attempt's terminal journal state before close and evidence review.

This controlled input certifies the Stage 1 handoff with
`qualifying_live_source:false` and `operator_attended_input:true`; it does not
establish unattended live-source operation. See the
[S2b option D addendum](../../docs/adr/2026-08-08-s2b-signal-daemon-build.md#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d),
[M1 input addendum](../../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-09-11--item-5-input-for-stage-1-operator-attended-controlled-input-express),
and [A7 attended ceremony](../../docs/briefs/handoffs/2026-09-10-track-a-a7-claude-attended-stage1-dry-run.md).
The daemon remains a separate app and volume; this packaging change grants no
deployment or emission authorization.
