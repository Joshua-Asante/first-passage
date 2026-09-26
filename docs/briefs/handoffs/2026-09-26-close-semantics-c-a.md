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
