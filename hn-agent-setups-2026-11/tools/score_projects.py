"""Rubric v2 for gallery projects. Priority = Impact x Fit x Confidence / Effort.
Impact/Ease/Fit come from a judgement file (one scorer: the main Claude session).
Confidence is counted: distinct commenters who mention the project (URL host/path
or its name). The person who posted their own project counts 0.5.
n>=3 -> 1.0, n>=2 -> 0.8, else 0.5.
usage: score_projects.py thread.json projects.json judgements.json out.json"""
import json, re, html, sys
from urllib.parse import urlparse
thread, proj_p, judge_p, out = sys.argv[1:5]
T = json.load(open(thread)); C = []
def walk(n):
    for c in n.get('children', []):
        if c.get('text'): C.append((c['author'], str(c['id']), html.unescape(c['text'])))
        walk(c)
walk(T)
PROMO = re.compile(r"\b(I|we)('ve| have)? (built|made|wrote|created|launched|am building|'m building)\b|\bmy (own )?(tool|project|app|harness)\b|disclos|shameless", re.I)
def needles(p):
    u = urlparse(p['url'] if '://' in p['url'] else 'https://' + p['url'])
    host = u.netloc.lower().removeprefix('www.')
    path = u.path.strip('/').lower()
    ns = []
    if host in ('github.com', 'gist.github.com', 'codeberg.org', 'gitlab.com') and path:
        ns.append(host + '/' + '/'.join(path.split('/')[:2]))
    elif host: ns.append(host + ('/' + path.split('/')[0] if path else ''))
    name = p['name'].strip().lower()
    word = re.compile(r'(?<![\w.-])' + re.escape(name) + r'(?![\w-])', re.I) if len(name) >= 4 else None
    return ns, word
def count(p):
    ns, word = needles(p); w = {}
    for a, i, t in C:
        tl = t.lower()
        if any(n in tl for n in ns) or (word and word.search(re.sub('<[^>]+>', ' ', t))):
            own = a == p.get('author') or (PROMO.search(t) and any(n in tl for n in ns))
            w[a] = max(w.get(a, 0), 0.5 if own else 1.0)
    n = sum(w.values())
    return (1.0 if n >= 3 else 0.8 if n >= 2 else 0.5), round(n, 1), len(w)
P = json.load(open(proj_p)); J = json.load(open(judge_p))
res = []
for p in P:
    j = J.get(p['url']) or J.get(p['name'])
    c, n, k = count(p)
    if not j: p.update(v2=None, v2_working='not scored', v2_authors=n); res.append(p); continue
    I, Ea, F = j[:3]; E = max(1, 6 - Ea); s = round(I * F * c / E, 1)
    p.update(impact=I, ease=Ea, fit=F, v2=s, v2_conf=c, v2_authors=n, v2_note=j[3] if len(j) > 3 else '',
             v2_working=f"{I}×{F}×{c}÷{E} = {s}")
    res.append(p)
res.sort(key=lambda x: -(x['v2'] or -1))
json.dump(res, open(out, 'w'), indent=1, ensure_ascii=False)
print('projects', len(res), 'scored', sum(x['v2'] is not None for x in res))
for x in res[:12]: print(f" {x['v2']!s:>5}  {x['v2_working']:<22} n={x['v2_authors']:<4} {x['name']}")
