# 11-08 sitting decision packet

**What this is:** the open decisions for Joshua's 2026-11-08 sitting, with options, downstream effects and recommendations. It was built from seven cluster analyses, each checked by an adversarial critique. It decides nothing. Where a recommendation changed because of the critique, the text says so. Private records are named only as "private record, confirm locally".

**Citation base.** For the checklist, `f96a657` is cited. It is the last main that still has the doc corpus: it is PR #1099, cut 1/2, and the corpus was deleted afterwards by 5510ca9 in #1100. I verified that the checklist is byte-identical to `b7eaff7` except at line 1099. Other deleted docs are cited at `b7eaff7`. "CK" means `docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md`.

**Two briefing corrections to read first.**
1. **T2 has been reversed.** `b7eaff7` CK:1099 reads "T2 stands: no agent or Codex acts on the eval". Joshua reversed that the same day in #1096 (a31aabc, 15:19 on 11-05). The text in force is `f96a657` CK:1099: "Agents may act on the eval on his direction, and under the standing GO for the weekly trade … T2 stays open: Joshua accepts that venue risk." Current AGENTS.md:17-23 matches it. T1 has never been ruled.
2. **Only rows 2, 3 and 12 of the reconciliation table are accepted** (CK:1078). The table itself is "Proposed, not accepted" (CK:1034). The 11-05 bare-bones path replaced rows 8-10 and open items 6-7 (CK:1032). Rows 1, 4, 5, 6, 7, 11, 11a and 13 are still open. Joshua can also reject the framing of a row, not just choose between its options.

---

## Eval-path decisions

### D1. Evidence case for the first forward attempt (row 1)

**Question.** What evidence is enough to start the ORB + Aegis pair on the owned Select 100K?

**State.** The question is at CK:1040. The 11-08 ruling says the 10-19 finding is an advisory prior and "the pair's own gates bind" (CK:1076). Rule 26 binds "each run's own pre-registered gates". The forward stop rule describes itself as "the committed registration that Rule 23 requires before the first forward session" (`docs/briefs/pre-registration/2026-10-31-tradeify-forward-stop-rule-registration.md:3`). The framework is a DRAFT that "decides nothing" (`docs/briefs/pre-registration/2026-10-26-tradeify-native-lane-prereg-DRAFT.md:3`). So the record points at the stop rule as the pair's own gate. STATE.md:15 still says "no configuration has an evidence case".

**The ORB identity gap.** T00 trial 13 records that "the author's model used the book's ORB O-N series; the native ORB build binds the unread solo O-0 configuration" (`discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json`, trial 13). Modelled evidence on O-N does not transfer to O-0. STATE.md:9 still calls the leg "ORB MNQ v7".

**The cards may not be edge evidence.** The signed cards are hash-registered at `docs/evidence/PRIVATE_EVIDENCE.sha256:421` (Aegis card 1c) and `:427` (ORB card 1). Their filenames sit beside freeze and adjudication files, which suggests build or port cards rather than edge evidence. Private record, confirm locally.

| Option | Unblocks | Risks / forecloses | Reversibility |
|---|---|---|---|
| A. The signed cards plus the stop rule are the evidence case | Closes row 1 | Only works if the cards actually state an evidence basis, which is doubtful (see above) | Until session 1 |
| **E. No pre-session evidence case is required; the stop rule is the pair's own gate; the gaps are named as accepted risk** | Closes row 1 whatever the private cards contain. Honest about what is missing | Accepts a weak prior. The 10-19 composition grid was exploratory, ran with protection off, and used book ORB legs, not O-0 | Until session 1. A bust cannot be undone |
| B. Must clear framework gates G0-G4 first | A statistical gate | Weeks to months: no §7 recipe, #940 open, rule citations dead. As written it conflicts with the data rules (see D2) | Fully |
| C. Accept, plus a pre-session descriptive backtest check | — | Not publicly re-runnable (TV exports are private and Codex cannot see them). It is a fresh look at the unread O-0 data, so it adds to K. It spoils any later clean route through the framework | Low |
| F. Start one leg only | Removes the cross-leg risk in session 1 | Each leg has its own negative prior. The per-leg cap split would need restating | Until session 1 |
| D. Defer | — | ORB's forward window shortens against its date gate (addendum-1 `:14`). No GO is consumed by waiting | Fully |

**Downstream.**
- If the stop rule drops one leg, a single-leg configuration remains. The acceptance should say whether that leg continues.
- The funded 100K starts at 3 minis / 30 micros (`b7eaff7:docs/notes/2026-11-01-tradeify-venue-deep-dive-DRAFT.md:21`), so the eval split may not fit after a pass.
- An eval pass is not evidence of edge (framework §5; native plan :94).
- A bust means a reset or rebuy, which is a spend decision under money control 6 (venue prices: `lab/analysis/_inbox/prop_payout_geometry_2026-10/programs.py:10`).

**Recommendation: E. The critique changed this from A/C to E and dropped C.** Suggested wording:

> "For the first forward attempt on the owned Select 100K, no pre-session statistical evidence case is required. The pair's own pre-registered gate is the 10-31 forward stop rule plus Addendum 1, unchanged. Accepted as risk on the signed page: the 10-19 prior, the exploratory composition-grid signal, the workshop finding that no out-of-sample edge is established, and that no O-N or model evidence transfers to O-0. A bust ends the attempt, and any reset is a fresh spend decision. This sets no precedent for scaling or new purchases."

**Questions.**
- Are cards 1c and 1 edge-evidence cards or build cards? (Private record, confirm locally.)
- Is the ORB leg O-0? Should STATE.md:9 drop the "v7" naming?
- After a stop-rule drop, does the surviving leg continue, or does it stop for a fresh decision?
- Does the acceptance cover the funded stage of this account, or only the eval?
- Do you still hold the recorder-text obligation that the pair "needs its own evidence case" (CK:1023, :1026)?

### D2. Nomination and what happens to the framework (row 4)

**State.**
- Row 4 is at CK:1043. No nominating amendment exists.
- G0 item 3 was superseded on 11-08, and an amendment is owed (CK:1079).
- The framework still carries branch (d) parking language (framework :5, :93) and cites rules in the deleted `docs/operational_rules.md`.
- Its §2 item 1 puts parameters "fixed in the nominating amendment" (:44). Its §10 says a reviewer re-runs the gates "from the merged amendment and the public tooling" (:124). For locked strategies in a public repo, both conflict with AGENTS.md data rules.
- A public trial ledger already exists: T00 trial 13, with quantities bound by a private hash.

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| **B/F. The framework does not gate this attempt. The nomination is the expressions in the signed cards at PRIVATE_EVIDENCE.sha256:421/:427 (T00 trial 13, ORB leg = O-0). The horizon edition substitutes only through Addendum 1** | Closes row 4 with no new brief and uses existing anchors | The framework stays stale unless it gets a pointer | Before session 1 |
| A. Ratify the framework and nominate under it | — | As written it cannot be carried out without breaching the data rules (parameters in public text, Codex review of gate evidence). Brings back D1-B's delays | Low (it freezes) |
| C. Amend the framework (carve-out plus repairs), keep it DRAFT | Removes contradictions | Effort on a draft that may never be used | High |
| D. Retire the framework to git history | Matches the cut | Loses the only drafted economics gate for scaling | High (git) |
| E. Defer | — | The signed page cannot name what is nominated | High |

**Recommendation: B in the F form.** The critique corrected two points: the cards are already hash-registered, and a public ledger exists. Add a one-line "does not gate the owned-100K attempt" pointer on the framework status line. That edit touches a gate document, so route it through Codex cross-review rather than merging it as doc-only. Leave full repair or retirement until a scaling or new-purchase decision needs a gate. See also D11.

**Questions.**
- Does admitting the horizon edition need a fresh nomination, or is it covered by Addendum 1?
- Keep the framework for future scaling, or retire it?

### D3. Account binding (row 5)

**State.**
- Row 5 is at CK:1044.
- The 11-05 path replaced §2.1-2.2 with "a static per-leg split of caps. Values stay private" (CK:1091), and the P2 gate with the signed page (CK:1090).
- Outside §2.1-2.2, the runbook config still names fields that loading requires: `day_loss_stop`, `unprotected_max`, `disconnect_max`, `outcome_window`, `fact_max_age`, `barrier_timeout`. "Loading rejects the configuration … if any field is unbound" (`b7eaff7:docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md:233-240`).
- The account choice may already be settled by a private 10-25 ruling (`b7eaff7:docs/notes/2026-10-24-assumption-challenge-rulings-proposal.md:19`). Private record, confirm locally.
- "The eval build uses S-PAIR's source set" (CK:1101). If the caps are compiled into the source, they must be fixed before S-PAIR runs.

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| **A. Confirm (or rule) the owned 100K now; fix the private values before the S-PAIR rerun; sign the full binding with build hashes on the signed page** | S-PAIR exercises the values that go live. Closes native plan D3 and framework §11 item 2 for release 1 | Changing values after S-PAIR forces a new rerun | Before session 1 |
| B. Sign the full binding now as a separate record | Row 5 visibly closed | Cannot name build hashes, so it gets signed twice | Before session 1 |
| C. Bind to a fresh Select 50K | Cheaper geometry | Needs spend approval, a new stop-rule registration (it names the 100K, :3), and contradicts the 11-05 path (CK:1083) | The purchase is not reversible |
| D. Defer | — | The signed page cannot be signed | High |

**Recommendation: A, amended per the critique.** The binding should also state:
- that it is eval-only, with a new split required at funded activation;
- an edition-swap clause tied to Addendum 1;
- that "only Aegis and ORB" means R1 MCL and any third leg need a new binding and registration;
- the preservation-trade placement rule (see D9);
- the native DD policy for this instance, confirmed by Joshua with its own admission or an explicit exception. Matching the frozen 1.5% / 0.40× literals does not make it an approved Tradeify policy. Money control 4 freezes the constants in `core/dd_protection.py`; it does not approve them for a new firm-tier instance. The 07-13 ADR rejects transplanting FXIFY's pair (`b7eaff7:docs/adr/2026-07-13-dd-protection-concept-not-constant.md:27-31`). `core/dd_geometry.py:25-39, 87-101` requires each instance's own admission and has no default. The Python constants stay untouched (Codex review).

Do not include a "sole operator" attestation until D8 is ruled.

**Questions.**
- Does your 10-25 ruling already settle the account?
- Are the caps source constants or instance properties? (Confirm locally.)
- Which runbook limits must the signed page still set?
- Does native DD sizing use the frozen constants?
- Is native ORB long-only? This matters for D9. Confirm locally and do not record the answer publicly.

### D4. Exclusivity (row 6)

**State.**
- Half (ii), ORB's §4 candidacy, is discharged by the 11-03 withdrawal (`b7eaff7:docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md:478-481`).
- What remains is the signature (CK:1045; framework G0 item 2, :45).
- Tradeify, 10-24: "allowed, as long as you are the sole owner and operator, and the strategy is not used at other prop firms" (`b7eaff7:…crosstrade-rest-route-assessment.md:398`).
- The 11-04 ruling "a different instrument counts as distinct" carries its own clause: "a contrary written answer reopens the ruling" (`b7eaff7:docs/notes/2026-11-01-generation-phase-strengthening-DRAFT.md:508`).
- T-1105, Tradeify's AI agent, wrote that same logic on different instruments is the same strategy (`b7eaff7:docs/notes/2026-11-03-cross-firm-exclusivity-and-account-caps-DRAFT.md:121`). On the clause's plain text, the reopen has already been triggered. Only the outcome is unruled.

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| **E. Sign broad scope publicly (released implementations, editions, successors, and the same logic on any instrument). Record the 11-04 ruling as reopened by T-1105, outcome pending a human answer. Optionally send one question to the human Compliance Manager** | Row 6 closes. The records stay consistent | Overrides, for ORB/Aegis-logic strategies, the 11-03 "index not Tradeify-only" ruling (generation note :498) and R1's distinctness basis (`b7eaff7:…builder-r1-mcl-one-card-reregistration-DRAFT.md:54`) | Easy to relax. A breach found by Tradeify is not reversible |
| B. Narrow scope; keep the 11-04 ruling | Keeps different-instrument variants open | Contrary to the only written answer. The downside lands on the eval | — |
| C. Narrow scope plus an interim bar plus a question | — | Keeps the 11-04 ruling "standing" while the bar denies it in practice, so the records contradict each other | High |
| F. Release-1 statement only; park the instrument question until a multi-firm deployment is proposed | Cheapest | Leaves the T-1105 conflict open; it would have to be named as risk | High |
| D. Defer | — | Row 6 stays a blocker, for a statement that costs nothing | — |

**Recommendation: E. The critique changed this from C, which left the records inconsistent.** State what it means for the 11-04 FX 6J→MFFU mapping (generation note :525). A different-logic 6J strategy elsewhere is permitted on the record but is exposed to Tradeify's "similar orders" scan and to ESA §6.7 (T3). If a question is sent, send it on a compliance ticket, not on the CME-copied thread #04738415.

### D5. Native build authority (row 7)

**State.**
- Branch (b) granted read-only stage 1 only: "no strategy code, build…" (CK:1018).
- A partial public trace exists. v11 registration :15 cites "Joshua, 2026-10-31: 'GO route b'", and CK:1036 names a private 10-31 ruling to release both strategies.
- The 11-05 addendum says it "changes frozen Rule 10 only as stated here, and no other rule" (CK:1083). Whether it lifts the branch (b) limit is contestable, so this needs an explicit ruling.
- STATE.md:11 still says read-only.
- The native NinjaScript is an executable port and must stay private (native plan :50). Codex therefore cannot carry out or review steps 1 and 3.

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| **A or B, plus enumerated forward authority: confirm the private ruling's date and words (A), or ratify the earlier canaries as of 11-08 (B). Then list what is authorized: the S-PAIR rerun; the eval build installed disabled on the trading host under the step-3 GO; the horizon-edition v2 build and Sim101 canary from 11-09 (v11 :19). No canary runs during an armed session. Codex is excluded from the private source** | Steps 1 and 3 stop contradicting the public record | Joshua must supply or confirm the wording | Forward authority can be revoked |
| C. Authority starts only at 11-05; earlier canaries are evidence only | A clean chain | Narrows what the signed page can rely on | High |
| D. Defer, or fold into the signed page | — | Steps 1 and 3 come before the page (step 4), so this would invert the order | — |

**Recommendation: A if Joshua can name the ruling, otherwise B, with the enumerated list (added per the critique).** Joshua should also name what check stands in for cross-review of the private eval build, since AGENTS.md review cannot reach it. Fix STATE.md:11-14 in the same PR.

### D6. Wait for Tradeify's reply to the 11-05 source email? (row 11)

**State.**
- Row 11 is at CK:1050. "Starting without Tradeify's reply" is still Joshua's (CK:1103).
- The request came on the CME ticket thread with CME Data Sales copied, and asked about "optional export functionality" (route :402). Joshua's 10-26 data-terms question is unanswered (:403). Verification timing is open (:408).
- Tradeify's support is fast: an answer within 2 minutes on 10-12 (route :376), within 2 days on 10-22/24, and within about a minute on 11-05. The analysis's "slow and lapsing" claim was wrong. Only the compliance manager's follow-up is unanswered.
- Native plan :57 (written answer on ownership for the candidate) is a separate obligation from source review. Tradeify's existing answer is general guidance only. Eligibility of the exact candidate stays open (`b7eaff7:docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md:401-407`). Neither a source-review deadline nor Joshua's exclusivity signature supplies it.

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| A. Wait indefinitely | Strongest posture | No end date | Fully |
| **B'. Wait until a fixed calendar date that Joshua picks (for example 11-19), set independently of any GO, with the first session GO issued only after it passes (tying it to the GO would be circular; Codex review), with Joshua sending a notice of intent rather than asking permission: "Unless you object by <date>, I will enable the strategy whose source I sent on <send date>; I will record the enable on video and keep logs." If the eval build is re-sent before session 1, a fresh notice goes with it and session 1 waits for that notice's deadline or a reply** | A dated path that puts the burden on Tradeify. No pre-approval gate gets created | If Tradeify requests a code change after session 1, the build is no longer S-PAIR's source set: S-PAIR must be rerun and the source re-sent. That alone does not end the stop rule's record. Registration :17 covers changes to the rule, and Addendum 1 admits the horizon successor without a rule change. Which other build changes need a fresh forward record is Joshua's question (Codex review) | Until session 1 |
| C. Proceed now | Fastest | Little time gained, since other rows are open | Until session 1 |
| D. Defer | — | Could become a last-minute blocker | Fully |

**Recommendation: B'. The critique changed the question to a notice and the deadline to a calendar date.** Also:
- Re-ask the 10-26 data-terms question.
- Rule now that any eval-build change, including admitting the horizon edition, is re-sent by Joshua before it runs.
- On the signed page, name who flattens and disables on an objection: Joshua, or an agent under that week's GO.
- Joshua prepares a plain-language description of the strategy he can give without help, in case of a KYT interview (deep-dive :17).

**Questions.**
- Wait for a candidate-specific ownership answer, or supersede that prerequisite explicitly and name the unresolved eligibility risk on the signed page? (Separate from the source-review wait; Codex review.)
- Which build changes after session 1 need a fresh forward record, as opposed to an S-PAIR rerun and a re-send?
- Has a reply arrived? (Mailbox, confirm locally.)
- Did the 11-05 email go on the CME-copied thread?
- Do the sent source or the build write market data out of NinjaTrader?

### D7. Data rights, CME licence, feature entitlement (row 11a)

**State.**
- Row 11a is at CK:1051.
- CME asked for "confirmation on the feed" (feed note :358). Tradeify's Compliance Manager then confirmed CQG on that same thread (:359). CME's precondition may now be met, so the next step is Joshua's, not a stall.
- The research note reads §7.3 as binding the distributor, "not a data subscriber". It also says an evaluation destination on the same data "plausibly adds no" category (`b7eaff7:docs/notes/2026-10-10-cme-non-display-licensing-research.md:36-37`). Both are inference, and both were written for the personal Tradovate lane's separate feed, not for native use on the data Tradeify supplies. The same note's 10-12 operator read is stricter. Subscriber Addendum §4.2: "All Non-Display Use of CME Licensed Information requires a direct license with CME", with no exception. §6.1(j) requires a separate direct agreement. §7.3 "bears on prop-evaluation environments", and the absence of a real exchange order "is not stated as an exemption" (:115-143). Those questions are still open on ticket #04738415 (:145-149). Treat the category risk as a contested reading, not a probable no-category outcome.

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| A. Close everything first | Clean standing | Long stall | Fully |
| **C'. Partial: (1) Joshua follows up on CME ticket #04738415, citing Tradeify's CQG confirmation; (2) re-ask NinjaTrader/CQG for the distributor, the agreement and a Managed User route; (3) confirm locally which agreement and status the eval login shows; (4) entitlement check, either discharged by S-PAIR having run on the Tradeify-credentialed install, or done as a read-only check; (5) confirm whether the build exports data. The CME category stays a named risk with a pay-or-stop trigger** | Session 1 not held hostage. The breakable item is checked | Fee exposure, on inference | Before session 1 |
| B. Accept all of row 11a as risk | — | Leaves an entitlement gap undetected | Before session 1 |
| D. Buy a direct CME licence now | Strictest reading covered | Recurring spend that may be unnecessary | Monthly |
| E. Defer | — | — | — |

**Recommendation: C'. The critique added the CME follow-up and the "may already be done" entitlement point.** Any feature list derived from the private source stays in Joshua's checkout and never reaches Codex or the repo. Any licence purchase needs rule-6 approval.

### D8. T2: who places the weekly trade and acts on the eval

**State.**
- In force: agents may act on direction and under the standing GO, and T2 is accepted risk (`f96a657` CK:1099; AGENTS.md:17-23).
- Venue texts: "personally own, control, verify, and operate" (FAQ 17069653); ESA §6.7(b) bans third-party management; KYT checks "own decisions" (`b7eaff7:…venue-deep-dive-DRAFT.md:14-19`); VPN/VPS login is banned (register :214).
- The standing GO has never placed an order. Both recent weeks were placed by Joshua (`b7eaff7:STATE.md:90-91`).
- Agents hold no broker credential. The away-week benefit therefore exists only if his PC is on, logged in and computer use is enabled. Nothing in the record shows that has been set up.
- **Conflict:** D3 and D4 would have Joshua attest "sole owner and operator" while AGENTS.md authorizes agent placement.

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| A. Keep the 11-05 posture and write the reasoning the deep-dive asked for (:73-77) | No change | Agent fills are evidence against 17069653 and KYT. Inconsistent with a sole-operator attestation unless Joshua rules a directed agent order is his own act | Ruling yes, fills no |
| **Hybrid: Joshua places by default; an agent places only as a late-week fallback (no fill by a set Thursday ET time), only on his own already-authenticated PC, never from a VM or VPS** | Keeps miss-week insurance and limits agent fills to near-miss weeks | Still some T2 exposure | High |
| B. Hand placement only until Tradeify answers; agents verify read-only | Lowest exposure | Re-imposes the line he reversed on 11-05, and suspends directed agent action too. Miss-week risk, with deletion "after an email warning" (register :202) | High |
| C. Local attended surfaces only | Drops the remote-access reading | Does not answer the third-party-management reading | High |
| D. Revoke the standing GO | Clearest record | Same as B | New grant needed |

**Recommendation: the hybrid. The critique changed this from B.** Offer B if Joshua wants zero agent fills before a written answer, and say plainly that B overturns his 11-05 reversal. Any AGENTS.md edit touches money control 1, so it merges only at a Codex-clean head with green CI. A revocation takes effect on his word, before the PR lands. Whatever he rules, put T1 and T2 with their status back into STATE "Open decisions". Their only home (CK:1103) was deleted.

### D9. T1: the shape of the weekly trade

**State.**
- Severity H, never ruled (`b7eaff7:…venue-fact-register-DRAFT.md:252`).
- ESA §6.5 says to refrain from "flipping contracts just to register a 'trading day'". Current practice is a "market round trip" (`b7eaff7:STATE.md:88`).
- The 11-05 "Unchanged" list keeps the weekly-trade obligation, "a real trade each week" (CK:1101). The same addendum reserves T1 as still Joshua's (CK:1103), so T1 is open.
- Once instances run, a manual fill on MNQ or 6J is a §6.8 incident for the instance that owns that instrument (CK:1093). A fill on an instrument neither leg owns, or on another account, is unexplained and a stop (CK:1094; runbook U-12, :146). 6J is a leg instrument, not an "other" one. A manual position held while ORB holds the opposite direction in the Equity Index group would be prohibited hedging (`core/firm_rules.py:256-266`).

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| A. Keep the round trip | Cheapest | Most exposed reading of §6.5 | Weekly |
| **B. A genuine minimal trade: normal entry, held well past 10 seconds, exited in RTH, minimum size, never while an Aegis/ORB instance is enabled** | Removes the worst reading | Small P&L variance. If an agent places it with a resting stop, that goes beyond the standing GO's "round trip" scope unless Joshua restates the GO | Weekly |
| C. Strategy fills count once sessions run; the preservation trade goes only in weeks with no fill (B shape) | Removes T1 in session weeks | Does nothing for the week of 11-09 | High |
| D. Ask Tradeify first, keep current shape meanwhile | Possible safe harbour | Flags past round trips | Cannot unsend |
| New ruling: B is the required shape (CK:1103 left T1 open, so this is a fresh ruling, not a confirmation) | Settles T1's shape question | — | High |

**Recommendation: B from the week of 11-09, moving to C once sessions run.** Either hand-place it, or restate the standing GO to cover the bracket and exit.

### D10. Ask Tradeify about T1 and T2 (deep-dive Q4/Q5)?

**State.** The questions are drafted (deep-dive :81-89). No record shows they were sent. Agent placement was drafted as a question on 10-13 and dropped on 10-21 (CK:958; `b7eaff7:docs/notes/2026-10-21-tradeify-native-followup-questions-DRAFT.md:8`).

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| **A'. After switching shape (D9-B), Joshua sends Q5 (and Q4 if he accepts the attention) on a separate compliance ticket or #148959547, asking for a human answer** | The only route to actually settling T1/T2 | A "no" reaches back to past practice, and to directed agent actions in sessions, not just the weekly trade | Cannot unsend |
| B. Q5 only | Avoids spotlighting round trips | Selective disclosure, against "Send now, disclose" | Cannot unsend |
| C. Fold into the source-review thread | One conversation | That thread has CME Data Sales copied (route :402) | Until sent |
| D. Don't ask; accept both | No attention drawn | T1/T2 can never be settled | High |

**Recommendation: A'. The critique moved it off the CME-copied thread.** Do not rely on any reply for 11-09→11-13.

### D11. Native plan scope and "fund the expanded assessment" (STATE open decision 1)

**State.**
- In every record, "expanded" means the native plan's expanded P1: a read-only toolchain check plus a Tradeify entitlement check, 1-2 sessions, $0 (plan :82, :100; CK:1018). The STATE wording first appears in d603e81 and is ambiguous.
- No P2-P7 GO exists. The plan assumes a Select 50K (plan :87).
- D2(b) is moot (ORB v7 withdrawn as the §4 candidate). D4 is moot (personal lane closed). D3 is decided for the first account by the 11-05 path (CK:1083).

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| **B'. The 11-05 path governs the owned 100K. The plan and framework do not gate it. D2(b)/D4 moot; D3 decided for the first account only. Expanded P1 is either ruled overtaken (if S-PAIR ran on the Tradeify-licensed install) or granted alone ($0). The plan and framework are annotated or retired. No fee budget now** | A clean record. Closes the entitlement half of row 11a | No ratified scaling gate | High |
| A. Grant P1-P5 before any session | Framework-grade evidence | At least 9-11 weeks. Contradicts 11-05. The "sim fills are optimistic" objection applies equally to the simulated eval | High |
| C. B plus parallel framework ratification and a §7 recipe for scaling | A scaling gate | Rests on deleted rules and breaches the data rules as written. Competes with Codex review capacity (#940 is Codex's) | High |
| Light scale criterion: register a short criterion before session 1 that reads 100K forward trades to decide on a second account; it can never stop or resize the 100K pair | A scaling gate with no recipe | Must be frozen before session 1 | High |
| D. Defer | — | STATE, row 7 and the plan keep contradicting each other | — |

**Recommendation: B'. The critique dropped C.** Add the light scale criterion only if Joshua wants 100K results to inform scaling. Record the open scaling items:
- funded resize (30 micros against the 80-micro eval cap);
- the Elite Live bar on holding other accounts, including household (deep-dive :26);
- the spend ceiling. It survives c1's retirement: Joshua ruled on 11-03, effective 11-08, that it is re-homed to the retained Tradeify account's private owner record (`b7eaff7:docs/adr/2026-07-17-c1-rail-build-account-registration-go.md:517-521`). The fresh approval each spend needs (money control 6) is a separate control and does not replace the aggregate ceiling. Ask Joshua to confirm it is set in the owner record, or to supersede it explicitly. D15's survivor list (the 11-03 rulings) keeps it (Codex review).

### D12. Sequencing, GO cadence and signed-page contents (rows 13 and the fold)

**State.**
- 11-05 path: step 2 is done (CK:1097). Step 1's status is private. Steps 3-5 are open (CK:1085).
- "Every session needs its own GO" (CK:1101) and AGENTS.md's 7-day GO (:17-25) are compatible. AGENTS.md limits how long a GO is valid. It does not say one GO covers several sessions. So whether one weekly GO may authorize more than one session is an open question for Joshua, separate from D15. Ask it explicitly; D15 must not settle it by implication (Codex review).
- The runbook's "One session, then a recorded review before another" (runbook :127) was not superseded by 11-05.
- "Kept" is not a lock event for the stop rule. It already binds under AGENTS rule 5, and the lock comes at session 1 (registration :17).

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| **A. Rule the paper items first (order below), then the operational steps. Rows 6 and 7 are recorded publicly. Rows 1, 4 and 5 plus the risk acceptances go on the private, hash-registered signed page with a public headings-only contents list. Separate build GO and session GO; the first session GO covers session 1 only if the review rule survives** | Each step runs with its authority | — | Until session 1 |
| One weekly GO covering build and session 1, conditioned in writing on S-PAIR acceptance and the signed page | Fewer acts | Could cover session 2 before any review | High |
| B. Also wait for Tradeify and CME | Removes external unknowns | Open-ended | High |
| C. Defer ordering | — | The page has no defined content | — |

**Recommendation: A.** The signed page lists:
- the binding (D3);
- the evidence acceptance (D1) and nomination (D2);
- a restatement of the exclusivity statement (D4);
- what S-PAIR showed;
- the CK:1103 acceptances: starting without a reply, CME licence, T1, T2;
- candidate-specific ownership/eligibility (native plan :57): answer received, or the prerequisite superseded and the risk accepted;
- the native-control risks S-PAIR does not prove, named and accepted: protection across a disconnect on the firm connection, and the rest of the U tests that Sim cannot prove. State that the automatic incident close is not relied on (CK:1090);
- the attending operator's duties: account-wide incidents, stopping new risk across both legs, and the account loss stop, all under this page and the registered stop rule, with no cross-instance automation (CK:1095) (Codex review);
- row 11a residuals;
- who enables the strategy. Step 5 says "he enables himself", and Tradeify may ask for video of the enabling;
- the preservation-trade placement rule;
- the review-before-session-2 rule;
- the stop trigger for a Tradeify objection;
- what the step-3 "name readback" is (undefined in the public record).

---

## Research decisions

### D13. Mechanism clause 2-A falsifier

**Reading: NOT FIRED.** The trigger is the first three compliant campaigns dying at Stage-2 or Stage-6 (`b7eaff7:docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md:86`). None did. The compliant cards (MSL-S4 parked, `ops/instruments/MGC.md:92-97`; F1 per the critique, `docs/rejected_candidates.md:1340-1349`, where the four-clause status is not fully verified) both stopped before Stage-2. Its owner ADR and target text (harvest Requirement 1a) were deleted, and no active Path-1a campaign exists.

| Option | Reversibility |
|---|---|
| A. Not fired, carry to 2027-02-08 (nothing in the tree tracks that date) | High |
| **B. Not fired, retire as an unreachable check. Precedent: Joshua's 11-03 decompound ruling ("Retire with legacy book.", c43d4b7). Its recorded rationale, written by the recorder rather than quoted from Joshua, is that an impossible check adds no evidence when its subject has no live venue. The ground here differs: no compliant campaign exists** | High (reinstate from git) |
| C. Defer | High |

**Recommendation: B.** Record it in the sitting PR description.

### D14. Mechanism clause 2-C falsifier (executed-K closures)

**State.**
- The trigger is an examined read missing from a closure note, which means reverting ALL executed-K closures to declared K (ADR 07-26 :88).
- The ORB manifest reads executed_looks "none" (`discovery_manifests/orb_mnq_intraday_breakout.json:23`). Campaign-named RESULTS files exist, for example `lab/analysis/orb/orb_mnq_2026-07/RESULTS.md:5`.
- The current 2a89d3e guard would refuse this close (`lab/discovery/register_search.py:900-904`).
- The manifest states its aim: "close as operator-stopped with executed_k=0 so K arithmetic is unchanged" and "Banks 0 to keep K_banked(MNQ)=2" (:22-23). It is not established whether this was tool misuse or outcome-targeted K selection. Present both readings and assert neither.
- Both TXG1 closures also name no examiner, but their K does not move.
- Effects:
  - Family banks are disclosure-only.
  - The builder and T00 ledgers are unaffected.
  - At K=1 the ORB manifest would become valid promotion backing (`lab/discovery/k_ledger_check.py:56-60`).
  - **ST-EH promotion requirements change.** `lab/discovery/promotion_packet.py:205-225` reads the backing manifest's K and requires an extra DSR-floor attestation when `floor_at_k(K)` exceeds CAP. CAP is 1.0. At K=2 the floor is 0.85; at K=84 it is 1.615. So re-banking ST-EH adds that attestation to any promotion packet it backs. Ask whether the ruling should change ST-EH's promotion requirements or keep an explicit historical exception (Codex review).
  - The native-lane K disclosure counts the July look regardless (v7 S4 draft :64).

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| **A (if deleted rules bind). FIRED, enacted as written: ORB 0→1, ST-EH 2→84; correct all four manifest verdicts and MNQ.md:88; owner re-sums MNQ/MYM (derived 64 / 47, unreconciled); register_search operator-stopped closes bank declared K (keep the path; deleting it leaves stopped campaigns with no close); update the three affected test files; decide promotion backing** | Honours the falsifier | ST-EH disclosure becomes conservative | Effectively one-way |
| **H (if they don't bind). Record the reading as FIRED, history only. Correct ORB to K=1 for accuracy. Keep ST-EH at 2 only after its enumeration is audited. Same register_search change** | Accuracy without precedent | — | High |
| F. A, then a new forward-only executed-K rule using the 2a89d3e guards | Keeps the ADR's case against always banking declared K | One more rule | High |
| B. Not fired (08-18 confirmation covers it) | No edits | Weak: 08-18 adjudicated the bank, not the enumeration | High |
| C. Retire without ruling | Minimal | Retiring a falsifier that just read FIRED looks like dodging it | — |
| D (as drafted). Limit the consequence to ORB | — | **Do not offer as drafted:** it claims an ST-EH audit that never ran (2-C check :97-98) | — |

**Recommendation: answer D15 first, then A or H.** This is a code PR: Codex review, CI green. Never quote ST-EH's `executed_looks` in PR text, because it holds a backtest dollar figure (`discovery_manifests/st_eh_supertrend_grid.json:21`).

### D15. Do obligations that live only in deleted docs still bind?

**State.** AGENTS.md:12-13 and README.md:16-17 say only that the docs are in git at `b7eaff7`. 5510ca9 says "Keep the docs that code or STATE reads". The 11-05 eval path, the runbook sections it amends, the T1/T2 reservations and the 11-03 rulings all live only in deleted text.

| Option | Unblocks | Risks | Reversibility |
|---|---|---|---|
| **A'. Retire obligations that exist only in deleted docs, except named survivors: the 11-05 eval path, the pilot runbook as amended by the 11-05 path (every section it does not supersede, which D3, D12 and the checklist rely on), the T1/T2 and CME reservations, the 11-03 rulings, the c1 Stage 2/3 rulings, and what kept files and code carry (frozen pre-registrations, the stop rule, lab/builder/README obligations, dated HOLDs in ops/instruments). Where deleted text conflicts with AGENTS.md or STATE, those govern. Preferably move the eval path's operative text into a kept file** | One answer for every later agent. Does not decide whether one GO covers several sessions (that is D12) | Retires unfired research falsifiers | High (git) |
| A as drafted (no precedence clause, eval path not named) | — | Could be read as retiring the eval path's safety conditions | High |
| B. Everything binds through git | Full discipline | No in-tree index, so silent misses | High |
| C. Item-by-item triage | Precise | Around 30 mostly moot items | High |
| D. Defer | — | Zombie citations keep growing | — |

**Recommendation: A'. The critique added the survivor list and the precedence clause.**

### D16. Data source (STATE open decision 2)

**Recommendation: ratify TV-only as Joshua's own ruling.** D8 was delegated (generation note :416-417). Corrections:
- Drop the "eval fills count as slip evidence" clause. Fills are account data that Codex and the repo cannot hold, and Aegis fills are not FX-fix fills.
- MNQFLOW wakes only on a historical MBP-10 source for its Databento S1 window. Any other vendor needs an amended pre-registration (`lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md:254-259`).
- TV export rights are unverified. The record treats TV as display-only for feeds (feed note :10, :56).
- Rule separately on the 27 unregistered 11-01 pages (MZC, MZS, MZW, MHG, SIL, MNG).

Alternatives: price a depth source at $0 (needs a non-Databento vendor and a new pre-registration); buy now (no consumer has a value case); defer (low cost).

### D17. Third-leg Experiment 1 GO

The frozen card (`b7eaff7:docs/briefs/handoffs/2026-10-29-orb-aegis-third-leg-exp1-baseline-readiness-card-DRAFT.md`) reads deleted files and scripts and would bounce at Step 2.1. Its "no 6J panel" premise was already wrong at drafting: a 6J1 page sat in SHA256SUMS at the card's base.

**Recommendation: defer to after the first sessions, and fix the plan :129 link.** If Joshua wants the R1-R3 readiness facts now, run it as a plain local inventory task ($0, K=0, no card) rather than a re-freeze. Note that a third leg falls outside the 11-05 second-instance exception (CK:1091).

### D18. Builder liveness ceiling, MGC, R1 validity

**State.**
- The 11-03 ruling says the builder owes a ceiling plus the contract fields (`b7eaff7:docs/adr/2026-08-30-candidate-contract.md:191-199`).
- The proposed per-instrument look budget fails the contract's "binding" and "not Confirm-only" tests (`b7eaff7:docs/methodology/strategy_harvest.md:83-87`). It resets with new instruments and can be enlarged by the 2009 calendar ruling (`ops/calendars/README.md:166`).
- MCL has already exhausted its instrument look budget. This does not depend on reading R1's results. The 11-05 addendum records eight banked cards, a D7 floor that cannot be reached, Joshua's "Park MCL", and that an invalid run would still count toward K (`b7eaff7:docs/briefs/pre-registration/2026-11-01-builder-r1-mcl-orb-registration.md:9`). `lab/builder/ledger.py:101-104` counts distinct ledgered cards without consulting results. Whether R1 is valid evidence is a separate, open question, and so is a channel-level ceiling that meets the contract (Codex review).
- MGC has eight ledgered cards and is "Not ruled" (`ops/instruments/MGC.md:107`).

**Recommendation: changed by the critique from "use the look budget".** Record in lab/builder/README.md that the channel is dormant. The next round's registration must declare a channel-level, audited ceiling and the owed contract fields before it freezes. Rule on these first:
- MGC's disposition (park as MCL was parked, or adjudicate the run);
- whether the R1 run is valid evidence;
- whether the 2009 calendar extends look budgets.

### D19. c1 Stage 3 residuals

**Recommendation:** the surface-ADR "own GO and quiet window" (`b7eaff7:docs/adr/2026-07-17-c1-rail-build-account-registration-go.md:506`) lapses. Removing LIVE_FLY_APPS and rail.deploy (`scripts/guard_operator_acts.py:74-76, :290`) needs normal Codex review and green CI. The Stage 3 conditions still apply unless Joshua supersedes them separately: `fly.toml`, `LIVE_FLY_APPS` and `rail.deploy` leave together in the last S3-2 PR, and each PR's executed consumer scan gives every outside consumer a disposition (`b7eaff7:docs/adr/2026-07-17-c1-rail-build-account-registration-go.md:506, :512`). Both `deploy/c1_rail/fly.toml` and `deploy/c1_signal_daemon/fly.toml` are still in the tree (Codex review). S3-4's destination comes back with the consumer table.

The volume archives (ADR :500) may hold runtime ports, `effective_inputs.json` or account identifiers. AGENTS.md forbids copying those anywhere. Joshua confirms the contents locally first, and agents do not copy them. If they contain Pine, runtime ports or `effective_inputs.json`, either he accepts the single copy, or he grants an explicit exception. If they hold account data only, the copy ban does not apply: AGENTS.md bars committing account identifiers and giving account data to Codex, not a private backup Joshua makes himself. Since these archives are the only copies found, on one machine, offer him a private backup for that case (Codex review).

### D20. Subscription reconfirm (11-21)

Keep the monthly cadence. If time allows, close the stale rows: the Tradeify carrying cost (d15), the Cursor cancellation date, final charges. Fix the ledger's links to deleted records. Nothing here blocks other work.

---

## Cross-decision interactions

**Constraints and conflicts.**
- **D15 comes before D14 and most cleanup.** The 2-C choice between A and H depends on it. It also decides whether the 11-05 path, itself a deleted text, governs the eval. It does not decide whether one weekly GO may cover several sessions: CK:1101 and AGENTS.md:17-25 are compatible, and that question is asked separately in D12.
- **D8 comes before D3 and D4.** A "sole owner and operator" attestation (route :398) is inconsistent with standing agent placement unless Joshua rules on it. Either a directed agent order counts as his act (surface ADR 09-30b, `b7eaff7:docs/adr/2026-07-14-cc-cursor-surface-allocation.md:896-900`), or placement narrows to B. The hybrid still needs the his-own-act ruling, because it keeps agent fills. Say also whether rule-1 directed agent acts on the eval stay authorized under the hybrid.
- **T2 vs the standing preservation GO.** There is no live conflict: the 11-05 reversal is in force. The conflict is between agent placement and the venue attestation.
- **D9 vs D3/D12.** Never place the preservation trade while an instance is enabled (CK:1094; runbook U-12). Choose its instrument so it cannot form an opposing Equity Index position. A genuine held trade placed by an agent needs the standing GO restated (AGENTS.md:21-23 covers only "the round trip").
- **D11 moots most of D2-A and D1-B.** If the framework does not gate the 100K, its gates are out of play for this attempt.
- **D1 and D2 must name O-0 consistently with the stop rule (:3) and with D3.**
- **D5 comes before D3's "values before S-PAIR".** The values cannot be fixed for a build nobody authorized. D5's authority list must include the 11-09 horizon-edition build, with no canary during armed sessions.
- **D6 and D7 are one thread.** The source request came on the CME data ticket and asks about export. A Tradeify reply may partly answer 11a.
- **The horizon edition touches D2, D3, D5 and D6.** Admission by 12-18 (v11 :19) changes the code on the eval. It needs the Addendum 1 path (stop rule), an edition-swap clause (binding), stated authority (build) and a re-send to Tradeify.
- **D4 vs research.** Broad exclusivity narrows R1 MCL, the 11-03 index ruling and any future different-instrument variants. Multi-firm is research-only, so the near-term cost is small.
- **Review routing.** These need a Codex-clean head and green CI, not a doc-only merge: AGENTS.md money-control edits (D8, D9), framework pointer or amendment (D2), register_search and test changes (D14), guard removal (D19), any core/firm_rules.py edit.
- **Codex never touches** the private NinjaScript, TV exports, strategy parameters or eval fill data (D5, D7, D14).

**Recommended ruling order at the sitting.**
1. D15: deleted-record status and precedence.
2. D8: T2 posture and the sole-operator question.
3. D11: the 11-05 path governs the 100K and the framework does not gate it.
4. D1 then D2: evidence acceptance, and nomination as O-0.
5. D5: build authority, enumerated.
6. D4: exclusivity.
7. D3: binding in principle, values before S-PAIR.
8. D6 and D7: risk acceptances and Joshua's sends.
9. D9 then D10: trade shape, then whether and where to ask.
10. D12: GO cadence and signed-page contents.
11. Research: D13, D14, D18 (MGC/R1 first), D16, D17, D19, D20.

---

## What must close before the first armed session GO

- [ ] D15 ruled: the 11-05 path confirmed in force from git history (or moved into a kept file), and AGENTS.md governs where texts conflict.
- [ ] D8 ruled: who may place and act on the eval, consistent with any sole-operator attestation.
- [ ] Row 1 (D1) ruled, including stop-rule drop, funded-stage and bust scope.
- [ ] Row 4 (D2) ruled: nomination = card hashes :421/:427, ORB leg = O-0. STATE.md:9 wording fixed.
- [ ] Row 7 (D5) recorded publicly before S-PAIR and the eval build. STATE.md:11-14 corrected. Joshua names the substitute review for the private eval build (Codex cannot see it), done before install.
- [ ] Row 6 (D4) signed publicly.
- [ ] S-PAIR bare rerun run and accepted, on the bound values (step 1; private, confirm locally).
- [ ] Step 3: name readback, eval build under its GO, installed disabled. The build matches the source sent to Tradeify, or is re-sent.
- [ ] Row 5 (D3): binding with build hashes, the per-leg split, every load-required config field, and the native DD policy confirmed by Joshua with its own admission or an explicit exception.
- [ ] Row 11 (D6): notice sent and deadline passed, or a reply received, for the source actually installed (a pre-session re-send restarts the window).
- [ ] Candidate-specific ownership/eligibility (native plan :57): answer received, or the prerequisite explicitly superseded with the risk named on the signed page.
- [ ] Row 11a (D7): CME follow-up sent, entitlement confirmed, export behaviour known, CME category accepted as risk with a pay-or-stop trigger.
- [ ] T1 (D9): placement rule on the signed page (never with an instance enabled).
- [ ] Step 4: signed page (contents per D12) hash-registered, and the attended pre-session check done (M1 replacement, CK:1089).
- [ ] Stop rule unchanged, or re-registered before session 1 (AGENTS rule 5).
- [ ] Step 5: Joshua's GO for the week (session 1 only if the review rule survives). He enables the strategy himself.

---

## Uncovered or adjacent items

- **Record drift.** STATE has no line for rows 11 or 11a, T1, T2, the 11-05 path or the source email. The skill file `.claude/skills/prop-firm-challenge/SKILL.md:72` points at a deleted AGENTS section. The native plan and builder README link to deleted files. All are doc-only fixes after the rulings.
- **The instrument_profiles check fails** after the cut (24 HARD findings reported by the critique; not re-run here). It is not a CI gate.
- **MNQ cash-open gap disposition** (#1106, 766568f): was the merge Joshua accepting "PARK execution, untested", or is a ruling owed?
- **Prop-envelope 90-day re-verify** (`ops/prop_envelope_default.md:81-83`): retire it now that multi-firm is research-only?
- **FXIFY Futures Flex provisional row** (`core/firm_rules.py:587, :676`) is orphaned. Removing it is a core edit and arguably a rule-4 surface.
- **Memory-store triage card** and the **Q-SFCLEAR-1 F6 upload**: both are likely overtaken by the cut and the lane closure, so withdraw them.
- **Generation-note decisions** D1, D3, D4, D5, the rest of D10, and the 5g cap: no recorded ruling.
- **ST-EH manifest hygiene.** A backtest dollar figure sits in a public manifest (`discovery_manifests/st_eh_supertrend_grid.json:21`). Redact it?
- **The MYM closing-location cell is withdrawn as an item.** It has been DEAD since 2026-08-30 (`ops/instruments/MYM.md:149`; `ops/instruments/profiles.json:161-165`, :1084).
- **T7 (undefined eval expiry)** bears on the deletion risk. Check the dashboard billing page.
- **Not verified here (private or mailbox):** card contents, S-PAIR status, the 10-25 and 10-31 rulings, whether caps are compiled into the source, whether any reply has arrived from Tradeify, CME or NinjaTrader, archive contents, and the ORB close timing against the 08-04 ratification (archive@8a78cdea).
