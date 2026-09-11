# Claude handoff — Track A / A5: deploy the listener, still disarmed

**Type:** cc_handoff (multi-step; live-safety surface; agent deploy under the 2026-08-02 grant)
**Date:** 2026-09-10
**Status:** dispatch only when A2-L is green, A3 is DONE, and A4-L is all GO; operator present for the flatness attestation
**Spawn target:** Claude Code (local session with `fly` auth; clean checkout of `main` at the merge SHA)
**Parent:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3
**Authority:** `fly deploy` and read-only commands, per the c1-rail skill §Agent-session authority. **No `--arm`, no `--acknowledge-m1-unresolved`, no `--enable-test`, no test signal.** Disarm is not expected to be needed; if it is, flat first.

## 0. Rule 0 reads (Phase 0 — report before any host action)

Currency: `git fetch origin main`; record the SHA; `git status --porcelain` empty; `git diff origin/main --stat` empty (the build context is the working tree — it must be byte-identical to the reviewed commit). At authoring time (2026-09-10) `origin/main` was `47972f6`, PR #332 head `811df7c`, and the host ran release v7 from `31fd642`. Hard check for `ops/c1_rail/m1_stage1_contract.py` on `origin/main`. Anchor every file below with `git log -1 --format=%h -- <path>` in the report.

- `docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md` §A3 and §A4-L — the frozen command sequence, the hash choreography, the rollback image, the operator's flatness attestation row. Missing → `NEEDS_CONTEXT`.
- `.claude/skills/c1-rail/SKILL.md` §Agent-session authority — the six pre-conditions, in order, per app.
- `deploy/c1_rail/README.md` — the deploy command and the "refresh `fixture_hashes` … IN-CONTAINER" paragraph; `deploy/c1_rail/Dockerfile` — the COPY set now including `m1_stage1_contract.py` / `m1_stage1_control.py`.
- `ops/c1_rail/c1_rail_arm.py` — `--status` shape; `ops/c1_rail/m1_stage1_control.py` — `migrate` plan/apply flags, backups, `--release-withdrawn` guard, `preflight` refusal text when sizing is unavailable.
- `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` — `fixture_hashes`, `fixture_hashes_note`, `code_commit_or_branch`, `notes[]` — the fields this sub-track updates; `scripts/validate_c1_monitoring_acceptance.py` — `--check-tree-skew` semantics.
- `tests/ops/test_c1_rail_image_manifest.py` — run it on the merge SHA before deploying.

## 0.5. Clarifications (halt on ambiguity)

- If `--status` shows `dry_run=False` or a non-null `armed_until`: the armed-host procedure (Track A plan §6) runs before anything else and the deploy does not happen. Read the boot line in `fly logs` as well (the running process holds its boot-time config). Ask the operator to attest flatness from Tradovate; **without the operator present do not disarm** (disarm blocks exits and would orphan an open position) — alert and return `BLOCKED — plan-itself-wrong` naming the state. With flatness attested: `python ops/c1_rail/c1_rail_arm.py --disarm`, then `fly machine restart <machine id> -a c1-rail` (the disarm takes effect only on restart), verify the boot line reads `dry_run=True armed_until=-` and `--status` agrees, record every command in the readiness record, then return `BLOCKED — plan-itself-wrong`. Finding the hazard and leaving it in place is not an option.
- If pre-deploy in-container hashes differ from the acceptance JSON pins, the running build is not the one on record → stop and return; do not deploy over an unknown build.
- If the A4 plan shows the volume still holds 69/11 caps, `--release-withdrawn` is used only if the operator says so in-session (the 2026-08-26 release is doctrine; the volume write is this session's act). Write the operator's answer down as `RW = True` or `RW = False` **before** Step 2.7 and use that one value in every plan read, the no-op check, and the apply. Consequence the operator must hear before answering: with the residue left in place the account-aggregate cap is fully allocated (69 + 11 = 80), so A7's enable plan (test row at 1 → 81) will raise `m1_test_account_cap_exhausted` and A7 cannot run; a `False` here is an open operator decision that A5 records in §A5 and returns as `DONE_WITH_CONCERNS`. If the residue is anything other than exactly 69/11 or 0/0, `plan_migration` refuses (`withdrawn allocation changed; reconcile separately`) — stop and return `BLOCKED — plan-itself-wrong`.
- If the Phase 0 code read shows constants/lifecycle are cached at boot, a `fly machine restart` follows the migration — preceded by a fresh `--status` read.

## 1. Context and deliverable

The listener image on the host is the 2026-08-19 build; main has moved (2026-08-21 skew note) and PR #332 added the test identity, the listener-side guard, and the migration tooling to the image. This deploy lands that image, applies the identity at **cap zero / `RETIRED`**, and refreshes the deployed-bytes pins — and stops.

**Deliverables:** (1) listener at the new release, disarmed; (2) migration applied at cap 0 / `RETIRED`; (3) acceptance JSON updated from in-container hashes with a dated note (status stays `CODE_LANDED`); (4) readiness record §A5; (5) PR with (3)+(4).

**Not asked:** enabling the test allocation; any ceremony; daemon changes; arming.

## 2. Execution plan (order is the six pre-conditions)

### Step 2.1 — Host read first (pre-condition 1)
`MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"` → paste **with the `account=…` token replaced by `account=<redacted>`** — `_PRINTABLE` in `c1_rail_arm.py` includes `account`, the identifier is private (plan §1 invariant 10), and the acceptance secret scanner does not catch it; this applies to every `--status` paste in this brief. Gate: `dry_run=True`, `armed_until=None`, `m1_gate: status='CODE_LANDED' result=FAIL`.

### Step 2.2 — Pre-deploy in-container hashes
`sha256sum` of the five deployed `ops/c1_rail/*.py` pins in `/app` → must equal the acceptance JSON pins. Record the last ledger `seq` (`tail -c 400 /data/c1_rail_events.jsonl`).

### Step 2.3 — Import closure (pre-condition 3)
`pytest tests/ops/test_c1_rail_image_manifest.py -q` on the merge SHA; then a manual trace: import `c1_rail_http_server`, `c1_rail_arm`, `c1_rail_slippage`, `m1_stage1_control` locally with the image's `sys.path` shape and diff first-party `sys.modules` paths against the Dockerfile COPY lines. Gate: 0 missing.

### Step 2.4 — Operator flatness attestation
Operator states Tradovate "No open positions" with time. Recorded verbatim. Gate: present before Step 2.7.

### Step 2.5 — Deploy (pre-condition 2)
From the repo root on `main` at the merge SHA: `fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile`. Paste the summary. Gate: release complete.

### Step 2.6 — Boot line + health (pre-condition 5)
`fly logs -a c1-rail` → boot line `dry_run=True armed_until=- equity_source=crosstrade`; `curl -sS https://c1-rail.fly.dev/` → `{"ok":true,...}`; `--status` in-container → same as 2.1. The ~1 s port-bind race warning from fly-proxy is benign (08-19 precedent); a `ModuleNotFoundError` is not — roll back to the §A3 image and return `FALSIFIED`.

### Step 2.7 — Migration at cap zero
Two reads, then one write, all parameterized on the one value `RW` fixed in §0.5 (`True` only when the volume holds 69/11 **and** the operator authorized the release in-session; otherwise `False`). (1) `python ops/c1_rail/m1_stage1_control.py migrate --config /data/c1_rail_config.json` plus `--release-withdrawn` iff `RW` (plan; no `--enable-test`) → prints `applied:false`, `enabled`, `release_withdrawn`, `before` (the two preimage digests) and `contract_sha256` — it does **not** print the after-state. (2) The after-state comes from the same pure function the CLI uses, called read-only in-container with the **same flags** the apply will use; substitute `RW` literally (`True`/`False`) for `<RW>`:

```bash
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python -c \"import json,sys;sys.path.insert(0,'ops/c1_rail');import m1_stage1_control as m;c=m._read('/data/c1_rail_config.json');p=m.plan_migration(c,enabled=False,release_withdrawn=<RW>);print(json.dumps({k:p[k] for k in ('enabled','release_withdrawn','before','contract_sha256','after')},indent=1,sort_keys=True))\""
```

`plan_migration` reads the constants and lifecycle files, mutates in-memory copies, validates, and returns; it writes nothing. Its `after` holds the full constants JSON (tier, firm constants, `leg_map` rows) and the lifecycle map — no secrets, no account figures — so paste it unredacted. Review: the printed `release_withdrawn` equals `RW`; `after.constants.leg_map` differs from the current file only by the added `m1_stage1_test` row with `cap_alloc` 0 and, iff `RW`, the two withdrawn rows at 0; `after.lifecycle` differs only by `M1 Stage1 Test: RETIRED`; the `before` digests equal those the CLI printed. Then `--apply --flat-verified --expect-constants <before.constants> --expect-lifecycle <before.lifecycle>` **with `--release-withdrawn` iff `RW`** — the apply recomputes the plan from its own flags and refuses if they do not reproduce the reviewed inputs, so a flag mismatch here is a refusal, not a silent different write. Verify: backups `*.m1-backup-*` present; re-run read (2) with the same `<RW>` and check the no-op property in-container:

```bash
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python -c \"import json,sys;sys.path.insert(0,'ops/c1_rail');import m1_stage1_control as m;c=m._read('/data/c1_rail_config.json');p=m.plan_migration(c,enabled=False,release_withdrawn=<RW>);print('noop', p['after']['constants']==json.load(open(c['constants_path'])) and p['after']['lifecycle']==json.load(open(c['lifecycle_state_path'])))\""
```

Expect `noop True` (the files now equal the plan's after-state; applying again would change nothing). Record in §A5 the final `leg_map` cap values by leg (0/0/0 after a release; 69/11/0 if the operator declined, with the A7 consequence named). If a restart is required (per §0.5), `--status` read, then `fly machine restart e820221a657d28`-class command with the current machine id, then 2.6 again.

### Step 2.8 — Preflight refusal (expected)
`python ops/c1_rail/m1_stage1_control.py preflight --config /data/c1_rail_config.json` → expect exit 1 with the refusal line (cap 0 / `RETIRED` cannot size one micro). This confirms the allocation is genuinely zero. Do not enable anything to make it pass.

### Step 2.9 — Post-deploy in-container hashes (pre-condition 4)
`sha256sum` in `/app` of the five deployed pins (`ops/c1_rail/c1_rail_arm.py`, `c1_rail_http_server.py`, `c1_rail_listener.py`, `c1_rail_telemetry.py`, `c1_sizing_host_reference.py`) plus `ops/c1_rail/m1_stage1_contract.py`, `ops/c1_rail/m1_stage1_control.py`, `scripts/validate_c1_monitoring_acceptance.py`. The sixth pin, `tests/ops/test_m1_acceptance_drills.py`, is **not in the image** (the Dockerfile copies no `tests/`; A2's L2 asserts that): hash it from the checked-out merge-SHA tree and compare to the existing pin `bf91071b…`, recording which byte form matched (LF blob via `git show <sha>:tests/ops/test_m1_acceptance_drills.py | sha256sum`, or working-tree bytes). Then `python -c "import sys;sys.path.insert(0,'ops/c1_rail');import m1_stage1_contract as m;print(m.contract_sha256())"` in-container. Paste all.

### Step 2.10 — Acceptance JSON update (repo, on a `claude/*` branch)
- `fixture_hashes`: the in-container values from 2.9 (extend the pin set with the two `m1_stage1_*` listener modules if A4 recommended it; keep `tests/ops/test_m1_acceptance_drills.py` re-verified against the tree as the 08-19 entry did).
- `code_commit_or_branch`: `origin/main @ <merge SHA> — DEPLOYED to host <date time UTC> (machine …, image …, release vN)`.
- `fixture_hashes_note`: prepend a dated `SKEW CLOSED <date>` entry in the established style (host state read first; import closure re-traced; deployed via the documented command; boot line; hashes read in-container after the deploy).
- `notes[]`: a dated entry — what was deployed, migration applied at cap 0 / `RETIRED`, preflight refusal expected, no arm / no signal / no order, host-verified before and after. **`status` stays `CODE_LANDED`.**
- Run: `python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` (exit 0) and `--check-tree-skew` (paste what it prints; CRLF vs LF is expected and the note already explains it).
- Append §A5 to the readiness record. Commit, push, PR.

### Step 2.11 — Stop
Final `--status` read pasted. No arm. No signal.

## 4. Falsifiable hypothesis

**H:** the merge-SHA listener image boots disarmed on the host, the identity lands at cap zero with the sizing host refusing to size it, and the deployed bytes are pinned from in-container reads.
**Reject** if the boot line is not `dry_run=True armed_until=-`, if `preflight` sizes anything, or if the hash of any pin the image carries (the `ops/c1_rail/*.py` and `scripts/` pins) had to come from the tree instead of an in-container read → roll back / stop and return `FALSIFIED`. The one non-image pin, `tests/ops/test_m1_acceptance_drills.py`, is tree-backed by design (Step 2.9) and is outside this clause. **Ambiguous** if the pre-deploy hashes do not match the record → stop before deploying.

## 5. Forbidden moves

- `--arm`, `--acknowledge-m1-unresolved`, hand-editing `/data/c1_rail_config.json`, `--enable-test`, any POST to the listener — each is one step away and each is out of scope.
- Deploying from a dirty tree, a worktree not at the merge SHA, or any branch but `main`.
- Refreshing any image-carried pin in `fixture_hashes` from tree bytes (the non-image test pin is verified from the merge-SHA tree, as the 2026-08-19 refresh did).
- `--release-withdrawn` without the operator's in-session yes.
- "Fixing" a dead CMD by editing the Dockerfile in this session (that is an A2 finding; roll back instead).
- Touching the daemon app or its volume.
- Scaling either app beyond one machine.

## 6. Gate and return taxonomy

RESOLVED = every step's gate met, `--status` disarmed after, pins refreshed in-container, PR open. FALSIFIED = §4 reject fired (rolled back; record what happened). AMBIGUOUS = a precondition input missing.

Return exactly one of `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`, with: release number, machine id, image ref, deployed SHA, the before/after `--status` lines, the migration plan digest, the PR URL.

## 7. Parent-session review

Pass 1 — spec compliance: no `--enable-test`; no POST; the JSON diff touches only the named fields; status still `CODE_LANDED`. Pass 2 — quality: parent re-reads `--status` on the host; parent compares the JSON pins to a fresh in-container `sha256sum`; the notes entry matches the transcript. Pass 3 — consolidated read of the deploy transcript + JSON diff + readiness §A5.

## 10. Audit hooks

```bash
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "sh -c 'cd /app && sha256sum ops/c1_rail/*.py scripts/validate_c1_monitoring_acceptance.py'"
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --check-tree-skew
fly releases -a c1-rail | head -3
```
