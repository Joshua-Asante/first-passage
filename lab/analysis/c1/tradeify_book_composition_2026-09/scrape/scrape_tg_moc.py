"""Enumerate FinancialJuice's public Telegram channel (t.me/s/FinancialJuice) for
"MOC IMBALANCE" posts via the preview's search + before= cursor. Polite: 1.6 s
between requests, exponential backoff on errors. Output: tg_moc_raw.jsonl
(one line per matched message, all formats) + progress log."""
import urllib.request, urllib.parse, re, html, time, json, sys
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) research-fetch/1.0"}
BASE="https://t.me/s/FinancialJuice"
STOP_BEFORE="2022-01-01"
def get(u, tries=6):
    delay=1.6
    for k in range(tries):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60)
            return r.read().decode("utf-8","replace")
        except urllib.error.HTTPError as e:
            if e.code in (429,503,500,502):
                wait=delay*(2**k); print(f"  HTTP {e.code} -> sleep {wait:.0f}s", flush=True); time.sleep(wait); continue
            raise
        except Exception as e:
            wait=delay*(2**k); print(f"  ERR {str(e)[:60]} -> sleep {wait:.0f}s", flush=True); time.sleep(wait)
    raise RuntimeError("gave up: "+u)
def parse(b):
    out=[]
    for m in re.finditer(r'<div class="tgme_widget_message_wrap.*?(?=<div class="tgme_widget_message_wrap|</section>)', b, re.S):
        blk=m.group(0)
        pid=re.search(r'data-post="FinancialJuice/(\d+)"',blk); dt=re.search(r'<time[^>]+datetime="([^"]+)"',blk)
        txt=re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',blk,re.S)
        t=html.unescape(re.sub(r"<br\s*/?>","\n",txt.group(1))) if txt else ""
        t=re.sub(r"<[^>]+>","",t).strip()
        if pid and dt:
            out.append({"id":int(pid.group(1)),"dt":dt.group(1),"text":t})
    return out
def main():
    seen=set(); n_pages=0; cursor=None; empty_streak=0
    fout=open("tg_moc_raw.jsonl","a",encoding="utf-8")
    # resume support
    try:
        for line in open("tg_moc_raw.jsonl",encoding="utf-8"):
            r=json.loads(line); seen.add(r["id"]); cursor=min(cursor or r["id"], r["id"])
        if seen: print(f"resuming below id {cursor} with {len(seen)} rows", flush=True)
    except FileNotFoundError: pass
    oldest_dt="9999"
    while True:
        params={"q":"MOC IMBALANCE"}
        if cursor: params["before"]=str(cursor)
        u=BASE+"?"+urllib.parse.urlencode(params)
        b=get(u); n_pages+=1
        msgs=parse(b)
        new=[m for m in msgs if m["id"] not in seen and re.search(r"(?i)MOC\s*IMBALANCE", m["text"])]
        for m in sorted(new,key=lambda x:-x["id"]):
            seen.add(m["id"]); fout.write(json.dumps(m,ensure_ascii=False)+"\n"); oldest_dt=min(oldest_dt,m["dt"])
        fout.flush()
        ids=[m["id"] for m in msgs]
        if msgs:
            empty_streak=0
            cursor=min(ids)
            print(f"page {n_pages}: {len(msgs)} msgs ({len(new)} new) ids {min(ids)}..{max(ids)} oldest {oldest_dt[:10]} total {len(seen)}", flush=True)
        else:
            empty_streak+=1
            # search window returned nothing: step the cursor down ~2 trading days of channel traffic
            cursor=(cursor or 131400)-400
            print(f"page {n_pages}: empty; cursor -> {cursor} (streak {empty_streak})", flush=True)
            if empty_streak>=25 or cursor<=1:
                print("stopping: exhausted", flush=True); break
        if oldest_dt[:10] < STOP_BEFORE:
            print("stopping: reached", STOP_BEFORE, flush=True); break
        time.sleep(1.6)
    print(f"done: {len(seen)} MOC rows, {n_pages} pages, oldest {oldest_dt}", flush=True)
if __name__=="__main__":
    main()
