# Q-MCLTAS-1 — MCL TAS settlement-window δ-extraction probe (scoping)

**Status:** `CLOSED-FALSIFIED` (2026-08-11) — Stage 0a+0b run on operator authorization; **Wall B fires**.
[`closure`](closures/Q-MCLTAS-1-closure-falsified.md) · [`Stage 0 RESULTS`](../../lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md).
Probe **never run** — the two free pre-stages establish it is unfundable before design. $0 / K=0.
⚠ **§7 Stage 0b's premise was wrong** (it assumed a committed 2023 MCL cache that is not on disk);
repaired at execution by substituting the committed *measured* σ surface — see closure §4.
**Authored:** 2026-08-11
**Authors:** Joshua + Claude Code
**Parent:** [`Q-TNEC-ENV-1` closure](closures/Q-TNEC-ENV-1-closure.md) item (b), RULED 2026-08-11/JA — *"the direction re-opens **only** through a completed δ-extraction probe"*
**Prior:** [`R8` gold-fix δ-extraction](../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md) `SCREEN-FAIL` (the shape-analogous completed probe) · `BE3`/`SFX-1` fade-scoped kills · [`F1`/MOC](2026-07-27-f1-moc-imbalance-mym-ruling.md) circular-probe precedent
**Parent cheap falsifier:** [`_cheap_falsifier_mcl_tas_probe_2026-08-11_LOG.md`](../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_mcl_tas_probe_2026-08-11_LOG.md) → **`KILL-PENDING-σ`**
**Loop:** Inquire — scoping frozen; **operator decision unpaid**
**Spend:** $0 · K=0 · Cap not claimed

---

## §0 — Rule 0 reads (verified 2026-08-11, worktree clean at `4e2339f`)

| Path | Anchor | What it grounds |
|---|---|---|
| [`Q-TNEC-ENV-1` closure](closures/Q-TNEC-ENV-1-closure.md) | `f949b81` 2026-08-11 | the ruling that re-opened the direction; the "full intake chain" sequencing note |
| [`N-2026-08-11-daily-auction-settlement-MCL.md`](../notes/notice/N-2026-08-11-daily-auction-settlement-MCL.md) | census entry, PREREG F6 | the four 1a clauses; the δ=`null` finding; the sign-laundering caveat |
| [envelope `PREREG.md`](../../lab/archive/tnec_envelope_compile_2026-08/PREREG.md) §F3/F4/F5 | FROZEN 2026-08-10 | RT $2.90 PRIMARY; `COST_LAW_MULTIPLE` 4.0; MCL committed `N=251` |
| [`DELTA_EXTRACTION_R8.md`](../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md) | 2026-08-10 `SCREEN-FAIL` | the probe template **and** the adverse prior — admissibility split, informed-flow signature |
| [`strategy_harvest.md`](../methodology/strategy_harvest.md) §1 Req 2/4/5 | canonical procedure | δ-extraction probe is the Req-2 relief valve, and it **costs data spend + K** |
| [`rejected_candidates.md`](../rejected_candidates.md) F1/MOC entry | rejected 2026-07-27 | what makes a probe route *circular*, and that circularity is a bar |
| [`ops/instruments/MCL.md`](../../ops/instruments/MCL.md) | 2026-08-11 entry | `#C2` standing posture: geometry ≠ edge; N-EDGE stays `U` |

**Gitignore pre-flight:** no Pine, no vendor CSV, and no gitignored constant is read or cited. Every
number below traces to a committed markdown/JSON file or to the falsifier script in this repo.

---

## §1 — Context

The 2026-08-11 ruling re-opened the MCL TAS direction **narrowly**: BE3's kill was a *fade-program*
design law, not a TNEC limb, so a TNEC-limb-scored TAS candidate is not barred — but *"No probe, no
candidate."* The [2026-08-11 Block 1 re-run](../../ops/instruments/MCL.md) then scored the cell
`P U U P P P` = `SHAPE-UNSCREENABLE`, with **EM1, EM2 and the Req-5 cost-law all blocked on the same
single input: δ is `null`.** This brief scopes the one act that could supply it.

**It does not open the probe.** Per `lesson_run_cheap_falsifier_before_authoring` the falsifier ran
**first**, parent-side, and it fired — so the honest scoping output is a *staged design whose first
two stages are free and can kill*, plus a plain statement that the probe is very likely unfundable.

Pre-Q gate:
  **D** — "just measure the settlement window and see" (deleted: launders direction, spends K, and
  the magnitude wall says the answer is already known)
  **S** — two independent walls, each with a $0 test, ordered cheapest-first
  **A** — the committed 2023 MCL cache and CME's free public schedule

---

## §2 — Prior art / lineage

- **`R8` gold-fix δ-extraction** (2026-08-10, `SCREEN-FAIL`) — the shape-analogous *completed* probe:
  same mechanism family (benchmark-execution window), same method (published-table δ extraction, $0,
  K=0), same admissibility split. Its scope clause is metals-only, so it is a **strong prior on this
  cell, not a bar over it** — as the census entry already states.
- **`H-FBEIA-1` CL-EIA** `SCREEN-FAIL` — the only CL-family cohort δ in the estate, **−1.16 bp**,
  wrong-signed. First confirmed instance of the informed-flow signature.
- **`F1`/MOC-imbalance on MYM** (rejected 2026-07-27) — the circularity precedent. Its δ-extraction
  route was ruled circular *because it needed the gated data*. This cell's route was recorded as
  non-circular on the strength of free CME TAS volumes; §4 tests whether that non-circularity
  survives the **sign** requirement, which volume alone does not address.
- **`BE1`** — *"constraint carries neither sign nor level; direction laundered from price."* The
  named failure mode this brief's §5 exists to prevent.
- `lesson_metric_cohort_provenance_binding` — fired on the falsifier's own bp-space comparison; the
  repair is Stage 0b.

---

## §3 — Question

**Q-MCLTAS-1:** Can a causal-public, non-laundered per-event δ for CME CL settlement-window
(14:28–14:30 ET) mandated flow be obtained at all — and if obtained, does the magnitude the Req-5
cost-law demands sit anywhere within the range this estate's evidence supports?

*(Symptom-only rephrase holds: it names the missing input and the wall, not a construct, a window,
or a filter.)*

---

## §4 — Falsifiable hypothesis (H-MCLTAS-1)

**H-MCLTAS-1:** A δ-extraction probe for this cell is **fundable** — i.e. **both** (A) a free or
already-entitled, **signed**, **price-exogenous** imbalance source exists, **and** (B) the δ the
Req-5 hurdle demands is within the range of causal-public effects the evidence supports.

**Reject H (FALSIFIED) if either limb fails:**
- **Wall A — circularity.** No free/already-entitled source is both *signed* and *exogenous to the
  window's own price*. ⇒ `STOP-CIRCULAR`, same class as F1/MOC.
- **Wall B — magnitude.** After σ-pinning (Stage 0b), the required δ still exceeds the estate's
  causal-public ceiling **in cohort-bound δ/σ units** at the most generous admissible basis.
  ⇒ `STOP-UNREACHABLE`.

**Accept H (RESOLVED) only if** both limbs clear, at which point the output is **not a candidate** —
it is a licence to author a G0 freeze and request a costed operator GO.

**Current standing:** Wall B **fires on the record as it stands** — required δ is **14.87 bp** at the
2023 panel basis (**4.63×** the 3.21 bp ceiling) and **9.67 bp** at an implausible $120 oil
(**3.01×**), surviving the forbidden bare-commission ablation (**3.04×**). Wall A is **unverified**
and is the load-bearing unknown.

---

## §5 — Forbidden moves

- **Reading the sign off the settlement-window price action.** This is the single most tempting move,
  because it is the *only* signal that is unambiguously free — and it is BE1's kill verbatim. A
  construct that does this is not a weaker version of the probe; it is a different, already-dead thing.
- **Transplanting R8's gold-fix δ (1.32–3.21 bp) into this cell.** Acutely tempting: the extraction
  work is done and sitting one directory away. Refused under harvest **Req 2** (cross-instrument
  transplant inadmissible, in both directions — as the MGC entry itself states about EURUSD).
- **Quoting the DISCLOSURE bare-commission basis ($1.90 RT ⇒ 7.6 ticks) as the hurdle.** F3 freezes
  slip=1 as PRIMARY. Named because it is the one available move that *materially* lowers the wall —
  and the ablation shows it still fails at 3.04×, so taking it buys a weaker verdict for nothing.
- **Deepening the stop to shrink the required R.** 11.6 ticks against a 40-tick stop is 0.29R instead
  of 0.58R — but the required **δ in ticks is unchanged**, and the bp comparison is untouched. This
  is cosmetic relief on the wrong axis.
- **Re-scoping to a spread expression to obtain a sign.** Front-vs-deferred *does* carry an ex-ante
  signed direction — which is exactly why it is tempting. Barred here: the ENV-1 closure §6.4.1 rules
  any spread-framed envelope a **new campaign**, not a re-run, and `SFX-1` (settlement + GSCI-roll) is
  already `DEAD`.
- **Treating a completed probe as a candidate.** The ruling licenses a *probe*; the full intake chain
  (dedup, EM verdict string, Req 1–5) still runs afterward, per the closure's sequencing note.
- **Patching `SHAPE-UNSCREENABLE` to PASS once any number exists.** Req 4's never-patch rule binds:
  the number must be *admissible*, not merely present.

---

## §6 — Gate criteria

| Verdict | Trigger | Disposition |
|---|---|---|
| `STOP-CIRCULAR` | Stage 0a enumerates the candidate sign-sources and none is jointly free/entitled **∧** signed **∧** price-exogenous | Close FALSIFIED; register the cell in `rejected_candidates.md` under the **F1/MOC circular-probe class**; re-proposal bar = a named signed source, not a re-read |
| `STOP-UNREACHABLE` | Stage 0a clears, but after Stage 0b's σ-pin the required δ still exceeds the estate causal-public ceiling in **δ/σ** units at the most generous admissible basis | Close FALSIFIED on magnitude; re-proposal bar = a published post-hoc-free cohort δ ≥ the 4× hurdle, mirroring R8's bar |
| `RESOLVED` | Both walls clear **and** Stage 1's literature sweep either supplies an admissible cohort δ **or** establishes that only an in-house extraction can | Author G0 freeze + `K_intrinsic` declaration; request costed operator GO. **Still not a candidate** |
| `AMBIGUOUS-HOLD` | Stage 0a clears but the sign source is *entitled-but-costed* (e.g. TAS instrument quotes in the databento feed) rather than free | Hold; the cost estimate becomes an operator budget decision, not a methodology one |

**Pre-registered before any data touches analysis.** Stage 0b reads the 2023 cache for a **dispersion
statistic only** — no PnL, no direction, no selection — which is why it is K=0; if that scope widens
by even one directional read, this gate is void and a G0 is owed first.

---

## §7 — Staged execution plan (cheapest-first; stages 0a/0b/1 are all $0 · K=0)

- **Stage 0a — sign-source enumeration ($0, K=0, no data).** Enumerate every candidate exogenous
  signed source for CL settlement-window flow and score each on three columns: *free/entitled?*
  *signed (net, not gross)?* *exogenous to the window's own price?* Candidates to score include at
  minimum: CME published TAS volume (expected: free, **unsigned** — the decisive check), the TAS
  instrument's own quoted offset in `GLBX.MDP3` (expected: signed and exogenous, but **entitled-costed**,
  not free), daily OI change (free, coarse, daily), and any published exchange imbalance print.
  **Empty intersection ⇒ `STOP-CIRCULAR`, and the brief closes here for $0.** This stage most likely
  fires; it is first for that reason.
- **Stage 0b — σ-pin on the committed 2023 cache ($0, K=0).** Measure the realized σ of the
  14:28–14:30 ET window on the existing MCL 1m cache. Dispersion only. Converts the falsifier's
  bp-space comparison into cohort-bound δ/σ units and either confirms `STOP-UNREACHABLE` or reopens
  Wall B. Repairs `lesson_metric_cohort_provenance_binding` against the falsifier's own arithmetic.
- **Stage 1 — literature δ sweep, R8-shaped ($0, K=0).** Targeted search for a published cohort δ on
  CL/energy settlement-window or TAS flow with a **decomposable** table (the R8 requirement — the
  informed/public split must be separable, or the number is inadmissible whatever its size). Prior:
  low hit rate; the census already reported none. Free, and it is the only route that satisfies Req 2
  without spending K.
- **Stage 2 — in-house δ extraction (COSTED · SPENDS K · NOT AUTHORIZED BY THIS BRIEF).** Reachable
  only if 0a and 0b both clear and Stage 1 is dry. Requires its own G0 freeze, a `K_intrinsic`
  declaration, a databento cost dry-run, and a separate operator GO. Deliberately left unscoped —
  scoping it now would imply a licence the falsifier says should not be granted.

---

## §8 — Verdict pre-registration

§6's table **is** the pre-registration for stages 0a/0b/1 (all $0/K=0, no market-data selection
surface). Stage 2 requires a separate frozen `PREREG_G0` in its own **earlier** commit before any
run — Rule 8.7, and the sentinel's `PREREG-SAMECOMMIT` check will flag a same-commit freeze.

---

## §9 — Closure record format

`docs/briefs/closures/Q-MCLTAS-1-closure-<verdict>.md`, carrying the typed Iterate block
(`check_closure_disposition.py` enforces it) and, on either STOP branch, the
`rejected_candidates.md` registry row with its re-proposal bar.

---

## §10 — Audit hooks (runnable)

```bash
# 1. The falsifier reproduces, and the two gap figures are unchanged.
python lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_mcl_tas_probe_2026-08-11.py | grep -E "Gap at"
# Expected: 4.63x at the panel basis, 3.01x at the most generous basis.

# 2. The frozen cost basis this brief consumes has not moved (would void the falsifier).
grep -n "commission_per_side=0.95\|COST_LAW_MULTIPLE" \
  lab/archive/tnec_envelope_compile_2026-08/PREREG.md
# Expected: F3 names 0.95/side, slip_ticks=1 PRIMARY, multiple 4.0 imported.

# 3. The parent ruling still reads CONFIRMED-narrow (this brief is void if it is vacated).
grep -n "CONFIRMED — narrow\|No probe, no candidate" \
  docs/briefs/closures/Q-TNEC-ENV-1-closure.md
# Expected: both present.

# 4. No probe has been silently opened — no manifest, no MCL campaign dir.
ls discovery_manifests/ | grep -i "mcl\|tas" || echo "no MCL/TAS manifest — correct"
ls lab/analysis/c1/ | grep -i "mcltas" || echo "no campaign dir — correct"

# 5. R8's family scope still excludes Energy (if it widens, this cell is barred, not scoped).
grep -n "venue-legal metals set" \
  lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md
# Expected: the GC/MGC/SI/SIL scope clause — Energy outside it.

# 6. The MCL ledger still records N-EDGE = U (no probe result has leaked into it).
grep -n "N-ACT  N-SURV N-EDGE" -A1 ops/instruments/MCL.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/Q-MCLTAS-1-tas-settlement-delta-extraction-probe-scoping.md --type inquire
python scripts/check_status_consistency.py
python scripts/check_falsifier_reachability.py
python lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_mcl_tas_probe_2026-08-11.py
```

---

## Pre-Lock Checklist

- [x] §0 paths read and anchored
- [x] §3 passes the symptom-only rephrase test
- [x] §4 hypothesis binary; both limbs have numeric or enumerable triggers
- [x] §5 forbidden moves genuinely tempting (transplant, disclosure-basis, spread re-scope)
- [x] §6 gates have specific triggers
- [x] §10 audit hooks runnable
- [ ] **Operator decision: run Stage 0a/0b, or close now on the falsifier** ← unpaid
