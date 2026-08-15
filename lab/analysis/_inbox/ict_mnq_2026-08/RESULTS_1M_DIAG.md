# Q-ICT-MNQ-1 / Part C — RESULTS: 1M diagnostic discrimination

**Date:** 2026-08-04 (measurements ran overnight 08-03 → 08-04)
**Pre-registration:** [`PREREG_1M_DIAG.md`](PREREG_1M_DIAG.md) — frozen at commit `5dc247b`,
before any M1/M2/M3 number existed and before the ES pull.
**Question:** which surviving hypothesis can actually produce US500's **0 fills in 247
attempts**, given the Part B finding that MNQ 1m displacement FVGs retrace to mid 59.06% of
the time? The frozen bar: a mechanism **EXPLAINS** 0/247 only at a fill rate ≤ **1.2%**
(the largest p with `(1−p)^247 ≥ 0.05`); > 20% is **REFUTED-AS-EXPLANATION**.
**Cost:** $0 (ES pull estimated and billed $0.00) · K=0 · no manifest · Cap seat untouched.
**Runner:** [`run_1m_diag.py`](run_1m_diag.py), 42 unit tests incl. a flag-equivalence pin of
the heap-based raid scan against the archived `detect_raid` semantics.

---

## 1. Verdict — all three testable hypotheses REFUTED; (c) leads by elimination

| Cell | Hypothesis | Measured | Frozen read |
|---|---|---|---|
| **M1** raid-conditioned rate, d=0 | (a2) population conditioning | **59.01%** (n=55,604) | **REFUTED-AS-EXPLANATION** |
| **M2** joint, min over d∈0..8, conditioned | (a1∧a2) arm-delay timing, best case | **55.91%** (d=8) | **REFUTED-AS-EXPLANATION** |
| **M3** ES, exact US500 window 06-24→26 | (b) index behavior in that window | **62.33%** (139/223) | **REFUTED-AS-EXPLANATION** |

**Pre-committed joint reading fires:** with (a) and (b) refuted, **(c) platform-side leads
by elimination** — a defect in the deployed (now lost) `ict_1m_execution_DRAFT.pine`, TV's
strategy-tester fill handling on that chart, or the retired Pepperstone US500 CFD feed.
These three cannot be separated further: the script is lost and the feed is retired.

**No plausible price-behavior story survives.** The per-attempt fill probability needed to
produce 0/247 is ≤1.2%; every measured cell sits at 45× that or higher, on two instruments,
across eight years each, including the exact calendar window in question.

---

## 2. What the measurements showed (and the two genuinely new facts)

**M1 — raid-conditioning does nothing to the retrace rate.** 43.4% of MNQ displacement FVGs
(55,604 of 128,089) pair to a `pvLen=2` pool sweep within `raidWin=8` bars per the declared
same-direction mapping. Their retrace rate — **59.01%** — is statistically indistinguishable
from the unconditioned 59.06%. Post-sweep FVGs are not a "continuation-prone" subclass.

**M2 — the arm-delay curve is nearly flat, which is the more surprising fact.**

| d (bars late) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| unconditioned | 59.06% | 58.95% | 58.34% | 57.73% | 57.18% | 56.75% | 56.42% | 56.22% | 56.10% |
| raid-conditioned | 59.01% | 58.82% | 58.25% | 57.69% | 57.08% | 56.67% | 56.28% | 55.99% | 55.91% |

An order armed **eight minutes late** still fills 56% of the time in its 6-bar window. The
naive story — "retraces are fast (median 2 bars), so late orders miss them" — is wrong
because mid-touches are not one-shot: price revisits the FVG mid repeatedly. Timing cannot
rescue the 0/247 fact even in its most generous cell.

**M3 — ES mirrors MNQ everywhere, including the exact window.** Full era 59.88%
(n=124,748); per-year 58.8–61.6% (2019–2026, no regime dependence); and in
**2026-06-24→26 specifically, 62.33%** — *above* its own full-era average. One
order-of-magnitude consistency note, not proof: the reconstruction found 223 eligible FVGs
on ES in that window, the same order as the 247 orders the deployed strategy armed on US500
over the same days.

---

## 3. Consequences

1. **The archived closure's mechanism claim is now dead twice over.**
   `CLOSURE-1M-INSUFFICIENT-N.md` §5 attributed 0/247 to an instrument-general price law
   ("displacement FVGs continue rather than retrace within 6 bars") and predicted it "would
   very likely recur on NAS100." Part B refuted the law on MNQ; Part C closes every escape
   route the law's defenders could take (conditioning, timing, that-specific-window) and
   adds ES. The prediction was wrong at the mechanism level, not merely miscalibrated.
2. **The operational fill wall on MNQ is gone.** Nothing in the measured price behavior of
   MNQ (or ES) prevents a `limit-on-return / mid / retraceK=6` entry from filling. What
   remains against a 1M execution design is everything else — no validated edge (that was
   never established anywhere), the K arithmetic (family bank 2 → `K_eff` 3 → DSR floor
   0.98 vs Cap 1.0), and the Cap seat. Per the frozen outcome map, **that decision is now
   live for the operator, with this diagnostic as its evidence base — and it is not opened
   here.**
3. **A standing caution for any future TV-strategy-tester result on this family:** the one
   place the 0-fill behavior is now localized to is the deployed-script/platform side. A
   future 1M-class design should treat TV-tester fill behavior as something to *verify
   against native data*, not something to trust — consistent with the repo's existing
   offline-fill-ports-vs-native-arbiter lesson, but pointing in the opposite direction
   (here the *platform*, not the offline port, is the suspect).

## 4. Scope limits

- **Nothing here measures edge.** Fill mechanics only; no P&L was computed anywhere in
  Part C. A 59% fill rate says orders *fill*, not that filled orders make money.
- The chain reconstruction omits the DOL/stop geometry filters (declared; ≤~5% population
  trim on US500's own B4 counts) and uses bar-level touch semantics (declared, shared with
  Part B).
- (c) is a **residual by elimination**, not a measured finding — the script is lost and the
  feed retired, so it is not further testable. The honest statement is "0/247 was
  platform-side," not "the script had bug X."

## 5. Reproduce

```bash
python -m pytest lab/analysis/_inbox/ict_mnq_2026-08/ -q          # 42 passed
python lab/analysis/_inbox/ict_mnq_2026-08/run_1m_diag.py <mnq_1m.parquet> <es_1m.parquet>
git diff HEAD -- lab/archive/ict_cascade_2026-06-18/       # must be EMPTY
```

ES data (gitignored, regenerable at $0.00):

```bash
python lab/databento_fetch/db_fetch.py pull --symbols ES.v.0 --stype continuous \
  --schema ohlcv-1m --start 2019-05-06 --end 2026-08-03 --phase oos --max-cost 1.00 --out es_1m.parquet
```
