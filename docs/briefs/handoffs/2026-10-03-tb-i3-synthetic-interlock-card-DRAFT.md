# TB-I3 synthetic-scope activation interlock (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT — coordinator (3) freezes. Drafted 2026-10-03 by a coordinator-(3) worker; not dispatched. D-3 is RULED U by Joshua (§11). Coordinator (3) answers the remaining open §11 items, commits the frozen revision under the committed-handoff rule and records its SHA in the ledger before any executor starts. Dispatch is a separate decision.

**Authority:** Operator ruling 2026-10-02 (sitting 2), TB-I3-CARD: card now, synthetic scope only. No arm, no deploy, no route integration; production blocked. Dispatch is separate.

**Rulings folded in (all "operator ruling 2026-10-02 (sitting 2)", Joshua "all recommended", 2026-10-03T01:42Z):**
- **TB-I3-CARD:** the activation-interlock card (`deployment_go.py` validator, `--arm` check, host boot gate checking M1 and the GO) may be written now, synthetic scope only. This narrows the TB-I1 prerequisite for this card only (umbrella `:232` TB-I3 row, appended by the c2 batch).
- **A12-STALE** (effective with D1: #575 is open and §A12 stays PROPOSED until the D1 acceptance act): stale order-level evidence remains a refusal, not an incident. Fresh evidence alone never lifts it; in the first release admission stays closed for the rest of the session. Risk-reducing exits and the scheduled flatten continue. TB-I3 implements the latch (owner row: [bounded incident contract `:536`](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md); halt/resume [O-1 `:106`](../../spec/2026-09-14-tb-s3-halt-resume-contract.md)). Armed commissioning and later releases are not decided.
- **TB-I4-M1:** M1 stays retained and does not cover the book host. Book-host monitoring evidence is the book-route monitoring acceptance added in T13/TB-I3. TB-I4 as written is not a book-route prerequisite (D-B13 amendment).

**Executor:** proposed Codex local (the umbrella's TB-I3 routing, `:232`), single writer of `codex/tb-i3-synthetic-interlock` (proposed), cut from the freeze base. **Not GLM:** arming, interlock and risk-admission code (AGENTS.md GLM rule).

**Coordinator:** coordinator (3). It owns the freeze, diff review, integration, the Codex relay, PRs and the ledger.

**Owners this card narrows (it changes none of them):**
- [Book protection admission ADR](../../adr/2026-09-12-tradeify-book-protection-instance-admission.md): §2a T10–T11 (`:99-100`), §2b validator and interlock (`:102-107`), initial-activation-only rule (`:109`), §2c TB-I3 row (`:118`).
- [Multi-leg rail extension spec](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) R-L (`:161`).
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
  - tests/ops/test_four_leg_runtime.py
  - tests/ops/test_feed_omission_session_end.py
```

`test_deployment_go.py` and `test_book_stale_admission_latch.py` are new. The rest exist and are extended in place or must stay green unchanged (§4).

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

1. **Premise.** HEAD descends from the freeze base (D-9). As drafted, `origin/main` is `1a350ec`. `POLICY_REGISTRY` is empty (`core/dd_geometry.py:92`). No `DEPLOYMENT_GO.json` exists. `ops/c1_rail/policy_fingerprint.py` exists (TB-I1). Before S2 only: #628 (`claude/book-incident-notifier`, head `60ba482` as drafted) and the GC-5-DISPLACED build PR have both merged, and the branch has merged an `origin/main` containing both (§9). No `.env` in the worktree.
2. **Rule-0 reads** (read them; do not infer them):
   - `ops/c1_rail/c1_rail_arm.py`: `m1_acceptance_reason` and `m1_acceptance_structurally_valid` (validator-backed, fail-safe); `plan_arm` (pure); `_record_deviation`, written **before** the config; the hidden `--acceptance` test seam.
   - `ops/c1_rail/c1_rail_http_server.py:142-219` `load_config`: boot **implicit disarm** in memory, never a raise, for an invalid window (2026-07-31 crash-loop lesson, `:160-193`). The one boot raise is a missing `events_log_path` (`:155-158`). The boot gate checks neither M1 nor any GO (AGENTS.md live-execution posture).
   - `scripts/validate_c1_monitoring_acceptance.py:81` `validate(path, *, require_resolved)`, which returns an error list. It is the schema owner; never re-implement it.
   - `ops/c1_rail/policy_fingerprint.py`: `canonical_policy_bytes`, `normalized_geometry_bytes`, `validate_registry` (expected rows supplied independently, `:181`), `validate_initial_arm_delta` (`:241`), `build_shared_manifest` and `verify_shared_manifest`. ADR `:76` forbids an independent reimplementation.
   - `deploy/c1_rail/Dockerfile` (the M1 artifact `COPY`, and the closure-guard comment), `.dockerignore:112-122`, `scripts/c1_image_validation.sh` `LISTENER_FILES` (exact-inventory diff), `tests/ops/test_c1_rail_image_manifest.py` (`_ENTRYPOINTS` includes the server and the arm CLI).
   - `ops/c1_rail/book_account_owner.py`: fence states (`:273-279`); `_request_classification_db` (`:843-880`; STALE is re-derived on every read, so fresh evidence clears it today); the entry/add admission branch (`:1787-1791`, `unknown_order`); the takeover risk-add branch (`:1767-1785`); `check_source_silence` (`:1029-1048`); `halt` (`:1294`); the terminal branch of `_observe_locked` (`:2091`), its `MAX_FACT_AGE` ingestion bound (`:2121`) and the terminal capacity append (`:2248`). These line numbers are at `1a350ec`; #628 and GC-5 move them, so re-locate each on the S2 base.
   - `ops/c1_rail/book_halt.py` (halt-only store; reasons include `feed`) and `ops/c1_rail/qualification/trust_domain.py:146`, which names `c1_rail.book_account_owner`.
3. **Findings returned before code** (the coordinator acknowledges each):
   - (a) Whether any §2 file is in the T00 P7 40-module first-party closure or the 68-module Stage 1c measured closure. Also whether editing `book_account_owner.py` changes a digest that `trust_domain.py`, `prepare_compute` or any qualification manifest pins. Any yes is a **stop**.
   - (b) Where the owner's SQLite schema is versioned. The latch adds no table or row (D-7); confirm that it needs no `book_migration*.py` or bootstrap-digest change. If it would, **stop**.
   - (c) Whether an owned parser exists for the FBR digest inside an admitted row's `provenance`. If none exists, return NEEDS_CONTEXT (D-6); never invent one.
   - (d) Whether Docker is usable locally for the two build-state checks (D-1). If not, return that item as owed; never substitute a static check and call it verified.
   - (e) The scheduled-flatten and exit dispatch paths in the owner. They must not pass the entry/add branch the latch guards (`file:line`).
   - (f) Whether the durable rows the boot derivation reads (`operations.session_id`, `operations.created_at`, the attempt rows and the accepted-terminal `capacity_events` rows with their `as_of`) are retained, or overwritten in place. Order evidence is not among them: it is per boot and never persisted (`book_account_owner.py:368-371`; the evidence path "never writes durable state", `:934`). Also whether every accepted entry/add terminal passed the `MAX_FACT_AGE` ingestion bound (`:2121`), including any migration path (`book_migration.py:88`), so that `as_of + MAX_FACT_AGE` bounds when it became visible. If any listed row is overwritten, or any accepted entry/add terminal bypasses the bound, **stop** (D-7).

## 0.5. Routing and clarifying questions

Codex local, under the umbrella's routing. Not the GLM lane: this is security-relevant arming, interlock and admission code. No secrets, `.env`, Pine, ports or account data are involved. Every fixture is synthetic, and nothing reads `/data` or a host. The coordinator answers the open §11 items at freeze; D-3 is RULED U. An open decision that Phase 0 needs is returned as NEEDS_CONTEXT, never assumed.

## 1. Goal

Build, offline and synthetic only, the fail-closed activation interlock that the ADR assigns to TB-I3. The image must refuse to arm or to boot armed (scope per D-3) without a validated M1, a validated deployment GO and a validated book-route monitoring acceptance. Admission must stay closed for the rest of a session once order-level evidence has gone stale. **The boundary:** nothing here arms, deploys, touches a host or an account, or wires the REST book route. Production stays blocked by construction: no producer for the effective-activation acknowledgment exists, so a production boot can never come up armed under this card (§2.3).

## 2. Scope

Two slices, sequential, one writer, one branch. Each slice returns to the coordinator before the next starts. S2 starts only after its predecessors on `book_account_owner.py` merge, from a branch head that has merged that `origin/main` (no rebase; §9).

### 2.1 S1: the deployment-GO validator (`ops/c1_rail/deployment_go.py`, new)

- **Schema.** A closed field set, exactly ADR T10 (`:99`): `status`, `replay_fingerprint_sha256`, `execution_fingerprint_sha256`, `snapshot_seal_sha256`, `n3_result_sha256`, `decision_record`, `go_recorded_at`, `valid_until`, `operator`. Missing or extra fields refuse. Every `*_sha256` value is 64 lowercase hex characters. `status == "GO"`. Timestamps are timezone-aware, with `go_recorded_at < valid_until`.
- **`validate(path, *, now, ...) -> list[str]`**, in the M1 validator's style (empty list = valid). It is fail-closed on a missing, unreadable, non-object or malformed artifact. The T11 comparisons (`:100`) go only through `policy_fingerprint`: `replay_fingerprint_sha256` must equal the FBR digest in the admitted row's provenance (finding (c)), and the normalized `dd_geometry.py` and full `book_policy.py` digests must equal the running files. Today an empty registry refuses ("no admitted row").
- **Attested inputs stay attested.** Where T11 names an operator host read (the EF2 image/config manifest digest, the GO's own SHA-256 against the TB-D2 record, the no-activity attestation bound to S), the code checks presence, shape and binding, and records the input. It never claims to have verified the broker or the host (ADR `:105`; no account read API exists).
- **Baked path only.** `DEFAULT_GO_PATH = _REPO_ROOT/docs/notes/rail_build/DEPLOYMENT_GO.json`. No config key and no environment variable may redirect the path that the boot gate reads.

### 2.2 S1: the `--arm` check (`ops/c1_rail/c1_rail_arm.py`)

- **Scope per D-3 = U:** every `--arm`, legacy single-leg included. `plan_arm` additionally refuses unless all of these hold: `deployment_go.validate` passes; the book-route monitoring acceptance validates (§2.4); the typed inputs `--ef2-manifest-sha256`, `--go-sha256` and `--no-activity-attestation <file>` are present and well-formed; and the two-field transition passes `policy_fingerprint.validate_initial_arm_delta` (only `dry_run` and `armed_until` change).
- The arm evidence (the typed inputs, the GO digest, the M1 status and the gate verdicts) is appended to the events ledger as an `arm_evidence` event **before** the config write. This is the existing deviation-record ordering: if the ledger refuses, the arm does not happen. An `arm_evidence` event with no matching config write (the ledger write succeeded, the config write failed) is an orphan: no reader treats it as armed, and a retry writes fresh evidence rather than reusing it.
- `--acknowledge-m1-unresolved` is unchanged at arm time and still writes its `arming_deviation` record. Under D-3 = U, boot does not honor it: the boot M1 check requires `RESOLVED` (§2.3), so it can no longer yield an armed rail.
- `--status` gains one `go_gate:` line and one `book_monitoring_gate:` line, built from the same predicates, and one `effective:` line computed by the boot-gate function itself (armed, or disarmed with the failing gate named), not only the `dry_run` the config file holds.

### 2.3 S1: the host boot gate (`ops/c1_rail/c1_rail_http_server.py` `load_config`)

- **Scope per D-3 = U:** every `dry_run=false` boot, legacy single-leg included. When the config says `dry_run=false`, boot additionally requires: M1 `validate(require_resolved=True)` on the **baked** artifact; `deployment_go.validate` on the baked GO; the book-route monitoring acceptance; and an **effective-activation acknowledgment** (`activation_ack_reason`). A failure is an **implicit disarm** in memory with a CRITICAL log naming the gate. It never raises and never rewrites the config, the same pattern as `:184-193`, and for the same reason: a guard that crash-loops the host removes the operator's ability to flatten.
- **No producer for the acknowledgment ships in this card.** `activation_ack_reason`'s production default refuses ("effective activation not implemented: TB-I3 activation slice", D-5). Tests inject a synthetic acknowledgment source, so the positive path is still reachable and tested. This is the "production blocked" construction.
- This boot gate closes the bypass AGENTS.md records (an edit to the `/data` config skips the arm helper) for every route: every check reads baked paths, and none reads the volume config.
- The existing positive control `test_boot_accepts_armed_with_future_deadline` **changes outcome by design**. It is replaced by a positive control that injects every valid synthetic input, plus a case showing that the old inputs alone now boot disarmed. This is the one sanctioned change to an existing test's outcome.

### 2.4 S1: the book-route monitoring acceptance gate (TB-I4-M1)

- A predicate `book_monitoring_reason(path)` over a baked artifact (`docs/notes/rail_build/BOOK_ROUTE_MONITORING_ACCEPTANCE.json`, proposed), consumed by both §2.2 and §2.3. It fails closed on absence.
- **The evidence items are T13's to define (D-MON, #606), not this card's.** The validator implements a closed skeleton (`status`, `items[]`, `operator_signoff`, `evidence_ids`), with the required item list as a frozen input at the freeze (D-4). No real artifact is committed; fixtures live under `tests/` only.

### 2.5 S1: image lines (D-1; recommended in scope)

- `deploy/c1_rail/Dockerfile`: add `ops/c1_rail/deployment_go.py` to the rail `COPY`. Replace the M1 artifact line with one absence-tolerant `COPY` for M1 and the monitoring acceptance (`docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json docs/notes/rail_build/BOOK_ROUTE_MONITORING_ACCEPTANCE.jso[n] ./docs/notes/rail_build/`), plus a **separate** `COPY` line for the GO alone (`docs/notes/rail_build/DEPLOYMENT_GO.jso[n] ./docs/notes/rail_build/`), so the GO's layer holds only the GO (D-4). Update the comment. If the v1 build (GO absent) rejects the all-unmatched GO line, stop and return it; do not add an anchor file. `.dockerignore`: two re-include lines plus the "ONLY docs/ path" comment. `scripts/c1_image_validation.sh`: the `LISTENER_FILES` line for `deployment_go.py`.
- **Both build states verified** (ADR `:105`, D-4): **v1** = M1 as committed plus a synthetic monitoring acceptance, GO absent; **v2** = v1 plus a synthetic GO. Both are built from a scratch context, never committed. Each records the files present under `/app/docs/notes/rail_build/`, and the check asserts that the GO line's layer is the only layer that differs between v1 and v2. Optional **v0**: monitoring acceptance and GO both absent, recording that the build succeeds and the image refuses to arm or boot armed (fail-closed). These builds are local only: no tag pushed, no registry, no `fly`.

### 2.6 S2: the A12-STALE no-auto-resume latch (`ops/c1_rail/book_account_owner.py`)

Design per D-7 (coordinator (3) ruling, option (ii), amended 2026-10-03 on the #633 review P2): an in-memory latch within one boot, plus a fail-closed derivation at boot from retained rows, so admission stays closed for the rest of the session across a restart (A12.5). No new table, no cache row, no schema change (finding (b) stands). Order evidence cannot be a durable input: it is per boot and never persisted (`book_account_owner.py:368-371`, `:934`).

- **Latch:** an in-memory set of latched session ids, empty at construction. Session X is the request's `operations.session_id`. X is latched by any of:
  1. **Observed STALE:** a classification read (`_request_classification_db`) returns STALE (ii) for an entry/add bound to X.
  2. **Unobserved stale window, ended by evidence:** when `observe_synthetic_order_evidence` accepts qualifying evidence for symbol S at its `now`, it first classifies the entry/add requests for S against the evidence held before the overwrite; any STALE latches X. The path still writes no durable state.
  3. **Unobserved stale window, ended by a terminal:** when an accepted terminal for an entry/add bound to X is applied at its `now` (the terminal branch of `_observe_locked`), the owner first classifies that request against the evidence held, as if the terminal were not yet applied; STALE latches X. The terminal path is otherwise unchanged.
  4. **Boot derivation (fail-closed; durable because its inputs are retained):** once per boot, at the first classification read or risk-add admission, with that call's `now`, X is latched if any entry/add bound to the current session X, not transport-rejected, either (a) has no accepted terminal and `now >= created_at + BAR_PERIOD`, or (b) has an accepted terminal with `as_of + MAX_FACT_AGE >= created_at + BAR_PERIOD`. Every accepted terminal passed the `MAX_FACT_AGE` ingestion bound (finding (f)), so (b) covers every request whose terminal may have become visible after its first bar, which includes every request that could have been STALE. It reads only retained rows (`operations.session_id`, `operations.created_at`, the attempt rows and the accepted-terminal `capacity_events` rows) and writes nothing.
- **Effect:** while X is latched, every risk-add admission for X is refused with the new refusal `stale_evidence_latched`, on both the ordinary entry/add branch and the takeover risk-add branch. Within the boot, fresh evidence or a terminal does not clear it. The latch never carries into the next session: a new session's id is not in the set, and the boot derivation reads only rows bound to the current session.
- **Over-refusal cost (accepted; widened 2026-10-03):** after a restart the derivation cannot tell a request that went STALE from one that stayed KNOWN_WORKING, because evidence does not survive the boot. So a restart closes admission for the rest of the session whenever an entry/add of the session is non-terminal past its first bar, or reached its accepted terminal possibly after its first bar, even if evidence never lapsed (case 16). Within one boot the latch stays exact: a request that stays KNOWN_WORKING through its first bar and then fills latches nothing (P4). Exits and the flatten continue, so the cost is lost entries after a restart, not added risk.
- **Rest-of-session closure across a restart (A12.5; the former residual, closed 2026-10-03):** STALE, then an accepted terminal, then a crash or restart in the same session. The in-memory latch is lost, but derivation (b) re-latches X at boot, so admission stays closed until the next session (case 17). The earlier draft accepted this reopening as a D-7 residual. That contradicted the operator's rest-of-session closure ([incident ADR §A12.5](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md) stale-evidence row `:536`, verified on `main` `a83a464`), which a coordinator residual cannot waive, so the residual is withdrawn.
- **Not an incident:** no `halt`, no `_halt_db`, authority stays NORMAL, and the fence set is unchanged for every other consumer (loosening-amend refusal, recovery, deadline, cutoff).
- **Continues:** exits, flat, cancels, tightening amends, first attaches and the scheduled flatten (finding (e)).
- First release only, as ruled, and effective with D1 (§A12 stays PROPOSED until the acceptance act). The code carries no release switch; changing it for a later release needs its own ruling.

**Card change (coordinator (3), 2026-10-03, #633 review P2).** Latch path 3 and derivation (b) are added inside the allowed file (`book_account_owner.py`, latch only). Path 3 sits in the terminal-ingestion branch, which the latch did not touch before; that is the scope expansion, and it is coordinator-owned. No file, table, row, migration or acceptance-list entry is added. A durable latch mark under `book_migration_schema` (D-7's former option (i)) is not needed for the closure.

### 2.7 Files

**Allowed.**
- S1 new: `ops/c1_rail/deployment_go.py`, `tests/ops/test_deployment_go.py`.
- S1 edits: `ops/c1_rail/c1_rail_arm.py`, `ops/c1_rail/c1_rail_http_server.py`, `deploy/c1_rail/Dockerfile` (the §2.5 lines only), `.dockerignore` (the §2.5 lines only), `scripts/c1_image_validation.sh` (one `LISTENER_FILES` line). Extend in place: `tests/ops/test_c1_rail_arm.py`, `tests/ops/test_c1_rail_http_server.py`.
- S2: `ops/c1_rail/book_account_owner.py` (latch only; after #628 and the GC-5 build merge, §9), `tests/ops/test_book_stale_admission_latch.py` (new).
- Synthetic fixtures under `tests/` only.

**The coordinator records the footprint amendment at freeze.** The umbrella row (`:232`) lists `deploy/*` and the arm module, but not `deployment_go.py` (ADR §2c `:118`: "coordinator extends the manifest footprint"), `c1_rail_http_server.py` or `book_account_owner.py`.

## 3. Method

- Tests first. Each §4 case is written and shown failing on the freeze base with a launcher record, then passing on the build. Preservation cases stay green on both; no red evidence is fabricated for them. **Exceptions, each with its own red definition, stated in the return:** case 1 is red at the base only because `deployment_go` does not exist (as GC-5's case 6); the S1 controls-and-evidence group (cases 7, 8, 9, §4) is defined there. Every other fail-first case must be red at the base for its stated reason.
- Fail-closed by default: every new predicate returns a reason or `None`, and an exception inside a predicate is a refusal, never a pass.
- One schema owner per artifact: the M1 validator for M1, `deployment_go` for the GO, the §2.4 validator for monitoring, and `policy_fingerprint` for every digest.
- Configuration as code: baked artifact paths are module constants resolved from `_REPO_ROOT`. Test seams are keyword injection, never config keys.

## 4. Acceptance checks (falsifier-first)

**H:** with this card built, no synthetic trace reaches an armed process or an admitted risk-add unless M1, the GO, the book-route monitoring acceptance and an injected activation acknowledgment all validate. Production defaults never arm. Once order-level evidence has gone stale in a session, no risk-add is admitted in that session for the rest of the session, including after a restart (A12.5; §2.6), while exits and the scheduled flatten still run. **Reject if** a fail-first case below cannot be made to fail on the base for its stated reason (case 1 and the controls-and-evidence group carry their own red definitions, §3), fails on the build, or any preservation test changes outcome (except the one sanctioned in §2.3). **Revert trigger:** any existing arm, boot or fence test outcome changes beyond §2.3's sanctioned replacement.

**S1 fail-first cases**
1. GO validation refuses each of: missing, unreadable, non-object, missing or extra field, `status != GO`, a malformed digest, a naive timestamp, `go_recorded_at >= valid_until`, `valid_until <= now`, an empty registry, a row/FBR mismatch, and a running `dd_geometry.py` or `book_policy.py` digest mismatch. A valid synthetic GO with a synthetic admitted row passes.
2. `--arm` refuses without a valid GO, without valid monitoring, without each typed input, with a malformed input, and with any config change beyond the two fields (`validate_initial_arm_delta`).
3. The arm evidence is written before the config. If the ledger refuses, the config is byte-identical afterwards.
4. Boot with `dry_run=false` and a future deadline implicitly disarms, logs CRITICAL, raises nothing and leaves the config file unchanged, for each failing gate in turn: M1, GO, monitoring and the activation acknowledgment.
5. **Production default:** with every artifact valid but no injected acknowledgment source, boot disarms.
6. **Bypass closed:** a config key naming an alternative M1, GO or monitoring path is ignored at boot (the baked path is still read), and a forged status-only M1 at the baked path disarms.
10. Orphan arm evidence: with the ledger write succeeding and the config write failing, the rail is not read as armed (`--status`, boot), and a retried `--arm` writes a fresh `arm_evidence` event.
11. `--status` with `dry_run=false` in the config but a failing boot gate reports `effective: disarmed` and names the gate.

**S1 controls and evidence (own red definitions; excepted in §3 and §4)**
7. Positive control: every input valid and an injected acknowledgment, so boot comes up armed (the replacement for `test_boot_accepts_armed_with_future_deadline`). **Red:** at the base only because the acknowledgment-injection seam is missing, as for case 1.
8. Image guards: `test_c1_rail_image_manifest.py` is green with `deployment_go.py` in the closure. **Red:** on a copy of the Dockerfile with the new `COPY` removed (a planted-defect run, not committed); it is green at the base.
9. Build states (§2.5): v1 and v2 recorded, with only the GO layer differing (v0 optional). **Red:** none; it is evidence, either recorded or returned as owed under finding (d).

D-3 is RULED U, so cases 2 and 4–7 apply to every route, legacy single-leg included. No legacy-unchanged twin applies.

**S2 fail-first cases** (each asserts `refusal_reason == "stale_evidence_latched"`, not refusal alone, so a refusal for another reason at the base does not pass)
12. Within one boot: STALE observed, then fresh working evidence, then entry: refused (today it is admitted).
13. Within one boot: STALE, then terminal, then add: refused. The takeover risk-add twin turns the takeover on explicitly through GC-5's named test seam, because after GC-5 the default is OFF and the branch is otherwise unreachable: for the owner, the keyword-only `aegis_takeover=None` on `BookAccountOwner.__init__`, forwarded by `BookAccountOwner.boot`, which the test calls (resolved to `book_policy.AEGIS_TAKEOVER` at call time), passed `AegisTakeover.WHOLE_LEG_PRIORITY`; for replay, monkeypatching `c1_rail.qualification.replay.CapacityLedger` with `functools.partial(CapacityLedger, takeover=AegisTakeover.WHOLE_LEG_PRIORITY)`.
14. Boot derivation: STALE, then a restart (new boot) in the same session with the request still non-terminal, then fresh evidence after the restart, then entry: refused.
15. Unobserved stale window within one boot: a request passes `created_at + BAR_PERIOD` with no classification read, then fresh evidence arrives (latch path 2), then entry: refused.
16. Over-refusal by design (§2.6 cost): (a) a request KNOWN_WORKING throughout the prior boot and still non-terminal past its first bar at restart; after the restart, fresh evidence, then entry: refused. (b) A request KNOWN_WORKING through its first bar that then reaches an accepted terminal after it; then a restart in the same session, then entry: refused (derivation (b)).
17. **Rest-of-session latch across a restart (A12.5; red-first, `test_stale_then_terminal_restart_same_session_refuses_next_session_admits`):** STALE observed, then an accepted terminal, then a restart (new boot) in the same session, then fresh evidence, then entry: refused. Then the next session opens, and an entry is admitted, subject to every other gate. **Red at the base:** the same-session entry is not refused with `stale_evidence_latched`. The next-session half is green on both and is shown red against the carry-into-next-session mutant.
18. Unobserved stale window ended by a terminal, within one boot (latch path 3): a request passes `created_at + BAR_PERIOD` with no classification read and no acquisition, then its accepted terminal arrives, then entry: refused.

**S2 preservation cases (new, in `test_book_stale_admission_latch.py`; green on base and build).** Each is also shown red against a scratch over-latching mutant (latch carried into the next session, exits blocked, the fence set changed, or a latch on every terminal), not committed.
- P1. Next session: a request with no stale history is admitted, subject to every other gate.
- P2. After a STALE window in the session, exit, flat, cancel, a tightening amend and the scheduled flatten all proceed. No halt or incident is recorded, and authority stays NORMAL.
- P3. The fence set returned to other consumers is unchanged (a loosening amend refuses exactly as before).
- P4. Precision (§2.6): (a) within one boot, a request KNOWN_WORKING through its first bar and then filled, then add: admitted, subject to every other gate; its mutant latches every terminal past the first bar. (b) A restart after every entry/add of the session reached its accepted terminal with `as_of + MAX_FACT_AGE < created_at + BAR_PERIOD`, then entry: admitted; its mutant latches at boot regardless of terminal timing.

**Preservation (green before and after, unchanged):** `test_validate_c1_monitoring_acceptance.py`; every existing `test_c1_rail_arm.py` and `test_c1_rail_http_server.py` case except the §2.3 replacement; `test_book_account_owner.py`, `test_pr409_review4.py`, `test_book_feedback_journal.py`, `test_book_close_reconciliation.py`, `test_four_leg_runtime.py`, `test_feed_omission_session_end.py`.

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
- `ops/c1_signal_daemon/**` and the daemon image-manifest tests (R-A2 is its own Track B card).
- The umbrella, ADRs, specs, STATE and the ledger (coordinator-reserved); GLM; opening a PR, merging, or pushing to `main`.

## 6. Return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED, per slice. The coordinator's verdict is RESOLVED (every §4 item for the slice holds) or FALSIFIED (named items fail; returned to the executor). The return holds:
- branch, head SHA and base; `git diff --stat` and the name list;
- Phase-0 findings (a)–(f); for S2, the #628 and GC-5 merge SHAs contained in the base;
- per case, the fail-on-base and pass-on-build launcher record IDs;
- the preservation results and the planted-defect image-guard output;
- the two build-state listings, or the owed note;
- concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- Phase-0 findings (a)–(f): return them, then wait for the coordinator before code.
- A closure-member or pinned digest would change (finding (a)); a schema migration, new table or new row is needed (finding (b), D-7); a durable row the boot derivation reads is overwritten (finding (f)); no owned provenance parser exists (finding (c)).
- Any change outside §2.7, a host or network action, or a real artifact would be needed.
- S2 while #628 or the GC-5-DISPLACED build is unmerged, or from a head that has not merged an `origin/main` containing both (§9).
- No executor starts before the card is frozen (D-3 is RULED U, §11).
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, stop folding; the coordinator adjudicates a rewrite or a narrower scope.
- A second writer appears on the branch.

## 8. Out of scope and decision unlocked

**Out of scope:**
- The effective-activation protocol itself: the pending request, the restart, the boot-bound fresh no-activity attestation, and the durable acknowledgment producer (D-5).
- Later-session rearming (ADR `:109`).
- TB-D2's GO write and reseal proof; TB-D0's row; TB-V1's binding; TB-O1's procedure; the TB-I3 live packet.
- The D-MON-1 notifier (#628, `claude/book-incident-notifier`; sequenced before S2, §9).
- The T09 split design and ED-10-SPLIT. GC-5-DISPLACED is its own card, sequenced before S2 (§9).
- R-A2, the offline four-source slice (`book_sources.py`; the `book_evaluate_loop.py` source-health halt). It is a Track B owner item with its own card; putting it under this card needs a new ruling from Joshua. The #619 revision latch (Q1) goes with it; it is a source-state latch, not A12-STALE.

**Unlocked:** with S1 and S2 RESOLVED and the Codex relay clean, the interlock exists in source, so an image built from it refuses to arm or boot armed until TB-D2's GO, T13's monitoring acceptance and the activation slice exist. A12-STALE moves from "owed" to "implemented, synthetic" in its owner rows only once the D1 acceptance act has happened (A12-STALE is effective with D1); before that the coordinator records the implementation without changing the PROPOSED rows' status.

## 9. Sequencing on `book_account_owner.py` (coordinator (3) ruling)

No two live packets share a file (umbrella `:245`). Three packets edit `ops/c1_rail/book_account_owner.py`: #628 (D-MON-1 notifier core, open, head `60ba482`, adds `read_incidents`), the GC-5-DISPLACED build (its own card), and this card's S2. Fixed order: #628 merges first; then the GC-5-DISPLACED build, cut from `main` after #628 merges; then TB-I3 S2, from `main` after GC-5 merges. Each card carries a stop if its predecessor is unmerged (§7). S1 touches none of #628's or GC-5's files and may proceed earlier.

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
gh pr view 628 --json state -q .state                      # S2 gate: MERGED (and the GC-5 build PR: MERGED)
# Scope at return.
git diff --stat "$BASE"...HEAD; git diff --name-only "$BASE"...HEAD -- deploy | grep -v '^deploy/c1_rail/Dockerfile$' && echo "FAIL: deploy scope"
test -z "$(git diff --name-only "$BASE"...HEAD -- ops/c1_signal_daemon)" || echo "FAIL: daemon scope"
```

## 11. Decisions (open items for coordinator (3) at freeze; D-3 RULED by Joshua)

- **D-1 Dockerfile `COPY` and "no deploy" (coordinator scoping call). Recommended: in scope, limited to the §2.5 lines.**
  - "No deploy" is the operator act `rail.deploy` (`fly deploy`; `scripts/seat_authority.yml`). Editing a build recipe that only a later, separately authorized deploy would consume is source work. Nothing reaches a host, and merging stays the operator's.
  - The existing guards force it. Once the server and arm CLI import `deployment_go.py`, `test_listener_import_closure_is_covered_by_dockerfile_copy`, `test_packaged_files_are_allowed_in_build_context` and `test_ci_exact_inventory_includes_packaged_python_modules` fail without the `COPY`, the `.dockerignore` and the `LISTENER_FILES` lines. Omitting them reproduces the 2026-07-31 green-build/dead-container class.
  - ADR §2b/§2c (`:103`, `:118`) assigns the absence-tolerant `COPY` and the two-state build check to TB-I3. Absence is the fail-closed state, so an image built from this card refuses the arm by itself.
  - Bound: no `fly.toml`, no daemon image, no push. Local builds only (finding (d)). If the coordinator rules it out, S1 cannot import `deployment_go` into the boot path, and the boot gate (the core of the ruling) must wait too. Ruling it out therefore defers S1 rather than narrowing it.
- **D-3 Arm-time and boot-time gate scope. RULED U (universal) by Joshua, 2026-10-03, directly to coordinator (3): "I approve of the recommendations, let's make it happen."** He approved coordinator (3)'s recommendation of U and named no path that still needs an armed c1 rail. Both the arm-time (§2.2) and boot-time (§2.3) GO and book-route monitoring checks apply to every `--arm` and every `dry_run=false` boot, legacy single-leg included. The draft's question put these consequences to him: legacy single-leg arming ends until TB-D2's GO, T13's monitoring acceptance and the activation slice exist; `--acknowledge-m1-unresolved` still writes its record but can no longer yield an armed rail; and the `/data` boot-gate bypass AGENTS.md records closes for every route. It also named the tension with the TB-I4-M1 clause "The 2026-09-11 GO for the legacy implementation is unchanged" (sitting-2 recording plan §1.16). This ruling answers it; it is not re-asked. Option N is not taken.
- **D-4 The book-route monitoring artifact and the T10 reseal.** T13/D-MON (#606) owns the item list. Recommended: freeze the skeleton with an empty required list that refuses (fail-closed) until T13 supplies one, with the artifact path fixed now so the `COPY` line lands once. **Reseal constraint** (ADR T10 `:99`, §2b `:102-107`): the c1→c2 build-context diff must be exactly the GO path. So the monitoring artifact is committed **before B7**, inside EF1 (image v1, commit c1), and the GO has its own `COPY` line so its layer holds only the GO (§2.5). If T13 cannot land the artifact before B7, the conflict goes to the [book protection admission ADR](../../adr/2026-09-12-tradeify-book-protection-instance-admission.md)'s owner; this card does not resolve it.
- **D-5 Effective activation.** Recommended: a separate TB-I3 activation slice (request → restart disarmed → fresh boot-bound attestation → durable acknowledgment before risk-add, with the ADR `:105` traces: delayed restart, intervening activity, changed image or config, replayed attestation, missing acknowledgment, crash). This card ships only the refusing default and the injected-source seam.
- **D-6 FBR in provenance.** If finding (c) shows no owned parser, the owner is TB-I1 (`policy_fingerprint`) or TB-D0. Recommended: TB-I1 adds `provenance_fbr_digest()` under its own card, and S1's GO comparison waits behind it.
- **D-7 Latch trigger and storage. RULED by coordinator (3): option (ii)** (§2.6), **amended 2026-10-03 on the #633 review P2** (card `:137` and `:191` at `4dce572`). An exact durable latch from retained rows alone is not buildable: order evidence is per boot and never persisted (`book_account_owner.py:368-371`), and the evidence path "never writes durable state" (`:934`), so no evidence `as_of` survives a restart. The latch is in memory within one boot (observed STALE; STALE classified before an evidence overwrite or before an accepted terminal) plus a fail-closed derivation at boot over retained rows: X is latched by an entry/add that is non-terminal past `created_at + BAR_PERIOD`, or whose accepted terminal has `as_of + MAX_FACT_AGE >= created_at + BAR_PERIOD`. No new table or row, so finding (b)'s stop stands. The amendment withdraws the earlier accepted residual (STALE, then terminal, then restart reopened admission): it contradicted the operator's rest-of-session closure (incident ADR §A12.5 stale-evidence row), which a coordinator residual cannot waive (case 17). Accepted cost, widened: a restart closes admission for the session whenever an entry/add of the session was, or may have been, non-terminal past its first bar (case 16). A durable latch mark under `book_migration_schema` (the former option (i)) would narrow that cost to observed STALE; it needs its own ruling lifting finding (b) and is not required for the closure.
- **D-8 Executor.** Codex local (recommended, umbrella routing) or a Claude worker. GLM is excluded either way.
- **D-9 Freeze base and record prerequisite.** The c2 batch ledger PR must land the TB-I3-CARD, A12-STALE and TB-I4-M1 records at their owners (recording plan §1.5, §1.16 and the A12 rows) before freeze, so this card cites them on `main`. Recommended base: `main` after that merge. S2's base is fixed separately by §9.
- **D-11 File sequencing. RULED by coordinator (3):** #628, then the GC-5-DISPLACED build, then TB-I3 S2, each from `main` after its predecessor merges (§9). The earlier draft named the wrong file: #628 does not touch `c1_rail_http_server.py`; the shared file is `book_account_owner.py`.
- D-2 and D-10 were R-A2's and left with it.

## Pre-mortem (README rule)

- **Loop cost:** two Windows build loops with launcher records, plus two local image builds. No Linux run, no host.
- **Decisions the executor will hit:** D-1 and D-6, ruled in one batch at freeze (D-3 and D-7 are ruled).
- **What makes it moot:** an operator ruling that withdraws the TB-I3 synthetic authorization, a route change that removes the c1 listener host, or the attempt ending (R1a/R1b) before an image matters.
- **Measurements the return fills in:** Phase-0 findings (a)–(f), per-case records, the planted-defect guard output and the build-state listings.
