# Pre-registration — Striker→MYM reconstruction candidate #2 (session-aware MYM opening-range continuation)

**Status:** `FROZEN` (operator selected re-registration and signed §9, 2026-07-16)
**Candidate ID:** `S-MYM-ORC-02`
**Question:** [`Q-STRIKER-MYM-RECON-2`](../Q-STRIKER-MYM-RECON-2-session-aware-continuation.md)
**Predecessor:** `S-MYM-ORC-01` — [`CLOSED-AMBIGUOUS`](../closures/2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md)
**Authored:** 2026-07-16
**Candidate class:** new venue-native Striker-family strategy; not Class S and not a locked-Pine transfer
**Instrument / timeframe:** `CBOT_MINI:MYM1!` / 15m
**Loop of record:** STRATEGIC / INQHIORI
**K declaration:** `K_reconstruction = 2`; this artifact contains **NO GRID**

Candidate #1's runner exited 2 before publishing artifacts with `AMBIGUOUS-HOLD: 2020-07-03: missing required 16:00 force-flat bar`. No metrics/artifacts were emitted, no candidate P&L was inspected, and no holdout P&L was opened. The operator selected “Close AMBIGUOUS and re-register session-aware force-flat semantics.”

Candidate #2 keeps every candidate #1 candidate semantic and D1–D9/H0–H9 threshold unchanged except the force-flat clock is made session-calendar aware in §2.3/§3.1/D0/D9/H9. H4 retains DSR ≥0.95 but correctly binds cumulative `K=2` and the canonical unconditional `V=1/n`; candidate #1 produced no valid returns and none are fabricated.

---

## §0 — Rule-0 reads (verified 2026-07-16)

- `docs/briefs/Q-STRIKER-MYM-RECON-1-venue-native-continuation.md` — latest source anchor `812f68d`; original question and verdict contract.
- `docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md` — latest source anchor `812f68d`; frozen baseline transcribed below.
- `lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/candidate_offline.py:307-312` — verified the universal-16:00 requirement that raised the measurement exception.
- `docs/superpowers/plans/2026-07-16-striker-mym-orc-development-harness.md` — working-tree plan read 2026-07-16; exit 2 is the no-artifact `AMBIGUOUS-HOLD` path.
- `docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` §2.3 — latest source anchor `812f68d`; unconditional `V=1/n` is canonical.
- MYM parsed panel SHA256 `298ab8c8900f1144b450537f14e356681aec7448b4787ebc770de88c83f9059c`.
- Raw MYM BAR EXPORT SHA256 `57b96597aef9a4e48a69a2c67b83c1eb10d9442af90b78984db36ccbb3c02d89`.
- `lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json` — exact 53 date→fill-minute mappings derived from timestamps only; canonical working-tree-byte SHA256 `7ff65ef4b0bdceb620f077708e55075f5f4295ae6fd594a56595282e72a8a3bd`.

No P&L was read while deriving or verifying the session calendar.

---

## §1 — Claim and unit of test

**Claim:** an exact long-only, same-session MYM opening-range continuation rule can produce an opening-anchor-specific edge whose gross expectancy is at least four times measured all-in cost and remains positive on an untouched holdout, when force-flat follows the panel's pre-registered standard/early-close session calendar.

**Not claimed:** preservation of DJ30 CFD edge, correctness of R5/P2, superiority to locked Striker, firm survivability, deployability, or any economic inference from candidate #1's aborted run.

**Unit:** one completed base trade, including its optional single add, expressed in base-risk R. Costs include every filled base/add entry and exit.

---

## §2 — Frozen candidate semantics (one successor candidate; no selection)

### §2.1 Data and clock

| Item | Frozen value |
| --- | --- |
| Bar panel | `core/data/bar_data/MYM_M15.csv`, SHA256 `298ab8c…f9059c` |
| Session calendar | `lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json`, SHA256 `7ff65ef4…a8a3bd` |
| Calendar payload | exactly 53 date→force-flat-fill-minute mappings; values are ET minute-of-day 765 (12:45) or 780 (13:00) |
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

### §2.3 Risk, add, exits, and session-aware force-flat

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
| Standard force-flat | order generated on 15:45 ET bar; fill at 16:00 ET |
| Allowlisted early-close force-flat | on an exact calendar date, fill at the mapped final available RTH bar open (12:45 or 13:00 ET); order generated exactly one 15m bar earlier |
| Post-force-flat rule | no base entry, add entry, stop exit, target exit, maximum-hold exit, or other exit may fill after that date's scheduled force-flat |
| Priority on same bar | conservative: stop before target/add; add is not filled if stop and add threshold are both touched before ordering is knowable |
| Pyramiding | base + one 100% add only; total cap 80 |

The session-calendar rule is exhaustive:

- a date present in the canonical JSON must use its exact mapped fill minute;
- a date absent from the JSON must use 16:00 ET;
- the trigger bar must be exactly 15 minutes before the scheduled fill;
- dynamic “last observed bar” inference is forbidden;
- any missing, extra, or mismatched date/time/adjacency is D0 `AMBIGUOUS-HOLD`, not an economic fail.

This is the sole candidate-semantic change from candidate #1. The locked 15-bar breakout, Tue/Fri filter, 1.20×ATR stop, 8.5×ATR target, 750% pyramid, BE/trail values, and CFD risk are not imported.

### §2.4 Costs

Stage 1/2 use the unchanged conservative intended-firm index-micro model:

- commission: **$0.91/contract/side**;
- slippage: **1 MYM tick ($0.50) per contract per filled side**;
- every base/add entry and exit pays both;
- gross and net P&L are both emitted; cost_R uses actual fills and base-risk R.

No lower-cost rerun may replace a failure. Per-firm cost differences are downstream diagnostics only.

---

## §3 — Frozen test protocol

### §3.1 Step-0 integrity

Hard requirements:

- panel SHA256 equals §0;
- exactly 141,471 rows and span 2020-07-01T00:00:00Z→2026-07-02T00:00:00Z;
- timestamps strictly increasing and unique;
- finite OHLC; `high ≥ max(open,close,low)` and `low ≤ min(open,close,high)`;
- DST-aware ET conversion;
- no result row may include 2026-07-01 onward;
- session-calendar SHA256 equals §0 and parses as exactly 53 unique ISO dates;
- calendar distribution is exactly 41 mappings to minute 765 and 12 to minute 780;
- development distribution is exactly 29 mappings (23 minute-765, 6 minute-780);
- holdout distribution is exactly 24 mappings (18 minute-765, 6 minute-780);
- every allowlisted date has its mapped bar and the immediately prior 15m trigger bar;
- no non-allowlisted eligible session substitutes 12:45/13:00 for the standard 16:00 fill;
- every scored session's scheduled trigger→fill interval is exactly 15 minutes;
- no entry or exit fill occurs after the scheduled force-flat.

Any failure is `AMBIGUOUS-HOLD`, not an economic failure.

### §3.2 Development-only run

The first implementation runs with an enforced date ceiling of 2023-12-31 and emits:

- every signal/fill/exit row;
- N, gross/net expectancy in R, actual cost_R, PF, max DD, DSR, block-bootstrap CI;
- year and half-window tables;
- drop-top-5 result;
- cap/quantity-zero/force-flat/seam diagnostics;
- standard versus allowlisted force-flat counts;
- config, calendar, panel, script, and output fingerprints.

No parameter is selected. `K_reconstruction` remains 2.

### §3.3 Opening-anchor placebo

On development dates only, test whether 09:30 is special:

- identical rule, duration, stop/add/exit/cost and session-calendar force-flat semantics;
- replace the 09:30 anchor with a same-day 30m range starting at one of **09:45, 10:00, 10:15, 10:30, 10:45, or 11:00 ET**;
- entry eligibility shifts with the anchor: starts immediately after that 30m range and lasts eight 15m bars;
- 10,000 date-wise random anchor assignments, seed 42;
- one-sided `p = (1 + count(null_mean_net_R ≥ observed_mean_net_R)) / 10001`.

The placebo windows are nulls, not candidate variants; their best result cannot be promoted.

### §3.4 Pine parity before holdout

After all development gates pass:

1. implement `S-MYM-ORC-02` as a new gitignored/hash-pinned Pine candidate;
2. bind the same calendar SHA and scheduled force-flat semantics;
3. export development-window trades;
4. require exact base-signal timestamp, scheduled-force-flat timestamp, and trade-count parity versus offline;
5. permit price/P&L differences only when explained by TradingView's documented intrabar fill convention; any unexplained timing difference is `AMBIGUOUS-HOLD`.

The holdout run is forbidden until parity passes and the offline/Pine/config/calendar hashes are recorded.

### §3.5 One-shot holdout

Run 2024-01-01→2026-06-30 exactly once. No development rerun, calendar edit, or semantic edit after holdout is opened. Append all metrics to RESULTS and mechanically apply §6.

---

## §4 — Power and multiplicity disclosure

**H-MYM-ORC-2:** If the exact §2 candidate clears every development and untouched-holdout gate, then a cost-reachable venue-native MYM continuation candidate exists; otherwise the candidate is falsified. **Accept H-MYM-ORC-2 if** D0–D9 and H0–H9 all pass. **Reject H-MYM-ORC-2 if** any validly-computed D1–D9 or H1–H9 gate fails. A D0/H0 measurement failure is `AMBIGUOUS-HOLD`, never a numerical rescue.

- `K_reconstruction = 2`; there is no parameter/config winner.
- Candidate #1 is a spent semantic candidate and therefore counts in cumulative K, but its aborted run produced no valid return series.
- H4 uses DSR threshold 0.95 with cumulative `K=2` and `var_trials=1/n`, where `n` is candidate #2's valid holdout completed-trade count.
- `V=1/n` is the canonical unconditional rule from the 2026-07-12 DSR K/V ADR. `var_trials=1`, empirical cross-candidate variance, and a fabricated candidate #1 series are forbidden.
- PBO remains undefined: cumulative K is 2, but only candidate #2 can supply a valid return column, so there is no two-column selection matrix. This does not reduce DSR's cumulative K.
- The spent mapped edition and locked CFD strategy remain disclosed prior looks, not members of this reconstruction candidate bank.
- Any further semantic alternative—short side, different opening range, stop, target, add, session-calendar mapping, filter, or direction—is candidate #3 and increments the reconstruction bank.
- At illustrative per-trade σ≈1.1R, SE(mean) is ≈0.10R at N=120 and ≈0.12R at N=80. Therefore N floors are trade-rate bars, not standalone proof; the block-bootstrap CI and DSR carry statistical support.

---

## §5 — Forbidden moves

- No parameter grid or “small sensitivity check” before the verdict.
- No holdout P&L read before development+parity pass.
- No edit to the 53-date calendar after any candidate #2 P&L is read.
- No dynamic last-bar inference in place of exact calendar membership and time.
- No day, year, seam, force-flat, or losing-trade deletion based on outcomes.
- No fill after a date's scheduled force-flat.
- No lower commission/slippage model as the headline after a fail.
- No replacing the opening-anchor placebo with direction-flip or cross-day permutation.
- No importing locked CFD defaults to rescue weak results.
- No using gross-only results to pass; net economics and 4× cost law both bind.
- No `K=1`, `var_trials=1`, empirical candidate-column V, or fabricated candidate #1 returns at H4.
- No adding candidate #3 after all-limb failure without fresh operator authorization.
- No firm-tier MC, lifecycle admission, rail build, account registration, or live spend from this artifact.

---

## §6 — Frozen gates and verdict

The only economic verdicts are `RESOLVED` when every hard gate passes and `FALSIFIED` when any valid hard gate fails. `AMBIGUOUS-HOLD` is reserved for a measurement-integrity defect that prevents a valid computation; it is not available for a near-pass.

### §6.1 Cheap pre-author diagnostic (already run; timestamps/event frequency only, not candidate P&L)

| Check | Observed | Pre-author disposition |
| --- | ---: | --- |
| Development eligible RTH days / long OR-high break days | 904 / 531 | candidate #1 frequency prior, unchanged |
| Holdout eligible days / long OR-high break days (count only) | 643 / 363 | N≥80 plausible; no P&L viewed |
| Development early-close sessions / OR-break days | 29 / 16 | session-calendar scope only |
| Development early-close fill minutes | 23 at 765 / 6 at 780 | exact calendar diagnostic |
| Holdout early-close sessions / OR-break days | 24 / 12 | count only; no P&L viewed |
| Holdout early-close fill minutes | 18 at 765 / 6 at 780 | exact calendar diagnostic |
| Total early-close sessions | 53 | exact mapping frozen by SHA256 |
| Recent-90d ATR(11) | 50.6885 pts | candidate #1 pre-author input; not recomputed |
| 2×ATR risk / contract | $50.69 | candidate #1 pre-author input; not recomputed |
| Worst RT cost / cost_R | $2.82 / 0.0556R | candidate #1 pre-author input; 4× hurdle = 0.2225R |
| $100K @ 0.35%, base + one add | 6 + 6 contracts | candidate #1 pre-author input; cap-safe |

The runner's aborted invocation emitted no metric or result artifact. This table only licenses the successor pre-registration; it does not satisfy any development or holdout gate.

### §6.2 Development hard gates (all required)

| ID | Gate |
| --- | --- |
| D0 | Step-0 integrity PASS, including exact calendar SHA/count/distribution, exact allowlist membership, exact scheduled fill time, exact 15m trigger→fill adjacency, and zero post-scheduled-force-flat fills |
| D1 | N ≥ 120 completed base trades |
| D2 | Opening-anchor placebo p < 0.05 |
| D3 | gross expectancy / mean actual cost_R ≥ 4.00 |
| D4 | net expectancy > 0R and PF ≥ 1.25 |
| D5 | stationary block-bootstrap 95% CI lower bound for mean net R > 0 |
| D6 | first-half and second-half net expectancy both > 0R |
| D7 | drop-top-5-trades net expectancy > 0R |
| D8 | max closed-equity DD ≤ 6.0% on the frozen $100K/0.35% sizing |
| D9 | zero fills after each date's scheduled force-flat; total contracts ≤80; quantity-zero skipped-signal rate ≤5% |

Any valid D1–D9 failure = `FALSIFIED` without opening holdout. Any D0 calendar/time/adjacency mismatch = `AMBIGUOUS-HOLD`.

### §6.3 Holdout hard gates (all required)

| ID | Gate |
| --- | --- |
| H0 | offline↔Pine development signal and scheduled-force-flat parity PASS before holdout |
| H1 | N ≥ 80 completed base trades |
| H2 | gross expectancy / mean actual cost_R ≥ 4.00 |
| H3 | net expectancy > 0R and PF ≥ 1.20 |
| H4 | DSR ≥ 0.95 at cumulative K=2 and unconditional V=1/n, n = valid candidate #2 holdout completed trades |
| H5 | stationary block-bootstrap 95% CI lower bound for mean net R > 0 |
| H6 | 2024 and 2025-01-01→2026-06-30 net expectancy both > 0R |
| H7 | drop-top-5-trades net expectancy > 0R |
| H8 | max closed-equity DD ≤ 6.0% |
| H9 | zero fills after each date's scheduled force-flat; total contracts ≤80; quantity-zero skipped-signal rate ≤5% |

### §6.4 Verdict table

| Verdict | Trigger | Disposition |
| --- | --- | --- |
| `RESOLVED` | D0–D9 and H0–H9 all pass | Candidate exists; pin artifacts and open separate firm-tier survivor-scoring pre-registration |
| `FALSIFIED` | Any validly-computed D1–D9 or H1–H9 gate fails | Close candidate #2; no in-place edit; candidate #3 requires fresh operator authorization |
| `AMBIGUOUS-HOLD` | D0 or H0 fails; any calendar membership/time/15m-adjacency/post-force-flat assertion fails; deterministic replay differs; or an implementation defect makes any metric invalid | Close or repair measurement byte-identically; any semantic/calendar change requires fresh registration |

There is no “near pass,” discretionary override, calendar extension, or holdout extension branch.

---

## §7 — Prior-look disclosure

| Date | Look | Information seen | Constraint imposed |
| --- | --- | --- | --- |
| 2026-07-03/06 | P2 locked replay | DJ30↔MYM divergence 8.51%; E1 miss | no locked-transfer claim or replay |
| 2026-07-09 | R5 MYM mapped edition | OOS PF 2.038; preservation ratio 0.559; cost/force-flat/cap attribution | mapped settings excluded; motivates new candidate |
| 2026-07-15/16 | Class-S candidate #1 | MYM+MNQ Part A discharged; regime-fragile | no alpha claim; downstream only |
| 2026-07-16 | Candidate #1 cheap falsifier | integrity, counts, ATR, cost_R, cap headroom; no candidate P&L | disclosed; values carried unchanged |
| 2026-07-16 | Candidate #1 aborted runner | exit 2 on 2020-07-03 missing 16:00 bar; no result artifacts | no economic inference; candidate #1 closes AMBIGUOUS |
| 2026-07-16 | Timestamp-only session census | development 29/16 OR-break; holdout 24/12; exact 53 dates and fill minutes | calendar frozen by hash; no P&L viewed |

No MYM opening-range-continuation P&L result has been viewed.

---

## §8 — Run outputs

Implementation remains under:
`lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/`

Required artifacts:

- `session_calendar.json` — frozen input, not an output;
- successor machine-readable runspec + hashes;
- calendar-aware offline candidate code + tests;
- `DEVELOPMENT_RESULTS.md`;
- candidate Pine hash entry (gitignored source);
- parity report;
- `HOLDOUT_RESULTS.md`;
- consolidated `RESULTS.md`;
- closure artifact under `docs/briefs/closures/`.

All outputs are append-only after holdout opens. No result output exists at this freeze.

---

## §9 — Operator signature (freeze gate)

```text
SIGNED / FROZEN: 2026-07-16 / JA
Authority: operator selected "Close AMBIGUOUS and re-register session-aware force-flat semantics"
Candidate: S-MYM-ORC-02 exactly as §2
K_reconstruction = 2; NO GRID
Development gates D0-D9 and holdout gates H0-H9 fixed
H4: DSR >= 0.95 at cumulative K=2 and V = 1/n
No candidate #2 P&L and no Pine build before this signature
```

Changing any §2 or §6 item after signature voids this artifact and requires a fresh pre-registration.

---

## §10 — Audit hooks

```bash
# Signature, cumulative bank, and no-grid declaration
grep -n "SIGNED / FROZEN:\|K_reconstruction = 2\|NO GRID\|V = 1/n" \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md

# Frozen panel and session-calendar bytes
sha256sum core/data/bar_data/MYM_M15.csv
sha256sum lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json

# Calendar exactness without reading OHLC or P&L
python -c "import json; p='lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json'; x=json.load(open(p)); assert len(x)==53; assert list(x)==sorted(x); assert sum(d<='2023-12-31' for d in x)==29; assert sum('2024-01-01'<=d<='2026-06-30' for d in x)==24; assert sum(v==765 for v in x.values())==41; assert sum(v==780 for v in x.values())==12"

# Every unchanged semantic and gate remains present
grep -n "09:30 and 09:45\|2.00 × ATR\|0.35%\|4.00 initial R\|D9\|H9" \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md

# No locked/production changes
git diff -- core/strategies/striker/LOCK.md core/config/params.toml \
  core/dd_protection.py core/firm_rules.py
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md --type brief

sha256sum lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json
python scripts/check_data_manifests.py
git diff --check
```

---

## Change history

| Date | Change | By |
| --- | --- | --- |
| 2026-07-16 | Candidate #1 closed AMBIGUOUS after no-artifact exit 2; successor frozen with exact session-calendar semantics, cumulative K=2, and H4 V=1/n | JA + Cursor |
