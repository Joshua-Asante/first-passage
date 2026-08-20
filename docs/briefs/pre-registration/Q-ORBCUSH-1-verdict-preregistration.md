# Q-ORBCUSH-1 — Verdict pre-registration

**Frozen:** 2026-08-20, before Phase 1 runs. Byte-unedited from this point forward — amendments via
a fresh Q, never an in-place edit (brief-authoring Known Trap #12).

---

## Classifier

**Primary:** trailing mean-R of ORB-MNQ-1's own realized trades — rolling window over the trade
sequence (not calendar days; ORB-MNQ-1 triggers on ~99% of sessions so the distinction is minor,
but the classifier is trade-indexed to match how mean-R is naturally computed), `.shift(1)`-equivalent
so day *t*'s classification uses only trades strictly before *t*. No full-sample or global-percentile
threshold — the bucket-split threshold is the trailing series' own running median up to that point
(an expanding, causal median, matching the stress-test variant that held up best in the prior
vol-regime round), never a full-sample statistic.

**Secondary (fallback only, per H-ORBCUSH's Ambiguous-hold clause):** trailing cost-to-range fraction
(round-trip cost ÷ trailing mean session range), same causal-window discipline, computed at daily/
session granularity rather than trade-count granularity.

## Three pre-registered windows (all three run; verdict uses all three, none dropped)

| Window | Rationale |
|---|---|
| W1 = 20 trading sessions | Short — matches the shortest window tested in the prior vol-regime round, where it was the one that inverted direction. Included specifically so a real short-window instability can't be avoided by only testing longer windows. |
| W2 = 63 trading sessions (≈1 quarter) | Matches the primary window from the prior vol-regime round. |
| W3 = 126 trading sessions (≈2 quarters) | Matches the long window from the prior vol-regime round, where date-purity was highest but flagged as risking circularity (collapsing toward a re-derivation of the calendar split). Included so that risk is checked directly on this classifier too, not assumed absent. |

## Frozen thresholds (byte-identical to Q-ORBCUSH-1 §4/§6 — restated here as the artifact of record)

- **Date-correlation pass condition, per window:** higher-edge bucket's post-2021-09-28 date
  fraction ≥ 75% AND lower-edge bucket's post-2021-09-28 date fraction ≤ 40%.
- **Direction-stability condition:** the gate-clearance direction (higher-edge bucket clears
  bust≤3.0%/pass≥50% under cushion sizing at k=1; lower-edge bucket does not) must be the same
  sign at all three windows — one sign-flip anywhere is disqualifying, full stop, no exceptions.
- **Accept H-ORBCUSH (→ RESOLVED):** date-correlation clears at ≥2 of 3 windows AND direction is
  stable (no sign-flip) across all three.
- **Reject H-ORBCUSH (→ FALSIFIED):** date-correlation fails at ≥2 of 3 windows, OR any sign-flip
  in direction between any two windows.
- **Ambiguous-hold (→ ITERATE, re-test 2026-11-08):** primary (mean-R) classifier structurally
  unreliable at n < 30 trades within a pre-registered window AND the secondary (cost-to-range
  fraction) fallback, run under the identical three-window/threshold discipline, is also unreliable
  or itself produces a §6-triggering result — in which case that fallback result is what gets
  reported, not a fresh threshold negotiated after seeing it.

## Explicit non-negotiables carried from the prior (vol-regime) round's own discipline

- No window may be dropped from the reported verdict after seeing its result.
- No threshold in this file may be loosened, tightened, or reworded once Phase 1 has been run even
  once, for any window, under any classifier. A miss is a miss.
- The classifier's causal-ness must be independently re-derived (a second, separate implementation,
  not a re-read of the first) before any verdict is trusted — matching the standard the prior
  round's own verification pass set and met.

**Committed:** 2026-08-20, same batch as `docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md`. Phase 1
has not run as of this commit.
