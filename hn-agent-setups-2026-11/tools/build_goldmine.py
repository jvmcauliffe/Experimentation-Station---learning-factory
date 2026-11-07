"""Build GOLDMINE.md and the page's v2 sections from the scored synthesis.
Usage: build_goldmine.py scored_synth.json crit.json|- reddit-check.md routing-table.md projects_v2.json out_dir"""
import json, re, html, sys, os
sp, cp, rp, tp, pp, out = sys.argv[1:7]
S = json.load(open(sp)); C = json.load(open(cp)) if cp != '-' else {}
reddit, routing = open(rp).read(), open(tp).read()
P = json.load(open(pp))
HN = 'https://news.ycombinator.com/item?id='
e = lambda s: html.escape(str(s or ''), quote=True)

def md_inline(s):
    s = e(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*([^*]+)\*(?!\w)', r'<i>\1</i>', s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r'#(5\d{7})\b', lambda m: f'<a href="{HN}{m[1]}" target="_blank" rel="noopener">#{m[1]}</a>', s)
    return s

def md_html(md, shift=1):
    o, lines, i = [], md.split('\n'), 0
    while i < len(lines):
        l = lines[i]
        if not l.strip(): i += 1; continue
        m = re.match(r'(#+) (.*)', l)
        if m:
            n = min(6, len(m[1]) + shift); o.append(f'<h{n}>{md_inline(m[2])}</h{n}>'); i += 1; continue
        if l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            rows = [r for r in rows if not all(re.fullmatch(r':?-+:?', c) for c in r)]
            h = ''.join(f'<th>{md_inline(c)}</th>' for c in rows[0])
            b = ''.join('<tr>' + ''.join(f'<td>{md_inline(c)}</td>' for c in r) + '</tr>' for r in rows[1:])
            o.append(f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'); continue
        if re.match(r'(\d+\.|[-*]) ', l):
            tag = 'ol' if l[0].isdigit() else 'ul'; items = []
            while i < len(lines) and re.match(r'\s*(\d+\.|[-*]) ', lines[i]):
                items.append(re.sub(r'\s*(\d+\.|[-*]) ', '', lines[i], count=1)); i += 1
            o.append(f'<{tag}>' + ''.join(f'<li>{md_inline(x)}</li>' for x in items) + f'</{tag}>'); continue
        if l.startswith('>'):
            q = []
            while i < len(lines) and lines[i].startswith('>'):
                q.append(lines[i].lstrip('> ')); i += 1
            o.append(f'<blockquote>{md_inline(" ".join(q))}</blockquote>'); continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r'(#+ |\||>|(\d+\.|[-*]) )', lines[i]):
            para.append(lines[i]); i += 1
        o.append(f'<p>{md_inline(" ".join(para))}</p>')
    return '\n'.join(o)

def ids_md(ids): return ', '.join(f'[#{i}]({HN}{i})' for i in (ids or [])[:6])
def txt(x):
    if isinstance(x, str): return x
    if isinstance(x, dict) and 'topic' in x:
        return f"**{x['topic']}** Yes: {x.get('side_a','')} No: {x.get('side_b','')} Verdict for you: {x.get('verdict','')}"
    if isinstance(x, dict) and 'quote' in x:
        return f"\u201c{x['quote']}\u201d \u2014 {x.get('author','')} #{x.get('comment_id','')}"
    if isinstance(x, dict): return ' — '.join(str(v) for v in x.values() if isinstance(v, (str, int, float)))
    return str(x)

EXTRA = [json.load(open(a))['recommendations'][0] for a in sys.argv[7:]]
for x in EXTRA: x.setdefault('what', ''); x.setdefault('how_in_harness', 'See the routing table section below.')
S['recommendations'] = sorted(S.get('recommendations', []) + EXTRA, key=lambda x: (x['v2'] is None, -(x['v2'] or 0)))
cats = S.get('categories', []); ins = S.get('top_insights', []); recs = S.get('recommendations', [])
ranked = lambda xs: [x for x in xs if not x['gated']]
gated = [('Camp', x.get('name')) for x in cats if x['gated']] + [('Insight', x.get('claim')) for x in ins if x['gated']] + \
        [('Change', x.get('title')) for x in recs if x['gated']]
gated_full = [x for x in recs + ins + cats if x['gated']]
topP = sorted(P, key=lambda p: -p['v2'])[:15]

def row(cells): return '| ' + ' | '.join(str(c).replace('|', '/').replace('\n', ' ') for c in cells) + ' |'
def tbl(head, rows): return '\n'.join([row(head), row(['---'] * len(head))] + [row(r) for r in rows])

M = ['# Gold mine: Ask HN "What\'s your current AI agentic setup?"', '',
     f'Source: [{HN}50366117]({HN}50366117), 645 comments, mined 6 Nov 2026 by 8 parallel readers, one synthesis and one critic.', '',
     '## How v2 is scored', '',
     'Priority = Impact × Fit × Confidence ÷ Effort. Effort = 6 − Ease. Impact, Ease and Fit are 1–5 judgements. '
     'Confidence is counted, not judged: distinct commenters behind the cited comments (a self-promoting comment counts 0.5); '
     '3 or more → 1.0, 2 → 0.8, 1 → 0.5. With no cited ids it falls back to the old Evidence score and says "proxy". '
     'Anything that needs John\'s decision, or has Fit ≤ 1, is not ranked; it goes on the John decides list. v1 is the old sum out of 20, kept for comparison.', '',
     '## Changes to adopt, ranked by v2', '',
     tbl(['#', 'Change', 'v2', 'Working', 'v1', 'Commenters'],
         [[k + 1, r['title'], r['v2'], r['v2_working'], r['v1'], r['v2_authors']] for k, r in enumerate(ranked(recs))]), '']
for k, r in enumerate(ranked(recs)):
    M += [f'### {k + 1}. {r["title"]} — v2 {r["v2"]}', '', r.get('what', ''), '', f'**In your harness:** {r.get("how_in_harness", "")}', '',
          f'Sources: {ids_md(r.get("source_ids"))}', '']
M += ['## John decides (not ranked)', '', 'These change policy, providers or spend, or fit poorly, so they are listed for your decision instead of ranked.', '',
      tbl(['Kind', 'Item', 'Would score', 'Working'],
          [[k, n, x['v2_working'].split('= ')[-1], x['v2_working']] for (k, n), x in zip(gated, [x for x in cats if x['gated']] + [x for x in ins if x['gated']] + [x for x in recs if x['gated']])]), '',
      '## Camps, ranked by v2', '',
      tbl(['#', 'Camp', 'Verdict', 'v2', 'Working', 'v1'],
          [[k + 1, c['name'], c.get('verdict', ''), c['v2'] if c['v2'] is not None else 'John', c['v2_working'], c['v1']] for k, c in enumerate(cats)]), '']
for c in cats: M += [f'**{c["name"]}** ({c.get("verdict", "")}). {c.get("summary", "")}', '']
M += ['## Top insights, ranked by v2', '',
      tbl(['#', 'Insight', 'Camp', 'v2', 'Working', 'Commenters', 'Sources'],
          [[k + 1, x['claim'], x.get('category', ''), x['v2'] if x['v2'] is not None else 'John', x['v2_working'], x['v2_authors'], ids_md(x.get('comment_ids'))] for k, x in enumerate(ins)]), '']
for k, x in enumerate(ins): M += [f'{k + 1}. **{x["claim"]}** {x.get("detail", "")} ({ids_md(x.get("comment_ids"))})']
M += ['']
coverage_path = os.path.join(os.path.dirname(sp), 'coverage_insights.json')
if os.path.exists(coverage_path):
    M += ['## Additional insights from the coverage review (57–62, unranked)', '',
          'See VERIFICATION.md for the retained snapshot, selection method and limits. These are source-supported candidates, not adopted policy.', '']
    for item in json.load(open(coverage_path)):
        M += [f"### {item['id']}. {item['claim']}", '', item['application'], '',
              f"Sources: {ids_md(item['comment_ids'])}", '', f"Evidence limit: {item['evidence_limit']}", '']
if S.get('disagreements'): M += ['## Where the thread disagrees', ''] + [f'- {txt(d)}' for d in S['disagreements']] + ['']
if S.get('gold_quotes'): M += ['## Gold quotes', ''] + [f'> {txt(q)}\n' for q in S['gold_quotes']]
M += [reddit.replace('## ', '## ', 1), '', routing, '',
      '## Projects worth a look, top 15 by v2', '', 'All 114 are in data/projects_v2.json and on the page, with screenshots.', '',
      tbl(['#', 'Project', 'Camp', 'v2', 'Working', 'Note'],
          [[k + 1, f'[{p["name"]}]({p["url"]})', p['category'], p['v2'], p['v2_working'], p.get('v2_note', '')] for k, p in enumerate(topP)]), '']
known = {p['url'].rstrip('/').lower() for p in P}
more = sorted([p for p in S.get('projects', []) if p['url'].rstrip('/').lower() not in known], key=lambda p: -(p.get('inspiration') or 0))
if more: M += ['## Also linked in the thread (not screenshotted)', '', f'{len(more)} more links the synthesis found, sorted by its 1–5 inspiration rating. Not scored with v2.', '',
               tbl(['Link', 'Kind', 'Inspiration', 'What', 'Comment'], [[f'[{x["name"]}]({x["url"]})', x.get('category', ''), x.get('inspiration', ''), x.get('what', ''), f'[#{x.get("comment_id","")}]({HN}{x.get("comment_id","")})'] for x in more]), '']
if S.get('changes_vs_first_pass'): M += ['## What changed since the first pass', ''] + [f'- {txt(x)}' for x in (S['changes_vs_first_pass'] if isinstance(S['changes_vs_first_pass'], list) else [S['changes_vs_first_pass']])] + ['']
if C.get('issues') or C.get('missing'):
    M += ['## Critic notes', '', 'An independent critic agent checked the synthesis. Its points:', ''] + \
         [f'- {txt(x)}' for x in C.get('issues', [])] + [f'- Missing: {txt(x)}' for x in C.get('missing', [])] + ['']
M += ['## Process record', '', 'One-day exception to CLAUDE.md rule 14, approved by John. Delegated agents: 8 readers + 1 synthesis + 1 critic = 10. Spend: unknown (no monetary telemetry).', '']
open(os.path.join(out, 'GOLDMINE.md'), 'w').write('\n'.join(M))

# HTML sections for the page
def scell(x): return f'<td class="tot">{x["v2"] if x["v2"] is not None else "John"}<span class="work">{e(x["v2_working"])}</span></td>'
H = ['<h2 id="method">How each item is scored (v2)</h2>',
     '<p class="sub"><b>Priority = Impact × Fit × Confidence ÷ Effort</b>, where Effort = 6 − Ease. Impact, Ease and Fit are 1–5 judgements. '
     '<b>Confidence is counted</b> from distinct commenters behind the cited comments (self-promotion counts half): 3+ → 1.0, 2 → 0.8, 1 → 0.5. '
     'Anything needing John\'s decision, or with Fit ≤ 1, is not ranked and goes on the <a href="#john">John decides</a> list. v1 (the old sum out of 20) is shown for comparison.</p>',
     '<h2 id="do">What to adopt, ranked by v2</h2>', '<div class="recs">']
for r in ranked(recs):
    H.append(f'<div class="rec"><h3>{e(r["title"])} <span class="score">· v2 {r["v2"]}</span></h3><p>{md_inline(r.get("what", ""))}</p>'
             f'<p class="how"><b>In your harness:</b> {md_inline(r.get("how_in_harness", ""))}</p><span class="work">{e(r["v2_working"])} · v1 {e(r["v1"])} · {r["v2_authors"]} commenters</span></div>')
H += ['</div>', '<h2 id="john">John decides</h2>', '<p class="sub">These change policy, providers or spend, or fit poorly, so they are not ranked.</p>',
      '<div class="tbl"><table><thead><tr><th>Kind</th><th>Item</th><th>Would score / working</th></tr></thead><tbody>']
for (k, n), x in zip(gated, [x for x in cats if x['gated']] + [x for x in ins if x['gated']] + [x for x in recs if x['gated']]):
    H.append(f'<tr><td>{k}</td><td>{e(n)}</td><td class="n">{e(x["v2_working"])}</td></tr>')
H += ['</tbody></table></div>', '<h2 id="camps">The camps, ranked by v2</h2>',
      '<p class="sub">Verdict tags: <span class="tag t-adopt">ADOPT</span> worth doing now · <span class="tag t-trial">TRIAL</span> try on one packet · <span class="tag t-watch">WATCH</span> not for you yet.</p><div class="cats">']
for k, c in enumerate(cats):
    v = (c.get('verdict') or 'watch').lower(); v = v if v in ('adopt', 'trial', 'watch') else 'watch'
    H.append(f'<article class="cat"><header><h3>{k + 1}. {e(c["name"])}</h3><span class="score">{c["v2"] if c["v2"] is not None else "John"}</span></header>'
             f'<span class="tag t-{v}">{v.upper()}</span><p>{md_inline(c.get("summary", ""))}</p><div class="who">{e(c["v2_working"])} · v1 {e(c["v1"])}</div></article>')
H += ['</div>', '<h2 id="insights">Top insights, ranked by v2</h2>',
      '<div class="tbl"><table><thead><tr><th>#</th><th>Insight</th><th>v2 / working</th></tr></thead><tbody>']
for k, x in enumerate(ins):
    src = ' '.join(f'<a href="{HN}{i}" target="_blank" rel="noopener">#{i}</a>' for i in (x.get('comment_ids') or [])[:4])
    H.append(f'<tr><td class="n">{k + 1}</td><td><b>{e(x["claim"])}</b> {md_inline(x.get("detail", ""))}<span class="work">{e(x.get("category", ""))} · {src}</span></td>{scell(x)}</tr>')
H += ['</tbody></table></div>']
if S.get('disagreements'): H += ['<h2 id="disagree">Where the thread disagrees</h2><ul>'] + [f'<li>{md_inline(txt(d))}</li>' for d in S['disagreements']] + ['</ul>']
if S.get('gold_quotes'): H += ['<h2 id="quotes">Gold quotes</h2>'] + [f'<blockquote>{md_inline(txt(q))}</blockquote>' for q in S['gold_quotes']]
H += ['<section id="reddit">', md_html(reddit, 0), '</section>', '<section id="routing">', md_html(routing, 0), '</section>']
if C.get('issues') or C.get('missing'):
    iss = sorted(C.get('issues', []), key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(str(x.get('severity', '')).lower(), 3) if isinstance(x, dict) else 3)
    H += ['<section id="critic"><h2>Critic notes</h2>',
          f'<p class="sub">An independent critic agent checked the synthesis: {len(iss)} issues and {len(C.get("missing", []))} gaps. Policy-sensitive items it flagged were moved to <a href="#john">John decides</a>.</p>',
          '<details><summary>Issues found, most severe first</summary><ul>'] + \
         [f'<li><b>{e(str(x.get("severity", "")).upper())}</b> {md_inline(x.get("problem", ""))} <i>Fix:</i> {md_inline(x.get("fix", ""))}</li>' if isinstance(x, dict) else f'<li>{md_inline(txt(x))}</li>' for x in iss] + \
         ['</ul></details>', '<details><summary>What the synthesis missed</summary><ul>'] + [f'<li>{md_inline(txt(x))}</li>' for x in C.get('missing', [])] + ['</ul></details></section>']
open(os.path.join(out, 'sections.html'), 'w').write('\n'.join(H))
print('recs', len(ranked(recs)), 'gated', len(gated), 'cats', len(cats), 'insights', len(ins))
