"""Q-KBUDGET-1 Phase-2 screen — Clause-K floor scan over the ratified axis inventory.

Frozen screen: docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md
(freeze b304f2c). Ratified inventory: docs/briefs/Q-KBUDGET-1-phase1-inventory.md
(ratification anchor ca02030, G2 2026-07-14). Class S is out-of-screen-scope per
the §6 ratification record and is deliberately absent here.
Harvest Phase-3 (2026-07-16): append-only H1/H2 from
Q-KBUDGET-HARVEST-1 inventory addendum — D1–D7 rows unchanged (Trap-12).

Pure arithmetic on the production module (pre-reg §F hook #3 method) — zero data
pulls, zero K consumed. floor(K) = min annualized Sharpe clearing DSR >= 0.95 at
(K, V = 1/n), most-permissive across trade frequencies f in {0.5, 1, 2, 4}/day,
6.5y, Gaussian moments.

Run:  python lab/analysis/q_kbudget_1_2026-07/floor_scan.py
Emits: results.json + a markdown table on stdout (transcribed into RESULTS.md
and the pre-reg §E annex).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # lab/
from research_utils.deflated_sharpe import deflated_sharpe, expected_max_sharpe

CAP = 1.0          # Q-GATECART-1 Cap, resolved 2026-07-14 (S_B-anchored rung)
DSR_MIN = 0.95     # frozen threshold (DSR-K ADR — value unchanged by supersession)
YEARS = 6.5
FREQS = (0.5, 1.0, 2.0, 4.0)


def floor_at_k(k: int, years: float = YEARS, freqs=FREQS, t: float = DSR_MIN) -> float:
    best = None
    for f in freqs:
        n = int(round(252 * f * years))
        sr0 = expected_max_sharpe(k, 1.0 / n)
        s = 0.01
        while s < 6.0:
            if deflated_sharpe(s / math.sqrt(252 * f), n, 0.0, 3.0, sr0) >= t:
                break
            s += 0.005
        best = s if best is None else min(best, s)
    return round(best, 3)


# Ratified Class-D inventory (docs/briefs/Q-KBUDGET-1-phase1-inventory.md §2 @ ca02030).
# K_eff = K_intrinsic + K_banked (pre-reg §B). Where a row spans a K range, both
# ends are screened; the row PASSES Clause K only if its BEST end passes.
AXES = [
    dict(axis="D1 GC/MGC successor (any design)", family="GC/MGC", k_banked=3177,
         k_intrinsic=(1, 1), clause_n="n/a — Clause K kills first"),
    dict(axis="D2 wide mining, other GLBX family", family="ES/NQ/YM", k_banked=1,
         k_intrinsic=(1000, 10000), clause_n="n/a — Clause K kills first"),
    dict(axis="D3 HARV-class ES month-end mechanism", family="ES", k_banked=1,
         k_intrinsic=(1, 2),
         clause_n="INHERITED FAIL: P(primary|true) ~= 0.24-0.30, joint 0.05-0.06 "
                  "(Q-HARV-1 SS-R DECLINE, commit 9bddd33; N ~= 100 month-ends 2018+)"),
    dict(axis="D4 XAU T3b swap-dealer COT (prop expression = GC/MGC)", family="GC/MGC",
         k_banked=3177, k_intrinsic=(1, 2),
         clause_n="UNSCREENABLE-moot (no citable delta; cannot flip — Clause K "
                  "kills any GC/MGC expression independently)"),
    dict(axis="D5 NQ/MNQ intraday-momentum footprint (was: gamma-positioning)",
         family="MYM/MNQ", k_banked=0,
         k_intrinsic=(1, 3),
         clause_n="PASS: confirm-construct = intraday-momentum footprint "
                  "(Baltussen et al. 2021 JFE NQ cohort, delta/sigma=0.113, "
                  "power=0.947 at N=1000); DJ30 drop/down-weight; "
                  "operator-ratified 2026-07-15 — see d5_clause_n_rescreen.md"),
    dict(axis="D6 eurusd_pattern_enum Phase-4 (locked K=450)", family="6E/EURUSD",
         k_banked=0, k_intrinsic=(450, 450), clause_n="n/a — Clause K kills first"),
    dict(axis="D7 JPY month-end mechanism (6J expression)", family="6J", k_banked=0,
         k_intrinsic=(1, 3),
         clause_n="FAIL (N, class-analogue): P(primary|true) ~= 0.30 < 0.50 at N~=100, "
                  "delta/sigma=0.144 (HARV class-analogue, Q-HARV-1 SS-R 9bddd33) -- "
                  "see d7_clause_n_screen.md"),
    # --- Q-KBUDGET-HARVEST-1 Phase-3 addendum (append-only; D1–D7 frozen) ---
    dict(axis="H-OD-1 overnight-drift inventory-risk (2:00-3:00 ET) [harvest H1]",
         family="ES", k_banked=1,
         k_intrinsic=(1, 2),
         clause_n="PASS: power=0.837 at N=1000, delta/sigma=0.093 "
                  "(FRBNY SR917 Table I; harvest addendum H1; Path 1a; RATIFIED 2026-07-16)"),
    # H2 pin 2026-07-16 (gate-stack audit R4): operator chose reading (c) —
    # Default-#1 OOS 2019-05-06→present, N≈86, power=0.34, Clause-N FAIL.
    # The harvest-addendum N=192 / power=0.638 PASS is superseded; citing it
    # as a fundable PASS is a forbidden move (H-TSMOM-1-ES-tsmom-scoping.md §3).
    # RESULTS.md / results.json in this directory stay the historical Phase-3
    # snapshot (Trap-12); this living harness must not reprint the stale PASS.
    dict(axis="H-TSMOM-1 Moskowitz 12m/1m TSMOM (S&P500/ES) [harvest H2]",
         family="ES", k_banked=1,
         k_intrinsic=(1, 1),
         clause_n="FAIL (N, Default-#1 OOS): power=0.34 at N=86, delta/sigma=0.167 "
                  "(Moskowitz Fig.2; operator-pinned reading (c) 2026-07-16; "
                  "supersedes harvest-addendum N=192 / power=0.638 PASS — "
                  "H-TSMOM-1-ES-tsmom-scoping.md)"),
]


def screen() -> list[dict]:
    rows = []
    for a in AXES:
        lo, hi = a["k_intrinsic"]
        k_lo, k_hi = lo + a["k_banked"], hi + a["k_banked"]
        f_lo, f_hi = floor_at_k(k_lo), floor_at_k(k_hi)
        clause_k = "PASS" if f_lo <= CAP else "FAIL"
        unscreenable = a["clause_n"].startswith("UNSCREENABLE —")
        if clause_k == "FAIL":
            verdict = "FAIL (Clause K)"
        elif a["clause_n"].startswith("INHERITED FAIL"):
            verdict = "FAIL (Clause N, inherited)"
        elif a["clause_n"].startswith("FAIL (N,"):
            # Newly-screened (non-inherited) Clause-N failure via a class-analogue
            # delta, per pre-reg Sec B's "nearest analytic analogue" provision.
            verdict = "FAIL (Clause N)"
        elif unscreenable:
            verdict = "UNSCREENABLE"
        else:
            verdict = "PASS"
        rows.append(dict(a, k_eff=(k_lo, k_hi), floor=(f_lo, f_hi),
                         clause_k=clause_k, verdict=verdict))
    return rows


def main() -> None:
    rows = screen()
    out = Path(__file__).with_name("results.json")
    out.write_text(json.dumps(dict(cap=CAP, dsr_min=DSR_MIN, rows=rows), indent=2))
    print(f"| Axis | Family | K_eff | floor(K_eff) | Clause K (Cap {CAP}) | Clause N | Screen |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        k = f"{r['k_eff'][0]}" if r['k_eff'][0] == r['k_eff'][1] else f"{r['k_eff'][0]}-{r['k_eff'][1]}"
        fl = f"{r['floor'][0]}" if r['floor'][0] == r['floor'][1] else f"{r['floor'][0]}-{r['floor'][1]}"
        print(f"| {r['axis']} | {r['family']} | {k} | {fl} | {r['clause_k']} | {r['clause_n']} | **{r['verdict']}** |")
    screened = [r for r in rows if r["verdict"] != "UNSCREENABLE"]
    unscreenable = [r for r in rows if r["verdict"] == "UNSCREENABLE"]
    passing = [r for r in rows if r["verdict"] == "PASS"]
    print(f"\nScreened FAIL: {len(screened) - len(passing)}/{len(screened)} · PASS: {len(passing)} · UNSCREENABLE: {len(unscreenable)}")
    if not passing and unscreenable:
        print("Verdict per pre-reg §D: AMBIGUOUS-HOLD (all screened fail; >=1 verdict-relevant UNSCREENABLE)")
    elif not passing:
        print("Verdict per pre-reg §D: FALSIFIED (fundable set empty; zero UNSCREENABLE)")
    else:
        print("Verdict per pre-reg §D: RESOLVED (fundable set non-empty)")


if __name__ == "__main__":
    main()
