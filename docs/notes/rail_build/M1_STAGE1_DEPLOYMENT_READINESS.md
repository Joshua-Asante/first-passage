# M1 Stage 1 deployment readiness record

**Date:** 2026-09-11 (opened by Track A / A3; §A4–§A8 append in later sub-tracks)
**Owner:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3 — the parent session records each sub-track's return after the two-pass review
**Purpose:** the public, secret-free evidence trail for the two Track A deployments and the single attended Stage 1 ceremony: what was verified, from where, and what remains NO-GO.
**This note authorizes nothing.** No deploy, arm, order, or `RESOLVED` claim rests on it; the owners are the [M1 ADR](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md), the [S2b build ADR](../../adr/2026-08-08-s2b-signal-daemon-build.md), the [GO ADR](../../adr/2026-07-17-c1-rail-build-account-registration-go.md) and the c1-rail skill. Private figures (tokens, account ids, equity, raw bar values) never appear here; every `--status` paste replaces the account token with `account=<redacted>`.

## §A3 — Recovery path (2026-09-11)

**Brief:** [A3 handoff](../../briefs/handoffs/2026-09-10-track-a-a3-claude-recovery-path-attestation.md) · **Currency:** `origin/main @ b7e028a`; A0 hard check `git ls-tree --name-only origin/main ops/c1_rail/ | grep -c m1_stage1_` → `2` · **Authority used:** read-only Fly commands and read-only reads of the public tree and the private archive; no deploy, restart, `ssh` write, volume read, or archive push.

### 1. Mitigation in code

- **On `origin/main @ b7e028a`:** `grep -n "IMPLICIT DISARM" ops/c1_rail/c1_rail_http_server.py` → `159:` (comment) and `186:` (the warning). The block (lines 158–191) runs inside `load_config`: when the volume config says `dry_run=false` but `armed_until` is expired, absent or malformed at boot, the process logs `IMPLICIT DISARM at boot — …`, sets `dry_run=True` and `armed_until=None` **in memory**, and boots disarmed; the file on disk is unchanged until `python ops/c1_rail/c1_rail_arm.py --disarm` makes the disarm durable. The comment block dates the reversal to the 2026-07-31 incident.
- **Deployed build, history corroboration:** `git show 31fd642:ops/c1_rail/c1_rail_http_server.py | grep -n "IMPLICIT DISARM"` → `159:` and `186:`. `31fd642` (2026-08-19) is an ancestor of `origin/main` (`git merge-base --is-ancestor` true) and a public commit (`gh api repos/Joshua-Asante/first-passage/commits/31fd642` → `2026-08-19T17:30:26Z`), and the acceptance JSON pins the running listener build to `origin/main @ 31fd642` (release v7, machine `e820221a657d28`, image `deployment-01M0DMFSFXVXEHZ27G8VYC0WQK`).
- **Deployed build, decisive in-container read:** `MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "grep -n IMPLICIT.DISARM ops/c1_rail/c1_rail_http_server.py"` → run by the operator in their own PowerShell console on 2026-09-11 (the form `& fly ssh console -a c1-rail -C "grep -n IMPLICIT.DISARM ops/c1_rail/c1_rail_http_server.py"`; flyctl auto-updated 0.4.85 → v0.4.102 during the call) and read from the Terminal panel by the session. Printed, verbatim:

```
Connecting to fdaa:9e:e939:a7b:894:a6fd:8e8a:2... complete
159:    # at boot, treat that as an IMPLICIT DISARM and boot disarmed — do not
186:                "IMPLICIT DISARM at boot — %s. The config on disk still says "
```

  The connection address is the private IP `fly machine list` reports for machine `e820221a657d28`, and the two line numbers equal the `31fd642` and `origin/main` greps. **The deployed listener carries the implicit-disarm boot path.**
- **What the mitigation removes:** the `armed_until`-lapse crash-loop class — on 2026-07-31 a lapsed `armed_until` with `dry_run=false` still on the volume made the boot gate raise, Fly stopped the machine at its max restart count, and `fly ssh` could not reach a machine that never booted, so the documented remedy (edit `/data`, restart) was unreachable and recovery took an entrypoint override.
- **What it does not remove:** (a) config missing → the entrypoint's `WAIT:` guard sleeps instead of crash-looping (both apps; load the volume, then restart); (b) a green build whose CMD dies with `ModuleNotFoundError` (a module in no COPY line) → image rollback to the references in item 4 (the 2026-07-31 `core/historical_challenge.py` class; re-trace the import closure before every deploy); (c) a config that **exists but does not validate** — the `WAIT:` guard only tests the file's existence, and both entrypoints call `load_config` before the health server starts, so the process exits and Fly restarts it until the machine is stopped, the same reachability problem as 2026-07-31. Listener (`ops/c1_rail/c1_rail_http_server.py::load_config`): not a JSON object, missing required keys, `dry_run=false` without `events_log_path`, a `path_token` shorter than the minimum or still starting with `REPLACE`, and the other `ValueError` branches at lines 195–213. Daemon (`ops/c1_signal_daemon/daemon.py::load_config`): malformed JSON, `m1_test` not an object, missing required keys or a short `path_token` (`SystemExit`), non-boolean enable flags, an unknown `strategy`, or an enabled-ceremony configuration that is incomplete or carries a non-positive `generation` (`ValueError`, lines 58–86). These recur after A6 or a rollback whenever the staged file is wrong, which is why A6 Step 2.2b runs `load_config` locally on the prepared daemon config before the operator puts it, and why A4 reads the listener config's key set before A5. (d) any other boot failure. Classes (c) and (d) are the private procedure's territory (item 2); the daemon has no arming gate, so class (a) of item 1's mitigation never applies to it, but (a), (b), (c) and (d) all do.
- **Skew flagged, not edited:** `.claude/skills/c1-rail/SKILL.md` deploy pre-condition 6 still reads "An expired `armed_until` makes the host refuse to boot, and `fly ssh` needs a booted machine, so a restart cannot fix it." That sentence describes the pre-fix behaviour; the code above (on `main` since before `31fd642`) boots disarmed instead. The pre-condition's conclusion — know the recovery path before starting — still holds because classes (b), (c) and (d) remain. The parent rewords it through the skill's own authoring path; this record does not touch the skill.

### 2. Procedure availability

- **Repository:** `Joshua-Asante/first-passage-archive` — private; marked archived (read-only) on GitHub since the 2026-09-06 preservation push (`gh repo view` → `archived=true`, `PRIVATE`).
- **Pinned SHA:** `5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2` — the pin every archive link on this tree uses (for example the W6 ADR's Related line).
- **Path:** `docs/notes/rail_build/RUNBOOK.md` — blob `0b90318f7695`, 119,887 bytes, 40 headings at that SHA. The public pointer to it is the W6 ADR's Related link `docs/notes/rail_build/RUNBOOK.md`, dead on this tree by design.
- **Heading grep** `^#+ .*(recover|self-brick|override|arming log|crash)` → one hit: line **217 `## B7 arming log`**, the section the acceptance JSON's 2026-07-27 and 2026-08-19 notes cite for the incident timeline and the "self-brick class"; the file names the incident date `2026-07-31` five times and the override once. No body text is reproduced here.
- **Method:** no clone of the archive exists on this machine and none was created (brief §0.5 forbids cloning by default). Availability was verified read-only through the GitHub contents API at the pinned SHA; only heading lines and counts left the shell pipe.

### 3. Operator access confirmed

**2026-09-11** — the operator opened the procedure in the browser at the pinned commit and said, in-session, verbatim: "I opened the RUNBOOK B7 arming log at 5d47b4dc." Recorded after it was said; nothing else about the procedure is recorded.

### 4. Current and rollback releases

Read-only inventory, 2026-09-11, `flyctl v0.4.85` (`fly releases`, `fly status`, `fly machine list`, `fly image show`):

| App | Release | Machine | Image (tag) | Image (digest) | Source commit |
|---|---|---|---|---|---|
| `c1-rail` (listener) | v7 `complete`, 2026-08-19 18:28 | `e820221a657d28` — `started`, 1/1 checks, last updated 2026-08-19T18:28:50Z, volume `vol_vxm828pzmlzyn7j4` | `registry.fly.io/c1-rail:deployment-01M0DMFSFXVXEHZ27G8VYC0WQK` | `sha256:05d509ad2166760e6af00be09f592190522e8962cccd02ae7f1d973cb1a21e13` | `origin/main @ 31fd642` (acceptance JSON `code_commit_or_branch`) |
| `c1-signal-daemon` | v1 **`failed`**, 2026-08-08 04:50 — the only release, yet the machine runs (A4 explains this from evidence; this section only names the image) | `840759c2474928` — `started`, 1/1 checks, last updated 2026-08-08T04:53:26Z, volume `vol_r1j1pglm3zpmyy9r` | `registry.fly.io/c1-signal-daemon:deployment-01KZFVAFXM3RTWJWVWND6W6TQ7` | `sha256:8e3a8f687ac4770b8125a99301a10265fdc55400d3031c71710b16b888f0ce2b` | not pinned in any record; the plan §0 identifies it as the 2026-08-08 pre-#332 `IdleBarSource` build |

- **Rollback targets:** A5 → the listener image above (not v6: v6 is the flat-layout build v7 retired). A6 → the daemon image above (the source-free build, inert by construction: no `ops/c1_signal_daemon/m1_stage1_*` modules, no journal).
- **No-build rollback form:** `fly deploy --help` line 134 confirms `-i, --image string   The Docker image to deploy`. From the repo root:

```bash
fly deploy --image registry.fly.io/c1-rail:deployment-01M0DMFSFXVXEHZ27G8VYC0WQK --config deploy/c1_rail/fly.toml
fly deploy --image registry.fly.io/c1-signal-daemon:deployment-01KZFVAFXM3RTWJWVWND6W6TQ7 --config deploy/c1_signal_daemon/fly.toml
```

- **Pre-condition:** a rollback is itself a deploy. The six per-app pre-conditions apply in order — the listener host `--status` read first (judge by printed output; Windows `fly ssh console -C` may exit 1 after correct output), the documented command from the repo root, the import-closure re-trace, `fixture_hashes` re-pinned from **in-container** bytes for the listener (a rollback moves pinned files back), the boot line and health verified after, and this recovery path known.

### 5. Recovery cannot restore obsolete state

- Recovery writes touch only `dry_run` and `armed_until`: `c1_rail_arm.py --disarm` (`plan_disarm` sets `dry_run=True`, `armed_until=None`; `_write` is an atomic write keeping a one-deep backup) or the entrypoint override in the private procedure. Neither rewrites `c1_sizing_constants.json`, `lifecycle_state.json`, the DD state, or the daemon journal (`c1_m1_stage1_state.json`, its `.lock` and `.owner.lock`).
- The 69/11 Striker allocation is released doctrine ([ADR 2026-08-26](../../adr/2026-08-26-striker-legmap-cap-release.md); the committed `LEG_MAP` reads 0/0). Any residue on the listener volume is handled only by A5's attended migration step (`ops/c1_rail/m1_stage1_control.py migrate … --release-withdrawn`, operator-confirmed in-session), never by a recovery step.
- `dry_run=false` is never a recovery target: recovery ends disarmed, and re-arming is operator-only under the M1 gate (`--arm` is not in Track A).

### Deviations and flags for the parent

- Archive availability was verified through the GitHub API (read-only, headings and counts only) rather than a local clone — none exists here and the brief forbids creating one by default.
- Codex review (P2, 2026-09-11) folded: the daemon's failure classes were understated as two; config-validation crash loops are now class (c) for both apps, with the A6/A4 guards named.
- The decisive in-container grep was run by the operator in their own console because this session's permission layer blocked `fly ssh console`; the session read the printed output from the Terminal panel and recorded it verbatim (item 1).
- c1-rail skill pre-condition 6 wording skew (item 1) — parent rewords via the skill's authoring path.

**Return:** `DONE_WITH_CONCERNS` — every §4 limb held with pasted evidence and all five items are recorded; the three flags above are for the parent (the skill wording skew needs an edit outside this record; the other two are method deviations, recorded so the review can weigh them). Per-step gates: 2.1 pass · 2.2 pass · 2.3 pass · 2.4 pass · 2.5 pass. Files touched: this note only.

## §A4-L — Listener readiness (2026-09-11, first dispatch of the A4 brief)

**Brief:** [A4 handoff](../../briefs/handoffs/2026-09-10-track-a-a4-claude-deployment-readiness-review.md) · **Currency:** `origin/main @ 3a1b859` (§A3 merged as #348); A0 hard check `git ls-tree --name-only origin/main ops/c1_rail/ | grep -c m1_stage1_` → `2` · **Inputs:** the A2 return = workflow run [34652166362](https://github.com/Joshua-Asante/first-passage/actions/runs/34652166362) (`workflow_dispatch` re-run by the parent on `81fe7d7`, success, 2026-09-11 22:02 UTC; the merge-push run 34634657453 on `6ce7b21` also success) and §A3 above · **Authority used:** read-only host reads (in-container commands run by the operator in their own console because this session's permission layer blocks `fly ssh console`; output read from the Terminal panel), non-ssh Fly reads, and local tests on `origin/main`. No write to either volume, no restart, no deploy, no migration, no `preflight`.

### Host reads (Step 2.1; the `--status` account token is redacted)

Operator-run 2026-09-11 in PowerShell as one compound read (`& fly ssh console -a c1-rail -C "sh -c '…'"`); session-read from the Terminal panel. Flags, key names, hashes and counts are recorded; every other value is omitted.

- `python ops/c1_rail/c1_rail_arm.py --status` → `current: dry_run=True armed_until=None equity_source='crosstrade' equity_field='balance.netLiq' destination='tradovate' account=<redacted> bind_host='0.0.0.0' bind_port=8080` · `m1_gate: status='CODE_LANDED' result=FAIL` (expected while unresolved).
- `/data/c1_rail_config.json` keys: `_comment, account, alert_ack_dir, alert_log_path, armed_until, audit_log_path, bind_host, bind_port, constants_path, crosstrade_api_token, dd_state_path, destination, dry_run, equity_field, equity_path, equity_source, events_log_path, execution_state_path, lifecycle_state_path, path_token, secret_key, webhook_id, webhook_secret`; `{'dry_run': True, 'armed_until': None, 'equity_source': 'crosstrade', 'bind_port': 8080}`. The four M1 ledger keys the 2026-07-27 host note added are present. `equity_source=crosstrade` means A7's read-only `preflight` uses the live equity GET.
- `/data/lifecycle_state.json` → `{"Striker": "WATCH-1", "Striker NAS100": "WATCH-1"}` — no `M1 Stage1 Test` key yet; A5's migration adds it as `RETIRED`.
- `/data/c1_sizing_constants.json` → `tier Tradeify_Select_100K`, `E_firm 100000`, `cap_firm 80`; `leg_map` `cap_alloc` = `{'dj30_mym': 69, 'nas100_mnq': 11}` — **the 69/11 residue is still on the volume**, and there is no `m1_stage1_test` row.
- `/data/c1_dd_state.json` → `peak_equity` is a finite positive float (`float True`); the value is not transcribed.
- `/data/c1_execution_state.json` → `{'legs': {}, 'schema_version': 1, 'last_updated_utc': '2026-07-27T04:00:54+00:00'}` — no confirmed base.
- `/data/c1_rail_events.jsonl` → 32 records; last record `seq 32`, `kind transport_result`; record keys `dry_run, error, event_id, execution_verified, http_status, kind, order_id, payload_sha256, schema_version, seq, transport_state, ts_utc`. **A6's "no signal on boot" baseline is `seq 32`.**
- `ls -la /data` → the config (2026-07-31 19:47) with its `.pre-arm-bak`, `.pre-disarm-bak`, `.pre-m1-bak`, `.pre-simchain-bak` and `.prev` copies; `c1_sizing_constants.json` (2026-07-25) and `.v3bak`; `lifecycle_state.json` (2026-07-19); the events ledger (2026-08-03) and its lock; the audit log (2026-08-19); the alerts ledger, ack dir, broker-evidence file and current-equity file; no `*.m1-backup-*` yet.
- In-container `sha256sum` of the five pins → `923e0847…` (`c1_rail_arm.py`), `711980e8…` (`c1_rail_http_server.py`), `d3b16b3e…` (`c1_rail_listener.py`), `471e28da…` (`c1_rail_telemetry.py`), `93992da9…` (`c1_sizing_host_reference.py`) — **all five equal the acceptance JSON pins**: the running build is still the 2026-08-19 one.
- `ls ops/c1_rail/` → `__init__.py, c1_rail_arm.py, c1_rail_http_server.py, c1_rail_listener.py, c1_rail_slippage.py, c1_rail_telemetry.py, c1_sizing_host_reference.py, crosstrade_payload.py` (plus `__pycache__`) — **no `m1_stage1_*` files**, as expected before A5.

### Listener checklist (Step 2.2)

| Item | How evidenced | GO / NO-GO (owner) |
|---|---|---|
| `dry_run=true` on host | `--status` line, above | **GO** |
| `armed_until` None | `--status` line, above | **GO** |
| Account broker-verified flat | operator statement in-session from Tradovate ("No open positions") with time — an attestation, not agent-observed; A5 takes a fresh one immediately before its migration apply | **GO** — 2026-09-11 19:13 CDT (2026-09-12 00:13 UTC, the clock on the operator's screenshot): the operator stated in-session, verbatim, "No open positions", and shared a Tradovate screenshot showing Position 0 and Open P/L 0.00 on the open instrument panel. Attestation, not agent-observed (the session's own browser tab reached only Tradovate's login page, and credentials are never entered by the session). Private figures on the screenshot (equity, account id) are not transcribed. A5 takes a fresh attestation immediately before its migration apply. |
| Test identity migration exact and limited to one micro | `plan_migration` (`ops/c1_rail/m1_stage1_control.py` 79–105): changes only `leg_map[m1_stage1_test]` (`constants_row(enabled)`: `cap_alloc` 1 when enabled, else 0) and `lifecycle["M1 Stage1 Test"]` (`AUTHORIZED` / `RETIRED`); with `--release-withdrawn` it also sets `dj30_mym`/`nas100_mnq` `cap_alloc` to 0 and refuses unless each still reads exactly 69 / 11 or 0; `validate_sizing_inputs` then asserts the frozen tuple and `sum(cap_alloc) ≤ cap_firm`. `apply_migration` (108–133) requires `--flat-verified`, re-plans and refuses if inputs moved, writes immutable `.m1-backup-<uuid>` copies, then writes constants at cap 0 **before** lifecycle and enables the cap only when `enabled` is true. A5 runs `enabled=False` → cap 0 / `RETIRED`. `cap_alloc` can never exceed 1 for this identity (`CAP_ALLOC = 1`). | **GO** |
| Existing allocations reconciled | after-plan `sum(cap_alloc) ≤ 80` from the constants read above; residue disposition: 69/11 is released doctrine (ADR 2026-08-26; committed `LEG_MAP` 0/0), so any residue is released only by A5's `--release-withdrawn` with the operator's in-session `RW = True`, never inferred | **GO — one decision owed in A5.** Residue present: `dj30_mym` 69, `nas100_mnq` 11, no test row. A5's own plan (`enabled=False`) sums to 69 + 11 + 0 = 80 ≤ 80 with `RW = False`, so A5 can land the test row at cap 0 either way. But A7's enable (cap 1) would sum to 81 > 80 and `plan_migration` raises `m1_test_account_cap_exhausted` — A7 Step 2.2 returns `BLOCKED` on that residue. The release is therefore required before A7; the 2026-08-26 ADR makes it doctrine, and the volume write is A5's act with the operator's in-session `RW = True` (`--release-withdrawn`; `plan_migration` refuses unless the two rows read exactly 69 / 11 or 0, which they do). Owner: operator (decision, in A5); A5 (write). |
| Rollback image known | §A3 item 4: `registry.fly.io/c1-rail:deployment-01M0DMFSFXVXEHZ27G8VYC0WQK` (`sha256:05d509ad…`), no-build form confirmed | **GO** |
| Fixture-hash choreography specified | written below (Step 2.4) | **GO** |
| Exact deployment commands reviewed | written below (Step 2.4) | **GO** |
| A2-L green with L5b/L6/L7/L8 evidence | run 34652166362 log: `PASS L5b migrate+POST qty_out=1; no restart {"dry_run": true, "halt": false, "halt_reason": null, "qty_out": 1, "transport_state": "not_attempted"}` · `PASS L6 live-mode halted {"dry_run": false, "halt": true, "halt_reason": "m1_test_requires_explicit_dry_run", "qty_out": 0, "transport_state": "not_attempted"}` · `PASS L6b absent dry_run defaults True` · `PASS L7 interlock refuses arm; sha unchanged` · `PASS L8 IMPLICIT DISARM on expired armed_until; alive` (L1–L5a and D1–D10 also PASS) | **GO** |
| Import closure re-trace on the merge SHA | on `origin/main @ 3a1b859`: `python -m pytest tests/ops/test_c1_rail_image_manifest.py tests/ops/test_c1_signal_daemon_image_manifest.py -q` → `6 passed`; manual AST trace of `c1_rail_http_server.py`, `c1_rail_arm.py`, `c1_rail_slippage.py`, `m1_stage1_control.py` against the listener Dockerfile COPY lines → 17 modules traced, **0 missing** | **GO** |
| Restart needed after migration? | **No.** `C1SizingHostReference` holds only the three state paths (constructed once in `serve`, `c1_rail_http_server.py` 599–603); `process_signal` re-reads constants (`_read_constants`, line 296), the lifecycle multiplier (317) and the DD state (318) on every request. A2's L5b proved it in-image (`migrate+POST qty_out=1; no restart`). A5 applies the migration without a restart; the boot line is re-verified only because the deploy itself restarts the machine | **GO** |
| Approved source configured but disabled | **N/A for the listener** (no feed) | **N/A** |

### Daemon presence reads (Step 2.3, recorded now and marked pre-A1b; graded in §A4-D)

Operator-run (`& fly ssh console -a c1-signal-daemon -C "sh -c '…'"`), session-read; keys and non-secret flags only, never the token.

- `ls -la /data` → `c1_signal_daemon_config.json` (2026-08-08 04:53, 239 bytes) and `lost+found` only — **no journal** (`c1_m1_stage1_state.json`, its `.lock` and `.owner.lock` absent): A6's first-deploy case, creation at generation 0.
- `ls /app/ops/c1_signal_daemon` → `__init__.py, __main__.py, b1_payload.py, daemon.py, evaluate_loop.py, feed.py, heartbeat.py, http_status.py, listener_client.py, strategy_protocol.py` — the pre-#332 image: no `m1_stage1_*`, no `operator_input_source.py`.
- Config keys: `bar_period_s, bind_host, bind_port, emit_enabled, listener_base_url, path_token, poll_interval_s`; `emit_enabled False`; `strategy` absent; `bar_period_s 900`; **`poll_interval_s 5`**; `m1_test` absent; `listener_base_url` host `c1-rail.fly.dev`.
- **Pending write for A6 (recorded now, graded in §A4-D):** `poll_interval_s: 1` — the only value change option D needs. The A1b `load_config` defaults `strategy: "null"` and `m1_test: {enabled: false}` when absent, so no new key is required; the operator may add them explicitly to match the example config. The config's mtime (04:53:26, equal to the machine's last update) corroborates the release explanation below: the config was loaded after the failed first boot and the machine restarted.

**Release v1 `failed` with a started, healthy machine — explanation from evidence.** `fly releases -a c1-signal-daemon` shows one release, v1 `failed` at 2026-08-08 04:50; `fly machine list` shows the machine created 2026-08-08T04:50:56Z and last updated 04:53:26Z, `started`, 1/1 checks passing on `deployment-01KZFVAFXM3RTWJWVWND6W6TQ7`; the volume `vol_r1j1pglm3zpmyy9r` is attached. The daemon Dockerfile's CMD sleeps on `WAIT:` when `/data/c1_signal_daemon_config.json` is absent, and a sleeping process answers no health check, so a first deploy onto an empty volume fails Fly's release health wait while the machine itself stays up — the release is marked `failed`, then the config is loaded and the machine restarted, which is the two-and-a-half-minute gap between creation and the last update. The retained log window (2026-09-11) no longer holds the 2026-08-08 boot lines, so the `WAIT:` line itself is not retrievable; what the logs do show today is the pre-#332 image polling every 5 s and suppressing on `feed_unhealthy` (`step {'action': 'suppress', 'reason': 'feed_unhealthy'}`, one line per poll — the 2026-08-08 build logs every step; #332 added the quiet path), which also evidences `poll_interval_s = 5` on the volume. No `b1_post` line. The explanation is inference from timestamps and the CMD, stated as such; nothing in it changes A6's plan (A6 is a redeploy over a running machine whose only release reads `failed`, and its Step 2.5 expects a fresh journal at generation 0 if none exists).

### The A5 sequence (Step 2.4) — frozen for the A5 brief

```bash
# 0. Host posture FIRST (pre-condition 1). Paste with account=<redacted>. PowerShell form: & fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"     # dry_run=True armed_until=None, m1_gate … result=FAIL (expected)
# 1. Local currency: clean checkout of main at the merge SHA (pre-condition 2)
git fetch origin main && git status -sb && git rev-parse --short HEAD && git diff --stat origin/main   # HEAD == origin/main, no diff
# 2. Import closure on that SHA (pre-condition 3)
python -m pytest tests/ops/test_c1_rail_image_manifest.py -q                                    # pass; plus the manual AST trace: 0 missing
# 3. Pre-deploy in-container hashes: the running build must still be the pinned one
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "sh -c 'cd /app && sha256sum ops/c1_rail/c1_rail_arm.py ops/c1_rail/c1_rail_http_server.py ops/c1_rail/c1_rail_listener.py ops/c1_rail/c1_rail_telemetry.py ops/c1_rail/c1_sizing_host_reference.py && ls ops/c1_rail/'"   # == acceptance JSON pins; no m1_stage1_* yet
# 4. Deploy from the repo root on main at the merge SHA (documented command only)
fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile           # release v8 … complete
# 5. Boot line + health (pre-condition 5): judge by printed output
fly logs -a c1-rail --no-tail | grep -E "dry_run=|armed_until=|IMPLICIT DISARM" | tail -3           # dry_run=True armed_until=-
curl -sS https://c1-rail.fly.dev/                                                                # {"ok":true,…}
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"     # still disarmed; m1_gate result=FAIL
# 6. Post-deploy in-container hashes of every image-carried pin (pre-condition 4) + the contract hash
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "sh -c 'cd /app && sha256sum ops/c1_rail/c1_rail_arm.py ops/c1_rail/c1_rail_http_server.py ops/c1_rail/c1_rail_listener.py ops/c1_rail/c1_rail_telemetry.py ops/c1_rail/c1_sizing_host_reference.py ops/c1_rail/m1_stage1_contract.py ops/c1_rail/m1_stage1_control.py scripts/validate_c1_monitoring_acceptance.py'"
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "sh -c 'cd /app && python -c \"import sys;sys.path.insert(0,chr(111)+chr(112)+chr(115));from c1_rail.m1_stage1_contract import contract_sha256;print(contract_sha256())\"'"   # the A5 brief may give a quote-free form
sha256sum tests/ops/test_m1_acceptance_drills.py                                                 # the one pin the image does not carry: from the merge-SHA tree (record the tree's line-ending form)
# 7. Migration: plan (read-only), review the after-state, operator flat attestation, apply, no-op check (no restart needed — reads are per request)
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/m1_stage1_control.py migrate --config /data/c1_rail_config.json"                     # plan; note before.constants / before.lifecycle
#    the volume HOLDS 69/11 (§A4-L read): add --release-withdrawn iff the operator says RW = True in-session (2026-08-26 release is doctrine; the write is this session's act); without it A7 is BLOCKED at cap 81 > 80
#    read-only after-state one-liner (the CLI prints digests, not the after-state): plan_migration(c, enabled=False, release_withdrawn=RW) → leg_map cap_alloc map + lifecycle["M1 Stage1 Test"]; expect only the test row (0) and its lifecycle key (RETIRED) to differ, plus the two withdrawn rows → 0 iff RW
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/m1_stage1_control.py migrate --config /data/c1_rail_config.json --apply --flat-verified --expect-constants <before.constants> --expect-lifecycle <before.lifecycle>"   # same RW flag; backups *.m1-backup-<uuid> appear
#    re-run the plan: before digests now equal the after-state digests (noop True); lifecycle shows "M1 Stage1 Test": "RETIRED"; test row cap_alloc 0
# 8. Posture after (account redacted), then the acceptance JSON update and validator
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json                      # exit 0, CODE_LANDED
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --check-tree-skew    # reports; the CRLF-vs-LF class is named in the note
# 9. Readiness record §A5 + PR (docs only; the volume writes above are the session's recorded acts)
```

### Fixture-hash choreography (Step 2.4)

- **What is pinned today (six, refreshed 2026-08-19 in-container):** `ops/c1_rail/c1_rail_arm.py`, `c1_rail_http_server.py`, `c1_rail_listener.py`, `c1_rail_telemetry.py`, `c1_sizing_host_reference.py` (image-carried) and `tests/ops/test_m1_acceptance_drills.py` (not in the image; re-verified from the deployed commit's tree).
- **When they are hashed:** only after a real deploy, in the same session, by `sha256sum` **inside the container** under `/app` (step 6 above) — never from tree bytes, because a tree rewrite would assert a deploy that never happened (pre-condition 4; `fixture_hashes_note` 2026-08-02 and 2026-08-19). The test-file pin comes from the merge-SHA tree.
- **Line endings are part of the pin.** The 2026-08-19 pins are the deployed bytes as the Fly remote builder received them from this Windows checkout, so `--check-tree-skew` on an LF tree reports all six as skew (the 2026-08-21 note names that class as drift, not corruption). A5 deploys from the same kind of checkout; whatever bytes land in the image are what the new pins record, and the dated note says so. `contract_sha256()` is computed from Python constants, not file bytes, so it is unaffected — which is why A7 can require the two images' values to be equal.
- **What the acceptance JSON entry will say (A5, one motion with the deploy):** `code_commit_or_branch` → `origin/main @ <merge SHA> — DEPLOYED to host <date> (release v8, machine e820221a657d28, image deployment-<new>)`; `fixture_hashes` → the in-container values from step 6 for every pinned path; a dated `fixture_hashes_note` entry: host read first (`dry_run=True armed_until=None`), pre-deploy in-container hashes equal to the 2026-08-19 pins (proving the running build was the pinned one), the deploy, the post-deploy refresh, the migration applied at cap 0 / `RETIRED` (and the 69/11 release iff RW), no arm, no order, no position; `status` stays `CODE_LANDED`; item 5 and `operator_signoff` remain the only bars to `RESOLVED`.
- **Recommendation for the A5 brief (parent decides):** extend the pin set with `ops/c1_rail/m1_stage1_contract.py`, `ops/c1_rail/m1_stage1_control.py` and `scripts/validate_c1_monitoring_acceptance.py`. The contract module is load-bearing for the ceremony (A7 gates on `contract_sha256()` equality across images and A8 compares pins per file against explaining commits, since A1b's marker changes the file's bytes but not the hash inputs); the control module carries `migrate`/`preflight`/`evidence`; the validator is the interlock's schema reader inside the image. The validator iterates whatever `fixture_hashes` holds (`scripts/validate_c1_monitoring_acceptance.py` 155), so extension is mechanical.

**Return:** `DONE_WITH_CONCERNS` — every §A4-L row is GO or N/A with evidence, the A5 sequence and the hash choreography are frozen above, and the daemon presence reads are recorded pre-A1b for §A4-D. Concerns for the parent: (1) the 69/11 residue is on the listener volume — A5 needs the operator's in-session `RW = True` or A7 is `BLOCKED` at cap 81 > 80; (2) the daemon volume holds `poll_interval_s: 5` and no journal — the pending write A6 stages, recorded here for §A4-D; (3) every in-container read was operator-run because this session's permission layer blocks `fly ssh console`, and A5's in-container hash reads will meet the same block unless a read-only permission rule is added. Per-step gates: 2.1 pass · 2.2 pass · 2.3 presence reads pass (pre-A1b) · 2.4 pass · 2.5 pass. Files touched: this note only.

## §A5 — Listener deployed, disarmed; identity at cap zero (2026-09-12)

**Brief:** [A5 handoff](../../briefs/handoffs/2026-09-10-track-a-a5-claude-listener-deploy-disarmed.md) · **Currency:** clean detached worktree at `origin/main @ cf75e45` (`git status --porcelain` empty; `git diff origin/main --stat` empty; `git cat-file -e 31fd642^{tree}` OK — full history) · **Authority used:** `fly deploy` under the 2026-08-02 grant (run by the session from the clean checkout), read-only Fly commands, and the in-container commands below, which the operator ran in their own console because this session's permission layer blocks `fly ssh console` (output read from the Terminal panel; `--status` pastes carry `account=<redacted>`). **No `--arm`, no `--acknowledge-m1-unresolved`, no `--enable-test`, no POST, no daemon change.**

### 2.1 Host read first (pre-condition 1)

`python ops/c1_rail/c1_rail_arm.py --status` → `current: dry_run=True armed_until=None equity_source='crosstrade' equity_field='balance.netLiq' destination='tradovate' account=<redacted> bind_host='0.0.0.0' bind_port=8080` · `m1_gate: status='CODE_LANDED' result=FAIL`. Gate met.

### 2.2 Pre-deploy in-container hashes

`sha256sum` in `/app` of the five pins → `923e0847…`, `711980e8…`, `d3b16b3e…`, `471e28da…`, `93992da9…` — **all five equal the acceptance JSON's 2026-08-19 pins**: the running build was the pinned v7. Ledger: 32 records, last `seq 32` (`transport_result`) — A6's "no signal on boot" baseline. `ls ops/c1_rail/` showed no `m1_stage1_*` file (expected pre-deploy).

### 2.3 Import closure (pre-condition 3)

On `cf75e45`: `python -m pytest tests/ops/test_c1_rail_image_manifest.py -q` → `4 passed`; manual AST trace of `c1_rail_http_server.py`, `c1_rail_arm.py`, `c1_rail_slippage.py`, `m1_stage1_control.py` against the listener Dockerfile COPY lines → 17 modules traced, **0 missing**.

### 2.4 Operator flatness attestation

Recorded verbatim, in-session, before Step 2.7: **"RW = True, no open positions 8:07 PM CDT"** (2026-09-12 01:07 UTC). The operator was asked to glance at Tradovate again immediately before running the apply block and did not report a position.

### 2.5 Deploy (pre-condition 2)

From the repo root of the clean `cf75e45` checkout: `fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile` → image `registry.fly.io/c1-rail:deployment-01M29JA2721JHQGCXCRNCF54G1` (`sha256:02ca9a12f935adb21e5adc4fd033352f0c8c05b52d7661b2484902f3f792447e`, 40 MB), rolling update of machine `e820221a657d28`, smoke and machine checks passed, DNS verified. `fly releases` → **v8 `complete`** (v7 2026-08-19 is now the rollback target named in §A3 item 4).

### 2.6 Boot line + health (pre-condition 5)

`fly logs` 2026-09-12T01:05:07–08Z: `Preparing to run: sh -c if [ ! -f /data/c1_rail_config.json ] …` (the `WAIT:` guard, config present so it fell through) → `WARNING c1_rail_http: DRY_RUN=true - will compute and audit, never call CrossTrade` → **`c1 rail HTTP adapter listening on http://0.0.0.0:8080/c1/<redacted>  dry_run=True armed_until=- equity_source=crosstrade`**; the port-bind race printed one `Health check … has failed` line at 01:05:08 and `is now passing` in the same second (the 2026-08-19 precedent, benign). `curl -sS https://c1-rail.fly.dev/` → `{"ok":true,"service":"c1_rail_http_server"}`. In-container `--status` after the deploy → identical to 2.1. No `ModuleNotFoundError`, no `IMPLICIT DISARM` (there was nothing to disarm).

### 2.7 Migration at cap zero — `RW = True`

Operator ruling recorded before the plan: **`RW = True`** (the volume held Striker's 69/11; the 2026-08-26 ADR released them; the volume write is this session's act). Reads first, then one write, all with `--release-withdrawn`:

- **Plan (CLI, read-only):** `migrate --config /data/c1_rail_config.json --release-withdrawn` → `applied: false`, `enabled: false`, `before.constants` `32a783304e8f307fae0ba0be2d25c023ae0cecf9ff5b889b5691faf0c05f084c`, `before.lifecycle` `6e29f44ba0f380e2a46524b631720599cb6027607fc2de5463bbc54a420aee05`, `contract_sha256` `346387e5…9d94f`. *Brief skew, not a defect:* the CLI's result dict does not print `release_withdrawn` (only `applied`, `enabled`, `before`, `contract_sha256`); the after-state read below does.
- **After-state (same function, read-only, `release_withdrawn=True`):** `release_withdrawn: true`; the same two `before` digests; `after.constants` = `tier Tradeify_Select_100K`, `E_firm 100000`, `cap_firm 80`, `cost_per_side_usd 0.91`, `leg_map` = `dj30_mym {base_risk 0.007, cap_alloc 0, dollars_per_pt 0.5, leg_key Striker, pyr_pct 750.0}` · `nas100_mnq {base_risk 0.0037, cap_alloc 0, dollars_per_pt 2.0, leg_key Striker NAS100, pyr_pct 1000.0}` · **`m1_stage1_test {base_risk 1.25e-05, cap_alloc 0, dollars_per_pt 0.5, leg_key M1 Stage1 Test, pyr_pct 0.0}`** (the contract's `constants_row(enabled=False)`); `after.lifecycle` = `{M1 Stage1 Test: RETIRED, Striker: WATCH-1, Striker NAS100: WATCH-1}`. Reviewed by the parent: differs from the volume only by the new test row at 0, the two withdrawn rows 69 → 0 and 11 → 0, and the added lifecycle key.
- **Apply:** `migrate --config /data/c1_rail_config.json --release-withdrawn --apply --flat-verified --expect-constants 32a78330… --expect-lifecycle 6e29f44b…` → `applied: true` with the same `before` digests and contract hash (the apply re-plans from its own flags and would have refused on any drift). Backups written 2026-09-12 01:33 UTC: `c1_sizing_constants.json.m1-backup-d440a68c-31f2-4438-8805-b804880ca1cd` (442 bytes) and `lifecycle_state.json.m1-backup-d440a68c-31f2-4438-8805-b804880ca1cd` (57 bytes).
- **No-op check** (plan re-run with `release_withdrawn=True`, after-state compared to the files) → `noop True`. Re-read: `cap_alloc` = **`{dj30_mym: 0, m1_stage1_test: 0, nas100_mnq: 0}`**; `lifecycle_state.json` = `{"M1 Stage1 Test": "RETIRED", "Striker": "WATCH-1", "Striker NAS100": "WATCH-1"}`. The 69/11 residue §A4-L flagged is released; A7's enable plan (test row → 1) now sums to 1 ≤ 80.
- **No restart:** §A4-L established that the sizing host re-reads constants, lifecycle and DD state on every request (A2 L5b proved it in-image), so none was issued.

### 2.8 Preflight refusal (expected)

`python ops/c1_rail/m1_stage1_control.py preflight --config /data/c1_rail_config.json` → `M1 control refused: invalid, changed, unavailable or unapproved inputs`, non-zero exit — cap 0 / `RETIRED` cannot size one micro. Nothing was enabled to change that.

### 2.9 Post-deploy in-container hashes (pre-condition 4)

`sha256sum` in `/app` after the deploy (operator-run; the terminal wraps 64-hex lines, so each value was reassembled and corroborated against the merge-SHA tree in both byte forms — every image pin reproduced exactly):

| Pinned file | In-container sha256 (v8) | Tree form at `cf75e45` | Explaining commits since `31fd642` |
|---|---|---|---|
| `ops/c1_rail/c1_rail_arm.py` | `723f1bf3349b0b0ec4c7d7b77d01057fb5ba62a0a5756a46a9ef0fd228e524bd` | LF | none (line-ending move only: `ops/c1_rail/*.py` now carry `text eol=lf`; the 2026-08-19 pins were CRLF) |
| `ops/c1_rail/c1_rail_http_server.py` | `9e62727078ea585c2fdc39fc82455ae2747f58031f7b36410746da6a56517984` | LF | none (line endings) |
| `ops/c1_rail/c1_rail_listener.py` | `a31b8869c1d1b2736ac63cf90c467295bc26a6c2a47eadae45b015496210c1c7` | LF | `509b524` (#332) |
| `ops/c1_rail/c1_rail_telemetry.py` | `45151defe6e747b96c0eaec64c6d348fbbddcfc9efbd8a05ef2f92638c37c93b` | LF | none (line endings) |
| `ops/c1_rail/c1_sizing_host_reference.py` | `5f10481b0d9474ad2bf37462ab64e606baa6065b097708de3f726d891da6a868` | LF | `509b524`, `25711e2`, `da084bc` |
| `ops/c1_rail/m1_stage1_contract.py` (new pin) | `35e4a72bbb036a3d9570f439f6abc2735dbcd4537006c60fd9560f3096466651` | LF | `811df7c`, `509b524` (#332), `36b3996` (#349) |
| `ops/c1_rail/m1_stage1_control.py` (new pin) | `7c5a9b15be989e7596fdf1344470dd50082ec4ac6e446085ee335e98c944ece1` | LF | `811df7c`, `509b524`, `36b3996` |
| `scripts/validate_c1_monitoring_acceptance.py` (new pin) | `452a52ab4c2606569c7ff31e4fece8897ac07d79545304682095439ea14d54c4` | **CRLF** (no eol attribute; shipped as checked out on Windows) | none |
| `tests/ops/test_m1_acceptance_drills.py` (not in the image) | `104dafa8cc3cf236cb88e2c4b929fffa0b72aa45e797723a88d9077afe7b8bbd` = LF blob at `cf75e45` (CRLF form `786009cc…`) | tree-backed by design (A2 L2) | `25711e2` (2026-08-26 cap release) — moved from the `31fd642` pin `bf91071b…` with an explaining commit |

In-container `contract_sha256()` → `346387e565225d956da0f5b9696f211dee82ff9a823dda6e56b0ce32aba9d94f` (equals the tree value; unchanged by A1b's marker). `ls ops/c1_rail/` now lists `m1_stage1_contract.py` and `m1_stage1_control.py`.

### 2.10 Acceptance JSON refresh

`docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`: `fixture_hashes` → the nine values above (pin set extended per §A4-L with the two Stage 1 modules and the validator); `code_commit_or_branch` → `origin/main @ cf75e45 — DEPLOYED to host 2026-09-12 01:05 UTC (machine e820221a657d28, image deployment-01M29JA2721JHQGCXCRNCF54G1, …, release v8)`; `fixture_hashes_note` → a `SKEW CLOSED 2026-09-12` entry prepended (host read first, pre-deploy pins matched, closure re-traced, documented command, boot line, in-container refresh, byte forms, RW = True, final caps); `notes[]` → a dated A5 entry. **`status` stays `CODE_LANDED`.** Validator: exit 0 (`OK status=CODE_LANDED`); `--check-tree-skew` → `tree skew: none — all 9 pinned file(s) match this tree` (on this Windows worktree the validator is CRLF and the `ops/` files LF, matching the image; an LF checkout will report the validator pin as skew, which the note explains); `--require-resolved` → exit 1 as expected (status, the event id and `operator_signoff` still owed).

### 2.11 Stop

Final in-container `--status` → `dry_run=True armed_until=None … m1_gate: status='CODE_LANDED' result=FAIL`. No arm, no signal, no order, no position.

**Return:** `DONE_WITH_CONCERNS` — every gate met and every §4 limb held (boot line disarmed; preflight refused; every image-carried pin read in-container). Concerns, none blocking: (1) the A5 brief describes the CLI plan output as printing `release_withdrawn`; it does not (the after-state read carries it) — a brief text skew for the parent; (2) every in-container command was operator-run because this session cannot invoke `fly ssh console`, so the transcript evidence is the Terminal panel read by the session; (3) the ledger `seq` was read pre-deploy only (32); A6 Step 2.1 re-reads it as its own baseline. Per-step gates: 2.1–2.11 pass. Files touched: the acceptance JSON and this note.

## §A4-D — Daemon readiness (2026-09-12, second dispatch of the A4 brief)

**Brief:** [A4 handoff](../../briefs/handoffs/2026-09-10-track-a-a4-claude-deployment-readiness-review.md) Steps 2.3b/2.4b · **Preconditions:** A1r and A1b merged (`fa02a13`), A2-D green on that merge SHA (push run [34660963201](https://github.com/Joshua-Asante/first-passage/actions/runs/34660963201)), A5 DONE (§A5, #352 `133f043`) · **Currency:** `origin/main @ 133f043` · **Authority used:** read-only — non-ssh Fly reads and local tests by the session; in-container reads operator-run in their own console (this session's permission layer blocks `fly ssh console`), output read from the Terminal panel; no write to either volume, no restart, no deploy.

### Fresh host reads (Step 2.3 re-run; `--status` account token redacted)

Operator-run 2026-09-12 (PowerShell, two `fly ssh console` calls on one line), session-read from the Terminal panel.

- Listener `--status` → `current: dry_run=True armed_until=None equity_source='crosstrade' equity_field='balance.netLiq' destination='tradovate' account=<redacted> bind_host='0.0.0.0' bind_port=8080` · `m1_gate: status='CODE_LANDED' result=FAIL`. Ledger: 32 records, last `seq 32` (`transport_result`) — unchanged since §A4-L and through the A5 deploy, so the v8 boot produced no request.
- Daemon `/data`: `c1_signal_daemon_config.json` (2026-08-08 04:53, 239 bytes) and `lost+found` only — **no journal**, no `.lock`, no `.owner.lock`.
- Daemon `/app/ops/c1_signal_daemon`: the pre-#332 file set (`__init__.py, __main__.py, b1_payload.py, daemon.py, evaluate_loop.py, feed.py, heartbeat.py, http_status.py, listener_client.py, strategy_protocol.py`) — the 2026-08-08 build still runs; its health JSON has the old field set (`ok, last_bar_age_s, feed_healthy, emit_enabled, connected`) and it logs a `suppress` step every 5 s.
- Daemon config keys `bar_period_s, bind_host, bind_port, emit_enabled, listener_base_url, path_token, poll_interval_s`; `emit_enabled False`; `strategy` absent; `bar_period_s 900`; **`poll_interval_s 5`**; `m1_test` absent; `listener_base_url` host `c1-rail.fly.dev`. Unchanged since §A4-L.

### Daemon checklist (Step 2.3b)

| Item | How evidenced | GO / NO-GO (owner) |
|---|---|---|
| Listener still `dry_run=true`, `armed_until` None | fresh `--status`, above | **GO** |
| A2-D green on the A1b merge SHA | push run [34660963201](https://github.com/Joshua-Asante/first-passage/actions/runs/34660963201) on `fa02a13`: `PASS D1 … D11`; D2 `COPY exact; no databento; extras match {"expected": [], "extras": []}` (no `requirements.txt` on `main`); D6 `prepare/enable/inject exit 2; hashes unchanged; no input files` — the three-refusal form the A1b PR specified, run without `PYTHONPATH`; D11 `one receipt; one transport_unknown; matching bar hash; cleanup; close/barrier; no values` | **GO** |
| Daemon import closure re-trace on the merge SHA | on `133f043`: `python -m pytest tests/ops/test_c1_signal_daemon_image_manifest.py -q` → `2 passed`; manual AST trace of `daemon.py`, `m1_stage1_control.py`, `evaluate_loop.py`, `__main__.py` against the daemon Dockerfile COPY lines → 15 modules (`operator_input_source.py` included), **0 missing**; `.dockerignore` and the Dockerfile both re-include the new module; no `deploy/c1_signal_daemon/requirements.txt` | **GO** |
| Approved source configured but disabled | **Pending write, reviewed here (the expected case: no sub-track before A6 writes the daemon volume).** Keys the A1b `load_config` requires: `listener_base_url`, `path_token`, `bind_host`, `bind_port`, `bar_period_s`, `emit_enabled`, `poll_interval_s`; optional with defaults `strategy` (`"null"`) and `m1_test` (`{"enabled": false}`). Secret: `path_token` only. Non-secret values to stage: `emit_enabled false`, `strategy "null"`, `m1_test.enabled false` (with `state_path /data/c1_m1_stage1_state.json`), `bar_period_s 900` (`prepare` sets 60 for a ceremony), `listener_base_url` unchanged (host `c1-rail.fly.dev`), and **`poll_interval_s: 1`** — the one value change option D needs (the volume holds 5, and `run_daemon` caches the interval at startup, so it must be staged before the deploy, never after). Operator confirmation in-session, verbatim: "I hold the daemon path_token and will do the A6 put myself." | **GO** — pending write recorded; the operator holds the secret and performs the put at A6 Step 2.2b |
| Credential values at rest only on the daemon volume | `git grep` on `main` for a literal 32+ character value after `path_token` outside test fixtures → none (every hit is a key name, a key list or a placeholder); the running daemon's health JSON `{"ok": true, "last_bar_age_s": null, "feed_healthy": false, "emit_enabled": false, "connected": true}` (the 2026-08-08 build's field set) carries no token-like string; a sampled `fly logs` window carries none; §A4-L's config read printed key names only | **GO** |
| Journal state | fresh read above: `/data/c1_m1_stage1_state.json` absent (the volume holds only the config and `lost+found`) — the first-deploy case; A6 Step 2.5 expects `CeremonyStore.boot()` to create it at `generation 0`, `enabled false`, `active null`, with the `.lock` marker reading `initialized`. No unresolved checkpoint can exist where no journal exists | **GO** |
| Two apps, two volumes | `fly volumes list`: `c1_rail_data` `vol_vxm828pzmlzyn7j4` on `e820221a657d28`; `c1_signal_daemon_data` `vol_r1j1pglm3zpmyy9r` on `840759c2474928`; `deploy/c1_signal_daemon/fly.toml` mounts `c1_signal_daemon_data` only; one machine per app | **GO** |
| Rollback image known | §A3 item 4: `registry.fly.io/c1-signal-daemon:deployment-01KZFVAFXM3RTWJWVWND6W6TQ7` (`sha256:8e3a8f68…`), the source-free 2026-08-08 build; the v1 `failed` release with a running machine explained in §A4-L from timestamps and the `WAIT:` CMD (config loaded 04:53:26, then a restart) | **GO** |
| Listener ledger baseline for "no signal on boot" | `seq 32` (`transport_result`), read fresh above; A6 Step 2.5 compares after its deploy | **GO** |
| Exact A6 command sequence reviewed | written below (Step 2.4b) | **GO** |

### The A6 sequence (Step 2.4b) — frozen for the A6 brief

Deploy from the repo root of a clean checkout of `main` at the merge SHA recorded at A6 time (any `main` at or after `fa02a13` carries A1b; `133f043` traced clean above). PowerShell forms are given where the operator runs the command; the `MSYS_NO_PATHCONV=1 fly ssh console …` forms in the A6 brief are the Git Bash equivalents.

```bash
# 0. Listener posture first (pre-condition 1) + ledger baseline — operator-run; paste with account=<redacted>
& fly ssh console -a c1-rail -C "sh -c 'cd /app; python ops/c1_rail/c1_rail_arm.py --status; echo ==LEDGER; python -c ""import json,sys;l=[x for x in open(sys.argv[1]).read().splitlines() if x.strip()];r=json.loads(l[-1]);print(len(l),{k:r.get(k) for k in sys.argv[2:]})"" /data/c1_rail_events.jsonl seq kind'"
#    gate: dry_run=True armed_until=None; record seq (A4-D read: see above)
# 1. Daemon pre-reads (Step 2.3 set)
fly status -a c1-signal-daemon; fly releases -a c1-signal-daemon | head -3; fly logs -a c1-signal-daemon --no-tail | tail -20; curl -sS https://c1-signal-daemon.fly.dev/
& fly ssh console -a c1-signal-daemon -C "sh -c 'ls -la /data; echo ==APP; ls /app/ops/c1_signal_daemon; echo ==CFG; python -c ""import json,sys;from urllib.parse import urlsplit;c=json.load(open(sys.argv[1]));print(sorted(c));print({k:c.get(k) for k in sys.argv[2:6]});m=c.get(sys.argv[6]);print(sys.argv[6], m.get(sys.argv[7]) if isinstance(m,dict) else m);print(urlsplit(str(c.get(sys.argv[8]))).hostname)"" /data/c1_signal_daemon_config.json emit_enabled strategy bar_period_s poll_interval_s m1_test enabled listener_base_url'"
#    gate (A6 §0.5): no journal on the volume (first-deploy case), or a journal with no unresolved checkpoint
# 2. Step 2.2b — stage the config (OPERATOR performs every step that touches the value)
#    a. prepare c1_signal_daemon_config.json LOCALLY from deploy/c1_signal_daemon/c1_signal_daemon_config.fly.example.json:
#       listener_base_url https://c1-rail.fly.dev · path_token = the value already on the volume (operator-held) · bind_host 0.0.0.0 · bind_port 8080
#       bar_period_s 900 · emit_enabled false · strategy "null" · m1_test {"enabled": false, "state_path": "/data/c1_m1_stage1_state.json"} · poll_interval_s 1
#    b. shape check locally on the merge-SHA checkout (PowerShell; prints keys and the four non-secret values, never the token):
python -c "import sys;sys.path.insert(0,sys.argv[1]);from c1_signal_daemon.daemon import load_config;from pathlib import Path;c=load_config(Path(sys.argv[2]));print(sorted(c), c[sys.argv[3]], c[sys.argv[4]], c[sys.argv[5]][sys.argv[6]], c[sys.argv[7]])" ops <local path> emit_enabled strategy m1_test enabled poll_interval_s
#       PRE-DEPLOY GATE: the last value printed must be 1; anything else is not put
#    c. put:  fly ssh sftp shell -a c1-signal-daemon   →   put <local path> /data/c1_signal_daemon_config.json   → then delete the local copy
#    d. verify in-container, keys and flags only (the step-1 CFG one-liner again) → poll_interval_s 1, emit_enabled False, strategy null, m1_test enabled False
#       (the running pre-A1b daemon holds its boot-time config and is unaffected until the deploy restarts it)
# 3. Import closure on the merge SHA (pre-condition 3)
python -m pytest tests/ops/test_c1_signal_daemon_image_manifest.py -q     # + the manual trace: 0 missing
# 4. Deploy (pre-condition 2) from the repo root on main at the merge SHA — session-run (fly deploy is permitted; fly ssh is not)
fly deploy . --config deploy/c1_signal_daemon/fly.toml --dockerfile deploy/c1_signal_daemon/Dockerfile     # release v2 … complete
# 5. Verify inert (pre-condition 5)
fly logs -a c1-signal-daemon --no-tail | tail -40      # `daemon up bind=0.0.0.0:8080 emit_enabled=false boot_id=…`; no b1_post / m1_b1_post; no connect line
curl -sS https://c1-signal-daemon.fly.dev/             # poll_interval_s:1, emit_enabled false, effective_emit false, strategy "NullStrategy", feed_mode "operator_input", connected false, feed_healthy false, ceremony_state "DISABLED", boot_id new
& fly ssh console -a c1-signal-daemon -C "sh -c 'cd /app; python ops/c1_signal_daemon/m1_stage1_control.py status --state /data/c1_m1_stage1_state.json; echo ==STATE; python -c ""import json,sys;o=json.load(open(sys.argv[1]));print({k:o.get(k) for k in sys.argv[2:]}, sorted(o.get(sys.argv[7],{})))"" /data/c1_m1_stage1_state.json schema_version generation enabled active boot_id ceremonies; ls -la /data'"
#    gates: status effective_emit false, source_status disconnected; state file created FRESH — schema_version 1, generation 0, enabled False, active None, ceremonies {} — and .lock marker + .owner.lock present (no journal existed before: A4-D read); no m1_upload_* / m1_bar_* / m1_claim_* files
& fly ssh console -a c1-rail -C "sh -c 'python -c ""import json,sys;l=[x for x in open(sys.argv[1]).read().splitlines() if x.strip()];print(len(l),json.loads(l[-1]).get(sys.argv[2]))"" /data/c1_rail_events.jsonl seq'"    # seq unchanged vs step 0 → no signal on boot
fly logs -a c1-signal-daemon --no-tail | tail -30      # 60 s after boot: no `step ` lines (quiet path)
# 6. Record §A6; commit on claude/*; PR. STOP before any ceremony preparation.
```

**Return:** `DONE` — every §A4-D row GO with evidence; the A6 sequence is frozen above; the only volume change A6 needs is the `poll_interval_s: 1` staging the operator performs. Per-step gates: 2.3 (fresh reads) pass · 2.3b pass · 2.4b pass · 2.5 pass. Files touched: this note only. Second dispatch of the A4 brief complete; the A4 box in the plan closes with this section.
