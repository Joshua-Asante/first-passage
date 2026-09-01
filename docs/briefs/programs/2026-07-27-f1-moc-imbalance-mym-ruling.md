# F1 — Closing-auction / MOC-imbalance flow on MYM: bar-ruling (admit-or-reject)

**Type:** paid-data-procurement-gate ruling (zero-run, zero-K, zero-$). **Authored:** 2026-07-27.
**Source:** entry **F1** of the forced-flow census `N-2026-07-26-forced-flow-census.md` (pruned at the Great Prune; retrieve via `git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`),
the census's only entry not already dead after its 2026-07-26 self-audit (F2/F3 were killed by prior rulings).
**Verdict (this brief):** **FALSIFIED — reject-at-bar**, blocked at the **paid-data procurement gate**
(not at the free-data domain bar — see §4, where F1 genuinely differs from D2). Not admitted for a full Pre-Q.
**Precedent template:** [`2026-07-24-d2-letf-eod-flow-ruling.md`](2026-07-24-d2-letf-eod-flow-ruling.md).

---

## §0 — Rule-0 reads (verified this session, 2026-07-27)

- [`docs/rejected_candidates.md`](../../rejected_candidates.md) @ `2fbc996` — **§ "5th-leg / portfolio-expansion (free-data search) — SNAG-CLOSED 2026-07-01"**: scope is candidates sourced from **free data**; explicitly does **not** close expansion via **paid data** or a new venue class. Its **route 1** reads: *"Paid / exogenous data the free searches could not access (e.g. NDX-native dealer gamma, intraday 0DTE order-flow), **demonstrating an edge that is both vol-orthogonal and within-era robust**"* — the demonstration is part of the route, not a consequence of clearing it. Also read: **§ "Single-instrument index-futures intraday OHLCV directional timing — RAISED BAR 2026-07-21"**, whose scope is *"from **OHLCV structure alone**"* and whose route 2 names *"a different modality (order-flow / microstructure — **untouched per the 'don't buy explanatory data before a survivor' rule**)"*.
- [`docs/briefs/programs/2026-07-24-avenue-a-microstructure-scoping.md`](2026-07-24-avenue-a-microstructure-scoping.md) — **the governing artifact for any paid order-flow procurement.** §1 names the two standing rules bracketing this modality: **(a)** "don't buy explanatory data before a survivor justifies it"; **(b)** the a4 prior (category-splitting is non-identifying from the tape). §2 fork table; §5 forbidden move *"Buying explanatory data before a survivor justifies it — the standing rule; a blind depth-shape sweep violates it."* §6 freezes the **qualifying triple** that alone authorizes a pull. Standing disposition: **"Avenue A stays scoped-not-procured."**
- [`docs/briefs/programs/2026-07-14-a4-flow-data-fork-scoping.md`](2026-07-14-a4-flow-data-fork-scoping.md) — the flow-data prior. Its kill is specifically **category-splitting** (Asset-Manager vs Leveraged-Funds is confounded; net/aggregate is non-identifying). It also records the standing read that EOD-flow effects in this programme are *"real as mechanisms but thin / redundant / decaying as tradable alpha."* **Scope note (load-bearing for honesty):** a4 does **not** kill a *published, signed* imbalance number — see §5's misrepresentation guard.
- [`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) (as amended 2026-07-26) — **Requirement 2** (cohort-cited per-instrument δ; "No citable δ ⇒ UNSCREENABLE → route to a δ-extraction probe or drop; **never invent a number**"); **Requirement 3** family banks (**MYM 1 → K_eff 2 → floor 0.85**, open); **Requirement 5** cost-law.
- [`core/firm_rules.py`](../../core/firm_rules.py) @ `fd95c72` — `Tradeify_Select_100K`: `cost_per_side_usd` 0.91; flat **16:45 ET** (a 15:50→16:00 ET window is envelope-compatible); MYM $0.50/pt, 1.00-pt tick.
- [`docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md`](../../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) `Accepted` — the four-clause Requirement-1a this entry was authored under, and §5's new forbidden moves (unexecuted attestations; capacity-grading before cost arithmetic) that this ruling is written to honour.

---

## §1 — Context

F1 proposes trading the **closing-auction imbalance**: index-tracking and passive funds are mandated
to execute at the official closing print, exchanges publish the resulting order imbalance from
~15:50 ET, and the claim is that a directional response is harvestable on MYM inside the
15:50→16:00 ET window, flat well before the 16:45 ET deadline.

The four Requirement-1a clauses are all *nameable*, which is why the entry survived the census's
first pass: **WHO** — passive/index mandates (a constraint, not a preference), compensated in
tracking-error avoided; **WHEN** — daily, publication-to-close, a published schedule; **WHY it
survives** — mandate-inelastic demand plus a micro-capacity residual below institutional ticket
size; **HOW it dies** — published imbalance sizes and close-auction volume share are observable.
A clean four-clause card is exactly what ADR §2-A was designed to elicit. **It is not sufficient
for admission**, and this ruling is where that gets demonstrated rather than asserted.

Standing doctrine this sits under: the 5th-leg/expansion domain is **SNAG-closed for free-data**
candidates (2026-07-01), and **paid** candidates are governed by the Avenue-A procurement gate
(2026-07-24), whose standing disposition is *scoped-not-procured*.

---

## §4 — Falsifiable hypothesis

**H:** F1 is **admissible for a full Pre-Q** — i.e. it clears a domain/procurement route as scoped.

**Falsifier:** if F1 clears **none** of the available routes at its current evidentiary state, H is
**falsified** (reject-at-bar).

**Adjudication, route by route.**

**(a) Free-data 5th-leg domain — route 1 (paid/exogenous data): NOT CLEARED, but for a reason that
distinguishes F1 from D2 and is worth stating precisely.** Unlike LETF rebalance flow — whose signal
is fully reconstructable from public AUM + public return + published leverage, and which was
therefore *classified* free-data and rejected — MOC imbalance is an **exchange-licensed product**
(NYSE Order Imbalance Information / Nasdaq NOII class). F1 is therefore **not killed by the
free-data classification**; D2's ratio decidendi does not reach it. But route 1 is not satisfied by
*data class alone*: its text requires **demonstrating an edge that is both vol-orthogonal and
within-era robust**. F1 demonstrates nothing — it has **no citable δ, no cohort, no measurement**.
The route is therefore **unclaimed, not cleared**. *(Assertion requiring `verify-source` if ever
escalated: that MOC imbalance is licensed rather than freely published. It is **not load-bearing**
to this verdict — if it turned out to be free-derivable, F1 would fail *harder*, landing directly in
the D2 free-data kill.)*

**(b) OHLCV raised bar — route 2 (different modality): NOT AVAILABLE AT THIS STATE.** The 2026-07-21
bar's scope is edges *"from OHLCV structure alone"*, so an exogenous-imbalance candidate is arguably
outside it entirely; but where it does reach, route 2's order-flow/microstructure sanction is
**expressly parenthesised to the standing rule** — *"untouched per the 'don't buy explanatory data
before a survivor' rule"*. That rule was operationalised three days later by the Avenue-A scoping,
whose §6 authorises procurement **only** via a pre-registration naming a feature that clears the
qualifying triple, and whose standing disposition is *scoped-not-procured*. F1 is **blind discovery
on paid data with no survivor tie** — precisely the shape both the rule and §5 of that brief forbid.
**This is the binding constraint.**

**(c) Harvest Requirement 2 — independently fatal at the front door.** No published or in-house δ
exists for *MOC-imbalance → MYM*. Requirement 2 forbids transplanting a cross-instrument δ and
forbids inventing one; the disposition is **UNSCREENABLE → δ-extraction probe or drop**. And the
probe route is **circular here**: extracting δ requires the paid imbalance data, whose procurement
is gated by (b). F1 cannot screen, and cannot buy its way to screenable, at its current state.

**Adjudication:** no route clears. → **Falsifier fires.**

**Non-load-bearing context (pure arithmetic on frozen constants; nothing run, no data touched).**
MYM RT = 2($0.91) + 2($0.50) = **$2.82**; 4× hurdle **$11.28** ⇒ at $0.50/pt, a qualifying edge must
net **≈22.6 Dow index points per trade** inside a ten-minute window. Recorded per ADR §5's new
requirement that capacity-niche entries carry their cost arithmetic — **not** used to decide this
verdict (the procurement gate is decisive), and explicitly **not** a cost-law pre-screen, which
would require data F1 is not authorised to hold.

**Also unvalidated (stated, not hidden):** MOC imbalance is a **cash-equity** phenomenon; any MYM
response is an *indirect transmission* (constituent basket → index → future). Nothing establishes
that transmission survives to a micro Dow future at tradable size. This is a second missing link
beneath the missing δ.

---

## §5 — Forbidden moves (each genuinely tempting in authoring this ruling)

- **Claiming free-data route 1 because "the data is paid."** The route requires *demonstrating* a
  vol-orthogonal, within-era-robust edge; data class is a precondition, not the clearance. Treating
  "it's paid" as self-clearing would let any licensed feed reopen a SNAG-closed domain by purchase.
- **Conflating the a4 prior with a kill it does not deliver.** a4 kills **participant-category
  splitting** (non-identifiable from the tape). A published, signed imbalance is a *different object*
  and a4 does not reach it. Borrowing a4's authority here would launder a weaker rejection — the
  same misrepresentation Avenue A §5 already names. The honest blocker is the **procurement gate**,
  not identifiability.
- **Buying the imbalance feed to "just get a δ."** This is the standing rule's exact prohibition and
  the circularity in §4(c) is not a loophole in it — it is the rule working.
- **Running a probe, cost-law pre-screen, or any simulation.** As in D2: the gate exists to avoid
  spending even a cheap probe. The §4 arithmetic is division on frozen constants, not a screen.
- **Re-labelling F1 as an execution-quality question to ride the c1 lane.** c1 execution research is
  authorised and unaffected; F1 is a **new directional entry mechanism**. Re-badging it would smuggle
  a 5th-leg candidate through a lane scoped for improving fills on the existing book.
- **Softening the verdict to "deferred" because the four clauses are well-formed.** A clean
  four-clause card is what ADR §2-A is *supposed* to produce; admission requires clearing the
  domain/procurement gates as well. Grading the card instead of the gates would make §2-A a
  rubber stamp on its second use.

---

## §6 — Gate / verdict

**Verdict: FALSIFIED — reject-at-bar** (blocked at the paid-data procurement gate).

| Route | F1 status | Cleared? |
|---|---|---|
| Free-data domain **route 1** — paid/exogenous data *demonstrating* a vol-orthogonal, within-era-robust edge | data plausibly paid (unlike D2), but **zero demonstration**: no δ, no cohort, no measurement | **No** — unclaimed, not cleared |
| Free-data domain **route 2** — genuinely new venue class relaxing a binding wall | same futures-prop venue, same MYM leg | **No** |
| Free-data domain **route 3** — dated live incident the book failed | none cited | **No** |
| OHLCV raised bar **route 2** — different modality (order-flow) | sanction is parenthesised to "don't buy explanatory data before a survivor"; Avenue A §6 qualifying triple unmet; no survivor tie | **No** — the binding constraint |
| Harvest **Requirement 2** — cohort-cited per-instrument δ | none exists for MOC→MYM; probe route circular (needs the gated data) | **No** — UNSCREENABLE |

**What this ruling does NOT decide:** that the mechanism is unreal (it is real and well-documented in
the cash-equity literature), or that MOC imbalance is permanently out of bounds. It decides that
**at zero evidence and with procurement gated, F1 is not admissible**, and that the honest next move
is not a purchase.

**Re-open condition (mechanism-evidence, not packaging) — the cheapest live path first:**

1. **A published cohort δ for imbalance → index-futures response** (not cash-equity single-name),
   citable under Requirement 2 **without** us procuring anything. This is **free, zero-K, and is the
   only route that can be attempted today** — it converts F1 from UNSCREENABLE to screenable, at
   which point route 1's "demonstrating" clause becomes reachable in principle; **or**
2. **A survivor tie** that justifies procurement under Avenue A §6's qualifying triple — i.e. an
   existing candidate whose *own* pre-registered question requires imbalance data; **or**
3. **The data becoming freely available** — which would *reverse* the sign of the argument,
   dropping F1 straight into the D2 free-data kill rather than rescuing it; **or**
4. **A dated live incident** the book failed that this leg would have covered.

**Not** re-openable by: a micro-capacity re-framing, a different index/instrument, a longer window,
an assertion that the mechanism is real, or a well-formed four-clause card.

---

## §7 — Forked questions

- **None opened.** A reject-at-bar closes the direction; §6's re-open bar is the only re-entry.
- **Census consequence (recorded, not a fork):** with F1 ruled, **all seven** forced-flow census
  entries are now dead, blocked, or deferred. The census's first pass yielded **zero admissible
  seeds**. That is a real result about the census channel and is the first datum against ADR §4's
  **2-B falsifier** ("zero seeds passing the intake screen by the second audit after ratification →
  retire the channel"). One pass is not the trigger — the trigger needs the 2026-11-08 and following
  audit — but it is the honest opening entry in that ledger, and it should be read alongside the
  fact that two of the seven were killed by *author error* (unexecuted attestations, 2026-07-26
  self-audit) rather than by the channel being barren.

---

## §10 — Audit hooks (runnable)

```bash
# The two bars this ruling is judged against
rg -n "5th-leg / portfolio-expansion \(free-data search\)" docs/rejected_candidates.md
rg -n "don't buy explanatory data before a survivor" docs/rejected_candidates.md docs/briefs/programs/2026-07-24-avenue-a-microstructure-scoping.md

# Avenue A must still be scoped-not-procured (if this flips, re-read this ruling)
rg -n "scoped-not-procured|stays scoped" docs/briefs/programs/2026-07-24-avenue-a-microstructure-scoping.md

# After recording, the registry entry + concept-intake comment must be present.
# Pattern matches the STORED mechanism_family, not the author's mental form (trap M-AHF:
# an earlier draft of this hook grepped "moc-imbalance-closing-auction" and found only 1 of 3).
rg -c "closing-auction-moc-imbalance-flow|MOC-imbalance flow on MYM" docs/rejected_candidates.md
# Expected: 3 (heading + concept-intake-entry comment + bullet)

# This brief is the Authoritative artifact the entry points to
test -f docs/briefs/programs/2026-07-27-f1-moc-imbalance-mym-ruling.md && echo AUTHORITATIVE_OK

# No procurement happened on the back of this ruling (expect no new cache growth / no manifest)
ls discovery_manifests/ | rg -i "moc|imbalance" || echo "no manifest, as expected (zero K spent)"

# Census cross-link: F1 must now read DEAD, not "only live entry"
# Working-tree path was pruned; retrieve then grep (tag is private-archive-only
# on this public clone — docs/ltm/README.md).
git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md | rg -n "F1 —"
```

---

## Verification

§0 cites concrete repo paths with anchors ✓ · §4 states `H:` + falsifier and adjudicates **each
route separately**, naming where F1 genuinely differs from D2 (paid vs public-derivable) rather than
borrowing D2's kill ✓ · §5 lists moves genuinely tempting in *this* authoring (claim route 1 on data
class; borrow a4's authority; buy the feed for a δ; soften to "deferred" because the clause card is
clean) ✓ · §6 binary verdict with the route table + a re-open bar whose **first item is free and
actionable today** ✓ · §10 runnable ✓ · doctrine-connected (free-data SNAG bar, OHLCV raised bar,
Avenue A gate, harvest Req 2/3/5, ADR 2026-07-26) ✓ · **zero runs, zero K, zero $** ✓.

---

## Registry entry (to append to `docs/rejected_candidates.md`)

### Closing-auction / MOC-imbalance flow on MYM — paid-data 5th-leg candidate

**Rejection scope:** trade the published closing-auction order imbalance (~15:50 ET publication →
16:00 ET close) as a directional entry on MYM, flat well before the 16:45 ET deadline. Rejected as a
**paid-data** 5th-leg directional mechanism at the **procurement gate**. Distinct from the LETF
EOD-flow rejection (that signal was public-AUM-derivable ⇒ free-data; this one is exchange-licensed,
so the free-data classification does **not** reach it) and from Avenue-A depth-shape discovery (this
is a published signed imbalance, not book geometry, so the a4 category-non-identifiability prior does
not reach it either).
**Closure date:** 2026-07-27
**Class:** paid-data-procurement-gate (reject-at-bar; mechanism real, evidence absent, procurement gated)
**Authoritative artifact:** [`docs/briefs/programs/2026-07-27-f1-moc-imbalance-mym-ruling.md`](briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md)
**Closure basis:** clears no route. Free-data route 1 requires *demonstrating* a vol-orthogonal,
within-era-robust edge — F1 has no citable δ, no cohort, no measurement, so the route is unclaimed
rather than cleared; routes 2/3 (new venue class / dated incident) plainly fail. The OHLCV raised
bar's order-flow modality is expressly parenthesised to the standing **"don't buy explanatory data
before a survivor justifies it"** rule, operationalised by the 2026-07-24 Avenue-A scoping (§6
qualifying triple; standing disposition *scoped-not-procured*) — F1 is blind discovery on paid data
with no survivor tie, the exact prohibited shape. Independently, harvest **Requirement 2** renders it
**UNSCREENABLE** (no MOC→MYM δ; transplant and invention both forbidden), and the δ-extraction probe
route is circular because it needs the gated data. Secondary unvalidated link: MOC imbalance is a
cash-equity phenomenon; transmission to a micro Dow future is unestablished. Cost context (non-load-bearing,
pure arithmetic): MYM RT $2.82 ⇒ 4× hurdle $11.28 ⇒ ≈22.6 Dow points/trade in a ten-minute window.
**Re-proposal bar:** a **published cohort δ for imbalance → index-futures response** citable without
procurement (free, zero-K — the only route attemptable today); OR a **survivor tie** meeting Avenue-A
§6's qualifying triple; OR the data becoming free (which would *drop it into the D2 free-data kill*,
not rescue it); OR a dated live incident the book failed. NOT a micro-capacity re-framing, a different
index/instrument, a longer window, or a well-formed four-clause card.

<!-- concept-intake-entry mechanism_family="closing-auction-moc-imbalance-flow" instrument="MYM" rejection_reason="paid-data-procurement-gate (reject-at-bar): census entry F1 - trade published MOC order imbalance (15:50 ET publication -> 16:00 ET close) directionally on MYM, flat by 16:45. Clears NO route: free-data route 1 requires demonstrating a vol-orthogonal + within-era-robust edge and F1 has zero delta/cohort/measurement (unclaimed, not cleared); no new venue class; no dated incident. Binding constraint = the standing 'don't buy explanatory data before a survivor justifies it' rule, operationalised by the 2026-07-24 Avenue-A scoping (qualifying triple unmet, scoped-not-procured) - F1 is blind discovery on paid data with no survivor tie. Independently UNSCREENABLE under harvest Req 2 (no MOC->MYM delta; transplant/invention forbidden; delta-extraction probe circular since it needs the gated data). Unvalidated cash-equity -> micro-Dow-future transmission. NOT killed by the D2 free-data classification (imbalance is exchange-licensed, not public-derivable) nor by the a4 category prior (published signed imbalance != category splitting) - those distinctions are stated so a future session does not borrow the wrong kill." harness_disposition_ref="F1-bar-ruling (manual paid-data-procurement-gate falsifier; docs/briefs/programs/2026-07-27-f1-moc-imbalance-mym-ruling.md)" date="2026-07-27" class="paid-data-procurement-gate" role_tested="entry" falsifier_failed="no route cleared: free-data route 1 unclaimed (zero demonstration), OHLCV route-2 order-flow modality gated by no-buy-before-survivor + Avenue-A qualifying triple, harvest Req 2 UNSCREENABLE with circular probe route" addback_condition="published cohort delta for imbalance->index-futures response citable WITHOUT procurement (free, zero-K, only route attemptable today), OR a survivor tie meeting Avenue-A section-6 qualifying triple, OR the data becoming free (which drops it into the D2 free-data kill), OR a dated live incident - NOT micro-capacity re-framing, different index, longer window, or a well-formed four-clause card" config_fingerprint="moc-imbalance/MYM/signal=exchange-published-signed-imbalance/window=1550-1600ET/venue=futures-prop-flat-1645" -->
- **closing-auction-moc-imbalance-flow on MYM** — rejected 2026-07-27 (paid-data-procurement-gate: no route cleared; free-data route 1 unclaimed for want of any δ; order-flow modality gated by "don't buy explanatory data before a survivor" + Avenue-A qualifying triple; UNSCREENABLE under Req 2 with a circular probe route); [`docs/briefs/programs/2026-07-27-f1-moc-imbalance-mym-ruling.md`](briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md).
