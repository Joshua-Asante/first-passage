#!/usr/bin/env python3
"""Score Q-CAPALLOC-2 6-cell grid from capalloc2/*.json artifacts."""
from __future__ import annotations

import json
from pathlib import Path

D = Path(__file__).resolve().parent
CELLS = [
    ("w150_p0", 150, 0),
    ("w200_p0", 200, 0),
    ("w250_p0", 250, 0),
    ("w150_p250", 150, 250),
    ("w200_p250", 200, 250),
    ("w250_p250", 250, 250),
]


def main() -> None:
    rows = []
    for name, win, pay in CELLS:
        j = json.loads((D / f"{name}.json").read_text(encoding="utf-8"))
        pins = j["rule_pins"]["used"]
        assert pins["WIN_MIN"] == float(win), (name, pins)
        assert pins["PAYOUT_MIN"] == float(pay), (name, pins)
        w1 = j["scoring"]["floor_on_D1D2_only"]["winners"]
        w2 = j["scoring"]["floor_on_all_four"]["winners"]
        d51 = j["scoring"]["floor_on_D1D2_only"]["detail"].get("51/29")
        rows.append((name, win, pay, w1, w2, j["verdict"], d51))

    print(f"{'cell':<12} {'W':>4} {'P':>4} {'winners':<16} {'51/29 H1':<8} {'51/29 H2':<8}")
    print("-" * 72)
    clear_all = None
    for name, win, pay, w1, w2, verdict, d51 in rows:
        h1 = d51["H1"]["all"] if d51 else None
        h2 = d51["H2"]["all"] if d51 else None
        both = bool(h1 and h2)
        print(f"{name:<12} {win:>4} {pay:>4} {str(w1):<16} {str(h1):<8} {str(h2):<8}")
        if clear_all is None:
            clear_all = set(w1)
        else:
            clear_all &= set(w1)

    print()
    # CAPALLOC-2 §6: need >=1 candidate clearing D1-D5 both halves at ALL 6 cells
    survivors = None
    for name, win, pay, w1, w2, verdict, d51 in rows:
        s = set(w1) & set(w2)  # both floor readings agree
        survivors = s if survivors is None else (survivors & s)
        print(f"  {name}: winners={w1} (strict={w2})")

    verified_ok = "51/29" in set(rows[1][3])  # w200_p0
    print()
    print(f"intersection across all 6 cells (both floors): {sorted(survivors) if survivors else '(none)'}")
    print(f"verified cell (200,0) has 51/29: {verified_ok}")

    if survivors:
        print("VERDICT: RESOLVED-ROBUST")
    elif verified_ok:
        failing = [n for n, _, _, w1, w2, _, _ in rows if "51/29" not in (set(w1) & set(w2))]
        print(f"VERDICT: RESOLVED-FRAGILE  failing_cells={failing}")
    else:
        print("VERDICT: FALSIFIED")


if __name__ == "__main__":
    main()
