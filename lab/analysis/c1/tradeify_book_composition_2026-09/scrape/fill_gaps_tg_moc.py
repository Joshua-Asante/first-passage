"""Second pass: group consecutive not-found trading days into brackets between found prints
(ids lo..hi), scan each bracket once page by page, and attribute every MOC IMBALANCE message
to its UTC date. Days still empty afterwards have no text print in the channel. Appends to
tg_moc_raw.jsonl; updates tg_moc_days.json. Paced 1.3 s."""
import urllib.request, urllib.parse, re, html, time, json, datetime as dt, sys
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) research-fetch/1.0"}
BASE="https://t.me/s/FinancialJuice"; RAW="tg_moc_raw.jsonl"; DAYS="tg_moc_days.json"; MIN_ID=44980
MOC=re.compile(r"(?i)MOC\s*IMBALANCE")
def get(u, tries=7):
    for k in range(tries):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60); return r.read().decode("utf-8","replace")
        except Exception as e:
            w=2.0*(2**k); print(f"  ERR {str(e)[:50]}; sleep {w:.0f}s",flush=True); time.sleep(w)
    raise RuntimeError("gave up "+u)
def parse(b):
    out=[]
    for m in re.finditer(r'<div class="tgme_widget_message_wrap.*?(?=<div class="tgme_widget_message_wrap|</section>)', b, re.S):
        blk=m.group(0); pid=re.search(r'data-post="FinancialJuice/(\d+)"',blk); d=re.search(r'<time[^>]+datetime="([^"]+)"',blk)
        txt=re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',blk,re.S)
        t=html.unescape(re.sub(r"<br\s*/?>","\n",txt.group(1))) if txt else ""; t=re.sub(r"<[^>]+>","",t).strip()
        if pid and d: out.append({"id":int(pid.group(1)),"dt":d.group(1),"text":t,"photo":"tgme_widget_message_photo" in blk})
    return out
def main():
    b0=int(sys.argv[1]) if len(sys.argv)>1 else 0; b1=int(sys.argv[2]) if len(sys.argv)>2 else 10**6; suffix=sys.argv[3] if len(sys.argv)>3 else ""
    days=json.load(open(DAYS))
    seen=set(json.loads(l)["id"] for l in open(RAW,encoding="utf-8") if l.strip())
    fout=open(RAW+suffix,"a",encoding="utf-8")
    keys=sorted(days)                       # ISO dates ascending
    # build brackets: runs of not-found days between found anchors
    brackets=[]; run=[]
    for k in keys:
        if days[k]["status"]=="found":
            if run: brackets.append(run); run=[]
        elif days[k]["status"]!="before-channel-start":
            run.append(k)
    if run: brackets.append(run)
    brackets=brackets[b0:b1]
    print(f"{sum(len(b) for b in brackets)} days in {len(brackets)} brackets [{b0}:{b1}] -> suffix {suffix!r}",flush=True)
    n_fetch=0
    for run in brackets:
        prev=[k for k in keys if k<run[0] and days[k]["status"]=="found"]; nxt=[k for k in keys if k>run[-1] and days[k]["status"]=="found"]
        lo=days[prev[-1]]["id"] if prev else MIN_ID
        hi=days[nxt[0]]["id"] if nxt else 131400
        hits={k:[] for k in run}; before=hi; pages=0; photo_only={k:0 for k in run}
        while before>lo and pages<400:
            msgs=parse(get(BASE+"?"+urllib.parse.urlencode({"before":str(before)}))); n_fetch+=1; pages+=1; time.sleep(1.3)
            if not msgs: break
            for m in msgs:
                d=m["dt"][:10]
                if d in hits:
                    if MOC.search(m["text"]): hits[d].append(m)
                    elif m["photo"] and not m["text"]: photo_only[d]+=1
            before=min(m["id"] for m in msgs)
            if min(m["dt"][:10] for m in msgs) < run[0]: break
        for k in run:
            hs=sorted(hits[k],key=lambda m:m["id"])
            for m in hs:
                if m["id"] not in seen:
                    seen.add(m["id"]); fout.write(json.dumps({x:m[x] for x in ("id","dt","text")},ensure_ascii=False)+"\n"); fout.flush()
            if hs: days[k]={"status":"found","id":hs[-1]["id"],"tries":days[k].get("tries",0),"text":hs[-1]["text"][:80],"pass":2}
            else: days[k].update({"status":"no-print-in-bracket","bracket":[lo,hi],"photo_only_msgs_that_day":photo_only[k]})
        json.dump(days,open(DAYS+suffix,"w"),indent=0)
        got=sum(1 for k in run if days[k]["status"]=="found")
        print(f"bracket {run[0]}..{run[-1]} ({len(run)} days) ids {lo}..{hi}: pages {pages}, found {got}, fetches {n_fetch}",flush=True)
    c={}
    for v in days.values(): c[v["status"]]=c.get(v["status"],0)+1
    print("done:",c,flush=True)
if __name__=="__main__":
    main()
