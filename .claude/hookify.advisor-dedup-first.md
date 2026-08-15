---
name: warn-advisor-dedup-first
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (Downloads[\\/]|web.?advisor|advisor (said|recommend|suggest|staged)|staged (artifact|brief|closure|gate.audit)|implement|port |build .*(as|for)|add .*(closed-form|algorithm|anchor) for)
---

📎 **Prior-art search before treating this as new work.**

Triggers on Downloads/advisor-staged language **and** build-intent phrasing
(`implement` / `port` / `build … as|for` / `add … closed-form|algorithm|anchor for`).

Two dated firings of the same miss:

- **2026-07-24:** a Downloads-staged Pre-Q brief + gate-audit note claimed an
  untested "Weekly+Daily residual" from an imagined 2026-07-23 ICT closure.
  `handoff-verify` caught it as confabulated — no such run existed; the real
  corpus (`lab/archive/ict_cascade_2026-06-18/`) had already closed PER-LAYER
  months earlier under a pre-registered ledger. The catch cost a full session
  because nothing pointed the session at the existing closure before it started
  reasoning about the staged claims as live.
- **2026-08-13:** Magdon-Ismail closed-form MDD work proceeded straight to
  WebSearch / implementation with no repo search; `lab/analysis/mc/mc_mdd_closed_form_2026-08/`
  already existed (PR #790), caught only when the pre-commit `lab-catalog` gate
  flagged a stale CATALOG. Same class, build-intent phrasing — the prior hookify
  regex never fired.

**Before scoping the work as new, run:**

```bash
# staged file (advisor / Downloads artifact)
python scripts/check_advisor_dedup.py <path-to-staged-file>

# or keywords only (before any file exists)
python scripts/check_advisor_dedup.py --keywords "Magdon-Ismail closed-form drawdown"
```

It ranks existing closures/audits/SESSIONS/CATALOG/rejected-candidates entries
by term overlap — a few-second lookup for what took a full session to
discover by hand. It is a search assistant, not a verdict: a match means
"read this before proceeding," not "this is definitely the same thing," and
no match does not mean the content is new — still verify claimed repo state
directly (`handoff-verify`) either way. Also open `lab/CATALOG.md` and
`docs/briefs/INDEX.md` and paste literal search output into §0
(`docs/operational_rules.md` Rule 8 sub-rule 8).

Grounding: [`ADR 2026-08-13`](docs/adr/2026-08-13-dedup-first-before-new-work.md);
2026-07-24 SESSIONS entry "Q-ICT-1 + composite-closure gate audit:
confabulated handoff caught, corrected, relocated";
`feedback_web_advisor_handoff_confabulates_repo_state`.
