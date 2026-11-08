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
clean tracked files, refuses an output path git tracks or does not ignore, refuses an instrument
without a pinned holdout boundary, refuses a second run, and writes only to private paths. The merge SHA of
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
- **One run, counted from its start.** The driver creates `run.started` in the private `out`
  directory with an exclusive create before it reads the calendar, book or any export. The marker records the frozen SHA and the UTC start
  time and is never removed, also not when the run fails. A run that fails after the marker is
  written therefore uses up the one run: the driver refuses another until a defect is recorded
  and an addendum written, as it does when `report.json` exists. The protocol says one run; this
  reading counts a started run as that run. The author's final comment on PR #1110 (2026-11-07)
  records it as confirmed by Joshua; that record is the author's comment, not Joshua's own words.
  `run.py` `claim_run` implements it.
- **Holdout boundary** (amended by Joshua 2026-11-08 after #1138). Each instrument entry in the
  freeze record carries either `h_start` with `dev_last_session` (ISO dates; `dev_last_session`
  is the last development session of the pinned export, recorded at freeze, and must be before
  `h_start`) or an explicit `holdout: {"none": "<reason>"}` with a non-empty reason. `main`
  validates every entry before `claim_run` and before it reads the calendar, book or any export:
  neither form, both forms, a non-ISO date, an empty reason or `dev_last_session` on or after
  `h_start` is refused and creates no marker. A missing `h_start` no longer skips the check.
  After loading an instrument's bars, the driver refuses unless the actual last development
  session equals the pinned `dev_last_session`. That read comes after the marker, so this
  refusal uses up the run like any failure after the start.
- **All-UNRESOLVED survey.** Labelling it NULL matches protocol v5; unchanged.
- **Re-freeze.** This amendment changes `run.py`, so the frozen SHA moves to the merge of the
  PR that carries it, and the private freeze record gains `dev_last_session` per instrument
  (Joshua's re-freeze).
- **Missing commission row.** Under 7.2 the instrument drops as NOT EVALUATED; the report's
  `commissions` map records that firm and symbol with `commission: null` and the reason.
