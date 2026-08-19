# Q-FIRMEOD-1 — Does the already-fixed EOD-vs-intraday breach-clock defect apply to the two firm classes it was never checked against?

**Status:** `OPEN — DRAFT (pre-lock)` — execution requires a separate operator GO (parent-Q convention: naming is not opening)
**Authored:** 2026-08-18
**Closed:** N/A
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the assumption-sweep audit note
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on a $0 primary-source re-read plus a one-seed engine diff, both already sketched, for the 7 Bulenox/BluSky tiers
**Artifact path:** `docs/briefs/Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md`

---

## Section 0 — Rule 0 reads (production-source verification)

All at commit `027a729` (2026-08-14, the public-transition base commit — pre-history is private per CLAUDE.md "Public-clone posture"); citations carried forward verbatim from the 2026-08-18 audit note's own direct reads, independently re-opened and confirmed during this authoring pass.

- `core/mc/simulation.py:78-88` — `simulate_path`'s `intraday_low` docstring: cites Tradeify's rule page (`help.tradeify.co` art. 10495897) by name as the sole sourcing for the intraday-honest barrier; no Bulenox/BluSky citation anywhere in the function.
- `core/mc/simulation.py:128-164` — `equity_test` (the barrier-tested value) computed once at :128-134 and consumed identically by both the `dd_type == "trailing"` branch (:141-151, Bulenox/BluSky's branch) and the `dd_type == "trailing_locking"` branch (:152-164, Tradeify/MFFU's branch) — confirms the fix mechanism is engine-generic, not Tradeify-specific.
- `core/mc/simulation.py:181` — `if equity > peak: peak = equity` — the floor still ratchets end-of-day only, identically for both branches.
- `core/mc/preflight.py:30-34` — module docstring: *"F2 (fixed-$ vs %-of-peak faithfulness for the `trailing` firms) is a modeling caveat this module does NOT correct — callers must still label Bulenox/BluSky results optimistic-lower-bounds."*
- `core/mc/preflight.py:98-102` — `firm_kwargs()` docstring: `trailing` → `trailing_dd_pct (%-of-peak; F2 optimistic for the Bulenox/BluSky fixed-$ rules — caller labels it)`, contrasted with `trailing_locking` → `"engine-faithful fixed-$ EOD trail with lock; Tradeify/MFFU"`.
- `core/firm_rules.py:31-32,39-88` — Bulenox's `dd_type="trailing"` classification, sourced only to `bulenox.com/help/qualification-account/` and `/help/master-account/`; no lock-adjacent language quoted anywhere in the sourcing comment.
- `core/firm_rules.py:433-537` (tiers at :505, :521) — BluSky's `dd_type="trailing"` classification, "minimum balance ratchets on EOD peak, never down" (:434); same absence-of-lock-citation pattern. Confirms Bulenox (5 tiers) + BluSky (2 tiers) = 7 of 13 program tiers on this branch.
- `core/firm_rules.py:266-306` — Tradeify's explicit primary-sourced lock-denial quote: *"Q: Does drawdown lock on Evaluation accounts? A: No. Drawdown only locks on Sim Funded accounts. Evaluation accounts do not have drawdown locking."*
- `core/firm_rules.py:368-381` — MFFU's parallel explicit lock-denial quote and correction, same shape.
- `docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md` Section 5 — the dedicated defect-correction ADR that made the Tradeify/MFFU lock-branch fix, triggered by exactly the same "absence-of-citation was being read as denial" error this Q asks about for Bulenox/BluSky.
- `docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md` Section 2.3 — the PASS→FAIL flip, Tradeify/MFFU only.
- `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` §4 finding B4 — the source finding this brief transcribes.

---

## Section 1 — Context and motivation

The 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`, finding **B4**) names two unverified, same-direction-optimistic assumptions in the Bulenox/BluSky bust-rate model, each of which has an already-closed analogue for Tradeify/MFFU on the exact same engine: the EOD-vs-intraday breach-clock fix (a PASS→FAIL flip, W1 ADR) and the lock/no-lock branch classification (found wrong and corrected for Tradeify/MFFU via a dedicated ADR). CLAUDE.md's own live-execution posture line — *"Eval bust figures remain EOD-clock lower bounds unless they cite an intraday-honest RESULTS path"* — is scoped in-repo only to the W1 Class-S remeasure; nothing extends it to the 7 Bulenox/BluSky tiers. This Q prices whether that scoping gap is costless or live.

**Out of scope, named not opened:** `core/mc/preflight.py:30-34,98-102`'s F2 fixed-$-vs-%-of-peak caveat is a related but structurally different gap — it was never "found and corrected" for Tradeify (Tradeify's `trailing_locking` branch is described as "engine-faithful" and doesn't carry F2 at all, per :101-102), so it has no already-fixed precedent for this Q's "does the fix apply here too" shape to test. It stays an open, disclosed-but-unquantified caveat; a separate note can pursue it if the operator elects to.

---

## Section 2 — Prior art / lineage

- `docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md` — the intraday-honest fix, proven material for Tradeify. Not re-applied here; this Q asks whether it should be.
- `docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md` — the worked precedent for Limb-LOCK: an identical "absence-of-citation read as denial" error, found wrong for Tradeify/MFFU, corrected via primary-sourced quotes.
- `docs/adr/2026-07-13-dd-protection-concept-not-constant.md` — cited in the audit's own §3 D-gate deletion #1 (a related but distinct finding: DD-protection multiplier pinned to FXIFY-C2 geometry). That deletion is **not** this Q's scope — it concerns `dd_protection.py`'s multiplier, not `firm_rules.py`'s branch/classification faithfulness — noted here only to confirm no overlap.
- None of the audit note's other four §3 D-gate deletions (CI gate wiring, sessions-order CI mirror, sentinel Tier 2-3, Requirement 5 slippage) touch this surface.

---

## Section 3 — Question (Q-FIRMEOD-1)

**Q-FIRMEOD-1:** For the 7 Bulenox/BluSky tiers modeled under `dd_type="trailing"`, has the same defect class already found and corrected for Tradeify/MFFU on this engine — an EOD-only breach clock, and a lock/no-lock branch classified from source-silence rather than a primary-sourced denial — ever been checked against Bulenox's and BluSky's own primary sources and the already-built fix, and if checked, does it hold?

(Symptom-only: names what has never been checked and what the check would look for; does not propose fixing, re-classifying, or editing anything.)

---

## Section 4 — Falsifiable hypothesis (H-FIRMEOD-1)

**H-FIRMEOD-1** (two named limbs — **CLOCK**, **LOCK**): the `dd_type="trailing"` engine branch, as currently applied to all 7 Bulenox/BluSky tiers, is a faithful-enough model of their real-money drawdown rules such that (**CLOCK**) re-applying the already-built intraday-honest fix and (**LOCK**) re-reading the cited primary sources would change neither any tested tier's bust-rate verdict nor the lock/no-lock branch selection. If CLOCK fails, the exact defect class already proven material for Tradeify (a PASS→FAIL flip) is live here too. If LOCK fails, the engine branch itself, not just a magnitude, is mis-selected for up to 7 of the program's 13 tiers.

**Reject H-FIRMEOD-1 → `FALSIFIED` if:** CLOCK fails (the one-seed diff on a tested Bulenox tier shows a nonzero `bust_trailing` count change between `intraday_low` populated vs `None`) **OR** LOCK fails (the primary-source re-read surfaces lock-adjacent language — "lock," "stop trailing," "cease," "no longer trail," "fixed at" — for either firm that contradicts the current `dd_type="trailing"` never-locks classification).

**Accept H-FIRMEOD-1 → `RESOLVED` if:** CLOCK holds (no flip) **AND** LOCK holds (no lock-adjacent language found).

**`AMBIGUOUS-HOLD` if:** either cheap check cannot execute at $0 (primary-source pages unreachable/changed, or no prior seed/path array is retrievable for reuse without a fresh simulation run).

---

## Section 5 — Forbidden moves

- **Assuming the fix mechanism is engine-generic, therefore it must already be fine for Bulenox/BluSky, without re-running it.** This is the exact unexamined leap this Q exists to close. Section 0 confirms `equity_test` (:128-164) is shared by both branches — but shared mechanism is not the same claim as shared verdict, and assuming so is precisely what let the Tradeify PASS→FAIL flip go undetected until the W1 remeasure actually ran it.
- **Editing `dd_type`, `trailing_dd_pct`, or `dd_lock_offset_usd` in `core/firm_rules.py` under this brief — even if Phase 1's primary-source re-read finds lock language.** A branch/constant change is a separate change-control action (pre-registration → re-derivation → admitting ADR, the same discipline `dd_protection`'s concept-not-constant rule enforces). This brief prices the question; it has no authority to move the answer.
- **Substituting a full 7-tier, multi-seed re-MC campaign for the one-seed diff.** The supplied falsifier is explicit that "a nonzero flip on even one seed is the same signal that flipped Tradeify PASS to FAIL" — a full campaign spends K and money this $0/K=0 inventory-depth brief was not chartered for, and needs its own operator GO.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | CLOCK holds AND LOCK holds | `INTEGRATE` — record the `trailing` branch as evidence-ratified for Bulenox/BluSky bust-rate use; discharge audit finding B4. No `dd_type`/constant edits — the branch is validated, not changed. The F2 magnitude gap (Section 1 aside) stays open and unquantified — this verdict does not speak to it. |
| `FALSIFIED` | CLOCK fails (seed diff flips) OR LOCK fails (lock-adjacent language found) | `STOP` — this brief's $0 check is complete; the defect is priced, not fixed. Re-proposal bar: a successor brief (named, not opened here) is owed to (i) re-run the intraday-honest fix across all 7 tiers per the W1 ADR pattern, and/or (ii) re-classify the affected firm's branch to `trailing_locking` with sourced lock terms, **before** any Bulenox/BluSky bust-rate figure is cited in a cross-firm capital-allocation comparison. |
| `AMBIGUOUS-HOLD` | either cheap check cannot execute at $0 | `ITERATE` — name (do not open) a successor to re-attempt the blocked check(s) on a re-test date; record which tier(s)/page(s) were blocked and why. |

**Pre-registered before any data touches analysis** — this table is frozen before Phase 1 reads a single primary-source page or runs a single diff (Known Trap #12).

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1a — LOCK.** Re-open the already-cited Bulenox primary pages (`bulenox.com/help/qualification-account/`, `/help/master-account/`, `Rates.pdf`) and BluSky's rules page (`help.blusky.pro` evaluation-rules, Terms of Use art. 11490284/12434442) and grep for lock-adjacent language ("lock," "stop trailing," "cease," "no longer trail," "fixed at") the same way Tradeify's verbatim FAQ denial and MFFU's article citation were originally found.
- **Phase 1b — CLOCK.** Re-invoke `simulate_path` (`core/mc/simulation.py`) for one existing Bulenox tier (`Bulenox_25K`, `dd_type="trailing"`) reusing an already-generated seed/path array from a prior RESULTS run — no new market data, no new discovery trial. Diff the `bust_trailing` count with `intraday_low` populated vs `None`.
- **Phase 2 — Verdict assertion.** Apply Section 6 mechanically to the two Phase-1 results; produce the closure per Section 9.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, committed before Phase 1 executes. Not yet authored — this Q is named, not opened; Section 6's table above is the frozen decision rule to be carried into the pre-registration file verbatim.

---

## Section 9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block. `RESOLVED` → `docs/briefs/closures/Q-FIRMEOD-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` with the re-test trigger named.

---

## Section 10 — Audit hooks (runnable)

```bash
# LOCK — re-open the primary sources already cited in core/firm_rules.py and grep
# for lock-adjacent language (manual browser read; no scraping automation)
#   bulenox.com/help/qualification-account/
#   bulenox.com/help/master-account/
#   bulenox.com Rates.pdf
#   help.blusky.pro evaluation-rules (art. 12434059)
#   BluSky Terms of Use art. 11490284 / Brokerage Funded Rules art. 12434442
# grep target once pages are saved/pasted locally:
grep -iE "lock|stop trailing|cease|no longer trail|fixed at" <saved_page_text>

# CLOCK — one-seed diff, reusing an already-generated path array
python -c "
from core.mc.simulation import simulate_path
from core.firm_rules import FIRM_RULES
from core.mc.preflight import firm_kwargs
kw = firm_kwargs('Bulenox_25K')
# path, dd_trigger, dd_scale, horizon supplied from an existing RESULTS run's
# saved seed/path array -- no new simulation input generated here
print('no-intraday:', simulate_path(path, dd_trigger, dd_scale, horizon, **kw)[0])
kw['intraday_low'] = existing_intraday_series
print('intraday:   ', simulate_path(path, dd_trigger, dd_scale, horizon, **kw)[0])
"
# expect: identical bucket if H holds; a bust_trailing appearing only in the
# intraday run is the same signal that flipped Tradeify PASS to FAIL

# Section 0 anchors still resolve
git log -1 --format="%h %ad" --date=short -- core/mc/simulation.py core/mc/preflight.py core/firm_rules.py
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md --type inquire

# Production-source verification (Section 0 anchors)
sed -n '78,88p;128,164p;181p' core/mc/simulation.py
sed -n '30,34p;98,102p' core/mc/preflight.py
sed -n '31,32p;39,88p;266,306p;368,381p;433,537p' core/firm_rules.py

# Cross-reference: 7 trailing tiers = Bulenox(5) + BluSky(2)
grep -n '"dd_type": "trailing"' core/firm_rules.py
```

If any verification command fails, the brief is not complete. Re-author the section that broke; do not handwave.

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary
- [x] Section 5 forbidden moves genuinely tempting
- [x] Section 6 triggers specific
- [ ] Section 8 pre-registration owed at operator GO
- [x] Section 10 hooks runnable
- [ ] Operator GO owed before Phase 1 — this brief is named, not opened
