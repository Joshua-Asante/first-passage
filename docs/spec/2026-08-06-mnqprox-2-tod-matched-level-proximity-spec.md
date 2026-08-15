# `MNQPROX-2` — ToD-matched level-proximity discriminator (spec)

**Type:** Screening / construct spec (`docs/spec/`)
**Status:** `PHASE-0 CLOSED — VOID-POWER-anticipated` (2026-08-06). Design freeze still
stands as documentation; **PREREG / run not opened.** Census:
[`lab/analysis/c1/mnq_orb_level_proximity_tod_2026-08-06/PHASE0.md`](../../lab/analysis/c1/mnq_orb_level_proximity_tod_2026-08-06/PHASE0.md)
(`n_paired=15` < 30). Named by
[`MNQPROX-1` RESULTS](../../lab/archive/mnq_orb_level_proximity_2026-08-05/RESULTS.md)
Iterate.
**Q-ID (when opened):** `Q-MNQPROX-2` / cell slug `mnq_orb_level_proximity_tod_2026-08-06`
(fresh directory — do **not** amend `mnq_orb_level_proximity_2026-08-05/`).
**Authored:** 2026-08-06 · Cursor (Composer), operator-directed (*"write it up as a spec"*).
**Cost if later authorized:** **$0.00** — reuse parent `MNQFLOW-1` / `MNQPROX-1` S1 `tbbo`
window (`MNQ.v.0`, 2025-08-06 → 2026-08-04); no new schema, no MBP-10.
**K_intrinsic = 0** (structural contrast; never reads ORB outcomes — same posture as N14 /
`MNQPROX-1`).
**Parent chain:** N14 (`MNQFLOW-1` re-aimed) → `MNQPROX-1` VOID-TOD-CONFOUND (W6) → **this
spec**.

---

## §0 — Rule-0 reads (verified 2026-08-06)

| Source | Anchor | What it grounds |
|---|---|---|
| [`mnq_orb_flow_substrate_2026-08-05/RESULTS.md`](../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md) | `be6b94e` | **N14:** Δ = **−0.009367**, CI **[−0.013430, −0.005354]**, placebo \|.\| p95 **0.004166**, n=255. Limitation 1: level-proximity uncontrolled. Disposition watchlist-only. |
| [`mnq_orb_level_proximity_2026-08-05/RESULTS.md`](../../lab/archive/mnq_orb_level_proximity_2026-08-05/RESULTS.md) | (merged 2026-08-05) | **W6 fired:** ORB tod median **602** IQR **[600, 616]** vs PDH/PDL-first-touch median **694** IQR **[640, 771]**; \|gap\| = **92 min** > 60. Δ not computed. Iterate: ToD-matched re-proposal needs **fresh freeze**, not a re-cut. |
| [`mnq_orb_level_proximity_2026-08-05/PREREG.md`](../../lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md) | `b160ab2`+ | S1–S7, S4c/W6, FM-1…FM-8, Avenue A triple, K=0 reasoning. **This spec inherits all FMs and the W6 *gate*; it replaces only the level-arm *definition* that made W6 inevitable.** |
| [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) N14 · N15 · F2 GUARD | HEAD | N15 records the confound; F2 bars outcome-conditioned ORB filters. |
| [`docs/notes/2026-08-05-order-flow-probe-governance-question.md`](../notes/2026-08-05-order-flow-probe-governance-question.md) §7 | `a7dde66` | Survivor-tied clears Avenue A §6 condition 3; blind barred. |

**Cheap falsifier (already measured, not re-derived):** naïve PDH/PDL *first-of-session*
touches are ToD-late vs OR-gated triggers by construction. Any successor that keeps
"first touch of the day" as the level arm **will re-fire W6**. That is the load-bearing
design constraint this spec exists to satisfy.

---

## §1 — Question

**Is N14's against-the-break L1 signature ORB-boundary-linked, or generic approached-level
microstructure — when the level-contrast arm is forced into the same time-of-day regime as
ORB triggers?**

Symptom only: N14's largest caveat is undischarged; `MNQPROX-1` proved the naïve PDH/PDL
first-touch contrast cannot answer it.

---

## §2 — Why `MNQPROX-1` cannot be patched

`MNQPROX-1` S4 defined the level arm as the **first** 1m mid-touch of PDH and/or PDL in the
session (after exclusions). ORB triggers live in a tight post-OR band (~10:00–10:16 ET).
First PDH/PDL touches live later and wider. Session-level pairing without ToD matching
reintroduces the liquidity U-shape confound that N14's own clock-matched controls were
built to remove.

FM-4 / RESULTS Iterate forbid densifying, reweighting, or re-cutting that cell after W6.
**Successor = new freeze.**

---

## §3 — Frozen construct (proposed)

Inherit **unchanged** from `MNQPROX-1` unless noted:

| # | Element | Frozen value |
|---|---|---|
| S1 | Instrument / schema / window | `MNQ.v.0`, `tbbo`, 2025-08-06 → 2026-08-04 (identical to N14 / `MNQPROX-1`) |
| S2 | ORB event set | Parent N14 frozen triggers — reuse `events` where byte-identical; do not re-cut |
| S3 | Feature | `A = (bid_sz − ask_sz)/(bid_sz + ask_sz)`, signed toward breakout / approach, mean over **`[t−60s, t)`** |
| **S4′** | **Level-contrast set (REPLACES `MNQPROX-1` S4)** | See §3.1 |
| S4a | Exclusions | Same spirit as `MNQPROX-1` S4a: (i) near-OR coincidence ≤ **4 ticks**; (ii) within **15 min** of that session's ORB trigger; (iii) no prior session; (iv) zero usable TBBO in window. Plus (v) **ToD match failure** (no eligible level moment for that ORB trigger under S4′) |
| S4c | ToD disclosure | Mandatory: median + IQR of minute-of-session for ORB arm and level arm on the **paired** set |
| S5 | Statistic | `Δ = mean(A_ORB) − mean(A_level)`, session-block bootstrap 95% CI, **10,000** reps, seed **`20260806c`** (new; not a silent reuse of `20260805` / `20260805b`) |
| S6 | Placebo | Within-session label shuffle among paired moments, 1,000 reps, same seed → \|Δ\| p95 |
| S7 | Coverage / power | Report: ORB coverage; fraction of ORB triggers retaining a ToD-matched level moment; n_paired; n_ORB / n_level in paired set. **VOID-POWER** if n_paired < **30** **or** n_level < 50% of n_ORB in the paired set |

### §3.1 — S4′ ToD-matched level arm (the only material change)

**Level class (kept):** prior-day high / prior-day low (PDH/PDL), same session-boundary and
mid definition pins as `MNQPROX-1` S4 implementation-precision amendment
(prev RTH session max high / min low; mid = `(h+l)/2` on free 1m panel).

**Touch definition (changed):** a **level-approach moment** is any 1m bar (from the session's
**second** bar onward) whose mid enters within **1 MNQ tick (0.25 pt)** of PDH or PDL after
having been strictly farther on the prior bar — **not** restricted to the first such touch
of the day.

**ToD match (new, load-bearing):** for each ORB trigger at minute-of-session `m_orb` in a
session:

1. Candidate set = all PDH/PDL approach moments in that session surviving S4a(i)–(iv) whose
   minute-of-session `m_lvl` satisfies **`|m_lvl − m_orb| ≤ τ`**, with **`τ = 30` minutes**
   frozen here (generous vs ORB's ~16-min IQR width; not tuned post-data).
2. If multiple candidates: take the one with **smallest `|m_lvl − m_orb|`**; ties → earliest
   bar.
3. If none: that ORB trigger is **unpaired** (S4a(v)); counted in the coverage ledger, not in
   `Δ`.
4. Signing of `A` at the retained level moment: PDH → `long`, PDL → `short` (toward breaking
   through), identical to `MNQPROX-1`.

**Why not "restrict first-touch to the ORB IQR"?** ORB IQR is ~[600, 616]. First PDH/PDL
touches almost never land there (`MNQPROX-1` level median 694). That restriction would almost
certainly VOID-POWER without answering the question. Matching *any* approach inside ±τ of
each trigger keeps the PDH/PDL class while forcing ToD overlap by construction.

**W6 retained (highest precedence):** after assembly, if paired-set IQRs do not overlap **or**
`|median(ORB tod) − median(level tod)| > 60` minutes → `VOID-TOD-CONFOUND`; do not interpret
`Δ`. Under S4′ this should be rare; if it fires, the τ choice failed and the cell stops
(no post-hoc τ edit — FM-6).

---

## §4 — Hypothesis and gates

**H-MNQPROX-2.** At ORB-MNQ-1's frozen triggers, mean signed L1 `A` differs from mean `A` at
**ToD-matched** same-session PDH/PDL approach moments (`τ = 30`), under the same feature
window and inference stack as N14 / `MNQPROX-1`.

| # | Condition (precedence order) | Verdict | Disposition |
|---|---|---|---|
| W6 | S4c: IQR non-overlap **or** \|median gap\| > 60 min | `VOID-TOD-CONFOUND` | Report ledger + S4c only; stop |
| W5 | S7 VOID-POWER | `VOID-POWER` | Report ledger only; not re-cut |
| W4 | ORB-arm coverage < 90% | `VOID-COVERAGE` | Same as parent |
| W3 | CI includes 0 | `FALSIFIED` (generic-level reading) | **Pre-registered likely branch.** N14 consistent with generic approached-level microstructure under ToD match; do not tag `A` as ORB-specific |
| W2 | CI excludes 0 but \|Δ\| ≤ placebo p95 | `AMBIGUOUS-CONFOUND` | Same disposition as W3 |
| W1 | CI excludes 0 ∧ \|Δ\| > placebo p95 | `RESOLVED` (ORB-linked) | Watchlist may name ORB-boundary linkage. **Opens no gate**; filter use = fresh K-bound axis |

**Pre-registered expectation:** **W3** most likely (same as `MNQPROX-1` §8) — recorded so a
null is a discharged prediction.

---

## §5 — Forbidden moves

- **FM-1 — Reading ORB / level-touch trade outcomes** (win/loss, PnL, MFE/MAE joins).
- **FM-2 — Emitting per-trade / excursion surfaces** a successor could tune a filter on.
- **FM-3 — Converting a positive into a fifth ORB conditioning gate** (F2 GUARD).
- **FM-4 — Second cell inside the eventual freeze:** no alternate level class (VWAP, round
  numbers, session H/L, …), no τ sweep, no MBP-10, no second instrument, no window widen.
  Each needs its own authorization.
- **FM-5 — Running before operator GO** and before Phase-0 power census (§7).
- **FM-6 — Editing τ, W6 threshold, seeds, or S4′ after seeing data.**
- **FM-7 — Patching `MNQPROX-1` in place** instead of a fresh directory / PREREG.
- **FM-8 — Quietly rewriting N14 / N15 as ORB-specific before this cell resolves.**
- **FM-9 — Skipping Phase-0** because "τ matching guarantees ToD overlap" — W6 still runs;
  power may still fail.

---

## §6 — Avenue A · K · cost

**Avenue A §6 triple:** depth-shape ✓ · not fill-trivial ✓ · **survivor-tied ✓** (ORB arm =
`ORB-MNQ-1` frozen triggers; level arm is an in-session contrast control). Same clearance
shape as `MNQPROX-1`.

**K_intrinsic = 0:** structural contrast; FM-1 removes tradeable emission. Selection honesty:
named after N14 W1 and `MNQPROX-1` W6 — follow-up contrast, not independent discovery of `A`.
Gate conversion inherits neither K=0.

**Cost:** $0 if parent `tbbo` cache intact; estimate-only dry-run before any pull.

---

## §7 — Execution sequence (when operator elects)

1. **Phase-0 power census (free 1m panel only, $0, before GO):** count, under S4′/S4a without
   TBBO, how many ORB triggers retain a ToD-matched PDH/PDL approach at `τ = 30`. If projected
   n_paired < 30 → **do not open PREREG**; record VOID-POWER-anticipated and stop (mirrors
   `Q-FVGFLOW-1` Phase-0 discipline).
2. Operator GO on the run (Avenue A; cache reuse ≠ new entitlement).
3. Fresh `PREREG.md` in a new analysis dir, committing this spec by reference; freeze before
   any `A` contrast quantity.
4. Harness + hand-computed tests (S4′ match, S4a, S4c, W6) green before real quotes.
5. Single run → RESULTS → board writes (STATE, `MNQ.md` N14/N15 amendment, SESSIONS, CATALOG).

**Not in scope of this spec file:** harness code, PREREG freeze commit, or GO.

---

## §8 — Operator ratification block

This spec is **PROPOSED**. It becomes the binding design for `Q-MNQPROX-2` only when the
operator records a one-line GO to (a) run Phase-0, and if Phase-0 clears, (b) authorize the
PREREG freeze + run. Until then it is documentation of the owed successor, not a live probe.

Suggested affirmation: *"Phase-0 MNQPROX-2 on the free panel; if n_paired≥30, freeze PREREG
and GO the $0 tbbo reuse."*

---

## §9 — Audit hooks

```bash
# Parent W6 numbers still on record
rg -n "92|VOID-TOD-CONFOUND|694" lab/archive/mnq_orb_level_proximity_2026-08-05/RESULTS.md

# This spec freezes τ=30 and S4′ (not first-touch-only)
rg -n "S4′|tau|τ = 30|ToD-matched" docs/spec/2026-08-06-mnqprox-2-tod-matched-level-proximity-spec.md

# No outcome columns in closed outputs
rg -n "win/loss|MFE|MAE|PnL" docs/spec/2026-08-06-mnqprox-2-tod-matched-level-proximity-spec.md

# Cost dry-run (FREE; never pull for estimate)
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate --symbols MNQ.v.0 \
  --stype continuous --schema tbbo --start 2025-08-06 --end 2026-08-04
```

---

## Amendment log

- **2026-08-06 — PROPOSED.** Spec authored to land on PR #665 alongside `Q-ICTSTOP-1`. Named
  by `MNQPROX-1` Iterate; design replaces first-of-day PDH/PDL touch with τ-matched approaches
  so W6 is satisfiable by construction. Run not authorized.
- **2026-08-06 — Phase-0 CLOSED (`VOID-POWER-anticipated`).** Operator GO for Phase-0 only;
  census `n_paired=15` < 30 on free panel. Status flipped; §§3–6 frozen text byte-intact
  (FM-6). No PREREG.
