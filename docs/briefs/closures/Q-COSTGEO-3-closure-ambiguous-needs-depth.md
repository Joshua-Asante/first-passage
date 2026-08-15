# Q-COSTGEO-3 — Closure: `AMBIGUOUS-NEEDS-DEPTH` (measurement ran; level-1 is structurally too shallow for a 67-lot order)

**Verdict:** `AMBIGUOUS-NEEDS-DEPTH` — the pre-registered gate fired cleanly (D1 = 0.0% ≪ 90%). The instrument executed end-to-end; the level-1 schema cannot bound the cost because **the live order is far larger than the displayed book**, which is itself the finding.
**Closed:** 2026-07-24
**Pre-registration:** [`Q-COSTGEO-3-verdict-preregistration.md`](../pre-registration/Q-COSTGEO-3-verdict-preregistration.md) — `FROZEN`, signed 2026-07-23 / JA, freeze commit **`4aa9971`**
**Spend:** **$3.5767** (`tbbo`, 34 MYM event-days, exactly the verified estimate; budget gate passed at ceiling $4.00). **First paid databento pull in the cost-geometry line.**
**Live effect:** **none.** c1 rung stays WATCH-1 0.50× / disarmed; no cost constant changed; lock HELD. But this produces a **pre-B7 safety flag** — see §4.
**Artifacts:** [`lab/analysis/c1/c1_cost_geometry_mym_add_2026-07-24/measured.json`](../../../lab/analysis/c1/c1_cost_geometry_mym_add_2026-07-24/measured.json).

---

## 1. The measurement

MYM add cohort, 63 rows / 34 event-days, `tbbo`, fill-price localization (±1 tick, `America/New_York` DST-aware bar windows). **61 of 63 localized** (96.83%); the 2 unlocalized are both on 2023-09-12, the single degraded-liquidity day (9,128 records vs a ~60k median) — below the 10% `AMBIGUOUS-LOCALIZATION` gate, so localization itself is sound.

| Deliverable | Result | vs gate |
|---|---|---|
| **D1 — inside-sufficiency @ 67 lots** | **0.0%** (0 of 61) | ≪ 90% ⇒ **NEEDS-DEPTH** |
| **D2 — half-spread** | median **0.5 tick**, p90 1.0 | — |
| **D3 — measured floor** | **0.5 tick/side** | < modeled 1.0 |
| **`UNLOCALIZED`** | 3.17% (2/63) | < 10% ✓ |

**Inside-size distribution (contracts resting at the aggressing best quote, 61 events):** min 1 · p10 1 · **median 5** · p90 15 · **max 30**. The full sorted vector tops out at 30. **The 67-lot live add never once clears the inside** — it is **2.2× the deepest** top-of-book observed and **~13× the median.**

---

## 2. Verdict routing (§6, mechanical)

- `RESOLVED-CONSERVATIVE` needs D1 ≥ 90% — **fails** (0.0%).
- `FALSIFIED-UNDERSTATED` needs D3 ≥ 1.0 tick/side — **fails** (0.5).
- `AMBIGUOUS-LOCALIZATION` needs `UNLOCALIZED` ≥ 10% — **fails** (3.17%).
- **`AMBIGUOUS-NEEDS-DEPTH` needs D1 < 90% — FIRES** (0.0%).
- `ABORTED-BUDGET` — did not fire ($3.5767 < $4.00).

Clean single verdict.

---

## 3. Why D3 = 0.5 tick does **not** mean the model is conservative

The tempting misread — "measured floor 0.5 < modeled 1.0, so the model is safe" — is **wrong here**, and the pre-registration's floor-asymmetry clause plus the D1 validity condition both block it:

- D2/D3 (the half-spread) price **the first marginal lot** crossing the spread. They are the cost of the inside quote.
- **D1 = 0 means 67 lots do not fill at the inside.** The order exhausts the ~5 lots there and walks deeper. So the 0.5-tick half-spread is the cost of ~the first 5 lots, **not** of the 67-lot order.
- The modeled `SLIPPAGE_TICKS_PER_SIDE = 1.0` is not merely mis-valued — it is the **wrong model shape** for the add. A single-tick-crossing model cannot represent an order that sweeps multiple price levels. The right model for the add is depth-walk, and its depth is **unmeasured by level-1 data.**

**Directional read (honest, bounded):** because the order is an order of magnitude larger than the displayed inside, the modeled single-tick crossing is **near-certainly optimistic** on the add cohort — i.e. this leans toward the `FALSIFIED-UNDERSTATED` direction. But level-1 `tbbo` **cannot quantify by how much**, and — per the standing floor asymmetry — even full depth data would give a book-state upper bound, not realized-fill cost. Two things are still true and unmeasured: displayed depth ignores hidden/iceberg liquidity and replenishment, and the live add may be worked rather than swept in one marketable order. So the correct statement is **"the add's execution cost is materially undermodeled and its magnitude is unresolved,"** not a specific tick count.

---

## 4. Decision-relevant findings (the value delivered for $3.58)

1. **The largest live c1 order is ~13× median displayed depth.** The 67-lot MYM add cannot fill at the inside at any of 61 historical add-moments. This is a concrete, hardened liquidity fact about the leg that arms at B7 — previously unmeasured anywhere in the program.

2. **The modeled add cost is very likely optimistic, not conservative** (§3). If the operator wants the add's cost quantified before B7, `SLIPPAGE_TICKS_PER_SIDE = 1.0` on the add is the wrong instrument and needs replacement, not re-valuation.

3. **The "base cell trivially clears" pre-judgement is now in question.** At these add-moments even the 9-lot base would clear the inside only 15/61 times (25%). *Caveat:* those are add-moments (breakout continuation, thin book), not base-entry moments, so this does **not** measure the base cell — but it removes the basis for treating the base cell as safely foregone. A base-cohort measurement at base-entry moments is a distinct, cheap follow-on if wanted.

4. **The verified §0 discipline held.** Every §0 number that fed this run was pre-verified; the run reproduced the $3.5767 estimate to the cent and localized 96.83% of events. Zero mid-run surprises — the first instrument in this line to reach P4. The three prior Phase-0 halts bought the discipline that made this one clean.

---

## 5. The escalation the verdict points to (separate priced decision — NOT taken here)

`AMBIGUOUS-NEEDS-DEPTH` routes to depth. Sizing it now (free estimate, 2026-07-24):

- **`mbp-10`, MYM add, 34 event-days = $19.9136.** This would measure cumulative depth through 10 levels and let D1/D3 be computed against the *actual* 67-lot walk rather than the inside.
- Per §5 + §6 this is a **separate operator decision**, not authorized by the Q-COSTGEO-3 signature. It is ~5.6× this instrument's spend and ~$253 cheaper than the continuous-span `mbp-10` month the ADR anchored.
- **Recommendation deferred to the operator.** The $19.91 buys a quantified add-slippage floor (still book-state, not realized fills). Whether that clears B7's evidence bar is the operator's call; the qualitative finding (add ≫ displayed depth ⇒ modeled cost optimistic) is already in hand and may itself be sufficient to act on.

---

## 6. Process record

**No new PD.** The instrument executed as frozen. This is the payoff of the [Q-COSTGEO-2 closure §5](Q-COSTGEO-2-closure-aborted.md) lesson: with every §0 claim pre-verified, the run had no premise left to falsify at Phase 0.

**Methodology note (positive):** `AMBIGUOUS-NEEDS-DEPTH` was framed in the pre-registration as a near-disappointing "couldn't answer" outcome. In practice this instance is **decision-relevant on its own** — D1 = 0.0 (not 70%) is a strong signal, and the escalation it licenses is now evidence-backed rather than speculative. When a pre-registered "ambiguous" branch fires at an extreme value, the extremity is information; the closure should read the magnitude, not just the label.

---

## 7. Audit hooks

```bash
# Freeze predates the pull (freeze-before-result).
git log -1 --format='%h %ci' 4aa9971

# Reproduce the headline: 0 of 61 localized add-moments hold >= 67 at the inside; max inside = 30.
python -c "import json,statistics as st; d=json.load(open('lab/analysis/c1/c1_cost_geometry_mym_add_2026-07-24/measured.json')); \
s=sorted(r['inside_sz'] for r in d['localized']); \
print('n',len(s),'max',s[-1],'median',st.median(s),'>=67:',sum(x>=67 for x in s))"
#   expect: n 61  max 30  median 5  >=67: 0

# Verdict inputs vs §6 thresholds.
python -c "import json; s=json.load(open('lab/analysis/c1/c1_cost_geometry_mym_add_2026-07-24/measured.json'))['summary']; \
print('D1',s['D1_inside_sufficiency_all'],'D3',s['D3_measured_floor_ticks_per_side'],'unloc',s['unlocalized_rate'])"
#   expect: D1 0.0  D3 0.5  unloc 0.0317

# Spend matches the signed basis.
grep -n '"tbbo_cost_estimated_usd": 3.5767' lab/analysis/c1/c1_cost_geometry_mym_add_2026-07-24/measured.json
```

---

## 8. Addendum 2026-07-24 — panel cost model verified; edge concentration measured; execution-policy read

Three follow-on checks, all $0.00, run after the verdict. They **close** the "is the panel optimistic?" question this closure's §3 opened, and they change the practical disposition.

### 8a. The panel is NOT zero-cost — it charges exactly what the discovery model charges

Both venue editions read directly (Pine is gitignored but present locally; **both hashes match [`PORT_MANIFEST.sha256`](../../../core/strategies/PORT_MANIFEST.sha256)** — `2b895317…` MYM, `bb921399…` MNQ, so the 2026-07-17 manifest drift is repaired). Cost declarations are **identical** on both:

| `strategy()` setting | Value |
|---|---|
| `commission_type` / `commission_value` | `cash_per_contract` / **0.91** (Tradeify; comment notes 0.95 for MFFU runs) |
| **`slippage`** | **1** (Pine minticks **per fill**, applied adversely) |
| `process_orders_on_close` | `true` |
| `pyramiding` | 2 |

**So the panel charges 1 tick/side + $0.91/side — identical to `cost_mnq.SLIPPAGE_TICKS_PER_SIDE = 1.0`.** The concern that the c1 admission might rest on a zero-cost backtest is **refuted**. It was raised in-session as a question, not a finding; this is its resolution.

### 8b. The residual (size-invariance) is real but bounded, and MYM-specific

TV applies that 1 tick uniformly to the 9-lot base and the 67-lot add. §1 says 67 lots cannot clear a median-5 book, so the add is where size-invariance most plausibly breaks. Sensitivity per **extra** tick/side on the add cohort only:

| Leg | Add size | Adds | Cost per extra tick | % of that leg's panel net |
|---|---|---|---|---|
| **MYM** | 67 | 35 | $2,345 | **−3.0%** |
| **MNQ** | 30 | 47 | $1,410 | **−0.12%** |

At a pessimistic 4 ticks/side (4× model): MYM −$7,035 (**−9.0%** of $78,217); MNQ −$4,230 (**−0.36%** of $1,171,754). MNQ is ~25× less exposed — its add is 30 lots averaging $21,861, so slippage is noise against it. **MYM carries essentially all of this risk** (2.2× the contracts for ~1/15th the average payoff).

**Verdict on the panel:** the c1 admission evidence is **not materially at risk**. A single-digit-percent P&L drag on one leg of a two-leg book is a return-quality effect, not a drawdown-geometry effect, and the survivor-scoring gate is denominated in the latter. **No panel re-run is warranted.**

### 8c. Scope correction to this instrument's own framing

The Q-COSTGEO pre-registrations said the measurement feeds "the live c1 bust calibration." **That is looser than it should be.** `SLIPPAGE_TICKS_PER_SIDE`'s direct consumer is the **forward discovery cost-law gate**; the c1 bust number runs off `book_daily_at_100k(panel_c1)` — the TV panel's own P&L, with the panel's own (now-verified) cost settings. Correcting the constant does **not** move bust without a panel re-run. The finding's live relevance is **B7 execution safety**, which stands on its own.

### 8d. Edge concentration — the adds ARE the book

Panel P&L decomposed by entry-leg class (byte-pinned panels, one row per trade number):

| Leg | Base | **Add** |
|---|---|---|
| **MYM** | n=232, $28,487 (36.4%), avg $123 | **n=35, $49,729 (63.6%), avg $1,421** |
| **MNQ** | n=237, $144,269 (12.3%), avg $609 | **n=47, $1,027,486 (87.7%), avg $21,861** |

Extends the standing NAS100 finding (base-only PF 0.31) to MYM. **The thin-book order is also the order carrying the edge** — which is what makes the execution-policy question load-bearing rather than cosmetic.

### 8e. Execution-policy read (RECOMMENDATION — not an operator decision)

Order semantics verified: the rail sends **`order_type=market`, `tif=day`, no SL/TP** ([`RUNBOOK.md`](../../notes/rail_build/RUNBOOK.md) §2026-07-20 (c), payload semantics re-verified from `ops/c1_rail/crosstrade_payload.py`). So the 67-lot add is a single marketable order into a median-5 book.

**Recommendation: keep market orders.** The governing asymmetry is **adverse selection on non-fill** — a limit order fails to fill precisely when the market runs away fastest, which is when a momentum-continuation add is most profitable. You would not miss a random subset of adds; you would systematically miss the right tail carrying 64%/88% of P&L. Against that, even a 4× sweep-cost error is ~15% of an average MYM add. Paying to guarantee the fill is the correct side of the trade. Two supporting reasons: (1) **parity** — the panel assumes the add fills, and that panel is the basis of the Class-S admission; a non-fill-risk policy breaks the panel↔live correspondence (cf. the F3 per-candle parity doctrine); (2) **slicing is worse** — TWAP-ing into a breakout converts spread cost into drift cost, and adds partial-fill state to a sizing host whose `confirm_executed_base` contract is currently clean, days before arming.

**Do instead:** capture **per-fill add slippage at B7** and compare against the now-known panel basis of **1 tick/side**. That is the parked [Q-NAS-ECR-1](../../../STATE.md) instrument's shape (per-fill add slippage, observable on fill #1, cohort-split) — it now has a fill source. Realized fills settle in weeks what book state can only bound. During attended operation the operator is the circuit breaker, so an automated pathological-book guard is largely redundant; that calculus changes if the rail ever runs unattended.

**Consequent recommendation on the §5 escalation: do NOT spend the $19.91.** No lever exists to act on the number — add size is `floor(base × 7.5)` with pyramid 750% **LOCKED**, and running the authorization ladder to WATCH-2 0.25× still yields ~52 lots against median depth 5. No rung makes the add fit the book, so "measure depth, then size to fit" is not an available action. If the number is ever wanted, buy it **after** B7 supplies realized fills to calibrate against — then it purchases a model rather than a bound.

---

## 9. Change history

| Date | Change | By |
|---|---|---|
| 2026-07-24 | **Addendum §8** — panel cost model verified from both venue editions (hashes match PORT_MANIFEST): `slippage=1` tick/side + $0.91/side, **identical to `cost_mnq`** ⇒ the "panel may be zero-cost" concern is **refuted**; residual size-invariance quantified and bounded (MYM −3.0%/tick, MNQ −0.12%/tick) ⇒ **no panel re-run**. Scope correction: the constant's consumer is the forward cost-law gate, not the c1 bust calibration. Edge concentration measured: adds carry **63.6% (MYM) / 87.7% (MNQ)** of panel net. Execution-policy read: **keep market orders** (adverse selection on non-fill dominates sweep cost); **do not spend the $19.91** (no lever — pyramid 750% LOCKED, no rung fits the add to the book). | Joshua (direction) + Claude Code (Opus 4.8) |
| 2026-07-24 | Closed `AMBIGUOUS-NEEDS-DEPTH`. Ran end-to-end ($3.5767, budget gate passed): 61/63 localized, D1 = 0.0% (0 of 61 add-moments hold 67 at the inside; max inside 30, median 5), D2/D3 half-spread 0.5 tick, `UNLOCALIZED` 3.17%. Substantive finding: the 67-lot MYM add is ~13× median displayed depth, so the modeled 1.0 tick/side is the wrong model shape and near-certainly optimistic on the add — a pre-B7 safety flag, magnitude unresolved by level-1. `mbp-10` event-day escalation priced at $19.91 (separate operator decision, not taken). No live effect; lock HELD. | Joshua (direction) + Claude Code (Opus 4.8) |
