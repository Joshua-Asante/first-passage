# PRE-REGISTRATION — External-strategy sourcing §0.5 locks (FROZEN 2026-06-30)

**Status:** FROZEN on the commit that adds this file. Append-only hereafter. These are the
`§0.5` HALT-ON-AMBIGUITY locks of `docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-external-strategy-sourcing.md`.
They are **immovable after the §2.5 corpus freeze** (CC-HANDOFF §5 "Peeking then pruning"). Any change
to §1–§4 below after a candidate's decorrelation or OOS result is inspected VOIDS that candidate's pass
(this is p-hacking at the pre-registration layer — CC-HANDOFF §5 / brief-authoring Known Trap #12).

**Authority:** Joshua (CEO) ratified the four locks 2026-06-30. Q3 (spec params) and Q4 (intake rules)
accepted as-stated; Q1 (regime label) and Q2 (decorrelation statistic) delegated to CC ("make your best
call") and frozen below. PR #251 (the §2.1 machinery) merged to `main` (`8458a90`) — the gate these
locks parameterize EXISTS and was Rule-0 re-confirmed this session (§0).

---

## §0 — Rule 0 reads (production-source verification, 2026-06-30)

The locks below parameterize merged production. Re-confirmed against bytes this session:

| File | Anchor | Confirmed assertion |
|---|---|---|
| [`lab/validation/harness.py`](../../validation/harness.py) | `main` @ `8458a90` (PR #251) | `run_harness_oos` selects IS-best on the **pre-d partition only** (`_filter_pre_d`, line ~442); evaluates edge on post-d (`_filter_post_d`); `INSUFFICIENT_OOS` iff `n_best_post < k_min` (line ~479); `OOS_PASS` iff `derive_verdict(post-d) ∈ _OOS_VALIDATED` (line ~522). The survivorship-leak fix (`cdbc3ce`) is live. |
| [`lab/validation/harness.py`](../../validation/harness.py) | same | `min_pre`/`min_rank` both reuse `pbo_n_splits` (default **16**; `run_candidate.py` passes **6**). Global constraint `k_min ≥ pbo_n_splits`: **k_min=30 clears both 16 and 6** → safe. Rank-comparability needs ≥ pbo_n_splits trades **per config** in BOTH pre-d and post-d windows. |
| [`lab/validation/concept_intake/admissibility_contract.yaml`](../../validation/concept_intake/admissibility_contract.yaml) | same | `side_prediction.returns_independent_markers` (flow, spread, loading, coefficient, regression, correlation, orthogonal, rate differential, …) vs `performance_markers` (profit factor, sharpe, drawdown, win rate). Performance-only falsifier = hard FAIL; the real Lane-B probe is Phase B (this pass). |
| [`core/portfolio_mc.py`](../../../core/portfolio_mc.py) | `main` @ `8458a90` | `build_daily_panel(trades_by_strat, …)` → per-business-day risk-normalized P&L panel (one col/strategy) the MC consumes; `_load_all` returns that `panel`. The **Constellation composite** is the row-sum over the locked four. |
| [`docs/adr/2026-06-07-decompound-remc-hold.md`](../../../docs/adr/2026-06-07-decompound-remc-hold.md) | committed | Canonical chop risk = **2020–2023 (H1)**: trend legs (Guardian gold-trend, Striker DJ30/NAS100 index-momentum) suffer; H2 (2023–2026) benign. Locked four: G 0.34 / DJ30 0.70 (pyr 750) / A 1.50 / N 0.37. |
| [`lab/validation/concept_intake/concepts/CONCEPT-USDCAD-RDM-001.yaml`](../../validation/concept_intake/concepts/CONCEPT-USDCAD-RDM-001.yaml) | committed | Template for the "anti-Constellation leg": mechanism claim + a **conditional-correlation-vs-composite** falsifier ("conditional correlation ≥ 0 → reject") + a confound control. The Q1/Q2 locks generalize exactly this falsifier. |

**Not reusable (closed-null, do NOT adopt as the regime label):**
[`lab/analysis/regime_cond_2026-06-30/`](../../analysis/regime_cond_2026-06-30/) Q-REGIME-COND-1 risk-off
composite — FALSIFIED (composite ≈ repackaged trailing vol on SPY) and **de-coupled from the book** by its
own §7. Its point-in-time / expanding-normalization / block-permutation *machinery* is reused (Q2 below);
its SPY composite is not.

---

## §1 — Lock 1 (Q1): thesis operationalization

The thesis is a **chop / follow-through-deficit, book-decorrelated leg** (the 2026-06-07 decompound HOLD
canonical risk). Two measurables are frozen: a per-day **regime label** and a **decorrelation statistic**.

### §1a — Regime label: efficiency-ratio (follow-through-deficit), per business day `t`, point-in-time

- **Instruments:** the three **trend legs** — `XAUUSD` (Guardian), `DJ30` (Striker DJ30), `NAS100`
  (Striker NAS100). **Aegis/USDJPY is excluded** (mean-reversion leg; including it dilutes the
  trend-efficiency signal).
- **Data:** canonical Pepperstone daily closes `C_I(t)` (resampled from the canonical feed under
  `core/data/`), **point-in-time** — the label at `t` uses only data with timestamp `≤ t`.
- **Window:** `N = 20` trading days (standard ER window; ≈ one trading month; frozen).
- **Per-instrument Kaufman Efficiency Ratio:**
  `ER_I(t) = |C_I(t) − C_I(t−N)| / Σ_{i=t−N+1..t} |C_I(i) − C_I(i−1)|`, `ER_I ∈ [0,1]`
  (1 = pure trend, →0 = pure chop / motion-without-progress = follow-through deficit).
- **Book ER:** `ER_book(t)` = equal-weight mean of `ER_I(t)` over the 3 instruments (all 3 required, else
  `t` is unlabeled).
- **Chop label:** `chop(t) = 1` iff `ER_book(t) < M(t)`, where `M(t)` = **expanding median** of
  `{ER_book(s) : warmup_end ≤ s ≤ t}` (point-in-time; **warmup = 252 trading days**). `t` before
  `warmup_end` is unlabeled. (Expanding median, not a fixed cut → no fitted threshold.)
- **Face-validity sanity gate (NOT a tuning knob):** the share of chop-days in **2020-01-01 → 2023-12-31**
  must **exceed** the share in **2024-01-01 → 2026-06-30** (the decompound HOLD names H1 as the chop
  regime). Violation → the label is **FLAGGED not-face-valid** and reported; it is **not** silently
  retuned (Known Trap #12).

### §1b — Decorrelation statistic: conditional ρ vs the Constellation composite, permutation-gated

- **Constellation composite** `C(t)` = row-sum over the **locked four** of
  `core/portfolio_mc.build_daily_panel` at locked allocations (G 0.34 / DJ30 0.70 / A 1.50 / N 0.37),
  risk-normalized basis.
- **Candidate daily P&L** `X(t)` = the survivor's realized daily P&L on the same business-day index,
  risk-normalized to the same basis, computed on the **post-`discovery_date` window** (Edit 1: pre-d
  carries no evidential weight). A full-series version is reported as a **labeled secondary** only.
- **Evaluation set** = chop-labeled days (§1a) inside the candidate's post-d window with both `C(t)` and
  `X(t)` defined.
- **Statistic:** `ρ_chop` = **Pearson** correlation of `X` and `C` over the evaluation set.
- **Acceptance (pre-registered):** the leg is "decorrelated in the chop regime" iff
  **`ρ_chop ≤ 0` AND `ρ_chop` < 5th-percentile** of a null from a **21-trading-day circular
  block-permutation of the chop-day labels** (B=2000, one-sided). Report point estimate, percentile, and
  a 21-day block-bootstrap 5/50/95 CI.
- **Power floor:** evaluation set `< 30` chop-days → the decorrelation screen is **INSUFFICIENT** (report;
  neither pass nor fail), mirroring `k_min`.

---

## §2 — Lock 2 (Q2 ratified): discovery-date rule

`discovery_date d` = **earliest public-disclosure** date (paper/SSRN, forum post, blog, repo commit). If
multiple plausible dates exist, take the **earliest**. **Undatable → `discovery_date: null` → forward-paper
only** (§6 forward window; no historical pass counts). The rule is confirmed BEFORE any concept is authored
(§2.4). Internal concepts (USDCAD-RDM-001 etc.) are unaffected (`discovery_date` optional, default `None`).

---

## §3 — Lock 3 (Q3 ratified): spec parameters

| Param | Value | Note |
|---|---|---|
| `m` (frozen corpus size) | **≤ 8** (target 4–8) | §2.5 freeze; `assert_family_frozen` enforces post-freeze. |
| `k_min` (min post-d trades for `OOS_PASS`) | **30** | Clears `k_min ≥ pbo_n_splits` at both 16 and 6 (§0). |
| forward-paper window | **≥ 30 trades OR ≥ 60 calendar days**, whichever first | For `INSUFFICIENT_OOS` / `discovery_date: null` routes. |

**Data-length floor (a consequence, not a movable param):** the OOS gate's rank-comparability needs
`≥ pbo_n_splits` trades **per config** in BOTH the pre-d and post-d windows (16 default / 6 in
`run_candidate`). A candidate whose post-d window cannot supply that across ≥2 configs routes to
`INSUFFICIENT_OOS` → forward-paper (neither pass nor fail).

---

## §4 — Lock 4 (Q4 ratified): side-prediction returns-independence rule

The mechanism's side-prediction must be checkable **WITHOUT the strategy's own returns**. A "side-prediction"
that reduces to the strategy's own P&L/Sharpe/DD → **`CULLED_AT_INTAKE`** (not a borderline ADMIT). Genuinely
ambiguous independence → **ASK Joshua** (do not rationalize). This is the structural defense against
confabulating a mechanism to pass intake (CC-HANDOFF §5, LOAD-BEARING; anchor: the GEX gate died because its
"mechanism" reduced to a realized-vol proxy).

---

## §5 — Forbidden moves (binding on the whole pass)

- Changing any §1 definition (`N=20`, expanding-median, equal-weight-3-instrument, Pearson, 21-day block,
  B=2000, `ρ≤0` sign, 30-chop-day floor) **after** any candidate's decorrelation/OOS result is seen.
- Retuning the §1a face-validity threshold to "make" a label face-valid (FLAG + report instead).
- Crediting pre-`discovery_date` performance as edge evidence (Edit 1).
- Adding/dropping a corpus member after any §2.6 result (`assert_family_frozen`; a grown corpus is a NEW
  pre-registration).
- Treating corpus-FDR as the survivorship antidote (it is SECONDARY to the `t>d` OOS gate — Edit 1).
- ADMITting a concept on a story alone with no returns-independent, probe-checkable side-prediction (§4).
- Silently capping the harvest (§2.2/§2.3 coverage gaps get `log()`-ged).

---

## §6 — Gate (binary)

- **Per-day label** is face-valid iff §1a sanity gate holds; else FLAGGED.
- **A candidate is a chop-decorrelated leg** iff §1b acceptance holds on `≥ 30` chop-days; else
  `INSUFFICIENT` (forward-paper) or FAIL (`ρ_chop > 0` or not permutation-significant).
- **Spec params** are pre-registered here; the §2.5 corpus freeze inherits them; `assert_family_frozen`
  refuses post-freeze membership change.
- **A SAVED candidate** (CC-HANDOFF §2.7) must clear: `OOS_PASS` (post-d, `≥ k_min`) ∧ corpus-FDR (secondary)
  ∧ regime-robustness gate ∧ MC re-anchor (raises challenge-window pass-rate without breaching lock gates)
  ∧ the §1b decorrelation screen. Expected outcome: **low-to-near-zero SAVED** = the pipeline working (§4
  of the CC-HANDOFF), not a failure.

---

## §10 — Audit hooks (runnable)

```bash
# This lock is referenced by the harvest/triage/closure artifacts of the same pass
grep -rn "PREREGISTRATION-0.5-locks" lab/research/external_sourcing_2026-06-30/

# §0 anchors still resolve (the gate these locks parameterize exists)
git log -1 --format='%h %ci' -- lab/validation/harness.py
grep -n "_filter_pre_d\|INSUFFICIENT_OOS\|OOS_PASS\|pbo_n_splits" lab/validation/harness.py | head

# k_min >= pbo_n_splits coupling holds (30 >= 16 and 30 >= 6)
grep -n "pbo_n_splits" lab/validation/harness.py lab/validation/run_candidate.py | head

# Constellation composite is buildable (row-sum of build_daily_panel)
grep -n "def build_daily_panel" core/portfolio_mc.py

# Frozen-since check (peek-then-prune guard on these locks)
git log -1 --format='%h %ci' -- lab/research/external_sourcing_2026-06-30/PREREGISTRATION-0.5-locks.md
```

---

## Verification

```bash
# §0 production-source verification (Rule 0 confirmation)
git log -1 --format='%h %ci' -- lab/validation/harness.py core/portfolio_mc.py
grep -n "side_prediction" lab/validation/concept_intake/admissibility_contract.yaml

# The four locks are internally consistent with the merged gate
grep -n "k_min\|pbo_n_splits" lab/validation/harness.py | head
```
