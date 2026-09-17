# Brief validator coverage and import design

Audited against `6a3d4b3` before extraction. Authoring and implementation are
authorized by the execution request. Scope is equivalent parsing and numbered
checks, not a merged dispatcher or generic rule language.

| Type/format | Repository CLI | Standalone skill CLI |
|---|---|---|
| adr, numbered | general numbered checks | general numbered checks |
| brief, generic | general numbered checks | CLI rejects these names |
| inquire | alias of brief, subset note | general numbered checks |
| handoff | general + required 0.5 + four statuses | CLI rejects this name |
| cc_handoff | alias of handoff, subset note | general + required 0.5 + four statuses |
| adr, concise header | NOT CHECKED, 0 | H2 Decision/Grounds/Current owner; missing/empty HARD |
| light header | NOT CHECKED, 0 | named Decision/Grounds/Reads/Gate/Boundary; 300-word WARN |
| notice | NOT CHECKED, 0 | 0/1/2/3/4/10, routing, HOLD requires 5, fence 10 |
| audit | NOT CHECKED, 0 | 0/1/2/3/4/5/6/7/10/11, path+anchor 0, fence 10 |
| lesson | NOT CHECKED, 0 | named sections, audit fence, promotion/retirement by status |
| lock | NOT CHECKED, 0 | trigger table or falsifier framing only |
| closure | DELEGATED instruction, 0 | DELEGATED instruction, 0 |

General checks, in order: required 0/1/4/5/6/10 (missing HARD, empty WARN),
path+anchor 0 HARD, hypothesis/falsifier or accepted alternate framing 4 HARD,
forbidden list 5 HARD, fenced audit hook 10 HARD, binary verdict 6 WARN.
Handoff adds required 0.5 and four-status 6 HARD. Skill empty-body classification
also rejects whole bracketed placeholders; repo classification does not. Keep
both predicates in their wrappers and pass them to `NumberedChecks`. Required
section tuples are arguments to its presence check; the common general tuple
has one owner. Nonidentical checks remain local.

CLI/report contracts remain in wrappers: missing/directory input returns 2,
HARD returns 1, warnings alone return 0. Skill alone offers list-checks/self-test
and reads all seven templates relative to its own file. Repo type aliases and
normalization remain local. Repo inference: header > filename handoff > body
handoff > ADR > generic. Skill: header > ID fields > filename/body handoff >
closure > ADR/default. Keep actual dispatch precedence, including closure CLI
delegation and concise/light handling; do not execute the closure checker.

Canonical engine: `.claude/skills/brief-authoring/scripts/brief_checks.py`, pure
stdlib, no repository imports. Both wrappers load an absolute sibling/repo-local
path using importlib file specs, independent of cwd/PYTHONPATH or installed home
skills. Explicit exports retain tested helper names. No shared mutable global
profile or monkeypatch of one wrapper's predicate into the other.

Publication tooling copies the skill tree (`scripts/sync_skills.py`), including
Python files and references; no generator or additional packaged copy is needed.
Verify temporary standalone copies with isolated Python, list-checks, self-test,
and input-error/delegation cases. Compare old/new API and CLI results across
types/formats, including bracket placeholders, against Git base code. Existing
independent per-type mutation tests stay intact. Accept extraction only if total
bytes including new tests and this design decrease; do not publish the skill.
