# Substrate Phase 6 — completion (docs + §10)

**Date:** 2026-08-23
**Owner ADR:** [`2026-07-22-challenge-era-substrate-retirement.md`](../../adr/2026-07-22-challenge-era-substrate-retirement.md)
**Plan:** [`2026-08-23-substrate-phase-6-implementation.md`](../../superpowers/plans/2026-08-23-substrate-phase-6-implementation.md)

**Phase 6 docs:** `DONE`
**Destroy offline rollback copy:** `NOT DONE` — operator confirmation only; this note does not destroy bytes.

Phases 1–5 remain as recorded on the owning ADR header (PRs #477 / #479 / #485 / #488 / #572; Phase 5 tombstone pruned — retrieve via the private archive / `git log --follow`). This note does not rewrite those bodies.

---

## §10 outcomes (this session, public clone @ `95fec61`)

| Hook | Result | Notes |
|---|---|---|
| `check_brief.py --type adr` | PASS (0 HARD / 0 WARN) | well-formed |
| `check_adr_graph.py` | PASS | A1, A2, A3, A4, A6 |
| `rg ACTIVE_FIRM` / `FIRM_RULES["FXIFY"]` / `calc_multiplier` / `get_multipliers` in active `*.py` | PASS as *no live selector* | Hits are comments, historical-module provenance, and tests asserting the names are **absent**. No `ACTIVE_FIRM =` assignment; no `def calc_multiplier`. |
| `rg PEPPERSTONE_PANELS` / `mc_anchor_pepperstone` / `requires_pepperstone` | PASS as *no live pin* | Comment / retired-script banners only |
| `rg tv_exports/oanda` / `_duka.csv` on manifest owners | PASS (empty) | |
| Forward invariants (`Tradeify_Select_100K`, `DD_TRIGGER` / `DD_SCALE` / `BASE_RISK`, `TIER_MULTIPLIER`) | PASS (present) | Values not restated here |
| `rg skipif.*Pepperstone` / `requires_pepperstone` under `tests/` | PASS (empty) | |
| `check_data_manifests.py` | PASS | Absent-tree WARN on gitignored vendor dirs (public-clone posture) |
| `check_boundaries.py` | PASS | |
| `check_path_liveness.py` | PASS | |
| `check_root_doc_liveness.py` | PASS | |
| `verify_lock_anchors.py` | PASS | `ROUTING: Closed` |
| `python scripts/gate_manifest.py --tier check` | PASS | Cheap `make check` subset. Pine WARN: no `.pine` on this clone |
| Targeted forward pytest (ADR §10 list) | PASS | 131 passed / 0.29s |
| Class-S §10 scripts at `lab/analysis/class_s_candidate1_scoring_2026-07-15/` | SKIPPED | Path gone (Great Prune). Not a Phase 1–5 selector defect — escalate only if a living consumer still required those bytes |
| Full `pytest tests/` | SKIPPED | Cheap-subset posture; targeted list + `--tier check` is the evidence this note claims |
| Destroy offline rollback copy | NOT RUN | Operator-gated; point of no return stays unmarked |

Raw captures: `/opt/cursor/artifacts/substrate-phase-6/section10_*.log` (agent workspace; not tracked).

---

## Root-doc pointers (Task 3)

Grep of `ACTIVE_FIRM`, `canonical CFD feed`, `Pepperstone/TV is the sole` on `README.md` / `REPO_MAP.md` / `PIPELINES.md` / `CLAUDE.md`:

- `CLAUDE.md` — standing-decision row already says the substrate is retired and there is no `ACTIVE_FIRM` selector. Left.
- `PIPELINES.md` — already says there is **no** canonical CFD feed; tombstones labeled pruned. Left.
- `README.md` / `REPO_MAP.md` — no hits. Left.

No living restatement of FXIFY-as-default or Pepperstone-as-canonical was found. Historical ADR bodies untouched.

---

## Point of no return

Unmarked. Destroying the Phase-0 offline rollback copy remains a distinct operator confirmation after this note. Git restores tracked manifests and code, not proprietary CSVs.
