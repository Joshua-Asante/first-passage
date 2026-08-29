# ADR: Re-lock DJ30 + NAS100 to TEST values

**Date:** 2026-05-18
**Status:** Accepted - **SUPERSEDED-BY-MERGE** — the lock action in this ADR is **not adopted**. The validator infrastructure landed alongside it was retired 2026-08-03 — see Addendum 2026-08-29.
**Decision date:** 2026-05-18
**Supersedes:** none
**Retain-until:** none
**Supersedes (same day):** [`2026-05-18-pine-input-float-defaults-realignment.md`](2026-05-18-pine-input-float-defaults-realignment.md) — the *direction* of that ADR (fix Pine to match lock); the validator/HARD-tier machinery from that ADR was later retired 2026-08-03 (see that file's Addendum 2026-08-29).
**Superseded-by:** [`2026-05-14-allocation-refresh.md`](2026-05-14-allocation-refresh.md) (already on main; the re-lock proposed here was authored against the pre-2026-05-14 baseline of 1.00% / 0.40% / 350 pyramid / 1.00 maxDD, which had already been superseded by main's 0.75% / 0.45% / 500 pyramid refresh four days earlier; the comparison MC therefore did not speak to main's actual canonical).
**Superseded-in-part-by:** `event:merge-reality` - lock action not adopted. Also `2026-08-03-params-toml-gate-retirement.md` - the validator-infrastructure bullet (retired 2026-08-03; see Addendum 2026-08-29).
**Superseded-in-part-by:** `2026-08-03-params-toml-gate-retirement.md` - the validator-infrastructure bullet only (see Addendum 2026-08-29).
**Related:** `compare_dj30_nas100_configs.py` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/analysis/dj30_nas100_config_compare/compare_dj30_nas100_configs.py`; archived 2026-05-19 with this ADR's SUPERSEDED-BY-MERGE status; see `docs/audits/2026-05-19-branch-currency-drift.md`), [`tests/test_mc_anchors.py`](../../tests/test_mc_anchors.py), [`docs/adr/2026-05-08-dd-trigger-c2-relock.md`](2026-05-08-dd-trigger-c2-relock.md), [`docs/adr/2026-05-16-fxify-correct-timeout-semantic.md`](2026-05-16-fxify-correct-timeout-semantic.md)

> **Superseded-by-merge note (2026-05-18):** This ADR was authored in a
> worktree that had branched from `main` at a point before the 2026-05-14
> allocation refresh and 2026-05-16 FXIFY-correct timeout-semantic ADRs
> landed. Main's actual canonical as of 2026-05-18 is **0.75% / 0.45% /
> 500% pyramid / 1.00 maxDD** with anchor **99.88 / 0.12 / 4.21** under
> the new timeout semantic — not the **1.00% / 0.40% / 350 / 1.00**
> baseline this ADR compared against. The −60% bust improvement claimed
> here is therefore against a baseline that no longer exists on main;
> the comparison does not show that the proposed 0.70% / 0.37% / 750 /
> 1.15 config is better than main's 0.75% / 0.45% / 500 / 1.00, only
> that it was better than the older 1.00% / 0.40% / 350 / 1.00.
>
> An apples-to-apples comparison would require (a) fresh TV exports at
> 0.70% / 0.37% / 750% / 1.15% against main's 2026-05-14 panel window,
> (b) MC under the FXIFY-correct timeout semantic, (c) side-by-side
> with main's 99.88 / 0.12 / 4.21 anchor. That work was not done; the
> lock proposed here is **not adopted**.
>
> What remains in effect from this work:
> - The parameter validator ([`scripts/validate_params.py`](../../scripts/validate_params.py))
>   and its self-test, manifest, and pre-commit-hook integration.
> - The "check both strategy + indicator" extension (catches per-file
>   drift that diverges between the two).
> - The methodology lesson that drift findings should run a comparison
>   MC before defaulting to "fix Pine to match the lock."
> - The fix to main's pre-existing `dd_protection.py BASE_RISK` drift
>   (which still had 1.00% / 0.40% while `firm_rules.py` and
>   `portfolio_mc.py` were at 0.75% / 0.45%) — landed in this branch
>   bringing BASE_RISK into alignment.
> - The historical record of how the day unfolded; useful for future
>   re-lock attempts on the same axis.

## Context

Earlier 2026-05-18 the parameter validator surfaced four risk_pct drifts:
DJ30 strategy & indicator both at 0.70 vs locked 1.00; NAS100 strategy at
0.37 / indicator at 0.45 vs locked 0.40. The first ADR of the day fixed
Pine defaults to match the lock and promoted the validator's Pine-vs-manifest
tier to HARD.

Joshua's follow-up question — *which config actually performs better in MC?*
— prompted a side-by-side run with both panels (he re-exported from TV at
both LOCKED and TEST configs, supplying four CSVs:
[`dj30default.csv`](../../core/data/tv_exports/pepperstone/), `dj30test.csv`,
`nas100default.csv`, `nas100test.csv`). The TEST config carried not just
risk_pct changes but pyramid_size and maxDailyDD too — those are
TV-exported into the trade record, so the comparison required separate
exports.

### Configs compared

| Field | LOCKED (canonical pre-2026-05-18) | TEST (Pine input.float defaults) |
|---|---|---|
| DJ30 risk_pct | 1.00% | **0.70%** |
| DJ30 pyramid_size | 350% | **750%** |
| DJ30 maxDailyDD | 1.00% | **1.15%** |
| DJ30 maxDailyTrades | 3 | **2** |
| NAS100 risk_pct | 0.40% | **0.37%** |
| NAS100 pyramid_size | 1000% | 1000% (no change) |
| Guardian risk_pct | 0.34% | 0.34% (no change) |
| Aegis risk_pct | 1.50% | 1.50% (no change) |
| dd_protection (DD_TRIGGER, DD_SCALE) | 1.5% / 0.40× | 1.5% / 0.40× (no change) |

### Comparison MC results (Pepperstone, 4-strategy, 10K × 3 seeds, C2)

| Metric | LOCKED | TEST | Delta | Direction |
|---|---:|---:|---:|---|
| Pass rate | 97.83% | **97.42%** | −0.41pp | TEST slightly worse |
| Bust rate | 0.35% | **0.14%** | −0.21pp (−60% relative) | TEST much better |
| Bust (daily / static) | 0.00% / 0.35% | 0.00% / 0.14% | — | — |
| Timeout | 1.82% | 2.44% | +0.62pp | TEST slower |
| p99 DD | 4.75% | **4.29%** | −0.46pp | TEST much better |
| p95 DD | 3.73% | 3.39% | −0.34pp | TEST better |
| p50 DD | 1.39% | 1.35% | — | flat |
| Median days to pass | 22 | 25 | +3 days | TEST slower |
| Pass-rate sigma (seed-to-seed) | 0.15% | 0.04% | tighter | TEST more stable |
| Bust attribution share (DJ30) | 38.7% | 24.4% | −14.3pp | shifted off DJ30 |
| Bust attribution share (Guardian) | 23.6% | 48.8% | +25.2pp | residual concentration |
| Lock criteria (bust <1%, p99 DD <5%) | PASS / PASS | PASS / PASS | both clear | TEST clears with more margin |

The bust-attribution share-shift toward Guardian is a normalization
artifact, not a real Guardian degradation: absolute Guardian busts dropped
~25 → ~21; absolute DJ30 busts dropped ~41 → ~10. Total bust pool shrank
from ~105 → ~42, so Guardian's *share* of a smaller pool grew while its
absolute count fell.

## Decision

Re-lock DJ30 + NAS100 to TEST values. Specifically:

1. **`dd_protection.py`** `BASE_RISK["Striker"]` `0.0100 → 0.0070`,
   `BASE_RISK["Striker NAS100"]` `0.0040 → 0.0037`.
2. **`firm_rules.py`** `_BASE_RISK["striker"]` `0.0100 → 0.0070`,
   `_BASE_RISK["striker_nas100"]` `0.0040 → 0.0037`.
3. **`portfolio_mc.py`** `ALLOCATIONS["striker"]` `0.0100 → 0.0070`,
   `ALLOCATIONS["striker_nas100"]` `0.0040 → 0.0037`; `PEPPERSTONE_PANELS`
   points at the new TEST exports
   (`Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-05-18_ca15e.csv` and
   `Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-18_d2c59.csv`).
4. **`tests/test_mc_anchors.py`** pinned to the new anchors:
   Pepperstone **97.42 / 0.14 / 4.29**, OANDA **96.30 / 0.33 / 4.69**.
5. **`CLAUDE.md`** Strategy Reference table + Protection MC anchor +
   historical "Prior anchors" entry for the superseded 2026-05-08 anchor.
6. **`config/params.toml`** risk_pct values updated; `pyramid_pct`,
   `max_daily_dd_pct`, `max_daily_trades` added as v2 manifest fields
   (DJ30 750 / 1.15 / 2 and NAS100 1000 / 1.00 / 2).
7. **Pine source-of-truth** — the four risk_pct fixes from the earlier
   2026-05-18 ADR are **reverted**; defaults now match the new lock
   (DJ30 0.70 / NAS100 0.37). Adjacent stale tooltips also updated where
   they referenced the prior lock value
   (`"LOCKED: 1.00%"` → `"LOCKED 2026-05-18: 0.70%"`, etc.). DJ30 indicator
   `pyramidSize` `maxval` expanded `500 → 1000` to match strategy file's
   `750` default. Files mirrored back to
   `C:\Users\joshu\Downloads\{dj30,dj30indicator,nas100,nas100indicator}.txt`
   for TV re-import.
8. **Validator** machinery and HARD-tier promotion from the superseded
   ADR are **preserved**. Manifest now declares 0.70 / 0.37; validator
   passes against the re-locked Pine source.

## Trade-offs

| Approach | Outcome |
|---|---|
| Keep prior lock (1.00% / 0.40% / 350 pyramid / 1.00 maxDD) | **Rejected** — TEST clears bust gate with 7× more margin and DD gate with 65% more margin. The 0.41pp pass-rate cost is dominated by the −60% bust risk improvement. Tail safety > expected outcome for a $200K-at-risk challenge. |
| Re-lock to TEST values | **Adopted.** Pine source-of-truth already had these as input.float defaults (the "drift" caught earlier was actually the *correct* operational config that hadn't been propagated to the lock spec). |
| Adopt only the risk_pct portion (0.70 / 0.37), keep 350 pyramid + 1.00 maxDD | **Rejected** — would require re-export and re-MC; the four-CSV comparison already shows the combined config is the right basket. Splitting one knob at a time would be three more cycles. |
| Promote the new TEST anchor via a multi-week regime-robustness gate | **Rejected this cycle.** Joshua reviewed the side-by-side and committed. The 2026-05-18 numbers are deterministic and reproducible; if 6-month rolling MC shows degradation under the new config, the standing C2 revert trigger applies. |

## Consequences

- **Reproducibility:** `python portfolio_mc.py --panel pepperstone` now
  reports the new canonical anchor 97.42 / 0.14 / 4.29.
  `python -m pytest tests/test_mc_anchors.py` pins this.
- **Operational behavior:** on a fresh TV chart attach with the re-locked
  Pine source, the strategy will trade at 0.70% DJ30 / 0.37% NAS100 by
  default — no manual override needed. The mismatch between Pine defaults
  and the locked operational layer (the original 2026-05-18 catch) is
  resolved at both ends now.
- **OANDA panel:** still on DJ30 v4.4. OANDA at the new ALLOCATIONS
  reports 96.30 / 0.33 / 4.69 — clears criteria with thinner margin
  (pattern-spotting role). An OANDA v4.5 re-export at the new
  pyramid/maxDD config is queued; until then the OANDA pattern-spotting
  effect of pyramid/maxDD changes is unobserved.
- **Forward revert trigger:** standing dd_protection C2 trigger applies
  unchanged (rolling 6-month MC pass-rate <95% for two consecutive 6-month
  windows → revert dd_protection to C0). Next quarterly check 2026-08-08.
  If the new ALLOCATIONS show regime degradation, the same trigger
  applies; revert path is to the 2026-05-08 anchor.
- **TradingView round-trip required:** the corrected Pine source lives in
  `C:\Users\joshu\Downloads\` ready for paste-into-TV. Until Joshua does
  the round-trip, a fresh re-export from the cloud version will revert
  the source files to whatever's stored in TV, which may or may not be
  current. The validator hard-fails on the next commit if drift returns.

## Verification

```bash
$ python portfolio_mc.py --panel pepperstone
# ... reports 97.42% pass / 0.14% bust / 4.29% p99 DD ...

$ python -m pytest tests/test_mc_anchors.py -v
# test_pepperstone_anchor PASS
# test_oanda_anchor       PASS

$ python scripts/validate_params.py
# Summary: 0 HARD violation(s), 0 WARN violation(s)
```

Side-by-side comparison was reproducible via the archived script (see
`archive/analysis/dj30_nas100_config_compare/compare_dj30_nas100_configs.py`,
archived 2026-05-19 alongside this ADR's SUPERSEDED-BY-MERGE status):

```bash
# Historical invocation (script archived 2026-05-19; not runnable from
# archived path without REPO_ROOT fix):
$ python scripts/compare_dj30_nas100_configs.py
# LOCKED:  97.83 / 0.35 / 4.75 (using superseded default CSVs)
# TEST:    97.42 / 0.14 / 4.29 (using new canonical CSVs)
```

The comparison script retains both panel pairs (DJ30/NAS100 default vs
test) for future reference; the default CSVs are no longer canonical but
remain available locally for re-running the comparison if a future
re-lock is contemplated. The new canonical pair is
`Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-05-18_ca15e.csv` and
`Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-18_d2c59.csv`.

## Methodology notes

- **The "drift" was right; the lock was wrong.** The Pine input.float
  defaults that the validator flagged as drift were actually the better
  operational config. The discipline that fixed Pine to match the lock
  was correct as a *generic rule*; the comparison MC was the right
  follow-up question to *verify the lock itself*, not just verify Pine
  vs lock. Future drift findings should run the same comparison before
  defaulting to "fix Pine to match the lock."
- **Validator value compounds beyond direct catches.** The validator's
  surfacing of drift didn't just fix four lines of Pine — it triggered
  the MC comparison that found a strictly better lock. The intrinsic
  value of the gate is wider than "stops bad commits."
- **Three-round refinement in one day.** Round 1 (4 indicator + 1
  strategy) → Round 2 (4 strategies) → Round 3 (1 indicator) → comparison
  MC → re-lock. The "check both strategy + indicator" extension to the
  validator (Round 2) was load-bearing for full coverage.

## Addendum 2026-08-29 — validator-infrastructure bullet superseded (DECAYED_UNDOCUMENTED, adr-decay-audit)

The top blockquote's "What remains in effect from this work" list asserts, as currently true, that
"the parameter validator (`scripts/validate_params.py`) and its self-test, manifest, and
pre-commit-hook integration" remains in effect. **That bullet is stale.**
[`2026-08-03-params-toml-gate-retirement.md`](2026-08-03-params-toml-gate-retirement.md) retired
`scripts/validate_params.py` outright (`git rm`, shape 1: delete the derived `params.toml` mirror
and retire the hub gates that only compared against it) — the file no longer exists on disk. The
blockquote and the header above stay byte-unedited as the historical record (Rule 14); this
addendum is the correction a reader needs.

**Current state, verified against production:**

- `scripts/validate_params.py` — **absent** (confirmed: no such file). Its self-test, manifest
  comparison, and pre-commit-hook wiring are retired with it.
- Successor for Pine integrity: `scripts/check_pine_manifest.py` + `core/strategies/MANIFEST.sha256`
  (hash-pinned, not a live cross-source drift comparison).
- Live-sizing constants remain canonical in `dd_protection.py` / `firm_rules.py`, **untouched** by
  the 2026-08-03 retirement — this ADR's re-locked risk_pct values (0.70% / 0.37%) are not affected.
- The other three "remains in effect" bullets in the same blockquote are **unaffected** by this
  addendum: the methodology lesson (run a comparison MC before defaulting to "fix Pine to match the
  lock"), the `dd_protection.py BASE_RISK` alignment fix landed in this branch, and the historical
  record of how the day unfolded all still stand as recorded.
- **Not separately re-verified here, flagged for the central regeneration pass:** the sibling
  bullet "the 'check both strategy + indicator' extension (catches per-file drift that diverges
  between the two)" was also validator-infrastructure (a `validate_params.py` behavior) — its
  current-effect status was out of scope for this remediation and was not independently confirmed
  against `check_pine_manifest.py`'s actual coverage.

`docs/adr/INDEX.md`'s "Partially superseded" table (the row for this file, ~line 143) mirrors the
same stale "validator infrastructure... remains in effect" claim and needs the same correction
during the central `check_adr_graph.py --regenerate-index` pass — not corrected in this addendum.
