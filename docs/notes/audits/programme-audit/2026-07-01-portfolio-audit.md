# Audit Note — Object-layer (portfolio) programme audit, full seven diagnostics

**Audit ID:** AUDIT-2026-07-01-portfolio
**Date:** 2026-07-01
**Triggered by:** degeneration-signal triggers, not calendar — the window contains a hard-core-adjacent execution failure (29–30 Jun tilt), three venue/feed retirements, and a dense run of null/falsified research loops (SNAG signal #5). Last portfolio audit: 2026-05-12.
**Authors:** Joshua (operator) + Claude Code (this session)
**Scope:** object layer — the 4-strategy locked portfolio, allocations, `dd_protection`, MC anchors, feeds, venues, firm deployments, and empirical market findings. All seven diagnostics.
**Window:** **2026-05-27 → 2026-07-01** (operator-specified "past 5 weeks"; ~378 non-merge commits). Precision note carried from verification: the current locked risk values (DJ30 0.70%, NAS100 0.37%) and the 99.83/0.17/4.37 anchor pins were established 2026-05-23/24 — *pre-window*; within this window they are byte-stable. `dd_protection` C2 constants stable since 2026-05-08.
**Method:** same workflow as the meta note (`wf_1daea9d2-09f`): evidence sweeps → per-diagnostic agents → adversarial verifier per diagnostic (one re-run standalone) → completeness critic → gap-filler pass. Evidence assembled and verified before verdicts.
**Layer discipline:** no conclusion below cites methodology-audit verdicts. Research-loop *outcomes* are the empirical evidence this layer owns.
**Environment note:** the audit worktree lacks gitignored vendor CSVs and Pine bytes (expected); anchor values were verified as pinned source text + committed artifacts, not recomputed. Anchor tests: 2 passed / 4 skipped; `validate_params` 0 HARD / 1 expected WARN.

---

## §0 — Source anchors (Phase-0 reads / Rule 0)

Read at on-disk-byte fidelity 2026-07-01, worktree `nervous-williams-a3c130`, HEAD `9402ee5`. Rule-0 production reads done directly (constants below verified on disk, not from docs):

- `core/dd_protection.py:52-53,63-68` — DD_TRIGGER 0.015 / DD_SCALE 0.40; BASE_RISK 0.0034/0.0070/0.0150/0.0037.
- `core/firm_rules.py:93,112` — `ACTIVE_FIRM="FXIFY"`; `_BASE_RISK` identical to lock; additive Bulenox tiers (`5bd5f31`).
- `tests/test_mc_anchors.py:75-77,91-92,123-124` — anchor pins 0.9983/0.0017/0.0437 (abs 1e-4), panel 1141/227, lock gates bust<1%/p99<5%. Rerun this audit: 2 passed / 4 skipped (vendor data absent — expected). `scripts/validate_params.py`: 0 HARD / 1 expected WARN.
- `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` (`20857d3`) — read in full this session; the #1 exhibit.
- `docs/adr/2026-06-07-decompound-remc-hold.md` (+ 2026-06-25 addendum, `efeda82`) and `docs/adr/2026-05-23-allocation-refresh-2.md` (`5b8ff71`) — falsifier texts for #7, re-read at cited lines by the re-run verifier.
- `lab/archive/futures_prop_hold_compat_2026-06-30/RESULTS.md` (`428dc93`), `lab/archive/bulenox_futures_remc_2026-07-01/NOTES.md` (`5bd5f31`), `lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_cleanvintage_2026-06-25.md` (`efeda82`), `lab/archive/timeframe_5m_2026-06-25/RESULTS.md` (`ec3fb6b`) — pivot/HOLD/5m evidence artifacts.
- `docs/SESSIONS.md` (window entries) + `docs/rejected_candidates.md` (11 in-window entries) + retirement ADRs `6f2f468` (Dukascopy) / `9b60ad2` (OANDA) — belt-churn and loop-census bases.
- Live scheduler + `ops/sentinel/` (`e4ba36f`) — verified by the #7 re-run: cron `fwd-quarterly-regime-ddrevert` enabled, next 2026-08-08; sentinel slate pinned with unremediated precondition findings.

**Failure class:** degeneration-signal-triggered portfolio diagnostic (execution-layer failure + venue retirements + SNAG signal), not calendar ceremony.

---

## §3 — Diagnostic evidence (assembled and verified before §4)

### #1 Hard core integrity — YELLOW (verify: 3 CONFIRMED, 1 WEAKENED→restated)

**Parameter/code core intact; execution-layer commitment violated (repeatedly); repair sound in design, unverified in fact.**

- On-disk verification: `core/dd_protection.py:52-53` DD_TRIGGER 0.015 / DD_SCALE 0.40; `BASE_RISK` 0.0034/0.0070/0.0150/0.0037; `firm_rules.py` identical, `ACTIVE_FIRM="FXIFY"`; `tests/test_mc_anchors.py:75-77` pins 0.9983/0.0017/0.0437 with lock-criteria gate bust<1%/p99<5%. **Restated per verification:** risk values byte-stable in-window (last governed change 2026-05-23, pre-window); Pine manifest changed in-window only via governed additive commits (05-28 8-hash re-pin; 06-01 default-OFF DJ30 day-stop toggle, M-13 cross-check installed). **Zero ungoverned changes found.**
- **The 29–30 Jun tilt was a hard-core violation at the execution layer:** six manual fills, net −$4,188.85, 100% OFF-SPEC against FILTERED/flat systems; 29 Jun size ~8× the strategy's own sanity tripwire. The ≥4th recurrence of the logged discretionary pattern (Feb-2026; 4/14, 4/16, 5/20 off-spec trades per `regime_fit_2026-06-17/RESULTS.md`). Off-spec execution severs live results from the anchor's per-spec premise — the anchor was becoming live-unfalsifiable.
- **Repair** (`2026-06-30-no-manual-trading-cfd-retirement.md`): structural role-removal, non-gameable §4 revert (manual returns only via a ratio that cannot accrue while manual is stopped), costs named honestly. But it is ~1 day old with zero verification window, enforcement is policy-only, and the idle FXIFY account remains credential-accessible. Residual tilt risk is relocated to the go-dark interval, not eliminated.
- Futures-pivot code preserved lock discipline: `5bd5f31` additive (0 deletions in `firm_rules.py`; keyword-only FXIFY-byte-identical defaults; TDD boundary tests); anchor-non-transfer to any Guardian-less prop subset explicitly pre-registered as requiring re-MC.

### #2 Belt churn balance — GREEN (verify: 4/4 CONFIRMED)

**ADD 7 / PRUNE 5 / REJECTED-pre-install 11** (counts granularity-sensitive ±2; line-count churn strongly net-negative). Prunes delete real code: Dukascopy −760 lines, OANDA −561, Notion ingest −5,396; plus CFD/manual venue retirement (docs-level) and Silver MC dumps archived. Dominant adds are venue-migration replacements (bust_trailing engine, Bulenox tiers, force-flat transform, bar-export v0.2, NAS100 v0.2 panel). Rejection-before-install dominates installation 11:7. **Direction: migration, not accumulation.**

Watch items: (a) the Dukascopy prune closed pre-registered measurement Q-FEED-1 unrun ("executive decision, recorded" — the ADR admits the measurement would inform a decision already made); (b) single-feed posture removes independent-corroboration capacity behind a passive falsifier; (c) orphaned adds — three CBOE external panels whose consumer (regime-signal battery) closed NULL, and the **shadow gold gate** (gap-filler pass): a twice-falsified signal (Q-REGIME-OOS-1, Q-REGIME-POSTCOVID-1) still ships as a logs-only instrument whose pre-registered kill tripwire keys on DEPLOY actions that shadow mode never emits (**structurally unfireable**), whose README acknowledges neither falsification, and whose weekly logging lapsed 2026-06-17. Retained by explicit brief decision ("stays FROZEN + SHADOW + CLOSED"), so not a quiet violation — but an unmaintained ops surface.

### #3 Progressive evidence — YELLOW (verify: 3 CONFIRMED, 1 WEAKENED)

Real predicted-then-corroborated results exist, several risky:

- **Q-INCUMBENT-REGIME-1 (flagship):** verdict bands + priors recorded before data access; all four locked incumbents cleared the H1-chop bar that rejected every challenger (PF 1.32/1.84/1.88/1.82); Guardian — pre-recorded most-likely-FAIL — cleared by 0.02. RESOLVED-EXONERATED. (Prereg is same-commit self-attested; hash placeholder unfilled.)
- **Anchor stability:** 99.83/0.17/4.37 reproduced byte-identical under the firm-constants refactor (585 tests); N1 ORB anchor re-pinned STABLE on the fresh v0.2 panel; the decompound regime-*split* held on the clean single-file vintage (H1 bust 13.84% vs H2 0.21%) while severity was honestly corrected 2.92→1.47%.
- Guardian v5.5 parity port §4: net diff 0.46%, PF 1.76%, 51/52 entries exact — labeled RESOLVED-POSITIVE though strictly failing its own trade-count-EXACT arm (51≠52); ECR post-deploy re-measure CLEAN.
- **Downgraded per verification (may not headline):** Q-REGIME-FIT-1's "+17.12% INSIDE the envelope" — ~6 of its 9 weeks (including the cluster carrying 81% of the edge) sit inside the very panel that re-pinned the envelope; only ~3.5 weeks are genuinely forward, and INSIDE-a-99.83%-envelope is a low-severity test.

**The structural fact driving yellow: the corroboration channel has narrowed to near-zero going forward.** The headline live prediction (99.83%-pass / 26d median) was forfeited untested (FXIFY idle); zero live flow since 06-30; the futures venue's validating re-MCs are vendor-data-blocked; the OANDA cross-feed is retired, so forward corroboration is single-feed signal-level only until the automation chain is live.

### #4 Degeneration evidence — GREEN (verify: 3 CONFIRMED, 1 WEAKENED)

- **The regime-caveat HOLD is evidenced, not rationalized:** it followed a de-risk sweep whose candidates were rejected by the *pre-existing* regime-robustness gate (k=0.55 → H1 bust 8.89%; DD_SCALE→0.20 → 13.50%; robust k≈0.25 unviable at 367–591d median); it adopted a *worse-looking* canonical risk picture; §4 carries binary dated falsifiers; §5 forbids loosening. The 2026-06-25 clean-vintage correction was triggered by an independent loop, softened the number, and the operator recorded HOLD-ROBUST/both-gates-still-breach rather than exploiting it (verification note: its prereg landed same-commit as results — the discipline claim is self-attested; the arithmetic left nothing to exploit regardless).
- **The venue pivot is not a belt-patch to rescue the automation premise:** the jurisdiction chain (EA parity PASS → OANDA US forex-only → TV→TradersPost→Tradovate the only US-legal automated chain → FXIFY rejects futures master → pivot) pre-dates the tilt ADR by 1–2 days on contemporaneous commits. The tilt drove only the no-manual rule; CFD retirement follows structurally. Post-pivot adverse findings were surfaced, not suppressed: Guardian BLOCKED (46.4% multi-day holds); "a prop book that drops it is a different portfolio… must be re-MC'd before it can claim the anchor"; Bulenox consistency rule = SERIOUS THROTTLE; integer-contract re-MC named the go-live gate.
- **Watch:** 2026-08-08 is the HOLD's first trigger execution — the machinery is still unexercised on this ADR; the pivot's validating re-MCs are owed — **any live futures deployment claiming the 99.83 anchor without them flips this verdict.**

### #5 Boundary respected — GREEN (verify: 3 CONFIRMED, 1 WEAKENED→restated)

One explicit, contained registry crossing (Silver — graded at the meta layer; object-side fact: never reached the live book, `_BASE_RISK` has 4 keys, registry entry intact). BTC futures reopen was a principled venue-class re-test, closed at Phase 0 with the bar raised. USOIL threads show dedup discipline (mechanism-distinct, declared collisions, PARK dated). No overlay on physical/narrative facts (only deployed instrument is the watch-only shadow gate; VIX-brake falsified, not deployed). **Restated per verification:** "no locked parameter changed" holds *for this window* (the 05-14/05-23 re-locks are pre-window and were ADR-governed); **zero quiet changes** is the accurate universal. The one attempted book change (NAS100 ORB 5th leg) was withdrawn same-day by its own pre-committed falsifier.

### #6 Theory-comparison — GREEN (verify: 4/4 CONFIRMED)

- **15m vs 5m:** adversarially tested under commit-ordered pre-registration; 5m unanimous HURTS (portfolio re-MC 85.79/14.21/7.99 vs 99.83/0.17/4.37; Striker pyramid engines collapse). 15m vindicated by direct comparison, not incumbency.
- **HOLD vs de-risk:** on the cleaner 2026-06-25 vintage the rejected candidates *still fail* H1 (2.81%/4.94% bust ≥1%) while the HOLD's breach softened — subsequent evidence favored the chosen option; the one reopen condition is dated (2026-08-08), not suppressed. Honest residual: the locked config itself fails H1 (13.84%) — "least-bad viable."
- **Single-feed vs two-tier:** revert trigger not fired through 07-01; prior evidence (OANDA DOW feed artifacts) favored the chosen feed. Two-edged: the DOW artifact was caught *by* the cross-check being retired; the ADR names that lost capacity as the real cost. Window short (~1wk).
- **Futures vs CFD:** structurally forced; outcome evidence **PENDING** — zero live trades, go-live gates not run. If the Bulenox re-MC fails when data lands, this becomes a genuine open comparison.

### #7 Falsifier check — YELLOW, re-based (verify re-run: 4/4 CONFIRMED; one caveat REFUTED and struck)

| Falsifier | Status |
|---|---|
| dd_protection C2 (0.015 / 0.40×) + C0-revert (<95% ×2 windows) | **INTACT** (values + text + `time_to_pass.py --regime-check` path) |
| MC anchor pins (0.9983/0.0017/0.0437, abs 1e-4; gates bust<1%/p99<5%) | **INTACT** (triple-agreement enforced by `verify_lock_anchors.py`; exercised only where vendor data exists) |
| 2026-05-23 ADR §Falsifier limb 1 (MC <95% ×2) | **INTACT** |
| 2026-05-23 ADR limbs 2–3 (DJ30/NAS100 live edge-captured <0.70, ≥30 post-lock trades) | **DORMANT-UNACKNOWLEDGED** — unaccruable since the 2026-06-30 CFD retirement; **NAS100's limb was dark from birth** (zero verified fills ever); DJ30's is permanently unbindable on its stated instrument (venue now MYM force-flat-modified). No document maps the retirement onto these limbs, while the 06-30 ADR flags exactly this failure class for its own metric. Material: these limbs are half of the named "dual retroactive catch-paths" compensating for that lock's skipped regime-robustness gate. |
| Decompound-HOLD §4 limb 1 (≥2 live DD-attributed failures / 6mo) | **Same dormancy pattern** (no live challenges exist) |
| Decompound-HOLD §4 limb 2 (quarterly trailing-6mo p99≥5% OR bust≥1%; next 2026-08-08) | **INTACT + mechanically scheduled** — live cron `fwd-quarterly-regime-ddrevert` verified enabled (next run 2026-08-08) + committed sentinel with the slate as a pinned regression fixture. The diagnostic's "no mechanical reminder exists" caveat is **struck** as refuted. Runnable post-retirement (consumes TV panel exports, not live fills). |
| Sentinel precondition findings for the 08-08 slate | **Unremediated 38 days out** — `regime_calendar.md` [M]/[L] rows; Rule-2 trip-log <2 rows; Action-routed since 2026-06-23, no action taken. (Audit-side inputs; the MC trigger itself is not blocked.) |
| Guardian decay gate (M=60/20, 0.50× WATCH, dwell 40) | **NEWLY-INSTALLED, unratified** delegation defaults; dormancy silently went from ~14 months to **indefinite** (Guardian lost all live venues 5 days after the build); README never updated. |
| STATE.md Q-NAS-ECR-1 precondition | Still gated on "first verified Copygram→DXTrade fill" — an event now impossible. |

**Zero DRIFTED findings anywhere.** Supersession discipline exercised twice in-window (two ADRs killed by their own falsifiers).

---

## §4 — Proposed disposition (PROPOSED — pending owner ratification)

**Object layer: PROPOSED STABLE — with one structural watch flag that all three yellows share.**

Grades: #1 yellow · #2 green · #3 yellow · #4 green · #5 green · #6 green · #7 yellow.

Not Degenerating: no post-hoc patching, active real-code pruning, rejection-dominant intake, boundaries held, zero falsifier drift, and the window's decisions (HOLD, pivot) are evidenced with named costs. Not Progressive: the in-window corroborations are real but the strongest one is an exoneration (a gate-pass, not a new lever), the headline live prediction was forfeited untested, and the forward corroboration channel is structurally narrowed.

**The shared structural fact behind all three yellows (#1, #3, #7): the programme's contact with live reality has gone dark.** Execution-layer integrity is repaired on paper but unverified; live corroboration is near-zero until the futures chain runs; the live halves of two lock-decision falsifier sets are dormant un-acknowledged. Simultaneously, the loop record shows the *empirical search space* the layer has been mining is exhausted: in-window terminal dispositions run ≈33 negative (18 FALSIFIED, 13 NULL, 2 NO-GO) vs 10 positive — and the positives are exonerations, gate-passes, and instruments, not new levers. Consecutive-negative streaks at window end: **5th-leg/expansion ≈17–22 closures, 0 admissions (past SNAG threshold, domain closure NOT formalized)**; regime-detection 9 (operator SNAG-closed 07-01); within-strategy-alpha 6–7 (closed by designed synthesis); external-sourcing 0/69 (exhausted-NULL).

STABLE is therefore conditional on the §5 re-arm actions: a Stable verdict with a darkening falsifier surface degrades to un-falsifiable — which is how degeneration starts *without* any of the seven signals firing.

---

## §5 — Spawned follow-ups (named actions)

1. **Falsifier back-propagation for retirement events** (resolves the #2-green vs #7-yellow tension as one finding): when a venue/feed/operator-role retires, sweep standing ADR falsifiers for limbs referencing the retired surface; annotate each dormant limb with a dated re-arm condition. Apply retroactively now to: 2026-05-23 ADR limbs 2–3; decompound-HOLD §4 limb 1; Guardian decay-gate README; STATE.md Q-NAS-ECR-1 precondition; gold-gate tripwire. Owner: CC drafts, operator ratifies. One session.
2. **Restore falsifiability (critical path):** land vendor CSVs in the working environment → run the Bulenox force-flat re-MC + integer-contract re-MC (the two named go-live gates) → firm/automation confirmation → chain build. Owner: operator (data export) then CC. Target: before 2026-08-08.
3. **Formal domain-level SNAG closure for 5th-leg/expansion** (and pin the within-strategy-alpha synthesis as closed): registry-grade entry with re-proposal bar = exogenous/paid data or a genuinely new venue class. Owner: operator ratifies; CC authors. One session.
4. **2026-08-08 slate readiness:** remediate the sentinel's own Action items (regime calendar [M]/[L]; trip-log inputs) ≥1 week before the date; confirm `time_to_pass.py --regime-check` runs on a fresh panel export.
5. **Go-dark behavioral tripwire:** a weekly mechanical zero-fills attestation on the idle DXTrade account (export → assert 0 fills → log) until it lapses; consider removing stored credentials. Converts the policy-only repair into a monitored one. Owner: operator.
6. **Orphan disposal:** shadow gold gate — retire it or re-scope its tripwire to something that can fire in shadow mode, and update its README with the two falsifications; CBOE panels — annotate retained-for or remove from manifests.

---

## §7 — Programme-audit signal check (this layer)

- [ ] Belt-patches without independent corroboration? **No** (#4).
- [ ] Belt only grows? **No** — prune-dominant (#2).
- [~] Falsifier thresholds drifting? **No drift; but two limb-sets dormant un-acknowledged** (#7) — repair action §5.1.
- [ ] Invoked to rationalize? **No** (#4: HOLD and pivot both evidenced).
- [x] **SNAG pattern? YES** — 5th-leg/expansion past threshold without formal domain closure; regime-detection SNAG-closed correctly. Repair action §5.3.
- [ ] Cross-layer contamination? One meta-citation inside an object answer caught by verification and excluded here.
- [~] Negative heuristic crossed without repair? Silver crossing contained but paperwork owed (tracked at the meta layer).

---

## §10 — Audit hooks (runnable at next cycle)

```bash
# Falsifier limb dormancy acknowledged?
grep -n "unaccruable\|dormant\|re-arm" docs/adr/2026-05-23-allocation-refresh-2.md docs/adr/2026-06-07-decompound-remc-hold.md
# Re-arm progress: did the go-live gates run?
ls lab/analysis/bulenox_futures_remc_2026-07-01/  # expect RESULTS with real numbers, not NOTES-only
# 08-08 slate executed?
grep -n "2026-08-08" docs/SESSIONS.md | head -5
# Domain closure formalized?
grep -n "5th-leg\|expansion" docs/rejected_candidates.md docs/methodology/rejected_signals.md
# Zero-fills attestation running?
grep -rn "zero-fills\|0 fills" ops/ docs/SESSIONS.md | head -5
# Constants still pinned
python scripts/verify_lock_anchors.py   # expect ROUTING: Closed
```

---

## §11 — Closure

- **Status:** `Closed (evidence assembled and adversarially verified; PROPOSED verdict pending owner ratification; follow-ups §5 spawned)`
- **Verdict:** object layer **PROPOSED STABLE**, conditional on the §5 falsifier re-arm actions; SNAG repair (§5.3) is mandatory under signal #5.
- Companion artifacts: meta-layer completion note + cross-layer synthesis (same date, this directory).
