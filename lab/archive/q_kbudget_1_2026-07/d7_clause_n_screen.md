# D7 (JPY month-end, 6J expression) — minimal Clause-N screening pass

**Status:** Screened-FAIL (Clause N). Converts D7 from UNSCREENABLE to a definite verdict.
**Frozen screen:** [`docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md) §B (freeze `b304f2c`). §B is untouched by this note — this fills the axis's declared inputs, per §B's own "nearest analytic analogue… recorded on the axis's screen row" provision.
**Reproduce:** `python lab/archive/q_kbudget_1_2026-07/d7_power.py` (zero pulls, zero K consumed).

---

## Clause-N definition (frozen, quoted verbatim from §B)

> P(primary confirm clause passes | mechanism/effect genuinely true) ≥ 0.50, the §R precedent threshold (Q-HARV-1: joint 5–6% ⇒ DECLINE; H1 power ~24–30% ⇒ unreachable). Computed coarse-by-design (screen tier): normal approximation, power = Φ(√N·|δ|/σ − z_α), with α = the campaign-default primary bar (two-sided p ≤ 0.05 ⇒ z ≈ 1.96 unless the axis declares a ratified alternative), N = the full declared OOS event count (generous), δ = the cohort-cited central (not top-of-range) plausible-true effect, σ from the same cited cohort. Where the axis's confirm design is not event-study-shaped, the nearest analytic analogue is used and recorded on the axis's screen row. Effect priors must be cohort-cited… No citable prior ⇒ the axis is UNSCREENABLE on Clause N — routed per §D, never patched with an invented number.

## Why D7 was UNSCREENABLE — the root cause

Q-MECH-1.JPY closed **MECHANISM-NAMED-ENDOGENOUS** ([`docs/ltm/briefs/Q-MECH-1.JPY_h_register.md`](lab/archive/../../docs/ltm/briefs/Q-MECH-1.JPY_h_register.md), H-JPY-C): Aegis's own locked month-end exclusion boundary *is* the mechanism, read in negative — permitted-day dips are transient flow that reverts; excluded-day dips are persistent benchmark/repatriation flow that pushes through the band. Monitor = the month-end calendar. **This is a loss-avoidance property of an existing leg, not a standalone directional entry edge** — the structural reason no non-circular δ exists, not a data gap a pull would fix.

## The three δ candidates

| # | Source | value | δ/σ | Validity |
|---|---|---|---|---|
| 1 | **P-cohort** ([`Q-MECH-1.JPY_T1_T2_results.md`](lab/archive/../../docs/ltm/briefs/Q-MECH-1.JPY_T1_T2_results.md), `db24726`; n=8, avg −$1,224.59) | own 8-trade σ ≈ $1,810–1,940 | ≈0.65 | **FORBIDDEN.** Same n=8 that motivated the Q-MECH-1 close; barred as discriminating evidence by [`Q-JPY-EOM-GUARDBAND-1_inquire.md`](lab/archive/../../docs/ltm/briefs/Q-JPY-EOM-GUARDBAND-1_inquire.md) §5 ("borrowing the motivating n=8 as both motivating AND discriminating evidence"). Would give spurious power ≈1.00 — exactly the unfalsifiable-by-construction trap §B's "never patched with an invented number" blocks. |
| 2 | **Loss-avoidance contrast** (v4.3 header, excluded −$2,746 vs permitted −$1,122; quoted §0.3 of the T1/T2 results doc) | no cohort-matched σ | ≈0.49 (invalid units splice, forcing 1R as σ) | **PARTIAL — invalid for Clause N.** Non-circular in provenance, but it is a conditional-on-loser avoidance magnitude on an *existing* leg, not an unconditional standalone-entry mean return. Reframing it as an entry δ over an unconditional σ is a metric-cohort provenance violation. |
| 3 | **HARV class-analogue** ([`Q-HARV-1-month-end-rebalance-successor.md`](lab/archive/../../docs/ltm/briefs/Q-HARV-1-month-end-rebalance-successor.md), `9bddd33`; +13 bp central, σ≈90 bp/monthly event) | cited from an external sibling cohort | **0.144** | **RECOMMENDED.** External, cohort-cited, central (not top-of-range); D7 is explicitly HARV-shaped (N≈10² monthly events) per §B's "nearest analytic analogue" provision. |

## Computation and verdict

```
N = 100 (≈ full declared 6J-era OOS monthly month-end event count, generous)
delta/sigma = 0.144 (HARV analogue)
power = Phi(sqrt(100) * 0.144 - 1.96) = Phi(-0.52) = 0.303
```

**0.303 < 0.50 → FAIL on Clause N.** Break-even requires δ/σ ≥ 0.196 (36% larger than the HARV analogue, with zero non-circular JPY evidence for it) or N ≥ 185 monthly events (≈15y; the declared panel is ≈8y).

**Row update:** UNSCREENABLE → `FAIL (N, class-analogue): P(primary|true) ≈ 0.30 < 0.50 at N≈100, delta/sigma=0.144 (HARV analogue 9bddd33)`.

## Effect on the KBUDGET verdict

D7 moves from UNSCREENABLE to screened-FAIL. It removes the *weakly* verdict-relevant hold; D5 (DJ30/NAS gamma-positioning) remains the sole verdict-relevant axis (see [`d5_clause_n_rescreen.md`](d5_clause_n_rescreen.md)).

## Caveats

1. **Symbology.** M6J (micro yen) is absent at all four `AUTOMATION_FRIENDLY_PROP_FIRMS`; a 6J prop expression means the full-size 6J contract (~$1,250/pip class), which raises per-event notional/margin and worsens, not helps, standalone consistency/bust math. This is a different, non-transferable venue from the self-funded Aegis→M6J lane.
2. **Category mismatch is the root cause, not a proxy for a data gap.** A newly-started prop discovery axis needs a standalone entry δ; the endogenous mechanism structurally does not yield one non-circularly. A cheap data pull would not fix this.
3. **A screened-FAIL is not a claim the mechanism is dead.** It states only that a *newly-started discovery axis* on it is not fundable/demonstrable at N≈100 monthly events. The mechanism remains live inside Aegis; the parked [`Q-JPY-EOM-GUARDBAND-1`](lab/archive/../../docs/ltm/briefs/Q-JPY-EOM-GUARDBAND-1_inquire.md) (n≥15 fresh-period, ≈7y USDJPY accrual) is the correct, separate, non-circular track and is unaffected by this screen.
4. **No reopening.** This note does not reopen the Q-MECH-1 closure, change any locked v4.3 parameter, or design a strategy — screening-design only. The circular P-cohort δ is shown solely to demonstrate why it is forbidden; it is never the load-bearing plug (see `d7_power.py`'s "INVALID sensitivities" block).

## Audit hooks

```bash
python lab/archive/q_kbudget_1_2026-07/d7_power.py
# expect: power = 0.303, verdict FAIL

git log -1 --format='%h %ci' -- docs/ltm/briefs/Q-MECH-1.JPY_T1_T2_results.md   # expect db24726
git log -1 --format='%h %ci' -- docs/ltm/briefs/Q-HARV-1-month-end-rebalance-successor.md  # expect 9bddd33
```
