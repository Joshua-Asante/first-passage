# Q-SIGID-1 — What is the measured live↔backtest signal-identity gap from mid-bar `alert()`/`strategy.entry`, and which architectures close it?

**Status:** `OPEN`
**Authored:** 2026-07-28
**Closed:** N/A
**Authors:** Cursor cloud agent (drafting) — operator lock pending
**Parent question:** N/A (graduated from RUNBOOK/desk §1c discharge; not a fork of Q-RAIL-1)
**Sub-questions opened:** none at authoring
**Loop:** Inquire-phase Pre-Q — closure gates on Fri 07-31 clean §2b result × offline phantom band; Pine edit remains a **separate operator GO**
**Artifact path:** `docs/briefs/Q-SIGID-1-intra-bar-signal-identity.md`

---

## §0 — Rule 0 reads (production-source verification)

Read before authoring (2026-07-28):

- `docs/notes/rail_build/RUNBOOK.md` — anchor: `ce768ee` (2026-07-28 §1c discharge: `parsed.close` 28051.50 vs confirmed C 28048.50).
- `docs/notes/rail_build/B7_STAGE1_DESK_CARD_2026-07-31.md` — anchor: `ce768ee` (§2b clean mid-bar protocol; fill-in block added this session).
- `docs/notes/2026-07-24-execution-quality-investigation.md` — anchor: `153b64e` (Pine timing **deferred** as locked-parameter axis, not EQ P1–P4).
- `scripts/pine_lint.py` (`check_entry_confirmed`, L216–264) — anchor: `9e62d2a` (check 7 FAIL text: unconfirmed entry on `calc_on_every_tick` can fire/unfire intra-bar).
- `core/strategies/nas/LOCK.md` — anchor: `48a7a48` (locked MNQ/NAS params: lookback 15, ATR 11/MA 85/exp 0.28, minBody 0.38, SL 1.20×ATR; Mon/Tue; session 13–17 UTC).
- `core/strategies/striker/LOCK.md` — same param block for DJ30/MYM (Tue/Fri; SL 1.20×ATR).
- `core/strategies/nas/striker_nas100_v1_mnq_FUTURES_LOCK.md` — alert-payload contract; venue editions gitignored (PORT pin), no local `.pine` bytes in this environment.
- `lab/analysis/c1/c1_signal_identity_2026-07-28/RESULTS.md` — cheap falsifier + 1m phantom proxy (**measured this session before this brief**, per falsifier-before-brief discipline). **2026-07-29:** FULL-panel census supersedes Phase 0 as §6 offline measurement source (ratios in RESULTS §FULL); **§6 threshold text and 0.5 cut unchanged**.
- `ops/instruments/MNQ.md` W3 — 1m cannot fill an intrabar *execution* layer; proxy here is signal-flip coarseness only.

Venue `.pine` files are gitignored and **absent** on this clone; mechanism lines cited from prior Rule-0 reads recorded in RUNBOOK/desk + LOCK transcriptions (entry `stop_dist = atrVal * stopAtr`; `longSignal` uses live `rawBreakout`/`bodyOK`; `calc_on_every_tick=true`; `barstate.isconfirmed` zero times).

---

## §1 — Context & motivation

On 2026-07-28 the first real MNQ strategy `alert()` reached the rail as B1 JSON. Operator chart C for that `bar_time` was **28,048.50**; ledger `parsed.close` was **28,051.50** (Δ 3.00). The fire was confounded by an alert-save, so Fri 07-31 owes a clean re-measure. What survives the confound: a confirmed-bar replay would have reported 28,048.50 and did not.

Offline cheap falsifier (same day, Databento `$0` 1m→15m): at confirmed C, `rawBreakout` still true, but **`longSignal` false** because **`body_ok` fails**; live vs confirmed entry stop Δ is **−0.10 pts (−$0.20/contract)**. Coarse 1m proxy: MNQ **15** / MYM **21** phantom bars (mid-true, close-false) against **22** / **30** confirmed-close signals (~0.7×). The threat is **signal identity**, not slippage — Strategy Tester evaluates at close; live `calc_on_every_tick=true` evaluates every tick; every modeled figure this book rests on is backtest-denominated.

Standing doctrine: parameter axis LOCKED (lifecycle ADR / CLAUDE.md); EQ investigation explicitly refuses Pine timing as an EQ lever. Remediation is a **separate locked-axis** decision.

---

## §2 — Prior art / lineage

- **RUNBOOK §1c / desk §2b (2026-07-28)** — live discharge + clean re-measure protocol.
- **EQ investigation note (2026-07-24)** — fills/exits spine; Pine timing deferred.
- **`pine_lint` check 7** — static FAIL on both venue editions (unconfirmed entry).
- **CFD indicator history** (`docs/audits/2026-05-28-striker-nas100-v1-indicator-strategy-diff.md`) — indicator-side historically used `barstate.isconfirmed`; venue strategy editions do not.
- **Q-RAIL-1** — alert-payload contract; alert-only diffs previously allowed without touching order/sizing/DD logic. Gating entry on `isconfirmed` is **not** that class.
- **ORB-MNQ** — `calc_on_every_tick=false` (contrast mechanism, not a Striker comparator).

---

## §3 — Question (Q-SIGID-1)

**Pre-Q gate test:** symptom-only rephrase — live alerts can bind to mid-bar states the Strategy Tester never sees; what is that identity gap, and what architectures close it?

**Q-SIGID-1:** Given mid-bar `alert()`/`strategy.entry` on the c1 venue editions, what is the measured live↔backtest signal-identity gap, and which architectures close it without pretending this is an execution-quality fill study?

---

## §4 — Falsifiable hypothesis (H-SIGID-1)

**H-SIGID-1:** If a clean Fri §2b fire shows `parsed.close ≠ confirmed C` (DIFFERENT), **or** (Fri EQUAL/VOID but offline phantom rate remains at or above 0.5× confirmed-signal count on either leg), then the live trade set is not the backtest trade set under current Pine timing — identity gap is real and a locked-axis architecture change is in scope for operator GO; otherwise (Fri EQUAL **and** offline phantoms below 0.5× on **both** legs) the 07-28 concerning branch was confounded/overstated and remediation is not warranted from these data.

**Falsifier:** Fri §2b = EQUAL **and** a new offline re-run revises **both** legs' phantom/confirmed-signal ratios below 0.5 — then reject H-SIGID-1.

**Reject H-SIGID-1 if:** Fri §2b = EQUAL **and** offline phantom/confirmed-signal ratio below 0.5 on **both** MNQ and MYM (already measured: MNQ 0.68, MYM 0.70 — so EQUAL alone cannot reject without a re-run that revises the offline band).

**Accept H-SIGID-1 if:** Fri §2b = DIFFERENT, **or** offline ratio at or above 0.5 on either leg stands after Fri (non-VOID) completes.

**Ambiguous-hold if:** Fri §2b = VOID (in-window TV UI), or Fri produces no entry in-window — re-test next MYM session; offline numbers stay on file.

---

## §5 — Forbidden moves

- **Silent PORT bump / land `barstate.isconfirmed` without operator GO** — locked parameter/timing axis; alert-only precedent does not cover this.
- **Treat as EQ P1–P4** — EQ note already deferred Pine timing; fills/exits stay on their own spine.
- **Change SL/TP/ATR/risk%/pyramid/session/BE/trail defaults** — out of scope; identity gap is timing, not retune.
- **Spend `trades`/`tbbo`/`mbp-*` to "finish" quantification before Fri §2b** — Avenue-A / EQ depth still declined; 1m proxy + live §2b are the declared instruments.
- **Alert-only confirm gate leaving `strategy.entry` tick-eval** — splits TV strategy fills from rail alerts (usually worse identity).
- **Block Fri item-5 / arming on this Q** — desk card already: bounded attended risk; this Q gates how much weight backtest-denominated expectations carry, not the single fill.

---

> ⚠ **READER INTERCEPT — Rule 11 (2026-08-06 / claim-alignment M32).**
>
> **(a) Darkened limb:** every §6 verdict row (RESOLVED / FALSIFIED / AMBIGUOUS-HOLD) is
> conditioned on a live Friday MYM observation; the 07-31 desk card is SPENT with its §2b
> table blank.
> **(b) Why the input cannot accrue today:** no deployed MYM leg / no alert path producing a
> Friday session under the standing rail disposition.
> **(c) Re-arm condition:** fork **F2** (rail / alert disposition) — **not** structurally dead.
> §2b compares ledger `parsed.close` against chart-confirmed C and merely *records*
> `dry_run=` — it needs **no fill, no order, no arming**.
> **(d) Surviving limbs:** the offline limb (MNQ 0.68 / MYM 0.70) stands on file.

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` (gap real) | Fri §2b = **DIFFERENT**, **or** offline phantom/confirmed ≥ **0.5** on either leg after a non-VOID Fri session | Operator GO packet for a named architecture (§7); no silent Pine edit |
| `FALSIFIED` (gap not warranting change) | Fri §2b = **EQUAL** **and** a **new** offline re-run revises **both** legs' phantom/confirmed ratios below **0.5** | Close; keep lint WARN; no Pine timing change |
| `AMBIGUOUS-HOLD` | Fri §2b = **VOID** or no MYM entry that day | Re-test next MYM session (Tue/Fri); offline RESULTS remain canonical until superseded |

Pre-registered: [`pre-registration/Q-SIGID-1-verdict-preregistration.md`](pre-registration/Q-SIGID-1-verdict-preregistration.md).

---

## §7 — Execution plan

- **Phase 0 (done):** Rule-0 reads + cheap falsifier + offline harness ([RESULTS](../../lab/analysis/c1/c1_signal_identity_2026-07-28/RESULTS.md)).
- **Phase 0b (done 2026-07-29):** native-micro FULL panel (2019-05-06→2026-07-30) — §6 offline limb now RESULTS §FULL; Phase 0 band retained as historical / P0REP strip.
- **Phase 1:** Fri 07-31 — fill desk §2b measurement log; no TV UI in-window.
- **Phase 2:** Apply §6 to Fri verdict × offline band; write closure artifact (§9).
- **Phase 3 (operator GO only, not this brief):** if RESOLVED, pick architecture:
  1. Gate `alert()` **and** `strategy.entry` on `barstate.isconfirmed`
  2. Set `calc_on_every_tick=false`
  3. Reject split (alert-only confirm / strategy still tick-eval) unless a separate brief defends it
  4. **Bar Magnifier** — TradingView Strategy Tester / broker-emulator *historical-fill* setting, not a live `alert()` gate (contrast 1–2). Vendor spec (fetched 2026-08-18): Premium/Ultimate can raise historical bar detail so the emulator uses lower-timeframe OHLC instead of chart-bar path assumptions (`use_bar_magnifier = true` on `strategy()`, or Properties / report “Bar detalization” → “High”) — [Pine v6 Strategies](https://www.tradingview.com/pine-script-docs/concepts/strategies/) (“high historical bar detail”); v5 still names the same switch **Bar Magnifier** ([v5 Strategies](https://www.tradingview.com/pine-script-docs/v5/concepts/strategies/)). This would move the **backtest** trade set toward intra-bar resolution; whether that closes the live↔tester identity gap is untested and **not chosen**.
     - **Not** the Pepperstone / TV-CSV **BT-OFF** export convention (`percent_of_equity` compounded, decompounded static) — verified: [`decompound_remc` inputs README](../../lab/analysis/regime/decompound_remc_2026-06-07/inputs/README.md); [`q_ddtrig_1` inputs README](../../lab/analysis/regime/q_ddtrig_1_2026-06-07/inputs/README.md) L9; [`TV-CSV feed policy`](../adr/2026-06-12-tv-csv-canonical-feed-policy.md) §1 (“BT-OFF doctrine”).
     - **Not** the Strategy Tester export step “`Backtest Mode` ON” — verified: [`guardian_parity` README](../../lab/analysis/legacy/guardian_parity_2026-06-23/README.md) L102. Operator-named `backtest_mode` (compounded-vs-static sizing) is cited on `docs/briefs/Q-DJ30-decomp_reconcile_table.md`, which is **absent** on this public clone (`git log --all -- '**/Q-DJ30-decomp*'` empty, 2026-08-18).
     - One prior repo mention: [`EXPORT_SPEC.md`](../../lab/archive/p2_replay_2026-07/EXPORT_SPEC.md) L32 — “Bar Magnifier **OFF** on both (BT-OFF canonical doctrine, 2026-05-17)”. That line is a **paired-TV-export-parity** checklist (same setting on both P2 charts of a leg). It is **not** a considered rejection of Bar Magnifier for Q-SIGID-1 signal-timing. The parenthetical “BT-OFF” on L32 is a name collision with the export-convention doctrine, not a finding that Bar Magnifier *is* BT-OFF. Repo-wide `Bar Magnifier` hits: that line only (`rg --no-ignore`, 2026-08-18).
  Then PORT re-pin + TV republish + alert recreate (three-surface lesson).

Candidate architectures are **named, not pre-chosen**. Adding #4 is prep against the Rule-11 intercept (this brief, reader intercept 2026-08-06 / §6): Phase 3 activates only after a live Friday MYM §2b observation; there is no deployed MYM leg and no alert path producing that Friday session under the standing disarmed-rail posture. Naming #4 does **not** advance this brief toward closure.

---

## §8 — Verdict pre-registration

File: `docs/briefs/pre-registration/Q-SIGID-1-verdict-preregistration.md`

Offline measurement was the **cheap falsifier that licenses this brief** (not Phase-1 of a post-pre-reg study). The pre-reg freezes the **Friday-dependent** §6 gate before that live observation.

Pre-registration commit hash: `78b16d2`
Pre-registration date: 2026-07-28

---

## §9 — Closure record format

- **RESOLVED:** `docs/briefs/closures/Q-SIGID-1-closure-resolved.md` + operator GO note for architecture choice (not a recommendation.md promote of a strategy).
- **FALSIFIED:** `docs/briefs/closures/Q-SIGID-1-closure-falsified.md`
- **AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-SIGID-1-closure-ambiguous.md` with next MYM session date

---

## §10 — Audit hooks

```bash
# §0 anchors
git log -1 --format='%h' -- docs/notes/rail_build/RUNBOOK.md          # expect ce768ee lineage or successor
git log -1 --format='%h' -- docs/notes/2026-07-24-execution-quality-investigation.md
git log -1 --format='%h' -- scripts/pine_lint.py

# Offline reproduce
python lab/analysis/c1/c1_signal_identity_2026-07-28/signal_identity.py
python3 -c "import json;r=json.load(open('lab/analysis/c1/c1_signal_identity_2026-07-28/results.json'));\
f=r['falsifier_2026_07_28']; assert f['databento_confirmed_c']==28048.5;\
assert f['long_signal_at_confirmed_c'] is False; assert f['components_at_c']['body_ok'] is False;\
print('falsifier OK', r['legs']['mnq']['phantom']['n_phantom'], r['legs']['mym']['phantom']['n_phantom'])"

# Desk §2b fill-in present
rg -n "2b fill-in" docs/notes/rail_build/B7_STAGE1_DESK_CARD_2026-07-31.md

# No Pine edit on the remediation branch
git diff origin/main -- '**/*.pine' core/strategies/PORT_MANIFEST.sha256
```

---

## Verification

```bash
python3 scripts/check_brief.py docs/briefs/Q-SIGID-1-intra-bar-signal-identity.md --type inquire
# Expected: mechanical checks PASS

git log -1 --format='%h %s' -- docs/notes/rail_build/RUNBOOK.md
git log -1 --format='%h %s' -- docs/notes/2026-07-24-execution-quality-investigation.md
rg -n "parsed.close|28051.50|28048.50" docs/notes/rail_build/RUNBOOK.md | head
rg -n "Pine-side timing|locked-parameter" docs/notes/2026-07-24-execution-quality-investigation.md
```
