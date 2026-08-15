# ST-EH-1 closure — OPERATOR-STOPPED (pre-adjudication)

**Status:** `FINAL — closed 2026-07-26` (operator ruling received; manifest
`discovery_manifests/st_eh_supertrend_grid.json` closed `operator-stopped`, banking
executed **K=2** with declared **84** retained in `declared_K`).
**Campaign:** ST-EH-1 — Supertrend `ST(period,mult)` flip-only 15m, NQ/YM parents +
MNQ/MYM micros; dual-track grid per
[`2026-07-26-st-eh-1-preregistration.md`](../pre-registration/2026-07-26-st-eh-1-preregistration.md)
(STAGE-0 FROZEN, §8 GO 2026-07-26/JA).
**Stop:** operator, 2026-07-26 — "I have stopped the pulls. Supertrend is closed."
Long-panel pull halted ~100/570 chunks; **Phases 3–6 never ran.**

---

## What this closure is and is not

- **No H1/H2 verdict exists.** The pre-registration's §6 verdicts (H1-VIABLE /
  GRID-CANDIDATE / REGIME-FLAG / FALSIFIED-AT-COST / AMBIGUOUS) were never reached
  and none may ever be quoted for this campaign. Supertrend-on-index-micros remains
  **UNADJUDICATED at the 16-yr panel level** — closed by direction, not by evidence.
  (The 1-yr TV cohort read — costed coin-flip, documented in the archived handoff —
  stands as the only examined evidence and was the LOW-prior basis all along.)
- **The reserved holdout (2024-01→present) was never opened per-cell** and remains
  clean for any future campaign that wants it.
- **Re-proposal:** any future Supertrend-family proposal on these instruments must
  cite this closure, the 2026-07-21 raised bar, and bring new *mechanism* evidence
  (the four-clause form if the boundaries ADR ratifies) — not new parameters.

## What ran, and survives as infrastructure

| Asset | State |
|---|---|
| Phase-2 replication fidelity gate | **PASS all 10 checks** ([`replication_gate.md`](../../../lab/analysis/harvest/st_eh_2026-07/results/replication_gate.md)) — the Python engine is TV-parity-licensed on both micros |
| Engine + modules + 53-test suite | `lab/analysis/harvest/st_eh_2026-07/` — engine (independent-reference parity, no-lookahead), panels (`.v.0` roll detection on `instrument_id` at 1m, panama back-adjustment), stats (block bootstrap, aligned best-of-K null, DSR floor), reserved-holdout guard (adversarially tested) |
| Dual-track / reserved-holdout pattern | [`2026-07-26-regime-candidate-flag-lane.md`](../../adr/2026-07-26-regime-candidate-flag-lane.md) (`Proposed`) — survives this campaign |
| Data cache | Fidelity window (2025-06→2026-07, both micros) complete; long-panel partial (~100/570 month-chunks); all $0.00 billed |
| Methodology lessons banked | reporting-burns-holdout; guards-need-adversarial-tests; roll-alias trap; DSR-floor closed form; chunking economics |

## The K-banking question (operator ruling required)

Declared at open: **K=84** (20 cells × 2 windows × 2 symbols + 4 baselines; split
MNQ 42 / MYM 42). Executed before the stop: **2 selection-shaped looks** — the two
1-yr TV baseline panels (MNQ, MYM), examined by the parent session (handoff §1
table) and re-verified by this session's loader. **Zero of the 80 grid reads
executed** — auditable: no results artifacts exist; the IS-era parent data was
absent (pull incomplete); the grid runner never invoked; the holdout guard's
artifact checks show nothing scored.

| Ruling | MNQ family bank (closed) | MYM family bank | New-seed floor MNQ / MYM |
|---|---|---|---|
| Bank declared 84 | 1 + 42 = 43 | 0 + 42 = 42 | ~1.44 / ~1.44 — **both families closed to harvest seeds** |
| Bank executed (~1/family) | 1 + 1 = 2 | 0 + 1 = 1 | 0.98–1.06 (marginal) / **0.85 (open)** |

Adjudication mechanism: clause **2-C** of
[`2026-07-26-mechanism-counterparty-constraint-boundaries.md`](../../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md)
(`Accepted` 2026-07-26) — executed-K closure for operator-stopped campaigns under four
auditable conditions, all of which this campaign meets. Recorded conflict: the drafter
of 2-C was the session that banked the K — which is why the ruling was the operator's.

```
K-BANKING RULING: EXECUTED K = 2 (1 per family) per ADR 2026-07-26 clause 2-C
                  ("Bank executed K per 2-C, and ratify all three clauses")
DATE / INITIALS:  2026-07-26 / JA
```

**Executed as ruled.** Manifest closed via the guarded `--operator-stopped` path added
to `register_search.py` this session (10 guard tests, incl. a regression pinning the
normal p-value path byte-unchanged). Post-closure ledger state:

| Family | Bank (closed manifests) | K_eff at K_intrinsic=1 | Floor | Standing |
|---|---|---|---|---|
| MNQ | 2 (D5 1 + ST-EH-1 1) | 3 | **0.98** | open, **at the cap** — one K_intrinsic=1 seed only; any second expression fails |
| MYM | 1 (ST-EH-1) | 2 | **0.85** | open |
| 6E | 1 (fc_carry) | 2 | **0.85** | open (unaffected by this campaign) |
| GC/MGC | 3,177 | — | 2.05 | permanently dead (Req-3) |

**Split warning for future readers:** this manifest banks `K=2` as a single number
spanning **two** families; the split is **1 MNQ + 1 MYM** (see its `executed_looks`
field). Do not add 2 to either family.

## Record-keeping notes folded into this closure

- Handoff premise corrections (tooling paths, deliverable root, off-by-one trade
  counts on both CSVs) — logged in the pre-registration §1 and the 2026-07-26
  commits; another `web-advisor-confabulates` instance, caught by handoff-verify.
- The pre-reg plateau criterion ("≥6 of available adjacent cells") was
  geometrically unsatisfiable as written on a 4×5 grid; the runner scored the
  8-cell diagonal-inclusive neighbourhood, disclosed at the time. Moot for
  verdicts (none exist); recorded for template hygiene in future grid pre-regs.
- SESSIONS.md entry lands with the closing commit for 2026-07-26.
