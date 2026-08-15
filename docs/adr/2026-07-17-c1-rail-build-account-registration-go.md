# ADR 2026-07-17 — GO: c1 execution-rail build + Tradeify Select 100K account registration

**Status:** Accepted (operator executive decision, recorded)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - `ACTIVE_FIRM` retention prohibition only. The c1 rail build, Tradeify registration, attended-only posture, spend ceiling, and B7 arm-gate stand.
**Superseded-in-part-by:** `2026-07-22-c1-venue-native-monitoring-maturity.md` - next `dry_run=false` entry/add send / B7-REFIRE Stage 2 gains the M1 operational-monitoring gate. Rail build, account registration, attended posture, and spend ceiling stand.
**Superseded-in-part-by:** `2026-08-04-tradeify-venue-descope-eval-included.md` - **DEPLOYMENT LIMB ONLY.** Tradeify is no longer a deployment target for the locked Striker book, **evaluation included**, and both legs are withdrawn from the c1 eval deployment. §2's authorization to *deploy* is spent. The rail build, the account registration, the attended-only posture, the $700 spend ceiling, and the arm gate all **stand** — the rail is retained and **disarmed** pending fork F2. See the dated Addendum 2026-08-04 below.
**Retain-until:** none
**Clarification 2026-08-08 (two dated corrections, no clause withdrawn):**
(1) **§5 forbidden move 1 — "nothing arms before B6" — is DISCHARGED FOR THIS BUILD**, not *spent*: B6 PASSED
2026-07-20 (RUNBOOK §B6, operator-signed). The **principle re-arms** for any rebuilt or re-hosted signal path,
including the S2b Python-native daemon ([`S2 ADR`](2026-08-07-loop-s2-signal-host-fork.md)) — a fresh path needs a
fresh dry-fire, and this bar must not be read as already satisfied for it. **Sharpened 2026-08-08 (same day):** the
daemon has since been **built and deployed warm** (Fly app `c1-signal-daemon`, `emit_enabled=false`) under
[`build ADR`](2026-08-08-s2b-signal-daemon-build.md) + a recorded operator build GO. The guard that exists is an
**authorization** one — `ops/c1_signal_daemon/daemon.py` refuses `emit_enabled=true` without a separate strategy
emit GO — **not a proving run**: [SPEC S2b](../spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) still carries
no dry-fire / B6-equivalent limb (verified by grep, 2026-08-08). So the B6-shaped question is open, not closed,
and it is now live rather than hypothetical.
(2) **The M1 gate trigger moved send → ARM** (Addendum 2026-07-31b to
[`2026-07-22-c1-venue-native-monitoring-maturity.md`](2026-07-22-c1-venue-native-monitoring-maturity.md)): the
Superseded-in-part-by line above still says *"next `dry_run=false` entry/add **send**"*. The operative rule is that
`dry_run=false` may not be **SET** while M1 is not `RESOLVED` — enforced in `ops/c1_rail/c1_rail_arm.py`. M1 is
`CODE_LANDED`, **not** `RESOLVED`, as of 2026-08-08.
**Decision date:** 2026-07-17
**Authors:** Joshua (decision) + Claude Code (recorder)
**Supersedes:** none — this ADR **discharges** the rail-build/account/live-spend gate held open by [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) ("rail build, account registration, and any live spend gated" on operator GO) and satisfies [`2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) §5 (no research ADR is rail authorization — a fresh operator decision + ADR is; this is that ADR). Manual-trading retirement ([`2026-06-30-no-manual-trading-cfd-retirement.md`](2026-06-30-no-manual-trading-cfd-retirement.md)) stands untouched — attended automation is not manual execution.
**Related:** [`Q-RAIL-1 closure RESOLVED`](../briefs/closures/Q-RAIL-1-closure-resolved.md) (the decision packet this GO consumes); GO packet [`PHASE4.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE4.md); rail architecture [`PHASE3.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE3.md); sizing contract [`docs/spec/c1_watch_realization_multiplier_layer.md`](../spec/c1_watch_realization_multiplier_layer.md) (`Accepted` 2026-07-17); NT8 sizing-host implementation spec [`docs/spec/c1_nt8_sizing_host_impl.md`](../spec/c1_nt8_sizing_host_impl.md) (`Proposed`, B2, 2026-07-17); [`Q-PYRPARITY-1 closure`](../briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md) (F1 fallback); c1 ratification [`G8_INTAKE.md`](../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md).
**Layer:** execution — **not** locked-parameter. No change to locked Pine, allocations, `dd_protection` constants, or the FXIFY MC anchor pins (~~`ACTIVE_FIRM` stays FXIFY~~ — **superseded, see header**: `ACTIVE_FIRM = "Tradeify_Select_100K"` live since substrate Phase 1, 2026-07-22; historical MC/`dd_protection` challenge semantics still pin to `FIRM_RULES["FXIFY"]` by name, just not via this selector).

---

## §0 — Rule 0 reads (production-source verification)

- [`lab/analysis/c1/q_rail_1_2026-07/PHASE4.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE4.md) + [`PHASE3.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE3.md) + [`F_SCORECARD.md`](../../lab/analysis/c1/q_rail_1_2026-07/F_SCORECARD.md) — authored/verified this session (F1–F5 all PASS; cost table sourced 2026-07-17; §10 hooks re-run green same day).
- `core/firm_rules.py` — anchor `a53ee99` (re-verified this session): `Tradeify_Select_100K` trailing_locking 3.0% / $100 lock / cap 80 / $0.91/side / consistency 40.0 eval-only-soft.
- [`docs/spec/c1_watch_realization_multiplier_layer.md`](../spec/c1_watch_realization_multiplier_layer.md) — `Accepted` 2026-07-17; §2 single rail-side integer-floored qty computation; §3 rules out TV-side scaling; §4 screen PASS via NT8-host row B.
- Operator ceiling: **$700** signed 2026-07-17 (`AskUserQuestion` against the assembled cost table — recorded in the Q-RAIL-1 closure and §8 of the parent brief).
- Operator GO: chat, 2026-07-17 — "GO on rail build + account registration."

---

## §1 — Context

Q-RAIL-1 closed `RESOLVED` 2026-07-17: all five execution-fidelity preconditions PASS at both discharge tiers, the rail chain is documented end-to-end from primary sources, and the operator signed the deferred §8 ceiling at $700 (both tiers clear with one-reset headroom). The pre-registered disposition of a RESOLVED close is exactly one open fork: operator GO/NO-GO on rail build + account, recorded as a fresh ADR. The operator issued the GO the same day.

**Decision driver (one sentence):** the decision-ready packet exists, the ceiling is signed, and every live-data-starved monitor in the estate (Q-DECAY-1 re-arm, lifecycle Call-1, ORB decay calibration, Q-NAS-ECR-1 successor) waits on a first fill source — delaying the GO after RESOLVED has cost and no informational gain.

---

## §2 — Decision

**Decision:** Commission the c1 execution rail — **TV alert → CrossTrade cloud → NT8 Add-On → Tradovate** — and register **one `Tradeify_Select_100K` evaluation account** (tier per the packet's §5 recommendation under the ratified "packet decides" delegation; MFFU Rapid remains the named fallback), to run the c1 2-leg book (Striker DJ30→MYM + Striker NAS100→MNQ venue editions) at **WATCH-1 0.50× realized at the account-multiplier layer**, attended-automation posture per envelope E6.

**Effective:** immediately upon acceptance (2026-07-17).
**Scope:** one eval account, one rail instance, c1 book only. Spend ceiling **$700 all-in to first live fill** (eval + 3 months run-rate; one reset headroom). ORB-MNQ-1 go-live is explicitly NOT in scope (its own Pine/rail gates stand).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| MFFU Rapid 100K first | $86–$156 dearer to first fill; post-16:10 orders can DISQUALIFY (hard failure mode vs Tradeify's non-fatal 16:59 auto-flatten). Packet §5 scored it fallback; nothing forecloses it later — Tradeify exclusive-use only binds once a Tradeify bot exists. |
| Both tiers at once | Tradeify FTA §6.6 exclusive-use forbids the same bot across firms; doubles spend before the rail is proven; packet pre-registered "live GO picks one first account." |
| NO-GO / wait for 08-08 | The 08-08 packet gains nothing from a parked RESOLVED closure; every fill-starved monitor stays starved; the JULY promo basis ($111 eval) expires 2026-07-31. |
| TV → Tradovate native (skip CrossTrade/NT8) | Tradovate API is LIVE-funded-only per envelope §4 (unavailable on eval); loses Account Manager EOD safeguards that implement E1; not the E6 reference rail. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger:** any of — (a) the rail cannot demonstrate the F1 sizing law end-to-end in **dry-fire** (CrossTrade `PLACE` carrying a computed `qty` from the NT8-side host, fail-safe proving most-conservative-tier on unreadable state) before the first armed session; (b) projected or actual all-in spend to first live fill exceeds **$700**; (c) a ToS/automation-posture change at Tradeify surfaces during wiring (Phase-0-class re-verify fails).

**Revert action:** halt build, zero armed sessions, flatten nothing (nothing is live pre-trigger); escalate to operator with the named blocker — fallback fork is MFFU Rapid under a status amendment to this ADR (supersede-in-part), not a silent tier swap.

**Trigger check schedule:** at every build milestone in §7 (B6 dry-fire is the load-bearing gate); spend tally re-checked at each purchase.

---

## §5 — Forbidden moves (under this ADR)

- **Arming a session before the B6 dry-fire passes** — the sizing host's fail-safe is the guard against the M8 failure mode (TV full-size fill); tempting because the rail "looks connected" earlier.
- **Realizing WATCH-1 via TV risk%-input scaling** — Q-PYRPARITY-1 `FALSIFIED-NONPROPORTIONAL`; the spec §3 rules it out; the haircut lives at the multiplier layer only.
- **Buying the Tradeify eval with the Rithmic/TradeSea broker** — M6 landmine; NT8/CrossTrade cannot attach; checkout must select **Tradovate**.
- **Running the same bot on MFFU concurrently** — FTA §6.6 exclusive-use.
- **Unattended / lights-out operation** — Q-BTC-3 falsified that lane; E6 attended bar binds (presence calendar PHASE3 §3; EOD flatten armed ≤16:00 ET).
- **Switching `ACTIVE_FIRM`** — anchor byte-reproducibility fixture; engine runs for this program use the tier configs directly.
- **Widening scope to ORB-MNQ-1 or a second account** because the rail exists — each is its own gated decision.
- **Arming any session with neither the CrossTrade Account Manager nor the operator 15:55 ET flat-check active** (added 2026-07-19 addendum) — the Pine force-flat is rail-dependent and must never be the sole own-flatten layer; a second, rail-independent layer (human 15:55 check now, automated AM when it ships) is required. Tradeify's 16:59 auto-liq is a final catch, never the designed mechanism (envelope E1: "never design to the auto-flatten as a backstop").

---

## §6 — Consequences

**Positive:** first live fill source since FXIFY closure; pre-registered unblocks fire — **Q-NAS-ECR-1 successor Pre-Q authorized** (fresh Pre-Q, MNQ fill microstructure); **ORB-MNQ-1 decay-monitor calibration re-scoped to the live venue**; Q-DECAY-1 re-arm limb and lifecycle Call-1 gain a live input path.

**Negative (real):** ~$49/mo standing bridge cost while the eval runs (~2× median pass time at WATCH-1 → plausibly >3 months); operator attendance obligation (seasonal window ≈09:00–13:15 ET, Mon/Tue/Fri + EOD daily); build work (payload contract + NT8 host) precedes any fill.

**Risks:** WATCH-1 pass-rate ≥95% is bust-geometry, not P&L promise; common-mode edge death remains uncovered (Q-DECAY-1 — drawdown-only detection); +0.46pp bust optimism (Q-PERSIST-1); H1 regime rescue is the haircut's doing. All carried verbatim from the packet — the GO is taken with these read.

**Downstream artifacts:** CLAUDE.md posture line (pointer only); STATE executed-decisions line + fill-starved thread annotations; SESSIONS entry; Q-RAIL-1 closure's "On GO" list activates.

---

## §7 — Implementation plan (build order; no step skips its predecessor)

| # | Step | Executor | Status |
|---|---|---|---|
| B1 | Alert-payload contract fields (`{leg_id, signal_type, bar_time, close, stop_dist_pts}`) on both venue editions + PORT_MANIFEST re-pin (spec §7 Phase 1) | CC/Cursor (Pine, gitignored) | **DONE 2026-07-17** — additive `alert()` calls landed on both venue editions (`42166af8…` DJ30/MYM, `139eb43d…` NAS100/MNQ); `pine_check.py` clean; F3 evidence unaffected (alert-only diff). FUTURES_LOCK.md + PORT_MANIFEST.sha256 updated. |
| B2 | Sizing host: account × lifecycle × DD → integer qty; fail-safe = most-conservative tier on unreadable state (spec §2/§6) | CC (spec + implementation — **Option C pivot means no Cursor/C# port needed**) | **ARCHITECTURE PIVOT 2026-07-18: Option C ADOPTED** (operator decision) — CrossTrade's direct-Tradovate webhook auth has no TV-specific gating, so the sizing computation runs in Python, not NinjaScript; NT8/ATI stay wired as a dormant fallback. Spec frozen 2026-07-17, algorithm tested 2026-07-18 ([`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py), 29 tests vs the `f2_floors.json` oracle) and transport built+tested same day ([`ops/c1_rail/crosstrade_payload.py`](../../ops/c1_rail/crosstrade_payload.py) 8 tests, [`ops/c1_rail/c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py) 9 tests; RED phase caught a real exit/flat gating bug before it shipped). **HTTP adapter + §2.5 landed 2026-07-18** ([`ops/c1_rail/c1_rail_http_server.py`](../../ops/c1_rail/c1_rail_http_server.py) — path-token gate + `equity_source` file/crosstrade; helpers unit-tested). Remaining before B6: always-on host+TLS standup (operator), live `equity_field` verify, instrument-symbol-format check. |
| B3 | CrossTrade **Pro** subscription (7-day trial first) + Account Manager: EOD flatten ≤16:00 ET, trailing-DD guard | Operator (account) + CC (config doc) | **DONE 2026-07-18** — Pro Monthly Unlimited **Active** (next charge Aug 18 2026); Account Manager unlocked. AM *settings* application (EOD flatten 15:55 ET, DD guard) tracked as [RUNBOOK](../notes/rail_build/RUNBOOK.md) B5d, applied pre-B6. |
| B4 | **Tradeify Select 100K checkout — Tradovate broker selected** (promo code JULY before 2026-07-31 → $111; else $181) | **Operator only** (account creation + payment) | **DONE 2026-07-18** — Select 100K · Evaluation · EOD, Tradovate platform FREE; **paid $159** (cart beat list/promo; invoice retained). Tally $208/$700. |
| B5 | trader.tradovate.com login → data agreement → NT8 8.1+ install, multi-provider on, Add-On connected, Account Type = Simulation | Operator (creds) + CC (checklist) | **DONE 2026-07-18** — Tradovate login + data agreement done ($0 data confirmed); NT8 desktop + XT Add-On connected; **ATI enabled**; NT8 spine wired as dormant fallback under Option C. |
| B6 | **Dry-fire gate:** Webhook Trader test end-to-end — computed qty lands; fail-safe proves; Strategy Sync green. §4(a) checks here. | Operator + CC | **PENDING** — pre-reqs before the 5-check dry-fire: always-on host + TLS standup, host state files ([RUNBOOK](../notes/rail_build/RUNBOOK.md) B5e; constants pre-flighted PASS 2026-07-18), AM settings (B5d), and the in-gate `equity_field`/instrument-symbol verifies. |
| B7 | First armed session per attended calendar (PHASE3 §3); failure-mode protocol M1–M8 printed at the desk | Operator | **PENDING** — blocked on B6. |

---

## §10 — Audit hooks (runnable)

```bash
# This GO is the only rail authorization; the research-ADR guard still holds upstream
grep -n "rail-build, account-registration, or live-spend" docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md
grep -rn "2026-07-17-c1-rail-build-account-registration-go" STATE.md docs/SESSIONS.md CLAUDE.md   # expect: pointer lines present

# No armed session before dry-fire: build artifacts must show B6 evidence before any fills log exists
ls docs/notes/rail_build/ 2>/dev/null || echo "no build notes yet - expected until B1 starts"

# Spend ceiling tally (update at each purchase; must stay <= 700)
grep -n "CEILING SIGNED" lab/analysis/c1/q_rail_1_2026-07/PHASE4.md

# Tier constants unchanged at build time (re-run before B2 arithmetic)
git log -1 --format='%h %cs' -- core/firm_rules.py   # a53ee99 at GO; investigate drift
```

---

## Verification

```bash
python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-07-17-c1-rail-build-account-registration-go.md --type adr
python scripts/check_adr_graph.py
grep -n "RESOLVED" docs/briefs/closures/Q-RAIL-1-closure-resolved.md
```

---

## Addendum — 2026-07-18: MYM Step-2 parity override re-affirmed against corrected exit-lag census

An adversarial re-audit of the F3 evidence (STEP2_PARITY.md) found the MYM per-candle
parity override — one of the fidelity limbs this GO's §0 Rule-0 reads cite as PASS —
was granted 2026-07-17 against an **understated** exit-lag census: the documented
bound was "MYM 1–3 bars later," T9 (+3), T11/T12 (+2). Independent re-comparison of the
underlying exports found **9 lagged exits**, not 3, including one pair at **+10 bars
(2.5 hours)**: T9/T11/T12 as documented, plus T25/T26 (+1, 2026-01-06), T29/T30 (+10,
2026-02-08 22:30 → 02-09 01:00), T37 (+1, 2026-05-29), T42 (+3, 2026-06-30). Full table:
[`lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md`](../../lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md).

**Operator re-affirmation (chat, 2026-07-18):** *"re-affirm the override against the
corrected census."* The override stands as-is against the corrected facts — entry-
cascade mechanism (larger CFD size → earlier day-stop soft-halt → MYM's smaller integer
size stays free to re-enter) and exit-lag absorption both re-affirmed; F3 stays `PASS`.
The pre-registered discharging same-size control (unrun at original grant) remains the
open revisit condition, unchanged by this re-affirmation — binds before any live-fill
claim leans on MYM CME-native timing precision, and in particular before/at **B6
dry-fire** (§7).

No change to §2 Decision, §4 Falsifier, or §5 Forbidden moves — the corrected census
does not flip a PASS to FAIL, does not change the tier recommendation, and does not
add a new forbidden move. It is carried into §6 Risks and PHASE4.md §3 Standing risk
framing (updated same date) because it is new information material to a risk already
accepted, discovered after ratification — same class of correction as the
[2026-06-07 decompound-remc HOLD addendum](2026-06-07-decompound-remc-hold.md)
(severity-corrected figures, verdict unchanged).

Also landed same date: the 12 F3 Step-2/C3 evidence CSVs (previously Downloads-only,
unpinned) archived into `core/data/tv_exports/{pepperstone,cme}/` with SHA256SUMS
regenerated — closing the evidence-volatility gap the same re-audit surfaced.

---

## Addendum — 2026-07-19: E1 EOD-flat coverage without the CrossTrade Account Manager (Option C)

**§0 reads (this addendum):** [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) §1 **E1 row** (line 16, v1.0 RATIFIED 2026-07-13) + §… line 55 ("E1 default print — CONFIRMED 16:00 ET"); [`PHASE3.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE3.md) E1/F4 rail rows (lines 27, 63, 168, 179); [`RUNBOOK.md`](../notes/rail_build/RUNBOOK.md) B5d BLOCKED note (2026-07-19). CrossTrade dashboard verified same day: banner "Account Manager for Tradovate is coming soon," left-nav AM carries a SOON badge.

**Discovery (wiring-time, B5d):** the CrossTrade **Account Manager** — the Pro-tier auto-flatten that [`PHASE3.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE3.md) maps to **E1** — is **not yet available for the Tradovate destination**. This is a CrossTrade-side capability gap surfaced during wiring, not a Tradeify ToS change (so §4(c) does not fire), but it removes an *automated* safeguard the GO packet assumed.

**What E1 requires (verbatim, envelope §1):** *"All positions closed before the daily flat deadline; build target 16:00 ET."* Load-bearing caveat: *"never design to the [firm] auto-flatten as a backstop."* E1's substance is **your own** flatten by 16:00 ET, in ≥1 layer that is not the firm's auto-liquidation.

**Decision (operator, chat 2026-07-19) — Option C:** proceed to B7 on a **two-layer own-flatten stack**, the CrossTrade AM deferred:
1. **Pine 15:45-bar force-flat** — automated, but **rail-dependent** (needs TV→Fly→CrossTrade→Tradovate up).
2. **Operator manual 15:55 ET flat-check** — **rail-independent**, performed **every session that carried open risk**; flatten via the Tradovate/CrossTrade manual dashboard if any position is open. This is the interim human replacement for the AM's automated rail-independent layer.
- Tradeify **16:59 ET firm auto-liq** remains **final catch only** — never the designed mechanism.

**Rationale:** (a) MYM/MNQ trade **morning sessions (8–12 ET)** and force-flat intraday — a position open at 15:45 is already an exception; (b) **Tradeify's auto-flatten is NON-FATAL** (envelope's exact reason Tradeify was the recommended tier; contrast MFFU, where post-16:10 orders can *disqualify*) — so the worst-case final catch is not account-ending; (c) WATCH-1 **0.50×** sizing keeps positions small.

**Residual explicitly accepted:** (i) EOD-flat — the compound case *(position open at 15:45 **and** rail down **and** operator absent)* falls to Tradeify's non-fatal 16:59 auto-liq; (ii) **the AM's automated pre-emptive DD-guard flatten is NOT replaced by Option C** — it stays covered only by WATCH-1 bust geometry (≥95%), the sizing-host `DD_SCALE`, and attendance, not by an automated pre-line flatten. Both carried with eyes open.

**Re-add trigger (binary, non-discretionary):** when CrossTrade ships AM-for-Tradovate (banner clears / AM configurable against the linked Tradovate account), apply the [`RUNBOOK.md`](../notes/rail_build/RUNBOOK.md) **5d** settings (EOD flatten 15:55 ET + DD guard) — restoring the automated rail-independent layer *and* the automated DD-guard. This is a **re-add, not a re-decision**; the operator 15:55 manual check may then relax to a backstop.

**Effect on parent sections:**
- **§5 Forbidden moves — ADDS one:** *arming any session with **neither** the CrossTrade AM **nor** the operator 15:55 ET flat-check active* (i.e., never run on the Pine force-flat as the sole own-flatten layer — the second, rail-independent layer, human or automated, must be present).
- **§7 B3/B5d:** AM settings **deferred** (not actionable until CrossTrade ships them); **B7 checklist ADDS** the operator 15:55 ET flat-check on every session that carried open risk.
- **Open item discharged:** this is the "E1 pre-B7 decision" the [`RUNBOOK.md`](../notes/rail_build/RUNBOOK.md) B6 progress log flagged as gating the `dry_run=false` flip.

No change to §2 Decision (tier stays Tradeify Select 100K), §4 Falsifier, or the WATCH-1 0.50× posture. Nothing arms on this addendum; B6 dry-fire and the remaining B6 items still precede B7.

**Audit hooks (runnable):**
```bash
# E1 requirement text unchanged at the source this addendum quotes
grep -n "never design to the" ops/prop_envelope_default.md          # expect the E1 caveat
grep -n "Account Manager for Tradovate is coming soon\|BLOCKED — DEFERRED 2026-07-19" docs/notes/rail_build/RUNBOOK.md
# The added forbidden move + B7 flat-check must be present before B7 is signed
grep -n "15:55 ET flat-check" docs/adr/2026-07-17-c1-rail-build-account-registration-go.md docs/notes/rail_build/RUNBOOK.md
```

---

## Addendum — 2026-07-22: Tradeify hedging rule — c1 CLEARS by construction; contract-cap defect fixed; one open B7 input

**§0 reads (this addendum).** Primary, [`help.tradeify.co`](https://help.tradeify.co) read 2026-07-22: [`10495868`](https://help.tradeify.co/en/articles/10495868) (hedging, article updated 2026-07-21) · [`10495876`](https://help.tradeify.co/en/articles/10495876-rules-permitted-times-to-trade) · [`10468222`](https://help.tradeify.co/en/articles/10468222) · [`10495897`](https://help.tradeify.co/en/articles/10495897-rules-trailing-max-drawdowns) · [`12853921`](https://help.tradeify.co/en/articles/12853921-select-evaluation-accounts) · [`12268167`](https://help.tradeify.co/en/articles/12268167-essential-trading-rules-overview); MFFU [`13286542`](https://help.myfundedfutures.com/en/articles/13286542). Production: `core/strategies/striker/striker_dj30_v4.5_mym.pine` + `core/strategies/nas/striker_nas100_v1_mnq.pine` (locked Pine, gitignored — read on disk); [`ops/c1_rail/c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py) `_leg_action`; [`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py).

### Hedging / correlated products — CLEARS, no guard required

Tradeify prohibits **opposing directions within a Product Group**, in one account or across any accounts under the same control. The **Equity Index** group contains `ES, MES, NQ, MNQ, YM, MYM, RTY, M2K, EMD, NKD` + EUREX index — so **c1's two legs share a group**. Consequences are severe: violation status on *every* account involved, profit forfeiture, possible permanent ban. Nothing in the repo encoded this rule.

**The two legs cannot ever be opposite-signed.** Three independent layers:

1. **Locked Pine (decisive).** Both venue editions are structurally long-only: **zero `strategy.short`** (also zero in the two CFD editions). Entries are only `strategy.entry(…, strategy.long, …)`; every exit is `strategy.exit` / `strategy.close_all`, which flatten and never reverse. The dashboard renders `LONG ONLY`.
2. **Rail.** `_leg_action` hard-codes `"buy"` for `entry`/`add` (*"c1 is long-only"*) and maps `exit`/`flat` to `command=closeposition`. No sell-to-open path exists; a `closeposition` cannot open a short.
3. **Realized.** Zero short entries across ~6,000 trade rows, every Striker DJ30 / NAS100 export vintage, CFD and venue-native.

Reachable joint states are **long+long** and **long+flat**. Tradeify lists long+long explicitly under *What IS Allowed*. **This is a proof of non-reachability, not an accepted risk.**

**Caveat worth recording:** the three-condition automated breach (opposing + >10s + >$250 profit) is **not a safe harbour** for the correlated-product case — that bucket is *"monitored separately and reviewed by our risk team"* with no published threshold. Moot for c1 as constituted; recorded so nobody later reasons "under $250 is fine."

**§5 Forbidden moves — ADDS one:** *adding any short-capable or long/short leg on an **Equity Index** Product Group instrument to this account, or to any account under the same control, while a long Equity Index leg can be open.* The published list is explicitly **not exhaustive**, and long **FVS** (Volatility) against long Equity Index is also treated as offsetting. This bites a live research direction: the Stage-8 gate ([ADR 2026-07-20](2026-07-20-stage8-variance-dominance-risk-neff-gate.md)) *rewards* `n_eff_risk_delta > 0`, and a negatively-correlated same-group leg is exactly what that gate favours and this rule forbids. Decorrelation candidates must now be screened for **Product Group + sign** before scoring.

### Contract cap — real defect, FIXED

The same article makes the cap explicitly combined: *"Your combined position must stay within your account's contract limit, counted at 10 micros = 1 mini"* (100K = 8 mini / 80 micro, [`12268167`](https://help.tradeify.co/en/articles/12268167-essential-trading-rules-overview)). The sizing host applied `cap_firm` **per leg**, each against the full 80 → worst case **MYM 76 + MNQ 77 = 153 micros, 1.91× the account limit**.

**Not theoretical.** On the pinned venue-edition exports: MYM is cap-bound in **93%** of trades (40/43); **22.1%** of DJ30 trades carry a simultaneous NAS position; observed **max combined 98 micros** (2025-10-14 12:15 = MYM 76 + MNQ 22). WATCH-1 0.50× does not rescue it — the haircut scales `r_eff`; the cap branch is invariant.

**Severity.** Tradeify does not publish the enforcement mechanism. MFFU, same firm class and same 8/80 numbers, does: exceeding it *"can result in a **breach** of the trading account."* Planned for breach, not a bounced order. **Open cheap action for the operator:** ask Tradeify support whether over-cap hard-rejects; a confirmed hard reject drops this to an execution defect and would let the split relax.

**Fix (operator-approved):** static per-leg allocation of the account cap — **MYM 69 / MNQ 11** → maxima 68 + 11 = **79 ≤ 80**. Stateless, deterministic, oracle-pinnable, provably compliant by construction. A missing/oversized `cap_alloc` halts to zero rather than falling back to the permissive whole-account cap. Cost: MYM base 9→8; MNQ capped at base 1. Locked pyramid ratios (750%/1000%) untouched — this allocates a *firm constant*. A runtime joint check was rejected: the host deliberately does not track live position size (`crosstrade_payload` omits quantity on close for exactly that reason), so sizing a compliance-critical budget off that bookkeeping is the M8 class the fail-safe doctrine exists to prevent; it would also make qty order-dependent when both legs fire on the same 15m close. **Upgrade path:** when the host gains verified position truth, the split relaxes to a runtime headroom check — same re-add shape as the 2026-07-19 AM trigger. `f2_floors.json` re-pinned (MYM 9/67 → 8/60), originals retained under `pre_2026_07_22_whole_cap_per_leg`.

### ⚠️ Open B7 input — §6's WATCH-1 0.50× figures are UNMEASURED under corrected geometry

The eval-tier drawdown-locking defect ([`lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md)) means the 0.50× figures §6 cites — full-panel bust 0.08%, H1 0.14%, bootstrap-95th 0.77% — were computed with a cushion the eval phase does not have. **Known-optimistic by an unmeasured amount**; direction certain, magnitude not. The corrected run was stopped on runtime cost before reaching that arm. The +2.10pp measured at 1.00× must **not** be scaled to 0.50× — halved risk interacts with the barrier non-linearly. Closing needs only the full-panel reference (≈3 min), not the n=100 bootstrap. **Recommend closing before B7 arms.** The GO itself is not overturned: the withdrawn Part A discharge is a different gate ([ADR 2026-07-22](2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)).

> **CLOSED 2026-07-24 — measured benign. See Addendum 2026-07-24 below.**

### Flat deadline corrected

**16:45 ET** regular (12:59 ET holiday-short), tightened from the 16:59 ET this ADR carried. **Verified harmless before editing:** the E1 target (16:00 ET), the Pine 15:45 force-flat, and the operator 15:55 check all sit inside the tighter print, and the auto-flatten remains explicitly **non-fatal** — the property the 2026-07-19 Option-C addendum leans on. Read every "16:59" in the 07-19 addendum as **16:45**.

**Audit hooks (runnable):**
```bash
python -c "import pathlib,sys; f=[p for p in ('core/strategies/striker/striker_dj30_v4.5_mym.pine','core/strategies/nas/striker_nas100_v1_mnq.pine') if pathlib.Path(p).exists()]; sys.exit(0) if not f else [print(p,'strategy.short x',pathlib.Path(p).read_text(encoding='utf-8',errors='replace').count('strategy.short')) for p in f]"
grep -n 'entry / add are always long' ops/c1_rail/c1_rail_listener.py     # rail long-only invariant
python -m pytest tests/ops/test_c1_sizing_host_reference.py -q -k "cap"   # combined-cap invariant
grep -n '§4a' ops/prop_envelope_default.md                        # hedging overlay present
```

---

## Addendum — 2026-07-24: §6's WATCH-1 0.50× figures MEASURED under corrected geometry — open B7 input CLOSED benign

Operator directive 2026-07-24 ("proceed with the two unmeasured arms"). Run:
[`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md`](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md)
(frozen 2026-07-15 primitives + the 2026-07-22 correction idiom; reproduction
controls matched every published corrected pin, incl. 1.00× full 4.74%/4.25% and
H1 6.78%/6.28%).

**Corrected WATCH-1 0.50×, $100K basis, both discharge tiers:** full-panel bust
**0.11%** (pass 99.80/99.81%), **H1 0.22%**, **H2 0.04%** — every partition
PASSES the frozen floor. Versus the defective-geometry figures §6 cited
(0.08% / 0.14%): the correction costs **+0.03pp full-panel / +0.08pp H1** at the
deployed rung. The §5-forbidden down-scaling of the 1.00× delta is empirically
vindicated: +2.10pp at 1.00× vs +0.03pp at 0.50× — strongly non-linear barrier
interaction. Still unmeasured (declared): the corrected 0.50× bootstrap-95th
(defective 0.77% vs 3.0% ceiling; separable long pole, not a B7 gate per the
withdrawal ADR's own close recommendation). Read §6's risk framing with these
corrected values; the GO stands unchanged. Same-day sibling result (separate
pre-registration, not this ADR's scope): two corrected-geometry Part A clearers
exist at the 50K band —
[`lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md`](../../lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md).

## Addendum 2026-07-28 — the declared separable long pole is MEASURED and CLEARS

The Addendum 2026-07-24 left exactly one open measurement on the deployed rung:
the **corrected-geometry 0.50× bootstrap-95th** (defective-era 0.77%), declared a
separable long pole and explicitly **not** a B7 gate. It is now measured.

`Tradeify_Select_100K` @ **WATCH-1 0.50×**, corrected geometry (worker-local patch,
all 100 panels attested at `dd_lock_offset_usd = 1e6`), frozen rider primitives
(`BOOT_SEED=20260715`, n=100, block=126bd, seeds 42/123/2026, 10K sims/seed,
horizon 1500):

| Partition | Bust | Floor (≤3.0% ∧ pass ≥50%) |
|---|---|---|
| Full-panel | 0.11% | PASS |
| H1 | 0.22% | PASS |
| H2 | 0.04% | PASS |
| **Bootstrap-95th** | **1.20%** (pass-5th 95.5%) | **PASS** |

Reproduction controls reproduced the published corrected full/H1/H2 pins exactly.
Correction cost at the bootstrap tail is **+0.43pp** (0.77% → 1.20%), leaving
1.8pp of headroom under the 3.0% ceiling. **Every partition of the deployed
configuration is now measured under corrected geometry and passes** — no open risk
measurement remains on the 0.50× rung. Evidence:
[`lab/analysis/c1/eval_shape_diagnostics_2026-07-28/RESULTS.md`](../../lab/analysis/c1/eval_shape_diagnostics_2026-07-28/RESULTS.md)
Part B · `rider_050x_report.json`.

**Scope discipline, unchanged.** This closes a *measurement*, not a gate: it was
never a B7 gate, and it does not touch B7's actual blockers (M1 `RESOLVED` +
operator GO), the §4 falsifier (undischarged; scored at the $100K band at 1.00×),
or any locked parameter. Same pass established that **1.00× is far worse than
previously published** under corrected geometry (bootstrap-95th **17.79%**), which
strengthens rather than disturbs §5's no-downscaling rule and the choice of the
0.50× rung.

## Addendum 2026-08-04 — the DEPLOYMENT limb is spent; the build stands, disarmed

⚠ **Reader-intercept: this ADR is no longer authorization to deploy anything.**
[`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md)
de-scoped the Tradeify venue as a deployment target for the locked Striker book, **evaluation
included**, and withdrew both Striker legs (DJ30→MYM, NAS100→MNQ) from the c1 eval deployment.
Recorded here — not only at the superseding ADR — because this is the artifact a reader consults
when asking *"what was authorized?"* (`docs/operational_rules.md` Rule 14: corrections land where
the error is READ). The header now carries the reciprocal `Superseded-in-part-by` edge.

**What §2 no longer authorizes:**

- Deploying the locked Striker book to Tradeify in **either** phase — funded **or evaluation**.
- Any successor deployment at this venue without a superseding ADR under the de-scope's §4 triggers.
- B7-REFIRE Stage 1 **as a Tradeify milestone**: it stays owed, and is undischargeable *at this
  venue* while no strategy is deployed to emit the signal. ⚠ Note precisely what that is **not**:
  M1 item 5 is a `dry_run` strategy signal at non-zero size, *"unarmed by design"*, which routes no
  order — so the blocker is the absence of a deployed strategy, **not** a standing rule making M1
  unresolvable. Deploying any qualifying strategy makes it dischargeable again.

**What stands, byte-untouched:**

- The rail **build** and its architecture; the **registered account**; the **attended-only** posture;
  the **$700** spend ceiling ($208 committed); the per-session arm-GO discipline; and the arm gate
  itself (`dry_run=false` barred while M1 is not `RESOLVED` — Addendum 2026-07-31b moved the trigger
  send→arm). The rail is **retained and DISARMED**, pointed at a de-scoped venue, pending fork **F2**
  (rail disposition, 2026-08-08), which also governs the account and the M1 spine.
- **§2, §4, §5 and every prior Addendum are unedited** (Trap #12 — frozen bodies are never rewritten
  in place). This Addendum is the intercept, not a revision.
- The lifecycle axis: both legs remain `AUTHORIZED @ 1.00×`. **Venue-fit is not decay.**

**Scope of the de-scope, stated so it is not over-read:** its same-day Addendum narrows the bar to
*redeploying those two legs*. **Tradeify-shaped research is expressly not barred**, and Tradeify
remains 1 of the 4 firms in the frozen prop-portfolio §4 falsifier set.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-17 | Initial authoring; Accepted on operator chat GO | Joshua + Claude Code |
| 2026-07-18 | Addendum: MYM Step-2 override re-affirmed against corrected exit-lag census (operator chat); F3 evidence CSVs archived | Joshua (re-affirm) + Claude Code (audit + recorder) |
| 2026-07-19 | Addendum: E1 EOD-flat coverage without CrossTrade AM — Option C (operator chat); adds §5 forbidden move + B7 flat-check; discharges the pre-B7 E1 decision | Joshua (decision) + Claude Code (recorder) |
| 2026-07-22 | Addendum: Tradeify hedging rule verified — c1 CLEARS by construction (long-only at Pine, rail, realized); adds §5 forbidden move (no short-capable Equity Index leg); account-aggregate contract cap defect FIXED via 69/11 split (operator-approved) + f2_floors re-pin; flat deadline 16:59 → 16:45 ET; flags §6's WATCH-1 0.50× figures as unmeasured under corrected eval geometry | Joshua (cap disposition) + Claude Code (verification + recorder) |
| 2026-07-24 | Addendum: §6 WATCH-1 0.50× figures **measured** under corrected geometry (operator "proceed with the two unmeasured arms") — full 0.11% / H1 0.22% / H2 0.04%, all PASS; open B7 input **closed benign**; corrected 0.50× bootstrap-95th declared the remaining separable long pole | Joshua (directive) + Claude Code (runner + recorder) |
| 2026-07-28 | Addendum: the declared separable long pole **measured and CLEARS** — corrected 0.50× bootstrap-95th **1.20%** vs the 3.0% ceiling (pass-5th 95.5%); every partition of the deployed rung now measured + passing; same pass found corrected 1.00× boot-95th 17.79% | Claude Code (Opus 5) — adjudication of PR #541 |
