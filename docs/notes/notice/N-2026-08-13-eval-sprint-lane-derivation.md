# NOTICE 2026-08-13 — eval-sprint lane: retry economics vs the one-shot gate

**Type:** Notice-phase analysis. **Proposes; rules on nothing.** $0 · K=0 · no gate moved, no threshold changed, no candidate admitted, no account purchased. Adding an admission lane requires an operator election (§8).
**Trigger:** operator direction 2026-08-13 — *"move fast and aggressively towards finding a strategy… ok with trying unorthodox methods if the data supports it."*
**Discharges a caveat open since 2026-07-10:** the SelectFlex re-MC recorded *"bust<1% is FXIFY one-shot economics; Tradeify Flex is cheap-retry → the accept/reject gate is a NEW operator EV decision, do not inherit 1%."* That decision was never taken. [`Q-BUSTGATE-1`](../../briefs/closures/Q-BUSTGATE-1-closure-falsified.md) then measured the fee/upside asymmetry at **12–36:1** and concluded economics *"do not reproduce 3.0% and… point looser"* — and stopped there, correctly, because loosening on EV alone is the degeneration move. This note supplies the third input that was missing.
**Reads:** [`survivor-scoring prereg`](../../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) §3 · [`Q-BUSTGATE-1 closure`](../../briefs/closures/Q-BUSTGATE-1-closure-falsified.md) · [`design-box re-derivation`](N-2026-08-13-msl-design-box-rederivation.md) (the frontier solver reused here) · [`population notice`](N-2026-08-13-external-eval-population-data.md) §2 · `core/firm_rules.py` `Tradeify_Select_100K` @ HEAD.

---

## §1 — A structural fact about the gate that has never been stated

The frozen gate is **bust ≤ 3.0% ∧ P(pass) ≥ 50%**. Under the venue's verified **no-time-limit** rule, an evaluation has exactly two terminal outcomes — reach +$6,000 or breach the trail — so `P(pass) = 1 − P(bust)`.

> **The 50% pass floor is therefore never the binding limb. `bust ≤ 3.0%` *is* `P(pass) ≥ 97%`.**

The pass floor still does real work inside a *finite-horizon simulator* (it catches the no-trade grinder whose run is truncated before either barrier), which is what the prereg §3 rationale describes. But as a statement about the venue, the gate demands a **97% per-attempt pass rate**.

**Correction to my own prior note.** [`N-2026-08-13-external-eval-population-data`](N-2026-08-13-external-eval-population-data.md) §2 said our floor is "~3× the per-attempt population rate," comparing 50% against Tradeify's disclosed **17.2%**. The binding limb is 97%, so the true multiple is **5.6×**. That correction makes the gate stricter than previously recorded, not looser — and it is the reason this lane is worth deriving rather than assumed away.

## §2 — What a 97% per-attempt requirement costs, priced against a $169 reset

Reusing the [design-box](N-2026-08-13-msl-design-box-rederivation.md) frontier at **p=0.35, rr=3, index-micro RT $2.82**, sweeping per-trade risk `R`:

| R | P(pass) | bust | trading days/attempt | win-day $ | best-day vs 40% | E[attempts] | E[fees] | E[days to funded] |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **$181** (3% frontier) | 0.970 | 0.030 | 86 | $540 | 9.0% ✓ | 1.03 | **$270** | **89** |
| $300 | 0.883 | 0.117 | 51 | $897 | 15.0% ✓ | 1.13 | $287 | 58 |
| $400 | 0.802 | 0.198 | 38 | $1,197 | 20.0% ✓ | 1.25 | $307 | 48 |
| $600 | 0.662 | 0.338 | 25 | $1,797 | 30.0% ✓ | 1.51 | $351 | 38 |
| **$780** | 0.567 | 0.433 | **19** | $2,337 | **39.0%** ✓ | 1.76 | **$394** | **34** |
| $800 | 0.558 | 0.442 | 19 | $2,397 | 40.0% ⚠ at line | 1.79 | $399 | 34 |
| $1,000 | 0.480 | 0.520 | 15 | $2,997 | 50.0% ✗ | 2.08 | $448 | 31 |
| $3,000 | 0.197 | 0.803 | 5 | $8,997 | 150% ✗ | 5.08 | $954 | 25 |

`E[fees]` = $265 + (E[attempts]−1) × $169. E[days] = E[attempts] × days/attempt (an **upper** bound — busted attempts terminate early).

**The finding: the 40% consistency rule, not the trail, is what caps sprint sizing.** A single-win day at `rr=3` must satisfy `3R ≤ 0.40 × $6,000`, giving a hard ceiling of **R ≤ $800** independent of any survival argument. Everything below the line in the table is inadmissible on compliance grounds before survival is even discussed. This is a *pleasing* result: the venue's own rule bounds the aggressive tail far more tightly than the bust gate does, and it does so at a sizing (≈5 MYM contracts on a 320-pt stop) that sits nowhere near the 80-micro cap.

**Read the frontier row against the sprint row.** Holding the mechanism fixed, moving from R=$181 to R=$780 costs **$124 in expected fees** and buys **89 → 34 days**. That is the whole trade, and it is not close.

## §3 — What this actually buys, stated precisely (and what it does not)

**⚠ Correction to my own verbal framing when proposing this lane.** I described the November date as a passage deadline. It is not. TNEC-1's clause reads *"FALSIFIED if 2026-11-08 passes with **no N-clear candidate**"* — a candidate that *scores* as clearing N-ACT…N-SIZE discharges it. **No account need be funded, and days-to-pass is irrelevant to the falsifier.** Any argument for this lane that leans on the clock is wrong and I withdraw it.

So the lane's value is **not** speed against §4. It is this:

> **At the 3.0% gate, a mechanism must carry a gross edge of ≈0.50R/trade to reach the target inside ~62 trading days. At sprint sizing with retries, a mechanism at 0.20–0.40R becomes deployable with positive expected economics.**

Verified at the 3% frontier (rr=3): m₀=0.40 → 86 days · m₀=0.45 → 68 · **m₀=0.50 → 55 (first cell that fits 62)** · m₀=0.60 → 39.

For scale: **ORB-MNQ-1's realized edge was +0.063R.** C1's was negative. Nothing this estate has ever measured comes near 0.50R. **The 3.0% ceiling does not merely screen candidates — at any edge we have observed, it admits none.** That is the honest case for a second lane, and it is an argument about *reachability*, not about EV.

**What the lane does not do, and must never be read as doing:** it does not loosen the 3.0% gate, revive any falsified target (ORB stays dead on its own R2/R3 bars), or lower a mechanism-admission bar. Req 1a, EM0–EM5, the regime both-halves gate, and DSR-at-K are untouched. A candidate that fails on *edge* fails in both lanes identically — this lane changes only the **sizing/retry objective** applied to a mechanism whose edge is already measured and positive.

## §4 — The parallel-account question — UNVERIFIED, and load-bearing

If a trader may run several evaluations concurrently, the arithmetic changes sharply. At R=$780 (P=0.567, 19 trading days):

| Accounts | P(≥1 pass) | Fees | Wall-clock |
|---:|---:|---:|---:|
| 1 | 0.567 | $265 | 19 d |
| 2 | 0.813 | $530 | 19 d |
| 3 | 0.919 | $795 | 19 d |
| **4** | **0.965** | **$1,060** | **19 d** |

Four parallel accounts reach the conservative path's 97% confidence in **19 days instead of 89**, for ~$800 more.

> ⚠ **DO NOT ACT ON THIS TABLE.** The account-count rules it rests on — "max 5 simulated funded accounts, household-enforced; max 15 evaluations per rolling 30 days" — came from a **web-research summary and are not repo-verified**. `help.tradeify.co` returns **HTTP 403** to WebFetch (re-confirmed this session), so I could not check them at source. Per [[feedback_quotes_from_reader_summaries_are_not_quotes]] this stays quarantined until an authenticated in-browser read confirms it. **Owed before any election on §4:** primary-source confirmation of (a) concurrent-evaluation legality, (b) per-person/household account caps, (c) whether one bot on N own accounts collides with the §6.6 sole-ownership scan. Note (c) cuts the other way from the rest of §6.6 — same-direction copy across a trader's *own* accounts is explicitly the thing copy-trading rules contemplate, but that must be read, not assumed.

Fees were soft at authoring. **Primary re-read 2026-08-13** (in-browser on `tradeify.co`, Select · Tradovate · 100K Evaluation): list **$265**, checkout **$159** with code **AUG** (40% off ×5 then 30%; ends 2026-08-31 23:59 EST), reset **$169**, activation **None** — owner [`2026-08-13-tradeify-select-100k-checkout-price.md`](../programs/2026-08-13-tradeify-select-100k-checkout-price.md). The 2026-07-18 invoice (**paid $159**) stays historical in the GO ADR and is not overwritten. Promo-bound $159 expires with the AUG banner; re-read before any spend model that outlives 2026-08-31.

## §5 — Compliance shape (§6.5 is the binding text, not the trail)

FTA §6.5 requires *"avoiding maximum or larger contract sizes on single trades… maintaining consistent trading sizes, avoiding dollar-cost averaging."* The compliant sprint expression is therefore **consistent-but-larger**: one frozen contract count for the whole evaluation (≈5 MYM micros at R=$780 on a 320-pt stop), never escalation, never max-cap punts, never adds. This is compatible with the existing N-SHAPE no-pyramiding rule and with the 2026-08-13 hard-stop ruling.

**Sprint sizing is evaluation-only.** At R=$780 the same construct carries ~43% bust in the funded phase against the same $3,000 trail — which would destroy the funded account. Any candidate entering this lane must declare **two sizings**: sprint-R for the evaluation and frontier-R (bust ≤3%) on funding. This is exactly the behaviour the population evidence documents (*"oversize during evals and size down once they get funded"*), and it is why the funded-phase mortality item deferred on 2026-08-13 becomes live the moment this lane is used.

## §6 — Objective function, if the lane is elected

Replace the single-attempt gate with a pre-registered pair, both frozen before scoring:

- **Primary:** minimise `E[$ to first funded] = fee₁ + (E[attempts] − 1) × fee_reset`, subject to §6.5 consistency, the 40% cap (`R ≤ $800` at rr=3), N-ACT weekly cadence, and the $200 winning-day floor.
- **Guard:** `P(pass) ≥ 0.50` per attempt — retained as a genuine floor here (it is not redundant once the objective is retries rather than survival), preventing the lane from degenerating into lottery sizing.
- **Reported, never optimised:** funded-phase bust at frontier-R; E[days]; best-day/total ratio.

**E[value of a funded account] is deliberately absent.** It cannot be computed: the payout-count distribution is unpublished, and all we have is 28.5% of funded participants receiving *any* payout at a ~$2,000 average. Any EV ratio built on that would be a fabricated denominator. The lane is therefore justified on **reachability** (§3), not on a positive-EV claim — and an election should not be sold one as the other.

## §7 — What would falsify this lane

Pre-committed: **two candidates admitted via the sprint lane that reach funded and then die in the funded phase before a first payout** ⇒ the lane is producing eval-passers rather than strategies, and closes pending a superseding ADR. Cheap tell before that: a candidate whose sprint-R and frontier-R differ by more than ~4× is being carried by sizing rather than edge, and should be refused at pre-registration.

## §8 — Operator elections requested

1. **Open the lane?** Second admission route, sprint-R evaluation + frontier-R funded, objective per §6 — or hold the single 3.0% gate and accept that no measured edge in this estate can clear it.
2. **§4 parallel accounts** — authorise the primary-source verification (in-browser, `help.tradeify.co` 403s automated fetch), or drop the parallel arm and keep the lane single-account.
3. **Guard value** — `P(pass) ≥ 0.50` as written, or a different floor.
