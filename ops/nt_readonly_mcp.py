"""Read-only NinjaTrader 8 MCP server (stdio, standard library only).

Lets an agent read the text files NinjaTrader and the strategy instances leave on
disk, instead of screenshotting the Log tab or the Output window. It runs outside
NinjaTrader and never talks to it:

* no sockets, HTTP, ATI, AddOn or subprocess; it only opens files for reading;
* every path is confined to a configured source directory; the walk lists entries
  with lstat, and symlinks, junctions and
  other name-surrogate reparse points are never followed;
* it places, changes and cancels nothing, so AGENTS.md money controls 1 and 3 and
  spec check B1 (no network calls, ATI, add-ons) are untouched.

The files can carry account data and strategy parameters, and AGENTS.md lets agents
read private logs only through tools that return approved fields. So the server
emits only the fields named in ``--fields-file``, a private allow-list Joshua signs
off, kept outside the repository; anything not on it is dropped, never shown.
``--redact-file`` (one regex per line) also masks every emitted value, as a backup.
Searches, globs and file names match on the masked text only, so match counts
cannot reveal a masked value. The server refuses to start without ``--fields-file``
unless it gets ``--allow-unredacted``, which serves whole lines unmasked: for
debugging that Joshua directs, and its output is never persisted.

Allow-list (``--fields-file``): UTF-8 text, one rule per line, ``#`` starts a
comment line. A rule is ``<source> <field>``:

    log      timestamp | level | category | kv:<Key>
    trace    timestamp | kv:<Key>
    journal  json:<dotted.path>
    refusal  json:<dotted.path>
    export   (no field can be approved)

Log lines are ``timestamp|level|category|text``; trace lines are a timestamp, then
text. ``kv:<Key>`` takes ``Key='value'`` or ``key=value`` pairs from that text.
Journal lines are JSON records; a refusal file is one JSON object. ``json:a.b``
walks objects, decoding a string that holds JSON on the way (``json:body.code``),
and emits scalars only. A malformed file, an unknown source or field syntax, or a
file with no rules stops the server from starting. Each line (record) comes back as
one compact JSON object of approved field -> value; a line with no approved field
is left out and counted. Order IDs and names are not approved fields.

Callers search with literal substrings only: Python's ``re`` has no time limit, so a
caller regex could stall the server. ``nt_errors`` uses one fixed built-in pattern.

Sources (each optional except ``log`` and ``trace``, which derive from ``--nt-root``):

    log      <nt-root>/log      NinjaTrader log files
    trace    <nt-root>/trace    NinjaTrader trace files
    journal  --journal-dir      the strategy instances' own journals (spec B2)
    refusal  --refusal-dir      the instances' refusal files
    export   --export-dir       exports kept in private custody (spec B11)

The files are read as UTF-8 text; UTF-16/32 and binary files are refused.

Run::

    python ops/nt_readonly_mcp.py --nt-root "C:\\Users\\<you>\\Documents\\NinjaTrader 8" --fields-file <private file> --redact-file <private file>
"""
from __future__ import annotations

import argparse
import codecs
import fnmatch
import json
import math
import re
import stat
import sys
import time
import unicodedata
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

SERVER_NAME = "nt-readonly"
SERVER_VERSION = "0.3.0"
SUPPORTED_PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")

MAX_LINES = 2000
MAX_MATCHES = 1000
MAX_OUTPUT_CHARS = 200_000
MAX_LINE_CHARS = 2000
MAX_ARG_CHARS = 1024
MAX_REQUEST_BYTES = 1024 * 1024
MAX_WALK_ENTRIES = 50_000
# Per-call read budget: a call stops once it has read this many bytes or run this long.
MAX_CALL_BYTES = 256 * 1024 * 1024
MAX_CALL_SECONDS = 20.0
# A line longer than this many bytes is never shown, even in part: a mask pattern
# may depend on the part that bounded memory cannot hold, so it is replaced whole
# by OMITTED_LINE (fail closed). Shorter lines are masked whole, then cut.
MAX_LINE_BYTES = 64 * 1024
READ_BLOCK = 64 * 1024
# A flat alternation of literals (one optional space): linear-time on any line.
DEFAULT_ERROR_PATTERN = r"error|exception|reject|disconnect|connection ?lost|lost connection|failed|halt"
ERROR_MATCHER = re.compile(DEFAULT_ERROR_PATTERN, re.IGNORECASE)
_WIDE_BOMS = (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE, codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)
# Reparse tags with this bit name another path (symlinks, junctions, mount points).
_NAME_SURROGATE = 0x20000000


class _Omitted(str):
    """Placeholder text for a line that is never shown; a search never matches it."""


OMITTED_LINE = _Omitted(f"[line over {MAX_LINE_BYTES} bytes omitted]")
OMITTED_NUL_LINE = _Omitted("[line with NUL bytes omitted]")


class ToolError(Exception):
    """A request the server refuses; reported to the client as a tool error."""


class FileRefused(ToolError):
    """One file the server will not read (not UTF-8 text)."""


class BudgetExceeded(ToolError):
    """The call has used its read budget."""


class Budget:
    """Bytes and wall time one tool call may spend reading files."""

    def __init__(self) -> None:
        self.left = MAX_CALL_BYTES
        self.deadline = time.monotonic() + MAX_CALL_SECONDS

    def charge(self, size: int) -> None:
        self.left -= size
        if self.left < 0 or time.monotonic() > self.deadline:
            raise BudgetExceeded(f"read budget reached ({MAX_CALL_BYTES} bytes or "
                                 f"{MAX_CALL_SECONDS:g} s per call)")


def _rule_lines(path: Path) -> Iterator[tuple[int, str]]:
    """Numbered rule lines of a private config file: comments and blanks skipped."""
    # utf-8-sig: a BOM left by an editor must not become part of the first rule.
    text = path.read_text(encoding="utf-8-sig")
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if any(unicodedata.category(ch) == "Cf" for ch in line):
            raise ValueError(f"line {number} contains an invisible format character")
        yield number, line


# --- approved fields -------------------------------------------------------------

FIELD_SOURCES = ("log", "trace", "journal", "refusal", "export")
_FIXED_FIELDS = {"log": ("timestamp", "level", "category"), "trace": ("timestamp",)}
_KV_SOURCES = ("log", "trace")
_JSON_SOURCES = ("journal", "refusal")
_KV_RULE = re.compile(r"kv:([A-Za-z_][A-Za-z0-9_]*)")
_JSON_RULE = re.compile(r"json:([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)")
# A fixed field whose value has the wrong shape is dropped, so a line that only
# looks like a log line cannot carry free text out through a fixed field.
_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.:,]\d{1,7})?")
_CODE = re.compile(r"[A-Za-z0-9_]{1,32}")
# One pass left to right: a quoted value is consumed whole, so text inside it is
# never read as another pair.
_PAIR = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_]*)=(?:'([^']*)'|([^\s']*))")
_MISSING: Any = object()


def _json_object(text: str) -> dict | None:
    try:
        value = json.loads(text, parse_constant=_no_constant, parse_float=_finite_float)
    except (ValueError, RecursionError):
        return None
    return value if isinstance(value, dict) else None


def _json_path(record: dict, path: str) -> Any:
    """The scalar at a dotted path; a string holding a JSON object is decoded on the way."""
    value: Any = record
    for key in path.split("."):
        if isinstance(value, str):
            value = _json_object(value)
        if not isinstance(value, dict) or key not in value:
            return _MISSING
        value = value[key]
    return _MISSING if isinstance(value, (dict, list)) else value


@dataclass(frozen=True)
class Fields:
    """The approved-field allow-list: source -> rules, in file order."""

    rules: dict[str, tuple[str, ...]]

    @classmethod
    def load(cls, path: Path) -> "Fields":
        rules: dict[str, list[str]] = {}
        for number, line in _rule_lines(path):
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"line {number}: expected '<source> <field>'")
            source, name = parts
            if source not in FIELD_SOURCES:
                raise ValueError(f"line {number}: unknown source {source!r}; "
                                 f"expected one of {', '.join(FIELD_SOURCES)}")
            if not (name in _FIXED_FIELDS.get(source, ())
                    or (source in _KV_SOURCES and _KV_RULE.fullmatch(name))
                    or (source in _JSON_SOURCES and _JSON_RULE.fullmatch(name))):
                raise ValueError(f"line {number}: {name!r} is not a field {source} can approve")
            if name not in rules.setdefault(source, []):
                rules[source].append(name)
        if not rules:
            raise ValueError("no rules")
        return cls({source: tuple(names) for source, names in rules.items()})

    def extract(self, source: str, text: str) -> dict[str, Any]:
        """The approved fields of one line (record), unmasked; nothing else is read out."""
        names = self.rules.get(source)
        if not names:
            return {}
        fixed: dict[str, str] = {}
        free: str | None = None
        record: dict | None = None
        if source == "log":
            parts = text.split("|", 3)
            if len(parts) == 4:
                stamp, level, category, free = (*(part.strip() for part in parts[:3]), parts[3])
                if _TIMESTAMP.fullmatch(stamp):
                    fixed["timestamp"] = stamp
                if _CODE.fullmatch(level):
                    fixed["level"] = level
                if _CODE.fullmatch(category):
                    fixed["category"] = category
        elif source == "trace":
            stamp = _TIMESTAMP.match(text)
            if stamp and (stamp.end() == len(text) or text[stamp.end()].isspace()):
                fixed["timestamp"] = stamp.group()
                free = text[stamp.end():]
        elif source in _JSON_SOURCES:
            record = _json_object(text)
        pairs: dict[str, list[str]] = {}
        if free is not None:
            for match in _PAIR.finditer(free):
                value = match.group(2) if match.group(2) is not None else match.group(3)
                pairs.setdefault(match.group(1), []).append(value)
        out: dict[str, Any] = {}
        for name in names:
            if name in fixed:
                out[name] = fixed[name]
            elif name.startswith("kv:") and name[3:] in pairs:
                values = pairs[name[3:]]
                out[name] = values[0] if len(values) == 1 else values
            elif name.startswith("json:") and record is not None:
                value = _json_path(record, name[5:])
                if value is not _MISSING:
                    out[name] = value
        return out


@dataclass
class Config:
    sources: dict[str, Path]
    redactions: list[re.Pattern[str]] = field(default_factory=list)
    # None serves whole lines; main() allows that only with --allow-unredacted.
    fields: Fields | None = None

    @classmethod
    def build(cls, nt_root: Path, journal_dir: Path | None = None,
              export_dir: Path | None = None, redact_file: Path | None = None,
              fields_file: Path | None = None, refusal_dir: Path | None = None) -> "Config":
        sources = {"log": nt_root / "log", "trace": nt_root / "trace"}
        if journal_dir is not None:
            sources["journal"] = journal_dir
        if refusal_dir is not None:
            sources["refusal"] = refusal_dir
        if export_dir is not None:
            sources["export"] = export_dir
        redactions: list[re.Pattern[str]] = []
        if redact_file is not None:
            redactions = [re.compile(line) for _, line in _rule_lines(redact_file)]
        fields = Fields.load(fields_file) if fields_file is not None else None
        return cls({name: path.resolve() for name, path in sources.items()}, redactions, fields)

    def redact(self, text: str) -> str:
        for pattern in self.redactions:
            text = pattern.sub("[redacted]", text)
        return text


# --- file access ---------------------------------------------------------------

@dataclass
class Entry:
    path: Path
    name: str  # masked path relative to the source: the only name a caller sees or uses
    mtime: float
    size: int


def _source_dir(config: Config, source: str) -> Path:
    if source not in config.sources:
        raise ToolError(f"unknown or unconfigured source {source!r}; configured: {sorted(config.sources)}")
    directory = config.sources[source]
    if not directory.is_dir():
        raise ToolError(f"source {source!r} directory does not exist: {directory}")
    return directory


def _is_link(info: Any) -> bool:
    """A symlink, junction or other reparse point that names another path."""
    if stat.S_ISLNK(info.st_mode):
        return True
    # Symlink (0xA000000C) and junction (0xA0000003) tags both carry this bit;
    # st_reparse_tag exists only on Windows.
    return bool(getattr(info, "st_reparse_tag", 0) & _NAME_SURROGATE)


def _reason(exc: OSError) -> str:
    """Why a file was skipped, without its path (strerror carries none)."""
    return f"{type(exc).__name__}: {exc.strerror or 'unreadable'}"


def _walk(config: Config, source: str, notes: list[str]) -> list[Entry]:
    """Regular files under the source, never reached through a link; failures noted."""
    directory = _source_dir(config, source)
    entries: list[Entry] = []
    seen: set[Path] = set()
    visited = 0
    pending = [directory]
    while pending:
        try:
            children = sorted(pending.pop().iterdir())
        except OSError:
            continue
        subdirs = []
        for path in children:
            visited += 1
            if visited > MAX_WALK_ENTRIES:
                notes.append(f"listing stopped after {MAX_WALK_ENTRIES} entries in {source}")
                return entries
            shown = config.redact(path.relative_to(directory).as_posix())
            try:
                info = path.lstat()  # never follows a link
                if _is_link(info):
                    continue
                if stat.S_ISDIR(info.st_mode):
                    subdirs.append(path)
                    continue
                if not stat.S_ISREG(info.st_mode):
                    continue
                resolved = path.resolve(strict=True)
            except OSError as exc:
                notes.append(f"skipped {source}/{shown}: {_reason(exc)}")
                continue
            if not resolved.is_relative_to(directory) or resolved in seen:
                continue
            seen.add(resolved)
            entries.append(Entry(resolved, shown, info.st_mtime, info.st_size))
        pending.extend(reversed(subdirs))
    return entries


def _files(config: Config, source: str, pattern: str, notes: list[str]) -> list[Entry]:
    """Files whose masked name matches the glob, newest first."""
    found = [entry for entry in _walk(config, source, notes)
             if fnmatch.fnmatch(entry.name, pattern)
             or fnmatch.fnmatch(entry.name.rsplit("/", 1)[-1], pattern)]
    found.sort(key=lambda entry: (entry.mtime, entry.name), reverse=True)
    return found


def _resolve_file(config: Config, source: str, name: str | None, notes: list[str]) -> Entry:
    """The file the caller names, looked up by masked name so a masked value can't be probed."""
    directory = _source_dir(config, source)
    if name is None:
        files = _files(config, source, "*", notes)
        if not files:
            raise ToolError(f"source {source!r} has no files")
        return files[0]
    if "\x00" in name:
        raise ToolError("file name contains a NUL character")
    if not (directory / name).resolve().is_relative_to(directory):
        raise ToolError(f"path escapes source {source!r}: {name}")
    wanted = "/".join(name.split("\\")).removeprefix("./")
    matches = [entry for entry in _walk(config, source, notes) if entry.name == wanted]
    if not matches:
        raise ToolError(f"no such file in source {source!r}: {name}")
    if len(matches) > 1:
        raise ToolError(f"{len(matches)} files in source {source!r} show as {name}")
    return matches[0]


# NinjaTrader keeps today's log open for writing; reading still works on Windows
# because Python opens with shared read access. Files are read in bounded blocks, so
# memory stays bounded whatever the file size, and only up to the size the file had
# when it was opened, so a writer that keeps appending cannot make a read endless.

def _check_text(head: bytes) -> None:
    """Refuse UTF-16/32 and binary files: read as UTF-8, NULs would split every mask."""
    if head.startswith(_WIDE_BOMS) or b"\x00" in head:
        raise FileRefused("not UTF-8 text (UTF-16/32 byte-order mark or NUL bytes); refused")


def _blocks(handle: Any, budget: Budget) -> Iterator[bytes]:
    """The file's blocks up to its size at open; the first block is checked as text."""
    remaining = handle.seek(0, 2)
    handle.seek(0)
    first = True
    while remaining > 0:
        block = handle.read(min(READ_BLOCK, remaining))
        if not block:
            return
        remaining -= len(block)
        budget.charge(len(block))
        if first:
            _check_text(block)
            first = False
        yield block


def _split_piece(raw: bytes, first: bool, last: bool) -> list[str]:
    """Raw lines of one piece between newlines.

    Gives the same lines ``str.splitlines`` gives for the whole file (CRLF, lone CR and
    the other Unicode breaks included). ``last`` marks a final piece with no newline.
    A piece holding a NUL byte comes back as OMITTED_NUL_LINE.
    """
    if b"\x00" in raw:
        return [OMITTED_NUL_LINE]
    text = raw.decode("utf-8-sig" if first else "utf-8", errors="replace")
    return text.splitlines() if last else (text + "\n").splitlines()


def _mask_value(value: Any, redact: Callable[[str], str]) -> Any:
    """One emitted field value, masked; a scalar the mask touches becomes masked text."""
    if isinstance(value, list):
        return [_mask_value(item, redact) for item in value]
    if isinstance(value, str):
        return redact(value)[:MAX_LINE_CHARS]
    text = json.dumps(value)
    masked = redact(text)
    return value if masked == text else masked[:MAX_LINE_CHARS]


def _match_texts(value: Any) -> list[str]:
    if isinstance(value, list):
        return [text for item in value for text in _match_texts(item)]
    return [value if isinstance(value, str) else json.dumps(value)]


def _present(config: Config, source: str, line: str) -> tuple[str, list[str]] | None:
    """What may leave the server for one raw line (record), and the texts a search
    may match: the same masked text that is output. None: no approved field."""
    if isinstance(line, _Omitted):
        return line, []
    if config.fields is None:
        shown = config.redact(line)[:MAX_LINE_CHARS]
        return shown, [shown]
    picked = {name: _mask_value(value, config.redact)
              for name, value in config.fields.extract(source, line).items()}
    if not picked:
        return None
    texts = [text for value in picked.values() for text in _match_texts(value)]
    return json.dumps(picked, ensure_ascii=False, separators=(",", ":")), texts


def _whole_file(path: Path, budget: Budget) -> list[str]:
    """A file read as one record (a refusal file); over MAX_LINE_BYTES it is omitted."""
    kept = bytearray()
    with open(path, "rb") as handle:
        for block in _blocks(handle, budget):
            if len(kept) + len(block) > MAX_LINE_BYTES:
                return [OMITTED_LINE]
            kept += block
    if not kept:
        return []
    if b"\x00" in kept:
        return [OMITTED_NUL_LINE]
    return [bytes(kept).decode("utf-8-sig", errors="replace")]


def _records(config: Config, source: str, path: Path, budget: Budget) -> Iterator[str]:
    """A file's raw units: lines, or the whole file for a refusal in approved-field mode."""
    if config.fields is not None and source == "refusal":
        yield from _whole_file(path, budget)
    else:
        yield from _iter_lines(path, budget)


def _iter_lines(path: Path, budget: Budget) -> Iterator[str]:
    """Stream a file's raw lines; a line over MAX_LINE_BYTES comes as OMITTED_LINE.

    Callers pass every line through ``_present`` before matching or output.
    """
    with open(path, "rb") as handle:
        kept = bytearray()
        oversized = False
        first = True
        for block in _blocks(handle, budget):
            start = 0
            while True:
                newline = block.find(b"\n", start)
                stop = len(block) if newline < 0 else newline
                room = MAX_LINE_BYTES - len(kept)
                if stop - start > room:
                    oversized = True
                elif not oversized:
                    kept += block[start:stop]
                if newline < 0:
                    break
                if oversized:
                    yield OMITTED_LINE
                else:
                    yield from _split_piece(bytes(kept), first, False)
                kept.clear()
                oversized = False
                first = False
                start = newline + 1
        if oversized:
            yield OMITTED_LINE
        elif kept:
            yield from _split_piece(bytes(kept), first, True)


def _tail_lines(path: Path, count: int, budget: Budget) -> list[str]:
    """The last ``count`` raw lines, found by reading backwards from the end in blocks."""
    with open(path, "rb") as handle:
        end = handle.seek(0, 2)
        if end == 0:
            return []
        handle.seek(0)
        head = handle.read(min(READ_BLOCK, end))
        budget.charge(len(head))
        _check_text(head)
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
            budget.charge(len(block))
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
            if stop - start > MAX_LINE_BYTES:
                lines.append(OMITTED_LINE)
                continue
            handle.seek(start)
            piece = handle.read(stop - start)
            budget.charge(len(piece))
            lines.extend(_split_piece(piece, start == 0, stop == end))
    return lines[-count:]


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
    if len(value) > MAX_ARG_CHARS:
        raise ToolError(f"{key} is longer than {MAX_ARG_CHARS} characters")
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


def _literal(pattern: str, ignore_case: bool) -> re.Pattern[str]:
    """A matcher for the literal substring; escaped, so it cannot backtrack."""
    return re.compile(re.escape(pattern), re.IGNORECASE if ignore_case else 0)


def _with_notes(lines: list[str], notes: list[str]) -> str:
    return "\n".join([*lines, *(f"note: {note}" for note in notes)])


# --- tools ---------------------------------------------------------------------
# Tool output is not masked again as a whole (that could join lines): every line,
# name and path is masked where it is produced.

def tool_list_sources(config: Config, arguments: dict) -> str:
    rows = []
    for name, directory in sorted(config.sources.items()):
        state = "ok" if directory.is_dir() else "missing"
        rows.append(config.redact(f"{name}\t{state}\t{directory}"))
    return "\n".join(rows)


def tool_list_files(config: Config, arguments: dict) -> str:
    source = _str(arguments, "source")
    limit = _int(arguments, "limit", 50, 1, 500)
    notes: list[str] = []
    files = _files(config, source, _str(arguments, "glob", "*"), notes)
    rows = []
    for entry in files[:limit]:
        modified = datetime.fromtimestamp(entry.mtime, timezone.utc).isoformat(timespec="seconds")
        rows.append(f"{entry.name}\t{entry.size}\t{modified}")
    header = f"{len(files)} file(s) in {source}, newest first (name, bytes, modified UTC)"
    if len(files) > limit:
        header += f"; showing {limit}"
    return _with_notes([header, *rows], notes)


def tool_tail(config: Config, arguments: dict) -> str:
    source = _str(arguments, "source")
    notes: list[str] = []
    entry = _resolve_file(config, source, _str(arguments, "file", None), notes)
    count = _int(arguments, "lines", 200, 1, MAX_LINES)
    if config.fields is not None and source == "refusal":
        raw, unit = _whole_file(entry.path, Budget()), "record"
    else:
        raw, unit = _tail_lines(entry.path, count, Budget()), "line"
    shown = [_present(config, source, line) for line in raw]
    tail = [item[0] for item in shown if item is not None]
    header = f"{entry.name}: last {len(raw)} {unit}(s)"
    if len(tail) < len(raw):
        header += f"; {len(raw) - len(tail)} without an approved field omitted"
    return "\n".join([header, *tail])


def _search(config: Config, sources: list[str], matcher: re.Pattern[str], glob: str,
            max_files: int, max_matches: int, context: int) -> str:
    out: list[str] = []
    notes: list[str] = []
    matches = 0
    unapproved = 0
    stopped = ""
    budget = Budget()
    for source in sources:
        for entry in _files(config, source, glob, notes)[:max_files]:
            before: deque[tuple[int, str]] = deque(maxlen=context)
            pending_after = 0
            last_printed = -1
            name = f"{source}/{entry.name}"
            try:
                # Match on the masked approved values, the same text that is output,
                # so a match count cannot reveal what the mask or the allow-list hides.
                for number, raw in enumerate(_records(config, source, entry.path, budget), 1):
                    shown = _present(config, source, raw)
                    if shown is None:
                        unapproved += 1
                        continue
                    line, texts = shown
                    if any(matcher.search(text) for text in texts):
                        if matches >= max_matches:
                            stopped = f"stopped at max_matches={max_matches}"
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
            except BudgetExceeded as exc:
                stopped = f"stopped: {exc}"
            except FileRefused as exc:
                notes.append(f"skipped {name}: {exc}")
            except OSError as exc:
                notes.append(f"skipped {name}: {_reason(exc)}")
            if stopped:
                break
        if stopped:
            break
    summary = f"{matches} match(es)" + (f"; {stopped}" if stopped else "")
    if unapproved:
        summary += f"; {unapproved} line(s) without an approved field skipped"
    return _with_notes([summary, *out], notes)


def tool_search(config: Config, arguments: dict) -> str:
    source = _str(arguments, "source")
    matcher = _literal(_str(arguments, "pattern"), _bool(arguments, "ignore_case", True))
    return _search(config, [source], matcher, _str(arguments, "glob", "*"),
                   _int(arguments, "max_files", 10, 1, 200),
                   _int(arguments, "max_matches", 200, 1, MAX_MATCHES),
                   _int(arguments, "context", 0, 0, 10))


def tool_errors(config: Config, arguments: dict) -> str:
    sources = [name for name in ("log", "trace") if config.sources[name].is_dir()]
    if not sources:
        raise ToolError("neither the log nor the trace directory exists under --nt-root")
    return _search(config, sources, ERROR_MATCHER, "*",
                   _int(arguments, "max_files", 2, 1, 50),
                   _int(arguments, "max_matches", 200, 1, MAX_MATCHES),
                   _int(arguments, "context", 0, 0, 10))


_SOURCE = {"type": "string",
           "description": "log, trace, journal, refusal or export (see nt_list_sources)"}
_FILE = {"type": "string", "description": "Path relative to the source, as nt_list_files shows it; "
                                          "default is the newest file"}
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
        "description": ("Search the newest files of a source for a literal substring, like "
                        "grep -F. Matches the masked text."),
        "inputSchema": {"type": "object", "properties": {
            "source": _SOURCE,
            "pattern": {"type": "string", "description": "Literal substring (not a regex)"},
            "glob": _GLOB,
            "ignore_case": {"type": "boolean", "description": "Default true"},
            "max_files": {"type": "integer", "description": "Newest files to scan; default 10"},
            "max_matches": {"type": "integer", "description": f"Default 200, max {MAX_MATCHES}"},
            "context": {"type": "integer", "description": "Lines of context, 0-10; default 0"},
        }, "required": ["source", "pattern"], "additionalProperties": False},
    }),
    "nt_errors": (tool_errors, {
        "description": ("Errors, rejections, disconnects and exceptions in the newest NinjaTrader "
                        "log and trace files, by the built-in pattern " + DEFAULT_ERROR_PATTERN),
        "inputSchema": {"type": "object", "properties": {
            "max_files": {"type": "integer", "description": "Newest files per source; default 2"},
            "max_matches": {"type": "integer"},
            "context": {"type": "integer"},
        }, "additionalProperties": False},
    }),
}

# Clearer refusals for arguments the tools once took.
_REMOVED_ARGUMENTS = {
    ("nt_search", "regex"): "regex is not supported: nt_search patterns are literal substrings",
    ("nt_errors", "pattern"): ("nt_errors takes no pattern: it uses its built-in error pattern; "
                               "use nt_search for a literal search"),
}


def _check_keys(name: str, arguments: dict) -> None:
    allowed = TOOLS[name][1]["inputSchema"]["properties"]
    unknown = sorted(key for key in arguments if key not in allowed)
    for key in unknown:
        if (name, key) in _REMOVED_ARGUMENTS:
            raise ToolError(_REMOVED_ARGUMENTS[(name, key)])
    if unknown:
        listed = ", ".join(repr(key[:60]) for key in unknown[:10])
        raise ToolError(f"unknown argument(s) for {name}: {listed}")


def call_tool(config: Config, name: str, arguments: dict) -> dict:
    if name not in TOOLS:
        raise KeyError(name)
    try:
        if not isinstance(arguments, dict):
            raise ToolError("arguments must be an object")
        _check_keys(name, arguments)
        text = TOOLS[name][0](config, arguments)
        is_error = False
    except (ToolError, OSError, UnicodeError) as exc:
        # Error text can quote arguments or paths, so it is masked as a whole.
        text, is_error = config.redact(str(exc)), True
    if len(text) > MAX_OUTPUT_CHARS:
        text = text[:MAX_OUTPUT_CHARS] + f"\n[truncated at {MAX_OUTPUT_CHARS} characters]"
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


# --- JSON-RPC over stdio -----------------------------------------------------------

def _valid_id(value: Any) -> bool:
    return value is None or isinstance(value, str) or (
        isinstance(value, (int, float)) and not isinstance(value, bool))


def handle(config: Config, message: Any) -> dict | None:
    """One JSON-RPC message in, the response out (None for notifications)."""
    if (not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or "method" not in message
            or not _valid_id(message.get("id"))):
        request_id = message.get("id") if isinstance(message, dict) else None
        return {"jsonrpc": "2.0", "id": request_id if _valid_id(request_id) else None,
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


def _no_constant(name: str) -> Any:
    raise ValueError(f"JSON constant {name} is not allowed")


def _finite_float(text: str) -> float:
    value = float(text)
    if not math.isfinite(value):
        raise ValueError("non-finite number")
    return value


def _parse_error(text: str) -> dict:
    return {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": text}}


def _respond(config: Config, line: bytes | str) -> dict | None:
    """Decode and parse one request line; a bad line is a parse error, never a crash."""
    try:
        text = line.decode("utf-8") if isinstance(line, bytes) else line
        if not text.strip():
            return None
        message = json.loads(text, parse_constant=_no_constant, parse_float=_finite_float)
    except (ValueError, RecursionError):
        return _parse_error("parse error")
    return handle(config, message)


def serve(config: Config, stdin=None, stdout=None) -> None:
    """Read JSON-RPC lines (bytes or text) until EOF; each line at most MAX_REQUEST_BYTES."""
    stdin = stdin if stdin is not None else sys.stdin.buffer
    stdout = stdout or sys.stdout
    while line := stdin.readline(MAX_REQUEST_BYTES + 1):
        newline = b"\n" if isinstance(line, bytes) else "\n"
        if len(line.rstrip(newline)) > MAX_REQUEST_BYTES:
            # Drop the rest of the oversized line without holding it.
            while not line.endswith(newline):
                line = stdin.readline(READ_BLOCK)
                if not line:
                    break
            response = _parse_error(f"request line over {MAX_REQUEST_BYTES} bytes")
        else:
            response = _respond(config, line)
        if response is not None:
            stdout.write(json.dumps(response, allow_nan=False) + "\n")
            stdout.flush()


class _Once(argparse.Action):
    """An option that may be given at most once."""

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest) is not None:
            parser.error(f"{option_string} given more than once")
        setattr(namespace, self.dest, values)


def _load_config(parser: argparse.ArgumentParser, options: argparse.Namespace) -> Config:
    """Fail closed: refuse to serve content without an approved-field allow-list,
    unless whole unmasked lines were chosen explicitly for directed debugging."""
    if options.fields_file is None and not options.allow_unredacted:
        parser.error("refusing to start without approved fields: pass --fields-file PATH "
                     "(optionally with --redact-file PATH as a backup mask), or "
                     "--allow-unredacted for debugging Joshua directs")
    if options.fields_file is not None and options.allow_unredacted:
        parser.error("--fields-file and --allow-unredacted are mutually exclusive")
    for option, path in (("--fields-file", options.fields_file),
                         ("--redact-file", options.redact_file)):
        if path is not None and not path.is_file():
            parser.error(f"{option} {path} is not a regular file")
    if options.fields_file is not None:
        try:
            Fields.load(options.fields_file)
        except (OSError, ValueError) as exc:
            parser.error(f"cannot load --fields-file: {exc}; refusing to start")
    try:
        config = Config.build(options.nt_root, options.journal_dir, options.export_dir,
                              options.redact_file, options.fields_file, options.refusal_dir)
    except (OSError, ValueError, re.error) as exc:
        parser.error(f"cannot load --redact-file: {exc}")
    if options.redact_file is not None and not config.redactions:
        parser.error(f"--redact-file {options.redact_file} has no patterns; refusing to start")
    return config


def main(argv: list[str] | None = None, stdin=None, stdout=None) -> int:
    parser = argparse.ArgumentParser(description="Read-only NinjaTrader 8 MCP server (stdio).",
                                     allow_abbrev=False)
    parser.add_argument("--nt-root", type=Path, default=Path.home() / "Documents" / "NinjaTrader 8",
                        help="NinjaTrader user data folder (default ~/Documents/NinjaTrader 8)")
    parser.add_argument("--journal-dir", type=Path, action=_Once,
                        help="strategy journal directory (private custody)")
    parser.add_argument("--refusal-dir", type=Path, action=_Once,
                        help="strategy refusal-file directory (private custody)")
    parser.add_argument("--export-dir", type=Path, action=_Once,
                        help="export directory (private custody)")
    parser.add_argument("--fields-file", type=Path, action=_Once,
                        help="private allow-list of approved fields, signed off by Joshua; "
                             "only these fields are served (required unless --allow-unredacted)")
    masking = parser.add_mutually_exclusive_group()
    masking.add_argument("--redact-file", type=Path, action=_Once,
                         help="regexes to mask in every emitted value, one per line (backup to "
                              "--fields-file)")
    masking.add_argument("--allow-unredacted", action="store_true",
                         help="serve whole lines unmasked, for debugging Joshua directs only; "
                              "never persist the output")
    options = parser.parse_args(argv)
    config = _load_config(parser, options)
    if stdout is None:
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    serve(config, stdin, stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
