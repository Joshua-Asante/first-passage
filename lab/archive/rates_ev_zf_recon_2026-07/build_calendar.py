"""RATES-EV-ZF-1 -- CPI+NFP event calendar, primary-sourced from bls.gov.

Source: bls.gov/schedule/{YYYY}/home.htm for YYYY in 2019..2026, browsed via
claude-in-chrome MCP this session (WebFetch 403s bls.gov -- memory
reference_bls_release_date_sourcing). NOT a first-Friday/mid-month heuristic
(brief §5 forbidden move) -- every date below is transcribed from the
"Employment Situation for <month>" / "Consumer Price Index for <month>" rows
on the actual per-year BLS schedule page.

2026-02-11 (Wed, not Fri) matches the memory's flagged shutdown-shift date --
corroborates the source. 2025 has a real gap, not a transcription error:
the government-shutdown lapse means the OCTOBER-reference-month release was
never published for EITHER series (confirmed by reading Nov/Dec 2025 pages --
September-data NFP appears on 2025-11-20, next NFP row is "for November 2025"
on 2025-12-16 -- no "for October 2025" row exists anywhere). Same gap for
CPI (August-data Sep-11, September-data delayed to Oct-24, next row is
"for November 2025" on Dec-18 -- no "for October 2025" CPI exists).
"""
from __future__ import annotations

NFP_DATES = [
    # 2019
    "2019-01-04", "2019-02-01", "2019-03-08", "2019-04-05", "2019-05-03", "2019-06-07",
    "2019-07-05", "2019-08-02", "2019-09-06", "2019-10-04", "2019-11-01", "2019-12-06",
    # 2020
    "2020-01-10", "2020-02-07", "2020-03-06", "2020-04-03", "2020-05-08", "2020-06-05",
    "2020-07-02", "2020-08-07", "2020-09-04", "2020-10-02", "2020-11-06", "2020-12-04",
    # 2021
    "2021-01-08", "2021-02-05", "2021-03-05", "2021-04-02", "2021-05-07", "2021-06-04",
    "2021-07-02", "2021-08-06", "2021-09-03", "2021-10-08", "2021-11-05", "2021-12-03",
    # 2022
    "2022-01-07", "2022-02-04", "2022-03-04", "2022-04-01", "2022-05-06", "2022-06-03",
    "2022-07-08", "2022-08-05", "2022-09-02", "2022-10-07", "2022-11-04", "2022-12-02",
    # 2023
    "2023-01-06", "2023-02-03", "2023-03-10", "2023-04-07", "2023-05-05", "2023-06-02",
    "2023-07-07", "2023-08-04", "2023-09-01", "2023-10-06", "2023-11-03", "2023-12-08",
    # 2024
    "2024-01-05", "2024-02-02", "2024-03-08", "2024-04-05", "2024-05-03", "2024-06-07",
    "2024-07-05", "2024-08-02", "2024-09-06", "2024-10-04", "2024-11-01", "2024-12-06",
    # 2025 -- shutdown gap: Sep-data delayed to 11-20; Oct-data NEVER published
    # (confirmed on the live BLS schedule -- next row after 11-20 is "for November
    # 2025" on 12-16, no "for October 2025" row exists at all).
    "2025-01-10", "2025-02-07", "2025-03-07", "2025-04-04", "2025-05-02", "2025-06-06",
    "2025-07-03", "2025-08-01", "2025-11-20", "2025-12-16",
    # 2026 (through the panel window; 02-11 is Wed not Fri -- shutdown catch-up,
    # matches memory reference_bls_release_date_sourcing's flagged date exactly)
    "2026-01-09", "2026-02-11", "2026-03-06", "2026-04-03", "2026-05-08", "2026-06-05",
    "2026-07-02",
]

CPI_DATES = [
    # 2019
    "2019-01-11", "2019-02-13", "2019-03-12", "2019-04-10", "2019-05-10", "2019-06-12",
    "2019-07-11", "2019-08-13", "2019-09-12", "2019-10-10", "2019-11-13", "2019-12-11",
    # 2020
    "2020-01-14", "2020-02-13", "2020-03-11", "2020-04-10", "2020-05-12", "2020-06-10",
    "2020-07-14", "2020-08-12", "2020-09-11", "2020-10-13", "2020-11-12", "2020-12-10",
    # 2021
    "2021-01-13", "2021-02-10", "2021-03-10", "2021-04-13", "2021-05-12", "2021-06-10",
    "2021-07-13", "2021-08-11", "2021-09-14", "2021-10-13", "2021-11-10", "2021-12-10",
    # 2022
    "2022-01-12", "2022-02-10", "2022-03-10", "2022-04-12", "2022-05-11", "2022-06-10",
    "2022-07-13", "2022-08-10", "2022-09-13", "2022-10-13", "2022-11-10", "2022-12-13",
    # 2023
    "2023-01-12", "2023-02-14", "2023-03-14", "2023-04-12", "2023-05-10", "2023-06-13",
    "2023-07-12", "2023-08-10", "2023-09-13", "2023-10-12", "2023-11-14", "2023-12-12",
    # 2024
    "2024-01-11", "2024-02-13", "2024-03-12", "2024-04-10", "2024-05-15", "2024-06-12",
    "2024-07-11", "2024-08-14", "2024-09-11", "2024-10-10", "2024-11-13", "2024-12-11",
    # 2025 -- same shutdown gap: Sep-data delayed to 10-24; Oct-data NEVER published
    "2025-01-15", "2025-02-12", "2025-03-12", "2025-04-10", "2025-05-13", "2025-06-11",
    "2025-07-15", "2025-08-12", "2025-09-11", "2025-10-24", "2025-12-18",
    # 2026 (through the panel window)
    "2026-01-13", "2026-02-13", "2026-03-11", "2026-04-10", "2026-05-12", "2026-06-10",
    "2026-07-14",
]


def events(end="2026-07-15") -> dict:
    """Returns {'NFP': [dates], 'CPI': [dates]} filtered to <= end (the ZF panel end)."""
    return {
        "NFP": [d for d in NFP_DATES if d <= end],
        "CPI": [d for d in CPI_DATES if d <= end],
    }


if __name__ == "__main__":
    ev = events()
    print(f"NFP events: {len(ev['NFP'])}")
    print(f"CPI events: {len(ev['CPI'])}")
    print(f"Combined (union, dedup same-day collisions): "
          f"{len(set(ev['NFP']) | set(ev['CPI']))}")
    overlap = set(ev["NFP"]) & set(ev["CPI"])
    print(f"Same-day NFP+CPI collisions: {len(overlap)} {sorted(overlap) if overlap else ''}")
