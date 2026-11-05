# R2 dossiers: dedup search (Rule 8)

Run 2026-11-04 before any dossier was drafted, on `claude/r2-cell-dossiers` (base `main`). Output pasted as printed. Empty output means no hit.

```text
$ git ls-files | grep -i dossier

$ grep -rIl -i "R2 dossier\|cell dossier\|builder-r2\|PREREG-BUILDER-R2" --include=*.md .

$ git branch -r | grep -i -E "dossier|r2|builder"
  origin/claude/builder-round-template
  origin/claude/builder-ten-step-mapping
  origin/claude/r1r2-evidence-cli
  origin/claude/sharp-heisenberg-ajbr2g
  origin/claude/strategy-builder-v1

$ gh api -X GET search/issues -f q='dossier repo:Joshua-Asante/first-passage is:pr' --jq '.items[] | [.number,.state,.title] | @tsv'
1051	open	docs(prereg): builder round template — task chain T1–T8, private/public split

$ gh api -X GET search/issues -f q='dossier repo:Joshua-Asante/first-passage is:issue' --jq '.items[] | [.number,.state,.title] | @tsv'

$ gh api -X GET search/issues -f q='R2 repo:Joshua-Asante/first-passage is:pr is:open' --jq '.items[] | [.number,.state,.title] | @tsv'
1051	open	docs(prereg): builder round template — task chain T1–T8, private/public split

$ gh api -X GET search/issues -f q='barrier repo:Joshua-Asante/first-passage is:pr is:open' --jq '.items[] | [.number,.state,.title] | @tsv'

```

**Reading:**
- No dossier existed.
- PR #1051 is the template these dossiers fill. Its §A2–§A3 fields were read from that PR's head `0a4c5a9`.
- The listed branches are the template, the gate mapping, an evidence CLI and the builder. None holds dossiers.
- The barrier atlas is a sibling session's work with no PR yet, so each dossier marks barrier feasibility "pending atlas".
- Also reused, not re-derived: PR #1040's cross-firm exclusivity draft, for venue legality.

**Per-cell priors:** each dossier's prior-consult section carries its `instrument_profiles.py cell` output and register hits (advisory, Rule 26).
