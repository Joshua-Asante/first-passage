> **STATUS — CLOSED / SHELVED 2026-06-10. THE PROBE NEVER COMPLETED.**
> The Dukascopy m15 fetch (2016–2026; EURUSD + S&P 500 + EuroStoxx 50) hung on
> closed-hour 503-retry latency before any panel finished, so **no
> `gate_result.json`, no `monthly_frame.csv`, and no DST table / month counts
> were ever produced.** The data-dependent sections below describe the *intended*
> run, not a completed one. What IS real and validated: the EuroStoxx-50
> symbol/factor (`EUSIDXEUR` / 1e3, independently re-confirmed by a 3-month smoke
> fetch) and the `gate.py` falsifier design. In place of the regression, a
> hand-authored Pine (`core/strategies/candidates/custodian-eurusd-v0.1.pine`,
> gitignored) was backtested manually on TradingView and underperformed → concept
> shelved (soft, reversible). **Manual-test rejection, NOT a completed formal
> falsifier.** Closure logged in `docs/rejected_candidates.md`
> (`custodian-family × EURUSD`); see `verdict.md`.

<!-- NOTE: data-dependent numbers (DST table, month counts, gate_result.json,
     monthly_frame.csv) were NEVER produced — the probe hung (see STATUS banner). -->
# Custodian-EURUSD v0.1 — month-end equity-hedging-flow mechanism falsifier

Mechanism probe for **`custodian-eurusd-v0.1`** (month-end equity-hedging
rebalancing flow on EURUSD; the Melvin–Prins equity-hedging channel). Tests
whether the prior-period relative (US−EZ) equity return **positively** predicts
the last-trading-day pre-fix EURUSD return into the London 4 p.m. WM/Reuters
fix. **Mechanism probe ONLY — no strategy/Pine is built and the codification
primitive library is NOT extended** (brief §5). Mirrors the
`lab/analysis/noct_spx/` (Stage-1-FALSIFIED) and `lab/analysis/oil_carry/`
(F1-FALSIFIED) precedents: a cheap `lab/analysis/` falsifier that gates whether
the concept ever earns a codify→sweep→validate pass.

Source brief: `docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-custodian-eurusd-v0.1-mechanism-probe.md`
(claude.ai advisor, 2026-06-09), executed by Claude Code 2026-06-09.

## Pipeline placement (house R&D loop)

1. **Front gate** — `custodian-eurusd-v0.1.yaml` registered in
   `lab/validation/concept_intake/concepts/` and passed the admissibility gate
   (`check_concept.py` → **ADMIT 7/7, 0 WARN, dedup CLEAR**, re-confirmed
   2026-06-09; falsifier sign corrected negative→**positive** at registration).
2. **This probe** — the pre-registered falsifier regression (here).
3. **Loop closure** — if FALSIFIED, the rejection is appended to
   `docs/rejected_candidates.md` via `validation/concept_intake/feedback.py`
   (composite key `custodian-family × EURUSD`); re-running the intake gate then
   returns **DUPLICATE** so the direction cannot regenerate.

## Pre-registered specification (brief §0.5, RATIFIED by Joshua 2026-06-09, frozen pre-data)

- **y (primary):** `close[16:00 London] / open[12:00 London] − 1` on the **last
  trading day** of each month (the London afternoon into the WM/R fix). 16:00
  `Europe/London`, **DST-aware** (15:00 UTC under BST, 16:00 UTC under GMT).
  m15 bars are stamped at bar-open, so the 16:00 fix close = close of the
  **15:45** London bar (the noct `close[05:15]→05:30` convention).
- **x (primary):** concluding month M **local-currency** relative return through
  **T-1** (penultimate trading day):
  `[SPX(T-1)/SPX(prev-month-end) − 1] − [ESTX50(T-1)/ESTX50(prev-month-end) − 1]`,
  the window ending **strictly before** the day-T y-window.
  **"Prior calendar-month" = concluding-month-through-T-1** (confirmed).
- **Causal lag (load-bearing, brief §5 #3):** x's last observation is the T-1
  close (end of day T-1); y's first bar is the day-T 12:00 London open. T-1 < T
  strictly ⇒ no same-day/look-ahead leakage (the noct Monday-bug class). Enforced
  by an `assert (Tm1 < T).all()` in `build_monthly_frame` and witnessed in the
  DST/lag spot-check.
- **Sample window:** 2016-01-01 → 2026-06-09.

## The pre-registered gate (brief §4 — KILL criterion)

**H-CUSTODIAN:** OLS `y ~ const + x` with **HC3**-robust SE yields `β > 0`,
two-sided `p < 0.05`, `n ≥ 90` months.

| Verdict | Trigger |
|---|---|
| **RESOLVED** | `β > 0` ∧ `p < 0.05` ∧ `n ≥ 90` |
| **FALSIFIED** | `p ≥ 0.05` **OR** `β ≤ 0` (a significant **negative** β is FALSIFIED, **not** a pass — load-bearing sign discipline) |
| **AMBIGUOUS-HOLD** | right sign but `0.05 ≤ p < 0.10`, **OR** `n < 90` from data gaps |

**Robustness set (reported, NOT a pass route — brief §5 #1):** y-window
`{15:00→16:00, 08:00→16:00}`; x `{FX-adjusted ESTX50-in-USD, single-leg US-only}`.
The primary spec is the only pass route.

**Stage 2 (ADVISORY ONLY — brief §2.4, must NOT move the kill verdict):** single
monthly sign-following trade into the fix (long EUR if x>0 else short), net of
swept round-trip spread `{0,1,2,3,5}` bps + one once-per-period overnight swap
(EURUSD swap not in the FXIFY table → a flat 0.5 bp/night drag assumed,
direction-independent so it cannot manufacture separation). Informs the
codification go/no-go, NOT the FALSIFIED criterion.

## Data provenance (Dukascopy — the canonical R&D feed)

- **EURUSD** m15 → `core/data/bar_data/EURUSD_M15.csv`, point_factor **1e5**
  (mapped in `core/lib/dukascopy.py`). The y instrument + the trading calendar.
- **USA500IDXUSD** (S&P 500) m15 → `core/data/bar_data/USA500IDXUSD_M15.csv`,
  point_factor **1e3** (verified in the noct precedent vs OANDA + index history).
  The US equity leg (daily closes).
- **EUSIDXEUR** (EuroStoxx 50) m15 → `core/data/bar_data/EUSIDXEUR_M15.csv`,
  point_factor **1e3** — **symbol + factor DISCOVERED and verified empirically**
  in Phase 0 (brief §0.5-1; indices are not in the adapter's factor map). The
  Eurozone equity leg (daily closes).

### EuroStoxx-50 symbol/factor verification (brief §0.5-1; mirrors noct's `USA500IDXUSD=1e3`)

Probed candidates `{EUSIDXEUR, E50EUR, EUSTX50EUR, EU50EUR, DEUIDXEUR,
EUSTX50IDXEUR, STOXX50EEUR}`. Only **`EUSIDXEUR`** resolved to plausible
EuroStoxx-50 levels at **point_factor 1e3** (the others 404'd or, for
`DEUIDXEUR`, returned DAX-magnitude levels — a different index). Cross-check
vs the published EuroStoxx-50 index history (raw integer points ÷ 1e3):

| date | EUSIDXEUR ÷ 1e3 | published EuroStoxx-50 | match |
|---|---|---|---|
| 2016-01-04 | 3176 | ~3150–3200 | ✓ |
| 2016-06-01 | 3035 | ~3000 | ✓ |
| 2018-01-23 | 3677 | ~3650 | ✓ |
| **2020-03-23 (COVID trough)** | **2473** | **~2450** | ✓ (load-bearing) |
| 2022-01-05 | 4391 | ~4300–4400 | ✓ |
| 2024-05-15 | 5078 | ~5050–5080 | ✓ |
| 2026-06 | ~6100 | continuation of the 2024–26 rally | ✓ plausible |

The COVID trough at ~2473 is the load-bearing cross-check a wrong symbol/factor
could not coincidentally reproduce. **Symbol/factor verified, not guessed** —
no `NEEDS_CONTEXT` (brief §0.5-1, forbidden move #5 avoided).

## DST verification (mandatory spot-check) — see `gate_result.json`

<!-- FILLED FROM GATE OUTPUT -->
The fix is **London-clock, DST-aware**: the 15:45→16:00 London fix bar maps to
**15:00 UTC under BST** (summer) and **16:00 UTC under GMT** (winter), and the
UK/US DST-mismatch weeks (mid-March, late-Oct/early-Nov) are handled by the
`Europe/London` tz_convert, not a fixed-UTC offset. Table in §"DST spot-check" of
the run summary / `gate_result.json["dst_spotcheck"]`.

## Reproduce

```bash
python lab/analysis/custodian_eurusd/run_gate.py          # fetch (if missing) + gate
# or step-by-step (targeted last-3-days-per-month fetch; see Deviations #2):
python lab/analysis/custodian_eurusd/fetch_panel.py --symbol EURUSD \
    --point-factor 100000 --out core/data/bar_data/EURUSD_M15.csv \
    --start 2016-01-01 --end 2026-06-09 --workers 8 --days-window 3
python lab/analysis/custodian_eurusd/fetch_panel.py --symbol USA500IDXUSD \
    --point-factor 1000 --out core/data/bar_data/USA500IDXUSD_M15.csv \
    --start 2016-01-01 --end 2026-06-09 --workers 8 --days-window 3
python lab/analysis/custodian_eurusd/fetch_panel.py --symbol EUSIDXEUR \
    --point-factor 1000 --out core/data/bar_data/EUSIDXEUR_M15.csv \
    --start 2016-01-01 --end 2026-06-09 --workers 8 --days-window 3
python lab/analysis/custodian_eurusd/gate.py
```

## Deviations from the brief (all flagged, none silent — noct standard)

| # | Brief said | Reality / decision | Why |
|---|---|---|---|
| 1 | EuroStoxx-50 symbol/factor: discover + verify; top candidate `EUSIDXEUR` | **`EUSIDXEUR` / point_factor 1e3**, verified empirically vs index history (table above). | brief §0.5-1; resolved affirmatively, no NEEDS_CONTEXT |
| 2 | Write full m15 panels to `core/data/bar_data/` | **Targeted `--days-window 3` panels** (only the last 3 calendar days of each month). Dukascopy rate-limited this IP under load (8 workers clean but a full 10.5yr dense m15 pull = ~4–5 h/symbol; 16–48 workers → 24–50% spurious 503s that would become silent data gaps). The targeted panel is a strict subset (same schema/feed/factor) and the gate reads only T, T-1 and the prev-month-end close — so x/y are identical to a dense pull. `fetch_panel.py` retains the dense default mode for a future dense-feed sweep. | environmental rate-limit; efficiency, not a spec change |
| 3 | Regenerate `core/data/bar_data/SHA256SUMS` and stage the delta in the same commit as the panels | Panels are gitignored vendor data and **left UNCOMMITTED** (brief discipline: no commit without Joshua's go). The pre-existing `SHA256SUMS` references six other gitignored CSVs NOT present in this fresh worktree, so a `--regenerate` here would *destroy* those entries. Manifest regeneration is therefore deferred to the commit step (Joshua's call), not run speculatively. See §"Manifest note". | no-commit discipline + avoid clobbering unrelated manifest entries |
| 4 | (swap modeled for Stage 2) | EURUSD swap not in the FXIFY table (`docs/external/fxify_swap_rates_2026-05-25.md` covers XAU/JPY/DJ30/NAS100 only) → a flat **0.5 bp/night** direction-independent drag assumed and reported. Stage 2 is advisory, so this cannot move the verdict. | no in-repo EURUSD swap rate |

## Manifest note (data-integrity gate)

The vendor-data manifest gate (`scripts/check_data_manifests.py`,
`core/data/bar_data/SHA256SUMS`) hashes working-tree CSV bytes. This worktree is
a fresh clone: the manifest lists six gitignored CSVs that are not on disk, so
`--check` already fails here independent of this work. The three probe panels are
left uncommitted; when Joshua commits them, run
`python scripts/check_data_manifests.py --regenerate` **with all canonical bar
CSVs present** so the delta is additive, and stage `SHA256SUMS` in the same
commit (CLAUDE.md vendor-data integrity gate).

## Files

- `fetch_panel.py` — chunked Dukascopy fetch (dense or `--days-window` targeted); relies on the adapter's native closed-hour-503 skip+count (no monkeypatch).
- `gate.py` — the falsifier: London-clock y-window, T/T-1 x legs with the causal lag, HC3 OLS, robustness runs, advisory Stage 2, DST spot-check → `gate_result.json` + `monthly_frame.csv`.
- `run_gate.py` — one-command reproducer (fetch-if-missing + gate).
- `gate_result.json` — full numeric result (written by gate.py).
- `monthly_frame.csv` — the per-month (x, y, T, T-1) audit frame.
- `verdict.md` — the binary verdict + the advisory Stage-2 read (clearly marked).
