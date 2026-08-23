# Q-TRADECAP-1 — Is there any bound on a single trade's realized dollar loss?

**Status:** `CLOSED-RESOLVED 2026-08-23` — all four checks confirm no per-trade dollar-loss bound exists anywhere in the live sizing/arming path. Closure: [`closures/Q-TRADECAP-1-closure-resolved.md`](closures/Q-TRADECAP-1-closure-resolved.md).
**Authored:** 2026-08-18
**Closed:** 2026-08-23
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the 2026-08-18 assumption-sweep audit note, finding A6
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on a locational read of already-cited artifacts (the sizing law, the M1 arming-gate acceptance package, and two candidate adjacent controls) for a per-trade-dollar-loss bound
**Artifact path:** `docs/briefs/Q-TRADECAP-1-per-trade-loss-bound.md`

---

## Section 0 — Rule 0 reads (production-source verification, executed 2026-08-18)

- `core/dd_protection.py:190-226` (`calculate_protection`) — read in full range this session. The multiplier is derived purely from `(equity, peak)` via `dd_from_peak` compared against `DD_TRIGGER`; `scaled_risk = BASE_RISK × multiplier × lifecycle`. No parameter, field, or return key bounds a single trade's dollar loss — the function's entire output is a sizing multiplier for the *next* trade-day, not an intra-trade limit.
- `docs/methodology/1r_estimation.md:191-263`, esp. `:198` and `:231-263` — read in full range this session. Line 198: the 2025-02-07 fresh-peak Striker trade consumed **71.2%** of the 5.00% FXIFY daily-DD budget in one shot. Line 231's own "Pre-staged Forward question" names the category gap explicitly — `dd_protection`'s daily cadence "cannot, by construction, attenuate a fresh-peak single-trade outlier" (line 233) — and stages two responses (within-day per-trade hard-cap vs. live-observed tripwire), gated on "the next allocation review or 6-month live reconciliation" (line 237). Neither trigger has fired.
- `docs/adr/2026-07-11-ops-cfd-estate-retirement.md` — read this session. Retires the CFD/manual-execution estate wholesale. The allocation-review / 6-month-reconciliation cadence the 1R-estimation Forward question was staged against was CFD-era operational rhythm; it was retired here without the Forward question ever being re-raised or re-gated to the harsher, intraday-enforced Tradeify_Select_100K environment.
- `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md:696-707` — read in full range this session. Explicitly distinguishes `reserve_cap` ("bounds **size**") from item 5 ("bounds signal **identity**"). No third axis — bounds loss **magnitude once sized** — is named anywhere in that ADR.
- `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json:8-15` — read this session. The six `REQUIRED_DRILLS` keys (`transport_unknown`, `partial_fill_confirmed_base`, `rejected_entry_no_add`, `exit_on_equity_failure`, `restart_confirmed_base`, `b6_wrong_secret_shape`) are exhaustively transport/reconciliation-shaped; none is risk-of-ruin-shaped.
- `scripts/validate_c1_monitoring_acceptance.py:51-58` (`REQUIRED_DRILLS`) — read this session. Schema owner backing the JSON above; same six keys, no seventh.
- `ops/c1_rail/c1_rail_arm.py:79-106` (`m1_acceptance_reason`, the arming interlock's `validate()` entry point) — read this session. Fails closed on anything short of a validator-passing `RESOLVED` (`require_resolved=True`); the interlock re-derives schema/status fields only, never a per-trade-loss property.
- `docs/spec/2026-08-05-eval-mechanism-shape-screen.md:85` (EM2, "Risk-per-trade ceiling") — read this session. EM2 is a **candidate-admission screen** for future discovery candidates (an edge-indexed $ ceiling vs. a $3,000 fixed rope), not a live sizing/arming control. `grep -rn "EM2" ops/` → **2 hits, both in `ops/instruments/MCL.md`** (an intake-screening notes doc recording EM2 as a scored *gate name* against an unrelated CL candidate, not code); zero hits in `ops/c1_rail/`, any `.py` file, or anything consuming/wiring EM2 into the live rail.
- `docs/adr/2026-07-28-c1-disaster-stop-payload-supported.md` — read this session. Proposes a rail-side, payload-supported, broker-side stop. `grep -rniE "disaster.?stop|protective_stop" ops/` → 0 hits — the mechanism is not implemented or wired into the live rail code.

---

## Section 1 — Context and motivation

This Q is opened directly from finding **A6** of the 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`, §4 Tier A). A6 sits inside the audit's own named cross-cutting pattern (§6): six of 25 findings (A2, A3, A4, A5, A6, D6) cluster on one theme — the c1 rail's live-safety interlocks are described in prose (ADRs, acceptance packages, docstrings) with more rigor than they are wired in code. A6 is the risk-of-ruin instance of that pattern: `dd_protection`'s daily-cadence sizing rule is real and doing real work, but it is reactive and next-trade-day by construction (`docs/methodology/1r_estimation.md:208-217`) — it cannot cap an in-flight trade. The M1 arming ADR itself named a "bounds size" vs. "bounds identity" distinction (`:696-707`) but never posed the third, structurally distinct question this Q asks. The gap is a dormant orphan, not a fresh discovery: `1r_estimation.md` staged it explicitly and gated it on CFD-era triggers that were retired before either fired, and it was never re-scoped to Tradeify_Select_100K's harsher intraday-enforced trailing-DD geometry.

---

## Section 2 — Prior art / lineage

- **2026-08-18 assumption-sweep audit note**, finding A6 (§4 Tier A) — the direct origin of this Q; also cited in §9 (aggregated audit hooks) and named in the audit's Iterate block as carrying its own frozen H + falsifier sketch as its entry packet.
- **Audit note §3 (D-gate deletions)** — none of the five deleted candidates cover A6. The nearest adjacent item, §3.5 (Harvest Requirement 5's cost-law hurdle resting on the unmeasured `SLIPPAGE_TICKS_PER_SIDE` constant), is a **different mechanism** (execution-cost realism for candidate screening, not a live per-trade loss bound) and its own closure explicitly forbids retro-application outside its scope — this Q does not touch it.
- **`docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md`** — supplies the "bounds size / bounds identity" distinction this Q completes with a third axis; not re-litigated, only extended.
- **`docs/methodology/1r_estimation.md`** — the only place in the repo the per-trade-cap question was ever posed. This Q re-dates and re-scopes it; it does not re-derive it.

---

## Section 3 — Question (Q-TRADECAP-1)

**Pre-Q gate test (symptom-only rephrase):** "a single trade's realized dollar loss is currently unbounded everywhere the live rail's own record has been checked; it is unknown whether that is still true once every named candidate control is read end-to-end, or whether some artifact already closes the gap without having been recognized as doing so." No fix baked in — the question does not mention adding, wiring, or sizing a cap.

**Q-TRADECAP-1:** Is there any point in the live sizing/arming path — the sizing law, the M1 arming gate, or either of the two candidate adjacent controls (EM2, the disaster-stop payload) — where a single trade's realized dollar loss is actually bounded, on the venue geometry (Tradeify_Select_100K, intraday-enforced trailing DD) the c1 rail is built and disarmed against?

---

## Section 4 — Falsifiable hypothesis (H-TRADECAP-1)

**H-TRADECAP-1**, three named limbs:
- **Limb-Sizing:** `dd_protection`'s sizing law (`calculate_protection`, consumed by the c1 sizing host) carries no per-trade-dollar-loss parameter.
- **Limb-Arming:** the M1 arming interlock's `REQUIRED_DRILLS` / acceptance criteria carries no risk-of-ruin-shaped drill.
- **Limb-Adjacent:** neither EM2 (candidate-admission screen) nor the disaster-stop payload (proposed, unimplemented) is wired as a live arming precondition for Tradeify_Select_100K.

**If all three limbs hold**, the elision named in this Q's motivation is confirmed real and total: nothing anywhere in the repo's code, ADRs, specs, or the M1 acceptance package bounds a single trade's realized dollar loss on the venue geometry the rail arms against. **If any limb fails** — a bound is actually found wired, not merely described — the elision is partially or fully false and the gap is narrower than the audit assumed.

**Reject H-TRADECAP-1 if:** the Phase 1 reads (§7/§10) surface a per-trade-dollar-loss parameter actually consumed by `calculate_protection()`/the c1 sizing host, **or** a `REQUIRED_DRILLS` key (or interlock code path) that checks single-trade loss magnitude, **or** EM2/the disaster-stop payload referenced from `ops/c1_rail/*` as a live precondition rather than a standalone document.
**Accept H-TRADECAP-1 if:** all three limbs hold as already verified in §0, **and** the repo-wide grep (`core/ ops/ docs/adr/ docs/spec/ docs/notes/rail_build/`) turns up no per-trade-dollar-cap hit beyond the already-classified false positives (risk-per-trade **%** sizing inputs, the account-level "Max Loss Lock" in `firm_rules.py`, the **daily** max-loss `L` in `docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md`).
**Ambiguous-hold if:** the repo-wide grep surfaces a genuinely new hit that cannot be cleanly classified as sizing-law input / account-level lock / daily-cadence target / design-time screen / genuine bound without judgment this $0/K=0 brief cannot exercise.

---

## Section 5 — Forbidden moves

- **Treating "`dd_protection` scales sizing on the NEXT trade-day" as "no single trade can do outsized damage."** This is the seeded elision the Q exists to test. `dd_protection` is reactive and daily-cadence by construction (`core/dd_protection.py:190-226`; `1r_estimation.md:208-217` names this design-intentional) — it cannot cap an in-flight trade. Ruled out because accepting it would close this Q before Phase 1 runs.
- **Treating the "max-loss `L`" in `docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md` as a per-trade bound.** It is a **daily** stop-down target for a candidate spec still under design, not wired into the live c1 rail or `dd_protection` at all — the same category error as the seeded one, one layer removed. Found live during this brief's own §0/repo-wide grep, not a strawman.
- **Treating EM2 ("Risk-per-trade ceiling," `docs/spec/2026-08-05-eval-mechanism-shape-screen.md:85`) as an existing per-trade bound because its name matches.** It is a candidate-**admission** screen for future discovery candidates (pre-registration gate), never consumed by `ops/c1_rail/*` or `dd_protection.py`, and scores hypothetical candidates — not live trades. `grep -rn "EM2" ops/` returns 2 hits, both prose references in `ops/instruments/MCL.md` scoring an unrelated CL candidate — zero hits in any code path or in `ops/c1_rail/` (§0).
- **Substituting `core/firm_rules.py`'s account-level "Max Loss Lock at $100" for a per-trade bound.** Different unit of analysis (account-level trailing lock vs. single trade) — already ruled a false positive by the repo-wide grep run for §0.
- **Designing or proposing the actual bound (hard-cap value, tripwire threshold, disaster-stop wiring) under this brief.** This is an Inquire-phase Pre-Q; `1r_estimation.md` already named two candidate responses and explicitly deferred the choice. This brief's job is to confirm and re-date the gap, not to design the fix — that is a separate, superseding decision packet, named but not opened in Section 6.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | All three limbs hold: no per-trade-dollar-loss parameter in `dd_protection`/the c1 sizing host; no risk-of-ruin-shaped drill in `REQUIRED_DRILLS`/the M1 interlock; EM2 and the disaster-stop payload confirmed unwired into `ops/c1_rail/*`; repo-wide grep returns only already-classified false positives | `INTEGRATE` — record A6 as formally confirmed (not merely triaged); discharge the audit finding with citation; add a `STATE.md` OPERATOR QUEUE row naming a successor decision packet (per `1r_estimation.md`'s own two staged options) for operator election. This brief authors no fix. |
| `FALSIFIED` | Any limb fails — a per-trade-dollar-loss bound is found actually wired into the sizing law, the arming gate, or as a live arming precondition | `ITERATE` — name (not open) a successor packet to confirm the found bound's coverage against the Tradeify_Select_100K intraday-enforced geometry specifically; a bound proven only against the CFD/EOD geometry does not transfer (per the harsher-regime finding in §0/§1). |
| `AMBIGUOUS-HOLD` | Repo-wide grep surfaces a genuinely unclassifiable candidate hit requiring judgment beyond $0/K=0 static reads | `ITERATE` — re-test when the ambiguous hit is resolved by its own owning artifact's next edit, or at the next c1-rail arming session, whichever is first. |

**Pre-registered before any gate fact beyond §0 is read.** §6 is not amended to match what Phase 1 returns (Known Trap #12).

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1 — Per-limb cheap falsifiers, reusing the audit note's own hooks verbatim:**
  - **Limb-Sizing + Limb-Arming (absence check):** `rg -i "(per.?trade|single.?trade|loss.?cap|max.?loss|risk.?per.?trade)" core/ ops/ docs/adr/ docs/spec/ docs/notes/rail_build/` — classify every hit as sizing-law-% input / account-lock / daily-cadence-target / design-time-screen / **genuine bound**.
  - **Limb-Sizing (end-to-end read):** `core/dd_protection.py`'s `calculate_protection()` for a per-trade-dollar-cap parameter.
  - **Limb-Arming (end-to-end read):** `ops/c1_rail/c1_rail_arm.py`'s `validate()`/`REQUIRED_DRILLS` chain (via `scripts/validate_c1_monitoring_acceptance.py`) for the same.
  - **Limb-Adjacent:** grep for `"EM2"` and `"disaster.stop"` to check whether either is wired as an arming precondition rather than a standalone doc.
- **Phase 2 — Verdict assertion per Section 6.**

Estimated cost: **$0, K = 0, no manifest.** No new backtest, data pull, or spend of any kind — this is inventory + triage depth, not a K-spending investigation.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, committed before Phase 1 executes. Not yet authored — this Q is named, not opened.

---

## Section 9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block. `RESOLVED` → `docs/briefs/closures/Q-TRADECAP-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` with the re-test trigger named.

---

## Section 10 — Audit hooks (runnable)

```bash
# Limb-Sizing + Limb-Arming: repo-wide absence check
# (already run over ops/ and ops/c1_rail specifically for this brief: 0 hits in the live path)
rg -i "(per.?trade|single.?trade|loss.?cap|max.?loss|risk.?per.?trade)" core/ ops/ docs/adr/ docs/spec/ docs/notes/rail_build/

# Limb-Sizing: end-to-end read for a per-trade-dollar-cap parameter
sed -n '190,226p' core/dd_protection.py

# Limb-Arming: end-to-end read of the arming interlock's validate() entry point + REQUIRED_DRILLS schema owner
sed -n '79,106p' ops/c1_rail/c1_rail_arm.py
sed -n '40,58p' scripts/validate_c1_monitoring_acceptance.py

# Limb-Adjacent: EM2 / disaster-stop wiring check
grep -rn "EM2" docs/spec/2026-08-05-eval-mechanism-shape-screen.md ops/
grep -rniE "disaster.?stop|protective_stop" ops/
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-TRADECAP-1-per-trade-loss-bound.md --type inquire
# Expected: all 6 checks PASS

# Production-source verification (Section 0 anchors)
sed -n '190,226p' core/dd_protection.py
sed -n '191,263p' docs/methodology/1r_estimation.md
sed -n '696,707p' docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md
sed -n '1,25p' docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
sed -n '51,58p' scripts/validate_c1_monitoring_acceptance.py
sed -n '79,106p' ops/c1_rail/c1_rail_arm.py
grep -n "EM2" docs/spec/2026-08-05-eval-mechanism-shape-screen.md
grep -rniE "disaster.?stop|protective_stop" ops/

# Cross-reference: the 71.2% figure and its source
grep -n "71.2%" docs/methodology/1r_estimation.md
```

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary (three limbs, all-hold vs. any-fail)
- [x] Section 5 forbidden moves genuinely tempting — three (daily max-loss `L`, EM2, account-level Max Loss Lock) were live near-misses surfaced by this brief's own §0 reads, not strawmen
- [x] Section 6 triggers specific
- [x] Section 8 pre-registration committed 2026-08-23, before Phase 1 ran
- [x] Section 10 hooks runnable
- [x] Operator GO given 2026-08-23 ("GO on Q-TRADECAP-1"); Phase 1 executed same session — see [`closures/Q-TRADECAP-1-closure-resolved.md`](closures/Q-TRADECAP-1-closure-resolved.md)
