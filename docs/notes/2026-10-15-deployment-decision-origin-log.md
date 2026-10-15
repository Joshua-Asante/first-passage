# Deployment decisions by judgment origin — first batch (2026-10-15)

Derived snapshot of public records at `main` `4121e84`, recorded at Joshua's direction. The linked owner records govern. This note decides nothing and changes no trading criteria, deployment permissions or ownership. It separates what agents recommended from what Joshua supplied. The portfolio's economic performance is a separate question, which this note does not address.

**Scope:** a bounded first batch of consequential Tradeify-book and personal-lane deployment choices, 2026-09-03 to 2026-10-14, plus two history rows (A3h, E2h). It is not a complete history. **Evidence:** tracked files, git history, and PR bodies and comments in this repository. No private inputs, conversations or billing were read; quotes are ones already committed in public records. **Method:** for each category, one agent extracted entries and an independent agent re-opened every cited source to refute them. A critic then checked consistency and coverage. The coordinating session merged duplicates and applied the rules below, and fidelity-checked agents condensed the entries. A3h was added at reconciliation and did not go through the extract-and-verify pass.

## Classes

| Class | Meaning | Test applied |
|---|---|---|
| 1 | Agent-recommended, operator-approved | The agent recommendation, or a choice an agent made under delegation, is in a committed file or posted comment dated before or with the ruling. Alternatively, the ruling's own words name a recommendation that can be located. |
| 2 | Operator-modified or overridden | Joshua changed, narrowed, extended or rejected a located recommendation, including corrections folded into an agent draft. |
| 3 | Operator-originated | Positive evidence: his words supply a value or choice that no committed agent text offered, he reports an act already taken, or the record states that no recommendation was made. Confidence is moderate where the chat is not public. |
| 4 | Unknown | Anything else. **probable 1**: his recorded words ("all recommended", "1 yes, 2 yes") accept a sheet that was never committed, so the recommendation survives only as an agent's restatement after the ruling. **leans 3**: operator origin is likely but not shown. |

- **Origin is not authority.** Joshua's approval is the authorization in every class.
- **No entry has an operator-authored artifact.** Agents commit as "Joshua Asante"/"Josh Asante" and post from the `Joshua-Asante` account; comments titled "Operator approval" are signed by coordinators (#629 comment 5965049542). "Joshua's words" therefore means a short quote recorded by an agent. "Agent report" means an agent asserts a ruling without quoting him.
- **Not a rate.** This is a sample, and no class counts or approval rates are derived from it.

## What the batch shows

1. **Class 1 can be logged reliably only where a committed packet carries the recommendation.** Examples: live-wiring J-1 to J-4 (H3a), the run-path packet (F4, G2d), G0/G4 (B5a, B5b), the 09-22 checklist amendment (F1a, F1b, C3a), T08 §7.7 (D2), the B–D packet (D3a, D3b), the feed binding packet (C4a), the D-MON lean (G5a), the p99 test (B2b), the T00 precision packet (G4b) and the Q-SFCLEAR-3 defaults (G6b–G6d).
2. **Class 2 is recovered only by diffing draft commits.** Joshua's changes are folded into agent drafts as "corrections" or appear as one-line rejections: A3h, A4a, A5c, B4a, D1b, D4e, E3b, E3c, G1b, G4c, H3b, H4b.
3. **Class 3 concerns preferences, acts and attestations:** the 15% drawdown tolerance (B2a), the D20 acceleration (H6a), the Databento cancellation (C1), reopening the self-funded lane (H2a), the maximum-growth objective (A4b), an attestation about private ports (A1b), D-B11 picked with no default given (B1b), and the July closure (E2h).
4. **Class 4 has two main sources.**
   - **Probable 1:** short replies to sheets that were never committed: sittings 1 and 2, decision sheet A–E, the 2026-10-12 route decision plan, and the 2026-10-13 cloud status review behind the Track B suspension (H1).
   - **Options without a recommendation record:** options presented with no record of whether one was recommended, e.g. A1a, A2a, A5a, A5b, A6b, B3c, E1, G6a.
5. **Record defects, to correct at their owners (Rule 14):**
   - S2b ADR `:442` gives a ruling time (~01:50Z) later than the commit that wrote it (`d27c7a1`, 01:08Z).
   - STATE `:45` files sheet E under sitting 1, while #649 calls it sitting 2.
   - The Aegis no-re-pin prereg skeleton cites a "§59 Ruling 8" that does not exist.
   - A2b's conditions are credited to the "executive review", which the seat chart makes Codex Astra, while incident ADR `:274` calls it the operator's.

## Superseded and amended chains

- **Aegis takeover:** A3h (09-15, kept) → A3a (10-02, first release without it).
- **Personal-lane pool:** A5a (option (c) split) → A5b (reuse the Tradeify book).
- **Feed:**
  - Stage 1 input (09-11): C2b (option A, conditional) → C2a (option D).
  - Production feed (09-11): C2c (A′ selected) → C2d (deferred, same day).
  - D-feed: C3a (09-22) → C3b/C3c (10-02).
- **T00 order:** F2a → F2b, the same day.
- **T00 depth:** G4a (1,000) → G4b (5,001) → G4c (1,002).
- **Four-firm §4:** B4a (09-03) → B4b (10-02) → H4a (10-06, FALSIFIED).
- **Build gate:** H3a → H3b.
- **Personal study:** G2c (Q-SFCLEAR-2 frozen) → G6a → G6d (Q-SFCLEAR-3 frozen).
- **Order expressions:** A1b → A2a.
- **X-1 option:** D4d → D4e.
- **Owner-file order:** F3a → F3b.
- **Self-funded lane:** E2h → H2a.
- **D20:** H6a → orchestrator narrowing (outside the classes, below) → the 09-05 S2 plan revision (not in this batch).

## Entries

Fields: recommendation (Rec.), operator response (Resp.), reason for the class (Why), resulting action (Result), uncertainty (Unc.) and sources. Paths are repo-relative; line numbers refer to `4121e84`.

Short names used in the entries:

| Short name | Path |
|---|---|
| `campaign` | [`docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md`](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md) |
| `lane ADR` | [`docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md`](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) |
| `T00 card` | [`docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md`](../briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md) |
| `B–D packet` | [`docs/notes/2026-09-26-tradeify-bd-decision-packet.md`](2026-09-26-tradeify-bd-decision-packet.md) |
| `checklist` | [`docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md`](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) |
| `live-wiring packet` | [`docs/notes/2026-10-11-live-wiring-decision-packet.md`](2026-10-11-live-wiring-decision-packet.md) |
| `S2b ADR` | [`docs/adr/2026-08-08-s2b-signal-daemon-build.md`](../adr/2026-08-08-s2b-signal-daemon-build.md) |
| `slices ledger` | [`docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`](../superpowers/plans/2026-09-18-full-e1-execution-slices.md) |
| `X-1 packet` | [`docs/notes/2026-09-29-x1-decision-packet.md`](2026-09-29-x1-decision-packet.md) |
| `incident ADR` | [`docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md`](../adr/2026-09-17-bounded-platform-protection-incident-contract.md) |
| `amendment` | [`docs/superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md`](../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md) |
| `binding packet` | [`docs/notes/2026-10-02-feed-spec-open-parameter-binding-packet.md`](2026-10-02-feed-spec-open-parameter-binding-packet.md) |

### A — Portfolio expression

**A1a** · 2026-09-25 · **class 4** — Requalify route-native expressions for ORB MNQ (fixed-stop OSO bracket) and Striker MYM (entry carrying stop) as one K=1 prereg, not reject route.
- Rec.: None located. Incident ADR §A4 (`incident ADR:228`, d95a72ad, before ruling) framed requalify-or-reject as an operator decision, recommending neither.
- Resp.: "go with the easier fix" (`campaign:3926`), recorded by a Claude session in b0d8de9b.
- Why: Agent framing gave both options without recommending; the in-session option list Joshua answered is unrecorded, so neither origin is established.
- Result: §59 Ruling 3; D-B4(a) amended; route-native prereg drafted (431258a6); ledger CANDIDATE rows; PR #497 merged 2026-09-25.
- Unc.: Adopted designs match the agent's §A4 examples, so design content was agent-drafted; 'easier fix' implies an in-session comparison was presented.
- Sources: campaign:3926-3956; incident ADR:228-230; commit b0d8de9b (PR #497)

**A1b** · 2026-09-25 · **class 3** — Vanguard MGC and Aegis 6J fit the narrowed request shape on Joshua's attestation, keeping their declared expressions.
- Rec.: None. Agent asked yes/no; record says no agent had read the private ports (`campaign:3914`); prior agent map rated both 'Undetermined' (d95a72ad).
- Resp.: "yes and yes" (fixed stop in same order; one-contract expressibility), agent-recorded at `campaign:3920`.
- Why: Positive evidence: no agent had read the private ports and the prior agent map said Undetermined; input is Joshua's own attestation.
- Result: §A4 per-leg table corrected 2026-09-25; agent read later found Vanguard TRAILING ACTIVE, accepted by Gate A A6 (bbaec94/#514).
- Unc.: Attestation of fact, not an option choice; 'keep declared expressions' was agent-drawn; agent evidence later showed the Vanguard half wrong.
- Sources: campaign:3914-3920; incident ADR:225-230; docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md:323,361

**A2a** · 2026-09-26 · **class 4** — Vanguard MGC takes a route-native fixed-stop edition (K=1, requalified through production E1), not rejection or deferral.
- Rec.: None located. Agent pre-drafted option A's prereg, framing options A and B without recommending (668650de, PR #506, before ruling 7fe28917).
- Resp.: Chose "Fixed-stop edition" from (A), (B) and deferral; agent-recorded at `campaign:3960`.
- Why: Agent framed options and pre-built option A without recommending either; no positive evidence of operator origin.
- Result: §59 Ruling 4; ledger CANDIDATE row vanguard_mgc_fixed_stop_oso; production gated at gate D; PR #515 merged 2026-09-26.
- Unc.: Pre-drafting only A may signal an unrecorded agent lean; whether the 2026-09-26 executive review recommended A is unrecorded, and its author contested.
- Sources: campaign:3958-3970; docs/briefs/pre-registration/2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md:3-9; commit 7fe28917 (PR #515)

**A2b** · 2026-09-26 · **class 4** — Vanguard conditions: full remaining-exits account; no alternative-expression search, automatic three-leg fallback or unchanged-economics claim; production behind gate D; A6 check at freeze.
- Rec.: Attributed to 'the 2026-09-26 executive review' (`campaign:3964`), first appearing with the ruling in 7fe28917; review text uncommitted; Astra per seat chart, operator per incident ADR :274.
- Resp.: Agent report: conditions 'adopted with the ruling' (`campaign:3964`).
- Why: Conditions' author unestablished: 'executive review' means Astra in the seat chart, but same-day records credit the operator; no review copy exists.
- Result: Conditions bind the Vanguard prereg and production handoff; commit 7fe28917; PR #515 merged 2026-09-26.
- Unc.: Class 1 if the review is Astra's text, class 3 if Joshua's own; only the agent recording asserts presentation and adoption.
- Sources: campaign:3964-3968; incident ADR:274,291,582-583; commit 7fe28917 (PR #515)

**A2c** · 2026-09-26 · **class 1** — Ruling 5 (preparation): ORB/Vanguard keep fixed stop, specified exits; Striker signal-bar stop; whole-intent sequential splits; no subset widening; failed modify returns.
- Rec.: Astra's recommended overall ruling (`B–D packet:7`), plus coordinator B-D packet decision 8 (:360), committed e2784aa3/e997eb20 before ruling af81e549; Astra text uncommitted.
- Resp.: Agent report: Joshua approved Astra's recommended overall ruling; structured answer "Adopt conditionally" (`B–D packet:13`).
- Why: Governing text is Astra's recommended ruling, approved by Joshua; narrowing from the coordinator packet (noop verification, no-retry dropped) came from agent text.
- Result: Dated markers on ORB/Striker and Vanguard prereg rows; commits af81e549, 5d939206; PRs #515 and #518.
- Unc.: Astra's ruling text exists only as recorded; whether 'Adopt conditionally' was marked recommended is unrecorded.
- Sources: B–D packet:7,13,360; campaign:3972-3985; commits e2784aa3, af81e549

**A2d** · 2026-09-26 · **class 1** — ORB base-entry lifecycle L1: one placement, no age-based expiry or periodic reissue, earlier cutoff kept; amendments returned for acceptance before freeze.
- Rec.: Codex Astra's recommendation, embedded as the selected option's text (`campaign:3989`); presented with the ruling, recorded d42c4679 (PR #519).
- Resp.: "L1 as Astra recommends", agent-recorded at `campaign:3989`.
- Why: The option label names the agent recommendation; Joshua selected it unchanged.
- Result: §59 Ruling 6; re-adopted by Ruling 7; integrated L1 change accepted 2026-10-02 sitting 2 (PR #605).
- Unc.: Astra's full recommendation text is not committed separately; Ruling 7 re-adopted L1 without the Ruling 6 record in view.
- Sources: campaign:3987-4009; docs/notes/2026-09-26-orb-lifecycle-evidence.md:3-5; commit d42c4679 (PR #519)

**A3h** · 2026-09-15 · **class 2** — Exclude replacing the shared 80-micro cap and Aegis takeover with static per-leg caps; whole-leg takeover in D-B8 priority order stays.
- Rec.: Claude Code architecture-review proposal packet, drafted at Joshua's instruction (`docs/notes/2026-09-15-tradeify-simplification-review.md`), same review; excluded proposal's wording not preserved.
- Resp.: "Aegis takeover is a key part of this book's edge." (review §1), recorded verbatim by the drafting agent.
- Why: Joshua rejected an agent-raised simplification (static per-leg caps) with his own stated reason.
- Result: Static per-leg allocations barred from re-proposal for this book; replay keeps modelling takeover (TB-S2 RC-5).
- Unc.: Added at reconciliation from a critic finding, not run through extract/verify; excluded proposal's wording not preserved; first release amended by A3a.
- Sources: docs/notes/2026-09-15-tradeify-simplification-review.md:79-85

**A3a** · 2026-10-02 · **class 4 (probable 1)** — First release runs without the Aegis takeover (fail-closed default), replacing B-11's 'Keep as declared' for that release.
- Rec.: Deployment coordinator's uncommitted sitting-1 sheet, answered 'all recommended'; closest committed text: C-a register R-1 PROPOSED fail-closed default (17d08bd3, before ruling).
- Resp.: "all recommended; yes to carry rule and term 8" (PR #610 body), agent-recorded; Codex relay cites 'directly observed approval'.
- Why: Item recommendation only in uncommitted sheet; committed text was PROPOSED, B-11 recommended opposite; reverses Joshua's A3h exclusion for first release.
- Result: GC-5 addendum (`B–D packet:131`); C-a R-1 discharged (550bc74f, PR #593); PR #610 merged.
- Unc.: B-11's change of recommendation is unrecorded; sitting-2 refuse-never-clip addition also answered 'all recommended' on a privately held sheet.
- Sources: B–D packet:131,133,209; commit 17d08bd3 (docs/notes/2026-09-26-close-semantics-c-a.md:470); commit 497b937a (PR #610)

**A3b** · 2026-10-02 (F-5 itself 2026-09-28) · execution route · **class 4** — The 2026-09-28 F-5 answer ('automation fenced, then reconciled') discharges C-a row S-X2; X-3/X-4 fills count toward weekly preservation trade.
- Rec.: None located for S-X2. Coordinator's GC-7 PROPOSED addendum (3747a178, hours earlier) said F-5 does not settle S-X2, proposing no option; sitting-1 sheet private.
- Resp.: "all recommended" (`B–D packet:135`; PR #610 body), agent-recorded.
- Why: Reply implies a sheet recommendation, but the only located agent text said F-5 does not settle S-X2 and proposed nothing.
- Result: GC-7 addendum (`bd-decision-packet.md:135`); S-X2 discharged in C-a register (550bc74f, PR #593); PR #610 merged.
- Unc.: Class 1 if the sitting-1 sheet item can be cited; F-5 alone reads class 1, agent-proposed and 'adopted as written' 2026-09-28.
- Sources: B–D packet:135; docs/notes/2026-09-27-route-commissioning-session-packet.md:65,70,89; commit 3747a178

**A4a** · 2026-10-09 · **class 2** — Personal-lane portfolio is not yet selected and does not default to the Tradeify book; selection owed against the lane's clearance standard.
- Rec.: Claude session's first ADR draft (7cbc87c4, 03:01Z, PR #743) bound the lane to the accepted four-strategy book; corrected 03:58Z in the same PR.
- Resp.: Agent report: commit 87d12a0b records 'Operator correction 2026-10-09: the personal account does not default to the Tradeify book'.
- Why: Joshua changed the agent draft's binding of the lane to the Tradeify book into an unselected portfolio.
- Result: ADR Decision 2 rewritten; owed item 5 conditional; Q-SFGROWTH-1 Pre-Q frozen; PR #743 merged 2026-10-09.
- Unc.: Unrecorded whether the draft's book was agent proposal or misrecording of Joshua's first instruction; if the latter, not agent judgment.
- Sources: lane ADR:3,16-18; commit 7cbc87c4; commit 87d12a0b (PR #743)

**A4b** · 2026-10-09 · risk criteria · **class 3** — Personal lane's objective is maximum account growth, the selection criterion within the 15% bound.
- Rec.: None located. First draft (7cbc87c4) states no objective; no 'maximum growth' text in repo history before 2026-10-09T04:00Z.
- Resp.: Agent report: commit 87d12a0b, under 'Operator correction', says 'portfolio selection is owed against a maximum-growth objective'.
- Why: Positive evidence: an operator correction added an objective absent from the agent draft and all earlier repo text, in an operator-executive-decision ADR.
- Result: ADR Decision 2 (`lane ADR:16-17`); Q-SFGROWTH-1 median-growth ranking rule (PR #743).
- Unc.: No Joshua verbatim words; earlier chat could have raised growth without repo trace, so class 3 is moderate confidence.
- Sources: lane ADR:3,16-17; commit 87d12a0b; commit 7cbc87c4

**A5a** · 2026-10-10 (ADR mislabels 2026-10-11 UTC) · **class 4** — Option (c): split strategies between lanes; Tradeify book's four strategies stay Tradeify-only, personal lane draws from other locked strategies.
- Rec.: None located. '(c)' implies Deployment Coordinator options (a)/(b), unrecorded; nearest agent text, exclusive-use note inference (`docs/notes/2026-10-10-tradeify-exclusive-use-replies.md:48`, 3ae919ee, before ruling), did not recommend (c).
- Resp.: "go with (c), split the strategies between lanes" (ADR :103), agent-recorded.
- Why: Option set and any recommendation unrecorded; agent inference supplied the premise (shared strategy presumed breach) but did not recommend (c).
- Result: ADR addendum 2026-10-11; Q-SFGROWTH-1 F8 lane-split HOLD (df67941e); PR #778 merged 2026-10-11.
- Unc.: Chat option set absent from repo and PRs; ADR's date label contradicted by d9292094 (2026-10-10T23:25Z); superseded by A5b.
- Sources: lane ADR:101-109; docs/notes/2026-10-10-tradeify-exclusive-use-replies.md:48; commit d9292094 (PR #778)

**A5b** · 2026-10-11 UTC · **class 4** — Reuse the Tradeify book's four strategies on personal lane sized for E_0; finish personal controls; strategy search off critical path; supersede (c).
- Rec.: None located in repo, commits d9292094..0c22ad90, or PRs #778/#784/#785/#752; the agent drafted the addendum after the ruling (0c22ad90).
- Resp.: "reuse the Tradeify strategies, qualify their sizing for the personal capital, and finish the personal-account operating controls" (ADR :113), agent-recorded.
- Why: Same-day reversal of (c); no recommendation or record of none; either Joshua's own or an accepted coordinator option (also reported as F6a).
- Result: ADR addendum 2026-10-11b (PR #784); Q-SFCLEAR-2 frozen 2026-10-12 (83867f0); clearance plan PR #785.
- Unc.: Reversal reason unrecorded; it followed a same-evening HOLD on the post-split pool (b02c173e).
- Sources: lane ADR:111-133; commit 0c22ad90 (PR #784); commit b02c173e

**A5c** · 2026-10-11 · **class 2** — Personal sizing starts from retained successor configuration (FLOOR-HALF); legs it sets OFF stay OFF; changes need explicit justified operator choice; no ladder.
- Rec.: Deployment Coordinator plan draft recommended D3 ladder M = {C3, C2} (5714da78, PR #785), committed before corrections were folded in 5034deb9/b1ea7afe.
- Resp.: Agent report: correction 3, 'Start from the retained successor configuration; justify any change' (plan :30).
- Why: Joshua rejected the recommended two-rung ladder {C3, C2} and chose the plan's non-recommended option A (FLOOR-HALF).
- Result: ADR :118; clearance plan §3.1 (:84); commits 5034deb9, b1ea7afe; PRs #784 and #785.
- Unc.: Joshua's exact words for correction 3 are not quoted; later Q-SFCLEAR sizing rulings were not audited and may amend this.
- Sources: docs/notes/2026-10-11-personal-clearance-plan-tradeify-book.md:24-30,84,425; lane ADR:115-118; commit 5714da78 (PR #785)

**A6a** · 2026-10-10 · **class 1** — Successor configuration relies on Tier-2 pattern row 5 only, read as a uniform cross-leg size cut; row 3 not relied on.
- Rec.: Deployment Coordinator: T00 card §8 'rely on row 5 only' (91c3c519) and readiness map Q4 'Treat row 5 as uniform' (8075b43f), both before ruling 086ef910.
- Resp.: "C-1 row 5 uniform, option A, K₀ = 8" (card :567), agent-recorded.
- Why: Both 'row 5 only' and 'uniform' match agent recommendations committed before the ruling, which adopts them unchanged.
- Result: #733 C-1 answered; successor build card updated (7b215060); PR #760 merged 2026-10-10.
- Unc.: Card recommendation committed 8 minutes before the ruling record; in-chat order is inferred from commit sequence.
- Sources: T00 card:563,566-567; docs/notes/2026-10-10-successor-screen-readiness-map.md:69; commit 086ef910 (PR #760)

**A6b** · 2026-10-10 · **class 4** — Successor whole-contract vector is Q1 option A, FLOOR-HALF: every leg at k = 0.5, rounded down, legs flooring to zero OFF.
- Rec.: Partial: Deployment Coordinator readiness map Q1 (8075b43f, before ruling) recommended halving scalable legs, leaving keep-or-drop open; the Q1 options sheet framing A is private.
- Resp.: "C-1 row 5 uniform, option A, K₀ = 8" (card :567), agent-recorded.
- Why: Option A is within the agent's recommended family, but keep-or-drop was left open and the private options sheet cannot be checked.
- Result: Vector frozen for the successor screen (size_vector 139919cd…), run 2026-10-11 (PR #760).
- Unc.: Option A's first position may reflect ordering, not recommendation; K₀ = 8 from the same ruling matches readiness map :77 (class 1).
- Sources: T00 card:564-567; docs/notes/2026-10-10-successor-screen-readiness-map.md:66,77; commit 086ef910 (PR #760)

### B — Risk criteria

**B1a** · 2026-09-10 · **class 4** — Tradeify book protection: combined 1% running-peak DD trigger; while protected, Aegis/Vanguard/Striker MYM at 40% and ORB adds off; ORB base one micro.
- Rec.: None located in the selection note, campaign state, umbrella or PR #329. A Codex weighting study's report (about 05:22, before selection) is lost; any recommendation is not public.
- Resp.: Agent report: the note says "The operator selected the 1% combined drawdown trigger..."; Joshua's verbatim "Yes you may." only authorizes publication.
- Why: No agent recommendation located and no positive evidence Joshua introduced the cell; Codex ran the study Joshua framed, proposer unrecorded.
- Result: PR #329 merged 2026-09-10, closing STATE item 1; frozen by D-B11; coded in `ops/c1_rail/book_policy.py:101-117`.
- Unc.: Private study artifacts and the selecting conversation are not public; the admission ADR's 'Joshua (selection...)' attributes authority, not judgment origin.
- Sources: docs/notes/2026-09-10-tradeify-protection-selection.md:3; docs/notes/2026-09-10-tradeify-protection-selection.md:60; PR #329

**B1b** · 2026-09-11 02:20 UTC · **class 3** — D-B11 = route (b): admit the accepted policy via instance-specific superseding ADR, no trigger-by-scale grid, rather than route (a)'s grid.
- Rec.: Umbrella rev 7 (ee80bb7, Claude co-authored, 02:07Z) D-B11 row: 'No shortcut default... State which.', standing since rev 3 (00:39Z), before the 02:20Z ruling; Codex review neutral.
- Resp.: Agent report: PR #336 comment (02:20Z, Joshua-Asante account, no agent footer): "D-B11 = (b), instance-specific superseding ADR..."
- Why: Positive evidence: packet withheld a default, Codex framed both neutrally; Joshua chose between agent-framed routes, picking (b). (also reported as H7c)
- Result: Rev 9 (303ddbb) removed the grid branch; recorded at campaign §55; TB-P2 instance-admission ADR, first ratified 2026-09-14.
- Unc.: Authorship of the 02:20 post is unestablished; same-style thread posts are agent-produced; if advisor-drafted, a private recommendation cannot be excluded.
- Sources: PR #336 comment 5628479176; ee80bb7: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md:80; campaign:3852

**B2a** · 2026-10-09 · **class 3** — Personal-lane capital clearance threshold: maximum 15% peak-to-trough drawdown.
- Rec.: None located for the value: 87d12a0 (03:58Z, two minutes before the recording commit) posed drawdown or risk of ruin with no value or lean.
- Resp.: Joshua, agent-recorded at ADR :29-30: "I'd accept a 15% drop"; 'measured peak to trough' is the agent's specification.
- Why: Positive evidence: committed agent framing had no number; 15% is Joshua's own words. Reconciled 4→3, moderate confidence. (also reported as H2b)
- Result: Commit 8a5e42c (PR #743, merged 2026-10-09T04:47Z) rewrote Decision 4 and STATE rows; gates owed items 1 and 7.
- Unc.: The eliciting chat is unrecorded, so a presented option containing 15% cannot be excluded; the drawdown metric was Joshua's pick among agent-framed alternatives.
- Sources: lane ADR:29-30; commit 87d12a0; commit 8a5e42c

**B2b** · 2026-10-09 · **class 1** — 15% standard: clear if intraday-honest simulated p99 peak-to-trough DD ≤15% after costs/rounding, highest median growth wins; live 15% halt-and-flatten, resume needs GO.
- Rec.: Claude session, commit 8a5e42c (04:00:19Z), ADR Decision 4: 'Proposed reading ... pending operator confirmation', 82 seconds before confirmation commit f63a19c.
- Resp.: Joshua, agent-recorded at ADR :31-32: "99 in 100, confirmed".
- Why: Agent proposal located verbatim, committed before confirmation, accepted without change. (also reported as H2c)
- Result: f63a19c (PR #743); c208bde added halt as owed item 7; Q-SFGROWTH-1 used it; successor Q-SFCLEAR-2 frozen 2026-10-12.
- Unc.: Quoted words address p99; coverage of the live halt and median-growth rule is agent report; order rests on commit order, not chat timestamps.
- Sources: lane ADR:31-38; commit 8a5e42c; commit f63a19c

**B3a** · 2026-10-02 (reply 2026-10-03T01:42Z) · **class 4** — #581 OD-1 = reading (c): UNDETERMINED-dependent NO-GO-evidence verdict meets D-feed (a) after Joshua's dated F1 risk acceptance; robust NO-GO needs amending (a).
- Rec.: None located for (c): #581 §4 adopted no reading; the sitting-2 sheet is uncommitted. Spec §12's 'Recommend: confirm both' only asked confirmation of the relayed ruling.
- Resp.: Agent-recorded at prereg :220: Joshua, "all recommended" (2026-10-03T01:42Z); coordinator (3), in #629, recorded his direct confirmation of OD-1 = (c).
- Why: 'All recommended' implies a recommendation, but the sheet's OD-1 row is not public and no agent restates it; origin of (c) unshown.
- Result: Recorded at D-feed row (amendment PROPOSAL :151) and CP-7; #581 merged as DRAFT 2026-10-03, ratified 2026-10-07.
- Unc.: Sitting-2 and sheet-4 replies may be one or two messages; sitting-2 reached coordinator (3) by relay.
- Sources: docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md:190-194; docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md:218-220; docs/superpowers/specs/2026-10-02-t00-screen-authority-design.md:713-714

**B3b** · 2026-10-10 · **class 1** — Successor-screen OD-1: reading (c) extends to FLOOR-HALF; UNDETERMINED-dependent NO-GO needs separate dated F1 acceptance; robust NO-GO needs amendment; INSUFFICIENT does not qualify.
- Rec.: Codex assessment chat (non-public) gave four recommendations adopted as decisions 1-4 (successor prereg :9, :267), presented in the chat the ruling answered.
- Resp.: Joshua, directly to the Deployment Coordinator, agent-recorded at D-feed row :153: "Agreed on all four recommendations".
- Why: Record names recommender (Codex) and item (decision 4 = OD-1); Joshua's verbatim words accept all four unchanged.
- Result: D-feed row addendum :153, CP-7 :512, successor prereg §4 OD-1 :202; applied in B3c 2026-10-11.
- Unc.: Codex text is non-public; the ruled wording passed via Joshua to the coordinator and assembly worker, so fidelity is uncheckable; (c)'s origin unknown (B3a).
- Sources: docs/briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md:9; amendment:153; checklist:512

**B3c** · 2026-10-11 (~23:45Z; confirmed 2026-10-12T00:12Z) · **class 4** — Accept FLOOR-HALF successor screen's UNDETERMINED-dependent NO-GO-evidence risk into T15's F1 (option 1), meeting D-feed (a) for FLOOR-HALF only, notwithstanding #733 §4 H.
- Rec.: None located: T00 card :577 quotes option 1 'as presented' with no recommendation marker; option text first committed after the ruling (7f71015). Any chat lean is not public.
- Resp.: Joshua, agent-recorded (T00 card :577, :579): "...go with option 1"; then "confirm A" on the §4 H tension.
- Why: Record says only that option 1 was presented; post-ruling 'confirm A' corrected the agent's presentation, not a recommendation. (also reported as A6c)
- Result: PR #792 merged 2026-10-12T00:46Z; mirrored at D-feed row :155, CP-7 :512, T15 F1 and `STATE.md:43`.
- Unc.: Full option list and any chat lean are not public; Track B's 2026-10-13 suspension froze CP-7 feed funding, so unexercised.
- Sources: T00 card:576-580; PR #792; STATE.md:43

**B4a** · 2026-09-03 · **class 2** — D5: re-admit candidate #1 at the 5.0% ceiling and restore the four-firm §4 discharge on EOD-clock figures, waiving the superseding-ADR requirement.
- Rec.: Claude Code (Opus 5) Proposed addendum, be8c284 (2026-09-03T04:18Z), hours before the 21:27Z ruling: '...5.0% ceiling is prospective-only and does not re-admit candidate #1'.
- Resp.: Joshua, agent-recorded at ADR :177-179: "I am allowing Candidate 1 to be readmitted. No need for the superceding ADR..."
- Why: Joshua chose the option the agent argued against (re-admission) and waived the superseding-ADR requirement the agent's proposal attached to it.
- Result: PR #291 (7a7d01c) ratified the addendum 'Accepted in the OPPOSITE disposition'; §4 and §5 overridden but unedited.
- Unc.: Joshua's interim 'the 5% is the rule' (20:48Z) arguably previewed the choice but followed the proposal; ruling time is from the commit.
- Sources: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md:177-181; docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md:298-304; commit be8c284

**B4b** · 2026-10-02 local · **class 1** — Withdraw 2026-09-03 EOD-clock §4 discharge; gating clears need intraday-honest clock and dated pre-registered re-MC by 2026-11-08; exactly-one-tier clear: no discharge, Joshua decides.
- Rec.: Coordinator (3) decision sheet item B (uncommitted, restated post-ruling at ADR :354); pre-ruling #616 draft 4b4e0a8 (00:28Z) proposed intraday-honest mandatory for gating reads.
- Resp.: Joshua, replying to the coordinator's sheet, agent-recorded at ADR :354: "all recommended".
- Why: Owner record identifies adopted content as the coordinator's recommendation; Joshua adopted the sheet as given; committed core-clock proposal predates ruling.
- Result: PR #620 merged 2026-10-03T04:40Z; folded into #616; dated re-MC (#715) returned FALSIFIED (early-fail), §4 undischarged.
- Unc.: Sheet text known only from post-ruling restatement; item 4 (exactly-one-tier reserved to Joshua) absent from pre-ruling #616 text; reply time unsettled.
- Sources: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md:352-376; PR #620; commit 4b4e0a8

**B5a** · 2026-10-12 · **class 1** — G0-2: personal live trading keeps all four first-release evidence-class calendar denials, not dropping UNCERTAIN_ADJACENT and MISSING_SOURCE.
- Rec.: Deployment Coordinator's worker, decisions note :44-47 'Recommendation: (a).', drafted in 95eaa09 (17:38 -0400) before the 483fbca ruling (18:04).
- Resp.: Joshua, directly to the Deployment Coordinator, agent-recorded at note :3: "G0/G4 as recommended".
- Why: Recommendation in the same packet the ruling answers, committed before it, accepted unchanged.
- Result: PR #809 merged 2026-10-12T22:17Z; G0 card frozen (483fbca).
- Unc.: Joshua's reply was a blanket acceptance of all G0/G4 items.
- Sources: docs/notes/2026-10-12-personal-live-g0-g4-decisions.md:3; docs/notes/2026-10-12-personal-live-g0-g4-decisions.md:44-47; commit 483fbca

**B5b** · 2026-10-12 · **class 1** — G4-4: roll-window entry/add refusal and G4 flatten sit in `book_account_owner.py` (trust domain T), folded into P4 under G-1b; daemon-side rejected.
- Rec.: Deployment Coordinator's worker, note :94 'Recommendation: (a), folded into P4 under G-1b', revised from (b) in 7942765 (17:50) before the 18:04 ruling.
- Resp.: Joshua, agent-recorded at note :3: "G0/G4 as recommended"; the code admission (G-1b) is a separate act, not given.
- Why: Revised recommendation committed before the ruling and accepted as given.
- Result: PR #809 merged; G4 card frozen; owner edit awaits G-1b and the P4 queue slot.
- Unc.: Recommendation changed during agent review (7942765) but before the ruling; the 15% halt wiring is not decided here.
- Sources: docs/notes/2026-10-12-personal-live-g0-g4-decisions.md:3; docs/notes/2026-10-12-personal-live-g0-g4-decisions.md:89-94; commit 7942765

### C — Feed and licensing

**C1** · 2026-09-10 · **class 3** — Retire Databento for research acquisition and the proposed daemon feed; subscription cancelled, no replacement approved.
- Rec.: None located. Last agent disposition was KEEP (`docs/pursuits/d12-databento-subscription.md:16`, 2026-08-09); 509b5247 pinned Databento about an hour before the retirement record.
- Resp.: Agent report: Codex records "Joshua reported that Databento has been retired ... and the subscription has been cancelled" (`databento-research-stack.md:266`).
- Why: Positive evidence: Joshua had already cancelled, reversing live agent work (KEEP standing, same-day Databento build); no retirement packet exists.
- Result: Commit 2cb980d8, PR #334 (merge 343bbd05): ADR addendum, skill blocks pulls, d12 to SUBTRACT; adapter retired PR #332.
- Unc.: Chat is private, so an off-repo agent cost suggestion cannot be ruled out; class 3 rests on circumstantial evidence.
- Sources: docs/adr/2026-07-10-databento-research-stack.md:264-270; git 2cb980d8; 509b5247; PR #334

**C2a** · 2026-09-11 · **class 1** — Stage 1 (M1 item 5) input is option D: operator-attended controlled input, bar transcribed from the Tradovate chart; Q1-Q4 adopted.
- Rec.: Claude A1 packet: "Recommended: option D" (`S2b ADR:348`), committed PROPOSED in df48c58a 06:53Z, before ruling 40ab7c0d 08:02Z.
- Resp.: "i choose option d"; Q1–Q5 "adopt all, dated 2026-09-11"; recorded by the parent Claude session (A1r).
- Why: Committed packet recommendation (D) preceded the ruling and the operator selected D. (also reported as H7e)
- Result: 40ab7c0d, PR #340 (merge 186cb73b): S2b §2 row revised, M1 addendum; M1 RESOLVED 2026-09-14.
- Unc.: Packet was agent-framed from operator direction; quoted words lack timestamp or channel; D followed the conditional option A ruling, which returned BLOCKED.
- Sources: S2b ADR:145,:348,:421-:422; git df48c58a, 40ab7c0d; PR #340

**C2b** · 2026-09-11 · **class 4** — Conditionally select option A (Tradovate market data via the Tradeify eval account) as Stage 1 input; no silent fallback or self-selection.
- Rec.: None located. A1 brief (8de8a9d2, handoff `:55`) seeds A among options, no lean; Track A plan has none; packet's only recommendation (D) came later.
- Resp.: Agent report: unsigned PR #335 comment from the shared account: "Ruled: the daemon's Stage 1 input source is Option A ..."
- Why: No recommendation for A located; sibling #336 comment records 'sensible defaults' under operator instruction, so agent default or Joshua's pick.
- Result: Packet ran: A ineligible, BLOCKED, no fallback; superseded by D (C2a). PR #335 merged 777ba495.
- Unc.: Ruling chat is private: a session 'sensible default' makes it agent-originated with blanket approval; Joshua naming A makes it class 3.
- Sources: PR #335 comment 5629047842; PR #336 comment 5629047943; S2b ADR:185-:191,:352

**C2c** · 2026-09-11 · **class 1** — Production feed for the four adapters (O-4/Q5) is option A′, a personal live Tradovate account for data only; Databento re-subscription declined.
- Rec.: Claude A1 packet df48c58a (06:53Z) graded A′ "the production-feed route", B "not recommended" (`S2b ADR:201-:202`), before the 18:45Z ruling.
- Resp.: Agent report: "Recorded from the operator's chat ruling" (S2b ADR `:408`); no operator words quoted.
- Why: Operator chose A′, the packet's graded production-feed route, over unrecommended B; the packet anticipated 'if the operator wants a machine feed now'.
- Result: Marked APPLIED on PR #343 branch (32912f18); umbrella O-4 RULED (2780ae41); reversed same day by C2d before merge.
- Unc.: Switch from morning 'later' to 'now' followed the agent-opened O-4 (3c439f73); whether 'now' was agent-suggested is unrecorded.
- Sources: S2b ADR:201-:202,:350,:408; git df48c58a, 32912f18, 3c439f73

**C2d** · 2026-09-11 · **class 1** — Defer O-4: no feed provider selected or funded; A′ demoted to shortlisted; only provider-neutral A9-PREP runs until source-independent gates clear.
- Rec.: Codex advisory review, PR #344 (29f67bbe 20:11Z, a991831e 20:12Z): "NO-GO on funding today; demote A′ ... to SHORTLISTED"; precedes 8f99b41d (20:50Z).
- Resp.: Agent report: "Joshua (deferral) · Codex (recorder)" (S2b ADR `:406`); umbrella: "DEFERRED by the operator 2026-09-11"; no operator words quoted.
- Why: Every ruling element appears in Codex's PR #344 before the deferral record; it departs from Claude's fold keeping A′ selected.
- Result: 8f99b41d (PR #342) and 33d1682c (PR #343): A′ NOT APPLIED, A9 became A9-PREP; PR #344 closed unmerged.
- Unc.: Ordering rests on commit times; #344 body may reflect a deferral Joshua already gave; its vendor-timing shift may be relayed operator instruction.
- Sources: PR #344 (commits 29f67bbe, a991831e); S2b ADR:406-:407; git 8f99b41d, 33d1682c

**C3a** · 2026-09-22 · **class 1** — Tick D-feed as a gate, not provider: provider work opens after qualifying T00 verdict and T10 phase-2 F1 packet; A′ shortlisted.
- Rec.: Claude proposal "D-feed — TICK AS A GATE, not a provider" (`amendment:141-:145`), commit 59683cc7 00:50Z, before ratification 118cd47f 04:25Z.
- Resp.: "Adopt all five as recommended." Operator, 2026-09-22, in session; recorded verbatim by an agent (`:97`, `:147`).
- Why: Committed recommendation adopted unchanged.
- Result: §4 D-feed box ticked, §5 corrected; PR #454 (merge f36af72f).
- Unc.: Agent-framed from operator direction: grounds cite the operator's own 2026-09-11 deferral rule.
- Sources: amendment:97,:141-:149; git 59683cc7, 118cd47f; PR #454

**C3b** · 2026-10-02 · **class 4 (probable 1)** — Re-rule D-feed condition (b): CP-7 may open after T00 GO-evidence, a bound equivalence spec and A9-PREP; provider-neutral preparation authorized now.
- Rec.: Coordinator (3)'s in-chat sitting-1 sheet, uncommitted; known only from post-ruling restatement (PR #610 comment). Earlier CP-7 proposal a5dd0241 kept CP-7 after T10.
- Resp.: "all recommended; yes to carry rule and term 8" (PR #610 body), given directly to the deployment coordinator; agent-recorded.
- Why: Leans 1: Joshua adopted 'all recommended', a second agent's re-read matches; but sheet uncommitted and entry elaborates beyond the grant.
- Result: Commit 497b937a, PR #610 (merged 2026-10-02T23:36Z): checklist §4 CP-7 row; mirrors swept in #620.
- Unc.: Committing coordinator (3)'s sitting-1 sheet would settle class 1 versus 2; CP-7 funding frozen since 2026-10-13.
- Sources: checklist:512; PR #610 comment 5962322698; git 497b937a, a5dd0241

**C3c** · 2026-10-02 local (before 2026-10-03T01:08Z) · **class 4 (probable 1)** — CP-7 re-rule supersedes the S2b §2 Live CME bar source row's (`:48`) wait for CP-7's grant scope only; trading use keeps its gates.
- Rec.: Coordinator (3)'s decision sheet item C, given in chat and uncommitted; known only from recorder's post-ruling restatement (S2b ADR `:442`) and PR #620 body.
- Resp.: "all recommended" — Joshua, directly in coordinator (3)'s chat, 2026-10-02 local; agent-recorded (S2b ADR `:442`, PR #620 body).
- Why: Leans 1: Joshua adopted the sheet, but recommendation known only post-ruling and the record's timestamp conflicts with its commit.
- Result: S2b ADR Addendum 2026-10-02 (`:440-:444`), checklist `:512`; commit d27c7a19, PR #620 merged 2026-10-03.
- Unc.: Committing sheet C would settle class 1 versus 2; the `:442` ruling time (after its 01:08Z commit) needs correcting where read.
- Sources: S2b ADR:440-:444; PR #620; git d27c7a19

**C4a** · 2026-10-03 to 2026-10-04 · **class 1** — Bind the frozen CME feed-equivalence spec's OPEN parameters to the binding packet's recommended values, plus the OPEN-8 per-leg scoring amendment.
- Rec.: Coordinator (4)'s binding packet 'Recommended value' column (`binding packet:32-:44`), committed 6fd25a61 before rulings; OPEN-8 fix: Codex review on #666 (08:23Z), before 08:34Z ruling.
- Resp.: "bind Group 1 as recommended"; "open-3/4 as recommended"; "yes, fold as corrected" — to coordinator (4), agent-recorded (spec §16.4 `:366-:378`).
- Why: Each bound value is the packet's committed recommendation or a public Codex fix, adopted as recommended/stated/corrected; no parameter ruled differently.
- Result: PR #661 (merge 9dc5df30) and PR #666 (merge c95a40b1), 2026-10-04; spec §16.4 binding log and digest chain.
- Unc.: "As stated" OPEN-8/OPEN-10 wording was put to Joshua in chat; row text is the recorder's account. OPEN-2 evidence came from a private panel read.
- Sources: binding packet:32-:44; docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md:362-:378; PR #666 review r4176749691

**C4a2** · 2026-10-03T22:52Z; MGC 2026-10-04T00:17Z · **class 4 (probable 1)** — Bind OPEN-11 per-leg values: MNQ N=3, MYM N=3, 6J N=1 business days before last trading day; MGC uses first-notice-day rule, October skipped.
- Rec.: Coordinator (4)'s private panel-read recommendation, uncommitted before the ruling; known only from post-ruling spec rows (`:372-:373`). Values first committed cd521a4c after the ruling.
- Resp.: "go on open 2 and open 11" (22:52:15Z); "yes, bind MGC as stated" (00:17:19Z) — to coordinator (4), agent-recorded.
- Why: Leans 1: log attributes values to coordinator's panel read and 'as stated' implies adoption, but recommendation exists only post-ruling; operator attestation unperformed.
- Result: cd521a4c (MNQ/MYM/6J); MGC e2f6f93f, re-bound 6a6e037c on explicit ruling after Codex review; PR #661 merged 9dc5df30.
- Unc.: Committing the panel-read recommendation (digests only) before the ruling would make this class 1; the panel read itself stays private.
- Sources: docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md:372-:373; binding packet:44; git cd521a4c, e2f6f93f, 6a6e037c

**C4b** · 2026-10-04 · **class 4 (probable 1)** — Adopt three hyper simplifications: window may open at first complete permitted session; separate §13 provider/collector-loss amendment; FEED-16 shadow reuse already permitted.
- Rec.: Proposals from hyper's scrutiny worker, relayed by Codex Coordinator 2; known only from post-ruling addendum 84208add (binding packet `:382`). Disposition draft uncommitted.
- Resp.: "go on the proposal dispositions and open-3/4 as recommended" — Joshua to coordinator (4), 2026-10-04T00:17:19Z; agent-recorded.
- Why: Leans 1: hyper proposed and 'go on the proposal dispositions' implies dispositions were presented, but neither located; origin rests on post-ruling addendum.
- Result: 84208add via PR #666 (merge c95a40b1); OPEN-8 start text (spec `:376`); §7.1 body amendment PR #694.
- Unc.: Committing hyper's relay and coordinator's disposition draft would settle class 1; whether coordinator (4) recommended adopting these three is unrecorded.
- Sources: binding packet:380-:388; docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md:160,:376; git 84208add

**C4c** · 2026-10-04 · **class 4** — Reject hyper's proposal to drop the live month-end-adjacent session (window minimum stays frozen); defer funded emission-disabled collection overlapping T00.
- Rec.: Not located. hyper proposed the opposite; 'go on the proposal dispositions' implies coordinator (4) likely presented reject/defer, but no draft predates 84208add.
- Resp.: Same reply: "go on the proposal dispositions ..." (binding packet `:382`); dispositions in agent wording at `:384`, `:387`.
- Why: Class 1 if coordinator (4) drafted the dispositions; class 2 only if Joshua himself chose reject/defer. Records establish neither.
- Result: Window minimum stays frozen (spec §16.2); no pre-T00 collection spend.
- Unc.: Disposition draft uncommitted; the 2026-10-04 proposals note presents agent-written disposition text as a quote from Joshua.
- Sources: binding packet:382-:387; docs/notes/2026-10-04-feed-overlap-and-october-exception-proposals.md:1-:43

**C5** · 2026-10-09 · **class 4** — Operator's existing personal Tradovate account is the intended real-time CME source for the daemon, replacing Databento; subject to licensing answers; activation gated.
- Rec.: None for 2026-10-09. Earlier agent framing: A1 packet A′ (S2b ADR `:201`, `:350`) and Codex PR #344 rule, weeks before; no 10-09 packet found.
- Resp.: Agent report: "Accepted (operator executive decision, chat 2026-10-09)" (lane ADR `:3`); PR #743 body says Joshua confirmed ("confirm").
- Why: Called an operator executive decision, but route already agent-scored (A′), grounds are agent feed-note findings; neither class 1 nor 3 established.
- Result: Lane ADR Decision 3 (PR #743, merge c3bd4140); licensing questions sent/reframed 2026-10-10 (ad3b977c); owed items 3-4 gate activation.
- Unc.: Bundled with the venue/lane executive decision; agent-written grounds may be post-hoc justification. S2b §2 row and STATE still say no provider.
- Sources: lane ADR:3,:13-:17; PR #743; git ad3b977c

**C6** · 2026-10-12 · **class 4** — Send narrowed follow-ups: CME (licence route, classification, internal 15-minute bars, retention, fees, per configuration) and P6 to NinjaTrader/Tradovate API Support.
- Rec.: Not located. Joshua answered item 3 of the coordinator's in-chat route decision plan, never committed; feed note, packets, d507e141 and PR #812 lack it.
- Resp.: "1 merge, 2 extend, 3 send both, 4 downgrade, 5 keep" (PR #812 body); agent-recorded.
- Why: Numbered answer to an uncommitted plan; records don't say whether 'send both' was the recommended option or one of several.
- Result: CME follow-up sent on existing ticket (sender unnamed); P6 sent by Joshua 23:12Z; PR #812, PR #813.
- Unc.: Drafter of the narrowed wording is unrecorded; consequential only as licensing prerequisite (lane ADR owed item 4).
- Sources: docs/notes/2026-10-01-feed-provider-questions-DRAFT.md:347-:354; PR #812; PR #813; git db23f165, 485a153d

### D — Execution route

**D1a** · 2026-09-26 · **class 4** — Route feasibility (T08 plus CrossTrade REST assessment) is the first Tradeify deployment decision; T09 waits behind four-row gate table; allocation objective set.
- Rec.: None located (PR #506 body, commits, comments searched); earliest text, Claude-authored 38c6141, already says 'Operator direction 2026-09-26', so origin is unproven.
- Resp.: 'confirm route-first, the T09 gates and the allocation objective' (agent recorded in PR #506 comment, relayed from babysit session).
- Why: Joshua confirmed directions the PR already labelled 'operator direction'; no record shows him introducing them or an agent proposing first.
- Result: Checklist Addendum 2026-09-26 and T09 gate acceptance record; PR #506 squash-merged 2026-09-26.
- Unc.: Possibly operator-originated in an unrecorded session, or agent-drafted; 'confirm' could ratify an agent framing; commit-author name is not authorship evidence.
- Sources: checklist:345,352-392; PR #506 comment 5845088628; commit 38c6141

**D1b** · 2026-09-26 · **class 2** — T09 Gate A (factual disposition of CrossTrade REST and Vanguard returns) accepted with changes to findings A3, A5, A6; others as drafted.
- Rec.: Coordinating session (Claude Code, Opus 5.5) draft at bbaec94, REST §6.11, committed 17:22Z, before the ruling reviewing that revision; corrections 5037ba4 at 17:34Z.
- Resp.: Agent report: the operator '...ruled acceptance of the gate A factual assessment'; PR #514 labels 5037ba4 'Operator corrections'.
- Why: bbaec94 draft changed: A3 refusal-to-unknown mapping became three-case classifier; A5 'already resolved' became 'direction adopted, not discharged'; A6 gained freeze-record check.
- Result: REST §6.11 and Vanguard caveat rewritten (5037ba4); gate A 'Accepted with changes'; PR #514 merged 2026-09-26.
- Unc.: Joshua's words unrecorded; 'executive review' may name the Codex Astra seat, making corrections Astra's and this class 1 against Astra.
- Sources: docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#611-gate-a-factual-disposition; PR #514; commits bbaec94, 5037ba4

**D2** · 2026-09-24 · **class 1** — After T08 R3=NONE: hold live release (d); one vendor question Joshua sends CrossTrade (b); scope bounded-exposure amendment (a); no route change (c).
- Rec.: T08 §7.7 recommendation (hold release; option c not recommended) authored in PR #482 commit 151da0b (Claude co-authored), 18:35Z, before ruling record aafe848 at 19:15Z.
- Resp.: 'approve item 1' (agent recorded in T08 §7.8 as operator, in session, verbatim).
- Why: Located recommendation committed before the ruling and adopted in full ('All three parts adopted').
- Result: T08 §7.8, vendor-question draft and amendment scope note (PR #488, merged 2026-09-24); vendor reply recorded §7.9.
- Unc.: §7.8 execution conditions (Joshua sends from own account, bytes retained, one follow-up max, no identifiers) are absent from §7.7; their author is unrecorded.
- Sources: docs/briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md:139-175; commit 151da0b; commit aafe848

**D3a** · 2026-09-26 · **class 1** — First release: preserve-and-block for one attended session, then review before extension; indefinite automation suspension accepted; option B deferred, stays Proposed.
- Rec.: Coordinator-authored B-D packet §3/§6 decisions 5-6 ('Preserve-and-block; defer B's implementation'), committed PR #518 19:18-20:42Z, before 22:54Z ruling; Astra's recommended overall ruling uncommitted.
- Resp.: 'Preserve-and-block, accept suspension'; operator approved the recommended overall ruling in writing (agent recorded, incident ADR §A11).
- Why: Joshua picked the packet's recommended posture and B deferral and approved Astra's recommended ruling; both recommendations predate the ruling record.
- Result: Incident ADR §A11 (PR #515, merged 2026-09-26); B-D packet rulings table (PR #518).
- Unc.: Suspension acceptance answered an agent question with no recommended answer; manual-intervention wording came from Astra's approved, non-public written ruling; answer may be agent option label.
- Sources: incident ADR:357-368; B–D packet:335-360; PR #518

**D3b** · 2026-09-26 · **class 1** — C-a investigated first; no close amendment or residual risk accepted; C-b separate; operator-performed REST reads R-1/R-2 after entitlement; X-5 deferred.
- Rec.: B-D packet §6 decisions 1-2 ('Investigate C-a first'; 'Authorize the two REST reads'), committed PR #518 19:19-20:42Z, before 22:54Z ruling commits; Astra's recommended ruling uncommitted.
- Resp.: 'Record as Astra recommends'; 'The written ruling governs' (agent recorded, incident ADR §A11.1).
- Why: Joshua's answer explicitly adopts the agent (Astra) recommendation; packet decisions 1-2 were committed before the ruling.
- Result: Incident ADR §A11.1, drill-plan ruling block (PRs #515, #518); operator-performed R-2 (#550) and R-1 (#574) followed.
- Unc.: Ruling narrower than packet decision 1 (§1.1a left OPEN, C-c unruled, X-5 deferred); narrowings assumed in Astra's non-public ruling.
- Sources: incident ADR:370-384; B–D packet:11,341-346

**D4a** · 2026-09-28 · **class 4 (probable 1)** — CP-2: entitlement gates REST reads only; known-order defined; T07 rule; drill costs count against $700 ceiling; preservation trades fenced; Stage 0/1 kept.
- Rec.: Commissioning packet §1.1 says six proposed rulings were adopted as written; proposer unnamed; text first committed with ruling (dff4c8d); proposal uncommitted beforehand (PR #540 checked).
- Resp.: Agent report: '...the six proposed rulings below were adopted as written... adopted in the operator's Codex conversation and relayed'.
- Why: Proposed text adopted unchanged in a Codex conversation, likely agent-proposed; reclassified 1→4 as proposer unnamed and no pre-ruling copy located.
- Result: Commissioning packet §1.1 (PR #542, merged 2026-09-28); Stage 0 R-2 read ran on preservation trade (#550).
- Unc.: Proposer not named, proposal survives only as relayed after the ruling, and Joshua's words are not quoted.
- Sources: docs/notes/2026-09-27-route-commissioning-session-packet.md:58-95; PR #542; commit dff4c8d

**D4b** · 2026-09-28 · venue · **class 4** — Tradeify 'exclusive use' condition: no clarification sought from Tradeify; portfolios adapted to each firm's rules count as distinct strategies.
- Rec.: None. Commit 69cf00b (15:15Z, before 15:52Z ruling 92cae00) only flagged that a clarifying question to Tradeify may be needed.
- Resp.: Agent report: operator ruled 'no clarification with Tradeify is needed. Portfolios adapted to each firm's rules are treated as distinct strategies'.
- Why: Agent raised a question, not a recommendation; the 'distinct strategies' reading is credited to the operator, but his words are absent.
- Result: F-6(a) row updated; X-1 CP-3 carries operator's five-condition attestation (PR #542).
- Unc.: May be operator-originated (class 3) or rejecting the agent's soft suggestion (class 2); neither established; possible duplicate of a venue entry.
- Sources: docs/notes/2026-09-27-route-commissioning-session-packet.md:79; commit 69cf00b; commit 92cae00

**D4c** · 2026-09-29 · **class 1** — X-1: narrow A-11 exception (non-disableable firm risk liquidation as external actor, X-1 only); evening window withdrawn; CP-3 after R-1 on preservation trade.
- Rec.: Codex-drafted X-1 packet §2 (narrow exception) and §6 item 4 (R-1 first), committed 4825831 at 16:25Z, before ruling record 107094a at 17:08Z.
- Resp.: 'proceed as recommended' (agent recorded as operator ruling 2026-09-29, in session).
- Why: Joshua's own words adopt the packet's located recommendations, committed before the ruling.
- Result: A-11 text in B-D packet GC-7 row (canonical via ccfe233); evening window withdrawn; PR #551 merged 2026-10-01.
- Unc.: Exact ruling time unrecorded, between 16:25Z and 17:08Z; R-1-first sequencing superseded same day (D4d, D4e).
- Sources: X-1 packet:32-60; commit 4825831; commit 107094a

**D4d** · 2026-09-29 · **class 4** — Option (a): run R-1 on next week's preservation trade (due 2026-10-09), in its own session, before X-1's CP-3.
- Rec.: None between options: packet author set out (a) and (b) 'for Joshua, not resolved here' in 818ede6 (17:44Z), before ruling 042e21e (18:30Z).
- Resp.: Agent report: struck record 'Operator ruling 2026-09-29 (in session): option (a).'
- Why: Joshua chose between unranked agent-framed options; (a) matches an earlier §6 item 4 recommendation, but (a) itself was not recommended.
- Result: None; superseded same day by option (b) (2c8af2f, 18:43Z).
- Unc.: Could read as class 1, since (a) carries the earlier agent recommendation forward; conditions attached to (a) have no recorded origin.
- Sources: X-1 packet:62-70; commit 818ede6; commit 042e21e

**D4e** · 2026-09-29 · **class 2** — Option (b): X-1's own REST-placed order supplies the same-session per-order read, so CP-3 no longer waits for preservation-trade R-1.
- Rec.: None between (a) and (b); X-1 packet §6 item 4 (4825831, 16:25Z) recommended R-1 on preservation trade before X-1; options 818ede6 (17:44Z); ruling 2c8af2f 18:43Z.
- Resp.: 'we're going with b, so that we can deploy... as quickly as possible' (coordinating session; agent recorded; confirmed in X-1 packet session).
- Why: Joshua reversed agent's recommended R-1-first sequencing and his own (a) ruling, citing speed; X-1 took exposure without prior successful per-order REST read.
- Result: X-1 executed 2026-09-30T23:42:32Z; post-teardown R-1 on X-1's order discharged 2026-10-01 (PR #574).
- Unc.: Option (b) was agent-framed and agent-proposed CP-2 F-3 already allowed X-1's order as target; counting only the unranked choice gives class 4 or 3.
- Sources: X-1 packet:71-81; docs/notes/2026-09-27-route-commissioning-session-packet.md:87; commit 2c8af2f

**D4f** · 2026-10-01 · **class 1** — Build reviewed R-1 v3.2 collector (A); fallback C (rehome R-1) if not Codex-accepted and started by 16:30 ET; read is Joshua's.
- Rec.: Coordinating session's recommendation 'A, with C as the automatic fallback...' (X-1 packet §8); ruling recorded as 'replying to' it; text appears only in ruling record 321ebf5 (05:41Z).
- Resp.: 'go with A, dispatch the builder' (Joshua, ~05:34Z; agent recorded, confirmed in X-1 packet session).
- Why: An agent recommendation is quoted and Joshua's reply adopts it, fallback included.
- Result: Builder dispatched for build and offline test only; Joshua ran R-1 v3.2 2026-10-01: LOCATED_WITH_CLORDID (PR #574).
- Unc.: Recommendation not committed separately before the ruling; the start-by refinement came from an agent clarification after Codex review, not Joshua.
- Sources: X-1 packet:268-285; commit 321ebf5

**D4g** · 2026-09-30 · **class 4** — Amended X-1 CP-3: after deferral, a separate operator CP-3 approved a 23:30-00:00Z window and attended-input/1 adapter, outside Codex's R7 acceptance window.
- Rec.: None located: the CP-3 file is private (hash only) and the public record names no proposer, so origin cannot be classified.
- Resp.: Agent report: 'A separate operator CP-3... approved a 23:30-00:00Z window and an attended-input/1 adapter'.
- Why: Public record shows the operator's approval but not where the amendment came from.
- Result: X-1 sent 2026-09-30T23:42:32Z; single POST.
- Unc.: Origin may be in private session evidence that this public audit cannot read.
- Sources: X-1 packet:286-289

**D4h** · 2026-10-01 · **class 4 (probable 1)** — Record X-1 as run under amended CP-3; require retrospective local-Codex adapter review; no later row uses the adapter until review accepts it.
- Rec.: Unnamed agent 'recommendations' presented in the coordinating session (Codex returned the window-scope issue, 7c336ed); text kept only as ruling's three items; uncommitted beforehand.
- Resp.: 'Go with recommendations' (agent recorded; given in coordinating session, confirmed in X-1 packet session).
- Why: Joshua's words adopt agent recommendations; reclassified 1→4 because recommendation text was not kept apart from the ruling.
- Result: Codex retrospective review ACCEPTED_SCOPED_TECHNICAL_REVIEW (2026-10-01) for run-1930 only; future use barred.
- Unc.: Recommendation text not kept separately from the ruling, and the recommending agent is not named.
- Sources: X-1 packet:290-300; commit 1a3f532; commit 7c336ed

**D5a** · 2026-10-12 · **class 4** — Treat CrossTrade eval route as UNRESOLVED/not permitted on current support guidance; keep rail disarmed; escalate to human compliance; personal lane unaffected.
- Rec.: None located; support replies (bridges and direct API not permitted for eval accounts, 'No exceptions') are external fact; ADR addendum calls itself 'Summary, not a ruling'.
- Resp.: Agent report: 'Joshua has asked for escalation to human risk/compliance.' (route assessment addendum 2026-10-12).
- Why: Escalation is Joshua's act; whether an agent suggested it is unrecorded; UNRESOLVED/disarmed status and 'no effect on item 5' are agent assessments.
- Result: Route-record addenda and ADR item-5 records (PRs #801, #810, merged 2026-10-12).
- Unc.: Deployment Coordinator read the external support replies from Joshua's support thread; original bytes are private.
- Sources: docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md:368-384; lane ADR:135-150; PR #810

**D5b** · 2026-10-12 · **class 4** — Defer new Tradeify-route and activation work, including native-platform rewrites; personal lane proceeds under ADR 2026-10-09 §6.6 reading.
- Rec.: None located; record cites 'Joshua's confirmed sequencing (2026-10-12)', implying a proposal, but no proposal text is committed (PR #806, #810 bodies checked).
- Resp.: Agent report: 'New Tradeify-route work and native-platform rewrites stay deferred under Joshua's confirmed sequencing (2026-10-12).'
- Why: An agent reports a confirmation, but neither a recommendation nor Joshua's words were found.
- Result: STATE 2026-10-12 decision-index row (PR #806); live-wiring §6d marks GC-5/S2 as serving deferred route.
- Unc.: 'Confirmed' suggests an agent proposal, which would make this class 1 if found; §6.6 reading predates this decision (ADR addendum 2026-10-11b).
- Sources: docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md:383; STATE.md:40; PR #806

**D6** · 2026-10-12 · **class 4** — Keep the CrossTrade subscription while Tradeify-route work is deferred.
- Rec.: Item 5 of the coordinator's 2026-10-12 'route decision plan'; its options and any item-5 recommendation are not committed, so whether keep was recommended is unknown.
- Resp.: '5 keep' (agent recorded verbatim in subscription ledger change log 2026-10-12 and PR #812 body).
- Why: Joshua chose 'keep' on a numbered agent plan whose item-5 recommendation cannot be located.
- Result: SUBSCRIPTION_LEDGER change-log row and STATE 'Route plan rulings' row (PR #812); no amount change.
- Unc.: Recoverable only if the route decision plan text is retained somewhere public; it is absent from repo and PR.
- Sources: docs/pursuits/SUBSCRIPTION_LEDGER.md:42; STATE.md:41; PR #812

### E — Venue

**E1** · 2026-10-09 · **class 4** — Self-funded lane venue: Joshua's existing personal Tradovate account, chosen as broker over Ironbeam, a Rithmic FCM, tastytrade and IBKR.
- Rec.: None located for Tradovate as trading broker; prior agent scorings (2026-09-11, 2026-10-03) cover data-only use; integration-cost rationale first appears in recording commit 7cbc87c.
- Resp.: Agent report: ADR records the broker choice; PR #743 says Joshua confirmed every ruling on 2026-10-09 ("confirm").
- Why: No prior trading-broker recommendation; rationale written with decision; only operator word is bare "confirm"; earlier operator A′ (data) shortlist blocks agent-origin inference.
- Result: PR #743 merged 2026-10-09 (c3bd414), creating ADR 2026-10-09; Tradovate API access (owed item 3) still open.
- Unc.: 2026-10-09 chat not public; rejected set mirrors feed-note candidates P2–P6, so agent comparison probably framed options, but no recommendation is recorded.
- Sources: `lane ADR:13-15,54-56`; PR #743; 7cbc87c (Grounds only)

**E2h** · 2026-07-16 · **class 3** — History: self-funded scale lane and Aegis→M6J parked; research redirected to Striker MYM/MNQ reconstruction.
- Rec.: None located; ADR cites no packet and frames alternatives around the operator's closure. Pre-07-16 private archive not searched.
- Resp.: Agent report: ADR records "Operator directive 2026-07-16: self-funded is closed as a lane for now"; Joshua decision, Cursor recorder.
- Why: Positive evidence: record states an operator directive, names Joshua decider and the agent only recorder, and cites no prior packet.
- Result: ADR 2026-07-16 accepted; reconstruction tracks set TERMINAL 2026-07-24; lane closed until ADR 2026-10-09.
- Unc.: Private pre-07-16 archive unsearched; an earlier agent memo would reclassify to 4. Redirect drew on agent R5 research, so may be agent-framed.
- Sources: `docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md:3,9,36,66`

**E3a** · 2026-10-11 · **class 1** — First deployment operates one account at a time (Tradeify or personal, never both); simultaneous operation needs its own safeguard and operator ruling.
- Rec.: Deployment Coordinator, addendum 10-11b first draft (0c22ad9, 01:59Z) and PR #784 body: no simultaneous operation until opposing-exposure safeguard accepted; precedes 03:32Z corrections fold.
- Resp.: Agent report: ADR :115 says he "supports ... operating only one account at a time for the first deployment."
- Why: Agent draft proposed the exclusion; record says Joshua supports it, not listed as a correction (also reported as A5e1, F6b).
- Result: PR #784 merged 2026-10-11 (214010c): ADR :131; clearance plan §7.2 (PR #785, 0fcc71f).
- Unc.: Joshua's words unquoted; final text confines the rule to first deployment, unlike the draft's Phase 2 both-armed path; class 2 reading possible.
- Sources: `lane ADR:115,131`; 0c22ad9; PR #784

**E3b** · 2026-10-11 · **class 2** — One-account switch check: two-way, outgoing account flat, no working orders, cannot submit delayed entries; uncertainty blocks; no remediation window; lane priority dropped.
- Rec.: Deployment Coordinator, clearance-plan draft 5714da7 (2026-10-11T03:06Z): two-way flatness evidence, recommended 5-minute remediation bound, D12 lane priority; corrections folded 03:32-03:34Z.
- Resp.: Agent report: plan correction 2 reads "Remove the five-minute fix window; a two-way switch check ... where uncertainty blocks".
- Why: Joshua removed the agent's 5-minute remediation bound and added delayed-entry and uncertainty-blocks conditions to its two-way check (also reported as A5e, F6b).
- Result: ADR :131 (PR #784); plan §7.2 and new P-SW packet under #779.
- Unc.: Draft already had symmetric two-way flatness, so the commit's attribution of "two-way switch check" to Joshua overstates; his verbatim corrections are unquoted.
- Sources: 5714da7 (plan lines 286-296, 405-406, 439); `docs/notes/2026-10-11-personal-clearance-plan-tradeify-book.md:28-29`; 5034deb

**E3c** · 2026-10-11 · **class 2** — Tradeify FTA §6.6 reading: personal brokerage account is a personal account, not another firm; no §6.6 gate; ownership and §6.7 restrictions bind.
- Rec.: Deployment Coordinator, 10-11b first draft (0c22ad9), PR #784 body and plan draft 5714da7: same reading held unresolved behind written-answer or risk-acceptance gate; all precede corrections.
- Resp.: Agent report: plan correction 1, "Remove the blanket §6.6 permission gate; keep the ownership and opposing-exposure restrictions".
- Why: Joshua rejected the agent-recommended written-answer or risk-acceptance gate and made the leaning reading the adopted one (also reported as A5d).
- Result: PR #784 merged (214010c): ADR :125-133, written Tradeify answer not required; clearance plan §7.1 and item-5 criteria.
- Unc.: Joshua's words unquoted; ADR leaves residual ambiguity "Joshua's to weigh"; Tradeify compliance escalation unanswered.
- Sources: `lane ADR:125-133`; `docs/notes/2026-10-11-personal-clearance-plan-tradeify-book.md:28,277`; 0c22ad9

**E4** · 2026-10-02 (local; sitting attribution disputed) · **class 4 (probable 1)** — 90-day venue-facts re-verification covers only the four friendly firms; Earn2Trade, Apex, Topstep and TradeDay rows stay stale, re-verify before use.
- Rec.: Coordinator (3)'s 2026-10-02 decision sheet E, presented in chat and uncommitted; existence attested only by recorded reply (`ops/prop_envelope_default.md:83`, PR #620); presented with ruling.
- Resp.: Joshua, verbatim as agent-recorded: "all recommended" (`ops/prop_envelope_default.md:83`; PRs #620, #621, #649).
- Why: His reply selects an agent sheet's recommendations; reconciled 1→4 because sheet E is uncommitted and known only from agent restatement.
- Result: PR #621 re-verified four rows (04c4956); PR #649 added scope note at `ops/prop_envelope_default.md:83`, trigger moved to ~2026-12-31.
- Unc.: Sheet-E text not public; recommended wording and alternatives known only from agent record; #649 review notes original sheet-E facts were not independently verified.
- Sources: `ops/prop_envelope_default.md:83`; `STATE.md:45,177-180`; PR #620

### F — Sequencing

**F1a** · 2026-09-22 · **class 1** — D-sequence: accept T05 parallel build behind a versioned T02 freeze and T06 fold-with-preserved-work; E01–E12 table gates T02 checkpoint acceptance.
- Rec.: Amendment author (Claude Fable 5.1), amendment PROPOSAL :173 "TICK, with two conditions"; committed 59683cc (00:50Z) before ratification 118cd47 (04:25Z).
- Resp.: "Adopt all five as recommended." Operator, 2026-09-22, in session; agent-recorded by the amendment author (:181).
- Why: Committed recommendation preceded the ruling in git order; operator adopted it verbatim "as recommended".
- Result: §4 D-sequence box ticked (:73) in 118cd47; no downstream receipt attributable to the ruling.
- Unc.: No receipt shows either condition (versioned freeze; E01–E12 table gating T02 checkpoint) applied. Codex shaped the parent amendment; spine frozen since 2026-10-13.
- Sources: `amendment:173-181`; commit 59683cc; commit 118cd47

**F1b** · 2026-09-22 · **class 1** — D-T00: authorize T00 step 1 only (producer inventory, may return INSUFFICIENT); pre-registration waits on positive step 1; condition 4 left to operator.
- Rec.: Amendment author (Claude Fable 5.1), PROPOSAL :129 "TICK step 1 now"; committed 59683cc (00:50Z) before ratification 118cd47 (04:25Z), same addendum.
- Resp.: "Adopt all five as recommended." Operator, 2026-09-22, in session; agent-recorded (:137).
- Why: Committed recommendation row adopted verbatim "as recommended"; git order shows the recommendation came first.
- Result: D-T00 ticked (:69); step 1 INSUFFICIENT accepted 2026-09-23 (ab07226); later P7 MET at 2baa516.
- Unc.: Authorized, not dispatched (coordinator's separate act). No recommendation given for condition 4; Joshua ruled it NO 2026-09-23, origin not established.
- Sources: `amendment:129-139`; commit 59683cc; commit 118cd47

**F2a** · 2026-10-02 (~21:00Z) · **class 4 (probable 1)** — Sitting-1 T00 order: step-3 screen on current code before r3c-a2 expires, then T05 qualification fixes merge, then P7 re-run under fresh approval.
- Rec.: Deployment coordinator's sitting-1 recommendations, in chat, uncommitted; attested by Joshua's reply (PR #610 body); Codex relay 5962322698 confirms a list, not the T00 order. No pre-ruling copy.
- Resp.: "all recommended; yes to carry rule and term 8" (Joshua to the deployment coordinator, ~21:00Z; agent-recorded, PR #610 body).
- Why: Joshua accepted recommendations unchanged, but the sheet was uncommitted; the T00-order content survives only in the post-ruling agent record.
- Result: Recorded at checklist :35 and closure doc :770 via #610; never executed, superseded by F2b; r3c-a2 lapsed.
- Unc.: Item (1) could not run on current code; an agent record noted r3c's SCREEN refusal at 19:58Z. Agent recommendation error, later agent-corrected.
- Sources: `checklist:35`; PR #610 comment 5962322698; PR #581 comment 5960404978

**F2b** · 2026-10-02 local / 2026-10-03 UTC · **class 4 (probable 1)** — Sheet A1: signed T00 screen authority: design (Joshua approves pre-code), build, P7 re-run, Joshua signs, step 3 once; r3c-a2 lapses unused.
- Rec.: Deployment coordinator (3)'s decision sheet, in chat, uncommitted, preceded the reply; agent-sourced basis in #581 comment 5960404978 (19:58Z). Ruling recorded d27c7a1, PR #620.
- Resp.: "all recommended" plus "yes to A3", replying to coordinator (3)'s sheet; agent-recorded at checklist :36 and PR #620 body.
- Why: Agent sheet accepted with "all recommended" but uncommitted; only its technical finding is agent-sourced; Codex observed the ruling, not the recommendation.
- Result: #620 merged 2026-10-03; design #629 and build card #634 approved; step 3 NO-GO-evidence, robust, 2026-10-08.
- Unc.: Sheet text uncommitted. d27c7a1 (~01:08Z) precedes relay-observed 01:16Z, unresolved. Unknown whether Joshua prompted the re-examination.
- Sources: `checklist:36`; PR #620 comment 5964508997; PR #581 comment 5960404978

**F3a** · 2026-10-12 · **class 4 (probable 1)** — §6b owner-file order: P-L2 may take book_account_owner.py before GC-5-DISPLACED and TB-I3 S2, one writer at a time; run-path card A precedes GC-5.
- Rec.: Deployment Coordinator's chat packet, uncommitted, grounded on an uncommitted readiness return at ebd84e4 (:173); reverses earlier agent order "GC-5 first, then by readiness" (:106).
- Resp.: "1 yes, 2 yes" (Joshua, 2026-10-12, directly to the Deployment Coordinator; agent-recorded at live-wiring packet :171).
- Why: Joshua said yes to coordinator proposals, but the chat packet was uncommitted; its wording is known only from the post-ruling record.
- Result: #802 merged 2026-10-12 (e150fd0); P-L2 #805 merged as 143a61a; GC-5/S2 frozen 2026-10-13.
- Unc.: No independent observation of the ruling found. The agent revised its own earlier order on new read-only evidence.
- Sources: `live-wiring packet:169-174`; `live-wiring packet:106`; PR #802

**F3b** · 2026-10-12 · **class 4** — §6d: after P-L2, book_account_owner.py writer order is P4 → P-SW → GC-5-DISPLACED → TB-I3 S2; GC-5 and S2 re-anchor after P-SW.
- Rec.: None located: coordinator's uncommitted "decision plan" framed options; its item-2 recommendation is unrecorded (searched repo, db23f16, PRs #802/#805/#812), leaving class 1 versus 2 open.
- Resp.: "2 extend" (Joshua, 2026-10-12, directly to the Deployment Coordinator; agent-recorded, live-wiring packet :188).
- Why: Agent-framed option set, but no record shows whether "extend" was recommended or an alternative Joshua chose.
- Result: §6d recorded in db23f16, PR #812 (merged 2026-10-12); STATE :41; GC-5/S2 tail frozen 2026-10-13.
- Unc.: Class 1 if "extend" was the plan's recommendation, class 2 if Joshua picked against it. Edit-site overlap "Not checked" (:192).
- Sources: `live-wiring packet:186-192`; PR #812; `STATE.md:41`

**F4** · 2026-10-12 · **class 1** — Q-SFCLEAR-2 run-path order A0→A→C→B→D→E; each card a single Codex-local writer, D Part 2 a Claude private executor act; none enters owner queue.
- Rec.: Drafting worker for the Deployment Coordinator, run-path packet :97 "Recommendation: the order above"; committed bcedcea (17:56Z), before ruling af2739a (18:18Z).
- Resp.: "... 5 as proposed ..." (Joshua, directly to the Deployment Coordinator; agent-recorded at run-path packet :99).
- Why: Committed Recommendation accepted "as proposed"; git order shows the recommendation first.
- Result: PR #798 merged 2026-10-12 (cards A–E frozen); STATE :40; card A dispatched.
- Unc.: The coordinator's relay of the packet is not separately evidenced; executor choices ride in the same recommendation. Amended by F3a.
- Sources: `docs/notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md:85-101`; PR #798; commits bcedcea, af2739a

**F5** · 2026-10-12 · **class 1** — O1: prepare R1's local settlement-import workflow and R2's read-only readiness view first, with baseline measurement; preparation only; O2–O4 keep defaults.
- Rec.: Operator-attention proposal author (PR #789, Codex branch; later Claude review commits), proposal :393 O1 row; present in cf6408b (2026-10-11T19:31Z), before ruling 99af266.
- Resp.: "approve O1" (to Claude Code; 99af266), reconfirmed "yes I approved O1" (to the Deployment Coordinator); agent-recorded at proposal :377.
- Why: Committed recommendation row approved by name; the recommendation predates the ruling.
- Result: PR #793 merged 2026-10-12 (§6 ruling, STATE row); frozen 2026-10-13 before any implementation card.
- Unc.: Source of the earlier recommendations Joshua asked to sharpen is unidentified; O2–O4 took effect by default-unless-objected, not Joshua's quoted words.
- Sources: `docs/notes/2026-10-11-tradeify-operator-attention-proposal.md:375-397`; PR #793; commits cf6408b, 99af266

**F6c** · 2026-10-11 · **class 1** — Run a cheap sizing, margin and risk pre-screen before expensive personal-lane runs.
- Rec.: Deployment Coordinator, clearance plan first draft 5714da7:94 "Zero-K pre-screen (data-independent)", 2026-10-11T03:06Z, before the corrections fold at 03:32Z.
- Resp.: Agent report: Joshua "supports ... a cheap sizing, margin and risk pre-screen before expensive runs" (ADR :115; plan :24).
- Why: The agent proposed the pre-screen-first ordering and Joshua endorsed it; only the ordering is classed.
- Result: Private pre-screen (hash-bound record) preceded Joshua's R1 ruling (Q-SFCLEAR-1 brief :24).
- Unc.: "Supports" is a paraphrase. Pre-screen content changes (correction 3; no 85% margin utilization without cash-buffer rationale) are class 2 under risk criteria.
- Sources: `lane ADR:115`; `docs/briefs/Q-SFCLEAR-1-personal-clearance-tradeify-book.md:24`; commit 5714da7

### G — Verification

**G1a** · 2026-09-27 · **class 4 (leans 3)** — Evidence proportional to the next step: bound each step under explicit limits; unknowns block only the activity they affect.
- Rec.: None located: git log -S on both phrases first hits 9448373f, which records the direction itself; absence does not prove operator origin.
- Resp.: "Unknowns should block the activity they affect, rather than every downstream preparation task." Claude recorded it (9448373f).
- Why: Recorded as operator direction quoting Joshua; no earlier agent packet, but nothing shows it unprompted or his wording; in-session exchange not public.
- Result: Checklist addendum and handoffs H1-H10 (9448373f, revised 1b365519); PR #520 merged 2026-09-27.
- Unc.: An in-session agent suggestion cannot be excluded; may be relayed advisor text (PR #520 comment shows advisor guidance under Joshua's account).
- Sources: `checklist:37,392-394`; commit 9448373f; PR #520 comment 5857162903

**G1b** · 2026-09-27 · sequencing · **class 2** — Staged-acceptance plan structure (changed-gates table, evidence classes, CP-1a..CP-9, handoffs H1-H10), corrected after Joshua reviewed the first draft.
- Rec.: Claude draft commit 9448373f (2026-09-27T01:32Z) proposed nine checkpoints and handoffs; revision 1b365519 followed 12 minutes later, before merge.
- Resp.: Agent report: plan "Revised 2026-09-27 after the operator's review of `9448373`"; nine corrections listed in agent words (checklist :396).
- Why: Joshua changed the agent draft: nine operator-attributed corrections, e.g. consuming #519's returns, separating preparation from execution authority.
- Result: 1b365519 revised addendum and handoffs; PR #520 merged 2026-09-27.
- Unc.: Joshua's wording not public; review may be relayed advisor text (posted under his account; 12-minute window); if so, the corrections' judgment was another agent's.
- Sources: `checklist:396-406`; commits 9448373f, 1b365519; PR #520

**G2a** · 2026-10-12 (UTC; e953ca69 at 2026-10-11 20:46 -0400) · **class 4** — Q-SFCLEAR-2 step-1 choices: (d)-1, (f) Vanguard drift binding (G1-D/G3-D), (g) schedule kept, (j) corrected premise accepted, (k)-1.
- Rec.: None located: draft 6eabdb63 §12 step 1 lists alternatives without recommendation; PR #752 body asks Joshua to choose; 10-11 relay is private.
- Resp.: "(d)-1, (f) binding, (g) keep, (j) accept, (k)-1", to the Deployment Coordinator; agent-recorded (prereg :343).
- Why: Agent framed options, Joshua selected; no public recommendation. (f) binding departs from successor ruling (a)'s drift re-check.
- Result: e953ca69 applied rulings (cells G1-D/G3-D, FG item 4 dropped); frozen in F 83867f0, PR #752.
- Unc.: Private relay could hold recommendations; if it recommended a non-binding drift re-check, (f) would be class 2.
- Sources: `docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md:78,97-101,340-356`; commits 6eabdb63, e953ca69; PR #752

**G2b** · 2026-10-12 (UTC; 1d194832 at 2026-10-11 21:10 -0400) · **class 1** — Q-SFCLEAR-2 choices (a)(b)(c)(h) as drafted: gap term in every ON leg's G3/G1; B2 g = 0.15×G3; slippage residual non-binding.
- Rec.: Drafting worker for the Deployment Coordinator; drafted text at 6eabdb63 (2026-10-11 20:19 -0400), before ruling at 1d194832 (21:10) (prereg :341-351).
- Resp.: "(a)(b)(c)(h) yes", to the Deployment Coordinator; agent-recorded (prereg :343).
- Why: Agent drafting text, committed before the ruling, accepted unchanged.
- Result: Recorded at 1d194832; frozen in F 83867f0.
- Unc.: Agent-framed from Joshua's 2026-10-11 direction 'accept all four, have the worker draft the successor'.
- Sources: `docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md:341-351`; commits 6eabdb63, 1d194832

**G2c** · 2026-10-12 (F committed 13:41:53 -0400; PR #752 merged 18:51:05Z) · **class 1** — Ratify Q-SFCLEAR-2 at draft b97beaa, freeze at F 83867f0, with Joshua's tuple re-hash and exposure attestation.
- Rec.: Pre-registration authored by drafting worker for the Deployment Coordinator (prereg :6); draft b97beaa (12:22 -0400) precedes ratification in F (13:41); attestation steps from Codex/review folds.
- Resp.: "ratify Q-SFCLEAR-2 at b97beaa..."; "1. I haven't seen any of them 2. i re-confirm"; agent-recorded (prereg :3).
- Why: Joshua ratified committed agent-drafted text unchanged at a named commit; procedure agent- and Codex-designed.
- Result: Freeze commit F 83867f0 with PRIVATE_EVIDENCE rows; PR #752 merged 2026-10-12; superseded by G6d.
- Unc.: Class 1 rests on draft authorship, not bare 'ratify'; embedded G2a selections (class 4) and privately relayed 10-11 rulings do not inherit it.
- Sources: `docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md:3-6,27,51,56`; commits b97beaa6, 83867f0d; PR #752

**G2d** · 2026-10-12 · **class 1** — Extend §60 VM exception so run-path card D's FG evidence run may use Joshua-controlled Azure VM; ports and effective_inputs.json only, no Pine.
- Rec.: Drafting worker for the Deployment Coordinator: packet first commit bcedcea8 (13:56 -0400) said "Recommendation: (b), if you extend the exception"; ruling applied af2739a0 (14:18).
- Resp.: "... 6 b (extend §60 to the FG run), 7 b", to the Deployment Coordinator; agent-recorded (packet :101).
- Why: Packet recommended (b) conditional on the extension; Joshua chose (b) and granted the extension in the same words.
- Result: Campaign §60 addendum 2026-10-12 (:4073); run-path cards updated af2739a0 (#798); superseded 2026-10-14.
- Unc.: Agent recommended the extension; only Joshua could grant it. The 2026-10-14 addendum re-grants same terms for Q-SFCLEAR-3 runs.
- Sources: `docs/notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md:18,93-101`; `campaign:4073,4083`; commits bcedcea8, af2739a0

**G3a** · 2026-10-02 (about 05:10-05:27Z) · **class 4** — Scope T00 P7's code_closure_sha256 claim to Python source closure plus interpreter binding; defer environment sealing to T05, before the R1 grant.
- Rec.: None located: trigger was Codex P1 on #594 (r4163033692) asking to hash runtime dependencies; coordinator reply r4163160489 records only the ruling.
- Resp.: "scoping is fine, defer the sealing to T05", in the coordinating session; agent-recorded (r4163160489, 19863dd2).
- Why: 'scoping is fine' reads as answering a proposal, but no proposal or recommendation is public; Codex's conditional is consistent, not overridden.
- Result: 19863dd2 scoped the p7_evidence docstring; ledger 50ab7458; PR #597 merged 2026-10-02.
- Unc.: Phrasing suggests an agent proposed the scoping; the record does not establish it.
- Sources: `slices ledger:2000-2006`; commit 19863dd2; PR #594 review comments r4163033692, r4163160489

**G3b** · 2026-10-02 (before 50ab7458 at 10:57 -0400) · **class 4** — Choose T05 sealing option 'C', later revised to C′ after the H9 source check found host-side code decides outcomes.
- Rec.: None located: the option set 'C' refers to is in no commit or PR #594/#597 thread; revision attributed to the agent H9 source check.
- Resp.: "C for the T05 sealing"; agent-recorded (execution-slices :2007).
- Why: Joshua picked a lettered option whose alternatives and any recommendation are not public.
- Result: Recorded at 50ab7458 (PR #597, merged 2026-10-02); amended to C′ (G3c).
- Unc.: Options were agent-framed in session; whether C was recommended is unknown.
- Sources: `slices ledger:2007`; commit 50ab7458; PR #597

**G3c** · 2026-10-02 · **class 4 (probable 1)** — Accept coordinator's narrowed C′: identity checks cover only finite known R1 host entrypoints; unmediated descendants and OS helpers join the residual.
- Rec.: Coordinator, in session before the 'yes'; no separate committed proposal; recorded only within ruling commit 50ab7458 (execution-slices :2008).
- Resp.: "yes" to the coordinator's narrowed C′; agent-recorded (execution-slices :2008).
- Why: Reclassified 1→4: proposal uncommitted, surviving only as the agent's summary inside the ruling entry; Joshua's 'yes' answers it.
- Result: C′ design recorded (:2024-2036); H9 C′ build card drafted; later S6 term 7 (1accd675).
- Unc.: Codex-driven extensions (VALID→VOID, uncharged recheck) were approved only through the later 'accept all seven'.
- Sources: `slices ledger:2008,2024-2036,673`; commits 50ab7458, 1b679048, 1accd675

**G3d** · 2026-10-02 · **class 1** — Pin standing worker base image python:3.12.3-slim-bookworm by manifest-list digest afc139a0…; later changes need Joshua's ruling.
- Rec.: Coordinator: digest from agent S5/S4 Linux evidence (first recorded a5f4099d, 2026-09-18) and a coordinator registry read, before ruling at 8e0cb569.
- Resp.: "yes to the pin"; agent-recorded (execution-slices :2009).
- Why: The specific digest came from agent-run evidence and the coordinator's read; Joshua approved the pin.
- Result: 8e0cb569; C′ build card D3 pin file carries the digest.
- Unc.: Proposal message not public; accepted trade-off (no later security patches) stated as accepted, not recommended.
- Sources: `slices ledger:2009-2013`; commits 8e0cb569, a5f4099d; `docs/briefs/handoffs/2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md:86-91,247`

**G3e** · 2026-10-02 (between 15:07Z and 15:19Z) · **class 4** — Broaden R1 to the combined Linux node set plus C′ and VALID→VOID cases, superseding H9 R1's result/seal-only set.
- Rec.: None located: agent commit 50ab7458 wrongly listed the broad R1 as unchanged; Codex P2 on #597 flagged it; 1b679048 retracted.
- Resp.: "broaden R1"; agent-recorded (execution-slices :2014).
- Why: Agents raised and briefly asserted the broad set; Joshua resolved toward it. No recorded recommendation.
- Result: 8e0cb569, then 0c35bc68 (H9 R1 work step runs the combined set).
- Unc.: Broad wording first appeared in unattributed 'coordination messages'; rationale at :2022 may reflect an unshown agent recommendation.
- Sources: `slices ledger:2014-2022`; commits 50ab7458, 1b679048, 8e0cb569; PR #597 review comment r4166986035

**G3f** · 2026-10-02 · risk criteria · **class 4** — Accept residual 'T05 C′ first-release host environment drift' (unsealed distribution, tzdata, mounts, native libraries, OS helpers, kernel; unmeasured) for first release.
- Rec.: None located: no explicit recommendation to accept; agent wrote the residual's content, partly from the narrowed C′ proposal (G3c).
- Resp.: Agent report: "Residual accepted by Joshua for the first release" (execution-slices :2038); the label is the agent's, not Joshua's.
- Why: Acceptance asserted without Joshua's words; no recommendation to accept the whole residual shown.
- Result: Recorded at 50ab7458 (PR #597); cited in S6 term 7 (:692).
- Unc.: Could be read as part of G3c's 'yes', but the record states the acceptance separately.
- Sources: `slices ledger:2038-2043,692`

**G4a** · 2026-10-03 (between 03:25Z and 04:04Z) · **class 4 (leans 3)** — T00 screen depth N = 1,000 per population (sheet 5).
- Rec.: None located: design §12 item 9 says "no number is recommended here"; PR #629 comment says coordinator (3) asked Joshua for a number.
- Resp.: "I approve of the recommendations, let's make it happen", answering private sheet 5, item 2 not marked 'as recommended'; agent-recorded (PR #634).
- Why: No number recommended and coordinator asked Joshua; later agent wording 'against your 1,002' hints Joshua's number. Leans 3, unestablished.
- Result: Card §8 recorded at d230b46b; superseded by G4b.
- Unc.: Sheet 5 is private and may have recommended 1,000; option (a) = 1,000 was agent-framed in design §6.4.
- Sources: `docs/superpowers/specs/2026-10-02-t00-screen-authority-design.md:600-612,725-726`; PR #629 comment 5965049542; PR #634 comment 5965354454

**G4b** · 2026-10-03 (about 17:19Z) · **class 1** — Revise T00 depth to N = 5,001 per population (1,667 per root), following the precision packet.
- Rec.: Precision packet commit 90e2587 (2026-10-03 00:08 -0400) §5 recommends N = 5,001; ruling about 17:19Z followed.
- Resp.: "I approve your recommendations", replying to "Depth N: 5,001 recommended, against your 1,002"; to coordinator (3); agent-recorded (T00 card :427).
- Why: An explicit committed recommendation was presented and Joshua approved it.
- Result: b03086d9 revised card §8 to 5,001; superseded by G4c.
- Unc.: Packet branch never merged or opened as a PR; retrievable only from remote branch claude/t00-depth-decision-packet.
- Sources: `T00 card:427`; commit 90e2587; commit b03086d9

**G4c** · 2026-10-05 · **class 2** — Final T00 depth N = 1,002 per population (334 per root), replacing approved 5,001 and interim 3,000; frozen at ratification.
- Rec.: Precision packet 90e2587 recommended 5,001 (approved G4b, 2026-10-03); alternatives 3,000 and 10,002; 1,002 only in its table and design option a.
- Resp.: "you know what, I have changed my mind. let's go with N = 1000", to coordinator (4); agent-recorded (T00 card :488).
- Why: Joshua departed from the packet's 5,001 recommendation: first 3,000 (alternative A), then 1,000, which the packet did not recommend.
- Result: PR #691 merged 2026-10-05 (38190afe, b6d6a1c8, 6d8280ba); T00 screen completed at N = 1,002.
- Unc.: The 2026-10-05 exchange before 3,000 is not public; a neutral menu that day could make it 4, never 3.
- Sources: `T00 card:488,574`; PR #691; commits 38190afe, b6d6a1c8

**G5a** · 2026-10-02 sitting 2 (ruling 2026-10-03T01:42Z) · **class 1** — D-MON-1 alert channel: provider A, Grafana Cloud IRM free tier, subject to qualification; B (Healthchecks.io plus PagerDuty Free) fallback.
- Rec.: Options packet lean "A, then B, then C" in first commit 63dcf871 (2026-10-02 15:57 -0400), before sitting-2 ruling 2026-10-03T01:42Z.
- Resp.: "all recommended" at sitting 2; ruling text 'A ... subject to qualification. B is the fallback' (packet :124); agent-recorded.
- Why: Committed lean is a recommendation; ruling matches it exactly, A first with B fallback.
- Result: Joshua opened the account 2026-10-03; binding card PR #635 merged 2026-10-04; Q7 passed 2026-10-05.
- Unc.: Sitting-2 sheet is private; match to the lean inferred from ruling text; bare 'all recommended' alone would not prove origin.
- Sources: `docs/notes/2026-10-02-d-mon-channel-options-packet.md:93-95,124`; PR #635; commits 63dcf871, 4d64e213

**G5b** · 2026-10-12 · **class 4** — Drop Grafana to Free at trial end; before first armed session, prove IRM SMS/voice with an attended test page or upgrade.
- Rec.: None located: route decision plan item 4 is uncommitted; PR #812 quotes only Joshua's answers; nearby agent text set the check, not plan tier.
- Resp.: "4 downgrade" (within "1 merge, 2 extend, 3 send both, 4 downgrade, 5 keep"); agent-recorded (watch draft :137, PR #812).
- Why: Option list and any item-4 recommendation not public; re-prove condition echoes 10-07 agent text not shown as a recommendation.
- Result: db23f165, PR #812 merged 2026-10-12; STATE :41 and :136 updated.
- Unc.: Keeps Joshua's 10-07 upgrade-if-needed condition but defers proof to before arming; whether an agent recommended downgrading is unknown.
- Sources: `docs/notes/2026-10-02-t13-a12-f3-held-request-watch-draft.md:134-138`; `STATE.md:41,136`; PR #812

**G6a** · 2026-10-13 · **class 4** — Replace frozen Q-SFCLEAR-2 with successor pre-registration (option B): same R1 tuple, 15:55 flatten at adverse intrabar placement, exposed legs only.
- Rec.: None located: the coordinator's options packet is uncommitted; PR #834 and the prereg cite only the choice.
- Resp.: "go with B, draft the successor pre-registration", to the Deployment Coordinator; agent-recorded (Q-SFCLEAR-3 prereg :5).
- Why: Joshua chose a lettered option from an agent packet; whether B was recommended is not public.
- Result: Draft d73a0575; PR #834 merged 2026-10-14; realized in G6d.
- Unc.: The packet is private or in session only.
- Sources: `docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md:5`; PR #834

**G6b** · 2026-10-13 · **class 1** — Q-SFCLEAR-3 (s1) uses the R1 run alone at 15:55, not the two-run bracket; (s2) no private R2 sensitivity report.
- Rec.: Deployment Coordinator draft d73a0575 (23:08:35 -0400): §S row 2 'R1 alone', (s2) default no; ruling recorded 62 s later at 5bfb1df0.
- Resp.: "R1 alone, no R2 report", to the Deployment Coordinator; re-confirmed at freeze "2. i re-confirm"; agent-recorded (prereg :142, :3).
- Why: Joshua accepted the drafted design and its stated default.
- Result: 5bfb1df0; an R2 run is now a forbidden move (:57); PR #834 merged.
- Unc.: Agent-framed from option B (G6a, class 4), which already implied R1-alone; 'conservative-leaning' description later withdrawn.
- Sources: `docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md:3,15,24,140-142`; commits d73a0575, 5bfb1df0; PR #834

**G6c** · 2026-10-13 (ET) · **class 1** — Q-SFCLEAR-3 (s3): exclude evidence-located rows; R1 applies at every exposed 15:55 instant (option (i)).
- Rec.: Deployment Coordinator "recommended and applied (i)" at de782a68 (23:41 -0400), after Joshua delegated; then in ratified draft 235f523, re-confirmed at F3.
- Resp.: "go with your best recommendation on 2", then "...2. i re-confirm" at freeze; agent-recorded (prereg :143, :3).
- Why: Joshua delegated, the coordinator chose (i), and Joshua re-confirmed (s3) after it was applied.
- Result: de782a68; card B amendment (c) requires empty splits (card B :247).
- Unc.: Delegation preceded the recommendation; coordinator chose knowing T00 facts (52% split yield; 190 unlocated splits fail), disclosed at §D :16.
- Sources: `docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md:3,16,143`; commits 424f86f2, de782a68; `docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-b-personal-replay-card-DRAFT.md:244-249`

**G6d** · 2026-10-14 (F3 13:14:04 -0400; PR #834 merged 19:07:13Z) · **class 1** — Ratify Q-SFCLEAR-3 at draft 235f523, freeze at F3 15bea250, with Joshua's tuple re-hash and exposure attestation.
- Rec.: Pre-registration authored by the Deployment Coordinator (prereg :6); draft 235f5234 (2026-10-14 03:44 -0400) committed before F3 (13:14); attestation clauses agent-written.
- Resp.: "confirm the §S changes as recorded"; "ratify Q-SFCLEAR-3 at 235f523..."; "...2. i re-confirm"; agent-recorded (prereg :3).
- Why: Joshua confirmed and ratified committed agent-drafted text unchanged at a named commit.
- Result: F3 15bea250; metadata 22388ca5; PR #834 merged 2026-10-14.
- Unc.: Class 1 rests on draft authorship, not bare ratification; the ratified text embeds G6a (class 4) and the G6b/G6c choices.
- Sources: `docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md:3-6,147`; PR #834; commits 235f5234, 15bea250, 22388ca5

### H — Stop/go

**H1** · 2026-10-13 · **class 4** — Suspend (not kill) Track B: freeze Tradeify-specific build and spend; draft 11-08 decision rules; defer FLOOR-HALF pass-time (E1 kill) check.
- Rec.: None located: ruling answers the 2026-10-13 cloud status review (checklist:929), absent from main and PRs #826/#830/#836/#841; class 1 cannot be shown.
- Resp.: "1 yes", "4 yes" (Joshua directly to the Deployment Coordinator), recorded by the Deployment Coordinator agent.
- Why: Numbered answers imply a presented list, but neither the list nor any suspension recommendation is public; no operator-origin evidence either.
- Result: Checklist addendum `:927-939`, `STATE.md:39` via PR #826 (381c47c, merge 7a4eb00).
- Unc.: Record does not map items 1 and 4 to actions; frozen-scope lists are agent-written and unattributed; review figures labelled unverified.
- Sources: `checklist:927-939`; PR #826; git 381c47c

**H2a** · 2026-10-09 · **class 3** — Reopen self-funded lane on Joshua's personal Tradovate account as posture and research target (GO); no capital authorization until clearance standard and checklist.
- Rec.: None located for reopening; nearest agent precedents (2026-07-16 closure's re-open path, feed-note P6, 09-11 A1 packet) concern a GO path or data route, not a trading lane.
- Resp.: Agent report: ADR status "Accepted (operator executive decision, chat 2026-10-09)"; PR #743 says Joshua confirmed ("confirm").
- Why: Record and first commit 7cbc87c label it an operator executive decision; no earlier reopen recommendation found (also reported as E2).
- Result: ADR 2026-10-09 merged via PR #743 (c3bd414), plus Q-SFGROWTH-1 Pre-Q and STATE rows.
- Unc.: Pre-decision chat not preserved, so an agent suggestion cannot be excluded; the 'operator executive decision' label is the recording agent's.
- Sources: `lane ADR:3,13-14,44-53`; PR #743; commit 7cbc87c

**H3a** · 2026-10-11 · **class 1** — Live-wiring rulings J-1 to J-4 and §5 defaults as recommended: EF shared GO/sizing, code admission, FILE sizing source, J-4 build gate.
- Rec.: Live-wiring lane packet Recommendation column (`live-wiring packet:21-28`), committed 748afdc 17:11Z (PR #788), before the ~17:15Z ruling.
- Resp.: "J-1 yes, J-2 yes, J-3 yes, J-4 yes, rest as recommended"; agent-recorded in the packet, reconfirmed 10-12.
- Why: Ruling accepts the pre-committed packet's Recommendation column item by item.
- Result: PR #788 merged (1d9e3f6); ADR addendum Accepted; P-L1 to P-L3 frozen 8a8d7a0; builds #794, #797, #805.
- Unc.: J-4 rule from coordinator, conditions from lane (both agents); 'rest as recommended' adopts §5 defaults without item-level response.
- Sources: `live-wiring packet:3,21-28,150`; PR #788; git 748afdc, 4edf564

**H3b** · 2026-10-12 · **class 2** — Amend J-4: build gate also opens on Joshua's acceptance of FLOOR-HALF successor screen risk into T15's F1; activation gates unchanged.
- Rec.: None for the amendment. Recommended J-4 rule (`live-wiring packet:84-86`) opened BUILD only on screen GO or Q-SFCLEAR-1 RESOLVED; countersign request 2447cdb and PR #792 omit it.
- Resp.: "confirm J-1 to J-4; amend J-4: the F1 acceptance opens it", to the Deployment Coordinator; agent-recorded in the packet.
- Why: Joshua added an F1-acceptance opening condition absent from the agent-recommended J-4 rule (screen GO or Q-SFCLEAR-1 RESOLVED only).
- Result: Packet amendment `:150-152`; #792 merged 2026-10-12T00:46Z; P-L1 #794, P-L3 #797, P-L2 #805 followed.
- Unc.: Successor coordinator's preceding chat not preserved; if it suggested the amendment, this becomes class 1.
- Sources: `live-wiring packet:84-86,150-152`; git f61ed2a, 2447cdb; PR #792

**H4a** · 2026-10-06 · **class 1** — Accept four-firm re-MC verdict FALSIFIED (early-fail) and consequence: §4 undischarged, candidate (A) closes, next candidate needs fresh operator authorization.
- Rec.: Deployment coordinator acceptance (recorded by coordinator (4), relayed by Joshua), PR #715 comment 6027345046 at 23:29:47Z, contemporaneous with ruling; Claude review CLEAN.
- Resp.: "Accept, merge", Joshua directly to the merge agent, which recorded it (comment 6027352641).
- Why: Agent acceptance was presented with the ruling and Joshua accepted it; stop consequence applies frozen prereg §4 mechanically.
- Result: PR #715 merged (11c6007); withdrawal ADR addendum 2026-10-06; SESSIONS 2026-10-06a; STATE 11-08 row.
- Unc.: The real judgment, the upstream early-fail and fresh-authorization rule, was not origin-traced.
- Sources: `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md:378-384`; PR #715 comment 6027345046; PR #715 comment 6027352641

**H4b** · 2026-10-06 · verification · **class 2** — Hold #715 and require a re-run with bound depth records instead of accepting coordinator (4)'s adjudication of the record-less run.
- Rec.: Coordinator (4) adjudicated FALSIFIED early-fail (`lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md:69`), committed c180283 21:01Z, before the 22:36Z re-run.
- Resp.: Agent report: Joshua held #715, chose a bound-depth-record re-run over the adjudication; run GO to run owner and via deployment coordinator (`RESULTS.md:76`).
- Why: Joshua declined coordinator (4)'s proposed adjudication basis and required stronger evidence (bound depth records) before accepting.
- Result: Re-run reproduced reports byte for byte (b31c6d4); acceptance and merge followed (H4a).
- Unc.: 'Chose ... over' implies presented options; if an agent recommended the re-run itself, this becomes class 1; no record shows who framed it.
- Sources: `lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md:65-76`; `docs/SESSIONS.md:71`; PR #715 commits c180283, b31c6d4

**H5a** · 2026-10-08 · **class 4** — Successor stopping rule: four-strategy-book successor work stops (no further size vector; program re-scoped) if R1/R2 resolution or successor screen confirms pessimistic anchor.
- Rec.: Not located for content: #733 skeleton (6ed1e37) listed generic options only; PR #732 names no proposer; ratification answered a coordinator recommendation recorded after the ruling.
- Resp.: "I agree with your recommendations", ratified in chat to the Deployment Coordinator; agent-recorded (T00 card:512).
- Why: Original ruling venue unrecorded and Joshua does not recall it; presented agent options lack the rule; ratifying words address binding, not content.
- Result: PR #734 merged 2026-10-08T21:02Z.
- Unc.: High: agent-drafted rule later ratified and operator rule written up by agents both fit; first record misstated venue (corrected 20ec3f4).
- Sources: `T00 card:512-522`; PR #734; PR #733 commit 6ed1e37

**H5b** · 2026-10-08 · **class 1** — Successor decision tree: size-feasibility check first; FEASIBLE/CLOCK-DEPENDENT: lift hold, Tier 2, one successor screen; GRID-NO-CLEAR: coordinator recommends stopping uniform-cut successors, Joshua chooses.
- Rec.: Deployment Coordinator recommendation (size-feasibility prereg:307), recorded only post-ruling (d104e13 19:17Z); label semantics in Codex review 6066299443, public 18:20Z, before ruling.
- Resp.: "I agree with your recommendations", to the Deployment Coordinator; agent-recorded (T00 card:524).
- Why: Quoted words accept agent recommendations; an agent record names the tree among them; label semantics predate ruling in public review.
- Result: Size-feasibility run returned FEASIBLE (#745); hold lifted 2026-10-09 (#747); successor screen verdict (#792).
- Unc.: Medium: coordinator's exact recommendation recorded only after the ruling by its recipient; later routing additions were agent-made without operator response.
- Sources: `T00 card:524-532`; `docs/briefs/pre-registration/2026-10-08-tradeify-size-feasibility-prereg-DRAFT.md:307`; PR #735 comment 6066299443

**H5c** · 2026-10-08 · **class 1** — Define 'confirms the pessimistic anchor': H2 pessimistic result fails A6 ceiling, or accepted R1/R2 resolution shows >half of resolved UNDETERMINED paths busting.
- Rec.: Deployment Coordinator definitions (86fbfe0, 19:26Z) and independent Claude review threshold suggestion (6067496045, 19:30Z), both before confirmation 6a6a45c at 19:33Z.
- Resp.: "go with your recommendation for 1", in chat to the Deployment Coordinator; agent-recorded (T00 card:544).
- Why: Definitions and threshold exist in agent text before the ruling; Joshua names the threshold as the agent's recommendation.
- Result: Commit 6a6a45c; coordinator note on PR #734 (comment 6067558481).
- Unc.: 'Resolved' qualifier absent from the public suggestion, presumably from coordinator chat; which question 'for 1' answered is the recorder's reading.
- Sources: `T00 card:533-544`; PR #734 commits 86fbfe0, 6a6a45c; PR #734 comment 6067496045

**H5d** · 2026-10-08 ET (PR body says 2026-10-09) · **class 4** — Midpoint clarification of (b): test: H2 agreed-bust share plus half H2 UNDETERMINED share, exact; tightened bracket reads confirmed, not confirmed or undecided.
- Rec.: None located before the ruling; PR #741 opens with Joshua's instruction, first commit ef6c54b Claude co-authored; clarification text author unknown.
- Resp.: "add the clarification under definition (b) on the T00 card", in chat to the Deployment Coordinator; agent-recorded (T00 card:536).
- Why: 'The clarification' refers to earlier-discussed text whose author, agent or Joshua, is unrecorded.
- Result: PR #741 merged (7aa2fb9, 2026-10-09T00:15Z).
- Unc.: Likely agent-drafted in chat, not shown; reviewer read interval branches as beyond Joshua's quote; date differs between PR body and card.
- Sources: `T00 card:536-542`; PR #741; PR #741 commit ef6c54b

**H5e** · 2026-10-08 ET (commit 2026-10-09T00:13Z) · **class 1** — Midpoint replaces resolved-subset denominator under partial resolution; unresolved paths bracket both ends; after 'Not confirmed', screen judged on tightened bracket's pessimistic end.
- Rec.: Independent Claude review 6071496034 (PR #741, 00:05Z) proposed both; coordinator folded them in 26c5c02 (00:13Z) with Joshua's permission.
- Resp.: "yes you may" to the amendments, in chat to the Deployment Coordinator; agent-recorded (T00 card:536).
- Why: Amendments came from an agent review; coordinator chose among its options; Joshua's permission accepts them unchanged.
- Result: PR #741 (7aa2fb9); re-check CLEAN at 26c5c02 (6071593661).
- Unc.: Unrecorded whether Joshua saw committed wording or a chat summary; reviewer asked Joshua to pick, but coordinator picked and Joshua permitted.
- Sources: `T00 card:536-542`; PR #741 comment 6071496034; PR #741 commit 26c5c02

**H5f** · 2026-10-08 · **class 4** — Hold the new H, P7 re-run and Tier-2 source approval while tree step 1 is pending; only Tier-2 capability PR exempt.
- Rec.: None located (T00 card §8, PR #734/#735 comments, SESSIONS 2026-10-08a); Codex review 6066299443 at 18:20Z already called it an existing operator hold.
- Resp.: Agent report: T00 card:545 attributes the hold to Joshua, 2026-10-08, without his words.
- Why: Attributed to Joshua without quote or prior recommendation; prior agent 'operator hold' reference is consistent with, not proof of, operator origin.
- Result: Recorded 20ec3f4; lifted 2026-10-09 on FEASIBLE (#745) via #747.
- Unc.: Hold appears to predate the tree, so probably not among ratified recommendations; origin still unrecorded.
- Sources: `T00 card:545-549`; `docs/SESSIONS.md:61`; PR #735 comment 6066299443

**H6a** · 2026-09-04 (UTC; recording commit 09-03 ET) · **class 3** — D20 acceleration: deploy the book on the live Tradeify eval at Phase 3 commit if sizing works together and MC bust <5%.
- Rec.: None located: pre-D20 campaign-state and plan at ef8b7aa contain no acceleration or early-deployment proposal; plan ended at Phase 7 CONFIRMED.
- Resp.: "I want to speed this plan up significantly ... I want to deploy the book on Tradeify."; agent-recorded (campaign:1079-1081).
- Why: Joshua's words introduce a choice absent from the agent-designed plan and every presented option.
- Result: §15 recorded in PR #295 (merged 2026-09-04T21:33Z); §15d sub-rulings; panels refreshed (#296).
- Unc.: Preceding chat not preserved; record dates it 2026-09-04 UTC but recording commit falls on 09-03 ET.
- Sources: `campaign:1077-1081,1124`; PR #295; commit 1d70502

**H7a** · 2026-09-11 · **class 1** — Track B release (TB-G0): twelve orchestrator-default D-B items: bounded HOLD release, dedupe GO at M1 RESOLVED, bounded Phase-8 emit GO (never arm).
- Rec.: Orchestrator umbrella §0.5 'Recommended default' column, revisions 7 and 8 (02:07Z, 02:21Z; rev 8 68610e6), before the 03:33Z ruling.
- Resp.: Agent report: "Recorded on the operator's instruction to apply sensible defaults" (PR #336 comment 5629047943).
- Why: Every listed item had a written default before the ruling, and the ruling adopts them.
- Result: Campaign §55, umbrella rev 10 (ec57e83), BOUNDED RELEASE; PR #336 merged 2026-09-11T04:56Z.
- Unc.: Joshua's words paraphrased, not quoted; ruling comment is an agent relay from the shared account.
- Sources: `campaign:3832-3856`; PR #336 comment 5629047943; umbrella rev 68610e6

**H7b** · 2026-09-11 · **class 1** — D-B4 (a): single-candidate confirmation of exactly the accepted four-strategy book, K=1; any failed screen or bound ends the attempt.
- Rec.: Orchestrator umbrella rev 7 (ee80bb7, 02:07Z) D-B4 default "(a)", before the 02:20Z ruling.
- Resp.: Agent report: comment headed 'Operator ruling' states "D-B4 = (a), single-candidate confirmation" (PR #336 comment 5628479176).
- Why: Ruling selects the recommended default, present before it.
- Result: Revision 9 (303ddbb, Codex) removed fifth-leg and runner-up branches; campaign §55:3845.
- Unc.: Comment author cannot be established from the shared account; added directives are consistent with the recommendation.
- Sources: PR #336 comment 5628479176; umbrella rev ee80bb7; `campaign:3845`

**H7d** · 2026-09-11 · risk criteria · **class 4** — D-B8: force-close priority Aegis 6J, Striker MYM, Vanguard MGC, ORB MNQ; whole legs close lowest priority first; unconfirmed close refuses Aegis entry.
- Rec.: None: revision 8 gave no default ("...live-risk semantic; the orchestrator escalates rather than guesses") and listed guessing the order as forbidden.
- Resp.: Agent report: semantic "already the operator's recorded selection" (09-10); "Confirmed ... this explicit list replaces it" (PR #336 comment 5629047943).
- Why: Semantic traces to untraced 09-10 operator selection; explicit order first appears in an agent ruling under blanket 'sensible defaults', chooser unrecorded.
- Result: Campaign §55:3849; TB-S1 (E) atomic takeover.
- Unc.: High: if the recording agent chose the order, an agent filled a live-risk item its own plan forbade guessing.
- Sources: PR #336 comment 5629047943; umbrella rev 68610e6 §0.5 D-B8; `campaign:3849`

## Agent-decided under delegation (outside the four classes)

- **D4i (2026-09-30):** the X-1 scoped PASS was a coordinator evidence decision by the reviewing Codex session, made under Joshua's instruction to review and record the run. No operator acceptance of the PASS is recorded. Source: `docs/notes/2026-09-26-tradeify-route-drill-plan-draft.md` (X-1 acceptance).
- **H6b (2026-09-04):** the orchestrator narrowed D20 so that the earliest deployment is the later of M1 item 5 and Phase 8 parity. No operator response was recorded at the time. Source: `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md:201`.

## Next batch (not classified)

- 2026-09-10: the four-strategy book selected. Source: `docs/notes/2026-09-10-tradeify-protection-selection.md`.
- 2026-09-12 and 09-20: campaign ownership moved to Astra (campaign §57), then back to the coordinating task (§58).
- 2026-10-10: operator HOLD on the growth study. Source: `docs/briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md:381`.
- 2026-09-01: F1 reversed. Source: `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md`.
- 2026-09-05: Striker expressions readmitted. Source: `docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md`.
- 2026-09-05: S2 plan revision. Source: campaign `:1124`.
- 2026-09-30: operator-directed agent orders. Source: surface ADR addendum 2026-09-30b.
- 2026-10-02: sitting-2 GC-2b edition rulings. Source: `docs/notes/2026-09-26-tradeify-bd-decision-packet.md:141`.
- 2026-10-07: first VM exception. Source: campaign §60 `:4066`.

Checking that a recommendation preceded a ruling dated before 2026-10-08 needs GitHub or a full clone.
