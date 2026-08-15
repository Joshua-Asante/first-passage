# Q-MONSURF-1 — Which monitoring surfaces are buildable venue-free now, and on what acceptance evidence? (MONITORING)

**Status:** `OPEN — F2 unblocked (rail retained)` — S1 ADR 2026-08-07 ruled F2 keep-warm; M1 spine retained. M-B Phase-3 logic battery buildable now; live-pointing still gated on M1 `RESOLVED`. Intaken 2026-08-05 (drafted 2026-08-04 by Joshua + claude.ai advisor from the four-tool-stack research report); `check_brief.py --type inquire` PASS (6/6)
**Authored:** 2026-08-04
**Intaken:** 2026-08-05 (handoff-verify PASS; anchors re-verified at `origin/main` `21e09c8`; DP2-dependency + M1-spine-risk notes added — see Amendment log)
**Closed:** N/A
**Authors:** Joshua + claude.ai (advisor); intake + amendment by CC
**Parent question:** N/A (triage parent; M-B/M-C surfaces open as their own Pre-Qs when their gates unlock)
**Sub-questions opened:** none yet (**M-B** idle-clock monitor is the limb that matters — venue-conditional; **M-A** shadow observer demoted to optional)
**Loop:** Inquire-phase Pre-Q — the **triage itself is the deliverable**; closure records each surface at its true gate and pre-registers M-B's acceptance so it is buildable the day F3 registers a venue
**Artifact path:** `docs/briefs/Q-MONSURF-1-monitoring-surface-triage-scoping.md`
**Spend by authoring:** $0 · K=0 · no manifest · nothing armed

---

## Amendment log (intake, 2026-08-05)

- **§0 re-anchored** at `origin/main` `21e09c8` (was `613aa0d`); content-diffed, no cited file changed
  in between (`handoff-verify` Phase-0 checklist run in full before this intake — confirmed no idle
  or activity monitor exists anywhere under `ops/`, matching this brief's core premise).
- **§1/§7 Phase 2 — explicit forward dependency on Q-VENUEGEO-1 DP2 added.** The original text
  correctly routed unpinnable idle-clock semantics to Q-VENUEGEO-1's DP2 sweep on the
  **Ambiguous-hold** branch (H-MONSURF-1), but treated this as a fallback rather than a forward
  sequencing fact. Since Q-VENUEGEO-1 was intaken the same day with DP2 now explicitly covering
  each candidate firm's idle-rule shape (existence/threshold/enforcement-hardness/reset semantics),
  M-B's Phase 2 freeze for **deployment at the eventual successor** properly waits on that sweep's
  output. This does not block Phase 2 from running now: the acceptance battery in Phase 3 tests the
  monitor's *logic* against the already-measured Tradeify cadence distribution
  (`c1_cadence_inactivity_2026-08-02`), which needs no new data. What is now explicit: **the freeze
  is provisional** (Tradeify-shaped semantics as reference implementation) until Q-VENUEGEO-1's DP2
  names the actual successor's idle-clock rules, at which point Phase 2 re-freezes before Phase 5
  deployment — never silently inheriting Tradeify's semantics onto a different firm's rule.
- **§5 — forbidden move added: no hard dependency on the M1 EventLedger surviving F2 unchanged.**
  M-B's Phase 3 acceptance-test harness must be built as a standalone module against the frozen
  simulated-quarter draw, not wired to `ops/c1_rail/c1_rail_telemetry.py`'s live schema. F2 (rail
  disposition, 2026-08-08) explicitly governs "M1-spine retention" — a tear-down ruling could sever
  or restructure that spine before F3 even has a successor to point M-B at. Phase 3 (build + battery)
  stays safely buildable now only if it doesn't assume the spine's current shape persists; the actual
  "point M-B at the live account, reusing the M1 event schema" step is already correctly gated at
  Phase 5 ("At F3 registration") in the original scoping — this amendment just makes the Phase-3
  independence explicit so an implementer doesn't quietly import live rail internals while building.

No other content changed. The M-A demotion, the triage structure, and the gate criteria are
otherwise as originally scoped.

---

## §0 — Rule 0 reads

Read this session (anchored at `origin/main` `21e09c8`, 2026-08-05; content-diffed against the
original `613aa0d` anchor — no cited file changed in between):
- `STATE.md` — stranded-threads block (five threads gated on "first live fill"; ECR re-home; lifecycle Call-1; ORB decay re-scope), via `git show`
- `docs/SESSIONS.md`, `CLAUDE.md` §posture — via diff
- Confirmed at intake: no idle/inactivity/activity monitor module exists anywhere under `ops/` (`rg -ln "inactivity|idle_clock" ops/` → empty; no `Monitor` class in `ops/**/*.py`) — the brief's central premise holds.

Anchored, body unread — `[§0-pending content read before lock]`:
- `docs/superpowers/specs/2026-08-02-venue-native-regime-monitor-design.md` — anchor: `b4222fb` (2026-08-02) — thresholds inherited; **build gated on first live fill** (the clause this Q surfaces, below)
- `docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md` — anchor: `47cc3eb` (2026-07-12) — ECR prereg; PARKED-DORMANT, discharge path gone with the de-scope
- `docs/adr/2026-06-07-decompound-remc-hold.md` §Addendum — anchor: `6158b13` (2026-08-03) — orphaned limb-2 falsifier; 11-08 standing-unfalsifiable escalation
- `lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md` — anchor: `92abdbb` (2026-08-03) — 26.3% zero-trade weeks; longest dead run 4; idle-gap median 3 / p90 9 / max 27 bdays (verified: matches RESULTS.md exactly at intake)
- `docs/spec/2026-08-02-tradeify-activity-rule-disposition-spec.md` — anchor: confirmed present at intake — token-trade ruling: Option A permitted in principle, M1-gated; **agent may never fire or authorize one**
- `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` — anchor: `6640141` (2026-08-02) — the structured-event spine M-B would reuse; retention rides F2 (see Amendment log above)

---

## §1 — Context & motivation

The de-scope stranded five monitoring-adjacent threads on "first live fill," and the board records them as one class. They are not one class. Triage, ordered by consequence:

**M-B — venue-conditional (needs an account, not fills). The limb that matters.** Trailing-DD proximity, consistency headroom, and above all the **activity/inactivity clock**. The seed-target spec makes this THE binding venue risk: at the incumbent's 0.22 duty, pass collapses to 3.0% with **96.9% account deletion**, and the cadence study shows why — 26.3% of Mon–Fri weeks are zero-trade, longest dead run 4 weeks, idle-gap p90 of 9 business days against a 5-idle-day deletion rule. **No automated observer for this exists anywhere in the estate** (confirmed at intake). It reuses the M1 structured-event spine for its *deployment* (Phase 5 only — see Amendment log); token trades remain operator-only per the 08-02 ruling — the monitor alerts, the operator acts. **Its Phase-2 freeze for a specific successor venue depends on Q-VENUEGEO-1's DP2 idle-rule sweep** (intaken the same day); Phase 3's acceptance test against the already-measured Tradeify distribution needs no new data and is not blocked.

**M-C — genuinely fill-stranded.** The live edge-captured-ratio monitor (discharge vehicle for Q-NAS-ECR-1's existing prereg) and per-fill slippage capture (re-homed from the dead Stage-2b path). Correctly gated; named here so the board stops recording them alongside M-B.

**M-A — venue-free but low-consequence. Optional, de-prioritized.** A Databento live/replay *market-data* regime observer computing the 08-02 design's inherited thresholds in shadow, alert-only. Genuinely has no venue dependency in its inputs — but a regime alert for a book that is not trading changes no decision, so building it now would fail the same retention test the board applies to every other row, while drawing on the agent budget the discovery campaign needs. **The load-bearing honesty item:** the 08-02 design's own build gate reads "first live fill." Whether that gate binds only the fill-coupled *venue-native* monitor or also a pure market-data observer is an **operator ruling this brief requests explicitly** — it does not reinterpret the clause to get building.

---

## §2 — Prior art / lineage

- Regime-monitor design (`b4222fb`) — every threshold inherited from it; nothing invented here.
- PREREG-NAS-ECR-1 (`47cc3eb`) — M-C's consequence rules live there; **not restated, not loosened** (the cross-brief Trap-#12 form).
- Decompound HOLD §Addendum (`6158b13`) — limb-2 orphaned; the 11-08 escalation this triage feeds context to.
- Activity-rule disposition spec (2026-08-02) — the operator-only token-trade boundary every monitor inherits.
- Cadence/inactivity study (`92abdbb`) — M-B's simulated-quarter test distribution.
- Q-VENUEGEO-1 (intaken same day) — DP2's per-firm idle-rule sweep is M-B's Phase-2 dependency for successor-venue deployment (intake amendment).

---

## §3 — Question (Q-MONSURF-1)

**Q-MONSURF-1:** Monitoring obligations exist at three distinct gate depths, but the estate currently records them as one stranded class. Which surfaces have no genuine venue/fill dependency, and what acceptance evidence must each class produce before its output is trusted?

---

## §4 — Falsifiable hypothesis (H-MONSURF-1)

**H-MONSURF-1 (primary — M-B acceptance, pre-registered now, tested at F3 registration):** If the idle-clock monitor, run against a simulated quarter drawn from the cadence study's own measured gap distribution (26.3% zero-trade weeks; p90 gap 9 bdays; max 27), alerts at **T-2 and T-1 business days** before every deletion-rule breach with **zero missed weeks and zero spurious alerts**, then the venue-conditional class is buildable on registration day and M-B lands as an alert-only observer; otherwise the monitor is not trustworthy and iterates — the monitor, never the rule.

**Reject H if:** any missed week or spurious alert over the frozen simulated quarter.
**Accept H if:** 0 missed / 0 spurious across the full frozen distribution draw.
**Ambiguous-hold if:** the venue's idle-clock semantics (business-day counting, week boundary, what resets the clock) cannot be pinned from DP2's verified facts → the gap list routes to Q-VENUEGEO-1's DP2 sweep, not to local guesswork.

⚠ **Testable now against the simulated distribution; deployable only at registration.** The acceptance test needs no venue — that is the point of pre-registering it here, so registration day costs zero design work.

**H-M-A (secondary, optional):** the shadow regime observer reproduces the 08-02 design's threshold events with 0 missed / 0 spurious against a hand-computed reference over a frozen replay window. Pre-registered for completeness; **not scheduled** — runs only if the operator elects it after M-B lands and spare agent budget exists.

---

## §5 — Forbidden moves

- **Silently reinterpreting the design's "first live fill" build gate** — the M-A-vs-venue-native distinction is *requested as a ruling* (§7), never assumed. Note the ruling is now only needed **if M-A is elected**; M-B's gate is a venue/account, which is unambiguous.
- **Building M-A because it is the buildable one** — the original draft's own failure mode, and the sharpest temptation in this brief: with no venue, a shadow observer is the only thing that *can* be built, and building it feels like progress. It alerts on a book that is not trading. Buildability is not consequence.
- **Letting the triage itself become the deliverable's substitute for M-B's pre-registration** — a classification with no acceptance test attached is a board edit, not a brief; H-MONSURF-1 must be frozen for this Q to have shipped anything.
- **Any monitor firing or authorizing an order, including a token trade to save the activity clock** — explicitly operator-only per the 08-02 disposition; monitors observe and alert, full stop. (Mechanical check in §10: zero order-send imports in the monitor package.)
- **Restating or loosening PREREG-NAS-ECR-1 thresholds while "just naming" M-C** — the prereg is cited by path and left byte-alone.
- **Inventing thresholds the design doesn't specify** — gaps route back as a spec addendum request (Ambiguous branch), not as local judgment.
- **Live-feed add-on spend beyond the flat Standard entitlement without a signed ceiling** — M-A's marginal cost claim is $0; keep it true.
- **Building M-B's Phase-3 acceptance harness as a hard import against the live M1 EventLedger schema** (intake addition) — F2 governs that spine's retention and rules 2026-08-08; a Phase-3 build that assumes the spine's current shape persists risks needing rework the moment F2 rules tear-down. Build against the frozen simulated distribution as a standalone module; wire to M1 only at Phase 5, post-registration.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | M-B acceptance passes (0 missed / 0 spurious over the frozen simulated quarter) **and** the triage is written to the board with each surface at its true gate | `INTEGRATE — M-B is registration-ready (deploys alert-only on F3 registration, no further design work); M-C recorded as first-live-fill-gated pointing at its existing prereg; M-A recorded as elective` |
| `FALSIFIED` | any missed week or spurious alert at frozen tolerances | `ITERATE — repair the monitor, never the rule; re-run the frozen draw` |
| `AMBIGUOUS-HOLD` | idle-clock semantics unpinnable from DP2's verified facts | `ITERATE — return target: Q-VENUEGEO-1 DP2 sweep; re-test when the clause is verified` |
| `MOOT` | F3 rules "no admissible successor" | `STOP — M-B has no venue to monitor; triage record stands as the board correction; re-proposal bar = a registered venue` |

**Note the FALSIFIED row is `ITERATE`, not `STOP`** — a monitor failing its own battery is a defect in the monitor, and the deletion rule it guards does not become less binding because the first implementation missed a week.

---

## §7 — Execution plan

**Now ($0, no venue needed):**
- **Phase 0** — Rule-0 reads (§0 pending list).
- **Phase 1** — **Write the triage to the board**: M-B (venue-gated) · M-C (first-live-fill-gated, pointing at PREREG-NAS-ECR-1) · M-A (elective). This replaces the single "five threads stranded on first live fill" block with three rows at three true gates. **This is the deliverable.**
- **Phase 2** — Freeze (§8): the simulated-quarter draw from the cadence distribution, alert lead times (T-2/T-1), tolerances, and the idle-clock semantics — **provisionally against Tradeify's measured shape** (intake amendment), re-frozen once Q-VENUEGEO-1's DP2 names the actual successor.
- **Phase 3** — Build M-B's logic **as a standalone module, no live M1-schema import** (intake amendment), and run the acceptance battery against the simulated quarter. No venue, no account, no live feed required.
- **Phase 4** — Assert §6; closure per §9 (gate 14 typed Iterate block).

**At F3 registration (no design work owed beyond the re-freeze):**
- **Phase 5** — Re-freeze idle-clock semantics against the actual successor's DP2-verified rules if they differ from the Tradeify-shaped provisional freeze; point the accepted M-B at the live account, wiring to the M1 event schema (if F2 retained it) at this step, alert-only. Operator acts on alerts; the monitor never trades.

**Elective, unscheduled:**
- **M-A** — requires the build-gate ruling first (does "first live fill" bind a pure market-data observer?). Runs only on operator election with spare agent budget, after M-B lands.

**M-C** — no build in this Q; pointer-only to its existing prereg.

---

## §8 — Verdict pre-registration

`docs/briefs/pre-registration/Q-MONSURF-1-verdict-preregistration.md` — committed before Phase 3. Hash/date: `<at prereg commit>`.

---

## §9 — Closure record format

Per `references/closure_record.md`; typed `## Iterate` block mandatory (gate 14 HARD).

---

## §10 — Audit hooks (runnable)

```bash
# Design's build-gate clause byte-intact (not quietly edited to admit M-A)
rg -n "first live fill" docs/superpowers/specs/2026-08-02-venue-native-regime-monitor-design.md

# ECR prereg untouched by this Q
git log -1 --format="%h %ad" -- docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md   # expect 47cc3eb lineage

# No order-send capability in the monitor package
rg -ln "crosstrade|payload|order" ops/ | rg -v c1_rail | rg monitor   # expect empty

# No hard M1-schema import in the Phase-3 build (intake amendment)
rg -n "c1_rail_telemetry|EventLedger" <monitor_pkg>/idle_clock*.py   # expect empty until Phase 5

# Triage landed: three rows at three gates, not one stranded block
rg -n "M-A|M-B|M-C|first live fill" STATE.md

# M-B acceptance reproducible against the frozen simulated quarter
python <monitor_pkg>/idle_clock_acceptance.py --draw <frozen> --reproduce

# M-A not built ahead of election (the resequence held)
git log --oneline --diff-filter=A -- <monitor_pkg>/regime_observer* | tail -3   # expect empty until elected

# Ruling request recorded only if M-A elected
rg -n "MONSURF.*ruling" docs/notes/ STATE.md
```

---

## Verification

`check_brief.py --type inquire` run at intake (2026-08-05): PASS (6/6). §0 anchors re-confirmed against `origin/main` `21e09c8`; cadence-study numbers grep-matched (26.3% / p90 9 / max 27 — exact).

## Pre-Lock Checklist

- [x] §0 pending reads completed with anchors (re-verified at intake against `21e09c8`; premise confirmed — no monitor exists)
- [ ] Triage written to the board (Phase 1) — the deliverable, not deferred to closure — **owed, not run at intake**
- [ ] Simulated-quarter draw + T-2/T-1 lead times + tolerances frozen at §8 — owed, Phase 2
- [ ] Idle-clock semantics sourced from DP2 verified facts (or the Tradeify-shaped provisional freeze, explicitly labelled) — owed, Phase 2
- [ ] Zero order-send paths asserted mechanically — owed, Phase 3
- [ ] Zero hard M1-schema import asserted mechanically (intake addition) — owed, Phase 3
- [ ] M-A confirmed NOT built (elective; no build without operator election + ruling)
- [x] Q-ID confirmed unclaimed (checked HEAD + origin/main at intake, 2026-08-05)
