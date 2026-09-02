# Q-MSCHAN-1 — Is sourcing exhaustion channel-specific or instrument-wide? (DISCOVERY)

**Status:** `DRAFTED — NOT OPENED` — superseded before intake by the 2026-08-05 admissibility ruling (see Supersession note below). Q-ID reserved for this historical record; a survivor-tied successor needs its own Q-ID, not reuse of this one, since the hypothesis shape differs materially.
**Authored:** 2026-08-04 (Joshua + claude.ai advisor, from the four-tool-stack research report)
**Superseded:** 2026-08-05 (before intake)
**Closed:** N/A — never opened, so no closure verdict applies
**Authors:** Joshua + claude.ai (advisor); supersession note by CC
**Parent question:** N/A (this was the parent; no forks ever opened)
**Loop:** N/A — blocked before the Inquire-phase Pre-Q could gate anything
**Artifact path:** `docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md`
**Spend by authoring:** $0 · K=0 · no manifest · nothing armed (unchanged — this brief never ran)

---

## Supersession note (2026-08-05, added at intake review)

This brief was drafted 2026-08-04, scoping a **blind** multi-family screen of the L3/order-flow
feature space on MNQ (Stage 1: included-window MBO pull, no survivor tie; Stage 2: purchased
regime-spanning window if Stage 1 clears). Before it reached intake, two things happened on
2026-08-05 that bar it as scoped:

1. **The governing gate ruled against exactly this shape.** [The 2026-08-05 admissibility
   ruling](../notes/2026-08-05-order-flow-probe-governance-question.md) held that Avenue A §6
   condition 3 — *"survivor-tied … not blind discovery"* — is a **shape requirement**, untouched by
   cost (the $0 included-window entitlement does not satisfy it), and explicitly **declined** the
   gate-widening reading that would have licensed a blind screen. This brief's Stage 1 is, by its
   own §4 wording, a blind screen ("does the never-searched L3 feature space contain sign-stable
   structure") with no survivor tie of the kind the ruling requires. Opening it as scoped would ask
   for exactly the admissibility the ruling just refused.

2. **The premise "never-searched" is no longer true.** `MNQFLOW-1` ran (as a recorded deviation, not
   a blessed result) and returned a wrong-signed null: 10-level book-size imbalance vs next-minute
   mid return, **ρ = −0.01205, p_emp 0.633**. It also produced the durable finding this brief's
   Stage 1 would have needed anyway — NQ's displayed book carries a **median 67 contracts across all
   twenty levels** (≈3.4/level), making any size-derived feature coarse by construction (525 distinct
   values in 1,167 observations, 78.1% tied). That census transfers as mandatory context to any
   successor probe on this channel, per the ruling's own §7.

3. **Data authorization does not reach this brief's Stage 1 or Stage 2.** The only order-flow pull
   authorized in the estate as of this note is the single `tbbo` pull named in the sanctioned
   re-aim's S1 (`MNQ.v.0`, 2025-08-06 → 2026-08-04, $0.0000) — see the [re-aimed
   PREREG](../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md) amendment log. This
   brief's Stage 1 feature families (multi-level OFI, depth/book-pressure imbalance, iceberg/
   replenishment) need MBO or MBP-10, and "any MBP-10 pull" is explicitly listed there as **still
   requiring its own decision** — this brief does not supply that decision.

**What survives and is salvageable, if a survivor-tied successor is ever proposed:**

- The two-stage purchase-licensing structure (Stage 1 on the included ~1-month window licenses only
  a purchase decision; Stage 2 on a purchased regime-spanning window is the only stage that can
  license procurement) — already the shape the sanctioned re-aim thread uses.
- The ≥5 s horizon floor, tied to the TV→CrossTrade webhook rail's own measured latency (sub-second
  is untradeable on this rail regardless of feature strength).
- The flicker-filter requirement on raw imbalance features (arXiv 2507.22712).
- The forbidden-move ruling out ES→MNQ lead-lag constructs (Fassas 2021: ~equal bidirectional
  information shares; "the big book leads" is unproven).
- The N11 event-ceiling framing (145–1,172 independent events/day vs ~0.24% incumbent capture) as
  the motivating fact that the bottleneck is mechanism-side, not opportunity-side — this still holds
  regardless of this brief's fate.

**Entry condition for a successor.** Either (a) an Avenue A §6 **amendment ADR** that reopens blind
discovery for this channel specifically — an operator-level act the 2026-08-05 ruling just declined,
not something a brief can self-authorize — or (b) a **reformulation as survivor-tied**, per the
ruling's own §7 pointer: a depth-shape feature that "improves or refines" an admitted survivor's
(e.g. `ORB-MNQ-1`, lifecycle `CANDIDATE @ 1.00×`, PARKED not retired) real breakouts vs its failures,
which "clears condition 3 by construction and needs no amendment." Route (b) is the cheaper and more
likely path; it is a **different hypothesis shape** from this brief's blind screen and would open
under a fresh Q-ID.

> **Update 2026-08-05 — entry condition (a) is now DISCHARGED as a reopen *path*, and this brief is
> still NOT OPENED.** [`ADR 2026-08-05-avenue-a-generate-confirm-route`](../adr/2026-08-05-avenue-a-generate-confirm-route.md)
> (`Accepted`) is the amendment condition (a) named: Avenue A §6 condition 3 now admits **Route B
> (generate→confirm)** alongside survivor-tie. Three things this does **not** do:
> 1. **It does not open this brief.** Status stays `DRAFTED — NOT OPENED`; a successor still opens
>    under a **fresh Q-ID** (the Q-ID reservation above is unchanged).
> 2. **It does not license this brief's Stage 1 as written.** Route B admits exploration that emits
>    *candidates only*, followed by a separate confirmatory PREREG on a **pre-reserved** window. This
>    brief's Stage 1 claims admission from the screen itself — that shape remains barred. A successor
>    must be re-scoped into the Stage G / Stage C split, not lifted verbatim.
> 3. **It authorizes no pull.** MBP-10/MBO remain cost-gated per stage, with their own operator GO.
>
> The salvage list above (two-stage licensing, ≥5 s horizon floor, flicker filter, no ES→MNQ
> lead-lag) transfers to any Route B successor and is now the natural input to its G0 freeze.

> **Update 2026-08-24 — entry condition (a)'s reopen path is now RETIRED, not merely discharged.**
> [`ADR 2026-08-05-avenue-a-generate-confirm-route`](../adr/2026-08-05-avenue-a-generate-confirm-route.md)
> — the amendment condition (a) named above — is now `Superseded` in full by
> [`ADR 2026-08-24 — sourcing-phase channel retirement`](../adr/2026-08-24-sourcing-phase-channel-retirement.md).
> Route B no longer exists as a live reopen path for this channel; the 2026-08-05 update above is
> historical record only. A successor to this brief now needs a **fresh ADR under corrected design**
> (§5 of the retirement ADR) before entry condition (a) can be satisfied again — not a citation to
> either the discharged-then-retired 2026-08-05 ADR or this brief's own now-superseded update block.
> This brief itself stays `DRAFTED — NOT OPENED`, unchanged.

**Disposition:** not intaken as an OPEN Inquire-phase Q. Filed here as a dormant-thread record (see
`STATE.md` §Dormant cross-session threads) so the salvage list above is not lost, mirroring the
`Q-ICT-1MEXEC-1` "DRAFTED, NOT OPENED" pattern. The original draft is preserved below, unedited
except for this note and the status header, as the historical record of what was scoped.

---

## §0 — Rule 0 reads (as drafted 2026-08-04; not re-verified for execution — this brief does not open)

- `STATE.md` — anchor: read via `git show origin/main:STATE.md` (decision index incl. MNQBASE-1 closure, K-bank ADR line)
- `docs/SESSIONS.md` — anchor: entries 2026-08-04f–j read via diff vs `origin/main`
- `CLAUDE.md` §Purpose + §Live-execution posture — anchor: `b6dc3b8` blob at `origin/main` (Addendum-narrowed de-scope wording)
- `discovery_manifests/orb_mnq_intraday_breakout.json` — anchor: working-tree diff read 2026-08-04 (manifest closure mechanics)

Anchored, body unread at authoring time — `[§0-pending content read before lock]` (moot; brief does not lock):
- `docs/briefs/programs/2026-07-24-avenue-a-microstructure-scoping.md` — anchor: `91137fb` (2026-08-03) — the qualifying feature-triple gate; this is the gate condition 3 of which barred this brief
- `docs/briefs/closures/MNQBASE-1-closure-intake-dry.md` — anchor: `5c5012c` (2026-08-04) — re-proposal bar wording
- `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` §4 — anchor: `1bafe6f` (2026-08-03) — idle guard 2026-11-08; 2-B fires at *second* audit
- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md` — anchor: `2ef7405` (2026-08-04) — K_eff = K_intrinsic, within-search only
- `.claude/skills/databento-data/SKILL.md` — anchor: `af51179` (2026-07-12) — mandatory cost dry-run before every pull
- `lab/discovery/register_search.py` — anchor: `e0bbad8` (2026-07-27) — K-ledger mechanics

---

## §1 — Context & motivation (as drafted; historical)

Five consecutive zero-seed sourcing passes; `MNQBASE-1` closed `FALSIFIED` (intake dry, at P2) with disposition STOP and a re-proposal bar of a **new sourcing channel**, never another pass over the same classes (STATE decision index 2026-08-04). Every channel searched to date is OHLCV-derived, and Mesfin ×2 (arXiv 2605.04004 / 2605.17724) independently corroborates that exhaustion: 0 of 14 standard OHLCV signal families cleared on MNQ. Meanwhile N11 says the instrument ceiling is not the constraint — 145–1,172 independent events/day vs the incumbent book's ~0.24% capture; the gap is mechanism-side. The L3/order-flow feature space (Databento GLBX.MDP3 MBO) had never been searched here at authoring time and is definitionally outside every dead channel — it is the cleanest available discriminator between "those channels are empty" and "this instrument is empty." Avenue A was already scoped 2026-07-24 with gate = qualifying feature-triple; this brief was intended as Avenue A's execution scoping. **As the Supersession note above records, condition 3 of that same gate is exactly what bars this brief's blind form, and the "never-searched" premise is now stale** — `MNQFLOW-1` ran in the interim.

**Clock relevance (as drafted):** this Q moves neither operator clock. It is not an 08-08 item — F2/F3 are venue decisions and this is a sourcing question. Its only dated consequence was to be what the 2026-11-08 harvest idle-guard reads as a sixth pass on a genuinely new channel — that consequence is now moot as scoped; a survivor-tied successor, if opened, would inherit it fresh.

---

## §2 — Prior art / lineage (as drafted; historical)

- Avenue A scoping brief (`91137fb`) — open; owns the qualifying-feature-triple gate; condition 3 is what barred this brief (see Supersession note).
- `MNQBASE-1` closure (`5c5012c`) — FALSIFIED intake-dry, STOP; this brief was meant to be the "new sourcing channel" its bar demands — still available to a survivor-tied successor.
- Harvest-intake ADR §4 (`1bafe6f`) — 11-08 idle guard; moot for this brief as scoped, live for any successor.
- Family-K ADR (`2ef7405`) — within-search K still counts; screens log trials even at $0. (Not triggered — this brief never opened, so no trial was logged against it.)
- **Added at supersession (2026-08-05):** [2026-08-05 admissibility ruling](../notes/2026-08-05-order-flow-probe-governance-question.md) — the gate that bars this brief's Stage 1 as scoped; `MNQFLOW-1` run (`docs/SESSIONS.md` 2026-08-05b) — the depth census this brief's Stage 1 would otherwise have needed to establish itself.
- External: Cont–Kukanov–Stoikov 2014 (OFI→Δprice linear; slope inversely proportional to depth — mechanically larger in thin micro books); FEDS Note 2025-11-03 (Treasury-futures corroboration); arXiv 2507.22712 (raw imbalance is flicker-sensitive; filtering required); Fassas 2021 (micro/mini information shares ~equal — **no lead-lag license**).

---

## §3 — Question (as drafted; historical — the shape a successor would need to change)

Symptom-only form (no fix baked in):

**Q-MSCHAN-1:** Five passes over OHLCV-derived channels returned zero seeds on MNQ — is that exhaustion a property of those channels, or of the instrument? Concretely: does the never-searched L3/order-flow feature space contain sign-stable structure at rail-tradeable horizons, or is it empty too?

*(A survivor-tied successor would need to rephrase this: not "does the L3 space contain structure" blind, but "does a depth-shape feature tied to an admitted survivor's breakout/failure discrimination improve or refine that survivor" — a materially different, condition-3-compliant question.)*

---

## §4 — Falsifiable hypothesis (as drafted; never pre-registered, never run)

**Two-stage by construction — and the staging is forced, not stylistic.** Databento Standard's *included* MBO history is ~1 month. One month cannot test regime robustness, which is this estate's standing bar (H1↔H2 spread gates appear throughout the corpus, and the frozen composed engine's own failure was regime-driven: 10.96% composed bust, H1 chop alone 23.64%). So a single-stage "screen → procurement GO" would either overclaim from a regime-blind window or smuggle in a history purchase before any evidence justified it. Stage 1 licenses **only the purchase**; procurement stays behind Stage 2.

**H-MSCHAN-1a (Stage 1 — included window, ~$0):** If, on a pre-registered MNQ screen of frozen feature families — multi-level OFI, microprice deviation, depth/book-pressure imbalance, signed-trade/CVD, sweep detection, iceberg/replenishment — evaluated at horizons ≥ 5 s (the webhook rail's latency floor makes sub-second untradeable) with flicker filtering, at least one family clears the Avenue A qualifying-feature-triple gate on the included window with a coherent sign, then the channel is **not obviously empty** and a regime-spanning history purchase is licensed; otherwise the channel is dead at the cheapest available test and no money is spent.

**Reject H-1a if:** 0 families clear at frozen thresholds on the included window.
**Accept H-1a if:** ≥1 family clears with coherent sign. ⚠ **Stage 1 licenses a data purchase and nothing else** — not procurement, not a candidate, not a Pine line.

**H-MSCHAN-1b (Stage 2 — purchased regime-spanning window):** If a Stage-1 survivor holds sign and its pre-registered magnitude band across **both** regime halves (H1/H2 split frozen at §8) at the pre-registered N floor, then exhaustion was channel-specific and Avenue A procurement is licensed; otherwise the L3 channel joins the dead list and the instrument-wide reading strengthens.

**Reject H-1b if:** survivor fails sign-stability or the magnitude band in either half.
**Accept H-1b if:** holds in both halves at the N floor.
**Ambiguous-hold if:** holds in both halves but N is below the floor → extend window, cost-gated.

**As the Supersession note records: H-1a as written IS a blind screen and does not survive Avenue A §6 condition 3.** This is preserved verbatim as the historical record of what was scoped, not as a live hypothesis.

---

## §5 — Forbidden moves (as drafted; historical)

- **Deep-history MBO pull before Stage 1 fires** — tempting because the included window is only ~1 month and buying history up front feels like it saves a round trip; it is peeking plus ungated spend, and it destroys the staging's entire purpose. Included window first, always; the purchase requires H-1a accept + cost dry-run + signed ceiling.
- **Reading a Stage-1 accept as a channel-works result** — tempting because it is the first non-zero signal after five dry passes; a regime-blind month licenses a purchase and nothing more. Any downstream citation of Stage 1 without Stage 2 is a misread.
- **Promoting any screening feature into a Pine/strategy candidate from this brief** — the screen licenses *procurement*, never a candidate; any strategy work needs its own Pre-Q + manifest.
- **Sub-second horizon constructs** — tempting because the OFI effect is strongest there; untradeable on TV→CrossTrade (tens-to-hundreds of ms floor). Horizons < 5 s are out of scope by construction.
- **ES→MNQ lead-lag constructs** — Fassas 2021 found ~equal bidirectional information shares; "the big book leads" is unproven and forbidden as a screen family.
- **Mid-screen instrument widening (MNQ→MES/MYM when MNQ disappoints)** — instrument-shopping prohibition stands; robustness legs only if pre-registered at freeze.
- **K-ledger bypass ("$0 screens don't bank")** — within-search selection still counts (K-bank ADR); every trial logs. (Moot here — no trial ran.)

---

## §6 — Gate criteria (never exercised — historical record only)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | H-1a accept **and** H-1b accept | `INTEGRATE — Avenue A procurement GO packet to operator` |
| `FALSIFIED (Stage 1)` | 0 families clear on the included window | `STOP — channel dead at $0; feeds the 11-08 idle-guard reading` |
| `FALSIFIED (Stage 2)` | Stage-1 survivor fails in either regime half | `STOP — L3 channel enters the dead list; same re-proposal bar; feeds 11-08` |
| `AMBIGUOUS-HOLD` | holds both halves but below N floor | `ITERATE — extend window (cost-gated, separate ceiling)` |

None of these fired; the brief was superseded before Phase 0 ran.

---

## §7–§10 (as drafted; not executed)

Preserved in the original draft's form for provenance only — Phase 0 (Rule-0 reads) never ran, no
pre-registration was committed, and no audit hooks were exercised. Omitted here to avoid implying
any of this brief's machinery is live; a successor brief authors its own §7–§10 against its own
(condition-3-compliant) hypothesis shape.

---

## Pre-Lock Checklist

- [x] Superseded before lock (2026-08-05) — never reached Pre-Lock review as scoped
- [x] Salvage list recorded above for any survivor-tied successor
- [x] Entry condition for reopening recorded above (Avenue A §6 amendment ADR, or survivor-tied reformulation under a fresh Q-ID)
- [x] `STATE.md` §Dormant cross-session threads carries the pointer (this intake session)
- [x] Q-ID `Q-MSCHAN-1` reserved for this historical record, not reused
