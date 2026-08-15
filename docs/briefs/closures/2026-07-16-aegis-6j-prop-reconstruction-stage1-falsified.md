# Closure — Aegis→6J prop reconstruction Stage-1 (H-SWEEP)

**Pre-registration:** [`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md`](../pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md) (`FROZEN` §9 2026-07-16 / JA)  
**Plan of record:** [`docs/superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md`](../../superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md) @ `eaa1191`  
**Sweep log / pins:** [`lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/SWEEP_LOG.md`](../../../lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/SWEEP_LOG.md)  
**Closed:** 2026-07-16 — operator accepted Stage-1 **FALSIFIED**

---

## Verdict (exactly one)

**FALSIFIED — H-SWEEP** (Stage-1).

Zero of c01–c12 clear hard filters (a)–(e). The mechanical max-mean-qty selection rule was never reached. Stage-2 H-SOLO is **not authorized**. This pre-reg closes; any retry needs a **fresh** pre-reg + operator GO (Known Trap #12 — do not amend N≥80 in place).

---

## Which trigger fired

Pre-reg §6 Stage-1 **FALSIFIED** branch: *zero cells clear (a)–(e)*.

| Filter | Outcome |
|---|---|
| (a) overnight 0% | PASS (all) |
| (a2) fills ≤ deadline | PASS (all; Stage-0 `≤` semantics) |
| (c) sel maxDD ≤ 6% | PASS (all; 0.49–1.24%) |
| **(d) sel N ≥ 80** | **FAIL (all; selection-window N = 73–74)** |
| (e) holdout net ≥ 0 | PASS (all) |

Binding constraint: frozen selection window **2022-01-12 → 2024-12-31** yields only 73–74 exits on every unique panel. Full-span N is 129–130 (Stage-0’s N≥80 used full span; Wave-1 (d) does not).

---

## Grid honesty (degeneracy, not missing data)

Operator-confirmed byte-identical collapses (risk% / cap shown on TV):

- **c02 ≡ c04** — cap8 @ 0.25% matched cap5 @ 0.25% (size never needed >5)
- **c05 ≡ c06** — on-screen risk **0.55%** still produced the 0.40% qty profile
- **c11 ≡ c12** — same on the 15:45 half

Nine unique sha256 digests cover twelve labels. Degeneracy does **not** rescue (d).

---

## What this does / does not close

| Closed | Still standing |
|---|---|
| This Stage-0→2 pre-reg’s H-SWEEP path | Class-S candidate #1 Part A DISCHARGED (regime-fragile caveat) |
| Stage-2 solo Part A under *this* pre-reg | Four-firms ADR §4 discharge via #1 |
| Compose Stage 3/4 under *this* plan | Self-funded Aegis→M6J scale path (separate) |
| | Stage-0 ENVELOPE-YES baseline (68f0e) as measurement |

---

## Forbidden moves carried out of closure

- Do **not** lower N≥80 or widen the selection window on this pre-reg after seeing results.
- Do **not** pick a “best” cell by PF / expectancy / full-span N and send it to Part A.
- Do **not** compose with MYM+MNQ from a non-survivor.
- Do **not** treat 0.40≡0.55 sizing collapse as license to retune BE/SL/TP/ATR (leaves Class S).

---

## Reproduction

```bash
# Metrics + filter flags
python -c "import json; m=json.load(open('lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/wave1_metrics.json')); print(sum(1 for r in m if r['PASS_all']), 'survivors'); print({r['sel_n'] for r in m})"
# expect: 0 survivors; {73, 74}

# Hash pins
cd lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07 && sha256sum -c WAVE1_SHA256SUMS  # or Get-FileHash on Windows
```

---

## Next (if revisited)

Fresh pre-reg only. Candidate amendments (not decided here): selection-window N bar calibrated to this panel’s ~74 exits; and/or acknowledge risk%/cap degeneracies in the grid design before TV spend. Operator GO required.
