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
EXPECTED_COUNT = 19


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

    persona_files = sorted(p for p in PERSONAS_DIR.glob("*.md") if p.name != "INDEX.md")

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

    if errors:
        print(f"FAIL: {len(errors)} issue(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"check_personas: OK -- {len(persona_files)} persona files, all required fields present, INDEX.md in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
