# Track A — Finish M1 / B7-REFIRE Stage 1: orchestration plan

**Date:** 2026-09-10
**Type:** orchestration plan (multi-session; not a single-session code plan)
**Owner:** Joshua (operator) · parent session: Claude Code (author of this plan; reviewer of every sub-track return)
**Spec being executed:** the operator's Track A packet (A1–A8, 2026-09-10) against
[M1 ADR §4 item 5](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md#4--falsifier-and-revert-trigger),
its [2026-08-24 addendum](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24),
the [GO ADR 2026-08-24 addendum](../../adr/2026-07-17-c1-rail-build-account-registration-go.md#addendum-2026-08-24--test-strategy-is-a-qualifying-strategy),
and the Stage 1 test contract that lands with PR #332 (`docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md`).
**Authority:** nothing in this plan arms the rail, places an order, or claims M1 `RESOLVED`. Every
sub-track returns to the parent session for a two-pass review before the next one dispatches.

**Goal:** M1 `RESOLVED` on a genuine, strategy-originated, expected-sizing (`qty_out=1`) dry-run
event from the ruled Python host through the deployed listener, with operator signoff, and the
`RESOLVED` artifact embedded in a redeployed listener image — rail still `dry_run=true`.

**Architecture:** four lanes with a dependency graph, not a linear list. The listener lane and the
recovery lane do not depend on the signal-source decision; the daemon lane does. The ceremony
lane needs all three. Each lane step is a separate session with its own handoff brief; the
parent reviews spec compliance, then quality, then (for multi-step returns) a consolidated read.

---

## 0. Verified premises and corrections to the Track A packet (handoff-verify, 2026-09-10)

Read directly this session from `origin/main @ 47972f6`, the two PR branches, and read-only Fly state.

| Packet claim | On-disk / host reality | Consequence |
|---|---|---|
| "PR #332 removed the Databento adapter" / "review the merged PR" | **PR #332 is OPEN** (head `811df7c`, branch `codex/m1-stage1-test`, merge-base `60ff835`, 5 commits behind main; checks green; every Codex finding answered in-thread). **PR #334 is OPEN** (head `3efdeb0`, mergeStateStatus CLEAN). Main never carried the adapter — it existed only in #332's earlier commits and was removed in `811df7c`. | **A0 precondition: merge #332 and #334 first** (operator, in progress). Every brief's Phase 0 checks for `ops/c1_rail/m1_stage1_contract.py` on `origin/main` and returns `NEEDS_CONTEXT` if absent. |
| "the new M1 infrastructure" | Exists only on the PR branch today. | Same as above. |
| A6 "Deploy the daemon" | `c1-signal-daemon` app **already exists**: release **v1 FAILED** (2026-08-08 04:50), yet machine `840759c2474928` is `started` with 1/1 checks passing on image `deployment-01KZFVAFXM3RTWJWVWND6W6TQ7` (the pre-#332 IdleBarSource build). Volume `c1_signal_daemon_data` attached. | A6 is a **redeploy over a running machine whose only release is marked failed**; A4 reads that machine's volume config and boot log before A6 plans anything. |
| A5 "Deploy the reviewed listener image" | `c1-rail` at release **v7** (2026-08-19 18:28), image `deployment-01M0DMFSFXVXEHZ27G8VYC0WQK`, machine `e820221a657d28`, 1/1 checks passing, built from `origin/main @ 31fd642`; `fixture_hashes` in the acceptance JSON are that build's in-container (CRLF-form) pins. | Rollback target for A5 is **that exact image**, not release v6 (v6 is the flat-layout build the 08-19 deploy retired). |
| A2 "Build … in Linux containers" | No `docker`/`podman` on this machine; WSL Ubuntu present but stopped; `fly` v0.4.85 authenticated; repo is public, so GitHub Actions minutes are free. Both Dockerfiles are `python:3.12-slim` stdlib-only; `.dockerignore` default-excludes everything but the traced COPY set (tests are **not** in the images). | A2 runs on **GitHub Actions ubuntu runners** (real Docker) as a standing path-filtered workflow — the gap PR #332 admits ("An actual Linux image build was not performed"). |
| A2 "Verify … atomic one-shot writes … on Linux" | `atomic_json` (daemon journal) and `atomic_write` (listener control) fsync the parent directory only when `os.name != "nt"` / via `os.O_DIRECTORY` — a branch **never executed** by the Windows suite that validated #332. Same for the `fcntl.flock` branches of `DaemonOwnership` / `CeremonyStore`. | A2 is load-bearing, not ceremony. |
| A1 "someone must make a new bounded decision" | #334 adds an addendum to the S2b build ADR: the Databento selection "is no longer authorized… No replacement provider… The existing live-feed requirement is not silently replaced with a local fixture or replay; that would need an explicit amendment identifying what the test certifies and leaving live-feed readiness separate." #332's contract: `prepare`/`enable` "refuse before writing state"; evidence projection is `offline_test_only=true`, `qualifying_live_source=false`, and never emits `dry_run_strategy_signal_event_id`. | A1 is an **ADR-class decision** (it amends the feed-lock owner) → a Claude session authors the packet; **the operator decides**. A1b (implementing the chosen input) is a separate frozen-spec build that cannot be specified until A1 is ratified. |
| A3 "private `armed_until` recovery procedure" | The crash-loop class is **mitigated in code** on main: `c1_rail_http_server.load_config` boots DISARMED (in-memory) on an expired/invalid `armed_until` instead of raising (its comment block cites the 2026-07-31 incident). The private RUNBOOK B7 arming log holds the entrypoint-override recovery; it lives in `first-passage-archive` (repo links pin `5d47b4dc…`). | A3 verifies the deployed `31fd642` build contains the implicit-disarm code **and** that the operator can open the private procedure; the public record states availability, not content. |
| A8 "validator lines 40–58" | Confirmed: `RESOLVED_REQUIRED` includes `dry_run_strategy_signal_event_id` and `operator_signoff`; `operator_signoff.operator` must be non-empty; `reconcile_verdict=CHAIN_OK` and `notification_acked=true` are already satisfied on main (`7f80b4be…`, `6ceffdec…`). | A8 edits exactly the owed fields; nothing else moves. |

Live posture confirmed from `CLAUDE.md` and the c1-rail skill (2026-08-02 grant): agents may run
`fly deploy` (six per-app pre-conditions), `--disarm` (after broker-verified flatness), and every
read-only command; `--arm` is operator-only and is **not in Track A at all**.

---

## 1. Standing invariants every sub-track restates (owners named; never re-derived)

1. `dry_run=true` throughout Track A. No sub-track sets `dry_run=false`, and none uses
   `--acknowledge-m1-unresolved`. Owner: M1 ADR Addendum 2026-07-31b; `ops/c1_rail/c1_rail_arm.py`.
2. Host state is established only by a host read (`fly ssh console -a <app> -C "python ops/c1_rail/c1_rail_arm.py --status"`), never by a local file. Owner: c1-rail skill §Verification.
3. Six deploy pre-conditions, per app, in order: (1) host `dry_run=true` read first; (2) deploy from `main`, repo root, documented command; (3) re-trace the import closure; (4) refresh `fixture_hashes` from **in-container** hashes in the same motion; (5) verify boot line + health by printed output; (6) know the crash-loop recovery path. Owner: c1-rail skill §Agent-session authority + `deploy/c1_rail/README.md`.
4. Disarm only after broker-verified flatness (disarm blocks exits). Owner: c1-rail skill invariant 2.
5. Two Fly apps, two volumes, never shared; single machine per app. Owner: S2b build ADR §2.
6. Item 5 qualifies only as: evaluate-hook strategy on the ruled host → ordinary daemon B1 POST → listener structured dry-run decision at `qty_out=1`; not canned, not `NullStrategy`, not a fabricated id, not a zero-qty floor, not live-armed. Owner: M1 ADR §4 item 5 + 2026-08-24 addendum; S2 ADR §2/§4.
7. `order_id` idempotency is DISPROVEN; every payload carries a fresh identity; a re-sent file is not a no-op. Owner: acceptance JSON notes (2026-07-27).
8. `fixture_hashes` for every pin the image carries are refreshed only from in-container bytes after a real deploy; a tree-bytes rewrite asserts a deploy that never happened. The one pin the image does not carry, `tests/ops/test_m1_acceptance_drills.py`, is re-verified from the deployed commit's tree, as the 2026-08-19 refresh recorded. Owner: acceptance JSON `fixture_hashes_note`.
9. No agent places a trade; the weekly account-preservation trade stays operator-placed. Owner: `CLAUDE.md` §Live-execution posture, `STATE.md` weekly trigger.
10. Private figures (Net Liq, account ids, tokens, raw bar values) never enter a public artifact; the acceptance validator's secret scanner is the mechanical check, and it does **not** detect account identifiers. `c1_rail_arm.py --status` prints `account=<id>` (its `_PRINTABLE` allow-list includes `account`), so every paste of that output into a readiness record, PR, or transcript replaces the token with `account=<redacted>`; the boot line in `fly logs` prints no account and may be pasted as is. Credential **key names** are public by design (READMEs, example configs, `load_config`); the thing that never appears anywhere is a credential **value**. Owner: `scripts/validate_c1_monitoring_acceptance.py` + `CLAUDE.md` §Live-execution posture.

---

## 2. Lanes and dependency graph

```
A0  merge #332 + #334  (operator)  ─────────────────────────────────────────────────┐
                                                                                      │
Lane R (recovery)   A3 recovery-path attestation ──────────────────────────┐         │
Lane L (listener)   A2-L image validation ──► A4-L readiness ──► A5 listener deploy (disarmed)
Lane D (daemon)     A1 source decision packet ──► operator ratifies ──► A1r records it on disk ──►
                    A1b build (PR) ──► A2-D image validation ──► A4-D readiness ──► A6 daemon deploy (inert)
Lane C (ceremony)   [A3 + A5 + A6 all DONE] ──► A7 attended Stage 1 dry-run (operator enables)
                    ──► A8 signoff + RESOLVED artifact + listener redeploy ──► STOP (no arm)
```

- A2 is one brief with two image targets; its listener half runs before A1b lands, and its
  daemon half is re-run on the final A1b image (the workflow is path-filtered, so re-runs are free).
- A4 is one brief; its listener half gates A5, its daemon half gates A6. A4 never deploys.
- A5 does **not** depend on A1: the listener image has no feed. Deploying it early closes the
  2026-08-21 tree skew and lands the `m1_stage1_test` identity at cap zero, `RETIRED`.
- A7 needs the approved input (A1b, deployed in A6), the migrated listener (A5), the attested
  recovery path (A3), and the operator at the console.

---

## 3. Division of labor

Routing test is [`2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md)
§2 (0: local-only deps; 1: doctrine/locked surface → Claude; 2: frozen spec → Cursor/Codex;
3: overhead threshold). Codex is the standing PR reviewer for every PR below regardless of author.

| Sub-track | Surface | Why (routing test) | Local-only deps | Return artifact | Parent review |
|---|---|---|---|---|---|
| A0 merge #332, #334 | Operator | Merge is operator-gated on rail surfaces (auto-merge ADR forbidden list). | — | merge SHAs | none |
| A1 signal-source decision packet | **Claude** | Authors an ADR addendum (test 1). Web research allowed; no signups, no spend. | archive reads only | PROPOSED addendum to the S2b build ADR with scored options; operator ratifies | spec + quality |
| A1r record the ratification | **Claude** (parent) | Docs-only edit of the A1 addendum status line plus the M1 ADR amendment when the option needs one (test 1); the operator's ruling becomes on-disk state that A6 checks. | none | PR replacing `PROPOSED` with the dated ruling | operator merge |
| A1b implement the ratified input | **Codex** (or Cursor) | Frozen spec from the merged A1r text; daemon-side code plus the validation-script expectations named in §3.1; Codex authored #332 and holds its design. Brief authored **after** A1r merges — not in this plan (must-cover list in §3.1). | none | PR on `codex/*` | fable-judge + Codex review |
| A2 Linux image validation | **Cursor** (or Codex) | Frozen spec; new workflow + script; no judgment calls. | none — GitHub Actions has Docker | PR adding `.github/workflows/c1-image-validation.yml` + `scripts/c1_image_validation.sh`; green run URL | spec + quality; parent re-runs the workflow |
| A3 recovery-path attestation | **Claude** + operator | Governed note; needs Fly read access and the private archive; operator attests access. | fly auth; archive clone | readiness record §A3 | spec + quality |
| A4 deployment-readiness review | **Claude** | Judgment-heavy review of live host state; governed note. | fly auth | readiness record §A4 with per-item GO/NO-GO | spec + quality |
| A5 listener deploy (disarmed) | **Claude** | Live-safety surface; the 2026-08-02 grant covers `fly deploy`; migration apply needs the operator's flat attestation. | fly auth | acceptance JSON `fixture_hashes` refresh + notes entry; readiness record §A5 | spec + quality + consolidated |
| A6 daemon deploy (inert) | **Claude** | Same class as A5. | fly auth | readiness record §A6 | spec + quality + consolidated |
| A7 attended Stage 1 dry-run | Operator + **Claude** (console) | Operator runs `enable`; agent runs read-only preflight, `prepare`, verification, `close`. | fly auth; operator present | evidence projection + genuine listener event UUID; readiness record §A7 | spec + quality + consolidated |
| A8 signoff + RESOLVED + redeploy | **Claude** | Edits the acceptance artifact (governed); redeploy under the grant. | fly auth | PR with `status=RESOLVED`; post-redeploy `--status` shows `m1_gate … result=PASS`; STOP | spec + quality + consolidated |

Handoff briefs (dispatch in this order; each is self-contained):

- [A1 — Claude: signal-source decision packet](../../briefs/handoffs/2026-09-10-track-a-a1-claude-signal-source-decision-packet.md)
- [A2 — Cursor: Linux image validation](../../briefs/handoffs/2026-09-10-track-a-a2-cursor-linux-image-validation.md)
- [A3 — Claude: recovery-path attestation](../../briefs/handoffs/2026-09-10-track-a-a3-claude-recovery-path-attestation.md)
- [A4 — Claude: deployment-readiness review](../../briefs/handoffs/2026-09-10-track-a-a4-claude-deployment-readiness-review.md)
- [A5 — Claude: listener deploy, disarmed](../../briefs/handoffs/2026-09-10-track-a-a5-claude-listener-deploy-disarmed.md)
- [A6 — Claude: daemon deploy, inert](../../briefs/handoffs/2026-09-10-track-a-a6-claude-daemon-deploy-inert.md)
- [A7 — Operator + Claude: attended Stage 1 dry-run](../../briefs/handoffs/2026-09-10-track-a-a7-claude-attended-stage1-dry-run.md)
- [A8 — Claude: signoff, RESOLVED artifact, redeploy](../../briefs/handoffs/2026-09-10-track-a-a8-claude-m1-resolution.md)

### 3.1 A1b frozen spec — must-cover list (authored after A1 ratification)

The implementer of the ratified input changes the daemon only. The spec the parent writes must pin:

- A `BarSource` implementation exposing `poll()`, `connected`, `activate(binding)`, `deactivate()`,
  `feed_mode`, and `binding`, matching what `EvaluateLoop` / `M1Coordinator` already call. `bar.ts`
  is the bar **open** time, tz-aware UTC, so the coordinator's acceptance window
  (`bar.ts == target` and `60 ≤ now − bar.ts ≤ 150` s) holds. Bar numerics finite and positive.
- The manifest `source` marker: `validate_manifest` currently requires equality with
  `OFFLINE_SOURCE`; the approved marker becomes a named constant in `ops/c1_rail/m1_stage1_contract.py`
  and the offline marker stays test-only. **The inputs of `contract_sha256()` (the frozen tuple,
  `entry_only`, `permanently_dry_run_only`) must not change**: A5's listener image keeps the pre-A1b
  copy of this module until A8, and A7 gates on both images' `contract_sha256()` being equal. If the
  tuple ever has to change, an A5-class listener redeploy precedes A7. The file's bytes will still
  differ between the A5 and A8 listener images (the added marker), which is why A8 compares pins per
  file against explaining commits rather than requiring "unchanged".
- The standing Linux validation (A2) expectations that the source changes — D2's declared-dependency
  set and D6's `prepare`/`enable` refusal wording — are updated in the A1b PR itself
  (`scripts/c1_image_validation.sh`, `tests/fixtures/c1_image_validation/`), never left red; the
  Databento-absence check stays as is. A `deploy/c1_signal_daemon/requirements.txt` is permitted
  when the ratified source needs a client package, and it must be a fully resolved, hash-pinned
  lock naming every transitive distribution (`pip-compile --generate-hashes`, installed with
  `--require-hashes`, as `requirements-ops.lock` is) so A2's D2 can compare the installed closure
  exactly; the listener image stays stdlib-only.
- Volume configuration for the ratified source (endpoint, credential key names) is documented in
  the A1b PR's README section, because A4-D reviews it as a **pending write** and A6 stages it
  (operator-performed `fly ssh sftp` put of a locally prepared config, never through an agent
  transcript) before deploying — no earlier sub-track writes the daemon volume.
- `daemon.build_loop` constructs the approved source **disconnected** plus the coordinator;
  `prepare`/`enable` stop returning the hard `2` but keep every boot/generation/manifest check.
- Credentials (if any) live only in the daemon volume config; `load_config` validates the new keys;
  health and `status` never print them. Listener volume untouched.
- `project_evidence` sets `qualifying_live_source` and emits the acceptance-event field exactly
  as the ratified amendment says — and the acceptance JSON edit remains A8's manual, operator-signed step.
- Dockerfile / `.dockerignore` additions; both image-manifest tests extended; A2 workflow re-run green.
- S2b §2 locks preserved: fail-closed on unhealthy feed (no signal of any type), staleness
  `2 × bar_period + 30 s`, second app, no listener B1 contract change.
- Tests: unit + the real-HTTP-handler integration path; the source-retirement test updated to the
  new disposition rather than deleted.

---

## 4. Task list (checkbox = parent-session acceptance after the two-pass review)

- [ ] **A0** — #332 and #334 merged; `origin/main` carries `ops/c1_rail/m1_stage1_contract.py` and the S2b build ADR's 2026-09-10 addendum. Then a one-line edit: `STATE.md` queue row 1 gains a pointer to this plan (Claude, docs-only PR).
- [ ] **A1** — decision packet returned; operator ratifies exactly one option (or NO-GO for all, which parks Track A after A5).
- [ ] **A1r** — the ratification is on disk: a docs-only PR (parent session) replaces the addendum's `PROPOSED` status line with `RATIFIED <date> — option <X>`, adds the change-history row, and applies the amendment text to the M1 ADR when the option needs one; operator merges. A6's Phase 0 hard-checks this edit; an oral or PR-comment ruling alone does not unblock the daemon lane. Parent then authors the A1b brief from the merged text.
- [ ] **A2 (listener half)** — workflow green on `main`; listener entrypoint boots disarmed under `--network none`; test identity rejected at `dry_run=false` in-container; focused suites pass on Linux.
- [ ] **A3** — readiness record §A3 written: procedure available (path @ SHA, no content), operator access confirmed (date), current + rollback images named for both apps, recovery cannot restore obsolete allocations or `dry_run=false`.
- [ ] **A4 (listener half)** — readiness record §A4-L: every checklist item GO, or the NO-GO named with its owner.
- [ ] **A5** — listener at the new release; `dry_run=True armed_until=-` by host read; `m1_stage1_test` row present at `cap_alloc=0` / lifecycle `RETIRED`; `fixture_hashes` refreshed in-container; `--status` prints `m1_gate: status='CODE_LANDED' result=FAIL` (expected while unresolved). No arm, no signal.
- [ ] **A1b** — ratified input implemented, reviewed by Codex, adjudicated by fable-judge, merged.
- [ ] **A2 (daemon half)** — re-run on the A1b image: boots inert, no outbound connection at boot (`--network none`), `prepare`/`enable` still refuse without a valid ceremony, lock/restart/timeout checks pass on Linux.
- [ ] **A4 (daemon half)** — second dispatch of the A4 brief (Step 2.3b/2.4b): readiness record §A4-D with every row GO; the v1-failed-release anomaly explained from evidence; approved-source keys present but disabled; journal state clean; daemon import closure re-traced on the A1b merge SHA; A6 command sequence frozen.
- [ ] **A6** — daemon at the new release; `GET /` shows `emit_enabled=false`, `effective_emit=false`, `strategy=NullStrategy`, source disconnected; no signal on boot (listener ledger last `seq` unchanged); ceremony state file valid; `status` CLI healthy. STOP before any ceremony.
- [ ] **A7** — one ceremony: preflight `expected_qty=1`; operator `enable`; one B1 POST; listener triad `request_received → decision(qty_out=1, dry_run=true, test_only=true, sender_invoked=false) → transport_result(not_attempted)`; evidence projection joins uniquely; `close`; listener disarm + daemon `effective_emit=false` reconfirmed; genuine listener event UUID recorded.
- [ ] **A8** — acceptance JSON: `dry_run_strategy_signal_event_id`, `operator_signoff`, `status=RESOLVED`, in-container `fixture_hashes` (deployed pins in-container, the test pin from the tree); validator plain + `--require-resolved` exit 0; PR merged; listener redeployed with the `RESOLVED` artifact; `--status` → `result=PASS`; if any pin moved at that deploy, PR 2's refreshed record is re-baked by one docs-only redeploy (ops bytes unchanged, hashes identical before and after) so the running image's embedded record describes its own bytes. **STOP. No arm.** STATE row 1 leaves the queue with its record.

---

## 5. Operator-only actions (no agent performs these)

1. Merge #332, #334, and every Track A PR (rail surfaces are on the auto-merge-forbidden list).
2. Ratify the A1 decision (one option, dated) — or NO-GO.
3. Attest broker-verified flatness before A5's migration apply and before A7 (Tradovate "No open positions").
4. Confirm access to the private recovery procedure (A3) — by opening it, not by recalling it.
5. Run `enable` for the single A7 ceremony; run `close` if the agent cannot.
6. Provide `operator_signoff` (name, date, statement) for A8.
7. Keep placing the weekly account-preservation trade; Track A does not change that obligation.
8. `--arm` is not in Track A. If anyone proposes it, the answer is the M1 ADR: `RESOLVED` **plus** a separate GO, in a later track.

---

## 6. Track-level stop rules

- **Armed-host discovery (any sub-track, any read):** if `--status` shows `dry_run=False` or a non-null `armed_until`, the sub-track stops and nothing else in it runs. `--status` reads the volume file; read the boot line in `fly logs` as well, because the running process holds its boot-time config and may differ. Then: (1) the operator attests flatness from Tradovate; **without the operator present do not disarm** (disarm blocks exits and would orphan an open position) — alert the operator and return `BLOCKED — plan-itself-wrong` naming the state; (2) with flatness attested, run `python ops/c1_rail/c1_rail_arm.py --disarm`, then `fly machine restart <listener machine id> -a c1-rail` (the disarm takes effect only on restart), then verify the boot line reads `dry_run=True armed_until=-` and `--status` agrees; (3) record the finding and every command in the readiness record; (4) return `BLOCKED — plan-itself-wrong`. Discovering the hazard and leaving it in place is not an option.
- Any unresolved ceremony checkpoint (`EVALUATED` / `SEND_RESERVED` / `EMITTED` / `TRANSPORT_UNKNOWN`) in the daemon journal: no new ceremony; preserve state; return for a separately reviewed reconciliation. No reset bypass exists and none is to be built.
- A green Linux build with a dead CMD (`ModuleNotFoundError` at boot) is a FAIL of A2, never "fix the COPY line and redeploy" inside A5/A6.
- A `qty_out` of anything other than exactly 1 at A7 preflight or decision: the ceremony does not proceed; the identity's frozen tuple is the contract's, and the discrepancy is a finding, not a parameter to tune.
- Two failed attempts at the same sub-track: stop, summarize, re-author the brief (CLAUDE.md §Continuous improvement).

---

## 7. Audit hooks (runnable)

```bash
# A0 landed?
git fetch origin main -q && git ls-tree --name-only origin/main ops/c1_rail/ | grep -c m1_stage1_   # expect 2
git show origin/main:docs/adr/2026-08-08-s2b-signal-daemon-build.md | grep -n "Addendum 2026-09-10"

# Host posture (read-only; judge by printed output — Windows fly ssh may exit 1 after correct output)
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
fly releases -a c1-rail | head -3
fly releases -a c1-signal-daemon | head -3

# Acceptance artifact state
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --require-resolved   # exit 1 until A8

# Briefs well-formed (skill-side is authoritative for cc_handoff)
for f in docs/briefs/handoffs/2026-09-10-track-a-a*.md; do python ~/.claude/skills/brief-authoring/scripts/check_brief.py "$f" --type cc_handoff | tail -1; done
```
