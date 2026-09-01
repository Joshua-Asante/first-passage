# ADR 2026-07-13 — Prop-portfolio account boundary: one account = one pre-registered book

**Status:** `Accepted` — operator ratified 2026-07-13 (drafted by claude.ai Tech Advisor)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-13
**Authors:** claude.ai Tech Advisor (draft) · Joshua (decision)
**Related:** [`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) (parent program — this ADR supplies its account-boundary semantics; supersedes nothing); [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) (E2/E3 interactions); [`docs/adr/2026-06-06-firm-constants-single-source.md`](2026-06-06-firm-constants-single-source.md); [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) (tier multipliers act per-account under this rule).
**Layer:** execution + portfolio operations — not locked-parameter. No change to locked allocations, `dd_protection`, Pine, `ACTIVE_FIRM`, or MC pins.

---

## §0 — Rule-0 reads (2026-07-13)

- [`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) — content-read 2026-07-13 (git `0e26a7b`). §2.1 makes multi-leg books a first-class design target; this ADR must therefore bind at the book level, not one-strategy-per-account.
- [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) — content-read 2026-07-13 (git `802ee60`). E2 default 40% consistency; E2 design consequence already names portfolio-slot smoothing; E3 trailing intraday on unrealized equity.
- [`core/firm_rules.py`](../../core/firm_rules.py) — working-tree Select-String read 2026-07-13. `inactivity_max_idle_days: 5` across Bulenox tiers (≥1 trade per 5 trading days); Tradeify Flex weekly (re-MC disables rather than models it).
- [`ops/instruments/6J.md`](../../ops/instruments/6J.md) — J1–J5 content-read 2026-07-13 (git `c675c9c`). J4: Aegis cap-12 breach ~11–12% standalone on the Bulenox Option-2 example — per-account survival math exists per book, not per account-mixture.
- Evidence panels (claude.ai reconcile 2026-07-13; Step-0 clean; context panels, NOT anchors): MYM `89a96dcc…`, MNQ `5a9816…`, 6J `dd6412…` (2026-07-12 TV exports; full pins in [`docs/briefs/Q-TVCOV-1-tv-bar-coverage-census.md`](../briefs/Q-TVCOV-1-tv-bar-coverage-census.md) §0).

---

## §1 — Context

The four-firms program (`Accepted` 2026-07-12) targets challenge-passing with portfolio composition as a first-class design object, but leaves the account boundary undefined: what may legally share one eval/funded account. The 2026-07-13 reconcile of the three seven-year futures panels supplies the missing empirical shape: three same-family legs (100% long-risk-side — 287/287 long MYM, 290/290 long MNQ, 155/155 short-yen 6J — NY-morning entries, in-market 0.62%/0.67%/0.27% of the clock) print pairwise monthly correlations of −0.10 / +0.13 / −0.01, worst-decile-month overlap 0–1 of 9, max-DD windows fully disjoint (2024-03→11 / 2024-12→2025-04 / 2021-10→2022-10), and zero all-three-lose days in seven years. There is no realized diversification offset for co-mingling to buy — the near-zero correlation is produced by non-overlap, not hedging — while co-mingling's structural cost under E3 is certain: one book's winning streak ratchets the shared trailing floor under the other book. Meanwhile the program falsifier (2026-11-08, "≥1 pre-registered candidate clears the bust ceiling on ≥2 tiers") is only well-posed if candidate bust attribution is per-account clean.

**Decision driver (one sentence):** trailing-DD entanglement is a certain structural cost of co-mingling, the measured diversification offset is ≈0, and the 11-08 falsifier requires per-candidate attribution — so the account boundary must be the pre-registered book.

---

## §2 — Decision

**One account = exactly one pre-registered book.** A book is single-leg or multi-leg; a multi-leg book exists only if registered as a book before deployment, with its own joint MC under the assigned firm-tier rule set (`firm_rules.FIRM_RULES[<tier>]` + envelope overlays).

- **No post-hoc co-mingling.** Adding a leg to a live account constitutes a new book: superseding registration + re-MC under that tier before the added leg's first trade.
- **Legacy × greenfield separation.** Any lifecycle survivor of the locked-book family and any greenfield discovery candidate never share an account absent rule-1 registration. (R6's locked-book fan-out NO-GO stands regardless.)
- **E2 consistency-pairing is an instance of the rule, not an exception.** Pairing legs to smooth the daily P&L distribution against a consistency cap is a legitimate multi-leg-book motive and follows the same pre-registration path.
- **Program-level risk is integrated even though deployment is segregated:** one joint MC across accounts — per-account bust under each account's own rule set, joint resampling for co-movement, plus the shock-conditional module proposed in [`docs/adr/2026-07-13-stage8-mechanistic-exposure-companion.md`](2026-07-13-stage8-mechanistic-exposure-companion.md).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Co-mingle strategies per account for capital efficiency | No cross-margining benefit at these firms; E3 trail entanglement is certain; 11-08 falsifier attribution destroyed; a leg can bust an account it would never have busted alone. |
| Strict one-strategy-per-account (forbid multi-leg books) | Contradicts four-firms §2.1 (composition first-class) and E2's portfolio-slot doctrine; profit-concentrated candidates are eval-hostile standalone by design. |
| Defer the boundary until the first candidate admits | The 11-08 pass-simulation semantics ("clears bust ceiling on ≥2 tiers") need account-boundary rules now for the MC to be well-posed; deferral invites drift-by-convenience under inactivity-clock pressure. |
| Realized-correlation gate for co-residency (allow if ρ < threshold) | Measured blind for this strategy class: the three-leg family reads ρ≈0 while being 100% same-direction — sparse in-market overlap manufactures zero correlation regardless of shared beta (companion ADR). |

---

## §4 — Falsifier (revert trigger)

**H (hypothesis):** segregation's per-account fixed frictions are affordable relative to book expectancy.

**Revert trigger (binary):** if the joint-MC + fee model shows per-account frictions — eval-fee amortization + inactivity-clock token-trade drag (`inactivity_max_idle_days: 5` Bulenox; weekly Tradeify Flex) + per-account data/rail fees — consuming ≥25% of a registered book's modeled expectancy at its assigned tier, the segregation default re-opens for that tier class via superseding ADR (never edited in place).

**Verdict at each check (binary per tier class):** RESOLVED (frictions < 25% of book expectancy — default stands) / FALSIFIED (≥ 25% — re-open per trigger above) / AMBIGUOUS (fee model incomplete — carry to next check date, never silently extend).

**Check schedule:** 2026-08-08 · 2026-11-08 (with the parent-program falsifier) · 2027-02-08.

---

## §5 — Forbidden moves (under this ADR)

- Parking a "temporary" second strategy in a funded account to feed an inactivity clock — the genuinely tempting one; token-trade mitigation must be an in-book mechanism, never a foreign leg.
- Citing the measured ρ≈0 as license to co-mingle ("they don't correlate anyway") — the zero is a sampling artifact of non-overlap, not independence evidence.
- Warehousing one book's eval attempt inside another book's cushioned account.
- Retro-designating co-resident legs as a "book" to launder a violation into compliance.

---

## §6 — Consequences

**Positive:** clean per-candidate falsifier attribution for 11-08; lifecycle tier multipliers (WATCH-1 0.5× / WATCH-2 0.25×) rescale one account without perturbing others; no trail entanglement; historically disjoint DD windows support staggered eval scheduling.

**Negative (real cost):** account multiplication — N books = N eval fees + N inactivity clocks + N flat-deadline surfaces; low-frequency candidates are the worst hit (priced by §4's trigger rather than hand-waved).

**Downstream updated:** none (doctrine only; no code).

**Downstream NOT changed (explicit):** locked allocations, `dd_protection`, `ACTIVE_FIRM`, four-firms §2, R6 boundary.

---

## §7 — Implementation plan

- **Phase 0** — this draft (2026-07-13). ✅
- **Phase 1** — operator ratify/edit; set Status + Decision date. ✅ **Ratified 2026-07-13.**
- **Phase 2** — `docs/SESSIONS.md` entry (2026-07-13) + any future joint-MC harness keys per-account rule sets by construction (standing obligation on that harness's author).

---

## §10 — Audit hooks

```bash
grep -n "Status.*Accepted\|one account = exactly one pre-registered book" docs/adr/2026-07-13-prop-account-book-segregation.md
python -c "import sys; sys.path.insert(0,'core'); import firm_rules; ks=[k for k,v in firm_rules.FIRM_RULES.items() if v.get('inactivity_max_idle_days')==5]; assert ks, 'Bulenox 5-day clocks missing'; print('OK', len(ks), 'tiers on 5-day clock')"
grep -rn "same account\|co-mingle" lab/ docs/briefs/rnd-pipeline/ 2>/dev/null | grep -v segregation || echo "no co-residency drift in research artifacts"
```

**Verification**

```bash
python scripts/check_brief.py docs/adr/2026-07-13-prop-account-book-segregation.md --type adr
```

---

## Addendum 2026-09-01 — §4's 2026-08-08 check: pointer only, disposition remains an operator call

**Status: informational pointer only — adds no verdict, moves no gate, edits no §1–§10 text above.**

§4 set a check date of 2026-08-08. An arithmetic reading against §4's 25% trigger was produced in [`docs/briefs/2026-07-17-0808-packet-delta-and-sequence.md`](../briefs/2026-07-17-0808-packet-delta-and-sequence.md) §1 (row "Segregation ADR §4 revert check"): per-account frictions $81.07/mo ÷ modeled expectancy $299.80/acct-mo = **27.04% at N=1**, above §4's 25% trigger. That brief's own §11-B says this reading is **"operator-owned"** and **"not accepted by signing this packet."** The packet's own Status line reads `DRAFT — SUPERSEDED BY EVENTS`, and its 2026-08-29 addendum records that the event which actually ran on 2026-08-08 was a disjoint programme-audit/prune, not this packet's own §2/§11 gate walk — which never executed.

No later artifact in the corpus disposes of this check. The reading's supporting provenance (the CrossTrade-subscription + eval-fee spend tally and the idle-rule-disposition design spec) is not present in this tree as of 2026-09-01, so the 27.04% figure can currently be read only as recorded in that brief, not independently re-derived here.

**This addendum takes no verdict.** Stamping one of §4's own three dispositions (`RESOLVED` / `FALSIFIED` / `AMBIGUOUS`) for the 2026-08-08 date is an operator call, not this addendum's to make.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-13 | Drafted, Status Proposed | claude.ai Tech Advisor |
| 2026-07-13 | Ratified — Status `Accepted` | Joshua |
| 2026-09-01 | Addendum: §4's 2026-08-08 check — verdict-free pointer to the arithmetic reading (27.04% @ N=1) recorded in a now-superseded brief; disposition remains an operator call | Claude Code (ADR-corpus reconciliation sweep) |
