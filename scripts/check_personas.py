#!/usr/bin/env python3
"""Audit hook: verify docs/personas/ roster is complete and well-formed.

Mirrors the bold-field grep convention used by docs/pursuits/*.md and this
repo's other check_*.py scripts (check_skill_refs.py, check_skills_no_constants.py).
"""
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PERSONAS_DIR = REPO_ROOT / "docs" / "personas"
INDEX_PATH = PERSONAS_DIR / "INDEX.md"

REQUIRED_FIELDS = [
    "Tier", "Office", "Reports-to", "Spawned", "Domain", "Independence rule", "Reads", "Writes", "Source",
]
VALID_TIERS = {"GRAND", "STRATEGIC", "STAFF"}
VALID_OFFICES = {"Front", "Middle", "Back", "Cross-office", "N/A"}
EXPECTED_COUNT = 14  # 19 built 2026-08-19; 5 non-front-office STAFF analysts archived to
# docs/personas/archive/ 2026-08-19 (operator-authorized cut, never spawned --
# see docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md)

LOG_ENTRY_HEADER = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s+—\s+(.+)$", re.MULTILINE)
LOG_HEADING_LOOSE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
LOG_REQUIRED_SUBFIELDS = ["Verdict", "Confirmed findings", "Ratified as recommended"]


def check_logs(errors):
    log_files = sorted(PERSONAS_DIR.glob("*-log.md"))
    for path in log_files:
        text = path.read_text(encoding="utf-8")
        all_headings = list(LOG_HEADING_LOOSE.finditer(text))
        valid_headers = list(LOG_ENTRY_HEADER.finditer(text))
        if not all_headings:
            errors.append(f"{path.name}: exists but has no entries matching '## YYYY-MM-DD — <path>'")
            continue

        # Every ## heading gets validated, not just the ones the strict pattern happens to match --
        # otherwise a malformed heading silently becomes body text of the preceding valid entry
        # instead of being flagged, which is exactly the failure mode this checker exists to catch.
        valid_starts = {m.start() for m in valid_headers}
        for m in all_headings:
            if m.start() not in valid_starts:
                errors.append(
                    f"{path.name}: malformed entry header '{m.group(0).strip()}' -- expected "
                    f"'## YYYY-MM-DD — <path>'"
                )

        for i, m in enumerate(valid_headers):
            start = m.end()
            # Block ends at the next heading of ANY kind (valid or malformed), not just the next
            # valid one -- otherwise a malformed heading between two valid entries gets absorbed
            # into the preceding entry's field-presence check instead of ending it.
            next_heading = next((h.start() for h in all_headings if h.start() > m.start()), len(text))
            block = text[start:next_heading]
            missing = [f for f in LOG_REQUIRED_SUBFIELDS if f"**{f}:**" not in block]
            if missing:
                errors.append(
                    f"{path.name}: entry dated {m.group(1)} missing required field(s): {', '.join(missing)}"
                )

def parse_fields(text):
    fields = {}
    for name in REQUIRED_FIELDS:
        m = re.search(rf"\*\*{re.escape(name)}:\*\*\s*(.+)", text)
        if m:
            fields[name] = m.group(1).strip()
    return fields


def main():
    errors = []

    if not PERSONAS_DIR.is_dir():
        print(f"FAIL: {PERSONAS_DIR} does not exist")
        return 1

    NON_PERSONA_FILES = {"INDEX.md", "ownership-map.md"}
    persona_files = sorted(
        p for p in PERSONAS_DIR.glob("*.md")
        if p.name not in NON_PERSONA_FILES and not p.name.endswith("-log.md")
    )

    if not persona_files:
        print(f"FAIL: no persona files found in {PERSONAS_DIR}")
        return 1

    role_names = set()
    reports_to_by_file = {}

    for path in persona_files:
        text = path.read_text(encoding="utf-8")
        fields = parse_fields(text)
        missing = [f for f in REQUIRED_FIELDS if f not in fields]
        if missing:
            errors.append(f"{path.name}: missing required field(s): {', '.join(missing)}")
            continue

        if fields["Tier"] not in VALID_TIERS:
            errors.append(f"{path.name}: invalid Tier '{fields['Tier']}' (expected one of {sorted(VALID_TIERS)})")

        if fields["Office"] not in VALID_OFFICES:
            errors.append(f"{path.name}: invalid Office '{fields['Office']}' (expected one of {sorted(VALID_OFFICES)})")

        if fields["Spawned"] not in {"Yes", "No"}:
            errors.append(f"{path.name}: Spawned must be 'Yes' or 'No', got '{fields['Spawned']}'")
        elif fields["Spawned"] == "Yes" and fields["Independence rule"].startswith("N/A"):
            errors.append(f"{path.name}: Spawned=Yes but Independence rule is N/A")
        elif fields["Spawned"] == "No" and not fields["Independence rule"].startswith("N/A"):
            errors.append(f"{path.name}: Spawned=No but Independence rule is not N/A")

        h1 = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if not h1:
            errors.append(f"{path.name}: missing H1 role-name heading")
        else:
            role_names.add(h1.group(1).strip())

        reports_to_by_file[path.name] = fields.get("Reports-to", "")

    for fname, reports_to in reports_to_by_file.items():
        if reports_to.startswith("N/A"):
            continue
        if reports_to not in role_names:
            errors.append(f"{fname}: Reports-to '{reports_to}' does not match any known role name")

    if len(persona_files) != EXPECTED_COUNT:
        errors.append(f"expected {EXPECTED_COUNT} persona files, found {len(persona_files)}")

    if not INDEX_PATH.is_file():
        errors.append(f"{INDEX_PATH} does not exist")
    else:
        index_text = INDEX_PATH.read_text(encoding="utf-8")
        index_rows = len(re.findall(r"^\|\s*\[", index_text, re.MULTILINE))
        if index_rows != len(persona_files):
            errors.append(f"INDEX.md has {index_rows} persona rows, but {len(persona_files)} persona files exist")

    check_logs(errors)

    if errors:
        print(f"FAIL: {len(errors)} issue(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"check_personas: OK -- {len(persona_files)} persona files, all required fields present, INDEX.md in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
