# Q-MNQSEL-1 — Does perfect selection among causal MNQ restart clocks clear EM1?

**Status:** `CLOSED-FALSIFIED` — Phase 0 RUN 2026-08-07 → C2; oracle top-1/day S3 long
**0.3998** / short **0.3984** both &lt; 0.40; STOP this universe.
**Authored:** 2026-08-07
**Closed:** 2026-08-07
**Authors:** Joshua + Cursor (Composer); plan execute after brainstorm + fable-judge of naïve window-ranking
**Parent question:** `MNQBASE-1` STOP re-proposal bar (*new sourcing channel*) · Step 1 N11 (selection, not opportunity)
**Sub-questions opened:** none — FALSIFIED does not license a feature campaign
**Loop:** Inquire-phase Pre-Q — closed at Phase 0; re-proposal = different causal candidate set
**Artifact path:** `docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md`
**Spend:** $0 · K=0 · no manifest · Cap untouched ·
[`RESULTS`](../../../lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md)

> **Cheap falsifier (parent-side, before lock — discharged this session):**
>
> 1. `Tradeify_Select_100K` geometry still matches EM §1 (`max_dd_pct=3.0`, unreachable eval lock,
>    idle=5, cap=80, cost=$0.91) — `core/firm_rules.py` @ `83b665d` (live-dict assert OK 2026-08-07).
> 2. Step-1 ceiling RESOLVED at `s=40` median **145**/day — [`RESULTS`](../../../lab/analysis/c1/mnq_event_ceiling_2026-08-04/RESULTS.md) @ `5e83949`.
> 3. EM0–EM5 `RATIFIED 2026-08-06` — [`spec`](../../spec/2026-08-05-eval-mechanism-shape-screen.md) @ `d08537a`.
> 4. `MNQBASE-1` intake-dry STOP stands; re-proposal = **new sourcing channel** — [`closure`](../closures/MNQBASE-1-closure-intake-dry.md) @ `d08537a`.
> 5. Cap seat **spent** (Q-CAPA-1) — this Phase 0 is not Cap-seat; any successor Route B is ordinary K-disclosure.
>
> **Nothing here authorizes a data run, explore GO, feature catalogue, Pine, or deployment.**

---

## §0 — Rule 0 reads (verified 2026-08-07)

| Path | Anchor | What it grounds |
|---|---|---|
| [`core/firm_rules.py`](../../../core/firm_rules.py) `Tradeify_Select_100K` | `83b665d` 2026-08-06 | Rope/target/idle/cap/cost/lock; RT cost → 1.41 pt |
| [`lab/analysis/c1/mnq_event_ceiling_2026-08-04/PREREG.md`](../../../lab/analysis/c1/mnq_event_ceiling_2026-08-04/PREREG.md) | `1eeb35c` 2026-08-04 | Greedy windows; restart-at-j+1; `G(s)=0.40·s+1.41` |
| [`lab/analysis/c1/mnq_event_ceiling_2026-08-04/RESULTS.md`](../../../lab/analysis/c1/mnq_event_ceiling_2026-08-04/RESULTS.md) | `5e83949` 2026-08-04 | N11: 145/day at s=40; selection bottleneck |
| [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](../../spec/2026-08-05-eval-mechanism-shape-screen.md) | `d08537a` 2026-08-07 | EM1–EM5; G0 application |
| [`lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md`](../../../lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md) | `d08537a` | 0.40R inversion floor |
| [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) N11 · N13 · F2 GUARD · Cap spent | `a4b36f8` 2026-08-07 | Ledger constraints; $2.00/pt |
| [`docs/briefs/closures/MNQBASE-1-closure-intake-dry.md`](../closures/MNQBASE-1-closure-intake-dry.md) | `d08537a` | STOP; new-channel bar |
| [`docs/briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md`](MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md) | `d08537a` | Parent harvest STOP lineage |
| [`lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md`](../../../lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) | `87b0547` | Successor Route B budget K≤3 (working 1–2) |
| [`docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md`](../../adr/2026-08-04-tradeify-venue-descope-eval-included.md) + Addendum | `8dffb9f` | Research admissible; Striker deploy barred |
| Phase-0 PREREG (this campaign) | freeze = introducing commit | Causal clocks; S1–S6; C1–C4 gates |

**Gitignore pre-flight.** No Pine read or cited. No Databento pull.

---

## §1 — Context & motivation

Step 1 established that MNQ is not short of independent G-sized opportunities (~145/day at a
40-pt stop). The incumbent captures ~0.24% of that ceiling. Step 2 searched published harvest
seeds and closed intake-dry (L2) with a re-proposal bar of a **new sourcing channel**, not
another OHLCV class pass. Q-OFCHAN-1 then tried a dense order-flow Route B cell and stopped on
**VOID-COVERAGE**.

The residual named by N11 — **selection** — was never bounded. A naïve reading ("rank the 145
completed windows") is look-ahead: window identity is only known after range ≥ G. The
survivable residue is to use Step 1's **restart clocks** as causal candidate entries and ask
whether **perfect** top-k selection among those clocks can clear EM1.

**Symptom (not fix):** abundant disjoint opportunity, dry harvest, failed dense OF cell, and no
measurement of whether selection value exists on a causal entry set.

---

## §2 — Prior art / lineage

- **`MNQBASE-1` Step 1** — RESOLVED; N11 selection bottleneck (`5e83949`).
- **`MNQBASE-1` Step 2** — FALSIFIED intake-dry STOP; new-channel bar (`d08537a`).
- **EM0–EM5** — ratified; EM1 ≥0.40R; EM4 weekly; no trades/day floor (`d08537a`).
- **Catalogue K wall** — Route B ≤3 cells; working 1–2 (`87b0547`).
- **`Q-OFCHAN-1`** — VOID-COVERAGE STOP; do not reopen same catalogue (`RESULTS_g2`).
- **ORB / ICT DEAD list + F2 GUARD** — thin-event ORB filters barred as laundering.
- **MNQDTL-1** — was `PROPOSED` at Phase 0 (now `RATIFIED` 2026-08-07); **out of scope** for Phase 0 (EM4 only).
- **Q-CAPA-1** — Cap seat spent; this Phase 0 does not claim it.

**Brainstorm + fable-judge (session, pre-authoring):** three universes considered —
(A) rank completed windows, (B) thin named events, (C) dense bar/OF grid. Naïve (A)
**REFUTED** as deployable selector (look-ahead). (B) inherits DEAD/F2. (C) just failed
coverage. Locked recommendation: causal restart clocks + selection-value ceiling.

---

## §3 — Question (Q-MNQSEL-1)

**Symptom-only rephrase:** We know MNQ has many independent range windows and almost no
realized entries that clear the eval shape; we do not know whether *any* take/skip rule over
causal entry times could clear the per-trade edge floor even with perfect foresight.

**Q-MNQSEL-1:** On the frozen Step-1 restart-clock candidate set at `s=40` / `G=17.41`, does
oracle top-1/day mean net R clear ≥0.40 on at least one direction arm while all-take stays
below 0.40 — establishing that selection value is the binding residual — or is even perfect
selection insufficient on this universe?

The question does **not** presuppose a feature, explore GO, Route B catalogue, MNQDTL
ratification, Pine, or deployment.

---

## §4 — Falsifiable hypothesis (H-SEL-1)

**H-SEL-1:** On at least one arm (long or short), oracle **top-1/day** mean net R ≥ **0.40**
**and** all-take mean R **&lt; 0.40** (selection is load-bearing).

**Reject H-SEL-1 if:** oracle top-1/day mean R &lt; 0.40 on **both** arms → **`FALSIFIED` /
STOP** this universe (re-proposal = different causal candidate set, not denser OF on the same
clocks, not completed-window ranking).

**Accept H-SEL-1 if:** top-1/day ≥ 0.40 on ≥1 arm **and** all-take &lt; 0.40 on that arm →
**`RESOLVED` / ITERATE** to a Route B K=1–2 feature campaign approximating the oracle
(separate GO; Cap not claimed; names no feature here).

**Surprise (not accept):** all-take ≥ 0.40 on an arm → **`SURPRISE-DIRECTION`** — direction
bias without selection; do not open a "selector" feature campaign on that arm.

**Ambiguous-hold if:** scored sessions &lt; 250 → `INSUFFICIENT-N` (should not fire on the
Step-1 panel).

Full freeze: companion [`PREREG.md`](../../../lab/archive/mnq_selection_ceiling_2026-08/PREREG.md)
§2–§4 (S1–S6 statistics; C1–C4 precedence). **Anti-tautology:** mean R of {R≥0.40} is **not**
a primary gate — under G construction a target-hit earns ≈0.40R by design.

---

## §5 — Forbidden moves

- **Ranking completed Step-1 windows / using completed-window labels as features** — look-ahead; fable-judge REFUTED.
- **Expanding `s`/`G` after seeing outcomes** — cell frozen at s=40.
- **ORB filter slices (F2 GUARD)** — Friday / Monday / OR-hi / same_bar laundering.
- **Binding MNQDTL D1/D2 into Phase 0** — was unbound/`PROPOSED` then; EM4 weekly is the cadence screen here.
- **TBBO/MBP pull, Cap-seat claim, Pine, rail, lock, `dd_protection`, lifecycle, `LEG_MAP`** — out of scope.
- **Reading Phase-0 `RESOLVED` as a candidate or edge** — ITERATE only; fresh G0 + explore GO required.
- **Re-opening Q-OFCHAN-1's catalogue** to "help" selection — FM-9 there; new campaign only.
- **Editing Step-1 PREREG/RESULTS** to rescue a FAIL.
- **Pooling long and short into one gated mean.**

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | C4 | ITERATE → Route B K=1–2 oracle-approximation campaign (docs + GO later) |
| `FALSIFIED` | C2 | STOP this universe; different candidate set to reopen |
| `AMBIGUOUS` (`INSUFFICIENT-N`) | C1 | STOP — panel too short (should not fire on Step-1 panel) |
| `SURPRISE-DIRECTION` | C3 (no C4 on other arm) | ITERATE under direction-bias framing, not selector — typed surprise, not H-SEL-1 accept |

Compose with **EM0–EM5** at any successor G0. No run authorized by this brief alone — Phase 0
runner needs a separate operator execute GO (measurement only; still $0/K=0 if using on-disk 1m).

---

## §7 — Execution plan (docs-only until GO)

1. **Done this session:** scoping brief + PREREG freeze; INDEX / CATALOG / STATE / SESSIONS / MNQ ledger mirrors.
2. **Owed under separate GO:** implement runner + unit tests **before** real bars (Step-1 pattern); run Phase 0; write RESULTS; close brief per §6.
3. **If RESOLVED:** draft successor Route B G0 (K=1–2) — not in this brief.

---

## §10 — Audit hooks (runnable)

```bash
# Brief + PREREG exist and PREREG forbids completed-window ranking:
test -f docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md
test -f lab/archive/mnq_selection_ceiling_2026-08/PREREG.md
rg -n "FM-1|restart clock|Oracle top-1/day|tautolog" lab/archive/mnq_selection_ceiling_2026-08/PREREG.md

# Geometry still matches EM / firm_rules:
python -c "import sys;sys.path.insert(0,'.');from core import firm_rules as F;r=F.FIRM_RULES['Tradeify_Select_100K'];assert r['cost_per_side_usd']==0.91;assert r['inactivity_max_idle_days']==5;assert r['max_dd_pct']==3.0;print('OK', r['dd_lock_offset_usd'])"

# check_brief well-formedness:
python scripts/check_brief.py --type inquire docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md

# No RESULTS yet (Phase 0 not run):
test ! -f lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md

# Roster + catalog pointers:
rg -n "Q-MNQSEL-1|mnq_selection_ceiling" docs/briefs/INDEX.md lab/CATALOG.md
```

---

## Amendment log (append-only)

- **2026-08-07 — OPEN.** Scoping + Phase-0 PREREG authored. No path PnL. Primary gate =
  oracle top-1/day (anti-tautology). Naïve completed-window ranking forbidden.
- **2026-08-07 — CLOSED-FALSIFIED (C2).** Operator execute GO discharged; runner + 16 tests;
  S3 long 0.3998 / short 0.3984 both &lt; 0.40; S1 ≈ −0.036 both arms; S5 ≈ 97–98 hits/day;
  S6 ≈ 99.7–99.9%. Pre-registered C4 expectation **wrong**. STOP this universe.
  [`RESULTS`](../../../lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md).
