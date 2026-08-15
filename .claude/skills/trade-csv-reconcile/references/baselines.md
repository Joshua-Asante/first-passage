# Pine-header Baselines — Lock-of-Record

This file is the cached anchor for `scripts/reconcile.py --baseline`. It must
be kept synced to the most recent strategy lock. The authoritative source is
the Pine source on disk; this file is a cache for fast reconciliation.

**Last synced:** 2026-06-04 (post 2026-05-23 allocation-refresh-2; CSV vintage 2026-05-24).

> ⚠ **DORMANT 2026-08-08 — the sync procedure is retained in full, but its trigger cannot currently fire.**
> These anchors are **CFD-era and gross-of-swap** (M-SWAP-1: the TV backtest engine does not model overnight
> financing), and the four locked strategies have **no live venue**. Step 1 — a fresh strategy-tester run on the
> canonical feed — is **not currently possible**: the Pepperstone feed retired 2026-08-02 and the panels are
> usable but **not regenerable**.
>
> **Do not delete steps 1–4.** Step 2 is the **only** written statement in the repo that the `STRATEGIES` dict
> embedded in `scripts/reconcile.py` must be updated in the same motion as this markdown — deleting it would turn
> a documented drift hazard into an undocumented one.
>
> **Re-arm condition:** a re-lock landed under a fresh admitting ADR via the standing change-control chain
> (pre-registration → re-MC → both-halves regime gate → ADR). A re-lock is **dormant, not foreclosed** — the
> 2026-05-23 allocation refresh is the in-repo precedent for one landing without a version bump. On re-arm,
> steps 1–4 apply **in full**.

> **Repo copy.** This is the in-repo canonical cache at the path CLAUDE.md
> references. The `trade-csv-reconcile` skill is also installed as a plugin with
> its own `references/baselines.md` — `scripts/reconcile.py --baseline` reads the
> *plugin* copy, so until that copy is updated too, a `--baseline` run will report
> DRIFT against the pre-2026-05-23 anchors it still holds. Keep the two in sync on
> every re-lock.

> **2026-08-14 — parameter/backtest values redacted from the public tree.** This file's per-strategy
> Pine-config blocks and PF/WR/Net/DD tables (below, and their archival predecessors) are redacted per
> [`docs/adr/2026-08-14-repo-public-visibility-transition.md`](../../../../docs/adr/2026-08-14-repo-public-visibility-transition.md)
> — same pass that redacted `core/strategies/_archive/*/LOCK.md`. The private operational archive holds
> the literal values; `scripts/reconcile.py --baseline` reads them from the private copy, not this one.

When a strategy is re-locked:
1. Read the new Pine source headers (Net / PF / WR / DD / N from a fresh
   strategy-tester run on the canonical feed).
2. Update the matching block below + the `STRATEGIES` dict in `reconcile.py`.
3. Note the lock date.
4. Re-run `reconcile.py --baseline` against the post-lock CSV to verify the
   anchor reproduces.

**DD convention:** values below are **trade-close** drawdown on the cumulative-P&L
curve (initial $200K, append each trade's realized Net P&L, peak-to-trough) — the
same reconstruction `reconcile.py` computes. This differs by design from
TradingView's intra-trade (intrabar) max DD; do not cross-compare the two.

---

## Locked allocations / protection / MC pin (mirrors — not owned here)

**Rule 7:** risk% / versions → [`CLAUDE.md`](../../../../CLAUDE.md) §Strategy Reference · `core/firm_rules.py` `_BASE_RISK`.
`dd_protection` literals → `core/dd_protection.py` · CLAUDE §Protection.
Portfolio MC pin → [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md) · CLAUDE historical headline · engine `tests/core/test_mc_synthetic_engine.py`.
Allocation-refresh ADR: [`2026-05-23`](../../../../docs/adr/2026-05-23-allocation-refresh-2.md).

This file's job below is **per-strategy Pine-header PF/WR/Net/DD/N** for `reconcile.py --baseline` — not a second home for portfolio risk constants.

---

## Guardian Gold v5.5 🔒 LOCKED 2026-04-23 (allocation unchanged)

**Pine config:** redacted from the public tree — see the private operational archive.

**1R basis:** median loss (architecture: trend-rider, no BE).

Baseline PF/WR/Net/DD/N table and archival vintages: redacted from the public tree — see the
private operational archive. Reproduces the CLAUDE.md baseline anchor (values not restated here).

**Notes:**
- v5.5 delta from v5.4: two hour-block inputs flipped TRUE (all other logic unchanged) — see the
  private archive for the exact flags.
- XAUUSD has feed-specific stop-proximity drift between Pepperstone and OANDA.
- The `Guardian n=209` figure in some legacy Notion artefacts is a stale anchor.

---

## Striker DJ30 v4.5 🔒 LOCKED 2026-05-05 (allocation-refresh-2 2026-05-23: risk 0.75%→0.70%, pyramid 500%→750%)

**Pine config:** redacted from the public tree — see the private operational archive.

**1R basis:** full-stop mean (|loss| > 1% of account, fallback to median if n=0).

Baseline PF/WR/Net/DD/N table and archival vintages: redacted from the public tree — see the
private operational archive.

**Pyramid share:** load-bearing to the strategy's return profile (Q-DJ30-2 Phase B 2026-05-06 —
base entries are themselves edge-bearing, so pyramid dependence is sub-majority but structural).
NOTE: `reconcile.py`'s pyramid-share detector read 0% on the 2026-05-24 export vintage — a
leg-classifier/CSV-format quirk, not a P&L issue (Net sums correctly from Exit rows; PF/Net/DD
reconcile). Investigate the detector before relying on pyramid_pnl_share from this vintage.

**Cross-feed contract-spec note:** OANDA US30.pro is $5/pt; Pepperstone US30 CFD is $1/pt.
Pine `calcSize` does not account for per-point value, so 5× dollar deltas on identical
trade selection are mechanical, not signal drift.

---

## Striker NAS100 v1 🔒 LOCKED 2026-05-05 (allocation-refresh-2 2026-05-23: risk 0.45%→0.37%, pyramid 1000% unchanged)

**Pine config:** redacted from the public tree — see the private operational archive.

**1R basis:** full-stop mean (|loss| > 1% of account, fallback to median if n=0).

Baseline PF/WR/Net/DD/N table and archival vintages: redacted from the public tree — see the
private operational archive.

**Pyramid share:** load-bearing (Q-NAS-1 2026-05-05). NOTE: same pyramid-share detector 0%
quirk as DJ30 on the 2026-05-24 vintage — leg-classifier/CSV-format issue, not P&L.

**Architectural finding (2026-05-05):** Aegis-style SHORT mirror falsified (direction-asymmetric
by structure). NAS100 stays long-only. Do NOT re-test without new mechanism evidence.

---

## Aegis-Reversion USDJPY v4.3 🔒 LOCKED 2026-04-22 (allocation unchanged)

**Pine config:** redacted from the public tree — see the private operational archive.

**1R basis:** full-stop mean (|loss| > 1% of account, fallback to median if n=0).

Baseline PF/WR/Net/DD/N table and archival vintages: redacted from the public tree — see the
private operational archive.

**Lock-of-record header panel (distinct from the CSV vintage above — 2026-07-05 clarification):**
the v4.3 Pine header (sha256 `d8c1188…` = `MANIFEST.sha256`, read 2026-07-05) carries a lock-time
panel figure set distinct from the table row's later re-export vintage — both are correct for
their own panel; cite whichever with its vintage, never mix. Values redacted from the public tree.

**USDJPY broker-uniform:** trade selection is broker-invariant across feeds; only spread/slippage
differs (Pepperstone vs OANDA).

**BE logic IS the edge:** a substantial share of winners are BE-manufactured.
**Binary-event pause rule applies** (BOJ, central-bank decisions) — manual, not a Pine condition.
**Regime risk:** USDJPY range-regime sensitive; 2022 was a materially weaker year.

---

## Cross-feed reconciliation table

| Strategy | Trade selection invariance | Dollar P&L delta source |
|---|---|---|
| Guardian XAUUSD | Within ±5% N across feeds | Stop-proximity slippage |
| Striker DJ30 | Within ±5% N across feeds | OANDA $5/pt vs Pepperstone $1/pt → 5× delta on identical trades |
| Striker NAS100 | Cross-feed validated 2026-05-24 (4-strategy parity) | Contract-spec (NAS100 +Net OANDA vs Pepperstone) |
| Aegis USDJPY | **Near-identical** trade counts | Spread/slippage only |

If WR or N drifts >5% across feeds for the same strategy/version, suspect feed
mislabel before suspecting strategy divergence.

---

## Versioning & change-log

Figures in the original change-log entries below are redacted from the public tree
(2026-08-14) — the provenance/methodology narrative is preserved, exact numbers live in the
private archive.

- 2026-07-05: **Aegis anchor-provenance correction note** (CC-HANDOFF-AEGIS-6J §2.6; NEVER
  silently re-baseline — no numbers changed, provenance clarified). Three figure sets were in
  circulation with different vintages/provenance (Pine header lock-of-record vs. this file's table
  row vs. a stale claude.ai-side skill-copy anchor that mixed in Guardian's DD by cross-strategy
  contamination). The stale anchor is retired; per the source-of-truth hierarchy the Pine header
  wins for lock-of-record, the table row remains the current-vintage reconcile anchor.
- 2026-06-08: corrected pyramid-share **expected** values for DJ30 and NAS100 (Q-DJ30-2 Phase B
  2026-05-06 corrected a cross-strategy misattribution; Q-NAS-1 retained its estimate). Mirrors the
  trade-csv-reconcile `SKILL.md` Step 4 correction same date. Sizing-risk %s unchanged.
- 2026-06-04: **repo copy created**; baselines synced to the 2026-05-23 allocation-refresh-2
  lock at the 2026-05-24 CSV vintage. Values computed via `scripts/reconcile.py` per-strategy
  reduction. dd_protection updated to C2 (0.015/0.40); MC anchor updated to 99.83/0.17/4.37.
  Plugin copy still on the 2026-05-06 anchor (update separately so `reconcile.py --baseline`
  reconciles).
- 2026-05-23: allocation-refresh-2 — DJ30 0.75%→0.70% pyr 500%→750%; NAS 0.45%→0.37% pyr 1000%.
- 2026-05-08: dd_protection relocked C0→C2 (0.010→0.015 trigger, 0.40 scale).
- 2026-05-06: file authored (plugin); baselines synced to 2026-05-05 4-strategy lock.
- 2026-05-05: Striker DJ30 v4.5 + NAS100 v1 LOCKED; portfolio MC re-anchored.
- 2026-04-23: Guardian v5.5 LOCKED; risk re-locked 0.30%→0.34%.
- 2026-04-22: Aegis v4.3 LOCKED (EOM filter).
