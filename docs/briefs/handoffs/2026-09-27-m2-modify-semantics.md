# M2 — rejected-modify semantics for L2(c): bounded handoff

**Status:** DISPATCH-READY 2026-09-27. The coordinating session carded this on the operator's instruction "dispatch the M2". **It executes only in a local session in the operator's primary checkout** (§Routing). **Dispatch revision:** the `origin/main` commit that carries this card after the operator merges PR #520, recorded as a frozen SHA in §Dispatch record at dispatch. The executor cuts its branch from that commit and verifies that `HEAD` descends from it. **Executor:** one documentary assessor in its own worktree of the primary checkout. **Coordinator:** accepts or corrects the return.

**What M2 is.** The documentary vendor-semantics step for GC-2b, "Rejected modify keeps the old stop (L2(c))" ([B–D packet](../../notes/2026-09-26-tradeify-bd-decision-packet.md), GC-2b row; its validation method is "Vendor semantics (drill-plan M2 …), then D2"). The [drill-plan draft](../../notes/2026-09-26-tradeify-route-drill-plan-draft.md) §2.2 defines M2 as "Documentary, like M (§2.5)", and states that its return "is a precondition of X-2". The same plan's authorization table puts M2 at "Documentary; vendor contact by the operator only. Not an account action; needs a coordinator dispatch". The [route commissioning packet](../../notes/2026-09-27-route-commissioning-session-packet.md) §4.3 holds X-2 at "READY ON M2's return".

**Precedent.** This card follows the M step for C-a ([close-semantics handoff](2026-09-26-close-semantics-c-a.md); [return](../../notes/2026-09-26-close-semantics-c-a.md), with its 2026-09-27 addendum). The method, evidence rules and output shape are the same, applied to modify instead of close.

## Routing (task-routing checklist, re-applied at dispatch)

`Routing: local` for two reasons:
- **The retained vendor captures exist only in the operator's primary checkout.** They are gitignored and absent from a fresh or cloud checkout:
  - `local_artifacts/t08-rest-route-assessment-2026-09-25/` (REST assessment Q-IDs, including Q21);
  - `local_artifacts/crosstrade-close-research-2026-09-27/` (637 files, `SHA256SUMS.all`, recorded by commit `e52c9621`).
- **The coordinating cloud session's network policy denies the vendor documentation hosts** (`crosstrade.io` and `api.tradovate.com` returned 403 at the proxy on 2026-09-27).

A cloud executor could reuse neither the captures nor the vendor pages, and it could not produce byte-level captures.

## Selected outcome

One documentary determination of the modify semantics on the exact route: our client → CrossTrade REST `change` → Tradovate modify of a working stop child of an OSO bracket. It has two parts:
- **Classification.** Each M2 question below is marked `DOCUMENTED` (bound to a source), `CONFLICTING` or `OPEN`. Nothing is inferred from silence.
- **What X-2 could and could not add.** Map the classification onto the X-2 row: what a pass would validate, and what stays undocumented after it (drill plan §2.2, the "Does NOT establish" row).

This is **not** a trace, a qualification, an L2(c) acceptance or an edition decision.

## Questions (verbatim from drill plan §2.2)

For CrossTrade `change` → Tradovate modify:
1. After a rejected modify of a working stop, does the original order stay `Working` at its original price?
2. A version can exist for a command Tradovate later rejects (Q21): what state does the order show in that interval, and after the rejection?
3. Is an accepted modify atomic, with the old stop effective until the new one is?
4. What does a modify with an unknown outcome leave working?

Also record, for X-2's GC-3 line: whether the command report and the order's lifecycle or version reads carry broker timestamps or versions that could postdate a send.

## Inputs (read first)

- Drill plan §2.2 (M2 and X-2) and §2.5 (M, as the method precedent).
- The B–D packet: GC-2b and GC-3; the §1.2 rows on modify of fixed stop/target and on unknown cancel, amend or close; B-4 and B-5 (ORB and Vanguard noop amends).
- REST assessment: [§6 and §6.11](2026-09-25-crosstrade-rest-route-assessment.md), including the `change` → Tradovate modify mapping and Q21.
- [T08 handoff](2026-09-21-tradeify-t08-broker-protection-feasibility.md) §7.
- [CAP-20260916](../phase4-preparation/2026-09-16/capability-decision.md): the L2(c) rows, including N1-c.
- The rail spec's R-B3 L-2 (a cancel/replace cannot satisfy L2(c)).
- The retained captures listed under §Routing, read in place. Cite their existing Q-IDs and quote IDs.

## Method and limits

1. **Reuse the retained captures first**, including the 2026-09-27 close-research set, which may already cover Tradovate order-modify pages.
2. **Retrieve official public documentation only for a named gap.** Where the captures do not settle a question, fetch CrossTrade and Tradovate public pages: API reference, help centre, order-state documentation.
   - Public retrieval only: no login, no account access, no vendor contact.
   - Retain new captures under **your worktree's** `local_artifacts/modify-semantics-2026-09-27/`, which is gitignored. Include `MANIFEST.tsv` (URL, capture UTC, bytes, SHA-256) and a quote index. The coordinator or operator relocates them to the primary checkout's `local_artifacts/`.
   - Reproduce no vendor text beyond short quoted phrases; cite by ID.
3. **Keep documented behavior, inference and contradiction apart.**
   - Do not treat NinjaTrader or another destination's semantics as Tradovate semantics.
   - Do not treat CrossTrade-managed work as broker-native.
   - Do not treat the webhook command's documented behavior as the REST `change` behavior without saying it is an inference (the M return's F1 pattern).
4. **For each question, establish three things:**
   - what the vendor documents;
   - whether that covers a stop child of a working OSO bracket (not only a standalone order);
   - what completion evidence the documents make available (it must postdate the send and be coherent; packet GC-3).

## Output

- `docs/notes/2026-09-27-m2-modify-semantics.md`, with these sections:
  1. Read report.
  2. Question classification table (Q1–Q4 plus the GC-3 record), each with its source ID.
  3. What X-2 could and could not add. A pass validates only what M2 documents (drill plan §2.2). If M2 leaves the mechanism undocumented, a pass shows only that one attempt did not fail.
  4. Contradictions found. A documentary contradiction is reported for the operator. Only a trace contradicts a mechanism.
  5. A draft vendor question for the operator to send, if any question stays `OPEN` or `CONFLICTING`. It is not sent.
  6. Limitations.
- A short executor-return section appended to this card.
- A `claude/*` branch cut from the frozen dispatch revision on `origin/main`, with one PR holding only the note and this card's return section. The operator merges.

## Stop conditions (return to the coordinator; do not work around)

- An answer needs a login, account access, a credential or vendor contact.
- An answer needs an order action or a trace of any kind.
- A question is ambiguous about the route (REST `change` versus the webhook form, or OSO child versus standalone order), and the choice changes its class.
- The retained captures are missing from the primary checkout.
- Two failed corrections of the same issue (AGENTS.md).

## Forbidden

- account access, credentials, order actions, drills, vendor contact or spend;
- contract or owner-record edits: the drill plan, B–D packet, rail spec, REST assessment and pre-registrations are read-only here;
- private strategy sources, `.env`, GLM or other external model services;
- committing captures or vendor text beyond short quoted phrases;
- any claim that L2(c) is qualified, accepted or authorized.

## Decision unlocked

M2's return is one of X-2's preconditions (commissioning packet §4.3). X-2 also still needs:
- X-1's pass;
- the drill-plan owner's confirmation of the fresh-position precondition;
- the §3.7 request-body item for its opening entry;
- its own CP-3 written authorization.

If Q1 is not `DOCUMENTED`, the GC-2b consequence (Striker and Aegis: OPERATOR DECISION, with alternatives) may be put to the operator on the documentary result, before any trace.

**Not granted:** any drill, order, account read, vendor contact, spend, merge, arm, deployment or GO.

## Dispatch record

- **Dispatch-time premise check (the executor's first act, reported before any research):**
  - `HEAD` descends from the frozen dispatch revision, and the card there matches this text;
  - both retained capture directories named in §Routing exist, and their `MANIFEST.tsv`, `SHA256SUMS` or `SHA256SUMS.all` verify with `sha256sum -c`, or the equivalent;
  - the drill plan §2.2 M2 questions are unchanged at the dispatch revision.

  Any failure is a stop.
- **Sequencing (operator guidance on PR #520, 2026-09-27):** land this card through the operator's merge of #520, then dispatch locally with the frozen SHA. M2 is not a prerequisite for CP-1a. It supports X-2's preparation and does not authorize X-2's execution; X-2's other prerequisites remain.
- **2026-09-27:** carded on the operator's instruction "dispatch the M2". Execution needs a local session in the primary checkout (§Routing). The coordinating cloud session cannot run it. **Owed:** the operator merges #520, then starts a local session in the primary checkout on the frozen revision. Until then M2 is **not executing**.
