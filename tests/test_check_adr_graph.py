"""Unit tests for scripts/check_adr_graph.py - ADR lifecycle graph gate."""
from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_PATH = REPO_ROOT / "scripts" / "check_adr_graph.py"
_spec = importlib.util.spec_from_file_location("check_adr_graph", _PATH)
cag = importlib.util.module_from_spec(_spec)
# Register before exec so @dataclass resolves (Python 3.14+)
sys.modules[_spec.name] = cag
_spec.loader.exec_module(cag)


HEADER_ACCEPTED = """# Title

**Status:** `Accepted` - operator executive decision, recorded
**Decision date:** 2026-05-14
**Supersedes:** `2026-04-17-portfolio-allocations.md` in part - Striker only
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

---

## §2 - Decision

body
"""


def test_header_region_stops_at_hr_or_h2():
    region, end = cag.header_region(HEADER_ACCEPTED)
    assert "**Status:**" in region
    assert "## §2" not in region
    assert end >= 8


def test_parse_status_token_keeps_annotation():
    tok, ann = cag.parse_status_token("`Accepted` - operator executive decision, recorded")
    assert tok == "Accepted"
    assert "operator" in ann


def test_parse_status_token_normalizes_case_unquoted():
    tok, ann = cag.parse_status_token("ACCEPTED (with override)")
    assert tok == "Accepted"
    assert "override" in ann or ann.startswith("(")


def test_load_adr_headers_skips_directory_readme(tmp_path):
    (tmp_path / "README.md").write_text("# hops only\n", encoding="utf-8")
    (tmp_path / "2026-05-14-example.md").write_text(HEADER_ACCEPTED, encoding="utf-8")
    headers = cag.load_adr_headers(tmp_path)
    assert "README.md" not in headers
    assert "2026-05-14-example.md" in headers


def test_parse_adr_header_ignores_status_after_body():
    text = HEADER_ACCEPTED + "\n## Addendum\n\n**Status:** `Withdrawn`\n"
    h = cag.parse_adr_header("docs/adr/x.md", text)
    assert h.status == "Accepted"
    assert len(h.supersedes) == 1
    assert h.supersedes[0].target == "2026-04-17-portfolio-allocations.md"
    assert h.supersedes[0].scope == "in_part"


def test_parse_eventful_in_part():
    text = """# t

**Status:** `Accepted`
**Decision date:** 2026-05-18
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `event:merge-reality` - lock action not adopted
**Retain-until:** none

## Body
"""
    h = cag.parse_adr_header("docs/adr/y.md", text)
    assert h.superseded_in_part_by[0].kind == "event"
    assert h.superseded_in_part_by[0].target == "merge-reality"


def test_parse_edge_value_recognizes_markdown_link_style():
    """Regression: 2026-07-22-prop-portfolio-s4-discharge-withdrawal.md's real
    Supersedes line uses [`file.md`](file.md) instead of the bare `file.md`
    ADR_FILE_RE expects. Before the fix this silently returned None -- no
    finding, edge just absent -- so check_a2 never required the four-firms ADR
    to carry the reciprocal Superseded-in-part-by. The graph reported OK while
    STATE.md separately drifted on the exact same fact (2026-07-24 incident).
    """
    value = ("[`2026-07-12-prop-portfolio-four-friendly-firms.md`]"
              "(2026-07-12-prop-portfolio-four-friendly-firms.md) in part "
              "— the §4 discharge status only.")
    e = cag.parse_edge_value("Supersedes", value, 8)
    assert e is not None
    assert e.kind == "adr"
    assert e.target == "2026-07-12-prop-portfolio-four-friendly-firms.md"
    assert e.scope == "in_part"


def test_a2_markdown_link_supersede_requires_reverse(tmp_path: Path):
    """Integration-level version of the same regression: a Supersedes line
    written in markdown-link style must still trip A2 when the target lacks
    the reciprocal edge, and must still pass once it's added -- proving the
    parser fix actually feeds check_a2, not just parse_edge_value in isolation.
    """
    _write_adr(tmp_path, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    _write_adr(tmp_path, "2026-02-01-new.md", """# new
**Status:** `Accepted`
**Decision date:** 2026-02-01
**Supersedes:** [`2026-01-01-old.md`](2026-01-01-old.md) in part - clause text
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    findings = cag.check_a2(cag.load_adr_headers(tmp_path))
    assert len(findings) == 1
    assert "missing Superseded-in-part-by" in findings[0].message

    _write_adr(tmp_path, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-02-01-new.md` - clause text
**Retain-until:** none

## body
""")
    assert cag.check_a2(cag.load_adr_headers(tmp_path)) == []


def _write_adr(tmp: Path, name: str, body: str) -> Path:
    p = tmp / name
    p.write_text(body, encoding="utf-8")
    return p


def test_a1_rejects_unknown_status_token(tmp_path: Path):
    _write_adr(tmp_path, "2026-01-01-bad.md", """# t
**Status:** `Funky`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## x
""")
    headers = cag.load_adr_headers(tmp_path)
    findings = cag.check_a1(headers)
    assert any(f.code == "A1" for f in findings)


def test_a1_accepts_annotated_accepted(tmp_path: Path):
    _write_adr(tmp_path, "2026-01-01-ok.md", """# t
**Status:** `Accepted` - with documented dissent
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## x
""")
    findings = cag.check_a1(cag.load_adr_headers(tmp_path))
    assert findings == []


def test_a2_pending_proposed_supersede_does_not_require_reverse(tmp_path: Path):
    _write_adr(tmp_path, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    _write_adr(tmp_path, "2026-02-01-new.md", """# new
**Status:** `Proposed`
**Decision date:** 2026-02-01
**Supersedes:** `2026-01-01-old.md` full
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    assert cag.check_a2(cag.load_adr_headers(tmp_path)) == []


def test_a2_accepted_full_requires_reverse_and_superseded_status(tmp_path: Path):
    _write_adr(tmp_path, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    _write_adr(tmp_path, "2026-02-01-new.md", """# new
**Status:** `Accepted`
**Decision date:** 2026-02-01
**Supersedes:** `2026-01-01-old.md` full
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    codes = {f.code for f in cag.check_a2(cag.load_adr_headers(tmp_path))}
    assert "A2" in codes


def test_a2_in_part_matches_file_not_clause_text(tmp_path: Path):
    _write_adr(tmp_path, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-02-01-new.md` - DIFFERENT CLAUSE TEXT
**Retain-until:** none

## body
""")
    _write_adr(tmp_path, "2026-02-01-new.md", """# new
**Status:** `Accepted`
**Decision date:** 2026-02-01
**Supersedes:** `2026-01-01-old.md` in part - original clause
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    assert cag.check_a2(cag.load_adr_headers(tmp_path)) == []


def test_a2_event_in_part_needs_no_reverse_adr(tmp_path: Path):
    _write_adr(tmp_path, "2026-05-18-merge.md", """# m
**Status:** `Accepted`
**Decision date:** 2026-05-18
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `event:merge-reality` - lock action not adopted
**Retain-until:** none

## body
""")
    assert cag.check_a2(cag.load_adr_headers(tmp_path)) == []


STUB_VALID = """# old stub

**Status:** `Superseded`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** `2026-02-01-new.md`
**Superseded-in-part-by:** none
**Retain-until:** none

**Body:** `docs/ltm/adr/{name}`

One-line disposition.
"""


def _stub(name: str, status: str = "Superseded", body_name: str | None = None) -> str:
    bn = body_name or name
    return STUB_VALID.format(name=bn).replace("`Superseded`", f"`{status}`")


def test_is_stub_valid():
    name = "2026-01-01-old.md"
    assert cag.is_stub(_stub(name), name)


def test_is_stub_rejects_h2():
    name = "2026-01-01-old.md"
    text = _stub(name) + "\n## Decision\n"
    assert not cag.is_stub(text, name)


def test_is_stub_rejects_wrong_body_link():
    name = "2026-01-01-old.md"
    text = _stub(name, body_name="other.md")
    assert not cag.is_stub(text, name)


def test_a3_proposed_supersede_fat_x_passes(tmp_path: Path):
    adr = tmp_path / "adr"
    ltm = tmp_path / "ltm"
    adr.mkdir()
    ltm.mkdir()
    _write_adr(adr, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body still hot
""")
    _write_adr(adr, "2026-02-01-new.md", """# new
**Status:** `Proposed`
**Decision date:** 2026-02-01
**Supersedes:** `2026-01-01-old.md` full
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    headers = cag.load_adr_headers(adr)
    assert cag.check_a3(headers, adr, ltm) == []


def test_a3_fat_superseded_fails(tmp_path: Path):
    adr = tmp_path / "adr"
    ltm = tmp_path / "ltm"
    adr.mkdir()
    ltm.mkdir()
    _write_adr(adr, "2026-01-01-old.md", """# old
**Status:** `Superseded`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** `2026-02-01-new.md`
**Superseded-in-part-by:** none
**Retain-until:** none

## Decision

still here
""")
    headers = cag.load_adr_headers(adr)
    findings = cag.check_a3(headers, adr, ltm)
    assert any(f.code == "A3" for f in findings)
    assert any("not stub-shaped" in f.message for f in findings)


def test_a3_stub_ltm_status_mismatch_fails(tmp_path: Path):
    adr = tmp_path / "adr"
    ltm = tmp_path / "ltm"
    adr.mkdir()
    ltm.mkdir()
    name = "2026-01-01-old.md"
    _write_adr(adr, name, _stub(name, status="Superseded"))
    _write_adr(ltm, name, """# old body
**Status:** `Withdrawn`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** `2026-02-01-new.md`
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    findings = cag.check_a3(cag.load_adr_headers(adr), adr, ltm)
    assert any(f.code == "A3" and "!= LTM Status" in f.message for f in findings)


def test_a3_valid_stub_with_ltm_passes(tmp_path: Path):
    adr = tmp_path / "adr"
    ltm = tmp_path / "ltm"
    adr.mkdir()
    ltm.mkdir()
    name = "2026-01-01-old.md"
    _write_adr(adr, name, _stub(name, status="Superseded"))
    _write_adr(ltm, name, """# old body
**Status:** `Superseded`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** `2026-02-01-new.md`
**Superseded-in-part-by:** none
**Retain-until:** none

## full body in LTM
""")
    assert cag.check_a3(cag.load_adr_headers(adr), adr, ltm) == []


def test_a4_accepted_stub_only_fails(tmp_path: Path):
    adr = tmp_path / "adr"
    ltm = tmp_path / "ltm"
    adr.mkdir()
    ltm.mkdir()
    name = "2026-01-01-hot.md"
    _write_adr(adr, name, _stub(name, status="Accepted"))
    findings = cag.check_a4(cag.load_adr_headers(adr), adr, ltm)
    assert any(f.code == "A4" for f in findings)
    assert len([f for f in findings if f.code == "A4"]) == 1


def test_a4_accepted_full_body_passes(tmp_path: Path):
    adr = tmp_path / "adr"
    ltm = tmp_path / "ltm"
    adr.mkdir()
    ltm.mkdir()
    _write_adr(adr, "2026-01-01-hot.md", """# hot
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## Decision

full hot body
""")
    assert cag.check_a4(cag.load_adr_headers(adr), adr, ltm) == []


def test_render_index_sections_and_a6_drift(tmp_path: Path):
    _write_adr(tmp_path, "2026-01-01-a.md", """# a
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## b
""")
    headers = cag.load_adr_headers(tmp_path)
    idx = cag.render_index(headers)
    assert "## Live" in idx
    assert "2026-01-01-a.md" in idx
    assert cag.check_a6(headers, idx) == []
    assert cag.check_a6(headers, idx + "\n") == []


def test_index_notes_passthrough_at_or_under_cap():
    short = "operator GO 2026-08-03 (shape 1)."
    assert cag._index_notes(short) == short
    exact = " ".join(f"w{i}" for i in range(cag.INDEX_NOTES_MAX_WORDS))
    assert cag._index_notes(exact) == exact
    assert cag._index_notes("") == ""
    assert cag._index_notes("   ") == ""


def test_index_notes_clips_over_cap_and_drops_broken_link():
    words = [f"w{i}" for i in range(cag.INDEX_NOTES_MAX_WORDS + 5)]
    clipped = cag._index_notes(" ".join(words))
    assert clipped.endswith(cag.INDEX_NOTES_ELLIPSIS)
    assert clipped.split()[: cag.INDEX_NOTES_MAX_WORDS] == words[: cag.INDEX_NOTES_MAX_WORDS]
    assert "w40" not in clipped
    prefix = " ".join(f"w{i}" for i in range(cag.INDEX_NOTES_MAX_WORDS - 2))
    broken = cag._index_notes(
        f"{prefix} see [full note](2026-07-22-challenge-era-substrate-retirement.md) leftover words here extra extra"
    )
    assert "[full note](" not in broken
    assert broken.endswith(cag.INDEX_NOTES_ELLIPSIS)


def test_render_index_clips_long_status_annotation(tmp_path: Path):
    essay = " ".join(f"phase{i}" for i in range(80))
    _write_adr(tmp_path, "2026-01-01-a.md", f"""# a
**Status:** `Accepted` — {essay}
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## b
""")
    headers = cag.load_adr_headers(tmp_path)
    assert headers["2026-01-01-a.md"].status_annotation == essay
    idx = cag.render_index(headers)
    assert essay not in idx
    assert "phase0" in idx
    assert "phase39" in idx
    assert "phase40" not in idx
    assert cag.INDEX_NOTES_ELLIPSIS.strip() in idx
    assert "40 words" in idx


def test_a3_public_seed_missing_ltm_dir_is_silent(tmp_path: Path):
    """docs/ltm/** is excluded from the public seed; missing dir is not A3."""
    adr = tmp_path / "adr"
    ltm = tmp_path / "ltm"  # deliberately not created
    adr.mkdir()
    name = "2026-01-01-old.md"
    _write_adr(adr, name, _stub(name, status="Superseded"))
    assert cag.check_a3(cag.load_adr_headers(adr), adr, ltm) == []


def test_main_bare_cli_exits_zero():
    assert cag.main([]) == 0


def test_main_enable_unknown_exits_nonzero(capsys):
    """A typo in --enable used to disable every real check and still print OK."""
    assert cag.main(["--enable", "NOPE"]) == 2
    err = capsys.readouterr().err
    assert "NOPE" in err
    assert "unknown check" in err


def test_main_enable_mixed_unknown_lists_invalid(capsys):
    assert cag.main(["--enable", "A1,NOPE,A2"]) == 2
    err = capsys.readouterr().err
    assert "unknown check(s): ['NOPE']" in err
    assert "valid=" in err


def test_main_enable_valid_opt_in_accepted():
    assert cag.main(["--enable", "A1"]) == 0


def test_main_regenerate_index(tmp_path: Path):
    adr = tmp_path / "docs" / "adr"
    adr.mkdir(parents=True)
    _write_adr(adr, "2026-01-01-a.md", """# a
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## b
""")
    assert cag.main(["--repo-root", str(tmp_path), "--regenerate-index"]) == 0
    idx_path = adr / "INDEX.md"
    assert idx_path.is_file()
    headers = cag.load_adr_headers(adr)
    assert cag.check_a6(headers, idx_path.read_text(encoding="utf-8")) == []

def _accepted_adr(name: str, decision: str, retain: str = "none", in_part: str = "none") -> str:
    return f"""# t
**Status:** `Accepted`
**Decision date:** {decision}
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** {in_part}
**Retain-until:** {retain}

## Decision

body
"""


def _setup_repo(tmp: Path) -> tuple[Path, Path]:
    adr = tmp / "docs" / "adr"
    adr.mkdir(parents=True)
    return tmp, adr


def test_a5_old_accepted_no_refs_fires(tmp_path: Path):
    repo, adr = _setup_repo(tmp_path)
    name = "2026-01-15-stale.md"
    _write_adr(adr, name, _accepted_adr(name, "2026-01-15"))
    headers = cag.load_adr_headers(adr)
    findings = cag.check_a5(headers, repo, today=date(2026, 10, 1))
    assert any(f.code == "A5" for f in findings)


def test_a5_retain_until_future_passes(tmp_path: Path):
    repo, adr = _setup_repo(tmp_path)
    name = "2026-01-15-stale.md"
    _write_adr(adr, name, _accepted_adr(name, "2026-01-15", retain="2026-12-01"))
    headers = cag.load_adr_headers(adr)
    assert cag.check_a5(headers, repo, today=date(2026, 10, 1)) == []


def test_a5_inbound_ref_in_methodology_passes(tmp_path: Path):
    repo, adr = _setup_repo(tmp_path)
    name = "2026-01-15-stale.md"
    _write_adr(adr, name, _accepted_adr(name, "2026-01-15"))
    meth = tmp_path / "docs" / "methodology" / "foo.md"
    meth.parent.mkdir(parents=True)
    meth.write_text("See [`" + name + "`](docs/adr/" + name + ") for context.\n", encoding="utf-8")
    headers = cag.load_adr_headers(adr)
    assert cag.check_a5(headers, repo, today=date(2026, 10, 1)) == []


def test_a5_event_in_part_exempt(tmp_path: Path):
    repo, adr = _setup_repo(tmp_path)
    name = "2026-05-18-merge.md"
    _write_adr(
        adr,
        name,
        _accepted_adr(name, "2026-01-15", in_part="`event:merge-reality` - note"),
    )
    headers = cag.load_adr_headers(adr)
    assert cag.check_a5(headers, repo, today=date(2026, 10, 1)) == []


def test_a5_too_young_passes(tmp_path: Path):
    repo, adr = _setup_repo(tmp_path)
    name = "2026-05-01-recent.md"
    _write_adr(adr, name, _accepted_adr(name, "2026-05-01"))
    headers = cag.load_adr_headers(adr)
    assert cag.check_a5(headers, repo, today=date(2026, 10, 1)) == []


def test_has_inbound_ref_skips_self_and_index(tmp_path: Path):
    repo, adr = _setup_repo(tmp_path)
    name = "2026-01-15-stale.md"
    self_path = adr / name
    self_path.write_text(_accepted_adr(name, "2026-01-15"), encoding="utf-8")
    (adr / "INDEX.md").write_text("row for docs/adr/" + name + "\n", encoding="utf-8")
    surfaces = list(cag.iter_a5_surfaces(repo))
    assert not cag.has_inbound_ref(name, surfaces, self_path)


def test_iter_a5_surfaces_includes_archive_lock_md(tmp_path: Path):
    """LOCK.md files live at core/strategies/_archive/<family>/LOCK.md.
    The old glob strategies/*/LOCK.md matched nothing and A5 never scanned them.
    """
    archive_lock = (
        tmp_path / "core" / "strategies" / "_archive" / "guardian" / "LOCK.md"
    )
    archive_lock.parent.mkdir(parents=True)
    archive_lock.write_text("# lock\n", encoding="utf-8")
    stale_flat = tmp_path / "core" / "strategies" / "guardian" / "LOCK.md"
    stale_flat.parent.mkdir(parents=True)
    stale_flat.write_text("# not a live lock path\n", encoding="utf-8")
    surfaces = list(cag.iter_a5_surfaces(tmp_path))
    assert archive_lock in surfaces
    assert stale_flat not in surfaces


def test_age_months_boundary():
    d = date(2026, 1, 15)
    assert not cag.is_older_than_months(d, date(2026, 7, 14), cag.AGE_MONTHS)
    assert cag.is_older_than_months(d, date(2026, 7, 15), cag.AGE_MONTHS)
    assert cag.is_older_than_months(d, date(2026, 10, 1), cag.AGE_MONTHS)


def test_a7_fires_on_uncited_supersede(tmp_path: Path):
    """Synthetic regression for the real 2026-07-25 incident: a forward-board
    bullet cites an ADR that was later partially superseded, and never updated
    to name the superseding ADR. Clean fixture (unlike the live corpus, which
    has 3 topically-unrelated false positives alongside this true one) so the
    check's correctness doesn't depend on STATE.md's prose staying stable.
    """
    _write_adr(tmp_path, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    _write_adr(tmp_path, "2026-02-01-new.md", """# new
**Status:** `Accepted`
**Decision date:** 2026-02-01
**Supersedes:** `2026-01-01-old.md` in part - clause X only
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    # reciprocal edge, exactly as A2 requires
    _write_adr(tmp_path, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-02-01-new.md` - clause X only
**Retain-until:** none

## body
""")
    headers = cag.load_adr_headers(tmp_path)
    state = """## Scheduled forward triggers

- **Stale obligation, never updated.** Owned by
  [`docs/adr/2026-01-01-old.md`](docs/adr/2026-01-01-old.md).
"""
    findings = cag.check_a7(headers, state, "STATE.md")
    assert len(findings) == 1
    assert findings[0].code == "A7"
    assert "2026-01-01-old.md" in findings[0].message
    assert "2026-02-01-new.md" in findings[0].message


def test_a7_silent_when_bullet_names_superseding_adr(tmp_path: Path):
    """Same graph as above, but the bullet already cites the superseding ADR
    -- the fix this check exists to require, and the state a bullet reaches
    after being correctly updated."""
    _write_adr(tmp_path, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-02-01-new.md` - clause X only
**Retain-until:** none

## body
""")
    _write_adr(tmp_path, "2026-02-01-new.md", """# new
**Status:** `Accepted`
**Decision date:** 2026-02-01
**Supersedes:** `2026-01-01-old.md` in part - clause X only
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    headers = cag.load_adr_headers(tmp_path)
    state = """## Scheduled forward triggers

- **Correctly updated obligation.** Owned by
  [`docs/adr/2026-01-01-old.md`](docs/adr/2026-01-01-old.md) — clause X status
  now owned by [`docs/adr/2026-02-01-new.md`](docs/adr/2026-02-01-new.md).
"""
    assert cag.check_a7(headers, state, "STATE.md") == []


def test_a7_ignores_bullets_outside_forward_triggers_section(tmp_path: Path):
    """A pointer-log bullet citing the same superseded ADR must NOT fire --
    A7 is scoped to the forward-trigger board only."""
    _write_adr(tmp_path, "2026-01-01-old.md", """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-02-01-new.md` - clause X only
**Retain-until:** none

## body
""")
    _write_adr(tmp_path, "2026-02-01-new.md", """# new
**Status:** `Accepted`
**Decision date:** 2026-02-01
**Supersedes:** `2026-01-01-old.md` in part - clause X only
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## body
""")
    headers = cag.load_adr_headers(tmp_path)
    state = """## Executed operator decisions — pointer log

- **Old event, no forward relevance.** See
  [`docs/adr/2026-01-01-old.md`](docs/adr/2026-01-01-old.md).
"""
    assert cag.check_a7(headers, state, "STATE.md") == []


A8_HEADER = """# t
**Status:** `Accepted`
**Decision date:** 2026-08-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

---

"""

A8_AUTHORITATIVE = (
    "**(a) Authoritative surface.** The running-count line in this addendum "
    "is canonical. `STATE.md` is a mirror only.\n"
)


def test_a8_table_n_mismatch_one_yes_vs_two(tmp_path: Path):
    """Canonical 2/3 with only one yes-row is a HARD finding."""
    _write_adr(tmp_path, "2026-08-01-count.md", A8_HEADER + A8_AUTHORITATIVE + """
**Running consecutive pre-G0 kill count (canonical):** 2 / 3

| # | Construct | Date | Increments? |
|---|---|---|---|
| 1 | ALPHA | 2026-08-15 | yes — executed pre-G0 screen |
""")
    findings = cag.check_a8(tmp_path)
    assert len(findings) == 1
    assert findings[0].code == "A8"
    assert findings[0].severity == "HARD"
    assert "2" in findings[0].message and "1" in findings[0].message


def test_a8_table_zero_yes_matches_zero_over_two(tmp_path: Path):
    """Harvest shape: 0 / 2 and zero yes-rows is clean."""
    _write_adr(tmp_path, "2026-08-01-count.md", A8_HEADER + A8_AUTHORITATIVE + """
**Running count (canonical): 0 / 2.** Not fired.

| Construct | Date | Class | Increments? |
|---|---|---|---|
| D5 | 2026-07-16 | Stage-2 cost-law KILL | no — already-closed at this mark |
| P1-CF | 2026-08-17 | Pre-admission | **no — never reached intake-class status** |
""")
    assert cag.check_a8(tmp_path) == []


def test_a8_deep_lane_abandoned_matches_two_citations(tmp_path: Path):
    _write_adr(tmp_path, "2026-08-01-count.md", A8_HEADER + A8_AUTHORITATIVE + """
**Running counts (canonical, this ADR):** campaigns completed **0** · survivors falsified **0 / 2** · campaigns abandoned **2** (consecutive **2 / 2**) · preregs refused **0** · **active campaign: none**. DL-2 — [`docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md`](../briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md). Prior: DL-1 — [`docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md`](../briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md).
""")
    assert cag.check_a8(tmp_path) == []


def test_a8_deep_lane_abandoned_one_vs_two_citations(tmp_path: Path):
    _write_adr(tmp_path, "2026-08-01-count.md", A8_HEADER + A8_AUTHORITATIVE + """
**Running counts (canonical, this ADR):** campaigns completed **0** · survivors falsified **0 / 2** · campaigns abandoned **1** · preregs refused **0**. DL-2 — [`docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md`](../briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md). Prior: DL-1 — [`docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md`](../briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md).
""")
    findings = cag.check_a8(tmp_path)
    assert len(findings) == 1
    assert findings[0].code == "A8"
    assert "1" in findings[0].message and "2" in findings[0].message


def test_a8_mutation_eight_day_lag_two_yes_line_still_one(tmp_path: Path):
    """The 2026-08-15→08-23 defect: table has two yes rows, line still 1/3."""
    _write_adr(tmp_path, "2026-08-01-count.md", A8_HEADER + A8_AUTHORITATIVE + """
**Running consecutive pre-G0 kill count (canonical):** 1 / 3

| # | Construct | Date | Increments? |
|---|---|---|---|
| 1 | MNQ-ANALOGUE-1 | 2026-08-15 | yes — executed pre-G0 information screen |
| 2 | MNQ-SIZEDIV-1 | 2026-08-15 | yes — executed pre-G0 Stage-2 falsifier |
""")
    findings = cag.check_a8(tmp_path)
    assert len(findings) == 1
    assert findings[0].code == "A8"
    assert "1" in findings[0].message and "2" in findings[0].message


def test_a8_is_default_on():
    assert "A8" in cag.DEFAULT_ENABLED_CHECKS
    assert "A8" in cag.VALID_CHECKS


def test_a8_ignores_adr_without_authoritative_surface_sentence(tmp_path: Path):
    """A 0/2 line without the (a) sentence is invisible to A8."""
    _write_adr(tmp_path, "2026-08-01-other.md", A8_HEADER + """
**Running count (canonical): 0 / 2.**

| Construct | Date | Increments? |
|---|---|---|
| X | 2026-08-01 | yes — should not count; no (a) sentence |
""")
    assert cag.check_a8(tmp_path) == []

