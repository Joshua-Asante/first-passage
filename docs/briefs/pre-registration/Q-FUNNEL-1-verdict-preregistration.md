# Verdict pre-registration — Q-FUNNEL-1 (contract-funnel EV analysis)

**Status:** `FROZEN` (2026-07-21, operator chat: "25% and 5 resets look right, freeze it" — ratifies §3(a)'s 25% relative threshold and §4's `MAX_RETRIES=5`. §5's funded-payout config remains a Phase-0 data-pin, not a frozen number — unchanged, see below.)
**Pre-registered:** 2026-07-21 — **BEFORE T0** (no funnel MC run yet, no `lab/archive/q_funnel_1_2026-07/funnel.py` execution)
**Parent brief:** [`docs/briefs/rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md`](../rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md)
**Design doc:** [`docs/superpowers/specs/2026-07-21-q-funnel-1-contract-ev-design.md`](../../superpowers/specs/2026-07-21-q-funnel-1-contract-ev-design.md) §2 (U2)
**Target account (confirmed 2026-07-21, operator chat):** Tradeify Select 100K, **Flex** payout policy, $3,000 EOD trailing DD — matches `core/firm_rules.py` `Tradeify_Select_100K` byte-for-byte (`max_dd_pct=3.0`, `daily_loss_pct=None`).

---

## What is frozen now (formula + grid shape — not yet the numeric thresholds)

1. **Question (symptom form):** does the funnel EV per dollar-day of the c1 book vary materially across the three ratified sizing rungs and a retry policy, once fees/resets/funded-phase payouts are priced — a question the discovery apparatus's bust/pass gate cannot answer because it terminates at `pass`.
2. **EV formula (frozen):**
   ```
   EV/day(rung, retry_policy, edge_scenario) =
       mean over simulated lineages of [ terminal_value(lineage) - cumulative_spend(lineage) ]
       ------------------------------------------------------------------------------------
                       mean over simulated lineages of [ cumulative_wall_clock_days(lineage) ]
   ```
   where `terminal_value` = 0 (retries exhausted with no funded outcome) or `busted-post-funding loss = -cumulative_spend` or `sum of realized payouts net of spend` (funded-then-extracting); `cumulative_spend` = eval fee × (1 + number of resets consumed) at the pinned fee schedule (Phase-0 config, cited primary-source, dated at execution — not fixed here); `cumulative_wall_clock_days` = trading days elapsed across all reset attempts for that lineage, from the frozen `simulate_path` daily loop.
3. **Rungs compared (frozen, the three ratified ladder values only — no smooth sweep):** 0.25× / 0.50× (current WATCH-1) / 1.00×.
4. **Retry policies compared (frozen, exactly two):** **no-retry** (single attempt; bust = terminal, `terminal_value = -eval_fee`) vs **retry-to-cap** (immediate reset on any bust up to `MAX_RETRIES` attempts — numeric value proposed in §4 below — then terminal with no funded outcome).
5. **Edge-scenario grid (frozen shape, three points):**
   - **edge=0** — the panel's daily strategy-P&L series de-meaned to zero (bootstrap-preserving variance/autocorrelation), isolating pure barrier-crossing + retry-economics value with no assumed market edge.
   - **edge=panel-historical** — the REGIME_GATE panel's actual realized daily P&L series, unmodified (the "as measured" case).
   - **edge=half-panel** — the panel de-meaned to half its historical drift, a conservative decay-haircut scenario matching this repo's standing convention (D5's "conservative central" derivation; the harvest doc's decay-haircut rule) for not taking a historical edge estimate at face value.
6. **Regime split (frozen):** every cell of the grid (rung × retry × edge-scenario) runs on both H1 (2020-23) and H2 (2023-26) per the standing regime-robustness gate, matching the WATCH-1 haircut ratification's own convention.

---

## Numeric thresholds (ratified 2026-07-21, operator chat)

**§3 — "Materially varies" threshold (governs H-FUNNEL-1 accept/reject, brief §4/§6).**

**Ratified:** EV/day is judged to vary materially between two rungs, at a given edge-scenario grid point, iff **all three** hold:
- (a) **Economic significance:** the better rung's EV/day point estimate exceeds the worse rung's by **≥25% relative** to the worse rung's magnitude.
- (b) **Statistical significance:** the two rungs' bootstrap 5th–95th percentile EV/day bands (same week-block bootstrap machinery as the WATCH-1 haircut re-MC) **do not overlap**.
- (c) **Regime consistency:** the direction of the difference (which rung is better) is the **same sign in H1 and H2**.

H-FUNNEL-1 is accepted if (a)+(b)+(c) hold at ≥1 grid point; rejected (falsified) if none hold at any grid point; AMBIGUOUS-HOLD if (a)+(b) hold at a grid point but (c) fails (direction reverses between halves) — this is a stronger ambiguity trigger than a simple non-finding, and is treated as a genuine open question rather than a null, per brief §4.

*Rationale for 25%:* large enough that no reasonable reader would call it noise-chasing (an EV/day difference of 2–5% is exactly the kind of thing that could be an artifact of the fee-schedule pin or the funded-payout config pinned at Phase 0, not a real structural effect); small enough to still catch a genuine, useful effect rather than requiring an implausibly large one. **Ratified as proposed, unchanged.**

**§4 — Retry cap (`MAX_RETRIES`).**

**Ratified: 5** resets per lineage before the retry-to-cap policy terminates with no funded outcome. Rationale: bounds simulation compute to a realistic operator horizon (5 consecutive Select 100K resets at ~$60–239 each per the Select Flex re-MC precedent, or the promo/worst-case figures in Q-RAIL-1 Phase 4, is already a materially large cumulative spend — beyond that, "keep resetting" stops being a live policy question and starts being a different, more extreme hypothesis this study is not scoped to test).

**§5 — Funded-phase payout config (data pin, not a threshold — resolved 2026-07-21, same day as the freeze, via live browser fetch of the primary source below).**

Pinned from **help.tradeify.co, "Select Flex and Select Daily Payout Policies"** (page dated "Updated over 2 weeks ago" as of fetch date 2026-07-21, i.e. ≈2026-07-07) and **"Select Evaluation Accounts"** (dated April 2, 2026), both fetched live 2026-07-21 (WebFetch was blocked 403 by Tradeify's Intercom bot-guard, matching the deep-research pass's own note on this — resolved via the in-app browser's rendered `get_page_text`, same workaround the deep-research pass used). **Select Flex, 100K account** (the confirmed target, §0):

- **Profit split:** 90% trader / 10% Tradeify. *Quote: "Profit Split: 90 Trader / 10 Tradeify."*
- **Payout frequency:** every 5 winning days; winning-day threshold on the 100K tier = **$200 minimum profit per day**. *Quote: "Payout Frequency: Every 5 winning days... 100K Account: $200 minimum profit per day."*
- **Payout cap:** up to 50% of total profit (current balance − starting balance), **capped at $4,000 per payout** on the 100K tier. *Quote: "100K Account: Up to 50% of your total profits..., capped at $4,000 per payout."*
- **No minimum balance requirement, no buffer system** (Flex-specific — contrasts with the Daily policy's buffer; do not conflate the two when wiring the funnel). *Quote: "Unlike other Tradeify programs, Select Flex has no minimum account balance requirement for payouts."*
- **Loss-recovery rule (applies to both Flex and Daily, all payouts after the first):** account must be net-positive for the current payout cycle before another payout can be requested — profit tracking resets to zero after each payout. *Quote: "You must have positive net profit during each payout cycle in order to request a payout."*
- **Drawdown lock (confirms design doc §0/§3, now primary-cited independently):** floor locks permanently at **$100,100** once EOD balance first exceeds **$103,100** (Flex) — matches `core/firm_rules.py`'s `dd_lock_offset_usd=100` / `max_dd_pct=3.0` exactly. *Quote: "100K Account: $103,100 (Flex) / $102,600 (Daily) → Locks at $100,100."*
- **No consistency rule once funded** (40% is eval-only, both policies) — matches `firm_rules.py`'s `consistency_rule_pct` scope.
- **No ongoing or activation fees once funded.** *Quote: "There are no ongoing fees for funded accounts and no activation fee."*
- **Funded contract-scaling law (new information — not currently modeled by the engine at all):** funded accounts start at 3 mini/30 micro (below the eval's flat 8/80 max) and scale up via EOD-equity triggers ($101,500 → 4/40; $102,000 → 5/50; $103,000 → 8/80 max), cumulative and monotonic. **This is out of scope for Q-FUNNEL-1's funnel wrapper** (the EV formula's `terminal_value` for a funded lineage does not need position-size resolution — it only needs realized payout totals) but is flagged here for any future study that models funded-phase *trading* rather than funded-phase *payout extraction*.
- **Purchase restrictions (already corroborated by the deep-research pass, now independently re-confirmed):** max 15 evaluations per rolling 30 days, max 10 resets per evaluation per 30 days, max 5 funded accounts held simultaneously.

**Eval fee / reset cost:** reused from this repo's own prior operational pricing (not re-fetched — checkout/cart pricing is dynamic and promo-gated, unlike the help-center docs above, and this repo already has a primary-adjacent pin from the actual account purchase): **Q-RAIL-1 Phase 4** (`lab/analysis/c1/q_rail_1_2026-07/PHASE4.md`, dated 2026-07-17) — Tradeify Select base **$328**, July promo **$258**, worst-case-plus-one-reset **$681**. Cursor's Phase-0 report should note whether these still match the live checkout price at build time (a drift here does not block Phase 1 — the §3(a) 25% relative threshold has margin against small fee-schedule movement — but should be logged, not silently assumed current).

---

## §6 table (frozen — trigger conditions use the ratified §3–§4 thresholds)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | §3(a)+(b)+(c) all hold at ≥1 edge-scenario grid point | Author the design doc §7 policy-layer GO case; fresh operator GO required before any build |
| `FALSIFIED` | §3(a) or §3(b) fails at every grid point (EV surface flat within noise or below the 25% economic floor everywhere) | Close; append to `docs/rejected_candidates.md`; policy layer not built |
| `AMBIGUOUS-HOLD` | §3(a)+(b) hold at some grid point but §3(c) fails (direction reverses H1↔H2), OR the §5 funded-payout config cannot be pinned from primary docs | Diagnose; re-test window = 2026-08-08 quarterly review or when the blocker resolves, whichever first |

---

## Denylist (hard — mirrors design doc §5 forbidden moves)

- No sizing-behavior change proposed or deployed by this study itself.
- No re-test of the FALSIFIED regime-*conditional* resizing finding (`lab/analysis/regime/regime_stress_2026-06-15/oracle_test.md`) — this study conditions on directly-observable contract state, not inferred market regime.
- No smooth rung sweep — only the three ratified ladder values.
- No K spend — `register_search open` binds `K=0`.
- No fabricated funded-payout numbers — AMBIGUOUS-HOLD if the §5 config cannot be pinned from primary docs.
- No amending §3/§4 after Phase 1 results exist. If either number needs to change after seeing data, this pre-registration closes AMBIGUOUS and a fresh one opens with new criteria stated up front (brief-authoring Known Trap #12 — mid-investigation gate amendment is `p`-hacking at the methodology layer).

---

## Commit discipline

This file + the parent scoping brief are **committed before Phase 1 executes**. §3(a)'s 25% threshold and §4's `MAX_RETRIES=5` are now ratified — both were load-bearing on the verdict and neither had prior-art precedent in this repo to inherit from (unlike, e.g., the DSR K-rule or the regime-robustness gate's H1/H2 split, both reused here without re-derivation). Any edit to §3/§4 after Phase 1 results exist requires closing this pre-registration AMBIGUOUS and opening a fresh one (Known Trap #12 — mid-investigation gate amendment is `p`-hacking at the methodology layer).

Pre-registration commit hash: this commit — verify via `git log -1 -- docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md`
Pre-registration date: 2026-07-21 (proposed) / 2026-07-21 (frozen, same day)
