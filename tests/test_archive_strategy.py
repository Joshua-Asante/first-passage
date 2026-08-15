"""Unit tests for scripts/archive_strategy.py."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_PATH = REPO_ROOT / "scripts" / "archive_strategy.py"
_spec = importlib.util.spec_from_file_location("archive_strategy", _PATH)
mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(mod)


def test_rewrite_manifest_path_keeps_hash():
    text = (
        "# comment\n"
        "aabbccdd00112233445566778899aabbccddeeff00112233445566778899aabb  "
        "core/strategies/guardian/foo.pine\n"
    )
    out = mod.rewrite_manifest_path(
        text,
        "core/strategies/guardian/foo.pine",
        "core/strategies/_archive/guardian/foo.pine",
    )
    assert "aabbccdd00112233445566778899aabbccddeeff00112233445566778899aabb  " in out
    assert "core/strategies/_archive/guardian/foo.pine" in out
    assert "core/strategies/guardian/foo.pine\n" not in out


def test_move_to_archive_refuses_overwrite(tmp_path: Path):
    src = tmp_path / "core" / "strategies" / "guardian" / "foo.pine"
    src.parent.mkdir(parents=True)
    src.write_text("// pine\n", encoding="utf-8")
    dest_dir = tmp_path / "core" / "strategies" / "_archive" / "guardian"
    dest_dir.mkdir(parents=True)
    (dest_dir / "foo.pine").write_text("existing\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        mod.move_to_archive(tmp_path, "core/strategies/guardian/foo.pine", "guardian")


def test_write_card_max_40_lines(tmp_path: Path):
    card = tmp_path / "CARD.md"
    mod.write_card(
        card,
        slug="guardian_gold_v5.5",
        family="guardian",
        disposition="VENUE_LESS_CFD",
        body_rel="core/strategies/_archive/guardian/",
        pin_lines=["abc…  guardian_gold_v5.5.pine"],
        adr_links=["docs/adr/2026-08-04-strategy-coldstore-phase-a.md"],
    )
    lines = card.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 40
    assert "VENUE_LESS_CFD" in card.read_text(encoding="utf-8")


def test_main_preflight_blocks_move_when_dest_exists(tmp_path: Path):
    """CLI must fail before any move when an archive destination already exists."""
    src = tmp_path / "core" / "strategies" / "guardian" / "foo.pine"
    src.parent.mkdir(parents=True)
    src.write_text("// pine\n", encoding="utf-8")
    dest_dir = tmp_path / "core" / "strategies" / "_archive" / "guardian"
    dest_dir.mkdir(parents=True)
    (dest_dir / "foo.pine").write_text("existing\n", encoding="utf-8")
    card_parent = tmp_path / "docs" / "cards"
    card_parent.mkdir(parents=True)

    rc = mod.main(
        [
            "--repo-root",
            str(tmp_path),
            "--family",
            "guardian",
            "--disposition",
            "VENUE_LESS_CFD",
            "--slug",
            "foo",
            "--files",
            "core/strategies/guardian/foo.pine",
            "--card-out",
            "docs/cards/foo.md",
        ]
    )
    assert rc == 1
    assert src.is_file(), "source must remain at original path after failed preflight"
    assert src.read_text(encoding="utf-8") == "// pine\n"


def test_main_preflight_blocks_move_when_manifest_missing(tmp_path: Path):
    """CLI must fail before any move when a listed --manifest path is missing."""
    src = tmp_path / "core" / "strategies" / "guardian" / "foo.pine"
    src.parent.mkdir(parents=True)
    src.write_text("// pine\n", encoding="utf-8")
    card_parent = tmp_path / "docs" / "cards"
    card_parent.mkdir(parents=True)

    rc = mod.main(
        [
            "--repo-root",
            str(tmp_path),
            "--family",
            "guardian",
            "--disposition",
            "VENUE_LESS_CFD",
            "--slug",
            "foo",
            "--files",
            "core/strategies/guardian/foo.pine",
            "--manifest",
            "core/strategies/MANIFEST.sha256",
            "--card-out",
            "docs/cards/foo.md",
        ]
    )
    assert rc == 1
    assert src.is_file(), "source must remain at original path after failed preflight"
    assert src.read_text(encoding="utf-8") == "// pine\n"
