"""Workflow path filters must name files that exist (2026-10-15 doc alignment).

A literal filter entry for a retired or never-seeded file can never trigger its
workflow; c1-image-validation listed a payload-sufficiency matrix that lives only
in the private archive.
"""
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
WORKFLOWS = sorted((REPO / ".github" / "workflows").glob("*.yml"))


def _filter_entries(workflow: Path) -> list[str]:
    data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    # PyYAML's YAML 1.1 loader reads the Actions `on` key as boolean True.
    events = data.get("on", data.get(True))
    if not isinstance(events, dict):
        return []
    return [
        entry.lstrip("!")
        for cfg in events.values()
        if isinstance(cfg, dict)
        for key in ("paths", "paths-ignore")
        for entry in cfg.get(key) or []
    ]


@pytest.mark.parametrize("workflow", WORKFLOWS, ids=lambda p: p.name)
def test_literal_and_directory_filters_exist(workflow):
    missing = []
    for entry in _filter_entries(workflow):
        if entry.endswith("/**") and not any(c in entry[:-3] for c in "*?["):
            if not (REPO / entry[:-3]).is_dir():
                missing.append(entry)
        elif not any(c in entry for c in "*?["):
            if not (REPO / entry).exists():
                missing.append(entry)
    assert missing == [], f"{workflow.name} filters name absent paths: {missing}"
