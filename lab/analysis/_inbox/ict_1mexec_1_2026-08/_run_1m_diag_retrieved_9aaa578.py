"""Q-ICT-MNQ-1 / Part C -- 1M diagnostic discrimination (M1 / M2 / M3).

Frozen by PREREG_1M_DIAG.md (commit is the firewall-lift). Discriminates the three
surviving hypotheses for US500's 0/247 fills:

  M1  raid-conditioned fill rate on MNQ (tests a2: population conditioning)
  M2  arm-delay curve d=0..8, unconditioned + conditioned (tests a1, a1^a2 jointly)
  M3  the Part B probe on ES.v.0 -- full era + the exact 2026-06-24..26 US500 window
      (tests b: index-behavior)

Chain reconstruction is prose+port-anchored ONLY (PREREG-1M.md + _ict_offline):
  * pools from pvLen=2 pivots (`pools_from_pivots`), sweepable only AFTER their
    registration bar t + pvLen (look-ahead-free -- an unconfirmed pivot cannot be
    in the Pine registry);
  * raid = pool sweep on a bar (`detect_raid` semantics, applied per-bar);
  * pairing: SSL raid (old low swept) -> bull FVG; BSL raid -> bear FVG, with
    0 <= i_fvg - i_raid <= raidWin (=8) -- PREREG_1M_DIAG sec 0 declared mapping;
  * fill = FVG mid touched within the 6-bar window starting at arm (bar-level
    semantics identical to the Part B probe).
The DOL/stop geometry filters are OMITTED by declaration (<=~5% trim on US500's
own B4 counts; PREREG_1M_DIAG sec 0). No P&L anywhere. Order-free.

Usage:
  python lab/analysis/ict_mnq_2026-08/run_1m_diag.py <mnq_1m.parquet> [<es_1m.parquet>]
"""
from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ARCHIVE = _HERE.parents[1] / "archive" / "ict_cascade_2026-06-18"
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_ARCHIVE))

import _ict_offline as M  # noqa: E402
import _build_w_export_retrieved as B  # noqa: E402
import _run_1m_probe_retrieved_82575fc as P  # noqa: E402

# ---- FROZEN (PREREG_1M_DIAG sec 1; sources: PREREG-1M.md L35-45 + closure) ----
PV_LEN = 2            # raid-pool swing strength (1M layer's own, NOT the D layer's 3)
RAID_WIN = 8          # raid -> entry window, bars
RETRACE_K = 6         # fill window length
D_GRID = tuple(range(0, 9))   # arm-delay sweep, d = 0..8
# Frozen discrimination bars (PREREG_1M_DIAG sec 2):
EXPLAINS_MAX = 0.012          # (1-p)^247 >= 0.05  ->  p <= 1.21%
REFUTED_MIN = 0.20

US500_WINDOW = (_dt.date(2026, 6, 24), _dt.date(2026, 6, 26))  # inclusive


def read_verdict(rate: float) -> str:
    if np.isnan(rate):
        return "NO-DATA"
    if rate <= EXPLAINS_MAX:
        return "EXPLAINS"
    if rate <= REFUTED_MIN:
        return "CONTRIBUTES-INSUFFICIENT"
    return "REFUTED-AS-EXPLANATION"


def raid_bars(o, h, l, pv_len=PV_LEN):
    """Per-bar raid flags from the archived pool primitives, look-ahead-free.

    Returns (raid_buy_bars, raid_sell_bars): boolean arrays, True on bars where a
    BSL pool (old high) / SSL pool (old low) is swept. A pool is eligible only
    from its registration bar + 1 onward (registration = true pivot bar + pv_len,
    the bar Pine first knows the pivot); each pool sweeps exactly once.

    IMPLEMENTATION NOTE (performance, not semantics). A literal per-bar
    `detect_raid` over the full unswept registry is O(bars x active-pools); on a
    trending 1m series the unswept far side accumulates for years (hundreds of
    thousands of pools), which is a multi-day runtime on 2.5M bars. Because
    `detect_raid`'s per-pool rule is independent of every other pool -- a pool
    sweeps at its FIRST eligible bar with hi >= price (BSL) / lo <= price (SSL),
    inclusive, once -- the per-bar flag is equivalently the OR over pools of
    "this bar is that pool's first crossing." Price heaps compute exactly that
    (each pool is pushed at its eligibility bar and popped exactly once, at its
    first crossing): identical flags, O((bars + pools log pools)).
    `test_heap_raid_bars_matches_archived_detect_raid` pins the equivalence
    against the literal archived-primitive scan on synthetic data.
    """
    import heapq

    n = len(h)
    pools = M.pools_from_pivots(h, l, pv_len)
    eligible_at = {}
    for p in pools:
        eligible_at.setdefault(p["bar"] + pv_len + 1, []).append(p)

    raid_buy = np.zeros(n, bool)
    raid_sell = np.zeros(n, bool)
    bsl_heap = []   # min-heap of BSL prices: swept when high[j] >= min price
    ssl_heap = []   # max-heap (negated) of SSL prices: swept when low[j] <= max price
    for j in range(n):
        for p in eligible_at.get(j, ()):
            if p["buyside"]:
                heapq.heappush(bsl_heap, p["price"])
            else:
                heapq.heappush(ssl_heap, -p["price"])
        while bsl_heap and h[j] >= bsl_heap[0]:
            heapq.heappop(bsl_heap)
            raid_buy[j] = True
        while ssl_heap and l[j] <= -ssl_heap[0]:
            heapq.heappop(ssl_heap)
            raid_sell[j] = True
    return raid_buy, raid_sell


def pair_fvgs_to_raids(fvgs, raid_buy, raid_sell, raid_win=RAID_WIN):
    """Subset of FVGs raid-paired per the declared mapping:
    bull FVG needs an SSL raid (raid_sell) within [i - raid_win, i];
    bear FVG needs a BSL raid (raid_buy) within the same window."""
    sell_idx = np.flatnonzero(raid_sell)
    buy_idx = np.flatnonzero(raid_buy)

    def last_at_or_before(idx_arr, i):
        k = np.searchsorted(idx_arr, i, side="right") - 1
        return idx_arr[k] if k >= 0 else None

    out = []
    for f in fvgs:
        i = f["bar"]
        src = sell_idx if f["bull"] else buy_idx
        r = last_at_or_before(src, i)
        if r is not None and (i - r) <= raid_win:
            out.append(f)
    return out


def delayed_fill_stats(fvgs, high, low, d: int, k: int = RETRACE_K):
    """P(mid touched in (i+d, i+d+k]) -- a limit ARMED d bars after registration.

    Touches BEFORE arm do not fill the order (that retrace is spent); only a touch
    inside the armed window counts. Censors FVGs without a complete window.
    """
    n = len(high)
    hits = 0
    eligible = 0
    for f in fvgs:
        t0 = f["bar"]
        if t0 + d + k >= n:
            continue
        eligible += 1
        mid = (f["top"] + f["bot"]) / 2.0
        for j in range(t0 + d + 1, t0 + d + k + 1):
            touched = (low[j] <= mid) if f["bull"] else (high[j] >= mid)
            if touched:
                hits += 1
                break
    rate = (hits / eligible) if eligible else float("nan")
    return {"d": d, "n": eligible, "hits": hits, "rate": rate}


def _load_instrument(path: Path):
    bars = P.load_parquet_bars(path)
    o = bars["open"].to_numpy()
    h = bars["high"].to_numpy()
    l = bars["low"].to_numpy()
    c = bars["close"].to_numpy()
    atr = M.wilder_atr(h, l, c, P.ATR_LEN)
    dates = np.array(
        [
            _dt.datetime.fromtimestamp(int(e) / 1000, _dt.timezone.utc).date()
            for e in bars["epoch_ms"].to_numpy()
        ]
    )
    roll = np.array([B.in_roll_window(d) for d in dates])
    fvgs = P.build_fvgs(o, h, l, c, atr, roll)
    return o, h, l, c, dates, roll, fvgs


def main(argv) -> int:
    if len(argv) < 2:
        print("usage: run_1m_diag.py <mnq_1m.parquet> [<es_1m.parquet>]")
        return 2
    mnq_path = Path(argv[1])
    es_path = Path(argv[2]) if len(argv) > 2 else None

    print("Q-ICT-MNQ-1 / Part C -- 1M diagnostic discrimination")
    print("PREREG: lab/analysis/ict_mnq_2026-08/PREREG_1M_DIAG.md (frozen pre-run)")
    print(f"FROZEN: pvLen={PV_LEN} raidWin={RAID_WIN} retraceK={RETRACE_K} "
          f"d-grid={list(D_GRID)}  bars: EXPLAINS<={EXPLAINS_MAX:.1%} / "
          f"REFUTED>{REFUTED_MIN:.0%}")
    print("US500 fact under diagnosis: 247 limit orders, 0 fills.\n")

    # ------------------------- MNQ: M1 + M2 ---------------------------------
    o, h, l, c, dates, roll, fvgs = _load_instrument(mnq_path)
    print(f"[MNQ] 1m bars {len(c):,}  displacement FVGs {len(fvgs):,}")

    rb, rs = raid_bars(o, h, l)
    print(f"[MNQ] raid bars: BSL(old-high) {int(rb.sum()):,}  "
          f"SSL(old-low) {int(rs.sum()):,}")
    paired = pair_fvgs_to_raids(fvgs, rb, rs)
    n_bull = sum(1 for f in paired if f["bull"])
    print(f"[MNQ] raid-paired FVGs: {len(paired):,} of {len(fvgs):,} "
          f"({len(paired) / len(fvgs):.1%})  (bull {n_bull:,} / "
          f"bear {len(paired) - n_bull:,})\n")

    m1 = delayed_fill_stats(paired, h, l, 0)
    print("=" * 78)
    print("M1 -- raid-conditioned fill rate, MNQ, d=0   [tests a2]")
    print("=" * 78)
    print(f"  n={m1['n']:,}  hits={m1['hits']:,}  RATE={m1['rate']:.4%}")
    print(f"  READ: {read_verdict(m1['rate'])}")

    print("\n" + "=" * 78)
    print("M2 -- arm-delay curves, MNQ   [tests a1; min-over-d conditioned = joint a1^a2]")
    print("=" * 78)
    print("   d | unconditioned            | raid-conditioned")
    cond_curve = []
    for d in D_GRID:
        u = delayed_fill_stats(fvgs, h, l, d)
        s = delayed_fill_stats(paired, h, l, d)
        cond_curve.append(s)
        print(f"  {d:>2} | rate={u['rate']:.4%} (n={u['n']:,}) | "
              f"rate={s['rate']:.4%} (n={s['n']:,})")
    joint = min(cond_curve, key=lambda x: x["rate"])
    print(f"\n  JOINT CELL (min over d, conditioned): d={joint['d']}  "
          f"rate={joint['rate']:.4%}")
    print(f"  READ: {read_verdict(joint['rate'])}")

    # ------------------------- ES: M3 ---------------------------------------
    print("\n" + "=" * 78)
    print("M3 -- Part B probe on ES.v.0 (d=0, retraceK=6)   [tests b]")
    print("=" * 78)
    if es_path is None or not es_path.exists():
        print("  ES parquet not supplied/present -- M3 PENDING (pull still running?)")
        return 0

    eo, eh, el, ec, edates, eroll, efvgs = _load_instrument(es_path)
    print(f"  [ES] 1m bars {len(ec):,}  displacement FVGs {len(efvgs):,}")

    full = P.retrace_stats(efvgs, eh, el, RETRACE_K)
    print(f"  full era : n={full['n']:,}  rate={full['rate']:.4%}")

    years = np.array([d.year for d in edates])
    print("  per-year :")
    for y in range(2019, 2027):
        sub = [f for f in efvgs if years[f['bar']] == y]
        if not sub:
            continue
        s = P.retrace_stats(sub, eh, el, RETRACE_K)
        print(f"    {y}: n={s['n']:>7,}  rate={s['rate']:.2%}")

    lo_d, hi_d = US500_WINDOW
    win = [f for f in efvgs if lo_d <= edates[f["bar"]] <= hi_d]
    w = P.retrace_stats(win, eh, el, RETRACE_K)
    print(f"  US500 window {lo_d}..{hi_d}: n={w['n']:,}  hits={w['hits']:,}  "
          f"rate={w['rate']:.4%}" if w["n"] else
          f"  US500 window {lo_d}..{hi_d}: n=0 (no eligible FVGs)")
    print(f"  READ (window): {read_verdict(w['rate']) if w['n'] else 'NO-DATA'}"
          f"  (small-n, order-of-magnitude only per PREREG sec 1)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
