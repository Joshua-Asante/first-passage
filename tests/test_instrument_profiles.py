"""Unit tests for scripts/instrument_profiles.py — mechanism x instrument index.

All fixtures are synthetic tmp_path trees; no test reads live ledger content.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_IP_PATH = REPO_ROOT / "scripts" / "instrument_profiles.py"
_spec = importlib.util.spec_from_file_location("instrument_profiles", _IP_PATH)
ip = importlib.util.module_from_spec(_spec)
sys.modules["instrument_profiles"] = ip
_spec.loader.exec_module(ip)


MECHANISMS_MD = """# MECHANISMS

## opening-range-continuation

Entering in the direction of an opening-range break and holding for continuation.

- **Class finding:** Dead on index micros at realized cost. [src](../../docs/x.md)

## opening-range-breakout

Trading the break of a session opening range.

- **Class finding:** Equity-index-specific; sign-reverses on Treasuries. [src](../../docs/y.md)
"""


def test_parse_mechanisms_reads_ids_definitions_and_findings(tmp_path):
    p = tmp_path / "MECHANISMS.md"
    p.write_text(MECHANISMS_MD, encoding="utf-8")

    mechs = ip.parse_mechanisms(p)

    assert set(mechs) == {"opening-range-continuation", "opening-range-breakout"}
    assert "continuation" in mechs["opening-range-continuation"].definition
    assert len(mechs["opening-range-breakout"].findings) == 1
    assert "Treasuries" in mechs["opening-range-breakout"].findings[0]
    assert mechs["opening-range-continuation"].lineno == 3


VALID_LEDGER = """# INSTRUMENT LEDGER — TST

**Symbol:** Test instrument

## PROFILE (machine-readable)

```yaml
symbol: TST
asset_class: equity-index-futures
family: []
venue_tradable: true
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: opening-range-breakout
    verdict: DEAD
    date: 2026-07-20
    source: "../../docs/x.md"
```

## STANDING WARNINGS
"""


def _write_ledger(tmp_path, name, body):
    d = tmp_path / "instruments"
    d.mkdir(exist_ok=True)
    p = d / name
    p.write_text(body, encoding="utf-8")
    return d


def test_load_profiles_parses_a_valid_block(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", VALID_LEDGER)
    profiles, findings = ip.load_profiles(d)
    assert findings == []
    assert len(profiles) == 1
    assert profiles[0].symbol == "TST"
    assert profiles[0].venue_tradable is True
    assert profiles[0].cells[0].mechanism == "opening-range-breakout"
    assert profiles[0].cells[0].verdict == "DEAD"


def test_load_profiles_skips_directory_readme(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", VALID_LEDGER)
    (d / "README.md").write_text("# hops only\n", encoding="utf-8")
    profiles, findings = ip.load_profiles(d)
    assert findings == []
    assert [p.symbol for p in profiles] == ["TST"]


def test_p1_flags_unknown_verdict(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", VALID_LEDGER.replace("DEAD", "MOSTLY-DEAD"))
    _, findings = ip.load_profiles(d)
    assert any(f.code == "P1" and "MOSTLY-DEAD" in f.message for f in findings)


TWO_CELL_LEDGER = """# INSTRUMENT LEDGER — TST

**Symbol:** Test instrument

## PROFILE (machine-readable)

```yaml
symbol: TST
asset_class: equity-index-futures
family: []
venue_tradable: true
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: opening-range-breakout
    verdict: DEAD
    date: 2026-07-20
    source: "../../docs/x.md"
  - mechanism: opening-range-continuation
    verdict: MOSTLY-DEAD
    date: 2026-07-20
    source: "../../docs/y.md"
```

## STANDING WARNINGS
"""


def test_p1_unknown_verdict_drops_only_that_cell(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", TWO_CELL_LEDGER)
    profiles, findings = ip.load_profiles(d)

    assert len(profiles) == 1
    cells = profiles[0].cells
    assert len(cells) == 1
    assert cells[0].mechanism == "opening-range-breakout"
    assert cells[0].verdict == "DEAD"
    assert not any(c.mechanism == "opening-range-continuation" for c in cells)

    p1_findings = [f for f in findings if f.code == "P1" and "MOSTLY-DEAD" in f.message]
    assert len(p1_findings) == 1


def test_p1_flags_malformed_yaml(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", VALID_LEDGER.replace("symbol: TST", "symbol: [unclosed"))
    _, findings = ip.load_profiles(d)
    assert any(f.code == "P1" for f in findings)


def test_p1_flags_ledger_with_neither_block_nor_marker(tmp_path):
    d = _write_ledger(tmp_path, "BARE.md", "# INSTRUMENT LEDGER — BARE\n\nNo block here.\n")
    _, findings = ip.load_profiles(d)
    assert any(f.code == "P1" and "no PROFILE block" in f.message for f in findings)


def test_no_profile_marker_is_skipped_without_finding(tmp_path):
    body = "# REDIRECT STUB\n\n<!-- no-profile: redirect stub -->\n"
    d = _write_ledger(tmp_path, "OLD.md", body)
    profiles, findings = ip.load_profiles(d)
    assert profiles == [] and findings == []


def test_p1_flags_missing_required_field(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", VALID_LEDGER.replace("asset_class: equity-index-futures\n", ""))
    _, findings = ip.load_profiles(d)
    assert any(f.code == "P1" and "asset_class" in f.message for f in findings)


def test_p1_flags_quoted_string_venue_tradable(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", VALID_LEDGER.replace('venue_tradable: true', 'venue_tradable: "false"'))
    profiles, findings = ip.load_profiles(d)
    assert profiles == []
    assert any(f.code == "P1" and "venue_tradable" in f.message for f in findings)


def _mechs(tmp_path):
    p = tmp_path / "MECHANISMS.md"
    p.write_text(MECHANISMS_MD, encoding="utf-8")
    return ip.parse_mechanisms(p)


def test_p2_flags_unknown_mechanism_with_nearest_match(tmp_path):
    d = _write_ledger(
        tmp_path, "TST.md", VALID_LEDGER.replace("opening-range-breakout", "opening-range-brekout")
    )
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "docs" / "x.md").write_text("**Closed:** 2026-07-20\n\nx\n", encoding="utf-8")
    profiles, _ = ip.load_profiles(d)
    findings = ip.validate(profiles, _mechs(tmp_path), tmp_path)
    p2 = [f for f in findings if f.code == "P2"]
    assert len(p2) == 1
    assert "opening-range-breakout" in p2[0].message  # nearest-match suggestion


def test_p2_accepts_a_known_mechanism(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", VALID_LEDGER)
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "docs" / "x.md").write_text("**Closed:** 2026-07-20\n\nx\n", encoding="utf-8")
    profiles, _ = ip.load_profiles(d)
    assert [f for f in ip.validate(profiles, _mechs(tmp_path), tmp_path) if f.code == "P2"] == []


def test_p1_flags_dangling_source_link(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", VALID_LEDGER)  # ../../docs/x.md never created
    profiles, _ = ip.load_profiles(d)
    findings = ip.validate(profiles, _mechs(tmp_path), tmp_path)
    assert any(f.code == "P1" and "does not resolve" in f.message for f in findings)


def test_p1_waives_public_seed_excluded_source(tmp_path):
    """docs/ltm/** (and notes/superpowers) were curated out of the public seed."""
    body = VALID_LEDGER.replace(
        '"../../docs/x.md"',
        '"../../docs/ltm/briefs/foo.md"',
    )
    d = _write_ledger(tmp_path, "TST.md", body)
    profiles, _ = ip.load_profiles(d)
    findings = ip.validate(profiles, _mechs(tmp_path), tmp_path)
    assert [f for f in findings if "does not resolve" in f.message] == []


def test_anchor_only_source_is_not_treated_as_a_path(tmp_path):
    d = _write_ledger(tmp_path, "TST.md", VALID_LEDGER.replace('"../../docs/x.md"', '"#M6"'))
    profiles, _ = ip.load_profiles(d)
    findings = ip.validate(profiles, _mechs(tmp_path), tmp_path)
    assert [f for f in findings if "does not resolve" in f.message] == []


# NOTE: the brief's version of this test built the fixture via VALID_LEDGER.replace(),
# keyed on a `source: "#B1"` string that does not occur in this file's VALID_LEDGER
# (whose single cell uses `source: "../../docs/x.md"`). Per the brief's own fallback
# instruction ("if the exact string ... differs, build the fixture by writing the
# two-cell YAML directly"), this is written directly instead of by string surgery.
DUPLICATE_CELL_LEDGER = """# INSTRUMENT LEDGER — TST

**Symbol:** Test instrument

## PROFILE (machine-readable)

```yaml
symbol: TST
asset_class: equity-index-futures
family: []
venue_tradable: true
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: opening-range-breakout
    verdict: DEAD
    date: 2026-07-20
    source: "#B1"
  - mechanism: opening-range-breakout
    verdict: LIVE
    date: 2026-07-21
    source: "#B2"
```

## STANDING WARNINGS
"""


def test_p1_flags_duplicate_mechanism_on_one_instrument(tmp_path):
    """One verdict per (instrument, mechanism). Two rows would silently
    overwrite in the generated index — reject instead of losing one."""
    d = _write_ledger(tmp_path, "TST.md", DUPLICATE_CELL_LEDGER)
    profiles, _ = ip.load_profiles(d)
    findings = ip.validate(profiles, _mechs(tmp_path), tmp_path)
    assert any(f.code == "P1" and "duplicate" in f.message.lower() for f in findings)


def _count_live_pipes(text: str) -> int:
    """Count '|' characters that act as live table-column delimiters under
    CommonMark backslash-escape pairing semantics.

    Backslash-escapes pair left-to-right, so a '|' is only escaped (inert)
    when it is preceded by an ODD number of consecutive backslashes; an
    EVEN run (0, 2, 4, ...) leaves it live. A single-character lookbehind
    like ``(?<!\\\\)\\|`` gets this wrong for runs of 2+ backslashes (it
    treats any backslash immediately before '|' as escaping it, so
    ``\\|`` — an escaped backslash followed by a *live* pipe — is
    miscounted as escaped). This walks the full backslash run before each
    pipe and checks its parity instead of looking at only one character.
    """
    count = 0
    for m in re.finditer(r"(\\*)\|", text):
        if len(m.group(1)) % 2 == 0:
            count += 1
    return count


def _profile(symbol, cells, family=(), bars=()):
    return ip.Profile(
        symbol=symbol, asset_class="equity-index-futures", family=list(family),
        venue_tradable=True, venue_note=None, k_bank_source=None, cost_hurdle=None,
        cells=[ip.Cell(*c) for c in cells], bars=list(bars), structure=[],
        path=Path(f"ops/instruments/{symbol}.md"), lineno=5,
    )


def test_build_view_is_deterministic(tmp_path):
    mechs = _mechs(tmp_path)
    profs = [
        _profile("BBB", [("opening-range-breakout", "DEAD", "2026-07-20", "#B1")]),
        _profile("AAA", [("opening-range-breakout", "LIVE", "2026-07-21", "#A1")]),
    ]
    md1, js1 = ip.build_view(profs, mechs)
    md2, js2 = ip.build_view(list(reversed(profs)), mechs)
    assert md1 == md2 and js1 == js2
    assert md1.endswith("\n") and js1.endswith("\n")
    assert "GENERATED" in md1


def test_build_view_json_indexes_cells_by_symbol_and_mechanism(tmp_path):
    profs = [_profile("AAA", [("opening-range-breakout", "DEAD", "2026-07-20", "#A1")])]
    _, js = ip.build_view(profs, _mechs(tmp_path))
    data = json.loads(js)
    assert data["cells"]["AAA"]["opening-range-breakout"]["verdict"] == "DEAD"


def test_build_view_ledger_field_is_repo_relative_for_in_repo_path(tmp_path):
    """Regression: build_view() used to emit the `ledger` JSON field via
    `p.path.as_posix()` -- an ABSOLUTE path, baking in the operator's home
    directory and this worktree's name. That breaks the byte-comparison
    staleness gate on any other clone, worktree, or CI runner. Fixed to route
    through `_rel()` like every other path-derived field.

    A tmp_path-only fixture cannot catch this: `_rel` legitimately falls back
    to an absolute path for anything outside REPO_ROOT (which tmp_path always
    is), so the regression and the fix would produce the identical string
    there. Exercise the actual in-repo branch by pointing `path` at a
    location under the real REPO_ROOT -- no file needs to exist there,
    `_rel` only does a path computation, never a filesystem check.
    """
    mechs = _mechs(tmp_path)
    in_repo_path = ip.REPO_ROOT / "ops" / "instruments" / "ZZZFAKE.md"
    prof = ip.Profile(
        symbol="ZZZFAKE", asset_class="equity-index-futures", family=[],
        venue_tradable=True, venue_note=None, k_bank_source=None, cost_hurdle=None,
        cells=[], bars=[], structure=[],
        path=in_repo_path, lineno=5,
    )
    _, js = ip.build_view([prof], mechs)
    data = json.loads(js)
    ledger = data["instruments"]["ZZZFAKE"]["ledger"]

    assert ledger == "ops/instruments/ZZZFAKE.md"
    assert not re.match(r"^[A-Za-z]:", ledger)  # no absolute drive-letter path
    assert not ledger.startswith("/")  # no absolute posix path either


def test_inherited_bars_surface_parent_bars_on_the_child(tmp_path):
    parent = _profile("YMX", [], bars=[{"id": "bar-1", "source": "#Y1"}])
    child = _profile("MYMX", [], family=["YMX"])
    by_symbol = {p.symbol: p for p in (parent, child)}
    assert [b["id"] for b in ip.inherited_bars(child, by_symbol)] == ["bar-1"]
    assert ip.inherited_bars(parent, by_symbol) == []


def test_unrecognized_mechanism_cell_appears_in_markdown_and_json_agree(tmp_path):
    """validate() raises a P2 for a cell whose mechanism isn't in MECHANISMS.md,
    but build_view has no guard of its own — an unregistered cell must not be
    silently dropped from the markdown while still showing up in the JSON."""
    mechs = _mechs(tmp_path)
    profs = [
        _profile("AAA", [("opening-range-breakout", "DEAD", "2026-07-20", "#A1")]),
        _profile("BBB", [("some-unregistered-mech", "LIVE", "2026-07-21", "#B1")]),
    ]
    md, js = ip.build_view(profs, mechs)
    data = json.loads(js)

    # Still present in the JSON twin (unchanged behavior).
    assert data["cells"]["BBB"]["some-unregistered-mech"]["verdict"] == "LIVE"

    # Now also surfaced in the markdown, instead of silently vanishing.
    assert "## Unrecognized mechanisms" in md
    section = md.split("## Unrecognized mechanisms", 1)[1]
    assert "BBB" in section
    assert "some-unregistered-mech" in section
    assert "LIVE" in section
    # And it must NOT appear in the registered per-mechanism sections.
    assert "## some-unregistered-mech" not in md


def test_no_unrecognized_section_when_all_mechanisms_registered(tmp_path):
    mechs = _mechs(tmp_path)
    profs = [_profile("AAA", [("opening-range-breakout", "DEAD", "2026-07-20", "#A1")])]
    md, _ = ip.build_view(profs, mechs)
    assert "Unrecognized mechanisms" not in md


def test_pipe_in_source_does_not_add_a_table_column(tmp_path):
    mechs = _mechs(tmp_path)
    profs = [
        _profile("AAA", [("opening-range-breakout", "DEAD", "2026-07-20", "weird|source.md")]),
    ]
    md, _ = ip.build_view(profs, mechs)
    row = next(line for line in md.splitlines() if line.startswith("| AAA |"))
    # The pipe is escaped (preceded by a single, i.e. odd, backslash run)
    # so it renders as literal cell content, not a column delimiter —
    # exactly 5 *live* pipes (4 columns), counted under CommonMark
    # left-to-right backslash-pairing semantics, not a naive
    # single-character lookbehind (which mis-scores runs of 2+
    # backslashes — see _count_live_pipes docstring).
    assert _count_live_pipes(row) == 5
    assert "\\|" in row


def test_preexisting_single_backslash_before_pipe_stays_escaped(tmp_path):
    """Reviewer-verified regression case: a source value that already
    contains one backslash immediately before a pipe (e.g. an anchor
    fragment like 'notes.md#sec\\|injected') must not defeat the escape.

    Before the fix, `_md_cell` replaced '|' -> '\\|' without first
    escaping the pre-existing backslash, so the one original backslash
    plus the newly-inserted one formed an EVEN (2) backslash run before
    the pipe — which CommonMark pairs off as an escaped backslash,
    leaving the pipe itself live and adding a spurious column.
    """
    mechs = _mechs(tmp_path)
    source = "notes.md#sec\\|injected"  # one literal backslash, then a pipe
    profs = [_profile("AAA", [("opening-range-breakout", "DEAD", "2026-07-20", source)])]
    md, _ = ip.build_view(profs, mechs)
    row = next(line for line in md.splitlines() if line.startswith("| AAA |"))

    # 5 structural delimiters + 1 embedded pipe = 6 raw '|' characters.
    assert row.count("|") == 6
    # Only the 5 structural delimiters are live; the embedded one is
    # escaped by an odd (3) backslash run: original 1 -> doubled to 2,
    # plus the 1 inserted to escape the pipe itself.
    assert _count_live_pipes(row) == 5
    assert ("\\" * 3 + "|") in row


def test_preexisting_double_backslash_before_pipe_stays_escaped(tmp_path):
    """Source already has TWO backslashes then a pipe (\\\\|) — an even
    run, i.e. already a "properly escaped backslash" followed by a live
    pipe in the *source* value. The emitted cell must still fully escape
    that pipe (2n+1 backslashes before it is always odd for any n)."""
    mechs = _mechs(tmp_path)
    source = "path\\\\|tail"  # two literal backslashes, then a pipe
    profs = [_profile("AAA", [("opening-range-breakout", "DEAD", "2026-07-20", source)])]
    md, _ = ip.build_view(profs, mechs)
    row = next(line for line in md.splitlines() if line.startswith("| AAA |"))

    assert row.count("|") == 6
    assert _count_live_pipes(row) == 5
    assert ("\\" * 5 + "|") in row


def test_preexisting_triple_backslash_before_pipe_stays_escaped(tmp_path):
    """Source has THREE backslashes then a pipe — an odd run (already
    "escaped" in the source's own terms), but the emitted cell must
    re-derive its own correct escaping from scratch, not assume the
    source's parity carries through unchanged."""
    mechs = _mechs(tmp_path)
    source = "path\\\\\\|tail"  # three literal backslashes, then a pipe
    profs = [_profile("AAA", [("opening-range-breakout", "DEAD", "2026-07-20", source)])]
    md, _ = ip.build_view(profs, mechs)
    row = next(line for line in md.splitlines() if line.startswith("| AAA |"))

    assert row.count("|") == 6
    assert _count_live_pipes(row) == 5
    assert ("\\" * 7 + "|") in row


def test_pipe_and_newline_in_source_both_neutralized(tmp_path):
    """A value carrying both hazards at once: a live pipe plus an
    embedded newline. The newline must collapse to a space (no injected
    markdown line) AND the pipe must stay escaped (no extra column) in
    the same emitted cell."""
    mechs = _mechs(tmp_path)
    source = "a|b\nc"
    profs = [_profile("AAA", [("opening-range-breakout", "DEAD", "2026-07-20", source)])]
    md, _ = ip.build_view(profs, mechs)
    row = next(line for line in md.splitlines() if line.startswith("| AAA |"))

    assert _count_live_pipes(row) == 5
    assert "\\|" in row
    assert "a\\|b c" in row
    # No stray raw newline reached the emitted row / file.
    assert "\n" not in row


def test_newline_in_source_does_not_inject_a_markdown_line(tmp_path):
    mechs = _mechs(tmp_path)
    profs = [
        _profile(
            "AAA",
            [("opening-range-breakout", "DEAD", "2026-07-20", "x.md\n## Injected Header\n")],
        ),
    ]
    md, _ = ip.build_view(profs, mechs)
    # The newline is collapsed to a space, so "## Injected Header" may still
    # appear as inert text inside a table cell — what must NOT happen is it
    # landing at the start of its own line, where markdown would render it
    # as a real heading.
    assert not any(line.strip() == "## Injected Header" for line in md.splitlines())
    assert "\n## Injected Header" not in md


def test_build_view_deterministic_with_unrecognized_mechanism_present(tmp_path):
    mechs = _mechs(tmp_path)
    profs = [
        _profile("BBB", [("some-unregistered-mech", "LIVE", "2026-07-21", "#B1")]),
        _profile("AAA", [("opening-range-breakout", "DEAD", "2026-07-20", "#A1")]),
    ]
    md1, js1 = ip.build_view(profs, mechs)
    md2, js2 = ip.build_view(list(reversed(profs)), mechs)
    assert md1 == md2
    assert js1 == js2
    assert md1.endswith("\n") and not md1.endswith("\n\n")


# --- Task 5: P3 staleness check + build/check CLI -------------------------
#
# NOTE on _fixture_repo: the brief's version places the resolvable-source
# fixture file at tmp_path/"ops"/"docs"/"x.md". VALID_LEDGER's cell source
# is "../../docs/x.md", resolved relative to the ledger's own directory
# (ops/instruments/TST.md -> parent ops/instruments). Two ".." from
# ops/instruments lands at tmp_path itself (not tmp_path/"ops"), then
# descends into docs/x.md -- i.e. the file must live at tmp_path/"docs"/"x.md"
# to actually resolve (verified with os.path.normpath). This mirrors the
# real repo layout: docs/ is root-resident (REPO_MAP), not nested under
# ops/. Placing it under tmp_path/"ops"/"docs" would make _resolve() fail
# with a P1 "does not resolve" finding, which (with the required cmd_build
# deviation calling validate()) would make `build` abort with returncode 1
# instead of 0 -- breaking test_build_then_check_is_clean. Fixed here to
# match actual path-resolution semantics.


def _fixture_repo(tmp_path, ledger_body=VALID_LEDGER):
    inst = tmp_path / "ops" / "instruments"
    inst.mkdir(parents=True)
    (inst / "MECHANISMS.md").write_text(MECHANISMS_MD, encoding="utf-8")
    (inst / "TST.md").write_text(ledger_body, encoding="utf-8")
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    (docs / "x.md").write_text("**Closed:** 2026-07-20\n\nx\n", encoding="utf-8")
    return tmp_path


def _run(repo_root, *args):
    return subprocess.run(
        [sys.executable, str(_IP_PATH), *args, "--repo-root", str(repo_root)],
        capture_output=True, text=True,
    )


def test_normalize_makes_crlf_and_lf_compare_equal():
    assert ip.normalize("a\r\nb\r\n") == ip.normalize("a\nb\n")


def test_build_then_check_is_clean(tmp_path):
    repo = _fixture_repo(tmp_path)
    assert _run(repo, "build").returncode == 0
    result = _run(repo, "check")
    assert result.returncode == 0, result.stdout + result.stderr


def test_p3_fires_when_a_verdict_changes_without_regenerate(tmp_path):
    repo = _fixture_repo(tmp_path)
    _run(repo, "build")
    ledger = repo / "ops" / "instruments" / "TST.md"
    ledger.write_text(ledger.read_text(encoding="utf-8").replace("DEAD", "LIVE"), encoding="utf-8")
    result = _run(repo, "check")
    assert result.returncode == 1
    assert "P3" in result.stdout


def test_check_fails_on_unknown_mechanism_via_cli(tmp_path):
    repo = _fixture_repo(tmp_path, VALID_LEDGER.replace("opening-range-breakout", "nonsense-class"))
    _run(repo, "build")
    result = _run(repo, "check")
    assert result.returncode == 1 and "P2" in result.stdout


def test_build_aborts_on_p2_and_writes_no_files(tmp_path):
    """The required deviation from the brief: cmd_build must also run
    validate() (P2 unknown-mechanism / P1 dangling-source checks), not just
    load_profiles' P1 block-schema checks. Otherwise `build` would happily
    generate a view from a ledger referencing an unregistered mechanism, and
    a subsequent `check` run would immediately flag the freshly-built view
    as having a P2 finding -- a build that "succeeds" but can never pass
    check. Assert directly on the CLI's own postcondition: no PROFILES.md /
    profiles.json land on disk when build aborts."""
    repo = _fixture_repo(tmp_path, VALID_LEDGER.replace("opening-range-breakout", "nonsense-class"))
    result = _run(repo, "build")
    assert result.returncode == 1
    assert "P2" in result.stdout
    assert not (repo / "ops" / "instruments" / "PROFILES.md").exists()
    assert not (repo / "ops" / "instruments" / "profiles.json").exists()


def test_check_is_clean_when_committed_view_has_crlf_line_endings(tmp_path):
    """Load-bearing CRLF check, exercised end-to-end through the CLI (not
    just the normalize() unit): this repo checks out CRLF on Windows, so the
    committed PROFILES.md/profiles.json bytes `check` reads back may carry
    \\r\\n even though `build` always writes \\n (newline="\\n"). Simulate a
    CRLF checkout by rewriting the just-built files with \\r\\n line endings
    and confirm `check` still reports clean (no spurious P3)."""
    repo = _fixture_repo(tmp_path)
    assert _run(repo, "build").returncode == 0
    md_path = repo / "ops" / "instruments" / "PROFILES.md"
    json_path = repo / "ops" / "instruments" / "profiles.json"
    for path in (md_path, json_path):
        text = path.read_text(encoding="utf-8")
        assert "\r\n" not in text  # build wrote LF-only, as required
        path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
    result = _run(repo, "check")
    assert result.returncode == 0, result.stdout + result.stderr


# --- Task 5 fix: missing MECHANISMS.md must fail clean, not crash ---------
#
# Reviewer-reproduced defect: parse_mechanisms() does path.read_text()
# unconditionally, and both cmd_build and cmd_check called it with no
# existence guard. With ledgers present but MECHANISMS.md absent (deleted
# or renamed), both commands dumped an uncaught FileNotFoundError traceback
# to stderr instead of reporting through the normal Finding path. The
# exit code happened to be 1 only as Python's default for an uncaught
# exception -- the CLI's own finding-reporting path never ran.


def test_check_reports_clean_p1_when_mechanisms_file_missing(tmp_path):
    repo = _fixture_repo(tmp_path)
    (repo / "ops" / "instruments" / "MECHANISMS.md").unlink()

    result = _run(repo, "check")

    assert result.returncode != 0
    assert "P1" in result.stdout
    assert "MECHANISMS.md" in result.stdout
    # This is the actual regression: assert on absence of a traceback, not
    # just the exit code -- a test that only checked returncode would pass
    # against the buggy (crashing) version too, since an uncaught exception
    # also exits 1.
    assert "Traceback" not in result.stderr
    assert result.stderr == ""


def test_build_reports_clean_p1_when_mechanisms_file_missing_and_writes_nothing(tmp_path):
    repo = _fixture_repo(tmp_path)
    (repo / "ops" / "instruments" / "MECHANISMS.md").unlink()

    result = _run(repo, "build")

    assert result.returncode != 0
    assert "P1" in result.stdout
    assert "MECHANISMS.md" in result.stdout
    assert "Traceback" not in result.stderr
    assert result.stderr == ""
    # No fallback to an empty vocabulary, and no partial/generated output.
    assert not (repo / "ops" / "instruments" / "PROFILES.md").exists()
    assert not (repo / "ops" / "instruments" / "profiles.json").exists()


# --- Task 9: `cell` subcommand ---------------------------------------------
#
# NOTE on mechanism choice for the untested case: the brief's version of
# test_cell_untested_exits_zero queries `cell TST intraday-momentum`.
# "intraday-momentum" is a real mechanism id in the live repo's
# ops/instruments/MECHANISMS.md, but it is NOT in this test file's own
# MECHANISMS_MD fixture constant (which registers only
# opening-range-continuation / opening-range-breakout, and is asserted
# exhaustively by test_parse_mechanisms_reads_ids_definitions_and_findings
# above). Querying an unregistered mechanism id is, by design, a USAGE
# error (exit 2 — "Declare it NEW in MECHANISMS.md"), not an untested-cell
# verdict (exit 0) — see cmd_cell. Using it here would make the test assert
# a code path it isn't exercising. Swapped to
# "opening-range-continuation": it IS registered in this fixture's
# MECHANISMS_MD, and TST's VALID_LEDGER carries no cell for it, so it is
# genuinely untested — the intended code path — without touching the
# shared MECHANISMS_MD constant (which would ripple into the exhaustive
# id-set assertion above).


def test_cell_untested_exits_zero(tmp_path):
    repo = _fixture_repo(tmp_path)
    _run(repo, "build")
    result = _run(repo, "cell", "TST", "opening-range-continuation")
    assert result.returncode == 0 and "untested" in result.stdout.lower()


def test_cell_dead_exits_nonzero_and_prints_source(tmp_path):
    repo = _fixture_repo(tmp_path)
    _run(repo, "build")
    result = _run(repo, "cell", "TST", "opening-range-breakout")
    assert result.returncode == 1
    assert "DEAD" in result.stdout and "docs/x.md" in result.stdout


def test_cell_live_exits_zero_with_note(tmp_path):
    repo = _fixture_repo(tmp_path, VALID_LEDGER.replace("verdict: DEAD", "verdict: LIVE"))
    _run(repo, "build")
    result = _run(repo, "cell", "TST", "opening-range-breakout")
    assert result.returncode == 0 and "book-correlation" in result.stdout


def test_cell_unknown_symbol_exits_two(tmp_path):
    repo = _fixture_repo(tmp_path)
    _run(repo, "build")
    assert _run(repo, "cell", "NOSUCH", "opening-range-breakout").returncode == 2


def test_cell_unknown_mechanism_exits_two(tmp_path):
    repo = _fixture_repo(tmp_path)
    _run(repo, "build")
    result = _run(repo, "cell", "TST", "no-such-mechanism")
    assert result.returncode == 2
    assert "FATAL" in result.stdout


def test_cell_missing_json_exits_two_and_names_build(tmp_path):
    """cell reads profiles.json only -- it never re-parses the ledgers. A
    missing profiles.json is a usage error telling the caller to run build,
    not a silent empty/untested result."""
    repo = _fixture_repo(tmp_path)
    result = _run(repo, "cell", "TST", "opening-range-breakout")
    assert result.returncode == 2
    assert "build" in result.stdout.lower()


def test_cell_wrong_arg_count_exits_two(tmp_path):
    repo = _fixture_repo(tmp_path)
    _run(repo, "build")
    result = _run(repo, "cell", "TST")
    assert result.returncode == 2


def test_cell_prints_cost_hurdle_with_source(tmp_path):
    """Standing lesson: never print a bare number without its source."""
    ledger = VALID_LEDGER.replace(
        "venue_tradable: true\n",
        'venue_tradable: true\ncost_hurdle:\n  value: 6.57\n  units: "bp/event"\n'
        '  basis: "4x Tradeify hurdle"\n  source: "#M6"\n',
    )
    repo = _fixture_repo(tmp_path, ledger)
    _run(repo, "build")
    result = _run(repo, "cell", "TST", "opening-range-breakout")
    assert "6.57" in result.stdout
    assert "#M6" in result.stdout


def test_cell_k_bank_prints_as_pointer_not_snapshot(tmp_path):
    repo = _fixture_repo(tmp_path, VALID_LEDGER)
    _run(repo, "build")
    result = _run(repo, "cell", "TST", "opening-range-breakout")
    assert "discovery_manifests/" in result.stdout
    assert "never trust a snapshot" in result.stdout.lower()
    assert "None" not in result.stdout


def test_cell_own_bar_forces_exit_one_even_on_untested_cell(tmp_path):
    """A binding bar on the instrument blocks even when the queried cell
    itself has no prior verdict at all."""
    ledger = VALID_LEDGER.replace(
        "venue_tradable: true\n",
        'venue_tradable: true\nbars:\n  - id: "some-bar"\n    source: "#X1"\n',
    )
    repo = _fixture_repo(tmp_path, ledger)
    _run(repo, "build")
    result = _run(repo, "cell", "TST", "opening-range-continuation")
    assert result.returncode == 1
    assert "BINDING BAR" in result.stdout


def test_cell_inherited_bar_from_family_parent_forces_exit_one(tmp_path):
    """A bar declared on a family parent inherits onto the child and binds
    there too, per profiles.json's separate `bars` / `inherited_bars` keys."""
    parent_ledger = VALID_LEDGER.replace("symbol: TST", "symbol: PAR").replace(
        "venue_tradable: true\n",
        'venue_tradable: true\nbars:\n  - id: "parent-bar"\n    source: "#P1"\n',
    ).replace(
        "cells:\n  - mechanism: opening-range-breakout\n    verdict: DEAD\n"
        "    date: 2026-07-20\n    source: \"../../docs/x.md\"\n",
        "cells: []\n",
    )
    child_ledger = VALID_LEDGER.replace("family: []", "family: [PAR]")
    repo = _fixture_repo(tmp_path, child_ledger)
    (repo / "ops" / "instruments" / "PAR.md").write_text(parent_ledger, encoding="utf-8")
    result = _run(repo, "build")
    assert result.returncode == 0, result.stdout + result.stderr
    result = _run(repo, "cell", "TST", "opening-range-continuation")
    assert result.returncode == 1
    assert "BINDING BAR" in result.stdout
    assert "parent-bar" in result.stdout


def test_cell_bars_entry_blocks_even_with_no_cell_for_the_queried_mechanism(tmp_path):
    """Regression for Task 9 review Finding 1: a real, load-bearing bar was
    missing from a ledger's `bars` list even though the ledger's own prose
    described it, so `cell` printed 'untested ... exit 0' (clear to
    proceed) on an instrument a prior bar actually binds. The CODE path for
    `bars` already exits 1 on an untested cell (see
    test_cell_own_bar_forces_exit_one_even_on_untested_cell) -- the gap was
    that a prose-only bar with no corresponding `bars:` YAML entry is
    invisible to the tool by construction. This models the actual fix
    shape: the SAME bar `id`/`source` declared independently on two
    SIBLING instruments (no `family` relationship -- the brief is explicit
    that `family` drives a different, parent/child inheritance mechanism
    and must not be used to model a same-complex bar). Both siblings must
    independently exit 1 on a mechanism neither has ever recorded a cell
    for, and the bar must come from each instrument's own `bars` list, not
    `inherited_bars`."""
    inst = tmp_path / "ops" / "instruments"
    inst.mkdir(parents=True)
    (inst / "MECHANISMS.md").write_text(MECHANISMS_MD, encoding="utf-8")
    sibling_a = VALID_LEDGER.replace("symbol: TST", "symbol: SIBA").replace(
        "venue_tradable: true\n",
        'venue_tradable: true\nbars:\n  - id: shared-complex-bar\n    source: "SIBB.md#X1"\n',
    )
    sibling_b = VALID_LEDGER.replace("symbol: TST", "symbol: SIBB").replace(
        "venue_tradable: true\n",
        'venue_tradable: true\nbars:\n  - id: shared-complex-bar\n    source: "SIBB.md#X1"\n',
    )
    (inst / "SIBA.md").write_text(sibling_a, encoding="utf-8")
    (inst / "SIBB.md").write_text(sibling_b, encoding="utf-8")
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    (docs / "x.md").write_text("**Closed:** 2026-07-20\n\nx\n", encoding="utf-8")

    assert _run(tmp_path, "build").returncode == 0

    for symbol in ("SIBA", "SIBB"):
        # opening-range-continuation: neither sibling has ever recorded a
        # cell for it -- exactly the "silently passed" gap.
        result = _run(tmp_path, "cell", symbol, "opening-range-continuation")
        assert result.returncode == 1, result.stdout + result.stderr
        assert "verdict: untested" in result.stdout
        assert "BINDING BAR: shared-complex-bar" in result.stdout

    data = json.loads((inst / "profiles.json").read_text(encoding="utf-8"))
    assert data["instruments"]["SIBA"]["family"] == []
    assert data["instruments"]["SIBB"]["family"] == []
    assert [b["id"] for b in data["instruments"]["SIBA"]["bars"]] == ["shared-complex-bar"]
    assert data["instruments"]["SIBA"]["inherited_bars"] == []


def test_cell_venue_not_tradable_line_printed(tmp_path):
    ledger = VALID_LEDGER.replace("venue_tradable: true", 'venue_tradable: false\nvenue_note: "no go"')
    repo = _fixture_repo(tmp_path, ledger)
    _run(repo, "build")
    result = _run(repo, "cell", "TST", "opening-range-breakout")
    assert "NOT TRADABLE" in result.stdout
    assert "no go" in result.stdout


def test_cell_class_finding_and_structure_prior_both_surfaced(tmp_path):
    ledger = VALID_LEDGER.replace(
        "venue_tradable: true\n",
        'venue_tradable: true\nstructure:\n  - claim: "TST fades its range"\n    source: "#S1"\n',
    )
    repo = _fixture_repo(tmp_path, ledger)
    _run(repo, "build")
    result = _run(repo, "cell", "TST", "opening-range-breakout")
    assert "class finding (mechanism-wide, not specific to TST):" in result.stdout
    assert "Treasuries" in result.stdout  # opening-range-breakout's class finding
    assert "TST fades its range" in result.stdout


def test_cell_class_finding_label_names_the_queried_symbol(tmp_path):
    """Regression for Task 9 review Finding 2: `class finding:` on its own
    reads as if the finding described the queried instrument. The label
    must scope it explicitly to the mechanism class and echo back the
    queried SYMBOL, so a skim can't misattribute a class-wide finding
    (which may have been measured on a completely different instrument)
    to the one just queried."""
    inst = tmp_path / "ops" / "instruments"
    inst.mkdir(parents=True)
    (inst / "MECHANISMS.md").write_text(MECHANISMS_MD, encoding="utf-8")
    (inst / "ZZZ.md").write_text(VALID_LEDGER.replace("symbol: TST", "symbol: ZZZ"), encoding="utf-8")
    (tmp_path / "docs").mkdir(parents=True)
    (tmp_path / "docs" / "x.md").write_text("**Closed:** 2026-07-20\n\nx\n", encoding="utf-8")

    _run(tmp_path, "build")
    result = _run(tmp_path, "cell", "ZZZ", "opening-range-breakout")
    assert result.returncode == 1
    assert "class finding (mechanism-wide, not specific to ZZZ):" in result.stdout
    assert "Treasuries" in result.stdout


def test_cell_is_read_only_does_not_write_any_file(tmp_path):
    repo = _fixture_repo(tmp_path)
    _run(repo, "build")
    before = {
        p: p.read_bytes()
        for p in (repo / "ops" / "instruments").iterdir()
        if p.is_file()
    }
    _run(repo, "cell", "TST", "opening-range-breakout")
    after = {
        p: p.read_bytes()
        for p in (repo / "ops" / "instruments").iterdir()
        if p.is_file()
    }
    assert before == after


def test_p1_flags_bars_entry_missing_source(tmp_path):
    """Empty/missing source on a bars entry must not vacuously resolve."""
    ledger = VALID_LEDGER.replace(
        "venue_tradable: true\n",
        "venue_tradable: true\nbars:\n  - id: \"unsourced-bar\"\n",
    )
    d = _write_ledger(tmp_path, "TST.md", ledger)
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "docs" / "x.md").write_text("**Closed:** 2026-07-20\n\nx\n", encoding="utf-8")
    profiles, _ = ip.load_profiles(d)
    findings = ip.validate(profiles, _mechs(tmp_path), tmp_path)
    assert any(
        f.code == "P1" and "bars" in f.message and "source" in f.message
        for f in findings
    )


def test_p1_flags_missing_k_bank_source(tmp_path):
    """k_bank_source is required so cell never prints a bare None pointer."""
    d = _write_ledger(
        tmp_path,
        "TST.md",
        VALID_LEDGER.replace('k_bank_source: "../../discovery_manifests/"\n', ""),
    )
    _, findings = ip.load_profiles(d)
    assert any(f.code == "P1" and "k_bank_source" in f.message for f in findings)


def test_parse_mechanisms_skips_finding_shaped_line_for_definition(tmp_path):
    """A Class-finding line before prose must not become (or displace) definition;
    finding-only entries leave definition empty so validate can P1 them."""
    finding_first = """# MECHANISMS

## finding-first-mech

- **Class finding:** Authored before the prose on purpose. [src](../../docs/x.md)

The real one-line definition comes after the finding.

## finding-only-mech

- **Class finding:** No prose definition at all. [src](../../docs/y.md)
"""
    p = tmp_path / "MECHANISMS.md"
    p.write_text(finding_first, encoding="utf-8")
    mechs = ip.parse_mechanisms(p)

    assert mechs["finding-first-mech"].definition.startswith("The real one-line")
    assert len(mechs["finding-first-mech"].findings) == 1
    assert "Authored before" in mechs["finding-first-mech"].findings[0]

    assert mechs["finding-only-mech"].definition == ""
    assert len(mechs["finding-only-mech"].findings) == 1

    findings = ip.validate([], mechs, tmp_path)
    assert any(
        f.code == "P1"
        and "finding-only-mech" in f.message
        and "no prose definition" in f.message
        for f in findings
    )
    assert not any("finding-first-mech" in f.message for f in findings)


# ---------------------------------------------------------------------------
# P4 / P5 date provenance (ADR 2026-07-25 execution note 1)
#
# A cell's `date` must be findable in that row's OWN cited source. Five defects
# of this class were caught by human review during the build -- a date taken
# from a tool-deletion event, one from an unrelated venue closure, one whose
# source carried no date at all. These tests pin the mechanical half.
# ---------------------------------------------------------------------------


def _dated_repo(tmp_path, source_body, cell_date, source="../../docs/src.md"):
    """Fixture repo whose single cell cites ../../docs/src.md with `cell_date`."""
    inst = tmp_path / "ops" / "instruments"
    inst.mkdir(parents=True)
    (inst / "MECHANISMS.md").write_text(MECHANISMS_MD, encoding="utf-8")
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    (docs / "src.md").write_text(source_body, encoding="utf-8")
    ledger = f"""# INSTRUMENT LEDGER - TST

## PROFILE (machine-readable)

```yaml
symbol: TST
asset_class: equity-index-futures
family: []
venue_tradable: true
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: opening-range-breakout
    verdict: DEAD
    date: {cell_date}
    source: "{source}"
```

## STANDING WARNINGS
"""
    (inst / "TST.md").write_text(ledger, encoding="utf-8")
    return inst


def _validate(inst, tmp_path):
    profiles, findings = ip.load_profiles(inst)
    assert findings == [], findings
    return ip.validate(profiles, ip.parse_mechanisms(inst / "MECHANISMS.md"), tmp_path)


def test_p4_fires_when_source_declares_a_different_date(tmp_path):
    inst = _dated_repo(tmp_path, "**Closed:** 2026-07-20\nbody\n", "2026-07-21")
    findings = _validate(inst, tmp_path)
    p4 = [f for f in findings if f.code == "P4"]
    assert len(p4) == 1
    # The message must name BOTH values, or it is not actionable.
    assert "2026-07-21" in p4[0].message and "2026-07-20" in p4[0].message


def test_p4_silent_when_source_declares_the_same_date(tmp_path):
    inst = _dated_repo(tmp_path, "**Closed:** 2026-07-21\nbody\n", "2026-07-21")
    assert [f for f in _validate(inst, tmp_path) if f.code == "P4"] == []


def test_p4_matches_colon_inside_the_bold(tmp_path):
    """This repo writes `**Closed:** <date>`; a pattern expecting `**Closed**:`
    matches almost nothing and silently disarms the check."""
    inst = _dated_repo(tmp_path, "**Lock date:** 2026-04-23\n", "2026-07-10")
    assert [f for f in _validate(inst, tmp_path) if f.code == "P4"]


def test_p5_fires_when_date_is_absent_from_an_unlabelled_source(tmp_path):
    inst = _dated_repo(tmp_path, "Numbers only. PF 1.80, n=263.\n", "2026-07-21")
    p5 = [f for f in _validate(inst, tmp_path) if f.code == "P5"]
    assert len(p5) == 1
    assert "2026-07-21" in p5[0].message


def test_p5_silent_when_date_appears_in_an_unlabelled_source(tmp_path):
    inst = _dated_repo(tmp_path, "Run executed 2026-07-21. PF 1.80.\n", "2026-07-21")
    assert [f for f in _validate(inst, tmp_path) if f.code == "P5"] == []


def test_multi_label_registry_never_produces_p4(tmp_path):
    """Picking the right date out of a many-entry registry needs semantics --
    the exact mistake the status-consistency C1 check was dropped for."""
    registry = (
        "### Entry A\n**Closure date:** 2026-07-01\n\n"
        "### Entry B\n**Closure date:** 2026-06-14\n"
    )
    inst = _dated_repo(tmp_path, registry, "2026-07-01")
    findings = _validate(inst, tmp_path)
    assert [f for f in findings if f.code == "P4"] == []
    assert [f for f in findings if f.code == "P5"] == []


def test_anchor_only_source_gets_no_p4_and_no_note(tmp_path):
    """A ledger row is not a decision artifact; the NOTE would be pure noise."""
    inst = _dated_repo(tmp_path, "unused\n", "2026-07-21", source="#B1")
    # The ledger itself must contain the date for P5 to stay silent.
    tst = inst / "TST.md"
    tst.write_text(tst.read_text(encoding="utf-8") + "\n| B1 | closed 2026-07-21 |\n",
                   encoding="utf-8")
    findings = _validate(inst, tmp_path)
    assert [f for f in findings if f.code == "P4"] == []
    assert [f for f in findings if f.severity == "NOTE"] == []


def test_note_fires_on_an_unlabelled_source_but_is_not_hard(tmp_path):
    inst = _dated_repo(tmp_path, "Run executed 2026-07-21. PF 1.80.\n", "2026-07-21")
    notes = [f for f in _validate(inst, tmp_path) if f.severity == "NOTE"]
    assert len(notes) == 1
    assert "self-date" in notes[0].message
    assert str(notes[0]).startswith("NOTE:")


def test_note_alone_does_not_change_the_cli_exit_code(tmp_path):
    """The advisory tier must never block a commit -- a gate that cries wolf
    stops being read."""
    inst = _dated_repo(tmp_path, "Run executed 2026-07-21. PF 1.80.\n", "2026-07-21")
    repo = inst.parent.parent
    assert _run(repo, "build").returncode == 0
    result = _run(repo, "check")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NOTE:" in result.stdout


def test_p4_regression_reproduces_the_real_historical_defect(tmp_path):
    """Backtest: XAUUSD trend-following was dated 2026-07-10 (the CFD venue
    closure) while citing guardian/LOCK.md, whose only labelled date is
    2026-04-23. Human review caught it; this is the mechanical guard."""
    inst = _dated_repo(
        tmp_path,
        "# GUARDIAN LOCK\n\n**Lock date:** 2026-04-23\n\nrisk 0.34%\n",
        "2026-07-10",
    )
    p4 = [f for f in _validate(inst, tmp_path) if f.code == "P4"]
    assert len(p4) == 1
    assert "2026-07-10" in p4[0].message and "2026-04-23" in p4[0].message
