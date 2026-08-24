> ⚠ **2026-08-23 reader-intercept (R1 CLOCK repair, fix-pass):** the Gate table below (25K 0.40% ·
> 50K 1.13% · 100K 8.54% · 150K 8.54% · 250K 18.50% bust) is **EOD-clock**, produced on the same
> live `simulate_path` engine R1 measures, with `intraday_low` never populated — every bust figure
> here is a lower bound, not an estimate. The 100K/150K/250K cells are already FAIL against the
> current 3.0% survivor-scoring ceiling and can only deepen on the honest clock (monotonicity); the
> 25K/50K cells PASS on this clock but are a named, un-re-run residual — not confirmed to still PASS
> honest-clock. See
> [`../../analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md`](../../analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md)
> §2/§4b for the full accounting and why this campaign is not re-run. Frozen body unedited below.

# C4 — Bulenox force-flat re-MC (first full run)

**Disposition:** CLOSED — R6 NO-GO — futures-prop program closed 2026-07-10

**Date:** 2026-07-03
**Status:** FIRST force-flat re-MC number. **NOT lock-grade** — %-of-equity sizing (integer CME-micro-contract sizing = C5, owed); Bulenox `profit_target_pct` / `inactivity` still placeholder.
**Unblocked by:** operator's full-history US30 15m BAR_EXPORT (`BAR_EXPORT_v0.2_PEPPERSTONE_US30_2026-07-03_eb971.csv`) — parsed to **153,536 bars, 2020-01-02 → 2026-07-02**. The prior on-hand `US30_M15.csv` covered only 2026-03→06, which force-flat-truncated with KeyErrors on every pre-March-2026 overnight trade.

## What ran

DJ30 (force-flat @ 17:00 ET) + NAS100 (clean — 0% boundary crossings) under each Bulenox tier's trailing-DD rules (`FIRM_RULES["Bulenox_*"]`: trailing DD, no daily-loss limit, no static, no min-days, ~6% target). 1R **pinned** to `PRE_SHOCK_1R` (striker $4,229 / striker_nas100 $3,940; Q-SWAP-2/M-SWAP-1, `fell_back=False`) so DJ30's force-flat truncation surfaces as bust risk instead of being absorbed into a smaller position scale. 10K × 3 seeds. Panel 1119 bdays / 223 week-blocks.

## Three `force_flat_transform` bugs fixed (all real-data-path, previously unexercised; TDD — 16 tests green)

The wrapper was flagged "NOT YET VALIDATED against a real export" (module docstring / NOTES #2). This run was that validation; three defects surfaced:

1. **`Price` → `Price USD`.** Real Pepperstone List-of-Trades exports use `Price USD`. This is the documented 2026-07-02 fix that **never merged onto a live branch** — both this worktree and the primary checkout still had `Price` (byte-identical).
2. **datetime-into-string-column write-back TypeError.** The truncation write-back had never executed on real data; the 2026-07-02 partial run applied no force-flat. Now writes the boundary time as a `"%Y-%m-%d %H:%M"` string (`load_trades` re-parses it).
3. **17:00 ET = the CME/CFD daily settlement break.** Empirically **0 bars stamped 17:00** across all 2024 days (the 17:xx hour is empty: 16:45 → gap → 18:00). The exact-match bar lookup raised on every overnight trade. Fixed with a **bounded backward-asof** to the last bar ≤ boundary (normally 16:45, whose close *is* the 17:00 price), preserving the data-gap safety raise (> 12h prior ⇒ raise).

## Force-flat diagnostic

DJ30: **14/218 exits truncated (6.4%)**; net **$440,448 → $398,057 (−9.6%)**. In line with the ~89% net-retention estimate (2026-06-30 hold-compat analysis).

## Gate table (%-EQUITY sizing — see caveats)

| Tier | $bal | no-FF / C2-on (validation) | **FF / C2-off — GATE** | FF / C2-on (ref) | gate med-days |
|---|---:|---|---|---|---:|
| Bulenox_25K  | 25,000  | 99.99% / 0.01% | **99.60% / 0.40%** (p99 DD 5.09%) | 100.00% / 0.00% | 72 |
| Bulenox_50K  | 50,000  | 99.94% / 0.06% | **98.87% / 1.13%** (p99 DD 4.73%) | 99.98% / 0.02%  | 72 |
| Bulenox_100K | 100,000 | 95.17% / 4.83% | **91.46% / 8.54%** (p99 DD 2.97%) | 97.41% / 2.59%  | 67 |
| Bulenox_150K | 150,000 | 95.17% / 4.83% | **91.46% / 8.54%** (p99 DD 2.97%) | 97.41% / 2.59%  | 67 |
| Bulenox_250K | 250,000 | 79.67% / 20.33% | **81.50% / 18.50%** (p99 DD 2.19%) | 85.64% / 14.36% | 61 |

Bust is **100% trailing-DD** in every cell (Bulenox has no daily-loss / no static mode).

## Findings

- **Validation:** the no-FF / C2-on arm reproduces the 2026-07-02 partial-run bound **exactly** (50K 99.94% / 100–150K 95.17% / 250K 79.67%) — confirms data, 1R pin, and orchestrator are consistent with the prior session.
- **Force-flat *helps* (flips the "modestly adverse" prior).** Force-flat clips 9.6% of DJ30 net yet **raises** pass rate vs unconstrained (+0.01 to +5.97pp at C2-on). Mechanism: Bulenox busts are 100% trailing-DD, and DJ30's overnight holds are gap/tail-risk-heavy; removing them cuts the DD tail faster than the lost overnight profit costs. The venue's flat rule is mildly *protective* for this book, not a cost.
- **C2 (dd_protection overlay) does real work — and the gate can't use it.** C2-off drops pass materially (100K/150K 97.41% → 91.46%). Because the TV→TradersPost rail can't execute a portfolio-equity overlay at Bulenox, the honest gate-bearing arm is **C2-off** (the lower number).
- **Tier shape:** small tiers easiest (fixed-$ trailing DD = a *bigger* % cushion on a small balance), 250K worst. **But** this is where the next caveat bites hardest.

## Caveats (why this is a bound, not a lock)

1. **%-EQUITY, not integer-contract (C5 owed, biggest unknown).** Integer MNQ/MYM sizing rounds the base position down; below ~$21.6–35K MNQ base rounds toward 0 (Phase A floors), killing the NAS100 pyramid on small evals. So the **25K/50K ~99% is the least trustworthy** — it will degrade under integer sizing. The **100K/150K ~91.5%** is the more robust zone (floors clear comfortably). Integer sizing needs the Pine-verified floors (Gate B0 → the `.pine` drop).
2. **Bulenox `profit_target_pct`=6.0 (corroborated-secondary) / `inactivity`=60 (FXIFY-carried placeholder).** Pass and median-days are contingent on these; operator confirm owed.
3. **Trailing-floor "stops ratcheting at start+$100" not modeled** (NOTES #5) — makes the sim slightly *more* conservative than reality (never more lenient), so gate numbers are marginally pessimistic on this axis (safe direction).
4. **NOT the FXIFY 4-leg anchor.** Different book (2-leg), firm, and DD rule. Do **not** cite the locked 99.83 / 0.17 / 4.37 for this.
5. **40% consistency / payout-cadence not in these numbers.** Median 61–72 days to *pass*; first clean payout is gated later by the 40% rule (~71–92d per `scratchpad/consistency_check_v2.py`). C5 consistency tracker owed.

## Reproduction

```bash
# 1. parse the full-history US30 bars (operator export -> canonical bar CSV)
python scripts/parse_bar_export.py --symbol US30 \
  --in <BAR_EXPORT_...US30_2026-07-03_eb971.csv> \
  --out core/data/bar_data/US30_M15.csv
# 2. drivers (session scratchpad): run_bulenox_gate.py — 3 arms x 5 tiers,
#    1R pinned to PRE_SHOCK_1R, C2-off via rb.DD_SCALE=1.0.
```

## Still owed for lock-grade

- **C5 integer-contract sizing** (needs Pine-verified floors ← Gate B0 ← operator drops the 8 `.pine` files).
- **Proper C2 toggle in the orchestrator** (this run used a monkeypatch; plan Task C4 wants it as a first-class arg).
- **Bulenox primary-source confirm:** target% / inactivity / exact flat time / per-SKU DD mode / trailing-floor stop-at-start+$100.
- **C5 consistency-ratio tracker** (40%-rule payout-eligibility delay distribution).
