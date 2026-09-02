# Q-FUNNEL-1 — contract-funnel EV analysis

**Status:** `CLOSED — RESOLVED 2026-07-22` — see [`docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md`](../closures/Q-FUNNEL-1-closure-resolved.md)
**Authored:** 2026-07-21
**Closed:** 2026-07-22
**Authors:** Joshua + claude.ai (advisor)
**Parent question:** N/A — forked from a design doc, not a prior Q
**Sub-questions opened:** N/A
**Loop:** Inquire-phase Pre-Q — gates whether the deferred cushion-proportional policy layer (design doc §7) gets built
**Artifact path:** `docs/briefs/rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md`
**Design doc:** [`docs/superpowers/specs/2026-07-21-q-funnel-1-contract-ev-design.md`](../../superpowers/specs/2026-07-21-q-funnel-1-contract-ev-design.md) — approved (brainstorming), this brief is its landing-sequence step 2
**Results:** [`lab/archive/q_funnel_1_2026-07/RESULTS.md`](../../../lab/archive/q_funnel_1_2026-07/RESULTS.md) · [`docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md`](../closures/Q-FUNNEL-1-closure-resolved.md) — funnel EV materially prefers the 1.00× rung over the ratified WATCH-1 0.50× at 4 of 6 (edge, retry-policy) grid points, all favoring 1.00×; but the closure's own caveat flags half that evidence (`edge_half_panel`) as horizon-fragile — it reverses sign in H1 at a 126-day funded horizon, vs the delivered 252-day default. Only `edge_panel_historical` is horizon-robust across {126,252,504}.
**Operator disposition:** [`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`](../../adr/2026-07-23-c1-rung-selection-ev-objective.md) — operator elected fork B (EV objective) but, once the both-halves regime gate is enforced, 1.00× is regime-inadmissible, so EV and the bust-floor converge on keeping 0.50×; live rung stayed WATCH-1 0.50× despite this brief's EV finding. Per current `CLAUDE.md` live-execution posture, there is no live c1 book as of 2026-08-04 (both Striker legs withdrawn) — this rung-selection question is now moot for the withdrawn book and would need re-measurement for any successor venue.

---

## §0 — Rule 0 reads (production-source verification)

Files read before authoring this brief and the upstream design doc, verified 2026-07-21:

- [`core/firm_rules.py`](../../../core/firm_rules.py) — `a53ee99` (2026-07-13). `Tradeify_Select_100K`: `dd_type="trailing_locking"`, `max_dd_pct=3.0` ($3,000), `dd_lock_offset_usd=100`, `daily_loss_pct=None`, `profit_target_pct=6.0`, `min_trading_days=3`, `consistency_rule_pct=40.0`. No fee, subscription, payout-split, or payout-minimum fields exist anywhere in the file.
- [`core/mc/simulation.py`](../../../core/mc/simulation.py) — `a53ee99` (2026-07-13). `simulate_path`: daily-resolution loop; `trailing_locking` floor `= min(peak - max_dd_usd, starting_equity + dd_lock_offset_usd)`; consistency clause is a soft keep-trading gate, never an absorbing barrier; the loop terminates the path at `pass` — no funded-phase state, no fee, no payout event exists past that point.
- [`core/mc/preflight.py`](../../../core/mc/preflight.py) — `a53ee99` (2026-07-13). `firm_kwargs` threads `trailing_dd_pct`/`dd_lock_offset_usd` into the sim; `summarize_outcomes` partitions `pass | bust_daily | bust_static | bust_trailing | bust_inactivity | horizon_cap`; no days-to-pass or EV field is emitted by default.
- [`core/dd_geometry.py`](../../../core/dd_geometry.py) — `85f883b` (2026-07-13). `POLICY_REGISTRY` holds `(portfolio, firm-tier) -> (trigger, scale, reference_mode)`; admission requires pre-registered re-MC + both-halves regime gate + admitting ADR; no runtime registration API. Only `FXIFY-C2` is registered; no `c1@Tradeify_Select_100K` row exists.
- [`docs/adr/2026-07-13-dd-protection-concept-not-constant.md`](../../adr/2026-07-13-dd-protection-concept-not-constant.md) — `ba943a1` (2026-07-17). "Numbers-before-question stays forbidden" — the objective-before-numbers pattern this brief's §8 pre-registration must follow.
- [`docs/adr/2026-07-17-c1-rail-build-account-registration-go.md`](../../adr/2026-07-17-c1-rail-build-account-registration-go.md) — `1ec003f` (2026-07-19). c1 book = Striker DJ30→MYM + Striker NAS100→MNQ on one Tradeify Select 100K eval, WATCH-1 0.50× realized at the rail's account-multiplier layer; §6 states WATCH-1's pass-rate "is bust-geometry, not a P&L promise."
- [`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md`](../../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md) — `d85c10c` (2026-07-17). WATCH-1 0.50×: full-panel bust 0.08%, bootstrap-95th bust 0.77%, pass-5th 95.76%. Median-days-to-pass **not reported** (documented §8 Phase-0 deviation); ratification notes it "roughly doubles" vs 1.00× qualitatively only. Day-level policy: none modeled (uniform ×0.5 scalar on `daily_100k`).
- [`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md`](../../../lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md) — `eba5030` (2026-07-11). Line-58-adjacent blocker note: "bust<1% gate is FXIFY one-shot economics; Tradeify cheap-retry may warrant a different EV gate" — named, not built.
- [`docs/briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md`](../../briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md) — `fad8984` (2026-07-14). §3.4 explicitly defers the "retry-EV objective" as 11-08 D1 material; ratified gate is bust≤3.0% AND P(pass)≥50% at the $100K band — a bust/pass gate, not an EV gate.
- [`lab/analysis/regime/regime_stress_2026-06-15/oracle_test.md`](../../../lab/analysis/regime/regime_stress_2026-06-15/oracle_test.md) — `b7841ef` (2026-06-22). Perfect-foresight regime-*resizing* ORACLE FAIL ("drift problem, you cannot detect your way out"). Scope note carried into §5 below: this killed regime-conditional resizing on detectability grounds, an unrelated failure mode to contract-state-conditioned policy (own equity/floor/day-count are directly observable, not inferred).
- [`docs/rejected_candidates.md`](../../rejected_candidates.md) — `d4a2070` (2026-07-21) and [`docs/methodology/rejected_signals.md`](../../methodology/rejected_signals.md) — `7c864aa` (2026-06-04). Neither contains an entry rejecting policy/funnel-layer optimization, retry-EV objectives, or pass-banking/day-quit rules as a direction.
- [`docs/methodology/regime_robustness_gate.md`](../../methodology/regime_robustness_gate.md) — `f2be990` (2026-07-11). Mandatory both-halves gate for any new `dd_protection`-class risk constant; binds if this study's findings ever feed a new `dd_geometry` instance (design doc §7, deferred).

External sources (verified 2026-07-21 via a 103-agent adversarial deep-research pass, `Workflow` run `wf_031aa3bf-c87`, 22/25 claims confirmed 3-0 or 2-1 against primary sources): Tradeify Select Evaluation help article (`help.tradeify.co/.../12853921`, June 2026), Tradeify Funded Trader Agreement (`tradeify.co/funded-trader-agreement`, May 2026), Tradeify trailing-max-drawdown article (`help.tradeify.co/.../10495897`, June 2026), MFFU fair-play article (`help.myfundedfutures.com/.../8444599`, updated 2025-11-24), MFFU payout-policy overview (updated 2026-02-22). One prior-plausible claim was refuted 0-3 against Tradeify's own docs: "Select evals have no daily loss limit" — a daily-loss dimension exists in some Select configuration not currently modeled by `firm_rules.py` (`daily_loss_pct=None` encodes the Flex reading only). This is the pre-flight blocker in §5.

---

## §1 — Context & motivation

Every probe run against the discovery apparatus this program (DISC-CAMP-0, the fork program, D5, H-OD-1, H-TSMOM-1, and the 2026-07-21 batch: OPENPRESS-1, MYM-3FPS-1, NG-EIA-1, RATES-EV-ZF-1, ORB-ZB-1) has converged on a bounded null: single-instrument index-futures intraday OHLCV is a bounded space with exactly one marginal survivor (ORB-MNQ). All of that apparatus answers "does mechanism X have demonstrable market edge" — a question distinct from the prop-portfolio program's actual objective, which is maximizing expected payout extracted per dollar of bounded spend. At c1's authorized WATCH-1 0.50×, pass probability is already ~96% (§0), so the bust/pass gate this program optimizes for is not the binding constraint for this book at this rung. The retry-EV gap it leaves unmeasured has been named four separate times since 2026-07-11 and never built (§0). This brief opens the investigation that closes that gap.

---

## §2 — Prior art / lineage

- **Q-DDP-1 + C2 relock** (`docs/adr/2026-05-08-dd-trigger-c2-relock.md`) — the one prior instance of genuine policy optimization against eval geometry (DD-trigger/scale grid, scored partly on median-days-to-pass), but for the now-closed FXIFY static venue, not a trailing-locking/retry object.
- **Bulenox C5 + tradeify_futures3_remc + tradeify_selectflex_remc** (`lab/archive/bulenox_futures_remc_2026-07-01/`, `lab/analysis/c1/tradeify_futures3_remc_2026-07-11/`, `lab/analysis/tradeify_selectflex_remc_2026-07-10/`) — three separate studies that each independently surfaced the same gap (bust<1% is one-shot economics; cheap Tradeify resets warrant a different gate) and none built it.
- **Survivor-scoring + ddp-reframe ADR** (`docs/briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md`, ratified) — fixed the current bust/pass gate and explicitly deferred the retry-EV objective as future (11-08 D1) work. This brief is that deferred work, opened early because the WATCH-1 pass-margin (§0) makes the gap load-bearing now, not just doctrinally overdue.
- **Class-S c1 haircut re-MC** (`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md`) — the current ratified WATCH-1 0.50× rung; this brief's U1 (design doc) evaluates funnel EV *at* that rung and the two adjacent ladder rungs, without proposing a new sizing behavior.
- **Perfect-foresight oracle test** (`lab/analysis/regime/regime_stress_2026-06-15/oracle_test.md`) — killed regime-*resizing* on detectability grounds. Named explicitly in §0 and §5 because this brief's object (contract-state-conditioned funnel accounting, not market-regime-conditioned resizing) is a different question and must not be read as re-opening that null.
- No prior Q-brief has modeled eval fees, reset economics, or the funded phase. This gap is confirmed, not assumed — see the prior-art audit underlying the design doc, which greped `docs/`, `lab/`, `ops/` (including `--no-ignore` over LTM/archive) for `optimal stopping|kelly|bold play|pass probability|day.?stop|bank(ing)? the pass|barrier` and found no formal treatment anywhere in this repo.

---

## §3 — Question (Q-FUNNEL-1)

What is the expected payout value per dollar-day of the c1 book's currently-ratified sizing rungs, once eval fees, reset economics, and the funded-phase payout structure — none of which the MC engine currently prices — are accounted for?

(Pre-Q gate: this names what's unmeasured, not a fix. It does not presuppose that a new sizing policy is warranted — §6's FALSIFIED branch is a legitimate, useful outcome.)

---

## §4 — Falsifiable hypothesis (H-FUNNEL-1)

**H-FUNNEL-1** (falsifiable): If the funnel EV per dollar-day of the c1 book at Tradeify Select 100K varies materially (per the §8 pre-registered threshold) across the three ratified sizing rungs (0.25× / 0.50× / 1.00×) and across a retry-vs-no-retry policy, on at least one point of the pre-declared edge-scenario grid (edge = 0 / panel-historical / half-panel), then the contract layer has demonstrable magnitude and the deferred policy layer (design doc §7) gets a GO case; otherwise the funnel EV surface is flat within MC noise, WATCH-1 0.50× stands as already near-optimal, the policy layer is not built, and H-FUNNEL-1 is **falsified**.

**Falsifier clause:** the hypothesis is falsified outright if the EV surface is flat within MC noise across all rungs and both retry policies at every edge-scenario grid point (restated with numeric triggers immediately below).

**Reject H-FUNNEL-1 if:** the EV surface is flat within MC noise across all three rungs and both retry policies, at every point on the edge-scenario grid.
**Accept H-FUNNEL-1 if:** EV varies by more than the §8 pre-registered threshold between at least two rungs, at any point on the edge-scenario grid, with the direction consistent across both regime halves (H1/H2).
**Ambiguous-hold if:** the funded-phase payout policy cannot be pinned from primary Tradeify docs at run time (i.e., the §5 pre-flight blocker is not resolvable), or the direction of the EV difference reverses between H1 and H2.

---

## §5 — Forbidden moves

- **No sizing-behavior change.** This study evaluates the existing ratified rungs; it does not introduce, deploy, or recommend a specific new day-policy. That is design doc §7's deferred item, gated on this brief's own verdict.
- **No re-opening the regime-resizing oracle null.** Contract-state (equity, floor distance, day count) is directly observable; this is not a re-test of the FALSIFIED regime-*conditional* resizing finding (`oracle_test.md`) and must not be framed as one.
- **No fabricated funded-phase numbers.** Payout buffer, minimums, caps, and split must be pinned from primary Tradeify docs at run time, dated and quoted. If unavailable, the study halts at AMBIGUOUS-HOLD (§4) rather than inventing a plausible figure.
- **No smooth continuous rung sweep.** Only the three existing discrete ladder values (0.25×/0.50×/1.00×) are compared, per the stepped-not-smooth doctrine (`docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md`).
- **No K spend.** The study conditions on contract state and own equity, not market data; `register_search open` binds `K=0` with that rationale. Any temptation to add a market-signal-conditioned variant is a different, K-bearing study and out of scope here.
- **No skipping the §5 pre-flight blocker.** The Select Flex-vs-Daily payout-policy confirmation (below) must complete before U1's config is pinned — the deep-research pass refuted "Select has no daily loss limit" 0-3 against Tradeify's own docs, so the currently-modeled `daily_loss_pct=None` cannot be assumed correct without a live-account check.

**Pre-flight (blocking, before §8 pre-registration is committed):** ~~confirm which Select payout policy the target Tradeify account carries~~ **RESOLVED 2026-07-21** (operator, chat): **Select Flex, $3,000 DD** — matches the current `firm_rules.py` encoding (`max_dd_pct=3.0`, `daily_loss_pct=None`) exactly. No engine gap on this axis; the daily-loss dimension the deep-research refutation flagged as unconfirmed belongs to the Daily variant, not this account. §8 pre-registration is unblocked.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | EV varies by more than the §8 threshold between ≥2 rungs, on ≥1 edge-scenario grid point, direction consistent across H1/H2 | Author the design doc §7 policy-layer GO case (new `dd_geometry` instance or rail-host factor); fresh operator GO required before any build |
| `FALSIFIED` | EV surface flat within MC noise across all rungs/retry policies, all grid points | Close; append to `docs/rejected_candidates.md` as a discharged D1 item; policy layer not built; WATCH-1 0.50× stands |
| `AMBIGUOUS-HOLD` | Funded-phase payout policy cannot be pinned from primary docs, OR EV-direction reverses between H1 and H2 | Diagnose the blocking gap; re-test window: next quarterly review (2026-08-08) or when the blocker resolves, whichever first |

Pre-registered before any data touches analysis — see §8.

---

## §7 — Execution plan

Self-executing in `lab/archive/q_funnel_1_2026-07/`, following design doc §2/§8:

- **Phase 0 — Rule-0 reads + pre-flight.** Confirm Select Flex-vs-Daily on the live account; pin current eval-fee/reset pricing and funded-payout policy from primary Tradeify docs, dated and quoted.
- **Phase 1 — Regression pins.** With fees=0, funded-value=0, resets=never, the funnel wrapper (`funnel.py`) must reproduce the ratified WATCH-1 bust/pass numbers from `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md` exactly. Hand-computed deterministic-path EV unit tests.
- **Phase 2 — Funnel MC.** Import `core/mc/simulation.py` read-only, same REGIME_GATE panel vintage as the WATCH-1 ratification; run all three rungs × retry policies × edge-scenario grid, both regime halves.
- **Phase 3 — Verdict assertion.** Apply §6 against the actual numbers; produce closure artifact per §9.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

To be authored as a separate file at `docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md`, containing: the exact EV formula (design doc §2/U2), the "materially varies" numeric threshold, and the three-point edge-scenario grid (edge = 0 / panel-historical estimate / half-panel) — written and committed **after** the §5 pre-flight blocker resolves and **before** Phase 1 executes.

Pre-registration commit hash: `<populated at pre-registration commit time>`
Pre-registration date: `<populated at pre-registration commit time>`

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md` + a recommendation note scoping the design doc §7 policy-layer GO case.
- **If FALSIFIED:** `docs/briefs/closures/Q-FUNNEL-1-closure-falsified.md` (no recommendation.md); append to `docs/rejected_candidates.md`.
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-FUNNEL-1-closure-ambiguous.md` with the explicit re-test trigger from §6.

Closure record must include: verdict, anchor numbers vs the §8 threshold, what the pre-registration predicted vs what actually happened, and lesson candidates with dollar anchor where applicable.

---

## §10 — Audit hooks

```bash
# Confirm §0 anchors still resolve
git log -1 -- core/firm_rules.py | grep a53ee99
git log -1 -- core/mc/simulation.py | grep a53ee99
git log -1 -- lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md | grep d85c10c

# Confirm no core/ file was touched by this investigation
git log --oneline -- core/ | grep -i funnel || echo "core/ untouched — confirmed"

# Confirm K=0 (no manifest opened for this study)
rg -n "funnel|q_funnel" discovery_manifests/ || echo "K=0 confirmed"

# Pre-registration commit predates first analysis script run
git log --oneline docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md
git log --oneline lab/archive/q_funnel_1_2026-07/funnel.py

# Re-run the gate-firing assertion (once RESOLVED/FALSIFIED)
python lab/archive/q_funnel_1_2026-07/funnel.py --reproduce-q-funnel-1

# Regression pin: funnel wrapper reproduces the ratified WATCH-1 numbers at fees=0/no-funded/no-retry
pytest -q lab/archive/q_funnel_1_2026-07/test_funnel.py -k regression_pin
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md --type inquire

git log -1 -- core/firm_rules.py
git log -1 -- core/mc/simulation.py
git log -1 -- lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md
git log -1 -- docs/briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md
```

If any verification command fails, the brief is not complete. Re-author the section that broke; do not handwave.
