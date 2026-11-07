import json,re,sys,html
t=json.load(open(sys.argv[1])); s=json.load(open(sys.argv[2]))
C={}
def w(n):
    C[n['id']]=n
    for c in n.get('children',[]): w(c)
w(t)
seen=set()
for i in map(int,sys.argv[3].split(',')):
    ins=s['top_insights'][i-1]
    print(f"\n=== #{i} CLAIM: {ins['claim']}")
    for cid in ins['comment_ids']:
        c=C.get(int(cid))
        if not c: print(' missing',cid); continue
        x=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',html.unescape(c.get('text') or '')))
        if cid in seen: print(f" [{c['author']} {cid}] (shown above)"); continue
        seen.add(cid); print(f" [{c['author']} {cid}] {x}")
