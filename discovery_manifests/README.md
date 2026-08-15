# discovery_manifests/

Committed home for discovery pre-registration manifests written by
`lab/discovery/register_search.py` (invoke:
`PYTHONPATH=lab python -m discovery.register_search …`).

Skill wrapper `.claude/skills/futures-anomaly-discovery/scripts/register_search.py`
forwards to the same module when run from a **monorepo checkout**; prefer the
`-m` form (required after `sync_skills` deploy outside the repo).

Each `<run_id>.json` is a **pre-registration-as-a-file**: it binds the search-space
size K, α, data window, and hypothesis to a run id *before* any result is examined
(`open`), then records the survivor p-values and the cheap Bonferroni/BH triage
(`close`). The rigorous universe-level correction (White RC / Hansen SPA /
Romano–Wolf, DSR, PBO) happens downstream in `strategy-validation` §8 and needs the
full K-column return set — this ledger just makes K an auditable, timestamped fact so
that correction is possible.

Manifests are **committed** (auditability is the point). The directory is
repo-root-anchored via `research_utils.repo_root()` so runs land here regardless of
the invoking cwd; set `DISCOVERY_LEDGER` to redirect for scratch/CI use.

Governance: `docs/adr/2026-07-10-databento-research-stack.md` (§4 uselessness check
= zero closed manifests here by 2027-01-10 → archive the stack) and its 2026-07-11
addenda (repo-root anchor + lab relocation). Campaign context:
`docs/briefs/rnd-pipeline/discovery-campaign-template.md`.
