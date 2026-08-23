# Strategy organization gains a third axis: venue binding (book → venue edition → deployment) — `strategy-venue-binding-axis`

**Status:** `Accepted` — operator GO 2026-08-22 (the fresh GO the 2026-08-14 addendum required). Axis is standing doctrine. §7 Phase 1–3 landed 2026-08-23 (ledger live set empty); T1 already fired (S1 F2/F3 in prose) and is acknowledged, not reopened.
**Decision date:** 2026-08-05
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction + both design rulings) + Claude Code (authoring)
**Related:** [`2026-07-10-strategies-never-locked-lifecycle-governance.md`](2026-07-10-strategies-never-locked-lifecycle-governance.md) (the two existing axes — **extended, not modified**) · [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) (canonical owner of the authorization axis) · [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md) (the decision that exposed the gap) · [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) (the four-firm programme this axis serves) · [`docs/spec/2026-07-27-third-leg-target-spec.md`](../spec/2026-07-27-third-leg-target-spec.md) (a screen whose limbs this ADR re-homes) · [`2026-08-05 claim-alignment audit`](../notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md) (B3 + the 112-site premise-dead estate this axis would have prevented)
**Layer:** governance / strategy organization. **No locked parameter, allocation, `dd_protection` constant, `core/lifecycle.py` tier multiplier, Pine file, or `LEG_MAP` entry is changed by this ADR.**

---

> ⚠ **2026-08-22 reader-intercept:** operator Accepted this ADR (fresh GO). The 2026-08-14 stall note is historical. T1 remains acknowledged as already fired. §7 Phase 1–3 landed 2026-08-23 (ledger live set empty). See Addendum 2026-08-22 + Change History 2026-08-23.

## §0 — Rule 0 reads (production-source verification, all executed 2026-08-05)

| Source | Anchor (`git log -1`) | What it pins |
|---|---|---|
| `core/lifecycle.py` L30–50 | `4441c72` 2026-07-11 | `TIER_MULTIPLIER = {AUTHORIZED 1.00, WATCH-1 0.50, WATCH-2 0.25, RETIRED 0.00}`; `DEFAULT_TIER = "AUTHORIZED"`; `STRATEGY_KEYS = {Guardian, Striker, Aegis, Striker NAS100}`; `_LADDER_ORDER` demotes DOWN only; `_validate_ladder()` hard-fails at import on any multiplier change. **Read with surrounding context per the §0 sub-rule.** This is the axis this ADR must not touch — and note `STRATEGY_KEYS` is **book-level**, with no venue dimension anywhere in the module. |
| `core/dd_protection.py` | `fc14682` 2026-07-30 | `scaled_risk = BASE_RISK × DD_SCALE × lifecycle` — the risk_pct composition. Venue binding must compose *multiplicatively alongside* this, never edit it. |
| `ops/c1_rail/c1_sizing_host_reference.py` L60–99, L276–296 | `2345095` 2026-08-03 | `LEG_MAP` maps `leg_id → {leg_key, pyr_pct, dollars_per_pt, cap_alloc}`. **This is the venue-edition record that already exists but is not named as one:** `leg_key` points at the book (`"Striker"`), while `cap_alloc` (69/11) is a pure Tradeify-account fact. `reserve_cap = floor(cap_alloc / (1 + pyr_pct/100))`; halts on missing `cap_alloc` and on `cap_alloc > cap_firm`. |
| `core/firm_rules.py` | `8ec740d` 2026-08-05 | `AUTOMATION_FRIENDLY_PROP_FIRMS = {bulenox, tradeify, myfundedfutures, blusky}`; per-tier venue facts (`micro_contract_cap`, `inactivity_max_idle_days`, `cost_per_side_usd`, `max_dd_pct`). The venue-fact source this axis binds against. **No `ACTIVE_FIRM` selector exists** (deleted substrate Phase 4). |
| `docs/methodology/strategy_lifecycle.md` L14–27, L95–107 | `cdfd2f8` 2026-08-03 | "The two orthogonal axes"; the descriptor triple `<version> · LOCKED · <authorization> · <durability-source>`; the forbidden-moves column. **The descriptor has no venue slot** — the defect this ADR names. |
| [`2026-07-10-strategies-never-locked-lifecycle-governance.md`](2026-07-10-strategies-never-locked-lifecycle-governance.md) | `c99c60d` 2026-07-29 | The ratified two-axis model and its five Calls. This ADR **extends** it; §2 of that ADR is untouched. |
| [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md) §2, §6 | `01714e5` 2026-08-05 | *"Lifecycle axis NOT moved — both legs stay `AUTHORIZED · MECHANISM @ 1.00×`; venue-fit is not decay."* The prose workaround this ADR converts into structure. |

**Gitignore pre-flight.** `**/*.pine` is ignored. **No Pine source is read or cited here** and no numeric constant below derives from Pine — this decision sits entirely at the organization layer. Citation-chain mode not required.

---

## §1 — Context

Strategy organization today has two ratified axes, both venue-agnostic. Three symptoms — one measured at 112 sites, one stated by the operator, one a 1.91× sizing defect — trace to the same missing dimension: nothing in the model records *where a strategy is allowed to trade*.

### §1.1 What exists today

Strategy organization has **two ratified orthogonal axes** ([`2026-07-10`](2026-07-10-strategies-never-locked-lifecycle-governance.md)):

- **Parameter axis — `LOCKED`.** SL/TP/ATR/risk%/pyramid/session/BE/trail + Pine are immutable.
- **Authorization axis — revocable.** `CANDIDATE → AUTHORIZED → WATCH-1 → WATCH-2 → RETIRED`, multipliers `1.00 / 0.50 / 0.25 / 0.00`, plus a durability tag `{MECHANISM | SURVIVAL-ONLY}`.

Both are **venue-agnostic**. `core/lifecycle.py`'s `STRATEGY_KEYS` names four strategies and nothing else; the descriptor triple has no venue slot.

### §1.2 The gap, named by the event that exposed it

On 2026-08-04 the Tradeify venue was de-scoped as a deployment target, **evaluation included**, and both Striker legs were withdrawn from the c1 eval deployment. The ADR then had to assert, in prose:

> *"Lifecycle axis **NOT** moved — both legs stay `AUTHORIZED · MECHANISM @ 1.00×`; venue-fit is not decay."*

That sentence is correct and was the right call. **But it is a workaround for a missing axis.** The two existing axes could express *"the mechanism is sound"* (`LOCKED`) and *"it is authorized to take risk"* (`AUTHORIZED`), and had **no way at all** to express *"…but it currently has nowhere to trade."* The only structural lever available — demotion — would have been false (it asserts decay, and no decay occurred), so the ADR correctly refused it and wrote prose instead.

The cost of prose-instead-of-structure is measured, not hypothetical. The [2026-08-05 claim-alignment audit](../notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md) found **112 sites still asserting the withdrawn configuration** across 140 confirmed findings, because a deployment-state change touched no code, no lifecycle state and no schema — so nothing forced a re-read anywhere.

### §1.3 The second symptom: a book with no edition at the live venue

Stated by the operator, 2026-08-05: *"Currently we have a strategy book, but none of our available strategies are venue specific to the current active venue (Tradeify)."*

That is a true and important fact about programme state, and **the repo has nowhere to record it**. There is no artifact whose shape makes "which book entries have a Tradeify edition?" answerable, which is why the question *"find a Tradeify-shaped strategy"* had no home to be tracked in, and why a prior session's answer to *"is MNQ eligible?"* was wrong in both directions within one conversation.

### §1.4 The third symptom: venue facts leaking into book-level artifacts

The audit's **B3** is this leak in its most consequential form. `docs/spec/c1_watch_realization_multiplier_layer.md` §2 — a *normative sizing law*, i.e. a book-layer artifact — divided by `cap_firm`, an account-aggregate venue fact, while production divides by `cap_alloc`, a **per-leg venue-edition** fact. When the 2026-07-22 cap split changed the venue edition, the book-layer law had no structural reason to track it, and it silently didn't. An implementer following the declared chain reproduces **153 micros against an 80 limit (1.91×)**.

**The layer confusion caused the defect.** `cap_alloc` is a venue-edition property that was living in a book-layer document.

---

## §2 — Decision

**Adopt a third orthogonal axis — VENUE BINDING — with three named levels. Every strategy artifact belongs to exactly one level, and each level owns a disjoint class of facts.**

### §2.1 The three levels

| Level | Identity | Owns | Example |
|---|---|---|---|
| **BOOK** | `<strategy>` | The mechanism, its parameter lock, its evidence, its durability tag, its instrument family, its K bank | `Striker NAS100 v1 · LOCKED · AUTHORIZED · MECHANISM` |
| **VENUE EDITION** | `<strategy>@<firm-tier>` | Everything derived from **one venue's geometry**: contract-cap allocation, cost basis, DD/trail geometry, cadence/activity rule fit, flat deadline, instrument symbol, compliance posture — **and its own authorization state** (§2.4) | `Striker NAS100@Tradeify_Select_100K` |
| **DEPLOYMENT** | `<strategy>@<firm-tier>#<account>` | Account binding, rail slot, `leg_id`, arming state, live P&L | `…#<ACCOUNT_ID>` via `leg_id=nas100_mnq` |

**The test that decides which level a fact belongs to:** *would this fact change if the same mechanism ran at a different firm?* If yes, it is venue-edition or deeper. `cap_alloc` changes → venue edition. `SL = 1.55×ATR` does not → book.

### §2.2 What this makes expressible that was not

| Statement | Before | After |
|---|---|---|
| "Sound mechanism, nowhere to trade" | prose only | `BOOK: AUTHORIZED` + **zero live editions** |
| "Withdrawn from Tradeify, fine elsewhere" | required a false demotion, so was written as prose | `EDITION@Tradeify: WITHDRAWN`, `BOOK: AUTHORIZED` |
| "No book entry has a Tradeify edition" | unrecordable (§1.3) | an empty edition set at that tier — **directly queryable** |
| "Screen-dead at Tradeify, untested elsewhere" | conflated with book-level death | `EDITION@Tradeify: SCREEN-DEAD` (§2.4 ruling 2) |
| "This cap is a Tradeify fact" | leaked into a book-layer spec (**B3**) | edition-owned by construction |

### §2.3 The de-scope, re-expressed — the validating test

The 2026-08-04 de-scope should move **exactly one thing**. Under this axis it does:

```
BEFORE   Striker NAS100          BOOK    LOCKED · AUTHORIZED · MECHANISM @ 1.00×
         …@Tradeify_Select_100K  EDITION ACTIVE   (cap_alloc 11, MNQ1!, 16:45 ET flat)
         …#TDFYSL1006…           DEPLOY  WIRED    (leg_id nas100_mnq, dry_run=true)

AFTER    Striker NAS100          BOOK    LOCKED · AUTHORIZED · MECHANISM @ 1.00×   ← UNCHANGED
         …@Tradeify_Select_100K  EDITION WITHDRAWN — venue de-scoped 2026-08-04    ← the only move
         …#TDFYSL1006…           DEPLOY  RETIRED (rail retained, disarmed, F2)     ← follows the edition
```

**One state transition, at one level, and "venue-fit is not decay" becomes a structural property rather than a sentence someone must remember to write.**

### §2.4 The two design questions, ruled

**Ruling 1 — a venue edition carries its OWN authorization lifecycle; it does not inherit the book's.** Operator, 2026-08-05: *"It's own."*

The edition reuses the ratified vocabulary and the ratified multipliers (`core/lifecycle.py` `TIER_MULTIPLIER`, unchanged), plus **one edition-only state** the book axis does not have:

| Edition state | Meaning |
|---|---|
| `CANDIDATE` | proposed for this venue; not screened |
| `SCREENED` | passed the venue's structural screen; not deployed |
| `ACTIVE` | deployed or deployable at this venue |
| `WATCH-1 / WATCH-2` | de-risked **at this venue** (edition-local decay) |
| `WITHDRAWN` | **venue-fit failure — NOT decay.** The book entry is untouched. New. |
| `SCREEN-DEAD` | failed this venue's structural screen (§2.4 ruling 2) |
| `RETIRED` | dead at this venue, permanently |

**Composition rule (load-bearing, and the reason this is safe):**

```
effective_multiplier = M_book(tier) × M_edition(tier) × DD_SCALE(dd_state)
```

`WITHDRAWN` and `SCREEN-DEAD` both carry `M_edition = 0.00` — they cannot size, by construction. **`M_book` is never modified by an edition event**, which is precisely the invariant the 08-04 ADR had to assert in prose.

> ⚠ **This composition is DESIGN-ONLY under this ADR.** It is not wired, and §5 forbids wiring it without a separate GO. Nothing about live sizing changes on acceptance — see §6.1.

**Ruling 2 — "screen-dead at venue X" is a VENUE-EDITION state, not a book state.** Operator, 2026-08-05: *"venue edition state."*

`ORB-MNQ-1` is the worked example, and it is instructive precisely because **its two negative results live at different levels**:

| Result | Level | Why |
|---|---|---|
| S7 order-symbol occupancy `SCREEN-DEAD` (2026-08-04) | **EDITION**@Tradeify | Occupancy is an artifact of *which legs share that account*. Change the venue or the account and the finding evaporates — it did, when both legs were withdrawn. |
| Payability target `FALSIFIED` (2026-08-03) | **BOOK** | Measured standalone: intraday-honest bust ≥ 67.67% at every admissible `k`. Not an occupancy fact. |

Conflating these is exactly the error made in this programme on 2026-08-05, when `MNQ` was ruled ineligible on S7 grounds that had died with the incumbents — while the *genuine* book-level falsification went uncited. **Separating the levels makes that class of error structurally hard**, and this ADR's own §1.2 cost figure is what it buys.

### §2.5 Consequent re-homing of the third-leg screen

[`docs/spec/2026-07-27-third-leg-target-spec.md`](../spec/2026-07-27-third-leg-target-spec.md) is scoped in its own header to *"a third leg on the same account **as the c1 book**"* — i.e. it is a **deployment-level** screen wearing a book-level name. Its limbs re-home cleanly, and this ADR records the split without editing that spec:

| Limb | Level | Status after the de-scope |
|---|---|---|
| S1 flat-by-16:45, S2 micros, S4 long-only-if-equity-index, S6 no-Treasuries | **EDITION** (venue facts) | Live for any Tradeify edition |
| **S5** cap table, **S7** symbol occupancy | **DEPLOYMENT** (which legs share the account) | **Vacuous while the account is empty** — no incumbent can fire, so no symbol is occupied and the full cap is free |
| **R1–R4** variance/correlation ceilings | **DEPLOYMENT** (composition against a live book) | **Inapplicable while the account is empty** — `σ_composed = √(273² + σ₃²)` has nothing to compose against |
| **T1–T5** cost-law, power, DSR, regime, bust | **BOOK** | **Unaffected. These survive the reframe intact** and remain the real bar |
| M1–M3 mechanism limbs | **BOOK** | Unaffected |

**This is the audit's finding restated structurally:** the limbs that died with the de-scope are exactly the deployment-level ones, and the limbs that survive are exactly the book-level ones. A reader with the axis in hand derives that in one step instead of mis-ruling it twice.

### §2.6 Physical form (minimum viable, deliberately small)

- **Book** stays where it is: `docs/methodology/strategy_lifecycle.md` + `core/lifecycle.py` + `core/firm_rules.py::_BASE_RISK`. **No schema change.**
- **Venue editions** get one new registry: **`ops/venue_editions/<firm_tier>.md`**, one row per edition — `strategy · edition state · cap_alloc · symbol · screen verdict + date · deployment pointer`. Markdown, hand-maintained, mirroring the `ops/instruments/*.md` ledger convention that already works.
- **Deployment** stays `LEG_MAP` + the rail config. **No code change.**
- The descriptor gains an optional fourth slot: `<version> · LOCKED · <authorization> · <durability> [· @<venue-tier>:<edition-state>]`. **Absent = book-level statement**, so every existing descriptor in the repo stays valid unedited.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Do nothing; keep writing prose.** | The status quo, and its cost is measured: 112 premise-dead sites, a 1.91× sizing-law defect (B3), and one documented double-mis-ruling of instrument eligibility inside a single session. Prose does not propagate; structure does. |
| **Overload the existing authorization axis** (add `WITHDRAWN` to `core/lifecycle.py`). | Genuinely tempting — one enum, no new artifact. Ruled out because it **destroys the very distinction the 08-04 ADR fought to preserve**: a book-level `WITHDRAWN` says the strategy lost authorization, when what happened is the *venue* went away. It also collides with `_validate_ladder()`'s hard pin and would make `Striker@Bulenox` inexpressible while `Striker@Tradeify` is withdrawn. |
| **Per-venue forks of each strategy** (`Striker-Tradeify` as its own book entry). | Multiplies the book by the firm count, splits each mechanism's evidence and K bank across forks, and makes "same mechanism, four venues" unstateable. The parameter lock is genuinely venue-independent; forking would imply otherwise. |
| **Bind at deployment only** (skip the edition level; two levels, not three). | Simpler, and briefly attractive. Fails on the operator's own §1.3 question: a *screened-but-undeployed* Tradeify candidate has no home, so "we have no Tradeify-shaped strategy" stays unrecordable — which is the state we are in **today**. The edition level exists precisely to hold screened-not-deployed. |
| **Build a machine-readable registry (JSON + validator) now.** | The repo's own audit just found ≥6 gates that stopped binding while their thresholds never moved, and its meta layer is `DEGENERATING` partly on unowned-gate grounds. **Adding a gate nobody has agreed to maintain would repeat the diagnosis.** Markdown first; mechanize only if the registry proves load-bearing (§4 T2). |

---

## §4 — Falsifier (revert trigger)

> ⚠ **2026-08-14 / 2026-08-22:** T1 fired — F2/F3 were recorded without an edition-state transition. Status is now `Accepted` (operator GO 2026-08-22); T1 stays acknowledged. See Addenda 2026-08-14 and 2026-08-22.

**H (binary):** *Naming venue binding as a third axis, with edition-level authorization state, prevents premise-dead claim propagation and layer-leak defects that the two-axis model structurally cannot prevent — at a maintenance cost below the cost of the prose workaround.*

**H is FALSIFIED — and this ADR is reverted by a superseding ADR — if any trigger fires:**

| # | Trigger | Threshold | Check |
|---|---|---|---|
| **T1** | **The axis is not consulted.** The next venue-scope decision (F2 / F3 election, or any venue withdrawal) is recorded **without** an edition-state transition, having to fall back to prose. | Any 1 occurrence | At the decision |
| **T2** | **The registry goes stale — it becomes the rot it exists to prevent.** `ops/venue_editions/*.md` disagrees with `LEG_MAP` / `firm_rules.py` / the live rail config at any audit. | Any 1 unreconciled disagreement at a quarterly audit | 2026-11-08 |
| **T3** | **It does not pay.** A *new* premise-dead claim of the class this axis exists to prevent (a venue fact asserted at book level, or a venue-conditional bar read as absolute) lands **after** acceptance. | ≥ 2 such findings at the next claim-alignment audit | 2026-11-08 |
| **T4** | **Nobody maintains it.** No edition row is created or updated for ≥ 1 quarter while venue-scope activity demonstrably occurred. | 1 quarter | 2026-11-08 |

**Reachability, stated honestly (the audit's own gate-reachability lesson):** T1 is reachable *this week* — F2 falls due 2026-08-08 and is exactly the shape of decision that must produce an edition transition. T2/T3/T4 are unreachable before 2026-11-08 by construction, and are dated accordingly rather than pretending otherwise.

**Revert action:** author a superseding ADR. **Never edit this §2 in place** (Known Trap #12).

**Trigger check schedule:** 2026-08-08 (T1 only, at F2/F3) and 2026-11-08 quarterly (all four).

---

## §5 — Forbidden moves (under this ADR)

Each was on the table while authoring.

- **Wiring `M_edition` into the live sizing path.** §2.4's composition is **design-only**. `dd_protection.py` and `c1_sizing_host_reference.py` are unchanged, and wiring needs its own ADR + engine pre-flight + operator GO. Genuinely tempting because the composition is three lines — and it is exactly how a governance ADR becomes an unreviewed production change.
- **Editing `core/lifecycle.py`** — its ladder, its multipliers, `STRATEGY_KEYS`, or `_validate_ladder()`. The edition axis is **additive and separate**. The import-time pin exists to stop precisely this.
- **Using an edition transition to move a book lifecycle state**, or vice versa. That collapse is the whole defect this ADR exists to prevent.
- **Reading `SCREEN-DEAD@<venue>` as a book-level death.** `ORB-MNQ-1@Tradeify` is `SCREEN-DEAD`; `ORB-MNQ-1` the book entry is `CANDIDATE`, PARKED, with an independent standalone falsification. ⚠ **Neither state licenses re-opening it** — its payability target is FALSIFIED on its own book-level evidence, and re-opening needs a fresh GO + a survivor-scoring pass.
- **Retro-fitting editions for every historical venue.** Register only what is live or under active consideration. A complete historical edition graph is archaeology, and the belt-only-grows failure mode.
- **Treating an empty edition set as a programme verdict.** "No Tradeify edition exists" is a *fact about our book's coverage*, not evidence the venue is unviable or that the programme has stalled.
- **Building the JSON registry + validator without a separate decision** (§3, last row).

---

## §6 — Consequences

This ADR buys a vocabulary and a place to put facts. It changes no arithmetic, no constant and no live behaviour; the honest summary is that its benefit is preventative and its cost is maintenance, and both are stated below rather than only the first.

### §6.1 What changes on acceptance — and what explicitly does not

**Changes:** one new registry directory (`ops/venue_editions/`); an optional fourth descriptor slot; §2.5's re-homing table becomes the standing reading of the third-leg screen; future venue decisions record an edition transition.

**Does NOT change — verified against production, not assumed:**

- **Live sizing.** `scaled_risk = BASE_RISK × DD_SCALE × lifecycle` is untouched. Every current leg sits at `M_book = 1.00`, and `M_edition` is not wired — **the arithmetic is byte-identical before and after.**
- **`core/lifecycle.py`**, `TIER_MULTIPLIER`, `_validate_ladder()`, `STRATEGY_KEYS` — untouched.
- **`LEG_MAP`, `dd_protection`, allocations, Pine, the rail, `firm_rules.py`** — untouched.
- **Both Striker legs** stay `AUTHORIZED · MECHANISM @ 1.00×` at book level.
- **The 08-04 de-scope** is re-*expressed*, never re-decided. Tradeify remains de-scoped.

### §6.2 Positive

- The 08-04 workaround becomes structure: "venue-fit is not decay" is a property of *where the state lives*, not a sentence someone must remember.
- **B3's defect class becomes hard to author** — `cap_alloc` is edition-owned, so a book-layer law dividing by it is visibly a layer error.
- The operator's §1.3 question becomes answerable and *trackable*: an empty edition set at `Tradeify_Select_100K` is a first-class, queryable fact.
- F3 gets a natural output shape: electing a successor venue = opening an edition set at that tier and screening book entries into it.
- Strategies gain a real pipeline — book entry → screened edition → deployment — instead of a binary deployed/not.

### §6.3 Negative / cost, recorded not minimised

- **A third axis is genuinely more to hold in mind.** Mitigated by the descriptor's optional slot (absent = book-level, so nothing existing changes) and by three levels being the *minimum* that expresses the states §2.2 lists — but the cost is real and T4 exists to catch it going unpaid.
- **A hand-maintained registry can go stale** — the exact failure this programme's audit just found six instances of. Accepted deliberately over a gate nobody owns (§3), with **T2** as the named catch.
- **Existing artifacts are not retro-fitted**, so for one cycle the estate is mixed: some documents speak the axis, most do not.
- **Nothing is enforced.** This ADR buys a vocabulary and a place to put facts. It does not, by itself, stop anyone writing a venue fact into a book-level spec.

---

## §7 — Implementation plan

**Phase 0 — acceptance.** Operator ratifies `Proposed → Accepted`. Nothing below runs first.

**Phase 1 — record what already exists (no new state invented).** Create `ops/venue_editions/Tradeify_Select_100K.md` with the three rows that are already true: `Striker@…` **WITHDRAWN** (2026-08-04), `Striker NAS100@…` **WITHDRAWN** (2026-08-04), `ORB-MNQ-1@…` **SCREEN-DEAD** (S7, 2026-08-04). **The live edition set is then visibly EMPTY — which is §1.3's fact, now recorded.**

**Phase 2 — pointers, one line each** (`docs/methodology/strategy_lifecycle.md` §two-axes → three; `CLAUDE.md` §Strategy Authorization Lifecycle; the 08-04 ADR gains a *"re-expressed under the venue-binding axis"* pointer). **No existing decision text is rewritten.**

**Phase 3 — the §2.5 re-homing** recorded as a dated note on the third-leg spec. Spec body unedited (Trap #12).

**Phase 4 — first live use: F2/F3 on 2026-08-08** produce edition transitions rather than prose. This is **T1's reachability test** and the earliest real evidence the axis pays.

**Not in scope:** wiring `M_edition`; a JSON registry or validator; retro-fitting historical venues; any change to book lifecycle state.

---

## §10 — Audit hooks (runnable)

```bash
# 1. The axis this ADR must NOT have moved — ladder + pin intact (expect 4 tiers, validator present)
grep -n "AUTHORIZED\|WATCH-1\|WATCH-2\|RETIRED" core/lifecycle.py | head -8
grep -c "_validate_ladder" core/lifecycle.py        # expect >= 2 (definition + call)

# 2. Live sizing composition unchanged (expect the BASE_RISK x DD_SCALE x lifecycle line)
grep -n "scaled_risk" core/dd_protection.py

# 3. cap_alloc is edition-owned and production still halts rather than falling back (expect both)
grep -n "cap_alloc" ops/c1_rail/c1_sizing_host_reference.py | head
grep -c "cap_firm / (1" docs/spec/c1_watch_realization_multiplier_layer.md   # expect 0 (B3 fixed)

# 4. Phase 1 landed and the Tradeify edition set is EMPTY of ACTIVE rows (the §1.3 fact)
ls ops/venue_editions/ 2>/dev/null || echo "Phase 1 not yet run"
grep -c "ACTIVE" ops/venue_editions/Tradeify_Select_100K.md 2>/dev/null   # expect 0 until F3

# 5. T1 reachability — did F2/F3 produce an edition transition, or fall back to prose?
grep -n "edition\|EDITION" STATE.md | head

# 6. Both Striker legs still AUTHORIZED at BOOK level (venue-fit is not decay)
grep -n "AUTHORIZED" docs/methodology/strategy_lifecycle.md | head -3
```

---

## Verification

```bash
# Discipline check (expect PASS)
PYTHONIOENCODING=utf-8 python scripts/check_brief.py docs/adr/2026-08-05-strategy-venue-binding-axis.md --type adr

# Graph integrity — this ADR declares no supersession edges, so A2 must stay clean
python scripts/check_adr_graph.py

# §0 anchors resolve
for f in core/lifecycle.py core/dd_protection.py ops/c1_rail/c1_sizing_host_reference.py \
         core/firm_rules.py docs/methodology/strategy_lifecycle.md; do
  git log -1 --format="%h %ci $f" -- $f
done
```

## Addendum 2026-08-14 — Status framing: stalled/bypassed; T1 likely fired

**Type:** dated status-framing correction under Rule 14. **Status field remained `Proposed` as of this addendum** (flipped `Accepted` 2026-08-22 — header + Addendum 2026-08-22). §2 decision text is not edited and is not withdrawn.

This ADR was never ratified; `ops/venue_editions/` was never created. Its own T1 fires on any venue-scope decision recorded without an edition-state transition. [`2026-08-07-loop-s1-environment-ratification.md`](2026-08-07-loop-s1-environment-ratification.md) resolved F2 and F3 in prose (rail keep-warm/disarmed; no successor migration) with no edition-state transition through that never-built registry. The [2026-08-05 claim-alignment follow-ups](../notes/audits/programme-audit/2026-08-05-claim-alignment/07-followups.md) item 5 already named "ratify before F2/F3" as the T1 reachability clock; that step was not taken.

Do not read `Proposed` as a live, pending, uncomplicated ratification path. Revisit would need a fresh GO, not a quiet flip. The underlying B3 layer-leak analysis (venue-fit facts must not leak into book-level artifacts) is **not** judged wrong and could still matter if venue-binding is reopened.

## Addendum 2026-08-22 — Operator Accept (fresh GO)

**Type:** status flip. **Status field is now `Accepted`.** §2 decision text is not edited.

Operator Accept 2026-08-22 is the fresh GO the 2026-08-14 addendum required. T1 (S1 recorded F2/F3 with no edition-state transition) is **acknowledged as already fired** — Accept ratifies the axis as standing doctrine going forward; it does not claim T1 did not fire and does not rewrite S1.

§7 Phase 0 (this flip) is done. **Phase 1 remains owed** (`ops/venue_editions/Tradeify_Select_100K.md` with the three already-true rows; live edition set EMPTY). Phase 2 pointer one-liners land with this ratification. Phase 4's T1 clock is historical.

Forbidden here: wiring `M_edition` into live sizing; editing `core/lifecycle.py`; treating this Accept as a Phase 1 registry land.

| Date | Change | By |
|---|---|---|
| 2026-08-14 | Addendum 2026-08-14 — stalled/bypassed framing; T1 likely fired. Status remains Proposed. §2 body byte-unchanged. | claim-alignment reconciliation |
| 2026-08-22 | **Operator Accept** (fresh GO named by the 2026-08-14 addendum). Status `Proposed` → `Accepted`. T1 acknowledged as already fired (S1 F2/F3 in prose; no edition transition). §2 body byte-unchanged. §7 Phase 1 registry still owed. | Joshua (GO) + Cursor (record) |
| 2026-08-23 | §7 Phase 1–3 landed: `ops/venue_editions/Tradeify_Select_100K.md` (three already-true rows; live set empty). Phase 2 leftover pointer on the 08-04 ADR. Phase 3 dated note on the third-leg spec (body unedited). §2 / §4 / §5 byte-unchanged. T1 still acknowledged. | Cursor (plan execution) |
