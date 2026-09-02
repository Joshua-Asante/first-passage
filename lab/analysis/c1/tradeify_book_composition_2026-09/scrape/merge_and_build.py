"""Merge the walker + three gap-worker outputs, then build the daily table and splice the Pine file.
RAW  : tg_moc_raw.jsonl (+ .p1 .p2 .p3)  -> deduped by message id, rewritten in id order
DAYS : tg_moc_days.json (+ .p1 .p2 .p3)  -> per-day status: any partial that changed a day wins
Then: build_moc_table.main()  (CSV + Pine splice) and a coverage report by month."""
import json, os, collections, importlib
RAW = "tg_moc_raw.jsonl"; DAYS = "tg_moc_days.json"; PARTS = (".p1", ".p2", ".p3")

def main():
    rows = {}
    for suf in ("",) + PARTS:
        p = RAW + suf
        if not os.path.exists(p):
            continue
        for l in open(p, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            try:
                r = json.loads(l)
            except Exception:
                continue
            rows[r["id"]] = {"id": r["id"], "dt": r["dt"], "text": r["text"]}
    with open(RAW, "w", encoding="utf-8") as fh:
        for i in sorted(rows):
            fh.write(json.dumps(rows[i], ensure_ascii=False) + "\n")
    print(f"merged raw rows: {len(rows)}")
    base = json.load(open(DAYS))
    # compare each partial against the WALKER's original statuses (frozen), not the mutating merge --
    # otherwise a later partial's stale copy of another range reverts earlier partials' updates
    original = json.load(open(DAYS + ".walker")) if os.path.exists(DAYS + ".walker") else dict(base)
    if not os.path.exists(DAYS + ".walker"):
        json.dump(base, open(DAYS + ".walker", "w"), indent=0)
    changed = 0
    for suf in PARTS:
        p = DAYS + suf
        if not os.path.exists(p):
            print("missing partial", p); continue
        part = json.load(open(p))
        for k, v in part.items():
            if k in original and v.get("status") != original[k].get("status"):
                base[k] = v; changed += 1
    json.dump(base, open(DAYS, "w"), indent=0)
    c = collections.Counter(v["status"] for v in base.values())
    print(f"days: {len(base)} | statuses: {dict(c)} | changed by gap pass: {changed}")
    bym = collections.defaultdict(collections.Counter)
    for k, v in base.items():
        bym[k[:7]][v["status"]] += 1
    for m in sorted(bym):
        print(f"  {m}: {dict(bym[m])}")
    nf = sorted(k for k, v in base.items() if v["status"] not in ("found", "before-channel-start"))
    print("days without a print:", len(nf), nf)
    import build_moc_table
    importlib.reload(build_moc_table)
    build_moc_table.main()

if __name__ == "__main__":
    main()
