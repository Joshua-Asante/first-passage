#!/usr/bin/env python3
"""
db_fetch.py — cost-gated Databento GLBX.MDP3 fetch with a local DBN cache.

Two subcommands:
  estimate  — read-only cost/size/record dry-run. Uses metadata endpoints only,
              which do NOT bill for the underlying data, so this is always free.
  pull      — run the estimate, enforce a --max-cost ceiling, then stream to a
              local DBN cache keyed by request params. Re-pulls hit cache.

The API key MUST be supplied via the DATABENTO_API_KEY environment variable.
Never pass it inline; never commit it.

Cache dir defaults to ~/.databento_cache, override with DATABENTO_CACHE.

Examples
--------
  python db_fetch.py estimate \
      --symbols ES.FUT --stype parent --schema trades \
      --start 2024-02-12 --end 2024-02-17

  python db_fetch.py pull \
      --symbols ES.c.0 --stype continuous --schema ohlcv-1m \
      --start 2010-06-06 --end 2026-01-01 --max-cost 5.00 --out es_1m.parquet
"""
import argparse
import hashlib
import os
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    import databento as db
except ImportError:
    sys.exit("databento not installed. Run `pip install databento` in the research venv.")

DATASET = "GLBX.MDP3"
CACHE_DIR = Path(os.environ.get("DATABENTO_CACHE", Path.home() / ".databento_cache"))

# Ratified campaign default (temporal-not-instrument OOS axis): discovery + ALL
# tuning are IS-only through this date; the OOS era (2019-05-06+) is a hold-out.
# Source: DISC-CAMP-0 pre-registration §2 + docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md.
RATIFIED_IS_BOUNDARY = "2018-12-31"


def _enforce_phase_boundary(args) -> None:
    """Structural IS/OOS cap: a `--phase discovery` request cannot read past the IS
    boundary. Fires BEFORE any (even free) databento call so a mis-scoped discovery
    pull fails cheap. No-op when `--phase` is absent (byte-identical legacy path)
    or `--phase oos` (the hold-out is allowed past the boundary).

    `--end` is EXCLUSIVE, so the last INCLUDED date is end-1; the full IS window
    through 2018-12-31 is `--end 2019-01-01`, which must be allowed."""
    if getattr(args, "phase", None) != "discovery":
        return
    boundary = date.fromisoformat(getattr(args, "is_boundary", None) or RATIFIED_IS_BOUNDARY)
    last_included = date.fromisoformat(args.end[:10]) - timedelta(days=1)
    if last_included > boundary:
        sys.exit(
            f"\nABORT: --phase discovery cannot read past the IS boundary {boundary} "
            f"(--end={args.end} exclusive => last bar {last_included}).\n"
            f"Discovery + all tuning are IS-only; the OOS era is a hold-out. Use "
            f"--phase oos for the hold-out, or correct --end (override the ratified "
            f"boundary only with a stated campaign reason via --is-boundary)."
        )


def _client() -> "db.Historical":
    key = os.environ.get("DATABENTO_API_KEY")
    if not key:
        sys.exit("DATABENTO_API_KEY is not set. Export it; never pass the key inline.")
    return db.Historical(key)


def _req_kwargs(args) -> dict:
    return dict(
        dataset=DATASET,
        symbols=args.symbols.split(","),
        schema=args.schema,
        stype_in=args.stype,
        start=args.start,
        end=args.end,
    )


def _cache_path(args) -> Path:
    parts = [DATASET, args.symbols, args.stype, args.schema, args.start, args.end]
    # Era-tag the key so a discovery read and an oos read of the same window land in
    # different cache entries. Fold in ONLY when non-None => omitting the new flags
    # keeps the hash (and every existing cache filename) byte-identical.
    campaign_id = getattr(args, "campaign_id", None)
    phase = getattr(args, "phase", None)
    if campaign_id is not None:
        parts.append(f"campaign={campaign_id}")
    if phase is not None:
        parts.append(f"phase={phase}")
    digest = hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]
    return CACHE_DIR / f"{args.schema}_{args.stype}_{digest}.dbn"


def _schema_range_bounds(rng: dict, schema: str) -> tuple[str, str] | None:
    """Extract (start, end) bound strings from a `get_dataset_range` response.

    Prefers the per-schema range (`rng["schema"][schema]`) over the
    dataset-wide range when both are present -- schemas can have a narrower
    availability window than the dataset as a whole (e.g. a microstructure
    schema starting later than ohlcv). Returns None on an unrecognized
    response shape so the caller can skip the check rather than guess.
    """
    if not isinstance(rng, dict):
        return None
    per_schema = rng.get("schema")
    if isinstance(per_schema, dict):
        entry = per_schema.get(schema)
        if isinstance(entry, dict) and "start" in entry and "end" in entry:
            return entry["start"], entry["end"]
    if "start" in rng and "end" in rng:
        return rng["start"], rng["end"]
    return None


def _check_request_in_range(args, rng: dict) -> None:
    """PD-1 fail-fast: compare the requested --start/--end against the
    dataset's (or schema's) available range and sys.exit with a clear,
    actionable message BEFORE the get_cost call -- instead of letting a
    request outside the available window surface as a raw
    `BentoClientError: 422 data_start_before_available_start` buried inside
    a metadata call (the DISC-CAMP-0 PD-1 catch: the frozen IS start
    2010-01-01 predates GLBX.MDP3's actual floor 2010-06-06).

    Only reached from the success path of estimate()'s get_dataset_range
    try/except -- if that fetch itself failed, this is never called and the
    existing non-fatal warning stands unchanged. Parses dates via the same
    slice + date.fromisoformat convention used elsewhere in this file (no
    new date-library dependency).
    """
    bounds = _schema_range_bounds(rng, args.schema)
    if bounds is None:
        return  # unrecognized response shape -- don't block on it
    avail_start, avail_end = bounds
    try:
        avail_start_d = date.fromisoformat(str(avail_start)[:10])
        avail_end_d = date.fromisoformat(str(avail_end)[:10])
        req_start_d = date.fromisoformat(args.start[:10])
        req_end_d = date.fromisoformat(args.end[:10])
    except ValueError:
        return  # unparseable bound -- don't block, get_cost is the real gate

    if req_start_d < avail_start_d or req_end_d > avail_end_d:
        sys.exit(
            f"\nABORT: requested window --start {args.start} --end {args.end} falls "
            f"outside {DATASET} schema '{args.schema}' available range "
            f"[{avail_start} .. {avail_end}].\n"
            f"Adjust --start/--end to fit inside the available window (see the "
            f"[range] line above for the exact bounds)."
        )


def estimate(args) -> float:
    """Print cost / billable size / record count. Returns estimated USD cost."""
    _enforce_phase_boundary(args)  # fail cheap before any (even free) API call
    client = _client()

    # Guard: is the requested window inside the dataset's available range?
    try:
        rng = client.metadata.get_dataset_range(dataset=DATASET)
        print(f"[range]    dataset available window: {rng}")
        _check_request_in_range(args, rng)  # PD-1 fix: fail fast, not inside get_cost
    except Exception as exc:  # non-fatal; the cost call is the real gate
        print(f"[range]    (could not fetch dataset range: {exc})")

    kwargs = _req_kwargs(args)
    cost = client.metadata.get_cost(**kwargs)  # default mode is historical-streaming; `mode=` is deprecated in the SDK
    size = client.metadata.get_billable_size(**kwargs)
    count = client.metadata.get_record_count(**kwargs)

    print(f"[estimate] cost      : ${cost:,.4f} USD (streaming)")
    print(f"[estimate] billable  : {size:,} bytes  (~{size / 1e9:.4f} GB)")
    print(f"[estimate] records   : {count:,}")
    return float(cost)


def pull(args) -> None:
    """Cost-gated streaming pull to the DBN cache, then load to a DataFrame."""
    cost = estimate(args)

    if cost > args.max_cost and not args.force:
        sys.exit(
            f"\nABORT: estimated ${cost:,.4f} exceeds --max-cost ${args.max_cost:,.4f}.\n"
            f"Raise --max-cost or pass --force only if this spend is intended."
        )

    path = _cache_path(args)
    if path.exists():
        print(f"[cache]    hit: {path}  (no new billing)")
    else:
        print(f"[pull]     streaming -> {path}")
        client = _client()
        data = client.timeseries.get_range(**_req_kwargs(args))
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        # PD-2 fix: write to a same-directory tmp file first, then atomically
        # replace the real cache path (os.replace is atomic on POSIX and
        # Windows). A crash/interrupt mid-write leaves ONLY the tmp file --
        # `path` itself is untouched until the write is known to have
        # completed -- so a later run's `path.exists()` cache-hit check can
        # never be fooled by a partial/corrupt file. Does not change the
        # final cache filename or _cache_path()'s hashing scheme.
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        try:
            data.to_file(tmp_path)
            os.replace(tmp_path, path)
        except BaseException:
            try:
                tmp_path.unlink()
            except OSError:
                pass
            raise

    store = db.DBNStore.from_file(path)
    df = store.to_df()
    print(f"[done]     {len(df):,} rows in cache.")
    print(f"[done]     reload elsewhere: "
          f"databento.DBNStore.from_file(r'{path}').to_df()")

    if args.out:
        store.to_parquet(args.out)
        print(f"[done]     wrote parquet: {args.out}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Cost-gated Databento GLBX.MDP3 fetch.")
    sub = p.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--symbols", required=True,
        help="Comma-separated. e.g. ES.FUT (parent), ES.c.0 (continuous), ESH4 (raw).",
    )
    common.add_argument(
        "--stype", default="parent",
        choices=["parent", "continuous", "raw_symbol", "instrument_id"],
        help="Symbology input type. Default: parent.",
    )
    common.add_argument(
        "--schema", required=True,
        help="ohlcv-1d | ohlcv-1h | ohlcv-1m | ohlcv-1s | trades | tbbo | "
             "mbp-1 | mbp-10 | mbo | definition",
    )
    common.add_argument("--start", required=True, help="ISO date/time, e.g. 2010-06-06")
    common.add_argument("--end", required=True, help="ISO date/time (exclusive).")
    # Campaign scoping (additive, default-off — omit for byte-identical legacy behavior).
    common.add_argument(
        "--campaign-id", default=None,
        help="Tag the cache entry to a campaign so a discovery read and an oos read "
             "of the same window never share a cache file.",
    )
    common.add_argument(
        "--phase", choices=["discovery", "oos"], default=None,
        help="discovery = IS-only (refuses --end past the IS boundary); oos = hold-out. "
             "Omit for un-scoped legacy behavior.",
    )
    common.add_argument(
        "--is-boundary", default=None,
        help=f"Override the ratified IS boundary (default {RATIFIED_IS_BOUNDARY}) for a "
             f"campaign that states its own reason. Only affects --phase discovery.",
    )

    est = sub.add_parser("estimate", parents=[common], help="Free read-only cost dry-run.")
    est.set_defaults(func=estimate)

    pl = sub.add_parser("pull", parents=[common], help="Cost-gated pull to DBN cache.")
    pl.add_argument(
        "--max-cost", type=float, required=True,
        help="Abort if the estimate exceeds this USD amount. No default, on purpose.",
    )
    pl.add_argument("--force", action="store_true", help="Override the cost ceiling.")
    pl.add_argument("--out", help="Optional parquet output path.")
    pl.set_defaults(func=pull)
    return p


if __name__ == "__main__":
    ns = build_parser().parse_args()
    ns.func(ns)
