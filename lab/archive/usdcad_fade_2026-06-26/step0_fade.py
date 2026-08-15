"""Step-0 panel-integrity battery for the USDCAD up-spike-fade study.

Tailored to BAR_EXPORT v0.1 (Signal column = epoch_ms|o|h|l|c|v, epoch in UTC).
Mandatory before ANY strategy metric (strategy-validation skill §1). Reuses the
triple-audited decode regex from the 2026-06-14 harness so the bytes that feed
the fade simulator are exactly the bytes we integrity-check here.

Exit code 0 = pass (warnings allowed); 2 = hard fail (do NOT compute metrics).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PIP = 1e-4
ET = "America/New_York"
SIGNAL_PIPE_RE = re.compile(
    r"^(?P<e>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)$"
)
DEFAULT_CSV = Path(
    r"C:\Users\joshu\Downloads\BAR_EXPORT_v0.1_PEPPERSTONE_USDCAD_2026-06-26_422ca.csv"
)


def decode(path: Path):
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    e = raw[raw["Type"].astype(str).str.startswith("Entry")]
    n_entry = len(e)
    recs, fails = [], 0
    for sig in e["Signal"].astype(str):
        m = SIGNAL_PIPE_RE.match(sig.strip())
        if m:
            recs.append((int(m.group("e")), float(m.group("o")), float(m.group("h")),
                         float(m.group("l")), float(m.group("c")), int(m.group("v"))))
        else:
            fails += 1
    df = pd.DataFrame(recs, columns=["e", "o", "h", "l", "c", "v"]).sort_values("e")
    df = df.reset_index(drop=True)
    return df, n_entry, fails


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    print(f"=== Step-0 panel integrity: {path.name} ===\n")
    hard, warn = [], []

    df, n_entry, fails = decode(path)
    n = len(df)
    print(f"entry rows           : {n_entry:,}")
    print(f"decoded bars         : {n:,}")
    print(f"decode failures      : {fails}")
    if fails:
        hard.append(f"{fails} Signal cells failed to decode")
    if n < 1000:
        hard.append(f"only {n} bars decoded")

    # (1) epoch monotonic + unique
    de = np.diff(df["e"].to_numpy())
    n_dup = int((de == 0).sum())
    n_back = int((de < 0).sum())
    print(f"duplicate epochs     : {n_dup}")
    print(f"backwards epochs     : {n_back}")
    if n_dup:
        hard.append(f"{n_dup} duplicate epochs")
    if n_back:
        hard.append(f"{n_back} non-monotonic epochs")

    # (2) 15-min spacing census (FX trades 24x5; weekend/holiday gaps expected)
    step = 15 * 60 * 1000
    n_contig = int((de == step).sum())
    n_gap = int((de > step).sum())
    pct_contig = 100.0 * n_contig / max(1, len(de))
    print(f"15-min contiguous    : {n_contig:,} ({pct_contig:.1f}% of steps)")
    print(f"gaps (> 15min)       : {n_gap:,}  (weekend/holiday breaks)")
    odd = int(((de != step) & (de > 0) & (de % step != 0)).sum())
    print(f"non-15min-multiple Δ : {odd}")
    if odd > n * 0.001:
        hard.append(f"{odd} gaps are not multiples of 15min (timeframe inconsistent)")
    elif odd:
        warn.append(f"{odd} small non-15min Δ (likely DST/holiday seams)")

    # (3) OHLC sanity
    o, h, l, c = (df[k].to_numpy(float) for k in ("o", "h", "l", "c"))
    bad_hl = int((h < l).sum())
    bad_h = int((h < np.maximum(o, c) - 1e-9).sum())
    bad_l = int((l > np.minimum(o, c) + 1e-9).sum())
    print(f"high<low             : {bad_hl}")
    print(f"high<max(o,c)        : {bad_h}")
    print(f"low>min(o,c)         : {bad_l}")
    for label, cnt in [("high<low", bad_hl), ("high<max(o,c)", bad_h), ("low>min(o,c)", bad_l)]:
        if cnt:
            hard.append(f"{cnt} bars violate OHLC ({label})")

    # (4) span + UTC→ET DST-aware decode sanity
    t_utc = pd.to_datetime(df["e"], unit="ms", utc=True)
    t_et = t_utc.dt.tz_convert(ET)
    print(f"\nspan (UTC)           : {t_utc.iloc[0]} -> {t_utc.iloc[-1]}")
    print(f"span (ET)            : {t_et.iloc[0]} -> {t_et.iloc[-1]}")
    years = sorted(t_et.dt.year.unique())
    print(f"years covered        : {years}")
    if len(years) < 5:
        warn.append(f"only {len(years)} calendar years (expected multi-regime 2020-2026)")

    # ET intraday activity: bar range by ET hour should peak NY-morning (08-11) if
    # the UTC->ET conversion is correct (durable #8: ET 08-11 range ~3x overnight).
    rng = (h - l) / PIP
    by_hr = pd.Series(rng).groupby(t_et.dt.hour.to_numpy()).mean()
    peak_hr = int(by_hr.idxmax())
    ny_morning = by_hr.loc[8:11].mean()
    overnight = by_hr.loc[0:5].mean()
    print(f"\nbar-range by ET hour (pips), peak hour = {peak_hr:02d}:00, "
          f"NY-morn/overnight = {ny_morning/max(overnight,1e-9):.2f}x")
    print(by_hr.round(2).to_string())
    if not (7 <= peak_hr <= 11):
        warn.append(f"activity peaks at ET {peak_hr:02d}:00, not NY-morning — TZ decode suspect")

    # weekend-gap DST tracer: the largest gaps should be Fri->Sun opens; print a few
    gi = np.argsort(de)[-3:]
    print("\nlargest gaps (weekend opens, ET):")
    for i in sorted(gi):
        print(f"  {t_et.iloc[i]}  ->  {t_et.iloc[i+1]}   (Δ {de[i]/3600000:.1f}h)")

    # ---- verdict
    print("\n" + "=" * 48)
    if warn:
        print("WARNINGS:")
        for w in warn:
            print(f"  ! {w}")
    if hard:
        print("HARD FAILURES (do NOT compute metrics):")
        for hf in hard:
            print(f"  X {hf}")
        print("\nSTEP-0: FAIL")
        sys.exit(2)
    print("STEP-0: PASS" + ("  (with warnings)" if warn else ""))
    sys.exit(0)


if __name__ == "__main__":
    main()
