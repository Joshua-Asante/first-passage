# Operator + Claude handoff — Track A / A7: the attended Stage 1 dry-run (one ceremony)

**Type:** cc_handoff (multi-step; attended; the operator runs `enable`)
**Date:** 2026-09-10
**Status:** dispatch only when A3, A5, and A6 are DONE, the A1 decision is ratified and implemented (A1b), and the operator is at the console for the whole window
**Spawn target:** Claude Code (local console session with `fly` auth) with the operator present
**Parent:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3
**Authority:** the listener stays `dry_run=true`; the sender is never invoked; exactly one ceremony; the operator enables it. The agent runs read-only preflight, `prepare`, verification, and `close`. **No `--arm`. No hand-POST. No retry.**

## 0. Rule 0 reads (Phase 0 — report before touching either host)

Currency: `git fetch origin main`; SHA recorded. At authoring time (2026-09-10) `origin/main` was `47972f6` and PR #332 head `811df7c`; the ceremony code cited below is that PR's `811df7c` revision. Hard checks: `ops/c1_rail/m1_stage1_contract.py` on main; A1b source module on main; readiness record §A3–§A6 present, else `NEEDS_CONTEXT`. Anchor every file below with `git log -1 --format=%h -- <path>` in the report.

- `docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md` — "Frozen identity and sizing" (why `expected_qty` is exactly 1 under normal and 40 % DD sizing; "Smaller DD multipliers are not covered"), "Retained offline components" (the journal's one-shot semantics), "Readiness and review".
- `ops/c1_signal_daemon/m1_stage1_control.py` — `validate_manifest` (fields: `ceremony_id` `[A-Za-z0-9_-]{1,80}`, `target` UTC minute with `second == 0`, `60 < expires − target ≤ 150`, `contract_sha256`, `expected_qty == 1`, `preflight_sha256` 64-hex, `source` == the approved marker), `prepare` (unresolved-history barrier; writes `emit_enabled=false`, `strategy=m1_stage1_test`, `bar_period_s=60`, READY), `enable` (identical reviewed manifest, same boot, generation match; flips `emit_enabled=true`), `close`, `safe_status`.
- `ops/c1_signal_daemon/m1_stage1.py` — `before_poll` (`_active` conditions; expiry closes), `accept_bar` (`bar.ts == target`, `60 ≤ now − bar.ts ≤ 150`, OHLC sanity), `reserve` (durable claim: `EVALUATED` → `SEND_RESERVED`, `enabled` flips false **before** the POST), `outcome` (`EMITTED` → `RESPONSE_RECORDED`, `dry_run_computed` classification), `close_attempt`.
- `ops/c1_signal_daemon/m1_stage1_strategy.py` — the hook fires only on the target bar with `bar_time = "m1-" + digest(ceremony_id, target, contract_sha256, source)`.
- `ops/c1_rail/m1_stage1_control.py` — `migrate --enable-test` (cap 1, `AUTHORIZED`), `preflight` (read-only; refuses unless `qty_out == 1` and `submit`), `project_evidence` (the join: `request_received.body_sha256 == request_sha256`, `order_id == m1_stage1_test-entry-<event>`, decision `qty_out 1 / halt false / dry_run true / test_only true / sender_invoked false / test_contract_sha256`, transport `not_attempted`; output fields).
- `ops/c1_rail/c1_rail_listener.py` — the test-identity guard and the `decision` payload fields written for this identity.
- The A1b brief / README section — how the approved source is activated by the manifest's `source` marker and delivers the target bar; its own pre-checks.
- `.claude/skills/c1-rail/SKILL.md` §Verification — host reads; Windows `fly ssh` exit-code quirk.
- CME Globex hours for MYM (the target minute must be inside a trading session and outside the daily maintenance break); the operator names the window.

## 0.5. Clarifications (halt on ambiguity)

- `target` selection: the operator names a UTC minute at least 5 minutes ahead, inside a Globex session; `expires = target + 120 s`. If the source's delivery latency (per the A1b brief) cannot guarantee arrival inside `[target + 60 s, target + 150 s]`, stop and return `NEEDS_CONTEXT` — do not widen the window in code.
- If `preflight` returns anything other than `expected_qty: 1`, the ceremony does not proceed (track stop rule). Return the receipt, disable the allocation again, and stop.
- If the daemon journal shows any unresolved checkpoint from an earlier attempt, no new ceremony; `BLOCKED — plan-itself-wrong`.
- The evidence projection needs the listener ledger and the daemon state on one filesystem. Default: `fly ssh sftp get` both files into the session scratchpad (never into the repo) and run the projection locally; delete the copies after the return is written.

## 1. Context and deliverable

M1 item 5 requires a real strategy signal from the ruled host that reaches the listener and produces a structured dry-run decision at expected non-zero sizing. Everything is deployed and inert. This session runs exactly one ceremony under the operator's hand and records the genuine listener event UUID. It does **not** edit the acceptance artifact (A8).

**Deliverables:** (1) the ceremony evidence — the projection JSON (public-safe fields), the listener event UUID, ceremony id, target minute, contract hash, request digest; (2) readiness record §A7; (3) allocation disabled again, listener disarmed, daemon `effective_emit=false` — all host-verified after; (4) PR with (2).

**Not asked:** editing `M1_MONITORING_ACCEPTANCE.json`; a second ceremony; any arm; any order.

## 2. Execution plan (gates are binary; any miss stops the session)

### Step 2.1 — Pre-checks
Listener `--status` → `dry_run=True`, `armed_until=None`, `m1_gate … result=FAIL` (expected). Daemon `GET /` → `effective_emit:false`, `ceremony_state:"DISABLED"`; `status` CLI healthy; record daemon `boot_id`. Both `contract_sha256()` values (listener image, daemon image) printed in-container → **must be equal**. Listener ledger last `seq` recorded.

### Step 2.2 — Enable the allocation
Operator flatness attestation (Tradovate "No open positions", time). `migrate --config /data/c1_rail_config.json --enable-test` plan → review: only the test row (`cap_alloc` 1) and lifecycle (`AUTHORIZED`) change → `--apply --flat-verified --expect-constants … --expect-lifecycle …`. Verify; restart the listener only if A4 established that constants are cached (then `--status` first).

### Step 2.3 — Read-only sizing preflight
`python ops/c1_rail/m1_stage1_control.py preflight --config /data/c1_rail_config.json` → JSON with `expected_qty:1`, `dry_run:true`, `armed_until:null`, `sizing_only:true`, `preflight_sha256`. Gate: exactly 1. Record `preflight_sha256`.

### Step 2.4 — Manifest
Write the manifest on the daemon volume (`/data/m1_manifest_<ceremony_id>.json`) with: fresh `ceremony_id` (e.g. `stage1-<YYYYMMDD>-1`), `target`, `expires` (= target + 120 s), `contract_sha256` (from 2.1), `expected_qty: 1`, `preflight_sha256` (from 2.3), `source` = the approved marker verbatim from the A1b brief. Paste it (no private values inside).

### Step 2.5 — Prepare (agent)
`python ops/c1_signal_daemon/m1_stage1_control.py prepare --state /data/c1_m1_stage1_state.json --config /data/c1_signal_daemon_config.json --boot-id <boot_id> --manifest /data/m1_manifest_<id>.json` → exit 0; `status` → `state:"READY"`, `effective_emit:false`. Health still `effective_emit:false`.

### Step 2.6 — Enable (operator)
Agent drafts the exact command; the **operator** runs it in their own `fly ssh console -a c1-signal-daemon`: `python ops/c1_signal_daemon/m1_stage1_control.py enable --state … --config … --boot-id <boot_id> --manifest /data/m1_manifest_<id>.json --ceremony-id <id>`. Health → `effective_emit:true`, `ceremony_state:"READY"`, source activates per the A1b brief. Time stamp recorded.

### Step 2.7 — The event
Watch `fly logs -a c1-signal-daemon` through `target + 150 s`. Expected: exactly one `m1_b1_post status=200`; journal → `RESPONSE_RECORDED` with `response_kind:"dry_run_computed"`; `enabled` already false (flipped at reservation). If `target_missed` / `expired` closes the ceremony with no POST: record it, `close`, disable the allocation (2.10), and return `DONE_WITH_CONCERNS` — a second attempt is a new session with a fresh ceremony id, never a retry here. If `TRANSPORT_UNKNOWN`: stop, do not retry, return `BLOCKED — plan-itself-wrong` (reconciliation is a separate review).

### Step 2.8 — Listener triad
In-container on `c1-rail`, find the three ledger lines for the request (`grep <request_sha256>` from the journal's `request_sha256`, then the `event_id`): `request_received` (`auth_ok` true, `body_category` `b1_json`, `parsed.leg_id` `m1_stage1_test`, `bar_time` `m1-…`), `decision` (`qty_out` 1, `halt` false, `dry_run` true, `test_only` true, `sender_invoked` false, `test_contract_sha256` = contract), `transport_result` (`not_attempted`, `dry_run` true). Exactly **one** `request_received` with that `body_sha256`. Operator confirms CrossTrade Alert History shows no new entry and Tradovate shows no order/position for the window.

### Step 2.9 — Close
`close --ceremony-id <id>` → journal `CLOSED` with `previous_state:"RESPONSE_RECORDED"`; config `emit_enabled:false`, `m1_test.enabled:false`; health `effective_emit:false`.

### Step 2.10 — Disable the allocation, reconfirm posture
`migrate` (no `--enable-test`) plan → apply with `--flat-verified` and the current preimage hashes → cap 0, `RETIRED`. Listener `--status` → disarmed. Daemon health → `effective_emit:false`, `emit_enabled:false`.

### Step 2.11 — Evidence projection
Fetch the two files per §0.5; run `python ops/c1_rail/m1_stage1_control.py evidence --events <events.jsonl> --daemon-state <state.json> --ceremony-id <id>` → JSON with `listener_event_id` (the UUID), `expected_qty:1`, `observed_qty:1`, `dry_run:true`, `sender_invoked:false`, `post_test_emit_enabled:false`, and the source-qualification fields as the ratified A1 amendment defines them. Record the UUID. Delete the scratch copies.

### Step 2.12 — Record and return
Append §A7 to the readiness record: UUID, ceremony id, target, contract hash, request digest, timestamps (enable, POST, close), the triad's field values, both post-checks. No bar values, no equity, no token. Commit on `claude/*`, push, PR.

## 4. Falsifiable hypothesis

**H:** with the allocation at one micro and the listener disarmed, the approved source delivers the target bar in-window, the evaluate hook emits exactly one B1 POST, and the listener records a dry-run decision with `qty_out=1` and the sender never invoked.
**Reject** if `qty_out ≠ 1`, if the sender was invoked, if any CrossTrade/Tradovate artefact appears, or if more than one request for the ceremony exists → `FALSIFIED`; disable, disarm-reconfirm, record. **Ambiguous** if no bar arrived in-window or transport is unknown → recorded as such; no acceptance claim.

## 5. Forbidden moves

- A second ceremony, a re-POST, or any retry after an uncertain send — the journal's barrier exists for this; do not look for a way around it.
- Hand-POSTing a payload to the listener to "help" (canned = DEAD-list; it would also poison the uniqueness join).
- Editing the journal, the manifest after `prepare`, or the volume configs by hand.
- Running `enable` as the agent.
- Populating `dry_run_strategy_signal_event_id` (A8).
- Leaving the allocation at cap 1 or the ceremony config enabled after the session.
- `--arm`, under any wording.

## 6. Gate and return taxonomy

RESOLVED = §4 H held; UUID recorded; both post-checks green. FALSIFIED = a reject fired. AMBIGUOUS = no bar / unknown transport.

Return exactly one of `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`, with the UUID, ceremony id, the projection JSON, the three triad lines (redacted), the enable/POST/close timestamps, and the PR URL.

## 7. Parent-session review

Pass 1 — spec compliance: one ceremony; `enable` run by the operator (transcript shows the agent drafting, not running); allocation back to zero; no acceptance edit. Pass 2 — quality: parent re-runs the projection from the retained host files and re-greps the ledger for the UUID (expects exactly three lines); parent confirms the manifest's `source` marker equals the ratified amendment's. Pass 3 — consolidated read of §A5–§A7.

## 10. Audit hooks

```bash
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "sh -c 'grep -c <listener_event_id> /data/c1_rail_events.jsonl'"   # expect 3
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
curl -sS https://c1-signal-daemon.fly.dev/
MSYS_NO_PATHCONV=1 fly ssh console -a c1-signal-daemon -C "python ops/c1_signal_daemon/m1_stage1_control.py status --state /data/c1_m1_stage1_state.json"
```
