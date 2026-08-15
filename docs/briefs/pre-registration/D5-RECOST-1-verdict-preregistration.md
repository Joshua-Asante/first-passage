# Stage-0 verdict pre-registration — D5-RECOST-1 (MNQ-native cost-law re-derivation)

**Status:** `STAGE-0 FROZEN · operator decisions made + GO given (delegated to CC, chat 2026-07-21)`.
This file freezes the window, the K-accounting decision, the economics basis, and the
binary gate **before** the OOS edge is measured. The run script
[`lab/archive/d5_recost_2026-07/run_recost.py`](../../../lab/archive/d5_recost_2026-07/run_recost.py)
is committed in the same freeze commit as this file; **RESULTS land in a later commit** — the
freeze-before-result ordering is git-checkable (§10 hook 1).
**Campaign:** D5-RECOST-1 — re-derive the D5 Baltussen-2021-JFE H1 Stage-2 cost-law gate on the
native-MNQ OOS window (same construct, same signal; cost geometry + fresh OOS edge only).
**Scoping:** [`D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md`](../rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md).
**Parent (closed):** [`D5-NQ-intraday-momentum-preregistration.md`](D5-NQ-intraday-momentum-preregistration.md)
(Stage-0 frozen 2026-07-15; construct + Stage 5-8 gates inherited **by reference**, unchanged).
**Loop of record:** STRATEGIC (discovery Stage-2 re-derivation). **Authored:** 2026-07-21 · CC (Opus 4.8), operator-delegated.

---

## §0 — Rule-0 reads (production source, verified 2026-07-21)

Reuses the scoping brief's §0 anchors (all read this session, unchanged since):
- [`lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md) @ `e1c51f0` — closed IS verdict (edge +1.4613 bp, hurdle 11.063 bp @ px 4013.5).
- [`lab/analysis/orb/d5_nq_intraday_mom_2026-07/baltussen.py`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/baltussen.py) @ `e1c51f0` — **the frozen construct**; `session_edges()` builds one H1 edge/session (`r_rod=ln(C_15:30/O_09:30)`, `r_last=ln(C_16:00/O_15:30)`, `edge=sign(r_rod)·r_last`, exit 16:00). Self-contained ET conversion; needs no volume-stitch on an already-single-symbol continuous frame. **This campaign changes nothing in this file.**
- [`lab/discovery/cost_mnq.py`](../../../lab/discovery/cost_mnq.py) @ `e1c51f0` — `hurdle_from_price`; hurdle = 4×(2×(cps+1-tick))/(px×$2), monotonic-decreasing in px (verified by read).
- [`lab/analysis/orb/d5_nq_intraday_mom_2026-07/series.py`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/series.py) @ `e1c51f0` — `cached_mnq_continuous_1m()` reads the already-cached OOS panel (`MNQ.v.0`, 2019-05-06→2026-07-16, 2,535,465 rows, $0.00 — [`PULL_LOG.md`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/PULL_LOG.md)). **No new pull.**
- [`core/firm_rules.py`](../../../core/firm_rules.py) @ `a53ee99` — `cost_per_side_usd`: Bulenox 0.61, MFFU_Rapid 0.95.

---

## §1 — The two frozen operator decisions (delegated to CC, chat 2026-07-21)

**Decision 1 — K accounting: REUSE the parent D5 `K_eff=1` binding; no fresh K charged.**
Rationale: one fixed construct, no new hypothesis or search-space; the signal is byte-identical
(`baltussen.py` unchanged). The sole new degree of freedom — window choice — is neutralized by
Decision 2 (single a-priori window). Charging "fresh campaign K" would be the *permissive* move
(resets the MNQ family's accumulated multiplicity); reuse is the conservative one. The MNQ family
K_banked stays where the parent left it (D5 banked K=1 as a closed non-survivor); this re-derivation
adds none.

**Decision 2 — window: full OOS `2019-05-06 → 2026-07-16`, edge AND hurdle measured jointly on it.**
Rationale: this is the **zero-discretion** choice — it is verbatim the window the parent pre-reg
already designated (§2, 2026-07-15: "statistical/realism OOS on native micro MNQ 2019-05-06:present"),
so selecting it introduces no new researcher freedom. It is also the **conservative** choice: its
blended median notional (~14.8k) yields a *higher* hurdle (~3.0 bp) than any recent-only cut, so a
pass is robust and a fail is not self-inflicted. Degraded-quality days flagged in `PULL_LOG.md`
(2020-02-27/28, 2020-06-30) are **defect-logged, not dropped** (3 of ~1,800 sessions).

Both decisions recorded **before** the OOS edge was measured (the run script is committed alongside
this file, unexecuted).

---

## §2 — Frozen search universe + design (Stage-0)

| Item | Frozen value |
|---|---|
| **Construct** | `baltussen.py::session_edges` @ `e1c51f0`, **unchanged**. `sign(r_rod)·r_last`, one RT/session, exit 16:00 ET. |
| **Instrument / data** | Native `MNQ.v.0` continuous, already-cached OOS panel. Single-symbol → `session_edges` applied directly (no volume-lead stitch). |
| **Window (frozen)** | `2019-05-06 → 2026-07-16` (full OOS). No sub-window search. |
| **Edge** | Fresh mean gross per-session `edge` on this window (the NEW measurement — unknown at freeze). |
| **Hurdle** | `hurdle_from_price(median(px_1530), firm_key)` — **primary `Bulenox_100K`** (cps $0.61, continuity with the closed verdict), **`MFFU_Rapid_100K`** (cps $0.95) reported alongside as a mandatory sensitivity, not a discretionary add. 1-tick slip/side, 4× multiple — all inherited unchanged. |
| **K_eff** | 1 (reused; no fresh charge — Decision 1). |
| **Gate** | Stage-2 cost-law only. Stage 5-8 (block size / DSR / temporal battery / placebo / realism / breadth) are **inherited frozen** from the parent pre-reg and run only on a PASS. |

---

## §R — Reachability attestation

The gate is a deterministic recomputation on cached data; "reachability" = does a plausible-true
world exist in which the measured OOS edge clears the OOS hurdle? **Yes:** the parent's frozen IS
edge (+1.461 bp) already sits at ~48.6% of the full-OOS hurdle (3.007 bp) and ~97% of the current-price
hurdle — a true world where the OOS-measured edge ≥ the OOS hurdle is not structurally foreclosed
(contrast DISC-CAMP-0, floor 2.05 > gross 1.79 = unreachable). **REACHABLE.** Honest caveat: reachable
≠ will-pass; the OOS edge may have decayed (search flagged ~50% post-publication decay; NY-Fed:
E-mini overnight drift ~zero since 2021), which is exactly what this run measures.

---

## §4 — Falsifiable hypothesis (H-D5-RECOST)

**H-D5-RECOST — if** the Baltussen H1 construct's fresh mean gross edge on the frozen full-OOS window
clears **4× the cost hurdle at that same window's median `px_1530`** (Bulenox_100K, 1-tick slip),
**then** Stage-2 PASS → route to the inherited-frozen Stage 5-8 pipeline; **otherwise** FALSIFIED —
the cost-geometry lever closes for this construct and the "narrows but does not close / edge decayed"
finding banks as a defect-log entry.

**Reject if:** OOS mean gross edge < 4× OOS hurdle (Bulenox basis).
**Accept if:** OOS mean gross edge ≥ 4× OOS hurdle (Bulenox basis).
**Ambiguous-hold if:** OOS session count insufficient for a stable mean-edge estimate (parent Default #3 `dsr_unreachable_low_n`) — not expected (~1,800 sessions).

---

## §5 — Forbidden moves (each genuinely tempting)

- **Switching to a more favorable sub-window (≥2023/≥2025/last-60) after seeing a full-OOS fail.** The window is frozen at full-OOS pre-result (Decision 2). A recent-window variant is a *separate*, freshly-pre-registered question, never an in-run re-pick (Q-ORB-FRIDAY-1 best-of-K scar).
- **Quoting the scoping brief's hurdle-only recency table (the "~97% of hurdle at current px" row) as a result.** That table repriced the hurdle against the *stale IS edge*; it is motivating, not a verdict.
- **Reporting only the Bulenox (cheapest) hurdle.** MFFU basis is a mandatory co-reported output (§2).
- **Treating a Stage-2 PASS as a survivor / deployable.** Stage 5-8 still gate (parent forbidden move #6).
- **Amending this gate after the number is visible** (Trap #12) — close + re-open a fresh Stage-0.

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` (Stage-2 PASS) | OOS mean gross edge ≥ 4× OOS hurdle (Bulenox_100K) on the frozen full-OOS window | Route to inherited-frozen Stage 5-8; report MFFU-basis hurdle as sensitivity |
| `FALSIFIED` | OOS mean gross edge < 4× OOS hurdle (Bulenox_100K) | Close; bank defect-log entry (cost-geometry lever closes for this construct); success-eligible |
| `AMBIGUOUS-HOLD` | OOS session count insufficient for a stable estimate | Name re-test condition; no in-place edit |

---

## §8 — Operator GO

```
DECISIONS + GO: 2026-07-21 / operator-delegated to CC (chat: "make the two operator decisions and run it")
  D1 = reuse K_eff=1 (no fresh K).  D2 = window 2019-05-06→2026-07-16 (full OOS), edge+hurdle jointly.
  Authorizes the Stage-2 re-derivation run on the already-cached MNQ OOS panel (zero pull, zero fresh K).
  Frozen BEFORE the OOS edge measurement (run script committed unexecuted alongside this file).
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Freeze-before-result: this pre-reg + run_recost.py commit must PRECEDE the RESULTS.md commit.
git log --format='%h %ci %s' -- docs/briefs/pre-registration/D5-RECOST-1-verdict-preregistration.md \
  lab/archive/d5_recost_2026-07/run_recost.py lab/archive/d5_recost_2026-07/RESULTS.md

# 2. Construct unchanged (frozen baltussen.py hash still e1c51f0-era; this campaign edits nothing in it).
git log -1 --format='%h' -- lab/analysis/orb/d5_nq_intraday_mom_2026-07/baltussen.py

# 3. Window frozen full-OOS (no sub-window in the run script's args).
grep -n "2019-05-06\|2026-07-16" lab/archive/d5_recost_2026-07/run_recost.py

# 4. Both firm keys reported (Bulenox primary + MFFU sensitivity).
grep -n "Bulenox_100K\|MFFU_Rapid_100K" lab/archive/d5_recost_2026-07/run_recost.py

# 5. Reproduce.
PYTHONPATH=lab;core python lab/archive/d5_recost_2026-07/run_recost.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-21 | Stage-0 FROZEN — D1 (reuse K_eff=1), D2 (full-OOS window), Bulenox-primary + MFFU-sensitivity economics, binary Stage-2 gate. Frozen before the OOS edge measurement (run script committed unexecuted). | Operator-delegated → CC (Opus 4.8) |
| 2026-07-21 | **RESULTS landed → `FALSIFIED`** (gate unchanged; recorded, not amended). OOS mean edge −0.33 bp < 3.01 bp Bulenox hurdle; edge decayed negative (corr +0.081→+0.024). See [`RESULTS.md`](../../../lab/archive/d5_recost_2026-07/RESULTS.md). | CC (Opus 4.8) |
