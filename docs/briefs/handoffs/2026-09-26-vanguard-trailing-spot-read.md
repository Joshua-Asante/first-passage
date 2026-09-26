# Vanguard trailing return: spot-read for disposition caveat 1 (bounded local handoff)

**Status:** DRAFT, ready to dispatch once committed. It is read-only and needs no new authority beyond [campaign §60](../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25). It runs only in the operator's primary checkout. Record the dispatch revision in §4.

**Selected outcome:** discharge or refute caveat 1 of the [draft coordinator disposition](2026-09-26-vanguard-mgc-trailing-determination.md#5-executor-return). The question is whether the private `file:line` citations behind `TRAILING ACTIVE` say what the return claims. The answer is one of `CONFIRMED`, `DISCREPANT` (with the exact rows) or `BLOCKED` (with the missing file or mismatched hash).

**Why:** the disposition checked the public loader path. It could not re-read the private port and Pine, because the cloud clone has neither. Acceptance needs either this spot-read or an explicit reliance note from the coordinator.

**Scope:**
- **In scope:** reading, hashing and reporting.
- **Out of scope:**
  - importing, executing or backtesting anything;
  - editing any file except §4 of this packet;
  - copying private files anywhere;
  - re-deriving the runtime digest (the return already did that);
  - re-deciding the verdict beyond the rows below;
  - touching caveats 2–4.

**Ownership:** one local executor, named at dispatch. The coordinator records acceptance in the determination's disposition. The operator then decides between the edition and rejection.

## 1. Before reading

1. Run `.\fp.ps1 doctor` in the primary checkout. Record the revision and tree state.
2. Hash both files in place and compare them with `core/strategies/BOOK_SOURCES.sha256`:
   - Pine `core/strategies/book/Vanguard_Gold_MGC_v0.4_venue_bound.pine`, expected `af26899c…`;
   - port `ops/c1_signal_daemon/ports/vanguard_mgc.py`, expected `e6a03d04…`.
3. If either hash mismatches, stop with `BLOCKED — hash`.
4. Confirm that the pinned `effective_inputs.json` (`66406dee…`) has an **empty** `vanguard_mgc.adapter` object. That fact is what makes the port's defaults the effective binding.

## 2. Rows to check

Line numbers come from the return. If a line has moved but the same construct exists at a nearby line, record the actual line and mark the row `CONFIRMED (moved)`. Judge the construct, not the line number.

| # | File | Cited | Claim to confirm |
|---|---|---|---|
| P1 | port | `:175-181` | The bracket construction sets both trailing fields when the trailing switch is enabled, and leaves them unset otherwise |
| P2 | port | `:253`, `:269`, `:274` | That construction is used for entry, scale-in and the managed-bar amend. List any **other** bracket construction path that bypasses it. |
| P3 | port | `:69-71` | The default binding enables the trailing switch, with non-zero trailing distances |
| P4 | port | `:291-292` | `build` takes its parameters only from its keyword overrides, with no other source for the trailing switch |
| P5 | port | `:66`, `:60`, `:245`, `:177` | Breakeven is inactive by default. The default activates the stop at entry, so the grace level is unused. |
| G1 | Pine | `:235`, `:237-238` | The default binding enables trailing, with non-zero distances |
| G2 | Pine | `:452-461`, `:499-503` | Every exit on the entry, grace and management paths carries trailing arguments gated on that switch |
| G3 | Pine | `:228`, `:169-171`, `:497` | Breakeven is inactive by default, and grace is inactive, matching the port |

**Discrepancy rule:** a row is `DISCREPANT` if the construct contradicts the claim. Examples: a default differs; a bracket path bypasses the cited construction; the trailing fields are set under a different condition. Only the rows go into the return, not a new verdict. If P1–P4 or G1–G2 are discrepant, note that `TRAILING ACTIVE` may not hold and stop; the coordinator reopens the determination.

## 3. Handling (§60)

- Read the files in place. No scratch copies, extracts, worktrees or external services.
- No source text, identifiers, default values or formulas in §4 (§60). Use `file:line` and behavior-level verdicts only, such as "confirmed: trailing enabled by default".

## 4. Executor return

**Status:** not dispatched.

| Field | Value |
|---|---|
| Executor / dispatch revision | |
| Checkout revision, tree state, `doctor` | |
| Hashes (Pine, port, effective inputs), match or mismatch | |
| Vanguard `adapter` override empty? | |
| P1 | |
| P2 (plus any bypass path) | |
| P3 | |
| P4 | |
| P5 | |
| G1 | |
| G2 | |
| G3 | |
| **Result** (`CONFIRMED` / `DISCREPANT: rows` / `BLOCKED: reason`) | |

**Coordinator use:** on `CONFIRMED`, the disposition records "caveat 1 discharged by spot-read at `<revision>`" and may be accepted. On `DISCREPANT`, the determination reopens.
