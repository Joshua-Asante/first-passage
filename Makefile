# First Passage - convenience targets.
# Wrappers around scripts that the pre-commit hook also calls.

.PHONY: help check audit validate validate-data validate-pine boundaries lab-catalog lab-catalog-check lab-archive-check test test-ops roll-sessions roll-sessions-dry instrument-profiles instrument-profiles-build gate-manifest gate-manifest-list

help:
	@echo "check                 run check-tier gates (scripts/gates.yml)"
	@echo "audit                 run report-only diagnostics"
	@echo "validate              data manifests + pine"
	@echo "lab-catalog           regenerate lab/CATALOG.md"
	@echo "sentinel              INQHIORI sentinel scan (report-only)"
	@echo "gate-manifest-list    print the hard-gate roster (blocking tiers)"
	@echo "test / test-ops       pytest (all / ops/)"

# Composition is owned by scripts/gates.yml via gate_manifest.py. Individual
# targets below are thin wrappers for one-off runs.

check:
	@python scripts/gate_manifest.py --tier check

audit:
	@python scripts/gate_manifest.py --tier audit

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

boundaries:
	@python scripts/check_boundaries.py

# Instrument-profile index (PROFILE blocks <-> MECHANISMS.md <-> generated view).
instrument-profiles:
	@python scripts/instrument_profiles.py check

instrument-profiles-build:
	@python scripts/instrument_profiles.py build

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

test:
	@python -m pytest tests/ -x

test-ops:
	@python -m pytest tests/ops/ -x

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
