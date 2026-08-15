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

---

## §0 — Rule 0 reads (production-source verification)

Read **before** authoring, this session (2026-06-07):

- `core/portfolio_mc.py` — anchor `4331e65` (2026-06-06). Read `_simulate_path` (bust/pass semantics, lines 369–426), `build_daily_panel` + `implied_1r` (risk-normalization, 292–354), `_load_all`. The locked anchor reproduces **99.83 / 0.17 / 4.37** in this environment (verified `pytest tests/test_mc_anchors.py -k pepperstone` → 2 passed, this session).
- `core/dd_protection.py` — anchor `4331e65` (2026-06-06). `DD_TRIGGER=0.015`, `DD_SCALE=0.40` (C2, single-tier brake).
- `core/firm_rules.py` — anchor `4331e65` (2026-06-06). FXIFY: `max_dd_pct=5`, `daily_loss_pct=5`, `profit_target_pct=5` → lock gates **bust<1% AND p99 DD<5%**; allocations G 0.34 / DJ30 0.70 / A 1.50 / N 0.37.
- `tests/test_mc_anchors.py` — anchor `92da2c9` (2026-05-25). Pins 99.83/0.17/4.37 on the **2022-01-04 → 2026-05-19** Pepperstone panel (1141 bdays / 227 week-blocks) — i.e. the locked anchor is a **2022+ window**.
- `docs/methodology/regime_robustness_gate.md` — anchor `5b8ff71` (2026-05-23). Gate v1.0: 6-month block bootstrap + half-panel split; floor = the brief's headline criteria; mandatory for dd_protection-class changes and "any brief comparing MC configurations where regime distribution materially affects the result."
- `docs/ltm/briefs/Q-SWAP-3/_run_regime_robustness.py` — implementation pattern mirrored by `lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py`.
- `lab/analysis/regime/decompound_remc_2026-06-07/` (this session) — REG byte-identity verified: the research driver, fed the canonical panels, reproduces `compute_default_config` and the 99.83/0.17/4.37 anchor exactly (18 gates pass, `test_decompound.py`). Decompounding round-trip error = $0.000000.

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
- The decompounding + regime-gate harness (`lab/analysis/regime/decompound_remc_2026-06-07/`) is reusable for the quarterly §4 trigger.

**Negative (real cost):**
- The portfolio carries **known, unfixed** tail risk in choppy/crisis regimes; safety now depends partly on operator discretion (harder to enforce than a constant).
- No static safety guarantee in a 2022-style regime; the only structural fix (regime-adaptive sizing) is deferred.

**Risks:**
- A 2022-style regime arrives unrecognized (mitigation: §4 quarterly regime-check + live-outcome monitor).
- Discretion drift — operators ignore regime-awareness under FOMO (mitigation: the §4 live trigger fires on realized failures regardless of discretion).

**Downstream artifacts that need updating:**
- `CLAUDE.md` MC-anchor section — add a caveat + pointer to this ADR (done this session).
- `lab/analysis/regime/decompound_remc_2026-06-07/RESULTS.md` — final record incl. gate + n=100 (done this session).
- Auto-memory `project_decompound_remc_canonical_shift_2026_06_07.md` — closure state (done this session).

---

## §7 — Implementation plan

Policy + risk-characterization — **no mechanical `core/` edits** (the decision is HOLD).

- **Phase 0** — §0 reads current (verified this session; anchor `4331e65`).
- **Phase 1** — add caveat + ADR pointer to `CLAUDE.md` MC-anchor section.
- **Phase 2** — finalize `RESULTS.md` with the n=100 bootstrap numbers; update auto-memory to closure.
- **Phase 3** — verification block executes; status `Accepted`.

---

## §10 — Audit hooks (runnable)

```bash
# This ADR is referenced from CLAUDE.md (characterization is canonical)
grep -n "2026-06-07-decompound-remc-hold" CLAUDE.md
# Expected: >=1 hit in the MC-anchor / Protection section

# §4 quarterly regime trigger (next: 2026-08-08) — re-run the gate on the locked config
python lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py 100
# Expected at HOLD: both candidates still GATE FAIL; the locked-config H1 still breaches
# (the trigger fires if a TRAILING-6mo window, substituted into the harness, clears/breaches)

# Locked config is genuinely untouched
git -C . diff --stat origin/main -- core/dd_protection.py core/firm_rules.py
# Expected: empty (no constant changes under this ADR)

# Calendar trigger reminder
# Quarterly regime check due: 2026-08-08 (then 11-08, 2027-02-08, 05-08)
```

---

## Verification

```bash
# Discipline checks (mechanical)
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-06-07-decompound-remc-hold.md --type adr
# Expected: all 6 checks PASS

# Production-source verification (Rule 0 confirmation)
git log -1 --format='%h %ci' -- core/portfolio_mc.py core/dd_protection.py core/firm_rules.py
pytest tests/test_mc_anchors.py -k pepperstone -q   # locked anchor still reproduces

# Regime-gate evidence reproduces
python lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py 100   # both candidates GATE FAIL on H1
```

---

## Addendum — 2026-06-25: clean single-file re-MC re-validation (HOLD-ROBUST)

**Trigger.** `Q-INCUMBENT-REGIME-1` (Scope-B per-strategy regime split) found that this
ADR's panels stitched Guardian/DJ30 from 2 TV exports each, and that the clean single-file
2026-06-25 export shows lower standalone DD for exactly those two strategies (DJ30 6.54% vs
stitched 9.03%; Aegis/NAS, single-file in both vintages, matched the old DD exactly) — a
**stitch-seam artifact**. This addendum re-runs the decompound re-MC on the clean vintage.

**Pre-registration:** `docs/ltm/briefs/pre-registration/2026-06-25-decompound-cleanvintage-remc-prereg.md`
(lock gates frozen before the run). **Full results:** `lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_cleanvintage_2026-06-25.md`. **Driver:** `remc_cleanvintage.py` (sibling; zero fork of the frozen 2026-06-07 harness).

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

**Flagged for the 2026-08-08 regime trigger (not run here):** because H1 is materially less
severe on clean data, the regime-robust deep-de-risk frontier may now clear at a more
practical risk/median than §3's "k≈0.25, 367-591d." Re-run `h1_check.py` on the clean vintage
at the trigger; a practical regime-robust config would reopen the de-risk option this ADR
closed. Today's HOLD is unchanged either way.

---

## Addendum — 2026-07-01 — §4 limb 1 falsifier dormancy (retirement back-propagation)

Per operational-rules Rule 11 (retirement events back-propagate to standing
falsifiers), the 2026-07-01 programme audit records that **§4 revert-trigger limb 1
— "≥2 challenge failures attributable to drawdown within any rolling 6-month
window" — is DORMANT.** As of the 2026-06-30 CFD retirement
(`docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`) there is no live
challenge in flight (FXIFY idle; futures chain not yet live), so no live challenge
failure can accrue to bind this limb. This is not a threshold change and §4 is not
edited — the limb re-arms automatically when live execution resumes (the futures
automation chain goes live and a challenge is in flight).

**Surviving coverage is intact:** §4 limb 2 (the quarterly trailing-6-month
`p99 DD ≥ 5% OR bust ≥ 1%` MC check, next **2026-08-08**) consumes TV panel
exports, not live fills, and remains fully in force and mechanically scheduled
(cron `fwd-quarterly-regime-ddrevert`). The HOLD's decision rests on that limb; the
dormant limb 1 was a *corroborating* live catch-path, not the primary. No re-MC and
no config change under this addendum.

> ⚠ **CORRECTION 2026-08-03 — the "surviving coverage is intact" paragraph above is NO LONGER
> TRUE.** It was accurate when written. Limb 2 is now **SUSPENDED-ORPHANED**: it consumes TV panel
> exports, and that panel can no longer be extended, so the trailing-window call is permanently
> `NOT_EXECUTABLE`. The sentence *"The HOLD's decision rests on that limb"* now reads as an
> **exposure statement**, not a reassurance — the limb it rested on is gone. See §Addendum
> 2026-08-03. Paragraph retained unedited as the 07-01 record.

---

## Addendum — 2026-08-03 — §4 limb 2 SUSPENDED-ORPHANED (retirement back-propagation)

**Type:** back-propagation under operational-rules **Rule 11** (retirement events back-propagate to
standing falsifiers), placed here under **Rule 14** (corrections land where the claim is read).
**This addendum decides nothing new.** The disposition was already ratified in
[ADR 2026-08-02 §2-D](2026-08-02-pepperstone-feed-retirement.md) (`Accepted`, operator ruling); a
second operator ruling 2026-08-03 (*"all pepperstone has been retired in light of the futures
pivot"*) re-confirmed the retirement independently. What was missing was the record **on the ADR
that owns the falsifier** — a reader of §4 had no way to learn its trigger could not fire.

### §0 — Rule 0 reads (this addendum, 2026-08-03)

Executed, not asserted — the claims below are measurements, not inferences:

| Read | Finding |
|---|---|
| `lab/analysis/regime/decompound_remc_2026-06-07/inputs/` (`ls`) | **6 Pepperstone CSVs + README still present.** Neither retirement touched them — both scoped to `core/data/tv_exports/pepperstone/`. The harness is **not** input-less. |
| `python regime_gate.py --regime-check --asof 2026-08-08` | `VERDICT: NOT_EXECUTABLE — panel ends 2026-06-02, 49 bdays short… 49/126 bdays uncovered.` Names its own remedy: *"a fresh Pepperstone TV export through the check date… an operator action, not a fetch."* |
| `python regime_gate.py 100` (the §10 hook) | **Still runs.** Full-panel C1 prints `pass 99.87% bust 0.13% p99 4.33%`. The §10 hook is not broken; only the *trailing-window* mode is unreachable. |
| [ADR 2026-08-02 §2-D](2026-08-02-pepperstone-feed-retirement.md) | A5 struck; limb 2 recorded as orphaned; owed forward regime monitor + orphaned limb 2 ruled **the same obligation**. |
| `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` | CFD venue closed — establishes that the named remedy is unprocurable, not merely outstanding. |

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
  [`docs/superpowers/specs/2026-08-02-venue-native-regime-monitor-design.md`](../superpowers/specs/2026-08-02-venue-native-regime-monitor-design.md).
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

### §10 — Audit hooks (runnable)

```bash
# 1. The suspension is recorded where the falsifier is READ (Rule 14 reader-intercept)
grep -c "SUSPENDED-ORPHANED" docs/adr/2026-06-07-decompound-remc-hold.md
# Expected: >=3 (the §4 banner, this addendum, the change-history row)

# 2. The gap is still open — the §4 reader-intercept still declares the HOLD uncovered
grep -c "no live falsifier" docs/adr/2026-06-07-decompound-remc-hold.md
# Expected: 2 — the §4 banner plus this hook's own string (M-AHF: the hook counts itself).
# A count of 1 means the banner was removed: do NOT read that as a lift until an explicit
# Rule-12 lift artifact is produced and named in Change history.

# 3. Limb 2 is genuinely unreachable, not merely unrun (re-verify, do not assume)
cd lab/analysis/regime/decompound_remc_2026-06-07 && python regime_gate.py --regime-check --asof 2026-11-08
# Expected: NOT_EXECUTABLE, uncovered-bday count LARGER than 08-08's 49/126 (the gap grows daily).
# If this ever returns a verdict, the panel was extended — investigate the source before trusting it.

# 4. Locked config untouched by this addendum
git diff --stat origin/main -- core/dd_protection.py core/firm_rules.py
# Expected: empty
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-07 | Initial authoring — HOLD + regime characterization; both de-risk candidates rejected by the regime-robustness gate | Joshua + claude.ai |
| 2026-06-25 | Addendum: clean single-file re-MC re-validation. HOLD-ROBUST (both gates still breach); breach severity corrected 2.92/5.93 → 1.47/5.32 (stitch-seam artifact). De-risk candidates still fail H1. | Joshua + Claude Code |
| 2026-07-01 | Addendum: §4 limb 1 (live challenge-failure catch-path) flagged DORMANT under go-dark (CFD retired, no live challenge); re-arms when live execution resumes. Limb 2 (quarterly MC) intact. No config/threshold change. | Joshua + Claude Code (programme audit) |
| 2026-08-03 | Addendum: §4 limb 2 **SUSPENDED-ORPHANED** — panel unextendable after the Pepperstone feed retirement (venue closed), so the trailing-window call is permanently `NOT_EXECUTABLE`; quarterly schedule struck (not deferred). HOLD stands but is now **unfalsifiable** until the venue-native regime monitor discharges it (ADR 2026-08-02 §2-D — "the two holes are one hole"). §4 reader-intercept added; the 07-01 "limb 2 intact" claim corrected in place. No config/threshold/allocation change. | Joshua + Claude Code |
