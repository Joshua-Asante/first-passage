---
name: prop-firm-challenge
description: Use this skill for firm/venue rules, portfolio MC, dd_protection, lifecycle sizing, broker CSV P&L analysis, or ops questions about Guardian/Striker/Aegis/NAS100 — including dormant FXIFY/Bulenox configs in core/firm_rules.py, self-funded Aegis→M6J scale-path work, MNQ/MYM/MGC, trailing-DD/eval/consistency rules, or c1 rail sizing questions. Triggers on strategy parameters in an ops (not Pine) context, uploaded broker CSVs, drawdown/P&L, or firm-tier questions. Live prop challenges are closed; live execution questions route to the `c1-rail` skill. This skill is durable ops + historical challenge-era reference — use pinescript-v6 for strategy-code work.
---

# Prop Firm / Portfolio Operations

Operational context for Joshua's locked 4-strategy book (Guardian v5.5, Striker DJ30 v4.5, Aegis v4.3, Striker NAS100 v1 — parameter-axis LOCKED) under firm rules from `core/firm_rules.py`. Firm-specific numbers are never hardcoded here; read the file.

## Posture — not owned here (rewritten 2026-08-08)

**Rail posture is NOT restated in this file.** Read it from
[`CLAUDE.md` §Live-execution posture](../../../CLAUDE.md) and the
[`c1-rail` skill](../c1-rail/SKILL.md), which are the owners.

The block that stood here was stamped 2026-07-24 and had gone wrong on three counts while still
carrying a "verify against CLAUDE.md" caveat — a caveat is not a substitute for being right, and a
paragraph a same-day PR edits without fixing is a *maintained* surface, not an acknowledged-stale one.
For the record, what it got wrong: the signal origin (**S2 ruled it Python-native**, not TV — Pine/TV is
research/export only); the arm-gate object (**Addendum 2026-07-31b moved the trigger send → ARM**, so
`dry_run=false` may not be *set* while M1 is not `RESOLVED`); and deployability (**2026-08-04 withdrew
both Striker legs**, so there is no deployed strategy and nothing to arm).

**Durable here (ops routing, not a second owner of decision narrative):**

- Live tier key: explicit `Tradeify_Select_100K` (`ACTIVE_FIRM` deleted — substrate Phase 4).
- Eval geometry: no drawdown lock in eval for Tradeify/MFFU — owner
  [`§4 withdrawal ADR`](../../../docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)
  (bust%/clearer counts, rider FAIL, hard date **not restated here**).
- Cap allocation / flat deadline / hedging Product-Group facts — owner
  [`GO ADR` Addendum 2026-07-22](../../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md)
  (per-leg shares live in `ops/c1_rail` constants / that ADR — not here).
- WATCH-1 measurement / B7 inputs — owner GO ADR + lab RESULTS under `lab/analysis/c1/`
  (do not restate panel bust cells here).
- ⚠ Bust/DD figures anywhere in this skill are **EOD-clock lower bounds** pending
  [`W1 ADR`](../../../docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md).
- Self-funded scale CLOSED/parked —
  [`2026-07-16`](../../../docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md);
  manual CFD + FXIFY closed; historical MC pins `FIRM_RULES["FXIFY"]` **by name**
  ([`substrate`](../../../docs/adr/2026-07-22-challenge-era-substrate-retirement.md)).
- **Arming / fills / disarm → `c1-rail` skill + RUNBOOK §B7.** Live sizing path:
  `BASE_RISK × DD_SCALE × lifecycle` with integer-qty flooring in
  `ops/c1_rail/c1_sizing_host_reference.py` (continuous-lot spine deleted).

This skill documents durable mechanics (firm rules, sizing, protection, MC) for historical challenge-era work and any future firm re-open (R6 ADR §4). It is **not** a claim that a prop challenge is running.

**Source-of-truth hierarchy (Notion retired 2026-06-12 — `docs/governance/notion-redirect-map.md`):** the **repo is canonical** — Pine source for strategy code; `core/firm_rules.py` / `core/dd_protection.py` / `core/lifecycle.py` for live-sizing & risk constants; `core/strategies/CATALOG.md` (index) → `core/strategies/_archive/<family>/LOCK.md` for lock records (family dirs `core/strategies/<family>/` retain `CARD.md` stubs only since the 2026-08-04 Phase-A cold-store move — a `LOCK.md` is never there.); `docs/adr/` for decisions. This skill is a secondary operational reference; when it disagrees with those sources, trust them.

---

## Rule 0 — audit-first discipline

Before authoring any decision brief that touches risk controls (dd_protection, lot sizing, account rules, protection tiers), read the production code directly — not memory, not prior docs, not reconstructed specs. Full doctrine: `docs/rule_0.md`. This rule exists because it was violated three times on 2026-04-17, producing a retune → reversal → delete-and-retune cycle that should have been a single decision (root cause each time: authoring the brief from assumed semantics rather than verified code). Full chain: `docs/adr/2026-04-17-dd-trigger-calibration.md` + `docs/adr/2026-04-17-equity-tier-deletion.md`.

Two corollaries specific to this operational domain:

- **Suspect single-rule descriptions of multi-rule systems.** Defensive engineering usually has belt-and-suspenders by design. Any time the system is described as "one rule," go look for the second.
- **Data-source labels are not data-source verification.** A CSV filename or directory path claiming `pepperstone/` (retired) is not evidence the file contains Pepperstone data. Always reconcile CSV trade count + headline metrics against the Pine-header backtest before accepting MC output. See the 2026-04-23 Aegis-on-Alchemy-mislabeled-as-Pepperstone incident for the canonical failure mode.

---

## Firms & challenge rules

`core/firm_rules.py`'s `FIRM_RULES` dict is canonical for every firm's challenge parameters. There is **no** live `ACTIVE_FIRM` switch (deleted Phase 4); c1 uses the explicit tier key `Tradeify_Select_100K`. **Read the file directly for exact values — the table below is a mirror, not a source; if it looks stale, trust the file.**

**Fields, generically:**

| Field | Meaning |
|---|---|
| `dd_type` | `"static"` (drawdown measured from the starting balance, never moves) or `"trailing"` (drawdown ratchets up with equity, real-time or EOD depending on venue) |
| `max_dd_pct` | Max drawdown allowed before bust, as % of the relevant basis for that `dd_type` |
| `daily_loss_pct` | Max single-day loss before bust; `None` where the firm has no daily-loss rule |
| `profit_target_pct` | % gain required to pass |
| `min_trading_days` | Minimum distinct trading days before a pass counts |
| `weekend_holds` | Whether positions may carry over a weekend (`False` on force-flat/no-overnight venues) |
| `inactivity_max_idle_days` | Consecutive no-progress days before the account is flagged/failed |
| `micro_contract_cap` | Futures-only: max micro contracts per position, this tier |
| `cost_per_side_usd` | Futures-only: all-in commission per contract per side |

**Snapshot (verify against `core/firm_rules.py` directly before relying on this):**

| Firm / tier | `dd_type` | `max_dd_pct` | Target | Daily loss | Min days | Micro cap |
|---|---|---|---|---|---|---|
| FXIFY (HISTORICAL fixture; pin by name) | static | 5.0% | 5.0% | 5.0% | 5 | — |
| Bulenox_25K | trailing | 6.0% | 6.0% | none | 0 | 30 |
| Bulenox_50K | trailing | 5.0% | 6.0% | none | 0 | 70 |
| Bulenox_100K | trailing | 3.0% | 6.0% | none | 0 | 120 |
| Bulenox_150K | trailing | 3.0% | 6.0% | none | 0 | 150 |
| Bulenox_250K | trailing | 2.2% | 6.0% | none | 0 | 250 |

FXIFY (historical): DXTrade via Alchemy Markets (CFD) — venue closed. Bulenox tiers force-flatten EOD (no overnight/weekend carry), no daily-loss limit — bust mode is 100% trailing-DD. Bulenox configs remain in `firm_rules.py` for simulation provenance; **no account registered; futures-prop NO-GO**.

**Onboarding a new firm:** add its config to `FIRM_RULES`, then run an **engine-support pre-flight** (many firms have `daily_loss_pct: None` and need bespoke bust branches — see CLAUDE.md Firm Expansion + challenge-era rescope ADR). If the execution feed differs from the locked MC's Pepperstone calibration feed, also run the feed-equivalence pre-flight (`docs/spec/feed_equivalence_discovery_test_LOCKED.md`) before re-MC against that firm's tier key.

---

## Portfolio Configuration

### Locked allocations (challenge = funded phase; no re-sizing at pass)

**Not restated here (Rule 7).** Human-readable lock table + versions: [`CLAUDE.md`](../../../CLAUDE.md) §Strategy Reference. Live sizing authority: `core/firm_rules.py` `_BASE_RISK` / `core/dd_protection.py` `BASE_RISK`. Per-strategy mechanics (session/hour filters, SL/TP structure): [`references/strategy_reference.md`](references/strategy_reference.md) (Pine remains source of truth for parameters).

Bust attribution under the historical Pepperstone calibration is record-only — `docs/mc_anchor_history.md` (tombstone via `git show pre-prune-2026-08-08:docs/ltm/notes/2026-07-24-pepperstone-executable-anchor-tombstone.md`). Engine regression: `tests/core/test_mc_synthetic_engine.py`.

### Guardian risk lock (no ramp / no overlays)

No funded-phase ramp, no active overlays — challenge and funded phase run identical parameters. Exact risk% lives with the owners above. Prior conditional overlay concepts (equity-ramp ladder, Iran-Israel/Hormuz conflict overlay, regime-indexed sizing) are retired; historical record preserved at git tag `pre-prune-2026-06-05` (retrieve: `git show pre-prune-2026-06-05:archive/docs/methodology/archive/overlays/guardian_conflict_risk.md`).

**Rationale (locked lesson):** the strategies are inherently regime-adaptive — Guardian's EMA slope, Striker's breakout-distance thresholds, and Aegis's BB+ATR gates already respond to volatility regime, trend strength, and range expansion. Overlays bolted on top double-adjust what the base strategy already captures. Don't reintroduce without a fresh INQHIORI loop demonstrating the base logic is demonstrably insufficient.

### Binary macro events — Aegis pause rule

For known binary volatility events (central-bank decisions, major scheduled geopolitical releases), Aegis is paused for the session — mean-reversion edge inverts on binary regime breaks. Not a general news filter; applies only to pre-scheduled binary-outcome events. Generic FOMC/NFP/CPI days are NOT binary-event pauses — those are handled by each strategy's existing session/hour filters. Guardian and Striker continue normal operation unless independently flagged.

Aegis's live instrument is venue-dependent: USDJPY on CFD venues (locked v4.3); a CME 6J synthetic-spot-inversion prototype exists for futures venues but is **non-canonical** (see `project_aegis_6j_transfer_state` project memory) — do not treat it as a drop-in replacement without re-checking that record.

---

## Protection system

Single-tier internal drawdown overlay, independent of whichever firm's own DD rule applies. **Literals and logic are not restated here** — read [`core/dd_protection.py`](../../../core/dd_protection.py) and the human summary in [`CLAUDE.md`](../../../CLAUDE.md) §Protection. Decision lineage: [`C2 relock`](../../../docs/adr/2026-05-08-dd-trigger-c2-relock.md) · [`equity-tier deletion`](../../../docs/adr/2026-04-17-equity-tier-deletion.md) · [`concept-not-constant`](../../../docs/adr/2026-07-13-dd-protection-concept-not-constant.md).

**This overlay sits on top of, not instead of, the active firm's own DD rule.** A static-DD firm and a trailing-DD firm bust differently underneath this same overlay — MC modeling must thread the active firm's `dd_type` through (`core/portfolio_mc.py`'s `bust_trailing` vs `bust_static`/`bust_daily` outcomes), not assume one firm's semantics apply everywhere.

### Re-MC triggers

- 6 months live data accumulated
- Any strategy version bump (material strategy change) — re-MC before locking
- Any allocation change beyond the documented Guardian safe band (see CLAUDE.md Strategy Reference / owning lock ADRs)
- Any `dd_protection` constant change
- Any firm/venue switch (new explicit tier key) or new firm onboarded

### Revert triggers for a second protection tier

Reintroduce only if: (1) single-tier DD-only fails to hold bust below the programme's live bust bar at any future portfolio mix change; (2) a specific tail failure emerges that DD-protection mechanically cannot catch (slow sustained bleed where peak tracks equity down); (3) allocation shifts push a high-risk leg above its locked band or add a fourth strategy with correlated tail. If any fire, the new tier must be MC-validated against **live code semantics** (not assumed semantics) from day one.

---

## Position sizing by venue

Sizing mechanics differ by venue type; both funnel through `ops/c1_rail/c1_sizing_host_reference.py` (live integer-qty rail; the continuous-lot multiplier spine is deleted — see CLAUDE.md "Multiplier System (RETIRED)").

### CFD venues (e.g. FXIFY/DXTrade) — HISTORICAL / DORMANT

Manual CFD execution and the FXIFY venue are **retired**. The table below is retained only as historical DXTrade contractValue provenance (Rule 3 safety fact). **Live sizing is the c1 integer-qty rail** (`ops/c1_rail/c1_sizing_host_reference.py`); do not execute FIRE→lots from this section.

Lot size historically scaled via a `contractValue` multiplier per instrument:

| Instrument | 1 Lot = | contractValue | Notes |
|---|---|---|---|
| XAUUSD | 100 oz | 100 | Direct match |
| USDJPY | 100K units | Default (1) | Direct match |
| DJ30 | 10 × index | **10** | MUST SET — default of 1 is 10× wrong. VERIFIED 2026-04-23. |
| NAS100 | 10 × index | **10** | MUST SET — default of 1 is 10× wrong. CONFIRMED 2026-05-05. |

**Historical desk sanity check (not a live action set)** — when reading old FIRE/DXTrade artifacts, lot sizes outside these ranges usually meant wrong ATR/risk% or `contractValue = 1`:

- Guardian lot size > 5 → probably wrong ATR or risk%
- Striker DJ30 lot size > 7 → probably contractValue = 1 instead of 10
- Striker NAS100 lot size > 4 → probably contractValue = 1 instead of 10
- Aegis lot size > 25 → probably wrong ATR
- Any trade risking > 2% of account on a single position

### Futures venues (e.g. Bulenox CME micros)

Sizing is **integer contract count**, not a continuous multiplier — this is the structural difference from CFD sizing:

- Position size = `floor(target_risk_$ / (stop_distance × tick_value))`, capped by the tier's `micro_contract_cap`.
- **Granularity floor**: the account balance below which a strategy's intended risk rounds to 0 contracts. Single-position strategies (Guardian) are granularity-*tolerant* (integer rounding only quantizes size uniformly). Pyramided strategies (Striker DJ30/NAS100) are granularity-*fragile* — a pyramid leg rounding to 0 breaks the edge structure, not just the size. Derive floors per `lab/analysis/legacy/futures_conversion_2026-07-01/derive_floors.py`'s pattern before sizing a pyramided strategy on a small account.
- **RESERVE cap rule** for pyramided strategies: base position size must be capped at `floor(account_cap / (1 + pyramid_pct))` so the pyramid add-on never gets starved of headroom by an oversized base — where `account_cap` is **this leg's allocated share** when several legs share one account-aggregate cap (Tradeify counts the limit across the whole account; per-leg shares live in the GO ADR Addendum 2026-07-22 / `c1_sizing_host_reference` constants — **not restated here**). Applying the **whole** account cap per leg over-counts. A missing per-leg allocation must **HALT**, never fall back to the account cap — `ops/c1_rail/c1_sizing_host_reference.py`.
- Contract specs (tick value, commission) are NOT the CFD `contractValue` table above — re-derive per instrument (MNQ/MYM/MGC/6J) from the venue's own contract specs, never reuse CFD numbers.

---

## Futures-venue mechanics

Pointer-heavy — these are the load-bearing differences from CFD operation, each gated by its own artifact rather than a fixed number restated here:

- **Trailing vs static DD, and EOD vs real-time.** A firm's trailing DD may ratchet in real time (Bulenox "Option 1") or only at end-of-day ("Option 2" / MFFU / Tradeify-style EOD-lock) — these are materially different risk profiles, not interchangeable. `core/portfolio_mc.py`'s `bust_trailing` currently models %-of-peak, EOD — confirm which real-time/EOD semantic the target firm actually uses before trusting a re-MC's bust rate.
- **Force-flat / no overnight.** Futures-prop venues typically force-flatten before session close — no overnight or weekend carry. Strategies with multi-day holds (Guardian) do not fit a force-flat venue as-is; see `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` and the futures-pivot project memory for the venue-fit determination per strategy.
- **Consistency + inactivity rules.** Most futures-prop firms require profit concentration below some % of total (a "consistency rule," typically since-inception-cumulative on funded accounts, not per-payout-window) and a minimum trading cadence (an "inactivity rule," e.g. Bulenox's ≥1 trade per 5 trading days). A strategy that goes quiet past the inactivity window needs a scheduled token-micro-trade mitigation at the execution layer — this is NOT optional if the strategy's natural trade cadence can exceed the window.
- **Eval economics.** Futures-prop evals are typically cheap-retry (a failed eval costs a modest monthly fee, re-purchasable) vs FXIFY's one-shot challenge purchase. This changes which bust-rate gate is appropriate — a 1% bust gate calibrated for a one-shot purchase may be needlessly conservative for a cheap-retry eval. Gate provenance (which economic model a bust-rate threshold assumes) must be pre-registered before reading results against it, not chosen after seeing the numbers.
- **Venue-transfer gates.** A strategy locked and backtested on one feed/venue does not automatically transfer its edge to a new feed/venue — treat every venue switch as a gated hypothesis, not a free port. Run the feed-equivalence pre-flight (`docs/spec/feed_equivalence_discovery_test_LOCKED.md`) before trusting a locked MC on a new feed. the P2 edge-transfer gate is the worked example (tombstoned 2026-08-08; body via `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md`): a two-sided gate that FALSIFIED on the as-mapped CME-micro venue for two of the four strategies (structural under-firing). The R5 DJ30→MYM successor also FALSIFIED (2026-07-09); residual futures-**prop** program closed at R6 NO-GO — see `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` and historical brief via `git show pre-prune-2026-08-08:docs/ltm/briefs/futures_residual_program_2026-07-05.md`.

---

## Strategy trading schedule

Which days/hours each strategy trades is a Pine session-filter property of the strategy itself, not of whichever firm hosts it — this table holds regardless of venue:

| Day | Strategies | Session Times (EST) |
|---|---|---|
| Monday | Guardian + Aegis + NAS100 | G: 8–16, A: 10–13:45, N: 8–12 |
| Tuesday | ALL FOUR | G: 8–16, S(DJ30): 8–12, N(NAS100): 8–12, A: 10–13:45 |
| Wednesday | Aegis only | A: 10–13:45 |
| Thursday | Guardian only | G: 8–16 |
| Friday | Striker DJ30 only | S: 8–12 |

All sessions are morning NY time by design (fits before Joshua's day-job hours).

---

## Alert semantics

**Live path:** strategy entry/exit webhooks on the **c1 rail** (`c1-rail` skill + `ops/c1_rail/crosstrade_payload.py`). Attended arming, M1, `armed_until`, and disarm rules live there — not in a manual FIRE desk loop.

**HISTORICAL / DORMANT (manual CFD desk):** Indicator + Anticipation scripts used a SETUP / PROXIMITY / FIRE / MISS state machine; only FIRE meant "execute." That action set is retired with manual trading. Informational alerts may still exist on charts; they are **not** an authorization to size or send orders outside the c1 rail.

---

## Performance analysis workflow (live P&L)

When Joshua uploads a broker CSV export (DXTrade, Tradovate/Bulenox, or any other execution broker):

1. Parse trade history (entry/exit pairs by Trade #)
2. Calculate: WR, PF, avg win/loss, max DD, daily P&L, cumulative equity
3. Compare against per-strategy backtest baselines (`references/strategy_reference.md` → `trade-csv-reconcile/references/baselines.md`)
4. Flag deviations: WR, PF, or DD outside expected ranges
5. Project days remaining to the active firm's profit target at current pace (`profit_target_pct` from `core/firm_rules.py`)
6. Check if the active firm's daily-loss limit (if any) was approached

Keep this tool SEPARATE from portfolio MC. Live P&L analysis is backward-looking on broker exports; portfolio MC is forward-looking on TV backtest CSVs. One tool per question.

---

## Portfolio Monte Carlo

Implemented in `core/portfolio_mc.py`. Answers one question: given locked strategies, the active firm's rules, and the current `dd_protection` config, what is the challenge pass/bust distribution?

### When to run

- After any broker CSV export + re-exported TV backtests for the newest bars, if pass/bust drift more than ~1σ from locked expectation (investigate — usually regime change, not strategy breakage)
- Before considering any allocation or parameter change — ALWAYS re-MC before locking
- At any Re-MC trigger (see Protection System section)
- Before onboarding a new firm tier key / re-MC against a new firm

### Methodology (enshrined after 2026-04-17 error; feed-calibration fixed 2026-04-20; Pepperstone re-basis 2026-04-23)

1. **Ingest** the per-strategy TV CSV exports for the panel the run targets. **There is no canonical CFD calibration feed** — Dukascopy retired 2026-06-17, OANDA 2026-06-24, Pepperstone 2026-08-02 (data tombstoned); `core/data/tv_exports/` holds only `cme/`. The live canonical feed is CME futures TV exports. Pair Entry/Exit rows by `Trade #`. ⚠ The CFD-era four-strategy run this methodology was written for is **NOT RUNNABLE** — its panels are gone and `PANELS_BY_BROKER` has been empty since substrate Phase 3; steps 2–8 remain the live engine's algorithm for CME-panel runs.
2. **Pre-MC CSV reconciliation (MANDATORY):** verify each CSV against its Pine-header backtest — trade count, net P&L, PF, DD within 0.5%. Halt if any leg fails. This check exists because a mislabeled CSV silently corrupted a lock run on 2026-04-23 (see Rule 0 corollary above).
3. **Implied 1R per strategy** — Guardian (no BE, pure trend-rider): median loss. Striker DJ30/NAS100 and Aegis (BE exits): mean of `|losses| > 1%` of account (full-stop cohort). Fall back to median ONLY if zero full stops (not `< 5` — that fallback was a trap, fixed 2026-04-23 via commit `bf32aa3`). Thin-cohort warning fires when `1 ≤ n < 5`.
4. **Scale factor** per strategy: `target_risk_pct / implied_risk_pct`, applied to every trade's P&L.
5. **Daily panel**: business-day index, columns = strategies, values = sum of scaled P&L on exit date. Fill missing days with zero.
6. **Week-block bootstrap**: Mon-anchored 5-day non-overlapping blocks, sampled with replacement until horizon filled.
7. **Simulation**: start at the active firm's starting balance, apply daily P&L with `dd_protection` scaling, terminate on PASS, BUST (mode depends on the active firm's `dd_type` — `bust_static`/`bust_daily` for a static-DD firm, `bust_trailing` for a trailing-DD firm), or INACTIVITY (per that firm's `inactivity_max_idle_days`).
8. **Aggregate**: 10K sims × 3 seeds, report mean and σ.

### Locked anchor (FXIFY historical — engine regression pin; not a live pass-probability)

**Literals not restated here (Rule 7).** Read the pin + panel provenance from
[`docs/mc_anchor_history.md`](../../../docs/mc_anchor_history.md) and the gated human headline in
[`CLAUDE.md`](../../../CLAUDE.md) §Strategy Reference (⚠ CLAUDE's three bolded literals are also
parsed by `ops/recall/guard.py` — do not "fix" them in isolation). Engine regression:
`tests/core/test_mc_synthetic_engine.py`. Tombstone (retired executable pin):
`git show pre-prune-2026-08-08:docs/ltm/notes/2026-07-24-pepperstone-executable-anchor-tombstone.md`.
Re-scope: [`2026-07-11`](../../../docs/adr/2026-07-11-challenge-era-claims-rescope.md) — **historical**,
not a live pass-probability.

This pin is FXIFY-rule-shaped (static DD, one-shot eval). A trailing-DD firm's simulation is a
**different** run — do not apply the FXIFY pin to Bulenox or other trailing-DD tiers. Successor
self-funded risk questions need a fresh Pre-Q (hard date per the rescope ADR).

### Known methodology traps

- **Day-of-week patterns from exit_date are misleading for long-hold strategies.** Guardian winners hold ~835 bars on average; exit DOW is effectively random. Segment DOW analysis by entry date for filtering decisions.
- **Standalone strategy MaxDD is not the right sizing input.** Portfolio-level tail contribution matters more — an uncorrelated strategy with low standalone DD can still dominate portfolio variance.
- **Stationarity assumption breaks across regime changes.** Re-run MC after any structural change before trusting the rate.
- **Model actual live protection semantics, not assumed ones.** If `dd_protection.py` uses `min()`, MC must use `min()`. If `*=`, MC must use `*=`. Verify by reading code, not assuming.
- **The `< 5` fallback was a trap** — fixed 2026-04-23 via the `== 0` fallback + thin-cohort warning.
- **File paths are not data provenance.** A CSV at a `pepperstone/` (retired) path is not necessarily Pepperstone data — reconcile trade count + metrics before accepting output (Rule 0 corollary).

---

## Core principles

1. **Trade the system, not your opinion.** Edge comes from 4+ years of tested data, not today's macro read.
2. **No discretionary overrides.** Rule logged from the February override incident on a valid Guardian long that would have been a winner.
3. **Live trades only via the c1 rail under GO + M1.** Historical FIRE/SETUP/PROXIMITY desk semantics are DORMANT — see Alert semantics above.
4. **One trade at a time per strategy.** Aegis max 1/day, Striker respects pyramid rules, Guardian one position.
5. **Respect the schedule.** Wednesday is Aegis only. Thursday is Guardian only. Don't improvise.
6. **Export CSVs weekly** for performance tracking, whichever firm/venue is active.
7. **The portfolio is locked at the parameter axis** — risk% / versions: [`CLAUDE.md`](../../../CLAUDE.md) §Strategy Reference; live authority `core/firm_rules.py` `_BASE_RISK`. Parameter/allocation changes require MC-validated re-locks. Capital **authorization** is a separate revocable axis owned by [`docs/methodology/strategy_lifecycle.md`](../../../docs/methodology/strategy_lifecycle.md) (current tier state lives there / CLAUDE §Strategy Authorization Lifecycle — do not restate here).
8. **Audit-first for risk-control decisions.** Read `dd_protection.py` (and any other production risk file) before authoring any decision brief that touches it.
9. **Headlines drive markets, not physical ground-truth.** No regime overlays built on physical facts. Strategies already adapt to regime through their base signal logic; overlays are redundant. Lesson locked from the Guardian conflict-overlay rejection.
10. **Do not quote challenge-era pass/bust rates as live probabilities.** The MC pin is historical / regression-only until a successor self-funded risk Pre-Q lands.

---

## References

Notion retired 2026-06-12 — canonical homes are in-repo: `docs/adr/` (decisions), `core/strategies/CATALOG.md` (index) → `core/strategies/_archive/<family>/LOCK.md` (locks), `core/firm_rules.py` / `core/dd_protection.py` / `core/lifecycle.py` (live constants). Historical Notion URLs: `docs/governance/notion-redirect-map.md`.

See also: `references/strategy_reference.md` (per-strategy mechanics) and `references/execution_history.md` (historical manual-execution playbook, retired 2026-06-30).

## Related skills

- `pinescript-v6` — strategy code work (Pine scripts, indicators, alerts)
- `trade-csv-reconcile` — verified per-strategy CSV metrics feed into this skill's MC step
- `strategy-validation` — robustness / multiplicity / breadth gates for research candidates
- `handoff-verify` — Phase-0 checks before executing external/advisor handoffs that touch ops posture
