# ADR — Decompounded full-history re-MC: HOLD locked config; adopt regime-dependence as canonical risk characterization

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-06-07
**Authors:** Joshua + claude.ai (advisor)
**Supersedes:** none (does NOT supersede the 2026-05-23 allocation-refresh-2 lock — that config is HELD)
**Related:** `docs/adr/2026-05-23-allocation-refresh-2.md` (the locked config being characterized) · `docs/methodology/regime_robustness_gate.md` (the gate applied) · Q-DDP-1 (the regime-fragility precedent)
**Layer:** portfolio
**Addendum 2026-06-25 (see end):** clean single-file re-MC re-validates the HOLD (still breaches both gates) but **corrects the breach severity** — the headline was inflated by a Guardian/DJ30 stitch-seam artifact. Clean B_2020 = **98.53% / 1.47% / 5.32%** (not 97.08 / 2.92 / 5.93).
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): reduced the spent §0 Rule-0 reads to a pointer and §10 to its one still-runnable hook; removed the §6 downstream-artifacts list, §7 implementation plan, Verification block, and the 2026-08-03 addendum's §0 table and §10 hooks; condensed the 2026-07-01 addendum and the 2026-06-25 re-run flag; repointed archived-harness paths and the dead design link. §1–§5 (including the §4 trigger field), the 2026-08-03 Decision, forbidden moves and §6 gate are unchanged. Pre-trim text at blob `8ba0605c4d12714e29da98384f08df953788fc47` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).

---

## §0 — Rule 0 reads (production-source verification)

Spent: the 2026-06-07 reads (anchor `4331e65`: `core/portfolio_mc.py`, `core/dd_protection.py`, `core/firm_rules.py`, `tests/test_mc_anchors.py`, `docs/methodology/regime_robustness_gate.md` and the since-archived harness) are in the pre-trim blob (see **Revision**).

---

## §1 — Context

The locked 4-strategy MC anchor (99.83 / 0.17 / 4.37, `docs/adr/2026-05-23-allocation-refresh-2.md`) is built on **compounded** TradingView backtests over a **2022-01 → 2026-05** window. On 2026-06-07 Joshua supplied the full **2020-01 → 2026-06** Pepperstone exports and asked to (a) extend to all available history and (b) remove the compounding effect via a "withdraw every +5%, reset to $200K" (banded-skim) model, which is closer to how a prop account actually sizes.

Re-MC on that corrected basis (decompounding round-trips losslessly; harness reproduces the locked anchor exactly) gives **97.08 / 2.92 / 5.93 — both lock gates breach.** Joshua accepted 2020-26 + decompounding as the canonical basis and that de-risking was warranted. A de-risk sweep found a full-panel frontier (uniform k≈0.55, or DD_SCALE 0.40→0.20). Per the regime-robustness gate (mandatory here — dd_protection-class candidate AND regime distribution materially affects the result), both candidates were gated. **Both FAIL**, decisively on the H1 (2020-2023) half: even half-risk busts 8.89%, brake-strengthen busts 13.50%. The hard regime only clears the gates at **~¼ of locked risk, where median pass-time is 367–591 days** — not a viable challenge.

**Decision driver (one sentence):** the gate proved that *no viable static sizing config (allocation or dd_protection) is regime-robust*, so the de-risk path the reevaluation was heading toward is mis-framed — a decision is needed to record the HOLD and re-characterize the canonical risk rather than relock to a benign-regime-weighted number.

---

## §2 — Decision

**Decision:** HOLD the locked configuration unchanged — allocations (G 0.34% / DJ30 0.70% / A 1.50% / N 0.37%) and dd_protection C2 (1.5% / 0.40×). Adopt the **regime-dependence characterization** as the canonical forward risk picture, replacing the misleadingly-benign single-number framing:

- The locked **99.83 / 0.17 / 4.37** is a 2022-26 **compounded, benign-regime-weighted** average and remains the pinned test reference for that panel.
- The corrected forward risk is **97.08 / 2.92 / 5.93** (decompounded, full-history 2020-26) — both gates breach — and is **strongly regime-split**: H1 (2020-2023, incl. 2022 chop) bust ~9–13% / p99 ~7.5%; H2 (2023-2026 trend) bust ~0% / p99 ~3-4%.
- **No static de-risk is regime-robust** without making the challenge impractical (≥367d median). Both de-risk candidates (k=0.55; DD_SCALE→0.20) are **rejected as regime-fragile**.
- The portfolio's tail risk is **regime-dependent and managed operationally** (size-down / pause challenges in recognized choppy/crisis regimes), not by a constant change.

**Effective:** immediately upon acceptance. **Scope:** the 4-strategy portfolio MC risk characterization and the HOLD on allocations + dd_protection. No `core/` constant changes.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Adopt uniform de-risk **k≈0.55** | Fails the regime-robustness gate (H1 bust **8.89%**, p99 **7.58%**). A benign-regime-weighted safety improvement that does **not** fix the hard regime, at a real pass-time cost (median 26→47d). Retained only as a documented *mitigation* if risk appetite shifts (see §5), never as a regime-robustness claim. |
| Strengthen brake **DD_SCALE 0.40→0.20** | A dd_protection change → its regime gate is *mandatory*, and it fails decisively (H1 bust **13.50%**). |
| Deep de-risk **k≈0.25** | Regime-robust (H1 clears) but median pass-time **367–591 days** → not a viable prop challenge. |
| Regime-adaptive sizing | The only thing that could actually fix the hard regime, but it is a **new strategy mechanism**, out of scope for an allocation/dd_protection decision. Flagged as a future Pre-Q (§4 revert action). |
| Status quo, **no characterization** | Leaves the misleadingly-benign 99.83 single number as the canonical risk picture, which the data shows materially understates live tail risk in a 2022-style regime. Doing nothing is worse than recording the characterization. |

---

## §4 — Falsifier (revert trigger)

> ⚠ **READ FIRST — NEITHER LIMB CAN FIRE TODAY (status as of 2026-08-03).** Thresholds below are
> **unchanged and not re-decided**; what changed is whether they are reachable.
> **Limb 1 — DORMANT** since 2026-07-01 (no live challenge in flight); re-arms automatically when
> live execution resumes. **Limb 2 — SUSPENDED-ORPHANED** since 2026-08-03: its trailing-window call
> is permanently `NOT_EXECUTABLE` because the panel cannot be extended (Pepperstone feed retired
> 2026-08-02, CFD venue closed 2026-06-30). ⇒ **This HOLD currently has no live falsifier.** That is
> a recorded, dated gap, not a claim the HOLD is safe. Discharge path and the "two holes are one
> hole" ruling: [ADR 2026-08-02 §2-D](2026-08-02-pepperstone-feed-retirement.md).
> Full record: §Addendum 2026-08-03 (limb 2) · §Addendum 2026-07-01 (limb 1).

**Revert trigger (binary):** the HOLD is falsified — escalate to de-risk / regime-adaptive investigation — if **either** fires:
1. **Live:** ≥2 challenge failures attributable to drawdown within any rolling 6-month window (i.e. realized bust rate exceeds the locked MC's implied ~0.2%), OR
2. **Regime:** a quarterly regime-check finds the **trailing-6-month** panel resembles H1 — re-run `regime_gate.py` on the trailing 6-month window at the locked config and observe **p99 DD ≥ 5% OR bust ≥ 1%**.

**Revert action:** open a fresh Pre-Q on **regime-adaptive sizing** (the only viable fix per §3); in the interim apply the documented **k≈0.55 mitigation** operationally (reduce all four allocations to 55%).

**Trigger check schedule:** quarterly, **aligned with the existing dd_protection revert-trigger dates** (`CLAUDE.md` Protection section): **2026-08-08**, 2026-11-08, 2027-02-08, 2027-05-08. ~~Run alongside `python lab/analysis/time_to_pass.py --regime-check`~~ — **that companion check (the C2→C0 quarterly revert check) was RETIRED 2026-07-22** ([`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md) §Addendum 2026-07-22, D2). This §4 limb-2 regime-check trigger is a **separate, still-standing** decompound-remc check — it just no longer has that CLI companion; re-run `regime_gate.py` directly per the line above.

---

## §5 — Forbidden moves (under this ADR)

- **Editing the locked anchor numbers / `test_mc_anchors.py` to "match" the decompounded figures.** The config is HELD; the test stays pinned to 99.83/0.17/4.37 (it measures the 2022-26 compounded panel, a still-valid reference). Do NOT change `dd_protection.py` / `firm_rules.py` constants. The characterization lives in docs, not in the pins.
- **Re-proposing k=0.55 or DD_SCALE→0.20 as a relock without NEW evidence.** Both failed the gate; revival requires a new mechanism (e.g. regime-adaptive logic) or a materially different gate result — not a re-run of the same sweep (Known Trap: rejected-alternative revival).
- **Loosening the §4 quarterly trigger without superseding this ADR.** Silent trigger amendment is p-hacking at the methodology layer; supersede with a fresh ADR if the trigger is wrong.
- **Narrowing back to a 2022+ window to make the numbers look benign.** The full 2020-26 window is accepted as canonical (Joshua, 2026-06-07); reverting the window to dodge the finding is the Iran/Hormuz silent-relabel pattern.
- **Attributing the result to the banded-skim withdrawal model.** Banding is immaterial in the risk-normalized MC (banding premium ~0.00pp, measured); the drivers are the **window** (largest) and **decompounding** (secondary).

---

## §6 — Consequences

**Positive:**
- Canonical risk picture now reflects regime-dependence instead of one misleading number; operators size with eyes open.
- Locked config unchanged → no relock churn, no benign-regime pass-time cost, no destabilization of a config that performs excellently in trending regimes.
- The decompounding + regime-gate harness ([archived](https://github.com/Joshua-Asante/first-passage-archive/tree/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/regime/decompound_remc_2026-06-07/); `lab/ARCHIVED.json` key `decompound_remc_2026-06-07`) was reusable for the quarterly §4 trigger, whose schedule was struck 2026-08-03.

**Negative (real cost):**
- The portfolio carries **known, unfixed** tail risk in choppy/crisis regimes; safety now depends partly on operator discretion (harder to enforce than a constant).
- No static safety guarantee in a 2022-style regime; the only structural fix (regime-adaptive sizing) is deferred.

**Risks:**
- A 2022-style regime arrives unrecognized (mitigation: §4 quarterly regime-check + live-outcome monitor).
- Discretion drift — operators ignore regime-awareness under FOMO (mitigation: the §4 live trigger fires on realized failures regardless of discretion).

---

## §10 — Audit hooks (runnable)

The other 2026-06-07 hooks target the retired `CLAUDE.md` and the archived harness (pre-trim blob, see **Revision**). Still runnable:

```bash
# Locked config is genuinely untouched
git -C . diff --stat origin/main -- core/dd_protection.py core/firm_rules.py
# Expected: empty (no constant changes under this ADR)
```

---

## Addendum — 2026-06-25: clean single-file re-MC re-validation (HOLD-ROBUST)

**Trigger.** `Q-INCUMBENT-REGIME-1` (Scope-B per-strategy regime split) found that this
ADR's panels stitched Guardian/DJ30 from 2 TV exports each, and that the clean single-file
2026-06-25 export shows lower standalone DD for exactly those two strategies (DJ30 6.54% vs
stitched 9.03%; Aegis/NAS, single-file in both vintages, matched the old DD exactly) — a
**stitch-seam artifact**. This addendum re-runs the decompound re-MC on the clean vintage.

**Pre-registration:** `docs/ltm/briefs/pre-registration/2026-06-25-decompound-cleanvintage-remc-prereg.md` at the time (lock gates frozen before the run; not in this public tree). **Full results:** [`RESULTS_cleanvintage_2026-06-25.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_cleanvintage_2026-06-25.md) (harness archived, `lab/ARCHIVED.json` key `decompound_remc_2026-06-07`). **Driver:** `remc_cleanvintage.py` (sibling; zero fork of the frozen 2026-06-07 harness).

**Result — the HOLD stands; its breach magnitude was inflated:**

| metric | this ADR (stitched) | clean single-file (2026-06-25) | Δ |
|---|---|---|---|
| B_2020 pass | 97.08% | **98.53%** | +1.45pp |
| B_2020 bust | 2.92% | **1.47%** | −1.45pp |
| B_2020 p99 DD | 5.93% | **5.32%** | −0.61pp |
| **lock gates** | both breach | **both still breach** (1.47% ≥ 1%, 5.32% ≥ 5%) | — |
| locked-config H1 (isolated) | (not run) | bust **13.84%** / p99 7.76% — FAIL | new |
| de-risk C1 k=0.55 H1 | 8.89% bust | 2.81% bust — still FAIL | softer, still fails |
| de-risk C2 DDscale→0.20 H1 | 13.50% bust | 4.94% bust — still FAIL | softer, still fails |

**Disposition: HOLD-ROBUST.** The decision (§2) is unchanged — the locked config still
breaches both gates on clean full-history data, the regime-split is intact (locked H1 bust
13.84%), and no static de-risk is regime-robust. **But the canonical breach figure is
corrected to 98.53% / 1.47% / 5.32%**; this ADR's 97.08 / 2.92 / 5.93 overstated the breach
by ~1.45pp bust / ~0.61pp p99 because of the stitch artifact. The §4 revert triggers and the
HELD config are unaffected.

*(The `h1_check.py` re-run this addendum flagged for the 2026-08-08 regime trigger lapsed with the schedule struck on 2026-08-03; today's HOLD is unchanged.)*

---

## Addendum — 2026-07-01 — §4 limb 1 falsifier dormancy (retirement back-propagation)

Per Rule 11, the 2026-07-01 programme audit recorded **§4 limb 1** ("≥2 challenge failures
attributable to drawdown within any rolling 6-month window") as **DORMANT**: after the 2026-06-30
CFD retirement (`docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`) no live challenge is in
flight, so no failure can accrue. Not a threshold change; §4 is not edited. The limb re-arms
automatically when live execution resumes with a challenge in flight. This addendum's further
statement that limb 2 remained fully in force was **corrected 2026-08-03** (limb 2
SUSPENDED-ORPHANED, below). Full text: `git show 4121e84c95f4990b71962e3b9570c4c3fad88426:docs/adr/2026-06-07-decompound-remc-hold.md`.

---

## Addendum — 2026-08-03 — §4 limb 2 SUSPENDED-ORPHANED (retirement back-propagation)

**Type:** back-propagation under operational-rules **Rule 11** (retirement events back-propagate to
standing falsifiers), placed here under **Rule 14** (corrections land where the claim is read).
**This addendum decides nothing new.** The disposition was already ratified in
[ADR 2026-08-02 §2-D](2026-08-02-pepperstone-feed-retirement.md) (`Accepted`, operator ruling); a
second operator ruling 2026-08-03 (*"all pepperstone has been retired in light of the futures
pivot"*) re-confirmed the retirement independently. What was missing was the record **on the ADR
that owns the falsifier** — a reader of §4 had no way to learn its trigger could not fire.

Rule-0 measurements behind this addendum (2026-08-03; the harness and its inputs are since archived, `lab/ARCHIVED.json` key `decompound_remc_2026-06-07`): prior body `4121e84c95f4990b71962e3b9570c4c3fad88426`.

### The precise failure — reachability, not thresholds

Limb 2 is **not** broken and **not** re-scoped. It is **unreachable**:

1. Its harness and panel survive; it executes and self-refuses correctly.
2. It requires a **trailing-6-month** window ending at the check date. The panel ends 2026-06-02.
3. Extending the panel requires a fresh Pepperstone TV export. The feed is retired and the venue is
   closed, so **no future export can exist**. The gap is permanent and grows one day per day.

⇒ Limb 2 can never again be evaluated on a current trailing window. Every future quarterly date
(2026-11-08, 2027-02-08, 2027-05-08) inherits this. Marking only the 08-08 instance moot would
under-record it — the *schedule* is dead, not one occurrence.

**It was already measuring the wrong exposure** (per §2-D): it scores the **CFD** panel while the
locked config's live expression is MYM/MNQ on CME futures. The retirement removed the last substrate
from a falsifier already aimed at a dormant book. Recording this is not mitigation — a falsifier
that was wrong *and* is now unreachable is worse than one that is merely unreachable.

### Decision

- **§4 limb 2 is `SUSPENDED-ORPHANED`,** effective 2026-08-03. Thresholds (`p99 DD ≥ 5% OR bust ≥ 1%`),
  the revert action (regime-adaptive Pre-Q + interim k≈0.55), and the locked config are
  **byte-unchanged**. Suspension is a statement about *reachability*, never about the bar.
- **The quarterly schedule is struck**, not deferred: 2026-08-08 / 11-08 / 2027-02-08 / 2027-05-08
  carry no limb-2 duty. (2026-08-08's other riders — per-strategy decay review, Call-4 beta-death
  review — are untouched.)
- **The HOLD stands.** Its §2 decision rested on the 2026-06-07 + 2026-06-25 evidence, which is
  unaffected. What lapses is the *compensation* the HOLD offered for consciously accepting regime
  risk. **The HOLD is now unfalsified and, until the successor lands, unfalsifiable.**
- **Discharge = the venue-native regime monitor** (§2-D: the two holes are one hole). It discharges
  limb 2 and the owed forward monitor together; its standing constraints carry unchanged (**not**
  pass-rate-shaped; the both-halves gate is **not** re-run as if the answer were unknown). Design:
  `docs/superpowers/specs/2026-08-02-venue-native-regime-monitor-design.md` (not in this public tree; private archive). Current status: STATE "M-A regime observer / decompound limb-2 successor" ([Q-MONSURF-1 closure](../briefs/closures/Q-MONSURF-1-closure-resolved.md)).
  It is gated on the **first live fill**, not a date — so this gap does not close on a calendar.
- **Limb 1 is unaffected** by this addendum — dormant since 2026-07-01, feed-independent, re-arms on
  live execution. It is a *corroborating* catch-path; it does not substitute for limb 2.

### §5 — Forbidden moves (this addendum)

1. **Do not re-point limb 2 at the CME panels.** Rejected in §2-D as a *rename*: the decompound HOLD
   is a claim about a specific decompounded CFD book. A same-name check on different data is a new
   falsifier wearing an old ADR's authority — it needs its own pre-registration and gate.
2. **Do not treat `NOT_EXECUTABLE` as a pass.** Absence of a breach reading is not a non-breach. The
   downstream 08-08 accept-beta fork is explicitly instructed not to record an absent re-MC as a
   passing one.
3. **Do not lower the coverage requirement** to make the stale panel "good enough." The 126-bday
   trailing window is the trigger's definition; relaxing it to reach a number is the
   threshold-drift degeneration this ADR's own §5 forbids.
4. **Do not close this gap by deleting the falsifier.** Retiring limb 2 outright would leave the HOLD
   with no revert trigger *and* no record that it once had one. Suspension keeps the debt visible.
5. **Do not let the successor's scope quietly grow** past discharging these two obligations.

### §6 — Gate (binary, for the successor)

**RESOLVED** — the venue-native regime monitor is built, pre-registered, and has produced one
verdict on live-fill-era data; §4 is amended to name it as limb 2's replacement, and this suspension
is lifted by an explicit lift artifact (Rule 12).
**FALSIFIED** — the successor is built and its first verdict breaches its inherited thresholds ⇒ the
HOLD is falsified on the merits; open the regime-adaptive-sizing Pre-Q and apply the interim k≈0.55.
**AMBIGUOUS** — no live fill has occurred by the **2026-11-08** review, so the successor remains
unbuilt. Then the gap is **≥3 months old** and must be re-raised in that cycle's programme audit as
a standing-unfalsifiable finding, not rolled forward silently.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-07 | Initial authoring — HOLD + regime characterization; both de-risk candidates rejected by the regime-robustness gate | Joshua + claude.ai |
| 2026-06-25 | Addendum: clean single-file re-MC re-validation. HOLD-ROBUST (both gates still breach); breach severity corrected 2.92/5.93 → 1.47/5.32 (stitch-seam artifact). De-risk candidates still fail H1. | Joshua + Claude Code |
| 2026-07-01 | Addendum: §4 limb 1 (live challenge-failure catch-path) flagged DORMANT under go-dark (CFD retired, no live challenge); re-arms when live execution resumes. Limb 2 (quarterly MC) intact. No config/threshold change. | Joshua + Claude Code (programme audit) |
| 2026-08-03 | Addendum: §4 limb 2 **SUSPENDED-ORPHANED** — panel unextendable after the Pepperstone feed retirement (venue closed), so the trailing-window call is permanently `NOT_EXECUTABLE`; quarterly schedule struck (not deferred). HOLD stands but is now **unfalsifiable** until the venue-native regime monitor discharges it (ADR 2026-08-02 §2-D — "the two holes are one hole"). §4 reader-intercept added; the 07-01 "limb 2 intact" claim corrected in place. No config/threshold/allocation change. | Joshua + Claude Code |
