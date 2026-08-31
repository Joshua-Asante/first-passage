# Reversed-evidence docs audit — 2026-08-31

**Audit ID:** AUDIT-2026-08-31-REVERSED-EVIDENCE · **Date:** 2026-08-31 · **Trigger:** operator direction
("take a deeper look into evidence that has been reversed, but still reads as current; I want this
repo's documentation to be in alignment, sharing the same facts across surfaces").

**Scope:** not a blind full-corpus sweep (that is `adr-decay-audit`'s job — see the companion run at
[`docs/notes/audits/adr-corpus/2026-08-29-adr-decay-audit.md`](adr-corpus/2026-08-29-adr-decay-audit.md)
and its §7 correction below). This run instead:

1. Extracted the full `Supersedes` / `Superseded-by` / `Superseded-in-part-by` graph across all 175
   `docs/adr/*.md` files (mechanical `grep`, not agent-based) and confirmed reciprocity — the ADR corpus
   itself carries this discipline well; no reciprocity gaps were found worth a separate finding.
2. Compiled a ~30-item reference sheet of known reversal events from that graph plus
   `docs/briefs/INDEX.md`'s closure ledger and `CLAUDE.md`'s own flagged reversals (Q-FIRMEOD-1,
   MC-anchor history, Q-GATESTACK-1, persona-hierarchy narrowing, Tradeify de-scope, Striker
   withdrawal, MYM/MNQ occupancy release, and others — see the workflow's `REVERSALS` block in the
   session transcript for the full text).
3. Ran one scan agent per file across 39 non-ADR mirror surfaces — `STATE.md`, `README.md`,
   `REPO_MAP.md`, `docs/briefs/INDEX.md`, `lab/CATALOG.md`, `docs/operational_rules.md`,
   `docs/rejected_candidates.md`, `docs/mc_anchor_history.md`, `ops/venue_editions/*.md`, all 14
   `docs/methodology/*.md` files, 6 `core/strategies/**/*.md` card/lock/catalog mirrors, 5
   `docs/pursuits/*.md` trackers, and the 2 highest-risk operational skills
   (`.claude/skills/{c1-rail,prop-firm-challenge}/SKILL.md`) — each checked against the reference
   sheet *and* independently allowed to surface any other reversal it could verify from primary source.
4. Ran an independent, refute-first adversarial verify pass on every flag (re-derive from the cited
   ADR/closure itself, re-locate the claim in the target file, check for an existing caveat, rule out
   accurate-past-tense narration) before treating anything as confirmed.
5. Applied minimal, pointer-based fixes to every confirmed finding — add a dated caveat/pointer to the
   canonical current source, per Rule 7 (`docs/operational_rules.md` — one canonical owner, everyone
   else links); never rewrite history or duplicate the current value inline.

**Method note:** this is a targeted (known-reversal-propagation) sweep, not `adr-decay-audit`'s blind
full-corpus scan — it will catch a reversed fact that leaked into a mirror surface, but not a fact that
decayed *without* any traceable reversal event in the ADR/closure graph. See §4 Scope limitations for
what this run did not cover.

---

## §1 — Result

| Verdict | Count |
|---|---|
| Files scanned | 39 |
| Candidate findings (Phase 1 scan) | 37 |
| `CONFIRMED_STALE` (Phase 2 verify) | 34 |
| `NOT_STALE` — false positives caught by verify | 3 |
| `UNCERTAIN` | 0 |
| **Fixed this session** | **34 / 34** |

All 34 confirmed findings were fixed in this session (two commits — see §3). Zero were left as a
forward obligation; zero came back `UNCERTAIN`.

---

## §2 — Findings (all `CONFIRMED_STALE`, all fixed)

| # | File | Stale claim (short) | Reversed by |
|---|---|---|---|
| 1 | `STATE.md` | Blind-channel pre-G0 kill count "1/3" | [channel ADR](../../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) Addendum 2026-08-23 → 2/3. **Also**: a prior commit (`975fe14`) had claimed this exact fix without landing it — see §5. |
| 2 | `REPO_MAP.md` | "Zero unmapped" coverage-check header + §5 status note | `requirements-research.lock` (added PR #166, 2026-08-24) was unmapped since that add; regenerated + regex fixed |
| 3 | `REPO_MAP.md` | `scripts/*.py` roster table (60 vs 61 files) | Regenerated via the file's own `check_repo_map_scripts_table.py --write` |
| 4 | `lab/CATALOG.md` | msl_s4_mgc_2026-08 row: "operator TV backtest owed", Status=ACTIVE | Explore-confirm ran 2026-08-21 → `AMBIGUOUS-HOLD` → operator `PARKED` same day |
| 5 | `docs/briefs/INDEX.md` | Q-BUSTGATE-1: "live rung stays WATCH-1 0.50×" | Striker withdrawn 2026-08-04; no live c1 book (tradeify de-scope ADR) |
| 6 | `docs/briefs/INDEX.md` | Q-PUBTRANS-1: Guardian-Gold parameter leak "still present... not remediated" | Redacted at the source 2026-08-24 |
| 7 | `docs/operational_rules.md` | 2026-07-01 footnote: "the repo is now private" | Public again since 2026-08-14 (transition ADR) |
| 8 | `docs/rejected_candidates.md` | 2026-07-16 Wave-1 entry: candidate #1's 2.65%/2.64% discharge cited unqualified | §4 discharge WITHDRAWN 2026-07-22 |
| 9 | `docs/rejected_candidates.md` | 2026-07-16 Stage-2 H-SOLO entry: same discharge, "carried by candidate #1" | same withdrawal |
| 10 | `docs/rejected_candidates.md` | Q-COMPOSE-1: 2-leg Striker book "is the c1 book's sole deployable path" | Striker withdrawn 2026-08-04 |
| 11 | `ops/venue_editions/Tradeify_Select_100K.md` | `cap_alloc` 69/11 stated flat, no caveat | Released to 0 by the 2026-08-26 LEG_MAP-cap-release ADR |
| 12 | `docs/methodology/strategy_lifecycle.md` | Call-4 "first eval 2026-08-08" (×3 sites) | Never conducted; beta-cohesion diagnostic didn't land until 2026-08-24 |
| 13 | `docs/methodology/strategy_lifecycle.md` | Call-3 lane list (R5, Aegis→6J, Guardian-MGC) as undifferentiated "new additions" | Guardian-MGC is DEAD, Striker-MYM is SUBTRACT; only Aegis→6J still open |
| 14 | `docs/methodology/inqhiori-canon.md` | §14(a) add-back rate "currently 0/1" | Registry grew to 0/2 per the owning ADR's 2026-08-21 addendum |
| 15 | `docs/methodology/inqhiori-canon.md` | §14(b) "object-layer anchor = Guardian Silver re-open" | That re-open was itself reversed 2026-07-01 |
| 16 | `docs/methodology/regime_robustness_gate.md` | Part A/B worked example: "52-month Pepperstone" as a live panel | Pepperstone retired 2026-08-02, bytes deleted |
| 17 | `docs/methodology/strategy_harvest.md` | Tier A: H-TSMOM-1 "is the sole current occupant" | Closed 2026-07-16, Clause-N FAIL, never reached cost-law |
| 18 | `docs/methodology/strategy_harvest.md` | §7: Q-KBUDGET-HARVEST-1 "In flight" | `RESOLVED` same day it was locked (2026-07-16) |
| 19 | `docs/methodology/strategy_harvest.md` | §2.4: flat "~65–70% win rate" shape floor | Per-shape floor is 55/65/55–70% (RESULTS.md §6.3) |
| 20 | `docs/methodology/backtest_live_shrinkage.md` | "Aegis→M6J... the sole active scale lane" | PARKED 2026-07-16; Aegis retired from living `BASE_RISK` 2026-08-23 |
| 21 | `docs/methodology/objective_composition_map.md` | Governing instrument = 2026-07-13 prereg, bust ≤3.0% | Superseded in full by prereg v2 (2026-08-26), ceiling now 5.0% |
| 22 | `docs/methodology/objective_composition_map.md` | "...both currently agree the number is 3.0%" | Same v2 supersession |
| 23 | `docs/methodology/prefilter_rank_correlation_gate.md` | "Superseding admission path: strategy-validation §8" | §8a/§8c dormant since W4 ADR (2026-08-07); live floor is prop survivor-scoring |
| 24 | `docs/methodology/README.md` | `avenue_a_generate_confirm.md` row, no withdrawal flag | File itself WITHDRAWN 2026-08-24 |
| 25 | `core/strategies/CATALOG.md` | candidates row: MSL-S4 "live, G0 FROZEN, not yet hash-pinned" | PARKED 2026-08-21, hash-pinned 2026-08-23 |
| 26 | `core/strategies/striker/striker_dj30_v4.5_mnq_qtxg1_CARD.md` | `Disposition: PARKED_PROTOTYPE` | Scored + killed `DEAD(N-SURV)` 2026-08-12 |
| 27 | `docs/pursuits/a1-four-firms-prop-portfolio-program.md` | Measure: "≥2 of 4 FRIENDLY firms" | F1 ruling 2026-08-23 narrows to functional ≥2-of-3 |
| 28 | `docs/pursuits/a1-four-firms-prop-portfolio-program.md` | Review date: F1 listed as still pending | F1 already ruled 2026-08-23 |
| 29 | `docs/pursuits/b3-orb-mnq-payability-line.md` | "...vs. the 3.0% ceiling" | Ceiling raised to 5.0% ~1hr later the same day (prereg v2) |
| 30 | `.claude/skills/c1-rail/SKILL.md` | "...until fork F3 rules" | F3 already ruled 2026-08-07 without lifting the suspension; real gate is S4 |
| 31 | `.claude/skills/prop-firm-challenge/SKILL.md` | Aegis "live instrument is venue-dependent... USDJPY on CFD venues" | No live instrument on any venue today (CFD retired, Aegis off living `BASE_RISK`, Aegis→M6J parked) |
| 32 | `.claude/skills/prop-firm-challenge/SKILL.md` | DD revert-triggers presented as a consultable list | `CLAUDE.md`: the original triggers are LOST; needs fresh pre-registration |
| 33 | `.claude/skills/prop-firm-challenge/SKILL.md` | "historical MC pins `FIRM_RULES[\"FXIFY\"]` by name" | `FIRM_RULES["FXIFY"]` deleted at Phase 4; fixture lives in `core/historical_challenge.py` |
| 34 | `core/strategies/_archive/{aegis,guardian,nas,striker}/LOCK.md` | `strategies/...` path prefix (pre-move) | Files live under `core/strategies/...`; caught via #26's own blast-radius note, not a Phase-1 scan flag |

Row 34 was not a scan-phase finding — it surfaced as a named blast-radius note inside finding #26's own
verify pass ("apply the same pattern to the sibling aegis/guardian/nas LOCK.md files") and was confirmed
mechanically (`grep` across all four files) before fixing all four, not just the two the scan happened to
cover (nas, striker).

**False positives caught by the verify pass** (reported for completeness, per the no-silent-caps
convention — these are correct as they stand and were left untouched):

- `docs/rejected_candidates.md` — two "Avenue A generate/confirm methodology" citations sit inside a
  dated, closure-scoped "Surviving finding" section, not an unqualified current-state claim.
- `docs/methodology/1r_estimation.md` — "Guardian v5.5 is the current example" is a taxonomy label for an
  exit-architecture class, not a claim about Guardian's live deployment status.
- `core/strategies/striker/striker_dj30_v4.5_mnq_qtxg1_CARD.md` Provenance sentence ("no scoring / N-SURV
  / PnL verdict in Blocks 2–3") is accurate, scoped past-tense narration of what Blocks 2–3 did — the
  actual stale claim in this file was the `Disposition` field (finding #26), not this sentence.

---

## §3 — Fixes applied

Two commits on `claude/reversed-evidence-docs-kcoc2t`:

- **Batch 1** (`1ac136c`) — 6 files: `STATE.md`, `REPO_MAP.md` (regenerated + coverage-regex fix), and
  all four `core/strategies/_archive/*/LOCK.md` path fixes (finding #34).
- **Batch 2** (`9c89dfa`) — 19 files: the remaining findings #4–#33, one agent per file, each given only
  its own confirmed finding(s) and instructed to add a minimal dated pointer, never restate or rewrite.

Every fix keeps the original historical text intact and adds a caveat/pointer to the canonical current
source, matching this repo's own established correction idiom (`⚠ Correction <date>:` / `⚠ Superseded
<date>:`) wherever a file already used one, and introducing that idiom where a file had none.

---

## §4 — Scope limitations (not covered this pass — no silent caps)

This was a targeted 39-file pass, not a full-corpus sweep. Left unswept for this specific failure class
(a reversed fact still reading as current):

- `ops/instruments/*.md` (32 files) — high-value candidates for a follow-up pass; these carry per-leg
  live/dead state that changes often.
- `docs/pursuits/*.md` — only 5 of 41 files checked (the ones tied to known Striker/Tradeify/ORB-MNQ
  reversals). The other 36 (subscriptions, user-skill trackers, most `b*`/`c*`/`d*` rows) were not swept.
- `docs/personas/*.md` (22 files) — not touched.
- `.claude/skills/*/SKILL.md` — only `c1-rail` and `prop-firm-challenge` checked (the two most
  fact-dense operational skills); the other 21 skills were not swept.
- `core/strategies/**/*.md` — only 6 of ~26 card/lock/changelog files checked (the ones on the
  Striker/withdrawal reversal path); `guardian/`, `orb/`, `nas/`, `aegis/` card files beyond what's
  listed above were not independently re-checked (though the LOCK.md path-prefix bug, once found in one
  file, was mechanically verified and fixed across all four archive families).
- `docs/notes/`, `docs/superpowers/`, `docs/governance/`, `docs/spec/`, `lab/analysis/**/README.md`
  campaign bodies — not swept at all.
- The ADR corpus itself was checked only for `Supersedes`/`Superseded-by` header **reciprocity**
  (mechanical), not for `adr-decay-audit`'s full DECAYED_UNDOCUMENTED body-content scan — that is a
  separate, larger undertaking (see `adr-decay-audit` skill; last full run 2026-08-29, next due
  alongside the next quarterly programme-audit).

**Forward obligation logged:** `STATE.md` "No fixed date / gated" section, new bullet — the unswept
surface list above, for a future reversed-evidence pass.

---

## §5 — Correction to the 2026-08-29 ADR-decay audit

[`docs/notes/audits/adr-corpus/2026-08-29-adr-decay-audit.md`](adr-corpus/2026-08-29-adr-decay-audit.md)
§7 "Living-document fixes" claims `STATE.md:197 "blind channel... 1/3" corrected to 2/3`. This session's
verify pass on finding #1 above re-derived that claim from scratch and found it false: `git show
975fe14 -- STATE.md` shows that commit's actual diff only added an unrelated forward-board line and
never touched the "1/3" text anywhere in the file — a self-certified-but-unexecuted repair. The stale
"1/3" text survived undetected for two days (2026-08-29 → 2026-08-31) because the audit that claimed to
fix it never actually re-read the file after "fixing" it.

This is itself a small instance of the exact pattern this whole audit was run to catch — a claimed
correction (in an audit note, no less) that reads as done but never landed. Fixed for real in this
session's Batch 1 commit (`1ac136c`); dated correction added to the 2026-08-29 note itself (see its own
Addendum below the original §7, not a rewrite of that section).

---

## §6 — Discipline check

```
[x] Scope stated up front — targeted known-reversal-propagation sweep, not a blind full-corpus scan
[x] Every non-ADR mirror file in scope got one independent scan agent (39/39)
[x] Every flag ran an independent refute-first verify pass (37/37) — 3 refuted, reasoning recorded
[x] Every CONFIRMED_STALE finding fixed this session, not left as an unowned forward obligation (34/34)
[x] Fixes are pointer-based, never rewrite history or duplicate the current value inline (Rule 7)
[x] False positives (refuted flags) reported, not silently dropped
[x] Unswept surfaces named explicitly, not implied clean by omission (§4)
[x] A prior audit's own self-certified-but-unexecuted fix caught and corrected (§5)
[x] Forward obligation logged in STATE.md for the unswept surface list
[x] Next trigger: on operator request, or opportunistically alongside the next adr-decay-audit /
    programme-audit cadence — no new standing calendar trigger added (avoid a second audit clock)
```
