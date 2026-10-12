"""G0-a personal forward calendar binding (card 2026-10-12, rows PC1-PC10)."""
import ast
import json
import shutil
from dataclasses import replace
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from c1_rail.book_session_calendar import CalendarError
from c1_rail.instance_binding import INSTANCE_KEYS
from c1_rail.personal_calendar_binding import load_personal_calendar_binding

REPO = Path(__file__).resolve().parents[2]
CAL = REPO / "ops" / "calendars"
BINDING = REPO / "deploy" / "c1_rail_personal" / "calendar_binding.json"
PERSONAL_REGISTRY = CAL / "personal" / "RATIFIED.json"
OCT, NOV = "book_session_calendar_2026-10.json", "book_session_calendar_2026-11.json"
OCT_SHA = "16e322b1b7c9c7e2b1e8a5fdebb6eaba34e7a509630677f7ac389df54e211b3b"
NOV_SHA = "b89562a58a665daa4054f310f41007f815bb45b54444c6404ad463ac0b60aad7"
ET = ZoneInfo("America/New_York")


def et(m, d, hh, mm=0):
    return datetime(2026, m, d, hh, mm, tzinfo=ET)


def dump(path, payload):
    path.write_bytes(json.dumps(payload, indent=2).encode("utf-8") + b"\n")


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def tmp_repo(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(CAL / "evidence", repo / "ops" / "calendars" / "evidence")
    for name in (OCT, NOV, "book_closure_overlay.json"):
        shutil.copyfile(CAL / name, repo / "ops" / "calendars" / name)
    return repo


def ratify(repo, names):
    """Synthetic personal registry rows (test authority only), ratified at generation."""
    rows = []
    for name in names:
        payload = json.loads((repo / "ops" / "calendars" / name).read_bytes())
        rows.append({
            "calendar_id": payload["calendar_id"], "calendar_file": f"ops/calendars/{name}",
            "calendar_sha256": digest(repo / "ops" / "calendars" / name),
            "closure_overlay_file": "ops/calendars/book_closure_overlay.json",
            "closure_overlay_sha256": digest(repo / "ops" / "calendars" / "book_closure_overlay.json"),
            "coverage_start_utc": payload["coverage"]["coverage_start_utc"],
            "coverage_end_utc": payload["coverage"]["coverage_end_utc"],
            "ratified_by": "operator", "ratified_utc": payload["generated_utc"],
            "instruction": "synthetic test authority", "record": "test", "scope": "test",
        })
    path = repo / "ops" / "calendars" / "personal" / "RATIFIED.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    dump(path, {"schema": "calendar_ratification/v1", "note": "synthetic", "ratifications": rows})


def bind(repo, names):
    doc = json.loads(BINDING.read_bytes())
    doc["calendars"] = [{"calendar_file": f"ops/calendars/{n}",
                         "calendar_sha256": digest(repo / "ops" / "calendars" / n)} for n in names]
    path = repo / "binding.json"
    dump(path, doc)
    return path


def mutate(repo, name, out, fn):
    payload = json.loads((repo / "ops" / "calendars" / name).read_bytes())
    fn(payload)
    dump(repo / "ops" / "calendars" / out, payload)


def test_pc1_tradeify_ratification_does_not_admit_the_personal_instance():
    tradeify = {r["calendar_sha256"] for r in json.loads((CAL / "RATIFIED.json").read_bytes())["ratifications"]}
    assert {OCT_SHA, NOV_SHA} <= tradeify
    assert json.loads(PERSONAL_REGISTRY.read_bytes())["ratifications"] == []
    with pytest.raises(CalendarError, match="^calendar_not_ratified$"):
        load_personal_calendar_binding(BINDING, repo_root=REPO)


def test_checked_in_binding_pins_the_checked_in_bytes():
    doc = json.loads(BINDING.read_bytes())
    assert [(c["calendar_file"], c["calendar_sha256"]) for c in doc["calendars"]] == [
        (f"ops/calendars/{OCT}", OCT_SHA), (f"ops/calendars/{NOV}", NOV_SHA)]
    assert doc["closure_overlay"]["sha256"] == digest(REPO / doc["closure_overlay"]["file"])
    assert doc["ratification_registry"] == "ops/calendars/personal/RATIFIED.json"


def test_pc2_personally_ratified_permitted_row_gives_the_section5_session(tmp_path):
    repo = tmp_repo(tmp_path)
    ratify(repo, [OCT, NOV])
    binding = load_personal_calendar_binding(bind(repo, [OCT, NOV]), repo_root=repo)
    decision = binding.session_for(et(10, 13, 10))
    assert decision.refusal is None and decision.calendar_digest == OCT_SHA
    s = decision.session
    assert s.session_id == "tradeify-account-day:2026-10-13"
    assert [t.astimezone(ET).strftime("%H:%M") for t in
            (s.risk_add_cutoff, s.flatten_start, s.own_flat_deadline)] == ["15:45", "15:55", "16:00"]


def test_pc3_flipped_calendar_byte_refuses_before_parsing(tmp_path):
    repo = tmp_repo(tmp_path)
    ratify(repo, [OCT, NOV])
    path = bind(repo, [OCT, NOV])
    target = repo / "ops" / "calendars" / OCT
    data = bytearray(target.read_bytes())
    data[0] ^= 0x01                                     # '{' -> 'z': no longer JSON
    target.write_bytes(bytes(data))
    with pytest.raises(CalendarError, match="^binding_digest_mismatch"):
        load_personal_calendar_binding(path, repo_root=repo)


@pytest.mark.parametrize("fn, message", [
    (lambda p: p["schedule_rule"].update(cutoff_before_own_flat_minutes=10), "schedule_rule constants differ"),
    (lambda p: p["first_release_policy"]["deny"].remove("MISSING_SOURCE"), "first_release_policy"),
], ids=["pc4_schedule_rule", "pc5_deny_set"])
def test_pc4_pc5_loader_refusals_propagate_without_fallthrough(tmp_path, fn, message):
    repo = tmp_repo(tmp_path)
    mutate(repo, OCT, "mutated.json", fn)
    ratify(repo, ["mutated.json", NOV])
    with pytest.raises(CalendarError, match=message):
        load_personal_calendar_binding(bind(repo, ["mutated.json", NOV]), repo_root=repo)


def test_pc5_missing_source_row_stays_denied(tmp_path):
    repo = tmp_repo(tmp_path)
    ratify(repo, [OCT, NOV])
    decision = load_personal_calendar_binding(bind(repo, [OCT, NOV]), repo_root=repo).session_for(et(10, 12, 10))
    assert decision.session is None and decision.refusal == "session_denied:MISSING_SOURCE"


def test_pc6_coverage_gap_refuses(tmp_path):
    repo = tmp_repo(tmp_path)

    def drop_first_three(p):                            # first row becomes 2026-11-03: 11-02 is uncovered
        p["sessions"] = p["sessions"][3:]
        first = p["sessions"][0]
        first["predecessor_in_file"] = False
        p["coverage"].update(first_session_id=first["session_id"], coverage_start_utc=first["opens_utc"])
    mutate(repo, NOV, "late.json", drop_first_three)
    ratify(repo, [OCT, "late.json"])
    with pytest.raises(CalendarError, match="^coverage_gap"):
        load_personal_calendar_binding(bind(repo, [OCT, "late.json"]), repo_root=repo)


@pytest.mark.parametrize("day", [29, 30])
def test_pc7_overlap_rows_agree_and_the_later_ratified_file_wins(tmp_path, day):
    repo = tmp_repo(tmp_path)
    ratify(repo, [OCT, NOV])
    binding = load_personal_calendar_binding(bind(repo, [OCT, NOV]), repo_root=repo)
    now = et(10, day, 10)
    oct_s, nov_s = (c.session_for(now).session for c in binding.calendars)
    assert oct_s is not None and replace(oct_s, calendar_digest="") == replace(nov_s, calendar_digest="")
    decision = binding.session_for(now)
    assert decision.calendar_digest == NOV_SHA and decision.session == nov_s


def test_pc8_overlay_pin_drift_refuses(tmp_path):
    repo = tmp_repo(tmp_path)
    ratify(repo, [OCT, NOV])
    path = bind(repo, [OCT, NOV])
    doc = json.loads(path.read_bytes())
    doc["closure_overlay"]["sha256"] = "0" * 64
    dump(path, doc)
    with pytest.raises(CalendarError, match="^binding_digest_mismatch"):
        load_personal_calendar_binding(path, repo_root=repo)


def _imports(path):
    names = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.add(node.module or "")
            names.update(a.name for a in node.names)
    return names


def test_pc9_module_stays_outside_the_trust_domain_and_lab():
    from c1_rail.qualification.trust_domain import PRODUCTION_TRUST_POLICY
    trusted = [m for m in PRODUCTION_TRUST_POLICY.required_code_roles.values() if m.startswith("c1_rail")]
    assert "c1_rail.book_session_calendar" in trusted and "c1_rail.book_account_owner" in trusted
    for module in trusted:
        base = REPO / "ops" / Path(*module.split("."))
        path = base / "__init__.py" if base.is_dir() else base.with_suffix(".py")
        assert not any("personal_calendar_binding" in n for n in _imports(path)), module
    # No production module imports it at all in G0-a (G0-b wiring is a separate admission).
    own = REPO / "ops" / "c1_rail" / "personal_calendar_binding.py"
    for path in (REPO / "ops").rglob("*.py"):
        if path != own:
            assert not any("personal_calendar_binding" in n for n in _imports(path)), path
    assert not any(n == "lab" or n.startswith("lab.") for n in _imports(own))


def _keys(node):
    if isinstance(node, dict):
        for key, value in node.items():
            yield key
            yield from _keys(value)
    elif isinstance(node, list):
        for value in node:
            yield from _keys(value)


def test_pc10_binding_key_set_is_exact_and_carries_no_identity_slot(tmp_path):
    doc = json.loads(BINDING.read_bytes())
    assert set(doc) == {"_comment", "schema", "instance", "schedule_rule", "first_release_policy_deny",
                        "ratification_registry", "closure_overlay", "calendars"}
    assert not set(_keys(doc)) & INSTANCE_KEYS
    doc["account"] = "x"
    path = tmp_path / "binding.json"
    dump(path, doc)
    with pytest.raises(CalendarError, match="^binding_schema"):
        load_personal_calendar_binding(path, repo_root=REPO)
