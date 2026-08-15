"""Canonical filesystem locations for campaign pre-registration artifacts.

Single source of truth for the on-disk paths of frozen campaign pre-registration
markdown. Tests and CLI ``--self-test`` defaults import from here so an LTM roll
(``docs/`` -> ``docs/ltm/``, e.g. commit ``fad8984``) or a rename is a one-line
change in this file instead of a sweep across every consumer. Add one constant
per campaign as new pre-registrations are frozen.
"""

from __future__ import annotations

from research_utils.repo_root import repo_root

# DISC-CAMP-0 (Gen-2 discovery campaign). Rolled to docs/ltm/ on 2026-07-14
# (commit fad8984, "Exclude LTM corpus from default agent search"); the bytes are
# git-tracked at the LTM path, so this resolves on a fresh clone / CI.
DISC_CAMP_0_PREREG = (
    repo_root()
    / "docs"
    / "ltm"
    / "briefs"
    / "pre-registration"
    / "DISC-CAMP-0-preregistration.md"
)
