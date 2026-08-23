#!/usr/bin/env python3
"""Q-MONSURF-1 M-B acceptance battery.

Retrieves the pruned daily_panel.csv read-only from the pre-prune tag (Great Prune, 2026-08-08),
groups it into Mon-anchored business-day weeks, and runs the frozen idle_clock_monitor logic
against every one of the 312 real weeks -- per
docs/briefs/pre-registration/Q-MONSURF-1-verdict-preregistration.md.

No new data pulled, no K spent -- this is a second read of the same committed panel the cited
RESULTS.md already scored. $0.
"""

import csv
import subprocess
import sys
from datetime import datetime
from io import StringIO

from idle_clock_monitor import evaluate_panel, score_battery, _default_lookback

PANEL_PATH = "lab/analysis/c1/tradeify_book_composition_2026-07-23/out/daily_panel.csv"
PRUNE_TAG = "pre-prune-2026-08-08"


def fetch_panel_csv() -> str:
    result = subprocess.run(
        ["git", "show", f"{PRUNE_TAG}:{PANEL_PATH}"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def parse_active_days(csv_text: str) -> list:
    """Returns list of (date, active_bool) in chronological order."""
    reader = csv.DictReader(StringIO(csv_text))
    rows = []
    for row in reader:
        date_str = row[""] if "" in row else row.get("date") or list(row.values())[0]
        combined = float(row["combined"])
        active = combined != 0.0
        rows.append((date_str, active))
    return rows


def group_into_weeks(day_rows: list) -> list:
    """Groups (date, active) rows into Mon-anchored weeks (business days only, no weekend rows
    expected -- the panel is already business-day-only per RESULTS.md)."""
    weeks = []
    current_week = []
    current_week_num = None
    for date_str, active in day_rows:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        iso_year, iso_week, _ = dt.isocalendar()
        key = (iso_year, iso_week)
        if key != current_week_num:
            if current_week:
                weeks.append(current_week)
            current_week = []
            current_week_num = key
        current_week.append(active)
    if current_week:
        weeks.append(current_week)
    return weeks


def sanity_check(day_rows: list, weeks: list) -> dict:
    """Reproduce RESULTS.md's own §1 anchors as a parse-correctness check before trusting
    anything downstream."""
    n_active_days = sum(1 for _, a in day_rows if a)
    n_zero_weeks = sum(1 for w in weeks if not any(w))
    n_one_day_weeks = sum(1 for w in weeks if sum(w) == 1)
    return {
        "n_days": len(day_rows),
        "n_active_days": n_active_days,
        "n_weeks": len(weeks),
        "n_zero_trade_weeks": n_zero_weeks,
        "pct_zero_trade_weeks": round(100 * n_zero_weeks / len(weeks), 1),
        "n_one_day_weeks": n_one_day_weeks,
        "pct_one_day_weeks": round(100 * n_one_day_weeks / len(weeks), 1),
    }


def run(weeks, lookback=_default_lookback):
    results = evaluate_panel(weeks, lookback=lookback)
    return score_battery(results)


def buggy_always_suppressed(day_active_flags, position):
    """Mutation: a monitor that always thinks the week is already satisfied (e.g. a stuck cache
    or an inverted boolean), so it never fires an alert. Should surface as a missed week on
    every one of the 82 real breached weeks -- the false-negative sibling of the lookback
    mutation above."""
    return True


def buggy_single_day_lookback(day_active_flags, position):
    """Mutation: a realistic off-by-one bug -- checks only the IMMEDIATELY preceding day for
    activity, instead of all days so far this week. A week active on Monday but quiet
    Tue/Wed would correctly need no T-2 alert under the frozen rule (the week is already
    satisfied) -- this buggy version fires one anyway once the immediately-preceding day goes
    quiet, which the scoring's spurious check (built against the REAL active_days, not this
    buggy lookback) should catch."""
    if position - 2 < 0:
        return False
    return bool(day_active_flags[position - 2])


def main():
    print("[fetch] retrieving daily_panel.csv from", PRUNE_TAG, "...")
    csv_text = fetch_panel_csv()
    day_rows = parse_active_days(csv_text)
    weeks = group_into_weeks(day_rows)

    checks = sanity_check(day_rows, weeks)
    print("[sanity] parsed panel:", checks)

    expected = {"n_days": 1556, "n_weeks": 312, "n_zero_trade_weeks": 82, "pct_zero_trade_weeks": 26.3}
    for k, v in expected.items():
        if checks[k] != v:
            print(f"[sanity] MISMATCH on {k}: expected {v}, got {checks[k]} -- HALT, do not trust battery")
            sys.exit(1)
    print("[sanity] all anchors reproduce RESULTS.md exactly -- panel parsing confirmed correct")

    print()
    print("[mutation] planting a logic defect: single-day lookback instead of full-week lookback...")
    mutated_score = run(weeks, lookback=buggy_single_day_lookback)
    print("[mutation] buggy-monitor score:", {k: v for k, v in mutated_score.items() if k not in ("missed", "spurious")})
    if mutated_score["pass"]:
        print("[mutation] FAIL -- the mutation was not caught by the battery. Battery is not trustworthy as written.")
        sys.exit(1)
    print(f"[mutation] caught: {mutated_score['n_spurious']} spurious alert(s) + {mutated_score['n_missed']} missed week(s) surfaced under the buggy lookback -- battery IS sensitive to this defect class")

    print()
    print("[mutation 2] planting a false-negative defect: lookback always reports 'already active'...")
    suppressed_score = run(weeks, lookback=buggy_always_suppressed)
    print("[mutation 2] buggy-monitor score:", {k: v for k, v in suppressed_score.items() if k not in ("missed", "spurious")})
    if suppressed_score["pass"] or suppressed_score["n_missed"] != 82 * 2:
        print(f"[mutation 2] FAIL -- expected 164 missed alerts (82 breached weeks x 2 checks), got {suppressed_score['n_missed']}. Battery is not trustworthy as written.")
        sys.exit(1)
    print(f"[mutation 2] caught: {suppressed_score['n_missed']} missed alerts across all 82 real breached weeks -- battery catches false-negative suppression too")

    print("[mutation] reverting to the correct (frozen) lookback for the actual acceptance run...")

    print()
    print("[battery] running against the real, unmutated panel (all 312 weeks)...")
    real_score = run(weeks)
    print("[battery] result:", {k: v for k, v in real_score.items() if k not in ("missed", "spurious")})
    if real_score["missed"]:
        print("[battery] missed weeks:", real_score["missed"][:10], "..." if len(real_score["missed"]) > 10 else "")
    if real_score["spurious"]:
        print("[battery] spurious alerts:", real_score["spurious"][:10], "..." if len(real_score["spurious"]) > 10 else "")

    print()
    print("VERDICT:", "PASS (RESOLVED)" if real_score["pass"] else "FAIL (FALSIFIED)")
    return real_score, checks, mutated_score


if __name__ == "__main__":
    main()
