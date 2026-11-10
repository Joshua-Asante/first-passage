# `ops/` — operational surface

Imports `core` + root-resident governance. **No strategy is deployed.** Live
posture is owned by [`AGENTS.md`](../AGENTS.md) §Live-execution posture — not
restated here.

| Path | Job |
|---|---|
| [`c1_rail/`](c1_rail/) | `book_policy`, the fixed-book quantity and protection law used by offline replay. The rail itself is gone. |
| [`c1_signal_daemon/`](c1_signal_daemon/) | Offline replay library and private port root. The daemon itself is gone. |
| [`contract_roll.py`](contract_roll.py) | 6J and MGC roll calendar and G4 checks |
| [`instruments/`](instruments/) | Per-symbol ledgers + mechanism index |
| [`sentinel/`](sentinel/) | Hygiene / preregistration scans |
| [`nt_readonly_mcp.py`](nt_readonly_mcp.py) | Read-only NinjaTrader 8 MCP server: logs, trace, journals, exports. Places nothing; see below |
| [`nt_install_check.py`](nt_install_check.py) | Read-only install checks: installed NinjaScript vs a frozen manifest, and NT safety settings. See below |
| [`prop_envelope_default.md`](prop_envelope_default.md) | Prop-envelope v1 pointer |

See [`REPO_MAP.md`](../REPO_MAP.md) §2.2.

Layer contract: [`REPO_MAP.md`](../REPO_MAP.md).

## Read-only NinjaTrader MCP (`nt_readonly_mcp.py`)

A stdio MCP server, standard library only, that lets an agent read what
NinjaTrader 8 and the strategy instances write to disk instead of screenshotting
the Log tab or Output window. It runs outside NinjaTrader and never talks to it:
no sockets, ATI, AddOn or subprocess, files opened read-only, every path confined
to a configured directory. It cannot place, change or cancel orders, so money
controls 1 and 3 and spec check B1 are unchanged. Orders, and anything shown only
in NinjaTrader's or Tradovate's grids, still go through computer use.

| Tool | Does |
|---|---|
| `nt_list_sources` | The configured directories and whether each exists |
| `nt_list_files` | Files in a source, newest first, with size and time |
| `nt_tail` | Last N lines of a file (default: the newest) |
| `nt_search` | Literal substring search over the newest files, with context |
| `nt_errors` | Errors, rejections, disconnects and exceptions in the newest log and trace files (fixed built-in pattern) |

Sources: `log` and `trace` under `--nt-root` (default `~/Documents/NinjaTrader 8`),
and optionally `journal` (`--journal-dir`), `refusal` (`--refusal-dir`) and
`export` (`--export-dir`), all kept in private custody outside the repo. Files are
read as UTF-8 text. A file that starts with a UTF-16/32 byte-order mark or has
NUL bytes in its first 64 KiB is refused (NULs between characters would defeat
every mask), and a later line with a NUL byte is omitted. Directory walks never
follow symlinks or junctions. Hard links are not detected: a hard link inside a
source to a file elsewhere is read like any other file.

**Approved fields.** The files carry account data and can carry strategy
parameters, and agents read private logs only through tools that return approved
fields (AGENTS.md data rules). `--fields-file` names those fields. The file is
private: it lives outside the repo, and Joshua signs it off. Every tool that
returns file content (`nt_tail`, `nt_search`, `nt_errors`) emits only those
fields; anything not on the list is dropped, never shown. Format: UTF-8 text
(a BOM is fine), one rule per line, `#` starts a comment line, and each rule is
`<source> <field>`:

| Source | Fields that can be approved |
|---|---|
| `log` | `timestamp`, `level`, `category`, `kv:<Key>` |
| `trace` | `timestamp`, `kv:<Key>` |
| `journal` | `json:<dotted.path>` |
| `refusal` | `json:<dotted.path>` |
| `export` | none: the source is refused (below) |

With `--fields-file`, a record is the text between two `\n` newlines, with one
trailing `\r` stripped; CR, VT, FF, `\x1c`–`\x1e`, U+0085, U+2028 and U+2029
stay inside the record. Log lines are `timestamp|level|category|text`; trace
lines are a timestamp, then text. A log record gives no field at all (no
fixed field and no kv) unless its timestamp looks like `YYYY-MM-DD hh:mm:ss`
(optional fraction) and its level and category are each 1–32 letters, digits or
`_`, so a quote or a pipe inside a quoted value can never move free text into
the header. A trace record gives no field unless it starts with such a timestamp
followed by whitespace or the line end.
`kv:<Key>` takes `Key='value'`, `Key="value"` or `Key=value` pairs from the text,
and fails closed whenever quoting is in doubt:

- The text must be printable ASCII (tab allowed) with no backtick. A control
  character, a Unicode line break or any non-ASCII quotation mark (curly quotes,
  `«»`, fullwidth quotes and the like) gives no kv field for the line.
- A `'` or `"` opens a quoted span only directly after `Key=`; the span runs to
  the next same quote, and keys are read only outside spans, so text inside any
  quoted value (whoever's key it follows) is never taken as a pair. Any other
  quote (a prose apostrophe such as `don't`, a quote after `Note:` or `(Note=`),
  an unclosed span, a backslash inside a span, or a closing quote followed by
  anything but whitespace, `,`, `;`, `|`, `&` or the line end (a doubled quote,
  `Note='it's`, `Price="1"tail`) makes the line's quoting unclear.
- A quoted message may run over several lines, and parity can't tell where it
  ends (an apostrophe in the value flips it). So quoting is checked on every log
  and trace record from the start of the file: a record with any quotation-like
  character (not only `'` and `"`) whose quoting is not clear in the sense above,
  and any omitted line, gives no field at all (timestamp, level and category
  included), and neither does any later record of the file. `nt_tail` learns
  this and its window from one forward read of the file from its start, so a
  record is judged by the bytes read before it (see **Files that change while
  they are read** below). A file larger than half the read budget gives no
  field in its window. A `note:` line says when fields were withheld this way. A log whose messages quote names in prose
  (`strategy 'X'`) therefore gives no fields after the first such message.
- A quoted value is the span's whole content. An unquoted value is a plain token
  (letters, digits, `_.:+-`) that must end at whitespace, `,`, `;`, `|`, `&` or
  the line end; otherwise the pair is dropped, so one value never carries another
  pair out with it. Either way a value is emitted only if it is at most 128
  characters of letters, digits, space and `_.:+-/@`, the same limit as JSON
  strings below.

A key must start the text or follow whitespace or one of those delimiters, and be
directly followed by `=`, so keys with spaces (NinjaTrader's `New state=…`, for
example) are not recognised. Check real NinjaTrader log and trace lines locally
against these rules before relying on a `kv:` field: a line that doesn't fit them
just yields fewer kv fields (or none), never extra text.

One limit remains: a value that itself holds a closing quote followed by
` Key='...'`, or unquoted free text holding ` Key=value`, can't be told apart from
real pairs, so it can surface as an approved field. When Joshua signs off the
allow-list, approve only `kv:` keys whose writers never put quotes or `Key=` text
inside other values.

Journals must be JSON Lines: one complete JSON object per line (`seq`, `prev`,
`kind`, `body`, `hash`). A journal line that is not one (a line of a
pretty-printed object, a blank line), or an omitted line, gives no field, and
neither does any later line of that file, since it may be the inside of a
multi-line record; `nt_tail` reads the file from its start for this, as for
quoting above, and a `note:` line says when fields were withheld. A refusal file
is one JSON object (`code`, `utc`, `fields`) and is read as one record. `json:a.b` walks
objects, decoding a string that holds a JSON object on the way, so `json:body.code`
reads `code` inside the `body` string. Only scalars are emitted: finite numbers,
booleans, null, and plain strings of at most 128 characters drawn from letters,
digits, space and `_.:+-/@`. A path that ends on an object, an array or any other
string (JSON or near-JSON text such as `json:body`, quotes, braces, long text)
gives nothing. A malformed line, an unknown source or field, or a file with no rules stops
the server from starting. Order IDs and names, hashed or not, are not approved
fields: don't list them.

Each line comes back as one compact JSON object of approved field to value, for
example `{"timestamp":"…","kv:Status":"…"}`. A line with no approved field is left
out and counted in the header (`nt_tail`) or summary (`nt_search`, `nt_errors`), so
"last N lines" still means the last N lines of the file. Searches, including
`nt_errors`' built-in pattern, match only within approved values.

**Files that change while they are read** (approved-field mode). NinjaTrader
writes today's log while it is read, so two things are never trusted:

- A last line with no newline yet may be one the writer has not finished, and
  part of a line can look clear when the whole line is not. It is never judged or
  shown: `nt_tail` returns `[unfinished last line (no newline yet) omitted]` in
  its place and `nt_search` and `nt_errors` skip it. A journal's last object
  counts only once its newline is written.
- A writer that rewrites part of a file during one forward read gives a torn
  view: an old prefix, then a new suffix whose records may sit inside a quoted
  span the unseen new prefix opens. So after reading a log, trace, journal or
  refusal file, the server checks that the path still names the same file
  (device and inode or file index), that the file has not shrunk below what was
  read, that it kept its modification time if it kept its size, and that a
  second read of the same bytes is identical (SHA-256). If any check fails,
  nothing from that file is shown: `nt_tail` withholds every field and says the
  file changed (try again), and `nt_search` and `nt_errors` drop that file's
  matches with a `note:` line. A search whose read budget runs out mid-file
  shows nothing from that file, since the read cannot be checked. Growth by
  appending passes, since only the bytes up to the size at open are read.

  Residual: a writer that changes the bytes being read and puts the same bytes
  back in step with both reads, leaving the size and modification time as they
  were, is not detected; logs and journals are expected to grow only by
  appending. The server does not lock files: opening without write sharing on
  Windows would fail on NinjaTrader's open log.

With `--fields-file`, the `export` source is refused outright by every tool:
`nt_list_files`, `nt_tail` and `nt_search` return an error naming the refusal
(`nt_errors` reads only `log` and `trace`), and
`nt_list_sources` shows it as refused: no export field can be approved, so not even
its file names, sizes or line counts are served. File names, configured paths and
tail/search headers in the other sources are metadata the allow-list does not cover:
they are masked only by `--redact-file`, so `--fields-file` refuses to start without it.

**Masking, as a backup.** `--redact-file` masks regexes in every emitted value;
keep that file private too. One
pattern per line, leading and trailing spaces stripped; a line starting with `#`
is a comment, so a pattern can't start with `#` (write `[#]`). The file may be
saved with or without a UTF-8 BOM; a pattern holding an invisible format
character (zero-width space, BOM and the like) stops the server from starting.
Patterns run in file order, each on one value at a time, so a later pattern sees
the earlier ones' `[redacted]`, and no pattern can span two lines. Every value is
masked, searched or not, so patterns must be linear-time: no nested quantifiers.

Each value (or, with `--allow-unredacted`, each full line) is masked before it is
cut to 2,000 characters, so a match that
crosses the cut is still masked. A line over 64 KiB is never shown, even in part:
it comes back as `[line over 65536 bytes omitted]`, because a mask pattern might
depend on the part that isn't held in memory. Searches, globs and the `file`
argument all match the masked text, the same text that is returned: a masked
value can't be found by searching for it, so match counts can't rebuild it. A
file whose name holds a masked value is listed and opened by its masked name.

The server fails closed: it refuses to start unless it gets `--fields-file` (a
regular file, given once, with at least one rule) together with `--redact-file`,
or `--allow-unredacted`. `--fields-file` without `--redact-file` is refused. The
two are mutually exclusive, and so are `--redact-file` and `--allow-unredacted`;
`--redact-file` alone is refused. Options must be spelled in full. An empty
`--redact-file` is refused. `--allow-unredacted` serves whole lines unmasked: it
is for debugging that Joshua directs, and its output is never persisted. No
default patterns ship for balances or P&L: write ones that fit the account's
formats.

**Search and memory.** Callers search with literal substrings only. Python's `re`
has no time limit and the server runs no subprocesses, so a caller regex could
stall every tool. `nt_search` rejects a `regex` argument, and `nt_errors` uses only
its built-in pattern and rejects a caller `pattern`. Files are read in bounded
blocks (searches, and tails in approved-field mode, line by line from the
start; other tails from the end), so memory stays bounded whatever the file
size. A read stops at the size the file had when it was opened,
so a writer that keeps appending can't make it endless, and each call stops after
256 MiB or 20 seconds of reading (in approved-field mode the check above reads
each file twice, and both reads count). String arguments are capped at 1,024
characters, a request line at 1 MiB, and unknown argument names are refused. A
file that is locked, vanishes or can't be read is skipped with a `note:` line;
the rest of the call goes on.

Register it in Claude Code on the NinjaTrader machine, local scope (the paths are
machine-specific, so no `.mcp.json` is committed):

```powershell
claude mcp add nt-readonly --scope local -- python -I ops/nt_readonly_mcp.py --nt-root "$HOME\Documents\NinjaTrader 8" --journal-dir <private journal dir> --fields-file <private fields file> --redact-file <private redact file>
```

Run that from the checkout root, or give the script's absolute path. Local scope
also reaches this repo's worktrees under `.claude/worktrees/`, so sessions there
get the server too. Any Python 3.11+ works; the server needs no packages. Tests:
`tests/ops/test_nt_readonly_mcp.py`.

## Read-only NinjaTrader install checks (`nt_install_check.py`)

A standard-library CLI for the pre-session check (spec §5 item 4) and the Monday
Sim101 check. It opens files for reading only, follows no links and talks to
nothing. Output is one JSON object of hashes, booleans, counts, file names under
`bin/Custom` and assembly names; it never prints file contents, XML values,
connection or account names. Exit 0 pass, 1 fail, 2 error.

```powershell
python -I ops/nt_install_check.py install --manifest <frozen SHA256SUMS> --manifest-sha256 <its sha256>
python -I ops/nt_install_check.py config
```

- `install`: each manifest file in `bin/Custom/Strategies` is `match`, `differ`,
  `differ-eol-or-bom-only` (still a fail) or `missing`. Any other non-stock `.cs`
  NT compiles (disk or compile project) is `extra`, a fail. The compiled DLL must
  be newer than every compiled source and the compile project. Bytes are compared raw: NT compiles what is
  on disk.
- `config`: ATI off, both cancel-on-disable options off (B8), no non-simulated
  connection set to connect on startup, no strategy saved in a workspace, no
  add-on sources, no non-stock assemblies or compile references in use (by name
  or `HintPath`). A reference that resolves to nothing is a warning. A link met
  under `workspaces` or `AddOns` fails, since it is not inspected.

Limits: stock `@` files are trusted by name; the DLL is tied to its sources by
file time only (recompile after every copy); `ati_enabled` false does not prove
the ATI port is closed; the workspace count recognises saved strategies by type
name, not yet seen with a strategy saved. Tests: `tests/ops/test_nt_install_check.py`.
