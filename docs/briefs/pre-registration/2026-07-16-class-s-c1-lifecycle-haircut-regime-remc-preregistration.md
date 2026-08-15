# Pre-registration — Class-S candidate #1: reversible lifecycle-haircut regime re-MC (deployable vs accept-with-caveat)

> ⚠ **2026-07-22:** this frozen body's "already-discharged four-firms ADR §4" premise was
> **WITHDRAWN** — see [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
> §4 is undischarged (hard date 2026-11-08 unchanged). Body left frozen as written (Trap #12); this Q's own verdict is unaffected.

**Status:** `FROZEN` (operator signed §9, 2026-07-16 — chat authorization "sign it, run the
1.00× control and both arms"). No item below changes after any haircut-arm result is seen
(Known Trap #12 — amendments require closing this pre-registration and opening a fresh one).
**What this is:** a pre-registered re-MC that tests whether a **reversible book-level
lifecycle haircut** (WATCH-1 0.50× or WATCH-2 0.25×) restores regime-robustness to the
already-DISCHARGED Class-S candidate #1, or whether c1 is accept-with-caveat.
**Parent candidate (unchanged, cited not re-decided):**
[`2026-07-15-existing-strategy-book-candidate-1-prereg.md`](2026-07-15-existing-strategy-book-candidate-1-prereg.md) (`FROZEN`; Part A **DISCHARGED**, regime rider **GATE FAIL**).
**Gate of record (unchanged, cited not re-decided):**
[`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) (`be6dda6`, FROZEN) — floor bust ≤ 3.0% + P(pass) ≥ 50%.
**Loop of record:** STRATEGIC.
**Feeds:** candidate #1's G8 deployability disposition (the standing regime-fragile caveat);
informs but does **not** alter the four-firms ADR §4 falsifier, already discharged.
**Authored:** 2026-07-16 · Claude Code (Opus 4.8), operator-directed ("scope the haircut re-MC").

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-16, HEAD `009b0ca`)

Per-file anchors (`git log -1 --format='%h %ci'`), all content-read in full this session:

- **[`core/lifecycle.py`](../../../core/lifecycle.py) @ `4441c72`** — `TIER_MULTIPLIER` pins the
  ratified ladder: `AUTHORIZED 1.00 / WATCH-1 0.50 / WATCH-2 0.25 / RETIRED 0.00` (L33-38),
  MVD-pinned by `_validate_ladder()` (a drift is a governance change, not a code edit). The
  multiplier is a **risk_pct-layer haircut that MULTIPLIES BASE_RISK/DD_SCALE, never edits
  them** (L9-16); down-only invariant `[0.0, 1.0]` (L187). **This is why the only legitimate
  haircut arms are 0.50× and 0.25× — a fractional value between/below the rungs is a
  governance violation, not a research knob.**
- **[`core/dd_protection.py`](../../../core/dd_protection.py) @ `a53ee99`** — sizing composition
  `scaled_risk = BASE_RISK × multiplier × lifecycle[k]` (L216); `lifecycle=None ⇒ all 1.0×`,
  byte-identical to the pre-lifecycle path. Confirms a uniform book-level lifecycle multiplier
  is a clean linear scalar on risk_pct. **Not touched by this brief** — the candidate scoring
  runs `dd_protection` OFF (parent §2), so there is no `DD_SCALE` compounding; the haircut is
  the sole internal sizing scalar.
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py) @ `163b0b5`** —
  the exact harness this re-MC extends. Reads in full: `daily_100k = book_daily_at_100k(panel_c1)`
  (L551) is the injection point; `full_panel_reference` + `part_b_half_panel` (index-midpoint
  H1/H2, L120-124) + `part_a_bootstrap` (`N_PANELS_DEFAULT=100`, `BLOCK_SIZE_BDAYS=126`,
  `BOOT_SEED=20260715`, L73-76); floor via `_floor_ok` = `bust ≤ thr.eval_bust_ceiling AND
  pass ≥ thr.pass_floor` (L113-117); `compose_verdict` = GATE PASS iff bootstrap ∧ H1 ∧ H2 on
  both tiers (L316-352). `DISCHARGE_TIERS = (Tradeify_Select_100K, MFFU_Rapid_100K)` (L72).
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md) @ `163b0b5`** —
  the **1.00× baseline** this re-MC's reproduction control must match within MC noise:
  Tradeify H1 bust **4.37%** / bootstrap-95th **10.37%**; MFFU H1 **4.36%** / bootstrap-95th
  **10.33%**; both full-panel + H2 PASS; verdict **GATE FAIL (regime-fragile)**.
- **[`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) @ `be6dda6`** —
  frozen floor **bust ≤ 3.0%** (daily+static+trailing via `summarize_outcomes`) **+ P(pass) ≥ 50%**
  (finite median-days inside a practical horizon) (L119-121); Run-2 (consistency-on) is the gate
  where consistency exists (L100-101). **Nothing here re-decides the floor.**
- **[`docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md`](2026-07-15-existing-strategy-book-candidate-1-prereg.md) @ `58fff1d`** —
  parent candidate: §2 fixed 2-leg MYM+MNQ book (panels byte-pinned; weights 0.70%/0.37% as
  venue variables); §6 regime rider (a both-halves FAIL rides into G8 as a standing caveat, does
  not overturn Part A DISCHARGED); §5 forbids re-weighting the book.
- **[`docs/methodology/regime_robustness_gate.md`](../../../docs/methodology/regime_robustness_gate.md) @ `f2be990`** —
  Part A (6mo-block bootstrap) + Part B (half-panel split); Part C acceptance = all three clear
  the **brief's full-panel floor**. **Load-bearing constraint (§"Pre-registered floor"):** the
  gate's floor MUST equal the full-panel floor — "no separate 'regime floor' is permitted — that
  would be a hidden parameter through which post-hoc fitting could enter." This forecloses
  inventing a laxer bust ceiling for the haircut arms.
- **[`lab/discovery/prop_survivor_scoring.py`](../../../lab/discovery/prop_survivor_scoring.py) @ `97011c1`** —
  `run_tier_remc` / `score_part_a` / `blocks_from_daily_pnl` (the MC primitives the harness
  calls). `score_part_a`'s finite-median check implies `run_tier_remc` computes median-days
  internally (surfaced as a diagnostic in §2). **Architecture-truth flag (executor confirms in
  §8 Phase 0):** the Run-2 consistency clause (`simulation.py`) is asserted scale-invariant under
  a uniform daily haircut — see §2; if it is dollar-thresholded rather than ratio-based, the
  haircut must be applied at the allocation layer instead (§8 fallback), not post-hoc on `daily_100k`.

---

## §1 — Context + the lever under test

Class-S candidate #1 (2-leg MYM+MNQ, the locked Striker legs on CME micros) **cleared frozen
Part A on Tradeify_Select_100K + MFFU_Rapid_100K and discharged the four-firms ADR §4 falsifier**
(2026-07-15) — that result is **banked and not re-opened here**. But the gate §7(7) regime rider
returned **GATE FAIL (regime-fragile)**: the book passes the full compounded panel and the
2023-26 trend half (H2 bust 1.70%), yet the **2020-23 chop half busts 4.37%/4.36%** and the
6mo-block bootstrap-95th hits **10.37%/10.33%**, both above the 3.0% ceiling. This is the book's
structural regime split — the same signature the **decompound re-MC HOLD** documented for the CFD
book ([`docs/adr/2026-06-07-decompound-remc-hold.md`](../../adr/2026-06-07-decompound-remc-hold.md)):
there, on the same 2020-23/2023-26 split, **no static de-risk was regime-robust without making the
challenge impractical**, and the locked config was HELD (managed operationally + quarterly regime
trigger). The two candidate de-risks (k=0.55, DD_SCALE→0.20) both failed the regime-robustness gate
on the 2020-23 half.

The operator-chosen lever (2026-07-16): the one **legitimate, non-forbidden, reversible** de-risk
that could move c1 from "gate-pass with a standing caveat" to "deployable" is a **book-level
lifecycle haircut** — WATCH-1 (0.50×) or WATCH-2 (0.25×), the ratified ladder rungs
([`core/lifecycle.py`](../../../core/lifecycle.py) `TIER_MULTIPLIER`). It multiplies the book's
risk_pct uniformly, never edits a locked parameter, never re-weights the composition, and is
authorization-down-only. Applied book-level in the scoring harness (per the G8 intake note: "no
`core/lifecycle.py` write for the four locked CFD legs"), it does not touch the live CFD legs'
authorization state.

**Honest prior (disclosed, not pre-biasing):** the decompound precedent predicts this test
**FALSIFIES** — a uniform haircut reduces the edge proportionally and static de-risk did not land
regime-robust there. But c1 is a materially different object (2 legs, Striker-only, native-futures
panels, the survivor-scoring $100K/trailing_locking model with **no** withdrawal/$200K-reset), so
the CFD verdict does not automatically transfer. The test is worth its compute precisely because a
FALSIFIED outcome (accept-with-caveat) and a RESOLVED outcome (a reversible path to deployability)
are both live, pre-committed possibilities.

---

## §2 — The test (FIXED — the entire arm set is these three multipliers)

| Item | Fixed value |
|---|---|
| Book | Class-S candidate #1 exactly as frozen: 2 legs Striker→MYM + Striker→MNQ, byte-pinned panels, weights 0.70%/0.37%. **Not re-weighted, not re-composed, no leg added/removed.** |
| Haircut arms | **Exactly three:** `1.00×` (reproduction control) · `0.50×` (WATCH-1) · `0.25×` (WATCH-2). No fractional value; no arm outside `TIER_MULTIPLIER`. |
| Injection (primary) | `daily_100k → daily_100k × h` after `book_daily_at_100k(panel_c1)` (harness L551), before full/half/bootstrap. The %-equity decompound panel is linear in position size, so ×h is the faithful representation of an h× risk_pct book-level haircut. |
| Injection (fallback, §8 Phase-0 gated) | If the Run-2 consistency clause is **not** ratio-based (dollar-thresholded), apply h at the allocation layer (`C1_ALLOCS × h` into `build_scaled_panel`) so the consistency interaction is modeled correctly; note the choice in RESULTS. |
| Partitions per arm | Full panel · H1 (2020-23 chop) · H2 (2023-26 trend) · 6mo-block bootstrap (n=100, block=126 bd, seed 20260715) — **identical to the 1.00× rider; not re-parameterized.** |
| Tiers per arm | The two discharge tiers only: `Tradeify_Select_100K` · `MFFU_Rapid_100K`. |
| Engine | Frozen: 10,000 sims × seeds 42/123/2026, horizon 1500, inactivity disabled, `dd_protection` OFF, Run-2 (consistency-on) where consistency exists — inherited from the parent, never re-decided. |
| Floor (per partition, both tiers) | **bust ≤ 3.0% AND P(pass) ≥ 50%** — the frozen gate floor, unchanged. Per the regime-gate methodology, **no separate "regime floor" is introduced.** |
| Reported per (arm × tier × partition) | `headline_bust`, `pass_rate`, `median_days_to_pass` (**diagnostic, non-gating** — surfaces the decompound "impractical" cost of the haircut), `floor_ok`; bootstrap adds `pass_5th`/`bust_95th`. |

**Scale-invariance note (the load-bearing subtlety):** a uniform daily haircut halves both max-day
P&L and total P&L, leaving the max-day/total **ratio** unchanged — so a ratio-based consistency rule
is scale-invariant under ×h and the primary injection is faithful under Run-2. §8 Phase-0 confirms
the clause is ratio-based; if not, the fallback injection binds. This is the one place the primary
injection could silently mismodel, so it is checked, not assumed.

**Decision rule (least-haircut-that-clears):** among arms whose regime gate **PASSES** (all three
partitions clear the floor on **both** tiers), select the **largest** multiplier (least haircut) —
0.50× before 0.25× — because down-only authorization applies the minimum necessary de-risk. If
neither 0.50× nor 0.25× clears, there is no passing arm.

---

## §3 — Inherited unchanged (cited, not re-decided)

- Frozen floor bust ≤ 3.0% + P(pass) ≥ 50% (survivor-scoring pre-reg `be6dda6`).
- The two discharge tiers, engine params, seeds, Run-2 gating (parent candidate §2).
- Bootstrap n=100 / block 126bd / seed 20260715, half-panel index-midpoint split (regime-gate driver `163b0b5`; methodology `f2be990`).
- The ratified haircut rungs 0.50×/0.25× (`lifecycle.py` `4441c72`).
- The mechanical Part A **DISCHARGED** read (parent §6): this re-MC informs **deployability only**; it cannot and does not re-open the discharge.

---

## §4 — Falsifiable hypothesis (H-HAIRCUT; binary)

**H-HAIRCUT — if** there exists a haircut arm `h ∈ {0.50×, 0.25×}` under which candidate #1's
regime-robustness gate **PASSES** — i.e. `headline_bust ≤ 3.0% AND pass_rate ≥ 50%` on the full
panel **AND** H1 **AND** H2 **AND** the 6mo-block bootstrap-95th, on **both** `Tradeify_Select_100K`
and `MFFU_Rapid_100K` — **then** c1 has a reversible static de-risk to regime-robust deployability,
applied at the least-haircut passing rung (a book-level lifecycle WATCH tier); rail/account/go-live
stay separately gated. **Otherwise** (neither rung clears every partition on both tiers) H-HAIRCUT
is **falsified**: c1's regime fragility is not fixable by a static lifecycle haircut, and its
disposition is **accept-with-caveat** (the decompound-HOLD precedent) — a CANDIDATE @ 1.00× riding
the quarterly regime trigger, not deployed static-robustly.

**Accept/reject (restated numerically):** accept-DEPLOYABLE iff ≥1 arm in {0.50×, 0.25×} yields
`bust ≤ 3.0% ∧ pass ≥ 50%` on {full, H1, H2, bootstrap-95th} × {Tradeify, MFFU} — all eight cells;
reject (accept-with-caveat) on any other pattern. The 1.00× arm is the reproduction control, not a
candidate to pass.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Inventing a fractional haircut** (0.35×, 0.60×, a bisection to "just clear" the bootstrap-95th) —
  only the ratified rungs 0.50×/0.25× are legitimate (`lifecycle.py` `TIER_MULTIPLIER`, MVD-pinned).
  A tuned multiplier is a researcher DOF **and** a governance violation; it voids this pre-registration.
- **Re-weighting the 0.70/0.37 book composition** to reduce H1 bust — the ADR- and parent-§5-forbidden
  composition-layer best-of-K; it is a different lever than a uniform lifecycle haircut and is not
  admitted here under any result.
- **Relaxing the 3.0% bust ceiling or the 50% pass floor, or introducing a separate "regime floor"** —
  explicitly forbidden by the regime-gate methodology's pre-registered-floor rule; the floor is the
  frozen gate floor or the arm fails.
- **Reading a haircut result as re-opening Part A DISCHARGED** — DISCHARGED is banked (mechanical,
  full-panel); this re-MC only informs deployability. A PASS does not "upgrade" the discharge; a FAIL
  does not retract it.
- **Editing `DD_TRIGGER`/`DD_SCALE`/`BASE_RISK` or any locked parameter** — the haircut multiplies,
  never edits (axis-separation invariant, `lifecycle.py` L15-16).
- **Writing `lifecycle_state.json` for the four CFD legs** — the haircut is book-level in the harness
  (G8 intake note); it must not haircut the live CFD legs' authorization.
- **Treating a PASS as go-live authorization** — rail build, account registration, and go-live stay
  operator-gated; a PASS yields a *deployability finding*, not a live account.
- **Using `median_days_to_pass` as a gate** — it is a reported diagnostic only; promoting it to a
  pass/fail threshold would introduce exactly the hidden parameter the regime-gate methodology forbids.

---

## §6 — Gate criteria (binary dispositions)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED-DEPLOYABLE** | ≥1 arm ∈ {0.50×, 0.25×} clears the floor on all four partitions × both tiers | c1 has a reversible de-risk to regime-robustness at the least-haircut passing rung (WATCH-1 preferred over WATCH-2); recorded as a **deployability finding** (book-level lifecycle tier); rail/account/go-live still gated; `median_days_to_pass` reported as the practicality cost for the operator's go-live judgment |
| **FALSIFIED-FRAGILE** | Neither 0.50× nor 0.25× clears every partition on both tiers | Static lifecycle haircut cannot make c1 regime-robust → **accept-with-caveat** per the decompound-HOLD precedent; c1 stays CANDIDATE @ 1.00× with the standing regime-fragile caveat, riding the quarterly regime trigger; the harvest/Class-S §4 falsifier is unaffected (already discharged) |
| **AMBIGUOUS (noise-band)** | An arm's decisive cell (typically bootstrap-95th) lands within MC noise of 3.0% — i.e. bootstrap-95th ∈ (3.0%, 3.0%+ε] **or** the reproduction control 1.00× fails to reproduce REGIME_GATE.md within noise | Upgrade bootstrap to **n=200** (methodology edge-case) and re-adjudicate that arm once; a still-borderline result closes AMBIGUOUS with the band reported (no third re-run, no floor move) |

Reproduction-control precondition: the 1.00× arm must reproduce REGIME_GATE.md (Tradeify H1 4.37% /
boot-95th 10.37%; MFFU 4.36% / 10.33%) within MC noise **before** the 0.50×/0.25× arms are trusted;
a mismatch routes to AMBIGUOUS (harness-extension defect), not to a haircut verdict.

---

## §7 — Prior-look disclosure

The **only** prior look on this book's regime surface is the **1.00× rider** (REGIME_GATE.md,
2026-07-15): GATE FAIL, H1 4.37%/4.36%, bootstrap-95th 10.37%/10.33%. **No haircut arm (0.50× or
0.25×) has been run on this book at any partition** — this pre-registration authors those arms before
any is seen. K accounting: 2 pre-declared arms on a governance-pinned grid (the ratified ladder rungs),
zero researcher DOF on the multiplier value; the 1.00× arm is a reproduction control, not a trial.
No DSR/Clause-K claim is made or needed (Class S is out-of-screen-scope; the gate of record has no DSR
clause — parent §7).

---

## §8 — Run protocol (post-signature)

1. **Phase 0 (architecture-truth confirm, before any arm):** confirm the Run-2 consistency clause in
   `core/mc/simulation.py` is **ratio-based** (max-day/total profit ratio), hence scale-invariant under
   a uniform daily haircut. If ratio-based → primary injection (`daily_100k × h`). If dollar-thresholded
   → fallback injection (`C1_ALLOCS × h` through `build_scaled_panel`); record the choice. Confirm
   `run_tier_remc` exposes `median_days_to_pass` (used by `score_part_a`'s finite-median check); if not
   surfaced, add it as a returned field (additive, non-behavioral).
2. **Harness extension (additive, backward-compatible):** add `--lifecycle-mult FLOAT` (default `1.0`)
   to `run_class_s_c1_regime_gate.py`; apply at the confirmed injection point; write results to a
   per-arm out-dir (`--out-dir`). Default `1.0` path must be **byte-identical** to the current harness
   (guard: a `--lifecycle-mult 1.0 --smoke` run matches the existing smoke output).
3. **Reproduction control:** run `--lifecycle-mult 1.0` full (n_panels=100, frozen sims); assert it
   reproduces REGIME_GATE.md within MC noise. Mismatch → AMBIGUOUS (harness defect), stop.
4. **Haircut arms:** run `--lifecycle-mult 0.50` then `--lifecycle-mult 0.25`, full, both discharge
   tiers, all partitions. (~2.6h wall each at n=100; may run serially or delegate; research venv.)
5. **Adjudicate** per §6 against the frozen floor; select the least-haircut passing arm if any.
6. **RESULTS** land in `lab/analysis/class_s_c1_haircut_regime_remc_2026-07-<dd>/`; header cites **this**
   pre-registration **and** the parent candidate + gate pre-registrations by path.

The run is **operator-gated on §9** and may be delegated (per the CC/Cursor surface-allocation ADR) to
a frozen-spec executor; adjudication (§6) returns to CC.

---

## §9 — Operator signature (gates the run; DRAFT until filled)

```
SIGNED / FROZEN: 2026-07-16 / JA
Authorized: reversible lifecycle-haircut regime re-MC on Class-S candidate #1.
Arms fixed at {1.00× control, 0.50× WATCH-1, 0.25× WATCH-2}; floor + tiers + engine
inherited unchanged. No arm runs before this block is filled. Deployability finding only —
rail/account/go-live remain separately gated.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature-before-run: signed form present (not the placeholder) before any arm runs.
grep -n "SIGNED / FROZEN: ____" docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md \
  && echo "STILL DRAFT — no arm may run" || echo "signed"

# 2. Arm-set immutability: exactly the three ratified multipliers, no fractional invention.
grep -n "1.00×\|0.50×\|0.25×" docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md | head

# 3. Haircut rungs match the production ladder (drift ⇒ this brief is stale, lifecycle.py wins).
grep -n '"WATCH-1":    0.50\|"WATCH-2":    0.25' core/lifecycle.py

# 4. Frozen floor unchanged (this brief must not have moved it).
grep -n "bust ≤ 3.0%\|P(pass) ≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head -3

# 5. Baseline the reproduction control must match.
grep -n "4.37%\|10.37%\|GATE FAIL" lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md

# 6. No haircut RESULTS exist yet (expected while DRAFT).
ls lab/analysis/ | grep -i "c1_haircut\|haircut_regime" || echo "no haircut re-MC yet (expected pre-signature)"

# 7. Default-1.0 byte-identity guard is honored once the harness is extended.
grep -n "lifecycle-mult\|lifecycle_mult" lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py || echo "harness not yet extended (expected pre-signature)"
```

---

## Verification

```bash
# Discipline checks — repo-side mechanical subset (in-repo; well-formed 0 HARD/0 WARN):
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md --type inquire
# Authoritative 6/6 discipline gate is skill-side (home path, run 2026-07-16 -> 6/6 PASS):
#   PYTHONIOENCODING=utf-8 python ~/.claude/skills/brief-authoring/scripts/check_brief.py <brief> --type inquire

# §0 anchors (Rule-0 confirmation)
git log -1 --format='%h %ci' -- core/lifecycle.py                                                             # 4441c72
git log -1 --format='%h %ci' -- core/dd_protection.py                                                         # a53ee99
git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py  # 163b0b5
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md       # be6dda6
git log -1 --format='%h %ci' -- docs/methodology/regime_robustness_gate.md                                    # f2be990

# Ladder + floor cross-checks
grep -n "0.50\|0.25" core/lifecycle.py | head -3
python -c "import sys; sys.path.insert(0,'core'); import lifecycle; print(lifecycle.TIER_MULTIPLIER)"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Drafted (`DRAFT — awaiting operator signature`); arms fixed at {1.00× control, 0.50×, 0.25×}; floor/tiers/engine inherited from the parent candidate + gate pre-registrations | Joshua (direction) + Claude Code (Opus 4.8) |
| 2026-07-16 | **Signed / FROZEN** (§9) — operator chat authorization ("sign it, run the 1.00× control and both arms"); run of all three arms authorized. No item above changed at signature. | Joshua (JA) |
