# Q-MNQSEL-1 Phase 0 — RESULTS: selection-value ceiling on MNQ

**Status:** `FALSIFIED` (C2) — oracle top-1/day mean net R is **below** EM1 0.40 on
**both** arms. Disposition **STOP** this universe per frozen PREREG §6.
**Date:** 2026-08-07
**Pre-registration:** [`PREREG.md`](PREREG.md) — frozen before any path PnL.
**Cost:** **$0.00** (MNQ 1m rebuilt from local `~/.databento_cache` DBN
`ohlcv-1m_continuous_b1fa4ae6b7ba9af2.dbn`, `MNQ.v.0`, 2019-05-06→2026-08-05) ·
**K=0** · **no manifest** · **Cap seat untouched**.
**Runner:** [`run_selection.py`](run_selection.py) · **16 unit tests**, hand-computed and
passing **before** the runner read a real bar.
**Raw:** [`RESULTS.json`](RESULTS.json)

---

## 1. Verdict — `FALSIFIED`, by a razor that is itself the finding

| Arm | S1 all-take | S2 random-1/day | **S3 oracle top-1/day** | S4 top-2 | S4 top-3 | S5 median hits | S6 ≥1 hit |
|---|---:|---:|---:|---:|---:|---:|---:|
| **long** | −0.0364 | +0.0023 | **+0.3998** | +0.3996 | +0.3993 | 98.0 | 99.9% |
| **short** | −0.0362 | −0.0499 | **+0.3984** | +0.3974 | +0.3959 | 97.0 | 99.7% |

**Gate (frozen):** S3 ≥ 0.40 on ≥1 arm **and** S1 < 0.40 → `RESOLVED`.  
**Observed:** S3 long **0.3998** and short **0.3984** — both **&lt; 0.40** → **C2 `FALSIFIED`**.
S1 is deeply negative on both arms (no SURPRISE-DIRECTION). n_sessions = **1,674** ≥ 250 (C1 clear).

Median restart clocks/session = **145.0** — matches Step-1 N11’s s=40 median event count
(restart clocks ≈ completions + session start; same order).

---

## 2. What the numbers mean (and what they do not)

1. **All-take is dead.** Taking every restart clock loses ~0.036R/trade net. Selection is
   load-bearing in spirit — there is no free direction bias.
2. **Oracle top-1 sits on the EM1 knife-edge.** A clean target-hit earns exactly
   `(17.41 − 1.41)/40 = 0.40R` by G construction. S6 shows **99.9% / 99.7%** of sessions
   have ≥1 target-hit, so almost every day’s best trade is a clean hit. The ~0.1–0.3% of
   sessions with **no** target-hit pull S3 a few ten-thousandths under 0.40 — enough to
   fire the frozen bar, not enough to invent headroom.
3. **Density is huge (S5 ≈ 97–98 target-hits/day)** — opportunity to *pick among winners*
   is abundant. The gate failure is not “no winners exist”; it is “perfect one-trade/day
   selection does not clear EM1 with any margin once no-hit sessions are averaged in.”
4. **`FALSIFIED` licenses no candidate and opens no feature campaign** (FM-8). Re-proposal
   bar (PREREG §6): a **different causal candidate set** — not denser OF on the same
   clocks, not completed-window ranking.

---

## 3. Pre-registered expectation

PREREG §4 called **C4 (`RESOLVED`)** most likely. **That expectation was wrong** and is
recorded as a failed prediction — not retrofitted. The miss is mechanical: S3 ≈ 0.40 from
below, not a sign flip or an empty opportunity set.

---

## 4. Scope limits

1. Upper bound on selection value among **restart clocks** only — not among all bars, not
   among completed-window labels (forbidden).
2. Entry at open of the restart bar; same-bar stop wins; flat at last in-session bar
   (sessionize drops 16:00+ ET).
3. Panel extends one day past Step-1’s end date (through 2026-08-05); n_sessions 1,674 vs
   Step-1’s 1,672 — immaterial to the razor.
4. No TBBO/MBP, no Pine, no Cap seat, no Route B catalogue.

---

## 5. Disposition

**Verdict used:** `FALSIFIED` (C2)  
**Next:** **STOP** this universe.  
**Entry packet for any successor:** this RESULTS + PREREG; must propose a **new causal
candidate set** with its own Phase-0 ceiling before any feature campaign.  
**Board write:** STATE / SESSIONS / INDEX / CATALOG / MNQ session log (this session).

---

## 6. Reproduce

```bash
python -m pytest lab/archive/mnq_selection_ceiling_2026-08/test_run_selection.py -q
# Rebuild parquet from local DBN cache (MNQ.v.0 ohlcv-1m), then:
python lab/archive/mnq_selection_ceiling_2026-08/run_selection.py <mnq_1m.parquet>
```

Expect: VERDICT `FALSIFIED`; S3 long ≈ 0.3998 / short ≈ 0.3984; S1 both ≈ −0.036.
