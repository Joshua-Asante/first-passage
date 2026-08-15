# Pre-registration — Q-RAIL-1 (c1 execution-rail go-live scoping verdict)

**Status:** FROZEN 2026-07-17, before Phase 0 (deployment-fork re-verifies) has executed.
**Parent brief:** [`docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md`](../Q-RAIL-1-c1-execution-rail-go-live-scoping.md)
**Loop of record:** STRATEGIC
**Authored:** 2026-07-17 · Claude Code, operator-ratified same day (chat: "ratify Q-RAIL-1 and Q-PYRPARITY-1, sign the §8 budget," plus a same-session `AskUserQuestion` clarification for the two operator-set items below).

---

## §0 — Rule-0 reads

Inherited by reference from the parent brief's own §0 — not re-derived here. Load-bearing anchors: `core/firm_rules.py` (`a53ee99`, 2026-07-13) — `Tradeify_Select_100K` / `MFFU_Rapid_100K` Tier-1 constants; `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` (`be6dda6`) — G8 "rail/account stay separately gated" + the 90-day commission-freshness deployment-fork re-verify trigger (this brief IS that fork); `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md` (`d85c10c`) — ratified WATCH-1 (0.50×) intake; `docs/ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md` — Tradeify/MFFU ToS + CrossTrade/NT8/Rithmic-Tradovate rail chain; `docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md` (`ba943a1`) §5 — this ADR is not rail-build/spend authorization.

---

## §1 — Context (one line)

c1 is ratified lifecycle CANDIDATE deployable at WATCH-1 (0.50×); this pre-registration freezes the execution-fidelity gate (F1–F5) and the two operator-set §8 items that determine whether the deployment axis is decision-ready.

---

## §4 — Falsifiable hypothesis (frozen verbatim from the parent brief, with the 2026-07-17 budget-deferral amendment)

**H-RAIL-1:** A ToS-compliant, attended-automation execution path for c1's deployable expression exists at ≥1 discharge tier, with every execution-fidelity precondition (F1–F5) individually satisfiable, at an all-in cost within the operator-signed budget (§8).

**Fidelity preconditions (scored PASS / FAIL / BLOCKED-ON-INPUT in Phase 2):** F1 WATCH-1 injection mechanism (gated on Q-PYRPARITY-1's verdict) · F2 integer-sizing feasibility (both legs, both cohorts) · F3 deployable expression exists + matches panel of record · F4 session/EOD semantics · F5 ToS re-verification (90-day rule).

**Reject H-RAIL-1 (`FALSIFIED`) if:** any F1–F5 is FAIL at *both* tiers with no documented recovery route, OR — once the operator sets a Phase-4 ceiling (see budget-clause status below) — the costed chain exceeds it at both tiers.
**Accept H-RAIL-1 (`RESOLVED`) if:** all five preconditions PASS (or executed fallback) at ≥1 tier AND the Phase-4 cost table clears the operator's then-set ceiling.
**Ambiguous-hold if:** ≥1 precondition BLOCKED-ON-INPUT at the 2026-08-01 pre-08-08 check, OR Phases 0–3 complete but Phase 4 has not yet obtained the operator's ceiling sign-off.

**Budget-clause status (frozen 2026-07-17 — this is the operative rule, not a placeholder):** the operator deferred the §8 dollar ceiling to Phase 4. No eval-fee pricing is sourced anywhere in the repo at freeze time. Phases 0–3 proceed fully unblocked (none reference a ceiling); Phase 4 assembles the real cost table and **re-requests a ceiling from the operator at that point** — a fresh sign-off, never an automatic multiple or an assumed number. H-RAIL-1's cost clause stays PENDING until that sign-off.

These numbers/mechanisms are FIXED as of this freeze. Any change requires closing this pre-registration and opening a fresh one (Known Trap #12).

---

## §5 — Forbidden moves (inherited by reference from the parent brief)

- **Registering an account or paying an eval fee during scoping** — spend is gated; this brief produces the decision packet only.
- **Commissioning CrossTrade/NT8/Tradovate wiring during scoping** — build starts only after operator GO.
- **Reusing the Bulenox-parameterized venue editions as-is** — costs, caps, force-flat times, and the promoted day-stop default are all Bulenox-chain decisions; Tradeify/MFFU need a fresh venue-constant pass and hash re-pin.
- **Folding ORB-MNQ-1 go-live into this packet as a co-primary** — rides as a second-wave annex only.
- **Reading c1's panel PF as a live-expectancy promise** — the Class-S claim is bust-geometry survival, not CFD-edge preservation.
- **Quietly widening to lights-out automation** — Q-BTC-3 falsified that lane; attended is the bar.
- **Switching `ACTIVE_FIRM`** — anchor byte-repro guard.

---

## §6 — Gate criteria (frozen, 2026-07-17 amended version)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` (decision-ready) | All five F-preconditions PASS (or fallback) at ≥1 tier; rail chain documented end-to-end; cost table complete; **operator confirms the Phase-4-requested ceiling clears** | Operator GO/NO-GO on rail build + account (fresh ADR on GO) |
| `FALSIFIED` (hard blocker or cost) | Any F1–F5 FAIL at both tiers with no recovery route; OR the operator's Phase-4 ceiling is exceeded at both tiers | Record blocker; research-only on the deployment axis; re-open requires the named input to change |
| `AMBIGUOUS-HOLD` | ≥1 precondition BLOCKED-ON-INPUT at 2026-08-01; OR Phase 4 cost table ready but ceiling sign-off not yet obtained | Carry into the 08-08 packet with the blocking input named |

---

## §8 — Operator-set items (signed 2026-07-17)

- **Target tier preference** if both clear: **"Packet decides"** — no pre-set preference; Phase 4 recommends based on whichever tier clears cleaner / costs less once both are scored.
- **Budget ceiling** for all-in cost-to-first-live-fill: **DEFERRED to Phase 4** — see the budget-clause status in §4. Not a number; a mechanism, fixed as of this freeze.

---

## §10 — Audit hooks (runnable)

```bash
# This pre-registration predates Phase 0 (Trap #12 guard)
git log --oneline -- docs/briefs/pre-registration/Q-RAIL-1-verdict-preregistration.md | tail -1

# Gating language intact until an operator GO exists
grep -n "separately gated" lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md

# Tier-1 constants unchanged since freeze
git log -1 --format='%h %cs' -- core/firm_rules.py    # a53ee99 at freeze; investigate any drift

# No build-before-GO
git log --oneline --all -- "**/crosstrade*" "**/nt8*" | head -5

# The executing session cites this pre-registration (Trap #10)
grep -rn "Q-RAIL-1-verdict-preregistration" docs/SESSIONS.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/pre-registration/Q-RAIL-1-verdict-preregistration.md --type generic
git log -1 --format='%h %cs' -- core/firm_rules.py docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
```
