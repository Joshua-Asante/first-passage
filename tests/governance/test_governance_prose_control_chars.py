"""Adversarial tests for check_governance_prose_control_chars.

Per lesson_discipline_guards_need_adversarial_tests: a guard earns trust only by
FAILING on a planted defect. The form-feed fixture is the load-bearing case —
if it ever passes, the gate has gone vacuous.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

_spec = importlib.util.spec_from_file_location(
    "check_governance_prose_control_chars",
    REPO / "scripts" / "check_governance_prose_control_chars.py",
)
cg = importlib.util.module_from_spec(_spec)
sys.modules["check_governance_prose_control_chars"] = cg
_spec.loader.exec_module(cg)


def _write(tmp_path: Path, name: str, text: str) -> Path:
    f = tmp_path / name
    f.write_text(text, encoding="utf-8", newline="\n")
    return f


# ---------------------------------------------------------------- planted defects

def test_planted_form_feed_fails(tmp_path):
    """THE defect shape: literal U+000C between words on a SESSIONS Shipped line."""
    f = _write(
        tmp_path,
        "SESSIONS.md",
        "**Shipped:** branch\x0cix/mcl-ledger-stale-1m-cache-claim\n",
    )
    msgs = cg.scan_file(f)
    assert msgs, "gate went VACUOUS: planted form-feed passed"
    assert "U+000C" in msgs[0]
    assert ":1:" in msgs[0]  # line 1


def test_planted_vertical_tab_fails(tmp_path):
    f = _write(tmp_path, "STATE.md", "hello\x0bworld\n")
    msgs = cg.scan_file(f)
    assert msgs, "gate went VACUOUS: planted VT passed"
    assert "U+000B" in msgs[0]


def test_planted_bel_fails(tmp_path):
    """Mangled ``\\a`` escape (real hit in docs/notes prune disposition)."""
    f = _write(tmp_path, "note.md", "DELETED husks: \\\x07dr-lifecycle\n")
    msgs = cg.scan_file(f)
    assert msgs, "gate went VACUOUS: planted BEL passed"
    assert "U+0007" in msgs[0]


def test_report_includes_column(tmp_path):
    f = _write(tmp_path, "x.md", "ab\x0ccd\n")
    msgs = cg.scan_file(f)
    assert msgs
    # 'a'=1 'b'=2 FF=3
    assert ":1:3:" in msgs[0]


# ---------------------------------------------------------------- negative controls

def test_clean_file_passes(tmp_path):
    f = _write(
        tmp_path,
        "clean.md",
        "# Title\n\n**Shipped:** branch fix/mcl-ledger\n\tindented\n",
    )
    assert cg.scan_file(f) == []


def test_crlf_allowed(tmp_path):
    """CR is allowed — Windows autocrlf checkouts must not brick the gate."""
    f = tmp_path / "crlf.md"
    f.write_bytes(b"**Shipped:** branch fix/example\r\n")
    assert cg.scan_file(f) == []


def test_find_control_chars_empty_is_not_a_pass_claim():
    """Vacuous empty-input assert is not a test — exercise the finder directly."""
    assert cg.find_control_chars("") == []
    assert cg.find_control_chars("\x0c") == [(1, 1, 0x0C)]
