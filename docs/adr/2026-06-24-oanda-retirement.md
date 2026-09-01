# ADR 2026-06-24 — Retire OANDA entirely; Pepperstone/TV BAR EXPORT is the sole canonical feed

**Status:** Accepted (operator executive decision, recorded)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - frozen OANDA CSV retention clause only (§2(c) "the 4 panel CSVs … stay manifest-pinned"). API deletion, cross-feed-tier collapse, and single-tier canonical feed stand.
**Superseded-in-part-by:** `2026-08-02-pepperstone-feed-retirement.md` - the "Pepperstone/TV is the sole canonical feed" consequence only; there is now no canonical CFD feed and the live canonical family is CME futures TV exports.
**Retain-until:** none
**Decision date:** 2026-06-24
**Authors:** Joshua (decision) + Claude Code (recorder, this session)
**Supersedes:** none directly. **Extends** `docs/adr/2026-06-17-dukascopy-retirement.md` — that ADR §2 explicitly scoped `scripts/fetch_oanda_bars.py` (OANDA) "out of scope and untouched"; this ADR completes the arc to a single canonical feed family. **Retires** the two-tier-canonical methodology (memory `feedback_two_tier_canonical_pepperstone_oanda`).
**Related:** `docs/spec/2026-06-24-oanda-retirement-design.md` (design) + `docs/spec/2026-06-24-oanda-retirement-plan.md` (implementation plan, executed this session).
**Layer:** infrastructure (R&D + live data-acquisition layer) + methodology (the two-tier→single-tier validation-posture change).

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring (this session, 2026-06-24, worktree `claude/festive-neumann-289a93`); anchors are the origin/main content state read, plus the commit on this branch that changed each:

- `core/lib/oanda.py` — anchor `dd4e4aa` (2026-06-06). The OANDA REST wrapper (`fetch_candles` paginated M15 candles; `account_summary` live NAV; oandapyV20; practice/live host from account-ID prefix). **Deleted this session in `0f128b4`.**
- `ops/cli.py` — read (origin/main); `_fetch_oanda_balance` + `--from-oanda` was the only OANDA live consumer in ops (firm=="OANDA" + creds-match gated). **Edited (path removed) in `0f128b4`.**
- `core/portfolio_mc.py` — anchor `4331e65` (2026-06-06). Held `OANDA_PANELS` / `PANELS_BY_BROKER["oanda"]` / `--panel oanda` / the per-broker EXPECTED_* dicts; the Pepperstone headline is computed at `DEFAULT_PANEL="pepperstone"` independently of OANDA (traced `compute_default_config → _load_all`). **Edited in `784a9ab`.**
- `scripts/verify_lock_anchors.py` — anchor `74ef32c` (2026-06-24). Parsed both panels' CLAUDE.md headlines + `[mc_anchor_*]` + test pins; OANDA absence in params would route **Action** unless the script drops OANDA. **Edited (Pepperstone-only) in `784a9ab`.**
- `core/config/params.toml` — read (origin/main); `[mc_anchor_oanda]` was the manifest pin the verifier compared. **Deleted that section in `784a9ab`.**
- `CLAUDE.md` — read (origin/main); MC anchor block carried the "OANDA proxy 99.85%" line + vendor-data restore note "OANDA bars still via `fetch_oanda_bars.py`". **Edited in `784a9ab`.**
- `ops/regime_gate/gold_gate_shadow.py` — read; reads cached `core/data/bar_data/XAUUSD.csv` (NOT the OANDA API at runtime); its skip-message named the deleted fetch script. **Comment repointed in `789be8e`.**
- `docs/adr/2026-06-17-dukascopy-retirement.md` — anchor `6f2f468` (2026-06-17). The precedent + the source of the "OANDA out of scope" scope statement this ADR extends.

---

## §1 — Context

OANDA entered the repo as a **programmatic data source** (a REST API with deep M15 history and live-NAV access) — the convenient feed when no broker-fidelity export pipeline existed. It came to wear two hats: (A) the REST API (`lib.oanda` bars + `account_summary`, `scripts/fetch_oanda_bars.py`, `cli.py --from-oanda`), and (B) a **cross-feed validation tier** — a second-broker TV-export panel in `portfolio_mc.py` (`--panel oanda`), the "OANDA proxy" anchor in `CLAUDE.md`, and the two-tier-canonical methodology (OANDA findings could drive Action; Pepperstone validated in TV). The 2026-06-17 Dukascopy retirement established that the operator prefers **one canonical, interpretable, broker-fidelity bar family** (the TV/Pepperstone BAR EXPORT v0.1 pipeline) and is willing to accept the loss of an independent second feed; that ADR deliberately scoped OANDA out as "a different feed." The operator now extends the same decision to OANDA: the BAR EXPORT pipeline "works better for our purposes," so OANDA's data-source role is fully superseded, and its cross-feed validation role — which only existed because a second feed existed — is retired with it. This connects to standing doctrine: the TV-CSV-canonical-feed policy (2026-06-12), the Dukascopy retirement (2026-06-17), and the parity-gate lesson (feed-source + PF≈1 calibration).

**Decision driver (one sentence):** the operator standardizes on one canonical broker-fidelity feed (Pepperstone/TV BAR EXPORT) and the cross-feed validation tier cannot stand once the second feed it compared against is gone — so the two-tier→single-tier posture must be recorded now, not left as an orphaned `--panel oanda` path and a stale "OANDA proxy" anchor.

---

## §2 — Decision

**Decision:** OANDA is retired entirely. (a) The OANDA REST API and its consumers are **deleted** (`core/lib/oanda.py`, `core/lib/oanda_creds.py`, `scripts/fetch_oanda_bars.py`, `ops/cli.py --from-oanda`, and the tests `test_oanda.py` / `test_oanda_gate.py` / `test_fetch_oanda_bars.py`). (b) The cross-feed validation tier is **collapsed to single-feed**: `OANDA_PANELS` / `PANELS_BY_BROKER["oanda"]` / `--panel oanda`, the `[mc_anchor_oanda]` manifest section, the OANDA anchor test pins + verifier parsing, and the `CLAUDE.md` "OANDA proxy" line are removed; Pepperstone/TV is the sole canonical feed. (c) OANDA data + closed lab investigations are **frozen as historical**: the 4 panel CSVs under `core/data/tv_exports/oanda/` stay manifest-pinned, `lab/analysis/oanda_stage1/` + the `mc_anchor_evolution` overlay get retirement banners and are kept. (d) The **two-tier-canonical methodology** (OANDA proxy / Pepperstone validates) is retired to **single-tier**.

**Effective:** immediately upon acceptance (code landed this session, branch `claude/festive-neumann-289a93`, commits `0f128b4`→`b5fd5fa`).
**Scope:** all bar-data acquisition, MC validation, and live-NAV reads from this date onward. Existing closed verdicts are not reopened; the frozen OANDA CSVs are retained as manifest-pinned historical provenance, not regenerated. The canonical Pepperstone headline (99.83/0.17/4.37) is **unchanged** — it was always computed independently of OANDA, so no re-MC is performed.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Retire the API only; keep the OANDA panel as a frozen cross-check** (`--panel oanda` runnable) | Leaves the two-tier methodology + a second-feed equivalence argument standing on a feed the operator has decided to stop maintaining. The cross-check's value (independent corroboration) did not justify the carrying cost of a second panel family + the proxy/validate methodology — the same trade the Dukascopy retirement already resolved toward one feed. |
| **Deprecate-in-place** (keep `lib.oanda` as a `NotImplementedError` shim) | Does not satisfy "retire entirely"; leaves dead code and a creds path. No benefit over deletion given the replacement producer (`bar_export_loader`) already exists and is canonical. |
| **Delete the OANDA data + closed lab too** (no freeze) | Loses reproducibility of historical anchors and the closed-investigation record; the cost (a few KB of frozen, manifest-pinned CSVs + comment banners) is trivial versus the audit-trail value. Operator chose freeze-as-historical. |
| **Status quo — no decision** | Leaves an orphaned `--panel oanda` path, a stale "OANDA proxy" headline in `CLAUDE.md`, a live `fetch_oanda_bars.py` that the Dukascopy ADR's restore note points at, and a two-tier methodology resting on a feed the operator has decided to abandon. Contradictory governance on the books; worse than recording the disposition. |

---

## §4 — Falsifier (revert trigger)

This ADR accepts a real cost (§6): the loss of the independent OANDA second-feed cross-check. The accepted posture is single-feed (Pepperstone/TV broker-fidelity), with the cross-feed concern managed by the operator's TradingView-side validation before any code/lock change.

**Revert trigger (binary):** if a **pre-registered** lock or allocation decision materially depends on an **independent second-feed corroboration** that the single Pepperstone/TV feed structurally cannot provide — concretely, a dated decision whose §0/§Falsifier names a cross-feed agreement check (e.g. "the verdict holds only if a second broker's panel reproduces it within band") and that check cannot be run because no second feed exists — then the single-feed posture is reopened with that dated decision as the anchor.

**Revert action:** supersede this ADR with a fresh one re-evaluating a second feed (OANDA REST, a different broker's TV export, or another programmatic source) as the cross-feed validation tier. Never edit §4 in place (Known Trap #12) — if the trigger is wrong, supersede.

**Trigger check schedule:** event-driven (at the moment such a decision is pre-registered and cannot assemble its cross-feed check); and reviewed at each quarterly programme audit (next **2026-08-08**, aligned with the standing regime trigger).

---

## §5 — Forbidden moves (under this ADR)

- **Re-introducing a programmatic broker feed (OANDA REST or another) by convention without an ADR** — OANDA's original presence was un-ADR'd convenience; that is exactly what this retirement + the Dukascopy retirement exist to prevent recurring. A second feed returns only via the §4 revert trigger or a fresh Pre-Q, not by quietly re-adding an adapter or a `--panel <broker>` key.
- **Citing the frozen `core/data/tv_exports/oanda/*.csv` as canonical-fresh** — they are frozen historical provenance, not a live feed. Using them to back a new verdict re-introduces the retired feed through the back door.
- **Loosening the §4 trigger after a single-feed limitation proves inconvenient** — "we wished we had a second feed, so we lowered the bar to bring OANDA back" is `p`-hacking at the methodology layer. The inconvenience IS the trigger; fire it openly (supersede), do not edit §4.
- **Re-proposing "keep the OANDA panel as a frozen cross-check" (§3 alternative) without new mechanism evidence** — that alternative is ruled out for a stated reason (carrying cost > corroboration value); reviving it requires evidence invalidating that reason, not renewed second-feed nostalgia.
- **Silently overwriting the canonical Pepperstone anchor with any OANDA-derived number** — the headline is Pepperstone-only; the frozen OANDA overlay is historical and must stay labeled as such in `mc_anchor_evolution`.

---

## §6 — Consequences

**Positive consequences:**
- One canonical, interpretable, broker-fidelity feed family (Pepperstone/TV BAR EXPORT) — no per-analysis "is this second feed equivalent enough?" argument; the methodology is single-tier.
- Three fewer maintained code paths (REST adapter + creds loader + bars fetcher) and one fewer optional dependency (`oandapyV20`).
- Governance is consistent: no orphaned `--panel oanda`, no stale "OANDA proxy" headline, no Dukascopy-restore-note pointing at a feed that is itself now retired.
- The retirement is purely subtractive — the canonical Pepperstone headline is unchanged (no re-MC), verified by `verify_lock_anchors` routing **Closed** and `PANELS_BY_BROKER == {"pepperstone"}`.

**Negative consequences (real cost):**
- Loss of the independent OANDA second-feed cross-check. Cross-feed corroboration now happens only via the operator's TradingView-side validation, not a second programmatic panel. Accepted, with the §4 falsifier as the safety valve.
- Live-NAV reads for any `firm="OANDA"` account fall back to manual balance entry (`--from-oanda` removed). OANDA is not a configured firm in `firm_rules.py`, so this affects only an ad-hoc manually-tracked OANDA account, if any.

**Risks (probabilistic):**
- The gold-gate shadow's feed (`core/data/bar_data/XAUUSD.csv`) was historically OANDA-fetched. **Mitigation:** the cached CSV still serves the (non-binding, shadow) gate; going forward it re-sources from `scripts/parse_bar_export.py --symbol XAUUSD`. The skip-message comment was repointed accordingly. No runtime breakage (the gate reads a cached CSV, not the API).

**Downstream artifacts that need updating (all done this session):**
- `core/portfolio_mc.py`, `core/config/params.toml`, `scripts/verify_lock_anchors.py`, `tests/test_mc_anchors.py`, `tests/test_verify_lock_anchors.py`, `CLAUDE.md` (anchor block + prose) — commit `784a9ab`.
- `ops/cli.py` + 3 deleted tests + deleted API/creds/fetch — commit `0f128b4`.
- `lab/analysis/oanda_stage1/*`, `docs/analytics/mc_anchor_evolution/README.md` — commit `78c07d4`.
- `pyproject.toml`, `ops/regime_gate/gold_gate_shadow.py`, `.gitignore` — commit `789be8e`.
- `README.md`, `REPO_MAP.md`, `docs/operational_rules.md` — commit `b5fd5fa`.
- `docs/SESSIONS.md` (this session entry) — this commit.
- Memory (outside repo): `feedback_two_tier_canonical_pepperstone_oanda` → single-tier; `reference_oanda_credentials` → tombstone; `MEMORY.md` index.
- **Skill files (out of scope — operator follow-up via skill-authoring path):** `fxify-challenge`, `trade-csv-reconcile` (+ `baselines.md`, `reconcile.py`), `inqhiori`, `live-execution-journal` (+ `journal_review.py`), `code-defect-debugging`. On-disk `SKILL.md` edits do not persist (memory `feedback_skill_amendments_via_authoring_path`).

---

## §7 — Implementation plan

Executed this session per `docs/spec/2026-06-24-oanda-retirement-plan.md` (Tasks 0–8, branch `claude/festive-neumann-289a93`):

- **Phase 0** — §0 reads verified; baseline green (495 passed / 14 skipped, `verify_lock_anchors` Closed, `check_boundaries` OK).
- **Phase 1** — delete REST API + tests + `--from-oanda` (Task 1, `0f128b4`).
- **Phase 2** — atomic cross-feed-tier collapse (Task 2, `784a9ab`): portfolio_mc + params.toml + verifier + 2 anchor tests + CLAUDE.md, committed together (test-import + verifier-Action couplings forced atomicity).
- **Phase 3** — freeze lab + analytics (`78c07d4`); standalone consequence files (`789be8e`); docs prose (`b5fd5fa`).
- **Phase 4** — this ADR + `SESSIONS.md`; memory updates; the §7 verification gate (`make validate`, full suite, grep sweep).
- **Operator follow-up** — skill-authoring-path edits for the 6 skill files (§6); optional gold-gate XAUUSD re-source via `parse_bar_export.py`; delete `~/.keys/oanda.txt`.

---

## §10 — Audit hooks (runnable)

```bash
# No live OANDA API code remains (only frozen lab banners + frozen records + this ADR)
grep -rin "lib.oanda\|oanda_creds\|fetch_oanda_bars\|--from-oanda\|--panel oanda\|account_summary\|fetch_candles" --include=*.py . | grep -v "lab/analysis/"
# Expected: empty (no live importer of the deleted API outside frozen lab dirs)

# No live reference to the removed MC constructs
grep -rin "mc_anchor_oanda\|OANDA_PANELS\|requires_oanda\|test_oanda_anchor" --include=*.py --include=*.toml .
# Expected: empty

# Lock-anchor verification stays Closed (proves the single-feed verifier is consistent)
python scripts/verify_lock_anchors.py
# Expected: ROUTING: Closed (exit 0)

# Single-feed panel set
python -c "import sys; sys.path.insert(0,'core'); import portfolio_mc; print(list(portfolio_mc.PANELS_BY_BROKER))"
# Expected: ['pepperstone']

# Frozen lab carries the retirement banner
grep -rl "OANDA retired 2026-06-24\|OANDA Stage-1 investigation frozen 2026-06-24" lab/analysis/oanda_stage1/ | sort
# Expected: the 8 oanda_stage1 files

# Full gate
python scripts/check_boundaries.py && make validate

# §4 trigger reminder — next programme audit / regime check: 2026-08-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-06-24-oanda-retirement.md --type adr
# Expected: all 6 checks PASS

# Production-source verification (§0 anchors)
git log -1 --format='%h' origin/main -- core/portfolio_mc.py     # 4331e65
git log -1 --format='%h' origin/main -- scripts/verify_lock_anchors.py  # 74ef32c
git log -1 --format='%h' -- docs/adr/2026-06-17-dukascopy-retirement.md # 6f2f468

# Extends-chain integrity
grep -n "scoped .*OANDA.*out of scope\|untouched" docs/adr/2026-06-17-dukascopy-retirement.md
grep -n "Extends" docs/adr/2026-06-24-oanda-retirement.md
```

---

## Addendum 2026-09-01 -- gold_gate_shadow.py mitigation target deleted (diagnostic only)

§0 and §6 of this ADR name `ops/regime_gate/gold_gate_shadow.py` as the one live consumer of an
OANDA-sourced cached feed (`core/data/bar_data/XAUUSD.csv`) and record the mitigation that it
"re-sources from `scripts/parse_bar_export.py --symbol XAUUSD`" going forward. That file (plus its
README and `ops/data/gold_gate_shadow_log.csv`) no longer exists: the shadow gate itself was
independently falsified and discontinued 2026-07-01 (gold KER/TSMOM signal inverted out-of-sample
twice -- Q-REGIME-OOS-1, Q-REGIME-POSTCOVID-1; unrelated to OANDA or this ADR), then formally
`git rm`'d 2026-07-11 by `docs/adr/2026-07-11-ops-cfd-estate-retirement.md`, which folded the
OOS-falsification finding into `docs/rejected_candidates.md`. That ADR does not cite or supersede
this one -- the deletion is incidental to this ADR's subject, not a reversal of the OANDA-retirement
decision.

This ADR's core decision (OANDA retired entirely; the single-canonical-feed posture, itself later
partially superseded 2026-08-02 to CME futures -- already correctly flagged via the existing
`Superseded-in-part-by` field) is unaffected and was re-verified 2026-09-01: no live
`lib.oanda`/`--panel oanda`/`mc_anchor_oanda` references outside frozen `lab/archive/oanda_stage1/`;
`verify_lock_anchors.py` still routes Closed; `oandapyV20` is absent from `pyproject.toml`.
`core/portfolio_mc.py`'s panel set is now `['cme']` rather than the `['pepperstone']` the §10
audit-hook comment still names as "Expected" -- that shift is the already-documented
pepperstone-retirement partial supersession, not new drift; only the hook's literal comment text is
cosmetically stale.

**Operator call (not resolved here):** whether the gold-gate deletion is worth a formal header edge
at all -- it is a downstream mitigation detail going stale for a reason wholly unrelated to this
ADR's subject (feed retirement) rather than a partial reversal of the decision, so the case for a
graph edge is weaker than the paired Dukascopy ADR's feed_loader.py finding. Default: leave as a
diagnostic addendum only.

**Ruling (direct operator instruction, 2026-09-01): confirmed, no formal graph edge.** This matches
the addendum's own default -- the gold-gate deletion is an unrelated downstream mitigation detail,
not a partial reversal of this ADR's decision. No further action needed.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-24 | Initial authoring + acceptance (operator executive decision) | Joshua + Claude Code |
| 2026-09-01 | Addendum: gold_gate_shadow.py mitigation target deleted (diagnostic only, unrelated retirement) | Claude Code (ADR-corpus reconciliation sweep) |
