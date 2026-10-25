# Assumption challenge: simplify by subtraction (2026-10-24)

**Status:** §2.1 ENDORSED by Joshua on 2026-10-24 (ruling recorded below). The rest of the report is the proposal and the study findings as written, and is not itself a ruling.
**Owner:** Portfolio Research Manager (PRM). **Rulings owner:** Joshua.
**How to read it:** the operator ruling below is what binds. §2 is the recommendation it answered. §3 is the historical study evidence.

## Operator ruling (Joshua, 2026-10-24)

Recorded separately from the study findings, in Joshua's words:

> "I endorse §2.1's deletions and authorize their implementation in the owner documents, enforcement code and duplicate references. Preserve the four boundaries in §2.2. Remove only the targeted restrictions, not adjacent cost accounting, evidence records or trading protections. Use focused checks to verify the deletions work; don't create replacement machinery or another review programme.
>
> Keep the current D1 horizon, cash and time limits unchanged. Use D1 as the single authority for paid-pilot approval. No standing maintenance-trade authorization is granted here, and the owned-account decision remains at November 8. No sizing, withdrawal or Flex/Daily policy is selected."

**The §2.3 items as ruled:**
1. The D1 window is **unchanged**.
2. **No** standing weekly-trade GO is granted. *(Superseded 2026-10-25: Joshua granted a standing, revocable GO for the weekly account-preservation trade; see [STATE](../../STATE.md#scheduled-forward-triggers) and [ADR Addendum 2026-09-30b](../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-30b).)*
3. **D1** is the single authority for paid-pilot approval.
4. The owned Select 100K decision stays at the **11-08 sitting**.

**Implementation:** a separate PR, with deletions only.
**Public-clone posture:** this report contains no account identifiers, account balances, budget amounts or backtest P&L. Dollar figures are published firm rules or synthetic-model outputs. The private returns are cited by content hash.

## 1. Direction

Joshua, 2026-10-24: "Simplify by subtraction. Remove redundant gates and their supporting machinery. Do not automatically replace them with another test, reviewer or approval. Bring me only deletions that change my financial exposure, account permissions or the evidence claimed."

**The keep test for any requirement:** what specific, material failure would become possible if it were deleted, and is that failure already covered elsewhere? If there is no concrete answer, delete it. Don't soften it.

**Where this came from:** seven bounded, candidate-blind chips ($0, no strategy results read, gates fixed in advance) and a related desk memo. All passed their gates.

| Chip | Constraint questioned | Return (private) |
|---|---|---|
| 1 | Cash within 90 days | `68b3d784…` |
| 2 | Gross edge ≥ 4× costs | `bcd77e96…` |
| 3 | Constant size and withdrawal | `fa95fc84…` |
| 4 | The owned Select 100K as destination | `c7563fe9…` |
| 5 | Diversified, multi-firm or unattended release 1 | `60f2bb5f…` |
| 6 | A standalone hurdle for each component | `7072ddfb…` |
| 7 | The same evidence for every step | `2f20cd2e…` |
| Memo | Net cash vs account survival | `504c5f05…` |

## 2. Current recommendation

### 2.1 Delete outright, with no replacement test, reviewer or approval

| Delete | Failure it guarded against | Already covered by |
|---|---|---|
| **The universal 4× cost gate** (strategy_harvest Requirement 5 and its sourcing-time copy) | An edge eaten by costs | Evaluating each candidate's estimated net return, execution uncertainty and cost sensitivity, plus D4's validated net performance before deployment |
| **Standalone Sharpe hurdles for components** | A weak component diluting the account | Evaluating what the actual combination delivers |
| **"Adaptive sizing must beat constant sizing in every scenario"** | Overfitted sizing rules | A fair comparison of the relevant alternatives, with the alternatives tried counted honestly |
| **Mandatory diversification, multiple firms or unattended operation for release 1**, and the expansion-trigger table | Concentration; operator overload | Cash and time limits, and attended operation. Build only what the first viable strategy needs |
| **Profitability sample-size requirements for implementation diagnostics** | None (a diagnostic makes no profitability claim) | — Test the behaviour to verify, then stop |
| **Routine permission requests for research steps inside an explicitly approved scope** | Unapproved spend or data use | The approved scope's own limits. Escalate only when the scope materially changes |
| **Proposed new machinery from the chips:** the replacement net-edge formula and its calibration project, the marginal-contribution admission gate, the evidence-ladder ADR addendum, and the E1 extensions P-E1H and E1-P | Nothing yet built | Not needed before finding one worthwhile strategy |

**Owner documents edited only to delete,** after Joshua endorses:
- `docs/methodology/strategy_harvest.md`: Requirement 5, §2.2;
- the candidate-contract probe clause;
- the D1 sizing-rule wording.

No new text replaces them beyond a dated "deleted, see this report" line.

**Make each deletion real:** remove its enforcement and duplicate references in the same change. For the 4× gate, that means:
- `register_search._require_cost_law`;
- the discovery-campaign template row;
- the strategy-validation cross-reference;
- any sourcing script that rejects below 4×.

No replacement formula, calibration project or review step.

### 2.2 Keep: boundaries that protect something real, each with one home

| Boundary | Protects | One home |
|---|---|---|
| Cash and time limits | Joshua's money and attention | D1 limits ruling (private relay record). Not restated in other documents |
| The chosen firm's actual rules | The account | `core/firm_rules.py` and the venue edition, checked against the firm's published pages |
| Honest treatment of evidence | Deployment claims | D4 (untouched validation for any deployment claim), with K and exposure records. Evidence reported from a common start date for every attempt, never only from accounts that reached a payout |
| Controls against unintended trading | Accounts and capital | `AGENTS.md` §Live-execution posture: M1, the arming interlock, per-session GO, and D6 (the owned evaluation never hosts an unqualified strategy) |

### 2.3 Bring to Joshua: only deletions that change exposure, permissions or claimed evidence

1. **Financial exposure: D1's 90-day window.**
   - D1 counts from the first paid attempt, so build time is already excluded.
   - Lengthening the paid-attempt window to up to six months (chip 1) lengthens how long money is at risk before cash must arrive.
   - **Keep 90 days, or set a longer window?**
2. **Account permissions: a standing, revocable GO for the owned evaluation's weekly maintenance trade** (chip 4), replacing a GO each week.
3. **Account permissions: one home for paid-pilot approval.** S5 (an automated sandbox admit without a GO) and D1 (a GO for each paid pilot) both claim this step. **Recommend D1 as the single home.**
4. **Financial exposure: the owned Select 100K.** Keep it while it costs $0 in cash, and buy nothing now (chip 4). Decide at the 11-08 sitting.

**Sizing method, withdrawal timing and Flex vs Daily:** deferred until a viable strategy exists. This report selects none of these policies. Routine choices within an approved operating scope stay with the owner. Material changes to financial exposure or account permissions come to Joshua. Flex vs Daily is a permanent account choice.

## 3. Evidence behind the recommendation

**Chip 2 (4× costs).**
- 4× is a convention (`MIN_RMULT = 4.0` → the cost-geometry pre-gate → ADR 2026-07-16 → Requirement 5). It has no term for sample size, volatility or selection.
- On synthetic cases it dropped a robust strategy at 3.3× and admitted two weak ones at 4.7–5×.
- A per-candidate net-return and cost-sensitivity estimate sees what the ratio misses.

**Chip 6 (component hurdles).** On synthetic Select Flex 100K funded paths, an SR-2 hurdle per component got all three cases wrong:
- it rejected two low-SR components that improved the account: one hedges losing days, and one fills the $200 winning days. The second helped only when a failed account could be replaced, which current purchase limits do not permit;
- it admitted a high-SR component whose shared 09:30 dip breached the floor.

What the combination delivers is what matters. **Daily data cannot show it when the floor is checked intraday:** an end-of-day model called the harmful pair +$3,922 when the true figure was −$1,604.

**Chip 3 (adaptive vs constant sizing).**
- No tested adaptive policy won every cell. Several won conditionally (under fat tails, or at low SR), so "must win everywhere" was the wrong bar.
- Its expected-cash-maximising size breached almost surely under unlimited resets. Expected cash alone is not a sizing rule.

**Chip 5 (release 1).** One strategy, one account, attended, inside 09:30–16:00 ET. Joshua has more than 15 attended hours a week. Operating time ≈ 5E + 3.75 h a week, so at 15 h a strategy can be exposed for about 2.25 h a day. The hour figures are estimates, to be replaced with canary timings.

**Chip 7 (evidence per step).**
- A native canary resolves implementation questions only. A pass is not economic evidence, and it needs no profitability sample.
- Forward observation offered as **proof of profitability** does need adequate power. With daily P&L at SR 2, about 240 sessions give 50% power, under those assumptions.

**Chip 1 (horizon).**
- In E1's synthetic model, 74–98% of paths are still active at day 90, so the window closes before most first payouts.
- A plain longer window also gains about as much pass probability at zero edge as at SR 2, which is why any longer window keeps the common-start cohort view (§2.2).

**Chip 4 and the memo (destination and cash).**
- Keeping the owned account at $0 cash beat every feasible alternative in expected cash at every tested SR. The break-even SRs for buying are model-conditional guides, not gates.
- E1's synthetic results (new 50K Flex, 90 days, law G, SR 2) show real tradeoffs, but no dependable quarterly income:

| Policy | E[N] | P(N < 0) | P(N ≤ −$300) | X3 |
|---|---|---|---|---|
| 3 MES, wait for lock | $206 | 67% | 47% | 9.1% |
| 3 MES, first eligibility | $161 | 62% | 39% | 10.2% |
| 4 MES, wait for lock | $481 | 57% | 55% | 36% |

- X3 is E1's event "no active account **and** N < 0". It is not a breach rate.
- More size means losing less often but more severely. Earlier payouts cost some expected cash in return for smaller losses.
- Copying one strategy across accounts is leverage, not diversification.

## 4. Outcome

**Fewer things to operate:**
- one admission gate, the component hurdles and two universal sizing and evidence rules are deleted;
- six proposed pieces of new machinery are never built;
- routine permission asks inside an approved scope stop.

**What remains:** four boundaries, each with one home, and four decisions for Joshua. The next substantial effort goes to finding one worthwhile strategy.
