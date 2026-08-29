# Notice — regime conditionality shows up everywhere this session touched; a forward regime-awareness capability is an unbuilt, cross-cutting gap

**Notice ID:** N-2026-08-28-regime-conditionality-cross-cutting-forward-item
**Observed:** 2026-08-28
**Author:** Claude Code (Sonnet 5), operator-directed — surfaced while investigating an Aegis-6J1 companion-leg candidate search, then explicitly flagged by the operator as a forward item deserving its own session, not action now.
**Source:** this session's own work (Aegis-6J1 ledger reads, the M6A/HG discovery pass, ORB-MNQ's ledger) plus `docs/adr/2026-05-23-allocation-refresh-2.md` Addendum 2026-08-02 (`decompound_remc_2026-06-07` clean-vintage re-run).
**Status:** `HOLD` — operator explicitly deferred to a dedicated future session.
**Lives in:** `docs/notes/notice/N-2026-08-28-regime-conditionality-cross-cutting-forward-item.md`

---

## §0 — Source anchor

- **Aegis-6J1**: `ops/instruments/6J.md` J4/J8/J9/J14 — every standalone or composed survival re-measurement of Aegis-6J1 names the 2020–2023 window ("H1") as the failure driver, independent of sizing, cap, or commission assumption tested this session and in prior sessions.
- **The M6A/HG divergence-reversion candidate** (this session, scratch analysis, not committed to the repo): split-half + year-by-year regime check found a real, cost-clearing signal in 2022–2023 that decayed to statistically indistinguishable-from-noise by 2025, with an erratic (not monotonic) partial 2026 revival.
- **ORB-MNQ-1**: `ops/instruments/MNQ.md` N1/N5 and the 2026-08-26 session-log entries — edge peaked 2023, has declined every year since, and the most recent corrected full-panel measurement busts at every tested contract size.
- **The CFD-era four-strategy locked book** (Guardian Gold + Striker DJ30 + Striker NAS100 + Aegis USDJPY): `docs/adr/2026-05-23-allocation-refresh-2.md` Addendum 2026-08-02, citing `lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_cleanvintage_2026-06-25.md` §"Half-panel regime cut (Part B)" — the exact locked config, on its full un-compounded history, split H1 2020-01→2023-03 vs H2 2023-03→2026-06: **H1 bust 13.84%, p99 DD 7.76% (FAIL); H2 bust 0.21%, p99 DD 4.53% (PASS)**. Disposition was HOLD: *"no viable static sizing config (allocation or dd_protection) is regime-robust — both de-risk candidates also FAIL H1."*

## §1 — The observation

Four independent candidates — spanning three different asset classes (JPY FX, gold, equity indices), at least three different mechanism shapes (BE-managed trend continuation, opening-range breakout, mean-reversion-on-divergence), and two different eras (the CFD/Pepperstone book and fresh 2026 futures-era discovery) — all show the same qualitative pattern: real, sometimes cost-clearing performance in one period, and materially weaker (in three of the four cases, decisively so) performance in another, with the 2020–2023 stretch (COVID crash + the 2022 rate-shock/Ukraine period) as the recurring weak/failing window across every one of them.

No strategy, mechanism, or static sizing config tested in this repo — across both the locked CFD-era book and this session's own fresh discovery work — has been found to be regime-robust in the strict sense (passing survival criteria in every sub-period tested). This is not one instrument's problem or one mechanism family's problem.

## §2 — Why it stands out

- **Baseline:** every closed regime-robustness check in this estate treats regime-conditionality as a per-candidate property to be measured and gated (`docs/methodology/regime_robustness_gate.md`'s half-panel split), not as a market-wide state to be detected and acted on going forward.
- **Delta:** the breadth here — same failing window recurring across unrelated asset classes and mechanism types, in both an old CFD book and fresh futures-era work — is more consistent with a shared macro-liquidity/volatility regime than with per-candidate overfitting. That distinction matters: if it's the latter, the fix is better candidate selection; if it's the former, the fix is a market-state-aware overlay, a structurally different kind of tool this repo does not currently have.
- **Frequency check:** this specific cross-cutting framing (four unrelated candidates, one shared failing window) has not been assembled in one place before this notice. Related but narrower prior work exists — see §3.

## §3 — What's already in the repo, and what already failed

**Tools that exist and are relevant:**
- `docs/methodology/regime_robustness_gate.md` — the half-panel-split + block-bootstrap methodology used to *detect* regime-fragility after the fact, on a candidate that already exists. Does not provide forward, real-time regime awareness.
- `docs/adr/2026-07-26-regime-candidate-flag-lane.md` — infrastructure for flagging regime-conditional candidates (built for ORB-MNQ's post-2020-only viability) so they can't promote purely on the window that selected them. A gating tool, not a detection/overlay tool.

**Prior attempts at forward regime detection specifically — all closed, none produced a working detector:**
- `Q-REGIME-AEGIS-1` (per `ops/instruments/6J.md` J6) — spot USDJPY trend-persistence flag tested directly against Aegis win/loss. **FALSIFIED** — per-trade AUC ≈ 0.499, indistinguishable from a coin flip.
- A broader regime-signal-battery effort and two further campaigns (2024 regime-shift accumulating-signal work; a regime-time-conditioned follow-up) — both closed with no promoted output.
- The synthesized, repo-wide lesson from this line of work: **the crux is detectability, not whether regimes exist.** Every attempt so far to build a real-time classifier that actually separates future win-probability by regime has failed; the *existence* of regime-dependent performance (measured after the fact, as in §1) has never been in doubt.

**Standing governance constraint, already in force:** per this repo's own overlay policy, no regime-based overlay may be built without going through the full INQHIORI investigation loop — this is explicit, existing doctrine, not a new gate this notice is proposing. The canonical cautionary worked example for exactly this failure mode (a plausible-looking macro/regime read used to justify a position-sizing overlay, without the discipline to first check whether the underlying signal was actually detectable and independent) is already documented in the `inqhiori` skill.

## §4 — Candidate mechanisms (informal, not investigated this session)

- **A — genuine shared macro regime.** A real, broad elevation in cross-asset tail risk during 2020–2023 (COVID + the 2022 policy-divergence/rate-shock period) that a sufficiently general market-state signal (realized volatility, cross-asset correlation, credit/liquidity proxies) could plausibly detect using data this repo can already reach (e.g., ES/MES realized vol, already flagged this session as a cheap, in-scope proxy).
- **B — selection/tuning-era artifact.** Every strategy examined was discovered or tuned using data that increasingly over-weights the calmer 2023+ regime relative to 2020–2023; some of the apparent "regime conditionality" could be an artifact of when discovery happened rather than a stable property of the market. Not ruled out; not tested.
- **C — the detectability wall may be domain-specific, not universal.** Prior detection attempts used a narrow, single-instrument trend/persistence flag (Q-REGIME-AEGIS-1). A cross-asset, volatility/liquidity-based signal is a genuinely different construction that has not been tried and is not automatically subject to the same failure.

## §5 — Routing decision

**HOLD.** Reason (operator-stated, this session): this deserves its own dedicated session — the scope (what kind of regime signal, which instruments, whether it becomes a hard gate or a soft sizing dial, how it interacts with the existing EV-vs-survival tradeoff discussion from earlier this session) is substantial enough to warrant deliberate scoping, not an in-session tangent. Not being built now.

## §6 — If HOLD: re-check trigger

- **Re-check date:** none set — operator-initiated, next dedicated session.
- **Trigger condition:** operator opens a session scoped to regime-awareness / overlay design.
- **Starting context that session should NOT have to re-derive:** (1) detectability, not existence, is the historically hard part — Q-REGIME-AEGIS-1's AUC≈0.499 result on the most direct prior attempt; (2) the full-INQHIORI-before-any-overlay policy is standing doctrine, not a fresh proposal; (3) the shared 2020–2023 failing window across four unrelated candidates (§1) is the concrete evidence base motivating the session, already assembled here rather than needing rediscovery.

**Forbidden moves, this notice:**
- Building any regime-detection code or overlay logic on the strength of this notice alone — it observes a pattern, it does not license a build.
- Treating "regimes exist" (already well-established, §1) as evidence that a detector is achievable — those are different claims; §3's prior failures bear on the harder one.
- Retroactively re-opening any specific closed candidate verdict (Aegis-6J1, ORB-MNQ-1, the CFD-era allocation ADR) on the basis of this notice alone.

---

## §10 — Audit hooks

```bash
# The CFD-era book's shared H1 failure this notice leans on hardest
grep -A3 "H1 2020-01" docs/adr/2026-05-23-allocation-refresh-2.md
# expect: bust 13.84%, p99 DD 7.76%, FAIL

# The prior detectability failure this notice cites
grep -n "Q-REGIME-AEGIS-1" ops/instruments/6J.md
# expect: J6, AUC ~0.499, FALSIFIED

# The standing overlay policy this notice does not propose to change
grep -n "No overlays without full INQHIORI" .claude/skills/inqhiori/SKILL.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/notes/notice/N-2026-08-28-regime-conditionality-cross-cutting-forward-item.md --type notice
# Ran 2026-08-28: RESULT NOT CHECKED — this repo-side check_brief.py subset does not
# model the 'notice' type contract (per-type template lives under
# .claude/skills/brief-authoring/references/, not modeled here). Structure was instead
# matched by hand against N-2026-08-15-nsurv-single-history-magnitude-blindspot.md.
```
