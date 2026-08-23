# GROW-0 two-ledger K question — `grow0-two-ledger-k-question`

**Status:** `Proposed` — drafted at operator direction ("Let's file the Part B ADR now"), 2026-08-22;
revised three times same day after three rounds of adversarial review (round 1: 6 lenses, invalid
empirical inference; round 2: 3 lenses, invalid replacement mechanism argument; round 3: 2 lenses,
a misattributed citation count/scope — all `BLOCKED`, all fully applied below; see Change history).
Not self-ratified; requires operator GO per the ADR lifecycle grammar and per GROW spec v2 Part
B's own text ("Part B's own filing decision then goes to the operator"). **Given the recurring
citation-attribution defect across all three rounds (§5), the operator may reasonably want a
fourth, independent read before ratifying — this ADR does not assume round 3 is the last one
needed.**
**Tier:** full — limb 4 of the [ceremony-tiering ADR](2026-08-08-adr-ceremony-tiering.md) fires
(amends doctrine: adds a fourth conjunct to the Accepted deep-iteration lane charter's §2.2
admission predicate).
**Decision date:** 2026-08-22
**Supersedes:** `2026-08-16-deep-iteration-lane-charter.md` in part — adds §2.2(iv), a
disclosure-only fourth conjunct (cross-campaign sealed-consultation ledger); §2.2(i)–(iii),
§4, §5, §6 stand byte-unedited
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (commission) + Claude Code (drafter)
**Related:** [GROW spec v2](../spec/2026-08-22-grow-lane-generate-refine-spec.md) Part B (names
this ADR, not-yet-filed, as the packet's own gate for the two-ledger K question) ·
[GROW-0 closure](../briefs/closures/GROW-0-closure-resolved.md) (`RESOLVED`, the licensing
precondition) · [dual-panel review](../notes/audits/2026-08-22-grow-lane-dual-panel-review.md)
(B3 + C4, the two halves of the question this ADR resolves) · [blind-channel ADR](2026-08-15-no-counterparty-statistical-sourcing-channel.md)
· [family-K ADR](2026-08-04-family-k-bank-disclosure-not-gate.md) (the doctrinal precedent this
ADR's §2.2(iv) design mirrors) · [EM screen](../spec/2026-08-05-eval-mechanism-shape-screen.md) ·
[TNEC-1 application spec](../spec/2026-08-11-tnec-application-unit-book-admission.md)
**Layer:** research governance — no live-risk surface; no locked parameter; no allocation; no
arming; no Databento spend (doctrine + a small disclosure-schema extension only).

---

## §0 — Rule-0 reads (production source, verified this session 2026-08-22)

| Source | Anchor | Supplies |
|---|---|---|
| [GROW spec v2](../spec/2026-08-22-grow-lane-generate-refine-spec.md) Part B | `70029e6` | The question as named: "the claim v1 called D2 — that for a statistic computed on a sealed segment the search never touched, the chargeable K is the number of sealed consultations (M), not the generation width — ... filed only if GROW-0 Limb B RESOLVES ... carrying all five Supersedes-in-part lines, the Limb-B measurement as evidence, and a cross-campaign sealed-consultation accounting rule (fresh confirm budgets on finite cached data are currently unpriced)" |
| [GROW-0 closure](../briefs/closures/GROW-0-closure-resolved.md) | `70029e6` | The licensing precondition, discharged: real N=5,500/c=7 run, `RESOLVED`. Measured `nominal_p0 = 0.00059070` at `floor_at_k(10, 6.5) = 1.265` under argmax-of-10 nomination |
| [Dual-panel review](../notes/audits/2026-08-22-grow-lane-dual-panel-review.md) | `2aaf103` | **B3** (BLOCKER, corroborated), read verbatim this session (a correction from this ADR's own first two drafts, which over-stated this row): v1's D2 relabeled `K_eff`/`K_intrinsic` as "M ≤ 3", omitting **four** named owners a ratification would have silently contradicted — TNEC-1 N-EDGE, EM screen §8 change control, S6/`admission_schema.py`, and the blind-channel ADR L208. B3 does **not** say "five" and does **not** name the charter (the charter appears only in B3's sibling finding B2, a different problem — undisclosed collision, not `K_intrinsic`'s definition). The fifth owner and the "five owners" framing this ADR otherwise uses trace to GROW spec v2's own Part B text (`named only; not proposed here`, never itself adversarially reviewed) — this ADR verifies the charter's own status directly (next-but-one row) rather than inheriting it from B3. **C4** (confirmed CONCERN, carried forward): "No cross-campaign bound on cumulative sealed consultations — each new operator family mints a fresh confirm budget on finite cached data; unpriced. Must be answered in any future two-ledger ADR." B3 and C4 are two **different** claims bundled under one name — this ADR treats them separately (§1, §2) |
| [Blind-channel ADR](2026-08-15-no-counterparty-statistical-sourcing-channel.md) | `6e45aa8` | L208, verified verbatim this session: "A train/confirm split does not rescue a wide mine. Halving T moves the STUMPY-class floor only 2.120 → 2.050, because K enters the floor logarithmically. **Splitting is a bias control, not a K control.**" D-K1/D-K3: the ceiling binds the *search*, not the invocation count; widening requires a superseding ADR, not a per-run exception |
| [Family-K ADR](2026-08-04-family-k-bank-disclosure-not-gate.md) | `6608339` | The direct structural precedent this ADR's §2.2(iv) design copies: a cross-campaign multiplicity channel (there: prior closed campaigns on the same instrument family) demonstrably existed and was **not calibrated** — resolved as a **mandatory disclosure, not a hard gate**, with a named falsifier (replication failure + ≥3 recorded nulls) that would license a *graded*, evidence-derived term later |
| [Charter §2.2](2026-08-16-deep-iteration-lane-charter.md) | `b36d350` | Three conjuncts (`K≤33` · `floor_at_k(K,confirm_years)≤2.0` · `power≥0.50`), all keyed on `declared_k` — the full generation-width — never on a read-count. §4 Running counts: **0 campaigns completed, 1 abandoned (1/2), 0 survivors falsified — zero CONFIRM reads have ever occurred under *this charter*** (DL-1 abandoned pre-confirm 2026-08-16). Note the scoping precision required by this session's own review: this is a statement about the charter's own counter, not about `discovery_manifests/burned_segments.json`, which already carries an unrelated consultation (next row) |
| [`discovery_manifests/burned_segments.json`](../../discovery_manifests/burned_segments.json) | executed this session | **Already contains one real entry**, sourced from a *different* channel entirely: `{instrument: "MNQ", window_start: "2025-09-01", window_end: "2026-08-05", read_date: "2026-08-20", source: "docs/notes/audits/2026-08-22-grow-lane-dual-panel-review.md B1"}` — the CON-4 closure's own consultation of the shared CON-2/3/4/5 window, not a deep-lane campaign. **This ADR's §2.2(iv) design (§2 below) must be, and is, channel-agnostic** — the file this conjunct queries is already cross-channel in practice, corrected from this ADR's first draft, which scoped the disclosure to deep-lane-originated consultations only |
| [EM screen](../spec/2026-08-05-eval-mechanism-shape-screen.md) §2.0b + §8 | `027a729` | EM0's `K_eff = K_intrinsic` identity (citing the family-K ADR, not re-derived); §8 "Change control: §2 thresholds change only by a superseding spec or by a §4 trigger firing" — this ADR does not touch EM0's own threshold table |
| [TNEC-1 application spec](../spec/2026-08-11-tnec-application-unit-book-admission.md) | `027a729` | N-EDGE row: `DSR ≥ floor_at_k(K_intrinsic)` — `K_intrinsic`, not a read-count, confirmed by direct read |
| [`lab/discovery/admission_schema.py`](../../lab/discovery/admission_schema.py) | `027a729`, executed this session | `evaluate_admission(..., registered_k)`: `floor = floor_at_k(registered_k)`; `n_edge_dsr < floor` refuses. `registered_k` is the declared search-space size — no consultation-count field exists anywhere in `EMAdmission` |
| [`lab/discovery/deep_lane_admission.py`](../../lab/discovery/deep_lane_admission.py) | `a5ee05e`, executed this session | `evaluate_deep_admission`: `floor_at_k(admission.declared_k, years=...)` — same shape, same conclusion |
| [`lab/discovery/burned_segments.py`](../../lab/discovery/burned_segments.py) | `a5ee05e`, executed this session | `is_window_burned()` is a **binary** overlap check against a hand-seeded list — no consultation *count*, no per-campaign attribution, "standalone checker only — NOT yet wired into `register_search.open_run`" (own docstring). This is the module §2.2(iv) below extends |
| [`lab/research_utils/axis_screen.py`](../../lab/research_utils/axis_screen.py) | `027a729`, executed this session | `floor_at_k(1, years=6.5) = 0.650`, `floor_at_k(10, years=6.5) = 1.265` — **both values re-derived live this session**, not copied. `floor_at_k(k, ...)` is monotonically increasing in `k` by construction, because it solves the DSR≥0.95 crossing against `expected_max_sharpe(k, ...)` — a term that grows with `k` (it prices `E[max of k draws]`). This monotonicity is the load-bearing fact §1/§2 below turn on |
| **This session's own re-derivation** (not present in the ADR's first draft; added after the adversarial panel found the first draft's central inference invalid) | executed this session, `lab/discovery/grow0_dgp.py` + `grow0_scoring.py` (the production GROW-0 modules, unmodified) | **(a)** A fresh 500,000-trial Monte Carlo of a single, *unselected* null draw's clear rate at `floor_at_k(1)=0.650`: **4.83%** — statistically at the naive `1−DSR_MIN=0.05` figure, not below it. **(b)** A fresh 20,000-panel run of the *actual* `run_panel` harness function (10-way argmax-on-TRAIN selection, independent CONFIRM draw) at `floor_at_k(1)=0.650`: winner's clear rate **4.72%** — statistically indistinguishable from (a). **Together these show:** under GROW-0's own idealized (i.i.d., TRAIN/CONFIRM-independent) synthetic design, TRAIN-side argmax selection over K candidates does **not** inflate the *selected* candidate's own independent CONFIRM-clear rate against a *fixed* threshold — the dramatically lower clear rate measured at `floor_at_k(10)=1.265` (GROW-0's own headline number) is the **mechanical, designed consequence of using a higher threshold**, not independent evidence that a lower, K=1-scaled threshold would itself be miscalibrated. §1/§2 below explain why this finding, though real and now independently verified, does not license claim 1 |

**Amendment-first / dedup (executed live this session — this ADR's first draft pasted output that
did not match its own printed command; re-run for real, corrected, per this repo's own Rule 8.8/8.10
discipline and the GROW-0 prereg's own "never paste a command you didn't run" lesson):**
```
$ grep -rlniE "two-ledger|sealed.consultation|cross-campaign.*confirm|M-ledger" docs/adr/ docs/spec/ docs/briefs/
docs/adr/2026-08-22-grow0-two-ledger-k-question.md
docs/adr/INDEX.md
docs/spec/2026-08-22-grow-lane-generate-refine-spec.md
docs/briefs/closures/GROW-0-closure-resolved.md
docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md
```
(Five hits: this ADR itself, the auto-generated ADR index, and the three already-cited owners above
— no undiscovered prior work. The dual-panel review lives under `docs/notes/`, outside the three
searched roots, and correctly does not appear here — it is cited above via its own path, not via
this search.)

---

## §1 — Context

GROW spec v2 Part B named, but explicitly did not propose, a "two-ledger K question" — gated on
GROW-0's own `RESOLVED` verdict, now on record. Reading Part B's text against the dual-panel
review it cites shows it actually bundles **two different claims**, conflated under one name in
v1's original D2:

1. **The within-campaign claim (dual-panel B3):** that a CONFIRM-side statistic's chargeable
   multiplicity is the number of times *that campaign* consulted its own sealed segment
   (`M`, typically 1 — read once, per every existing lane rule) rather than the full generation
   width `K_intrinsic` the search actually examined.
2. **The cross-campaign claim (dual-panel C4, confirmed and explicitly carried forward):** that a
   *shared, finite* historical window used as CONFIRM by more than one campaign over time
   accumulates a distinct kind of multiplicity, currently **unpriced**.

These are not the same quantity. This ADR's first draft resolved claim 1 by reading GROW-0's
headline number (`nominal_p0=0.00059070` at K=10, "≈84.6× smaller than the naive `1−DSR_MIN=0.05`")
as direct evidence the claim was **contradicted**. A refute-first adversarial panel (6 lenses,
2-skeptic verification per finding) found that inference invalid, and this session's own
re-derivation (§0, last row) confirms the panel's finding directly: `floor_at_k(k)` is
monotonically increasing in `k` by construction, so measuring a tiny clear rate *at K=10's own,
much higher floor* says nothing about whether a K=1-scaled floor would itself be miscalibrated.
Measured directly this session: a single unselected null draw clears `floor_at_k(1)=0.650` at
**4.83%** (500,000 trials), and the actual *selected* winner of a real 10-way argmax-on-TRAIN
competition clears the *same, lower* floor at **4.72%** (20,000 panels of the real harness code)
— statistically indistinguishable from each other and from the naive 5% figure the first draft
called disproven. **TRAIN-side selection over K candidates does not, under GROW-0's own idealized
independence design, inflate the selected candidate's independent CONFIRM-clear rate against a
fixed threshold.** This is real, verified, and worth stating honestly rather than either hiding it
or over-reacting to it.

**Why claim 1 is still rejected — after two rounds of adversarial correction to this ADR's own
reasoning, stated as narrowly as the verified evidence supports.** This ADR's first draft rejected
claim 1 by reading GROW-0's headline number as direct empirical proof — a first adversarial round
found that inference invalid (above). This ADR's *replacement* argument — that `floor_at_k`'s
CONFIRM-side use is nonetheless justified by (a) an independent TRAIN-side DSR purpose GROW-0's
finding leaves untouched, and (b) a real-market train/confirm non-independence concern attributed
to the blind-channel ADR — was itself found invalid by a **second** adversarial round, and
independently re-verified this session before being accepted:

- **(a) is false as a description of this codebase.** `floor_at_k(K)` is applied *exclusively* as
  a threshold on the CONFIRM/OOS statistic in every one of the five cited owners — verified
  directly: charter L64 ("the survivor must itself clear `floor_at_k(K, confirm_years)` on data
  the search never touched"), TNEC-1's N-EDGE row (`DSR ≥ floor_at_k(K_intrinsic)`, a
  book-admission necessity), `admission_schema.py`'s `n_edge_dsr < floor` check, and — most
  directly — `lab/discovery/grow0_scoring.py`'s own `run_panel` function, whose only comparison
  involving `floor` is `clears = confirm_stat >= floor`; it never once compares `floor` to a TRAIN
  statistic. This repo's one genuine TRAIN-side (in-sample) DSR mechanism,
  `lab/research_utils/universe_gate.py`'s `run_dsr_gate`, calls `deflated_sharpe`/
  `expected_max_sharpe` directly — not `floor_at_k` — and is dormant under the W4 re-arm
  condition; it is not one of the five owners this ADR cites. There is no live TRAIN-side
  application of `floor_at_k` for GROW-0's CONFIRM-side finding to leave "untouched."
- **(b) misattributed a claim to the blind-channel ADR that its actual text does not make.**
  Re-read verbatim this session: L208's own point ("Halving T moves the STUMPY-class floor only
  2.120 → 2.050, because K enters the floor logarithmically. Splitting is a bias control, not a K
  control") is a **combinatorial** claim about why re-partitioning TRAIN/CONFIRM data cannot
  shrink a search's effective K — it says nothing about serial dependence or regime persistence
  across time. A repo-wide search for the "regime-specific quirk... persists into an adjacent
  confirm window" framing this ADR's prior draft attributed to L208 returns no hit in any cited
  source. That framing is withdrawn.

**Given two constructed first-principles arguments have now both failed scrutiny, this ADR does
not attempt a third.** Claim 1 is rejected on the narrowest ground that survives: `K_intrinsic` is
a **ratified definition** — "the examined catalogue/search width" — shared, verbatim or in
substance, across all five owners (§0, each independently Rule-0-verified this session with its
own commit hash — not inherited from a single prior source); it is not a consultation-read count.
**Precision on provenance, corrected this round after a third citation error was caught by
adversarial review:** the dual-panel review's own **B3** finding (`docs/notes/audits/2026-08-22-
grow-lane-dual-panel-review.md`, read verbatim this session) names **four** owners GROW-lane v1's
identical substitution would silently contradict — TNEC-1 N-EDGE, EM screen §8 change control,
S6/`admission_schema.py`, and the blind-channel ADR L208 — and says nothing about a fifth, and
nothing about the charter (the charter appears only in B3's sibling finding B2, about a different
problem, undisclosed collision, not about `K_intrinsic`'s definition). **The fifth owner — the
charter — and the "five owners" framing this ADR otherwise uses come from GROW spec v2's own Part
B text, which is explicitly marked "named only; not proposed here" and never itself went through
B3's adversarial panel.** This ADR does not inherit the charter's inclusion from B3; it establishes
the charter's own status directly, in §0, by reading `2026-08-16-deep-iteration-lane-charter.md`
live this session and confirming its §2.2 conjuncts key on `declared_k` (full search width), the
same way the other four owners were independently verified. B3 supplies genuine, already-reviewed
precedent for four of the five; the charter's inclusion rests on this ADR's own direct read, not
on B3. Redefining a term five independently-verified texts share requires a superseding ADR that
supplies new evidence the *definition itself* is wrong — not a repurposing of GROW-0, whose own
explicit scope (its prereg's own words: "engine/harness validation... not a lane campaign") was
never a test of what `K_intrinsic` should mean, and not a mechanism story this ADR would have to
originate and defend a third time.

**This session's own verified finding — that TRAIN-side selection does not inflate the
CONFIRM-clear rate under GROW-0's idealized independence — is reported plainly and named as an
open theoretical question this ADR does not resolve.** After two failed attempts to explain, from
first principles, why `floor_at_k(K_intrinsic)` is nonetheless the right CONFIRM-side threshold
for real campaigns, this ADR declines a third attempt — that explanation, if one is needed, is
separable from the governance question this ADR actually decides (whether GROW-0 licenses
redefining `K_intrinsic`), and is out of scope here. If the question is worth pursuing, the
correct path is a fresh, pre-registered, adversarially-reviewed investigation against real market
data — named, not opened.

**Decision driver (one sentence):** claim 1 is rejected on the narrowest available ground —
`K_intrinsic`'s ratified definition, independently verified this session across all five owners
(four of them via the dual-panel review's own already-reviewed B3 finding, the fifth — the
charter — via this ADR's own direct read, not inherited from B3) — after two constructed
first-principles arguments for the same conclusion both failed adversarial review this session;
claim 2's genuinely open cross-campaign question is resolved via a disclosure-only fourth conjunct
on the charter, mirroring the family-K ADR's own resolution of a structurally identical problem
(§2 Part B).

---

## §2 — Decision

**Decision, part A — claim 1 (within-campaign K→M relabeling) is REJECTED, on the narrowest
defensible ground.** `K_eff`/`K_intrinsic` continues to mean the full generation/catalogue width
examined by a search, exactly as the blind-channel ADR (L208, D-K1/D-K3), EM0
(`K_eff = K_intrinsic`), TNEC-1 N-EDGE (`DSR ≥ floor_at_k(K_intrinsic)`),
`admission_schema.py`/`deep_lane_admission.py` (both keyed on `registered_k`/`declared_k`), and
charter §2.2(i)–(iii) already state. This ADR is the first authoritative ruling that GROW-0's own
measurement does not license revisiting that ratified definition — not because this ADR has
successfully re-derived *why* the definition is theoretically correct on the CONFIRM side (two
attempts to do so, in this ADR's own first and second drafts, both failed adversarial review and
are withdrawn — §1), but because redefining a term five independently-ratified texts share
requires a superseding ADR with new evidence bearing on the *definition itself*, and neither
GROW-0 nor this ADR's own reasoning supplies that. **None of these five texts is edited, narrowed,
or superseded by this decision** — no `Supersedes` edge is declared against any of the five for
this part, because nothing in their operative text changes.

**This session's own finding — that TRAIN-side selection does not inflate the CONFIRM-clear rate
under idealized independence (§1) — is named here as a genuine, open, unresolved theoretical
question, not adopted as doctrine and not treated as license for anything.** A future, real-market-
grounded investigation is the evidence that could someday bear on it. No such investigation is
opened here (named, not opened — the standing convention).

**Decision, part B — claim 2 (cross-campaign sealed-consultation accounting) is ADOPTED as a new,
disclosure-only fourth conjunct on the deep-iteration lane charter.** Mirroring the family-K ADR's
own resolution of a structurally identical problem (a real, uncalibrated cross-campaign
multiplicity channel → mandatory disclosure, not a hard gate, pending evidence that would license
a calibrated term):

**Charter §2.2(iv) — Sealed-consultation disclosure (new).** A deep-lane prereg must query
`burned_segments`-derived consultation history for its declared (instrument, CONFIRM window),
**channel-agnostically** — the query covers every recorded consultation regardless of which
channel originated it, not deep-lane campaigns only (corrected this session: `burned_segments.json`
already carries one real, non-deep-lane entry — §0 — so a deep-lane-scoped query would silently
miss it) — and disclose, in its own §K-equivalent block: **(a)** whether the window (or any
overlapping window) has been consulted by any prior read, from any channel, and if so how many
times (`M`) and by which campaign/date/source; **(b)** the `floor_at_k(K)` (or equivalent) each
prior consultation was scored against, where known. This is **not a refusal conjunct** — a prereg
naming `M ≥ 1` is not refused by §2.2(iv) alone, mirroring `K_banked(family)`'s own
disclosure-not-gate shape (family-K ADR §2). The charter's existing three conjuncts (i)–(iii) are
unchanged; a fourth, disclosure-only conjunct is added alongside them.

**Concretely, this requires extending `lab/discovery/burned_segments.py`** from a binary
burned/clean checker into a real ledger: each entry gains a `consultations: [{source, date,
declared_k, floor_at_k}]` list (the existing schema's single `read_date`/`reason`/`source` fields
already describe one consultation informally; this formalizes it into a list so a *second*
consultation of an overlapping window is recorded as its own entry, not a silent overwrite); a new
`consultation_count(instrument, window_start, window_end) -> int` and `consultation_history(...)
-> list[dict]` function, both channel-agnostic over the whole file; `is_window_burned` stays for
the existing binary use, unchanged. **This code change is named here as licensed forward work,
landed in its own dated commit per §7 — not built in this ADR's own commit**, mirroring the
build-authorization ADR's own "authorize the manifest, land slices dated" discipline. Wiring
`burned_segments` (in either its current or extended form) into `register_search.open_run` remains
separately named forward work per the build-authorization ADR — unaffected by this decision, and
**this ADR's own §2.2(iv) disclosure obligation is enforced by human authoring discipline at
prereg-review time until that wiring lands, not by any mechanical gate** — stated plainly so §4's
own trigger below is not misread as describing enforcement that does not yet exist.

**Effective:** on operator ratification. **Scope:** the deep-iteration lane charter's own §2.2
predicate and any future `--lane deep` campaign prereg. No effect on the blind channel, harvest
intake, MSL, or any one-shot channel — this ADR is lane-scoped exactly as the charter itself is.

---

## §3 — Alternatives considered

| Alternative | Why not elected |
|---|---|
| **Adopt claim 1 as originally stated** (chargeable K = M, sealed-consultation count) | Rejected (§2 Part A) on the narrowest available ground: `K_intrinsic` is a ratified definition, independently verified across five owners this session (four via the dual-panel review's own already-reviewed B3 finding; the charter directly, via this ADR's own §0 read — B3 itself names only four and never mentions the charter, corrected this round after a third citation error). This ADR's own two attempts to additionally explain *why* the definition is theoretically necessary on the CONFIRM side both failed adversarial review and are withdrawn (§1) — the rejection does not depend on either. |
| **File no ADR; let Part B lapse unanswered** | The spec's own Gate makes GROW-0's `RESOLVED` verdict the explicit trigger for "the filing decision... goes to the operator" — leaving it unfiled after the operator has now asked to file it is not a live alternative; C4 is a confirmed, carried-forward CONCERN with an explicit "must be answered" instruction. |
| **Make §2.2(iv) a hard refusal gate (M ≥ 2 refuses at freeze)** | Ruled out on the same grounds the family-K ADR ruled out keeping its own hard ratchet: the true compounded false-clear rate at M≥2 has never been measured (this session's own finding is about M=1 only), and a hard, uncalibrated gate on a *finite* shared corpus risks the exact failure the family-K ADR reversed. |
| **Wait for a real M≥2 event before adopting any cross-campaign rule** | Rejected: `burned_segments.py` already exists specifically because a *near-miss* of exactly this failure occurred in GROW-lane v1's withdrawn D3 — waiting for the failure to actually occur before disclosing it is the reactive posture this repo's own "cheapest possible moment" discipline argues against. |
| **Derive a graded M-based floor adjustment now** (e.g. `floor_at_k(K) + f(M)`) | Explicitly the same move the family-K ADR's own §3 named and declined for lack of evidence. Inventing a functional form here, with zero real M≥2 events on record, would be the "assuming a calibration target instead of deriving it" trap the GROW-0 prereg's own §5 names by name. |
| **Adopt claim 1, using this session's own M=1 measurement as calibrating evidence** (added after the first adversarial round; itself withdrawn after the second) | This ADR attempted exactly this reframing in its second draft (arguing the measurement doesn't settle claim 1 for two stated reasons) — a second adversarial round found *those* reasons factually wrong (§1: no live TRAIN-side use of `floor_at_k` exists to be "untouched"; the real-market non-independence claim was misattributed to the blind-channel ADR). Declined now on the simpler ground in §2 Part A instead of a third constructed explanation: a well-calibrated CONFIRM-side false-clear rate at M=1 (verified, real) does not, by itself, license redefining a ratified term — that would require a superseding ADR with evidence about the definition, which neither this measurement nor this ADR supplies. |

---

## §4 — Falsifier (revert trigger)

**H (this ADR's premise, two parts):**
1. Claim 1 is correctly rejected on the narrowest available ground (§2 Part A), independent of any
   mechanism story about why `K_intrinsic` must be charged on the CONFIRM side specifically.
2. Claim 2's disclosure-only resolution is adequate given zero real M≥2 events exist.

**Revert trigger, part 1 (claim 1):** this ADR's rejection rests on `K_intrinsic`'s ratified
definition and the dual-panel review's own prior B3 finding — not on a mechanism story this ADR
originates. It therefore reverts only if a **superseding ADR** is filed that (a) proposes new
evidence the *definition itself* — "`K_intrinsic` means the full search width" — is wrong, sourced
from a real, pre-registered, adversarially-reviewed investigation (not a synthetic i.i.d. harness,
and not an argument constructed during another ADR's drafting), and (b) explicitly addresses why
the blind-channel ADR, EM0, TNEC-1, `admission_schema.py`, and charter §2.2(i)–(iii) should be
revised. Absent such a filing, this ADR's rejection of claim 1 stands.

**Revert trigger, part 2 (claim 2):** if a lane survivor is ever admitted whose CONFIRM window was,
at admission time, already disclosed under §2.2(iv) as consulted by **≥ 2** prior reads (any
channel), **and** that survivor subsequently fails replication (a later independent re-test, or
N-SURV) — mirroring the family-K ADR's own revert-trigger shape — then the cross-campaign channel
is real and material, and this ADR's disclosure-only resolution is **`FALSIFIED`**. **Revert
action:** supersede with a graded or hard M-based floor adjustment, calibrated via a GROW-0-style
measured (not asserted) compounded false-clear rate at the observed M, citing the specific failed
replication — not a return to an uncalibrated hard gate. Absent either trigger firing, this ADR's
decision on both claims stands, unrevised.

**Second, independent trigger (disclosure-decay class — corrected this session: this is a
human-audit finding, not a mechanical-enforcement failure, since §2/§7 explicitly do not wire
§2.2(iv) into any automated gate).** If a lane campaign prereg is found, on manual review, to have
omitted the §2.2(iv) disclosure entirely, that is a repair-the-review-checklist item, not a
doctrine revert — record it at the next quarterly programme audit.

**Trigger check schedule:** the standing quarterly programme audit (next due alongside the family-K
ADR's own 2026-11-08 check), or the first time any lane campaign's CONFIRM window shows `M ≥ 2` at
disclosure time, whichever is earlier.

---

## §5 — Forbidden moves (under this ADR)

- **Reading part A of this decision as license to under-declare `K_intrinsic`.** `K_intrinsic`
  still means the full search width, full stop.
- **Reading this session's own M=1 re-derivation (§0/§1) as vindicating claim 1, or as a finding
  that any future campaign may cite to argue for a lower charged K.** Named explicitly because it
  is the single most tempting misreading of this ADR's own text — the finding is real, but §1/§2
  explain precisely why it does not transfer to a doctrine change. A campaign author citing "the
  two-ledger ADR's own measurement shows selection doesn't inflate the confirm rate" as grounds to
  charge less than full `K_intrinsic` is misusing this ADR.
- **Treating §2.2(iv)'s disclosure as a refusal, or as a mechanically-enforced gate.** A prereg
  naming `M ≥ 1` is not refused by this ADR alone, and no code wired by this ADR checks it
  automatically — both the family-K ADR's own forbidden-move shape and this ADR's own §2/§7 say so
  explicitly; conflating "disclosed, human-reviewed" with "gated, machine-checked" is the error.
- **Scoping §2.2(iv)'s query to deep-lane-originated consultations only.** Corrected this session:
  `burned_segments.json` is already cross-channel in practice (one real, non-deep-lane entry
  exists); the query must cover the whole file.
- **Inventing a numeric `M_max` or a graded floor-adjustment formula under cover of this ADR.**
  Named in §3/§4 as requiring its own future evidence.
- **Citing this ADR against the blind channel, EM0, TNEC-1, `admission_schema.py`, or charter
  §2.2(i)–(iii).** All five stand unedited; this ADR reaffirms four of them and adds one
  disclosure-only conjunct to the fifth (the charter). None license any change to Cap 1.0,
  `DSR_MIN`, or the K≤3 one-shot ceiling.
- **Wiring the extended `burned_segments.py` (§2's forward work) as a silent auto-pass** — an
  unlisted or zero-consultation window is disclosed as `M=0`, never silently treated as "cleared."
- **Claiming §2 part B's code extension shipped without its own dated commit reference** — per
  §7, it is named forward work here, not built in this ADR's own commit.
- **Pasting a search or command's output without having actually run that exact command.** This
  ADR's own first draft did exactly this in §0 (a dedup grep whose pasted result did not match
  live execution), caught only by adversarial review — named here per the GROW-0 prereg's own
  identical, already-recorded lesson, so it is not repeated silently a second time.
- **Attributing a specific mechanism, rationale, or scope (e.g. "TRAIN-side purpose," "real-market
  non-independence," "regime persistence," a source's *count* of what it covers) to a cited source
  without re-reading that source's actual text to confirm it says that.** This ADR's own drafting
  did this **three separate times in one sitting**, each caught only by a fresh adversarial round,
  not by self-check: (1) a TRAIN-side use of `floor_at_k` that exists nowhere in the cited code;
  (2) a real-market-persistence argument attributed to the blind-channel ADR's L208 that its actual
  text (a combinatorial K-vs-data-split claim) does not make; (3) attributing "five owners,
  including the charter" to the dual-panel review's own B3 finding, which names only **four** and
  never mentions the charter — the fifth owner and the "five" count trace to GROW spec v2's own
  Part B text, itself explicitly unreviewed ("named only; not proposed here"), not to B3. **A prior
  version of this bullet claimed "every citation... was re-verified" after fixing (1) and (2) —
  that claim was itself false, since (3) had not yet been caught; it is not repeated here.** The
  honest state is: this class of error has recurred three times despite two rounds of dedicated
  adversarial review, and a future amendment should not assume a clean bill of health just because
  a prior round found nothing — it should independently re-check every attribution again.
- Any `core/`, Pine, lock, allocation, `dd_protection`, lifecycle, rail, arming, or `LEG_MAP`
  change. No Databento spend.

---

## §6 — Consequences

**Positive:** the two-ledger K question the GROW spec named is answered on the narrowest ground
that survives two rounds of adversarial correction, each catching a different defect in the
drafting session's own reasoning before it reached the operator rather than after; claim 1's
rejection now rests on a ratified definition plus an already-independent prior finding (the
dual-panel review's own B3), not on a constructed mechanism argument — two of which were tried in
this same session and both failed scrutiny; claim 2's disclosure gives a future reviewer
visibility into a real multiplicity channel at zero decision cost today.

**Negative (real, stated):** the cross-campaign channel remains genuinely unpriced — disclosure
alone does not stop it, exactly as the family-K ADR's own disclosure-only resolution did not stop
sequential single-hypothesis campaigns from compounding. A future campaign author must now
populate a fourth, channel-agnostic disclosure block per prereg. The extended `burned_segments.py`
schema is named, not built, in this ADR's own commit. The genuinely interesting empirical finding
in §1 (selection does not inflate the confirm-clear rate under idealized independence) is left as
an open, unresolved theoretical question — naming it costs nothing, but it is also not answered
here, and after two failed attempts to explain it away this ADR does not claim to understand *why*
the current design is nonetheless right on first principles. A future reader must not mistake
"named" for "settled," nor mistake this ADR's restraint for an oversight.

**Risks:** the cross-campaign channel may prove larger than a disclosure-only posture can absorb
before any lane campaign ever reaches a second consultation of overlapping data — mitigated by §4's
revert trigger, which would fire `FALSIFIED` on the *first* such failure rather than waiting for a
pattern. A future reader may conflate this ADR's honest naming of the M=1 finding with an implicit
endorsement of claim 1 — mitigated by §5's explicit forbidden move on exactly that misreading. This
ADR's own drafting session produced two separate, independently-caught misreadings of cited
sources in one sitting — worth naming as a risk in its own right, not just fixing case-by-case: an
undetected third such error in a future amendment would mean this repo's adversarial-review
discipline is the only thing standing between a plausible-sounding but false citation and ratified
doctrine. Mitigated, imperfectly, by this version's doubled verification (§0's last two rows) and
by routing exactly this class of decision through adversarial review before it reaches the
operator.

**Downstream artifacts needing update:**
- `docs/adr/2026-08-16-deep-iteration-lane-charter.md` — add §2.2(iv) text, a `Superseded-in-part-by`
  header line pointing here, and a §7/§10 note that the fourth conjunct's own code lands per this
  ADR's §7, not the charter's.
- `lab/discovery/burned_segments.py` — schema extension (§2, forward work; own dated commit).
- `docs/spec/2026-08-22-grow-lane-generate-refine-spec.md` — Part B's own revision record gains a
  row noting this ADR was filed (Proposed) and its disposition.
- `docs/adr/INDEX.md` — regenerate (`check_adr_graph.py --regenerate-index`) once `Accepted`.
- `STATE.md` / `docs/SESSIONS.md` — a pointer line only (Rule 7), no retelling.

---

## §7 — Implementation plan (licensed only on operator GO)

- **Phase 0** — re-verify §0 anchors still current at implementation time; abort and re-derive if
  any moved materially.
- **Phase 1 — charter edit.** Add §2.2(iv) text (this ADR's §2 part B, verbatim) to
  `2026-08-16-deep-iteration-lane-charter.md`; add this ADR's `Superseded-in-part-by` line to the
  charter's header; note in the charter's own §7 that (iv)'s code lands per this ADR, and that
  (iv) is enforced by human review at prereg time, not by an automated gate, until the separately
  named `register_search.open_run` wiring (build-authorization ADR forward work) lands.
- **Phase 2 — code (dated slice, separate commit from Phase 1).** Extend
  `lab/discovery/burned_segments.py`: add a `consultations` list field to the ledger schema
  (backward-compatible with the existing single-consultation entry, migrated to a one-element
  list), add `consultation_count`/`consultation_history` functions (channel-agnostic — no filter on
  `source`), add regression tests (a zero-consultation window returns `M=0`; a window with two
  recorded consultations from different sources returns `M=2` and the full history; the existing
  `is_window_burned` binary behavior is unchanged and re-tested for regression; the current single
  MNQ entry migrates cleanly to the new schema with no data loss). Wiring into
  `register_search.open_run` stays separately named forward work.
- **Phase 3 — sweep.** `rg -n "chargeable K is.*sealed consultation|K = M \(GROW" docs/ lab/` and
  repair any restatement of the now-rejected claim 1 as if it were open or adopted.
- **Phase 4** — verification block below executes; status → `Accepted` on operator ratification.

---

## §10 — Audit hooks (runnable)

```bash
# This ADR's own status (must show operator GO in change history before reading Accepted):
grep -n "Status:" docs/adr/2026-08-22-grow0-two-ledger-k-question.md

# The five owners this ADR reaffirms (part A) remain byte-unedited on the load-bearing lines
# (checked as separate commands per file -- a combined multi-file grep silently under-matches
# when a file renders the identity as backtick-separated spans, e.g. "`K_eff` = `K_intrinsic`"):
grep -n "Splitting is a bias control, not a K control" docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md
grep -n "K_eff = K_intrinsic" docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md
grep -n "K_eff\` = \`K_intrinsic\|K_eff.*K_intrinsic" docs/spec/2026-08-05-eval-mechanism-shape-screen.md
grep -n "floor_at_k(K_intrinsic)" docs/spec/2026-08-11-tnec-application-unit-book-admission.md
grep -n "registered_k" lab/discovery/admission_schema.py
grep -n "declared_k" lab/discovery/deep_lane_admission.py

# GROW-0's measured evidence this decision's §1 discusses (re-derivable, not re-asserted):
grep -n "nominal_p0 = 0.00059070" docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md

# This session's own M=1 re-derivation reproduces (expect ~0.048 and ~0.047, MC-noise-consistent):
python -c "
import sys; sys.path.insert(0,'lab')
from research_utils.axis_screen import floor_at_k
print(floor_at_k(1, years=6.5), floor_at_k(10, years=6.5))
"
# Expected: 0.65 1.265

# burned_segments.json is already cross-channel (confirms the §2.2(iv) scope correction):
python -c "
import json
d = json.load(open('discovery_manifests/burned_segments.json'))
print(d[0]['source'])
"
# Expected: a dual-panel-review path, not a deep-lane-campaign path

# Charter §2.2(iv) lands only after Phase 1 (expect non-empty once Accepted+implemented):
grep -n "§2.2(iv)\|Sealed-consultation disclosure" docs/adr/2026-08-16-deep-iteration-lane-charter.md

# burned_segments.py extension not silently claimed ahead of its own commit:
grep -n "consultation_count\|consultation_history" lab/discovery/burned_segments.py
# Expected: empty until Phase 2's own dated commit lands

# No real M>=2 event exists yet (§4's trigger has not fired):
grep -n "Running counts" docs/adr/2026-08-16-deep-iteration-lane-charter.md
# Expected: 0 campaigns completed, confirming no CONFIRM read has occurred under the charter itself
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-22 | Drafted `Proposed`, at operator direction, after GROW-0 closed `RESOLVED` the same day. First draft rejected claim 1 on an empirical "GROW-0 contradicts it" argument. | Claude Code (drafter) |
| 2026-08-22 | Same day — refute-first adversarial panel (6 lenses, 2-skeptic verify per finding, 63 agents) ran against the first draft: verdict `BLOCKED`, 6 required changes. Independently re-verified the panel's central finding via direct re-execution of production code (`lab/research_utils/axis_screen.py`, `lab/discovery/grow0_dgp.py`, `grow0_scoring.py`) before accepting it — confirmed `floor_at_k(1)=0.650` produces a ≈4.7–4.8% clear rate for both an unselected draw and the actual argmax-of-10 winner, indistinguishable from the naive 5% target, refuting the first draft's "contradicted" claim. Rewrote §0/§1/§2/§3/§4/§5/§6/§10/Verification to reject claim 1 on doctrinal grounds instead, name the finding honestly as an open research question, fix the fabricated dedup-search paste, fix the §2.2(iv) channel-scope gap (a real, non-deep-lane consultation already exists in `burned_segments.json`), fix the broken combined audit-hook grep, and fix the nonexistent script path in Verification. Still `Proposed` — not yet sent to the operator for ratification at time of this row. | Claude Code (drafter, same session) |
| 2026-08-22 | Same day, second round — a lightweight confirmatory adversarial pass (3 lenses, 2-skeptic verify, 18 agents) on the revised draft found the *replacement* argument for rejecting claim 1 itself invalid: (a) `floor_at_k` has no live TRAIN-side application in any of the five cited owners for GROW-0's finding to leave "untouched" (verified directly against `grow0_scoring.py`'s `run_panel`, and the repo's one real TRAIN-side DSR mechanism, `lab/research_utils/universe_gate.py`, which uses a different function and is dormant under W4); (b) the "real-market non-independence" argument attributed to the blind-channel ADR was a misattribution — its actual L208 text makes a combinatorial claim about data-partition/K substitution, not a serial-dependence claim (re-verified verbatim, and via repo-wide grep for the attributed framing, which returned no hits). Rewrote §1/§2/§3/§4/§5/§6 to reject claim 1 on the narrowest ground that survives both rounds — `K_intrinsic`'s ratified definition plus the dual-panel review's own prior B3 finding — without constructing a third first-principles mechanism argument; added a forbidden move on citation attribution without re-verification. Still `Proposed` — not yet sent to the operator for ratification. | Claude Code (drafter, same session) |
| 2026-08-22 | Same day, third round — a small targeted check (2 lenses, 2-skeptic verify, 13 agents) on the round-2 argument found a **third** citation error: this ADR (in §0's very first draft and unchanged through round 2) attributed "five owners, including the charter" to the dual-panel review's own B3 finding. Read verbatim this round: B3 names only **four** owners (TNEC-1 N-EDGE, EM screen §8, `admission_schema.py`, blind-channel ADR L208) and never mentions the charter or the numeral "five" — the fifth owner and the "five" framing trace to GROW spec v2's own Part B text, which is explicitly unreviewed ("named only; not proposed here"), not to B3's own adversarially-corroborated finding. Corrected §0/§1/§2/§3's citations to attribute exactly four owners to B3 and the charter's inclusion to this ADR's own direct §0 read (independently re-verified: `universe_gate.py` has zero `floor_at_k` references and operates on `best_returns`/IS-selected candidates via `deflated_sharpe`/`expected_max_sharpe` directly). Rewrote §5's citation-discipline bullet, which had falsely claimed "every citation... was re-verified" after round 2 — that claim was itself wrong, since this third error had not yet been caught; withdrawn, not repeated. The ADR's ultimate rejection of claim 1 does not depend on the miscount (the charter's own status was separately, correctly verified all along) — but the misattribution itself was real and is fixed. Given three citation errors in one drafting session, this row's own header note recommends a fourth, independent read before operator ratification rather than assuming this round closed the matter. Still `Proposed`. | Claude Code (drafter, same session) |

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-22-grow0-two-ledger-k-question.md --type adr
python scripts/check_adr_graph.py
```
