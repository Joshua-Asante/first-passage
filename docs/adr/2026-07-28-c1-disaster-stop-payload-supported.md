# ADR 2026-07-28 — Rail-side payload-supported disaster stop for c1 base-entry orders

**Status:** `Accepted` — operator GO 2026-08-22. Accept is the decision GO; §7 Phase 0 empirical SIM remains the implementation gate before any `sl=` wiring lands armed. Does not authorize skipping Phase 0 or setting `dry_run=false`.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-28
**Authors:** Joshua (decision pending) + Claude Code (authoring, brainstorm item C2)
**Supersedes:** none
**Related:** [`2026-07-17-c1-rail-build-account-registration-go.md`](2026-07-17-c1-rail-build-account-registration-go.md) (parent GO ADR — this decision operates entirely within its account/attended-posture/spend-ceiling scope, adds nothing to it); [`docs/spec/c1_nt8_sizing_host_impl.md`](../spec/c1_nt8_sizing_host_impl.md) `Proposed`/Option-C-adopted (§2's exit-scope line this ADR narrowly extends, not overrides — see §1); [`docs/spec/c1_watch_realization_multiplier_layer.md`](../spec/c1_watch_realization_multiplier_layer.md) `Accepted` (source of the `stop_dist_pts` semantics this design consumes verbatim); [`2026-07-22-c1-venue-native-monitoring-maturity.md`](2026-07-22-c1-venue-native-monitoring-maturity.md) (M1 telemetry spine this design adds one event type to); [`docs/notes/2026-07-24-execution-quality-investigation.md`](../notes/2026-07-24-execution-quality-investigation.md) (standing research interest this proposal was scoped under, brainstorm item C2, 2026-07-28 session).
**Layer:** execution — not locked-parameter. No change to locked Pine, allocations, `dd_protection` constants, or sizing law; this ADR relays a value Pine already computes, it does not compute or tune one.

---

## §0 — Rule 0 reads (production-source verification)

Repo-internal (all read directly this session, 2026-07-28; anchors via `git log -1`):

- [`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py) — anchor `c134060` (2026-07-24). Full read. Confirms `stop_dist_pts` is a required entry-payload field, consumed only to derive `per_contract` for qty sizing, and is **not** carried onto `SizingDecision` — the raw payload value must be read by the caller directly, not via the decision object. Confirms `signal_type in ("exit", "flat")` returns immediately with a comment: *"Bookkeeping only — exits/EOD/DD-closes are the strategy's own orders + CrossTrade Account Manager, never this host's."*
- [`ops/c1_rail/crosstrade_payload.py`](../../ops/c1_rail/crosstrade_payload.py) — anchor `54b1489` (2026-07-23). Full read. `build_crosstrade_payload` already accepts `sl: float | None = None, tp: float | None = None` and, when set, appends `stop_loss={sl}` / `take_profit={tp}` to the payload text (lines 46, 82-85). **This capability exists and is untested-in-production-path but already payload-correct** — it was promoted from `tests/rail_crosstrade/translator.py`'s golden-path prototype and carried forward unused.
- [`ops/c1_rail/c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py) — anchor `5fa31b5` (2026-07-27). Full read. `handle_signal`'s call to `build_crosstrade_payload` (lines 254-258) passes `leg, action, symbol, qty, order_id, account, secret_key, destination` — **no `sl`/`tp`**. This is the exact, single wiring gap: the field exists at the payload-builder layer and is unused at the only call site.
- [`ops/c1_rail/c1_rail_http_server.py`](../../ops/c1_rail/c1_rail_http_server.py) — anchor `5fa31b5` (2026-07-27). Targeted read (`build_parsed_fields`, L374-382). Confirms `stop_dist_pts` and `close` are both captured verbatim into `request_received.parsed` at every signal, not just entry — so the raw values this design needs are already ledger-visible today, independent of this ADR.
- [`ops/c1_rail/c1_rail_telemetry.py`](../../ops/c1_rail/c1_rail_telemetry.py) — anchor `b949642` (2026-07-27). Targeted read (grep on `reconcile`). Confirms `reconcile_chain` / `reconcile_event` / `write_reconciliation` exist as an "evidence overlay + six fixed reconcile verdicts" mechanism joining rail records to broker evidence by `event_id` — the existing structure this design's telemetry gap (§6) should extend, not a new mechanism.
- [`core/firm_rules.py`](../../core/firm_rules.py) — anchor `cb60516` (2026-07-26). Targeted read. `Tradeify_Select_100K`: `dd_type=trailing_locking`, `max_dd_pct=3.0`, `dd_lock_offset_usd=100`, `micro_contract_cap=80`, `cost_per_side_usd=0.91`.
- [`docs/spec/c1_nt8_sizing_host_impl.md`](../spec/c1_nt8_sizing_host_impl.md) — anchor `2910882` (2026-07-24). Read §0-§2.2. §2 Decision states verbatim: *"It does not manage exits, EOD flatten, or DD-limit closes — those remain the strategy's own `strategy.exit`/`strategy.close_all` orders and CrossTrade's Account Manager (E1); this host sizes entry and add orders only."* This is the tension §1 below addresses directly.
- [`docs/spec/c1_watch_realization_multiplier_layer.md`](../spec/c1_watch_realization_multiplier_layer.md) — anchor `25c5a92` (2026-07-17). Read §0 + §2 in full (initial targeted read was line 49 only; a §10 audit-hook re-run this session surfaced the fuller §0 and is folded in here per the "surrounding-context" Rule-0 sub-rule, rather than left as a narrower citation than what was actually available). Verbatim (§2, current/decision-state): *"Pine already computes `stop_dist` at signal time (`stopDist = atrVal * stopAtr`, both editions) — the payload emits it; it does not create it."* §0 also carries a **direct Pine-source quote** (gitignored file, read on local disk by that document's author): DJ30/MYM lines 248-252, *"`stopDist = atrVal * stopAtr; size = calcSize(stopDist); strategy.entry(qty=size)`"*; NAS100 CFD source `atrLength=11, stopAtr=1.20`. **Caveat, stated per the citation-chain discipline:** that quote's PORT_MANIFEST pin (`fd91f37b…`) predates the currently-published venue editions (STATE.md 2026-07-28 pointer-log: MYM v3 Jul 22 17:04 / MNQ v4 Jul 22 17:05, re-pinned after the alert-shadowing fix) — the exact line numbers and pin are a **superseded snapshot**, corroborating-only (Tier 2-3), not a live Tier-1 match. **This ADR's correctness does not depend on resolving that gap:** the value this design consumes is validated by the rail's own current, directly-verified contract — `_REQUIRED_PAYLOAD_FIELDS` in `c1_sizing_host_reference.py` (§0 above, anchor `c134060`, 2026-07-24) hard-halts entry sizing if `stop_dist_pts` is absent from the payload, so the field's live presence is already load-bearing for today's qty computation, independent of this ADR and independent of Pine's internal formula. This worktree has no local Pine copy (`ls core/strategies/*/[...].pine` — not found, consistent with the repo's public-clone gitignore posture), so a fresh direct read was not possible this session; Phase 0 (§7) should include a cheap `scripts/check_pine_manifest.py` pass to confirm the PORT_MANIFEST pins are current before Phase 1 implementation.
- [`docs/adr/2026-07-17-c1-rail-build-account-registration-go.md`](2026-07-17-c1-rail-build-account-registration-go.md) — anchor `153b64e` (2026-07-24, latest addendum). Full read incl. all four addenda. §5 already carries the forbidden move *"Arming any session with neither the CrossTrade Account Manager nor the operator 15:55 ET flat-check active"* (2026-07-19 addendum) — established precedent that a single exit path is doctrine-recognized as insufficient; this ADR is the same logic applied across the trade's full lifetime, not just EOD.
- [`docs/rejected_candidates.md`](../rejected_candidates.md) — anchor `fbf3590` (2026-07-27). Grepped for `stop|bracket|OCO|disaster|dead.man` — no prior rejection of a protective-stop-as-safety-mechanism on the existing book (the one "protective stop" hit is an unrelated 5th-leg EURUSD fix-fade *entry* mechanism, rejected on cost-geometry grounds — different mechanism family, no collision).

External (fetched live this session, 2026-07-28 — Tier 1, primary source, dated):

- [`crosstrade.io/docs/webhooks/commands/place-order`](https://crosstrade.io/docs/webhooks/commands/place-order) — verbatim: *"`place` is fully supported with `destination=tradovate;`, including `flatten_first`, Tradovate-native TP/SL brackets, iceberg `max_show`, trailing stops, MIT, and extra TIFs."* Separately, the page documents that NinjaTrader **ATM Strategies** *"will create orphaned Stops and Target orders as those are not canceled by default"* — an explicit, documented orphan-order failure mode in this ecosystem, but for a **different** order-management system (NT8 ATM, not in this rail's Option-C path) than the one this ADR proposes using.
- [`crosstrade.io/docs/webhooks/advanced-options/tradovate-atm`](https://crosstrade.io/docs/webhooks/advanced-options/tradovate-atm) — the "ownership matrix": *"Entry, scale-out targets, fixed stops, and OCO relationships"* are listed **Tradovate native** (broker-owned, not CrossTrade-emulated). **Not documented anywhere on either page:** what happens to a resting native stop when the position is closed by a *separate* command (this rail's own later `closeposition` call) rather than by the bracket's own sibling leg filling, or whether a stop firing against an already-flat position can open an unintended new position. This is the load-bearing open question §7 Phase 0 exists to close empirically — it is not resolved by documentation and this ADR does not pretend otherwise.

**Contingency note:** the mechanism's *existence* (Tradovate-native OCO brackets, reachable via CrossTrade's documented `stop_loss=`/`take_profit=` fields on `destination=tradovate`) is Tier-1-cited and solid. The mechanism's *cross-command cancellation behavior* — the one fact that determines whether this design is safe to arm — is undocumented publicly and is treated throughout this ADR as unverified, gated behind a mandatory empirical test (§7 Phase 0), never assumed.

---

## §1 — Context

The 2026-07-24 execution-quality investigation note ([pointer](../notes/2026-07-24-execution-quality-investigation.md)) set the standing research interest — better fills and exits — and named exit measurement as "half the standing interest" and currently unmeasured. This ADR is not that measurement; it is a **safety** proposal (brainstorm survey item "C2," 2026-07-28 session) discovered while surveying the option space, and it is motivated by a **dated incident**, not a hypothetical.

**The incident this closes a gap against:** per STATE.md's 2026-07-28 pointer-log entry, the TV→rail signal path was **silently broken from 2026-07-24 to 2026-07-28** — alerts created 2026-07-18 ran a pre-fix Pine snapshot and arrived as plain text (`body_category=non_json`), which the rail correctly logged and refused to size, but nothing about that failure was visible from the TradingView side, and it was not caught by any of the attended sessions in that window (07-24, 07-27) because the rail's own ignored-alert log was not what anyone was watching. The seam is now proven (SEAM THEN PROVEN, same entry), but the failure class — *the signal path can go silently dead while everything upstream looks fine* — is not something this fix retires; it is a property of having exactly one path from Pine's exit decision to the broker.

**Today, if that same failure class recurs while a position is open, there is no broker-side protection at all.** The sizing host explicitly declines this responsibility (§0 citation: *"exits ... are the strategy's own orders ... never this host's"*), the CrossTrade Account Manager remains unavailable for the Tradovate destination (2026-07-19 GO ADR addendum, unconfirmed whether still true — flagged as a stale check in §5), and the only standing backstop is the 16:45 ET firm auto-flatten — a many-hours-wide exposure window, non-fatal to the account but not small. The GO ADR's own §5 already encodes the doctrine that a single exit path is insufficient — that is exactly why the 2026-07-19 addendum forbids arming without *either* the CrossTrade AM *or* the operator's manual 15:55 ET check. This ADR extends that same doctrine from "covered at EOD" to "covered for the trade's full lifetime," using a mechanism that costs nothing against the modeled edge (§6).

**The apparent tension with standing doctrine, named directly:** the frozen sizing-host spec states the host "does not manage exits ... this host sizes entry and add orders only" (§0 citation). This ADR does not change what the sizing host computes — `C1SizingHostReference.process_signal` is untouched, still returns qty only. What changes is one layer up: `c1_rail_listener.py::handle_signal` already has direct access to the raw incoming payload (`payload["close"]`, `payload["stop_dist_pts"]`) before it ever calls the sizing host, and it already builds a CrossTrade `place` order for every entry. This ADR proposes attaching one additional, already-existing payload field (`sl=`) to that **same** order submission — not a new exit decision, not a new order, not the sizing host managing anything. The stop's price is fully determined by a number **Pine itself already computed and already emits** (`stopDist = atrVal * stopAtr`, §0 citation) — the rail relays it, the same way it already relays `qty`. If this distinction does not hold up to future scrutiny, that is a reason to amend or withdraw this ADR, not to read it as silently contradicting the frozen spec.

**Decision driver (one sentence):** the exact failure class that produced four days of unprotected live exposure (07-24→07-28) has no broker-side backstop today, and the fix costs one unused struct field plus a keyword argument — the gap is worth closing before, not after, the next occurrence.

---

## §2 — Decision

**Decision:** For **base-entry orders only** (`signal_type == "entry"`, not `add`, not `exit`/`flat`) on both c1 legs, `c1_rail_listener.py::handle_signal` computes a stop price from the raw incoming payload (`stop_price = payload["close"] - payload["stop_dist_pts"]`, long-only so the stop sits below close) and passes it as `sl=stop_price` to `build_crosstrade_payload`, attaching a Tradovate-native stop-loss bracket to the same `place` order already being submitted. **No take-profit is attached** (`tp` stays `None` — see §3, §5). Pine's own managed exit (`strategy.exit`/`strategy.close_all` relayed via the existing `command=closeposition` path) remains the **primary, first-line exit mechanism**, unchanged in every respect; the broker-side stop is strictly a backstop for the case where that primary path is dead.

**Effective:** not immediately — contingent on (a) operator GO and (b) §7 Phase 0's empirical verification passing. Until both, this ADR's status stays `Proposed` and no code implementing it lands armed.
**Scope:** `dj30_mym` and `nas100_mnq` base ("entry") orders on `Tradeify_Select_100K`, while the c1 rail is armed (`dry_run=false`). Add orders, exit orders, and flat orders are explicitly **out of scope** and unaffected (see §3 for why add is excluded; exit/flat already carry no `sl`/`tp` semantics — `build_crosstrade_payload`'s `closeposition` branch does not accept them). No new subscription or account — but **not free or risk-free either**: the empirical verification (§7 Phase 0) fires on the same **real** Tradeify eval account as the 2026-07-20 controlled one-shot (−$[redacted]) and the 2026-07-27 `CHAIN_OK` run (+$[redacted]); CrossTrade has no separate paper-trading destination for `destination=tradovate`. Cost is bounded to that same small class by using account-minimum quantity on the test fires, and per the 2026-07-19 standing convention the resulting in-eval P&L does not count against the GO ADR's $700 ceiling — but it is real money moving on the real account, not a demo sandbox, and needs the same attended-only posture as any other armed-adjacent action. Live testing (Phase 2/3) rides sessions already planned under the GO ADR's existing attended posture.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo — rely solely on Pine → rail → `closeposition`** | This is the exact path that went silently dead for four days, undetected during two attended sessions in that window. The GO ADR's own §5 already treats a single exit path as insufficient at EOD (2026-07-19 addendum); leaving the rest of the trade's lifetime on a single path is the same risk, uncovered. |
| **Wait for the CrossTrade Account Manager (Tradovate destination)** | Deferred since 2026-07-19 (banner: "coming soon" at that check). Solves a different problem (automated EOD flatten + DD-guard, account-level) — not a per-trade catastrophic-loss backstop, and still unavailable as of the last confirmed check (unconfirmed whether that has changed since — flagged in §5, not assumed). |
| **Rail-side polling/reconciliation loop** (rail periodically compares broker position to expected state, force-closes on divergence) | Requires the rail to hold verified live position truth — a capability `c1_sizing_host_reference.py`'s own comments call out as not yet built ("when the host gains verified live position truth, this static split relaxes to a runtime headroom check"). Building that is a materially larger scope than wiring an already-existing, already-tested payload field, and it recreates exactly the class of live-position-dependent sizing the M8 fail-safe doctrine exists to avoid. |
| **Attach take-profit alongside the stop** | Asymmetric in the wrong direction. A stop only ever *reduces* loss if it fires; a take-profit that fires prematurely *forfeits* upside — and the adds, which the stop does not even cover, carry 63.6% (MYM) / 87.7% (MNQ) of panel net (2026-07-24 execution-quality note, §0-cited there). Capping the base position's profit via a fixed broker-side TP works directly against the pyramid edge. Scoped out; see §5. |
| **Cover the add leg in this same ADR** | The add fires as a separate order against an already-open position. Whether a second `stop_loss=` at add-time replaces, stacks with, or conflicts with the base entry's resting bracket is not documented anywhere this session's research reached (§0). Bundling it here would compound one unresolved-semantics question with a second, distinct one in the same decision. Scoping to base-only bounds the unknown to a single, simpler case while still covering the position's largest single unprotected quantity (the base is where the position originates; an unprotected base is the worse failure mode than an unprotected add sitting on top of a protected base). |

---

## §4 — Falsifier (revert trigger)

This ADR is a **falsifiable safety claim**, not a permanent architectural commitment: the hypothesis is that a broker-native stop, attached at entry using Pine's own already-computed distance, strictly improves the account's worst case with no cost to modeled edge. Anything that falsifies either half of that claim reverts it.

**Revert trigger (any one, non-discretionary):**

1. **§7 Phase 0's empirical SIM test finds that a resting native stop does NOT auto-cancel when the position is closed via a separate `closeposition` command** (i.e., the exact healthy-path Pine exit leaves an orphaned working stop at the broker). This is the load-bearing falsifier — a negative result here means the mechanism as designed is not safe to arm at all, full stop, before any code beyond the Phase 0 test itself is written.
2. **Any single live occurrence** of the disaster stop firing while it should have been cancelled (i.e., coinciding with a healthy signal path that should have exited via the normal route first), or opening any position while the account was already flat. One incident is sufficient — this is not a statistical threshold, given the severity class (an unintended live fill).
3. **Any live occurrence** where the disaster stop fires and Pine's real managed exit (if BE/trail logic exists on these editions — unconfirmed this session, Pine source gitignored) would have exited materially better, by an amount large enough that the static ATR-distance stop is judged to be providing false comfort rather than real protection. (Deliberately soft-worded — this is an operator judgment call at review, not a mechanical trigger, because "materially better" has no pre-registered threshold and inventing one without live data would be exactly the kind of ungrounded precision brief-authoring discipline warns against.)

**Falsifiable hypothesis, stated once for the record:** if the Phase 0 SIM test passes (stop auto-cancels correctly on external close, does not misfire when flat) and the first ~10 live base-entry fills with the mechanism active show zero unintended fills and zero orphaned-order incidents, then H holds — the mechanism is validated as a standing safety feature. If either condition fails, H is falsified and the design reverts.

**Revert action:** disarm immediately if live (`dry_run=true`), strip the `sl=` argument from the `build_crosstrade_payload` call in `c1_rail_listener.py` (a one-line revert, by design — see §6), notify operator, and either open a fresh Pre-Q for a redesign (e.g., an explicit rail-side cancel-companion if native OCO proves insufficient) or withdraw this ADR outright.

**Trigger check schedule:** Phase 0 (§7) before any implementation lands; every armed session thereafter until ~10 base-entry fills with the mechanism active have accumulated (mirrors the existing P1 ~10-add-fill checkpoint cadence from the 2026-07-24 execution-quality plan), at which point review and either confirm as a standing feature or amend.

---

## §5 — Forbidden moves (under this ADR)

- **Attaching `take_profit` under this ADR's authority.** Ruled out in §3 on asymmetric-risk grounds. A future proposal to cap upside via broker bracket needs its own falsifiable case weighed against the pyramid-add edge concentration — not a quiet extension of this one.
- **Extending the bracket to `add` orders without a fresh, dedicated verification of stacking/replace semantics.** The base-only scope in §2 is deliberate. Widening it because "the mechanism already works for base" would carry over an unverified assumption into a case with its own distinct unknowns.
- **Treating "OCO relationships ... Tradovate native" (§0 citation) as proof that cross-command cancellation is safe.** The fetched documentation confirms bracket OCO exists as a broker-native feature; it is silent on whether a *third*, separate command (this rail's own later `closeposition` call, arriving on a different HTTP request than the original bracket-carrying entry) triggers that cancellation. Conflating "the feature exists" with "the feature covers our exact two-command pattern" is precisely the gap Rule 0 exists to catch — §7 Phase 0 exists because this was tempting to just assume.
- **Computing a stop distance independent of `stop_dist_pts`.** Tightening it "for safety margin" or widening it "to reduce false stops" would be inventing a parameter outside Pine's locked logic and outside this ADR's mandate. The entire safety argument in §6 (the stop can never realize more than the risk already budgeted by the sizing law) depends on the stop level being *exactly* the value Pine emitted, unmodified.
- **Treating a clean Phase 0 pass as license to arm immediately.** Phase 0 is two isolated test fires on the real account (not a demo/paper environment — see §2 Scope), not the N-fill validation window §4 actually requires. The standing B6-style discipline — dry-fire before arm — still applies in full: §7 Phase 2 requires observing the actual computed payload text in `dry_run=true` on the live rail before any armed session relies on this.
- **Reading the 2026-07-23 execution-quality note's "rail sends order_type=market/tif=day/no SL/TP" as a forbidding ruling this ADR overrides.** That note is a factual description of current behavior, reasoning entirely about **entry order type** (market vs. limit) — it never addresses whether a protective stop should be attached, and its "KEEP MARKET ORDERS" recommendation is untouched by this ADR (the entry itself stays a market order; only a stop-loss bracket rides alongside it). This ADR extends territory that note never reached; it does not contradict it.
- **Silently loosening §4's revert trigger 1 (the Phase 0 gate) if the SIM test is inconvenient to run or ambiguous.** If Phase 0 cannot be cleanly executed or interpreted, the correct move is to say so and hold `Proposed`, not to proceed on a partial or ambiguous result.

---

## §6 — Consequences

**Outcome states this ADR can land in** (mirrors §4's falsifier in Accepted/Proposed/reverted terms): **RESOLVED** — Phase 0 passes, the N-fill observation window (§4) shows zero incidents, operator accepts; status moves to `Accepted` and the mechanism stands as a permanent feature. **FALSIFIED** — Phase 0 fails, or any single live incident fires (§4 triggers 1-2); immediate one-line revert, status moves to `Withdrawn` or a superseding ADR is authored for a redesigned mechanism. **AMBIGUOUS** — Phase 0 passes but CrossTrade support (§7 Phase 0b) cannot corroborate, or the N-fill window is inconclusive; status stays `Proposed` pending further evidence, no arming proceeds either way.

**Positive consequences:**
- Closes the exact gap the 2026-07-24→07-28 incident exposed: a silently dead signal path with an open position today has zero broker-side protection until the 16:45 ET auto-flatten (a many-hours window); with this mechanism, the same failure caps exposure at the position's own initial ATR stop distance.
- Costs nothing against modeled edge in the base case: the stop level equals exactly the distance the sizing law already budgeted (`risk_dollars = E_firm × r_eff`, `per_contract = stop_dist_pts × dollars_per_pt`, §0 citation) — if it fires in the failure-path scenario, it realizes a loss no larger than what position sizing already assumed, never a surprise magnitude.
- Mechanically minimal: reuses an already-built, payload-correct field (`sl=` in `build_crosstrade_payload`) and a computation from data the listener already receives (`payload["close"]`, `payload["stop_dist_pts"]`) — no sizing-host change, no new state file, no new external dependency.
- One-line revert path if falsified (§4) — the design was deliberately kept this simple specifically so it stays cheaply reversible.

**Negative consequences (real, not theatrical):**
- Introduces a new unverified surface: a broker-side order the rail does not directly control after submission. If cross-command cancellation does not work as hoped, a normal healthy-path Pine exit could leave an orphaned resting stop — which itself then carries the "fires while flat" risk the public documentation left unanswered. This is precisely why §7 Phase 0 is mandatory-before-any-code, not optional diligence.
- New telemetry blind spot: a stop fill is an event the rail did not initiate. Today's `request_received` → `decision` → `transport_result` triad only captures rail-initiated actions; a disaster-stop fill would be invisible to the ledger until the next reconciliation pass. Mitigated (not eliminated) by logging a `protective_stop_placed` event at attach-time (§7 Phase 1b) — the attempt is on record even though the eventual fill, if any, is broker-side.
- Reduced fidelity to the panel basis in the tail case: if the stop fires, the realized exit is not the panel's modeled exit (a Pine-managed close, possibly at a trailed level) — it is a wider, cruder fill. Accepted because the counterfactual (no protection at all) is strictly worse, not because this is fidelity-neutral; do not cite a disaster-stop fill as if it were a normal panel-basis comparison point in future execution-quality measurement (P1/P2 of the 2026-07-24 plan should tag and exclude these, not average them in).

**Risks (probabilistic, distinct from the costs above):**
- Low-probability, high-severity tail: an undocumented Tradovate/CrossTrade edge case (order-type interaction, account-state timing, a bug) causes the stop to misbehave in a way Phase 0's necessarily-limited SIM testing doesn't happen to exercise. Mitigated, not eliminated, by the dry-fire-before-arm discipline (§7 Phase 2) and the N-fill observation window (§4) before treating it as validated.
- BE/trail staleness: if either venue edition uses break-even or trailing-stop logic (unconfirmed this session — Pine source is gitignored per the repo's public-clone posture, and no citation this session's reads reached confirms or denies BE/trail presence on these two editions specifically), a live-managed stop could sit materially tighter than the static entry-time ATR distance this design uses. In the failure-path scenario, this means the disaster stop caps loss at the *initial* risk budget, not at whatever tighter level a trail would have reached — a real but bounded degradation, and never worse than today's zero-protection state.

**Downstream artifacts that need updating (only once Accepted, per §7):**
- [`c1-rail` SKILL.md](../../.claude/skills/c1-rail/SKILL.md) — file map gains this design's touched files; safety invariants section gains the base-only-stop-loss fact.
- [`docs/notes/rail_build/RUNBOOK.md`](../notes/rail_build/RUNBOOK.md) §B8 — **DONE 2026-07-28**, same session (procedure for §7 Phase 0, cross-referenced from there). A Phase 1 build step remains owed once Phase 0 passes.
- `STATE.md` — pointer-log line at operator decision time (this ADR does not add one itself; per this repo's convention, the pointer line records the *decision*, authored after the operator acts, not at proposal time).

---

## §7 — Implementation plan

**Phase 0 — Empirical verification (blocking; no Phase 1 work starts before this passes). Procedure: [`RUNBOOK.md` §B8](../notes/rail_build/RUNBOOK.md) — written 2026-07-28, this is now the authoritative step-by-step; the summary below should not drift from it.**
- **0a.** Fires on the **real** Tradeify eval account — CrossTrade has no separate paper-trading destination for `destination=tradovate`. Same account (no new subscription) as the 2026-07-20 controlled one-shot (−$[redacted]) and the 2026-07-27 `CHAIN_OK` run (+$[redacted]); quantity held to the account minimum on both fires to bound cost to that same small class (in-eval P&L, not cash spend, per the 2026-07-19 convention — does not count against the $700 ceiling, but is real money and needs the same attended posture as any other armed-adjacent action). Procedure: place an entry order carrying `stop_loss=`, then send a *separate* `closeposition` command against the same position (mirroring exactly the two-command pattern Pine's real exit uses via this rail). Observe directly whether the resting stop auto-cancels — this is the single go/no-go gate named in §4's revert trigger 1. RUNBOOK §B8's optional Test 2 (letting a tightly-set stop fire naturally) corroborates fill mechanics but is not required to close this gate.
- **0b.** In parallel (corroborating, not blocking 0a): ask CrossTrade support the two questions public documentation left open (§0) — cross-command cancellation behavior, and fire-while-flat behavior — for a second, independent confirmation.
- **0c.** Cheap, mechanical: run `python scripts/check_pine_manifest.py` to confirm the PORT_MANIFEST pins are current (§0 flags the `fd91f37b…` MYM citation as a superseded snapshot) before trusting any Pine-internals detail beyond what the rail's own payload contract already validates.

**Phase 1 — Implementation (only after 0a passes):**
- **1a.** In `c1_rail_listener.py::handle_signal`, for `signal_type == "entry"` when `not decision.halt and decision.submit`: compute `stop_price = payload["close"] - payload["stop_dist_pts"]` (long-only book — verify the sign convention against one worked example, e.g. the frozen spec's own worked check, `close` minus `stop_dist_pts` for a long stop below entry, before landing) and pass `sl=stop_price` into the existing `build_crosstrade_payload` call.
- **1b.** Add a `protective_stop_placed` event type to `c1_rail_telemetry.py`'s `EventLedger`, appended alongside the existing pre-send `decision` event for entry signals, so the attach attempt is durably on record.
- **1c.** Test coverage in `tests/ops/` and `tests/rail_crosstrade/` for the new `sl=` wiring — `tests/rail_crosstrade/fixtures.py` already defines `sl`/`tp` fields on its golden-path fixtures (§0), so producer-side test scaffolding may already partially exist and should be checked before writing new fixtures from scratch.

**Phase 2 — Dry-fire (mirrors the GO ADR's B6 discipline):**
- **2a.** One full armed-but-`dry_run=true` session: confirm the computed payload text carries the correct `stop_loss=` value at the correct price for a real incoming signal, matching a hand-computed expectation.

**Phase 3 — First live-armed observation:**
- **3a.** First live session with the mechanism active: explicit operator confirmation that the bracket appears on the Tradovate/CrossTrade dashboard immediately after entry, exactly as attached.
- **3b.** Accumulate ~10 base-entry fills with the mechanism active (§4) before treating it as a validated standing feature.

---

## §10 — Audit hooks (runnable)

```bash
# The unused sl/tp payload fields this ADR proposes wiring — confirm still present as of any re-check
grep -n "sl: float | None" ops/c1_rail/crosstrade_payload.py
grep -n "stop_loss={sl}" ops/c1_rail/crosstrade_payload.py

# Pre-implementation state check: listener must NOT yet pass sl= (expect this to flip once Phase 1 lands —
# re-run after Phase 1 and expect the opposite: a match)
grep -n "sl=" ops/c1_rail/c1_rail_listener.py || echo "not yet wired, as expected pre-Phase-1"

# Pine's own stop-distance computation this design relies on (frozen spec citation must still read this way)
grep -n "stopDist = atrVal" docs/spec/c1_watch_realization_multiplier_layer.md

# This ADR must not silently contradict the sizing-host spec's exit-scope line — re-read §1's argument
# against this line at any future amendment
grep -n "does not manage exits" docs/spec/c1_nt8_sizing_host_impl.md

# GO ADR forbidden-move precedent this design extends (single-exit-path insufficiency doctrine)
grep -n "neither the CrossTrade Account Manager nor the operator" docs/adr/2026-07-17-c1-rail-build-account-registration-go.md

# No prior rejection of this mechanism (checked at authoring time; re-check before Phase 1 in case
# something was rejected in the interim)
grep -in "disaster.stop\|dead.man\|resting.stop.*bracket" docs/rejected_candidates.md || echo "none found, as expected"

# Phase 0 gate must be recorded before Phase 1 code exists — expect no sl= wiring in the listener
# until a Phase-0 result (pass/fail) is recorded somewhere in docs/notes/rail_build/ or this ADR's
# change history
grep -rn "Phase 0" docs/adr/2026-07-28-c1-disaster-stop-payload-supported.md
```

---

## Verification

```bash
# Discipline checks (mechanical) — repo-side MECHANICAL SUBSET.
# ⚠ CORRECTED 2026-08-09: this block previously called the repo-root copy
# "canonical". It is not, and never was — scripts/check_brief.py's own docstring
# names the SKILL-SIDE checker canonical, and skill-side is the one that
# self-tests its templates. Ruled in docs/adr/2026-08-09-check-brief-canon-ruling.md.
# The repo-root copy stays useful (VC-tracked, resolves in a public clone) but a
# pass here is not a discipline pass.
python scripts/check_brief.py docs/adr/2026-07-28-c1-disaster-stop-payload-supported.md --type adr

# Production-source verification (Rule 0 confirmation) — re-run the §0 anchors
git log -1 --format='%h %cs' -- ops/c1_rail/c1_sizing_host_reference.py    # expect c134060 2026-07-24
git log -1 --format='%h %cs' -- ops/c1_rail/crosstrade_payload.py          # expect 54b1489 2026-07-23
git log -1 --format='%h %cs' -- ops/c1_rail/c1_rail_listener.py            # expect 5fa31b5 2026-07-27

# Cross-reference: sl/tp fields exist in the payload builder as cited
grep -n "sl: float | None = None, tp: float | None = None" ops/c1_rail/crosstrade_payload.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-28 | Initial authoring (brainstorm item C2); Phase 0 (§7) not yet run; operator decision pending | Joshua (pending) + Claude Code |
| 2026-07-28 | Correction: §2 Scope, §5, and §7 Phase 0a wrongly implied Phase 0 runs on a free/demo "SIM environment." Corrected — Phase 0 fires on the real Tradeify eval account (same class as the 2026-07-20 −$[redacted] and 2026-07-27 +$[redacted] precedents), cost-bounded by account-minimum quantity, in-eval P&L not counted against the $700 ceiling per standing convention. §7 Phase 0a now points to [`RUNBOOK.md` §B8](../notes/rail_build/RUNBOOK.md) (written same session) as the authoritative procedure. No change to §2 Decision, §4 Falsifier, or §5/§6 substance beyond this wording fix. | Joshua (flagged) + Claude Code (correction) |
| 2026-08-22 | **Operator Accept.** Status `Proposed` → `Accepted`. Decision GO recorded. §7 Phase 0 empirical SIM remains the implementation gate; no `sl=` listener wiring and no arming land with this flip. | Joshua (GO) + Cursor (record) |
