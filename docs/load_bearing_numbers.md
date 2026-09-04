# Load-bearing numbers — the live value, and the one place that owns it

**Read this before quoting any prop-tier figure from this repo.** Two standing rules qualify
*every* published bust/pass number, and six figures have a second, historical value somewhere in
the tree. Each owner named below is the only surface authorized to move its number.

Extracted from [`CLAUDE.md`](../CLAUDE.md) on 2026-09-04 (it landed there 2026-09-03); CLAUDE.md
now carries a pointer block naming the two rules in one line each.
[`operational_rules.md`](operational_rules.md) §7 owns the ownership doctrine, §14 the rule that a
correction lands where the claim is read.

---

## 1. Standing rule — eval bust figures are EOD-clock lower bounds

⚠ **An eval bust figure is an EOD-clock lower bound unless it cites an intraday-honest RESULTS
path.** Scope is all 7 `dd_type="trailing"` tiers — Tradeify/MFFU **and** Bulenox/BluSky, confirmed
CLOCK-affected, not just the Class-S candidate's tiers
([`Q-FIRMEOD-1`](briefs/closures/Q-FIRMEOD-1-closure-falsified.md) `FALSIFIED`;
[W1 ADR](adr/2026-08-07-w1-intraday-honest-engine-remeasure.md) `Accepted` 2026-08-22, with other
decisions of record still pending as measurement).

Honest-clock RESULTS that satisfy the rule:

| Cohort | Path |
|---|---|
| Class-S 0.50× full + halves | [`RESULTS_INTRADAY_W1`](../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md) |
| Bulenox_100K / BluSky_Premium_100K at 1.00× / 0.50× | [`R1 7-tier RESULTS`](../lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md) |

Read that R1 file's §2/§4b before concluding anything about the remaining tiers: the other four
Bulenox tiers carry a since-corrected archived figure from a closed, NO-GO'd, non-live book — that
is **not** the same as "no figure". Only `BluSky_Premium_50K` genuinely carries none.

## 2. Standing rule — every published figure assumes the inactivity barrier is OFF

⚠ **Every published prop-tier bust/pass figure in this repo assumes the inactivity barrier is OFF**
(`firm_kwargs(inactivity_off=True)`) unless its own file says otherwise — the Part A figures, the
A2 feasibility map and the ORB campaign cells included.

That is the intended operational model, not an oversight: the **operator-placed weekly venue-idle
token trade** satisfies the venue rule when the strategy itself has not fired, which makes the
mitigation load-bearing rather than optional.

The barrier-**ON** re-MC has been run twice and is degenerate:

| Study | Result |
|---|---|
| [`c1_cadence_inactivity_2026-08-02`](../lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md) | 92.6–97.6% path death |
| [`orb_mym_v04_riskbudget_2026-09-02`](../lab/analysis/orb/orb_mym_v04_riskbudget_2026-09-02/RESULTS.md) §5c | 74.8–100% pure-inactivity failure across every cell tested, including one at 39.7% trade-day density |

Barrier-ON does not refine the pins; it measures the mitigation's absence. **Do not re-open this as
a fresh finding.**

⚠ **And read barrier-ON figures carefully in both directions.** The engine counts *rolling*
consecutive idle business days (`inactivity_max_idle_days`) while the venue rule is a *weekly
bucket*, so on a complete business-day calendar the engine over-fires and its rates are
conservative ceilings — but on a sparse, trade-days-only input series the idle days are dropped
before the engine sees them and it under-fires instead. Neither direction is safe without a
full-calendar input. The measured demonstration of both, stated where the figures are read, is
`core/mc/preflight.py` (`INACTIVITY_OFF`).

## 3. Two values in the tree — which one is live

The other value is historical. The stale surfaces named below each carry a head banner
(§14); this table is pointer-heavy and number-light by design — **never apply a transformation to a
figure in it.**

| Number | **LIVE value** | Owner (the only authority) | The other value you will find |
|---|---|---|---|
| **Part A eval bust ceiling** | **5.0%** (since 2026-08-26) | [`prereg v2`](briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3 → `prop_survivor_scoring.DEFAULT_PREREG` | **3.0%** = [`prereg v1`](briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md), CLOSED. Still correct-in-context in the [A2 map](../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md) (its verdict labels are keyed to it), the [A2 venue-bound campaign](../lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/RESULTS.md) (its `ln(1/0.03)` bound and every derived figure are v1 results; that study's own banner owns the re-derivation arithmetic and the standing instruction not to quote its magnitudes for current planning without re-deriving at 5.0%), the [withdrawal ADR](adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md), and the v1-pinned loader tests (`test_book_score`, `test_nsurv_channel`, `test_msl_score`, `test_prop_survivor_scoring`). **Do not confuse with `max_dd_pct: 3.0`** — the $100K tier's DD barrier width, a different live 3.0% |
| **Pass floor / funded ceiling / `trailing_locking` rule** | **50% / 1.0% / ≥1 required** | same prereg v2 §3 | unchanged from v1 — no second value |
| **§4 firm set** | **four firms** — Bulenox · Tradeify · MFFU · BluSky | [F1 reversal](adr/2026-08-04-tradeify-venue-descope-eval-included.md#addendum-2026-09-01--f1-reversed-a-tradeify-resting-discharge-now-counts-toward-4) (2026-09-01) | the **three-firm** reading (2026-08-23 → 2026-09-01) survives only in that ADR's own dated addendum, SESSIONS, and archives. **Election only — no code moved:** `AUTOMATION_FRIENDLY_PROP_FIRMS` and both preregs' frozen `$100K×4` tier set always held Tradeify |
| **Venue inactivity rule** | **≥1 trade per Mon–Fri week**, per account, eval **and** funded (art. 10468318; deletion is irreversible, art. 12268494) | [`core/firm_rules.py`](../core/firm_rules.py) `Tradeify_Select_*` sourcing block (`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` §2a is the owner of record, and is **redacted from this public clone**) | **"5 consecutive idle days"** is the *engine's* `inactivity_max_idle_days`, a rolling counter — a conservative **upper bound** on the weekly rule, not the rule (see §2). [`ops/sentinel/activity_week.py`](../ops/sentinel/activity_week.py) is the rule's report-only operational surface; `book_grid.py::weekly_coverage` (`W-FRI`) and `idle_clock_monitor.py::evaluate_week` (breached iff a week has zero active days) also model the bucket faithfully and are reusable |
| **Q-RANGECOND-1 verdict** | **`FALSIFIED`** (2026-08-31) | [`closure-falsified`](briefs/closures/Q-RANGECOND-1-closure-falsified.md) | `RESOLVED` + `+24.75pp` / `66.47%` / `+0.711R` are **retracted** — the [resolved closure](briefs/closures/Q-RANGECOND-1-closure-resolved.md) is frozen historical record behind its own banner, and no longer occupies a STATE decision-index slot |
| **ORB-MYM headline** | the **canonical engine**, not TradingView | [`orb_mym_v04_riskbudget_2026-09-02/RESULTS.md`](../lab/analysis/orb/orb_mym_v04_riskbudget_2026-09-02/RESULTS.md) §2 | TV net/PF/maxDD are **leg-level under pyramiding** and carry no firm DD geometry. P50's $31,947.96 reconciles to the cent yet **busts Select on day 42** at the size it was measured. Third occurrence in this construct family |

---

**Adding a row.** A number earns a row here only when it has **two** values readable in the tree and
a reader landing on the wrong one would act on it. One value with one owner needs no row — that is
ordinary Rule 7, and the owner is enough.
