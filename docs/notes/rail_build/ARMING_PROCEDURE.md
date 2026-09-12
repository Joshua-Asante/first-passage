# c1 rail — arming and session operating procedure (public, redacted)

**Type:** operating procedure · **Packet:** Track B TB-O1 ([umbrella](../../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) claim manifest row TB-O1)
**Date:** 2026-09-12 · **Author:** Claude Code (recorder) · **Authority:** Joshua (operator)
**Status:** **PREPARATION COMPLETE — NOT AUTHORIZED TO EXECUTE.** This file authorizes nothing. It
describes how an attended c1 session is armed, monitored, disarmed and recovered, with every step
anchored to source. **Gate status is never read from this file**: the
[Track B umbrella](../../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) claim
manifest and [STATE](../../../STATE.md) own what is open; §1 names the gates and their owners. No
agent arms, emits, trades, or edits host state under this file.

**Book this file serves:** the Tradeify portfolio — the operator-accepted Aegis 6J · Vanguard MGC ·
Striker MYM · ORB MNQ configuration with its protection/capacity rules
([acceptance record](../2026-09-10-tradeify-protection-selection.md)). The generic c1 session
procedure (§4–§7) applies to any deployed strategy on the rail; the portfolio prerequisites (§1)
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

## §1 — Gates and owners (status lives with the owners, not here)

Before any use of this file, read gate status from the umbrella's claim manifest and STATE's queue.
This section only names the gates, in the umbrella's order, and where each one's state is recorded.
An A7 pass (Track A's attended Stage 1 dry-run) discharges M1 item 5 **only**; it is not portfolio
deployment authority, and M1 `RESOLVED` (A8) is not a GO.

| Gate | Owner / where its state is recorded |
|---|---|
| M1 acceptance `RESOLVED` **in the deployed listener image** (the interlock reads the artifact baked into the image, so `RESOLVED` on the tree needs a redeploy) | [M1 ADR](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) §4 · [acceptance JSON](M1_MONITORING_ACCEPTANCE.json) · [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) A7/A8 · [readiness record](M1_STAGE1_DEPLOYMENT_READINESS.md) |
| Session-specific operator GO (every armed session needs its own) | [GO ADR](../../adr/2026-07-17-c1-rail-build-account-registration-go.md) · `CLAUDE.md` §Live-execution posture |
| TB-O1 (this procedure) merged before TB-B7 / TB-B10 | umbrella claim manifest |
| Approved production feed and source equivalence (O-4 → TB-I5) | umbrella §0.8 O-4 · [S2b build ADR](../../adr/2026-08-08-s2b-signal-daemon-build.md) Addendum 2026-09-11 |
| Runtime binding and per-symbol verification (TB-V1, TB-S3 (B)) | umbrella TB-V1 stub · `ops/c1_rail/c1_sizing_host_reference.py` `LEG_MAP` · `ops/c1_rail/c1_rail_listener.py` `INSTRUMENT_SYMBOLS` |
| Protection policy admitted for the book (TB-D0, D-B11) | umbrella TB-D0 stub · `core/dd_geometry.py` `POLICY_REGISTRY` |
| Multi-leg daemon and rail extension (TB-S3 → TB-I3) | umbrella TB-S3 packet |
| Dedupe implemented (TB-I4, D-B13) | [pre-registration](../../spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md) |
| Live test on the sealed image (TB-I3 live part, D-B15) | umbrella TB-I3 stub |
| Sealed snapshot and execution/replay fingerprint equality (TB-T1 → TB-B7) | umbrella TB-B7 stub · seal contract (PR #358) |
| Sole n3 (TB-E2) and deployment GO (TB-D2 → operator) | umbrella TB-E2 / TB-D2 stubs |
| Arm (TB-B10) | this file §4–§5, only after every row above is closed at its owner |

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

The five files that carry every behavioural claim in §4–§7. Other sources are cited inline where
used.

| Source | Anchor | What it pins for this procedure |
|---|---|---|
| `ops/c1_rail/c1_rail_arm.py` | `027a729` 2026-08-14 | `DEFAULT_CONFIG_PATH = /data/c1_rail_config.json`; `plan_arm` (M1 interlock via the validator with `require_resolved=True`; `--acknowledge-m1-unresolved` path; `armed_until = now_utc + hours`, second-truncated; self-check with `arming_expiry_reason`); `plan_disarm` (`dry_run=True`, `armed_until=None`); `describe_m1_gate` (`--status` line `m1_gate: status=… result=PASS|FAIL`); `_LONG_WINDOW_HOURS = 8.0` (warn, not refuse); `_write` keeps a one-deep `.prev` backup; `main` prints **NOT YET IN EFFECT … Restart to apply** — the tool edits the volume file and does not restart the host |
| `ops/c1_rail/c1_rail_http_server.py` | `027a729` | `load_config`: `dry_run` defaults True when absent; `dry_run=false` without `events_log_path` raises; expired/absent/malformed `armed_until` at boot → **IMPLICIT DISARM in memory** (log line), disk unchanged; `startup_log_line` prints `dry_run=… armed_until=…`; `ratchet_peak_equity` persists `max(peak, current)`; equity/peak read failure → HTTP 503 and no decision for entry/add, best-effort relay for exit/flat; `serve` loads `ExecutionStateStore` into `open_leg_state` at startup and each request; unhealthy ledger at startup blocks risk-add |
| `ops/c1_rail/c1_rail_listener.py` | `509b524` 2026-09-10 | `arming_expiry_reason` (absolute ISO-8601 deadline with offset; absent/naive/unparseable/past → expired; **risk-add only** — exit/flat keep relaying past expiry); `handle_signal` (risk-add blocked by ledger, by expiry; `dry_run` returns before the sender for **every** signal type, exits included; `transport_unknown` blocks further risk-add and never auto-retries); `INSTRUMENT_SYMBOLS` (three entries, no 6J/MGC) |
| `scripts/validate_c1_monitoring_acceptance.py` | `027a729` | `RESOLVED_REQUIRED`; `--require-resolved`; `--check-tree-skew` / `--require-tree-current` ("pre-deploy / pre-arm use only"); `fixture_hashes` describe the **deployed** bytes |
| `ops/c1_signal_daemon/daemon.py` | `36b3996` 2026-09-11 | `load_config`: `emit_enabled=true` or `m1_test.enabled=true` is accepted only with `strategy == m1_stage1_test`, `bar_period_s == 60` and both flags equal; the daemon boots `emit_enabled=false` — no portfolio strategy can emit from the deployed daemon |

**Distinguish three things throughout:** repository code (anchored above), historical evidence
(acceptance JSON notes, readiness record, private runbook), and **actual host state** — which only
a host read establishes (§5 step 5.1). This packet verified none of the host.

---

## §4 — Entry checklist (session-local checks; the gate order is the umbrella's)

The umbrella's dependency graph and wave-3 gates own the order in which Track B's gates close
(Track A `RESOLVED` → TB-I5 → D-B13 → TB-I4 → TB-I3 live test → TB-O1 → TB-B7 seal → TB-E2 → TB-D2
→ TB-B10) and the entry conditions of each; this file does not restate them. Confirm at the
umbrella that every gate up to TB-D2 is closed and the deployment GO is recorded, then run the four
checks below, which are the only ones a session adds. A row that cannot be evidenced is a **stop**,
returned to its owner; it is never waived, and a future gate is never recorded as satisfied because
its implementation is "expected".

| # | Check | Actor | How it is checked | Evidence recorded | If it fails |
|---|---|---|---|---|---|
| E1 | M1 `RESOLVED` in the **deployed** image | Operator (reads), agent may draft | In-container: `python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --require-resolved` → exit 0; `python ops/c1_rail/c1_rail_arm.py --status` → `m1_gate: status='RESOLVED' result=PASS`. A tree-side pass is not the gate; the image is. | the two printed lines (account token redacted) | stop; Track A (A8 + redeploy) owns it |
| E2 | Deployed build is the reviewed, sealed build | Operator | `--require-tree-current` in-container against the deployed artifact (pre-arm use); release/image identity equals the readiness record's last deploy and the B7 execution fingerprint | printed skew line; release + image tag | stop; a redeploy is a deploy (six pre-conditions), and a change after the seal re-seals and re-runs the live test before B10 |
| E3 | Session-specific operator GO | Operator | dated statement naming the session window and this procedure's revision; recorded before any host write | verbatim in the private session record; date + digest in the public record | no GO → nothing arms |
| E4 | Account flat, no working orders, no open reconciliation | Operator | Tradovate positions and working orders; CrossTrade Alert History; ledger `--deviations` and any `transport_unknown` since the last session resolved | attestation sentence with time (UTC and ET) | resolve first; never arm over an open position or an unreconciled send |

**Sole n3 adjudication and the stop rule after it:** TB-E2's result is adjudicated once by the
orchestrator; any change after n3 stops for the operator (governing plan S2; umbrella wave-3 gate).
This procedure never reopens n3.

---

## §5 — Session timeline (generic c1; runs only after §4 is all PASS)

Every host command is **operator-run** in the operator's own console unless marked *agent*. The
agent may draft commands, run read-only reads it is permitted to run, and read printed output. No
command below is a validation step that silently arms, emits, trades or changes host state; the four
writes (arm, apply, disarm, apply) are labelled and are the operator's.

> **Three rules this timeline exists to enforce** (each from a dated incident; sources in §3).
>
> 1. **An edit is not a restart.** `c1_rail_arm.py` validates and atomically writes
>    `/data/c1_rail_config.json`; the listener reads its config once at boot into a closure. A
>    written but un-restarted arm leaves the rail **disarmed** (the safe direction); a restart
>    without a preceding `--disarm` re-applies whatever the file says (2026-07-27). Always read both
>    surfaces — `--status` for the file, the boot line for the process — and treat disagreement as
>    a stop.
> 2. **Expiry is not a disarm.** `armed_until` is an absolute ISO-8601 deadline with a UTC offset
>    (`plan_arm`: `now_utc + --hours`, truncated to the second; above 8 h the tool warns, it does
>    not refuse). Past it, `handle_signal` halts **risk-add only**; exits keep relaying because the
>    process is still `dry_run=false`, and the disk still says armed. At boot, a lapsed, absent or
>    malformed deadline with `dry_run=false` on disk produces an **in-memory implicit disarm**
>    (`IMPLICIT DISARM at boot`) — the 2026-07-31 crash-loop class is mitigated in the deployed code
>    (readiness record §A3; `tests/ops/test_c1_rail_http_server.py` @ `027a729` pins the four invalid
>    shapes booting disarmed) — but the file is unchanged until `--disarm` runs. The operator who
>    armed disarms **deliberately, before the deadline**; a lapsed or disarmed window is never
>    extended in place — re-arming is a new session with its own GO (§4 E1–E4, then this timeline).
> 3. **Disarm is not flat.** `dry_run=true` returns before the sender for **every** signal type,
>    exits included, so a disarm over an open position orphans it (c1-rail skill, invariant 2).
>    Order: broker-confirmed flat → disarm → restart → verify. An agent that finds an armed host
>    without the operator present alerts and does **not** disarm.

| Step | Actor | Command / source | Expected observation | Refusal / stop |
|---|---|---|---|---|
| **Pre-arm** | | | | |
| 5.1 Host read — on-disk config | Operator (agent may) | PowerShell: `& fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"` · Git Bash: prefix `MSYS_NO_PATHCONV=1`. Judge by the printed text, not the exit code (Windows `fly ssh console -C` may exit 1 after correct output). | `current: dry_run=True armed_until=None …` and `m1_gate: status='RESOLVED' result=PASS` | `dry_run=False` or a non-null `armed_until` → **armed-host stop rule** (Track A plan §6): nothing else runs; with flatness attested, `--disarm` → restart → verify; without the operator present do **not** disarm (rule 3) |
| 5.2 Host read — running process | Operator (agent may) | `fly logs -a c1-rail --no-tail` filtered to `dry_run=`, `armed_until=`, `IMPLICIT DISARM` | boot line `dry_run=True armed_until=-`; no `IMPLICIT DISARM` line | boot line disagrees with `--status` → rule 1: stop, reconcile, never assume |
| 5.3 Health | Agent | `curl -sS https://<listener-app>.fly.dev/` and the daemon health `GET /` | listener `{"ok":true,…}`; daemon `effective_emit false`, `ceremony_state DISABLED`, `connected` per the approved feed's contract | unhealthy → stop |
| 5.4 Ledger health | Operator | ledger health is reported at boot (`events ledger unhealthy/blocked at startup`); deviations: `python ops/c1_rail/c1_rail_telemetry.py --events /data/c1_rail_events.jsonl --deviations` (read-only) | no unhealthy/blocked line; `arming_deviations: 0` or every listed record already explained in the private record | an unexplained deviation, a blocked ledger, or a truncated tail → stop (M1 §2.8: armed risk-add stays blocked until operator repair) |
| 5.5 State files present and seeded | Operator | existence and **shape** of `/data/lifecycle_state.json` (a key per active leg), `/data/c1_dd_state.json` (`peak_equity`; seeding per §7), `/data/c1_sizing_constants.json` (regenerated from production, never hand-typed), `/data/c1_execution_state.json`; the sizing host (`ops/c1_rail/c1_sizing_host_reference.py` @ `509b524`, `_read_lifecycle_multiplier`, `_read_dd_scale`) halts per request on any unreadable or unlisted input, so a missing key is a halt, not a default | keys only; **no values pasted** | a missing leg key or malformed file → stop; fix only through the documented writers / TB-V1 migration, never by hand-editing volume JSON |
| 5.6 Broker flatness and working orders | Operator | re-confirm §4 E4 immediately before the arm (Tradovate positions and working orders; CrossTrade Alert History clear) | attestation sentence with time (UTC and ET) | any position or working order → resolve first; never arm over an open position |
| 5.7 Window and deadline fixed | Operator | write the intended **absolute end of session** in ET and UTC; it must fall inside attended time and **before the venue flat deadline** (16:45 ET regular, 12:59 ET early close — GO ADR Addendum 2026-07-22); choose `<H>` so `now_utc + <H>h` is at or before it; name the person who will disarm | the deadline and the name in the session record | no absolute deadline → no arm |
| **Arm** | | | | |
| 5.8 **ARM** (write 1 of 4) | **Operator only** | in-container: `python ops/c1_rail/c1_rail_arm.py --arm --hours <H>` | prints `before : dry_run=True …`, `after  : dry_run=False armed_until='<UTC deadline>' window=open`, `backup : /data/c1_rail_config.json.prev`, then `*** NOT YET IN EFFECT — the running process still holds its old config. Restart to apply`; a `WARNING: <H>h window is long` appears above 8 h | `ERROR: refusing to arm: …` → stop; read the reason; do **not** pass `--acknowledge-m1-unresolved` (5.10); do **not** hand-edit the file |
| 5.9 **APPLY** (write 2 of 4) and verify | **Operator only** | `fly machine restart <listener-machine-id> -a c1-rail` (id from `fly machine list -a c1-rail`; the tool's own print names `fly apps restart c1-rail`) · then `fly logs -a c1-rail --no-tail` and `--status` | boot line `dry_run=False armed_until=<deadline>` and `--status` `window=open`; health green; **no** `IMPLICIT DISARM` line | an `IMPLICIT DISARM` line means the deadline was already past or malformed at boot (rule 2): run `--disarm`, restart, start over; a restart that does not come back → 5.19 |
| 5.10 M1 interlock precision | — | `plan_arm` refuses when `m1_acceptance_reason` is non-null. The code carries an explicit acknowledgement path for a **structurally valid but unresolved** artifact (`--acknowledge-m1-unresolved '<reason>'` writes an `arming_deviation` ledger record **before** the config edit and refuses the arm if the record cannot be written); a forged or status-only `RESOLVED` is refused on both paths (`tests/ops/test_c1_rail_arm.py` @ `027a729`). | — | **This procedure and this handoff authorize no such deviation.** Code capability is not operator authority. The M1 ADR's falsifier names a third armed session while unresolved as the trigger for structural escalation; the acknowledgement path is never the readiness solution. A hand edit of `/data/c1_rail_config.json` is the same act with the audit trail removed and is barred. |
| 5.11 Signal source enable | Operator, per TB-S3 | the portfolio daemon's emit-enable step — **pending** (§7). Today the deployed daemon accepts `emit_enabled=true` only for the M1 test identity. | per TB-S3 | absent spec → no session |
| **Monitor** | | | | |
| 5.12 Attend until the deliberate disarm | Operator | §6 stop conditions; the operator 15:55 ET flat-check on every session that carried open risk (GO ADR Option C); disarm at or before the 5.7 deadline | evidence per §6 | any §6 stop → go to 5.13 now |
| **Close** | | | | |
| 5.13 Flat and clean | Operator | Tradovate positions and working orders; CrossTrade Alert History for the window | "No open positions", no working orders, every alert accounted for | flatten by hand if needed (Option C operator layer); never disarm first (rule 3) |
| 5.14 **DISARM** (write 3 of 4) | **Operator** (an agent may, only after broker-verified flatness — c1-rail skill grant) | in-container `python ops/c1_rail/c1_rail_arm.py --disarm` | `after  : dry_run=True armed_until=None …`, `backup : …prev`, then the NOT YET IN EFFECT print | `--disarm` never consults the M1 gate and clears the deadline so a later bare edit cannot inherit a window |
| 5.15 **APPLY** (write 4 of 4) and verify | Operator | `fly machine restart <listener-machine-id> -a c1-rail`; then `fly logs -a c1-rail --no-tail` and `--status`; health | boot line `dry_run=True armed_until=-`; `--status` `dry_run=True armed_until=None`; health green | the disarm takes effect only on restart (rule 1); both surfaces must agree |
| 5.16 Signal source disabled | Operator, per TB-S3 | daemon emit-disable (pending, §7); today: health `GET /` shows `effective_emit false` | `emit_enabled false` verified in-container (flags only) | — |
| 5.17 Evidence capture (private) | Operator (agent may run the dry-run plan) | `python ops/c1_rail/export_session_evidence.py --src-dir /data --dest <private root>/sessions/<date> --include-acks` (plan, then `--apply`; tool @ `027a729`); deviations list as in 5.4 | copies of `c1_rail_events.jsonl`, `c1_broker_evidence.jsonl`, `c1_execution_state.json`, acks, under the private root | ledger lines carry `current_equity` and `parsed.close`: **never paste raw lines**; use the allowlisted projection pattern (readiness record §A7-P, Step 2.8) for anything that enters a public record |
| 5.18 Session record | Operator | append to a **separate** private session log in the private root (not to the retrieved `RUNBOOK.md`); the public readiness-style record carries dates, digests, labels and redacted status lines only | digest of the private entry in the public record | §33a applies to every line |
| **Recover** | | | | |
| 5.19 Crash-loop / recovery | Operator | the private runbook's B7 arming log section (unchanged by this packet; §2 retrieval) and readiness record §A3 (what the in-memory implicit disarm removes — the lapsed-deadline crash loop — and what it does not: missing config `WAIT`, dead `CMD`, non-validating config, anything else) | recovery ends **disarmed**; `dry_run=false` is never a recovery target | recovery touches only `dry_run`/`armed_until`; it never rewrites constants, lifecycle, DD state or the daemon journal; a rollback is itself a deploy (six pre-conditions) |
| 5.20 Resume / re-arm | Operator | a new session: §4 re-evidenced, this timeline from 5.1, its own GO | — | after the B7 seal no executable change without reseal and a re-run live test before B10 (umbrella wave-3 gate); any change after n3 stops for the operator |

---

## §6 — Monitoring and stop conditions

**Frozen controls (pointers, not restatements).** `DD_TRIGGER`/`DD_SCALE` are frozen and
import-guarded in `core/dd_protection.py` (@ `94041d9`); the rail's sizing path composes them with
the lifecycle multiplier (down-only, `core/lifecycle.py` @ `027a729`) and the account-aggregate
`cap_alloc`. The accepted 1%/40% portfolio policy reaches the sizing path only through the
`core/dd_geometry.py` `POLICY_REGISTRY` row TB-D0 admits (D-B11; the registry is empty at
`4929c44`). M1 telemetry is the monitoring spine: pre-send decision persistence, honest transport
states, `transport_unknown` blocking, the `FileAckNotifier` alert/ack channel. Feed-failure
handling and the kill switch are **not built** (§7).

| Condition | How it shows | Rail behaviour (source) | Operator action | Evidence | Escalation |
|---|---|---|---|---|---|
| Stale / missing / malformed state input (constants, lifecycle key, DD state, execution state) | entry/add halted `qty_out 0`; `--status` unaffected | sizing host halts the signal; exits relay | stop adding risk; verify positions on Tradovate; repair only via the writers / migration; disarm **after** flat | halt reason line from the ledger projection | unresolved after one repair attempt → close (5.13) |
| Equity / peak read failure | HTTP 503 on entry/add; CRITICAL on exit/flat (relayed best-effort) | `_handle_post` | treat as feed/broker failure; confirm positions directly | the 503/CRITICAL line | close if it recurs |
| `transport_unknown` | `transport_unknown: reconcile before retry` response; CRITICAL alert | ledger blocks further risk-add; never auto-retries | reconcile against CrossTrade Alert History (the source of truth for whether a signal validated) and Tradovate before any manual action; never re-POST | reconciler verdict | `RAIL_ONLY`/`REJECTED`/`QTY_MISMATCH`/`POSITION_MISMATCH`/`NO_FLAT_CONFIRM` → stop and flatten by hand if needed |
| Reconciliation failure on a fill | non-`CHAIN_OK` verdict | — | stop; do not add risk; flatten via the Tradovate/CrossTrade dashboards if a position is open (GO ADR Option C operator layer) | verdict + broker evidence overlay | close |
| Restart uncertainty (boot id changed, boot line ≠ `--status`, unknown config in memory) | health `boot_id` differs; boot line mismatch | process may hold a different config than disk (rule 1) | stop; re-run 5.1–5.2; re-verify deployment identity before continuing | the two readings | any doubt → close (5.13) |
| Alert not acknowledged | unacked file in the ack dir | pull-based channel; no push exists | acknowledge or act; attended-only posture is the mitigation | ack file | — |

No threshold in this section is new; each points at its owner. Strategy behaviour (what a leg does
on a bar) is the adapters' and the replay spec's, never this file's.

---

## §7 — Capabilities this procedure depends on that are not built (owner named; no workaround)

Each item is owed to the named packet and is absent from the deployed rail and daemon. Where one is
missing the disposition is **stop and return to the owner** — never hand-edit live state, never
improvise an interlock, never substitute a source.

- **Evidence-bound account snapshot seal** with the kernel drawdown breach check (C2) — TB-T1
  sealer, then TB-B7 (umbrella stubs; seal contract on PR #358).
- **Live peak seeding from the sealed snapshot (O-3)** — initialize and verify `c1_dd_state.json`
  from `historical_eod_peak` before the execution fingerprint is sealed, with an arm-interlock check
  — TB-S3 spec → TB-I3; today the peak is operator-typed and `ratchet_peak_equity` only raises it.
- **Kill switch** (coordinated flatten-all + disarm + emit-disable, callable without the daemon) —
  TB-S3 (F). Today: flatten by hand on Tradovate/CrossTrade, then 5.14–5.16.
- **Feed failure, bar-time barrier timeout and restart semantics** for the multi-leg daemon (exits
  only, risk-adds refused, adapters restart warm and reconcile to the broker-confirmed position)
  and the **EOD flatten scheduler** — TB-S3 (A)/(G)/(H) → TB-I3.
- **Portfolio emit-enable / emit-disable step** (5.11, 5.16) — TB-S3 (F)/(K) → TB-I3; the deployed
  daemon accepts `emit_enabled=true` only for the M1 test identity (`load_config` @ `36b3996`).
- **Active-leg digest and initial lifecycle state for the four legs (O-2)** — TB-V1; the host halts
  any leg without a key.
- **Protection-policy row equal to the TB-E1 sealed cell, with `--arm` refusing otherwise** —
  TB-S3 (L) / TB-D0.

**Implemented, with a gap.** Execution-state restore across restart is in code and drilled
(`ExecutionStateStore.load_into` at `serve` and per request; drill `restart_confirmed_base` —
`ops/c1_rail/c1_rail_telemetry.py` @ `027a729`, `tests/ops/test_m1_acceptance_drills.py` @
`25711e2`), but **no production write path populates the store**: `set_confirmed_base` /
`confirm_executed_base` have no callers outside tests
([Q-M1WIRE-1](../../briefs/Q-M1WIRE-1-arming-interlock-coverage.md) limb A2, CLOSED — FALSIFIED),
so an `add` halts until an operator-attested write exists. The operator decision that closure names
is owed before any armed session relies on adds.

---

## §8 — Preservation obligation

The operator-placed account-preservation trade (at least one per venue week) is **not** part of
this procedure and is never agent-placed; the rail stays disarmed for it. The current deadline and
attestation state live on [STATE's forward board](../../../STATE.md#scheduled-forward-triggers) —
read it there; this reusable procedure carries no date.

---

## §9 — Verification (runnable, read-only; none of these arms, emits, trades or writes host state)

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
