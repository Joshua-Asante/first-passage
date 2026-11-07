"""Read-only NinjaTrader 8 MCP server (stdio, standard library only).

Lets an agent read the text files NinjaTrader and the strategy instances leave on
disk, instead of screenshotting the Log tab or the Output window. It runs outside
NinjaTrader and never talks to it:

* no sockets, HTTP, ATI, AddOn or subprocess; it only opens files for reading;
* every path is confined to a configured source directory (symlinks resolved);
* it places, changes and cancels nothing, so AGENTS.md money controls 1 and 3 and
  spec check B1 (no network calls, ATI, add-ons) are untouched.

Its output can carry account data (fills, account names, balances). That data
reaches the agent's context and must never be written into this repository
(AGENTS.md data rules, spec B15). ``--redact-file`` masks patterns, one regex per
line, before anything leaves the server. Do not give this server to Codex: the
journal and logs can carry strategy parameters.

Sources (each optional except ``log`` and ``trace``, which derive from ``--nt-root``):

    log      <nt-root>/log      NinjaTrader log files
    trace    <nt-root>/trace    NinjaTrader trace files
    journal  --journal-dir      the strategy instances' own journals (spec B2)
    export   --export-dir       exports kept in private custody (spec B11)

The files are read as plain text; no NinjaTrader line format is assumed.

Run::

    python ops/nt_readonly_mcp.py --nt-root "C:\\Users\\<you>\\Documents\\NinjaTrader 8"
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

SERVER_NAME = "nt-readonly"
SERVER_VERSION = "0.1.0"
SUPPORTED_PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")

MAX_LINES = 2000
MAX_MATCHES = 1000
MAX_OUTPUT_CHARS = 200_000
MAX_LINE_CHARS = 2000
DEFAULT_ERROR_PATTERN = r"error|exception|reject|disconnect|connection ?lost|lost connection|failed|halt"


class ToolError(Exception):
    """A request the server refuses; reported to the client as a tool error."""


@dataclass
class Config:
    sources: dict[str, Path]
    redactions: list[re.Pattern[str]] = field(default_factory=list)

    @classmethod
    def build(cls, nt_root: Path, journal_dir: Path | None = None,
              export_dir: Path | None = None, redact_file: Path | None = None) -> "Config":
        sources = {"log": nt_root / "log", "trace": nt_root / "trace"}
        if journal_dir is not None:
            sources["journal"] = journal_dir
        if export_dir is not None:
            sources["export"] = export_dir
        redactions: list[re.Pattern[str]] = []
        if redact_file is not None:
            for raw in redact_file.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if line and not line.startswith("#"):
                    redactions.append(re.compile(line))
        return cls({name: path.resolve() for name, path in sources.items()}, redactions)

    def redact(self, text: str) -> str:
        for pattern in self.redactions:
            text = pattern.sub("[redacted]", text)
        return text


# --- file access ---------------------------------------------------------------

def _source_dir(config: Config, source: str) -> Path:
    if source not in config.sources:
        raise ToolError(f"unknown or unconfigured source {source!r}; configured: {sorted(config.sources)}")
    directory = config.sources[source]
    if not directory.is_dir():
        raise ToolError(f"source {source!r} directory does not exist: {directory}")
    return directory


def _files(config: Config, source: str, pattern: str = "*") -> list[Path]:
    """Regular files under the source matching the glob, newest first."""
    directory = _source_dir(config, source)
    found = []
    for path in directory.rglob("*"):
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if not resolved.is_relative_to(directory) or not resolved.is_file():
            continue
        relative = path.relative_to(directory).as_posix()
        if fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(path.name, pattern):
            found.append(path)
    found.sort(key=lambda p: (p.stat().st_mtime, p.name), reverse=True)
    return found


def _resolve_file(config: Config, source: str, name: str | None) -> Path:
    directory = _source_dir(config, source)
    if name is None:
        files = _files(config, source)
        if not files:
            raise ToolError(f"source {source!r} has no files")
        return files[0]
    candidate = (directory / name).resolve()
    if not candidate.is_relative_to(directory):
        raise ToolError(f"path escapes source {source!r}: {name}")
    if not candidate.is_file():
        raise ToolError(f"no such file in source {source!r}: {name}")
    return candidate


def _read_lines(path: Path) -> list[str]:
    # NinjaTrader keeps today's log open for writing; reading still works on Windows
    # because Python opens with shared read access.
    with open(path, "rb") as handle:
        data = handle.read()
    text = data.decode("utf-8-sig", errors="replace")
    return [line[:MAX_LINE_CHARS] for line in text.splitlines()]


def _relative(config: Config, source: str, path: Path) -> str:
    return path.resolve().relative_to(config.sources[source]).as_posix()


def _int(arguments: dict, key: str, default: int, low: int, high: int) -> int:
    value = arguments.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ToolError(f"{key} must be an integer")
    return max(low, min(high, value))


def _compile(pattern: str, regex: bool, ignore_case: bool) -> re.Pattern[str]:
    flags = re.IGNORECASE if ignore_case else 0
    try:
        return re.compile(pattern if regex else re.escape(pattern), flags)
    except re.error as exc:
        raise ToolError(f"bad regex: {exc}") from exc


# --- tools ---------------------------------------------------------------------

def tool_list_sources(config: Config, arguments: dict) -> str:
    rows = []
    for name, directory in sorted(config.sources.items()):
        state = "ok" if directory.is_dir() else "missing"
        rows.append(f"{name}\t{state}\t{directory}")
    return "\n".join(rows)


def tool_list_files(config: Config, arguments: dict) -> str:
    source = arguments["source"]
    limit = _int(arguments, "limit", 50, 1, 500)
    files = _files(config, source, arguments.get("glob", "*"))
    rows = []
    for path in files[:limit]:
        stat = path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(timespec="seconds")
        rows.append(f"{_relative(config, source, path)}\t{stat.st_size}\t{modified}")
    header = f"{len(files)} file(s) in {source}, newest first (name, bytes, modified UTC)"
    if len(files) > limit:
        header += f"; showing {limit}"
    return "\n".join([header, *rows])


def tool_tail(config: Config, arguments: dict) -> str:
    source = arguments["source"]
    path = _resolve_file(config, source, arguments.get("file"))
    count = _int(arguments, "lines", 200, 1, MAX_LINES)
    lines = _read_lines(path)
    tail = lines[-count:]
    header = f"{_relative(config, source, path)}: last {len(tail)} of {len(lines)} line(s)"
    return "\n".join([header, *tail])


def _search(config: Config, sources: list[str], matcher: re.Pattern[str], glob: str,
            max_files: int, max_matches: int, context: int) -> str:
    out: list[str] = []
    matches = 0
    truncated = False
    for source in sources:
        for path in _files(config, source, glob)[:max_files]:
            lines = _read_lines(path)
            before: deque[tuple[int, str]] = deque(maxlen=context)
            pending_after = 0
            last_printed = -1
            name = f"{source}/{_relative(config, source, path)}"
            for number, line in enumerate(lines, 1):
                if matcher.search(line):
                    if matches >= max_matches:
                        truncated = True
                        break
                    matches += 1
                    for ctx_number, ctx_line in before:
                        if ctx_number > last_printed:
                            out.append(f"{name}:{ctx_number}- {ctx_line}")
                    out.append(f"{name}:{number}: {line}")
                    last_printed = number
                    pending_after = context
                    before.clear()
                elif pending_after:
                    out.append(f"{name}:{number}- {line}")
                    last_printed = number
                    pending_after -= 1
                else:
                    before.append((number, line))
            if truncated:
                break
        if truncated:
            break
    summary = f"{matches} match(es)" + (f"; stopped at max_matches={max_matches}" if truncated else "")
    return "\n".join([summary, *out])


def tool_search(config: Config, arguments: dict) -> str:
    source = arguments["source"]
    matcher = _compile(arguments["pattern"], bool(arguments.get("regex", False)),
                       bool(arguments.get("ignore_case", True)))
    return _search(config, [source], matcher, arguments.get("glob", "*"),
                   _int(arguments, "max_files", 10, 1, 200),
                   _int(arguments, "max_matches", 200, 1, MAX_MATCHES),
                   _int(arguments, "context", 0, 0, 10))


def tool_errors(config: Config, arguments: dict) -> str:
    sources = [name for name in ("log", "trace") if config.sources[name].is_dir()]
    if not sources:
        raise ToolError("neither the log nor the trace directory exists under --nt-root")
    matcher = _compile(arguments.get("pattern", DEFAULT_ERROR_PATTERN), True, True)
    return _search(config, sources, matcher, "*",
                   _int(arguments, "max_files", 2, 1, 50),
                   _int(arguments, "max_matches", 200, 1, MAX_MATCHES),
                   _int(arguments, "context", 0, 0, 10))


_SOURCE = {"type": "string", "description": "log, trace, journal or export (see nt_list_sources)"}
_FILE = {"type": "string", "description": "Path relative to the source; default is the newest file"}
_GLOB = {"type": "string", "description": "Filename glob, e.g. 'log.*.txt'; default '*'"}

TOOLS: dict[str, tuple[Callable[[Config, dict], str], dict]] = {
    "nt_list_sources": (tool_list_sources, {
        "description": "List the configured read-only sources and whether each directory exists.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    }),
    "nt_list_files": (tool_list_files, {
        "description": "List files in a source, newest first, with size and modification time.",
        "inputSchema": {"type": "object", "properties": {
            "source": _SOURCE, "glob": _GLOB,
            "limit": {"type": "integer", "description": "Default 50, max 500"},
        }, "required": ["source"], "additionalProperties": False},
    }),
    "nt_tail": (tool_tail, {
        "description": "Last N lines of a file in a source (default: the newest file).",
        "inputSchema": {"type": "object", "properties": {
            "source": _SOURCE, "file": _FILE,
            "lines": {"type": "integer", "description": f"Default 200, max {MAX_LINES}"},
        }, "required": ["source"], "additionalProperties": False},
    }),
    "nt_search": (tool_search, {
        "description": "Search the newest files of a source for a substring or regex, like grep.",
        "inputSchema": {"type": "object", "properties": {
            "source": _SOURCE, "pattern": {"type": "string"}, "glob": _GLOB,
            "regex": {"type": "boolean", "description": "Default false (literal substring)"},
            "ignore_case": {"type": "boolean", "description": "Default true"},
            "max_files": {"type": "integer", "description": "Newest files to scan; default 10"},
            "max_matches": {"type": "integer", "description": f"Default 200, max {MAX_MATCHES}"},
            "context": {"type": "integer", "description": "Lines of context, 0-10; default 0"},
        }, "required": ["source", "pattern"], "additionalProperties": False},
    }),
    "nt_errors": (tool_errors, {
        "description": ("Errors, rejections, disconnects and exceptions in the newest NinjaTrader "
                        "log and trace files."),
        "inputSchema": {"type": "object", "properties": {
            "pattern": {"type": "string", "description": "Case-insensitive regex; default "
                        + DEFAULT_ERROR_PATTERN},
            "max_files": {"type": "integer", "description": "Newest files per source; default 2"},
            "max_matches": {"type": "integer"},
            "context": {"type": "integer"},
        }, "additionalProperties": False},
    }),
}


def call_tool(config: Config, name: str, arguments: dict) -> dict:
    if name not in TOOLS:
        raise KeyError(name)
    try:
        if not isinstance(arguments, dict):
            raise ToolError("arguments must be an object")
        text = TOOLS[name][0](config, arguments)
        is_error = False
    except KeyError as exc:
        text, is_error = f"missing argument: {exc.args[0]}", True
    except (ToolError, OSError, UnicodeError) as exc:
        text, is_error = str(exc), True
    text = config.redact(text)
    if len(text) > MAX_OUTPUT_CHARS:
        text = text[:MAX_OUTPUT_CHARS] + f"\n[truncated at {MAX_OUTPUT_CHARS} characters]"
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


# --- JSON-RPC over stdio -----------------------------------------------------------

def handle(config: Config, message: Any) -> dict | None:
    """One JSON-RPC message in, the response out (None for notifications)."""
    if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or "method" not in message:
        return {"jsonrpc": "2.0", "id": message.get("id") if isinstance(message, dict) else None,
                "error": {"code": -32600, "message": "invalid request"}}
    method = message["method"]
    if "id" not in message:
        return None
    request_id = message["id"]
    params = message.get("params") or {}

    def result(value: dict) -> dict:
        return {"jsonrpc": "2.0", "id": request_id, "result": value}

    def error(code: int, text: str) -> dict:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": text}}

    if method == "initialize":
        requested = params.get("protocolVersion")
        version = requested if requested in SUPPORTED_PROTOCOLS else SUPPORTED_PROTOCOLS[0]
        return result({
            "protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            "instructions": ("Read-only access to NinjaTrader 8 log/trace files and the strategy "
                             "journals and exports. It cannot place, change or cancel orders. "
                             "Output may contain account data: never write it into the repository."),
        })
    if method == "ping":
        return result({})
    if method == "tools/list":
        return result({"tools": [{"name": name, **spec} for name, (_, spec) in TOOLS.items()]})
    if method == "tools/call":
        try:
            return result(call_tool(config, params.get("name"), params.get("arguments") or {}))
        except KeyError:
            return error(-32602, f"unknown tool: {params.get('name')!r}")
    return error(-32601, f"method not found: {method}")


def serve(config: Config, stdin=None, stdout=None) -> None:
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    for line in stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
        else:
            response = handle(config, message)
        if response is not None:
            stdout.write(json.dumps(response) + "\n")
            stdout.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only NinjaTrader 8 MCP server (stdio).")
    parser.add_argument("--nt-root", type=Path, default=Path.home() / "Documents" / "NinjaTrader 8",
                        help="NinjaTrader user data folder (default ~/Documents/NinjaTrader 8)")
    parser.add_argument("--journal-dir", type=Path, help="strategy journal directory (private custody)")
    parser.add_argument("--export-dir", type=Path, help="export directory (private custody)")
    parser.add_argument("--redact-file", type=Path, help="regexes to mask in all output, one per line")
    options = parser.parse_args(argv)
    config = Config.build(options.nt_root, options.journal_dir, options.export_dir, options.redact_file)
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    serve(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
