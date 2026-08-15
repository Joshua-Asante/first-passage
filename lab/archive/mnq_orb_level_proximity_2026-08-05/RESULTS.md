# `MNQPROX-1` — RESULTS: VOID-TOD-CONFOUND (W6) — arms do not share a time-of-day regime

**Status:** CLOSED — VOID-TOD-CONFOUND (W6) — highest-precedence amended §7 gate; Δ not interpreted. (Catalog stamp CLOSED = archive-owed HOLD; the §7 branch discharged is W6, not W3.)
**Δ is not interpreted.** The accept/reject branches of H-MNQPROX-1 are unreachable under a confounded ToD split; this is a pre-registered stop, not a soft fail.

**Date:** 2026-08-05 · **Pre-registration:** [`PREREG.md`](PREREG.md) freeze → three load-bearing amendments (S4c/W6, operator GO, S4 implementation-precision pin) → Cursor handoff — all before any proximity-contrast quantity. Ordering is git-auditable on `analysis/mnqprox-1-level-proximity-prereg`.

**Cost:** **$0.00.** Level-arm TBBO was **not pulled** (Step 2.2 stop-rule). Parent `events.parquet` rebuilt from the free 1m panel via unmodified `build_events.py` (gitignored cache absent in this worktree). No new estimate/pull beyond the already-authorized S1 window.

---

## Verdict table (amended §7)

| Gate | Fired? | Notes |
|---|---|---|
| **W6 VOID-TOD-CONFOUND** | **YES** | IQRs non-overlap **and** |median gap| = **92.0 min** > 60 |
| W5 VOID-POWER | not reached | n_paired=75 ≥ 30; n_level=75 = 100% of n_ORB |
| W4 VOID-COVERAGE | not reached | (no TBBO read on level arm) |
| W3 / W2 / W1 | not reached | Δ not computed |

---

## Headline numbers (closed list)

| Quantity | Value |
|---|---|
| n_paired sessions | **75** |
| n_ORB moments (paired) | 75 |
| n_level moments (paired) | 75 (one retained touch per paired session after S4a i–iii) |
| orb-only sessions (ledger) | 180 |
| level-only sessions | 0 |
| candidate PDH/PDL scans | 508 |
| retained after S4a i–iii | 75 (drop_near_orb=2, drop_near_trig=5, drop_no_touch=426, drop_no_prev=1) |
| **S4c ORB tod** | median **602.0** · IQR **[600.0, 616.0]** |
| **S4c level tod** | median **694.0** · IQR **[640.0, 771.0]** |
| |median gap| (min) | **92.0** (threshold 60) |
| mean(A_ORB), mean(A_level), Δ, CI, placebo | **not computed** (W6 stop) |

ORB triggers cluster at the post-OR window (~10:00–10:16 ET). Retained PDH/PDL first-touches land later and wider (~10:40–12:51 ET IQR). The designs are not ToD-matched; W6 exists exactly to refuse interpreting that split as ORB-specificity.

---

## What this does NOT say

- It does **not** say the parent's W1 L1 signature is generic approached-level microstructure (that would be W3).
- It does **not** say the signature is ORB-specific (that would be W1).
- It does **not** authorize a re-cut, ToD reweight, alternate level class, τ sweep, or threshold edit (FM-4 / FM-6). A successor that wants an interpretable contrast needs a **fresh freeze** whose level arm is ToD-matched (or otherwise de-confounded) *before* data — not a patch on this cell.
- It does **not** touch F2 / filter conversion / Pine / sizing / the rail.

---

## Limitations

1. **W6 is a design-reachability finding, not a market finding.** The PDH/PDL first-touch definition as frozen systematically samples a later ToD than ORB triggers gated by the opening range.
2. **S4a(iv) never applied** — zero-quote drops require the level-arm TBBO pull, which W6 forbids once confound is known.
3. **Parent `quotes.parquet` was not rebuilt** in this worktree for the void path (not required once W6 fires). Parent `events.parquet` was rebuilt; trigger count **255** matches `events_summary.json` / N14.

---

## Process disclosures

- Unit tests: `test_proximity_lib.py` **27 passed** before any real quote read; parent `test_flow_lib.py` **27 passed** re-run.
- Seed: `int("20260805b", 16)` = 8629813339 (distinct from parent `20260805`).
- Assembler filters on `np.isfinite` (None→NaN coercion fix carried from parent).
- W6 evaluated from free-panel `level_events.parquet` + parent triggers **before** any level-arm `get_range`.

---

## Iterate

This cell is **closed** on W6. Any ToD-matched level-proximity re-proposal is a new PREREG + operator GO (Avenue A / FM-4). Parent `MNQFLOW-1` W1 + N14 stand; their largest caveat (limitation 1) remains **undischarged**, now with a measured reason the naïve PDH/PDL contrast cannot discharge it.

---

## Audit hooks

See handoff §10 / PREREG §10. Machine record: [`RESULTS.json`](RESULTS.json).
