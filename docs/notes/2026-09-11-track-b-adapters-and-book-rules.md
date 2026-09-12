# Track B — fixed-book adapters, protection/capacity rules, parity (2026-09-11)

**Status:** implementation + verification record for the operator instruction "complete Track B's
strategy work: implement the four adapters and the exact protection/capacity rules; verify their
behaviour against the strategy sources, including protected sizes and ORB adds-off exits".
Owner of the rules: [protection selection](2026-09-10-tradeify-protection-selection.md) and the
[Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)
(TB-S1 (A)-(F), TB-S3 (C)/(D)/(M), D-B7/D-B8/D-B10/D-B11/D-B14). Nothing here deploys, arms, admits a
`POLICY_REGISTRY` row, edits `core/dd_protection.py`, or selects a market-data feed.

## Footprint

Tracked (public):

| File | Role |
|---|---|
| `ops/c1_rail/book_policy.py` | Candidate 1 % / 40 % policy value (threaded, unadmitted); trigger formula with ULP rounding; prior-close mode clock with a frozen initial state; D-B10 floor in exact rationals; the explicit per-leg / per-tier / per-mode integer table; carried-position rule; micro-equivalent capacity ledger with the atomic fail-closed Aegis takeover |
| `ops/c1_signal_daemon/book_protocol.py` | Adapter contract: sided integer orders, per-fill exit brackets, execution feedback (fills / cancels / rejects), protection mode |
| `ops/c1_signal_daemon/tv_broker_emulator.py` | Offline fill model with TradingView semantics (below); FIFO lot accounting; margin affordability; the replay device for parity and checkpoint restore |
| `ops/c1_signal_daemon/pine_ta.py` | Pine-equivalent indicators, clocks, the CME early-close list, the TradingView daily-bar key |
| `ops/c1_signal_daemon/book_adapters.py` | Public registry of the four adapters (leg ids, pinned Pine digests, instrument constants) + private-port loader |
| `ops/c1_signal_daemon/book_parity.py` | Parity harness + CLI (`python -m c1_signal_daemon.book_parity`) |
| `ops/c1_signal_daemon/ports/README.md`, `.gitignore` | The private port root (inside `ops/`: the ports import daemon modules); everything but these two files is ignored |
| `tests/ops/test_book_policy.py` | Every rule above as a failing-first test |
| `tests/ops/test_tv_broker_emulator.py` | The fill semantics on synthetic bars |
| `tests/ops/test_book_adapters_parity.py` | Parity + protected-size + adds-off behaviour (skip without private inputs) |
| `tests/ops/test_book_review_followups.py` | PR #356 review follow-ups: fixed-instance policy validation, post-refusal ledger reconciliation, partial explicit exits, exit side validation, gap trail activation, marketable next-open stops, OCA cancel events, digest pin, P&L in the verdict |

Private (primary checkout `ops/c1_signal_daemon/ports/`, gitignored; digests reported for TB-A0):

| Port | `leg_id` | SHA-256 |
|---|---|---|
| `aegis_6j.py` | `aegis_6j` | `11763740bc3fdcc8b9e94cb0b465823aec202cd8333379c46878185db5e9e84f` |
| `dj30_mym_p250.py` | `dj30_mym_p250` | `c81aa59c811dd2f318bf2f6b51e9df32fca20315ffab0885ec1d4ec6a2ab5379` |
| `vanguard_mgc.py` | `vanguard_mgc` | `e6a03d04c65a19e7fde71103560a229630c3663f445676f06622feec4e9157a3` |
| `orb_mnq_v7.py` | `orb_mnq_v7` | `b1f4e573009e62b976013e08e7ef2784497d840f490f04e3878fdaef553f317d` |
| `effective_inputs.json` | reconstructed capture inputs | `66406dee955fa69f237fde60eacdd24259a08d5320352d98e59889acaa18158d` |

Private evidence base restored on the primary checkout: the four refreshed CME panels
(`core/data/bar_data/{6J,MGC,MNQ,MYM}_M15.csv`) were regenerated from the 2026-09-03 BAR EXPORT
captures in Downloads and match `core/data/bar_data/SHA256SUMS` exactly (the on-disk panels were the
stale pre-refresh captures; those bytes are kept outside the tree under
`~/first-passage-private-backups/bar_data_pre_refresh_2026-09-11/`). The four captured exports are
located in Downloads by filename and verified against `phase1_config.json` digests
(`FP_TV_EXPORT_DIR`); the D26 override files remain LOST.

## Verification — parity against the captured exports

Each port is replayed through the emulator on its frozen panel and matched to the pinned export on
(entry bar, exit bar, quantity, entry price, exit price, net P&L incl. commission); the window is the
panel's span. The private `effective_inputs.json` is digest-pinned in `book_adapters.py`; the loader
refuses other bytes.

| Leg | Export trades | Matched | Missing | Extra | Qty mismatch | Price mismatch | P&L mismatch | Verdict |
|---|---|---|---|---|---|---|---|---|
| `orb_mnq_v7` | 681 | 681 | 0 | 0 | 0 | 0 | 0 | PASS |
| `dj30_mym_p250` | 203 | 203 | 0 | 0 | 0 | 0 | 0 | PASS |
| `vanguard_mgc` | 338 | 338 | 0 | 0 | 0 | 0 | 0 | PASS |
| `aegis_6j` | 121 | 121 | 0 | 0 | 0 | 0 | 0 | PASS |

Regression: `tests/ops` + `tests/core` green (841 passed, 4 skipped) with the new modules in place.

### TradingView fill semantics pinned by the exports (implemented in the emulator)

1. Intrabar path O→H→L→C when the open is closer to the high, else O→L→H→C; a level crossed in the
   gap fills at the open; stops fill on an exact touch (16 such fills across the three long legs).
2. `process_orders_on_close=true`: market orders fill at the generating close; a buy-stop already at
   or below the close, and an exit stop already through the close when issued, fill at that close.
3. Slippage applies to market and stop fills, never to limit fills; a long's protective stop level
   is floored to the tick, a long's limit ceiled (mirrored for shorts).
4. One exit order per entry fill; exits close lots **FIFO** (`close_entries_rule` default) — an add's
   trailing exit is reported against the older base lot; sibling exit orders persist with their own
   trailing state after one fills and a consumed order is not re-created while the position lasts.
5. Trailing stop: activation at fill price + `trail_points` ticks; then the extreme minus
   `trail_offset` ticks; it can fill on the activation bar.
6. A next-open close is sized at the position that existed when it was issued (an add issued on the
   same bar survives to the next bar's close order).
7. Pine v6 `strategy()` defaults `margin_long/short` to 100: a body that omits them (ORB v7) cannot
   fill an entry whose value exceeds the equity not already committed (both marked at the decision
   price) — the emulator rejects it. Marketable stops activate at once (this close, or the next open).
8. `time("D")` has no daily bar on a US market holiday: the holiday session belongs to the next
   trading day's bar, so `ta.change(time("D"))` is 0 at that evening's reopen (`tv_daily_key`).

## Findings the campaign must carry

- **ORB adds in the captured ledger are TradingView-margin-throttled.** With the v6 default margin
  the capture (2 contracts per fill) placed adds through 2023-05 and then almost none (0 in most
  later months) because a second lot no longer fit the paper equity. The port reproduces this
  exactly, but it means the "normal recorded adds" of the selection note are mostly *absent* adds,
  and the export is not a faithful 1-micro proxy for the add branch (TB-R2 scaling-faithfulness:
  ORB is size-dependent through the margin/affordability branch, not only mode-dependent). At one
  micro with no TradingView margin the adds fire whenever the price rule fires.
- **Aegis capture ≠ pinned defaults.** The export reproduces exactly only under a reconstructed
  effective-input set that differs from the pinned body's defaults in the risk fraction, the contract
  cap, the breakeven trigger and the stop multiple, and in the commission/slippage properties. Those
  inputs are the lost D26 override; they are recorded privately (`effective_inputs.json`) and are
  **not** the locked v4.3 values the body labels as locked. Any qualification statement about
  "Aegis 8×6J" refers to this effective set.
- **Striker capture ran with backtest mode OFF**: the export carries `DD Limit` exits, so the leg's
  1.15 % daily / 4.85 % total kill on its own paper equity and the -1.15 % day soft-stop were live
  in the capture. Both are account-state feedback; at 40 % size the leg's realised P&L halves, so
  the halts move (the protected-mode test records the divergence rather than asserting equality).
- **Vanguard trades nothing on the session after a US holiday** (flat latch never reset because the
  daily bar did not roll) — a TradingView artefact the adapter reproduces; the live daemon must
  decide whether to keep it (it is behaviour of the captured ledger, not of the strategy's intent).
- **Rail law vs captured sizing.** Aegis was captured on an equity-based ladder (59 of 121 trades at
  the 8-contract cap); the rail expresses the leg as a fixed 8 (TB-S1 (F)), so under the fixed law
  the normal-mode book sizes 62 trades larger than the capture. ORB was captured at 2 contracts per
  fill; the fixed book uses 1. Striker's base ladder is stop-distance-driven (1..22, adds 250 %).
- **Add-tier composition.** TB-S1 (C) floors every add tier from its *own* normal value
  (Striker 22/55 → 8/22); the deployed sizing host's add law `floor(executed_base × pyr%)` would
  give 8/20. `book_policy` implements the TB-S1 reading; the host's law is not changed here — the
  consolidated wave-2 read must pick one.

## Protected sizes and ORB adds-off — verified behaviour

- Aegis at the protected size: every entry 3 contracts; entry/exit bars and prices identical to the
  fixed-8 run (price-only exits) — `test_aegis_protected_size_three_with_identical_signals_under_the_fixed_law`.
- Striker at 40 %: base = floor(0.4 × ladder value), add = floor(0.4 × normal add) on every matched
  entry; caps 8 / 22; divergent entries caused by the leg's own P&L feedback are counted.
- Vanguard at 40 %: no entry at all (base 2 → 0, 1 → 0; D-B10 accepted consequence); WATCH-1 places 1.
- ORB adds-off: identical to the Pine with scale-in disabled (no add, **no stall exit** — the stall
  rule is gated on scale-in), base entries unchanged versus the adds-on run, exits differ (recorded).
- Lifecycle tiers compound before the floor (D-B14 (a)); the ORB base itself floors to 0 at WATCH-1.
- No OP-1 export exists yet, so the protected-size and adds-off results are verified against the
  ports' Pine-faithful semantics (which reproduce the captured runs exactly), not against
  TradingView exports at those sizes; TB-R3/OP-1 remains the export-side check.

## Not done here (owned elsewhere)

Daemon registry / bar-time barrier / listener side check / kill switch / EOD scheduler (TB-I3);
lifecycle keys in `core/lifecycle.py` and `LEG_MAP` rows (TB-I1/TB-V1); `POLICY_REGISTRY` row (TB-D0
after TB-E1); Call-4 beta term (O-1); OP-1 exports and their intake (TB-R3); market-data source (O-4).

## How to run

```bash
FP_PORT_ROOT=<primary>/ops/c1_signal_daemon/ports FP_BAR_DATA_DIR=<primary>/core/data/bar_data \
FP_TV_EXPORT_DIR=<dir holding the four exports> python -m pytest tests/ops/test_book_adapters_parity.py -q
```

```bash
python -m c1_signal_daemon.book_parity
```

## Review loop closure (2026-09-12)

Codex returned 11, 3 and 7 distinct findings over three rounds on PR #356. Rounds 1-2 and the real
items of round 3 (the takeover cancel/fill race, non-finite parity values, close-quantity
validation, action ownership, siblings cancelled only on a confirmed fill, the exact protected-fill
assertion) are fixed with failing-first tests in `tests/ops/test_book_review_followups.py`. Half of
round 3 was on code the earlier fixes added; the loop was therefore stopped with a scope statement
rather than a fourth fold: the emulator is the offline replay broker for the four ported bodies,
judged by exact parity plus tests, and refuses order shapes no adapter emits (`NotImplementedError`
at submit). Later reviewer findings land here as open items, not as further folds.

| # | Open item | Owner |
|---|---|---|
| R-1 | Marketable next-open stop inside an OCA group is refused, not modelled | TB-I2 if a future adapter needs it |
| R-2 | `check_state_currency` fails once STATE's weekly deadline (2026-09-11) is past; worker commits bypassed the hook with the reason in each commit body | orchestrator (STATE row) |

