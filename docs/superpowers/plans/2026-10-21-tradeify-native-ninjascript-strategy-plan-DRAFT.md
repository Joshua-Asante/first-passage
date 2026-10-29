# Tradeify-only native NinjaScript strategy: plan (DRAFT)

**Status:** DRAFT, 2026-10-21. Proposes a sequence; grants nothing. Every phase marked **GO** needs its own operator ruling. Under the [11-08 decision rules](2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-13--track-b-suspended-11-08-decision-rules-draft), only branch (b), [#807](https://github.com/Joshua-Asante/first-passage/pull/807) stage 1, is in scope before the sitting.
**Question:** can a strategy dedicated to Tradeify, with all logic native to NinjaTrader 8, reach a first Select Flex payout of ≥ $1,000 net at acceptable fee cost?
**Decision it changes:** whether Tradeify gets a native lane at the 11-08 sitting (branch (b) and onward), or parks under branch (d).
**Inputs:** [Q-PATH-TO-PAYOUT-1](../../notes/research/2026-10-21-q-path-to-payout-1-memo.md) (geometry, sizing, §5 verification); [compliant automation routes](../../notes/2026-10-13-tradeify-compliant-automation-routes.md) (route 1); #807 (native runtime proposal).

## 1. Constraints (verified 2026-10-21 unless noted)

| Constraint | Consequence for the strategy | Source |
|---|---|---|
| All strategy logic, calculations and signals native to NinjaTrader; no external engine, bridge or API | Self-contained NinjaScript strategy. Python is for offline research only | [route record](../../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#addendum-2026-10-12-later--tradeify-support-strategy-logic-must-be-native-for-evaluation-accounts) |
| Same bot at another firm is prohibited; the agreement permits personal accounts | The candidate must not be any firm's strategy elsewhere. Personal-lane use is a **recorded conflict**: FTA §6.6 permits personal accounts, but support's 2026-10-08 reply says "used only within Tradeify" | Q-PATH §5; [follow-up §2](../../notes/2026-10-21-tradeify-native-followup-questions-DRAFT.md#2-topics-not-in-the-message-and-where-each-goes); [10-10 replies](../../notes/2026-10-10-tradeify-exclusive-use-replies.md#3-answers-r1-paraphrased-per-point) |
| Sole ownership of "the bot or strategy", provable on request; Tradeify may require a live video of enabling it; no HFT | Private code. Whether a private, AI-assisted implementation of a published rule satisfies sole ownership is **OPEN** (follow-up Q1). Login never via VPN/VPS; after a normal login a VPS may be used "at your own risk" ([FAQ](https://help.tradeify.co/en/articles/12268494-common-faqs), 2026-10-20). The first release is attended locally | Q-PATH §5; [10-10 replies](../../notes/2026-10-10-tradeify-exclusive-use-replies.md) |
| NinjaTrader via Tradovate only, under Tradeify's company license | Needs an account bought with Tradovate as broker. Native automated strategies are a documented NinjaTrader capability. Whether this entitlement restricts a feature the strategy needs is a P1 technical check, not a support question unless a concrete gap remains | Q-PATH §5; [NinjaTrader automated trading](https://ninjatrader.com/support/helpGuides/nt8/automated_trading.htm) |
| Book lineage has no evidence case for the Tradeify eval | Excludes the declared book, its T00 rungs, FLOOR-HALF and R1 | [10-19 addendum](2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-19--no-book-lineage-configuration-has-an-evidence-case-for-the-tradeify-evaluation) |
| ORB MNQ v7 solo is the four-firm §4 candidate | Excluded unless Joshua reassigns it (decision D2) | [#864](https://github.com/Joshua-Asante/first-passage/pull/864) |
| Select 50K eval: $3K target, $2K EOD trailing drawdown enforced intraday, no lock, 40% consistency, 3-day minimum, 4 minis / 40 micros | Size and cap per §3 | `core/firm_rules.py` `Tradeify_Select_50K`; Q-PATH §5 |
| Flat by 16:45 ET; ≥ 1 trade per week per account; no hedging across own accounts; funded payouts need > 50% of trades and profit from holds > 10 s | Hard-coded session flatten, a weekly-activity guard and a minimum hold | Q-PATH §5 |
| Public repo | NinjaScript source of the strategy is an executable strategy port. Keep it private, like the Pine and ports | AGENTS.md §Public-clone posture |

## 2. Prerequisites, by what they gate

**For bounded offline research and prototyping (P1–P4):** only the existing internal approvals. That means the 11-08 ruling granting branch (b) for P1, and the phase GOs below. Tradeify's answers are not a prerequisite for this work.

**For enabling a strategy on an evaluation account (P6):**
1. **A written Tradeify answer on ownership and exclusivity** for the chosen candidate: a private, AI-assisted implementation of a published rule. This is the [follow-up draft](../../notes/2026-10-21-tradeify-native-followup-questions-DRAFT.md), unsent, which needs D2 to name the rule.
2. **Data rights** through the existing licensing thread: the legal distributor and subscriber agreement from Tradeify/Tradovate, then the open classification via CME ticket #04738415.
3. **The P1 entitlement check** of the features the strategy uses. Support is asked only about a concrete gap.

**Deferred until planned:** unattended or remote operation; concurrent personal-account use; cross-firm use; scaling across accounts (design question, P7). The follow-up draft's §2 says when each is raised.

## 3. Strategy design targets

These come from the Q-PATH model (i.i.d. Gaussian; an upper bound on what a fat-tailed strategy gets).

| Target | Value (Select 50K) | Why |
|---|---|---|
| Live Sharpe after costs ($0.91/side micros) | ≥ 1.5 to proceed; ≥ 2 planning case | At Sharpe 2: P(first payout ≤ 120d) ≈ 0.88, about $535 per payout. At Sharpe 1: about $980 |
| Daily P&L σ, eval | $400–600 (up to $800 if speed matters more than fees) | Cheapest $/payout around 0.2–0.3 × drawdown |
| Daily profit cap | $750–1,050, then flat for the day | Keeps the 40% consistency rule satisfied by construction |
| Catastrophe stop | ≥ $1,000/day | Gap and tail guard only; it does not raise pass odds |
| Instruments | Micros (MNQ/MES/MYM/MGC) for sizing granularity | 40-micro eval cap; funded starts at 2 minis (20 micros) |
| Session | RTH intraday, flat by 16:45 ET | Venue force-flat |
| Activity | ≥ 1 trade per week by construction | Inactivity rule, per account |

## 4. Phases

| Phase | Work | Exit gate | Owner / authority |
|---|---|---|---|
| P0 | 11-08 ruling (branch (b)); send the follow-up once D2 names a candidate | Ruling; follow-up sent | Joshua |
| P1 | #807 stage 1, repurposed: it was scoped as an Aegis dependency/toolchain assessment. Here it means a read-only NinjaTrader toolchain assessment for this candidate, plus a check that the installed Tradeify entitlement supports the features this strategy needs. Feature list comes from the candidate; a menu being present is not evidence of trading permission or correct execution | Assessment report naming any concrete entitlement gap; no strategy code | Branch (b) GO, which must state this repurposed scope explicitly |
| P2 | Candidate sourcing under the [evaluation order](../../adr/2026-08-30-evaluation-order.md), steps 1–6: structural screen; Confirm reservation; contract freeze with Tradeify Select 50K as the role; TRADEABLE-REACHABLE; bind K; Explore; selection freeze. Check the [rejected register](../../rejected_candidates.md) first | Frozen candidate contract and selection freeze | **GO** (campaign envelope) |
| P3 | Confirm/holdout per the evaluation order, steps 7–10, on the Python reference. Intraday-honest scoring against `Tradeify_Select_50K` (EOD-clock results are lower bounds) | Confirm verdict; first-payout model rerun with the measured return distribution in place of Gaussian | Campaign owner |
| P4 | Native port: a private NinjaScript implementation with fixed parameters; frozen identical-input parity (decisions and sizing) against the Python reference (#807 §2.6, §6) | Parity pass; no external calls in the binary | **GO** (implementation) |
| P5 | Forward test on NinjaTrader sim with Tradeify-equivalent rules: at least 40 sessions or a pre-registered N, attended start | Live Sharpe after costs ≥ 1.5 at a pre-registered confidence; no rule breach | **GO** |
| P6 | First evaluation: Select 50K ($165, reset $109), Tradovate broker. Requires §2's evaluation-account prerequisites. Monitoring acceptance for the new instance (AGENTS.md: a new instance needs its own M1) | Pass or bust record; fee budget 4 attempts (about $490) before review | **GO** + spend ruling |
| P7 | Funded: request at the first eligible cycle with ≥ $2,222 profit (≥ $1,000 net). Scale only by adding 50K accounts that copy the same strategy (≤ 5 funded per household) | First payout | **GO** per account |

**Stop rules:**
- Tradeify answers that the candidate does not satisfy ownership/exclusivity: do not enable it on Tradeify. That rules out this deployment route for that candidate. It does not void the research or implementation done, which internal approvals still govern. Choose another candidate (D2) or park (branch (d)).
- P3 Confirm fails: record in the rejected register; next candidate only through a new contract.
- P5 live Sharpe after costs is inconsistent with ≥ 1: stop before P6.
- P6: judge the edge on trade-level statistics, not pass/fail. Zero edge passes about 22% of attempts, Sharpe 2 about 40%.

## 5. Budget (Rule 2)

| Phase | Agent effort (estimate) | Spend |
|---|---|---|
| P1 | 1–2 sessions | $0 |
| P2–P3 | 3–6 sessions per candidate; K and data per contract | $0 (existing TV CME exports) |
| P4 | 1–3 weeks of sessions, by #807 §7's weeks-to-months range for the full book; one strategy is smaller | $0 |
| P5 | Operator-attended sessions, ≥ 8 weeks | $0 platform; CME per P0 item 2 |
| P6–P7 | Per account | $165 per eval, $109 per reset; Tradeify charges no activation fee |

Reaching any phase's bound triggers reassessment, not expansion.

## 6. Decisions for Joshua

- **D1.** Pursue a Tradeify native lane at all (11-08 branch (b)), or park (branch (d)).
- **D2. Candidate source:**
  - (a) a new candidate through P2;
  - (b) reassign ORB MNQ v7 from the four-firm §4 slot to Tradeify-only;
  - (c) another non-lineage strategy you name.

  Recommendation: (a), unless the §4 run on ORB v7 is dropped. (b) trades the four-firm falsifier's candidate for a faster Tradeify route.
- **D3. First account:** the incumbent Select 100K eval (no new fee, but 2.0 geometry and a used state) or a new Select 50K (1.5 geometry, $165).

  Recommendation: decide after P5, using the measured distribution in the payout model.
- **D4. Personal lane reuse:** whether to also run the strategy on the personal Tradovate account. Tradeify's terms are in recorded conflict (§1), so this needs Tradeify's written clarification before any concurrent use. Live capital there stays under that lane's own clearance standard ([ADR](../../adr/2026-10-09-self-funded-tradovate-lane-reopen.md)).
