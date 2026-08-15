"""Unit tests for scripts/gate_fire_log.py — 2026-08-15 governance-belt audit action 2."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "gate_fire_log", REPO / "scripts" / "gate_fire_log.py"
)
gfl = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = gfl
_SPEC.loader.exec_module(gfl)


def test_log_fire_appends_one_json_line(tmp_path, monkeypatch):
    log_path = tmp_path / "gate_fires.jsonl"
    monkeypatch.setattr(gfl, "LOG_PATH", log_path)

    gfl.log_fire("repo_retrieve", query="foo bar", n_hits=3)

    assert log_path.is_file()
    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["tool"] == "repo_retrieve"
    assert record["query"] == "foo bar"
    assert record["n_hits"] == 3
    assert "ts" in record and record["ts"]


def test_log_fire_never_raises_on_write_failure(tmp_path, monkeypatch):
    # Point LOG_PATH's parent at a path that can't be created (a file, not a dir).
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory", encoding="utf-8")
    monkeypatch.setattr(gfl, "LOG_PATH", blocker / "gate_fires.jsonl")

    gfl.log_fire("some_tool", n_hits=1)  # must not raise


def test_tally_counts_by_tool(tmp_path, monkeypatch):
    log_path = tmp_path / "gate_fires.jsonl"
    monkeypatch.setattr(gfl, "LOG_PATH", log_path)

    gfl.log_fire("repo_retrieve", n_hits=1)
    gfl.log_fire("repo_retrieve", n_hits=0)
    gfl.log_fire("sync_liveness_indexes", n_problems=2)

    counts = gfl.tally()
    assert counts == {"repo_retrieve": 2, "sync_liveness_indexes": 1}


def test_tally_since_filters_by_timestamp(tmp_path):
    log_path = tmp_path / "gate_fires.jsonl"
    log_path.write_text(
        json.dumps({"ts": "2026-08-01T00:00:00+00:00", "tool": "old_tool"}) + "\n"
        + json.dumps({"ts": "2026-08-20T00:00:00+00:00", "tool": "new_tool"}) + "\n",
        encoding="utf-8",
    )
    counts = gfl.tally(since="2026-08-15", log_path=log_path)
    assert counts == {"new_tool": 1}


def test_tally_ignores_malformed_lines(tmp_path):
    log_path = tmp_path / "gate_fires.jsonl"
    log_path.write_text(
        "not json\n" + json.dumps({"ts": "2026-08-15T00:00:00+00:00", "tool": "x"}) + "\n",
        encoding="utf-8",
    )
    assert gfl.tally(log_path=log_path) == {"x": 1}


def test_cli_tally_empty_log(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gfl, "LOG_PATH", tmp_path / "does_not_exist.jsonl")
    rc = gfl.main(["--tally"])
    assert rc == 0
    assert "no fires recorded" in capsys.readouterr().out
