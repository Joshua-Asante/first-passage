# Assumption challenge: seven constraints tested, proposed rulings (2026-10-24)

**Status:** PROPOSAL for operator review. Nothing here is a ruling; every rule it names stays in force until Joshua rules.
**Owner:** Portfolio Research Manager (PRM). **Rulings owner:** Joshua.
**Public-clone posture:** this report has no account identifiers, account balances, budget amounts or backtest P&L. Dollar figures are either published firm rules or outputs of synthetic models. The underlying returns are private records held by the PRM; they are cited by content hash below.

## 1. Why this exists

Joshua questioned seven standing constraints on 2026-10-24: "The aim is to remove unnecessary constraints, not lower the standard until a favourite strategy passes." Each one became a bounded, candidate-blind task ("chip"):
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

All seven chips spent $0 and added nothing to K.

**SR** throughout means the annualised Sharpe ratio of an assumed true, net-of-cost edge:
- mean daily profit ÷ daily standard deviation × √252;
- the chips assume one micro contract's day swings about $150, one standard deviation;
- SR 2 is about $19 per contract per day, with about 55% winning days.

## 2. Summary of proposed rulings

| # | Constraint | Proposed ruling | PRM | Joshua's input needed |
|---|---|---|---|---|
| R1 | 90-day cash window | Split into a startup **runway** (≤ 6 months, budget-limited) and a **quarterly cadence**, with a zero-edge null control | Adopt | Quarterly no-payout limit p_Q |
| R2 | 4× cost hurdle | 4× stops being an automatic exclusion and becomes a disclosed warning. The proposed net-edge test (retention ρ, tick stress, selection shrink) is **provisional**: the shrink is not a calibrated confidence bound | Adopt the direction; calibrate the test before it binds | — |
| R3 | Constant size and withdrawal | Constant integer size per leg is the **baseline**, not a proven optimum. Adaptive policies showed conditional gains, and must be compared fairly under the relevant assumptions and stresses, including finite purchase limits. **No withdrawal policy is selected** (§3.9) | Adopt as baseline | Operating horizon(s) for cash comparison (§6) |
| R4 | Component hurdle | Policies qualify, components don't; marginal-contribution test on joint intraday paths | Adopt with R3 | — |
| R5 | Owned 100K as destination | Keep it while it costs $0 in cash; buy nothing now. The synthetic SR 2.0–2.5 break-evens and the 50K ranking are **model-conditional** guides, not admission gates; vehicle comparison stays open | Adopt "keep, buy nothing now" at the 11-08 sitting | Standing weekly-trade GO? Review cadence |
| R6 | First-release scope | One strategy, one account, one firm, attended; exposure fits the attention budget; each expansion has one trigger and one evidence item | Adopt | — |
| R7 | Uniform evidence | Step-risk evidence ladder: each requirement binds only the steps it protects | Adopt | Which of S5 and D1 governs paid pilots; whether a pilot-only evaluation is a pilot or a deployment |

**Net effect:**
- **Removed or narrowed:**
  - the 90-day-only window;
  - 4× as an exclusion;
  - the standalone component hurdle;
  - the operator GO for $0 probes on examined data;
  - a multi-firm or unattended first release.
- **Kept or tightened:**
  - D4's untouched validation for deployment;
  - D6;
  - a cost test stressed for slippage and shrunk for selection;
  - statistical power for forward evidence;
  - explicit breach and no-payout limits.
- **Not loosened:** the standard itself. Where a constraint was removed, the replacement is at least as demanding on the risk it protected.

## 3. Chip findings in detail

### Chip 1 — separate the startup runway from the payout cadence (R1)

**What the 90-day window actually measures.**
- D1's window already starts at the first paid attempt, so build time sits outside it.
- The venue minimum to a first bank payout is about three weeks:
  - three evaluation days;
  - five Flex winning days;
  - about seven bank days.
- In E1's synthetic model, at every tested SR and under both return laws, the window closes before a typical path's first payout. 74–98% of paths are still active at day 90, so their later losses go uncounted.
- The window measures almost no ongoing earning.

**Why a plain 180-day window would lower the standard.**
- Doubling the window raises pass probability by about the same amount (+0.15 to +0.19) at zero edge as at SR 2. That gain is diffusion, not skill.
- Funded payouts can be drawn from the cushion even at zero edge. A longer horizon would count them as cash.

**Proposal:**
- A **runway** from the first paid attempt to the first bank-received payout:
  - at most six months;
  - shorter when the stage-2 budget cannot carry the route's monthly fixed costs after its fees.
- Then a **quarterly cadence**: expected bank-received net cash, and P(no payout in a quarter).
- **Admission:** a runway beyond 90 days counts only if it raises post-runway quarterly cash at equal budget and risk. Pass probability alone never counts.
- **Qualification** needs a positive lower bound in each of the first two post-runway quarters, and **a zero-edge law must stay non-qualifying** (the null control).
- E1's 90-day labels stand until a split-horizon run (P-E1H) is approved and accepted.

**Limits:**
- E1 cannot run 180 days without code changes, so the 180-day figures are closed-form approximations.
- The split is only workable if recurring data costs stay low. Above roughly $75 a month the budget caps the runway at three months.

**Would reverse:** zero edge qualifying in a split run; high data costs; a preference for first cash within 90 days; venue payout-timing changes.

### Chip 2 — the 4× cost multiple (R2)

**Origin.** 4× is a convention: `MIN_RMULT = 4.0` → the cost-geometry pre-gate → ADR 2026-07-16 → `strategy_harvest.md` §1 Requirement 5. It absorbs a 4× cost error or 25% retention. It has no term for sample size N, volatility σ, or selection K.

**Proposed binding test:**

LCB = ρ·δ_sel − c₊₂ − 1.96·σ/√N > 0

- δ_sel: the conservative cohort edge, shrunk for best-of-K selection by e_K·σ/√N_est (e_K = 0, 0.564, 0.846 for K = 1, 2, 3);
- ρ: declared live retention, at most 0.70, and 0.50 if undeclared;
- c₊₂: round-trip cost plus two extra ticks per side.

4× remains a mandatory disclosed BELOW-4× flag.

**Synthetic cases (basis points; c₀ = 1.5, so 4c₀ = 6.0):**

| Case | δ (× c₀) | Today | New LCB | New test |
|---|---|---|---|---|
| A: robust, high N, low σ | 5.0 (3.3×) | dropped | +0.39 | admit |
| A′: same, ρ = 0.5 | 5.0 | dropped | −0.61 | reject |
| B1: thin N, high σ | 7.5 (5.0×) | admitted | −3.13 | reject |
| B2: best of K = 3 | 7.0 (4.7×) | admitted | −0.15 | reject |
| B3: large edge, drawdown at one lot | 12.0 (8.0×) | admitted | +1.04 | admit |

**In realistic intraday regimes the test is mostly stricter than 4×.** Earlier kills (D5, H-OD-1) still fail.

**Provisional (after review):**
- Subtracting the expected best-of-K bias does not by itself give a confidence bound with calibrated coverage. Dependence, effective sample size and cost uncertainty all matter.
- ρ, the tick stress and the shrink are proposals to calibrate, not settled parameters.
- "Stricter" is not itself evidence of better decisions.

**PRM caveats:**
- Case A is admitted only at ρ = 0.70, so any loosening rests on justifying that retention.
- B3's drawdown risk is caught by neither rule; survivor scoring against the account envelope stays binding.

**Changes if adopted:**
- a dated revision of ADR 2026-07-16 §2 item 2;
- the strategy_harvest §1 Requirement 5 row, its relief valve, §2.2, §2.1 Tiers B and C, and the §8 audit hook;
- code: `register_search._require_cost_law` computes the LCB instead of refusing below 4×;
- the discovery-campaign template row 0;
- the strategy-validation §2 cross-reference.

**Would reverse:** slippage tails beyond model + 2 ticks; realised retention below ρ; σ or N unknowable at sourcing (keep 4× at §2.2); a below-4× admit that later dies on cost.

### Chip 3 — stage-aware sizing and withdrawal (R3)

**Design:**
- A standalone simulator of Select 100K, evaluation → funded (Flex or Daily):
  - an intraday-checked trailing floor (26 steps a day);
  - consistency;
  - the lock;
  - the payout rules.
- 20,000 paths over 180 days, at SR 0.5–3, under a normal and a t(3) law.
- **The policy family and the gate were frozen and hashed before any code ran.**
- Constant size was tested at 20 sizes, which makes the gate harder for the challengers.

**Result: no policy beats constant size in every cell.**

| Policy | Best cells won (of 12) | Where it helps |
|---|---|---|
| P1, cushion-proportional | 4 Flex / 6 Daily | Fat tails only |
| P2, consistency taper near target | 3 Flex / 0 Daily | Low SR, normal law only |
| P3, stage-aware | 1 Flex / 6 Daily | Fat tails; the gain is from sizing, not withdrawal |
| Cushion-preserving withdrawal alone | 0 | Never |

**Proposal:**
- One constant integer size per leg, the same in evaluation and funded stages.
- Greedy withdrawal: request the maximum eligible amount at the first eligible end of day.
- The size is chosen against stated P(breach) and P(no payout) limits, **not by expected cash alone**.
- A state-dependent policy returns only through a fresh candidate-blind pre-registration that wins every cell.
- **PRM qualification (after review):**
  - "No challenger won every cell" does not prove constant size optimal for an eventual candidate. The table shows conditional gains under fat tails.
  - Chip 3 allowed unlimited resets, so it cannot establish the optimum under finite purchase limits.
  - Its greedy-vs-lock-first withdrawal comparison is specific to its setup and does not select a withdrawal policy (§3.9).

**Side finding: expected cash alone points to reckless size.** The expected-cash-maximising constant size has P(breach) 0.96–1.00, because the model allows unlimited cheap resets and rebuys. That is outside D1's purchase limits and is **not a sizing result**. It is why R3 requires explicit limits.

**Limits:**
- Tradeify's help site returned 403 to the cloud container, so the rules were read through a mirror.
- The Daily loss limit and the Daily scaling ladder are assumptions.
- Days are i.i.d., so volatility clustering is untested.

### Chip 4 — the owned Select 100K against its alternatives (R5)

**Options compared**, on synthetic edges across the SR grid at 90 and 180 days, under a central and a conservative case (t(3), −0.5 SR, an extra round-trip cost):
- keep the owned evaluation (fee sunk);
- let it lapse and buy a new Select 25K, 50K or 100K (Flex or Daily);
- a small personal account (D2);
- no deployment.

**Findings:**
1. **Keep, and buy nothing, at every SR band while the owned account costs $0 in cash.** It beats every feasible alternative in expected cash at every tested SR and cannot lose cash. Keep vs lapse turns on upkeep (time on the weekly trade) against the chance a qualified native strategy arrives, not on SR.
2. **A new 100K is never the right purchase.** Wherever buying pays, a Select 50K beats the 25K and the 100K.
3. **Buying passes the conservative test only at true SR ≥ 2.5** (90 days) **or ≥ 2.0** (180 days, with R1's runway).
4. **A small personal account is never best while the owned evaluation is kept.** At E1's volatility it cannot meet D1's exhaustion tolerance.
5. **Null control:** at SR 0 every purchase and the personal account lose money. The owned account's small positive result at zero edge is cushion harvest, which D6's "never hosts an unqualified strategy" rule keeps off-limits.

**Break-even SR** (90 days / 180 days):

| Comparison | Central | Conservative |
|---|---|---|
| A purchase beats none | 1.0 / 1.0 | 2.5 / 2.0 |
| A purchase beats the personal account | 1.5 / 1.0 | 2.5 / 2.0 |
| The personal account beats none | 0.5 / 1.0 | 1.5 / 2.0 |
| A new 50K matches the owned account | ≈ 3 / ≈ 3 | > 3 / ≈ 3 |

**Scope (after review):** these break-evens come from one synthetic model (IID sessions, fixed volatility, no continuation value). They are guides, not universal validated-SR admission gates, and the Select 50K is not a universal winner. "Buy nothing now" stands as a practical recommendation without blocking later vehicle comparisons.

**Proposed for the 11-08 sitting:**
- Keep the owned evaluation, which never hosts an unqualified strategy.
- D-A: $0 recurring cash; any charge ends it.
- Review every eight weeks: keep only while a native, Tradeify-eligible candidate is in frozen validation or is named for freezing.
- Model no purchase until validated SR supports 2.5 (2.0 with R1), and then the Select 50K only. *(As drafted by chip 4. The PRM recommends adopting only "keep, buy nothing now"; see Scope above.)*

**Changes to existing rules (Joshua's call):** a revocable **standing GO for the weekly maintenance trade**, placed for him. Today each weekly trade needs his own GO.

**Limits:**
- i.i.d. sessions with a fixed volatility;
- no continuation value;
- this model is kinder to purchases than E1, so E1 would raise these thresholds, not lower them.

### Chip 5 — the smallest first release (R6)

**Joshua's input:** more than 15 attended hours a week, weekdays 09:30–16:45 ET, no evenings.

**Release 1:** one strategy, one account, one firm, attended. Every exposure window sits inside 09:30–16:00 ET, which leaves 45 minutes before Tradeify's 16:45 deadline.
- One leg removes the multi-leg runbook items: U-2, the D-N2 priority rank and the same-instrument rules.
- Attended operation removes the dependence on the D-N1 incident close (U-17).
- **Still needed:**
  - the three native canary items: compile/load/startup, restart protection, session-end cancel and flatten;
  - U-1, U-3, U-6, U-7, U-9–U-14 and U-16.

**The attention budget is a hard screen.** Operating time ≈ 5E + 3.75 hours a week, where E is exposure hours per weekday. So E ≤ (H − 3.75)/5:
- at 15 h a week, E ≤ 2.25 h a day;
- an all-day hold needs about 36 h a week.

**Expansions, each with one trigger and one evidence item:**

| Expansion | Trigger | Evidence |
|---|---|---|
| Second strategy | Improves joint losses or payout timing | A pre-registered joint simulation of the whole account policy |
| Unattended operation | Restart and recovery demonstrated | A release-1 recovery record: every restart, disconnect and incident reaches verified flat, or stays bounded by a broker-resident stop, without operator action, and pages the operator |
| Second firm | The first firm's limits cap growth | A cash-cadence record that names the blocking limit. The new firm also needs its own qualified strategy (same-bot bar) |
| Activity leg | The weekly trade can't be met more cheaply | A weekly-coverage record. It must be low-frequency (high-frequency bar) |

**Also proposed:** a second account at the same firm, admitted on the same cash-cadence record. Same-direction copying across one's own accounts is allowed.

**Limits:**
- The hour figures are estimates; replace them with timings from the 2026-10-26 canary.
- The 16:45 and 12:59 deadlines were verified first-party by the PRM on 2026-10-23.

### Chip 6 — qualify the complete policy (R4)

**The qualified object:**
- the components;
- the sizing policy (shared cap, scaling ladder, protection);
- the withdrawal and replacement policy;
- the account rules.

**Synthetic cases** (Select Flex 100K funded, 250 days, 20,000 paths, 5-minute steps):

| Case | Added component's SR | Δ E[cash] | Δ P(breach) | Δ P(no payout) | SR-2 hurdle | Marginal rule |
|---|---|---|---|---|---|---|
| (a-i) wins on the other component's losing days | 0.72 | +$3,255 | −0.27 | −0.10 | rejects (wrong) | admits (right) |
| (a-ii) fills the $200 winning days | 0.79 | +$2,684 | +0.35 | −0.40 | rejects (wrong) | admits (right) |
| (b) shares a 09:30 dip that recovers by the close | 2.51 | −$1,604 | +0.24 before first payout | +0.23 | admits (wrong) | rejects (right) |

**Daily evidence is not enough.**
- In (b), an end-of-day model gives Δ cash +$3,922 against the true −$1,604.
- A variant with identical daily statistics but the dip at 14:00 is genuinely positive.
- No daily statistic separates the two.

**Proposal:** no component has a standalone hurdle. A component enters only if, on paired simulations with and without it:
1. the lower confidence bound of Δ E[net cash] is above 0;
2. Δ P(no payout per cycle) is not significantly above 0;
3. the new policy passes complete-policy qualification.

Further:
- Δ P(breach) is reported, and binds through the owning gates' limits (R3).
- Intraday-checked floors need the components' **joint intraday** mark-to-market. Without it, use the comonotone bound (sum of each component's own low): a pass stands, a fail is not a pass.
- Horizon, valuation, confidence level and withdrawal policy are pre-registered. Each component tried counts toward K.

**Engine gap:** `core/mc/simulation.py::simulate_path` takes one `intraday_low` per day, which must be the low of the summed path. It has no payout or withdrawal model.

**PRM reconciliation with chip 3:**
- Chips 3 and 6 used different withdrawal rules (chip 6 kept a $1,500 cushion). No withdrawal policy is selected (§3.9). Any adopted use of R4 pre-registers one withdrawal policy and re-checks case (a-ii) under it.
- (a-ii) raises P(breach) by 0.35. That is acceptable only with R3's explicit breach limit, so R3 and R4 must be adopted together.
- (a-ii) wins only if a breached account is replaced. Under D1's current purchase limits the no-replacement valuation applies.

### Chip 7 — evidence matched to what each step risks (R7)

**Principle:** a requirement binds a step only if it protects something that step uses up (cash, attention, K, unexamined data, an account) or a claim that step makes.

| Step | Resolves | Needs | Does not need |
|---|---|---|---|
| 1. Zero-cost read | Whether a question deserves a costlier step | The pre-Q gate; K if it selects. On unexamined data: reservation, exposure entry, committed statistic, operator GO | On examined data: GO, Req 1–5, D1/D4/D6 |
| 2. Mechanism depth check | Whether a mechanism exists and how large it is | Req 1's before-data clauses; discriminator, statistic and K ≤ 3 committed before the read; Req 5 as the **pass line** | GO at $0 on examined data; Req 5 as a precondition; D1/D4/D6 |
| 3. Paid data | The right to test on new data | Req 1, 2, 4 and 5; campaign envelope with a GO under D1; an approved vendor | Canary, D4, D6, M1 |
| 4. Native canary | Whether the code matches the frozen spec (implementation only) | A frozen spec; synthetic or examined data only | Req 4, D4, D6, M1, firm permissions. **A pass is never economic evidence** |
| 5. Sim forward observation | Performance on unseen data; real-time behaviour | Canary pass; statistic, cost model, stop rules and **N set by Req 4 power**, frozen before the first session | D1, D6, M1, firm permissions |
| 6. Paid pilot | Real fills and costs at minimum size; operating load | D1 economic evidence; native correctness; permissions; separate GO; M1 and per-session GO for any live send | D4. Never on the owned evaluation |
| 7. Evaluation or funded deployment | Whether it earns at the venue's geometry | D4, D6, venue fit, lifecycle admission, Req 5 at the venue's costs, canary, permissions, M1, arming, per-session GO | Nothing removed |

**Changes:**
1. **Remove the operator GO** for a $0 pre-freeze probe that reads only examined data, has K ≤ 3, and is committed before the read. Keep the GO for any spend or any read of unexamined data.
2. **Requirement 5** is the pass line at a $0 depth check, not a precondition.
3. **Requirement 4 power** applies to forward observation offered as D4 evidence. With daily P&L at SR 1.5:
   - 40 sessions give power ≈ 0.09;
   - power 0.5 needs about 430 sessions;
   - at SR 2 it needs about 240.

   (PRM checked this arithmetic.)
4. **Economic evidence, D4, D6, M1 and firm permissions** are not prerequisites of a sim canary or sim forward observation.

**Wording:** an addendum to `docs/adr/2026-08-30-evaluation-order.md` (the "step-risk evidence ladder"), plus three matching edits:
- the candidate-contract probe clause;
- the Requirement 5 depth-check note;
- the forward-observation N rule.

**Open for Joshua:**
- S5 (an automated sandbox admit without a GO) and D1 (a GO for each paid pilot) both govern step 6.
- Does an evaluation bought only to pilot count as step 6 or step 7? It is treated as step 7 until he rules.

### 3.8 Related evidence: net cash generation vs account survival (desk memo, not a chip)

**Source:** a separate desk session's memo of the same day (private, `504c5f05…`).
- It asks whether accepting more funded-account failures raises net cash.
- It uses E1's stored 90-day results (synthetic, new Select 50K Flex, 20,000 paths per row), closed-form lifetime arithmetic and Tradeify's payout-policy page.
- It ran no new simulation, used no market data, and added nothing to K.

**Findings relevant to R1–R7** (corrected after review; see §3.9 for definitions):
1. **Zero edge, scoped.**
   - In the memo's closed-form model, expected lifetime withdrawals equal the starting cushion under any withdrawal policy. That model is IID, reflects at cushion K, runs to ruin, and has no caps.
   - That is a model result, not a general one. Negative net cash also needs the acquisition and replacement economics, which E1 supplies for a new purchase.
   - It is consistent with chip 4's small positive zero-edge result for the already-owned account. There the fee is sunk, so withdrawing the cushion is pure gain. That conditional funded-account result is not the full evaluation-to-payout lifecycle, and it is no case for trading without edge.
2. **At SR ≤ 1.5, separate negative from inadmissible.**
   - In E1 some policies there have **negative** expected cash (for example G SR 1, 3 MES: −$63).
   - Others have **positive expected cash but are inadmissible** under the elected X3 ≤ 10% (for example G SR 1, 4 MES: +$116 with X3 50%).
   - So "nothing qualifies" does not mean not trading has the highest expected cash there.
3. **Within 90 days, size raises expected cash, and X3 bars it.**
   - At SR 2 (law G), going from 3 to 4 MES (wait for lock) raises mean 90-day net cash from $206 to $481, and lowers P(N < 0) from 67% to 57%.
   - X3 rises from 9.1% to 36%. **X3 is E1's terminal event P(no active account at day 90 and N < 0), not a funded-breach rate.**
   - Under law K the gain nearly vanishes ($9 → $39).
4. **Withdrawal timing: no common winner yet.**
   - E1's "first eligibility" vs "wait for lock" comparison (new 50K, 90 days) and chip 3's "greedy" vs "lock-first, keep one drawdown" comparison (100K evaluation → funded, 90/180 days, unlimited resets) are **different policies, programs and comparators**.
   - In E1, waiting has the higher mean cash. First eligibility has more payouts, less severe loss, and a 3.5–9.4% class of paths paid and still cash-negative.
   - The memo's lifetime sensitivity (a $3,000 cushion ≈ 29× an early-request cushion at SR 2; Daily about 25–40% below Flex on 100K) is **model-conditional**. Its formulas compare remaining continuation value, not cash already withdrawn plus continuation from comparable starting states, and it has not been independently checked.
5. **Select Daily** suits frequent payouts: daily eligibility, no winning-day threshold, an enforced buffer. The Flex/Daily choice is permanent at activation. Its cost against Flex is unquantified beyond the model-conditional sensitivity above.
6. **Copying one strategy across accounts is leverage, not diversification.**
   - Accounts that move together bust together, so P(cash-positive quarter) does not improve.
   - *Chip 5's second-account option is therefore justified only by fees and cadence, not by risk. Real diversification needs distinct strategies.*
7. **What strategies to seek:**
   - net edge first;
   - under Flex, frequency counted in qualifying days ($200 on 100K, $150 on 50K), not winning trades;
   - profit spread across many days rather than a few large ones;
   - left tails decide survival.

**Proposed follow-up (not recommended yet): E1-P.**
- Rerun the accepted E1 harness with Select Daily, Flex with a fixed cushion, and one de-risking rule.
- Budget: ≤ 3 h build plus 1 h independent review, $0, K += 0.
- It becomes decision-relevant only when a candidate has edge evidence, because the first irreversible policy choice comes at activation after a pass.

### 3.9 Definitions and decision comparison (added after Codex review, 2026-10-24)

**Definitions:**
- **N_T:** bank-received net cash at horizon T, after all fees and costs.
- **X3:** E1's elected tolerance event: no active account at T **and** N_T < 0. It is neither P(N_T < 0) nor a funded-breach rate.
- **P(breach):** the probability an account hits its floor. It is not measured by X3 and has no adopted limit.
- **Continuation value:** future net payouts a surviving account can credibly produce. It is reported separately from cash received, never added to it, and depends on stated edge durability, discounting, future costs, payout caps and termination. A nominal balance is not wealth, and survival is not an objective in itself.

**Decision comparison: accepted E1 results only.** The program is a new Select 50K Flex; the horizon is 90 days, about one quarter; σ is $150 per MES; up to 4 purchases are allowed with replacement; seed B, 20,000 paths. Original labels are kept.

| Law, SR | MES, withdrawal | E[N] | P(N < 0) | P(no payout) | P(N ≤ −$300) | X3 | Requests / 90d |
|---|---|---|---|---|---|---|---|
| G, 2 | 3, wait (selected) | $206 | 67% | 67% | 47% | 9.1% | 0.59 |
| G, 2 | 3, first | $161 | 62% | 53% | 39% | 10.2% | 0.77 |
| G, 2 | 4, wait | $481 | 57% | 57% | 55% | 36% | 0.79 |
| G, 2 | 4, first | $422 | 55% | 48% | 47% | 36% | 0.89 |
| K, 2 | 3, wait | $9 | 82% | 82% | 36% | 3.1% | 0.31 |
| K, 2 | 4, wait | $39 | 78% | 78% | 67% | 22% | 0.36 |

**What it supports:**
- Higher expected cash comes with more finite downside and a higher X3.
- No row has a cash-loss probability below 50%.
- The ranking changes with the return law.
- **The current evidence does not select one cash-generation policy.** Account survival need not be the prize. The comparison that would decide is total net cash over explicit finite operating horizons, with any terminal continuation value shown separately.

## 4. What the seven results mean together

1. **The binding constraint is validation speed, not the rules removed.**
   - A purchase needs validated SR ≥ 2.0–2.5 (R5).
   - Forward evidence with adequate power takes about 240 sessions at SR 2 (R7).
   - D6 never hosts an unqualified strategy.

   **The fastest credible route is historical data that no one in the selection chain has examined**, not forward time. Research should prefer candidates for which such data exists.
2. **Attention narrows the search (R6).** At about 15 attended hours a week, a candidate's exposure must fit about 2.25 hours a day inside 09:30–16:00 ET. The overnight territory waits until unattended operation is earned.
3. **Expected cash alone is not a decision rule.**
   - Chip 3's expected-cash-maximising size breaches with probability 0.96–1.00, under unlimited resets.
   - In E1, higher expected cash comes with a higher X3 and more finite downside (§3.9).
   - R1's null control, R3's limits and R4's no-payout term each guard against that.
4. **The open question is the operating horizon, not survival.**
   - Continuation counts only through future net cash.
   - Comparing total net cash over explicit finite horizons, with continuation reported separately, is what would choose between withdrawal policies and between Flex and Daily.
   - A ruling that continuation matters does not settle either choice by itself.
   - R1's runway-plus-cadence structure supplies one such horizon.
5. **The standard is not lowered.** Every removal is paired with a replacement that is at least as strict on the risk it protected (§2).

## 5. Follow-ups if adopted

| Item | Owner |
|---|---|
| ADR 2026-07-16 and strategy_harvest Requirement 5 amendment; `register_search._require_cost_law` | R2 |
| Evaluation-order ADR addendum and the three matching edits | R7 |
| D1 wording: split horizon, constant size, breach and no-payout limits (withdrawal rule after the continuation-value ruling) | R1, R3 |
| Qualification-screen wording: marginal-contribution test | R4 |
| `core/mc` engine: summed-path intraday low, plus a payout and withdrawal model | R4 |
| P-E1H: extend E1 to runway plus two quarters, with the null control (needs approval) | R1 |
| Pre-register one withdrawal policy after the continuation-value ruling; re-check chip 6 case (a-ii) under it | R3/R4 |
| E1-P (Daily, fixed-cushion Flex, one de-risk rule), only once a candidate has edge evidence | §3.8 |
| Replace chip 5's hour estimates with canary timings | R6 |

## 6. Decisions requested from Joshua

1. Adopt R1–R7, in whole or in part.
2. The quarterly no-payout limit p_Q (R1).
3. A P(breach) limit for sizing (R3). D1's 10% tolerance covers budget exhaustion, not account breach.
4. A standing, revocable weekly-trade GO for the owned evaluation, and an 8-week review (R5, at the 11-08 sitting).
5. Which of S5 and D1 governs paid pilots, and whether a pilot-only evaluation is step 6 or step 7 (R7).
6. The explicit finite operating horizon(s) for comparing total net cash. Any terminal continuation value is reported separately, with stated edge durability, discounting and costs (§3.9). This frames, but does not by itself decide, the withdrawal rule and the Flex/Daily choice.
