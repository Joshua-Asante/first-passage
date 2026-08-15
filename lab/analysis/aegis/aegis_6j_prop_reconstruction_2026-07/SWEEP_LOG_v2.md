# SWEEP_LOG — Aegis→6J Wave-1 **v2** (window-realigned offline re-slice, c01–c12)

**Pre-reg (v2):** [`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md`](../../../docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md) (`FROZEN` §9 2026-07-16 / JA)
**Tie-break (v2.1):** [`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md`](../../../docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md) (`FROZEN` §9 2026-07-16 / JA)
**Driver:** [`wave1_reslice_v2.py`](wave1_reslice_v2.py) (validated 12/12 vs v1 pins; hash-gated to `WAVE1_SHA256SUMS`)
**Windows (v2):** selection **2022-01-12 → 2025-06-30**; holdout **2025-07-01 → 2026-06-30**; Stage-2 panel 2022-01-12 → 2026-06-30
**Inputs:** the 9 unique **pinned** Wave-1 CSVs (full-span exports) — **no new TV export**; pure offline re-slice.
**Pins:** [`WAVE1_SHA256SUMS`](WAVE1_SHA256SUMS) · [`wave1_v2_metrics.json`](wave1_v2_metrics.json)

---

## Cell table (v2 realigned windows)

| Cell | cap | risk% | fill | sel N | sel maxDD% | sel meanQ | sel net $ | ho net $ | a/a2/c/d/e | note |
|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|
| c01 | 3 | 0.25 | 16:00 | 94 | 0.49 | 1.72 | 2902 | 2010 | Y/Y/Y/Y/Y | |
| c02 | 5 | 0.25 | 16:00 | 94 | 0.49 | 1.79 | 2890 | 1929 | Y/Y/Y/Y/Y | ≡ c04 |
| c03 | 5 | 0.40 | 16:00 | 95 | 0.78 | 3.09 | 6115 | 3613 | Y/Y/Y/Y/Y | |
| c04 | 8 | 0.25 | 16:00 | 94 | 0.49 | 1.79 | 2890 | 1929 | Y/Y/Y/Y/Y | ≡ c02 |
| **c05** | 8 | 0.40 | 16:00 | 95 | 1.24 | **4.60** | 8803 | 5755 | Y/Y/Y/Y/Y | **≡ c06; WINNER (v2.1)** |
| c06 | 8 | 0.55 | 16:00 | 95 | 1.24 | **4.60** | 8803 | 5755 | Y/Y/Y/Y/Y | ≡ c05; 0.55 on screen |
| c07 | 3 | 0.25 | 15:45 | 94 | 0.49 | 1.72 | 2614 | 1916 | Y/Y/Y/Y/Y | |
| c08 | 5 | 0.25 | 15:45 | 94 | 0.49 | 1.79 | 2583 | 1817 | Y/Y/Y/Y/Y | |
| c09 | 5 | 0.40 | 15:45 | 95 | 0.78 | 3.09 | 5565 | 3457 | Y/Y/Y/Y/Y | |
| c10 | 8 | 0.25 | 15:45 | 95 | 0.78 | 3.19 | 5596 | 3683 | Y/Y/Y/Y/Y | |
| c11 | 8 | 0.40 | 15:45 | 95 | 1.24 | 4.57 | 7597 | 5354 | Y/Y/Y/Y/Y | ≡ c12 |
| c12 | 8 | 0.55 | 15:45 | 95 | 1.24 | 4.57 | 7597 | 5354 | Y/Y/Y/Y/Y | ≡ c11; 0.55 on screen |

---

## Hard-filter outcome (§2.6)

| Filter | Result |
|---|---|
| (a) overnight = 0 | **PASS** all 12 |
| (a2) fills ≤ cell deadline | **PASS** all 12 |
| (c) sel maxDD ≤ 6% | **PASS** all 12 (0.49–1.24%) |
| (d) **sel N ≥ 80** | **PASS** all 12 (**94–95** — reachable; v1 was 73–74 FAIL) |
| (e) holdout net ≥ 0 | **PASS** all 12 (+$1,817 … +$5,755) |

**Survivors: 12 / 12.** The v1 falsification cause (unreachable (d)) is resolved by the window
realignment; the genuine unknown — (e) on the *new* 12-month holdout — passed for every cell.

---

## Selection (§2.6 → §2.6′)

**Max mean position quantity = 4.60**, held by **c05 and c06**, which are **byte-identical**
(both sha `ED91CD2D5D40`; the pre-disclosed c05≡c06 degeneracy). They tie on mean qty **and**
both v2 tie-breaks (sel maxDD 1.2425, sel net $8,803) because they are the same CSV → mechanical
v2 §2.6 → **AMBIGUOUS**. c11/c12 next at 4.5684 (strictly lower; not tied at top).

**v2.1 degeneracy tie-break (byte-identical top tie → lower `risk_pct_display`,
never-round-up-on-risk `CLAUDE.md:55`):** collapse c05≡c06 to the one panel `ED91CD2D`; take the
lower label → **c05**.

---

## Verdict

**Stage-1-v2 RESOLVED (via v2.1 tie-break) — winner c05:** `max_contracts` **8** ·
`risk_pct_display` **0.40%** · `eod_fill_deadline_et` **16:00** (`pine_eod_trigger_et` 15:45) ·
panel sha **`ED91CD2D5D40`** · sel N 95 · sel maxDD 1.24% · sel meanQ 4.60 · sel net $8,803 ·
holdout net $5,755 · **envelope-YES** (overnight 0%, fills ≤ 16:00). Deployable panel identical
to c06 (label-only difference; 0.55% never binds under cap8). → **Stage-2 solo Part A** (v2 §2.7;
H-SOLO on `Tradeify_Select_100K` AND `MFFU_Rapid_100K` — not run here).

---

## Reproduction

```bash
python -c "import json; m=json.load(open('lab/analysis/aegis_6j_prop_reconstruction_2026-07/wave1_v2_metrics.json')); print(sum(1 for r in m if r['PASS_all']),'survivors'); t=max(r['sel_mean_qty'] for r in m); tied=[r for r in m if abs(r['sel_mean_qty']-t)<1e-9]; print('top-tie:',[(r['cell'],r['risk'],r['sha'][:12]) for r in tied])"
# expect: 12 survivors; top-tie c05(0.40)/c06(0.55) both ED91CD2D5D40

# full re-slice (hash-gated; needs the LF-pinned CSVs — see .gitattributes eol=lf fix):
python lab/analysis/aegis_6j_prop_reconstruction_2026-07/wave1_reslice_v2.py --mode validate
python lab/analysis/aegis_6j_prop_reconstruction_2026-07/wave1_reslice_v2.py --mode run
```
