# ADR 2026-07-22 — Adopt a venue-native c1 monitoring spine and staged maturity gates

**Superseded-in-part-by:** `2026-09-14-a7-attended-agent-capture.md` — controlled-input actor and candle transcript scope only

> **Scoped amendment, 2026-09-14:** [Attended agent capture](2026-09-14-a7-attended-agent-capture.md) changes the controlled-input actor/provenance for the approved agent variant. Item 5's origin, sizing, dry-run and signoff requirements stand; the source is not a production-feed qualification. Historical manual evidence is unchanged; M1 acceptance was set `RESOLVED` on 2026-09-14 from the event A7 attempt 4 captured under this variant (A8).

**D-S-A domain:** system
**Status:** `Accepted` — operator ratified 2026-07-23 ("flip ADR to ratified and proceed to close the monitoring gap"); **M1 `RESOLVED` 2026-09-14** ([acceptance](../notes/rail_build/M1_MONITORING_ACCEPTANCE.json); [A8](../notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md#a8--signed-acceptance-deployed-re-bake-verified-2026-09-14)), limited by Addendum 2026-10-01 (no legacy-leg arm while #571 is parked); architecture policy in force. **AMENDED 2026-07-31, operator-ratified (Addendum 2026-07-31b): the M1 gate's trigger is the ARM, not the send** — `dry_run=false` may not be set while M1 is not `RESOLVED`. Acceptance (2026-07-23) authorizes M1 implementation; it does **not** by itself claim M1 is `RESOLVED` or permit an armed session (§4 M1 verdict is the next-**arm** gate).
**Decision date:** 2026-07-22
**Supersedes:** `2026-07-17-c1-rail-build-account-registration-go.md` in part — the next armed session/B7-REFIRE Stage 2 gains the M1 monitoring gate defined here (trigger amended from "send" to "session" 2026-07-31b)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-loop-s2-signal-host-fork.md` — §4 item 5 **signal-origin definition only** (TradingView-only → ruled Python-native host). Item 5 itself, expected sizing, Stage-1 `dry_run`, deletion decline, and the bar on **silent** redefinition stand.
**Superseded-in-part-by:** `2026-08-07-loop-s5-bounded-promotion-lane.md` — §5 forbidden move *“Creating a second tier/state writer or autonomous promotion path”* **autonomous promotion path limb only** (bounded sandbox lane). No second tier/state writer; arm-gate, reflex layer, and unattended bar **stand**.
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0's non-RUNBOOK Rule-0 bullets and cheap-falsifier transcript, the §7 phase list, §10's duplicated operator-evidence list, and the narrative parts of Addenda 2026-07-31 and 2026-07-31b condensed; no clause amended, and every RUNBOOK site the 2026-09-12 intercept lists is unchanged. Pre-trim text at blob `a164a94581e2b35813100893628c11665f6233c7` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`): [this file at `4121e84c`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md).

**Related:** `2026-07-11-ops-cfd-estate-retirement.md` (venue-native rebuild
rule); `2026-07-10-strategies-never-locked-lifecycle-governance.md`;
`docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md` (parked historical test);
`docs/briefs/closures/Q-DECAY-1-closure-scope-split.md`; proposed
`2026-07-22-challenge-era-substrate-retirement.md`;
`2026-08-07-loop-s2-signal-host-fork.md` (express item-5 origin supersession).

**Pointer re-home 2026-09-12 (TB-O1; reader-intercept, no clause amended):** every
`docs/notes/rail_build/RUNBOOK.md` reference below — the §0 anchor, the §6 downstream list, the
§Verification command, and Addendum 2026-07-31b's §0 table, §Falsifier and §10 hook 2 — names a
private file that is **not on the public tree**. The public operating procedure is
[`ARMING_PROCEDURE.md`](../notes/rail_build/ARMING_PROCEDURE.md); the private runbook is retrieved
per its §2 (archive pin `5d47b4dc…`, or the primary checkout's ignored private root). Hooks that grep
the old path run against that private copy. Body text below is byte-unedited; see Addendum
2026-09-12.

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
- `docs/notes/rail_build/RUNBOOK.md` — anchor `d9e8f2a` (2026-07-21).
  B6 proved synthetic sizing and controlled SIM fills. It also records two
  monitoring-relevant incidents: the rail reported HTTP 200 while CrossTrade
  failed validation on a wrong secret, and B7 delivered non-JSON informational
  alerts instead of the B1 JSON order payload. B7-REFIRE still requires a
  real strategy signal through the complete chain.
- Other anchors read at authoring — `ops/c1_rail/c1_rail_http_server.py`, `ops/c1_rail/c1_sizing_host_reference.py`, `core/lifecycle.py`, `lab/discovery/lifecycle_call1/evaluate.py`, the c1 GO ADR, the estate-retirement ADR, the frozen Q-NAS-ECR-1 pre-registration, the Q-DECAY-1 closure, `docs/methodology/strategy_lifecycle.md` and `PIPELINES.md` (anchors 2026-07-10…07-21) — are in the pinned prior version (header Revision line).

**Cheap falsifier, run parent-side before authoring** (transcript in the pinned prior version): `RailAction` carried only `decision, sent, dry_run, payload_text, http_status`, `send_to_crosstrade` returned a bare HTTP status, and no ops telemetry module existed. The rail could prove that it computed and attempted transport, but could not represent downstream acceptance, fill truth, or a durable event identity; the B6 false-positive HTTP-200 incident was therefore architectural, not merely a missing dashboard.

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

Phases 0–3 — freeze the M1 contract (event variants, overlay schema, outcomes, identity, secret denylist, locked/fsynced append and startup validation, session export, and a deployed operator-reachable notification channel whose provider gets its own dependency and secret-handling review; M1 cannot resolve with a fake sink), structured hot-path events, downstream evidence and reconciliation, and the operator gate — were delivered against §2 and §4: M1 was set `RESOLVED` 2026-09-14 (acceptance JSON; A8), limited by Addendum 2026-10-01. Phases 4–5 follow §2 M2/M3: normalize first armed fills without post-hoc thresholds and freeze any successor thresholds before M2 results are read; admit venue-native per-leg PF baselines and matching σ panels and pre-register the minimum trade count before calling the Call-1 harness; keep missing/thin data `AMBIGUOUS`; scope Call-4 separately. Each phase is a separate commit and review boundary; Phases 4–5 cannot claim maturity before their data gates clear. The full phase list is in the pinned prior version.

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
  ops/c1_rail/c1_rail_listener.py ops/c1_rail/c1_rail_http_server.py ops/c1_rail/crosstrade_payload.py
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

The draft called item 5 circular. It is not: B7-REFIRE **Stage 1 is the unarmed stage**, so a real strategy signal arriving with `dry_run=true` discharges item 5 with no arming and no circularity; on 07-31 Stage 1 had been *collapsed into Stage 2 and armed* — a session-level choice, not a defect in the gate. Item 5 is therefore **satisfiable as written**; the cost of keeping it was operator-hours, not impossibility.

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

The 07-31 sizing analysis is **correct and retained**: `reserve_cap = ⌊cap_alloc/(1+pyr%)⌋`, `qty_out = min(qty_base_raw, reserve_cap)`, `submit = qty_out > 0`. A bad mid-bar ATR can only **under**-size an entry, never over-size it, and a floored `qty_out=0` returns before the sender.

But that bounds **size**, not **signal identity**. The 07-28 finding was that the rail acted on a
price that was never the bar's close — which changes *which trade is taken*, not how large it is.
`reserve_cap` is silent on that, and item 5 is the only gate positioned to catch it before money
is live. This is where the deletion argument fails.

### What follows operationally

1. **Run Stage 1 unarmed.** Do not collapse it into Stage 2 again; that is what made 07-31
   undischargeable.
2. **Redefinition stays forbidden** — the one part of the draft that survives intact. Item 5 must
   never be re-read to accept live evidence, and `--allow-live` must never write into
   `dry_run_strategy_signal_event_id`; the field would then assert something untrue. An acceptance
   artifact that lies is worse than one missing an item.
3. **4-session review trigger — discharged.** Ratified 2026-08-02 (a review after 4 further attended Stage-1 sessions without a discharge; sessions 08-04/08-07/08-11/08-14) and **suspended** 2026-08-04, when the Striker withdrawal left no qualifying session to draw. Its object — re-deciding the item-5 deletion while item 5 stayed undischarged — lapsed when item 5 was discharged on 2026-09-14 (acceptance `dry_run_strategy_signal_event_id`; A8). **Do not read the elapsed 2026-08-14 as a fired review.** The counting convention, reachability check and suspension text are in the pinned prior version.

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

On **2026-07-28** the operator armed live over the planned Stage-1 `dry_run=true` step (pre-flight 9/9 clear). A real MYM entry routed nothing — the body arrived as plain text from alerts that predated the 07-21/22 fixes — and after the alerts were recreated a real MNQ `alert()` arrived as `b1_json` and sized to **`qty_out 0`** (the granularity floor), so `dry_run_strategy_signal_event_id` was deliberately left unset. On **2026-07-31** the operator collapsed B7-REFIRE Stage 1 into Stage 2 and armed before M1 `RESOLVED` — recorded as *"a knowing deviation … with the amendment to be written after the fact"* — for 4 h with zero arrivals; that session's own finding, the `armed_until` self-brick, is an availability defect owned by the RUNBOOK, not by M1. M1 was `CODE_LANDED` throughout both. The full narrative is in the pinned prior version.

### The finding, and the definitional gap it exposes

Neither session produced an armed send, but the gate stopped neither: an arithmetic floor (07-28) and an absent signal (07-31) did — outcomes of the market and the sizing law, not under operator control at arming time. Twice the rail was placed in a state where the next qualifying signal would have sent with M1 unresolved, and chance rather than control kept it from sending. The gate's object was the market-triggered **send**; the operator's controllable act is the **arm**, so the gate could only be evaluated afterwards, never complied with prospectively. Both session records already read the gate as covering arming; the text lagged.

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

**Disposition (2026-10-15, additive; the falsifier text above is unchanged):** the structural escalation it names was built — `ops/c1_rail/c1_rail_arm.py` `m1_acceptance_reason` refuses `--arm` unless `scripts/validate_c1_monitoring_acceptance.py` passes with `require_resolved=True` (hook 4 below) — and M1 was set `RESOLVED` 2026-09-14. Arming with an unresolved artifact is possible only through `--acknowledge-m1-unresolved`, against a structurally valid artifact, and writes an `arming_deviation` record citing this addendum.

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
# ⚠ CORRECTED 2026-10-15: the scope caveat first recorded here (status-field-only read; validator
# not called) no longer holds. m1_acceptance_reason runs validate_c1_monitoring_acceptance with
# require_resolved=True, so a 24-byte {"status":"RESOLVED"} fails; a complete forged RESOLVED
# artifact still passes (AGENTS.md §Live-execution posture). Non-empty = a validating gate exists.
```

---

## Addendum 2026-08-07 — item-5 signal-origin definition superseded in part (S2)

**Status: `Accepted` (express supersession).** [S2 ADR](2026-08-07-loop-s2-signal-host-fork.md) **expressly** supersedes §4 item 5’s **TradingView-only** signal-origin limb. Forward discharge: a real strategy signal from the **ruled host** (Python daemon B1 POST with expected non-zero sizing at `dry_run=true`). Historical body above (incl. Addendum 2026-07-31 “real TradingView strategy signal” / “Redefinition stays forbidden”) is **frozen** — the bar was on *silent* redefinition; this addendum records the express edge. Item 5 remains **owed**; M1 stays `CODE_LANDED`; no event ids fabricated; deletion decline stands.

---

## Addendum 2026-08-24 — test strategy licensed for item 5; dated 08-24

**Does not amend** item 5’s limbs (real signal, expected non-zero sizing, Stage-1 `dry_run=true`, no silent redefinition, `--allow-live` must not write `dry_run_strategy_signal_event_id`). **Does not** claim M1 `RESOLVED`. **Does not** arm. **$0 / K=0.**

**Rule 0 (this addendum):** this file Addendum 2026-08-07 @ `027a729` — discharge is a ruled-host B1 POST at expected non-zero dry-run sizing. [S2](2026-08-07-loop-s2-signal-host-fork.md) §4.2 @ `027a729` — canned / live-armed / zero-qty floors stay DEAD-list. [GO ADR](2026-07-17-c1-rail-build-account-registration-go.md) de-scope addendum @ `acc4f41` — “Deploying any qualifying strategy makes it dischargeable again.” `ops/c1_signal_daemon/strategy_protocol.py` `NullStrategy` @ `027a729` — default never emits. Cheap falsifier: `rg -n "any qualifying strategy" docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` hits; `NullStrategy.on_bar` returns `None`.

**Operator ruling 2026-08-24:** item 5 may be discharged with a **test strategy** on the ruled host — `Strategy.on_bar` → daemon B1 POST → structured dry-run decision at expected non-zero sizing. Dated on the [`STATE.md`](../../STATE.md) 2026-08-24 board next to disaster-stop Phase 0a. Queue `#2` no longer waits on `#1` for this limb ([current queue](../../STATE.md#operator-queue--strictly-ordered-5-live-items)).

**Qualifying instrument:** evaluate-hook strategy, not a canned hand-POST (item 6 class), not `NullStrategy`, not a fabricated event id, not a withdrawn Striker redeploy. Any required `LEG_MAP` extension is part of the attended 08-24 packet, not this commit.

**Still owed after a recorded event id:** `operator_signoff`. `emit_enabled=true` is the attended emit step the daemon already refuses without a strategy GO — this addendum *is* that GO for a test strategy only. Q-M1WIRE-1 A2/A5 gaps do not block `RESOLVED`. `dry_run=false` stays forbidden.

## Addendum 2026-09-11 — item-5 input for Stage 1: operator-attended controlled input (express)

**Does not amend** item 5's limbs (real signal, expected non-zero sizing, Stage-1 `dry_run=true`, no silent redefinition, `--allow-live` must not write `dry_run_strategy_signal_event_id`). **Does not** claim M1 `RESOLVED`. **Does not** arm. **$0 / K=0.**

**Rule 0 (this addendum):** [S2b build ADR Addendum 2026-09-11](2026-08-08-s2b-signal-daemon-build.md#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d) — packet pinned at `df48c58` (status `PROPOSED` at that pin; it only recommends D); the ratification is the A1r revision in the same change-set (PR #340), verified by `grep -n '^\*\*Status:\*\* RATIFIED 2026-09-11' docs/adr/2026-08-08-s2b-signal-daemon-build.md` → 1 hit — option D, RATIFIED 2026-09-11 (options A/A′/B/C/E/F scored and not selected; option A ineligible on the eval account; option C out on TradingView Terms of Use §3). `ops/c1_signal_daemon/m1_stage1.py` `accept_bar` window `60 ≤ now − bar.ts ≤ 150` @ `3cdeabe`. `ops/c1_rail/m1_stage1_control.py::project_evidence` @ `811df7c` (returns `listener_event_id`, never `dry_run_strategy_signal_event_id`).

**Operator ruling 2026-09-11 ("i choose option d"; Q1–Q5 "adopt all, dated 2026-09-11"):** the Stage 1 ceremony's bar is a genuine, just-closed 1-minute bar of the dated front-month MYM contract named in the ceremony manifest (`venue_contract`), transcribed by the operator from the Tradovate platform chart and injected in-container within the ceremony window (`MYM1!` is the identity's listener route label, not a venue symbol; S2b build ADR Addendum 2026-09-11, option D, ratified 2026-09-11). This is the explicit amendment the 2026-09-10 addenda require: it is a **controlled input**, not a fixture or a replay — nothing is replayed from a store and the bar did not exist before the ceremony (Q1). The signal origin is the daemon (`Strategy.on_bar` → B1 → listener); the payload is not canned.

**What the item-5 event certifies:** the ruled host produced a real strategy signal on a real market bar with expected sizing at `dry_run=true`, through the deployed daemon and listener, including the ceremony journal, reservation, evidence join and input → decision price identity in production containers; the record names the venue contract the bar came from.
**What it does not certify:** any live feed. Live-feed readiness, feed → daemon price identity, feed health and the `MYM1!` ↔ venue-contract mapping for any live feed remain entirely separate and owed (S2b step 1). The evidence projection records `qualifying_live_source: false`, `operator_attended_input: true`; `dry_run_strategy_signal_event_id` is written only by the operator-signed A8 edit from a projection's `listener_event_id`.

**Not licensed by this addendum (Q2–Q5 scope):** a TradingView alert webhook as bar transport (Terms of Use §3 ruled applicable, Q3); any delayed feed without a window and staleness amendment (Q4); any Tradovate API session on the eval account (ineligible; primary confirmation left open, Q2); a machine feed for M1 (deferred to a production-strategy ruling, Q5); arming; `RESOLVED`.

---

## Addendum 2026-09-12 — `RUNBOOK.md` pointer re-home (TB-O1; no clause amended)

**Does not amend** §2, §4, §5 or any prior addendum; M1 stays `CODE_LANDED`; nothing arms.
**$0 / K=0.**

Six sites in this file cite `docs/notes/rail_build/RUNBOOK.md`: the §0 Rule-0 anchor (`d9e8f2a`),
the §6 downstream-artifacts list ("M1 gate and session export procedure"), the §Verification
`git log` command, and Addendum 2026-07-31b's §0 table row, §Falsifier ("a new entry in the RUNBOOK
§B7 arming log") and §10 hook 2 (`grep -n "DRY_RUN=false" …`). The file left the public tree under
the [public-visibility ADR](2026-08-14-repo-public-visibility-transition.md)'s exclusion rule
(operational logs carrying the live account identifier and dollar history). Those sites stay
byte-unedited (Trap #12); this addendum and the header intercept re-home the reader:

- **Public procedure (steps, interlocks, window, stop conditions, recovery pointers):**
  [`docs/notes/rail_build/ARMING_PROCEDURE.md`](../notes/rail_build/ARMING_PROCEDURE.md) — TB-O1,
  Track B umbrella. It restates no account value and authorizes nothing.
- **Private runbook (history, B7 arming log, crash-loop recovery):** retrieved per that file's §2 —
  archive pin `5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2` (the revision Track A §A3 verified), or
  the `pre-prune-2026-08-08` blob `d523ee0d…` copied into the primary checkout's ignored private
  root (`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/rail_build/`).
  Hooks 2 and the §Verification anchor command run against that copy; their expected counts were
  recorded against the 2026-07-31 revision and are not re-baselined here.
- **Unchanged:** the crash-loop recovery procedure (private; availability attested in the
  [readiness record](../notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md) §A3), the acceptance
  JSON's status, evidence ids, pins and signoff (a `notes` entry only was added, same PR).

Reads: this file @ `0059ca7` (six sites located by `grep -n RUNBOOK`) · `ops/c1_rail/c1_rail_arm.py`
@ `027a729` · `ops/c1_rail/c1_rail_http_server.py` @ `027a729`.

---

## Addendum 2026-10-01 — `transport_unknown` risk-add block proven only within one process; #571 parked

**Finding.** On `main`, the legacy c1-rail `EventLedger` lifts the `transport_unknown` risk-add block across a restart. This acceptance's "transport_unknown blocks risk-add" drill exercised that block only within a single process. PR #571 makes the block durable across restarts, but it is **parked** by operator ruling (deployment checklist, [first-session simplification rulings](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-01--first-session-simplification-rulings-six-cuts), item 4). The book route does not use this path. It halts durably through CC-3 (`ops/c1_rail/book_account_owner.py`).

**Limitation and guard.** M1's `RESOLVED` status stands for the record. While #571 is parked, **it does not support arming any legacy leg**:
- `dry_run=true` stays;
- no `c1_rail_arm` of any legacy leg, including the M1 Stage-1 test leg;
- #571 is retained and deployed, with its pin refresh, before any legacy re-arm or M1 Stage-1 ceremony.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-10-15 | History trim (header Revision line): §0 non-RUNBOOK bullets + cheap-falsifier transcript, §7 phases, §10 duplicated evidence list, and the narrative of Addenda 2026-07-31 / 2026-07-31b condensed; 4-session trigger dispositioned discharged; 07-31b falsifier disposition appended; Status / L5 / hook-4 / §10-path FIXes. RUNBOOK sites unchanged; prior text pinned at `4121e84c` (ADR decay audit; operator direction 2026-10-15) | Claude Code (recorder) |
| 2026-09-12 | Addendum + header intercept — `RUNBOOK.md` pointer re-home to the public `ARMING_PROCEDURE.md` and the private retrieval convention (TB-O1); no clause amended, status unchanged | Claude Code (recorder) |
| 2026-09-11 | Codex fold (PR #340): Rule 0 pin distinguishes the PROPOSED packet pin from the A1r ratification; option D names the venue contract (`venue_contract`) the operator reads — provenance, not sizing | Claude (fold) · Codex (review) |
| 2026-09-11 | Addendum — item-5 Stage 1 input = operator-attended controlled input (express); limbs, decline, no-arm stand; TV webhook / delayed feed / eval-account API not licensed | Joshua (ruling) · Claude (recorder) |
| 2026-08-24 | **Test strategy licensed** as item-5 qualifying emit; dated 08-24. Limbs + deletion decline + no-arm stand; M1 stays `CODE_LANDED` until the attended session records the event id + `operator_signoff` | Joshua (ruling) · Cursor (recorder) |
| 2026-08-07 | **§5 autonomous-promotion limb superseded in part** by S5 ADR (bounded sandbox lane). Header `Superseded-in-part-by` extended; no second tier/state writer; arm-gate + unattended bar stand | Cursor (drafter) · Joshua (plan GO) |
| 2026-08-07 | **Item-5 signal-origin superseded in part** by S2 ADR (Python-native ruled host). Header `Superseded-in-part-by` + this addendum; historical body frozen; item 5 still owed; `status` unchanged | Cursor (drafter) · Joshua (plan GO) |
| 2026-08-02 | **4-session review trigger RATIFIED** (Addendum 2026-07-31 item 3; operator ruling *"rule the 4-session trigger"*). Counting convention **derived from the proposal's own model, not chosen**: a session counts whether or not a signal arrived, because the stated *"~23% chance of nothing after four more"* reproduces only as `(1−0.307)^4 = 23.06%` — attended sessions, not signal-bearing ones. A session that never reached the entry window does not count. Reachability verified: fires at **23.1%** after 4 sessions ≈ 2 weeks; sessions 1–4 are **08-04 / 08-07 / 08-11 / 08-14**, review after **2026-08-14**. Schedules a look, **not** an outcome — no auto-delete of item 5, no gate relaxation, decline stands unless the operator changes it | Claude (specify + reachability) · Joshua (ruling) |
| 2026-07-31 | Addendum 2026-07-31b **RATIFIED** — operator ruling *"ratify the trigger change"*. **M1's trigger moves from "before the next armed send" to "before the next armed session"** (`dry_run=false` may not be set while M1 is not `RESOLVED`), **applied at four normative sites**: §Status, §2 M1 heading, §2 Effective, §6 maturity table. The 07-28 and 07-31 deviations are **recorded, NOT ratified retroactively**. Finding behind it: neither session was stopped by the gate — an arithmetic floor (`qty_out 0`) and an absent signal stopped them. Zero new operational cost: Stage 1 is unarmed by definition, so the only path M1 requires already complies. M1 remains `CODE_LANDED` | Claude (draft + apply) · Joshua (ruling) |
| 2026-07-31 | Addendum 2026-07-31 — deletion of §4 item 5 proposed, then **DECLINED** by operator ruling. §4 unchanged; item 5 stands. The draft's "circular" premise is **corrected on the record**: Stage 1 is the unarmed stage, so item 5 is satisfiable as written. Operative: run Stage 1 unarmed; redefinition stays forbidden | Claude (draft + correction) · Joshua (ruling) |
| 2026-07-23 | Operator ratification → Status `Accepted`; reverse partial-supersession edge on c1 GO ADR; M1 implementation authorized (M1 `RESOLVED` still owed before next armed send) | Joshua (decision) · Cursor (apply) |
| 2026-07-22 | Initial `Proposed` ADR; venue-native M1 gate plus staged M2/M3 monitoring maturity | Joshua + Cursor |
