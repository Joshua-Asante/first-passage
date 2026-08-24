**Theme:** c1
# R1 — 7-tier intraday-honest re-run (Bulenox / BluSky, W1 pattern extended) — RESULTS

**Status:** `MEASURED` — CLOCK re-run complete on both tiers carrying a published bust/pass figure
(Bulenox_100K, BluSky_Premium_100K); the other 5 tiers carry no published bust/pass figure to
re-run (recorded, not manufactured — see §2).
**Date:** 2026-08-23
**Task:** [`docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md`](../../../../docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md)
Task R1
**Predecessor:** [`Q-FIRMEOD-1` closure `FALSIFIED`](../../../../docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md)
— entry packet (i): the CLOCK evidence + explicit instruction that a successor "re-runs the
intraday-honest fix (`intraday_low`) across all 7 tiers per the W1 ADR pattern and reports whether
any published figure flips."
**Method owner:** [`docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md`](../../../../docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md)
(`Accepted`) — this campaign extends that method's scope from Tradeify/MFFU to Bulenox/BluSky; it
does not re-open or amend the ADR itself.
**Runner / raw:** [`run_r1_bulenox_blusky_intraday.py`](run_r1_bulenox_blusky_intraday.py) ·
[`r1_bulenox_blusky_intraday_report.json`](r1_bulenox_blusky_intraday_report.json)
**Gate (frozen, unedited):** bust ≤ 3.0% ∧ P(pass) ≥ 50% —
[`2026-07-13 survivor-scoring prereg`](../../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
**Cost:** $0 / K=0 — reused committed engine fixtures + gitignored vendor CSVs already present
locally (byte-verified against the tracked `SHA256SUMS` manifests before use; none re-fetched or
re-purchased).

---

## §0 — Rule 0 reads (this session)

- `core/firm_rules.py` — `grep -n '"dd_type": "trailing"'` re-run this session: **122, 134, 146,
  158, 170, 538, 554** (7 hits — Bulenox_25K/50K/100K/150K/250K + BluSky_Premium_50K/100K). The
  Q-FIRMEOD-1 closure's own pin (92,104,116,128,140,508,524) has **shifted by a constant +30**
  since it was recorded — confirmed stale-but-consistent (same 7 tiers, same relative order), not
  a changed tier set.
- `core/mc/simulation.py` (`simulate_path`, full function) — the `equity_test = min(equity_new,
  equity + intraday_low[day]*scale)` construction (L131-134) and the `dd_type=="trailing"` branch
  (L141-151).
- `core/mc/preflight.py` (`firm_kwargs`, full function) — confirms `dd_type="trailing"` never
  threads `dd_lock_offset_usd` (only `"trailing_locking"` does, L172-180), so Bulenox/BluSky need
  no lock-unreachable patch.
- `lab/discovery/prop_survivor_scoring.py` (full file) — `run_tier_remc`, `firm_kwargs`-based,
  confirmed tier-agnostic (no Tradeify/MFFU special-casing); `load_scoring_thresholds`,
  `paired_blocks_from_daily`, `assert_intraday_channel_nonvacuous`.
- `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_w1_intraday_both_halves.py` (full
  file) + its `RESULTS_INTRADAY_W1.md` — the template this campaign extends. **Defect found**:
  its own `sys.path` setup points at `class_s_candidate1_scoring_2026-07-15/` for
  `run_class_s_c1_scoring.py`, which the Great Prune (commit `283d1de`, 2026-08-08) removed from
  that directory — the module now lives only in `geofit_iid_sufficiency_power_2026-08-15/`
  (vendored copy, byte-identical per that probe's own README). Confirmed empirically:
  `python -c "import run_w1_intraday_both_halves"` raises `ModuleNotFoundError` today with the
  path as originally written. Not repaired in the frozen script (Trap #12); this campaign's own
  runner points at the live location instead (see its docstring).
- `tests/core/test_mc_intraday_barrier.py` (full file) — `9 passed`; reproduced verbatim.
- `docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md`, `docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md`
  (R2, already landed this session at commit `65dc17b` before this task started — the Bulenox
  Master-lock does **not** reach the modeled horizon, so no `dd_lock_offset_usd`-shaped patch is
  needed for either Bulenox or BluSky in this campaign).
- Candidate published-figure sources read in full: `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md`,
  `lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md`,
  `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md`,
  `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_corrected_haircut_fullpanel.py`,
  `lab/archive/class_s_candidate2_scoring_2026-07-15/RESULTS.md`, `lab/archive/q_compose_1_2026-07/RESULTS.md`,
  `lab/analysis/c1/band_quantization_2026-08-02/RESULTS.md`,
  `lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md`,
  `lab/analysis/c1/venuegeo_dp3_bustceiling_2026-08-05/RESULTS.md`,
  `lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md` (§5 — confirms that campaign carries
  **zero** Bulenox/BluSky scoring calls, structurally blocked pending this repair),
  `docs/briefs/pre-registration/2026-08-02-sub100k-realizable-book-scoring-prereg.md` (`SIGNED /
  FROZEN`, never executed — no RESULTS/closure exists anywhere in the tree).

---

## §1 — CLOCK sanity check (reproduced before the full run, per task brief)

`pytest tests/core/test_mc_intraday_barrier.py -q` → `9 passed`.

Reproduced the closure's own Bulenox_100K diff **independently**, against the real
`firm_kwargs('Bulenox_100K')` output (not the test's hand-built fixture):

```
firm_kwargs(Bulenox_100K) = {'starting_equity': 100000.0, 'daily_loss_pct': None,
  'profit_target': 106000.0, 'min_trading_days': 0, 'inactivity_limit': 1501,
  'consistency_frac': None, 'dd_type': 'trailing', 'trailing_dd_pct': -0.03}
no-intraday: ('horizon_cap', 1, 0.001, None)
intraday:    ('bust_trailing', 1, 0.001, 0)
```

Byte-identical flip to the closure's §1 citation, confirmed on production `firm_kwargs`, not a
test fixture.

**BluSky, run through the same direct diff (not assumed clean by analogy or by its own "EOD
trailing drawdown" language, per the task brief's explicit instruction):** all 7 `dd_type="trailing"`
tiers' real `firm_kwargs()` output was diffed directly against a common-shape excursion
(1.5× each tier's own dollar trail width, closing back to a small loss):

| Tier | Trail width ($) | No-intraday | Intraday (excursion) | Flips |
|---|---:|---|---|:---:|
| Bulenox_25K | $1,500 | `horizon_cap` | `bust_trailing` (−$2,250) | YES |
| Bulenox_50K | $2,500 | `horizon_cap` | `bust_trailing` (−$3,750) | YES |
| Bulenox_100K | $3,000 | `horizon_cap` | `bust_trailing` (−$4,500) | YES |
| Bulenox_150K | $4,500 | `horizon_cap` | `bust_trailing` (−$6,750) | YES |
| Bulenox_250K | $5,500 | `horizon_cap` | `bust_trailing` (−$8,250) | YES |
| BluSky_Premium_50K | $2,000 | `horizon_cap` | `bust_trailing` (−$3,000) | YES |
| BluSky_Premium_100K | $3,000 | `horizon_cap` | `bust_trailing` (−$4,500) | YES |

All 7 tiers flip under direct `simulate_path` diff on their own real `firm_kwargs()` — the CLOCK
defect is structural (engine-generic across every `dd_type="trailing"` branch), not a Bulenox-only
coincidence, and BluSky's own textual "EOD" framing does **not** exempt it. This block satisfies
the task's explicit "run BluSky through the same direct `simulate_path` diff Bulenox got" —
BluSky's two tiers were diffed directly here, not inferred.

---

## §2 — Per-tier disposition

**Gate (R1):** `RESOLVED` when all 7 tiers carry an honest-clock figure or an explicit
none-to-re-measure line — verdict below.

| Tier | Published bust/pass figure(s) to re-run | Disposition |
|---|---|---|
| **Bulenox_100K** | 1.00×: 3.51%/96.49% ([`class_s_candidate1_scoring_2026-07-15/RESULTS.md`](../class_s_candidate1_scoring_2026-07-15/RESULTS.md), reproduced [`tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../tradeify_eval_lock_correction_2026-07-22/RESULTS.md)) · 0.50× WATCH-1: 0.08%/99.82% ([`CORRECTED_FULLPANEL.md`](../class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md)) | **MEASURED — §3** |
| **BluSky_Premium_100K** | 1.00×: 4.44%/95.54% (same sources) · 0.50× WATCH-1: 0.08%/99.80% (same source) | **MEASURED — §3** |
| Bulenox_25K | none | **none to re-measure** — `band_quantization_2026-08-02/RESULTS.md` is arithmetic/sizing only (own banner: "no MC, no gate scored, no verdict claimed"); the sub-100K realizable-book scoring pre-reg (`docs/briefs/pre-registration/2026-08-02-sub100k-realizable-book-scoring-prereg.md`) is `SIGNED/FROZEN` but was **never executed** — no RESULTS/closure exists anywhere in the tree (verified: `find` + repo-wide grep, zero hits) |
| Bulenox_50K | none | **none to re-measure** — same as Bulenox_25K |
| Bulenox_150K | none | **none to re-measure** — zero repo hits outside `firm_rules.py`/skill docs |
| Bulenox_250K | none | **none to re-measure** — zero repo hits outside `firm_rules.py`/skill docs/2026-07-12 four-firms ADR (config listing only) |
| BluSky_Premium_50K | none | **none to re-measure** — same class as Bulenox_25K/50K (band_quantization sizing-only + un-executed pre-reg) |

**Also considered, disposed by monotonicity rather than re-run (§4):**
`class_s_candidate2_scoring_2026-07-15` (Bulenox_100K 7.38%/92.62% FAIL, BluSky_Premium_100K
8.76%/91.24% FAIL) and `q_compose_1_2026-07` (Bulenox_100K 44.75% FAIL, BluSky_Premium_100K
51.91% FAIL) — both closed/FALSIFIED books, both already deep FAIL (7–52pp over the 3.0%
ceiling) on the EOD clock.

---

## §3 — Honest-clock re-run (Bulenox_100K / BluSky_Premium_100K)

**Method:** identical construction to W1 — `intraday_low` derived from the same MYM/MNQ 15m bars
(`core/data/bar_data/MYM_M15.csv`, `MNQ_M15.csv`) and the same static×1R trade panel
(`Striker_DJ30_v4.5_MYM…15d8b.csv`, `Striker_NAS100_v1…beabf.csv`), reused verbatim via
`W1.build_book_intraday_low` (imported as a library, not re-derived — see §0 defect note).
Thresholds/seeds/sims/horizon from `load_scoring_thresholds()` reading the same frozen
2026-07-13 pre-reg W1 read: seeds 42/123/2026, 10,000 sims/seed, horizon 1500. Both tiers are
`dd_type="trailing"`, so no `dd_lock_offset_usd` patch applies (that kwarg is
`trailing_locking`-only). Bulenox_100K has no `consistency_rule_pct` (Run-1/degenerate, matching
its published figure's own `gated_on: "run1_degenerate"`); BluSky_Premium_100K's is 34.0%
(Run-2), matching its own `gated_on: "run2"`.

**Non-vacuity guard, per target tier** (not inherited from Tradeify's W1 proof — each tier's own
`dd_type="trailing"` %-of-peak branch was independently checked to prove the channel is
load-bearing for it specifically; horizon 400, 200 sims/seed, 1.00× book):

| Tier | EOD bust | Real (intraday) bust | Zeros-arm reproduces EOD? |
|---|---:|---:|:---:|
| Bulenox_100K | 1.83% | 26.17% | OK (asserted in-script) |
| BluSky_Premium_100K | 2.17% | 30.17% | OK (asserted in-script) |

(Non-vacuity guard runs at horizon=400/200 sims — a short-horizon proxy to keep the guard cheap, not
the production headline; the production headline is §3's main table below.)

**Results — full-panel, both published arms:**

| Tier | Arm | EOD-clock (published) | Honest-clock (this run) | Δ bust (pp) | Verdict flip (PASS→FAIL)? |
|---|---|---:|---:|---:|:---:|
| Bulenox_100K | 1.00× | 3.51% / 96.49% | **26.77% / 73.23%** FAIL | **+23.26pp** | No — already FAIL both clocks |
| Bulenox_100K | 0.50× WATCH-1 | 0.08% / 99.82% | **0.59% / 99.33%** PASS | **+0.51pp** | No — PASS both clocks |
| BluSky_Premium_100K | 1.00× | 4.44% / 95.54% | **32.26% / 67.74%** FAIL | **+27.82pp** | No — already FAIL both clocks |
| BluSky_Premium_100K | 0.50× WATCH-1 | 0.08% / 99.80% | **0.59% / 99.31%** PASS | **+0.51pp** | No — PASS both clocks |

**No verdict flips against the 3.0%/50% floor on either measured tier at either arm.** The
magnitude moves are large regardless — proportionally ~7.4× at 0.50× (0.08%→0.59% on both tiers,
essentially identical honest-clock outcomes for Bulenox and BluSky at this arm) and an order of
magnitude at 1.00× (3.51%→26.77%, 4.44%→32.26%, ~7.6–7.7× worse in absolute percentage points).
Both tiers' `dd_type="trailing"` %-of-peak trail (F2 caveat) interacts with the intraday barrier far
more severely than Tradeify/MFFU's fixed-$ `trailing_locking` trail did under the identical fix
(W1's own 0.50× delta was +0.61pp off a 0.11% published base — a ~6.5× proportional move, in the
same order as this campaign's ~7.4×, but off a published base that started at essentially the same
absolute level). This is consistent with — not contradicted by — the pre-existing repo note that
Bulenox's `trailing` branch is "doubly optimistic" (F2 + no venue-native intraday accounting), now
measured rather than asserted. At the WATCH-1 0.50× rung specifically (the only rung with live
decision relevance today, per CLAUDE.md's live-execution posture — no strategy is currently
deployed at either firm), both tiers clear the 3.0% ceiling with **2.41pp of headroom**, not a
knife's-edge PASS.

Raw floats: [`r1_bulenox_blusky_intraday_report.json`](r1_bulenox_blusky_intraday_report.json).

---

## §4 — Monotonicity disposition (candidate #2, Q-COMPOSE-1 — not independently re-run)

`simulate_path`'s intraday barrier check is `equity_test = min(equity_new, equity +
intraday_low[day]*scale)` (`core/mc/simulation.py:131-134`) — literally a `min()` against the
close-only value, so `equity_test <= equity_new` on every day, for every path, whenever
`intraday_low` is populated. The trailing-bust condition `(equity_test - peak)/peak <=
trailing_dd_pct` (or the `trailing_locking` equivalent) can therefore only become *easier* to
trigger as `equity_test` falls, never harder. Since `simulate_path` returns at the first day a
bust condition fires, any path that busts on the EOD-only clock busts on the honest clock too (same
day or earlier) — so, on the **same seeds/blocks**, `bust_rate(honest) >= bust_rate(EOD)` and
`pass_rate(honest) <= pass_rate(EOD)` always. This is a property of the engine code, not an
assumption about the data.

`class_s_candidate2_scoring_2026-07-15` (Bulenox_100K 7.38%, BluSky_Premium_100K 8.76%) and
`q_compose_1_2026-07` (Bulenox_100K 44.75%, BluSky_Premium_100K 51.91%) are both **already FAIL**
on the EOD clock, by 4.4–49pp over the 3.0% ceiling. By the monotonicity property above, their
honest-clock bust rate is provably `>=` those EOD figures — the verdict cannot flip FAIL→PASS, and
no re-run changes that disposition. Both candidates are closed (FALSIFIED); re-running them would
spend K to reconfirm an engine-forced conclusion, which this campaign declines to do. This is
recorded explicitly rather than silently skipped, per the task's own "record 'none to re-measure'
rather than manufacturing" instruction extended to the FAIL-side case: there is nothing to
manufacture here because the direction is already forced.

---

## §5 — What this does NOT license

- Does not edit `dd_type`, `trailing_dd_pct`, or any `firm_rules.py` numeric field — the forbidden
  move both the parent plan and the Q-FIRMEOD-1 closure name explicitly.
- Does not resolve the Bulenox lock-scope question — already resolved separately by R2
  ([`docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md`](../../../../docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md)),
  landed before this task started; this campaign only carries CLOCK.
- Does not touch the F2 fixed-$-vs-%-of-peak faithfulness caveat — `dd_type="trailing"` still
  models Bulenox/BluSky's real fixed-$ trail as a %-of-peak trail that **widens** as the peak
  rises, which is a **separate, still-open** optimism source layered underneath the CLOCK fix this
  campaign makes. The honest-clock figures below are still labeled `optimistic-lower-bound` for
  that reason — CLOCK-honest is not the same claim as F2-faithful.
- Does not re-litigate the LOCK-defect (`dd_lock_offset_usd`) correction chain — that is a
  Tradeify/MFFU-only, already-closed issue (W1 ADR §2), orthogonal to this campaign.
- Does not license citing any Bulenox/BluSky bust-rate figure in a cross-firm capital-allocation
  comparison beyond what is reported here — Task R3 (survivor §4 scoring) is a separate,
  downstream task this campaign does not perform.
- Does not open or amend the W1 ADR, the survivor-scoring pre-reg, or any frozen threshold.

---

## §6 — Reproduction

```bash
python -m pytest tests/core/test_mc_intraday_barrier.py -q
# Expected: 9 passed

python lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/run_r1_bulenox_blusky_intraday.py
# Requires gitignored vendor CSVs present locally (core/data/bar_data/{MYM,MNQ}_M15.csv,
# core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM…15d8b.csv,
# core/data/tv_exports/cme/Striker_NAS100_v1…beabf.csv — sha256-pinned in
# lab/analysis/c1/geofit_iid_sufficiency_power_2026-08-15/run_class_s_c1_scoring.py PANEL_FILES).
# ~24 min wall on this machine (4 x 10k-sim x 3-seed runs at horizon 1500 + 2 non-vacuity
# guards at horizon 400; per-call: Bulenox 1.00x 235s, BluSky 1.00x 302s, Bulenox 0.50x 386s,
# BluSky 0.50x 348s -- consistency-gated (Run-2) tiers/arms run longer on average since a
# profit-target hit that fails the consistency check does not exit early).

grep -n '"dd_type": "trailing"' core/firm_rules.py
# Expected: 122, 134, 146, 158, 170, 538, 554 (re-confirm before citing — these shift when
# firm_rules.py grows above the Bulenox block, as they already have once since Q-FIRMEOD-1)
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Initial. CLOCK sanity reproduced (test + independent firm_kwargs diff, all 7 tiers incl. both BluSky tiers directly diffed); honest-clock re-run for the two tiers carrying a published figure; monotonicity disposition for the two FALSIFIED candidates; 5 tiers recorded none-to-re-measure. | Claude Code (Sonnet 5) |
