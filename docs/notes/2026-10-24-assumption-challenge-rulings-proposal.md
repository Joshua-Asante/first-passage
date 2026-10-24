# Assumption challenge: seven constraints tested, proposed rulings (2026-10-24)

**Status:** PROPOSAL for operator review. Nothing here is a ruling. Every rule it names stays in force until Joshua rules.
**How to read it:** **§2 is the only current recommendation.** §3 records each chip's findings and its proposal **as returned**. Where a returned proposal differs from §2, it is marked **SUPERSEDED** and must not be executed. Revised after two reviews (consistency pass, 2026-10-24).
**Owner:** Portfolio Research Manager (PRM). **Rulings owner:** Joshua.
**Public-clone posture:** this report contains no account identifiers, account balances, budget amounts or backtest P&L. Dollar figures are either published firm rules or outputs of synthetic models. The underlying returns are private records held by the PRM; they are cited by content hash.

## 1. Why this exists

Joshua questioned seven standing constraints on 2026-10-24: "The aim is to remove unnecessary constraints, not lower the standard until a favourite strategy passes." Each one became a bounded, candidate-blind task (a "chip"):
- $0 spend;
- no strategy's results read;
- a pass/fail gate fixed in advance;
- a written proposal returned.

All seven passed their gates.

| Chip | Constraint questioned | Ran | Effort / bound | Return (private, hash) |
|---|---|---|---|---|
| 1 | Cash must arrive within 90 days | local | ~35 / 90 min | `68b3d784…` |
| 2 | Gross edge ≥ 4× trading costs | cloud | ~45 / 120 min | `bcd77e96…` |
| 3 | Size and withdrawals must be constant | cloud | ~75 / 180 min | `fa95fc84…` |
| 4 | The owned Select 100K must be the destination | local | ~75 / 150 min | `c7563fe9…` |
| 5 | Release 1 must be diversified, multi-firm or unattended | cloud | ~40 / 90 min | `60f2bb5f…` |
| 6 | Each component must meet the whole account's hurdle | cloud | ~40 / 120 min | `7072ddfb…` |
| 7 | Every step needs the same evidence | cloud | ~10 / 90 min | `2f20cd2e…` |

All seven spent $0 and added nothing to K.

**A related desk memo** on net cash versus account survival (`504c5f05…`) is summarised in §3.8.

**SR** throughout means the annualised Sharpe ratio of an assumed true, net-of-cost edge: mean daily profit ÷ daily standard deviation × √252. The chips assume one micro contract's day swings about $150, one standard deviation, so SR 2 is about $19 per contract per day, with about 55% winning days.

## 2. Current recommendation

**In one line:** endorse the principles, keep the detailed tests provisional, select no sizing, withdrawal or Flex/Daily policy yet, and have Joshua choose the operating horizon and cash-risk preferences deliberately.

### 2.1 Principles to endorse

| # | Principle | What it replaces |
|---|---|---|
| P1 (from R4) | **Qualify the whole policy, not each component.** The qualified object is the components, the sizing policy, the withdrawal and replacement policy, and the account rules. No component has a standalone performance hurdle | A standalone SR hurdle per component |
| P2 (from R3) | **Constant integer size per leg is the baseline** that any other sizing is compared against, fairly, under the relevant assumptions and stresses, including finite purchase limits. It is not a proven optimum, and challengers need not dominate every cell to be considered | An implicit assumption that size stays fixed |
| P3 (from R6) | **Start small:** release 1 is one strategy, one account, one firm, attended, with exposure that fits the attention budget. Each expansion has one trigger and one evidence item (§3, chip 5) | A diversified, multi-firm or unattended first release |
| P4 (from R7) | **Match the evidence to the decision:** a requirement binds a step only if it protects something that step uses up (cash, attention, K, unexamined data, an account) or a claim that step makes | The same evidence for every step |
| P5 (from R2) | **4× costs is a warning, not an economic law.** A candidate below 4× is disclosed, not automatically excluded. Until a calibrated net-edge test is adopted, admission rests on the reviewer, who sees the 4× ratio and the provisional test (§2.2) | 4× as an automatic exclusion |
| P6 (from R1) | **Separate the startup period from ongoing cadence, without survivor bias.** Every assessment reports two views: **(a) a common-start cohort**, covering every attempt from its first paid day, including attempts that never reach a payout, all money spent and elapsed time; and **(b) cadence conditional on reaching the payout stage.** View (b) never replaces view (a) | A single 90-day window counted from the first paid attempt |
| P7 (from R5) | **Keep the owned Select 100K while it costs $0 in cash, and buy nothing now** | — |

**For P6:** a quarter with no payout and a quarter with negative cash are different events, and both are reported. D1's window already starts at the first paid attempt and excludes build time, so extending the paid-attempt runway to six months is a **substantive economic change**, not a recognition of development time.

### 2.2 Provisional: report, don't gate

- **R2's net-edge formula** (LCB = ρ·δ_sel − c₊₂ − 1.96σ/√N): computed and disclosed, but not binding.
  - The best-of-K shrink is not a calibrated confidence bound.
  - Dependence, effective sample size and cost uncertainty are not yet handled.
  - **No admission code changes.**
- **R4's marginal-contribution tests:** report Δ E[net cash], Δ P(no payout), Δ P(cash-negative quarter) and Δ P(breach) as a tradeoff.
  - If a gate is later wanted, it must be **non-inferiority within an explicit acceptable margin**. "Not significantly worse" is not enough, because a small sample passes it by failing to detect harm.
  - **The comonotone shortcut** (summing each component's own intraday low) is a conservative survival check only under fixed, compatible paths. It does not validate the complete policy where sizing, stops, liquidation or withdrawals change those paths.
- **R7's power arithmetic** (about 240 sessions for power 0.5 at SR 2): applies only to forward observation offered as D4 profitability evidence, under its stated assumptions. It is not a universal time to qualification.
  - Native diagnostics and canaries do not inherit it.
  - Data-use permissions and host isolation still apply to them, even without real trading.

### 2.3 Not selected yet

- **Sizing beyond the baseline.**
- **The withdrawal policy.** No common comparison exists (§3.8, §3.9).
- **Flex versus Daily.** The choice is permanent at activation.
- **Any purchase vehicle.** Chip 4's SR 2.0–2.5 break-evens and its 50K ranking are model-conditional guides, not admission gates.

### 2.4 Choices for Joshua (deliberate, not inherited)

1. **Operating horizon(s)** for comparing total net cash. Runway length and cadence period.
2. **Cash-risk preferences on the cohort view:**
   - acceptable P(cash-negative) and finite cash downside (for example P(N ≤ −$X));
   - acceptable P(no payout) per quarter;
   - whether to keep E1's X3 ≤ 10% election.

   These are chosen directly. An account-breach limit is not inherited from earlier models.
3. **Continuation value:** whether a total economic-value comparison may add discounted future payouts beyond the horizon. Any such value is shown separately and never counted as bank cash (§3.9).
4. **Owned evaluation at the 11-08 sitting:** keep or lapse; a standing, revocable weekly-trade GO; the review cadence.
5. **Paid pilots:** which of S5 and D1 governs them, and whether a pilot-only evaluation is step 6 or step 7.

**What the endorsements remove:**
- the 90-day-only window;
- 4× as an automatic exclusion;
- the standalone component hurdle;
- the operator GO for $0 probes on examined data;
- a multi-firm or unattended first release.

**What they keep:**
- D4's untouched validation for deployment;
- D6;
- statistical power for forward profitability evidence;
- reviewer judgment on costs until a calibrated test exists.

**Honest note:** P5 removes an automatic exclusion before its replacement is calibrated. During that gap the protection is the reviewer's disclosed judgment, not a formula.

## 3. Chip findings in detail

### Chip 1 — the startup runway and payout cadence (feeds P6)

**What the 90-day window measures:**
- D1's window starts at the first paid attempt.
- The venue minimum to a first bank payout is about three weeks: three evaluation days, five Flex winning days and about seven bank days.
- In E1's synthetic model, at every tested SR and under both return laws, the window closes before a typical path's first payout. 74–98% of paths are still active at day 90.

**Why a plain 180-day window would lower the standard:**
- Doubling it raises pass probability by about the same amount (+0.15 to +0.19) at zero edge as at SR 2. That gain is diffusion, not skill.
- Funded payouts can be drawn from the cushion even at zero edge.

**Returned proposal** (**SUPERSEDED in part by §2.1 P6:** the cadence clock must not replace the common-start cohort):
- a runway of at most six months, shorter when the budget cannot carry fixed costs;
- quarterly cadence after the first payout;
- a longer runway counts only if post-runway quarterly cash improves at equal budget and risk;
- a zero-edge law must stay non-qualifying.

**Limits:**
- E1 cannot run 180 days without code changes, so the 180-day figures are closed-form approximations.
- Above roughly $75 a month of recurring cost, the budget caps the runway at about three months.

### Chip 2 — the 4× cost multiple (feeds P5)

**Origin.** 4× is a convention: `MIN_RMULT = 4.0` → the cost-geometry pre-gate → ADR 2026-07-16 → `strategy_harvest.md` §1 Requirement 5. It absorbs a 4× cost error or 25% retention, and has no term for N, σ or K.

**Returned test** (**PROVISIONAL, §2.2**):

LCB = ρ·δ_sel − c₊₂ − 1.96·σ/√N > 0

- δ_sel: shrunk for best-of-K by e_K·σ/√N_est (e_K = 0, 0.564, 0.846 for K = 1, 2, 3);
- ρ: retention, at most 0.70, and 0.50 if undeclared;
- c₊₂: cost plus two ticks per side.

**Synthetic cases (basis points; c₀ = 1.5, so 4c₀ = 6.0):**

| Case | δ (× c₀) | Today | LCB | Returned test |
|---|---|---|---|---|
| A: robust, high N, low σ | 5.0 (3.3×) | dropped | +0.39 | admit |
| A′: same, ρ = 0.5 | 5.0 | dropped | −0.61 | reject |
| B1: thin N, high σ | 7.5 (5.0×) | admitted | −3.13 | reject |
| B2: best of K = 3 | 7.0 (4.7×) | admitted | −0.15 | reject |
| B3: large edge, drawdown at one lot | 12.0 (8.0×) | admitted | +1.04 | admit |

**Caveats:**
- Case A passes only at ρ = 0.70.
- B3's drawdown risk is caught by neither rule.
- Coverage is uncalibrated, and "stricter" is not itself evidence of better decisions.

**Returned implementation list:** the ADR 2026-07-16 revision, the strategy_harvest edits and the `register_search._require_cost_law` LCB. **SUPERSEDED:** no doc or code change until a calibrated test is adopted (§2.2).

### Chip 3 — stage-aware sizing and withdrawal (feeds P2)

**Design:**
- A standalone Select 100K simulator, evaluation → funded (Flex or Daily), with an intraday-checked trailing floor, consistency, the lock and the payout rules.
- 20,000 paths over 180 days, at SR 0.5–3, under a normal and a t(3) law.
- The policy family and the gate were frozen and hashed before any code ran.
- Constant size was tested at 20 sizes.
- **Unlimited resets were allowed.**

**Result:** no tested policy beat constant size in every cell, but several won conditionally.

| Policy | Cells won (of 12) | Where it helps |
|---|---|---|
| P1, cushion-proportional | 4 Flex / 6 Daily | Fat tails |
| P2, consistency taper near target | 3 Flex / 0 Daily | Low SR, normal law |
| P3, stage-aware | 1 Flex / 6 Daily | Fat tails; from sizing, not withdrawal |
| Cushion-preserving withdrawal alone | 0 | — |

**Returned proposal:** constant size; greedy withdrawal; challengers must win every cell. **SUPERSEDED by §2.1 P2 and §2.3:**
- constant size is a baseline, not the rule;
- no withdrawal policy is selected;
- challengers need fair comparison, not universal dominance;
- results under unlimited resets cannot establish the optimum under finite purchase limits.

**Side finding:** the expected-cash-maximising constant size breaches with probability 0.96–1.00 under unlimited resets. This is not a sizing result. It shows that expected cash alone is not a decision rule.

**Limits:**
- the rules were read through a mirror;
- the Daily loss limit and the Daily ladder are assumed;
- days are i.i.d.

### Chip 4 — the owned Select 100K against its alternatives (feeds P7)

**Options compared:** keep the owned evaluation (fee sunk); lapse and buy a new Select 25K, 50K or 100K; a small personal account; no deployment. They were tested on synthetic edges at 90 and 180 days, in central and conservative cases.

**Findings (model-conditional):**
1. Keeping the owned account beats every feasible alternative in expected cash at every tested SR while it costs $0 in cash. Keep vs lapse turns on upkeep against the chance a qualified native strategy arrives.
2. Wherever buying paid in this model, a Select 50K beat the 25K and the 100K.
3. A small personal account never ranked best while the owned evaluation was kept.
4. At SR 0, purchases and the personal account lose. The owned account's small zero-edge gain is cushion harvest with the fee sunk. D6 keeps it off-limits for unqualified strategies.

**Break-even SR** (90 / 180 days), **guides only** (§2.3):

| Comparison | Central | Conservative |
|---|---|---|
| A purchase beats none | 1.0 / 1.0 | 2.5 / 2.0 |
| A purchase beats the personal account | 1.5 / 1.0 | 2.5 / 2.0 |
| The personal account beats none | 0.5 / 1.0 | 1.5 / 2.0 |
| A new 50K matches the owned account | ≈ 3 / ≈ 3 | > 3 / ≈ 3 |

**Returned proposal for 11-08:**
- keep the account;
- $0 recurring cash, with any charge ending it;
- an 8-week review;
- a standing weekly-trade GO;
- "model no purchase until validated SR supports 2.5 (2.0 with a runway), then the 50K only".

**The last item is SUPERSEDED:** keep "buy nothing now" only, and leave vehicle comparison open.

**Limits:** i.i.d. sessions with fixed volatility; no continuation value; kinder to purchases than E1.

### Chip 5 — the smallest first release (feeds P3)

**Joshua's input:** more than 15 attended hours a week, weekdays 09:30–16:45 ET, no evenings.

**Release 1:** one strategy, one account, one firm, attended, with exposure inside 09:30–16:00 ET.
- One leg removes U-2, the D-N2 priority rank and the same-instrument rules.
- Attended operation removes the dependence on the D-N1 incident close (U-17).
- **Still needed:** the three native canary items, plus U-1, U-3, U-6, U-7, U-9–U-14 and U-16.

**Attention:** operating time ≈ 5E + 3.75 hours a week, where E is exposure hours per weekday, so E ≤ (H − 3.75)/5. That gives E ≤ 2.25 h a day at 15 h a week. These are estimates; replace them with canary timings.

**Expansions:**

| Expansion | Trigger | Evidence |
|---|---|---|
| Second strategy | Improves the complete policy's tradeoffs | A pre-registered joint simulation of the whole account policy |
| Unattended operation | Restart and recovery demonstrated | A release-1 recovery record: every case reaches verified flat, or stays bounded by a broker-resident stop, without operator action, and pages the operator |
| Second firm | The first firm's limits cap growth | A cash-cadence record that names the blocking limit, plus a qualified strategy for that firm (same-bot bar) |
| Activity leg | The weekly trade can't be met more cheaply | A weekly-coverage record (low-frequency only) |

**A second account at the same firm** is justified only by cost and cadence, not risk: copies move together (§3.8).

### Chip 6 — qualify the complete policy (feeds P1)

**Synthetic cases** (Select Flex 100K funded, 250 days, 20,000 paths, 5-minute steps):

| Case | Added component's SR | Δ E[cash] | Δ P(breach) | Δ P(no payout) | SR-2 hurdle | Marginal view |
|---|---|---|---|---|---|---|
| (a-i) wins on the other's losing days | 0.72 | +$3,255 | −0.27 | −0.10 | rejects (wrong) | admits |
| (a-ii) fills the $200 winning days | 0.79 | +$2,684 | +0.35 | −0.40 | rejects (wrong) | admits only if replacement is allowed |
| (b) shares a 09:30 dip that recovers by the close | 2.51 | −$1,604 | +0.24 before first payout | +0.23 | admits (wrong) | rejects |

**Daily evidence is not enough.**
- In (b), an end-of-day model gives Δ cash +$3,922 against the true −$1,604.
- A variant with identical daily statistics but the dip at 14:00 is genuinely positive.

**Returned proposal:** admit if LCB Δ cash > 0 and Δ P(no payout) is "not significantly above 0"; use the comonotone bound when joint paths are missing. **SUPERSEDED by §2.2:** report as a tradeoff; any future gate uses non-inferiority with an explicit margin; the comonotone shortcut is narrowed.

**Notes:**
- Chips 3 and 6 used different withdrawal rules.
- (a-ii) raises P(breach) by 0.35.
- (a-ii) wins only with replacement, which current purchase limits rule out.

**Engine gap:** `core/mc/simulation.py::simulate_path` takes one `intraday_low` per day and has no payout or withdrawal model.

### Chip 7 — evidence matched to what each step risks (feeds P4)

| Step | Resolves | Needs | Does not need |
|---|---|---|---|
| 1. Zero-cost read | Whether a question deserves a costlier step | The pre-Q gate; K if it selects. On unexamined data: reservation, exposure entry, committed statistic, operator GO | On examined data: GO, Req 1–5, D1/D4/D6 |
| 2. Mechanism depth check | Whether a mechanism exists and its size | Req 1's before-data clauses; discriminator, statistic and K ≤ 3 committed before the read; 4× as a disclosed reference line | GO at $0 on examined data; D1/D4/D6 |
| 3. Paid data | The right to test on new data | Req 1, 2 and 4; reviewer cost judgment (P5); a campaign envelope with a GO under D1; an approved vendor; licence terms | Canary, D4, D6, M1 |
| 4. Native canary | Whether the code matches the frozen spec | A frozen spec; synthetic or examined data; **data-use permissions and host isolation** | Profitability sample size; D4, D6, M1. **A pass is never economic evidence** |
| 5. Sim forward observation | Performance on unseen data | A canary pass; statistic, cost model and stop rules frozen; **N set by power if offered as D4 profitability evidence** | D1, D6, M1 |
| 6. Paid pilot | Real fills and costs; operating load | D1 economic evidence; native correctness; permissions; separate GO; M1 and per-session GO for any live send | D4. Never on the owned evaluation |
| 7. Evaluation or funded deployment | Whether it earns at the venue's geometry | D4, D6, venue fit, lifecycle admission, cost judgment at the venue's costs, canary, permissions, M1, arming, per-session GO | Nothing removed |

**Power arithmetic** (PRM-checked; it applies only as stated in §2.2):
- daily P&L at SR 1.5 over 40 sessions gives power ≈ 0.09;
- power 0.5 needs about 430 sessions at SR 1.5, and about 240 at SR 2.

**Returned wording:** an addendum to `docs/adr/2026-08-30-evaluation-order.md`, plus edits to the candidate-contract probe clause, the Req 5 depth-check note and the forward-observation N rule. These follow only after Joshua endorses P4.

### 3.8 Related evidence: net cash generation vs account survival (desk memo, not a chip)

**Source:** a separate desk session's memo (private, `504c5f05…`). It uses E1's stored 90-day results (synthetic, new Select 50K Flex), closed-form lifetime arithmetic and Tradeify's payout page. No new simulation, $0, K += 0.

1. **Zero edge, scoped.**
   - In the memo's closed-form model (IID, reflecting at cushion K, run to ruin, no caps), expected lifetime withdrawals equal the starting cushion under any withdrawal policy.
   - That is a model result. Negative net cash also needs the acquisition and replacement economics.
   - It is consistent with chip 4's small zero-edge gain on the owned account (fee sunk), which is a conditional funded-account result, not the full lifecycle, and no case for trading without edge.
2. **At SR ≤ 1.5, negative is not the same as inadmissible.** In E1, G SR 1 at 3 MES has −$63 expected cash, while G SR 1 at 4 MES has +$116 but X3 50%. "Nothing qualifies" does not mean not trading has the highest expected cash.
3. **More size is not one direction of risk.** At G SR 2, going from 3 to 4 MES (wait):
   - raises E[N] from $206 to $481 and lowers P(N < 0) from 67% to 57%;
   - but raises P(N ≤ −$300) from 47% to 55% and X3 from 9.1% to 36%.

   It loses less often, and more severely when it loses.
4. **Earlier payouts have a price.** At G SR 2, 3 MES, first eligibility vs waiting:
   - E[N] falls from $206 to $161;
   - P(N < 0) falls from 67% to 62%;
   - P(N ≤ −$300) falls from 47% to 39%.

   This prices the preference for frequent modest payouts; it does not make either choice irrational. E1 and chip 3 compared different withdrawal policies, programs and comparators, so **no common winner exists.**
5. **Lifetime figures are illustrations only.** The memo's sensitivities (a $3,000 cushion ≈ 29× an early-request cushion at SR 2; Daily about 25–40% below Flex on 100K) compare remaining continuation from non-comparable states. They are unverified and not a basis for choosing a withdrawal policy.
6. **Select Daily** suits frequent payouts: daily eligibility, no winning-day threshold, an enforced buffer. The choice is permanent at activation.
7. **Copying one strategy across accounts is leverage, not diversification.**
8. **What to seek:**
   - net edge first;
   - under Flex, frequency counted in qualifying days ($200 on 100K, $150 on 50K);
   - profit spread across days;
   - left tails decide survival.

**E1-P** (Daily, fixed-cushion Flex, one de-risk rule; ≤ 3 h build + 1 h review) is listed but not recommended until a candidate has edge evidence.

### 3.9 Definitions and decision comparison

**Definitions:**
- **N_T:** bank-received net cash at horizon T, after all fees and costs.
- **X3:** E1's elected tolerance event: no active account at T **and** N_T < 0. It is neither P(N_T < 0) nor a breach rate.
- **P(breach):** the probability an account hits its floor. It has no adopted limit.
- **P(no payout in a quarter)** and **P(cash-negative in a quarter):** different events, and both are reported.
- **Continuation value:** future net payouts a surviving account can credibly produce beyond the horizon.
  - A total economic-value comparison may add cash received plus discounted continuation, provided nothing is double-counted.
  - That total is always shown separately, never presented as bank cash, and never used to satisfy a cash-payment requirement.
  - A nominal balance is not wealth, and survival is not an objective in itself.

**Decision comparison: accepted E1 results only.**
- New Select 50K Flex; 90 days, about one quarter; σ $150 per MES; up to 4 purchases with replacement; seed B, 20,000 paths.
- Original labels are kept.
- **These are synthetic new-50K results, not recommendations for the owned account. No row shows dependable quarterly income.**

| Law, SR | MES, withdrawal | E[N] | P(N < 0) | P(no payout) | P(N ≤ −$300) | X3 | Requests / 90d |
|---|---|---|---|---|---|---|---|
| G, 2 | 3, wait (selected) | $206 | 67% | 67% | 47% | 9.1% | 0.59 |
| G, 2 | 3, first | $161 | 62% | 53% | 39% | 10.2% | 0.77 |
| G, 2 | 4, wait | $481 | 57% | 57% | 55% | 36% | 0.79 |
| G, 2 | 4, first | $422 | 55% | 48% | 47% | 36% | 0.89 |
| K, 2 | 3, wait | $9 | 82% | 82% | 36% | 3.1% | 0.31 |
| K, 2 | 4, wait | $39 | 78% | 78% | 67% | 22% | 0.36 |

**The current evidence does not select one cash-generation policy.** It exposes real tradeoffs between expected cash, frequency of loss, severity of loss and payout timing. Joshua's choices in §2.4 decide between them.

## 4. What the results mean together

1. **The first bottleneck is a credible candidate,** with net edge and account fit. Validation time comes after that, and depends on the evidence route and its assumptions. The ~240-session figure is one forward-power case at 50% power, not a universal requirement. Historical data no one in the selection chain has examined can shorten validation where it exists.
2. **Attention narrows the search (P3).** At about 15 attended hours a week, a candidate's exposure must fit about 2.25 hours a day inside 09:30–16:00 ET. The overnight territory waits until unattended operation is earned.
3. **Expected cash alone is not a decision rule.**
   - Chip 3's expected-cash-maximising size breaches almost surely under unlimited resets.
   - In E1, more size trades fewer losses for larger ones.
   - Cash-risk preferences have to be chosen (§2.4).
4. **Survival is not the prize; future cash is.** The choices that remain are the horizon and the cash-risk preferences. More simulation is not what's missing.

## 5. Follow-ups, only after Joshua rules

| Item | Depends on |
|---|---|
| Record the endorsed principles (P1–P7) with their owners: D1 wording (P6), qualification screen (P1, P2), release-1 rule (P3), evaluation-order addendum (P4), Req 5 note that 4× is a warning (P5) | §2.1 endorsement |
| Calibrate the net-edge test (coverage, dependence, effective N, cost uncertainty) before any code change | P5 |
| `core/mc` engine: summed-path intraday low, payout and withdrawal model | Before the P1 tradeoffs are computed for real candidates |
| Cohort and cadence reporting in E1 (P-E1H), with the null control (needs approval) | P6 and the horizon choice |
| One pre-registered withdrawal policy; re-check chip 6 case (a-ii) under it | §2.4 choices |
| E1-P (Daily, fixed-cushion Flex, one de-risk rule) | A candidate with edge evidence |
| Replace chip 5's hour estimates with canary timings | The 2026-10-26 canary |

## 6. Decisions requested from Joshua

1. Endorse principles P1–P7 (§2.1), in whole or in part.
2. Confirm that the detailed tests stay provisional (§2.2), and that sizing, withdrawal, Flex/Daily and purchases are not yet selected (§2.3).
3. The choices in §2.4:
   - operating horizon(s);
   - cash-risk preferences on the common-start cohort;
   - the continuation-value treatment;
   - the owned evaluation at 11-08;
   - S5 vs D1 for paid pilots.
