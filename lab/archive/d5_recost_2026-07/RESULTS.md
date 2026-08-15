# D5-RECOST-1 RESULTS — MNQ-native cost-law re-derivation of the Baltussen H1 construct

**Campaign:** `d5_recost_1`
**Pre-reg (frozen before this run):** [`docs/briefs/pre-registration/D5-RECOST-1-verdict-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/D5-RECOST-1-verdict-preregistration.md) (freeze commit `2dad8f9`)
**Scoping:** [`docs/briefs/rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md`](lab/archive/../../docs/briefs/rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md)
**Machine report:** [`recost_report.json`](recost_report.json) · edge series [`recost_oos_edges.csv`](recost_oos_edges.csv)

**Verdict: FALSIFIED — Stage-2 KILL (binding cause is edge decay, not cost).**

---

## Verdict — `FALSIFIED` (Stage-2 KILL), but the binding cause is **edge decay, not cost**


The cost-geometry lever was arithmetically real — and moot. Repricing dropped the hurdle
~3.7×; the edge itself went **negative** out-of-sample.

| Metric | IS (2010-18, parent verdict) | **OOS (2019-26, this run)** |
|---|---|---|
| Window | 2010-06-07 → 2018-12-31 | **2019-05-06 → 2026-07-15** |
| N sessions | 2,127 | **1,789** |
| **Mean gross edge** | **+1.4613 bp** | **−0.3265 bp** |
| median `px_1530` | 4,013.5 | **14,769.25** |
| 4× hurdle (Bulenox_100K) | 11.063 bp | **3.006 bp** (fell 3.7×) |
| edge / hurdle (Bulenox) | 0.132 | **−0.109** |
| 4× hurdle (MFFU_Rapid, sensitivity) | — | 3.927 bp |
| edge / hurdle (MFFU) | — | −0.083 |
| `corr(r_rod, r_last)` | +0.081 | **+0.024** |
| gross ann. Sharpe (diagnostic) | +0.883 | **−0.133** |
| hit rate | 0.489 | 0.496 |

**PASS iff** OOS mean gross edge ≥ 4× OOS hurdle (Bulenox basis). **Edge is negative → FALSIFIED.**
Stage 5-8 not run (Stage-2 is a hard kill).

---

## What this establishes

1. **The cost-geometry thesis was correct but does not rescue the construct.** The pre-flight
   was right that fixed-$ cost over rising notional collapses the bp hurdle: 11.06 bp (IS) →
   **3.01 bp** (OOS). The scoping brief's motivating question ("has the margin narrowed enough?")
   is answered — the *hurdle* side narrowed decisively, but the **edge side decayed past zero**,
   so no repricing can help. This is why §4 gated on a **jointly re-measured** OOS edge, not the
   frozen IS number.

2. **The Baltussen intraday-momentum effect has decayed to statistically absent on modern MNQ.**
   The predictive correlation `corr(r_rod, r_last)` fell from +0.081 (IS) to **+0.024** (OOS);
   the traded edge from +1.46 bp to **−0.33 bp** (gross Sharpe +0.88 → **−0.13**, hit 0.489 →
   0.496 ≈ coin-flip). This is not "a profitable short" — it is a slightly-negative, ~zero result:
   the rest-of-day → last-30-min timing relationship is **gone** on 2019-2026 native micro data.

3. **Independent corroboration, on our own data, of the 2026-07-21 deep-search decay flags.**
   The literature caveats surfaced this session — documented ~50% post-publication anomaly decay,
   and the NY-Fed-lineage finding that the related E-mini overnight/intraday drift faded to ~zero
   **since 2021** — are reproduced here directly: the effect is present IS (pre-2019), absent OOS
   (2019+). It also aligns with the external MNQ 14-signal-family falsification (arXiv 2605.04004),
   which found nothing survives on modern MNQ.

4. **Discipline win — the zero-discretion window choice was load-bearing.** Freezing the full-OOS
   window (the parent's own pre-designated confirmation window) *before* measuring foreclosed the
   §5 temptation to window-shop. Had we scored the "favorable" recent cuts (≥2025 hurdle 1.82 bp;
   last-60 hurdle 1.51 bp — where the *stale* IS edge sat at ~97% of the hurdle), a noise-positive
   near the lower hurdle could have been mistaken for a marginal PASS. On the honest full-OOS
   window the answer is unambiguous: the edge is negative. This is the freeze-before-result gate
   earning its keep.

---

## Disposition

- **Stage-2:** KILL — OOS edge negative; fails the 4× cost-law on both firm bases.
- **Cost-geometry lever:** **CLOSED for this construct.** The re-proposal grounds that opened this
  campaign (venue-external price-level change) are now spent — the price side moved as predicted,
  the edge side decayed. Banks a defect-log entry on the MNQ family.
- **K:** unchanged. Decision 1 (reuse `K_eff=1`) holds; no fresh K consumed; MNQ family K_banked
  unchanged from the parent close.
- **Does NOT reopen** on a different sub-window (§5 forbidden — best-of-window). A genuinely
  different mechanism, or materially-better-than-retail execution evidence, would be a fresh
  question, not a re-run of this one.
- **Parent D5 verdict stands** and is now *strengthened*: the IS-era Stage-2 cost-law kill was
  correct at IS prices; this run shows the construct also has **no OOS edge to deploy at any price** —
  the two closures are consistent (IS: real-but-sub-cost; OOS: decayed-to-zero).

Reproduce:

```bash
PYTHONPATH=lab;core python lab/archive/d5_recost_2026-07/run_recost.py
```

---

## Provenance note (for the 08-08 packet)

D5 / D5-RECOST is the repo's own test of the **single strongest academically-evidenced,
futures-native, cost-aware intraday index-futures edge** in the literature (Baltussen, Da,
Lammers & Martens, *JFE* 2021 — RANK #1 of the 2026-07-21 archetype deep-search). Tested IS
(cost-law kill) and OOS (edge decayed to zero). The prop-fundable-archetype search surfaced no
stronger candidate; this closes the highest-evidence intraday-momentum thread on both axes.
