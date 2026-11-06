# DYN-SURVEY-1: survey code

**Status:** code only. Nothing here has read an export; the tests use synthetic bars.
**Authority:** Joshua, 2026-11-02, "Yes, authorize D1", for the private frozen protocol v5
(sha256 `293d5853c9910462b46e36df65fee54235f39141fc47d3119e3c023aeec7f20a`). That text is the
specification; this file records only how the code reads it. Results stay private.

## Question and decision it changes

Does a fully specified session-clock rule on an admitted Tradeify micro, at one contract, raise
the book's in-sample per-session Sharpe after costs? The answer decides whether at most one
card follows before the 2027-01-31 falsifier.

## Scope

Five instruments (MNQ, MYM, M2K, MGC, MCL) × eight cells × two directions: K = 80, fixed. `survey.py`
holds the fill, cell, statistics, eligibility and selection rules. `run.py` is the one-shot
driver: it reads a private freeze record, refuses unless HEAD is the record's frozen SHA with
clean tracked files, refuses a second run, and writes only to private paths. The merge SHA of
this PR is the frozen SHA. The parity, holdout and 5h stages are separate, contingent work.

## Readings of the protocol

- **Session bars.** Every bar the rules use opens between 07:30 and 16:45 ET on the session date,
  so a session is that date's bars before 17:00. The 18:00 start of the session day never binds.
- **Previous session day** for `C_prev` is the prior development session, including a
  calendar-closed date. Earlier bars feed C8's warm-up only, so the first development session
  has no `C_prev`.
- **Calendar-listed** means `data.Calendar.closed`, the builder's rule since the 2026-11-03
  ruling on PR #1045: an entry with a non-NORMAL status. The protocol defers to builder rules.
- **C6/C7 validity.** A missing or off-grid S, or either window failing, drops both cells.
- **S** is the end of CME's published settlement window, converted to ET.
- **Unresolved trades** take precedence over eligibility, so such a cell gets no series statistics.
- **Exposure log.** The driver appends one `planned` row per instrument before reading its bars.
  A dropped instrument reads nothing and adds no row.
