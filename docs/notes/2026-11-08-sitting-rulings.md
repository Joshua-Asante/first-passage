# 2026-11-08 sitting: rulings

Joshua ruled on 2026-11-08, in the Claude session that prepared the sitting. The options and reasoning
are in [the options packet](2026-11-08-sitting-options.md). Claude and Codex reviewed the packet
independently in #1120. Joshua accepted the eleven rulings where they agreed. Claude settled the
disputed ones at his direction, and he accepted them, with D14 = A and the D16 risk accepted ("D14 A,
accept D16 risk, record all rulings").

Citations: "CK" is `docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md` at `f96a657`.
Other deleted docs are cited at `b7eaff7`. Private facts are named, never recorded: "confirm locally".

## Weekly preservation trade (from the week of 11-09)

**D8. Who places it.** Joshua places the weekly preservation trade by hand, on his own normally
logged-in device, with no VPN or VPS. Agents may remind him and may check, read-only, that the account
is flat with no working orders. No agent (Codex included) places, changes, cancels or exits an order
on the eval. This holds until Tradeify answers Q5 in writing (D10) or Joshua re-rules in his own words.
It suspends the standing preservation-trade GO of 2026-10-25 and, for eval orders, rule-1 directed
agent acts. Rule-1 directed authority stays for other acts. No "sole owner and operator" attestation
goes to Tradeify until Q5 is answered or he rules on it. Inactive accounts are deleted "after an email
warning" (`b7eaff7:docs/notes/2026-11-01-prop-firm-venue-fact-register-DRAFT.md:202`), so a missed
week is not immediately fatal. AGENTS.md money control 1 and STATE are updated in the same PR as this
record.

**D9. Its shape (T1).** From the week of 11-09, the trade is one genuine minimal trade per Mon–Fri week:

- 1 micro, with a normal market or limit entry;
- a protective stop placed with the entry and cancelled with the exit, as default practice (not a compliance condition);
- held for minutes, not seconds;
- entered and exited in RTH, away from scheduled high-impact releases, and well before the 16:45 ET flat-by;
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

**D10. Ask Tradeify.** After the first minimal trade, Joshua sends one message himself. It goes on a
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
- that no O-N or model evidence transfers to O-0.

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
limit the build implements set before the S-PAIR rerun. The binding states:

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

**D5. Native build authority.** Joshua records the private ruling that authorised the native build and
the Sim101 canaries, by date and words (A). If he cannot name it, native builds, canaries and S-PAIR
runs before 11-08 are ratified as of today (B). From 11-08 the authority is enumerated:

1. the S-PAIR bare rerun on Sim101;
2. the eval build, compiled from the accepted S-PAIR source set and installed disabled under the step-3 GO;
3. the horizon v2 build and its Sim101 canary.

No canary runs during an armed session. The substitute for Codex review of the private eval build is
done before install. It is (a) a fresh-context Claude review in place in Joshua's primary checkout,
and (b) hash identity: the installed build equals the S-PAIR source set, which equals the source sent
to Tradeify. If those don't match, the source is re-sent with a fresh notice (D6). Which option
applies, A or B, depends on a private fact: confirm locally.

**D6. Tradeify source review.** Joshua sends Tradeify a notice of intent, without copying CME:

> "Unless Tradeify objects by <date>, I will enable the strategy whose source I sent on <send date>.
> I will record the enable on video and keep platform logs."

- **Deadline:** 2026-11-19 17:00 ET if the notice goes out by 11-10. Otherwise 7 business days after
  sending, never inside Thanksgiving week.
- **Session 1:** waits for the deadline or a reply.
- **Objections:** the notice invites objection on any ground, eligibility included. An objection stops
  the attempt. Silence by the deadline lets Joshua set aside the candidate-specific ownership
  prerequisite (native plan :57) on the signed page, with the risk named.
- **Re-sends:** a re-send before session 1 needs a fresh notice and restarts the window.
- **Export:** settle the export question (D7) before sending.
- **After session 1:** a change to signal logic, entries, exits, stops, sizing, caps, DD behaviour,
  instrument or session, pair composition, the outcome window, or a stop-rule assumption needs a new
  registration before the next eval session. A fidelity fix that leaves all of those unchanged needs
  an S-PAIR rerun, a re-send and a fresh notice. Documentation, diagnostics and UI-only changes need
  ordinary verification. Addendum 1 stays the only registered horizon-edition substitution.

**D7. Data rights and CME licence.** Four things happen. None of them gates session 1, except that
the build checks must pass first.

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

**D12. Sequencing and GO cadence.** Weekly GO cadence governs, per Joshua's 11-05 ruling
(`a16270d`), which is later than CK:1101. Build and session GOs stay separate acts. Session 2 runs
only after the session-1 review is recorded, and an adverse review suspends the rest of that week's
GO automatically. Joshua confirms that the 11-05 cadence ruling covers eval sessions.

Order of steps:

1. paper rulings;
2. S-PAIR rerun and acceptance;
3. step 3: name readback, then the build GO, with the build installed disabled;
4. step 4: the signed, hash-registered page and the attended pre-session check;
5. step 5: the session GO, after the D6 deadline or a reply. Joshua enables the strategy himself.

The signed page lists:

- the binding (D3);
- the evidence acceptance (D1) and the nomination (D2);
- the exclusivity statement (D4);
- what S-PAIR showed;
- the CK:1103 acceptances: no reply, CME licence, T1, T2;
- candidate-specific eligibility (D6);
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

**D17. Third-leg Experiment 1.** Deferred until after the first eval sessions and their review. The
10-29 card is withdrawn, not repaired. Fix the native plan's :129 link. A plain local inventory ($0,
K=0, no card) runs only if Joshua directs it. A third leg needs its own authority beyond the CK:1091
pair exception.

**D18. Builder.** No per-instrument look budget as the liveness ceiling. `lab/builder/README.md`
records the channel as dormant. No round opens until a registration declares an audited,
channel-level ceiling that does not grow with new instruments or calendar extensions, plus the owed
contract fields. MGC is parked, following "Park MCL", with results unread. R1 validity is not
adjudicated; it is moot while MCL is parked, and its cards count toward MCL K. The 2009 calendar
enlarges no ceiling.

**D19. c1 Stage 3.** The surface-ADR "own GO and quiet window" clause lapses. Removing
`LIVE_FLY_APPS` and `rail.deploy` needs a Codex-reviewed clean head and green CI. The Stage 3
conditions hold:

- both `deploy/*/fly.toml` files, `LIVE_FLY_APPS` and `rail.deploy` leave together in the last S3-2 PR;
- each PR's executed consumer scan gives every outside consumer a disposition (ADR :506, :512);
- S3-4's destination returns with the consumer table.

Joshua checks the c1 volume archives locally, and agents neither open nor copy them. If they contain
Pine, runtime ports or `effective_inputs.json`, he accepts the single copy or grants an explicit backup
exception. If they hold account data only, he may make a private backup.

**D20. Subscriptions.** Keep the monthly reconfirm, by 11-21. If time allows, close the stale rows
(Tradeify carrying cost, Fly.io final bill, final charges) and fix links to deleted records.

## Follow-up work

| Item | Route |
|---|---|
| AGENTS.md money control 1 and STATE (D8) | This PR, at a Codex-clean head with green CI |
| D14 re-bank, verdicts, `register_search` and tests | Code PR, at a Codex-clean head with green CI |
| D2 framework status pointer | Gate document, at a Codex-clean head |
| D18 builder README, MGC.md, MCL K disclosures | Doc-only |
| D17 plan link, D20 ledger links | Doc-only |
| D19 last S3-2 PR | Code PR, at a Codex-clean head with green CI |

## Joshua, locally

- **D5:** the date and words of the private build ruling.
- **D7:** which subscriber agreement the eval login accepted.
- **D11:** the ceiling's scope and what happens on breach.
- **D12:** confirm the 11-05 cadence ruling covers eval sessions.
- **D19:** the contents of the c1 archives.
- **Generally:** what the signed cards contain, S-PAIR status, and any Tradeify, CME or NinjaTrader replies.
