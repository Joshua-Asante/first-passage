# Q-FIRMEOD-1 — CLOSURE: `FALSIFIED` (CLOCK flips on Bulenox_100K's own trailing branch; LOCK surfaces unexamined lock language on Bulenox's Master Account primary source)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-23
**Lane:** `UNASSIGNED`
**Pre-registration:** [`Q-FIRMEOD-1-verdict-preregistration.md`](../pre-registration/Q-FIRMEOD-1-verdict-preregistration.md) — frozen at commit `9bb650c`, before Phase 1 ran
**Successor:** none named yet — the re-proposal bar below names what a successor must do, but does not itself open one
**Spend / K:** $0.00 · K consumed: 0 (validity/governance re-check on an already-coded engine branch, not a strategy-candidate proposal — same class as Q-M1WIRE-1/Q-ORBCUSH-1/Q-GATESTACK-1)
**Live effect:** none — no `core/`, `firm_rules.py`, `dd_protection.py`, allocation, Pine, or rail surface touched or edited; no live sizing changes; Bulenox/BluSky are research-only configs today (no live c1 book on either firm)
**Artifacts:** this closure + its pre-registration are the only artifacts (no new lab/ campaign directory needed — both checks ran as direct one-off invocations of already-existing, already-committed code and fixtures per the frozen method)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | CLOCK holds AND LOCK holds | CLOCK **fails** (bust_trailing 0→1 flip, `Bulenox_100K`); LOCK **fails** for Bulenox (lock-adjacent language found on primary Master Account page) | — |
| `FALSIFIED` | CLOCK fails OR LOCK fails | Both disjuncts independently true | ✓ |
| `AMBIGUOUS-HOLD` | either cheap check cannot execute at $0 | Neither check was blocked — both executed to a determinate result (Bulenox's originally-cited URLs were dead, but the frozen method's Wayback fallback executed cleanly) | — |

**CLOCK (Phase 1b).** Reused the pre-existing, CI-stable fixture in `tests/core/test_mc_intraday_barrier.py::test_static_and_trailing_branches_also_see_the_intraday_low` (on disk since the 2026-08-14 public-transition base commit `027a729`, predating this brief) — its `dd_type="trailing"` case is parametrized byte-identically to `Bulenox_100K`'s real `firm_kwargs()` output (`trailing_dd_pct=-0.03`, `starting_equity=$100,000`, `daily_loss_pct=None`). Diffed `simulate_path` directly against production code:

```
no-intraday: ('horizon_cap', 1, 0.001, None)
intraday:    ('bust_trailing', 1, 0.001, 0)
```

`bust_trailing` count 0 → 1 — the same class of flip that drove Tradeify's PASS→FAIL. `pytest tests/core/test_mc_intraday_barrier.py -q` → `9 passed`, confirming the underlying engine behavior is stable and CI-verified, not an artifact of the one-off script.

**LOCK (Phase 1a).** The brief's originally-cited Bulenox URLs (`bulenox.com/help/qualification-account/`, `/help/master-account/`) are now dead (404 via both `WebFetch` and browser navigation — a genuine post-citation site restructure). Per the pre-registered fallback, re-read the same pages via Wayback Machine captures (`20260120055137` and `20260310032809`, both pre-dating the code's 2026-07-01–07-27 citation window). Bulenox's own Master Account Rules page states, verbatim: *"The trailing or EOD drawdown stops moving when the trailing or EOD drawdown reaches the initial starting balance +100."* — lock-adjacent language ("stops moving," a fixed +$100 offset structurally identical to Tradeify's `dd_lock_offset_usd`) describing the same "trailing" mechanism `FIRM_RULES` encodes as never-locking. This is a **new finding** — `grep -ri "starting balance +100\|stops moving"` across the whole repo returns zero prior hits. BluSky's equivalent pages (both eval-stage article 12434059 and funded-stage article 11490300, both live and directly read) carry **no** lock language at all — LOCK holds cleanly for BluSky.

## 2. What the pre-registration predicted vs what happened

The pre-registration explicitly anticipated the originally-cited URLs might be dead and froze a Wayback fallback rule in advance, rather than letting the live-site outage become an ad hoc justification for an `AMBIGUOUS-HOLD` softening — that fallback executed and produced a determinate primary-source read, so `AMBIGUOUS-HOLD` correctly did not fire on that axis. The pre-registration also explicitly named, in advance, the exact trap this closure had to resist: that a scope argument ("the lock is Master-only, and the engine never simulates past Qualification, so it doesn't matter") could be used to quietly convert a found-lock-language LOCK failure into a pass. That trap materialized almost exactly as anticipated during Phase 1a, and the frozen table held — LOCK fired FALSIFIED on the literal text, with the scope question recorded as an open caveat rather than a silent override. No surprise in the *mechanism*: CLOCK failing on the `trailing` branch was the expected-shape finding (Section 0 had already established the branch is engine-generic, shared with Tradeify's now-fixed defect); what was not anticipated going in was that LOCK would independently *also* fail, and specifically for Bulenox (not BluSky) — the brief's own Section 1 treated CLOCK and LOCK as two separately-plausible but unconfirmed risks, not as a pair where both would land on the same firm.

## 3. What this closure does NOT license

- Does not edit `dd_type`, `trailing_dd_pct`, or any `firm_rules.py` constant for Bulenox or BluSky — Section 5 forbids that under this brief regardless of what Phase 1 found; any branch change is a separate change-control action (pre-registration → re-derivation → admitting ADR).
- Does not resolve whether Bulenox's Master-account lock is reachable by the currently-simulated (Qualification-only, absorbing-at-pass) horizon — that scope question is real, recorded, and explicitly **not** decided here; a successor must investigate it, not assume either answer.
- Does not extend to BluSky's CLOCK behavior — only Bulenox's `trailing` branch was engine-diffed. The BluSky evaluation-rules article's own "at any point" / "realtime" language is textual evidence the same defect class plausibly applies there too, but this closure does not claim BluSky's CLOCK has been falsified by direct measurement — only that it has not been shown to hold either.
- Does not touch or re-open the F2 fixed-$-vs-%-of-peak caveat (`core/mc/preflight.py:30-34,98-102`) — named out of scope in the parent brief's own Section 1 and left exactly as open and unquantified as before.
- Does not change anything about the live c1 book, which trades neither Bulenox nor BluSky today (both are research-only `FIRM_RULES` entries; no live account, no rail wiring, no sizing consequence).
- Does not license citing any current Bulenox/BluSky bust-rate figure in a cross-firm capital-allocation comparison — that is precisely what the `FALSIFIED` disposition below bars until a successor lands.

## 4. Defects found in the frozen brief (recorded, not repaired)

None in the brief itself. One defect found in **production code's documentation**, recorded here per Trap #12 (the frozen pre-registration and brief are byte-unedited; this is a finding *about* `firm_rules.py`, not an edit to it): the Bulenox sourcing comment at `core/firm_rules.py:41-77` cites `bulenox.com/help/master-account/` and asserts "no reset option" is "the only Master difference" from Qualification — but the cited page's own text also states the trailing DD "stops moving" at a fixed +$100 offset once an account reaches Master. That second difference was never captured in the sourcing comment. This is the same *shape* of omission (silence read as denial/completeness) as the original Tradeify defect, though — unlike Tradeify's case — it has not been shown here whether it actually changes any bust figure the engine currently produces, since the engine never simulates the Master stage at all for these 7 tiers.

## 5. Lesson candidates

**Below the two-incident bar on its own, but worth flagging alongside Q-M1WIRE-1/Q-GATESTACK-1/Q-ORBCUSH-1 (the assumption-sweep's other 2026-08 FALSIFIED closures):** this is now at least the second time (after the original Tradeify/MFFU CLOCK+LOCK fix) that re-pointing the exact "absence-of-citation read as denial" check at a *sourcing comment*, rather than at the engine code, surfaced a real primary-source gap the original author's comment simply never addressed. The Tradeify fix corrected an engine constant; this finding is purely in a `firm_rules.py` *comment*'s completeness, one level upstream of any constant. Watch for whether a third instance (a third firm's sourcing comment) makes this a load-bearing pattern about how sourcing comments get written, not just how engine branches get chosen.

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `FALSIFIED`
- **Model update:** The engine-generic-fix-mechanism assumption Section 5 named as the exact trap this brief exists to close ("the fix mechanism is engine-generic, therefore it must already be fine for Bulenox/BluSky, without re-running it") was in fact live: CLOCK genuinely does flip on Bulenox's own `dd_type="trailing"` branch under its own real tier parametrization, using nothing but pre-existing, already-committed engine test fixtures — no new simulation, no new market data. LOCK adds a second, independent, previously-undocumented finding: Bulenox's own Master Account primary source contains lock-adjacent language the current `firm_rules.py` sourcing comment never addressed, whose applicability to the currently-simulated (eval-only) horizon is a genuinely open scope question, not yet resolved either way. Every current Bulenox/BluSky bust-rate figure is now confirmed to sit in the same "EOD-clock lower bound" caveat class CLAUDE.md already applies to Tradeify's W1 figures — but that caveat line is currently scoped in-repo to Tradeify/Class-S only, and this closure is the evidence that scoping gap was live, not costless.
- **Next:** `STOP`
- **Routing:** n/a — no successor named here (naming ≠ opening, parent-Q convention). A future session taking up either repair path below opens a fresh Q against this closure, not an amendment to it. **2026-08-23 update (pointer only, this closure stays byte-unedited otherwise):** both repair paths named in the entry packet below have since been executed under the [§4 firm-model-repair plan](../../superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md), operator-GO'd the same date — (i) the 7-tier intraday-honest re-run: [`RESULTS`](../../../lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md) · [`audit note`](../../notes/audits/2026-08-23-r1-bulenox-blusky-clock-repair.md); (ii) the lock-scope question, resolved NO: [`audit note`](../../notes/audits/2026-08-23-bulenox-lock-scope-resolution.md). The re-proposal bar below is correspondingly discharged for citation purposes — see those artifacts for the actual figures before citing any Bulenox/BluSky bust rate.
- **Entry packet:** *(required — Next = STOP but with a live re-proposal bar, so the packet is what a successor must carry)* — (i) this closure's CLOCK evidence (the exact `firm_kwargs('Bulenox_100K')` output and the 0→1 `bust_trailing` flip, reproducible verbatim from the command in §1 above) as the frozen starting point for a W1-pattern intraday-honest re-run across all 7 Bulenox/BluSky tiers; (ii) this closure's LOCK evidence (the verbatim Master Account Rules quote + both Wayback capture URLs/timestamps) as the frozen starting point for resolving the Bulenox lock-scope question — does it reach the simulated Qualification-only horizon, yes or no, with its own primary-source-grounded answer, not an inference; (iii) explicit note that BluSky's CLOCK was **not** independently engine-diffed here (only textually suggestive) — a successor should not assume BluSky is CLOCK-clean without running its own tier through the same diff Bulenox got.
- **Stop rule / re-proposal bar:** No Bulenox/BluSky bust-rate figure may be cited in a cross-firm capital-allocation comparison until a successor brief either (a) re-runs the intraday-honest fix (`intraday_low`) across all 7 tiers per the W1 ADR pattern and reports whether any published figure flips, and/or (b) resolves the Bulenox lock-scope question and, if the lock is found to bite the modeled horizon, re-classifies the tier to `trailing_locking` with sourced lock terms via its own pre-registration → re-derivation → admitting ADR (never as an in-place edit riding on this closure). Re-tuning window/threshold choices without touching either of these two named gaps does not clear this bar.
- **Board write:** `STATE.md forward board: "- **2026-08-23** — \`Q-FIRMEOD-1\` closed \`FALSIFIED\`. [\`brief\`](docs/briefs/Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md) [\`closure\`](docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md)"` Owner: this closure.
- **Registry:** `n/a — governance/validity re-check on an already-coded engine branch, not a strategy-mechanism kill (same convention as Q-M1WIRE-1, Q-GATESTACK-1, Q-ORBCUSH-1; no docs/rejected_candidates.md row)`

## §10 audit-hook discharge

```bash
# Section 0 anchors still resolve (all three cited files last touched same commit)
$ git log -1 --format="%h %ad" --date=short -- core/mc/simulation.py core/mc/preflight.py core/firm_rules.py
94041d9 2026-08-23

# 7 trailing tiers cross-reference (Bulenox 5 + BluSky 2)
$ grep -n '"dd_type": "trailing"' core/firm_rules.py
92,104,116,128,140,508,524   [7 hits, confirmed]   # as-of-authoring 2026-08-23
# 2026-08-24 currency: same 7 hits, lines now 122,134,146,158,170,600,616
# Durable hook (line-number-free):
$ grep -c '"dd_type": "trailing"' core/firm_rules.py
7

# CLOCK evidence reproduces verbatim (see §1 command + output above)
$ python -m pytest tests/core/test_mc_intraday_barrier.py -q
9 passed in 0.25s

# LOCK evidence — Wayback captures resolve at the timestamps cited
$ # https://web.archive.org/web/20260120055137/https://bulenox.com/help/master-account/
$ # https://web.archive.org/web/20260310032809/https://bulenox.com/help/qualification-account/
[both fetched live during Phase 1; full text extracted via DOM textContent, not summarized]

# Repo-wide check that the LOCK finding is genuinely new (no prior record)
$ grep -riE "starting balance \+100|stops moving" .
[zero hits before this closure]

# Pre-registration commit predates Phase 1 (ordering holds)
$ git log --oneline -- docs/briefs/pre-registration/Q-FIRMEOD-1-verdict-preregistration.md
[frozen at 9bb650c, same session, before Phase 1 executed]
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Operator GO recorded; pre-registration authored and frozen; Phase 1a (LOCK) + Phase 1b (CLOCK) executed same session; closure authored. `FALSIFIED` recorded. | Claude Code (Sonnet 5), operator GO |
| 2026-08-24 | §10 currency note only: `dd_type=trailing` grep line numbers shifted (still 7 hits). Durable hook is `grep -c` expected 7. Verdict / Iterate unedited. | Cursor (surface-consistency Packet 5) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md
grep -c "Fired?" docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md
```
