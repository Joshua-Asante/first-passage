# Q-TRADECAP-2 — CLOSURE: `RESOLVED` (licensed close is frozen ID 2, observe-only)

**Verdict:** `RESOLVED`
**Closed:** 2026-08-24
**Lane:** `UNASSIGNED`
**Pre-registration:** [`Q-TRADECAP-2-verdict-preregistration.md`](../pre-registration/Q-TRADECAP-2-verdict-preregistration.md) — frozen at `4d6761b`
**Spend / K:** $0.00 · K consumed: 0
**Live effect:** none — election record only; no tripwire, cap, `dd_protection`, arming, or `sl=` wire
**Artifacts:** [`2026-08-24-q-tradecap-2-elect-alert-tripwire.md`](../../adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md) (`Accepted`) · [consult](../../notes/notice/N-2026-08-24-ox-alpha-per-trade-bound-election.md)

---

## 1. Verdict (§6 asserted against actual results)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | Operator elects exactly one of {**2**, **1-size**, **1-realized**} on an owning artifact (light ADR if no live-risk wire) | Operator ratified ID **2** on the light ADR 2026-08-24. No `dd_protection` / arming / `sl=` change | ✓ |
| `FALSIFIED` | Any of G1/G2/G3 is false on the frozen owners | G1/G2/G3 still hold (below) | — |
| `AMBIGUOUS-HOLD` | Operator declines all three named closes and also declines to delete STATE queue row 2 | Operator elected **2** | — |

## 2. What the pre-registration predicted vs what happened

H-GEO accepted at brief open: Option 1-as-staged is not startable. H-ELECT fired on ID **2**, the pre-reg recommended default. No fourth ID. Consult rows O4/O5/O6/O7/O9 disposed on the electing ADR (O4 declined as re-litigation of absence; O9 N/A because **1-size** is not elected; O5/O6/O7 named on the Decision line). Threshold was never in this Q's option set.

## 3. What this closure does NOT license

- Does not wire a tripwire, invent a threshold, or import the CFD-era example percent.
- Does not flatten, pass `sl=`, or change `DD_TRIGGER` / `DD_SCALE` / `BASE_RISK`.
- Does not treat **2** as discharging the realized-loss gap. Does not wire **1-size** or **1-realized**.
- Does not re-open Q-TRADECAP-1.

## 4. Defects found in the frozen brief (recorded, not repaired)

None. Frozen pre-reg left byte-unedited (`4d6761b` still says Phase 1 had not run as of that commit).

## 5. Lesson candidates

Below the two-incident bar — watch: an observe-only election can be read as closing the gap in prose. The ADR hangs the non-discharge label on **2** itself (O7).

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Model update:** the licensed Tradeify close is observe-only ID **2**. The startable set stays {**2**, **1-size**}; **1-realized** stays gated on disaster-stop Phase 0a. Parent “unbounded” remains no per-trade bound *inside* the trail.
- **Next:** INTEGRATE
- **Routing:** elect-2 `Accepted`; this Q closed; STATE queue row 2 deleted (no auto-replace). No rail / sizing / arming wire. Threshold + tripwire implementation named, not opened.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** n/a — integrated
- **Board write:** STATE.md OPERATOR QUEUE — row 2 deleted (no auto-replace). Decision index 2026-08-24. SESSIONS Open/next: `STATE queue: #1 B7-REFIRE Stage 1 + M1`. Owner: this closure + elect-2.
- **Registry:** n/a — governance election of a licensed close, not a strategy-grounds kill

## §10 audit-hook discharge

```
$ PYTHONPATH=core python -c "from firm_rules import FIRM_RULES; t=FIRM_RULES['Tradeify_Select_100K']; sb=t['starting_balance']; print(t['daily_loss_pct'], sb*t['max_dd_pct']/100, sb*0.02, (sb*0.02)/(sb*t['max_dd_pct']/100))"
None 3000.0 2000.0 0.6666666666666666

$ sed -n '262,266p' ops/c1_rail/c1_rail_listener.py
    payload_text = build_crosstrade_payload(
        leg=leg, action=action, symbol=symbol, qty=decision.qty_out,
        order_id=order_id, account=config["account"],
        secret_key=config["secret_key"], destination=config.get("destination"),
    )

$ rg -n "stop_loss=" ops/c1_rail/crosstrade_payload.py
83:        parts.append(f"stop_loss={sl}")

$ rg -n "CLOSED-RESOLVED 2026-08-23" docs/briefs/Q-TRADECAP-1-per-trade-loss-bound.md
3:**Status:** `CLOSED-RESOLVED 2026-08-23` — ...

$ rg -n "per.trade.dollar|TRADECAP_BOUND|max_loss_usd" ops/c1_rail core/dd_protection.py
(no matches)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Closure authored. Operator ratified elect-2 after Claude review. `RESOLVED` recorded. | Cursor Cloud Agent, operator GO |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-TRADECAP-2-closure-resolved.md
python scripts/check_brief.py docs/adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md --type adr
python scripts/check_adr_graph.py
```
