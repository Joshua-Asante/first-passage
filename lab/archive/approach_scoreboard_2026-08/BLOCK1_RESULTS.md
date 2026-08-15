# Q-SCORE-1 Block 1 — freeze results

**Status:** H_A FALSIFIED · 2026-08-11 · $0 · K=0
**PREREG:** [PREREG.md](PREREG.md) · **Map:** [RETRO_MAP.md](RETRO_MAP.md)
**Design:** docs/superpowers/specs/2026-08-11-approach-scoreboard-design.md (RATIFIED; PR #743)

## §1 Closed: coverage (PREREG F3 grammar)

```json
{
  "n_closures": 53,
  "n_with_closed": 38,
  "n_without_closed": 15,
  "date_coverage": 0.7169811320754716,
  "without_closed": [
    "2026-07-27-hermes-agent-adoption-closure-resolved.md",
    "MNQBASE-1-closure-intake-dry.md",
    "Q-6JCOMPOSE-1-closure-void-unexecutable.md",
    "Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md",
    "Q-ICT-1-closure-moot.md",
    "Q-JOINT-TAIL-WEEKLY-closure-retired.md",
    "Q-KBUDGET-1-axis-reachability-screen.md",
    "Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md",
    "Q-MCLTAS-1-closure-falsified.md",
    "Q-TNEC-CON-3-closure-ambiguous-hold.md",
    "Q-TNEC-CON-4-closure-ambiguous-hold.md",
    "Q-TNEC-CON-5-closure-ambiguous-hold.md",
    "Q-TNEC-ENV-1-closure.md",
    "Q-USOIL-1-closure-subtract.md",
    "ST-EH-1-closure-operator-stopped.md"
  ],
  "without_closed_grandfathered": [
    "2026-07-27-hermes-agent-adoption-closure-resolved.md",
    "Q-6JCOMPOSE-1-closure-void-unexecutable.md",
    "Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md",
    "Q-ICT-1-closure-moot.md",
    "Q-JOINT-TAIL-WEEKLY-closure-retired.md",
    "Q-KBUDGET-1-axis-reachability-screen.md",
    "Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md",
    "ST-EH-1-closure-operator-stopped.md"
  ],
  "without_closed_recent": [
    "MNQBASE-1-closure-intake-dry.md",
    "Q-MCLTAS-1-closure-falsified.md",
    "Q-TNEC-CON-3-closure-ambiguous-hold.md",
    "Q-TNEC-CON-4-closure-ambiguous-hold.md",
    "Q-TNEC-CON-5-closure-ambiguous-hold.md",
    "Q-TNEC-ENV-1-closure.md",
    "Q-USOIL-1-closure-subtract.md"
  ],
  "grandfather_concentration": "recent-spread"
}
```

**Grandfather-concentration sub-question (design §12 item 2):**
**recent-spread** — 7 of 15 undated closures (46.7% ≥ 40%) are **not** in `GRANDFATHERED` (MNQBASE-1, Q-MCLTAS-1, Q-TNEC-CON-3/4/5, Q-TNEC-ENV-1, Q-USOIL-1). The other 8/15 are grandfathered pre-ADR names. Forward coverage is not healthy: recent closures still ship without F3 `Closed:` (explore-record aliases on CON-3/4/5; `Date:` on MNQBASE; prose `Closed: PARKED…` on USOIL; missing header on ENV-1/MCLTAS). The forward `Lane:`/`Closed:` template amendment is **urgent**, not merely a retro-map convenience. Design-time cited 13/50 (74%); HEAD verify under the same F3 grammar is 15/53 (71.7%) after PR #745's coverage-backlog stubs — bar not loosened.

Near-miss patterns observed (labeled; do NOT count toward H_A):
- `Closed (explore record):` — Q-TNEC-CON-3-closure-ambiguous-hold.md, Q-TNEC-CON-4-closure-ambiguous-hold.md, Q-TNEC-CON-5-closure-ambiguous-hold.md
- `Date:` / verdict-embedded dates — MNQBASE-1-closure-intake-dry.md, Q-6JCOMPOSE-1-closure-void-unexecutable.md, Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md
- `Status: … closed YYYY-MM-DD` prose — ST-EH-1-closure-operator-stopped.md
- `**Closed:** PARKED …` non-date grammar — Q-USOIL-1-closure-subtract.md

## §2 Retro-map assignability

| limb | n | % of closures |
|---|---:|---:|
| machine Closed: | 38 | 71.7% |
| lane ≠ UNASSIGNED | 50 | 94.3% |
| verdict token present | 53 | 100% |
| **assignable (all three)** | **37** | **69.8%** |

**H_A: FALSIFIED <80%** — bar not loosened (design §3). Date limb alone (71.7%) is already under the bar; lane mapping is not the bottleneck (3 UNASSIGNED: Q-ICT-1, Q-ICT-CASCADE-1, Q-JOINT-TAIL-WEEKLY).

## §3 What this does NOT establish

1. No lane is closed, watched, or level-changed by this freeze — Signal columns are Block 2.
2. The retro-map is one-time; re-tuning it after seeing streaks is forbidden.
3. Git-date fallbacks are disclosure only.
4. H_B is unscored here.

## §4 Gate to next

H_A FALSIFIED → continue Task 6 — residue + closure; Block 2 gated off.
