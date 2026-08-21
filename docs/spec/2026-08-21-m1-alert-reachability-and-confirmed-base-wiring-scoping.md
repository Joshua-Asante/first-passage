# SPEC (scoping only) — M1 alert reachability + confirmed-base wiring: closing the Q-M1WIRE-1 gaps

**Status:** `Proposed` — scoping pass only. **No code lands with this document.** Ratification of
this document authorizes a follow-up implementation ADR + pre-registration for `ops/c1_rail/`
changes; it does not itself wire anything. Per `Q-M1WIRE-1`'s own §5 forbidden moves, wiring A2/A5
as a byproduct of a diagnostic brief is barred — this spec is the vehicle that discipline requires
before any of the below can land.
**Decision date:** 2026-08-21
**Authors:** Joshua (direction) + Claude Code (scoping)
**Related:** [`Q-M1WIRE-1` closure (FALSIFIED)](../briefs/closures/Q-M1WIRE-1-closure-falsified.md) — the diagnostic this spec answers · [`M1 ADR`](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) — owning ADR for the acceptance package, frozen §10 hooks · `.claude/skills/c1-rail/SKILL.md` — standing safety invariants this spec must not violate
**Layer:** execution / infrastructure, `ops/c1_rail/`. **Explicitly not in scope: any `dry_run`, arm-path, sizing-law, or `dd_protection`/lifecycle change.**

---

## §0 — Rule 0 reads (this session, 2026-08-21)

- [`ops/c1_rail/c1_rail_telemetry.py:161-224`](../../ops/c1_rail/c1_rail_telemetry.py) — `LoggingNotifier` (process log only) and `FileAckNotifier` (JSONL alert log + operator-written ack file). Both are **pull-based**; nothing pushes. `FileAckNotifier`'s own docstring: *"operator-reachable on the Fly volume... without inventing a third-party provider"* — a deliberate prior design constraint, not an oversight.
- [`ops/c1_rail/c1_sizing_host_reference.py:175-192`](../../ops/c1_rail/c1_sizing_host_reference.py) — `confirm_executed_base(leg_key, qty)` exists, is documented (*"Call `confirm_executed_base` after durable [fill confirmation]"*), and is **never called outside `tests/`**.
- [`ops/c1_rail/c1_rail_telemetry.py:403+`](../../ops/c1_rail/c1_rail_telemetry.py) — `EventLedger.set_confirmed_base` — same pattern: defined, tested, never called in production.
- [`docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`](../notes/rail_build/M1_MONITORING_ACCEPTANCE.json), item-6 note (2026-07-27 SIM CHAIN_OK session) — the only concrete precedent for how a confirmed fill is actually recorded today: an **operator-attested BrokerEvidence append** to `/data/c1_broker_evidence.jsonl`, manually reconciled via `python ops/c1_rail_telemetry.py --events ... --event-id ... --evidence ...`, printing `CHAIN_OK`. This is the one moment in the current design where "the base is actually confirmed" is knowable — and `confirm_executed_base` is not called from it.
- [`ops/c1_rail/c1_rail_arm.py:79-117`](../../ops/c1_rail/c1_rail_arm.py) (`m1_acceptance_reason`) — validates the acceptance artifact's schema/status only; never calls `tree_skew()`.
- [`scripts/gates.yml`](../../scripts/gates.yml) — no `validate_c1_monitoring_acceptance` entry at any tier.
- `Q-M1WIRE-1` closure §1/§4 — the two confirmed gaps this spec exists to close (A2, A5), and the explicit note that A4 (human alert-reachability) is a separate, still-open question this spec does not answer — a monitor changes what happens *after* an alert fires, not whether a human notices it.

---

## §1 — Context

`Q-M1WIRE-1` closed `FALSIFIED` 2026-08-21 on two independently-confirmed gaps: nothing in production ever calls the confirmed-base recording methods (A2), and nothing checks fixture-hash drift before arming or on any cadence (A5). Both gaps share a root cause worth naming plainly: the M1 acceptance package was built to **certify a schema**, and the schema was mistaken for the capability. This spec scopes closing both gaps for real, plus the adjacent question A5 raised but didn't fully cover — whether alert delivery should keep depending entirely on a human happening to check a file.

**Decision driver:** these are the last two concrete, already-diagnosed gaps standing between "M1 says `RESOLVED`" and "M1 is actually true." Item 5 (a real strategy-signal fill) and `operator_signoff` remain separately owed and are untouched by this spec.

---

## §2 — Decision (scope only — three components, each with open design questions)

This is deliberately **not** a single mechanism. The three problems are different shapes and may want different fixes; forcing one design would repeat the exact "one artifact stands in for three claims" mistake `Q-M1WIRE-1` just found.

### Component A — wire `confirm_executed_base` to a real production call site (closes A2)

**Problem:** the only place in the current design where a fill becomes *known* rather than *intended* is the manual operator-run broker-evidence reconciliation CLI (`c1_rail_telemetry.py --evidence`). `confirm_executed_base`/`set_confirmed_base` are never called from there or anywhere else live.

**Candidate approaches (not chosen here):**
1. Call `confirm_executed_base` from inside `reconcile_chain`/`reconcile_event` at the moment a `CHAIN_OK` verdict is reached — ties the write to the one place confirmation is already operator-attested, no new trust surface. Open question: `reconcile_*` is currently read-only evidence-joining; giving it a write side-effect changes its contract and needs its own review.
2. A separate, explicit CLI step the operator runs immediately after `CHAIN_OK` — keeps `reconcile_*` pure, but reintroduces exactly the "an extra manual step nobody remembers" failure shape this repo has already named more than once this session (the crash-loop, the M1 forgery hole).
3. Something entirely different if a real fill-confirmation event ever gets a machine source (e.g. a broker webhook) rather than operator attestation — out of scope until such a source exists.

**Not decided here:** which of these, or something else. That's implementation-ADR work.

### Component B — wire fixture-hash drift into an arm check or `gates.yml` (closes A5, first half)

**Problem:** `validate_c1_monitoring_acceptance.py --check-tree-skew` exists and works (confirmed this session — it correctly reported 6/6 drift), but nothing calls it before arming, and it's absent from `gates.yml` at every tier.

**Candidate approaches:**
1. Add a call to `--check-tree-skew --require-tree-current` inside `c1_rail_arm.py`'s arm path itself, hard-failing the arm attempt on drift — closes the gap at the point that actually matters (arm time), but only fires on an actual arm attempt, which is rare by design.
2. Add a `gates.yml` entry at a low-cost tier (e.g. weekly/on-touch) so drift is visible long before an arm attempt — cheaper feedback loop, but doesn't itself gate arming (a gap the arm-path check in (1) closes and this doesn't).
3. Both — arguably the honest answer, since they answer different questions ("is it safe to arm right now" vs. "has this drifted since I last looked").

**Not decided here:** which, or both. Note for whoever picks this up: `c1_rail_arm.py`'s arm path is explicitly named in `Q-M1WIRE-1`'s and the M1 ADR's own frozen surfaces — this is exactly the kind of edit CLAUDE.md's live-execution posture requires an admitting ADR for, not a quiet patch.

### Component C — alert reachability beyond a pull-only file (addresses the reachability *mechanism* A5 touches; does not replace A4's human-attention test)

**Problem:** both existing notifier channels require a human to go look at something. There is no push channel. A mechanical monitor that watches `alert_path` and escalates on an unacknowledged CRITICAL alert would shorten the *mechanical* gap — but it does not answer A4's actual question, which is about human attention, not machinery. A4's unannounced drill stays owed regardless of what gets built here.

**Candidate approaches:**
1. A lightweight watcher (cron/scheduled process, same host) that tails `alert_path`, and if a CRITICAL entry has no matching `.ack.json` within N minutes, escalates — to the process log at minimum (cheap, no new dependency), or to a real push channel if one gets approved.
2. A real push channel (email/SMS/webhook) for CRITICAL only. **This directly reopens a design choice `FileAckNotifier`'s own docstring already made deliberately** ("without inventing a third-party provider") — proposing to reverse that needs to say why, not just add it.
3. Do nothing mechanical, and instead treat A4 as the real test: if the unannounced drill shows reachability is fine in practice, a monitor may be solving a problem that doesn't exist. **This is a legitimate answer** — worth running A4 before committing to (1) or (2), so the fix matches a measured gap rather than an assumed one.

**Not decided here.** Recommend, but do not require: run the A4 drill before choosing between (1)/(2)/(3) — it directly informs whether this component is needed at all.

---

## §3 — Forbidden moves (this document)

- **No code lands with this spec.** Landing any of A/B/C needs its own pre-registration → re-derivation → admitting ADR, per `Q-M1WIRE-1` §5 and CLAUDE.md's live-execution posture.
- **No `dry_run`, arm-path, sizing-law, `dd_protection`, or lifecycle edit** — even Component B's arm-path candidate is a *scoped option*, not an authorization to edit `c1_rail_arm.py`.
- **Do not treat Component C as a substitute for A4.** A monitor changes what happens after an alert fires. It does not test whether a human notices it. Both are owed independently.
- **Do not pick a third-party notification provider by default** in a follow-up ADR without addressing why `FileAckNotifier`'s stated "no third-party provider" constraint no longer holds — that constraint was deliberate, not an oversight this spec gets to quietly override.

## §4 — Gate (what "scoped enough" means)

This spec is ready to ratify when: the three components are separable (a follow-up ADR could pick up just one), each carries at least one concrete candidate approach with a stated open question, and no candidate approach requires touching a locked/frozen surface without naming that it does. **Ratification does not authorize implementation** — it authorizes a named successor (implementation ADR + pre-registration) to be opened, per the parent-Q convention (naming ≠ opening).

## §5 — Consequences

**Positive:** the two confirmed `Q-M1WIRE-1` gaps get a real path to closure instead of sitting as findings; Component C gives A4 a mechanical complement worth having regardless of the drill's outcome.
**Cost:** three follow-up efforts instead of one, deliberately — the alternative (one combined fix) would repeat the exact conflation `Q-M1WIRE-1` exists to prevent.
**Risk:** none live — nothing here executes against the deployed rail; the risk is entirely "this scoping turns out incomplete at implementation time," which is what the follow-up ADR's own Rule 0 pass is for.

## §7 — Implementation plan

- **Phase 0 (this document).** Scoping only, `Proposed`.
- **Phase 1 (operator ratification).** Status → `Accepted`. Does not authorize code.
- **Phase 2 (separate, per component).** Whoever picks up A, B, or C opens its own pre-registration/ADR, re-reads the frozen surfaces named above fresh, and lands independently. Components may ratify and land in any order or not at all.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-21 | Initial scoping — `Proposed`, three components, no code | Joshua (direction) + Claude Code |
