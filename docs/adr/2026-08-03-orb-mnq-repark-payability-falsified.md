# ADR 2026-08-03 — ORB-MNQ-1 re-PARKED; the payable-Tradeify-leg target is FALSIFIED on §4 T2

**Status:** `Accepted` — operator rulings in chat 2026-08-03: (1) *"rule T2 fired — Part A bust reading governs"*; (2) disposition = escalate, i.e. re-park + record the payability target FALSIFIED, rather than T2's literal cap-at-k=1; (3) §4 H limb (b) keeps its literal wording.
**Decision date:** 2026-08-03
**Supersedes:** `2026-07-31-orb-mnq-unpark-payability-target.md` in part — its **§2 unpark decision**, its **payable-`Tradeify_Select_100K`-leg target**, and its **§4 trigger table** only. That ADR's §3 evidence, Addendum 2026-07-31b (both operator rulings), Addendum 2026-07-31c (T1 `PASS`), and Addendum 2026-08-02 (T2 measurement) stand as `Accepted` record and are **not** retracted.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (three rulings, chat 2026-08-03) + Claude Code (adjudication mechanics + recorder)
**Related:** [`RESULTS_t2_intraday_bust.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md) (the measurement this rests on) · [`2026-07-13-prop-survivor-scoring-prereg.md`](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) (the frozen protocol both limbs fail) · [`2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) (the lane ADR whose reopen bar governs any future unpark) · [`Q-COMPOSE-1 closure`](../briefs/closures/Q-COMPOSE-1-closure-falsified.md) (book-leg role, independently FALSIFIED and untouched)
**Layer:** research-authorization status. **No locked parameter, allocation, `dd_protection` constant, `core/lifecycle.py` entry, rail, `LEG_MAP`, Pine construct, or K ledger is touched. $0 spend. Nothing armed.**

---

## §0 — Rule 0 reads (production source, verified this session at `0392011`, 2026-08-03)

- [`docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md`](2026-07-31-orb-mnq-unpark-payability-target.md) — anchor `4a0b45c` (2026-08-02). Read in full, §4 table **and** its header clause together, because they prescribe different dispositions. Header verbatim: *"If any trigger below fires, ORB-MNQ-1 returns to `PARKED` by a superseding ADR and the payability target is recorded FALSIFIED."* T2 row Action verbatim: *"k policy capped at k=1; payability target re-scoped by amending ADR."* T1 row Action is *"Halt"*; T4 row Action is *"ORB-MNQ-1 stays unparked at k-policy scope only"*.
- [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md) — anchor `4a0b45c` (2026-08-02). §0 verdict, the three-arm k table, the realized-panel anchor, and the four controls (A/B/G + non-vacuity).
- [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) — anchor `be6dda6` (2026-07-13), **unedited since**. The frozen gate: **bust ≤ 3.0% ∧ P(pass) ≥ 50%**. Both limbs are load-bearing below; the second has not previously been quoted in the ORB thread.
- [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) §1 Req 3 line 26 — anchor `e0bbad8` (2026-07-27). Confirms `K_banked(MNQ) = 2 (D5 1 + ST-EH-1 1) → K_eff 3, floor 0.98 — open but AT the cap`. **This is the independent home of the Addendum-31b Ruling-1 doctrine**, which is why that ruling survives this supersession — verified before choosing the edge scope.
- [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md) — anchor `df13e74` (2026-07-16). Full-window Tradeify DSR **FAIL** at $0.91/side; 2021+ passes all four FRIENDLY firms to 3 ticks. Read because it is the evidence a non-Tradeify re-scope would have rested on (§3 Alternative C).
- [`scripts/check_adr_graph.py`](../../scripts/check_adr_graph.py) A2 + A3 — anchor `0392011`. A2 in-part requires the target stay `Accepted` + carry the reciprocal `Superseded-in-part-by`. **A3 has no age gate**: any `Superseded` ADR must be stub-shaped *and* have an LTM body. That mechanical fact decided the edge scope (§3 Alternative D).

---

## §1 — Context

ORB-MNQ-1 was unparked to active research on 2026-07-31 against a single named target: a *payable* standalone `Tradeify_Select_100K` leg. Its §4 hypothesis H was left deliberately open, and four triggers were frozen. T1 discharged `PASS` the same day. T2 waited on a computational limb — `core/mc/simulation.py::simulate_path` had gained an opt-in `intraday_low=` argument on 2026-07-30 that nothing had ever fed, so every published bust figure in the repo tested the trailing barrier against the **close** rather than the intraday extreme.

On 2026-08-02 that limb was fed for the first time. The measurement returned a result that T2's own wording could not adjudicate: its threshold — *"k=2 single-day bust exceeds the frozen 3.0% ceiling"* — welds a **single-day dollar** quantity to a **Monte-Carlo rate** ceiling, and the two readings disagree. The 08-02 addendum recorded the measurement and explicitly declined to choose, on the grounds that reading a §4 trigger in whichever direction the data now favours is the same error class §5 forbids. The disposition was left owed to the operator.

**Decision driver (one sentence):** the operator ruled on 2026-08-03 that the Part A bust reading governs, which fires T2 — and because T2's own prescribed remedy is measurably inert, executing it literally would leave the ADR authorizing research toward a target no admissible configuration can reach.

---

## §2 — Decision

**ORB-MNQ-1 returns to `PARKED`. The payable-`Tradeify_Select_100K`-leg target is recorded FALSIFIED.**

**Effective:** immediately upon acceptance.
**Scope:** research-authorization status of Candidate B (ORB-MNQ) only, at the Tradeify target only.

### The three rulings this records

1. **T2 FIRED, on the Part A bust reading.** Of T2's two available readings, the Part A Monte-Carlo bust rate governs; the literal single-day reading does not.
2. **Disposition escalates past T2's own Action column.** T2 prescribes *"k policy capped at k=1; payability target re-scoped by amending ADR."* Capping at k=1 yields **67.67%** bust against a **3.0%** ceiling — 23× over — and one contract is the smallest integer expression. The remedy is inert, so the §4 header disposition applies instead: re-park, record FALSIFIED, by a superseding ADR.
3. **§4 H limb (b) keeps its literal wording.** *"Positive single-day headroom against the $3,000 trail under intraday-honest bust accounting"* remains a single-day test and remains **SATISFIED** at $1,432 (k=2). It is **not** retrofitted to mean account survival.

### What this decision does **not** do

| Unchanged | Status after this ADR |
|---|---|
| Frozen construct (parameter axis) | **LOCKED**, per the 2026-07-16 pre-reg §2/§5. Untouched. |
| Lifecycle standing | `CANDIDATE @ 1.00×`, unchanged. **No `core/lifecycle.py` write.** Parking is operational, not a lifecycle demotion. |
| `K_banked(MNQ) = 2`; one Cap seat, unspent | Unchanged. This ADR spends no K and opens no manifest. |
| Addendum 2026-07-31b Ruling 1 (open manifests do not bank K) | **Stands.** Independent home is `strategy_harvest.md` §1 Req 3 (§0). |
| Addendum 2026-07-31b Ruling 2 (sibling routed to the K=0 fade program) | **Stands and is still live.** The fade program remains ACTIVE with its own two owed rulings. |
| T1 `PASS`, the 16:00 clock, D5 | **Stand.** The 15:30 exit stays barred (reaffirmed 2026-08-02 by the eodadv closure). |
| Book-leg role | Still FALSIFIED by Q-COMPOSE-1, independently. Not reopened, not re-closed. |
| Candidate A (MYM ORC) | Still CLOSED. R5/P2 still FALSIFIED. |
| Prop-portfolio program §4 falsifier, hard date **2026-11-08** | **Undischarged and unaffected.** A different falsifier from the 07-31 ADR's T3 — do not conflate. |
| ORB at any non-Tradeify venue | **Not authorized and not falsified** — see §3 Alternative C and §4 R3. |

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **A — Execute T2 literally: cap k=1, stay unparked, re-scope by amending addendum** | Offered to the operator and declined. The remedy is inert: k=1 is **67.67%** bust, 23× the ceiling, and there is no smaller integer than one contract. An ADR left authorizing research toward an unreachable target is worse than one that records the target dead. |
| **B — Hold T2 unfired on the literal single-day reading** | Available on the wording (0 days reach the trail at any k; $1,432 headroom at k=2) and rejected by ruling 1. Taking it would have meant a leg that busts 77% of simulated paths and dies in March 2020 on the realized panel passing its own falsifier on a technicality. |
| **C — Cap k=1 and re-scope the target to a non-Tradeify firm** | Offered to the operator and declined. Stage-7 shows 2021+ passing all four FRIENDLY firms to 3 ticks, so the evidence existed — but re-pointing a target mid-ADR to the venue that survives is target-shopping after seeing the data, the same error class §5 forbids. **This ADR therefore falsifies the Tradeify target only**; it does not falsify ORB elsewhere, and does not license a move there without a fresh GO (§4 R3). |
| **D — Full supersede of the 07-31 ADR rather than in-part** | Mechanically wrong here. A3 has **no age gate**: `Superseded` forces the body to LTM as a ≤40-line stub, which would bury the T1/T2 measurement record five days before the 08-08 checkpoint and take Addendum-31b's still-live fade-program routing cold with it. In-part is also the truthful scope — the decision is reversed, the measurements are not retracted. |
| **E — Read the §4 header as governing and skip the analysis** | The header says *any* trigger firing means re-park + FALSIFIED, which would have produced this same outcome by a shorter route. Rejected as reasoning: T1's Action is *"Halt"* and T4's is *"stays unparked"*, so three of four rows contradict the header. It is a generalization written from T3's shape, not a governing clause. The escalation had to be **ruled**, not read off. |
| **F — Status quo (leave the disposition owed)** | The 08-02 addendum was right to leave it owed for one operator pass; it is now taken. Leaving it longer carries a live ADR whose §2 authorizes research the evidence has closed. |

---

## §4 — Falsifier (revert trigger for **this** ADR)

**H′ (binary):** *no configuration of the frozen ORB construct at k ∈ {1,2,3} produces a `Tradeify_Select_100K` account that clears the frozen survivor-scoring gate (bust ≤ 3.0% ∧ P(pass) ≥ 50%) under intraday-honest bust accounting.*

Measured, at the corrected eval geometry, 10,000 sims/seed × 3 seeds:

| k | bust (intraday-honest) | vs 3.0% ceiling | P(pass) | vs 50% floor |
|---:|---:|---:|---:|---:|
| 1 | **67.67%** | 23× over | **32.33%** | FAIL |
| 2 | **77.01%** | 26× over | **22.99%** | FAIL |
| 3 | **80.18%** | 27× over | **19.82%** | FAIL |

**Both** pre-registered limbs fail at **every** admissible k — not only the bust limb T2 named. Independent of the bootstrap, a `Tradeify_Select_100K` eval walked over the *realized* panel busts in **March 2020** at every k (day 226/221/217 of 1,878, both clocks, same day); realized max DD is **−$6,527 at k=1**, 2.18× the $3,000 trail, against +$17,780 net.

| # | Trigger | Threshold | Action |
|---|---|---|---|
| R1 | The measurement this ADR rests on fails to reproduce | `run_t2_intraday_bust.py` returns k=1/k=2 bust outside **±1.0pp** of 67.67%/77.01%, **or** any of Controls A/B/G breaks | **Halt.** This ADR's basis is void; re-open the disposition under a superseding ADR before any other action |
| R2 | Tradeify venue geometry materially loosens at the $100K band | A tier change (static DD, larger trail, or a documented trail mechanism other than the $3,000 intraday-enforced one) under which k=1 clears **both** frozen limbs on the unedited survivor-scoring protocol | Fresh operator GO + superseding ADR required to unpark. **Not automatic** |
| R3 | A non-Tradeify target is proposed | Any proposal to run this construct at another firm | **Not authorized by this ADR.** Requires the 07-24 addendum's standing bar (fresh operator GO + pre-registration) **and** a survivor-scoring pass at that firm's geometry **before** unparking — not after |

**Revert action:** author a superseding ADR; never silently edit this ADR's decision text.
**Trigger check schedule:** R1 on any re-run of the harness; R2 on any Tradeify rule-pin re-verification; R3 on proposal.

**Explicitly not a trigger:** the prop-portfolio program's own §4 falsifier at **2026-11-08**. It is undischarged, unaffected, and belongs to [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md).

---

## §5 — Forbidden moves (under this ADR)

- **Retrofitting H limb (b) to mean account survival.** Genuinely tempting, because it would make the 07-31 ADR's own falsifier deliver this verdict cleanly instead of leaving the defect in §6 on the record. Ruled out by operator ruling 3 and by Known Trap #12 — tightening a falsifier after seeing the data is the mirror image of loosening it, and 2026-07-31c already declined exactly this move with RF < 1.
- **Reading this ADR as falsifying ORB-MNQ as a mechanism.** It falsifies **one deployment target at one firm**. The construct's edge (meanR +0.0626, n=1,846), its cost-law PASS, and its Stage-7 result at other firms are untouched. Recording it in `docs/rejected_candidates.md` as a rejected *mechanism family* would be over-recording; the entry made there is scoped to the target.
- **Moving the target to whichever firm survives.** §3 Alternative C was declined by the operator; re-proposing it without the §4 R3 sequence (survivor-scoring pass *before* unpark) is target-shopping after seeing the data.
- **Treating the re-park as a lifecycle demotion.** `CANDIDATE @ 1.00×` is unchanged and no `core/lifecycle.py` write occurs. Parking is operational standing; conflating the two axes is the exact error the 2026-07-10 lifecycle ADR exists to prevent.
- **Spending the MNQ Cap seat under cover of this ADR.** `K_banked(MNQ) = 2` with one `K_intrinsic=1` seat left, and Req 3 has no recovery route. Spending it is an operator decision, not an author's.
- **Quoting the EOD bust arm (74.00% at k=2) as the current figure.** Superseded by the intraday-honest 77.01%. Equally: neither arm's `p99 DD` is intraday-honest — `peak` stays EOD-denominated in both by design.
- **Loosening any §4 trigger above without a superseding ADR** — Known Trap #12.

---

## §6 — Consequences

**A falsifier-construction defect, recorded rather than repaired retroactively.**

This is the load-bearing methodological finding and it is stated plainly because the alternative is to hide it. The 07-31 ADR's H reads: *there exists an admissible configuration … simultaneously (a) payable and (b) survivable.* Under the rulings recorded here:

- **Limb (b) is SATISFIED** — $1,432 single-day headroom at k=2, on its own literal wording (ruling 3).
- **Limb (a) has no numeric threshold in §4 at all**, and measures 17.8%–40.6% payable days depending on k and window. It cannot deliver a FALSIFIED on its own terms either.
- **The target dies anyway**, on Part A bust and P(pass) — criteria H's wording never contained.

So H's two limbs, read literally, both survive, and the thing they were written to test is dead. The falsifier was constructed to interrogate **single-day headroom and payable-day cadence** and never bound **account-level survival**, which is what actually decides fundability. This is a near-relative of the 2026-07-31 fade-program finding (*"the screen interrogates the GEOMETRY and never the EDGE"*) and of the standing `lesson_gate_reachability_preregistration` pattern (bundled clauses in mismatched units).

It is recorded here as **candidate-status**, not promoted to `methodology_lessons.md`: per the lessons threshold it lacks a clean dollar anchor or a third firing across separate windows. If a third instance appears, this is the second and the promotion should happen then.

**Positive:**
- The disposition is taken on measured numbers with four controls behind them, not on an intention or a deadline.
- ORB comes **off the 2026-08-08 checkpoint slate** as a must-decide — its T3 row is moot. That frees gate time for the undischarged prop-portfolio §4 work.
- The `intraday_low=` limb is now exercised, controlled, and reusable. Every future bust figure in this repo can be run intraday-honest.
- Scope is preserved honestly: one target at one firm dies, the mechanism and the other-venue evidence do not.

**Negative (real cost):**
- Three days of research attention (07-31 → 08-03) spent reaching a FALSIFIED, while the prop-portfolio §4 falsifier stays undischarged against a 2026-11-08 hard date.
- The reconstruction lane now has **no** active candidate: Candidate A CLOSED, Candidate B PARKED with its target falsified.
- A published falsifier is left on the record whose limbs do not deliver its own verdict. That is the honest state, but it is a defect, not a feature.

**Risks:**
- **Under-recording.** A reader may take "PARKED" as "shelved pending capacity" rather than "target measured dead." Mitigation: §2's decision line and the `rejected_candidates.md` entry both say FALSIFIED explicitly.
- **Over-recording.** A reader may take this as ORB being dead everywhere. Mitigation: §5 bullet 2 and §4 R3.

**Downstream artifacts updated (see §7):**
- [`2026-07-31-orb-mnq-unpark-payability-target.md`](2026-07-31-orb-mnq-unpark-payability-target.md) — reciprocal `Superseded-in-part-by` + change-history row. **Decision text untouched.**
- [`CLAUDE.md`](../../CLAUDE.md) §Live-execution posture — the ORB pointer line. One line, never a retelling.
- [`STATE.md`](../../STATE.md) — pointer-log entry.
- [`RESULTS_t2_intraday_bust.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md) — disposition banner (its §0 says the call is owed; it no longer is).
- [`docs/rejected_candidates.md`](../rejected_candidates.md) — target-scoped entry + re-proposal bar.
- [`docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md`](../briefs/2026-07-17-0808-packet-delta-and-sequence.md) — three rows carrying "disposition owed / record-only".
- [`docs/adr/INDEX.md`](INDEX.md) — regenerate.
- [`docs/SESSIONS.md`](../SESSIONS.md) — session entry.

---

## §7 — Implementation plan

- **Phase 0** — ✅ §0 reads verified at `0392011` before authoring; T2 measurement and its controls read at `4a0b45c`.
- **Phase 1** — reciprocal edge on the 07-31 ADR (`Superseded-in-part-by` + change-history row); no decision-text edit.
- **Phase 2** — downstream sync per §6.
- **Phase 3** — `python scripts/check_adr_graph.py` exit 0; `make validate` clean.

---

## §10 — Audit hooks (runnable)

```bash
# The in-part edge is reciprocal and correctly scoped (A2)
python scripts/check_adr_graph.py
# Expected: exit 0

# The 07-31 ADR's decision text was NOT edited — only its header + change history
git diff main -- docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md
# Expected: hunks touch only the Superseded-in-part-by line and the change-history table

# The measurement this ADR rests on still reproduces (R1)
.venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_t2_intraday_bust.py
# Expected: k=1 bust 67.67%, k=2 77.01%, k=3 80.18% (±1.0pp); Controls A/B/G pass

# Scope discipline — this ADR must NOT read as a mechanism rejection.
# Assert the HTML-comment form, not the bare phrase: the entry's own prose says it carries
# "no `concept-intake-entry` comment", so a word-match returns a false positive (Trap M-AHF).
rg -n '<!-- concept-intake-entry[^>]*instrument="MNQ"[^>]*opening-range' docs/rejected_candidates.md
# Expected: NO match — registering opening-range-breakout x MNQ in the dedup machinery would
# return REJECTED for the mechanism family, which is not what was decided.

# The target-scoped entry exists and is labelled as a target rejection
rg -n "DEPLOYMENT-TARGET rejection" docs/rejected_candidates.md
# Expected: exactly one heading, for the Tradeify_Select_100K target

# The construct is still preserved where the corpus already says so (must stay consistent)
rg -n "Explicitly preserved \(NOT rejected\).*ORB-MNQ-1" docs/rejected_candidates.md
# Expected: the 2026-07-21 and 2026-08-02 raised-bar preservations still stand — this ADR
# falsifies a target, so those lines must NOT have been edited

# Lifecycle untouched (parking is not demotion). State file is core/lifecycle_state.json
# (STATE_FILE = Path(__file__).parent / "lifecycle_state.json", core/lifecycle.py:55) and is
# local-only/untracked; per its own docstring an ABSENT file == all-1.0x default. So the
# property to assert is "no ORB entry anywhere in the lifecycle surface", which holds whether
# or not the file exists — not "the file lacks a key", which would silently pass on absence.
test -f core/lifecycle_state.json && rg -ci "orb" core/lifecycle_state.json || echo "state file absent => all-1.00x default, no ORB write possible"
rg -ci "orb" core/lifecycle.py
# Expected: 0 from lifecycle.py, and either 0 or the absent-file message — never a nonzero count

# The K ledger did not move
rg -n "MNQ 2|K_banked" docs/methodology/strategy_harvest.md
# Expected: MNQ 2 (D5 1 + ST-EH-1 1), one K_intrinsic=1 seat, unspent
```

---

## Addendum 2026-08-30 — §4 R1 dormancy (Rule 11; Great Prune class-2)

**Does not amend §4** (threshold text, ±1.0pp band, Controls A/B/G, or Halt action
unchanged). **Does not amend §5** (forbidden-moves list untouched — including
"Loosening any §4 trigger above without a superseding ADR"). **Does not amend §2**
(PARKED + Tradeify-target FALSIFIED stands). This is a **reachability / dormancy
record**, not a threshold change and not a re-disposition. **$0 / K=0.**

Per operational-rules [Rule 11](../operational_rules.md#11-retirement-events-back-propagate-to-standing-falsifiers)
(retirement events back-propagate to standing falsifiers): a falsifier whose input
can no longer accrue is not "in force" regardless of unchanged threshold text.
`check_falsifier_reachability.py --stats` reports this ADR's R1 as the live WARN
(`missing: run_t2_intraday_bust.py`). Rule 11 requires a dated re-arm addendum —
never an in-place edit of the falsifier.

**(a) Limb + retiring event.** Limb **R1** (§4) — *"The measurement this ADR rests
on fails to reproduce"* — depends on `run_t2_intraday_bust.py`. Retiring event: the
2026-08-08 Great Prune class-2 policy
([`2026-08-08-great-prune.md`](2026-08-08-great-prune.md); commit `283d1de`
`prune(class 2): drop closed-campaign harnesses/panels from lab/analysis; keep
RESULTS*/PREREG*/CARD`) deleted
`lab/analysis/orb/orb_mnq_2026-07/run_t2_intraday_bust.py`. This ADR's own §2
decision closed the ORB-MNQ-1 Tradeify-leg campaign that harness measured, which
made the harness eligible for the same prune — retention policy working as designed,
not data loss.

**(b) Why the input can no longer accrue.** The script does not exist at HEAD. It is
retrievable only via
`git show pre-prune-2026-08-08:lab/analysis/orb/orb_mnq_2026-07/run_t2_intraday_bust.py`
(or equivalent history lookup). Until retrieved, R1 cannot be exercised; a reader of
§4 who treats R1 as live coverage is reading coverage that does not exist.

**(c) Re-arm condition.** R1 re-arms the moment the harness is retrieved from that
pre-prune tag (one-command `git show` — no rebuild) and re-run. The ±1.0pp threshold
on k=1/k=2 bust (67.67%/77.01%) and the Controls A/B/G requirement are **unchanged**
by this addendum. This is a dormancy record, not a loosened trigger. §4's table text
is not edited; §5 already forbids loosening any §4 trigger without a superseding ADR.

**(d) Surviving limbs.** Spot-checked against §4:

| Limb | Depends on `run_t2_intraday_bust.py`? | Status after this addendum |
|---|---|---|
| **R2** — Tradeify venue geometry materially loosens at the $100K band | **No** — fires on a tier/trail/mechanism change under which k=1 clears both frozen survivor-scoring limbs | **Unaffected; still in force** |
| **R3** — A non-Tradeify target is proposed | **No** — fires on any proposal to run this construct at another firm; requires the 07-24 standing bar + survivor-scoring pass before unpark | **Unaffected; still in force** |

R2 and R3 continue to cover the decision's live edges (venue-geometry reopen;
other-venue re-proposal). R1's reproduction gate is dormant until re-armed per (c);
the FALSIFIED disposition and PARKED status do not depend on R1 firing continuously.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-03 | Initial authoring. Three operator rulings recorded (T2 fired on the Part A reading; disposition escalated past T2's inert remedy; H limb (b) keeps its literal wording). In-part supersession of the 07-31 ADR's §2/§4. Falsifier-construction defect recorded candidate-status | Joshua (rulings) + Claude Code (recorder) |
| 2026-08-30 | Addendum: §4 R1 flagged DORMANT under Rule 11 after Great Prune class-2 removed `run_t2_intraday_bust.py`; re-arms on `git show` retrieval + re-run; ±1.0pp / Controls A/B/G unchanged; R2+R3 unaffected. §4/§5 text not edited | Joshua (PR directive) + Cursor Cloud Agent |
