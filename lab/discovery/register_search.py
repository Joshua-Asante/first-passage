#!/usr/bin/env python3
"""
register_search.py — pre-registration ledger for discovery runs.

Turns "declare K before you look" from an intention into a file. Stdlib only —
this is a bookkeeping tool, not part of the science stack.

Subcommands
-----------
  open    Register a search BEFORE examining results: bind the search-space size
          K, alpha, data window, and hypothesis to a run id. Refuses to overwrite
          an existing registration (you cannot re-declare K after seeing results).
  close   Submit survivor p-values AFTER the run. Requires a prior `open`.
          Computes the Bonferroni floor (alpha/K), BH-FDR survivors at K, and the
          expected false positives under the global null (K*alpha). Writes the
          manifest the validation gate consumes. Verdict is ALWAYS a hand-off to
          strategy-validation, never a promotion.
  status  Print one manifest, or list all.

Ledger dir defaults to <repo-root>/discovery_manifests (anchored via __file__, so it
is cwd-independent and lands in the committed, auditable location); override with
DISCOVERY_LEDGER.

Notes on the statistics
-----------------------
- K is the PRE-REGISTERED search-space size (how many hypotheses were examined),
  NOT the number of survivors you kept. The multiplicity burden is the size of the
  search. All thresholds use registered K as the denominator.
- Submitted p-values are assumed to be the smallest among the K tests (i.e. the
  survivors). BH ranks them 1..s and steps up against (i/K)*alpha.
- These are the CHEAP triage. The rigorous universe-level correction (White RC /
  Hansen SPA / Romano-Wolf) lives in strategy-validation and needs all K returns.

Camp layout (orthogonal to this ledger)
---------------------------------------
This tool does not create analysis camps. When scaffolding a campaign dir under
``lab/analysis/`` (or later archiving it under ``lab/archive/``) that will carry
``test_*.py`` modules — especially a shared basename such as
``test_construct_lib.py`` — drop an empty ``__init__.py`` in that camp at create
time and load camp-local siblings via
``research_utils.camp_import.load_camp_sibling``. Hyphenated ``…_YYYY-MM``
slugs are not valid packages; CI relies on ``--import-mode=importlib``. See
``lab/CATALOG.md`` camp-layout note + MSL charter Camp layout line.
"""
import argparse
import csv
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from discovery.admission_schema import evaluate_admission, load_admission
from research_utils.repo_root import repo_root

# Committed home for manifests: <repo-root>/discovery_manifests, cwd-independent.
# DISCOVERY_LEDGER overrides for scratch / CI use.
_REPO_ROOT = repo_root()
LEDGER = Path(os.environ.get("DISCOVERY_LEDGER", str(_REPO_ROOT / "discovery_manifests")))


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _path(run_id):
    return LEDGER / f"{run_id}.json"


def _load(run_id):
    p = _path(run_id)
    if not p.exists():
        sys.exit(f"No registration for run-id '{run_id}'. Run `open` first (declare K before results).")
    return json.loads(p.read_text())


def _save(manifest):
    LEDGER.mkdir(parents=True, exist_ok=True)
    _path(manifest["run_id"]).write_text(json.dumps(manifest, indent=2))


def _resolve_params(args) -> str:
    """PD-3 fix: --params-file reads a JSON file directly, bypassing shell
    quoting entirely (an inline --params JSON string round-tripped through
    PowerShell/argparse into a manifest field containing literal
    backslash-escaped quotes -- human-readable but not machine-parseable).
    Validates the file parses as JSON before it is ever written to a
    manifest; --params keeps its free-text default behavior unchanged."""
    params_file = getattr(args, "params_file", None)
    if params_file is None:
        return args.params
    if args.params:
        sys.exit("ABORT: pass --params or --params-file, not both.")
    text = Path(params_file).read_text(encoding="utf-8")
    try:
        json.loads(text)
    except json.JSONDecodeError as exc:
        sys.exit(f"ABORT: --params-file {params_file} is not valid JSON: {exc}")
    return text


# Four fields ADR 2026-07-25 §2a established for cost_hurdle; reused here for
# every bundled reachability clause. units is recorded as-stated, never normalized.
_CLAUSE_FIELDS = ("value", "units", "basis", "source")


def _require_reachability_attestation(att_path):
    """HARV ADR 2026-07-13 §2 HARD gate: mechanism-first open needs a
    non-empty written reachability attestation on disk.

    Presence check first (exists + regular file + strip()-truthy). When the
    attestation is JSON, also enforce declaration-completeness: a per-clause
    list where every clause carries {value, units, basis, source} (ADR
    2026-07-25 §2a field shape). Returns the parsed clause table for the
    mechanism-first manifest.

    Backward compatibility: existing attestations are prose markdown. A
    non-JSON file keeps the presence-only behaviour and emits a WARN naming
    the ADR — hard-failing prose would retroactively invalidate every frozen
    pre-registration. Returns None on the prose path (no clause table).
    """
    if att_path is None:
        sys.exit(
            "ABORT: mechanism-first campaign requires a non-empty reachability "
            "attestation (HARV ADR 2026-07-13 §2 HARD gate). Pass "
            "--reachability-attestation <path>. not provided."
        )
    p = Path(att_path)
    if not p.exists() or not p.is_file():
        sys.exit(
            "ABORT: mechanism-first campaign requires a non-empty reachability "
            "attestation (HARV ADR 2026-07-13 §2 HARD gate). Pass "
            "--reachability-attestation <path>. file not found."
        )
    text = p.read_text(encoding="utf-8")
    if not text.strip():
        sys.exit(
            "ABORT: mechanism-first campaign requires a non-empty reachability "
            "attestation (HARV ADR 2026-07-13 §2 HARD gate). Pass "
            "--reachability-attestation <path>. file empty."
        )
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        print(
            "WARN: --reachability-attestation is prose (non-JSON); "
            "declaration-completeness not enforced "
            "(ADR 2026-07-25). Prefer a JSON attestation with a per-clause "
            "list of {value, units, basis, source}.",
            file=sys.stderr,
        )
        return None
    return _require_attestation_clause_completeness(payload, att_path)


def _require_attestation_clause_completeness(payload, att_path):
    """Validate a JSON reachability attestation's per-clause field completeness.

    Accepts a top-level list of clause objects, or an object with a `clauses`
    list. The list must be NON-EMPTY, and each clause must carry
    {value, units, basis, source}; `units` must be non-empty (as-stated; never
    normalized — ADR 2026-07-25 §2a).
    """
    if isinstance(payload, list):
        clauses = payload
    elif isinstance(payload, dict) and isinstance(payload.get("clauses"), list):
        clauses = payload["clauses"]
    else:
        sys.exit(
            "ABORT: --reachability-attestation must be a JSON per-clause list "
            "(a top-level array, or an object with a `clauses` array) where "
            "every clause declares {value, units, basis, source} "
            f"(ADR 2026-07-25 §2a). got type {type(payload).__name__}."
        )
    # An empty clause list is the D5 failure mode itself -- a gate declared and
    # never simulated -- and it would satisfy a for-loop-only check vacuously.
    # A gate that never bites decays to ceremony (ADR 2026-07-25 §4, H3
    # calibration standard): declaring zero clauses is not a default pass.
    if not clauses:
        sys.exit(
            "ABORT: --reachability-attestation declares ZERO clauses. Every "
            "bundled gate must be declared with {value, units, basis, source} "
            "(ADR 2026-07-25 §2a; harvest Req 5). An empty declaration is the "
            "unsimulated-clause failure this gate exists to catch -- if the "
            "campaign genuinely bundles no gate, it does not need this lane."
        )
    for i, clause in enumerate(clauses):
        if not isinstance(clause, dict):
            sys.exit(
                f"ABORT: --reachability-attestation clauses[{i}] must be an "
                f"object with {{value, units, basis, source}} "
                f"(ADR 2026-07-25 §2a). got type {type(clause).__name__}."
            )
        name = clause.get("clause") or clause.get("id") or f"clauses[{i}]"
        for field in _CLAUSE_FIELDS:
            if field not in clause:
                sys.exit(
                    f"ABORT: --reachability-attestation clause {name!r} "
                    f"missing field {field!r}. Each bundled gate must declare "
                    f"{{value, units, basis, source}} (ADR 2026-07-25 §2a)."
                )
        units = clause["units"]
        if units is None or (isinstance(units, str) and not str(units).strip()):
            sys.exit(
                f"ABORT: --reachability-attestation clause {name!r} has empty "
                f"units. units is recorded as-stated and must be non-empty "
                f"(ADR 2026-07-25 §2a)."
            )
    return clauses


# Header that `scripts/instrument_profiles.py cell` emits as its first line.
# This is a cross-module contract, pinned by a test against real cmd_cell output.
PROFILE_CONSULT_HEADER = "=== {symbol} x {mechanism} ==="


def _require_profile_consult(consult_path, profile_cell):
    """Instrument-profile gate (ADR 2026-07-25 §2a): a mechanism-first open must
    declare the (instrument, mechanism) cell it occupies and carry the written
    `instrument_profiles.py cell` output for it.

    Mechanical check only (exists + regular file + strip()-truthy + names the
    declared cell) -- it deliberately does NOT parse the verdict. A DEAD cell is
    still openable; addressing a blocking prior is prose work the pre-registration
    author owns. The gate only enforces that they LOOKED.

    Consumes written output rather than importing the profile module: this file
    is lab/, the module is scripts/, and scripts/check_boundaries.py enforces
    that layer contract.

    The cell match is ANCHORED on the header `cmd_cell` emits, not on two
    independent substring tests. Substring matching false-accepted a sibling's
    consult wherever one symbol contains another -- declaring NQ while attaching
    MNQ's consult passed, because "NQ" occurs inside "MNQ". Parent-vs-micro is
    exactly the distinction this programme treats as load-bearing, so the loose
    form was not safe. `tests/test_discovery_register_search.py` pins the header
    contract against real `cmd_cell` output, so a future format change fails in
    tests rather than silently disarming this gate.
    """
    if not profile_cell or ":" not in profile_cell:
        sys.exit(
            "ABORT: mechanism-first campaign requires --profile-cell "
            "<SYMBOL>:<mechanism-id> (ADR 2026-07-25). "
            f"got: {profile_cell!r}"
        )
    symbol, mechanism = profile_cell.split(":", 1)
    if not symbol or not mechanism:
        # "" is a substring of everything -- an empty half would vacuously
        # satisfy any consult, silently disarming the check below.
        sys.exit(
            "ABORT: --profile-cell needs a non-empty SYMBOL and mechanism-id "
            f"(ADR 2026-07-25). got: {profile_cell!r}"
        )
    if consult_path is None:
        sys.exit(
            "ABORT: mechanism-first campaign requires a written profile consult "
            "(ADR 2026-07-25). Run:\n"
            f"  python scripts/instrument_profiles.py cell {symbol} {mechanism} > consult.txt\n"
            "then pass --profile-consult consult.txt. not provided."
        )
    p = Path(consult_path)
    if not p.exists() or not p.is_file():
        sys.exit(
            "ABORT: mechanism-first campaign requires a written profile consult "
            f"(ADR 2026-07-25). --profile-consult {consult_path}: file not found."
        )
    text = p.read_text(encoding="utf-8")
    if not text.strip():
        sys.exit(
            "ABORT: mechanism-first campaign requires a written profile consult "
            f"(ADR 2026-07-25). --profile-consult {consult_path}: file empty."
        )
    if PROFILE_CONSULT_HEADER.format(symbol=symbol, mechanism=mechanism) not in text:
        sys.exit(
            f"ABORT: --profile-consult {consult_path} does not name the declared "
            f"cell {symbol} x {mechanism}. A consult for a different cell is not "
            "evidence for this one. Regenerate it with:\n"
            f"  python scripts/instrument_profiles.py cell {symbol} {mechanism} > consult.txt"
        )


def _require_prereg(prereg_path, lane):
    """Bind a campaign to its frozen pre-registration body at open (2026-08-08).

    Motivation, measured: W4 (ADR 2026-08-07) defines the live minimal gate set as
    "G0-G5 + G8, **and any limb a campaign's own frozen prereg still binds**". That
    clause is unevaluable unless a campaign says which body is its own -- and before
    this gate the word "prereg" appeared ZERO times in this module. The only binding
    was an optional, undocumented `prereg` key that 9 of 13 manifests happened to
    carry (1 of those dangling), so 14 of 17 live campaign bodies had no machine
    pointer at all and W4's additive limb resolved to "unknown" or "empty".

    Mechanical check only, in the house style of the sibling gates: exists, regular
    file, markdown, non-empty. It deliberately does NOT parse the body, judge its
    freeze status, or require a §6 gate -- a body with no gate is a real (and
    recorded) condition, not something this gate should mask. It enforces that the
    campaign NAMED one.

    Returns the repo-relative POSIX path to record on the manifest, or None when
    not supplied on the blind lane. Absolute/os-specific paths are normalised so a
    manifest stays portable and greppable across clones.

    Lane asymmetry mirrors ``_require_admission``: required on mechanism-first (the
    default and live lane), omittable on blind so the frozen legacy 11-key schema
    stays byte-identical. Blind opens therefore remain unbound -- a known residual,
    not an oversight.
    """
    if prereg_path is None:
        if lane == "mechanism-first":
            sys.exit(
                "ABORT: mechanism-first campaign requires --prereg <path-to-frozen "
                "pre-registration .md>. W4's live gate set is a function of the "
                "campaign's own frozen body; an unnamed body makes that clause "
                "unevaluable. Pass the path you froze."
            )
        return None
    p = Path(prereg_path)
    if not p.exists() or not p.is_file():
        sys.exit(f"ABORT: --prereg {prereg_path}: file not found.")
    if p.suffix.lower() != ".md":
        sys.exit(f"ABORT: --prereg {prereg_path}: expected a markdown body (.md).")
    if not p.read_text(encoding="utf-8", errors="replace").strip():
        sys.exit(f"ABORT: --prereg {prereg_path}: file is empty.")
    try:
        rel = p.resolve().relative_to(_REPO_ROOT).as_posix()
    except ValueError:
        sys.exit(
            f"ABORT: --prereg {prereg_path}: must live inside the repo so the "
            f"manifest pointer resolves on a fresh clone."
        )
    return rel


def _require_admission(args, lane):
    """SPEC S6 + TNEC-1: EM0/EM2–EM5 + N-EDGE + DSR-cap refusal at open.

    EM1 / D1 / D2 are disclosure-only (recorded, never refuse). ``--admission-file``
    is required on mechanism-first. Blind may omit it (legacy 11-key schema).
    When supplied on either lane, refuse writes nothing.
    Returns the admission summary dict on ADMIT, or None when not evaluated.
    """
    adm_path = getattr(args, "admission_file", None)
    if adm_path is None:
        if lane == "mechanism-first":
            sys.exit(
                "ABORT: mechanism-first campaign requires --admission-file "
                "(SPEC S6 + TNEC-1: EM0/EM2–EM5 + N-EDGE + DSR-cap; EM1/D1/D2 "
                "disclosure-only). Pass a JSON admission object. not provided."
            )
        return None
    p = Path(adm_path)
    if not p.exists() or not p.is_file():
        sys.exit(f"ABORT: --admission-file {adm_path}: file not found.")
    try:
        admission = load_admission(p)
    except (ValueError, json.JSONDecodeError, TypeError) as exc:
        sys.exit(f"ABORT: --admission-file {adm_path} is not a valid admission: {exc}")
    result = evaluate_admission(admission, registered_k=args.search_space_size)
    if not result.admitted:
        reason = ",".join(result.reasons) if result.reasons else "unknown"
        print(
            f"[refuse] admission REFUSE reasons={reason} "
            f"K={args.search_space_size} floor={result.summary.get('floor_at_k')} "
            f"cap={result.summary.get('cap')} power={result.summary.get('power')}",
            file=sys.stderr,
        )
        sys.exit(
            f"ABORT: admission refused ({reason}). "
            "EM/TNEC / DSR-cap empty or failed at catalogue size — no manifest "
            "written (SPEC S6 + TNEC-1, $0/K=0)."
        )
    print(
        f"[admit]  admission ADMIT K={args.search_space_size} "
        f"floor={result.summary.get('floor_at_k')} "
        f"power={result.summary.get('power')}"
    )
    return result.summary


def open_run(args):
    run_id = args.run_id or f"disc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if _path(run_id).exists():
        sys.exit(f"ABORT: '{run_id}' already registered. Pre-registration is immutable; "
                 f"pick a new run-id rather than re-declaring K after results.")
    if args.search_space_size < 1:
        sys.exit("ABORT: --search-space-size (K) must be >= 1.")
    lane = getattr(args, "lane", "mechanism-first")
    att = getattr(args, "reachability_attestation", None)
    profile_cell = getattr(args, "profile_cell", None)
    profile_consult = getattr(args, "profile_consult", None)
    reachability_clauses = None
    if lane == "mechanism-first":
        reachability_clauses = _require_reachability_attestation(att)
        _require_profile_consult(profile_consult, profile_cell)
    # SPEC S6: after mechanism-first attestation gates, before any manifest write.
    admission_summary = _require_admission(args, lane)
    prereg_rel = _require_prereg(getattr(args, "prereg", None), lane)
    params = _resolve_params(args)
    manifest = {
        "run_id": run_id,
        "status": "open",
        "opened_at": _now(),
        "tool": args.tool,
        "K": args.search_space_size,
        "alpha": args.alpha,
        "data_window": args.data_window,
        "hypothesis": args.hypothesis,
        "params": params,
        "closed_at": None,
        "results": None,
    }
    # Blind / legacy: keep the 11-key schema byte-identical. Mechanism-first
    # records lane + attestation path only on that path (HARV HARD gate), plus
    # the declared profile cell + consult (ADR 2026-07-25), plus the parsed
    # clause table when the attestation is JSON (completeness gate).
    if lane == "mechanism-first":
        manifest["lane"] = lane
        manifest["reachability_attestation"] = att
        manifest["profile_cell"] = profile_cell
        manifest["profile_consult"] = profile_consult
        if reachability_clauses is not None:
            manifest["reachability_clauses"] = reachability_clauses
    if admission_summary is not None:
        manifest["admission"] = admission_summary
    if prereg_rel is not None:
        manifest["prereg"] = prereg_rel
    _save(manifest)
    print(f"[open]   registered '{run_id}'")
    print(f"[open]   tool={args.tool}  K={args.search_space_size:,}  alpha={args.alpha}")
    print(f"[open]   window={args.data_window}")
    print(f"[open]   -> run the discovery, then `close` with survivor p-values.")


def _bh(pvals, K, alpha):
    """Benjamini-Hochberg step-up, denominator = pre-registered K."""
    ranked = sorted(pvals)
    rows, max_reject = [], 0
    for i, p in enumerate(ranked, start=1):
        thr = (i / K) * alpha
        if p <= thr:
            max_reject = i
        rows.append({"rank": i, "pvalue": p, "bh_threshold": round(thr, 8)})
    for r in rows:
        r["bh_reject"] = r["rank"] <= max_reject
    return rows, max_reject


def close_run(args):
    manifest = _load(args.run_id)
    if manifest["status"] != "open":
        sys.exit(f"ABORT: '{args.run_id}' is '{manifest['status']}', not open. Cannot re-close.")

    # Operator-stopped closure (ADR 2026-07-26 clause 2-C): a campaign halted by
    # operator direction BEFORE its declared reads executed banks the EXECUTED
    # selection events, not the declared K. Guarded, because the difference is the
    # difference between an honest ledger and a laundering device:
    #   - requires an explicit --executed-k (never inferred),
    #   - requires --stop-reason and --executed-looks prose enumerating every look
    #     and its examiner (2-C condition iii),
    #   - refuses to raise K (this path may only bank the same or fewer),
    #   - records declared_K in provenance so the amendment is never invisible.
    # Campaigns that DID look close through the normal p-value path; the ratified
    # "abandoned campaigns still bank their K" rule is unchanged for them.
    if getattr(args, "operator_stopped", False):
        if args.pvalues or args.pvalues_file:
            sys.exit("ABORT: --operator-stopped is for campaigns stopped BEFORE results "
                     "existed. p-values imply reads executed -> close via the normal path.")
        if args.executed_k is None:
            sys.exit("ABORT: --operator-stopped requires --executed-k (the count of "
                     "selection events actually examined). It is never inferred.")
        if args.executed_k < 0:
            sys.exit("ABORT: --executed-k must be >= 0.")
        if args.executed_k > manifest["K"]:
            sys.exit(f"ABORT: --executed-k {args.executed_k} exceeds declared K "
                     f"{manifest['K']}. This path may only bank the same or fewer.")
        if not (args.stop_reason or "").strip():
            sys.exit("ABORT: --operator-stopped requires --stop-reason.")
        if not (args.executed_looks or "").strip():
            sys.exit("ABORT: --operator-stopped requires --executed-looks enumerating "
                     "every executed look and its examiner (ADR 2-C condition iii).")
        declared = manifest["K"]
        manifest["status"] = "closed"
        manifest["closed_at"] = _now()
        manifest["K"] = args.executed_k
        manifest["declared_K"] = declared
        manifest["closure_mode"] = "operator-stopped"
        manifest["stop_reason"] = args.stop_reason
        manifest["executed_looks"] = args.executed_looks
        manifest["results"] = {
            "n_submitted": 0,
            "executed_k": args.executed_k,
            "declared_k": declared,
            "candidates": [],
        }
        manifest["verdict"] = (
            "OPERATOR-STOPPED before declared reads executed. NO campaign verdict "
            "exists and none may be quoted. Banks executed selection events "
            f"({args.executed_k}) per ADR 2026-07-26 clause 2-C; declared K "
            f"({declared}) retained in provenance."
        )
        _save(manifest)
        print(f"[close]  '{args.run_id}'  OPERATOR-STOPPED")
        print(f"[close]  banked K = {args.executed_k} (declared {declared:,}, retained in provenance)")
        print(f"[close]  reason: {args.stop_reason}")
        print(f"[close]  no verdict exists for this campaign; do not quote one.")
        return

    # Gather p-values, optionally with candidate ids.
    labelled = []
    if args.pvalues_file:
        with open(args.pvalues_file, newline="") as fh:
            for row in csv.reader(fh):
                if not row or row[0].lstrip().startswith("#"):
                    continue
                if len(row) >= 2:
                    labelled.append((row[0].strip(), float(row[1])))
                else:
                    labelled.append((None, float(row[0])))
    elif args.pvalues:
        labelled = [(None, float(x)) for x in args.pvalues.split(",")]
    else:
        sys.exit("ABORT: provide --pvalues or --pvalues-file.")

    pvals = [p for _, p in labelled]
    if any(not (0.0 <= p <= 1.0) for p in pvals):
        sys.exit("ABORT: p-values must be in [0, 1].")

    K = manifest["K"]
    alpha = manifest["alpha"]
    if len(pvals) > K:
        print(f"[warn]   submitted {len(pvals)} p-values but K={K}. Survivors cannot "
              f"exceed the search space — check that K is the true search size.")

    bonf_thr = alpha / K
    bonf = [p for p in pvals if p <= bonf_thr]
    naive = [p for p in pvals if p <= alpha]          # significant at naive alpha
    killed = [p for p in pvals if bonf_thr < p <= alpha]  # naive-sig but multiplicity-killed
    bh_rows, max_reject = _bh(pvals, K, alpha)
    exp_fp = K * alpha

    manifest["status"] = "closed"
    manifest["closed_at"] = _now()
    manifest["results"] = {
        "n_submitted": len(pvals),
        "naive_alpha": alpha,
        "n_pass_naive_alpha": len(naive),
        "bonferroni_threshold": round(bonf_thr, 10),
        "n_pass_bonferroni": len(bonf),
        "n_multiplicity_killed": len(killed),
        "bh_rows": bh_rows,
        "n_pass_bh": max_reject,
        "expected_false_positives_global_null": round(exp_fp, 4),
        "candidates": [{"id": cid, "pvalue": p} for cid, p in labelled],
    }
    manifest["verdict"] = (
        "FIRST-PASS ONLY. Candidates clearing the crude multiplicity floor are "
        "listed above. This is NOT a promotion. Hand the full candidate set (all K "
        "returns) to strategy-validation for universe-level correction (White RC / "
        "Hansen SPA / Romano-Wolf) and the native-micro OOS gate before any candidate "
        "is trusted."
    )
    _save(manifest)

    print(f"[close]  '{args.run_id}'  K={K:,}  alpha={alpha}")
    print(f"[close]  naive alpha       : p <= {alpha:g}      -> {len(naive)} 'significant' "
          f"(expect ~{exp_fp:.0f} false at this threshold under the global null)")
    print(f"[close]  Bonferroni floor  : p <= {bonf_thr:.3e}  -> {len(bonf)} pass (FWER-controlled)")
    print(f"[close]  BH-FDR survivors  : {max_reject} of {len(pvals)} submitted")
    if killed:
        print(f"[close]  ** {len(killed)} candidate(s) significant at naive alpha={alpha:g} but "
              f"KILLED by the K={K:,} multiplicity floor -- the classic data-snooping false "
              f"positives. Do not carry these forward. **")
    print(f"[close]  verdict: first-pass only -> hand to strategy-validation. "
          f"Manifest: {_path(args.run_id)}")


def status(args):
    if args.run_id:
        print(json.dumps(_load(args.run_id), indent=2))
        return
    if not LEDGER.exists():
        print(f"No ledger at {LEDGER} yet.")
        return
    for p in sorted(LEDGER.glob("*.json")):
        m = json.loads(p.read_text())
        tag = m["status"].upper()
        print(f"{tag:7} {m['run_id']:32} tool={m.get('tool','?'):10} K={m.get('K','?')}")


def build_parser():
    p = argparse.ArgumentParser(description="Pre-registration ledger for discovery runs.")
    sub = p.add_subparsers(dest="cmd", required=True)

    o = sub.add_parser("open", help="Register a search BEFORE results (declare K).")
    o.add_argument("--run-id", help="Stable id. Auto-generated if omitted.")
    o.add_argument("--tool", required=True,
                   help="stumpy | ruptures | tsfresh | catch22 | hmmlearn | gplearn | pysr")
    o.add_argument("--search-space-size", type=int, required=True,
                   help="K: number of hypotheses examined (subsequences*windows, features, "
                        "expressions tried, penalty grid size, ...). The true search size.")
    o.add_argument("--alpha", type=float, default=0.05, help="Significance level. Default 0.05.")
    o.add_argument("--data-window", required=True, help="e.g. 2010-06-06:2026-01-01")
    o.add_argument("--hypothesis", required=True, help="The Notice-phase observation being probed.")
    o.add_argument("--params", default="", help="Free-text / JSON of the search config.")
    o.add_argument("--params-file", default=None,
                   help="Path to a JSON file with the search config -- reads the file "
                        "directly, bypassing shell-quoting entirely (mutually exclusive "
                        "with --params; validated as JSON before the manifest is written).")
    o.add_argument("--lane", choices=["blind", "mechanism-first"],
                   default="mechanism-first",
                   help="Discovery lane. Default mechanism-first (SPEC S6 + TNEC-1). "
                        "mechanism-first requires --reachability-attestation "
                        "(HARV ADR 2026-07-13 §2 HARD gate), profile consult "
                        "(ADR 2026-07-25), and --admission-file (SPEC S6 + TNEC-1 "
                        "N-EDGE; EM1/D1/D2 disclosure-only). "
                        "Pass --lane blind for the legacy 11-key schema.")
    o.add_argument("--reachability-attestation", default=None,
                   help="Path to a non-empty reachability-attestation file. "
                        "Required when --lane mechanism-first; ignored on blind.")
    o.add_argument("--profile-cell", default=None,
                   help="<SYMBOL>:<mechanism-id> this campaign occupies. "
                        "Required when --lane mechanism-first (ADR 2026-07-25).")
    o.add_argument("--profile-consult", default=None,
                   help="Path to saved `scripts/instrument_profiles.py cell "
                        "<SYMBOL> <mechanism-id>` output for --profile-cell. "
                        "Required when --lane mechanism-first; ignored on blind.")
    o.add_argument("--prereg", default=None,
                   help="Path to this campaign's frozen pre-registration .md. "
                        "REQUIRED on mechanism-first; recorded on the manifest as a "
                        "repo-relative path so W4's 'limbs the campaign's own frozen "
                        "prereg binds' is answerable. Omittable on --lane blind only.")
    o.add_argument("--admission-file", default=None,
                   help="Path to admission JSON (EM0/EM2–EM5 + optional N-EDGE / "
                        "confirm-power; EM1 + D1/D2 disclosure-only per TNEC-1). "
                        "Required when --lane mechanism-first (SPEC S6 + TNEC-1); "
                        "optional on blind — when present, Cap/EM0, N-EDGE, and "
                        "power refusals still abort with no manifest write.")
    o.set_defaults(func=open_run)

    c = sub.add_parser("close", help="Submit survivor p-values AFTER the run.")
    c.add_argument("--run-id", required=True)
    c.add_argument("--pvalues", help="Comma-separated survivor p-values.")
    c.add_argument("--pvalues-file", help="CSV: candidate_id,pvalue (or one p-value per line).")
    # Operator-stopped path (ADR 2026-07-26 clause 2-C) — stopped BEFORE reads executed.
    c.add_argument("--operator-stopped", action="store_true",
                   help="Close a campaign halted by operator direction before its declared "
                        "reads executed. Banks --executed-k, not declared K. Mutually "
                        "exclusive with p-values.")
    c.add_argument("--executed-k", type=int, default=None,
                   help="With --operator-stopped: selection events actually examined. "
                        "Never inferred; may not exceed declared K.")
    c.add_argument("--stop-reason", default=None,
                   help="With --operator-stopped: who stopped it and why.")
    c.add_argument("--executed-looks", default=None,
                   help="With --operator-stopped: enumerate every executed look and its "
                        "examiner (ADR 2-C condition iii).")
    c.set_defaults(func=close_run)

    s = sub.add_parser("status", help="Print one manifest, or list all.")
    s.add_argument("--run-id", help="Omit to list all registrations.")
    s.set_defaults(func=status)
    return p


if __name__ == "__main__":
    ns = build_parser().parse_args()
    ns.func(ns)
