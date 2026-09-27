# M2 — rejected-modify semantics for L2(c): bounded handoff

**Status:** DISPATCH-READY 2026-09-27. The coordinating session carded this on the operator's instruction "dispatch the M2". **It executes only in a local session in the operator's primary checkout** (§0.5). **Dispatch revision:** the `origin/main` commit that carries this card after the operator merges PR #520, recorded as a frozen SHA in §9 at dispatch. The executor cuts its branch from that commit and verifies that `HEAD` descends from it. **Executor:** one documentary assessor in its own worktree of the primary checkout. **Coordinator:** accepts or corrects the return.

**What M2 is.** The documentary vendor-semantics step for GC-2b, "Rejected modify keeps the old stop (L2(c))" ([B–D packet](../../notes/2026-09-26-tradeify-bd-decision-packet.md), GC-2b row; its validation method is "Vendor semantics (drill-plan M2 …), then D2"). The [drill-plan draft](../../notes/2026-09-26-tradeify-route-drill-plan-draft.md) §2.2 defines M2 as "Documentary, like M (§2.5)", and states that its return "is a precondition of X-2". The same plan's authorization table puts M2 at "Documentary; vendor contact by the operator only. Not an account action; needs a coordinator dispatch". The [route commissioning packet](../../notes/2026-09-27-route-commissioning-session-packet.md) §4.3 holds X-2 at "READY ON M2's return".

**Precedent.** This card follows the M step for C-a ([close-semantics handoff](2026-09-26-close-semantics-c-a.md); [return](../../notes/2026-09-26-close-semantics-c-a.md), with its 2026-09-27 addendum). The method, evidence rules and output shape are the same, applied to modify instead of close.

**Form.** Restructured 2026-09-27, before dispatch, into the numbered handoff sections that `scripts/check_brief.py` checks ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision), handoff contract item 1; [ruling 2026-09-27](../../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-27)). Scope, grants and acceptance are unchanged. Every earlier section's text moves verbatim under a numbered heading: Inputs into §0, Routing to §0.5 and Output into §6. Only section references change (§Routing is now §0.5; §Dispatch record is now §9). The lead of §0, §4, the status lines of §6, §10 and the last §9 line are new, and each restates a requirement this card or the ADR already makes. The earlier text is at `git show ed3e476:docs/briefs/handoffs/2026-09-27-m2-modify-semantics.md`. The premise check (§9) compares the card at the dispatch revision with this text, so the frozen SHA must be a commit that carries this restructure.

## 0. Phase 0: read first, then report before any research

The executor's first act is the dispatch-time premise check in §9, reported before any research. Any failure is a stop (§7), returned under §6. A contradiction between this card and what the executor reads is returned as `NEEDS_CONTEXT` ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision), handoff contract item 2); the executor does not choose a reading itself.

**Test 0 (vendor bytes and secrets).** The reads include gitignored vendor captures: the two retained directories named in §0.5, read in place in the primary checkout. The confirmed-present check for this dispatch is §9's premise check: both directories exist and their manifests verify. No read touches a credential or a secret (§5).

**Inputs (read first).**

- Drill plan §2.2 (M2 and X-2) and §2.5 (M, as the method precedent).
- The B–D packet: GC-2b and GC-3; the §1.2 rows on modify of fixed stop/target and on unknown cancel, amend or close; B-4 and B-5 (ORB and Vanguard noop amends).
- REST assessment: [§6 and §6.11](2026-09-25-crosstrade-rest-route-assessment.md), including the `change` → Tradovate modify mapping and Q21.
- [T08 handoff](2026-09-21-tradeify-t08-broker-protection-feasibility.md) §7.
- [CAP-20260916](../phase4-preparation/2026-09-16/capability-decision.md): the L2(c) rows, including N1-c.
- The rail spec's R-B3 L-2 (a cancel/replace cannot satisfy L2(c)).
- The retained captures listed under §0.5, read in place. Cite their existing Q-IDs and quote IDs.

Last-modified anchors of the linked inputs at this restructure (`git log -1 --format='%h %as' -- <path>` on `origin/main` `ed3e476`):
- `docs/notes/2026-09-26-tradeify-route-drill-plan-draft.md`: `6479f0e` 2026-09-27;
- `docs/notes/2026-09-26-tradeify-bd-decision-packet.md`: `d42c467` 2026-09-26;
- `docs/notes/2026-09-27-route-commissioning-session-packet.md`: `6479f0e` 2026-09-27;
- `docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md`: `121f07d` 2026-09-26;
- `docs/briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md`: `af81e54` 2026-09-26;
- `docs/briefs/phase4-preparation/2026-09-16/capability-decision.md`: `bccaf53` 2026-09-24;
- `docs/briefs/handoffs/2026-09-26-close-semantics-c-a.md` and `docs/notes/2026-09-26-close-semantics-c-a.md`: `e52c962` 2026-09-27.

## 0.5. Routing (task-routing checklist, re-applied at dispatch)

`Routing: local` for two reasons:
- **The retained vendor captures exist only in the operator's primary checkout.** They are gitignored and absent from a fresh or cloud checkout:
  - `local_artifacts/t08-rest-route-assessment-2026-09-25/` (REST assessment Q-IDs, including Q21);
  - `local_artifacts/crosstrade-close-research-2026-09-27/` (637 files, `SHA256SUMS.all`, recorded by commit `e52c9621`).
- **The coordinating cloud session's network policy denies the vendor documentation hosts** (`crosstrade.io` and `api.tradovate.com` returned 403 at the proxy on 2026-09-27).

A cloud executor could reuse neither the captures nor the vendor pages, and it could not produce byte-level captures.

## 1. Selected outcome

One documentary determination of the modify semantics on the exact route: our client → CrossTrade REST `change` → Tradovate modify of a working stop child of an OSO bracket. It has two parts:
- **Classification.** Each M2 question below is marked `DOCUMENTED` (bound to a source), `CONFLICTING` or `OPEN`. Nothing is inferred from silence.
- **What X-2 could and could not add.** Map the classification onto the X-2 row: what a pass would validate, and what stays undocumented after it (drill plan §2.2, the "Does NOT establish" row).

This is **not** a trace, a qualification, an L2(c) acceptance or an edition decision.

## 2. Questions (verbatim from drill plan §2.2)

For CrossTrade `change` → Tradovate modify:
1. After a rejected modify of a working stop, does the original order stay `Working` at its original price?
2. A version can exist for a command Tradovate later rejects (Q21): what state does the order show in that interval, and after the rejection?
3. Is an accepted modify atomic, with the old stop effective until the new one is?
4. What does a modify with an unknown outcome leave working?

Also record, for X-2's GC-3 line: whether the command report and the order's lifecycle or version reads carry broker timestamps or versions that could postdate a send.

## 3. Method and limits

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

## 4. Verification (falsifier-first)

This section adds no requirement. It restates the card's existing requirements as the checks the coordinator applies to the return, and names the section each comes from.

**H:** the return classifies each of Q1–Q4 and the GC-3 record, for the exact route in §1, as `DOCUMENTED`, `CONFLICTING` or `OPEN`; it binds each class to a cited source ID; and it keeps documented behavior, inference and contradiction apart. **Reject if** any item below is falsified; **accept if** all hold on the returned head.
- **Premise check first** (§0, §9). *Falsified by* research reported before the premise check, or a premise-check failure that did not stop the work.
- **Classification** (§1; §6 note item 2). *Falsified by* a question or the GC-3 record with no class, a class with no source ID, or a class inferred from silence.
- **Route fidelity** (§3 items 3 and 4). *Falsified by* NinjaTrader's or another destination's semantics read as Tradovate's, CrossTrade-managed work read as broker-native, the webhook command's behavior used for REST `change` without being labelled an inference, or a question whose entry does not say whether it covers a stop child of a working OSO bracket.
- **Completion evidence** (§3 item 4; §2). *Falsified by* a question whose entry omits what completion evidence the documents make available, or a missing GC-3 record.
- **What X-2 could add** (§1; §6 note item 3). *Falsified by* a claim that an X-2 pass validates more than M2 documents.
- **Captures** (§3 item 2; §5). *Falsified by* a new capture with no `MANIFEST.tsv` row (URL, capture UTC, bytes, SHA-256) or quote-index entry, a committed capture, or vendor text beyond short quoted phrases.
- **Output shape** (§6). *Falsified by* a note missing any of its six sections, no executor-return section on this card, or a PR holding anything but the note and that section.
- **Limits** (§5). *Falsified by* any §5 move, including any claim that L2(c) is qualified, accepted or authorized.

An `OPEN` or `CONFLICTING` class is a valid result, not a failure: §6 note item 5 turns it into a draft vendor question for the operator.

## 5. Forbidden

- account access, credentials, order actions, drills, vendor contact or spend;
- contract or owner-record edits: the drill plan, B–D packet, rail spec, REST assessment and pre-registrations are read-only here;
- private strategy sources, `.env`, GLM or other external model services;
- committing captures or vendor text beyond short quoted phrases;
- any claim that L2(c) is qualified, accepted or authorized.

## 6. Output and return (status taxonomy)

- `docs/notes/2026-09-27-m2-modify-semantics.md`, with these sections:
  1. Read report.
  2. Question classification table (Q1–Q4 plus the GC-3 record), each with its source ID.
  3. What X-2 could and could not add. A pass validates only what M2 documents (drill plan §2.2). If M2 leaves the mechanism undocumented, a pass shows only that one attempt did not fail.
  4. Contradictions found. A documentary contradiction is reported for the operator. Only a trace contradicts a mechanism.
  5. A draft vendor question for the operator to send, if any question stays `OPEN` or `CONFLICTING`. It is not sent.
  6. Limitations.
- A short executor-return section appended to this card.
- A `claude/*` branch cut from the frozen dispatch revision on `origin/main`, with one PR holding only the note and this card's return section. The operator merges.

**Status.** The executor-return section states exactly one:
- `DONE`: the note, the return section and the PR above exist, and every §4 item holds.
- `DONE_WITH_CONCERNS`: as `DONE`, plus a named concern that the coordinator adjudicates before the operator merges.
- `NEEDS_CONTEXT`: a §7 stop that is an ambiguity or a contradiction in this card or its premises: a route ambiguity that changes a class, or a premise-check mismatch in `HEAD`, this card or the drill plan (§9). Name it with the evidence and stop.
- `BLOCKED`: any other §7 stop: an answer needs a login, account access, a credential, vendor contact, an order action or a trace; the retained captures are missing or do not verify; or two failed corrections of the same issue. Name it and stop.

The coordinator accepts the return (verdict RESOLVED: every §4 item holds) or corrects it (verdict FALSIFIED: an item fails, named).

## 7. Stop conditions (return to the coordinator; do not work around)

- An answer needs a login, account access, a credential or vendor contact.
- An answer needs an order action or a trace of any kind.
- A question is ambiguous about the route (REST `change` versus the webhook form, or OSO child versus standalone order), and the choice changes its class.
- The retained captures are missing from the primary checkout.
- Two failed corrections of the same issue (AGENTS.md).

## 8. Decision unlocked

M2's return is one of X-2's preconditions (commissioning packet §4.3). X-2 also still needs:
- X-1's pass;
- the drill-plan owner's confirmation of the fresh-position precondition;
- the §3.7 request-body item for its opening entry;
- its own CP-3 written authorization.

If Q1 is not `DOCUMENTED`, the GC-2b consequence (Striker and Aegis: OPERATOR DECISION, with alternatives) may be put to the operator on the documentary result, before any trace.

**Not granted:** any drill, order, account read, vendor contact, spend, merge, arm, deployment or GO.

## 9. Dispatch record

- **Dispatch-time premise check (the executor's first act, reported before any research):**
  - `HEAD` descends from the frozen dispatch revision, and the card there matches this text;
  - both retained capture directories named in §0.5 exist, and their `MANIFEST.tsv`, `SHA256SUMS` or `SHA256SUMS.all` verify with `sha256sum -c`, or the equivalent;
  - the drill plan §2.2 M2 questions are unchanged at the dispatch revision.

  Any failure is a stop.
- **Sequencing (operator guidance on PR #520, 2026-09-27):** land this card through the operator's merge of #520, then dispatch locally with the frozen SHA. M2 is not a prerequisite for CP-1a. It supports X-2's preparation and does not authorize X-2's execution; X-2's other prerequisites remain.
- **2026-09-27:** carded on the operator's instruction "dispatch the M2". Execution needs a local session in the primary checkout (§0.5). The coordinating cloud session cannot run it. **Owed:** the operator merges #520, then starts a local session in the primary checkout on the frozen revision. Until then M2 is **not executing**.
- **2026-09-27 (restructure, PR #532):** #520 has merged, but it carries the pre-restructure text. **Owed now, superseding the line above:** the operator merges #532, then starts a local session in the primary checkout on a frozen revision that descends from #532's merge commit. A revision without the restructure fails the premise check (the card at the dispatch revision must match this text).

## 10. Audit hooks (runnable)

```bash
# Card form (surface-allocation ADR, handoff contract item 1). Expected: RESULT: well-formed
python scripts/check_brief.py docs/briefs/handoffs/2026-09-27-m2-modify-semantics.md

# §9 premise check, in the executor's worktree of the primary checkout (Git Bash).
# <dispatch-sha> is the frozen SHA recorded in §9; <primary> is the primary checkout's absolute path.
git merge-base --is-ancestor <dispatch-sha> HEAD && echo "HEAD descends from the dispatch revision"
git diff --exit-code <dispatch-sha> HEAD -- docs/briefs/handoffs/2026-09-27-m2-modify-semantics.md
# The drill plan's §2.2 at the dispatch revision; compare its Questions row with §2 of this card.
git show <dispatch-sha>:docs/notes/2026-09-26-tradeify-route-drill-plan-draft.md | sed -n '/^### 2\.2 /,/^### 2\.3 /p'
# Close-research captures: pin the index to its recorded digest, then verify every capture against it.
(cd "<primary>/local_artifacts/crosstrade-close-research-2026-09-27" \
  && echo "8dd20292daa98f0fee17f3c0e0c9f2585696eee7303791dc61bf8a883b70dbe6  SHA256SUMS.all" | sha256sum -c - \
  && sha256sum -c --quiet SHA256SUMS.all)
# REST-assessment captures: only digest prefixes are recorded (REST assessment, Evidence directory row):
# MANIFEST.tsv d069ae7e, EVIDENCE_INDEX.sha256 c0fd2c95. Compare both; a mismatch is a stop.
(cd "<primary>/local_artifacts/t08-rest-route-assessment-2026-09-25" \
  && test "$(sha256sum MANIFEST.tsv | cut -c1-8)" = d069ae7e \
  && test "$(sha256sum EVIDENCE_INDEX.sha256 | cut -c1-8)" = c0fd2c95 && echo "REST indexes pinned")
# Then verify the captures against the pinned index. The operator's 2026-09-26 spot-check recorded
# that 5 of its 227 entries are notes, not file paths, and cannot pass a plain sha256sum -c. Those
# 5 are the only failures allowed; any other failed or missing entry is a stop.
(cd "<primary>/local_artifacts/t08-rest-route-assessment-2026-09-25" && sha256sum -c --quiet EVIDENCE_INDEX.sha256)
```
