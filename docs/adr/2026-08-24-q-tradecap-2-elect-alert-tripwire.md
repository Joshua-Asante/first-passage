# Q-TRADECAP-2 elects alert tripwire (observe-only) — `2026-08-24-q-tradecap-2-elect-alert-tripwire`

**Status:** `Proposed` — operator asked for this light ADR and a Claude judgment review; not ratified
**Decision date:** 2026-08-24
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** election record. **$0 / K=0.** No live-risk wire.

Decision: Elect frozen ID **2** (alert tripwire) as the licensed close for [`Q-TRADECAP-2`](../briefs/Q-TRADECAP-2-per-trade-bound-election.md). Observe-only: does not flatten and does not discharge the realized-loss gap. Do not wire **1-size** or **1-realized**. Threshold is a later election; do not import the CFD-era example percent. If a tripwire is later implemented, freeze an MTM-or-dual trigger and threshold-before-first-fill, or accept fail-open on that implementation record.

Grounds: [`Q-TRADECAP-2`](../briefs/Q-TRADECAP-2-per-trade-bound-election.md) · [pre-reg](../briefs/pre-registration/Q-TRADECAP-2-verdict-preregistration.md) @ `4d6761b` · [consult](../notes/notice/N-2026-08-24-ox-alpha-per-trade-bound-election.md) (O4/O5/O6/O7/O9) · operator ask after the consult recommendation.

Reads: `docs/briefs/Q-TRADECAP-2-per-trade-bound-election.md` @ `eed4a45` · `docs/briefs/pre-registration/Q-TRADECAP-2-verdict-preregistration.md` @ `4d6761b` · `docs/notes/notice/N-2026-08-24-ox-alpha-per-trade-bound-election.md` @ `eed4a45` · `core/firm_rules.py` `Tradeify_Select_100K` @ `94041d9` · `ops/c1_rail/c1_rail_listener.py` L262–266 @ `027a729` · `core/dd_protection.py` `calculate_protection` @ `94041d9`

Gate: `Accepted` when Claude judgment review returns and the operator ratifies. FALSIFIED if any of G1/G2/G3 is already false on those frozen owners (then escalate; do not elect the CFD pair in place).

Boundary: Do not treat this Proposed record as a wire. Do not change `DD_TRIGGER` / `DD_SCALE` / `BASE_RISK`. Do not pass `sl=` or flatten. Do not treat **1-size** as discharging realized loss. Do not close `Q-TRADECAP-2` until this ADR is `Accepted`. Do not invent a fourth frozen ID.

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md --type adr
python scripts/check_adr_graph.py
# Expected: light → NOT CHECKED; graph exit 0
```
