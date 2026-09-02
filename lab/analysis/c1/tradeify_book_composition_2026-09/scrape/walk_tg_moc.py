"""Day-walker over t.me/s/FinancialJuice plain listing (before=<id>): for each trading day,
estimate the message id at 15:50 ET via an id->time model learned from every fetched page,
fetch that page, extract the MOC IMBALANCE print. Appends found posts to tg_moc_raw.jsonl
(dedup by id) and writes per-day status to tg_moc_days.json. Paced 1.6 s; resumable."""
import urllib.request, urllib.parse, re, html, time, json, bisect, datetime as dt
from zoneinfo import ZoneInfo
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) research-fetch/1.0"}
BASE="https://t.me/s/FinancialJuice"
ET=ZoneInfo("America/New_York"); UTC=dt.timezone.utc
START_DAY=dt.date(2026,9,1); STOP_DAY=dt.date(2025,3,10); MIN_ID=44980
RAW="tg_moc_raw.jsonl"; DAYS="tg_moc_days.json"
MOC=re.compile(r"(?i)MOC\s*IMBALANCE")

def get(u, tries=7):
    for k in range(tries):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60); return r.read().decode("utf-8","replace")
        except urllib.error.HTTPError as e:
            w=2.0*(2**k); print(f"  HTTP {e.code}; sleep {w:.0f}s",flush=True); time.sleep(w)
        except Exception as e:
            w=2.0*(2**k); print(f"  ERR {str(e)[:50]}; sleep {w:.0f}s",flush=True); time.sleep(w)
    raise RuntimeError("gave up "+u)
def parse(b):
    out=[]
    for m in re.finditer(r'<div class="tgme_widget_message_wrap.*?(?=<div class="tgme_widget_message_wrap|</section>)', b, re.S):
        blk=m.group(0); pid=re.search(r'data-post="FinancialJuice/(\d+)"',blk); d=re.search(r'<time[^>]+datetime="([^"]+)"',blk)
        txt=re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',blk,re.S)
        t=html.unescape(re.sub(r"<br\s*/?>","\n",txt.group(1))) if txt else ""; t=re.sub(r"<[^>]+>","",t).strip()
        if pid and d: out.append({"id":int(pid.group(1)),"dt":d.group(1),"text":t})
    return out
def ts(s): return dt.datetime.fromisoformat(s).timestamp()

known={}   # id -> epoch
def learn(msgs):
    for m in msgs: known[m["id"]]=ts(m["dt"])
def estimate(target):
    ids=sorted(known); tsl=[known[i] for i in ids]
    # find bracket by time
    order=sorted(range(len(ids)), key=lambda k: tsl[k]); t_sorted=[tsl[k] for k in order]; i_sorted=[ids[k] for k in order]
    j=bisect.bisect_left(t_sorted,target)
    if 0<j<len(t_sorted):
        t0,t1=t_sorted[j-1],t_sorted[j]; i0,i1=i_sorted[j-1],i_sorted[j]
        if t1>t0: return int(round(i0+(i1-i0)*(target-t0)/(t1-t0)))
        return i0
    # extrapolate with the rate over the nearest ~3 days of known points
    if j==0: i_ref,t_ref=i_sorted[0],t_sorted[0]
    else: i_ref,t_ref=i_sorted[-1],t_sorted[-1]
    # rate from two known points at least 2 days apart, nearest to the reference
    k=0 if j==0 else len(t_sorted)-1; kk=k
    while 0<=kk<len(t_sorted) and abs(t_sorted[kk]-t_ref)<2*86400: kk += (1 if j==0 else -1)
    if 0<=kk<len(t_sorted) and t_sorted[kk]!=t_ref: rate=(i_sorted[kk]-i_ref)/(t_sorted[kk]-t_ref)
    else: rate=150/86400.0
    return int(round(i_ref+rate*(target-t_ref)))

def main():
    seen=set(); days={}
    try:
        for line in open(RAW,encoding="utf-8"):
            r=json.loads(line); seen.add(r["id"]); known[r["id"]]=ts(r["dt"])
    except FileNotFoundError: pass
    try: days=json.load(open(DAYS))
    except FileNotFoundError: pass
    # seed anchors from earlier probes (id, iso time)
    for i,s in ((126930,"2026-08-04T18:25:30+00:00"),(126949,"2026-08-04T20:04:57+00:00"),(99980,"2026-02-10T14:59:00+00:00"),
                (99999,"2026-02-10T17:20:00+00:00"),(59980,"2025-05-21T12:59:00+00:00"),(59999,"2025-05-21T15:05:00+00:00"),
                (44980,"2025-03-13T21:44:00+00:00"),(44999,"2025-03-13T21:54:00+00:00"),(131347,"2026-09-01T19:00:00+00:00")):
        known.setdefault(i,ts(s))
    fout=open(RAW,"a",encoding="utf-8")
    d=START_DAY; n_fetch=0
    while d>=STOP_DAY:
        if d.weekday()>=5 or d.isoformat() in days:
            d-=dt.timedelta(1); continue
        target=dt.datetime(d.year,d.month,d.day,15,50,tzinfo=ET).astimezone(UTC).timestamp()
        est=estimate(target); found=None; tries=0; direction=0; status="missing"
        while tries<6:
            before=est+10
            if before<=MIN_ID+20: status="before-channel-start"; break
            msgs=parse(get(BASE+"?"+urllib.parse.urlencode({"before":str(before)}))); n_fetch+=1; time.sleep(1.6); tries+=1
            if not msgs: status="empty-page"; break
            learn(msgs)
            hits=[m for m in msgs if MOC.search(m["text"]) and m["dt"][:10]==d.isoformat()]
            for m in hits:
                if m["id"] not in seen:
                    seen.add(m["id"]); fout.write(json.dumps(m,ensure_ascii=False)+"\n"); fout.flush()
            if hits:
                found=hits[-1]; status="found"; break
            tmin=min(ts(m["dt"]) for m in msgs); tmax=max(ts(m["dt"]) for m in msgs)
            if tmax < target-120:      # page ends before the print time -> move later
                if direction==-1: status="spanned-no-print"; break
                direction=1; est=max(m["id"] for m in msgs)+12
            elif tmin > target+120:    # page starts after the print time -> move earlier
                if direction==1: status="spanned-no-print"; break
                direction=-1; est=min(m["id"] for m in msgs)-12
            else:
                # page spans the target time with no MOC post: look one page later, then earlier
                if direction==0:
                    direction=2; est=max(m["id"] for m in msgs)+12
                elif direction==2:
                    direction=3; est=min(m["id"] for m in msgs)-32
                else:
                    status="spanned-no-print"; break
        days[d.isoformat()]={"status":status,"id":found["id"] if found else None,"tries":tries,"text":found["text"][:80] if found else None}
        json.dump(days,open(DAYS,"w"),indent=0)
        print(f"{d} {status:18} tries {tries} fetches {n_fetch} {found['dt'][11:16] if found else ''} {found['text'][:50].replace(chr(10),' ') if found else ''}",flush=True)
        if status=="before-channel-start": break
        d-=dt.timedelta(1)
    fnd=sum(1 for v in days.values() if v["status"]=="found")
    print(f"done: {fnd} found / {len(days)} trading days examined, {n_fetch} fetches",flush=True)
if __name__=="__main__":
    main()
