# -*- coding: utf-8 -*-
"""Growth-vs-Select comparison over the shape feasibility map (2026-08-24).

Consumes the sharded sweep output and answers the one question the Growth tier
was added to answer: does +16.7% rope headroom ($3,500 vs $3,000) move the
feasible region, and specifically does it move the win-rate FLOOR that
RESULTS.md Sec7.2 identified as the hard constraint?

Read-only. Writes nothing. Dedupes by cell_id (last write wins) because a shard
that was killed and resumed can re-emit its in-flight cell.
"""
import argparse
import collections
import glob
import json
import os

SELECT = "Tradeify_Select_100K"
GROWTH = "Tradeify_Growth_100K"
MFFU = "MFFU_Rapid_100K"
SHAPES = ("symmetric", "mild_right_skew", "bounded_clustered")
WRS = (0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70)


def load(paths):
    rows = {}
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                rows[r["cell_id"]] = r  # last write wins
    return list(rows.values())


def key(r):
    return (r["win_rate"], r["shape"], r["cadence"], r["risk_usd"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="shard_*.jsonl")
    args = ap.parse_args()

    rows = load(sorted(glob.glob(args.glob)))
    by_firm = collections.defaultdict(dict)
    for r in rows:
        by_firm[r["firm"]][key(r)] = r

    sel, gro = by_firm[SELECT], by_firm[GROWTH]
    shared = sorted(set(sel) & set(gro))
    print("cells: Select=%d  Growth=%d  MFFU=%d  |  paired=%d of 315"
          % (len(sel), len(gro), len(by_firm[MFFU]), len(shared)))
    if not shared:
        return

    print("\n" + "=" * 78)
    print("1. VERDICT COUNTS (paired cells only)")
    for label, d in (("Select", sel), ("Growth", gro)):
        c = collections.Counter(d[k]["verdict"] for k in shared)
        print("  %-7s FEASIBLE=%-4d MARGINAL=%-4d INFEASIBLE=%-4d"
              % (label, c["FEASIBLE"], c["MARGINAL"], c["INFEASIBLE"]))

    print("\n" + "=" * 78)
    print("2. VERDICT TRANSITIONS  Select -> Growth")
    trans = collections.Counter((sel[k]["verdict"], gro[k]["verdict"]) for k in shared)
    order = ["FEASIBLE", "MARGINAL", "INFEASIBLE"]
    rank = {v: i for i, v in enumerate(order)}
    improved = degraded = same = 0
    for (a, b), n in sorted(trans.items(), key=lambda kv: -kv[1]):
        arrow = "same" if a == b else ("BETTER" if rank[b] < rank[a] else "WORSE")
        print("  %-11s -> %-11s  %4d   %s" % (a, b, n, arrow))
        if a == b:
            same += n
        elif rank[b] < rank[a]:
            improved += n
        else:
            degraded += n
    print("  ---- improved=%d  unchanged=%d  degraded=%d" % (improved, same, degraded))

    print("\n" + "=" * 78)
    print("3. WIN-RATE FLOOR per shape (lowest win_rate with >=1 FEASIBLE cell)")
    print("   RESULTS.md Sec7.2 baseline: no cell at win_rate <= 50% is FEASIBLE, any firm.")
    for shape in SHAPES:
        line = "  %-18s" % shape
        for label, d in (("Select", sel), ("Growth", gro)):
            floor = None
            for wr in WRS:
                if any(d[k]["verdict"] == "FEASIBLE" for k in shared
                       if k[0] == wr and k[1] == shape):
                    floor = wr
                    break
            line += "  %s floor=%s" % (label, ("%.0f%%" % (floor * 100)) if floor else "none")
        print(line)

    print("\n" + "=" * 78)
    print("4. BUST DELTA (Growth - Select), mean by win_rate  [negative = Growth safer]")
    for wr in WRS:
        ks = [k for k in shared if k[0] == wr]
        if not ks:
            continue
        db = sum(gro[k]["bust"] - sel[k]["bust"] for k in ks) / len(ks)
        sb = sum(sel[k]["bust"] for k in ks) / len(ks)
        gb = sum(gro[k]["bust"] for k in ks) / len(ks)
        print("  wr=%.0f%%  n=%-3d  Select bust=%.4f  Growth bust=%.4f  delta=%+.4f"
              % (wr * 100, len(ks), sb, gb, db))

    print("\n" + "=" * 78)
    print("5. CELLS THAT FLIP TO FEASIBLE UNDER GROWTH (the actionable set)")
    flips = [k for k in shared
             if gro[k]["verdict"] == "FEASIBLE" and sel[k]["verdict"] != "FEASIBLE"]
    if not flips:
        print("  none")
    for k in sorted(flips):
        s, g = sel[k], gro[k]
        print("  wr=%.0f%% %-18s cd=%d $%d | Select %s bust=%.4f -> Growth %s bust=%.4f"
              % (k[0] * 100, k[1], k[2], k[3], s["verdict"], s["bust"],
                 g["verdict"], g["bust"]))

    print("\n" + "=" * 78)
    print("6. MEDIAN DAYS-TO-PASS, FEASIBLE cells only (Growth min_trading_days=1 vs Select 3)")
    for label, d in (("Select", sel), ("Growth", gro)):
        vals = [d[k]["median_days_to_pass"] for k in shared
                if d[k]["verdict"] == "FEASIBLE" and d[k]["median_days_to_pass"]]
        if vals:
            vals.sort()
            print("  %-7s n=%-4d median-of-medians=%.0f days  min=%.0f  max=%.0f"
                  % (label, len(vals), vals[len(vals) // 2], vals[0], vals[-1]))
        else:
            print("  %-7s no FEASIBLE cells yet" % label)

    print("\n" + "=" * 78)
    print("7. SANITY: Select cells reproduce the committed sweep byte-for-byte?")
    committed = {}
    cp = os.path.join(os.path.dirname(args.glob) or ".", "region_data.jsonl")
    if os.path.exists(cp):
        for r in load([cp]):
            if r["firm"] == SELECT:
                committed[key(r)] = r
        diffs = [k for k in shared if k in committed
                 and abs(committed[k]["bust"] - sel[k]["bust"]) > 1e-12]
        print("  compared=%d  bust mismatches=%d %s"
              % (len(set(shared) & set(committed)), len(diffs),
                 "(OK - Select untouched)" if not diffs else "(!! INVESTIGATE)"))
    else:
        print("  region_data.jsonl not found; skipped")


if __name__ == "__main__":
    main()
