# Avenue A Route B — generate→confirm checklist (runnable) — **WITHDRAWN 2026-08-24**

> ⚠ **Withdrawn 2026-08-24.** The governing ADR, [`2026-08-05-avenue-a-generate-confirm-route`](../adr/2026-08-05-avenue-a-generate-confirm-route.md),
> is now `Superseded` in full by [`2026-08-24-sourcing-phase-channel-retirement`](../adr/2026-08-24-sourcing-phase-channel-retirement.md) — ground: 0/4 campaigns, across the mechanism's entire life, ever reached the confirm stage. Per the note below ("if the ADR ever reverts to `Proposed`/`Withdrawn`, this file is a draft playbook again and authorizes no pull"), this checklist now authorizes **no pull, no G0 freeze, no campaign**. Re-entry requires a fresh ADR under corrected design (a redesigned promotion floor — the diagnosed flaw, per `2026-08-08-edge-cohort-correction-and-necessity-retarget.md`), not a revival of this checklist as written. The body below is left unedited (dated-decision integrity) as a historical/reference playbook only.

# Avenue A Route B — generate→confirm checklist (runnable)

**Status:** checklist for [`ADR 2026-08-05-avenue-a-generate-confirm-route`](../adr/2026-08-05-avenue-a-generate-confirm-route.md).  
**In force:** only while that ADR is `Accepted` — it was Accepted 2026-08-05, so this checklist is live. If the ADR ever reverts to `Proposed`/`Withdrawn`, this file is a draft playbook again and authorizes no pull.  
**Companion to:** Avenue A Route A (survivor-tied) — unchanged; use Route A when a named survivor owns the question.

This is the formalization of: *generate a hypothesis from order-flow exploration → lock a confirmatory test → score once on reserved same-instrument OOS / other-regime data.*

---

## 0. Preconditions (all must be true)

- [ ] ADR `2026-08-05-avenue-a-generate-confirm-route` Status = `Accepted` (else STOP — Route A only)
- [ ] Instrument + mechanism cell consulted via `scripts/instrument_profiles.py` (re-proposal bars named)
- [ ] Dedup attestation against `rejected_candidates.md` / instrument DEAD list
- [ ] a4 category-split fork not in scope
- [ ] Horizon floor for any *tradeable* claim: **≥ 5 s** (rail latency); shorter horizons only as pre-registered non-tradeable diagnostics
- [ ] No ES→MNQ lead-lag feature family in the catalogue

---

## Stage G — Generate (hypothesis only)

### G0 — Freeze the exploration charter (commit before any explore pull)

Commit a pre-registration (or Stage-G section of a campaign prereg) naming **all** of:

| Field | Requirement |
|---|---|
| Instrument / symbology | e.g. `MNQ.v.0` continuous; parent vs micro rule stated |
| Schema ladder | Coarsest-first, e.g. `tbbo` → `mbp-10` → `mbo`; escalation only via pre-registered fail clause |
| **EXPLORATION window** | Closed interval; must not overlap CONFIRM |
| **CONFIRM window** | Closed interval; **reserved now**; no exploration score may use it |
| Feature catalogue | Frozen list of families/cells (each cell = feature × horizon × side rule); this list size → **K_intrinsic** |
| Flicker / cleaning rules | Pre-registered (e.g. imbalance flicker filter) |
| Promotion rule to "candidate" | Exact statistic + threshold on EXPLORATION only (e.g. sign + CI / placebo limbs) |
| Cost ceiling | `estimate` + `--max-cost`; operator GO |

**Hard rule:** after G0 is committed, the catalogue and windows do not grow. New cells = new campaign.

### G1 — Cost dry-run + operator GO (explore pull)

```bash
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
  --symbols <SYM> --stype <STYPE> --schema <SCHEMA> \
  --start <EXPLORATION_START> --end <EXPLORATION_END>
```

- [ ] Estimate recorded in the prereg amendment log
- [ ] Operator GO for **this schema × window only**
- [ ] Pull (or cache hit) only after GO

### G2 — Run exploration on EXPLORATION only

- [ ] Score **every** catalogue cell (or log explicit skips with reason — skipped cells still count toward K if they were available to be chosen)
- [ ] Emit a **candidate list** (may be empty) — IDs, exact feature definition, EXPLORATION metrics
- [ ] **Do not** read CONFIRM timestamps, files, or aggregates

### G3 — Stage G disposition

| Outcome | Next |
|---|---|
| 0 candidates | `STOP` — channel empty at this catalogue/window; board write; K disclosed |
| ≥1 candidates | Proceed to Stage C for **one** pre-chosen candidate, or a pre-registered multi-confirm budget of **M** candidates — M frozen at G0, and its per-candidate confirm threshold multiplicity-adjusted per C0. Choosing among candidates **after** G2 counts in K |

Exploration results are **not** edges, seeds, or watchlist gates.

---

## Stage C — Confirm (admission limb)

### C0 — Freeze the confirmatory PREREG (commit before any CONFIRM score)

For the chosen candidate, commit a confirmatory pre-registration that copies the feature **byte-faithfully** from G2 and names:

| Field | Requirement |
|---|---|
| Hypothesis H | Falsifiable; same instrument |
| CONFIRM window | Exact reserved interval from G0 |
| Statistic + gates | Identical limbs to promotion rule, or a stricter pre-registered confirm bar |
| Placebo / bootstrap | Seed + block rule frozen |
| `K_intrinsic` | = number of exploration cells examined (within-search); `K_banked` disclosed not gated |
| **Confirm-budget M + multiplicity bar** | M = candidates this campaign will confirm (default **1**). If **M > 1**, the per-candidate confirm threshold is **Bonferroni/Holm-adjusted for M** (or an equivalently stricter pre-registered bar), stated numerically here before any CONFIRM score |
| VOID-POWER | Minimum N / coverage; what to report if underpowered |
| Forbidden moves | No retune; no window edit; no outcome-laundering into ORB filters if MNQ F2 applies |

**Ordering trap:** if any CONFIRM metric was computed before this commit, the confirm is void — open a new campaign with a fresh holdout.

**Why M is priced (added on Accept, 2026-08-05).** `K_intrinsic` accounts for selection *within the exploration search*; it does not account for taking **M independent shots at the confirm bar**. Confirming M candidates at the unadjusted promotion threshold makes "at least one clears" scale with M — reproducing the exact generate-winner→confirm-pass laundering Route B exists to prevent, one stage later and behind a "pre-registered" label. M is therefore frozen at G0 (it cannot grow after seeing G2's candidate list) and its threshold adjusted here. A campaign that wants more shots opens a new campaign with a fresh holdout, not a larger M.

### C1 — Cost dry-run + operator GO (confirm pull / run)

- [ ] Estimate for CONFIRM window (may be $0 inside entitlement)
- [ ] Operator GO for confirm **run** (distinct from explore GO)
- [ ] Reuse cache only if it is a strict subset of an already-GO'd request

### C2 — Single confirmatory run

- [ ] One run; discharges exactly one pre-registered verdict branch
- [ ] No threshold sweep, no alternate horizon, no "also try the sibling cell"

### C3 — Verdict → harvest / STOP

| Verdict | Disposition |
|---|---|
| `RESOLVED` | Candidate becomes a **seed** eligible for normal harvest / Stage-7+ path — **not** auto-deployed |
| `FALSIFIED` | DEAD-list the candidate; exploration win was window luck or noise |
| `VOID-*` | Report honesty limb; do not re-cut CONFIRM; new campaign if retry |

Board write owed every branch (instrument ledger, SESSIONS, CATALOG/manifest as applicable).

---

## Schema escalation (optional, pre-registered only)

Escalate EXPLORATION schema only if G0 named:

> "If no catalogue cell clears the Stage-G promotion rule on schema S, escalate once to S' on the **same** EXPLORATION window."

Each escalation is either:
- pre-counted in K as its own cell block, or
- a new campaign.

Never escalate on CONFIRM after a fail.

---

## Worked minimal example (MNQ, illustrative — not authorized)

| | Example freeze |
|---|---|
| Schema | `tbbo` first |
| EXPLORATION | second half of free 1y `tbbo` window (e.g. last 6 months) |
| CONFIRM | first half of that same 1y window (reserved; older regime slice) |
| Catalogue | 6 pre-named imbalance / microprice / depth-proxy cells × 2 horizons ≥5 s → K_intrinsic = 12 |
| Route | B only after ADR Accept + two operator GOs |

*(Prefer Default #1's 2010–2018 / 2019+ split when the schema is free that far — `ohlcv` always; order-flow usually is not.)*

---

## Anti-patterns (instant void)

1. Screen → write prereg → "confirm" on a slice you already ranked during the screen  
2. Confirm pass → add a filter → re-score CONFIRM  
3. K=1 after looking at 20 cells  
4. Running Route B while the ADR is not `Accepted`  
5. Calling Stage G a watchlist overlay or ORB gate (use Route A + F2 discipline for survivor monitoring)  
6. Confirming M > 1 candidates at the unadjusted threshold and reporting whichever cleared (C0 multiplicity bar), or growing M after seeing G2's candidate list

---

## Audit hooks

```bash
# ADR must be Accepted before any Route B pull
rg -n '^\*\*Status:\*\*' docs/adr/2026-08-05-avenue-a-generate-confirm-route.md

# Confirm prereg commit must predate confirm RESULTS
git log --format='%h %ci %s' -- <path-to-confirm-PREREG.md> <path-to-RESULTS.md>

# CONFIRM window must appear in G0 freeze
rg -n "CONFIRM|EXPLORATION" <path-to-G0-prereg.md>

# Multi-confirm budget M and its multiplicity adjustment are frozen in the confirm PREREG
rg -n "confirm-budget|Bonferroni|Holm|M = " <path-to-confirm-PREREG.md>
# expect: M stated numerically; if M > 1, an adjusted per-candidate threshold alongside it
```
