# Q-KBUDGET-HARVEST-1 — Bounded literature harvest: expand the axis inventory without pulls or K

**Status:** `CLOSED-RESOLVED` — **2026-07-16** (Phase-3 screen extension fired §6).
**Authored:** 2026-07-16
**Locked:** 2026-07-16 (operator: "lock the harvest Pre-Q")
**Closed:** 2026-07-16 — [`closures/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md`](closures/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md). Prior: LOCKED; Phase-1/2 done; Phase-3 → 3 PASS (D5+H1+H2). Zero pulls / zero K.
**Authors:** Joshua (authority) + Cursor Cloud (assembly from standing Q-KBUDGET-1 doctrine)
**Parent question:** [`Q-KBUDGET-1`](Q-KBUDGET-1-axis-reachability-screen.md) (`RESOLVED` 2026-07-15 — D5 sole PASS). This harvest does **not** reopen that verdict; it asks whether the *inventory* can grow before the standing 2026-08-08 re-screen window.
**Sub-questions opened:** none at authoring
**Loop:** OUTER — closed RESOLVED 2026-07-16 after Phase-3 screen extension
**Artifact path:** `docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md`

---

## §0 — Rule 0 reads (production-source verification)

Read in full this session (2026-07-16) before authoring. Cheap falsifier (parent-side, <5 min): `python3 lab/archive/q_kbudget_1_2026-07/floor_scan.py` → **6 FAIL / 3 PASS (D5+H1+H2) / 0 UNSCREENABLE → RESOLVED** (post–Phase-3; historical baseline was 1 PASS) — confirms the fundable set is non-empty but single-seeded; inventory expansion is the binding bottleneck for a multi-axis 08-08 slate, not another D5 ratification.

| Source | Anchor | What it supplies |
|---|---|---|
| Parent brief + closure §5–§6 | `936a9e0` | RESOLVED on D5 pin; screen PASS licenses scoping only; L-cand-3/4 (effect-prior supply + construct-definition gaps) |
| Frozen screen pre-reg §B/§C/§D | `b304f2c` (content last touched `936a9e0`) | Two-clause screen; **§C four admission fields** (extraction template below); ranking; verdict table |
| Phase-1 inventory §2/§6/§7 | `1417b79` (ratification `ca02030`) | D1–D7 ratified as complete *for the frozen screen*; additions require a fresh ratification act; below-the-line exclusions |
| Live harness `floor_scan.py` + `RESULTS.md` | harness `936a9e0`; RESULTS synced this session | Reproducible RESOLVED table; extension target for any ratified additions |
| HARV lane ADR | `fad8984` | HARD §R still binds every funded campaign; this harvest never discharges it |
| D5 scoping + Stage-0 pre-reg | scoping + pre-reg on `main` @ post-`936a9e0` | First public-seeded campaign already GO-signed — harvest is **parallel**, not a prerequisite for D5 `register_search open` |

**Pre-Q gate (D-S-A on the literature corpus):**
- **D:** closed campaigns (DISC-CAMP-0, Q-HARV-1) enter only as calibration citations — never as reopenable axes (parent §5).
- **S:** each harvested candidate compresses to the §C 4-tuple (family→K_banked, design→K_intrinsic, era→N, cohort δ/σ or UNSCREENABLE) — nothing about reachability is lost at this dimension.
- **A:** floor(K) + power formula already exist; extending the scan is a table append after ratification, not a new engine.

---

## §1 — Context & motivation

Q-KBUDGET-1 resolved with a **single** fundable discovery axis (D5 NQ/MNQ intraday-momentum footprint). That seed is enough to start the first public-seeded campaign (Stage-0 frozen + §R GO signed — no new harvest required for D5 execution). Separately, L-cand-3 records that the binding constraint on discovery has moved to *effect-prior supply*, and D5 itself flipped from "buy a vendor dataset" to "pin a literature construct" for free. A bounded literature harvest — Tier-1/Tier-2 sources only, four §C admission fields as the extraction template, zero pulls, zero K — is the cheap way to ask whether the 08-08 slate can carry more than one ranked discovery axis without waiting for another accidental literature find.

Standing doctrine: screen kills / never blesses (pre-reg §B); inventory composition is an operator ratification act (inventory §6 ask 1); 2026-08-08 remains the standing re-screen date on the closure disposition.

---

## §2 — Prior art / lineage

- **Q-KBUDGET-1** (`RESOLVED` 2026-07-15) — parent; supplies the frozen screen, the D1–D7 inventory, and the D5 seed.
- **Q-GATECART-1** (`CLOSED-FALSIFIED`) — M-19 / Cap 1.0 / K_eff ≤ 3 design class that any harvested axis must still clear.
- **HARV lane ADR** (`Accepted`) — downstream HARD §R; harvest rows that later fund still face reachability attestation.
- **L-cand-3 / L-cand-4** (closure §4 / §5) — effect-prior supply is binding; construct-definition gaps are free to resolve from literature.
- **D5 Baltussen path** — worked example of a Tier-1 literature δ discharging an UNSCREENABLE row without procurement.

---

## §3 — Question (Q-KBUDGET-HARVEST-1)

Symptom-only form: **the ratified discovery inventory that cleared the screen has one PASS; the 08-08 re-screen window is open; literature can supply cohort-cited δ without pulls — which additional candidate axes (if any) admit under the frozen §C declaration fields from a bounded Tier-1/Tier-2 source fan-out?**

---

## §4 — Falsifiable hypothesis (H-HARVEST)

**H-HARVEST:** If a bounded Tier-1/Tier-2 literature fan-out is run with the frozen §C four-field extraction template, **then ≥1 new candidate-axis row emits with all four fields populated (or an honest UNSCREENABLE flag naming the missing input)** and survives operator ratification into an inventory addendum that extends `floor_scan.py`; **otherwise** the 08-08 discovery slate remains D5-only (an admissible outcome — D5 execution is already unblocked) and the harvest closes empty without inventing axes.

**Accept (RESOLVED) if:** ≥1 harvested row is operator-ratified into the inventory addendum **and** the extended floor scan runs (PASS / FAIL / UNSCREENABLE recorded) with zero pulls and zero K.
**Reject (FALSIFIED) if:** the fan-out completes across the frozen source list and yields **zero** rows that clear the four-field template (including honest UNSCREENABLE), after a documented pass over every Tier-1 and Tier-2 source on the list.
**Ambiguous-hold if:** ≥1 well-formed row emits but operator declines ratification (or defers past 2026-08-08) — hold; name the deferred rows; re-open only via a fresh Pre-Q, not an in-place edit.

---

## §5 — Forbidden moves

- **Treating harvest PASS rows as campaign-funded** — screen / inventory admission never discharges HARV §R or authorizes a Databento pull (parent §5; D5 scoping §2).
- **Reopening DISC-CAMP-0 or Q-HARV-1** as harvest candidates — operator-accepted closures; calibration citations only (parent §5).
- **Inventing δ/σ to fill Clause N** — no citable prior ⇒ UNSCREENABLE with the missing input named (pre-reg §B; rescope ADR §5).
- **Expanding K_intrinsic after looking** — harvested designs must declare K at extraction; under-declaring to clear Cap 1.0 voids the later `register_search` bind (pre-reg §C).
- **Silently editing the frozen D1–D7 screen rows** — additions are an *addendum* inventory + extended scan; the historical RESOLVED table stays (Trap-12).
- **Making D5 execution wait on this harvest** — D5 `register_search open` is already the unblocked next step; this Pre-Q is parallel.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | ≥1 harvested row operator-ratified + `floor_scan.py` extended and run (zero pulls / zero K) | Inventory addendum + extended RESULTS; ranked additions feed 08-08 packet alongside D5 |
| `FALSIFIED` | Frozen Tier-1/Tier-2 list fully swept; zero four-field-complete rows (incl. honest UNSCREENABLE empties do not count as "complete" unless the row itself is the product — see §7) | Close empty; 08-08 slate stays D5-only; capture whether the source list was too narrow (lesson candidate) |
| `AMBIGUOUS-HOLD` | Well-formed rows emit but ratification deferred past 2026-08-08 | Name deferred rows; do not extend the harness; reopen only via fresh Pre-Q |

**Pre-registered before Phase-1 extraction.** Amending §6 mid-harvest to match emerging papers is Trap-12.

---

## §7 — Execution plan (literature only; self-executing / CC-adjudication)

### Economic-grounding pre-check (added 2026-07-16, pre-Phase-1 — see pre-reg §C.1)

Before a candidate is logged against the four-field template below, it must clear **either** Path 1a (named mechanism) **or** Path 1b (evidence-robustness: ≥3 decades, ≥3 independent cohorts, ≥1 replication ≥10yr post-discovery, no known sign-reversal — all four) per [`docs/adr/2026-07-15-external-mechanism-harvest-intake.md`](../adr/2026-07-15-external-mechanism-harvest-intake.md) (`Accepted`), which this sweep now executes under as its front-door doctrine. Neither path clears ⇒ `EXCLUDE:no-economic-grounding` in the coverage log. Full criteria: pre-reg §C.1.

### Extraction template (frozen §C four admission requirements)

Every candidate row that clears the pre-check above **must** carry:

1. **Instrument family** → `K_banked` (from closed manifests; else 0)
2. **Search-design class + coarse tool ladder** → `K_intrinsic` (mechanism-first ≤3 preferred; wide-mining / locked-K designs are recordable FAIL-invariants)
3. **OOS era + expected event rate** → `N` (declared panel event count)
4. **Cohort-cited effect prior δ, σ** → Clause N **or** explicit `UNSCREENABLE` naming the missing input

### Source tiers (frozen for this sweep)

| Tier | Admission bar | Examples of class (not an exhaustive paper list — Phase 1 enumerates) |
|---|---|---|
| **Tier 1** | Peer-reviewed journal; **per-instrument or per-index futures** cohort with extractable central δ/σ (or β/t/R² convertible without cross-instrument transplant) | *JFE / JF / RFS / JFQA*-class empirical microstructure or anomaly papers with NQ/ES/YM/GC/6J (or liquid micro) cohorts — D5's Baltussen 2021 is the archetype |
| **Tier 2** | Reputable working paper or handbook/survey chapter with the same extractable per-instrument δ/σ bar | NBER / known-lab working papers; published anomaly surveys that report instrument-level stats (not SPX-only transplants) |

**Out of scope for this sweep:** vendor marketing decks; SPX-only γ-sign estimates transplanted to NQ/YM; blogs; anything requiring a paid dataset pull to *obtain the δ* (procurement is a different Pre-Q).

### Phases

- **Phase 0 — Rule-0 reads.** DONE parent-side (§0). Re-confirm `floor_scan.py` still RESOLVED before extraction.
- **Phase 0.5 — Lock.** **DONE 2026-07-16** — operator locked this brief; paired pre-reg FROZEN ([`Q-KBUDGET-HARVEST-1-verdict-preregistration.md`](pre-registration/Q-KBUDGET-HARVEST-1-verdict-preregistration.md)). **No paper extracted before the freeze commit.**
- **Phase 1 — Fan-out.** **DONE 2026-07-16** — Tier-1/Tier-2 fan-out under Q1–Q6; artifacts in [`lab/analysis/harvest/q_kbudget_harvest_1_2026-07/`](../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/README.md). Two four-field-complete candidates after Fig. 2 scrape (`H-OD-1`, `H-TSMOM-1`); E.1 seeds logged. Zero pulls. Zero K.
- **Phase 2 — Operator ratification.** **DONE 2026-07-16** — operator ACCEPT both → inventory addendum [`Q-KBUDGET-HARVEST-1-inventory-addendum.md`](Q-KBUDGET-HARVEST-1-inventory-addendum.md) (H1/H2); Path-1b scored PASS for H-TSMOM-1; record [`PHASE2_RATIFICATION.md`](../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md).
- **Phase 3 — Extend floor scan.** **DONE 2026-07-16** — append-only H1/H2 in `floor_scan.py`; `phase3_screen_manifest.json` + `axis_screen` → 6 FAIL / 3 PASS; [`PHASE3_RESULTS.md`](../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md); §6 **RESOLVED**; closure written; STATE updated.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

[`docs/briefs/pre-registration/Q-KBUDGET-HARVEST-1-verdict-preregistration.md`](pre-registration/Q-KBUDGET-HARVEST-1-verdict-preregistration.md) — frozen §B verdict table + §C four-field template + §D Tier bars + §E source-list appendix (seeds + query families Q1–Q6 + coverage rule).

Pre-registration commit hash: `c79bfe6` (2026-07-16 — commit landing **FROZEN** status; also cite via `git log --format='%h %ci' -- docs/briefs/pre-registration/Q-KBUDGET-HARVEST-1-verdict-preregistration.md | tail -1`)
Pre-registration date: 2026-07-16
Operator lock: 2026-07-16 (Joshua — "lock the harvest Pre-Q")

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md` + inventory addendum path + extended RESULTS citation.
- **If FALSIFIED:** same path, empty-harvest record + source-list coverage attestation.
- **If AMBIGUOUS-HOLD:** same path + deferred-row table + re-open bar.

---

## §10 — Audit hooks (runnable)

```bash
# Parent verdict still RESOLVED (harvest does not reopen it)
python3 lab/archive/q_kbudget_1_2026-07/floor_scan.py | tail -3
# expect (post–Phase-3): PASS: 3 · … Verdict … RESOLVED

# No K consumed by this Pre-Q (no harvest manifest until a future funded campaign)
grep -rn "Q-KBUDGET-HARVEST\|KBUDGET.HARVEST" discovery_manifests/ 2>/dev/null \
  && echo "REVIEW" || echo "no harvest manifest (expected pre-close)"

# Four-field template still matches frozen §C
grep -n "instrument family\|K_intrinsic\|cohort-cited\|UNSCREENABLE" \
  docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md | head -10

# 08-08 obligation visible
grep -n "Q-KBUDGET-HARVEST-1\|2026-08-08" STATE.md

# D5 execution not blocked by this brief
grep -n "§R GO SIGNED\|register_search open" \
  docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md | head -5
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python3 scripts/check_brief.py \
  docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md --type inquire
# Expected at lock: all mechanical checks PASS

# Cheap falsifier (pre-authoring, re-run at lock)
python3 lab/archive/q_kbudget_1_2026-07/floor_scan.py | tail -3
# expect RESOLVED, PASS: 1

git log -1 --format='%h %ci' -- docs/briefs/Q-KBUDGET-1-phase1-inventory.md
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md
```

*Locked 2026-07-16:* status `OPEN`; paired pre-reg FROZEN. Deep-research fan-out over query families Q1–Q6 is Phase 1 — next execution step after this lock commit.

*Amended 2026-07-16 (pre-Phase-1):* economic-grounding pre-check (Path 1a/1b) added to §7's extraction template + pre-reg §C.1, inheriting [`docs/adr/2026-07-15-external-mechanism-harvest-intake.md`](../adr/2026-07-15-external-mechanism-harvest-intake.md) (`Accepted`) as this sweep's front-door doctrine — see pre-reg §G history.
