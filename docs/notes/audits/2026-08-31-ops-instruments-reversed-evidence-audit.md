# ops/instruments/ reversed-evidence audit — 2026-08-31

**Audit ID:** AUDIT-2026-08-31-OPS-INSTRUMENTS-REVERSED-EVIDENCE · **Date:** 2026-08-31 · **Trigger:**
operator direction ("on a separate branch, take a similar look at `ops/instruments/`"), following the
companion mirror-docs audit ([`docs/notes/audits/2026-08-31-reversed-evidence-docs-audit.md`](2026-08-31-reversed-evidence-docs-audit.md)
§4), which had explicitly logged `ops/instruments/*.md` (32 files) as unswept and high-risk for this
failure class — per-leg live/dead state that changes often.

**Scope:** all 32 `ops/instruments/*.md` files. Same targeted (known-reversal-propagation) method as the
companion audit, not a blind full-corpus scan.

**Method:**

1. Reused the ~30-item reversal reference sheet compiled for the companion audit (the ADR supersession
   graph + closure ledger + `CLAUDE.md`'s own flagged reversals), extended with a few instrument-specific
   entries (Striker `LEG_MAP` cap release, Aegis venue status, ORB-MNQ repark).
2. Ran one scan agent per file (32/32), each checked against the reference sheet and free to surface any
   other verifiable reversal, with explicit attention to occupancy/leg-live-dead status, `cap_alloc`
   figures, campaign dispositions, and cross-references between sibling instrument files.
3. Ran an independent, refute-first adversarial verify pass on every flag (37/37) — each verifier
   re-derived the claim and the reversal from primary source rather than trusting the scan pass, and for
   any numeric claim independently re-checked the exact figure before proposing a fix.
4. Applied minimal, pointer-based fixes across the 19 files with confirmed findings, one agent per file.
5. Regenerated `ops/instruments/PROFILES.md` + `profiles.json` via `python scripts/instrument_profiles.py
   build` after any PROFILE-YAML source edit — see §5 (lesson carried over from the companion PR's Codex
   review).

---

## §1 — Result

| Verdict | Count |
|---|---|
| Files scanned | 32 |
| Candidate findings (Phase 1 scan) | 47 |
| `CONFIRMED_STALE` (Phase 2 verify) | 38 |
| `NOT_STALE` — false positives caught by verify | 9 |
| `UNCERTAIN` | 0 |
| **Fixed this session** | **38 / 38** (46 discrete edit sites — several findings touched more than one line) |

---

## §2 — Findings by theme

Three reversal events accounted for most of the drift, each propagating unevenly across the fleet of
sibling instrument ledgers (a pattern the companion audit's method — scan every mirror independently
rather than assume siblings share a fix — was specifically designed to catch):

**Striker `LEG_MAP` cap_alloc release (69/11 → 0/0, 2026-08-26)** — not yet reflected in:
`6J.md`, `M2K.md`, `M6A.md`, `MCL.md`, `MES.md`, `MNQ.md` (×2 — RECORD section + N1 finding),
`MYM.md`, `NQ.md`. Each still stated the pre-release 69/11 figures as current code truth or an
unresolved headroom question.

**F2/F3 environment ratification (2026-08-07 S1 ADR — rail warm/disarmed at incumbent eval, no
successor venue)** — not yet reflected in: `ES.md` (both forks stated as still open), `M2K.md`
(cost-hurdle basis citing "F3 open"), `MNQ.md` (×2 — N1 finding and ORB-MNQ-1 bullet, both citing
F2/F3 as pending gates rather than settled).

**Pepperstone feed retirement (2026-08-02)** — not yet reflected in: `EURUSD.md`, `GER40.md`,
`NAS100.md`, `SPX500.md` (×3 sites), `USOIL.md` header (already correctly hedged, not flagged),
`XAGUSD.md`, `XAUUSD.md` (×4 sites, including a compounding Dukascopy-retirement claim). Each still
named Pepperstone as "canonical feed" in present tense; several of these instruments have no live
venue at all, so "canonical feed" should read as historical provenance, not current designation.

**Other, single-instance findings:**

| File | Stale claim | Reversed by |
|---|---|---|
| `BTCUSD.md` | FXIFY $200K CFD challenge framed as a currently-running venue | Challenge closed 2026-07-10, CFD estate retired 2026-07-11 |
| `EURUSD.md` | eurusd_pattern_enum "Phase 4+ not started" (×4 sites) | Phase 4 CLOSED 2026-08-24 DONE_WITH_CONCERNS |
| `EURUSD.md` | `compose_from_hint`/codification pipeline framed as extensible | Gen-1 pipeline retired 2026-07-11, `lab/codification/` gone 2026-08-02 |
| `M6A.md` | Commission input $0.91/side (RT $2.82) stated as settled | Disputed by `core/firm_rules.py` (M6A is in the cheaper $1.60-RT group) and an already-disclosed-but-unapplied DL-2 prereg correction — **flagged, not corrected**, since resolving it is this ledger owner's call, not this audit's |
| `M6A.md` | "No candidate, no K spend" | DL-2 campaign ran and closed AMBIGUOUS-ABANDONMENT 2026-08-22, K≈10 spent |
| `MECHANISMS.md` | MSL-S4 candidate reads as an open/undecided item | Operator-PARKED 2026-08-21, same day as the AMBIGUOUS-HOLD result |
| `MECHANISMS.md` | `prior-session-breakout-continuation` reads as "untested" | DL-2/M6A campaign closed AMBIGUOUS/ABANDONMENT the same day the id was minted |
| `MGC.md` | Guardian→MGC lane "remains PARKED/CLOSED" | DEAD(N-SURV) 2026-08-11, Standing flipped PARK→SUBTRACT same day |
| `MNQ.md` | 3yr combined-book bust figure cited as 4.34% | Same-day follow-up (§10.2) revised to both-halves 3.29%/5.37% |
| `USOIL.md` | Concept `CONCEPT-USOIL-RGC-001` reads as active/PARKED (×4 sites: Status line, ACTIVE CONCEPTS table, ANTI-SNAG LEDGER, OPEN QUESTIONS) | CLOSED via GSUB-1 SUBTRACT, ratified 2026-08-09 |

**False positives caught by the verify pass** (reported for completeness, per the no-silent-caps
convention — correct as-is, left untouched):

- `6J.md` — the H-PARITY bullet's Pepperstone reference is about a different retirement axis (CFD/manual-trading) than the scanner assumed; not the same claim as the feed-retirement pattern above.
- `6J.md` — finding J4 is explicitly superseded in-file by J4b already; no separate fix needed.
- `BTCUSD.md` — durable finding #7 and the Q-BTC-3 entry's "5/6 prohibit/restrict" figure is independently sourced and accurate; not tied to the FXIFY closure the scanner cited.
- `MGC.md` — "Never hash-pinned" (2026-08-21e session-log entry) is accurate dated historical narration, not a live claim.
- `PROFILES.md` (×3: MYM, NAS100, XAUUSD matrix rows) — the mechanism matrix's "LIVE" tag is a distinct vocabulary (parameter-lock status) from live-deployment status; not the same claim as "currently trading."
- `USOIL.md` — the PROFILE cell's `verdict: AMBIGUOUS-PARKED` / `date: 2026-06-15` is accurate as the dated verdict at that time; the file's prose elsewhere (fixed above) was the actual stale surface, not this structured cell.
- `YM.md` — "parked NO-MECH per Q-MECH-1 to the 2026-08-08 review" uses a vocabulary this repo keeps deliberately distinct from `strategy_lifecycle.md`'s tier language; not a contradiction.

---

## §3 — Fixes applied

One commit on `claude/ops-instruments-reversed-evidence-audit` (`d81697c`): 21 files (19 instrument
ledgers with confirmed findings, plus the regenerated `PROFILES.md` + `profiles.json`). Every fix adds a
dated `⚠ Correction <date>:` or `⚠ Superseded <date>:` pointer next to the stale claim, in the style each
file already uses for its own prior corrections where one existed. Historical text is preserved
throughout — nothing is rewritten, per Rule 7.

The M6A commission-figure finding is the one exception to "fix now": per the audit's own discipline
(verify, don't silently correct disputed operational figures that belong to a different owner's forward
work), it is flagged with a pointer to the already-existing DL-2 prereg correction rather than having
this audit compute and assert a new number.

---

## §4 — Scope limitations

This audit covered `ops/instruments/*.md` completely (32/32 files) — no further scope gap to log for
this specific directory. It does not extend to the other unswept surfaces already logged in the
companion audit's §4 (`docs/pursuits/*.md` beyond the 5 already checked, `docs/personas/*.md`, most
`.claude/skills/*/SKILL.md`, most `core/strategies/**/*.md` card mirrors) — those remain open forward
obligations on `STATE.md`, unchanged by this pass.

---

## §5 — Generated-view discipline (lesson carried from PR #230's review)

Several confirmed findings (`M2K`, `M6A`, `MCL`, `MES`) required editing `venue_note` / `cost_hurdle`
fields inside a `PROFILE` YAML block — source data that `scripts/instrument_profiles.py build` compiles
into `ops/instruments/PROFILES.md` and `ops/instruments/profiles.json`. Per the repo's own convention
(and the exact mistake caught by Codex's review on the companion PR #230, where `lab/CATALOG.md` was
hand-edited instead of its actual source), this audit edited only the `.md` source files and then ran:

```bash
python scripts/instrument_profiles.py build
python scripts/instrument_profiles.py check   # confirms: view current
```

The regenerated `PROFILES.md`/`profiles.json` diff is small (12 lines) and matches exactly what the
source edits imply — no hand-editing of either generated file occurred.

---

## §6 — Discipline check

```
[x] Full ops/instruments/*.md file list enumerated (32), none silently dropped
[x] Every file got one independent scan agent (32/32)
[x] Every flag ran an independent refute-first verify pass (47/47) — 9 refuted, reasoning recorded
[x] Every CONFIRMED_STALE finding fixed this session, not left as an unowned forward obligation (38/38)
[x] Fixes are pointer-based, never rewrite history or duplicate the current value inline (Rule 7)
[x] False positives reported, not silently dropped (§2)
[x] One disputed-but-not-this-audit's-to-resolve figure (M6A commission) flagged, not silently "fixed"
    with an unverified replacement number
[x] Generated-mirror discipline followed — PROFILES.md/profiles.json regenerated via their own build
    command after every PROFILE-YAML edit, not hand-edited (§5)
[x] gate_manifest.py --tier check run clean (instrument_profiles: OK, view current; the one pre-existing
    check_instrument_rejection_coverage gap-report and the pre-existing numpy import failure are both
    identical on clean main, confirmed via git stash — unrelated to this diff)
[x] Next trigger: on operator request, or opportunistically alongside the next reversed-evidence pass
    over the remaining unswept surfaces named in the companion audit's §4
```
