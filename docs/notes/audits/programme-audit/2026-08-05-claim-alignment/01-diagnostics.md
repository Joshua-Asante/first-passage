# §3 — The seven diagnostic questions

**Section covers:** the Programme Audit Protocol's seven diagnostics, answered **separately for the object layer** (the prop-portfolio / venue / deployment claim estate) and **the meta layer** (the correction machinery and gate estate) — **14 layer-separated answers**, carrying **16 table rows** across four tables (object belt 4 · meta belt 3 · threshold changes 3 · gates that stopped binding 6).

**Evidential standing.** The body of this section is round 1's §3, ported essentially intact at repo anchor `e031225`; its evidence anchors were re-verified and hold. Round-2 evidence is integrated at four points and marked **`[R2]`** inline — round-2 findings carry slightly lower evidential standing than round-1's, stated once and only once in [`README.md`](README.md). Four findings that this section reports as *found* have since been **FIXED or RULED**; each carries a `✅` disposition line naming the commit. The diagnostic answers are stated **as of the audit anchor**, because that is what the diagnosis is about; the fixes are downstream of the diagnosis and do not retro-edit it.

**Pointer:** section index, combined counts and the round-1-vs-round-2 standing note live in [`README.md`](README.md).

---

## §3.0 — Two-layer discipline (load-bearing, not ceremonial)

Every question below is answered twice, once per layer, and **no answer cites the other layer's evidence**. Cross-layer citation is degeneration signal #6 in its own right, so the discipline is not a formatting convention — violating it would corrupt the instrument. It was enforced by construction in both rounds.

**No meta-layer answer below cites deployment state, venue facts, cap allocation, book σ, bust rates, or P&L.** **No object-layer answer cites gate-script behaviour or rule-text completeness.** Four labelling decisions sit at the seam and are stated so a reader can check them rather than infer them:

1. `state-rider-enumeration-command-undercounts` is filed **object** — `STATE.md`'s forward board is the object programme's own obligation register, not part of the `scripts/` gate estate.
2. `.claude/skills/**`, `.claude/commands/**` and `.cursor/**` are agent-instruction surfaces carrying object-layer *content*. They are cited **only** as evidence about gate coverage (**meta**), never as evidence about deployment state. `[R2]`'s 23 `.claude` findings and 4 `.cursor` findings enter §3.2 and §3.6 on that footing alone; their object-layer content is adjudicated in the findings sections, not here.
3. The `PYTHONPATH` defect in the documented `ops/sentinel` invocation was **discovered while fixing an object finding** (B2) but is filed **meta** — it is a property of the gate estate, and it is cited only in meta answers.
4. ADR `2026-08-05-strategy-venue-binding-axis.md` (`Proposed`, commit `0af62ec`) is filed **object** — it ratifies the organization of strategy facts, which is object-layer subject matter. It is cited in no meta answer, and it is **`Proposed`, not in force**; nothing below treats it as binding.

---

## §3.1 Hard-core integrity

**OBJECT LAYER — hard core preserved; the violation is representational, not substantive.**

The object-layer hard core is: *locked parameters are immutable; authorization is a separate revocable axis; deployment scope is an operator decision.* All three held. ADR [`2026-08-04-tradeify-venue-descope-eval-included.md`](../../../../adr/2026-08-04-tradeify-venue-descope-eval-included.md) §2 changed no Pine, no `BASE_RISK`, no `dd_protection` constant, no `LEG_MAP` entry, and explicitly declined to move lifecycle — recording its reasoning ("venue-fit is not decay") rather than exercising the axis silently. Verified at HEAD: `core/lifecycle_state.json` **does not exist**, so both Striker keys default to `AUTHORIZED` at 1.00×, exactly as the ADR states.

What the audit found instead is a cluster of **artifacts asserting a configuration the hard core no longer instantiates**. Three rose to BLOCKER. All three are now fixed; the findings are preserved because the diagnosis rests on them.

- **`docs/adr/2026-07-17-c1-rail-build-account-registration-go.md`** — at the anchor: Status `Accepted`, `Superseded-by: none`, addenda stopping 2026-07-28, and a grep for `2026-08-04|de-scope|descope` returning **0**. §2 still read: *"Commission the c1 execution rail … and register **one `Tradeify_Select_100K` evaluation account** … to run the c1 2-leg book … at **WATCH-1 0.50×**."* The 08-04 ADR named this file as *"the GO this reverses in its deployment limb"* but filed it under `Related`, so no reciprocal edge existed and `check_adr_graph.py` could not enforce one. In a repo whose charter states "ADRs are canonical for every decision", an `Accepted` GO whose deployment limb is reversed, carrying no reader-intercept of any kind, is a governance-level gap — and `docs/notes/rail_build/RUNBOOK.md` L3 names it as "Authority".
  **✅ FIXED — `ae5ffe7`.** Reciprocal supersession edges between the GO ADR and the de-scope ADR, a dated Addendum 2026-08-04 on the GO ADR, and the `RUNBOOK.md` Authority intercept. `check_adr_graph` passes. The GO ADR went from **0 → 7** mentions of the de-scope. §2, §4, §5 and all five prior addenda are byte-intact.

- **`STATE.md`'s published 08-08 rider-enumeration command.** The board said *"Enumerate the riders mechanically at audit time — do not maintain a list here"* and supplied a single-line, single-spelling `rg` one-liner. Live-obligation files were individually verified as dropped: a wrapped field (`2026-07-22-c1-venue-native-monitoring-maturity.md`), two using the alternate `**Check schedule:**` spelling (`2026-07-13-prop-account-book-segregation.md`, `2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`), `2026-08-03-params-toml-gate-retirement.md`, and **the entire hard-core P-gate family**, which states its 08-08 duty in prose under `## §6 — Gate + review` with no bolded field at all. Running the 08-08 audit from the published command silently drops them, three days out.
  **✅ FIXED — `a818b3f`.** The under-reaching command is retired. Measured while fixing, at that commit: the published one-liner returns **33**; the sentinel returns **36**; **53** ADRs mention the date; the residue of **17** carries its duty in **prose with no trigger field**, of which **~10 are live obligations** and **FIVE are hard-core P-gates (P1–P5)**. **Round 1 said four — that was an undercount, corrected here rather than quietly re-stated.** `docs/adr/2026-07-03-hardcore-p5-source-truth-rail-gate.md` exists and carries the same prose-only shape as P1–P4. These three counts are *not constants*; they move with every ADR added, which is precisely why the board's own rule is **enumerate, never cite from memory** — the rule was right and its instrument was wrong.

- **`docs/spec/c1_watch_realization_multiplier_layer.md` §2** — *not de-scope-caused, and older*, but the sharpest safety-relevant divergence found in either round. An `Accepted` normative sizing law that `docs/spec/c1_nt8_sizing_host_impl.md` L6/L16 declares is "the sizing law this spec implements verbatim (not re-derived)" stated `qty_base = min(qty_base, floor(cap_firm / (1 + pyr_pct/100)))`, while production (`ops/c1_rail/c1_sizing_host_reference.py:296`) uses `cap_alloc` per leg behind a HALT guard and carries the header comment recording exactly what the `cap_firm` form produced: **"the 2-leg book could compute MYM 76 + MNQ 77 = 153 micros against an 80 limit (1.91x)"**. The 2026-08-02 cap-split staleness sweep classified this file as a live defect and opened only its §10 audit hook — re-pinned to (8, 60) — leaving §2's worked check still asserting (9, 67) and "Matches `f2_floors.json` exactly". The spec contradicted its own hook. An F3 implementer following the declared chain reproduces a measured account-limit breach.
  **✅ FIXED — `d84c5e4`.** `cap_firm → cap_alloc[leg]` in **both** `docs/spec/c1_watch_realization_multiplier_layer.md` §2 and `docs/spec/c1_nt8_sizing_host_impl.md` §2.2, plus the normative HALT property, the constants gloss, and the worked check (9/67 → 8/60, pre-split pair retained for provenance). **Production was already correct and was not touched; no encoded value changed; the 69/11 split is unchanged.**

**Where the fix leaves the diagnosis.** All three BLOCKERs were *representational*: three artifacts asserting a configuration, not three breaches of the hard core. Fixing them does not change the §4.1 verdict, because the verdict turns on the **class** — a ruled decision that did not reach its reading sites — and the class is 250 confirmed findings wide, not three.

**Structural note (object, `Proposed`).** ADR `docs/adr/2026-08-05-strategy-venue-binding-axis.md` (`0af62ec`) proposes a third orthogonal axis, **BOOK → VENUE EDITION → DEPLOYMENT**, alongside the parameter (`LOCKED`) and authorization axes, both of which are venue-agnostic. It bears on this question because B3's defect shape — *an account-aggregate venue fact living inside a book-layer normative spec* — is invisible under a two-axis model and becomes a **visible layer error** under a three-axis one. Recorded as the structural answer to the failure class; **it is `Proposed` and nothing here treats it as in force.**

**META LAYER — hard core preserved in rule text; violated in gate implementation.**

The meta-layer hard core is: *corrections land where the error is read; frozen bodies are never edited in place; every mechanical gate binds over the surface it declares.* The first two hold and are demonstrably exercised (dated addenda, `⚠ SUPERSEDED` banners preserving "Original text follows", reader-intercept blocks). The third is violated, mechanically and measurably:

- `scripts/check_supersession_placement.py:96` globs `lab.glob("*/RESULTS*.md")` — one level — while its own SCOPE docstring declares `lab/analysis/*/RESULTS*.md` as a class. Executed at HEAD: **flat glob = 5 files; `find` over the tree = 73.** The gate opens 5 of 73 (**6.8%**) and prints `check_supersession_placement: OK — every withdrawing addendum has an upstream reader-intercept` on every commit. Git dates the cause precisely: the gate landed `c271411` 2026-08-03 12:49; the lab theme-nest landed `92abdbb` 2026-08-03 22:14 — **nine and a half hours of bindingness**, unnoticed for two days.
- `scripts/check_adr_graph.py:31-32` — `FIELD_RE` recognises six header fields and silently `continue`s on anything else. The corpus has invented `**Withdraws:**` (08-04 ADR L9) and `**Withdrawn-by:**` (08-02 ADR L7); the graph drops both, so the derived `docs/adr/INDEX.md` renders the withdrawal pair with successor `none` at both ends. The gate exits 0. `check_a2` compounds it: it iterates only `y.supersedes`, so the reverse direction — the one a reader traverses when asking "is this still current?" — is never validated. Measured: 2 live unreciprocated reverse edges across 107 dated ADRs.
- `scripts/retire_adr.py:211-212` — the `set_header_field(updated, "Superseded-by", …)` write is guarded by `if by_filename:` alone, unconditional on reason, while `_validate_supersede_precondition` runs only under `reason == "superseded"`. So `--reason withdrawn --by X` skips all edge validation and still writes a false supersession edge. `docs/adr/2026-08-02-striker-tradeify-funded-phase-descope.md` L6 records in past tense that the tool did exactly this and that it was hand-corrected. `tests/test_retire_adr.py:146` exercises `--reason withdrawn` **without** `--by`, so the failing invocation is untested. **Still unrepaired.**
- `scripts/check_skills_no_constants.py` — `GUARDED_SKILLS` covers the four *methodology* skills, which carry almost no operational constants, and exempts every ops skill that does. It cannot see `.claude/hookify.*`, `.claude/commands/*`, or `.cursor/**` at all. `[R2]` sharpens the denominator: `.claude/skills/` holds **18** skills and `.claude/commands/` **3** command files; the guard reads four of twenty-one.
- `[R2]` **The documented invocation of the sentinel scanner does not run.** `python -m ops.sentinel.scan`, as published, raises `ModuleNotFoundError: No module named 'sentinel'`; the canonical form is `PYTHONPATH=ops python -m sentinel`. Discovered while fixing an object finding (see §3.0 labelling decision 3) and filed here because it is a gate-estate property: a scanner whose *published* invocation throws is a gate that binds only for a reader who already knows the undocumented form.

## §3.2 Belt churn — explicit tallies

**No pre-existing artifact enumerates either belt. Both tables are this audit's own construction.**

**OBJECT LAYER belt (claim estate), 2026-07-12 → 2026-08-05:**

| Category | Count | Instances |
|---|---:|---|
| **ADD** | **18** | S4 product-group bar · S5 cap allocation · S7 symbol occupancy (07-29 ADR) · R1 σ ceiling · T3 family DSR floors · L1 liveness limb (08-02 ADR) · idle-rule disposition options · idle-clock tracking spec · WATCH-1H rung (`Proposed`) · Phase-4 rerun spec · EV rung-selection objective · segregation §4 revert check · book-comp D1 gate · prop_envelope E1–E7 · M1 monitoring spine · M1 4-session review trigger · disaster-stop proposal · cadence pre-registration |
| **REVISE** | **6** | cap 80 → 69/11 · ORB unpark → re-park · F1(b) ruled then reversed · `dd_lock_offset_usd` applied · BluSky idle 30 → 22 · envelope verified-dates |
| **REMOVE (decided)** | **7** | K-bank gate → disclosure · two legs withdrawn · four queue rows mooted · 08-02 ADR withdrawn · F1(b) reversed · quarterly C2→C0 retired · params.toml gate retired |
| **REMOVE (propagated to reading sites)** | **1** | the 08-04 §6 six-site sweep (`CLAUDE.md`, `STATE.md`, `ops/instruments/{MYM,MNQ}.md`, `docs/adr/INDEX.md`, `docs/SESSIONS.md`) |

**Add : effectively-propagated-remove ≈ 18 : 1.** The decisive number is not the add count — it is that **seven removals were decided and one was propagated**. Round 1 measured 120 object-layer findings still asserting the removed configuration; the combined two-round total is larger still. The belt did not fail to prune; **the prune was ruled and did not reach the reading sites.**

**The trend limb cannot be run on this layer, and is not being asserted.** No prior audit enumerated the *claim estate's* belt. The table above is this audit's own first construction, so the protocol's "net-positive across ≥3 consecutive audits" test **has no prior points to fit** on the object layer. Stated rather than papered over — and it is the reason §4.1 declines the Degenerating verdict's second limb rather than clearing it.

**META LAYER belt (correction machinery + gate estate), same window:**

| Category | Count | Instances |
|---|---:|---|
| **ADD** | **12** | Rule 11 (back-propagate) · Rule 14 (supersession placement) · pre-commit gate 13 · pre-commit gate 14 · `check_falsifier_reachability` · `check_root_doc_liveness` · `check_status_consistency` · `check_adr_graph` A1–A7 · `check_skills_no_constants` · `retire_adr` · `ops/sentinel` scanners · the ADR §10 runnable-hook convention |
| **REVISE** | **3** | M1 trigger send → arm (07-31b) · K-bank rule (08-04) · 90-day venue-fact clock made per-firm |
| **REMOVE** | **3** | `validate_params.py` + `params.toml` (08-03) · quarterly regime check (07-22) · `lab/codification` bridge (08-02) |

**Net +9, add : remove = 4 : 1.** Better than the 2026-08-03 gate-stack audit's 8 : 1, but still net-positive — and **2 of the 3 removals left dead pointers in live guidance.** Verified at HEAD: `scripts/validate_params.py` does not exist and `core/config/` does not exist, yet `README.md`, `PIPELINES.md` (×2), `core/dd_geometry.py`, `ops/instruments/NAS100.md` and `docs/operational_rules.md`'s Rule 7 owner table all still cite them; `REPO_MAP.md` §2.2 still lists a runnable `codification.emit` invocation for a deleted module. So the meta layer reproduces, on itself, the object layer's exact failure shape — **removals executed in code, not propagated to the inventories** — and this is the **second consecutive meta-layer audit** to find net-positive belt with near-zero effective prune.

**`[R2]` — the trend limb the meta layer *does* have, and it worsens the reading.** Round 2 swept the `scripts/` estate and the agent-instruction surfaces, neither of which round 1's tally reached. Two measurements:

- **22 scripts are unwired or mis-scoped** — against a denominator of **37** files in `scripts/*.py`, that is **59% of the script estate that either nothing runs or that runs over the wrong surface.** The belt table above counts *additions of machinery*; this counts *machinery that does not bind*. The two together say the ratio is not 4 : 1 in effect — most of what was added is not doing the work the tally credits it with.
- **The agent-instruction surface was never swept at all** — 18 skills, 3 command files, `.cursor/**`, and `hookify` rules, none of them reachable by `check_skills_no_constants`'s four-skill guard (§3.1). Round 1's own completeness critic independently flagged `.claude` as its **largest coverage hole** before round 2 ran; round 2 then returned **23 agent-facing findings** there.

This is belt-trend evidence of exactly the kind the object layer lacks, and it points one way: **the meta belt grew, and the growth was not verified.** It is the primary evidence under §4.2, and it is cited nowhere in an object-layer answer.

## §3.3 Progressive evidence

**OBJECT LAYER — yes, and it is the strongest evidence in the audit.**

The de-scope itself is a predicted-and-corroborated result running *against* the programme's interest. Three funded-phase misfits were measured before the ruling (1.01 qualifying winning days/mo · 104.7% of net from >40-micro days · $299.80/acct-mo chain at 49.06% 1-yr mortality); an eval-phase limb was then added on the same evidentiary footing (`inactivity_max_idle_days: 5` priced at **92.6–97.6% path death**, mitigation undelivered); and the venue was abandoned at recorded cost — *"$208/$700 sunk, first live fill never occurs and strands five threads"* — rather than patched to preserve the conclusion. The lifecycle axis was explicitly **not** moved, and §5 forbids citing the ADR to pre-empt the 2026-11-08 §4 falsifier. That is a programme paying to abandon a position rather than rescuing it.

Corroborating: `ORB-MNQ-1`'s payability target was ruled **FALSIFIED** 2026-08-03 (intraday-honest bust ≥ 67.67% against a 3.0% ceiling) with lifecycle not demoted, K not spent and mechanism not rejected — falsification correctly scoped to one target at one firm. Two adverse rulings in two days, both against interest.

**A third instance, and it is structural rather than empirical.** ADR `docs/adr/2026-08-05-strategy-venue-binding-axis.md` (`Proposed`, `0af62ec`) responds to *the failure class this audit found*, not to any single finding: it gives venue facts an owning level (**BOOK → VENUE EDITION → DEPLOYMENT**), so a venue fact sitting inside a book-layer artifact becomes a layer error a reader can see. That is the correct progressive shape — a diagnosed failure mode converted into structure. Two qualifications, both material: it is **`Proposed` and not in force**, so it is corroborating evidence about the programme's response, not about its state; and a new axis is itself belt, which the §3.2 tally does not yet carry and which the next audit must price rather than assume.

**META LAYER — present but thin, and one instance is contaminated.**

Rule 11 fired: the de-scope ran a §6 downstream sweep under it and **all six enumerated sites landed correctly** — verified. Gate 14 and Rule 14 exist because two 2026-08-02 supersession incidents that manual review barely caught were converted into a mechanical check. That is the correct progressive shape: an incident becoming a gate.

Against that, the one certification the machinery produced about itself is over-claimed. ADR 2026-08-04's Status asserts *"§6 downstream sweep **COMPLETE** 2026-08-04"*, and §7 Phase 2's stated aim is a *"grep-sweep for text reading Tradeify (either phase) as a live target"* — but §10 hook 3 implements it over **four files**, every one a strict subset of the §6 list the author had already edited. As a discovery instrument it structurally cannot surface an untouched file. **This audit tested the obvious remedy and it fails:** hook 3's exact six-key pattern run against `docs/spec/2026-07-27-third-leg-target-spec.md` — the estate's most consequential stale artifact — returns **0 hits**. Widening the file list changes nothing, because the sweep is keyed on the *decision's* vocabulary and derived documents share no token with it. The sentence itself is literally accurate about its six sites, which is why this is reported at MISLEADING, not BLOCKER.

## §3.4 Degeneration evidence — was anything patched to rescue a conclusion?

**OBJECT LAYER — no.** No threshold moved to rescue a conclusion in the window. The one rule change that loosened an admission gate (`K_eff = K_intrinsic + K_banked` → `K_eff = K_intrinsic`, ADR 2026-08-04) went through a ratified ADR with a stated rationale, was executed the same session at the enforcement surface (`lab/research_utils/axis_screen.py`), and was propagated to `ops/instruments/MNQ.md` N10 with a full "what survives / what does not" disclosure. It is a belt revision with corroboration, not a rescue.

The residual degeneration-shaped risk is different in kind: **stale figures from the superseded rule still circulate as current.** `docs/spec/2026-07-27-third-leg-target-spec.md`'s T3 row still reads *"MNQ **0.98 (at the cap — one K_intrinsic=1 seed only)** · MYM 0.85 · 6E 0.85 · GC/MGC **2.05, permanently dead**"* — every value derived from the retired ladder, inside a RATIFIED spec consumed as current screening guidance, and stating a false *permanent instrument foreclosure* on the family the amending ADR calls "the largest single unlock". `CLAUDE.md` still quotes `K_banked(MNQ)=2` with "one Cap seat left" while the ledger records three spends since (2→3, 3→4, 4→5) and the seat arithmetic itself was retired. The mandatory-disclosure quantity is wrong in the always-loaded charter.

One further instance is **not de-scope-caused and is the most serious of the class**: `lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md` still publishes `z = −2.90` with the interpretive sentences *"the final block is anomalous rather than merely long"* and *"That is a phenomenon, not an artifact"*, while the later `docs/rejected_candidates.md` entry (2026-08-02) states the estimate treated 11 differenced points as independent, that the direct per-day test returns `t = −1.78`, that max |t| across all 11 session blocks is 1.84 against an expected null max of ≈2.2–2.4, and that **"z = −2.90 must not be re-quoted"**. The RESULTS carries no intercept and `lab/CATALOG.md` lists the study a bare `ACTIVE`.

**META LAYER — one instance, and it is a certification, not a threshold.** The "sweep COMPLETE" claim in §3.3 is the only artifact in the window written to support a conclusion its own instrument cannot test. **No gate threshold was softened anywhere.**

## §3.5 Boundary respected — were forbidden moves made?

**OBJECT LAYER — yes, respected. One boundary was crossed deliberately, with reasoning recorded; under this protocol that is the system working.**

The negative heuristics held: no locked parameter edited, no lifecycle write, no allocation change, no frozen body edited in place, no §4 falsifier pre-empted. The rail remains disarmed and the arm path is hard-gated in code (`m1_acceptance_reason`).

**The recorded crossing — FU-1, `551d5c5`.** Round 1 surfaced a time-asymmetry the de-scope ruling had not priced (see §3.6): the eval sits on the venue's weekly activity clock, and the first uncovered Mon–Fri window closes **2026-08-07 — one day before fork F2 is due**, so the "leave dormant" branch could lapse before it could be chosen. The operator ruled, in session: *"We will not let the venue lapse. If no strategy has been found by Friday we will submit a token trade."* The primary path is a deployed strategy covering the week with its own fill; the **fallback is ONE operator-submitted manual token trade by 2026-08-07**, and it crosses the book-composition brief's §5 forbidden-move item — the third option that brief expressly excluded.

**Why this is not erosion.** The crossing is (a) **named as a crossing** — the commit records it as a deliberate override of a stated forbidden move, citing degeneration signal #7 by number; (b) **reasoned** — it buys the ability to *rule* F2 rather than have F2 foreclosed by deletion; (c) **bounded** — exactly one trade, operator-submitted, by a stated date, with **the rail not moving and no agent permitted to place it**; and (d) **recorded at the reading sites** — `STATE.md` and `docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md`, the two places a reader meets the constraint. A negative heuristic that can never be crossed is not a heuristic, it is a wall; the protocol's concern is *silent* crossing. This one is the audited-and-approved shape.

**What would make it erosion — pre-registered here so the next audit can test it, not argued after the fact:**

1. **A second token trade** fired on the same reasoning without a fresh, separately recorded ruling — i.e. the one-off becoming a standing practice by precedent.
2. **Any crossing of this or an adjacent forbidden move that is not recorded** at the site where the constraint is read, on the date it happens.
3. **An agent placing the trade**, or the rail being armed to place it — the ruling's bound is that this is operator-manual; automating it converts a bounded override into a channel.
4. **The reasoning being reused for a different constraint** without re-derivation — citing FU-1 as authority rather than re-arguing the case.

Any one of the four is a §3.5 failure at the next audit and should be reported as such.

**Two live exposures remain adjacent to the boundary rather than across it.** `docs/notes/rail_build/RUNBOOK.md` §B8 still reads *"Run it whenever attended time is available; do not block it on M1/item-5 closing"* for a test the same section describes as *"real money moving on a real account"* — on an account whose disposition is open fork F2, for a Phase-1 successor that wires `sl=` for the two withdrawn legs and therefore falls under the ADR's narrowed §2 clause 3. And `docs/notes/rail_build/B7_STAGE1_DESK_CARD_2026-08-04.md` — named by date in the ADR's own §0 and §6 as mooted — is the newest card in its directory, opens with a live goal statement, carries an empty §2b capture table and "Today is session 1 of 4", and has no SPENT/MOOT marker anywhere in 391 lines, while its 07-31 sibling carries exactly that marker in its H1. **Neither is discharged by FU-1**, and the distinction matters: FU-1 authorizes one operator-manual trade, not a B8 dry-fire and not a desk-card session.

**META LAYER — one boundary crossed and unrepaired.** `scripts/retire_adr.py` emits a false `Superseded-by` edge on `--reason withdrawn` (§3.1). The 2026-08-02 stub records in past tense that the tool did this and that it was hand-corrected; the tool was not fixed, the failing invocation is untested, and no repair item exists anywhere. A known-defective governance tool that caused a recorded incident, tolerated rather than removed, three days on — this is trigger #7 shape.

**The two layers' crossings are opposite in kind, and the contrast is the point.** The object crossing is named, reasoned, bounded and recorded. The meta crossing is undocumented as a live defect, unbounded (any `--reason withdrawn --by X` invocation reproduces it), and has no owner. Same protocol, same window, two different dispositions — which is why §4.1 and §4.2 diverge.

## §3.6 Theory comparison — did the chosen design outperform?

**OBJECT LAYER.** Two counterfactuals are priced.

1. **De-scope now vs "hold the eval to 2026-11-08" (the reversed F1(b) ruling).** The hold branch is directly costed by the estate's own measurement: `inactivity_max_idle_days: 5` at 92.6–97.6% path death with the mitigation undelivered, plus $299.80/acct-mo chain against 1.01 qualifying winning days/mo. Holding buys a 2.4–7.4% survival path at recurring cost. The chosen branch wins on the recorded numbers.
   **The comparison's open limb has since closed.** Round 1 reported this comparison as *not closed*, because it had surfaced a time-asymmetry the ruling did not price: the eval is still on the venue's weekly activity clock, the last covered week was 2026-07-27→31, and the first uncovered Mon–Fri window closes **2026-08-07 — one day before fork F2 is due**; enforcement is warning-first and no warning had arrived as of 2026-08-02, so foreclosure was *possible*, not scheduled — but the "leave dormant" branch might lapse before it could be chosen. **The operator ruled that limb 2026-08-05 (`551d5c5`, §3.5):** the venue will not be allowed to lapse; primary path a deployed strategy, fallback one operator-submitted token trade by 08-07. The counterfactual is therefore now decided on cost grounds alone, with the calendar hazard removed rather than absorbed — **and the fact that the audit surfaced an unpriced limb which was then ruled within a day is itself the comparison working.**
2. **Lifecycle unmoved vs demote-to-WATCH.** The chosen branch is corroborated by consequence: because no lifecycle write occurred, a de-risk decision was not smuggled into a venue decision, and both legs remain re-deployable at full authorization if F3 elects a successor. The counterfactual would have conflated two orthogonal axes the programme spent an ADR separating — and the `Proposed` third axis (§3.3) is a bid to make that separation structural rather than remembered.

**META LAYER.** The relevant comparison is *mechanical gate vs doc discipline* for the staleness class. Doc discipline is the declared owner (Rule 6 skew audit + Rule 7 canonical-owner discipline), and this audit is direct evidence about its performance: it caught nothing in 24 hours across 120 round-1 object-layer findings. But the mechanical alternative loses on its own terms too — gate 13 opens 6.8% of its declared corpus; `check_root_doc_liveness` resolves markdown links only, so dead paths inside backtick spans pass green; `check_skills_no_constants` guards the four skills with the fewest constants; and `check_adr_graph --enable A7` returns **4 findings at HEAD** but is excluded from `DEFAULT_ENABLED_CHECKS`, so nothing runs it by default. **Neither theory is winning; the class is uncovered.**

**`[R2]` — a third contender was measured and it loses hardest.** Round 2's most consequential structural fact is that **71 of its 110 confirmed findings are agent-facing** — consumed by an AI agent or an operator *mid-task*, where a stale instruction causes an **action** rather than merely misleading a reader. They concentrate in `.claude` (23), `docs` (19), `scripts` (16), `deploy` (8) and `.cursor` (4). This changes the comparison in two ways:

- **The failure mode is worse than the one both theories were designed for.** Doc discipline and gate 13 both target *a reader forming a false belief*. An agent-facing stale instruction skips the belief step. Neither owner was scoped for it.
- **Neither theory covers the surface at all.** `check_skills_no_constants` reads 4 of 21 `.claude` instruction files; nothing reads `.cursor/**`, `.claude/commands/**`, `hookify` rules, or `deploy/`; Rule 7's canonical-owner table does not name any of them. The 71 findings sit in a region with **no owner of either kind** — which is a stronger statement than "neither theory is winning": on the highest-consequence third of the estate, **neither theory is even applied.**

That is the meta layer's most consequential finding, and it is unchanged in direction by round 2 — only in magnitude.

## §3.7 Falsifier check — executed, with the diff reported

**Pre-committed thresholds, verified at `e031225`:**

```
core/dd_protection.py   DD_TRIGGER = 0.015                    ✓ unchanged (C2 relock 2026-05-08)
core/dd_protection.py   DD_SCALE   = 0.40                     ✓ unchanged
core/dd_protection.py   MVD spec-pin  :292 / :297             ✓ present and passing
core/lifecycle.py       1.00 / 0.50 / 0.25 / 0.00             ✓ unchanged (ratified Call-2 table)
prereg                  headline bust ≤ 3.0%                  ✓ present at HEAD
prereg                  P(pass) ≥ 50%                         ✓ present at HEAD
prereg                  Part B bust ≤ 1.0%                    ✓ present at HEAD
```

**Zero numeric drift** on every locked risk constant and on the G1 Part A/B pair. (Note: `docs/methodology/strategy_lifecycle.md` and the 2026-07-10 lifecycle ADR both cite the MVD pin as `dd_protection.py:176/181`; those lines now hold an unrelated `_validate_state` multiplier guard. The **pin passes**; only the citation is stale — a finding, not drift.)

**Three threshold-affecting changes in the window, all ADR-borne, reported with direction:**

| Change | Direction | Instrument |
|---|---|---|
| `K_eff = K_intrinsic + K_banked(family)` → `K_eff = K_intrinsic`; MNQ floor 0.980 → **0.650** | **LOOSENS** an admission gate | ADR 2026-08-04 `family-k-bank-disclosure-not-gate`, `Accepted`, §7 executed same session |
| BluSky `inactivity_max_idle_days` 30 → **22** | TIGHTENS a venue fact | ADR 2026-08-05b, primary-sourced (ToU art. 11490284 §3.3) |
| `dd_lock_offset_usd` 100 → **1_000_000.0** on six Tradeify rows | TIGHTENS (removes an unreachable lock) | ADR 2026-08-04 `firm-rules-eval-lock-fix-applied` |

The loosening is disclosed, corroborated and propagated at its enforcement surface. It is **not** drift. It is, however, the source of three confirmed stale-figure findings, because the *derived* floors were never re-pointed.

### The finding the standard falsifier check misses — the audit's sharpest structural result

**No threshold moved — and yet several gates stopped binding or became unreachable, purely because their subject was withdrawn.** A falsifier check that reads only *threshold values* returns all-green over this table. That is the class:

| Gate | Was | Now |
|---|---|---|
| Third-leg **S5** cap table | reserves 69/11 | reserves capacity for legs that cannot fire; `LEG_MAP` untouched, so **inert-but-not-released** pending F2 |
| Third-leg **R1** $125/contract ceiling | +10% variance-inflation budget on a $273/day book σ | no book, nothing to inflate; propagated into ≥5 further live files |
| Third-leg **S1 / S3 / S6** | Tradeify flat-deadline, the rail as built, that firm's product set | all three are venue/rail artifacts of a de-scoped venue with F3 unruled — the one class that can produce a wrong **clearance** as well as a wrong rejection |
| **M1 4-session review trigger** | fires at 23.1% after 4 qualifying sessions (08-04 / 08-07 / 08-11 / 08-14) | no qualifying session can be drawn; **unreachable on the draw limb and trivially reached on the date limb** — it would "fire" on 2026-08-14 having sampled nothing, and it is booked on no board row |
| **Hard-core P4** tail-survival gate | delegates disposition to the 2026-06-07 decompound HOLD's §4 | that HOLD's own §4 banner reads *"NEITHER LIMB CAN FIRE TODAY … this HOLD currently has no live falsifier"* and its quarterly schedule was struck 08-03. P4 is `Accepted`, asserts *"P4's kill process is already running"*, and its §5 forbidden-move 4 bars it from forking a second process — so **P4 has no disposition process at all**, and the 2026-08-08 quarterly will supply no P4 verdict |
| **Q-SIGID-1** §6 verdict rows | RESOLVED / FALSIFIED / AMBIGUOUS all conditioned on a live Fri §2b observation | the 07-31 desk card is SPENT with its §2b table blank and no further MYM session is scheduled — stranded, and it is a *sixth* stranded thread that the ADR's five-thread enumeration does not carry |

**Six gates, zero threshold movement.** Every one of them would report "unchanged" to a check that greps for constants.

**`[R2]` — direct corroboration on the same limb, from a surface round 1 never opened.** Round 2 swept the `scripts/` estate and found **22 unwired-or-mis-scoped scripts against 37 files in `scripts/*.py`**. That is the identical failure shape measured on independent evidence: a gate whose *threshold* is intact and whose *reach* is not. The two measurements are not the same finding counted twice — round 1's table is gates made unreachable by a **subject withdrawal** (the legs went away), round 2's is gates made unreachable by **wiring and scope** (nothing invokes them, or they read the wrong tree). Together they establish that **the reachability limb, not the threshold limb, is where this programme's falsifiers fail**, and that it fails on both layers by two independent mechanisms.

**Consequence for the standing falsifier discipline.** A falsifier check that verifies values and not bindingness is measuring the limb that has never failed. The audit's recommendation follows directly and is filed in the follow-ups section: **every pre-registered gate needs a reachability assertion alongside its threshold assertion**, and a gate whose subject is withdrawn must be marked **unreachable**, not left green. `check_falsifier_reachability` is the nearest existing instrument and is itself only 25% anchored (below).

**Compounding.** At the anchor, the board's own rider-enumeration command dropped ≥8 live-obligation files including the whole hard-core P-gate family — while the same board warned *"the count is not a constant — enumerate it, never cite it from memory."* **Fixed `a818b3f`** (§3.1), with the family measured at **five (P1–P5)**, not four.

**META LAYER falsifier check.** The meta layer's own falsifiers are its gates. Executed:

- `check_adr_graph` → exit 0 while blind to two header fields the corpus uses and to one whole edge direction.
- `check_supersession_placement` → green over **6.8%** of its declared surface, and its companion `tests/governance/test_supersession_placement.py:96` asserts corpus cleanliness over that same collapsed selector with **no test pinning the selector itself**.
- `ops/sentinel/scan.py::skew_scan` → returns `[]` because its single registered `canonical_needle` ("p99 DD 0.63pp headroom") has **zero occurrences** in `CLAUDE.md`, and the guard `if needle not in claude: continue` fails **open and silently**, so an empty skew result is indistinguishable from a clean corpus. `[R2]` compounds it: the *documented* invocation (`python -m ops.sentinel.scan`) raises `ModuleNotFoundError` — the canonical form is `PYTHONPATH=ops python -m sentinel` — so the scanner is unreachable to a reader following the published instruction before it is uninformative to one who isn't.
- `check_falsifier_reachability --stats` → **21 of 83** falsifier sections anchored (**25%**) against a docstring claiming 28%: the census overstates and coverage is eroding.
- `.github/workflows/skills-check.yml` claims to be "the pre-commit backstop" while three hook items (`check_root_doc_liveness`, `roll_sessions --check-order`, `check_closure_disposition`) appear in no workflow at all.

**No meta falsifier threshold drifted; several meta falsifiers cannot fire, and one reports green over almost nothing.** With `[R2]`'s 22-of-37 measurement, the meta reading is no longer "some gates are mis-scoped" — it is that **the majority of the script estate has never been shown to bind**, and no instrument in the repo asserts bindingness as a property.

---

**Next:** disposition verdicts and their watch conditions follow in the verdicts section; the confirmed findings and their per-file actions follow in the findings sections. Index and combined counts: [`README.md`](README.md).


