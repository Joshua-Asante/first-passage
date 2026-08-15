# pine_check.py — zero-auth Pine v6 compile gate

Stdlib-only pre-flight compile checker. POSTs Pine source to TradingView's
**Guest** `translate_light` facade (`pine-facade.tradingview.com`), parses
`errors2`/`warnings2`, and recovers the offending source token as `[near: "..."]`.
No login, no chart, no CDP, no third-party server — the only egress is the POST
to TradingView's own compiler. Decouples the Pine compile loop from the
authenticated `tradingview-mcp` surface (deliberately not vendored here).

## Usage

```bash
python scripts/pine_check.py strategy.pine          # one file
python scripts/pine_check.py a.pine b.pine          # several (exit 1 if ANY fail)
python scripts/pine_check.py - < strategy.pine      # stdin
python scripts/pine_check.py --json strategy.pine   # machine-readable
```

Exit codes: `0` all clean · `1` a file had errors · `2` transport/usage failure.
Warnings do **not** affect the exit code.

## Validation provenance

Validated **RESOLVED-TRUSTWORTHY on 2026-06-23** (handoff
`cc_handoff_pine_check_validation.md`):

- All 4 locked strategies (Guardian v5.5 / Striker DJ30 v4.5 / Aegis v4.3 /
  NAS100 v1) compiled clean — the Guest endpoint is **verdict-equivalent to the
  authenticated editor** for self-contained scripts.
- 4 injected defects across distinct error classes (name-resolution / type /
  parse / arity) were all caught with correct `line:col`.
- **Published-library imports resolve**: `TradingView/ta/8` and
  `PineCoders/Time/4` compiled; a fake library errored
  *"does not have a published library"*.

## Two boundaries

1. **Locked `.pine` are gitignored** → absent from git worktrees; they live in
   the MAIN working tree only. Point the checker at main-tree paths (the oracle
   hook in `pine_check_audit.*` skips-if-missing for exactly this reason).
2. **Unpublished libraries won't resolve as Guest** (reasoned, not tested): a
   library still private/unpublished in the editor — the normal mid-iteration
   state — is invisible to an anonymous request, so an importing script fails
   this gate until its library is published.

## Re-checking

`scripts/pine_check_audit.sh` (bash) and `scripts/pine_check_audit.ps1`
(PowerShell) run the fixture assertions, the ENDPOINT tamper-grep, and the
oracle regression. Oracle paths are read from
`core/strategies/MANIFEST.sha256` (strategy `.pine` rows only; `_indicator.pine`
excluded) — do not hard-code paths in the audit scripts. **LOCAL / MANUAL only** (live network + locked `.pine`) — not
a CI gate. Fixtures: `tests/pine_check_fixtures/{good,bad}.pine`.
