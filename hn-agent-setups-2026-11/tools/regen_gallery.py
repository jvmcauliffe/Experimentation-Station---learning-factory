import json,re,sys
page=open('agent-setups.html').read()
m=re.search(r'^const P=(\[.*\]);?$',page,re.M)
old={p[0]:p for p in json.loads(m.group(1))}
print('old',len(old),'kilo',old.get('kilo'))
new=json.load(open('projects_v2.json'))
out=[]
for p in new:
    o=old.get(p['key'])
    a=p['v2_authors']; a=int(a) if a==int(a) else a
    if o: cat,stars,what=o[3],o[4],o[5]
    else: cat,stars,what=old['kilo'][3],old['kilo'][4],p['what']
    out.append([p['key'],p['name'],p['url'],cat,stars,what,p['v2'],p['v2_working'],p['v2_note'],a])
print('new',len(out),[o for o in out if o[0] in('tuicr','agent-vault','workspace')])
page=page[:m.start()]+'const P='+json.dumps(out,ensure_ascii=False)+';'+page[m.end():] if m.group(0).endswith(';') else page[:m.start()]+'const P='+json.dumps(out,ensure_ascii=False)+page[m.end():]
page=page.replace('111 linked projects','114 linked projects').replace('All 111 projects','All 114 projects')
print('111 left',page.count('111'))
open('out/page.html','w').write(page)
