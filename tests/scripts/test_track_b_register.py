"""Acceptance tests for scripts/track_b_register.py.

The committed register must pass; each synthetic case names the invariant (I-n,
see the checker docstring) and the finding code it proves. Synthetic registers
live in a temporary tree so link checks run against files the test controls.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "track_b_register.py"


def _load():
    spec = importlib.util.spec_from_file_location("track_b_register", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


tbr = _load()
PLAN = (("docs/plan.md", "table"),)


def _row(**over):
    row = {
        "id": "slice.S5",
        "kind": "slice",
        "aliases": ["T04"],
        "title": "Part A",
        "status": "ACCEPTED_LIMITED",
        "since": "2026-10-01",
        "owner": "../ledger.md#ruling",
        "next": None,
        "next_actor": "none",
    }
    row.update(over)
    return row


def _register(**over):
    data = {
        "schema": "track_b_register/v1",
        "role": "pilot",
        "as_of": "2026-10-03",
        "reconciled_at": "d5d559b",
        "items": [
            _row(),
            _row(id="defect.D-S5-1", kind="defect", aliases=[], status="CLOSED", owner="../ledger.md"),
        ],
    }
    data.update(over)
    return data


@pytest.fixture
def root(tmp_path):
    (tmp_path / "docs" / "governance").mkdir(parents=True)
    (tmp_path / "docs" / "ledger.md").write_text("# Ledger\n", encoding="utf-8")
    return tmp_path


def _codes(findings):
    return sorted({f.split(" ", 1)[0] for f in findings})


# ---------------------------------------------------------------- committed register

def test_committed_register_passes():
    result = subprocess.run([sys.executable, str(SCRIPT), "check"], capture_output=True, text=True, cwd=REPO)
    assert result.returncode == 0, result.stdout + result.stderr


def test_committed_register_parses_values_whole():
    text = (REPO / "docs" / "governance" / "track_b_register.yml").read_text(encoding="utf-8")
    assert tbr.lint(text) == []
    assert yaml.safe_load(text)["schema"] == "track_b_register/v1"


def test_clean_synthetic_register(root):
    assert tbr.check(_register(), root) == []


# ---------------------------------------------------------------- I1 / I2 shape (R1)

def test_r1_bad_status_and_actor(root):
    data = _register()
    data["items"][0] = _row(status="DONE", next_actor="robot")
    assert _codes(tbr.check(data, root)) == ["R1"]


def test_r1_id_prefix_must_match_kind(root):
    data = _register()
    data["items"][0] = _row(id="gate.S5")
    assert "R1" in _codes(tbr.check(data, root))


def test_r1_role_enum_and_unknown_top_keys(root):
    assert _codes(tbr.check(_register(role="derived-mirror"), root)) == ["R1"]
    for key in ("watch", "noted", "covers_from", "generated"):  # deleted keys stay refused
        assert any(key in f for f in tbr.check(_register(**{key: []}), root))


@pytest.mark.parametrize("value", [
    dt.date(2026, 10, 1),                                   # unquoted YAML date
    yaml.safe_load("x: 2026-10-05T23:30:00-05:00")["x"],    # unquoted YAML timestamp
    "2026-10-05T23:30:00-05:00",                            # quoted, but not a date
    "2026-02-30",                                           # not a calendar date
])
def test_r1_dates_are_strict_quoted_strings(root, value):
    data = _register()
    data["items"][0] = _row(since=value)
    assert _codes(tbr.check(data, root)) == ["R1"]
    assert "R1" in _codes(tbr.check(_register(as_of=value), root))


@pytest.mark.parametrize("value", [
    "2026-10-09T01:52:19",                                  # no zone
    yaml.safe_load("x: 2026-10-09T01:52:19Z")["x"],         # unquoted YAML timestamp
    "2026-10-09",                                           # a date, not a datetime
])
def test_r1_expires_is_a_quoted_zoned_datetime(root, value):
    data = _register()
    data["items"][0] = _row(expires=value)
    assert _codes(tbr.check(data, root)) == ["R1"]


def test_expiry_offset_is_converted_to_utc():
    assert tbr._expiry("2026-10-09T01:00:00-04:00") == dt.datetime(2026, 10, 9, 5, tzinfo=dt.timezone.utc)


@pytest.mark.parametrize("note", ["two\nlines", "carriage\rreturn", "   ", 5])
def test_r1_note_is_one_nonempty_line(root, note):
    data = _register()
    data["items"][0] = _row(note=note)
    assert _codes(tbr.check(data, root)) == ["R1"]


@pytest.mark.parametrize("over", [
    {"status": "OPEN", "next": None, "next_actor": "coordinator"},
    {"status": "ACCEPTED", "next": "do more", "next_actor": "coordinator"},
    {"status": "OPEN", "next": "do it", "next_actor": "none"},
])
def test_r1_next_and_actor_agree_with_status(root, over):
    data = _register()
    data["items"][0] = _row(**over)
    assert _codes(tbr.check(data, root)) == ["R1"]


# ---------------------------------------------------------------- I3 identity (R2)

def test_r2_alias_collides_with_other_row(root):
    data = _register()
    data["items"][1]["aliases"] = ["t04"]  # casefolded collision with slice.S5's alias
    assert _codes(tbr.check(data, root)) == ["R2"]


def test_r2_repeated_id_without_aliases(root):
    data = _register()
    dup = dict(data["items"][1], status="ACCEPTED")
    dup.pop("aliases", None)
    data["items"].append(dup)
    assert any(f.startswith("R2 ") and "2 rows" in f for f in tbr.check(data, root))
    with pytest.raises(tbr.Finding):
        tbr._groups(data["items"])


def test_load_rejects_duplicate_mapping_keys(tmp_path):
    reg = tmp_path / "r.yml"
    reg.write_text("schema: a\nschema: b\n", encoding="utf-8")
    with pytest.raises(tbr.Finding, match="duplicate key"):
        tbr.load(reg)


# ---------------------------------------------------------------- I4 graph (R3)

def test_r3_unknown_reference_and_cycle(root):
    data = _register()
    data["items"][0]["blocked_by"] = ["defect.D-S5-1"]
    data["items"][1]["blocked_by"] = ["slice.S5", "ghost.X"]
    findings = tbr.check(data, root)
    assert any("cycle" in f for f in findings) and any("ghost.X" in f for f in findings)


def test_r3_checkpoint_must_be_checkpoint_row(root):
    data = _register()
    data["items"][0]["checkpoint"] = "defect.D-S5-1"
    assert _codes(tbr.check(data, root)) == ["R3"]


# ---------------------------------------------------------------- I5 links (R4)

def test_r4_missing_file_in_owner_and_evidence(root):
    data = _register()
    data["items"][0]["owner"] = "../missing.md#x"
    data["items"][1]["evidence"] = ["../gone.md"]
    assert len([f for f in tbr.check(data, root) if f.startswith("R4")]) == 2


@pytest.mark.parametrize("link", ["https://example.com/x", "/etc/passwd", "C:/x.md", "../../../outside.md"])
def test_r4_links_stay_repository_relative_and_inside(root, link):
    data = _register()
    data["items"][0]["evidence"] = [link]
    assert _codes(tbr.check(data, root)) == ["R4"]


def test_r4_fragment_is_not_parsed(root):
    data = _register()
    data["items"][0]["owner"] = "../ledger.md#any-fragment"
    assert tbr.check(data, root) == []


def test_link_fields_are_one_enumerated_list():
    row = _row(owner="../a.md#x", evidence=["../b.md", "../c.md#y"])
    assert tbr.LINK_FIELDS == ("owner", "evidence")
    assert tbr._links(row) == ["../a.md#x", "../b.md", "../c.md#y"]


# ---------------------------------------------------------------- I6 revision (R6)

def test_r6_as_of_must_cover_every_since(root):
    data = _register()
    data["items"][0] = _row(since="2026-10-04")
    assert _codes(tbr.check(data, root)) == ["R6"]


def _git_root(root):
    env = {**os.environ, "GIT_COMMITTER_DATE": "2026-10-02T12:00:00+00:00",
           "GIT_AUTHOR_DATE": "2026-10-02T12:00:00+00:00"}
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "base"]):
        subprocess.run(["git", "-C", str(root), "-c", "user.email=t@t", "-c", "user.name=t", *args],
                       check=True, capture_output=True, env=env)
    return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def test_r6_reconciled_at_postdates_since_and_holds_every_linked_file(root):
    sha = _git_root(root)
    data = _register(reconciled_at=sha)
    assert tbr.check(data, root) == []
    data["items"][0]["since"] = "2026-10-03"
    assert any("predates the newest status" in f for f in tbr.check(data, root))
    data["items"][0]["since"] = "2026-10-01"
    (root / "docs" / "later.md").write_text("# Later\n", encoding="utf-8")  # added after sha
    data["items"][0]["evidence"] = ["../later.md"]
    assert any("docs/later.md does not exist at reconciled_at" in f for f in tbr.check(data, root))
    assert any("is not a commit" in f for f in tbr.check(_register(reconciled_at="abcdef1"), root))


# ---------------------------------------------------------------- I7 lint (R7)

def test_r7_inline_comment_truncation_is_caught():
    text = "items:\n  - next: rule after #611 lands\n    title: \"quoted # is fine\"\n  # full-line comment\n"
    assert len(tbr.lint(text)) == 1


# ---------------------------------------------------------------- I8 mirrors (R8)

def _plan(root, view="table", body="\n"):
    target = root / "docs" / "plan.md"
    target.write_text(
        f"# Plan\n\n<!-- BEGIN generated: track-b-register ({view}) -->{body}"
        "<!-- END generated: track-b-register -->\n\nafter\n",
        encoding="utf-8",
    )
    data = _register(role="owner")
    data["items"][0] = _row(status="OPEN", next="run it", next_actor="coordinator")
    return target, data, ((("docs/plan.md", view)),)


def test_r8_pilot_generates_nothing(root):
    assert tbr._targets(_register()) == ()
    assert tbr.write(_register(), root) == []
    assert tbr._targets(_register(role="owner")) == tbr.GENERATED_TARGETS


def test_r8_targets_are_fixed_in_code():
    assert tbr.GENERATED_TARGETS == (
        ("STATE.md", "summary"),
        ("docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md", "table"),
    )
    assert all(not p.startswith(("/", "..")) for p, _ in tbr.GENERATED_TARGETS)


@pytest.mark.parametrize("view", ["table", "summary"])
def test_r8_stale_block_then_write_makes_it_current(root, view):
    target, data, targets = _plan(root, view)
    assert _codes(tbr.check(data, root, targets=targets)) == ["R8"]
    assert tbr.write(data, root, targets) == ["docs/plan.md"]
    assert tbr.check(data, root, targets=targets) == []
    text = target.read_text(encoding="utf-8")
    assert text.startswith("# Plan\n") and text.endswith("\n\nafter\n")
    assert "slice.S5" in text and "defect.D-S5-1" not in text
    assert tbr.write(data, root, targets) == []


def test_r8_register_edit_makes_block_stale(root):
    _, data, targets = _plan(root)
    tbr.write(data, root, targets)
    data["items"][0]["next"] = "something else"
    assert _codes(tbr.check(data, root, targets=targets)) == ["R8"]


def test_r8_markers_must_appear_once(root):
    target, data, targets = _plan(root)
    target.write_text("no markers here\n", encoding="utf-8")
    findings = tbr.check(data, root, targets=targets)
    assert _codes(findings) == ["R8"] and "exactly one" in findings[0]
    with pytest.raises(tbr.Finding):
        tbr.write(data, root, targets)


def test_r8_view_mismatch(root):
    _, data, _ = _plan(root, view="summary")
    assert any("view" in f for f in tbr.check(data, root, targets=PLAN))


def test_write_preserves_crlf(root):
    target, data, targets = _plan(root)
    target.write_bytes(target.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert tbr.write(data, root, targets) == ["docs/plan.md"]
    raw = target.read_bytes()
    assert raw.count(b"\n") == raw.count(b"\r\n")
    assert tbr.check(data, root, targets=targets) == []


def test_mirrors_carry_notes(root):
    data = _register()
    data["items"] = [
        _row(status="OPEN", next="run it", next_actor="coordinator", note="not cleared to execute"),
        _row(id="gate.R1", kind="gate", aliases=[], status="BLOCKED", next="grant",
             next_actor="coordinator", blocked_by=["slice.S5"], note="barred until accepted"),
    ]
    for text in (tbr.render(data, "summary", "STATE.md"), tbr.table(data)):
        assert "not cleared to execute" in text and "barred until accepted" in text


@pytest.mark.parametrize(
    "target, expected",
    [("STATE.md", "docs/ledger.md#a"), ("docs/superpowers/plans/x.md", "../../ledger.md#a")],
)
def test_links_are_rewritten_relative_to_the_target(target, expected):
    assert tbr._relink("../ledger.md#a", target) == expected


def test_generated_header_routes_write_through_launcher():
    assert "python -I scripts/fp.py python scripts/track_b_register.py write" in tbr.render(
        _register(), "table", "docs/plan.md"
    )


# ---------------------------------------------------------------- I9 gate selection (R9)

def _gates(root, regex):
    (root / "scripts").mkdir(exist_ok=True)
    gate = {"id": "track-b-register", "when": {"staged_regex": regex}}
    (root / "scripts" / "gates.yml").write_text(yaml.safe_dump({"gates": [gate]}), encoding="utf-8")


def test_r9_gate_selector_covers_linked_files_and_gates_yml(root):
    _gates(root, "^docs/governance/track_b_register[.]yml$")
    findings = tbr.check(_register(), root)
    assert _codes(findings) == ["R9"]
    assert any("docs/ledger.md" in f for f in findings) and any("scripts/gates.yml" in f for f in findings)
    _gates(root, "^(docs/ledger[.]md|docs/governance/track_b_register[.]yml|scripts/track_b_register[.]py|scripts/gates[.]yml)$")
    assert tbr.check(_register(), root) == []


def test_r9_owner_role_adds_the_mirrors(root):
    _gates(root, "^(docs/ledger[.]md|docs/governance/track_b_register[.]yml|scripts/track_b_register[.]py|scripts/gates[.]yml)$")
    _, data, targets = _plan(root)
    tbr.write(data, root, targets)
    assert any("docs/plan.md" in f for f in tbr.check(data, root, targets=targets))


# ---------------------------------------------------------------- I10 readiness and expiry (views)

def test_check_is_independent_of_the_clock(root):
    data = _register()
    data["items"][0] = _row(status="OPEN", next="run it", next_actor="coordinator", expires="2000-01-01T00:00:00Z")
    assert tbr.check(data, root) == []


def test_waits_for_blocks_next_and_shows_in_views(root):
    data = _register()
    data["items"][0] = _row(status="OPEN", next="freeze", next_actor="operator", waits_for=["full behavior inventory"])
    assert tbr.check(data, root) == []
    nexts, blocked = tbr._groups(data["items"])
    assert nexts["operator"] == [] and blocked[0][1] == ["full behavior inventory"]
    assert "full behavior inventory" in tbr.table(data)


def test_digest_reports_expiry_next_and_blocked():
    data = _register()
    data["items"] = [
        _row(status="OPEN", next="run the screen", next_actor="coordinator", expires="2026-10-09T01:52:19Z"),
        _row(id="gate.R1", kind="gate", aliases=[], status="BLOCKED", next="grant",
             next_actor="coordinator", blocked_by=["slice.S5"]),
    ]
    text = tbr.digest(data, dt.datetime(2026, 10, 3, 12, tzinfo=dt.timezone.utc), 7)
    assert "Expiring within 7d" in text and "gate.R1 <- slice.S5" in text
    assert "grant" not in text.split("Blocked:")[0]
    later = tbr.digest(data, dt.datetime(2026, 10, 10, tzinfo=dt.timezone.utc), 7)
    assert "EXPIRED" in later and "Next (coordinator)" not in later


def test_digest_carries_row_notes():
    data = _register()
    data["items"][0] = _row(status="OPEN", next="run it", next_actor="coordinator", note="scope limit")
    assert "note: scope limit" in tbr.digest(data, dt.datetime(2026, 10, 3, tzinfo=dt.timezone.utc), 7)


def test_expiry_lapsed_terminal_row_satisfies_nothing():
    data = _register()
    data["items"] = [
        _row(status="ACCEPTED", expires="2026-10-09T01:52:19Z"),
        _row(id="gate.R1", kind="gate", aliases=[], status="OPEN", next="grant",
             next_actor="coordinator", blocked_by=["slice.S5"]),
    ]
    before = tbr.digest(data, dt.datetime(2026, 10, 8, tzinfo=dt.timezone.utc), 7)
    assert "slice.S5" in before.split("Next")[0] and "gate.R1: grant" in before
    after = tbr.digest(data, dt.datetime(2026, 10, 10, tzinfo=dt.timezone.utc), 7)
    assert "gate.R1 <- slice.S5 (expired)" in after and "gate.R1: grant" not in after
    assert "Expires 2026-10-09T01:52Z" in tbr.render(data, "summary", "STATE.md")
    assert "2026-10-09T01:52Z" in tbr.table(data)


def test_table_lists_open_rows_and_escapes_pipes():
    data = _register()
    data["items"].append(_row(id="gate.R1", kind="gate", aliases=[], status="OPEN", next="a | b", next_actor="operator"))
    table = tbr.table(data)
    assert "gate.R1" in table and "defect.D-S5-1" not in table and "a \\| b" in table


# ---------------------------------------------------------------- digest safety

def test_hook_digest_never_fails(tmp_path):
    bad = tmp_path / "bad.yml"
    bad.write_text("items: [\n", encoding="utf-8")
    result = subprocess.run([sys.executable, str(SCRIPT), "digest", "--hook", "--register", str(bad)],
                            capture_output=True, text=True)
    assert result.returncode == 0 and result.stdout.startswith("track-b register digest unavailable:")


def test_hook_digest_unavailable_on_status_finding(tmp_path, capsys):
    reg = tmp_path / "r.yml"
    bad = _register()
    bad["items"][0] = _row(status="OPEN", next=None, next_actor="coordinator")
    reg.write_text(yaml.safe_dump(bad), encoding="utf-8")
    assert tbr.main(["digest", "--hook", "--register", str(reg)]) == 0
    assert "unavailable" in capsys.readouterr().out


@pytest.mark.parametrize("target", [("../STATE.md", "table"), ("/abs.md", "table"), ("C:/x.md", "table"), ("ok.md", "pie")])
def test_r8_target_list_cannot_leave_the_checkout(target):
    with pytest.raises(tbr.Finding):
        tbr._targets(_register(role="owner"), (target,))
