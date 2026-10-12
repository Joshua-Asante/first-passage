"""Q-SFCLEAR-2 G4 roll-date generator (build card v3, §4 roll-date checks). Calendar only."""
from __future__ import annotations

import csv
import importlib.util
import json
import pathlib
import subprocess
import sys
from datetime import date

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHED = ROOT / "lab" / "analysis" / "c1" / "sfclear_2026-10" / "schedule"
GEN = SCHED / "build_roll_dates.py"


def _load():
    spec = importlib.util.spec_from_file_location("sfclear2_roll_dates", GEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rd = _load()
D19 = json.loads((ROOT / rd.D19).read_text(encoding="utf-8"))
CAL = rd.Calendar(D19)
ROWS = [r for r in csv.DictReader((l for l in (ROOT / rd.CAPTURE).read_text(encoding="utf-8").splitlines()
                                   if not l.startswith("#")), delimiter="\t")]
VECTORS = [(r["code"], r["product"], r["month"], k, r[k]) for r in ROWS
           for k in (("first_notice", "last_trade") if r["product"] == "MGC" else ("last_trade",))]


def _ym(month):
    y, m = month.split("-")
    return int(y), int(m)


def _rule(cal, product, month, key, **mut):
    y, m = _ym(month)
    if product == "MGC":
        return (rd.mgc_first_notice(cal, y, m, **mut) if key == "first_notice"
                else rd.mgc_last_trade(cal, y, m))
    return rd.j6_last_trade(cal, y, m, **mut)


def test_capture_has_36_vectors():
    assert len(VECTORS) == 36


@pytest.mark.parametrize("code,product,month,key,want", VECTORS, ids=[f"{v[0]}-{v[3]}" for v in VECTORS])
def test_every_capture_row_regenerates(code, product, month, key, want):
    assert _rule(CAL, product, month, key).isoformat() == want


@pytest.mark.parametrize("product,month,key,want", [
    ("MGC", "2027-06", "first_notice", "2027-05-28"),   # failed under v1 (Memorial Day)
    ("6J", "2027-01", "last_trade", "2027-01-15"),      # failed under v1 (MLK Day)
    ("6J", "2027-02", "last_trade", "2027-02-12"),      # failed under v1 (Presidents Day)
    ("MGC", "2027-12", "last_trade", "2027-12-29"),     # failed under v2 (Saturday New Year not observed)
])
def test_rows_that_failed_under_v1_and_v2(product, month, key, want):
    assert _rule(CAL, product, month, key).isoformat() == want


def _mismatches(**mut):
    return sum(_rule(CAL, p, mo, k, **mut).isoformat() != w for _, p, mo, k, w in VECTORS
               if (p == "MGC" and k == "first_notice" and "k_last" in mut) or (p == "6J" and "before" in mut))


@pytest.mark.parametrize("mut", [{"k_last": 2}, {"before": 1}, {"before": 3}])
def test_mutated_offset_is_caught(mut):
    assert _mismatches(**mut) > 0


def test_saturday_new_year_not_observed():
    assert date(2027, 12, 31) not in rd.federal_holidays(2028)
    assert date(2027, 12, 31) not in rd.federal_holidays(2027)
    assert CAL.is_bd(date(2027, 12, 31), "MGC")


def test_d19_federal_and_good_friday_each_move_a_date():
    bare = rd.Calendar({"entries": []}, federal=False, good_friday=False)
    # D19: an injected metals FULL_CLOSURE on Fri 2026-07-31 moves MGCQ26 first notice; FX is unaffected.
    inj = rd.Calendar({"entries": [{"date": "2026-07-31", "metals_status": "FULL_CLOSURE",
                                    "fx_status": "NORMAL", "equity_index_status": "NORMAL"}]},
                      federal=False, good_friday=False)
    assert rd.mgc_first_notice(bare, 2026, 8) == date(2026, 7, 31)
    assert rd.mgc_first_notice(inj, 2026, 8) == date(2026, 7, 30)
    assert inj.is_bd(date(2026, 7, 31), "6J")
    # Federal: Memorial Day 2027-05-31 (outside D19 coverage).
    fed = rd.Calendar({"entries": []}, federal=True, good_friday=False)
    assert rd.mgc_first_notice(bare, 2027, 6) == date(2027, 5, 31)
    assert rd.mgc_first_notice(fed, 2027, 6) == date(2027, 5, 28)
    # Good Friday: 2024-03-29.
    gf = rd.Calendar({"entries": []}, federal=False, good_friday=True)
    assert rd.mgc_first_notice(bare, 2024, 4) == date(2024, 3, 29)
    assert rd.mgc_first_notice(gf, 2024, 4) == date(2024, 3, 28)


def test_juneteenth_moves_june_2023_6j():
    assert rd.j6_last_trade(CAL, 2023, 6) == date(2023, 6, 16)
    assert rd.j6_last_trade(rd.Calendar(D19, juneteenth=False), 2023, 6) == date(2023, 6, 19)


def test_check_prints_match_and_output_names_sources():
    out = subprocess.run([sys.executable, "-I", str(GEN), "--check"], capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert out.stdout.strip().endswith("MATCH")
    doc = json.loads(rd.OUT.read_text(encoding="ascii"))
    srcs = {s["path"]: s["sha256"] for s in doc["header"]["sources"]}
    assert srcs[rd.CAPTURE] == "1afbcd9fe42b5237466837ed95e67a477ebb4a3b47812e8fc3b7fdc9e287efa6"
    assert srcs[rd.D19] == rd.hashlib.sha256((ROOT / rd.D19).read_bytes()).hexdigest()
    assert doc["header"]["capture_vectors"] == {"checked": 36, "mismatches": 0}


def test_output_rows_follow_the_rules():
    doc = json.loads(rd.OUT.read_text(encoding="ascii"))
    lo, hi = date(2022, 9, 1), date(2026, 9, 2)
    for c in doc["contracts"]:
        y, m = _ym(c["contract_month"])
        lt = date.fromisoformat(c["last_trade"])
        start = date.fromisoformat(c["g4_start_trade_date"])
        assert start <= hi and lt >= lo
        if c["product"] == "MGC":
            assert m % 2 == 0 and c["first_notice"] == rd.mgc_first_notice(CAL, y, m).isoformat()
        else:
            assert "first_notice" not in c and lt == rd.j6_last_trade(CAL, y, m)
        assert start == CAL.prev_bd(min(date.fromisoformat(c.get("first_notice", c["last_trade"])), lt),
                                    c["product"], 1)
    seams = doc["seams"]
    assert {s["product"] for s in seams} == {"6J", "MGC", "MYM"}
    for s in seams:
        m = _ym(s["from_month"])[1]
        assert m in ({2, 4, 6, 8, 12} if s["product"] == "MGC" else {3, 6, 9, 12})
        assert s["switch_open_local"].endswith("T18:00:00-04:00") or s["switch_open_local"].endswith("T18:00:00-05:00")
        assert lo <= date.fromisoformat(s["switch_trade_date"]) <= hi
    # MYM: 3 business days before the 3rd Friday (e.g. Sep 2025: Fri 19th -> Tue 16th).
    assert any(s["product"] == "MYM" and s["from_month"] == "2025-09" and s["switch_trade_date"] == "2025-09-16"
               for s in seams)
