# Stage-8 gains a variance-dominance companion (risk-N_eff-delta binding gate + daily-$-std pre-flight) — `2026-07-20-stage8-variance-dominance-risk-neff-gate`

**Status:** `Accepted` — operator ratified 2026-07-20 (superseding-ADR adoption route per campaign-template change control; co-sibling to `2026-07-13-stage8-mechanistic-exposure-companion.md`, **not** a supersede). Drafted by Claude Code 2026-07-20 from the Q-COMPOSE-1 closure lesson candidates. The 2026-07-13 companion was consolidated here as Companion A on 2026-10-15.
**Decision date:** 2026-07-20
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-w4-minimal-gate-set-dormancy.md` — sole-producer status of risk-breadth coordinates while `breadth.py` is tombstoned (doctrine retained; producer dormant)
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 body condensed; §6 downstream list, §7 and Verification removed; §10 reduced to its still-runnable hooks; 2026-09-01 addenda condensed (ruling verbatim); 2026-07-13 mechanistic-exposure companion absorbed as Companion A. Pre-trim text at blob `4feb50c4efab3290ba5096059987787f4fc4c646` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).

---

## §0 — Rule 0 reads (production-source verification)

Read 2026-07-20: `lab/research_utils/breadth.py` @ `d83e0f9` already emits `n_eff_risk` (participation ratio of the weekly covariance matrix) and `n_eff_risk_delta` on candidate injection (Q-NEFF-1 4-leg anchors 3.98 dependence / 3.09 risk); the Q-COMPOSE-1 closure @ `4de8085` (figures in §1); the 2026-07-13 sibling @ `ba943a1`; ORB-MNQ-1 `ADMISSION.md` @ `9620138`; the template Stage-8 row. Full reads: [prior revision](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md).

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

**Trigger check schedule:** evaluated at each quarterly regime cluster (2026-11-08, 2027-02-08) and on the close of every composed-candidate evaluation, whichever fires first. Companion A (carried from the removed `2026-07-13-stage8-mechanistic-exposure-companion.md` §4): hard check 2026-11-08 — shock-conditional MC vs stream bootstrap on the three-leg family; < 1pp joint bust delta at every grid point → demote Companion A to annotation-only; module not runnable by 2026-11-08 → AMBIGUOUS, escalate at that gate.

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
```

---

## Companion A — mechanistic exposure

*Consolidated 2026-10-15 from `2026-07-13-stage8-mechanistic-exposure-companion` (removed; see [TOMBSTONES](TOMBSTONES.md#2026-10-15-adr-decay-audit-removals)). Operator ratified 2026-07-13; [prior body](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-13-stage8-mechanistic-exposure-companion.md). A distinct Stage-8 blindness from variance dominance (§1). The text below is that ADR's §1–§5, verbatim except spent items; its section references (§2c, §8) use the original numbering — §2a–§2c are items (a)–(c) under Decision.*

**Symptom (measured 2026-07-13).** Three legs of the ratified one-beta family, on their seven-year futures panels (2026-07-12 TV exports: Striker→MYM, Striker-NAS→MNQ, Aegis→6J), measure as follows. Direction census: 287/287 long, 290/290 long, 155/155 short-yen — every trade in all three books is the same macro side. Entries cluster in the NY morning; time-in-market is 0.62% / 0.67% / 0.27% of the clock; in-market overlaps in seven years: 64 (MYM×MNQ), 18 (MNQ×6J), 4 (MYM×6J); days all three traded: 6; days all three lost: 0. And yet pairwise monthly correlations on equity-deflated streams are −0.10 / +0.13 / −0.01, worst-decile-month overlap 0–1 of 9, same-day both-lose rates at or below the independence baseline, max-DD windows fully disjoint.

The zero is a sampling fact, not an exposure fact: episodic strategies are almost never in-market together, so the shared factor has no data through which to express itself. Consequences: (1) Stage-8's realized-stream statistic cannot detect same-beta duplication for exactly the strategy class the discovery engine most plausibly emits (NY-session, direction-conditional, episodic) — a candidate that is the incumbent beta with a fresh label passes by construction; (2) any bootstrap that resamples these realized streams (week-block included) mechanically reports near-independence and cannot price the common-mode event (zero occurrences in seven years to resample). The known common-mode kill path stays both uninsured and unmeasured. This finding is robust to the Q-TVCOV-1 census outcome: it is driven by structural non-overlap, which only strengthens if pre-2022 segments are discarded.

**Decision.**

**(a) Campaign template, Stage-8 row** — append a companion clause:

> …reproduces the Q-NEFF-1 4-leg anchor first. **Companion (mechanistic exposure):** every Stage-8 candidate files an exposure declaration — {unconditional or regime-conditional side; entry session window (ET); expected in-market minutes/yr; per-book-leg structural overlap = expected simultaneous-in-market minutes/yr × sign-agreement} — and the campaign pre-registration binds a structural-overlap admission threshold at Stage 0. Realized-correlation/ENB deltas remain reported but are not sufficient for breadth admission for episodic candidates (in-market < 5% of session clock).

**(b) Envelope §2** — add item 5: exposure-coordinates annotation (same fields) required at closure alongside `DEPLOYABLE-DEFAULT-ENVELOPE`, so the coordinates travel to the deployment fork.

**(c) Consumer note** — 08-08 Class A (accept-beta fork), proposed input only, packet owner accepts/rejects: the program-level MC pricing the accept-beta decision should add a shock-conditional module — impose an adverse NY-morning gap over a pre-registered grid (e.g., −1% to −5%) on a max-concurrency day, all in-market legs at entry-time sizing, evaluated against per-account rule sets — precisely because stream resampling cannot generate the event. Not a unilateral packet edit.

Applied 2026-07-13: template Stage-8 row; envelope §2 item 5 ([`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md)); (c) was recorded as a proposed input in the 08-08 pre-triage brief. The packet never dispositioned it and the module was never built (status 2026-10-15).

**Alternatives considered.**

| Alternative | Why ruled out |
|---|---|
| Tighten the correlation/ENB threshold | Blind is blind at any threshold — the statistic reads ≈0 for same-beta episodic legs regardless of the cut. |
| Demand longer panels before Stage 8 | Event frequency, not panel length, binds: seven years produced six all-three days. |
| Handle exposure only at the deployment fork | Too late — discovery K budget is spent re-manufacturing the incumbent beta; Stage 8 exists to gate book-level admission. |
| Drop the correlation delta entirely | Q-NEFF-1 anchor reproduction still catches dense-overlap duplication cheaply; companion, not replacement. |

**Falsifier.**

**H (hypothesis):** the blindness is material to bust risk.

**Test (pre-registered here, before any run):** run the §2c shock-conditional module on the current three-leg family versus the stream-bootstrap estimate under identical per-account rule sets. **Falsifier:** if, at every point of the pre-registered shock grid, the joint bust-probability delta is < 1pp absolute, the companion demotes to annotation-only (declaration retained, no admission gate) via superseding ADR. Grid and rule sets frozen in the run's pre-registration; first run owed with the 08-08 packet work; hard check 2026-11-08.

**Verdict (binary):** RESOLVED (delta ≥ 1pp somewhere on the grid — companion stands) / FALSIFIED (< 1pp everywhere — demote to annotation-only) / AMBIGUOUS (module not runnable by 2026-11-08 — escalate at that gate).

Status 2026-10-15: undischarged; module unbuilt; the 2026-11-08 hard check is carried in §4's `**Trigger check schedule:**` field.

**Forbidden moves.**

- Choosing or trimming the shock grid after seeing MC output.
- Letting exposure declarations become entry filters — declarations describe, never filter (default #4's "test conditions, never filters" applies).
- Editing the §Campaign-defaults table or the Stage-8 row in place without this ADR's ratification event.

---

## Addendum 2026-09-01 -- `breadth.py`'s risk-N_eff producer revived on canonical CME data; this ADR's "producer dormant" clause is stale

[`2026-08-19-cme-broker-panel-admission-for-breadth-revival.md`](2026-08-19-cme-broker-panel-admission-for-breadth-revival.md) registered a `"cme"` panel in `core/mc/modes.py` `PANELS_BY_BROKER`, so `breadth.py` runs on real CME data with measured anchors (`CME_NEFF_DEPENDENCE_ANCHOR = 1.9988`, `CME_NEFF_RISK_ANCHOR = 1.0871`). The header's "producer dormant" clause is historical. §2's binding gate and ρ pre-flight are unaffected. Whether this is W4's re-arm event is ruled below.

## Addendum 2026-09-01 (operator ruling) — 2026-08-19 revival is not W4's re-arm event

**Ruling (direct operator instruction, 2026-09-01):** the 2026-08-19 CME-panel admission does **not**
count as the re-arm event W4 §2's dormancy table names. Envelope §2 item 6 (risk-breadth coordinates)
**stays report-optional / doctrine-retained**, not mandatory, until a session actually evaluating a
new book-leg admission decision explicitly rules on re-arming it.

Grounds (condensed 2026-10-15): the revival ADR carries no graph edges, never says "re-arm", and its §0 disclaims altering the Stage-8 gate; the re-arm call belongs to a session with a live admission decision. Full text: prior revision (see Revision).

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-20 | Initial authoring (Status `Proposed`) — promotes Q-COMPOSE-1 lesson candidates #1/#2 to a Stage-8 gate | Claude Code (draft) · Joshua (ratification owed) |
| 2026-07-20 | Ratified — Status `Accepted`; §6 downstream applied (template Stage-8 row, envelope §2 item 6, lesson M-21, STATE pointer) | Joshua (decision) · Claude Code (apply) |
| 2026-09-01 | Addendum: breadth.py's risk-N_eff producer revived 2026-08-19 on canonical CME data; "producer dormant" clause stale; operator call on whether this counts as W4's re-arm condition | Claude Code (ADR-corpus reconciliation sweep) |
| 2026-09-01 | Ruling: 2026-08-19 revival is not treated as the re-arm event; envelope §2 item 6 stays report-optional pending a session with an actual admission decision in front of it | Claude Code (ADR-corpus reconciliation sweep, operator ruling) |
| 2026-10-15 | Spent §6-downstream/§7/Verification removed; §0 condensed; §10 reduced to still-runnable hooks; 2026-09-01 addenda condensed (ruling verbatim); 2026-07-13 companion absorbed as Companion A with its 2026-11-08 hard check carried in §4's trigger field | ADR decay audit |
