**Theme:** orb
**Status:** ACTIVE (one headline RETRACTED 2026-08-02) — faithful close_tod session-truncation sweep (MNQ, Tradeify)
# Q-SESSCONF-1 — RESULTS: faithful `close_tod` session-truncation sweep (MNQ, Tradeify)

**Pre-registration:** [`Q-SESSCONF-1`](../../../docs/briefs/rnd-pipeline/Q-SESSCONF-1-mnq-session-confluence-longer-hold-scoping.md), frozen `d88a47e` **before** this ran (axis ruling, 12-cell ladder, annualization convention, Δ\* = +0.124).
**Harness:** [`run_sessconf_sweep.py`](run_sessconf_sweep.py) — `orb_lib.orb_backtest` called **verbatim**; `_gross`-at-rt=0-then-subtract pattern copied from `run_stage7.py`.
**Spend:** **$0.00 · K=0 · no manifest · no pull.** The MNQ family's last Cap seat is **UNSPENT**.

**Provenance (pinned pre-run).** Panel `_mnq_15m.pkl` sha256 `81c05e9a4ee319e8b3efa61333cf00a1…`;
engine `orb_lib.py` sha256 `dcfe83e1ad8db180…`, byte-identical between `origin/main` `491d3b6` and the
primary checkout `2c5f937` where the gitignored panel lives. Cost: Tradeify $0.91/side + 1 tick ⇒
`rt_pt` 1.41.

---

## Verdict — **FALSIFIED** on the admissible ladder

`max_h annSR_h − annSR_close = +0.091` (13:45 cell) against Δ\* = **+0.124**. The hold-window axis
does not carry enough headroom to pay for the K that composing costs.

**The nominal max was +0.234, and it is inadmissible.** The best-scoring cell is `close_tod 15:15` —
which *is* `CLOSE_TOD_DEFECT`, the pre-D5 **15:30 exit**, barred by
[`ADR 2026-07-31 §5`](../../../docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md) first bullet
(*"Adopting the 15:30 exit because it backtests better"*), a standing `Accepted` ruling dated
**before** this pre-registration was frozen, and named as forbidden in this brief's own §5. Excluding
it is applying a prior constraint, not amending a gate after seeing results.

**Author error, recorded.** The frozen 12-cell ladder *included* that forbidden cell. §7 and §5 of the
pre-registration were internally inconsistent; **§5 governs**. The ladder should have excluded any
cell reconstructing a non-16:00 session end at freeze time.

---

## Phase 1 — baseline reproduction: three exact hits

| Check | Local | Published | Δ |
|---|---:|---:|---:|
| 2021+ annSR @ Tradeify | **+1.140** | +1.140 ([Stage-7 T1](../orb_mnq_2026-07/RESULTS_stage7.md)) | **+0.000** |
| FULL annSR @ Tradeify | **+0.835** | +0.835 (Stage-7 T1) | **+0.000** |
| Correct-clock meanR / n | **+0.0626 / 1,846** | +0.0626 / 1,846 ([ADR §3](../../../docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md)) | **exact** |
| Defective-clock meanR / n | **+0.0778 / 1,841** | +0.0778 / 1,841 (ADR §3) | **exact** |

The harness independently reproduces **both rows** of the ADR's Finding-1 clock table to four
decimals. That is the anchor arm working, and it is also what identifies the 15:15 cell as the
adjudicated defect rather than a discovery.

**Correction to the pre-registration.** §0/§4 stated the local panel begins 2020-07-01 (from
`core/data/bar_data/MNQ_M15.csv`). Wrong file: `run_stage2.load_mnq_15m()` builds from the
**databento** cache, spanning **2019-05-06+** (n=1,846, 7.19 y). The cohort is therefore *identical*
to the published one — which is why reproduction is exact and the ±0.15 band was never stressed. The
§6 AMBIGUOUS clause did not fire (n=1,846 ≥ 400; Δ = 0.000 ≤ 0.15).

---

## Phase 2 — full ladder (all 12 cells; no silent top-N)

| close_tod | n | tr/yr | meanR | perTrade | ann252 | annFreq | best | vs base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 10:45 | 1725 | 239.8 | +0.0133 | +0.0202 | +0.320 | +0.313 | +0.320 | −0.522 |
| **11:00** | 1756 | 244.1 | +0.0225 | +0.0315 | +0.501 | +0.493 | **+0.501** | **−0.342** |
| **11:15** | 1777 | 247.1 | +0.0236 | +0.0309 | +0.490 | +0.485 | **+0.490** | **−0.352** |
| 11:45 | 1796 | 249.7 | +0.0361 | +0.0426 | +0.676 | +0.673 | +0.676 | −0.166 |
| 12:15 | 1807 | 251.2 | +0.0476 | +0.0524 | +0.832 | +0.830 | +0.832 | −0.011 |
| 12:45 | 1817 | 252.6 | +0.0499 | +0.0529 | +0.839 | +0.840 | +0.840 | −0.002 |
| 13:15 | 1824 | 253.6 | +0.0464 | +0.0476 | +0.756 | +0.758 | +0.758 | −0.084 |
| **13:45** | 1831 | 254.6 | +0.0609 | +0.0585 | +0.929 | +0.934 | **+0.934** | **+0.091** ← best admissible |
| 14:15 | 1835 | 255.1 | +0.0576 | +0.0536 | +0.851 | +0.856 | +0.856 | +0.014 |
| 14:45 | 1838 | 255.5 | +0.0636 | +0.0578 | +0.917 | +0.924 | +0.924 | +0.082 |
| ~~15:15~~ | 1841 | 256.0 | +0.0778 | +0.0672 | +1.068 | +1.076 | ~~+1.076~~ | ~~+0.234~~ **INADMISSIBLE — the 15:30 defect** |
| **15:45** | 1846 | 256.7 | +0.0626 | +0.0526 | +0.835 | +0.842 | +0.842 | baseline |

Both annualization conventions agree throughout (max divergence 0.008), so the verdict is not an
annualization artifact — trade count barely moves across cells (239.8 → 256.7/yr).

### Two substantive findings

1. **The 60–75 minute class is strongly adverse, not merely unproven.** The `11:00`/`11:15` cells —
   the externally-carved-out class (arXiv 2605.04004) that motivated this entire thread — measure
   **+0.501 / +0.490 against the incumbent's +0.842**. This is the first direct measurement of that
   class on MNQ, and it answers the standing *"one remaining untested lever"* question negatively.
2. **Even counting the forbidden cell, the honest K kills it.** Adopting the best of a 12-cell sweep
   is a search of 12, so `K_eff = 14` and the floor is **1.262** (7.19 y era) — the 15:15 cell's
   +1.076 fails by 0.19. It clears only under the ADR's assumption of a single declared variant
   (`K_eff = 3`, floor 0.931). *Side note:* the ADR's stated reason for barring it compares the
   **correct-clock Bulenox** figure (0.890) against 0.98, but the cell under consideration is the
   **defective-clock Tradeify** construct at +1.068 — that particular arithmetic does not rule it
   out. The conclusion survives on the selection-deflation argument above, not on the ADR's stated one.

---

## Exposure control → forks Q-EODADV-1

> ⚠ **READER INTERCEPT — published `z = −2.90` RETRACTED 2026-08-02 (claim-alignment M11 / H12).**
> The estimate below **must not be re-quoted**. It differenced the ladder then treated
> the same 11 points as independent. The direct per-day test gives `t = −1.78`; max
> |t| across all 11 blocks is 1.84 against an expected null max ≈2.2–2.4; MNQ's 14:00
> block is as negative as the final block. So *"the final block is anomalous rather
> than merely long"* and *"That is a phenomenon, not an artifact"* are **superseded**.
> Body below retained byte-intact as the frozen record of what was published.
>
> ⚠ **Operator flag (mechanical half only):** gate 13 cannot catch this class — the
> retraction lived in a different file with no addendum-confined token. Do not "fix"
> gate 13 here.


Decomposing the ladder into marginal blocks, the final 30 minutes contributes **−50.7 (×1e-5)
per minute** against a prior-block mean of **+24.9, sd 26.0** ⇒ **z = −2.90**. A constant-hazard /
pure-time-at-risk null predicts z ≈ 0, so the final block is anomalous rather than merely long.

That is a phenomenon, not an artifact — but this curve is the *symptom* and cannot confirm any
mechanism explaining itself. The mechanism question is forked, pre-registered, and independence-
constrained at
[`Q-EODADV-1`](../../../docs/briefs/rnd-pipeline/Q-EODADV-1-mnq-final-half-hour-adversity-scoping.md).

---

## Disposition

- **Q-SESSCONF-1: FALSIFIED.** Hold-window axis exhausted; the residual (confluence-conditioning
  only) is the 4/4-FALSIFIED tail-exhausted class. The 07-21 domain audit's "untested" preservation
  of the session-confluence longer-hold thread is **discharged** — measured, and adverse.
- **MNQ Cap seat: UNSPENT.** No manifest opened, no K consumed, $0 spent.
- **`ORB-MNQ-1` untouched**; D5 and the 16:00 clock stand.

Reproduce:

```bash
/c/Users/joshu/multi_firm_operations/.venv-research/Scripts/python.exe \
  lab/analysis/sessconf_mnq_2026-08/run_sessconf_sweep.py
```
