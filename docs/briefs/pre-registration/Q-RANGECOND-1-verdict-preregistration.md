# Q-RANGECOND-1 — Verdict pre-registration (H-RANGECOND-1)

**Frozen:** 2026-08-30, before Phase 1 (the trade-log build) has been run. Parent brief:
[`Q-RANGECOND-1-overnight-range-conditioned-orb-mnq-payability.md`](../Q-RANGECOND-1-overnight-range-conditioned-orb-mnq-payability.md).

A verdict computed after moving any threshold below is void.

**Forbidden regardless of outcome:** no threshold moves after Phase 1-3 results exist. If the
join needs a design change once run, that is a new design decision requiring a fresh freeze —
not an edit to this one.

---

## §A — Frozen constants

- **Conditioner** (reused verbatim from `Q-RANGEXFER-1`, not re-derived): `bias_overnight_d =
  1{ON_range_d >= P80(ON_range_{d-60..d-1})}`, `WINDOW=60`, `Q_BIAS=0.80`, strictly-prior
  trailing window.
- **ORB-MNQ-1 construction** (reused verbatim from `run_orb_mnq_bulenox_blusky.py::make_inst`,
  not re-derived): `or_bars=2`, `open_tod=09:30 ET`, `close_tod=15:45 ET`, `tick=0.25`,
  `spread_pt=0.25`.
- **Payability floor** (from `shape_feasibility_map_2026-08/RESULTS.md` §7, cross-checked before
  this freeze commits, not taken from memory alone): win rate ≥55% as the measured lower bound;
  larger mean win as the second-order lever.
- **n floor:** 30 conditioned trades — reused verbatim from `Q-ORBCUSH-1`'s own closure, the
  correctly-scoped precedent (a closure ON `ORB-MNQ-1` ITSELF): "primary classifier structurally
  unreliable at n < 30 trades in a pre-registered window"
  ([`Q-ORBCUSH-1-closure-falsified.md`](../closures/Q-ORBCUSH-1-closure-falsified.md) line 19).
- **Block-bootstrap CI:** circular day-block, `block=20 trading days, draws=4000, seed=42` — the
  exact frozen construction the presence-battery used, reused for consistency across this
  research line, not re-derived.

---

## §B — Presence/comparison limbs (GATE)

| Limb | Content | Role |
|---|---|---|
| L1 | n-floor: n_conditioned ≥ 30 trades | GATES — below this, AMBIGUOUS-HOLD regardless of direction |
| L2 | Block-bootstrap CI on (WR_conditioned − WR_unconditioned) excludes 0, positive-signed | GATES toward RESOLVED |
| L3 | Block-bootstrap CI on (mean_win_conditioned − mean_win_unconditioned) excludes 0, positive-signed | GATES toward RESOLVED |
| L4 | WR_conditioned ≥ 0.55 (the measured Tradeify floor's own lower bound) | GATES toward RESOLVED |

---

## §C — Verdict map (mirrors the parent brief's §6 table exactly)

| Verdict | Trigger | Applies to |
|---|---|---|
| `RESOLVED` | L1 passes AND L2 AND L3 both clear (CI excludes 0, positive-signed) AND L4 passes | H-RANGECOND-1 |
| `FALSIFIED` | L1 passes but L2 or L3's CI includes 0 or is wrong-signed, OR L4 fails while L2/L3 clear | H-RANGECOND-1 |
| `AMBIGUOUS-HOLD` | L1 fails (n < 30 conditioned trades) regardless of L2-L4's direction | H-RANGECOND-1 |

---

## §D — Pinned ex-ante expectation

**Corrected on adversarial review — power estimate revised.** An earlier draft of this prediction
assumed `ORB-MNQ-1`'s own entry-trigger rate would materially thin the conditioned count below the
30-trade floor. Checked directly against `RESULTS.md` (Stage 2): `ORB-MNQ-1` fires on **99.4%** of
RTH session-days (1,846/1,857 — an opening-range breakout is triggered by price moving at any
point across a ~5.75-hour session, which almost always happens). The "further reduced by
entry-trigger rate" clause in the withdrawn draft was close to a no-op.

**Predicted: L1 clears comfortably, RESOLVED or FALSIFIED is the more likely outcome than
AMBIGUOUS-HOLD.** `ORB-MNQ-1` is a ~6-year panel (~1,500 trading days, ~1,846 entries at 99.4%).
The overnight-range-elevated predictor fires on roughly the top quintile of days by construction
(`Q_BIAS=0.80`, minus the 60-day warmup). Expected conditioned trade count ≈ 0.20 × ~1,780
(post-warmup entries) ≈ **280-300 trades** — roughly 10× the 30-trade floor. This is stated now,
before Phase 1 runs, precisely because it inverts the withdrawn prediction: the test is likely to
be well-powered and land at a decisive verdict, which raises (not lowers) the stakes of getting
§6/§C's gate criteria right before any data exists.
**Predicted, conditional on L1 passing (expected):** directionally favorable (higher conditioned WR
and mean win) on the mechanism story's own terms (parent brief §1), but that mechanism story is
itself only a plausible, not uniquely-predicted, prior (§1's own correction) and a directly
contrary same-claim finding exists on a sibling instrument (§2 of the parent brief) — so no
confident prediction is made on whether L2-L4 clear decisively. This is exactly what Phase 1-3
exist to measure, not to
presuppose.

Substituting real Phase 1-3 numbers to confirm or refute this prediction is the compute step, not
this freeze.
