"""NG-EIA-1 -- weekly Natural Gas Storage Report event calendar, 2019-01 -> 2026-07.

Source: ir.eia.gov/ngs/ngs.html + ir.eia.gov/ngs/schedule.html (WebFetch-verified this
session -- brief §0). Standard release: Thursday 10:30am ET. Holiday-week exceptions are
NON-UNIFORM (unlike F-B/CL's simple Wed->Thu shift): New Year's/Veterans Day -> Friday
10:30am; National Day of Mourning/Juneteenth/Thanksgiving -> Wednesday 12:00pm; Christmas
-> Monday 12:00pm. The EIA's own published exception table only documents 2025-2026 --
the historical (2019-2024) pattern is NOT confirmed from session sources.

Per the brief §5 forbidden-move discipline: DO NOT guess the historical shift day.
PRIMARY cohort = every Thursday 10:30 ET in the window, MINUS any week containing a US
federal holiday Monday-Thursday (dropped entirely -- conservative, trades N for dating
certainty). SECONDARY (non-gating) = a best-effort shift applied using the CONFIRMED
2025-2026 exception pattern, reported for comparison only, never gating.
"""
from __future__ import annotations

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar

ET = "America/New_York"

# Confirmed exception mapping (ir.eia.gov/ngs/schedule.html, 2025-2026 only).
# Keyed by the pandas USFederalHolidayCalendar holiday names that appear in
# Mon-Thu of the report week; used ONLY for the SECONDARY reconstruction.
SHIFT_TO_FRIDAY = {"New Year's Day", "Veterans Day"}
SHIFT_TO_WED_NOON = {"Juneteenth National Independence Day", "Thanksgiving Day"}
SHIFT_TO_MON_NOON = {"Christmas Day"}
# "National Day of Mourning" is not a standing USFederalHolidayCalendar entry
# (it was a one-off 2025 designation) -- not modeled; any week it fell in is
# already dropped from PRIMARY as a holiday-adjacent week regardless.


def primary_thursdays(start="2019-01-01", end="2026-07-15") -> list[str]:
    """Every Thursday 10:30 ET in [start,end], MINUS weeks with a Mon-Thu US federal
    holiday (dropped entirely -- the brief's required conservative discipline)."""
    cal = USFederalHolidayCalendar()
    hols = cal.holidays(start=pd.Timestamp(start) - pd.Timedelta(days=7),
                         end=pd.Timestamp(end) + pd.Timedelta(days=7))
    hol_set = set(hols.normalize())
    thursdays = pd.date_range(start, end, freq="W-THU")
    out = []
    for th in thursdays:
        mon = th - pd.Timedelta(days=3)
        week_mon_thu = {mon, mon + pd.Timedelta(days=1), mon + pd.Timedelta(days=2), th}
        if week_mon_thu & hol_set:
            continue  # ambiguous week -- dropped from PRIMARY
        out.append(th.strftime("%Y-%m-%d"))
    return out


def secondary_shifted(start="2019-01-01", end="2026-07-15") -> list[tuple[str, str]]:
    """Best-effort reconstruction applying the CONFIRMED 2025-2026 shift pattern to
    every holiday-ambiguous week. Returns (date, time) tuples; NON-GATING, informational
    only (brief §3/§5) -- the historical shift pattern is not confirmed pre-2025."""
    cal = USFederalHolidayCalendar()
    hols = cal.holidays(start=pd.Timestamp(start) - pd.Timedelta(days=7),
                         end=pd.Timestamp(end) + pd.Timedelta(days=7))
    hol_series = pd.Series(hols.normalize(), index=hols.normalize())
    thursdays = pd.date_range(start, end, freq="W-THU")
    out = []
    for th in thursdays:
        mon = th - pd.Timedelta(days=3)
        week = [mon, mon + pd.Timedelta(days=1), mon + pd.Timedelta(days=2), th]
        hol_this_week = None
        for d in week:
            if d.normalize() in hol_series.index:
                name = cal.holidays(start=d, end=d, return_name=True)
                if len(name):
                    hol_this_week = str(name.iloc[0])
                break
        if hol_this_week is None:
            out.append((th.strftime("%Y-%m-%d"), "10:30"))
        elif hol_this_week in SHIFT_TO_FRIDAY:
            out.append(((th + pd.Timedelta(days=1)).strftime("%Y-%m-%d"), "10:30"))
        elif hol_this_week in SHIFT_TO_WED_NOON:
            out.append(((th - pd.Timedelta(days=1)).strftime("%Y-%m-%d"), "12:00"))
        elif hol_this_week in SHIFT_TO_MON_NOON:
            out.append((mon.strftime("%Y-%m-%d"), "12:00"))
        else:
            continue  # unmapped holiday type -- drop (same as PRIMARY)
    return out


if __name__ == "__main__":
    p = primary_thursdays()
    s = secondary_shifted()
    print(f"PRIMARY (holiday weeks dropped): {len(p)} events")
    print(f"SECONDARY (best-effort shifted): {len(s)} events")
    print(f"Dropped from PRIMARY: {round((len(s) - len(p)) / len(s) * 100, 1)}% "
          f"of the secondary-reconstructed count")
