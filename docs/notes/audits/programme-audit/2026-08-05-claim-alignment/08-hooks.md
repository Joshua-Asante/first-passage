# 08 — Audit hooks (runnable)

**What this file is.** Every runnable check the two-round audit produced: round 1's **H1–H25** ported and **re-executed at HEAD** (not carried forward on trust), **R1–R21** for the round-2 surfaces, and two structural hooks — **X1** re-derives the combined finding counts, **X2** verifies this section set is intact. Each hook names the finding it binds, in [`02-blockers.md`](02-blockers.md) / [`03-agent-facing.md`](03-agent-facing.md) / [`04-misleading.md`](04-misleading.md) / [`05-cosmetic.md`](05-cosmetic.md) / [`06-operator-judgement.md`](06-operator-judgement.md) / [`07-followups.md`](07-followups.md). **No hook here targets a finding that does not appear in those files.**

**Anchor.** Round 1 recorded its hooks at `e031225`, **before** any fix. **Everything below was executed at HEAD `0af62ec`** (post-B1/B2/B3/FU-1, post-`0af62ec` proposed ADR) during the 2026-08-05→06 session, in this worktree, and **the recorded output is what it actually printed.** A hook asserting a fix is worth only what its last execution is worth.

**Why this discipline is not ceremony.** A hook written against a *mental model* of a file rather than its **literal bytes** is a named recurring trap in this repo, and [`01-diagnostics.md`](01-diagnostics.md) §3.3 records the estate's own instance: the 08-04 de-scope's §10 sweep hook certified itself against a pattern that returns **0 hits** on the artifact it most needed to reach. This pass found three more of exactly that shape — **H9** flipped green on a still-open finding, **R12** returns 17 where its own ADR says *"Expected: empty"*, and **R13** raises an IO error where it was written to print a PASS.

**Conventions.** `rg` exit code **1** with no output means **zero matches** and is recorded as such. Line numbers are as of `0af62ec`. Hooks that assert *absence* are the fragile class — re-read the file if one flips. Commands are POSIX shell (Git Bash on this machine); `rg` is ripgrep 14.1.1.

---

## Hook index

| Hook | Binds | Verdict at HEAD |
|---|---|---|
| **H1 · H2 · H3** | B1 · B2 · B3 (`02`) | ✅ **FIXED** — all three flipped |
| **H4 · H5 · H6** | gate 13 selector (C16/FU-5) · `check_adr_graph` fields · `retire_adr` (FU-6) | ❌ open, unchanged |
| **H7 · H8** | dead `validate_params` (M6/M7/C14/M25) · `REPO_MAP` codification (C3) | ❌ open, unchanged |
| **H9 ⚠** | RUNBOOK §B7/§B8 (M14/M15/M16) | ⚠ **REPAIRED** — the round-1 form now fails open |
| **H10 · H11 · H12 · H13 · H14** | desk card (M17) · lifecycle owner path (M26) · `z = −2.90` (M11/O-J) · charter counters (M2/M3) · skill surfaces (§5.10 → `03`) | ❌ open, unchanged |
| **H15** | Algorithm distribution (round-1 artifact) | ✅ reproduces exactly |
| **H16** | `deploy/` arming recipe (G9/G10 → A1) | ❌ open — see **R1** |
| **H17 · H18** | falsifier reachability (C17) · A7 (FU-7) | ❌ open, **both drifted** |
| **H19** | the de-scope's own sweep hook (M8/M44/FU-8) | ❌ open, unchanged |
| **H20 · H21** | `docs/spec/` status discipline (C18) · ledger `Last updated:` (C6) | ❌ open, unchanged |
| **H22 · H23** | M1 pin skew (M20/C19/C22) · skew sentinel (`01` §3.7) | ❌ open, unchanged |
| **H24** | the frozen set — **post-remediation guard** | ✅ baseline re-pinned |
| **H25 ⚠** | pre-decision vocabulary sweep (M44/FU-8) | ⚠ **REPAIRED** — the audit's own files inflated it |
| **R1–R21** | round-2 findings (`03`, `04`, `05`) | 21 hooks, all executed |
| **X1 · X2** | combined counts · section-set integrity | ✅ / ❌ **README absent · 37 dead refs · 1 dangling section ref** |
| **D1 · D2 · D3** | **deliberately discarded** | reasoning recorded, no hook shipped |

---

## Discards and repairs, stated up front

**Three hooks are deliberately discarded** and are written out in full at the end (**D1** the venue activity window · **D2** the sentinel field-form count · **D3** the deployed-image pin). Round 1 shipped one discard; this pass ships three, and each names an authority that lives **outside the tree**. That is the pattern worth reading: the checks this repo cannot write are the ones whose ground truth is at a venue, in a container, or behind a side effect.

**Six hooks did not support their claim on first execution and were repaired, not shipped as written.**

| # | What went wrong | Repair |
|---|---|---|
| **H9** | Round 1's `rg -c 'de-scope\|descope\|2026-08-04' RUNBOOK.md` expected **0** and now returns **1** — B1's fix (`ae5ffe7`) added the L3 Authority intercept. The count went green while **M14/M15/M16 (§B7/§B8) are untouched.** A count-based absence hook fails open the moment *any* corrective text lands. | Re-keyed to the literal §B8 sentence and the absent banners. Both forms recorded so the failure is visible. |
| **H25** | 88 → **95** files. Seven of the seven new hits are **this audit's own section files**. A rising number read as estate rot when it was the audit measuring itself. | Added `\| rg -v 'audits'`, which returns **88 — identical to round 1's baseline.** |
| **R6** | Measured whole-file, `.claude/commands/post-merge.md` looks **4** gates short; `archive_lab_analysis` appears at L40–41 in a *different* step. | Restricted to the L27–34 fallback block → **5**, matching A13 exactly. Pattern-sensitive; run the hook, do not quote a remembered number. |
| **R8** | First method was to *run* `scripts/pine_check_audit.sh`. It **POSTs to the live TradingView Guest endpoint** (its own header says so). | Replaced with a static form that reproduces the vacuity without touching the network. |
| **R12** | The ADR's own §10 command returns **17** against *"Expected: empty"*. My first diagnosis — `--all` unions with `--branches` — is **wrong**: dropping `--all` still returns 17. | Correct cause is that `--branches=cursor/*` scopes by **reachability**, and all five `cursor/*` branches have `main` merged in. Verified the prescribed `--not main` repair returns empty. |
| **R21** | The naive "unwired script" measure returns **16**, not the **22** cited in [`01-diagnostics.md`](01-diagnostics.md) §3.2 and [`07-followups.md`](07-followups.md) FU-17. | Neither number is wrong: 22 = unwired **∪ mis-scoped**, and mis-scoped is not mechanically derivable. Shipped explicitly as a **floor**. |

**Nothing was shipped aspirationally.** Every fence below was pasted from a terminal.

**One tree-state note, because it is the exact side effect D2 exists to avoid.** At the start of this pass the worktree carried an **uncommitted 60-line `## Run 2026-08-08` block** in `docs/notes/sentinel/queue.md`, left by an earlier measuring run. No section file cites its output, and [`02-blockers.md`](02-blockers.md) explicitly declines to re-run that command for this reason. It was reverted (`git checkout -- docs/notes/sentinel/queue.md`); `git status` is clean apart from this section directory. **A future-dated sentinel run block, planted three days before the gate it feeds, is a record defect — not a measurement.**

---

# §A — Round-1 hooks H1–H25, re-executed at HEAD

## H1 — B1: the GO ADR's reader-intercept. ✅ FIXED (`ae5ffe7`)

```bash
rg -c '2026-08-04|de-scope|descope' docs/adr/2026-07-17-c1-rail-build-account-registration-go.md
rg -n '^\*\*(Status|Supersedes|Superseded-by|Superseded-in-part-by):' \
   docs/adr/2026-07-17-c1-rail-build-account-registration-go.md
python scripts/check_adr_graph.py
```

```
Executed at 0af62ec:
  7                                          # was: no output, exit 1 (ZERO) at e031225
  L3 **Status:** Accepted (operator executive decision, recorded)
  L4 **Superseded-by:** none
  L5 **Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - ...
  L6 **Superseded-in-part-by:** `2026-07-22-c1-venue-native-monitoring-maturity.md` - ...
  L7 **Superseded-in-part-by:** `2026-08-04-tradeify-venue-descope-eval-included.md` -
     **DEPLOYMENT LIMB ONLY.** ... §2's authorization to *deploy* is spent. The rail build,
     the account registration, the attended-only posture, the $700 spend ceiling, and the
     arm gate all **stand** ... See the dated Addendum 2026-08-04 below.
  L11 **Supersedes:** none — this ADR **discharges** ...
  check_adr_graph: OK (enabled=['A1', 'A2', 'A3', 'A4', 'A6'])
```

**Read the L7 wording, not just the count.** The edge is scoped to the deployment limb and enumerates what still stands — which is what makes B1 closed rather than merely papered. `Superseded-by: none` at L4 is **correct and must stay**: the ADR is not wholly superseded. Residues **R-B1a** / **R-B1b** ([`07-followups.md`](07-followups.md)) are open and are *not* asserted by this hook.

## H2 — B2: the 08-08 rider enumeration. ✅ FIXED (`a818b3f`)

```bash
rg -l 'Trigger check schedule.*2026-08-08' docs/adr/ | wc -l    # the RETIRED one-liner
rg -l '2026-08-08' docs/adr/ | wc -l                            # any mention, incl. INDEX.md
rg -l 'Trigger check schedule.*2026-08-08' docs/adr/ | rg -c 'hardcore'
rg -l '\*\*Check schedule:\*\*.*2026-08-08' docs/adr/
rg -l '2026-08-08' docs/adr/2026-07-03-hardcore-p*.md
rg -c 'Trigger check schedule.*2026-08-08' STATE.md
```

```
Executed at 0af62ec:
  34                                    (was 33 at e031225 — one ADR joined the field-form class)
  56                                    (= 55 ADRs + INDEX.md; was 54 counted the same way)
  no output, exit 1                     <- STILL ZERO hardcore ADRs in the field-form set
  docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
  docs/adr/2026-07-13-prop-account-book-segregation.md
  ALL FIVE P-gates returned: p1 / p2 / p3 / p4 / p5
  no output, exit 1                     <- the under-reaching one-liner is GONE from STATE.md
```

**The fix took the second branch of round 1's own FIXED-when.** Round 1 said *"FIXED when the hardcore count is 4+ **or** the board defers to `ops.sentinel` plus a named hand-check list."* The hardcore count is **still zero** — those ADRs state their duty in prose and no pattern reaches them — so the repair is the deferral, and it landed:

```bash
rg -n 'PYTHONPATH=ops python -m sentinel|hand-check|prose-only' STATE.md
rg -n 'hardcore-p[1-5]' STATE.md
```

```
Executed:
  L49  "**36 ADRs** carry a field-form ... plus ~10 more whose duty is prose-only and which
        NO pattern reaches (see the 2026-08-08 section for the hand-check list)"
  L259 "> PYTHONPATH=ops python -m sentinel --asof 2026-08-08    # canonical; see Makefile"
  L269 "> ⚠⚠ A THIRD CLASS EXISTS THAT NO PATTERN REACHES — hand-check it. 53 ADRs mention..."
  L278-282  all five P-gates named individually in the hand-check table, with their prose quoted
```

**Round 1 said four P-gates. It is five.** `2026-07-03-hardcore-p5-source-truth-rail-gate.md` carries the same prose-only shape. Corrected in [`01-diagnostics.md`](01-diagnostics.md) §3.1 rather than quietly restated.

**The counts are not constants** — 34 / 56 moved from 33 / 54 in three commits. That is the board's own rule (*enumerate, never cite from memory*) demonstrating itself, and it is why **R-B2a** (the durable additive fix) is still owed.

## H3 — B3: the reserve denominator. ✅ FIXED (`d84c5e4`)

```bash
grep -c "cap_firm / (1" docs/spec/c1_watch_realization_multiplier_layer.md
rg -n 'cap_firm / \(1|cap_alloc\[leg\] / \(1|floor\(cap_alloc' \
   docs/spec/c1_watch_realization_multiplier_layer.md docs/spec/c1_nt8_sizing_host_impl.md
rg -n 'reserve_cap = math.floor|"cap_alloc": (69|11)' ops/c1_rail/c1_sizing_host_reference.py
rg -c '1\.91' ops/c1_rail/c1_sizing_host_reference.py
```

```
Executed at 0af62ec:
  0                                     <- the cap_firm denominator form is GONE
  c1_nt8_sizing_host_impl.md:71   reserve_cap  = floor(cap_alloc / (1 + pyr_pct / 100))
                                  # THIS LEG'S allocated share — HALT if absent (§5);
  c1_watch_realization_multiplier_layer.md:52
      qty_base = min( qty_base, floor( cap_alloc[leg] / (1 + pyr_pct/100) ) )
      # RESERVE: the add must fit under THIS LEG'S cap share
  c1_watch_realization_multiplier_layer.md:60
      "... RESERVE `floor(cap_alloc 69 / 8.5) = 8` → **8**; `qty_add = floor(8 × 7.5) = 60`.
       Matches `f2_floors.json` exactly (`legs[0].recent_90d = (8, 60)`)."
  production L91 "cap_alloc": 69   L97 "cap_alloc": 11   L296 reserve_cap = math.floor(...)
  2                                     <- the 1.91x breach comment is INTACT
```

**Three properties this hook asserts jointly, and all three matter.** The law now divides by the per-leg share in **both** specs; the worked check reproduces `f2_floors.json` at **(8, 60)** rather than the pre-split (9, 67); and **production is byte-unchanged** — `cap_alloc` 69/11, the `math.floor` at L296, and the two `1.91` breach-record comments. **This hook must never be made to pass by editing the host.**

## H4 — gate 13 is green over 6.8% of its declared corpus (C16 / FU-5). ❌ Open

```bash
python -c "
from pathlib import Path
lab = Path('lab/analysis')
print('flat glob :', len(list(lab.glob('*/RESULTS*.md'))))
print('tree      :', len(list(lab.glob('**/RESULTS*.md'))))"
rg -n 'lab.glob' scripts/check_supersession_placement.py
```

```
Executed at 0af62ec:
  flat glob : 5
  tree      : 73                        (5/73 = 6.8% — unchanged from e031225)
  L96  files += sorted(lab.glob("*/RESULTS*.md"))
```

**FIXED when** `flat == tree` **and** C16's four selector assertions pin it. A repair that widens the glob without a test pinning the selector reproduces the original defect on the next tree move.

## H5 — `check_adr_graph` is blind to two header fields the corpus uses. ❌ Open

```bash
rg -n 'FIELD_RE' scripts/check_adr_graph.py
rg -n '^\*\*(Withdraws|Withdrawn-by):' docs/adr/
```

```
Executed at 0af62ec:
  L31  FIELD_RE = re.compile(r"^\*\*(Status|Decision date|Supersedes|Superseded-by|"
  L226 m = FIELD_RE.match(line)
  2026-08-02-striker-tradeify-funded-phase-descope.md:7  **Withdrawn-by:** `2026-08-04-...`
  2026-08-04-tradeify-venue-descope-eval-included.md:9   **Withdraws:** [`2026-08-02-...`]
```

Both are silently `continue`d, so `docs/adr/INDEX.md` renders the withdrawal pair with successor `none` at both ends. **`check_adr_graph` exiting OK in H1 does not cover this** — the two hooks measure different things, and H1's green is about the reciprocal edge B1 added, not about field coverage.

## H6 — the one meta boundary crossing: a false supersession edge on `--reason withdrawn` (FU-6). ❌ Open

```bash
sed -n '209,213p' scripts/retire_adr.py
rg -n '"--reason", "withdrawn"' tests/test_retire_adr.py
```

```
Executed at 0af62ec (L209 blank; L210-212 are the defect):
      updated = set_header_field(original, "Status", f"`{token}`")
      if by_filename:
          updated = set_header_field(updated, "Superseded-by", superseded_by_value)
  tests/test_retire_adr.py:151:  "2026-01-01-old.md", "--reason", "withdrawn", "--repo-root", str(tmp),
```

The write is guarded on `by_filename` **alone**, unconditional on reason, while `_validate_supersede_precondition` runs only under `reason == "superseded"`. The only withdrawn-reason test **omits `--by`**, so the failing invocation is untested. Unchanged since `e031225`, and unchanged since the 2026-08-02 incident the tool's own victim ADR records in past tense.

## H7 — a deleted gate is still cited as live, and the gate that should catch it is green (M6 · M7 · C14 · M25). ❌ Open

```bash
ls scripts/validate_params.py core/config 2>&1
rg -n 'validate_params|core/config/params\.toml' README.md PIPELINES.md core/dd_geometry.py \
   ops/instruments/NAS100.md docs/operational_rules.md
python scripts/check_root_doc_liveness.py
```

```
Executed at 0af62ec:
  ls: cannot access 'scripts/validate_params.py': No such file or directory
  ls: cannot access 'core/config': No such file or directory
  README.md:61 | PIPELINES.md:155 | core/dd_geometry.py:30 |
  ops/instruments/NAS100.md:6 | docs/operational_rules.md:170, :310, :336      -> 7 hits / 5 files
  check_root_doc_liveness: OK - all root-doc markdown links resolve.
```

**The green line is the finding.** The gate resolves markdown links only, so a dead path inside a backtick span passes. `operational_rules` L310/L336 are **prose bodies** — check their class (Trap #12) before any edit. See **R5**: three *more* surfaces repeat this citation in `.claude/` and `.cursor/`, where nothing gates it at all.

## H8 — `REPO_MAP.md` publishes a runnable invocation of a module deleted 2026-08-02 (C3). ❌ Open

```bash
rg -n 'codification' REPO_MAP.md
ls -d lab/codification 2>&1
rg -n 'codification\.emit' REPO_MAP.md
```

```
Executed at 0af62ec:
  L42  (archive note) · L57 "**RETIRED 2026-08-02**" · L113 (no dotted path) ·
  L121 | Codification emit | `PYTHONPATH=lab python -m codification.emit …` |
  L151 "**RETIRED 2026-08-02** — Python→Pine bridge deleted"
  ls: cannot access 'lab/codification': No such file or directory
  L121  <- the `codification.emit` pattern matches ONE line, and it is the line to delete
```

⚠ **Round 1's correction to C3's own verification line still stands, re-verified.** C3 says to confirm with `rg -n 'codification\.emit'` that *"only §1 L57 and §4 L151 remain"*. Executed, that pattern matches **only L121** — L57/L151 say `codification` without `.emit`. **After the L121 deletion the stated grep returns ZERO, not two lines.** Use `rg -n 'codification' REPO_MAP.md` and expect L42/L57/L113/L151. The tombstone rows are real; the pattern C3 names to find them is not.

## H9 ⚠ REPAIRED — the RUNBOOK's §B7/§B8 exposures (M14 · M15 · M16). ❌ Open

**Round 1's form, and why it must not be re-used:**

```bash
rg -c 'de-scope|descope|2026-08-04' docs/notes/rail_build/RUNBOOK.md
# Executed at e031225: no output, exit 1 (ZERO)
# Executed at 0af62ec: 1        <- FLIPPED GREEN
```

The single hit is **L4**, added by B1's fix:

```
> ⚠ **That authority is SUPERSEDED IN PART (2026-08-04) — its DEPLOYMENT limb only.**
  [2026-08-04-tradeify-venue-descope-eval-included.md] de-scoped Tradeify as a deployment
  target **evaluation included** and withdrew both Striker ...
```

**One correct banner at the top of a 400-line desk document turned a whole-file absence hook green while every finding it was written for is untouched.** That is a fail-open, and it is the same shape [`01-diagnostics.md`](01-diagnostics.md) §3.3 diagnoses in the de-scope's own §10 sweep. **Replacement, keyed to the literal text rather than to a count:**

```bash
rg -n 'whenever attended time is available' docs/notes/rail_build/RUNBOOK.md
rg -c 'B8 .*(MOOT|SUSPENDED|barred)|§B7.*(MOOT|SUSPENDED|barred)' docs/notes/rail_build/RUNBOOK.md
```

```
Executed at 0af62ec:
  L365  "... Run it whenever attended time is available; do not block it on M1/item-5
         closing, and do not let it block M1/item-5 either."
  no output, exit 1     <- NO §B7/§B8 disposition banner exists
```

**FIXED when** the first command returns nothing **and** the second returns ≥ 1. Note what the sentence sits next to: the same section describes the test as *"real money moving on a real account"*, on an account whose disposition is open fork **F2**, wiring `sl=` for the two **withdrawn** legs. **FU-1's ruling does not discharge it** — one operator-manual token trade is not a B8 dry-fire.

## H10 — the mooted desk card lacks its own sibling's convention (M17). ❌ Open

```bash
rg -n '^# ' docs/notes/rail_build/B7_STAGE1_DESK_CARD_*.md | rg -v '^\S+:[0-9]{2,}:'
```

```
Executed at 0af62ec (4 H1s; the trailing rg -v drops in-body shell-comment lines):
  ..._2026-07-28.md:1: # B7-REFIRE Stage 1 — desk card, Tue 2026-07-28
  ..._2026-07-31.md:1: # B7 desk card — Fri 2026-07-31 (MYM only) — **SPENT**
  ..._2026-08-03.md:1: # B7 desk card — Mon 2026-08-03 (**MNQ only**)
  ..._2026-08-04.md:1: # B7 desk card — Tue 2026-08-04 (MYM **and** MNQ)
```

Exactly **one** card carries a disposition marker, and it is not the 08-04 card — which is the newest and the only one the 08-04 ADR names by date (§0 **and** §6) as mooted. **Gate 13 cannot catch this:** `scan_file` returns early on a file with no addendum heading.

## H11 — the declared canonical owner of the authorization axis points at a path that does not exist (M26). ❌ Open

```bash
rg -n 'c1_sizing_host_reference' docs/methodology/strategy_lifecycle.md | rg -o 'ops/[a-z0-9_/]*\.py' | sort -u
ls ops/c1_sizing_host_reference.py ops/c1_rail/c1_sizing_host_reference.py 2>&1
```

```
Executed at 0af62ec:
  ops/accounts.py
  ops/c1_sizing_host_reference.py       <- the LINK TARGET at both L52 and L113
  ls: cannot access 'ops/c1_sizing_host_reference.py': No such file or directory
  ops/c1_rail/c1_sizing_host_reference.py            <- the real path
```

**Read the two hits differently.** `ops/accounts.py` appears inside L52's dated correction **prose** (deleted 2026-07-24, correctly recorded — Trap #12, do not touch). The dangling one is the **link target**. The sharpest part is unchanged: L52's own 2026-08-03 amendment, which removed the `ops/accounts.py` reference, **wrote the successor without the `c1_rail/` segment** — the repair created the new dangler.

## H12 — a retracted headline is still published, and the retraction is in another file (M11 / O-J). ❌ Open

```bash
rg -n '2\.90' lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md
rg -c 'RETRACT|must not be re-quoted' lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md
rg -c 'must not be re-quoted' docs/rejected_candidates.md
```

```
Executed at 0af62ec:
  L94  "... against a prior-block mean of **+24.9, sd 26.0** ⇒ **z = −2.90**. A constant-hazard /"
  no output, exit 1                     <- ZERO intercept tokens in the RESULTS
  1                                     <- the retraction lives in docs/rejected_candidates.md
```

This cross-file shape is the one **O-J** records that **no addendum-confined gate can reach**: the retracting document is correct, the retracted document is correct history, and nothing links them.

## H13 — the always-loaded charter publishes a mutable counter and a retired seat budget (M2 / M3). ❌ Open

```bash
rg -c 'K_banked\(MNQ\)=2' CLAUDE.md
rg -c 'one Cap seat left' CLAUDE.md
```

```
Executed at 0af62ec:  1  and  1        (both inside the ORB-MNQ posture bullet, L18)
```

**FIXED when both return zero AND no substitute count replaces them.** M2/M3 forbid a new finite count — the ruling survives, the figure goes.

## H14 — four agent-instruction surfaces name the venue; none names the decision. ❌ Open

```bash
for f in $(rg -l 'Tradeify' .claude/skills/*/SKILL.md); do
  echo "$f  descope_hits=$(rg -c 'de-scope|descope|2026-08-04' "$f" || echo 0)"
done
rg -n 'sole live execution surface' .claude/skills/c1-rail/SKILL.md
```

```
Executed at 0af62ec:
  .claude/skills/trade-csv-reconcile/SKILL.md   descope_hits=0
  .claude/skills/c1-rail/SKILL.md               descope_hits=0
  .claude/skills/handoff-verify/SKILL.md        descope_hits=0
  .claude/skills/prop-firm-challenge/SKILL.md   descope_hits=0
  L8: "The sole live execution surface: TradingView alert → ops/c1_rail/c1_rail_http_server.py
       (Fly.io, thin adapter) → ... → Tradovate (Tradeify Select 100K eval)."
```

**4 of 4 name the venue, 0 of 4 name the de-scope — unchanged at HEAD.** Round 1 filed these as refutation-**untested** §5.10 candidates; round 2 tested them and they became rows **A3 · A4 · A7 · S-20** in [`03-agent-facing.md`](03-agent-facing.md) / [`04-misleading.md`](04-misleading.md). **They are now findings, not candidates.**

## H15 — re-derive the Algorithm verdict distribution (round-1 artifact). ✅ Reproduces exactly

```bash
python - <<'PY'
import io, re, collections
A = 'docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md'
txt = io.open(A, encoding='utf-8').read().splitlines()
TOK = re.compile(r'(KEEP-CORRECTED|KEEP-AS-IS|SIMPLIFY|DELETE)(\s*(?:×|x)\s*(\d+))?')
sec, per, tot = 'pre', collections.defaultdict(collections.Counter), collections.Counter()
for ln in txt:
    m = re.match(r'^#{1,3} §([\d.]+)', ln)
    if m: sec = m.group(1)
    if not ln.startswith('| '): continue
    c = ln.split('|')
    if len(c) < 6: continue
    for t, _, n in TOK.findall(c[4]):          # column 4 == the Verdict cell
        k = int(n) if n else 1
        per[sec][t] += k; tot[t] += k
for s in sorted(per): print('S'+s, dict(per[s]), '=', sum(per[s].values()))
print('ROW-TOKEN TOTAL', dict(tot), '=', sum(tot.values()))
PY
rg -c '^\| \*\*O-.*Adjudicated' \
   docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md
```

```
Executed at 0af62ec — byte-identical to the e031225 run:
  S5.1 {'KEEP-CORRECTED': 2, 'SIMPLIFY': 1} = 3
  S5.2 {'KEEP-CORRECTED': 4, 'DELETE': 5, 'SIMPLIFY': 2} = 11
  S5.3 {'KEEP-CORRECTED': 8, 'SIMPLIFY': 6, 'DELETE': 4} = 18
  S5.4 {'SIMPLIFY': 1, 'KEEP-CORRECTED': 5, 'DELETE': 4} = 10
  S5.5 {'KEEP-CORRECTED': 2, 'SIMPLIFY': 2} = 4
  S5.6 {'DELETE': 8, 'KEEP-CORRECTED': 12, 'SIMPLIFY': 13} = 33
  S5.7 {'SIMPLIFY': 4, 'DELETE': 4, 'KEEP-CORRECTED': 5} = 13
  ROW-TOKEN TOTAL {'KEEP-CORRECTED': 38, 'SIMPLIFY': 29, 'DELETE': 25} = 92
  KEEP-AS-IS (§5.8 anchor) = 2
```

⚠ **The anchor is load-bearing.** The obvious pattern `Adjudicated .KEEP-AS-IS.` returns **3** in the round-1 artifact, because the hook's own printed command line matches itself. `^\| \*\*O-` confines it to §5.8 table rows.

**What it reproduces, and what it does not.** It confirms the ordering (KEEP-CORRECTED > SIMPLIFY > DELETE ≫ KEEP-AS-IS) at every level, confirms `KEEP-AS-IS = 2` independently, and confirms §5.7's *"13 findings across 11 rows"* exactly. **It does not reproduce ≈66 / ≈36 / ≈34**, and the reason is structural: §5 groups by **target file**, so most rows carry several findings under one verdict token without `×N` notation (**M21** = *"Six findings, one file"* under a single `SIMPLIFY`). **92 is a floor, not the distribution.** Quote §2's hand tally with its ±2, or quote this floor and say which. **X1 is the successor hook for the split section set.**

## H16 — an arming recipe with neither binding gate in view (G9 / G10 → A1). ❌ Open

```bash
rg -n 'dry_run|B6' deploy/c1_rail/README.md | head -8
rg -c 'M1|de-scope|descope|2026-08-04' deploy/c1_rail/README.md
grep -c "dry_run" deploy/c1_rail/README.md
```

```
Executed at 0af62ec:
  L5  "**Nothing here arms trading.** `dry_run` stays `true` and `equity_source` stays `file`
       until the GO ADR's B6 dry-fire passes. This runbook only stands the host up."
  L69 fly logs -a c1-rail-<suffix>   # expect "listening on ...  dry_run=True equity_source=file"
  L76 "Leave TV alerts **unarmed** and `dry_run: true` until B6."
  L78 "## B6 → arming (later)"
  L82 "4. Only then flip `dry_run: false` (edit the config on the volume, restart)."
  no output, exit 1                   <- ZERO M1 / de-scope / 08-04 references
  4                                   <- four dry_run references
```

**B6 PASSED 2026-07-20**, so by L5's own terms its restraint reads **discharged**, and the four numbered steps then read live. Round 1's highest-priority §5.10 row; round 2 confirmed it as **A1** (7 findings, one file) and it is **FU-14**, the highest open consequence in [`07-followups.md`](07-followups.md). **R1** carries the full round-2 form.

## H17 — falsifier coverage is a minority and eroding (C17). ❌ Open, and it drifted

```bash
python scripts/check_falsifier_reachability.py --stats
```

```
Executed at 0af62ec:
  ADRs scanned              : 108        (e031225: 107)
  carrying a falsifier      : 84         (e031225: 83)
  with a runnable anchor    : 22 (26%)   (e031225: 21 / 25%)
    -> 62 falsifiers are prose-only and UNCHECKABLE here
  findings                  : 0 | exempted : 9
  check_falsifier_reachability: OK (22 anchored falsifier(s), 0 findings, 9 exempted)
    NOTE: green != all falsifiers in force. Prose-only limbs and retired-duty limbs are
          invisible to this check (see module docstring).
```

**Three readings in three days: 28% (2026-08-02 docstring) → 25% (`e031225`) → 26% (HEAD).** The corpus keeps adding falsifier sections faster than it anchors them, and **62 prose-only limbs is the number that has not moved.** C17's remedy stands: delete the hand-maintained numeric census from the docstring and state the direction, because a census that must be edited by hand is the class this audit is about.

## H18 — a falsifier with four live findings and no owner (FU-7). ❌ Open, and its anchors moved

```bash
python scripts/check_adr_graph.py --enable A7
rg -l 'A7' Makefile scripts/githooks/pre-commit .github/workflows/
```

```
Executed at 0af62ec:
  HARD: STATE.md:234  A7 cites 2026-08-02-pepperstone-feed-retirement.md, superseded by
        ['2026-08-03-bar-data-cfd-and-candidates-retirement.md'] -- bullet does not name it
  HARD: STATE.md:236  A7 cites 2026-07-11-challenge-era-claims-rescope.md, superseded by
        ['2026-07-22-challenge-era-substrate-retirement.md'] -- bullet does not name it
  HARD: STATE.md:315  A7 cites 2026-07-12-prop-portfolio-four-friendly-firms.md, superseded by
        [3 ADRs] -- bullet does not name the superseding ADR
  HARD: STATE.md:322  A7 cites 2026-07-11-ops-cfd-estate-retirement.md, superseded by
        ['2026-07-22-challenge-era-substrate-retirement.md'] -- bullet does not name it
  check_adr_graph: 4 finding(s).   exit=1
  second command: no output, exit 1   <- A7 appears in ZERO wiring files
```

**Same four findings; the line numbers moved 233/235/268/275 → 234/236/315/322** because B2's fix inserted the hand-check table into `STATE.md`. **Cite the finding, not the line.** A check that returns four HARD findings at HEAD and is excluded from `DEFAULT_ENABLED_CHECKS` is FU-7's whole case: own it or tombstone it.

## H19 — the de-scope's own sweep hook cannot surface an untouched file (M8 · M44 · FU-8). ❌ Open

```bash
rg -c "chain rate|acct-mo|funded phase|Select Flex|live c1 leg|LIVE c1 leg" \
   CLAUDE.md STATE.md ops/instruments/MYM.md ops/instruments/MNQ.md
rg -c "chain rate|acct-mo|funded phase|Select Flex|live c1 leg|LIVE c1 leg" \
   docs/spec/2026-07-27-third-leg-target-spec.md
```

```
Executed at 0af62ec (the ADR §10 hook 3 pattern, verbatim):
  CLAUDE.md:1   ops/instruments/MYM.md:1   ops/instruments/MNQ.md:1   (STATE.md: nothing)
  third-leg spec: no output, exit 1        <- ZERO hits
```

The hook reaches 3 of its own 4 declared files and **0** on the estate's most consequential stale artifact. **Widening the file list changes nothing** — the pattern is keyed to the *decision's* vocabulary, and derived documents share no token with it. That is the defect **M44 / FU-8** repairs at the authoring surface, and **H25 / X1** are the sweep shape that replaces it.

## H20 — `docs/spec/` has no status discipline to gate (C18). ❌ Open

```bash
ls docs/spec/*.md | wc -l
for f in docs/spec/*.md; do rg -q '^\*\*Status:\*\*' "$f" || echo "NO-STATUS: $f"; done | wc -l
```

```
Executed at 0af62ec:  28 files;  11 lack a line-initial **Status:** field.
```

⚠ **PATTERN-SENSITIVE, and C18's prose says 10.** With `\*\*Status` (any position) only **6** lack it; only **2** files contain no `status` token at all. **Run the hook; do not quote the prose number.** C18's remedy (add `Status` to the gap, triage all 28, defer any new checker as a *recorded decision*) is unaffected by which count is used — **but the triage list is not.**

## H21 — the hand-maintained ledger date has drifted, and the audit's own named set is not the one it drifts on (C6). ❌ Open

```bash
python - <<'PY'
import io, re, glob, os
n, bad = 0, []
for f in sorted(glob.glob('ops/instruments/*.md')):
    t = io.open(f, encoding='utf-8').read()
    m = re.search(r'\*\*Last updated:\*\*\s*(\d{4}-\d{2}-\d{2})', t)
    if not m: continue
    n += 1; hdr = m.group(1)
    parts = t.split('## SESSION LOG', 1)
    if len(parts) < 2: continue
    ds = re.findall(r'^- \*\*(\d{4}-\d{2}-\d{2})', parts[1], re.M)
    if ds and max(ds) > hdr: bad.append((os.path.basename(f), hdr, max(ds)))
print('ledgers carrying **Last updated:** =', n)
for b in bad: print('STALE', b)
print('stale =', len(bad))
PY
```

```
Executed at 0af62ec:  20 ledgers carry the field; stale = 4
  ('6J.md','2026-08-02','2026-08-04')   ('M2K.md','2026-07-27','2026-07-30')
  ('MNQ.md','2026-08-04','2026-08-05')  ('MYM.md','2026-07-29','2026-08-04')
```

⚠ **The COUNT reproduces C6's "four of twenty"; the NAMED SET does not** — C6's parenthetical names MYM, M2K, NQ and NAS100, and **two of the four differ.** Run the hook; do not remediate from the parenthetical. C6's verdict (**DELETE** the field, or **generate** it in `instrument_profiles.py --check`) is unchanged either way — which is the point: a hand-maintained freshness stamp drifts faster than the audits that check it.

## H22 — the M1 pin's skew note is wrong about its own cause (M20 · C19 · C22). ❌ Open

```bash
python scripts/validate_c1_monitoring_acceptance.py \
  docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --check-tree-skew
```

```
Executed at 0af62ec:
  OK status=CODE_LANDED path=docs\notes\rail_build\M1_MONITORING_ACCEPTANCE.json
  NOTE: M1 is not RESOLVED - next dry_run=false entry/add send remains gated.   <- C19/C22: SEND-shaped
  tree skew: 5 of 6 pinned file(s) differ from this tree (deployed pin -> tree):
    ops/c1_rail_arm.py / c1_rail_http_server.py / c1_rail_listener.py /
    c1_rail_telemetry.py / c1_sizing_host_reference.py     — every one "tree MISSING"
  This is drift, not corruption: fixture_hashes describes the DEPLOYED build ...
  A redeploy MUST refresh the pin in the same motion, from hashes read in-container.
```

**The cause is the 2026-08-03 move to `ops/c1_rail/` (commit `2345095`) — not content drift and not CRLF/LF.** M20 corrects the **prose only**: do not re-hash, do not re-pin, do not re-path here. The `NOTE:` string is the fourth surface in the send-vs-arm cluster (Addendum 2026-07-31b moved the trigger **send → arm**). **D3** records why the *deployed* side of this cannot be hooked at all.

## H23 — the skew sentinel fails open, and its empty result is indistinguishable from a clean corpus. ❌ Open

```bash
rg -n 'canonical_needle' ops/sentinel/scan.py
rg -c 'p99 DD 0\.63pp headroom' CLAUDE.md
```

```
Executed at 0af62ec:
  ops/sentinel/scan.py:78    "canonical_needle": "p99 DD 0.63pp headroom",
  ops/sentinel/scan.py:101   needle = chk["canonical_needle"]
  no output, exit 1          <- ZERO occurrences in CLAUDE.md
```

The guard `if needle not in claude: continue` then skips the only registered check, so `skew_scan` returns `[]` from a registry that resolves to **zero live checks**. Compounded by the documented invocation throwing (`01` §3.1 limb 5): the scanner is unreachable to a reader following the published instruction **before** it is uninformative to one who is not.

## H24 — the frozen set, as a post-remediation guard. ✅ Baseline re-pinned at HEAD

Run this **after** any commit executing a row in `03` / `04` / `05`. It asserts the surfaces [`06-operator-judgement.md`](06-operator-judgement.md) §6 and the round-1 §6.1 freeze. **A failure means the remediation exceeded its mandate.**

```bash
rg -n '^DD_TRIGGER|^DD_SCALE' core/dd_protection.py
rg -n 'TIER_MULTIPLIER = |"AUTHORIZED":|"WATCH-1":' core/lifecycle.py | head -4
ls core/lifecycle_state.json 2>&1
rg -n '"cap_alloc": (69|11)' ops/c1_rail/c1_sizing_host_reference.py
rg -c '3\.0%' docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
rg -o '≥ 50%|1\.0%' docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | sort | uniq -c
```

```
Executed at 0af62ec — IDENTICAL to the e031225 baseline. Every later run must match:
  L78 DD_TRIGGER = 0.015    # 1.5% DD from peak triggers scaling
  L79 DD_SCALE = 0.40       # multiply risk by 0.40x when triggered
  L33 TIER_MULTIPLIER = {   L34 "AUTHORIZED": 1.00   L35 "WATCH-1": 0.50
  L180 expected = {"AUTHORIZED": 1.00, "WATCH-1": 0.50, "WATCH-2": 0.25, "RETIRED": 0.00}
  ls: cannot access 'core/lifecycle_state.json'   (=> both Striker keys default to 1.00x)
  L91 "cap_alloc": 69       L97 "cap_alloc": 11
  11 occurrences of 3.0% ;  5x "≥ 50%" ;  5x "1.0%"
```

**Four fix commits and a proposed ADR landed between the two runs and this hook did not move a byte.** That is the audit's own boundary claim ([`01-diagnostics.md`](01-diagnostics.md) §3.5), measured rather than asserted.

## H25 ⚠ REPAIRED — the pre-decision vocabulary sweep, as a baseline to diff against (M44 / FU-8)

This is the **shape** M44 prescribes for Phase 2 — grep the configuration that was true **before** the decision, not the decision's own words. It is a **triage surface, not a pass/fail gate**: every hit still needs the four refutation questions before it is a finding.

```bash
rg -l 'live c1|live 2-leg|2-leg book|MYM 69|cap_alloc.*69|69 / 11|69/11' \
   CLAUDE.md STATE.md README.md PIPELINES.md REPO_MAP.md docs/ ops/ core/ .claude/ deploy/ | wc -l
rg -l 'live c1|live 2-leg|2-leg book|MYM 69|cap_alloc.*69|69 / 11|69/11' \
   CLAUDE.md STATE.md README.md PIPELINES.md REPO_MAP.md docs/ ops/ core/ .claude/ deploy/ \
   | rg -v 'audits' | wc -l
rg -c 'live c1|live 2-leg|2-leg book|MYM 69|69/11' CLAUDE.md STATE.md README.md PIPELINES.md
```

```
Executed at 0af62ec:
  95        <- raw, and MISLEADING: see below
  88        <- excluding docs/notes/audits/**  == round 1's e031225 baseline, exactly
  README.md:1   STATE.md:4   CLAUDE.md:5   PIPELINES.md:1
```

⚠ **The repair, and it matters more than the number.** The raw form rose 88 → 95, and **all seven new hits are this audit's own files** — the round-1 artifact plus six of the seven section files. An audit that greps for the pre-decision vocabulary *while writing about the pre-decision vocabulary* counts itself. Without the `rg -v 'audits'` exclusion, the next sweep reads a **+7 estate regression** that never happened.

**Recorded so the next sweep has a number to diff against, not so 88 can be quoted as a finding count.** Note what the 88 includes and must keep including: dated history, correct records, and the corrected sites themselves. **A falling number is not automatically progress — Trap #12 cuts both ways.**

---

# §B — Round-2 hooks R1–R21

Round 2 swept seven surfaces round 1 never opened. These bind the findings in [`03-agent-facing.md`](03-agent-facing.md) (rows `A1`–`A49`), [`04-misleading.md`](04-misleading.md) (`RDB-*`, `SP-*`, `S-*`, `LAB-*`) and [`05-cosmetic.md`](05-cosmetic.md) (`C32`–`C45`). **Every round-2 finding carries slightly lower evidential standing than round 1's** — stated once, in `README.md`, and not repeated per hook. What is *not* lower-standing is the output below: it was executed here.

## R1 — A1 / FU-14: the arming recipe, in full. ❌ Open — highest consequence

Extends **H16**. Three properties, because A1 requires the parts to co-land:

```bash
grep -c "dry_run" deploy/c1_rail/README.md
rg -c 'M1|de-scope|descope|2026-08-04' deploy/c1_rail/README.md
sed -n '78,82p' deploy/c1_rail/README.md
rg -n 'm1_acceptance_reason' ops/c1_rail/c1_rail_arm.py | head -2
rg -n 'armed_until' deploy/c1_rail/c1_rail_config.fly.example.json ; rg -n 'armed_until' deploy/c1_rail/README.md
```

```
Executed at 0af62ec:
  4                                     <- four dry_run references
  no output, exit 1                     <- ZERO references to EITHER binding bar
  L78 "## B6 → arming (later)"
  L82 "4. Only then flip `dry_run: false` (edit the config on the volume, restart)."
  c1_rail_arm.py:78   def m1_acceptance_reason(path: Path | None = None) -> str | None:
  c1_rail_arm.py:136      m1_reason = m1_acceptance_reason(acceptance_path)
  template L20  "armed_until": null,
  template L19  "... REQUIRED whenever dry_run is false: the host refuses to boot armed
                 without a valid future value ... null while disarmed."
  README.md     no output, exit 1       <- the README never mentions armed_until AT ALL
```

**FIXED when** the second command returns ≥ 1 **and** L78–82 is a dated tombstone. **Do not fix it by adding a caveat below L82** — A1's standard is that the instruction be *safe to follow literally*, and an agent does not scroll past an executable step to find a warning.

**The guard that bounds this row, and why the bound is not comfort.** `m1_acceptance_reason` refuses the write while M1 reads `CODE_LANDED`; the shipped template's `armed_until: null` means the lone L82 edit boots the host **DISARMED**; and `.claude/skills/c1-rail/SKILL.md` invariant 2 declines `--arm` under any authorization. **Three of those are one guard away from the recipe being live, and two of the three are themselves audited findings in this set.**

## R2 — A3 / FU-15: the skill routes agents to the wrong ledgers, and the wrong ledgers contradict the right ones. ❌ Open

```bash
rg -n 'ops/instruments/(YM|NQ)\.md' .claude/skills/c1-rail/SKILL.md
rg -n '^\*\*Status:\*\*' ops/instruments/YM.md ops/instruments/NQ.md | rg -c 'LIVE c1 leg|live c1 rail leg'
rg -c 'Status amendment \(2026-08-04\)' ops/instruments/YM.md ops/instruments/NQ.md
rg -c 'NO LONGER A LIVE c1 LEG' ops/instruments/MYM.md ops/instruments/MNQ.md
```

```
Executed at 0af62ec:
  L63  "- Instrument ledgers: `ops/instruments/YM.md` (MYM) + `ops/instruments/NQ.md` (MNQ)
        — rule 10 read-before-touch applies."
  2                        <- BOTH parent Status lines still assert a live leg:
     YM.md:4  "Micro sibling [MYM.md] is a **LIVE c1 leg (disarmed)** on Tradeify Select 100K."
     NQ.md:4  "**MNQ is a live c1 rail leg (disarmed)** + hosts the parked ORB-MNQ CANDIDATE."
  no output, exit 1        <- NEITHER parent carries an 08-04 status amendment
  MYM.md:1  MNQ.md:1       <- the CORRECT ledgers carry the dated withdrawal
```

**The mandatory Rule-10 read is routed to the two files the 08-04 §6 sweep did not touch, while the two it did touch are not named.** This is the sharpest single row in `03`. **FIXED when** command 1 names `MYM.md`/`MNQ.md`, command 3 returns 2, and the parents' original Status prose is **preserved as record** (append, never edit — Trap #12).

## R3 — A14: a hookify warn on the most protected constants in the repo names two dead verifications. ❌ Open

```bash
ls tests/core/test_mc_anchors.py 2>&1
rg -n 'test_mc_anchors|portfolio_mc' .claude/hookify.locked-sizing-const.local.md
ls tests/core/test_mc_synthetic_engine.py scripts/verify_lock_anchors.py 2>&1
git check-ignore -v .claude/hookify.locked-sizing-const.local.md
```

```
Executed at 0af62ec:
  ls: cannot access 'tests/core/test_mc_anchors.py': No such file or directory
  L19  `tests/core/test_mc_anchors.py`.
  L23  - Any change requires **re-running `portfolio_mc` + a lock decision brief**.
  scripts/verify_lock_anchors.py            <- the live substitute, present
  tests/core/test_mc_synthetic_engine.py    <- the live substitute, present
  .gitignore:48:.claude/*.local.md	.claude/hookify.locked-sizing-const.local.md
```

**Both named verifications are dead** (`test_mc_anchors.py` deleted 2026-07-24 substrate Phase 3; `portfolio_mc` hard-exits on an empty `PANELS_BY_BROKER`) and **both live substitutes exist and are unnamed.** The warn overstates machine coverage at the edit where false assurance costs most.

⚠ **The last line is the operator flag, mechanically confirmed: this file is gitignored, so the fix cannot land in a PR.** FU-16's second limb is exactly this class.

## R4 — A16: the Cursor-side hook has been dead since it landed, and silent by construction. ❌ Open

```bash
sed -n '18,20p' .cursor/hooks/after_file_edit.py
python -c "
from pathlib import Path
p = Path('.cursor/hooks/after_file_edit.py').resolve()
print('parents[1] =', p.parents[1]); print('  scripts/ exists:', (p.parents[1]/'scripts').exists())
print('parents[2] =', p.parents[2]); print('  scripts/ exists:', (p.parents[2]/'scripts').exists())"
```

```
Executed at 0af62ec:
  def _repo_root() -> Path:
      # .cursor/hooks/after_file_edit.py → repo root is parents[1]
      return Path(__file__).resolve().parents[1]
  parents[1] = <root>\.cursor          scripts/ exists: False      <- the defect
  parents[2] = <root>                  scripts/ exists: True       <- the fix
```

`if not script.exists(): return` therefore fires for **both** targets, so neither `scripts/lock_event_hook.py` nor `scripts/sync_skills_hook.py` has ever run from the Cursor surface — dead since `f10aeea` (2026-07-12). **The absence of complaints is not evidence of no consumer:** fail-open plus an `exists()` early-out means nobody *could* have noticed. **A16's second edit — make the miss loud — is the part that must land**, or the next path bug survives another 24 days.

## R5 — A18 / A15 / A17: a retired gate cited as live on three agent surfaces, while a fourth records its retirement correctly. ❌ Open

```bash
rg -n --no-ignore 'validate_params' .cursor/ .claude/
```

```
Executed at 0af62ec:
  .cursor/rules/locked-params.mdc:40   "(`validate_params.py`) were **retired 2026-08-03**"   <- CORRECT
  .cursor/rules/git-workflow.mdc:25    "- Pre-commit runs `validate_params`, data manifest ..."  <- STALE
  .cursor/hooks/before_shell.py:78     "(validate_params + data/pine manifests). Not the standing " <- STALE
  .claude/hookify.no-verify-commit.local.md:13  "load-bearing gates: `validate_params` + ..."  <- STALE
```

**The repo contradicts itself across four agent surfaces, one of which is executable and one of which is gitignored.** Add **H7**'s five tracked doc sites and this single retirement (2026-08-03, `755d07f`) left **eight** live citations across two layers. **Do not repair by re-pinning an accurate list** — A15/A17/A18 all prescribe replacing the enumeration with a pointer to `scripts/githooks/pre-commit`, because nothing gates a `.cursor/` file and it will rot again.

## R6 ⚠ REPAIRED — A13: the post-merge fallback is five gates short of `make check`. ❌ Open

```bash
python - <<'PY'
import re, pathlib
mk = pathlib.Path('Makefile').read_text(encoding='utf-8')
chain = ['validate-data','validate-pine','skills-check','skills-no-constants','boundaries',
         'path-liveness','root-doc-liveness','status-consistency','adr-graph',
         'lab-catalog-check','instrument-profiles']
make_scripts = set()
for t in chain:
    body = re.search(rf'^{re.escape(t)}:.*\n((?:\t.*\n)+)', mk, re.M).group(1)
    make_scripts |= set(re.findall(r'scripts/(\w+)\.py', body))
pm = pathlib.Path('.claude/commands/post-merge.md').read_text(encoding='utf-8').splitlines()
fb = set(re.findall(r'scripts/(\w+)\.py', '\n'.join(pm[26:34])))   # the L27-34 fallback block
print('make check reaches       :', len(make_scripts), sorted(make_scripts))
print('fallback block runs      :', len(fb), sorted(fb))
print('MISSING from the fallback:', len(make_scripts - fb), sorted(make_scripts - fb))
PY
```

```
Executed at 0af62ec:
  make check reaches       : 11 [archive_lab_analysis, check_adr_graph, check_boundaries,
     check_data_manifests, check_path_liveness, check_pine_manifest, check_root_doc_liveness,
     check_skill_refs, check_skills_no_constants, check_status_consistency, instrument_profiles]
  fallback block runs      : 6  [check_boundaries, check_data_manifests, check_path_liveness,
     check_pine_manifest, check_skill_refs, check_skills_no_constants]
  MISSING from the fallback: 5  [archive_lab_analysis, check_adr_graph, check_root_doc_liveness,
     check_status_consistency, instrument_profiles]
```

⚠ **Repair note, and it is the reason the hook is scoped to lines 26:34.** Measured over the whole file the answer is **4**, because `archive_lab_analysis` appears at **L40–41** in a *different* step. A13's "five gates" is right about the fallback block and wrong about the file. **The failure mode is a false green:** §7's single `make check | pass/fail` row records a five-gate-short run as a full pass, and the two missing gates include **both doc-rot gates a post-merge pass exists to run.**

## R7 — A20: an advertised refusal the code no longer performs, and the one finding that *mints* stale text. ❌ Open, unguarded

```bash
sed -n '14p' scripts/m1_item5_capture.py
rg -n '^ITEM5_LEGS|^LEG_MYM|^LEG_MNQ' scripts/m1_item5_capture.py
sed -n '388,392p' scripts/m1_item5_capture.py
```

```
Executed at 0af62ec:
  L14   Refuse paths (exit 2): qty 0 / floored, non-MYM, non-entry, incomplete triad,
  L40   LEG_MYM = "dj30_mym"
  L50   ITEM5_LEGS = (LEG_MYM, LEG_MNQ)          <- MNQ has been ACCEPTED since 2026-08-02
  L390  "M1 §4 item 5 non-zero MYM dry_run strategy entry + prior items "
        "6/10/drills; next dry_run=false send still needs a separate GO."
```

**Two distinct defects in one file.** L14 is the docstring `argparse` prints as `--help`, advertising a `non-MYM` refusal the code stopped performing — **the failure mode is inaction**, a reader holding a real MNQ triad concludes the tool rejects it, and **no guard catches inaction.** L390 is the only finding in either round that **writes** fresh false text: a hardcoded `MYM` provenance string into `operator_signoff.note`, i.e. into the artifact `c1_rail_arm.py` reads as the arming gate and the `Dockerfile` bakes into the image.

## R8 ⚠ REPAIRED — A23 / A24 / A25 / A26: one directory move, three broken selectors, all silent. ❌ Open

The 2026-08-04 Phase-A cold-store moved the locked Pine bodies to `core/strategies/_archive/<family>/`. **Three independent selectors still point at the pre-move layout, and none of them fails loudly.**

```bash
# (a) A24/A25 — the pine_check regression oracle. STATIC form: the script POSTs to a LIVE
#     third-party endpoint, so it is deliberately NOT executed here.
python - <<'PY'
import re, pathlib
sh = pathlib.Path('scripts/pine_check_audit.sh').read_text(encoding='utf-8')
oracle = re.findall(r'"(core/strategies/[^"]+\.pine)"', sh)
print('oracle entries in .sh :', len(oracle), '| resolvable:', sum(pathlib.Path(p).is_file() for p in oracle))
ps = pathlib.Path('scripts/pine_check_audit.ps1').read_text(encoding='utf-8')
o2 = re.findall(r"'(core/strategies/[^']+\.pine)'", ps)
print('oracle entries in .ps1:', len(o2), '| resolvable:', sum(pathlib.Path(p).is_file() for p in o2))
PY
# (b) A23 — the worktree-sync gate target.
rg -n '^LOCKED_GLOB' scripts/sync_pine_to_worktree.py
# (c) A26 — the pine_lint locked-write refusal.
sed -n '53,58p' scripts/pine_lint.py
```

```
Executed at 0af62ec (this WORKTREE — .pine bytes are gitignored and live in the MAIN tree):
  oracle entries in .sh : 4 | resolvable: 0
  oracle entries in .ps1: 4 | resolvable: 0
  L55  LOCKED_GLOB = "core/strategies/*/*.pine"   # the locked strategy Pine (--check gate target)
  L53-58  LOCKED_DIRS = (REPO_ROOT/"core"/"strategies"/{"guardian","striker","aegis","nas"})
```

⚠ **The absence is NOT a worktree artifact — that is the whole finding, and it required leaving the worktree to establish.** Re-run in the **main** checkout, where the Pine bytes exist:

```
Executed at C:\Users\joshu\multi_firm_operations (MAIN tree, 0af62ec):
  core/strategies/guardian/guardian_gold_v5.5.pine     ABSENT
  core/strategies/striker/striker_dj30_v4.5.pine       ABSENT
  core/strategies/aegis/aegis_usdjpy_v4.3.pine         ABSENT
  core/strategies/nas/striker_nas100_v1.pine           ABSENT
  core/strategies/_archive/guardian/guardian_gold_v5.5.pine    PRESENT
  core/strategies/_archive/striker/striker_dj30_v4.5.pine      PRESENT
  core/strategies/_archive/aegis/aegis_usdjpy_v4.3.pine        PRESENT
  core/strategies/_archive/nas/striker_nas100_v1.pine          PRESENT
  .pine under LOCKED_DIRS : 0        .pine under _archive/* : 17
  `core/strategies/*/*.pine` (LOCKED_GLOB) matches: 0    `_archive/*/*.pine` matches: 17
```

**Read each consequence separately, because they differ in kind.**
- **A24/A25** — the audit prints `SKIP (absent)` four times and then `== audit PASS ==`, having regression-tested **zero** locked strategies. The `skip-if-absent` branch never sets `fail`. The scripts' own headers blame worktrees; **the paths are wrong in the main tree too**, so that explanation has expired.
- **A23** — the `--check` gate target matches nothing, so the sync gate cannot fail.
- **A26 is the safety-relevant one** — `LOCKED_DIRS` guards four directories holding **0** `.pine`, while **17** sit unguarded under `_archive/`. A write to `core/strategies/_archive/guardian/guardian_gold_v5.5.pine` is **not refused**.

**The guard that bounds A26, verified in the main tree:**

```bash
head -4 core/strategies/MANIFEST.sha256 ; python scripts/check_pine_manifest.py
```

```
Executed (MAIN tree):
  d8c1188...  core/strategies/_archive/aegis/aegis_usdjpy_v4.3.pine     <- MANIFEST pins _archive paths
  WARN EXTRA core/strategies/_archive/candidates/{3 candidate files}    (on disk, not pinned)
  exit 0
```

**`check_pine_manifest` is always-on in pre-commit and does cover the moved bodies** — which is why A26 is MISLEADING and not BLOCKER. The `pine_lint` refusal is redundant belt that stopped binding; the manifest is what actually holds.

## R9 — A22: a dead default export directory behind a fail-closed exit. ❌ Open

```bash
rg -n '^DEFAULT_EXPORT_DIR' scripts/parse_bar_export.py
ls core/data/tv_exports/ ; ls -d core/data/tv_exports/pepperstone 2>&1
sed -n '50,55p' scripts/parse_bar_export.py
```

```
Executed at 0af62ec:
  L31  DEFAULT_EXPORT_DIR = REPO_ROOT / "core"/"data"/"tv_exports"/"pepperstone"/"bar_export"
  cme                                                    <- the only surviving panel dir
  ls: cannot access 'core/data/tv_exports/pepperstone': No such file or directory
  L51-55   missing = [p for p in in_paths if not p.exists()]
           if missing: print(f"=== missing TV export: {p} ===", file=sys.stderr); return 2
```

**This is the good failure mode and it is worth naming as such.** The default is dead, but the tool **exits 2 naming the exact missing path** rather than silently producing nothing. That is what bounds A22 to COSMETIC. Contrast **R8(a)**, where the same "input absent" condition prints `PASS`.

## R10 — A27: `repo_hygiene`'s orphan-worktree scan is scoped to a path that does not exist where it runs. ❌ Open

```bash
rg -n '^WORKTREE_PARENT|^REPO_ROOT' scripts/repo_hygiene.py
python -c "
import pathlib; r=pathlib.Path('.').resolve()
print('worktree parent exists HERE (a worktree):', (r/'.claude'/'worktrees').is_dir())"
```

```
Executed at 0af62ec:
  L27  REPO_ROOT = Path(__file__).resolve().parent.parent
  L28  WORKTREE_PARENT = REPO_ROOT / ".claude" / "worktrees"
  worktree parent exists HERE (a worktree): False
  (MAIN tree: True)
```

Run from inside a worktree — which is where a hygiene pass is most likely to be run after a batch of merges — `_orphan_dirs` scans a directory that is not there and reports none. **Bounded by repo-hygiene rule 1** (report-only; deletion requires explicit operator confirmation): an omission shortens a prune list, it never deletes.

## R11 — A8 / A12: a numbering convention dropped 2026-07-17 is still the authoring default. ❌ Open

```bash
rg -n --no-ignore 'ADR-NNN|docs/adr/NNN-' .claude/skills/ | rg -v 'there is no|were dropped' | wc -l
rg -c --no-ignore 'no `ADR-NNN` numbering' .claude/skills/brief-authoring/references/adr.md
ls docs/adr/ | rg -c '^[0-9]{3}-'
sed -n '113,117p' scripts/check_skill_refs.py
```

```
Executed at 0af62ec:
  11        <- sites USING the dead convention, across SKILL.md + 5 reference templates
  2         <- sites in the SAME bundle recording that it was dropped
  exit 1    <- ZERO three-digit-prefixed ADRs exist
  L114  _PLACEHOLDER_RE = re.compile(
  L115      r"<[^>]*>|\{[^}]*\}|YYYY|MM\b|DD\b|NNN|\*|(?<![A-Za-z])X(?![A-Za-z])"
```

**Eleven use sites against two record sites, in one skill bundle.** And the mechanical gate cannot catch it: `NNN` is inside `_PLACEHOLDER_RE`, so **every `ADR-NNN` token is discarded before evaluation** by `check_skill_refs`. A8's L91 is the last instruction read before a filename is chosen, and it sits *upstream* of the bundled template that corrects it.

## R12 ⚠ REPAIRED — A30: the only mechanical locked-surface containment check for the Cursor lane fires on ordinary merged history. ❌ Open

**The ADR's own §10 command, run verbatim:**

```bash
git log --all --oneline --since=2026-07-14 --author=. --branches="cursor/*" -- \
  core/dd_protection.py core/firm_rules.py core/portfolio_mc.py core/mc/ core/lifecycle.py core/dd_geometry.py
```

```
Executed at 0af62ec — its stated expectation is "Expected: empty":
  17 commits, including 8ec740d, bda9ad9, 2345095, fc14682, bd92d8e, ff3510d, f8f8db1 ...
```

**My first diagnosis was wrong and is recorded as wrong.** Dropping `--all` returns **17 again**, so `--all` is not the operative cause. Measured:

```bash
git branch -a --list 'cursor/*' | wc -l           # 5
git branch -a --contains bd92d8e | head -5        # analysis/..., chore/..., claude/... — it is on main lineage
git log --oneline --since=2026-07-14 --branches="cursor/*" --not main -- <the six locked paths>
```

```
Executed:
  5                        <- five cursor/* branches exist
  bd92d8e is reachable from many branches, main lineage included
  third command: no output, exit 0    <- EMPTY
```

**Cause: `--branches=cursor/*` scopes by REACHABILITY, not authorship.** Every `cursor/*` branch has `main` merged in, so all of main's locked-surface history is "reachable from `cursor/*`". `--author=.` matches every commit and filters nothing.

**A30's prescribed replacement, executed as A30 itself demands:**

```bash
git log --oneline --no-merges --branches="cursor/*" --not main -- \
  core/dd_protection.py core/firm_rules.py core/portfolio_mc.py core/mc/ core/lifecycle.py core/dd_geometry.py
```

```
Executed at 0af62ec:  no output, exit 0    <- "Expected: empty" now means something
```

**The boundary actually held.** That is the finding: the gate reported 17 violations of a boundary that was never crossed, and **a gate that fires on ordinary history is dismissed every time it fires.** It rides the **2026-08-08** dual-limb falsifier, which is why A30 prescribes an **Addendum** (never an edit to the frozen §10 body) with this output pasted in.

## R13 — A41 / SP-08: §10 hooks broken by the theme nest — and they fail LOUD. ❌ Open

```bash
rg -n "CAP_LO|np.where\(tier_hi" lab/analysis/tradeify_book_composition_2026-07-23/ ; echo "exit=$?"
ls -d lab/analysis/tradeify_book_composition_2026-07-23 lab/analysis/*/tradeify_book_composition_2026-07-23 2>&1
```

```
Executed at 0af62ec:
  rg: IO error for operation on lab/analysis/tradeify_book_composition_2026-07-23/:
      The system cannot find the file specified. (os error 2)
  exit=2
  ls: cannot access 'lab/analysis/tradeify_book_composition_2026-07-23': No such file or directory
  lab/analysis/c1/tradeify_book_composition_2026-07-23        <- post-nest location
```

**All three SP-08 hooks name the pre-nest path.** They raise an **IO error and exit 2** rather than printing a clean empty PASS — which is the one fail-closed property that keeps this at COSMETIC. Compare **R8(a)**, where the identical "target absent" condition prints `PASS`: same cause, opposite safety.

## R14 — A44 / C32 / RDB-07: `PIPELINES.md` publishes a `make check` that does not exist and a live path that does not. ❌ Open

```bash
rg -c '^validate-params:' Makefile
ls ops/c1_rail_*.py 2>&1
for n in 15 127 155 160; do echo "--- L$n ---"; sed -n "${n}p" PIPELINES.md | cut -c1-150; done
```

```
Executed at 0af62ec:
  exit 1                                   <- there is NO validate-params target
  ls: cannot access 'ops/c1_rail_*.py': No such file or directory   (moved 2026-08-03, 2345095)
  --- L15 ---  | **P5** | Live execution rail (c1) | ... | **BUILT · currently DISARMED** |
               `ops/c1_rail_*.py`, `ops/c1_rail/c1_sizing_host_reference.py`, ...
  --- L127 --- **Active path** (GO 2026-07-17): `TradingView alert → ... → Tradovate` on one
               `Tradeify_Select_100K` eval; 2-leg book at WATCH-1 0.50× via the multiplier layer
  --- L155 --- | **Locked-constant integrity** | `scripts/validate_params.py` + `verify_lock_anchors.py` |
  --- L160 --- | **Build entry points** | `make check` = `validate` (+ `validate-{params,data,pine}`) ...
```

**Four defects, one file, one commit** (C32 groups them): a `make` target that does not exist, a glob that resolves to nothing, a *"Locked-constant integrity"* row naming a deleted script, and an **"Active path"** describing a deployment that was withdrawn 2026-08-04. **L3's own Status claim — that this file is the accurate dynamic view — is false until the body edits land**, which is why C32 requires them in one commit.

## R15 — A46 / C33 / C37: the CI "backstop" claim and the pre-commit header both understate by design. ❌ Open

```bash
sed -n '9,10p' .github/workflows/skills-check.yml
rg -l 'check_root_doc_liveness|roll_sessions|check_closure_disposition' .github/workflows/ ; echo "exit=$?"
rg -n 'check_root_doc_liveness|roll_sessions|check_closure_disposition' scripts/githooks/pre-commit
rg -o '^#   [0-9]+\.' scripts/githooks/pre-commit
rg -c '^python scripts/' scripts/githooks/pre-commit
```

```
Executed at 0af62ec:
  L9-10  "# Gate scripts once in CI as the pre-commit backstop; test execution lives in
          #  tests.yml — operator ruling 2026-07-24 (Algorithm review #5)."
  no output, exit 1        <- those three gates appear in ZERO workflow files
  L50  python scripts/check_root_doc_liveness.py || exit 1
  L89  python scripts/roll_sessions.py --check-order || exit 1
  L111 python scripts/check_closure_disposition.py || exit 1
  #   1.   #   2.   #   4.   #   5.        <- header enumerates FOUR, and NUMBER 3 IS MISSING
  14                                       <- fourteen gate invocations actually run
```

**Two claims, both understating, in opposite directions.** The workflow calls itself *"the pre-commit backstop"* while **three** pre-commit gates have no CI mirror at all. The pre-commit header enumerates **four** checks — numbered 1, 2, **4**, 5, with the hole left by the retired `validate_params` gate — while the file runs **14** invocations across 13 distinct scripts. **C37's DELETE verdict is right**: a hand-maintained header on a file that gains gates monthly is the same class as C6's `Last updated:` field.

## R16 — A45 / C36 / C12(c): path literals broken by the 2026-08-03 theme nest, in selectors nothing checks. ❌ Open

```bash
sed -n '22p' .gitattributes ; ls -d lab/analysis/aegis_6j_prop_reconstruction_2026-07 lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07 2>&1
sed -n '171p' .gitignore    ; ls -d lab/analysis/us500_discovery_2026-06-22 lab/analysis/legacy/us500_discovery_2026-06-22 2>&1
sed -n '294p' core/firm_rules.py ; ls -d lab/analysis/c1_cadence_inactivity_2026-08-02 lab/analysis/c1/c1_cadence_inactivity_2026-08-02 2>&1
python scripts/check_path_liveness.py
```

```
Executed at 0af62ec:
  .gitattributes:22   lab/analysis/aegis_6j_prop_reconstruction_2026-07/*.csv text eol=lf
      -> No such file or directory   |   real: lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07
  .gitignore:171      lab/analysis/us500_discovery_2026-06-22/us500_15m.pkl
      -> No such file or directory   |   real: lab/analysis/legacy/us500_discovery_2026-06-22
  core/firm_rules.py:294   #   c1_cadence_inactivity_2026-08-02, this file's own correction study) had
      -> No such file or directory   |   real: lab/analysis/c1/c1_cadence_inactivity_2026-08-02
  check_path_liveness: OK - all declared committed paths resolve.
```

**Three dead path literals, three different failure modes, and the gate is green** because `check_path_liveness` only resolves MANIFEST parent directories. The `.gitattributes` break silently stops LF normalization on a hash-gated tree; the `.gitignore` break silently makes a **vendor-derived pickle committable** — *"Never committed"*, says the comment above the dead line. **This is FU-19's case measured**: widen the checker to path literals inside `core/**/*.py`, `ops/**/*.py`, `.gitignore` and `.gitattributes`, or accept that one directory move breaks selectors nothing will notice.

## R17 — C44 / C34: two build-surface pointers whose referents were deleted. ❌ Open

```bash
rg -n 'dd_protection.py' .claude/settings.json ; ls dd_protection.py 2>&1
sed -n '8p;17p' pyproject.toml ; ls -d lab/codification 2>&1
```

```
Executed at 0af62ec:
  .claude/settings.json:7   "Bash(python dd_protection.py:*)",
  ls: cannot access 'dd_protection.py': No such file or directory   (it is core/dd_protection.py)
  pyproject L8   description = "First Passage prop trading operational pipeline (multipliers,
                  DD protection, Monte Carlo validation)."
  pyproject L17  "pyyaml",  # codification concept_schema YAML loading
  ls: cannot access 'lab/codification': No such file or directory   (deleted 2026-08-02)
```

The settings permission grants a repo-root invocation that has not existed since the 2026-06-05 monorepo split. The `pyyaml` justification names the module deleted with the codification bridge — **C34 keeps the dependency and corrects the comment**; removing a dependency on the strength of a stale comment is the move to avoid. `description` still advertises the retired multiplier spine.

## R18 — A47 / A48 / A49: the `lab/analysis` RESULTS corpus. ❌ Open

```bash
sed -n '144,146p' lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor.md
ls lab/analysis/orb_mnq_2026-07/run_decay_monitor.py lab/analysis/orb/orb_mnq_2026-07/run_decay_monitor.py 2>&1
sed -n '1,8p' lab/analysis/legacy/futures_conversion_2026-07-01/RESULTS_phaseA.md
sed -n '13p' lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md | cut -c1-120
sed -n '29p' lab/CATALOG.md | cut -c1-120
```

```
Executed at 0af62ec:
  A47  [the file's own Reproduce fence, L144-146]
       PYTHONPATH=lab .venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_decay_monitor.py
       -> ls: cannot access 'lab/analysis/orb_mnq_2026-07/run_decay_monitor.py'
          real: lab/analysis/orb/orb_mnq_2026-07/run_decay_monitor.py
  A49  **Theme:** legacy
       **Status:** ACTIVE — Phase A provisional MNQ/MYM granularity floors
       **PROVISIONAL:** the floors below are provisional until the ATR length (11), SL
       multiple (1.20×), and risk% ... re-verified against the dropped Pine source at Phase B
       Task B0. Treat as a LOCK.md mirror, not an authoritative recompute.
  A48  RESULTS L13:  "**Status:** ACTIVE — the cadence axis F3 required is measured, and
                      **F3 is not decidable on it.** ..."
       CATALOG:29:   | f3_cadence_successor_venues_2026-08-05 | c1 | ACTIVE | ... |
```

**The A48 pair is the one to read carefully.** RESULTS and CATALOG agree — both say `ACTIVE` — and that is the finding: a study whose own headline is *"F3 is not decidable on it"* is indexed identically to a study still in progress, three days before **F3** is due. The `ACTIVE` token carries no verdict.

**The class behind A47, measured — and it is a triage surface, not a finding count:**

```bash
python - <<'PY'
import re, pathlib
bad = set()
for p in pathlib.Path('lab/analysis').rglob('*.md'):
    t = p.read_text(encoding='utf-8', errors='replace')
    for m in re.finditer(r'lab/analysis/([A-Za-z0-9_.\-]+)/', t):
        if not (pathlib.Path('lab/analysis')/m.group(1)).exists():
            bad.add((str(p), m.group(1)))
print('dead lab/analysis/<slug>/ literals inside lab/analysis/**/*.md :', len(bad))
PY
```

```
Executed at 0af62ec:  55
```

⚠ **Do not read 55 as 55 findings.** Most sit inside **dated bodies that were correct when written** — Trap #12 — and must not be edited in place. The actionable subset is narrow: **Reproduce fences and other forward instructions**, which A47 is. Recorded as a number for the next sweep to diff against, exactly as **H25** is.

## R19 — S-20: the reconcile skill's mission framing names a retired feed and a live rail. ❌ Open

```bash
sed -n '10p' .claude/skills/trade-csv-reconcile/SKILL.md | cut -c1-300
ls -d core/data/tv_exports/pepperstone 2>&1
```

```
Executed at 0af62ec:
  L10  "**Mission framing (2026-08-02):** live execution is the **c1 Tradeify/Tradovate rail**
        (disarmed by default); active research is prop-portfolio + ORB-MNQ on CME micros.
        Pepperstone TV exports remain the locked-book historical panel. ..."
  ls: cannot access 'core/data/tv_exports/pepperstone': No such file or directory
```

Dated **2026-08-02** — two days before the de-scope and the same day the Pepperstone feed retired. **A dated framing line is not a dated body**: it is a live orientation statement carrying its authorship date, which is why S-20 is a finding and the `RESULTS` bodies in R18 mostly are not. Round 1 reached this file only as an untested §5.10 candidate (**H14**).

## R20 — SP-20 / A34: an `Accepted`-in-practice spec still labelled `Proposed`, with a checklist that cannot be completed. ❌ Open

```bash
sed -n '3p' docs/spec/c1_nt8_sizing_host_impl.md | cut -c1-220
```

```
Executed at 0af62ec:
  **Status:** `Proposed` — **Option C ADOPTED 2026-07-18** (operator decision, both §2.4
  unknowns resolved favorably; supersede-in-part of the original NT8/NinjaScript execution
  path — the algorith...
```

The Status word says `Proposed`; the same line says the decision was **adopted**, and the host it specifies has been deployed and dry-fired since 2026-07-20. Its *"Remaining before `Accepted`"* checklist now contains items that require a deployment that was withdrawn. **This is the file B3 corrected at §2.2** — the header was left alone deliberately, because a Status flip is a governance act and not a spec repair.

## R21 ⚠ REPAIRED — FU-17: the script-estate wiring census, as a FLOOR. ❌ Open

```bash
ls scripts/*.py | wc -l
python - <<'PY'
import pathlib
scripts = sorted(p.stem for p in pathlib.Path('scripts').glob('*.py'))
wired = ''
for f in ['Makefile', 'scripts/githooks/pre-commit']: wired += pathlib.Path(f).read_text(encoding='utf-8')
for f in pathlib.Path('.github/workflows').glob('*.yml'): wired += f.read_text(encoding='utf-8')
for f in pathlib.Path('.claude').glob('settings*.json'): wired += f.read_text(encoding='utf-8')
un = [s for s in scripts if s not in wired]
print('scripts/*.py                       :', len(scripts))
print('named in Makefile/pre-commit/CI/settings:', len(scripts) - len(un))
print('named NOWHERE in those             :', len(un))
for s in un: print('   ', s)
PY
```

```
Executed at 0af62ec:
  scripts/*.py                            : 37
  named in Makefile/pre-commit/CI/settings: 21
  named NOWHERE in those                  : 16
    archive_strategy · check_advisor_dedup · check_brief · check_push_collision ·
    cost_geometry_pregate · import_skill_from_cache · layer_bootstrap · m1_item5_capture ·
    mc_user_guardian · parse_bar_export · pine_check · pine_lint · repo_hygiene ·
    retire_adr · sync_pine_to_worktree · validate_c1_monitoring_acceptance
```

⚠ **This returns 16, and [`01-diagnostics.md`](01-diagnostics.md) §3.2 / FU-17 say 22. Neither is wrong.** 22 = **unwired ∪ mis-scoped**, and *mis-scoped* — a script that is wired but reads the wrong tree — **cannot be derived by any pattern**; it is exactly what **R8** and **R16** had to establish by hand, one script at a time. **16 is a mechanically reproducible floor. The gap of 6 is the part that needs eyes**, and that is FU-17's actual deliverable.

**Do not read the 16 as 16 defects, either.** Several are legitimately operator-run tools (`pine_check`, `repo_hygiene`, `retire_adr`). The census is the *input* to the wire-or-retire ruling, not the ruling.

---

# §C — Structural hooks

## X1 — re-derive the combined finding counts from the section set

**Why this exists.** The split moved the counts out of one document into eight. The old failure mode was a stale number; the new one is **eight numbers that do not add up and no place where that is visible.** This hook re-derives what is derivable and states precisely what is not — the same discipline as **H15**, which it succeeds for the section set.

```bash
cd docs/notes/audits/programme-audit/2026-08-05-claim-alignment
python - <<'PY'
import re, pathlib, collections
ID  = re.compile(r'^\|\s*\*{0,2}(A\d+|C\d+|M\d+|B[123]|O-[A-J]|U[12]|G\d+|R-B\d\w?|FU-\d+'
                 r'|LAB-\d+|SP-\d+|S-\d+|CAC-\d+|RDB-\d+|DR-\d+|SE-\d+)\b')
TOK = re.compile(r'(KEEP-CORRECTED|KEEP-AS-IS|SIMPLIFY|DELETE)(?:\s*(?:×|x)\s*(\d+))?')
tot = collections.Counter()
for f in sorted(pathlib.Path('.').glob('0*.md')):
    rows, per = 0, collections.Counter()
    for ln in f.read_text(encoding='utf-8').splitlines():
        if not ln.startswith('|'): continue
        m = ID.match(ln)
        if not m: continue
        rows += 1
        c = ln.split('|')
        if len(c) >= 6:
            for t, n in TOK.findall(c[4]): per[t] += int(n) if n else 1
    tot.update(per)
    print(f'{f.name:26s} id-rows={rows:3d}  verdicts={dict(per)}')
print('TOTAL verdict tokens:', dict(tot), '=', sum(tot.values()))
PY
```

```
Executed at 0af62ec, then RE-EXECUTED after this file landed — output identical, and
08-hooks.md contributes 0 rows / 0 verdict tokens (it carries no finding rows by design):
  01-diagnostics.md          id-rows=  1  verdicts={}
  02-blockers.md             id-rows= 11  verdicts={}
  03-agent-facing.md         id-rows= 49  verdicts={'KEEP-CORRECTED': 34, 'SIMPLIFY': 25,
                                                    'DELETE': 16, 'KEEP-AS-IS': 1}
  04-misleading.md           id-rows= 49  verdicts={'KEEP-CORRECTED': 25, 'SIMPLIFY': 14, 'DELETE': 13}
  05-cosmetic.md             id-rows= 46  verdicts={'KEEP-CORRECTED': 23, 'SIMPLIFY': 23, 'DELETE': 20}
  06-operator-judgement.md   id-rows= 31  verdicts={}
  07-followups.md            id-rows= 42  verdicts={}
  08-hooks.md                id-rows=  0  verdicts={}
  TOTAL verdict tokens: {'KEEP-CORRECTED': 82, 'SIMPLIFY': 62, 'DELETE': 49, 'KEEP-AS-IS': 1} = 194
```

**And the round-2 concentration claim, re-derived independently:**

```bash
python - <<'PY'
import re, pathlib, collections
t = pathlib.Path('03-agent-facing.md').read_text(encoding='utf-8')
dom, ids = collections.Counter(), collections.Counter()
for rid, cell in re.findall(r'^\|\s*\*\*(A\d+)\*\*\s*\|\s*(.+?)\|', t, re.M):
    p = (re.search(r'`([^`]+)`', cell) or [None,'?'])[1]
    d = ('deploy' if p.startswith('deploy/') else '.claude' if p.startswith('.claude')
         else '.cursor' if p.startswith('.cursor') else 'scripts' if p.startswith('scripts/')
         else 'docs' if p.startswith('docs/') else 'lab' if p.startswith('lab/') else 'root/build')
    dom[d] += 1
    ids[d] += len(set(re.findall(r'\b(DR-\d+|S-\d+|CAC-\d+|SE-\d+|SP-\d+|LAB-\d+|RDB-\d+)\b', cell)))
print('rows per domain      :', dict(dom), '=', sum(dom.values()))
print('finding-ids per domain:', dict(ids), '=', sum(ids.values()))
PY
```

```
Executed at 0af62ec:
  rows per domain      : {deploy:2, .claude:13, .cursor:4, scripts:10, docs:13, lab:4, root/build:3} = 49
  finding-ids per domain: {deploy:8, .claude:23, .cursor:4, scripts:16, docs:18, lab:4, root/build:3} = 76
```

**What this reproduces — and it is more than H15 managed.**

- **`03`'s declared Algorithm split reproduces byte-exactly:** *"34 KEEP-CORRECTED · 25 SIMPLIFY · 16 DELETE · 1 KEEP-AS-IS"*.
- **`03`'s declared record count reproduces exactly: 76.**
- **`03`'s declared row count reproduces exactly: 49.**
- **The agent-facing concentration reproduces on four of five domains exactly** — `.claude` **23**, `scripts` **16**, `deploy` **8**, `.cursor` **4**.
- **`docs` returns 18 against a declared 19, and the one-unit gap is fully explained**, not waved at: row **A43** spans two files (`lab/analysis/c1/README.md` **and** `docs/superpowers/specs/2026-08-03-…-design.md`) and this classifier attributes a row to its **first** backticked path. Re-attributing A43's `docs/` limb gives **docs 19 / lab 3**, which reconciles to the declared split exactly.

**What it does NOT reproduce, stated rather than smoothed.**

- **It cannot reach 316 / 53 / 250.** Those are *raised* / *refuted* / *confirmed* counts. **Refuted findings have no row** — that is what refuted means — so the section set contains no trace of the 53, by construction. The combined headline is a property of the adjudication passes, not of this corpus, and it lives in `README.md` with its provenance.
- **194 verdict tokens is a floor, not a finding count.** Rows group by target file and many carry several findings under one token (`A1` = seven findings, `C12` = three). The `×N` notation is parsed; **prose multiplicities are not.**
- **`03`'s 71 findings vs 76 records is a real and declared gap**, not an error: five findings carry more than one adjudication record. The hook counts records because records are what the table encodes.
- **`01`, `02`, `06` and `07` return zero verdict tokens by design** — diagnostics, fixed BLOCKERs, unadjudicated items and follow-ups carry no Algorithm verdict. **A zero there is correct; a non-zero would be the anomaly.**

**Anyone quoting a distribution must say which one they are quoting**: §2's hand tally with ±2, H15's round-1 floor of 92, or X1's section-set floor of 194.

## X2 — the section set is complete and its internal links resolve

**Why this exists, in one sentence: a split document's new failure mode is a section going missing, and nothing in the repo's gate estate looks here.** `check_root_doc_liveness` resolves root-doc links only (**H7**); `check_path_liveness` resolves MANIFEST parents only (**R16**); gate 13 globs one level of `lab/analysis` (**H4**). **This directory is gated by nothing.**

```bash
cd docs/notes/audits/programme-audit/2026-08-05-claim-alignment
python - <<'PY'
import re, pathlib
here = pathlib.Path('.')
expect = ['README.md','01-diagnostics.md','02-blockers.md','03-agent-facing.md',
          '04-misleading.md','05-cosmetic.md','06-operator-judgement.md',
          '07-followups.md','08-hooks.md']
present = sorted(p.name for p in here.glob('*.md'))
print('present :', present)
print('MISSING :', [e for e in expect if not (here/e).exists()])
print('EXTRA   :', [p for p in present if p not in expect])
dead = set()
for p in sorted(here.glob('*.md')):
    txt = p.read_text(encoding='utf-8')
    for m in re.finditer(r'\]\(([^)#][^)]*?)(?:#[^)]*)?\)', txt):        # markdown links
        t = m.group(1).strip()
        if t.startswith(('http','mailto')): continue
        if not (p.parent / t).exists(): dead.add((p.name, t))
    for m in re.finditer(r'`(\d{2}-[a-z-]+\.md)`', txt):                 # backticked section refs
        if not (here / m.group(1)).exists(): dead.add((p.name, m.group(1)+'  [SECTION REF]'))
print('dead relative references:', len(dead))
for d in sorted(dead): print('   ', d)
PY
```

```
Run 1 — executed at 0af62ec BEFORE this file was written, over 01-07:
  present : ['01-diagnostics.md','02-blockers.md','03-agent-facing.md','04-misleading.md',
             '05-cosmetic.md','06-operator-judgement.md','07-followups.md']
  MISSING : ['README.md', '08-hooks.md']
  EXTRA   : []
  dead relative references: 37

Run 2 — re-executed immediately after this file was written, over 01-08:
  present : [... all eight 0N-*.md ...]
  MISSING : ['README.md']
  EXTRA   : []
  dead relative references: 38
  delta   : [('08-hooks.md', '09-unadjudicated.md', 'sectionref')]     <- see the ⚠ below
```

⚠ **Record the number the published command actually returns, not the one a draft returned.** An earlier form of this hook accumulated into a **list** rather than a set and reported **48** — duplicate `(file, target)` pairs counted repeatedly. The command as published above de-duplicates and returns **37 / 38**. This is the trap in miniature and it was caught only by re-running the hook against the finished artifact.

**Three findings, and the third is the one that would have gone unnoticed.**

1. **`README.md` was absent at both runs**, and **all seven of the round-1-ported section files link to it** (`01` … `07`) — 7 of the 37. It is authored in the same pass as this file; **re-run X2 after the set lands** and expect `MISSING: []`.

2. **30 dead relative references that are not the README, and the shape is systematic.** Measured breakdown of the 37: **17 `../` depth errors · 12 repo-root-relative · 7 README · 1 dangling section file.** The split moved every section one directory deeper than the round-1 artifact, and cross-references were carried over at the old depth or written as if from the repo root. Representative, from the executed output:

```
   ('03-agent-facing.md', '../../adr/2026-08-04-tradeify-venue-descope-eval-included.md')
   ('03-agent-facing.md', '../adr/2026-08-04-tradeify-venue-descope-eval-included.md')
   ('04-misleading.md',   'docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md')
   ('04-misleading.md',   'CLAUDE.md')            <- repo-root-relative, written as if from root
   ('05-cosmetic.md',     '../../../adr/2026-08-05-strategy-venue-binding-axis.md')
   ('06-operator-judgement.md', '../../ops/accounts.py')
```

**The same ADR is linked at three different depths inside this set, and none of the three resolves.** **Verified**: the correct form from `docs/notes/audits/programme-audit/2026-08-05-claim-alignment/` is `../../../../adr/…` — four `..` reach `docs/`, and `01-diagnostics.md:28` already uses exactly that and resolves. Fix them mechanically from this hook's output; do not hand-verify 30 links.

3. **⚠ One dangling *section-file* reference, and it is the exact failure this hook was built for.** `05-cosmetic.md` cites **`09-unadjudicated.md`** — a section file that **does not exist**. The two unadjudicated items (**U1**, **U2**) live in [`06-operator-judgement.md`](06-operator-judgement.md) §3. **A reader following that pointer concludes two findings were lost in the split.** They were not; the pointer is wrong. **FIXED when** the backticked-ref limb returns exactly one hit — this file's, below.

   ⚠ **This file is the second hit, and it is a self-match, not a defect.** Run 2's `delta` is `08-hooks.md → 09-unadjudicated.md`: the hook flags this section *because it quotes the dangling name in order to report it*. Round 1 hit the identical shape at **H15**, where the naive `KEEP-AS-IS` pattern matched its own printed command line. **A grep run over the document that contains it is self-referential.** Do not "fix" this file; after `05-cosmetic.md` is repaired the correct expected output is **one** section-ref hit, here.

**Standing use.** Run X2 **before** publishing any revision of this set and **after** any file is added, renamed or removed. It is cheap, it is the only check that reaches this directory, and its whole value is that it catches the class of error a human re-reading their own document cannot see.

---

# §D — Deliberately discarded hooks

**Three checks were designed, judged unfixable, and are recorded rather than shipped.** Round 1 shipped one such discard; this pass ships three. Each names an authority that **lives outside the tree**, and that is the pattern worth carrying forward: this repo's most consequential facts — a venue's trade clock, a deployed image's bytes, a scanner's own output — are the ones its gates structurally cannot reach.

## D1 — that the eval's weekly activity window is covered (FU-1 / O-C / M36) — **CARRIED FORWARD FROM ROUND 1, UNCHANGED**

**It cannot be made to bind.** The venue's trade clock is not in the tree. `docs/notes/rail_build/RUNBOOK.md`'s arming log records fills inside narrative prose, and the whole log yields exactly one grep-visible fill line:

```bash
rg -c 'Filled BUY|Filled SELL' docs/notes/rail_build/RUNBOOK.md
```

```
Executed at 0af62ec:  1        (the 2026-07-27 entry, unchanged since e031225)
```

**No pattern establishes week-coverage from one narrative line.** The most calendar-critical item in this audit has no runnable in-repo hook, and inventing one would have been worse than saying so.

⚠ **FU-1's ruling does not change this, and the distinction is worth stating precisely.** The ruling *is* recorded, and that much is checkable:

```bash
rg -c 'RULED 2026-08-05|token trade' docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md STATE.md
```

```
Executed at 0af62ec:
  docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md:8
  STATE.md:2
```

**But that hooks the DECISION, not the ACT.** An operator-placed token trade at the venue leaves **no in-tree trace** — the rail does not move, no fill flows through `ops/c1_rail/`, no telemetry event is written. **Whether the window was actually covered remains unverifiable from this repo**, exactly as it was before the ruling. Verification is an operator observation at the venue.

## D2 — the sentinel's field-form reach at HEAD (B2 residue **R-B2a**) — **NEW**

The natural companion to **H2** is `PYTHONPATH=ops python -m sentinel --asof 2026-08-08`, which measures the field-form class the way the corrected `STATE.md` prescribes. **It is not run here, and the reason is a side effect, not a scruple:** that command **writes** a run block to `docs/notes/sentinel/queue.md`. Re-running it to refresh a count inside an audit note plants a **future-dated sentinel run** in the record, days before the gate it feeds.

**This is not hypothetical. The worktree already carried one.** A 60-line uncommitted `## Run 2026-08-08` block was present at the start of this pass, left by an earlier measuring run, containing seven queued items including `PRECOND-board-sync-2026-08-08`. It was reverted:

```bash
git status --short docs/notes/sentinel/queue.md   # was:  M docs/notes/sentinel/queue.md
git checkout -- docs/notes/sentinel/queue.md
git status --short                                # now:  ?? <this section directory> only
```

**The field-form figure at HEAD is therefore stated as DERIVED, never measured** — [`02-blockers.md`](02-blockers.md) B2.2 does exactly this (55 ADR mentions − 18 prose-only residue = 37) and labels it. **Re-measure at the 08-08 gate, where the write is the point.** Only the `--help` invocation is safe to run for verification, and **H2**'s companion in `02` does exactly that.

## D3 — that the deployed pin matches the deployed image (A1(e) / H22 / M20) — **NEW**

`M1_MONITORING_ACCEPTANCE.json`'s `fixture_hashes` describes the **deployed Fly build**, and every consumer of it says so in the imperative: *"A redeploy MUST refresh the pin in the same motion, from hashes read **in-container** — never from these tree bytes."* **There is no in-repo way to check that the pin matches the image**, because the authoritative bytes are inside a container this repo cannot read. The two flags that exist measure the wrong thing on purpose:

```bash
python scripts/validate_c1_monitoring_acceptance.py \
  docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --require-tree-current ; echo "exit=$?"
```

```
Executed at 0af62ec (tail):
  This is drift, not corruption: fixture_hashes describes the DEPLOYED build and stays
  authoritative until a real deploy.
  A redeploy MUST refresh the pin in the same motion, from hashes read in-container.
  exit=1
```

**`--require-tree-current` exits 1 unconditionally in this state — it blocks, it never permits**, which is the correct fail-closed shape and is precisely why it is not a verification of the pin. A hook asserting pin-freshness would have to compare tree bytes to a deployed image, and comparing tree bytes is the exact act every consumer forbids. **Recorded as unhookable rather than approximated**, and it is the standing reason A1(e) states the refresh as a **deploy pre-condition** rather than as a check.

---

**Section ends.** Every hook above was executed at `0af62ec` and its recorded output is what it printed. **Six hooks were repaired** (H9, H25, R6, R8, R12, R21) and **three discarded** (D1, D2, D3); none was shipped aspirationally. Findings remain **recommendations pending operator ruling** except the four marked FIXED/RULED in [`02-blockers.md`](02-blockers.md) and [`07-followups.md`](07-followups.md). No edit was applied by this file; the only tree change made during its authoring was reverting the spurious `docs/notes/sentinel/queue.md` write recorded under **D2**.
