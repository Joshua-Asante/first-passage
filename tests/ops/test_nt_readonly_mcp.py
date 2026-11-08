"""Read-only NinjaTrader MCP server: protocol, tools, confinement and the no-write surface."""
import ast
import codecs
import io
import json
import os
import sys
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
    text, _ = call(config, "nt_search", source="log", pattern="line.1")
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
    assert call(config, "nt_search", source="log", pattern="x", regex=True)[1]
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


# --- review fixes: mask before cutting, argument types, bounded reads ---------------

SYNTHETIC_ID = "ACCT-12345"


@pytest.mark.parametrize("start", [server.MAX_LINE_CHARS - 7, server.MAX_LINE_CHARS - 3,
                                   server.MAX_LINE_CHARS - 1])
def test_redaction_applies_before_line_cut(tmp_path, start):
    # The synthetic ID starts before character MAX_LINE_CHARS and ends after it.
    root = tmp_path / "NinjaTrader 8"
    (root / "log").mkdir(parents=True)
    (root / "trace").mkdir()
    prefix = "rejected "
    line = prefix + "x" * (start - len(prefix)) + SYNTHETIC_ID + " tail"
    assert line.index(SYNTHETIC_ID) < server.MAX_LINE_CHARS < line.index(SYNTHETIC_ID) + 10
    (root / "log" / "log.txt").write_text(f"{line}\n", encoding="utf-8")
    (root / "trace" / "trace.txt").write_text(f"{line}\n", encoding="utf-8")
    rules = tmp_path / "redact.txt"
    rules.write_text("ACCT-\\d+\n", encoding="utf-8")
    config = server.Config.build(root, redact_file=rules)
    expected = (prefix + "x" * (start - len(prefix)) + "[redacted] tail")[:server.MAX_LINE_CHARS]
    outputs = {"nt_tail": call(config, "nt_tail", source="log"),
               "nt_search": call(config, "nt_search", source="log", pattern="rejected"),
               "nt_search_trace": call(config, "nt_search", source="trace", pattern="xxx"),
               "nt_errors": call(config, "nt_errors")}
    for tool, (text, error) in outputs.items():
        assert not error, tool
        body = [row for row in text.splitlines()[1:] if row]
        assert body, tool
        for row in body:
            content = row if tool == "nt_tail" else row.split(": ", 1)[1]
            assert content == expected, tool
            assert not any(content.endswith(SYNTHETIC_ID[:k]) for k in range(1, 11)), tool


@pytest.mark.parametrize("name, arguments", [
    ("nt_tail", {"source": "log", "file": 5}),
    ("nt_tail", {"source": 5}),
    ("nt_search", {"source": "log", "pattern": None}),
    ("nt_search", {"source": "log", "pattern": "x", "glob": 3}),
    ("nt_search", {"source": "log", "pattern": "x", "regex": "yes"}),
    ("nt_list_files", {"source": "log", "glob": ["*"]}),
    ("nt_errors", {"max_files": "2"}),
])
def test_wrong_argument_types_are_tool_errors(nt, name, arguments):
    config, _ = nt
    result = server.call_tool(config, name, arguments)
    assert result["isError"]


def test_malformed_calls_do_not_stop_the_server(nt):
    config, _ = nt
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
         "params": {"name": "nt_tail", "arguments": {"source": "log", "file": 5}}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
         "params": {"name": "nt_search", "arguments": {"source": "log", "pattern": None}}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": ["nt_tail"]},
        {"jsonrpc": "2.0", "id": 4, "method": "initialize", "params": "x"},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call",
         "params": {"name": "nt_tail", "arguments": {"source": "log", "lines": 1}}},
    ]
    stdin = io.StringIO("\n".join(json.dumps(r) for r in requests) + "\n")
    stdout = io.StringIO()
    server.serve(config, stdin, stdout)
    responses = [json.loads(line) for line in stdout.getvalue().splitlines()]
    assert [r["id"] for r in responses] == [1, 2, 3, 4, 5]
    assert responses[0]["result"]["isError"] and responses[1]["result"]["isError"]
    assert responses[2]["error"]["code"] == -32602
    assert responses[3]["error"]["code"] == -32602
    assert not responses[4]["result"]["isError"]
    assert responses[4]["result"]["content"][0]["text"].endswith("\nafter")


@pytest.mark.parametrize("ending", ["\n", "\r\n", ""])
def test_tail_reads_from_end_of_large_file(tmp_path, monkeypatch, ending):
    monkeypatch.setattr(server, "READ_BLOCK", 64)
    root = tmp_path / "NinjaTrader 8"
    (root / "log").mkdir(parents=True)
    newline = ending or "\n"
    body = newline.join(f"row {i:05d} " + "y" * (i % 50) for i in range(1, 3001)) + ending
    path = root / "log" / "big.txt"
    path.write_bytes(("﻿" + body).encode("utf-8"))
    config = server.Config.build(root)
    expected = body.splitlines()
    for count in (1, 7, 200, 2000):
        text, error = call(config, "nt_tail", source="log", lines=count)
        assert not error
        lines = text.splitlines()
        assert lines[1:] == expected[-count:]
        assert lines[0] == f"big.txt: last {count} line(s)"
    small = root / "log" / "small.txt"
    small.write_bytes(b"\xef\xbb\xbfonly\r\nlines\n")
    text, _ = call(config, "nt_tail", source="log", file="small.txt", lines=50)
    assert text.splitlines() == ["small.txt: last 2 line(s)", "only", "lines"]


def test_tail_does_not_read_whole_file(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "READ_BLOCK", 128)
    root = tmp_path / "NinjaTrader 8"
    (root / "log").mkdir(parents=True)
    path = root / "log" / "big.txt"
    path.write_text("".join(f"row {i}\n" for i in range(100_000)), encoding="utf-8")
    config = server.Config.build(root)
    reads = []
    real_open = open

    class Spy:
        def __init__(self, handle):
            self._handle = handle

        def read(self, size=-1):
            reads.append(size)
            return self._handle.read(size)

        def __getattr__(self, name):
            return getattr(self._handle, name)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            self._handle.close()

    monkeypatch.setattr(server, "open", lambda *a, **k: Spy(real_open(*a, **k)), raising=False)
    text, _ = call(config, "nt_tail", source="log", lines=1)
    assert text.splitlines()[1] == "row 99999"
    assert reads and all(0 < size <= 128 for size in reads) and sum(reads) < 1024


def test_search_streams_lines_and_matches_previous_behaviour(nt, tmp_path):
    config, _ = nt
    text, _ = call(config, "nt_search", source="log", pattern="line", max_matches=3)
    assert text.splitlines() == [
        "3 match(es); stopped at max_matches=3",
        "log/log.20261106.00000.txt:1: line 1",
        "log/log.20261106.00000.txt:2: line 2",
        "log/log.20261106.00000.txt:3: line 3",
    ]
    crlf = config.sources["journal"] / "crlf.txt"
    crlf.write_bytes(b"\xef\xbb\xbfa\r\nhit one\r\nb\r\n\xff hit two\r\n")
    text, _ = call(config, "nt_search", source="journal", pattern="hit", glob="crlf.txt",
                   context=1)
    assert text.splitlines() == [
        "2 match(es)",
        "journal/crlf.txt:1- a",
        "journal/crlf.txt:2: hit one",
        "journal/crlf.txt:3- b",
        "journal/crlf.txt:4: � hit two",
    ]


# --- held findings, ruled on: fail closed without masking; literal search only ------

def _write_log(tmp_path, text):
    root = tmp_path / "NinjaTrader 8"
    (root / "log").mkdir(parents=True)
    (root / "trace").mkdir()
    (root / "log" / "log.txt").write_text(text, encoding="utf-8")
    return root


def _run_main(argv, requests):
    stdin = io.StringIO("".join(json.dumps(r) + "\n" for r in requests))
    stdout = io.StringIO()
    code = server.main(argv, stdin=stdin, stdout=stdout)
    return code, [json.loads(line) for line in stdout.getvalue().splitlines()]


TAIL_REQUEST = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                "params": {"name": "nt_tail", "arguments": {"source": "log"}}}
# Synthetic log-shaped line: timestamp|level|category|text with a Key='value' pair.
STAMP = "2026-01-02 03:04:05:678"
NOTE_LINE = f"{STAMP}|1|4|Note='fill {SYNTHETIC_ID}'\n"


def _fields(tmp_path, text="log kv:Note\n"):
    path = tmp_path / "fields.txt"
    path.write_text(text, encoding="utf-8")
    return path


def test_startup_refused_without_masking_choice(tmp_path, capsys):
    root = _write_log(tmp_path, f"fill {SYNTHETIC_ID}\n")
    with pytest.raises(SystemExit) as exc:
        _run_main(["--nt-root", str(root)], [TAIL_REQUEST])
    assert exc.value.code != 0
    err = capsys.readouterr().err
    assert "--fields-file" in err and "--redact-file" in err and "--allow-unredacted" in err


def test_startup_refused_with_redact_file_but_no_fields_file(tmp_path, capsys):
    # Masking alone is a backup: AGENTS.md requires approved-field reads.
    root = _write_log(tmp_path, NOTE_LINE)
    rules = tmp_path / "redact.txt"
    rules.write_text("ACCT-\\d+\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        _run_main(["--nt-root", str(root), "--redact-file", str(rules)], [TAIL_REQUEST])
    assert exc.value.code != 0 and "--fields-file" in capsys.readouterr().err


def test_startup_refused_with_empty_redact_file(tmp_path, capsys):
    root = _write_log(tmp_path, f"fill {SYNTHETIC_ID}\n")
    rules = tmp_path / "redact.txt"
    rules.write_text("# no patterns\n\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        _run_main(["--nt-root", str(root), "--fields-file", str(_fields(tmp_path)),
                   "--redact-file", str(rules)], [TAIL_REQUEST])
    assert exc.value.code != 0
    assert "no patterns" in capsys.readouterr().err


def test_redact_file_and_allow_unredacted_are_exclusive(tmp_path):
    root = _write_log(tmp_path, "x\n")
    rules = tmp_path / "redact.txt"
    rules.write_text("ACCT-\\d+\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        _run_main(["--nt-root", str(root), "--redact-file", str(rules), "--allow-unredacted"],
                  [TAIL_REQUEST])
    assert exc.value.code != 0


def test_allow_unredacted_starts_and_serves_raw(tmp_path):
    root = _write_log(tmp_path, f"fill {SYNTHETIC_ID}\n")
    code, responses = _run_main(["--nt-root", str(root), "--allow-unredacted"], [TAIL_REQUEST])
    assert code == 0
    assert responses[0]["result"]["content"][0]["text"].endswith(f"fill {SYNTHETIC_ID}")


def test_redact_file_starts_and_masks(tmp_path):
    root = _write_log(tmp_path, NOTE_LINE)
    rules = tmp_path / "redact.txt"
    rules.write_text("ACCT-\\d+\n", encoding="utf-8")
    code, responses = _run_main(["--nt-root", str(root), "--fields-file", str(_fields(tmp_path)),
                                 "--redact-file", str(rules)], [TAIL_REQUEST])
    assert code == 0
    text = responses[0]["result"]["content"][0]["text"]
    assert SYNTHETIC_ID not in text and text.endswith('{"kv:Note":"fill [redacted]"}')


def test_search_pattern_is_literal(tmp_path):
    root = _write_log(tmp_path, "axb(c)\na.b(c)*z\n(([x]+)+)+Z\n")
    config = server.Config.build(root)
    text, error = call(config, "nt_search", source="log", pattern="a.b(c)*")
    assert not error and text.splitlines() == ["1 match(es)", "log/log.txt:2: a.b(c)*z"]
    text, error = call(config, "nt_search", source="log", pattern="(([x]+)+)+Z")
    assert not error and text.splitlines()[0] == "1 match(es)"


def test_regex_options_removed_from_tools(nt):
    config, _ = nt
    search = server.TOOLS["nt_search"][1]["inputSchema"]["properties"]
    errors = server.TOOLS["nt_errors"][1]["inputSchema"]["properties"]
    assert "regex" not in search and "pattern" not in errors
    text, error = call(config, "nt_search", source="log", pattern="rejected", regex=True)
    assert error and "literal" in text
    text, error = call(config, "nt_errors", pattern=".*")
    assert error and "built-in" in text
    text, error = call(config, "nt_errors")
    assert not error and "insufficient margin" in text and "Connection lost" in text


# --- Codex review of 9accc66: oversized lines fail closed; match before masking -------

def _masked_config(tmp_path, text, rule):
    root = _write_log(tmp_path, text)
    (root / "trace" / "trace.txt").write_text(text, encoding="utf-8")
    rules = tmp_path / "redact.txt"
    rules.write_text(rule + "\n", encoding="utf-8")
    return server.Config.build(root, redact_file=rules)


@pytest.mark.parametrize("ending", ["\n", ""])
def test_oversized_line_is_omitted_not_partly_masked(tmp_path, ending):
    # A rule that needs the end of the line: masking a 64 KiB prefix would miss it.
    line = f"error {SYNTHETIC_ID} " + "p" * (server.MAX_LINE_BYTES + 10) + "END"
    config = _masked_config(tmp_path, f"before\n{line}{ending}", r"ACCT-12345(?=.*END$)")
    outputs = [call(config, "nt_tail", source="log"),
               call(config, "nt_search", source="log", pattern="error"),
               call(config, "nt_search", source="log", pattern="before", context=1),
               call(config, "nt_errors")]
    for text, error in outputs:
        assert not error
        assert SYNTHETIC_ID not in text and "12345" not in text
    tail = outputs[0][0].splitlines()
    assert tail[1:] == ["before", server.OMITTED_LINE]
    assert outputs[2][0].splitlines()[-1].endswith(server.OMITTED_LINE)


def test_search_matches_masked_text_only(tmp_path):
    # Reversed 11-07: matching the raw line let match counts rebuild a masked value.
    config = _masked_config(
        tmp_path, f"ok\nOrder rejected: insufficient margin {SYNTHETIC_ID}\nok\n", r".*ACCT-\d+.*")
    text, error = call(config, "nt_errors")
    assert not error and text.splitlines() == ["0 match(es)"]
    text, _ = call(config, "nt_search", source="log", pattern="insufficient margin")
    assert text.splitlines() == ["0 match(es)"]
    text, _ = call(config, "nt_search", source="log", pattern="[redacted]", context=1)
    assert text.splitlines() == ["1 match(es)", "log/log.txt:1- ok", "log/log.txt:2: [redacted]",
                                 "log/log.txt:3- ok"]


# --- 11-07 probe fixes ----------------------------------------------------------------

def _rules(tmp_path, text, encoding="utf-8"):
    rules = tmp_path / "redact.txt"
    rules.write_bytes(text.encode(encoding))
    return rules


def test_search_cannot_probe_a_masked_value(tmp_path):
    config = _masked_config(tmp_path, f"fill {SYNTHETIC_ID} done\n", r"ACCT-\d+")
    # Each prefix of the masked value, one character longer: none may match.
    for k in range(1, len(SYNTHETIC_ID) + 1):
        text, error = call(config, "nt_search", source="log", pattern=SYNTHETIC_ID[:k],
                           ignore_case=False)
        assert not error and text == "0 match(es)", k
    assert call(config, "nt_search", source="log", pattern="12345")[0].startswith("0 match")
    text, _ = call(config, "nt_search", source="log", pattern="fill [redacted] done")
    assert text.splitlines() == ["1 match(es)", "log/log.txt:1: fill [redacted] done"]


def test_glob_and_file_argument_match_masked_names(tmp_path):
    config = _masked_config(tmp_path, "x\n", r"ACCT-\d+")
    (config.sources["log"] / f"{SYNTHETIC_ID}.txt").write_text("named\n", encoding="utf-8")
    text, _ = call(config, "nt_list_files", source="log")
    assert SYNTHETIC_ID not in text and "[redacted].txt\t" in text
    for glob in ("ACCT-1*", f"{SYNTHETIC_ID}.txt", "*12345*"):
        assert call(config, "nt_list_files", source="log", glob=glob)[0].startswith("0 file(s)")
        assert call(config, "nt_search", source="log", pattern="named", glob=glob)[0] == "0 match(es)"
    assert call(config, "nt_list_files", source="log", glob="*redacted*")[0].startswith("1 file(s)")
    real, error = call(config, "nt_tail", source="log", file=f"{SYNTHETIC_ID}.txt")
    fake, _ = call(config, "nt_tail", source="log", file="ACCT-99999.txt")
    assert error and real == fake and SYNTHETIC_ID not in real
    text, error = call(config, "nt_tail", source="log", file="[redacted].txt")
    assert not error and text.splitlines() == ["[redacted].txt: last 1 line(s)", "named"]


@pytest.mark.parametrize("bom, encoding", [
    (codecs.BOM_UTF16_LE, "utf-16-le"), (codecs.BOM_UTF16_BE, "utf-16-be"),
    (codecs.BOM_UTF32_LE, "utf-32-le"), (codecs.BOM_UTF32_BE, "utf-32-be"),
])
def test_wide_encoded_files_are_refused(tmp_path, bom, encoding):
    config = _masked_config(tmp_path, "plain error\n", r"ACCT-\d+")
    (config.sources["log"] / "wide.txt").write_bytes(bom + f"error {SYNTHETIC_ID}\n".encode(encoding))
    text, error = call(config, "nt_tail", source="log", file="wide.txt")
    assert error and "not UTF-8" in text
    text, error = call(config, "nt_search", source="log", pattern="error")
    assert not error and text.splitlines()[:2] == ["1 match(es)", "log/log.txt:1: plain error"]
    assert text.splitlines()[2].startswith("note: skipped log/wide.txt: not UTF-8")
    assert "\x00" not in text and "12345" not in text


def test_nul_bytes_refuse_file_or_omit_line(tmp_path):
    config = _masked_config(tmp_path, "x\n", r"ACCT-\d+")
    log = config.sources["log"]
    (log / "nul.txt").write_bytes(b"e\x00r\x00r\x00o\x00r\x00 A\x00C\x00C\x00T\x00\n")
    assert "not UTF-8" in call(config, "nt_tail", source="log", file="nul.txt")[0]
    late = b"ok\n" * (server.READ_BLOCK // 3 + 10) + b"error A\x00CCT-12345\nlast error\n"
    (log / "late.txt").write_bytes(late)
    text, error = call(config, "nt_tail", source="log", file="late.txt", lines=2)
    assert not error and text.splitlines()[1:] == [server.OMITTED_NUL_LINE, "last error"]
    text, _ = call(config, "nt_search", source="log", pattern="error", glob="late.txt")
    assert text.splitlines()[0] == "1 match(es)" and "12345" not in text


def test_redact_file_bom_does_not_disable_first_pattern(tmp_path):
    root = _write_log(tmp_path, NOTE_LINE)
    rules = _rules(tmp_path, "﻿ACCT-\\d+\n")
    code, responses = _run_main(["--nt-root", str(root), "--fields-file", str(_fields(tmp_path)),
                                 "--redact-file", str(rules)], [TAIL_REQUEST])
    assert code == 0
    assert responses[0]["result"]["content"][0]["text"].endswith('{"kv:Note":"fill [redacted]"}')


@pytest.mark.parametrize("char", ["​", "‍", "﻿", "⁠"])
def test_redact_pattern_with_format_character_refused(tmp_path, capsys, char):
    root = _write_log(tmp_path, f"fill {SYNTHETIC_ID}\n")
    rules = _rules(tmp_path, f"# ids\nACCT{char}-\\d+\n")
    with pytest.raises(SystemExit) as exc:
        _run_main(["--nt-root", str(root), "--fields-file", str(_fields(tmp_path)),
                   "--redact-file", str(rules)], [TAIL_REQUEST])
    assert exc.value.code != 0 and "format character" in capsys.readouterr().err


def _junction(target, link):
    if sys.platform != "win32":
        pytest.skip("junctions are Windows-only")
    import _winapi
    _winapi.CreateJunction(str(target), str(link))


def test_walk_does_not_follow_junctions(tmp_path):
    config = _masked_config(tmp_path, "x\n", r"ACCT-\d+")
    log = config.sources["log"]
    (log / "a").mkdir()
    (log / "a" / "inner.txt").write_text("inner error\n", encoding="utf-8")
    _junction(log, log / "a" / "loop1")
    _junction(log / "a", log / "loop2")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "far.txt").write_text("far error\n", encoding="utf-8")
    _junction(outside, log / "out")
    text, error = call(config, "nt_list_files", source="log")
    assert not error
    names = [row.split("\t")[0] for row in text.splitlines()[1:]]
    assert sorted(names) == ["a/inner.txt", "log.txt"]
    text, _ = call(config, "nt_search", source="log", pattern="error")
    assert text.splitlines()[0] == "1 match(es)" and "far" not in text
    assert call(config, "nt_tail", source="log", file="out/far.txt")[1]


def test_symlinked_files_and_dirs_are_skipped(tmp_path):
    config = _masked_config(tmp_path, "x\n", r"ACCT-\d+")
    log = config.sources["log"]
    try:
        (log / "dup.txt").symlink_to(log / "log.txt")
        (log / "dir").symlink_to(log, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    text, _ = call(config, "nt_list_files", source="log")
    assert text.splitlines()[0].startswith("1 file(s)")


def _serve_bytes(config, raw: bytes):
    stdout = io.StringIO()
    server.serve(config, io.BytesIO(raw), stdout)
    text = stdout.getvalue()
    assert text.isascii()
    return [json.loads(line) for line in text.splitlines()]


GOOD = json.dumps({"jsonrpc": "2.0", "id": 9, "method": "ping"}).encode() + b"\n"


@pytest.mark.parametrize("bad", [
    b"\xff\xfe{}\n",
    b"[" * 200_000 + b"\n",
    b'{"jsonrpc":"2.0","id":' + b"9" * 5000 + b',"method":"ping"}\n',
    b'{"jsonrpc":"2.0","id":NaN,"method":"ping"}\n',
    b'{"jsonrpc":"2.0","id":Infinity,"method":"ping"}\n',
    b'{"jsonrpc":"2.0","id":1e999,"method":"ping"}\n',
], ids=["bad-utf8", "deep-nesting", "huge-int", "nan", "infinity", "overflow-float"])
def test_serve_survives_bad_lines(nt, bad):
    config, _ = nt
    responses = _serve_bytes(config, bad + GOOD)
    assert responses[0]["error"]["code"] == -32700 and responses[0]["id"] is None
    assert responses[1] == {"jsonrpc": "2.0", "id": 9, "result": {}}


def test_serve_rejects_non_scalar_id(nt):
    config, _ = nt
    line = json.dumps({"jsonrpc": "2.0", "id": [[1]], "method": "ping"}).encode() + b"\n"
    responses = _serve_bytes(config, line + GOOD)
    assert responses[0]["error"]["code"] == -32600 and responses[0]["id"] is None
    assert responses[1]["id"] == 9


def test_serve_caps_request_line(nt, monkeypatch):
    config, _ = nt
    monkeypatch.setattr(server, "MAX_REQUEST_BYTES", 1000)
    monkeypatch.setattr(server, "READ_BLOCK", 64)
    big = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "ping", "pad": "p" * 5000}).encode()
    responses = _serve_bytes(config, big + b"\n" + GOOD + big)
    assert [r.get("id") for r in responses] == [None, 9, None]
    assert all(r["error"]["code"] == -32700 for r in (responses[0], responses[2]))


@pytest.mark.parametrize("argv_tail", [
    ["--allow"],
    ["--redact"],
    ["--fields"],
    ["--fields-file", "{fields}", "--redact-file", "{rules}", "--redact-file", "{rules}"],
    ["--fields-file", "{fields}", "--redact-file", "{dir}"],
    ["--allow-unredacted", "--journal-dir", "{dir}", "--journal-dir", "{dir}"],
    ["--fields-file", "{fields}", "--fields-file", "{fields}"],
    ["--fields-file", "{dir}"],
    ["--fields-file", "{fields}", "--allow-unredacted"],
    ["--fields-file", "{fields}", "--refusal-dir", "{dir}", "--refusal-dir", "{dir}"],
])
def test_startup_argument_checks(tmp_path, argv_tail):
    root = _write_log(tmp_path, "x\n")
    rules = _rules(tmp_path, "ACCT-\\d+\n")
    fields = _fields(tmp_path)
    argv = ["--nt-root", str(root)] + [a.format(rules=rules, dir=tmp_path, fields=fields)
                                       for a in argv_tail]
    with pytest.raises(SystemExit) as exc:
        _run_main(argv, [TAIL_REQUEST])
    assert exc.value.code != 0


def test_unreadable_file_is_skipped_and_noted(nt, monkeypatch):
    config, _ = nt
    real_open = open

    def locked(path, *args, **kwargs):
        if Path(path).name == "log.20261106.00000.txt":
            raise PermissionError(13, "locked")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(server, "open", locked, raising=False)
    text, error = call(config, "nt_search", source="log", pattern="rejected")
    assert not error
    assert text.splitlines()[:2] == ["1 match(es)", "log/log.20261105.00000.txt:2: Order rejected: OLD"]
    assert "note: skipped log/log.20261106.00000.txt: PermissionError: locked" in text


def test_file_failing_stat_is_skipped_in_listing(nt, monkeypatch):
    config, _ = nt
    real_lstat = Path.lstat

    def lstat(self):
        if self.name == "log.20261106.00000.txt":
            raise FileNotFoundError(2, "gone")
        return real_lstat(self)

    monkeypatch.setattr(Path, "lstat", lstat)
    text, error = call(config, "nt_list_files", source="log")
    assert not error and text.splitlines()[0].startswith("1 file(s)")
    assert "note: skipped log/log.20261106.00000.txt: FileNotFoundError: gone" in text
    text, error = call(config, "nt_errors")
    assert not error and "Order rejected: OLD" in text


def test_read_stops_at_size_taken_at_open(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "READ_BLOCK", 64)
    root = _write_log(tmp_path, "".join(f"hit {i}\n" for i in range(50)))
    config = server.Config.build(root)
    path = config.sources["log"] / "log.txt"
    real_open = open

    class Appending:
        def __init__(self, handle):
            self._handle = handle

        def read(self, size=-1):
            with real_open(path, "ab") as writer:
                writer.write(b"hit more\n" * 20)
            return self._handle.read(size)

        def __getattr__(self, name):
            return getattr(self._handle, name)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            self._handle.close()

    monkeypatch.setattr(server, "open", lambda *a, **k: Appending(real_open(*a, **k)), raising=False)
    text, _ = call(config, "nt_search", source="log", pattern="hit", max_matches=1000)
    assert text.splitlines()[0] == "50 match(es)"


def test_read_budget_stops_the_call(nt, monkeypatch):
    config, _ = nt
    monkeypatch.setattr(server, "MAX_CALL_BYTES", 10)
    text, error = call(config, "nt_search", source="log", pattern="line")
    assert not error and "stopped: read budget reached" in text.splitlines()[0]
    text, error = call(config, "nt_tail", source="log")
    assert error and "read budget" in text


@pytest.mark.parametrize("key", ["pattern", "glob", "file"])
def test_long_string_arguments_refused(nt, key):
    config, _ = nt
    arguments = {"source": "log", "pattern": "x", key: "a" * (server.MAX_ARG_CHARS + 1)}
    tool = "nt_tail" if key == "file" else "nt_search"
    if tool == "nt_tail":
        del arguments["pattern"]
    text, error = call(config, tool, **arguments)
    assert error and "longer than" in text


@pytest.mark.parametrize("name, arguments", [
    ("nt_tail", {"source": "log", "bogus": 1}),
    ("nt_list_sources", {"x": None}),
    ("nt_search", {"source": "log", "pattern": "x", "Pattern": "y"}),
    ("nt_errors", {"max_file": 3}),
])
def test_unknown_argument_keys_refused(nt, name, arguments):
    config, _ = nt
    text, error = call(config, name, **arguments)
    assert error and "unknown argument" in text


def test_search_never_matches_placeholder_text(tmp_path):
    line = "z" * (server.MAX_LINE_BYTES + 5)
    config = _masked_config(tmp_path, f"{line}\n", r"ACCT-\d+")
    for pattern in ("omitted", "bytes", "[line over"):
        assert call(config, "nt_search", source="log", pattern=pattern)[0] == "0 match(es)"


def test_masking_is_per_line_not_on_joined_output(tmp_path):
    config = _masked_config(tmp_path, "keep x\ny keep\n", r"x\ny")
    text, _ = call(config, "nt_tail", source="log")
    assert text.splitlines()[1:] == ["keep x", "y keep"]
    text, error = call(config, "nt_tail", source="log", file="x\ny")
    assert error and "[redacted]" in text


# --- #1136: approved-field mode --------------------------------------------------------

MARKER = "MARKER-SECRET-7Q"
FIELDS = """\
# synthetic allow-list
log timestamp
log level
log kv:Status
trace timestamp
trace kv:state
journal json:kind
journal json:body.code
refusal json:code
refusal json:fields.reason
"""


@pytest.fixture
def approved(tmp_path):
    root = tmp_path / "NinjaTrader 8"
    (root / "log").mkdir(parents=True)
    (root / "trace").mkdir()
    (root / "log" / "log.txt").write_text(
        f"{STAMP}|1|4|Status='Filled' Secret='{MARKER}' error {MARKER}\n"
        f"{STAMP}|2|4|free text only {MARKER}\n"
        f"not a log line {MARKER} Status='Spoof'\n"
        f"{MARKER}|{MARKER}|{MARKER}|Status='Working' Note='x Status=Inner'\n", encoding="utf-8")
    (root / "trace" / "trace.txt").write_text(
        f"{STAMP} connect state=up acct={MARKER}\n{MARKER} state=down\n", encoding="utf-8")
    journal = tmp_path / "journal"
    journal.mkdir()
    body = json.dumps({"code": "REJECTED", "detail": MARKER})
    records = [{"seq": 1, "prev": "0" * 8, "kind": "request", "body": body, "hash": MARKER},
               {"seq": 2, "prev": MARKER, "kind": "fill", "body": "not json", "hash": "h"}]
    (journal / "a.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records)
                                     + f"{MARKER} not json\n", encoding="utf-8")
    refusal = tmp_path / "refusal"
    refusal.mkdir()
    (refusal / "r1.json").write_text(json.dumps(
        {"code": "NOT_FLAT", "utc": "2026-01-02T03:04:05Z",
         "fields": {"reason": "position open", "account": MARKER}}, indent=2), encoding="utf-8")
    export = tmp_path / "export"
    export.mkdir()
    (export / "e.csv").write_text(f"Status,Account\nFilled,{MARKER}\n", encoding="utf-8")
    return server.Config.build(root, journal_dir=journal, export_dir=export,
                               refusal_dir=refusal, fields_file=_fields(tmp_path, FIELDS))


def _all_outputs(config):
    calls = [("nt_errors", {})]
    for source in ("log", "trace", "journal", "refusal", "export"):
        calls.append(("nt_tail", {"source": source}))
        for pattern in ("", "MARKER", "e", "Status", "Secret"):
            calls.append(("nt_search", {"source": source, "pattern": pattern, "context": 2}))
    return [(name, args, *call(config, name, **args)) for name, args in calls]


def test_unapproved_fields_never_appear(approved):
    for name, args, text, error in _all_outputs(approved):
        assert not error, (name, args, text)
        assert MARKER not in text and "SECRET" not in text.upper(), (name, args)
        assert "Spoof" not in text and "Inner" not in text, (name, args)


def test_approved_kv_and_fixed_fields(approved):
    text, error = call(approved, "nt_tail", source="log")
    assert not error
    assert text.splitlines() == [
        "log.txt: last 4 line(s); 1 without an approved field omitted",
        '{"timestamp":"2026-01-02 03:04:05:678","level":"1","kv:Status":"Filled"}',
        '{"timestamp":"2026-01-02 03:04:05:678","level":"2"}',
        '{"kv:Status":"Working"}',
    ]
    text, _ = call(approved, "nt_tail", source="trace")
    assert text.splitlines() == [
        "trace.txt: last 2 line(s); 1 without an approved field omitted",
        '{"timestamp":"2026-01-02 03:04:05:678","kv:state":"up"}',
    ]


def test_journal_body_is_decoded_and_paths_select(approved):
    text, error = call(approved, "nt_tail", source="journal")
    assert not error
    assert text.splitlines() == [
        "a.jsonl: last 3 line(s); 1 without an approved field omitted",
        '{"json:kind":"request","json:body.code":"REJECTED"}',
        '{"json:kind":"fill"}',
    ]
    text, _ = call(approved, "nt_search", source="journal", pattern="rejected")
    assert text.splitlines() == [
        "1 match(es); 1 line(s) without an approved field skipped",
        'journal/a.jsonl:1: {"json:kind":"request","json:body.code":"REJECTED"}']


def test_refusal_file_is_one_record(approved):
    text, error = call(approved, "nt_tail", source="refusal")
    assert not error
    assert text.splitlines() == ["r1.json: last 1 record(s)",
                                 '{"json:code":"NOT_FLAT","json:fields.reason":"position open"}']
    text, _ = call(approved, "nt_search", source="refusal", pattern="position")
    assert text.splitlines()[0] == "1 match(es)"


def test_exports_emit_nothing(approved):
    text, error = call(approved, "nt_tail", source="export")
    assert not error
    assert text.splitlines() == ["e.csv: last 2 line(s); 2 without an approved field omitted"]
    text, _ = call(approved, "nt_search", source="export", pattern="")
    assert text.splitlines() == ["0 match(es); 2 line(s) without an approved field skipped"]


def test_search_matches_only_approved_values(approved):
    # "error" and the MARKER are in line 1's free text, but in no approved value.
    text, _ = call(approved, "nt_errors")
    assert text.splitlines()[0].startswith("0 match(es)")
    assert call(approved, "nt_search", source="log", pattern=MARKER)[0].startswith("0 match")
    assert call(approved, "nt_search", source="log", pattern="Secret")[0].startswith("0 match")
    text, _ = call(approved, "nt_search", source="log", pattern="filled", context=1)
    assert text.splitlines() == [
        "1 match(es); 1 line(s) without an approved field skipped",
        'log/log.txt:1: {"timestamp":"2026-01-02 03:04:05:678","level":"1","kv:Status":"Filled"}',
        'log/log.txt:2- {"timestamp":"2026-01-02 03:04:05:678","level":"2"}',
    ]


def test_masking_still_runs_on_approved_values(tmp_path):
    root = _write_log(tmp_path, f"{STAMP}|1|4|Note='fill {SYNTHETIC_ID}' Count=12345\n")
    rules = _rules(tmp_path, "ACCT-\\d+\n^12345$\n")
    config = server.Config.build(root, redact_file=rules,
                                 fields_file=_fields(tmp_path, "log kv:Note\nlog kv:Count\n"))
    text, _ = call(config, "nt_tail", source="log")
    assert text.splitlines()[1] == '{"kv:Note":"fill [redacted]","kv:Count":"[redacted]"}'
    for k in range(1, len(SYNTHETIC_ID) + 1):
        assert call(config, "nt_search", source="log", pattern=SYNTHETIC_ID[:k],
                    ignore_case=False)[0] == "0 match(es)", k


def test_oversized_line_is_omitted_in_approved_mode(tmp_path):
    line = f"{STAMP}|1|4|Note='{SYNTHETIC_ID}' " + "p" * (server.MAX_LINE_BYTES + 10)
    root = _write_log(tmp_path, f"{line}\n")
    config = server.Config.build(root, fields_file=_fields(tmp_path))
    text, _ = call(config, "nt_tail", source="log")
    assert text.splitlines()[1:] == [server.OMITTED_LINE] and SYNTHETIC_ID not in text


def test_json_paths_emit_scalars_only(tmp_path):
    root = _write_log(tmp_path, "x\n")
    journal = tmp_path / "journal"
    journal.mkdir()
    record = {"kind": "k", "body": json.dumps({"inner": {"a": MARKER}, "n": 3, "ok": True}),
              "list": [MARKER]}
    (journal / "j.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
    fields = _fields(tmp_path, "journal json:body.inner\njournal json:list\n"
                               "journal json:body.n\njournal json:body.ok\n")
    config = server.Config.build(root, journal_dir=journal, fields_file=fields)
    text, _ = call(config, "nt_tail", source="journal")
    assert text.splitlines()[1:] == ['{"json:body.n":3,"json:body.ok":true}']


@pytest.mark.parametrize("content, message", [
    ("log\n", "expected '<source> <field>'"),
    ("log timestamp extra\n", "expected '<source> <field>'"),
    ("account timestamp\n", "unknown source"),
    ("log kv:\n", "not a field log can approve"),
    ("log kv:Bad-Key\n", "not a field log can approve"),
    ("log json:kind\n", "not a field log can approve"),
    ("journal kv:Status\n", "not a field journal can approve"),
    ("journal json:body..code\n", "not a field journal can approve"),
    ("trace level\n", "not a field trace can approve"),
    ("export json:a\n", "not a field export can approve"),
    ("export kv:Status\n", "not a field export can approve"),
    ("log regex:.*\n", "not a field log can approve"),
    ("# only comments\n\n", "no rules"),
    ("log kv:Sta​tus\n", "format character"),
])
def test_malformed_fields_file_refuses_start(tmp_path, capsys, content, message):
    root = _write_log(tmp_path, NOTE_LINE)
    with pytest.raises(SystemExit) as exc:
        _run_main(["--nt-root", str(root), "--fields-file", str(_fields(tmp_path, content))],
                  [TAIL_REQUEST])
    assert exc.value.code != 0
    err = capsys.readouterr().err
    assert "--fields-file" in err and message in err


def test_fields_file_starts_and_serves_approved_only(tmp_path):
    root = _write_log(tmp_path, f"{STAMP}|1|4|Note='ok' Account='{MARKER}'\n")
    fields = _fields(tmp_path, "﻿# signed\nlog kv:Note\n")
    code, responses = _run_main(["--nt-root", str(root), "--fields-file", str(fields)],
                                [TAIL_REQUEST])
    assert code == 0
    text = responses[0]["result"]["content"][0]["text"]
    assert text.splitlines() == ["log.txt: last 1 line(s)", '{"kv:Note":"ok"}']
