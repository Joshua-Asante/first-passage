"""G4-a live roll source (card 2026-10-12-personal-live-g4-roll-card, section 4 rows R1-R9).

Lab files are read as bytes by path only; nothing here imports lab code.
"""
import ast
import hashlib
import json
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from c1_rail import contract_roll as cr

REPO = Path(__file__).resolve().parents[2]
LAB = REPO / "lab" / "analysis" / "c1" / "sfclear_2026-10" / "schedule"
BOUND = LAB / "roll_dates_6J_MGC_2022-09-01_2026-09-02.json"
LAB_CAPTURE = LAB / "sources" / "cme_calendar_capture_20261012.tsv"
OPS_CAPTURE = REPO / "ops" / "calendars" / "roll_sources" / "cme_calendar_capture_20261012.tsv"
FORWARD = REPO / "ops" / "calendars" / "contract_roll_forward.json"
MODULE = REPO / "ops" / "c1_rail" / "contract_roll.py"
SCRIPT = REPO / "scripts" / "author_contract_roll.py"
BOUND_SHA = "72677d254045fd35ca3da7047c8b649f47d0ae283d3fc41a402467de8de4134c"
CAPTURE_SHA = "1afbcd9fe42b5237466837ed95e67a477ebb4a3b47812e8fc3b7fdc9e287efa6"
G4_LEGS = {"aegis_6j": "6J", "vanguard_mgc": "MGC"}
UTC = timezone.utc


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _utc(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def _rows(raw):
    data = json.loads(raw)
    return data["header"], data["contracts"], data["seams"]


# R1 ---------------------------------------------------------------------------------------------
def test_r1_compat_build_is_the_bound_list_byte_for_byte():
    bound = BOUND.read_bytes()
    assert _sha(bound) == BOUND_SHA == cr.COMPAT_SHA256
    assert cr.build(date(2022, 9, 1), date(2026, 9, 2), compat=True) == bound


def test_r1_header_counts_match_the_card():
    header, contracts, seams = _rows(BOUND.read_bytes())
    assert header["counts"] == {"contracts": 72, "seams": 52}
    assert header["capture_vectors"] == {"checked": 36, "mismatches": 0}


# R1b --------------------------------------------------------------------------------------------
@pytest.mark.parametrize("day", [date(2027, 3, 26), date(2028, 4, 14)])
@pytest.mark.parametrize("product", ["MGC", "6J"])
def test_r1b_good_friday_is_not_a_business_day(day, product):
    assert day.weekday() == 4
    assert not cr.Calendar({"entries": []}).is_bd(day, product)


def test_r1b_d19_full_closure_is_per_group():
    day = date(2026, 3, 4)   # an ordinary Wednesday
    row = {"date": day.isoformat(), "metals_status": "FULL_CLOSURE",
           "fx_status": "OPEN", "equity_index_status": "OPEN"}
    cal = cr.Calendar({"entries": [row]})
    assert not cal.is_bd(day, "MGC")
    assert cal.is_bd(day, "6J") and cal.is_bd(day, "MYM") and cal.is_bd(day, "MNQ")
    assert cr.Calendar({"entries": []}).is_bd(day, "MGC")


def test_r1b_saturday_new_year_is_not_observed_on_friday():
    # 2027-01-01 is a Friday (observed itself); 2022-01-01 is a Saturday: 2021-12-31 stays open.
    cal = cr.Calendar({"entries": []})
    assert cal.is_bd(date(2021, 12, 31), "MGC")
    assert not cal.is_bd(date(2027, 1, 1), "MGC")


# R2 ---------------------------------------------------------------------------------------------
def test_r2_ops_capture_is_a_byte_copy_and_pinned():
    assert OPS_CAPTURE.read_bytes() == LAB_CAPTURE.read_bytes()
    assert _sha(OPS_CAPTURE.read_bytes()) == CAPTURE_SHA == cr.CAPTURE_SHA256


def test_r2_all_36_capture_vectors_reproduce():
    sources = cr.load_sources()
    assert (sources.vectors_checked, sources.vectors_bad) == (36, 0)
    assert sources.horizon == {"6J": (2027, 9), "MGC": (2028, 8)}


def test_r2_a_one_byte_change_refuses(tmp_path):
    raw = bytearray(OPS_CAPTURE.read_bytes())
    raw[-2] = ord("0") if raw[-2] != ord("0") else ord("1")
    bad = tmp_path / "capture.tsv"
    bad.write_bytes(bytes(raw))
    with pytest.raises(cr.RollSourceError, match="sha256"):
        cr.load_sources(capture_path=bad)


def test_r2_mgc_2027_12_last_trade_matches_capture():
    # M-R1a: observing a Saturday New Year's Day on the Friday before would give 2027-12-28.
    cal = cr.load_sources().calendar
    assert cr.mgc_last_trade(cal, 2027, 12) == date(2027, 12, 29)


# R3 ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("path", [BOUND, FORWARD], ids=["compat", "forward"])
def test_r3_zero_margin_on_every_on_cycle_seam(path):
    _, contracts, seams = _rows(path.read_bytes())
    by = {(r["product"], r["contract_month"]): r for r in contracts}
    on_cycle = [s for s in seams if s["product"] in G4_LEGS.values()]
    assert on_cycle
    for seam in on_cycle:
        row = by[(seam["product"], seam["from_month"])]
        assert seam["switch_open_utc"] == row["g4_start_open_utc"]
        assert seam["switch_trade_date"] == row["g4_start_trade_date"]


def test_r3_forward_lists_a_seam_for_every_on_cycle_contract():
    _, contracts, seams = _rows(FORWARD.read_bytes())
    want = {(r["product"], r["contract_month"]) for r in contracts if r["on_seam_cycle"]}
    assert want == {(s["product"], s["from_month"]) for s in seams}


def test_r3_switch_rule_is_independent_of_the_g4_rule():
    cal = cr.load_sources().calendar
    for y in (2023, 2027):
        fn = cr.mgc_first_notice(cal, y, 6)
        d = cr.contract_dates(cal, "MGC", y, 6)
        assert d["switch"] == cal.prev_bd(fn, "MGC", 1) == d["g4_start"]


# R4 ---------------------------------------------------------------------------------------------
def _weekdays(first, last):
    d = first
    while d <= last:
        if d.weekday() < 5:
            yield d
        d += timedelta(1)


@pytest.mark.parametrize("leg,product", sorted(G4_LEGS.items()))
def test_r4_selected_contract_is_never_inside_its_own_window(leg, product):
    end = cr.load_sources().refuse_from[product]
    cycle = {"6J": {3, 6, 9, 12}, "MGC": {2, 4, 6, 8, 12}}[product]
    n = 0
    for d in _weekdays(date(2022, 9, 1), end - timedelta(1)):
        ref = cr.select_contract(leg, d)
        assert ref.g4_start_trade_date > d, (d, ref)
        assert int(ref.contract_month[5:]) in cycle
        n += 1
    assert n > 1000
    with pytest.raises(cr.RollHorizonExceeded):
        cr.select_contract(leg, end)


@pytest.mark.parametrize("leg", ["aegis_6j", "vanguard_mgc", "dj30_mym_p250"])
def test_r4_selection_switches_exactly_at_each_bound_seam(leg):
    product = cr.LEGS[leg]
    _, _, seams = _rows(BOUND.read_bytes())
    cal = cr.load_sources().calendar
    rows = [s for s in seams if s["product"] == product]
    assert rows
    for s in rows:
        sw = date.fromisoformat(s["switch_trade_date"])
        assert cr.select_contract(leg, sw).contract_month == s["to_month"]
        assert cr.select_contract(leg, cal.prev_bd(sw, product, 1)).contract_month == s["from_month"]


def test_r4_mnq_uses_n3_before_the_third_friday():
    assert cr.select_contract("orb_mnq_v7", date(2026, 12, 14)).code == "MNQZ26"
    assert cr.select_contract("orb_mnq_v7", date(2026, 12, 15)).code == "MNQH27"


def test_r4_codes_are_dated_contracts():
    assert cr.select_contract("aegis_6j", date(2026, 10, 12)).code == "6JZ26"
    assert cr.select_contract("vanguard_mgc", date(2026, 10, 12)).code == "MGCZ26"


def test_legs_match_book_policy():
    from c1_rail.book_policy import BOOK_LEGS
    assert cr.LEGS == {row.leg_id: row.symbol for row in BOOK_LEGS}


# R5 ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("leg,code", [("aegis_6j", "6JZ26"), ("vanguard_mgc", "MGCZ26"),
                                      ("aegis_6j", "6JH27"), ("vanguard_mgc", "MGCG27")])
def test_r5_window_boundary(leg, code):
    start = cr.contract_ref(leg, code).g4_start_open_utc
    assert cr.g4_refusal(leg, code, start - timedelta(seconds=1)) is None
    assert cr.g4_refusal(leg, code, start) == "g4_window"
    assert cr.g4_refusal(leg, code, start + timedelta(days=1)) == "g4_window"


# R6 ---------------------------------------------------------------------------------------------
NOW = datetime(2026, 10, 12, 15, 0, tzinfo=UTC)


@pytest.mark.parametrize("leg,code", [("aegis_6j", "6JH27"), ("aegis_6j", "6JX26"),
                                      ("vanguard_mgc", "MGCG27"), ("vanguard_mgc", "MGCV27")])
def test_r6_wrong_month_is_not_selected(leg, code):
    assert cr.g4_refusal(leg, code, NOW) == "contract_not_selected"


@pytest.mark.parametrize("leg,code", [("aegis_6j", "6J1!"), ("aegis_6j", None), ("aegis_6j", "6JZ6"),
                                      ("vanguard_mgc", "MGC1!"), ("vanguard_mgc", "6JZ26"),
                                      ("vanguard_mgc", "")])
def test_r6_continuous_or_missing_contract_is_unbound(leg, code):
    assert cr.g4_refusal(leg, code, NOW) == "contract_unbound"


def test_r6_selected_contract_passes():
    for leg in G4_LEGS:
        ref = cr.select_contract(leg, cr.trade_date_of(NOW))
        assert cr.g4_refusal(leg, ref.code, NOW) is None
        assert cr.g4_refusal(leg, ref, NOW) is None


def test_naive_now_is_rejected():
    with pytest.raises(ValueError):
        cr.g4_refusal("aegis_6j", "6JZ26", datetime(2026, 10, 12, 15))


# R7 ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("leg,code", [("aegis_6j", "6JU27"), ("vanguard_mgc", "MGCQ28")])
def test_r7_past_horizon_refuses(leg, code):
    product = G4_LEGS[leg]
    end = cr.load_sources().refuse_from[product]
    last_ok = datetime(end.year, end.month, end.day, 12, tzinfo=UTC) - timedelta(days=3)
    while last_ok.weekday() > 4:
        last_ok -= timedelta(days=1)
    assert cr.g4_refusal(leg, code, last_ok) is None
    after = datetime(end.year, end.month, end.day, 12, tzinfo=UTC) + timedelta(days=7)
    assert cr.g4_refusal(leg, code, after) == "roll_horizon_exceeded"
    assert cr.flatten_required(leg, code, after)


def test_r7_contract_beyond_capture_refuses():
    assert cr.g4_refusal("aegis_6j", "6JZ27", NOW) == "roll_horizon_exceeded"
    assert cr.g4_refusal("vanguard_mgc", "MGCZ28", NOW) == "roll_horizon_exceeded"


def test_r7_cash_settled_legs_are_not_g4_gated():
    far = datetime(2029, 6, 1, 15, tzinfo=UTC)
    for leg in ("orb_mnq_v7", "dj30_mym_p250"):
        for now in (NOW, far):
            assert cr.g4_refusal(leg, "MNQ1!", now) is None
            assert cr.g4_refusal(leg, None, now) is None
            assert cr.flatten_required(leg, None, now) is False


def test_unknown_leg_raises():
    with pytest.raises(ValueError):
        cr.g4_refusal("nope", "6JZ26", NOW)


# R8 ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("leg,code", [("aegis_6j", "6JZ26"), ("vanguard_mgc", "MGCZ26")])
def test_r8_flatten_at_or_after_window_start(leg, code):
    start = cr.contract_ref(leg, code).g4_start_open_utc
    assert cr.flatten_required(leg, code, start - timedelta(seconds=1)) is False
    assert cr.flatten_required(leg, code, start) is True
    assert cr.flatten_required(leg, code, start + timedelta(hours=30)) is True


@pytest.mark.parametrize("leg,code", [("aegis_6j", "6JH27"), ("aegis_6j", "6JX26"),
                                      ("vanguard_mgc", "MGCG27"), ("aegis_6j", None),
                                      ("aegis_6j", "6J1!")])
def test_r8_flatten_a_non_selected_or_unbound_contract(leg, code):
    assert cr.flatten_required(leg, code, NOW) is True


# R9 ---------------------------------------------------------------------------------------------
def _imports(source):
    """Every module name an AST imports, with `from X import Y` also yielding X.Y."""
    names = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            base = ("." * node.level) + (node.module or "")
            names.add(base)
            names |= {f"{base}.{a.name}".lstrip(".") if base.strip(".") else a.name for a in node.names}
    return names


def _imports_contract_roll(source):
    return any("contract_roll" in name.split(".") for name in _imports(source))


def test_r9_scanner_catches_an_added_import():
    src = (REPO / "ops" / "c1_rail" / "book_account_owner.py").read_text(encoding="utf-8")
    assert not _imports_contract_roll(src)
    for line in ("from .contract_roll import g4_refusal", "from . import contract_roll",
                 "import c1_rail.contract_roll", "from c1_rail import contract_roll as x"):
        assert _imports_contract_roll(src + "\n" + line + "\n")


def test_r9_module_and_script_import_no_lab_code():
    for path in (MODULE, SCRIPT):
        names = _imports(path.read_text(encoding="utf-8"))
        assert not any(n.split(".")[0] in {"lab", "analysis", "build_roll_dates"} for n in names), names
    stdlib = set(sys.stdlib_module_names) | {"__future__"}
    assert {n.split(".")[0] for n in _imports(MODULE.read_text(encoding="utf-8"))} <= stdlib


def _module_file(name):
    rel = Path(*name.split("."))
    for root in (REPO / "ops", REPO / "core", REPO):
        for candidate in (root / rel.with_suffix(".py"), root / rel / "__init__.py"):
            if candidate.is_file():
                return candidate
    return None


def test_r9_no_trust_domain_module_imports_contract_roll():
    from c1_rail.qualification.trust_domain import _PRODUCTION_CODE
    scanned = 0
    for role, name in _PRODUCTION_CODE.items():
        path = _module_file(name)
        if path is None:
            assert name.startswith("fp_qualification_port_"), name   # private runtime ports
            continue
        assert not _imports_contract_roll(path.read_text(encoding="utf-8")), (role, name)
        scanned += 1
    assert scanned > 50
    assert "c1_rail.contract_roll" not in _PRODUCTION_CODE.values()


def test_r9_nothing_in_ops_or_core_imports_contract_roll():
    importers = [p for top in ("ops", "core") for p in (REPO / top).rglob("*.py")
                 if p != MODULE and _imports_contract_roll(p.read_text(encoding="utf-8", errors="replace"))]
    assert importers == []


def _script(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, cwd=REPO)


def test_r9_forward_artifact_regenerates_byte_identically():
    assert cr.forward() == FORWARD.read_bytes()
    run = _script("--forward", "--check")
    assert run.returncode == 0 and run.stdout.strip().endswith("MATCH"), run.stdout + run.stderr


def test_r9_compat_check_prints_match():
    run = _script("--compat-check")
    assert run.returncode == 0, run.stderr
    assert run.stdout.split() == [BOUND_SHA, "MATCH"]


def test_forward_header_and_rows():
    header, contracts, _ = _rows(FORWARD.read_bytes())
    assert header["compat_sha256"] == BOUND_SHA
    assert {s["path"]: s["sha256"] for s in header["sources"]}[
        "ops/calendars/roll_sources/cme_calendar_capture_20261012.tsv"] == CAPTURE_SHA
    assert header["horizon"]["6J"]["last_contract"] == "2027-09"
    assert header["horizon"]["MGC"]["last_contract"] == "2028-08"
    assert all(r["g4_start_trade_date"] >= "2026-09-03" for r in contracts)
    captured = {(r["product"], r["month"]): r for r in cr.capture_rows(OPS_CAPTURE.read_text(encoding="utf-8"))}
    assert {(r["product"], r["contract_month"]) for r in contracts} == set(captured)
    for r in contracts:
        cap = captured[(r["product"], r["contract_month"])]
        assert r["last_trade"] == cap["last_trade"]
        assert r.get("first_notice", "-") == cap["first_notice"]
