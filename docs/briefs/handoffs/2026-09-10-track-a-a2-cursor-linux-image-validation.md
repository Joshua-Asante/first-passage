# Cursor handoff — Track A / A2: Linux image validation for the c1 listener and daemon

**Type:** cc_handoff (frozen-spec implementation; Cursor variant with recommended defaults)
**Date:** 2026-09-10
**Status:** dispatch after PR #332 and PR #334 are merged; re-run the daemon half after A1b merges
**Spawn target:** Cursor (or Codex) — `cursor/*` branch, PR, no merge
**Parent:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3 · parent re-runs the workflow and reviews
**Authority:** no Fly access, no deploy, no secrets. This PR adds a GitHub Actions workflow and a script; it changes no image, no `ops/` code, and no acceptance artifact.

## 0. Rule 0 reads (Phase 0 — post the read-report before writing code)

Currency: `git fetch origin main`; record the SHA. At authoring time `origin/main` was `47972f6` and PR #332 head `811df7c`. Hard check: `git ls-tree --name-only origin/main ops/c1_rail/ | grep m1_stage1_contract.py` must hit, else `NEEDS_CONTEXT`.

- `deploy/c1_rail/Dockerfile`, `deploy/c1_signal_daemon/Dockerfile`, `.dockerignore` — the COPY sets and the CMD `WAIT:` guards. Report both COPY lists verbatim.
- `deploy/c1_rail/README.md`, `deploy/c1_signal_daemon/README.md`, `deploy/c1_rail/c1_rail_config.fly.example.json`, `deploy/c1_signal_daemon/c1_signal_daemon_config.fly.example.json` — config shapes.
- `ops/c1_rail/c1_rail_http_server.py` — `_REQUIRED_CONFIG`, `load_config` (implicit disarm on expired `armed_until`; `path_token` ≥ 32 chars and no `REPLACE` prefix; `equity_source` values), `startup_log_line`, `do_GET` body, `_respond` (200 `dry_run: computed, not sent`).
- `ops/c1_rail/c1_rail_arm.py` — `--status` output shape (`m1_gate: status=… result=…`), `plan_arm` refusal text.
- `ops/c1_rail/m1_stage1_control.py` — `migrate` (plan vs `--apply --flat-verified --expect-constants --expect-lifecycle`), `atomic_write` (POSIX dir-fsync branch).
- `ops/c1_rail/m1_stage1_contract.py`, `ops/c1_rail/c1_rail_listener.py` (test-identity guard: `dry_run` must be exactly `True` for `m1_stage1_test`; reasons `m1_test_requires_explicit_dry_run`, `m1_test_entry_only`).
- `ops/c1_signal_daemon/daemon.py` (`load_config`, `build_loop` inert by design, `run_daemon`), `ops/c1_signal_daemon/m1_stage1_state.py` (`DaemonOwnership` non-blocking flock, `CeremonyStore.locked/boot`, `atomic_json` with `os.O_DIRECTORY` fsync), `ops/c1_signal_daemon/m1_stage1_control.py` (`main` returns 2 for prepare/enable; `status` JSON), `ops/c1_signal_daemon/listener_client.py` (`default_transport` 30 s timeout, `_NoRedirect`), `ops/c1_signal_daemon/http_status.py` (health JSON keys).
- `tests/ops/test_c1_rail_image_manifest.py`, `tests/ops/test_c1_signal_daemon_image_manifest.py` — the existing static COPY-subset guards this workflow complements.
- `tests/ops/test_m1_stage1_integration.py`, `tests/ops/test_c1_signal_daemon_m1.py` (fixtures `prepared`, `manifest`, `cfg`, `NOW`) — the construction of an emitting loop for the timeout check.
- `.github/workflows/tests.yml` — job conventions (checkout, python setup, ripgrep install).

Anchor each with `git log -1 --format=%h -- <path>`.

## 0.75. Local-only dependency check

`N/A for cloud dispatch — no gitignored vendor data, no secrets.` Every config this workflow uses is a placeholder committed under `tests/fixtures/c1_image_validation/`; `path_token` values are ≥ 32 random-looking ASCII characters that do not start with `REPLACE`; `equity_source` is `file`. GitHub Actions `ubuntu-latest` has Docker.

## 0.5. Clarifications — parent-recommended defaults (apply unless Phase 0 contradicts; then bounce `NEEDS_CONTEXT` quoting the conflict)

- (A) **Where tests run.** Default: focused suites run in a plain `python:3.12-slim` container with the repo bind-mounted read-only and `pytest` installed at run time; additionally, the subset whose imports resolve inside each **built** image runs there with `tests/` bind-mounted and `pytest` installed into an ephemeral container (never into the Dockerfiles). Report which files ran where; a test whose imports fail in-image is reported, not forced.
- (B) **How to get `qty_out=1` for the listener check.** Default: apply the migration in-container with `--enable-test` on the throwaway `/data` (plan first to obtain the `--expect-*` preimage hashes). Do not hand-edit constants.
- (C) **Timeout check construction.** Default: build the emitting loop exactly as `tests/ops/test_m1_stage1_integration.py` does, substituting the real `default_transport` and a local listening-but-silent socket. If that needs an `ops/` edit, return `NEEDS_CONTEXT` instead of editing.
- (D) **Workflow triggers.** Default: `pull_request` and `push` filtered to `deploy/**`, `.dockerignore`, `ops/c1_rail/**`, `ops/c1_signal_daemon/**`, `core/**` (the listener image COPYs and imports `core/` modules, and a new transitive import anywhere under `core/` is exactly the green-build / dead-CMD class this workflow exists to catch), `scripts/validate_c1_monitoring_acceptance.py`, `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`, `tests/ops/**`, `tests/fixtures/c1_image_validation/**`, `scripts/c1_image_validation.sh`, the workflow file itself; plus `workflow_dispatch`. Not a required merge check (the ruleset owner is Q-GATESTACK-1's closure; do not edit it).
- (E) **Runtime budget.** Default: the job completes in under 15 minutes; the single 30 s timeout probe is acceptable.

## 1. Context and deliverables

PR #332 validated its 33-file change on Windows with five Docker COPY-subset import checks and states plainly: "An actual Linux image build was not performed." Two code paths in that change execute only on POSIX — the parent-directory `fsync` in `atomic_json` / `atomic_write` and the `fcntl.flock` branches of the ceremony locks — and the in-container arming interlock has never been exercised on the new listener image. Track A cannot deploy either image without this evidence.

**Deliverables (one PR, `cursor/*` branch):**

1. `.github/workflows/c1-image-validation.yml` — one job per image (`listener`, `daemon`), each calling the script below with a target argument; artifacts: container logs and the pass/fail table.
2. `scripts/c1_image_validation.sh` — bash, runnable on any Linux host with Docker (`./scripts/c1_image_validation.sh listener|daemon|all`), every check a named step printing `PASS <id>` / `FAIL <id>` and exiting non-zero on any FAIL. No check may be skipped silently.
3. `tests/fixtures/c1_image_validation/` — placeholder configs and a ceremony manifest used by the daemon checks. No secrets.
4. `deploy/README.md` — one short paragraph pointing at the workflow as the Linux validation path (procedure owner stays the per-app READMEs).

**Not asked:** editing Dockerfiles, `.dockerignore`, any `ops/` file, the acceptance JSON, or CI rulesets; touching Fly; making a red check green by weakening it.

## 2. Execution plan — the frozen check list

All `docker run` boot checks use `--network none`. Build context is the repo root. Tag images `c1-rail:ci` and `c1-signal-daemon:ci`. A throwaway host directory is bind-mounted as `/data` per check.

### Listener image

- **L1 build:** `docker build -f deploy/c1_rail/Dockerfile -t c1-rail:ci .` succeeds.
- **L2 contents:** `find /app -type f | sort` inside the image equals exactly the Dockerfile's COPY sources (plus nothing); asserts absence of `*.pine`, `core/data`, `tests/`; asserts presence of `/app/docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` and that `python -c "import sys; sys.path.insert(0,'scripts'); import validate_c1_monitoring_acceptance"` succeeds in-image.
- **L3 WAIT guard:** start with an empty `/data`; within 10 s stderr contains `WAIT:` and the process is still alive.
- **L4 boot disarmed:** `/data` holds the placeholder config (`dry_run:true`, `armed_until:null`, `equity_source:"file"`, all `/data` paths, placeholder auth fields), `c1_current_equity.json` = `{"current_equity":100000.0}`, constants generated **inside the image** via `generate_constants('Tradeify_Select_100K')`, lifecycle `{"M1 Stage1 Test":"RETIRED","Striker":"WATCH-1","Striker NAS100":"WATCH-1"}`, DD state with `peak_equity` 100000.0. Expect the boot line to contain `dry_run=True armed_until=-` and `GET /` → `{"ok":true,...}`.
- **L5a default identity decision:** `POST /c1/<token>` with `{"leg_id":"m1_stage1_test","signal_type":"entry","bar_time":"ci-<uuid>","close":42000.0,"stop_dist_pts":1.0}`; expect HTTP 200; the events ledger gains a `decision` with `qty_out` 0, `dry_run` true, `test_only` true, `sender_invoked` false and a `transport_result` with `transport_state` `not_attempted` (cap 0 / `RETIRED` default).
- **L5b enabled identity decision:** `migrate --config /data/c1_rail_config.json --enable-test` (plan) → `--apply --flat-verified --expect-constants <plan.before.constants> --expect-lifecycle <plan.before.lifecycle>`; backups `*.m1-backup-*` exist; a fresh POST (new `bar_time`) yields `decision.qty_out == 1`, `halt` false, `dry_run` true, `test_only` true, `sender_invoked` false, `test_contract_sha256` equal to `contract_sha256()` computed in-image; response body `dry_run: computed, not sent`. (Verify in Phase 0 whether constants/lifecycle are read per request or cached at boot; if cached, restart the container between apply and POST and say so.)
- **L6 live-mode prohibition:** config copy with `dry_run:false`, `armed_until` = now+1 h ISO UTC, `events_log_path` set → boot line `dry_run=False` → same test POST → `decision.halt` true, `halt_reason` `m1_test_requires_explicit_dry_run`, `qty_out` 0, `sender_invoked` false; `transport_result` `not_attempted`. The absent-key rejection (`dry_run` missing → `m1_test_requires_explicit_dry_run`) is a `handle_signal`-level guard the HTTP server never reaches: `load_config` applies `setdefault("dry_run", True)` and `_rail_config_from` forwards an explicit `True`, so through the built image an absent key is the safe direction, not a rejection. Do not assert it over HTTP; it is covered on Linux in D9 by `tests/ops/test_m1_stage1_listener.py::test_guard_precedes_host_and_payload_even_with_valid_state` (`mode="absent"`).
- **L6b absent key in-image:** config copy with the `dry_run` key **absent** → boot line `dry_run=True armed_until=-` and the test POST yields the L5-shape dry-run decision (`dry_run` true, `sender_invoked` false, `transport_result` `not_attempted`) — never a send. This is the in-image truth for that case and the check asserts exactly that.
- **L7 interlock in-image:** `python ops/c1_rail/c1_rail_arm.py --status --config /data/c1_rail_config.json` prints `m1_gate: status='CODE_LANDED' result=FAIL`; `--arm --hours 1` exits 1 with `refusing to arm` and the config bytes are unchanged (sha256 before == after).
- **L8 implicit disarm:** config `dry_run:false` with `armed_until` in the past → boot line `dry_run=True armed_until=-` and the log contains `IMPLICIT DISARM`.

### Daemon image

- **D1 build:** `docker build -f deploy/c1_signal_daemon/Dockerfile -t c1-signal-daemon:ci .` succeeds.
- **D2 contents:** file set equals the COPY sources (includes `ops/c1_rail/m1_stage1_contract.py`, `ops/c1_rail/__init__.py`); `python -c "import databento"` fails regardless of any later source decision; the third-party distributions installed in the image (`pip list --format=json` minus the base `python:3.12-slim` image's own set) equal exactly the set declared in `deploy/c1_signal_daemon/requirements.txt` when that file exists on the merge SHA, and are empty when it does not. A ratified source may later add a declared client package (Track A plan §3.1); A1b updates this expectation and the fixtures in its own PR, so the check is parameterized by the declared file, never a flat prohibition.
- **D3 WAIT guard:** empty `/data` → `WAIT:` on stderr within 10 s, process alive.
- **D4 inert boot:** example config with a 32+ char placeholder `path_token`, `listener_base_url` `http://127.0.0.1:9`, `strategy:"null"`, `m1_test.enabled:false` → log `daemon up … emit_enabled=false`; `GET /` JSON has `emit_enabled:false`, `effective_emit:false`, `strategy:"NullStrategy"`, `feed_mode:"unavailable"`, `connected:false`, `feed_healthy:false`, `ceremony_state:"DISABLED"`, non-empty `boot_id`; `/data/c1_m1_stage1_state.json` created with `schema_version` 1, `enabled` false, `active` null; `.owner.lock` present; over 15 s no `step ` log lines; no `b1_post` / `m1_b1_post` log lines.
- **D5 stale-enabled config cannot activate:** config with `emit_enabled:true`, `strategy:"m1_stage1_test"`, `bar_period_s:60`, `m1_test.enabled:true` plus placeholder `boot_id`/`ceremony_id`/`generation`/`manifest_sha256` → health identical to D4 (`effective_emit:false`, `strategy:"NullStrategy"`), no POST.
- **D6 CLI refusal without writes:** `prepare` and `enable` exit 2 printing `ceremony blocked: no approved source`; state and config sha256 unchanged; `status` exits 0 with `effective_emit:false`, `source_status:"unavailable"`. (After A1b this check's expectation changes to "refuse without a valid current-boot ceremony"; the re-run brief will say so.)
- **D7 ownership lock across processes:** with the daemon running, a second `python ops/c1_signal_daemon/daemon.py --config …` in the same container exits non-zero within 5 s with `daemon ownership unavailable`; the first daemon's `GET /` still returns 200.
- **D8 restart semantics:** stop and restart against the same `/data`: `boot_id` changed, `generation` incremented by exactly 1, `enabled` false, `active` null, the `.lock` marker still reads `initialized`, and the state file was not re-created (generation > 0).
- **D9 focused suites on Linux:** run `tests/ops/test_c1_signal_daemon_*.py tests/ops/test_m1_stage1_*.py tests/ops/test_c1_rail_*.py tests/ops/test_c1_sizing_host_reference.py tests/ops/test_m1_acceptance_drills.py tests/ops/test_crosstrade_payload.py tests/test_validate_c1_monitoring_acceptance.py tests/rail_crosstrade tests/test_rail_goldenpath_crosstrade.py` per §0.5 (A); all pass; print counts per location.
- **D10 real-socket timeout:** an emitting loop (per §0.5 (C)) POSTing through the real `default_transport` to a local socket that listens but never reads: the call returns after the 30 s timeout with an exception, the journal records `TRANSPORT_UNKNOWN`, exactly one TCP connection was accepted, and two further `step()` calls make no new connection.

### Per-step gate

Each check prints `PASS <id>` or `FAIL <id>` plus the evidence line (boot line, JSON, hash pair). The script's exit code is non-zero if any FAIL. The workflow uploads `/tmp/c1_image_validation/*.log` as an artifact.

## 4. Falsifiable hypothesis

**H:** both images build on Linux from the repo-root context, boot inert/disarmed with no outbound connection, and the POSIX-only fsync/flock branches plus the in-image arming interlock behave as the Windows-validated suite claims.
**Reject** if any L/D check fails — then the PR reports `FAIL <id>` with the log and the check stays red; the parent routes the fix (a Dockerfile/`ops/` defect is a finding for the parent, never a silent fix in this PR). **Ambiguous** if a check cannot be constructed without an `ops/` edit — `NEEDS_CONTEXT`.

## 5. Forbidden moves

- Editing `deploy/*/Dockerfile`, `.dockerignore`, or any `ops/` file to make a check pass.
- Installing `pytest` or anything else into the production Dockerfiles.
- Running any boot check with networking enabled.
- Committing a real token, account id, or equity figure; every value is a placeholder.
- Touching `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` (a green build is not a deploy; `fixture_hashes` are in-container-only).
- Marking a failing check `SKIP`, `xfail`, or "known" to keep the job green.
- Using `fly` in any form.
- Making the workflow a required merge check.

## 6. Gate and return taxonomy

RESOLVED = every L/D check PASS on the PR's workflow run, script runnable locally, `deploy/README.md` pointer added, checkers green. FALSIFIED = a check FAILs for a reason in the image/code (report it; do not fix). AMBIGUOUS = a check could not be built under §0.5.

Return exactly one of `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`, with: branch, PR URL, workflow run URL, the PASS/FAIL table, test counts per location, files changed.

## 7. Parent-session review

Pass 1 — spec compliance: diff limited to the four deliverables; every check id present in the script; no Dockerfile/`ops/` edits; no secrets. Pass 2 — quality: parent re-runs the workflow via `workflow_dispatch` and reads the logs, not the summary; L6 and L7 evidence lines quoted; D10 shows exactly one accepted connection. Pass 3 — consolidated read of workflow + script + fixtures together.

## 10. Audit hooks

```bash
gh run list --workflow c1-image-validation.yml --limit 3
gh run view <run-id> --log | grep -E "^(PASS|FAIL) [LD][0-9]+"
git diff --stat origin/main...HEAD          # expect: workflow, script, fixtures dir, deploy/README.md
git diff origin/main...HEAD -- deploy/c1_rail/Dockerfile deploy/c1_signal_daemon/Dockerfile .dockerignore ops/ | wc -l   # expect 0
```
