**Theme:** _inbox
**Status:** ACTIVE — OFFICIAL corrected-null re-score complete: S1a (GC) NULL (driving L2,L4; obs at 8.4th pct of its own linear-ACF band — near-miss dissolved); S1b (CL) SIGNAL-GENERIC (69th pct, canon-attributed; L4 boundary-exact 6/8)
# Corrected-null re-score (OFFICIAL) — `H-RANGESTATE-GC-1` and `H-RANGESTATE-CL-1` under the frozen class battery

**Date:** 2026-08-18 · **Class:** RE-MEASUREMENT of already-disclosed looks (K unchanged)
**Spec:** [`2026-08-18-magnitude-persistence-corrected-null-battery.md`](../../../docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md)
(frozen `12877c4` before any scoring surrogate; **ADDENDUM-1** pre-official, all 16 items —
read A1–A16 before quoting anything here). Operator election **PROCEED** recorded per A16.
**Runner:** [`run_corrected_null.py`](run_corrected_null.py) (post-FIX-1/2/3, pilot-asserted
bit-identical scoring) · official JSON: [`corrected_null_results_official.json`](corrected_null_results_official.json)
· diagnostics: `diagnostics_{GC,CL}_official.json` (written to disk before any hit rate).
**Verification:** design panel `wf_ebc728eb-2ef` (4 lenses + synthesis); pre-official
verification `wf_e06ebc90-c3e` (4 lenses + synthesis; independent reimplementation matched the
pilot **bit-exactly, 44/44 quantities, both instruments**). Official seeds
`[20260818, {1,2}, 0..999]`, M=1000, IAAFT 100 iter, normal-scores domain — drawn once, here.

## 1. Official results

| | GC (S1a) | CL (S1b) |
|---|---|---|
| diagnostic gate (Spearman rank-ACF; limits 0.04/0.07) | PASS (med 0.0316 / p95 0.0509) | PASS (med 0.0276 / p95 0.0411) |
| frozen obs | 0.5299 | 0.6282 |
| surrogate band mean / [p5, p95] | 0.5548 / [0.5245, 0.5851] | 0.6189 / [0.5893, 0.6481] |
| **obs percentile in band** | **8.4th** | **69.0th** |
| p_upper / p_lower | 0.9161 / 0.0849 | 0.3107 / 0.6903 |
| L1 n-floor / L2 CI / L3 halves (carried) | ✓ / **✗ (0.4545)** / ✓ | ✓ / ✓ (0.5651) / ✓ |
| L4 by-year (NEW) | **FAIL** — 5 of 9 valid, required 7 | PASS — 6 of 8 valid, required 6, **boundary-exact** |
| L5 attribution | GENERIC (p_upper 0.9161) | GENERIC (p_upper 0.3107) |
| flags | none (broad-BORDERLINE note: p_lower within 0.02 of the 0.07 line, per A10(iv)/A14 — wording-layer only) | none |
| **VERDICT** | **NULL (driving: L2, L4)** | **SIGNAL-GENERIC** |

Both verdicts match ADDENDUM-1's expected outcomes exactly; no stop-and-investigate event.
Construction-sanity brackets fired **as pre-named in A13**: GC unconditional P(y=1) 0.4778
below its surrogate band [0.4877, 0.5099] (phase-locked panel-scale vol decline — biases GC's
conditional band UP ~+0.02 via the base rate) and CL bias-share marginally below (0.2067 vs
[0.2072, 0.2276]). Per A13, the GC lift line rides every SUB-LINEAR-adjacent statement: **real
GC conditional-minus-unconditional lift (+0.0521) sits at the 41st percentile of the surrogate
lift band — dead center.** AR(1) positive-control citation (design-phase): 1/20 at
p_upper ≤ 0.05, vs the invalidated block-shuffle's 20/20 false-clear.

## 2. S1a (GC) — the operator's question, answered officially (CASE A)

The obs sits at the **8.4th percentile** of what GC's own marginal + linear autocorrelation
produces with zero mechanism. **CASE A: the "near-miss" characterization dissolves.** The
original 3-of-4-limbs framing had it backwards — 0.5299 was not a real effect lacking precision;
it was *below* the zero-mechanism benchmark's center. Under the corrected battery S1a is a
clean two-gate NULL (L2 precision AND L4 regime stability — only 5 of 9 years above coin-flip;
per-year table now in evidence per O4, disclosed in §1's JSON). No SUB-LINEAR flag (p_lower
0.0849 > 0.05, the pre-estimated 1.3–1.5% flag probability did not realize); broad-BORDERLINE
vs the 0.07 line noted per A14, wording-layer only, and per A13 the lift-percentile line
identifies the low raw placement as predominantly a base-rate artifact of the band's upward
bias — not anti-clustering.

## 3. S1b (CL) — SIGNAL-GENERIC, with ADDENDUM-1's guard-rails (A6) binding

Presence passes as frozen (L2 0.5651; halves; **L4 at its frozen threshold: 6 of 8 valid
years, boundary-exact** — 2010 excluded at n_cond=14; 2013/2017 fail; one flipped year flips
the verdict, a symmetric fact). Attribution is decisively **GENERIC**: obs at the 69th
percentile of its own linear-ACF band — the predictability is real at the pooled construction
and attributable to generic volatility clustering (canon), not beyond-linear structure.
**What this verdict may NOT be quoted as (A6, verbatim rails):** not "regime-robust" beyond the
L4 operational sentence; not a mechanism (D22 GARCH sensitivity never run — GENERIC never
reaches it); not a discharge of MCL's mechanism-owed status; not a conditioner license (the O2
connecting arithmetic from the 4× cost hurdle is still owed); the old calm-subset placebo is
VOID in both directions (retired null). The drop-cluster diagnostic and per-year table are
co-quoted wherever this verdict travels: crisis>calm ordering stands (top years 2011/2016/2014);
the level-based calm/crisis disclosure buckets (calm 0.617 / crisis 0.649) differ from the
review's event-identity split (calm 0.537) on the 2014/2016 transition years — neither read
travels without its year list (A7).
**Routing:** counts toward slate §4 RESOLVED → **H-SLATE = RESOLVED**. Conditioner-engineering
follow-up **PARKED** by [`Q-CONDVAL-1`](../../../docs/briefs/closures/Q-CONDVAL-1-closure-falsified.md)
(`FALSIFIED` 2026-08-18; O2 discharged). Calm-regime (A7) / O3 / L4 boundary remain on the
finding's record; they do not reopen the engineering branch.

## 4. Battery disposition (the structural repair itself)

The corrected battery is the **standing battery for the magnitude-persistence class**. Its
first official application performed as designed: it caught what the invalidated shuffle could
not (attribution typing), added the regime axis the incident exposed (L4 — which is what
actually kills GC alongside L2), and its diagnostic gate + pre-registered interpretation table
held through a live prediction-miss without any outcome-conditional parameter movement (the
full fork record is ADDENDUM-1). S2's null still does not port (O1 — stage-1 cheap falsifier
first); S3 goes matched-day (decoupled). Audit-note structural repair: the corrected-null
design item is now DONE; skill-clause propagation landed with this commit.
