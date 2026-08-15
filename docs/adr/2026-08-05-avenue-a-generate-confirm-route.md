# ADR 2026-08-05 — Avenue A Route B: generate→confirm for order-flow discovery

**Status:** `Accepted` — **operator Accept recorded 2026-08-05** (*"I accept the ADR"*), after a review pass that raised two findings; both are addressed in this same change (§0 anchor correction; C0 multi-confirm multiplicity bar). Route B is now in force under the checklist; Route A (survivor-tied) is unchanged. Blind screens remain barred — Route B is not "$0 = free to screen."
**Decision date:** 2026-08-05
**Authors:** Joshua (process shape) + Cursor (drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Amends-in-part:** [`docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md`](../briefs/2026-07-24-avenue-a-microstructure-scoping.md) §6 condition 3 — amended on Accept (2026-08-05) by **adding** Route B alongside survivor-tie, not replacing it. Avenue A is a brief, not an ADR, so the amendment lands as an addendum block on that brief with its frozen §6 text preserved.
**Related:** [`2026-08-05 order-flow admissibility ruling`](../notes/2026-08-05-order-flow-probe-governance-question.md) · [`Q-MSCHAN-1` (not opened)](../briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md) salvage list · [`discovery-campaign-template` Default #1](../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) · [`2026-07-26-regime-candidate-flag-lane.md`](2026-07-26-regime-candidate-flag-lane.md) · [`2026-08-04-family-k-bank-disclosure-not-gate.md`](2026-08-04-family-k-bank-disclosure-not-gate.md) · runnable checklist [`docs/methodology/avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md)
**Layer:** methodology (research rules of evidence only). No strategy parameter, allocation, `dd_protection`, lifecycle, Pine, or rail config is touched.

---

## §0 — Rule 0 reads (verified 2026-08-05)

| Source | Anchor | What it pins |
|---|---|---|
| [`docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md`](../briefs/2026-07-24-avenue-a-microstructure-scoping.md) §6 | `a7dde66` | Qualifying triple; condition 3 = survivor-tied, **not blind discovery** |
| [`docs/notes/2026-08-05-order-flow-probe-governance-question.md`](../notes/2026-08-05-order-flow-probe-governance-question.md) §7 | `a7dde66` | Blind probe INADMISSIBLE; $0 entitlement does not rewrite the *shape* limb; Avenue A unmodified; re-aim (survivor-tie) is the cheap live path |
| [`docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md`](../briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md) | `38006ae` | Entry condition (a) = this class of ADR; salvage: two-stage licensing, ≥5 s horizon, flicker filter, no ES→MNQ lead-lag |
| [`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) Default #1–4 | `a7dde66` | Temporal IS/OOS axis, K binding before p-values, universe correction, temporal-consistency battery |
| [`.claude/skills/databento-data/SKILL.md`](../../.claude/skills/databento-data/SKILL.md) | present | Estimate before pull; coarsest schema first; parent→micro proxy discipline |
| [`docs/notes/2026-08-04-databento-entitlement-inventory.md`](../notes/2026-08-04-databento-entitlement-inventory.md) | present | Free windows: `ohlcv` unlimited; `tbbo`/`trades` ~1y; `mbp-10` ~30d |

---

## §1 — Context

Avenue A §6 bars **blind** order-flow discovery as a *shape*, not as a schema: condition 3 requires a survivor tie. That bar is load-bearing — unguided screens in a tail-exhausted domain launder multiplicity. The 2026-08-05 ruling reaffirmed it when a $0 MBP-10 entitlement tempted a cost-only reading.

Separately, OHLCV sourcing on MNQ is intake-dry (`MNQBASE-1` STOP); the honest next *channel* question is whether order-flow contains structure OHLCV does not. That question cannot be asked under condition 3's current letter without either (i) tying every probe to ORB-MNQ-1 (narrow, and F2-guard constrained), or (ii) an operator amendment that reopens a **controlled** generate path.

The operator's stated clean shape (2026-08-05): **generate a hypothesis from L3/order-flow exploration, then test it once on out-of-sample / other-regime data from the same instrument** — with the confirmatory design locked before scoring.

**Decision driver (one sentence):** keep Avenue A's anti-fishing bar, but add an explicit Route B so "find then validate" is runnable under pre-registered multiplicity and a burned holdout, rather than remaining an informal temptation that either stays barred forever or happens off-book.

---

## §2 — Decision

**Decision:** On Accept, Avenue A §6 gains a **second admissible route** for order-flow / depth pulls. Route A (survivor-tied) is unchanged. **Route B (generate→confirm)** is admitted only when a campaign follows the frozen checklist in [`docs/methodology/avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md).

### Route B in one paragraph

Exploration may search a **frozen feature catalogue** on a **frozen EXPLORATION window** and may emit candidate hypotheses only. Those candidates are **not** admissible edges. Admission requires a **separate confirmatory pre-registration**, committed **before any score** on a **pre-reserved CONFIRM window** (temporal OOS / other regime on the same instrument), with **K_intrinsic** equal to the exploration search size (within-search selection), a **single confirmatory run**, and no post-peek retune. Conditions 1–2 of Avenue A (depth-shape, not fill-trivial) still bind both stages. Cost dry-run + operator GO bind each pull stage.

### What changes in Avenue A §6 (text to apply on Accept)

Replace condition 3's exclusive survivor-tie with:

> **3 — Either (Route A) survivor-tied** — improves or monitors ORB-MNQ-1 (or another admitted survivor), **or (Route B) generate→confirm** under [`avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md) — not an unguided screen that claims admission from the exploration window.

Route A's "not blind discovery" clause remains the default reading when Route B's checklist is not frozen and followed.

**Effective:** on operator Accept of this ADR (flip Status → `Accepted` and apply the Avenue A §6 wording in the same change).
**Scope:** Databento GLBX order-flow / depth discovery and monitoring pulls under Avenue A (schemas `tbbo`, `trades`, `mbp-1`, `mbp-10`, `mbo`). Does not reopen participant-category flow (a4 still kills that fork). Does not authorize spend, arming, or deployment.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo** (Route A only) | Leaves the only non-OHLCV sourcing channel permanently unreachable except via ORB-tied diagnostics; conflicts with the `MNQBASE-1` re-proposal bar ("new sourcing channel") without offering one |
| **Widen condition 3 to "$0 entitlement = free to screen"** | Rejected by the 2026-08-05 ruling: cost is not shape; would revive the exact prohibited form |
| **Full DISC-CAMP on L3 with Default #1 IS 2010–2018** | Infeasible: deep-history MBP/MBO is severe spend; free windows are recent; Default #1 remains the *confirm* temporal ideal when data exist, not a requirement that blocks Route B's free-window exploration |
| **Silent practice** (screen off-book, write PREREG after) | The failure mode this ADR exists to prevent |

---

## §4 — Falsifier (revert trigger)

**H:** Route B, when followed as written, produces confirmatory verdicts whose OOS stability matches the estate's temporal-consistency expectations for single-hypothesis seeds, without a measurable rise in "exploration winner → confirm pass → later regime death" relative to Route A / OHLCV campaigns.

**Revert trigger (either limb):**
1. **Process breach:** any Accept-era campaign claims a Route B admission while missing a frozen confirmatory PREREG that predates CONFIRM-window scores, **or** retunes after peeking at CONFIRM — → immediate superseding ADR withdrawing Route B; the offending seed is DEAD-listed, not rescued.
2. **Empirical:** within **two** completed Route B confirm campaigns that printed `RESOLVED` on CONFIRM, **both** later fail the standing temporal-consistency battery (Default #4 sign-consistency / drop-top-year) on a further reserved slice or live forward window dated in their own prereg — → supersede; Route A only.

**Revert action:** new ADR supersedes this one in full or in part; Avenue A §6 reverts to survivor-tie-only wording; checklist marked withdrawn.
**Trigger check schedule:** 2026-08-08 programme audit (process limb); after each Route B confirm closure (empirical limb).

---

## §5 — Forbidden moves

- **Claiming Route B under any status other than `Accepted`.** In force from 2026-08-05; a revert to `Proposed`/`Withdrawn` takes the checklist down with it.
- **Treating Stage G (exploration) output as an edge, seed, or watchlist gate.** Exploration emits *candidates* only.
- **Writing the confirmatory PREREG after seeing CONFIRM-window numbers.** Trap #12 at the methodology layer.
- **Burning the CONFIRM window during exploration** (any score, plot, or threshold tune that uses CONFIRM timestamps).
- **Setting K_intrinsic = 1 after a multi-cell screen.** K is the exploration catalogue size actually examined (ADR 2026-08-04 within-search rule).
- **Confirming a multi-candidate budget at the unadjusted threshold.** `K_intrinsic` prices selection *within the search*, not M independent shots at the confirm bar; M > 1 requires the Bonferroni/Holm-adjusted per-candidate threshold frozen in C0. Growing M after seeing G2's candidate list is the same move wearing a budget label.
- **Skipping estimate→max-cost** or jumping to `mbo`/`mbp-10` before a coarser schema failed a pre-registered escalation clause.
- **Participant-category / "who is trading" features** — still a4-killed.
- **ES→MNQ lead-lag constructs** — Q-MSCHAN salvage; Fassas 2021.
- **Sub-5 s horizons** as tradeable claims on the TV→CrossTrade rail (latency floor); research diagnostics may measure them only if pre-registered as non-tradeable.
- **Silent edit of Avenue A or this ADR's gates after data.** Supersede; do not patch.

---

## §6 — Consequences

### Gains
- A written path to ask whether order-flow is empty or OHLCV-empty, without pretending a screen is a pre-registration.
- Salvages Q-MSCHAN's two-stage structure under an operator-level amendment the 08-05 ruling named as the reopen condition.
- Keeps Route A cheap path for ORB-tied diagnostics (`MNQFLOW-1` shape).

### Costs / risks
- Operator attention: each Route B campaign needs two GOs (explore pull; confirm run) and honest K.
- Free-window exploration is regime-narrow; CONFIRM power may be thin — campaigns must pre-register VOID-POWER, not stretch windows after a miss.
- Temptation to treat a CONFIRM pass as deployable — still needs harvest/Stage-7+ and separate operator spend GO.

### Explicit non-licenses
- No venue registration, no rail arm, no token-trade authorization, no Striker redeploy.
- No automatic MBP-10/MBO purchase — still cost-gated per stage.

---

## §7 — Implementation (executed on Accept, 2026-08-05)

1. ~~Flip this ADR Status → `Accepted`.~~ **DONE** — operator Accept recorded in the Status line.
2. ~~Amend Avenue A §6 condition 3 with the §2 wording (addendum block on that brief; frozen historical text preserved).~~ **DONE** — addendum block on [`2026-07-24-avenue-a-microstructure-scoping.md`](../briefs/2026-07-24-avenue-a-microstructure-scoping.md); §6's frozen text untouched.
3. ~~Point `Q-MSCHAN-1` supersession note's entry condition (a) at this ADR as discharged *as a reopen path*.~~ **DONE** — entry condition (a) now names this ADR; **does not auto-open a campaign** (that brief stays `DRAFTED — NOT OPENED`, and a successor still needs a fresh Q-ID).
4. **OWED** — first campaign: operator picks instrument + schema ladder + windows via a fresh Q-ID / prereg pair under the checklist — **not** this ADR.

**Two review findings closed in the same change:** the `§0` Q-MSCHAN-1 anchor was corrected (`a7dde66` → `38006ae`; the old anchor predated the file's creation by ~11.5 h and was unverifiable), and the checklist's multi-confirm budget gained an explicit multiplicity bar (C0) — see the change history.

**If this ADR ever reverts to `Proposed`/`Withdrawn`:** the checklist authorizes no pull, and Avenue A §6's addendum block must be withdrawn in the same change.

---

## §10 — Audit hooks (runnable)

```bash
# This ADR's status (expect Accepted from 2026-08-05)
grep -n "Status" docs/adr/2026-08-05-avenue-a-generate-confirm-route.md | head -3

# Avenue A §6: frozen condition-3 text preserved AND the Route B addendum present
grep -n "Survivor-tied\|not blind discovery" docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md
grep -n "Route B\|generate→confirm" docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md
# expect: BOTH — the addendum adds a route, it does not rewrite the frozen triple

# Checklist exists and names both stages
grep -n "Stage G\|Stage C\|CONFIRM window\|EXPLORATION" docs/methodology/avenue_a_generate_confirm.md

# Multi-confirm multiplicity bar is present (review finding closed on Accept)
grep -n "Bonferroni/Holm\|Confirm-budget M" docs/methodology/avenue_a_generate_confirm.md

# Q-MSCHAN entry condition (a) now names this ADR, and the brief stays NOT OPENED
grep -n "amendment ADR" docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md
grep -n "DRAFTED — NOT OPENED" docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md

# Graph index lists this ADR as Accepted
grep -n "avenue-a-generate-confirm-route" docs/adr/INDEX.md

# §0 anchors resolve to commits that actually contain each cited file
git log -1 --format='%h %ci' 38006ae -- docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md
```

---

## Verification

```bash
python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" \
  docs/adr/2026-08-05-avenue-a-generate-confirm-route.md --type adr
python scripts/check_adr_graph.py
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-05 | Authored `Proposed` with companion checklist | Joshua (shape) + Cursor (draft) |
| 2026-08-05 | **`Proposed` → `Accepted`** (operator: *"I accept the ADR"*). §7 steps 1–3 executed: Avenue A §6 addendum block added (frozen text preserved); `Q-MSCHAN-1` entry condition (a) points here. Two review findings closed in the same change: (i) §0's `Q-MSCHAN-1` anchor corrected `a7dde66` → `38006ae` — the prior anchor predated that file's creation by ~11.5 h and could not have been read at it; (ii) checklist C0 gained an explicit **multi-confirm multiplicity bar** (M frozen at G0; Bonferroni/Holm-adjusted per-candidate threshold when M > 1), closing a gap where M unadjusted shots at the confirm bar would reproduce the generate-winner→confirm-pass laundering Route B exists to prevent. §10 hooks re-pointed from pre-Accept to post-Accept assertions. | Joshua (Accept) + CC (review + execution) |
