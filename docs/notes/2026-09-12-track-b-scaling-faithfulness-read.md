# Track B — scaling-faithfulness read and the export menu (TB-R2, 2026-09-12)

**Status:** classification RESOLVED · export menu **DRAFT — NOT FROZEN** (freeze waits on umbrella
§0.8 rulings **O-5** (ladder-leg sizing law), **O-6** (add-quantity law) and **O-7** (ORB chart margin
for the new exports)) · authorizes nothing ($0 · K=0).
**Packet:** TB-R2 of the [Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)
(footprint: this file). **Owner of the rules:** [Tradeify portfolio acceptance record](2026-09-10-tradeify-protection-selection.md)
(D-B10, D-B14 (a)). **Coordinator record:** [dispatch 1](2026-09-12-tradeify-portfolio-coordinator-dispatch-1.md).
This note names strategy inputs by role and Pine line number only; it publishes no parameter value
beyond those already in `phase1_config.json`, `book_policy.py` and the acceptance record.

## Phase 0 — reads (anchors at `origin/main @ c41e2be`, 2026-09-12)

| Source | Located / anchor | What it fixes here |
|---|---|---|
| Four pinned Pine bodies | **Found by digest** in the operator's Downloads (not under `core/strategies/`): `db78ecba…` (Aegis 6J1 VB), `712cf395…` (Striker DJ30 v4.5 MYM p250 cap100k), `af26899c…` (Vanguard Gold MGC v0.4 VB), `176c4f70…` (ORB-MNQ-1 recon v7 VB); each equals its `phase1_config.json` `pine_sha256` | the read below |
| Effective chart inputs | `ops/c1_signal_daemon/ports/effective_inputs.json` (private, `66406dee…`, pinned in `book_adapters.py @ 8c9d002`) — **RECONSTRUCTED**; the D26 override files (`460f40fa…`, `b7369ee3…`, `3bacd6f1…`, `102635ac…`) remain **LOST** (umbrella §0.8 **O-9**) | which branch was live in the capture |
| Captured exports | Downloads, all four digest-equal to `export_sha256` (`71e732fc…`, `bff235ea…`, `5a500658…`, `7b9cc65c…`) | parity oracles at the captured size |
| Panels | `core/data/bar_data/{6J,MGC,MNQ,MYM}_M15.csv` verify against `SHA256SUMS` (CRLF-stripped) | replay inputs; window 2022-09-01 → 2026-09-03 00:00Z |
| `ops/c1_rail/book_policy.py @ bda7a48` | `BOOK_LEGS`, `scaled_quantity`, `quantity_table`, `reachable_quantity_menu` | the as-built quantity law (**law A** below) |
| `ops/c1_rail/c1_sizing_host_reference.py @ 509b524` lines 296–368 | `r_eff = base_risk × dd_scale × lifecycle`; `qty = floor(E_firm·r_eff / per_contract)`; `add = floor(executed_base × pyr%)` | the deployed law (**law B** below) |
| Governing plan Task 1 (`@ 3c439f7` lines 163–171) · campaign-state §7 prerequisite 1, §19d, §19e | "a coded default is not evidence that a branch was inactive"; one finite menu; no reweighting | the rule this read serves |
| [Adapters and book rules note](2026-09-11-track-b-adapters-and-book-rules.md) `@ 027895e` | parity PASS 681/203/338/121; findings carried | re-verified today: `tests/ops` book suites **85 passed** with the private inputs |

## §1 — Classification (per leg; Pine line refs are to the pinned body)

| Leg | Quantity rule | Dollar/equity stops and account-state feedback | Pyramids | Margin (TV) | Verdict |
|---|---|---|---|---|---|
| **Aegis 6J** (`aegis_6j`) | equity-based ladder capped by a contract-cap input (L539–551); the capture ran at cap 8 and hit it on 59/121 trades | rails (trailing-DD and daily-loss dollar inputs, L559–590) are **display-only** under the capture's backtest mode; exits are price-only (stop / TP / breakeven / stale / EOD) | none (`pine_pyramiding_pct` 0) | header sets long/short margin to 0 (L10–11): no affordability branch | Pine sizing branch is SIZE-DEPENDENT; **timing is SIZE-INVARIANT** — verified today: replaying the port at a fixed 8 reproduces all 121 captured entry/exit bars and prices (62 trades sized up), and fixed 3 is identical again (`test_aegis_protected_size_three_…`). Rail expression: **fixed quantity** (TB-S1 (F)) |
| **Striker MYM p250** (`dj30_mym_p250`) | ladder from a fixed account-size input, not from equity (L188–193; the public form is in `book_policy.py`) | **SIZE-DEPENDENT through feedback**: day soft-stop on the leg's realised closed-trade profit (L225–234) and the daily/total DD kill on the leg's own paper equity (L198–203, L368) — live in the capture because backtest mode was **OFF** (export carries `DD Limit` exits). Halts move when trade size moves | add = `floor(initialSize × pyramid%)` where `initialSize` is the **executed** base (L301, L340) — TV's add law is the host's law | header margin 0 (L21–22) | **SIZE-DEPENDENT** (feedback + ladder) |
| **Vanguard MGC v0.4** (`vanguard_mgc`) | leg-equity ladder capped by a contract-cap input (L419, L157); reaches 1 or 2 in the capture | DD kill display-only (backtest mode ON, L382). **Holiday artefact:** the EOD flat latch resets on `ta.change(time("D"))` (L299); a US market holiday has no daily bar, so the leg trades nothing on the session after a holiday (umbrella §0.8 **O-8**) | add = `max(1, round(base × 80%))` (L489), up to two | header margin 0 (L11–12) | **SIZE-DEPENDENT** (weakly, via the equity ladder); **MODE**: protected quantity floors to 0 (D-B10 accepted consequence) |
| **ORB MNQ v7** (`orb_mnq_v7`) | fixed contracts input (L67); the capture ran at 2, the fixed book at 1 | none (no account-state read) | adds at 100 % of the entry quantity, ≤2 (L112–114) | **header omits margin** (L27–38) → Pine v6 default 100 %: the capture's adds were **affordability-throttled** by TradingView (2 contracts per fill; adds nearly vanish after 2023-05). The rail has no such branch (**O-7**) | **SIZE-DEPENDENT in TV only** (margin branch); **MODE-DEPENDENT**: adds-off disables the stall exit (L291) and changes average-price-driven exits — verified (`test_orb_adds_off_mode_…`) |

Striker NAS100 (Wednesday-excluded) is out of scope (D-B4).

## §2 — Reachable quantities: what the rulings fix and what remains

Lifecycle tiers compound before the floor (D-B14 (a)); the reachable multiplier set is
`{1, 0.5, 0.25} × {1, 0.40}` if **O-1** is ruled "Call-4 handled off-rail" (recommended in the
coordinator record); it grows to include 0.125 and 0.05 otherwise.

Two laws can express "40 % of normal" and they are **not equal** for a ladder leg:

- **Law A — quantity-floor at the adapter's normal integer** (as built in `book_policy.scaled_quantity`;
  the wording of D-B10 and TB-S1 (C)): `qty = floor(normal_qty × 0.40 × lifecycle)`.
- **Law B — risk-scaled** (the deployed sizing host): the ladder is recomputed with
  `r_eff = base_risk × 0.40 × lifecycle`, i.e. `floor(0.40 × y)` instead of `floor(0.40 × floor(y))`.

They differ by one contract whenever `0.40·y` crosses an integer that `0.40·floor(y)` does not
(for the 40 % factor: `y ∈ [n+0.5, n+1)` with `n ∈ {2, 7, 12, 17, 22}` — roughly one entry in ten for
Striker's ladder), and at the cap (22 → 8 under A; unchanged 22 under B). Only **law B** can be
reproduced on a TradingView chart, because the pinned bodies carry no quantity-multiplier input:
Striker's Account Size input and Vanguard's risk input scale the *risk*, never the resulting integer.

| Leg | Normal | Protected | WATCH-1 | WATCH-1 + P | WATCH-2 | WATCH-2 + P | TV-expressible under A / B |
|---|---|---|---|---|---|---|---|
| Aegis (fixed 8) | 8 | 3 | 4 | 1 | 2 | 0 | A: n/a (timing size-invariant, no export needed) |
| Striker (ladder 1..22, add 250 %) | ladder | A: `floor(0.4·ladder)`, cap 8 · B: ladder at 0.4× risk, cap 22 | ×0.5 | ×0.2 | ×0.25 | ×0.1 | **A: no** (no input yields `floor(0.4·floor(y))`) · **B: yes** (scale the Account Size input; the risk input's minimum bound blocks the 0.1 cell, the account-size input does not) |
| Vanguard (ladder 1..2, add 80 %) | 1 or 2 | A: **0** (accepted) · B: 0 or 1 | A: 1 only when the ladder is 2 · B: ladder at 0.5× risk | 0 | 0 | 0 | A: **no** for WATCH-1 (a cap of 1 also yields 1 when the ladder is 1) · B: yes via the risk input, subject to its step |
| ORB (fixed 1, adds 1 each) | 1 + adds | 1, adds off | **0** (base floors to 0) | 0 | 0 | 0 | mode exports only (§3) |

**Consequences to record (not new decisions):** under either law ORB places nothing at WATCH-1/2
and Vanguard places nothing while protected; both are accepted consequences of D-B10/D-B14, and
TB-P1 (E) records them as the reachable-ladder restriction for those legs. **The decision that
gates the menu is O-5** (law A or B for Striker, and for Vanguard's WATCH-1 cell) and **O-6**
(add law: A's `floor(0.4 × normal add)` vs B's `floor(executed base × pyramid%)`, which is also
TradingView's own law at any size — Striker at 22 gives 22 vs 20).

## §3 — The single finite export menu (DRAFT, written for the recommended rulings)

Recommended rulings assumed: **O-5 = law B for Striker, law A (zero) for Vanguard with its WATCH
tiers restricted to zero**, **O-6 = law B**, **O-7 = ORB exports at 0 % chart margin**. If the
operator rules otherwise, this menu is **re-issued as a replacement** (plan Task 1: never extended
after results). Common chart state for every owed export — identical to the 2026-09-03 capture
except the one named change: same symbol (the continuous CME contract in the pinned filename),
15-minute bars, Deep Backtesting over the same span the capture used (campaign-state §47 (e)),
same commission/slippage properties, **List of trades** CSV export, plus **one Inputs-tab and one
Properties-tab screenshot per export** taken in the export's exact chart state (the D26 snapshot
procedure, campaign-state §47a) so the new override file is never lost again.

| Export id | Strategy / source identity | Quantity · mode (the one change vs capture) | Warm-up | Delivery (primary checkout, ignored roots) | Parity obligation discharged | Status |
|---|---|---|---|---|---|---|
| A-0 | Aegis 6J1 VB `db78ecba…` | captured ladder, cap 8 (`71e732fc…`) | none owed (panel origin = TV run origin) | already in Downloads | Aegis Pine-faithful port at the captured size (**PASS 121/121**); the fixed-8/3/4/2/1 rail rule is verified against A-0 by timing invariance (§1) | **AVAILABLE** — no further Aegis export |
| V-0 | Vanguard Gold MGC v0.4 VB `af26899c…` | captured (`7b9cc65c…`) | none owed | already in Downloads | Vanguard at the captured size (**PASS 338/338**); protected = no entries; WATCH tiers restricted to zero (no executable state to export) | **AVAILABLE** — no further Vanguard export |
| S-0 | Striker DJ30 v4.5 MYM p250 cap100k `712cf395…` | captured (`5a500658…`) | none owed | already in Downloads | Striker at the captured size (**PASS 203/203**) | **AVAILABLE** |
| S-P | same body | Account Size input × 0.40 (protected) — every other input as captured | none owed | `core/data/tv_exports/cme/` + screenshots under `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/` | Striker protected size **with** its halt feedback at that size (TB-A2 protected parity) | **OWED (operator)** |
| S-W1 | same | Account Size × 0.50 | none | as S-P | WATCH-1 unprotected | OWED |
| S-W1P | same | Account Size × 0.20 | none | as S-P | WATCH-1 protected | OWED |
| S-W2 | same | Account Size × 0.25 | none | as S-P | WATCH-2 unprotected | OWED |
| S-W2P | same | Account Size × 0.10 | none | as S-P | WATCH-2 protected | OWED |
| O-0 | ORB-MNQ-1 recon v7 VB `176c4f70…` | captured: 2 contracts, TV default margin (`bff235ea…`) | none | already in Downloads | the Pine-faithful port incl. the margin branch (**PASS 681/681**) — *not* an oracle for the rail's 1-micro book | **AVAILABLE** |
| O-N | same body | contracts input 1 · chart Properties margin long/short **0 %** (O-7) · scale-in enabled | none | as S-P | the fixed book's **normal** ORB mode (1 micro, adds fire whenever the price rule fires) | **OWED (operator)** |
| O-P | same body | contracts 1 · margin 0 % · **scale-in disabled** | none | as S-P | the fixed book's **protected** ORB mode (base one micro, no adds, no stall exit) | **OWED (operator)** |

Count: **7 owed exports** (5 Striker, 2 ORB); 4 available. If O-5 is ruled **law A for Striker**,
S-P … S-W2P are **withdrawn** (not expressible) and the Striker protected/WATCH evidence becomes the
port's Pine-faithful semantics plus a recorded bounded-divergence test against S-0 — that waiver
is then an explicit operator ruling recorded in TB-S1, never an inference. Every owed export enters
through the **TB-R3 intake gate** (source identity with the new override digest, normalization,
reconciliation) before it is decision-bearing; parity at a protected size or in adds-off mode may
not start on an un-intaken export (umbrella D-B10, TB-R3).

## §4 — TB-W1 warm-up requirements (public summary; private inventory on the primary checkout)

- **Replay / parity warm-up boundary = the panel origin** (2022-09-01 00:00Z; 6J 2022-09-01 23:00Z,
  its own first session). The TradingView deep-backtest runs started at the same origin
  (campaign-state §47 (e) run span), the ports start cold at the same bar, and parity is exact from
  the first captured trade on all four legs — so **no pre-window bars are owed** for TB-I2 or TB-E1.
  A scoring window starting after the origin inherits this state; a window that starts *before* the
  origin has no bars and fails closed.
- **Live cold-start / warm restart** (TB-S3 (H)): the per-leg maximum indicator and account-state
  lookbacks, the recommended emission-hold bar counts derived from them, and the sessions ORB needs
  for its opening-range volume history are recorded in the private inventory
  `ops/c1_signal_daemon/ports/TB-W1_warmup_inventory_2026-09-12.md` (ignored root; SHA-256 in the
  coordinator record). Checkpointed warm restart removes the lookback requirement; a leg restored by
  replay emits nothing until its hold count has elapsed. These counts are a **recommendation for
  TB-S3/TB-F1 to freeze**, not a ruling.

## §5 — Findings carried to their owners

- O-5 / O-6 / O-7 / O-8 / O-9 are recorded in the umbrella §0.8 with the coordinator's
  recommendation; the coordinator record states each one's consequence.
- Aegis's fixed-quantity expression needs a **fixed-quantity leg type** in the sizing host
  (`qty = floor(fixed × dd_scale × lifecycle)`); the current risk law cannot yield 8 → 3 without it
  (a risk large enough to pin 8 stays ≥ 8 under 0.4×). TB-S1 (F) / TB-I1 own that.
- Under law B the leg's own paper equity is not the account: the Striker halts and the Vanguard
  ladder read a per-leg synthetic equity in Pine and in the ports. TB-S3 must state whether the
  live adapters keep that synthetic equity (faithful to the capture; recommended) — the rail's
  account-level protection remains the book policy, not the leg's rails.

## Verification run for this note

```bash
FP_PORT_ROOT=<primary>/ops/c1_signal_daemon/ports FP_BAR_DATA_DIR=<primary>/core/data/bar_data \
FP_TV_EXPORT_DIR=<dir holding the four exports> python -m pytest tests/ops/test_book_policy.py \
  tests/ops/test_book_review_followups.py tests/ops/test_tv_broker_emulator.py \
  tests/ops/test_book_adapters_parity.py -q      # 2026-09-12: 85 passed
python scripts/check_md_relative_links.py --glob "docs/notes/2026-09-12-track-b-scaling-faithfulness-read.md" --strict
```
