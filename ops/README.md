# `ops/` — operational surface

Imports `core` + root-resident governance. **No strategy is deployed.** Live
posture is owned by [`AGENTS.md`](../AGENTS.md) §Live-execution posture — not
restated here.

| Path | Job |
|---|---|
| [`c1_rail/`](c1_rail/) | Listener / sizing host / arm CLI (disarmed) |
| [`c1_signal_daemon/`](c1_signal_daemon/) | S2b signal daemon (`emit_enabled=false`) |
| [`instruments/`](instruments/) | Per-symbol ledgers + mechanism index |
| [`sentinel/`](sentinel/) | Hygiene / preregistration scans |
| [`cli.py`](cli.py) | Tearsheet-only historical CLI |
| [`nt_readonly_mcp.py`](nt_readonly_mcp.py) | Read-only NinjaTrader 8 MCP server: logs, trace, journals, exports. Places nothing; see below |
| [`prop_envelope_default.md`](prop_envelope_default.md) | Prop-envelope v1 pointer |

Import split: rail modules are **flat** (`c1_rail_arm`, … under
`PYTHONPATH=ops/c1_rail`); the daemon is a **package**
(`python -m c1_signal_daemon` under `PYTHONPATH=ops/c1_signal_daemon`).
See [`REPO_MAP.md`](../REPO_MAP.md) §2.2.

Deploy packaging: [`deploy/c1_rail/`](../deploy/c1_rail/) ·
[`deploy/c1_signal_daemon/`](../deploy/c1_signal_daemon/).
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
| `nt_search` | Literal or regex search over the newest files, with context |
| `nt_errors` | Errors, rejections, disconnects and exceptions in the newest log and trace files |

Sources: `log` and `trace` under `--nt-root` (default `~/Documents/NinjaTrader 8`),
and optionally `journal` (`--journal-dir`) and `export` (`--export-dir`), both kept
in private custody outside the repo. Files are read as plain text; no NinjaTrader
line format is assumed.

**Account data.** Output can carry fills, account names and balances. It enters
the agent's context and never goes into this repo (data rules; spec B15).
`--redact-file` masks regexes, one per line, `#` for comments, in all output; keep
that file private too. Each full line is masked before it is cut to 2,000
characters, so a match that crosses the cut is still masked. Files are read in
bounded blocks (tails from the end, searches line by line), so memory stays bounded
whatever the file size. Don't register the server for Codex: journals and logs can
carry strategy parameters.

Register it in Claude Code on the NinjaTrader machine, local scope (the paths are
machine-specific, so no `.mcp.json` is committed):

```powershell
claude mcp add nt-readonly --scope local -- python -I ops/nt_readonly_mcp.py --nt-root "$HOME\Documents\NinjaTrader 8" --journal-dir <private journal dir> --redact-file <private redact file>
```

Run that from the checkout root, or give the script's absolute path. Any Python
3.11+ works; the server needs no packages. Tests: `tests/ops/test_nt_readonly_mcp.py`.
