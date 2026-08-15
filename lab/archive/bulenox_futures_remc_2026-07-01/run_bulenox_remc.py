"""Bulenox futures-prop re-MC orchestrator (2026-07-01).

Runs the 2-strategy prop-hostable subset (DJ30 force-flatted at 17:00 ET +
clean NAS100 — Guardian and Aegis are NOT part of this book; see
lab/analysis/futures_prop_hold_compat_2026-06-30/RESULTS.md) under a chosen
Bulenox account tier's actual rules (trailing DD, no daily loss limit, no
minimum trading days — Option 1, per firm_rules.FIRM_RULES["Bulenox_<tier>"]).

ZERO fork of locked core/portfolio_mc — reuses `load_trades`, `build_daily_panel`,
`build_week_blocks`, `run_seed` directly (same pattern as
lab/analysis/q_ddtrig_1_2026-06-07/bundle_remc.py and
lab/analysis/decompound_remc_2026-06-07/decompound.py).

STATUS (2026-07-01): cannot produce a real number in this environment — the
raw DJ30 Pepperstone export, DJ30's BAR_EXPORT bar file, and the NAS100
export all need to be vendor data this worktree doesn't have (see NOTES.md).
Running this script today fails fast at `_require_inputs()` with a specific
message, not a deep pandas traceback — that is the expected, correct
behavior until the files are dropped in.

Known scope boundary (also in NOTES.md): this models %-of-equity sizing only
(same locked risk% as the FXIFY book). Integer-CME-micro-contract rounding
and per-account contract caps (the pivot's "granularity floors vs contract
caps" open item) are NOT modeled here — a separate, further refinement.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

_CORE = Path(__file__).resolve().parents[3] / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))

from dd_protection import DD_SCALE, DD_TRIGGER  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402
from portfolio_mc import (  # noqa: E402
    ALLOCATIONS,
    BASELINE_BALANCE,
    PEPPERSTONE_PANELS,
    SEEDS,
    SIMS_PER_SEED,
    build_daily_panel,
    build_week_blocks,
    load_trades,
    run_seed,
)

from force_flat_transform import bars_utc_to_et, force_flat_csv  # noqa: E402

_HERE = Path(__file__).resolve().parent
_INPUTS = _HERE / "inputs"

BULENOX_STRATS = ("striker", "striker_nas100")
BULENOX_ALLOC = {s: ALLOCATIONS[s] for s in BULENOX_STRATS}

# Raw DJ30 export is the SAME locked Pepperstone CSV the canonical anchor
# uses (force-flat is applied on top, at load time, below) -- NAS100 needs
# no transform at all (0% of trades open at the 17:00 ET boundary, per the
# 2026-06-30 hold-compat analysis).
RAW_DJ30_CSV = PEPPERSTONE_PANELS["striker"]
NAS100_CSV = PEPPERSTONE_PANELS["striker_nas100"]
# core/bar_export_loader.write_bar_data's canonical naming convention
# (<SYMBOL>_M15.csv); "US30" matches EXPECTED_SYMBOLS_BY_BROKER["pepperstone"]["striker"].
DJ30_BAR_CSV = _CORE / "data" / "bar_data" / "US30_M15.csv"


def _require_inputs() -> None:
    """Fail loudly and specifically -- not a deep pandas traceback -- when
    the vendor files this script needs aren't present in this environment."""
    missing = [p for p in (RAW_DJ30_CSV, DJ30_BAR_CSV, NAS100_CSV) if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Bulenox re-MC needs these vendor files, not present in this "
            "environment:\n" + "\n".join(f"  - {p}" for p in missing) +
            "\nSee lab/analysis/bulenox_futures_remc_2026-07-01/NOTES.md "
            "for what to drop in and where."
        )


def build_bulenox_panel(tier_balance: float,
                         fixed_1r_reference: dict[str, float] | None = None):
    """Force-flat DJ30 + clean NAS100 -> a 2-strategy daily panel rescaled to
    `tier_balance`.

    `build_daily_panel` normalizes 1R to `allocation * BASELINE_BALANCE`
    ($200K) internally -- that's a fixed property of the locked Pine
    strategies' risk-normalization, not of any particular account size.
    Since risk is %-of-equity, a strategy sized to the SAME allocation% on a
    DIFFERENT account produces P&L proportional to that account's size, so
    rescaling the $200K-normalized panel by (tier_balance / BASELINE_BALANCE)
    is the MC-panel-level equivalent of ops/accounts.py's live lot-size
    multiplier -- not an ad-hoc adjustment. `_simulate_path` is told the
    tier's real `starting_equity` separately, so the bust/profit thresholds
    and the P&L scale agree.

    `fixed_1r_reference` should be pinned to the CURRENT canonical DJ30/NAS100
    1R values once known (Q-SWAP-2/M-SWAP-1: letting 1R re-derive from the
    force-flat-modified panel would silently absorb the force-flat truncation
    as a smaller position size instead of letting it show up as bust risk).
    Left adaptive (None) by default here only because this environment has
    no data to compute the canonical 1R from -- fill in before a lock-grade
    run.
    """
    _require_inputs()

    raw_dj30 = pd.read_csv(RAW_DJ30_CSV, encoding="utf-8-sig")
    dj30_bars = bars_utc_to_et(pd.read_csv(DJ30_BAR_CSV))
    forceflat_dj30 = force_flat_csv(raw_dj30, dj30_bars)
    _INPUTS.mkdir(exist_ok=True)
    forceflat_dj30_path = _INPUTS / "dj30_forceflat.csv"
    forceflat_dj30.to_csv(forceflat_dj30_path, index=False)

    trades_by_strat = {
        "striker": load_trades(forceflat_dj30_path, strategy="striker"),
        "striker_nas100": load_trades(NAS100_CSV, strategy="striker_nas100"),
    }
    panel, scale_info = build_daily_panel(
        trades_by_strat, BULENOX_ALLOC, fixed_1r_reference=fixed_1r_reference,
    )
    return panel * (tier_balance / BASELINE_BALANCE), scale_info


def run_bulenox_remc(tier: str = "Bulenox_150K",
                      fixed_1r_reference: dict[str, float] | None = None) -> dict:
    firm = FIRM_RULES[tier]
    tier_balance = float(firm["starting_balance"])
    panel, scale_info = build_bulenox_panel(tier_balance, fixed_1r_reference)
    blocks = build_week_blocks(panel)

    firm_kwargs = {
        "starting_equity": tier_balance,
        "dd_type": firm["dd_type"],
        "trailing_dd_pct": -firm["max_dd_pct"] / 100,
        "daily_loss_pct": (None if firm["daily_loss_pct"] is None
                            else -firm["daily_loss_pct"] / 100),
        "profit_target": tier_balance * (1 + firm["profit_target_pct"] / 100),
        "min_trading_days": firm["min_trading_days"],
        "inactivity_limit": firm["inactivity_max_idle_days"],
    }

    seeds_results = [
        run_seed(seed, SIMS_PER_SEED, blocks, DD_TRIGGER, DD_SCALE,
                 strats=BULENOX_STRATS, firm_kwargs=firm_kwargs)
        for seed in SEEDS
    ]
    per = SIMS_PER_SEED
    outcome_keys = ("pass", "bust_daily", "bust_static", "bust_trailing",
                    "bust_inactivity", "horizon_cap")
    rates = {k: float(np.mean([r["outcomes"][k] / per for r in seeds_results]))
             for k in outcome_keys}
    all_dds = [d for r in seeds_results for d in r["max_dds"]]
    all_days = [d for r in seeds_results for d in r["days_to_pass"]]

    return {
        "tier": tier,
        "tier_balance": tier_balance,
        **rates,
        "bust": rates["bust_daily"] + rates["bust_static"] + rates["bust_trailing"],
        "p99_dd": float(np.percentile(all_dds, 99)) if all_dds else float("nan"),
        "median_days_to_pass": int(np.median(all_days)) if all_days else -1,
        "scale_info": scale_info,
        "n_bdays": len(panel),
        "n_blocks": len(blocks),
    }


def main():
    result = run_bulenox_remc()
    print(f"Bulenox {result['tier']} (${result['tier_balance']:,.0f}) re-MC "
          f"-- DJ30(force-flat 17:00 ET) + NAS100(clean)")
    print(f"  pass {result['pass']:.2%}  bust {result['bust']:.2%}  "
          f"(daily {result['bust_daily']:.2%} / static {result['bust_static']:.2%} / "
          f"trailing {result['bust_trailing']:.2%})")
    print(f"  inactivity {result['bust_inactivity']:.2%}  horizon_cap {result['horizon_cap']:.2%}")
    print(f"  p99 DD {result['p99_dd']:.2%}  median days-to-pass {result['median_days_to_pass']}")
    print(f"  panel: {result['n_bdays']} bdays / {result['n_blocks']} week-blocks")


if __name__ == "__main__":
    main()
