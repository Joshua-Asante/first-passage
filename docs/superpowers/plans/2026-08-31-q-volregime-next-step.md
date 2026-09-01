# Q-VOLREGIME-1 next step — L3 completion and bar-native L5 design

> **For agentic workers:** REQUIRED SUB-SKILL: use
> `superpowers:executing-plans`. Steps use checkbox (`- [ ]`) syntax. Execute one
> packet at a time and stop at every named gate.
>
> **Status:** Packet A COMPLETE (both instruments PASS frozen L3, PR #240,
> merged). **Packet B B1–B4 drafted 2026-08-31** — the day-level
> joint-surrogation adaptation is retired for this construct; replaced with a
> bar-native nested forward-prediction design at
> [`volregime_l5_design_2026-08-31/DESIGN.md`](../../../lab/analysis/_inbox/volregime_l5_design_2026-08-31/DESIGN.md).
> No real L5 statistic was inspected before drafting. **B5 (adversarial
> review) not yet run.** Packets C-D were not started.
>
> **Queue:** serves STATE queue `#1` (mechanism supply), but queue placement is
> not a phase GO. It does not block independent queue `#2` (B7-REFIRE/M1).

**Goal:** finish the cheap, already-frozen chronological-halves presence limb
(L3) for MNQ and MYM, then—only for instruments that pass—replace the blocked
day-level-surrogate adaptation with a bar-native, estimation-aware L5 design.
The new design must prove null size, useful planted-effect power, and absolute
model adequacy before it may score the real attribution statistic once.

**Terminal outcomes:** each instrument ends this packet either (a) stopped under
the existing frozen verdict map after an L3 failure, (b) left
`AMBIGUOUS-PARKED` because no valid L5 design clears the pilot, or (c) handed to
a separately authorized, K-declared one-shot L5 execution. This plan does not
authorize an entry, exit, sizing, Pine, allocation, `dd_protection`, rail, or
live-account change.

---

## 1. Why this is the next step

The surviving evidence is coherent but incomplete:

- Both instruments cleared the within-own-range-stratum null-calibration
  precondition (`p=0.00025` in each stratum).
- L4 passes independently on both instruments: 7/7 qualifying years positive,
  versus 5 required. Panel length therefore no longer forces
  `AMBIGUOUS-HOLD`.
- L3 now passes independently on both instruments. Chronological-halves
  stability is complete; L5 attribution remains the only open limb.
- The parent brief's planned L5 route was to adapt `Q-RANGEXFER-1`'s day-level
  joint-surrogation design. That parent did not clear either absolute model
  adequacy or estimation-aware size control. Its false-positive rate inflated
  materially when parameters were re-estimated as they must be on real data.

Therefore the falsify-first order is: **score L3 now; do not spend design effort
on an instrument that fails it; amend the L5 route only after a survivor
exists.** Do not certify either finding from the current precondition and L4
results alone.

---

## 2. Governing decisions (frozen for this plan)

| ID | Decision | Consequence |
|---|---|---|
| D1 | MNQ and MYM are scored independently. | No pooling, averaging, or cross-instrument inheritance of verdicts. |
| D2 | L3 uses the existing frozen criterion: positive lift in both chronological halves. | Confidence intervals are disclosed diagnostics; do not invent a new L3 threshold after seeing results. |
| D3 | The split rule is frozen before half-results are printed. | Use a chronological split of the scored observations, with no date optimization. Record the exact boundary and counts. |
| D4 | An L3 failure stops that instrument before L5 design/execution. | Apply the parent brief's existing verdict map; do not rescue it with alternate thresholds or subperiods. |
| D5 | A passing L3 authorizes only an L5 design amendment proposal. | No real L5 statistic runs until pilot validation, adversarial review, K declaration, and a fresh execution GO. |
| D6 | The replacement L5 design tests incremental forward information, not a causal mechanism. | A pass promotes at most a conditioner-role class finding; it does not license a strategy construct. |
| D7 | Every null replicate re-runs the complete estimation procedure. | Known-parameter-only validation is forbidden; it repeats the defect that invalidated the day-level route. |
| D8 | A pilot failure is a designed outcome. | Leave the mechanism `AMBIGUOUS-PARKED`; do not tune repeatedly against the observed MNQ/MYM result. |

---

## 3. Files and ownership

**Read before every packet (Rule 0; do not trust this plan's cached state):**

- `docs/briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md`
- `docs/briefs/pre-registration/Q-VOLREGIME-1-verdict-preregistration.md`
- `lab/analysis/_inbox/volregime_byyear_l4_2026-08-31/RESULTS.md`
- `ops/instruments/MECHANISMS.md`
- `ops/instruments/MNQ.md`
- `ops/instruments/MYM.md`
- the two candidate-3 scored-frame builders and their result JSON files
- `core/data/bar_data/SHA256SUMS`

**Expected new analysis home (create only after GO):**

- `lab/analysis/_inbox/volregime_l3_2026-08-31/`
- `lab/analysis/_inbox/volregime_l5_design_2026-08-31/`

If execution occurs on a later date, use that execution date in the directory
name; do not backdate it to this plan's drafting date.

**Owner updates after a scored result:** parent Q brief amendment log, the
relevant analysis `RESULTS.md`, `lab/CATALOG.md` through its generator, and only
the instrument/mechanism ledger surfaces whose recorded status actually
changes. Do not hand-edit generated profiles.

---

## Packet A — Complete L3 cheaply

**Authorization required:** operator GO on Packet A. This packet is a presence
diagnostic on the already-scored, hash-pinned panels; record the applicable K
treatment before execution rather than assuming it.

- [x] **A1 — Re-read owners and verify the input bytes.** **HARD STOP
  2026-08-31:** both required CSVs are absent; recorded in the Packet-A results.

```bash
sha256sum -c core/data/bar_data/SHA256SUMS --ignore-missing
python lab/analysis/_inbox/volregime_byyear_l4_2026-08-31/byyear_l4.py
```

Expected: both available MNQ/MYM panels match their tracked hashes; the L4
reproduction prints `n_valid=7 n_pass=7 required=5 L4=PASS` for each. A mismatch
is a hard stop—do not compute L3 on different bytes under the existing freeze.

- [x] **A2 — Write the L3 test before printing results.** Scorer and three
  boundary/failure tests landed; no real-panel result was available to print.

Create a deterministic script that reuses the frozen scored-frame construction
and, independently by instrument:

1. retains only valid scored pairs;
2. orders them chronologically;
3. fixes one midpoint split before calculating lift;
4. reports the exact timestamp boundary, observation counts, conditional counts,
   and date spans;
5. in each half, calculates volume-conditioned lift separately within
   `own_range_not_elevated` and `own_range_elevated`;
6. declares the half statistic as the minimum of those two stratum lifts;
7. scores L3 PASS only when both half statistics are strictly positive.

Do not search alternate split dates. Do not pool the instruments. Add focused
tests for boundary assignment, invalid-row exclusion, and a fixture with one
negative stratum that must fail the half.

- [x] **A3 — Freeze code and expected schema, then execute once.**

The result artifact must include the script hash, panel hashes, split boundary,
all four per-instrument stratum lifts, both half minima, counts, and the frozen
PASS/FAIL calculation. Confidence intervals may be reported but do not gate L3.

- [x] **A4 — Apply the stop rule independently.**

| Outcome | Action |
|---|---|
| Both instruments fail L3 | Close both under the existing frozen map; stop this plan. No L5 amendment. |
| One passes, one fails | Close the failing instrument; carry only the survivor into Packet B. |
| Both pass | Carry both independently into Packet B. |

- [x] **A5 — Update owners without overstating the result.**

Record that L3 is complete and whether each instrument passes. A pass means
`presence battery complete, L5 still open`; it is not `RESOLVED`, `CERTIFIED`,
or an authorization to construct a trade.

**Packet-A falsifier:** a repository search must find no newly authored claim
that a passing L3 alone certifies the conditioner.

---

## Packet B — Amend the L5 route

**Entry gate:** at least one instrument passes Packet A. **Authorization
required:** operator acceptance of the amended design route before code is
executed against the real hypothesis.

- [x] **B1 — Amend the parent brief and pre-registration prospectively.** Done
  2026-08-31 — parent brief §7/§11, pre-registration §C. Both preserve the
  hypothesis, per-instrument scoring, L1–L4 results, `alpha=0.05`,
  distinct-WHO disclosure, and the verdict map; only the day-level-surrogate
  instruction was replaced.

Preserve the hypothesis, per-instrument scoring, L1–L4 results, `alpha=0.05`,
distinct-WHO disclosure, and the existing verdict map. Replace only the
unvalidated instruction to adapt the day-level surrogate. Date the amendment
and state explicitly that no real L5 statistic was inspected before it landed.

- [x] **B2 — Freeze a nested forward-prediction comparison.** Done 2026-08-31
  — [`DESIGN.md`](../../../lab/analysis/_inbox/volregime_l5_design_2026-08-31/DESIGN.md)
  §3.

For each surviving instrument, specify the same model family and rolling folds:

**Baseline information set**

- time-of-day slot;
- trigger-bar realized range and own-range-elevated indicator;
- a fixed set of recent range lags;
- prior trading day's realized-range state;
- fixed calendar/session controls justified before execution.

**Augmented information set**

- every baseline term;
- trigger-bar time-of-day-normalized volume state;
- only those volume lags declared before the pilot.

Use strictly past training data for every test fold. Freeze the warm-up period,
fold boundaries, missing-data behavior, learner/hyperparameters, and any
regularization without looking at real augmented-minus-baseline performance.

- [x] **B3 — Freeze the primary statistic and dependence treatment.** Done
  2026-08-31, reworked same date after a second Codex review round —
  [`DESIGN.md`](../../../lab/analysis/_inbox/volregime_l5_design_2026-08-31/DESIGN.md)
  §4.1 (statistic), §4.3 (day-level dependence blocking, carried by the circular-shift
  construction itself rather than a separate section).

Primary: augmented-minus-baseline improvement in a proper out-of-sample loss
(Brier or log loss; elect one before code runs). Companion: the existing minimum
within-own-range-stratum lift. Inference must be blocked at trading-day/session
level; treating M15 bars as IID is forbidden.

- [x] **B4 — Freeze the attribution null.** Done 2026-08-31, reworked same date
  after a second Codex review round found the first draft's null did not actually
  preserve the confound it claimed to —
  [`DESIGN.md`](../../../lab/analysis/_inbox/volregime_l5_design_2026-08-31/DESIGN.md)
  §4.2–§4.6, §5.

Fit the predictable component of trigger-bar volume using training data only.
Randomize the residual component in blocks within predeclared time-of-day and
range-state cells, preserving the predictable component and declared controls
while breaking candidate incremental information. The full residualization,
model fit, and score process is repeated inside every replicate.

> **Superseded 2026-08-31 (Codex fourth-pass review, Finding 8) — this paragraph is
> this task's original prescriptive instruction, predating any implementation
> round, and was never updated as the design evolved.** The actually-frozen
> construction is a day-level, regime-and-slot-mask-stratified circular shift of
> whole residual vectors (reusing `circular_shift_null_p`), drawn once globally
> per replicate and applied consistently across every fold — not a bar-level
> block permutation within `(time-of-day, range-state)` cells. Following this
> paragraph literally would rebuild the superseded, defective null. Read
> [`DESIGN.md`](../../../lab/analysis/_inbox/volregime_l5_design_2026-08-31/DESIGN.md)
> §4.2–§4.4 directly; this checklist item is a task description, not the
> controlling spec.

The design must separately report the distinct-WHO check after adding prior-day
range state. Whether the lift survives that addition types attribution but does
not silently change the frozen verdict criterion.

- [ ] **B5 — Adversarial design review before pilot execution.** Design's own
  §6 pre-answers all six questions below (self-review, not a substitute).
  Routed through this design's own PR review (Codex) rather than an
  in-session panel — operator decision, 2026-08-31; not yet run —
  [`DESIGN.md`](../../../lab/analysis/_inbox/volregime_l5_design_2026-08-31/DESIGN.md)
  §6–§7.

Required review questions:

1. Does the null preserve same-bar volume/range association and intraday
   seasonality closely enough for the claim being tested?
2. Can information cross a rolling-fold boundary through normalization,
   residualization, or hyperparameter fitting?
3. Is every fitted component re-estimated in each replicate?
4. Is the primary statistic declared once, with no best-of-metrics selection?
5. Does daily-state conditioning at bar granularity introduce a collider or
   future-information path?
6. Are session blocks long enough for the dependence visible in both panels?

Any load-bearing review finding returns to B1–B4 and requires a dated amendment
before the pilot. Review is not permission to inspect the real L5 statistic.

---

## Packet C — Validate the machinery, not the hypothesis

**Entry gate:** Packet B design committed and reviewed. **Authorization
required:** pilot GO. Do not run the observed L5 statistic in this packet.

- [ ] **C1 — Freeze pilot acceptance bands before simulation.**

Declare, before results:

- replicate count and seeds;
- empirical Type-I acceptance band around nominal 5%;
- minimum useful power at one or more planted effects no larger than the
  observed stage-1 lift;
- absolute calibration/adequacy diagnostics and their pass rules;
- one bounded escalation, if any, and the terminal failure disposition.

- [ ] **C2 — Null-size study with re-estimation.**

Generate null panels preserving intraday seasonality, contemporaneous
volume/range dependence, volatility clustering, serial dependence, session
boundaries, and the observed missingness pattern. Re-run the complete estimation
pipeline in every replicate. Known-parameter-only results may be diagnostic but
never satisfy this gate.

- [ ] **C3 — Planted-effect power study.**

Plant declared incremental effects without changing the nuisance structure and
measure rejection probability. A method with controlled size but no useful
power at effects below the observed lifts does not clear.

- [ ] **C4 — Absolute model-adequacy checks.**

Report calibration/residual behavior by time-of-day, own-range stratum,
calendar year, chronological half, and instrument. Being relatively best among
candidate models is insufficient; the design must pass its absolute criteria.

- [ ] **C5 — Apply the joint pilot gate.**

| Pilot result | Disposition |
|---|---|
| Size, power, and adequacy all pass | Produce a frozen L5 execution packet; proceed no further without Packet D GO and K declaration. |
| Any gate fails after the bounded escalation | Stop. Leave surviving mechanisms `AMBIGUOUS-PARKED`; record a design failure, not a negative empirical verdict on volume. |

No repeated tuning against the observed MNQ/MYM L5 result is allowed because
that result must still be unseen.

---

## Packet D — One-shot L5 execution and closure

**Entry gate:** Packet C passes. **Authorization required:** explicit operator
GO plus K declaration under the standing program convention.

- [ ] **D1 — Pin code, inputs, environment, K, and one-shot command.**
- [ ] **D2 — Run diagnostics first; hard-stop before headline p-values if a frozen diagnostic fails.**
- [ ] **D3 — Score MNQ and MYM separately using the identical reviewed design.**
- [ ] **D4 — Publish both one-sided bounds, full presence battery, halves, annual table, and distinct-WHO result.**
- [ ] **D5 — Apply the existing verdict map mechanically and file one closure naming each instrument's verdict.**
- [ ] **D6 — Update mechanism/instrument owners and regenerate derived indexes.**

`RESOLVED` promotes only a certified conditioner-role finding. `FALSIFIED`
stops that instrument under the existing re-proposal bar. Neither outcome
licenses an entry, exit, sizing rule, strategy, or live deployment.

---

## 4. Verification checklist

Run the narrow checks after each packet and the repo gates before merge:

```bash
python scripts/check_brief.py docs/briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md
python scripts/check_spec_provenance.py
python scripts/check_instrument_ledger_coverage.py
python scripts/check_status_consistency.py
python scripts/check_md_relative_links.py
python scripts/check_path_liveness.py
make validate
git diff --check
```

If `check_brief.py`'s supported CLI differs at execution time, read
`python scripts/check_brief.py --help` and record the exact supported invocation;
do not silently omit the check.

---

## 5. Explicit non-goals

- No reuse of the failed day-level surrogate merely because it already exists.
- No pooled MNQ+MYM statistic or replication-as-substitute-for-attribution.
- No alternate volume quantiles, trailing windows, split dates, model families,
  or outcome definitions selected after observing L3/L5.
- No revival of the corrected/falsified overnight-range-conditioned ORB-MNQ
  payability path.
- No changes to Pine, `core/` risk constants, allocations, `dd_protection`, rail,
  or live-account posture.
- No claim that a magnitude conditioner supplies direction or a tradable payoff
  without a separate, fully gated construct.

---

## 6. Handoff summary

The next executable action is **Packet A only**: reproduce the pinned scored
frames and compute the missing chronological-halves L3 result once. Everything
after Packet A is conditional. If an instrument survives, the next action is an
operator-reviewed amendment and validation pilot—not immediate L5 execution.
