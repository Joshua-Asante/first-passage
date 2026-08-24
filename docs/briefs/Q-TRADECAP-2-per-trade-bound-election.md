# Q-TRADECAP-2 — Which close is licensed for the unbounded per-trade realized loss?

**Status:** `CLOSED-RESOLVED 2026-08-24` — licensed close is frozen ID **2** (observe-only). Closure: [`closures/Q-TRADECAP-2-closure-resolved.md`](closures/Q-TRADECAP-2-closure-resolved.md).
**Authored:** 2026-08-24
**Closed:** 2026-08-24
**Authors:** Joshua + Cursor
**Parent question:** [`Q-TRADECAP-1`](Q-TRADECAP-1-per-trade-loss-bound.md) (`RESOLVED` 2026-08-23) — absence confirmed; this brief is the opened successor
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on operator election among a frozen option set, after a $0 geometry re-scope of the CFD-era fork to `Tradeify_Select_100K`
**Artifact path:** `docs/briefs/Q-TRADECAP-2-per-trade-bound-election.md`

---

## §0 — Rule 0 reads (production-source verification, executed 2026-08-24)

- `core/dd_protection.py` `calculate_protection` L191–227 — anchor `94041d9` (2026-08-23). Output is `(equity, peak, lifecycle)` only. No per-trade dollar field. Reconfirms Q-TRADECAP-1 Limb-Sizing; not re-litigated.
- `core/firm_rules.py` `Tradeify_Select_100K` L337–349 — anchor `94041d9` (2026-08-23). `starting_balance=100_000`, `max_dd_pct=3.0` (trail **$3,000**), `daily_loss_pct=None`. Cheap geometry (this session): CFD example `0.02 × 100_000 = $2,000` = **0.6667** of the trail.
- `ops/c1_rail/c1_sizing_host_reference.py` L1–80, L58–80 `LEG_MAP` / cap-split — anchor `da084bc` (2026-08-23). Qty law: `floor(E_firm * r_eff / (SL_pts * $/pt))`. `stop_dist_pts` sizes qty; it is not a live stop.
- `ops/c1_rail/crosstrade_payload.py` — anchor `027a729` (2026-08-14). Builder accepts `sl=` and emits `stop_loss=` (`L83`).
- `ops/c1_rail/c1_rail_listener.py` `handle_signal` L262–266 — anchor `027a729` (2026-08-14). Call site passes `leg, action, symbol, qty, order_id, account, secret_key, destination` — **no `sl=`**.
- `docs/methodology/1r_estimation.md` L235–267 — anchor `670e776` (2026-08-14). CFD-era fork: hard-cap vs observe-with-tripwire; example 2.0%; gated on allocation review / 6-month live reconciliation (both retired with the CFD estate).
- `docs/briefs/closures/Q-TRADECAP-1-closure-resolved.md` — anchor `afa0d56` (2026-08-23). Absence confirmed; two options named, not elected; this brief is the named successor.
- `docs/adr/2026-07-28-c1-disaster-stop-payload-supported.md` — anchor `b2ead40` (2026-08-23). `Accepted`; Phase 0a `BLOCKED`. [`BLOCKED note`](../notes/rail_build/2026-08-23-disaster-stop-phase-0.md) same commit.
- `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` — anchor `027a729` (2026-08-14). Distinguishes `reserve_cap` (bounds **size**) from item 5 (bounds signal **identity**). No third axis (bounds realized **magnitude** once sized).

Amendment-first / sub-rule 8 (this session, literal):

```
$ rg -n 'Q-TRADECAP-2' lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
(no matches)

$ python scripts/check_advisor_dedup.py --keywords "per-trade dollar-loss bound TRADECAP"
  nearest: Q-TRADECAP-1 closure (parent; closed). No Q-TRADECAP-2.

$ PYTHONPATH=core python -c "from firm_rules import FIRM_RULES; t=FIRM_RULES['Tradeify_Select_100K']; ..."
starting_balance 100000  max_dd_pct 3.0  daily_loss_pct None
trail_usd 3000.0  cfd_2pct_usd 2000.0  cfd_frac_of_trail 0.6667
```

Nearest owners: this Q (new), the parent closure, `1r_estimation.md` (CFD-era fork — amend-in-place cannot hold a Tradeify election without mixing eras). New file required.

---

## §1 — Context and motivation

Q-TRADECAP-1 confirmed the gap. STATE queue row 2 held the election (now deleted). The CFD-era fork assumed a daily-cadence layer to sit on and used 2.0% of equity as the example threshold. Tradeify Select 100K has **no daily-loss rule** and a **$3,000** trailing DD; 2.0% of $100K is $2,000 — two-thirds of the whole trail. A realized-loss hard-cap also needs a flatten/stop path; disaster-stop Phase 0a is `BLOCKED` and the listener still does not pass `sl=`. Starting the bound is possible only for the closes that do not require those missing pieces.

---

## §2 — Prior art / lineage

- [`Q-TRADECAP-1`](Q-TRADECAP-1-per-trade-loss-bound.md) + [closure](closures/Q-TRADECAP-1-closure-resolved.md) — parent; absence only.
- [`1r_estimation.md`](../methodology/1r_estimation.md) L235–267 — pre-staged pair; CFD-era trigger retired.
- [`disaster-stop ADR`](../adr/2026-07-28-c1-disaster-stop-payload-supported.md) — the only accepted path that can cap *realized* loss; unpaid Phase 0a.
- M1 ADR — size-bound vs identity-bound; realized-magnitude is the unnamed third axis.
- Assumption-sweep A6 — origin of the parent.
- Ox-alpha consult (zero authority): [`N-2026-08-24-ox-alpha-per-trade-bound-election.md`](../notes/notice/N-2026-08-24-ox-alpha-per-trade-bound-election.md). Surviving rows travel with the election; they do not elect.
- Election record (`Accepted`): [`2026-08-24-q-tradecap-2-elect-alert-tripwire.md`](../adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md) — ID **2**.

---

## §3 — Question (Q-TRADECAP-2)

**Pre-Q gate test (symptom-only):** a single trade's realized dollar loss is unbounded on Tradeify_Select_100K's intraday-enforced trail; the CFD-era fork named two closes that assumed a daily-loss layer and a 2.0% example; it is unknown which close is licensed given there is no book, no daily-loss rule, and no broker-side stop.

**Q-TRADECAP-2:** On `Tradeify_Select_100K`, which of the frozen closes is licensed for the confirmed unbounded per-trade realized loss, and is the CFD-era Option 1 even startable on this venue?

---

## §4 — Falsifiable hypothesis (H-TRADECAP-2)

**H-GEO (Phase 0):** G1 ∧ G2 ∧ G3 hold on the frozen owners → Option 1-as-originally-staged (realized-loss hard-cap layered on a daily-cadence rule, example 2.0%) is **not startable**. The startable set is {**2** alert tripwire, **1-size** entry-size $ ceiling}. **1-realized** stays named and gated on Phase 0a `PASS`.

**H-ELECT (Phase 1):** exactly one of {**2**, **1-size**, **1-realized**} is the licensed close; the other two are not wired.

**Reject H-GEO if:** any of G1/G2/G3 is false (daily-loss layer exists, or 2.0% < 50% of trail, or `sl=` is live at the listener call site).
**Accept H-GEO if:** all three predicates hold as measured in §0.
**Reject / accept H-ELECT if:** operator election recorded vs declined (see §6).
**Ambiguous-hold if:** operator declines all three named closes and also declines to delete queue row 2.

---

## §5 — Forbidden moves

- **Importing 2.0% as the Tradeify threshold.** Tempting because the parent carried it. $2,000 is 66.7% of the $3,000 trail — not a conservative example. Threshold is a later election.
- **Wiring 1-realized before Phase 0a PASS.** Tempting because it is the close that actually caps realized loss. The flatten path is unpaid; a docs-only "hard-cap" is the A6 pattern again.
- **Treating 1-size as discharging the realized-loss gap.** Tempting because the sizing host already consumes `stop_dist_pts`. That bounds *intended* entry risk. Pyramid, slippage, and a dead exit path can still exceed it in-flight.
- **Treating `dd_protection` as the daily-loss layer.** Tempting because the CFD fork said "layered on the existing daily-cadence rule." `daily_loss_pct` is `None`; `calculate_protection` is next-trade-day sizing, not an intra-day stop.
- **Changing `DD_TRIGGER` / `DD_SCALE` / `BASE_RISK` to manufacture a bound.** Frozen; change-control is pre-reg → re-MC → both-halves → ADR.
- **Re-opening Q-TRADECAP-1** to hold this election. Parent is closed; this is the successor.
- **Electing in this brief without operator GO.** This packet names the reachable set; it does not pick.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Operator elects exactly one of {**2**, **1-size**, **1-realized**} and the election is recorded on an owning artifact (light ADR if no live-risk wire; full ADR before any `dd_protection` / arming / `sl=` change) | `INTEGRATE` — implement only the elected close |
| `FALSIFIED` | Any of G1/G2/G3 is false on the frozen owners | `ITERATE` — name (not open) a packet that elects the original CFD pair without the third option |
| `AMBIGUOUS-HOLD` | Operator declines all three named closes and also declines to delete STATE queue row 2 | `ITERATE` — re-test at the next arming GO or disaster-stop Phase 0a `PASS`, whichever is first |

---

## §7 — Execution plan (self-executing; $0 / K=0)

- **Phase 0 — Geometry (done this session, before lock).** G1/G2/G3 measured in §0. **H-GEO accepts:** Option 1-as-staged is not startable. Recommended default for the *operator* (not elected here): **2** (alert tripwire), threshold not imported from 2.0%. **1-realized** waits on disaster-stop Phase 0a. **1-size** is available if the operator wants a size bound knowing it does not close realized loss.
- **Phase 1 — Operator election.** `Accepted` on [`2026-08-24-q-tradecap-2-elect-alert-tripwire.md`](../adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md) (ID **2**). Observe-only; threshold later; not a wire.
- **Phase 2 — Verdict assertion** per §6: `RESOLVED`. See [`closures/Q-TRADECAP-2-closure-resolved.md`](closures/Q-TRADECAP-2-closure-resolved.md).

---

## §8 — Verdict pre-registration

[`Q-TRADECAP-2-verdict-preregistration.md`](pre-registration/Q-TRADECAP-2-verdict-preregistration.md)

Pre-registration commit hash: `4d6761b`
Pre-registration date: 2026-08-24

---

## §9 — Closure record format

Per `references/closure_record.md`. `RESOLVED` → `docs/briefs/closures/Q-TRADECAP-2-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md`.

---

## §10 — Audit hooks (runnable)

```bash
# G1 + G2
PYTHONPATH=core python -c "from firm_rules import FIRM_RULES; t=FIRM_RULES['Tradeify_Select_100K']; sb=t['starting_balance']; print(t['daily_loss_pct'], sb*t['max_dd_pct']/100, sb*0.02, (sb*0.02)/(sb*t['max_dd_pct']/100))"
# expect: None 3000.0 2000.0 0.6667

# G3 — listener call site still omits sl=
sed -n '262,266p' ops/c1_rail/c1_rail_listener.py
rg -n "stop_loss=" ops/c1_rail/crosstrade_payload.py

# Parent still closed; this Q closed on INDEX Recently-closed
rg -n "Q-TRADECAP-2" docs/briefs/INDEX.md
rg -n "CLOSED-RESOLVED 2026-08-23" docs/briefs/Q-TRADECAP-1-per-trade-loss-bound.md

# No live bound invented in the meantime
rg -n "per.trade.dollar|TRADECAP_BOUND|max_loss_usd" ops/c1_rail core/dd_protection.py
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-TRADECAP-2-per-trade-bound-election.md --type inquire
# Expected: RESULT: well-formed

git log -1 -- core/dd_protection.py core/firm_rules.py
PYTHONPATH=core python -c "from firm_rules import FIRM_RULES; t=FIRM_RULES['Tradeify_Select_100K']; print(t['daily_loss_pct'], t['starting_balance']*t['max_dd_pct']/100)"
sed -n '262,266p' ops/c1_rail/c1_rail_listener.py
```

---

## Pre-Lock Checklist

- [x] §0 paths read and anchored
- [x] §3 symptom-only
- [x] §4 binary (G1/G2/G3 + election)
- [x] §5 tempting, not strawmen
- [x] §6 specific triggers
- [x] §8 pre-registration authored before Phase 1 (frozen `4d6761b`; election now `Accepted`)
- [x] §10 hooks runnable
