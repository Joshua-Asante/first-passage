# Q-OFCHAN-1 — Does the order-flow channel carry a Route B–admissible L1→return cell on MNQ?

**Status:** `CLOSED — Stage-G VOID-COVERAGE` — G0 charter frozen at
[`lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md`](../../lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md);
G2 [`RESULTS_g2.md`](../../lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md) empty candidates → STOP this catalogue.
**Explore GO discharged; G2 COMPLETE 2026-08-07.** Cap seat not claimed. CONFIRM untouched.
**Authored:** 2026-08-06
**Closed:** 2026-08-07 (Stage-G coverage floor fired; re-proposal bar = new G0 / new mechanism, not retune)
**Authors:** Joshua + Cursor (Grok); Rule-0 + cheap falsifier parent-side; EM0–EM5 ratified same session
**Parent question:** `MNQBASE-1` STOP re-proposal bar (*new sourcing channel*) · `Q-MSCHAN-1` salvage under Route B (fresh Q-ID; do **not** reuse Q-MSCHAN-1)
**Sub-questions opened:** none — G2 closed empty; no C0 / confirm GO
**Loop:** Inquire-phase Pre-Q — gates whether a single pre-registered Route B cell on flicker-filtered TBBO L1 imbalance → 60s mid return clears Stage-G promotion on EXPLORATION, then (under a later confirm GO) Stage-C on the reserved CONFIRM half
**Artifact path:** `docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md`
**Spend by authoring:** $0 · K=0 · no manifest · nothing armed · no pull

> **Cheap falsifier (parent-side, before lock — discharged this session):**
>
> 1. `Tradeify_Select_100K` geometry still matches EM §1 (`max_dd_pct=3.0`, no eval lock, idle=5, cap=80, cost=$0.91) — `core/firm_rules.py` @ `83b665d` (script assert OK 2026-08-06).
> 2. Avenue A Route B ADR still `Accepted` — [`ADR`](../adr/2026-08-05-avenue-a-generate-confirm-route.md) @ `b0427fd`.
> 3. EM0–EM5 ratified this session — [`spec`](../spec/2026-08-05-eval-mechanism-shape-screen.md) Status `RATIFIED 2026-08-06`; screen is a **G0 act** (§2.0a).
> 4. Free 1y `tbbo` entitlement still the working window — [`inventory`](../notes/2026-08-04-databento-entitlement-inventory.md) @ `b82ae65`; Cap full-year estimate was $0.0000 (no new estimate required to pin ISO halves).
> 5. Cap seat is **spent** (Q-CAPA-1) — this campaign is ordinary Route B K-disclosure, **not** Cap-seat.
>
> **Nothing here authorizes explore GO, pull, confirm, Pine, or deployment.**

---

## §0 — Rule 0 reads (verified 2026-08-06)

| Path | Anchor | What it grounds |
|---|---|---|
| [`core/firm_rules.py`](../../core/firm_rules.py) `Tradeify_Select_100K` | `83b665d` 2026-08-06 | EM §1 geometry falsifier — rope/target/idle/cap/cost/lock |
| [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](../spec/2026-08-05-eval-mechanism-shape-screen.md) | ratified this session (was `87b0547`) | EM0–EM5; G0 application; §7 dispositions |
| [`docs/adr/2026-08-05-avenue-a-generate-confirm-route.md`](../adr/2026-08-05-avenue-a-generate-confirm-route.md) | `b0427fd` 2026-08-05 | Route B Accepted; Stage G/C; blind admission barred |
| [`docs/methodology/avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md) | `b0427fd` | G0 checklist; CONFIRM=older / EXPLORATION=newer worked example; M at G0 |
| [`docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md`](Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md) | `b0427fd` | Salvage: two-stage, ≥5 s, flicker (arXiv 2507.22712), no ES→MNQ lead-lag. **Do not reuse Q-ID** |
| [`docs/briefs/closures/MNQBASE-1-closure-intake-dry.md`](closures/MNQBASE-1-closure-intake-dry.md) | `5c5012c` + intercept 2026-08-06 | STOP; re-proposal bar = new sourcing channel |
| [`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md`](../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md) | `be6b94e` 2026-08-05 | MNQFLOW depth census — mandatory §0 context (median L1 thin; ties) |
| [`docs/notes/2026-08-04-databento-entitlement-inventory.md`](../notes/2026-08-04-databento-entitlement-inventory.md) | `b82ae65` 2026-08-05 | Free 1y `tbbo`; no pull this session |
| [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) N11 · N13 · N14 · N16 · F2 GUARD | `9d8dffc` 2026-08-06 | Cap spent; F2 GUARD; cadence/no-duration-cap; depth context |
| [`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) | `2ef7405` | `K_eff = K_intrinsic`; bank discloses, does not gate |

**Gitignore pre-flight.** No Pine read or cited. No Databento `pull`.

---

## §1 — Context & motivation

`MNQBASE-1` closed intake-dry with disposition STOP and a re-proposal bar of a **new sourcing channel**, not another pass over OHLCV classes. Avenue A Route B (`Accepted` 2026-08-05) is the controlled generate→confirm path that discharges entry condition (a) on `Q-MSCHAN-1` without opening that brief or licensing its blind Stage-1 form. EM0–EM5 is now ratified and binds **at G0**: shape-pruning after G2 is a K charge.

The Cap seat is already spent on a Route A tripwire (Q-CAPA-1 / N16). This brief opens the first **ordinary Route B** campaign: one pre-registered L1 imbalance → 60s mid-return cell on an RTH time-grid (not ORB-trigger-tied — that remains Route A / Cap territory), schema `tbbo` only, free-year halves frozen with CONFIRM older / EXPLORATION newer, M=1.

**Symptom (not fix):** OHLCV intake is dry; order-flow has a minimum sanctioned measurement (N14/N16) but no Route B generate→confirm charter that could admit a non-survivor-tied candidate under the ratified screen.

---

## §2 — Prior art / lineage

- **`MNQBASE-1`** — FALSIFIED intake-dry STOP; new-channel bar (`5c5012c`); T2/T6-rider/T7 reuse retired/superseded by EM §7 (2026-08-06 intercept).
- **`Q-MSCHAN-1`** — `DRAFTED — NOT OPENED`; salvage transfers; **Q-ID not reused**.
- **Avenue A Route B ADR + checklist** — Accepted; G0≤3 cells; two operator GOs (`b0427fd`).
- **EM0–EM5** — ratified 2026-08-06; catalogue wall K≤3; working budget 1–2.
- **MNQFLOW-1 / N14 + Q-CAPA-1 / N16** — Cap spent; depth census mandatory; F2 GUARD (no ORB-outcome joins).
- **Catalogue K wall** — K=1 floor 0.650 / headroom 0.350 (`87b0547`).
- **Order-flow ruling 2026-08-05** — blind admission barred; Route B confirm limb is the shape fix, not a waiver.

---

## §3 — Question (Q-OFCHAN-1)

**Symptom-only rephrase:** OHLCV sourcing on MNQ is intake-dry; the order-flow channel has depth-census context and Cap-spent Route A measurements, but no frozen Route B generate→confirm cell that could earn admission under EM0–EM5 and Avenue A without survivor-tie.

**Q-OFCHAN-1:** On a pre-registered RTH time-grid (not ORB-tied), does flicker-filtered TBBO L1 signed size imbalance predict 60-second mid returns on `MNQ.v.0` strongly enough to clear a frozen Stage-G promotion rule on EXPLORATION and — under a later confirm GO — the reserved CONFIRM half at M=1, or is the cell empty / VOID under those gates?

The question does **not** presuppose explore GO, pull, confirm, Pine, deployment, activity-week cover, Cap-seat reuse, or MBP-10/MBO escalation.

---

## §4 — Falsifiable hypothesis (H-OFCHAN-1)

**Falsifier (binary):** the cell earns Route B candidate status only if Stage-G promotion clears on EXPLORATION under the frozen G0 limbs and Stage-C clears on the reserved CONFIRM window at M=1 under a later C0 PREREG; otherwise the cell is rejected / VOID / AMBIGUOUS without admission.

**H-OFCHAN-1:** On the frozen G0 catalogue (exactly one cell: flicker-filtered L1 signed size imbalance → 60s mid return, RTH grid, `tbbo`, `MNQ.v.0`), the EXPLORATION-only promotion limbs (sign + CI excluding 0 + placebo) fire with coverage/power clear; then, under a separate confirm GO and C0 PREREG, the same limbs clear on the reserved CONFIRM window at M=1 — establishing a Route B–admissible candidate (still not a harvest admission, not a deployment).

**Reject H-OFCHAN-1 if:** Stage-G promotion fails on EXPLORATION (CI includes 0, or fails placebo, or VOID-POWER / VOID-COVERAGE), **or** Stage-C fails on CONFIRM under the C0 bar → channel cell **empty** for this catalogue; STOP or ITERATE only via a **new** campaign (new G0), not by growing the catalogue.

**Accept H-OFCHAN-1 if:** Stage-G emits the cell as candidate **and** Stage-C clears at M=1 under the frozen confirm bar → candidate recorded; harvest Req 1–5 / EM1–EM2 screening remain independent bars at construct time.

**Ambiguous-hold if:** EXPLORATION clears but halves disagree on sign, **or** effect clears limbs yet falls below a pre-registered magnitude floor in G0 → ITERATE with dated packet; CONFIRM not scored until resolved.

---

## §5 — Forbidden moves

- **Issuing explore GO / pulling / reading CONFIRM from this brief** — stop line is docs + G0 freeze only; explore GO is a separate operator act (checklist G1).
- **Reusing `Q-MSCHAN-1` or its blind Stage-1 form** — barred; fresh Q-ID required; Route B is Stage G/C, not screen-as-admission.
- **ORB-outcome conditioning / breakout-vs-failure joins** — MNQ **F2 GUARD**; Cap/Route A territory; this cell is time-grid only.
- **Claiming Cap seat** — Cap spent (Q-CAPA-1); this is ordinary Route B `K_intrinsic=1` disclosure.
- **Treating G2 / Stage-G pass as edge or admission** — candidates only; CONFIRM + harvest bars still bind.
- **Growing the catalogue after G0 / after seeing G2** — Trap #12 / checklist hard rule; new cells = new campaign.
- **EM1/EM2 patched to PASS** — SHAPE-UNSCREENABLE until a tradeable stop/R construct exists at harvest (§6 attestation).
- **Schema escalation to `mbp-10`/`mbo`** — not in this G0; needs a later campaign pre-register.
- **ES→MNQ lead-lag** — MSCHAN salvage forbid; Fassas 2021.
- **FU-1 Friday activity-week token / F2/F3 venue forks** — out of scope.
- **Pine / deployment / live wiring** — not licensed.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | G0 frozen ∧ explore GO ∧ G2 promotion PASS on EXPLORATION ∧ C0 frozen ∧ confirm GO ∧ Stage-C PASS at M=1 (identical or stricter limbs) ∧ no CONFIRM peek before C0 | `INTEGRATE` — record candidate; open harvest/construct packet under separate GO (not auto-deploy) |
| `FALSIFIED` | Stage-G fails promotion (CI/placebo) **or** Stage-C fails at M=1 under frozen bar | `STOP` — re-proposal bar: new mechanism / new G0 catalogue, not retuning this cell post-hoc |
| `AMBIGUOUS-HOLD` | VOID-POWER / VOID-COVERAGE on EXPLORATION, **or** halves disagree after CI clear, **or** below G0 magnitude floor | `ITERATE` — dated packet; do not score CONFIRM until resolved; re-test window set at closure |

**This session's gate (authoring only):** brief + G0 PREREG exist, `check_brief.py` PASS, EM attestation recorded, **explore GO explicitly unpaid**. Closure of the *empirical* question waits on GOs.

---

## §6a — EM pre-freeze attestation (binding at G0)

| Limb | Verdict | Grounds |
|---|---|---|
| **EM0** | **PASS** | Catalogue size = **1** (≤3; working budget 1–2). DSR floor 0.650 at Cap 1.0. |
| **EM1** | **SHAPE-UNSCREENABLE** | No tradeable stop / realized-R construct yet — do not patch to PASS. |
| **EM2** | **SHAPE-UNSCREENABLE** | No risk-per-trade size yet — do not patch to PASS. |
| **EM3** | **Design grounds** | Independence: single-entry cell (no pyramid / scale-in / same-signal multi-entry). Stop integrity deferred with EM1 to harvest (not claimed PASS). |
| **EM4** | **Design grounds** | RTH grid produces many candidate observation times per Mon–Fri week if harvested; idle-week failure mode is design-avoided vs clustered ORB books. |
| **EM5** | **Design grounds** | Intraday-complete / flat by envelope 16:00 ET; MNQ micro; Equity Index long-only if direction elected at harvest; S7 `MNQ1!` unoccupied (Striker withdrawn). |

Verdict string at freeze: `P U U D D D` (EM0 PASS; EM1–EM2 UNSCREENABLE; EM3–EM5 design grounds). **Not SHAPE-CLEAR** — harvest still owes EM1/EM2 evidence.

---

## §7 — Execution plan

- **Phase 0 (this session — DONE):** Rule-0 + falsifier; ratify EM; freeze G0 PREREG; board writes; handoff card.
- **Phase 1 (operator):** Explore GO → G1 `$0` estimate for EXPLORATION window → G2 on EXPLORATION only.
- **Phase 2 (operator):** If ≥1 candidate, freeze C0 confirm PREREG (M=1) → confirm GO → Stage-C on CONFIRM only.
- **Phase 3:** Closure per §6 + Iterate block; board write.

Companion handoff: [`docs/briefs/handoffs/2026-08-06-q-ofchan-1-explore-go-card.md`](handoffs/2026-08-06-q-ofchan-1-explore-go-card.md).

---

## §8 — Verdict pre-registration

Empirical §6 gates and cell definition are frozen in
[`lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md`](../../lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md)
**before any explore pull**. Pre-registration commit hash: *populated when this branch is committed*.

Pre-registration date: 2026-08-06

---

## §9 — Closure record format

On empirical gate fire: `docs/briefs/closures/Q-OFCHAN-1-closure-*.md` with mandatory typed `## Iterate` block
(INTEGRATE | ITERATE | STOP). No `recommendation.md` for non-PROMOTE verdicts.

---

## §10 — Audit hooks

```bash
# EM ratified; Route B Accepted
rg -n "RATIFIED 2026-08-06|DATE / INITIALS: 2026-08-06" docs/spec/2026-08-05-eval-mechanism-shape-screen.md
rg -n '^\*\*Status:\*\*' docs/adr/2026-08-05-avenue-a-generate-confirm-route.md

# G0 lists CONFIRM window and does not claim CONFIRM metrics
rg -n "CONFIRM|EXPLORATION" lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md

# No Cap-seat claim; schema tbbo only; M=1
rg -n "Cap seat|mbp-10|mbo|M = 1|confirm-budget" lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md

# Geometry falsifier still green
python -c "import sys; sys.path.insert(0,'core'); from firm_rules import FIRM_RULES as F; t=F['Tradeify_Select_100K']; assert t['max_dd_pct']==3.0 and t['inactivity_max_idle_days']==5; print('ok')"

# Brief discipline
python scripts/check_brief.py docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md --type inquire
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md --type inquire
# Expected: all 6 checks PASS

git log -1 --format="%h %cs" -- core/firm_rules.py docs/adr/2026-08-05-avenue-a-generate-confirm-route.md
rg -n "SHAPE-UNSCREENABLE|EM0" docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md
```
