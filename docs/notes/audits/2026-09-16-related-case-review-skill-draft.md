# Related case review skill draft evaluation

Artifact: [SKILL.md](../../skill-drafts/related-case-review/SKILL.md).

Status: authored and subsequently installed at the user's request into `C:/Users/joshu/.codex/skills/related-case-review`. Installed and source file SHA-256 hashes match. Automatic discovery is expected next turn; selection by a future agent has not been observed. Existing receiving-code-review guidance already covers affected contracts; this skill adds a bounded map with evidence-backed dispositions. No plugin cache was modified.

One independent subagent performed a read-only, hypothetical decision evaluation of three supplied fixtures. The outcome rubric was supplied before responses: identify materially related paths and suitable evidence for a shared validation defect; keep a cosmetic edit local; reject an unsupported review claim. No implementation shape was prescribed.

- Shared validation: two unchecked dictionary lookups in a parser used by API and CLI. The evaluator identified both fields, caller error translation, negative and valid cases, and a bounded common-owner repair.
- Cosmetic control: a misspelled UI label. The evaluator selected a focused edit without an audit.
- Incorrect finding: nonstring input already returns before membership. The evaluator rejected the claimed defect rather than adding a redundant guard.

All three hypothetical decisions met the rubric. No code was executed, and there was no baseline comparison; these observations do not establish improved reliability. The evaluator identified possible scope and test-combination ambiguity. The final draft clarifies a concrete boundary and avoids demanding exhaustive combinations; those wording changes were not independently retested.

The bundled quick_validate.py was attempted with available Python runtimes but could not run because PyYAML was absent; the project virtual environment also could not launch. Frontmatter and body were inspected manually: required name and description present, valid lowercase hyphenated name, no scaffold placeholders or supporting-resource dependencies. Automated schema validation remains unverified.

Follow-up: PyYAML 6.0.3 was installed in Codex's bundled Python 3.12 runtime at the user's request. Package permissions were restored to parent inheritance after pip retained restrictive temporary-directory permissions. A normal sandboxed invocation successfully imported PyYAML and parsed YAML. The bundled quick_validate.py then passed for both source and installed skill. This supersedes the earlier unverified schema status. Default Python 3.14 user packages already contain PyYAML but remain inaccessible to ordinary sandboxed commands; writing its system site-packages was blocked by Windows permissions.
