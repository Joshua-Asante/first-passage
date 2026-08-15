"""P2 replay harness — tolerant-pairing K2 diff module (Q-P2-MEASURE-1).

The frozen ``p2_diff_k2.k2_report`` (NOTES.md Sec Freeze declaration) pairs
signals by EXACT ET bar timestamp — a pep-only fire at 11:15 and a cme-only
fire at 11:30 (the same underlying breakout, one bar apart on the other
feed) count as TWO divergences. RESULTS.md's own Observation #1 flagged this
as visible in the scored Phase-B run. Because the exact-timestamp rule is
frozen ("must not be adjusted after real exports arrive to make divergence
counts drop"), correcting it requires a NEW pre-registered instrument, not an
edit — this module, gated by ``docs/briefs/Q-P2-MEASURE-1.md``.

Rule: a pep-only signal and a cme-only signal collapse into ONE "agree"
union member iff (a) they are within ``tolerance_bars`` bars of each other
AND (b) they fire the SAME direction. Direction-flips at an EXACTLY matched
timestamp are untouched -- tolerance reconciles a timing offset between
feeds, it never launders a same-bar direction disagreement into agreement
(brief Sec5 forbidden moves).

Frozen tolerance: ``TOLERANT_BAR_WINDOW = 2`` -- reuses
``p2_diff_k2.ROLL_SEAM_BAR_WINDOW`` (the harness's own existing adjacency
window), not a value fitted to clear any leg. Floating this value after
seeing results is a forbidden move (brief Sec5) -- the scorer takes it as an
explicit argument with this frozen default, never swept.

Invariant (seeded-defect check, ``test_p2_diff_k2_tolerant.py``): at
``tolerance_bars=0`` this reduces EXACTLY to ``p2_diff_k2.k2_report``'s
output on the same inputs, because two DIFFERENT-origin timestamp sets
(pep_only, cme_only are constructed as set differences) can never contain an
equal element, so no candidate ever satisfies ``abs(delta) <= 0``. This
proves the module is a strict generalization of the frozen harness, not a
different instrument.
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
    BAR_INTERVAL,
    NeedsContextError,
    Signal,
    assert_bar_grid,
    extract_signals,
    filter_signals_window,
    first_trade_sanity,
    grid_warnings,
    load_export,
    to_et_boundary,
)
import p2_diff_k2 as base  # noqa: E402 (reuse: classification, scoring, report shape)

#: Q-P2-MEASURE-1 Sec0 frozen tolerance -- the harness's own existing
#: ROLL_SEAM_BAR_WINDOW (==2), NOT a value fitted to clear any leg.
TOLERANT_BAR_WINDOW = base.ROLL_SEAM_BAR_WINDOW


def k2_report_tolerant(
    leg: str,
    signals_pep: list[Signal],
    signals_cme: list[Signal],
    seam_timestamps: list[pd.Timestamp],
    bars_pep: set[pd.Timestamp] | None,
    bars_cme: set[pd.Timestamp] | None,
    tolerance_bars: int = TOLERANT_BAR_WINDOW,
) -> base.K2Report:
    """Same signal-set divergence measure as ``p2_diff_k2.k2_report``, except
    unmatched pep-only/cme-only signals within ``tolerance_bars`` bars of
    each other, firing the SAME direction, collapse into one agreeing union
    member instead of counting as two divergences.

    Cause classification (ROLL-SEAM/SESSION/BASIS/DATA-GAP), scoring
    (``score_k2``), and reporting (``format_report``) are entirely REUSED
    from ``p2_diff_k2`` -- only the pairing step differs.
    """
    base._assert_signal_grid(signals_pep, "pepperstone")
    base._assert_signal_grid(signals_cme, "cme")

    pep = base._signal_map(signals_pep)
    cme = base._signal_map(signals_cme)

    both_ts = sorted(set(pep) & set(cme))
    pep_only = sorted(set(pep) - set(cme))
    cme_only = sorted(set(cme) - set(pep))

    if not (both_ts or pep_only or cme_only):
        raise NeedsContextError(
            "NEEDS_CONTEXT: empty union signal set — check the window pin and "
            "that both exports cover it."
        )

    window = tolerance_bars * BAR_INTERVAL

    # Greedy nearest-neighbor collapse, pep_only walked in time order.
    # Deterministic tie-break: nearest by absolute time delta, then earliest
    # cme_only timestamp. A pep-only signal matches at most one cme-only
    # signal (and vice versa) -- `matched_cme` enforces one-to-one.
    matched_cme: set[pd.Timestamp] = set()
    collapsed_pairs: list[tuple[pd.Timestamp, pd.Timestamp]] = []
    still_pep_only: list[pd.Timestamp] = []
    for p_ts in pep_only:
        candidates = [
            c_ts for c_ts in cme_only
            if c_ts not in matched_cme
            and abs(p_ts - c_ts) <= window
            and pep[p_ts] == cme[c_ts]
        ]
        if candidates:
            best = min(candidates, key=lambda c_ts: (abs(p_ts - c_ts), c_ts))
            matched_cme.add(best)
            collapsed_pairs.append((p_ts, best))
        else:
            still_pep_only.append(p_ts)
    still_cme_only = [c_ts for c_ts in cme_only if c_ts not in matched_cme]

    report = base.K2Report(leg=leg, n_union=0, n_agree=0)

    for ts in both_ts:
        if pep[ts] == cme[ts]:
            report.n_agree += 1
        else:
            cause = base.classify_divergence(ts, seam_timestamps, bars_pep, bars_cme)
            report.divergences.append(
                base.Divergence(ts=ts, kind="direction-flip", cause=cause)
            )

    report.n_agree += len(collapsed_pairs)  # each collapsed pair = 1 agree event

    for ts in still_pep_only:
        cause = base.classify_divergence(ts, seam_timestamps, bars_pep, bars_cme)
        report.divergences.append(base.Divergence(ts=ts, kind="pep-only", cause=cause))
    for ts in still_cme_only:
        cause = base.classify_divergence(ts, seam_timestamps, bars_pep, bars_cme)
        report.divergences.append(base.Divergence(ts=ts, kind="cme-only", cause=cause))

    report.n_union = (
        len(both_ts) + len(collapsed_pairs) + len(still_pep_only) + len(still_cme_only)
    )
    return report


# ---------------------------------------------------------------------------
# CLI — Phase 2 real-data runner (Q-P2-MEASURE-1 Sec7). New script, does not
# touch the frozen run_p2_replay.py.
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--leg", required=True, choices=["dj30", "nas100"])
    ap.add_argument("--pep", required=True)
    ap.add_argument("--cme", required=True)
    ap.add_argument("--window-start", required=True)
    ap.add_argument("--window-end", required=True)
    ap.add_argument("--source-tz", default="America/New_York")
    ap.add_argument("--point-value", type=float, required=True)
    ap.add_argument("--pep-bars")
    ap.add_argument("--cme-bars")
    ap.add_argument("--cme-symbol")
    ap.add_argument("--tolerance-bars", type=int, default=TOLERANT_BAR_WINDOW)
    ap.add_argument("--k2-kill", type=float, help="Frozen K2 kill threshold (percent)")
    ap.add_argument("--k2-treatment", choices=["with-roll", "ex-roll"], default="with-roll")
    args = ap.parse_args(argv)

    try:
        df_pep = load_export(args.pep, source_tz=args.source_tz)
        df_cme = load_export(args.cme, source_tz=args.source_tz)

        first_trade_sanity(df_pep, args.point_value, feed_label="pepperstone")
        first_trade_sanity(df_cme, args.point_value, feed_label="cme")

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
            bars_cme = base.bar_index_et(cme_bars)
            if not args.cme_symbol:
                print("ERROR: --cme-bars requires --cme-symbol", file=sys.stderr)
                return 2
            seams = base.seam_timestamps_from_bars(cme_bars, args.cme_symbol)
        if args.pep_bars:
            bars_pep = base.bar_index_et(pd.read_csv(args.pep_bars))

        # Frozen (exact-timestamp) reference, printed alongside for comparison.
        frozen = base.k2_report(args.leg, sig_pep, sig_cme, seams, bars_pep, bars_cme)
        print("=== FROZEN (exact-timestamp, tolerance=0) reference ===")
        print(base.format_report(frozen))
        print()

        tolerant = k2_report_tolerant(args.leg, sig_pep, sig_cme, seams, bars_pep, bars_cme,
                                      tolerance_bars=args.tolerance_bars)
        print(f"=== TOLERANT (+/-{args.tolerance_bars}-bar, same-direction collapse) ===")
        print(base.format_report(tolerant))

        if args.k2_kill is not None:
            print()
            print(f"Frozen verdict   ({args.k2_treatment}, kill>{args.k2_kill}%): "
                  f"{base.score_k2(frozen, args.k2_kill, args.k2_treatment)}")
            print(f"Tolerant verdict ({args.k2_treatment}, kill>{args.k2_kill}%): "
                  f"{base.score_k2(tolerant, args.k2_kill, args.k2_treatment)}")
    except NeedsContextError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
