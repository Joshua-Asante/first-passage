# Q-TRADECAP-2 — Verdict pre-registration

**Frozen:** 2026-08-24, before Phase 1 (operator election). Parent
[`Q-TRADECAP-1`](../Q-TRADECAP-1-per-trade-loss-bound.md) is closed `RESOLVED`
and is not re-opened. Byte-unedited from this point forward — amendments via a
fresh Q (brief-authoring Known Trap #12).

---

## Frozen option set (exactly these; no fourth invented post-hoc)

| ID | Close | What it bounds | Startable on current `main`? |
|---|---|---|---|
| **2** | Alert tripwire | Observation — fires when a single trade's realized loss exceeds a named threshold; does not flatten | Yes (dark until a strategy-signal fill) |
| **1-size** | Entry-size dollar ceiling | Size at entry (`qty` such that intended $ risk ≤ bound). Does **not** cap in-flight realized loss | Yes (sizing-host / listener). Distinct from the CFD-era Option 1 |
| **1-realized** | Within-day realized-loss hard-cap | In-flight flatten / broker-side stop when realized loss hits the bound | **No** — gated on disaster-stop Phase 0a `PASS` + Phase 1 `sl=` wiring ([ADR](../../adr/2026-07-28-c1-disaster-stop-payload-supported.md); Phase 0a `BLOCKED` 2026-08-23) |

The CFD-era pair in [`1r_estimation.md`](../../methodology/1r_estimation.md)
L244–260 is **2** vs **1-realized**. **1-size** is the third option the M1 ADR
already named as a different axis ("bounds size" ≠ "bounds realized magnitude").

## Frozen geometry predicates (Phase 0; $0 / K=0)

Measured against `core/firm_rules.py` `Tradeify_Select_100K` and the listener
call site. A predicate flip after freeze is a fresh Q, not an in-place edit.

| ID | Predicate | Startable-Option-1-as-staged if |
|---|---|---|
| G1 | `daily_loss_pct is None` | G1 is false (a daily-loss layer exists to layer a cap on) |
| G2 | CFD example `0.02 × starting_balance` ≥ **50%** of `starting_balance × max_dd_pct` | G2 is false (the 2.0% example is a small fraction of the venue trail) |
| G3 | `c1_rail_listener.py` `build_crosstrade_payload(...)` does not pass `sl=` | G3 is false (`sl=` is live at the only call site) |

**Option 1-as-originally-staged is not startable** iff G1 ∧ G2 ∧ G3 all hold.

## Gate criteria

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | Operator elects exactly one of {**2**, **1-size**, **1-realized**} and the election is recorded on an owning artifact (light ADR if no live-risk wire; full ADR before any `dd_protection` / arming / `sl=` change) | `INTEGRATE` — close this Q; implement only the elected close; do not wire the other two |
| `FALSIFIED` | Any of G1/G2/G3 is false on the frozen owners (Option 1-as-staged is startable; the original two-option fork stands unmodified) | `ITERATE` — name (not open) a packet that elects the original pair without the third option |
| `AMBIGUOUS-HOLD` | Operator declines all three named closes and also declines to delete STATE queue row 2 | `ITERATE` — re-test at the next arming GO or disaster-stop Phase 0a `PASS`, whichever is first |

## Explicit non-negotiables

- Do not import **2.0%** as the Tradeify threshold. Threshold is a separate
  election after form is chosen; CFD 2.0% is the example under test in G2, not
  a candidate number.
- Do not wire **1-realized** before Phase 0a `PASS`.
- Do not treat **1-size** as discharging the realized-loss gap.
- Do not change `DD_TRIGGER` / `DD_SCALE` / `BASE_RISK` to manufacture a bound.
- Do not re-open Q-TRADECAP-1.

**Committed:** 2026-08-24. Phase 1 (operator election) has not run as of this commit.
