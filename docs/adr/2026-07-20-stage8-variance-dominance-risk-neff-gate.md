# Stage-8 gains a variance-dominance companion (risk-N_eff-delta binding gate + daily-$-std pre-flight) — `2026-07-20-stage8-variance-dominance-risk-neff-gate`

**Status:** `Accepted` — operator ratified 2026-07-20 (superseding-ADR adoption route per campaign-template change control; co-sibling to `2026-07-13-stage8-mechanistic-exposure-companion.md`, **not** a supersede). Drafted by Claude Code 2026-07-20 from the Q-COMPOSE-1 closure lesson candidates.
**Decision date:** 2026-07-20
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-w4-minimal-gate-set-dormancy.md` — sole-producer status of risk-breadth coordinates while `breadth.py` is tombstoned (doctrine retained; producer dormant)
**Retain-until:** none

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR (this session, 2026-07-20):

- `lab/research_utils/breadth.py` — anchor: `d83e0f9` (verified `git log -1 -- lab/research_utils/breadth.py` on 2026-07-20). Confirms the Stage-8 tool **already emits** `n_eff_risk` (PR of the weekly covariance matrix) and `n_eff_risk_delta` on candidate injection — the gated statistic historically was `n_eff_dependence` / ENB, not risk. Self-test anchors: Q-NEFF-1 4-leg baseline 3.98 dependence / 3.09 risk.
- `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md` — anchor: `4de8085` (verified 2026-07-20). Source of the two lesson candidates this ADR promotes to a gate. Confirmed numbers: composed 3-leg bust 38.75% (Tradeify full) vs 2.65% 2-leg baseline; ORB daily-$std $438 vs whole-book $273; composed ~$539/day vs unchanged $3,000 trailing barrier; dependence N_eff 1.9948→2.9502; **risk N_eff 1.96→1.96 (flat)**.
- `docs/adr/2026-07-13-stage8-mechanistic-exposure-companion.md` — anchor: `ba943a1` (verified 2026-07-20). The sibling companion this one is authored parallel to; it addresses realized-**correlation** blindness for same-beta episodic legs, a **distinct** failure mode from variance dominance. This ADR adds a second companion clause; it does not touch the 2026-07-13 clause.
- `lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md` — anchor: `9620138` (verified 2026-07-20). The admitted candidate whose composition Q-COMPOSE-1 falsified; confirms ORB-MNQ-1 was admitted on dependence-breadth (+0.96 N_eff) with risk-breadth flat, the exact separation this gate makes decision-binding.
- Campaign template Stage-8 row content-read 2026-07-20 (`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`): current row gates on "5th-column ENB / cross-leg-correlation delta" + the 2026-07-13 mechanistic-exposure companion; **no risk-N_eff / variance clause present** — the gap this ADR fills.

**Owed at implementation (not read this session):** `ops/prop_envelope_default.md` §2 (envelope item add is a §6 downstream — Rule-0 read it before the §7 Phase-1 edit); `core/mc/modes.py` / the compose harness `run_compose_regime_remc.py` (if ρ emission is wired MC-side).

---

## §1 — Context

Q-COMPOSE-1 (CLOSED FALSIFIED 2026-07-17) tested adding the discovery-factory's only admitted survivor, ORB-MNQ-1, at its admitted 0.37% weight into the live 2-leg MYM+MNQ prop book, and the composed book's bust probability detonated to 38.75–67.63% across all four automation-friendly firm tiers versus a ~2.65% 2-leg baseline — 15–23× over the 3.0% ceiling, on partitions the 2-leg book passes. The kill mechanism was **not** the expected regime-common-mode contest but plain **variance dominance**: ORB's daily dollar std at the $100K basis ($438) exceeds the *entire* 2-leg book's ($273), so against a dollar-denominated **trailing** drawdown barrier the composed series collapses bust geometry regardless of correlation. The decisive signal was in the Stage-8 tool's own output all along — `n_eff_risk_delta ≈ +0.00` while `n_eff_dependence_delta` read a flattering +0.96 — but only the dependence/ENB figure was decision-binding at admission, so ORB was admitted as a "near-independent diversifier" it geometrically is not for this barrier. The closure recorded two lesson candidates (*"dependence N_eff is not a bust-geometry input; risk N_eff is"* and *"the cheap daily-$std falsifier ran before the expensive engine and was decisive"*) but the grep confirms neither was promoted to a standing lesson or a gate; the number remains printed-but-not-gated. This ADR is authored as the co-sibling of `2026-07-13-stage8-mechanistic-exposure-companion.md`, which added a companion for a *different* Stage-8 blindness (correlation-invisibility of same-beta episodic legs); variance dominance is the second blindness and needs its own clause.

**Decision driver (one sentence):** The one composed-candidate datapoint the program has (ORB-MNQ-1) was admitted on a breadth statistic that is blind to the exact geometry that then falsified its deployment, and the correct statistic is already computed but not binding — so the next candidate would repeat the error unless the risk-space screen is made a gate before the 2026-08-08 packet reopens composition.

---

## §2 — Decision

**Decision:** Stage-8 composition admission gains a **variance-dominance companion** with two mechanical screens, both bound a-priori in the composed-candidate's pre-registration (never tuned after MC output):

1. **Binding gate — risk-N_eff-delta floor.** A candidate is admissible as a composed **book leg** only if `n_eff_risk_delta ≥ τ_risk` (from `breadth.py`, PR of the weekly covariance matrix, candidate-injected minus same-window baseline), where `τ_risk > 0` is set in the compose pre-registration §9. A positive `n_eff_dependence_delta` (correlation breadth) is **explicitly not sufficient** for a book-leg add. ORB worked example: risk-delta +0.00 → **fails** the floor at any `τ_risk > 0`.

2. **Mandatory pre-flight disclosure — daily-$-std ratio.** The compose pre-registration §7 must surface `ρ = (candidate daily-$std at the intended weight and firm $-basis) / (existing book daily-$std)` **before** the frozen-engine run, alongside (not merely) weekly vol. `ρ ≥ 1.0` (a single leg carrying ≥ the whole book's dollar variance) is a **presumptive reject**: the pre-registration must either bind a smaller weight up front or drop the candidate as a book leg — it may not proceed to the frozen engine on an unjustified variance-dominant weight. ORB worked example: ρ = $438/$273 = 1.60 → presumptive reject, knowable at panel-build in seconds.

Both screens gate **composition-into-the-book only**. They do **not** gate lifecycle admission (a candidate may remain a standalone `CANDIDATE @ 1.00×` — ORB-MNQ-1 does), and they do **not** touch any locked parameter, allocation, `dd_protection`, or `ACTIVE_FIRM`.

**Effective:** immediately upon acceptance; first binding use is the 2026-08-08 packet's composition work.
**Scope:** every candidate proposed as a leg of a live prop book (compose re-MC), across all `AUTOMATION_FRIENDLY_PROP_FIRMS` tiers. Not applied to standalone lifecycle admission or to the locked 4-leg book (parameter axis untouched).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep gating on dependence-N_eff / ENB only (status quo) | Blind to the geometry that falsified ORB — the tool printed risk-delta +0.00 and the book still blew to 38.75%. Status quo admits the next variance-dominant "diversifier" by construction. |
| Tighten the dependence-N_eff / correlation threshold | Wrong axis at any cut. ORB's dependence delta was strongly positive (+0.96); no dependence threshold separates a variance-dominant leg from a genuine risk diversifier. |
| Let composition rely solely on the frozen-engine bust MC (no pre-screen) | The engine is a 1.5 h run gated behind a signed pre-registration; the ρ pre-flight already implied the verdict in seconds. A cheap decisive screen that runs before an expensive one should gate first (closure lesson #2). Also spends discovery/compose K re-manufacturing known failures. |
| Make ρ / risk-N_eff a hard filter with a repo-wide constant threshold | Over-rigid and invites a single magic number. Binding `τ_risk` and the ρ line per-campaign in the pre-registration keeps the a-priori discipline (Trap #12) while allowing firm-$-basis differences; a repo constant would need its own ADR each time a firm tier changed. |
| Status quo — no decision | The 2026-08-08 packet reopens composition; without this the one lesson the program paid for (ORB) is not encoded and the error is free to recur. |

---

## §4 — Falsifier (revert trigger)

**H (hypothesis):** the risk-N_eff-delta floor + ρ pre-flight are *materially predictive* of composed-book bust — i.e., they separate admit/reject verdicts that the dependence-delta statistic gets wrong, and they do not false-reject candidates the frozen engine would pass.

**Revert trigger (binary):** if, by **2027-02-08** (the next-but-one quarterly regime cluster) **or** after **≥3 composed-candidate evaluations** carrying both a screen verdict and a frozen-engine verdict, whichever comes first, **either**:

- **(immaterial)** every candidate's screen verdict agrees with what the dependence-delta statistic *plus* the frozen engine would have decided anyway (the screen never changes an outcome) → the gate adds no separating information; **or**
- **(false-reject)** any candidate the screen **rejects** (`n_eff_risk_delta < τ_risk` or `ρ ≥ 1.0`) is shown by a pre-registered frozen-engine run at the same weight to **pass** the ≤3.0% bust floor on all committed partitions → the screen's necessity claim is falsified,

then this ADR is revoked.

**Revert action:** author a superseding ADR that demotes the binding gate to **advisory-disclosure-only** (ρ and risk-N_eff-delta still reported in §7, no admission gate) — parallel to the 2026-07-13 companion's own annotation-only fallback. Never silently edit this ADR's decision text.

**Verdict (binary):** `RESOLVED` (a composed-candidate evaluation shows the screen changing an outcome the dependence-delta statistic got wrong, with no false-reject — gate stands) / `FALSIFIED` (immaterial or false-reject limb above fires by the schedule — demote to advisory-only via superseding ADR) / `AMBIGUOUS` (no composed candidate reaches a frozen-engine verdict by 2027-02-08 — escalate at that quarterly cluster, hold the gate meanwhile).

**Trigger check schedule:** evaluated at each quarterly regime cluster (2026-11-08, 2027-02-08) and on the close of every composed-candidate evaluation, whichever fires first.

---

## §5 — Forbidden moves (under this ADR)

- **Iterating a failed composed candidate's weight to squeak it past the screen or the engine** — Q-COMPOSE-1 §5: "a failed composed candidate closes; it does not iterate weight." The screen binds the weight *a-priori* in the pre-registration; searching weight after a fail is p-hacking the composition (Trap #12). ORB's role as a c1 book leg is closed — this ADR does not reopen it.
- **Treating a positive `n_eff_dependence_delta` as sufficient for a book-leg add** — the exact error that admitted ORB. Correlation breadth without risk breadth is the falsified pattern; dependence-delta is necessary-context, never the admission grant.
- **Tuning `τ_risk` or the ρ line after seeing MC output** — both must be frozen in the compose pre-registration §9/§7 before any engine run (Trap #12). If a threshold is wrong, author a fresh superseding ADR; do not amend this one's text.
- **Letting the screen become a strategy entry filter** — parallels the 2026-07-13 §5 "declarations describe, never filter." This gates *book composition admission* (a legitimate Stage-8 gate), never signal-level entry.
- **Reviving "gate on dependence-N_eff only" (§3 alt) without new evidence** — requires a datapoint where dependence-delta out-predicts risk-delta on composed bust, not a restated preference.

---

## §6 — Consequences

**Positive consequences:**
- The one lesson ORB-MNQ-1 cost is encoded as a gate rather than a footnote; the next variance-dominant "diversifier" is caught at panel-build, before K or a 1.5 h engine run is spent.
- The gate reuses an already-shipped, already-tested, anchor-verified computation (`breadth.py` `n_eff_risk_delta`) — near-zero implementation surface for the binding half.
- ρ makes the decisive quantity legible up front, satisfying closure lesson #2 ("surface injected-leg vs book daily-$-std ratio in §7, not just weekly vol").

**Negative consequences (real cost, not theatrical):**
- One more bound threshold (`τ_risk`) and one more disclosure (ρ) per composed-candidate pre-registration — marginal ceremony; §4 exists to kill the gate if it proves immaterial.
- ρ is not currently emitted by `breadth.py` (it is return-space; ρ is $-space, computed in the compose MC harness) — a small wiring or manual-compute item until surfaced.

**Risks (probabilistic, distinct from costs):**
- **Single-datapoint induction.** The gate is generalized from one composed candidate (ORB). Mitigation: §4's ≥3-evaluation / false-reject clause forces a demote if the separation doesn't hold on the next candidates.
- **`τ_risk` set too tight** could false-reject a genuine risk-diversifier; the §4 false-reject limb is the explicit guard, and `τ_risk` lives per-campaign so it can be justified against that campaign's baseline.

**Downstream artifacts that need updating (Status stays `Proposed` until all done):**
- `docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md` Stage-8 row — append the variance-dominance companion clause (parallel to the 2026-07-13 mechanistic-exposure clause).
- `ops/prop_envelope_default.md` §2 — add an item: risk-N_eff-delta + ρ coordinates travel to the deployment fork (Rule-0 read the file first).
- `docs/methodology/lessons/methodology_lessons.md` — **promote Q-COMPOSE-1 lesson #1** to a standing lesson (dated 2026-07-17; dollar anchor: composed bust 2.65%→38.75% on the $100K Tradeify tier, ~15× the 3.0% ceiling — a book-blowup counterfactual well past the E1 >$3K single-incident bar).
- `STATE.md` — one pointer line under the executed-decision log once ratified.
- (Optional) `lab/research_utils/breadth.py` / compose harness — emit ρ so §7 disclosure is mechanical rather than hand-computed.

---

## §7 — Implementation plan

- **Phase 0** — re-confirm §0 anchors current at apply-time (`git log -1` on `breadth.py`, the closure, the 2026-07-13 ADR); Rule-0 read `ops/prop_envelope_default.md` §2 before editing it.
- **Phase 1** — apply the four documentation edits in §6 (template Stage-8 row; envelope item; methodology lesson promotion; STATE.md pointer). These are the substance; a small CC handoff (`references/cc_handoff.md`) is warranted only if the envelope/lesson edits touch >1 file family — otherwise direct apply.
- **Phase 2** — grep-sweep for any Stage-8 doc asserting "breadth = dependence/ENB delta" without the variance companion, and cross-link this ADR from the 2026-07-13 sibling's Related line.
- **Phase 3** — verification block executes; on green + operator ratification, Status → `Accepted`.

---

## §10 — Audit hooks (runnable)

```bash
# Variance-dominance companion applied to the campaign template?
grep -n "risk-N_eff\|variance dominance\|daily-\$-std\|n_eff_risk_delta" \
  docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md \
  || echo "Stage-8 variance companion NOT applied (check §6 disposition)"

# Lesson #1 promoted out of candidate status?
grep -n "risk N_eff\|variance dominance\|dependence N_eff is not a bust-geometry input" \
  docs/methodology/lessons/methodology_lessons.md \
  || echo "Q-COMPOSE-1 lesson #1 still candidate-only (not promoted)"

# The gated statistic is really computed (guard against breadth.py regressing away n_eff_risk_delta)
grep -n "n_eff_risk_delta" lab/research_utils/breadth.py \
  || echo "breadth.py no longer emits n_eff_risk_delta — gate has no input"

# §4 falsifier check (run at each composed-candidate close / quarterly cluster):
# For each evaluated composed candidate, compare (screen verdict) vs (frozen-engine verdict)
# and vs (dependence-delta-only verdict). Demote if immaterial or a false-reject appears.
# Next scheduled evaluation: 2026-11-08 regime cluster; hard revert check 2027-02-08.

# ADR graph integrity
python scripts/check_adr_graph.py   # expect exit 0 (A2 edge-check skipped while Proposed)
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python "C:/Users/joshu/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/72fdf38f-9be5-43cc-9803-8e04bfac2290/4a461c5e-0034-4ec3-8928-8324158d1365/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md --type adr
# Expected: all 6 checks PASS

# ADR lifecycle graph
$ python scripts/check_adr_graph.py
# Expected: exit 0; A2 reverse-edge check skipped (this ADR is Proposed, Supersedes: none)

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format='%h %ci' -- lab/research_utils/breadth.py                       # expect d83e0f9
$ git log -1 --format='%h %ci' -- docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md  # expect 4de8085
$ grep -n "438\|273\|1.9948\|2.9502\|1.96 → 1.96" docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md

# Sibling cross-reference (co-companion, not supersede)
$ grep -n "2026-07-13-stage8-mechanistic-exposure-companion" docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md
```

If §6 downstream artifacts haven't all been updated, the ADR stays `Proposed`. Do not flip to `Accepted` until the downstream sweep completes **and** the operator ratifies.

---

## Addendum 2026-09-01 -- `breadth.py`'s risk-N_eff producer revived on canonical CME data; this ADR's "producer dormant" clause is stale

**What changed.** This ADR's own `Superseded-in-part-by` field (-> `2026-08-07-w4-minimal-gate-set-dormancy.md`)
carries the clause *"sole-producer status of risk-breadth coordinates while `breadth.py` is
tombstoned (doctrine retained; producer dormant)"* -- accurate when W4 ratified 2026-08-07.
[`2026-08-19-cme-broker-panel-admission-for-breadth-revival.md`](2026-08-19-cme-broker-panel-admission-for-breadth-revival.md)
(`Accepted`, ratified 2026-08-19) registered a `"cme"` entry in `core/mc/modes.py`
`PANELS_BY_BROKER` for the two `AUTHORIZED` legs (Striker DJ30/MYM, Striker NAS100/MNQ) -- confirmed
present at `core/mc/modes.py` lines 115-133 this session. `breadth.py`'s `load_baseline_panel()` no
longer fails for lack of a registered panel, and its self-test anchors now carry a measured,
non-placeholder fresh value: `CME_NEFF_DEPENDENCE_ANCHOR = 1.9988` / `CME_NEFF_RISK_ANCHOR = 1.0871`
(`lab/research_utils/breadth.py` lines 69-70) -- the §7 Phase-2 measurement the revival ADR called
for was actually executed. The producer runs on real data today; "producer dormant" no longer
describes the current state.

**What this does and does not affect.** §0-§10 above stay byte-unedited as the historical record
(Rule 14); this addendum is the discharge. No operative clause of this ADR changes: the binding
gate (§2 item 1, risk-N_eff-delta floor) and the ρ pre-flight (§2 item 2) are unaffected by which
panel feeds them -- they gate on `n_eff_risk_delta`/ρ regardless of data source, and
`n_eff_risk_delta` is still emitted (confirmed, `lab/research_utils/breadth.py`).

> ⚠ **2026-09-01 reader-intercept:** the "not decided here" framing below is superseded by direct
> operator ruling the same day — see "Addendum 2026-09-01 (operator ruling)" below. The 2026-08-19
> revival is **not** treated as W4's re-arm event; envelope §2 item 6 stays report-optional. This
> paragraph is left unedited as the record of what this addendum originally proposed.

**Not resolved by this note -- an operator call.** Whether the 2026-08-19 revival is the "re-arm ADR
[that] restores a producer" W4 §2's dormancy table names as the condition for lifting "report-optional
/ no sole producer" back to a binding sole-producer status is not decided here. The revival ADR
registers a working data source and says in its own §6 that it "revives" the mechanism, but carries
no formal `Supersedes`/`Superseded-by` edge naming W4 or this ADR, and never uses the word "re-arm."
Whether envelope §2 item 6 is once again mandatory (not merely doctrine-retained/optional) is an
operator disposition this addendum does not make.

**Not re-opened by this note.** No new GO, gate change, or threshold re-election is authorized here.

## Addendum 2026-09-01 (operator ruling) — 2026-08-19 revival is not W4's re-arm event

**Ruling (direct operator instruction, 2026-09-01):** the 2026-08-19 CME-panel admission does **not**
count as the re-arm event W4 §2's dormancy table names. Envelope §2 item 6 (risk-breadth coordinates)
**stays report-optional / doctrine-retained**, not mandatory, until a session actually evaluating a
new book-leg admission decision explicitly rules on re-arming it.

**Grounds, all three independently supporting this reading:**
1. The revival ADR carries zero formal graph edges (`Supersedes: none`, `Superseded-by: none`,
   `Superseded-in-part-by: none`) — it does not touch W4's or this ADR's position in the supersession
   graph at all.
2. It never uses the word "re-arm" anywhere in its text.
3. Its own §0 explicitly disclaims altering the Stage-8 gate: *"This ADR's panel feeds that existing,
   unchanged mechanism; it does not alter the Stage-8 gate itself."* The authors had both W4 and this
   ADR open (both are read in full in its §0) and chose not to claim re-arm status — a deliberate
   scoping choice, not an oversight.

**Rationale for deferring rather than ruling the other way:** whether item 6 is mandatory is a real
decision with consequences — it determines whether a future candidate's risk-N_eff/dependence-N_eff
coordinates are a *required* clearance, not just optional context. That's better decided by whoever is
actually looking at a live admission decision than pre-emptively now, with no candidate pending
(Striker disarmed, no active third-leg candidate at this stage). `breadth.py` producing real numbers
again is necessary but not sufficient for re-arm; a session with an actual admission in front of it
should make that call explicitly, citing this addendum, rather than inheriting an implicit default
either way.

**What does not change:** §0-§10 above and the 2026-08-19 revival ADR's own text both stay
byte-unedited (Rule 14/Trap #12). The revival's factual content (panel registered, `breadth.py` runs
on real CME data, self-test anchors measured) is unaffected — only the mandatory/optional status of
envelope §2 item 6 is ruled on here, and it stays optional.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-20 | Initial authoring (Status `Proposed`) — promotes Q-COMPOSE-1 lesson candidates #1/#2 to a Stage-8 gate | Claude Code (draft) · Joshua (ratification owed) |
| 2026-07-20 | Ratified — Status `Accepted`; §6 downstream applied (template Stage-8 row, envelope §2 item 6, lesson M-21, STATE pointer) | Joshua (decision) · Claude Code (apply) |
| 2026-09-01 | Addendum: breadth.py's risk-N_eff producer revived 2026-08-19 on canonical CME data; "producer dormant" clause stale; operator call on whether this counts as W4's re-arm condition | Claude Code (ADR-corpus reconciliation sweep) |
| 2026-09-01 | Ruling: 2026-08-19 revival is not treated as the re-arm event; envelope §2 item 6 stays report-optional pending a session with an actual admission decision in front of it | Claude Code (ADR-corpus reconciliation sweep, operator ruling) |
