# Sourcing-phase channel retirement: structural flow census + Avenue A Route B generate→confirm — `2026-08-24-sourcing-phase-channel-retirement`

**Status:** `Proposed` — drafted this session; awaiting adversarial pre-ratification review and explicit operator GO before Accept (see §7).
**Decision date:** 2026-08-24
**Supersedes:** `2026-07-26-mechanism-counterparty-constraint-boundaries.md` in part — clause 2-B only (structural flow census sourcing channel); clauses 2-A and 2-C untouched
**Supersedes:** `2026-08-05-avenue-a-generate-confirm-route.md` full
**Supersedes:** `2026-08-08-edge-cohort-correction-and-necessity-retarget.md` in part — §2-C row L1 only (Route B lane disposition); rows L2–L5 and §2-A/§2-B untouched
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction) + Claude Code (drafter)
**Layer:** methodology (sourcing-phase channel taxonomy + research rules of evidence only). No `dd_protection`, allocation, lifecycle, Pine, or rail config touched; nothing armed; no venue action; no spend.

---

## §0 — Rule 0 reads (production-source verification, this session 2026-08-24)

- `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md` — anchor `aef55a9` (2026-08-23), full read. Clause 2-B: "if by the second quarterly audit after ratification the census has produced zero seeds that pass the §3 intake screen, the channel is dead weight — retire the rank." Trigger check schedule rides 2026-11-08 / 2027-02-08. Clauses 2-A (four-clause mechanism definition) and 2-C (executed-K closure rule) confirmed unrelated to the census and left untouched by this ADR.
- `docs/adr/2026-08-05-avenue-a-generate-confirm-route.md` — anchor `1a07c35` (2026-08-21), full read. Status `Accepted`; §4 falsifier's empirical limb requires "two completed Route B confirm campaigns that printed `RESOLVED` on CONFIRM" — structurally unfireable since zero campaigns, ever, have printed `RESOLVED` on CONFIRM. §7 item 4 pre-specifies the exact revert mechanics this ADR now executes: "Avenue A §6's addendum block must be withdrawn in the same change."
- `docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md` — anchor `1a07c35` (2026-08-21), full read. §2-C row L1: Route B's one tried family "PAUSED... Avenue A Route A/B doctrine itself is untouched," reopening path stated (a redesigned tradeable-object promotion floor). Row L2: "The structural-flow census stays closed (5 dry passes)" — an independent, second ratified statement of the census's dead status, corroborating clause 2-B.
- `docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md` §6 — anchor `1a07c35` (2026-08-21). Condition 3 carries the frozen original ("Survivor-tied... not blind discovery") plus a later addendum block adding "(Route B) generate→confirm under `avenue_a_generate_confirm.md`" — confirmed the addendum is additive, not a rewrite of the frozen text, per the file's own explicit convention.
- `docs/methodology/avenue_a_generate_confirm.md` — anchor `1a07c35` (2026-08-21), full read. The runnable Route B checklist (Stage G / Stage C, G0–G3, C0–C3), currently live.
- `docs/methodology/strategy_harvest.md` §2.3 — anchor `ac05de6` (2026-08-24). Ranked channel portfolio; rank "1-tie" is the structural flow census.
- `docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md` — anchor `1a07c35` (2026-08-21), full read. Entry condition (a): "an Avenue A §6 amendment ADR that reopens blind..." — a 2026-08-05 addendum block already names that ADR as the discharged reopen *path* (brief itself stays `DRAFTED — NOT OPENED`).
- `docs/pursuits/c5-q-mschan-1.md` — anchor `1a07c35` (2026-08-21), full read. GRAND-tier SUBTRACT disposition (ratified 2026-08-09, GSUB-1 Phase 3). "Test applied" field states plainly: "Route B (generate→confirm) is live under pursuit a3 and already supplied the depth census this brief's Stage 1 would otherwise have needed." Re-entry armor explicitly points at the 2026-08-05 ADR. Both claims go stale on full retirement of that ADR.
- `STATE.md` — anchor `eaf5574` (2026-08-24). 2026-11-08 forward-trigger row: "Mechanism-boundaries ADR §4 — clauses 2-A / 2-B / 2-C first check."
- `docs/adr/INDEX.md` — anchor `2de171d` (2026-08-24), re-verified after adversarial review. **Correction (adversarial-review BLOCKER 1):** the baseline is NOT clean — `docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md` already carries `**Superseded-in-part-by:** \`2026-08-12-msl-sourcing-channel-ratification.md\` — §2-C L2 channel taxonomy by addition only (MSL named as a sourcing channel); 2-A/2-B and L1/L3–L5 untouched.` That prior edge targets row **L2** (unrelated to this ADR's row **L1** edge), so it does not conflict — but §6/§7's instruction to add "a `Superseded-in-part-by` line" is corrected below to mean *append a second line*, never overwrite. The other two touched ADRs (`2026-07-26-mechanism-counterparty-constraint-boundaries.md`, `2026-08-05-avenue-a-generate-confirm-route.md`) do have a genuinely clean baseline — verified directly, no existing `Superseded-by`/`Superseded-in-part-by` entries on either.
- Repo-wide grep sweep (Phase-2 discipline). **Correction (adversarial-review BLOCKER 2):** the counts and "raw output pasted in §10" claim below were both wrong at initial authoring — re-run and verified 2026-08-24 post-review: `structural flow census|forced-flow census|N-2026-07-26-forced-flow-census|1-tie` → **35 files** (not 26 — see §10 hook 2 for the corrected raw list and disposition of the 7 previously-missed hits, 2 of which are genuine census citations this ADR had not accounted for). `Route B|generate.{0,3}confirm|2026-08-05-avenue-a|avenue_a_generate_confirm|Avenue A` → **75 files** (not 70 — see §10 hook 3 for the corrected raw list). Every hit in the corrected lists is individually dispositioned in §10, not merely summarized — the original §10 pasted prose conclusions instead of the actual filenames, which is fixed below. The root cause of the original undercounts was not determined (files may have changed between the original sweep and the correction, or the original tool call under-matched `lab/archive/`); the corrected counts are the ones this ADR now relies on.

---

## §1 — Context

This session ran a citation-backed audit of an operator-provided sourcing-phase pipeline mapping (a Design-canvas artifact external to this repository, describing the estate's candidate-sourcing process as 23 numbered steps across four parallel channels) against this repo's actual execution history (four parallel research threads over `lab/CATALOG.md`, `docs/rejected_candidates.md`, `docs/briefs/INDEX.md`, and the governing ADRs), at the operator's request, to find steps that could be deleted or simplified given what has actually fired versus what is doctrine-only. **Note (adversarial-review CONCERN):** the "23-step"/step-numbering language is this session's own paraphrase of that external artifact, not a citation to any in-repo document — no file in this tree enumerates 23 steps or labels a range "18–22"; every substantive claim below is instead grounded in the repo's own ADRs/CATALOG/closures cited by file path. Two of the mapped phase's four sourcing channels came back zero-yield across their entire recorded life in this repo, independent of each other's evidence:

**Structural flow census** (`strategy_harvest.md` §2.3 rank "1-tie"): 4–5 real passes (2026-07-26 → 2026-08-01), ~24 individually-reasoned entries, one (F1) developed to its own dedicated falsification ruling — genuinely exercised, not merely defined on paper — and still **zero admissible seeds, ever**. Its own falsifier (clause 2-B) is substantively met; a second, independent ADR (`2026-08-08-edge-cohort-correction-and-necessity-retarget.md` §2-C row L2) already calls it "stays closed."

**Avenue A Route B (generate→confirm)**: 4 campaigns opened at G0 (Q-OFCHAN-1, Q-R2FLOW-1, Q-R2VBUCK-1, Q-R2AGRUN-1), all 4 died at the explore stage (empty candidate list or a magnitude-floor miss an order of magnitude short), and **0/4 ever reached the confirm stage** — the elaborate C0 freeze / multiplicity-adjusted C1–C2 run / C3 verdict machinery has never executed once, in the mechanism's entire life. The governing ADR's own §4 empirical falsifier requires a `RESOLVED` CONFIRM verdict to exist before it can even evaluate — so it can structurally never fire, in either direction. The 2026-08-08 ADR already paused the one family tried, on design grounds (promotion floor ~0.3pt/1σ vs. a round-trip cost the venue actually charges of **~1.41pt** — verified directly against `core/firm_rules.py:378` (`Tradeify_Select_100K` `cost_per_side_usd: 0.91`) and `lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage6.md:41` ("Tradeify $0.91/side → RT ≈1.41pt"); **correction (adversarial-review CONCERN):** this ADR originally restated the 2026-08-08 ADR's own "~0.95 pt round trip" figure uncritically — 0.95 is MFFU/BluSky's per-side *dollar* commission (`core/firm_rules.py:509`), not a Tradeify round-trip point figure at all, and that error is inherited-and-uncorrected in the source ADR, not fixed here (out of this ADR's scope; the design-flaw conclusion is unchanged and if anything strengthened, since the true cost gap is wider than originally stated, not narrower)), but left the mechanism itself formally `Accepted` with an explicit reopening path.

Presented with this record, the operator elected **full retirement** of Route B (not merely formalizing the existing single-family pause), on the grounds that 0-for-4 across the mechanism's whole life — not just the one tested family — is sufficient regardless of the un-tripped falsifier, and that carrying a formally-live-but-never-successful mechanism costs ongoing citation-drift risk (concretely realized in `docs/pursuits/c5-q-mschan-1.md`, whose ratified SUBTRACT disposition already cites Route B as live "armor" for a re-entry decision) for no measured benefit.

**Decision driver (one sentence):** two sourcing channels are formally `Accepted`/open while every measured outcome in their history says otherwise, and at least one downstream ratified decision (`c5-q-mschan-1.md`) is already relying on that stale liveness as a load-bearing fact.

---

## §2 — Decision

**Decision, two clauses, separable at ratification** (mirrors the "three clauses, separable" shape of the ADR this partially supersedes, and the multi-row lane-disposition shape of the 2026-08-08 ADR §2-C):

**(a) Structural flow census retired as a sourcing channel.** `2026-07-26-mechanism-counterparty-constraint-boundaries.md` clause 2-B is superseded in part: the census's "1-tie" rank is struck from `strategy_harvest.md` §2.3's channel portfolio. Clauses 2-A and 2-C, and every other channel rank, are unaffected. The census's own required fields (four WHO/WHEN/WHY/HOW clauses, venue check, family K-bank disclosure, graveyard-adjacency attestation) and its Notice-phase recording convention are retired alongside it — no future entry opens under this rank.

**(b) Avenue A Route B (generate→confirm) retired in full.** `2026-08-05-avenue-a-generate-confirm-route.md` is superseded in full. Avenue A §6 condition 3 reverts to its frozen original wording (survivor-tied only) via withdrawal of the Route B addendum block, per that ADR's own §7 pre-specified revert instruction. The `avenue_a_generate_confirm.md` checklist is marked withdrawn — no future campaign may open a G0 freeze under it. `2026-08-08-edge-cohort-correction-and-necessity-retarget.md` §2-C row L1 is superseded in part: its disposition for the OF-minute catalogue family changes from `PAUSED` to `RETIRED (subsumed by full mechanism retirement)`; rows L2–L5 are unaffected.

**Effective:** on operator Accept (Status flips to `Accepted` only after §7 Phase 2's disposition sweep and adversarial review are complete — see §7).
**Scope:** the sourcing-phase channel taxonomy (`strategy_harvest.md` §2.3) and the Avenue A generate-confirm mechanism in its entirety — all instruments/schemas it was ever scoped to reach, not only the one order-flow-minute family actually tried. Route A (survivor-tied) is explicitly unaffected. Neither harvest (Branches B1–B6), the deep-iteration lane (GROW/DL), nor the classic mining stack (STUMPY/ruptures/catch22) is touched by this ADR.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Wait for clause 2-B's formal check date | **Corrected (adversarial-review CONCERN — the original row here conflated the two scheduled dates):** clause 2-B's own trigger text requires "the second quarterly audit after ratification" (`2026-07-26-mechanism-counterparty-constraint-boundaries.md` §4), and both that ADR's own §7 Phase 3 ("first §4 check rides 2026-11-08") and `STATE.md`'s forward-trigger row (labeling 2026-11-08 the "first check") confirm 2026-11-08 is the *first* of the two scheduled audits, not the second — the literal trigger date is **2027-02-08**, roughly 5.5 months out, not 2.5. The condition it checks (zero seeds by second quarterly audit) is already met twice over regardless (this ADR's own record and the independent 2026-08-08 L2 finding); waiting adds no new information and leaves a known-dead channel presenting as live for ~5.5 more months, not 2.5. This timing correction does not change the retirement decision, which rests on the substantive 0-for-4/0-for-4 operator override (§1, row 2 below), not on either scheduled date having arrived. |
| Retire only the one paused Route-B family; leave the mechanism formally `Accepted` for a future redesigned family | The fork the operator was offered this session. Rejected 2026-08-24: 0/4 across the mechanism's *entire* life (not just the one family) was judged sufficient on its own, and a formally-live-but-dormant mechanism has already produced one concrete citation-drift incident (`c5-q-mschan-1.md`'s re-entry armor). |
| Status quo — leave both channels' current status unedited | Both channels' "Accepted"/formally-open status actively misleads: the 23-step sourcing-phase document presents them as co-equal to the two channels that actually work (harvest, deep-iteration lane), and at least one ratified downstream decision already treats Route B's liveness as a fact it relies on. |
| Fold this into a new promotion-floor redesign for Route B instead of a pure retirement | Conflates two different decisions (kill the current grant vs. author a corrected successor) and would require pre-committing to redesign specifics the operator has not yet reviewed. This ADR retires the standing grant only; nothing in it bars a fresh ADR from reopening either channel under corrected design (§5). |

---

## §4 — Falsifier (revert trigger)

**H:** the zero-seed record this ADR relies on for both channels is complete and accurate, and no admitted seed from either channel exists that this ADR's §0 evidence missed.

**Revert trigger (either limb falsifies the relevant clause only):**
1. **Factual — FALSIFIED iff:** an audit surfaces an admitted seed, ever, from the structural flow census or from any Route B campaign (any family, any instrument) that this ADR's §0 did not account for. **RESOLVED iff:** no such seed is ever surfaced. → on FALSIFIED, the retirement's factual premise is wrong for that clause; author a fresh superseding ADR correcting the record before either channel may be treated as retired again.
2. **Starvation — AMBIGUOUS iff:** at the next 2 quarterly programme audits after ratification, the surviving sourcing channels (harvest, deep-iteration lane) are themselves found zero-yield/degenerating, **and** no successor ADR reopening either retired channel under corrected design has been authored in the interim. **RESOLVED iff** either condition fails to hold (channels still productive, or a redesign has already been authored). → on AMBIGUOUS, the programme audit must explicitly rule on whether channel starvation, not channel quality, is now the sourcing phase's binding constraint, and whether a redesigned reopening of either retired channel is warranted.
3. **Early-closure legitimacy — FALSIFIED iff:** an independent re-examination at (or before) 2027-02-08 — clause 2-B's own literal "second quarterly audit" trigger date, which this ADR elects to preempt on judgment rather than wait for — finds that the 0-for-4/0-for-4 record this ADR relies on does not, in fact, support closing ahead of that schedule (e.g., a material campaign or finding existed at authoring time that this ADR's §0 missed, distinct from limb 1's narrower "an admitted seed was missed" test). **RESOLVED iff** that re-examination affirms the early closure was sound. This limb exists because limbs 1–2 above test the record's completeness and the *surviving* channels' future health, but neither one asks whether short-circuiting the pre-registered schedule on judgment, rather than new evidence, was itself the right call — a gap confirmed by adversarial review (BLOCKER 3) and closed by adding this limb. → on FALSIFIED, the retirement stands as a factual matter (the channels are still dead) but the *process* of closing early without waiting for new evidence is flagged as a precedent not to repeat; no automatic reversal of clauses (a)/(b).

**Revert action:** a fresh ADR supersedes this one (full or in-part per the standard edge rules); never a silent edit of this decision text.
**Trigger check schedule:** limb 1 — on demand, any time a contradicting seed is found. Limb 2 — rides the standing programme-audit dates (next two after 2026-08-24). Limb 3 — a dedicated check at 2027-02-08 (see the corresponding `STATE.md` forward-trigger row added under §6/§7).

---

## §5 — Forbidden moves (under this ADR)

- **Reopening either channel informally** (a Notice-log entry, a quick unscoped campaign) rather than a fresh ADR under corrected design. Genuinely tempting: both channels' checklists (`avenue_a_generate_confirm.md`, the census's own required-fields list) still sit in the tree post-retirement and would make an informal revival trivial. Re-entry requires a new ADR naming what changed in the design (per §3's redesign alternative) — never a lookup of the old grant.
- **Reading this ADR as touching Route A (survivor-tied)** or the general "freeze exploration before any peek" discipline pattern Route B popularized. Route A is explicitly unchanged. The G0-freeze principle is broader than this one mechanism — `docs/spec/2026-08-22-grow-lane-generate-refine-spec.md` D1 already imported it as a standalone principle for the GROW lane, independent of Route B's continued existence (confirmed this session: `lab/discovery/grammar.py:100` cites the rule generically, not as a Route B liveness claim — reviewed, no action needed).
- **Silently editing the frozen text of clause 2-B or §2-C row L1** instead of appending a dated addendum. Known Trap #12 / dated-decision integrity — the exact pattern this repo already uses for surgical single-clause amendments (the existing 2026-08-08 addendum narrowing the family-K-floor arithmetic on the same ADR being touched here).
- **Treating this ADR as extending to the Branch A mining stack** (STUMPY/ruptures/catch22/tsfresh/HMM/PySR) or the deep-iteration lane. Those channels were separately audited this session and are out of scope for this decision; the K-wall/DSR-floor finding that deprioritized Branch A mining is unrelated to why these two channels are being retired here.

---

## §6 — Consequences

**Positive consequences:**
- The sourcing-phase documentation stops presenting two zero-yield channels as co-equal to the two that actually work (harvest, deep-iteration lane).
- `c5-q-mschan-1.md`'s stated re-entry armor gets corrected before it misleads a future GRAND-tier re-entry decision, and `a3-mnq-discovery-pipeline.md`'s own title (which names "Route A/B" as live scope) stops misrepresenting an active, ratified KEEP pursuit's actual boundaries.
- The operator's external sourcing-phase pipeline mapping shrinks by five of its mapped steps (the census channel and the four generate→confirm stages), with the audit trail this ADR provides standing in place of the elaborate confirm-machinery detail that never executed.

**Negative consequences (real cost):**
- The census's "cheap enumeration, zero K until graduation" property and Route B's order-flow/depth-data generate→confirm shape are both real capabilities a future researcher must now re-derive from scratch (fresh ADR, fresh design) rather than reactivate directly.
- The executed-K closure rule (clause 2-C, untouched) loses one of the two contexts (structural-flow-census seeds) it was written to cover, though ST-EH-1 remains its worked example.

**Risks:**
- Retiring a mechanism whose only diagnosed design flaw (promotion floor too weak) is fixable in principle forecloses cheap resumption of the *current* grant. Mitigated: §5's re-entry path stays open via a fresh ADR: nothing here bars a corrected-design successor.

**Downstream artifacts that need updating** (derived from the §0 grep sweep, dispositioned; raw output in §10):
- `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md` — dated addendum after clause 2-B (pattern: the existing 2026-08-08 addendum on the same file), `Superseded-in-part-by` line added.
- `docs/adr/2026-08-05-avenue-a-generate-confirm-route.md` — full retire: `Status: Superseded`, `Superseded-by:` this ADR, body moved to `docs/ltm/adr/`, hot file stubbed (accept+retire checklist, §7).
- `docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md` — dated addendum after §2-C row L1; a **second** `Superseded-in-part-by` line **appended** below the existing 2026-08-12 MSL-ratification entry (which targets row L2 and stays exactly as-is — never overwritten); L2–L5 untouched.
- `docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md` §6 — withdraw the Route B addendum block (per that ADR's own §7 pre-specified instruction); frozen original condition-3 text stands alone again.
- `docs/methodology/avenue_a_generate_confirm.md` — header banner: `Withdrawn`, pointer to this ADR.
- `docs/methodology/strategy_harvest.md` §2.3 — strike the "1-tie" row, pointer to this ADR.
- `docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md` — entry condition (a)'s pointer to the now-superseded 2026-08-05 ADR gets a dated intercept noting the reopen path requires a fresh ADR, not a lookup of the retired one.
- `docs/pursuits/c5-q-mschan-1.md` — banner noting its "Test applied"/re-entry-armor citations to Route B are now stale; re-entry (if ever pursued) needs fresh evaluation, not a citation to the retired grant.
- `docs/pursuits/a3-mnq-discovery-pipeline.md` — **its own numbered fix (adversarial-review CONCERN: this was previously folded into the c5 item as a parenthetical, which undersold that a3 is a live, ratified `Class (a) active campaign · KEEP` pursuit, not a dormant record like c5)**: its title ("MNQ discovery pipeline (TNEC intake · Route A/B · CapFLOW · dense-1m/instrument/W1)") names "Route A/B" as active scope; banner the title/body to reflect Route B's retirement (Route A stays; TNEC intake, CapFLOW, dense-1m/instrument/W1 are unaffected and out of this ADR's scope).
- `STATE.md` — three edits: (i) the 2026-11-08 forward-trigger row gets a note that clause 2-B was discharged early by this ADR (2-A/2-C keep their own unaffected check); (ii) a new dedicated forward-trigger row for §4 limb 2 (starvation check, next two programme audits); (iii) a new dedicated forward-trigger row for §4 limb 3 (early-closure-legitimacy check, due 2027-02-08 — clause 2-B's actual literal trigger date this ADR preempts).
- `docs/adr/INDEX.md` — mechanically regenerated (`check_adr_graph.py --regenerate-index`), not hand-edited.
- The remaining hits from the corrected §10 sweeps (35 + 75, minus the 12 action owners above and 2 self-citations to this ADR itself) are frozen campaign/session history (closed `PREREG`/`RESULTS`/closures, per-instrument ledger citations, session narrative, cold-stored `docs/ltm/adr/`) — reviewed, no edit, per this repo's own convention that history stays history. Two exceptions worth naming: `lab/archive/approach_scoreboard_2026-08/{PREREG,RETRO_MAP}.md` and `lab/archive/tnec_envelope_compile_2026-08/{PREREG,RESULTS}.md` are genuine, previously-uncounted citations of the census channel (all four already-archived, frozen history — no edit owed, but now correctly counted rather than missed). A separate false-positive was also found and is worth flagging for the pattern's own future use: `lab/archive/class_s_aegis_solo_scoring_2026-07-16/{HANDOFF,RESULTS,run_aegis_solo_scoring.py}` matched the `1-tie` fragment only because it appears inside the unrelated filename `2026-07-16-aegis-6j-prop-reconstruction-**v2.1-tie**break-prereg.md` — not a real census citation.

---

## §7 — Implementation plan

- **Phase 0** — DONE, this session: §0 reads verified current; repo-wide grep sweep run (raw output §10); the two ambiguous hits most likely to carry live claims (`c5-q-mschan-1.md`, `lab/discovery/grammar.py`) individually read and dispositioned.
- **Phase 1** — OWED, gated on operator Accept: execute the eleven file edits enumerated in §6, in the order: (i) addendum on 2026-07-26 clause 2-B; (ii) addendum on 2026-08-08 §2-C row L1 — **append** a second `Superseded-in-part-by` line below the existing 2026-08-12 MSL-ratification entry (L2), never overwrite it; (iii) withdraw the Route B addendum block on the 2026-07-24 brief §6; (iv) mark `avenue_a_generate_confirm.md` Withdrawn; (v) strike the "1-tie" row in `strategy_harvest.md` §2.3; (vi) intercept on Q-MSCHAN-1's entry condition (a); (vii) banner on `c5-q-mschan-1.md`; (viii) banner on `a3-mnq-discovery-pipeline.md`'s title/body; (ix) three STATE.md forward-trigger row edits (2-B early-discharge note, new §4-limb-2 row, new §4-limb-3 row due 2027-02-08); (x) disposition the `approach_scoreboard_2026-08` and `tnec_envelope_compile_2026-08` census citations found by the corrected sweep (no edit expected — confirm and record); (xi) full accept+retire of `2026-08-05-avenue-a-generate-confirm-route.md` via `scripts/retire_adr.py 2026-08-05-avenue-a-generate-confirm-route --reason superseded --by 2026-08-24-sourcing-phase-channel-retirement` (or hand-equivalent), including its own residual-inbound-refs sweep.
- **Phase 2** — OWED: dispositioning of the remaining raw grep hits not already covered in Phase 1 (confirm none require action beyond what §6 already dispositions); `check_adr_graph.py --regenerate-index` run and diff included; `check_brief.py` + `check_adr_graph.py` both exit clean.
- **Phase 3** — OWED: adversarial pre-ratification review, then explicit operator GO; only then does Status flip `Proposed` → `Accepted` in the same change as Phase 1–2 landing.

This ADR is **not** self-executing — per the "Proposed successors declare pending edges" rule, none of the three superseded/in-part-superseded ADRs are touched while this one stays `Proposed`. CI stays green; the reverse edges and cold-store shape become mandatory only on Accept.

---

## §10 — Audit hooks (runnable)

```bash
# 1. This ADR's status (expect Proposed until Phase 3 completes)
grep -n "^\*\*Status:\*\*" docs/adr/2026-08-24-sourcing-phase-channel-retirement.md

# 2. Structural-flow-census sweep (corrected raw output, re-run + pasted 2026-08-24 post-review) — 35 files
grep -rlI "structural flow census\|forced-flow census\|N-2026-07-26-forced-flow-census\|1-tie" \
  --include='*.md' --include='*.py' . 2>/dev/null
# Expected hits (2026-08-24, corrected count = 35):
# docs/SESSIONS.md
# docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md
# docs/adr/2026-08-13-dedup-first-before-new-work.md
# docs/adr/2026-08-15-notice-log-is-the-live-observation-routing-convention.md
# docs/adr/2026-08-24-sourcing-phase-channel-retirement.md    (self-citation, expected)
# docs/adr/INDEX.md                                             (self-citation, expected)
# docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md
# docs/briefs/closures/2026-07-16-aegis-6j-prop-reconstruction-stage2-hsolo-falsified.md
# docs/briefs/closures/MNQBASE-1-closure-intake-dry.md
# docs/briefs/closures/Q-TNEC-ENV-1-closure.md
# docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md
# docs/briefs/rnd-pipeline/Q-SESSCONF-1-mnq-session-confluence-longer-hold-scoping.md
# docs/methodology/strategy_harvest.md                          (action owner, §6)
# docs/notes/audits/2026-08-23-kill-register-attribution-audit.md
# docs/notes/notice/N-2026-08-14-msl-who-track.md
# docs/notes/notice/N-2026-08-24-b2-london-fix-wake-cost-arithmetic.md
# docs/notes/research/2026-08-24-cot-positioning-reversal-harvest-sourcing.md
# docs/operational_rules.md
# docs/superpowers/plans/2026-08-20-cross-campaign-mechanism-prior.md
# docs/superpowers/plans/2026-08-23-viable-strategy-phase-a-target-derivation.md
# docs/superpowers/specs/2026-08-20-cross-campaign-mechanism-prior-design.md
# lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/SWEEP_LOG_v2.md
# lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md
# lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/SOURCES_LOG.md
# lab/archive/approach_scoreboard_2026-08/PREREG.md             (previously missed — genuine census citation, frozen/archived, no edit)
# lab/archive/approach_scoreboard_2026-08/RETRO_MAP.md          (previously missed — genuine census citation, frozen/archived, no edit)
# lab/archive/class_s_aegis_solo_scoring_2026-07-16/HANDOFF.md  (FALSE POSITIVE — "1-tie" matches inside "v2.1-tiebreak-prereg.md", not a census citation)
# lab/archive/class_s_aegis_solo_scoring_2026-07-16/RESULTS.md  (FALSE POSITIVE — same cause)
# lab/archive/class_s_aegis_solo_scoring_2026-07-16/run_aegis_solo_scoring.py  (FALSE POSITIVE — same cause)
# lab/archive/tnec_envelope_compile_2026-08/PREREG.md           (previously missed — genuine census citation, frozen/archived, no edit)
# lab/archive/tnec_envelope_compile_2026-08/RESULTS.md          (previously missed — genuine census citation, frozen/archived, no edit)
# lab/research_utils/mechanism_prior_schema.py
# ops/instruments/M2K.md
# ops/instruments/MCL.md
# ops/instruments/MYM.md
# All but strategy_harvest.md and the 2026-07-26 ADR are frozen history/citations or the two
# self-citations — no edit owed beyond what §6 already dispositions.

# 3. Avenue A / Route B sweep (corrected raw output, re-run + pasted 2026-08-24 post-review) — 75 files
grep -rlI "Route B\|generate.\{0,3\}confirm\|2026-08-05-avenue-a\|avenue_a_generate_confirm\|Avenue A" \
  --include='*.md' --include='*.py' --include='*.json' . 2>/dev/null
# Expected hits (2026-08-24, corrected count = 75):
# docs/adr/2026-07-26-regime-candidate-flag-lane.md
# docs/adr/2026-08-05-avenue-a-generate-confirm-route.md        (action owner, §6 — full retire)
# docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md  (action owner, §6)
# docs/adr/2026-08-08-great-prune.md
# docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md
# docs/adr/2026-08-24-sourcing-phase-channel-retirement.md      (self-citation, expected)
# docs/adr/INDEX.md                                               (self-citation, expected)
# docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md      (action owner, §6)
# docs/briefs/2026-07-24-d2-letf-eod-flow-ruling.md
# docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md
# docs/briefs/2026-07-28-m2k-order-flow-avenue-a-ruling.md
# docs/briefs/GSUB-1-inventory-and-dispositions.md
# docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md
# docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md
# docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md   (action owner, §6)
# docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md
# docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md
# docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md
# docs/briefs/Q-R2VBUCK-1-volume-bucket-aggressor-route-b-scoping.md
# docs/briefs/closures/Q-CAPA-1-closure-resolved.md
# docs/briefs/closures/Q-MNQSEL-1-closure-falsified.md
# docs/briefs/closures/Q-OFCHAN-1-closure-void-coverage.md
# docs/briefs/closures/Q-R2AGRUN-1-closure-ambiguous-hold.md
# docs/briefs/closures/Q-R2FLOW-1-closure-falsified.md
# docs/briefs/closures/Q-R2VBUCK-1-closure-falsified.md
# docs/briefs/handoffs/2026-08-06-q-ofchan-1-explore-go-card.md
# docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md
# docs/briefs/pre-registration/2026-08-22-mnq-tape-imbalance-prereg.md
# docs/briefs/pre-registration/2026-08-23-mnqtape-2-larger-n-prereg.md
# docs/briefs/rnd-pipeline/Q-FVGFLOW-1-fvg-edge-book-signature-scoping.md
# docs/briefs/rnd-pipeline/Q-ICTNF-1-nearfield-ssl-bear-fvg-scoping.md
# docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md
# docs/briefs/rnd-pipeline/closures/Q-FVGFLOW-1-closure-ambiguous.md
# docs/ltm/adr/2026-08-10-implied-sr-plausibility-gate.md        (cold-stored, frozen)
# docs/methodology/README.md
# docs/methodology/avenue_a_generate_confirm.md                  (action owner, §6 — mark Withdrawn)
# docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md
# docs/notes/notice/N-2026-08-20-anthropic-training-principles-pipeline-mapping.md
# docs/pursuits/c5-q-mschan-1.md                                  (action owner, §6)
# docs/rejected_candidates.md
# docs/spec/2026-08-05-eval-mechanism-shape-screen.md
# docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md
# docs/spec/2026-08-06-mnqprox-2-tod-matched-level-proximity-spec.md
# docs/spec/2026-08-07-loop-s6-k-aware-generation-spec.md
# docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md
# docs/spec/2026-08-22-grow-lane-generate-refine-spec.md
# lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md
# lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md
# lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md
# lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG.md
# lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md
# lab/analysis/c1/mnq_r2agrun_routeb_2026-08/PREREG_G0.md
# lab/analysis/c1/mnq_r2agrun_routeb_2026-08/RESULTS_g2.md
# lab/analysis/c1/mnq_r2agrun_routeb_2026-08/agrun_lib.py
# lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/PREREG.md
# lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md
# lab/analysis/c1/research-analyst-mnq-atomic-facts-2026-08-19/DRAFT_INSTRUMENT_PROFILE.md
# lab/archive/mnq_capa_n14_tripwire_2026-08-06/PHASE0.md
# lab/archive/mnq_capa_n14_tripwire_2026-08-06/PREREG.md
# lab/archive/mnq_capflow_orb_r_2026-08/PREREG.md
# lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md
# lab/archive/mnq_orb_level_proximity_2026-08-05/RESULTS.md
# lab/archive/mnq_orderflow_probe_2026-08-04/RESULTS.md
# lab/archive/mnq_r2flow_routeb_2026-08/PREREG_G0.md
# lab/archive/mnq_r2flow_routeb_2026-08/RESULTS_g2.md
# lab/archive/mnq_r2flow_routeb_2026-08/flow_lib.py
# lab/archive/mnq_r2vbuck_routeb_2026-08/PREREG_G0.md
# lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md
# lab/archive/mnq_selection_ceiling_2026-08/PREREG.md
# lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md
# lab/archive/tnec_envelope_compile_2026-08/run_envelope_compile.py
# lab/discovery/grammar.py                                       (reviewed §5 — generic G0-discipline citation, not a Route B liveness claim, no edit)
# ops/instruments/MECHANISMS.md
# ops/instruments/MNQ.md
# tests/scripts/test_check_closure_disposition.py
# Note: this list also implicitly includes docs/pursuits/a3-mnq-discovery-pipeline.md's own
# generate→confirm/Route-B references, which the original sweep's pattern set does not directly
# match on filename/title alone but which §6 separately names as an action owner (its title text
# literally contains "Route A/B") — confirm this file also appears in a live re-run before Phase 1
# executes; if it is absent, add it to the disposition list rather than skip it.
# All hits above the two self-citations, the 4 action owners marked, and the a3 note are frozen
# campaign/session history, ledger citations, or cold-stored records — no edit owed.

# 4. §4 limb 1 (factual) re-check — run at any time a contradicting seed is suspected
grep -rn "admitted\|ADMIT\b" docs/notes/notice/N-2026-07-26-forced-flow-census.md \
  lab/analysis/c1/mnq_ofchan_routeb_2026-08/ lab/archive/mnq_r2flow_routeb_2026-08/ \
  lab/archive/mnq_r2vbuck_routeb_2026-08/ lab/analysis/c1/mnq_r2agrun_routeb_2026-08/ 2>/dev/null
# Expected: no hit asserting a seed from either channel was ever admitted (the census file itself
# is git-show-only post-prune; retrieve via `git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`)

# 5. §4 limb 3 (early-closure legitimacy) — calendar reminder, not yet due
# Re-examination due: 2027-02-08 (clause 2-B's own literal "second quarterly audit" trigger date)
# Command to run at that date: re-read this ADR's §0/§1 evidence against whatever record exists by
# 2027-02-08 and confirm no material campaign/finding was missed at 2026-08-24 authoring time.

# 6. Reverse-edge check (fires only once this ADR is Accepted)
grep -n "Superseded-by\|Superseded-in-part-by" \
  docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md \
  docs/adr/2026-08-05-avenue-a-generate-confirm-route.md \
  docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md
# Expected while Proposed: the 2026-08-08 ADR shows its pre-existing L2 entry
# (Superseded-in-part-by: 2026-08-12-msl-sourcing-channel-ratification.md) and nothing else on any
# of the three; this ADR is not yet referenced. Expected post-Accept: all three additionally point
# here (the 2026-08-08 ADR carries TWO Superseded-in-part-by lines — L2's existing one, unedited,
# plus this ADR's new L1 one).

# 7. Full retire shape check (post-Accept only)
test -f docs/ltm/adr/2026-08-05-avenue-a-generate-confirm-route.md && \
  wc -l docs/adr/2026-08-05-avenue-a-generate-confirm-route.md
# Expected post-Accept: LTM body exists; hot stub ≤40 lines.

# 8. Graph integrity
python scripts/check_adr_graph.py
# Expected: exit 0 (edges skipped while Proposed; mandatory once Accepted)
```

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-08-24-sourcing-phase-channel-retirement.md --type adr
# Expected: RESULT: well-formed

# ADR lifecycle graph
python scripts/check_adr_graph.py
# Expected: exit 0 (A2 edge-reverse-match skipped while Proposed)

# §0 anchors
git log -1 --format='%h %cs' -- docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md   # aef55a9 2026-08-23
git log -1 --format='%h %cs' -- docs/adr/2026-08-05-avenue-a-generate-confirm-route.md                # 1a07c35 2026-08-21
git log -1 --format='%h %cs' -- docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md  # 1a07c35 2026-08-21
git log -1 --format='%h %cs' -- docs/methodology/strategy_harvest.md                                   # ac05de6 2026-08-24

# Supersede chain integrity (post-Accept)
grep -A1 "Supersedes" docs/adr/2026-08-24-sourcing-phase-channel-retirement.md
grep -A1 "Superseded-by\|Superseded-in-part-by" docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md docs/adr/2026-08-05-avenue-a-generate-confirm-route.md docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Initial authoring, `Proposed`. Companion to the same-session sourcing-phase usage audit (four-branch fan-out over `lab/CATALOG.md`, `docs/rejected_candidates.md`, `docs/briefs/INDEX.md`, and the governing ADRs) run against an operator-provided external pipeline mapping. Operator elected full Route B retirement over formalizing the existing single-family pause. | Joshua (direction) + Claude Code (draft) |
| 2026-08-24 | Adversarial pre-ratification review (`pre-ratification-adversarial-panel`, 50 agents: 6 lenses + skeptic verification + synthesis) returned **BLOCKED** — 3 confirmed BLOCKERs, 6 confirmed CONCERNs, 0 disputed. All 9 fixed in place, still `Proposed` (no material change to the underlying two-clause decision): (1) §0's "clean baseline" claim corrected — the 2026-08-08 ADR already carries an unrelated `Superseded-in-part-by` entry (L2), §6/§7 corrected to append rather than overwrite; (2) §0/§10 grep-sweep counts corrected 26→35 / 70→75 and actual raw filenames pasted (previously only prose); (3) §4 gained a third falsifier limb testing early-closure legitimacy against clause 2-B's real 2027-02-08 trigger date, with a matching `STATE.md` forward-trigger row owed in §6/§7; (4) §3's date math corrected (2026-11-08 is the *first* scheduled audit, not the second — the real trigger is 2027-02-08, ~5.5 months out); (5) `a3-mnq-discovery-pipeline.md` given its own numbered Phase-1 fix instead of a parenthetical on the `c5` item; (6) the inherited "~0.95pt round-trip cost" figure (actually MFFU/BluSky's per-side dollar commission, not a Tradeify point figure) corrected to the verified ~1.41pt Tradeify figure, flagged as an uncorrected error in the source 2026-08-08 ADR rather than silently fixed there. Per template convention these are pre-Accept corrections to a `Proposed` draft, not a material amendment to an already-ratified decision — no supersession needed. | Claude Code (review response) |
