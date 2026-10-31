"""Behavioral contracts for the tracked Markdown link ratchet."""
import importlib.util
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/check_md_anchors.py"


@pytest.fixture
def checker():
    assert SCRIPT.is_file(), "Markdown anchor checker has not been implemented"
    spec = importlib.util.spec_from_file_location("check_md_anchors", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    return tmp_path


def write(repo, name, text):
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    subprocess.run(["git", "add", "--", name], cwd=repo, check=True)
    return path


@pytest.mark.parametrize("heading, fragment", [
    ("# Rule 0 — Audit first", "rule-0--audit-first"),
    ('<a id="Named-ID"></a>', "named-id"),
    ("<a name='Old-Name'></a>", "OLD-NAME"),
    ("# Repeat\n# Repeat\n# Repeat", "repeat-2"),
    ("# Repeat\n# Repeat-1\n# Repeat", "repeat-2"),
    ("# Café!", "CAF%C3%89"),
    ("Title\n====", "title"),
    ("## Edit result_g5 (2026-10-02)", "edit-result_g5-2026-10-02"),
    ("# Use `<name>` and `test_ac_<n>_*`", "use-name-and-test_ac_n_"),
    ("> ## Quoted", "quoted"),
    ("# [`foo`](target.md)", "foo"),
    ("## **Bold** [link](https://example.org) `code` ##", "bold-link-code"),
])
def test_rendered_heading_and_explicit_anchors(checker, repo, heading, fragment):
    write(repo, "target.md", heading + "\r\n")
    write(repo, "source.md", f"[ok](target.md#{fragment})\r\n")
    assert checker.scan(repo) == []


@pytest.mark.parametrize("fence", ["```", "~~~~"])
def test_fenced_headings_and_html_are_not_anchors(checker, repo, fence):
    write(repo, "a.md", f'{fence}\n# Hidden\n<a id="secret">\n{fence}\n'
          "[bad](#hidden) [bad](#secret)\n")
    assert checker.scan(repo) == [
        "a.md:5 -> a.md#hidden [missing-anchor]",
        "a.md:5 -> a.md#secret [missing-anchor]",
    ]


def test_missing_file_anchor_same_file_and_document_resolution(checker, repo):
    write(repo, "target.md", "# Here\n")
    write(repo, "sub/a.md", "# Local\n[ok](#local)\n[bad](#absent)\n"
          "[ok](../target.md#here)\n[bad](../target.md#gone)\n"
          "[bad](lost.md#gone)\n")
    assert checker.scan(repo) == [
        "sub/a.md:3 -> sub/a.md#absent [missing-anchor]",
        "sub/a.md:5 -> target.md#gone [missing-anchor]",
        "sub/a.md:6 -> sub/lost.md#gone [missing-file]",
    ]


def test_inline_links_inside_fences_are_not_links(checker, repo):
    write(repo, "a.md", "```\n[example](missing.md)\n```\n> ~~~\n> [quoted](gone.md)\n> ~~~\n"
          "[real](lost.md)\n")
    assert checker.scan(repo) == ["a.md:7 -> lost.md [missing-file]"]


def test_skips_urls_pinned_paths_outside_and_historical_lines(checker, repo):
    write(repo, "a.md", "[url](HTTPS://example.org/x) [mail](mailto:x@y.org)\n"
          "[blob](blob/abcdef1234/missing.md#x)\n"
          "[tree](../repo/tree/abcdef1234/missing.md)\n"
          "[outside](../missing.md)\n"
          "[history](lost.md) git show old\n"
          "[history](#gone) pre-prune-old\n")
    assert checker.scan(repo) == []


def test_non_markdown_fragments_and_decoded_paths(checker, repo):
    write(repo, "some file.md", "# Yes\n")
    write(repo, "code.py", "pass\n")
    write(repo, "a.md", "[ok](some%20file.md#YES) [ok](code.py#L999)\n")
    assert checker.scan(repo) == []


def test_scan_uses_only_tracked_markdown_including_skills(checker, repo):
    write(repo, ".claude/skills/demo/SKILL.md", "[bad](missing.md)\n")
    (repo / "untracked.md").write_text("[bad](untracked-target.md)", encoding="utf-8")
    assert checker.scan(repo) == [
        ".claude/skills/demo/SKILL.md:1 -> .claude/skills/demo/missing.md [missing-file]",
    ]


@pytest.mark.parametrize("target", [False, True])
def test_legacy_invalid_utf8_warns_without_losing_links(checker, repo, capsys, target):
    path = write(repo, "a.md", "")
    path.write_bytes(b"Legacy \x97 text\n[bad](lost.md)\n")
    expected = ["a.md:2 -> lost.md [missing-file]"]
    if target:
        write(repo, "source.md", "[bad](a.md#absent)\n")
        expected.append("source.md:1 -> a.md#absent [missing-anchor]")
    assert checker.scan(repo) == expected
    assert "a.md: invalid UTF-8" in capsys.readouterr().err


def test_default_reports_sorted_misses_and_fails(checker, repo, capsys):
    write(repo, "z.md", "[bad](z-lost.md)\n")
    write(repo, "a.md", "[bad](a-lost.md)\n")
    assert checker.main([], repo_root=repo) == 1
    assert capsys.readouterr().out.splitlines() == [
        "a.md:1 -> a-lost.md [missing-file]",
        "z.md:1 -> z-lost.md [missing-file]",
    ]


def test_baseline_new_miss_fails_fixed_miss_counted(checker, repo, capsys):
    write(repo, "a.md", "[bad](new.md)\n")
    baseline = repo / "baseline.txt"
    baseline.write_bytes(b"a.md -> old.md [missing-file]\t1\r\n")
    assert checker.main(["--baseline", str(baseline)], repo_root=repo) == 1
    assert capsys.readouterr().out.splitlines() == [
        "a.md -> new.md [missing-file] (current=1, baseline=0)",
        "a.md -> old.md [missing-file] (fixed=1, current=0, baseline=1)",
        "Baseline occurrences now fixed: 1",
    ]
    write(repo, "a.md", "# Fixed\n")
    assert checker.main(["--baseline", str(baseline)], repo_root=repo) == 0
    assert "Baseline occurrences now fixed: 1\n" in capsys.readouterr().out


def test_update_bootstraps_refuses_growth_and_shrinks(checker, repo, capsys):
    write(repo, "a.md", "[bad](old.md)\n")
    baseline = repo / "baseline.txt"
    args = ["--update-baseline", str(baseline)]
    assert checker.main(args, repo_root=repo) == 0
    original = b"a.md -> old.md [missing-file]\t1\n"
    assert baseline.read_bytes() == original
    write(repo, "b.md", "[bad](new.md)\n")
    assert checker.main(args, repo_root=repo) == 2
    assert baseline.read_bytes() == original
    write(repo, "b.md", "# Fixed\n")
    write(repo, "a.md", "# Fixed\n")
    assert checker.main(args, repo_root=repo) == 0
    assert baseline.read_bytes() == b""


def test_line_movement_does_not_grow_baseline(checker, repo, capsys):
    write(repo, "a.md", "[bad](lost.md)\n")
    baseline = repo / "baseline.txt"
    assert checker.main(["--update-baseline", str(baseline)], repo_root=repo) == 0
    write(repo, "a.md", "# Intro\n\n[bad](lost.md)\n")
    assert checker.main(["--baseline", str(baseline)], repo_root=repo) == 0


@pytest.mark.parametrize("separator", ["\n", " "])
def test_duplicate_occurrence_grows_baseline(checker, repo, capsys, separator):
    write(repo, "a.md", "[bad](lost.md)\n")
    baseline = repo / "baseline.txt"
    update = ["--update-baseline", str(baseline)]
    assert checker.main(update, repo_root=repo) == 0
    original = baseline.read_bytes()
    write(repo, "a.md", f"[bad](lost.md){separator}[bad](lost.md)\n")
    assert checker.main(["--baseline", str(baseline)], repo_root=repo) == 1
    assert "current=2, baseline=1" in capsys.readouterr().out
    assert checker.main(update, repo_root=repo) == 2
    assert "current=2, baseline=1" in capsys.readouterr().err
    assert baseline.read_bytes() == original


def test_count_decrease_passes_and_update_lowers_count(checker, repo, capsys):
    write(repo, "a.md", "[bad](lost.md)\n[bad](lost.md)\n")
    baseline = repo / "baseline.txt"
    update = ["--update-baseline", str(baseline)]
    assert checker.main(update, repo_root=repo) == 0
    assert baseline.read_bytes() == b"a.md -> lost.md [missing-file]\t2\n"
    write(repo, "a.md", "[bad](lost.md)\n")
    assert checker.main(["--baseline", str(baseline)], repo_root=repo) == 0
    assert "fixed=1, current=1, baseline=2" in capsys.readouterr().out
    assert checker.main(update, repo_root=repo) == 0
    assert baseline.read_bytes() == b"a.md -> lost.md [missing-file]\t1\n"


def test_claude_repo_root_fallback_is_scoped_and_document_first(checker, repo):
    write(repo, "docs/target.md", "# Root\n")
    write(repo, ".claude/skills/demo/SKILL.md", "[ok](docs/target.md#root)\n")
    assert checker.scan(repo) == []
    write(repo, ".claude/skills/demo/docs/target.md", "# Local\n")
    write(repo, ".claude/skills/demo/SKILL.md", "[ok](docs/target.md#local)\n")
    write(repo, "sub/a.md", "[bad](docs/target.md#root)\n")
    assert checker.scan(repo) == [
        "sub/a.md:1 -> sub/docs/target.md#root [missing-file]",
    ]




@pytest.mark.parametrize("mode", ["", "--baseline", "--update-baseline"])
def test_empty_tracked_set_fails_closed_without_touching_baseline(checker, repo, capsys, mode):
    write(repo, "notes.txt", "[bad](lost.md)\n")
    baseline = repo / "baseline.txt"
    baseline.write_bytes(b"a.md -> lost.md [missing-file]\t1\n")
    args = [mode, str(baseline)] if mode else []
    assert checker.main(args, repo_root=repo) == 2
    assert "no tracked Markdown files" in capsys.readouterr().err
    assert baseline.read_bytes() == b"a.md -> lost.md [missing-file]\t1\n"

# One test per Codex finding on #954; each was a regex misread of CommonMark.

def test_finding_reference_links_resolve_through_definitions(checker, repo):
    write(repo, "target.md", "# Here\n")
    write(repo, "a.md", "[ok][t] [bad][g]\n[lost][L] [ok][t]\n\n[t]: target.md#here\n"
          "[g]: <target.md#gone>\n[l]: lost.md 'title'\n[unused]: absent.md\n"
          "```\n[x][f]\n```\n[f]: fenced.md\n")
    assert checker.scan(repo) == [
        "a.md:1 -> target.md#gone [missing-anchor]",
        "a.md:2 -> lost.md [missing-file]",
    ]


@pytest.mark.parametrize("heading, fragment", [
    ("# Use `<name>` and `test_ac_<n>_*`", "use-name-and-test_ac_n_"),
    ("# `a  b` <span>c</span> &amp; d", "a--b-c--d"),
])
def test_finding_code_span_text_renders_literally_in_slugs(checker, repo, heading, fragment):
    write(repo, "target.md", heading + "\n")
    write(repo, "a.md", f"[ok](target.md#{fragment})\n")
    assert checker.scan(repo) == []


@pytest.mark.parametrize("block", ["```\n{}\n```", "~~~~\n{}\n~~~~", "    {}", "````md\n```\n{}\n```\n````"])
def test_finding_fenced_and_indented_code_hold_no_links_or_headings(checker, repo, block):
    write(repo, "a.md", block.format("[x](missing.md) # Hidden") + "\n\n"
          + block.format("# Hidden") + "\n\n[bad](#hidden)\n")
    assert checker.scan(repo) == ["a.md:" + str(2 * block.count("\n") + 5) + " -> a.md#hidden [missing-anchor]"]


def test_finding_blockquoted_headings_and_links(checker, repo):
    write(repo, "a.md", "> ## Quoted\n>\n> > [ok](#quoted) [bad](lost.md)\n")
    assert checker.scan(repo) == ["a.md:3 -> lost.md [missing-file]"]


@pytest.mark.parametrize("heading, fragment", [
    ("# [`foo`](target.md)", "foo"),
    ("# [label *em*](target.md) and ![alt](target.md) tail", "label-em-and--tail"),
    ("# [ref][r]\n\n[r]: target.md", "ref"),
])
def test_finding_link_labels_render_in_slugs(checker, repo, heading, fragment):
    write(repo, "target.md", heading + "\n")
    write(repo, "a.md", f"[ok](target.md#{fragment})\n")
    assert checker.scan(repo) == []


def test_finding_link_syntax_inside_code_spans_is_not_a_link(checker, repo):
    write(repo, "a.md", "Use `[example](missing.md)` or ``[x](#gone) ` y``\n"
          "and `[ref]: lost.md`\n\n[real](lost.md)\n")
    assert checker.scan(repo) == ["a.md:4 -> lost.md [missing-file]"]


def test_finding_angle_bracket_destinations(checker, repo):
    write(repo, "some file.md", "# Sec tion\n")
    write(repo, "a.md", "[ok](<some file.md#sec-tion>) [url](<https://example.org/a b>)\n"
          "[bad](<some file.md#gone> \"t\") [lost](<no file.md>)\n")
    assert checker.scan(repo) == [
        "a.md:2 -> no file.md [missing-file]",
        "a.md:2 -> some file.md#gone [missing-anchor]",
    ]


def test_finding_html_comments_hide_headings_anchors_and_links(checker, repo):
    write(repo, "a.md", "<!--\n# Hidden\n<a id=\"secret\"></a>\n[x](lost.md)\n-->\n"
          "# Shown\n# Shown\n[ok](#shown-1) [bad](#hidden) [bad](#secret) [bad](#shown-2)\n")
    assert checker.scan(repo) == [
        "a.md:8 -> a.md#hidden [missing-anchor]",
        "a.md:8 -> a.md#secret [missing-anchor]",
        "a.md:8 -> a.md#shown-2 [missing-anchor]",
    ]


def test_tables_front_matter_images_and_wrapped_lines(checker, repo):
    write(repo, "a.md", "---\nname: x\ndescription: y\n---\n# Real\n\n| a | b |\n|---|---|\n"
          "| [bad](lost.md) | ![img](gone.png) |\n\nwrapped text\nthen [bad](#name)\n[ok](#real)\n")
    assert checker.scan(repo) == [
        "a.md:12 -> a.md#name [missing-anchor]",
        "a.md:9 -> gone.png [missing-file]",
        "a.md:9 -> lost.md [missing-file]",
    ]
