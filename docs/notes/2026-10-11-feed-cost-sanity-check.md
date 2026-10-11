# Live-data cost vs what the two lanes can plausibly earn (sanity check, 2026-10-11)

**Status:** analysis note for the Deployment Coordinator; a recommendation for Joshua, not a ruling. It selects, funds and signs nothing.
**Serves (Rule 7):** the feed funding decision at CP-7 ([checklist §4](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#4-operator-checkpoints--where-approval-is-taken)) and [ADR 2026-10-09](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) owed items 3–4. Cost inputs come from the CME licensing note ([PR #770](https://github.com/Joshua-Asante/first-passage/pull/770)) and the vendor answer table §4.1 ([PR #768](https://github.com/Joshua-Asante/first-passage/pull/768)); this note edits neither.
**Evidence limit.** No MC, replay or screen was run (checklist 7.6.1). Earnings come from existing private model output: the eval → funded → payout desk model of 2026-10-08 and the [size-feasibility](../../lab/analysis/c1/size_feasibility_2026-10/RESULTS.md) run. Both are **model output under stated assumptions, not evidence**. Private working: `t00-step3-console/feed-cost-check-20261010T230316Z/`, `SHA256SUMS` sha256 `22a26ec13289b923bc11c90e303a11f9bf5454c5ee9e56f41dbcab38e53f865d`. Dollar figures here are public prices only.

Labels: **DOCUMENTED** (a published price or term, per the cited note), **ESTIMATE** (arithmetic on documented or model figures), **ASSUMPTION** (an input chosen here).

## 1. Monthly cost bands per licence path

Every row adds Tradovate's $25/month API add-on (DOCUMENTED) and $12/month non-pro Level 1 (DOCUMENTED price; whether API use needs it: not stated). CME fees are per exchange (DCM) per month, not pro-rated; three DCMs (CME, CBOT, COMEX) unless stated.

| Path | CME fee | Monthly total | Licensing status | Label |
|---|---|---|---|---|
| A9 Managed User | $624 ($645 from Jan 2027) | **$661** ($682) | Only if CME confirms Tradovate's flow qualifies and internal bars fall outside §11.3 | DOCUMENTED price / OPEN eligibility |
| **A8 User Non-Display** | $1,371 ($1,416) | **$1,408** ($1,453) | Safe reading on the Tradovate route | DOCUMENTED |
| A1 Basic | $1,827 | **$1,864** | If CME requires it | DOCUMENTED |
| Wrong A3 reading | $5,460 | $5,497 | Tail risk only | DOCUMENTED price |
| A8 / A9 on two DCMs | $914 / $416 | $951 / $453 | Only if the traded book needs two exchanges | ESTIMATE |
| Rithmic direct (P5d), no CME fee | none | ~$134 ($99.99 software + $8.65 top of book + Tradovate API) | Needs the §3.3 carve-out (no own licence for a non-pro on distributor data); FAQ Q10 and, reportedly, Addendum §4.2 contradict it. If CME's fee is owed too, add an A-category row above | DOCUMENTED price per reply / OPEN legitimacy |
| Massive (P1), no CME fee | none | ~$224 ($199 + Tradovate API) | Same Q1 ambiguity; "personal, non-commercial" plan | DOCUMENTED price per reply / OPEN legitimacy |

One-off and capital items: the $1,000 API-key balance is capital, not cost (DOCUMENTED; continued holding not stated). The $35 inactivity fee applies per 30 days without a live trade on the free plan (DOCUMENTED); a trading personal lane avoids it.

**Shared across lanes.** One feed drives both destinations (ADR 2026-10-09 Decision 3, item 4). The fee is per DCM whose data is used, not per destination (CM1 Q14), so the evaluation destination plausibly adds no category or fee (INFERENCE, CME to confirm). The same holds for every extra Tradeify account on the same feed. Cost is therefore a fixed monthly block that both lanes, and every account in them, share.

## 2. Break-even per lane

### 2.1 Tradeify lane at FLOOR-HALF

FLOOR-HALF sits at or below k = 0.5 on every leg (ORB off), so the desk model's k = 0.5 rows bound its economics from above (ESTIMATE). The model excludes data, platform and rail costs, and its normal tail is thinner than observed, so it is optimistic (DOCUMENTED in the model).

**Required payout (ASSUMPTION: one chain = the evaluation plus 12 funded months, feed paid throughout, 21 sessions a month).** Required net payout per funded month, as a ratio of the venue's $3,000 drawdown rope:

| Path | Eval lasts 3 months | 6 months | 12 months | Label |
|---|---|---|---|---|
| A9 | 0.28 rope | 0.34 rope | 0.45 rope | ESTIMATE |
| A8 | 0.59 rope | 0.71 rope | 0.95 rope | ESTIMATE |

Under the venue's 5-winning-day cycle and per-request cap, A8 needs most of a rope paid out every funded month, every month.

**Coverage by the model (one account, ESTIMATE):**

| Anchor | Share of A9 covered | Share of A8 covered | Accounts on one feed to break even at A8 (venue cap 5) |
|---|---|---|---|
| Favourable (optimistic H2) | about 1/4 to 1/2 | about 1/8 to 1/4 | about 4 to 9 |
| Governing (pessimistic H2; R1/R2 held, so the successor is judged here) | about 1/20 to 1/7 | under 1/14 | over 14 |

Only the favourable anchor, at its upper end, with four or five funded accounts on one feed, reaches A8 break-even. The governing anchor reaches it at no feasible account count.

### 2.2 Personal Tradovate lane

Q-SFGROWTH-1 has a frozen prereg but no run, so there is no growth forecast. Break-even is the annual growth g\* that pays the feed: **g\* = 12 × monthly cost / E_0** (ESTIMATE; `E_0` stays private). Equivalently, the capital at which a given growth rate pays the feed:

| Path | Capital needed at 15%/yr | at 30%/yr | at 50%/yr | Label |
|---|---|---|---|---|
| A9 | ~$53k | ~$26k | ~$16k | ESTIMATE |
| A8 | ~$113k | ~$56k | ~$34k | ESTIMATE |
| A8 on two DCMs | ~$76k | ~$38k | ~$23k | ESTIMATE |
| Rithmic direct, no CME fee | ~$11k | ~$5k | ~$3k | ESTIMATE |

**ASSUMPTION:** 15–50%/yr is the plausible median growth band under the ADR's p99 15% peak-to-trough limit; nothing on disk measures it. The private working compares `E_0` with these rows. Joshua can read the row for his own `E_0`.

### 2.3 Both lanes on one feed

Combining the personal lane at 30%/yr with one Tradeify account at either anchor covers A8 at well under half, and A9 at about two-fifths to nine-tenths (ESTIMATE, private working). Only a path with no CME fee is covered with margin.

## 3. Assumptions that dominate (largest first)

1. **Whether an own CME licence is owed at all** (FAQ Q10 / Addendum §4.2 vs Schedule 5 §3.3). It moves monthly cost by about 5–10×, from ~$134–224 to $661–1,864 (DOCUMENTED range, OPEN fact).
2. **The intrabar anchor (R1/R2).** It moves the Tradeify lane's modelled earnings by about 3–6×, more than any licence choice. R1/R2 is held, so the governing anchor applies (DOCUMENTED ruling, T00 card §8).
3. **A8 vs A9:** 2.1× on cost (DOCUMENTED).
4. **Tradeify accounts on one feed:** linear in earnings, cost fixed; venue cap 5 (DOCUMENTED cap; the program's scope today is one account).
5. **Personal growth rate and capital** (ASSUMPTION; Q-SFGROWTH-1 unrun).
6. **DCM count:** each dropped exchange cuts the CME fee by a third. FLOOR-HALF keeps all three DCMs while Vanguard trades (ESTIMATE); the personal portfolio is unselected, so this is a live lever for Q-SFGROWTH-1, not a reason to re-optimize a locked or ruled book.

## 4. Sensitivity: A9 vs A8

A9 saves $747 a month ($771 from Jan 2027), halving every break-even above: required Tradeify payout drops from about 0.6–0.95 rope to about 0.3–0.45 rope per funded month, accounts needed from about 4–9 to about 2–4 at the favourable anchor, and personal capital needed by 53%. It does **not** change the verdict at the governing anchor (still over 6 accounts). A9 also carries a design risk: §11.3 bars derivative works, which may forbid the internally built 15-minute bars unless CME rules otherwise (#770 §4).

## 5. Cheapest legitimate path

- **Confirmed legitimate today: none.** Every route's Q1 is ambiguous and hinges on CME's written reply (#768 §4.1 screen: no variant passes).
- **Cheapest on Tradovate that CME's documents support:** A8 at $1,408/month (DOCUMENTED reading, INFERENCE that CME agrees).
- **Cheaper if CME says so in writing:** A9 at $661, or, if no own licence is owed for a non-pro on distributor data, Rithmic direct at about $134 or Massive at about $224, each pending its own Q1 answer.
- Fees are not pro-rated, so any licence should start at the start of a month in which a lane is ready to trade (DOCUMENTED basis).

## 6. Recommendation for Joshua

**Defer the feed until a lane clears; do not sign A8 on current economics.** At the governing anchor the Tradeify lane covers a small fraction of A8 at any feasible account count, and A9 does not change that. The personal lane breaks even only at the capital shown in §2.2. Meanwhile:
1. **Push CME in writing** on the two questions that move cost most: whether a non-pro on a distributor's data needs an own licence (dominant assumption 1), and whether Tradovate's flow is A9 with internal bars allowed under §11.3.
2. **Re-open the funding decision at CP-7 when either** the Tradeify successor screen returns GO (then price the account count needed, §2.1), **or** Q-SFGROWTH-1 returns RESOLVED with median growth at or above g\* for the cheapest confirmed path.
3. **Proceed at A8 only if** a lane clears **and** the plan carries enough funded Tradeify accounts or personal capital to meet §2's break-even, or Joshua accepts the shortfall as a cost of learning.

Deferring costs no timing on the evidence path: the successor screen and Q-SFGROWTH-1 run offline on recorded data and need no live feed (INFERENCE). It does mean no live strategy-signal evaluation before a lane clears.

## 7. Verification

- Inputs read: #770's note at its branch head; the #583 note §4.1 at #768's branch head; size-feasibility RESULTS and private `verdict.json` and k = 0.5 reports in place; the private desk model (sha256 `86c03617…`) and Q1 options sheet in place; [load-bearing numbers](../load_bearing_numbers.md); the T00 card §8; the Q-SFGROWTH-1 prereg (no RESULTS on disk).
- Arithmetic: the private `calc.py`; its output is pinned in the private `SHA256SUMS`. No MC, replay, screen or GLM.
- Gates: `python -I scripts/fp.py check`; record cited in the PR body.
