"""Q-RAIL-1 — re-author MNQ + apply Tradeify/MFFU venue deltas (D1–D5).

Operator GO 2026-07-17. No locked CFD parameter edits — futures sizing/EOD/costs only.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(r"C:/Users/joshu/multi_firm_operations")
STRAT = ROOT / "core/strategies"
OUT_DIR = ROOT / "lab/analysis/c1/q_rail_1_2026-07"

# Discharge-tier defaults (Phase-1 D1–D5). MFFU commission 0.95 is a TV override note.
COMMISSION = 0.91  # Tradeify Select; MFFU=0.95 documented in FUTURES_LOCK
ACCOUNT = 100_000
MICRO_CAP = 80
# 15:45 ET bar closes 16:00 with process_orders_on_close — inside E1 / before MFFU 16:10
EOD_HOUR = 15
EOD_MINUTE = 45


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def apply_mym_deltas(text: str) -> str:
    """Update on-disk MYM edition Bulenox constants → discharge-tier defaults."""
    reps = [
        ("commission_value=0.61,", f"commission_value={COMMISSION},"),
        (
            'accountSize   = input.float(150000, "Account Size ($)", group=group_futures)',
            f'accountSize   = input.float({ACCOUNT}, "Account Size ($)", group=group_futures)',
        ),
        (
            'microCap      = input.int(150, "Micro Contract Cap", group=group_futures)',
            f'microCap      = input.int({MICRO_CAP}, "Micro Contract Cap", group=group_futures)',
        ),
        (
            'isEodBar = hour(time, "America/New_York") == 16 and minute(time, "America/New_York") == 30',
            f'isEodBar = hour(time, "America/New_York") == {EOD_HOUR} and minute(time, "America/New_York") == {EOD_MINUTE}',
        ),
    ]
    out = text
    for old, new in reps:
        if old not in out:
            raise SystemExit(f"MYM delta miss: {old!r}")
        out = out.replace(old, new, 1)
    # provenance banner after strategy()
    banner = (
        "\n// Q-RAIL-1 venue re-parameterization 2026-07-17 (Tradeify/MFFU discharge):\n"
        f"//   commission ${COMMISSION}/side (Tradeify; set 0.95 for MFFU TV runs),\n"
        f"//   accountSize ${ACCOUNT:,}, microCap {MICRO_CAP},\n"
        f"//   EOD force-flat {EOD_HOUR}:{EOD_MINUTE:02d} ET bar → ~16:00 ET fill (E1).\n"
        "// Day soft-stop default remains -1.15% (automated-chain promoted default).\n"
    )
    marker = "margin_short=0)\n"
    if marker not in out:
        raise SystemExit("MYM banner anchor miss")
    out = out.replace(marker, marker + banner, 1)
    return out


def port_nas_to_mnq(nas: str) -> str:
    """Byte-carry NAS100 CFD → MNQ edition with discharge-tier venue constants."""
    t = nas

    # Header
    old_hdr = '''strategy("Striker NAS100 v1.0", "Striker NAS100 v1", overlay=true,
     initial_capital=200000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     commission_type=strategy.commission.cash_per_order,
     commission_value=0,
     slippage=2,'''
    new_hdr = f'''strategy("Striker NAS100 v1 MNQ", "Striker NAS100 MNQ", overlay=true,
     initial_capital=200000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     commission_type=strategy.commission.cash_per_contract,
     commission_value={COMMISSION},
     slippage=1,'''
    if old_hdr not in t:
        raise SystemExit("NAS header miss")
    t = t.replace(old_hdr, new_hdr, 1)

    banner = (
        "\n// ============================================================================\n"
        "// FUTURES VENUE EDITION — MNQ (Q-RAIL-1 re-author 2026-07-17)\n"
        "// Source: striker_nas100_v1.pine (locked). Parameter-axis LOCKED.\n"
        "// Venue deltas only: integer MNQ sizing + RESERVE cap, EOD force-flat ET,\n"
        f"// costs ${COMMISSION}/side (Tradeify; MFFU TV override 0.95), accountSize\n"
        f"// ${ACCOUNT:,}, microCap {MICRO_CAP}, EOD {EOD_HOUR}:{EOD_MINUTE:02d} ET bar.\n"
        "// Precedence: FUTURES_LOCK.md + lab/analysis/c1/q_rail_1_2026-07/PHASE1.md D1–D5.\n"
        "// ============================================================================\n"
    )
    t = t.replace("margin_short=0)\n", "margin_short=0)\n" + banner, 1)

    futures_block = f'''
// ============================================================================
// FUTURES (MNQ)
// ============================================================================
group_futures = "═══ FUTURES (MNQ) ═══"
accountSize   = input.float({ACCOUNT}, "Account Size ($)", group=group_futures)
microCap      = input.int({MICRO_CAP}, "Micro Contract Cap", group=group_futures)
mnqPointValue = input.float(2.00, "MNQ $ per index point", group=group_futures)
forceFlat     = input.bool(true, "EOD Force-Flat (ET)", group=group_futures)

'''
    insert_at = "// ============================================================================\n// BREAKOUT\n// ============================================================================\n"
    if insert_at not in t:
        raise SystemExit("NAS breakout anchor miss")
    t = t.replace(insert_at, futures_block + insert_at, 1)

    old_size = '''// ============================================================================
// POSITION SIZING — rolling-equity (G2 verified 2026-05-04)
// ============================================================================
calcSize(stopDist) =>
    risk = strategy.equity * (riskPerTrade / 100)
    stopDist > 0 ? risk / stopDist : 0
'''
    new_size = '''// ============================================================================
// POSITION SIZING — integer MNQ, static account (live-path; B0)
// ============================================================================
calcSize(stopDist) =>
    riskDollars = accountSize * (riskPerTrade / 100)
    perContract = stopDist * mnqPointValue
    rawQty = perContract > 0 ? math.floor(riskDollars / perContract) : 0
    reserveCap = math.floor(microCap / (1 + pyramidSize / 100))
    math.min(rawQty, reserveCap)
'''
    if old_size not in t:
        raise SystemExit("NAS calcSize miss")
    t = t.replace(old_size, new_size, 1)

    # EOD + eodHaltedToday (mirror MYM)
    old_daily = '''var int dailyTradeCount   = 0
var float strikerDayPnl   = 0.0
var bool strikerHaltedToday = false
var int prevClosedCount   = 0

if ta.change(time("D")) != 0
    dailyTradeCount     := 0
    strikerDayPnl       := 0.0
    strikerHaltedToday  := false
'''
    new_daily = '''var int dailyTradeCount   = 0
var float strikerDayPnl   = 0.0
var bool strikerHaltedToday = false
var bool eodHaltedToday   = false
var int prevClosedCount   = 0

if ta.change(time("D")) != 0
    dailyTradeCount     := 0
    strikerDayPnl       := 0.0
    strikerHaltedToday  := false
    eodHaltedToday      := false
'''
    if old_daily not in t:
        raise SystemExit("NAS daily vars miss")
    t = t.replace(old_daily, new_daily, 1)

    old_halt = '''if not strikerHaltedToday and strikerDayPnl <= strategy.initial_capital * strikerDayStopPct / 100
    strikerHaltedToday := true

canTrade = not ddHit and strategy.opentrades == 0 and dailyTradeCount < maxDailyTrades and not strikerHaltedToday
'''
    new_halt = f'''if not strikerHaltedToday and strikerDayPnl <= strategy.initial_capital * strikerDayStopPct / 100
    strikerHaltedToday := true

// EOD force-flat (ET-pinned, DST-aware) — {EOD_HOUR}:{EOD_MINUTE:02d} bar → ~16:00 ET fill (E1 / MFFU 16:10).
isEodBar = hour(time, "America/New_York") == {EOD_HOUR} and minute(time, "America/New_York") == {EOD_MINUTE}
if forceFlat and isEodBar
    strategy.close_all("EOD Flat")
    eodHaltedToday := true

canTrade = not ddHit and strategy.opentrades == 0 and dailyTradeCount < maxDailyTrades and not strikerHaltedToday and not eodHaltedToday
'''
    if old_halt not in t:
        raise SystemExit("NAS halt/canTrade miss")
    t = t.replace(old_halt, new_halt, 1)

    old_entry = '''if longSignal and canTrade
    stopDist = atrVal * stopAtr
    size     = calcSize(stopDist)

    strategy.entry("Long", strategy.long, qty=size)

    entryPrice     := close
    entryAtr       := atrVal
    tpPrice        := close + (atrVal * tpAtr)
    currentStop    := close - stopDist
    trailStop      := na
    trailTightened := false
    barsInTrade    := 0
    initialSize    := size
    pyramidCount   := 0
    pyramidDone    := false
    beTriggered    := false
    dailyTradeCount := dailyTradeCount + 1
'''
    new_entry = '''flooredThisBar = false
if longSignal and canTrade
    stopDist = atrVal * stopAtr
    size     = calcSize(stopDist)

    if size > 0
        strategy.entry("Long", strategy.long, qty=size)

        entryPrice     := close
        entryAtr       := atrVal
        tpPrice        := close + (atrVal * tpAtr)
        currentStop    := close - stopDist
        trailStop      := na
        trailTightened := false
        barsInTrade    := 0
        initialSize    := size
        pyramidCount   := 0
        pyramidDone    := false
        beTriggered    := false
    else
        flooredThisBar := true

    dailyTradeCount := dailyTradeCount + 1
'''
    if old_entry not in t:
        raise SystemExit("NAS entry block miss — inspect source")
    t = t.replace(old_entry, new_entry, 1)

    old_add = "        addSize = initialSize * (pyramidSize / 100)"
    new_add = "        addSize = math.floor(initialSize * (pyramidSize / 100))"
    if old_add not in t:
        raise SystemExit("NAS addSize miss")
    t = t.replace(old_add, new_add, 1)

    # Flooring visibility before ALERTS
    floor_viz = '''
// ============================================================================
// FLOORING VISIBILITY (R9)
// ============================================================================
plotshape(flooredThisBar, "Floored", shape.xcross, location.abovebar, color.orange, size=size.tiny)
if flooredThisBar
    alert("Striker NAS100 MNQ: qty floored to 0 (insufficient account/ATR headroom under RESERVE cap)", alert.freq_once_per_bar)

'''
    if "// ============================================================================\n// ALERTS\n// ============================================================================\n" not in t:
        raise SystemExit("NAS alerts anchor miss")
    t = t.replace("// ============================================================================\n// ALERTS\n// ============================================================================\n", floor_viz + "// ============================================================================\n// ALERTS\n// ============================================================================\n", 1)

    # Alert strings
    t = t.replace("Striker NAS100 v1.0", "Striker NAS100 MNQ")
    t = t.replace("STRIKER NAS100 v1.0", "STRIKER NAS100 MNQ")

    return t


def main() -> None:
    mym_path = STRAT / "striker/striker_dj30_v4.5_mym.pine"
    nas_path = STRAT / "nas/striker_nas100_v1.pine"
    mnq_path = STRAT / "nas/striker_nas100_v1_mnq.pine"

    pre_mym = sha256(mym_path)
    mym_new = apply_mym_deltas(mym_path.read_text(encoding="utf-8"))
    mym_path.write_text(mym_new, encoding="utf-8", newline="\n")
    post_mym = sha256(mym_path)

    mnq_new = port_nas_to_mnq(nas_path.read_text(encoding="utf-8"))
    mnq_path.write_text(mnq_new, encoding="utf-8", newline="\n")
    post_mnq = sha256(mnq_path)

    report = {
        "mym_pre": pre_mym,
        "mym_post": post_mym,
        "mnq_post": post_mnq,
        "mym_bytes": mym_path.stat().st_size,
        "mnq_bytes": mnq_path.stat().st_size,
        "commission": COMMISSION,
        "account": ACCOUNT,
        "micro_cap": MICRO_CAP,
        "eod": f"{EOD_HOUR}:{EOD_MINUTE:02d}",
    }
    (OUT_DIR / "phase1b_reauthor_hashes.json").write_text(
        __import__("json").dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(report)


if __name__ == "__main__":
    main()
