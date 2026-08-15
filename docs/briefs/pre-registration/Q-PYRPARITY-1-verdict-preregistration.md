# Pre-registration — Q-PYRPARITY-1 (WATCH-1 pyramid-proportionality verdict)

**Status:** FROZEN 2026-07-17, before Phase 0 (Pine read) or Phase 1 (TV runs) has executed.
**Parent brief:** [`docs/briefs/Q-PYRPARITY-1-watch1-pyramid-proportionality.md`](../Q-PYRPARITY-1-watch1-pyramid-proportionality.md)
**Loop of record:** INNER (single TV observation, mechanically verified)
**Authored:** 2026-07-17 · Claude Code, operator-ratified same day.

---

## §0 — Rule-0 reads

Inherited by reference from the parent brief's own §0 — not re-derived here. Load-bearing anchors: `docs/methodology/strategy_lifecycle.md:113` (the OPEN claim under test, anchor `83ba1b2`); `core/strategies/striker/striker_dj30_v4.5.pine` (sha `716f8b43…`) and `core/strategies/nas/striker_nas100_v1.pine` (sha `f5a567b5…`), both verified present on local disk 2026-07-17 (gitignored but readable in this session — citation-chain mode not required); `core/config/params.toml` (anchor `784a9ab`) lines 69/94, `pyramid_pct = 750.0` / `1000.0`.

---

## §1 — Context (one line)

c1's ratified WATCH-1 (0.50×) haircut applies to exactly the two pyramided legs (Striker DJ30, Striker NAS100); whether halving the risk% input halves the whole pyramided stack — base and adds alike — was left an open TV-observation item at lifecycle-governance authoring and is now load-bearing for deployment.

---

## §4 — Falsifiable hypothesis (frozen verbatim from the parent brief)

**H-PYRPARITY-1:** Halving the risk% input produces a per-trade executed-quantity ratio of 0.500 for **both** cohorts (base entries AND pyramid adds), with identical signal timing, on both legs.

**Protocol statistic (branch selected at Phase 0, recorded below once known — NOT yet selected as of this freeze):**
- **Branch A** (sizing basis = initial-capital, non-compounding): per-fill qty ratio `qty(r0/2) / qty(r0)` on entry-time-paired fills.
- **Branch B** (sizing basis = strategy.equity, compounding): per-fill **normalized** qty ratio `[qty/equity](r0/2) / [qty/equity](r0)`, equity taken at entry, removing the compounding-feedback confound.

**Branch selected (Phase 0 output — RECORDED 2026-07-17, before any TV export opened):** **Branch B** (equity-normalized ratio). Both locked sources size base off `strategy.equity` (`calcSize`: `risk = strategy.equity * (riskPerTrade/100)`; DJ30 `:149-151`, NAS100 `:202-204`) — rolling-equity, compounding — so raw qty ratios drift from 0.500 post-first-trade and must be equity-normalized. Full Phase-0 read + the source-side structural corroboration (base and add both exactly linear in `riskPerTrade`, no floor/cap/round/min-qty on the sizing path; add normalizes on **entry-bar** equity because `addSize = initialSize·pyramidSize%` and `initialSize` is captured at entry): [`lab/archive/q_pyrparity_1_2026-07/PHASE0.md`](../../../lab/archive/q_pyrparity_1_2026-07/PHASE0.md).

**Accept (`RESOLVED-PROPORTIONAL`) if:** on BOTH legs and BOTH cohorts (base / adds) separately — ≥95% of paired fills have statistic within **0.500 ± 0.02**, median within **0.500 ± 0.005**, AND entry/exit timestamps identical run-to-run.
**Reject (`FALSIFIED-NONPROPORTIONAL`) if:** either cohort's median statistic falls outside 0.500 ± 0.02 on either leg, OR the add cohort's fill count drops run-to-run.
**Ambiguous-hold if:** trade lists misalign for reasons other than clipped adds, or TV min-qty rounding makes the tolerance undecidable at the tested account size (one permitted re-size at a larger test account, then decide).

These numbers are FIXED as of this freeze. Any change requires closing this pre-registration and opening a fresh one (Known Trap #12 — no in-place amendment after data is seen).

---

## §5 — Forbidden moves (inherited by reference from the parent brief)

- **Editing the locked Pine to expose a sizing hook** — parameter axis immutable; observe, don't instrument.
- **Substituting a CFD-symbol test for the CME panel-of-record test** — CFD is optional corroboration only, labeled as such; the deployment surface is MYM1!/MNQ1!.
- **Aggregating base+adds into one ratio** — the edge lives in the adds; cohort-split is mandatory.
- **Accepting a near-miss to keep Q-RAIL-1 moving** — the documented account-multiplier fallback exists precisely so a FALSIFIED here is cheap.
- **Automating the TV runs** — no TV backtest API; operator-executed only, 4 runs total.

---

## §6 — Gate criteria (frozen verbatim)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED-PROPORTIONAL` | §4 accept bands met on both legs × both cohorts | `strategy_lifecycle.md:113` flips to CONFIRMED (dated); Q-RAIL-1 F1 = PASS via risk-input scaling |
| `FALSIFIED-NONPROPORTIONAL` | §4 reject fires on any leg/cohort | Apply the documented fallback: WATCH-1 haircut at the account-multiplier layer for the two pyramided legs; Q-RAIL-1 F1 = PASS-via-fallback; re-opens the multiplier-spine forward-relevance flag in the affirmative |
| `AMBIGUOUS-HOLD` | Misaligned trade lists (non-add-clipping) or undecidable rounding after the one permitted re-size | Route to a Pine-behavior look (fresh Q); Q-RAIL-1 F1 = BLOCKED-ON-INPUT |

---

## §7 — Freeze list

1. Tolerance bands: 0.500 ± 0.02 (per-fill), 0.500 ± 0.005 (median) — FIXED.
2. Cohort split mandatory (base vs adds, never aggregated) — FIXED.
3. Panel-of-record charts: CBOT_MINI:MYM1! 15m / CME_MINI:MNQ1! 15m, same settings/date range as the sha-pinned scoring exports (`15d8b` / `beabf`) — FIXED.
4. Branch selection (A vs B) happens at Phase 0, recorded in §4 above, before any TV export opens — process FIXED, outcome pending.
5. No TV automation — operator-executed, 4 runs total (2 legs × 2 risk settings) — FIXED.

---

## §10 — Audit hooks (runnable)

```bash
# This pre-registration predates any TV export (Trap #12 guard)
git log --oneline -- docs/briefs/pre-registration/Q-PYRPARITY-1-verdict-preregistration.md | tail -1

# The claim under test still reads OPEN until Q-PYRPARITY-1 actually closes
grep -n "OPEN — Pine pyramid-parity" docs/methodology/strategy_lifecycle.md

# Locked sources unchanged since freeze
git log -1 --format='%h %cs' -- core/strategies/striker/striker_dj30_v4.5.pine core/strategies/nas/striker_nas100_v1.pine

# The executing session cites this pre-registration (Trap #10)
grep -rn "Q-PYRPARITY-1-verdict-preregistration" docs/SESSIONS.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/pre-registration/Q-PYRPARITY-1-verdict-preregistration.md --type generic
git log -1 --format='%h %cs' -- docs/methodology/strategy_lifecycle.md core/config/params.toml
```
