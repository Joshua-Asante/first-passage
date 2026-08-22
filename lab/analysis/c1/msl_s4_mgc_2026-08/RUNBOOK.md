# MSL-S4 RUNBOOK — MGC expiry-OI-strike convergence (operator TV backtest, charter step 7)

**Chokepoint rule (charter step 7, quoted):** *"the runbook must link the step 2–5 artifacts
(dedup block · door-check record · screens table · G0 PR#) and the operator refuses the TV seat if
any is missing."* This runbook links what exists and **explicitly flags what does not**, so nothing
reads as a silently missing link.

## Links to steps 2–5

| Artifact | Link | Status |
|---|---|---|
| Dedup block (step 2) | [`STAGE1.md`](STAGE1.md) §Step 2 | present — three `rg` commands, output pasted |
| Door-check record (step 2) | [`STAGE1.md`](STAGE1.md) §Step 2 (`instrument_profiles.py cell` output) | present |
| $0 screens table (step 3) | [`STAGE1.md`](STAGE1.md) §Step 3 | present — cost-law/payability/survival all PASS |
| Cheap falsifier (step 4) | [`STAGE1.md`](STAGE1.md) §Step 4 | **NOT AVAILABLE** — no market-data access this session, disclosed, not silently skipped |
| G0 freeze (step 5) | [`PREREG_G0.md`](PREREG_G0.md) | present — FROZEN 2026-08-21 |
| Explore-confirm (step 5a) | — | **DEFERRED BY OPERATOR OVERRIDE** — [`PREREG_G0.md`](PREREG_G0.md) §0a. No `SHAPE-CLEAR` verdict exists. Your TV backtest is the first empirical look at this construct, not a second one. |
| G0 PR# | *(fill in once this branch's PR is opened — see the session's own commit)* | — |

**Before you take the TV seat:** the deferred Explore-confirm step means no one has checked this
construct against real price/OI data yet — not a $0 arithmetic screen, not a delete/flip test, not
even a 5-minute cheap falsifier. Your backtest is genuinely the first evidence. That was an
explicit choice you made this session (trading Explore-confirm's discipline for speed), not an
omission — but it means the ordinary caution applies at full strength: a good-looking TV curve
here has had zero prior filtering, unlike every other MSL card's TV run.

## The Pine file

**File:** `expiry_oi_strike_convergence_mgc_v0_1.pine` (sent to you directly as a file this
session — check your downloads / the file the assistant sent). `pine_lint.py` run clean, 13/13
checks PASS, targeted at `core/strategies/candidates/expiry_oi_strike_convergence_mgc_v0_1.pine`.

**Why it isn't committed to the repo:** `**/*.pine` is gitignored by design (public-clone posture,
`CLAUDE.md`) — only `core/strategies/MANIFEST.sha256` hash-pins are tracked, never the source
itself. This session ran in an ephemeral cloud container. Writing the `.pine` under
`core/strategies/` and hash-pinning it *from this session* would create exactly the failure this
repo's own `check_pine_manifest.py` was built to catch — a manifest pin whose bytes exist only on
a machine that is about to disappear (`docs` for that gate cite two real past incidents,
`fd91f37b…` and `bad8068d…`, both cloud/ephemeral pins that went unrecoverable). So this session
deliberately did **not** place the file under `core/strategies/` or touch `MANIFEST.sha256`.

**What to do with it (on your durable local checkout):**
1. Save the file to `core/strategies/candidates/expiry_oi_strike_convergence_mgc_v0_1.pine`.
2. Compute its hash and add the line to `core/strategies/MANIFEST.sha256` (matching the existing
   format: `<64-hex-sha256>  core/strategies/candidates/expiry_oi_strike_convergence_mgc_v0_1.pine`).
   `sha256sum core/strategies/candidates/expiry_oi_strike_convergence_mgc_v0_1.pine` on
   Linux/macOS, or `certutil -hashfile ... SHA256` on Windows — or just ask a local (non-cloud)
   Claude Code session to do it; the pin-provenance gate accepts a pin from your durable machine.
3. Update `core/strategies/candidates/candidates_CARD.md`'s disposition and hash-pins section
   (currently `FALSIFIED_PARKED` / `(none)` — this candidate is neither yet).
4. Run `python3 scripts/pine_lint.py core/strategies/candidates/expiry_oi_strike_convergence_mgc_v0_1.pine --target-path core/strategies/candidates/expiry_oi_strike_convergence_mgc_v0_1.pine` locally to reconfirm before pasting into TV (compile gate — TV itself is the real gate per the CE10237 precedent, `pine_lint` only catches what TV would reject anyway).

## Exact inputs for the TV backtest

| Input | Value / source |
|---|---|
| Chart | **MGC1!** (continuous Micro Gold futures), or a specific front-month contract matching the tested expiry cycle |
| Chart timezone | **America/New_York** (script inputs are ET-based; TV chart TZ must match or the session-flat/window logic misfires) |
| Bar interval | Intraday (1m or 5m recommended for entry precision within the arm window; the construct's own logic is date/level-driven, not TF-sensitive beyond needing intraday resolution for the session-flat check) |
| `Options expiry date (window anchor)` | The last-trading-day timestamp of the Gold options cycle under test — read from CME's Options Calendar. **Set this per cycle you test; do not leave the script default.** |
| `Arm window: sessions before expiry` | Design default **3** — sweep {1, 2, 3} per `PREREG_G0.md` §3 as robustness probes, not for selection |
| `Highest-OI strike (GC/OG, $/oz)` | Read from CME's **Options Settlement Tool** or **OI Heatmap** (`cmegroup.com`) for the prior session, for the expiry cycle under test. **This cannot be computed by the script — it is your manual per-cycle input.** Not available via any TradingView built-in. |
| `Min displacement from strike to arm (pts)` | Design default **3.0** — sweep {2, 3, 5} per `PREREG_G0.md` §3 |
| `ATR length (stop reference)` | Design default **14** |
| `Stop = ATR x` | Design default **1.5** |
| `Target R:R (of stop distance)` | Design default **2.0** |
| `Session-flat hour/minute (ET)` | **16 / 45** (Tradeify Select verified deadline) |

## Data-source procedure (per expiry cycle you test)

1. Pick a past Gold options expiry (weekly or monthly) inside your backtest window.
2. From CME's Options Settlement Tool or OI Heatmap, pull the OI-by-strike snapshot for the
   session **before** the arm window opens (i.e., 3+ sessions before expiry, matching the design
   default) — note the strike with the largest open interest.
3. Set the script's `expiryTimestamp` input to that cycle's expiry date-time and `strikeLevel` to
   the strike you read off.
4. Run the backtest over a window that covers just that cycle's arm window (or string several
   cycles together manually — the script's own k=1-per-window latch resets whenever you change
   `expiryTimestamp`, so running several cycles back-to-back on one chart requires updating the
   input between cycles, which TV's Strategy Tester does not automate; a multi-cycle backtest
   needs either several single-cycle runs or a Cursor/local script wrapping this — out of scope
   for this session).

## What this backtest can and cannot tell you

**Can:** whether the construct, as specified, produces trades that look directionally sane on
real MGC price action around real expiry cycles — the first real signal on whether the mechanism
story holds up outside pure reasoning.

**Cannot (without more work):** a statistically rigorous verdict. One or a few TV-eyeballed cycles
is not the session-block bootstrap CI, delete/flip test, or DSR-at-K check that Explore-confirm
would have run. Treat a good-looking curve as "worth building the deferred Explore-confirm
harness for," not as "done."

## Next steps after your TV run

- **If it looks dead on sight** (no real trades, obviously wrong-signed, or contradicts the
  mechanism story) — report back; this closes the card cheaply, same as any other MSL Explore
  kill, just discovered via TV instead of a script.
- **If it looks live** — the next owed step is the deferred Explore-confirm: get a real MGC/GC
  panel (Databento pull, cost estimate first) and run the delete/flip test properly before any
  further build-out. A promising TV eyeball is not survivor-MC-ready.
