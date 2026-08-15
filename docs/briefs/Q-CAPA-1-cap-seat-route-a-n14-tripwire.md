# Q-CAPA-1 — Cap-seat Route A after N14: forward tripwire, or hold Cap?

**Status:** `CLOSED` — `RESOLVED` 2026-08-06 ([`closure`](closures/Q-CAPA-1-closure-resolved.md)); Cap seat **spent**; tripwire **registered companion** (docs-only — [`ADR 2026-08-06`](../adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md))
**Authored:** 2026-08-06
**Closed:** 2026-08-06
**Authors:** Joshua + Cursor (Composer); Rule-0 + cheap falsifier parent-side; Cap-spend GO same day
**Parent question:** N14 / `MNQFLOW-1` re-aimed Iterate (watchlist + forward tripwire named, not wired) · catalogue K-wall Route A preference · `Q-MSCHAN-1` salvage (survivor-tied path only — **not** its breakout-vs-failure framing)
**Sub-questions opened:** Phase-0 `CHARTER-CLEARS` → Cap-spend GO → PREREG `022c17d` → RUN `RESOLVED` (W5) → wiring GO discharged as companion registration ADR
**Loop:** Inquire-phase Pre-Q — closure gates whether the standing MNQ Cap-seat / single Route A discovery cell is spent on an N14-native **outcome-free forward tripwire**, or correctly **held**
**Artifact path:** `docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md`
**Spend by authoring:** $0 · K=0 · no manifest · nothing armed · no pull

> **Cheap falsifier (parent-side, before lock — discharged this session):**
>
> 1. N14 stands: Δ = **−0.009367**, CI excludes 0, placebo p_emp **0.000**, n=255 — watchlist only ([`RESULTS`](../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md) @ `be6b94e`).
> 2. Level-proximity discriminator chain **STOPPED** (operator B/1): `MNQPROX-1` W6 + `MNQPROX-2` VOID-POWER (`n_paired=15`) — no MNQPROX-3 ([`PHASE0`](../../lab/analysis/c1/mnq_orb_level_proximity_tod_2026-08-06/PHASE0.md) @ `c820c12`).
> 3. Catalogue wall: Route B ≤ **3** cells; arithmetic **favours Route A** (K=1, floor 0.650, headroom 0.350) ([`RESULTS`](../../lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) @ `87b0547`).
> 4. Avenue A Route A (survivor-tied) live; Route B `Accepted` but **not** the vehicle here ([`ADR`](../adr/2026-08-05-avenue-a-generate-confirm-route.md) @ `b0427fd`).
> 5. Blind order-flow inadmissible; survivor-tied re-aim cleared condition 3 ([ruling §7](../notes/2026-08-05-order-flow-probe-governance-question.md) @ `a7dde66`).
> 6. Estate still carries **Cap seat unspent** as the protected single discovery cell language (SESSIONS / MNQ session log) — under [`ADR 2026-08-04`](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) `K_banked` discloses and does **not** gate; this brief treats Cap seat as the **operator-reserved K_intrinsic=1 Route A slot**, not a resurrected summed-K scarcity claim.
>
> **Nothing here authorizes a pull, a manifest, or Cap spend.** Phase-0 below is charter-only until operator GO.

---

## §0 — Rule 0 reads (verified 2026-08-06)

| Path | Anchor | What it grounds |
|---|---|---|
| [`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md`](../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md) | `be6b94e` 2026-08-05 | **N14** numbers; FM-1; W1 opens nothing; Iterate names **watchlist + forward tripwire** companion to PF-CUSUM (baseline PF **1.1691**, floor **1.0855**, `block_size=2`); stop rule forbids outcome joins and gate conversion |
| [`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md`](../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md) | `2c1ff11`+ freeze lineage | S1–S7, FM-1…FM-8, Avenue A triple, K=0 reasoning for the diagnostic cell |
| [`lab/analysis/c1/mnq_orb_level_proximity_tod_2026-08-06/PHASE0.md`](../../lab/analysis/c1/mnq_orb_level_proximity_tod_2026-08-06/PHASE0.md) | `c820c12` 2026-08-06 | PROX-2 VOID-POWER; operator B/1 STOP on discriminator chain |
| [`lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md`](../../lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) | `87b0547` 2026-08-05 | Route B catalogue ≤3; **Route A favoured**; PROX named as owed successor — **superseded** by PROX Phase-0 kill (do not re-open that cell) |
| [`docs/adr/2026-08-05-avenue-a-generate-confirm-route.md`](../adr/2026-08-05-avenue-a-generate-confirm-route.md) | `b0427fd` 2026-08-05 | Route A unchanged; Route B admitted with Stage G/C; blind admission barred |
| [`docs/methodology/avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md) | `b0427fd` | Checklist; ≥5 s horizon for *tradeable* claims; no ES→MNQ lead-lag |
| [`docs/notes/2026-08-05-order-flow-probe-governance-question.md`](../notes/2026-08-05-order-flow-probe-governance-question.md) | `a7dde66` | Blind probe inadmissible; survivor-tied clears condition 3 |
| [`docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md`](Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md) | intake note 2026-08-05 | Salvage: two-stage licensing, ≥5 s, flicker filter, no ES lead-lag. **⚠ Do not import** its “breakouts vs failures” reformulation — that is MNQ **F2 GUARD** / FM-1 |
| [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) N14 · N15 · F2 GUARD | `c820c12` (N14 B/1 amend) | F2 GUARD; Cap/session language; DEAD PROX-2 row |
| [`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) | `2ef7405` | `K_eff = K_intrinsic`; bank disclosure |

**Data / spend:** none at authoring. Parent TBBO cache from N14 S1 may be reused later **only** under a separate operator GO (cache reuse ≠ entitlement expansion — N14 precedent).

---

## §1 — Context & motivation

`MNQFLOW-1` (re-aimed) produced the estate’s first Avenue A–cleared order-flow measurement: at ORB-MNQ-1’s own triggers, L1 size asymmetry signed toward the break is **against** the break (N14). Disposition was explicit — **opens nothing**; deliverable = watchlist + **forward tripwire** candidate beside PF-CUSUM, which only fires *after* decay is paid in realized P&L.

The free discriminator that would have asked “ORB-specific vs generic level?” is **power-dead** (PROX-1 W6, PROX-2 VOID-POWER). Catalogue arithmetic still favours **Route A** over a multi-cell Route B campaign. The Cap seat remains the operator’s protected single discovery cell. The honest next question is not another proximity cell and not a blind L3 screen — it is whether N14’s standing tripwire charter is **real enough to spend Cap on**, under Route A and FM-1, or whether Cap should stay held.

---

## §2 — Prior art / lineage

- **N14 / `MNQFLOW-1` re-aimed** — `RESOLVED` (W1); K_intrinsic=0 diagnostic; Iterate STOP for that thread; tripwire named not wired (`be6b94e`).
- **`MNQPROX-1` / `MNQPROX-2`** — W6 then VOID-POWER; discriminator STOP B/1 (`c820c12`) — **closed path**.
- **Catalogue K wall** — Route B ≤3; Route A favoured; its “owe PROX” Iterate line is **moot** (`87b0547`).
- **Avenue A ADR + checklist** — Route A default for survivor-tied; Route B needs G0≤3 cells + two GOs (`b0427fd`).
- **Order-flow ruling 2026-08-05** — blind barred; survivor-tied cleared (`a7dde66`).
- **`Q-MSCHAN-1`** — `DRAFTED — NOT OPENED`; salvage list transferable **except** breakout-vs-failure framing (F2).
- **`MNQBASE-1`** — intake dry STOP; new sourcing channel still owed — Cap spend here is **not** that channel unless the tripwire itself graduates (it should not under FM-1).
- **ORB-MNQ-1** — lifecycle `CANDIDATE @ 1.00×`, PARKED; Tradeify payability FALSIFIED; still the named survivor Route A ties to.
- **Family K ADR** — bank discloses; does not gate Cap-seat language into old scarcity arithmetic (`2ef7405`).

---

## §3 — Question (Q-CAPA-1)

**Symptom-only:** Cap seat sits unspent; N14’s against-break L1 signature is measured but only watchlisted; PF-CUSUM still has no pre-P&L companion; the proximity discriminator that was supposed to refine N14 is dead.

**Q-CAPA-1:** Does pre-touch L1 asymmetry `A` at ORB-MNQ-1’s frozen triggers carry **forward**, **outcome-free** information that can act as a Cap-admissible Route A tripwire companion to PF-CUSUM — or is Cap correctly held with N14 left as disclosure-only watchlist?

The question does **not** presuppose wiring into live decay automation, a filter on entries, MBP-10, or spending Cap without Phase-0 + GO.

---

## §4 — Falsifiable hypothesis (H-CAPA-1)

**Falsifier (binary):** Cap is spent on this Route A cell only if the accept limbs below all fire on a frozen PREREG; otherwise Cap is held (reject / VOID / AMBIGUOUS-without-spend).

**H-CAPA-1:** On the N14 event set (or a pre-registered subset), a single frozen function of pre-touch `A` (and/or its short forward path in L1 state over horizon `H ≥ 5 s`, never joining trade R / win / MFE / MAE) separates a pre-registered “stress” class from ToD-matched controls with CI excluding 0 **and** beating a within-session placebo at the frozen limb — under Avenue A Route A, `K_intrinsic = 1` if Cap is spent.

**Reject H-CAPA-1 if:** primary CI includes 0, **or** |stat| ≤ placebo p95, **or** Phase-0 projects VOID-POWER / VOID-COVERAGE before Cap spend, **or** the only passing constructions require outcome joins or ORB win/loss labels → Cap **held**; N14 stays disclosure watchlist.

**Accept H-CAPA-1 if:** frozen limbs clear on the Cap-spend cell → Cap may be marked spent on this Route A cell; tripwire remains **candidate** (wiring to PF-CUSUM / live monitors = separate operator GO — INTEGRATE packet, not auto-wire).

**Ambiguous-hold if:** power clears but halves disagree on sign, **or** effect is significant yet smaller than a pre-registered minimal economically interpretable L1 move (freeze as ticks/contracts of L1, not Sharpe) → ITERATE with dated re-test; Cap not spent until resolved.

**Pre-registered expectation:** **Reject / Cap held** — N14’s effect is tiny (~0.07 contracts at median L1 7) and contemporaneous; forward tripwire power is the unlikely branch. Recorded so a null is a discharged prediction, not a surprise.

---

## §5 — Forbidden moves

- **Re-opening MNQPROX / editing τ or S4a(ii)** — discriminator STOP is operator B/1; FM-6/FM-7 on that freeze.
- **Joining ORB outcomes (R, win/loss, MFE/MAE) to `A`** — FM-1 / MNQ **F2 GUARD**; the MSCHAN “breakouts vs failures” reformulation is **explicitly barred** here even though it was named as a survivor-tied salvage path elsewhere.
- **Converting a positive into a fifth ORB conditioning gate or entry filter** — N14 stop rule; fresh K-bound axis + GO required, not this brief’s INTEGRATE default.
- **Route B multi-cell catalogue “while we’re in the book”** — catalogue wall; Cap seat is a **single** Route A cell (`K_intrinsic=1`), not a generate screen.
- **MBP-10 / MBO escalation without fail-clause + GO** — N14 sign-off listed these as still requiring their own decision; coarsest schema first (`tbbo` reuse).
- **Spending Cap / opening a manifest before Phase-0 charter clears and operator GO** — FM-5 class.
- **Treating watchlist registration as already wiring the tripwire** — N14 Iterate: candidate companion; wiring is separate.
- **Instrument-shopping to MYM/M2K to “preserve Cap”** — needs non-K justification (standing bar).
- **Quietly rewriting N14 as ORB-specific after PROX died** — caveat stands as disclosure (B/1).

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | H-CAPA-1 accept limbs all fire on the frozen Cap-spend cell | `INTEGRATE — Cap seat marked spent on this Route A cell; board write; tripwire stays candidate — wiring GO separate` |
| `FALSIFIED` | H-CAPA-1 reject limbs (incl. Phase-0 VOID before spend) | `STOP — Cap held; N14 disclosure watchlist only; re-proposal needs new survivor-tied feature family, not A-threshold retune` |
| `AMBIGUOUS-HOLD` | Power OK but halves disagree **or** below minimal L1 magnitude floor | `ITERATE — dated packet; Cap not spent until discharge` |
| `VOID-POWER` / `VOID-COVERAGE` (Phase-0) | Projected n / coverage below frozen floors **before** Cap spend | `STOP — Cap held; same re-proposal bar as FALSIFIED` |

---

## §7 — Execution plan

- **Phase 0 — Charter only ($0, no Cap spend, no manifest).** **DONE 2026-08-06** — [`PHASE0.md`](../../lab/archive/mnq_capa_n14_tripwire_2026-08-06/PHASE0.md) verdict **`CHARTER-CLEARS`**. Frozen: forward twin of N14 — mean signed `A` on `[t, t+60s)` at the N14 event set vs same controls; stress class = ORB triggers (no A-threshold subclass); `K_intrinsic=1` if Cap spent; magnitude floor 0.05 contracts @ L1 median 7 (‖Δ‖ ≥ 0.00714); N14 quote cache is pre-touch only (forward pull still GO-gated).
- **Phase 1 — Operator GO** on Cap spend + PREREG freeze. **DONE 2026-08-06** — operator affirmed Phase-0 charter (*"affirm charter, commit, then proceed with next steps"*). Cap seat not marked spent until accept limbs fire.
- **Phase 2 — PREREG** in `lab/archive/mnq_capa_n14_tripwire_2026-08-06/`; freeze before any forward-window quote; tests green before quotes.
- **Phase 3 — Single run → RESULTS → closure** per §9; board writes (STATE, MNQ.md, SESSIONS, CATALOG, Cap-seat status line).

---

## §8 — Verdict pre-registration

**Not yet frozen.** ~~Phase-0 charter is landed (`CHARTER-CLEARS`); Cap-spend PREREG still requires operator GO.~~ **Superseded 2026-08-06:** Cap-spend GO issued; PREREG frozen at **`022c17d`**; run `RESOLVED` — see closure.

Pre-registration commit hash: `022c17d`  
Pre-registration date: 2026-08-06

---

## §9 — Closure record format

On gate fire: `docs/briefs/closures/Q-CAPA-1-closure-<verdict>.md` with mandatory typed `## Iterate` block discharging §6. No `recommendation.md` unless a separate wiring/PROMOTE ADR is opened (out of scope here).

---

## §10 — Audit hooks

```bash
# N14 still opens nothing / tripwire named
rg -n "forward tripwire|opens nothing|FM-1" lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md

# PROX discriminator STOP (no Cap path through proximity)
rg -n "VOID-POWER-anticipated|B/1|no MNQPROX-3" lab/analysis/c1/mnq_orb_level_proximity_tod_2026-08-06/PHASE0.md ops/instruments/MNQ.md

# This brief forbids outcome joins and PROX reopen
rg -n "F2 GUARD|breakouts vs failures|MNQPROX|Cap held" docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md

# Route A preference still on record
rg -n "favours Route A|Route A" lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md

# No Cap spend without GO (expect no new mnq capa manifest until Phase-1)
ls discovery_manifests/*capa* 2>/dev/null; ls discovery_manifests/*n14trip* 2>/dev/null
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md --type inquire
```

---

## Pre-Lock Checklist

- [x] §0 paths read and anchored
- [x] §3 symptom-only (Cap idle + tripwire untested + PROX dead)
- [x] §4 falsifiable with Cap held as reject branch
- [x] §5 tempting moves (PROX reopen, F2 laundering, Route B catalogue, auto-wire)
- [x] §6 binary triggers + typed dispositions
- [x] §8 deferred until Phase-0 + GO (explicit)
- [x] §10 runnable hooks
- [x] Phase-0 charter landed (`CHARTER-CLEARS`) — Cap-spend GO issued 2026-08-06
- [x] `check_brief.py` PASS
- [x] Operator affirm Phase-0 charter (Cap-spend GO)
- [x] Cap-spend RUN `RESOLVED` — Cap seat spent; closure filed
