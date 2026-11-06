"""Rubric v2: Priority = Impact x Fit x Confidence / Effort.
Effort = 6 - Ease. Confidence is counted from the thread, never judged:
distinct authors of the cited comments; a self-promoting comment counts 0.5.
n>=3 -> 1.0, n>=2 -> 0.8, n>0 -> 0.5. No cited ids -> falls back to the
old Evidence score (4-5 -> 1.0, 3 -> 0.8, else 0.5) and is flagged 'proxy'.
Gate: needs_john_decision or Fit<=1 -> not ranked, listed for John."""
import json, re, html, sys
thread, synth_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
T = json.load(open(thread)); C = {}
def walk(n):
    for c in n.get('children', []):
        if c.get('text'): C[str(c['id'])] = (c['author'], re.sub('<[^>]+>', ' ', html.unescape(c['text'])))
        walk(c)
walk(T)
PROMO = re.compile(r"\b(I|we)('ve| have)? (built|made|wrote|created|launched|am building|'m building)\b|\bmy (own )?(tool|project|app|harness)\b|disclos|shameless", re.I)
def confidence(ids, ev):
    ids = [str(i) for i in (ids or []) if str(i) in C]
    if not ids:
        return ({5: 1.0, 4: 1.0, 3: 0.8}.get(ev, 0.5), 0, 'proxy')
    w = {}
    for i in ids:
        a, t = C[i]; promo = bool(PROMO.search(t)) and 'http' in t
        w[a] = max(w.get(a, 0), 0.5 if promo else 1.0)
    n = sum(w.values())
    return (1.0 if n >= 3 else 0.8 if n >= 2 else 0.5, round(n, 1), 'counted')
def score(x, ids_key):
    I, F, ev = x['impact'], x['fit'], x['evidence']; E = max(1, 6 - x['ease'])
    c, n, how = confidence(x.get(ids_key), ev)
    gated = bool(x.get('needs_john_decision')) or F <= 1
    p = round(I * F * c / E, 1)
    x['v1'] = f"{I}+{x['ease']}+{ev}+{F} = {I + x['ease'] + ev + F}"
    x['v2'] = None if gated else p
    x['v2_working'] = f"{I}×{F}×{c}÷{E} = {p}" + ("" if how == 'counted' else " (conf. proxy)")
    x['v2_authors'] = n; x['v2_conf_source'] = how; x['gated'] = gated
    return x
S = json.load(open(synth_path))
for k, ids in (('categories', None), ('top_insights', 'comment_ids'), ('recommendations', 'source_ids')):
    items = [score(x, ids) for x in S.get(k, [])]
    S[k] = sorted(items, key=lambda x: (x['v2'] is None, -(x['v2'] or 0)))
json.dump(S, open(out, 'w'), indent=1, ensure_ascii=False)
for k in ('categories', 'top_insights', 'recommendations'):
    print(k, len(S[k]), 'gated', sum(x['gated'] for x in S[k]), 'proxy', sum(x['v2_conf_source'] == 'proxy' for x in S[k]))
