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
| [`cli.py`](cli.py) | Tearsheet-only historical CLI |
| [`nt_readonly_mcp.py`](nt_readonly_mcp.py) | Read-only NinjaTrader 8 MCP server: logs, trace, journals, exports. Places nothing; see below |
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
and optionally `journal` (`--journal-dir`) and `export` (`--export-dir`), both kept
in private custody outside the repo. Files are read as UTF-8 text; no NinjaTrader
line format is assumed. A file that starts with a UTF-16/32 byte-order mark or has
NUL bytes in its first 64 KiB is refused (NULs between characters would defeat
every mask), and a later line with a NUL byte is omitted. Directory walks never
follow symlinks or junctions. Hard links are not detected: a hard link inside a
source to a file elsewhere is read like any other file.

**Account data.** Output can carry fills, account names and balances. It enters
the agent's context and never goes into this repo (data rules; spec B15).
`--redact-file` masks regexes in all output; keep that file private too. One
pattern per line, leading and trailing spaces stripped; a line starting with `#`
is a comment, so a pattern can't start with `#` (write `[#]`). The file may be
saved with or without a UTF-8 BOM; a pattern holding an invisible format
character (zero-width space, BOM and the like) stops the server from starting.
Patterns run in file order, each on one line at a time, so a later pattern sees
the earlier ones' `[redacted]`, and no pattern can span two lines. Every line is
masked, searched or not, so patterns must be linear-time: no nested quantifiers.

Each full line is masked before it is cut to 2,000 characters, so a match that
crosses the cut is still masked. A line over 64 KiB is never shown, even in part:
it comes back as `[line over 65536 bytes omitted]`, because a mask pattern might
depend on the part that isn't held in memory. Searches, globs and the `file`
argument all match the masked text, the same text that is returned: a masked
value can't be found by searching for it, so match counts can't rebuild it. A
file whose name holds a masked value is listed and opened by its masked name.

The server fails closed: it refuses to start unless it gets `--redact-file` (a
regular file, given once) with at least one pattern, or `--allow-unredacted`.
Options must be spelled in full. The two are mutually exclusive.
With `--allow-unredacted` the agent may see account data unmasked; that data must
never enter this repository. No default patterns ship for balances or P&L: write
ones that fit the account's formats.

**Search and memory.** Callers search with literal substrings only. Python's `re`
has no time limit and the server runs no subprocesses, so a caller regex could
stall every tool. `nt_search` rejects a `regex` argument, and `nt_errors` uses only
its built-in pattern and rejects a caller `pattern`. Files are read in bounded
blocks (tails from the end, searches line by line), so memory stays bounded
whatever the file size. A read stops at the size the file had when it was opened,
so a writer that keeps appending can't make it endless, and each call stops after
256 MiB or 20 seconds of reading. String arguments are capped at 1,024
characters, a request line at 1 MiB, and unknown argument names are refused. A
file that is locked, vanishes or can't be read is skipped with a `note:` line;
the rest of the call goes on.

Don't register the server for Codex: journals and logs can carry strategy
parameters.

Register it in Claude Code on the NinjaTrader machine, local scope (the paths are
machine-specific, so no `.mcp.json` is committed):

```powershell
claude mcp add nt-readonly --scope local -- python -I ops/nt_readonly_mcp.py --nt-root "$HOME\Documents\NinjaTrader 8" --journal-dir <private journal dir> --redact-file <private redact file>
```

Run that from the checkout root, or give the script's absolute path. Local scope
also reaches this repo's worktrees under `.claude/worktrees/`, so sessions there
get the server too. Any Python 3.11+ works; the server needs no packages. Tests:
`tests/ops/test_nt_readonly_mcp.py`.
