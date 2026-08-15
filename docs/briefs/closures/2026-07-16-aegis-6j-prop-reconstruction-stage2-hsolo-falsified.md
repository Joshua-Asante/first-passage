# Closure — Aegis→6J prop reconstruction Stage-2 (H-SOLO)

**Pre-registrations:** v2 window-realigned + v2.1 tie-break + v2.2 native-path 1R guard
([`v2`](../pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md) /
[`v2.1`](../pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md) /
[`v2.2`](../pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md))
— all `FROZEN` §9 2026-07-16 / JA  
**Winner panel:** c05 (cap8 / 0.40% / 16:00 / sha `ED91CD2D`)  
**RESULTS:** [`lab/archive/class_s_aegis_solo_scoring_2026-07-16/RESULTS.md`](../../../lab/archive/class_s_aegis_solo_scoring_2026-07-16/RESULTS.md)  
**Closed:** 2026-07-16 — Stage-2 **H-SOLO FALSIFIED** under v2.2

---

## Verdict (exactly one)

**FALSIFIED — H-SOLO** (Stage-2 solo Part A).

c05 native $100K panel fails Part A on **both** required firms. Winner expression closes.
**No compose, no in-place reweight** (v2.1 §4 / v2.2 §4). Any retry needs a **fresh**
pre-reg + operator GO (Trap #12).

---

## Which trigger fired

v2.2 §6 **FALSIFIED** branch: either firm fails Part A (bust > 3.0% or pass < 50%), Run-2.

| Firm | bust | pass | Part A |
|---|---:|---:|---|
| Tradeify_Select_100K | **0.0641** | 0.9327 | **FAIL** (bust > 0.03) |
| MFFU_Rapid_100K | **0.0641** | 0.9327 | **FAIL** (bust > 0.03) |

Killer = **trailing bust ~6.41%** (daily/static 0). Pass rate clears the 50% floor on both.
Gated on Run-2; seeds 42/123/2026; 10k×3; horizon 1500; `dd_protection` OFF.

---

## Path honesty (not a rescue)

- Stage-1 **v1** FALSIFIED (sel N≥80 unreachable) → **v2** window realign cleared 12/12 →
  **v2.1** tie-break → c05 → Stage-2 `NEEDS_CONTEXT` on full-stop 1R FALLBACK (`1ababcf`) →
  **v2.2** native-path 1R re-spec (option c; diagnostic-only; cannot bias MC).
- Panel: n=128 trades, envelope YES, net_static $13,736, 1R(median) $87, 0 full-stops > $1,000.
- v2.2 guard-drop does **not** explain the FAIL — 1R is not a scoring input on the native path.

---

## What this does / does not close

| Closed | Still standing |
|---|---|
| H-SOLO under v2 / v2.1 / v2.2 (c05 winner expression) | Class-S candidate #1 Part A DISCHARGED (regime-fragile caveat) |
| Stage-3 compose under *this* reconstruction chain | Four-firms ADR §4 discharge via #1 |
| | Self-funded Aegis→M6J (PARKED 2026-07-16) |
| | Stage-0 ENVELOPE-YES / Wave-1 measurement artifacts as history |

---

## Forbidden moves carried out of closure

- Do **not** reweight c05 risk%/cap or swap fill deadline after seeing Part A.
- Do **not** compose MYM+MNQ with this panel to “rescue” H-SOLO.
- Do **not** treat pass≈93% as a soft pass — the frozen ceiling is bust ≤ 3.0%.
- Do **not** cite the v2.2 1R re-spec as able to change the MC outcome.

---

## Artifacts

- [`RESULTS.md`](../../../lab/archive/class_s_aegis_solo_scoring_2026-07-16/RESULTS.md)
- [`aegis_solo_report.json`](../../../lab/archive/class_s_aegis_solo_scoring_2026-07-16/aegis_solo_report.json)
- [`run_aegis_solo_scoring.py`](../../../lab/archive/class_s_aegis_solo_scoring_2026-07-16/run_aegis_solo_scoring.py)
- Prior Stage-1 v1 close: [`2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md`](2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md)
