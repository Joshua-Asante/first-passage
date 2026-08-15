# Bulenox futures-prop re-MC — status (2026-07-01)

Prep-ahead-of-data session: the vendor Pepperstone CSVs (and bar data) are
completely absent from this environment (confirmed via glob across this
worktree and the main checkout — nothing under `core/data/` except
`SHA256SUMS` manifests). Nothing here can produce a real number until that's
fixed. This session built everything that doesn't need data, so the re-MC
is one command away once it is.

## What's built (all TDD, all green)

- **`core/portfolio_mc.py`** — `_simulate_path` (and `run_seed`/`_run_seeds`)
  gained a new `bust_trailing` outcome + keyword-only firm-rule overrides
  (`starting_equity`, `daily_loss_pct`, `dd_type`, `static_dd_pct`,
  `trailing_dd_pct`, `profit_target`, `min_trading_days`, `inactivity_limit`).
  Every existing call site is byte-identical (defaults reproduce today's
  FXIFY/static behavior exactly) — full suite still 462 passed / 12 skipped
  (all pre-existing vendor-data skips) / 0 failed after the change.
- **`core/firm_rules.py`** — 5 additive `Bulenox_25K`/`_50K`/`_100K`/`_150K`/`_250K`
  entries (Option 1: trailing DD, no daily loss limit, no min trading days).
  `ACTIVE_FIRM` stays `"FXIFY"`.
- **`tests/test_trailing_dd_boundary.py`** — 8 synthetic-path tests for the
  new engine branch (fires/doesn't-fire, ULP-precision boundary, culprit
  attribution, the "static default never touches the new branch" safety
  proof, "busts even while cumulatively profitable" semantic-difference
  proof, `daily_loss_pct=None`, `starting_equity` override).
- **`force_flat_transform.py`** — the DJ30-force-flat-at-17:00-ET transform.
  14 synthetic-fixture tests, including a DST-aware UTC→ET bar-time
  conversion (BAR_EXPORT bars are UTC; trade CSVs are chart-TZ ET — see
  memory `reference_bar_export_epoch_utc` — these two clocks do NOT match
  without this conversion).
- **`run_bulenox_remc.py`** — orchestrator reusing `load_trades`/
  `build_daily_panel`/`build_week_blocks`/`run_seed` directly (zero fork of
  locked core, same pattern as `lab/analysis/q_ddtrig_1_2026-06-07/bundle_remc.py`).
  Fails fast and specifically (`FileNotFoundError` naming the exact missing
  files) rather than a deep pandas traceback — verified.

## What's still owed before this is a real, lock-grade number

1. **Vendor data.** Drop these into this worktree:
   - `core/data/tv_exports/pepperstone/Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-05-24_567e1.csv`
     (the SAME canonical DJ30 export the locked anchor uses — force-flat is
     applied on load, not baked into a separate export)
   - `core/data/tv_exports/pepperstone/Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-24_11605.csv`
     (canonical, unmodified)
   - `core/data/bar_data/US30_M15.csv` (produce via
     `python scripts/parse_bar_export.py --symbol US30` from a BAR EXPORT
     v0.1/v0.2 List-of-Trades CSV, per CLAUDE.md's public-clone posture
     section)
2. **`force_flat_csv`'s raw-CSV column assumptions are unvalidated.** It
   assumes the standard TV List-of-Trades shape (`Trade #`, `Date and time`,
   `Price`, `Net P&L USD`/normalized equivalent) and a strict 1 Entry : 1
   Exit row pairing per Trade # (mirroring `portfolio_mc.load_trades`'s and
   `_count_rollovers`'s existing assumption — if pyramid adds turn out to
   share a Trade # with their parent leg rather than getting their own, this
   raises `ValueError` loudly rather than guessing, but the DJ30 pyramid
   structure needs a real CSV to confirm which is true).
3. **`fixed_1r_reference` is not pinned.** `build_bulenox_panel` defaults to
   adaptive 1R recalibration. Per Q-SWAP-2/M-SWAP-1, this SILENTLY ABSORBS
   the force-flat truncation as a smaller effective position size instead of
   letting it show up as bust risk — pin it to the current canonical
   DJ30/NAS100 1R dollar values (from `docs/mc_anchor_history.md` or a fresh
   `implied_1r` run on the unmodified panel) before trusting any headline
   number this produces.
4. **`profit_target_pct: 6.0`** (all 5 tiers) is corroborated across two
   independent secondary sources plus partial primary confirmation — NOT yet
   triple-confirmed directly from Bulenox's own pricing/account-selection
   page. `inactivity_max_idle_days: 60` is an explicitly-flagged UNCONFIRMED
   placeholder carried from FXIFY (low-stakes: empirically ~0% impact on the
   FXIFY anchor, but not a verified Bulenox rule).
5. **Known, deliberate simplification:** Bulenox's real trailing-DD floor
   stops ratcheting upward once it reaches starting-balance+$100 (becomes
   static beyond that point, per the Master-account help page). Not modeled
   here — omitting it makes the simulation slightly MORE conservative than
   reality (the floor keeps chasing peaks a bit longer than the real rule
   would), never more lenient. Worth adding once a lock-grade number matters.
6. **Not modeled at all (separate, larger piece of work):** integer
   CME-micro-contract sizing and per-account contract caps. This script
   models %-of-equity sizing only (the same locked risk% as the FXIFY book,
   rescaled to the tier's balance). The pivot's "granularity floors vs.
   contract caps" open item ([[project_futures_prop_pivot]]) is a further
   refinement layered on top of this, not covered here.

## How to run once data lands

```bash
# 1. one-time: regenerate the bar file if not already produced
python scripts/parse_bar_export.py --symbol US30

# 2. run the re-MC (defaults to the Bulenox_150K tier)
python lab/analysis/bulenox_futures_remc_2026-07-01/run_bulenox_remc.py
```

To try a different tier, call `run_bulenox_remc(tier="Bulenox_100K")` (or
any of `_25K`/`_50K`/`_100K`/`_150K`/`_250K`) from a Python shell or a small
`__main__` edit — no code changes needed elsewhere.
