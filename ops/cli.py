"""
First Passage historical-analysis CLI.

The continuous-lot account/multiplier surface (add / update / status / lots)
was retired in substrate Phase 2
(docs/adr/2026-07-22-challenge-era-substrate-retirement.md). Live sizing is
the c1 rail (`ops/c1_rail/c1_sizing_host_reference.py`), not this CLI.

Usage:
    python ops/cli.py tearsheet <csv_path> [--out PATH] [--starting-equity N]
"""

import argparse
import sys
from pathlib import Path

# Standalone-run bootstrap: cli.py (ops) imports core/lib. Run as
# `python ops/cli.py …`, the layer roots aren't on sys.path — add them
# (Option B, 2026-06-05 monorepo restructure). No-op under pytest.
_REPO_ROOT = Path(__file__).resolve().parent.parent
for _layer in ("core", "lab", "ops", "governance"):
    _p = str(_REPO_ROOT / _layer)
    if _p not in sys.path:
        sys.path.insert(0, _p)

from lib.validation import require_finite_number


def _positive_finite_float(raw: str) -> float:
    """Argparse type for positive, finite monetary inputs."""
    try:
        return require_finite_number(
            float(raw), field="value", strictly_positive=True
        )
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def cmd_tearsheet(args):
    from lib.tearsheet import from_csv

    out_path = Path(args.out) if args.out else Path(args.csv_path).with_suffix(".tearsheet.html")
    try:
        path = from_csv(
            args.csv_path,
            args.starting_equity,
            out_path,
            title=args.title or "Prop Firm Tearsheet",
        )
        print(f"Tearsheet written: {path}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="First Passage CLI (historical tearsheet only)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_tear = sub.add_parser("tearsheet", help="Generate HTML tearsheet from DXTrade CSV")
    p_tear.add_argument("csv_path", help="Path to DXTrade CSV export")
    p_tear.add_argument(
        "--out",
        default=None,
        help="Output HTML path (default: <csv>.tearsheet.html)",
    )
    p_tear.add_argument(
        "--starting-equity",
        type=_positive_finite_float,
        default=200_000.0,
        help="Starting equity for return-series normalization (default: 200000)",
    )
    p_tear.add_argument("--title", default=None, help="Tearsheet title")
    p_tear.set_defaults(func=cmd_tearsheet)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
