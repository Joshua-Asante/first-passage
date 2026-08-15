**Theme:** legacy
**Status:** ACTIVE — Guardian XAUUSD filter-validity sweep harness
# Guardian XAUUSD — filter-validity sweep harness

**Built:** 2026-06-20 · **Loop:** INQHIORI / OUTER (selection-level, feeds a low-reversibility keep/remove read)
**Status:** harness BUILT + self-tested. **BLOCKED on two operator inputs** before any real verdict:
1. a **filters-region isolation export** (you produce in TV), and
2. the **frozen keep-gate** (your live XAUUSD round-trip cost).

This is the in-repo realisation of the `filter_validation.py` CC-handoff brief, landed
through Rule 0. It tests, one filter at a time, whether a Guardian filter removes a real
structural drag on edge or just a slice that happened to hold bad trades.

---

## Rule-0 landing of the brief (what was real vs confabulated)

The brief was authored without repo access. Verified against the actual tree:

| Brief asset | Reality |
|---|---|
| `scripts/filter_validation.py` (the harness) | Not in repo; lived only in `~/Downloads`. Ported here verbatim ([`filter_validation.py`](filter_validation.py)); self-test `ALL SELF-TESTS PASSED`. **Genuine + sound.** |
| `scripts/selection_tests.py` (5a–5e) | **Never existed** (no git history). The `[SWAP]` component tests inlined in `filter_validation.py` stand; there is nothing in-repo to swap to. |
| `scripts/step0_battery.py` | **Never existed.** Built here as [`step0_battery.py`](step0_battery.py) (bespoke, per the documented "real tooling = per-investigation `lab/analysis/` harness" pattern — XAUUSD ledger 2026-06-15). |
| `ops/instruments/XAUUSD.md` read | Exists (created 2026-06-15). Read; F1/F3 anchors reused. |
| Feed = Pepperstone, **not** Dukascopy | Brief got this **right** (unlike the 2026-06-15 brief). Canonical Pepperstone TV CSV only. |

Same confabulation class as the 2026-06-15 CGB handoff (`step0_battery`/`selection_tests`/
`plateau_tracker` named at `scripts/`, none real). Logged again here.

---

## The load-bearing design departure: region isolation (NOT "filters-OFF")

The brief's method needs the **excluded bucket** — the trades a filter removes, with their
realized R. Its implicit model is a single trade population with a row-wise filter label.
**Guardian violates that badly:**

- Single position at a time, and **50.2% of trades span >1 calendar day** (33.5% ≥1 day,
  28.1% ≥2 days, P90 hold = 10.5 days, max 15.3). Measured on the locked panel.

So a naïve **all-filters-OFF re-export is invalid**: any re-admitted trade seizes the one
position slot for days and **cascade-displaces** downstream locked trades. The result is
neither the locked book (kept contaminated) nor a clean excluded bucket.

**Clean design = region isolation:**
- **KEPT bucket** = the existing locked book (`…1bb97.csv`, N=203) — already on disk, untouched.
- **EXCLUDED bucket** = Guardian run **restricted to one filter's excluded region** (e.g. Wed+Fri
  only, all other filters locked). Self-consistent, uncontaminated by the kept book.

R is **compounding-invariant** (`R = net_usd/(0.0034·equity_before) = price_move/stopDist`), so
concatenating R from two separately-de-compounded exports is valid. Each export is
de-compounded on its own cumulative equity path.

### Per-filter cleanliness ladder (which verdicts to trust)

| Filter (from `guardian_gold_v5.5.pine`) | Isolation export | Cleanliness |
|---|---|---|
| **Day** — keep Mon/Tue/Thu (Wed/Fri off) | Wed+Fri only, all else locked | **CLEAN** — excluded region shares no slot with the kept book. Highest-value test (drops 2 of 5 weekdays). Do FIRST. |
| **Session** — NY-Ext 08–16 | `useSession=false`, day+hours locked; software-extract hour<8 \| hour>16 | **MILD contamination** — out-of-session trades displace within the run; flagged in report. |
| **Hour blocks** — Tue H08 / Mon H08 / Mon H09 / H12-entry / H12-signal-day | all four blocks off, day+session locked; extract blocked cells | **HEAVY contamination** — blocked cells are embedded inside otherwise-traded days; an un-blocked H08 trade can hold into and displace later trades even within isolation. Verdicts carry a contamination tag; treat as directional, confirm with single-block re-export if a cell flags. |

**Stationarity interaction (documented):** `_stationarity` sorts the concatenated panel by
time and splits halves/thirds. The isolation export **must span the full 2022→2026 panel
window** or late segments get zero excluded trades (`nan`) and auto-route to
CONTINGENT-FORWARD. Wed/Fri trades naturally span the period; just export the same chart
range as the baseline. Step-0's `date_span_coverage` check **hard-fails** an excluded export
that covers <80% of the kept-book span, so a time-clustered export is caught up front rather
than producing a spurious verdict.

---

## Operator inputs still required

### 1. Day-filter isolation export (TV → Pepperstone XAUUSD 15m)

Open `guardian_gold_v5.5.pine` (BACKTEST mode), set **only** the day filter to Wed+Fri,
leave everything else at locked values, export **List of Trades** over the **same window as
the baseline** (2022-01-11 → 2026-05-14):

Set the day filter to Wed+Fri only; leave every other locked input (session, hour blocks,
risk/core parameters) at its locked value — exact values redacted from the public tree
2026-08-14, see the private archive. Feed/TF: Pepperstone, XAUUSD, 15m, same chart history
as the baseline export.

This yields the **marginal day-filter excluded bucket**: trades that pass every OTHER filter
and fail only the day filter. Save anywhere; pass the path to `run_sweep.py day`.

### 2. Frozen keep-gate (OQ1)

The 0.08 default is **forbidden** (§0.5e). At the verified $5.68 median stop, the gate maps to
the round-trip cost: **$0.30→0.053, $0.50→0.088, $0.70→0.123** (run `keep_gate.py`). Supply the
live FXIFY/DXTrade XAUUSD round-trip cost (spread+commission, USD) to freeze it. This is a
pre-registered constant — set before the sweep, never moved after a verdict.

---

## Run

```bash
python filter_validation.py          # classifier self-test -> ALL SELF-TESTS PASSED
python r_pinning.py                  # R-pinning vs ledger F1 anchor (figures redacted from public tree — see private archive)
python step0_battery.py              # panel-integrity battery self-test (+ negative control)
python keep_gate.py                  # cost-law candidate gates (UNFROZEN)
python run_sweep.py --selftest       # full pipeline on a SYNTHETIC excluded bucket (wiring)

# real run, once both inputs are in hand:
python run_sweep.py day  /path/to/WEDFRI_ISOLATION.csv  --keep-gate <frozen>
```

## Files
- `filter_validation.py` — the classifier (ported verbatim; PreReg constants, FilterSpec, disposition ladder).
- `r_pinning.py` — TV export → compounding-invariant R panel (reuses the verified `xauusd_cgb_2026-06-15` method).
- `step0_battery.py` — panel-integrity battery (minute/day/hour census, n-bounds, duplicate/wrong-file).
- `keep_gate.py` — cost-law keep-gate derivation (UNFROZEN pending broker cost).
- `run_sweep.py` — orchestrator: kept locked book + excluded isolation export → Step-0 → classify → report.

## Forbidden moves (from the brief, binding here)
No moving a PreReg constant after a verdict; no guessing a filter's family/`searched`; no
substituting a different feed for the isolation export (Jaccard-0.96 trap); no re-running or
re-optimising the strategy or touching locked Pine; CONTINGENT-FORWARD means freeze + forward-test
on an independent path, **not** delete the filter now; test exactly Guardian's filter set; never
collapse a verdict to a bare pass/fail — the nulls-alive ledger is the product.

## Persist on completion
Report → `docs/briefs/Q-FILTER-SWEEP-XAUUSD-<date>.md`; one durable disposition line per filter →
`ops/instruments/XAUUSD.md`. No `core/` touch, no lock/allocation change.
