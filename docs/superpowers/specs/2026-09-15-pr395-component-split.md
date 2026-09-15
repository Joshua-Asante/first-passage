# PR 395 component split

Approved by the operator on 2026-09-15. PR 395 remains the integration reference;
approval of this split does not approve activation or merge.

## Boundaries and dependencies

The coordinating agent owns integration acceptance. Extract from `bd41cb6`, with
the calendar starting on main `242992b`. Each component needs independent review.

| Component | Owns | Input / output | Latest review findings |
| --- | --- | --- | --- |
| Session calendar | Schedule validation and permission timing | Pinned calendar, overlay, evidence and operator ratification → historical schedules or admission decision | Ratification time discarded |
| Evidence ingestion | Report parsing, source independence, window coverage and capture chronology | Retained source bytes → complete validated evidence snapshot or refusal | Window/source binding, close-equity independence, local-day DST limit, future rows |
| Settlement calculation | History comparison, reconciliation and numeric bounds | Validated evidence, selected session and accepted predecessor → proposed close or refusal; no database writes | Ordinary-predecessor catch-up, float overflow |
| Durable settlement owner | Challenge/authentication, atomic acceptance, correction and recovery | Verified proposal plus retained evidence → durable accepted/revised history | Missing revision source bytes |
| Qualification | End-to-end acceptance and Step 6 integration | All four components and real source captures → qualification evidence | Integration acceptance remains outstanding |

Calendar is independently useful on main. Ingestion does not own acceptance.
Calculation consumes ingestion and calendar contracts. The durable owner owns
serialization and must reverify retained evidence on reopen; a proposed close is
never an accepted close. Qualification follows all four. Subsequent component
plans must define concrete interfaces from the extracted code before edits.

## Calendar contract

`load_session_calendar` validates artifacts and produces a `SessionCalendar`
with no admission authority. `schedule_for`, `row_containing`, and
`next_row_after` remain available before ratification, including denied rows
needed for protective deadlines and historical settlement.

`load_ratified_calendar` additionally verifies the operator record against the
calendar digest, overlay digest, calendar identity and coverage. It retains
the second-precision UTC `ratified_at` instant. `session_for(now)` produces a
`BookSession` only when ratification exists, `now >= ratified_at`, and all
existing coverage, schedule, product-open and cutoff requirements pass.
Refusals retain the current row and warnings where available. Ratification
does not retroactively authorize admission into earlier sessions.

## Constraints and acceptance

- Preserve the pinned calendar, overlay and evidence bytes and policy constants.
- Keep the existing legacy evidence warning visible; extraction is not fresh source qualification.
- No settlement database, signing key, Step 5 acceptance or Step 6 admission is part of the calendar PR.
- Test raw-load refusal, one microsecond before / at / after ratification, historical lookup, and sizing integration through the real ratified loader.
- Calendar acceptance does not close the other seven review findings or establish live readiness.
