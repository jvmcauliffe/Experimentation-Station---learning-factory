"""Splice v2 sections into the page. Usage: assemble_page.py base.html sections.html scored_synth.json out.html [rt.out.json]"""
import json, sys, re, html
base, sec, sp, out = sys.argv[1:5]
L = open(base).read().split('\n'); SEC = open(sec).read(); S = json.load(open(sp))
recs = [r for r in S['recommendations'] if not r['gated']]
for a in sys.argv[5:]: recs += json.load(open(a))['recommendations']
recs.sort(key=lambda r: -r['v2'])
idx = lambda pred: next(i for i, l in enumerate(L) if pred(l))
a, b = idx(lambda l: l.startswith('<h2 id="method">')), idx(lambda l: l.startswith('<h2 id="cost">'))
L[a:b] = [SEC]
t0 = idx(lambda l: l.startswith('<div class="tldr"')); t1 = idx(lambda l: l.startswith('</ol></div>'))
e = html.escape
L[t0:t1 + 1] = ['<div class="tldr" id="tldr"><strong>Top five changes for your harness, by v2 priority</strong><ol>'] + \
    [f'<li><b>{e(r["title"])}</b> — v2 {r["v2"]} <span class="work">{e(r["v2_working"])}</span></li>' for r in recs[:5]] + \
    ['</ol><p style="margin:10px 0 0;font-size:14px">The thread\'s loudest message is still "less is more": nobody posted an eval showing a custom harness beats vanilla. Six more ideas need your decision; see <a href="#john">John decides</a>.</p></div>']
i = idx(lambda l: l.startswith('<nav class="toc">'))
L[i] = '<nav class="toc">' + ''.join(f'<a href="#{h}">{t}</a>' for h, t in [('tldr', 'TL;DR'), ('method', 'How scored'), ('do', 'What to adopt'), ('john', 'John decides'), ('camps', 'Camps'), ('insights', 'Insights'), ('disagree', 'Disagreements'), ('quotes', 'Quotes'), ('reddit', 'Reddit check'), ('routing', 'Routing table'), ('critic', 'Critic notes'), ('cost', 'Cost maths'), ('gallery', 'Gallery')]) + '</nav>'
i = idx(lambda l: l.startswith('<p class="lede">'))
L[i] = f'<p class="lede">The 645-comment thread, mined by eight parallel readers, synthesised and critic-checked: {len(S["categories"])} camps, {len(S["top_insights"])} insights and {len(S["recommendations"]) + len(sys.argv[5:])} candidate changes for your three-provider harness, all scored with rubric v2. It ends with screenshots of 111 linked projects.</p>'
i = idx(lambda l: l.startswith('<footer>'))
L[i] = '<footer>Source: news.ycombinator.com/item?id=50366117 (645 comments). Screenshots taken 6 Nov 2026 at 1280×800. Impact, Ease and Fit are judgement calls; Confidence is counted from commenters. Made under a one-day exception to CLAUDE.md rule 14 approved by John: 8 readers + 1 synthesis + 1 critic = 10 delegated agents. Spend: unknown.</footer>'
# drop the v1 camp/rec data and renderers
L = [l for l in L if not re.match(r"(const (CAMPS|RECS|camps|recs|tagTxt|row|rank|sum)=|document\.(getElementById\('(catgrid|recs)'\)|querySelector\('#(camptable|rectable))|\s*\{n:|\s*\{t:|\];?$)", l)]
open(out, 'w').write('\n'.join(L))
