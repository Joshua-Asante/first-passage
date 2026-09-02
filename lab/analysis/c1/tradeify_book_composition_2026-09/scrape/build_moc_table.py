"""tg_moc_raw.jsonl -> per-day MOC imbalance table (CSV) + Pine array literals spliced into
MES_MOC_fade_v0_1.pine's SIGN TABLE section.

Formats handled (FinancialJuice Telegram/X mirror):
  A  "❗ MOC IMBALANCE\nS&P 500: -4479.4 MLN\nNASDAQ 100: ... \nDOW 30: ...\nMAG 7: ... $MACRO|FJ"
     signed MLN figures (+ buy-side, - sell-side)
  B  "🔴/🟢 MOC IMBALANCE S&P 500: 2787.9 MLN NASDAQ 100: ..."  unsigned; sign inferred from the
     leading emoji (🔴 = sell-side, 🟢 = buy-side) -> flagged sign_source=emoji
  C  "MOC IMBALANCE 2.1 BLN SELL-SIDE." / "MOC imbalance 4 bln buy-side" single figure, words carry the
     sign -> sp500 only, flagged single_figure
  Posts containing "Early" are kept but flagged early=True and never used as the day's final print.
Per day: the LAST non-early post before 20:30 UTC (or the last early one if nothing else) is final.
"""
import csv, json, re, sys, os
from collections import defaultdict

RAW = "tg_moc_raw.jsonl"
PINE = r"C:\Users\joshu\Downloads\MES_MOC_fade_v0_1.pine"
OUT_CSV = "moc_imbalance_daily.csv"

num = r"([+-]?\d[\d,]*\.?\d*)\s*(MLN|BLN|M|B|MILLION|BILLION)?"

def _et_hhmm(iso: str) -> str:
    """UTC ISO timestamp -> 'HH:MM' in America/New_York, so a wall-clock cutoff means the
    same thing in EDT and EST."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    return (datetime.fromisoformat(iso).astimezone(ZoneInfo("America/New_York"))
            .strftime("%H:%M"))


def to_mln(val, unit):
    v = float(val.replace(",", ""))
    if unit and unit.upper().startswith("B"):
        v *= 1000.0
    return v

def parse_post(text):
    t = text.replace("\u2009", " ")
    rec = {"format": None, "sp500": None, "ndx": None, "dow": None, "mag7": None,
           "sign_source": "explicit", "early": bool(re.search(r"(?i)\bearly\b", t))}
    m_sp = re.search(r"(?i)S&P\s*500\s*:\s*" + num, t)
    if m_sp:
        rec["format"] = "A/B"
        rec["sp500"] = to_mln(m_sp.group(1), m_sp.group(2))
        for key, pat in (("ndx", r"(?i)NASDAQ\s*100\s*:\s*" + num), ("dow", r"(?i)DOW\s*30\s*:\s*" + num),
                         ("mag7", r"(?i)MAG(?:NIFICENT)?\s*7\s*:\s*" + num)):
            m = re.search(pat, t)
            if m:
                rec[key] = to_mln(m.group(1), m.group(2))
        # Sign rule for the multi-index format: any figure in the post carrying '-' or '+' means the
        # post is explicitly signed and bare numbers are positive (buy-side) -- the channel prints
        # negatives with '-' and positives bare. Only a post with NO sign anywhere falls back to the
        # emoji/word inference (the old X-style unsigned format).
        allnums = re.findall(r"(?i)(?:S&P\s*500|NASDAQ\s*100|DOW\s*30|MAG(?:NIFICENT)?\s*7)\s*:\s*([+-]?)\d", t)
        signed = any(sg in ("+", "-") for sg in allnums)
        if not signed:
            if "\U0001F534" in t or re.search(r"(?i)sell[- ]?side", t):   # red circle
                rec["sign_source"] = "emoji/word-sell"
                for k in ("sp500", "ndx", "dow", "mag7"):
                    if rec[k] is not None:
                        rec[k] = -abs(rec[k])
            elif "\U0001F7E2" in t or re.search(r"(?i)buy[- ]?side", t):  # green circle
                rec["sign_source"] = "emoji/word-buy"
            else:
                # multi-index format with no minus anywhere: every figure is buy-side (the channel
                # never writes "+" in this format; negatives always carry "-")
                rec["sign_source"] = "bare-positive"
        return rec
    m_c = re.search(r"(?i)MOC\s*IMBALANCE\s*(?:OF\s*)?" + num + r"\s*(?:TO\s+THE\s+)?(BUY|SELL)", t)
    if m_c:
        rec["format"] = "C"
        v = to_mln(m_c.group(1), m_c.group(2))
        rec["sp500"] = -abs(v) if m_c.group(3).upper() == "SELL" else abs(v)
        rec["sign_source"] = "word"
        return rec
    rec["format"] = "UNPARSED"
    return rec

def main():
    rows = [json.loads(l) for l in open(RAW, encoding="utf-8") if l.strip()]
    by_day = defaultdict(list)
    unparsed = []
    for r in rows:
        p = parse_post(r["text"])
        p.update({"id": r["id"], "dt": r["dt"], "date": r["dt"][:10], "text": r["text"].replace("\n", " | ")[:200]})
        if p["format"] == "UNPARSED":
            unparsed.append(p)
            continue
        by_day[p["date"]].append(p)
    final = []
    for d in sorted(by_day):
        posts = sorted(by_day[d], key=lambda x: x["id"])
        # Cutoff must be applied in EASTERN time. The ~15:50 ET print lands at 19:50 UTC in
        # EDT but 20:50 UTC in EST, so the old fixed "<= 20:30 UTC" test excluded every
        # winter print from `cands`. It happened to be harmless on this dataset -- with
        # `cands` empty the `(cands or posts)` fallback picks the right post, verified on all
        # 72 EST days and all 3 days carrying two non-early posts, 0 changed -- but a winter
        # day with an earlier non-early post would have silently selected that earlier post.
        # Latent, not live. Fixed 2026-09-02 (Codex review, PR #260, second round).
        cands = [p for p in posts
                 if not p["early"] and _et_hhmm(p["dt"]) <= "17:00"]
        pick = (cands or posts)[-1]
        pick = dict(pick)
        pick["n_posts_that_day"] = len(posts)
        final.append(pick)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "dt", "id", "format", "sign_source", "early", "n_posts_that_day",
                                           "sp500_mln", "ndx_mln", "dow_mln", "mag7_mln", "text"])
        w.writeheader()
        for p in final:
            w.writerow({"date": p["date"], "dt": p["dt"], "id": p["id"], "format": p["format"], "sign_source": p["sign_source"],
                        "early": p["early"], "n_posts_that_day": p["n_posts_that_day"],
                        "sp500_mln": p["sp500"], "ndx_mln": p["ndx"], "dow_mln": p["dow"], "mag7_mln": p["mag7"], "text": p["text"]})
    # summary
    n = len(final); dates = [p["date"] for p in final]
    src = defaultdict(int)
    for p in final: src[p["sign_source"]] += 1
    print(f"posts {len(rows)} | days with a final print {n} | span {dates[0] if dates else None} .. {dates[-1] if dates else None}")
    print("sign sources:", dict(src), "| unparsed posts:", len(unparsed))
    for u in unparsed[:5]: print("  UNPARSED:", u["dt"], u["text"][:120])
    import datetime as _dt
    if dates:
        d0 = _dt.date.fromisoformat(dates[0]); d1 = _dt.date.fromisoformat(dates[-1])
        bdays = sum(1 for i in range((d1 - d0).days + 1) if (d0 + _dt.timedelta(i)).weekday() < 5)
        print(f"coverage: {n} prints over {bdays} weekdays in span = {n / bdays:.1%} (US holidays are ~4% of weekdays)")
    # Pine splice: only rows with a usable S&P sign
    # ONLY verified-sign sessions reach the Pine. The "bare-positive" inference was
    # FALSIFIED 2026-09-02: the X original for 2025-04-30 carries a red (sell-side)
    # marker with the identical four figures this table had stored as buy-side, and
    # the Telegram mirror renders that colour marker as a plain exclamation mark, so
    # the sign is unrecoverable for those posts. They are kept in the CSV, flagged,
    # and excluded from the tradeable table.
    usable = [p for p in final if p["sp500"] is not None and p["sign_source"] == "explicit"]
    def chunks(xs, k=80):
        for i in range(0, len(xs), k):
            yield xs[i:i + k]
    lines = ["var int[] tblDate = array.new<int>()", "var float[] tblImb = array.new<float>()",
             "// Generated " + _dt.date.today().isoformat() + f" from FinancialJuice's Telegram mirror: {len(usable)} sessions, "
             + f"{usable[0]['date']}..{usable[-1]['date']}; S&P 500 MOC imbalance in $bn (+ buy-side). "
             + "VERIFIED-SIGN SESSIONS ONLY: posts whose sign lived in a colour marker the Telegram mirror drops are excluded.",
             "if barstate.isfirst"]
    for ch in chunks(usable):
        ds = ", ".join(p["date"].replace("-", "") for p in ch)
        vs = ", ".join(f"{p['sp500'] / 1000.0:.4f}" for p in ch)
        lines.append("    array.concat(tblDate, array.from(" + ds + "))")
        lines.append("    array.concat(tblImb, array.from(" + vs + "))")
    block = "\n".join(lines) + "\n"
    src_pine = open(PINE, encoding="utf-8").read()
    start = src_pine.index("var int[] tblDate")
    end = src_pine.index("var signMap = map.new<int, float>()")
    new_pine = src_pine[:start] + block + "\n" + src_pine[end:]
    open(PINE, "w", encoding="utf-8").write(new_pine)
    print(f"spliced {len(usable)} rows into {PINE} ({len(new_pine):,} chars)")

if __name__ == "__main__":
    main()
