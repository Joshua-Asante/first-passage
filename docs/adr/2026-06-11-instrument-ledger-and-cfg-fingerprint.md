# ADR 2026-06-11 — Instrument-ledger rule + cfg-fingerprint convention (P1/P3 ratified; P2 forward-WIP cap NOT ratified)

**Status:** Accepted (P1 + P3) · P2 recorded as **not ratified** (§2c)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-06-11
**Authors:** Joshua (ratification) + Claude Code (placement); proposals authored by the 2026-06-11 cross-session review (claude.ai strategy sessions)
**Supersedes:** none
**Related:** [`docs/adr/2026-06-05-concept-admissibility.md`](2026-06-05-concept-admissibility.md) (R&D stage-1 gate this complements) · [`ops/instruments/USDCAD.md`](../../ops/instruments/USDCAD.md) (first ledger) · [`docs/ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md`](../ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md) (Amendment A1 = the FM#3 adjudication this review surfaced)
**Layer:** methodology / infrastructure (R&D session governance) — does not touch strategy code, allocations, dd_protection, or MC calibration

Single-decision note: this ADR records the ratification outcomes of ONE governance review (the 2026-06-11 memo, three proposals, one ratification event, shared rationale stream). Precedent for batching tightly-coupled outcomes in one ADR: [`2026-05-23-allocation-refresh-2.md`](2026-05-23-allocation-refresh-2.md).

---

## §0 — Rule 0 reads (production-source verification)

Read before authoring, in this session, all at worktree HEAD `de47e1d` (== `origin/main` at authoring time; currency verified via `git log HEAD..origin/main` → empty, 2026-06-11):

- [`docs/operational_rules.md`](../operational_rules.md) — anchor `de47e1d`. Confirms: Rule 8 is the §0-discipline home the memo's "§0 conventions" refers to; the maintenance bar ("rules earn their place by being paid for" — satisfied by the 2026-06-11 collision); Rules 5/7 ownership boundaries the ledger must not violate.
- [`docs/adr/2026-06-05-concept-admissibility.md`](2026-06-05-concept-admissibility.md) — anchor `de47e1d`. The stage-1 intake gate; the instrument ledger is cross-session state the intake gate does not carry (intake dedups concepts; it does not share anti-SNAG budgets or instrument findings between live parallel sessions).
- [`.claude/skills/pinescript-v6/SKILL.md`](../../.claude/skills/pinescript-v6/SKILL.md) — anchor `de47e1d`. P3 target surface (repo-side copy). The cloud-synced user-skill copy is NOT writable from disk; it requires the skill-authoring path (standing lesson: skill amendments via authoring path).
- Source artifacts (all `~/Downloads`, dated 2026-06-11): `GOVERNANCE-PROPOSALS-2026-06-11.md` (the memo), `USDCAD-LEDGER.md`, `REGIME-CALENDAR-2020-2026.md`, `FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md`, `SVRN_session_handoff_2026-06-11.md`, `SESSION-RECORD-USDCAD-BPC-2026-06-11.md`. Cross-checked per the web-handoff-confabulation discipline before placement:
  - BPC claims **verified** against the session record (entry-date Jaccard 0.96, Tuesday-by-year incl. 2024 +1.125R n=8, excl-2024 +0.164R n=84, Dukascopy disqualification).
  - SVRN ledger row **stale** vs its own cited handoff (`cfg05 = live best, cfg06–10 queue` vs handoff showing cfg10/11/12 already run, cfg10 BEST: N=204, PF 1.232, RF +1.93, DD 1.87%) — corrected at placement, correction logged in the ledger's session log.
- Repo-state verification: `ops/instruments/` and `ops/reference/` did not exist (new trees — no convention collision); repo-wide grep `USDCAD|SVRN|BPC|band-pierce|FWD-PREREG` → only `core/lib/dukascopy.py` (incidental symbol list), so no stale in-repo references to repair.

---

## §1 — Context

On 2026-06-11, multiple parallel strategy sessions ran on USDCAD. Two coordination failures surfaced at the cross-session review: (1) **the collision** — two sessions burned one instrument's shared anti-SNAG budget with mutually invisible forbidden moves and findings, and one session's pre-registration (BPC FM#3) accidentally captured another session's concept (SVRN v0.2-X15) in ambiguous wording; (2) **three relay defects** in the TV-export pipeline caught only by manual review (wrong timeframe, duplicate export, mislabeled subset). A third observation — generation throughput (3+ concepts that day) vastly exceeding forward-resolution throughput (~1 hypothesis/year at realistic trade rates) — motivated a proposed WIP cap.

The review produced three governance proposals (P1 instrument ledger, P2 forward-validation WIP limit, P3 cfg-fingerprint convention), none self-executing. Joshua ratified **P1 and P3** and declined **P2** on 2026-06-11 (AskUserQuestion, this session). The same ratification session adjudicated the FM#3 scope question (Reading A — recorded in the ledger and as pre-reg Amendment A1, which had to land before the forward window opens 2026-06-16).

**Decision driver (one sentence):** the memo requires P1 ratified before the next strategy session opens, and the FM#3 amendment is only clean while no forward data exists — both expire 2026-06-16.

---

## §2 — Decision

### §2a — P1: Instrument-ledger rule (RATIFIED)

Any session that derives, tests, tunes, or adjudicates on an instrument MUST (a) read `ops/instruments/<SYMBOL>.md` before its first run/edit, and (b) append a dated disposition entry at session end. Ledgers carry: active concepts + status, dead/parked items, durable instrument findings, the shared anti-SNAG budget, and open decisions. The anti-SNAG budget becomes **instrument-level and shared across sessions**, with family-level sub-ledgers where mechanisms genuinely differ. Ledgers are created on the first session touching a new instrument (no pre-emptive backfill — §5).

**Effective:** immediately. **Scope:** all R&D / strategy sessions on any surface (CC, claude.ai, cursor). Codified as [`docs/operational_rules.md`](../operational_rules.md) Rule 10; first ledger placed at [`ops/instruments/USDCAD.md`](../../ops/instruments/USDCAD.md).

### §2b — P3: Config-fingerprint convention (RATIFIED)

All ACTIVE-DERIVATION Pine scripts embed a cfg-ID in the strategy title (e.g. `"SVRN USDCAD v0.2-X15 [cfg10]"`), updated per run, so TV export filenames self-identify configuration. Step-0 of the reconcile pipeline parses and verifies the tag against the declared run. **Exemption: frozen/pre-registered scripts (e.g. BPC) are immutable and exempt; their exports are identified by the pre-registration itself.**

**Effective:** immediately for new ACTIVE-DERIVATION scripts; existing scripts (SVRN v0.2-X15) adopt at their **next legitimate edit** — not a standalone touch. Convention documented in the repo-side [`.claude/skills/pinescript-v6/SKILL.md`](../../.claude/skills/pinescript-v6/SKILL.md); the cloud-synced skill copy is updated via the skill-authoring path (§6 downstream).

### §2c — P2: Forward-validation WIP limit (NOT RATIFIED — recorded restraint)

The proposed programme-wide cap of 2 concurrent forward-validation slots was **not ratified** on 2026-06-11. No slot system takes effect; no queue ordering is in force. The BPC Tuesday forward test proceeds under its own pre-registration, which stands independently of P2. This declination is recorded here so its absence is a visible decision, not a silent drop (visible-restraint discipline). **Re-proposal path:** P2 is a process rule, not a rejected portfolio candidate — re-proposal does NOT require new mechanism evidence; it requires evidence that the absence of a cap is binding (e.g. concurrent unregistered forward tests accumulating, or in-sample evidence observably becoming the de facto decision basis).

**Context note (2026-06-12, Joshua + CC follow-up): the "~1 hypothesis/year" premise is conditional, not structural — and is far too small as a programme target.** The figure assumed (a) 2 slots, (b) BPC-class trade rates (~15 signals/yr Tuesday-only → C2 n=25 ≈ 24 months; the slowest concept class in the pipeline), and (c) counting only confirmations as resolutions. Throughput levers that scale forward resolution **without weakening pre-registered tests**:

1. **Parallelism** — forward demo tests compete for journaling fidelity (every-signal + skipped-signal logging), not capital; the binding constraint is a *capacity* cap set by demonstrated logging fidelity (edge-captured machinery), not a fixed small slot count. Concurrency disclosure rule: each pre-reg / ledger entry records how many forward tests ran concurrently, so a future "1 of K confirmed" reads with the right denominator.
2. **Trade-rate-aware queueing** — SE = σ/√n is denominated in trades, so calendar cost is purely signal-frequency-driven (n=25: ~24 mo at 15/yr vs ~2 mo at 150/yr). Among concepts of comparable expected information, the faster-resolving one goes first.
3. **Kills count as resolutions** — C1 kills land at n=12, and the intake base rate says most candidates die; resolution throughput is dominated by kill speed.
4. **Mechanism replication across path-independent instruments** — each its own registration, joint reading pre-specified (k-of-n), independence = different price path, not different feed (Jaccard-0.96 lesson).
5. **High-prior filtering before the forward gate** — the cheap-killer battery (cost-law pre-flight, excursion-bounded counterfactual, placebo/permutation, plateau, validation harness) spends zero forward days; the more it filters, the higher the confirm fraction per forward slot.

Non-levers (forbidden — they buy throughput by weakening tests): shrinking n floors (σ=1.15R at n=12 → SE ±0.33R), escalating on strong interims, peeking to rotate slow tests mid-window, early micro-allocation (live capital does not increase trade rate). **Irreducible bound:** confirmation throughput is capped by the true-edge base rate of the candidate stream — if confirmations stay ~1/yr after the levers above, that is the market's base rate, not pipeline underperformance. **Implication for any P2 re-proposal:** it should return as a fidelity-based capacity cap + the concurrency-disclosure rule, not a fixed cap of 2.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Status quo for cross-session state (SESSIONS.md + memory files) | Failed 2026-06-11: `docs/SESSIONS.md` is repo-chronological, not instrument-indexed; memory files are per-surface (CC project memory is invisible to claude.ai sessions). The collision happened *with both in place*. |
| Family-level ledgers only (per mechanism, no instrument file) | The collision was instrument-level — the shared anti-SNAG budget and the FM#3 scope ambiguity both live at the instrument, not the mechanism. P1 keeps family sub-ledgers *inside* the instrument file. |
| Manual export-naming discipline instead of P3 | Failed three times in one day (wrong TF, duplicate, mislabeled subset) with an attentive operator; the class needs to be machine-detectable at Step-0, not vigilance-dependent. |
| Ratify P2 as proposed | Declined by Joshua 2026-06-11 — recorded in §2c with re-proposal path. |
| Do nothing | The same parallel-session pattern that produced the collision is now the operating norm (multiple same-day sessions per instrument); recurrence is near-certain. |

---

## §4 — Falsifier (revert trigger)

**Hypothesis (falsifiable):** H: the ledger read+append rule and the cfg fingerprint each prevent their 2026-06-11 incident class at sustainable cost — concretely, (P1) sessions actually perform the read+append (no silent skips), and (P3) no fingerprint-class relay defect survives Step-0 on a cfg-tagged export. **Verdict mapping:** either trigger below fires → that decision is **FALSIFIED** and its revert action executes; neither fires through 2026-11-08 with ≥2 instrument-touching sessions of exposure → **RESOLVED** (load-bearing, rule stands); <2 instrument-touching sessions by 2026-11-08 → **AMBIGUOUS**, carry the evaluation to the next quarterly slate unchanged.

**P1 revert trigger:** if, at the 2026-11-08 quarterly review, ≥2 sessions since ratification that derived/tested/tuned on a ledgered instrument (identified from `docs/SESSIONS.md` entries naming the instrument) have **no same-date disposition entry** in that instrument's ledger, the rule is being skipped in practice. → Revert action: either add mechanical enforcement (session-start hook analogous to the M-9 pre-commit gate) or supersede/withdraw the rule — do not let it decay into ceremony.

**P3 revert trigger:** if a fingerprint-class relay defect (wrong timeframe / duplicate export / mislabeled subset) recurs on a cfg-tagged export AND Step-0 tag verification fails to catch it before analysis consumes the data, the convention is falsified as a detection mechanism. → Revert action: tighten (e.g. require the cfg-ID inside export rows, not just the title/filename) or supersede.

**Trigger check schedule:** quarterly slates 2026-08-08 (first look) and 2026-11-08 (P1 binary evaluation), alongside the standing portfolio regime trigger.

---

## §5 — Forbidden moves (under this ADR)

- **Pre-emptively backfilling ledgers for every historical instrument** (XAUUSD, XAGUSD, GBPUSD, EURUSD, USOIL, NAS100, DJ30, USDJPY all have history; the completeness urge is real). Ruled out by the operational-rules maintenance bar — rules earn their place. Ledgers are created on the first post-ratification session touching the instrument, seeded from that session's reads.
- **Letting ledgers restate strategy parameters or locked constants.** Ownership stays per operational rules 5/7 (Pine canonical for strategy params; `dd_protection.py`/`firm_rules.py` for sizing constants). Ledgers own instrument-level findings and concept status; everything else links out. A ledger that restates values becomes the next `STATE.md` drift incident.
- **Retro-tagging the frozen BPC pre-reg Pine with a cfg fingerprint** for convention uniformity. The P3 exemption is load-bearing: pre-registered scripts are immutable, and immutability wins.
- **Propagating P3 into SVRN v0.2-X15 as a standalone touch.** The memo's placement instruction is explicit: next legitimate edit only. A convention-only edit to an active-derivation script creates a phantom config generation.
- **Treating P2's declination as a rejected-candidates-registry entry.** Wrong layer — that registry's new-mechanism-evidence bar applies to portfolio candidates, not process rules. §2c states the actual re-proposal path.

---

## §6 — Consequences

**Positive:**
- Cross-session instrument truth exists at a known path; the anti-SNAG budget is shared and visible instead of per-session.
- The FM#3 collision class (one session's pre-registration ambiguously capturing another's concept) gets a standing resolution surface (ledger §Open/Resolved decisions).
- The relay-defect class becomes machine-detectable at reconcile Step-0.
- Regime attributions standardize on one calendar ([`ops/reference/regime_calendar.md`](../../ops/reference/regime_calendar.md)) instead of per-session narratives.

**Negative (real cost):**
- Per-session overhead on every instrument-touching session: one read at start, one append at end.
- Two new trees (`ops/instruments/`, `ops/reference/`) join the maintenance surface.
- cfg-tag churn in active Pine titles (a title edit per run during derivation).

**Risks:**
- Ledger staleness — observed at creation: the USDCAD draft's SVRN row was stale within hours of being written. Mitigation: the disposition append is mandatory at session END (not mid-session), owner-session anchors are named per row, and the placement correction is logged as the worked example.
- Regime-calendar [M]/[L] cells consumed as evidence without verification. Mitigation: calendar usage rule 1 + the verification pass due before 2026-08-08.

**Downstream artifacts updated (this commit):**
- [`ops/instruments/USDCAD.md`](../../ops/instruments/USDCAD.md) — placed (adjudication resolved, SVRN row corrected, session log appended).
- [`ops/reference/regime_calendar.md`](../../ops/reference/regime_calendar.md) — placed (canonical-path header + maintenance contract added).
- [`docs/ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md`](../ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md) — committed verbatim + Amendment A1 (FM#3 Reading A), anchoring the registration hash/date in git per its own audit hooks.
- [`docs/operational_rules.md`](../operational_rules.md) — Rule 10 added (P1).
- [`.claude/skills/pinescript-v6/SKILL.md`](../../.claude/skills/pinescript-v6/SKILL.md) — cfg-fingerprint section added (P3, repo-side copy). **Pending (Joshua, outside this repo):** mirror the same section into the cloud-synced pinescript-v6 user skill via the skill-authoring path.
- [`docs/SESSIONS.md`](../SESSIONS.md) — session entry.

---

## §7 — Implementation plan

All phases executed in the placement commit accompanying this ADR:

- **Phase 0** — §0 reads verified current at `de47e1d`; source artifacts cross-checked (one stale row found and corrected — see §0).
- **Phase 1** — placements + Rule 10 + skill section per §6 list.
- **Phase 2** — stale-reference sweep: repo grep for prior `ops/instruments`/`regime_calendar`/`FWD-PREREG` references → none pre-existing (new trees); ledger/calendar/pre-reg cross-links all point at the new canonical paths.
- **Phase 3** — verification block below run; status `Accepted`.

Not implemented (deliberately): P2 slot machinery (§2c); ledger backfill for other instruments (§5); SVRN Pine cfg-tag edit (§5 — next legitimate edit); cloud-skill mirror (requires skill-authoring path — flagged to Joshua).

---

## §10 — Audit hooks (runnable)

```bash
# P1 placed and codified
test -f ops/instruments/USDCAD.md && grep -n "Session log" ops/instruments/USDCAD.md
grep -n "ops/instruments/" docs/operational_rules.md
# Expected: Rule 10 present, pointing at this ADR

# P1 skip-detection (run at quarterly review): every SESSIONS.md entry naming a
# ledgered instrument should have a same-date ledger disposition
grep -n "USDCAD" docs/SESSIONS.md
grep -n "^- 2026" ops/instruments/USDCAD.md

# P3 convention present (repo-side skill)
grep -n "cfg-ID\|\[cfg" .claude/skills/pinescript-v6/SKILL.md
# Expected: convention section with title-tag example + frozen-script exemption

# FM#3 amendment landed pre-forward (must be dated before 2026-06-16)
grep -n "A1 — 2026-06-11" docs/ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md

# Regime-calendar maintenance trigger on the quarterly slate
grep -n "2026-08-08" ops/reference/regime_calendar.md

# P2 visible-restraint record (this ADR is the canonical record of the declination)
grep -n "NOT RATIFIED" docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md
```

---

## Verification

```bash
# Discipline checks (mechanical) — repo-side checker
python scripts/check_brief.py docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md --type adr
# Expected: PASS

# Production-source verification (Rule 0 confirmation)
git log --oneline -1   # de47e1d at authoring
git log HEAD..origin/main --oneline   # empty at authoring

# Downstream artifact update verification (§6 list)
test -f ops/instruments/USDCAD.md && test -f ops/reference/regime_calendar.md \
  && test -f docs/ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md \
  && grep -q "ops/instruments/" docs/operational_rules.md \
  && grep -q "\[cfg" .claude/skills/pinescript-v6/SKILL.md && echo ALL-PLACED
```

---

## Addendum — 2026-07-16 · Scoped §5 override (XAGUSD + EURUSD ledger creation)

**Status:** operator-approved exception to §5 “pre-emptive backfill” — **scoped**, not a general repeal.

**Trigger:** coverage inventory [`docs/notes/2026-07-16-instrument-ledger-coverage-inventory.md`](../notes/2026-07-16-instrument-ledger-coverage-inventory.md) (Approach C → B extract; durable + dead row types) found high-density corpus claims with **no** instrument card for XAGUSD and EURUSD, plus MISSING/PARTIAL rows on existing cards. Operator chose write fork **A + selective B** and explicitly approved creating the two missing cards (2026-07-16 session).

**What this override permits**
- Create [`ops/instruments/XAGUSD.md`](../../ops/instruments/XAGUSD.md) and [`ops/instruments/EURUSD.md`](../../ops/instruments/EURUSD.md), seeded only from existing registry + lab closures (link-out; no param restatement).
- Gap-close existing cards per the inventory §2b (XAUUSD, SPX500, USOIL status annotate, 6J→USDJPY SIBLING pointer).

**What this override does NOT permit**
- Pre-emptive cards for GC/MGC, MICRO10Y, GBPUSD, DJ30, or a full USDJPY card in this pass (remain creation-on-touch / deferred).
- A standing doctrine change: §5’s default remains “create on first post-ratification session.” Future NO_LEDGER symbols still need an operator GO or a live touching session.

**Plan:** [`docs/superpowers/plans/2026-07-16-instrument-ledger-coverage-ab.md`](../superpowers/plans/2026-07-16-instrument-ledger-coverage-ab.md).

---

## Addendum — 2026-07-16 · Regime calendar inlined into USDCAD ledger

**Status:** operator-directed. The shared USDCAD regime calendar formerly at `ops/reference/regime_calendar.md` is now a section of [`ops/instruments/USDCAD.md`](../../ops/instruments/USDCAD.md) (`## Regime calendar`). `ops/reference/` deleted. Sentinel obligation/precondition scans retarget that section (Tag-column `[M]`/`[L]` only — not whole-file token match). Durable outcomes unchanged; no second file to point at.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-11 | Initial authoring; P1+P3 ratified, P2 declined, FM#3 adjudicated Reading A | Joshua + Claude Code |
| 2026-06-12 | §2c context note added: the ~1 hypothesis/yr premise is conditional (slots × trade rate × confirmations-only counting); throughput levers + non-levers + irreducible base-rate bound recorded; shapes any P2 re-proposal (fidelity-based capacity cap + concurrency disclosure, not fixed 2). Decision unchanged. | Joshua + Claude Code |
| 2026-07-16 | Addendum: scoped §5 override for XAGUSD + EURUSD ledger creation + A-side gap-close (inventory-backed). Default §5 doctrine unchanged for other symbols. | Joshua + Cursor |
| 2026-07-16 | Addendum: regime calendar inlined into USDCAD ledger; `ops/reference/` removed. | Joshua + Cursor |
