# Packet 1 Step 4 — bounded session calendar (September 3–30, 2026)

Status: **IMPLEMENTED and OPERATOR-RATIFIED by digest (2026-09-15); independent review
still owed.** Base: PR #394 head plus this change. Owner: Packet 1 coordinator (TB-C1).
No runtime activation, live permission, deployment or resumption authority is granted.

## What was built

| Artifact | Identity (SHA-256) |
|---|---|
| `ops/calendars/book_session_calendar_2026-09.json` | `650e8aab4166f74a988675a3f3dfa2dbd21c1c1b342777ac37d65aacea9d6f2f` |
| `ops/calendars/book_closure_overlay.json` | `483f2324b85548e60429b823454641a0ee6e34c8ef2a9cadc7dcc6555f7def5b` |
| `ops/calendars/evidence/2026-09-15-forward-session-source-captures.json` | `56951e1527af20966dea64130bf8d0a1dccb9bc011bd6e0501282faa549fcba5` |
| `ops/calendars/cme_holiday_calendar_2022_2026.json` (D19, unchanged) | `2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9` |

Code: `ops/c1_rail/book_session_calendar.py` (loader and `BookSession` producer),
`scripts/author_book_session_calendar.py` (authoring tool for the monthly extension),
`tests/ops/test_book_session_calendar.py` (64 tests).

**Path decision.** The Track B umbrella's TB-C1 claim named
`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/` for the forward file and overlay; the
attended-release plan names `ops/calendars/`. The consumer is the rail and `lab` may not be
imported by `ops`, so the artifacts live under `ops/calendars/`. The umbrella carries a dated
pointer to this record.

## Sources actually consumed

All captured 2026-09-15 through read-only page loads and quoted in the evidence file.

- **Tradeify permitted times** (article dated 2026-07-14): all positions closed by **4:45 PM ET**
  on regular days and **12:59 PM ET** on holiday-shortened days; the account day runs
  **6:00 PM ET to 5:00 PM ET** the next calendar day; holiday days are independent days.
- **CME 2026 Globex holiday schedule**: Labor Day covers **6–8 September 2026**; the next listed
  holiday is Thanksgiving (26–28 November). No other September date appears.
- **CME contract specs** for 6J, MGC, MYM, MNQ: each trades Sunday–Friday 6:00 PM–5:00 PM ET
  with a daily break from 5:00 PM ET.
- **Retained 2026-09-07 product observations** (private, digest `3dafe4b7…`): matching halts
  at 13:00 ET (MYM, MNQ), 14:30 ET (MGC), 17:00 ET (6J); reopen 18:00 ET for the September 8
  CME trade date.

## Session semantics

- Session key: `tradeify-account-day:YYYY-MM-DD`, the Tradeify account day ending 17:00 ET on
  that date. Per-product CME trade dates are recorded on every row; on ordinary days they equal
  the account date. A broker CSV date is never copied into this key.
- Predecessor chain runs through every account day, including denied ones and across weekends:
  September 9's prior session is September 8 (denied), September 7's is September 4. The
  consumer test proves a settled close for the last traded day cannot substitute.
- Schedule (TB-S3 rev9 §5, verified on every row by the loader): `V` = min(venue deadline,
  product closes); `D = min(16:00 ET, V − 15 min)`; cutoff `D − 15`; flatten start `D − 5`.
  Ordinary rows: **15:45 / 15:55 / 16:00 ET**. The Labor Day row: **12:29 / 12:39 / 12:44 ET**
  from `V = 12:59`, matching the spec example.
- `BookSession` values carry UTC instants; the ET mapping is verified at load, and DST gap or
  fold wall times are refused.

## Permission for the first release

| Sessions | Permission | Reason |
|---|---|---|
| 18 ordinary account days | PERMITTED | all four products qualified from the spec pages; no holiday row |
| 2026-09-07 | DENIED `HOLIDAY` | CME Labor Day schedule; venue 12:59 deadline; products' preceding open not separately established |
| 2026-09-08 | DENIED `UNCERTAIN_ADJACENT` | inside the CME schedule dates 6–8 September; reopen observed, full session not separately qualified |

Denied rows are permission restrictions on the book, not exchange-closure claims. Coverage:
2026-09-02 22:00Z through 2026-09-30 21:00Z. Review due **2026-09-24**; a session at or past
that instant still loads but carries a `calendar_review_due` warning. Coverage expiry refuses new
risk; it never invents a fallback session.

## Verification

- `tests/ops/test_book_session_calendar.py`: 64 passed. Covers byte pinning of all four files,
  deterministic regeneration from the authoring tool, the umbrella-owed checks (both files parse,
  no forward row at or before the frozen D19 window end 2026-09-02, overlay rows flagged
  `overrides_d19: true`, coverage reaches the horizon), §5 derivations, every refusal reason,
  consumer agreement through `size_book_request` on the real predecessor chain, DST mapping across
  2026-03-08, gap/fold refusal, overlay blocking, a 25-case calendar mutation matrix and a 6-case
  overlay mutation matrix.
- `tests/ops` full suite: 1708 passed, 15 skipped. `scripts/check_boundaries.py`: OK.

## What this does not do

- No historical legality or matching-hour claim for any date before 2026-09-03. D19 remains
  date membership only; the 296-check archival inventory stays `INCOMPLETE_NOT_RUNTIME_INPUT`.
- No runtime binding yet: the account identity is `BOUND_AT_RUNTIME`. The tracked ratification
  row is the pin the loader enforces; the activation-time volume-config pin is Packet 6.
- No scheduler, `AccountClock` or replay integration (Packet 2). This record supplies the
  producer those consumers will call.

## Ratification — 2026-09-15

Operator instruction, verbatim: **"ratify calendar 650e8aab"**. Recorded in
`ops/calendars/RATIFIED.json` (schema `calendar_ratification/v1`) against the full
calendar digest `650e8aab4166f74a988675a3f3dfa2dbd21c1c1b342777ac37d65aacea9d6f2f`.
The closure overlay digest `483f2324…` was presented in the same request as the
calendar's companion artifact and is pinned in the same row; the operator did not
name it separately, so an objection would unpin it without touching the calendar row.
`ops/c1_rail/book_session_calendar.load_ratified_calendar` refuses any calendar whose
exact bytes are not ratified there, and refuses a ratified calendar whose overlay or
coverage bounds differ from the row. The volume-config pin at activation remains a
Packet 6 step. Ratification grants book permission rows only: no activation,
deployment, resumption or historical legality.

## Remaining to close Step 4

1. Independent review of this record, the loader and the file against the amendment.
2. Monthly extension before 2026-09-30 (procedure in `ops/calendars/README.md`); each
   extension needs its own ratification row.
