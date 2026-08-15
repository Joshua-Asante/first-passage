# `feature_space` and `K_total` Selection Justification — EURUSD Pattern-Enumeration Harness

**Date:** 2026-05-23
**Phase:** 3 (executing Reality-Check Harness ADR §2.2 lock template, `feature_space` + `K_total` fields)
**Chosen value:** `K_total = 450`
**Selection rule applied:** minimum-bucket-count cartesian product honoring all five ADR §5 Q-H2 dimensions (gap, range, sequence, holding, stop), with one structural narrowing within the sequence dimension (drop trivial all-up/all-down 3-bar patterns).

---

## 1. Source authority for the feature classes

ADR §5 Q-H2 (locked 2026-05-21, `docs/adr/2026-05-22-reality-check-harness.md`) scopes the binding feature classes:

> Feature space scope (binding for this Pre-Q): gap classes (gap-up / gap-down / no-gap, quantile-bucketed by gap size) × range classes (current-bar range quantile vs trailing-N median) × short bar-sequence patterns (2–4 bar sequences of direction/range/close-position signs). Holding periods enumerated within {1, 2, 4, 8, 16} bars. Stop conventions enumerated within {1×ATR, 2×ATR, structural}. Exact K populated at Phase 3 from cartesian-product count of the locked enumeration.

The ADR also locks `K_total_bound = [50, 500]`. Phase 3 must select a cartesian construction whose product lands inside that bound.

---

## 2. Cartesian dimensions and bucket counts

Five dimensions, with bucket counts chosen at the **minimum-defensible** level per dimension:

### D1 — Gap-sign class (3 buckets)

| Bucket | Definition |
|---|---|
| `GAP_UP` | (open[t] - close[t-1]) / close[t-1] ≥ +SMALL_GAP_THRESHOLD |
| `NO_GAP` | \|(open[t] - close[t-1]) / close[t-1]\| < SMALL_GAP_THRESHOLD |
| `GAP_DOWN` | (open[t] - close[t-1]) / close[t-1] ≤ -SMALL_GAP_THRESHOLD |

`SMALL_GAP_THRESHOLD` is the 20th percentile of `|gap_pct|` over the IS window, computed once at Phase 4 enumeration startup. Quantile size sub-buckets (e.g., "gap-up small" vs "gap-up large") are NOT used in this Pre-Q; they would multiply the cartesian past the 500 ceiling. If a `GAP_*` bucket survives §6 OOS gating, the follow-up Pre-Q (§12 of the parent Pre-Q) may stratify by size as a regime-decomposition step — not as a within-this-Pre-Q post-hoc split.

### D2 — Range-vs-trailing-median class (2 buckets, N=20)

| Bucket | Definition |
|---|---|
| `RANGE_ABOVE_MED` | (high[t] - low[t]) ≥ median over `range[t-20..t-1]` |
| `RANGE_BELOW_MED` | (high[t] - low[t]) < median over `range[t-20..t-1]` |

N=20 (≈3-4 trading days at H4) is fixed; trailing-N is not multi-valued. Half-and-above quartile sub-buckets (e.g., "≥ 1.5×" / "≤ 0.5×") are NOT used in this Pre-Q for the same K-ceiling reason as D1.

### D3 — Bar-sequence patterns (10 buckets: 4 two-bar + 6 three-bar)

Each pattern element is one bar; the sign is the close-direction (close[t] vs close[t-1]: U=up, D=down). Doji bars (close[t] == close[t-1] to floating-point exact) are unreachable on real H4 EURUSD log returns; if encountered they are mapped to U via the convention `close[t] >= close[t-1] → U`.

**2-bar sequences (4):** UU, UD, DU, DD
**3-bar sequences (6):** UUD, UDU, UDD, DUU, DUD, DDU

UUU and DDD are excluded with structural rationale: they are degenerate momentum patterns trivially captured at the holding-period level by a single-bar direction filter. Their inclusion would add 2 patterns whose hypothesis ("3 consecutive same-direction bars → continuation or reversal") is already exercised by the (single-bar-direction + long/short direction + 1-bar hold) cell elsewhere in the cartesian. The 4-bar sequences (16 patterns: 2^4) are excluded entirely with structural rationale: at H4 over the 6-year IS window, the expected occurrence rate per 4-bar pattern is ~150-300 bars; conditioned on the gap/range filters in this Pre-Q's cartesian, the per-pattern N drops near or below the §4 (b) gate floor of N≥50 trades on OOS. Underpowered cells dilute the Bonferroni denominator without contributing decision-grade evidence. Reopening 4-bar is a candidate follow-up Pre-Q (one with a longer IS window or a lower-K shape).

Pattern → direction-of-next-bar prediction is enumerated independently of the sequence sign — see D4 below. So both "after UU go long" and "after UU go short" are separate patterns.

### D4 — Direction (2 buckets)

| Bucket | Definition |
|---|---|
| `LONG` | enter long at next bar's open |
| `SHORT` | enter short at next bar's open |

Direction is independent of trigger: for every trigger (gap/range/sequence) there are two patterns, one in each direction. This is the bitter-lesson commitment: we do not assume gap-up implies momentum-long or mean-reversion-short; we enumerate both.

### D5 — Holding period (5 buckets)

`{1, 2, 4, 8, 16}` bars, per ADR §5 Q-H2 verbatim. Full set; no narrowing.

### D6 — Stop convention (3 buckets)

`{1×ATR(14), 2×ATR(14), structural}` where:
- `1×ATR(14)` — stop placed 1.0 × trailing-14-bar ATR from entry
- `2×ATR(14)` — stop placed 2.0 × trailing-14-bar ATR from entry
- `structural` — stop placed at the swing low (long) / swing high (short) of the trailing-5-bar window from entry

Full set per ADR §5 Q-H2 verbatim; no narrowing.

---

## 3. Trigger enumeration and K computation

**Trigger count = D1 + D2 + D3 = 3 + 2 + (4 + 6) = 15 triggers**

Each "trigger" is a single entry condition; patterns are formed by attaching direction (D4), holding (D5), and stop (D6) to a trigger.

```
K_total = N_triggers × N_direction × N_holding × N_stop
        = 15 × 2 × 5 × 3
        = 450
```

| Field | Value |
|---|---|
| `N_triggers` | 15 |
| `N_direction` | 2 |
| `N_holding` | 5 |
| `N_stop` | 3 |
| `K_total` | **450** |
| `K_total_bound` (ADR §2.2) | [50, 500] |
| In-bound? | ✓ (60 below ceiling) |
| Bonferroni per-pattern α | 0.05 / 450 ≈ 1.111e-4 |

---

## 4. Comparison table — rejected alternatives

| Candidate | Trigger count | K | Bound | Why not chosen |
|---|---|---|---|---|
| Naïve full cartesian (gap-quintile × range-quartile × seq2-4) | ≈ 41 | ≈ 1,230 | ✗ over ceiling | Quintile/quartile sub-buckets + 4-bar sequences both inflate K past 500. K>500 forces a post-hoc narrowing during enumeration, which is ADR §3 forbidden move #5 ("Selecting which metric to gate on after seeing results"). |
| **Chosen (K=450)** | 15 | **450** | ✓ in-bound | Minimum-bucket per dimension; one structural narrowing (drop trivial UUU/DDD). Full holding + stop cross. |
| Drop holding={1} (K=408) | 17 | 408 | ✓ in-bound | Avoids any sequence-dimension narrowing, but loses a meaningful holding-period DoF. 1-bar (4hr) holds are not obviously noise-dominated — at H4 EURUSD the average bar range is ~25 pips so a 1-bar hold has a non-trivial signal-to-noise. Joshua-rejected this on the basis of preserving the smaller-K (tighter Bonferroni) candidate. |
| Drop stop={1×ATR} (K=340) | 17 | 340 | ✓ in-bound | Avoids any sequence-dimension narrowing, but loses a stop convention DoF. The structural rationale ("1×ATR is below spread+slippage scale") was deemed weaker than the UUU/DDD-degeneracy rationale for the chosen K=450 candidate. Joshua-rejected. |

The K=450 candidate was selected by Joshua (CEO) via AskUserQuestion on 2026-05-23 before this brief was authored. The other three K values were surfaced with their structural narrowings; K=450 was preferred for tightest Bonferroni gate clearance combined with full holding/stop dimensional preservation.

---

## 5. Connection to standing doctrine

| Doctrine | Connection |
|---|---|
| ADR §5 Q-H2 (feature-space scope) | All five locked dimensions honored at minimum-bucket count |
| ADR §3 forbidden move #5 ("Selecting which metric to gate on after seeing results") | K is locked BEFORE enumeration; post-lock K-change requires new ADR per ADR §5 |
| Pre-Q §4 (a)–(d) gate (PF≥1.3, N≥50, DD-ratio≤1.5, p<0.05 post-Bonferroni) | Per-pattern α = 0.05/450 ≈ 1.111e-4 is achievable; smaller K (340, 408) would have a looser per-pattern α but lose dimensional coverage |
| ADR §2.3 Component B (registry append-only during enumeration) | Phase 4 registers all 450 patterns BEFORE running; mid-enumeration additions are §3 forbidden move #1 (Pre-Q "Expanding K mid-enumeration") |
| Pre-Q §5 #1 forbidden move (K is locked, final report cites locked K) | The Bonferroni denominator at §6 OOS evaluation will be K=450 verbatim; the audit hook (ADR §4 #5) enforces `wc -l < logs/enumeration.jsonl == 450` |

---

## 6. Disposition if revisited

Phase 3 should reject this `feature_space` / `K_total` and require a re-run if any of the following changes:

1. **The IS window changes.** SMALL_GAP_THRESHOLD (the 20th percentile of `|gap_pct|`) is a function of the IS window; a different window produces a different threshold and the gap-class definitions shift accordingly. The threshold is computed at Phase 4 enumeration startup once, not committed to the lock file (the lock file commits the *spec*, not the empirical value).

2. **Doji-handling becomes load-bearing.** The convention `close[t] >= close[t-1] → U` is asymmetric; if Phase 4 enumeration surfaces a pattern whose edge concentrates exactly on doji bars (close-exact-equal-to-previous-close), the asymmetric mapping may bias the result. Currently dismissed because real H4 EURUSD log returns are continuous-valued and exact-zero is unreachable; this is the load-bearing assumption.

3. **4-bar sequences are re-proposed.** Reopening D3 to include 4-bar (2^4 = 16 patterns) requires either (a) a longer IS window that raises per-pattern N above the §4 (b) floor, or (b) a different cartesian shape that excludes other dimensions to stay in-bound. Either way, a new ADR — not an inline `K_total` edit.

4. **Stop = 1×ATR is flagged as noise-dominated post-hoc.** If Phase 4 enumeration shows all 1×ATR-stop patterns systematically failing across triggers, the K=340 candidate (drop 1×ATR) becomes a defensible Phase-3-revisit. But this would close the current Pre-Q AMBIGUOUS or FALSIFIED first; the re-Phase-3 happens under a new Pre-Q, not as a mid-investigation amendment.

5. **The trivial-momentum rationale for excluding UUU/DDD is contested.** If a reviewer argues UUU/DDD are NOT trivially equivalent to (single-bar-direction + 1-bar-hold), the K=510 candidate (full seq3 enumeration) becomes a defensible re-Phase-3. The argument would need to be made BEFORE Phase 4 enumeration begins; post-hoc reinclusion is ADR §3 forbidden.

Disposition cases that do NOT invalidate this selection:

- Phase 4 enumeration produces a pattern with high in-sample PF that fails OOS gate. That's the gate working as designed (Pre-Q §6 FALSIFIED verdict); K is not on trial.
- Phase 6 OOS evaluation produces a result that survives in-sample MTC but fails on OOS. Same — the gate worked; K is not on trial.
- The Bonferroni method itself is contested. ADR §5 Q-H1 locks Bonferroni; switching MTC method is a new ADR, not a `K_total` revisit.

---

## 7. Cross-references

- Parent ADR: [`docs/adr/2026-05-22-reality-check-harness.md`](../../../docs/adr/2026-05-22-reality-check-harness.md)
- Parent Pre-Q: `preq_eurusd_pattern_enumeration.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/preq_eurusd_pattern_enumeration.md`)
- Sibling Phase 2 doc: [`avg_block_length_justification.md`](avg_block_length_justification.md)
- Lock file: [`harness_lock.json`](harness_lock.json)
- AskUserQuestion record: 2026-05-23 session, K=450 selected from 4 candidates (K=450 / K=408 / K=340 / other)
