# ORB MNQ v0.2 — venue-conformance amendment (ORB-MNQ-1)

**Status:** `CANDIDATE · PARKED · NOT LIVE` — calendar-conformance amendment to v0.1.
Lifecycle admission unchanged ([ADMISSION](../../../lab/analysis/orb_mnq_2026-07/ADMISSION.md));
PARKED 2026-07-23 (operator); rail / account / spend remain separately gated.
**Edition file:** `orb_mnq_v0_2.pine` (gitignored; hash pinned in
[`PORT_MANIFEST.sha256`](../PORT_MANIFEST.sha256) — **`bad8068d…`**).
**Supersedes (active working edition):** `orb_mnq_v0_1.pine` (`df05512d…`) for any new
export or reconcile. v0.1 remains hash-pinned as the OCA-fixed baseline the half-day
deltas are measured against.

**Naming:** `orb_mnq`, not `striker-*` — distinct mechanism from locked Striker NAS100.

## What v0.2 is (and is not)

v0.2 is a **calendar / envelope-conformance** amendment only. The frozen pre-registered
construct is unchanged (OR = first 2×15m RTH bars → both-sides touch-fill → opposite-OR
stop → flat at session close → one trade/day; no gates, no give-back, K_intrinsic=1).

On any **full-session** day, trade selection must be byte-identical to v0.1. Expected
panel deltas vs the v0.1 ~1,026-trade panel are confined to the half-day cohort (see
Pine header reconcile block). A large PF/WR/DD move outside that cohort is a defect.

**Not in scope for v0.2:** BE/targets/DOW/OR-length (pre-killed or pre-reg-voiding);
payability redesign (needs a different construct or book role — new campaign ID);
composing into the c1 book (Q-COMPOSE-1 FALSIFIED).

## Deltas vs v0.1

| ID | Class | Change |
|---|---|---|
| **D1** | Early-close calendar | Year-agnostic reduced-session detection; force-flat on 12:30 → fill 12:45 (≤ Tradeify 12:59). Half-day uses (close−30) because the 12:45 bar is the session's last bar. |
| **D2** | Resting-order leak | Entry-placement cutoff derived from the **same** effective close as EOD (stops half-day OCO fills at Globex reopen; cites trade 748 / Juneteenth). |
| **D3** | Contracts (k) | Exposed as input, default 1 = harness parity. Live sizing stays account-multiplier layer. |
| **D4** | Manual override | Comma-separated early-close date list for one-offs date rules miss. |
| **D5** | Full-session clock pin | `sessOpen`/`sessClose` are **constants** (09:30 / 16:00), not inputs. A 2026-07-30 export printed full-session EOD @ 15:30 (286×) while source defaults were already 16:00 — chart/session input had been set to 15:30 ([`RESULTS_v02_clock_kgrid.md`](../../../lab/analysis/orb_mnq_2026-07/RESULTS_v02_clock_kgrid.md)). Pinning removes that override class. Reduced-session end (`ecCloseH/M`) remains an input. |

EXPERIMENTAL block (BE stop, OR-range regime gate) stays master-gated OFF (`UNFREEZE`);
enabling any of it voids the 2026-07-16 pre-registration.

## Cost model

Unchanged frozen research economics: **$0.61/side** (Bulenox) + 1-tick slip. For any
Tradeify-facing panel set commission **0.91** in Properties before export and label the
file accordingly. Stage-7: 2021+ passes all four FRIENDLY firms to 3 ticks; FULL window
is Bulenox-and-≤1-tick-specific.

## Clock audit + k-grid (2026-07-31)

Structural scorecard on the pre-D5 2026-07-30 Bulenox-costed export
([`RESULTS_v02_clock_kgrid.md`](../../../lab/analysis/orb_mnq_2026-07/RESULTS_v02_clock_kgrid.md)):

- Half-day path **PASS** (15× EOD @ 12:45, calendar-aligned).
- Full-session EOD **30m early** under the unpinned inputs → **D5**.
- Tradeify-recosted k grid (geometry only, this ~2y window): single-day trail headroom
  at k∈{1,2,3}; k≥4 single-day bustable vs $3k; payability not cured by k (~22% days
  ≥$200 at k=1). **Do not freeze a k policy** until a post-D5 re-export at 16:00 is
  scored with the same harness.

## Acceptance checklist

- [x] Compile clean — `python3 scripts/pine_check.py core/strategies/orb/orb_mnq_v0_2.pine` (OK 2026-07-31)
- [x] Hash pinned in `PORT_MANIFEST.sha256` (`bad8068d…`) in the same motion as land.
- [ ] Operator: paste/update the published TV script from this file (D5 removes Session
      open/close inputs — confirm the Inputs pane no longer exposes them).
- [ ] Re-export `CME_MINI:MNQ1!` 15m with commission appropriate to the decision
      (Bulenox 0.61 or Tradeify 0.91); expect full-session EOD timestamps at **16:00**
      (or 15:45 if TV reports the order bar — either way not 15:30).
- [ ] Re-run [`run_v02_clock_kgrid.py`](../../../lab/analysis/orb_mnq_2026-07/run_v02_clock_kgrid.py)
      on that export; half-day cohort should be byte-stable vs the 2026-07-30 panel.
- [ ] Then — and only then — k-policy geometry (still not a Stage-7/8 substitute).
- [ ] Rail integration — separate operator GO; not authorized by this amendment.

## Provenance

1. Construct: `ops/instruments/NAS100.md` N1 → native MNQ Stages 2/6/7/8
   ([`lab/analysis/orb/orb_mnq_2026-07/RESULTS.md`](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS.md)).
2. v0.1 authoring + OCA fix 2026-07-21
   ([`orb_mnq_v0_1_CANDIDATE.md`](orb_mnq_v0_1_CANDIDATE.md)).
3. v0.2 D1–D4 authored on TV (calendar conformance); D5 + in-repo land 2026-07-31.
