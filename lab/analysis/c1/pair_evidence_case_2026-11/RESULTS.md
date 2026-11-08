# ORB O-0 + Aegis A-0 evidence case: the August gate on the current pair (2026-11-07)

**Verdict: PRIOR STANDS.** The current pair fails the
[2026-08-26 combined-book gate](../aegis_orbmnq_combined_book_2026-08-26/RESULTS.md) at the
eval's actual sizing, in both chronological halves, by more than the frozen noise band.

**Status:** Codex-verified (#1151, #1170). Joshua accepted the verdict on 2026-11-08 ("I accept
the prior stands verdict"); for the first attempt it is accepted as risk under sitting ruling D1. It
changes no strategy, sizing or session procedure, and it authorizes nothing.

This file carries the method and the verdict only. All figures are in a private record.
Exploratory and in-sample; it is not a pre-registered qualification (the framework's G1 is
borrowed as a read, not run as a gate).

## Question

Does the live pair on the Tradeify Select 100K evaluation have an evidence case, given that the
earlier pairing (Aegis-6J1 v3 + ORB-MNQ v6) was falsified on this eval? Under amended Rule 26 that
result is an advisory prior.

## Inputs

Joshua confirmed the inputs and the sizing on 2026-11-07.

| Leg | Export (sha256) | Use |
|---|---|---|
| ORB O-0 | `bff235ea0934dace…` | As captured. It is the pinned O-0 export; the 10-28 ORB export has O-N's structure and was not used |
| Aegis A-0 | `9592577152296479…` | Has A-0's signals at other sizes, so it is rescaled per contract to the eval's size |

- **Why the rescale is sound here:** per-contract net and adverse excursion match native
  exports at other sizes exactly on every matched trade.
- **Window:** 2022-09-01 to 2026-09-01, the O-0 export's span.
- **Current version:** D7's fixes don't change entries, exits, sizing or stops. Parity between
  these exports and the eval build is limited, and that reconciliation stays private.
- **Per-leg sizes** are private.

## Method

The decision rule was frozen before any figure on these inputs existed. The driver refused to run
on any other hash.

1. **Engine.** `core/mc` unchanged, row `Tradeify_Select_100K`, consistency 0.40, inactivity
   barrier off, DD throttle off, seeds 1–5 × 2,000 paths, 5-day blocks. The August scripts ran
   unmodified from git `770413b^`.
2. **Control, first.** The August §9.2 and §10.2 cells, on August's inputs, through this driver
   and the current engine. Allowed miss: 0.10pp. **Result: all four cells reproduced exactly.**
3. **Binding cell.** The pair at eval sizing, under §10's timestamp-sequenced intraday-honest
   floor, bootstrapped within each chronological half. Ceiling: August's 3.0% headline bust in
   both halves, with a noise band of two binomial standard errors. The band covers simulation
   error only, not estimation error in the history.
4. **Tail-consistent sizing.** The eval sets the sizing here, so this is reported rather than
   chosen: the 95th-percentile drawdown ratio, computed with August's method on the current
   series, compared with the eval's ratio, plus a cell at that ratio with Aegis held at its eval
   size.
5. **G1 read** (framework §3–§4), on the combined day series with zero days included: SR̂ per
   chronological half; SR_LB with Lo's (2002) GMM standard error, Newey-West weights, lags 1–5;
   z = Φ⁻¹(1 − 0.20/K), run at K = 13 and restated at K = 14 (see Limits). Three other standard errors are reported beside it. Per-leg reads are
   reported and don't bind, because framework §11 item 5 is open.
6. **Reported, not binding:** flat EOD halves, each leg solo, and an Aegis fill sensitivity using
   the frozen H-AEGIS-FILL-1 central ratio.

**G2 is out of scope.** The funded model and fee budget B aren't set, and no values were invented.

## Verdict rule (first match wins)

| Condition | Verdict |
|---|---|
| Control misses | inconclusive |
| Either half above the ceiling by more than the noise band | prior stands |
| Either half inside the noise band | inconclusive |
| Both halves clear, SR̂ > 0 in each half, SR_LB > 0 | prior overturned |
| Both halves clear, otherwise | inconclusive |

G1 cannot rescue a failed gate under this rule.

## Result

- The control passed. The binding cell failed in both halves, beyond the noise band.
- No reported cell cleared both halves, including the tail-consistent one, which is not a
  tradeable size, and each leg solo.
- **Post-hoc check, outside the frozen rule:** rolling chronological starts in the same engine,
  and bootstrap blocks longer than 5 days, give a lower bust rate than the binding cell, and
  rolling starts reproduce the earlier private replay. The point estimates all stay above the
  ceiling. This is direction only: rolling starts overlap, and the rolling figure counts late starts
  that cannot finish, which pulls it slightly low. No dependence-aware margin was computed, and the
  verdict rests on the binding cell alone.

## What this does not show

- It does not show negative expected value. The 3.0% ceiling is a preservation bar from August,
  not an economics test, and G2 was not run.
- The G1 read does not establish an edge: it uses one exposed, tuned, in-sample history. K = 14 is a
  disclosed lower bound, not a total multiplicity correction, since v1→v7 ORB tuning is unreconciled.
  The read uses α = 0.20 and the running K. The T00 manifest carries α = 0.05, and the framework
  sets z from the lane's trial cap. Either would tighten it; the private record restates the
  read under the stricter α.

## Limits

- In-sample, with prior performance reads of both legs.
- **K accounting.** This re-test counts: Joshua ruled on 2026-11-07, so it is T00 trial 14 and the
  ledger is K = 14. That supersedes the frozen rule's K += 0. The run's G1 read used z for K = 13;
  the private record restates it for K = 14. The gate has no K term, so the verdict is unaffected.
- A fresh account, not the owned account's state.
- TradingView fills, apart from the Aegis sensitivity. ORB has no fill test.
- The intraday floor is trade-level and assumes concurrent trades hit their worst together. It
  leans conservative and is not a tick path.
- The simulation halves share the split day, a holiday with no trades, so the effect is nil. The
  G1 halves don't overlap.

## Independent review

On 2026-11-07, at Joshua's request, an independent Claude reviewer read the private materials. It
derived the verdict before reading the author's record and reached the same one, prior stands. It
also reproduced the input checks, the G1 read with its own code, and the binding cell under new
seeds. Its wording corrections are in this file and in the private record. This review does not
replace Codex's.

## Provenance

Private, under `local_artifacts/pair-evidence-2026-11/`, by sha256:

| File | sha256 prefix |
|---|---|
| `DECISION-RULE-v1.md` | `5310b15a383f1d15` |
| `run_gate_v1.py` | `bf2ffe4876c23d91` |
| `RESULTS-v1.json` | `aec38d98ab005ac9` |
| `reconcile_v1.py` | `e8d82e81a6d59238` |
| `RECONCILE-v1.json` | `0425c11d126fa64e` |

Engine revision `8887470`. The later commits on `main` at the time of the run did not touch `core/`.
