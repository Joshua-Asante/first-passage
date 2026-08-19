# [Q-DATAFIDELITY-1] — Do the stated data-integrity safety nets cover CME-futures price fidelity?

**Status:** `OPEN — DRAFT (pre-lock)` — execution requires a separate operator GO (parent-Q convention: naming is not opening)
**Authored:** 2026-08-18
**Closed:** N/A
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the 2026-08-18 assumption-sweep audit note, findings C2/C3
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on a $0 spreadsheet-level price diff for one onboarded instrument plus a $0 repo-wide grep for undocumented gate scope
**Artifact path:** `docs/briefs/Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md`

---

## Section 0 — Rule 0 reads (production-source verification)

Verified this session (2026-08-18), each against working-tree bytes:

- `docs/briefs/Q-TVCOV-1-tv-bar-coverage-census.md:69` — §5 Forbidden moves, item 4: *"Comparing prices across TV/Databento continuous series (roll-rule/adjustment mismatch noise; counts only)."* Confirms price-value comparison was explicitly out of scope for the only prior TV-fidelity census, which covered bar existence/coverage for 3 symbols and closed **FALSIFIED** 2026-07-13 (`docs/briefs/INDEX.md:135`).
- `core/data/tv_exports/cme/SHA256SUMS` — read in full this session. `BAR_EXPORT_v0.2_COMEX_MINI_MGC1!_2026-08-17_05851.csv`, `BAR_EXPORT_v0.2_NYMEX_MCL1_2026-08-13_3fd7c.csv`, `BAR_EXPORT_v0.2_CME_MINI_M2K1!_2026-08-13_14faf.csv` — all three postdate the 2026-07-13 census close. `git log -1` on this path (2026-08-18): `5464cb4` "data(tv_exports): land fresh MGC 1! export for six-lead pursuit P1/P2."
- `ops/instruments/MCL.md:54-56,86,88` — MCL findings C4/C5 already scored (`2026-08-18b` "OFFICIAL corrected-null re-score: `SIGNAL-GENERIC` (C5 added...)") off the un-censused BAR_EXPORT panel.
- `ops/instruments/M2K.md:62,73-75` — MSL-C3-K2 dual-axis explore, closed **FALSIFIED** 2026-08-13 (`docs/briefs/closures/MSL-C3-K2-closure-falsified.md`), consumed the un-censused `M2K_M15.csv` panel (sha256 `81922570…`), both axes' IS CI entirely < 0.
- `core/bar_export_loader.py:111-173` — read in full this session. `price_tolerance()` (:111-117) and the cross-check at `:167-173` (`if abs(entry_px - enc["c"]) > tol: raise ValueError(...)`) compare the TV export's own Entry-price column against its own encoded-close signal string — an internal-consistency check within one TV file, never against an independent source.
- `docs/spec/feed_equivalence_discovery_test_LOCKED.md:41` — §Scope: *"Symbol: **XAUUSD.a** only… Window: 2026-04-13 through 2026-04-25… Timeframe: 15m."* Tests the retired MT5-Pepperstone vs TV-Pepperstone CFD pair — no CME-futures instrument, no venue this program still uses.
- `docs/notes/audits/2026-08-14-requirements-backlog-ratification.md:61` — row DOC-1: *"`feed_equivalence_discovery_test_LOCKED.md` — MANDATORY per CLAUDE.md's Firm Expansion section, but its Phase-0 steps require a directory deleted with Pepperstone… This is a live gate on a process (firm expansion) that could fire again — needs explicit ruling before deletion, not a chip."* No ruling recorded since.
- `docs/notes/audits/2026-08-08-conventions-delete-phase-gap-audit.md:132` — same finding, independently confirmed one audit earlier: *"CONFIRMED → **DELETE** (~99 lines) — *operator decision*"* — still undischarged.
- `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md:17` — *"does NOT supersede `docs/spec/feed_equivalence_discovery_test_LOCKED.md` (firm-onboarding execution-feed equivalence — different question, unaffected)"* — the ADR that made CME futures TV exports canonical explicitly declines to replace the broken pre-flight; no successor named anywhere else in the corpus (`feed_equivalence` greps to 17 files, none a CME-era replacement).
- `scripts/check_data_manifests.py` — read in full this session; hashes working-tree bytes against `SHA256SUMS`, by design a byte-stability-since-last-`--regenerate` check with no independent re-derivation of the source values.
- `docs/adr/2026-05-10-manifest-integrity-gate.md:33-37` — §Trade-offs: *"Hash validation in GitHub Actions | **Rejected** — vendor bytes are not in the repo; runners cannot recompute ground truth."* Confirms the gate's own admitting ADR frames it as a byte-recomputation check, not a source-correctness check — but this framing is stated only inside the Trade-offs table, never surfaced as a caveat anywhere a reader of the manifest gate itself (`scripts/check_data_manifests.py`, `CLAUDE.md` §Vendor-data integrity gate) would see it.
- Repo-wide grep this session for `byte.stab|capture.time|wrongly.sourced|drift-only|source-correctness` (case-insensitive) across `docs/` — 0 hits describing the manifest gate's blind spot outside the one Trade-offs row above; all other hits are unrelated byte-stability claims about frozen constants (`core/firm_rules.py`, `dd_protection` C2 constants).
- `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` — findings C2 (§4 Tier C) and C3 (§4 Tier C), this session's source material; uncommitted at authoring time (`git status --short` shows `??`).

---

## Section 1 — Context and motivation

The 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`, findings **C2** and **C3**) surfaced that the repo's trust in TradingView-exported CME futures OHLC has never been tested at the price-value level, and that the two artifacts CLAUDE.md cites as data-integrity safety nets — the feed-equivalence pre-flight and the SHA256SUMS manifest gate — do not actually cover that question. This connects directly to standing doctrine: `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` made TV exports canonical for the CME-futures era; `core/firm_rules.py`'s "Firm Expansion" pre-flight requirement (CLAUDE.md §Firm Expansion) is supposed to be the check that a new feed is trustworthy before it's used for closure-grade decisions. Three newly onboarded micros (MGC, MCL, M2K) are already producing FALSIFIED/SIGNAL-GENERIC discovery verdicts on exactly this unverified ground.

---

## Section 2 — Prior art / lineage

- **Q-TVCOV-1** (closed **FALSIFIED** 2026-07-13, `docs/briefs/INDEX.md:135`) — the only prior TV-fidelity work. Covered bar existence/coverage only, for 3 symbols, and its own §5 Forbidden moves (`Q-TVCOV-1-tv-bar-coverage-census.md:69`) explicitly ruled price comparison out of scope. This Q does not re-litigate that closure — it opens the narrower question Q-TVCOV-1 deliberately left untouched, for instruments Q-TVCOV-1 never covered.
- **D-gate scoping (audit note §3):** none of the 5 already-covered deletions in the audit's D-gate touch price fidelity or manifest-gate scope — no overlap to avoid.
- **Q-CAPBAND-1** (`docs/briefs/Q-CAPBAND-1-cap-band-counterfactual.md`) — the structural precedent this brief follows: one brief, one combined falsifiable H spanning named limbs, one gate-criteria table, closed-artifact/self-executing $0 execution.
- **DOC-1** (`docs/notes/audits/2026-08-14-requirements-backlog-ratification.md` row DOC-1; independently confirmed `2026-08-08-conventions-delete-phase-gap-audit.md:132`) — names the feed-equivalence pre-flight's broken state twice, with no ruling issued either time. This Q inherits that unresolved fact as Limb-C3's starting condition rather than re-deriving it.

---

## Section 3 — Question (Q-DATAFIDELITY-1)

**Pre-Q gate test (symptom-only rephrase):** "the repo trusts TradingView CME-futures OHLC and trusts that two named artifacts catch a bad feed, and neither trust has ever been checked against ground truth or against what those artifacts actually verify." No fix is named — the question does not say "add a price-comparison check" or "replace the pre-flight."

**Q-DATAFIDELITY-1:** Do the repo's stated data-integrity safety nets — for the specific claim that TradingView's exported CME-futures OHLC values match the real venue tape — actually cover what they are trusted to cover?

---

## Section 4 — Falsifiable hypothesis (H-DATAFIDELITY-1)

**H-DATAFIDELITY-1** (two named limbs, one combined verdict):

- **Limb C2 (price fidelity):** for at least one newly onboarded CME micro instrument (MGC, MCL, or M2K), TradingView's exported daily OHLC values diverge from an independently sourced same-date reference (CME's own published settlement/OHLC, or a free Databento daily-bar pull) by more than 1 tick on a value that would change a stop/TP-hit determination.
- **Limb C3 (safety-net scope):** no document anywhere in the repo states that the SHA256SUMS manifest gate is a byte-stability-since-last-`--regenerate` check only (not a source-correctness check), **AND** no CME-futures-era feed-equivalence check exists to replace the broken Pepperstone-only pre-flight.

**If Limb C2 holds (divergence found) OR Limb C3 holds (both scope gaps confirmed undocumented/unfilled), the combined H is CONFIRMED**: at least one of the two safety-net failure modes the audit flagged is real, and every locked-strategy MC calibration figure and backtest stop/TP-hit determination downstream of TV CME-futures data carries unverified ground truth. **If neither limb holds, H is REJECTED**: the safety nets cover what they're trusted to cover for this specific claim.

**Reject H-DATAFIDELITY-1 (→ RESOLVED) if:** Limb C2 finds all sampled days within 1-tick tolerance on the affected instrument(s) **AND** Limb C3's grep finds an existing documented caveat on the manifest gate's scope **AND** a CME-era feed-equivalence replacement already exists somewhere in the corpus.

**Accept H-DATAFIDELITY-1 (→ FALSIFIED) if:** Limb C2 finds ≥1 day exceeding 1-tick tolerance on a stop/TP-relevant value, **OR** Limb C3 confirms both the undocumented-scope gap and the missing replacement.

**Ambiguous-hold if:** Limb C2's diff is inconclusive (e.g., CME's free settlement page does not publish the needed OHLC granularity for the sampled instrument, or Databento's RECENT-DATA entitlement doesn't cover the sampled dates) **and** Limb C3 alone is not decisive enough to close the combined H (e.g., a caveat is found for one sub-claim but not the other, needing operator judgment on materiality).

---

## Section 5 — Forbidden moves

- **Treating Q-TVCOV-1's FALSIFIED bar-coverage closure as if it also settled price fidelity.** This is the specific conflation named in this Q's own charter — Q-TVCOV-1's §5 explicitly excluded price comparison (`Q-TVCOV-1-tv-bar-coverage-census.md:69`), and three new instruments (MGC, MCL, M2K) postdate that census entirely. Ruled out because the citation is direct and unambiguous — restating "coverage was already censused" as fidelity coverage would be citing a closed brief for a claim it deliberately declined to make.
- **Treating "the manifest gate passed" as fidelity evidence.** `scripts/check_data_manifests.py` proves byte-stability since the last `--regenerate`, nothing about whether the bytes were right when captured (`docs/adr/2026-05-10-manifest-integrity-gate.md:33-37`). Tempting because a green gate reads as reassurance; ruled out because the gate's own admitting ADR names this exact blind spot, and MEMORY.md's own standing lesson (`lesson_green_gate_is_not_coverage`) is precisely this trap.
- **Fixing DOC-1 (deleting or repairing the feed-equivalence spec) as a side effect of this brief.** Tempting because the broken state is already twice-flagged and looks like a quick delete. Ruled out because DOC-1 itself says the disposition needs "explicit ruling before deletion, not a chip" — that ruling is a separate operator decision this Q does not have standing to make; this Q only prices whether the gap is real and undocumented.
- **Running a new backtest or paid data pull to "really" nail down the divergence once Limb C2's cheap 10-row diff comes back close-but-not-exact.** Tempting because a borderline result invites more rigor. Ruled out by this brief's own depth charter (inventory + triage, $0/K=0) — a borderline Limb C2 result routes to Ambiguous-hold, not to an uncommissioned spend.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | Limb C2: all sampled days within 1-tick tolerance on the diffed instrument's stop/TP-relevant OHLC values. Limb C3: repo grep finds an existing documented byte-stability-only caveat on the manifest gate, AND a CME-era feed-equivalence replacement is found to already exist. | `INTEGRATE — record TV CME-futures price fidelity and safety-net scope as evidence-checked for the sampled instrument/dates; no code or doc change owed.` |
| `FALSIFIED` | Limb C2: ≥1 sampled day exceeds 1-tick tolerance on a stop/TP-relevant value. OR Limb C3: grep confirms 0 hits documenting the manifest gate's blind spot AND 0 hits for a CME-era feed-equivalence successor. | `STOP — the specific safety-net gap(s) confirmed real are named findings for the operator queue (candidate items: a CME-era feed-equivalence replacement; a documented manifest-gate scope caveat; a price-fidelity census extended to MGC/MCL/M2K). Re-proposal bar: new mechanism evidence (a real fix landed and re-verified), not a re-run of the same diff.` |
| `AMBIGUOUS-HOLD` | Limb C2 inconclusive (reference source unavailable/insufficient granularity for the sampled dates) and Limb C3 partially decisive (one sub-claim confirmed, the other not). | `ITERATE — name (do not open) a successor: re-run Limb C2 against a different free reference source or a different sampled instrument; re-test window: next time a 4th CME micro is onboarded via BAR_EXPORT.` |

**Pre-registered before any diff or grep runs.** §6 is not amended mid-investigation to match what either limb returns (Known Trap #12).

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1a — Limb C2 diff.** Pick 5-10 arbitrary trading days already covered by the on-disk TV export for one instrument (e.g. MGC, `core/data/tv_exports/cme/BAR_EXPORT_v0.2_COMEX_MINI_MGC1!_2026-08-17_05851.csv`). Manually diff O/H/L/C for those exact dates against CME Group's own free published daily settlement page, or a trivial free-tier Databento daily-bar pull via the `databento-data` skill's RECENT-DATA access. Spreadsheet-level row diff of ~10 values. No new backtest, no paid pull, no K spend.
- **Phase 1b — Limb C3 grep.** `rg` for `byte.stab|drift.only|capture.time|wrongly.sourced|hashed.correctly|source.correctness` across `docs/` and `scripts/check_data_manifests.py` (already run this session in Section 0 — 0 hits describing the gap outside the Trade-offs table row). `rg -i "feed.equivalence|feed_equivalence"` repo-wide (already run — 17 files, no CME-era successor spec found). `rg "DOC-1"` across `STATE.md`, `docs/SESSIONS.md`, `docs/adr/INDEX.md` (confirm no resolution logged since the 2026-08-14 audit note).
- **Phase 2 — Verdict assertion.** Apply Section 6 mechanically to Phase 1a/1b outputs. Produce the closure artifact per Section 9.

Estimated cost: **$0, K = 0.** No manifest, no backtest, no paid data pull.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, committed before Phase 1 executes: `docs/briefs/pre-registration/Q-DATAFIDELITY-1-verdict-preregistration.md`, containing the Section 6 table above plus the frozen instrument/date sample for Limb C2 and the frozen grep patterns for Limb C3. Not yet authored — this Q is named, not opened.

---

## Section 9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block.

- **If RESOLVED:** `docs/briefs/closures/Q-DATAFIDELITY-1-closure-resolved.md`
- **If FALSIFIED:** `docs/briefs/closures/Q-DATAFIDELITY-1-closure-falsified.md` (no `recommendation.md`)
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-DATAFIDELITY-1-closure-ambiguous.md` with the re-test trigger (next CME micro onboarding) named explicitly

---

## Section 10 — Audit hooks (runnable)

```bash
# Limb C2 — instrument on disk, ready to diff
ls core/data/tv_exports/cme/ | grep -i "MGC\|MCL\|M2K"
# expect: BAR_EXPORT_v0.2_COMEX_MINI_MGC1!_2026-08-17_05851.csv (or MCL/M2K equivalents)
# then: manually diff ~10 O/H/L/C rows against CME Group's free published daily settlement page
# (or a free-tier Databento daily-bar pull via the databento-data skill's RECENT-DATA access)

# Limb C3 — manifest-gate scope, undocumented anywhere
rg -i "byte.stab|drift.only|capture.time|wrongly.sourced|hashed.correctly|source.correctness" docs/ scripts/check_data_manifests.py
# expect: 0 hits describing the manifest gate's blind spot (the one exception is the
# Trade-offs table inside docs/adr/2026-05-10-manifest-integrity-gate.md itself)

# Limb C3 — no CME-era feed-equivalence successor
rg -i "feed.equivalence|feed_equivalence"
# expect: docs/spec/feed_equivalence_discovery_test_LOCKED.md (the broken Pepperstone-only
# spec) plus citing surfaces; no second, CME-futures-scoped spec

# Limb C3 — DOC-1 still undischarged
rg -n "DOC-1" STATE.md docs/SESSIONS.md docs/adr/INDEX.md
# expect: no resolution logged since docs/notes/audits/2026-08-14-requirements-backlog-ratification.md
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/briefs/Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md --type inquire
# Expected: all checks PASS

# Production-source verification (Section 0 anchor confirmation)
$ rg -n "Comparing prices across TV/Databento" docs/briefs/Q-TVCOV-1-tv-bar-coverage-census.md
$ cat core/data/tv_exports/cme/SHA256SUMS | rg -i "MGC|MCL|M2K"
$ sed -n '108,175p' core/bar_export_loader.py
$ sed -n '30,45p' docs/spec/feed_equivalence_discovery_test_LOCKED.md
$ rg -n "DOC-1" docs/notes/audits/2026-08-14-requirements-backlog-ratification.md docs/notes/audits/2026-08-08-conventions-delete-phase-gap-audit.md
$ sed -n '30,40p' docs/adr/2026-05-10-manifest-integrity-gate.md

# Cross-reference verification (cited facts match canonical sources)
$ grep -n "Q-TVCOV-1" docs/briefs/INDEX.md
# Expected: FALSIFIED closure, 2026-07-13
```

If any verification command fails, the brief is not complete. Re-author the section that broke; do not handwave.

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary
- [x] Section 5 forbidden moves genuinely tempting
- [x] Section 6 triggers specific
- [x] Section 8 pre-registration owed at operator GO
- [x] Section 10 hooks runnable
- [ ] Operator GO owed before Phase 1 — this brief is named, not opened