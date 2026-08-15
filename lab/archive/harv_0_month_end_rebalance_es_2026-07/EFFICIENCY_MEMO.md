# Q-HARV-0 Efficiency Memo — faster path to a valid §6 verdict

**Date:** 2026-07-11  
**Scope:** Recommend a tighter Wave-1→H1 path. Does **not** edit the multitask plan file. Does **not** close the discovery manifest. Does **not** mark plan todos complete.

**Repo state snapshot (readonly inventory):**

| Symbol | Status | Evidence |
|---|---|---|
| ES.c.0 | **DONE** 2010-06-07 → 2026-06-30 | 4× ~4y parts (`_part_ES_c_0_{2010,2014,2018,2022}.parquet`) |
| YM.c.0 | **DONE** same span | 4× 4y parts — **not on §6 critical path** |
| ZN.c.0 | **PARTIAL** through 2017-12-29; 2018 part is **1y only** (312 rows); **2019–2026 missing** | `_part_ZN_c_0_2010/2014` OK; `_2018` thin; pull-log mid-year resume |
| GC.c.0 | **NONE** | — |
| MES.c.0 / MYM.c.0 | **NONE** | — |
| `definition` / `NOTES.md` | **NOT LANDED** | README still expects NOTES; no definition parquet |
| Harness | **READY** | `build_panel.py`, `run_harv0.py`, `step0_checks.py`, `cost_hurdle.py`, `test_harv0.py`, Phase0/G1/PROVENANCE |
| RESULTS | stub only | no verdict yet |

**Known failure mode (confirmed by lab scripts):** full-history / multi-symbol `ohlcv-1d` streams hang or 504. **Proven working:** single-symbol **~4-year** chunks (`validated_pull.py` CHUNKS). **Anti-pattern in flight:** `_wave1_pull_missing.py` yearly resume (~16 calls/symbol) — stop that path for remaining work.

---

## 1. Critical path — minimum data + steps to a valid §6 verdict

§6 partitions cleanly. The **minimum** depends on the H1 outcome:

### Path A — FALSIFIED-at-primary (cheapest valid close)

**Strict data:** `ES.c.0` + `ZN.c.0` only (2010-06 → 2026-06).

1. Finish ZN coverage (2× 4y pulls — see §4 commands).
2. Cheap `definition` for ES+ZN (roll-rule letter + close-print note → `NOTES.md`).
3. Concat → `parents_ohlcv_1d.parquet` (ES+ZN; YM optional).
4. Step-0 on monthly panel → H1 (sign-aligned mean, 4× single-RT hurdle, 10k label permutation, trade-rate).
5. If H1 fails per §6 FALSIFIED triggers → **close FALSIFIED**. Controls / GC / MES **not required for the gate** (brief + plan early-exit). C/G annotation still computable from ES alone for information.

**API calls remaining to unlock Path A:** **2** (ZN) + **1** definition ≈ **3**.

### Path B — H1 passes → need full §6 package for RESOLVED / most AMBIGUOUS

**Strict for RESOLVED (ALL of):** H1 ∧ P-placebo ∧ P-instrument ∧ P-covariance ∧ P-micro-OOS.

| Need | Symbol | Why |
|---|---|---|
| H1 + P-placebo + P-covariance + C/G | ES + ZN | Same panel; placebo/covariance/C need no extra symbols |
| P-instrument | **GC.c.0** | Identical rule on GC |
| P-micro-OOS | **MES.c.0** (2019-05→) | Native micro same-sign; **MYM not gated** |
| Cost hurdles | constants + price | `cost_hurdle.py` already uses MES specs; `run_harv0` can proxy price from ES until MES lands |

**Not on §6 critical path:** YM (breadth only), MYM (breadth micro).

**Extra API calls if H1 survives:** GC 4×4y + MES 2 chunks = **6** (still ≪ yearly 100-call plan).

---

## 2. What to cut / defer (without violating frozen §4/§5)

| Item | Verdict | Rationale |
|---|---|---|
| **YM / MYM** | **Defer forever for gates** (YM already pulled — sunk cost; keep, don’t wait on it) | Brief §1/§4: YM = breadth, not independent N. §6 lists no YM/MYM gate. MYM never appears in P-micro-OOS. |
| **GC** | **Defer until after H1** | Required only for P-instrument / RESOLVED. Early FALSIFIED skips it for the gate. |
| **MES** | **Defer until after H1** | Required for P-micro-OOS / RESOLVED. Hurdles don’t need the MES series first. |
| **Yearly chunking** | **Cut** | Replace with **4-year** single-symbol chunks (proven on ES/YM). |
| **Multi-symbol one-shot streams** | **Cut** | Hang/504 failure mode. |
| **~100 sequential yearly calls** | **Cut** | Worst-case design; ZN remainder is **2** 4y calls, not 8–16. |
| **Parallel symbol streams** | **Yes, cautiously** | Max **2** concurrent single-symbol `db_fetch pull` processes (separate terminals). Do **not** put multiple symbols in one `--symbols` arg for long ranges. |
| **Wider than 4y?** | **Optional try once** | ES 4y worked. An 8y single-symbol trial is a one-shot experiment; if it hangs, revert to 4y. Do **not** block H1 on that experiment. |
| **Unconditional TOM / ex-quarter-end / YM breadth report** | **Defer to post-H1 diagnostics** | Explicitly non-gating (§4/§6). |
| **definition before any remaining deep pull** | **Keep (cheap, parallel)** | Databento Rule 3 / brief Phase 1 — still owed in NOTES; can run beside ZN remainder. |

**Frozen §4 params untouched:** T-3→T-1, T-4, 100bp, bundled P-*, C/G annotation semantics.

---

## 3. Revised agent map — fewer sequential waits

```text
NOW (H1 critical path) — 2 agents max
  A  ZN remainder: 2× 4y pulls → quarantine thin 2018 year-part → concat ES+ZN
  B  definition (ES,ZN) + NOTES stub (roll-rule / close-print)   [parallel with A]

THEN (single agent, sequential)
  C  Step-0 → H1 (+ placebo + covariance + C/G from same panel)
     └─ if FALSIFIED → Phase 5 close (skip D/E for gate)
     └─ if H1 survives → fan-out:

AFTER H1 pass — 2 agents parallel
  D  GC: 4× 4y chunks → concat into parents
  E  MES: 2 chunks (2019-05→2022, 2022→2026-07) → micros parquet

THEN
  F  P-instrument + P-micro-OOS → §6 verdict → closure artifacts
  G  Optional: YM breadth table, MYM, unconditional TOM  [never blocks]
```

**vs original plan:** Wave 1 was one sequential agent pulling all 6 symbols before any test. Revised map **front-loads H1**, **gates GC/MES on H1 survival**, and **drops MYM from the gate path**.

**Max safe parallelism:** 2 concurrent single-symbol pulls. Avoid 3+ until one run proves Databento rate limits are happy.

---

## 4. Concrete next commands — fastest path to H1

Use research venv. Working dir = repo root. **Stop any in-flight yearly ZN loop** before starting.

### 4.0 Quarantine thin ZN 2018 year-part (so 4y pull can overwrite cleanly)

```powershell
cd c:\Users\joshu\multi_firm_operations
Move-Item lab\analysis\harv_0_month_end_rebalance_es_2026-07\data\_part_ZN_c_0_2018.parquet `
  lab\analysis\harv_0_month_end_rebalance_es_2026-07\data\_part_ZN_c_0_2018_YEARONLY.bak.parquet
```

### 4.1 Definition (parallel / cheap — Agent B)

```powershell
.\.venv-research\Scripts\python.exe .claude\skills\databento-data\scripts\db_fetch.py estimate `
  --symbols ES.c.0,ZN.c.0 --stype continuous --schema definition `
  --start 2024-01-01 --end 2024-02-01

.\.venv-research\Scripts\python.exe .claude\skills\databento-data\scripts\db_fetch.py pull `
  --symbols ES.c.0,ZN.c.0 --stype continuous --schema definition `
  --start 2024-01-01 --end 2024-02-01 --max-cost 1.00 `
  --out lab\analysis\harv_0_month_end_rebalance_es_2026-07\data\definition_ES_ZN.parquet
```

(Short window is enough for roll-rule / instrument metadata; pin letter + price-adjust flag in `NOTES.md`.)

### 4.2 ZN remainder — **only** pulls blocking H1 (Agent A)

```powershell
# Chunk 1: 2018–2021
.\.venv-research\Scripts\python.exe .claude\skills\databento-data\scripts\db_fetch.py estimate `
  --symbols ZN.c.0 --stype continuous --schema ohlcv-1d `
  --start 2018-01-01 --end 2022-01-01

.\.venv-research\Scripts\python.exe .claude\skills\databento-data\scripts\db_fetch.py pull `
  --symbols ZN.c.0 --stype continuous --schema ohlcv-1d `
  --start 2018-01-01 --end 2022-01-01 --max-cost 1.00 `
  --out lab\analysis\harv_0_month_end_rebalance_es_2026-07\data\_part_ZN_c_0_2018.parquet

# Chunk 2: 2022–2026-06
.\.venv-research\Scripts\python.exe .claude\skills\databento-data\scripts\db_fetch.py estimate `
  --symbols ZN.c.0 --stype continuous --schema ohlcv-1d `
  --start 2022-01-01 --end 2026-07-01

.\.venv-research\Scripts\python.exe .claude\skills\databento-data\scripts\db_fetch.py pull `
  --symbols ZN.c.0 --stype continuous --schema ohlcv-1d `
  --start 2022-01-01 --end 2026-07-01 --max-cost 1.00 `
  --out lab\analysis\harv_0_month_end_rebalance_es_2026-07\data\_part_ZN_c_0_2022.parquet
```

### 4.3 Concat + H1 (after both ZN parts land)

```powershell
.\.venv-research\Scripts\python.exe lab\analysis\harv_0_month_end_rebalance_es_2026-07\concat_parts.py
# If concat expects GC/MES: either stub those symbols out for H1-only parents file
# or concat ES+ZN(+YM) manually into data\parents_ohlcv_1d.parquet, then:

.\.venv-research\Scripts\python.exe lab\analysis\harv_0_month_end_rebalance_es_2026-07\run_harv0.py
```

`build_panel.py` already accepts `ym=None` / `gc=None`. Prefer an H1-first runner path that loads ES+ZN only so missing GC does not block (patch `run_harv0.main` to tolerate absent GC/MES — harness already NaNs P-instrument / skips micro when missing).

### 4.4 Only if H1 survives — GC + MES in parallel (Agents D / E)

```powershell
# Agent D — GC (4 chunks; same windows as validated_pull.py)
foreach ($c in @(
  @("2010-06-06","2014-01-01","2010"),
  @("2014-01-01","2018-01-01","2014"),
  @("2018-01-01","2022-01-01","2018"),
  @("2022-01-01","2026-07-01","2022")
)) {
  .\.venv-research\Scripts\python.exe .claude\skills\databento-data\scripts\db_fetch.py pull `
    --symbols GC.c.0 --stype continuous --schema ohlcv-1d `
    --start $c[0] --end $c[1] --max-cost 1.00 `
    --out "lab\analysis\harv_0_month_end_rebalance_es_2026-07\data\_part_GC_c_0_$($c[2]).parquet"
}

# Agent E — MES only (not MYM)
.\.venv-research\Scripts\python.exe .claude\skills\databento-data\scripts\db_fetch.py pull `
  --symbols MES.c.0 --stype continuous --schema ohlcv-1d `
  --start 2019-05-06 --end 2022-01-01 --max-cost 1.00 `
  --out lab\analysis\harv_0_month_end_rebalance_es_2026-07\data\_part_MES_c_0_2019.parquet

.\.venv-research\Scripts\python.exe .claude\skills\databento-data\scripts\db_fetch.py pull `
  --symbols MES.c.0 --stype continuous --schema ohlcv-1d `
  --start 2022-01-01 --end 2026-07-01 --max-cost 1.00 `
  --out lab\analysis\harv_0_month_end_rebalance_es_2026-07\data\_part_MES_c_0_2022.parquet
```

Always `estimate` immediately before each `pull` if the batch script isn’t wrapping it (db_fetch re-estimates inside `pull`, but a dry-run first still matches house rule).

---

## 5. Risks if we defer breadth / controls

| Deferral | Risk | Severity |
|---|---|---|
| **YM / MYM** | Lose same-driver breadth corroboration; cannot show “ES-only quirk.” Does **not** invalidate §6. | Low for verdict; medium for narrative / 08-08 packet |
| **GC until after H1** | If H1 passes, wall-clock delay before RESOLVED/AMBIGUOUS. If you forget to pull GC and claim RESOLVED → **protocol break**. | Process risk, not statistical |
| **MES until after H1** | Same; also cannot claim RESOLVED without P-micro-OOS (§5.8 forbids skipping). FALSIFIED-at-primary remains valid without MES. | Process risk |
| **Closing FALSIFIED without computing C/G** | Annotation is informational for FALSIFIED; skipping is OK for gate, weaker for ops learning. | Low |
| **Treating missing P-instrument as pass** | `run_harv0` currently emits NaN/p=1.0 stub if GC absent — that must **not** be read as P-instrument pass. Wire explicit `SKIPPED` / refuse RESOLVED until GC lands. | **High** if misread |
| **4y ZN hang** | Unlikely (ES/YM succeeded); fallback = yearly only for the failing window. | Medium operational |
| **Sunk YM pull** | Already complete — no further deferral cost. Don’t re-pull. | None |

---

## Bottom line

**Fastest honest path:** abandon yearly ZN resume → **2× 4y ZN pulls** → Step-0/H1 on ES+ZN. That alone can produce a valid **FALSIFIED** §6 close. Pull **GC + MES** only if H1 survives; **never block on YM/MYM**. Expected remaining gate-critical Databento calls: **~3 now**, **+6 if H1 passes** — not ~100.
