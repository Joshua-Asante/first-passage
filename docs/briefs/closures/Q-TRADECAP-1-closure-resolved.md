# Q-TRADECAP-1 — CLOSURE: `RESOLVED` (no per-trade dollar-loss bound exists anywhere in the live sizing/arming path)

**Verdict:** `RESOLVED`
**Closed:** 2026-08-23
**Lane:** `UNASSIGNED`
**Pre-registration:** [`Q-TRADECAP-1-verdict-preregistration.md`](../pre-registration/Q-TRADECAP-1-verdict-preregistration.md) — frozen 2026-08-23, before Phase 1 ran
**Spend / K:** $0.00 · K consumed: 0 (inventory/triage depth — repo-wide grep + two end-to-end code reads, no data pull, no simulation)
**Live effect:** none — this brief confirms an absence, it authors no fix; no `dd_protection`/allocation/Pine/rail surface touched
**Artifacts:** none beyond this closure and the terminal output quoted below (no script — the four checks are the grep/read commands in the parent brief's own §10, executed directly)

---

## 1. Verdict (§6 asserted against actual results)

| §6 route | Trigger condition | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | All four checks confirm no genuine bound exists — every classifiable hit sorts into a non-bound category | All four checks confirm absence (below) | ✓ |
| `FALSIFIED` | Any check surfaces a genuine live per-trade-dollar bound | Not found | — |
| `AMBIGUOUS-HOLD` | A grep hit cannot be cleanly sorted into the frozen classification categories | Every hit sorted cleanly | — |

## 2. Per-check results

**Check 1 — repo-wide absence sweep** (`core/ ops/ docs/adr/ docs/spec/ docs/notes/rail_build/`, pattern `(per.?trade|single.?trade|loss.?cap|max.?loss|risk.?per.?trade)`): every hit sorts into the five frozen categories with no residue —
- **sizing-law-% input**: the `riskPerTrade`/`_BASE_RISK` percentage fields across the four locked strategies' LOCK/CHANGELOG docs and ADRs (0.34–1.50% of equity, not a dollar cap).
- **account-level lock**: `core/firm_rules.py:377` "Max Loss Lock at $100" (already classified false positive, §0/§5 of the parent brief).
- **daily-cadence target**: `docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md` — `L = $325`, a **daily** stop-down for a still-under-design candidate spec, not wired into `dd_protection.py` or the live rail (already classified false positive).
- **design-time screen**: `EM2` ("risk-per-trade ceiling") in `docs/spec/2026-08-05-eval-mechanism-shape-screen.md` — a candidate-admission gate for future discovery candidates, zero hits in any code path.
- **forward-owed reporting, not a live control**: `ops/prop_envelope_default.md:28` — per-trade excursion **reporting** required of any candidate advancing to a deployment fork; a documentation requirement for a future decision, not a bound that exists today.
- Zero hits in `ops/c1_rail/*` or any `.py` file — the live rail code itself carries none of these tokens.

**Check 2 — `core/dd_protection.py` `calculate_protection()`, L190–226 (read in full):** the function computes `dd_from_peak`, compares against `DD_TRIGGER`, and returns a `multiplier`/`scaled_risk` dict — every field is a function of `(equity, peak, lifecycle)` only. No per-trade-dollar parameter, field, or return key anywhere. **Limb-Sizing confirmed: no bound.**

**Check 3 — `ops/c1_rail/c1_rail_arm.py` `m1_acceptance_reason()` / `scripts/validate_c1_monitoring_acceptance.py` `REQUIRED_DRILLS` (read in full):** `REQUIRED_DRILLS` is exactly the six transport/reconciliation-shaped keys named in the parent brief's §0 (`transport_unknown`, `partial_fill_confirmed_base`, `rejected_entry_no_add`, `exit_on_equity_failure`, `restart_confirmed_base`, `b6_wrong_secret_shape`) — no seventh, no risk-of-ruin-shaped drill. **Limb-Arming confirmed: no bound.**

**Check 4 — EM2 / disaster-stop wiring:** `grep -rn "EM2" docs/spec/2026-08-05-eval-mechanism-shape-screen.md ops/` → every hit is inside the design-time spec itself or a prose mention in `ops/instruments/MCL.md` scoring an unrelated CL candidate; zero hits in any code path. `grep -rniE "disaster.?stop|protective_stop" ops/` → **zero hits anywhere** — the disaster-stop payload (GO'd 2026-08-22, `docs/adr/2026-07-28-c1-disaster-stop-payload-supported.md`, Phase 0a recorded `BLOCKED` 2026-08-23) is not implemented in `ops/` at all yet. **Limb-Adjacent confirmed: neither is a live arming precondition.**

## 3. What this closure does NOT license

- Does not design, size, or wire the fix. Per the parent brief's own §5, that is a separate, superseding decision packet.
- Does not touch `dd_protection.py`, `firm_rules.py`, `core/lifecycle.py`, or any live rail code.
- Does not re-open or re-litigate any of the already-classified false positives (daily max-loss `L`, EM2, account-level Max Loss Lock) — reused verbatim from the parent brief's §0/§5, not re-derived.

## 4. Defects found in the frozen brief

None. The Phase 1 reads confirmed the parent brief's own §0 pre-registration reads exactly — no surprise hit, no reclassification.

## 5. Successor decision packet (per §6's `RESOLVED` disposition — a STATE.md row is owed, not this brief's to open)

`docs/methodology/1r_estimation.md` (L231–263) pre-staged exactly this fork on 2025-02-07's 71.2%-of-daily-budget single-trade finding, gated on "the next allocation review or 6-month live reconciliation" — a trigger that never fired because the CFD estate retired before either did, and the question was never re-scoped to Tradeify_Select_100K's harsher intraday-enforced geometry. Two named options, unchanged, neither elected here:

1. **Within-day per-trade hard-cap** — a tripwire layered on the existing daily-cadence rule, capping a single trade's realized loss at e.g. 2.0% of equity at entry. Closes the gap by construction. Cost: adds operational surface area, and 94% of historical Striker profit sits above the cap-clip threshold for the largest pyramid stacks — needs a re-MC to confirm the cap doesn't over-attenuate PF.
2. **Leave the rule, observe live with a tripwire** — an alert (not an auto-cap) firing when any single trade exceeds 2.0% of equity at entry, accepting that with n=1 historical fresh-peak single-trade outliers in four years, the real base rate is only estimable from live data.

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Model update:** the audit note's finding A6 is confirmed real and total, not a triage overstatement — nothing anywhere in the repo's code, ADRs, specs, or the M1 acceptance package bounds a single trade's realized dollar loss on the venue geometry (`Tradeify_Select_100K`, intraday-enforced trailing DD) the c1 rail arms against. This is a structural gap the CFD-era 1R-estimation Forward question already named and staged a fork for — it was never closed, only orphaned by the CFD retirement removing its trigger.
- **Next:** `ITERATE` — successor decision packet named above, not opened here.
- **Routing:** a STATE.md OPERATOR QUEUE row, naming the two-option fork above, for operator election.
- **Entry packet:** the two options in §5 above, byte-carried from `1r_estimation.md` L240–256, re-scoped to Tradeify_Select_100K rather than the CFD-era panel.
- **Stop rule / re-proposal bar:** N/A for this closure (it discharges cleanly); the successor packet's own re-proposal bar is standard operator election, no falsifier needed to open it.
- **Board write:** `STATE.md` OPERATOR QUEUE (new row) + decision index; `docs/briefs/INDEX.md` — this Q moves from Open to Recently closed. Owner: this closure.
- **Registry:** no `docs/rejected_candidates.md` row — this confirms an absence in live risk infrastructure, not a candidate/mechanism kill.

## §10 audit-hook discharge

```bash
$ grep -rniE "(per.?trade|single.?trade|loss.?cap|max.?loss|risk.?per.?trade)" core/ ops/ docs/adr/ docs/spec/ docs/notes/rail_build/ | grep -c "ops/c1_rail"
0

$ sed -n '190,226p' core/dd_protection.py | grep -ciE "per.?trade.?(dollar|cap|bound)"
0

$ sed -n '40,58p' scripts/validate_c1_monitoring_acceptance.py | grep -c "REQUIRED_DRILLS"
1

$ grep -rniE "disaster.?stop|protective_stop" ops/ | wc -l
0
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure authored. Pre-registration committed, Phase 1 executed same session under operator GO ("GO on Q-TRADECAP-1"). `RESOLVED` recorded. | Claude Code (Sonnet 5), operator GO |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-TRADECAP-1-closure-resolved.md
```
