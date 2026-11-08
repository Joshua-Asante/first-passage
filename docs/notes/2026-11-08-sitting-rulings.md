# 2026-11-08 sitting: rulings

Joshua ruled on 2026-11-08, in the Claude session that prepared the sitting. The options and reasoning
are in [the options packet](2026-11-08-sitting-options.md). Claude and Codex reviewed the packet
independently in #1120. Joshua accepted the eleven rulings where they agreed. Claude settled the
disputed ones at his direction, and he accepted them, with D14 = A and the D16 risk accepted ("D14 A,
accept D16 risk, record all rulings").

**Reconciled with the 11-06 and 11-07 rulings.** The packet was cut from the record as of 11-05/06
and missed rulings Joshua made in other sessions on 11-06 and 11-07: the
[design spec](../spec/2026-11-06-orb-aegis-eval-build-design.md), the
[attended-session procedure](../spec/2026-11-07-orb-aegis-attended-session-procedure.md) with its F
rehearsal, the candidate-bar overturn and the 11-07 priority rule (STATE). Six rulings conflicted or
were overtaken. Joshua accepted Claude's reconciliation for all six ("accept all recommendations"),
and the text below already reflects it:

1. **D6:** the first session does not wait for Tradeify's source-review reply (11-06 spec).
2. **D9:** the F rehearsal is this week's trade; the D9 shape starts the week of 11-16.
3. **D12:** one GO per session (STATE, 11-06), within AGENTS.md's 7-day window.
4. **D17, D18:** new candidates and builder rounds are allowed under the 11-07 priority rule.
5. **D1:** the 11-07 pair-evidence verdict ("prior stands") is named as accepted risk.
6. **D8:** stands as ruled.

Overtaken: **D19** (the c1 code and Fly guards were already removed) and part of **D5** (S-PAIR was
accepted on 11-06, and the 11-06 GO covered the eval build).

Citations: "CK" is `docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md` at `f96a657`.
Other deleted docs are cited at `b7eaff7`. Private facts are named, never recorded: "confirm locally".

## Weekly preservation trade (from the week of 11-09)

**D8. Who places it.** Joshua places the weekly preservation trade by hand, on his own normally
logged-in device, with no VPN or VPS. Agents may remind him and may check, read-only, that the account
is flat with no working orders. No agent (Codex included) places, changes, cancels or exits an order
on the eval. This holds until Joshua re-rules after Tradeify's written answer to Q5 (D10); the answer
alone, yes or no, does not lift it (Joshua, 11-08).
It suspends the standing preservation-trade GO of 2026-10-25 and, for eval orders, rule-1 directed
agent acts. Rule-1 directed authority stays for other acts. No "sole owner and operator" attestation
goes to Tradeify until Q5 is answered or he rules on it. Inactive accounts are deleted "after an email
warning" (`b7eaff7:docs/notes/2026-11-01-prop-firm-venue-fact-register-DRAFT.md:202`), so a missed
week is not immediately fatal. AGENTS.md money control 1 and STATE are updated in the same PR as this
record.

**D9. Its shape (T1).** **Week of 11-09:** the trade is the F rehearsal under the 11-07 procedure
(§10): MNQ at about 16:15 ET, with a resting stop and a flatten-and-cancel exit, placed by Joshua.
Joshua's own hand placement needs no agent GO: this ruling meets procedure §10 step 0, and §10's
standing-GO references read as Joshua's own placement while D8 holds.

**From the week of 11-16**, the trade is one genuine minimal trade per Mon–Fri week. So that each one
adds an F sample (procedure §10), it uses MNQ and exits by flatten-and-cancel in Tradovate web, then
verify:

- 1 micro, with a normal market or limit entry;
- a protective stop placed with the entry and cancelled with the exit, as default practice (not a compliance condition);
- held for minutes, not seconds;
- entered and exited before the 16:45 ET flat-by, away from scheduled high-impact releases;
- ending flat with no working orders, which Joshua confirms.

It is placed only while no Aegis or ORB instance is enabled. It is never placed while the account, or
any other account Joshua controls, holds an opposite position in the same product group. Once armed
sessions produce fills, those fills satisfy the week, and the minimal trade runs only in weeks without
them.

Before the first armed session, the signed page names the preservation trade as explained activity:
its instrument, its window, and the fact that it is placed with instances disabled. This is needed
because a manual MNQ or 6J fill is a §6.8 incident for the instance that owns that instrument
(CK:1093), and a fill on neither instrument is a stop (CK:1094).

This ruling settles the trade's shape. It does not settle T1: whether Tradeify accepts the shape stays
open (CK:1103).

**D10. Ask Tradeify.** After the F rehearsal, Joshua sends one message himself. It goes on a
separate compliance ticket, never on the CME-copied thread #04738415, and asks for a written answer
from a human:

- Q5: may an AI assistant, acting under his sole direction, place an order he has specified, through
  the platform UI on his own logged-in PC?
- The question about evaluation-account expiry, if the dashboard is silent on it.
- Optionally, whether the D9 shape is compliant with ESA §6.5 and §6.9.

Silence is not approval. Nothing relies on a reply for 11-09 → 11-13.

## Eval path

**D1. Evidence case.** For the first forward attempt on the owned Select 100K (eval stage only), no
pre-session statistical evidence case is required. The pair's own pre-registered gate is the 10-31
forward stop rule plus Addendum 1, unchanged. For this attempt, this supersedes the recorder text that
the pair "needs its own evidence case" (CK:1023). Accepted as risk on the signed page:

- the 10-19 prior;
- the exploratory composition-grid signal;
- the workshop finding that no out-of-sample edge is established;
- that no O-N or model evidence transfers to O-0;
- the 11-07 pair-evidence verdict: the current pair fails the 2026-08-26 combined-book gate at the
  eval's sizing, "prior stands"
  (`lab/analysis/c1/pair_evidence_case_2026-11/RESULTS.md`). That file's own status (Codex
  verification, then Joshua's ruling on it) is separate from this acceptance.

A bust ends the attempt, and any reset is a fresh spend decision. This sets no precedent for scaling
or new purchases. The funded stage needs a new binding.

**D2. Nomination.** The draft native-lane framework does not gate the owned-100K attempt. The
nomination is Aegis A-0 and ORB O-0, as the stop-rule registration names them (:3), with the
expressions recorded in the signed cards (`docs/evidence/PRIVATE_EVIDENCE.sha256:421`, `:427`; T00
trial 13). The ORB horizon edition substitutes only through Addendum 1. A one-line "does not gate the
owned-100K attempt" pointer is added to the framework's status line, via a Codex-reviewed PR because
it is a gate document. Repair or retirement of the framework waits until a scaling or purchase
decision needs a gate.

**D3. Account binding.** Bind both strategies to the owned Select 100K, eval stage only, with every
limit the build implements set as in the frozen set (spec D7). The binding states:

- an edition-swap clause tied to Addendum 1;
- that only Aegis and ORB are bound;
- the preservation-trade placement rule (D9).

Joshua signs the binding with build hashes on the signed page. The native DD tier runs under an
**explicit exception, not an admission**. Admission means a re-MC, a regime gate and an admitting ADR
(`core/dd_geometry.py:25-39, 87-101`). The tier is stated as built, is not changed after S-PAIR, and
its unadmitted status is accepted as risk on the signed page. Admission is owed before any scaling.
Money control 4 is untouched.

**D4. Exclusivity.** Joshua signs, in public:

> "Neither Aegis nor ORB — their released NinjaScript implementations, editions and successors, and
> the same logic on any instrument — is run or planned at any other prop firm while it runs at Tradeify."

This is an interim bar. T-1105, a later written answer attributed to an AI agent, reopens the 11-04
"a different instrument counts as distinct" ruling under that ruling's own clause. Joshua re-rules it
after a human compliance answer. A different-logic strategy elsewhere is permitted, but it is exposed
to Tradeify's "similar orders" scan and ESA §6.7 (T3). Any question about this goes on a compliance
ticket, not on #04738415.

**D5. Native build authority.** Joshua accepted S-PAIR on 11-06, and his 11-06 GO covers the eval
build only: no order, session or spend (STATE). From 11-08 the enumerated authority is:

1. any S-PAIR rerun on Sim101;
2. the eval build, compiled from the frozen set in the 11-06 design spec and installed disabled under
   its GO;
3. the horizon edition build and its Sim101 canary.

No canary runs during an armed session. Verification of the private eval build follows AGENTS.md
Roles: Codex reads the frozen build read-only, in place, against its checksums (Joshua, 11-06).
Hash identity is also checked before install: the installed build equals the frozen set, which equals
the source sent to Tradeify; otherwise the source is re-sent. Earlier native builds and canaries not
covered by a recorded ruling are ratified as of 11-08.

**D6. Tradeify source review.** The first session does **not** wait for Tradeify's source-review
reply (11-06 spec; STATE). Starting without it stays an accepted risk on the signed page (CK:1103).

- **Notice:** optional. Joshua may send Tradeify a notice of intent ("I will enable the strategy whose
  source I sent on <date>; I will record the enable on video and keep platform logs"), without copying
  CME. It sets no waiting period.
- **Objection:** a Tradeify objection received at any time stops the attempt until Joshua re-rules.
- **Eligibility:** the candidate-specific ownership prerequisite (native plan :57) is set aside on the
  signed page, with the risk named.
- **Re-send:** any eval-build change is re-sent to Tradeify by Joshua before it runs on the eval.
- **Export:** settle the export question (D7) before the eval files go out.
- **After session 1:** a change to signal logic, entries, exits, stops, sizing, caps, DD behaviour,
  instrument or session, pair composition, the outcome window, or a stop-rule assumption needs a new
  registration before the next eval session. A fidelity fix that leaves all of those unchanged needs
  an S-PAIR rerun and a re-send. Documentation, diagnostics and UI-only changes need ordinary
  verification. Addendum 1 stays the only registered horizon-edition substitution.

**D7. Data rights and CME licence.** Four things happen. None of them gates session 1, except items
2 and 3, which must be done before session 1.

1. Joshua follows up on CME ticket #04738415, citing Tradeify's CQG confirmation, and re-asks
   NinjaTrader/CQG for the legal distributor, the subscriber agreement and the Managed User route.
2. Before session 1, Joshua confirms locally which subscriber agreement the eval login accepted.
3. Before session 1, the build is confirmed to make no external calls and export no market-data series.
4. The CME licence category is treated as contested risk, with a pay-or-stop trigger.

Feature lists derived from the private source stay in Joshua's checkout and never reach Codex or the
repo. A licence purchase needs money-control-6 approval.

**D11. Native plan scope.** The 11-05 path governs the owned Select 100K. The draft native plan and
draft framework do not gate it. "Fund the expanded assessment" referred to the expanded P1, a $0
read-only check. It is ruled overtaken, because its entitlement content is covered by D7. No P2–P7
phase and no fee budget.

The spend ceiling stays, as re-homed to the account's private owner record by the 11-03 ruling
(`b7eaff7:docs/adr/2026-07-17-c1-rail-build-account-registration-go.md:517-521`). The first attempt
plans no incremental spend. Any licence, reset, second account or paid data needs an approved amount
under money control 6, checked against the ceiling. Joshua confirms locally the ceiling's scope for
the native lane and what happens on breach.

**D12. Sequencing and GO cadence.** One GO per session (STATE, 11-06), each within AGENTS.md's
7-day window. Build and session GOs stay separate acts. Session 2 runs only after the session-1 review
is recorded.

Order of steps (main's 11-06 spec and 11-07 procedure):

1. paper rulings;
2. S-PAIR: run and accepted on 11-06, with no rerun (spec §7);
3. name readback, then the build installed disabled under the 11-06 build GO;
4. the F rehearsal (procedure §10);
5. a short Sim101 check of ORB on the frozen set;
6. the eval files to Tradeify;
7. the signed, hash-registered page and the attended pre-session check;
8. the session GO; Joshua enables the strategy himself.

The signed page lists:

- the binding (D3);
- the evidence acceptance (D1) and the nomination (D2);
- the exclusivity statement (D4);
- what S-PAIR showed;
- the CK:1103 acceptances: no reply, CME licence, T1, T2;
- candidate-specific eligibility (D6) and starting without Tradeify's reply;
- the 11-07 pair-evidence verdict (D1);
- the unproved native-control risks (protection across a disconnect, and the U tests Sim cannot
  prove), with the automatic incident close not relied on (CK:1090);
- the attending operator's account-wide duties (CK:1095);
- the preservation-trade rule (D9);
- the review-before-session-2 rule;
- who flattens and disables on a Tradeify objection.

## Research and records

**D13. Clause 2-A.** Not fired: 0 of 3 campaigns. Retired by Joshua's judgment that it is no longer
useful (cf. 5675d8c), not as unreachable. It re-arms before the first admission if harvest intake or
Path-1a is ever reactivated.

**D14. Clause 2-C.** Ruled **FIRED** at its 11-08 check. Its remedy is enacted (option A), in a code
PR (Codex-clean head, green CI):

- **Re-bank:** ORB `orb_mnq_intraday_breakout` goes from K 0 to 1, and ST-EH `st_eh_supertrend_grid`
  from 2 to 84. Each manifest gets a provenance field. `executed_looks` stays byte-identical.
- **Verdicts:** fix the verdict text of the ORB manifest and both TXG1 manifests. Fix the MNQ and MYM
  bank lines. The owners re-sum.
- **register_search:** operator-stopped closes bank declared K, and its tests are updated.
- **Superseded:** Joshua expressly supersedes the 08-18 line "ORB Ruling 1 (`executed_k=0`) still banks 0".
- **No ST-EH exception:** promotion packets backed by ST-EH carry the K-conditional DSR-floor
  attestation as coded (`lab/discovery/promotion_packet.py:205-225`).

D15's retirement does not cancel a falsifier that has already fired. Codex preferred recording it as
history only (option H); Joshua chose A.

**D15. Obligations in deleted docs.** Obligations recorded only in docs deleted by 5510ca9 retire,
going forward only, except these named survivors:

- the 11-05 eval path (CK:1085-1103), and the pilot runbook as it amends it;
- the T1, T2, CME-licence and start-without-a-reply reservations;
- the 11-03 rulings as decisions;
- the c1 Stage 2/3 rulings;
- the 2026-10-18 ORB v7 S4 ratification;
- whatever kept files and code carry: frozen pre-registrations, the stop rule, `lab/builder/README`
  obligations, and dated HOLDs in `ops/instruments`.

AGENTS.md governs any conflict. STATE points to rulings but cannot settle a ruling reserved to Joshua.
A falsifier that fired before retirement keeps its remedy (D14). The 11-03 checks carried to
2027-02-08 retire with their deleted owners unless a kept file or code carries them.

**D16. Data source.** Research data is TradingView CME exports only. CSVs stay local and are never
committed (SHA256SUMS only). TradingView is never used as a feed, alert transport or automation.
Databento stays retired, and there is no spend. This covers the research corpus only, not NinjaTrader
platform data inside NinjaTrader. **Risk accepted by Joshua:** TradingView's terms license data for
display-only use and bar machine-driven, non-display use (§3), with automatic termination (§12).
Offline backtests on exported bars sit on the wrong side of that text. The plausible consequence is
loss of the TradingView account. MNQFLOW stays parked: it wakes only on a historical MBP-10 source for
its registered window.

**D17. Third-leg Experiment 1.** The 10-29 card is withdrawn, not repaired. Fix the native plan's
:129 link. New third-leg research may run under Joshua's 11-07 priority rule for new candidates
(STATE). A third leg on the eval needs its own authority beyond the CK:1091 pair exception.

**D18. Builder.** Builder rounds are allowed under Joshua's 11-06/07 candidate-bar overturn and the
11-07 priority rule (STATE). A per-instrument look budget is not the liveness ceiling: each round's
registration declares an audited, channel-level ceiling that does not grow with new instruments or
calendar extensions, plus the owed contract fields, before it freezes. MGC is parked (Joshua, 11-06),
results unread, and its 8 ledgered cards are disclosed as K. MCL is parked (11-05); R1 validity is
not adjudicated, and its 8 cards count toward MCL K. The 2009 calendar enlarges no ceiling.

**D19. c1 Stage 3.** Overtaken: the c1 rail code, both `fly.toml` files, `LIVE_FLY_APPS` and
`rail.deploy` were already removed (#1122 / f901f726, #1152). Remaining: Joshua checks the c1 volume
archives locally, and agents neither open nor copy them. If they contain Pine, runtime ports or
`effective_inputs.json`, he accepts the single copy or grants an explicit backup exception. If they
hold account data only, he may make a private backup.

**D19 closed (Joshua, 11-08, "go ahead with 1a and fix the comments").** S3-4: `ops/c1_rail/book_policy.py`
stays where it is, as the offline replay law; it is not moved or renamed. `ops/c1_signal_daemon/` stays
because the private ports import it and `core/strategies/BOOK_SOURCES.sha256` pins that path.
`core/dd_geometry.py` stays (D3). The two `core/firm_rules.py` comments that cited deleted c1 files now
say those files were removed with the rail, last at b7eaff7; comment text only, no values (money
control 4 approval given). D19 is complete apart from Joshua's local archive check.

**D20. Subscriptions.** Keep the monthly reconfirm, by 11-21. If time allows, close the stale rows
(Tradeify carrying cost, Fly.io final bill, final charges) and fix links to deleted records.

## Follow-up work

Every PR, doc-only included, merges only at a head the other agent has reviewed clean, with CI green,
and Joshua merges (AGENTS.md).

| Item | PR |
|---|---|
| AGENTS.md money control 1 and Roles, and STATE (D8, D9, D12) | This PR |
| D14 re-bank, verdicts, `register_search` and tests | #1163 |
| D2 framework status pointer | #1164 |
| D18 builder README, MGC/MCL K disclosures; D17 plan link; D20 ledger links | #1165 |

## Joshua, locally

- **D7:** which subscriber agreement the eval login accepted.
- **D11:** the spend ceiling's scope and what happens on breach.
- **D19:** the contents of the c1 archives.
- **Generally:** what the signed cards contain, and any Tradeify, CME or NinjaTrader replies.
