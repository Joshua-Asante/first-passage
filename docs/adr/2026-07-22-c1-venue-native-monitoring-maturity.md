# ADR 2026-07-22 — Adopt a venue-native c1 monitoring spine and staged maturity gates

**D-S-A domain:** system
**Status:** `Accepted` — operator ratified 2026-07-23 ("flip ADR to ratified and proceed to close the monitoring gap"); architecture policy in force. **AMENDED 2026-07-31, operator-ratified (Addendum 2026-07-31b): the M1 gate's trigger is the ARM, not the send** — `dry_run=false` may not be set while M1 is not `RESOLVED`. Acceptance authorizes M1 implementation; it does **not** claim M1 is `RESOLVED` or permit an armed session (§4 M1 verdict is the next-**arm** gate).
**Decision date:** 2026-07-22
**Supersedes:** `2026-07-17-c1-rail-build-account-registration-go.md` in part — the next armed session/B7-REFIRE Stage 2 gains the M1 monitoring gate defined here (trigger amended from "send" to "session" 2026-07-31b)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-loop-s2-signal-host-fork.md` — §4 item 5 **signal-origin definition only** (TradingView-only → ruled Python-native host). Item 5 itself, expected sizing, Stage-1 `dry_run`, deletion decline, and the bar on **silent** redefinition stand.
**Superseded-in-part-by:** `2026-08-07-loop-s5-bounded-promotion-lane.md` — §5 forbidden move *“Creating a second tier/state writer or autonomous promotion path”* **autonomous promotion path limb only** (bounded sandbox lane). No second tier/state writer; arm-gate, reflex layer, and unattended bar **stand**.
**Retain-until:** none

**Related:** `2026-07-11-ops-cfd-estate-retirement.md` (venue-native rebuild
rule); `2026-07-10-strategies-never-locked-lifecycle-governance.md`;
`docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md` (parked historical test);
`docs/briefs/Q-DECAY-1-closure-scope-split.md`; proposed
`2026-07-22-challenge-era-substrate-retirement.md`;
`2026-08-07-loop-s2-signal-host-fork.md` (express item-5 origin supersession).

---

## §0 — Rule 0 reads and cheap falsifier

Read before authoring on 2026-07-22 after fetching `origin/main` and
fast-forwarding the current branch through the latest PR-review fix.

- `ops/c1_rail/c1_rail_listener.py` — anchor `48fb15f` (2026-07-18).
  `RailAction` records sizing decision, `sent`, `dry_run`, payload text, and
  HTTP status. `sent=True` means the HTTP sender returned; it does not mean
  CrossTrade validated or Tradovate filled the order.
- `ops/c1_rail/crosstrade_payload.py` — anchor `13c1942` (2026-07-18).
  `_urllib_sender` and `send_to_crosstrade` return an integer HTTP status only;
  response body, CrossTrade validation stage, broker order ID, fill, and reject
  reason are discarded.
- `ops/c1_rail/c1_rail_http_server.py` — anchor `1ec003f` (2026-07-19). `_audit`
  emits an unstructured log line after `handle_signal`; unauthorized paths,
  ignored non-JSON alerts, equity failures, and handler exceptions have no
  shared structured event contract. The optional audit file is a normal text
  `FileHandler`.
- `ops/c1_rail/c1_sizing_host_reference.py` — anchor `7a95f81` (2026-07-18).
  `SizingDecision` already contains the quantity, floor/halt state, DD scale,
  lifecycle multiplier, and effective risk needed for a monitoring event.
  The sizing host deliberately does not own broker fills or exits.
- `core/lifecycle.py` — anchor `4441c72` (2026-07-11). Call-1 breach logic and
  Call-4 mechanical beta-death controls exist; neither ingests live fills.
- `lab/discovery/lifecycle_call1/evaluate.py` — anchor `a38676d`
  (2026-07-14). Thin or missing data returns `AMBIGUOUS`; its
  `MIN_TRADE_COUNT=30` is explicitly provisional pending 2026-08-08.
- `docs/notes/rail_build/RUNBOOK.md` — anchor `d9e8f2a` (2026-07-21).
  B6 proved synthetic sizing and controlled SIM fills. It also records two
  monitoring-relevant incidents: the rail reported HTTP 200 while CrossTrade
  failed validation on a wrong secret, and B7 delivered non-JSON informational
  alerts instead of the B1 JSON order payload. B7-REFIRE still requires a
  real strategy signal through the complete chain.
- `docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` — anchor
  `1ec003f` (2026-07-19). It authorizes the c1 rail and says a first fill
  unblocks the Q-NAS-ECR successor, ORB decay calibration, Q-DECAY re-arm, and
  lifecycle Call-1; it does not build their data path.
- `docs/adr/2026-07-11-ops-cfd-estate-retirement.md` — anchor `ba943a1`
  (2026-07-17). Trigger A requires a repository-native rebuild against the
  actual venue and explicitly forbids restoring the DXTrade-shaped
  `live_journal` estate.
- `docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md` — anchor `47cc3eb`
  (2026-07-12). The frozen Copygram→DXTrade gate is unreachable; MNQ/Tradovate
  is not type-preserving and requires a fresh Pre-Q.
- `docs/briefs/Q-DECAY-1-closure-scope-split.md` — anchor `79b78b7`
  (2026-07-10). ECR is execution fidelity, not decay; common-mode edge death
  remains uncovered.
- `docs/methodology/strategy_lifecycle.md` — anchor `ae91ddd`
  (2026-07-17). Call-1 uses rolling PF against a pre-registered floor; Call-4
  is sequenced first; surveillance is scheduled, not discretionary P&L
  staring.
- `PIPELINES.md` — anchor `3c14385` (2026-07-21). P5 is built/disarmed; P6 is
  retired. The allowed rebuild path is venue-native, not a restore.

**Cheap falsifier, run parent-side before authoring:**

```text
send_to_crosstrade(fake_sender_returning_200) -> 200 (int)
RailAction fields:
  decision, sent, dry_run, payload_text, http_status
Can RailAction represent response body, execution status, broker order ID,
or event ID? False.
ops/*telemetry*.py: zero files.
ops/*.py references to event_id, execution_verified, fill_qty,
broker_order, events_log_path, or jsonl: zero.
```

This confirms the gap at the cheapest level: the current rail can prove that
it computed and attempted transport, but cannot represent downstream
acceptance, fill truth, or a durable event identity. The B6 false-positive
HTTP-200 incident is therefore architectural, not merely a missing dashboard.

---

## §1 — Context

The c1 rail is operationally ahead of its monitoring. Sizing, fail-safe state
reads, webhook transport, and controlled SIM fills have been demonstrated, but
the automated evidence stops at an HTTP status and a human-readable log line.
CrossTrade Alert History and Tradovate remain the actual sources of validation,
fill, position, and flatness truth, checked manually by the attended operator.

That asymmetry has already produced two incidents. First, four orders appeared
successfully sent from the rail while CrossTrade rejected all four at
validation. Second, real strategy signals reached the webhook but an
informational alert shadowed the B1 JSON payload, so no order was created.
Neither was a sizing-algorithm failure; both were observability failures at the
seams between independently healthy components.

The retired P6 estate cannot close this gap. It was coupled to
Copygram/DXTrade/Alchemy and its ECR ratio cannot detect strategy decay.
Meanwhile, lifecycle Call-1 and Call-4 are mechanically built but honestly
data-starved. A monitoring decision must therefore separate what can be proven
before the next `dry_run=false` entry/add send from what can only mature after
fills accrue.

**Decision driver (one sentence):** live-order transport must not outrun the
ability to correlate intent, downstream acceptance, broker fills, and flatness,
while statistical edge surveillance must remain `AMBIGUOUS` rather than
manufacture confidence from thin data.

---

## §2 — Decision

**Decision:** build a new c1 venue-native monitoring spine with three explicit
maturity levels, and make the first level a prerequisite for the next
`dry_run=false` entry/add send. The monitoring subsystem extends the existing
rail records; it does not restore `live_journal`, reinterpret ECR as decay, or
create a second sizing or lifecycle authority.

### M1 — operational chain observability (required before the next armed SESSION)

> **Trigger amended 2026-07-31 (Addendum 2026-07-31b, operator-ratified).** This heading read
> *"required before the next armed send"* until 2026-07-31. The gate's object is now the **arm**:
> **`dry_run=false` may not be set while M1 is not `RESOLVED`.** Rationale — the send is
> market-triggered and therefore cannot be complied with prospectively; the arm is the operator's
> own act. See the addendum for the two sessions that exposed the gap.

M1 closes the immediate operational maturity gap. It is code- and SIM-testable
before statistically meaningful live data exists.

1. **Versioned structured event stream.** Add an ops-owned append-only JSONL
   writer, consumed by `c1_rail_http_server` and configured with an explicit
   `events_log_path`. The stream uses immutable event variants rather than one
   row that must somehow contain fields unavailable at every stage:
   - `request_received` — common envelope, auth/body category, UTC timestamp,
     body hash; parsed B1 fields are nullable;
   - `decision` — flattened `SizingDecision`, equity metadata, and pre-send
     persistence result;
   - `transport_result` — exactly one of
     `{not_attempted, accepted, failed, unknown}`;
   - `broker_evidence` — CrossTrade/Tradovate facts attached later;
   - `reconciliation` — fixed verdict over the joined chain.
   Unauthorized, non-JSON, equity-failure, and handler-error events therefore
   remain representable without inventing B1 identity.

2. **Identity semantics.** `event_id` identifies one received attempt;
   `order_id` remains stable for the B1 signal identity and supports dedupe and
   downstream joining. Retries receive a new `event_id` without pretending to
   be a new strategy signal.

3. **No secrets in telemetry.** The ledger never stores `secret_key`,
   `webhook_secret`, `path_token`, bearer token, or raw outbound payload.
   Bodies are represented only by allow-listed fields and hashes. Any secret
   detected by tests or review is a release blocker.

4. **Honest transport state and uncertainty.** HTTP 200 is named
   `transport_accepted`, never `execution_verified`. A timeout, connection
   reset, or exception after bytes may have left the process is
   `transport_unknown`, not “no order placed.” On `unknown`, the server
   acknowledges the TradingView request to suppress upstream retry, raises a
   CRITICAL notification, blocks further entry/add attempts for that leg, and
   requires broker reconciliation. It never retries automatically. CrossTrade
   validation and Tradovate fill remain separate states. Response-body parsing
   may be added only after its live schema is captured and frozen; unknown
   bodies remain unverified.

5. **Broker-evidence overlay and reconciliation.** Before a verified read-only
   API exists, an operator-attested JSONL overlay is acceptable because the
   rail is attended. It joins `event_id`/`order_id` to:
   CrossTrade `{receive, validate, execute, trace_id}` and Tradovate
   `{order_id, status, fill_qty, fill_price, position_after, flat_confirmed}`.
   A read-only reconciler emits exactly:
   `CHAIN_OK`, `RAIL_ONLY`, `REJECTED`, `QTY_MISMATCH`, `POSITION_MISMATCH`,
   or `NO_FLAT_CONFIRM`.

6. **Fail-safe asymmetry.**
   - If the ledger cannot persist the pre-send decision for an `entry` or
     `add`, the rail halts that risk-adding order.
   - The adapter classifies `signal_type` before equity/state resolution.
     `exit` and `flat` bypass equity, DD, lifecycle, constants, and telemetry
     preconditions; they relay best effort and raise a CRITICAL operator
     notification if evidence cannot be written.
   - If post-send event persistence fails, the rail never retries the order
     automatically; it alerts and leaves reconciliation to the operator.
   This preserves the standing rule: automation may fail closed on risk-add,
   never fail closed on risk reduction.

7. **Confirmed-base interlock.** The sizing host may calculate an intended base
   quantity, but it must not mark that quantity as executed before broker
   evidence exists. An `add` is blocked until a durable execution-state record
   contains the broker-confirmed base fill quantity; partial fills use the
   actual filled base. This state survives process restart and is cleared only
   by broker-confirmed flatness. The add formula remains unchanged; its input
   changes from intended to confirmed quantity.

8. **Concurrency and durability contract.** Because the HTTP server is
   threaded, each JSONL record is written under a cross-thread/process file
   lock as one UTF-8 append, followed by flush and `fsync` before lock release.
   Each record carries a monotonic sequence number. Startup validates the full
   stream; malformed or truncated tails block armed risk-add until operator
   repair, never receive silent truncation. Tests race simultaneous MYM/MNQ
   events and inject crashes/partial tails.

9. **M1 arming gate** (retitled by Addendum 2026-07-31b, which moved the trigger from the send to the arm). B7 was already armed without fills on 2026-07-20 and
   re-armed into the alert-shadowing failure on 2026-07-21. This ADR cannot
   retroactively gate those attempts. It gates the **next `dry_run=false`
   entry/add send**, including B7-REFIRE Stage 2:
   - a real strategy signal at `dry_run=true` produces a structured event with
     the expected quantity and no informational-alert shadowing;
   - a controlled SIM fire joins rail intent → CrossTrade
     RECEIVE/VALIDATE/EXECUTE → Tradovate fill at expected quantity;
   - an exit/flat joins to `flat_confirmed=true`;
   - wrong credentials, non-JSON signal-bar payload, equity failure, sizing
     halt, genuine quantity floor, telemetry write failure, transport timeout,
     partial fill, and restart each produce a distinct tested outcome;
   - a deployed operator-reachable notification channel delivers and the
     operator acknowledges a test alert. A test double alone cannot pass M1.

M1 does not require continuous broker API polling. Manual CrossTrade/Tradovate
evidence is sufficient only under the existing attended-only posture. Any
future unattended authorization must first replace that manual overlay with
automated downstream truth.

### M2 — execution-fidelity monitoring (starts with the first armed fill)

M2 uses the M1 identity spine to build venue-native fill evidence:

1. Normalize completed MYM/MNQ broker records into a small fill/trade ledger
   carrying expected alert price, actual fill, quantity, commission, leg
   identity, base/add cohort, and session flatness.
2. Report delivery rate, reject rate, quantity parity, entry/exit slippage,
   partial fills, latency where observable, and base-vs-add cohort outcomes.
3. Never use M2 metrics as a strategy-decay trigger. They characterize
   execution fidelity and supply evidence to a **fresh** Q-NAS-ECR successor
   Pre-Q on Tradovate/MNQ microstructure.
4. The frozen DXTrade thresholds do not transfer. Any MNQ/MYM slippage or ECR
   thresholds freeze in that successor Pre-Q before M2 live results are read.

M2 may begin on fill one. It cannot be declared statistically mature merely
because the plumbing exists.

### M3 — lifecycle and portfolio surveillance (data-dependent)

M3 connects normalized completed trades to existing lifecycle machinery:

1. A thin adapter computes per-leg rolling PF and trade count and calls the
   existing `lifecycle_call1` harness. It does not reimplement
   `decay_breach`, persistence, or demotion.
2. Missing or sub-threshold data returns `AMBIGUOUS` and cannot increment the
   consecutive-breach counter.
3. The current Call-1 harness carries CFD Pepperstone Striker baselines and
   cannot evaluate MYM/MNQ venue editions as-is. M3 is blocked until a
   venue-native per-leg PF baseline and matching σ panel are pre-registered,
   validated, and admitted. No CFD baseline is silently relabeled futures.
4. `MIN_TRADE_COUNT` remains provisional until its own 2026-08-08
   pre-registration. This ADR does not ratify 30.
5. Call-4 beta-cohesion remains a separately specified data-dependent
   diagnostic. The existing mechanical 2-of-4/3-of-4 controls stand; this ADR
   neither fabricates a cohesion result nor changes their constants.
6. Any lifecycle write remains down-only and uses the existing
   `lifecycle_state.json` path. Promotions, retirement, and full beta shutdown
   retain their existing operator boundaries.
7. If the proposed challenge-era substrate retirement later removes a
   Pepperstone baseline, the M3 adapter must consume the canonical baseline
   admitted at that time; monitoring does not silently retain or revive a
   retired anchor.

### Layer and ownership boundary

- `ops/` owns hot-path events, broker evidence, reconciliation, and operator
  notification.
- `lab/discovery/lifecycle_call1/` remains the statistical Call-1 harness.
- `core/lifecycle.py` remains the only authorization-rule owner.
- `ops/sentinel/` remains repository-governance scanning and is not expanded
  into trading telemetry.
- Pine, allocations, `dd_protection` constants, lifecycle values, and sizing
  arithmetic are unchanged. This ADR explicitly authorizes one execution-state
  correction: entry intent no longer seeds add state; broker-confirmed base
  quantity does.

**Effective:** architecture policy became effective 2026-07-23 on operator
acceptance (this ADR `Accepted` + matching reverse supersession edge on the
c1 GO ADR + regenerated ADR index). Acceptance authorizes implementation; it
does **not** claim M1 is built or permit an armed session. The separate §4 M1
verdict gates the next **arm** (amended 2026-07-31b — was "the next armed send").
Acceptance alone changes no B7 arm state.

**Scope:** the c1 MYM/MNQ Tradeify/Tradovate rail and its lifecycle data feed.
ORB-MNQ execution, another account/firm, unattended operation, strategy
parameters, and statistical threshold selection are separate decisions.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Restore `ops/live_journal/` and ECR | Explicitly forbidden by the estate-retirement ADR; Copygram/DXTrade/Alchemy schemas and counterfactuals are not type-preserving for CrossTrade/Tradovate futures. |
| Treat the existing text audit log as sufficient | B6 falsified this: `sent=True http_status=200` coexisted with CrossTrade validation failure. Text transport logs cannot represent broker truth or reliably join fills. |
| Build a full broker API integration before the next armed send | Overbuilds an attended SIM rail around an endpoint/schema not yet verified. A structured ledger plus attested evidence closes M1 honestly and creates the join seam for later automation. |
| Expand `ops/sentinel/` into execution monitoring | Violates Sentinel’s report-only repository-governance purpose and mixes batch doc hygiene with the live trading path. |
| Make ECR the lifecycle decay trigger | Q-DECAY-1 proved ECR is execution fidelity and divides out edge magnitude; a faithfully executed dead edge can retain ECR near one. |
| Wait for statistically meaningful fills before building anything | Inverts causality: without M1, the fills cannot be trusted or joined. Operational observability must precede the data whose statistical maturity necessarily follows later. |
| Require M2/M3 maturity before the next armed session | Impossible by construction—both need armed fills. M1 is the next-**arm** gate (amended 2026-07-31b); M2/M3 remain explicitly data-dependent. |
| Allow live sends when the event ledger is unavailable | Repeats the present maturity gap. Risk-add without durable intent evidence is forbidden; exits retain their separate fail-open-to-flat rule. |

---

## §4 — Falsifier and revert trigger

**Hypothesis:** if c1 has a durable per-attempt identity and a broker-evidence
join, then every attended SIM order can be classified unambiguously as a
pre-send halt, dry run, transport-only attempt, downstream reject, correct
fill, quantity mismatch, or unconfirmed flat—without restoring DXTrade
machinery or changing the quantity formula for the same broker-confirmed base
input.

**RESOLVED — M1 closes the operational gap when all are true:**

1. Offline tests cover every M1 outcome and prove no secret reaches the event
   file.
2. Planted event-log write failure halts entry/add, never blocks exit/flat, and
   never causes automatic order retry.
3. Planted equity/state failure still relays an exit/flat without invoking
   sizing, and broker-confirmed flatness clears persisted execution state.
4. Concurrent MYM/MNQ writes remain valid, ordered JSONL; injected truncated
   tails block armed risk-add until explicit repair.
5. B7-REFIRE Stage 1 produces a structured `dry_run` event from a real strategy
   signal with expected sizing.
6. A controlled SIM sequence reconciles rail intent, CrossTrade execution
   success, Tradovate filled quantity, and final flatness as `CHAIN_OK`.
7. Replaying the B6 wrong-secret shape yields `RAIL_ONLY` or `REJECTED`, never
   `CHAIN_OK`, despite HTTP 200.
8. A transport timeout after send yields `transport_unknown`, suppresses
   upstream/automatic retry, blocks the next risk-add, and requires
   reconciliation. CrossTrade `order_id` idempotency is empirically proven in
   SIM or explicitly treated as unproven; no correctness claim rests on it.
9. A rejected entry cannot authorize an add; a partial entry authorizes add
   sizing only from its broker-confirmed base quantity, including after
   process restart.
10. A deployed operator-reachable notification channel delivers and receives
    an operator acknowledgement.
11. Unaffected entry arithmetic, payload, fail-safe, and dry-run invariants
    remain behavior-identical. Tests that currently encode “intended entry
    quantity immediately becomes executed base” are intentionally replaced by
    reject/partial/full-fill confirmation cases; preserving that old assertion
    would preserve the defect this ADR closes.

**FALSIFIED — revert and redesign if any occurs:**

- telemetry failure permits an entry/add to send without a persisted
  pre-send decision;
- telemetry, equity, lifecycle, DD, or constants failure blocks an exit/flat;
- HTTP 200 can still be surfaced as execution verified without downstream
  evidence;
- an uncertain send is automatically retried, or an unconfirmed/partial base
  can spawn an add sized from intended quantity;
- concurrent writes can corrupt the stream or startup silently discards a
  malformed tail;
- joining the controlled SIM fill requires Copygram, DXTrade, Alchemy, or
  retired `live_journal` schemas;
- adding monitoring changes the entry quantity formula, add arithmetic for an
  identical confirmed-base input, lifecycle multiplier, order payload
  semantics, or Pine behavior. The intended→confirmed execution-state
  correction in §2 is authorized and is not a falsifier.

**AMBIGUOUS — stay disarmed:** real strategy JSON does not arrive, external
CrossTrade/Tradovate evidence is unavailable, notification cannot be proven,
or the controlled fill cannot be joined uniquely. Thin M2/M3 data is also
`AMBIGUOUS`, but does not invalidate an already-passed M1 architecture.

**Revert action:** revert the monitoring implementation commit, restore
`dry_run=true`, and supersede this ADR with a corrected architecture. Do not
restore the retired CFD estate.

**Trigger check schedule:** every M1 implementation commit; B7-REFIRE Stage 1
and controlled SIM Stage 2; the first five armed sessions **after M1
RESOLVED**; then the lifecycle review cadence. M3’s first formal review remains
2026-08-08 and may validly return `AMBIGUOUS`.

---

## §5 — Forbidden moves

- **Reinstating `live_journal`, `ecr_rolling.py`, Copygram/DXTrade gates, or
  Alchemy counterfactuals.** They are historical design reference only.
- **Editing the frozen Q-NAS-ECR-1 pre-registration in place for MNQ.** The
  venue and fill mechanism changed; author a fresh Pre-Q.
- **Calling HTTP 200, `sent=True`, or a CrossTrade RECEIVE event a fill.**
  Execution verification requires downstream evidence.
- **Persisting secrets or raw authenticated URLs/payloads in the ledger.**
  Redaction after writing is not an acceptable mitigation.
- **Using aggregate ECR, slippage, or reject rate to trigger lifecycle decay.**
  M2 fidelity corroborates; Call-1 PF and Call-4 own authorization evidence.
- **Fabricating PF, filling missing trades, or counting thin-data
  `AMBIGUOUS` as a breach.**
- **Creating a second tier/state writer or autonomous promotion path.** Reuse
  lifecycle machinery; automation moves authorization down only.
  ⚠ **Superseded in part 2026-08-07** ([`S5 ADR`](2026-08-07-loop-s5-bounded-promotion-lane.md)): the **autonomous promotion path** limb alone gains the bounded sandbox-up exception (budgets not candidates; ceiling-crossings operator-only). A second tier/state writer remains forbidden; demotion stays universal+instant.
- **Expanding Sentinel into a telemetry service.** Governance and execution
  monitoring stay separate.
- **Blocking exit/flat because telemetry is unhealthy.** Flattening is the
  protective direction.
- **Automatically retrying an order after an uncertain send.** The original
  order may already exist; reconciliation precedes any operator retry.
- **Treating intended entry quantity as executed base quantity.** Adds use only
  broker-confirmed fills; rejects and partials must never inherit intended
  state.
- **Silently repairing, truncating, or reordering a corrupt event stream.**
  Armed risk-add stays blocked until the operator resolves the evidence gap.
- **Treating M1 completion as evidence that the strategy edge survives.** M1
  proves the chain is observable, not profitable.
- **Changing Pine, sizing constants, allocations, DD rules, or B1 order
  semantics while implementing monitoring.**
- **Authorizing unattended operation from this ADR.** Manual broker evidence
  is acceptable only because c1 remains attended.

---

## §6 — Consequences and maturity verdict

**Maturity definition:**

| Level | Meaning | Closure state |
|---|---|---|
| M1 | Intent → transport → downstream evidence → fill/flat can be uniquely reconciled | Must be `RESOLVED` before the next armed **session** — i.e. before `dry_run=false` is set (amended 2026-07-31b; was "before the next armed send") |
| M2 | Venue-native execution fidelity measured from real fills | Starts at fill one; may be `AMBIGUOUS` |
| M3 | Venue-native Call-1 baseline/σ plus sufficient pre-registered data; Call-4 separately scoped | Data-dependent; `AMBIGUOUS` is valid |

This ADR closes the **operational** maturity gap at M1. It does not falsely
declare the statistical monitoring gap closed before data exists.

**Positive consequences:**

- B7 gains a machine-readable evidence chain rather than a text-log inference.
- The exact B6 false-positive class becomes mechanically distinguishable.
- Fill evidence can feed fresh fidelity and lifecycle questions without a
  second identity/reconciliation rebuild.
- Fail-safe direction is explicit for both monitoring and orders.

**Negative consequences:**

- M1 adds a write on the hot path and makes its durability a precondition for
  risk-adding orders.
- Until a verified broker API exists, the operator must enter/attach
  CrossTrade and Tradovate evidence.
- M1 requires a real deployed notification sink and durable event I/O rather
  than only test doubles, increasing operational setup.
- M2/M3 maturity remains slow and may stay `AMBIGUOUS` for many sessions.

**Risks:**

- An append-only local volume is not an external durable store; a Fly volume
  loss can still remove evidence. Mitigation: session export/backup is an M1
  runbook requirement.
- Manual evidence can be mistyped. Mitigation: schema validation, immutable
  overlay rows, and order/quantity/flatness cross-checks.
- Threaded/concurrent writes can corrupt a naive JSONL implementation.
  Mitigation: the M1 lock/fsync/startup-validation contract and race tests.
- Monitoring code can accidentally become an order dependency beyond its
  intended fail-safe. Mitigation: explicit exit/flat tests and no automatic
  retry.

**Downstream artifacts required on implementation:**

- `ops/c1_rail/c1_rail_telemetry.py` and tests;
- `ops/c1_rail/c1_rail_http_server.py`, `ops/c1_rail/c1_rail_listener.py`, and config examples;
- read-only reconciliation CLI/module and evidence schema;
- `scripts/validate_c1_monitoring_acceptance.py` plus a machine-readable,
  secret-free `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`;
- `docs/notes/rail_build/RUNBOOK.md` M1 gate and session export procedure;
- `PIPELINES.md` P6 status: venue-native M1 rebuilt, M2/M3 staged;
- c1 GO ADR reverse partial-supersession edge when this ADR is accepted;
- `STATE.md` forward board and `docs/SESSIONS.md`;
- fresh Q-NAS-ECR successor Pre-Q only after M1 and first fill.

---

## §7 — Implementation plan

### Phase 0 — freeze the M1 contract

- Record operator architecture acceptance separately from M1 completion.
  Acceptance flips the ADR to `Accepted`, adds the c1 GO ADR’s matching
  `Superseded-in-part-by` edge, and regenerates the ADR index in one commit.
- Write the versioned event-variant and evidence-overlay schemas.
- Freeze allowed outcomes, event/order identity, secret denylist, append
  lock/fsync/startup-recovery semantics, session export, and fail-safe
  behavior.
- Capture B6 wrong-secret and B7 non-JSON examples as redacted regression
  fixtures.
- Specify an injected operator-notification interface and select a deployed,
  operator-reachable channel. Provider choice/addition receives its own
  dependency and secret-handling review; M1 cannot resolve with a fake sink.

### Phase 1 — structured hot-path events

- Implement the ops-owned append-only writer; do not import lab.
- Emit structured records for authorized ignored payloads, equity failures,
  handler errors, sizing halts/floors, dry runs, and sends.
- Parse valid B1 `signal_type` before equity/state reads so exit/flat always
  bypass risk-add prerequisites.
- Require a writable event path before armed entry/add.
- Preserve best-effort exit/flat and no-retry semantics.
- Add `transport_unknown`; acknowledge uncertain sends without upstream retry,
  block subsequent risk-add, and reconcile before any operator retry.
- Implement the locked/fsynced append and strict startup validation.
- Add schema, redaction, concurrency, crash-tail, tamper, write-failure,
  exit-on-equity-failure, unknown-send, and behavior-parity tests.

### Phase 2 — downstream evidence and reconciliation

- Add the operator-attested CrossTrade/Tradovate overlay schema.
- Build a read-only reconciler with the six fixed verdicts.
- Persist broker-confirmed base fills and flatness as execution state. Move
  open-base tracking out of pre-transport sizing; reject/partial fixtures prove
  adds use confirmed quantity and restart safely.
- Add B6 reject, successful B6 round-trip, quantity mismatch, and missing-flat
  fixtures.
- Empirically test duplicate `order_id` behavior in CrossTrade SIM; treat
  idempotency as unproven unless the evidence is explicit.
- Verify a session export can be copied off the Fly volume without secrets.

### Phase 3 — M1 operator gate

- Run B7-REFIRE Stage 1 at `dry_run=true` on a real strategy signal.
- Run the controlled SIM full-chain and flatness check.
- Exercise deployed notification, transport-unknown, duplicate-order,
  restart/open-position, partial-fill, and exit-during-equity-failure
  procedures.
- Return `RESOLVED`, `FALSIFIED`, or `AMBIGUOUS` under §4.
- Write the secret-free M1 acceptance artifact and validate it mechanically;
  it records fixture hashes, test commit, event IDs, reconcile verdict,
  notification acknowledgement, restart/partial/unknown-send drills, and
  operator sign-off.
- Only `RESOLVED` permits the next c1 `dry_run=false` entry/add send.

### Phase 4 — M2 venue-native fills

- Normalize first armed fills without defining post-hoc thresholds.
- Publish fidelity metrics descriptively.
- Author and freeze the Q-NAS-ECR successor before testing any transfer claim.

### Phase 5 — M3 lifecycle feed

- Pre-register the minimum trade count at the 2026-08-08 review.
- Admit venue-native MYM/MNQ per-leg PF baselines and matching σ panels before
  calling the existing Call-1 harness; the CFD baselines are not substitutes.
- Build the thin adapter from completed venue-native trades to the existing
  Call-1 harness.
- Keep missing/thin data `AMBIGUOUS`.
- Scope Call-4 beta cohesion separately; do not bundle an uncalibrated
  diagnostic into the M1 hot path.

Each phase is a separate commit and review boundary. Phases 4–5 cannot block
the code build but cannot claim maturity before their data gates clear.

---

## §10 — Audit hooks

```bash
# ADR structure and graph
python3 scripts/check_brief.py \
  docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md --type adr
python3 scripts/check_adr_graph.py

# Retired estate must stay absent
test ! -e ops/live_journal
rg -n 'live_journal|ecr_rolling|Copygram|DXTrade' \
  ops/c1_rail_*.py ops/c1_rail/crosstrade_payload.py
# Expected: empty.

# Structured monitoring exists and is configured
test -f ops/c1_rail/c1_rail_telemetry.py
rg -n 'events_log_path|schema_version|event_id|order_id|transport_unknown' \
  ops/c1_rail/c1_rail_telemetry.py ops/c1_rail/c1_rail_http_server.py deploy/c1_rail/

# Monitoring does not become a second sizing/lifecycle implementation
rg -n 'DD_TRIGGER|DD_SCALE|BASE_RISK|TIER_MULTIPLIER|decay_breach' \
  ops/c1_rail/c1_rail_telemetry.py
# Expected: empty.

# Targeted M1 tests
python3 -m pytest \
  tests/ops/test_c1_rail_telemetry.py \
  tests/ops/test_c1_rail_listener.py \
  tests/ops/test_c1_rail_http_server.py \
  tests/ops/test_crosstrade_payload.py \
  tests/ops/test_c1_sizing_host_reference.py -q
# The telemetry/reconcile tests must assert: denylisted secrets absent;
# HTTP 200 alone unverified; unknown-send no-retry; exit on equity failure;
# rejected/partial base blocks or correctly sizes add; concurrent/crash-safe log.

# Lifecycle thin-data contract remains
python3 -m pytest tests/test_lifecycle.py tests/test_lifecycle_call1.py -q

# Machine-validated operator evidence (not grep/self-attestation)
python3 scripts/validate_c1_monitoring_acceptance.py \
  docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
# Expected: M1 RESOLVED, fixture/event hashes valid, CHAIN_OK, notification
# acknowledged, all required drills present, zero secret-valued fields.

# Repository gates
python3 scripts/check_boundaries.py
python3 scripts/check_path_liveness.py
python3 scripts/check_root_doc_liveness.py
make check
```

Operator M1 acceptance evidence:

```text
1. Real strategy signal at dry_run=true → structured event, expected qty.
2. Controlled SIM entry → CrossTrade RECEIVE/VALIDATE/EXECUTE Success.
3. Tradovate Filled quantity == sizing decision quantity.
4. Exit/flat → Tradovate no open position.
5. Session event/evidence export validates and reconciler returns CHAIN_OK.
```

---

## Verification

```bash
python3 scripts/check_brief.py \
  docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md --type adr
python3 scripts/check_adr_graph.py
python3 scripts/check_path_liveness.py
python3 scripts/check_root_doc_liveness.py
python3 scripts/check_boundaries.py

# Rule-0 anchors
git log -1 --format='%h %ci' -- ops/c1_rail/c1_rail_listener.py
git log -1 --format='%h %ci' -- ops/c1_rail/crosstrade_payload.py
git log -1 --format='%h %ci' -- ops/c1_rail/c1_rail_http_server.py
git log -1 --format='%h %ci' -- docs/notes/rail_build/RUNBOOK.md
git log -1 --format='%h %ci' -- docs/adr/2026-07-11-ops-cfd-estate-retirement.md

# Draft-only scope
git diff --name-only origin/main...HEAD
```

---

## Addendum 2026-07-31 — deletion of §4 item 5 **proposed and DECLINED**. Item 5 stands.

**Status: `Accepted` (as a decline).** Operator ruling 2026-07-31: *"amend the draft to decline."*
The proposal was to delete §4 item 5; it is **declined**. **§4 is unchanged** — item 5 stands as
written, `dry_run_strategy_signal_event_id` remains in `RESOLVED_REQUIRED`, and M1 remains
`CODE_LANDED`. This addendum relaxes nothing; it is recorded because the reasoning that produced
and then defeated the proposal is reusable, and because the proposal's central premise was wrong
in a way worth keeping on the record.

### The premise was wrong — and this correction is the reason for the decline

The draft asserted item 5 is **circular**: that it wants a `dry_run` event while §6 makes
`RESOLVED` the gate on arming, so an armed session discharging it would let the gate be satisfied
by the act it authorizes.

**That is not a property of the item.** B7-REFIRE **Stage 1 is the unarmed stage.** A real strategy
signal arriving with `dry_run=true` produces a structured dry-run event and discharges item 5
cleanly, with no arming and no circularity. What happened on 07-31 is that Stage 1 was *collapsed
into Stage 2 and armed*, skipping the dry run — a session-level choice, not a defect in the gate.
The circularity only bites if one insists on discharging item 5 from an armed session, which is
precisely what item 5 exists to prevent.

Item 5 is therefore **satisfiable as written**. The real cost of keeping it is operator-hours, not
impossibility.

### What item 5 uniquely certifies

It is the **only** acceptance item requiring a real TradingView strategy signal. Every other item
is a planted synthetic failure (1–4, 8, 9) or a hand-POSTed canned payload (item 6's SIM
`CHAIN_OK`, item 7's B6 replay). No strategy-signal-originated decision has ever occurred on this
rail.

That distinction is load-bearing, because every defect that has actually bitten this rail was a
real-signal-only discovery: the 07-21 informational-`alert()` shadowing of the JSON payloads; the
07-24→07-28 upstream TV→rail break that went undetected; and the 07-28 §1c finding that
`parsed.close` was `28,051.50` against a confirmed close of `28,048.50`. None were reachable from
canned payloads.

### The engineering read survives, but does not cover the exposure

The 07-31 sizing analysis is **correct and retained** — verified against
[`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py): `reserve_cap =
⌊cap_alloc/(1+pyr%)⌋` gives MYM `⌊69/8.5⌋ = 8` and MNQ `⌊11/11⌋ = 1`; `qty_out =
min(qty_base_raw, reserve_cap)`; `submit = qty_out > 0`. A bad mid-bar ATR can only **under**-size
an entry, never over-size it, and a floored `qty_out=0` returns before the sender.

But that bounds **size**, not **signal identity**. The 07-28 finding was that the rail acted on a
price that was never the bar's close — which changes *which trade is taken*, not how large it is.
`reserve_cap` is silent on that, and item 5 is the only gate positioned to catch it before money
is live. This is where the deletion argument fails.

### Cost of the decline, stated so it is chosen knowingly

MYM trades Tue/Fri at a ~30.7% entry rate — about 0.6 entry-days per week, so roughly 3.3 attended
sessions in expectation (~1.5–2 weeks), with a ~23% chance of nothing after four more. MNQ does not
rescue it: `reserve_cap` is 1 there and it floored to 0 at a 126.75 stop on 07-28. Three of the
four prior misses (post-window, alert shadowing, qty 0) were fixable defects **since fixed**, so
only 07-31 was a genuine base-rate miss and the forward odds are better than an 0-for-4 record
suggests. Every later item — Stage 2, first live fill, and the Q-NAS-ECR successor / lifecycle
Call-1 / ORB decay re-scope chain behind it — waits that long.

### What follows operationally

1. **Run Stage 1 unarmed.** Do not collapse it into Stage 2 again; that is what made 07-31
   undischargeable.
2. **Redefinition stays forbidden** — the one part of the draft that survives intact. Item 5 must
   never be re-read to accept live evidence, and `--allow-live` must never write into
   `dry_run_strategy_signal_event_id`; the field would then assert something untrue. An acceptance
   artifact that lies is worse than one missing an item.
3. **RATIFIED 2026-08-02** (operator ruling: *"rule the 4-session trigger"*; proposed 2026-07-31,
   unruled until now): a review trigger of **4 further attended Stage-1 sessions** without a
   discharge, at which point this decline is revisited with the base rate as measured rather than
   modelled.

   **Counting convention — DERIVED, not chosen.** A session counts whether or not a strategy signal
   arrived. This is not a preference: the proposal's own cost model says *"~23% chance of nothing
   after four more"*, and at the stated ~30.7% MYM entry rate that figure reproduces only as
   `(1 − 0.307)^4 = 23.06%` — i.e. four **attended** sessions, not four signal-bearing ones. Reading
   it the other way (count only sessions where a signal arrived) would measure a different quantity
   entirely — defect rate rather than base rate — and would leave the trigger effectively
   unreachable, since the 07-31 miss was an absent signal, not a failed one.

   **What counts:** the rail attended and live through the MYM entry window with the §0
   receiver-side pre-flight passed — a session that *could* have discharged item 5. A session that
   never reached the window (2026-07-20's post-window arrival) does **not** count; it was not a draw
   from the distribution being measured.

   **Reachability check** (per the standing gate-reachability discipline — a trigger that cannot
   fire is not a trigger): fires with probability **23.1%** after 4 sessions, ~2 calendar weeks at
   MYM's Tue/Fri schedule. Sessions 1–4 are **2026-08-04, 08-07, 08-11, 08-14**; the review fires
   after **2026-08-14** if item 5 is still undischarged. It is deliberately a tail trigger — firing
   is itself evidence the ~30.7% model is wrong, which is the thing the review exists to re-examine.

   **What the review does:** compares measured vs modelled entry rate; classifies each miss as
   base-rate (no signal arrived) or defect (signal arrived and failed to discharge — a materially
   different finding that would point at the rail, not the odds); and re-decides the item-5 deletion
   on that evidence. **What it does not do:** it does not auto-delete item 5, auto-relax the gate, or
   authorize anything. The decline stands unless the operator changes it; this schedules a look, not
   an outcome.

#### Addendum 2026-08-04 — 4-session review trigger **SUSPENDED** (not discharged)

The 2026-08-02 reachability certification ("a trigger that cannot fire is not a trigger") is now false **in both directions**: no qualifying session can be drawn (counting convention requires the rail attended and live through the MYM entry window with a deployed emitter), yet the date limb reaches **2026-08-14** regardless and would "fire" on zero draws. **SUSPENDED**, not discharged. The **23.1%** figure no longer describes a sampled distribution. Session 1 (2026-08-04) never ran and cannot (both Striker legs withdrawn — [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md)). **Do not read an elapsed 2026-08-14 as a fired review.** Re-arms against whatever fork **F3** registers. Trigger text, counting convention, and the item-5 deletion decline above remain **byte-unchanged**.

### What this addendum does not do

It changes no acceptance item, authorizes no armed send, and does not touch `operator_signoff`,
sizing, Pine, allocations, or DD rules. The §2b clean mid-bar re-measurement remains owed
independently — an execution-quality question, not an M1 item.

---

## Addendum 2026-07-31b — the two knowing deviations past the M1 gate, recorded; and the gate's trigger is proposed to move from "send" to "arm"

**Status: `Accepted` — operator ratified 2026-07-31 ("ratify the trigger change").** This is the
amendment the 07-28 and 07-31 sessions each recorded as owed ("with the amendment to be written
after the fact").

**The ratified change is now IN FORCE and applied at four sites in this ADR** — §Status, the §2 M1
heading, §2 §Effective, and the §6 maturity table: **M1 `RESOLVED` is required before the next armed
SESSION, i.e. `dry_run=false` may not be set while M1 is not `RESOLVED`.** The prior wording
("before the next armed *send*") is preserved inline at each site so the change is diffable in
place.

**What ratification did NOT do.** It does **not** ratify either deviation retroactively — 07-28 and
07-31 remain recorded as knowing deviations, not as precedent. It does not resolve M1 (still
`CODE_LANDED`), does not touch `operator_signoff`, does not reopen item 5, and authorizes no armed
session. Under the tightened trigger the next arm is **more** gated than before, not less.

### §0 — Rule 0 reads

| Source | Anchor | Read for |
|---|---|---|
| This ADR §Status, §4 M1 heading, §4 items 1–11 | `7160207` 2026-07-31 18:10 | the exact gate text and what it takes as its object |
| `docs/notes/rail_build/RUNBOOK.md` §B7 arming log, entries 2026-07-28 and 2026-07-31 | `5543a20` 2026-07-31 16:18 — the commit that **wrote** those entries; verified not modified since (the later `6a31a26` touched only §Standing ToS, 0 arming-log lines) | what was armed, when, on what rationale, and what arrived |
| `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` | `21cd717` 2026-07-31 16:52 | verdict state across both sessions (`CODE_LANDED` throughout) |
| Addendum 2026-07-31 (this file, above) | same as ADR | the standing decline; this addendum must not contradict it |

### What happened — both sessions, factually

**2026-07-28.** Operator elected to override the planned Stage-1 `dry_run=true` step and arm live,
on the stated rationale *"we have already proven that the rail works."* Pre-flight 9/9 clear. A real
MYM entry fired at 11:28 ET and **routed nothing** — the body arrived as plain text, because
TradingView snapshots a script at *alert-creation* time and the alerts predated the 07-21/22 fixes.
After the alerts were recreated, a real MNQ `alert()` arrived as `b1_json` and was sized:
`r_eff 0.00185`, `per_contract 253.50`, **`qty_out 0`** — the documented granularity floor.
`dry_run_strategy_signal_event_id` was **deliberately left unset**, correctly: populating it from a
floored-to-zero decision would advance the gate on evidence the gate exists to exclude.

**2026-07-31.** Operator elected to collapse B7-REFIRE Stage 1 into Stage 2 and arm before M1
`RESOLVED` — recorded in the RUNBOOK as *"a knowing deviation … with the amendment to be written
after the fact."* The engineering case was that `reserve_cap = ⌊69/8.5⌋ = 8` hard-caps a base entry
regardless of the incoming stop, so the dry-run step's marginal *safety* value is near zero. Armed
12:57:28 UTC for 4 h. **The ledger never moved** — `seq 25` at open, `seq 25` at close, zero arrivals
in four hours, consistent with MYM's ~30.7% entry rate. The session's own finding was the subsequent
`armed_until` self-brick, which is an availability defect and is owned by the RUNBOOK, not by M1.

M1 was `CODE_LANDED` throughout both.

### The finding: the gate stopped neither session — other things did

**Neither session produced an armed send.** On the gate's literal text that is compliance: §4 M1 is
*"required before the next armed send"*, and no send occurred. That reading is too kind to what
happened.

What actually prevented a send was, on 07-28, **an arithmetic floor** (`qty_out 0`, a property of the
granularity law at a 126.75 stop) and, on 07-31, **the absence of a signal** (a property of MYM's
base rate). Both are outcomes of the market and the sizing law. Neither is the gate, and neither was
under operator control at arming time. On 07-28 in particular the rail processed a live strategy
signal while armed, and the distance between that session and a live send was one stop-width.

So the honest statement is not *"the gate was breached twice"* and not *"the gate held twice."* It is:
**twice the rail was placed in a state where the next qualifying signal would have sent, with M1
unresolved, and on both occasions the reason nothing sent was chance rather than control.**

### The definitional gap this exposes

The gate's object is the **send**. The send is market-triggered. The operator's controllable act is
the **arm**. A gate whose trigger is not the operator's own action cannot be complied with
prospectively — it can only be evaluated afterwards, which is why both sessions could be simultaneously
*"a knowing deviation"* in the operator's own words and *not a literal breach* on the text.

Note that both operators-of-record already read the gate as covering arming: each session logged
itself as a deviation. The text is what lagged.

### The change (the only substantive one) — **RATIFIED AND APPLIED 2026-07-31**

**M1's trigger moves from "before the next armed send" to "before the next armed session."**
Concretely: `dry_run=false` may not be set while M1 is not `RESOLVED`.

Cost of this tightening: **zero new operational burden.** B7-REFIRE Stage 1 is unarmed by definition
(Addendum 2026-07-31), so the only path M1 currently requires is already compliant with the tighter
trigger. This formalizes what both session records already assumed; it does not add a step.

### Forbidden moves

1. **Do not ratify either deviation retroactively.** This was the tempting shape — both sessions were
   attended, careful, produced real findings, and cost nothing. Ratifying them converts the gate into
   advice, and the next deviation inherits the precedent rather than the reasoning.
2. **Do not treat "no send occurred" as evidence the gate worked.** It is evidence that the
   granularity floor and MYM's base rate worked. Crediting the gate for their behaviour is how a
   control decays into a formality.
3. **Do not weaken item 5 or `RESOLVED_REQUIRED` here.** Addendum 2026-07-31 declined that and this
   addendum does not reopen it. Redefinition stays forbidden; `--allow-live` must never write
   `dry_run_strategy_signal_event_id`.
4. **Do not fold the 07-31 self-brick into M1.** It is a host-availability defect with its own
   operating rule (disarm *before* `armed_until` lapses) and its own owner (RUNBOOK §B7). M1 is about
   observability of the execution chain; merging them would make both harder to close.

### Falsifier

**If a third armed session occurs while M1 is not `RESOLVED`**, then the gate — under either
trigger, and regardless of whether that session sends — is not functioning as a control on this
operation, and the correct response is to stop amending it and instead escalate to a **structural**
enforcement: make `ops/c1_rail/c1_rail_arm.py --arm` refuse unless `M1_MONITORING_ACCEPTANCE.json` reads
`status: "RESOLVED"`. That is a small extension, not a new mechanism — the tool **already** carries
an M1-gated refusal (`ops/c1_rail/c1_rail_arm.py:78`, *"refusing to arm: events_log_path missing (M1
monitoring gate)"*) and already parses JSON config (`:123`). What it does **not** do today is read
the acceptance artifact at all; hook 4 below asserts exactly that, so the hook flips from empty to
non-empty the day the escalation is built. **Otherwise**, if the next armed session follows an M1
`RESOLVED` verdict, the tightened trigger is doing its job and no further instrument is needed.

The mechanical form of the falsifier: a new entry in the RUNBOOK §B7 arming log dated after this
addendum whose text records `DRY_RUN=false`, while `M1_MONITORING_ACCEPTANCE.json` still carries
`"status": "CODE_LANDED"`.

### What this addendum does not do

It changes no acceptance item, does not touch `operator_signoff`, and authorizes no armed send. It
does not modify sizing, Pine, allocations, `dd_protection`, lifecycle, or the order payload. It does
not resolve M1. The §2b clean mid-bar re-measurement remains owed independently. Until an operator
ruling lands, the gate text stands as originally written.

### §10 — Audit hooks

All four executed 2026-07-31 against the storage form, not the author's mental form (Trap M-AHF);
expected outputs recorded so a later reader can tell drift from noise.

```
# 1. The ratified trigger is actually applied — not merely announced in this addendum.
#    Assert on the LIVE-ASSERTION FORM, not on a total count: counting "next armed send"
#    conflates live gate statements with quotes and history, and the tally moves whenever
#    anyone adds a sentence. (Authoring note: the first version of this hook predicted a
#    count of 8, the real figure was 11, and the discrepancy hid TWO surviving live
#    assertions at §1 item 9 and §3. Count-based hooks fail open. This form does not.)
grep -rn "next-send gate" docs/adr/ CLAUDE.md | grep -v 'grep -v'
# Expected: ZERO hits. (The bare grep self-matches this very line inside the fence; the
# -v filter drops it. Any SURVIVING hit is a live statement of the retired trigger. The
# old wording is deliberately absent from prose here so this stays a clean zero-test —
# quoting a retired term in prose is what made the first draft of this hook false-positive.)

# 1b. The four normative sites carry the new trigger.
grep -c "armed SESSION\|armed \*\*session\*\*\|next-\*\*arm\*\* gate\|next \*\*arm\*\*" docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md
# Expected: >= 4 (§Status, §2 M1 heading, §2 Effective, §6 maturity table).

# 2. FALSIFIER — an armed session logged while acceptance is still CODE_LANDED.
#    NOTE the field is "status"; "reconcile_verdict" is a DIFFERENT field (the CHAIN_OK result).
grep -n "DRY_RUN=false" docs/notes/rail_build/RUNBOOK.md
grep -n '"status"' docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
# Expected 2026-07-31, executed: **5** hits for `DRY_RUN=false` and `"status": "CODE_LANDED"`
# at line 3. Falsifier fires if a NEW dated arming entry pushes that count above 5 while
# status is still CODE_LANDED. (Do NOT widen this to `DRY_RUN=false\|dry_run=False` — that
# form returns 8 by also matching host-verified disarm confirmations, and the two counts are
# not interchangeable.)

# 3. The declined item-5 deletion stays declined — this addendum must not have reopened it
grep -n "dry_run_strategy_signal_event_id" docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
# Expected: 2 hits (RESOLVED_REQUIRED membership + the field itself), unset.
# CORRECTED 2026-08-08: actual is 3. A third mention was added to the artifact's own notes; the
# item-5 deletion is still DECLINED and the field is still unset, so the guarded property holds.
# Re-baseline to 3, or re-scope the grep to the RESOLVED_REQUIRED block — do not read 3 as a breach.

# 4. Structural escalation tripwire: does the arm tool read the acceptance artifact?
grep -n "M1_MONITORING_ACCEPTANCE" ops/c1_rail/c1_rail_arm.py
# Expected TODAY: empty — the tool gates on events_log_path (:78) but never on M1 status.
# This hook flips to non-empty the day the §Falsifier escalation is built. Empty is the
# current correct state, NOT a passing gate.
# INVERTED 2026-08-08: actual is NON-empty (c1_rail_arm.py:58) — the escalation WAS built
# (PR #601, m1_acceptance_reason). Non-empty is now the CORRECT state and empty would be the
# regression. Read this hook inverted until the comment above is rewritten.
# ⚠ Scope caveat, measured: the interlock reads ONLY the artifact's `status` field. A 24-byte
# {"status":"RESOLVED"} clears it while scripts/validate_c1_monitoring_acceptance.py FAILs the
# same bytes with 19 errors, and the arm path never invokes that validator. Non-empty here means
# "a gate exists", NOT "the artifact was validated".
```

---

## Addendum 2026-08-07 — item-5 signal-origin definition superseded in part (S2)

**Status: `Accepted` (express supersession).** [S2 ADR](2026-08-07-loop-s2-signal-host-fork.md) **expressly** supersedes §4 item 5’s **TradingView-only** signal-origin limb. Forward discharge: a real strategy signal from the **ruled host** (Python daemon B1 POST with expected non-zero sizing at `dry_run=true`). Historical body above (incl. Addendum 2026-07-31 “real TradingView strategy signal” / “Redefinition stays forbidden”) is **frozen** — the bar was on *silent* redefinition; this addendum records the express edge. Item 5 remains **owed**; M1 stays `CODE_LANDED`; no event ids fabricated; deletion decline stands.

---

## Addendum 2026-08-24 — test strategy licensed for item 5; dated 08-24

**Does not amend** item 5’s limbs (real signal, expected non-zero sizing, Stage-1 `dry_run=true`, no silent redefinition, `--allow-live` must not write `dry_run_strategy_signal_event_id`). **Does not** claim M1 `RESOLVED`. **Does not** arm. **$0 / K=0.**

**Rule 0 (this addendum):** this file Addendum 2026-08-07 @ `027a729` — discharge is a ruled-host B1 POST at expected non-zero dry-run sizing. [S2](2026-08-07-loop-s2-signal-host-fork.md) §4.2 @ `027a729` — canned / live-armed / zero-qty floors stay DEAD-list. [GO ADR](2026-07-17-c1-rail-build-account-registration-go.md) de-scope addendum @ `acc4f41` — “Deploying any qualifying strategy makes it dischargeable again.” `ops/c1_signal_daemon/strategy_protocol.py` `NullStrategy` @ `027a729` — default never emits. Cheap falsifier: `rg -n "any qualifying strategy" docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` hits; `NullStrategy.on_bar` returns `None`.

**Operator ruling 2026-08-24:** item 5 may be discharged with a **test strategy** on the ruled host — `Strategy.on_bar` → daemon B1 POST → structured dry-run decision at expected non-zero sizing. Dated on the [`STATE.md`](../../STATE.md) 2026-08-24 board next to disaster-stop Phase 0a. Queue `#2` no longer waits on `#1` for this limb ([Survive-bound addendum](2026-08-09-survive-bound-is-the-queue-cap.md#addendum-2026-08-24--m1-item-5-no-longer-waits-on-queue-1)).

**Qualifying instrument:** evaluate-hook strategy, not a canned hand-POST (item 6 class), not `NullStrategy`, not a fabricated event id, not a withdrawn Striker redeploy. Any required `LEG_MAP` extension is part of the attended 08-24 packet, not this commit.

**Still owed after a recorded event id:** `operator_signoff`. `emit_enabled=true` is the attended emit step the daemon already refuses without a strategy GO — this addendum *is* that GO for a test strategy only. Q-M1WIRE-1 A2/A5 gaps do not block `RESOLVED`. `dry_run=false` stays forbidden.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | **Test strategy licensed** as item-5 qualifying emit; dated 08-24. Limbs + deletion decline + no-arm stand; M1 stays `CODE_LANDED` until the attended session records the event id + `operator_signoff` | Joshua (ruling) · Cursor (recorder) |
| 2026-08-07 | **§5 autonomous-promotion limb superseded in part** by S5 ADR (bounded sandbox lane). Header `Superseded-in-part-by` extended; no second tier/state writer; arm-gate + unattended bar stand | Cursor (drafter) · Joshua (plan GO) |
| 2026-08-07 | **Item-5 signal-origin superseded in part** by S2 ADR (Python-native ruled host). Header `Superseded-in-part-by` + this addendum; historical body frozen; item 5 still owed; `status` unchanged | Cursor (drafter) · Joshua (plan GO) |
| 2026-08-02 | **4-session review trigger RATIFIED** (Addendum 2026-07-31 item 3; operator ruling *"rule the 4-session trigger"*). Counting convention **derived from the proposal's own model, not chosen**: a session counts whether or not a signal arrived, because the stated *"~23% chance of nothing after four more"* reproduces only as `(1−0.307)^4 = 23.06%` — attended sessions, not signal-bearing ones. A session that never reached the entry window does not count. Reachability verified: fires at **23.1%** after 4 sessions ≈ 2 weeks; sessions 1–4 are **08-04 / 08-07 / 08-11 / 08-14**, review after **2026-08-14**. Schedules a look, **not** an outcome — no auto-delete of item 5, no gate relaxation, decline stands unless the operator changes it | Claude (specify + reachability) · Joshua (ruling) |
| 2026-07-31 | Addendum 2026-07-31b **RATIFIED** — operator ruling *"ratify the trigger change"*. **M1's trigger moves from "before the next armed send" to "before the next armed session"** (`dry_run=false` may not be set while M1 is not `RESOLVED`), **applied at four normative sites**: §Status, §2 M1 heading, §2 Effective, §6 maturity table. The 07-28 and 07-31 deviations are **recorded, NOT ratified retroactively**. Finding behind it: neither session was stopped by the gate — an arithmetic floor (`qty_out 0`) and an absent signal stopped them. Zero new operational cost: Stage 1 is unarmed by definition, so the only path M1 requires already complies. M1 remains `CODE_LANDED` | Claude (draft + apply) · Joshua (ruling) |
| 2026-07-31 | Addendum 2026-07-31 — deletion of §4 item 5 proposed, then **DECLINED** by operator ruling. §4 unchanged; item 5 stands. The draft's "circular" premise is **corrected on the record**: Stage 1 is the unarmed stage, so item 5 is satisfiable as written. Operative: run Stage 1 unarmed; redefinition stays forbidden | Claude (draft + correction) · Joshua (ruling) |
| 2026-07-23 | Operator ratification → Status `Accepted`; reverse partial-supersession edge on c1 GO ADR; M1 implementation authorized (M1 `RESOLVED` still owed before next armed send) | Joshua (decision) · Cursor (apply) |
| 2026-07-22 | Initial `Proposed` ADR; venue-native M1 gate plus staged M2/M3 monitoring maturity | Joshua + Cursor |
