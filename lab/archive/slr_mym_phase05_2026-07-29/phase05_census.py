"""SLR-MYM-1 Phase 0.5 — FREE event-rate bound on the local MYM 15m panel.

NOT a measurement of the 1m mechanism. A 15m bar cannot resolve a sweep and reclaim
inside itself, so this is a BOUND with undetermined bias direction. Its job is to
answer one question cheaply: can ANY S5-compliant day set reach the pre-registered
IS-partition floor of 120 entries?

Reads the primary checkout (vendor data is gitignored; absent from worktrees).
Zero outcomes examined -- entry COUNTS only. Consumes no K.
"""
import pandas as pd
import numpy as np

PANEL = r"C:\Users\joshu\multi_firm_operations\core\data\bar_data\MYM_M15.csv"

df = pd.read_csv(PANEL, parse_dates=["time"])
df["time"] = pd.to_datetime(df["time"], utc=True)
# Panel meta declares America/Chicago; convert to ET for all session logic.
df["et"] = df["time"].dt.tz_convert("America/New_York")
df = df.set_index("et").sort_index()

df["date"] = df.index.date
df["tod"] = df.index.time
df["dow"] = df.index.dayofweek  # 0=Mon

RTH_START, RTH_END = pd.Timestamp("09:30").time(), pd.Timestamp("16:00").time()
rth = df[(df.tod >= RTH_START) & (df.tod < RTH_END)]

# ---- daily RTH bars -------------------------------------------------------
daily = rth.groupby("date").agg(
    o=("open", "first"), h=("high", "max"), l=("low", "min"),
    c=("close", "last"), n=("close", "size")
)
daily = daily[daily.n >= 20]                      # drop half/holiday sessions
daily.index = pd.to_datetime(daily.index)
daily["dow"] = daily.index.dayofweek

# ---- overnight low (18:00 ET prior day -> 09:29 ET) -----------------------
df["sess"] = df.index.to_series().apply(lambda t: (t + pd.Timedelta(hours=6)).date())
on = df[(df.tod >= pd.Timestamp("18:00").time()) | (df.tod < RTH_START)]
on_low = on.groupby("sess")["low"].min()
on_low.index = pd.to_datetime(on_low.index)

# ---- vStruct: close vs EMA(20), PRIOR completed bar (non-repaint) ---------
daily["ema20"] = daily["c"].ewm(span=20, adjust=False).mean()
daily["vstruct_d"] = (daily["c"] > daily["ema20"]).shift(1)      # prior close

wk = daily.resample("W-FRI").agg(c=("c", "last"), l=("l", "min"))
wk["ema20"] = wk["c"].ewm(span=20, adjust=False).mean()
wk["vstruct_w"] = (wk["c"] > wk["ema20"]).shift(1)
wk["pw_low"] = wk["l"].shift(1)

daily["vstruct_w"] = wk["vstruct_w"].reindex(daily.index, method="ffill")
daily["pw_low"] = wk["pw_low"].reindex(daily.index, method="ffill")
daily["pd_low"] = daily["l"].shift(1)
daily["on_low"] = on_low.reindex(daily.index)

# ---- ATR(14) on RTH daily, as of PRIOR close -----------------------------
pc = daily["c"].shift(1)
tr = pd.concat([daily.h - daily.l, (daily.h - pc).abs(), (daily.l - pc).abs()], axis=1).max(axis=1)
daily["atr14"] = tr.rolling(14).mean().shift(1)

# ---- the §1 conditioning stack -------------------------------------------
d = daily.dropna(subset=["vstruct_w", "vstruct_d", "atr14", "pd_low", "on_low"]).copy()

d["aligned"] = d.vstruct_w.astype(bool) & d.vstruct_d.astype(bool)

lv = d[["pd_low", "on_low", "pw_low"]]
below = lv.where(lv.lt(d.o, axis=0))                 # strictly below the 09:30 open
d["armed"] = below.max(axis=1)                        # NEAREST below = highest of them
d["has_level"] = d.armed.notna()
d["reachable"] = (d.o - d.armed) <= d.atr14           # 1x ATR reachability cap

# sweep proxy: RTH session low pierced the armed level.
# 15m LIMIT: cannot time the sweep to 09:30-10:00 -- so this OVERSTATES the sweep
# rate (a 14:00 pierce counts here, but would not arm the real 09:30-10:00 rule).
d["swept"] = d.l < d.armed
# reclaim proxy: session closed back above the armed level.
d["reclaimed"] = d.c > d.armed

d["entry"] = d.aligned & d.has_level & d.reachable & d.swept & d.reclaimed

IS_END = pd.Timestamp("2023-12-31")
is_ = d[d.index <= IS_END]

def rate(x, col="entry"):
    return float(x[col].mean()) if len(x) else float("nan")

print("=" * 74)
print("SLR-MYM-1 PHASE 0.5 -- free event-rate BOUND (15m proxy, NOT a 1m measurement)")
print("=" * 74)
print(f"panel span      : {d.index.min().date()} -> {d.index.max().date()}")
print(f"scoreable sess. : {len(d)}   (IS <=2023-12-31: {len(is_)}, {len(is_)/len(d):.1%})")
print()
print("--- conditioning stack, full panel (each is CUMULATIVE) ---")
for label, mask in [
    ("weekly+daily vStruct bullish", d.aligned),
    ("+ a level below the open", d.aligned & d.has_level),
    ("+ within 1x ATR", d.aligned & d.has_level & d.reachable),
    ("+ swept", d.aligned & d.has_level & d.reachable & d.swept),
    ("+ reclaimed  = ENTRY", d.entry),
]:
    print(f"  {label:<34} {mask.mean():6.2%}   n={int(mask.sum()):5d}")

print()
print(f"full-panel entry rate : {rate(d):.2%}   entries={int(d.entry.sum())}")
print(f"IS-partition rate     : {rate(is_):.2%}   entries={int(is_.entry.sum())}")

DOW = ["Mon", "Tue", "Wed", "Thu", "Fri"]
print()
print("--- per weekday (IS partition = what §6 Stage 1 actually gates on) ---")
print(f"{'day':<5}{'sessions':>9}{'entries':>9}{'rate':>8}{'% of entries':>14}{'free cap':>10}")
CAP = {0: 69, 1: 0, 2: 80, 3: 80, 4: 11}
tot = int(is_.entry.sum())
per = {}
for i, nm in enumerate(DOW):
    sub = is_[is_.dow == i]
    e = int(sub.entry.sum())
    per[i] = e
    print(f"{nm:<5}{len(sub):>9}{e:>9}{rate(sub):>8.1%}{(e/tot if tot else 0):>13.1%}{CAP[i]:>10}")

print()
print("--- S5-compliant day sets vs the pre-registered IS floor of 120 ---")
SETS = [
    ("Wed+Thu (spec Slot 1)", [2, 3]),
    ("Mon+Wed+Thu", [0, 2, 3]),
    ("Mon+Wed+Thu+Fri", [0, 2, 3, 4]),
    ("all-but-Tue", [0, 2, 3, 4]),
    ("ALL 5 (S5-NONCOMPLIANT)", [0, 1, 2, 3, 4]),
]
seen = set()
for nm, days in SETS:
    k = tuple(sorted(days))
    if k in seen and "NONCOMP" not in nm:
        continue
    seen.add(k)
    n = sum(per[x] for x in days)
    ok = "CLEARS" if n >= 120 else "**BELOW FLOOR**"
    print(f"  {nm:<26} IS entries={n:>4}   {ok}")

print()
print("NOTE: the sweep proxy is DELIBERATELY LOOSE (any-time-of-day pierce), so these")
print("counts are an UPPER bound on the real 09:30-10:00 rule. The true 1m numbers are")
print("lower, not higher -- a day set below the floor here cannot clear it on 1m data.")
