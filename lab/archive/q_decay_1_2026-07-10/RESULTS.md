# Q-DECAY-1 — earliest decay detector vs. realized drawdown (RESULTS)

**Disposition:** CLOSED — SCOPE-SPLIT — Guardian-only coverage; rest UNCOVERED

**Loop:** OUTER (INQHIORI), fast-follow to Q-NEFF-1. **Domain:** data.
**Return:** `DONE_WITH_CONCERNS` (feasibility-limited harness; common-mode fire-order shock-sensitive; H premise not clean — an existing per-leg detector partially falsifies it).
**Verdict:** **SCOPE-SPLIT** — narrow per-leg coverage (Guardian only, dormant), everything else UNCOVERED.
**Analysis only. No detector built; no `core/`/`dd_protection`/`ecr`/`firm_rules` change; no real leg retired.**

---

## §0 — Rule-0 production reads (anchors)

| # | Artifact | Anchor | Role established |
|---|---|---|---|
| 1 | `docs/operational_rules.md` | `6bcb034` | Rule 11 names the **Guardian decay-gate** + an **≥80%-ECR revert** metric, both flagged **dormant/unaccruable** post-CFD-retirement. No live "k-of-N legs" family monitor anywhere. |
| 2 | `ops/live_journal/scripts/ecr_rolling.py` | `a85e340` | ECR = **realized / counterfactual** (a ratio), rolling-6wk, feed=Alchemy, `ECR_GATE_THRESHOLD=0.70`. Portfolio-aggregated + per-strategy. |
| 2 | `ops/live_journal/scripts/journal_review.py` | `2555b9f` | `counterfactual_pnl = sig.pnl` (backtest signal P&L in the **same** window); `ratio = realized/counterfactual`. |
| 2 | `docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md` | `73eeab6` | ECR is **execution-fidelity**; §8: a re-backtest counterfactual "would show ECR ≈ 1 **spuriously**". **PARKED / UNREACHABLE** (no live fills). |
| 3 | `core/dd_protection.py` | `6f5480b` | `DD_TRIGGER=0.015`, `DD_SCALE=0.40`; portfolio DD-from-peak → ×0.40. **De-risk, not retirement.** |
| 4 | `core/firm_rules.py` | `57f491c` | FXIFY `max_dd_pct=5`, `daily_loss_pct=5` — the hard bust line, distinct from dd_protection. |
| 5 | `.claude/skills/trade-csv-reconcile/references/baselines.md` | `881a28d` | Per-leg expectancy bands (WR/PF/1R/N) used to calibrate the synthetic harness. |
| 6 | `core/portfolio_mc.py` | `83e589f` | Joint Mon-anchored week-block bootstrap; `_simulate_path` dd_protection + bust logic (harness substrate). |
| — | `lab/analysis/guardian_decay_gate_2026-06-25/{decay_gate,build_envelope}.py` | `8212ff0` | The **only** live-decay detector: lower-CUSUM on regime-conditional per-trade R; ARMED→WATCH→DECAYED; DP-4 classifier interlock. |
| — | `lab/analysis/guardian_decay_gate_2026-06-25/README.md` | `8ecf7be` | Dormancy **indefinite** (Guardian lost all live venues 2026-06-30). |
| — | `lab/analysis/time_to_pass.py` | `53f59f5` | `--regime-check` = C2→C0 dd_protection revert (a *simulated* MC pass-rate check on the panel, **not** a live PnL decay detector). |

---

## §2.1 — Coverage matrix

For each `{scope} × {detector exists? · cheaper-than-DD? · pre-registered threshold? · PnL-computable alone? · terminal action}`:

| Scope | Detector exists? | Cheaper than DD? | Pre-reg threshold? | PnL-computable alone? | Terminal action | Coverage |
|---|---|---|---|---|---|---|
| **Guardian (per-leg)** | **Yes** — decay-gate CUSUM | Yes (fires on expectancy, not loss) | Yes (h_watch α=0.20, h_decay α=0.01, M=60/20) | **WATCH: yes** · DECAYED: **no** (needs a validated exogenous regime classifier — none exists, DP-4 interlock) | DECAYED→retire (verdict only; interlocked off) | **COVERED-in-principle but DORMANT** (no live venue) + terminal verdict interlocked |
| **Striker DJ30 (per-leg)** | No | — | — | — | dd_protection de-risk only | **UNCOVERED** |
| **Striker NAS100 (per-leg)** | No | — | — | — | dd_protection de-risk only | **UNCOVERED** |
| **Aegis (per-leg)** | No | — | — | — | dd_protection de-risk only | **UNCOVERED** |
| **Family / common-mode** | **No** (no k-of-N breadth / aggregate-expectancy monitor) | — | — | — | dd_protection de-risk only | **UNCOVERED** |

Notes:
- **ECR is not a decay detector.** It is a ratio of realized to counterfactual P&L over the *same* window; it divides out edge magnitude, so faithful execution of a decaying edge keeps ECR ≈ 1 (numerator and denominator fall together), and total edge death sends the denominator ≤ 0 → **NOT-SCORED**, never `BREACH`. It measures the *execution* gap and requires live DXTrade fills, which **no longer accrue** (manual trading retired). It is the portfolio-aggregate closest to a "family monitor" but is blind to edge decay by construction → does **not** trigger the §0.5-A hard stop.
- **Only production response to decay is dd_protection de-risk (×0.40).** No discrete strategy-retirement action exists in production (parent brief §0.4: "NO symmetric live-strategy retirement process exists"). A permanently-dead edge would be run at reduced size indefinitely — and for a *single* leg, dd_protection never even engages (below).

## §2.2 — dd_protection baseline (reference "expensive detector")

Portfolio DD-from-peak ≤ **−1.5%** → ×0.40 all sizing; clears at new peak. Same-day equity brake, **not** decay-attributing.

---

## §2.3 — Synthetic fire-order harness

**Feasibility limit (§0.5-B):** locked Pepperstone panels are gitignored & absent in this worktree (Rule 9) → `build_envelope.py` = `NEEDS_DATA`. Harness drives the **real** machinery (`DecayGate`, `calibrate_cusum`, production `DD_TRIGGER`/`DD_SCALE` + the exact `_simulate_path` engage rule) with **synthetic** per-trade R streams calibrated to documented per-leg stats (`E0=(1−WR)(PF−1)` reproduces Guardian +2.14R). Fire-**order** & structure are calibration-robust; absolute sim-weeks are illustrative. Panel-calibrated numbers → run `build_envelope.py` locally.

**Shocks (§0.5-C, stress inputs, not decay estimates):** `step50` (win-mass ×0.50 at onset), `ramp50` (linear 1→0.50 over 40wk), `kill` (win-mass ×0.06 → Guardian E0 +2.14R → ≈−0.5R; genuine edge death). Onset week 100/228.

dd_protection engagement uses the production constants + the engage rule **byte-identical (inline reimplementation) to `_simulate_path`** (`round(dd_from_peak,6) <= -DD_TRIGGER → ×DD_SCALE`); the harness does not import `portfolio_mc`.

**Primary run (seed 42, 600 paths). Seed-robust: control false-WATCH = 14 / 18 / 18% and the per-leg step-lift = +62 / +57 / +59 across seeds 42 / 11 / 7 (after the C1 calibration fix — reference `k` set from a large synthetic reference so it doesn't track a single 203-draw). Real gate self-test passes: in-sample false-DECAYED 0.010 ≈ α_decay; DP-4 interlock holds (0 DECAYED unvalidated).**

| Scope | Shock | CUSUM→WATCH fired (lift vs 14% ctrl) | median wk | DD @ WATCH | dd_prot engaged | dd_prot DD | median max DD |
|---|---|---|---|---|---|---|---|
| control | none | 14% | onset+69 | 0.13% | **40%** | 1.58% | 2.7% |
| per-leg (Guardian) | step50 | 75% (+62) | onset+74 | 0.16% | 48% | 1.60% | 2.7% |
| per-leg (Guardian) | ramp50 | 64% (+51) | onset+87 | 0.18% | 43% | 1.59% | 2.8% |
| per-leg (Guardian) | kill | 98% (+84) | onset+44 | 0.18% | 63% | 1.60% | 2.8% |
| common-mode | step50 | 77% (+63) | onset+74 | 0.59% | 90% | 1.61% | 2.8% |
| common-mode | ramp50 | 61% (+48) | onset+86 | 0.49% | 76% | 1.58% | 2.7% |
| common-mode | kill | 97% (+83) | onset+43 | 4.67% | 100% | 1.69% | **11.73%** |

## §2.4 — Per-scope verdict + drawdown-paid

- **Per-leg Guardian → H FALSIFIED (detector exists), but narrowly.** The CUSUM's fire-rate tracks decay severity (14%→75%→98% control/step/kill) and it fires at **~0.15–0.25% portfolio DD** — an order of magnitude below dd_protection's 1.5%. dd_protection is decay-**blind** here: its engage-rate barely moves (control 40% → step 48% → kill 63%), it never attributes to Guardian, and every engagement is at the same ~1.58% DD *regardless of decay*. So a real, cheaper-than-DD, PnL-computable-at-WATCH, pre-registered detector exists — **but it is Guardian-only, dormant (no live venue), and its terminal DECAYED verdict is classifier-interlocked off.** Drawdown-paid before a *decay-specific* signal via drawdown: effectively ∞ (dd_protection never carries decay information for one leg).
- **Per-leg DJ30 / NAS100 / Aegis → H CONFIRMED.** No detector exists; the only response is dd_protection, which (as control shows) fires on normal variance and never attributes to a leg. Drawdown is the earliest — and non-attributing — signal.
- **Common-mode → H CONFIRMED.** No family-level (k-of-N / aggregate-expectancy) detector exists. Under mild decay the portfolio still grows (median final equity > start); dd_protection's elevated firing is drawdown-on-a-still-profitable-curve, not decay detection. Under genuine common-mode edge death (`kill`), the earliest *portfolio-level* signal (dd_protection at 1.5%) cannot arrest four dead legs — the ×0.40 de-risk still rides the portfolio to a **median max DD of ~11.7%, past the 5% firm bust line**: drawdown "detects" catastrophic common-mode decay only *after the account has already busted*. Even Guardian's single-leg CUSUM is late for the family — it fires only at ~4.7% portfolio DD in the `kill` case (it samples 1/4 of the trades, so the other three dead legs have already dragged the aggregate down before enough decayed Guardian trades accumulate); the other 3/4 have no early signal at all.

**Drawdown-paid-before-detection, by scope:** Guardian per-leg ≈ **0.2%** (CUSUM) vs ∞ (drawdown never decay-signals one leg); other 3 legs per-leg = **no cheaper-than-DD signal**; common-mode = **no cheaper-than-DD family signal** — drawdown-only, and unambiguous only at ≥ bust-line loss.

## Concerns (DONE_WITH_CONCERNS)

1. **Feasibility-limited:** synthetic inputs (panels absent). Real per-leg R distributions / bust envelopes need local `build_envelope.py`. The *ordering* and *structural* results are calibration-robust; absolute sim-week magnitudes are illustrative.
2. **Common-mode fire-order is shock-sensitive:** at `kill` severity, drawdown fires *before* the CUSUM (loss outruns per-trade accumulation) — but this does not flip the coverage verdict (it sharpens it: the earliest family signal is a ruinous drawdown).
3. **H's premise was not clean:** an existing per-leg detector (Guardian) partially falsifies it. Reported per §0.5-A (report-and-continue), not a hard stop (no family monitor found).
4. **C1 (fixed):** the CUSUM reference `k` was initially estimated from a single synthetic 203-trade draw, making the control false-WATCH baseline and the lift magnitudes seed-fragile (22→44%). Fixed by calibrating `k` on a large synthetic reference (`build_envelope()` in the harness); control false-WATCH now 14–18% across seeds 42/11/7 and the lifts are stable. Structural conclusions were unchanged by the fix.

## §5 forbidden moves — honored
No detector built (harness tests adequacy). No `core/`/`dd_protection`/`ecr`/`firm_rules` edit (imported read-only). No `portfolio_mc` re-pin. No real leg retirement (synthetic decay). Decay magnitudes treated as stress inputs. Common-mode uncovered-verdict proved by the harness, **not** by citing Q-NEFF-1 corr≈0.

## Reproduce
```bash
python lab/analysis/q_decay_1_2026-07-10/fire_order_harness.py --paths 1000 --seed 42
# real gate mechanics (audit hook; UTF-8 console on Windows):
PYTHONIOENCODING=utf-8 python lab/analysis/guardian_decay_gate_2026-06-25/decay_gate.py --self-test
```
