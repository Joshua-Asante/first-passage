# Cheap falsifier — HTF-5m bias + LTF-1m with-break (Master-Pattern-shaped) — `FALSIFIED`

**Date:** 2026-08-10  
**Q-ID spent:** **none** (killed before G0 / brief)  
**Cost / K:** $0.00 · K=0  
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) step 2  
**Defaults packet:** Tradeify-suited Master-Pattern-shaped freeze (HTF 5m bias · LTF 1m with-break · G=10 · session-flat · RT 1.41)  
**Runner:** [`_cheap_falsifier_htf_bias_break_2026-08-10.py`](_cheap_falsifier_htf_bias_break_2026-08-10.py)  
**Raw:** [`_cheap_falsifier_htf_bias_break_2026-08-10_RESULTS.json`](_cheap_falsifier_htf_bias_break_2026-08-10_RESULTS.json)  
**Panel:** `mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet` (MNQSEL-2 cache reuse)  
**Distinct from:** [`Q-TNEC-CON-2`](../../../docs/briefs/closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) (single-TF with-break; already `AMBIGUOUS-HOLD` non-promotable) · Family A displacement fade · CON-1 ES/NQ divergence

## Frozen geometry (a priori)

| Knob | Value |
|---|---|
| Instrument | `MNQ.v.0` RTH 09:30–15:59 ET |
| HTF / LTF | **5m** bias · **1m** entry |
| Contraction | `K_NARROW=2` · `NARROW_MULT=1.0` · med20 (HTF for bias box; LTF for entry) |
| Bias settle | HTF close beyond quiet extreme **and** on that side of quiet midline; session-standing until opposite settle |
| Entry | LTF with-break **only in HTF bias direction**, next 1m open |
| Stop / exit / cost | G=10 · session-flat · RT 1.41 · EM3 |
| Coverage floor | bias on ≥ **20%** of θ-warm sessions |

Kill rule: `VOID-COVERAGE` if bias frac &lt; floor; else both arms powered (n≥100) **and** trade-weighted session-block 95% CI entirely &lt; 0 → `FALSIFIED`.

## Result

| Check | Value |
|---|---|
| eligible sessions (θ warm) | 1,648 |
| bias sessions | 1,510 (**91.6%** — clears coverage floor) |
| entry clocks | 7,560 |
| elapsed | ~57s |

| Arm | n | mean net R | WR | stop rate | session-block 95% CI |
|---|---:|---:|---:|---:|---|
| long | 3,837 | **−0.146** | 0.143 | 0.846 | **[−0.242, −0.045]** |
| short | 3,723 | **−0.142** | 0.116 | 0.876 | **[−0.253, −0.024]** |

**Verdict:** `FALSIFIED` — coverage OK; both arms CI entirely below 0 at powered n. HTF-directed with-break is **worse** than CON-2's unfiltered with-break (which straddled and closed AMBIGUOUS-HOLD): the filter did not rescue net R under Tradeify RT 1.41.

## Disposition

- **No** `Q-TNEC-CON-3` · **no** PREREG_G0 · **no** explore GO · **no** S6 ADMIT  
- Do **not** retune K_NARROW / NARROW_MULT / HTF pair / G / sign-invert (forbidden; would be a new family)  
- Lane consecutive-kill counter: still **1/3** (CON-1 only; cheap-falsifier kills do not consume a campaign slot; CON-2 was AMBIGUOUS-HOLD not FALSIFIED)  
- CON-2 remains its own closed cell — this kill does not reopen or retune it  
- Re-proposal bar = new **entry mechanism** (or a cost-geometry G0 as CON-2 Iterate named), not Master-Pattern θ-rescue
