# Q-DATAFIDELITY-1 — CLOSURE: `FALSIFIED` (both limbs fired — TV price-fidelity spot check is mostly clean but the safety nets have real, confirmed scope gaps)

**Verdict:** `FALSIFIED` — H-DATAFIDELITY-1 CONFIRMED: Limb C2 (price fidelity) fires on 2 of 9 sampled MGC trade dates; Limb C3 (safety-net scope) fires on both sub-claims. Either limb alone would have been sufficient; both fired.
**Closed:** 2026-08-23
**Lane:** `UNASSIGNED`
**Pre-registration:** [`Q-DATAFIDELITY-1-verdict-preregistration.md`](../pre-registration/Q-DATAFIDELITY-1-verdict-preregistration.md) — frozen 2026-08-23, before any comparison value or grep result was read
**Spend / K:** $0.00 (2 Databento `estimate`+`pull` calls, both billed `$0.0000`; 3 greps) · K consumed: 0
**Live effect:** none — no code, sizing, or arming path touched. Diagnostic/governance finding only.
**Artifacts:** this closure · [`Q-DATAFIDELITY-1-verdict-preregistration.md`](../pre-registration/Q-DATAFIDELITY-1-verdict-preregistration.md) · scratchpad working scripts (not committed; reproducible from the commands in §10 below)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | Limb C2 all 9 days within 1-tick tolerance AND Limb C3 finds a documented byte-stability caveat AND a CME-era feed-equivalence replacement | Limb C2: 7/9 days exact match, 2/9 exceed tolerance by 40-600 ticks on High/Low. Limb C3: 0 hits for either sub-claim. | — |
| `FALSIFIED` | Limb C2 ≥1 day exceeds 1-tick tolerance on a stop/TP-relevant value, OR Limb C3 confirms both gaps | Limb C2: 2026-07-30 (all 4 fields, 566-623 ticks off) and 2026-07-31 (Open 616 ticks, High 47 ticks; Low/Close exact) exceed tolerance. Limb C3: 0 hits documenting the manifest gate's blind spot outside self-referential sources; 0 hits for a CME-era feed-equivalence successor (only file is the broken Pepperstone-only spec). | ✓ (both limbs) |
| `AMBIGUOUS-HOLD` | Limb C2 inconclusive (source unavailable/insufficient granularity) and Limb C3 partially decisive | Not applicable — Limb C2 was fully measurable on all 9 days (no unavailable-data case), and Limb C3 was fully decisive on both sub-claims (not partial). | — |

## 2. What the pre-registration predicted vs what happened

The pre-registration (§D) predicted FALSIFIED via Limb C3 alone on structural grounds, with Limb C2's outcome left genuinely open — including flagging, *before* any comparison ran, that continuous-series roll-timing noise (a class the parent brief's own Section 0 cites Q-TVCOV-1 as having excluded for counts-level work) was a gap in the frozen brief's design for price-level work. That is almost exactly what happened: Limb C3 fired as predicted; Limb C2 also fired, but on evidence that is a mix of genuine signal (7/9 exact matches, strong price-fidelity evidence) and exactly the pre-flagged confound (2/9 exceptions, one at a documented continuous-contract roll boundary, one on a date Databento's own API flagged as degraded quality). The surprise is the *strength* of the 7/9 clean result — not approximate agreement within a tick, but bit-for-bit identical OHLC across two independently-operated data pipelines on every non-confounded day sampled.

## 3. What this closure does NOT license

- **Does not license concluding "TV CME-futures OHLC is unreliable."** The 7/9 exact-match result is, if anything, unusually strong positive evidence for price fidelity on the clean days. The FALSIFIED verdict is about the *safety nets' scope* (Limb C3, unambiguous) and about *2 specific sampled days carrying unresolved divergence* (Limb C2) — not a general finding that TV data is wrong.
- **Does not adjudicate which side (TV or Databento) is correct on 2026-07-30 or 2026-07-31.** This $0 spot check cannot determine fault without a third source; CME's own settlement page was unreachable from this environment (`curl` returned connection failure) and pursuing it further would have exceeded this brief's own $0/spreadsheet-diff charter (§5 forbidden move #4).
- **Does not extend the finding to MCL or M2K**, the other two newly onboarded micros named in the brief's motivation — only MGC was sampled. A census extension is explicitly named as a FALSIFIED-disposition candidate item, not performed here.
- **Does not authorize deleting or repairing `docs/spec/feed_equivalence_discovery_test_LOCKED.md`** — DOC-1's disposition remains a separate operator ruling (parent brief §5 forbidden move #3), unchanged by this closure.
- **Does not license re-opening Q-TVCOV-1's bar-coverage FALSIFIED closure** — that closure covered existence/coverage only and stays untouched.

## 4. Defects found in the frozen brief (recorded, not repaired)

1. **Section 0's citation of the manifest-gate ADR's Trade-offs row as a grep "hit" is a miscitation.** `docs/adr/2026-05-10-manifest-integrity-gate.md:37`'s actual text ("runners cannot recompute ground truth") does not contain any of the frozen grep pattern's substrings and does not appear in the Limb C3 grep-1 result set run this session. The sub-claim it supports is still true (0 real hits, confirmed more strongly than the brief's own framing implied) — only the citation itself is inaccurate.
2. **Phase 1a's execution plan (§7) names a native Databento "daily-bar pull" without accounting for the project's own already-documented UTC-midnight-bucketing gotcha** (`lesson_databento_ohlcv1d_weekend_bars`). A literal reading of §7 would have produced a comparison against phantom UTC-day buckets misaligned with CME trade dates by up to several hours, and correspondingly a spuriously "arbitrary" 10th sampled date (2026-07-26, a Sunday partial-session artifact) rather than a genuine CME trade date. Corrected in the pre-registration by escalating to `ohlcv-1h` (still $0, still the coarsest schema that answers the question) and re-bucketing both sides by the same trade-date rule.
3. **Neither §4 (falsifiable hypothesis) nor §5 (forbidden moves) excludes continuous-series roll-timing noise for the Limb C2 *price* comparison**, even though this brief's own Section 0 cites `Q-TVCOV-1-tv-bar-coverage-census.md:69`'s forbidden move #4 excluding exactly this noise class for *count*-level comparison. This is a real gap: one of the two sampled-day exceptions (2026-07-31) lands directly on a confirmed continuous-contract roll (Databento `instrument_id` changed that session) and shows the textbook roll-mismatch signature (Open/High diverge, Low/Close match exactly). A successor brief should either exclude roll-window dates from the frozen sample or treat divergence at a roll date as a separate, expected finding class rather than raw fidelity evidence.

## 5. Lesson candidates

- **Below the two-incident bar for a new named lesson** — the roll-timing-noise-in-price-comparisons issue is a *specific instance* of an already-recorded standing lesson (`lesson_roll_rule_changes_bar_existence`) and Q-TVCOV-1's own forbidden move #4; this closure extends that prior finding from counts to prices rather than establishing a new mechanism. Watch, do not add a new MEMORY.md entry.
- The `lesson_databento_ohlcv1d_weekend_bars` memory was directly load-bearing this session (caught a real methodology defect before any comparison ran) — confirms its ongoing validity; no update needed.

---

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `FALSIFIED`
- **Model update:** the repo's trust in the two named safety nets was misplaced exactly as the source audit note suspected — Limb C3 confirms neither artifact covers TV CME-futures price fidelity, with zero hedging. Limb C2 updates the *prior* on price fidelity itself in a genuinely mixed way: the raw TV-export values match an independent feed exactly on 7/9 clean days (strong evidence FOR fidelity, stronger than the brief's authors likely expected going in), while the 2 exceptions are best explained by two well-understood confounds (vendor-flagged degraded reference data; continuous-series roll-timing) rather than a TV capture defect — but this $0 check cannot fully rule out a TV-side cause on either exception day.
- **Next:** STOP
- **Routing:** STOP — per the pre-registered FALSIFIED disposition, the confirmed safety-net gaps are named findings for the operator queue, not something this Q has standing to fix (parent brief §5 forbidden move #3 explicitly reserves the feed-equivalence-spec disposition for a separate operator ruling). No further spend is owed by this Q; a successor Q may be opened (not by this closure) to extend the MGC finding to MCL/M2K or to adjudicate the 2 confounded days against a third source.
- **Entry packet:** *(iff a successor is later opened — naming here is not opening one)* a successor would carry: the MGC 7/9-exact-match result as a positive prior; the roll-window and degraded-quality-flag exclusion rule as a required frozen-sample constraint; the $0/K=0 budget; and the standing operator-only DOC-1 ruling as an unresolved dependency, not something the successor can discharge itself.
- **Stop rule / re-proposal bar:** new mechanism evidence — a landed CME-era feed-equivalence replacement, or a landed documented manifest-gate scope caveat, or a re-run of the price diff on a *roll-window-excluded* sample that still shows divergence. Not a re-run of this exact 9-day MGC diff.
- **Board write:** `STATE.md` decision index (2026-08-23 entry, appended after this closure): "`Q-DATAFIDELITY-1` closed `FALSIFIED` — TV MGC price fidelity clean on 7/9 sampled non-confounded trade dates; both named safety nets (SHA256SUMS manifest gate, feed-equivalence pre-flight) confirmed to not cover CME-futures price fidelity. [`closure`](docs/briefs/closures/Q-DATAFIDELITY-1-closure-falsified.md)." Plus `docs/briefs/INDEX.md` — this Q moves from Open to Recently closed (see `index_row_update`).
- **Registry:** `n/a — governance/data-integrity Q on the safety nets' own coverage, not a strategy-grounds kill. No `docs/rejected_candidates.md` row owed; MGC/MCL/M2K discovery-verdict standing is unaffected by this closure (it characterizes the ground the verdicts stand on, it does not overturn them).`

## §10 audit-hook discharge

Parent brief's §10 hooks, re-run this session:

```
$ ls core/data/tv_exports/cme/ | grep -i "MGC\|MCL\|M2K"
BAR_EXPORT_v0.2_CME_MINI_M2K1!_2026-08-13_14faf.csv
BAR_EXPORT_v0.2_COMEX_MINI_MGC1!_2026-08-17_05851.csv
BAR_EXPORT_v0.2_NYMEX_MCL1_2026-08-13_3fd7c.csv
# MGC picked for the diff, as the brief's own §7 example names.

$ rg -i "byte.stab|drift.only|capture.time|wrongly.sourced|hashed.correctly|source.correctness" docs/ scripts/check_data_manifests.py
# 0 hits outside this brief's own text + the 2026-08-18 source audit note (§4). Confirmed —
# matches the hook's own "expect 0 hits" comment. (Note: the brief's Section 0 miscited the
# manifest-integrity-gate ADR's Trade-offs row as a hit; it is not — see §4 above.)

$ rg -i "feed.equivalence|feed_equivalence"
# 18 files (17 pre-existing + this brief). No second CME-era spec; confirmed via
# `ls docs/spec/ | grep -i "feed|equiv"` -> exactly feed_equivalence_discovery_test_LOCKED.md.

$ rg -n "DOC-1" STATE.md docs/SESSIONS.md docs/adr/INDEX.md
# 0 hits — DOC-1 still undischarged since 2026-08-14. Confirmed.
```

Databento cost-gate commands (Rule-1 dry-run discipline, `databento-data` skill), reproducible:

```
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate --symbols MGC.v.0 --stype continuous --schema ohlcv-1h --start 2026-07-18 --end 2026-08-01
# [estimate] cost : $0.0000 USD (streaming); 229 records
PYTHONPATH=lab python -m databento_fetch.db_fetch pull --symbols MGC.v.0 --stype continuous --schema ohlcv-1h --start 2026-07-18 --end 2026-08-01 --max-cost 0.50
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Operator GO recorded; pre-registration frozen; Phase 1 executed (MGC 9-day session-bucketed OHLC diff vs Databento MGC.v.0, + 3 frozen greps); verdict FALSIFIED asserted mechanically | Claude Code spawn |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-DATAFIDELITY-1-closure-falsified.md
grep -c "Fired?" docs/briefs/closures/Q-DATAFIDELITY-1-closure-falsified.md
```
