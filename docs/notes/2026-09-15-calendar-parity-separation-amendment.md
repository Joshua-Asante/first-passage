# Packet 1 amendment: provider-data parity and session legality

## Decision and scope

Operator instruction: **“make that amendment”**, September 15, 2026, following
the proposal to separate historical provider-data verification from exchange
calendar reconstruction. Base revision: `1bd196b` on
`codex/tradeify-packet1-startup-coverage`.

This is an authorized change to the acceptance method, not a retrospective PASS.
It supersedes the attended-release plan's Step 3 requirement to explain **every**
historical panel gap using Step 4 calendar evidence before provider-data parity
can pass. Previous evidence and OPEN dispositions remain historical records.
No existing bundle is admitted by this amendment. Apply the amended requirements
only through a newly reviewed, digest-bound admission contract.

Grounding: inspected `ops/c1_rail/book_sizing_context.py` at the base revision.
`BookSession` carries session/prior-session identities, opening, risk-add cutoff,
closing and calendar digest. `_session_mode` requires the matching prior close,
valid time ordering, matching digests and fresh account evidence. A successful
sizing result does not authorize submission. The calendar producer, verified
session selection and execution owner remain responsible for those boundaries.

## 1. Step 3: establish the actual provider calculation input

Accept provider-data coverage only when the reviewed evidence establishes all of:

1. Exact source body, effective inputs, symbol, timeframe, session/chart settings,
   adjustment state and calculation interval, including endpoint interpretation.
2. Complete provider bar evidence for that interval and required initialization
   history, with retained raw bytes and capture provenance. Verify export limits,
   truncation, duplicate timestamps, chunk seams and terminal-bar handling. Trade
   CSVs, first/last timestamps, equal row counts or matching trades alone cannot
   establish complete bar coverage.
3. Exact ordered timestamp and normalized OHLCV agreement between that evidence
   and the Python input. Normalization must be explicit and lossless for the
   represented values; no new tolerance, interpolation or forward fill. Any
   difference blocks this verdict until investigated and resolved in a separately
   reviewed evidence generation. A newer provider revision does not silently
   replace the captured reference or its source state.
4. Source/settings-bound initial adapter and emulator state; every required bar
   consumed once in order. Indicator seeds, session history and account/fill state
   are distinct obligations. A short warm-up or empty positions cannot stand in
   for the complete initialization contract.
5. Independent review binding the panel, source, settings, normalization, runtime,
   interval and report identities. All required trade comparisons still run with
   no excluded trades under the existing admission and parity requirements.

A timestamp absent from both independently qualified provider evidence and the
replay panel is **absent from the qualified provider input**. It is not thereby an
exchange closure, a zero-volume bar, evidence of broker finality or proof of a
complete exchange trade tape. The verdict is explicitly provider-relative.

Retain the gap inventory. Calendar cause labels are diagnostic unless the claim
being accepted depends on them. A gap remains blocking if provider completeness,
initialization, fill interpretation, venue legality or another required claim
depends on its unresolved cause. This amendment does not permit selective trade
removal or changing the frozen historical strategy/calendar overlay to obtain
agreement.

## 2. Step 4: qualify the session facts actually consumed

Exchange/account evidence remains required for every trading-permission boundary,
mandatory flattening deadline, session/prior-session mapping and historical venue
legality or outage claim actually used. Provider-data parity cannot satisfy these
requirements. D19 remains immutable historical **date membership only**; typed
policy restrictions do not become exchange closure facts.

For the first attended release, use a small versioned session file for the already
approved **September 3–30, 2026** horizon. It must enumerate permitted ordinary
sessions and explicit denied/unknown coverage, product/account identities, source
references, opening/cutoff/flattening/closing times, timezone/UTC mapping and
coverage expiry. Derive accepted `BookSession` values only from qualified rows;
the current consumer is not itself the source verifier.

- Permit new risk only when the required account and all four product session
  facts are qualified. Holiday, shortened and uncertain adjacent sessions are
  denied for this first release. Exclusion is a book permission restriction,
  not an assertion of exchange closure.
- Missing, conflicting or expired coverage halts new risk. No weekday fallback,
  inferred holiday deadline, operator acknowledgment override or automatic resume.
- Qualify the flattening deadline and subsequent transition before admitting the
  preceding session. Denying a later session must not abandon existing exposure,
  cancel necessary protection or disable the attended recovery owner.
- Keep account-session chronology across denied/no-trade days. The prior settled
  close remains the prior required account session, not simply the last day on
  which this book traded. Freshness, full-history evidence and catch-up rules stay
  intact.
- Review and extend the file monthly before expiry. Calendar/permission changes
  receive new digests and the applicable freeze/reseal and activation checks.
  This amendment neither installs such a file nor schedules its renewal.

The ordinary-session restriction applies to the first forward release. It does
not trim historical source-parity exports. Historical schedule-overlay results
remain separately identified, and any historical venue-legality acceptance still
requires evidence for its actual matching intervals and deadlines.

## 3. Separate verdicts and acceptance checks

Record provider-data coverage, strategy parity and session legality separately.
Step 3 can close without a calendar explanation for every shared provider gap
once its own requirements above pass. Packet 1 and live activation still require
their calendar, settlement, risk, recovery and combined acceptance gates.

Review these concrete cases before adopting the revised admission contract:

| Case | Required result |
|---|---|
| Qualified provider and Python input share an absent interval, with no dependent legality/fill claim | Provider coverage may pass; exchange cause stays unknown |
| One timestamp or OHLCV value differs, or export completeness is unproven | Provider coverage blocked |
| Trade ledgers match but source state or initialization is unbound | Step 3 blocked |
| Data parity passes but a consumed venue deadline is unsupported | Relevant legality/permission gate blocked |
| Holiday or uncertain adjacent session | No new risk under first-release restriction |
| Calendar expires while exposure exists | New risk halted; protective/recovery ownership retained |
| A denied session separates two trading sessions | Required account chronology and prior-close verification retained |

The existing intake fields are not automatically reinterpreted. Reconcile the
trusted admission contract and any validator assumptions before issuing a PASS.
Production code, private reference bytes and accepted verdicts are unchanged.

## Verification

Documentation-only amendment. Review the complete diff against the requirements
above, the actual `BookSession` consumer and the five linked owning records. Run
`git diff --check` and verify local Markdown targets. Independent review must
accept the changed acceptance method before its first decision-bearing use.

Owning records:

- [Attended-release plan](../superpowers/plans/2026-09-14-tradeify-attended-release.md)
- [Execution-domain evidence](2026-09-15-packet1-execution-domain.md)
- [Calendar/account contract](2026-09-15-calendar-account-contract-resolution.md)
- [Bundle intake interface](../briefs/handoffs/2026-09-14-seven-bundle-runtime-interface-plan.md)
- [Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)

Independent reviewer `packet0_review` accepted the six-document amendment against
the actual consumer and intake assumptions with no blocking findings. This accepts
the method, not Step 3 completion, bundle admission or activation. On base
`1bd196b` plus this amendment, `git diff --check` passed and all 42 local Markdown
targets in the changed documents resolved. No runtime tests are claimed for this
documentation-only change.
