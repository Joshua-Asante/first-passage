#!/usr/bin/env python3
"""F3 cadence measurement — Bulenox / MFFU / BluSky vs Striker's cadence.

Fork F3 (ADR 2026-08-04 §7): score the three remaining FRIENDLY firms against
the locked Striker book's cadence axis. Sibling of
c1_cadence_inactivity_2026-08-02 (Tradeify only). Same panel, same seeds, same
OFF→ON factorial; the deliverable is the per-tier inactivity delta.

Tiers (frozen $100K band):
  Bulenox_100K          trailing,        inactivity_max_idle_days=5
  MFFU_Rapid_100K       trailing_locking, inactivity_max_idle_days=5
  BluSky_Premium_100K   trailing,        inactivity_max_idle_days=30

Control: Tradeify_Select_100K C2-off · 1.00× OFF/ON must reproduce the
published pin (pass 68.07% / INACT 92.60%) before any new cell is trusted.

Geometry notes (attested in output):
  * MFFU / Tradeify trailing_locking — disk dd_lock_offset_usd is now the
    unreachable-lock idiom (ADR 2026-08-04 firm-rules-eval-lock-fix); used
    native, no runtime override.
  * Bulenox / BluSky trailing — firm_kwargs expresses %-of-peak trailing
    (optimistic vs their fixed-$ ropes). Absolute DD-bust levels are NOT
    gate-grade; the OFF→ON inactivity delta is the F3 deliverable.

Arms per measured tier: {C2-off, C2-on} × {1.00×, 0.50×} × {inact OFF, ON}.
Panel: committed 2026-07-23 book-composition daily_panel (backtest sizing) —
absolute pass/bust NOT comparable to rail-geometry pins; delta is.

Run:  python lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/run_f3_cadence.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
for _p in (_ROOT / "core", _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from portfolio_mc import HORIZON_CAP, SEEDS, SIMS_PER_SEED, run_seed  # noqa: E402
from mc.ingest import build_week_blocks  # noqa: E402
from mc.preflight import firm_kwargs  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402

PANEL = (
    _ROOT / "lab" / "analysis" / "c1" / "tradeify_book_composition_2026-07-23"
    / "out" / "daily_panel.csv"
)
OUT = _HERE / "out"
STRATS = ("striker_dj30", "striker_nas")
OUTCOMES = (
    "pass", "bust_daily", "bust_static", "bust_trailing",
    "bust_inactivity", "horizon_cap",
)
BUST_KEYS = ("bust_daily", "bust_static", "bust_trailing")

# Headline F3 tiers + Tradeify control for pin reproduction.
TIERS = (
    "Bulenox_100K",
    "MFFU_Rapid_100K",
    "BluSky_Premium_100K",
)
CONTROL_TIER = "Tradeify_Select_100K"
# Published pin from c1_cadence_inactivity_2026-08-02 (C2-off · 1.00×).
CONTROL_PIN = {
    "pass_off": 0.6807,
    "inact_on": 0.9260,
    "tol_pp": 0.50,  # absolute pp; seeds identical → expect ~0.00pp
}

NO_PROTECTION_TRIGGER = 10.0
DD_TRIGGER = 0.015
DD_SCALE = 0.40


def arm(tier: str, blocks: np.ndarray, *, c2_on: bool, inactivity_off: bool) -> dict:
    # ⚠ BluSky's limit CHANGED after this study published. RESULTS §2/§3 BluSky
    # rows were measured at idle=30; ADR 2026-08-05b sourced the real rule (ToU
    # art. 11490284 §3.3, trade-based per art. 12434442) and unit-corrected it to
    # 22 idle bdays. Re-running this script now therefore reproduces Bulenox,
    # MFFU and the Tradeify control EXACTLY, but returns the corrected BluSky
    # figures (INACT 4.87–13.14%), not the published 0.52–1.40%. That is
    # intended — see the RESULTS Addendum 2026-08-05b and
    # out/blusky_unit_sensitivity.{log,json}.
    # allow_unsourced_inactivity is retained and is now a no-op for every shipped
    # tier (all sourced); it stays so the script keeps working if a future tier is
    # flagged, and so the guard's intent remains visible at the call site.
    kw = firm_kwargs(
        tier, inactivity_off=inactivity_off, allow_unsourced_inactivity=True
    )
    res = [
        run_seed(
            s, SIMS_PER_SEED, blocks,
            dd_trigger=DD_TRIGGER if c2_on else NO_PROTECTION_TRIGGER,
            dd_scale=DD_SCALE,
            horizon=HORIZON_CAP, strats=STRATS, firm_kwargs=kw,
        )
        for s in SEEDS
    ]
    n = SIMS_PER_SEED
    for r in res:
        total = sum(r["outcomes"][k] for k in OUTCOMES)
        assert total == n, f"{tier}: outcome buckets sum {total} != {n} sims"
    agg = {k: float(np.mean([r["outcomes"][k] / n for r in res])) for k in OUTCOMES}
    agg["bust_dd"] = sum(agg[k] for k in BUST_KEYS)
    dtp = [
        np.asarray(r["days_to_pass"], dtype=float)
        for r in res if len(r.get("days_to_pass", []))
    ]
    agg["median_days_to_pass"] = (
        float(np.median(np.concatenate(dtp))) if dtp else None
    )
    agg["inactivity_limit_used"] = int(kw["inactivity_limit"])
    agg["dd_type_used"] = str(kw["dd_type"])
    if "dd_lock_offset_usd" in kw:
        agg["dd_lock_offset_used"] = float(kw["dd_lock_offset_usd"])
    return agg


def run_tier_grid(tier: str, panel: pd.DataFrame) -> dict[str, dict]:
    f = FIRM_RULES[tier]
    idle = f["inactivity_max_idle_days"]
    print(f"\n{'=' * 78}")
    print(f"tier   : {tier}")
    print(
        f"  dd_type={f['dd_type']}  max_dd={f['max_dd_pct']}%  "
        f"target={f['profit_target_pct']}%  min_days={f['min_trading_days']}"
    )
    print(f"  inactivity_max_idle_days = {idle}")
    if f["dd_type"] == "trailing":
        print(
            "  GEOMETRY NOTE: %-of-peak trailing via firm_kwargs "
            "(optimistic vs venue fixed-$ rope) — inactivity delta is the deliverable"
        )
    elif f["dd_type"] == "trailing_locking":
        print(
            f"  GEOMETRY ATTESTATION: dd_lock_offset_usd = "
            f"{f['dd_lock_offset_usd']} (native; unreachable-lock idiom)"
        )

    results: dict[str, dict] = {}
    for c2_on in (False, True):
        c2_label = "C2-on (rail overlay 1.5%/0.40x)" if c2_on else "C2-off (raw book)"
        for scalar in (1.00, 0.50):
            blocks = build_week_blocks(panel * scalar)
            print(
                f"\n--- {c2_label} | risk scalar {scalar:.2f}x "
                f"({len(blocks)} week-blocks) ---"
            )
            for off in (True, False):
                a = arm(tier, blocks, c2_on=c2_on, inactivity_off=off)
                key = (
                    f"{'c2on' if c2_on else 'c2off'}_{scalar:.2f}x_"
                    f"inact{'OFF' if off else 'ON'}"
                )
                results[key] = a
                med = (
                    f"{a['median_days_to_pass']:.0f}"
                    if a["median_days_to_pass"] is not None else "n/a"
                )
                tag = "OFF   " if off else f"ON({idle}d)"
                print(
                    f"  inactivity {tag}  "
                    f"pass {a['pass']:>7.2%}  bust_dd {a['bust_dd']:>7.2%}  "
                    f"INACT {a['bust_inactivity']:>7.2%}  "
                    f"horizon {a['horizon_cap']:>6.2%}  med-days {med}"
                )
    return results


def print_deltas(tier: str, results: dict[str, dict]) -> None:
    print(f"\nDELTA (inactivity OFF -> ON) — {tier}")
    for c2 in ("c2off", "c2on"):
        for scalar in ("1.00x", "0.50x"):
            off = results[f"{c2}_{scalar}_inactOFF"]
            on = results[f"{c2}_{scalar}_inactON"]
            print(f"  {c2} / {scalar}:")
            print(
                f"    pass            {off['pass']:>7.2%} -> {on['pass']:>7.2%}  "
                f"({(on['pass'] - off['pass']) * 100:+.2f} pp)"
            )
            print(
                f"    bust (DD-class) {off['bust_dd']:>7.2%} -> {on['bust_dd']:>7.2%}"
            )
            print(
                f"    bust_inactivity {off['bust_inactivity']:>7.2%} -> "
                f"{on['bust_inactivity']:>7.2%}"
            )


def check_control(results: dict[str, dict]) -> bool:
    """Reproduce Tradeify C2-off · 1.00× pin; return True on MATCH."""
    off = results["c2off_1.00x_inactOFF"]
    on = results["c2off_1.00x_inactON"]
    d_pass = abs(off["pass"] - CONTROL_PIN["pass_off"]) * 100
    d_inact = abs(on["bust_inactivity"] - CONTROL_PIN["inact_on"]) * 100
    ok = d_pass <= CONTROL_PIN["tol_pp"] and d_inact <= CONTROL_PIN["tol_pp"]
    status = "MATCH" if ok else "DRIFT"
    print(f"\nCONTROL PIN ({CONTROL_TIER} C2-off · 1.00×): {status}")
    print(
        f"  pass OFF   measured {off['pass']:.2%}  "
        f"pin {CONTROL_PIN['pass_off']:.2%}  d={d_pass:.3f}pp"
    )
    print(
        f"  INACT ON   measured {on['bust_inactivity']:.2%}  "
        f"pin {CONTROL_PIN['inact_on']:.2%}  d={d_inact:.3f}pp"
    )
    return ok


class _Tee:
    """Stdout + log file with line-buffered flush (avoids PowerShell Tee hang)."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._fp = path.open("w", encoding="utf-8", newline="\n")
        self._stdout = sys.stdout

    def write(self, s: str) -> int:
        self._stdout.write(s)
        self._fp.write(s)
        if "\n" in s:
            self._stdout.flush()
            self._fp.flush()
        return len(s)

    def flush(self) -> None:
        self._stdout.flush()
        self._fp.flush()

    def close(self) -> None:
        self._fp.close()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    log_path = OUT / "f3_cadence.log"
    tee = _Tee(log_path)
    sys.stdout = tee  # type: ignore[assignment]
    try:
        _main_body()
    finally:
        sys.stdout = tee._stdout  # type: ignore[assignment]
        tee.close()
        print(f"log saved -> {log_path.relative_to(_ROOT).as_posix()}", flush=True)


def _main_body() -> None:
    panel = pd.read_csv(PANEL, index_col=0, parse_dates=True)[list(STRATS)]
    rel = str(PANEL.relative_to(_ROOT)).replace("\\", "/")
    print(f"panel  : {rel}")
    print(
        f"  {panel.index.min().date()} -> {panel.index.max().date()}  "
        f"({len(panel)} bdays)  net ${panel.sum().sum():,.2f}  "
        f"active days {int((panel.sum(axis=1) != 0).sum())}"
    )
    print(
        f"sims   : {SIMS_PER_SEED:,} x {len(SEEDS)} seeds, "
        f"horizon {HORIZON_CAP}d, seeds identical across all arms"
    )

    payload: dict = {
        "panel": rel,
        "sims": f"{SIMS_PER_SEED}x{len(SEEDS)}",
        "horizon": HORIZON_CAP,
        "tiers": {},
        "control": {},
    }

    # Control first — pin cell only (C2-off · 1.00× OFF/ON). Halt on drift.
    print(f"\n{'=' * 78}")
    print(f"CONTROL PIN: {CONTROL_TIER} C2-off · 1.00× OFF/ON")
    blocks_1x = build_week_blocks(panel * 1.00)
    ctrl = {
        "c2off_1.00x_inactOFF": arm(
            CONTROL_TIER, blocks_1x, c2_on=False, inactivity_off=True
        ),
        "c2off_1.00x_inactON": arm(
            CONTROL_TIER, blocks_1x, c2_on=False, inactivity_off=False
        ),
    }
    for key, a in ctrl.items():
        med = (
            f"{a['median_days_to_pass']:.0f}"
            if a["median_days_to_pass"] is not None else "n/a"
        )
        print(
            f"  {key}: pass {a['pass']:>7.2%}  bust_dd {a['bust_dd']:>7.2%}  "
            f"INACT {a['bust_inactivity']:>7.2%}  med-days {med}"
        )
    pin_ok = check_control(ctrl)
    payload["control"] = {
        "tier": CONTROL_TIER,
        "pin_match": pin_ok,
        "arms": ctrl,
    }
    if not pin_ok:
        print("\nHALT: Tradeify control pin drifted — investigate before trusting F3 cells.")
        (OUT / "f3_cadence.json").write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )
        sys.exit(2)

    out_path = OUT / "f3_cadence.json"
    for tier in TIERS:
        arms = run_tier_grid(tier, panel)
        print_deltas(tier, arms)
        f = FIRM_RULES[tier]
        payload["tiers"][tier] = {
            "dd_type": f["dd_type"],
            "inactivity_max_idle_days": f["inactivity_max_idle_days"],
            "max_dd_pct": f["max_dd_pct"],
            "profit_target_pct": f["profit_target_pct"],
            "min_trading_days": f["min_trading_days"],
            "arms": arms,
        }
        # Checkpoint after every tier — a late crash must not discard measured cells.
        out_path.write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )

    print("\n" + "=" * 78)
    print("CAVEAT: engine barrier = rolling N-consecutive-idle-bday ABSORBING.")
    print("Venue rules differ (Mon-Fri week / trading-day idle / subscription")
    print("window). Numbers price the unmitigated barrier assumption — not a")
    print("forecast of any venue's soft-enforcement path.")
    print("=" * 78)

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    out_rel = str(out_path.relative_to(_ROOT)).replace("\\", "/")
    print(f"\nresults saved -> {out_rel}")


if __name__ == "__main__":
    main()
