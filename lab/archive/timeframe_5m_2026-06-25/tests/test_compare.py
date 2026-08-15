import compare

_HEADER = "Trade #,Type,Date and time,Net P&L USD,Net P&L %\n"

def _csv(tmp_path, name, pairs):
    # pairs: list of (date_str, pct). Each becomes an Entry+Exit row pair.
    lines = []
    for i, (d, pc) in enumerate(pairs, start=1):
        lines.append(f"{i},Entry long,{d},0,{pc}")
        lines.append(f"{i},Exit long,{d},0,{pc}")
    p = tmp_path / name
    p.write_text(_HEADER + "\n".join(lines) + "\n", encoding="utf-8")
    return p

def _spread(dates, pcts, n=60):
    # n deterministic pairs cycling the dates/pcts. n>=50 clears the 100-raw-row
    # MVD floor in io_tv.load_exits (each pair = 2 raw rows).
    return [(dates[i % len(dates)], pcts[i % len(pcts)]) for i in range(n)]

def test_compare_one_matches_window(tmp_path):
    # baseline spans 2022..2026 (3 dates x20 rows); proto only 2025 (2 dates x30)
    base = _csv(tmp_path, "base.csv",
                _spread(["2022-06-02 10:00", "2025-06-02 10:00", "2026-05-01 10:00"],
                        [1.0, -0.5, 0.5], n=60))
    proto = _csv(tmp_path, "proto.csv",
                 _spread(["2025-02-02 10:00", "2025-09-09 10:00"], [0.5, -0.25], n=60))
    r = compare.compare_one("striker", base, proto)
    assert r["span"]["proto_n"] == 60
    # window [2025-02-02, 2025-09-09]: of the 3 baseline dates only 2025-06-02
    # (20 of the 60 cycled rows) falls inside.
    assert r["span"]["baseline_in_window_n"] == 20
    assert r["baseline"]["trades"] == 20
    assert r["proto"]["trades"] == 60
    assert "pf" in r["baseline"] and "rf" in r["proto"]

def test_render_table_is_markdown(tmp_path):
    base = _csv(tmp_path, "b.csv",
                _spread(["2025-02-02 10:00", "2025-09-09 10:00"], [1.0, -0.5], n=60))
    proto = _csv(tmp_path, "p.csv",
                 _spread(["2025-03-03 10:00", "2025-08-08 10:00"], [0.5, 0.5], n=60))
    md = compare.render_table([compare.compare_one("aegis", base, proto)])
    assert "| Strategy |" in md and "aegis" in md
    assert ("|" + "---|" * 8) in md   # separator matches the 8-column header
