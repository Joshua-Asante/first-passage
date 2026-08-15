"""Q-TXG-1 Blocks 2–3 — sibling-swap research ports (execution mechanics only).

Reads locked CFD Pine from the durable primary checkout (gitignored bytes),
writes research prototypes into this worktree's `_archive/`, and prints SHA256
pins for PORT_MANIFEST.

Frozen mapping (cell PREREGs 2026-08-12):
  * striker_nas100 × MYM — NAS100 v1 signal identity, MYM venue economics
  * striker × MNQ       — DJ30 v4.5 signal identity, MNQ venue economics

Does NOT redeploy WITHDRAWN(F1) same-underlying legs. No B1 rail alerts
(research prototype, not a live leg). Locked day soft-stops preserved
(DJ30 −2% Pine default; NAS100 −1.5%). initial_capital aligned to Tradeify
Select 100K (Guardian-MGC / Aegis-6J true-target precedent).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

PRIMARY = Path(r"C:/Users/joshu/multi_firm_operations/core/strategies/_archive")
WT = Path(__file__).resolve().parents[4]  # worktree root
OUT_NAS = WT / "core/strategies/_archive/nas"
OUT_STR = WT / "core/strategies/_archive/striker"

COMMISSION = 0.91
ACCOUNT = 100_000
MICRO_CAP = 80
EOD_HOUR = 15
EOD_MINUTE = 45
INIT_CAPITAL = 100_000  # true-target geometry (not CFD 200k)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _req(hay: str, needle: str, label: str) -> None:
    if needle not in hay:
        raise SystemExit(f"{label} miss: {needle[:80]!r}")


def port_nas_to_mym(nas: str) -> str:
    """NAS100 locked signal → MYM venue mechanics (sibling-swap)."""
    t = nas

    old_hdr = """strategy("Striker NAS100 v1.0", "Striker NAS100 v1", overlay=true,
     initial_capital=200000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     commission_type=strategy.commission.cash_per_order,
     commission_value=0,
     slippage=2,"""
    new_hdr = f"""strategy("Striker NAS100 v1 MYM Q-TXG-1 PROTOTYPE", "Striker NAS100 MYM QTXG1", overlay=true,
     initial_capital={INIT_CAPITAL},
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     commission_type=strategy.commission.cash_per_contract,
     commission_value={COMMISSION},
     slippage=1,"""
    _req(t, old_hdr, "NAS header")
    t = t.replace(old_hdr, new_hdr, 1)

    banner = (
        "\n// ============================================================================\n"
        "// Q-TXG-1 SIBLING-SWAP PROTOTYPE — MYM (2026-08-12)\n"
        "// Source: striker_nas100_v1.pine (LOCKED). Parameter-axis LOCKED.\n"
        "// Cross-underlying research port: NAS100 breakout logic on CBOT MYM.\n"
        "// NOT the WITHDRAWN(F1) nas100×MNQ redeploy. Venue deltas only:\n"
        f"//   integer MYM sizing + RESERVE cap, EOD force-flat ET, costs\n"
        f"//   ${COMMISSION}/side (Tradeify Select), accountSize ${ACCOUNT:,},\n"
        f"//   microCap {MICRO_CAP}, EOD {EOD_HOUR}:{EOD_MINUTE:02d} ET bar,\n"
        f"//   initial_capital ${INIT_CAPITAL:,} (true-target Tradeify_Select_100K).\n"
        "// PREREG: docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md\n"
        "// ============================================================================\n"
    )
    _req(t, "margin_short=0)\n", "NAS margin_short")
    t = t.replace("margin_short=0)\n", "margin_short=0)\n" + banner, 1)

    futures_block = f"""
// ============================================================================
// FUTURES (MYM) — Q-TXG-1 sibling-swap
// ============================================================================
group_futures = "═══ FUTURES (MYM) ═══"
accountSize   = input.float({ACCOUNT}, "Account Size ($)", group=group_futures)
microCap      = input.int({MICRO_CAP}, "Micro Contract Cap", group=group_futures)
mymPointValue = input.float(0.50, "MYM $ per index point", group=group_futures)
forceFlat     = input.bool(true, "EOD Force-Flat (ET)", group=group_futures)

"""
    insert_at = (
        "// ============================================================================\n"
        "// BREAKOUT\n"
        "// ============================================================================\n"
    )
    _req(t, insert_at, "NAS breakout anchor")
    t = t.replace(insert_at, futures_block + insert_at, 1)

    # Research bypass toggles (defaults ON = lock-identical)
    old_sess = """// ============================================================================
// SESSION & DAY
// ============================================================================
currentHourUTC = hour(time, "UTC")
sessionOK      = currentHourUTC >= 13 and currentHourUTC < 17
"""
    new_sess = """// ============================================================================
// SESSION & DAY
// ============================================================================
// Research bypass toggles — defaults ON preserve locked Mon+Tue + 13-17 UTC.
group_session = "═══ SESSION & DAY ═══"
useSession    = input.bool(true, "Use Hour-of-Day Filter?", group=group_session,
     tooltip="ON = locked 13-17 UTC window + 3-bar session warmup. OFF = all hours (warmup bypassed). Default ON preserves lock.")
useDowFilter  = input.bool(true, "Use Day-of-Week Filter?", group=group_session,
     tooltip="ON = per-day Allow* toggles below. OFF = all days (Allow* ignored). Default ON preserves lock.")

currentHourUTC = hour(time, "UTC")
inSessionWindow = currentHourUTC >= 13 and currentHourUTC < 17
sessionOK      = useSession ? inSessionWindow : true
"""
    _req(t, old_sess, "NAS session block")
    t = t.replace(old_sess, new_sess, 1)

    old_dow = """currentDow = dayofweek(time, "UTC")
dowOK = (allowMon and currentDow == dayofweek.monday) or
     (allowTue and currentDow == dayofweek.tuesday) or
     (allowWed and currentDow == dayofweek.wednesday) or
     (allowThu and currentDow == dayofweek.thursday) or
     (allowFri and currentDow == dayofweek.friday)

var int barsSinceSessionStart = 0
sessionJustOpened = sessionOK and not (currentHourUTC[1] >= 13 and currentHourUTC[1] < 17)
if sessionJustOpened
    barsSinceSessionStart := 0
if sessionOK
    barsSinceSessionStart := barsSinceSessionStart + 1

warmupOK = barsSinceSessionStart > 3
"""
    new_dow = """currentDow = dayofweek(time, "UTC")
dowRaw = (allowMon and currentDow == dayofweek.monday) or
     (allowTue and currentDow == dayofweek.tuesday) or
     (allowWed and currentDow == dayofweek.wednesday) or
     (allowThu and currentDow == dayofweek.thursday) or
     (allowFri and currentDow == dayofweek.friday)
dowOK = useDowFilter ? dowRaw : true

var int barsSinceSessionStart = 0
// Warmup counter always tracks the locked window; gate only applies when useSession is ON.
sessionJustOpened = inSessionWindow and not (currentHourUTC[1] >= 13 and currentHourUTC[1] < 17)
if sessionJustOpened
    barsSinceSessionStart := 0
if inSessionWindow
    barsSinceSessionStart := barsSinceSessionStart + 1

warmupOK = useSession ? barsSinceSessionStart > 3 : true
"""
    _req(t, old_dow, "NAS dow/warmup")
    t = t.replace(old_dow, new_dow, 1)

    old_size = """// ============================================================================
// POSITION SIZING — rolling-equity (G2 verified 2026-05-04)
// ============================================================================
calcSize(stopDist) =>
    risk = strategy.equity * (riskPerTrade / 100)
    stopDist > 0 ? risk / stopDist : 0
"""
    new_size = """// ============================================================================
// POSITION SIZING — integer MYM, static account (research path; Q-TXG-1)
// ============================================================================
calcSize(stopDist) =>
    riskDollars = accountSize * (riskPerTrade / 100)
    perContract = stopDist * mymPointValue
    rawQty = perContract > 0 ? math.floor(riskDollars / perContract) : 0
    reserveCap = math.floor(microCap / (1 + pyramidSize / 100))
    math.min(rawQty, reserveCap)
"""
    _req(t, old_size, "NAS calcSize")
    t = t.replace(old_size, new_size, 1)

    old_daily = """var int dailyTradeCount   = 0
var float strikerDayPnl   = 0.0
var bool strikerHaltedToday = false
var int prevClosedCount   = 0

if ta.change(time("D")) != 0
    dailyTradeCount     := 0
    strikerDayPnl       := 0.0
    strikerHaltedToday  := false
"""
    new_daily = """var int dailyTradeCount   = 0
var float strikerDayPnl   = 0.0
var bool strikerHaltedToday = false
var bool eodHaltedToday   = false
var int prevClosedCount   = 0

if ta.change(time("D")) != 0
    dailyTradeCount     := 0
    strikerDayPnl       := 0.0
    strikerHaltedToday  := false
    eodHaltedToday      := false
"""
    _req(t, old_daily, "NAS daily vars")
    t = t.replace(old_daily, new_daily, 1)

    old_halt = """if not strikerHaltedToday and strikerDayPnl <= strategy.initial_capital * strikerDayStopPct / 100
    strikerHaltedToday := true

canTrade = not ddHit and strategy.opentrades == 0 and dailyTradeCount < maxDailyTrades and not strikerHaltedToday
"""
    new_halt = f"""if not strikerHaltedToday and strikerDayPnl <= strategy.initial_capital * strikerDayStopPct / 100
    strikerHaltedToday := true

// EOD force-flat (ET-pinned, DST-aware) — {EOD_HOUR}:{EOD_MINUTE:02d} bar → ~16:00 ET fill.
isEodBar = hour(time, "America/New_York") == {EOD_HOUR} and minute(time, "America/New_York") == {EOD_MINUTE}
if forceFlat and isEodBar
    strategy.close_all("EOD Flat")
    eodHaltedToday := true

canTrade = not ddHit and strategy.opentrades == 0 and dailyTradeCount < maxDailyTrades and not strikerHaltedToday and not eodHaltedToday
"""
    _req(t, old_halt, "NAS halt/canTrade")
    t = t.replace(old_halt, new_halt, 1)

    old_entry = """if longSignal and canTrade
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
"""
    new_entry = """flooredThisBar = false
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
"""
    _req(t, old_entry, "NAS entry")
    t = t.replace(old_entry, new_entry, 1)

    old_add = "        addSize = initialSize * (pyramidSize / 100)"
    new_add = "        addSize = math.floor(initialSize * (pyramidSize / 100))"
    _req(t, old_add, "NAS addSize")
    t = t.replace(old_add, new_add, 1)

    floor_viz = """
// ============================================================================
// FLOORING VISIBILITY (R9)
// ============================================================================
plotshape(flooredThisBar, "Floored", shape.xcross, location.abovebar, color.orange, size=size.tiny)
if flooredThisBar
    alert("Striker NAS100 MYM Q-TXG-1: qty floored to 0 (insufficient account/ATR headroom under RESERVE cap)", alert.freq_once_per_bar)

"""
    alerts_anchor = (
        "// ============================================================================\n"
        "// ALERTS\n"
        "// ============================================================================\n"
    )
    _req(t, alerts_anchor, "NAS alerts")
    t = t.replace(alerts_anchor, floor_viz + alerts_anchor, 1)

    t = t.replace("Striker NAS100 v1.0", "Striker NAS100 MYM Q-TXG-1")
    t = t.replace("STRIKER NAS100 v1.0", "STRIKER NAS100 MYM Q-TXG-1")
    return t


def port_dj30_to_mnq(dj: str) -> str:
    """DJ30 locked signal → MNQ venue mechanics (sibling-swap)."""
    t = dj

    old_hdr = """strategy("Striker DJ30 v4.5", overlay=true,
     initial_capital=200000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     commission_type=strategy.commission.cash_per_order,
     commission_value=0,
     slippage=2,"""
    new_hdr = f"""strategy("Striker DJ30 MNQ Q-TXG-1 PROTOTYPE", overlay=true,
     initial_capital={INIT_CAPITAL},
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     commission_type=strategy.commission.cash_per_contract,
     commission_value={COMMISSION},
     slippage=1,"""
    _req(t, old_hdr, "DJ30 header")
    t = t.replace(old_hdr, new_hdr, 1)

    banner = (
        "\n// ============================================================================\n"
        "// Q-TXG-1 SIBLING-SWAP PROTOTYPE — MNQ (2026-08-12)\n"
        "// Source: striker_dj30_v4.5.pine (LOCKED). Parameter-axis LOCKED.\n"
        "// Cross-underlying research port: DJ30 breakout logic on CME MNQ.\n"
        "// NOT the WITHDRAWN(F1) striker×MYM redeploy. Venue deltas only:\n"
        f"//   integer MNQ sizing + RESERVE cap, EOD force-flat ET, costs\n"
        f"//   ${COMMISSION}/side (Tradeify Select), accountSize ${ACCOUNT:,},\n"
        f"//   microCap {MICRO_CAP}, EOD {EOD_HOUR}:{EOD_MINUTE:02d} ET bar,\n"
        f"//   initial_capital ${INIT_CAPITAL:,} (true-target Tradeify_Select_100K).\n"
        "// Day soft-stop stays LOCKED Pine default −2% (not live TV −1.15%).\n"
        "// PREREG: docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md\n"
        "// ============================================================================\n"
    )
    _req(t, "margin_short=0)\n", "DJ30 margin_short")
    t = t.replace("margin_short=0)\n", "margin_short=0)\n" + banner, 1)

    # Insert futures block after maxDailyTrades / day soft-stop inputs (before BREAKOUT).
    futures_block = f"""
// ============================================================================
// FUTURES (MNQ) — Q-TXG-1 sibling-swap
// ============================================================================
group_futures = "═══ FUTURES (MNQ) ═══"
accountSize   = input.float({ACCOUNT}, "Account Size ($)", group=group_futures)
microCap      = input.int({MICRO_CAP}, "Micro Contract Cap", group=group_futures)
mnqPointValue = input.float(2.00, "MNQ $ per index point", group=group_futures)
forceFlat     = input.bool(true, "EOD Force-Flat (ET)", group=group_futures)

"""
    # DJ30 locked places BREAKOUT after risk inputs — find unique anchor near day-stop end.
    insert_at = (
        "// ============================================================================\n"
        "// BREAKOUT\n"
        "// ============================================================================\n"
    )
    _req(t, insert_at, "DJ30 breakout anchor")
    t = t.replace(insert_at, futures_block + insert_at, 1)

    old_sess = """// ============================================================================
// SESSION & DAY
// ============================================================================
currentHourUTC = hour(time, "UTC")
sessionOK      = currentHourUTC >= 13 and currentHourUTC < 17

currentDow     = dayofweek(time, "UTC")
dowOK          = currentDow == dayofweek.tuesday or currentDow == dayofweek.friday

var int barsSinceSessionStart = 0
sessionJustOpened = sessionOK and not (currentHourUTC[1] >= 13 and currentHourUTC[1] < 17)
if sessionJustOpened
    barsSinceSessionStart := 0
if sessionOK
    barsSinceSessionStart := barsSinceSessionStart + 1

warmupOK = barsSinceSessionStart > 3
"""
    new_sess = """// ============================================================================
// SESSION & DAY
// ============================================================================
// Research bypass toggles — defaults ON preserve locked Tue/Fri + 13-17 UTC.
group_session  = "═══ SESSION & DAY ═══"
useSession     = input.bool(true, "Use Hour-of-Day Filter?", group=group_session,
     tooltip="ON = locked 13-17 UTC window + 3-bar session warmup. OFF = all hours (warmup bypassed). Default ON preserves lock.")
useDowFilter   = input.bool(true, "Use Day-of-Week Filter?", group=group_session,
     tooltip="ON = locked Tue+Fri only. OFF = all days. Default ON preserves lock.")

currentHourUTC = hour(time, "UTC")
inSessionWindow = currentHourUTC >= 13 and currentHourUTC < 17
sessionOK      = useSession ? inSessionWindow : true

currentDow     = dayofweek(time, "UTC")
dowRaw         = currentDow == dayofweek.tuesday or currentDow == dayofweek.friday
dowOK          = useDowFilter ? dowRaw : true

var int barsSinceSessionStart = 0
// Warmup counter always tracks the locked window; gate only applies when useSession is ON.
sessionJustOpened = inSessionWindow and not (currentHourUTC[1] >= 13 and currentHourUTC[1] < 17)
if sessionJustOpened
    barsSinceSessionStart := 0
if inSessionWindow
    barsSinceSessionStart := barsSinceSessionStart + 1

warmupOK = useSession ? barsSinceSessionStart > 3 : true
"""
    _req(t, old_sess, "DJ30 session")
    t = t.replace(old_sess, new_sess, 1)

    old_size = """// ============================================================================
// POSITION SIZING — rolling-equity (G2 verified 2026-05-04)
// ============================================================================
calcSize(stopDist) =>
    risk = strategy.equity * (riskPerTrade / 100)
    stopDist > 0 ? risk / stopDist : 0
"""
    # DJ30 may have slightly different sizing comment — try both.
    if old_size not in t:
        old_size = """calcSize(stopDist) =>
    risk = strategy.equity * (riskPerTrade / 100)
    stopDist > 0 ? risk / stopDist : 0
"""
        new_size = """// POSITION SIZING — integer MNQ, static account (research path; Q-TXG-1)
calcSize(stopDist) =>
    riskDollars = accountSize * (riskPerTrade / 100)
    perContract = stopDist * mnqPointValue
    rawQty = perContract > 0 ? math.floor(riskDollars / perContract) : 0
    reserveCap = math.floor(microCap / (1 + pyramidSize / 100))
    math.min(rawQty, reserveCap)
"""
    else:
        new_size = """// ============================================================================
// POSITION SIZING — integer MNQ, static account (research path; Q-TXG-1)
// ============================================================================
calcSize(stopDist) =>
    riskDollars = accountSize * (riskPerTrade / 100)
    perContract = stopDist * mnqPointValue
    rawQty = perContract > 0 ? math.floor(riskDollars / perContract) : 0
    reserveCap = math.floor(microCap / (1 + pyramidSize / 100))
    math.min(rawQty, reserveCap)
"""
    _req(t, old_size, "DJ30 calcSize")
    t = t.replace(old_size, new_size, 1)

    old_daily = """var int dailyTradeCount   = 0
var float strikerDayPnl   = 0.0
var bool strikerHaltedToday = false
var int prevClosedCount   = 0

if ta.change(time("D")) != 0
    dailyTradeCount     := 0
    strikerDayPnl       := 0.0
    strikerHaltedToday  := false
"""
    new_daily = """var int dailyTradeCount   = 0
var float strikerDayPnl   = 0.0
var bool strikerHaltedToday = false
var bool eodHaltedToday   = false
var int prevClosedCount   = 0

if ta.change(time("D")) != 0
    dailyTradeCount     := 0
    strikerDayPnl       := 0.0
    strikerHaltedToday  := false
    eodHaltedToday      := false
"""
    _req(t, old_daily, "DJ30 daily vars")
    t = t.replace(old_daily, new_daily, 1)

    old_halt = """if not strikerHaltedToday and strikerDayPnl <= strategy.initial_capital * strikerDayStopPct / 100
    strikerHaltedToday := true

canTrade = not ddHit and strategy.opentrades == 0 and dailyTradeCount < maxDailyTrades and not strikerHaltedToday
"""
    new_halt = f"""if not strikerHaltedToday and strikerDayPnl <= strategy.initial_capital * strikerDayStopPct / 100
    strikerHaltedToday := true

// EOD force-flat (ET-pinned, DST-aware) — {EOD_HOUR}:{EOD_MINUTE:02d} bar → ~16:00 ET fill.
isEodBar = hour(time, "America/New_York") == {EOD_HOUR} and minute(time, "America/New_York") == {EOD_MINUTE}
if forceFlat and isEodBar
    strategy.close_all("EOD Flat")
    eodHaltedToday := true

canTrade = not ddHit and strategy.opentrades == 0 and dailyTradeCount < maxDailyTrades and not strikerHaltedToday and not eodHaltedToday
"""
    _req(t, old_halt, "DJ30 halt/canTrade")
    t = t.replace(old_halt, new_halt, 1)

    old_entry = """if longSignal and canTrade
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
"""
    new_entry = """flooredThisBar = false
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
"""
    _req(t, old_entry, "DJ30 entry")
    t = t.replace(old_entry, new_entry, 1)

    old_add = "        addSize = initialSize * (pyramidSize / 100)"
    new_add = "        addSize = math.floor(initialSize * (pyramidSize / 100))"
    _req(t, old_add, "DJ30 addSize")
    t = t.replace(old_add, new_add, 1)

    floor_viz = """
// ============================================================================
// FLOORING VISIBILITY (R9)
// ============================================================================
plotshape(flooredThisBar, "Floored", shape.xcross, location.abovebar, color.orange, size=size.tiny)
if flooredThisBar
    alert("Striker DJ30 MNQ Q-TXG-1: qty floored to 0 (insufficient account/ATR headroom under RESERVE cap)", alert.freq_once_per_bar)

"""
    alerts_anchor = (
        "// ============================================================================\n"
        "// ALERTS\n"
        "// ============================================================================\n"
    )
    _req(t, alerts_anchor, "DJ30 alerts")
    t = t.replace(alerts_anchor, floor_viz + alerts_anchor, 1)

    t = t.replace("Striker DJ30 v4.5", "Striker DJ30 MNQ Q-TXG-1")
    t = t.replace("STRIKER DJ30 v4.5", "STRIKER DJ30 MNQ Q-TXG-1")
    return t


def main() -> None:
    nas_src = PRIMARY / "nas/striker_nas100_v1.pine"
    dj_src = PRIMARY / "striker/striker_dj30_v4.5.pine"
    if not nas_src.is_file() or not dj_src.is_file():
        raise SystemExit(
            f"locked Pine missing on primary checkout:\n  {nas_src}\n  {dj_src}"
        )

    out_nas = OUT_NAS / "striker_nas100_v1_mym_qtxg1_prototype.pine"
    out_dj = OUT_STR / "striker_dj30_v4.5_mnq_qtxg1_prototype.pine"
    OUT_NAS.mkdir(parents=True, exist_ok=True)
    OUT_STR.mkdir(parents=True, exist_ok=True)

    nas_out = port_nas_to_mym(nas_src.read_text(encoding="utf-8"))
    dj_out = port_dj30_to_mnq(dj_src.read_text(encoding="utf-8"))

    # LF endings (match venue-edition convention)
    nas_bytes = nas_out.replace("\r\n", "\n").encode("utf-8")
    dj_bytes = dj_out.replace("\r\n", "\n").encode("utf-8")
    out_nas.write_bytes(nas_bytes)
    out_dj.write_bytes(dj_bytes)

    report = {
        "nas_mym": {
            "path": str(out_nas.relative_to(WT)).replace("\\", "/"),
            "sha256": sha256_bytes(nas_bytes),
            "bytes": len(nas_bytes),
            "src_sha256": sha256_bytes(nas_src.read_bytes()),
        },
        "dj30_mnq": {
            "path": str(out_dj.relative_to(WT)).replace("\\", "/"),
            "sha256": sha256_bytes(dj_bytes),
            "bytes": len(dj_bytes),
            "src_sha256": sha256_bytes(dj_src.read_bytes()),
        },
    }
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
