# Gate audit — composite-closure deletion — 2026-07-24

**Trigger:** regret on deletion (INQHIORI §6.2) — premise re-examined against production this session
**Loop context:** ICT top-down framework (Q-ICT-CASCADE-1), corpus at `lab/archive/ict_cascade_2026-06-18/`
**Status:** worked example **RETRACTED** (premise not substantiated); granularity criterion **retained as precaution**, re-anchored on the real 2026-07-17 CFD instance. No §5 permitted-list change from this incident.

## What the gate was claimed to have done

- **D-test alleged (implicit, never written):** *"Did the framework, as a unit, clear its bar?"*
- **Alleged deletion:** the entire ICT top-down construct (Weekly / Daily / 1H / 1M) in one composite action.
- **Alleged defect:** one test logged, four deletions executed — a 3-to-1 granularity gap — with Weekly and Daily removed as untested collateral of a composite verdict.

## What production shows (Rule 0, 2026-07-24)

The claim does not survive contact with the corpus. The ICT construct was **not** closed as a composite. Q-ICT-CASCADE-1 closed **per-layer**, each layer under its own pre-registered gate and a joint **M=65** DSR/PBO multiplicity ledger — the opposite of "one test, four deletions."

| Layer | Verdict | Logged test (anchor) |
|---|---|---|
| LIB | foundation OK | orientation fixture → standard-ICT ratified (`TEST_PLAN.md` §7.A B1) |
| **W** (Weekly) | **RESOLVED** | structure-only 0.5571, block-CI [0.5242, 0.5901] lb>0.50, stationary halves 0.547/0.567, eff_N 910, own best-of-K max-stat permutation B=10000 (`PREREG-W.md`; `TEST_PLAN.md` cont.7) — routes to path-independent confirmation, **not deploy** |
| **D** (Daily) | **SSL bear-FVG RESOLVED / BSL + both pools FALSIFIED** | SSL.fvg 0.795 > base 0.712, stationary; base-rate null + selectivity (`PREREG-D.md`; `TEST_PLAN.md` cont.8) — single-panel, not deploy |
| 1H | **FALSIFIED** | prem→down 0.4725 / disc→up 0.5430 straddle 0.5 after 9-cell penalty (`CLOSURE-1H-FALSIFIED.md`) |
| 1M | **INSUFFICIENT-N** | n=0 (0/247 fills), single-regime ~2-day 1m wall (`CLOSURE-1M-INSUFFICIENT-N.md`) |

Net (`CLOSURE-1M` §4): *"no layer licenses a deployable edge."*

Three factual corrections follow:

1. **W and D were individually tested and given logged verdicts** (RESOLVED / side-split), recorded in the `TEST_PLAN.md` Progress Ledger, the per-layer `PREREG-W/D.md`, and the `CLOSURE-1M` §4 cascade table. They are **not** untested residuals. (What is literally absent is a standalone `CLOSURE-W/D.md` file — `TEST_PLAN.md` §9 marks those **optional** — a documentation-completeness nit, not an untested deletion.)
2. **Multiplicity was applied**, not omitted. `DSR_PBO_LEDGER.md` books a joint family **M=65** (42 best-of-K/grid + 3 n-throttle + 20 LOCK knobs), ratified pre-data 2026-06-18. The "best-of-4-timeframes, no multiplicity accounting" framing is false.
3. **The date is wrong.** No ICT run exists on 2026-07-23 (git window + `docs/SESSIONS.md`). The corpus is 2026-06-18/19; archived 2026-07-12 (`lab/CATALOG.md`).

So the 3-to-1 gap the audit exists to flag **did not occur**. The founding regret rests on a misremembering of a per-layer cascade as a composite closure.

## Criterion disposition

- **Old D-test (alleged):** "Did the framework, as a unit, clear its bar?" — this composite D-test was never applied; the cascade applied four layer-level tests.
- **The granularity principle is sound but not sourced here.** "A verdict licenses deletion only at its own granularity" is valid in the abstract, and it is **already instantiated** by the 2026-07-17 CFD-estate gate audit (`docs/notes/audits/2026-07-17_gate_cfd-estate-classwide-delete.md`): *class-wide deletion requires per-file consumer enumeration; may fire only per-file where that enumeration is empty.* Same rule, real instance. Anchor the principle there.
- **No §5 permitted-list addition from this incident.** The INQHIORI §5 permitted list is unchanged; a criterion cannot be promoted from an incident that did not happen (E1/E2 threshold not met — no dated cost, and the founding event is retracted, not a firing).

## Real residual (recorded so it is not re-litigated)

The only genuine loose thread: the **W-RESOLVED and D-SSL-RESOLVED** sides are single-instrument (US500), mostly-single-regime belt findings that `CLOSURE-1M` §4/§5 routed to *"path-independent confirmation, not deploy."* That confirmation was never registered as a Forward question (`docs/methodology/observation_routing.md`) and was not pursued when the line was archived. **This is defensible research triage, not a gate defect** — the cascade found no deployable edge and the 1M execution layer is dead on the canonical 1m feed (0/247 fills, F8 data wall). Named here; not opened. See the Q-ICT-1 disposition.

## Cross-references

- **Corpus:** `lab/archive/ict_cascade_2026-06-18/` — `TEST_PLAN.md`, `DSR_PBO_LEDGER.md`, `CLOSURE-1H-FALSIFIED.md`, `CLOSURE-1M-INSUFFICIENT-N.md`
- **Governing (corrected citations):** INQHIORI §4 (D logs its test), §5 (relevance test + forbidden/permitted D-tests), **§6.2** (Audit on regret → write-target `docs/notes/audits/…`). *Not* §12 (§12 is Cross-references).
- **Real instance of the granularity principle:** `docs/notes/audits/2026-07-17_gate_cfd-estate-classwide-delete.md`
- **Follow-on:** Q-ICT-1 → **MOOT** — `docs/briefs/closures/Q-ICT-1-closure-moot.md` (its motivating "ungated residual" is refuted: W was gated to RESOLVED under M=65). Q-ARCH-1 stays closed absent independent motivation.
- **Skew resolved (2026-07-24):** this audit and the 2026-07-17 CFD audit were relocated from the drift-revived `docs/methodology/gate_audits/` to the canon/adjudicated live target `docs/notes/audits/YYYY-MM-DD_gate_<slug>.md` (INQHIORI §6.2/§12; operator adjudication 2026-07-10, `docs/governance/deletion_ledger.md` commit `032cd64`). The `docs/methodology/gate_audits/` dir had been re-created as drift by the 2026-07-17 CFD commit against that standing decision, and is removed.
