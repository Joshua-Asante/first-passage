"""Read-only NinjaTrader MCP server: protocol, tools, confinement and the no-write surface."""
import ast
import io
import json
import os
from pathlib import Path

import pytest

import nt_readonly_mcp as server

SOURCE_FILE = Path(server.__file__)


@pytest.fixture
def nt(tmp_path):
    root = tmp_path / "NinjaTrader 8"
    (root / "log").mkdir(parents=True)
    (root / "trace").mkdir()
    journal = tmp_path / "journal"
    journal.mkdir()
    old = root / "log" / "log.20261105.00000.txt"
    old.write_text("old line\nOrder rejected: OLD\n", encoding="utf-8")
    os.utime(old, (1_000_000, 1_000_000))
    new = root / "log" / "log.20261106.00000.txt"
    new.write_text("".join(f"line {i}\n" for i in range(1, 11))
                   + "Order rejected: insufficient margin ACCT-12345\nafter\n", encoding="utf-8")
    (root / "trace" / "trace.20261106.00000.txt").write_text(
        "ok\nConnection lost\nok\n", encoding="utf-8")
    (journal / "orb.jsonl").write_text('{"event":"request"}\n', encoding="utf-8")
    outside = tmp_path / "secret.txt"
    outside.write_text("outside\n", encoding="utf-8")
    return server.Config.build(root, journal_dir=journal), tmp_path


def call(config, name, **arguments):
    result = server.call_tool(config, name, arguments)
    return result["content"][0]["text"], result["isError"]


def test_protocol_round_trip(nt):
    config, _ = nt
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
         "params": {"name": "nt_tail", "arguments": {"source": "log", "lines": 1}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "nt_place_order"}},
        {"jsonrpc": "2.0", "id": 5, "method": "resources/list"},
    ]
    stdin = io.StringIO("\n".join(json.dumps(r) for r in requests) + "\nnot json\n")
    stdout = io.StringIO()
    server.serve(config, stdin, stdout)
    responses = [json.loads(line) for line in stdout.getvalue().splitlines()]
    assert [r.get("id") for r in responses] == [1, 2, 3, 4, 5, None]
    assert responses[0]["result"]["protocolVersion"] == "2025-06-18"
    assert {t["name"] for t in responses[1]["result"]["tools"]} == set(server.TOOLS)
    assert responses[2]["result"]["content"][0]["text"].endswith("\nafter")
    assert responses[3]["error"]["code"] == -32602
    assert responses[4]["error"]["code"] == -32601
    assert responses[5]["error"]["code"] == -32700


def test_unknown_protocol_version_gets_latest(nt):
    config, _ = nt
    response = server.handle(config, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                                      "params": {"protocolVersion": "1999-01-01"}})
    assert response["result"]["protocolVersion"] == server.SUPPORTED_PROTOCOLS[0]


def test_list_sources_and_files_newest_first(nt):
    config, _ = nt
    text, error = call(config, "nt_list_sources")
    assert not error and "journal\tok" in text and "export" not in text
    text, error = call(config, "nt_list_files", source="log")
    assert not error
    rows = text.splitlines()[1:]
    assert rows[0].startswith("log.20261106") and rows[1].startswith("log.20261105")


def test_tail_named_file(nt):
    config, _ = nt
    text, error = call(config, "nt_tail", source="log", file="log.20261105.00000.txt", lines=1)
    assert not error and text.splitlines()[1] == "Order rejected: OLD"


def test_search_literal_and_context(nt):
    config, _ = nt
    text, error = call(config, "nt_search", source="log", pattern="REJECTED", context=1)
    assert not error
    lines = text.splitlines()
    assert lines[0] == "2 match(es)"
    assert "log/log.20261106.00000.txt:10- line 10" in lines
    assert "log/log.20261106.00000.txt:12- after" in lines
    text, _ = call(config, "nt_search", source="log", pattern="line.1", regex=False)
    assert text.startswith("0 match")


def test_search_caps_matches(nt):
    config, _ = nt
    text, _ = call(config, "nt_search", source="log", pattern="line", max_matches=3)
    assert text.startswith("3 match(es); stopped")


def test_errors_reads_log_and_trace(nt):
    config, _ = nt
    text, error = call(config, "nt_errors")
    assert not error
    assert "insufficient margin" in text and "Connection lost" in text


def test_redaction(nt, tmp_path):
    config, _ = nt
    rules = tmp_path / "redact.txt"
    rules.write_text("# account ids\nACCT-\\d+\n", encoding="utf-8")
    redacted = server.Config.build(config.sources["log"].parent, redact_file=rules)
    text, _ = call(redacted, "nt_errors")
    assert "ACCT-12345" not in text and "[redacted]" in text


@pytest.mark.parametrize("name", ["../../secret.txt", "../journal/orb.jsonl"])
def test_paths_cannot_escape_source(nt, name):
    config, _ = nt
    text, error = call(config, "nt_tail", source="log", file=name)
    assert error and "escapes" in text


def test_symlink_out_of_source_is_ignored(nt):
    config, tmp_path = nt
    link = config.sources["log"] / "link.txt"
    try:
        link.symlink_to(tmp_path / "secret.txt")
    except OSError:
        pytest.skip("symlinks unavailable")
    text, _ = call(config, "nt_list_files", source="log")
    assert "link.txt" not in text
    text, error = call(config, "nt_tail", source="log", file="link.txt")
    assert error


def test_bad_arguments_are_tool_errors(nt):
    config, _ = nt
    assert call(config, "nt_tail", source="export")[1]
    assert call(config, "nt_tail")[1]
    assert call(config, "nt_search", source="log", pattern="(", regex=True)[1]
    assert call(config, "nt_tail", source="log", lines="5")[1]


def test_module_has_no_write_or_network_surface():
    tree = ast.parse(SOURCE_FILE.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {alias.name.split(".")[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    forbidden = {"socket", "http", "urllib", "requests", "subprocess", "ctypes", "asyncio",
                 "shutil", "tempfile", "ssl", "multiprocessing", "os"}
    assert not imported & forbidden
    allowed_open_modes = {"rb"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
            assert name not in {"write_text", "write_bytes", "unlink", "rename", "replace",
                                "mkdir", "rmdir", "touch", "symlink_to", "chmod"} or (
                isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)
                and func.value.id == "stdout"), ast.unparse(node)
            if name == "open":
                assert len(node.args) >= 2 and isinstance(node.args[1], ast.Constant)
                assert node.args[1].value in allowed_open_modes
