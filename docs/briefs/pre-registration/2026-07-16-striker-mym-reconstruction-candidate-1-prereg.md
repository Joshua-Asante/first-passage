# Pre-registration — Striker→MYM reconstruction candidate #1 (MYM opening-range continuation)

**Status:** `FROZEN` (operator signed §9, 2026-07-16)
**Candidate ID:** `S-MYM-ORC-01`
**Question:** [`Q-STRIKER-MYM-RECON-1`](../Q-STRIKER-MYM-RECON-1-venue-native-continuation.md)
**Authored:** 2026-07-16
**Candidate class:** new venue-native Striker-family strategy; not Class S and not a locked-Pine transfer
**Instrument / timeframe:** `CBOT_MINI:MYM1!` / 15m
**Loop of record:** STRATEGIC / INQHIORI
**K declaration:** `K_reconstruction = 1`; this artifact contains **NO GRID**

No candidate P&L has been computed from the 2026-07-16 MYM bar panel. The only pre-author reads were integrity, event-frequency, ATR/cost, and cap-feasibility diagnostics disclosed in §7. Operator signature in §9 is required before Stage 1.

---

## §0 — Rule-0 reads (verified 2026-07-16)

- Reconstruction ADR — commit `9aa2dbf`; new MYM/MNQ candidates allowed, while R5/P2 and locked Pine remain untouched.
- Striker DJ30 LOCK — commit `48a7a48`; lineage is long breakout + pyramid, but its parameters are not candidate defaults.
- MYM FUTURES_LOCK — commit `fe83d17`; verifies MYM point/tick value, integer sizing, cap pressure, cost, and force-flat semantics.
- R5 MYM RESULTS + P2 ADR — commit `fad8984`; preservation claims falsified, while mapped MYM absolute PF≈2 is prior evidence only.
- `core/firm_rules.py` — commit `a53ee99`; `Tradeify_Select_100K` cap 80 and index-micro commission $0.91/side; force-flat firm semantics.
- Opening-anchor null lesson — commit `514a366`; same-day window-slide, not cross-day or direction-flip.
- Frozen survivor gate — commit `be6dda6`; downstream only, not run or amended here.
- MYM parsed panel SHA256 `298ab8c8900f1144b450537f14e356681aec7448b4787ebc770de88c83f9059c`.
- Raw MYM BAR EXPORT SHA256 `57b96597aef9a4e48a69a2c67b83c1eb10d9442af90b78984db36ccbb3c02d89`.

---

## §1 — Claim and unit of test

**Claim:** an exact long-only, same-session MYM opening-range continuation rule can produce an opening-anchor-specific edge whose gross expectancy is at least four times measured all-in cost and remains positive on an untouched holdout.

**Not claimed:** preservation of DJ30 CFD edge, correctness of R5/P2, superiority to locked Striker, firm survivability, or deployability.

**Unit:** one completed base trade, including its optional single add, expressed in base-risk R. Costs include every filled base/add entry and exit.

---

## §2 — Frozen candidate semantics (one candidate; no selection)

### §2.1 Data and clock

| Item | Frozen value |
| --- | --- |
| Bar panel | `core/data/bar_data/MYM_M15.csv`, SHA256 `298ab8c…f9059c` |
| Chart | `CBOT_MINI:MYM1!`, 15m, adjust-for-contract-changes ON |
| Clock | `America/New_York` (DST-aware), never fixed UTC |
| Development | 2020-07-01 through 2023-12-31 |
| Untouched P&L holdout | 2024-01-01 through 2026-06-30 |
| Incomplete tail | 2026-07-01 onward excluded |
| Roll handling | seam bars flagged by registered MYM quarterly cycle; a signal touching a seam bar is retained and tagged, not silently deleted |

### §2.2 Signal

1. Build the opening range from exactly the two 15m bars opening at **09:30 and 09:45 ET**.
2. Long-only candidate. No short side.
3. Eligible signal bars open from **10:00 through 11:45 ET**.
4. The first eligible bar whose **close is strictly above the opening-range high** signals one trade.
5. Fill the base at the **next bar open**; therefore the latest base fill is 12:00 ET.
6. One signal / base trade per RTH date. No day-of-week, volatility, news, or regime filter.

### §2.3 Risk, add, and exits

| Item | Frozen value |
| --- | --- |
| ATR | Wilder/RMA ATR(11), known using bars through the signal close only |
| Initial stop | base fill − `2.00 × ATR(11)` fixed at base fill |
| Base risk | 0.35% of static $100,000 research balance |
| MYM value | $0.50 / index point / contract; 1-point tick = $0.50 |
| Base quantity | `floor($350 / (stop_points × $0.50))`, capped at 40; quantity 0 = skipped signal, logged |
| Add | exactly one add, quantity = base quantity, when a bar close first reaches base fill + 1.00 initial R; fill next bar open |
| Add timing | not before four complete bars after base fill |
| Stop after add | from add fill onward, stop for all contracts = base fill (break-even on base; add can lose) |
| Profit target | base fill + 4.00 initial R, for all open contracts |
| Maximum hold | exit at next bar open after 12 complete bars from base fill |
| Force-flat | Pine trigger 15:45 ET; expected fill 16:00 ET; zero fills after 16:00 ET |
| Priority on same bar | conservative: stop before target/add; add is not filled if stop and add threshold are both touched before ordering is knowable |
| Pyramiding | base + one 100% add only; total cap 80 |

This is a new strategy. The locked 15-bar breakout, Tue/Fri filter, 1.20×ATR stop, 8.5×ATR target, 750% pyramid, BE/trail values, and CFD risk are not imported.

### §2.4 Costs

Stage 1/2 use the conservative intended-firm index-micro model:

- commission: **$0.91/contract/side**;
- slippage: **1 MYM tick ($0.50) per contract per filled side**;
- every base/add entry and exit pays both;
- gross and net P&L are both emitted; cost_R uses actual fills and base-risk R.

No lower-cost rerun may replace a failure. Per-firm cost differences are downstream diagnostics only.

---

## §3 — Frozen test protocol

### §3.1 Step-0 integrity

Hard requirements:

- SHA256 equals §0;
- exactly 141,471 rows and span 2020-07-01T00:00:00Z→2026-07-02T00:00:00Z;
- timestamps strictly increasing and unique;
- finite OHLC; `high ≥ max(open,close,low)` and `low ≤ min(open,close,high)`;
- DST-aware ET conversion;
- no result row may include 2026-07-01 onward.

Failure is `AMBIGUOUS-HOLD`, not an economic failure.

### §3.2 Development-only run

The first implementation runs with an enforced date ceiling of 2023-12-31 and emits:

- every signal/fill/exit row;
- N, gross/net expectancy in R, actual cost_R, PF, max DD, DSR, block-bootstrap CI;
- year and half-window tables;
- drop-top-5 result;
- cap/quantity-zero/force-flat/seam diagnostics;
- config fingerprint and script hash.

No parameter is selected. `K_reconstruction` remains 1.

### §3.3 Opening-anchor placebo

On development dates only, test whether 09:30 is special:

- identical rule, duration, stop/add/exit/cost semantics;
- replace the 09:30 anchor with a same-day 30m range starting at one of **09:45, 10:00, 10:15, 10:30, 10:45, or 11:00 ET**;
- entry eligibility shifts with the anchor: starts immediately after that 30m range and lasts eight 15m bars;
- 10,000 date-wise random anchor assignments, seed 42;
- one-sided `p = (1 + count(null_mean_net_R ≥ observed_mean_net_R)) / 10001`.

The placebo windows are nulls, not candidate variants; their best result cannot be promoted.

### §3.4 Pine parity before holdout

After all development gates pass:

1. implement `S-MYM-ORC-01` as a new gitignored/hash-pinned Pine candidate;
2. export development-window trades;
3. require exact base-signal timestamp parity and exact trade count versus offline;
4. permit price/P&L differences only when explained by TradingView’s documented intrabar fill convention; any unexplained timing difference is `AMBIGUOUS-HOLD`.

The holdout run is forbidden until parity passes and the offline/Pine/config hashes are recorded.

### §3.5 One-shot holdout

Run 2024-01-01→2026-06-30 exactly once. No development rerun or semantic edit after holdout is opened. Append all metrics to RESULTS and mechanically apply §6.

---

## §4 — Power and multiplicity disclosure

**H-MYM-ORC-1:** If the exact §2 candidate clears every development and untouched-holdout gate, then a cost-reachable venue-native MYM continuation candidate exists; otherwise the candidate is falsified. **Accept H-MYM-ORC-1 if** D0–D9 and H0–H9 all pass. **Reject H-MYM-ORC-1 if** any validly-computed D1–D9 or H1–H9 gate fails. A D0/H0 measurement failure is `AMBIGUOUS-HOLD`, never a numerical rescue.

- `K_reconstruction = 1`; there is no parameter/config winner.
- The spent mapped edition and locked CFD strategy are disclosed prior looks, not members of this candidate’s K.
- Any semantic alternative—short side, different opening range, stop, target, add, session, filter, or direction—is a new candidate and increments the reconstruction bank.
- At illustrative per-trade σ≈1.1R, SE(mean) is ≈0.10R at N=120 and ≈0.12R at N=80. Therefore N floors are trade-rate bars, not standalone proof; the block-bootstrap CI and DSR carry statistical support.
- Holdout significance uses DSR with `K=1`, `var_trials=1`, threshold 0.95. PBO is not defined for a one-column, no-selection candidate; it becomes mandatory if any future pre-registration creates K>1.

---

## §5 — Forbidden moves

- No parameter grid or “small sensitivity check” before the verdict.
- No holdout P&L read before §9 is signed and development+parity pass.
- No day, year, seam, force-flat, or losing-trade deletion based on outcomes.
- No lower commission/slippage model as the headline after a fail.
- No replacing the opening-anchor placebo with direction-flip or cross-day permutation.
- No importing locked CFD defaults to rescue weak results.
- No using gross-only results to pass; net economics and 4× cost law both bind.
- No adding a second MYM candidate after all-limb failure without fresh operator authorization.
- No firm-tier MC, lifecycle admission, rail build, account registration, or live spend from this artifact.

---

## §6 — Frozen gates and verdict

The only economic verdicts are `RESOLVED` when every hard gate passes and `FALSIFIED` when any valid hard gate fails. `AMBIGUOUS-HOLD` is reserved for a measurement-integrity defect that prevents a valid computation; it is not available for a near-pass.

### §6.1 Cheap pre-author falsifier (already run; not candidate P&L)

| Check | Observed | Pre-author disposition |
| --- | ---: | --- |
| Development eligible RTH days / long OR-high break days | 904 / 531 | frequency feasible |
| Holdout eligible days / long OR-high break days (count only) | 643 / 363 | N≥80 plausible; no P&L viewed |
| Recent-90d ATR(11) | 50.6885 pts | input to cost check only |
| 2×ATR risk / contract | $50.69 | — |
| Worst RT cost / cost_R | $2.82 / 0.0556R | 4× hurdle = 0.2225R |
| $100K @ 0.35%, base + one add | 6 + 6 contracts | 68-contract headroom vs cap 80 |

This only licenses the pre-registration. It does not satisfy a development or holdout gate.

### §6.2 Development hard gates (all required)

| ID | Gate |
| --- | --- |
| D0 | Step-0 integrity PASS |
| D1 | N ≥ 120 completed base trades |
| D2 | Opening-anchor placebo p < 0.05 |
| D3 | gross expectancy / mean actual cost_R ≥ 4.00 |
| D4 | net expectancy > 0R and PF ≥ 1.25 |
| D5 | stationary block-bootstrap 95% CI lower bound for mean net R > 0 |
| D6 | first-half and second-half net expectancy both > 0R |
| D7 | drop-top-5-trades net expectancy > 0R |
| D8 | max closed-equity DD ≤ 6.0% on the frozen $100K/0.35% sizing |
| D9 | zero fills after 16:00 ET; total contracts ≤80; quantity-zero skipped-signal rate ≤5% |

Any valid D1–D9 failure = `FALSIFIED` without opening holdout.

### §6.3 Holdout hard gates (all required)

| ID | Gate |
| --- | --- |
| H0 | offline↔Pine development signal parity PASS before holdout |
| H1 | N ≥ 80 completed base trades |
| H2 | gross expectancy / mean actual cost_R ≥ 4.00 |
| H3 | net expectancy > 0R and PF ≥ 1.20 |
| H4 | DSR ≥ 0.95 at K=1 |
| H5 | stationary block-bootstrap 95% CI lower bound for mean net R > 0 |
| H6 | 2024 and 2025-01-01→2026-06-30 net expectancy both > 0R |
| H7 | drop-top-5-trades net expectancy > 0R |
| H8 | max closed-equity DD ≤ 6.0% |
| H9 | zero fills after 16:00 ET; total contracts ≤80; quantity-zero skipped-signal rate ≤5% |

### §6.4 Verdict table

| Verdict | Trigger | Disposition |
| --- | --- | --- |
| `RESOLVED` | D0–D9 and H0–H9 all pass | Candidate exists; pin artifacts and open separate firm-tier survivor-scoring pre-registration |
| `FALSIFIED` | Any validly-computed D1–D9 or H1–H9 gate fails | Close candidate #1; no in-place edit; second MYM candidate requires fresh operator authorization |
| `AMBIGUOUS-HOLD` | D0 or H0 fails, deterministic replay differs, or an implementation defect makes any metric invalid | Repair measurement only and rerun byte-identical semantics; if semantics must change, close and re-register |

There is no “near pass,” discretionary override, or holdout extension branch.

---

## §7 — Prior-look disclosure

| Date | Look | Information seen | Constraint imposed |
| --- | --- | --- | --- |
| 2026-07-03/06 | P2 locked replay | DJ30↔MYM divergence 8.51%; E1 miss | no locked-transfer claim or replay |
| 2026-07-09 | R5 MYM mapped edition | OOS PF 2.038; preservation ratio 0.559; cost/force-flat/cap attribution | mapped settings excluded; motivates new candidate |
| 2026-07-15/16 | Class-S candidate #1 | MYM+MNQ Part A discharged; regime-fragile | no alpha claim; downstream only |
| 2026-07-16 | Floor refresh | MYM full/recent floor $3,234/$4,350 | feasibility only |
| 2026-07-16 | Cheap falsifier §6.1 | integrity, counts, ATR, cost_R, cap headroom; **no P&L** | disclosed; holdout is P&L-untouched |

No MYM opening-range-continuation P&L result has been viewed.

---

## §8 — Run outputs

Required path after freeze:
`lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/`

Required artifacts:

- `RUNSPEC.md` — verbatim §2 machine-readable config + hashes;
- `cheap_falsifier.py` — reproduces §6.1;
- `candidate_offline.py` + tests;
- `DEVELOPMENT_RESULTS.md`;
- candidate Pine hash entry (gitignored source);
- parity report;
- `HOLDOUT_RESULTS.md`;
- consolidated `RESULTS.md`;
- closure artifact under `docs/briefs/closures/`.

All outputs are append-only after holdout opens.

---

## §9 — Operator signature (freeze gate)

```text
SIGNED / FROZEN: 2026-07-16 / JA
Candidate: S-MYM-ORC-01 exactly as §2
K_reconstruction = 1; NO GRID
Development gates D0-D9 and holdout gates H0-H9 fixed
No candidate P&L and no Pine build before this signature
```

Changing any §2 or §6 item after signature voids this artifact and requires a fresh pre-registration.

---

## §10 — Audit hooks

```bash
# Signature and one-candidate declaration
grep -n "SIGNED / FROZEN:\|K_reconstruction = 1\|NO GRID" \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md

# Frozen panel bytes
sha256sum core/data/bar_data/MYM_M15.csv
grep "MYM_M15.csv" core/data/bar_data/SHA256SUMS

# No locked/production changes
git diff -- core/strategies/striker/LOCK.md core/config/params.toml \
  core/dd_protection.py core/firm_rules.py

# Candidate semantics and all gates remain present
grep -n "09:30 and 09:45\|2.00 × ATR\|0.35%\|4.00 initial R\|D9\|H9" \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md

# No early result directory before signature
test ! -d lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07 || \
  grep -n "SIGNED / FROZEN:" \
    docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md --type brief

python scripts/check_data_manifests.py
git diff --check
```

---

## Change history

| Date | Change | By |
| --- | --- | --- |
| 2026-07-16 | Drafted exact K=1 MYM candidate and binary development/holdout gates; awaiting operator freeze | Cursor |
| 2026-07-16 | Operator selected “Freeze as drafted”; §9 signed, candidate semantics and gates frozen | JA + Cursor |
