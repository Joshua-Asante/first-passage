**Theme:** c1

# ORB-MNQ-1 regime-break re-test under the corrected (anchored) date-correlation method

**Status:** **RESOLVED** — both candidates still miss the pre-registered ≥2/3 clearance bar under the
corrected apparatus, but one produces a precisely-scoped, statistically decisive near-miss worth
carrying forward.
Does not reopen `Q-ORBCUSH-1` or `Q-ORBPOS-1`; both stay closed under their own original verdicts.
This is new, additional evidence recorded under a corrected apparatus, not an amendment to either
closure.

**Trigger:** `POSITIVE_CONTROL_METHOD_FIX.md` §6.3 (2026-08-23) names this explicitly as a worthwhile,
separately-scoped follow-on, with an explicit instruction to report the two axes (date-correlation vs
gate-clearance-direction) separately rather than collapsed. Operator GO: 2026-08-24, in-session
("Run the ORB-MNQ regime-break re-test under the fixed method").

**$0 / K=0** — diagnostic re-measurement of an already-real historical pattern under a corrected
measurement apparatus, same class as `Q-ORBCUSH-1`/`Q-ORBPOS-1` themselves. One live network pull
(CFTC Socrata public API, free, no key) for TFF; mean-R uses only ORB-MNQ-1's own realized trades,
already on disk. Writes only to this directory.

---

## §0 — Rule 0 reads (production/prior-artifact reads, this session, 2026-08-24)

| Source | What it grounds |
|---|---|
| `lab/analysis/c1/q_orbpos_1_2026-08/POSITIVE_CONTROL_METHOD_FIX.md` (full) | The frozen fix design (§3), its own explicit recommendation to run this re-test (§6.3), and the non-negotiable instruction to report two axes separately |
| `lab/analysis/c1/q_orbpos_1_2026-08/run_orbpos_positive_control_v2_anchored.py` | `build_classifier_anchored`, `print_level_association`, `ASSOC_ALPHA=0.01`, `MIN_SEPARATION_PP=0.35` — imported unchanged |
| `lab/analysis/c1/q_orbpos_1_2026-08/run_orbpos_tff_probe.py` | TFF's own frozen classifier construction, `WINDOWS={4,13,26}`, `CUTOFF`, `gate_check_bucket`, `classify_direction` — imported unchanged |
| `lab/archive/q_orbcush_1_2026-08/run_meanr_regime_gate.py` | Mean-R's own frozen classifier construction (rolling-mean-R **with** its `.shift(1)` self-referential-outcome exclusion), `WINDOWS={20,63,126}` trades, `gate_check_bucket` — read in full, one stale absolute path patched in-memory (never written to the archived file) |
| `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/stage2_regime_gate.py` | The original trailing-volatility classifier's actual construction — confirmed **architecturally different** from the expanding-median design the fix targets (see §3) |
| `docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md`, `Q-ORBPOS-1-closure-falsified.md` | Original verdicts, re-proposal bars, and the STOP disposition this re-test does not disturb |

---

## §1 — What was re-tested, and what was not

**Re-tested (2 of 3 named candidates):**
- **Trailing mean-R** of ORB-MNQ-1's own realized trades (`Q-ORBCUSH-1`) — its original architecture
  (trailing rolling mean → fully-expanding causal median threshold, `WINDOWS={20,63,126}` trades) is
  the exact defect class `POSITIVE_CONTROL_METHOD_FIX.md` diagnosed and fixed.
- **CFTC TFF Leveraged-Funds positioning extremity** (`Q-ORBPOS-1`) — same architecture,
  `WINDOWS={4,13,26}` weekly prints, real fresh CFTC pull (not the frozen archived one).

**Not re-tested: trailing realized volatility.** Read in full (`stage2_regime_gate.py`) before
deciding this, not assumed. The original volatility round used a **single 63-day window with a
full-sample (not expanding, not causal-in-the-relevant-sense) median split** — a different, older,
simpler construction than the `WINDOWS={20,63,126}`-plus-expanding-median architecture mean-R and TFF
share and that the fix specifically targets. Volatility was never built under the architecture this
fix repairs. Applying `build_classifier_anchored`/`print_level_association` to it would require
**constructing a new three-window, expanding-median volatility classifier from nothing** — a design
decision (window choice, extremity definition) on the same order as authoring a fresh candidate, not
a re-score of an existing one. That is out of scope for "re-run the existing fix"; it was not done
here, and it is not silently substituted for. If wanted, it is a separate, explicitly-scoped
follow-on in its own right (name a volatility extremity series + windows before running anything).

---

## §2 — Fidelity controls (both scripts, before touching either classifier)

| Candidate | k=1 bust | k=2 bust | Published | Verdict |
|---|---:|---:|---:|---|
| Mean-R refit | 67.67% | 77.01% | 67.67% / 77.01% | **PASS**, exact (0.00pp delta both k) |
| TFF refit | 67.67% | 77.01% | 67.67% / 77.01% | **PASS**, exact (0.00pp delta both k) |

Both harnesses reproduce the published intraday-honest bust rate byte-for-byte — the reused
`day_loop_intraday`/`run_policy_orb`/`pol_cushion` engine path is unaffected by anything in this refit.

---

## §3 — Results, per candidate, both axes reported separately

### Mean-R (trailing mean-R of ORB-MNQ-1's own trades)

| Window | n(HIGHER) | n(LOWER) | Separation | Fisher's exact p | Point-biserial r (p) | Axis 1: corrected assoc. clears? | Direction |
|---|---:|---:|---:|---:|---:|---|---|
| W1 (20 trades) | 1,104 | 722 | +10.2pp | 5.46×10⁻⁶ | 0.196 (3.0×10⁻¹⁷) | no (sep < 35pp) | `HIGHER_CLEARS_LOWER_DOES_NOT` |
| W2 (63 trades) | 1,240 | 543 | +26.5pp | 1.22×10⁻²⁷ | 0.383 (2.6×10⁻⁶³) | **no** (sep < 35pp, despite p≈10⁻²⁷) | `HIGHER_CLEARS_LOWER_DOES_NOT` |
| W3 (126 trades) | 1,384 | 336 | **+59.4pp** | **2.95×10⁻⁹⁵** | 0.575 (5.0×10⁻¹⁵²) | **YES** | `HIGHER_CLEARS_LOWER_DOES_NOT` |

- **Axis 1 (corrected date-correlation-equivalent, ≥2/3 needed):** **1/3 — does not fire.** (Original,
  broken method: 0/3.)
- **Axis 2 (gate-clearance direction, same sign every window):** **YES, stable at all 3 windows**
  (`HIGHER_CLEARS_LOWER_DOES_NOT`) — identical to the original result; this axis was never the problem
  for mean-R, in either method.
- Independently re-verified by hand (separate script, this session): W3's Fisher's-exact p and
  separation recomputed from the raw 2×2 table (`{higher_post:1151, higher_pre:233, lower_post:80,
  lower_pre:256}`) match the pipeline's own output to floating-point precision.

### TFF Leveraged-Funds positioning extremity

| Window | n(HIGHER) | n(LOWER) | Separation | Fisher's exact p | Point-biserial r (p) | Axis 1: corrected assoc. clears? | Direction |
|---|---:|---:|---:|---:|---:|---|---|
| W1 (4 prints) | 171 | 127 | +23.5pp | 1.23×10⁻⁸ | 0.040 (0.492) | no (sep < 35pp) | `BOTH_CLEAR` |
| W2 (13 prints) | 154 | 135 | +18.9pp | 3.42×10⁻⁷ | 0.035 (0.555) | no (sep < 35pp) | `BOTH_CLEAR` |
| W3 (26 prints) | 127 | 149 | +12.0pp | 7.74×10⁻⁵ | 0.032 (0.596) | no (sep < 35pp) | `LOWER_CLEARS_HIGHER_DOES_NOT` |

- **Axis 1:** **0/3 — does not fire.** Unchanged from the original (0/3).
- **Axis 2:** **NO, unstable** — `BOTH_CLEAR, BOTH_CLEAR, LOWER_CLEARS_HIGHER_DOES_NOT`. The original
  run's instability was `LOWER_CLEARS_HIGHER_DOES_NOT, BOTH_CLEAR, LOWER_CLEARS_HIGHER_DOES_NOT` — a
  **different** disqualifying pattern (W1 flipped from a signed direction to `BOTH_CLEAR`), but still
  disqualifying either way.

---

## §4 — Honest interpretation

**Neither candidate clears the pre-registered composite bar under the corrected apparatus. Both
closures' verdicts stand: mean-R and TFF positioning do not explain the 2021-09-28 break.** The fix
repaired the measurement apparatus, not the underlying economics — and the apparatus fix is precisely
what makes this null more trustworthy than the original one, not less: `POSITIVE_CONTROL_METHOD_FIX.md`
showed the *broken* method could not recover even a designed d=2.0 synthetic signal (0/3, contamination
mechanism identified and proven), so a 0/3 or a non-clearing near-miss under the *corrected* method is
now informative in a way the original 0/3 results were not.

**The one thing worth carrying forward precisely, not oversold:** mean-R's failure mode changed in a
specific, diagnostic way. Under the original (broken) method it failed because the apparatus itself
could not separate the eras cleanly (contaminated LOWER bucket, per `POSITIVE_CONTROL.md`'s own
mechanism). Under the corrected method, the eras separate cleanly (W3 shows 59.4pp separation at
p=3×10⁻⁹⁵ — as clean a signal as the fix's own synthetic positive control produced), **and mean-R still
misses the ≥2/3 bar only because W1 and W2's separation (10.2pp, 26.5pp) sits under the 35pp floor,
not because of a Fisher's-exact significance problem** — W2's p-value (10⁻²⁷) is more extreme than
almost anything else in this campaign, yet its separation is under half the required floor. This is a
**precise, narrow failure** (association-strength threshold, not statistical noise, not apparatus
contamination) — a materially different and more interpretable finding than the original's opaque,
apparatus-confounded 0/3. Direction (Axis 2) was never mean-R's problem, in either method.

**TFF shows no equivalent improvement.** Its best separation (23.5% at W1) is comparable in *shape* to
mean-R's weakest window, its point-biserial correlations are an order of magnitude weaker (r≈0.03-0.04
vs mean-R's 0.20-0.58), and its direction axis is unstable under both methods. The corrected apparatus
gives TFF no more credit than the broken one did.

**What this does NOT license:**
- Does not reopen `Q-ORBCUSH-1` or `Q-ORBPOS-1` — both remain `FALSIFIED`/`STOP`. Their own re-proposal
  bars (a genuinely different candidate mechanism) are unchanged and unmet by this refit, which used
  the identical two classifiers, not a new one.
- Does not license loosening `MIN_SEPARATION_PP` or `ASSOC_ALPHA` to make W1/W2 clear — those are
  frozen per `POSITIVE_CONTROL_METHOD_FIX.md` §3f ("not changed after seeing a result"); this document
  reports the miss honestly rather than re-deriving a bar that would happen to admit it.
- Does not extend to volatility, which was never in scope for this pass (§1).
- Does not touch any locked/frozen surface, allocation, `dd_protection` constant, Pine, or rail. ORB-MNQ-1
  stays `PARKED`; the Tradeify payability target stays `FALSIFIED` (2026-08-03 ADR, unaffected).

---

## §5 — Artifacts

- [`run_meanr_refit_anchored.py`](run_meanr_refit_anchored.py) · [`results_meanr_refit_anchored.json`](results_meanr_refit_anchored.json) · [`run_log_meanr_refit_anchored.txt`](run_log_meanr_refit_anchored.txt)
- [`run_tff_refit_anchored.py`](run_tff_refit_anchored.py) · [`results_tff_refit_anchored.json`](results_tff_refit_anchored.json) · [`run_log_tff_refit_anchored.txt`](run_log_tff_refit_anchored.txt)

## §6 — Audit hooks

```bash
# Re-verify mean-R's W3 Fisher's-exact figure independently
python -c "
import json
from scipy import stats
r = json.load(open('lab/analysis/c1/orbcush_orbpos_refit_2026-08/results_meanr_refit_anchored.json', encoding='utf-8'))
t = r['windows']['W3']['association']['contingency_table']
_, p = stats.fisher_exact([[t['higher_post'], t['higher_pre']], [t['lower_post'], t['lower_pre']]])
assert abs(p - r['windows']['W3']['association']['fisher_p']) < 1e-12
print('OK', p)
"

# Confirm both fidelity controls hit the published anchor exactly
python -c "
import json
for f in ('results_meanr_refit_anchored.json', 'results_tff_refit_anchored.json'):
    r = json.load(open(f'lab/analysis/c1/orbcush_orbpos_refit_2026-08/{f}', encoding='utf-8'))
    assert r['fidelity_control']['1']['delta_pp'] == 0.0 or abs(r['fidelity_control']['1']['delta_pp']) < 0.01
print('OK')
"

# Confirm neither original closure was edited by this refit
git log --oneline -- docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md docs/briefs/closures/Q-ORBPOS-1-closure-falsified.md
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Re-test executed under operator GO. Mean-R and TFF positioning re-scored under the corrected (anchored) method; volatility explicitly excluded (architecture mismatch, recorded not silently skipped). Both candidates still fail the pre-registered composite bar; mean-R's failure mode sharpened to a precise association-strength miss (W2 p≈10⁻²⁷, separation 26.5pp vs 35pp floor). W3's Fisher's-exact result independently re-verified by hand. | Claude Opus 5, operator GO |
