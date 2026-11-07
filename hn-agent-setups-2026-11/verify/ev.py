import json,re,html,sys
T=json.load(open(sys.argv[1]));C={}
def w(n):
    if n.get('id'):C[str(n['id'])]=(n.get('author'),re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',n.get('text') or ''))).strip())
    for c in n.get('children',[]):w(c)
w(T)
d=json.load(open(sys.argv[2]))['top_insights']
lo,hi=int(sys.argv[3]),int(sys.argv[4])
if lo==0:
    bad=0
    for i,x in enumerate(d,1):
        for cid,au in zip(x['comment_ids'],x['authors']):
            if cid not in C: print('MISSING',i,cid); bad+=1
            elif C[cid][0]!=au: print('AUTHOR',i,cid,au,'vs',C[cid][0]); bad+=1
    print('id/author problems:',bad,'of',sum(len(x['comment_ids']) for x in d),'citations')
else:
    for i,x in enumerate(d,1):
        if lo<=i<=hi:
            print(f'\n#{i} CLAIM: {x["claim"]}')
            for cid in x['comment_ids'][:3]:
                a,t=C.get(cid,('?','?')); print(f'  [{a} {cid}] {t[:330]}')
