---
name: c1-rail
description: Use this skill for ANY task touching the c1 live execution rail — ruled signal host (Python daemon, S2) → listener (Fly.io) → CrossTrade → Tradovate on the Tradeify Select 100K eval; Pine/TV remains research/export. Triggers on c1, CrossTrade, Tradovate, Tradeify, rail listener, webhook, sizing host, signal daemon, B6/B7, arming, dry_run, M1 monitoring, telemetry/EventLedger, fly deploy, alert payload, or execution-quality (fills/exits) questions on the MYM/MNQ legs. BUILT and DISARMED at the live incumbent eval (S1), with no strategy deployed (locked Striker book barred 2026-08-04) — this skill's job is routing + safety invariants + where the canonical numbers live, never a substitute for reading them. Hand off to prop-firm-challenge for firm rules/MC/dd_protection mechanics, pinescript-v6 for the Pine venue editions.
---

# c1 Rail — live execution path (Option C)

**Status 2026-08-08.** Rail is BUILT, account-registered and **DISARMED** (`dry_run=true`), pointed at the incumbent `Tradeify_Select_100K` eval ([`S1 ADR`](../../../docs/adr/2026-08-07-loop-s1-environment-ratification.md)). No strategy deployed; withdrawn Striker legs stay barred. **Live signal host for new strategies = Python-native** ([`S2 ADR`](../../../docs/adr/2026-08-07-loop-s2-signal-host-fork.md)); [S2b](../../../docs/spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) Accepted · [build ADR](../../../docs/adr/2026-08-08-s2b-signal-daemon-build.md) Accepted · build GO 2026-08-08 — daemon lands warm with `emit_enabled=false`. Everything below describes the built path, not an operating one.

The built (currently disarmed) execution path: **ruled signal host** (Python daemon POSTing B1 JSON — **built**, `emit_enabled=false` until strategy GO) → `ops/c1_rail/c1_rail_http_server.py` (Fly.io listener app, thin adapter; contract origin-agnostic) → `ops/c1_rail/c1_rail_listener.py` (`handle_signal`) → `C1SizingHostReference` sizing decision → `ops/c1_rail/crosstrade_payload.py` → CrossTrade webhook → Tradovate (Tradeify Select 100K eval). Historical TV-alert→same-listener path remains on the record as the pre-S2 branch. **Option C (2026-07-18): the Python sizing reference is the listener's sizing host when armed — there is no NT8 hop; the NinjaScript port is a dormant fallback that was never built. No book is deployed.**

This skill is pointer-first by design. **Never restate rail constants (quantities, ceilings, multipliers, thresholds) from this file or from memory — read the owning source.** If this skill and a canonical doc disagree, the doc wins; flag the skew.

## Safety invariants (violating any of these is a stop-and-surface, never a judgment call)

1. **Disarmed by default.** `dry_run=true` is the standing state; `dry_run` defaults True if the config key is absent (never fail open to live). DRY_RUN computes the would-be payload for audit but never calls the sender.
2. **Arming is an operator GO.** The next `dry_run=false` entry/add send (B7-REFIRE Stage 2) is gated on **M1 monitoring `RESOLVED`** (all six drills evidenced; items still owed = `dry_run_strategy_signal_event_id` at non-zero size from the **ruled Python host** + `operator_signoff`) **plus** a separate operator GO — architecture alone does not arm. Owner: [`M1 ADR`](../../../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) (item-5 origin: [`S2 ADR`](../../../docs/adr/2026-08-07-loop-s2-signal-host-fork.md)). The M1 acceptance JSON lives in the private archive, not this public tree. **Trigger amended 2026-07-31b (operator-ratified): the gate's object is the ARM, not the send** — `dry_run=false` may not be set while M1 is not `RESOLVED`. **Third bar (2026-08-04): both Striker legs WITHDRAWN; redeploy barred.** Environment = incumbent eval ([`S1`](../../../docs/adr/2026-08-07-loop-s1-environment-ratification.md)); no deployed strategy — **there is nothing to arm.**

   ### Agent-session authority (operator grant 2026-08-02)

   Supersedes the prior blanket *"never an agent action"* / *"do not arm/disarm/deploy from an agent session"*.

   | Action | Agent may run? | Conditions |
   |---|---|---|
   | `fly deploy` (listener **or** signal-daemon app) | **YES** | All six deploy pre-conditions below, **scoped per app**. |
   | `--disarm` | **YES** | Only once flatness is **broker-verified** — `dry_run=true` blocks *everything including exits*, so disarming over an open position **orphans** it. Flat first, then disarm. |
   | `--status`, pre-flight reads, boot-line verification | **YES** | Read-only; always permitted. |
   | `--arm` (`dry_run=false`) | **NO — declined by the agent, and this is NOT a permissions gap** | See below. |

   **Why `--arm` stays with the operator.** Setting `dry_run=false` on a live broker account means the next qualifying strategy signal routes a **real futures order with no further human action**. An agent treats that as equivalent to placing the order itself, and declines it under any authorization — this is a standing boundary, not an unlifted restriction, so **do not re-litigate it as stale policy or route around it** (e.g. by hand-editing `/data/c1_rail_config.json`, which is the same act with the audit trail removed). What an agent MAY do: draft the exact command, run `--status`, complete the §0 pre-flight, and verify the post-restart boot line. The operator runs the one command.

   **Two Fly apps (S2b):** (1) **listener** — `deploy/c1_rail/` (sizing + DD state); (2) **signal daemon** — `deploy/c1_signal_daemon/` (own machine/volume; never shares listener `peak_equity`). Deploy pre-conditions apply **per app**; items 1/4/5/6 are listener-specific until the daemon has its own arm/M1 surface.

   **Deploy pre-conditions** — each earned by a dated incident; all six, in order (**per app**):
   1. **Verify `dry_run=true` on the listener host first** (listener deploys). A deploy restarts the machine, which re-reads the volume config; if it still says `dry_run=false`, the rail **reboots armed** (2026-07-27 class).
   2. **Deploy from `main`**, repo root, documented command only (`fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile` for the listener; daemon config path lands with its build).
   3. **Re-trace the import closure** if `ops/` or `core/` gained an import. A module in no COPY line yields a **GREEN build** that dies at CMD (2026-07-31, `core/historical_challenge.py`). Do not trust a green build.
   4. **Refresh `fixture_hashes` from in-container hashes in the same motion** (listener / M1 pin) — a deploy that moves pinned files without re-pinning breaks the M1 acceptance record.
   5. **Verify the boot line** (`dry_run=` / `armed_until=`) **and health** after (listener). Judge by the command's own printed output, not its exit code (Windows `fly ssh console -C` exits 1 after correct output).
   6. **Know the crash-loop recovery path before starting** — [`deploy/c1_rail/README.md`](../../../deploy/c1_rail/README.md) + GO ADR (public); private RUNBOOK is not on this tree. An expired `armed_until` makes the host refuse to boot, and `fly ssh` needs a booted machine, so a restart cannot fix it.
3. **Fail-safe sizing.** ANY unreadable/malformed state input (missing file, bad JSON, unlisted leg key, unknown tier) halts entry/add sizing for that signal — qty 0, no submit. A halt or floored decision NEVER reaches the sender.
4. **Transport honesty (M1).** An HTTP response is `accepted`, never execution-verified; a timeout/reset after bytes may have left is `unknown` — blocks further risk-add and is never auto-retried. Exit/flat are best-effort.
5. **CrossTrade's Alert History is the source of truth for whether a signal validated** — not the rail's own `sent=True http_status=200` log (the B6 `secret_key` defect was invisible to the rail log).
6. **Attended-only, spend ceiling per the GO ADR** (`docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` — read it for the ceiling; do not quote from memory).
7. **Sizing law lives in `dd_protection`/lifecycle, not here:** `r_eff = BASE_RISK × DD_SCALE × lifecycle`, integer-qty flooring, proven against the committed F2 oracle `lab/analysis/c1/q_rail_1_2026-07/f2_floors.json`. WATCH haircuts on the pyramided legs realize at the **account-multiplier layer**, never via TV risk%-input scaling (Q-PYRPARITY-1).
8. **Venue facts were corrected 2026-07-22 — read the ADRs, never re-derive from an older brief, and never from this line.** Per invariant 12 above, the numbers that used to sit here (cap allocation, flat deadline, the WATCH-1 0.50× panel/half figures, the bootstrap-95th vs ceiling) were **deleted 2026-08-08** — this file forbids restating rail constants and was violating its own rule. Read them from their owners: `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` and the GO ADR's Addenda **2026-07-22** and **2026-07-24**. What survives here is only the *shape* a reader needs to route correctly: the contract cap is **account-aggregate and allocated per leg** (an earlier read gave each leg the full amount — a real, measured over-count); the hedging rule clears **by construction** (c1 is long-only at every layer); the same pass **withdrew the prop-portfolio §4 discharge**, and §4 **remains undischarged** (a 07-24 band re-score found 50K-tier clearers under a regime-fragile caveat, which does **not** discharge the $100K-scored gate). **2026-08-04:** both Striker legs were WITHDRAWN from the c1 eval deployment — no deployed rung, no forthcoming B7 at this venue; the allocation and both **Striker** symbols stay barred for redeploy (S1 kept the rail at the incumbent). MYM1!/MNQ1! **research occupancy** was released for new non-Striker work ([occupancy ADR](../../../docs/adr/2026-08-12-msl-mym-occupancy-release.md)) — that is not a Striker redeploy. ⚠ **Every bust/DD figure in those owners is an EOD-clock LOWER BOUND pending W1 RESULTS** ([`W1 ADR`](../../../docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md)).
9. **Alerts are JSON-only** on both venue editions — informational `alert()` calls shadowed the JSON payloads and caused the 2026-07-21 B7 miss (fixed; editions re-pinned in `core/strategies/PORT_MANIFEST.sha256`). Any Pine-edition change re-runs `pine_check` + re-pins in the same motion.
10. **Always-on hosting (Rule 15 / W6):** listener + signal daemon (built, `emit_enabled=false`) run on Fly / always-on host; desktop is console-only for those processes — not the runtime. Does not ban route-LOCAL interactive work. [`operational_rules.md` Rule 15](../../../docs/operational_rules.md) · [`W6 ADR`](../../../docs/adr/2026-08-07-w6-rail-infra-closures.md). Prefer `c1_rail_arm.py` / `write_volume_config.py` / `export_session_evidence.py` over hand-editing volume JSON.

## File map (read these, in this order, for any rail change)

| Surface | File | Note |
|---|---|---|
| Runbook + B-gate history | private archive (`docs/notes/rail_build/` excluded from the public seed) | B1–B7 record; public owners are the GO ADR + [`deploy/c1_rail/README.md`](../../../deploy/c1_rail/README.md) |
| Decision routing | `ops/c1_rail/c1_rail_listener.py` | `handle_signal` + leg_id→symbol map; pure function, tested |
| HTTP adapter | `ops/c1_rail/c1_rail_http_server.py` | listener app; origin-agnostic `POST /c1/<path_token>`; deliberately untested |
| Sizing host | `ops/c1_rail/c1_sizing_host_reference.py` | Listener's sizing reference when armed (Option C); no book is deployed; 29-test suite vs the F2 oracle |
| Signal daemon | `ops/c1_signal_daemon/` · [S2b](../../../docs/spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) · [build ADR](../../../docs/adr/2026-08-08-s2b-signal-daemon-build.md) | second Fly app (`deploy/c1_signal_daemon/`); B1 POST client; emit disabled until strategy GO |
| Order payload + sender | `ops/c1_rail/crosstrade_payload.py` | CrossTrade webhook builder; `destination=tradovate`; sender is DI'd |
| M1 telemetry | `ops/c1_rail/c1_rail_telemetry.py` | EventLedger; pre-send decision events; uses `core/lib/file_lock.py` |
| Stage 2b slippage | `ops/c1_rail/c1_rail_slippage.py` | Read-only per-fill join (`parsed.close` ↔ `fill_price`); cohort-split; panel-baseline compare. Operator CLI — not on the request path. |
| Deploy (listener) | `deploy/c1_rail/` + root `.dockerignore` | Fly.io listener image; single machine **per app**; daemon is a separate app (S2b) — never collapse DD volumes |
| Spec | `docs/spec/c1_nt8_sizing_host_impl.md` | frozen sizing-host spec + Option C addendum |
| Firm/account | `core/firm_rules.py` (`Tradeify_Select_100K` explicit tier key; `ACTIVE_FIRM` deleted Phase 4) | via prop-firm-challenge skill |

## Standing context

- Two legs: Striker DJ30/**MYM** + Striker NAS100/**MNQ** venue editions — **both withdrawn from the c1 eval deployment 2026-08-04** (ADR `2026-08-04-tradeify-venue-descope-eval-included.md`). Deliberately unchanged by that ADR: lifecycle stays `AUTHORIZED · MECHANISM @ 1.00×` (venue-fit is not decay), and `LEG_MAP` / Pine / allocations are untouched.
- Instrument ledgers (rule 10 read-before-touch): `ops/instruments/MYM.md` + `ops/instruments/MNQ.md` — the **MICRO** cards own c1 leg state and carry the dated 2026-08-04 `⚠ NO LONGER A LIVE c1 LEG — withdrawn from deployment` status. Parents `ops/instruments/YM.md` / `ops/instruments/NQ.md` are secondary (shared venue geometry only) and their status lines are **NOT** corrected — never read c1 leg state from them.
- ~~Execution-quality research (better fills/exits) is the standing research interest on this rail~~ — **SUSPENDED 2026-08-04, not re-scoped and not closed: it has no data source.** No strategy-signal-originated fill ever occurred and the discharge path is gone (ADR 2026-08-04 §6; CLAUDE.md §Purpose). Do not open a fills/exits workstream and do not route a depth/microstructure pull from this skill until fork F3 rules.

## Verification commands

**Suite / pins (repo-side — these run from a clean checkout; they do not report armed/disarmed):**

```bash
pytest tests/ops/ tests/rail_crosstrade/ -q          # sizing host + payload + arming suites
python scripts/check_pine_manifest.py                # venue-edition pins; exit 0 (WARN EXTRA for unpinned candidates/ is OK)
```

**Armed / disarmed state — host read only.** The live config is `/data/c1_rail_config.json` on the Fly volume (`DEFAULT_CONFIG_PATH` in `ops/c1_rail/c1_rail_arm.py`). There is no `ops/data/c1_rail_config.json` (deleted) in the tree. A local grep, a gitignored root `c1_rail_config.json`, or the committed `.example.json` files do **not** establish armed/disarmed state — only a host read does. Confirm before/after any session that touched the rail. (Protects the 2026-07-27 failure class: restart re-reads the volume file; an unedited `dry_run:false` reboots armed. Owner: GO ADR + `deploy/c1_rail/README.md`; `armed_until` design.)

```bash
# In-container (secret-free status reader):
#   fly ssh console -a c1-rail
#   python ops/c1_rail/c1_rail_arm.py --status
# One-shot (same reader). PowerShell — `&` call operator:
& fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
# Git-Bash — MSYS rewrites a `/data/...` remote arg; disable that when the -C string contains a volume path:
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
# Expect dry_run=True (armed_until absent/cleared). Windows: fly ssh console -C may exit 1 with
# "Error: The handle is invalid." AFTER printing correct output — judge by the command's own print
# (Windows fly ssh console -C notes, 2026-07-27).
# Agent authority (2026-08-02 grant): deploy YES (six pre-conditions), disarm YES (flat-verified
# first — disarm blocks exits and orphans an open position), status/read-only YES, ARM NO.
# See invariant 2 §Agent-session authority. `--arm` is operator-run, always.
```

**Repo-side path asserts (do NOT establish armed/disarmed — only that the live path is host-side and not checked in):**

```bash
git ls-files | grep c1_rail_config                   # expect only the two .example.json files
grep -n "DEFAULT_CONFIG_PATH" ops/c1_rail/c1_rail_arm.py     # expect /data/c1_rail_config.json
```

## Hand-offs

- Firm rules / MC / dd_protection mechanics → `prop-firm-challenge`
- Pine venue-edition code → `pinescript-v6`
- New data pulls for execution research → `databento-data` (mandatory cost dry-run)
- Any handoff brief claiming rail state → `handoff-verify` first
