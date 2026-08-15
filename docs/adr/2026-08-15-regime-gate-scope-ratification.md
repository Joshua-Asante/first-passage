# ADR 2026-08-15 — Ratify the 2026-08-02 regime-robustness-gate scope narrowing (discharges F1)

**Status:** `Accepted` — ratified by operator (JA) 2026-08-15, in-session instruction ("address F1 ... as a Cursor task" → routed to CC per the cursor-fleet skill's own locked-surface disqualifier; operator's dispatch instruction stands as the ratification)
**Decision date:** 2026-08-15
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** governance convention. **$0 / K=0.**

## Decision

The 2026-08-02 addition to [`regime_robustness_gate.md`](../methodology/regime_robustness_gate.md) §"Not required for" — "ORB-MNQ / venue-native research that does not change locked risk constants" plus "Do not fire it as ceremony on tooling or research CSVs with no risk-constant change" plus the LOCK-CANDIDATE conditioning — is **ratified as-is, not reverted**. No text changes.

## Grounds

The gate's own opening section states its hard core is specifically Pareto-relaxation sweeps on `dd_protection`-class constants ("this gate exists because of one structural asymmetry... in any Pareto-relaxation question on `dd_protection` or analogous risk constants"). c1/MSL/TNEC candidate-generation research (ORB-MNQ, MSL cards, dense-1m, Route-B) proposes new *strategy candidates* — already separately covered by "Adding / removing strategies" and "Strategy parameter changes" in the same Not-required list, both present since canonization (`26f3a26`, 2026-05-06) — never a `DD_TRIGGER`/`DD_SCALE` relaxation. The 2026-08-02 line is a clarification consistent with the gate's own stated scope, not a substantive loosening; reverting it would force the gate onto research that structurally cannot touch a locked risk constant, at MSL's current multi-G0-freeze-per-day cadence — genuine ceremony, the exact failure mode the gate's own guidance warns against ("Do not fire it as ceremony").

## Reads

`docs/methodology/regime_robustness_gate.md` @ `ae8646c` (2026-08-11, unrelated later touch; the narrowing itself is `cd8b617` 2026-08-02, `chore: prune retired FXIFY/NT8 surfaces off the live mission path`) · [2026-08-03 gate-stack audit](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) §3.4/§4.1 (G4 Degenerating, F1) · [2026-08-15 wall-scope audit](../notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md) §2 (re-verification, F1 still-owed at 7 days overdue).

## Gate

RESOLVED — this record itself discharges F1. No further trigger; a future scope change to this gate needs a fresh ADR, not an in-place edit.

## Boundary

Do not read this as re-opening the gate's mandatory scope (Pareto sweeps on `dd_protection`-class constants remain fully mandatory, unchanged). Do not cite this ADR to exempt a brief that *does* propose a risk-constant relaxation.
