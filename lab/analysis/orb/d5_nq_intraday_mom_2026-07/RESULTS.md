**Theme:** orb
**Status:** ACTIVE — Baltussen H1 on NQ IS — Stage-2/4 results
# D5 Stage-2/4 RESULTS — Baltussen H1 on NQ IS

**Campaign:** `d5_nq_intraday_mom`  
**Pre-reg:** [`docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md`](../../../docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md)  
**Manifest:** [`discovery_manifests/d5_nq_intraday_mom.json`](../../../discovery_manifests/d5_nq_intraday_mom.json)  
**Machine report:** [`stage2_4_report.json`](stage2_4_report.json) · edge series [`stage4_is_edges.csv`](stage4_is_edges.csv)

---

## Verdict — Stage-2 cost-law **KILL**

| Metric | Value |
|---|---|
| IS sessions (complete RTH) | **2,127** (2010-06-07 → 2018-12-31) |
| Mean gross edge | **+1.46 bp** / session |
| 4× RT hurdle (MNQ econ) | **11.06 bp** (`Bulenox_100K` cps=$0.61 + 1 tick slip) |
| Margin | **−9.6 bp** (edge is ~7.6× below the hurdle) |
| Gross ann. Sharpe (diagnostic) | 0.88 |
| hit rate | 0.489 |
| corr(r_rod, r_last) | **+0.081** (sign matches Baltussen; magnitude thin) |

**PASS iff** mean gross edge ≥ 4× RT cost fraction. **Failed.** Stage-5/6/7/8 are **not run** — cost-law is a hard kill (campaign Default / pre-reg §3).

---

## Frozen construct (H1)

| Piece | Pin |
|---|---|
| Clock | America/New_York RTH 09:30–16:00 |
| Predictor | `r_rod = ln(C_15:30 / O_09:30)` |
| Response | `r_last = ln(C_16:00 / O_15:30)` |
| Trade | `sign(r_rod) × r_last`, exit 16:00, one RT/session |
| Series | `NQ.FUT` parent 1m → ET-day volume-lead stitch → session extract |
| Economics | MNQ multiplier $2, tick $0.50; commission from `firm_rules` |

---

## Cost anatomy (median px 15:30 = 4013.5)

```
RT_usd = 2 × (0.61 + 1×0.50) = $2.22
notional = 4013.5 × 2 = $8,027
rt_frac = 2.22 / 8027 ≈ 2.77 bp
hurdle_4x = 11.06 bp
```

Parent-NQ price levels drive the notional; dollars are MNQ (proxy discipline). Native-MNQ OOS would not change the kill — the gross edge would need to rise ~7.6× to clear, not a micro-vs-parent rescaling.

---

## Disposition

- **Stage-2:** KILL — H1 does not clear the 4× cost-law on IS.
- **Stage-4:** IS edge series emitted for the record (n=2,127); not a survivor hand-off.
- **Stage-5+:** blocked.
- **Register:** closed with H1 as non-survivor (banks K=1 for the MNQ family).
- **Campaign outcome class:** cost-law falsification (success-eligible research close — pre-reg §6 analogue / Default #8). Directional footprint present (ρ=+0.08) but **not tradeable** at MNQ RT economics under the frozen 4× bar.

Reproduce:

```bash
PYTHONPATH=lab;core python lab/analysis/d5_nq_intraday_mom_2026-07/run_stage2_4.py
```

---

## 2026-07-21 addendum — OOS re-derivation (D5-RECOST-1) confirms the kill, refines the reasoning

[D5-RECOST-1](../d5_recost_2026-07/RESULTS.md) (frozen `2dad8f9`, run 2026-07-21) re-derived
Stage-2 on the native `MNQ.v.0` OOS window (2019-05-06→2026-07-16, n=1,789) — the panel already
earmarked in the pre-reg for the never-reached confirmation. **The kill is CONFIRMED, but the
line-48 note ("native-MNQ OOS would not change the kill... the gross edge would need to rise ~7.6×...
not a micro-vs-parent rescaling") is refined.** That note conflated two axes: the **contract** axis
(MNQ vs parent NQ, same $2 multiplier — correctly irrelevant) and the **temporal** axis (NQ median
4,013→14,769), which it did not separate. D5-RECOST separated them:

- The temporal price move **did** cut the hurdle **11.06 → 3.01 bp (3.7×)** — so the "~7.6×" figure
  was IS-price-specific and overstated the standing hurdle.
- The kill nonetheless holds because the **OOS edge decayed negative**: **+1.461 bp (IS) → −0.327 bp
  (OOS)**, `corr(r_rod,r_last)` +0.081 → **+0.024**, gross Sharpe +0.88 → **−0.13**, hit ≈ coin-flip.
  The directional footprint present IS (ρ=+0.08) is **absent OOS** (ρ≈0).

Net: this IS verdict **stands and is strengthened** — IS real-but-sub-cost; OOS decayed-to-zero. The
Baltussen effect (RANK #1 of the 2026-07-21 prop-fundable-archetype deep-search) is statistically
absent on modern MNQ, independently corroborating the deep-search's decay flags on our own data.
