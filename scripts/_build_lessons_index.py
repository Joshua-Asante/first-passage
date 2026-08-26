#!/usr/bin/env python3
"""One-shot generator for docs/methodology/LESSONS_INDEX.jsonl.

NOT a standing script (no gate wires to it) -- it exists so the index's
provenance is reviewable as code rather than as an opaque data file, and so a
future re-generation from updated source lessons can start from a real diff
instead of hand-editing JSON. Run once, by hand, when the source lesson
registries change enough to warrant a rebuild:

    python scripts/_build_lessons_index.py > docs/methodology/LESSONS_INDEX.jsonl

Every "full" entry below was transcribed directly from primary source
(docs/methodology/lessons/execution_lessons.md, methodology_lessons.md, and
the two docs/lessons/*.md standalone files) by a full read of each file on
2026-08-26 -- not summarized by a subagent, not copied from a prior research
pass's paraphrase. Every "stub" entry's citing_files were confirmed by a grep
run on 2026-08-26 against the live tree; stub entries deliberately carry NO
one_line_lesson / mechanism / trigger fields, because their actual content
lives only in an external (Notion / Claude-memory) store this repo checkout
cannot read -- inventing plausible-sounding content for them would be
exactly the confabulation-under-plausible-cover failure class this index
exists to catch. See docs/methodology/LESSONS_INDEX.md for the schema notes
and how a session is meant to use this file.

full_ref anchors for the two lesson-registry files are computed by
resolve_anchor() from the REAL heading text, never hand-typed -- a stray
unicode symbol in a heading (M-18's real heading contains U+00D7 x, which
GitHub's slugifier strips entirely, not replaces with the letter "x")
silently produces a dead anchor if hand-typed and not caught until a test
walks every full_ref against the file it names.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TODAY = "2026-08-26"

EXEC = "docs/methodology/lessons/execution_lessons.md"
METH = "docs/methodology/lessons/methodology_lessons.md"


def _slugify(heading: str) -> str:
    """GitHub markdown-heading-anchor slugification: strip punctuation (an
    em-dash disappears, not collapses to one hyphen), then replace each
    remaining space with its own hyphen -- consecutive spaces are NOT
    collapsed first, so "M-18 -- Foo" (dash flanked by two spaces) becomes
    "m-18--foo" (double hyphen)."""
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s", "-", s)
    return s


_HEADING_CACHE: dict[str, list[str]] = {}


def resolve_anchor(rel_path: str, id_prefix: str) -> str:
    """Find the '## <id_prefix> ...' heading in rel_path and return
    'rel_path#slug', computed from the file's actual heading text."""
    if rel_path not in _HEADING_CACHE:
        text = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
        _HEADING_CACHE[rel_path] = re.findall(r"^#{1,6}\s+(.+)$", text, re.M)
    for heading in _HEADING_CACHE[rel_path]:
        if heading == id_prefix or heading.startswith(id_prefix + " "):
            return f"{rel_path}#{_slugify(heading)}"
    raise ValueError(f"no heading starting with {id_prefix!r} found in {rel_path}")


# ---------------------------------------------------------------------------
# FULL entries: transcribed from primary source, full read, this session.
# ---------------------------------------------------------------------------
FULL = [
    dict(id="E1", cls="E", status="DORMANT", status_note="PROMOTED 2026-04-29; DORMANT 2026-08-14 (watch-point script journal_review.py retired 2026-07-11, firings cannot accrue)",
         title="Trust the design through macro",
         one_line_lesson="Never skip a valid system signal on a macro-volatility forecast -- the filter stack already prices regime, and macro-volatile periods are when the strongest trends form.",
         cost_if_repeated="Anchor: 2026-04-07 Guardian XAUUSD skip during the US-Iran macro-stress window cost the largest single winner in the window's CSV, +$3,752 counterfactual (13-day hold to 2026-04-20).",
         trigger_globs=["ops/live_journal/**"],
         trigger_keywords=["discretionary skip", "macro override", "skip signal", "regime overlay"],
         full_ref=lambda: resolve_anchor(EXEC, "E1"),
         siblings=["E2"]),
    dict(id="E2", cls="E", status="DORMANT", status_note="PROMOTED 2026-04-29; DORMANT 2026-08-14 (watch-point script journal_review.py retired 2026-07-11, firings cannot accrue)",
         title="Don't decompose intended single-position holds",
         one_line_lesson="When a FIRE alert specifies one entry size, execute it as one entry -- splitting one trade into N sub-entries turns a 1R worst case into an aggregate ~3R worst case and degrades Aegis's BE-manufactured-winner mechanism.",
         cost_if_repeated="Anchor: 2026-04-15 Aegis USDJPY -- a single 35-lot signal live-decomposed into 3 sub-entries; one hit its stop while the others ran. Backtest counterfactual +$6,467; realized +$362 -- a $6,105 execution gap, the largest single-day leakage in the 7-week audit window.",
         trigger_globs=["ops/live_journal/**"],
         trigger_keywords=["decompose entry", "sub-entry", "split position", "multi-fill single signal"],
         full_ref=lambda: resolve_anchor(EXEC, "E2"),
         siblings=["E1"]),
    dict(id="E3", cls="E", status="CANDIDATE", status_note="never promoted; DORMANT 2026-08-14 (promotion counter structurally unreachable, journal_review.py retired)",
         title="Capture skip rationale at skip time, not retrospectively",
         one_line_lesson="Retrospective skip-rationale recall skews toward flattering reconstruction; log a one-line reason (date, strategy, alert tag) at the moment of skip, not weeks later.",
         cost_if_repeated="No dollar anchor -- procedural lesson affecting rationale quality, not directly P&L. Never reached promotion (n=3 firing threshold) before its watch-point script retired.",
         trigger_globs=["ops/live_journal/**"],
         trigger_keywords=["skip rationale", "post-hoc reasoning", "retrospective skip review"],
         full_ref=lambda: resolve_anchor(EXEC, "E3"),
         siblings=["E1", "E2"]),
    dict(id="E4", cls="E", status="CANDIDATE", status_note="firing 1 of 3 for promotion (2026-06-01); DORMANT 2026-08-14 (promotion counter structurally unreachable)",
         title="Entry latency from manual SL/size adjustment (feed-realign lag)",
         one_line_lesson="Keep the live indicator on the execution feed at all times -- never hand-translate SL/size from a different-feed indicator at fire time; the manual-adjustment latency (not the price-basis difference) is what eats a breakout's front-loaded edge.",
         cost_if_repeated="Anchor: 2026-05-29 Striker DJ30 v4.5 -- indicator on Pepperstone, execution on Alchemy (~23pt basis); manual SL/size re-derivation cost ~21pt of late entry. Backtest counterfactual +$300.82; realized +$30 -- only 10.0% of edge captured, -$270.82 gap.",
         trigger_globs=["ops/live_journal/**"],
         trigger_keywords=["feed mismatch", "manual SL adjustment", "entry latency", "different feed indicator"],
         full_ref=lambda: resolve_anchor(EXEC, "E4"),
         siblings=["E1", "E2", "E3"]),

    dict(id="M-7", cls="M", status="CANDIDATE", status_note="2026-05-08, ~$103 single-incident anchor",
         title="Anticipation-alert audit before lock declaration",
         one_line_lesson="Before declaring a Pine strategy LOCK complete, grep the locked source for a paired alert() call inside every entry-condition branch -- alertcondition() alone requires manual per-chart UI wiring that silently lapses.",
         cost_if_repeated="Anchor: 2026-05-07 Guardian XAUUSD ~$103 entry slippage from a bar-late alert fire (alertcondition() only, no alert() call).",
         trigger_globs=["**/*.pine", "**/*indicator*.pine"],
         trigger_keywords=["lock complete", "alert(", "alertcondition(", "Pine lock", "strategy lock"],
         full_ref=lambda: resolve_anchor(METH, "M-7"),
         siblings=["M-11"]),
    dict(id="M-8", cls="M", status="CANDIDATE", status_note="2026-05-10, near-miss (wrong-verdict count 0, prevented by DONE_WITH_CONCERNS)",
         title="Mechanical thresholds need a qualitative override channel",
         one_line_lesson="Pair count-only disposition thresholds ('if count >= N') with a qualitative scope, or explicitly flag the threshold as mechanical-only and rely on DONE_WITH_CONCERNS to surface the gap.",
         cost_if_repeated="Near-miss only: GH #54 ULP audit returned 5 hits, all in archived/dormant code, zero in production risk-control sites -- caught by DONE_WITH_CONCERNS before a wrong verdict landed.",
         trigger_globs=["docs/briefs/**"],
         trigger_keywords=["disposition rule", "count >= N", "mechanical threshold", "qualitative gate"],
         full_ref=lambda: resolve_anchor(METH, "M-8")),
    dict(id="M-9", cls="M", status="PROMOTED", status_note="2026-05-10",
         title="Gitignored vendor-data manifests need a local pre-commit hash gate",
         one_line_lesson="CI cannot hash gitignored bytes -- a local pre-commit hash gate is mandatory for vendor-data manifests, or manual regen drifts silently.",
         cost_if_repeated="Anchor: GH #62 / PR #59 manifest-drift RCA -- on-disk CSVs changed between an 11:12 EDT commit and ~12:10/12:21 pre-flight; NAS100USD.csv went conclusively missing, undetected until a manual reconcile.",
         trigger_globs=["core/data/tv_exports/**", "core/data/bar_data/**", "core/data/external/**", "**/SHA256SUMS"],
         trigger_keywords=["vendor manifest", "SHA256SUMS", "gitignored data", "re-export"],
         full_ref=lambda: resolve_anchor(METH, "M-9"),
         siblings=["M-12", "M-22"]),
    dict(id="M-10", cls="M", status="PROMOTED", status_note="2026-05-10",
         title="FXIFY ops integration: validator routing beats parallel display layers",
         one_line_lesson="Route display and failure through one validator per firm; never default fake inputs that defeat an explicit skip path; persist audit-worthy completion as real timestamps.",
         cost_if_repeated="Anchor: FXIFY tooling shipped a parallel accounting layer alongside the firm-rule validator -- 5 contradiction surfaces found (flag merge, status-table adjacency, duplicate metrics, silent daily-loss default, phase-complete persistence ambiguity); pytest green caught none of them.",
         trigger_globs=["ops/**/accounts.py", "ops/**/cli.py"],
         trigger_keywords=["firm validator", "parallel display layer", "dd_remaining_pct", "phase_complete"],
         full_ref=lambda: resolve_anchor(METH, "M-10")),
    dict(id="M-11", cls="M", status="CANDIDATE", status_note="2026-05-28, $2,600 single-incident anchor (below $3K threshold)",
         title="Falsifier-scope shadow when patching inherited infrastructure",
         one_line_lesson="A patch's pre-registered falsifier must test the interaction between new behavior and infrastructure it inherits, not only the new behavior in isolation.",
         cost_if_repeated="Anchor: 2026-04-27/2026-05-07 alert() patches reused strictApproach/approachZone predicates originally authored as PLOT-only conditions, inheriting the wrong gate. Realized on 2026-05-19 Aegis USDJPY: -$2,299.50 vs +$300 counterfactual, -$2,600 single-trade ECR delta.",
         trigger_globs=["**/*.pine"],
         trigger_keywords=["inherited infrastructure", "falsifier scope", "silent zone", "patch interaction"],
         full_ref=lambda: resolve_anchor(METH, "M-11"),
         siblings=["M-7"]),
    dict(id="M-12", cls="M", status="CANDIDATE", status_note="2026-05-28, $0 (Poisson-luck no-cost outcome), workstream-class count 4",
         title="Gitignored-target CC handoffs need post-execution verification beyond CC's own return status",
         one_line_lesson="When a handoff dispatches changes to a gitignored target (Pine, sealed configs, binaries), the parent MUST verify deployment via the system that owns the target -- CC's own DONE return is necessary but not sufficient, since git diff cannot reconstruct gitignored edits.",
         cost_if_repeated="Anchor: a 2026-05-19 CC handoff to patch all 4 locked Pine indicators returned DONE, but none of the 4 patches actually landed on TradingView -- undetected for 9 days until a manual TV-side grep on 2026-05-28.",
         trigger_globs=["**/*.pine"],
         trigger_keywords=["gitignored target", "CC handoff", "deployment verification", "DONE return status"],
         full_ref=lambda: resolve_anchor(METH, "M-12"),
         siblings=["M-9", "M-11", "M-AHF"]),
    dict(id="M-13", cls="M", status="CANDIDATE", status_note="2026-05-28, workstream-class wrong-state count 1 (dollars unmeasured)",
         title="Pine parameter-lock changes must update BOTH the strategy and indicator .pine",
         one_line_lesson="Every Pine parameter-lock change must be applied to both the strategy .pine AND the indicator .pine (the live alert/sizing source), and both re-exported -- a refresh applied to only one file silently splits backtest from live.",
         cost_if_repeated="Anchor: the 2026-05-23 allocation-refresh-2 ADR updated DJ30 pyramid 500->750 and NAS100 risk 0.45->0.37 in the strategy .pine only; the indicator .pine stayed stale 5 days -- live NAS100 ran ~22% over-risk, DJ30 pyramid ~33% under-sized.",
         trigger_globs=["**/*.pine", "docs/adr/*allocation*"],
         trigger_keywords=["pyramidSize", "riskPerTrade", "indicator vs strategy", "allocation refresh"],
         full_ref=lambda: resolve_anchor(METH, "M-13"),
         siblings=["M-12", "M-7", "M-11", "M-9"]),
    dict(id="M-14", cls="M", status="CANDIDATE", status_note="2026-06-01, $0 near-miss (caught pre-verdict by a Rule-0 Pine read)",
         title="Empty strategy-tester != indicator<->strategy divergence; check the Pine backtest endDate first",
         one_line_lesson="A zero-trade strategy-tester result is not evidence of indicator/strategy divergence until the strategy's endDate/startDate inputs are read -- a stale endDate silently gates out recent bars via inDateRange, and reproduces identically across every feed (a false corroborator of 'real divergence').",
         cost_if_repeated="Anchor: 2026-06-01 weekly review -- Striker DJ30/NAS100 backtests returned zero trades on live-fire windows across two feeds; escalating to 'real divergence' would have impugned every live signal. Actual cause: stale endDate = 2026-04-17/2026-04-20 gating longSignal.",
         trigger_globs=["**/*.pine"],
         trigger_keywords=["empty strategy tester", "zero trades", "endDate", "inDateRange", "indicator strategy divergence"],
         full_ref=lambda: resolve_anchor(METH, "M-14"),
         siblings=["M-13", "M-12"]),
    dict(id="M-15", cls="M", status="CANDIDATE", status_note="2026-06-19, $0 (caught on first real export, before any wrong verdict); a.k.a. M-ICT-1H-OFFSET",
         title="A pre-registered offline instrument needs a real-data faithfulness anchor; self-referential tests can't catch a scoring inversion",
         one_line_lesson="An offline harness that re-ports a source-of-truth computation (Pine offset, vendor engine) must be pinned against a REAL artifact from that source, not only its own fixtures -- self-referential tests prove internal consistency, never faithfulness, and can't catch a direction/offset inversion.",
         cost_if_repeated="Anchor: Q-ICT-CASCADE-1 ported Pine's backward historical offset series[fwdK] as a forward array index arr[i+fwdK], scoring the COMPLEMENT of the intended claim. A dedicated look-ahead audit detected the ~49% mismatch against real exported columns but discarded the ground truth in favor of its own buggy recompute; a 20-finding adversarial review also missed it. Caught only when a hand reconstruction matched the real export 100% vs the harness's ~36%.",
         trigger_globs=["lab/**"],
         trigger_keywords=["offline port", "Pine offset", "series[k]", "self-referential test", "faithfulness anchor", "look-ahead audit"],
         full_ref=lambda: resolve_anchor(METH, "M-15"),
         siblings=["M-9", "M-AHF", "M-14"]),
    dict(id="M-16", cls="M", status="CANDIDATE", status_note="2026-06-22, $0 near-miss (lab/-only)",
         title="Realistic entry-fill slip is the cheapest falsifier for a stop-entry edge; run it before any exit/sizing/MC",
         one_line_lesson="For any stop/break-entry candidate, run a fill-slip sweep (0/0.5/1/1.5 ticks) BEFORE building any exit design, sizing frontier, or first-passage MC -- spread-cost-clearable does not mean fill-robust, and realistic slip is often a larger tax than spread.",
         cost_if_repeated="Anchor: a US500 30-min ORB candidate showed +0.058R cost-net after spread charge, all-years-positive, p=0.012 -- but +1pt of break-bar slippage (generous, on an 18.8pt median range) flipped it to -0.031R; edge crosses zero at ~0.9pt slip. First-passage MC and an exit-policy sweep had already been commissioned before this cheaper test ran.",
         trigger_globs=["lab/analysis/**"],
         trigger_keywords=["fill slip", "stop entry", "break-bar slippage", "cost-net edge", "first-passage MC"],
         full_ref=lambda: resolve_anchor(METH, "M-16"),
         siblings=["M-19", "M-20", "M-21"]),
    dict(id="M-17", cls="M", status="CANDIDATE", status_note="2026-06-22, $0 (lab/-only)",
         title="The honest null for a time-of-day-anchored setup is a same-day time-placebo",
         one_line_lesson="To test whether a time-anchored intraday setup (opening range, session open) carries anchor-specific edge, the null must hold the day's price scale/volatility/cost fixed and vary only the anchor time -- cross-day rotation breaks on price-scale mismatch; direction-flip tests stop geometry, not the anchor.",
         cost_if_repeated="Anchor: US500 opening-range test. Direction-flip null was mechanically catastrophic (trivial 'rejection', p~0.0001); cross-day rotation was degenerate (2022 ~4000 level vs 2025 ~5800 path, null mean +74R). The honest same-day window-slide null showed the opening anchor genuinely special at p=0.012.",
         trigger_globs=["lab/analysis/**"],
         trigger_keywords=["time-anchored setup", "opening range", "placebo null", "same-day window slide"],
         full_ref=lambda: resolve_anchor(METH, "M-17"),
         siblings=["M-16"]),
    dict(id="M-18", cls="M", status="CANDIDATE", status_note="2026-06-22, $0 (lab/-only)",
         title="A deadline-capped challenge is a Sharpe race, not a symmetric first-passage; screen on the edge x frequency ceiling and prefer information-ratio exits",
         one_line_lesson="A prop-challenge objective (reach +5% before -5% within a horizon) is a Sharpe-race-with-a-deadline, not symmetric first-passage -- screen candidates on the analytic pass-ceiling (edge x frequency vs barrier) before any MC, and prefer highest information-ratio exits over highest-skew exits.",
         cost_if_repeated="Anchor: a Sharpe-~0.6 ~1-trade/day edge caps at ~58% challenge pass-rate regardless of sizing (computable a-priori, no MC needed). A low-variance give-back-33%-of-open-profit exit (WR 0.755) beat a max-positive-skew lottery exit for the 120-day-capped FXIFY challenge.",
         trigger_globs=["lab/analysis/**"],
         trigger_keywords=["prop challenge deadline", "first-passage", "Sharpe race", "pass-ceiling", "information ratio exit"],
         full_ref=lambda: resolve_anchor(METH, "M-18")),
    dict(id="M-19", cls="M", status="CANDIDATE", status_note="2026-07-14, $0 (docs/lab-only)",
         title="The DSR selection floor, not the bust/pass gate, is a discovery axis's binding reachability constraint -- governed by K, not sample size",
         one_line_lesson="Before committing a discovery axis, compute its DSR demonstrability floor at the axis's intrinsic trial count K and benchmark against the best in-house validated edge -- if the floor exceeds it, the axis is dead at the admission gate regardless of how forgiving the downstream survivor geometry is. The floor is governed by K, not n; more data does not help.",
         cost_if_repeated="Anchor: Q-GATECART-1 -- at banked GC/MGC K=3,177, the DSR floor (min Sharpe clearing DSR>=0.95) = 2.05, above the best in-house edge (Aegis 1.83) and ~2.4x the corrected published top-decile Sharpe (0.85). FALSIFIED by arithmetic before the cartography grid even ran.",
         trigger_globs=["lab/**", "docs/briefs/pre-registration/**"],
         trigger_keywords=["DSR floor", "discovery axis K", "trial count", "deflated Sharpe", "reachability screen"],
         full_ref=lambda: resolve_anchor(METH, "M-19"),
         siblings=["M-20", "M-21", "M-16"]),
    dict(id="M-20", cls="M", status="CANDIDATE", status_note="2026-07-16, two same-day firings (D5 + H-OD-1), ~$0 data cost + 2 full campaign cycles + 2 family-K spent re-deciding arithmetic",
         title="Reachability must be simulated per-gate, in the gate's own units, at the adjudication panel's price basis",
         one_line_lesson="A reachability attestation discharges a gate only when simulated in THAT gate's own units, at the basis the gate is scored on, with commissions divided out explicitly -- a Sharpe-space argument does not discharge a bp-space cost gate, and pricing at current market levels instead of the historical panel basis mis-scales the result.",
         cost_if_repeated="Anchor: D5 attested Stage-6 (Sharpe space) and never simulated Stage-2 (bp space) -- cohort edge ~2.97bp vs 11.06bp hurdle, unreachable ~3.7x. H-OD-1 simulated Stage-2 but at the wrong price basis (current ~4400 vs panel median 1942) plus a 10x commission mis-scale, masking a mechanism that actually confirmed in-sample (+1.444bp, t~5.0, 9/9 years positive) -- the gate math, not the mechanism, was the failure.",
         trigger_globs=["docs/briefs/pre-registration/**", "docs/methodology/strategy_harvest.md"],
         trigger_keywords=["reachability attestation", "cost gate", "bp space", "price basis", "commission scaling"],
         full_ref=lambda: resolve_anchor(METH, "M-20"),
         siblings=["M-19", "M-21"]),
    dict(id="M-21", cls="M", status="CANDIDATE", status_note="2026-07-17, $0 realized (caught by the downstream frozen engine, not by the breadth gate meant to catch it)",
         title="Against a dollar-trailing drawdown barrier, correlation breadth (dependence N_eff) is not admissibility; risk breadth (covariance N_eff) is",
         one_line_lesson="When admitting a candidate as a book leg against a dollar-denominated trailing drawdown barrier, require it to lift risk N_eff (covariance-matrix participation ratio) -- a positive dependence N_eff / low correlation is necessary context but never sufficient; screen the daily-$std ratio (candidate vs existing book) first, seconds-cost.",
         cost_if_repeated="Anchor: ORB-MNQ-1 admitted on dependence N_eff +0.96 ('near-independent diversifier') while its own risk N_eff delta was flat (+0.00, never decision-binding). Composing it at 0.37% weight detonated composed bust to 38.75% (Tradeify) / 67.63% (BluSky) vs a ~2.65% 2-leg baseline -- 15-23x over the 3.0% ceiling. Root cause: ORB's daily-$std ($438) alone exceeded the entire 2-leg book's ($273).",
         trigger_globs=["lab/research_utils/breadth.py", "docs/briefs/**compose**"],
         trigger_keywords=["risk N_eff", "dependence N_eff", "correlation breadth", "trailing drawdown barrier", "book leg admission"],
         full_ref=lambda: resolve_anchor(METH, "M-21"),
         siblings=["M-16", "M-19", "M-20"]),
    dict(id="M-22", cls="M", status="PROMOTED", status_note="2026-07-24, three-surface structural recurrence",
         title="Freshness/integrity gates over gitignored-generated content must presence-degrade (WARN, exit 0), never hard-fail, on a bare worktree/clone",
         one_line_lesson="Any always-on freshness gate that derives a compared field from disk-presence of a gitignored artifact must WARN and exit 0 when that artifact is absent (a worktree/clone), never hard-fail -- while still hard-failing every non-disk-derived field and real drift when the artifact IS present.",
         cost_if_repeated="Anchor: archive_lab_analysis.py --check --catalog-only hard-failed EVERY commit from any worktree/clone lacking gitignored heavy files (inputs/, *.pkl), and its own auto-fix hint (--regenerate-catalog) would have corrupted the canonical catalog by stripping correct annotations.",
         trigger_globs=["scripts/check_*.py", "docs/superpowers/specs/**"],
         trigger_keywords=["worktree gate false positive", "gitignored artifact", "presence-degrade", "hard-fail on absent bytes"],
         full_ref=lambda: resolve_anchor(METH, "M-22"),
         siblings=["M-9", "M-12", "M-13"]),
    dict(id="M-23", cls="M", status="CANDIDATE", status_note="dated incident 2026-07-24, detected 2026-07-28 (4 days later)",
         title="A parent-process config patch does not cross a process pool",
         one_line_lesson="Any run whose correctness depends on a mutated module-level constant must apply the mutation INSIDE the worker (after its own re-import), read the value back from the object the engine actually consumes, and assert the attested set is a singleton across every unit of work -- passing a config KEY rather than a resolved value lets a joblib worker silently re-resolve the still-defective on-disk config.",
         cost_if_repeated="Anchor: a 2026-07-24 band re-score rider patched FIRM_RULES in the parent process; its bootstrap arm fanned out via joblib passing only a firm-key string, so each worker re-imported from disk and scored the still-defective dd_lock_offset_usd:100 config. Published boot-95th figures 4.54%/4.49% were wrong; corrected values were 6.69%/17.79% -- an error of 1.5-7pp, optimistic (understated risk). Nothing errored; the defective path produced well-formed, plausible output.",
         trigger_globs=["**/*.py"],
         trigger_keywords=["joblib", "process pool", "parallel worker re-import", "module-level constant mutation"],
         full_ref=lambda: resolve_anchor(METH, "M-23"),
         siblings=["M-9", "M-12", "M-22", "M-24"]),
    dict(id="M-24", cls="M", status="CANDIDATE", status_note="dated incidents 2026-07-22 through 2026-07-28",
         title="When a venue fact is corrected in config, sweep for INDEPENDENT re-encodings of it",
         one_line_lesson="On correcting any venue fact, run a mechanic sweep (search for the numbers and the behavior, not just the config key) across every harness that simulates the affected phase -- a config fix does not reach an independent hard-coded reimplementation, which shares no identifier with the config and is invisible to any symbol-grep.",
         cost_if_repeated="Anchor: 'Tradeify eval accounts have no drawdown locking' was wrongly encoded in 3 independent places: (1) core/firm_rules.py dd_lock_offset_usd:100 (found 2026-07-22, +2.10pp bust, flipped a Part A PASS->FAIL, fix still unapplied); (2) the same config re-resolved incorrectly across a process boundary (=M-23); (3) hard-coded literals in gap_stage2_capbound.eval_sim, contaminating a downstream capital-allocation study's eval-pass-rate (63%), median (8.2mo), and a $339/acct-mo chain-rate figure.",
         trigger_globs=["core/firm_rules.py", "lab/**"],
         trigger_keywords=["venue fact correction", "hard-coded reimplementation", "mechanic sweep", "config fix blast radius"],
         full_ref=lambda: resolve_anchor(METH, "M-24"),
         siblings=["M-23", "M-9", "M-12", "M-22"]),
    dict(id="M-AHF", cls="M", status="PROMOTED", status_note="2026-05-10, third-instance auto-graduation; 4th anchor added 2026-07-06",
         title="Audit hooks check storage form, not human-readable property",
         one_line_lesson="Before committing a grep/assertion audit hook, state the property in plain language, cat the target file to confirm the regex matches the LITERAL storage form (not the author's mental form -- percent vs decimal, URL vs bare ID, commit metadata vs file content), and prefer property assertions over form matches when storage form is variable.",
         cost_if_repeated="4 dated instances: (1) a hook checked commit metadata as a proxy for content stability, missing actual drift; (2) a hook grepped MC-anchor pins in percent form when the file stored decimal form, matching zero pins; (3) a hook grepped a Notion page ID in URL form when the file stored the bare ID (self-caught, no cost); (4) a self-referential audit-hooks block quoted its own hook commands' expected output inside the same file it audits, so re-running post-commit self-matched on the quoted text and inflated counts.",
         trigger_globs=["docs/adr/**", "docs/briefs/**", "scripts/check_*.py"],
         trigger_keywords=["audit hook", "grep regex assertion", "storage form", "mental form mismatch"],
         full_ref=lambda: resolve_anchor(METH, "M-AHF"),
         siblings=["M-12", "M-15", "M-SWAP-1"]),
    dict(id="F-1", cls="F", status="CANDIDATE", status_note="2026-05-16, retroactive seed (defect predates F-class infrastructure)",
         title="TradingView <30-day JPY P&L inflation (~153x at USDJPY ~150)",
         one_line_lesson="Before citing an analysis-script output as brief evidence, confirm the script has a fixture test pinning its anchor invariant against an independently derived expected value, and that pytest is green -- order-of-magnitude defects escape eyeballing when the wrong magnitude is plausible at first glance.",
         cost_if_repeated="Anchor: TradingView reports JPY-quoted P&L in raw JPY (not USD) on holds strictly under 30 calendar days -- a figure that looks like a plausible USD value but is inflated ~153x at USDJPY ~150. Discovered manually during a Q-MT5-TV equivalence cross-check; no fixture suite existed yet to catch it.",
         trigger_globs=["**/*.py"],
         trigger_keywords=["TradingView JPY P&L", "fixture test", "order-of-magnitude defect", "USDJPY inflation"],
         full_ref=lambda: resolve_anchor(METH, "F-1"),
         siblings=["M-AHF"]),
    dict(id="M-SWAP-1", cls="M", status="PROMOTED", status_note="2026-05-26 dollar-cost anchor, upgraded same day to wrong-verdict anchor on Q-SWAP-2 closure",
         title="Risk-normalized MC absorbs additive-cost shocks via implied_1r recalibration",
         one_line_lesson="If a Pre-Q tests the lock-decision impact of an additive cost shock (swap, slippage, commission), verify whether implied_1r shifts materially -- if it does, run BOTH adaptive-1R and fixed-1R MC (frozen pre-shock baseline) and take the more conservative verdict; live Pine sizes by ATR, not median loss, so the shock is purely additive live even when adaptive-1R MC absorbs it into a smaller simulated position size.",
         cost_if_repeated="Anchor: Q-SWAP-1 -- swap cost applied to adaptive-1R MC barely moved verdict gates (Δbust 0.01pp) while reality showed $59,153 hidden per panel-year-equivalent on Guardian alone (-10.34% raw Net). Re-running under fixed-1R calibration (Q-SWAP-2) flipped the verdict FALSIFIED -> AMBIGUOUS-HOLD, provisionally retracting a prior ADR's 'criteria clear with margin' claim.",
         trigger_globs=["**/portfolio_mc.py", "docs/briefs/**swap**"],
         trigger_keywords=["implied_1r", "adaptive-1R", "fixed-1R", "additive cost shock", "swap MC"],
         full_ref=lambda: resolve_anchor(METH, "M-SWAP-1"),
         siblings=["M-AHF", "M-7", "F-1"]),
    dict(id="M-Q-SWAP-3-2", cls="M", status="CANDIDATE", status_note="2026-05-26, first worked example after gate-doctrine codification",
         title="Regime-robustness gate floor doctrine: headline criteria, never a relaxed strict-lock floor",
         one_line_lesson="When a brief's headline criteria are multi-metric (not a simple pass-rate), the Phase-4 regime-robustness floor must be EXPLICITLY specified as the same multi-metric headline criteria, never defaulted to the (more permissive) strict-lock criteria -- the relaxed reading lets a config falsely pass Phase 4 by not breaking the strict lock under regime variance.",
         cost_if_repeated="Anchor: Q-SWAP-3's original brief specified the relaxed floor (bust<1%, p99 DD<5%) instead of its own multi-metric headline (p99 DD<4.50%, bust<1.00%, median<=30d). Under the relaxed floor, GA-4's Bootstrap (4.91/0.48) and H1 (4.90/0.49) would have falsely PASSED Phase 4, producing an unjustified ADR superseding the 2026-05-23 allocation lock. Caught by the Phase-0 dispatch agent as a §0.5 ambiguity before it locked in.",
         trigger_globs=["docs/methodology/regime_robustness_gate.md", "docs/briefs/**"],
         trigger_keywords=["regime-robustness floor", "Phase 4", "headline criteria", "strict-lock floor"],
         full_ref=lambda: resolve_anchor(METH, "M-Q-SWAP-3-2"),
         siblings=["M-SWAP-1", "M-Q-REGIME-1"]),
    dict(id="M-Q-REGIME-1", cls="M", status="CANDIDATE", status_note="2026-05-26, first formal test of the N>=3 accumulating-signal hypothesis",
         title="The 2024-04-30 panel-temporal boundary is a structural regime inflection, not a sample-size artifact",
         one_line_lesson="When an investigation's half-panel split lands within +-2 months of 2024-04-30, treat the H1/H2 spread as priors-shifting, not sample-size noise -- if verdict-deciding, run a multi-boundary sweep (~5 min) rather than reaching for the sample-size discount, which is now rebuttable evidence, not a free move.",
         cost_if_repeated="Anchor: three independent investigations (Q-DDP-1, Q-GDN-DDcap, Q-SWAP-3) all landed an H1/H2 split near 2024-04-30 with unusually large spreads. A 5-boundary sweep {2023-07-31, 2024-01-31, 2024-04-30, 2024-07-31, 2025-01-31} showed |H1-H2| spread z=+2.056σ at 2024-04-30 (non-monotone local maximum, Spearman ρ=-0.500 -- two independent falsification signals pointing the same direction).",
         trigger_globs=["docs/methodology/regime_robustness_gate.md", "docs/briefs/**"],
         trigger_keywords=["2024-04-30 boundary", "H1 H2 split", "regime inflection", "boundary sweep"],
         full_ref=lambda: resolve_anchor(METH, "M-Q-REGIME-1"),
         siblings=["M-Q-SWAP-3-2", "M-SWAP-1"],
         memory_twin="project_2024_regime_shift_accumulating_signal"),

    dict(id="brief-authoring-traps-13-14-15", cls="standalone", status="CANDIDATE", status_note="2026-05-27, not yet promoted (fired 3x in one window, not 3 separate windows)",
         title="Brief-authoring traps #13/#14/#15: precision exceeds grounding, claim-to-test exceeds methodology, verdict-subset existence unverified",
         one_line_lesson="Before locking a brief's §1 framing or §3/§4 thresholds, explicitly enumerate its implicit assumptions about (a) current canonical state, (b) methodology-claim alignment, and (c) data shape supporting the verdict -- each needs authoring-time verification sourced from current canonical state, not memory or a prior brief.",
         cost_if_repeated="Three traps fired sequentially across one Q-JOINT-TAIL-1 brief sequence (2026-05-27): #13 (brief cited a week-stale MC anchor as current), #14 (brief claimed to test an assumption its methodology didn't actually test), #15 (verdict subset turned out to have 1 of 1141 days qualifying, later found N<30 even at the relaxed bar). No dollar cost (~4 review cycles counterfactual).",
         trigger_globs=["docs/briefs/**"],
         trigger_keywords=["brief authoring", "stale numerics", "verdict subset", "panel-shape sanity check"],
         full_ref=lambda: "docs/lessons/2026-05-27-brief-authoring-traps-13-14-15.md"),
    dict(id="M-25", cls="M", status="CANDIDATE", status_note="2026-07-06, registered via structural-argument bypass (not empirical E1/E2 gate); renumbered from a self-assigned M-19 on 2026-08-15 after a 40-day undetected collision with the canonical registry's real M-19",
         title="Close-vocabulary gap: pre-registration freezes the map before the data, but does not guarantee the map covers the eventual finding",
         one_line_lesson="When authoring a §3 outcome->standing map, run a close-label reachability check before freezing it: for each pre-registered terminal close label, confirm at least one reachable discriminator-outcome tuple satisfies it (not foreclosed by an earlier discriminator, not trivially satisfiable by noise alone).",
         cost_if_repeated="Two firings same window (2026-07-06): DJ30's §4 criteria had no multiplicity guard (a single spurious ELEVATED could false-graduate a candidate, repaired in-design); NAS's sole terminal close label ENGINEERED-BETA-CONFIRMED became permanently unreachable once an earlier discriminator returned GENUINE-CONTINUATION-DOMINATED (the map couldn't name the result that actually occurred).",
         trigger_globs=["docs/briefs/**"],
         trigger_keywords=["outcome standing map", "close label", "H-register", "pre-registration coverage"],
         full_ref=lambda: "docs/lessons/2026-07-06-close-vocabulary-gap.md",
         siblings=["brief-authoring-traps-13-14-15"]),

    dict(id="feedback_web_advisor_handoff_confabulates_repo_state", cls="feedback", status="PROMOTED",
         status_note="7 documented instances 2026-06-06 through 2026-07-11 (per .claude/workflows/handoff-verify-panel.js's own whenToUse text, verified by direct read 2026-08-26) -- \"the single most-fired lesson in memory\"",
         title="External handoffs narrate repo state that isn't true",
         one_line_lesson="External instruction packets (web-advisor notes, CC spawn briefs, Cursor Phase-0 packets, Downloads-staged artifacts) repeatedly narrate repo state that isn't true: phantom files claimed present, unlanded edits described as landed, already-executed programs described as pending, fabricated labels, wrong self-referential fire counts.",
         cost_if_repeated="7 documented instances in a 5-week span (2026-06-06 to 2026-07-11) -- the single most-fired lesson in this repo's memory. Mitigated by the handoff-verify skill (inline Phase-0 gate) and handoff-verify-panel workflow (fan-out edition).",
         trigger_globs=[],
         trigger_keywords=["handoff", "web advisor note", "CC spawn brief", "Cursor Phase-0", "confabulate"],
         full_ref=lambda: "external (Notion / Claude memory) -- cited verbatim in .claude/workflows/handoff-verify-panel.js and .claude/skills/handoff-verify/SKILL.md; full text not present in this checkout"),
    dict(id="lesson_gate_reachability_preregistration", cls="lesson", status="PROMOTED",
         status_note="5+ firings through 2026-08-10, climbing further afterward (per .claude/workflows/gate-reachability-audit.js's own whenToUse text, verified by direct read 2026-08-26)",
         title="A frozen pre-registered gate fails two independent ways: UNREACHABLE or UNBINDING",
         one_line_lesson="A frozen pre-registered gate fails either UNREACHABLE (cannot fire at the declared N/power/threshold given the campaign's real trial budget) or UNBINDING (live, even machine-enforced, but the campaign choreography never actually consults it before scoring/freeze).",
         cost_if_repeated="Named UNREACHABLE instances: Q-HARV-0, DISC-CAMP-0 (k_dsr=3177), MNQPROX-2 (n_paired=15). Named UNBINDING instances: dense-1m CON-1/CON-2 (a tier=always domain bar existed and would have fired, but the lane's Step-1 door check never reached it -- two campaigns ran fully unbound). Mitigated by the gate-reachability-audit workflow, mandatory at every G0/pre-registration freeze.",
         trigger_globs=["docs/briefs/pre-registration/**", "docs/spec/**"],
         trigger_keywords=["gate reachability", "pre-registration freeze", "UNREACHABLE", "UNBINDING", "door check"],
         full_ref=lambda: "external (Notion / Claude memory) -- cited verbatim in .claude/workflows/gate-reachability-audit.js; full text not present in this checkout",
         siblings=["M-19", "M-20"]),
    dict(id="feedback_adversarial_review_before_ratification", cls="feedback", status="PROMOTED",
         status_note="per .claude/workflows/pre-ratification-adversarial-panel.js's own whenToUse text, verified by direct read 2026-08-26",
         title="A green check_brief.py pass is FORM-only and has missed real BLOCKERs",
         one_line_lesson="A mechanical check_brief.py pass verifies form, not substance -- run a refute-first adversarial review before ratifying any Pre-Q brief, ADR, lock decision, or closure, since a green mechanical check has missed real BLOCKERs before.",
         cost_if_repeated="A real R&D pipeline scoping brief carried 6 BLOCKERs invisible to a mechanical 6/6 PASS: a doubled/double-applied 4x cost multiplier, an N-basis mismatch between two gates, an unread ADR clause, a claimed-but-never-scored screen, a missing dedup attestation, a false bounding claim. Reproduced in a controlled 2026-08-22 test with an external reviewer. Mitigated by the pre-ratification-adversarial-panel workflow (6 refute-first lenses + 2 skeptics + adjudicator).",
         trigger_globs=["docs/adr/**", "docs/briefs/**"],
         trigger_keywords=["check_brief.py", "ratification", "adversarial review", "BLOCKER"],
         full_ref=lambda: "external (Notion / Claude memory) -- cited verbatim in .claude/workflows/pre-ratification-adversarial-panel.js; full text not present in this checkout"),
]

# ---------------------------------------------------------------------------
# STUB names: bare pointer names found cited in-repo by name only, content
# lives in the external memory/Notion store this checkout cannot read. Each
# name's citing_files is populated by a real grep run below -- NOT hand-typed
# -- so a name with zero hits gets dropped rather than shipped as a stale
# unverified claim.
# ---------------------------------------------------------------------------
STUB_NAMES = {
    "feedback": [
        "absence_in_known_location_is_not_absence", "audit_doc_unreliable_for_pine_defaults",
        "check_origin_main_before_multistep_build", "dedup_attestation_must_be_executed",
        "discipline_guards_need_adversarial_tests", "hurst_rs_log_prices_trap",
        "oanda_dow_feed_artifact", "on_disk_artefact_can_be_wrong",
        "parity_gate_feed_and_pf_calibration", "per_strategy_pepperstone_baseline_uncommitted",
        "phase_4_floor_specification", "pine_offset_port_faithfulness_anchor",
        "quotes_from_reader_summaries_are_not_quotes", "rule0_pine_code_check",
        "run_cheap_falsifier_before_authoring", "section_7_skip_cost_concrete",
        "skill_amendments_via_authoring_path", "static_equity_default_for_param_compare",
        "two_tier_canonical_pepperstone_oanda", "unpriced_branch_search_the_corpus",
        "verify_owed_claims_before_reporting", "verify_source_not_label",
        "visible_restraint_in_closing_brief",
    ],
    "lesson": [
        "block_shuffle_needs_acf_match", "borrowed_numbers_need_connecting_arithmetic",
        "corrections_land_where_read", "cost_law_pre_screen_mr_fade", "crypto_trend_venue_wall",
        "databento_ohlcv1d_weekend_bars", "driver_layer_fix_leaves_kernel_default_stale",
        "dsr_floor_k_governed", "fifth_leg_no_regime_robust_static", "full_panel_masks_regime_split",
        "green_gate_is_not_coverage", "leading_indicator_pnl_gate_rationalization",
        "market_neutral_not_regime_neutral", "metric_cohort_provenance_binding",
        "offline_fill_port_inflates_native_tv_arbiter", "offline_port_needs_real_source_anchor",
        "oos_gate", "oos_gate_select_on_insample_only", "prereg_freeze_and_confound_control",
        "prop_archetype_drawdown_survival", "ratified_text_edited_alongside_authorized_change",
        "regime_detectability_wall", "regime_directional_graveyard", "reporting_burns_holdout",
        "rgignore_excludes_archive_from_repo_research", "roll_rule_changes_bar_existence",
        "snag_best_of_k_anchor_graveyard", "standalone_dd_window_artifact",
        "tradeify_trail_enforced_intraday", "trailing_dd_survival_is_skew_governed",
        "verify_content_not_path_or_id",
    ],
    "project": [
        "2024_regime_shift_accumulating_signal", "4strategy_mc_anchor_2026_05_05",
        "aegis_6j_transfer_state", "btc_fifth_leg_lead", "copygram_migration_state",
        "core_fxify_anchoring_audit", "databento_research_stack",
        "decompound_remc_canonical_shift_2026_06_07", "disccamp0_gate_reachability_audit",
        "dj30_mym_prototype_falsified", "ea_conversion_state", "futures_prop_pivot",
        "grokbot_evaluation_2026_08_18", "ict_cascade_true_state_qict1_moot",
        "missed_alpha_sweep_synthesis", "no_manual_trading_cfd_retirement",
        "ox_alpha_openrouter_evaluation_2026_08_22", "pyramid_is_strategy_for_nas100",
        "q_ict_1h_revcon_phase0a", "q_mech_1_family_synthesis", "q_nas_4_closure",
        "rnd_pipeline_state", "status_consistency_gate", "strategy_lifecycle_governance",
        "tradeify_consistency_payoff_shape_constraint_2026_08_22",
        "tradeify_discovery_channels_dry_2026_08_20", "tv_csv_canonical_feed_policy",
        "tv_egress_automation", "us_legal_master_research",
    ],
}


def grep_citing_files(name: str) -> list[str]:
    try:
        out = subprocess.run(
            ["git", "grep", "-l", "-F", name],
            cwd=REPO_ROOT, capture_output=True, text=True, check=False,
        )
    except OSError:
        return []
    if out.returncode not in (0, 1):
        return []
    files = [ln for ln in out.stdout.splitlines() if ln.strip()]
    return sorted(files)


def build_full_entry(d: dict) -> dict:
    return {
        "id": d["id"],
        "class": d["cls"],
        "status": d["status"],
        "status_note": d.get("status_note", ""),
        "title": d["title"],
        "one_line_lesson": d["one_line_lesson"],
        "cost_if_repeated": d["cost_if_repeated"],
        "trigger_globs": d.get("trigger_globs", []),
        "trigger_keywords": d.get("trigger_keywords", []),
        "full_ref": d["full_ref"](),
        "siblings": d.get("siblings", []),
        "memory_twin": d.get("memory_twin"),
        "content_verified": True,
        "last_verified_date": TODAY,
    }


def build_stub_entry(prefix: str, name: str, citing_files: list[str]) -> dict:
    full_id = f"{prefix}_{name}"
    return {
        "id": full_id,
        "class": prefix,
        "status": "external-unmigrated",
        "status_note": (
            "Name only, cited in-repo; full lesson content lives in an external "
            "Claude-memory / Notion store this checkout cannot read (per "
            "methodology_lessons.md's own Migration plan section). Do NOT infer "
            "content from the name -- verify against the external store or wait "
            "for it to be migrated into a full entry on next cite."
        ),
        "title": None,
        "one_line_lesson": None,
        "cost_if_repeated": None,
        "trigger_globs": [],
        "trigger_keywords": [],
        "full_ref": "external (Notion / Claude memory) -- not present in this checkout",
        "siblings": [],
        "memory_twin": None,
        "content_verified": False,
        "citing_files": citing_files,
        "last_verified_date": TODAY,
    }


def main() -> int:
    lines = []
    seen_ids = set()
    for d in FULL:
        entry = build_full_entry(d)
        if entry["id"] in seen_ids:
            print(f"DUPLICATE ID: {entry['id']}", file=sys.stderr)
            return 1
        seen_ids.add(entry["id"])
        lines.append(entry)

    dropped = []
    for prefix, names in STUB_NAMES.items():
        for name in names:
            full_id = f"{prefix}_{name}"
            if full_id in seen_ids:
                continue  # already a full entry (shouldn't happen, but stay safe)
            citing = grep_citing_files(name)
            if not citing:
                dropped.append(full_id)
                continue
            entry = build_stub_entry(prefix, name, citing)
            seen_ids.add(entry["id"])
            lines.append(entry)

    if dropped:
        print(f"# dropped {len(dropped)} name(s) with zero live citations: {dropped}", file=sys.stderr)

    for entry in lines:
        sys.stdout.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"# wrote {len(lines)} entries ({len(FULL)} full, {len(lines) - len(FULL)} stub)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
