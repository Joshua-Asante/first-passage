# Public-exposure cleanup packet — 2026-10-09 (PREPARED, not applied)

**Status:** prepared under the operator's 2026-10-09 preparation handoff. Nothing below has been applied to GitHub. Editing or deleting any PR body or comment needs the operator's separate approval.

**Originals preserved:** `first-passage-archive` branch `archive/preserve-exposure-2026-10-09` (preservation commit `950ee0f`, manifest update `e273cbb`), manifest `preservation/2026-10-09-public-exposure/MANIFEST.json`.

**Substitution used:** the self-funded account's dollar starting capital becomes `E_0` (value private). No other wording changes, except removing one ratio that would have derived the value (comment `6074237135`).

## 1 — Replacement text by item

| Kind | ID | Author | Body has the figure | Diff-hunk copies | Who can act |
|---|---|---|---|---|---|
| PR body | `4795402344` | Joshua-Asante | yes | 0 | Joshua edits the body |
| issue comment | `6074228455` | Joshua-Asante | yes | 0 | Joshua edits the body |
| issue comment | `6074237135` | Joshua-Asante | yes | 0 | Joshua edits the body |
| issue comment | `6074252253` | Joshua-Asante | yes | 0 | Joshua edits the body |
| review comment | `4226569974` | chatgpt-codex-connector[bot] | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226569981` | chatgpt-codex-connector[bot] | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226569999` | chatgpt-codex-connector[bot] | no | 2 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226570012` | chatgpt-codex-connector[bot] | yes | 4 | delete only (bot-authored; needs operator approval) |
| review comment | `4226570018` | chatgpt-codex-connector[bot] | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226570024` | chatgpt-codex-connector[bot] | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226570041` | chatgpt-codex-connector[bot] | yes | 0 | delete only (bot-authored; needs operator approval) |
| review comment | `4226570054` | chatgpt-codex-connector[bot] | no | 6 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226570056` | chatgpt-codex-connector[bot] | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226570061` | chatgpt-codex-connector[bot] | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226570066` | chatgpt-codex-connector[bot] | yes | 0 | delete only (bot-authored; needs operator approval) |
| review comment | `4226570099` | chatgpt-codex-connector[bot] | yes | 1 | delete only (bot-authored; needs operator approval) |
| review comment | `4226570105` | chatgpt-codex-connector[bot] | no | 4 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226588984` | Joshua-Asante | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226589170` | Joshua-Asante | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226589624` | Joshua-Asante | no | 2 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226589774` | Joshua-Asante | yes | 4 | Joshua edits the body |
| review comment | `4226589933` | Joshua-Asante | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226590068` | Joshua-Asante | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226590388` | Joshua-Asante | yes | 0 | Joshua edits the body |
| review comment | `4226590763` | Joshua-Asante | no | 6 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226590896` | Joshua-Asante | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226591064` | Joshua-Asante | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226591494` | Joshua-Asante | yes | 0 | Joshua edits the body |
| review comment | `4226591962` | Joshua-Asante | no | 1 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226592081` | Joshua-Asante | no | 4 | not editable (diff hunk is GitHub's copy of the PR diff); deletion only |
| review comment | `4226599132` | Joshua-Asante | yes | 0 | Joshua edits the body |

A review comment's diff hunk is copied from the PR diff and cannot be edited; it disappears only if the comment is deleted. The PR's *Files changed* view and commits keep the original text regardless.

### PR body `4795402344` — Joshua-Asante — 2026-10-09T03:01:22Z

<details><summary>Replacement text</summary>

~~~~markdown
Records Joshua's 2026-10-09 decision to reopen a self-funded lane on his personal Tradovate account, and adds the frozen plan for choosing that account's portfolio. **Joshua confirmed every ruling recorded here on 2026-10-09 ("confirm").**

**What changes**
- **New concise ADR** `docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md`
  - Reopens the self-funded lane on the personal Tradovate account, with planned starting capital `E_0` (value private) and a maximum-growth objective. The portfolio is not yet selected.
  - The same account is the intended CME data source.
  - Clearance standard: at most a 15% peak-to-trough drawdown, with a 99-in-100 selection test and a live halt at 15% below peak.
  - Seven items are owed. Items 3–4 (API access and CME licensing) gate any feed activation and cover every destination the feed drives. Item 7 is a tested, fail-closed 15% halt.
- **New Pre-Q** `docs/briefs/Q-SFGROWTH-1-…` with a **frozen** verdict pre-registration (final freeze `ff9f6792`; amendments logged in §E)
  - Pool: five legs, including the NAS100 MNQ edition by operator ruling. Only normal mode is used.
  - Exports: one size-specific TradingView export per (leg, k). Contract counts are floored, and account-size inputs and initial capital scale by k.
  - Search space: K = 2,375, independent of the data. MNQ co-occupancy is excluded, and a conservative margin gate is applied.
  - Statistic and windows: pinned bootstrap; intraday peak-to-trough drawdown including intraday highs; one calendar with an Explore/Confirm split.
  - Verdict: VOID is evaluated first. Confirm runs at 1× and 1.5× cost, plus a roll-seam sensitivity.
- **Other edits**
  - Reverse `Superseded-in-part-by` edge on the 2026-07-16 ADR.
  - STATE: decision-index and forward rows (keep-15 roll).
  - `docs/briefs/INDEX.md` row.
  - `prop-firm-challenge` skill posture line.
  - Merged `main` into the branch.

**Reviews**
- Codex review on `d90eae8`: all 21 threads fixed, answered and resolved.
- Independent Claude re-review: **CLEAN** at `da6d15d`.

**Verification**
- `check_brief.py`: well-formed for both the ADR and the Pre-Q.
- `check_adr_graph.py`: OK.
- `check_state_currency.py`: OK.
- `check_root_doc_liveness.py`: OK.
- `gate_manifest.py --tier pre-commit`: exit 0. This needed `markdown-it-py` installed per `pyproject.toml` and `git fetch --unshallow` in the container.
- `fp.py check` did not start because the ops environment is absent, so the full gate suite has **not** been run locally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Q1B3t69LCnU8uvMMmNoPPe
~~~~

</details>

### issue comment `6074228455` — Joshua-Asante — 2026-10-09T04:24:22Z

<details><summary>Replacement text</summary>

~~~~markdown
## Independent Claude review at 5a5013d

**Verdict: FINDINGS** (5 × P1, 3 × P2). Not merged.

I reviewed `5a5013d62a90a7a2f2713380393ffc78f93ba897` (I did not draft this PR). The §E amendment closes 7 of Codex's 21 findings on `d90eae8`: intraday high, bootstrap, calendar, dedup/K, tie-break, 1.5× growth and the median. K is now analytic, which also clears the Phase 0/1 ordering finding. The rest are unaddressed, and none of the 21 threads is resolved or answered. I checked these against `main`:

**P1 (the frozen statistic stays ambiguous or misstates what can be traded)**
1. **Quantity baseline / input mode.** `remc_series_builder.DEFAULT_QUANTITY_SPEC` rescales Aegis to 8 (normal) / 3 (protected) and has a separate protected channel for each leg. The pre-registration doesn't say whether `q` means the raw export `Size (qty)` or the builder quantity, or which mode feeds `d_t`/`l_t`. Two implementers would build different series.
2. **Linear scaling of stateful legs.** The Striker day soft-stop latches on `initial_capital × strikerDayStopPct` (campaign §D15). It is a fixed-dollar threshold, so scaling quantity by `n/q` changes which later trades exist. A scaled full-size list isn't a path the reduced-size strategy can produce. A size-specific export or a proof of invariance is needed.
3. **Same-symbol MNQ co-occupancy.** ORB MNQ and Striker NAS100 MNQ can both be non-zero. `crosstrade_payload.py` sends `flatten_first=true` and `closeposition` keyed by account and instrument, so one leg can flatten the other while the score adds their P&L independently.
4. **Roll-seam limitation.** Campaign §D13(b) made stating the seam risk and a pre-registered seam-sensitivity check binding obligations for claims on these `1!` exports. This pre-registration carries neither.
5. **VOID precedence.** The §D rows overlap: an integrity failure can also fail condition (1). State that VOID short-circuits before (1)–(4).

**P1/P2 ADR and inputs**
6. The 15% live halt-and-flatten isn't among the six items owed before the first order. Nothing in `ops/c1_rail` or `core` implements it, so items 1–6 can all be done with no live stop in place.
7. The cost basis lists commission + exchange + NFA but not clearing or the account plan. Margin feasibility isn't gated, which matters for full-size 6J on `E_0`. Feed activation (Decision 3) can happen before items 3–4, which are framed as "before first order".
8. (P2) §A says "6J (full size; no micro on Tradovate)". The cited source (`core/firm_rules.py` :236-239) says only that **Tradeify** lacks M6J. The superseded ADR's §4 limb 1 requires the GO to come "with a fresh venue/parity checklist", which this ADR doesn't supply or explicitly waive. The binding is keyed `(portfolio, venue)`, but the concept ADR keys it `(portfolio, firm-tier)`.

Fast CI was still pending when I read it. Re-request a review after the fixes and the re-freeze.
~~~~

</details>

### issue comment `6074237135` — Joshua-Asante — 2026-10-09T04:25:14Z

<details><summary>Replacement text</summary>

~~~~markdown
## Independent Claude re-review at fec6ad2

**Verdict: FINDINGS** (1 × P1, 1 × P3). Supersedes my review at `5a5013d`.

Amendment 2 (`c208bde`) closes all eight findings from that review and the remaining Codex items. I checked the arithmetic: K = 6^5 − 1 − 5·5·6^3 = 7,775 − 5,400 = **2,375** ✓. VOID-first ✓. Normal mode with the leg-1 baseline at 8 ✓. MNQ co-occupancy exclusion ✓. Margin, clearing and the roll-seam condition (5) ✓. Item 7 in the ADR and feed gating on items 3–4 ✓. The `(portfolio, firm-tier)` key and the limb-1 checklist reading ✓.

**P1 — the size-specific export rule doesn't define sizing for the risk-sized Striker legs (2 and 5).** §B sets "every position-size input that is a contract count" to `floor(k × accepted value)`. Per [campaign §D15](../blob/main/docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md), both Strikers size through `calcSize`: `accountSize × riskPerTrade/100` from a static `accountSize` input (default 100000), not a contract-count input. Under the text as written:
- k does nothing for legs 2 and 5, so all five of their non-zero `k` exports are identical;
- a fixed `E_0` initial capital moves only the day soft-stop, which becomes many times tighter while positions stay at their reference size.

One implementer would leave the inputs alone, another would scale `accountSize` by k. They would produce different trade lists, and K would overstate the distinct prospective rules for those legs. Freeze the k-mapping for risk-sized legs, for example `accountSize = k × 100000` with any floor of the resulting contract count stated. Also say whether the soft-stop capital anchor is `E_0` or scales too. Confirm against the Pine in the operator checkout which legs are risk-sized versus fixed-count.

**P3.** In the brief, §6's RESOLVED disposition still says "proceed to ADR owed items 2–6"; the ADR now owes 7. The §6 VOID row's parenthetical also omits the margin snapshot, the roll dates and "k = 1 export has no trades". It defers to §D, so this is cosmetic.

Fast CI was still pending at this read.
~~~~

</details>

### issue comment `6074252253` — Joshua-Asante — 2026-10-09T04:26:44Z

<details><summary>Replacement text</summary>

~~~~markdown
Re: independent re-review at `fec6ad2`. Both findings are fixed in `ff9f6792`, and the plan is re-frozen with its hash recorded in `da6d15d`.

**P1.** I confirmed the premise against campaign §D15 and the §19c notes: `calcSize` reads a static `accountSize` (100000), and the day soft-stop is anchored to initial capital. The frozen mapping is now:
- contract-count inputs are set to `floor(k × reference)`;
- account-size inputs used for sizing are set to `k × reference`, unrounded, and the Pine rounds the resulting quantity;
- initial capital is set to `k ×` the reference export's value, so the soft-stop keeps its locked ratio to position size.

The `E_0` account exists only in the simulator, as `E_0`. Before any export is produced, Phase 0 classifies each leg's sizing inputs from the Pine in the operator checkout (without quoting it) and has that classification reviewed. Logged as §E item 13.

**P3.** The brief's §6 RESOLVED disposition now says items 2–7. Its VOID parenthetical now lists the margin and roll-date snapshots and the empty k = 1 export.

The skill-side brief checker and the pre-commit gates both pass.

---
_Generated by [Claude Code](https://claude.ai/code)_
~~~~

</details>

### review comment `4226570012` — chatgpt-codex-connector[bot] — 2026-10-09T04:20:12Z

Bot-authored: we cannot edit it. Shown for reference if it is deleted and re-posted as a quoted summary.

<details><summary>Replacement text</summary>

~~~~markdown
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Align stressed-cost growth with the hypothesis**

A candidate whose 1.5×-cost run has no more than 100 hits but a median terminal equity below `E_0` is `RESOLVED` here, because condition (3) checks only hits and condition (4) checks growth only at 1×. The parent hypothesis says the winner holds at 1× and 1.5× cost with a positive Confirm return, so this case receives conflicting verdicts. Explicitly require positive 1.5× growth or narrow the parent hypothesis to 1× growth.

Useful? React with 👍 / 👎.
~~~~

</details>

### review comment `4226570041` — chatgpt-codex-connector[bot] — 2026-10-09T04:20:12Z

Bot-authored: we cannot edit it. Shown for reference if it is deleted and re-posted as a quoted summary.

<details><summary>Replacement text</summary>

~~~~markdown
**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Reject configurations that exceed account margin**

The grid constrains only rounded contract quantities, so a configuration can clear drawdown and win growth while requiring more day or initial margin than the `E_0` account can supply, especially with full-size 6J or concurrent micro positions. The later firm-tier preflight cannot repair this because Confirm is restricted to the single winner and walking down the ranking is forbidden. Add a prospectively verified margin/capacity gate to every path or prefilter the grid using the account's applicable limits; Tradovate publishes distinct day and initial margins on its [margin schedule](https://www.tradovate.com/resources/markets/margin/?term=cbot).

Useful? React with 👍 / 👎.
~~~~

</details>

### review comment `4226570066` — chatgpt-codex-connector[bot] — 2026-10-09T04:20:12Z

Bot-authored: we cannot edit it. Shown for reference if it is deleted and re-posted as a quoted summary.

<details><summary>Replacement text</summary>

~~~~markdown
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Correct the claim that Tradovate has no yen micro**

The broker-availability claim is false for a personal Tradovate account: Tradovate's official [all-in rate sheet](https://www.tradovate.com/TradovateAllInRates120625.pdf) lists the E-Micro Japanese Yen contract `MJY`, and its [Micro FX toolkit](https://info.tradovate.com/hubfs/Micro_FX_Futures%20Toolkit.pdf) lists `M6J`. The repository source cited by the parent establishes only that Tradeify's product list lacks M6J, not that Tradovate does. Distinguish “no accepted micro trade list yet” from broker unavailability so the self-funded lane does not incorrectly rule out the feasible contract class.

Useful? React with 👍 / 👎.
~~~~

</details>

### review comment `4226570099` — chatgpt-codex-connector[bot] — 2026-10-09T04:20:12Z

Bot-authored: we cannot edit it. Shown for reference if it is deleted and re-posted as a quoted summary.

<details><summary>Replacement text</summary>

~~~~markdown
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Define the median for the even pooled sample**

Pooling three 10,000-path runs creates an even 30,000-value sample, for which “median” is not a unique order statistic: implementations may average the two central values or choose the lower or upper central value. Near the `E_0` gate or an Explore ranking tie, those conventions can change eligibility and the selected winner. Freeze an explicit quantile method or reference implementation.

Useful? React with 👍 / 👎.
~~~~

</details>

### review comment `4226589774` — Joshua-Asante — 2026-10-09T04:24:35Z

<details><summary>Replacement text</summary>

~~~~markdown
Fixed in 30c42f82. RESOLVED condition (4) now requires Confirm growth > `E_0` at c = 1 **and** at c = 1.5, which matches H-SFGROWTH-1.

---
_Generated by [Claude Code](https://claude.ai/code)_
~~~~

</details>

### review comment `4226590388` — Joshua-Asante — 2026-10-09T04:24:44Z

<details><summary>Replacement text</summary>

~~~~markdown
Fixed in c208bde9 with a conservative prefilter. A configuration is excluded when `Σ_i max_n_i × IM_i > `E_0``, where:
- `max_n_i` is the largest per-trade quantity in each leg's size-specific export;
- `IM_i` is Tradovate's initial margin, taken from a dated snapshot recorded in the Phase-0 manifest.

This assumes every leg holds its largest position at the same time. Excluded vectors still count in K.

---
_Generated by [Claude Code](https://claude.ai/code)_
~~~~

</details>

### review comment `4226591494` — Joshua-Asante — 2026-10-09T04:24:57Z

<details><summary>Replacement text</summary>

~~~~markdown
Fixed in c208bde9. Linear rescaling is removed. Every (leg, k) series, k = 1 included, now comes from its own export with these settings:
- initial capital at `E_0`;
- contract-count size inputs at `floor(k × accepted)`;
- all other inputs equal to the reference export's.

I verified the premise first: the campaign record shows the Striker day soft-stop catching different days at 200K and 100K initial capital.

---
_Generated by [Claude Code](https://claude.ai/code)_
~~~~

</details>

### review comment `4226599132` — Joshua-Asante — 2026-10-09T04:26:40Z

<details><summary>Replacement text</summary>

~~~~markdown
Correction to my reply above, superseded by ff9f6792. Initial capital is no longer a fixed `E_0`; it is `k ×` the reference export's initial capital. The Striker legs size from a static `accountSize` input, not from a contract count (campaign §D15). A fixed `E_0` would therefore have tightened the day soft-stop many times over while the positions stayed the same size. The rules are now:
- account-size inputs scale by `k`, unrounded;
- contract-count inputs stay at `floor(k × reference)`;
- Phase 0 classifies every sizing input from the Pine before any export is produced.

---
_Generated by [Claude Code](https://claude.ai/code)_
~~~~

</details>

## 2 — Owner coordination (PR #743)

PR #743's branch `ccr-b35046a2-2e9dnk` came from a remote Claude Code session (linked at the end of the PR body). Its review replies were posted through the operator's account, so the operator can edit those bodies; the Codex bot comments cannot be edited by us. For that session, or whichever session continues Q-SFGROWTH-1:

- write the starting capital only as `E_0` in public files; the value goes in the private Phase-0 manifest;
- start from the sanitized ADR, brief and pre-registration once this PR merges, and keep §E's redaction note;
- post no PR comments that restate the value.

## 3 — Nearby duplicates of the changelog passages

Search: `rg -F` over the public checkout for distinctive values and strings from the four changelogs (net P&L figures, recovery factors, loss sizes, parameter names and values, hour-block names).

| Location | What it repeats | Action here |
|---|---|---|
| `docs/adr/2026-04-17-striker-v4.3-pyramid.md` Consequences | Striker v4.3 backtest net/PF/RF/WR/trades/DD and μ/σ figures | **sanitized** (qualitative, pointer to archive) |
| `docs/adr/2026-04-17-striker-v4.3-pyramid.md` Risks | long max-DD duration in days | kept: a duration, not P&L; flagged |
| `docs/adr/2026-04-17-portfolio-allocations.md` Alternatives | Guardian/Striker recovery factors, Aegis μ/σ | kept, flagged: ratios inside a ratified allocation rationale |
| `ops/instruments/XAUUSD.md` (F7 row, 2026-06-21 log) | Guardian hour-block names, R deltas and one dollar delta | kept, flagged: separate filter-sweep record, outside the four changelogs |
| `core/lib/mvd.py`, `tests/core/test_mvd_selfchecks.py` | the Aegis month-end block expression as a string the check looks for | kept, flagged: code dependency; changing it changes a check |
| `docs/methodology/lessons/execution_lessons.md` | names "ATR expansion" among the filters | kept: generic |

Intentionally public and kept: risk%, pyramid size and `contractValue` ([CATALOG §Locked parameter record](../../core/strategies/CATALOG.md#locked-parameter-record-cfd-era-book)); historical portfolio MC anchors ([`mc_anchor_history.md`](../mc_anchor_history.md)), which the changelogs now point to instead of restating. The CATALOG says other strategy parameters live "in Pine only and [are] never duplicated in markdown"; the changelog parameter tables broke that rule.

## 4 — Exposure only history rewriting or deletion can address

- **Git history.** The four changelogs have been public since the initial public commit `027a729` (2026-08-14); the capital figure is in PR #743's commits (first in `7cbc87c`) and merge `c3bd414`. A merged draft PR leaves both readable.
- **PR #743 thread.** The PR body and 7 operator-authored comments carry the figure (editable, §1). 4 Codex bot review comments carry it in their bodies, and 22 review comments (11 bot, 11 operator) carry it in diff hunks; those copies go away only by deleting the comment. The *Files changed* view keeps it.
- **Other PRs.** `gh search prs`/`issues` found no other PR or issue matching the changelog figures or the capital figure; GitHub search tokenizes numbers poorly, so this is not proof of absence.
- **Forks and caches.** The repository reports 0 forks, 0 stars and 0 watchers (2026-10-09). Clones, GitHub's own caches, search-engine caches and any archive crawl cannot be recalled.

## 5 — Operator decisions

1. Merge this draft PR (sanitized changelogs, pyramid ADR line, #743 files)? **DECIDED 2026-10-09: yes** (Joshua, in chat to the merge agent).
2. Is the §E redaction note acceptable on a FROZEN pre-registration (value unchanged, symbol only), or should the pre-registration stay byte-identical with only the ADR, brief and index redacted? **DECIDED 2026-10-09: the §E redaction note is accepted** (Joshua, in chat to the merge agent).
3. Edit PR #743's body and the 7 operator comments with §1's text?
4. Delete the 4 Codex bot comments (and accept that the 22 diff-hunk copies go only if those comments are deleted too)? Deletion is irreversible; originals are in the archive.
5. Rewrite history (filter the changelogs and the figure from all commits, force-push)? This breaks every SHA cited in the repo and every open branch; recommended only if the exposure is judged material.
6. The flagged duplicates in §3: sanitize, or leave as ratified record?
