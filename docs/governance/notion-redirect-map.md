# Notion Redirect Map

**Created:** 2026-06-13 — Notion Phase-2 migration, per [`docs/adr/2026-06-12-notion-surface-retirement.md`](../adr/2026-06-12-notion-surface-retirement.md) §2.6.
**Purpose:** resolve every retired Notion page-ID to its repo home, archive path, or successor — so dead IDs in
memory, briefs, and the canon's `[LEGACY-NOTION]` tags never become silent drift sources (forbidden move #4).

**Format:** `notion-page-id → REPO:path | ARCHIVED-AT:path | SUPERSEDED-BY:path | DEAD (404) → resolution`.
The Notion workspace is FROZEN (read-only) under Phase 1 and **cold-archived** under Phase 3
(executed 2026-08-10 — Addendum on the retirement ADR; **workspace not deleted**). IDs may still
dereference there as historical / rollback reserve; **repo paths in this map are the read authority**.
LTM export bodies under `docs/ltm/notes/archive/notion/` were removed from the working tree in the
Great Prune T1 pass — recover via `git show pre-prune-2026-08-08:<path>`.

## Structural / hub pages

- `288dc0b53c118010afaac75a0be2dd52` — Trading Plan (root) → REPO:docs/ltm/notes/archive/notion/ (children individually mapped; root itself not exported)
- `32cdc0b53c1181b8a18cce1401a4f8e8` — Command Center → ARCHIVED-AT:docs/ltm/notes/archive/notion/command-center.md (current state: REPO:CLAUDE.md + STATE.md)
- `358dc0b53c11814f8b70c95fd25ec906` — Dev-phase archive → ARCHIVED-AT:docs/ltm/notes/archive/notion/dev-phase-archive.md
- `35cdc0b53c11819e86fbf4658ab88278` — Framework references → ARCHIVED-AT:docs/ltm/notes/archive/notion/framework-references.md

## Methodology canon (now repo-canonical)

- `34ddc0b53c1181479d7bdecc61f47078` — INQHIORI canon (D-S-A pre-Q gate) → REPO:docs/methodology/inqhiori-canon.md  *(memory #8, #24)*
- `361dc0b53c1181138eccf03074d05486` — Methodology Canon (hub) → ARCHIVED-AT:docs/methodology/archive/notion/methodology-canon.md; LoR §3.5 now SUPERSEDED-BY:docs/adr/2026-06-12-three-loop-methodology-binding.md  *(memory #16)*

## `[LEGACY-NOTION]` tags from inqhiori-canon.md (all 7)

- `34cdc0b53c11812d96f8f6e9ee500d5e` — INQHIORI v1 (reference) → ARCHIVED-AT:docs/methodology/archive/notion/inqhiori-v1-investigation-framework.md
- `34ddc0b53c11811eb6a0d9192b63d252` — The Algorithm (reference) → ARCHIVED-AT:docs/methodology/archive/notion/the-algorithm.md
- `34cdc0b53c11812cbb4ff637ba44736e` — Rule 1 — Small-cell variance prior → ARCHIVED-AT:docs/methodology/archive/notion/rule-1-small-cell-variance-prior.md
- `34bdc0b53c1181fe9dc3fd93eadf3e8e` — Iran-Hormuz overlay deactivation (hard lesson) → DEAD (404, 2026-06-13) → REPO-HISTORY:`git show pre-prune-2026-06-05:archive/docs/methodology/archive/overlays/guardian_conflict_risk.md`; summary in inqhiori-canon.md §7 + methodology-canon.md §5
- `357dc0b53c118124a3ddf811d1d50745` — Reflect — Striker NAS100 v1 dual-loop closure → DEAD (404, 2026-06-13) → SUPERSEDED-BY:inqhiori-canon.md §9 (closure summary) + core/strategies LOCK record
- `346dc0b53c11816085bbf2292be934cc` — 2026-04-17 risk-control incident chain → DEAD (404, 2026-06-13) → SUPERSEDED-BY:docs/adr/2026-04-17-dd-trigger-calibration.md + docs/adr/2026-04-17-equity-tier-deletion.md
- `34ddc0b53c1181199976c9b1b4effb17` — CC brief: 1R diagnosis + Notice-phase compression (first INQHIORI test case) → DEAD (404, 2026-06-13) → SUPERSEDED-BY:docs/methodology/observation_routing.md + docs/methodology/archive/notion/the-algorithm.md (worked example)

## Command Center current-state pages (§2.4 verified MATCH vs repo)

- `35cdc0b53c1181f2be51c8a8f0078046` — Strategy Lock Reference → ARCHIVED-AT:docs/ltm/notes/archive/notion/strategy-lock-reference.md; CANONICAL:core/strategies/*/{*.pine,LOCK.md} + docs/adr/2026-05-23-allocation-refresh-2.md  *(memory #5)*
- `35cdc0b53c11813e82fdf5f09f36a459` — Portfolio MC Lock Details → ARCHIVED-AT:docs/ltm/notes/archive/notion/portfolio-mc-lock-details.md; CANONICAL:CLAUDE.md + tests/core/test_mc_anchors.py  *(memory #2, #9)*
- `35cdc0b53c11814d8985d778a92b640f` — Per-Firm Broker Matrix → ARCHIVED-AT:docs/ltm/notes/archive/notion/per-firm-broker-matrix.md; CANONICAL:core/config/params.toml
- `35cdc0b53c11812dbdd1e84b7e37693f` — Operating Procedures → ARCHIVED-AT:docs/ltm/notes/archive/notion/operating-procedures.md; CANONICAL:docs/operational_rules.md + docs/rule_0.md
- `35bdc0b53c118175b9eacf4d26c5e1e8` — Weekly Schedule v1.0 (Locked 2026-05-09) → REPO:CLAUDE.md (schedule mirrored in command-center.md); BULK-EXPORT pending (Joshua native)

## Loop records / investigations

- `361dc0b53c11812d838be99fc1f7734f` — Execution Reconciliation Apr13–May14 → ARCHIVED-AT:docs/ltm/notes/archive/notion/execution-reconciliation-apr13-may14-2026.md
- `36ddc0b53c11818ba799d9522280ed9a` — Q-JOINT-TAIL-WEEKLY (OPEN) → REPO:docs/briefs/2026-05-27-q-joint-tail-weekly-pre-q.md (roster: docs/briefs/INDEX.md); snapshot docs/ltm/notes/archive/notion/q-joint-tail-weekly.md  *(memory #13)*
- `367dc0b53c11816eb4ded6ea231cbb8a` — Q-PRECOND-1 (closed FALSIFIED) → BULK-EXPORT pending (Joshua native); roster: docs/briefs/INDEX.md
- `36ddc0b53c1181c481f4f164c2d7f722` — Q-JOINT-TAIL-1 (closed BLOCKED-RETIRED) → BULK-EXPORT pending (Joshua native); roster: docs/briefs/INDEX.md
- `372dc0b53c1181cca132ecb973886cfc` — Execution Review Week 2026-05-25 → BULK-EXPORT pending (Joshua native) → docs/ltm/notes/archive/notion/
- `367dc0b53c11811a8944f4159ee32e11` — Q-PRECOND-1 OANDA Data Quality & Backfill Log → BULK-EXPORT pending (Joshua native)

## Daily Execution System — databases & behavioral pages (NATIVE CSV/MD export — §0.5-Q2)

- `a1614cd86569477a81fb111264bb53e4` — Trade Journal [DB] → NATIVE-CSV → lab/data/behavioral_archive/trade_journal.csv
- `df731a855e1d41e0aa9966355ed11b5a` — Pre-Trade Log [DB] → NATIVE-CSV → lab/data/behavioral_archive/pre_trade_log.csv (schema in README)
- `0875d626e4444e90988bd339ddad2ea6` — Operational Risk Register [DB] → NATIVE-CSV → lab/data/behavioral_archive/operational_risk_register.csv
- `da7c42365a334970984fcae9b04173eb` — Replication Health [DB] → NATIVE-CSV → lab/data/behavioral_archive/replication_health.csv
- `35bdc0b53c1181bd8b66d7882bb9b5e5` — Morning Anchor — Standard → BULK-EXPORT (behavioral/Action-Library) → lab/data/behavioral_archive/ (md)
- `35bdc0b53c118195a5bdd4278ab5e916` — Evening Wrap → BULK-EXPORT (behavioral/Action-Library)
- `35bdc0b53c118102a60ad1779ab68821` — Sunday Review Sub 2 (Edge Captured + Behavioral) → BULK-EXPORT (behavioral/Action-Library)
- `35bdc0b53c1181a985f7d65021b4b857` — Sunday Review Sub 3 (CTA Habits) → BULK-EXPORT (behavioral/Action-Library)
- `35bdc0b53c118127a7d2cc3d4adc3574` — Sick / Low-Energy Day Protocol → BULK-EXPORT (behavioral/Action-Library)

## Memory-anchor resolution summary (claude.ai advisor-memory → repo)

- memory **#2** (MC Lock Details) → CLAUDE.md MC anchor + tests/core/test_mc_anchors.py
- memory **#5** (Strategy Lock Reference) → CLAUDE.md Strategy Reference + core/strategies/*/LOCK.md
- memory **#8** (loop-selection canon) → docs/methodology/inqhiori-canon.md
- memory **#9** (anchors) → CLAUDE.md + docs/mc_anchor_history.md
- memory **#13** (Q-roster) → docs/briefs/INDEX.md
- memory **#16** (role map / three-surfaces) → docs/methodology/archive/notion/methodology-canon.md + docs/adr/2026-06-12-notion-surface-retirement.md
- memory **#24** (canon §14 read-surface clause) → docs/methodology/inqhiori-canon.md §14
