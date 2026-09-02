# ADR 2026-07-13 — Prop envelope v1.0 ratification (E1/E2/E7 resolved, ETF closed, commissions single-sourced)

**Status:** Accepted (operator "proceed" directive 2026-07-13, executing item 2 of the ratified 2026-07-12 recommendation; B1 on the STATE forward board)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-13
**Authors:** Joshua (decision) + Claude Code Opus 4.8 (research + recorder)
**Ratifies:** [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) v0.1 → **v1.0** (change control now per its header)
**Related:** [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) (§2 step-1 consumes the envelope); [`docs/briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md`](../briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md) (RATIFIED §7 — the G1/G2 gates this envelope feeds); [`2026-06-06-firm-constants-single-source.md`](2026-06-06-firm-constants-single-source.md) (why commissions land in `firm_rules`, not envelope prose)
**Layer:** ops/governance + `core/firm_rules.py` **data fields** (additive) — no locked constant, allocation, `dd_protection` value, MC pin, or Pine touch.

---

## §0 — Rule-0 reads + evidence provenance

- `ops/prop_envelope_default.md` @ `802ee60` — v0.1 full read (E1–E7, §5 five open items).
- `core/firm_rules.py` (this branch, post-`0e26a7b`) — all four FRIENDLY families; `cost_per_side_usd` present only on Bulenox tiers pre-change; Tradeify consistency % un-encoded pre-change.
- `tests/core/test_automation_friendly_prop_firms.py` — guard shape (additive-friendly) before extending.
- **Evidence:** 10-agent research workflow, 2026-07-13 — 5 primary-source researchers (Tradeify, MFFU, BluSky, Bulenox re-verify, ETF) + 5 independent adversarial citation-verifiers that re-fetched every cited URL and specifically checked per-side-vs-round-trip units, CT→ET/DST conversion, and plan/tier attribution. **Zero load-bearing facts refuted**; all corrections were citation-placement or wording nits (folded in). Every fact in §2 carries a firm-primary URL + verbatim quote + 2026-07-13 verified date in the envelope §4 rows / `firm_rules` comments.

## §1 — Context

The four-firms ADR §2 step 1 requires DISC-CAMP-0 survivors to declare `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO` against the envelope, and the ratified survivor-scoring recommendation's G1 (deployable decomposition) and G2 (cost-law kill gate) gates consume it. Scoring against a PROVISIONAL v0.1 risked wasted verdicts if E1/E2/E7 shifted at ratification, and G2 was **blocked for 3 of 4 firms** (no commission data). With DISC-CAMP-0 unfrozen (operator, 2026-07-12) survivors are imminent — the envelope had to ratify first.

## §2 — Decision (resolving the five v0.1 open items)

1. **E1 default flat-deadline print: 16:00 ET CONFIRMED.** Verified prints: MFFU **16:10 ET** auto-liq (the binding minimum; "4:10 PM EST", holiday half-days have NO auto-liq and post-deadline orders can disqualify) · BluSky **~16:45 ET** derived (auto-liq ~15m pre-close, best-effort) · Bulenox **16:59 ET year-round** (15:59 CT; the v0.1 row's summer/winter ET split was **erroneous** — CT/ET shift together on US DST) · Tradeify **16:59 ET** (12:59 ET holiday-short; all account types; auto-flatten non-fatal). 16:00 ET sits strictly inside every print with ≥10-min buffer. Design consequence added: never design to the auto-flatten as a backstop (miss-consequences range from benign-slippage to disqualification).
2. **E2 checkpoint semantics: SOFT ELIGIBILITY GATE, never a breach — at all four firms.** Tradeify Select 40% at-eval-pass only (removed funded); MFFU 50% eval-only (none sim-funded/payout); BluSky 34% target-re-scale; Bulenox 40% checkpoint-at-withdrawal (blocks payout, never violates; **now primary-sourced**, upgrading the v0.1 community-audit citation). Consequence: a concentrated edge is not eval-fatal, it is eval-*hostile* — the delay extends exposure to the trailing barrier. **This validates the MC engine's existing consistency modeling** (`core/mc/simulation.py` keeps a profit-concentrated account trading until consistent — exactly the verified firm semantics), so the recommendation's Run-2-gates rule stands unmodified.
3. **E7 news restrictions: stays OVERLAY-ONLY** (firm spread irreducible: three allow, MFFU tiers by plan).
4. **Elite Trader Funding: CLOSED PROHIBITIVE (primary-sourced — the Q-AUTO-FIRM-1 INSUFFICIENT is discharged).** ToS clause (ac) default-prohibits owner-operated automation absent unpublished written authorization; only account-to-account trade copiers are pre-approved; clause (ah) = 10-second minimum trade duration. **ETF stays out of `AUTOMATION_FRIENDLY_PROP_FIRMS`.**
5. **Commissions single-sourced into `core/firm_rules.py` (`cost_per_side_usd`, all-in per-side, index micros):** Tradeify **$0.91** (RT $1.82; MGC $1.06; platform-uniform; **no M6J**) · MFFU **$0.95** (RT $1.90; MGC $1.10; M6E $0.72; **no M6J**) · BluSky **$0.95 NT-rail conservative** (BluSky's own Rithmic-class eval rail is $0.50 flat all micros, but the declared TV→CrossTrade→NT8 rail pays the NinjaTrader brokerage schedule; funded pricing is "set by brokerage" with no firm figures) · Bulenox $0.61 re-verified byte-exact (still Sept-2024 vintage — STALE flag retained; per-side annotated as arithmetically-forced inference, PDF prints only "ALL IN RATES"). Tradeify tiers additionally gain `consistency_rule_pct: 40.0` (closes the recommendation §2.4(5) flagged gap). Guard test extended: **every FRIENDLY tier must carry a plausible `cost_per_side_usd`** — the G2 cost gate is now structurally unblockable-by-omission.

**Incidental load-bearing finding (routed to `ops/instruments/6J.md`):** M6J (micro JPY) is offered by NONE of Tradeify / MFFU / Bulenox (full-size 6J only at $3.10 / $2.56 / $2.36 per side). The self-funded Aegis→M6J lane is unaffected (doesn't route through prop firms); any future prop-hosted JPY-micro idea is dead on product availability.

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Ratify v1.0 without re-verifying v0.1 rows | v0.1 carried a confirmed error (Bulenox seasonal ET split) and a Tier-3 citation (Bulenox 40%) — ratifying unverified rows bakes both in |
| Keep commissions in envelope prose | Violates the firm-constants single-source ADR (2026-06-06); G2 needs machine-readable values |
| Encode BluSky at its cheaper $0.50 eval rate | Wrong rail — the $0.50 applies on Rithmic/Volumetrica/Tradesea, which don't carry NT8/CrossTrade; encoding it would flatter G2 cost hurdles by ~2× on the declared rail |
| Graduate E7 into the default | Over-constrains 3 firms or under-models MFFU; verified spread is irreducible |
| Admit ETF as a 5th friendly firm (its copier list exists) | Pre-approved copiers ≠ owner-operated strategy automation; clause (ac) default-prohibits the actual rail; authorization path unpublished |

## §4 — Falsifier (revert trigger)

**Reject (stale/wrong) if:** any §4 overlay row's load-bearing cell (deadline, consistency %/semantics, commission) is found to diverge from the firm's current primary doc when re-verified — **then** re-verify that row (90-day stale rule; a row older than 90 days must be re-verified before any deployment-fork use), and if the E1 binding minimum drops **below 16:00 ET** or any firm's consistency becomes a hard mid-eval breach rule, the corresponding §1 default is re-opened by a fresh ADR (never edited in place). **Accept (holds) if** rows re-verify within their 90-day windows. Standing check: the Bulenox Rates.pdf is ALREADY stale (Sept-2024 vintage) — its row may not be used at a deployment fork without re-verification (its byte-hash is pinned in the research record for drift detection: `EEF222E8…D58B8`).

## §5 — Forbidden moves (under this ADR)

- Using `compute_default_config`'s headline bust for any prop tier scored against this envelope (F1 trap — recommendation §1).
- Scoring a candidate against a §4 row older than 90 days without re-verification.
- Treating the E1 auto-flatten as a design backstop (MFFU disqualification risk; BluSky best-effort).
- Swapping BluSky's `cost_per_side_usd` to $0.50 while the declared rail is TV→CrossTrade→NT8.
- Re-admitting ETF via its copier list without a written firm authorization for owner-operated strategy automation.
- Hard-coding any of these firm facts in `lab/` research artifacts (envelope §2.4 — deployment-fork only).

## §6 — Consequences

**Positive:** G1/G2 fully runnable for all four firms (the scoring pre-registration's only remaining blocker is the engine pre-flight); v0.1's confirmed error + Tier-3 citation repaired; Bulenox 40% upgraded to primary; ETF permanently disposed; the engine's consistency modeling is now evidence-backed rather than assumed.
**Negative (real cost):** BluSky's funded-tier commission is a NinjaTrader-retail-schedule proxy (firm publishes no figure) — flagged, not hidden; MFFU's "EST" prints carry an ET-prevailing assumption (flagged); the Bulenox schedule remains stale pending the firm re-publishing.

**Downstream artifacts updated:** `ops/prop_envelope_default.md` (v1.0), `core/firm_rules.py` (additive fields + provenance comments), `tests/core/test_automation_friendly_prop_firms.py` (cost guard), `ops/instruments/6J.md` (M6J-availability line), `STATE.md`.
**NOT changed:** `ACTIVE_FIRM`, FXIFY config, locked allocations, `dd_protection` constants, MC pins, Pine.

## §10 — Audit hooks (runnable)

```bash
# Every FRIENDLY tier carries a plausible all-in per-side cost (the G2 guard)
python -m pytest tests/core/test_automation_friendly_prop_firms.py -q

# Envelope is v1.0 and cites this ADR
grep -n "v1.0, RATIFIED\|2026-07-13-prop-envelope-v1-ratification" ops/prop_envelope_default.md

# The five §5 resolutions are recorded (expect all five numbered items)
grep -n "CONFIRMED 16:00 ET\|soft eligibility gate\|OVERLAY-ONLY\|CLOSED PROHIBITIVE\|single-sourced" -i docs/adr/2026-07-13-prop-envelope-v1-ratification.md

# 90-day staleness: every §4 row carries a 2026-07-13 verified date (re-check quarterly)
grep -c "2026-07-13" ops/prop_envelope_default.md

# The M6J finding reached the instrument ledger
grep -n "M6J" ops/instruments/6J.md

# Locked surfaces untouched
# HOOK REPAIRED 2026-08-03 (Rule 11 back-propagation, gate-stack audit R8). Two retirements
# broke the original two lines and BOTH raised rather than reporting:
#   * ACTIVE_FIRM + FIRM_RULES["FXIFY"] deleted 2026-07-30 (substrate Phase 4, fc14682) ->
#     the fixture assert raised AttributeError. Historical challenge semantics moved to
#     core/historical_challenge.py, which is where the FXIFY pin now lives.
#   * scripts/validate_params.py deleted 2026-08-03 (PR #624, 2026-08-03-params-toml-gate-retirement.md).
python scripts/verify_lock_anchors.py && python scripts/check_pine_manifest.py
python -c "import sys; sys.path.insert(0,'core'); import historical_challenge as h; assert h.DAILY_LOSS_PCT_SIGNED == -0.05 and h.HISTORICAL_CHALLENGE_BALANCE == 200_000.0; print('historical FXIFY fixture OK')"
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-13 | Initial acceptance; v0.1 → v1.0 | Joshua + Claude Code |
