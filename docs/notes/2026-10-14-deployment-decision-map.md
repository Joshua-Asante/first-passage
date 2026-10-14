# Deployment choices: start here (2026-10-14)

Derived navigation map at `main` `4ca81af941df14909790ef7108bea3fd77603c60`.
The linked owners govern; this map records their scope, not new decisions.

| Choice | Current standing and authoritative scope |
|---|---|
| Strategy expression | **Personal study decided:** [Q-SFCLEAR-3 §S](../briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md) is frozen at F₃ `15bea250fc8ee9a57b59735c9e8be685c4ddbf22`; it incorporates [Q-SFCLEAR-2 at F₂, §§1–2](https://github.com/Joshua-Asante/first-passage/blob/83867f0d362931c2a516a62b990bb1c209372527/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md). Locked Pine/accepted ports and effective inputs remain unchanged; R1 keeps Aegis base, disables Striker/Vanguard adds and disables ORB. This is not the full declared book. Q-SFCLEAR-2 is superseded before run, not a clearance verdict. |
| Personal / prop accounts | **Decided for first deployment:** personal Tradovate; one account at a time. [Personal ADR, October 11b](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11b--tradeify-book-reused-on-the-personal-lane-supersedes-the-option-c-split) supersedes the earlier strategy split. Before either-direction switching, including weekly preservation trades, prove outgoing account flat, no working orders and no delayed-entry path. Concurrent operation needs a separate safeguard and Joshua's ruling. |
| Tradeify work | **Suspended:** [checklist, October 13](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-13--track-b-suspended-11-08-decision-rules-draft) freezes Tradeify-specific build/spend; personal work and weekly preservation continue. The November 8 decision rules are draft. Earlier accepted engineering and verdicts retain their original scope. |
| Execution route | **Unresolved for deployment:** [Tradeify route record, October 12 addenda](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#addendum-2026-10-12--tradeify-support-rejects-bridge-routes-for-evaluation-accounts) records support's evaluation/sim-funded bridge/API rejection and later native-logic requirement; it does not prohibit the personal lane. [CrossTrade retention](../pursuits/SUBSCRIPTION_LEDGER.md) is a subscription decision, not a choice over direct Tradovate. The book owner still returns `production_route_unavailable` without a synthetic broker ([runtime](../../ops/c1_rail/book_account_owner.py)); implemented replay/controls do not establish an approved production route. |
| Attendance | **Current first-release requirement:** [personal plan §8](2026-10-11-personal-clearance-plan-tradeify-book.md#8-live-path-to-an-attended-armed-personal-session) and [halt/resume §§3–4](../spec/2026-09-14-tb-s3-halt-resume-contract.md) require attended operation and session authority. [Attention proposal §6](2026-10-11-tradeify-operator-attention-proposal.md#6-decisions-for-joshua) approves O1 preparation only; reduced checking effort is not unattended permission. Unattended operation is a separate unresolved change from concurrent accounts. |
| Order splitting / protection | **Tradeify-scoped candidates:** [ORB/Striker successor](../briefs/pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md) and [Vanguard fixed-stop successor](../briefs/pre-registration/2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md) remain unfrozen within the suspended lane. Their one-contract entry requests, fixed-stop/no-modify expressions and whole-leg close directions are not personal R1 rules or automatic requirements at another venue. Prospective request-count/order envelopes describe a proposed expression; they are not measured rate, latency, stop-coverage or execution bounds. Qualification belongs to the exact route/edition. |
| Sizing | **Personal R1 decided for study:** F₂ §§1–3 as incorporated by F₃ bind P0 (normal mode plus the live 15% halt), the existing 80-micro cap, quantity laws and private tuple. Clearance and live wiring remain gates. Full declared quantities, FLOOR-HALF and personal R1 are distinct. Alternative-venue size suggestions and drawdown extrapolations in the [assessment](2026-10-14-funded-venue-alternatives-assessment.md) are research, not a selected tuple or measured clearance at that venue. |
| Session deadlines | **Current rule:** [TB-S3 §5](../spec/2026-09-14-tb-s3-halt-resume-contract.md#5-exact-schedule-rule): own-flat D = min(16:00 ET, venue deadline − 15 minutes), entry cutoff D − 15, flatten start D − 5. Thus a regular session with venue deadline ≥16:15 uses 15:45 / 15:55 / 16:00. F₃ §S places exposed 15:55 instants at R1 only; this is a modeling convention, not a proven worst case. Historical [16:15 fills](../superpowers/specs/2026-09-03-venue-bound-session-guard.md) and [four-firm results](../../lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md) remain evidence of their own schedules, not today's holding allowance. |
| Data feed | **Intended source, activation unresolved:** [personal ADR Decision 3 / owed items 3–4](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) names personal Tradovate, subject to API access and CME licensing for every destination. F₂ D10 separates feed funding from clearance. Databento is [retired](../adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento). Cost estimates and a reusable adapter do not select, fund or license a feed. |

## Continue through the existing owners

The [mutable parent brief](../briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md)
routes to F₃. Existing [Card B](../briefs/handoffs/2026-10-12-q-sfclear-2-run-path-b-personal-replay-card-DRAFT.md),
[Card D](../briefs/handoffs/2026-10-12-q-sfclear-2-run-path-d-fg-parity-card-DRAFT.md)
and [Card E](../briefs/handoffs/2026-10-12-q-sfclear-2-run-path-e-run-record-card-DRAFT.md)
retain their owners, branches, acceptance and F₃ amendments. The [live-wiring
packet §§6b–6d](2026-10-11-live-wiring-decision-packet.md#6b-owner-file-order-amendment-2026-10-12)
supersedes old personal-plan queue rows behind GC-5/S2; this map dispatches nobody.

## Open choices for Joshua

- **Alternative-venue objective:** should alternatives preserve original strategy
  behavior first? If so, does that mean original signals/exits with personal R1
  sizing/P0/schedule, or full declared quantities and adds too? Neither is selected.
- **Route and venue:** personal CrossTrade versus direct Tradovate, and any successor
  prop venue, remain subject to their own selection and qualification. Tradeify-native
  re-expression research is a separate option, not a default for alternatives.
- **Operating scope:** concurrent accounts and unattended operation are separate
  decisions if requested; the current one-account, attended scope stands.
- **Feed:** resolve access/licensing and funding through the existing owners.

Historical freezes, old verdicts and dated research retain their provenance. This
reconciliation uses public repository sources only; it does not reverify venue terms,
inspect private inputs or establish any clearance result.
