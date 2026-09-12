# CC Handoff — TB-T1: account-snapshot sealer (Codex implementation packet)

**Type:** cc_handoff
**Date:** 2026-09-12
**Parent session:** Tradeify portfolio coordinator, dispatch 1 ([record](../../notes/2026-09-12-tradeify-portfolio-coordinator-dispatch-1.md))
**Spawn target:** Codex local (D-B6: Cursor is not a lane)
**Repo:** `Joshua-Asante/first-passage` — primary checkout `C:\Users\joshu\multi_firm_operations`
**Parent packet:** [Track B umbrella](2026-09-10-track-b-qualify-accepted-book-umbrella.md) TB-T1 stub (claim manifest row TB-T1)
**Governing contract:** [account-snapshot seal contract](../../spec/2026-09-12-tradeify-account-snapshot-seal-contract.md) (PROPOSED; the packet implements it verbatim)
**Authority:** Joshua (operator) merges; the coordinator adjudicates. This packet authorizes a tool and its tests, nothing else — no snapshot is captured, no account value is read, nothing is deployed.
**Disposition:** **READY** (entry condition "TB-P1 field/evidence contract fixed" is met by the governing contract).

> Run `handoff-verify` first: `git status -sb`, `git rev-parse --show-toplevel`, `git fetch origin`,
> `git log --oneline HEAD..origin/main`. Base must be at or after `c41e2be` (main, 2026-09-12). Work in
> `.worktrees/tb-t1` on branch `codex/tb-t1-snapshot-sealer`; never `git add -A`; never `git stash`;
> never write `STATE.md`, `docs/SESSIONS.md`, the campaign record, the governing plan, `CLAUDE.md`,
> `PIPELINES.md` or the umbrella. Commit no account value, no screenshot, no statement, no export.

---

## §0 — Rule 0 reads (verified base `c41e2be`; the worker re-verifies at dispatch)

| Source | Anchor | What it pins |
|---|---|---|
| `core/mc/simulation.py` `EvaluationState`, `_drawdown_outcome` and `core/mc/preflight.py` `firm_kwargs` | `adccb7d` | the five-field kernel validation plus the tier-aware initial drawdown-floor predicate; constructor validation alone does not reject an already-breached account; "cannot certify provenance" |
| `core/firm_rules.py` `Tradeify_Select_100K` | `d4d1c5e` | `starting_balance`, `max_dd_pct` 3.0, `profit_target_pct` 6.0, `min_trading_days` 3, `consistency_rule_pct` 40 |
| `core/lib/validation.py` | `origin/main` | `require_finite_number`, `dump_strict_json` |
| `scripts/certification_power.py` | `5e5a216` | stdlib-script convention (argparse, no third-party imports, exact-integer oracle in tests) |
| `ops/c1_rail/c1_sizing_host_reference.py` lines 44–52 | `509b524` | the `sys.path` bootstrap pattern for importing `core/` modules from a script |
| Governing contract | this dispatch (rev 3: Codex review on #358 folded — distinct artifacts, working orders, zero adjustments, `valid_until`) | fields, evidence files, checks C1–C10, output, boundary |
| Umbrella TB-T1 / TB-B7 stubs | `8f99b41` | evidence class (dashboard PRIMARY), refusal without the statement, freshness at a session boundary |

## §0.5 — Recommended defaults (apply unless Phase 0 contradicts; then `NEEDS_CONTEXT`)

- (A) Inputs arrive as one operator-authored JSON manifest path plus the three evidence file paths (CLI flags); no interactive prompts, no environment-variable secrets.
- (B) Frozen defaults live as module constants: `FRESHNESS_WINDOW_MINUTES = 30`, `SEAL_WITHIN_HOURS = 24`, the session-boundary rule of C5; a CLI flag may only tighten them.
- (C) Time zone: every timestamp must carry an offset; the tool converts to `America/New_York` (`zoneinfo`) for C5.
- (D) Output path default per the contract; the tool runs `git check-ignore -q <path>` from the repo root and refuses when the exit status is non-zero (C9).
- (E) Ambiguities the worker may not resolve: any new field, any relaxed check, any reading of Tradovate/Tradeify. Post them under `## §0.5 Response — ambiguities` in the PR body with `Status: NEEDS_CONTEXT`.

## §1 — Context

TB-B7 seals the fresh live-account snapshot that TB-E2 (the sole n3) initializes from. The kernel validates five numbers but cannot establish provenance; the campaign's accepted evidence class is the Tradeify dashboard capture (PRIMARY), with the relational fact `threshold + $3,000 == balance` at the high-water mark. This tool binds the typed values to the evidence files and their timestamps and refuses to seal otherwise. The fresh snapshot itself is a later operator gate (after Track A `RESOLVED`, TB-D0, TB-V1, TB-I4 and the TB-I3 live test).

## §2 — Steps (test-first)

- **2.1 Failing tests first** in `tests/test_seal_account_snapshot.py`, one per check: C1 missing/empty evidence file, the same canonical file passed for two evidence roles (including path aliases), and distinct paths with identical bytes; C2 kernel rejection (peak below basis; zero trade days with a non-pristine state; constructor-valid equity exactly at the floor, below it, or inside the kernel's rounded breach boundary must all refuse; a valid state safely above the boundary must pass); C3 equity ≠ balance, `positions_export_shows_flat: false`, and `working_orders_count: 1`; C4 `threshold + width < balance`; C5 captures 31 minutes apart, seal 25 hours late, a capture inside a live session (Tuesday 14:00 ET); C6 display disagrees by more than one point; C7 wrong target display; C8 any non-zero `cash_adjustments_total` (sum of absolute adjustment amounts, including equal deposit/withdrawal amounts whose signed net is zero; no note path exists); C9 output path not ignored (use a temporary git repo in the test); C10 seal time at or after the window's reopen, and `valid_until` equal to that reopen on a passing seal; plus one **synthetic** all-pass fixture at the high-water mark and one with a carried drawdown, asserting the sealed JSON's shape, `at_high_water_mark`, `valid_until`, the recorded digests. Parse stdout into exactly four allowed lines (one 64-character lowercase hexadecimal digest matching the sealed file, the exact passed check-id list, the derived ISO-8601 `valid_until`, and the fixed attestation sentence), with no additional text and empty stderr on success. On refusal, require empty stdout and only failing check ids on stderr. Do not search fixture digit sequences in allowed fields: check ids, timestamps and hashes legitimately contain digits.
- **2.2 Implement** `scripts/seal_account_snapshot.py`: stdlib only; `EvaluationState`, `_drawdown_outcome`, `firm_kwargs` and `FIRM_RULES` imported through the `sys.path` bootstrap; C2 requires both successful construction and a null drawdown outcome under the tier geometry; `valid_until` derived from the C5 window in `America/New_York`; atomic write (temp file + `os.replace`); exit code 0 on seal, 2 on refusal; stdout = sealed-file SHA-256 + passed check ids + `valid_until` + the attested-not-verified sentence; stderr = failing check ids only.
- **Consumer acceptance (TB-E2 / TB-B10, outside this tool footprint):** reject consumption at or after `valid_until` or after intervening account activity; require recapture, reseal, rerun and renewed dependent approvals with matching seal/result digests. A fresh seal paired with an old n3 result must fail.
- **2.3 Independent oracle**: one test recomputes `historical_eod_peak` and the C6 ratio with `fractions.Fraction` from the synthetic fixture and compares to the tool's output.
- **2.4 Run** `python -m pytest tests/test_seal_account_snapshot.py -q` and `make check`; record both outputs in the PR body.

## §4 — Hypothesis and gate

**H:** the B7 snapshot boundary can be bound to the three evidence files by mechanical checks alone (C1–C10), so that a sealed file exists only when every check passed and the seal carries no value the evidence does not.

**Revert trigger (binary):** **Reject (FALSIFIED) if** any check C1–C10 cannot be implemented from the three evidence files as the contract defines them — then return `BLOCKED — plan-itself-wrong` naming the check and change nothing. **Accept (RESOLVED) if** every C1–C10 refusal has a named failing test that passed only after the implementation, both synthetic seals produce the contract's JSON shape, `make check` is green, and no test fixture, log line or PR body carries a live account value.

## §5 — Forbidden moves

- Reconstructing or defaulting any field (peak from statements, basis from balance, trade days from dates).
- Reading Tradovate, Tradeify, CrossTrade or the rail hosts; this tool is offline and file-bound.
- Relaxing a frozen default via CLI; widening the evidence set; sealing without E3; inventing adjustment or rebasing semantics for a non-zero `cash_adjustments_total`.
- Using any real account value, screenshot or statement as a fixture; synthetic values only.
- Touching `core/`, `ops/`, `docs/` beyond the two footprint files.

## §6 — Return (umbrella §6 taxonomy)

```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Packet: TB-T1   Branch: codex/tb-t1-snapshot-sealer   Base: <sha of origin/main at cut>
Per-step gates: 2.1 [..], 2.2 [..], 2.3 [..], 2.4 [..]
Diffs (files touched): scripts/seal_account_snapshot.py · tests/test_seal_account_snapshot.py
Private outputs (paths only, no values): none
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

**File ownership (exact):** `scripts/seal_account_snapshot.py` (new) · `tests/test_seal_account_snapshot.py` (new). **Reusable components:** `EvaluationState`, `_drawdown_outcome`, `firm_kwargs`, `FIRM_RULES`, `require_finite_number`, `dump_strict_json`. **Dependencies:** none pending (contract fixed 2026-09-12). **Non-goals:** the live capture, TB-B7's execution fingerprint, any n3 run, any change to the kernel. **Stopping condition:** the §4 gate reads RESOLVED, or a `NEEDS_CONTEXT` / `BLOCKED` return is posted; no second design pass without the coordinator.

## §10 — Audit hooks (runnable)

```bash
python -m pytest tests/test_seal_account_snapshot.py -q            # expected: all pass
git diff --name-only origin/main...HEAD                             # expected: exactly the two footprint files
git log origin/main..HEAD --name-only --pretty=format: | grep -Ei 'png|jpg|csv|statement' ; echo "exit=$?"   # expected: exit=1
grep -rnE '\$ ?[0-9]{2,3},[0-9]{3}' tests/test_seal_account_snapshot.py | grep -v -E '100,000|106,000|3,000|2,400' ; echo "exit=$?"   # expected: exit=1 (tier constants only)
```
