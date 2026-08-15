# NAS100 ORB Filters — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add toggleable day-of-week + hour-block (ET) filters to the NAS100 ORB research harness and a parity Pine strategy file, defaulting OFF so current behavior is preserved.

**Architecture:** Filters live on the exit-at-close engine `orb_lib.orb_backtest` (two new kwargs + `entry_tod` in the output). A thin CLI runner exposes them. A v6 Pine strategy mirrors the engine with `input.bool` toggles gated in ET. C1 (scan-next-eligible) for hour-blocks. No core/lock/allocation/dd_protection change.

**Tech Stack:** Python 3 / numpy / pandas / pytest; Pine Script v6; `scripts/pine_check.py` compile gate.

**Commit policy:** This repo commits only on Joshua's go-ahead. Treat the `git commit` steps as ready-to-run but batch them until he approves; the `.pine` is gitignored (won't stage). Spec: [`2026-06-24-nas100-orb-filters-design.md`](2026-06-24-nas100-orb-filters-design.md).

---

### Task 1: Harness filters on `orb_backtest`

**Files:**
- Modify: `lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py` (`orb_backtest`, ~line 241)
- Test: `lab/analysis/orb/orb_universe_2026-06-22/test_orb_filters.py` (create)

- [ ] **Step 1: Write the failing tests (synthetic fixture — no vendor data)**

```python
# test_orb_filters.py
import datetime as dt
import numpy as np
import pandas as pd
import orb_lib as L

TODS = [570, 585, 600, 615, 630, 645, 660]  # 09:30..11:00 ET, 15m
DAYS = [dt.date(2026, 6, d) for d in (1, 2, 3, 4, 5)]  # Mon..Fri
DOW = [0, 1, 2, 3, 4]

def _fixture():
    """5 identical days: OR(09:30/09:45)=[99,101]; clean up-break that persists
    through 11:00; flat at close. First breakout bar = 600 (10:00 ET)."""
    bars = {  # tod -> (o, h, l, c)
        570: (100, 101, 99, 100), 585: (100, 101, 99, 100),
        600: (101, 103, 101, 103), 615: (103, 104, 103, 104),
        630: (104, 105, 104, 105), 645: (105, 106, 105, 106),
        660: (106, 107, 106, 107),
    }
    piv = {f: pd.DataFrame(index=DAYS, columns=TODS, dtype=float) for f in
           ("open", "high", "low", "close")}
    for tod, (o, h, l, c) in bars.items():
        for day in DAYS:
            piv["open"].loc[day, tod] = o; piv["high"].loc[day, tod] = h
            piv["low"].loc[day, tod] = l;  piv["close"].loc[day, tod] = c
    meta = pd.DataFrame(index=DAYS)
    meta["rth_close"] = 107.0
    meta["year"] = 2026
    meta["dow"] = DOW
    inst = L.Instrument("SYN", L.Path("x"), "bar_export", "Pepperstone",
                        tick=0.1, spread_pt=1.0, rt_cost_pt=0.0,
                        open_tod=570, close_tod=660)
    return piv, meta, inst

def test_defaults_unchanged():
    piv, meta, inst = _fixture()
    bt = L.orb_backtest(piv, meta, inst, or_bars=2)
    assert len(bt["R"]) == 5
    assert list(bt["side"]) == ["long"] * 5
    assert list(bt["entry_tod"]) == [600] * 5      # first breakout = 10:00
    np.testing.assert_allclose(bt["R"], [3.0] * 5)  # (107-101-0)/2

def test_dow_filter_monday_only():
    piv, meta, inst = _fixture()
    bt = L.orb_backtest(piv, meta, inst, or_bars=2, allowed_dows=frozenset({0}))
    assert len(bt["R"]) == 1
    assert list(bt["entry_tod"]) == [600]

def test_hour_block_unused_hour_noop():
    piv, meta, inst = _fixture()
    bt = L.orb_backtest(piv, meta, inst, or_bars=2, blocked_hours=frozenset({11}))
    assert list(bt["entry_tod"]) == [600] * 5      # first break already in hour 10

def test_hour_block_pushes_entry_to_eligible_bar():
    piv, meta, inst = _fixture()
    bt = L.orb_backtest(piv, meta, inst, or_bars=2, blocked_hours=frozenset({10}))
    assert list(bt["entry_tod"]) == [660] * 5      # only eligible rest bar = 11:00
    assert all((t // 60) != 10 for t in bt["entry_tod"])

def test_hour_block_all_eligible_blocked_no_trades():
    piv, meta, inst = _fixture()
    bt = L.orb_backtest(piv, meta, inst, or_bars=2, blocked_hours=frozenset({10, 11}))
    assert len(bt["R"]) == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd lab/analysis/orb/orb_universe_2026-06-22 && python -m pytest test_orb_filters.py -v`
Expected: FAIL — `orb_backtest() got an unexpected keyword argument 'allowed_dows'` (and `KeyError: 'entry_tod'` in `test_defaults_unchanged`).

- [ ] **Step 3: Add the kwargs + filter logic + `entry_tod`**

In `orb_lib.py`, change the signature (line ~241):
```python
def orb_backtest(piv, meta, inst: Instrument, *, or_bars=2, entry_slip_pt=0.0,
                 vol_filter=False, allowed_dows=None, blocked_hours=None):
```
Add `entry_tods = []` to the init list (line ~258):
```python
    Rs, years, sides, rngs, stops, entry_tods = [], [], [], [], [], []
```
At the top of `for day in c.index:` (line ~259), add the DOW gate:
```python
    for day in c.index:
        if allowed_dows is not None and int(meta.loc[day, "dow"]) not in allowed_dows:
            continue
        or_hi = h.loc[day, or_tods].max()
```
Replace the breakout-scan block (lines ~267-280) with the C1 + entry_t version:
```python
        side = None
        entry_t = None
        for t in rest_tods:
            if blocked_hours and (t // 60) in blocked_hours:
                continue
            bh, bl, bo = h.loc[day, t], l.loc[day, t], o.loc[day, t]
            if not np.isfinite(bh):
                continue
            up = bh >= or_hi
            dn = bl <= or_lo
            if up and dn:
                side = "long" if bo <= (or_hi + or_lo) / 2 else "short"
                entry_t = t; break
            if up:
                side = "long"; entry_t = t; break
            if dn:
                side = "short"; entry_t = t; break
        if side is None:
            continue
```
Add `entry_tods.append(entry_t)` next to the other appends (line ~295):
```python
        Rs.append((pnl - rt) / rng)
        years.append(meta.loc[day, "year"]); sides.append(side)
        rngs.append(rng); stops.append(bool(stopped)); entry_tods.append(entry_t)
```
Apply the `vol_filter` mask to `entry_tods` too (line ~300-302) and add it to the return dict (line ~303):
```python
    Rs = np.array(Rs); years = np.array(years); sides = np.array(sides)
    rngs = np.array(rngs); stops = np.array(stops, bool); entry_tods = np.array(entry_tods)
    if vol_filter and len(rngs):
        keep = rngs > np.median(rngs)
        Rs, years, sides, rngs, stops, entry_tods = (
            Rs[keep], years[keep], sides[keep], rngs[keep], stops[keep], entry_tods[keep])
    return {"R": Rs, "year": years, "side": sides, "range": rngs,
            "stopped": stops, "entry_tod": entry_tods}
```
Update the docstring to note: filters default off ⇒ parity; OR construction is never gated by `blocked_hours`; the stop/exit min/max over all `rest_tods` is the inherited approximation, unchanged.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd lab/analysis/orb/orb_universe_2026-06-22 && python -m pytest test_orb_filters.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit (on go-ahead)**

```bash
git add lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py lab/analysis/orb/orb_universe_2026-06-22/test_orb_filters.py
git commit -m "feat(orb): toggleable DOW + hour-block filters on orb_backtest (default off)"
```

---

### Task 2: CLI runner `nas100_orb_filtered.py`

**Files:**
- Create: `lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_filtered.py`

- [ ] **Step 1: Write the runner**

```python
"""Filtered ORB runner — flip DOW + hour-block filters and see the offline effect.

  python nas100_orb_filtered.py                      # no filter = baseline
  python nas100_orb_filtered.py --dow mon,tue        # Mon+Tue only
  python nas100_orb_filtered.py --block-hours 12,13  # block 12:xx,13:xx ET entries
"""
from __future__ import annotations
import argparse
import orb_lib as L

DOW = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inst", default="NAS100_pep")
    ap.add_argument("--or-bars", type=int, default=2)
    ap.add_argument("--dow", default="", help="comma list of mon,tue,wed,thu,fri")
    ap.add_argument("--block-hours", default="", help="comma list of ET hours to block")
    ap.add_argument("--risk-pct", type=float, default=0.40)
    args = ap.parse_args()

    allowed = frozenset(DOW[d.strip().lower()] for d in args.dow.split(",") if d.strip()) or None
    blocked = frozenset(int(x) for x in args.block_hours.split(",") if x.strip()) or None

    inst = L.INSTRUMENTS[args.inst]
    piv, meta = L.session_panel(L.load(inst), inst)
    bt = L.orb_backtest(piv, meta, inst, or_bars=args.or_bars,
                        allowed_dows=allowed, blocked_hours=blocked)
    s = L.summ(bt["R"], bt["year"])
    print(f"dow={sorted(allowed) if allowed else 'all'} "
          f"block_hours={sorted(blocked) if blocked else 'none'}")
    print(f"  n={s['n']} meanR={s['mean_R']:+.4f} t={s['t']:+.2f} WR={s['wr']:.3f} "
          f"PF={s['pf']:.3f} sumR={s['sumR']:+.1f} h1={s['h1']:+.4f} h2={s['h2']:+.4f}")
    mc = L.first_passage_mc(bt["R"], args.risk_pct / 100.0)
    print(f"  MC@{args.risk_pct:.2f}%: pass={mc['pass']:.3f} bust_static={mc['bust_static']:.3f} "
          f"bust_daily={mc['bust_daily']:.3f} timeout={mc['timeout']:.3f} "
          f"p99_dd={mc['p99_dd']:.4f} median_days={mc['median_days_to_pass']}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-run (skip-if-no-data is acceptable)**

Run: `cd lab/analysis/orb/orb_universe_2026-06-22 && python nas100_orb_filtered.py && python nas100_orb_filtered.py --dow mon,tue --block-hours 12,13`
Expected: a baseline line, then a filtered line with `n` ≤ baseline. (If the vendor CSV is missing locally, expect a load error — that's the known vendor-data gate, not a code bug; note it and move on.)

- [ ] **Step 3: Commit (on go-ahead)**

```bash
git add lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_filtered.py
git commit -m "feat(orb): nas100_orb_filtered CLI runner for DOW + hour-block toggles"
```

---

### Task 3: Pine strategy `nas100_orb_v0_1.pine`

**Files:**
- Create: `core/strategies/candidates/nas100_orb_v0_1.pine` (gitignored — local artifact)

**Sub-skill:** use `anthropic-skills:pinescript-v6` when writing this file; the load-bearing requirements are the inputs + the ET/DOW/hour-block gating below. Mechanism must mirror `orb_backtest`: touch-fill at the OR level, protective stop at the opposite OR extreme, flat at the session close, both sides. Known gotcha: cancel resting entry orders at session end (the v0.1 leak was resting-order persistence) and on blocked hours (C1).

- [ ] **Step 1: Write the Pine strategy**

```pinescript
//@version=6
// NAS100 ORB v0.1 — opening-range breakout, exit-at-close (offline-faithful engine).
// CANDIDATE (NO-GO/HOLD per ops/instruments/NAS100.md N5/N7). NOT a locked strategy.
// Mirrors lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py::orb_backtest
// (or_bars, both-sides, stop=opposite OR extreme, flat at RTH close). Filters DEFAULT OFF.
strategy("NAS100 ORB v0.1", overlay=true, calc_on_every_tick=false,
     process_orders_on_close=false, pyramiding=0, initial_capital=200000,
     default_qty_type=strategy.percent_of_equity, default_qty_value=100)

orBars     = input.int(2, "OR bars (15m)", minval=1)
tz         = "America/New_York"
sessOpenH  = input.int(9,  "Session open hour (ET)")
sessOpenM  = input.int(30, "Session open minute (ET)")
sessCloseH = input.int(16, "Session close hour (ET)")
sessCloseM = input.int(0,  "Session close minute (ET)")

useDowFilter = input.bool(false, "Filter by day-of-week", group="DOW filter")
tradeMon = input.bool(true, "Mon", group="DOW filter")
tradeTue = input.bool(true, "Tue", group="DOW filter")
tradeWed = input.bool(true, "Wed", group="DOW filter")
tradeThu = input.bool(true, "Thu", group="DOW filter")
tradeFri = input.bool(true, "Fri", group="DOW filter")

useHourBlock = input.bool(false, "Block entry hours (ET)", group="Hour-block")
blkH09 = input.bool(false, "Block 09:xx (OR window — no-op at OR=2)", group="Hour-block")
blkH10 = input.bool(false, "Block 10:xx", group="Hour-block")
blkH11 = input.bool(false, "Block 11:xx", group="Hour-block")
blkH12 = input.bool(false, "Block 12:xx", group="Hour-block")
blkH13 = input.bool(false, "Block 13:xx", group="Hour-block")
blkH14 = input.bool(false, "Block 14:xx", group="Hour-block")
blkH15 = input.bool(false, "Block 15:xx", group="Hour-block")

etH = hour(time, tz)
etM = minute(time, tz)
tod = etH * 60 + etM
openTod  = sessOpenH * 60 + sessOpenM
closeTod = sessCloseH * 60 + sessCloseM
inSession = tod >= openTod and tod < closeTod
newDay = ta.change(dayofmonth(time, tz)) != 0

dowOk = not useDowFilter or
     (dayofweek(time, tz) == dayofweek.monday    and tradeMon) or
     (dayofweek(time, tz) == dayofweek.tuesday   and tradeTue) or
     (dayofweek(time, tz) == dayofweek.wednesday and tradeWed) or
     (dayofweek(time, tz) == dayofweek.thursday  and tradeThu) or
     (dayofweek(time, tz) == dayofweek.friday    and tradeFri)

hourBlocked = useHourBlock and (
     (etH == 9 and blkH09) or (etH == 10 and blkH10) or (etH == 11 and blkH11) or
     (etH == 12 and blkH12) or (etH == 13 and blkH13) or (etH == 14 and blkH14) or
     (etH == 15 and blkH15))

var float orHi = na
var float orLo = na
var int   orCount = 0
var bool  tradedToday = false

if inSession and newDay
    orHi := high
    orLo := low
    orCount := 1
    tradedToday := false
else if inSession and orCount < orBars
    orHi := math.max(orHi, high)
    orLo := math.min(orLo, low)
    orCount += 1

orReady = inSession and orCount >= orBars
eligible = orReady and not tradedToday and dowOk and not hourBlocked and strategy.position_size == 0

if eligible
    strategy.entry("L", strategy.long,  stop=orHi)
    strategy.entry("S", strategy.short, stop=orLo)
else if (hourBlocked or not inSession) and strategy.position_size == 0
    strategy.cancel("L")
    strategy.cancel("S")

if strategy.position_size > 0
    strategy.exit("Lx", "L", stop=orLo)
    tradedToday := true
if strategy.position_size < 0
    strategy.exit("Sx", "S", stop=orHi)
    tradedToday := true

if not inSession and strategy.position_size != 0
    strategy.close_all("EOD")
```

- [ ] **Step 2: Compile-check (zero-auth gate)**

Run: `python scripts/pine_check.py core/strategies/candidates/nas100_orb_v0_1.pine`
Expected: compile OK / no errors. Fix any v6 syntax issues with the pinescript-v6 skill and re-run until clean.

- [ ] **Step 3: No commit (gitignored)**

The `.pine` will not stage (`**/*.pine` is gitignored — live-edge protection). It stays a local artifact; Joshua loads it into TradingView. Note this in the handoff.

---

### Task 4: Ledger disposition

**Files:**
- Modify: `ops/instruments/NAS100.md` (SESSION LOG, top of the list ~line 40)

- [ ] **Step 1: Append a dated SESSION LOG entry**

```markdown
- **2026-06-24 (ORB filters — tooling)** — Added toggleable **day-of-week** + **hour-block (ET)** filters to the exit-at-close ORB engine `orb_lib.orb_backtest` (`allowed_dows`, `blocked_hours`, + `entry_tod` in output; C1 scan-next-eligible; OR construction never gated), a CLI runner `nas100_orb_filtered.py`, and a parity Pine strategy `core/strategies/candidates/nas100_orb_v0_1.pine` (gitignored). **All filters default OFF ⇒ exact parity with current behavior** (5 synthetic-fixture pytests, incl. defaults-unchanged). These are the *reliable-offline* class per N5/N7 (day-level selection, touch-fill preserved). **No validation claim** — adding the capability only; a DOW/hour combo that *improves* the edge needs pre-registration + multiplicity correction (N6 best-of-K trap). No core/lock/allocation/dd_protection change. Disposition unchanged: ORB stays **NO-GO/HOLD**. Spec/plan: `docs/spec/2026-06-24-nas100-orb-filters-{design,plan}.md`. Pine numeric parity pending a Joshua TV export.
```

- [ ] **Step 2: Commit (on go-ahead)**

```bash
git add ops/instruments/NAS100.md docs/spec/2026-06-24-nas100-orb-filters-design.md docs/spec/2026-06-24-nas100-orb-filters-plan.md
git commit -m "docs(orb): NAS100 ledger disposition + design/plan for toggleable DOW + hour-block filters"
```

---

## Self-Review

**Spec coverage:** harness kwargs + `entry_tod` (Task 1) ✓; C1 hour-block (Task 1 Step 3) ✓; DOW master+per-day (Task 1 + Pine) ✓; runner (Task 2) ✓; Pine strategy-only with ET gating + default-off (Task 3) ✓; tests incl. defaults-parity (Task 1 Step 1) ✓; pine_check.py verification (Task 3 Step 2) ✓; ledger disposition, no-claim (Task 4) ✓; out-of-scope items untouched ✓.

**Placeholder scan:** none — all steps carry concrete code/commands.

**Type consistency:** `allowed_dows` / `blocked_hours` are `frozenset[int] | None` in the signature, tests, and runner; `entry_tod` returned as `np.array` and indexed by `// 60` consistently; DOW int codes (Mon=0..Fri=4) consistent between `meta["dow"]`, tests, and the runner's `DOW` map; Pine uses `dayofweek.monday..friday` constants (Pine's own enum) which is correct for the Pine side and independent of the Python int codes.
