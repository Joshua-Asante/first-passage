# Claude handoff — Track A / A4: deployment-readiness review (listener half now, daemon half after A1b)

**Type:** cc_handoff (read-only host review + governed note; no deploy)
**Date:** 2026-09-10
**Status:** listener half dispatches after A2-L is green and A3 is DONE; daemon half after A1b merges and A2-D is green
**Spawn target:** Claude Code (local session with `fly` auth; operator present for the flatness attestation)
**Parent:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3
**Authority:** read-only. `fly ssh console -C` is used only for reads; nothing is written to either volume; no restart; no deploy. Private values (Net Liq, tokens, account ids) are read for presence/shape and never transcribed.

## 0. Rule 0 reads (Phase 0 — report before any host read)

Currency: `git fetch origin main`; record the SHA (authoring-time `47972f6`). Hard check for `ops/c1_rail/m1_stage1_contract.py` on `origin/main`, else `NEEDS_CONTEXT`. Read the A2 return (workflow run URL) and `docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md` §A3 (A3's return); if either is missing, `NEEDS_CONTEXT`.

- `.claude/skills/c1-rail/SKILL.md` §Agent-session authority (the six pre-conditions; `fly ssh` Windows exit-code quirk; `MSYS_NO_PATHCONV=1` for `/data` args).
- `deploy/c1_rail/README.md` (deploy command; "Refresh `fixture_hashes` … from hashes read IN-CONTAINER"), `deploy/c1_signal_daemon/README.md`, both Dockerfiles, `.dockerignore`.
- `ops/c1_rail/c1_rail_arm.py` (`--status` output; `DEFAULT_ACCEPTANCE_PATH` in-image), `ops/c1_rail/c1_rail_http_server.py` (`_REQUIRED_CONFIG`; whether constants/lifecycle are read per request — locate `_read_constants` call sites in `c1_sizing_host_reference.py` and say whether a restart is needed after migration).
- `ops/c1_rail/m1_stage1_control.py` (`plan_migration` — what it changes; `--release-withdrawn` semantics: only when rows still hold 69/11; `preflight` — read-only, uses the live equity GET when `equity_source=crosstrade`), `ops/c1_rail/m1_stage1_contract.py` (frozen tuple, `constants_row`, `contract_sha256`).
- `docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md` — "Frozen identity and sizing" table and "Readiness and review".
- `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` — `fixture_hashes` (the six 2026-08-19 in-container pins), `host_config_note` (which volume keys exist), the 2026-08-19 and 2026-08-21 skew notes.
- `docs/adr/2026-08-26-striker-legmap-cap-release.md` — the 0/0 release; `ops/c1_rail/c1_sizing_host_reference.py` `LEG_MAP` cap values on main.
- `ops/c1_signal_daemon/daemon.py` (`load_config` required keys; `build_loop`), `ops/c1_signal_daemon/m1_stage1_state.py` (`CeremonyStore.boot` behaviour on an existing state file; `.lock` marker), `ops/c1_signal_daemon/http_status.py` (health keys).
- Fly, read-only (paste printed output): `fly releases -a c1-rail`, `fly status -a c1-rail`, `fly logs -a c1-rail` (last boot line), and the same for `c1-signal-daemon`; `fly volumes list -a <app>` for both.

## 0.5. Clarifications (halt on ambiguity)

- The daemon volume config contains `path_token`. Never `cat` it. Read keys and non-secret flags only through an in-container one-liner that prints `sorted(cfg)` and the values of `emit_enabled`, `strategy`, `bar_period_s`, `poll_interval_s`, `m1_test.enabled`, `listener_base_url`'s host part. If the one-liner cannot run on the old image (pre-#332 image has no `m1_test` defaults), print keys only.
- If the listener's `--status` shows anything other than `dry_run=True` with `armed_until=None`, stop: this is the track-level stop rule (`BLOCKED — plan-itself-wrong`), not a checklist item.
- If the A2 workflow is green but its L5b/L6 evidence lines are not in the log, treat A2 as not done and return `NEEDS_CONTEXT`.

## 1. Context and deliverable

Two deploys are ahead (A5 listener, A6 daemon). Each is a risk event on a live broker-linked host. This review establishes, from host reads and the A2/A3 returns, whether every A5 (and later A6) precondition is evidenced — and names the owner of every item that is not. No deploy happens here.

**Deliverable:** append **§A4-L — Listener readiness** (and later **§A4-D — Daemon readiness**) to `docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md`: a table `item → evidence (command + printed line, redacted) → GO / NO-GO (owner)`, followed by the **exact A5 command sequence** the parent will freeze into the A5 brief, and the **fixture-hash choreography** (which files are pinned, when they are hashed, what the acceptance JSON entry will say).

**Not asked:** deploying, restarting, migrating, editing any volume file, editing the acceptance JSON, or running `preflight` with the test row enabled.

## 2. Execution plan

### Step 2.1 — Listener host reads (all read-only)

Run and paste, redacting values that are private:

```bash
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python -c \"import json;c=json.load(open('/data/c1_rail_config.json'));print(sorted(c));print({k:c.get(k) for k in ('dry_run','armed_until','equity_source','destination','account' if False else 'bind_port')})\""
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "cat /data/lifecycle_state.json"
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python -c \"import json;c=json.load(open('/data/c1_sizing_constants.json'));print(c.get('tier'),c.get('E_firm'),c.get('cap_firm'));print({k:v.get('cap_alloc') for k,v in c['leg_map'].items()})\""
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python -c \"import json,math;d=json.load(open('/data/c1_dd_state.json'));p=d.get('peak_equity');print(type(p).__name__, isinstance(p,(int,float)) and math.isfinite(p) and p>0)\""
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python -c \"import json;print(json.load(open('/data/c1_execution_state.json')))\""
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "sh -c 'ls -la /data; tail -c 600 /data/c1_rail_events.jsonl'"
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "sh -c 'cd /app && sha256sum ops/c1_rail/c1_rail_arm.py ops/c1_rail/c1_rail_http_server.py ops/c1_rail/c1_rail_listener.py ops/c1_rail/c1_rail_telemetry.py ops/c1_rail/c1_sizing_host_reference.py && ls ops/c1_rail/'"
```

Gate: `dry_run=True`, `armed_until=None`; the five in-container hashes equal the acceptance JSON's pins (proves the running build is still the 08-19 one); `ls ops/c1_rail/` shows **no** `m1_stage1_*` files (expected: not yet deployed); constants `leg_map` cap values recorded (69/11 residue or 0/0); execution state shows no confirmed base; ledger tail parses and the last `seq` is recorded (A6's "no signal on boot" baseline).

### Step 2.2 — Listener checklist (fill every row)

| Item | How evidenced | GO/NO-GO |
|---|---|---|
| `dry_run=true` on host | `--status` line | |
| `armed_until` None | `--status` line | |
| Account broker-verified flat | operator states it in-session from Tradovate ("No open positions") with time; recorded as an attestation, not agent-observed | |
| Test identity migration exact and limited to one micro | `plan_migration` reasoning from code: only the `m1_stage1_test` row + lifecycle key change; `cap_alloc` 0 at A5; `cap_alloc` ≤ 1 ever; `--release-withdrawn` needed iff the volume still holds 69/11 (from 2.1) | |
| Existing allocations reconciled | sum of `cap_alloc` ≤ 80 after the plan; residue disposition named (release under the 2026-08-26 ADR, operator-confirmed in A5) | |
| Rollback image known | §A3 | |
| Fixture-hash choreography specified | written in this section (2.4) | |
| Exact deployment commands reviewed | written in this section (2.4) | |
| A2-L green with L5b/L6/L7/L8 evidence | run URL + quoted lines | |
| Import closure re-trace on the merge SHA | `pytest tests/ops/test_c1_rail_image_manifest.py -q` locally on `origin/main` + manual `sys.modules` trace of `c1_rail_http_server`, `c1_rail_arm`, `c1_rail_slippage`, `m1_stage1_control` against the COPY lines: 0 missing | |
| Restart needed after migration? | from 2.0 code read (per-request vs cached) | |
| Approved source configured but disabled | **N/A for the listener** (no feed); recorded as such | |

### Step 2.3 — Daemon host reads (daemon half; also do the presence reads now and mark "pre-A1b")

```bash
fly releases -a c1-signal-daemon; fly status -a c1-signal-daemon; fly logs -a c1-signal-daemon | tail -40
curl -sS https://c1-signal-daemon.fly.dev/
MSYS_NO_PATHCONV=1 fly ssh console -a c1-signal-daemon -C "sh -c 'ls -la /data; ls /app/ops/c1_signal_daemon'"
MSYS_NO_PATHCONV=1 fly ssh console -a c1-signal-daemon -C "python -c \"import json;c=json.load(open('/data/c1_signal_daemon_config.json'));print(sorted(c));print(c.get('emit_enabled'),c.get('strategy'),c.get('bar_period_s'),c.get('poll_interval_s'),(c.get('m1_test') or {}).get('enabled'))\""
```

Explain the **v1 `failed` release with a started, healthy machine** from evidence only (release history, logs, whether the config existed at first boot, whether a manual restart followed). Record: image ref, machine id, whether `/data/c1_m1_stage1_state.json` exists (pre-#332 image: expected absent), `emit_enabled` value.

### Step 2.4 — Freeze the A5 sequence and the hash choreography

Write, as a fenced block, the exact ordered commands for A5 (host `--status` read → local currency check → import-closure test → pre-deploy in-container hashes → `fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile` from the repo root on `main` at the merge SHA → boot line + health → post-deploy in-container `sha256sum` of the six pinned files plus `ops/c1_rail/m1_stage1_contract.py`, `ops/c1_rail/m1_stage1_control.py`, `scripts/validate_c1_monitoring_acceptance.py` → `contract_sha256()` in-image → migration plan/apply → `--status` → acceptance JSON update → validator). Recommend extending the pin set with the two `m1_stage1_*` listener modules and say why (the contract hash is load-bearing for the ceremony); the parent decides in the A5 brief.

### Step 2.5 — Write the note and verify

```bash
grep -n -i -E "netliq|token|secret" docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md   # no values
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json   # untouched
git diff --stat origin/main...HEAD   # expect: the one note
```

Commit on `claude/*`, push, PR.

## 4. Falsifiable hypothesis

**H:** every A5 precondition can be evidenced from host reads plus the A2 and A3 returns without a deploy, and the running listener build is still the 2026-08-19 pinned build.
**Reject** if any item lacks evidence → that row is NO-GO with an owner; if the in-container hashes do not match the pins, the running build is unknown → NO-GO for A5 until explained. **Ambiguous** if the operator cannot attest flatness now → the row stays open and A5 cannot start.

## 5. Forbidden moves

- Any write to either volume, any restart, any deploy — tempting for "just fix the stale config"; A5 owns writes.
- `cat` of the daemon config or the listener config (tokens); transcribing `peak_equity` or any equity figure.
- Running `preflight` with the test row enabled (A7 owns that) or running a migration apply.
- Grading an item GO on the strength of a document rather than a host read.
- Editing the acceptance JSON.

## 6. Gate and return taxonomy

RESOLVED = every listener row GO (daemon rows may read "pre-A1b" for the first dispatch). FALSIFIED = a row is NO-GO for a reason A5 cannot fix (report). AMBIGUOUS = operator attestation or A2/A3 inputs missing.

Return exactly one of `DONE` · `DONE_WITH_CONCERNS` (any NO-GO) · `NEEDS_CONTEXT` · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`, with branch, PR URL, the checklist table, and the frozen A5 command block.

## 7. Parent-session review

Pass 1 — spec compliance: reads only; one note appended; no volume writes in the transcript. Pass 2 — quality: hashes compared to the JSON pins by the parent; the v1-failed explanation rests on quoted log lines; the A5 sequence matches the README and the skill's six pre-conditions in order. Pass 3 — consolidated read of §A3 + §A4 together before A5 is authored.

## 10. Audit hooks

```bash
grep -n "^## §A4\|^## A4\|GO\b\|NO-GO" docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md | head -40
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
python -c "import json;d=json.load(open('docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json'));print(json.dumps(d['fixture_hashes'],indent=1))"
```
