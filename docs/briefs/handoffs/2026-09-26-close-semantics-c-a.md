# Close semantics for C-a (whole-leg broker liquidation) — bounded handoff

**Status:** DISPATCHED 2026-09-26 by the coordinating session (Claude Code, Opus 5.5) on the operator's instruction "start the close semantics, S5 measurement and ORB trace handoffs". **Dispatch revision:** the commit that adds this card; the executor verifies its `HEAD` descends from it. **Executor:** one assessor subagent in its own worktree. **Coordinator** accepts or corrects the return. Combined acceptance stays with the coordinator.

**Authority (operator ruling 2026-09-26, §2):** pursue C-a as the first candidate **to investigate**. The ruling approves investigation only; neither the close-contract amendment nor an unspecified residual risk is accepted. It asks for authoritative semantics for:
- protection during liquidation;
- partial or rejected outcomes;
- protective-fill races;
- reversal prevention;
- completion evidence.

Unresolved risks are returned precisely. A contradicting trace stops C-a. C-b needs its own operator expression decision and qualification, and is never automatic.

Sources: [incident ADR §A11.1](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md); the [B–D packet](../../notes/2026-09-26-tradeify-bd-decision-packet.md) §1.1 and §1.1a (a)–(e); the [drill-plan draft](../../notes/2026-09-26-tradeify-route-drill-plan-draft.md) §2.5, "mechanism step M".

## Selected outcome

One documentary determination of the vendor semantics that decide C-a on the exact route: our client, then CrossTrade REST `close`, then Tradovate liquidation of the position on an exclusively owned symbol. It has two parts:
- **Classification.** Every drill-plan M question and every §1.1a element (a)–(e) is classed `DOCUMENTED`, `CONFLICTING` or `OPEN`, each with its source.
- **Residual-risk statement.** For each element that is not `DOCUMENTED`: the worst credible outcome as a conditional inference, how it would be detected, and what bounds it.

This is **not** a trace, qualification, amendment acceptance or residual-risk acceptance.

## Inputs (read first)

- Packet §1.1/§1.1a; drill plan §2.5; REST assessment [§6 and §6.11](2026-09-25-crosstrade-rest-route-assessment.md).
- Retained vendor captures in the operator's primary checkout, `C:\Users\joshu\multi_firm_operations\local_artifacts\t08-rest-route-assessment-2026-09-25\` (`MANIFEST.tsv`, `QUOTE_INDEX.txt`). These are public pages, read in place. Cite the existing Q-IDs.
- T08 handoff §7 ([T08](2026-09-21-tradeify-t08-broker-protection-feasibility.md)); [CAP-20260916](../phase4-preparation/2026-09-16/capability-decision.md) rows L2(d) and L2(e); the rail spec's `CLOSE(scope)`, R-B3 L-2 (d)/(e), S5 and I7.

## Method and limits

1. **Reuse the retained captures first.**
2. **Retrieve official public documentation only for a named gap.** Fetch CrossTrade and Tradovate pages (API, help centre, execution internals) only where the captures do not settle a named M question or element.
   - Public retrieval only: no login, no account access, no vendor contact. Any vendor question is drafted for the operator to send.
   - Retain new captures under **your worktree's** `local_artifacts/close-semantics-2026-09-26/`, which is gitignored. Include `MANIFEST.tsv` (URL, capture UTC, bytes, SHA-256) and a quote index. The coordinator relocates them to the primary checkout.
   - Reproduce no vendor text beyond short quoted phrases; cite by ID.
3. **Keep documented behavior, inference and contradiction apart.** Do not treat NinjaTrader or another destination's semantics as Tradovate semantics. Do not treat CrossTrade-managed work as broker-native.
4. **For each element, establish four things:**
   - what the vendor documents;
   - whether that covers liquidation **while a protective order is working or in flight**;
   - whether it bounds reversal;
   - what completion evidence the documents make available (it must postdate preparation and be coherent; packet GC-3).

## Output

- `docs/notes/2026-09-26-close-semantics-c-a.md`, with these sections:
  1. Read report.
  2. Question and element classification table.
  3. Residual-risk statement, per element.
  4. Contradictions found. A *documentary* contradiction is reported for the operator; only a *trace* contradiction stops C-a under the ruling.
  5. What order-producing drills could and could not add: X-3, and X-5 (which is deferred).
  6. A draft vendor question for the operator, if needed.
  7. Limitations.
- A short executor-return section appended to this card.

## Forbidden

Account access, credentials, order actions, drills, vendor contact, spend, contract or owner edits, private strategy sources, `.env`, GLM or external model services. No claim that anything is qualified, accepted or authorized.

## Executor return (2026-09-26)

**Status:** RETURNED for coordinator acceptance. Documentary determination only; it accepts, authorizes, qualifies or releases nothing. **Dispatch revision:** `62c956f538dfa53f31eaec5951efc3ffa1dce53b`; the worktree `HEAD` was verified to descend from it before work began. **Executor:** assessor subagent (Claude Code, Opus 5.5), worktree `.claude/worktrees/close-semantics`, branch `claude/close-semantics-c-a`.

**Output:** [`docs/notes/2026-09-26-close-semantics-c-a.md`](../../notes/2026-09-26-close-semantics-c-a.md), with sections 1–7 as specified.

**Evidence:** `local_artifacts/close-semantics-2026-09-26/` in this worktree (gitignored). It contains:
- nine public captures made on 2026-09-26;
- `MANIFEST.tsv`, SHA-256 `74721db0f4223329c97a9e4ede2f03e0173fa20236f6b800b48617ae024d1d29`;
- `QUOTE_INDEX.txt` with IDs CS01–CS24, CR01–CR08 and CT01–CT14;
- `SHA256SUMS`.

The coordinator relocates the directory to the primary checkout.

**Findings.**
- **M questions.** All nine drill-plan M questions are `OPEN`, and none is `CONFLICTING`. §1.1a elements (a)–(e) are all `OPEN`.
- **No no-reversal mechanism is documented.** The residual-risk statement (§3 of the note) therefore covers every element.
- **Documented facts:**
  - A full close is one Tradovate `liquidateposition` request. It is quantity-less, cancels the contract's working orders and closes the position.
  - Tradovate calls it "not a guarantee".
  - Bracket children are not tied to the position.
  - Several other actors can liquidate the same symbol.
- **Contradictions.** There is no trace, so there is no trace contradiction. There is one documentary inconsistency, D-1: CrossTrade's generic command text says a close cancels "account-level" orders, while its Tradovate rows and Tradovate's own text say the cancellation is contract-scoped. The note resolves it to contract scope and reports it. It does not stop C-a.

**Routed to the coordinator (nothing edited outside the permitted outputs):**
1. Under packet §1.1 and drill plan CR-3, (a)–(c) remain `OPEN` after M. X-3 can therefore be authorized only as part of the operator's decision on the residual-risk statement.
2. Packet §1.1's C-a row says liquidation cancels "the OCO children". The sources say it cancels all of the contract's working orders, and Tradovate adds "not a guarantee" (note §4.4).
3. **Candidates for the GC-7 actor inventory** (drill plan §0.1):
   - the Tradovate platform's timed exit-and-cancel function (CS22);
   - firm-side Tradovate automatic liquidation (CT12, CT13).

   For the attended recovery flatten, Tradovate and CrossTrade document that a plain exit order leaves brackets working (CS09, CT02). The flatten must therefore also cancel working orders, which the drill plan's §2.0 recovery step already requires.
4. **X-3 read additions** (not adopted): read the lifecycle of the liquidation order and of both children, and record whether their command and report rows carry timestamps (note §5).
5. **Draft vendor question** (note §6) for the operator's decision. It is not sent.

**Not done:** account access; vendor contact; drills or order actions; spend; contract or owner edits; private strategy sources; `.env`; GLM or other external model services.
