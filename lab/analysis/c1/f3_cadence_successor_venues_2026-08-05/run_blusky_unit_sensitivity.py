#!/usr/bin/env python3
"""BluSky idle-unit sensitivity — 30 CALENDAR days vs the engine's 30 BUSINESS days.

Follow-up to run_f3_cadence.py, triggered by sourcing BluSky's actual clause
(2026-08-05): Terms of Use section 3.3 "Abandoned Accounts" (under section 3,
Refunds and Billing Policy) binds Evaluation accounts at "inactive for 30
consecutive days ... may be closed at our discretion".

Two faithfulness gaps between that clause and the engine:

  * UNIT (optimistic, the reason this script exists). The engine's barrier is
    30 consecutive idle BUSINESS days = ~6 calendar weeks (~42 calendar days).
    The clause says 30 *days*, unqualified; BluSky's own billing article says
    "30 calendar days" when it means calendar. Under a calendar reading the
    faithful engine threshold is ~21-22 idle bdays, NOT 30 -- i.e. the shipped
    encoding is ~40% too lenient.
  * MODALITY (conservative, not corrected here). The clause is discretionary
    ("may be closed"); the engine barrier is absorbing and certain. Real hazard
    is therefore <= whatever this prices.

Arms: BluSky_Premium_100K x {C2-off, C2-on} x {1.00x, 0.50x} at
inactivity_limit in {21, 22}, against the already-published 30. 21 and 22
bracket "30 calendar days" (4 weeks + 2 days = 20-22 bdays depending on
alignment/holidays); 22 is the value at which 30 calendar days has certainly
elapsed, 21 the tighter end.

Same panel, seeds, and geometry as run_f3_cadence.py. The 30-limit column is
read from that run's committed JSON, not re-simulated.

Run:  python lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/run_blusky_unit_sensitivity.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
for _p in (_ROOT / "core", _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from portfolio_mc import HORIZON_CAP, SEEDS, SIMS_PER_SEED, run_seed  # noqa: E402
from mc.ingest import build_week_blocks  # noqa: E402
from mc.preflight import firm_kwargs  # noqa: E402

PANEL = (
    _ROOT / "lab" / "analysis" / "c1" / "tradeify_book_composition_2026-07-23"
    / "out" / "daily_panel.csv"
)
OUT = _HERE / "out"
STRATS = ("striker_dj30", "striker_nas")
OUTCOMES = (
    "pass", "bust_daily", "bust_static", "bust_trailing",
    "bust_inactivity", "horizon_cap",
)
BUST_KEYS = ("bust_daily", "bust_static", "bust_trailing")

TIER = "BluSky_Premium_100K"
LIMITS = (21, 22)
NO_PROTECTION_TRIGGER = 10.0
DD_TRIGGER = 0.015
DD_SCALE = 0.40


def arm(blocks: np.ndarray, *, c2_on: bool, limit: int) -> dict:
    # allow_unsourced_inactivity: this tier is still flagged unsourced (ADR
    # 2026-08-05). Sourcing the clause did not make the ENGINE ENCODING
    # sourced -- that is precisely what this script measures.
    kw = firm_kwargs(TIER, inactivity_off=False, allow_unsourced_inactivity=True)
    kw["inactivity_limit"] = limit  # explicit override, attested in output
    res = [
        run_seed(
            s, SIMS_PER_SEED, blocks,
            dd_trigger=DD_TRIGGER if c2_on else NO_PROTECTION_TRIGGER,
            dd_scale=DD_SCALE,
            horizon=HORIZON_CAP, strats=STRATS, firm_kwargs=kw,
        )
        for s in SEEDS
    ]
    n = SIMS_PER_SEED
    for r in res:
        assert sum(r["outcomes"][k] for k in OUTCOMES) == n, "bucket-sum violation"
    agg = {k: float(np.mean([r["outcomes"][k] / n for r in res])) for k in OUTCOMES}
    agg["bust_dd"] = sum(agg[k] for k in BUST_KEYS)
    agg["inactivity_limit_used"] = limit
    return agg


def main() -> None:
    OUT.mkdir(exist_ok=True)
    panel = pd.read_csv(PANEL, index_col=0, parse_dates=True)[list(STRATS)]
    print(f"tier   : {TIER}  (idle-unit sensitivity)")
    print(f"panel  : {panel.index.min().date()} -> {panel.index.max().date()}")
    print(f"sims   : {SIMS_PER_SEED:,} x {len(SEEDS)} seeds, horizon {HORIZON_CAP}d")
    print("clause : ToU 3.3 Abandoned Accounts — 'inactive for 30 consecutive days'")
    print("         (discretionary; unit unqualified; billing art. says '30 calendar days')")

    prior = json.loads((OUT / "f3_cadence.json").read_text(encoding="utf-8"))
    base = prior["tiers"][TIER]["arms"]

    rows: dict[str, dict] = {}
    for c2_on in (False, True):
        for scalar in (1.00, 0.50):
            blocks = build_week_blocks(panel * scalar)
            key_base = f"{'c2on' if c2_on else 'c2off'}_{scalar:.2f}x"
            pub = base[f"{key_base}_inactON"]
            print(f"\n--- {key_base} ({len(blocks)} week-blocks) ---")
            print(
                f"  limit 30 bdays (published)  INACT {pub['bust_inactivity']:>7.2%}  "
                f"pass {pub['pass']:>7.2%}"
            )
            for limit in LIMITS:
                a = arm(blocks, c2_on=c2_on, limit=limit)
                rows[f"{key_base}_limit{limit}"] = a
                print(
                    f"  limit {limit} bdays (calendar) INACT "
                    f"{a['bust_inactivity']:>7.2%}  pass {a['pass']:>7.2%}  "
                    f"(INACT {(a['bust_inactivity'] - pub['bust_inactivity']) * 100:+.2f} pp "
                    f"vs published)"
                )

    payload = {
        "tier": TIER,
        "clause": (
            "ToU s3.3 Abandoned Accounts: Evaluation/BluLive/SimFunded/brokerage "
            "accounts inactive for 30 consecutive days may be closed at our discretion"
        ),
        "published_limit_bdays": 30,
        "calendar_equivalent_bdays": list(LIMITS),
        "arms": rows,
    }
    (OUT / "blusky_unit_sensitivity.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print("\nsaved -> out/blusky_unit_sensitivity.json")


if __name__ == "__main__":
    main()
