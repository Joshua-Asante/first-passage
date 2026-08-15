# Audit follow-up — §5.4 gate-denominated closure annotation sweep

**Audit ID:** AUDIT-2026-07-11-core-fxify-anchoring §5.4
**Date:** 2026-07-15
**Triggered by:** remaining open item from [`2026-07-11-core-fxify-anchoring-audit.md`](2026-07-11-core-fxify-anchoring-audit.md) (§5.4 / §2 re-scope principle)
**Authors:** Cursor Cloud Agent (this session)
**Scope:** claims-inventory of research *closures* whose §6 verdict rests on challenge-gate numbers (pass/bust % / p99 DD lock floors / median days-to-pass). One-line annotations only — **no** re-adjudication, **no** constant/parameter edit, **no** rejection-registry reopen.
**Method:** Rule-0 inventory of on-disk closure briefs under `docs/ltm/briefs/` + `docs/briefs/`; classify by whether the *verdict trigger* quotes challenge survival criteria vs panel-level grounds (edge / cost-law / regime structure / signal AUC). Parent principle (audit §2):

> a closure whose *verdict* rests on challenge-gate numbers (pass/bust %) gets a one-line annotation "gate-denominated; directional/panel-level finding survives"; closures on panel-level grounds (edge, cost-law, regime) stand unmodified. Rejection registry re-proposal bars stand everywhere.

**Related:** [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](../../../adr/2026-07-11-challenge-era-claims-rescope.md) (executes §5.1/§5.3/§5.5; D1 discharged 2026-07-15; this note discharges §5.4).

---

## §1 — Annotated (gate-denominated)

| Closure | Verdict (unchanged) | Why gate-denominated | What survives (directional / panel) |
|---|---|---|---|
| [`Q-SWAP-1-closure-falsified.md`](../../../ltm/briefs/Q-SWAP-1-closure-falsified.md) | FALSIFIED | Δbust / Δp99 vs challenge MC thresholds | M-SWAP-1: implied-1R absorbs overnight swap as size reduction |
| [`Q-SWAP-2-closure-ambiguous.md`](../../../ltm/briefs/Q-SWAP-2-closure-ambiguous.md) | AMBIGUOUS-HOLD | Δp99 lock-margin vs bust<1% / p99<5% | Fixed-1R swap moves p99 into the pre-reg AMBIGUOUS band (wrong instrument) |
| [`Q-SWAP-3-closure-ambiguous.md`](../../../ltm/briefs/Q-SWAP-3-closure-ambiguous.md) | AMBIGUOUS-HOLD | full-panel p99/bust/median floors + regime gate | Full-panel clearance is H2-driven; H1 structural risk unchanged by allocation cuts |
| [`Q-SWAP-4-closure-ambiguous.md`](../../../ltm/briefs/Q-SWAP-4-closure-ambiguous.md) | AMBIGUOUS-HOLD | same headline floors | Pine overnight-hold shrink ≠ H1/H2 asymmetry cure |
| [`Q-DDTRIG-1-closure-hold.md`](../../../ltm/briefs/Q-DDTRIG-1-closure-hold.md) | RESOLVED — HOLD | regime-robustness bust<1% / p99<5% | No static DD_TRIGGER makes 2020–23 chop half regime-robust |
| [`Q-REGIME-ADAPT-1-closure-falsified.md`](../../../ltm/briefs/Q-REGIME-ADAPT-1-closure-falsified.md) | FALSIFIED-T2b | H1 bust<1% / p99<5% / median≤45d | VIX>20 binary brake fires on wrong days; worse than unconditional k≈0.55 |

Annotation stamp (identical prefix on each file):

> **2026-07-15 · AUDIT-2026-07-11 §5.4:** gate-denominated; directional/panel-level finding survives. …

**Archival (not rewritten — bytes live only under `pre-prune-2026-06-05`):** Q-DDP-1 recommendation (`archive/docs/briefs/Q-DDP-1/recommendation.md`) — verdict was gate-denominated (C2 passed full-panel lock criteria / failed regime gate). Its operational consequence is already re-scoped via the C2 ADR + this audit's §5.1 (pass-time grounds void; constants frozen). No archive edit.

**ADRs (out of §5.4 "research closures" scope; already handled by §5.1/§5.3):**
- [`2026-05-08-dd-trigger-c2-relock.md`](../../../adr/2026-05-08-dd-trigger-c2-relock.md) — pass-time + lock-gate grounds
- [`2026-05-14-allocation-refresh.md`](../../../adr/2026-05-14-allocation-refresh.md) / [`2026-05-23-allocation-refresh-2.md`](../../../adr/2026-05-23-allocation-refresh-2.md) — challenge-era lock anchors
- [`2026-06-07-decompound-remc-hold.md`](../../../adr/2026-06-07-decompound-remc-hold.md) — uses bust/p99 as characterization; HOLD + regime-split finding already listed keep-class (K6); limb-2 stays LIVE as mechanism property under the rescope

---

## §2 — Unmodified (panel-level / non-challenge verdict)

Sampled closures whose §6 trigger is edge, cost-law, regime *structure*, signal AUC, dependence, or premise-moot — **not** challenge pass/bust as the verdict currency. Left byte-unchanged:

| Closure | Verdict grounds (why unmodified) |
|---|---|
| `Q-REGIME-1-closure-falsified-structural.md` | z-score on H1↔H2 p99 *spread* as structural-regime test (panel-temporal) |
| `Q-REGIME-OOS-1` / `POSTCOVID` / `RATEVOL` / `AEGIS` | detector AUC / payoff arms |
| `Q-INCUMBENT-REGIME-1-closure-resolved.md` | per-leg PF / meanR half-panel |
| `Q-NEFF-1-closure-resolved-benign.md` | cross-leg correlation / N_eff |
| `Q-PERSIST-1-closure-moot.md` | already-answered persistence premium on decompound panel |
| `Q-DECAY-1-closure-scope-split.md` | decay-detector vs drawdown (not challenge MC) |
| `Q-SFRISK-1-closure-resolved.md` | successor self-funded T1 (post-rescope) |
| edge/cost/ORB/ICT/BTC/Aegis-6J BEPAD closures | edge / cost-law / transfer falsifiers |
| discovery closures (DISC-CAMP-0, HARV-0, GATECART, KBUDGET, JOINT-TAIL-WEEKLY) | DSR/K / reachability / panel-shape — not FXIFY challenge pass |

---

## §3 — Rejection-registry check

[`docs/rejected_candidates.md`](../../../rejected_candidates.md) read in full this session.

- **Re-opens:** **zero.** Venue retirement / claim re-scope is explicitly **not** new mechanism evidence (audit K7; rescope ADR §5).
- **Stamp:** dated confirmation block added under the registry header pointing at this note.
- Entry classes remain edge-failure / venue-cost / SNAG-closed / soft-shelved as authored — none rewritten.

---

## §4 — Disposition

**§5.4 DONE.** Six closures annotated; rejection registry confirmed standfast; no `core/` / allocation / `dd_protection` / Pine / test-pin touch.

Parent audit §5 slate after this session: §5.1 ✓ · §5.2 ✓ (D1 via Q-SFRISK-1, 2026-07-15) · §5.3 ✓ · §5.4 ✓ · §5.5 ✓. Remaining from the 07-11 audit's broader board (not §5): D2 calibration re-derivation at the 2026-08-08 review.

---

## §10 — Audit hooks

```bash
# Annotations landed
rg --no-ignore -n 'AUDIT-2026-07-11 §5.4' docs/ltm/briefs/Q-SWAP-*-closure-*.md \
  docs/ltm/briefs/Q-DDTRIG-1-closure-hold.md \
  docs/ltm/briefs/Q-REGIME-ADAPT-1-closure-falsified.md
# Expected: 6 files, one stamp each

# Rejection registry standfast stamp
rg -n '§5.4 confirmation' docs/rejected_candidates.md

# Parent audit marks §5.4 DONE
rg -n '§5.4.*DONE' docs/notes/audits/programme-audit/2026-07-11-core-fxify-anchoring-audit.md

# No executable core delta from this sweep
git diff --stat origin/main -- core/
# Expected: empty
```
