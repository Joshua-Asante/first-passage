# Q-MCLTAS-1 — closure: `FALSIFIED` (Wall B magnitude; STOP-UNREACHABLE)

**Verdict:** `FALSIFIED` · 2026-08-11 · **$0.00 · K=0 · no manifest · no pull · no market data read**
**Scoping brief:** [`Q-MCLTAS-1`](../Q-MCLTAS-1-tas-settlement-delta-extraction-probe-scoping.md) (§6 gate pre-registered before either stage ran)
**Results:** [`_probe_stage0_RESULTS_2026-08-11.md`](../../../lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md) ·
[Wall-B falsifier](../../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_mcl_tas_probe_2026-08-11_LOG.md)
**Parent:** [`Q-TNEC-ENV-1` closure](Q-TNEC-ENV-1-closure.md) item (b), RULED 2026-08-11/JA — *"the direction re-opens only through a completed δ-extraction probe."*
**Live effect:** none. No candidate proposed, admitted, scored, or licensed. Harvest Req 1–5, DSR-at-K, N-SURV MC and the regime gate are untouched and unweakened. No `core/` / Pine / allocation / `dd_protection` / rail change.

---

## 1. Verdict against the frozen gate (brief §6)

| Wall | Trigger | Actual | Fired? |
|---|---|---|---|
| A — `STOP-CIRCULAR` | no source jointly free/entitled ∧ signed ∧ price-exogenous | intersection over **free** sources EMPTY; one **entitled-costed** route survives (unverified) ⇒ `AMBIGUOUS-HOLD` | — |
| **B — `STOP-UNREACHABLE`** | required δ still exceeds the estate causal-public ceiling in **δ/σ** units at the most generous admissible basis | **3.2× at the friendliest constructible reading**, 7.0× at the defensible one | **✓** |
| `RESOLVED` | both walls clear | not reached | — |

§4 rejects H-MCLTAS-1 if **either** limb fails. **Wall B fires ⇒ FALSIFIED.**

**The probe was not run, and that is the result.** The ruling required a *completed δ-extraction
probe* before the direction could produce a candidate. The two free pre-stages establish that the
probe is unfundable before it is designed: its output would have to be a per-event δ **3.2×–7.0×**
larger than any causal-public δ this estate has ever committed, in a two-minute window, on the
instrument family where the informed-flow signature was **first** confirmed (`H-FBEIA-1`, −1.16 bp,
wrong-signed).

## 2. What the pre-registration predicted vs what happened

The brief predicted Wall A would be the likely killer (*"this stage most likely fires; it is first
for that reason"*) and that Wall B would **narrow to ~2.4×** once converted to cohort-bound δ/σ units.
**Both predictions were wrong, in opposite directions:**

- **Wall A came back weaker than predicted** — `AMBIGUOUS-HOLD`, not `STOP-CIRCULAR`, because one
  entitled-but-costed route (TAS-book order flow in `GLBX.MDP3`) survives on paper. It is unverified,
  and Wall B makes it moot.
- **Wall B came back *stronger* than predicted** — the measured floor is **3.2×**, not 2.4×, and the
  defensible reading is **7.0×**. The 2.4× rested on a GC fix-window σ **invented rather than
  measured**.

The load-bearing methodological point: the free stage that looked *most* likely to be confirmatory is
the one that moved the number, and it moved it **against** the candidate. Skipping it would have left
an optimistic figure standing as the record.

## 3. What this closure does NOT license

Reading Wall B as a kill on **MCL the instrument** (it is a design-region kill, per the ledger's
2026-08-10c precedent — the symbol stays in the L3 pool). Reading it as a kill on settlement-window
mechanisms **generally** — the arithmetic is MCL's own tick geometry against MCL's own σ, and R8's
metals-scoped bar remains separate. Treating Wall A's `AMBIGUOUS-HOLD` as a live route. Re-running
either stage's arithmetic as a re-proposal. Loosening Req 1–5, the 4× multiple, or the F3 cost basis
under cover of "necessity was screened here."

## 4. Defects found (recorded; one repaired, one not)

- **REPAIRED IN PLACE — brief-grounding defect, mine, one turn old.** §7 scoped Stage 0b against *"the
  already-committed 2023 MCL cache"*. That cache **is not on disk** (heavy artifacts gitignored and
  absent; the fade stage0 dir holds `RESULTS*` markdown only). The brief asserted its presence without
  verifying — **Known Trap #13**, *brief precision exceeds brief grounding*. Repaired by substituting
  the committed **measured σ surface**, which is strictly better (a result, not a re-derivation).
- **NOT REPAIRED — `ops/instruments/MCL.md` `k_bank_source` / cache line.** The ledger's ACTIVE section
  states *"MCL 1m cache … exists for 2023"*. It does not, in this checkout. Left as an observation for
  the operator; out of this task's touch scope, and it changes no verdict here.

## 5. Lesson candidates

**`lesson_metric_cohort_provenance_binding` — second and third firings, both inside this one probe.**
First against the falsifier's bp-space comparison (oil δ required vs gold/index δ ceiling); then
against my own *repair* of it, where the comparator σ was invented rather than measured. The lesson's
instruction was applied to the *required* side and skipped on the *comparator* side — both times.

**Candidate sharpening, not a new lesson:** *when you correct a cohort-provenance error, the correction
introduces a second cohort — bind that one too.* Below the two-incident bar as a standalone lesson;
recorded here because both firings are same-session and the existing lesson's text already covers the
general form. Watch; no new lesson filed.

---

## Iterate

- **Verdict used:** `FALSIFIED` (Wall B magnitude), STOP per brief §6
- **Model update:** the ENV-1 closure recorded MCL TAS as *"the one cell blocked on δ alone, with a
  non-circular probe route."* That reading is now **corrected in both halves**. (a) The route's
  non-circularity is real but **scoped to decay observables** — free TAS volume is gross by
  construction and can never supply a sign; the only signed route is costed. (b) More importantly, the
  cell was **never blocked on δ alone**: it was *also* blocked on a magnitude wall that no δ could
  clear, and that wall was computable at $0 without ever finding one. The general form: **"UNSCREENABLE
  on a missing input" and "unreachable even if the input arrives" are different states**, and the
  second is cheaper to test than the first is to resolve. The envelope's per-cell "must defend" numbers
  make that test mechanical for any future cell.
- **Next:** STOP
- **Routing:** STOP — no successor Q. The MCL TAS direction is closed on magnitude; registry row filed
  in [`rejected_candidates.md`](../../rejected_candidates.md) so a future dedup grep finds it in the
  registry rather than only in a campaign directory (`lesson_absence_in_known_location_is_not_absence`,
  the exact trap the MGC census entry flagged against R8).
- **Entry packet:** n/a — STOP.
- **Stop rule / re-proposal bar:** a **published, post-hoc-free cohort δ for CL/MCL settlement-window
  flow ≥ the 4× hurdle at a named venue-legal outright expression** — mirroring R8's bar. **NOT** a
  re-read of this arithmetic, a re-tune of the window or stop, the DISCLOSURE cost basis, a spread
  re-frame (that is a new campaign per ENV-1 §6.4.1), or resolution of Wall A's costed route (which
  cannot reach Wall B).
- **Board write:** `STATE.md` decision-index line + `docs/SESSIONS.md` entry + `ops/instruments/MCL.md`
  session-log cell + `rejected_candidates.md` registry row — all in this commit.

## §10 audit-hook discharge

```text
falsifier reproduces (4.63x / 3.01x bp)                    OK  _cheap_falsifier_mcl_tas_probe_2026-08-11.py
sigma-pin reproduces (7.0x / 4.2x / 3.2x delta/sigma)      OK  _probe_stage0b_sigma_pin_2026-08-11.py
F3 cost basis unmoved (0.95/side, slip=1, multiple 4.0)    OK  envelope PREREG unchanged
parent ruling still CONFIRMED-narrow                        OK  ENV-1 closure, 2 matches
no manifest / no campaign dir silently opened               OK  discovery_manifests/ clean
R8 family scope still metals-only (Energy outside)          OK  DELTA_EXTRACTION_R8.md
MCL ledger N-EDGE still U (no probe result leaked in)       OK  ledger disposition unchanged
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-11 | Closure authored on operator-authorized Stage 0a+0b run | Claude Code (Opus 5) |
