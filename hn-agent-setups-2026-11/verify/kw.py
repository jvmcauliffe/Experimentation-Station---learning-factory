import json,re,sys,html
t=json.load(open(sys.argv[1])); s=json.load(open(sys.argv[2]))
C={}
def w(n):
    C[n['id']]=n
    for c in n.get('children',[]): w(c)
w(t)
def clean(x): return re.sub(r'<[^>]+>',' ',html.unescape(x or ''))
K={1:r'hand.?off|handoff|summar',3:r'sub.?agent',8:r'escalat|fail|tier',9:r'.',
17:r'determin|script|fallback|resum|harden',18:r'prose|slop|writ',26:r'notif|alert|finish|ping|sound|bell',
27:r'ignore|bloat|instruction|agents\.md|claude\.md',30:r'tip|100|audit',31:r'vulcan',32:r'discrepan|clear|score|fresh',
34:r'digest|roadmap|approve|intake',35:r'builder|overfit|orchestrator|prompt',36:r'push|script|one language|approval',
39:r'overnight|morning|night|blog|report',41:r'review|loop|clean|subagent',43:r'pastiche|clean.?up|harden|isolated',
45:r'token|consum|determin|deterministic',47:r'AST|hash|rebase|cache',48:r'leftover|reset|queue|capacity|spare',
50:r'refus|fallback',51:r'quota|limit|switch|fall|reset',53:r'review page|html|visual|page',54:r'weaker|lower|effort|review',
55:r'browser|playwright|regression|explor',56:r'cron|digest|dwindl|always.on'}
for i,ins in enumerate(s['top_insights'],1):
    if i not in K: continue
    ids=ins['comment_ids']; hits=[]
    for cid in ids:
        c=C.get(int(cid)) or C.get(cid)
        if not c: continue
        x=clean(c.get('text')); m=re.search(K[i],x,re.I)
        if m:
            a=max(0,m.start()-90); hits.append((c['author'],x[a:a+260].replace('\n',' ')))
    print(f"#{i} {ins['claim'][:70]} | cited={len(ids)} kwhits={len(hits)}")
    for a,h in hits[:2]: print(f"   [{a}] ...{h}")
