# Pre-registration — sub-100K realizable-book Part A scoring (integer-quantization successor)

**Status:** `SIGNED / FROZEN 2026-08-02 / JA` — see §9. No item below changes after any bust number
is seen; amendments require closing this pre-registration and opening a fresh one (Known Trap #12).
The freeze is git-auditable: this file's commit must strictly precede any harness execution
(§10 hook 1).
> **Header duty at signature — DISCHARGED in the signing commit**, per the rule this line carried
> while unsigned: `Q-6JCOMPOSE-1` sat at `DRAFT — §9 UNSIGNED` for four days after it was signed
> *and* after it was closed VOID, and that stale header directly cost a session on 2026-08-02.

**Authored:** 2026-08-02 · Claude Code (Opus 5), operator-directed ("author the scoring pre-reg with
that selection rule")
**Motivating measurement (arithmetic, already run, $0):**
[`lab/analysis/c1/band_quantization_2026-08-02/RESULTS.md`](../../../lab/analysis/c1/band_quantization_2026-08-02/RESULTS.md)
**Frozen gate (cited, not re-decided):**
[`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) — Part A
`bust ≤ 3.0% ∧ P(pass) ≥ 50%`, Run-2, 10k × seeds 42/123/2026, horizon 1500, inactivity off.
**Parent band study (cited, not reopened):**
[`2026-07-24-c1-band-rescore-corrected-geometry-prereg.md`](2026-07-24-c1-band-rescore-corrected-geometry-prereg.md)
(`FROZEN`) — this brief is its **integer-realization successor**, not an amendment to it.
**Loop of record:** OUTER (INQHIORI). **D-S-A domain:** data.
**Layer:** measurement against a standing gate. **No locked parameter, allocation, `dd_protection`
constant, Pine file, rail config, `LEG_MAP` entry, or lifecycle state is touched.**

---

## §0 — Rule-0 reads (executed this session 2026-08-02, not recalled)

| # | Source + anchor | What it established | Verification performed |
|---|---|---|---|
| 1 | `ops/c1_rail/c1_sizing_host_reference.py` @ `c134060`, **L295** | The production sizing law `reserve_cap = floor(cap_alloc / (1 + pyr_pct/100))`; a leg with `reserve_cap = 0` never sends | Source read. Re-applied and **controlled against the file's own pinned comment (L76-79)**: `MYM 8+60=68 · MNQ 1+10=11 · 79 ≤ 80` — **MATCH**. |
| 2 | `lab/analysis/c1/band_quantization_2026-08-02/RESULTS.md` (this session) | Under the locked-proportional 69/11 split, **MNQ zero-floors at every FRIENDLY tier below 100K**; T-25K floors both legs. Exhaustive search: 11–51 viable re-allocated 2-leg splits exist per tier (T-25K excepted); smallest viable `cap_firm` = 20 | Harness committed and re-runnable; exits non-zero if either control fails. |
| 3 | `lab/analysis/c1/eval_shape_diagnostics_2026-07-28/RESULTS.md` Part A appendix | The published T-50K quantization result: *"MNQ zero-floors (`floor(5/11)=0`) → 1-leg MYM book, aggregate 34/40"* | Re-derived independently — **MATCH** (control 2 of the harness). This brief extends it, it does not restate it. |
| 4 | `lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md` | The figures under test: **T-50K 1.06% / 98.93%** and **MFFU-50K 0.96% / 99.03%** at 1.00×, corrected geometry, full panel; the *"NOT a §4 discharge"* clause; the cap-exact 40/40 note and its **pre-committed** integer-quantization follow-on | Read in full including the 2026-07-28 addendum. Confirmed the published rider bootstraps **4.54%/4.49% are SUPERSEDED** (M-23 process-pool defect); corrected T-50K is **6.69%**, MFFU-50K **NOT RE-MEASURED / impeached**. |
| 5 | `core/firm_rules.py` @ `fc14682` | `Tradeify_Select_50K`: cap **40**, trail 4.0%, target 6.0%, bal $50K. `MFFU_Rapid_50K`: cap **50**, trail 4.0%, target 6.0%, bal $50K. **Both ship `dd_lock_offset_usd: 100`, known-defective for eval** | Dumped programmatically. The corrected-geometry patch is therefore **mandatory and worker-local** (§2). |
| 6 | `lab/analysis/c1/eval_shape_diagnostics_2026-07-28/_boot_attested.py` + `run_rider_tail_attribution.py` | The **worker-attested** corrected-geometry primitives (`run_partition_mc_attested`, `half_panel_attested`, `part_a_bootstrap_attested`) and the M-23 idiom: patch `dd_lock_offset_usd` **inside each worker**, attest the value used | Source read. This is the harness this brief extends; a parent-only patch through a process pool silently scores defective geometry with plausible output (M-23, dated 2026-07-25). |
| 7 | `docs/briefs/closures/Q-CAPALLOC-2-closure-resolved-fragile.md` | Operator elected **DECLINE** 2026-07-30: `69/11` stands, **no `LEG_MAP` change**, no tripwire | Read. §5 forbids this brief from being cited toward any live allocation change. |
| 8 | `2026-07-13-prop-survivor-scoring-prereg.md` §5 | *"Post-hoc tier substitution after seeing per-tier results (best-of-K at the gate layer) — the four $100K tiers are frozen."* | Read. This is the discipline the §2 selection rule exists to satisfy one layer down (allocation space). |

---

## §1 — Question (symptom-only)

The estate's only two mechanical Part A clearers — `Tradeify_Select_50K` **1.06%** and
`MFFU_Rapid_50K` **0.96%** — were scored on a **continuously-sized 2-leg book**. The integer rail
cannot realize that book at those tiers under the locked-proportional split: MNQ's `reserve_cap`
floors to 0, leaving a 1-leg MYM book. **The bust of what the rail would actually run there has never
been measured**, and those two figures are the sole basis on which the 2026-11-08 demotion clause is
currently defeated.

*Symptom-only phrasing: a published pass-rate describes a book configuration the execution layer
cannot instantiate, and the configuration it can instantiate is unmeasured.*

---

## §2 — Method (FROZEN)

**Engine:** the corrected-geometry attested primitives from
`lab/analysis/c1/eval_shape_diagnostics_2026-07-28/_boot_attested.py`, imported **unmodified**. 10,000
sims × seeds 42/123/2026, horizon 1500, **Run-2** (consistency-on), `dd_protection` off, **full panel
only**.

**Geometry — MANDATORY:** `dd_lock_offset_usd → 1_000_000.0`, applied **worker-local**, the value
used **attested in the run record**, restored to `100` afterwards. The production constant is **not**
edited. Running the shipped `100` scores a drawdown lock the evaluation does not have (2026-07-22
correction); patching parent-only through a process pool reproduces M-23.

**Panel:** the frozen c1 daily panel via the untouched `build_scaled_panel` (guards intact), rescaled
to each tier's `starting_balance`. **Book shapes are constructed by COLUMN SELECTION on that panel —
never by re-running, re-fitting, or re-weighting a strategy.**

### The frozen cell set — 4 gating cells, all pre-named, no post-hoc selection

| # | Tier | Book shape | Realizable because |
|---|---|---|---|
| A1 | `Tradeify_Select_50K` | **1-leg MYM** (MNQ column dropped) | locked-proportional 34/5 ⇒ MNQ `reserve_cap` 0 |
| A2 | `MFFU_Rapid_50K` | **1-leg MYM** | locked-proportional 43/6 ⇒ MNQ `reserve_cap` 0 |
| B1 | `Tradeify_Select_50K` | **2-leg** | re-allocated **MYM 29 / MNQ 11** ⇒ stacks 25 + 11 = 36/40 |
| B2 | `MFFU_Rapid_50K` | **2-leg** | re-allocated **MYM 39 / MNQ 11** ⇒ stacks 34 + 11 = 45/50 |

**Rung:** **1.00×** — the frozen gate's candidate basis, and the basis the published 1.06%/0.96%
clearers were scored on. The deployed **0.50×** rung is **not** run here; it is a **pre-committed
follow-on** for any clearer (§7), matching the parent band study's structure.

**Tier set is FROZEN at these two and adding a tier is forbidden (§5).** Bulenox 25K/50K and
BluSky 50K are unscored and are **explicitly out of scope**: scoring them would be *searching for a
clearer*, a different act from *re-verifying an impeached one*, and it carries its own K and its own
pre-registration.

### §2.1 — The allocation-selection rule (operator-approved 2026-08-02, fixed before any result)

> **Rule: locked-proportional as configured, plus exactly ONE re-allocated split per tier, selected
> by MAXIMUM MYM `cap_alloc` among all splits where both legs have `reserve_cap ≥ 1` and the realized
> aggregate fits `micro_contract_cap`.**

This collapses an 11–51-wide viable allocation space to **one** named cell per tier. The rule is
mechanical, stated before any bust is seen, and is **not** re-run if the chosen split fails —
re-selecting after a result is the best-of-K move §5 bars.

Applied: T-50K → **29/11** (of 21 viable); MFFU-50K → **39/11** (of 31 viable).

### §2.2 — What the gate can and cannot see (scoping, declared not discovered)

The gate scores an **R-normalized** panel: legs enter by **risk %**, not contract count. Therefore:

- **Composition is visible.** Dropping MNQ is a real change the gate scores. Cells A1/A2 are
  genuinely new measurements.
- **Cap clipping is invisible.** The gate cannot see that the 29/11 book runs MYM at a **25**-contract
  stack where the published cell modeled **34** (−26.5%). Cells B1/B2 therefore reproduce the
  published 2-leg figures **modulo an unmodellable clipping term**.

**This is why B1/B2 are worth running anyway, and their role is stated in advance: they are
simultaneously the realizable 2-leg expression AND a reproduction check on the published clearers.**
Pre-registered expectation, scoreable: **B1 ≈ 1.06% and B2 ≈ 0.96%, and because the re-allocated book
carries strictly LESS total size than the published cell modeled, B should land at or BELOW the
published figure.** A B-cell landing **materially above** its published figure is a **defect signal**,
not a finding, and routes to §6 AMBIGUOUS.

**Exactly four gating cells are run.** No rung sweep, no tier sweep, no allocation sweep, no panel
sweep, no re-selection.

---

## §3 — Preconditions

- **P1 — Geometry.** Corrected + worker-attested (§2). If the attestation is absent from the run
  record, the run is **VOID**, not "reported with a caveat".
- **P2 — Column selection only.** The 1-leg book is the 2-leg panel minus its MNQ column. Any
  re-derivation, re-fit, or re-weight of a leg voids the cell.
- **P3 — Cap 40 / 50 are read from `firm_rules.py`, not inferred.** Both are config values, unlike
  the 6J cap-8 inference. No standing conditional attaches.
- **P4 — The published figures under test are the CORRECTED-geometry ones** (T-50K 1.06%, MFFU-50K
  0.96%). The superseded rider bootstraps (4.54% / 4.49%) are **not** used anywhere.

---

## §4 — Falsifiable hypothesis + disclosed prior

**H:** *At least one realizable sub-100K book shape clears Part A* — i.e. `bust ≤ 3.0%` **and**
`P(pass) ≥ 50%` on the full panel at 1.00×, corrected geometry, in at least one of the four frozen
cells.

**If** any cell clears, **then** H holds and the 11-08 demotion-clause defeat survives integer
realization on that cell. **If** no cell clears, **then** H is FALSIFIED and the sub-100K clearer
status does not survive integer realization — the demotion clause's defeat rests on an
unrealizable configuration.

| Observation | Threshold | Conclusion |
|---|---|---|
| any cell: bust ≤ 3.0% **and** P(pass) ≥ 50% | full panel, 1.00× | H holds → **RESOLVED-CLEARER-SURVIVES** |
| all four cells: bust > 3.0% **or** P(pass) < 50% | full panel, 1.00× | H falsified → **FALSIFIED** |
| a decisive cell in (3.0%, 3.2%] | MC noise band | **AMBIGUOUS** (§6) |

**DISCLOSED PRIOR — split, and stated so both limbs are scoreable:**

- **B-cells: expected to CLEAR** (≈1.06% / ≈0.96%, at or below published). They are near-reproductions
  of figures already measured as clearers. A B-clear is therefore **weak evidence** — it mostly
  confirms the harness.
- **A-cells (1-leg MYM): genuinely uncertain, and I decline to predict a direction.** Two opposing
  mechanisms, both real: dropping MNQ **removes variance** (MNQ is the smaller, lower-variance leg —
  bust down), but it also **removes diversification and halves trade cadence** (bust up via a longer
  time-to-target under the same trail, and a worse loss-side shape — the property Q-GEOFIT-1 showed
  actually governs trailing-DD survival). **No prior artifact measures a 1-leg MYM book at any tier**,
  so there is nothing to extrapolate from and a guess here would be theatre.

**The load-bearing cell is A, not B.** A B-clear does not rescue the published clearer, because the
published clearer was scored under an allocation nobody has authorized — see §8.

---

## §5 — Forbidden moves

Each was available to the author; none is a strawman.

- **Re-selecting the allocation after seeing a result.** The §2.1 max-MYM rule is fixed. If 29/11
  fails, trying the other 20 viable T-50K splits is best-of-K at the allocation layer — the exact
  move the frozen gate's §5 bars one layer up.
- **Adding Bulenox 25K/50K or BluSky 50K if the four cells fail.** Bulenox_25K has the friendliest
  trail/target ratio in the registry (6%/6%) and is the most tempting place to go looking. Out of
  scope by §2; a new tier needs a new pre-registration and its own K.
- **Reading a B-cell clear as rescuing the published clearer.** B is realizable only under a cap
  re-allocation that has never been authorized, and Q-CAPALLOC-2 closed with the operator declining
  a `LEG_MAP` change (§0 row 7).
- **Citing any result here as a §4 discharge.** §4 discharges only at the frozen **$100K×4** set.
  Sub-100K clearing bears on the 11-08 *demotion clause*, never on the discharge.
- **Quoting the superseded rider bootstraps (4.54% / 4.49%)**, or treating MFFU-50K's impeached
  bootstrap as measured.
- **Running with the shipped `dd_lock_offset_usd: 100`, or patching parent-only** (M-23).
- **Treating a clear as licence to buy an eval, change a tier, or touch `LEG_MAP`.** See §8.
- **Sweeping rungs to find a passing cell.** 1.00× is the gate basis; 0.50× is a follow-on for
  clearers only (§7), never an alternative arm for failures.

---

## §6 — Gate (binary)

| Verdict | Trigger |
|---|---|
| **RESOLVED-CLEARER-SURVIVES** | ≥1 of the 4 cells: bust ≤ 3.0% ∧ P(pass) ≥ 50%, controls C1–C4 green |
| **FALSIFIED** | All 4 cells miss (bust > 3.0% or P(pass) < 50%), controls green |
| **AMBIGUOUS** | Controls C1–C4 not all green; **or** a decisive cell lands in (3.0%, 3.2%] (single n-doubling re-run of that cell only); **or** a B-cell lands **materially above** its published figure (>+0.30pp), which is a harness-defect signal per §2.2 and voids that cell rather than producing a finding |

No criterion above moves after any number is seen.

---

## §7 — Controls, follow-ons, and K accounting

**Controls — all green before any verdict is read:**

- **C1 — published-figure reproduction.** The harness must reproduce the published **2-leg continuous**
  cells at both tiers: T-50K **1.06%**, MFFU-50K **0.96%** (±0.15pp). Establishes the harness scores
  the same thing the band study did.
- **C2 — standing anchor.** `Tradeify_Select_100K` 2-leg at 1.00× reproduces **4.74%** (±0.15pp).
- **C3 — geometry attestation.** `dd_lock_offset_usd = 1_000_000.0` recorded per cell in the run
  artifact; `core/firm_rules.py` still ships `100` after the run (`git diff` empty).
- **C4 — realized-stack disclosure.** Each cell's log prints its `cap_alloc`, per-leg `reserve_cap`,
  realized stacks, and aggregate-vs-cap — so an unrealizable cell cannot be scored silently.

**Pre-committed follow-on (separate run, NOT part of this verdict):** any cell that clears at 1.00×
owes the **both-halves regime gate + worker-attested bootstrap-95th** before any downstream use,
per `regime_robustness_gate.md` and the parent band study's §7(7). The deployed **0.50×** diagnostic
runs in that same follow-on. **A clear here is not usable until that rider lands.**

**K accounting: no new discovery K.** The candidate book is pre-existing (Class-S candidate #1), the
gate is ratified and cited, the tier set is frozen at two, and the allocation space is collapsed to
one pre-registered rule. This is **re-verification of an impeached published figure**, not a search.
Should the operator later want unscored tiers, that is a new look with its own pre-reg and K.

---

## §8 — What a clear licenses (and does not)

A `RESOLVED-CLEARER-SURVIVES` verdict means **one thing**: at least one book shape the integer rail
can actually instantiate clears Part A at that tier on the full panel. It does **not**:

- discharge the prop-portfolio **§4 falsifier** — that requires the frozen **$100K×4** set (§5);
- survive as usable evidence without the pre-committed regime rider (§7);
- authorize a **cap re-allocation** — a B-cell clear is conditional on an allocation Q-CAPALLOC-2
  declined, and adopting it needs its own ADR;
- authorize buying a 50K eval, switching tiers, or any `LEG_MAP`, rail, sizing, or spend change —
  all require an amending ADR **and** a separate operator GO;
- bear on the live `Tradeify_Select_100K` account, which realizes 2-leg at 79/80 exactly as deployed
  and is untouched by every cell here.

Given that this brief's motivating arithmetic impeaches a figure the 11-08 clause rests on, **any
clear should be adversarially reviewed before it is cited downstream** — and so should the control
block, not only the verdict.

---

## §9 — Operator sign-off

**SIGNED / FROZEN: 2026-08-02 / JA** — operator approval in-session, verbatim: *"signed, run the four
cells"*, following *"yes, author the scoring pre-reg with that selection rule"* which approved §2.1
before this brief was authored. Freeze is in effect from this commit; the body is **no longer
amendable in place** (Trap #12). Any change from here closes this pre-reg and opens a fresh one.

- [x] **§2.1 selection rule accepted** — locked-proportional + exactly one max-MYM re-allocated split
      per tier (T-50K 29/11, MFFU-50K 39/11); no re-selection if it fails. *(Approved before
      authoring — the rule was fixed by the operator, not chosen by the author after seeing the
      allocation space.)*
- [x] **§2 tier set accepted as frozen at two** — Bulenox/BluSky out of scope, needing their own pre-reg.
- [x] **§4's split prior accepted** — B expected to clear (weak evidence); A direction deliberately
      unpredicted.
- [x] **§8 accepted** — a clear admits nothing, discharges no falsifier, and authorizes no purchase,
      tier change, or allocation change.

**Upstream-staleness check executed at signature (2026-08-02):** `origin/main` was 4 commits ahead of
this branch's merge-base at resume. Diffed — all four are housekeeping (SESSIONS.md rolled into the
2026-Q3 LTM archive, sentinel prereg name-matching fix, dispatch table sync). **No premise of this
run is touched:** no change to the §4 falsifier status, the band-rescore clearers (1.06% / 0.96%), or
the quantization question. Recorded because the 2026-07-24 incident — a §4 discharge written 36
minutes after `main` withdrew it — is the dated reason this check exists.

**Author's recommendation: sign, and run the four cells once.** The measurement is cheap (four
full-panel MCs on committed panels, $0, no K), the harness and its attested geometry already exist,
and the question is load-bearing — the 11-08 demotion-clause defeat currently rests on a book
configuration the execution layer cannot instantiate. The A-cells are the ones that matter and
nothing in the estate predicts them.

---

## §10 — Audit hooks (runnable)

**Hook 1 — freeze precedes execution.**
```bash
git log -1 --format=%ci -- docs/briefs/pre-registration/2026-08-02-sub100k-realizable-book-scoring-prereg.md
```
**Hook 2 — the motivating arithmetic reproduces (both its controls must MATCH).**
```bash
python lab/analysis/c1/band_quantization_2026-08-02/run_band_quantization.py
```
**Hook 3 — the frozen gate thresholds are untouched.**
```bash
rg -n "3\.0%|50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head
```
**Hook 4 — the published figures under test are the corrected ones.**
```bash
rg -n "1\.06%|0\.96%" lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md | head
```
**Hook 5 — production geometry constant NOT edited.**
```bash
git diff --stat HEAD -- core/firm_rules.py
rg -n "dd_lock_offset_usd" core/firm_rules.py | head
```
**Hook 6 — no cap re-allocation smuggled into the live rail.**
```bash
rg -n "cap_alloc" ops/c1_rail/c1_sizing_host_reference.py
```
**Hook 7 — exactly four gating cells in the artifact (no sweep).**
```bash
python -c "import json,sys; d=json.load(open(sys.argv[1])); print(len(d.get('cells',{})))"
```
**Hook 8 — lock untouched.**
```bash
python scripts/validate_params.py && git diff --stat HEAD -- core/ ops/c1_rail/c1_sizing_host_reference.py
```

---

## Verification

```bash
python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" docs/briefs/pre-registration/2026-08-02-sub100k-realizable-book-scoring-prereg.md --type inquire
python scripts/check_status_consistency.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-02 | Initial authoring. Successor to the 2026-07-24 band study on integer-realization grounds. Selection rule operator-approved before authoring; §2.2 records that the gate is contract-blind, which is why the B-cells double as reproduction checks rather than independent arms | Claude Code (Opus 5) |
