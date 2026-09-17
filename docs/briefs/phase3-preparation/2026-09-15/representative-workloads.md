# Repeated representative synthetic workloads

**Provisional engineering observations, not an approved E1 budget.** No actual
market panels, private strategy ports, account source or qualification streams
were used. The complete test-domain composition and G5 security repairs were
still pending at measurement time. Raw observations, runtime identity and source
SHA256 maps are in [representative-workloads.json](representative-workloads.json).

## Work measured

One process, CPython3.12.14, three sequential repeats per workload, fixed synthetic
seed791946223. The interpreter was the existing `a1b-operator-input/.venv`
environment. The separate CPython3.13.2 test interpreter could not import pandas
outside its supplied dependency path (`dateutil` absent); no packages were
installed. Peak working set is the process lifetime high-water value, not a
per-run increment. Other application/system activity was not isolated.

| Workload | Wall minimum / median / maximum, seconds | CPU median, seconds | Peak working set |
|---|---|---|---|
| Assemble, replay, shared account kernel, serialize one500-session path |9.489 /10.090 /10.352|8.953|129,064,960bytes maximum|
| Generate8synthetic source months, choose6-month outer blocks, replay/prove alternate panel, rebuild inner blocks, sample/replay/kernel/serialize one500-session path |10.885 /11.467 /13.190|10.859|160,440,320bytes maximum|

Each path contains46,000M15 rows and184,000adapter-bar calls across four invented
adapters,5,012fills and54,022events. The path serialization is7,185,415bytes and
its digest is unchanged across repeats:
`744a5972e672e4c6059431449d87e988812ba9c4fed3298ed4dfe788b49152ca`.

The Part A fixture contains175source sessions and proves all175alternate-panel
occurrences/16,100bars before rebuilding171candidate five-session blocks.
Proof-plus-path serialization is9,696,449bytes; all repeats have digest
`185561d9d90e53550c558c95c7e6099b8dd729708f087bd967b5f53d0163b196`.
Median internal components: source generation0.404s, outer selection0.001s,
continuous proof/rebuild2.855s, sampled path replay/kernel6.550s, and combined
serialization1.427s. Medians of components need not sum to median total.

## Reproduction

From the isolated repository root, set `PYTHONDONTWRITEBYTECODE=1` and import
roots `PYTHONPATH=ops;core;ops/c1_rail` on Windows. With the recorded interpreter:

```text
python -m c1_rail.qualification.benchmark --horizon 500 --seed 791946223
python -m c1_rail.qualification.benchmark_part_a --horizon 500 --seed 791946223
```

Run each three times sequentially. The raw report additionally wraps each call
with `time.perf_counter()` and `time.process_time()`, invokes `gc.collect()` before
each repeat, and reads `production._peak_memory_bytes()` afterward. Outer wall
time includes source generation and source-hash collection even where a module's
internal timer does not. These commands produce synthetic counts/timing only.

## Limited scaling illustration

Using 10.0902747 seconds per 500-session path and the median combined
generation/selection/proof time (about 3.3 seconds), the draft n1=200, n2=970
and Part A depth 200 would imply:

| Draft case | Path count | Illustrative replay/proof time |
|---|---|---|
| E1,100PartA panels |3×200+3×970+100×200=23,510|65.99hours|
| E1,200PartA panels |3×200+3×970+200×200=43,510|122.14hours|
| Later sole n3,970 per FULL/H1/H2 |3×970=2,910|8.16hours|

These are linear illustrations, not resource bounds or ratified depths. They
exclude initial FULL/H1/H2 proof, probes, runtime capture/verification, G1/G2/G5,
durable receipts, actual source I/O and the final output inventory. The175-session
proof fixture is shorter than the intended historical population, so its proof
cost cannot stand in for that workload. Invented adapters have different
indicator complexity, fill behavior and memory use from accepted private ports.
No entire100/200-panel batch or qualification depth was run. Final compute
acceptance must account for these differences, the accepted integrated revision
and its actual frozen source population before requesting exact-depth approval.
