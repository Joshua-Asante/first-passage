# Q-CADENCE-1 — Pre-registration: is the c1 book's weekly-coverage deficit closable by a leg, or is scheduled maintenance the cheapest cadence instrument?

**Status:** `FROZEN` — pre-registration only. **Phase 1 has not run.** K=0 · $0 · no manifest · no pull · **M2K bank UNSPENT** · MYM bank unspent at 1.
**Authored:** 2026-08-03
**Authors:** Joshua (direction 2026-08-03: *"I do not want to have to use token trade mitigation to get around this"*) + Claude Code (Opus 5)
**Parent measurement:** [`lab/analysis/c1/c1_cadence_coverage_2026-08-03/RESULTS.md`](../../../lab/analysis/c1/c1_cadence_coverage_2026-08-03/RESULTS.md) §B — authored this session, `a1123b8`.
**Sibling:** [`docs/adr/2026-08-03-lifecycle-ladder-intermediate-rung.md`](../../adr/2026-08-03-lifecycle-ladder-intermediate-rung.md) (§A of the same measurement; independent decision).
**Loop:** Inquire-phase Pre-Q — closure gates on one non-inferiority test at minimum size.
**Artifact path:** `docs/briefs/pre-registration/2026-08-03-c1-cadence-leg-preregistration.md`

---

> ⚠ **READER INTERCEPT 2026-08-06 (claim-alignment M39) — banner only; frozen body unedited.**
> **Deployment limb MOOT** with the Tradeify de-scope. The ≥90%-of-weeks floor and the C1–C5
> structure **survive as a reusable gate** for F3. **ORB-MNQ was adjudicated SCREEN-DEAD on S7
> 2026-08-04 — do not re-nominate it.** §0's cap reads remain **code-true** but describe a venue
> no longer targeted; C5's `80 − (69 + 11) = 0` arithmetic and the MYM 9 / MNQ 4 floors are
> Tradeify-specific and must be **re-derived in a new pre-registration** if C1–C5 are reused.


## §0 — Rule 0 reads (verified 2026-08-03 at `a1123b8`, worktree clean)

| Source | Anchor | Supplies |
|---|---|---|
| [`lab/analysis/c1/c1_cadence_coverage_2026-08-03/RESULTS.md`](../../../lab/analysis/c1/c1_cadence_coverage_2026-08-03/RESULTS.md) §B | this session, `a1123b8` | The generating evidence — and therefore the **burned** evidence (§1). 217/297 weeks covered, 80 idle (26.9%); co-idle +14.6% vs independence; marginal coverage 44.8%/44.1%; the residual-idle projection table. |
| [`core/firm_rules.py`](../../../core/firm_rules.py) L321–334, L196–207, L216–222, L230–237, L245–264 | `89a069a` 2026-08-02 | `inactivity_max_idle_days: 5` is a **VENUE FACT** (art. 10468318, ≥1 trade/week, eval **and** funded); the barrier is disabled in the re-MC as a *modelling choice*, now PRICED at 92.6–97.6% path death with the mitigation **undelivered** (residual track R8). Contract cap is **ACCOUNT-AGGREGATE** (80 micros), already allocated MYM 69 / MNQ 11. Costs $1.82 RT index micros. Hedging: Equity Index Product Group; long+long explicitly allowed. **US Treasuries untradable.** |
| [`ops/instruments/M2K.md`](../../../ops/instruments/M2K.md) §PROFILE, M4, W4, 2026-07-30 disposition | `249b30d` 2026-07-30 | **K bank 0 — the widest DSR headroom in the repo, spendable exactly once.** `floor_at_k(1)`=0.650 vs Cap 1.0. Verbatim: *"Do not spend this bank on a wide search. One pre-committed mechanism, `K_eff=1`."* **W4: no panel exists locally** — any pull needs a recorded cost dry-run, `--force` forbidden. Shares the account-aggregate cap with MYM+MNQ. Must be sequenced against `WSTRUCT-M2K-1` by the operator first. |
| [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) | `6ef7d8a` 2026-08-02 | MNQ family bank **2 → floor 0.980, at the 1.0 Cap**. MNQ is closed to new edge seeds. |
| [`ops/instruments/MYM.md`](../../../ops/instruments/MYM.md) L4, L93–95, L101 | `96974de` 2026-08-03 | Reconstruction track **TERMINAL**; 5 DEAD rows. Bank 1 → `K_eff` 2 at floor 0.850. **S3 order-symbol occupancy**: MYM1! Tue+Fri closed until the Striker leg parks and its TV alerts are deleted. ⚠ unreconciled `S-MYM-ORC-02` K=2 would push the family to floor 1.06 > Cap, closing MYM entirely. |
| [`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md`](../../adr/2026-08-03-orb-mnq-repark-payability-falsified.md) | `9b5ce43` 2026-08-03 | ORB-MNQ-1 re-PARKED **today**; the *payable standalone Tradeify leg* target FALSIFIED on §4 T2 (bust 67.67/77.01/80.18% vs a 3.0% ceiling). Lifecycle **not** demoted, K **not** spent, mechanism **not** rejected — **the falsification is scoped to one target at one firm.** |
| [`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) | `ba943a1` 2026-07-17 | Class-S: existing-strategy books admitted through the **unchanged** frozen gate; the claim is **native-book bust-geometry, never edge-transfer**. The route this brief uses to avoid re-spending K. |
| [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) | `be6dda6` 2026-07-13 | The frozen survivor-scoring gate this brief does **not** amend. |

**Gitignore pre-flight:** `**/*.pine` is ignored; **no Pine source is read or cited** by this brief.
No numeric constant here derives from Pine. Citation-chain mode not required.

**Post-authoring merge (recorded, not re-stamped).** All reads above were performed at `a1123b8`. The branch subsequently merged `origin/main` `d4a1cc9` (PR #624, params.toml gate retirement). Every file anchor cited above was re-verified unchanged across that merge; `scripts/validate_params.py` was deleted by #624 and the §10 hooks were repaired accordingly.

---

## §1 — What is burned, stated before anything else

**The firing-rate floor in §4 was derived from the incumbents' own coverage.** The 80 idle weeks, the
+14.6% excess co-idleness, and the 44.8%/44.1% marginal-coverage figures are what *produced* the
hypothesis that a leg must fire in ≥90% of weeks to matter. They therefore **cannot also confirm a
candidate**.

**Consequently BURNED — may set the bar, may not clear it:**

- MYM and MNQ weekly-coverage counts, in any form;
- the co-idleness excess and the residual-idle projection table;
- any statistic computed on the 2026-08-03 MYM/MNQ exports.

**The floor is frozen from the burned evidence; the candidate is scored on its own panel.** This is
the legitimate use — a threshold derived from incumbents and applied to a construct measured
elsewhere is a *bar*, not a confirmation. What is illegitimate is measuring the candidate's coverage
on the incumbents' panel and calling the agreement evidence.

**Honest limitation, disclosed pre-result.** Any admissible candidate instrument (Equity Index micros)
is correlated with the incumbents by construction — `corr(RV)` MYM↔MNQ 0.717 (cross-index probe
2026-07-21), and `M2K.md` M4 states the tension directly: *"opening-range momentum is an equity-index
property … that same tie means cost-viability and decorrelation-from-the-book are in tension by
construction."* A candidate that clears the floor on its own panel may still under-cover **the
incumbents' specific idle weeks**. §4 limb C3 tests exactly that and is gating.

---

## §2 — The problem, stated precisely enough to be wrong

The eval requires ≥1 trade per week. The book delivers a trade in 73.1% of weeks — not because its
rate is too low (it averages 1.06 active days per week) but because the spacing is **clustered**: the
two legs go quiet together, 14.6% more than independence.

The operator's constraint is *no scheduled maintenance trade*. That converts a rate problem into a
**coverage** problem, and coverage compounds multiplicatively:

> residual idle weeks after adding a leg firing with weekly probability `p` ≈ `80 × (1 − p)`

The measured incumbent rate is `p = 0.512`. One more such leg leaves **39 idle weeks** — halving the
gap, not closing it — even under the *generous* assumption of full independence. Reaching under one
expected idle week per eval window (32.6 weeks) requires **`p ≥ ~0.90`**.

**A leg shaped like the incumbents cannot solve this.** Only a near-unconditional-entry construct —
one that fires on most *days*, so that a week without a trade is rare by construction — changes the
answer. That is a statement about **firing frequency**, and it is independent of edge.

Which sets up the real question. A cadence leg earns its place only if it does **not** degrade the
book. Its expectancy must be non-negative after Tradeify costs, and its contribution to the intraday
excursion that sets the critical scale (0.441×, sibling ADR §A) must be immaterial. **A cadence leg
with negative expectancy is a scheduled maintenance trade with worse variance and a contract-cap
cost** — strictly dominated by the thing the operator is trying to avoid.

---

## §3 — Question

**Q-CADENCE-1:** Does a near-unconditional-entry construct, at minimum size on the c1 account, raise
the book's weekly coverage above the frozen floor **without** degrading its eval survival geometry —
or is a scheduled maintenance trade the cheapest available cadence instrument?

---

## §4 — Falsifiable hypothesis and frozen thresholds

**H-CADENCE-1 — If** a pre-committed candidate construct (C1) fires in ≥90% of calendar weeks on its
own panel, **and** (C2) carries non-negative expectancy net of Tradeify all-in cost, **and** (C3)
raises the *combined* book's weekly coverage to ≥95% measured on the incumbents' idle weeks
specifically, **and** (C4) leaves the book's eval geometry non-inferior, **and** (C5) fits the
account-aggregate contract cap without reducing either incumbent leg below its current allocation,
**then** a cadence leg is licensable and the maintenance trade is unnecessary; **otherwise** the
maintenance trade is the cheapest cadence instrument and the cadence program closes.

| Limb | Frozen threshold |
|---|---|
| **C1 — firing rate** | Candidate fires in **≥ 90%** of calendar weeks over its own panel span, ≥3 years. Derived in §2 from the burned evidence; frozen here before any candidate is named. |
| **C2 — cost viability** | Mean per-trade P&L **≥ 0** net of **$1.82 RT** (`cost_per_side_usd: 0.91` × 2), with the lower bound of a 95% block-bootstrap CI **> −0.02R**. Non-negative, *not* positive — this is a cadence bar, not an edge bar. |
| **C3 — incumbent-idle coverage** | The candidate fires in **≥ 95%** of the incumbents' **80 idle weeks** — i.e. **≥ 76 of 80**. This is the limb §1's honest-limitation paragraph exists for: a candidate can pass C1 on its own panel and still fail C3 if its quiet periods coincide with the book's. **C3 is gating and may not be waived by a strong C1.** |
| **C4 — non-inferiority of eval geometry** | With the candidate added at minimum size, the combined book's **max intraday drawdown** (`cluster` proxy) rises by **≤ 5%** vs the 2-leg baseline at the same rung, **and** rolling-eval failure rate rises by **≤ 1.0pp**. Scored by the sibling harness, same geometry, same proxy. |
| **C5 — cap feasibility** | Candidate's max simultaneous position fits within `80 − (MYM 69 + MNQ 11) = 0` **at the current allocation** ⇒ **the allocation must be re-derived**, and neither incumbent may drop below the quantity its own panel actually used (MYM median 9, MNQ median 4). If no allocation satisfies this, C5 fails. |

**Accept H-CADENCE-1 if:** C1 **and** C2 **and** C3 **and** C4 **and** C5 all hold.

**Reject H-CADENCE-1 if:** C3 fails (quiet periods coincide), **or** C2 fails (the leg costs money to
run), **or** C4 fails (it degrades survival), **or** C5 fails (it cannot be sized alongside the book).

**Ambiguous-hold if:** C1 and C2 hold but the candidate's panel is shorter than 3 years or does not
overlap ≥60 of the incumbents' 80 idle weeks — C3 is then undecidable and **no leg may be licensed on
a C1+C2 pass alone.**

**Order of operations is part of the pre-registration.** C1 is measured and written into RESULTS
**before** C3 is computed. A RESULTS artifact reporting C1 and C3 in the same pass without the frozen
intermediate is void. Rationale: C3 is the limb most likely to be reached for post-hoc if C1 passes
handsomely.

---

## §5 — Forbidden moves

- **Spending M2K's K bank on this.** `M2K.md` M4 is explicit — bank 0, the widest headroom in the
  repo, *"spendable exactly once"*, `K_eff=1`, and any probe electing M2K must be sequenced against
  `WSTRUCT-M2K-1` **by the operator first**. A cadence leg is a low-value claim to spend the highest-value
  seat on. Phases 1–3 are panel-free by design; electing M2K is an operator decision at §8, not an author's.
- **Seeding a new edge claim on MNQ.** Family bank 2, floor 0.980, **at the Cap**. Closed.
- **Re-opening MYM opening-range-continuation.** DEAD; reconstruction TERMINAL (`96974de`). Also blocked
  operationally by **S3 order-symbol occupancy** — MYM1! Tue+Fri are closed while the Striker leg holds
  its TV alerts, so a MYM cadence leg cannot even be deployed without parking an incumbent.
- **Reading today's ORB-MNQ falsification as closing this question.** It falsified *one target*
  (payable standalone leg) *at one firm* — explicitly scoped, lifecycle not demoted, K not spent
  (`9b5ce43`). A minimum-size non-inferiority claim is a different bar. **Equally forbidden: reading
  that scope limit as permission to re-run ORB-MNQ's payability under a friendlier target.** The
  falsified target stays falsified.
- **Letting "it's only for cadence" admit a negative-expectancy leg.** If C2 fails, the leg is a
  maintenance trade with worse variance, a contract-cap cost, and a Pine surface to maintain —
  strictly worse than the thing it replaces. C2's bar is ≥0, and ≥0 is not negotiable downward.
- **Widening the search after seeing C1 fail.** One pre-committed construct. Screening several and
  reporting the best is a K-inflating search that this brief's `K_eff=1` framing does not cover, and
  it re-enters the SNAG/best-of-K graveyard.
- **Treating a RESOLVED verdict as authorization to arm or to re-tier.** `dry_run=false` still needs
  M1 `RESOLVED` at arm time + operator GO; sizing still needs the sibling ADR's own gate.
- **Touching the parameter axis.** No reshaping of Striker or Aegis. A reshaped incumbent is a new
  construct with its own pre-registration and its own K — not licensed here.

---

## §6 — Gate criteria

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | C1–C5 all pass | A cadence leg is licensable. Author a candidate pre-registration at `K_eff` per the elected instrument's bank; **operator GO required** before any manifest or pull. The maintenance-trade requirement (R8) is superseded for the eval, **not** for funded. |
| `FALSIFIED` | C3 fails, **or** C2 fails, **or** C4 fails, **or** C5 fails | Close at $0 / K=0. **The scheduled maintenance trade is the cheapest cadence instrument**, and R8 is confirmed as the correct — not merely expedient — remedy. Record the specific limb; a future re-open needs new evidence against *that* limb, not a restated preference. |
| `AMBIGUOUS-HOLD` | C1+C2 pass but the panel cannot decide C3 | Name the instrument and panel span that would decide it, and the cost dry-run to obtain it. **Do not license a leg on a partial verdict.** |

**Verdict-independent finding, recorded now:** whatever the outcome, `firm_rules.py` (`89a069a`)
already prices the inactivity barrier ON at **92.6–97.6% path death** with the mitigation undelivered.
Until either this brief RESOLVES or R8 ships, **every c1 pass-rate figure in the repo presumes a
cadence mitigation that does not exist.** That statement does not wait on this brief.

---

## §7 — Execution plan (Phases 1–3 are K=0, $0, no pull)

- **Phase 0** — re-verify §0 anchors; confirm M2K bank still 0 and no manifest touches RTY/M2K;
  land the 2026-08-03 panels into `core/data/tv_exports/cme/` with regenerated `SHA256SUMS`
  (repairs the `RESULTS.md` §0 provenance defect).
- **Phase 1 — freeze C1 from panels already on hand.** Compute weekly firing rate for candidate
  *shapes* (not instruments) using in-repo bar panels only. **Write C1 to RESULTS before Phase 3.**
- **Phase 2 — C5 first, because it is cheap and can kill the brief.** Re-derive the account-aggregate
  cap allocation for three legs against `LEG_MAP.cap_alloc`. If no allocation preserves MYM 9 / MNQ 4,
  **stop and return FALSIFIED** — no panel, no pull, no K.
- **Phase 3 — C3 against the incumbents' 80 idle weeks.** The gating limb. Requires only trade dates.
- **Phase 4 — C2 and C4**, contingent on C1+C3+C5 surviving. C4 reuses
  `lab/analysis/c1/c1_cadence_coverage_2026-08-03/run_coverage.py` unchanged (same geometry, same
  `cluster` proxy) with the candidate appended.
- **Phase 5 — verdict** against §6; land `lab/analysis/cadence_leg_2026-08/RESULTS.md`.

**Instrument election is deliberately absent from Phases 1–3.** The brief is written so the
expensive, K-spending choice is made *after* the cheap limbs have had their chance to kill it.

---

## §8 — Operator gate

Two decisions are the operator's, not the author's:

1. **Which instrument** hosts a candidate, if Phases 1–3 survive. Every admissible instrument spends
   a bank: M2K 0→1 (floor 0.650, the widest runway in the repo, one-shot, and sequenced behind
   `WSTRUCT-M2K-1`); MYM 1→2 (floor 0.850, plus the S3 occupancy blocker); MNQ closed at Cap.
2. **Whether to run this at all.** The measured alternative is ~13 maintenance trades/year at ~$1.82
   round-trip. This brief exists because that alternative was declined, not because the arithmetic
   favours it. **A FALSIFIED verdict here is a cheap, useful outcome** — it converts a preference into
   a priced decision.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Freeze-before-run: this pre-registration predates any result artifact.
git log --format='%h %ci' -1 -- docs/briefs/pre-registration/2026-08-03-c1-cadence-leg-preregistration.md
ls lab/analysis/cadence_leg_2026-08/ 2>/dev/null || echo "no results yet, as expected pre-run"

# 2. K unspent — no manifest may touch this question or the M2K/RTY family.
ls discovery_manifests/ | rg -i "cadence|m2k|rty" && echo "VIOLATION" || echo "OK: K unspent"
rg -n "K bank 0|spendable exactly once" ops/instruments/M2K.md

# 3. C1 was frozen BEFORE C3 (order-of-operations clause, §4).
rg -n "C1 frozen at|FROZEN BEFORE C3" lab/analysis/cadence_leg_2026-08/RESULTS.md 2>/dev/null

# 4. Closed guards still hold — MNQ at Cap, MYM TERMINAL + S3 occupancy.
rg -n "MNQ 2 -> floor 0.980|at cap" ops/instruments/M2K.md
rg -n "TERMINAL|S3 order-symbol occupancy" ops/instruments/MYM.md

# 5. Today's ORB falsification is scoped, not global — the scope clause must still read this way.
rg -n "scoped to \*\*one target at one firm\*\*|one target at one firm" \
  docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md CLAUDE.md

# 6. The verdict-independent finding is still true (R8 undelivered).
rg -n "92.6-97.6% path death|residual track R8" core/firm_rules.py

# 7. No parameter-axis drift.
# validate_params.py RETIRED 2026-08-03 (ADR 2026-08-03-params-toml-gate-retirement.md);
# successors are the pine-hash + skills-no-constants + path-liveness gates.
python scripts/check_pine_manifest.py && python scripts/check_skills_no_constants.py \n  && python scripts/check_path_liveness.py
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/pre-registration/2026-08-03-c1-cadence-leg-preregistration.md --type inquire

git log -1 --format='%h %ci' -- ops/instruments/M2K.md    # expect 249b30d
git log -1 --format='%h %ci' -- ops/instruments/MYM.md    # expect 96974de
git log -1 --format='%h %ci' -- ops/instruments/MNQ.md    # expect 6ef7d8a
git log -1 --format='%h %ci' -- core/firm_rules.py        # expect 89a069a
git log -1 --format='%h %ci' -- docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md  # expect 9b5ce43

# §2 arithmetic reproduces from the pinned panels
cd lab/analysis/c1/c1_cadence_coverage_2026-08-03 && python run_coverage.py --mym <path> --mnq <path> \
  | python -c "import json,sys; c=json.load(sys.stdin)['coverage']; print(c['idle_weeks'], c['co_idle_excess_pct'], c['projections']['incumbent_like']['residual_idle_after_1_to_5_legs'][0])"
# Expected: 80 14.6 39.1
```
