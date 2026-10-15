# ADR 2026-07-17 — GO: c1 execution-rail build + Tradeify Select 100K account registration

**Status:** Accepted (operator executive decision, recorded)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - `ACTIVE_FIRM` retention prohibition only. The c1 rail build, Tradeify registration, attended-only posture, spend ceiling, and B7 arm-gate stand.
**Superseded-in-part-by:** `2026-07-22-c1-venue-native-monitoring-maturity.md` - next `dry_run=false` entry/add send / B7-REFIRE Stage 2 gains the M1 operational-monitoring gate. Rail build, account registration, attended posture, and spend ceiling stand.
**Superseded-in-part-by:** `2026-08-04-tradeify-venue-descope-eval-included.md` - **DEPLOYMENT LIMB ONLY.** Tradeify is no longer a deployment target for the locked Striker book, **evaluation included**, and both legs are withdrawn from the c1 eval deployment. §2's authorization to *deploy* is spent. The rail build, the account registration, the attended-only posture, the $700 spend ceiling, and the arm gate all **stand** — the rail is retained and **disarmed** (fork F2 ruled 2026-08-07 by [S1](2026-08-07-loop-s1-environment-ratification.md): built, warm and disarmed at the incumbent eval). See the dated Addendum 2026-08-04 below.
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
`CODE_LANDED`, **not** `RESOLVED`, as of 2026-08-08. M1 has been `RESOLVED` since 2026-09-14 ([acceptance](../notes/rail_build/M1_MONITORING_ACCEPTANCE.json)); while #571 is parked it supports no legacy-leg arm ([M1 Addendum 2026-10-01](2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-10-01--transport_unknown-risk-add-block-proven-only-within-one-process-571-parked)).
**Decision date:** 2026-07-17
**Authors:** Joshua (decision) + Claude Code (recorder)
**Supersedes:** none — this ADR **discharges** the rail-build/account/live-spend gate held open by [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) ("rail build, account registration, and any live spend gated" on operator GO) and satisfies [`2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) §5 (no research ADR is rail authorization — a fresh operator decision + ADR is; this is that ADR). Manual-trading retirement ([`2026-06-30-no-manual-trading-cfd-retirement.md`](2026-06-30-no-manual-trading-cfd-retirement.md)) stands untouched — attended automation is not manual execution.
**Related:** [`Q-RAIL-1 closure RESOLVED`](../briefs/closures/Q-RAIL-1-closure-resolved.md) (the decision packet this GO consumes); GO packet [`PHASE4.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/q_rail_1_2026-07/PHASE4.md); rail architecture [`PHASE3.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/q_rail_1_2026-07/PHASE3.md); sizing contract [`docs/spec/c1_watch_realization_multiplier_layer.md`](../spec/c1_watch_realization_multiplier_layer.md) (`Accepted` 2026-07-17); NT8 sizing-host implementation spec [`docs/spec/c1_nt8_sizing_host_impl.md`](../spec/c1_nt8_sizing_host_impl.md) (`Proposed`, B2, 2026-07-17); [`Q-PYRPARITY-1 closure`](../briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md) (F1 fallback); c1 ratification [`G8_INTAKE.md`](../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md).
**Layer:** execution — **not** locked-parameter. No change to locked Pine, allocations, `dd_protection` constants, or the FXIFY MC anchor pins (~~`ACTIVE_FIRM` stays FXIFY~~ — **superseded, see header**: the `ACTIVE_FIRM` selector and the FXIFY tier row were deleted in substrate Phase 4, 2026-07-30 (`core/firm_rules.py` provenance note); historical challenge semantics live in `core/historical_challenge.py` (opt-in fixture only), and the rail uses the explicit `Tradeify_Select_100K` tier key).

**Pointer re-home 2026-09-12 (TB-O1; reader-intercept, no clause amended):** the `RUNBOOK.md` links in the header clarification, the §7 table (B3, B6 rows) and the 2026-07-19 addendum (re-add trigger, discharged open item, audit hooks) name `docs/notes/rail_build/RUNBOOK.md`, a private file **not on the public tree**; those bodies stay byte-unedited (Trap #12; Addendum 2026-08-21). The public operating procedure is [`ARMING_PROCEDURE.md`](../notes/rail_build/ARMING_PROCEDURE.md); the private runbook is retrieved per its §2 (archive pin `5d47b4dc…`, or the primary checkout's ignored private root). See Addendum 2026-09-12 at the end of this file.

---

## §0 — Rule 0 reads (production-source verification)

- [`lab/analysis/c1/q_rail_1_2026-07/PHASE4.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/q_rail_1_2026-07/PHASE4.md) + [`PHASE3.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/q_rail_1_2026-07/PHASE3.md) + [`F_SCORECARD.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/q_rail_1_2026-07/F_SCORECARD.md) — authored/verified this session (F1–F5 all PASS; cost table sourced 2026-07-17; §10 hooks re-run green same day).
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

Consequences as of 2026-07-17 are history (full text: [this file at `4121e84c`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-17-c1-rail-build-account-registration-go.md)): a first live fill source and the fill-starved unblocks it listed; a standing bridge cost and an operator attendance obligation (the legs' locked signal window on their locked trading days + EOD daily) *(Redaction 2026-10-09 — operator decision 2026-10-09, option 2: Striker DJ30 v4.5 Pine-only parameter values removed from the public copy; no other content changed; original preserved in first-passage-archive `archive/preserve-exposure-2026-10-09` `7df79240c146ec8a3e9799bb882431c5ab13b9a7`; values live in the locked Pine only — [CATALOG §Locked parameter record](../../core/strategies/CATALOG.md#locked-parameter-record-cfd-era-book).)*; and the packet's risks, carried verbatim. The WATCH-1 0.50× figures those risks cited were re-measured under corrected geometry (Addenda 2026-07-24 and 2026-07-28), and the book was withdrawn from this venue on 2026-08-04 (Addendum 2026-08-04).

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
# Spend ceiling and its dated exemptions (§2, §4(b), Addenda 2026-10-01 and 2026-10-02)
grep -n '\$700\|\$500' docs/adr/2026-07-17-c1-rail-build-account-registration-go.md
# Hedging-clearance premise and contract-cap invariants (Addendum 2026-07-22)
grep -n 'entry / add are always long' ops/c1_rail/c1_rail_listener.py
python -m pytest tests/ops/test_c1_sizing_host_reference.py -q -k "cap"
grep -n '§4a' ops/prop_envelope_default.md
# E1 caveat at the source the 2026-07-19 addendum quotes
grep -n "never design to the" ops/prop_envelope_default.md
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

*Condensed 2026-10-15; full text in [this file at `4121e84c`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-17-c1-rail-build-account-registration-go.md).* The MYM per-candle parity override (an F3 fidelity limb) was granted 2026-07-17 against an understated exit-lag census; the re-audit found 9 lagged exits, not 3, including one pair at +10 bars. **Operator re-affirmation (chat, 2026-07-18):** *"re-affirm the override against the corrected census"* — F3 stays `PASS`; no change to §2, §4 or §5. The pre-registered discharging same-size control stays the open revisit condition, recorded with the corrected census in [`STEP2_PARITY.md`](../../lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md): it binds before any live-fill claim leans on MYM CME-native timing precision (the Striker DJ30 MYM edition it concerns is barred from redeploy since 2026-08-04).

---

## Addendum — 2026-07-19: E1 EOD-flat coverage without the CrossTrade Account Manager (Option C)

**§0 reads (this addendum):** [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) §1 **E1 row** (line 16, v1.0 RATIFIED 2026-07-13) + §… line 55 ("E1 default print — CONFIRMED 16:00 ET"); [`PHASE3.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/q_rail_1_2026-07/PHASE3.md) E1/F4 rail rows (lines 27, 63, 168, 179); [`RUNBOOK.md`](../notes/rail_build/RUNBOOK.md) B5d BLOCKED note (2026-07-19). CrossTrade dashboard verified same day: banner "Account Manager for Tradovate is coming soon," left-nav AM carries a SOON badge.

**Discovery (wiring-time, B5d):** the CrossTrade **Account Manager** — the Pro-tier auto-flatten that [`PHASE3.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/q_rail_1_2026-07/PHASE3.md) maps to **E1** — is **not yet available for the Tradovate destination**. This is a CrossTrade-side capability gap surfaced during wiring, not a Tradeify ToS change (so §4(c) does not fire), but it removes an *automated* safeguard the GO packet assumed.

**What E1 requires (verbatim, envelope §1):** *"All positions closed before the daily flat deadline; build target 16:00 ET."* Load-bearing caveat: *"never design to the [firm] auto-flatten as a backstop."* E1's substance is **your own** flatten by 16:00 ET, in ≥1 layer that is not the firm's auto-liquidation.

**Decision (operator, chat 2026-07-19) — Option C:** proceed to B7 on a **two-layer own-flatten stack**, the CrossTrade AM deferred:
1. **Pine 15:45-bar force-flat** — automated, but **rail-dependent** (needs TV→Fly→CrossTrade→Tradovate up).
2. **Operator manual 15:55 ET flat-check** — **rail-independent**, performed **every session that carried open risk**; flatten via the Tradovate/CrossTrade manual dashboard if any position is open. This is the interim human replacement for the AM's automated rail-independent layer.
- Tradeify **16:59 ET firm auto-liq** remains **final catch only** — never the designed mechanism.

**Rationale:** (a) MYM/MNQ trade **morning sessions (the locked window *(redacted 2026-10-09; see note above)*)** and force-flat intraday — a position open at 15:45 is already an exception; (b) **Tradeify's auto-flatten is NON-FATAL** (envelope's exact reason Tradeify was the recommended tier; contrast MFFU, where post-16:10 orders can *disqualify*) — so the worst-case final catch is not account-ending; (c) WATCH-1 **0.50×** sizing keeps positions small.

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

*Condensed 2026-10-15; the §0 source list (help.tradeify.co articles read 2026-07-22, the locked Pine, the rail code), the exposure figures and the audit hooks are in [this file at `4121e84c`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-17-c1-rail-build-account-registration-go.md). Venue facts are owned by [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) §4 (Tradeify row) and §4a.*

### Hedging / correlated products — CLEARS, no guard required

Tradeify prohibits **opposing directions within a Product Group**, in one account or across any accounts under the same control; MYM and MNQ share the Equity Index group (rule, group table, detection and consequences: envelope §4a). c1's two legs could never be opposite-signed: both locked venue editions are long-only (zero `strategy.short`), the rail's `_leg_action` hard-codes `"buy"` for `entry`/`add` and maps `exit`/`flat` to `command=closeposition`, and no short entry appears in any export. **This is a proof of non-reachability, not an accepted risk.** The automated three-condition breach is **not a safe harbour** for the correlated-product case, which Tradeify reviews separately with no published threshold (envelope §4a Detection; its profit limb is >$150 since 2026-10-02, was >$250).

**§5 Forbidden moves — ADDS one:** *adding any short-capable or long/short leg on an **Equity Index** Product Group instrument to this account, or to any account under the same control, while a long Equity Index leg can be open.* The published list is explicitly **not exhaustive**, and long **FVS** (Volatility) against long Equity Index is also treated as offsetting. This bites a live research direction: the Stage-8 gate ([ADR 2026-07-20](2026-07-20-stage8-variance-dominance-risk-neff-gate.md)) *rewards* `n_eff_risk_delta > 0`, and a negatively-correlated same-group leg is exactly what that gate favours and this rule forbids. Decorrelation candidates must now be screened for **Product Group + sign** before scoring.

### Contract cap — real defect, FIXED

The cap is **account-aggregate**: *"Your combined position must stay within your account's contract limit, counted at 10 micros = 1 mini"* (100K = 8 mini / 80 micro; envelope §4a contract-cap corollary). The sizing host had applied `cap_firm` **per leg**, so the two-leg book could reach 1.91× the account limit, and the pinned exports showed combined positions above 80. Plan for breach, not a bounced order, unless Tradeify confirms otherwise in writing (envelope §4a corollary); a confirmed hard reject would drop this to an execution defect and let the split relax.

**Fix (operator-approved):** static per-leg allocation of the account cap (`cap_alloc` in `LEG_MAP`, [`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py)) — stateless, deterministic, oracle-pinnable, provably compliant by construction; it allocates a firm constant, and the locked pyramid ratios are untouched. A missing/oversized `cap_alloc` halts to zero rather than falling back to the permissive whole-account cap. A runtime joint check was rejected: the host deliberately does not track live position size (`crosstrade_payload` omits quantity on close for exactly that reason), so sizing a compliance-critical budget off that bookkeeping is the M8 class the fail-safe doctrine exists to prevent; it would also make qty order-dependent when both legs fire on the same 15m close. **Upgrade path:** when the host gains verified position truth, the split relaxes to a runtime headroom check — same re-add shape as the 2026-07-19 AM trigger. The original MYM 69 / MNQ 11 split (`f2_floors.json` re-pinned, originals retained under `pre_2026_07_22_whole_cap_per_leg`) was **released to 0/0** by operator ruling 2026-08-26 (Addendum 2026-09-01 below).

### Open B7 input — CLOSED 2026-07-24, measured benign

The WATCH-1 0.50× figures §6 cited had been computed under defective eval geometry ([`RESULTS.md`](../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md)); Addenda 2026-07-24 and 2026-07-28 measured them.

### Flat deadline corrected

**16:45 ET** regular (12:59 ET holiday-short), tightened from the 16:59 ET this ADR carried (owner: envelope §4 Tradeify row). The E1 target (16:00 ET), the Pine 15:45 force-flat and the operator 15:55 check all sit inside it, and the auto-flatten remains **non-fatal** — the property the 2026-07-19 Option-C addendum leans on. Read every "16:59" in the 07-19 addendum as **16:45**.

---

## Addendum — 2026-07-24: §6's WATCH-1 0.50× figures MEASURED under corrected geometry — open B7 input CLOSED benign

Operator directive 2026-07-24 ("proceed with the two unmeasured arms"); run [`CORRECTED_FULLPANEL.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md). **Corrected WATCH-1 0.50×, $100K basis, both discharge tiers:** full-panel bust **0.11%**, **H1 0.22%**, **H2 0.04%** — every partition passes the frozen floor. Against the defective-geometry figures (0.08% / 0.14%) the correction costs **+0.03pp full-panel / +0.08pp H1**, versus +2.10pp at 1.00× — a strongly non-linear barrier interaction that vindicates §5's no-down-scaling rule. The GO stands unchanged. Same-day sibling result (separate pre-registration, not this ADR's scope): two corrected-geometry Part A clearers at the 50K band ([`RESULTS.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md)).

## Addendum 2026-07-28 — the declared separable long pole is MEASURED and CLEARS

The one measurement Addendum 2026-07-24 left open on the deployed rung — the corrected-geometry 0.50× **bootstrap-95th**, declared a separable long pole and **not** a B7 gate — measured **1.20%** (pass-5th 95.5%) against the 3.0% ceiling (`Tradeify_Select_100K`, frozen rider primitives; reproduction controls matched the published full/H1/H2 pins), so every partition of the deployed configuration was measured under corrected geometry and passed. Evidence: [`RESULTS.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/eval_shape_diagnostics_2026-07-28/RESULTS.md) Part B · `rider_050x_report.json`.

**Scope discipline, unchanged.** This closed a *measurement*, not a gate: it did not touch B7's actual blockers (M1 `RESOLVED` + operator GO), the §4 falsifier (undischarged; scored at the $100K band at 1.00×), or any locked parameter. The same pass found corrected 1.00× bootstrap-95th **17.79%**, which strengthens rather than disturbs §5's no-downscaling rule and the choice of the 0.50× rung.

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
  (rail disposition, 2026-08-08; ruled 2026-08-07 by [S1](2026-08-07-loop-s1-environment-ratification.md)), which also governs the account and the M1 spine.
- **§2, §4, §5 and every prior Addendum are unedited** (Trap #12 — frozen bodies are never rewritten
  in place). This Addendum is the intercept, not a revision. *(Revision 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §6 shortened, §10 hooks replaced, Addenda 2026-07-18, 2026-07-22, 2026-07-24 and 2026-07-28 condensed, header FIXes in place; recorded here, not as a header line, so L1–L95 keep their cited line numbers. Pre-trim text at blob `3cc1081f6cbf34c57de708534efd5eb9172426bf` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`): [this file at `4121e84c`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-17-c1-rail-build-account-registration-go.md).)*
- The lifecycle axis: both legs remain `AUTHORIZED @ 1.00×`. **Venue-fit is not decay.**

**Scope of the de-scope, stated so it is not over-read:** its same-day Addendum narrows the bar to
*redeploying those two legs*. **Tradeify-shaped research is expressly not barred**, and Tradeify
remains 1 of the 4 firms in the frozen prop-portfolio §4 falsifier set.

---

## Addendum 2026-08-21 — §7 B6 cell is the 2026-07 build-order snapshot

**Does not amend §2 / §4 / §5.** Header clarification 2026-08-08 already records B6 PASSED 2026-07-20 for this build (operator-signed). The §7 table's B6 **PENDING** cell is the 2026-07-17 build-order snapshot and stays byte-unedited (Trap #12). Readers take this-build B6 status from the header, not from §7. A rebuilt or re-hosted signal path still needs its own dry-fire (same header: the principle re-arms). B7 stays PENDING behind STATE queue #2 (acceptable strategy on the ruled host).

Reads: this file header L9–19 + §7 B6 row @ `027a729` (2026-08-14).

---

## Addendum 2026-08-24 — test strategy is a qualifying strategy

**Does not amend §2 / §4 / §5.** The de-scope addendum’s line “Deploying any qualifying strategy makes it dischargeable again” is the owner; this records the operator’s 2026-08-24 instrument. A **test strategy** on the ruled host (evaluate-hook → B1 POST, `dry_run=true`, expected non-zero sizing) qualifies for M1 item 5 / B7 Stage 1. Dated 2026-08-24. Not a canned hand-POST. Not Striker redeploy. Not an arm. B7 Stage 2 stays behind M1 `RESOLVED` + a separate arm GO.

Owner: [M1 addendum](2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24). The 2026-08-21 sentence “B7 stays PENDING behind STATE queue #2 (acceptable strategy on the ruled host)” is stale for the Stage 1 limb — take `#2` from [`STATE.md`](../../STATE.md).

Reads: de-scope addendum “any qualifying strategy” @ `acc4f41` · M1 addendum 2026-08-24 (this session).

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
| 2026-08-21 | Addendum: §7 B6 **PENDING** cell is the 2026-07 build-order snapshot; this-build B6 status is the header PASSED record | Joshua (H3 GO) + Cursor |
| 2026-08-24 | Addendum: test strategy is a qualifying strategy for M1 item 5 / B7 Stage 1; dated 08-24; Stage 2 / arm unchanged | Joshua (ruling) + Cursor |
| 2026-09-01 | Addendum: reader-intercept -- Addendum 2026-07-22's 69/11 cap-alloc split was released to 0/0 by a later ADR (2026-08-26); this addendum was never updated to reflect it | Claude Code (ADR-corpus reconciliation sweep) |
| 2026-09-12 | Addendum + header intercept: `RUNBOOK.md` pointer re-home to the public `ARMING_PROCEDURE.md` and the private retrieval convention (TB-O1); no clause amended | Claude Code (recorder) |
| 2026-10-15 | History trim: §6 shortened, §10 hooks replaced, Addenda 2026-07-18/07-22/07-24/07-28 condensed; header FIXes (F2 ruled by S1; M1 `RESOLVED` 2026-09-14; `ACTIVE_FIRM` deleted). Prior text pinned at `4121e84c` (ADR decay audit; operator direction 2026-10-15) | Claude Code (recorder) |

---

## Addendum 2026-09-01 -- Reader-intercept: Addendum 2026-07-22's 69/11 cap-alloc split has been RELEASED to 0/0

**Does not amend §2 Decision, §4 Falsifier, or §5 Forbidden moves.** The Addendum 2026-07-22 "Fix (operator-approved)" section above describes a static MYM 69 / MNQ 11 account-aggregate cap allocation as the live sizing-host state. That allocation was **released to 0/0** by operator ruling 2026-08-26 ([`2026-08-26-striker-legmap-cap-release.md`](2026-08-26-striker-legmap-cap-release.md)) -- `LEG_MAP["dj30_mym"]["cap_alloc"]` and `LEG_MAP["nas100_mnq"]["cap_alloc"]` in `ops/c1_rail/c1_sizing_host_reference.py` now read `0`, freeing the full 80-micro account cap for a future leg's own allocation. Grounds (from that ADR, verified this session): both Striker legs have sent zero signals since the 2026-08-04 withdrawal, the rail stays disarmed, and the sizing host's existing fail-safe halts a zeroed leg to `qty_out=0` rather than falling back to the pre-2026-07-22 permissive per-leg cap (the 1.91x over-cap defect this addendum's split was built to prevent does not return).

Recorded here per Rule 14 (corrections land where the error is read, `docs/operational_rules.md`) -- a reader landing on the 2026-07-22 addendum without independently finding the 2026-08-26 ADR would believe 69/11 is still the live split. The 2026-07-22 addendum's engineering reasoning (account-aggregate cap math, the defect it fixed, the 68+11=79≤80 arithmetic) remains an accurate historical record of 2026-07-22→2026-08-26 behavior and stays byte-unedited (Trap #12); only its "this is live today" reading is corrected. No candidate is admitted, sized, or authorized by this addendum -- the freed headroom is a separate future admission decision under the third-leg target spec's own screens, per the release ADR's own §Boundary.

**Verification:**
```bash
grep -n '"cap_alloc": 0' ops/c1_rail/c1_sizing_host_reference.py
grep -n "RELEASED 2026-08-26" ops/c1_rail/c1_sizing_host_reference.py
grep -n "Status" docs/adr/2026-08-26-striker-legmap-cap-release.md | head -1
```

---

## Addendum 2026-09-12 -- `RUNBOOK.md` pointer re-home (TB-O1; no clause amended)

**Does not amend §2 Decision, §4 Falsifier, §5 Forbidden moves, §7, or any prior addendum.** The arm gate, the attended-only posture, the spend ceiling and the per-session GO stand exactly as written. **$0 / K=0.** Nothing arms.

`docs/notes/rail_build/RUNBOOK.md` is cited by this file at the header clarification (B6 PASSED, "RUNBOOK §B6"), §7 rows B3 ("B5d") and B6 ("B5e"), and the 2026-07-19 Option C addendum (the **5d** re-add trigger, the discharged "E1 pre-B7 decision", and two audit-hook `grep` lines). The file left the public tree under the [public-visibility ADR](2026-08-14-repo-public-visibility-transition.md)'s exclusion rule; every one of those links is dead on this tree **by design**, and the bodies stay byte-unedited (Trap #12; Addendum 2026-08-21 already fixes §7 as the 2026-07 snapshot). This addendum and the header intercept re-home the reader:

- **Public procedure:** [`docs/notes/rail_build/ARMING_PROCEDURE.md`](../notes/rail_build/ARMING_PROCEDURE.md) (Track B TB-O1) — arm/disarm/session steps, interlocks, `armed_until` discipline, stop conditions and recovery pointers, with source anchors. It carries no account value and authorizes nothing; the arm stays operator-only behind M1 `RESOLVED` **plus** a separate GO.
- **Private runbook:** retrieved per that file's §2 — archive pin `5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2` ([RUNBOOK.md at the pin](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/notes/rail_build/RUNBOOK.md)), or the `pre-prune-2026-08-08` blob `d523ee0d…` in the primary checkout's ignored private root. The 2026-07-19 addendum's two `grep … RUNBOOK.md` hooks run against that copy.
- **Unchanged:** the private crash-loop recovery procedure (availability attested in the [readiness record](../notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md) §A3).

Reads: this file @ `770413b` (sites located by `grep -n RUNBOOK`) · `deploy/c1_rail/README.md` @ `811df7c` ("Operating procedure lives in the private archive") · `.claude/skills/c1-rail/SKILL.md` @ `9c89dfa` (file map row "Runbook + B-gate history").

## Addendum — 2026-10-01: production data-feed costs are outside the $700 ceiling

**Source.** Joshua, in the coordinating session on 2026-10-01: "feed costs don't count toward the $700 ceiling". This answers decision D-Q1 of the H8 feed-preparation return (PR #583).

**Effect.** **Feed costs only** fall outside this ADR's $700 all-in ceiling (§2) and outside the projected spend that revert trigger (b) measures (§4). Feed costs means production data-feed subscription fees and exchange (CME) market-data licence fees. The ceiling continues to cover what it did before: the eval, the rail run-rate, and the drill costs ruled under F-4.

**Clarified by the operator on 2026-10-01, relayed by the merge-order session after Codex's review:** refundable **deposits and minimum balances stay under the cap** until the operator rules on them separately. For example, the A′ parked deposit remains capped. **Open operator decision:** whether refundable deposits or minimum balances needed for data access are exempt. *2026-10-03 (coordinator (3) batch 2b):* ruled; see the [D-Q5 addendum below](#addendum--2026-10-02-refundable-data-access-deposits-and-minimum-balances-exempt-up-to-500).

**Definition of "feed costs", operator ruling 2026-10-01 (structured question; decides D-Q6 and D-Q7 of the H8 questions draft, PR #583).** A feed cost is **any non-refundable charge whose purpose is receiving the market data**, and it is exempt. That includes:
- data-feed subscription fees;
- exchange (CME) licence fees;
- recurring API or data-access fees required to receive the data, for example a broker API add-on or a monthly API fee;
- one-time, non-refundable setup, activation or onboarding charges for the feed.

Refundable deposits and minimum balances **stay under the cap**, as clarified above. *2026-10-03 (coordinator (3) batch 2b):* except as exempted by the [D-Q5 addendum below](#addendum--2026-10-02-refundable-data-access-deposits-and-minimum-balances-exempt-up-to-500).

**Still counted under the cap:** any charge whose purpose is not receiving the market data. That includes account, inactivity, platform or trading fees that are not required for data access, and the eval and rail costs.

**Unchanged.** Feed signup and spend still require D-feed (a)+(b) and CP-7. Every feed purchase stays an operator act. Feed costs are still recorded, outside the ceiling tally, wherever their owner keeps them.

## Addendum — 2026-10-02: production qualification-host spend is outside the $700 ceiling, under its own $500 cap

**Source.** Operator ruling 2026-10-02 (sitting 2), Q-8 (Joshua, "all recommended"). The cap was set by Joshua's follow-up at 2026-10-03T03:16Z ("go with your best recommendations").

**Effect.** Production qualification-host spend does not count toward this ADR's $700 ceiling (§2). It is subject to its own separate cap of **$500**, revisited at CP-8. The $700 continues to cover the eval, the rail run-rate and F-4 drill costs. Host provisioning and any spend stay at CP-8.

## Addendum — 2026-10-02: refundable data-access deposits and minimum balances, exempt up to $500

**Source.** Operator ruling 2026-10-02 (sitting 2), D-Q5 (Joshua, "all recommended"); the amount was set by Joshua's follow-up at 2026-10-03T03:16Z ("go with your best recommendations"). It answers the open decision in the 2026-10-01 addendum.

**Effect.** Refundable deposits and minimum balances required for data access are exempt from the $700 ceiling, up to **$500**. Anything above $500 stays under the cap. This exemption is separate from the qualification-host cap above. Feed signup and spend still require D-feed (a)+(b) and CP-7.
