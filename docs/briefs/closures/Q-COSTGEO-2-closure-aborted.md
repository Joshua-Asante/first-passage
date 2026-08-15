# Q-COSTGEO-2 — Closure: `ABORTED at P0.1` (cost premise falsified; protocol-mandated stop)

**Verdict:** `ABORTED` — P0.1's own abort condition fired on the first command. The §0 cost claim was an extrapolation and it was wrong by **$272.91**.
**Closed:** 2026-07-23
**Pre-registration:** [`Q-COSTGEO-2-verdict-preregistration.md`](../pre-registration/Q-COSTGEO-2-verdict-preregistration.md) — `FROZEN`, signed 2026-07-23 / JA, freeze commit **`32d9c87`**
**Successor:** [`Q-COSTGEO-3-verdict-preregistration.md`](../pre-registration/Q-COSTGEO-3-verdict-preregistration.md) — MYM add-cohort only, event-day pull shape, cost verified day-by-day rather than extrapolated.
**Spend:** **$0.00.** No pull. P0.2 never started. K=0, no manifest.
**Live effect:** **none.** c1 rung stays WATCH-1 0.50× / disarmed; no cost constant changed; lock HELD.

---

## 1. What fired

§8 P0.1, as frozen:

> **P0.1 — fetch-path confirm (BLOCKING).** Re-run the free estimate for `bbo-1s` on both instruments. **Abort if it no longer returns $0.0000** (ADR falsifier: un-estimated billing event ⇒ freeze).

Measured, full span 2020-01-06 → 2026-06-30:

| Symbol | `bbo-1s` full span | Volume |
|---|---|---|
| `MNQ.v.0` | **$147.5736** | 10.36 GB / 129,486,152 records |
| `MYM.v.0` | **$125.3330** | 8.79 GB / 109,863,802 records |
| | **$272.9066** | 19.15 GB |

Not $0.0000. **Abort.** No pull ran; the guard worked exactly as designed and cost nothing.

---

## 2. The falsified premise, and how it got in

Both Q-COSTGEO-1 and Q-COSTGEO-2 asserted in §0:

> `bbo-1s` **$0.0000**, 144 MB/instrument-month … Full c1 span at `bbo-1s` ≈ **11 GB/instrument, ~22 GB both legs, $0.00**.

**One month was estimated. The full span was extrapolated** — on the implicit assumption that a $0.00 monthly reading scales as $0.00 × N. It does not: the subscription entitles **recent** data and **bills history**.

Measured cost curve (`MNQ.v.0`, `bbo-1s`, free metadata endpoints):

| Window | Cost |
|---|---|
| 1 month (2026-06) | $0.0000 |
| 3 months (2026-04→07) | $0.0000 |
| 12 months (2025-07→2026-07) | $1.4116 |
| 24 months (2024-07→2026-07) | $28.4658 |
| 48 months (2022-07→2026-07) | $81.9818 |
| full span | $147.5736 |
| 2020 alone (12 months, old) | $25.9892 |

Per **instrument-day**: **$0.0000** in 2026 · ~**$0.105** for 2021–2025 · ~**$0.043** in 2020. Note 2020 costs *less* than 2022–25 per day because it carries fewer quote records (31,959 vs ~78,000), not because old data is cheaper — **cost tracks billable volume, not age**; the *window* results above look age-driven only because the recent months are entitlement-covered.

**This is the third instance this session of one failure mode**, and the most expensive had it not been caught: an unverified premise about the shape of an external artifact, asserted at authoring, with a sub-five-minute direct verification available and not run. The prior two were the panel's span (Q-C1PANEL-1) and the meaning of a timestamp (Q-COSTGEO-1). See §5.

---

## 3. What the abort diagnostic bought (the useful part)

Two structural facts, both measured, both free:

**(a) Billing granularity is per-day, not per-request-window.** A 15-minute request and a full trading day return **byte-identical** estimates ($0.0429 / 2,556,720 bytes / 31,959 records for `MNQ.v.0` on 2020-03-16). Sub-day windowing buys nothing; the **day is the atom**.

**(b) The events touch only 403 of ~1,630 instrument-days.** MYM 197 · MNQ 206 (union 350 calendar days). The frozen continuous-span pull shape was **~98% dead weight** — paying for 6.5 years of continuous quotes to measure ~1,100 moments.

**Event-day pulling costs ~$36 for the byte-identical sample** — every one of the 551 entries and their paired exits, all four cells at full N — versus $272.91 for the frozen shape. The frozen shape is **strictly dominated**: it buys no additional event.

---

## 4. Why the successor is one cell, not four

Sizing the four cells against their prior uncertainty:

| Cell | Live order | Prior uncertainty | Event-day cost |
|---|---|---|---|
| MNQ base | 3 lots | none — clears the inside trivially | — |
| MYM base | 9 lots | none — clears the inside trivially | — |
| MNQ add | 30 lots | low | ~$4.04 (est.) |
| **MYM add** | **67 lots** | **the actual question** | **$2.3371 — VERIFIED day-by-day** |

The MYM add figure is **measured, not extrapolated**: `bbo-1s` cost queried for each of the 34 event-days individually (28 billed at $0.06–$0.10, 6 free — the entitlement window reaches back to 2025-10-14). The first-pass extrapolation at a flat $0.105/day gave $3.17, i.e. **36% high**. Conservative direction, but the same class of error that closed this instrument — hence the verified number is what the successor's §0 carries.

Three further constraints compress it to one cell:

- **The `FALSIFIED-UNDERSTATED` route can barely fire on D3.** A measured floor ≥ 1.0 tick/side requires a ≥2-tick spread at fill moments; these books are 1-tick-wide through the overwhelming majority of RTH. The realistic non-benign outcome is `AMBIGUOUS-NEEDS-DEPTH` — a pointer to a **$115+/instrument-month `mbp-10`** study, not an answer.
- **The benign outcome licenses nothing.** The pre-registered floor asymmetry means measured-below-modeled cannot cut the hurdle without realized fills. `RESOLVED-CONSERVATIVE` changes no constant, no sizing, no rung.
- **So the decision value is concentrated in one cell**: the largest order the live system sends (67 lots), on the lighter of the two instruments, fired into a breakout, on the leg carrying the pyramid economics, days before B7 arms.

**Explicitly NOT pre-registered:** any *a fortiori* rule of the form "MYM's 67-lot add clears ⇒ MNQ's 30-lot add clears." That would bake an **unmeasured** depth-ordering between the two instruments into a frozen decision rule — the exact error class that halted the three prior instruments. Whether the other three cells are worth their ~$29 becomes a fresh decision once a real MYM number exists.

---

## 5. Process record

**PD-1 — cost extrapolated from a single sample.** Recorded above (§2).

**Standing lesson candidate (brief-authoring) — the §0 verification sweep.** Three instruments halted at Phase 0 today, all on the same failure: *a quantitative or structural claim about an external artifact, asserted in §0 at authoring time, when its cheapest direct verification was under five minutes and was not run.*

| Instrument | Unverified §0 claim | Truth | Cheapest check not run |
|---|---|---|---|
| Q-C1PANEL-1 | panel starts 2020-07-01 | 2020-01-06 | read the cited parent pre-reg |
| Q-COSTGEO-1 | stamped time = fill instant | it is the bar label | price vs bar open/close |
| Q-COSTGEO-2 | full span = $0.00 | $272.91 | estimate the full span |

**Proposed mechanical rule:** *before freezing any pre-registration, enumerate every quantitative or structural claim in §0 and run its cheapest direct verification; §0 states the verification, not just the value.* Each of the three above was a one-command check. The pre-registration discipline caught all three at **$0.00 spend**, which is the system working — but it caught them at the gate rather than at authoring, and each catch cost a full authoring + signature cycle. Extends [[lesson_run_cheap_falsifier_before_authoring]] from "run the cheap falsifier before the brief" to "run the cheap *verification* of every §0 constant before the freeze." Dated anchor: this closure. Cost: three authoring cycles, three operator signatures, $0.00 spend, zero data touched.

---

## 6. Audit hooks

```bash
# Freeze predates the abort (guard fired on the first command after signature).
git log -1 --format='%h %ci' 32d9c87

# Reproduce the abort: full-span estimate must NOT be $0.0000.
PYTHONPATH=lab .venv-research/Scripts/python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema bbo-1s --start 2020-01-06 --end 2026-06-30 | grep cost
#   expect ~$147.57  (the frozen §0 claimed $0.00)

# Per-day billing granularity: 15-min and 1-day estimates are byte-identical.
PYTHONPATH=lab .venv-research/Scripts/python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema bbo-1s --start 2020-03-16T13:30 --end 2020-03-16T13:45 | grep billable
PYTHONPATH=lab .venv-research/Scripts/python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema bbo-1s --start 2020-03-16 --end 2020-03-17 | grep billable

# No pull ever ran under this instrument.
ls -d lab/analysis/c1_cost_geometry_* 2>/dev/null | wc -l   # must be 0
ls discovery_manifests/ | grep -i costgeo || echo "no manifest (correct — K=0)"
```

---

## 7. Change history

| Date | Change | By |
|---|---|---|
| 2026-07-23 | Closed `ABORTED at P0.1`. Full-span `bbo-1s` estimates $147.57 (MNQ) + $125.33 (MYM) = **$272.91**, against a frozen §0 claim of $0.00 extrapolated from one month. Guard fired on the first command; $0.00 spent, no data touched. Diagnostic established per-day billing granularity and that events touch only 403 of ~1,630 instrument-days, making the frozen continuous-span shape strictly dominated. Successor scoped to the MYM add cohort alone. Third same-class §0 failure this session → standing lesson candidate proposed (§5). | Joshua (direction) + Claude Code (Opus 4.8) |
