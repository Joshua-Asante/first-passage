# Claude handoff — Track A / A6: deploy the signal daemon, still inert

**Type:** cc_handoff (multi-step; live-adjacent surface; agent deploy under the 2026-08-02 grant)
**Date:** 2026-09-10
**Status:** dispatch only when A1b is merged, A2-D is green on that image, A4-D is all GO, and A5 is DONE
**Spawn target:** Claude Code (local session with `fly` auth; clean checkout of `main` at the merge SHA)
**Parent:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3
**Authority:** `fly deploy` and read-only commands. **No `prepare`, no `enable`, no ceremony manifest, no source activation.** The daemon must come up with emission disabled and the approved source disconnected.

## 0. Rule 0 reads (Phase 0 — report before any host action)

Currency: `git fetch origin main`; SHA recorded; tree clean and equal to `origin/main`. At authoring time (2026-09-10) `origin/main` was `47972f6`, PR #332 head `811df7c`, and the daemon host ran the 2026-08-08 image `deployment-01KZFVAFXM3RTWJWVWND6W6TQ7` on machine `840759c2474928`. Hard checks: `ops/c1_rail/m1_stage1_contract.py` on main; the A1b source module named in the A1b brief present on main; the S2b build ADR carries the ratified A1 addendum (status no longer PROPOSED). Anchor every file below with `git log -1 --format=%h -- <path>` in the report.

- `docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md` §A3, §A4-D, §A5 — rollback image, the v1-failed explanation, the config keys read, the listener ledger's last `seq` baseline (from A4/A5). Missing → `NEEDS_CONTEXT`.
- The A1b brief and its merged PR — the approved source's `feed_mode` when disconnected, its config keys, its secret handling, and the expected health JSON at boot.
- `deploy/c1_signal_daemon/README.md`, `deploy/c1_signal_daemon/Dockerfile`, `.dockerignore` — deploy command and COPY set on the merge SHA.
- `ops/c1_signal_daemon/daemon.py` (`load_config` — what an enabled-shaped stale config does at boot; `build_loop`), `ops/c1_signal_daemon/m1_stage1_state.py` (`CeremonyStore.boot` on an existing state file: closes READY/DISABLED ceremonies with `boot_changed`, increments `generation`; refuses to re-initialize when the `.lock` marker exists), `ops/c1_signal_daemon/m1_stage1_control.py` (`status` JSON), `ops/c1_signal_daemon/http_status.py`.
- `tests/ops/test_c1_signal_daemon_image_manifest.py` — run on the merge SHA.
- `.claude/skills/c1-rail/SKILL.md` §Agent-session authority — pre-conditions scoped to the daemon app (1/4/5/6 are listener-specific; still read the listener `--status` first as the README asks).

## 0.5. Clarifications (halt on ambiguity)

- If the daemon volume already holds `/data/c1_m1_stage1_state.json` with any ceremony in an unresolved state (`EVALUATED`/`SEND_RESERVED`/`EMITTED`/`TRANSPORT_UNKNOWN`, including under `CLOSED.previous_state`): do not deploy; return `BLOCKED — plan-itself-wrong` (track stop rule; reconciliation is a separate review).
- If the A1b image needs a new config key on the volume (a credential or endpoint), the value is supplied by the operator in-session and written with a one-liner that never echoes it; if the operator is absent, `NEEDS_CONTEXT`.
- If the deploy's health wait fails on the `WAIT:` guard even though the config exists, do **not** apply a command override (the 2026-07-31 residual class); investigate logs and return.

## 1. Context and deliverable

The daemon app runs the 2026-08-08 build under a release Fly marks `failed`. The A1b image carries the approved input, disconnected by default, plus the one-shot ceremony. This deploy lands it inert and proves inertness from the host: no emission, no ceremony, no source connection, no POST at boot.

**Deliverables:** (1) daemon at the new release; (2) host-verified inert state; (3) readiness record §A6 (image, release, machine, health snapshot without secrets, state-file summary); (4) PR with (3).

**Not asked:** any ceremony step; any listener change; enabling anything.

## 2. Execution plan

### Step 2.1 — Listener disarm reconfirm
`MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"` → `dry_run=True`, `armed_until=None`. Record the listener ledger's last `seq`.

### Step 2.2 — Daemon pre-read
`fly status`, `fly releases`, `fly logs | tail -40`, `curl -sS https://c1-signal-daemon.fly.dev/`; in-container `ls -la /data`; state-file summary via a one-liner printing `boot_id`, `generation`, `enabled`, `active`, ceremony states (never manifests' private fields); config keys + non-secret flags. Gate: §0.5 first bullet clear.

### Step 2.3 — Import closure
`pytest tests/ops/test_c1_signal_daemon_image_manifest.py -q` on the merge SHA; manual `sys.modules` trace of `daemon.py` and `m1_stage1_control.py` against the COPY lines. Gate: 0 missing.

### Step 2.4 — Deploy
From the repo root on `main` at the merge SHA: `fly deploy . --config deploy/c1_signal_daemon/fly.toml --dockerfile deploy/c1_signal_daemon/Dockerfile`. Paste the summary. Gate: release complete (v2 or later shows `complete`).

### Step 2.5 — Verify inert
- `fly logs` → `daemon up bind=… emit_enabled=false boot_id=…`; no `b1_post` / `m1_b1_post` lines; no source-connect lines.
- `curl -sS https://c1-signal-daemon.fly.dev/` → `emit_enabled:false`, `effective_emit:false`, `strategy:"NullStrategy"`, `connected:false`, `feed_healthy:false`, `ceremony_state:"DISABLED"`, `feed_mode` = the A1b-defined disconnected value, `boot_id` new.
- In-container `python ops/c1_signal_daemon/m1_stage1_control.py status --state /data/c1_m1_stage1_state.json` → `effective_emit:false`.
- State file: `enabled:false`, `active:null`, `generation` = previous + 1, prior ceremonies (if any) closed with `boot_changed` tombstones, `.lock` marker intact.
- Listener side: last ledger `seq` unchanged vs 2.1 → **no signal on boot**.
- Over 60 s of logs: no `step ` lines (inert quiet path).

### Step 2.6 — Record and stop
Append §A6 to the readiness record; commit on `claude/*`, push, PR. Final `--status` on the listener pasted. Stop before any ceremony preparation.

## 4. Falsifiable hypothesis

**H:** the A1b daemon image boots on the host with emission disabled, the source disconnected, the one-shot journal valid, and no listener request generated.
**Reject** if any health field above differs, if the listener ledger gained a `request_received`, or if the boot log shows a connect or POST → close nothing, touch nothing, roll back to the §A3 image, return `FALSIFIED`. **Ambiguous** if the journal shows an unresolved checkpoint → `BLOCKED`.

## 5. Forbidden moves

- `prepare`, `enable`, writing a manifest, or activating the source — each is the next lane's first step.
- Deleting or editing `/data/c1_m1_stage1_state.json`, its `.lock`, or `.owner.lock`.
- A command override to get past a failed health wait.
- Mounting or reading the listener volume from the daemon app.
- Echoing the `path_token` or any credential.
- Deploying the pre-A1b (source-free) image "as an interim" without the operator asking for it in-session.

## 6. Gate and return taxonomy

RESOLVED = release complete and every inert check evidenced. FALSIFIED = §4 reject (rolled back). AMBIGUOUS = unresolved journal or missing A1b inputs.

Return exactly one of `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`, with release number, machine id, image ref, deployed SHA, the health JSON (redacted), the state-file summary, and the PR URL.

## 7. Parent-session review

Pass 1 — spec compliance: no ceremony commands in the transcript; no listener changes; no journal edits. Pass 2 — quality: parent curls the health endpoint and reads the listener `seq` itself. Pass 3 — consolidated read of §A5 + §A6 before A7 is authored.

## 10. Audit hooks

```bash
curl -sS https://c1-signal-daemon.fly.dev/
fly releases -a c1-signal-daemon | head -3
MSYS_NO_PATHCONV=1 fly ssh console -a c1-signal-daemon -C "python ops/c1_signal_daemon/m1_stage1_control.py status --state /data/c1_m1_stage1_state.json"
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "sh -c 'tail -c 300 /data/c1_rail_events.jsonl'"
```
