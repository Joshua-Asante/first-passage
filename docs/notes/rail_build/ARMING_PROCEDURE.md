# c1 rail — arming and session operating procedure (public, redacted)

**Type:** operating procedure · **Packet:** Track B TB-O1 ([umbrella](../../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) claim manifest row TB-O1)
**Date:** 2026-09-12 · **Author:** Claude Code (recorder) · **Authority:** Joshua (operator)
**Status:** **PREPARATION COMPLETE — NOT AUTHORIZED TO EXECUTE.** This file authorizes nothing. It
describes how an attended c1 session is armed, monitored, disarmed and recovered, with every step
anchored to source. The gates that must be open before any step here runs are listed in §1 and
most of them are still owed. No agent arms, emits, trades, or edits host state under this file.

**Book this file serves:** the Tradeify portfolio — the operator-accepted Aegis 6J · Vanguard MGC ·
Striker MYM · ORB MNQ configuration with its protection/capacity rules
([acceptance record](../2026-09-10-tradeify-protection-selection.md)). The generic c1 session
procedure (§4–§9) applies to any deployed strategy on the rail; the portfolio prerequisites (§1, §3)
are Track B's.

**Redaction rule applied:** campaign-state §33a — the redaction class is *any dollar figure, or
derivative that inverts to one, describing live-account activity* (balances, thresholds, P&L over
any window, per-fill results, token-trade outcomes)
([owner](../../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md), §33a). This
file carries no account identifier, no account dollar figure or history, no credential, and no
private operational output. A tool's "secret-free" output is not automatically public-safe:
`c1_rail_arm.py --status` prints `account=<id>`; every paste of it replaces the token with
`account=<redacted>` (Track A plan §1 invariant 10).

**Private runbook:** the historical operator runbook (`docs/notes/rail_build/RUNBOOK.md`, B3→B7
build record, B7 arming log, relink procedure, post-disarm export) is **not on the public tree** by
the [public-visibility ADR](../../adr/2026-08-14-repo-public-visibility-transition.md)'s exclusion
rule. §2 gives the retrieval convention. This file is the public successor for the *procedure*; the
private runbook remains the owner of the *history* and of the crash-loop recovery procedure, which
this packet did not change.

---

## §1 — Readiness ledger: what is prepared vs. what is authorized

Read this table before anything else. "Prepared" means the artifact exists and was reviewed.
"Open" means the gate is owed to its named owner. An A7 pass (Track A's attended Stage 1 dry-run,
scheduled Sunday 2026-09-13) discharges M1 item 5 **only**; it is not portfolio deployment
authority, and M1 `RESOLVED` (A8) is not a GO.

| Gate | State 2026-09-12 | Owner / evidence |
|---|---|---|
| M1 acceptance `RESOLVED` **in the deployed listener image** | **OPEN** — `status: CODE_LANDED`; item 5 and `operator_signoff` owed (A7 → A8, then a listener redeploy, because the interlock reads the artifact baked into the image) | [M1 ADR](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) §4 · [acceptance JSON](M1_MONITORING_ACCEPTANCE.json) · [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §4 A7/A8 · [readiness record](M1_STAGE1_DEPLOYMENT_READINESS.md) §A7-P |
| Session-specific operator GO | **OPEN by construction** — every armed session needs its own GO; none is recorded | [GO ADR](../../adr/2026-07-17-c1-rail-build-account-registration-go.md) (arm gate) · `CLAUDE.md` §Live-execution posture |
| TB-O1 (this procedure) merged before TB-B7 / TB-B10 | **PREPARED** — this PR | umbrella claim manifest |
| Approved production feed and source equivalence (O-4 → TB-I5) | **OPEN** — no provider selected, funded or connected (operator deferral 2026-09-11); TB-I5 spec not authored; option D covers the M1 ceremony only | umbrella §0.8 O-4 · [S2b build ADR Addendum 2026-09-11](../../adr/2026-08-08-s2b-signal-daemon-build.md) |
| Runtime binding / symbol verification (TB-V1, TB-S3 (B)) | **OPEN** — `LEG_MAP` carries `dj30_mym`, `nas100_mnq`, `m1_stage1_test` at `cap_alloc` 0 and no portfolio leg; `INSTRUMENT_SYMBOLS` has no 6J/MGC entry; no per-symbol CrossTrade ticket verification | `ops/c1_rail/c1_sizing_host_reference.py` `LEG_MAP` @ `509b524` · `ops/c1_rail/c1_rail_listener.py` `INSTRUMENT_SYMBOLS` @ `509b524` · umbrella TB-V1 stub |
| Protection policy admitted for the book (TB-D0) | **OPEN** — `core/dd_geometry.POLICY_REGISTRY` is empty; the live sizing path applies the frozen `dd_protection` rule, not the accepted 1%/40% instance | `core/dd_geometry.py` @ `4929c44` · `ops/c1_rail/c1_sizing_host_reference.py` `_read_dd_scale` @ `509b524` · D-B11 |
| Multi-leg daemon and rail extension (TB-S3 → TB-I3) | **OPEN** — TB-S3 not authored (branch exists, no commits); the deployed daemon refuses `emit_enabled=true` for anything but the M1 test identity | `ops/c1_signal_daemon/daemon.py` `load_config` @ `36b3996` · umbrella TB-S3 packet |
| Dedupe implementation (TB-I4) | **OPEN** — gated on M1 `RESOLVED` + D-B13 GO (granted 2026-09-11, effective at `RESOLVED`) | [pre-registration](../../spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md) |
| Live test on the sealed image (TB-I3 live part) | **OPEN** | umbrella TB-I3 / D-B15 |
| Sealed snapshot + execution/replay fingerprint equality (TB-T1 → TB-B7) | **OPEN** — TB-T1 packet READY on PR #358 (not merged, not built); no seal exists | umbrella TB-B7 stub · PR #358 (`docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md` once merged) |
| Sole n3 adjudication (TB-E2) | **OPEN** | umbrella TB-E2 stub |
| Deployment GO (TB-D2 → operator) | **OPEN** — separate from acceptance, M1, admission and publication | umbrella TB-D2 stub |
| Arm (TB-B10) | **NOT REACHABLE** until every row above closes | this file §4 |

---

## §2 — Private runbook retrieval (convention; content never enters the public tree)

| Item | Value |
|---|---|
| Archive repository | `Joshua-Asante/first-passage-archive` (private, archived/read-only) |
| Archive pin used by every link on this tree | `5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2` — [RUNBOOK.md at the pin](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/notes/rail_build/RUNBOOK.md) (blob `0b90318f7695…`, the revision Track A §A3 verified) |
| Revision this packet retrieved (umbrella TB-O1 manifest) | `pre-prune-2026-08-08:docs/notes/rail_build/RUNBOOK.md` → blob `d523ee0d1e9d6054fdd75813a9bc25221102e635` · SHA-256 `d672c331bc9bd7ddabc44da6bae737cd4f6032b1bb5cd897b395c743d965cf5a` |
| Private root (primary checkout, ignored) | `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/rail_build/RUNBOOK.md` — the Track B private root named by the umbrella (§10 D-B3 hook, TB-R1 2.4); ignored by that study's `.gitignore` (`local_artifacts/`) |
| Integrity check (read-only, prints no content) | `git hash-object <private root>/RUNBOOK.md` → must print `d523ee0d…`; a differing digest means the copy was edited and is no longer the archive blob |

**Convention.** The `pre-prune-2026-08-08` tag is **not** on public clones
([ltm README](../../ltm/README.md)); `git show pre-prune-2026-08-08:<path>` works only on a clone
that carries the private lineage, or against the archive. The archive pin `5d47b4dc` is a **later**
revision of the same file (same heading structure, additional body text); the umbrella manifest
names the pre-prune tag, Track A's readiness record cites the pin. Both are recorded here so a reader can tell which revision they hold; the
choice of which revision the private root should carry going forward is the umbrella owner's
(flagged in the TB-O1 PR). Never copy either revision into the public tree, a PR, a log, or a
tracked patch; never print its body. The retrieved copy is **read-only history** — new session
entries go to a separate private file in the same root, never into `RUNBOOK.md`, so its digest
keeps matching the archive blob.

Other private `docs/notes/rail_build/` artifacts referenced by public documents (desk cards,
`b4_dry_fire_payloads/`, compliance notes) follow the same convention: archive URL at the pin, or
the private root.

---

## §3 — Source anchors (Rule 0; read before stating any behaviour below)

| Source | Anchor | What it pins for this procedure |
|---|---|---|
| `ops/c1_rail/c1_rail_arm.py` | `027a729` 2026-08-14 | `DEFAULT_CONFIG_PATH = /data/c1_rail_config.json`; `plan_arm` (M1 interlock via the validator with `require_resolved=True`; `--acknowledge-m1-unresolved` path; `armed_until = now_utc + hours`, second-truncated; self-check with `arming_expiry_reason`); `plan_disarm` (`dry_run=True`, `armed_until=None`); `describe_m1_gate` (`--status` line `m1_gate: status=… result=PASS|FAIL`); `_LONG_WINDOW_HOURS = 8.0` (warn, not refuse); `_write` keeps a one-deep `.prev` backup; `main` prints **NOT YET IN EFFECT … Restart to apply** — the tool edits the volume file and does not restart the host |
| `ops/c1_rail/c1_rail_http_server.py` | `027a729` | `load_config`: `dry_run` defaults True when absent; `dry_run=false` without `events_log_path` raises; expired/absent/malformed `armed_until` at boot → **IMPLICIT DISARM in memory** (log line), disk unchanged; `startup_log_line` prints `dry_run=… armed_until=…`; `ratchet_peak_equity` persists `max(peak, current)`; equity/peak read failure → HTTP 503 and no decision for entry/add, best-effort relay for exit/flat; `serve` loads `ExecutionStateStore` into `open_leg_state` at startup and each request; unhealthy ledger at startup blocks risk-add |
| `ops/c1_rail/c1_rail_listener.py` | `509b524` 2026-09-10 | `arming_expiry_reason` (absolute ISO-8601 deadline with offset; absent/naive/unparseable/past → expired; **risk-add only** — exit/flat keep relaying past expiry); `handle_signal` (risk-add blocked by ledger, by expiry; `dry_run` returns before the sender for **every** signal type, exits included; `transport_unknown` blocks further risk-add and never auto-retries); `INSTRUMENT_SYMBOLS` (three entries) |
| `ops/c1_rail/c1_sizing_host_reference.py` | `509b524` | `LEG_MAP` (three legs, `cap_alloc` 0); `_read_lifecycle_multiplier` halts on a missing leg key (never defaults a tier); `_read_dd_scale` ratchets peak and calls `dd_protection.calculate_protection` (frozen constants); constants/lifecycle/DD state are re-read per request (no restart needed for state-file changes) |
| `ops/c1_rail/c1_rail_telemetry.py` | `027a729` | `EventLedger` (append-only JSONL, fsync, startup validation, `risk_add_blocked`); `ExecutionStateStore` (`set_confirmed_base`, `load_into`); `FileAckNotifier` (alert file + operator ack dir); `iter_arming_deviations`; CLI `--deviations` (read-only list) |
| `scripts/validate_c1_monitoring_acceptance.py` | `027a729` | `RESOLVED_REQUIRED`; `--require-resolved`; `--check-tree-skew` / `--require-tree-current` ("pre-deploy / pre-arm use only"); `fixture_hashes` describe the **deployed** bytes |
| `ops/c1_signal_daemon/daemon.py` | `36b3996` 2026-09-11 | `load_config`: `emit_enabled=true` or `m1_test.enabled=true` is accepted only with `strategy == m1_stage1_test`, `bar_period_s == 60` and both flags equal; the daemon boots `emit_enabled=false` |
| `ops/c1_rail/write_volume_config.py` · `ops/c1_rail/export_session_evidence.py` | `027a729` | non-secret key merge (refuses unless `dry_run` is true, `--force-armed` is operator-GO only); evidence export (default dry-run plan, `--apply` copies; never edits `/data` config) |
| `core/dd_protection.py` · `core/dd_geometry.py` · `core/lifecycle.py` | `94041d9` · `4929c44` · `027a729` | `DD_TRIGGER`/`DD_SCALE` frozen and import-guarded; `POLICY_REGISTRY` empty; lifecycle multipliers in `[0, 1]` (down-only) |
| `deploy/c1_rail/Dockerfile` · `deploy/c1_rail/README.md` | `509b524` · `811df7c` | the acceptance JSON and the validator are COPYed into the listener image (the interlock reads the deployed artifact); six deploy pre-conditions owned by the c1-rail skill |
| `tests/ops/test_c1_rail_arm.py` · `tests/ops/test_c1_rail_http_server.py` · `tests/ops/test_m1_acceptance_drills.py` | `027a729` · `027a729` · `25711e2` | refusal on unresolved/forged/missing artifact, acknowledgement writes a deviation record or refuses the arm; implicit-disarm boot cases; `restart_confirmed_base` and the other five M1 drills |
| [M1 ADR](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) | `0059ca7` 2026-09-11 | gate object = the **arm** (Addendum 2026-07-31b); §4 RESOLVED list; §5 forbidden moves; falsifier: a third armed session while unresolved escalates to structural enforcement |
| [GO ADR](../../adr/2026-07-17-c1-rail-build-account-registration-go.md) | `770413b` 2026-09-06 | attended-only posture; spend ceiling; per-session arm GO; Option C own-flatten stack (operator 15:55 ET flat-check on every session that carried open risk); flat deadline 16:45 ET regular / 12:59 ET early close (Addendum 2026-07-22) |
| [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) · [readiness record](M1_STAGE1_DEPLOYMENT_READINESS.md) | `01519fc` · `2a849b9` 2026-09-12 | §1 standing invariants; §6 armed-host stop rule (flatness attested → `--disarm` → restart → verify); §A3 recovery-path record; §A7-P teardown table and the allowlisted ledger projection |
| [Track B umbrella](../../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) | `8f99b41` 2026-09-11 (revised on PR #358) | gate order (dependency graph, wave-3 gates), TB-B7 / TB-E2 / TB-D2 / TB-B10 stubs, §0.8 O-3, D-B12, D-B13, D-B15 |
| [Q-M1WIRE-1](../../briefs/Q-M1WIRE-1-arming-interlock-coverage.md) | `770413b` | CLOSED — FALSIFIED: `require_resolved=True` does not certify every capability the acceptance package describes (confirmed-base production write path; alert reachability; skew cadence) |

**Distinguish three things throughout:** repository code (anchored above), historical evidence
(acceptance JSON notes, readiness record, private runbook), and **actual host state** — which only
a host read establishes (§5 step 1). This packet verified none of the host.

---

## §4 — Entry checklist (gate order is the umbrella's; each row names actor, prerequisite, evidence, failure disposition)

Nothing in §5 starts until every row reads PASS in the session record. A row that cannot be
evidenced is a **stop**, returned to its owner; it is never waived, and a future gate is never
recorded as satisfied because its implementation is "expected".

| # | Gate | Actor | Prerequisite / how it is checked | Evidence recorded | If it fails |
|---|---|---|---|---|---|
| E1 | M1 `RESOLVED` in the **deployed** image | Operator (reads), agent may draft | In-container: `python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --require-resolved` → exit 0; `python ops/c1_rail/c1_rail_arm.py --status` → `m1_gate: status='RESOLVED' result=PASS`. A tree-side pass is not the gate; the image is. | the two printed lines (account token redacted) | stop; Track A (A8 + redeploy) owns it |
| E2 | Deployed build is the reviewed build | Operator | `--require-tree-current` in-container against the deployed artifact (pre-arm use); release/image identity matches the readiness record's last deploy | printed skew line; release + image tag | stop; a redeploy is a deploy (six pre-conditions) |
| E3 | Session-specific operator GO | Operator | dated statement naming the session window and this procedure's revision; recorded before any host write | verbatim in the private session record; date + digest in the public record | no GO → nothing arms |
| E4 | TB-O1 merged (this file) | Orchestrator | `git log --oneline origin/main -- docs/notes/rail_build/ARMING_PROCEDURE.md` non-empty | merge SHA | stop |
| E5 | Approved feed + source equivalence PASS | Operator (feed ruling) → Track A (delivery) → TB-I5 | O-4 ruled; TB-I5 frozen before comparison, applied to the delivered source, PASS recorded with the source identity/config digest | TB-I5 RESULTS digests | FAIL blocks the live test; the source, not the adapters, is the defect |
| E6 | Runtime binding and symbols | TB-V1 (operator-ratified) | four venue-edition rows; `LEG_MAP` `cap_alloc` for all four legs; active-leg digest sealed; per-symbol CrossTrade ticket-format confirmation for every fixed-book symbol (6J and MGC are provisional strings today) | TB-V1 PR + digests | a leg without verification stays at `cap_alloc` 0; no arm |
| E7 | Dedupe implemented and tested | TB-I4 | PREREG-C1-DEDUPE-1 plan executed verbatim (R1–R6, planted-defect tests) on a disarmed rail, host read `dry_run=True` first | PR + test output | stop; no live test without it |
| E8 | Live test passed on the sealed image | TB-I3 (D-B15 window) | listener verified `dry_run=true` by host reads before and after; `armed_until` unset; emit GO revoked at window end | readiness-style record | stop |
| E9 | Sealed snapshot + fingerprint equality | Operator (TB-T1 sealer) + orchestrator (TB-B7) | account flat with no pending orders; TB-T1 seals with all three evidence files and the kernel breach check; execution fingerprint sealed with written proof that every shared component equals the TB-F1 replay fingerprint | seal digest + timestamp; fingerprint record | stop; a failed relational check or breach check refuses the seal |
| E10 | Sole n3 adjudicated | TB-E2 → orchestrator (`fable-judge`) | one run, four conditions, fixed-book replay fingerprint unchanged since TB-E1 | verdict label + digests (figures private, D-B12) | FALSIFIED closes the attempt; no runner-up |
| E11 | Deployment GO recorded | Operator, after TB-D2 | separate from acceptance, `RESOLVED`, admission and publication; recheck snapshot identity and both fingerprints (no executable change since B7) | dated GO | withheld GO = `BLOCKED`, not negative evidence |
| E12 | No executable change after the B7 seal | Orchestrator | `git diff` of the sealed commit vs the image's build commit is empty for every shared component; otherwise reseal and re-run the live test before B10 | diff output | stop; reseal/retest |

**Sole n3 adjudication and the stop rule after it:** TB-E2's result is adjudicated once by the
orchestrator; any change after n3 stops for the operator (governing plan S2; umbrella wave-3 gate).
This procedure never reopens n3.

---

## §5 — Session start (generic c1; runs only after §4 is all PASS)

Every host command is **operator-run** in the operator's own console unless marked *agent*. The
agent may draft commands, run read-only reads it is permitted to run, and read printed output. No
command below is a validation step that silently arms, emits, trades or changes host state; the two
writes (arm, restart) are labelled and are the operator's.

| Step | Actor | Command / source | Expected observation | Refusal / stop |
|---|---|---|---|---|
| 5.1 Host read — on-disk config | Operator (agent may) | PowerShell: `& fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"` · Git Bash: prefix `MSYS_NO_PATHCONV=1`. Judge by the printed text, not the exit code (Windows `fly ssh console -C` may exit 1 after correct output). | `current: dry_run=True armed_until=None …` and `m1_gate: status='RESOLVED' result=PASS` | `dry_run=False` or a non-null `armed_until` → **armed-host stop rule** (Track A plan §6): nothing else runs; with flatness attested, `--disarm` → restart → verify; without the operator present do **not** disarm (it blocks exits) |
| 5.2 Host read — running process | Operator (agent may) | `fly logs -a c1-rail --no-tail` filtered to `dry_run=`, `armed_until=`, `IMPLICIT DISARM` | boot line `dry_run=True armed_until=-`; no `IMPLICIT DISARM` line | boot line disagrees with `--status` → the process holds boot-time config that differs from disk; stop, reconcile, never assume |
| 5.3 Health | Agent | `curl -sS https://<listener-app>.fly.dev/` and the daemon health `GET /` | listener `{"ok":true,…}`; daemon `effective_emit false`, `ceremony_state DISABLED`, `connected` per the approved feed's contract | unhealthy → stop |
| 5.4 Ledger and state health | Operator | `--status` already reads the volume config; ledger health is reported at boot (`events ledger unhealthy/blocked at startup`) and the reconciler lists deviations: `python ops/c1_rail/c1_rail_telemetry.py --events /data/c1_rail_events.jsonl --deviations` (read-only) | no unhealthy/blocked line; `arming_deviations: 0` or every listed record already explained in the private record | an unexplained deviation, a blocked ledger, or a truncated tail → stop (M1 §2.8: armed risk-add stays blocked until operator repair) |
| 5.5 State files present and seeded | Operator | existence and **shape** of `/data/lifecycle_state.json` (a key per active leg), `/data/c1_dd_state.json` (`peak_equity` per §8), `/data/c1_sizing_constants.json` (regenerated from production, never hand-typed), `/data/c1_execution_state.json`; the sizing host halts per request on any unreadable or unlisted input, so a missing key is a halt, not a default | keys only; **no values pasted** | a missing leg key or malformed file → stop; fix only through the documented writers / TB-V1 migration, never by hand-editing volume JSON |
| 5.6 Broker flatness and working orders | Operator | Tradovate: "No open positions" and no working orders; CrossTrade Alert History clear for the window | attestation sentence with time (UTC and ET) | any position or working order → resolve first; never arm over an open position |
| 5.7 Window and deadline fixed | Operator | write the intended **absolute end of session** in ET and UTC (§6); choose `<H>` so that `now_utc + <H>h` is at or before it and before the venue flat deadline; name the person who will disarm | the deadline and the name in the session record | no absolute deadline → no arm |
| 5.8 **ARM** (write 1 of 2) | **Operator only** | in-container: `python ops/c1_rail/c1_rail_arm.py --arm --hours <H>` | prints `before : dry_run=True …`, `after  : dry_run=False armed_until='<UTC deadline>' window=open`, `backup : /data/c1_rail_config.json.prev`, then `*** NOT YET IN EFFECT — the running process still holds its old config. Restart to apply`; a `WARNING: <H>h window is long` appears above 8 h | `ERROR: refusing to arm: …` → stop; read the reason; do **not** pass `--acknowledge-m1-unresolved` (§5.10); do **not** hand-edit the file |
| 5.9 **APPLY** (write 2 of 2) and verify | **Operator only** | `fly machine restart <listener-machine-id> -a c1-rail` (id from `fly machine list -a c1-rail`; the tool's own print names `fly apps restart c1-rail`) · then `fly logs -a c1-rail --no-tail` and `--status` | boot line `dry_run=False armed_until=<deadline>` and `--status` `window=open`; health green; **no** `IMPLICIT DISARM` line | an `IMPLICIT DISARM` line means the deadline was already past or malformed at boot: the process is disarmed, the disk says armed — run `--disarm`, restart, and start over; a restart that does not come back → recovery (§9) |
| 5.10 M1 interlock precision | — | `plan_arm` refuses when `m1_acceptance_reason` is non-null. The code carries an explicit acknowledgement path for a **structurally valid but unresolved** artifact (`--acknowledge-m1-unresolved '<reason>'` writes an `arming_deviation` ledger record **before** the config edit and refuses the arm if the record cannot be written); a forged or status-only `RESOLVED` is refused on both paths. | — | **This procedure and this handoff authorize no such deviation.** Code capability is not operator authority. The M1 ADR's falsifier names a third armed session while unresolved as the trigger for structural escalation; the acknowledgement path is never the readiness solution. A hand edit of `/data/c1_rail_config.json` is the same act with the audit trail removed and is barred. |
| 5.11 Signal source enable | Operator, per TB-S3 | the multi-leg daemon's emit-enable step is specified by TB-S3 (F)/(K) and implemented by TB-I3 — **pending**. Today the deployed daemon accepts `emit_enabled=true` only for the M1 test identity (`load_config`), so no portfolio strategy can emit. | per TB-S3 | absent spec → no session |

**On-disk vs running-process state.** The arm helper validates and atomically writes
`/data/c1_rail_config.json`; the listener reads its config once at boot into a closure. A written
but un-restarted arm leaves the rail **disarmed** (safe direction); a restart without a preceding
`--disarm` re-applies whatever the file says (the 2026-07-27 class). Always read both surfaces —
`--status` for the file, the boot line for the process — and treat disagreement as a stop.

---

## §6 — Bounded arming window

- **Absolute deadline, with timezone.** `plan_arm` computes `armed_until = now_utc + --hours`,
  truncated to the second, stored as ISO-8601 with a UTC offset. The operator states the intended
  end of session in **ET and UTC** before arming and chooses `<H>` so the computed deadline is at or
  before it. The deadline must fall inside attended time and **before the venue flat deadline**
  (16:45 ET regular, 12:59 ET early close — GO ADR Addendum 2026-07-22); windows above 8 h print a
  warning, not a refusal.
- **Who ends the session.** The operator who armed is responsible for the deliberate disarm (§9)
  **before** `armed_until`, and names themself in the session record at 5.7.
- **What expiry actually does (from source).** Per request, `handle_signal` halts **risk-add**
  (entry/add) once `arming_expiry_reason` is non-null; exit/flat keep relaying because the process
  is still `dry_run=false`. At **boot**, an expired/absent/malformed deadline with `dry_run=false`
  on disk produces an **in-memory implicit disarm** (`IMPLICIT DISARM at boot` warning) — the file
  on disk still says armed until `--disarm` runs. Expiry is therefore **not a substitute for
  disarm**: it stops new risk, leaves the process armed for exits, and leaves the disk armed. The
  2026-07-31 crash-loop class (boot refused on a lapsed deadline) is mitigated in the deployed code
  (readiness record §A3); the operating rule — disarm before the deadline — stands regardless.
- **Re-arm = new session.** A lapsed or disarmed window is never extended in place; re-arming
  repeats §4 E1–E3 and §5 in full with its own GO.

---

## §7 — Monitoring and stop conditions

**Frozen controls (pointers, not restatements).** `DD_TRIGGER`/`DD_SCALE` are frozen and
import-guarded in `core/dd_protection.py`; the rail's sizing path composes them with the lifecycle
multiplier (down-only, `core/lifecycle.py`) and the account-aggregate `cap_alloc`. The accepted
1%/40% portfolio policy reaches the sizing path only through the `POLICY_REGISTRY` row TB-D0 admits
(D-B11). M1 telemetry is the monitoring spine: pre-send decision persistence, honest transport
states, `transport_unknown` blocking, the `FileAckNotifier` alert/ack channel.

| Condition | How it shows | Rail behaviour (source) | Operator action | Evidence | Escalation |
|---|---|---|---|---|---|
| Stale / missing / malformed state input (constants, lifecycle key, DD state, execution state) | entry/add halted `qty_out 0`; `--status` unaffected | sizing host halts the signal; exits relay | stop adding risk; verify positions on Tradovate; repair only via the writers / migration; disarm **after** flat | halt reason line from the ledger projection | unresolved after one repair attempt → end session (§9) |
| Equity / peak read failure | HTTP 503 on entry/add; CRITICAL on exit/flat (relayed best-effort) | `_handle_post` | treat as feed/broker failure; confirm positions directly | the 503/CRITICAL line | end session if it recurs |
| Feed failure / stale bars (portfolio daemon) | per TB-S3 (H): reconnect with backoff; exits only, risk-adds refused, telemetry raised on barrier timeout | **UNIMPLEMENTED** — TB-S3 (A)/(H) spec, TB-I3 build | no discretionary substitution of a source; stop | per TB-S3 | — |
| `transport_unknown` | `transport_unknown: reconcile before retry` response; CRITICAL alert | ledger blocks further risk-add; never auto-retries | reconcile against CrossTrade Alert History (the source of truth for whether a signal validated) and Tradovate before any manual action; never re-POST | reconciler verdict | `RAIL_ONLY`/`REJECTED`/`QTY_MISMATCH`/`POSITION_MISMATCH`/`NO_FLAT_CONFIRM` → stop and flatten by hand if needed |
| Reconciliation failure on a fill | non-`CHAIN_OK` verdict | — | stop; do not add risk; flatten via the Tradovate/CrossTrade dashboards if a position is open (GO ADR Option C operator layer) | verdict + broker evidence overlay | end session |
| Restart uncertainty (boot id changed, boot line ≠ `--status`, unknown config in memory) | health `boot_id` differs; boot line mismatch | process may hold a different config than disk | stop; re-run 5.1–5.2; re-verify deployment identity before continuing | the two readings | any doubt → §9 end-of-session sequence |
| Alert not acknowledged | unacked file in the ack dir | pull-based channel; no push exists | acknowledge or act; attended-only posture is the mitigation | ack file | — |
| Kill switch (coordinated flatten-all + disarm + emit-disable, callable without the daemon) | — | **UNIMPLEMENTED** — TB-S3 (F) | today: flatten manually on Tradovate/CrossTrade, then `--disarm` + restart, then daemon emit-disable | per TB-S3 | — |

**Disarming is not flatness.** `dry_run=true` returns before the sender for **every** signal type,
exits included, so a disarm over an open position orphans it (c1-rail skill, invariant 2). Order:
broker-confirmed flat → disarm → restart → verify. Without the operator present, an agent that
discovers an armed host alerts and does **not** disarm.

No threshold in this section is new; each points at its owner. Strategy behaviour (what a leg does
on a bar) is the adapters' and the replay spec's, never this file's.

---

## §8 — Snapshot and restart state (implemented / verified vs. pending)

| Requirement | Status | Source / owner |
|---|---|---|
| Evidence-bound account snapshot sealed before B7 (three evidence files, relational checks, freshness at a session boundary) | **PENDING** — TB-T1 packet READY on PR #358; tool not built; seal contract PROPOSED | umbrella TB-T1 / TB-B7 stubs; `docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md` (PR #358) |
| Kernel drawdown breach check on the snapshot (`EvaluationState` + `_drawdown_outcome` under the tier geometry) | **PENDING** — TB-T1 check C2 (PR #358 revision at `ff6d756`) | same |
| Live peak seeding from the sealed snapshot (O-3): initialize account-scoped DD state from `historical_eod_peak` and verify before the execution fingerprint is sealed; arm-interlock check | **PENDING** — TB-S3 requirement + test, TB-I3 implementation, B7 procedural step. Today `c1_dd_state.json` is operator-typed (deploy README) and `ratchet_peak_equity` only raises it | umbrella §0.8 O-3 |
| Execution-state restore across restart (broker-confirmed base per leg) | **IMPLEMENTED in code and drilled** (`ExecutionStateStore.load_into` at `serve` and per request; drill `restart_confirmed_base`). **Gap:** no production write path populates the store — `set_confirmed_base` / `confirm_executed_base` have no callers outside tests (Q-M1WIRE-1 limb A2, CLOSED — FALSIFIED), so an `add` halts until an operator-attested write exists. Operator decision owed before any armed session relies on adds. | `ops/c1_rail/c1_rail_telemetry.py` @ `027a729`; `tests/ops/test_m1_acceptance_drills.py`; Q-M1WIRE-1 |
| Active-leg check (fixed leg set + digest consumed by the daemon registry, `LEG_MAP` and `c1_rail_arm.py`) | **PENDING** — TB-V1 | umbrella TB-V1 |
| Initial lifecycle state for the four legs (O-2) | **PENDING** — TB-V1 migration before the live test; the host halts any leg without a key | `_read_lifecycle_multiplier`; umbrella §0.8 O-2 |
| Protection policy row equals the TB-E1 sealed cell; `--arm` refuses otherwise | **PENDING** — TB-S3 (L) / TB-D0 | umbrella TB-S3 §0.5 (L) |

No live state is hand-edited. Where an interlock is missing, the disposition is **stop and return
to the owner**, never an improvised workaround.

---

## §9 — End of session and recovery

| Step | Actor | Command / source | Expected | Notes |
|---|---|---|---|---|
| 9.1 Flat and clean | Operator | Tradovate positions and working orders; CrossTrade Alert History for the window | "No open positions", no working orders, every alert accounted for | flatten by hand if needed (Option C operator layer); never disarm first |
| 9.2 **DISARM** (write 1 of 2) | **Operator** (an agent may, only after broker-verified flatness — c1-rail skill grant) | in-container `python ops/c1_rail/c1_rail_arm.py --disarm` | `after  : dry_run=True armed_until=None …`, `backup : …prev`, then the NOT YET IN EFFECT print | `--disarm` never consults the M1 gate and clears the deadline so a later bare edit cannot inherit a window |
| 9.3 **APPLY** (write 2 of 2) and verify | Operator | `fly machine restart <listener-machine-id> -a c1-rail`; then `fly logs -a c1-rail --no-tail` and `--status`; health | boot line `dry_run=True armed_until=-`; `--status` `dry_run=True armed_until=None`; health green | the disarm takes effect only on restart; both surfaces must agree |
| 9.4 Signal source disabled | Operator, per TB-S3 | daemon emit-disable per TB-S3 (pending); today: health `GET /` shows `effective_emit false` | `emit_enabled false` verified in-container (flags only) | — |
| 9.5 Evidence capture (private) | Operator (agent may run the dry-run plan) | `python ops/c1_rail/export_session_evidence.py --src-dir /data --dest <private root>/sessions/<date> --include-acks` (plan), then `--apply`; deviations list via the telemetry CLI `--deviations` | copies of `c1_rail_events.jsonl`, `c1_broker_evidence.jsonl`, `c1_execution_state.json`, acks, under the private root | ledger lines carry `current_equity` and `parsed.close`: **never paste raw lines**; use the allowlisted projection pattern (readiness record §A7-P, Step 2.8) for anything that enters a public record |
| 9.6 Session record | Operator | append to a **separate** private session log in the private root (not to the retrieved `RUNBOOK.md`); the public readiness-style record carries dates, digests, labels and redacted status lines only | digest of the private entry in the public record | §33a applies to every line |
| 9.7 Crash-loop / recovery | Operator | the private runbook's B7 arming log section (unchanged by this packet; §2 retrieval) and readiness record §A3 (what the in-memory implicit disarm removes — the lapsed-deadline crash loop — and what it does not: missing config `WAIT`, dead `CMD`, non-validating config, anything else) | recovery ends **disarmed**; `dry_run=false` is never a recovery target | recovery touches only `dry_run`/`armed_until`; it never rewrites constants, lifecycle, DD state or the daemon journal; a rollback is itself a deploy (six pre-conditions) |
| 9.8 Resume / re-arm | Operator | a new session: §4 E1–E3 re-evidenced, §5 in full, its own GO | — | after the B7 seal no executable change without reseal and a re-run live test before B10 (umbrella wave-3 gate); any change after n3 stops for the operator |

---

## §10 — Preservation obligation

The operator-placed account-preservation trade (at least one per venue week) is **not** part of
this procedure and is never agent-placed; the rail stays disarmed for it. The current deadline and
attestation state live on [STATE's forward board](../../../STATE.md#scheduled-forward-triggers) —
read it there; this reusable procedure carries no date.

---

## §11 — Coverage table (procedure section · governing source · implementation/evidence today · remaining gate)

| Section | Governing source | Implementation / evidence today | Remaining gate |
|---|---|---|---|
| §1 readiness | umbrella gate order; M1 ADR; Track A plan | listener and daemon deployed disarmed and inert 2026-09-12 (readiness record §A5/§A6); M1 `CODE_LANDED` | A7 → A8 → redeploy; every Track B gate |
| §2 private runbook | public-visibility ADR; umbrella TB-O1 | pre-prune blob retrieved to the private root, digest-verified; archive pin holds a later revision | umbrella owner: which revision the root carries going forward |
| §4 entry checklist | umbrella dependency graph + wave-3 gates; D-B13/D-B15 | TB-O1 prepared; TB-T1 READY (PR #358) | E1–E3, E5–E12 all open |
| §5 session start | `c1_rail_arm.py`, `c1_rail_http_server.py`, c1-rail skill, Track A plan §6 | arm/disarm/status tool + boot gates tested (`test_c1_rail_arm.py`, `test_c1_rail_http_server.py`) | TB-S3 daemon enable step; operator GO; M1 in image |
| §5.10 M1 interlock | M1 ADR Addendum 2026-07-31b; `plan_arm` | validator-backed refusal; acknowledgement path exists and is tested | none for the code; authority: never used under this file |
| §6 window | `arming_expiry_reason`, `plan_arm`, `load_config`; GO ADR 07-22 flat deadline | absolute UTC deadline, risk-add-only expiry, implicit disarm at boot (§A3 verified in-container) | none for the code |
| §7 monitoring | M1 ADR §2; `dd_protection`; lifecycle; GO ADR Option C | telemetry spine landed and drilled; alert channel pull-based | TB-S3 (F) kill switch, (H) feed/restart, (G) scheduler; TB-D0 policy row |
| §8 snapshot/restart | TB-T1 contract (PR #358); O-3; `ExecutionStateStore` | restore path drilled; no production confirmed-base writer (Q-M1WIRE-1 A2) | TB-T1 build; TB-S3/TB-I3 O-3; TB-V1 O-2 + active-leg digest; operator ruling on A2 |
| §9 end/recovery | `plan_disarm`; `export_session_evidence.py`; readiness record §A3; private runbook | tools committed and dry-run safe; recovery path attested 2026-09-11 | none |
| §10 preservation | STATE forward board; S1 ADR | operator-attested weekly | standing |

---

## §12 — Verification (runnable, read-only; none of these arms, emits, trades or writes host state)

```bash
# Acceptance artifact still validates; RESOLVED is still owed (expect exit 0, then "NOTE: M1 is not RESOLVED")
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
# Pre-arm form — expected exit 1 until A8 lands; never forced
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --require-resolved

# Relative links on this file and the four re-homed pointer files
python scripts/check_md_relative_links.py --strict --glob docs/notes/rail_build/ARMING_PROCEDURE.md

# Interlock and boot-gate tests
python -m pytest tests/ops/test_c1_rail_arm.py tests/ops/test_c1_rail_http_server.py -q

# The arm helper does not restart; the boot gate disarms in memory on a lapsed deadline
grep -n "NOT YET IN EFFECT" ops/c1_rail/c1_rail_arm.py
grep -n "IMPLICIT DISARM" ops/c1_rail/c1_rail_http_server.py

# Private copy integrity (operator, primary checkout; prints a digest, never content)
git hash-object lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/rail_build/RUNBOOK.md   # expect d523ee0d1e9d6054fdd75813a9bc25221102e635

# §33a: no dollar figure in this file (expect no output)
grep -nE '\$ ?[0-9]' docs/notes/rail_build/ARMING_PROCEDURE.md
```

**Boundary.** This file changed no runtime code, sizing rule, allocation, policy admission,
deployment configuration or historical decision. Decisions stay with their owners (the M1 ADR, the
GO ADR, the Track B umbrella, the Track A plan); no ADR was created for this procedure.
