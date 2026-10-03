# TB-I3 synthetic-scope activation interlock (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT — coordinator (3) freezes. Drafted 2026-10-03 by a coordinator-(3) worker; not dispatched. Coordinator (3) answers §12, commits the frozen revision under the committed-handoff rule and records its SHA in the ledger before any executor starts. Dispatch is a separate decision.

**Authority:** Operator ruling 2026-10-02 (sitting 2), TB-I3-CARD: card now, synthetic scope only. No arm, no deploy, no route integration; production blocked. Dispatch is separate.

**Rulings folded in (all "operator ruling 2026-10-02 (sitting 2)", Joshua "all recommended", 2026-10-03T01:42Z):**
- **TB-I3-CARD:** the activation-interlock card (`deployment_go.py` validator, `--arm` check, host boot gate checking M1 and the GO) may be written now, synthetic scope only. This narrows the TB-I1 prerequisite for this card only (umbrella `:232` TB-I3 row, appended by the c2 batch).
- **A12-STALE:** stale order-level evidence remains a refusal, not an incident. Fresh evidence alone never lifts it; in the first release admission stays closed for the rest of the session. Risk-reducing exits and the scheduled flatten continue. TB-I3 implements the latch (owner row: [bounded incident contract `:536`](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md); halt/resume [O-1 `:106`](../../spec/2026-09-14-tb-s3-halt-resume-contract.md)). Armed commissioning and later releases are not decided.
- **TB-I4-M1:** M1 stays retained and does not cover the book host. Book-host monitoring evidence is the book-route monitoring acceptance added in T13/TB-I3. TB-I4 as written is not a book-route prerequisite (D-B13 amendment).

**Executor:** proposed Codex local (the umbrella's TB-I3 routing, `:232`), single writer of `codex/tb-i3-synthetic-interlock` (proposed), cut from the freeze base. **Not GLM:** arming, interlock and risk-admission code (AGENTS.md GLM rule; this supersedes the R-A2 draft's `glm_agent` suggestion).

**Coordinator:** coordinator (3). It owns the freeze, diff review, integration, the Codex relay, PRs and the ledger.

**Owners this card narrows (it changes none of them):**
- [Book protection admission ADR](../../adr/2026-09-12-tradeify-book-protection-instance-admission.md): §2a T10–T11 (`:99-100`), §2b validator and interlock (`:102-107`), initial-activation-only rule (`:109`), §2c TB-I3 row (`:118`).
- [Multi-leg rail extension spec](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) R-L (`:161`) and R-A2 (`:145`).
- [Track B umbrella](2026-09-10-track-b-qualify-accepted-book-umbrella.md) TB-I3 row (`:232`) and wave-3 stub (`:635`).
- [TB-S3 halt/resume contract](../../spec/2026-09-14-tb-s3-halt-resume-contract.md) O-1 (`:106`).

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - synthetic_scope_only
  - no_arm
  - no_deploy
  - no_route_integration
  - no_host_or_fly_command
  - no_image_push
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - card_section2_files_only
  - no_real_go_or_monitoring_artifact_committed
  - no_m1_artifact_edit
  - no_dd_protection_or_frozen_constant_edit
  - no_pine_or_port_access
  - no_private_bytes_committed
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_deployment_go.py
  - tests/ops/test_c1_rail_arm.py
  - tests/ops/test_c1_rail_http_server.py
  - tests/ops/test_c1_rail_image_manifest.py
  - tests/test_validate_c1_monitoring_acceptance.py
  - tests/ops/test_book_stale_admission_latch.py
  - tests/ops/test_book_account_owner.py
  - tests/ops/test_pr409_review4.py
  - tests/ops/test_book_feedback_journal.py
  - tests/ops/test_book_close_reconciliation.py
  - tests/ops/test_book_sources.py
  - tests/ops/test_book_loop_source_health.py
  - tests/ops/test_four_leg_runtime.py
  - tests/ops/test_feed_omission_session_end.py
  - tests/ops/test_c1_signal_daemon_image_manifest.py
```

`test_deployment_go.py`, `test_book_stale_admission_latch.py`, `test_book_sources.py` and `test_book_loop_source_health.py` are new. The rest exist and are extended in place or must stay green unchanged (§4).

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

1. **Premise.** HEAD descends from the freeze base (D-9). As drafted, `origin/main` is `1a350ec`. `POLICY_REGISTRY` is empty (`core/dd_geometry.py:92`). No `DEPLOYMENT_GO.json` exists. `ops/c1_rail/policy_fingerprint.py` exists (TB-I1). PR #619 (`claude/a9-prep-barsource`, head `77373bd`) is **OPEN**. No `.env` in the worktree.
2. **Rule-0 reads** (read them; do not infer them):
   - `ops/c1_rail/c1_rail_arm.py`: `m1_acceptance_reason` and `m1_acceptance_structurally_valid` (validator-backed, fail-safe); `plan_arm` (pure); `_record_deviation`, written **before** the config; the hidden `--acceptance` test seam.
   - `ops/c1_rail/c1_rail_http_server.py:142-219` `load_config`: boot **implicit disarm** in memory, never a raise, for an invalid window (2026-07-31 crash-loop lesson, `:160-193`). The one boot raise is a missing `events_log_path` (`:155-158`). The boot gate checks neither M1 nor any GO (AGENTS.md live-execution posture).
   - `scripts/validate_c1_monitoring_acceptance.py:81` `validate(path, *, require_resolved)`, which returns an error list. It is the schema owner; never re-implement it.
   - `ops/c1_rail/policy_fingerprint.py`: `canonical_policy_bytes`, `normalized_geometry_bytes`, `validate_registry` (expected rows supplied independently, `:181`), `validate_initial_arm_delta` (`:241`), `build_shared_manifest` and `verify_shared_manifest`. ADR `:76` forbids an independent reimplementation.
   - `deploy/c1_rail/Dockerfile` (the M1 artifact `COPY`, and the closure-guard comment), `.dockerignore:112-122`, `scripts/c1_image_validation.sh` `LISTENER_FILES` (exact-inventory diff), `tests/ops/test_c1_rail_image_manifest.py` (`_ENTRYPOINTS` includes the server and the arm CLI).
   - `ops/c1_rail/book_account_owner.py`: fence states (`:273-279`); `_request_classification_db` (`:843-880`; STALE is re-derived on every read, so fresh evidence clears it today); the entry/add admission branch (`:1787-1791`, `unknown_order`); the takeover risk-add branch (`:1767-1785`); `check_source_silence` (`:1029-1048`); `halt` (`:1294`).
   - `ops/c1_rail/book_halt.py` (halt-only store; reasons include `feed`) and `ops/c1_rail/qualification/trust_domain.py:146`, which names `c1_rail.book_account_owner`.
   - S3 only, after #619 merges: `ops/c1_signal_daemon/bar_source_contract.py`, `book_evaluate_loop.py`, `book_runtime.py:349-373`, `book_session_calendar.py` (`load_ratified_calendar`), and the two ratified calendar JSONs.
3. **Findings returned before code** (the coordinator acknowledges each):
   - (a) Whether any §2 file is in the T00 P7 40-module first-party closure or the 68-module Stage 1c measured closure. Also whether editing `book_account_owner.py` changes a digest that `trust_domain.py`, `prepare_compute` or any qualification manifest pins. Any yes is a **stop**.
   - (b) Where the owner's SQLite schema is versioned, and whether a new latch table needs `book_migration*.py` or a bootstrap-digest change. If it does, **stop** (D-7).
   - (c) Whether an owned parser exists for the FBR digest inside an admitted row's `provenance`. If none exists, return NEEDS_CONTEXT (D-6); never invent one.
   - (d) Whether Docker is usable locally for the two build-state checks (D-1). If not, return that item as owed; never substitute a static check and call it verified.
   - (e) The scheduled-flatten and exit dispatch paths in the owner. They must not pass the entry/add branch the latch guards (`file:line`).

## 0.5. Routing and clarifying questions

Codex local, under the umbrella's routing. Not the GLM lane: this is security-relevant arming, interlock and admission code. No secrets, `.env`, Pine, ports or account data are involved. Every fixture is synthetic, and nothing reads `/data` or a host. The coordinator answers §12 at freeze. An open decision that Phase 0 needs is returned as NEEDS_CONTEXT, never assumed.

## 1. Goal

Build, offline and synthetic only, the fail-closed activation interlock that the ADR assigns to TB-I3. The image must refuse to arm or to boot armed without a validated M1, a validated deployment GO and a validated book-route monitoring acceptance. Admission must stay closed for the rest of a session once order-level evidence has gone stale. The offline R-A2 four-source slice lands when its prerequisite clears. **The boundary:** nothing here arms, deploys, touches a host or an account, or wires the REST book route. Production stays blocked by construction: no producer for the effective-activation acknowledgment exists, so a production boot can never come up armed under this card (§2.3).

## 2. Scope

Three slices, sequential, one writer, one branch. Each slice returns to the coordinator before the next starts.

### 2.1 S1: the deployment-GO validator (`ops/c1_rail/deployment_go.py`, new)

- **Schema.** A closed field set, exactly ADR T10 (`:99`): `status`, `replay_fingerprint_sha256`, `execution_fingerprint_sha256`, `snapshot_seal_sha256`, `n3_result_sha256`, `decision_record`, `go_recorded_at`, `valid_until`, `operator`. Missing or extra fields refuse. Every `*_sha256` value is 64 lowercase hex characters. `status == "GO"`. Timestamps are timezone-aware, with `go_recorded_at < valid_until`.
- **`validate(path, *, now, ...) -> list[str]`**, in the M1 validator's style (empty list = valid). It is fail-closed on a missing, unreadable, non-object or malformed artifact. The T11 comparisons (`:100`) go only through `policy_fingerprint`: `replay_fingerprint_sha256` must equal the FBR digest in the admitted row's provenance (finding (c)), and the normalized `dd_geometry.py` and full `book_policy.py` digests must equal the running files. Today an empty registry refuses ("no admitted row").
- **Attested inputs stay attested.** Where T11 names an operator host read (the EF2 image/config manifest digest, the GO's own SHA-256 against the TB-D2 record, the no-activity attestation bound to S), the code checks presence, shape and binding, and records the input. It never claims to have verified the broker or the host (ADR `:105`; no account read API exists).
- **Baked path only.** `DEFAULT_GO_PATH = _REPO_ROOT/docs/notes/rail_build/DEPLOYMENT_GO.json`. No config key and no environment variable may redirect the path that the boot gate reads.

### 2.2 S1: the `--arm` check (`ops/c1_rail/c1_rail_arm.py`)

- `plan_arm` additionally refuses unless all of these hold: `deployment_go.validate` passes; the book-route monitoring acceptance validates (§2.4); the typed inputs `--ef2-manifest-sha256`, `--go-sha256` and `--no-activity-attestation <file>` are present and well-formed; and the two-field transition passes `policy_fingerprint.validate_initial_arm_delta` (only `dry_run` and `armed_until` change).
- The arm evidence (the typed inputs, the GO digest, the M1 status and the gate verdicts) is appended to the events ledger as an `arm_evidence` event **before** the config write. This is the existing deviation-record ordering: if the ledger refuses, the arm does not happen.
- `--acknowledge-m1-unresolved` is unchanged at arm time. Whether boot honors it is D-3.
- `--status` gains one `go_gate:` line and one `book_monitoring_gate:` line, built from the same predicates.

### 2.3 S1: the host boot gate (`ops/c1_rail/c1_rail_http_server.py` `load_config`)

- When the config says `dry_run=false`, boot additionally requires: M1 `validate(require_resolved=True)` on the **baked** artifact; `deployment_go.validate` on the baked GO; the book-route monitoring acceptance; and an **effective-activation acknowledgment** (`activation_ack_reason`). A failure is an **implicit disarm** in memory with a CRITICAL log naming the gate. It never raises and never rewrites the config, the same pattern as `:184-193`, and for the same reason: a guard that crash-loops the host removes the operator's ability to flatten.
- **No producer for the acknowledgment ships in this card.** `activation_ack_reason`'s production default refuses ("effective activation not implemented: TB-I3 activation slice", D-5). Tests inject a synthetic acknowledgment source, so the positive path is still reachable and tested. This is the "production blocked" construction.
- This boot gate closes the bypass AGENTS.md records (an edit to the `/data` config skips the arm helper): every check reads baked paths, and none reads the volume config.
- The existing positive control `test_boot_accepts_armed_with_future_deadline` **changes outcome by design**. It is replaced by a positive control that injects every valid synthetic input, plus a case showing that the old inputs alone now boot disarmed. This is the one sanctioned change to an existing test's outcome.

### 2.4 S1: the book-route monitoring acceptance gate (TB-I4-M1)

- A predicate `book_monitoring_reason(path)` over a baked artifact (`docs/notes/rail_build/BOOK_ROUTE_MONITORING_ACCEPTANCE.json`, proposed), consumed by both §2.2 and §2.3. It fails closed on absence.
- **The evidence items are T13's to define (D-MON, #606), not this card's.** The validator implements a closed skeleton (`status`, `items[]`, `operator_signoff`, `evidence_ids`), with the required item list as a frozen input at the freeze (D-4). No real artifact is committed; fixtures live under `tests/` only.

### 2.5 S1: image lines (D-1; recommended in scope)

- `deploy/c1_rail/Dockerfile`: add `ops/c1_rail/deployment_go.py` to the rail `COPY`. Replace the M1 artifact line with one absence-tolerant `COPY` (`docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json docs/notes/rail_build/DEPLOYMENT_GO.jso[n] docs/notes/rail_build/BOOK_ROUTE_MONITORING_ACCEPTANCE.jso[n] ./docs/notes/rail_build/`) and update the comment. `.dockerignore`: two re-include lines plus the "ONLY docs/ path" comment. `scripts/c1_image_validation.sh`: the `LISTENER_FILES` line for `deployment_go.py`.
- **Both build states verified** (ADR `:105`): a local build with both artifacts absent (v1) and one with synthetic fixtures present (v2, built from a scratch context, never committed), each recording the files present under `/app/docs/notes/rail_build/`. These builds are local only: no tag pushed, no registry, no `fly`.

### 2.6 S2: the A12-STALE no-auto-resume latch (`ops/c1_rail/book_account_owner.py`)

- **Trigger:** an entry/add request bound to session X reaches fence state STALE (ii) (D-7 decides whether this is on observation or derived retrospectively).
- **Effect:** a durable, account-bound latch row keyed by `session_id`. While the bound session is X, every risk-add is refused with the new refusal `stale_evidence_latched`, on both the ordinary entry/add branch and the takeover risk-add branch. This holds whatever happens afterwards: fresh working evidence, a terminal, a restart or a new boot. The latch does not carry into the next session; any request still STALE there re-latches by derivation.
- **Not an incident:** no `halt`, no `_halt_db`, authority stays NORMAL, and the fence set is unchanged for every other consumer (loosening-amend refusal, recovery, deadline, cutoff).
- **Continues:** exits, flat, cancels, tightening amends, first attaches and the scheduled flatten (finding (e)).
- First release only, as ruled. The code carries no release switch; changing it for a later release needs its own ruling.

### 2.7 S3: the offline R-A2 slice (prerequisite: #619 merged)

Reconstructed from the restored R-A2 draft summary. The full draft (`ra2-offline-card-DRAFT.md`) was lost with the scratchpad, so the coordinator confirms this list at freeze (D-10).
- **New `ops/c1_signal_daemon/book_sources.py`:** `compose_book_sources` builds exactly four `ContractBarSource`s from `LEG_FEEDS`, keyed in `LEG_ORDER`, and refuses duplicate legs, provider codes or venue contracts. The session-window callable is built from `load_ratified_calendar`: it returns `(opens_at, closes_at)` for a row only if `permission == "PERMITTED"` and not `overlay_blocked`, else `None`. It uses `closes_at`, not the risk-add cutoff, because exits need bars after the cutoff. No calendar code or data changes.
- **Edit `ops/c1_signal_daemon/book_evaluate_loop.py` `FourLegEvaluateLoop.step`:** poll all four sources, **then** check health, **then** feed bars. Inside the bound session, a source whose `state` string is `REFUSED` or `DISCONNECTED` calls `owner.halt("source-unhealthy:<session_id>:<leg>:<detail>", "feed", now=now)` (D-2 adds the session id). The loop reads the `state` string only: no import of `bar_source_contract` or `book_sources` into the loop (daemon image closure). It never calls `healthy()`. Having no bar yet at session open does not halt; silence stays with `check_source_silence`.
- **Not wired:** `daemon.py`, `build_loop`, the CLI, `deploy/c1_signal_daemon/**` and the image-manifest tests are untouched until the live packet.

### 2.8 Files

**Allowed.**
- S1 new: `ops/c1_rail/deployment_go.py`, `tests/ops/test_deployment_go.py`.
- S1 edits: `ops/c1_rail/c1_rail_arm.py`, `ops/c1_rail/c1_rail_http_server.py`, `deploy/c1_rail/Dockerfile` (the §2.5 lines only), `.dockerignore` (the §2.5 lines only), `scripts/c1_image_validation.sh` (one `LISTENER_FILES` line). Extend in place: `tests/ops/test_c1_rail_arm.py`, `tests/ops/test_c1_rail_http_server.py`.
- S2: `ops/c1_rail/book_account_owner.py` (latch only), `tests/ops/test_book_stale_admission_latch.py` (new).
- S3: `ops/c1_signal_daemon/book_sources.py` (new), `ops/c1_signal_daemon/book_evaluate_loop.py`, `tests/ops/test_book_sources.py` (new), `tests/ops/test_book_loop_source_health.py` (new).
- Synthetic fixtures under `tests/` only.

**The coordinator records the footprint amendment at freeze.** The umbrella row (`:232`) lists `deploy/*` and the arm module, but not `deployment_go.py` (ADR §2c `:118`: "coordinator extends the manifest footprint"), `c1_rail_http_server.py` or `book_account_owner.py`.

## 3. Method

- Tests first. Each §4 case is written and shown failing on the freeze base with a launcher record, then passing on the build. Preservation cases stay green on both; no red evidence is fabricated for them.
- Fail-closed by default: every new predicate returns a reason or `None`, and an exception inside a predicate is a refusal, never a pass.
- One schema owner per artifact: the M1 validator for M1, `deployment_go` for the GO, the §2.4 validator for monitoring, and `policy_fingerprint` for every digest.
- Configuration as code: baked artifact paths are module constants resolved from `_REPO_ROOT`. Test seams are keyword injection, never config keys.

## 4. Acceptance checks (falsifier-first)

**H:** with this card built, no synthetic trace reaches an armed process or an admitted risk-add unless M1, the GO, the book-route monitoring acceptance and an injected activation acknowledgment all validate. Production defaults never arm. Once order-level evidence has gone stale in a session, no risk-add is admitted in that session, while exits and the scheduled flatten still run. **Reject if** a case below cannot be made to fail on the base, fails on the build, or any preservation test changes outcome (except the one sanctioned in §2.3). **Revert trigger:** any existing arm, boot or fence test outcome changes beyond §2.3's sanctioned replacement.

**S1 fail-first cases**
1. GO validation refuses each of: missing, unreadable, non-object, missing or extra field, `status != GO`, a malformed digest, a naive timestamp, `go_recorded_at >= valid_until`, `valid_until <= now`, an empty registry, a row/FBR mismatch, and a running `dd_geometry.py` or `book_policy.py` digest mismatch. A valid synthetic GO with a synthetic admitted row passes.
2. `--arm` refuses without a valid GO, without valid monitoring, without each typed input, with a malformed input, and with any config change beyond the two fields (`validate_initial_arm_delta`).
3. The arm evidence is written before the config. If the ledger refuses, the config is byte-identical afterwards.
4. Boot with `dry_run=false` and a future deadline implicitly disarms, logs CRITICAL, raises nothing and leaves the config file unchanged, for each failing gate in turn: M1, GO, monitoring and the activation acknowledgment.
5. **Production default:** with every artifact valid but no injected acknowledgment source, boot disarms.
6. **Bypass closed:** a config key naming an alternative M1, GO or monitoring path is ignored at boot (the baked path is still read), and a forged status-only M1 at the baked path disarms.
7. Positive control: every input valid and an injected acknowledgment, so boot comes up armed (the replacement for `test_boot_accepts_armed_with_future_deadline`).
8. Image guards: `test_c1_rail_image_manifest.py` is green with `deployment_go.py` in the closure, and **red** on a copy of the Dockerfile with the new `COPY` removed (a planted-defect run, not committed).
9. Both build states (§2.5) are recorded, or returned as owed under finding (d).

**S2 fail-first cases**
10. STALE, then fresh working evidence, then entry: refused `stale_evidence_latched` (today it is admitted).
11. STALE, then terminal, then add: refused. The same holds for the takeover risk-add branch.
12. STALE, then a restart (new boot) in the same session, then entry: refused. The latch is durable.
13. Next session: a request with no stale history is admitted, subject to every other gate.
14. While latched, exit, flat, cancel, a tightening amend and the scheduled flatten all proceed. No halt or incident is recorded, and authority stays NORMAL.
15. The fence set returned to other consumers is unchanged by the latch (a loosening amend refuses exactly as before).

**S3 fail-first cases**
16. `test_four_sources_one_per_symbol`: exactly four sources keyed in `LEG_ORDER`, and duplicate legs, provider codes or venue contracts refuse.
17. Session window: `None` for DENIED and overlay-blocked rows; `(opens_at, closes_at)` for PERMITTED rows.
18. Calendar tripwire: the test reads the **raw calendar JSON** and asserts that each PERMITTED row's product closes equal `closes_at`, on both ratified calendars (the loaded `SessionSchedule` drops per-product closes, and `v` folds in the venue deadline).
19. An in-session `REFUSED` or `DISCONNECTED` source halts with reason `feed` at once. The same states outside the session do not halt. Having no bar yet at open does not halt.
20. **Poll-all-then-check:** an earlier leg's bar cannot complete a barrier and dispatch in a step where a later leg is unhealthy.
21. The loop never calls `healthy()`, and its import closure stays inside the daemon image (`test_c1_signal_daemon_image_manifest.py` green).
22. Incident ids differ across sessions (D-2).

**Preservation (green before and after, unchanged):** `test_validate_c1_monitoring_acceptance.py`; every existing `test_c1_rail_arm.py` and `test_c1_rail_http_server.py` case except the §2.3 replacement; `test_book_account_owner.py`, `test_pr409_review4.py`, `test_book_feedback_journal.py`, `test_book_close_reconciliation.py`, `test_four_leg_runtime.py`, `test_feed_omission_session_end.py`, `test_c1_signal_daemon_image_manifest.py`.

**Runs** (each with its launcher record; cite `record.json`, `verification_exit_code`, `source_stable`):
- `python -I scripts/fp.py doctor`
- `python -I scripts/fp.py python -m pytest <the authority-block acceptance list>`
- `python -I scripts/fp.py test-ops`
- `python -I scripts/fp.py check`
- `git diff --check`

A pre-existing gate failure is disclosed, never described as a pass.

## 5. Forbidden

- Any route code: the REST book route, CrossTrade or Tradovate transports, `crosstrade_payload.py`, `c1_rail_listener.py` send paths, T09 code, and route wiring in `daemon.py`, `build_loop` or the CLI.
- `deploy/**`, except the §2.5 lines in `deploy/c1_rail/Dockerfile`. In particular: `fly.toml`, `deploy/c1_signal_daemon/**`, `deploy/qualification/**`, any `fly` command, any image push or registry tag, any host read or write, and `/data`.
- Arming configuration: the `/data` config, `armed_until`, `dry_run` on any host, `ARMING_PROCEDURE.md`, and invoking `--arm`, `--disarm` or `--acknowledge-m1-unresolved` against anything but a temporary test path.
- `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` (no edit); committing any `DEPLOYMENT_GO.json` or `BOOK_ROUTE_MONITORING_ACCEPTANCE.json` outside `tests/`.
- `core/dd_protection.py`, `core/dd_geometry.py` (including `POLICY_REGISTRY`), `core/firm_rules.py`, `core/lifecycle.py`, `book_policy.py`, `policy_fingerprint.py` (consume only), and `c1_sizing_host_reference.py`.
- Pine sources, runtime ports, `PORT_MANIFEST.sha256`, `BOOK_SOURCES.sha256`, and any private value.
- In S3: calendar code and data, `bar_source_contract.py` (the #619 file), `book_account_owner.py`, `daemon.py`, the CLI and the daemon image-manifest tests.
- The umbrella, ADRs, specs, STATE and the ledger (coordinator-reserved); GLM; opening a PR, merging, or pushing to `main`.

## 6. Return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED, per slice. The coordinator's verdict is RESOLVED (every §4 item for the slice holds) or FALSIFIED (named items fail; returned to the executor). The return holds:
- branch, head SHA and base; `git diff --stat` and the name list;
- Phase-0 findings (a)–(e);
- per case, the fail-on-base and pass-on-build launcher record IDs;
- the preservation results and the planted-defect image-guard output;
- the two build-state listings, or the owed note;
- concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- Phase-0 findings (a)–(e): return them, then wait for the coordinator before code.
- A closure-member or pinned digest would change (finding (a)); a schema migration is needed (finding (b)); no owned provenance parser exists (finding (c)).
- Any change outside §2.8, a host or network action, or a real artifact would be needed.
- S3 before #619 has merged, or #619 merges with a `state` vocabulary different from `REFUSED` / `DISCONNECTED`.
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, stop folding; the coordinator adjudicates a rewrite or a narrower scope.
- A second writer appears on the branch.

## 8. Out of scope and decision unlocked

**Out of scope:**
- The effective-activation protocol itself: the pending request, the restart, the boot-bound fresh no-activity attestation, and the durable acknowledgment producer (D-5).
- Later-session rearming (ADR `:109`).
- TB-D2's GO write and reseal proof; TB-D0's row; TB-V1's binding; TB-O1's procedure; the TB-I3 live packet.
- The D-MON-1 notifier (`claude/book-incident-notifier`).
- The T09 split design, GC-5-DISPLACED and ED-10-SPLIT.
- The #619 revision latch (Q1). It is a source-state latch, not A12-STALE.

**Unlocked:** with S1–S3 RESOLVED and the Codex relay clean, the interlock exists in source, so an image built from it refuses to arm or boot armed until TB-D2's GO, T13's monitoring acceptance and the activation slice exist. A12-STALE moves from "owed" to "implemented, synthetic" in its owner rows (written by the coordinator).

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: well-formed; 0 violations.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-tb-i3-synthetic-interlock-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-tb-i3-synthetic-interlock-card-DRAFT.md
# Premise (Git Bash), in the executor worktree.
git rev-parse HEAD; test ! -e .env && echo "no .env" || echo "FAIL: .env present"
grep -n "^POLICY_REGISTRY" core/dd_geometry.py            # expected: empty dict
test ! -e docs/notes/rail_build/DEPLOYMENT_GO.json && echo "no GO"   # expected: no GO
grep -n "M1\|deployment_go" ops/c1_rail/c1_rail_http_server.py      # expected before S1: no boot M1/GO check
gh pr view 619 --json state -q .state                      # S3 gate: MERGED
# Scope at return.
git diff --stat "$BASE"...HEAD; git diff --name-only "$BASE"...HEAD -- deploy | grep -v '^deploy/c1_rail/Dockerfile$' && echo "FAIL: deploy scope"
```

## 12. Open decisions (for coordinator (3) at freeze)

- **D-1 Dockerfile `COPY` and "no deploy" (coordinator scoping call). Recommended: in scope, limited to the §2.5 lines.**
  - "No deploy" is the operator act `rail.deploy` (`fly deploy`; `scripts/seat_authority.yml`). Editing a build recipe that only a later, separately authorized deploy would consume is source work. Nothing reaches a host, and merging stays the operator's.
  - The existing guards force it. Once the server and arm CLI import `deployment_go.py`, `test_listener_import_closure_is_covered_by_dockerfile_copy`, `test_packaged_files_are_allowed_in_build_context` and `test_ci_exact_inventory_includes_packaged_python_modules` fail without the `COPY`, the `.dockerignore` and the `LISTENER_FILES` lines. Omitting them reproduces the 2026-07-31 green-build/dead-container class.
  - ADR §2b/§2c (`:103`, `:118`) assigns the absence-tolerant `COPY` and the two-state build check to TB-I3. Absence is the fail-closed state, so an image built from this card refuses the arm by itself.
  - Bound: no `fly.toml`, no daemon image, no push. Local builds only (finding (d)). If the coordinator rules it out, S1 cannot import `deployment_go` into the boot path, and the boot gate (the core of the ruling) must wait too. Ruling it out therefore defers S1 rather than narrowing it.
- **D-2 Incident-id uniqueness (R-A2 D-2).** Recommended: include the session id.
- **D-3 Boot-gate scope and the M1 acknowledgment.** Recommended: universal. Every `dry_run=false` boot in an image carrying this code needs M1, the GO, monitoring and the acknowledgment. Keying the gate off a config mode would reopen the `/data` bypass. Consequence: the 2026-09-26 `--acknowledge-m1-unresolved` discretion still writes its arm-time record, but it can no longer produce an armed boot, so legacy single-leg arming ends until the GO path exists. No current consumer needs an armed legacy rail (M1 item 5 is "no arm"; the book is undeployed). This narrows an operator-ratified discretion, so **Joshua confirms it** before freeze (do not change an operator-agreed rule unilaterally).
- **D-4 The book-route monitoring item list.** T13/D-MON (#606) owns the content. Freeze either the skeleton plus the item list from #606, or the skeleton with an empty required list that refuses (fail-closed) until T13 supplies one. Recommended: the latter, with the artifact path fixed now so the `COPY` line lands once.
- **D-5 Effective activation.** Recommended: a separate TB-I3 activation slice (request → restart disarmed → fresh boot-bound attestation → durable acknowledgment before risk-add, with the ADR `:105` traces: delayed restart, intervening activity, changed image or config, replayed attestation, missing acknowledgment, crash). This card ships only the refusing default and the injected-source seam.
- **D-6 FBR in provenance.** If finding (c) shows no owned parser, the owner is TB-I1 (`policy_fingerprint`) or TB-D0. Recommended: TB-I1 adds `provenance_fbr_digest()` under its own card, and S1's GO comparison waits behind it.
- **D-7 Latch trigger and storage.** Either latch on observation (every classification read, plus a per-bar check from the loop) or derive it retrospectively from durable preparation and acquisition times. Recommended: retrospective derivation, with the latch row as a durable cache. Observation-only latching misses a stale window in which no request was evaluated, and "once evidence has gone stale" does not depend on being observed. A schema change that touches `book_migration*.py` is a stop (finding (b)).
- **D-8 Executor.** Codex local (recommended, umbrella routing) or a Claude worker. GLM is excluded either way.
- **D-9 Freeze base and record prerequisite.** The c2 batch ledger PR must land the TB-I3-CARD, A12-STALE and TB-I4-M1 records at their owners (recording plan §1.5, §1.16 and the A12 rows) before freeze, so this card cites them on `main`. Recommended base: `main` after that merge.
- **D-10 The R-A2 reconstruction.** The original 12-test draft is lost. Confirm §2.7 and cases 16–22, and the R-A2 draft's open D-1 (an immediate halt on any in-session `DISCONNECTED`, so #619's reconnect cannot recover in session; implemented strictly as frozen) and D-3 (the spec names `daemon.py` and this slice uses a new module; annotating the spec is the coordinator's).
- **D-11 File collision.** D-MON-1's notifier ("rail-side bounded publish plus heartbeat (TB-I3 scope)") is likely to touch `c1_rail_http_server.py` and telemetry. Sequence the two cards; no two live packets share a file (umbrella `:245`).

## Pre-mortem (README rule)

- **Loop cost:** three Windows build loops with launcher records, plus two local image builds. No Linux run, no host.
- **Decisions the executor will hit:** D-1, D-3, D-6 and D-7. They are ruled in one batch at freeze.
- **What makes it moot:** an operator ruling that withdraws the TB-I3 synthetic authorization, a route change that removes the c1 listener host, or the attempt ending (R1a/R1b) before an image matters.
- **Measurements the return fills in:** Phase-0 findings (a)–(e), per-case records, the planted-defect guard output and the build-state listings.
