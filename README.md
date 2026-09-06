# First Passage

Research and operations for automated futures strategies: **generate → evaluate →
deploy → measure → update**. Current priorities are in [STATE.md](STATE.md);
execution safeguards and the recorded rail posture are in
[CLAUDE.md](CLAUDE.md#live-execution-posture).

## Source of truth

The five root documents have separate jobs:

| File | Job |
|---|---|
| [README.md](README.md) | Human entry point and task routing |
| [CLAUDE.md](CLAUDE.md) | Agent instructions, essential safeguards, and source authority |
| [PIPELINES.md](PIPELINES.md) | Workflow, handoffs, and available machinery |
| [STATE.md](STATE.md) | Current priorities and outstanding obligations |
| [REPO_MAP.md](REPO_MAP.md) | Present architecture, import boundaries, and module entry points |

Campaign plans own executable next steps; their campaign records own evidence
and decisions. [SESSIONS.md](docs/SESSIONS.md) is historical narrative, not the
current work list. [Operational Rule 7](docs/operational_rules.md#7-one-canonical-owner-per-fact-every-other-mention-links-or-is-a-labeled-mirror)
assigns ownership; [Rule 0](docs/rule_0.md) requires reading production sources
when checking claims about code, parameters, or risk controls.

## Where to look

| Need | Open first |
|---|---|
| Choose or resume current work | [STATE queue](STATE.md#operator-queue--strictly-ordered-5-live-items), then the linked executable plan |
| Understand a research or execution handoff | [PIPELINES.md](PIPELINES.md) |
| Locate code or run a layer module | [REPO_MAP.md](REPO_MAP.md) |
| Find prior research before opening work | [Lab catalog — In flight](lab/CATALOG.md#in-flight), then [brief index](docs/briefs/INDEX.md) |
| Check instrument evidence and re-proposal bars | [Instrument profiles](ops/instruments/PROFILES.md), [mechanisms](ops/instruments/MECHANISMS.md), [rejected candidates](docs/rejected_candidates.md) |
| Check a strategy's parameters or venue disposition | [Strategy catalog](core/strategies/CATALOG.md), [venue editions](ops/venue_editions/Tradeify_Select_100K.md) |
| Resolve conflicting published figures | [Load-bearing numbers](docs/load_bearing_numbers.md) |
| Find a decision or governing method | [ADR index](docs/adr/INDEX.md), [methodology](docs/methodology/README.md) |
| Run checks or install hooks | [Scripts README](scripts/README.md), [gate manifest](scripts/gates.yml) |
| Interpret identifiers or routine governance | [Governance index](docs/governance/INDEX.md) |
| Retrieve a removed artifact | [Archive retrieval](docs/ltm/README.md), [removed-path manifest](lab/ARCHIVED.json) |

Layer READMEs point to their catalogs. **In flight** means a question is not spent
or on HOLD; **hot** means its body is on disk. Neither denotes queue priority.
Default search excludes cold stores, and private inputs are gitignored: an empty
search is not evidence that prior work or source bytes never existed.

## Public-clone note

Vendor data, Pine sources, and executable ports of locked strategies are private,
hash-pinned inputs; see [CLAUDE.md §Public-clone posture](CLAUDE.md#public-clone-posture)
for the boundaries and integrity checks.
