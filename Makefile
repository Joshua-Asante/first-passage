# First Passage - convenience targets.
# Wrappers around scripts that the pre-commit hook also calls.

.PHONY: help check audit validate validate-data validate-pine boundaries test test-ops instrument-profiles instrument-profiles-build gate-manifest gate-manifest-list

help:
	@echo "check                 run check-tier gates (scripts/gates.yml)"
	@echo "audit                 run report-only diagnostics"
	@echo "validate              data manifests + pine"
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

test:
	@python -m pytest tests/ -x

test-ops:
	@python -m pytest tests/ops/ -x
