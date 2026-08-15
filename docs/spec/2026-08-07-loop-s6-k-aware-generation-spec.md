# SPEC S6: K-aware generation

Status: CODE_LANDED · schema live in `lab/discovery/admission_schema.py` +
`register_search open --admission-file` (lane default `mechanism-first`) · 2026-08-07 ·
authorizes nothing ($0 · K=0) · **gate not yet RESOLVED** — RESOLVED needs the first
campaign under the schema (corridor-compliant open **or** refuse at $0/K=0 with the
refusal logged) · depends: — (parallel)
Objective: Make the ratified corridor and the DSR-cap arithmetic executable at
campaign-open — a candidate outside the corridor, or whose demonstrable band is empty at
its catalogue size, is refused before any spend.

Steps:
1. Encode the eval mechanism-shape screen (EM0–EM5, `RATIFIED` 2026-08-06; +D1/D2 where
   `MNQDTL-1` is the target) as an admission schema consumed by `register_search.py` at
   open — refusal is machine-generated, not reviewer-caught.
2. Pre-spend check at open: DSR Cap vs catalogue size (Cap crosses at K=4 — catalogue-K
   wall) and confirm-power ≥ 0.50 (`axis_screen.py`); empty band → refuse at $0/K=0.
3. Exploration stays free on frozen EXPLORATION windows (Route B); K is spent only at
   CONFIRM under the existing PREREG discipline.

Gate: RESOLVED if the first campaign under the schema either opens corridor-compliant or
is refused at $0/K=0 with the refusal logged (cheaper honest kills are the win); FALSIFIED
if a campaign opens outside the corridor — or with an empty band at its catalogue size —
without the schema refusing it.
Boundary: no threshold edits mid-campaign · CONFIRM windows untouched by exploration ·
K-banks stay disclosure-not-gate (ADR 2026-08-04) — this spec adds refusals, never a
new bank cap.
Reads (at HEAD `a6a5fe6` 2026-08-07): [EM screen](2026-08-05-eval-mechanism-shape-screen.md)
(RATIFIED 2026-08-06) · [MNQDTL-1](2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md)
(PROPOSED) · `lab/discovery/register_search.py` · `lab/research_utils/axis_screen.py` ·
`lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md`
Owner: EM screen + [K-disclosure ADR](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md);
new code lands in `register_search.py`'s open path.
