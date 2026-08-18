#!/usr/bin/env python3
"""Diff request.economic() export dates against hand-pinned campaign calendars.

Provenance/hygiene only. Does not reopen RATES-EV-ZF-1, NG-EIA-1, or Aegis BOJ.

Hand-pinned owners are imported from their archive modules (not copied).
FOMC has no request.economic() field — always NO_TV_FIELD.
EVT-1 FOMC 2019–2021 is UNRECOVERABLE_PIN on this public clone.

Usage:
    python scripts/diff_econ_calendar.py
    python scripts/diff_econ_calendar.py --in lab/tools/econ_export/exports/*.csv
    python scripts/diff_econ_calendar.py --require-tv-export --in path.csv
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from parse_econ_export import parse_econ_export  # noqa: E402

RATES_CAL = REPO_ROOT / "lab/archive/rates_ev_zf_recon_2026-07/build_calendar.py"
NG_CAL = REPO_ROOT / "lab/archive/ng_eia_recon_2026-07/build_calendar.py"
FOMC_ECHO = REPO_ROOT / "lab/archive/msl_s2a_mcl_2026-08/construct_lib.py"
DEFAULT_EXPORT_DIR = REPO_ROOT / "lab/tools/econ_export/exports"

RATES_START = "2019-01-01"
RATES_END = "2026-07-15"
EVT1_END = "2025-08-31"
FOMC_UNRECOVERABLE_END = "2021-12-31"

NO_TV_FIELDS = frozenset({"FOMC"})


@dataclass(frozen=True)
class DiffRow:
    limb: str
    field: str
    status: str
    date: str
    note: str = ""


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def load_rates_events(*, end: str = RATES_END) -> dict[str, set[str]]:
    mod = _load_module("rates_ev_zf_build_calendar", RATES_CAL)
    ev = mod.events(end=end)
    return {"CPI": set(ev["CPI"]), "NFP": set(ev["NFP"])}


def load_ng_primary(*, start: str = RATES_START, end: str = RATES_END) -> set[str]:
    mod = _load_module("ng_eia_build_calendar", NG_CAL)
    return set(mod.primary_thursdays(start=start, end=end))


def load_fomc_echo() -> set[str]:
    """2022–2026 echo only. 2019–2021 is not in this public clone."""
    mod = _load_module("msl_s2a_construct_lib", FOMC_ECHO)
    return set(mod.FOMC_DATES)


def _shift(iso: str, days: int) -> str:
    d = date.fromisoformat(iso) + timedelta(days=days)
    return d.isoformat()


def _in_window(iso: str, start: str, end: str) -> bool:
    return start <= iso <= end


def compare_sets(
    *,
    limb: str,
    field: str,
    hand: set[str],
    tv: set[str] | None,
    tv_present: bool,
    no_tv_field: bool = False,
) -> list[DiffRow]:
    rows: list[DiffRow] = []
    if no_tv_field:
        rows.append(DiffRow(limb, field, "NO_TV_FIELD", "", "request.economic() has no field"))
        return rows
    if not tv_present:
        rows.append(DiffRow(limb, field, "AWAIT_TV_EXPORT", "", "no ECON_EXPORT CSV landed"))
        return rows
    assert tv is not None
    if not tv and field == "NGSC":
        rows.append(DiffRow(limb, field, "NO_TV_FIELD", "", "export present but zero NGSC rows"))
        return rows

    used_tv: set[str] = set()
    for h in sorted(hand):
        if h in tv:
            rows.append(DiffRow(limb, field, "MATCH", h))
            used_tv.add(h)
        elif _shift(h, -1) in tv or _shift(h, 1) in tv:
            neighbor = _shift(h, -1) if _shift(h, -1) in tv else _shift(h, 1)
            rows.append(DiffRow(limb, field, "TZ_SHIFT", h, f"tv={neighbor}"))
            used_tv.add(neighbor)
        else:
            rows.append(DiffRow(limb, field, "MISSING_TV", h))

    for t in sorted(tv):
        if t in used_tv:
            continue
        if _shift(t, -1) in hand or _shift(t, 1) in hand:
            continue
        rows.append(DiffRow(limb, field, "EXTRA_TV", t))
    return rows


def discover_exports(explicit: list[Path] | None) -> list[Path]:
    if explicit:
        return list(explicit)
    if not DEFAULT_EXPORT_DIR.is_dir():
        return []
    return sorted(
        p for p in DEFAULT_EXPORT_DIR.glob("ECON_EXPORT_v0.1_*.csv") if p.is_file()
    )


def run_diff(*, export_paths: list[Path]) -> list[DiffRow]:
    tv_present = bool(export_paths)
    tv_by_field: dict[str, set[str]] = {}
    if tv_present:
        tv_by_field = parse_econ_export(export_paths)

    rows: list[DiffRow] = []
    rates = load_rates_events(end=RATES_END)
    for field in ("CPI", "NFP"):
        rows.extend(
            compare_sets(
                limb="RATES-EV-ZF-1",
                field=field,
                hand=rates[field],
                tv=tv_by_field.get(field, set()),
                tv_present=tv_present,
            )
        )

    ng = load_ng_primary()
    rows.extend(
        compare_sets(
            limb="NG-EIA-1",
            field="NGSC",
            hand=ng,
            tv=tv_by_field.get("NGSC", set()),
            tv_present=tv_present,
        )
    )

    evt_rates = load_rates_events(end=EVT1_END)
    for field in ("CPI", "NFP"):
        hand = {d for d in evt_rates[field] if d <= EVT1_END}
        rows.extend(
            compare_sets(
                limb="EVT-1",
                field=field,
                hand=hand,
                tv=tv_by_field.get(field, set()),
                tv_present=tv_present,
            )
        )

    rows.extend(
        compare_sets(
            limb="EVT-1",
            field="FOMC",
            hand=set(),
            tv=None,
            tv_present=tv_present,
            no_tv_field=True,
        )
    )
    echo = {d for d in load_fomc_echo() if _in_window(d, "2022-01-01", EVT1_END)}
    rows.append(
        DiffRow(
            limb="EVT-1",
            field="FOMC",
            status="UNRECOVERABLE_PIN",
            date=f"{RATES_START}/{FOMC_UNRECOVERABLE_END}",
            note=(
                "stage2_run.py FOMC_DATES_ET absent on this public clone; "
                f"construct_lib echo n={len(echo)} for 2022–{EVT1_END} (not a TV field)"
            ),
        )
    )
    return rows


def format_report(rows: list[DiffRow]) -> str:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.status] = counts.get(r.status, 0) + 1
    summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    lines = [
        "# ECON EXPORT v0.1 provenance diff",
        "",
        "Hygiene only. Does not reopen closed campaigns or license a day-filter.",
        f"Summary: {summary}",
        "",
        "| limb | field | status | date | note |",
        "|---|---|---|---|---|",
    ]
    # Compact: collapse MATCH rows to a count per limb/field; keep exceptions.
    match_counts: dict[tuple[str, str], int] = {}
    shown: list[DiffRow] = []
    for r in rows:
        if r.status == "MATCH":
            match_counts[(r.limb, r.field)] = match_counts.get((r.limb, r.field), 0) + 1
        else:
            shown.append(r)
    for (limb, field), n in sorted(match_counts.items()):
        shown.insert(0, DiffRow(limb, field, "MATCH", f"n={n}"))
    shown.sort(key=lambda r: (r.limb, r.field, r.status, r.date))
    for r in shown:
        note = r.note.replace("|", "/")
        lines.append(f"| {r.limb} | {r.field} | {r.status} | {r.date} | {note} |")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Diff ECON EXPORT dates vs hand-pinned calendars.")
    ap.add_argument("--in", dest="in_paths", nargs="*", default=None, help="ECON_EXPORT CSV path(s)")
    ap.add_argument(
        "--require-tv-export",
        action="store_true",
        help="Fail closed (exit 2) when no TV export CSV is present.",
    )
    ap.add_argument("--out", default=None, help="Write report markdown to this path")
    a = ap.parse_args(argv)

    explicit = [Path(p) for p in a.in_paths] if a.in_paths else None
    if explicit:
        missing = [p for p in explicit if not p.is_file()]
        if missing:
            for p in missing:
                print(f"=== missing ECON export: {p} ===", file=sys.stderr)
            return 2
        paths = explicit
    else:
        paths = discover_exports(None)

    if a.require_tv_export and not paths:
        print("=== --require-tv-export: no ECON_EXPORT CSV ===", file=sys.stderr)
        return 2

    rows = run_diff(export_paths=paths)
    text = format_report(rows)
    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"=== wrote {out} ===")
    print(text, end="" if text.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
