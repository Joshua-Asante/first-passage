"""Per-strategy 15m-vs-5m comparison on a matched window. Outputs a markdown
table. Pure functions are unit-tested; main() wires real CSV paths."""
from __future__ import annotations
import argparse
from pathlib import Path

import io_tv
import metrics
import window_match

def compare_one(strategy: str, baseline_csv, proto_csv) -> dict:
    base = io_tv.load_exits(baseline_csv)
    proto = io_tv.load_exits(proto_csv)
    clipped, span = window_match.match(base, proto)
    return {
        "strategy": strategy,
        "span": span,
        "baseline": metrics.compute_metrics(clipped, strategy),
        "proto": metrics.compute_metrics(proto, strategy),
    }

_COLS = [("trades", "{:d}"), ("pf", "{:.3f}"), ("win_rate", "{:.2%}"),
         ("net_usd", "${:,.0f}"), ("max_dd_usd", "${:,.0f}"), ("rf", "{:.2f}"),
         ("r1_usd", "${:,.0f}")]

def _row(label: str, m: dict) -> str:
    cells = [label] + [fmt.format(m[k]) for k, fmt in _COLS]
    return "| " + " | ".join(cells) + " |"

def render_table(results: list[dict]) -> str:
    head = "| Strategy | Trades | PF | WR | Net | MaxDD | RF | 1R |"
    sep = "|" + "---|" * 8
    lines = [head, sep]
    for r in results:
        s, sp = r["strategy"], r["span"]
        lines.append(f"| **{s}** (window {sp['start'].date()}→{sp['end'].date()}, "
                     f"{sp['span_days']}d) | | | | | | | |")
        lines.append(_row(f"{s} · 15m", r["baseline"]))
        lines.append(_row(f"{s} · 5m", r["proto"]))
    return "\n".join(lines)

# strategy -> (15m baseline CSV, 5m proto CSV). Filled at execution time (Task 12).
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline-dir", required=True)
    ap.add_argument("--proto-dir", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    bd, pd_ = Path(args.baseline_dir), Path(args.proto_dir)
    # Concrete filenames resolved in Task 12 once exports exist.
    raise SystemExit("compare.main(): wire the {strategy: (baseline, proto)} map in Task 12")

if __name__ == "__main__":
    main()
