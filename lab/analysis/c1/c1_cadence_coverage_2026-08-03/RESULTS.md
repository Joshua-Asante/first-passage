# c1 two-leg book — eval-geometry scoring + weekly-coverage measurement

**Run date:** 2026-08-03 · **Harness:** [`run_coverage.py`](run_coverage.py) · **Raw:** [`RESULTS.json`](RESULTS.json)
**Repo anchor:** `a1123b8`, worktree clean at run time.
**Status:** ACTIVE — 0.50× fails 16.0% of eval starts once overlapping pyramid holds are priced (critical scale 0.441×; 0.40× clean under all three proxies); the book covers 217/297 weeks and its idle weeks are +14.6% co-dependent, so one incumbent-shaped leg halves the cadence gap rather than closing it

**Scope:** measurement only. **$0 spent · K=0 consumed · no manifest opened · no `core/`, Pine, allocation, `dd_protection`, lifecycle-state, or rail change.**

Feeds two 2026-08-03 decision artifacts:
- [`docs/adr/2026-08-03-lifecycle-ladder-intermediate-rung.md`](../../../../docs/adr/2026-08-03-lifecycle-ladder-intermediate-rung.md) — §A size frontier
- [`docs/briefs/pre-registration/2026-08-03-c1-cadence-leg-preregistration.md`](../../../../docs/briefs/pre-registration/2026-08-03-c1-cadence-leg-preregistration.md) — §B weekly coverage

---

## §0 — Panels

| Leg | File | sha256 | Rows | Reconcile |
|---|---|---|---|---|
| MYM | `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-08-03_906e3.csv` | `bb2d52b705e433d7…` | 250 exits | **PASS** — Σ exits $34,168.88 = stated cumulative |
| MNQ | `Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-08-03_17bc9.csv` | `ecfe2ce3972ab7b8…` | 251 exits | **PASS** — Σ exits $90,000.44 = stated cumulative |

Span 2020-12-01 → 2026-08-03 (5.67 yr, 313 active days, 297 calendar weeks).

⚠ **Panel-provenance defect, unrepaired.** Both files were read from `C:\Users\joshu\Downloads\`
— **outside** `core/data/tv_exports/cme/`, whose current MYM/MNQ rows are the 2026-07-11 vintage.
This is the same manifest-tree bypass recorded against the 07-11 futures3/bustcut runs. The harness
takes explicit `--mym/--mnq` paths so the panel is an argument of record, and pins sha256 — but
**landing these into the manifest tree with a regenerated `SHA256SUMS` is a prerequisite for any
lock-grade use of these numbers.**

**Reconciliation scope.** Internal only (Σ exit rows = stated cumulative; per-contract commission
arithmetic verified: MYM $0.50/pt × 9, MNQ $2.00/pt, $1.82 RT both — matching `cost_per_side_usd:
0.91`). **No Pine-header lock-of-record reconciliation was performed** for the MYM/MNQ venue
editions. Per `trade-csv-reconcile` Step 5 that gate is not cleared.

---

## §A — Size frontier (rolling eval, all start dates, intraday-enforced, integer contracts)

Tradeify Select 100K **evaluation** geometry: floor `= peak_EOD − $3,000` (**no lock** — the
`dd_lock_offset_usd: 100` in `core/firm_rules.py` models a mechanism the eval does not have),
target $106,000, ≥3 trading days, best day ≤ 40% of profit, 400-calendar-day horizon.

| Rung | Pass | Fail | Slow | max DD intraday | Headroom ×(vs $3,000) | Median cal. days |
|---|---|---|---|---|---|---|
| 0.25× | 38.7% | **0.0%** | 61.3% | $1,556 | 1.93 | 316 |
| 0.34× | 63.8% | **0.0%** | 36.2% | $2,157 | 1.39 | 255 |
| **0.40×** | **64.8%** | **0.0%** | 35.2% | $2,495 | **1.20** | 228 |
| 0.50× (deployed) | 59.9% | **16.0%** | 24.1% | $3,361 | **0.89** | 203 |
| 1.00× | 13.2% | 79.4% | 7.4% | $6,809 | 0.44 | 99 |

**Headroom ×** = $3,000 ÷ max-DD-intraday at that rung. Below 1.00 the worst historical excursion
consumes the whole rope. **The absolute critical scale is 0.441×** (the 1.00× row).

**0.50× is dominated, not a risk/return trade-off** — 0.40× passes *more often* (64.8% vs 59.9%)
**and** never fails on this path.

### Proxy sensitivity — the load-bearing sensitivity

Intraday enforcement is modelled from per-trade MAE under three overlap assumptions:

| Proxy | 0.40× fail | 0.50× fail | Critical scale |
|---|---|---|---|
| `seq` — realized-only sequencing | 0.0% | **0.0%** | 0.533× |
| `cluster` — overlapping holds summed | 0.0% | **16.0%** | **0.441×** |
| `joint` — all same-day trades at max adverse | 0.0% | 16.0% | 0.441× |

`cluster` ≡ `joint` here, which locates the damage **inside a single leg**, not across MYM+MNQ (they
are co-active on only 51 of 313 days, daily correlation −0.04). A pyramid opens its add *while the
base is live*, so the overlap is structural, not incidental — `cluster` is the honest proxy and
`seq` is the one that flatters 0.50× to zero. **0.40× is 0.0% under all three.**

### Pyramid attribution (classified by ENTRY signal)

| Leg | Base legs | Base net | Add legs | Add net | Add share |
|---|---|---|---|---|---|
| MYM | 218 | $14,556 | 32 | $19,613 | **57.4%** |
| MNQ | 207 | $13,029 | 44 | $76,971 | **85.5%** |

Classifying by the **exit** signal undercounts (adds exiting via `EOD Flat`/`Max Hold` are missed) —
it reads MYM at 25 adds and −$2,079, flipping the sign. Entry-signal classification is correct.

---

## §B — Weekly coverage

| | Weeks | Share |
|---|---|---|
| Calendar weeks in span | 297 | — |
| MYM active | 152 | 51.2% |
| MNQ active | 154 | 51.9% |
| **Book active (union)** | **217** | **73.1%** |
| **Idle (zero trades)** | **80** | **26.9%** |

Activity gaps: median 4 days, **max 78 days**, 77 gaps > 7 days, 26 gaps > 14 days.
Tradeify requires ≥1 trade per week (art. 10468318) ⇒ **77 breaches over the span**.

**Idleness is positively dependent, not independent.** Observed co-idle 80 weeks vs 69.8 expected
under independence ⇒ **+14.6% excess**. The two legs go quiet *together* more than chance.

**Marginal coverage of a second leg (measured):** MNQ covers **44.8%** of MYM's 145 idle weeks;
MYM covers **44.1%** of MNQ's 143. A second index-breakout leg closes under half the gap.

### Generous projection — residual idle weeks after adding 1…5 legs

Each added leg assumed **fully independent** of every other. The measured legs are positively
dependent (+14.6%), so this **overstates** what a real leg would cover; a failure here is conclusive.

| Added leg | p(fires in a given week) | +1 | +2 | +3 | +4 | +5 |
|---|---|---|---|---|---|---|
| Incumbent-like (~45 trade-days/yr) | 0.512 | **39.1** | 19.1 | 9.3 | 4.5 | 2.2 |
| Higher-frequency | 0.750 | 20.0 | 5.0 | 1.2 | 0.3 | 0.1 |
| ORB-like | 0.900 | **8.0** | 0.8 | 0.1 | 0.0 | 0.0 |
| Near-unconditional (fires ~99% of *days*) | 0.994 | **0.5** | 0.0 | 0.0 | 0.0 | 0.0 |

**Per eval window** (32.6 weeks at the 0.40× median of 228 calendar days), expected idle weeks:
book as-is **8.8** → +1 incumbent-like **4.3** → +1 ORB-like **0.9** → +1 near-unconditional **0.1**.

**The decisive finding:** a leg shaped like the incumbents does *not* solve cadence even under the
generous assumption — it halves the gap. Only a leg firing in **≥ ~90% of weeks** reduces expected
idle weeks per eval below 1. That is a frozen admission floor derived *before* any candidate exists.

---

## §C — What this measurement does NOT establish

1. **These are not probabilities.** 310 overlapping start dates drawn from **one** 5.67-year path;
   the effective independent sample is closer to ~10 evals. Error bars are wide. The correct
   instrument is the week-block bootstrap in `core/portfolio_mc.py` driven through
   `simulation.py`'s `intraday_low` argument.
2. **Intraday enforcement is an MAE proxy, not bar data.** `cluster` is the right direction; a real
   `intraday_low` series from 15m bars would supersede it.
3. **Inactivity barrier is OFF**, matching the re-MC convention. With it ON the repo has measured
   92.6–97.6% path death (`lab/analysis/c1/c1_cadence_inactivity_2026-08-02`). Every pass rate above
   presumes a cadence mitigation that does not yet exist at the execution layer (residual track R8).
4. **No Pine-header reconciliation** (see §0) and **no manifest-tree placement**.
5. **Regime split reported, not gated:** both halves hold at 0.40–0.50× under `seq`
   (H1 critical 0.533×, H2 0.540×); at 1.00× H2 is materially worse (62.4% vs 41.5% fail).

---

## §D — Reproduce

```bash
cd lab/analysis/c1/c1_cadence_coverage_2026-08-03
python run_coverage.py \
  --mym "<path>/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-08-03_906e3.csv" \
  --mnq "<path>/Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-08-03_17bc9.csv"
```

Panel identity is asserted by sha256 in `RESULTS.json` → `panels.*.sha256`; a differing hash
invalidates every number above.
