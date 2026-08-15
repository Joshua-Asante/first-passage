#!/usr/bin/env python3
"""
pine_check.py - standalone Pine Script compile checker.

Calls TradingView's translate_light compile endpoint as Guest (no login,
no chart open, no CDP, no third-party server) and reports structured errors.

This reproduces the load-bearing compile path of the tradingview-mcp
'pine_check' tool in auditable, stdlib-only Python. Nothing leaves your
machine except the POST to pine-facade.tradingview.com.

Usage:
    python pine_check.py strategy.pine                # check one file
    python pine_check.py a.pine b.pine c.pine         # check several
    python pine_check.py -                            # read source from stdin
    python pine_check.py --json strategy.pine         # machine-readable output

Exit code: 0 if every input compiled clean, 1 if any had errors,
2 on a transport/usage failure. Warnings do NOT affect the exit code.

Embed in your own pipeline:
    from pine_check import check_pine
    res = check_pine(open("strategy.pine").read())
    if not res["compiled"]: ...
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

ENDPOINT = (
    "https://pine-facade.tradingview.com/pine-facade/translate_light"
    "?user_name=Guest&pine_id=00000000-0000-0000-0000-000000000000"
)
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://www.tradingview.com/",
    "User-Agent": "pine_check/1.0",
}


def _span(lines: list, line, column, end_line, end_column) -> str:
    """Return the source text an error points at, capped, or '' if unrecoverable.

    translate_light returns message templates with {placeholders} for the
    dynamic parts (identifier/function/type names) but always gives exact
    line/column ranges, so we recover the real token straight from the source.
    """
    if not line or line < 1 or line > len(lines):
        return ""
    row = lines[line - 1]
    if not column or column < 1:
        return row.strip()[:80]
    start = column - 1
    if end_line == line and end_column and end_column >= column:
        return row[start:end_column][:80]
    return row[start:].strip()[:80]


def check_pine(source: str, timeout: float = 20.0) -> dict:
    """Compile-check one Pine source string. Returns a structured result dict."""
    body = urllib.parse.urlencode({"source": source}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8", "replace"))

    src_lines = source.split("\n")
    inner = payload.get("result") or {}
    errors, warnings = [], []

    for e in inner.get("errors2") or []:
        start, end = e.get("start") or {}, e.get("end") or {}
        line, col = start.get("line"), start.get("column")
        end_line, end_col = end.get("line"), end.get("column")
        msg = e.get("message", "")
        item = {"line": line, "column": col, "end_line": end_line,
                "end_column": end_col, "message": msg}
        if "{" in msg:  # templated placeholder -> attach the source it points at
            near = _span(src_lines, line, col, end_line, end_col)
            if near:
                item["near"] = near
        errors.append(item)
    for w in inner.get("warnings2") or []:
        start, end = w.get("start") or {}, w.get("end") or {}
        line, col = start.get("line"), start.get("column")
        msg = w.get("message", "")
        item = {"line": line, "column": col, "message": msg}
        if "{" in msg:
            near = _span(src_lines, line, col, end.get("line"), end.get("column"))
            if near:
                item["near"] = near
        warnings.append(item)
    # top-level string error (e.g. malformed request)
    if isinstance(payload.get("error"), str) and payload["error"]:
        errors.append({"line": None, "column": None, "message": payload["error"]})

    return {
        "compiled": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def _fmt(label: str, items: list, kind: str) -> list:
    out = []
    for it in items:
        loc = ""
        if it.get("line") is not None:
            loc = f":{it['line']}"
            if it.get("column") is not None:
                loc += f":{it['column']}"
        msg = it["message"]
        if it.get("near"):
            msg += f'   [near: "{it["near"]}"]'
        out.append(f"{label}{loc}: {kind}: {msg}")
    return out


def main(argv: list) -> int:
    ap = argparse.ArgumentParser(
        description="Compile-check Pine Script via TradingView (Guest)."
    )
    ap.add_argument("files", nargs="+", help="Pine files to check, or '-' for stdin")
    ap.add_argument("--json", action="store_true",
                    help="emit JSON instead of compiler-style text")
    ap.add_argument("--timeout", type=float, default=20.0,
                    help="HTTP timeout seconds (default 20)")
    args = ap.parse_args(argv)

    results, any_errors = {}, False
    for path in args.files:
        try:
            source = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        except OSError as ex:
            print(f"{path}: fatal: cannot read file ({ex})", file=sys.stderr)
            return 2
        try:
            res = check_pine(source, timeout=args.timeout)
        except HTTPError as ex:
            print(f"{path}: fatal: endpoint returned HTTP {ex.code}", file=sys.stderr)
            return 2
        except (URLError, TimeoutError, json.JSONDecodeError) as ex:
            print(f"{path}: fatal: transport error ({ex})", file=sys.stderr)
            return 2

        label = "<stdin>" if path == "-" else path
        results[label] = res
        any_errors = any_errors or not res["compiled"]

    if args.json:
        print(json.dumps(results, indent=2))
        return 1 if any_errors else 0

    for label, res in results.items():
        lines = _fmt(label, res["errors"], "error") + _fmt(label, res["warnings"], "warning")
        if lines:
            print("\n".join(lines))
        status = "OK" if res["compiled"] else f"FAILED ({res['error_count']} error(s))"
        wtail = f", {res['warning_count']} warning(s)" if res["warning_count"] else ""
        print(f"{label}: {status}{wtail}")
    return 1 if any_errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
