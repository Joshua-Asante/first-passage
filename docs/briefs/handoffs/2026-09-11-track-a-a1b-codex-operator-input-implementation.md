# Codex handoff — Track A / A1b: implement the ratified Stage 1 input (option D, operator-attended controlled input)

**Type:** cc_handoff (frozen-spec implementation; Codex variant with parent-recommended defaults)
**Date:** 2026-09-11
**Status:** dispatch now — A1r merged 2026-09-11 (PR #340), A2 listener half merged (PR #339); the daemon half of A2 re-runs on this PR automatically (the workflow is path-filtered on `ops/c1_signal_daemon/**`)
**Spawn target:** Codex (or Cursor) — `codex/*` branch, PR, no merge; Codex is also the standing reviewer of the PR
**Parent:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3.1 (must-cover list) · parent adjudicates with fable-judge, then Codex review
**Authority:** code and tests only. No Fly access, no deploy, no volume write, no ceremony, no secrets, no new runtime dependency. `contract_sha256()` inputs, the listener B1 contract, the `accept_bar` window (`60 ≤ now − bar.ts ≤ 150`) and the manifest window (`60 < expires − target ≤ 150`) do not change.

## 0. Rule 0 reads (Phase 0 — post the read-report before writing code)

Currency: `git fetch origin main`; record the SHA. At authoring time `origin/main` was `26574fa` (2026-09-11). Hard checks: `git ls-tree --name-only origin/main ops/c1_signal_daemon/ | grep -c operator_input_source.py` must print `0` (else someone already built it → `NEEDS_CONTEXT`); `grep -c "^\*\*Status:\*\* RATIFIED 2026-09-11" docs/adr/2026-08-08-s2b-signal-daemon-build.md` must print `1`. Anchor every file below with `git log -1 --format=%h -- <path>` in the report.

- `docs/adr/2026-08-08-s2b-signal-daemon-build.md` @ `33d1682` — §2 rows *Live CME bar source*, *Reconnect* and *Heartbeat* (2026-09-11 scope notes), *Staleness*, *Fail-closed*, *Listener*; Addendum 2026-09-11 §Option D (**Mechanism**, **Build**, **Reversibility** — the binding text; quote it verbatim in the read-report) and §Amendment text — option D.
- `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` @ `0059ca7` — Addendum 2026-09-11: what the event certifies; projection fields `qualifying_live_source: false`, `operator_attended_input: true`.
- `docs/superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md` @ `33d1682` — §1 items 6, 7, 10; §3.1 must-cover list; §6 stop rules.
- `docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md` @ `c480f99` — "Two states, read them apart"; frozen identity and sizing.
- `docs/briefs/handoffs/2026-09-10-track-a-a6-claude-daemon-deploy-inert.md` @ `017bf65` (Step 2.5 health fields) and `docs/briefs/handoffs/2026-09-10-track-a-a7-claude-attended-stage1-dry-run.md` @ `037f09a` (Steps 2.4–2.7, 2.9, 2.11: manifest fields, `prepare`/`enable`/`inject`/`close` command lines, terminal-state wait, projection fields) — the consumers of this build; every interface they name is binding here.
- `ops/c1_rail/m1_stage1_contract.py` @ `811df7c` — `OFFLINE_SOURCE`; `contract_sha256()` (frozen inputs).
- `ops/c1_rail/m1_stage1_control.py` @ `811df7c` — `project_evidence` (lines 162–241; marker check at 198; output dict at 236–241).
- `ops/c1_signal_daemon/m1_stage1_control.py` @ `811df7c` — `validate_manifest`, `prepare`, `enable`, `close`, `safe_status`, `main` (hard `return 2` for prepare/enable at 155–157; line 11 import fails from `/app` without `PYTHONPATH`).
- `ops/c1_signal_daemon/m1_stage1.py` @ `3cdeabe` — `M1Coordinator._active`, `before_poll` (`activate`/`deactivate` calls), `accept_bar`, `reserve` (`bar_sha256 = digest({"bar": …, "source": …})`), `close_attempt`.
- `ops/c1_signal_daemon/m1_stage1_state.py` @ `509b524` — `atomic_json`, `CeremonyStore.locked/boot/mutate`, `DaemonOwnership`, `CeremonyError`, `require`.
- `ops/c1_signal_daemon/daemon.py` @ `811df7c` — bootstrap lines 18–23, `IdleBarSource`, `load_config`, `build_loop`, `run_daemon` quiet path (142–147; interval cached at 138).
- `ops/c1_signal_daemon/evaluate_loop.py` @ `811df7c` — `_step` order: `before_poll` → `poll()` → `accept_bar` → `feed_healthy(connected=…)`; `heartbeat`.
- `ops/c1_signal_daemon/feed.py` @ `811df7c`, `heartbeat.py` @ `509b524`, `http_status.py` @ `027a729`, `m1_stage1_strategy.py` @ `509b524`, `listener_client.py` @ `509b524`, `strategy_protocol.py` @ `027a729`.
- `deploy/c1_signal_daemon/Dockerfile` @ `811df7c`, `deploy/c1_signal_daemon/README.md` @ `811df7c`, `deploy/c1_signal_daemon/c1_signal_daemon_config.fly.example.json` @ `509b524`, `.dockerignore` @ `811df7c`, `ops/c1_signal_daemon/README.md` @ `811df7c`.
- `scripts/c1_image_validation.sh` @ `d584942` — `DAEMON_FILES`; D2 (`D2_pip.py`); D4 `need` dict (`feed_mode:"unavailable"`); D5; D6 (`ceremony blocked: no approved source`, `source_status == "unavailable"`, `-e PYTHONPATH=/app/ops`); D9 `d9_image_files`; D10 probe shape; `.github/workflows/c1-image-validation.yml` @ `2cdab01` (triggers).
- `tests/fixtures/c1_image_validation/ceremony_manifest.json`, `c1_signal_daemon_config.json`, `c1_signal_daemon_config.stale_enabled.json` @ `3ca8fab`.
- `tests/ops/test_c1_signal_daemon_m1.py` @ `811df7c` (`cfg`, `manifest`, `prepared`, `active_loop`; `test_cli_prepare_enable_close_are_control_only`; `test_process_lock_and_optimized_validation`; `test_response_receipt_redacts_body_and_retains_bar_fingerprint`), `tests/ops/test_c1_signal_daemon_source_retirement.py` @ `811df7c`, `tests/ops/test_m1_stage1_integration.py` @ `811df7c`, `tests/ops/test_m1_stage1_control.py` @ `811df7c`, `tests/ops/test_c1_signal_daemon_image_manifest.py` @ `509b524`, `tests/conftest.py` @ `e6b2bd5` (exports `PYTHONPATH` to child interpreters).

## 0.75. Local-only dependency check

`N/A for cloud dispatch — no gitignored vendor data, no secrets.` Every fixture value is a placeholder; bar numbers in tests are synthetic (never a ceremony bar).

## 0.5. Clarifications — parent-recommended defaults (apply unless Phase 0 contradicts; then bounce `NEEDS_CONTEXT` quoting the conflict)

- (A) **Activation carries the ceremony identity.** `M1Coordinator.before_poll` calls `source.activate(manifest["source"], ceremony_id=obj["active"])`. The test sources in `test_c1_signal_daemon_m1.py::active_loop` and `test_m1_stage1_integration.py` change their `activate` signature to accept the keyword. (Rejected: the source reading the journal itself.)
- (B) **File locations derive from the state path.** `state_dir = Path(cfg["m1_test"].get("state_path", DEFAULT_STATE_PATH)).parent` (`/data` on the host, `tmp_path` in tests). Upload `<state_dir>/m1_upload_<ceremony_id>.json`; published one-shot `<state_dir>/m1_bar_<ceremony_id>.json`; claim `<state_dir>/m1_claim_<ceremony_id>`. The A7 operator SFTP target is that same `/data`.
- (C) **Marker value, fixed by the S2b option D block:** `OPERATOR_INPUT_SOURCE = {"kind": "operator_attended_input", "schema": "ohlcv-1m", "symbol": SYMBOL}`.
- (D) **`venue_contract` rule.** Regex `^MYM[HMUZ]\d$`; month H=3, M=6, U=9, Z=12; expiry = third Friday of that month; year = the one year in `target.year − 1 … target.year + 1` whose last digit matches the code; refuse if none, if the expiry date is before `target.date()`, or if it is later than the second quarterly third-Friday on/after `target.date()`. Stdlib date arithmetic only. A provenance sanity bound, not the venue's roll rule. For the fixtures' `target` 2026-09-10: `MYMU6` and `MYMZ6` accepted; `MYMH7`, `MYMN6`, `MYMZ5` refused.
- (E) **Status vocabulary.** `OperatorInputSource.feed_mode` is the constant `"operator_input"` (D4/D5/A6 read it). `status` CLI `source_status` is `"disconnected"` when no published file exists for the active ceremony, `"bar_published"` otherwise. Never a value.
- (F) **Quiet log path.** `run_daemon` logs nothing for `suppress/ceremony_disabled`, and nothing for `suppress/feed_unhealthy` while `not loop._source.connected` (this replaces the `feed_mode == "unavailable"` test); every other non-idle record is still logged.
- (G) **Two markers in the library, one at the CLI.** `validate_manifest`, `prepare` and `enable` accept exactly `OPERATOR_INPUT_SOURCE` and `OFFLINE_SOURCE` (existing fixture tests keep running); `main` refuses `prepare`/`enable`/`inject` unless the manifest (or the READY ceremony's manifest) carries `OPERATOR_INPUT_SOURCE`; `OperatorInputSource.activate` raises `CeremonyError` on any other binding. The runtime can never produce a bar for an offline manifest.
- (H) **D11 is an addition to §3.1.** The atomic publish, the `O_EXCL` claim and the parent-directory fsync are POSIX-only branches, and A7 runs the CLI inside the image, so the one-shot chain gets its own Linux check. If D11 cannot be built within the script's conventions, return `NEEDS_CONTEXT`; do not weaken it. D10 is adapted, not replaced (Step 2.7).
- (I) **Interval cache.** `run_daemon` keeps reading `poll_interval_s` once at startup (A6 stages `1` on the volume before the deploy; A7 verifies `GET /`). Do not add hot-reload.

## 1. Context and deliverables

Option D was ratified 2026-09-11 and recorded by A1r. On `main` nothing of it exists: the daemon CLI offers `prepare`/`enable`/`close`/`status` and returns `2` for the first two; `build_loop` constructs `IdleBarSource` + `NullStrategy` with no coordinator; `validate_manifest` and `project_evidence` accept only the offline marker; the daemon CLI has no `sys.path` bootstrap. A6 deploys this build and A7 runs one ceremony through it, so the interfaces those briefs name are the acceptance surface of this PR. §3.1 says the implementer "changes the daemon only" and then names two listener-side files: read that as *no listener runtime change* — the listener image's B1 path is untouched; the marker constant and `project_evidence` are the only listener-side edits.

**Deliverables (one PR, `codex/*` branch):**

1. `ops/c1_signal_daemon/operator_input_source.py` (new) — `OperatorInputSource` + `cleanup_orphans` (Step 2.2).
2. `ops/c1_rail/m1_stage1_contract.py` — `OPERATOR_INPUT_SOURCE`; `contract_sha256()` output byte-identical (Step 2.1).
3. `ops/c1_signal_daemon/m1_stage1_control.py` — bootstrap; `validate_manifest`; `prepare`/`enable` (no hard `2`; interval gate); `inject`; `close` cleanup; `safe_status`; `main` (Step 2.3).
4. `ops/c1_signal_daemon/m1_stage1.py`, `daemon.py`, `heartbeat.py` — activation call, shared predicate, `venue_contract` in the bar record, wiring, startup cleanup, config validation, quiet path, heartbeat field (Step 2.4).
5. `ops/c1_rail/m1_stage1_control.py::project_evidence` — marker acceptance and output fields (Step 2.5).
6. `deploy/c1_signal_daemon/Dockerfile`, `.dockerignore`, `deploy/c1_signal_daemon/c1_signal_daemon_config.fly.example.json` (`poll_interval_s: 1`), `deploy/c1_signal_daemon/README.md` (option D section), `ops/c1_signal_daemon/README.md` (Step 2.6).
7. `scripts/c1_image_validation.sh` + `tests/fixtures/c1_image_validation/` — D2 file list, D4/D5 health, D6 refusals, D9 subset, new D11 (Step 2.7).
8. Tests (Step 2.8).

**Not asked:** `ops/c1_rail/c1_rail_listener.py`, `c1_rail_http_server.py`, `c1_rail_arm.py` or any listener runtime file; the acceptance JSON; the two ADRs, the Track A plan, the A6/A7 briefs (the parent records the build after merge); the workflow trigger list; `requirements.txt`; the A2 listener checks; anything on Fly.

## 2. Execution plan — the frozen spec

### Step 2.1 — Marker (`ops/c1_rail/m1_stage1_contract.py`)

- Add `OPERATOR_INPUT_SOURCE = {"kind": "operator_attended_input", "schema": "ohlcv-1m", "symbol": SYMBOL}` after `OFFLINE_SOURCE`, with a one-line comment that the offline marker is test-only. Nothing else in the file changes.
- **Gate:** `python -c "import sys;sys.path.insert(0,'ops');from c1_rail.m1_stage1_contract import contract_sha256;print(contract_sha256())"` printed before and after the change, equal; both prints go in the PR body.

### Step 2.2 — `OperatorInputSource` (`ops/c1_signal_daemon/operator_input_source.py`, new)

- `OperatorInputSource(state_dir: Path, *, boot_id: str)`; `feed_mode = "operator_input"` (constant); `binding` and `ceremony_id` are `None` while inactive; `connected` is a property.
- `activate(binding, *, ceremony_id)`: `binding != OPERATOR_INPUT_SOURCE` → `raise CeremonyError` (the coordinator's `before_poll` catches it, deactivates, returns `False`). Same `ceremony_id` as currently bound → no-op (it is called every poll cycle). A different id → discard any cached bar, `connected = False`, bind the new id.
- `poll()`: inactive → `None`. Bar already handed out → `None`. Otherwise read `<state_dir>/m1_bar_<ceremony_id>.json`: absent → `None`; unreadable, not a JSON object, `schema_version != 1`, `ceremony_id`/`boot_id` mismatch, `bar_sha256` mismatch on recomputation, non-finite/non-positive/bool numbers, OHLC inconsistency (`low ≤ min(open, close) ≤ max(open, close) ≤ high`), or a timestamp that is not explicit UTC → `None` (one value-free `operator_input: published bar rejected` log line per ceremony at most; never the numbers). Valid → cache it, `connected = True`, return `Bar(ts=utc(timestamp), open, high, low, close, volume)` **exactly once**.
- `connected` stays `True` from the first valid read until `deactivate()`, independent of whether the file still exists (`EvaluateLoop._step` evaluates `feed_healthy` after `poll()`; deriving `connected` from the file would suppress the only bar as `feed_unhealthy`).
- `deactivate()`: no-op when nothing is bound; otherwise clear binding/cache, `connected = False`, unlink `m1_bar_<id>.json`, `m1_upload_<id>.json`, `m1_claim_<id>` for the released id (missing → ignore). Idempotent.
- `cleanup_orphans(state_dir)` (module function): unlink every `m1_bar_*.json`, `m1_upload_*.json`, `m1_claim_*`; `build_loop` calls it right after `store.boot()` (the boot closes every ceremony of an earlier boot, so nothing READY under the current boot exists yet).
- No log, print, or exception message ever carries a bar value.
- **Gate:** tests 2.8 (a).

### Step 2.3 — `inject` and the CLI (`ops/c1_signal_daemon/m1_stage1_control.py`)

- **Bootstrap:** copy `daemon.py` lines 18–23 verbatim above the imports, so `python ops/c1_signal_daemon/m1_stage1_control.py <action> …` runs from the repo root and from `/app` with no `PYTHONPATH` (A6 and A7 invoke it that way).
- **`validate_manifest(value, now=None)`:** key set becomes `{ceremony_id, target, expires, contract_sha256, expected_qty, preflight_sha256, source, venue_contract}`; `source in (OPERATOR_INPUT_SOURCE, OFFLINE_SOURCE)`; `venue_contract` per §0.5 (D) against `target`; every other rule unchanged.
- **`prepare` / `enable`:** before any write, `CeremonyError` unless the config's `poll_interval_s` is an `int`/`float` (not `bool`), finite, and `0 < poll_interval_s ≤ 1`. `prepare` checks it before writing `obj["enabled"] = False`.
- **Shared predicate:** move `M1Coordinator._active`'s condition list into `active_ceremony(obj, cfg, boot_id, now) -> item | None` in this module; `m1_stage1.py` imports and delegates to it; `inject` uses the same function. One predicate, two callers.
- **`close`:** after the existing writes, unlink `m1_upload_<id>.json`, `m1_bar_<id>.json`, `m1_claim_<id>` (missing → ignore).
- **`inject(store, config_path, *, ceremony_id, boot_id, contract, time, bar_file, now)`** — in this order, refusing with `CeremonyError` before any write:
  1. `now` is wall-clock UTC in `main` (`datetime.now(timezone.utc)`), injected in tests.
  2. **Upload path first, before any read or lock:** `Path(bar_file).resolve()` must equal `<state_dir>/m1_upload_<ceremony_id>.json` resolved; any other path — the journal, the config, the published bar, a sibling upload, a symlink that resolves elsewhere — is refused (`bad upload path`) and **nothing is read or deleted**. Because this check precedes every other, its verdict does not depend on the ceremony state.
  3. Under `store.locked()`: `active_ceremony(obj, load_config(config_path), boot_id, now)` must return the item for `obj["active"] == ceremony_id` — current boot, READY, not tombstoned, `obj["enabled"] is True`, config `emit_enabled` and `m1_test.enabled` `True` with matching `ceremony_id`/`boot_id`/`generation`/`manifest_sha256`, manifest valid, not expired. A READY ceremony after `prepare` but before `enable` is therefore refused (the daemon would otherwise `deactivate()` and delete the sole injection).
  4. `contract == manifest["venue_contract"]` and `utc(time) == utc(manifest["target"])`.
  5. `60 ≤ (now − target).total_seconds() ≤ 120`.
  6. The upload: exists; a JSON object with exactly the keys `open, high, low, close, volume`; each `int`/`float` (not `bool`), finite, `> 0`; `low ≤ min(open, close) ≤ max(open, close) ≤ high`.
  7. Claim: `os.open(<state_dir>/m1_claim_<id>, O_CREAT | O_EXCL | O_WRONLY, 0o600)`; `FileExistsError` → refused (`already injected`). Taken only after 2–6 pass and while the journal lock is held, so concurrent injectors serialize on the lock and exactly one obtains the claim. The claim persists until `close`/`deactivate`/startup cleanup.
  8. Publish with `atomic_json(<state_dir>/m1_bar_<id>.json, record)` where `record = {"schema_version": 1, "ceremony_id", "boot_id", "venue_contract", "timestamp": utc(manifest["target"]).isoformat(), "open", "high", "low", "close", "volume" (floats), "bar_sha256"}` and `bar_sha256 = digest({"bar": {"timestamp", "open", "high", "low", "close", "volume", "venue_contract"}, "source": manifest["source"]})` — the identical expression `reserve()` uses (Step 2.4), so the receipt joins the journal and the projection by hash. **If anything raises after the claim exists** — including `atomic_json` failing in the parent-directory fsync after `os.replace` has already made the complete file visible — **the claim is preserved**, nothing is retried, and the CLI exits 2 with `inject refused: publication uncertain`. If the published file exists the daemon consumes it as normal (`os.replace` is atomic, so the file is complete); if not, the ceremony expires and a later ceremony gets a fresh id. A publication failure never releases the claim.
  9. Receipt on stdout, exit 0: `{"action": "inject", "ceremony_id", "venue_contract", "target", "bar_sha256", "published_at": <now ISO UTC>}` — no OHLCV, no token, no path.
  10. `finally`: unlink the **validated** upload path from step 2 (never the caller string as given) on every exit path after step 2, success or refusal (missing → ignore); when step 2 refused, nothing is unlinked. On refusal nothing else is written.
  11. Refusals print `inject refused: <reason>` from the fixed set `bad upload path · not active · not enabled · contract mismatch · time mismatch · before window · after window · bad bar file · already injected · publication uncertain`, exit 2; any other `CeremonyError`/`OSError`/`ValueError` prints `ceremony control failed closed`, exit 2. Never echo a value.
- **`safe_status`:** existing fields plus `source_status` per §0.5 (E); still no `--config` needed.
- **`main`:** `action` choices gain `inject`; new arguments `--contract`, `--time`, `--bar-file`; the hard `return 2` for `prepare`/`enable` is removed; `prepare`/`enable`/`inject` refuse (exit 2, value-free text) unless the manifest — for `inject`, the READY ceremony's manifest — carries `OPERATOR_INPUT_SOURCE`; every `except` branch stays value-free.
- **Gate:** tests 2.8 (b), (e); D6; D11.

### Step 2.4 — Coordinator, loop wiring, heartbeat (`m1_stage1.py`, `daemon.py`, `heartbeat.py`)

- `before_poll`: `source.activate(active["manifest"]["source"], ceremony_id=obj["active"])`; the `deactivate()` calls and the expiry close are unchanged; `_active` delegates to `active_ceremony`.
- `accept_bar`: window and checks unchanged; `_accepted_bar` gains `"venue_contract": self.current_manifest["venue_contract"]`, so `reserve()`'s existing `bar_sha256 = digest({"bar": item["bar"], "source": …})` carries the contract without changing form.
- `daemon.py`: delete `IdleBarSource`. `build_loop`: `state_dir = store.path.parent`; `cleanup_orphans(state_dir)` after `store.boot(boot_id)`; `source = OperatorInputSource(state_dir, boot_id=boot_id)`; `coordinator = M1Coordinator(store, config_path, boot_id=boot_id)`; `EvaluateLoop(source=source, client=…, strategy=NullStrategy(), bar_period_s=60, emit_enabled=False, coordinator=coordinator, boot_id=boot_id)`. Inert by construction: with no active ceremony every step is `suppress/ceremony_disabled`, and `strategy` stays `NullStrategy` until a ceremony activates (A6 reads `strategy:"NullStrategy"` at boot).
- `load_config`: `poll_interval_s` must be `int`/`float` (not `bool`), finite, `> 0`, else `ValueError`. The `≤ 1` bound is the ceremony gate (Step 2.3), not a boot requirement.
- `run_daemon`: quiet path per §0.5 (F); the interval is still read once at startup (§0.5 (I)).
- `HeartbeatState.poll_interval_s: float | None = None`; `EvaluateLoop.heartbeat(now=None, *, poll_interval_s=None)` fills it; `run_daemon` passes the cached interval. `GET /` JSON therefore reports `poll_interval_s` (A6 Step 2.5, A7 Step 2.1).
- No log record may contain a bar value; the coordinator path's `step` record stays `{"action": "posted", "http_status": …}`.
- **Gate:** tests 2.8 (c), (d); D4; D5; D11.

### Step 2.5 — Evidence projection (`ops/c1_rail/m1_stage1_control.py`)

- Accept `source in (contract.OFFLINE_SOURCE, contract.OPERATOR_INPUT_SOURCE)`; anything else stays `feed binding mismatch`. For the operator marker additionally require `manifest["venue_contract"]` to match `^MYM[HMUZ]\d$` and `bar["venue_contract"] == manifest["venue_contract"]`.
- Output: `offline_test_only` = source is offline; `operator_attended_input` = source is the operator marker; `qualifying_live_source: False` in both cases; `venue_contract` = the manifest value for the operator marker, `None` for offline; every other field unchanged; `dry_run_strategy_signal_event_id` is still never emitted.
- **Gate:** tests 2.8 (d), (f).

### Step 2.6 — Image, README, example config

- Dockerfile `COPY` adds `ops/c1_signal_daemon/operator_input_source.py`; `.dockerignore` re-includes it; `DAEMON_FILES` in the validation script adds `/app/ops/c1_signal_daemon/operator_input_source.py`.
- Example config: `"poll_interval_s": 1`; nothing else changes.
- `deploy/c1_signal_daemon/README.md`: replace the "2026-09-10 - source unavailable" section with "2026-09-11 - Stage 1 input: operator-attended controlled input (option D)": no new config keys; `poll_interval_s` must be `1` on the volume before a ceremony because the loop caches it at startup; the upload/published/claim path conventions; the exact `prepare`, `enable`, `inject` and `close` command lines in the A7 form; what `status` and `GET /` report; links to the S2b and M1 addenda. No values, no secrets. A4-D reviews this section as the pending-write record.
- `ops/c1_signal_daemon/README.md`: the disposition paragraph updated to option D (three lines).
- **Gate:** `python -m pytest tests/ops/test_c1_signal_daemon_image_manifest.py tests/ops/test_c1_rail_image_manifest.py -q`; D2.

### Step 2.7 — Linux validation expectations (`scripts/c1_image_validation.sh`, fixtures)

- **D2:** file list gains the new module; the no-`requirements.txt` rule is unchanged.
- **D4/D5:** `need` gains `"feed_mode": "operator_input"` (replacing `unavailable`) and `"poll_interval_s"` equal to the fixture config's value (the D4/D5 fixtures keep `5`; D11 stages its own `1`).
- **D6 → three refusals**, each exit 2, config and state hashes unchanged, no `m1_bar_*`/`m1_claim_*` created, the staged upload removed: (i) `prepare` with a manifest whose `contract_sha256` the script computes **in-image** (as L5b does) and `venue_contract` valid for its `target`, but `--boot-id stale-boot` → refused; (ii) `enable --ceremony-id does-not-exist` → refused; (iii) `inject` with a staged `/data/m1_upload_<id>.json` fixture bar and no READY ceremony → refused, upload gone. Invocation form `python ops/c1_signal_daemon/m1_stage1_control.py <action> …` from `/app` **without** `-e PYTHONPATH` (proves the bootstrap in-image). `status` → exit 0, `effective_emit:false`, `source_status:"disconnected"`.
- **Fixture `ceremony_manifest.json`:** `source` = the operator marker; add `venue_contract` valid for the fixture `target` (2099-01-01 → `MYMH9`).
- **D9:** add the new unit-test files (2.8 (a), (b), (c), (e)) to `d9_image_files` — their imports resolve from `/app/ops`.
- **D10:** the existing probe keeps its purpose (30 s timeout, `TRANSPORT_UNKNOWN`, one accepted connection) and is adapted, never skipped: its embedded manifest gains `venue_contract` (computed for its own `target` by the §0.5 (D) rule — the offline marker may stay because the probe drives the library, not the CLI), and its inline `Source.activate` accepts `ceremony_id=`. Its config already carries `poll_interval_s: 1`. A probe that now fails in `prepare`/`enable` before reaching the timeout is a `FAIL D10`.
- **D11 (new) — one-shot injection on Linux**, daemon image, `--network none`, throwaway `/data`: (1) stage a config with `poll_interval_s: 1`, `bar_period_s: 60`, `strategy: "null"`, `emit_enabled: false`, `listener_base_url: "http://127.0.0.1:9"`; boot the daemon; read `boot_id` from `GET /`. (2) Compute `contract_sha256()` in-image; `target` = the first whole UTC minute at or after `now + 20 s` (so the wait to `target` is 20–80 s and `prepare`/`enable` have time to run before it), `expires = target + 150 s`, the operator marker, `venue_contract` = the first quarterly code whose third Friday is on/after the target date (the §0.5 (D) rule), `expected_qty: 1`, a placeholder `preflight_sha256`. (3) `prepare` → exit 0; `status` `state:"READY"`; `GET /` `effective_emit:false`. (4) `enable` → exit 0; `GET /` `effective_emit:true`, `ceremony_state:"READY"`, `connected:false`, `strategy` may already read `M1Stage1TestStrategy`. (5) Stage `/data/m1_upload_<id>.json` = `{"open":41000,"high":41002,"low":40999,"close":41001,"volume":3}`; `inject` at `target + 59 s` (the sleep is computed against `target` from the script's clock) → exit 2 `before window`, upload absent, no `m1_bar_*`; re-stage; `inject` at `target + 61 … 70 s` → exit 0, receipt JSON with `bar_sha256`, upload absent; re-stage at once and run a second `inject` → exit 2 with **either** `already injected` (the claim is reached first) **or** `not enabled`/`not active` (the daemon has already reserved the bar — with a 1 s poll this is the usual outcome, and it is accepted): both refusals write nothing, so assert the upload is absent and that no new `m1_bar_<id>.json` appears afterwards; the deterministic pre-consumption duplicate is 2.8 (b)'s job, which D9 runs in-image. Then `inject --bar-file /data/c1_m1_stage1_state.json` → exit 2 `bad upload path` with the state file byte-identical (path validation precedes every other check, so this holds in any ceremony state). (6) Within 5 s of the first receipt the journal reaches the terminal state `TRANSPORT_UNKNOWN` (`127.0.0.1:9` refuses, so the single attempt fails fast), `enabled` false, journal `bar_sha256` == receipt `bar_sha256` (the consumed bar is the first and only publication), `m1_bar_<id>.json` and `m1_claim_<id>` removed by the following cycle's `deactivate()`; `docker logs` shows exactly one `step {'action': 'transport_unknown'}` record, and no log line or stdout contains `41000`, `41001`, `40999` or `41002`. (7) `close` → exit 0; journal `CLOSED` with `previous_state:"TRANSPORT_UNKNOWN"`; `prepare` of a fresh id → exit 2 (unresolved-attempt barrier); `GET /` `effective_emit:false`. Wall-clock budget ≤ 4 minutes (≤ 80 s to `target`, 61 s to the window, ≤ 20 s of checks, ≤ 15 s of settle and close); every wait is computed from the script's own clock against `target`, never a fixed `sleep`.
- **Gate:** the workflow run on the PR head is green with `PASS D1 … PASS D11` and the listener checks unchanged.

### Step 2.8 — Tests (add or update; never delete)

- (a) `tests/ops/test_c1_signal_daemon_operator_input.py` (new): inactive `poll()` is `None`; `activate` refuses a foreign binding; idempotent re-activation; valid file → one `Bar`, then `None`, with `connected` still `True`; `deactivate()` → disconnected and the three files removed; each rejection class in Step 2.2 (wrong ceremony id, wrong boot, bad hash, truncated JSON, NaN/inf/negative/bool, OHLC inconsistency, naive timestamp); `cleanup_orphans` removes all three patterns; concurrent publication (a writer does temp-file + `os.replace` while a poller loops: the poller sees `None` or the complete bar, never raises).
- (b) `inject` (same file or `tests/ops/test_c1_signal_daemon_inject.py`): window boundaries at `now − target` ∈ {59, 60, 120, 121} s; contract mismatch; time mismatch; READY-not-enabled; journal enabled but config `m1_test.enabled` false; expired manifest; wrong boot; each bad-bar-file class; the upload is removed on every path; published path distinct from the upload (delete the upload after a successful inject → the published file is still there and `poll()` returns the bar); second inject → `already injected`; concurrent inject (two threads, two upload files) → exactly one exit 0, one `already injected`, one published file; the receipt contains no OHLCV substring; receipt `bar_sha256` == journal `bar_sha256` after `loop.step()` reserves; publication failure before replacement (monkeypatched `os.replace` raising): no published file, claim kept, a second inject → `already injected`; publication failure after replacement (the parent-directory `os.fsync` inside `atomic_json` monkeypatched to raise): the complete published file is present, claim kept, a second inject → `already injected`, `poll()` returns the bar; upload-path validation: `--bar-file` set to the state path, the config path, the published path, a sibling `m1_upload_<other-id>.json`, or a symlink at the correct name that resolves outside `state_dir` → `bad upload path`, every file byte-identical, nothing unlinked, and the same verdict after the ceremony has been consumed (path validation precedes the state check); `main(["inject", …])` with an offline-marker ceremony returns 2 with `inject refused:`.
- (c) runtime: `build_loop` on a fresh tmp state yields the operator source disconnected with a coordinator; `heartbeat` reports `feed_mode "operator_input"`, `strategy "NullStrategy"`, `connected False`, `effective_emit False`, `poll_interval_s` from config; a stale-enabled config with a foreign boot stays inert; startup cleanup removes orphans; `run_daemon` logs no `step ` line while idle and none while an enabled ceremony awaits injection (caplog); `load_config` rejects `poll_interval_s` ∈ {0, −1, "1", True, NaN}; `prepare`/`enable` refuse `5` and accept `1` and `0.5`.
- (d) `tests/ops/test_m1_stage1_integration.py`: a second parametrized path with the real `OperatorInputSource` and the `inject` library function through the same real HTTP handler → `posted`, `RESPONSE_RECORDED` `dry_run_computed`; `project_evidence` → `operator_attended_input True`, `offline_test_only False`, `qualifying_live_source False`, `venue_contract` = the manifest's; the equity string absent from the proof; crash-before-poll (inject, then `store.boot("new-boot")` + `cleanup_orphans` → published file gone, ceremony `CLOSED`/`boot_changed`, a fresh ceremony prepares cleanly); the `dry_run False` case unchanged.
- (e) `tests/ops/test_c1_signal_daemon_cli_bootstrap.py` (new): `subprocess.run([sys.executable, "ops/c1_signal_daemon/m1_stage1_control.py", "status", "--state", <tmp state seeded by CeremonyStore.boot>], cwd=<repo root>, env={k: v for k, v in os.environ.items() if k != "PYTHONPATH"})` → exit 0 and a JSON line; the same with the absolute script path from `tmp_path` as cwd → exit 0.
- (f) Existing tests updated, not deleted: `test_c1_signal_daemon_source_retirement.py` keeps `test_no_retired_provider_module_or_dependency` and re-states the other cases for the option D runtime; `test_cli_prepare_enable_close_are_control_only` uses the operator marker and asserts `enable` → 0 with no send, `close` → 0; every `manifest()` fixture gains `venue_contract` (`MYMZ6` for the 2026-09-10 target); `test_m1_stage1_control.py::proof()` gains `venue_contract` and a second proof with the operator marker (the mutation cases run against both); `active_loop` and the integration source accept `ceremony_id=`; `test_response_receipt_redacts_body_and_retains_bar_fingerprint` expects `venue_contract` inside `item["bar"]`; the D6 fixture manifest as in Step 2.7.
- **Gate:** `python -m pytest tests/ops/test_c1_signal_daemon_*.py tests/ops/test_m1_stage1_*.py tests/ops/test_c1_rail_image_manifest.py -q` green locally on Python 3.12; counts per file reported.

### Step 2.9 — PR and return

Branch `codex/a1b-operator-input`; PR title `feat(a1b): operator-attended controlled input — one-shot source, inject CLI, marker, evidence projection (Track A / A1b)`; body: the file list, both `contract_sha256()` prints, test counts, the workflow run URL with the `PASS D1 … D11` lines, the README section pasted, and the §6 status line. No merge.

## 4. Falsifiable hypothesis

**H:** the ratified option D input is implementable inside `ops/c1_signal_daemon/`, `ops/c1_rail/m1_stage1_contract.py` (marker only), `ops/c1_rail/m1_stage1_control.py::project_evidence`, `deploy/c1_signal_daemon/`, `.dockerignore`, `scripts/c1_image_validation.sh` and `tests/` — with `contract_sha256()` byte-identical, the listener B1 contract untouched, no runtime dependency, every A6/A7 interface satisfied as named — and on Linux the one-shot chain (`prepare` → `enable` → `inject` → `poll()` → hook → reservation → one POST attempt → terminal journal state → cleanup) completes with no bar value in any log or stdout.
**Reject** if any surface outside that list must change, `contract_sha256()` changes, a value leaks, or D11 cannot pass without weakening → report it and return `BLOCKED — plan-itself-wrong`; the parent re-authors. **Ambiguous** if a §0.5 default contradicts a Phase 0 read → `NEEDS_CONTEXT` quoting the conflict.

## 5. Forbidden moves

- Widening `60 ≤ now − target ≤ 120`, the `accept_bar` 60…150 s window, or the manifest window "to give the operator more time".
- Deriving `connected` from the published file's continued existence (it consumes the file and suppresses the only bar as `feed_unhealthy`).
- Releasing the claim after a publication failure (`os.replace` may already have made the file visible), or unlinking any path other than the validated upload path.
- Passing bar values on the command line, printing them in the receipt, or logging them anywhere — including exception messages and `step` records.
- Changing `contract_sha256()` inputs, `LEG_ID`/`SYMBOL`/`STOP_DIST_PTS`, the B1 payload shape, or any listener runtime file.
- Adding a runtime dependency or a `deploy/c1_signal_daemon/requirements.txt` — option D is stdlib-only.
- Letting the runtime CLI accept `OFFLINE_SOURCE` manifests, or `OperatorInputSource.activate` accept a foreign binding.
- Deleting the source-retirement test or the D6 refusal check instead of updating them; marking any D check `SKIP`.
- Editing the acceptance JSON, either ADR, the Track A plan, the A6/A7 briefs, or the workflow's trigger list.
- Touching Fly, any volume, or the running hosts.
- Hand-editing a fixture's `contract_sha256` to green a check (compute it in-image instead).
- A "while I was in there" refactor of `EvaluateLoop`, the journal, or the listener client.

## 6. Gate and return taxonomy

RESOLVED = every Step 2.x gate met; the workflow green on the PR head with `PASS D1 … D11`; the local suite green; the two `contract_sha256()` prints equal; `git diff --stat origin/main...HEAD` confined to the §1 surface. FALSIFIED = a §4 reject fired (report; do not work around it). AMBIGUOUS = a §0.5 conflict.

Return exactly one of `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`, with: branch, PR URL, workflow run URL, the PASS/FAIL table, test counts per location, the two `contract_sha256()` prints, files changed.

## 7. Parent-session review

Pass 1 — spec compliance: diff confined to the §1 surface; `contract_sha256()` unchanged; no listener code beyond `project_evidence` and the marker; no dependency; no ADR/plan/brief edits; D6 and D11 present with the pinned assertions; `feed_mode`, `source_status` and the heartbeat field spelled exactly as A6/A7 read them. Pass 2 — quality (fable-judge): parent runs the suite locally, re-runs the workflow via `workflow_dispatch` and reads D11's log (receipt hash == journal hash; upload absent after every call; `already injected` on the second call; no bar value in logs); reads `inject` for the write order (upload path validated first, claim after every check, publish after the claim, the claim preserved on any failure after it, only the validated upload path unlinked in `finally`); reads `poll()` for the once-only hand-out and `connected` independence from the file. Pass 3 — consolidated read of source + CLI + coordinator + projection together, then the A6/A7 briefs against the merged interfaces: A6 Step 2.5 and A7 Steps 2.4–2.7 and 2.11 must need no edits — if they do, the parent edits the briefs, never the code.

## 10. Audit hooks

```bash
git diff --stat origin/main...HEAD            # expect: the §1 surface only
python -c "import sys;sys.path.insert(0,'ops');from c1_rail.m1_stage1_contract import contract_sha256,OPERATOR_INPUT_SOURCE;print(contract_sha256());print(OPERATOR_INPUT_SOURCE)"
grep -n "OPERATOR_INPUT_SOURCE\|OFFLINE_SOURCE" ops/c1_signal_daemon/m1_stage1_control.py ops/c1_rail/m1_stage1_control.py ops/c1_signal_daemon/operator_input_source.py
grep -n "<= 120\|<= 150\|60 <=" ops/c1_signal_daemon/m1_stage1_control.py ops/c1_signal_daemon/m1_stage1.py   # windows unchanged
grep -n "bad upload path\|publication uncertain\|already injected" ops/c1_signal_daemon/m1_stage1_control.py   # refusal set present
grep -n "operator_input_source" deploy/c1_signal_daemon/Dockerfile .dockerignore scripts/c1_image_validation.sh
grep -n "operator_input\|source_status\|poll_interval_s\|D11" scripts/c1_image_validation.sh | head -20
gh run list --workflow c1-image-validation.yml --limit 3
gh run view <run-id> --log | grep -E "^(PASS|FAIL) [LD][0-9]+"
python -m pytest tests/ops/test_c1_signal_daemon_*.py tests/ops/test_m1_stage1_*.py tests/ops/test_c1_rail_image_manifest.py -q
```
