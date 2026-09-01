# ADR 2026-08-07 — Loop S2: signal-host fork (Python-native)

**Status:** `Accepted` — implements [SPEC S2](../spec/2026-08-07-loop-s2-signal-host-fork-spec.md); plan default Python-native + operator plan-execution GO 2026-08-07
**Decision date:** 2026-08-07
**Authors:** Joshua (plan GO) + Cursor (drafter)
**Supersedes:** `2026-07-22-c1-venue-native-monitoring-maturity.md` in part — §4 item 5 **signal-origin definition only** (TradingView-only → ruled host). Item 5 itself (real strategy signal, expected sizing, `dry_run` Stage-1 shape), the decline of deletion (Addendum 2026-07-31), and the bar on **silent** redefinition **stand**; this ADR is the **express** supersession that Addendum required.
**Supersedes:** `2026-07-10-databento-research-stack.md` in part - the §2 rail-verdict clause only (TradingView/NinjaTrader8/Rithmic/Bulenox chain); that ADR's §4 falsifier never fired, the rail changed via this ADR's mechanism instead.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [SPEC S2](../spec/2026-08-07-loop-s2-signal-host-fork-spec.md) · [SPEC S2b](../spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) · [S1 ADR](2026-08-07-loop-s1-environment-ratification.md) · [M1 ADR](2026-07-22-c1-venue-native-monitoring-maturity.md) · [rail GO ADR](2026-07-17-c1-rail-build-account-registration-go.md) · [loop index](../spec/2026-08-07-loop-spec-index.md) · [TV backtest-egress automation ADR](2026-06-23-tv-backtest-egress-automation.md) (added 2026-08-29, adr-decay-audit discharge — this ADR makes Pine/TV the research/export surface rather than the live signal origin for new strategies; see that ADR's 2026-08-29 addendum for the open forward question this raises) · [`2026-07-10-databento-research-stack.md`](2026-07-10-databento-research-stack.md) (added 2026-08-29, adr-decay-audit discharge — superseded in part by this ADR: its §2 rail-verdict clause named TradingView as the live signal origin, which this ADR replaces with the ruled Python-native host. See that ADR's 2026-08-29 addendum)
**Layer:** signal-host / M1 origin definition only. **$0 / K=0** — this ADR authorizes no daemon build, no arming, no agent trade. Downstream: S2b Accepted + [build ADR](2026-08-08-s2b-signal-daemon-build.md) Accepted + operator build GO 2026-08-08 — daemon warm (`emit_enabled=false`); strategy emit + M1 item 5 still owed.

---

## §0 — Rule 0 reads (verified 2026-08-07)

| Source | Anchor | What it pins |
|---|---|---|
| [SPEC S2](../spec/2026-08-07-loop-s2-signal-host-fork-spec.md) | `aee4137` | Fork: Python daemon vs Pine/TV; M1 item-5 origin must be discharged or expressly superseded; no build before S2b |
| `ops/c1_rail/c1_rail_http_server.py` | `2345095` | `POST /c1/<path_token>` + JSON parse; **origin-agnostic** (no TV/sender identity gate) — cheap falsifier PASS 2026-08-07 |
| `ops/c1_rail/c1_rail_listener.py` · `crosstrade_payload.py` | `2345095` | B1 → `handle_signal` → sizing → CrossTrade; same contract regardless of POST origin |
| [M1 ADR Addendum 2026-07-31](2026-07-22-c1-venue-native-monitoring-maturity.md) | `8483743` | Item 5 stands; **silent** redefinition forbidden; deletion DECLINED |
| [S1 ADR](2026-08-07-loop-s1-environment-ratification.md) | working tree (Accept same day) | Environment = incumbent eval; rail warm/disarmed — fork is not moot |

---

## §1 — Context

S1 ruled the environment (incumbent `Tradeify_Select_100K` eval; rail warm/disarmed). New strategies still need a live signal origin. The listener contract is already origin-agnostic: any client that POSTs valid B1 JSON to `POST /c1/<path_token>` exercises the same path TV alerts use today. Keeping TV as the sole live emitter re-imports the port-parity / alert-snapshot defect class; a Python daemon posting the same payload removes that class from the live chain.

M1 §4 item 5 still requires a real strategy signal with expected sizing at `dry_run=true`. Its historical wording and operative (“only item requiring a real **TradingView** strategy signal”; “Redefinition stays forbidden”) barred *silent* redefinition — not an express ADR supersession of the origin limb.

---

## §2 — Decision

**Live signal host for new strategies: Python-native.** A Python signal daemon (specified in [S2b](../spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md), not built by this ADR) evaluates strategy logic against a live bar feed and POSTs B1 JSON to the existing listener. Pine/TradingView remains the **research/export** surface. TV login/actuation automation stays **absolutely prohibited** (both branches of the fork).

**Costs recorded (accepted with the ruling):**
- Live bar feed (availability, cost, and fail-closed behavior — detail in S2b).
- Daemon uptime + heartbeat (operator-visible liveness).
- Kill-on-feed-loss (fail-closed: no signals while the feed is unhealthy).

**M1 item 5 — EXPRESS supersession of signal-origin definition:** discharge path is a **real strategy signal from the ruled host** — i.e. a Python-daemon B1 POST that produces a structured dry-run decision with **expected (non-zero) sizing** — not a TradingView-only origin. Item 5’s other limbs stand: real strategy signal (not canned), expected sizing, Stage-1 `dry_run=true`, no silent redefinition, `--allow-live` must not write `dry_run_strategy_signal_event_id`. Historical TV-origin attempts remain on the record; they do not redefine the forward gate.

**Unchanged:** S1 environment; rail warm/disarmed; M1 arm-gate; attended-only; Striker redeploy bar; locked sizing constants.

**Effective:** immediately upon Accept (2026-08-07).
**Spend:** $0 / K=0 / no daemon build / no arming / no agent trade.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep Pine/TV as live signal host | Re-keeps alert-snapshot / port-parity class on the live path; plan default was Python-native |
| Discharge item 5 via TV before cutover | No strategy deployed at this venue; TV path is the defect class being exited; express supersession is the SPEC S2-authorized route |
| Build the daemon in this ADR | Boundary: no build before S2b; this ADR rules the fork only |
| Collapse daemon into the listener Fly app | Violates DD-locality / single-machine-per-app invariant — S2b keeps a **second** app |

---

## §4 — Falsifier (revert trigger)

**H:** After Accept, new-strategy live signals are defined to originate from the Python-native host; M1 item 5’s origin limb reads “ruled host,” not TradingView-only; no daemon is built under this ADR alone.

**Revert / FALSIFIED (any limb):**
1. A later artifact treats TV as the **required** live origin for new strategies without a superseding ADR → supersede.
2. Item 5 is silently re-read to accept canned payloads, live-armed evidence, or zero-qty floors as discharge → DEAD-list; Addendum 2026-07-31 bar stands.
3. Daemon code lands without an Accepted S2b + build GO → unauthorized build; tear back.

**Trigger check schedule:** S2b Accept / first daemon build GO, or 2026-08-08 programme audit — confirm origin definition + no unauthorized build.

---

## §5 — Forbidden moves

- Building the daemon under this ADR alone (S2b + separate build GO required).
- TV login/actuation automation.
- Arming the rail or setting `dry_run=false`.
- Treating this ADR as M1 `RESOLVED` or fabricating `dry_run_strategy_signal_event_id`.
- Collapsing the future daemon into the listener app’s volume/DD state.
- Redeploying withdrawn Striker legs.

---

## §6 — Consequences

- Unblocks S2b (daemon minimal spec) and, after S2b + build GO, the Python signal path.
- M1 item 5 remains **owed**; discharge definition re-pointed (JSON note + M1 Addendum 2026-08-07).
- CLAUDE.md / c1-rail skill / RUNBOOK gain pointer or scoping notes (S7 S2-ADR + S2b sections).
- Pine/TV stays research/export; historical B7 TV checklists scoped as TV-branch-only.

---

## §7 — Propagation (S7 S2-ADR + S2b sections)

Discharged in the same change-set as Accept — see [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md) §S2-ADR / §S2b.
