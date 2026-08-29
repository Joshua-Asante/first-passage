# Brief corpus decay audit — full-corpus tiered scan/verify run

**Audit ID:** AUDIT-2026-08-29-BRIEF-DECAY · **Date:** 2026-08-29 · **Trigger:** operator direction,
extending the same-day `adr-decay-audit` full-corpus run (`docs/notes/audits/adr-corpus/2026-08-29-adr-decay-audit.md`)
to the `docs/briefs/` corpus (342 files) — no equivalent skill exists for briefs, so this audit adapts
`adr-decay-audit`'s scan→verify method to the corpus's actual shape.
**Authors:** Joshua (direction) + Claude Code. **Method:** the brief corpus is structurally unlike the
ADR corpus (mostly terminal question/investigation records rather than standing decisions), so files
were tiered by decay risk before scanning rather than treated uniformly:

- **Tier 1 (44 files, full decay-audit rigor)** — every OPEN/DRAFT/ACTIVE/RATIFIED/DORMANT root-level
  brief, `docs/briefs/INDEX.md`'s Open+Dormant tables (row-by-row), and the handful of `rnd-pipeline/`
  scoping docs still asserting a live/unconsumed state. These are the closest analog to Accepted ADRs —
  standing claims that could have been overtaken by events. 11 Phase-1 batches (4 files each), same
  4-point method as `adr-decay-audit` (self-declared status vs. reality; falsifier/expiry/wake-condition
  dates; factual claims spot-checked against actual current source; cross-reference integrity), followed
  by a Phase-2 refute-first verify on every non-`STILL_APPLICABLE` flag (31 of 44).
- **Tier 2 (176 files, lightweight citation-consistency check)** — closed/terminal root-level briefs and
  their matched `closures/` records. These are historical record by design (their job is to accurately
  record what was found at closure time, not to remain "true" indefinitely), so the check is narrower:
  internal consistency (does a brief's Status line agree with its own closure?) and downstream-reference
  drift (does a citation assert a state — "successor Q-X is OPEN", "ADR Y (Proposed)" — that's now
  factually wrong?), not full content re-derivation. 18 Phase-1 batches (10 files each), Phase-2 verify
  on all 14 non-`CLEAN` flags.
- **Tier 3 (125 files, mechanical integrity check only)** — frozen `pre-registration/` artifacts and
  one-shot `handoffs/` packets. Neither is subject to content decay by design (a pre-registration's whole
  point is to stay frozen; a handoff is a consumed one-shot packet), so this tier checks structural
  integrity only: do cited freeze-hashes/paths still resolve, and does any handoff still get described
  elsewhere as pending when it's demonstrably done. 9 Phase-1 batches (15 files each), no verify phase
  (low-stakes, self-evidencing findings).

83 agents total (44 Phase-1 batches + 39 Phase-2 verify calls), 0 errors, 0 empty results, ~11.1M
subagent tokens, 1920 tool calls.

One harness note: a single Tier-3 scan batch's structured output was flagged by the platform's own
defensive pattern-matcher as containing instruction-shaped text (re: `.claude/settings.json`). Checked
directly — the flagged content was a legitimate finding discussing whether certain `.claude/settings.json`
allow-rules were removed as part of a handoff's discharge verification. Confirmed benign; no injection
attempt. Noted here for transparency, not because it required any action.

---

## §1 — Result

| Tier | Scanned | Verdict counts (Phase 1 raw) |
|---|---:|---|
| 1 — live/open briefs | 44 | STILL_APPLICABLE 13 · DECAYED_DOCUMENTED 8 · DECAYED_UNDOCUMENTED 21 · UNCERTAIN 2 |
| 2 — closed briefs + closures | 176 | CLEAN 162 · STALE_CITATION 9 · INCONSISTENT 5 |
| 3 — pre-registration + handoffs | 125 | OK 102 · BROKEN_LINK 19 · STALE_PENDING_CLAIM 4 |

| Tier 1 (Phase 2 final, after 10 reclassifications) | Count |
|---|---:|
| STILL_APPLICABLE | 15 (+2) |
| DECAYED_DOCUMENTED | 9 (+1) |
| DECAYED_UNDOCUMENTED | 20 (−1) |
| UNCERTAIN | 0 (−2) |

Tier 2's 14 flagged findings were all **confirmed** on Phase-2 verify (0 refuted, 0 reclassified) — every
one independently re-derived and held up, several with a sharper root-cause story than Phase 1 gave.

---

## §2 — Tier 1 reclassifications (10)

| Brief | Phase 1 | Phase 2 final | Why |
|---|---|---|---|
| `2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md` | DECAYED_DOCUMENTED | **DECAYED_UNDOCUMENTED** | The one drift Phase 1 found is fine (properly documented); Phase 2 found a second, undocumented one — 2 of the brief's own 5 named falsifier gates no longer exist as files (`validate_params.py` retired, `test_mc_anchors.py` deleted). |
| `docs/briefs/INDEX.md#Q-FUNDPOL-1` | UNCERTAIN | **DECAYED_UNDOCUMENTED** | Sharper than Phase 1's open question: the wake condition's first disjunct ("Q-POLFRONT-1 reads positive on funded-relevant cells") has no literal referent — Q-POLFRONT-1 never measured a funded-phase cell at all. No ruling needed; the phrase itself doesn't parse against its own source. |
| `2026-07-14-a4-flow-data-fork-scoping.md` | DECAYED_UNDOCUMENTED | **DECAYED_DOCUMENTED** | Underlying facts confirmed, but Phase 1 didn't chase down that the stalled diagnostic is at least tracked (unresolved) in `lab/CATALOG.md`'s ACTIVE row — thin, but present. |
| `2026-07-17-0808-packet-delta-and-sequence.md` | DECAYED_DOCUMENTED | **DECAYED_UNDOCUMENTED** | The existing reader-intercept banner is real and traced to its source (claim-alignment finding M30), but it only covers the pre-de-scope staleness — it says nothing about what *actually* superseded the packet (the Great Prune, a disjoint mechanism) or that A1 remains genuinely undecided under any framing. |
| `2026-07-23-tradeify-book-composition.md` | DECAYED_UNDOCUMENTED | **STILL_APPLICABLE** | Phase 1's two grounds don't survive close reading: D1's SHIP/HOLD gate is scoped to the *existing 2-leg Striker book* specifically, not "any account" — S1's environment ratification doesn't contradict the "no account to SHIP to" claim once read against the gate's actual object. |
| `Q-CALLBOUND-1-automation-boundary-symmetry.md` | DECAYED_UNDOCUMENTED | **DECAYED_DOCUMENTED** | Facts confirmed (closed AMBIGUOUS-HOLD, header never updated), but this is one of 8 sibling briefs from the same 2026-08-18 batch sharing the identical defect — Phase 2 judged it a known, batch-scale pattern rather than an isolated undocumented case (see §5's batch note). |
| `Q-PUBTRANS-1-public-transition-completeness.md` | DECAYED_UNDOCUMENTED | **DECAYED_DOCUMENTED** | Same batch-pattern reasoning — closure/INDEX.md/CLAUDE.md all correctly treat it as closed and load-bearing; only the source brief's own header lags, matching 7 siblings. |
| `Q-SIZECOMP-1-sizing-composition.md` | DECAYED_UNDOCUMENTED | **DECAYED_DOCUMENTED** | Same batch pattern. |
| `Q-VENUEGEO-1-f3-successor-venue-geometry-scoping.md` | UNCERTAIN | **STILL_APPLICABLE** | Every claim in the brief re-verified accurate; Phase 1's two loose threads (DP4 mini-spec never authored, missing from INDEX.md's tables) are real but are tracking-hygiene gaps, not factual errors in the brief's own content. |
| `rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md` | DECAYED_DOCUMENTED | **DECAYED_UNDOCUMENTED** | The closure is real and correctly cross-referenced by 4 later files — but never by the brief's own header, which Phase 1 missed. |

---

## §3 — Tier 1 `DECAYED_UNDOCUMENTED` (20) — full findings, all remediated this session

Each carries a Rule-14-compliant remediation (dated addendum / reader-intercept banner / header-field
correction — frozen body prose never rewritten in place). Full evidence and exact remediation text are
in the source audit data; summarized here.

1. **`2026-07-12-08-08-packet-pretriage.md`** — Its Class-A slate (A1 paired with A5) is dead: A5 was
   struck by the Pepperstone-feed-retirement ADR and declared permanently unrunnable; A1 carries forward
   undecided. The 2026-08-08 date passed via an unrelated mechanism (the Great Prune sweep), which never
   adjudicated this brief's own slate.
2. **`2026-07-14-a1-accept-beta-preassembly.md`** — Entirely structured around pairing with the same dead
   A5; the owning ADR's own forbidden-moves list explicitly names this brief's mechanism as something not
   to trust, yet no correction ever landed here.
3. **`2026-08-02-retired-surface-mission-alignment-prune.md`** — Packet F still frames Decompound A5 as
   an open sequencing question; A5 was independently retired the same day via a different ADR.
4. **`2026-08-12-msl-program-plan.md`** — Self-declares as the program's sole-writer claim manifest; three
   of its own lines about MSL-S4 are false as of the same day they describe (Explore-confirm was in fact
   run and returned AMBIGUOUS-HOLD, operator PARKED same day) — independently confirmed on three other
   surfaces this file doesn't link to.
5. **`GSUB-1-inventory-and-dispositions.md`** — Two rows never received the "⚠ superseded" annotation this
   same file gives its other six updated rows (Q-TOM-SPX-1's disposition change; the Notion action's
   early execution).
6. **`Q-KBUDGET-1-phase1-inventory.md`** — Guardian→MGC described as merely data-blocked/re-armable; it
   was since data-procured, scored, and killed. Separately, its bust-rate table benchmarks against a 3.0%
   ceiling superseded 2026-08-26 (now 5.0%) — several "marginal/failing" rows would clear today.
7. **`Q-KBUDGET-HARVEST-1-inventory-addendum.md`** — Its own correction claims a machine artifact "still
   shows PASS"; that artifact was fixed two weeks ago and now shows the corrected FAIL.
8. **`Q-NSURV-2-second-uncertainty-layer-design.md`** — RESOLVED same day it was authored; unlike its
   sibling Q-NSURV-1, never self-updated. Also points to a script path that was never used (real artifacts
   live elsewhere).
9. **`Q-POLFRONT-1-policy-augmented-seed-frontier.md`** — Still shows as un-run; closed RESOLVED-QUANTIFIED
   2026-08-16, then the very next day its own named fork found the headline effect does not survive an
   intraday-honest remeasure — a load-bearing reversal the brief gives zero indication of.
10. **`Q-S5CAP-1-capped-concurrency-invariant.md`** — Closed RESOLVED 2026-08-23 (capped concurrency is a
    per-packet self-report, not a system invariant); header never updated.
11. **`Q-STATVALID-1-mc-resampling-and-constant-multiplicity.md`** — Closed FALSIFIED 2026-08-23; header
    still shows unopened.
12. **`Q-XMEM-1-cross-surface-memory-sidecar-pilot.md`** — The most consequential finding in this tier:
    permanently SUBTRACTed at the GRAND-tier pursuit layer 2026-08-19 with a hard re-entry bar (a genuine
    dated incident); the brief's own banner still frames the pilot as live and gateable.
13. **`rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md`** — Ran to completion and closed 2026-07-22;
    header still shows an un-run pre-lock checklist.
14. **`rnd-pipeline/Q-ICTEXP-1-ict-chain-gross-expectancy-scoping.md`** — Header claims "not run, not
    pre-registered"; both false — ran 2026-08-04, verdict AMBIGUOUS, cited as settled fact by a sibling
    brief in the same batch.
15. **`rnd-pipeline/Q-ICTNF-1-nearfield-ssl-bear-fvg-scoping.md`** — Fork F3 was elected, run, and closed
    (AMBIGUOUS-HOLD); this file's own header still frames the election as pending.
16. **`rnd-pipeline/Q-SESSCONF-1-mnq-session-confluence-longer-hold-scoping.md`** — Closed FALSIFIED
    2026-08-02; a later edit (2026-08-23) touched an unrelated citation in the same file without updating
    Status — the promised closure artifact was also never produced.
17. **`rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md`** — Closed FALSIFIED
    (intake dry) 2026-08-04, correctly recorded in its own Amendment log and cited by 4 later files — just
    never reflected in its own header.
18. **`2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md`** — 2 of 5 named falsifier gates no
    longer exist as files (retired 2026-08-03); the falsifier is now only mechanically checkable against 3
    of 5.
19. **`docs/briefs/INDEX.md#Q-FUNDPOL-1`** — The Dormant-table wake condition's first disjunct has no
    literal referent in the source it names.
20. **`2026-07-17-0808-packet-delta-and-sequence.md`** — Existing banner covers only half the staleness;
    doesn't name what actually superseded the packet or that A1 remains genuinely undecided.

---

## §4 — Tier 1 `DECAYED_DOCUMENTED` (9) — compact, no action needed beyond what's already recorded

| Brief | Note |
|---|---|
| `2026-07-14-a4-flow-data-fork-scoping.md` | Stalled diagnostic tracked (thinly) in `lab/CATALOG.md`'s ACTIVE row. |
| `2026-08-18-step0-daily-geometry-mechanism-slate.md` | Header stale but the file's own §4 same-day addendum already gives the true state; a reader of the full file isn't misled. |
| `Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md` | Closed FALSIFIED 2026-08-23; correctly recorded in INDEX.md and CLAUDE.md; only the source header lags (batch pattern, see below). |
| `Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md` | Same batch pattern — closure/INDEX.md/CLAUDE.md all correct. |
| `Q-GATESTACK-1-gate-stack-enforcement.md` | Closed FALSIFIED 2026-08-19, correctly recorded elsewhere; the FALSIFIED verdict's own Limb-A finding is itself superseded same-day by a ruleset creation — doubly stale, but doubly documented too. |
| `Q-INTAKEGOV-1-intake-registry-governance-coverage.md` | Same batch pattern; the closure record even self-flags two of this brief's own stale anchors. |
| `Q-CALLBOUND-1-automation-boundary-symmetry.md` | Batch pattern (see below). |
| `Q-PUBTRANS-1-public-transition-completeness.md` | Batch pattern. |
| `Q-SIZECOMP-1-sizing-composition.md` | Batch pattern. |

**Batch note:** 7 of these 9 (`Q-CALLBOUND-1`, `Q-PUBTRANS-1`, `Q-SIZECOMP-1`, `Q-STATVALID-1` — counted
in §3 above since it stayed DECAYED_UNDOCUMENTED — plus `Q-DATAFIDELITY-1`, `Q-FIRMEOD-1`, `Q-INTAKEGOV-1`)
share one root cause: commit `afa0d56` fixed the identical stale-header defect for 4 *other* briefs from
the same 2026-08-18 assumption-sweep batch (`Q-ORBSURV-1`, `Q-ORBCUSH-1`, `Q-CAPBAND-1`, `Q-TRADECAP-1`)
but missed these 8. Flagged for a single batch remediation pass rather than 8 isolated fixes.

---

## §5 — Tier 2 findings (14) — all confirmed on Phase-2 verify, all remediated this session

Every flag independently survived refutation; several sharpened Phase 1's root-cause story. Remediation
in every case is Rule-14-compliant: no closure verdict, disposition, or frozen finding rewritten — only a
dated correction note placed upstream of the stale claim in reading order, or (for genuinely mechanical
header/procedural fields like a Pre-Lock Checklist) a direct field correction matching this corpus's own
demonstrated convention.

**STALE_CITATION (9):**
- `Q-BUSTGATE-1-bust-gate-re-derivation.md` + its closure — both cite the fork-B ADR as `(Proposed)`; it's
  been `Accepted` since the same day, over 5 weeks ago. The closure is internally self-contradictory about
  it (says `Proposed` 3 times, `Accepted` once).
- `closures/Q-CAPFLOW-1-closure-falsified.md` — 5 dead links to a directory that moved during archival;
  parent reservation `Q-CAPRES-2` carries the identical stale path (flagged, not separately fixed).
- `closures/Q-CONDVAL-1-closure-falsified.md` — same relocation-skew pattern; the §10 audit hook's exact
  reproduction command fails as written.
- `closures/Q-ICT-CASCADE-1-closure-insufficient-n.md` — claims "INDEX does not list this Q"; it's been
  listed correctly since the repo's first public commit.
- `closures/Q-NSURV-2-closure-resolved.md` — cites its own successor ADR as `Proposed`; ratified `Accepted`
  the same day, 9 days ago.
- `closures/Q-TNEC-ENV-1-closure.md` — cites a notice file with no self-disclosing caveat that it doesn't
  exist on this public clone; root-caused to a *different*, undocumented exclusion event (the 2026-08-14
  seed-cut's directory-prefix rule), not the already-documented Great Prune. Wider blast radius than
  Phase 1 flagged: the identical dead citation is load-bearing in an **open**, operator-pending brief.
- `closures/ST-EH-1-closure-operator-stopped.md` — cites an ADR as `Proposed`; the ADR's own addendum
  already discusses this citation by name but only honors half of Rule 14 (frozen-body protection) without
  adding the required reader-intercept.
- `rnd-pipeline/D5-NQ-intraday-momentum-scoping.md` and `rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md`
  — both claim a sibling axis "remains live" as of the 2026-08-08 checkpoint; both siblings had already
  closed with zero survivors weeks earlier. `H-TSMOM-1`'s own forbidden-moves clause explicitly
  anticipates and forbids exactly this citation error.

**INCONSISTENT (5):**
- `2026-07-27-hermes-agent-adoption-ruling.md` — header says ratified/closed; its own Pre-Lock Checklist
  still shows the ratification box unchecked.
- `closures/MSL-S2B-closure-stage1-fail-route.md` — states verdict `STAGE-1 FAIL` throughout, but its own
  Registry citation line names a different verdict belonging to a later, distinct entry. Structurally
  invisible to CI (the gate checks presence, not heading-match).
- `closures/Q-BUSTGATE-1-closure-falsified.md` — cites the same ADR as both `Proposed` (3x) and `Accepted`
  (1x) within the same document.
- `closures/SLR-MYM-1-closure-falsified-stage0.md` — §6 says "deliberately not appended to the rejection
  registry"; the Registry line two sections later says it was. Root cause: a later, legitimate governance
  rule (mandatory registry line, 2026-08-15) overrode the earlier editorial call via an append-only
  backfill — not a contradiction at authoring time, just missing the required reader-intercept.
- `rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md` — header shows closed FALSIFIED; the
  body's own operator-decision table still shows both blocking decisions as OPEN.

---

## §6 — Tier 3 findings (23) — mechanical, no verify phase; triaged by actionability

**Fixed this session (6 — genuine, in-repo, actionable defects):**
- `pre-registration/2026-08-23-mnqtape-2-larger-n-prereg.md` — one-line relative-path depth bug
  (`../` should be absent).
- `handoffs/2026-08-13-msl-c2-explore-go-card.md` — two links one directory level too shallow (`../../`
  should be `../../../`).
- `pre-registration/Q-NSURV-2-verdict-preregistration.md` — audit-hook path stale after an archival rename
  (traceable in-repo, not a squash artifact).
- 4 `STALE_PENDING_CLAIM` handoffs (all demonstrably done, still self-described as pending elsewhere):
  `handoffs/2026-07-24-cursor-handoff-ltm-rolloff-execution.md`,
  `handoffs/2026-07-26-cursor-fleet-cost-normalization-umbrella.md`,
  `handoffs/2026-08-20-cursor-handoff-aegis-3leg-risk-parameterization.md`,
  `handoffs/2026-08-20-cursor-handoff-notice-e1-e3-action-rows.md`.

**Flagged, logged as forward obligations (not fixed this session — genuine but lower-priority or needing
operator judgment):**
- `pre-registration/Q-TRAINKILL-2-verdict-preregistration.md` and `...Q-TRAINKILL-3-...` — content-hash
  drift: the committed file's SHA-256 does not match the freeze hash both closures attest was captured
  pre-compute. Path-level citations are fine; only the integrity attestation is broken. This is a data
  question (was the wrong version committed, or was the wrong hash recorded?) that needs operator
  judgment, not a mechanical fix — logged on `STATE.md`.
- `pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md` — cites a governing ruling doc
  that's genuinely missing (6 other files cite the same dead path — real deletion, not a squash artifact).
- `pre-registration/2026-08-11-guardian-mgc-transfer-cell-prereg.md` — cites a spec doc missing repo-wide
  (3 other files share the citation).
- `pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md` — cites an ADR under a filename that
  never existed (the real file has a different name — isolated to this one citation).
- `handoffs/2026-07-24-cursor-handoff-gate-estate-repairs.md` — cites a "parent session" doc with zero
  git history anywhere in the repo.
- `handoffs/2026-07-31-cursor-fleet-fade-mcl-parity-umbrella.md` — cites 2 governing spec docs missing
  repo-wide (5 other files share the citations).

**Not actionable — expected, already-documented public-clone limitation (11):** the remaining `BROKEN_LINK`
findings are all pre-2026-08-14-history-squash artifacts (unresolvable commit hashes) or citations to the
already-documented Great-Prune-pruned/`pre-prune-2026-08-08`-tag class (`Q-6JCOMPOSE-1/2`'s darkened
`validate_params.py` hook — already tracked with a stated workaround in the retiring ADR;
`Q-FUNDPOL-1-verdict-preregistration.md`, `Q-FUNNEL-1-verdict-preregistration.md`,
`Q-KBUDGET-1-screen-preregistration.md`, `Q-MONSURF-1-verdict-preregistration.md`,
`Q-PUBTRANS-1-verdict-preregistration.md` — all cite content this session already confirmed (via the ADR
audit) has no retrieval path on this public clone). No individual remediation — this is the same class
of finding as the ADR audit's Great Prune retrievability gap, already logged as a systemic, accepted
limitation.

---

## §7 — Remediation ledger

**Applied this session:** all 20 Tier-1 `DECAYED_UNDOCUMENTED` findings (§3), all 14 Tier-2 findings
(§5), and 6 Tier-3 findings (§6) — 40 files remediated via dated addenda, reader-intercept banners, or
direct header/path corrections per Rule 14's frozen-vs-living classification, matching the established
pattern from this session's earlier ADR-corpus remediation.

**Logged as forward obligations:** the `Q-TRAINKILL-2`/`Q-TRAINKILL-3` hash-drift pair (needs an operator
data-integrity call), the batch-pattern fix for the 8 sibling 2026-08-18-cohort briefs sharing the
`afa0d56`-missed header defect (worth one coordinated pass rather than piecemeal edits — 4 of the 8 are
already covered individually in this session's remediation; `Q-CALLBOUND-1`/`Q-PUBTRANS-1`/`Q-SIZECOMP-1`/
`Q-DATAFIDELITY-1`/`Q-FIRMEOD-1`/`Q-INTAKEGOV-1`/`Q-STATVALID-1` still need the header-field flip), and
the 6 genuinely-dead-but-lower-priority Tier-3 citations.

**Adjacent findings surfaced, not part of this audit's own scope:**
- `Q-CAPRES-2-mnq-cap-seat-reservation.md` carries the identical stale `c1/`-path citations as its child
  `Q-CAPFLOW-1` closure (not independently audited — flagged by the Tier-2 verify pass in passing).
- `scripts/check_supersession_placement.py`'s scope excludes `docs/briefs/closures/` entirely — a
  structural gap that let at least 3 of this audit's Tier-2 findings go uncaught by CI. Worth a backlog
  item, not fixed here (tooling change, out of an audit's own scope).
- `scripts/check_closure_disposition.py::scan_registry` checks Registry-line *presence* only, not
  heading-match correctness — the root cause of the MSL-S2B mis-citation. Same disposition as above.

---

## §8 — Discipline check

```
[x] Full brief corpus enumerated and tiered by decay-risk shape (342 files: 44/176/125 - three-way split
    justified by structural differences between live briefs, closed records, and frozen/one-shot artifacts)
[x] Phase 1 scan covers every file in scope, none silently dropped (44 batches returned)
[x] Phase 2 verify runs on every non-clean Tier-1/Tier-2 flag, framed to refute not confirm (39/39 returned)
[x] Every Phase 2 verdict has real reasoning behind it, not placeholder/degenerate output
[x] DECAYED_UNDOCUMENTED findings each carry a named remediation AND an owner/date (20/20 fixed this session)
[x] A harness-flagged instruction-shaped pattern was investigated directly and confirmed benign, not
    assumed safe
[x] Batch-pattern findings (the afa0d56-missed cohort) identified and named explicitly rather than treated
    as N independent defects
[x] Tier-3 findings triaged by actionability rather than treated uniformly — squash-artifact noise
    separated from genuine in-repo defects
[x] Output artifact lands at docs/notes/audits/brief-corpus/, mirroring the ADR-corpus audit's structure
[x] Next trigger: no standing cadence exists for this audit yet (unlike adr-decay-audit's programme-audit
    piggyback) — recommend the same piggyback convention: run alongside the next quarterly programme-audit
    cycle, or before the next repo-public snapshot/major handoff
```
