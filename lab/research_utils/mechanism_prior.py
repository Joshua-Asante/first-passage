"""Cross-campaign mechanism prior -- computes and reports univariate
survival rates by mechanism_tier, sourcing_channel_rank, and
target_instrument_family.

See docs/superpowers/specs/2026-08-20-cross-campaign-mechanism-prior-design.md.
Pure arithmetic over lab/research_utils/mechanism_prior_tags.json -- never
calls an LLM, never gates anything. Run on demand:

    python lab/research_utils/mechanism_prior.py
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Direct invocation (`python lab/research_utils/mechanism_prior.py`, per this
# module's own CLI contract) puts this file's directory on sys.path[0], not
# the repo root -- `lab.research_utils....` then fails to import. Bootstrap
# the repo root onto sys.path before those imports. No-op under pytest (repo
# root is already on sys.path via pyproject.toml's pythonpath config).
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lab.research_utils.mechanism_prior_store import DEFAULT_STORE_PATH, load_latest_records  # noqa: E402
from lab.research_utils.wilson_interval import wilson_interval  # noqa: E402

SURVIVED = "SURVIVED"
FIELDS_TO_REPORT = ("mechanism_tier", "sourcing_channel_rank", "target_instrument_family")
FIELD_TITLES = {
    "mechanism_tier": "By mechanism tier",
    "sourcing_channel_rank": "By sourcing channel rank",
    "target_instrument_family": "By target instrument family",
}


def aggregate_by_field(records: list[dict], field: str) -> dict[str, tuple[int, int, float, float]]:
    """Group records by `field`, return {value: (successes, n, lo, hi)}.

    "successes" counts outcome == SURVIVED. A value with n == 0 never
    appears (nothing to divide by). Requires n >= 1 per group -- callers
    must not pass an empty `records` list expecting per-value output.
    """
    counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for record in records:
        value = record[field]
        counts[value][1] += 1
        if record["outcome"] == SURVIVED:
            counts[value][0] += 1

    result = {}
    for value, (successes, n) in counts.items():
        lo, hi = wilson_interval(successes, n)
        result[value] = (successes, n, lo, hi)
    return result


def render_report(records: list[dict], store_path: Path, now: datetime) -> str:
    """Render the full Markdown report for the given records."""
    lines = [
        "# Cross-campaign mechanism prior",
        "",
        f"Generated: {now.isoformat()}",
        f"Tag store: `{store_path}` -- {len(records)} current records "
        "(superseded records excluded from this count; see `supersedes` "
        "chains in the raw file for the full history).",
        "",
        "Every rate below is 95% Wilson-interval bounded, not a bare "
        "percentage. Small cells (single-digit N) are expected in this "
        "corpus by design -- read the interval width, not just the center.",
        "",
    ]
    for field in FIELDS_TO_REPORT:
        table = aggregate_by_field(records, field)
        lines.append(f"## {FIELD_TITLES[field]}")
        lines.append("")
        lines.append("| Value | Survived / N | 95% Wilson interval |")
        lines.append("|---|---|---|")
        for value in sorted(table):
            successes, n, lo, hi = table[value]
            lines.append(f"| {value} | {successes}/{n} | [{lo:.3f}, {hi:.3f}] |")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE_PATH)
    parser.add_argument("--out", type=Path, default=None, help="write report here instead of stdout")
    args = parser.parse_args(argv)

    records = load_latest_records(args.store)
    report = render_report(records, args.store, datetime.now(timezone.utc))

    if args.out:
        args.out.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
