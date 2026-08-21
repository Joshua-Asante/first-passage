# CC Handoff — CFO subscription-ledger consolidation (mechanical build)

**Date:** 2026-08-21
**Parent session:** Claude Code (this session, orchestrating per the `cursor-fleet` skill)
**Spawn target:** Cursor (frozen-spec implementation — per `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`; §0.5 Cursor variant applies)
**Repo:** `first-passage`
**Brief type:** CC handoff (multi-step)
**Parent question:** `N/A` — executing `docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md` D1 + D2 (the ADR that ratifies this build; author it before dispatch, it names this brief in its §7)
**Authority:** Joshua (CEO), in-session direct instruction ("implement 1-4, reconfirm ledger once a month"). Claude Code authored this brief; Cursor executes. No commit/merge without Joshua's or CC's go (CC reviews the returned PR under receiving-code-review discipline before recommending merge).

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 work)

Cursor: read each file below and report contents (or the specific stated range) in your first response. Do not propose changes, do not write code, until this Phase 0 read-report has been delivered.

- `docs/pursuits/d11-tradingview-subscription.md` — report: full contents
- `docs/pursuits/d12-databento-subscription.md` — report: full contents
- `docs/pursuits/d13-flyio-subscription.md` — report: full contents
- `docs/pursuits/d14-crosstrade-subscription.md` — report: full contents
- `docs/pursuits/d15-tradeify-account.md` — report: full contents
- `docs/pursuits/d16-cursor-subscription.md` — report: full contents
- `docs/pursuits/d17-claude-max-subscription.md` — report: full contents
- `scripts/check_pursuit_records.py` — report: full contents
- `tests/scripts/test_check_pursuit_records.py` — report: full contents
- `git log -1 --oneline -- docs/pursuits/d17-claude-max-subscription.md` — report: commit hash (Phase-0 staleness anchor — expect `412efa1` or later; if the hash differs or the file's Survive-bound text differs from what §2 Step 2.2 quotes as "old text" below, STOP and return `NEEDS_CONTEXT` with the diff — do not proceed on a stale assumption, this exact failure class is why this line exists)

**No-op condition:** if `docs/pursuits/SUBSCRIPTION_LEDGER.md` already exists on `origin/main` at dispatch time, this packet has been overtaken — return `DONE` citing the existing commit, do not re-do the work.

---

## §0.75 — Local-only dependency check (required, Spawn target is Cursor)

- **Gitignored vendor data:** N/A — this packet touches no path under `core/data/tv_exports/**`, `core/data/bar_data/**`, or `core/data/external/**`. All touched files are plain tracked markdown/Python in `docs/pursuits/` and `scripts/`.
- **Secrets/API keys:** N/A — no credential is read or needed by any step below.

---

## §0.5 — Clarifying questions (Cursor variant — recommended defaults)

Do not leave any of these open. Apply the recommended default unless your Phase-0 read contradicts it, in which case bounce `NEEDS_CONTEXT` with the conflict quoted verbatim.

**(A) Where does the ledger file live?** **Recommended default:** `docs/pursuits/SUBSCRIPTION_LEDGER.md` (colocated with the d11–d17 records it summarizes; not under `docs/personas/` even though the CFO conceptually owns it — `docs/pursuits/` is where every other pursuit-adjacent registry artifact in this repo lives).

**(B) Should the ledger's dollar figures be re-derived from anything, or copied verbatim from this brief?** **Recommended default:** copied verbatim from §2 Step 2.1's table below — every figure was already operator-confirmed or explicitly marked unconfirmed in the parent session; this packet's job is mechanical transcription and cross-linking, not re-verification.

**(C) Should the seven pursuit records' Survive-bound edits also carry the exact string `"C-1 CLOSED"` / `"C-1 partially closed"` / `"C-1 still open"` as they do today?** **Recommended default:** yes, preserve the current C-1 disposition wording exactly (per §2 Step 2.2's frozen old/new text) — this build reorganizes *where* the dollar figure lives, it does not re-adjudicate any C-1 disposition.

**(D) What severity tier does the new `check_pursuit_records.py` check use?** **Recommended default:** WARN, report-only, exit 0 — identical severity to every existing limb in that script (see its own module docstring: "Default every limb to WARN / report-only... gate composition is owned by `scripts/gates.yml`... Wiring is an operator decision"). Do not introduce a HARD-tier check.

---

## §1 — Context

**Decision being executed (ADR):** `docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md` D1 (consolidated ledger) + D2 (required ledger-pointer field, mechanically checked) — one-sentence summary: replace seven scattered `$ unverified in-repo (C-1)`-style tags across the d11–d17 pursuit records with one ledger table those records point to, and mechanically flag any future subscription/venue-account-class KEEP record that ships without a pointer to it.

**What CC is being asked to produce:**
- `docs/pursuits/SUBSCRIPTION_LEDGER.md` — new file, exact content in §2 Step 2.1.
- Seven edits to `docs/pursuits/d11-tradingview-subscription.md` through `d17-claude-max-subscription.md` — exact old/new text in §2 Step 2.2.
- An extension to `scripts/check_pursuit_records.py` — exact diff in §2 Step 2.3.
- Corresponding new tests in `tests/scripts/test_check_pursuit_records.py` — exact fixtures/tests in §2 Step 2.4.
- A PR against this repo with all of the above, tests green.

**What CC is NOT being asked to do:**
- Do not touch `docs/adr/`, `STATE.md`, `docs/SESSIONS.md`, `docs/personas/cfo.md`, or `docs/personas/cfo-log.md` — those are reserved to the orchestrating CC session's own integration commit (per the `cursor-fleet` skill; also `STATE.md`/ADRs are locked surfaces under `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §2 test 1, full stop, no exception for this packet).
- Do not re-adjudicate whether Databento's `$200/mo` figure is really flat vs. usage-billed, or chase down Fly.io/Tradeify's still-missing figures. Those are open questions for the operator/CFO, not this build.
- Do not touch any `docs/pursuits/*.md` file outside the seven named above (d11–d17) — in particular, do not "helpfully" apply the ledger-pointer pattern to any other pursuit record.

---

## §2 — Execution plan

### Step 2.1 — Create `docs/pursuits/SUBSCRIPTION_LEDGER.md`

- **Inputs:** none beyond this brief.
- **Action:** create the file with exactly this content:

```markdown
# Subscription / venue-account ledger — CFO-owned

One row per `docs/pursuits/d11-d17` cost-carrying record. Canonical source for every $/mo
figure — the pursuit records themselves link here rather than restating the number (Rule 7,
one canonical owner). Built per
[`docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md`](../adr/2026-08-21-cfo-subscription-ledger-consolidation.md),
closing GSUB-1's concern C-1 (subscription $ figures not discoverable in-repo, open
2026-08-09 → 2026-08-21).

**Reconfirm cadence:** monthly — see `STATE.md` § Scheduled forward triggers, "Monthly —
recurring." Each reconfirm updates the "Last confirmed" column below; a figure that goes
un-reconfirmed for >60 days should be treated as stale, not silently trusted.

| Subscription | Pursuit | $/mo | Billing model | Last confirmed | Status |
|---|---|---|---|---|---|
| TradingView | [d11](d11-tradingview-subscription.md) | $70 | flat | 2026-08-21 | confirmed |
| Databento | [d12](d12-databento-subscription.md) | $200 | **flagged** — record describes usage-billed/per-pull-gated; operator's figure reads flat. Tension open, not reconciled. | 2026-08-21 | confirmed (billing-model question open) |
| Fly.io | [d13](d13-flyio-subscription.md) | — | — | asked 2026-08-21, not supplied | **still open** |
| CrossTrade | [d14](d14-crosstrade-subscription.md) | $50 | flat | 2026-08-21 | confirmed |
| Tradeify | [d15](d15-tradeify-account.md) | — | account-carrying cost, not a subscription fee | asked 2026-08-21, not supplied | **still open** |
| Cursor Ultra | [d16](d16-cursor-subscription.md) | $200 | flat | 2026-08-21 | confirmed |
| Claude Max | [d17](d17-claude-max-subscription.md) | $200 | flat | 2026-08-21 | confirmed |

**Confirmed monthly total:** $720/mo (five confirmed rows; Fly.io and Tradeify excluded from
this sum since their figures are still unverified, not zero — do not read $720 as the true
total).

**Change log**

| Date | Change |
|---|---|
| 2026-08-21 | Ledger created — five figures operator-confirmed, one flagged (Databento billing-model tension), two still open (Fly.io, Tradeify). Closes GSUB-1 C-1. |
```

- **Expected output:** `docs/pursuits/SUBSCRIPTION_LEDGER.md` exists with the exact content above (verbatim — this is a frozen spec, not a draft to improve on).
- **Per-step gate:** file exists, content matches verbatim. Any deviation (reworded prose, reordered columns, added/removed rows) is scope creep — see §5.

### Step 2.2 — Re-point the seven pursuit records at the ledger

For each file below, find the **exact old text** (a single Markdown line, possibly wrapping) and replace with the **exact new text**. If the old text is not found verbatim (whitespace-exact), do not guess — bounce `NEEDS_CONTEXT` quoting what you actually found at that location.

**`docs/pursuits/d11-tradingview-subscription.md`**

Old:
```
**Survive bound:** live consumer confirmed; **Premium plan** (operator-confirmed 2026-08-18,
includes Deep Backtesting), **$70/mo** (operator-confirmed 2026-08-21 — C-1 CLOSED). No
disposition here turns on the dollar figure, only on the live consumer and its entitlements.
```

New:
```
**Survive bound:** live consumer confirmed; **Premium plan** (operator-confirmed 2026-08-18,
includes Deep Backtesting). $/mo tracked in [`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md)
(C-1 CLOSED). No disposition here turns on the dollar figure, only on the live consumer and
its entitlements.
```

**`docs/pursuits/d12-databento-subscription.md`**

Old:
```
**Survive bound:** usage-billed, not a flat subscription — cost dry-run is the per-pull gate.
Operator-supplied figure 2026-08-21: **$200/mo**. Flagged, not silently reconciled (CFO
2026-08-21): this record's own billing-model description is usage-billed/per-pull-gated, and
the operator's figure reads as a flat monthly number — the two are in tension. Two open
readings: (a) $200/mo is a monthly usage estimate or spend cap operating *within* the existing
per-pull-gated model, or (b) the billing model has moved to (or was always) closer to flat and
this record's "usage-billed" framing needs re-confirming. C-1 **partially closed** — a real
number now exists — but the billing-model question stays open pending operator clarification;
do not read $200/mo as validating either reading over the other.
```

New:
```
**Survive bound:** usage-billed, not a flat subscription — cost dry-run is the per-pull gate.
$/mo tracked in [`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md) — flagged there against
this record's own billing-model description (usage-billed vs. the operator's flat $200/mo
figure); see the ledger for the open tension, not restated here. C-1 **partially closed**.
```

**`docs/pursuits/d13-flyio-subscription.md`**

Old:
```
**Survive bound:** $ **unverified in-repo** (C-1 — still open for this row: operator supplied
figures for five of six d11–d16 rows 2026-08-21; Fly.io was asked and not among them); rides
a2's $700 spend ceiling where applicable
```

New:
```
**Survive bound:** $ unverified — tracked as open in
[`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md) (C-1 still open for this row: asked
2026-08-21, not supplied); rides a2's $700 spend ceiling where applicable
```

**`docs/pursuits/d14-crosstrade-subscription.md`**

Old:
```
**Survive bound:** **$50/mo** (operator-confirmed 2026-08-21 — C-1 CLOSED); rides a2
```

New:
```
**Survive bound:** $/mo tracked in [`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md) (C-1
CLOSED); rides a2
```

**`docs/pursuits/d15-tradeify-account.md`**

Old:
```
**Survive bound:** account-carrying cost **unverified in-repo** (C-1 — still open for this row:
operator supplied figures for five of six d11–d16 rows 2026-08-21; Tradeify was asked and not
among them); the binding weekly cost is the operator's token-trade decision, not a dollar figure
```

New:
```
**Survive bound:** account-carrying cost unverified — tracked as open in
[`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md) (C-1 still open for this row: asked
2026-08-21, not supplied); the binding weekly cost is the operator's token-trade decision, not
a dollar figure
```

**`docs/pursuits/d16-cursor-subscription.md`**

Old:
```
**Survive bound:** **Cursor Ultra**, **$200/mo** (operator-confirmed 2026-08-21 — C-1 CLOSED)
```

New:
```
**Survive bound:** **Cursor Ultra**; $/mo tracked in
[`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md) (C-1 CLOSED)
```

**`docs/pursuits/d17-claude-max-subscription.md`**

Old:
```
**Survive bound:** **$200/mo** (operator-confirmed 2026-08-21)
```

New:
```
**Survive bound:** $/mo tracked in [`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md)
```

- **Expected output:** all seven files edited exactly as specified, nothing else in any of them touched.
- **Per-step gate:** `git diff --stat` on these seven files shows only the Survive-bound line changed in each (a one-paragraph diff per file); no other line differs.

### Step 2.3 — Extend `scripts/check_pursuit_records.py`

Add a new mechanical limb, `ledger-pointer`, following the exact pattern of the existing limbs in that file (WARN-tier, report-only). Frozen diff:

1. Add near the top, alongside the existing `RE_ENTRY_FIELD` / `EXPIRY_FIELD` compiled patterns:

```python
CLASS_LEDGER_TRACKED = re.compile(
    r"(?m)^\*\*Class:\*\*.*\(d\)\s*meta-belt\s*\((subscription|venue account)",
    re.IGNORECASE,
)
LEDGER_POINTER = re.compile(r"SUBSCRIPTION_LEDGER\.md")
```

Verified against the live corpus at authoring time (CC, this session): `CLASS_LEDGER_TRACKED` matches exactly `d11` through `d17` (7 files) and no others — do not widen or narrow this pattern without re-checking against the full `docs/pursuits/*.md` corpus first.

2. Inside `scan_file`, immediately after the existing `if standing == "KEEP":` block's `KEEP_FIELDS` loop (i.e., as a sibling check under the same `if standing == "KEEP":` condition, not a new top-level `if`), add:

```python
        if CLASS_LEDGER_TRACKED.search(text) and not LEDGER_POINTER.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "ledger-pointer",
                    path,
                    "subscription/venue-account-class KEEP missing a SUBSCRIPTION_LEDGER.md "
                    "pointer (CFO 2026-08-21 recommendation — $/mo tracked at row-creation "
                    "time, not backfilled later; see docs/adr/2026-08-21-"
                    "cfo-subscription-ledger-consolidation.md D2)",
                )
            )
```

3. Update the module's top-of-file docstring "THE MECHANICAL RULE" list to add a 5th limb, matching the existing numbered-list style:

```
  5. ledger-pointer — every KEEP whose Class is (d) meta-belt (subscription) or
     (d) meta-belt (venue account) must reference SUBSCRIPTION_LEDGER.md
     somewhere in its body (§2.5-adjacent; added 2026-08-21 per the CFO's
     C-1-closure recommendation, docs/adr/2026-08-21-cfo-subscription-
     ledger-consolidation.md D2).
```

- **Expected output:** `scripts/check_pursuit_records.py` diff matches the above exactly — three localized additions, nothing else in the file touched (no reformatting, no unrelated cleanup).
- **Per-step gate:** `python scripts/check_pursuit_records.py` still exits 0 on the live corpus (all seven d11–d17 records now carry the ledger pointer from Step 2.2, so the new limb fires zero findings against the live tree); running it against a synthetic fixture missing the pointer produces exactly one `ledger-pointer` WARN.

### Step 2.4 — Extend `tests/scripts/test_check_pursuit_records.py`

Add fixtures and tests following the file's own existing style exactly (see the `COMPLIANT_KEEP` / `KEEP_MISSING_MEASURE` pattern already in the file — Phase-0 read-report should have surfaced this).

Add these three fixtures (place near the other `KEEP_*` fixtures):

```python
COMPLIANT_SUBSCRIPTION_KEEP = """# Fixture — subscription KEEP with ledger pointer

**Class:** (d) meta-belt (subscription) · **Standing:** KEEP
**Aim served:** A2
**Measure:** live consumer confirmed
**Survive bound:** $/mo tracked in [`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md)
**Review date:** none fixed
"""

SUBSCRIPTION_KEEP_MISSING_LEDGER = """# Fixture — subscription KEEP missing ledger pointer

**Class:** (d) meta-belt (subscription) · **Standing:** KEEP
**Aim served:** A2
**Measure:** live consumer confirmed
**Survive bound:** $ unverified in-repo
**Review date:** none fixed
"""

NON_SUBSCRIPTION_KEEP_NO_LEDGER_NEEDED = """# Fixture — non-subscription KEEP, ledger check does not apply

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A1
**Measure:** progress metric
**Survive bound:** operator gate-walk cadence
**Review date:** 2026-11-08
"""
```

Add these tests (place near the other KEEP-related tests):

```python
def test_subscription_keep_with_ledger_pointer_passes(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "sub-keep-ok.md", COMPLIANT_SUBSCRIPTION_KEEP), asof=ASOF_BEFORE
    )
    assert not any(f.limb == "ledger-pointer" for f in findings), findings


def test_subscription_keep_missing_ledger_pointer_fails(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "sub-keep-bad.md", SUBSCRIPTION_KEEP_MISSING_LEDGER), asof=ASOF_BEFORE
    )
    assert any(f.limb == "ledger-pointer" for f in findings), findings


def test_non_subscription_keep_not_ledger_flagged(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "non-sub-keep.md", NON_SUBSCRIPTION_KEEP_NO_LEDGER_NEEDED), asof=ASOF_BEFORE
    )
    assert not any(f.limb == "ledger-pointer" for f in findings), findings


def test_live_subscription_keeps_have_ledger_pointer():
    subs = sorted(cpr.PURSUITS_DIR.glob("d1[1-7]-*.md"))
    assert len(subs) == 7, f"expected 7 subscription/venue-account pursuit records (d11-d17), got {len(subs)}"
    for p in subs:
        text = p.read_text(encoding="utf-8")
        assert cpr.LEDGER_POINTER.search(text), f"{p.name} missing SUBSCRIPTION_LEDGER.md pointer"
```

Note: `test_live_corpus_clean_at_gsub1_asof` (existing test, asof 2026-08-09) must still pass unmodified after Step 2.2/2.3 — the new `ledger-pointer` limb is not date-gated, so it evaluates current file content regardless of `asof`, and all seven records will carry the pointer after Step 2.2. Do not edit that existing test.

- **Expected output:** `pytest tests/scripts/test_check_pursuit_records.py -v` — all tests pass, including the four new ones and every pre-existing one unmodified.
- **Per-step gate:** full green run, no skips, no modified pre-existing test bodies (only additions).

### Step 2.5 — Closure

Open a PR titled `docs(cfo): consolidate subscription ledger (d11-d17), extend ledger-pointer gate` against `main`, containing exactly the 9 files touched above (1 new ledger + 7 pursuit-record edits + 1 checker script) plus the test file. Nothing else.

---

## §4 — Falsifiable hypothesis

`N/A` — executing an ADR (`docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md`), not a
Pre-Q investigation; no hypothesis is under test in this mechanical build. The parent ADR's own
§4 Revert trigger (a false hidden number appearing in the ledger, or the ledger-pointer check
producing noise on unrelated pursuit classes) governs whether the *design* should be reverted —
this packet only executes it.

---

## §5 — Forbidden moves

- **Scope creep — the "while I was in there" refactor.** If you notice the ledger table's markdown could be prettier, or `check_pursuit_records.py` has an unrelated inefficiency, log it in your closure report under `Concerns surfaced`, do not fix it here.
- **Touching any file outside the 9 named** (`SUBSCRIPTION_LEDGER.md`, d11–d17, `check_pursuit_records.py`, its test file). In particular: no edits to `STATE.md`, `docs/SESSIONS.md`, `docs/adr/*`, or `docs/personas/*` — those are the orchestrating session's reserved surfaces.
- **Re-adjudicating any C-1 disposition** (Databento's billing-model tension, Fly.io/Tradeify's missing figures). Transcribe the frozen text exactly; do not resolve the open questions yourself.
- **Widening or narrowing `CLASS_LEDGER_TRACKED`** beyond what §2 Step 2.3 specifies without re-verifying against the live `docs/pursuits/*.md` corpus first — the pattern was regex-tested against the actual repo state before this brief was frozen; a plausible-looking variant can silently change which files the check covers.
- **Amending the new `ledger-pointer` check's severity to HARD.** WARN-tier only, matching every other limb in this script — see §0.5 (D).

---

## §6 — Gate + status return taxonomy

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | All §2 steps passed; all per-step gates green; no scope creep. | CC reviews diff + gates, recommends merge to Joshua. |
| `DONE_WITH_CONCERNS` | Work completed but Cursor flags a doubt CC should resolve before accepting. | CC reviews concerns; accepts or re-dispatches with clarification. |
| `NEEDS_CONTEXT` | Cannot proceed without missing/contradicted input (e.g., Step 0's staleness check found the frozen "old text" doesn't match disk). | CC supplies context; re-dispatches same plan. |
| `BLOCKED` | Structural obstruction; sub-case required. | CC escalates or decomposes. |

**Closure report format:**
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [...], 2.2 [...], 2.3 [...], 2.4 [...], 2.5 [...]
Diffs (files touched): <list — must be exactly the 9 files>
PR: <url>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (CC, after Cursor returns)

**Pass 1 — Spec-compliance audit.**
- [ ] `SUBSCRIPTION_LEDGER.md` content matches §2 Step 2.1 verbatim
- [ ] All seven pursuit-record edits match §2 Step 2.2's old/new pairs exactly, nothing else in those files changed
- [ ] `check_pursuit_records.py` diff matches §2 Step 2.3 exactly — no reformatting drift
- [ ] Test file additions match §2 Step 2.4, existing tests unmodified
- [ ] Diff touches exactly 9 files — flag any unexpected path

**Pass 2 — Quality audit.**
- [ ] `python scripts/check_pursuit_records.py` exits 0 on the PR branch
- [ ] `pytest tests/scripts/test_check_pursuit_records.py -v` fully green
- [ ] `python scripts/gate_manifest.py --tier pre-commit` exits 0
- [ ] No HARD-severity finding introduced anywhere

**Pass 3 (§2 has 5 steps, >1) — Final consolidated read.** Read the full diff together: does the ledger's content actually match what each of the seven pursuit records now claims (no drift between the two)? Does the new checker limb's message text reference the correct ADR path?

Only after all three passes does CC recommend Joshua merge.

---

## §10 — Audit hooks (runnable)

```bash
# Ledger content matches frozen spec
diff <(sed -n '/^# Subscription/,$p' docs/pursuits/SUBSCRIPTION_LEDGER.md) /dev/stdin <<'EOF'
# (compare against this brief's §2 Step 2.1 block by eye — no single grep captures a full-file diff)
EOF

# All seven records carry the pointer
grep -L "SUBSCRIPTION_LEDGER.md" docs/pursuits/d1[1-7]-*.md
# Expected: empty (no file lacks the pointer)

# Checker + tests green
python scripts/check_pursuit_records.py
pytest tests/scripts/test_check_pursuit_records.py -v

# Diff touches exactly the 9 expected files
git diff <pre-dispatch-commit>..<pr-head> --name-only | sort
# Expected: docs/pursuits/SUBSCRIPTION_LEDGER.md, docs/pursuits/d11..d17 (7 files),
#           scripts/check_pursuit_records.py, tests/scripts/test_check_pursuit_records.py
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
# Mechanical discipline check on this handoff brief
$ python scripts/check_brief.py docs/briefs/handoffs/2026-08-21-cc-handoff-subscription-ledger-consolidation.md --type cc_handoff

# Confirm Cursor's closure report uses the four-state taxonomy
$ grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cursor-return-path>
```

If Cursor returned `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete; re-dispatch per §6 disposition guide.
