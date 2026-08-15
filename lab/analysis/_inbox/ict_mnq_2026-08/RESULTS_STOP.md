# `Q-ICTSTOP-1` — RESULTS: ICT stop-lever space-kill (native MNQ 1m)

**Date:** 2026-08-06
**Pre-registration:** [`PREREG_STOP.md`](PREREG_STOP.md) — frozen at commit `30a89a0`,
**before any stop-space expectancy number existed**. ICTEXP's stop-free T2 was known;
no MAE-conditioned or raid-scaled stop P&L had been computed on this chain.
**Cost:** **$0.00** (estimate + pull both billed `$0.0000`, 2,556,165 records) · **K=0**
(operator-affirmed via plan ratification) · **no manifest** · **Cap seat untouched**.
**Runner:** [`run_stop.py`](run_stop.py) · **16 new unit tests** (106 total in this
directory), all hand-computed and passing *before* the runner touched a real bar.

---

## 1. Verdict — `NOT-KILLED` (X4)

| | Measured |
|---|---|
| n after `raid_dist > 0` | **30,156** (≥100) |
| Stop-free T2 on this pop | mean **−0.891** pt, CI [−3.630, +1.664] (continuity with ICTEXP null) |
| ∀ f ∈ F_GRID: E_best CI **lower** | **≥ 5.640 pt** |
| Gate | **X4 → `NOT-KILLED`** |

Per [`PREREG_STOP.md`](PREREG_STOP.md) §6: **licenses nothing.** Removes only the claim
"no raid-scaled stop width could ever clear the bar under the optimistic E_best limb."
Any reconstructed Pine stop remains a **new K-bound pre-registration**. NO-GO on
`Q-ICT-1MEXEC-1` reasons 1/2/4 untouched; ICTEXP's measured null on the stop-free chain
stands.

---

## 2. F-grid (E_best is the kill limb; E_worst is disclosure)

BAR = **5.640 pt**. Seed `20260806`. `s = f × raid_dist`.

| f | median s (pt) | stop-out % | E_best mean | CI lo | CI hi | E_worst mean |
|---|---|---|---|---|---|---|
| 0.50 | 3.31 | 93.1% | **24.431** | **22.812** | 26.044 | 1.003 |
| 0.75 | 4.97 | 90.6% | **23.621** | **22.019** | 25.254 | 0.977 |
| 1.00 | 6.62 | 88.4% | **22.982** | **21.398** | 24.626 | 0.989 |
| 1.25 | 8.28 | 86.4% | **22.253** | **20.618** | 23.957 | 0.768 |
| 1.50 | 9.94 | 84.5% | **21.508** | **19.856** | 23.239 | 0.559 |
| 2.00 | 13.25 | 80.9% | **20.350** | **18.672** | 22.104 | 0.418 |

Every f clears the bar on E_best CI **lower**. Every E_worst mean sits **~0.4–1.0 pt** —
near the stop-free null, far below 5.640. **NOT-KILLED is carried entirely by the
optimistic same-path limb** (credit target when both stop and target are reachable).
That is the frozen gate reading, not a soft re-read (FM-7: do not promote E_worst to a
kill).

---

## 3. Mechanism disclosure — winners sit through deep drawdown

| Leg | n | MAE q25 / q50 / q75 | MAE mean |
|---|---|---|---|
| target touched | 7,937 | 7.38 / **22.12** / 54.00 | 40.93 |
| bleed to E1 | 22,219 | 37.12 / **91.38** / 183.75 | 133.93 |

`raid_dist` quartiles: **3.25 / 6.62 / 13.00** pt. Median winner MAE (**22 pt**) is
**~3×** median raid_dist — the ORB §2a shape again: a raid-scaled stop fires on most
paths that later reach the target, so E_best and E_worst diverge sharply. This is why
E_best alone can clear a cost bar the stop-free chain never approached.

Drops vs ICTEXP continuity: `nonpos_raid_dist` **2,242** (fill already beyond raid —
geometric filter, not an invented floor); `no_raid_px` 0. Filled events 30,156 vs
ICTEXP's 32,355 on a one-day-longer panel — expected size after the raid_dist filter.

---

## 4. Consequences

1. **ICTEXP RESULTS §6.1 scope limit is discharged.** The stop lever was tested as a
   *space* without inventing the lost Pine rule. Outcome: space not killed under E_best;
   residual for a real stop is explicitly **K-bound** if pursued.
2. **`Q-ICT-1MEXEC-1` NO-GO stands.** Reasons 1/2/4 untouched. Reason 3 remains a
   measured stop-free null; X4 does not invent an edge hypothesis for the frozen
   construct.
3. **Seat preserved.** $0.00, K=0, no manifest, Cap untouched.
4. **Do not read E_best ~20–24 pt as harvestable expectancy.** It assumes optimistic
   path order on dual-reach bars. E_worst ~0–1 pt is the honest same-order bound and
   does not clear the bar on the point estimate alone (CIs for E_worst were not the
   verdict instrument; they are not required to quote the mechanism).

---

## 5. Scope limits

1. Raid distance is a **scale**, not a reconstructed locked stop (PREREG_STOP FM-2).
2. E_best / E_worst dual bound; kill reads E_best only by freeze.
3. Same ICTEXP fill / DOL / E1 generosity; bar-level touch; no gap-through.
4. R-denominated arm filters still NOT applied (inherited ICTEXP omission).
5. **No GO state.**

---

## 6. Reproduce

```bash
python -m pytest lab/analysis/_inbox/ict_mnq_2026-08/ -q          # 106 passed
python lab/analysis/_inbox/ict_mnq_2026-08/run_stop.py <mnq_1m.parquet>
git --no-pager diff HEAD -- lab/archive/ict_cascade_2026-06-18/   # must be EMPTY
git log --format='%h %cs' -- lab/analysis/_inbox/ict_mnq_2026-08/PREREG_STOP.md
git log --format='%h %cs' -- lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_STOP.md
```

Data (gitignored, regenerable at $0.00 — estimate first):

```bash
python -m lab.databento_fetch.db_fetch estimate --symbols MNQ.v.0 --stype continuous \
  --schema ohlcv-1m --start 2019-05-06 --end 2026-08-06 --phase oos
python -m lab.databento_fetch.db_fetch pull --symbols MNQ.v.0 --stype continuous \
  --schema ohlcv-1m --start 2019-05-06 --end 2026-08-06 --phase oos \
  --max-cost 1.00 --out mnq_1m.parquet
```
