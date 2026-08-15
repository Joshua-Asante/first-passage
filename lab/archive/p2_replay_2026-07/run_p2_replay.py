#!/usr/bin/env python3
"""P2 replay harness — Phase-B orchestrator (built in Phase A; NOT run on real
data in Phase A — no exports exist yet, the window is unpinned, and the K2/E1
gate values are [RATIFY]-pending).

Runs handoff steps 2.2-2.4 on one leg's paired exports:

  python lab/analysis/p2_replay_2026-07/run_p2_replay.py \
      --leg dj30 --pep <pepperstone_csv> --cme <cme_csv> \
      --window-start <YYYY-MM-DD> --window-end <YYYY-MM-DD> \
      --point-value <per-point USD of 1 unit qty, per feed spec> \
      --pep-bars <bar_panel_csv> --cme-bars <bar_panel_csv> \
      --cme-symbol MYM1!

Scoring is opt-in and double-gated: ``--score`` additionally requires
``--gates-ratified`` plus EXPLICIT ``--k2-kill``, ``--e1-pf-floor`` and
``--e1-net-floor`` values (the ADR's 10% / 0.8x / 0.7x are [RATIFY]-pending;
this tool has no gate defaults).

The window is a required CLI input (handoff §0.5-b) — no dates are hardcoded
anywhere in this pipeline. Misaligned grids exit 3 with a NEEDS_CONTEXT
message (§0.5-d); they are never silently resampled.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from p2_ingest import (  # noqa: E402
    NeedsContextError,
    assert_bar_grid,
    extract_signals,
    filter_signals_window,
    first_trade_sanity,
    grid_warnings,
    load_export,
    to_et_boundary,
)
import p2_diff_k2 as diff  # noqa: E402
import p2_envelope_e1 as env  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--leg", required=True, choices=["dj30", "nas100"])
    ap.add_argument("--pep", required=True, help="Pepperstone TV list-of-trades CSV")
    ap.add_argument("--cme", required=True, help="CME-continuous TV list-of-trades CSV")
    ap.add_argument("--window-start", required=True,
                    help="Pinned window start (ET, inclusive) — Joshua's §0.5-b pin")
    ap.add_argument("--window-end", required=True,
                    help="Pinned window end (ET, exclusive) — Joshua's §0.5-b pin")
    ap.add_argument("--source-tz", default="America/New_York",
                    help="Chart TZ both exports were made with (EXPORT_SPEC: New York)")
    ap.add_argument("--point-value", type=float, required=True,
                    help="USD per point per unit qty (first-trade sanity input)")
    ap.add_argument("--pep-bars", help="Pepperstone 15m bar panel CSV (UTC 'time' col) — classification aid")
    ap.add_argument("--cme-bars", help="CME 15m bar panel CSV (UTC 'time' col) — classification aid + seams")
    ap.add_argument("--cme-symbol", help="CME continuous symbol (MYM1!/MNQ1!) for roll-seam derivation")
    ap.add_argument("--score", action="store_true",
                    help="Score K2/E1 (Phase B, gates ratified only)")
    ap.add_argument("--gates-ratified", action="store_true",
                    help="Operator confirmation that the [RATIFY] gate values are ratified")
    ap.add_argument("--k2-kill", type=float, help="Ratified K2 kill threshold (percent)")
    ap.add_argument("--k2-treatment", choices=["with-roll", "ex-roll"],
                    help="Joshua's §0.5-c roll-treatment call (required with --score)")
    ap.add_argument("--e1-pf-floor", type=float, help="Ratified E1 PF-ratio floor")
    ap.add_argument("--e1-net-floor", type=float, help="Ratified E1 net-ratio floor")
    args = ap.parse_args(argv)

    if args.score:
        missing = [n for n, v in [("--gates-ratified", args.gates_ratified),
                                  ("--k2-kill", args.k2_kill),
                                  ("--k2-treatment", args.k2_treatment),
                                  ("--e1-pf-floor", args.e1_pf_floor),
                                  ("--e1-net-floor", args.e1_net_floor)] if not v]
        if missing:
            print(f"ERROR: --score requires explicit ratified gates; missing: {missing}. "
                  f"The ADR's K2/E1 values are [RATIFY]-pending — no defaults exist.",
                  file=sys.stderr)
            return 2

    try:
        df_pep = load_export(args.pep, source_tz=args.source_tz)
        df_cme = load_export(args.cme, source_tz=args.source_tz)

        # §0.5-e first-trade sanity, both exports, before anything else.
        first_trade_sanity(df_pep, args.point_value, feed_label="pepperstone")
        first_trade_sanity(df_cme, args.point_value, feed_label="cme")

        # §0.5-d grid alignment BEFORE diffing; misalignment is a hard error.
        assert_bar_grid(df_pep, "pepperstone")
        assert_bar_grid(df_cme, "cme")
        for w in grid_warnings(df_pep, "pepperstone") + grid_warnings(df_cme, "cme"):
            print(f"WARNING: {w}")

        start, end = to_et_boundary(args.window_start), to_et_boundary(args.window_end)
        sig_pep = filter_signals_window(extract_signals(df_pep), start, end)
        sig_cme = filter_signals_window(extract_signals(df_cme), start, end)

        seams: list[pd.Timestamp] = []
        bars_pep = bars_cme = None
        if args.cme_bars:
            cme_bars = pd.read_csv(args.cme_bars)
            bars_cme = diff.bar_index_et(cme_bars)
            if not args.cme_symbol:
                print("ERROR: --cme-bars requires --cme-symbol for seam derivation",
                      file=sys.stderr)
                return 2
            seams = diff.seam_timestamps_from_bars(cme_bars, args.cme_symbol)
        if args.pep_bars:
            bars_pep = diff.bar_index_et(pd.read_csv(args.pep_bars))

        report = diff.k2_report(args.leg, sig_pep, sig_cme, seams, bars_pep, bars_cme)
        print(diff.format_report(report))
        print()
        ratios = env.e1_ratios(args.leg, df_pep, df_cme, start, end)
        print(env.format_ratios(ratios))

        if args.score:
            print()
            print(f"K2 verdict ({args.k2_treatment}, kill>{args.k2_kill}%): "
                  f"{diff.score_k2(report, args.k2_kill, args.k2_treatment)}")
            print(f"E1 verdict (PF>={args.e1_pf_floor}x, net>={args.e1_net_floor}x): "
                  f"{env.score_e1(ratios, args.e1_pf_floor, args.e1_net_floor)}")
    except NeedsContextError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
