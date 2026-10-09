# Q-SFGROWTH-1 — Self-funded growth portfolio selection under a 15% peak-to-trough limit

**Status:** `OPEN`
**Authored:** 2026-10-09
**Closed:** N/A
**Authors:** Joshua (rulings) + Claude Code (author)
**Parent question:** N/A — owed item 1 of the [self-funded lane ADR](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#grounds)
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure is gated by the frozen [verdict pre-registration](pre-registration/Q-SFGROWTH-1-verdict-preregistration.md)
**Artifact path:** `docs/briefs/Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md`

---

## §0 — Rule 0 reads (production-source verification)

All anchors are `git log -1 --format='%h %cs' -- <path>` on 2026-10-09.

- `docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md` — anchor `f63a19c 2026-10-09`. Decision 4 is the operator-confirmed clearance standard this brief scores against.
- `core/mc/simulation.py` — anchor `0db500e 2026-10-05`. `simulate_path` (:321) honors an optional `intraday_low` for the barrier (:523-533), but `max_dd` is computed on end-of-day equity only (:519-521); the engine is pass/bust shaped (`profit_target` > start, :195). It cannot produce this brief's statistic without new code.
- `lab/discovery/remc_series_builder.py` — anchor `dbaa1ec 2026-10-05`. Builds the daily P&L series and the conservative coincident-sum intraday low (`-Σ|adverse excursion| - cost`); costs are `sides × cost_per_side_usd` (:588-669).
- `core/firm_rules.py` — anchor `7e9bd50 2026-10-04`. No self-funded tier type exists; Tradeify per-side costs (:321) and the 6J full-contract-only constraint (:236-239) are the only Tradovate-routed cost facts on file.
- `core/strategies/BOOK_SOURCES.sha256` — anchor `7e9bd50 2026-10-04`. Pins the four accepted legs' Pine and runtime ports (private; not read, not quoted).
- `lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md` — anchor `b31c6d4 2026-10-06`. The four-leg book FALSIFIED on the intraday-honest clock at four 100K tiers (bust 25–36%).
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json` — anchor `7e9bd50 2026-10-04`. Names the fifth source with an accepted CME trade list (Striker NAS100 MNQ, DOW-excluded), not selected for Tradeify. Ruled into this pool by the operator 2026-10-09.
- `docs/adr/2026-08-30-evaluation-order.md` — anchor `7e9bd50 2026-10-04`. Portfolio/venue fit comes last, only for already-confirmed candidates, with K opened before any Explore read.
- `core/lifecycle.py` — anchor `7e9bd50 2026-10-04`. State file absent ⇒ every leg reads AUTHORIZED 1.0× (:56-59); locked parameters are not touched by sizing.

**Dedup search (sub-rule 8), executed 2026-10-09:** `grep -i "self-funded|growth|kelly|personal" lab/CATALOG.md docs/briefs/INDEX.md` returned one unrelated hit (`shape_feasibility_map_2026-08`, a Tradeify Growth tier). `check_advisor_dedup.py --keywords "self-funded,kelly,growth,personal account,portfolio selection"` returned the 2026-07-16 closure ADR, the ORB-MNQ unpark ADR and unrelated audits; no prior self-funded selection study.

---

## §1 — Context & motivation

On 2026-10-09 the operator reopened a self-funded lane on a personal Tradovate account with $10,000, set its objective as maximum growth, left the portfolio unselected, and ruled the clearance standard: at most a 15% peak-to-trough drawdown, tested as p99 on an intraday-honest simulation with Tradovate costs and whole-contract sizing, with a live halt at 15% below peak ([ADR Decision 4](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#decision)). No strategy or combination has been scored against that standard.

---

## §2 — Prior art / lineage

- [Four-firm re-MC](../../lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md) — FALSIFIED early-fail for the full four-leg book at 100K prop tiers; a $1,500 limit on $10,000 is tighter in dollars, so the full book at accepted size is expected to fail here too (disclosed ex-ante, not a reason to skip it).
- [Size-feasibility prereg](../../lab/analysis/c1/size_feasibility_2026-10/) — FROZEN 2026-10-08, uniform scaling k at prop tiers, no RESULTS yet. Different question (prop pass/bust), same integer-rounding gap.
- Rejected or falsified, excluded from the pool: R5/P2 locked edge transfer, S-MYM-ORC-02, Guardian→MGC (R7/b8), Q-TXG-1 swaps, Q-COMPOSE-1 ([rejected_candidates.md](../rejected_candidates.md)). Re-proposal needs new mechanism evidence.
- Parked lanes b1 Aegis→6J, b3 ORB-MNQ payability and b6 Q-NAS-ECR convert to SUBTRACT on 2026-11-08 ([STATE](../../STATE.md#2026-11-08)); this brief uses only legs with an accepted trade list, not those lanes' research bodies.

---

## §3 — Question (Q-SFGROWTH-1)

**Q-SFGROWTH-1:** Among the strategies with an accepted CME trade list, which combination and whole-contract sizing gives the highest typical one-year growth on a $10,000 Tradovate account while keeping the chance of a 15% peak-to-trough drop at or below 1 in 100, and does that choice hold on data it was not selected on?

---

## §4 — Falsifiable hypothesis (H-SFGROWTH-1)

**H-SFGROWTH-1:** If at least one configuration on the frozen grid clears the 1-in-100 limit with a median one-year return above zero on the Explore window, then the top-ranked one also clears the limit, at 1× and 1.5× cost, with a positive median return on the Confirm window; otherwise no portfolio from the current pool is fit for this account.

**Accept H-SFGROWTH-1 if:** all four RESOLVED conditions in the [pre-registration §D](pre-registration/Q-SFGROWTH-1-verdict-preregistration.md#d--verdict-table) hold.
**Reject H-SFGROWTH-1 if:** no grid configuration clears on Explore with median terminal equity above $10,000.
**Ambiguous-hold if:** the top Explore configuration fails any Confirm or cost-stress condition.

---

## §5 — Forbidden moves

- **Walking down the ranking after a Confirm failure** — taking the second-ranked configuration is a second selection on the same data; AMBIGUOUS-HOLD returns to the operator instead.
- **Widening the sizing grid or the leg pool after Explore results exist** — that turns K into a function of the outcome (Known Trap #12); a new grid is a new pre-registration.
- **Using end-of-day drawdown** — the four-firm run showed the intraday clock changes verdicts; the live halt fires intraday.
- **Fractional contracts or uncompounded "scaled P&L" without floor rounding** — a $10,000 account cannot hold 0.3 contracts; the selection must match what the rail can place.
- **Relaxing to 95 in 100 because nothing clears** — the operator confirmed 99 in 100; a change is a new ruling and a new freeze.
- **Retuning any strategy parameter** — locked parameters are immutable; only per-leg contract multipliers vary.
- **Adding any other VENUE_WITHDRAWN or rejected edition** — only the NAS100 MNQ edition was ruled in (pre-lock checklist); rejected candidates need new mechanism evidence.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Pre-registration §D RESOLVED row: ≥1 Explore clearer with median > start; the top one clears Confirm at 1× and 1.5× cost; Confirm median > start | `INTEGRATE — record the selected legs and multipliers as the lane's portfolio and sizing binding; proceed to ADR owed items 2–6` |
| `FALSIFIED` | No grid configuration clears on Explore with median terminal equity > $10,000 | `STOP — re-proposal bar: a new confirmed strategy, or an operator change to capital or the clearance standard; not a re-grid` |
| `AMBIGUOUS-HOLD` | The top Explore configuration fails any Confirm or 1.5× cost condition | `ITERATE — return to the operator with the full ranking; no automatic second pick` |
| `VOID` | Integrity failure: a pinned export hash mismatches, the run's K differs from the manifest's K, or a cost input is unverified | `ITERATE — fix the input and rerun the same frozen design` |

---

## §7 — Execution plan

- **Phase 0 — inputs (operator checkout).** Confirm the pinned exports for each pool leg are present and hash-match `run_four_firm_remc.py`'s pins; record the verified personal-Tradovate all-in cost per side for 6J, MNQ, MYM and MGC; open a `register_search` manifest with the grid's K before any Explore read.
- **Phase 1 — scorer.** Implement the pre-registration's statistic as a new lab scorer reusing `remc_series_builder` for daily P&L and intraday lows; unit-test it against the pre-registration's worked example and a synthetic panel. Reviewed before any real export is read.
- **Phase 2 — Explore.** Score every grid configuration on the Explore window; commit the full ranking as a hash-pinned freeze.
- **Phase 3 — Confirm and verdict.** Score only the top configuration on Confirm at 1× and 1.5× cost; assign the §6 verdict mechanically; write the closure.

Execution runs in the operator's primary checkout (private exports); this public clone cannot run Phases 0–3.

---

## §8 — Verdict pre-registration

[`docs/briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md`](pre-registration/Q-SFGROWTH-1-verdict-preregistration.md) — ships a worked numeric example for the two-implementer test.

Pre-registration commit hash: `<populated when the operator freezes it>`
Pre-registration date: 2026-10-09 (FROZEN)

Operator rulings before freeze (2026-10-09): the Striker NAS100 MNQ (DOW-excluded) edition is in the pool for this personal-account selection only, its Tradeify withdrawal standing ("include it"); the pre-registration is frozen ("freeze the plan").

---

## §9 — Closure record format

Per `references/closure_record.md`: `docs/briefs/closures/Q-SFGROWTH-1-closure-<verdict>.md` with the full Explore ranking, the Confirm numbers against the thresholds, and the mandatory typed `## Iterate` block.

---

## §10 — Audit hooks (runnable, not vague)

```bash
# Anchors still resolve
git log -1 --format=%h -- core/mc/simulation.py lab/discovery/remc_series_builder.py docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md
# Pre-registration committed before any Explore ranking exists
git log --format='%h %cI' -- docs/briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md | tail -1
git log --format='%h %cI' -- 'lab/analysis/**/sfgrowth*' | tail -1
# K in the manifest equals K in the ranking
rg -n '"K"' discovery_manifests/*sfgrowth*.json
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md --type inquire
git log -1 --format='%h %cs' -- core/mc/simulation.py lab/discovery/remc_series_builder.py core/firm_rules.py
```

