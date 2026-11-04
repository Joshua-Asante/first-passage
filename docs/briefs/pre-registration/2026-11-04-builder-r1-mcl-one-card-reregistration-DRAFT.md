# Builder run R1, MCL opening-range breakout, one card: re-registration (DRAFT)

**Status:** `DRAFT 2026-11-04`. This draft authorizes nothing. It becomes the committed registration (Part B of the builder round template, PR #1051, not yet merged) only after a local session fills the private fields and Joshua records his GO. Until then, no R1 card is ledgered, run or looked at.

**Why.** The [R1 registration](2026-11-01-builder-r1-mcl-orb-registration.md) is not run as pinned (Joshua, 2026-11-03). Its re-registration on the current engine is owed as **one MCL card** (Joshua, 2026-11-04, addendum there), chosen from the registered eight by stated rationale before any result. This file is that re-registration's draft. K = 0 in drafting: no data, card, book or result was read.

## Public pins (filled)

| Item | Value |
|---|---|
| Engine | `lab/builder` at `main` `15af399` (branch B, PR #1054, with its follow-up PR #1058: no book gives `placement: not_evaluated`, and the pinned book sha is recorded); `gates.engine_version()` `10f0eb19f302533ffc3ad56f8e06f76734d011ab4a851488e767b41bd4cfa363`. A later engine change before freeze moves this pin |
| Gate mapping | [`lab/builder/README.md` §Ten-step mapping](../../../lab/builder/README.md#ten-step-mapping) (PR #1053, merged) |
| Calendar | [`ops/calendars/cme_holiday_calendar_2016_2026.json`](../../../ops/calendars/cme_holiday_calendar_2016_2026.json), sha256 `407d93bb815ee6b297b2b58d56a71724506f1304756d698bb9c6e52ca5b60ad4`, coverage 2016-01-01..2026-12-31 (accepted 2026-11-04, [calendars README](../../../ops/calendars/README.md#20162026-extension-accepted-2026-11-04)) |
| Firm | `Tradeify_Select_100K` (as R1); costs from `FIRM_RULES` per the builder README *Costs* rule |
| Cells | one: MCL × opening-range breakout × Tradeify Select 100K. Session window and clock settings stay in Part A |
| K | MCL builder bank 0 (R1 never ran; checked locally, prerequisite 2) + 1 new = **1**, `k_scope: instrument` (D9 item 4). `register_search` manifest `discovery_manifests/builder-r1-mcl-one-card.json`, opened at freeze before any data read: `--search-space-size 1 --alpha 0.05 --instrument MCL --lane mechanism-first` |
| Multiplicity | M = 1, alpha 0.05, applied to the Confirm test Part A freezes (A5). With one card no multiplicity adjustment applies; the engine's stage-8 pass is not that test |
| Reach (D7), estimated | at K = 1 and about 960 development sessions: floor 0.843 annual, P(pass) 0.51 at 0.85 and 0.54 at 0.89, **reachable**. Estimate from calendar spans, not the export; the run's printed `reachability_5f` is the value of record |
| Gate 5h | not run before Joshua's forward GO on a survivor (as R1) |

## Decisions before freeze

**Ruled by Joshua, 2026-11-04, verbatim:** "go with A for the holdout, and your card rule". Decisions 1 and 2 are settled as A and the rule below. Decision 3 is open.

1. **Holdout window: A (ruled 2026-11-04).** No MCL window is demonstrably untouched.
   - MSL-S2A's explore read MCL through 2025-06-30 (a different construct; [closure](../closures/MSL-S2A-closure-falsified.md)).
   - The MCL retain-mutate pilot's draft spec calls 2025-07-01..2026-06-30 an "uncertified historical replay, never independent OOS", because later exposure is unknown ([spec §2.2](../../spec/2026-10-30-mcl-retain-mutate-pilot-rev3-DRAFT.md#22-historical-exposure-uncertified-replay)). No read of it is recorded.
   - 2026-07-03..2026-11-02 is newly exported (2026-11-03), about 85 sessions. Its exposure is unverified too, short of a local audit or operator attestation, and it is too short to confirm on its own.

   | Option | Holdout | Development (est.) | Floor at K = 1 | Bars read by MSL-S2A explore |
   |---|---|---|---|---|
   | **A (ruled)**: D9 | last ~378 sessions of the new export (from about 2025-05) | ~960 | 0.843 | about 2 months |
   | B: R1's old boundary | 2025-02-25 → 2026-11-02 (~425) | ~910 | 0.866 | about 4 months |

   A is the split the 2026-11-04 reach figure assumed (0.84) and overlaps less read data. It contains the uncertified 2025-07..2026-06 period, and the registration discloses that exposure. Part A pins the dates from the landed export: `dev_end` is the session before the last 378, and `holdout_end` is the export's last session.
2. **Card-selection rule (ruled 2026-11-04)**, outcome-free and applied locally from the card files only: the card the v3 pre-registration names as primary, if it names one; otherwise the card at the centre of the registered grid, so that every ±1 neighbour is valid for 5d. Part A records the rule, the card and why.
3. **Book (open).** Recommended: keep R1's book series for the post-holdout placement check (5g, now placement only). Its `min_overlap` must hold on the new development window; if it does not, Joshua chooses a smaller `min_overlap` or `book: null`. Under PR #1058, `book: null` leaves placement `not_evaluated`, never a clear.

## Prerequisites (Must run locally)

Must run locally: the cards, R1's pre-registration, the book and the MCL export are private or vendor data, and the cloud clone has none of them.

1. **Data landing** ([generation note §9.3 step 2, §11](../../notes/2026-11-01-generation-phase-strengthening-DRAFT.md#11-updates-2026-11-04)). Validate the six MCL1! pages (2021-07-11..2026-11-02) in one `scripts/validate_bar_export_v2.py` call and commit the `SHA256SUMS` delta (Rule 19). The 2026-08-13 export cannot serve: it starts in 2022, and at K = 1 its development window does not reach.
2. **K check.** Confirm that no ledger holds an MCL card before the run (R1 never ran), so `ledger.k()` returns 1 after the card is appended.
3. **Prior-read check.** Confirm the MCL-1 pilot has not read any bar in the chosen holdout. Binding carried from R1: the holdout look happens before the pilot reads any of those bars.

## Part A fields still owed (private, per the round template)

The local session fills the template's Part A (PR #1051) as `PREREG-BUILDER-R1-ONECARD-DRAFT-v1.md` under `local_artifacts/strategy-builder-2026-10/prereg-r1/`. These are owed beyond the pins above, by the [mapping](../../../lab/builder/README.md#ten-step-mapping):

- **A1:** data pins and split dates (`dev_start`, `dev_end`, `holdout_end`) from the landed export.
- **A2:** cell dossier. Distinctness is disclosed as weak: MCL ORB shares the ORB mechanism with the index book ([generation note §10.2](../../notes/2026-11-01-generation-phase-strengthening-DRAFT.md#102-d10-which-family-seeds-which-firm), open question 1). Also step 1's EM limbs, step 5's TRADEABLE-REACHABLE limbs, or UNSCREENABLE where no citable prior exists.
- **A3:** the reach line at the real development-session count.
- **A4:** the card, its sha256 and the selection rationale (decision 2). The mechanism discriminator is report-only (D9 item 3): observable, null, direction, threshold, coverage.
- **A5:**
  - the Confirm statistic and its alpha-calibrated decision rule at alpha 0.05 (a significance test with a stated p-value method). The engine's stage-8 pass (positive net and `8_min_pf`) is a necessary condition only: it computes no p-value, and the [mapping's stage-8 row](../../../lab/builder/README.md#ten-step-mapping) says its raw pass/fail never maps to CONFIRMED by itself;
  - a holdout coverage floor;
  - the step-9 temporal battery, which is mandatory;
  - routing: `unresolved` or under-coverage → EVIDENCE-VOID, a failed statistic or battery → EXPRESSION-FAIL, all clear → CONFIRMED, and `placement: fail` → CONFIRMED · VENUE-FAIL(edition).
- **Selection freeze:** before `builder.holdout` runs, register the sha256 of `verdict.json` and the report in [`PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256) and commit them.
- **Step 8:** a compliance snapshot at freeze, rechecked just before the look.
- **Review and freeze:** a Codex review of Part A within Rule 6's limit, then a freeze record pinning the card, book, run spec, data and calendar; all hashes registered in `PRIVATE_EVIDENCE.sha256`; then Joshua's GO, recorded verbatim here.

**Binding once registered.** Changing a criterion needs a new version, a new review and a new registration. One holdout look. A survivor goes to Joshua for the forward GO with gate 5h outstanding.
