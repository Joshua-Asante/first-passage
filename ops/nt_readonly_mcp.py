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
from typing import Any, Callable, Iterator

SERVER_NAME = "nt-readonly"
SERVER_VERSION = "0.1.0"
SUPPORTED_PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")

MAX_LINES = 2000
MAX_MATCHES = 1000
MAX_OUTPUT_CHARS = 200_000
MAX_LINE_CHARS = 2000
# Bytes of one line kept and masked before the MAX_LINE_CHARS cut; the rest of a
# longer line is read past and dropped, so a single huge line cannot exhaust memory.
MAX_LINE_BYTES = 64 * 1024
READ_BLOCK = 64 * 1024
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
    if name is not None and "\x00" in name:
        raise ToolError("file name contains a NUL character")
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


# NinjaTrader keeps today's log open for writing; reading still works on Windows
# because Python opens with shared read access. Files are read in bounded blocks, so
# memory stays bounded whatever the file size.

def _split_piece(raw: bytes, first: bool, last: bool, redact: Callable[[str], str]) -> list[str]:
    """Lines of one piece between newlines: decoded, masked whole, then cut.

    Gives the same lines ``str.splitlines`` gives for the whole file (CRLF, lone CR and
    the other Unicode breaks included). ``last`` marks a final piece with no newline.
    """
    text = raw.decode("utf-8-sig" if first else "utf-8", errors="replace")
    pieces = text.splitlines() if last else (text + "\n").splitlines()
    return [redact(line)[:MAX_LINE_CHARS] for line in pieces]


def _iter_lines(path: Path, redact: Callable[[str], str]) -> Iterator[str]:
    """Stream a file's lines, each masked before it is cut to MAX_LINE_CHARS."""
    with open(path, "rb") as handle:
        kept = bytearray()
        first = True
        while block := handle.read(READ_BLOCK):
            start = 0
            while True:
                newline = block.find(b"\n", start)
                stop = len(block) if newline < 0 else newline
                room = MAX_LINE_BYTES - len(kept)
                if room > 0:
                    kept += block[start:min(stop, start + room)]
                if newline < 0:
                    break
                yield from _split_piece(bytes(kept), first, False, redact)
                kept.clear()
                first = False
                start = newline + 1
        if kept:
            yield from _split_piece(bytes(kept), first, True, redact)


def _tail_lines(path: Path, count: int, redact: Callable[[str], str]) -> list[str]:
    """The last ``count`` lines, found by reading backwards from the end in blocks."""
    with open(path, "rb") as handle:
        end = handle.seek(0, 2)
        if end == 0:
            return []
        handle.seek(end - 1)
        scan_end = end - 1 if handle.read(1) == b"\n" else end
        # The last `count` newline positions before scan_end mark where the last
        # `count` lines start. Each block is dropped once it has been scanned.
        newlines: list[int] = []
        position = scan_end
        while position > 0 and len(newlines) < count:
            size = min(READ_BLOCK, position)
            position -= size
            handle.seek(position)
            block = handle.read(size)
            index = len(block)
            while len(newlines) < count:
                index = block.rfind(b"\n", 0, index)
                if index < 0:
                    break
                newlines.append(position + index)
        starts = sorted(n + 1 for n in newlines)
        if len(newlines) < count:
            starts.insert(0, 0)
        ends = [s - 1 for s in starts[1:]] + [scan_end]
        lines: list[str] = []
        for start, stop in zip(starts, ends):
            handle.seek(start)
            raw = handle.read(min(stop - start, MAX_LINE_BYTES))
            lines.extend(_split_piece(raw, start == 0, stop == end, redact))
    return lines[-count:]


def _relative(config: Config, source: str, path: Path) -> str:
    return path.resolve().relative_to(config.sources[source]).as_posix()


_REQUIRED: Any = object()


def _str(arguments: dict, key: str, default: Any = _REQUIRED) -> Any:
    """A string argument; JSON null or absence gives the default (if there is one)."""
    value = arguments.get(key)
    if value is None:
        if default is _REQUIRED:
            raise ToolError(f"missing argument: {key}")
        return default
    if not isinstance(value, str):
        raise ToolError(f"{key} must be a string")
    return value


def _bool(arguments: dict, key: str, default: bool) -> bool:
    value = arguments.get(key, default)
    if not isinstance(value, bool):
        raise ToolError(f"{key} must be a boolean")
    return value


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
    source = _str(arguments, "source")
    limit = _int(arguments, "limit", 50, 1, 500)
    files = _files(config, source, _str(arguments, "glob", "*"))
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
    source = _str(arguments, "source")
    path = _resolve_file(config, source, _str(arguments, "file", None))
    count = _int(arguments, "lines", 200, 1, MAX_LINES)
    tail = _tail_lines(path, count, config.redact)
    header = f"{_relative(config, source, path)}: last {len(tail)} line(s)"
    return "\n".join([header, *tail])


def _search(config: Config, sources: list[str], matcher: re.Pattern[str], glob: str,
            max_files: int, max_matches: int, context: int) -> str:
    out: list[str] = []
    matches = 0
    truncated = False
    for source in sources:
        for path in _files(config, source, glob)[:max_files]:
            lines = _iter_lines(path, config.redact)
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
    source = _str(arguments, "source")
    matcher = _compile(_str(arguments, "pattern"), _bool(arguments, "regex", False),
                       _bool(arguments, "ignore_case", True))
    return _search(config, [source], matcher, _str(arguments, "glob", "*"),
                   _int(arguments, "max_files", 10, 1, 200),
                   _int(arguments, "max_matches", 200, 1, MAX_MATCHES),
                   _int(arguments, "context", 0, 0, 10))


def tool_errors(config: Config, arguments: dict) -> str:
    sources = [name for name in ("log", "trace") if config.sources[name].is_dir()]
    if not sources:
        raise ToolError("neither the log nor the trace directory exists under --nt-root")
    matcher = _compile(_str(arguments, "pattern", DEFAULT_ERROR_PATTERN), True, True)
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
    except (ToolError, OSError, UnicodeError) as exc:
        text, is_error = str(exc), True
    text = config.redact(text)  # again, for error text that quotes arguments or paths
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
    params = message.get("params")
    if params is None:
        params = {}

    def result(value: dict) -> dict:
        return {"jsonrpc": "2.0", "id": request_id, "result": value}

    def error(code: int, text: str) -> dict:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": text}}

    if not isinstance(params, dict):
        return error(-32602, "params must be an object")

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
        name = params.get("name")
        if not isinstance(name, str) or name not in TOOLS:
            return error(-32602, f"unknown tool: {name!r}")
        arguments = params.get("arguments")
        return result(call_tool(config, name, {} if arguments is None else arguments))
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
