"""Shared dependency edits must schedule the lab consumer suite on both events."""

from fnmatch import fnmatchcase
from pathlib import Path

import pytest
import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/validation-controls.yml"


@pytest.mark.parametrize("event", ["push", "pull_request"])
@pytest.mark.parametrize("changed_path, expected", [
    ("core/mc/simulation.py", True),
    ("core/lib/validation.py", True),
    ("core/mc/README.md", True),  # The core/** predicate includes documentation.
    ("lab/analysis/example/test_replay.py", True),
    ("pyproject.toml", True),
    ("requirements-ops.lock", True),
    (".github/workflows/validation-controls.yml", True),
    ("requirements-research.lock", False),
    ("scripts/layer_bootstrap.py", False),
    ("docs/notes/example.md", False),
    ("ops/c1_rail/c1_rail_listener.py", False),
])
def test_dependency_change_schedules_consumer_suite(event, changed_path, expected):
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    # PyYAML's YAML 1.1 loader reads the Actions `on` key as boolean True.
    events = workflow.get("on", workflow.get(True))
    patterns = events[event]["paths"]
    # These predicates use only literal paths and trailing /**. fnmatchcase
    # matches their Actions semantics; more complex glob syntax needs a matcher.
    assert all(not any(char in p for char in "?![]+") and
               ("*" not in p or p.endswith("/**") and p.count("*") == 2)
               for p in patterns)
    assert any(fnmatchcase(changed_path, pattern) for pattern in patterns) is expected
