# ADR — Admit a `"cme"` broker panel to `PANELS_BY_BROKER`, reviving `breadth.py` on canonical data

**Status:** `Accepted` — operator ratified 2026-08-19, in-session direct instruction ("I accept
docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md, and you can touch
core/mc/modes.py"); see Ratification note
**Decision date:** 2026-08-19
**Authors:** Joshua + Claude Code
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`2026-07-22-challenge-era-substrate-retirement.md`](2026-07-22-challenge-era-substrate-retirement.md)
disposition C (the ADR that emptied `PANELS_BY_BROKER` and left the "new panels require an admitting
ADR" gate this ADR clears) · [Stage-8 variance-dominance ADR](2026-07-20-stage8-variance-dominance-risk-neff-gate.md)
(the risk-N_eff mechanism this panel feeds) · [Q-COMPOSE-1 closure](../briefs/closures/Q-COMPOSE-1-closure-falsified.md)
(the falsified-composition lesson `breadth.py` encodes) · [design spec](../superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md)
(content of record — this ADR is a pointer-tier registration, per CLAUDE.md's "ADRs carry pointers
only, never a retelling")
**Layer:** infrastructure (data-registry admission, not a strategy/engine/allocation change)

---

## §0 — Rule 0 reads (this session, 2026-08-19)

- `core/mc/modes.py` — read in full around the registry definitions (lines 80–110). Confirmed
  verbatim: *"Broker panel registry — empty after substrate Phase 3 (ADR 2026-07-22 §2-C)... New
  panels require an admitting ADR + explicit registration here."* This is the gate this ADR clears.
  `PANELS_BY_BROKER`, `EXPECTED_SYMBOLS_BY_BROKER`, `EXPECTED_VERSIONS_BY_BROKER` are `Dict[str,
  Dict[str, ...]] = {}` — confirmed empty, confirmed generic (not Pepperstone-specific machinery).
  `STRATEGY_FILENAME_TOKEN` (lines 87–92) is already broker-agnostic and populated for all four
  strategy keys (`guardian`, `striker`, `aegis`, `striker_nas100`) — no change needed there.
- `docs/adr/2026-07-22-challenge-era-substrate-retirement.md` §2 disposition C — read in full.
  Confirmed this is the retiring ADR: it removed the Pepperstone-specific `PEPPERSTONE_PANELS`/
  `DEFAULT_PANEL` hardcoded contract and explicitly directed keeping `core/mc/` as "only a
  parameterized simulation library used by current firm scoring and research" — i.e. generic
  infrastructure, admitting new panels deliberately rather than by convenience. This ADR does not
  reverse or weaken that disposition; it uses the door that disposition left open.
- `docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md` — read in full this session
  (earlier in this session's design-spec work). Confirms `n_eff_risk_delta` (covariance-based) is the
  binding statistic for composition decisions, `n_eff_dependence_delta` (correlation-based) is
  explicitly non-binding context — the exact lesson Q-COMPOSE-1 paid for. This ADR's panel feeds that
  existing, unchanged mechanism; it does not alter the Stage-8 gate itself.
- `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md` — read in full this session. ORB-MNQ-1
  composed into the 2-leg MYM+MNQ book blew bust probability 2.65%→38.75% (Tradeify tier) on plain
  variance dominance (daily $std $438 vs. the book's $273), while dependence-N_eff read a flattering
  +0.96 and risk-N_eff stayed flat. Grounds why this ADR's baseline is scoped to the two `AUTHORIZED`
  legs only, not a naive 4-leg mirror of the retired CFD book.
- `docs/pursuits/b1-aegis-6j-transfer-lane.md` / `docs/pursuits/b8-guardian-mgc-transfer-lane.md` —
  read in full this session. Aegis (6J): `PARK`, expiring 2026-11-08. Guardian (MGC): `SUBTRACT`/DEAD,
  measured non-viable (bust 42.2/72.4/16.5% vs ≤3.0% ceiling). Neither belongs in a locked baseline.
- `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md` — read in full this session. Confirms
  Striker DJ30 (MYM) and Striker NAS100 (MNQ) remain `AUTHORIZED · MECHANISM @ 1.00×` — only
  *deployment* at Tradeify was withdrawn, parameters untouched.
- `core/data/tv_exports/cme/SHA256SUMS` and the private `first-passage-archive` remote (already
  configured as git remote `archive`, read without unarchiving — archived-repo state blocks writes,
  not reads) — read this session. Confirmed the canonical export for each admitted leg (see §2).
- `python scripts/check_data_manifests.py --check` — executed this session after landing the fresh
  MNQ export and copying the pre-existing 28 vendor CSVs into this worktree (they were absent from
  this specific git worktree, not from the repo's actual vendor-data state — copied from the
  operator's main checkout, same machine, same bytes, not fabricated). Result: clean, both non-empty
  `tv_exports/cme` entries verified; `bar_data`/`external` soft-degrade WARN (unrelated, pre-existing,
  zero files present in this worktree for those two trees).

---

## §1 — Context

`lab/research_utils/breadth.py` computes portfolio risk-breadth (`n_eff_risk`, the covariance-based
statistic Q-COMPOSE-1 and the Stage-8 ADR established as the one that actually predicts composed-book
bust) but has been dormant since the Pepperstone/CFD data it depended on was retired
(2026-07-22 disposition C; confirmed final retirement 2026-08-02,
`docs/adr/2026-08-02-pepperstone-feed-retirement.md`). Its `load_baseline_panel()` call fails today
with `PANELS_BY_BROKER` empty. The four locked strategies' CME-futures editions already have real,
manifested backtest data (`core/data/tv_exports/cme/SHA256SUMS`), and two of the four —
Striker DJ30 (MYM) and Striker NAS100 (MNQ) — remain `AUTHORIZED @ 1.00×`, the same 2-leg composition
Q-COMPOSE-1 itself used as its baseline. `PANELS_BY_BROKER` is a clean, deliberately-empty extension
point whose own governing comment requires exactly this: an admitting ADR before registration.

**Decision driver (one sentence):** a previously load-bearing, correctly-designed risk gate has no
working data source on canonical data, the data already exists and is already manifested, and the
registry that would revive it was deliberately left admission-gated rather than reopened by
convenience — this ADR is that admission.

---

## §2 — Decision

**Decision:** Admit a `"cme"` entry to `PANELS_BY_BROKER`, `EXPECTED_SYMBOLS_BY_BROKER`, and
`EXPECTED_VERSIONS_BY_BROKER` in `core/mc/modes.py`, scoped to the two `AUTHORIZED` futures legs only:

| Strategy key | Symbol | Canonical export | Provenance |
|---|---|---|---|
| `striker` | MYM | `core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-21_73182.csv` | Commit `7d80037`, "pin latest MYM strategy export" (verified in the private archive) |
| `striker_nas100` | MNQ | `core/data/tv_exports/cme/Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-08-19_3ad92.csv` | Fresh export, landed this session specifically because the only prior general-purpose MNQ export was ~6 weeks stale relative to MYM's pin — the four same-day 2026-07-17 MNQ files in the manifest are Q-RAIL-1 parity-evidence CSVs (`STEP2_PARITY.md`/`STEP3_1A/1B/1C.md`), not general strategy exports, confirmed via the archive; using one would be a category error |

**`guardian` and `aegis` keys are deliberately omitted from this panel entry**, not merely
unpopulated — Guardian (MGC) is `SUBTRACT`/DEAD (measured non-viable), Aegis (6J) is `PARK` (expiring
2026-11-08). Neither belongs in a locked composition baseline today. Either could still be *injected
as a candidate* via `breadth.py`'s existing 5th-column mechanism (same as ORB-MNQ-1 was) without
needing this admission — that is a separate, later use, not gated by this ADR.

This ADR does **not** touch `breadth.py` itself (its `load_baseline_panel(panel_name=...)` call
already works generically once the registry has a matching key — confirmed in §0), does not touch any
locked strategy parameter, `dd_protection` constant, or `firm_rules` allocation, and does not compose
any candidate into any live book. It registers a research-tooling data source only.

**Effective:** upon acceptance. First use: `python lab/research_utils/breadth.py --self-test --panel
cme`, which will establish a **fresh** anchor (a 2-leg CME panel) — not comparable to the retired
4-leg Pepperstone Q-NEFF-1 anchor (3.98 dependence / 3.09 risk). The fresh anchor number is not
predicted here; it will be recorded as a `breadth.py` self-test constant once measured, in a follow-up
commit, not guessed in this ADR.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Populate all four legs (mirror the old CFD 4-leg book) | Would include Guardian (measured non-viable) and Aegis (parked, expiring) as locked baseline legs — nonsensical; the whole reason Q-COMPOSE-1/Stage-8 matter is that *what's in the baseline* is load-bearing, not incidental. |
| Skip the ADR, register directly under Option E's "opt-in, no new mandatory gate" precedent | Ruled out on direct Rule-0 evidence, not a judgment call — `core/mc/modes.py`'s own comment is unambiguous: "New panels require an admitting ADR." Option E's lighter posture applied to `lab/discovery/` files that carry no such requirement; this file explicitly does. |
| Use the stale (2026-07-11) MNQ export rather than pulling fresh | Considered; rejected because MYM's own precedent (the 07-21 "pin latest" commit) establishes that this repo treats panel freshness as worth a fresh pull rather than shipping on a known-stale one when the gap is easily closed — and it was, same session. |
| Wait for a future, larger data-refresh initiative rather than a narrowly-scoped admission | Rejected — the gate this ADR clears blocks nothing else; a narrow, precisely-scoped admission is lower-ceremony and lower-risk than bundling this into a larger, undefined future effort. |

---

## §4 — Falsifier (revert trigger)

**H:** the CME-native 2-leg panel, once measured, produces a self-test that is internally consistent
(panel shape sane, `n_eff_risk ≤ n_eff_dependence` per the participation-ratio math's own invariant)
and, when ORB-MNQ-1 or any future composed candidate is injected, reproduces or is consistent with the
CFD-era Q-COMPOSE-1 finding's *qualitative* shape (variance dominance visible in the risk-N_eff
statistic) — i.e. the mechanism transfers to native data, it was not an artifact of the retired feed.

**Falsified if:** the self-test panel shape is inconsistent with the two admitted CSVs' own trade
counts/date ranges (a wiring defect), or a composed-candidate injection produces a risk-N_eff reading
that contradicts the CFD-era finding's direction without a data-quality explanation.

**Trigger check schedule:** at first real use of the panel (the self-test run, or the first candidate
injection, whichever comes first) — not a scheduled future date, since this is a mechanical
correctness check, not a behavioral hypothesis needing a data-accumulation window.

**Revert action:** if falsified, the panel registration is superseded (not silently edited) naming the
specific inconsistency; `breadth.py` itself is untouched either way, since the defect would be in the
registered data/paths, not in the already-anchor-tested computation.

---

## §5 — Forbidden moves

- **Registering Guardian or Aegis into this panel entry "since the data already exists."** Explicitly
  the tempting move this ADR's §2 rules out by name — data existing is not the same as the strategy
  being a valid baseline leg.
- **Treating this ADR as reopening any live-composition or deployment decision.** It registers a
  research data source. Whether any candidate is ever actually composed into a live book remains a
  fully separate, unaddressed-here decision (no live c1 book exists today regardless).
- **Silently updating this registration when a newer MYM/MNQ export lands later** without a dated
  Change History entry — the same discipline every other manifest-touching decision in this repo
  already carries.
- **Using this admission as precedent to skip the "admitting ADR" requirement for any future broker
  panel key** — this ADR admits exactly one key (`"cme"`), scoped exactly as stated in §2; a future
  panel needs its own ADR, not a citation of this one.

---

## §6 — Consequences

**Positive:** revives a previously load-bearing, correctly-designed risk mechanism using canonical
data, with near-zero implementation surface (`breadth.py` needs no code change at all — confirmed in
§0). Closes the gap between "the mechanism is right" (Stage-8 ADR) and "the mechanism has no working
inputs" (this session's finding).

**Negative (real cost):** one more registered data dependency to keep fresh — if MYM or MNQ get a
materially newer export in the future, this registration should be updated (see §5's forbidden move
on doing so silently).

**Risks:** the fresh anchor number is unmeasured at authoring time; §4's falsifier is the mechanism
for catching a wiring or data-quality defect at first real use, not a promise the anchor will look any
particular way.

**Downstream artifacts (on acceptance):**
- `core/mc/modes.py` — the three-dict registration (mechanical, ~6 lines).
- `docs/superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md` — §7 open items 1
  and 2 both close (canonical exports resolved; ADR question resolved yes) — Change History entry
  added there, ratified body of this ADR stays untouched per the same convention every other ADR in
  this repo uses.
- `breadth.py`'s self-test anchor constants — updated in a small follow-up commit once the fresh
  2-leg number is actually measured (not part of this ADR's own diff).

---

## §7 — Implementation plan

- **Phase 0** — this ADR; re-verify §0 anchors at ratification time if more than a session elapses.
- **Phase 1** — on acceptance, register the three dict entries in `core/mc/modes.py` per §2's table.
- **Phase 2** — run `python lab/research_utils/breadth.py --self-test --panel cme`; record the
  resulting anchor as a new named constant (not overwriting `NEFF_DEPENDENCE_ANCHOR`/
  `NEFF_RISK_ANCHOR`, which remain the historical 4-leg Pepperstone record).
- **Phase 3** — design spec Change History update; STATE.md pointer line.

---

## §10 — Audit hooks (runnable)

```bash
# Registry actually populated, scoped to exactly the two AUTHORIZED legs:
python -c "import sys; sys.path.insert(0,'core'); from mc.modes import PANELS_BY_BROKER; print(sorted(PANELS_BY_BROKER.get('cme', {}).keys()))"
# Expected: ['striker', 'striker_nas100'] -- NOT guardian, NOT aegis

# breadth.py needed no code change:
git diff <pre-this-ADR-commit>..HEAD -- lab/research_utils/breadth.py
# Expected: empty

# Manifest still clean:
python scripts/check_data_manifests.py --check
# Expected: exit 0 (or the pre-existing, unrelated bar_data/external soft-degrade WARN only)

# Self-test runs and produces a real number (not a crash):
python lab/research_utils/breadth.py --self-test --panel cme
```

---

## Ratification note

**Ratified by:** Joshua, in-session direct instruction — *"I accept
docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md, and you can touch
core/mc/modes.py while we wait for Stage 2 to land"* (2026-08-19). Authority channel: explicit owner
adjudication.

**Two real corrections found during implementation, both against this ADR's own §2 table as
originally drafted — recorded here per §5's own discipline against silent amendment, not applied
silently:**

1. **MYM export corrected.** §2's table originally cited `2026-07-21_73182.csv` (the commit-labeled
   "latest MYM strategy export"). Measured at implementation time: 343 days' trade-date span, well
   under the 4-year floor `core/mc/ingest.py::load_trades`'s own `assert_window` enforces. "Latest
   pinned" turned out to mean a short recency-check re-export, not a full backtest. Corrected to
   `2026-07-11_15d8b.csv` (measured: 2020-01-14→2026-06-30, 2359 days, 534 rows) — the longer of two
   same-span exports 3 days apart, verified by direct measurement of every candidate MYM file in the
   manifest, not assumed.
2. **`breadth.py` needed code changes after all.** §0/§6 originally stated "`breadth.py` needs no
   code change at all." Falsified at implementation time: `load_baseline_panel`'s call to
   `lib.mvd.assert_tv_export` requires the strict OANDA/Pepperstone 7-field filename pattern, which
   no CME export in the manifest actually follows (verified: Guardian's export has 9
   underscore-delimited fields, Striker DJ30's has 9 in a different shape, Striker NAS100's has 8
   with no version token, Aegis's carries parentheses/hyphens — no single alternate pattern to add
   either). Fixed with a lighter, CME-appropriate identity check (`breadth._assert_cme_export` —
   confirms strategy/symbol tokens appear in the filename, no position, no field count) used only on
   the `"cme"` panel path; the strict OANDA-shaped check is untouched for every other panel.
   `_self_test` was also made panel-aware (a `_SELF_TEST_ANCHORS` table keyed by panel name), since
   the alternative — leaving it hard-coded to the 4-leg Pepperstone anchor — would report `FAIL` on a
   working 2-leg panel forever.

**Neither correction changes §2's actual decision** (admit `"cme"`, scoped to the two `AUTHORIZED`
legs, Guardian/Aegis excluded) — both are implementation-fidelity fixes, found by measuring rather
than assuming, the same discipline this ADR's own §0 already modeled.

**First real measurement (2026-08-19):** `python lab/research_utils/breadth.py --self-test --panel
cme` → `n_bdays=1711 n_blocks=341, N_eff dependence=1.9988, N_eff risk=1.0871, ENB=1.9994` → `PASS`
against the newly-recorded `cme` anchor (§4's first falsifier limb — `n_eff_risk ≤ n_eff_dependence`
— holds: 1.0871 ≤ 1.9988). §4's second limb (candidate-injection consistency with the Q-COMPOSE-1
qualitative finding) is untested — no candidate has been injected yet; not blocking on acceptance.

**§6 downstream sweep, this commit:** `core/mc/modes.py` registration (with the corrected MYM path)
· `breadth.py`'s CME identity-check fix and panel-aware self-test anchors (both beyond this ADR's
original stated scope, recorded above rather than silently expanded into) · design spec Change
History entry · STATE.md pointer line.

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md --type adr
python scripts/check_adr_graph.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-19 | Initial authoring — drafted after discovering `core/mc/modes.py`'s own "admitting ADR" requirement mid-implementation of the design spec's Stage 1 (a course-correction from that spec's earlier, incorrect "leaning toward no ADR needed" §7 note). Rule-0 grounded against the retiring ADR, the Stage-8 ADR, Q-COMPOSE-1, the two transfer-lane pursuit records, and this session's own archive-verified canonical-export findings. Status `Proposed` — awaiting operator ratification. | Claude Code (drafted at operator request, mid-Stage-1 build) |
| 2026-08-19 | Ratified `Proposed` → `Accepted` (operator in-session instruction). §6 downstream applied same commit: `core/mc/modes.py` registration, `breadth.py` CME identity-check fix + panel-aware self-test, design spec Change History, STATE.md pointer. Two implementation-time corrections against §2's original table recorded in the Ratification note (MYM export swapped to a genuinely long-history file; `breadth.py` needed a real code fix, not zero changes as originally stated) — measured and documented, not silently applied. First real self-test measurement recorded: `n_eff_dependence=1.9988, n_eff_risk=1.0871` on `n_bdays=1711/n_blocks=341`. | Joshua (ratification + go on `core/mc/modes.py`) + Claude Code (implementation, correction, recording) |
