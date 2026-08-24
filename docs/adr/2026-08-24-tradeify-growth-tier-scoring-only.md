# ADR 2026-08-24 — `Tradeify_Growth_100K` added to `firm_rules` + promoted to the operational target set

**Status:** `Accepted` — ratified by operator (JA) 2026-08-24, in-session instruction ("Add Growth
to the AUTOMATION_FRIENDLY_PROP_FIRMS. ratify the ADR."). Authored `Proposed`/scoring-only, then
edited in place pre-ratification once the operator promoted it same session — no ratified text
existed to preserve. Filename kept from the draft (stable anchor; cf. `Q-FIRMEOD-1-closure-falsified.md`,
content outgrew its filename with no rename).
**Decision date:** 2026-08-24
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** firm-model config + one modeling convention. **$0 · K=0.** No allocation, no
`dd_protection` constant, no Pine, no `LEG_MAP`, no lifecycle entry, nothing armed.

## §0 — Rule 0 reads (production, this session, 2026-08-24)

`core/firm_rules.py` `Tradeify_Select_100K` block (`65dc17b` 2026-08-23, schema + unreachable-lock
idiom copied) · `core/mc/simulation.py::simulate_path` (`027a729` 2026-08-14, L137-140
`daily_loss_pct`→hard fail; art. 10495897 clock quote read 2026-07-30) · `core/mc/preflight.py`
`firm_kwargs`/`assert_engine_ready` (`027a729`, None-threading + `dd_type` dispatch) ·
help.tradeify.co art. **10495915** (dated 2026-06-05, read in-browser 2026-08-24 — source of every
numeric below).

## Decision

`Tradeify_Growth_100K` joins `FIRM_RULES`: $6,000 target, **$3,500** fixed-$ EOD-ratcheting trail,
80 micro cap, `min_trading_days=1`, **no consistency rule**, $2,500 daily loss limit — then joins
`AUTOMATION_FRIENDLY_PROP_FIRMS["tradeify"]` alongside the four Select tiers (firm-level dict; same
pattern as Select's tiers under
[`2026-07-12-prop-portfolio-four-friendly-firms`](2026-07-12-prop-portfolio-four-friendly-firms.md),
no per-tier amendment). Only the $100K row is defined; 25K/50K/150K need their own rows first.

**`daily_loss_pct` stays `None`** — the DLL is a *soft* breach (art. 10495915: *"trading is stopped
for the day but your account is not failed"*); the engine's branch is a hard fail, so encoding it
would model a rule the venue lacks. Omitting it fattens the modeled daily left tail vs. reality.
**Every Growth bust figure is an upper bound w.r.t. the missing lockout, a lower bound w.r.t. the
intraday clock — two-sided, not a point estimate.** A faithful soft-DLL limb needs its own engine
change + ADR + re-MC.

Engine pre-flight 30/30 (incl. discriminator: Select busts at peak−$3,250 where Growth survives).
Measurement:
[`shape_feasibility_map_2026-08/RESULTS.md`](../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md)
§13 — wider rope drops the win-rate floor ~5pp for 2/3 shapes, 5/5 full-N validation cells agree.

**Owed:** re-read art. 10495897 *for Growth* — clock reading rests on the 2026-07-30 read.
Challenge-pass re-MC and rail build stay separately gated.

## Audit hooks

```bash
python -c "import sys; sys.path.insert(0,'core'); from firm_rules import FIRM_RULES as F, AUTOMATION_FRIENDLY_PROP_FIRMS as A; assert F['Tradeify_Growth_100K']['daily_loss_pct'] is None; assert F['Tradeify_Growth_100K']['max_dd_pct'] == 3.5; assert 'Tradeify_Growth_100K' in A['tradeify']; print('OK')"
grep -n "10495915" core/firm_rules.py
grep -n "§13" lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md | head -1
```
