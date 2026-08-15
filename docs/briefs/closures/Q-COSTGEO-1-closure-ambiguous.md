# Q-COSTGEO-1 — Closure: `AMBIGUOUS-ALIGNMENT` (frozen-item defect found at Phase 0, pre-pull)

**Verdict:** `AMBIGUOUS-ALIGNMENT` — P0.1 passed its stated test but produced a finding that invalidates a **frozen** §2 rule. Closed and re-issued rather than amended (Known Trap #12).
**Closed:** 2026-07-23 (same day as authoring + signature)
**Pre-registration:** [`Q-COSTGEO-1-verdict-preregistration.md`](../pre-registration/Q-COSTGEO-1-verdict-preregistration.md) — `FROZEN`, signed 2026-07-23 / JA, freeze commit **`a51ce0a`** (2026-07-23 19:08:50 -0400)
**Successor:** [`Q-COSTGEO-2-verdict-preregistration.md`](../pre-registration/Q-COSTGEO-2-verdict-preregistration.md) — one row changed; all other frozen items carried verbatim.
**Spend:** **$0.00.** No pull. No `bbo-1s` data touched. K=0, no manifest.
**Live effect:** **none.** c1 rung stays WATCH-1 0.50× / disarmed; no cost constant changed; lock HELD.

---

## 1. What P0.1 established (banked, carried into the successor)

Panel `Date and time` → UTC mapping, anchored against the UTC-stamped 15m bar panel by testing whether entry prices fall inside the containing bar's `[low, high]`:

| Hypothesis | MYM (n=261) | MNQ (n=266) |
|---|---|---|
| **`America/New_York` (DST-aware)** | **96.2%** | **97.4%** |
| `UTC-4` fixed | 64.8% | 68.8% |
| `UTC-5` fixed | 53.6% | 48.9% |
| `America/Chicago` | 31.5% | 26.7% |
| `UTC` (naive) | 0.8% | 1.1% |

**Verdict: the panel is stamped in `America/New_York`, DST-aware.** This is a **banked input** for the successor, not a re-derivation.

**The gate justified itself twice.** A naive UTC read fails at ~1% — obvious and self-announcing. The dangerous case is the **fixed `UTC-4` shortcut at ~2/3**: right often enough to survive spot-checking, wrong on every DST boundary. That is the silent-misalignment class the blocking gate exists to catch, and it would not have announced itself in the output.

---

## 2. The defect that closes the instrument

A second test discriminated the fill convention — do entry prices equal the stamped bar's open or close?

| Match | MYM (n=261) | MNQ (n=266) |
|---|---|---|
| price == close of stamped bar | **0.0%** | **0.0%** |
| price == open of stamped bar | **0.0%** | **0.0%** |
| price == open of next bar | 27.2% | 8.3% |
| price ∈ `[low, high]` of stamped bar | 96.2% | 97.4% |

**Entries are intrabar stop fills, not bar-boundary market orders** — correct and expected for a breakout construct, and confirmed by the pattern (inside the range essentially always; equal to a boundary essentially never).

Therefore **the stamped timestamp identifies the *bar*, not the *fill instant***, and the frozen §2 rule —

> *Quote selection | The last `bbo-1s` record at or before the event's UTC timestamp.*

— samples the book at the bar's **opening second**, up to 15 minutes before the fill.

### Why this is disqualifying rather than merely imprecise

The bias is **directional and lands on the deciding quantity**:

- **D2 (half-spread)** barely moves intrabar on MYM/MNQ — this component would survive.
- **D1 (inside-sufficiency)** moves enormously. An **add** fires exactly when a stop cascade is running, which is when the book is thinnest. Sampling at bar-open measures depth at a **calm** moment.
- Inflated D1 suppresses **`AMBIGUOUS-NEEDS-DEPTH`** (fires on D1 < 90%) **and** weakens the evidentiary basis for **`FALSIFIED-UNDERSTATED`**.

So the frozen rule systematically suppresses **both** non-benign verdicts, on the cohort (67-lot MYM / 30-lot MNQ adds) that carries the entire decision. A run under it would have been biased toward `RESOLVED-CONSERVATIVE` — the comfortable answer — by construction.

---

## 3. Why closed-and-re-issued rather than amended

§2 is a **frozen** row of a pre-registration signed 2026-07-23. Trap #12 forbids amending frozen items once the instrument is live, *regardless of whether any result has been seen* — the discipline is that the rules do not move, not that they do not move after data. Editing §2 in place would have been the single most defensible-looking violation available: pre-run, well-motivated, and invisible in the final artifact.

The successor changes **exactly one row** and carries every other frozen item verbatim (§2 of the successor lists them).

---

## 4. What survives intact

Schema `bbo-1s` ($0.00) · span 2020-01-06→2026-06-30 · event set (MYM 267 / MNQ 284 entries + paired exits) · cohorts base-vs-add (MYM 232/35, MNQ 237/47) · live sizing pinned to `f2_floors.json` (MYM 9/67, MNQ 3/30) · the two-sided falsifier with the dangerous direction firing the action · the floor asymmetry (measured-below-modeled licenses no hurdle cut) · `mbp-10` ring-fenced as a separate priced decision · **K=0, no manifest, no DSR floor**.

The motivating production findings are unchanged and remain the reason to run the successor: `SLIPPAGE_TICKS_PER_SIDE = 1.0` is 35–45% of the round trip and unmeasured; `cost_es.py` carries a **4×-apart** frozen passive model in the same repo; **no `cost_mym.py` exists**; live adds are 7.5–10× base.

---

## 5. Process record

**PD-1 (this instrument).** A quote-selection rule was frozen on an unstated assumption — that a TradingView List-of-Trades timestamp marks the fill instant. It marks the bar. The assumption was never written down as an assumption, so it was never a candidate for testing; it surfaced only because P0.1 happened to require a price-vs-bar comparison for an unrelated purpose (TZ resolution).

**Lesson candidate (brief-authoring):** *a measurement rule that reads an external artifact's timestamp must state, as a testable §0 claim, what that timestamp denotes* — trade instant, bar label, ingestion time, or settlement. Timestamp semantics are a Tier-1 constant when a measurement is anchored on them, and this repo already carries the adjacent scar ([[reference_bar_export_epoch_utc]] — "Signal epoch UTC even on ET charts"; [[reference_platform_display_tz_edt]]). Dated anchor: this closure. Cost: one authoring cycle + one operator signature, $0 spend, zero data touched.

**Standing note — second Phase-0 halt this session.** Q-C1PANEL-1 and Q-COSTGEO-1 both died at a blocking Phase 0 before spend. That is the gate working, not a pattern of bad instruments: in both cases the defect was an unverified premise about an artifact's *shape* (panel span; timestamp semantics) rather than about the question's merit. Both questions remain worth answering; one was re-issued, one was closed permanently on data physics.

---

## 6. Audit hooks

```bash
# Freeze predates every Phase-0 read.
git log -1 --format='%h %ci' a51ce0a

# Reproduce the P0.1 TZ result (read-only; panel CSVs are gitignored, primary checkout).
# America/New_York must dominate; UTC ~1%; UTC-4 ~2/3 (the dangerous near-miss).

# The frozen rule that closed this instrument.
grep -n "last .bbo-1s. record at or before" docs/briefs/pre-registration/Q-COSTGEO-1-verdict-preregistration.md

# The successor changed exactly one row.
grep -n "price-anchored\|fill localization" docs/briefs/pre-registration/Q-COSTGEO-2-verdict-preregistration.md

# No pull ever ran under this instrument.
ls -d lab/analysis/c1_cost_geometry_* 2>/dev/null | wc -l   # must be 0
ls discovery_manifests/ | grep -i costgeo || echo "no manifest (correct — K=0)"
```

---

## 7. Change history

| Date | Change | By |
|---|---|---|
| 2026-07-23 | Closed `AMBIGUOUS-ALIGNMENT`. P0.1's stated gate PASSED (TZ = `America/New_York`, 96.2/97.4%) and is banked for the successor; the same read established that entries are **intrabar stop fills**, invalidating the frozen §2 quote-selection rule, which would have sampled the book up to 15 min before the fill and suppressed both non-benign verdicts. Closed rather than amended per Trap #12. $0.00 spend, no data touched, no live effect. | Joshua (direction) + Claude Code (Opus 4.8) |
