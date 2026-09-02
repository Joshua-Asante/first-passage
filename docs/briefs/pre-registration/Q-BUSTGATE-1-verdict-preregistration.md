# Pre-registration — Q-BUSTGATE-1 (Part-A eval bust-gate re-derivation, fee-vs-upside)

**FROZEN 2026-07-23, before the economic derivation number is admitted as a successor
ceiling.** This artifact freezes the *derivation method*, the *pinned inputs*, and the
*decision rule* for the 08-08-packet **A0 / P0** re-derivation directive (operator, 2026-07-23).
It exists so the successor ceiling — if one is admitted — is derived from a rule fixed
**before** the number is read, not reverse-engineered to clear the operator's parallel
**1.00×** aim (directive 2). No number below changes after the derivation is read; a change
requires closing this pre-registration and opening a fresh one (Known Trap #12).

**Status:** FROZEN / not-yet-exercised. The incumbent **Part A bust ≤ 3.0% / pass ≥ 50%**
(2026-07-13 survivor-scoring pre-reg, commit `be6dda6`) **stands unchanged and in force**
until — and unless — the companion Pre-Q brief admits a successor under the §D rule below.
**Loop of record:** STRATEGIC.
**Companion Pre-Q:** [`../Q-BUSTGATE-1-bust-gate-re-derivation.md`](../Q-BUSTGATE-1-bust-gate-re-derivation.md).
**Packet home:** [`../2026-07-17-0808-packet-delta-and-sequence.md`](../programs/2026-07-17-0808-packet-delta-and-sequence.md) §0.5 directive (1), §3 P0.
**Authored:** 2026-07-23 · Claude Code (Opus 4.8), operator-directed.

---

## §A — Frozen inputs (pinned to closed artifacts; not re-computed here)

| # | Input | Value | Source (commit) |
|---|---|---|---|
| I1 | Incumbent Part A ceiling (the object under re-derivation) | **bust ≤ 3.0%** (daily+static+trailing), **pass ≥ 50%**, Run-2, $100K band | survivor-scoring pre-reg §3 `be6dda6` |
| I2 | Incumbent ceiling's *stated* rationale | barrier-width analogy: 3.0% = the $100K band's own DD-barrier width; "a deployable edge should bust less often than its barrier is wide" | survivor-scoring pre-reg §3 `be6dda6` |
| I3 | Actual-paid eval fee (Tradeify Select 100K, JULY promo applied) | **$111 promo** (list $181); reset/re-attempt = a fresh eval purchase | Q-RAIL-1 PHASE4 `43db219` line 35 |
| I4 | Conservative per-reset cost used by Q-FUNNEL-1 (eval + 3-mo bridge run-rate) | **$328 list / $258 promo** (all-in cost-to-first-live-fill) | Q-RAIL-1 PHASE4 `43db219` line 39 |
| I5 | Funded-payout upside cap (single Flex payout) | **≤ min($4,000, 50% of total profit)**; 90/10 split; activation fee **$0** | book-composition §0 rule pins `730bb29`; PHASE4 line 36 |
| I6 | Book funded economics (2-leg c1 geometry) | eval pass **63%** / median **8.2 mo**; funded-dead-1y **43%**; renewal-reward chain **$339/acct-mo** | book-composition §2 `730bb29` |
| I7 | Q-FUNNEL-1 horizon-robust cell | `edge_panel_historical` (both retry policies): **1.00× beats 0.25× and 0.50× on EV/dollar-day at every horizon {126, 252, 504} in both regime halves** | Q-FUNNEL-1 closure `b56c5b3` |
| I8 | Bust of each admissible rung (2-leg, Tradeify Select 100K, Run-2) | 0.50× (WATCH-1, ratified) **0.08%**; 1.00× **4.37%** (H1) / **10.37%** (bootstrap-95th) | Q-FUNNEL-1 closure `b56c5b3` (0.08% ratified; 4.37/10.37% at 1.00×) |
| I9 | Lifecycle ladder cap | automation is **down-only**; the maximum admissible rung is **1.00×** (never sizes up past it) | `strategy_lifecycle.md`; four-friendly-firms lifecycle wiring |

**Fee/upside asymmetry (arithmetic on I3/I5, no new data):** one funded Flex payout (up to
$4,000) against one eval re-attempt ($111 promo) is a **≈36:1** upside:cost ratio; against the
conservative $328 all-in per-reset it is **≈12:1**. This asymmetry is the entire reason
Q-FUNNEL-1 found a higher-bust rung EV-superior (I7). It is pinned here, not re-derived.

---

## §B — Frozen derivation method

The re-derivation does **not** run a new Monte Carlo. It reads the already-closed Q-FUNNEL-1
EV verdict (I7) — the pinned artifact the operator directive names — and asks a single
**locational** question, fixed here before the answer is read:

> **Does the eval-fee-vs-funded-upside-optimal admissible rung bust *inside* the incumbent
> 3.0% ceiling, or *outside* it?**

- The **fee-vs-upside-optimal admissible rung** = the rung Q-FUNNEL-1's horizon-robust
  `edge_panel_historical` cell prefers on EV-per-dollar-day (inclusive of resets at the I3/I4
  fee and funded payouts), capped at the ladder maximum 1.00× (I9).
- Its **bust** = the Run-2 daily+static+trailing headline for that rung on the Tradeify
  Select 100K deployable expression (I8), read via `preflight.summarize_outcomes` (never
  `compute_default_config()['bust_rate']` — F1).
- **Inside** ⇔ that bust **≤ 3.0%**. **Outside** ⇔ that bust **> 3.0%**.

No free tolerance parameter is introduced. The method is deliberately **binary and
locational** rather than "compute an economic ceiling number `b*` and compare to 3.0%,"
because the pure fee-vs-upside break-even bound (net EV → 0) is degenerate — the ≈12–36:1
asymmetry pushes it far above any survival-relevant band — and pinning a precise `b*` would
require a bust-swept re-MC not authorized by this brief. The locational test is fully
answerable from the closed Q-FUNNEL-1 artifact and cannot be tuned toward a target.

---

## §C — Frozen tolerance / robustness guards

1. **Horizon-robustness required.** The optimal-rung read is taken **only** from Q-FUNNEL-1's
   horizon-robust cell (`edge_panel_historical`, verdict direction stable across {126, 252,
   504}). The horizon-**fragile** cell (`edge_half_panel`, H1 reverses at 126) is **excluded**
   from the locational read — it may not decide the fork.
2. **Down-only ladder cap.** The optimal admissible rung is capped at 1.00× (I9). If EV would
   prefer >1.00×, the read still uses 1.00× (the gate cannot authorize sizing up).
3. **F1/F2 engine discipline inherited verbatim** from the survivor-scoring pre-reg §5: headline
   bust = daily+static+trailing via `summarize_outcomes`; `trailing`-geometry firm reads stay
   optimistic-lower-bounds; `ACTIVE_FIRM` is not switched to run a tier.

---

## §D — Frozen decision rule (routes the companion brief's §6 verdict)

| Read (from §B) | Verdict (H-BUSTGATE = "economics ratifies 3.0%") | Disposition (frozen) |
|---|---|---|
| Optimal admissible rung busts **≤ 3.0%** on the horizon-robust cell | **`RESOLVED`** (H accepted) | The incumbent 3.0% is fee-vs-upside-consistent; its rationale upgrades from barrier-width analogy (I2) to economics. No successor; no ceiling edit. |
| Optimal admissible rung busts **> 3.0%** on the horizon-robust cell | **`FALSIFIED`** (H rejected — a legitimate finding) | 3.0% is **not** a fee-vs-upside quantity — it can only be a survival / P(pass) / firm-relations gate. Output = a two-option operator fork (A: retain 3.0%, re-justified as a survival gate; B: adopt an EV-per-dollar-day objective via a **fresh superseding ADR**). **Neither option edits this pre-reg or the 2026-07-13 pre-reg in place.** No *successor* ceiling is admitted, so the incumbent 3.0% stands and any 1.00× rung ADR is **blocked** (packet §2 step 5) until the operator picks. |
| The optimal rung is **horizon-fragile** (only the excluded cell would flip the read) | **`AMBIGUOUS-HOLD`** (OPEN) | The economic optimum is not robustly identified; the derivation cannot discriminate. 08-08 records OPEN; 3.0% stands; 1.00× rung ADR blocked. |

**The 1.00× aim is never itself a trigger in this table.** That a given disposition would
(or would not) make 1.00× admissible is an *output* to be reported, never an input that
selects the disposition. Choosing the derivation to clear 1.00× is the forbidden move this
freeze exists to prevent.

**A successor ceiling, if fork-option A or B is later ratified, is admitted only via a fresh
Trap-#12-compliant brief + freeze — never by editing `be6dda6`'s `3.0%` string.**

---

## §E — Pinned expectation (stated from the closed artifact, for post-hoc honesty)

From I8 (Q-FUNNEL-1 closure `b56c5b3`, already closed before this freeze): the horizon-robust
optimal admissible rung is **1.00×**, which busts **4.37% (H1) / 10.37% (bootstrap-95th) > 3.0%**.
Under §D the **middle row** is therefore expected to fire (**`FALSIFIED`** — H's "economics
ratifies 3.0%" claim rejected; route to operator fork). This expectation is recorded so that a
*different* companion-brief outcome would be a visible surprise, not a silently-absorbed edit.
It does **not** pre-decide the operator's fork choice (A vs B), which is not this brief's to make.

---

## §F — Audit hooks (runnable)

```bash
# The frozen incumbent ceiling this re-derivation must not edit in place.
grep -n "3.0%\|P(pass) ≥ 50%\|≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md

# The pinned fee (actual-paid promo) and the conservative per-reset figure.
grep -n "111\|181\|328\|258" lab/analysis/c1/q_rail_1_2026-07/PHASE4.md | head

# The horizon-robust cell + the 1.00× bust the locational read consumes.
grep -n "edge_panel_historical\|horizon-robust\|4.37%\|10.37%\|0.08%" docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md

# This freeze predates the companion brief's derivation (commit ordering).
git log --oneline -- docs/briefs/pre-registration/Q-BUSTGATE-1-verdict-preregistration.md \
                     docs/briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md
```
