# 11-08 sitting decision packet

Open decisions for Joshua's 2026-11-08 sitting, with options and recommendations. **It decides nothing.** Private records appear only as "private record, confirm locally".

**Citations.** "CK" is `docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md` at `f96a657` (PR #1099), the last main with the doc corpus before 5510ca9 (#1100) deleted it; it is byte-identical to `b7eaff7` except line 1099. Other deleted docs are cited at `b7eaff7`.

**State of the record.**
1. **T2 is reversed.** `b7eaff7` CK:1099 said "T2 stands: no agent or Codex acts on the eval". #1096 (a31aabc, 11-05) replaced it; in force is `f96a657` CK:1099: "Agents may act on the eval on his direction, and under the standing GO for the weekly trade … T2 stays open: Joshua accepts that venue risk." AGENTS.md:17-23 matches. T1 has never been ruled.
2. **Only reconciliation rows 2, 3, 12 are accepted** (CK:1078); the table is "Proposed, not accepted" (CK:1034). The 11-05 bare-bones path replaced rows 8-10 and open items 6-7 (CK:1032). Rows 1, 4, 5, 6, 7, 11, 11a, 13 are open. Joshua may reject a row's framing outright.

---

## Decide first (preservation trade due the week of 11-09)

### D8. T2: who places the weekly trade and acts on the eval

**State.** Agents act on direction and under the standing GO; T2 is accepted risk (CK:1099; AGENTS.md:17-23). Venue texts: "personally own, control, verify, and operate" (FAQ 17069653); ESA §6.7(b) bans third-party management; KYT checks "own decisions" (`b7eaff7:…venue-deep-dive-DRAFT.md:14-19`); VPN/VPS login banned (register :214). The standing GO has never placed an order; Joshua placed both recent weeks (`b7eaff7:STATE.md:90-91`). Agents hold no broker credential, so agent placement needs his PC on, logged in, computer use enabled; nothing shows that is set up. **Conflict:** D3/D4 would have him attest "sole owner and operator" while AGENTS.md authorizes agent placement.

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| A. Keep 11-05 posture; write the reasoning the deep-dive asked for (:73-77) | No change | Agent fills are evidence against 17069653 and KYT; inconsistent with a sole-operator attestation unless a directed agent order is ruled his own act | Ruling yes, fills no |
| **Hybrid: Joshua places by default; an agent places only as late-week fallback (no fill by a set Thursday ET time), only on his authenticated PC, never VM/VPS** | Miss-week insurance; agent fills only in near-miss weeks | Some T2 exposure | High |
| B. Hand placement only until Tradeify answers; agents verify read-only | Lowest exposure | Overturns his 11-05 reversal, suspends directed agent action; miss-week risk, deletion "after an email warning" (register :202) | High |
| C. Local attended surfaces only | Drops remote-access reading | Leaves third-party-management reading | High |
| D. Revoke the standing GO | Clearest record | As B | New grant |

**Recommendation: hybrid.** Offer B if he wants zero agent fills before a written answer, saying plainly it overturns 11-05. The hybrid keeps agent fills, so it still needs the own-act ruling (Interactions). AGENTS.md edits touch money control 1: Codex-clean head, green CI; a revocation takes effect on his word, before any PR. Either way, put T1/T2 with status back into STATE "Open decisions" (their only home, CK:1103, was deleted).

### D9. T1: the shape of the weekly trade

**State.** Severity H, never ruled (`b7eaff7:…venue-fact-register-DRAFT.md:252`). 11-05 keeps "a real trade each week" (CK:1101) and reserves T1 to Joshua (CK:1103), so T1 is open. ESA §6.5: refrain from "flipping contracts just to register a 'trading day'"; current practice is a "market round trip" (`b7eaff7:STATE.md:88`). Once instances run, a manual fill on MNQ or 6J is a §6.8 incident for the instance owning that instrument (CK:1093); only a fill on an instrument neither leg owns, or another account, is unexplained and a stop (CK:1094; runbook U-12, :146). A manual position opposite ORB in the Equity Index group is prohibited hedging (`core/firm_rules.py:256-266`).

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| A. Keep the round trip | Cheapest | Most exposed §6.5 reading | Weekly |
| **B. Genuine minimal trade: normal entry, held well past 10 s, exited in RTH, minimum size, never with an Aegis/ORB instance enabled** | Removes the worst reading | Small P&L variance; an agent placing it with a resting stop exceeds the GO's "round trip" scope unless restated | Weekly |
| C. Strategy fills count once sessions run; B-shape trade only in no-fill weeks | No T1 in session weeks | Nothing for 11-09 | High |
| D. Ask Tradeify first, keep shape meanwhile | Possible safe harbour | Flags past round trips | Cannot unsend |
| Rule B as required shape (a new ruling, not a confirmation: CK:1103 left T1 open) | Settles shape | — | High |

**Recommendation: B from the week of 11-09, then C once sessions run.** Under the D8 hybrid the standing GO must be restated to cover bracket and exit, whoever places by default, because the fallback agent may place it. Hand-placement only goes with D8-B.

### D10. Ask Tradeify about T1/T2 (deep-dive Q4/Q5)?

Drafted (deep-dive :81-89), no record of sending. Agent placement was drafted as a question 10-13 and dropped 10-21 (CK:958; `b7eaff7:docs/notes/2026-10-21-tradeify-native-followup-questions-DRAFT.md:8`).

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| **A'. After D9-B, Joshua sends Q5 (and Q4 if he accepts the attention) on a separate compliance ticket or #148959547, asking for a human answer** | Only route to settling T1/T2 | A "no" reaches past practice and directed agent acts in sessions | Cannot unsend |
| B. Q5 only | No round-trip spotlight | Selective disclosure, against "Send now, disclose" | Cannot unsend |
| C. Fold into the source-review thread | One thread | CME Data Sales copied there (route :402) | Until sent |
| D. Don't ask | No attention | Never settled | High |

**Recommendation: A'.** Rely on no reply for 11-09→11-13.

---

## Questions for Joshua

(local) = answer from private records or mailbox; do not record publicly.

- **D1:** Cards 1c and 1: edge-evidence or build cards (local)? Are CK:1076's "ORB MNQ v7" and the stop rule's "ORB O-0" the same configuration (local)? If so, align STATE.md:9. After a drop, does the registered rule text keep the survivor (local)? An added condition needs a new registration. Funded stage covered, or eval only? Still hold the recorder-text "needs its own evidence case" (CK:1023, :1026)?
- **D2:** Horizon edition: fresh nomination, or covered by Addendum 1? Keep or retire the framework?
- **D3:** Does the 10-25 ruling settle the account (local)? Caps: source constants or instance properties (local)? Which runbook limits must the signed page set? Native DD on frozen constants? Native ORB long-only (local)? **Native DD policy: own admission, or explicit exception?**
- **D5:** The private 10-31 build ruling's date and words, or ratify earlier canaries as of 11-08? Which check substitutes for cross-review of the private eval build?
- **D6:** **Fixed calendar date ending the source-review wait? Which post-session-1 build changes need a fresh forward record, versus S-PAIR rerun and re-send? Wait for a candidate-specific ownership answer, or supersede it and name the risk?** Reply arrived (local)? Did the 11-05 email go on the CME-copied thread? Do the sent source or build write market data out of NinjaTrader?
- **D8:** **Under the hybrid, is a directed agent order your own act, and do rule-1 directed agent acts stay authorized?**
- **D9:** Restate the GO to cover bracket and exit (needed under the D8 hybrid), or hand-place only (with D8-B)?
- **D11:** **Spend ceiling: set in the owner record, or superseded?**
- **D12:** **Relax CK:1101 (one GO per session) so one weekly GO may cover more than one session?**
- **D14:** **ST-EH re-bank: change its promotion requirements, or historical exception?**
- **D18:** MGC: park or adjudicate? Is R1 valid evidence? Does the 2009 calendar extend look budgets?
- **D19:** Archive contents (local)?

---

## Eval-path decisions

### D1. Evidence case for the first forward attempt (row 1)

What evidence is enough to start ORB + Aegis on the owned Select 100K?

**State.**
- Row 1: CK:1040. Joshua's 11-03 ruling (effective 11-08) made the 10-19 finding an advisory prior; "the pair's own gates bind" (CK:1076). Rule 26 binds "each run's own pre-registered gates". The stop rule is "the committed registration that Rule 23 requires before the first forward session" (`docs/briefs/pre-registration/2026-10-31-tradeify-forward-stop-rule-registration.md:3`); the framework is a DRAFT that "decides nothing" (`docs/briefs/pre-registration/2026-10-26-tradeify-native-lane-prereg-DRAFT.md:3`). The record points at the stop rule as the pair's gate. STATE.md:15 still says "no configuration has an evidence case".
- **ORB identity gap.** T00 trial 13: "the author's model used the book's ORB O-N series; the native ORB build binds the unread solo O-0 configuration" (`discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json`). O-N evidence does not transfer to O-0. CK:1076 names "the ORB MNQ v7 + Aegis A-0 pair", and STATE.md:9 follows it; the stop rule names "ORB O-0" (registration :3). Whether these are one configuration is Joshua's call (private record, confirm locally).
- **Cards may not be edge evidence.** Hash-registered at `docs/evidence/PRIVATE_EVIDENCE.sha256:421` (Aegis 1c) and `:427` (ORB 1), beside freeze and adjudication files, suggesting build or port cards. Private record, confirm locally.

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| A. Cards plus stop rule are the evidence case | Closes row 1 | Only if cards state an evidence basis (doubtful) | Until session 1 |
| **E. No pre-session case; stop rule is the gate; gaps accepted as risk** | Closes row 1 regardless of card contents | Weak prior: 10-19 grid was exploratory, protection off, book ORB legs not O-0 | Until session 1; bust irreversible |
| B. Clear framework G0-G4 first | Statistical gate | Weeks-months: no §7 recipe, #940 open, dead citations; conflicts with data rules (D2) | Fully |
| C. A plus a pre-session descriptive backtest check | — | Not publicly re-runnable (TV exports private); fresh look at unread O-0 adds to K, spoils a clean framework route | Low |
| F. One leg only | No cross-leg risk | Each leg has a negative prior; cap split restated | Until session 1 |
| D. Defer | — | ORB's forward window shortens against its date gate (addendum-1 `:14`); no GO consumed | Fully |

**Downstream.** Whether a surviving leg continues after a drop comes from the registered rule text, which decides keep, drop or halt per strategy (registration :15; private record, confirm locally). An added continuation condition needs a new registration before session 1 (registration :17; AGENTS rule 5), not a line on the signed page. Funded 100K starts at 3 minis / 30 micros (`b7eaff7:docs/notes/2026-11-01-tradeify-venue-deep-dive-DRAFT.md:21`), so the split may not fit after a pass. A pass is not edge evidence (framework §5; native plan :94). A bust means reset/rebuy, a money-control-6 spend (prices: `lab/analysis/_inbox/prop_payout_geometry_2026-10/programs.py:10`).

**Recommendation: E.** Wording:

> "For the first forward attempt on the owned Select 100K, no pre-session statistical evidence case is required. The pair's own pre-registered gate is the 10-31 forward stop rule plus Addendum 1, unchanged. Accepted as risk on the signed page: the 10-19 prior, the exploratory composition-grid signal, the workshop finding that no out-of-sample edge is established, and that no O-N or model evidence transfers to O-0. A bust ends the attempt, and any reset is a fresh spend decision. This sets no precedent for scaling or new purchases."

### D2. Nomination and the framework (row 4)

**State.** Row 4: CK:1043; no nominating amendment. G0 item 3 superseded by the 11-03 ruling (effective 11-08), amendment owed (CK:1079). The framework keeps branch (d) parking language (:5, :93) and cites the deleted `docs/operational_rules.md`. §2 item 1 fixes parameters "in the nominating amendment" (:44); §10 re-runs gates "from the merged amendment and the public tooling" (:124). Both conflict with AGENTS.md data rules for locked strategies. A public ledger exists: T00 trial 13, quantities under a private hash.

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| **B/F. Framework does not gate this attempt. Nomination = the expressions in cards at PRIVATE_EVIDENCE.sha256:421/:427 (T00 trial 13; ORB leg as D1 settles it, O-0 per the stop rule). Horizon edition substitutes only via Addendum 1** | Closes row 4 on existing anchors | Framework stale without a pointer | Before session 1 |
| A. Ratify and nominate under it | — | Unworkable without breaching data rules (public parameters, Codex review of gate evidence); D1-B delays | Low |
| C. Amend, keep DRAFT | Removes contradictions | Effort on a maybe-unused draft | High |
| D. Retire to git | Matches the cut | Loses the only drafted scaling economics gate | High |

Deferring leaves the signed page unable to name the nomination.

**Recommendation: B/F.** Add a one-line "does not gate the owned-100K attempt" pointer to the framework status line, via Codex cross-review (gate document). Leave repair or retirement until a scaling or purchase decision needs a gate (D11).

### D3. Account binding (row 5)

**State.** Row 5: CK:1044. 11-05 replaced §2.1-2.2 with "a static per-leg split of caps. Values stay private" (CK:1091) and the P2 gate with the signed page (CK:1090). Loading still requires `day_loss_stop`, `unprotected_max`, `disconnect_max`, `outcome_window`, `fact_max_age`, `barrier_timeout`: "Loading rejects the configuration … if any field is unbound" (`b7eaff7:docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md:233-240`). A private 10-25 ruling may settle the account (`b7eaff7:docs/notes/2026-10-24-assumption-challenge-rulings-proposal.md:19`; private record, confirm locally). "The eval build uses S-PAIR's source set" (CK:1101), so compiled caps must be fixed before S-PAIR.

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| **A. Confirm (or rule) the owned 100K; fix private values before the S-PAIR rerun; sign full binding with build hashes on the signed page** | S-PAIR exercises live values; closes native plan D3 and framework §11 item 2 for release 1 | Value change after S-PAIR forces a rerun | Before session 1 |
| B. Sign binding now separately | Row 5 visibly closed | No hashes yet; signed twice | Before session 1 |
| C. Fresh Select 50K | Cheaper geometry | Spend approval; new stop-rule registration (names the 100K, :3); contradicts 11-05 (CK:1083) | Purchase irreversible |

Deferring leaves the signed page unable to be signed.

**Recommendation: A.** The binding also states: eval-only, new split at funded activation; an edition-swap clause tied to Addendum 1; "only Aegis and ORB" (R1 MCL or any third leg needs a new binding and registration); the preservation-trade placement rule (D9); and the native DD policy for this instance, confirmed by Joshua with its own admission or an explicit exception. Matching the frozen 1.5% / 0.40× literals is not an approved Tradeify policy: money control 4 freezes the `core/dd_protection.py` constants without approving them for a new firm-tier instance; the 07-13 ADR rejects transplanting FXIFY's pair (`b7eaff7:docs/adr/2026-07-13-dd-protection-concept-not-constant.md:27-31`); `core/dd_geometry.py:25-39, 87-101` requires each instance's own admission, no default. Python constants stay untouched. No "sole operator" attestation until D8.

### D4. Exclusivity (row 6)

**State.** Half (ii), ORB's §4 candidacy, is discharged by the 11-03 withdrawal (`b7eaff7:docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md:478-481`); the signature remains (CK:1045; framework G0 item 2, :45). Tradeify, 10-24: "allowed, as long as you are the sole owner and operator, and the strategy is not used at other prop firms" (`b7eaff7:…crosstrade-rest-route-assessment.md:398`). The 11-04 ruling "a different instrument counts as distinct" says "a contrary written answer reopens the ruling" (`b7eaff7:docs/notes/2026-11-01-generation-phase-strengthening-DRAFT.md:508`). T-1105 (Tradeify's AI agent) wrote that same logic on different instruments is the same strategy (`b7eaff7:docs/notes/2026-11-03-cross-firm-exclusivity-and-account-caps-DRAFT.md:121`). On plain text the reopen has triggered; only the outcome is unruled.

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| **E. Sign broad scope publicly (released implementations, editions, successors, same logic on any instrument); record 11-04 as reopened by T-1105, outcome pending a human answer; optionally ask the human Compliance Manager** | Row 6 closes; records consistent | For ORB/Aegis logic, overrides the 11-03 "index not Tradeify-only" ruling (generation note :498) and R1's distinctness basis (`b7eaff7:…builder-r1-mcl-one-card-reregistration-DRAFT.md:54`) | Easy to relax; a breach Tradeify finds is not |
| B. Narrow; keep 11-04 | Keeps variants open | Contrary to the only written answer; downside on the eval | — |
| C. Narrow plus interim bar plus question | — | Records contradict each other | High |
| F. Release-1 statement; park instrument question until multi-firm | Cheapest | T-1105 conflict open, named as risk | High |

Deferring keeps row 6 blocking for a free statement.

**Recommendation: E.** State the effect on the 11-04 FX 6J→MFFU mapping (generation note :525): a different-logic 6J strategy elsewhere is permitted but exposed to Tradeify's "similar orders" scan and ESA §6.7 (T3). Any question goes on a compliance ticket, not CME-copied thread #04738415.

### D5. Native build authority (row 7)

**State.** Branch (b) granted read-only stage 1: "no strategy code, build…" (CK:1018). Partial trace: v11 registration :15 cites "Joshua, 2026-10-31: 'GO route b'"; CK:1036 names a private 10-31 ruling releasing both strategies. 11-05 "changes frozen Rule 10 only as stated here, and no other rule" (CK:1083); whether it lifts branch (b) is contestable, so rule explicitly. STATE.md:11 still says read-only. The NinjaScript is an executable port and stays private (native plan :50), so Codex cannot do or review steps 1 and 3.

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| **A/B plus enumerated forward authority: confirm the private ruling's date and words (A) or ratify earlier canaries as of 11-08 (B). Authorized: S-PAIR rerun; eval build installed disabled on the trading host under the step-3 GO; horizon-edition v2 build and Sim101 canary from 11-09 (v11 :19). No canary in an armed session. Codex excluded from private source** | Steps 1, 3 consistent with the record | Joshua supplies or confirms wording | Revocable |
| C. Authority from 11-05; earlier canaries evidence only | Clean chain | Narrows what the page relies on | High |
| D. Defer / fold into signed page | — | Steps 1, 3 precede the page (step 4) | — |

**Recommendation: A if Joshua can name the ruling, else B, with the list.** He names the substitute check for the private eval build. Fix STATE.md:11-14 in the same PR.

### D6. Wait for Tradeify's reply to the 11-05 source email? (row 11)

**State.** Row 11: CK:1050; starting without a reply is Joshua's call (CK:1103). Tradeify's 10-26 source request came on the CME ticket thread with CME Data Sales copied, asking about "optional export functionality" (route :402); his 10-26 data-terms question is unanswered (:403); verification timing open (:408). Support is fast (2 minutes 10-12, route :376; 2 days 10-22/24; ~1 minute 11-05); only the compliance manager's follow-up is unanswered. Native plan :57 (written ownership answer for the candidate) is separate from source review: Tradeify's answer is general guidance and exact-candidate eligibility is open (`b7eaff7:docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md:401-407`). Neither a review deadline nor the exclusivity signature supplies it.

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| A. Wait indefinitely | Strongest | No end | Fully |
| **B'. Wait to a fixed calendar date Joshua picks (e.g. 11-19), independent of any GO; the first session GO follows its expiry (tying it to the GO is circular). He sends notice, not a request: "Unless you object by <date>, I will enable the strategy whose source I sent on <send date>; I will record the enable on video and keep logs." A pre-session re-send carries a fresh notice; session 1 waits for its deadline or a reply** | Dated; burden on Tradeify; no pre-approval gate | A requested code change after session 1 means S-PAIR rerun and re-send. That alone does not end the stop rule's record: registration :17 covers rule changes; Addendum 1 admits the horizon successor. Which other changes need a fresh forward record is Joshua's call | Until session 1 |
| C. Proceed now | Fastest | Little gained with rows open | Until session 1 |

Deferring risks a last-minute blocker.

**Recommendation: B'.** Also: re-ask the 10-26 question; rule that any eval-build change, horizon edition included, is re-sent by Joshua before it runs, with the notice naming the source actually sent; name on the signed page who flattens and disables on an objection (Joshua, or an agent under that week's GO); wait for the candidate-specific ownership answer or supersede it and name the risk on the page; Joshua prepares a plain-language strategy description for a KYT interview (deep-dive :17).

### D7. Data rights, CME licence, entitlement (row 11a)

**State.** Row 11a: CK:1051. CME asked for "confirmation on the feed" (feed note :358); Tradeify's Compliance Manager confirmed CQG on that thread (:359), so CME's precondition may now be met and the next step is Joshua's. The 10-10 note reads §7.3 as binding the distributor, "not a data subscriber", and an evaluation destination as "plausibly adds no" category (`b7eaff7:docs/notes/2026-10-10-cme-non-display-licensing-research.md:36-37`); both are inferences for the personal Tradovate lane's feed, not native use on Tradeify's data. Its 10-12 operator read is stricter: Subscriber Addendum §4.2, "All Non-Display Use of CME Licensed Information requires a direct license with CME", no exception; §6.1(j) needs a separate direct agreement; §7.3 "bears on prop-evaluation environments", and the absence of a real exchange order "is not stated as an exemption" (:115-143); open on ticket #04738415 (:145-149). Treat the category risk as contested.

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| A. Close everything first | Clean | Long stall | Fully |
| **C'. (1) Follow up on CME #04738415 citing the CQG confirmation; (2) re-ask NinjaTrader/CQG for distributor, agreement, Managed User route; (3) confirm locally the eval login's agreement and status; (4) entitlement: discharged if S-PAIR ran on the Tradeify-credentialed install, else a read-only check; (5) confirm whether the build exports data. CME category a named risk with a pay-or-stop trigger** | Session 1 not hostage; breakable item checked | Fee exposure on a contested reading | Before session 1 |
| B. Accept all as risk | — | Entitlement gap undetected | Before session 1 |
| D. Buy a direct licence now | Strictest covered | Recurring, maybe unneeded spend | Monthly |

**Recommendation: C'.** Feature lists derived from the private source stay in Joshua's checkout and never reach Codex or the repo. A licence purchase needs rule-6 approval.

### D11. Native plan scope, "fund the expanded assessment" (STATE open decision 1)

**State.** Everywhere, "expanded" means expanded P1: read-only toolchain plus Tradeify entitlement check, 1-2 sessions, $0 (plan :82, :100; CK:1018); the STATE wording (d603e81) is ambiguous. No P2-P7 GO; the plan assumes a Select 50K (:87). Plan D2(b) is moot (ORB v7 withdrawn as the §4 candidate); D4 is moot (personal lane closed); D3 is decided for the first account by 11-05 (CK:1083).

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| **B'. 11-05 governs the owned 100K; plan and framework do not gate it. Expanded P1 ruled overtaken (if S-PAIR ran on the Tradeify-licensed install) or granted alone ($0). Plan and framework annotated or retired. No fee budget** | Clean record; closes entitlement half of 11a | No ratified scaling gate | High |
| A. Grant P1-P5 first | Framework-grade evidence | 9-11+ weeks; contradicts 11-05; "sim fills optimistic" applies to the simulated eval too | High |
| C. B' plus framework ratification and §7 recipe | Scaling gate | Deleted rules, data-rule breach, Codex capacity (#940) | High |
| Light scale criterion, registered before session 1: reads 100K forward trades to decide a second account; never stops or resizes the pair | Gate without recipe | Must freeze before session 1 | High |

Deferring leaves STATE, row 7 and the plan contradicting each other.

**Recommendation: B'.** Add the light criterion only if 100K results should inform scaling. Record open scaling items: funded resize (30 micros vs the 80-micro eval cap); the Elite Live bar on other accounts, household included (deep-dive :26); the spend ceiling, which survives c1's retirement, re-homed by Joshua's 11-03 ruling (effective 11-08) to the retained Tradeify account's private owner record (`b7eaff7:docs/adr/2026-07-17-c1-rail-build-account-registration-go.md:517-521`). Per-spend approval (money control 6) is separate and does not replace it. Confirm it is set there or supersede it; D15's survivor list keeps it.

### D12. Sequencing, GO cadence, signed page (row 13 and the fold)

**State.** 11-05 path: step 2 done (CK:1097), step 1 private, steps 3-5 open (CK:1085). CK:1101, "every session needs its own GO", plainly means one GO per session, inside the AGENTS.md 7-day limit (:17-25). The question is whether Joshua wants to relax CK:1101 so one weekly GO covers more than one session; D15 does not settle it. The runbook's "One session, then a recorded review before another" (:127) survives 11-05. "Kept" is not a stop-rule lock event: it binds under AGENTS rule 5 and locks at session 1 (registration :17).

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| **A. Paper items first (order below), then operational steps. Rows 6, 7 public; rows 1, 4, 5 and risk acceptances on the private hash-registered signed page with a public headings-only list. Separate build and session GOs; first session GO covers session 1 only if the review rule survives** | Each step has its authority | — | Until session 1 |
| One weekly GO for build and session 1, conditioned on S-PAIR acceptance and the page | Fewer acts | If CK:1101 is relaxed, could cover session 2 before review | High |
| B. Also wait for Tradeify and CME | No external unknowns | Open-ended | High |

Deferring the ordering leaves the signed page with no defined content.

**Recommendation: A.** The signed page lists: binding (D3), evidence acceptance (D1), nomination (D2); exclusivity restated (D4); what S-PAIR showed; the CK:1103 acceptances (no reply, CME licence, T1, T2); candidate-specific ownership/eligibility (native plan :57), answered or superseded with risk accepted; unproved native-control risks accepted (protection across a disconnect on the firm connection, other U tests Sim cannot prove; automatic incident close not relied on, CK:1090); the attending operator's duties (account-wide incidents, stopping new risk across both legs, account loss stop, under this page and the stop rule, no cross-instance automation, CK:1095); row 11a residuals; who enables (step 5 "he enables himself"; Tradeify may want video); preservation-trade placement rule; review-before-session-2 rule; stop trigger on a Tradeify objection; what the step-3 "name readback" is (undefined publicly).

---

## Research decisions

### D13. Mechanism clause 2-A falsifier

**NOT FIRED.** Trigger: the first three compliant campaigns die at Stage-2 or Stage-6 (`b7eaff7:docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md:86`). The compliant cards (MSL-S4 parked, `ops/instruments/MGC.md:92-97`; F1, `docs/rejected_candidates.md:1340-1349`, four-clause status not fully verified) both stopped before Stage-2. Its owner ADR and target text (harvest Requirement 1a) are deleted; no Path-1a campaign is active.

| Option | Reversibility |
|---|---|
| A. Not fired, carry to 2027-02-08 (nothing tracks that date) | High |
| **B. Not fired, retire as unreachable. Precedent: Joshua's 11-03 decompound ruling, verbatim only "Retire with legacy book." (c43d4b7); the rationale (an impossible check adds no evidence when its subject has no live venue) is the recorder's. Grounds here differ: no compliant campaign exists** | High (git) |
| C. Defer | High |

**Recommendation: B,** recorded in the sitting PR description.

### D14. Mechanism clause 2-C falsifier (executed-K closures)

**State.** Trigger: an examined read missing from a closure note; consequence: revert ALL executed-K closures to declared K (ADR 07-26 :88). The ORB manifest reads executed_looks "none" (`discovery_manifests/orb_mnq_intraday_breakout.json:23`) though campaign RESULTS exist (`lab/analysis/orb/orb_mnq_2026-07/RESULTS.md:5`); the 2a89d3e guard would refuse the close (`lab/discovery/register_search.py:900-904`). The manifest's stated aim: "close as operator-stopped with executed_k=0 so K arithmetic is unchanged", "Banks 0 to keep K_banked(MNQ)=2" (:22-23). Tool misuse versus outcome-targeted K selection is unestablished; present both, assert neither. Both TXG1 closures also name no examiner, but their K does not move.

Effects: family banks are disclosure-only; builder and T00 ledgers unaffected; at K=1 the ORB manifest becomes valid promotion backing (`lab/discovery/k_ledger_check.py:56-60`); the native-lane disclosure counts the July look regardless (v7 S4 draft :64). **ST-EH promotion requirements change:** `lab/discovery/promotion_packet.py:205-225` requires an extra DSR-floor attestation when `floor_at_k(K)` of the backing manifest exceeds CAP (1.0); the floor is 0.85 at K=2 and 1.615 at K=84, so re-banking ST-EH 2→84 adds it to every packet ST-EH backs. Ask: change, or historical exception?

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| **A (deleted rules bind). FIRED, enacted: ORB 0→1, ST-EH 2→84; fix all four manifest verdicts and MNQ.md:88; owner re-sums MNQ/MYM (derived 64 / 47, unreconciled); register_search operator-stopped closes bank declared K (keep the path, or stopped campaigns have no close); update the three affected test files; decide promotion backing** | Honours the falsifier | Conservative ST-EH disclosure | Effectively one-way |
| **H (they don't). FIRED as history only; ORB to K=1 for accuracy; ST-EH stays 2 only after its enumeration is audited; same register_search change** | Accuracy, no precedent | — | High |
| F. A, then a forward-only executed-K rule on the 2a89d3e guards | Keeps the ADR's case against always banking declared K | One more rule | High |
| B. Not fired (08-18 covers it) | No edits | 08-18 adjudicated the bank, not the enumeration | High |
| C. Retire unruled | Minimal | Looks like dodging a FIRED reading | — |
| D (as drafted). ORB only | — | **Do not offer:** claims an ST-EH audit that never ran (2-C check :97-98) | — |

**Recommendation: D15 first, then A or H.** Code PR: Codex review, CI green. Never quote ST-EH's `executed_looks` in PR text: it holds a backtest dollar figure (`discovery_manifests/st_eh_supertrend_grid.json:21`).

### D15. Do deleted-doc obligations still bind?

**State.** AGENTS.md:12-13 and README.md:16-17 only say the docs are in git at `b7eaff7`; 5510ca9: "Keep the docs that code or STATE reads". The 11-05 path, the runbook sections it amends, the T1/T2 reservations and the 11-03 rulings exist only in deleted text.

| Option | Effect | Risks | Reversibility |
|---|---|---|---|
| **A'. Retire deleted-only obligations except named survivors: the 11-05 eval path; the pilot runbook as amended by 11-05 (all sections not superseded, relied on by D3, D12, the checklist); T1/T2 and CME reservations; 11-03 rulings; c1 Stage 2/3 rulings; what kept files and code carry (frozen pre-registrations, stop rule, lab/builder/README obligations, dated HOLDs in ops/instruments). AGENTS.md and STATE govern on conflict. Preferably move the eval path's operative text into a kept file** | One answer for later agents; leaves the multi-session GO question to D12 | Retires unfired research falsifiers | High (git) |
| A as drafted (no precedence clause, eval path unnamed) | — | Readable as retiring eval-path safety conditions | High |
| B. Everything binds via git | Full discipline | No index; silent misses | High |
| C. Item-by-item | Precise | ~30 mostly moot items | High |

Deferring lets zombie citations grow.

**Recommendation: A'.**

### D16. Data source (STATE open decision 2)

**Recommendation: ratify TV-only as Joshua's own ruling** (D8 was delegated, generation note :416-417), with corrections: drop "eval fills count as slip evidence" (account data Codex and the repo cannot hold; Aegis fills are not FX-fix fills); MNQFLOW wakes only on a historical MBP-10 source for its Databento S1 window, other vendors need an amended pre-registration (`lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md:254-259`); TV export rights are unverified and the record treats TV as display-only (feed note :10, :56); rule separately on the 27 unregistered 11-01 pages (MZC, MZS, MZW, MHG, SIL, MNG). Alternatives: a $0 depth source (non-Databento, new pre-registration); buy now (no value case); defer (cheap).

### D17. Third-leg Experiment 1 GO

The frozen card (`b7eaff7:docs/briefs/handoffs/2026-10-29-orb-aegis-third-leg-exp1-baseline-readiness-card-DRAFT.md`) reads deleted files and scripts and would bounce at Step 2.1; its "no 6J panel" premise was wrong at drafting (a 6J1 page was in SHA256SUMS at its base). **Recommendation: defer until after the first sessions; fix the plan :129 link.** For R1-R3 readiness now, run a plain local inventory ($0, K=0, no card). A third leg falls outside the 11-05 second-instance exception (CK:1091).

### D18. Builder liveness ceiling, MGC, R1 validity

**State.** The 11-03 ruling: the builder owes a ceiling plus contract fields (`b7eaff7:docs/adr/2026-08-30-candidate-contract.md:191-199`). A per-instrument look budget fails the contract's "binding" and "not Confirm-only" tests (`b7eaff7:docs/methodology/strategy_harvest.md:83-87`): it resets with new instruments and the 2009 calendar ruling can enlarge it (`ops/calendars/README.md:166`). MCL's budget is already exhausted, independent of R1's results: the 11-05 addendum records eight banked cards, an unreachable D7 floor, Joshua's "Park MCL", and that an invalid run still counts toward K (`b7eaff7:docs/briefs/pre-registration/2026-11-01-builder-r1-mcl-orb-registration.md:9`); `lab/builder/ledger.py:101-104` counts distinct ledgered cards without consulting results. R1 validity and a contract-compliant channel-level ceiling are separate open questions. MGC has eight ledgered cards, "Not ruled" (`ops/instruments/MGC.md:107`).

**Recommendation: do not use the look budget.** Record the channel dormant in lab/builder/README.md; the next registration declares a channel-level audited ceiling and the owed contract fields before freezing. Rule first on MGC (park, or adjudicate), R1 validity, and the 2009 calendar.

### D19. c1 Stage 3 residuals

**Recommendation:** the surface-ADR "own GO and quiet window" (`b7eaff7:docs/adr/2026-07-17-c1-rail-build-account-registration-go.md:506`) lapses; removing LIVE_FLY_APPS and rail.deploy (`scripts/guard_operator_acts.py:74-76, :290`) needs normal Codex review and green CI. Unless Joshua supersedes them, the Stage 3 conditions hold: `fly.toml`, `LIVE_FLY_APPS` and `rail.deploy` leave together in the last S3-2 PR, and each PR's executed consumer scan gives every outside consumer a disposition (ADR :506, :512). Both `deploy/c1_rail/fly.toml` and `deploy/c1_signal_daemon/fly.toml` still exist. S3-4's destination returns with the consumer table.

The volume archives (ADR :500) may hold runtime ports, `effective_inputs.json` or account identifiers. Joshua confirms contents locally; agents do not copy them. With Pine, runtime ports or `effective_inputs.json`, he accepts the single copy or grants an explicit exception. With account data only, the copy ban does not apply (AGENTS.md bars committing identifiers and giving account data to Codex, not his own private backup); as these are the only copies found, on one machine, offer him a private backup.

### D20. Subscription reconfirm (11-21)

Keep the monthly cadence. If time allows, close stale rows (Tradeify carrying cost d15, Cursor cancellation date, final charges) and fix links to deleted records. Blocks nothing.

---

## Cross-decision interactions

- **D15 before D14 and cleanup:** decides 2-C A vs H, and whether the 11-05 path (deleted text) governs. Not the multi-session GO question (D12).
- **D8 before D3/D4.** A "sole owner and operator" attestation (route :398) conflicts with agent placement unless a directed agent order is ruled his act (surface ADR 09-30b, `b7eaff7:docs/adr/2026-07-14-cc-cursor-surface-allocation.md:896-900`) or placement narrows to B. The hybrid keeps agent fills, so it still needs that ruling, plus a statement on whether rule-1 directed agent acts on the eval stay authorized.
- **T2 vs standing GO:** no live conflict (11-05 reversal in force); the conflict is agent placement vs the venue attestation.
- **D9 vs D3/D12:** never trade with an instance enabled (CK:1094; runbook U-12); pick an instrument that cannot oppose ORB in Equity Index; an agent-placed held trade needs the GO restated (AGENTS.md:21-23 covers only "the round trip").
- **D11 moots most of D2-A and D1-B.**
- **D1 and D2 must name O-0** consistently with the stop rule (:3) and with D3.
- **D5 before D3's "values before S-PAIR":** no values for an unauthorized build; D5 lists the 11-09 horizon build, no canary in armed sessions.
- **D6 and D7 are one thread:** the source request sits on the CME ticket and asks about export. A Tradeify reply may partly answer 11a.
- **Horizon edition (D2, D3, D5, D6):** admission by 12-18 (v11 :19) needs the Addendum 1 path, edition-swap clause, stated authority, and a re-send with fresh notice.
- **D4 vs research:** broad exclusivity narrows R1 MCL, the 11-03 index ruling and different-instrument variants; small near-term cost (multi-firm is research-only).
- **Not doc-only (Codex-clean head, green CI):** AGENTS.md money-control edits (D8, D9), framework pointer or amendment (D2), register_search and tests (D14), guard removal (D19), any core/firm_rules.py edit.
- **Codex never touches** private NinjaScript, TV exports, strategy parameters or eval fills (D5, D7, D14).

**Ruling order** (D9 comes before D3, whose binding carries the placement rule; D9 can be ruled alone if time runs short):
1. D15 status and precedence. 2. D8 T2 and sole operator. 3. D9 trade shape and placement. 4. D11 11-05 governs, framework does not gate. 5. D1 then D2 (O-0). 6. D5 enumerated authority. 7. D4. 8. D3 in principle, values before S-PAIR. 9. D6, D7 acceptances and sends. 10. D10. 11. D12. 12. Research: D13, D14, D18 (MGC/R1 first), D16, D17, D19, D20.

---

## Before the first armed session GO

- [ ] D15: 11-05 path confirmed in force from git (or moved to a kept file); AGENTS.md and STATE govern on conflict.
- [ ] D8: who may place and act, consistent with any sole-operator attestation.
- [ ] Row 1 (D1), including funded-stage and bust scope; survivor handling per the registered rule.
- [ ] Row 4 (D2): nomination = card hashes :421/:427, ORB leg named per D1 (O-0 per the stop rule); STATE.md:9 aligned.
- [ ] Row 7 (D5) public before S-PAIR and the eval build; STATE.md:11-14 corrected; Joshua names the substitute review for the private eval build (Codex cannot see it), done before install.
- [ ] Row 6 (D4) signed publicly.
- [ ] S-PAIR bare rerun accepted on the bound values (step 1; private, confirm locally).
- [ ] Step 3: name readback; eval build under its GO, installed disabled; matches the source sent to Tradeify, or re-sent.
- [ ] Row 5 (D3): binding with build hashes, per-leg split, every load-required field, native DD policy confirmed by Joshua with its own admission or an explicit exception.
- [ ] Row 11 (D6): notice sent and deadline passed, or reply received, for the source actually installed; the notice names it, and a pre-session re-send needs a fresh notice and restarts the window.
- [ ] Candidate-specific ownership/eligibility (plan :57): answered, or explicitly superseded with the risk on the signed page.
- [ ] Row 11a (D7): CME follow-up sent, entitlement confirmed, export behaviour known, category accepted with pay-or-stop trigger.
- [ ] T1 (D9): placement rule on the page (never with an instance enabled).
- [ ] Step 4: signed page (per D12) hash-registered; attended pre-session check (M1 replacement, CK:1089).
- [ ] Stop rule unchanged, or re-registered before session 1 (AGENTS rule 5).
- [ ] Step 5: Joshua's weekly GO (session 1 only if the review rule survives); he enables the strategy himself.

---

## Uncovered or adjacent items

- **Record drift:** STATE lacks rows 11/11a, T1, T2, the 11-05 path, the source email; `.claude/skills/prop-firm-challenge/SKILL.md:72` points at a deleted AGENTS section; the native plan and builder README link deleted files. Doc-only, after rulings.
- **instrument_profiles check fails** after the cut (24 HARD findings reported; not re-run here). Not a CI gate.
- **MNQ cash-open gap** (#1106, 766568f): did the merge accept "PARK execution, untested", or is a ruling owed?
- **Prop-envelope 90-day re-verify** (`ops/prop_envelope_default.md:81-83`): retire now multi-firm is research-only?
- **FXIFY Futures Flex provisional row** (`core/firm_rules.py:587, :676`) is orphaned; removal is a core edit, arguably rule-4.
- **Memory-store triage card, Q-SFCLEAR-1 F6 upload:** likely overtaken; withdraw.
- **Generation-note decisions** D1, D3, D4, D5, rest of D10, the 5g cap: no recorded ruling.
- **ST-EH manifest hygiene:** a backtest dollar figure sits in `discovery_manifests/st_eh_supertrend_grid.json:21`. Redact?
- **MYM closing-location cell withdrawn:** DEAD since 2026-08-30 (`ops/instruments/MYM.md:149`; `ops/instruments/profiles.json:161-165`, :1084).
- **T7 (undefined eval expiry)** bears on deletion risk; check the dashboard billing page.
- **Not verified here (private or mailbox):** card contents, S-PAIR status, the 10-25 and 10-31 rulings, whether caps are compiled, replies from Tradeify, CME or NinjaTrader, archive contents, ORB close timing against the 08-04 ratification (archive@8a78cdea).
