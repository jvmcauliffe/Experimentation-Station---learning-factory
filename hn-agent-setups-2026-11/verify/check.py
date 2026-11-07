import json,re,html,sys
G='/home/user/Experimentation-Station---learning-factory/hn-agent-setups-2026-11/GOLDMINE.md'
T=json.load(open(sys.argv[1]))
C={}
def walk(n):
    if n.get('id'): C[n['id']]=(n.get('author'),n.get('text') or n.get('title') or '')
    for c in n.get('children',[]): walk(c)
walk(T)
def norm(s):
    s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s)
    s=s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('–','-').replace('—','-')
    s=re.sub(r'[*_`]','',s)
    return re.sub(r'\s+',' ',s).lower().strip()
N={i:norm(t) for i,(a,t) in C.items()}
ALL=' || '.join(N.values())
lines=open(G).read().split('\n')
ids=set(); missing=set(); badauth=[]; qtot=0; qline=0; qany=0; qfail=[]
for ln,l in enumerate(lines,1):
    lid=[int(x) for x in re.findall(r'item\?id=(\d+)',l)]+[int(x) for x in re.findall(r'#(5\d{7})',l)]
    lid=list(dict.fromkeys(lid)); ids.update(lid)
    for i in lid:
        if i not in C: missing.add(i)
    for m in re.finditer(r'(?<![\w\[])@?([A-Za-z0-9_\-]{3,})\s+\[?#(5\d{7})',l):
        a,i=m.group(1),int(m.group(2))
        if i in C and C[i][0] and C[i][0].lower()!=a.lower(): badauth.append((ln,a,i,C[i][0]))
    nl=norm(l)
    for q in re.findall(r'[“"]([^"“”]{25,}?)[”"]',l):
        qn=norm(q); segs=[s.strip(' .,') for s in re.split(r'…|\.\.\.',qn) if len(s.strip(' .,'))>=15]
        if not segs: continue
        qtot+=1
        if lid and all(any(s in N.get(i,'') for i in lid) for s in segs): qline+=1
        elif all(s in ALL for s in segs): qany+=1
        else: qfail.append((ln,q[:110]))
print('comments in thread:',len(C))
print('distinct ids cited:',len(ids),' not in thread:',sorted(missing))
print('author mismatches:',len(badauth)); [print(' ',b) for b in badauth[:15]]
print('quotes checked:',qtot,' found in a cited comment:',qline,' found elsewhere in thread only:',qany,' not found:',len(qfail))
for f in qfail[:25]: print(' L%d %s'%f)
