"""Acceptance tests for scripts/track_b_register.py.

The committed register must pass; each synthetic case names the rule it must
violate. Synthetic registers live in a temporary repository tree so link and
coverage checks run against files the test controls.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
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

OWNER_MD = """\
# Ledger

### Operator ruling — thing accepted, 2026-10-01

text

### Coordinator acceptance — fix slice (#586), 2026-10-02

```
### 2026-10-05 not a heading inside a fence
```

### Old entry, 2026-09-20

<a id="addendum-2026-09-30b"></a>
"""


def _row(**over):
    row = {
        "id": "slice.S5",
        "kind": "slice",
        "aliases": ["T04"],
        "title": "Part A",
        "status": "ACCEPTED_LIMITED",
        "since": "2026-10-01",
        "owner": "../ledger.md#operator-ruling--thing-accepted-2026-10-01",
        "next": None,
        "next_actor": "none",
    }
    row.update(over)
    return row


def _register(**over):
    data = {
        "schema": "track_b_register/v1",
        "role": "owner",
        "as_of": "2026-10-03",
        "reconciled_at": "d5d559b",
        "covers_from": "2026-10-01",
        "watch": ["docs/ledger.md"],
        "items": [
            _row(),
            _row(
                id="defect.D-S5-1",
                kind="defect",
                aliases=[],
                status="CLOSED",
                owner="../ledger.md#coordinator-acceptance--fix-slice-586-2026-10-02",
            ),
        ],
    }
    data.update(over)
    return data


@pytest.fixture
def root(tmp_path):
    (tmp_path / "docs" / "governance").mkdir(parents=True)
    (tmp_path / "docs" / "ledger.md").write_text(OWNER_MD, encoding="utf-8")
    return tmp_path


def _codes(findings):
    return sorted({f.split(" ", 1)[0] for f in findings})


def test_committed_register_passes():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "check"], capture_output=True, text=True, cwd=REPO
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_clean_synthetic_register(root):
    assert tbr.check(_register(), root) == []


@pytest.mark.parametrize(
    "heading, anchor",
    [
        ("Operator ruling — C3 accepted; S5 accepted for TEST_ONLY on landing, 2026-10-01",
         "operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01"),
        ("Coordinator acceptance — D-S5-1/D-S5-2 fix slice (#586), 2026-10-02",
         "coordinator-acceptance--d-s5-1d-s5-2-fix-slice-586-2026-10-02"),
        ("Harness fix `b5f53da` read; fresh Stage 1c approval, 2026-09-29",
         "harness-fix-b5f53da-read-fresh-stage-1c-approval-2026-09-29"),
        ("T05 environment sealing (C′)", "t05-environment-sealing-c"),
        ("See [the ruling](x.md#y) here", "see-the-ruling-here"),
    ],
)
def test_slug_matches_github(heading, anchor):
    assert tbr.slugify(heading) == anchor


def test_repeated_headings_get_suffixes_and_fences_are_skipped():
    amap = tbr.anchors("# A\n# A\n```\n# B\n```\n<a id=\"x-y\"></a>\n")
    assert set(amap) == {"a", "a-1", "x-y"}


def test_r1_bad_status_and_actor(root):
    data = _register()
    data["items"][0] = _row(status="DONE", next_actor="robot")
    assert _codes(tbr.check(data, root)) == ["R1"]


def test_r1_id_prefix_must_match_kind(root):
    data = _register()
    data["items"][0] = _row(id="gate.S5")
    assert "R1" in _codes(tbr.check(data, root))


def test_r1_next_needs_actor(root):
    data = _register()
    data["items"][0] = _row(next="do it", next_actor="none")
    assert _codes(tbr.check(data, root)) == ["R1"]


def test_r1_expiry_needs_zone(root):
    data = _register()
    data["items"][0] = _row(expires="2026-10-09T01:52:19")
    assert _codes(tbr.check(data, root)) == ["R1"]


def test_r2_alias_collides_with_other_row(root):
    data = _register()
    data["items"][1]["aliases"] = ["t04"]  # casefolded collision with slice.S5's alias
    assert _codes(tbr.check(data, root)) == ["R2"]


def test_r2_repeated_id_without_aliases(root):
    data = _register()
    dup = dict(data["items"][1], status="ACCEPTED", next=None, next_actor="none")
    dup.pop("aliases", None)
    data["items"].append(dup)
    findings = tbr.check(data, root)
    assert any(f.startswith("R2 ") and "2 rows" in f for f in findings)
    with pytest.raises(tbr.Finding):
        tbr._groups(data["items"])


def test_r3_unknown_reference_and_cycle(root):
    data = _register()
    data["items"][0]["blocked_by"] = ["defect.D-S5-1"]
    data["items"][1]["blocked_by"] = ["slice.S5", "ghost.X"]
    findings = tbr.check(data, root)
    assert any("cycle" in f for f in findings)
    assert any("ghost.X" in f for f in findings)


def test_r3_checkpoint_must_be_checkpoint_row(root):
    data = _register()
    data["items"][0]["checkpoint"] = "defect.D-S5-1"
    assert _codes(tbr.check(data, root)) == ["R3"]


def test_r4_missing_anchor_and_file(root):
    data = _register()
    data["items"][0]["owner"] = "../ledger.md#no-such-heading"
    data["items"][1]["evidence"] = ["../missing.md"]
    findings = [f for f in tbr.check(data, root) if f.startswith("R4")]
    assert len(findings) == 2


def test_r4_html_anchor_resolves(root):
    data = _register()
    data["items"][0]["evidence"] = ["../ledger.md#addendum-2026-09-30b"]
    assert tbr.check(data, root) == []


def test_r4_external_links_refused(root):
    data = _register()
    data["items"][0]["evidence"] = ["https://example.com/x"]
    assert _codes(tbr.check(data, root)) == ["R4"]


def test_r5_new_dated_heading_needs_a_row(root):
    (root / "docs" / "ledger.md").write_text(
        OWNER_MD + "\n### Operator ruling — new thing, 2026-10-03\n", encoding="utf-8"
    )
    findings = tbr.check(_register(), root)
    assert _codes(findings) == ["R5"]
    assert "operator-ruling--new-thing-2026-10-03" in findings[0]


def test_r5_noted_entry_discharges_coverage(root):
    (root / "docs" / "ledger.md").write_text(
        OWNER_MD + "\n### Archive record (2026-10-03)\n", encoding="utf-8"
    )
    data = _register(noted=[{"link": "../ledger.md#archive-record-2026-10-03", "reason": "no status change"}])
    assert tbr.check(data, root) == []


def test_r5_headings_before_covers_from_are_exempt(root):
    data = _register(covers_from="2026-10-02")
    data["items"] = [data["items"][1]]
    assert tbr.check(data, root) == []


def test_r7_inline_comment_truncation_is_caught():
    text = "items:\n  - next: rule after #611 lands\n    title: \"quoted # is fine\"\n  # full-line comment\n"
    assert [f.split(" ", 2)[1] for f in tbr.lint(text)] == ["line"]
    assert len(tbr.lint(text)) == 1


def test_check_is_independent_of_the_clock(root):
    data = _register()
    data["items"][0] = _row(status="OPEN", next="run it", next_actor="coordinator",
                            expires="2000-01-01T00:00:00Z")
    assert tbr.check(data, root) == []


def test_digest_reports_expiry_next_and_blocked(root):
    data = _register()
    data["items"] = [
        _row(status="OPEN", next="run the screen", next_actor="coordinator",
             expires="2026-10-09T01:52:19Z"),
        _row(id="gate.R1", kind="gate", aliases=[], status="BLOCKED", next="grant",
             next_actor="coordinator", blocked_by=["slice.S5"]),
    ]
    now = dt.datetime(2026, 10, 3, 12, tzinfo=dt.timezone.utc)
    text = tbr.digest(data, now, 7)
    assert "Expiring within 7d" in text and "slice.S5" in text
    assert "gate.R1 <- slice.S5" in text
    assert "grant" not in text.split("Blocked:")[0]  # blocked rows are not offered as next
    later = tbr.digest(data, dt.datetime(2026, 10, 10, tzinfo=dt.timezone.utc), 7)
    assert "EXPIRED" in later


def test_table_lists_open_rows_only(root):
    data = _register()
    data["items"].append(_row(id="gate.R1", kind="gate", aliases=[], status="OPEN",
                              next="a | b", next_actor="operator"))
    table = tbr.table(data)
    assert "gate.R1" in table and "defect.D-S5-1" not in table
    assert "a \\| b" in table


def test_committed_register_parses_values_whole():
    """Guard the committed file against comment truncation via the lint as well."""
    text = (REPO / "docs" / "governance" / "track_b_register.yml").read_text(encoding="utf-8")
    assert tbr.lint(text) == []
    assert yaml.safe_load(text)["schema"] == "track_b_register/v1"


def test_r1_role_must_be_owner(root):
    assert _codes(tbr.check(_register(role="derived-mirror"), root)) == ["R1"]


def _with_target(root, view="table", body="\n"):
    target = root / "docs" / "plan.md"
    target.write_text(
        "# Plan\n\n"
        f"<!-- BEGIN generated: track-b-register ({view}) -->{body}"
        "<!-- END generated: track-b-register -->\n\nafter\n",
        encoding="utf-8",
    )
    data = _register(generated=[{"path": "docs/plan.md", "view": view}])
    data["items"][0] = _row(status="OPEN", next="run it", next_actor="coordinator")
    return target, data


@pytest.mark.parametrize("view", ["table", "summary"])
def test_r8_stale_block_then_write_makes_it_current(root, view):
    target, data = _with_target(root, view)
    assert _codes(tbr.check(data, root)) == ["R8"]
    assert tbr.write(data, root) == ["docs/plan.md"]
    assert tbr.check(data, root) == []
    text = target.read_text(encoding="utf-8")
    assert text.startswith("# Plan\n") and text.endswith("\n\nafter\n")
    assert "slice.S5" in text and "defect.D-S5-1" not in text  # open rows only
    assert tbr.write(data, root) == []  # idempotent


def test_r8_register_edit_makes_block_stale(root):
    _, data = _with_target(root)
    tbr.write(data, root)
    data["items"][0]["next"] = "something else"
    assert _codes(tbr.check(data, root)) == ["R8"]


def test_r8_markers_must_appear_once(root):
    target, data = _with_target(root)
    target.write_text("no markers here\n", encoding="utf-8")
    findings = tbr.check(data, root)
    assert _codes(findings) == ["R8"] and "exactly one" in findings[0]
    with pytest.raises(tbr.Finding):
        tbr.write(data, root)


def test_r8_view_mismatch(root):
    _, data = _with_target(root, view="summary")
    data["generated"][0]["view"] = "table"
    assert any("view" in f for f in tbr.check(data, root))


def test_r1_generated_entry_shape(root):
    data = _register(generated=[{"path": "STATE.md", "view": "pie"}])
    assert "R1" in _codes(tbr.check(data, root))


@pytest.mark.parametrize(
    "target, expected",
    [
        ("STATE.md", "docs/ledger.md#a"),
        ("docs/superpowers/plans/x.md", "../../ledger.md#a"),
        ("docs/governance/y.md", "../ledger.md#a"),
    ],
)
def test_links_are_rewritten_relative_to_the_target(target, expected):
    assert tbr._relink("../ledger.md#a", target) == expected


def test_summary_lists_expiry_and_hides_blocked_next(root):
    data = _register()
    data["items"] = [
        _row(status="OPEN", next="run the screen", next_actor="coordinator",
             expires="2026-10-09T01:52:19Z"),
        _row(id="gate.R1", kind="gate", aliases=[], status="BLOCKED", next="grant",
             next_actor="coordinator", blocked_by=["slice.S5"]),
    ]
    text = tbr.render(data, "summary", "STATE.md")
    assert "**Expires 2026-10-09T01:52Z:** `slice.S5`" in text
    assert "`gate.R1` ← slice.S5" in text
    assert "grant" not in text


def test_hook_digest_never_fails(tmp_path):
    bad = tmp_path / "bad.yml"
    bad.write_text("items: [\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "digest", "--hook", "--register", str(bad)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert result.stdout.startswith("track-b register digest unavailable:")


def test_committed_generated_blocks_are_current():
    data = tbr.load(tbr.DEFAULT_REGISTER)
    assert [f for f in tbr.check(data) if f.startswith("R8")] == []


def test_digest_drops_expired_rows_from_next(root):
    data = _register()
    data["items"] = [_row(status="OPEN", next="run the screen", next_actor="coordinator",
                          expires="2026-10-09T01:52:19Z")]
    later = tbr.digest(data, dt.datetime(2026, 10, 10, tzinfo=dt.timezone.utc), 7)
    assert "EXPIRED" in later and "Next (coordinator)" not in later


def test_waits_for_blocks_next_and_shows_in_views(root):
    data = _register()
    data["items"][0] = _row(status="OPEN", next="freeze", next_actor="operator",
                            waits_for=["full behavior inventory"])
    assert tbr.check(data, root) == []
    nexts, blocked = tbr._groups(data["items"])
    assert nexts["operator"] == [] and blocked[0][1] == ["full behavior inventory"]
    assert "full behavior inventory" in tbr.table(data)


def test_r1_naive_yaml_datetime_expiry_rejected(root):
    data = _register()
    data["items"][0] = _row(expires=yaml.safe_load("x: 2026-10-09T01:52:19")["x"])
    assert _codes(tbr.check(data, root)) == ["R1"]


def test_r6_as_of_must_cover_every_since(root):
    data = _register()
    data["items"][0] = _row(since="2026-10-04")
    assert _codes(tbr.check(data, root)) == ["R6"]


def test_write_preserves_crlf(root):
    target, data = _with_target(root, "table")
    target.write_bytes(target.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert tbr.write(data, root) == ["docs/plan.md"]
    raw = target.read_bytes()
    assert raw.count(b"\n") == raw.count(b"\r\n")
    assert tbr.check(data, root) == []


def test_r9_gate_selector_covers_cited_files(root):
    (root / "scripts").mkdir()
    gates = root / "scripts" / "gates.yml"
    gate = {"id": "track-b-register", "when": {"staged_regex": "^docs/governance/track_b_register[.]yml$"}}
    gates.write_text(yaml.safe_dump({"gates": [gate]}), encoding="utf-8")
    findings = tbr.check(_register(), root)
    assert _codes(findings) == ["R9"] and any("docs/ledger.md" in f for f in findings)
    gate["when"]["staged_regex"] = "^(docs/ledger[.]md|docs/governance/track_b_register[.]yml|scripts/track_b_register[.]py|scripts/gates[.]yml)$"
    gates.write_text(yaml.safe_dump({"gates": [gate]}), encoding="utf-8")
    assert tbr.check(_register(), root) == []


def test_r9_gate_selector_must_select_gates_yml(root):
    (root / "scripts").mkdir()
    regex = "^(docs/ledger[.]md|docs/governance/track_b_register[.]yml|scripts/track_b_register[.]py)$"
    gate = {"id": "track-b-register", "when": {"staged_regex": regex}}
    (root / "scripts" / "gates.yml").write_text(yaml.safe_dump({"gates": [gate]}), encoding="utf-8")
    assert any("scripts/gates.yml" in f for f in tbr.check(_register(), root))


def test_r5_any_heading_date_on_or_after_covers_from_needs_a_row(root):
    ledger = root / "docs" / "ledger.md"
    ledger.write_text(OWNER_MD + "\n### Superseded 2026-09-20 ruling, re-ruled 2026-10-04\n", encoding="utf-8")
    assert "R5" in _codes(tbr.check(_register(), root))


def test_expiry_offset_is_converted_to_utc():
    assert tbr._expiry("2026-10-09T01:00:00-04:00") == dt.datetime(2026, 10, 9, 5, tzinfo=dt.timezone.utc)
    aware = dt.datetime(2026, 10, 9, 1, tzinfo=dt.timezone(dt.timedelta(hours=-4)))
    assert tbr._expiry(aware).hour == 5


def test_production_register_requires_generated(root):
    assert tbr.check(_register(), root) == []
    assert "R1" in _codes(tbr.check(_register(), root, production=True))


@pytest.mark.parametrize("over", [
    {"status": "OPEN", "next": None, "next_actor": "coordinator"},
    {"status": "ACCEPTED", "next": "do more", "next_actor": "coordinator"},
])
def test_r1_next_and_actor_agree_with_status(root, over):
    data = _register()
    data["items"][0] = _row(**over)
    assert _codes(tbr.check(data, root)) == ["R1"]


def test_hook_digest_unavailable_on_status_finding(tmp_path, capsys):
    reg = tmp_path / "r.yml"
    bad = _register()
    bad["items"][0] = _row(status="OPEN", next=None, next_actor="coordinator")
    reg.write_text(yaml.safe_dump(bad), encoding="utf-8")
    assert tbr.main(["digest", "--hook", "--register", str(reg)]) == 0
    assert "unavailable" in capsys.readouterr().out
