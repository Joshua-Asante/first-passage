**Theme:** legacy
**Status:** ACTIVE — SPX500 turn-of-month Layer-A inference harness
# Q-TOM-SPX-1 - SPX500 turn-of-month (Layer-A inference harness)

Layer-A existence/persistence harness for **Q-TOM-SPX-1** (does a tradeable
turn-of-month edge exist in SPX500 daily returns?). Classifies daily
close-to-close returns by trading-day-of-month (forward count, matching
`tom_test_spx500.pine` exactly) and runs the selection-test battery the brief
§6 gate references. Mechanism: Etula et al. 2020 "dash-for-cash" month-end
liquidity (deliberately independent of any hawkish-regime thesis - the
source-diversity discriminating test from the 2026-06-10..14 audit).

> **Status: `DEAD` 2026-08-23.** Layer A RESOLVED-ABSENT on the canonical
> Pepperstone feed (2026-06-16). The frozen existence battery hard-failed
> (Welch t=0.64, permutation p=0.2544, COVID concentration, halves sign
> reversal). Reserved native Pine confirmation unpaid and not reserved.
> Do not rerun wider windows or change thresholds. See
> [`closure`](../../../docs/briefs/closures/Q-TOM-SPX-1-closure-dead.md),
> [`docs/briefs/Q-TOM-SPX-1.md`](../../../docs/briefs/Q-TOM-SPX-1.md) and the
> [SPX500 ledger](../../../ops/instruments/SPX500.md).

## Two-layer measurement (read before interpreting any result)

1. **Layer A - existence.** Window-day vs off-day mean daily return, with
   label-permutation, bootstrap, drop-top-k-months, and halves stationarity.
   Captures the FULL effect including the structurally-untradeable T+1 day move.
2. **Layer B - capturability.** Per-trade tradeable return (enter close
   T+start, exit close T+end) minus cost vs the 4x cost-law hurdle. The
   diagnostic-minus-strategy gap (concentrated in T+1) is a result, not a bug.

## Feed & scope (load-bearing - 2026-06-15 operator decision)

- **SPX500 is an INDEX CFD.** Per
  [`docs/adr/2026-06-12-rnd-feed-instrument-class-split.md`](../../../docs/adr/2026-06-12-rnd-feed-instrument-class-split.md)
  §Decision, **Dukascopy index symbols are EXPLORATORY-ONLY, NEVER GATE-BEARING**
  for SPX-class R&D - a structurally different instrument from the Pepperstone
  SPX500 CFD (basis/session/funding differ; index feed divergence demonstrably
  bites, DJ30 ECR 2026-05-25). **The CANONICAL verdict comes from the Pine
  harness on the TV/Pepperstone SPX500 feed.** This Python/Dukascopy path is an
  exploratory cross-check that can generate hypotheses but cannot gate the concept.
- **Persistence-only (Q1).** The canonical Dukascopy `USA500IDXUSD` history
  starts ~2011, so the literature pre/post-2001 **decay** split cannot be
  populated here. The harness reports decay **UNTESTED** (not a silent pass -
  see the 2026-06-15 vacuous-gate fix) and the verdict speaks to **current
  (post-2011) persistence only.** Decay is testable only on a long-history TV
  feed via the Pine harness.

## The §6 gate (frozen in the brief; do not change)

Existence (`diff>0` AND perm p<0.05 AND survives drop-top-k AND both halves >0)
-> persistence (Welch `t>=2.0`) -> capturability (gross expectancy >= 4x
round-trip cost). Hard-absent if `diff<=0` / perm p>=0.10 / t<1.0 / drop-top-k
flips sign. Window mechanism-anchored at `[1:3]` (Lakonishok-Smidt classic) -
**NOT swept** (degrees-of-freedom hazard). Changing any frozen threshold
(`--split-year` / `--window` / perm-alpha / t-cut / hurdle) VOIDS the verdict
(trap #12) - close AMBIGUOUS and open a fresh brief.

## Files

- `q_tom_spx_1.py` - the Layer-A inference + §6 verdict (self-contained; numpy+pandas).
- `test_verdict.py` - pins the §6 gate logic, incl. the decay-untested-is-not-a-pass regression.
- `fetch_daily.py` - EXPLORATORY-ONLY Dukascopy daily fetch (exists-guarded; not run this session).
- `README.md` - this file.
- `tom_test_spx500.pine` - the CANONICAL concept-stage TV harness (gitignored per `**/*.pine`; run on TV/Pepperstone SPX500). **Hash-pinned in `PINE_MANIFEST.sha256`** (2026-06-16) so this gate-bearing instruction stays verifiable even though the source stays gitignored - the original authoring copy was found unrecoverable and was reconstructed from the operator paste; verify before relying on a copy.
- `PINE_MANIFEST.sha256` - committed SHA256 pin of `tom_test_spx500.pine` (LF-normalized). Verify: `sha256sum -c PINE_MANIFEST.sha256` (LF copy) or the CRLF-robust python one-liner in its header.

## Reproduce

**Canonical (do this first):** load `tom_test_spx500.pine` on a **daily**
TV/Pepperstone (or US500) SPX500 chart with maximum history. The diagnostic
table reports window vs off means split at the decay year; the strategy equity
shows the real-time-capturable piece. This is the gate-bearing measurement.

**Exploratory cross-check (Dukascopy; never gate-bearing):**

```bash
# 1. fetch the daily panel (heavy tick pull; or resample the NOCT M15 panel)
python lab/analysis/tom_spx/fetch_daily.py \
    --out core/data/bar_data/USA500IDXUSD_D1.csv --start 2011-09-18 --end 2026-06-15
# 2. Layer-A inference (no --cost-pct -> capturability PENDING)
python lab/analysis/tom_spx/q_tom_spx_1.py --series core/data/bar_data/USA500IDXUSD_D1.csv
# 3. tests
python -m pytest lab/analysis/tom_spx/test_verdict.py -q
```

## Provenance / lineage

- **Prior SPX500 state (collision note).** `CONCEPT-NOCT-SPX-001`
  (inventory-reversal-immediacy-premium) was **FALSIFIED 2026-06-07** on the
  same Dukascopy `USA500IDXUSD` feed -
  [`lab/analysis/noct_spx/CARD.md`](../noct_spx/CARD.md),
  [`docs/rejected_candidates.md`](../../../docs/rejected_candidates.md). NOCT
  predates the 2026-06-12 index-class ADR, so its Dukascopy-index use was
  pre-policy. TOM is a **different mechanism** (turn-of-month / dash-for-cash,
  not overnight inventory reversal) - admissible, not a duplicate - but it
  inherits NOCT's infrastructure (point_factor=1e3, DST map) and the
  unknown-SPX500-cost finding (no recorded FXIFY/Alchemy spread).
- Source: claude.ai Tech-Advisor concept package (ledger + harness + Pine),
  landed and Rule-0-corrected by Claude Code 2026-06-15.
