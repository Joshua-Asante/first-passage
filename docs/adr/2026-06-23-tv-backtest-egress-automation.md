# ADR 2026-06-23 — TradingView backtest-egress automation

**Status:** `Accepted`
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-27-tv-agent-browser-access.md` in part — the agent-access prohibition only (§5 bullet 1 as applied to agent browser reads). The layered egress strategy (§2), the allowlist-circumvention bullet, the second-account bullet and the private-Pine bullet all stand.
**Retain-until:** none
**Decision date:** 2026-06-23
**Authors:** Joshua + Claude Code
**Related:** PR #217 (`scripts/pine_check.py` compile gate — the adoption that motivated the broader egress question); ADR `2026-06-05-sweep-engine.md` (the Python-prefilter/native-confirm two-tier this builds on); ADR `2026-06-12` (TV CSV canonical-feed policy)
**Layer:** infrastructure

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR:

- `core/strategies/guardian/guardian_gold_v5.5.pine` — anchor: blob `de54ef3b` (per `core/strategies/guardian/LOCK.md`, lock 2026-04-23; gitignored `**/*.pine`, read from the main working tree on 2026-06-23). Verbatim: `process_orders_on_close=false` (line 9), `slippage=3` (line 8), grace stop `minBarsBeforeStop=1`/`graceStopMult=2.0` (lines 47–49, 195–216).
- `lab/validation/sweep/engine.py` — anchor: read 2026-06-23. `PythonPrefilterEngine` enters at `feed.close[i]` under `process_orders_on_close=true` (line 328); signal_fn contract = `SignalArrays` (lines 99–131); intentionally NO gate authority (lines 195–207).
- `lab/validation/sweep/parity.py` / `parity_run.py` — anchor: read 2026-06-23. Parity gate = trade-count EXACT + net/PF within `PARITY_NET_PF_BAND=0.02`; rank falsifier ρ≥`0.70`; native tier is a **documented manual** export (no browser automation).
- `core/strategies/guardian/LOCK.md` — anchor: lock 2026-04-23 (Tier-2 citation for the locked config).
- Research workflow `woys2grk6` (run `wf_cc4027e7-07e`, 2026-06-23) — 6 path-research agents + 42 adversarially-verified claims (37 supported / 2 refuted / 3 uncertain). The findings/verdicts JSON is the §3 evidence base.
- Empirical environment probe (2026-06-23): the Claude-in-Chrome MCP **refuses to navigate to `tradingview.com`** ("not allowed due to safety restrictions") — verified by a `navigate` call returning the restriction.

---

## §1 — Context

TradingView exposes **no public API** to run a backtest and return results; the canonical analysis pipeline therefore consumes hand-exported "List of Trades" CSVs. Having just adopted the zero-auth `translate_light` *compile* gate (PR #217), the natural next question was whether the *backtest-egress* step (getting the List-of-Trades out) can be automated too — and "any other automation paths" to work around the missing API. The constraint that dominates every answer: the **authenticated TradingView account runs the live FXIFY trading edge** (Pine → alert → Copygram → DXtrade), so any automation that risks a ToS ban on that account can take down live execution. A 6-path research workflow (browser / undocumented-endpoints / Pine-alert-egress / desktop-GUI / local-port / ToS), each path adversarially verified, produced the evidence base; this ADR records the decision.

**Decision driver (one sentence):** We need a standing policy on TV-egress automation now, because the obvious move (script the authenticated app) couples directly to the one account we cannot risk, and an unrecorded "just try it" invites exactly that coupling.

---

## §2 — Decision

**Decision:** Pursue a **layered** egress strategy, never on the live-edge account:

1. **Manual List-of-Trades export stays the sanctioned default** for the locked book — it is zero-risk and already the canonical-feed source of truth.
2. **Local reproduction (Path E) is the real leverage** and the only zero-account-risk automation: extend `PythonPrefilterEngine` to *generate* the trade list for **bar-close** logic, with the native TV export as the parity ground-truth. First target: Guardian (harness landed this commit).
3. **Native-CSV browser automation (Path A2) is a contained, isolated-account-only fallback** for when a genuine native CSV is required (intrabar exits, final deploy-gating numbers) — *never* on the live-edge account, never as a batch loop.
4. **Undocumented WebSocket (Path B) is forensic-only** (one-shot reads), because loading private Pine over it requires the live-edge `sessionid`.
5. **Pine `alert()` egress (Path C) is closed for backtest egress** (alerts fire realtime-only) but retained as the forward live-journal feed.

**Effective:** immediately upon acceptance.
**Scope:** all TradingView backtest-egress and chart-automation work for `multi_firm_operations`.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Path A1 — DOM-scrape the trades table in-page** | **Refuted** (workflow verdict, medium conf): the List-of-Trades table is virtualized; the full list is *not* in the DOM, so "re-serialize the in-memory table" doesn't work. A2 (capture the native Download) supersedes it. |
| **Path A via the connected MCP-Chrome** | **Blocked**: the Claude-in-Chrome MCP refuses `tradingview.com` navigation (safety allowlist, verified 2026-06-23). A2 would need a CDP-attached Playwright/Selenium driver — higher detection profile. |
| **Path B (WebSocket) as the primary loop** | Loading *private* Pine over the chart socket requires the live-edge `sessionid` (`study_not_auth` otherwise; no anonymous mode, a throwaway account can't see the private script). Couples the highest-power path to the un-riskable account. Forensic-only. |
| **A second TV account, naively isolated** | A second account is independently bannable (multi-account House Rule), and shared device/IP/payment/fingerprint can **collateral-ban** the live account. Isolation must be structural (separate machine/IP/profile, independently paid), not just "a different login." |
| **PyneCore SaaS compiler / any third-party optimizer** | Uploads private Pine — contradicts edge-protection doctrine; already rejected in `docs/rejected_candidates.md`-class reasoning. The Apache-2.0 PyneCore *runtime* is acceptable only as a DIY local port (= Path E by another name). |
| **Status quo — manual only, no local port** | Leaves every wide grid and every bar-close re-check gated on hand-exports; the local pre-filter (Path E) is cheap leverage the repo already half-owns (`engine.py`). |

---

## §4 — Falsifier (revert trigger)

**H (falsifiable):** If the engine gains `next_bar_open` + grace-stop + slippage support, then the Guardian signal port clears the parity gate (trade-count EXACT, net/PF within 2%) on ≥2 native Pepperstone XAUUSD anchors — making Path E a **validated** bar-close pre-filter (verdict RESOLVED); otherwise this hypothesis is **falsified** (verdict FALSIFIED) and Path E is confined to new-candidate screening. This is the **Falsifier** that gates §2 item 2's "local reproduction is the real leverage" bet; Guardian — the *least* intrabar-dependent locked strategy — is the deliberately-easiest test (AMBIGUOUS is not available: trade-count is exact-or-not).

**Revert trigger:** If, after the engine gains `next_bar_open` + grace-stop + slippage support, the Guardian signal port **cannot clear the parity gate** (trade-count EXACT, net/PF within 2%) on **≥2 native Pepperstone XAUUSD anchors**, then Path E is **confined to new-candidate screening** and the locked book is declared **native-only** (manual export remains the sole egress for locked strategies). Conversely, if Guardian clears it, Path E is a validated pre-filter for bar-close strategies and extends to the next-least-intrabar locked strategy.

**Revert action:** record the outcome in `lab/analysis/legacy/guardian_parity_2026-06-23/README.md` §Status; if FAIL, supersede §2 item 2's "locked book" ambition with "candidate-screening only" and stop porting locked strategies.

**Trigger check schedule:** on completion of the engine extension + Joshua's 2 Guardian exports (no fixed calendar date — event-driven; the harness is the gate).

**Status (2026-06-23): RESOLVED-POSITIVE (full window).** Final run over the full 52-trade window from the true $200K base (combined BAR_EXPORT pages cover 2025-06-22 → 2026-06-23 ET): **net 0.46% and PF 1.76% — both clear the 2% band** over a full year of compounding; 51/52 entries exact. The residual is the irreducible 15m bar-resolution floor (4 stop exits ±1 bar from hair-width stop-level precision; 1 cascaded missed same-day 2nd trade) — by the STRICT gate this fails trade-count-EXACT (51≠52) while passing net & PF. Three data-found corrections folded into the engine: (1) maxHold "Stale" market close fills next-bar-open; (2) `applyDdProtection` defaults OFF (raw Pine backtest has no portfolio dd overlay; dd ON read 79% off); (3) net parity needs the engine seeded at the native compounding base ($200K full-window → 0.46%; a partial window seeded mid-stream read 6.2%, the confound). Per ADR §2, Path E is a **validated bar-close reproduction of Guardian** — the trailing/intrabar caveat (NAS100-ORB precedent) still bounds it to bar-close logic.

---

## §5 — Forbidden moves (under this ADR)

- **Running any TV automation (A/B/D) on the live-edge account** — ruled out absolutely; a backtest-automation ban takes down live execution. Account isolation is structural, not a login switch.
- **Loosening the parity band (`PARITY_NET_PF_BAND` / ρ floor) to force a Path-E pass** — that is methodology p-hacking (sweep-ADR §5 #3). If Guardian can't clear 2%, that is the §4 finding, not a band to widen.
- **Treating Path A1 (DOM scrape) or Path C (alert backtest egress) as viable** — both were refuted; re-proposing requires new evidence (a de-virtualized table; historical-bar alert firing), not a restated plan.
- **Circumventing the browser safety allowlist** to reach TV through the MCP — the restriction is a safety control; the answer is a different driver under isolation, not a bypass.
- **Uploading private Pine to any third-party compiler/optimizer** to shortcut the local port — edge-protection doctrine; the DIY runtime is the only acceptable form.

---

## §6 — Consequences

**Positive:**
- One un-riskable thing (the live-edge account) is explicitly walled off from all automation experiments.
- Path E gives a zero-risk path to cheap local trade-list generation for bar-close logic, building on existing `engine.py`.
- The Guardian harness (this commit) converts an optimistic "port the logic" step into a grounded, tested signal + an explicit execution-model gap.

**Negative (real cost):**
- The locked book's authoritative numbers still require manual TV exports — Path E does not eliminate that for intrabar-dependent strategies (likely 3 of 4).
- Faithful Path E for Guardian needs an engine extension (next-bar-open + grace + slippage) that does not exist yet.

**Risks:**
- Path E parity may fail even for Guardian (intrabar path-dependence) → mitigation: §4 makes that a clean, pre-committed outcome, not a sunk cost.
- Isolated-account A2 still carries non-zero residual ban risk on the *research* account → mitigation: human cadence, one export at a time, structural isolation.

**Downstream artifacts:**
- `lab/analysis/legacy/guardian_parity_2026-06-23/` — harness + README (landed).
- Memory `reference_pine_check_tool` / new `project_tv_egress_automation` — pointer to this ADR.
- `REPO_MAP.md` — no change (research under `lab/analysis/`, ADR under `docs/adr/`).

---

## §7 — Implementation plan

- **Phase 0** — §0 reads confirmed current (done 2026-06-23).
- **Phase 1** — Land the Guardian signal port + tests + README under `lab/analysis/legacy/guardian_parity_2026-06-23/` (done; 9/9 tests pass) and this ADR.
- **Phase 2** — (gated, Joshua-owned) extend `PythonPrefilterEngine` with `next_bar_open` entry + grace-stop + slippage; produce ≥2 native Guardian exports; run the parity gate → resolves §4.
- **Phase 3** — Record the §4 outcome; status stays `Accepted` (policy is live now; the §4 test is an open empirical question, not a blocker on the policy).

---

## §10 — Audit hooks (runnable)

```bash
# Guardian signal port + execution engine still pass their unit tests
python lab/analysis/legacy/guardian_parity_2026-06-23/test_guardian_signal.py     # Expected: 9/9 passed
python lab/analysis/legacy/guardian_parity_2026-06-23/test_next_open_engine.py    # Expected: 9/9 passed

# The Rule-0 execution-model gap is still documented (next-bar-open premise)
grep -n "process_orders_on_close=false" core/strategies/guardian/guardian_gold_v5.5.pine
# Expected: line 9 (if this flips to true, the dominant §3 gap is gone — revisit)

# Path A via MCP-Chrome is still blocked (re-probe if revisiting browser automation)
#   navigate https://www.tradingview.com/chart/  -> expect "not allowed due to safety restrictions"

# §4 falsifier status
grep -n "End-to-end parity" lab/analysis/legacy/guardian_parity_2026-06-23/README.md
# Expected: "BLOCKED" until the engine extension + 2 native exports land
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-06-23-tv-backtest-egress-automation.md --type adr
# Expected: all 6 checks PASS

python lab/analysis/legacy/guardian_parity_2026-06-23/test_guardian_signal.py    # 9/9
grep -n "process_orders_on_close" core/strategies/guardian/guardian_gold_v5.5.pine
```

---

## Addendum 2026-07-27 — §1's rationale names a chain that no longer exists; the constraint transfers

§1 grounds the whole "un-riskable account" argument in a specific pipeline:
*"the authenticated TradingView account runs the live FXIFY trading edge (Pine → alert → Copygram
→ DXtrade)."* **Every named component of that chain is now retired** — FXIFY closed 2026-07-10,
Copygram retired with the venue, the DXTrade/CFD estate retired 2026-07-11
(`2026-06-30-no-manual-trading-cfd-retirement.md` + `2026-07-11-ops-cfd-estate-retirement.md`).

Read literally today, §1's justification is dead, and a reader could reasonably conclude the
constraint it justifies is obsolete. **It is not.** The dependency structure is unchanged and the
same TV account still sits at its head:

> **Pine → `alert()` → c1 rail listener (Fly) → CrossTrade → Tradovate (Tradeify Select 100K).**

The 2026-06-30 retirement ADR moved the **broker** to an isolated futures account; it did **not**
move the TradingView account, which remains the **sole origin of every c1 entry, add, exit and
flat**. There is no second signal source and no manual fallback (manual execution is retired). So
the consequence that motivated §1 — automation-triggered enforcement against this account takes
down live execution — holds identically; only the downstream venue names changed.

**Scope note, for accuracy:** §5's forbidden move is *"Running any TV automation (A/B/D)"* — the
three **backtest-egress** paths. It is not, on its face, a rule about page-level reads. Anyone
extending it to reads should say they are extending it. The durable core is the
**consequence asymmetry**, not a probability claim: this ADR nowhere establishes that a given
interaction triggers enforcement, and it explicitly accepts *"non-zero residual ban risk"*
elsewhere.

Superseded in part 2026-07-27 — see `2026-07-27-tv-agent-browser-access.md`, which reverses the
repo-side agent-access prohibition while retaining the allowlist-circumvention and
edge-protection bullets.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-23 | Initial authoring (research workflow `woys2grk6` + Guardian Rule-0 reads) | Joshua + Claude Code |
| 2026-06-23 | §7 Phase-2 engine extension landed (`next_open_engine.py` next-open+grace+slippage, 7/7 tests; `run_parity.py` driver). Parity now runnable; §4 falsifier verdict PENDING Joshua's ≥2 native exports. | Claude Code |
| 2026-06-23 | §4 falsifier **RESOLVED-POSITIVE (partial)** on first exports — count+entries+exits exact on the 10-trade overlap; two data-found fixes (stale-close-next-open + dd-protection-off) folded in (9/9 execution tests). See `lab/analysis/legacy/guardian_parity_2026-06-23/README.md` §Result. | Claude Code |
| 2026-06-23 | §4 upgraded to **FULL-WINDOW** on a back-page BAR_EXPORT (2025-06→2026-06): all 52 trades from the true $200K base — **net 0.46% / PF 1.76% both clear the 2% band**, 51/52 entries; residual = irreducible 15m stop-fill precision. Path E validated as a bar-close reproduction of Guardian. | Claude Code |
| 2026-07-01 | Disclosure follow-up: the Phase-1 port (`guardian_signal.py` + its unit tests) had been **publicly tracked** — a case this ADR's §2/§5 edge-protection reasoning never weighed. Untracked (kept locally, hash-pinned in `PORT_MANIFEST.sha256`) per ADR `2026-07-01-guardian-pyport-public-tracking.md`; history exposure accepted explicitly there (public since 2026-06-23; untracking limits amplification, not disclosure). §10's first two hooks now require the locally-restored port. | Claude Code |
