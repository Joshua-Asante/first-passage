# First Passage - convenience targets.
# Wrappers around scripts that the pre-commit hook also calls.

.PHONY: check validate validate-data validate-pine skills-no-constants boundaries path-liveness root-doc-liveness md-relative-links lab-path-relocation status-consistency adr-graph adr-graph-index lab-catalog lab-catalog-check lab-archive-check test test-ops skills-check sync-skills sync-skills-check roll-sessions roll-sessions-dry instrument-profiles instrument-profiles-build gate-manifest gate-manifest-list

# W5: composition owned by scripts/gates.yml via gate_manifest.py
# (docs/adr/2026-08-07-w5-governance-diet.md). Individual targets below remain
# as thin wrappers for one-off runs.

check:
	@python scripts/gate_manifest.py --tier check

validate:
	@python scripts/gate_manifest.py --tier validate

gate-manifest:
	@python scripts/gate_manifest.py --tier pre-commit

gate-manifest-list:
	@python scripts/gate_manifest.py --list

validate-data:
	@python scripts/check_data_manifests.py --check

validate-pine:
	@python scripts/check_pine_manifest.py

skills-no-constants:
	@python scripts/check_skills_no_constants.py

boundaries:
	@python scripts/check_boundaries.py

path-liveness:
	@python scripts/check_path_liveness.py

# Root orientation-doc link gate (README/CLAUDE/PIPELINES/REPO_MAP/STATE).
root-doc-liveness:
	@python scripts/check_root_doc_liveness.py

# Warn-only corpus scan (file-relative). NOT a `check` candidate and no longer
# carries a promotion TODO (removed 2026-08-08): runtime disqualifies it from any
# commit-time tier regardless of debt level, and the promotion clause had no owner,
# no debt census and no trigger. It is a manual forensic tool — run it deliberately.
# Scope caveat: it does not scan `.claude/`, so skill links are outside its reach.
md-relative-links:
	@python scripts/check_md_relative_links.py

# Warn-only: docs cite a dead lab/ path whose tail still exists elsewhere under
# lab/ (theme-nest / archive relocation rot). Pruned-by-design harnesses do not
# flag. NOT in scripts/gates.yml — belt-churn YELLOW; promote via soft/warn tier
# later (CLAUDE.md §Gate composition authority).
lab-path-relocation:
	@python scripts/check_lab_path_relocation.py

# Cross-surface status-consistency gate (CATALOG <-> instrument-ledger DEAD-lists
# <-> rejected_candidates.md; C2 CATALOG self-consistency + C3 stale analysis->archive tier).
status-consistency:
	@python scripts/check_status_consistency.py

# Instrument-profile index (PROFILE blocks <-> MECHANISMS.md <-> generated view).
instrument-profiles:
	@python scripts/instrument_profiles.py check

instrument-profiles-build:
	@python scripts/instrument_profiles.py build

# ADR lifecycle graph (headers, edges when enabled, derived INDEX).
adr-graph:
	@python scripts/check_adr_graph.py

adr-graph-index:
	@python scripts/check_adr_graph.py --regenerate-index

# lab/CATALOG.md freshness (always-on). Stale → regenerate, then commit the delta.
lab-catalog-check:
	@python scripts/archive_lab_analysis.py --check --catalog-only

# Rebuild lab/CATALOG.md from lab/analysis + lab/archive (commit the delta).
lab-catalog:
	@python scripts/archive_lab_analysis.py --regenerate-catalog

# Full STM/LTM hygiene (unstubbed closes, stub shape, catalog). Not in `make check`
# — archive promotion stays operator-fired via --slug.
lab-archive-check:
	@python scripts/archive_lab_analysis.py --check

# Rule 11 floor: do standing ADR falsifiers still name inputs that exist?
# Deliberately NOT in `make check` and NOT in the pre-commit hook — WARN-tier only.
# A hard gate would block commits on ADRs nobody is touching (the M-22 failure mode).
# Covers ~28% of falsifier sections (the rest are prose); blind to retired-duty limbs.
falsifier-reachability:
	@python scripts/check_falsifier_reachability.py --stats

test:
	@python -m pytest tests/ -x

test-ops:
	@python -m pytest tests/ops/ -x

# Skill gate: path-reference linter (no-constants is skills-no-constants).
skills-check:
	@python scripts/check_skill_refs.py --all

# One-way sync of in-repo .claude/skills/ -> deployed bundle (repo is source of truth).
# `make sync-skills` copies; `make sync-skills-check` is drift-only (advisory vs cloud-synced target).
sync-skills:
ifdef CHECK
	@python scripts/sync_skills.py --check
else
	@python scripts/sync_skills.py
endif

sync-skills-check:
	@python scripts/sync_skills.py --check

# Keep the newest 20 session entries live and preserve older entries verbatim
# in quarterly archives. Preview is always available as a no-write target.
roll-sessions-dry:
	@python scripts/roll_sessions.py --dry-run

roll-sessions:
	@python scripts/roll_sessions.py

# INQHIORI Sentinel — Tier-1 deterministic hygiene scan (report-only, zero-token).
# Prepends a run block to docs/notes/sentinel/queue.md. Override date: make sentinel ASOF=2026-06-23.
.PHONY: sentinel
sentinel:
	@PYTHONPATH=ops python -m sentinel --asof $(or $(ASOF),$(shell python -c "import datetime;print(datetime.date.today())"))
