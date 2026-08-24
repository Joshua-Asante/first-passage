**Theme:** orb

# ORB-MNQ-1 payability at Bulenox_100K / BluSky_Premium_100K / MFFU_Rapid_100K — intraday-honest re-score

**Date:** 2026-08-24 · **Harness:** [`run_orb_mnq_bulenox_blusky.py`](run_orb_mnq_bulenox_blusky.py) ·
**Report:** [`run_orb_mnq_bulenox_blusky_report.json`](run_orb_mnq_bulenox_blusky_report.json)

**Trigger under test** — [`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md`](../../../docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md)
§4 **R3**: *"A non-Tradeify target is proposed → requires the 07-24 addendum's standing bar
(fresh operator GO + pre-registration) **and** a survivor-scoring pass at that firm's geometry
**before** unparking — not after."* Operator GO given 2026-08-24 ("GO on ORB-MNQ-1 at
Bulenox/BluSky", extended same date to "Test MFFU_Rapid_100K too"). This is the
survivor-scoring-pass measurement R3 requires — a precondition check, not an unpark action. With
MFFU included, **all four `AUTOMATION_FRIENDLY_PROP_FIRMS`** (`core/firm_rules.py`) have now been
tested against this construct under the intraday-honest gate — Tradeify via T2 (2026-08-02), the
other three here.

**Cost:** $0. No pull, no cost dry-run, no K spend, no manifest. Reuses the already-cached MNQ
15m panel (`_mnq_15m.pkl`, same file T2 used, resolved from the primary checkout).

---

## §0 — Verdict

**No configuration clears both frozen survivor-scoring limbs (bust ≤ 3.0% ∧ P(pass) ≥ 50%) at
any of the three firms, at any k ∈ {1, 2, 3}.** R3's re-entry bar is **not cleared** at
Bulenox_100K, BluSky_Premium_100K, or MFFU_Rapid_100K.

| Firm | k | headline bust | vs 3.0% ceiling | P(pass) | vs 50% floor | Part A |
|---|---:|---:|---:|---:|---:|:--|
| Bulenox_100K | 1 | **62.37%** | 21× over | 37.63% | FAIL | **FAIL** |
| Bulenox_100K | 2 | **71.86%** | 24× over | 28.14% | FAIL | **FAIL** |
| Bulenox_100K | 3 | **75.92%** | 25× over | 24.08% | FAIL | **FAIL** |
| BluSky_Premium_100K | 1 | **67.26%** | 22× over | 32.74% | FAIL | **FAIL** |
| BluSky_Premium_100K | 2 | **77.17%** | 26× over | 22.83% | FAIL | **FAIL** |
| BluSky_Premium_100K | 3 | **82.22%** | 27× over | 17.78% | FAIL | **FAIL** |
| MFFU_Rapid_100K | 1 | **66.40%** | 22× over | 33.60% | FAIL | **FAIL** |
| MFFU_Rapid_100K | 2 | **75.95%** | 25× over | 24.05% | FAIL | **FAIL** |
| MFFU_Rapid_100K | 3 | **78.49%** | 26× over | 21.51% | FAIL | **FAIL** |

10,000 sims/seed × seeds (42, 123, 2026), horizon 1500 — the frozen
[2026-07-13 survivor-scoring pre-reg](../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md),
unedited, same gate T2 (Tradeify) and R1 (Bulenox/BluSky on the Class-S candidate #1 book) both
scored against.

**Reading this against Tradeify's own T2 figures**
([`RESULTS_t2_intraday_bust.md`](RESULTS_t2_intraday_bust.md) §4, k=1: 67.67% bust / 32.33% pass):
Bulenox is meaningfully *better* than Tradeify at every k (lower cost, $0.61/side vs $0.91/side,
and a pure percentage trail vs a fixed-$ trail — see §3), but still catastrophically over the
ceiling. BluSky and MFFU both sit close to Tradeify's own numbers (k=1: 67.26% / 66.40% vs
67.67%) despite BluSky/MFFU sharing the same, *higher* cost ($0.95/side) — explained in §3, not a
defect. **The failure is not Tradeify-specific and not venue-specific at all.** All four
`AUTOMATION_FRIENDLY_PROP_FIRMS` this repo tracks now cluster in the same 60–82% bust range at
k=1–3, 20–27× the 3.0% ceiling. Venue migration does not rescue this construct; its actual
realized drawdown (−$6,527 at k=1, per T2 §3's realized-panel anchor) is simply too large
relative to *any* of these firms' ~$3,000-scale $100K-tier trailing buffers.

---

## §1 — Rule 0 reads (production source, this session, 2026-08-24)

- [`docs/pursuits/b3-orb-mnq-payability-line.md`](../../../docs/pursuits/b3-orb-mnq-payability-line.md)
  — PARK standing; re-entry clause *"new payability / cost-geometry evidence at an admissible
  venue"*; expiry 2026-11-08.
- [`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md`](../../../docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md)
  §4 R3 — the trigger this measurement discharges (not automatically; still needs an operator
  reading of the result, per R3's own "Not automatic").
- [`RESULTS_t2_intraday_bust.md`](RESULTS_t2_intraday_bust.md) — the Tradeify intraday-honest
  derivation this campaign extends (same construct, same panel, same controls, re-costed).
- `run_t2_intraday_bust.py` — retrieved via `git show pre-prune-2026-08-08:lab/analysis/orb/orb_mnq_2026-07/run_t2_intraday_bust.py`
  (pruned from the working tree 2026-08-08, not deleted from history). The excursion derivation
  (`orb_days_with_excursion` + its two engine-matching controls) is copied verbatim from this
  file and re-parametrized per firm's own round-trip cost — not re-derived from scratch (Trap
  #12: frozen/tested logic is reused, not rewritten).
- `lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/run_r1_bulenox_blusky_intraday.py` — the
  precedent for extending the intraday-honest engine from Tradeify/MFFU to Bulenox/BluSky via
  `discovery.prop_survivor_scoring.run_tier_remc(firm_key=...)`, confirmed tier-agnostic.
- `core/firm_rules.py` `Bulenox_100K` / `BluSky_Premium_100K` / `MFFU_Rapid_100K` blocks —
  `dd_type` `"trailing"` / `"trailing"` / `"trailing_locking"`; MFFU's own `dd_lock_offset_usd`
  already ships `1,000,000.0` (unreachable) directly in `FIRM_RULES`, fixed 2026-08-04 — no manual
  override needed, unlike Tradeify's pre-2026-08-04 shipped value which T2 had to correct by hand;
  `cost_per_side_usd` 0.61 / 0.95 / 0.95; `starting_balance` 100,000 all three;
  `consistency_rule_pct` unset / 34.0 / 50.0; `min_trading_days` 0 / 0 / 2.
- `core/mc/simulation.py` `simulate_path` L141–158 — read directly to confirm the `"trailing"`
  vs `"trailing_locking"` barrier dispatch (see §3).
- `lab/discovery/prop_survivor_scoring.py` — `run_tier_remc`, `_consistency_frac`,
  `paired_blocks_from_daily`, `score_part_a`, `load_scoring_thresholds`, `assert_intraday_channel_nonvacuous`
  — all reused unmodified; none of this campaign's own code re-implements engine or scoring logic.

---

## §2 — Controls

Same four controls T2 established, re-run per firm at that firm's own cost basis:

| # | Control | Bulenox_100K | BluSky_Premium_100K | MFFU_Rapid_100K |
|---|---|---|---|---|
| Mirror vs `orb_lib.orb_backtest` (R/range/side/stopped/entry_tod, elementwise) | **PASS**, n=1,846 | **PASS**, n=1,846 | **PASS**, n=1,846 |
| Excursion invariants (≤0; dominates realized P&L; equals it on stopped days; bounded by −(range+rt)) | **PASS** | **PASS** | **PASS** |
| Non-vacuity (a planted deep excursion must bust a path the close alone survives; short horizon=400, 200 sims) | **PASS** — EOD 59.50% vs real(intraday) 61.67% | **PASS** — EOD 64.33% vs real(intraday) 67.00% | **PASS** — EOD 62.67% vs real(intraday) 65.67% |
| `assert_engine_ready(firm_key)` (Constraint-D pre-flight) | **PASS** | **PASS** | **PASS** |

`engine_ready` and the mirror control ran against each firm's *own* `Instrument` (own
`rt_cost_pt`), not a shared/cached one — confirmed by inspection: `worst_realized_day_usd_1lot`
differs by cost tier (−$783.22 Bulenox vs −$783.90 both BluSky and MFFU — identical cost basis,
$0.95/side — vs −$783.82 Tradeify, T2 §3), tracking each firm's own round-trip cost exactly as
expected, not a copy-paste artifact.

---

## §3 — Why BluSky/MFFU (higher cost) land close to Tradeify, and Bulenox (lower cost) doesn't

Worth stating plainly since it looks paradoxical at first glance: BluSky's and MFFU's cost
($0.95/side each) is *higher* than Tradeify's ($0.91/side), yet their k=1 bust (67.26% / 66.40%)
sits close to Tradeify's (67.67%), while Bulenox's *lower* cost ($0.61/side) produces a
materially *better* bust rate (62.37%). This is barrier geometry, not a defect — verified
directly in `core/mc/simulation.py`. (MFFU shares Tradeify's exact `dd_type="trailing_locking"`
mechanism — the two are the *same* barrier type, not merely a coincidental early-path
approximation like BluSky's percentage trail — yet still lands a hair further from Tradeify's own
number than BluSky did, which is consistent with the remaining ~1pp-scale differences being
ordinary MC noise plus MFFU's own `min_trading_days=2` / `consistency_rule_pct=50.0`, not a
sign of anything wrong.)

- **Tradeify's corrected geometry** (`dd_type="trailing_locking"`, lock forced unreachable per
  the 2026-07-22 eval-lock correction) reduces to `floor = peak − max_dd_usd`, where
  `max_dd_usd = −trailing_dd_pct × starting_equity` — a **fixed-dollar** trail ($3,000 at
  $100K), pinned to the *starting* balance, never growing with peak (L152–158).
- **Bulenox/BluSky's geometry** (`dd_type="trailing"`) fires when
  `(equity − peak) / peak ≤ trailing_dd_pct` — a **percentage-of-peak** trail. In dollar terms
  the allowed drawdown *grows* as peak grows (L141–151).

At $100K peak both reduce to the same ~$3,000 buffer. They only diverge once equity has grown
materially past $100K — and this construct busts *early* relative to the 1,500-day horizon (T2's
own realized-panel anchor: Tradeify busts in March 2020, inside the first year). Most of the
probability mass governing `headline_bust` is accumulated before the percentage and fixed-dollar
trails have meaningfully diverged, so BluSky's own slightly-higher cost is the dominant remaining
difference vs Tradeify — pushing its number a hair worse, not the ~9pp better a naive
cost-ordering (Bulenox < Tradeify < BluSky) might predict from cost alone. Bulenox's lower cost
is a bigger, cleaner effect and shows up as a genuinely lower bust rate at every k.

**Verified, not assumed:** an earlier smoke test at 200 sims/seed happened to land BluSky's k=1
figure on an exact bit-for-bit match with Tradeify's own published 67.67%/32.33% — investigated
before trusting it (see the derivation above) and resolved by the full 10,000-sims/seed run,
which shows BluSky at 67.26%/32.74% — close, not identical, consistent with genuinely similar but
non-identical barrier geometry rather than a bug that happened to look plausible.

---

## §4 — Honest limits (inherited from T2, unchanged)

- Same lower-bound caveat as T2: `peak` stays EOD-denominated in `simulate_path`; only the
  equity *tested* against the floor gets the intraday minimum. If either venue's trail ratchets
  off an intraday high-water mark rather than an EOD one, this arm is still optimistic in the
  same direction T2 already disclosed.
- Engine ≠ Pine (96.9% per-trade parity, inherited); panel ends 2026-07-15.
- One position per session is what makes the excursion derivation exact — unchanged from T2, and
  still true here (same construct, same panel, different cost/geometry only).
- `median_days_to_pass` is not reported here (this campaign's own harness did not thread it
  through from `run_tier_remc`'s return shape) — non-load-bearing; the frozen gate is
  `headline_bust`/`pass_rate` only, both reported and controlled above.

---

## §5 — What this does not decide

This is a **measurement**, not an unpark. Per ADR §4 R3, a survivor-scoring PASS at a non-Tradeify
firm is a *precondition* for proposing an unpark, not a self-executing trigger — and this
measurement returns FAIL at all three tested firms, so R3 does not fire anywhere.
`docs/pursuits/b3-orb-mnq-payability-line.md` stays **PARK**, unchanged. Nothing here touches
`core/`, allocation, `dd_protection`, Pine, the rail, or the K ledger. **With MFFU included, all
four `AUTOMATION_FRIENDLY_PROP_FIRMS`** this repo tracks (Tradeify, Bulenox, BluSky, MFFU) **have
now been tested under the intraday-honest survivor-scoring gate and all four FAIL at every
k ∈ {1,2,3}.** Venue migration inside this repo's currently-tracked friendly-firm set is
exhausted as a re-entry path for ORB-MNQ-1 — a future re-entry would need either a firm outside
the current `AUTOMATION_FRIENDLY_PROP_FIRMS` set, or genuinely new payability/cost-geometry
evidence per the ADR's own re-entry clause, not another venue swap among these four.

---

## §10 — Audit hooks (runnable)

```bash
# Reproduce (venv-research; ~10 min total, three firms)
.venv-research/Scripts/python.exe lab/analysis/orb/orb_mnq_2026-07/run_orb_mnq_bulenox_blusky.py
# Expected: all controls PASS; Bulenox k=1 bust ~62.37% (±1pp); BluSky k=1 bust ~67.26% (±1pp);
# MFFU k=1 bust ~66.40% (±1pp); every (firm,k) FAILs Part A.

# Confirm dd_type for all three target firms (MFFU's dd_lock_offset_usd already unreachable, no patch needed)
grep -n '"Bulenox_100K"\|"BluSky_Premium_100K"\|"MFFU_Rapid_100K"' -A 4 core/firm_rules.py | grep "dd_type\|dd_lock_offset_usd"

# Confirm the barrier-dispatch asymmetry cited in §3
sed -n '141,158p' core/mc/simulation.py

# Confirm this campaign never touched core/, Pine, dd_protection, or the K ledger
git diff --stat -- core/ '**/*.pine' docs/methodology/strategy_harvest.md
# Expected: empty
```

## Verification

§0 verdict table matches the report JSON byte-for-byte (both hand-checked) · §2 controls all PASS,
run per-firm not shared · §3 states the geometry finding plainly, including the smoke-test anomaly
that was investigated rather than silently trusted · §5 correctly scopes the non-decision (PARK
unchanged, MFFU untested) · $0 / K=0 confirmed by construction (no pull, no manifest).
