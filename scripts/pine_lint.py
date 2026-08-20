#!/usr/bin/env python3
"""§2.3 — pine_lint.py: static linter for codification-stage candidate .pine.

⚠ STATUS (corrected 2026-08-08; Actions-status clause corrected 2026-08-19 per
Q-GATESTACK-1): this module is NOT wired. It appears in no Makefile target, no
scripts/gates.yml entry, and no git hook or CI workflow — that absence is about
this script specifically, independent of GitHub Actions being enabled repo-wide
(it has run live and green since the 2026-08-15 public transition). The previous docstring called it "THE
LOAD-BEARING CHECK of the R&D pipeline ... this linter owns it" — that was a
claim about importance, not about wiring, and a reader could not tell the
difference. Run it deliberately, or wire it (a `.pine`-scoped data-conditional
gate is the natural shape) — but do not assume a candidate passed through it.

THE RISK IT ADDRESSES IS REAL AND UNOWNED. Codification is the only stage that
can catch repaint / lookahead bias: the downstream harness operates only on the
trade CSV, so a repainting candidate produces a CSV that overstates edge and
CPCV/DSR/PBO will certify a phantom with full rigor. The contamination is in HOW
the returns were generated, not in the returns — invisible to everything
downstream. Nothing else covers it; today nothing covers it automatically.

Mirrors the output shape of the skill-side check_brief.py (the previously-cited
validation/concept_intake/check_concept.py was retired with the Gen-1 tree,
2026-07-11): PASS / FAIL / WARN per check with a symbol (✓/✗/!), a
per-check repair message, then a RESULT summary. Exit 0 if clean (no FAILs), 1
if any FAIL, 2 on usage error.

Checks (brief §2.3):
  REPAINT / LOOKAHEAD (the core job):
    - lookahead_on                       (barmerge.lookahead_on)
    - entry signal not gated on barstate.isconfirmed
    - future-referencing negative index  (series[-1], close[-n])
    - request.security without lookahead_off
  HARDCODE:
    - bare numeric literals in SIGNAL slots where input.* belongs
  LOCKED-PATH WRITE:
    - candidate path resolving inside a locked-production dir -> HARD REFUSE
  pinescript-v6 STATIC CHECKLIST:
    - //@version=6 declaration present
    - multi-line ternary (? / : split across lines)
    - continuation-line indentation
    - plot() in local scope
    - na handling on input-free division (advisory WARN)

Usage:
    python scripts/pine_lint.py <candidate.pine>
    python scripts/pine_lint.py <candidate.pine> --target-path strategies/candidates/x.pine
    python scripts/pine_lint.py --self-test
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SYMBOL = {"PASS": "✓", "FAIL": "✗", "WARN": "!"}

REPO_ROOT = Path(__file__).resolve().parents[1]

# Locked-production directories — any write resolving inside these is REFUSED.
# Sourced from strategies/{guardian,striker,aegis,nas} (the four locked books).
LOCKED_DIRS = (
    REPO_ROOT / "core" / "strategies" / "guardian",
    REPO_ROOT / "core" / "strategies" / "striker",
    REPO_ROOT / "core" / "strategies" / "aegis",
    REPO_ROOT / "core" / "strategies" / "nas",
)

# The sanctioned candidate output root.
CANDIDATE_DIR = REPO_ROOT / "core" / "strategies" / "candidates"

# Markers delimiting the emitter's signal slots. Hardcode-literal checking is
# scoped to lines BETWEEN a SIGNAL marker and the next section ruler so the
# scaffold's own plumbing literals (initial_capital=200000 etc.) are not flagged.
SIGNAL_SLOT_MARKERS = (
    "SIGNAL: INPUTS",
    "SIGNAL: FILTER",
    "SIGNAL: ENTRY",
    "INDICATORS & SIGNAL CALC",
)


@dataclass
class CheckResult:
    name: str
    status: str                 # PASS | FAIL | WARN
    message: str | None          # repair guidance (None when clean)
    kind: str = "mechanical"     # mechanical | judgment


# ---------------------------------------------------------------------------
# Locked-path write refusal (hard) — checked on the TARGET path, not contents
# ---------------------------------------------------------------------------

def is_locked_path(target: str | Path) -> bool:
    """True if `target` resolves inside any locked-production directory."""
    try:
        p = Path(target)
        # Resolve relative to repo root if not absolute; don't require existence.
        if not p.is_absolute():
            p = (REPO_ROOT / p)
        p = p.resolve(strict=False)
    except (OSError, ValueError):
        return False
    for locked in LOCKED_DIRS:
        try:
            locked_r = locked.resolve(strict=False)
        except (OSError, ValueError):
            continue
        if p == locked_r or locked_r in p.parents:
            return True
    return False


def check_locked_path(target_path: str | Path | None) -> CheckResult:
    if target_path is None:
        return CheckResult(
            "Output path not in a locked-production dir", "PASS",
            None,
        )
    if is_locked_path(target_path):
        return CheckResult(
            "Output path not in a locked-production dir", "FAIL",
            f"REFUSED — target '{target_path}' resolves inside a locked-production "
            "directory (strategies/{guardian,striker,aegis,nas}). Locked Pine is "
            "read-only; candidates MUST be written under strategies/candidates/ "
            "(forbidden move #1).",
        )
    return CheckResult("Output path not in a locked-production dir", "PASS", None)


# ---------------------------------------------------------------------------
# Source-content checks
# ---------------------------------------------------------------------------

def _signal_slot_lines(lines: list[str]) -> list[tuple[int, str]]:
    """Return (lineno, text) for lines inside a signal slot.

    A slot opens on a line containing a SIGNAL_SLOT_MARKER and closes at the next
    full section ruler (a comment line of '='*N) AFTER at least one content line.
    """
    out: list[tuple[int, str]] = []
    in_slot = False
    opened_at = -1
    for i, raw in enumerate(lines, 1):
        text = raw.rstrip("\n")
        stripped = text.strip()
        is_ruler = stripped.startswith("//") and set(stripped.replace("//", "").strip()) <= {"="} and "=" in stripped
        if any(m in text for m in SIGNAL_SLOT_MARKERS):
            in_slot = True
            opened_at = i
            continue
        if in_slot and is_ruler and i > opened_at + 1:
            in_slot = False
            continue
        if in_slot:
            out.append((i, text))
    return out


def check_version_decl(src: str) -> CheckResult:
    if re.search(r"^//@version=6\b", src, re.MULTILINE):
        return CheckResult("Pine v6 version declaration", "PASS", None)
    return CheckResult(
        "Pine v6 version declaration", "FAIL",
        "missing '//@version=6' as the first directive. Required for TradingView "
        "compilation.",
    )


def check_lookahead_on(src: str) -> CheckResult:
    hits = [
        i + 1 for i, ln in enumerate(src.splitlines())
        if "barmerge.lookahead_on" in ln and not ln.strip().startswith("//")
    ]
    if hits:
        return CheckResult(
            "No lookahead_on (future-bar leakage)", "FAIL",
            f"barmerge.lookahead_on found at line(s) {hits}. This leaks future-bar "
            "data into the backtest — the exact contamination nothing downstream "
            "can catch. Use lookahead=barmerge.lookahead_off.",
        )
    return CheckResult("No lookahead_on (future-bar leakage)", "PASS", None)


def check_security_lookahead(src: str) -> CheckResult:
    """Any request.security(...) must specify lookahead_off explicitly."""
    bad = []
    for i, ln in enumerate(src.splitlines(), 1):
        if ln.strip().startswith("//"):
            continue
        if "request.security" in ln or re.search(r"\bsecurity\s*\(", ln):
            if "lookahead" not in ln and "lookahead_off" not in src:
                bad.append(i)
            elif "lookahead_on" in ln:
                bad.append(i)
    if bad:
        return CheckResult(
            "request.security uses lookahead_off", "FAIL",
            f"request.security at line(s) {bad} without explicit "
            "lookahead=barmerge.lookahead_off. The default historical behavior can "
            "repaint on the realtime bar. Always pin lookahead_off.",
        )
    return CheckResult("request.security uses lookahead_off", "PASS", None)


def check_future_index(src: str) -> CheckResult:
    """Negative-offset indexing (series[-1]) references not-yet-formed bars."""
    bad = []
    for i, ln in enumerate(src.splitlines(), 1):
        if ln.strip().startswith("//"):
            continue
        if re.search(r"\[\s*-\s*\d+\s*\]", ln):
            bad.append(i)
    if bad:
        return CheckResult(
            "No future-referencing negative index", "FAIL",
            f"negative-offset index (series[-n]) at line(s) {bad} references "
            "future bars. Pine indexing is backward-only; a negative offset is a "
            "lookahead bug.",
        )
    return CheckResult("No future-referencing negative index", "PASS", None)


def check_entry_confirmed(src: str) -> CheckResult:
    """Entry signals must be gated on barstate.isconfirmed.

    Heuristic: every line invoking strategy.entry( must be inside an if-block
    whose condition (or an enclosing condition) references barstate.isconfirmed,
    OR the file must gate the longSignal execution on barstate.isconfirmed.
    We approximate: if strategy.entry appears but barstate.isconfirmed does NOT
    appear anywhere guarding it -> FAIL.
    """
    lines = src.splitlines()
    entry_lines = [i for i, ln in enumerate(lines)
                   if "strategy.entry" in ln and not ln.strip().startswith("//")]
    if not entry_lines:
        # No entries at all -> nothing to repaint via same-bar entry.
        return CheckResult(
            "Entry gated on barstate.isconfirmed", "WARN",
            "no strategy.entry() found — cannot confirm entry-confirmation gating. "
            "If this is a candidate, it has no entry. Flagged for review.",
            kind="judgment",
        )
    # Look upward from each entry line for the controlling if-condition(s).
    for idx in entry_lines:
        guarded = False
        entry_indent = len(lines[idx]) - len(lines[idx].lstrip())
        for j in range(idx, -1, -1):
            ln = lines[j]
            stripped = ln.strip()
            if not stripped or stripped.startswith("//"):
                continue
            indent = len(ln) - len(ln.lstrip())
            if indent < entry_indent and stripped.startswith("if "):
                if "barstate.isconfirmed" in stripped:
                    guarded = True
                    break
                # keep climbing to an outer if
                entry_indent = indent
            # also accept a same-or-outer if directly containing the gate
            if stripped.startswith("if ") and "barstate.isconfirmed" in stripped and indent <= entry_indent:
                guarded = True
                break
        if not guarded:
            return CheckResult(
                "Entry gated on barstate.isconfirmed", "FAIL",
                f"strategy.entry at line {idx + 1} is not gated on "
                "barstate.isconfirmed. On calc_on_every_tick the signal can fire "
                "and unfire intra-bar (repaint). Gate the entry on "
                "barstate.isconfirmed.",
            )
    return CheckResult("Entry gated on barstate.isconfirmed", "PASS", None)


# Numeric-literal pattern for hardcode detection inside signal slots.
# Skip: input.* lines, comments, group/string assignments, array indices [1],
# common Pine constants (0, 1, 100), color/time/percent fragments.
_NUM_LIT = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])")
_INPUT_LINE = re.compile(r"\binput\.")
_INDEX_ONLY = re.compile(r"\[\s*\d+\s*\]")


def check_hardcode_in_signal(lines: list[str]) -> CheckResult:
    """Flag bare numeric literals in SIGNAL slots where a sweepable input belongs.

    Tuning constants (ATR multiples, lengths, thresholds) must be input.* so the
    sweep can grid them (forbidden move #2). Literals that are clearly structural
    (loop bounds, array indices [1], 0/1 booleans-as-ints, percent 100) are
    allowed; everything else in a signal calc/entry slot is flagged.
    """
    slot = _signal_slot_lines(lines)
    offenders: list[tuple[int, str]] = []
    allowed = {"0", "1", "100", "2", "23456"}  # 23456 = session day-mask idiom
    for lineno, text in slot:
        stripped = text.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if _INPUT_LINE.search(text):
            continue  # input.* declarations legitimately carry numeric ranges
        # strip out indexing offsets like [1] before scanning
        scrub = _INDEX_ONLY.sub("", text)
        # strip quoted strings
        scrub = re.sub(r'"[^"]*"', "", scrub)
        for m in _NUM_LIT.finditer(scrub):
            tok = m.group(0)
            if tok in allowed:
                continue
            offenders.append((lineno, stripped))
            break
    if offenders:
        lns = ", ".join(str(n) for n, _ in offenders)
        ex = offenders[0][1]
        return CheckResult(
            "No hardcoded params in SIGNAL slots", "FAIL",
            f"bare numeric literal(s) in signal slot at line(s) {lns} (e.g. "
            f"'{ex}'). A tuning constant baked into signal logic is pre-overfitting "
            "and starves the sweep (forbidden move #2). Expose it as input.*.",
        )
    return CheckResult("No hardcoded params in SIGNAL slots", "PASS", None)


def check_multiline_ternary(lines: list[str]) -> CheckResult:
    """pinescript-v6: a ternary's ? or : must not end a continuation line."""
    bad = []
    for i, raw in enumerate(lines, 1):
        text = raw.rstrip("\n")
        if text.strip().startswith("//"):
            continue
        # a line ending in '?' or in ' :' (ternary split) without the rest
        stripped = text.rstrip()
        if re.search(r"\?\s*$", stripped) or re.search(r"(?<!:):\s*$", stripped):
            # allow ':' that is part of a session string already stripped; here a
            # trailing bare ? or : in code is the multi-line ternary error.
            if "?" in stripped or stripped.endswith(":"):
                bad.append(i)
    if bad:
        return CheckResult(
            "Ternary operators one-line", "FAIL",
            f"multi-line ternary at line(s) {bad} (a '?' or ':' ends the line). "
            "Pine v6 requires the whole ternary on one line or assigned via "
            "intermediate vars; this causes 'end of line without continuation'.",
        )
    return CheckResult("Ternary operators one-line", "PASS", None)


def check_plot_local_scope(lines: list[str]) -> CheckResult:
    """pinescript-v6: plot() may not appear in a local (indented) scope."""
    bad = []
    for i, raw in enumerate(lines, 1):
        text = raw.rstrip("\n")
        if text.strip().startswith("//"):
            continue
        indent = len(text) - len(text.lstrip())
        if indent > 0 and re.match(r"\s*plot\s*\(", text):
            bad.append(i)
    if bad:
        return CheckResult(
            "No plot() in local scope", "FAIL",
            f"plot() in a local scope at line(s) {bad}. Pine raises "
            "\"Cannot use 'plot' in local scope\". Move it to top level and gate "
            "with a ternary (plot(cond ? v : na)).",
        )
    return CheckResult("No plot() in local scope", "PASS", None)


def check_continuation_indent(lines: list[str]) -> CheckResult:
    """pinescript-v6: a continuation line (after a trailing binary operator/comma)
    must be indented MORE than the STATEMENT's first line — not more than the
    immediately-preceding line (consecutive continuation lines legitimately share
    one indent). Advisory WARN: a full parser is needed for certainty; we flag
    the clear case where a continuation is indented <= the statement-start line.
    """
    bad = []
    cont_ops = ("and", "or", "+", "-", "*", "/", ",")

    def _indent(s: str) -> int:
        return len(s) - len(s.lstrip())

    i = 0
    n = len(lines)
    while i < n - 1:
        cur = lines[i].rstrip("\n")
        cs = cur.strip()
        if not cs or cs.startswith("//"):
            i += 1
            continue
        # Is this the start of a continued statement?
        if any(cs.endswith(op) for op in cont_ops):
            stmt_indent = _indent(cur)
            # Walk the continuation run; each line is compared to STMT indent.
            j = i + 1
            while j < n:
                cont = lines[j].rstrip("\n")
                ds = cont.strip()
                if not ds or ds.startswith("//"):
                    break
                if _indent(cont) <= stmt_indent:
                    bad.append(j + 1)
                    break
                # if this continuation also ends in an operator, the run continues
                if not any(ds.endswith(op) for op in cont_ops):
                    break
                j += 1
            i = j
            continue
        i += 1
    if bad:
        return CheckResult(
            "Continuation-line indentation", "WARN",
            f"possible under-indented continuation at line(s) {bad}. Pine "
            "continuation lines must be indented MORE than the first line. Verify "
            "in TradingView. Flagged for review.", kind="judgment",
        )
    return CheckResult("Continuation-line indentation", "PASS", None)


# Top-level declaration: optional var/varip, optional TYPE keyword (each kept
# distinct by requiring trailing whitespace, so a var named e.g. "intRate" is not
# misparsed as type 'int'), then the identifier and a single '=' that is neither
# ':=' (reassignment) nor '==' (comparison).
_TOP_DECL = re.compile(
    r"^(?:(?:var|varip)\s+)?"
    r"(?:(?:float|int|bool|string|color|line|label|table|box|array|matrix|map)\s+)?"
    r"([A-Za-z_]\w*)\s*=(?!=)"
)


def check_duplicate_declarations(lines: list[str]) -> CheckResult:
    """Flag any top-level variable declared with '=' more than once.

    Re-declaring a name with '=' (instead of ':=') at the same scope is a Pine
    compile error ("Variable is already declared"). This is the class the scaffold
    comment-leak and the redundant filter-guard fell into — invisible to the
    repaint checks but fatal at compile, so the candidate would never run. Only
    top-level (indent 0) declarations are counted; indented (local-scope) lines
    and ':=' reassignments are excluded.
    """
    seen: dict[str, list[int]] = {}
    for i, raw in enumerate(lines, 1):
        text = raw.rstrip("\n")
        if not text or text[:1].isspace():   # indented => local scope, skip
            continue
        if text.lstrip().startswith("//"):
            continue
        m = _TOP_DECL.match(text)
        if m:
            seen.setdefault(m.group(1), []).append(i)
    dupes = {name: ls for name, ls in seen.items() if len(ls) > 1}
    if dupes:
        detail = "; ".join(f"{n} at lines {ls}" for n, ls in sorted(dupes.items()))
        return CheckResult(
            "No duplicate top-level declarations", "FAIL",
            f"variable(s) declared with '=' more than once at top level: {detail}. "
            "Pine raises 'Variable is already declared' (use ':=' to reassign). A "
            "duplicate here means the emitter leaked a slot into the header or "
            "emitted a redundant guard — the candidate will not compile.",
        )
    return CheckResult("No duplicate top-level declarations", "PASS", None)


def check_no_unrendered_placeholder(src: str) -> CheckResult:
    """No unsubstituted {{...}} template token may remain in a rendered candidate."""
    hits = sorted(set(re.findall(r"\{\{[^}]+\}\}", src)))
    if hits:
        return CheckResult(
            "No unrendered template placeholders", "FAIL",
            f"unsubstituted scaffold placeholder(s) remain: {hits}. The emitter did "
            "not fill every slot — the candidate is incomplete.",
        )
    return CheckResult("No unrendered template placeholders", "PASS", None)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Alert shadowing (c1 rail) — informational alert() starving the JSON payload
# ---------------------------------------------------------------------------

_ALERT_CALL = re.compile(r"\balert\s*\(")
# A JSON alert payload opens an object with a quoted key: {"leg_id": ...
_JSON_OBJ = re.compile(r"\{\s*[\"']")
_ASSIGN = re.compile(r"^\s*(?:var\s+)?(\w+)\s*(?::=|=)\s*(.+)$")


def _strip_comments(src: str) -> str:
    """Drop `//` comments without cutting inside string literals."""
    out_lines = []
    for line in src.splitlines():
        buf, quote, i = [], None, 0
        while i < len(line):
            ch = line[i]
            if quote:
                buf.append(ch)
                if ch == "\\" and i + 1 < len(line):
                    buf.append(line[i + 1])
                    i += 2
                    continue
                if ch == quote:
                    quote = None
            elif ch in "\"'":
                quote = ch
                buf.append(ch)
            elif ch == "/" and line[i + 1:i + 2] == "/":
                break
            else:
                buf.append(ch)
            i += 1
        out_lines.append("".join(buf))
    return "\n".join(out_lines)


def _first_arg(text: str, open_idx: int) -> str:
    """Text of the first argument of a call whose '(' is at open_idx."""
    depth, quote, start = 0, None, open_idx + 1
    for i in range(open_idx, len(text)):
        ch = text[i]
        if quote:
            if ch == "\\":
                continue
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start:i]
        elif ch == "," and depth == 1:
            return text[start:i]
    return text[start:]


def check_alert_json_only(src: str) -> CheckResult:
    """Rail editions must not mix JSON alert payloads with plain-text alert()s.

    TradingView's "Any alert() function call" delivers ONE alert() message per
    bar, so an informational alert can win the race and starve the JSON payload
    the rail parses. That is the 2026-07-21 B7 first-fire miss: both venue
    editions were made JSON-only and re-pinned in PORT_MANIFEST.sha256.

    Self-scoping: fires only on files that already emit a JSON payload. A
    candidate with no JSON alert has no contract to shadow.
    """
    name = "Alert path JSON-only (no informational-alert shadowing)"
    clean = _strip_comments(src)

    json_vars = {
        m.group(1) for m in (_ASSIGN.match(ln) for ln in clean.splitlines())
        if m and _JSON_OBJ.search(m.group(2))
    }

    json_alerts, text_alerts = 0, []
    for m in _ALERT_CALL.finditer(clean):
        arg = _first_arg(clean, m.end() - 1).strip()
        if _JSON_OBJ.search(arg) or arg in json_vars:
            json_alerts += 1
        else:
            text_alerts.append(arg[:60])

    if json_alerts and text_alerts:
        return CheckResult(
            name, "FAIL",
            f"{len(text_alerts)} plain-text alert() call(s) coexist with "
            f"{json_alerts} JSON payload alert(s): {text_alerts}. TradingView "
            "delivers one alert() message per bar, so the informational call can "
            "shadow the JSON payload and the rail routes no order (2026-07-21 "
            "B7 miss). Remove the informational alert()s; keep the edition "
            "JSON-only and re-pin PORT_MANIFEST.sha256.",
        )
    return CheckResult(name, "PASS", None)


def run_checks(src: str, target_path: str | Path | None = None) -> list[CheckResult]:
    lines = src.splitlines()
    return [
        check_locked_path(target_path),
        check_alert_json_only(src),
        check_version_decl(src),
        check_lookahead_on(src),
        check_security_lookahead(src),
        check_future_index(src),
        check_entry_confirmed(src),
        check_hardcode_in_signal(lines),
        check_multiline_ternary(lines),
        check_plot_local_scope(lines),
        check_continuation_indent(lines),
        check_duplicate_declarations(lines),
        check_no_unrendered_placeholder(src),
    ]


def is_clean(results: list[CheckResult]) -> bool:
    """Clean iff no FAILs. WARNs are surfaced for human review, not blocking."""
    return not any(r.status == "FAIL" for r in results)


def render(results: list[CheckResult], label: str, verbose: bool = True) -> bool:
    passes = sum(r.status == "PASS" for r in results)
    fails = sum(r.status == "FAIL" for r in results)
    warns = sum(r.status == "WARN" for r in results)
    if verbose:
        print(f"Candidate: {label}")
        print()
        for i, r in enumerate(results, 1):
            sym = SYMBOL[r.status]
            tag = "" if r.kind == "mechanical" else "  [judgment]"
            print(f"  [{i}] {r.name:<44} {sym} {r.status}{tag}")
            if r.message:
                print(f"        -> {r.message}")
        print()
    clean = fails == 0
    total = len(results)
    if clean:
        print(f"RESULT: PASS ({passes}/{total} PASS, {warns} WARN for human review)")
    else:
        print(f"RESULT: FAIL ({fails} of {total} checks failed; {warns} WARN)")
    return clean


def lint_text(src: str, target_path: str | Path | None = None,
              label: str = "<text>", verbose: bool = True) -> bool:
    results = run_checks(src, target_path=target_path)
    return render(results, label, verbose=verbose)


def lint_file(path: str | Path, target_path: str | Path | None = None,
              verbose: bool = True) -> bool:
    p = Path(path)
    src = p.read_text(encoding="utf-8")
    tgt = target_path if target_path is not None else p
    return lint_text(src, target_path=tgt, label=str(p), verbose=verbose)


def _self_test() -> int:
    """Lint the scaffold template itself (slots filled -> should pass structure)."""
    scaffold = REPO_ROOT / "lab" / "codification" / "scaffold.pine.tmpl"
    if not scaffold.exists():
        print(f"self-test: scaffold not found at {scaffold}")
        return 2
    src = scaffold.read_text(encoding="utf-8")
    # Substitute trivial clean slot content so structural checks have signal.
    #
    # EVERY slot the scaffold declares must be filled — check 13 ("no unrendered
    # template placeholders") is one of the checks under test, so a missing
    # substitution here fails the self-test on the harness rather than on the
    # linter. The short-side and trailing slots were added to the scaffold after
    # this list was written and went unfilled, which is exactly what check 13
    # was reporting. Keep this list in sync with
    # `grep -o '{{[A-Z_]*}}' lab/codification/scaffold.pine.tmpl | sort -u`.
    #
    # Short side renders `shortSignal = false` per the scaffold's own line 169
    # ("Long-only candidates render `shortSignal = false`, leaving the short
    # block below dead (but compiling)") — that is also the shape of the locked
    # book, whose venue editions carry zero `strategy.short`. The dead blocks
    # still have to COMPILE, so their expression slots get valid mirrors.
    src = (src
           .replace("{{TITLE}}", "Self Test")
           .replace("{{SHORTTITLE}}", "ST")
           .replace("{{SIGNAL_INPUTS}}", 'stLen = input.int(20, "L", group="═══ SIGNAL ═══")')
           .replace("{{SIGNAL_CALC}}", "stEma = ta.ema(close, stLen)")
           .replace("{{SIGNAL_FILTER}}", "signalFilterOK = true")
           .replace("{{SIGNAL_ENTRY}}", "longSignal = close > stEma and close[1] <= stEma[1]")
           .replace("{{SIGNAL_ENTRY_SHORT}}", "shortSignal = false")
           .replace("{{USE_TRAILING}}", "false")
           .replace("{{SIGNAL_EXIT_DIST}}", "ta.atr(stLen) * 1.5")
           .replace("{{SIGNAL_EXIT_TP}}", "close + ta.atr(stLen) * 3.0")
           .replace("{{SIGNAL_EXIT_TP_SHORT}}", "close - ta.atr(stLen) * 3.0")
           .replace("{{SIGNAL_EXIT_TRAIL_DIST}}", "ta.atr(stLen) * 2.0"))
    leftover = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", src)))
    if leftover:
        print(f"self-test: scaffold slots not covered by this harness: {leftover}\n"
              f"  -> add them to _self_test()'s substitution list, then re-run.")
        return 2
    ok = lint_text(src, target_path=CANDIDATE_DIR / "selftest.pine",
                   label="scaffold(self-test)")
    return 0 if ok else 1


def main(argv=None) -> int:
    # Windows consoles default to cp1252, which cannot encode this tool's own
    # PASS/FAIL glyphs (U+2713 / U+2717) or the scaffold's box-drawing group
    # headers — the linter crashed with UnicodeEncodeError before printing a
    # single result, so a real finding was indistinguishable from a broken tool.
    # errors="replace" degrades a glyph to '?' rather than losing the report.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):  # redirected / already-wrapped stream
            pass

    ap = argparse.ArgumentParser(description="Static linter for candidate Pine")
    ap.add_argument("pine", nargs="?", help="path to candidate .pine")
    ap.add_argument("--target-path", default=None,
                    help="intended write path (for locked-path refusal check)")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()
    if not args.pine:
        ap.error("pine path required (or --self-test)")

    clean = lint_file(args.pine, target_path=args.target_path,
                      verbose=not args.quiet)
    return 0 if clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
