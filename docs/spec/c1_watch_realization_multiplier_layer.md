# SPEC — c1 WATCH realization at the multiplier layer: single rail-side quantity computation for the venue-native futures legs

**Status:** `Accepted` — operator-ratified 2026-07-17 (chat: "ratify the spec and commit it"). Phase-3 bridge-capability check remains the implementability gate (§4); the §6 downstream pointer-sweep is deferred until the in-flight Cursor Q-RAIL-1 session lands (its files own those edit targets).
**Decision date:** 2026-07-17 (authored)
**Authors:** Joshua (direction) + Claude Code (authoring)
**Related:** [`Q-PYRPARITY-1` closure](../briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md) (the falsification that forces this) · [`Q-RAIL-1`](../briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md) (consumer: Phase 1 payload contract + Phase 3 bridge screen) · [`strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) §change-log CONFIRMED-FALLBACK row (the rule this spec mechanizes) · ADR [2026-07-10 lifecycle governance](../adr/2026-07-10-strategies-never-locked-lifecycle-governance.md)
**Layer:** execution / infrastructure

---

## §0 — Rule 0 reads (production-source verification, all 2026-07-17)

- [`ops/accounts.py:166-187`](../../ops/accounts.py) — anchor `8c461bc` (2026-07-11). `calc_multiplier = (balance × tier_risk) / (200,000 × BASELINE_RISK)`, **`math.floor(x*100)/100` — round down, never up**. This is the account-multiplier layer's existing arithmetic doctrine.
- [`core/dd_protection.py:189-224`](../../core/dd_protection.py) — anchor `a53ee99` (2026-07-13). `scaled_risk = BASE_RISK × multiplier(DD) × lifecycle[k]` (line 216); `DD_TRIGGER=0.015`, `DD_SCALE=0.40`; `lifecycle=None ⇒ all 1.0×`. The risk_pct layer composes multiplicatively — this spec preserves that composition, relocated to qty.
- [`core/lifecycle.py:34-55`](../../core/lifecycle.py) — anchor `4441c72` (2026-07-11). Ladder `AUTHORIZED 1.00 / WATCH-1 0.50 / WATCH-2 0.25 / RETIRED 0.00`; runtime tier interface = `core/lifecycle_state.json` (absent ⇒ all AUTHORIZED); autonomous moves are down-only.
- `core/strategies/striker/striker_dj30_v4.5_mym.pine` — **gitignored; read directly on local disk**; anchor = PORT_MANIFEST pin `fd91f37b…` (verified this session). Lines 248-252: `stopDist = atrVal * stopAtr; size = calcSize(stopDist); strategy.entry(qty=size)`. Line 300-301: `addSize = math.floor(initialSize × pyramidSize/100)`. **Lines 455-465: all `alert()` calls are plain-text strings — no qty, no price, no stop payload.** Header: `default_qty_type=strategy.percent_of_equity`.
- `core/strategies/nas/striker_nas100_v1.pine:80,98,281` — locked CFD source, on disk (MANIFEST `f5a567b5…`): `atrLength=11`, `stopAtr=1.20`, `stopDist = atrVal * stopAtr`. (MNQ venue edition MISSING on disk — PORT_MANIFEST pin `4bb37729…`; recovery route = operator's TV script library, exports dated 2026-07-17 prove it exists there.)
- [`lab/analysis/c1/q_rail_1_2026-07/f2_floors.json`](../../lab/analysis/c1/q_rail_1_2026-07/RESULTS.md) + `f2_floors.py` — re-run 2026-07-17 by this author, output **byte-identical**; MYM recent-90d: ideal base 11 → RESERVE-capped 9, add 67; MNQ recent-90d: base 1, add 10. These are the numbers any realization mechanism must reproduce. ⚠ 2026-08-05 — `f2_floors.json` was re-pinned 2026-07-22 to `(8, 60)` under the per-leg `cap_alloc` allocation; the `(9, 67)` pair above is the pre-split record retained under `pre_2026_07_22_whole_cap_per_leg` and is **not** what a realization mechanism must reproduce. See §2 and the Change history.
- [`Q-PYRPARITY-1` RESULTS §2](../../lab/archive/q_pyrparity_1_2026-07/RESULTS.md) — MYM1! @$200K TV qty ceiling: base clips at **17** (210/232 fills), add at **127**; below-ceiling ratios ≈0.50.
- [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) row scan — anchor `6b94032` (2026-07-13). Micro caps are firm/tier-specific (Bulenox 30–250 by tier; Q-RAIL-1 brief carries 80 for the discharge tier). **The cap is a parameter from `firm_rules.py`, not a constant of this spec.**

Contingency note: the MNQ venue edition could not be read (missing on disk). Its stop-path is cited from the locked CFD source (`striker_nas100_v1.pine`, Tier-1 direct read); the venue edition must be diffed against this expectation at F3 acceptance.

---

## §1 — Context

[`Q-PYRPARITY-1`](../briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md) (closed 2026-07-17, `FALSIFIED-NONPROPORTIONAL`) established that TV risk%-input scaling does **not** proportionally scale the pyramided stack on MYM (TV/symbol qty ceiling 17/127 @$200K); the ratified fallback is realization at the **account-multiplier layer**. Q-RAIL-1 F1 is `PASS-via-fallback` on that basis, and F2's floors were computed at that layer. But "account-multiplier layer" is currently a *layer name*, not a mechanism: nothing specifies **where in the TV-alert → bridge → firm chain the quantity is actually computed**, who reads the lifecycle/DD state, and how integer flooring + the firm micro-cap compose. Phase 3 (rail architecture selection) cannot score candidate chains without this contract, and Phase 1 (venue-edition re-parameterization) needs to know what the alert must carry.

**Decision driver:** Phase 3 is next on Q-RAIL-1's critical path after F3 unblocks; selecting a bridge without a sizing contract means selecting blind on the one capability Q-PYRPARITY-1 proved cannot be delegated to TV.

---

## §2 — Decision

**Decision:** For c1's venue-native futures legs (DJ30/MYM, NAS100/MNQ), every risk_pct-layer multiplier — account scaling, lifecycle authorization tier, and dd_protection's DD scale — is realized as **one combined, integer-floored quantity computation at a single rail-side scaling point downstream of TradingView**. The TV chart stays byte-locked at the panel-of-record configuration ($200K, locked inputs); the alert payload carries **signal identity + Pine's own stop distance**, never TV-computed quantity as the sizing source.

**Sizing law (normative):**

> ⚠ **NORMATIVE SAFETY PROPERTY — the cap is ACCOUNT-AGGREGATE, allocated PER LEG.** The reserve
> denominator is **`cap_alloc[leg]`** (this leg's share), **never `cap_firm`** (the whole account).
> Since 2026-07-22 the allocation is **MYM 69 / MNQ 11** against a firm cap of 80. Applying `cap_firm`
> to *each* leg is not a rounding difference — it is the defect the production host was changed to
> fix, and it computes **1.91× the account limit** (MYM 76 + MNQ 77 = **153 against 80**).
> **A missing `cap_alloc` must HALT, never fall back to `cap_firm`** — this mirrors production
> (`ops/c1_rail/c1_sizing_host_reference.py:290-296`, which halts on a missing key and on
> `cap_alloc > cap_firm`). Corrected 2026-08-05; see Change history.

```
r_eff     = BASE_RISK[leg] × DD_SCALE(dd_state) × M_lifecycle(tier)     # same composition as dd_protection.py:216
qty_base  = floor( E_firm × r_eff / (SL_pts × dollars_per_pt) )         # SL_pts from the alert payload (Pine's stopDist)
qty_base  = min( qty_base, floor( cap_alloc[leg] / (1 + pyr_pct/100) ) ) # RESERVE: the add must fit under THIS LEG'S cap share
qty_add   = floor( qty_base × pyr_pct/100 )                             # sized off EXECUTED base, preserving the locked ratio
```

`E_firm` = firm account size; `cap_firm` = the account-aggregate micro contract cap from `firm_rules.py` (**bound only, never a per-leg denominator**); **`cap_alloc[leg]`** = this leg's allocated share of `cap_firm`, from `LEG_MAP` in `ops/c1_rail/c1_sizing_host_reference.py` (**MYM 69 / MNQ 11** since 2026-07-22; `Σ cap_alloc ≤ cap_firm` is an invariant the host asserts); `pyr_pct` from locked Pine; `M_lifecycle` read from `core/lifecycle_state.json` (the same file `core/lifecycle.py` reads — no second source of truth); `dd_state` from rail-side equity tracking against the firm account's peak (implementation requirement, not resolved plumbing — flagged in §6).

**Alert payload contract (minimum fields, added to venue editions in Q-RAIL-1 Phase 1):** `{leg_id, signal_type (entry|add|exit|flat), bar_time, close, stop_dist_pts}`. Pine already computes `stop_dist` at signal time (`stopDist = atrVal * stopAtr`, both editions) — the payload emits it; it does not create it.

**Worked check (must reproduce F2):** MYM recent-90d, $100K W1: `r_eff = 0.0070 × 1.0 × 0.5 = 0.35%`; SL = 50.68 × 1.20 = 60.8 pts × $0.50 = $30.41/micro; `qty_base = floor(350/30.41) = 11` → RESERVE `floor(cap_alloc 69 / 8.5) = 8` → **8**; `qty_add = floor(8 × 7.5) = 60`. Matches `f2_floors.json` exactly (`legs[0].recent_90d = (8, 60)`).

> ⚠ **Superseded arithmetic, retained for provenance.** This worked check previously read
> `floor(80/8.5) = 9` → `qty_add = 67`, using the **whole firm cap per leg**. That pair is
> **pre-2026-07-22** and is retained in `f2_floors.json` under its own
> `pre_2026_07_22_whole_cap_per_leg` key — it is **not** the current expected output. The §10 hook
> was re-pinned to `(8, 60)` on 2026-08-02; this §2 text was not corrected in the same motion and
> asserted the superseded pair until 2026-08-05.

**Effective:** upon operator ratification; consumed by Q-RAIL-1 Phases 1 and 3.
**Scope:** c1's two pyramided futures legs on any discharge-tier firm. Flat (non-pyramided) legs and any future CFD-style venue are out of scope (risk-input scaling was only falsified for the pyramided/ceiling path).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **TV risk%-input scaling** (halve `riskPerTrade`) | FALSIFIED — Q-PYRPARITY-1: MYM medians 0.8707/0.9164 vs accept band 0.500 ± 0.005 (ceiling binds). |
| **Multiply TV's alert qty by M** (`floor(qty_tv × 0.25)`) | Doubly broken. (a) The ceiling contaminates the source: `floor(17 × 0.25) = 4` vs the correct 9–11 at $100K W1 — a silent ~2.5× under-size on MYM. (b) §0 read: the venue editions' alerts carry **no qty at all** (plain-text strings), so there is nothing to multiply without a Pine edit anyway. |
| **Set TV `initial_capital` to the effective size** (e.g. $50K ⇒ 0.25×) | Changes fills, pyramid triggers, and day-stop dollar gates → the venue edition no longer matches the panel of record, unanchoring F3's per-candle parity; and it still trusts the TV sizing runtime Q-PYRPARITY-1 just falsified (the ceiling would re-bind at a different level, unobserved). |
| **Rail recomputes ATR/stop from its own data feed** | Offline-port trap (standing lesson: offline ports need a real-source anchor; feed ≠ chart feed). A parallel stop implementation can silently diverge from Pine's; the stop must come from the signal source. |
| **Status quo — leave "account-multiplier layer" unspecified** | Phase 3 selects a bridge blind on the one capability TV cannot provide; the GO packet would carry an unverifiable F1. |

---

## §4 — Falsifier (implementability trigger)

**Falsifier:** If Q-RAIL-1 Phase 3 finds that **no candidate chain** (TV webhook → CrossTrade → NT8/Rithmic, or → Tradovate direct) can set per-order quantity from computed payload fields — i.e., every bridge only mirrors a TV-supplied qty or fixed presets with no computation hook — then the payload-computation route is unimplementable as specified.

**Falsified action (ordered):** (1) evaluate NT8-side sizing (an NT8 script computes the law from the payload's `stop_dist_pts` — same law, different host); (2) if no host on the chain can run the computation, score the affected rail tier **FAIL on F1-realization** in the H-RAIL-1 packet — do not degrade to alternative rows in §3 (each is ruled out on evidence, not preference).

**Trigger check:** Q-RAIL-1 Phase 3 bridge-capability screen (CrossTrade/firm primary docs) — each candidate chain's scorecard must cite the doc section proving or refuting payload-qty capability.

**Standing revert:** if a future TV observation shows the qty ceiling **absent** on the discharge symbols at the deployed capital (a fresh Q-PYRPARITY-class test, pre-registered), risk-input scaling may be re-proposed — via a new brief, not an edit here.

---

## §5 — Forbidden moves

- **Scaling the TV alert qty by M** — the cheap, obvious route; ruled out in §3 (ceiling contamination + no payload exists). Genuinely tempting because it needs no Pine change if a qty placeholder were added.
- **Touching the locked CFD originals to add payloads** — payload fields land **only on the venue editions** during Phase-1 re-parameterization (they are pre-FUTURES_LOCK and already being re-parameterized); `striker_dj30_v4.5.pine` / `striker_nas100_v1.pine` stay byte-identical to their manifest pins.
- **Hardcoding 0.50 (or 0.25 combined) into the rail** — the multiplier must be *read* from `lifecycle_state.json` + DD state at order time. Hardcoding freezes a revocable authorization into infrastructure — exactly the axis confusion ADR 2026-07-10 separates. (Tempting: it's one constant today.)
- **Applying the lifecycle haircut in `ops/cli.py lots` as well** — double-count. Standing doctrine (lifecycle ADR): one layer owns the haircut; the read-only surface only displays it.
- **Amending the §4 falsifier when Phase 3 finds a partial capability** — a bridge that "almost" supports payload qty gets the NT8-side evaluation, not a loosened trigger (Trap #12).

---

## §6 — Consequences

**Positive:**
- Phase 3 gains a mechanical screen: any candidate chain is scoreable against one required capability + one sizing law.
- WATCH/DD/account scaling collapse to a single audited computation — no distributed multiplier fragments to double-apply.
- The worked check ties the rail's arithmetic to `f2_floors.json`, so F2's PASS and the rail's behavior can never silently diverge.

**Negative (real):**
- The venue editions need alert-payload work in Phase 1 (new delta on the re-parameterization list; re-pin + FUTURES_LOCK acceptance still required).
- Rail-side equity/peak tracking for `dd_state` is new infrastructure with its own failure modes (stale equity ⇒ wrong DD tier).

**Risks:**
- Bridge JSON limits (payload size/field constraints) could force a reduced contract — mitigated by the contract being 5 fields.
- `lifecycle_state.json` unreadable at order time ⇒ **fail-safe rule: absent/unreadable state ⇒ treat as most-conservative known tier, never as 1.0×** (mirrors `lifecycle.py`'s absent⇒AUTHORIZED default *inverted* for live orders — a live rail must not fail-open to full size; this deliberately diverges from the read-only default and must be pinned in the rail's tests).

**Downstream artifacts (deferred until the Cursor Q-RAIL session lands — its files are in flight):**
- Q-RAIL-1 brief: Phase 1 delta list gains "alert payload contract"; Phase 3 gains the bridge-capability screen (cite this spec).
- `strategy_lifecycle.md` CONFIRMED-FALLBACK row: add pointer to this spec as the mechanization.
- STATE.md forward board: none needed (no new dated obligation; Phase 3 carries the check).

---

## §7 — Implementation plan

- **Phase 0** — operator ratifies this spec (or amends §2's payload fields).
- **Phase 1** (rides Q-RAIL-1 Phase 1, Cursor) — venue editions gain the payload fields during re-parameterization; re-pin hashes; FUTURES_LOCK acceptance.
- **Phase 2** (rides Q-RAIL-1 Phase 3) — bridge-capability screen per §4; chain scorecards cite doc sections.
- **Phase 3** — rail build (separately gated: no build/spend authorized by this spec) implements the sizing law + fail-safe rule + per-order audit log `{payload_in, r_eff components, qty_out}`.

---

## §10 — Audit hooks (runnable)

```bash
# The sizing-law composition matches production (dd_protection.py risk_pct layer)
grep -n "scaled_risk = {k: v \* multiplier \* lifecycle" core/dd_protection.py   # expect 1 hit (line ~216)
# Lifecycle state file is still the single tier source
grep -n "lifecycle_state.json" core/lifecycle.py docs/methodology/strategy_lifecycle.md
# Venue-edition alerts still payload-free (pre-Phase-1); after Phase 1 this hook EXPECTS payload fields — flip the assertion then
grep -n "alert(" core/strategies/striker/striker_dj30_v4.5_mym.pine | grep -c "stop_dist" # expect 0 now, >0 post-Phase-1
# Worked-check numbers still match F2's committed output
# RE-PINNED 2026-08-02: this hook asserted the PRE-2026-07-22 whole-cap values (9,67) and had been
# FAILING since the account-aggregate cap split (cap_alloc MYM 69 => reserve_cap floor(69/8.5)=8).
# The pre-split pair is still available under f2's own pre_2026_07_22_whole_cap_per_leg key.
python -c "import json; d=json.load(open('lab/analysis/c1/q_rail_1_2026-07/f2_floors.json')); r=d['legs'][0]['recent_90d']; assert (r['base_capped'], r['add_qty'])==(8,60), r; assert r['pre_2026_07_22_whole_cap_per_leg']['base_capped']==9; print('MYM 8/60 OK (pre-split 9/67 retained)')"
# Locked CFD originals untouched
python scripts/check_pine_manifest.py
```

---

## Verification

```bash
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/spec/c1_watch_realization_multiplier_layer.md --type adr
git log -1 --format="%h %ci" -- ops/accounts.py core/dd_protection.py core/lifecycle.py   # §0 anchors
grep -c "fd91f37b" core/strategies/PORT_MANIFEST.sha256                                    # MYM pine pin cited in §0
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-17 | Initial authoring (parallel lane B alongside Cursor Q-RAIL-1 Phase 0/F-scoring) | Joshua + Claude Code |
| 2026-07-17 | **Operator ratified** (`Proposed` → `Accepted`, same day). §6 downstream sweep deferred until the Cursor Q-RAIL-1 landing; §7 Phase 0 discharged. | Joshua (ratify) + Claude Code (record) |
| 2026-08-05 | **SAFETY CORRECTION — §2 reserve denominator `cap_firm` → `cap_alloc[leg]`**, plus the normative HALT property, the constants gloss, and the worked check (`9/67` → `8/60`, pre-split pair retained for provenance). Found by the [post-de-scope claim-alignment audit](../notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md) **B3**. The 2026-07-22 account-aggregate cap split changed production (`c1_sizing_host_reference.py`) and the §10 hook (re-pinned 2026-08-02) but never this normative §2 law, which `c1_nt8_sizing_host_impl.md` declares it implements *"verbatim (not re-derived)"* — so an implementer following the declared chain would have applied the whole account cap to each leg (**153 micros against 80, 1.91×**). **Production was already correct and is untouched; no encoded value changed; the 69/11 split is unchanged.** | Joshua (direction) + Claude Code (edit) |
