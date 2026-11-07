"""Regenerate GOLDMINE.md deterministically from data/projects_v2.json (rubric v2)."""
import json, collections, sys
d = json.load(open(sys.argv[1]))
ranked = sorted([p for p in d if p['fit'] > 1], key=lambda p: (-p['v2'], p['name'].lower()))
gated = [p for p in d if p['fit'] <= 1]
def row(i, p):
    cat = p['category'] or 'Uncategorised'
    return f"| {i} | [{p['name']}]({p['url']}) | {cat} | {p['impact']} | {p['ease']} | {p['fit']} | {p['v2_working']} | {p['v2']} | {p.get('v2_note') or p['what'][:90]} |"
hdr = "| # | Project | Category | Impact | Ease | Fit | Working | Priority | Note |\n|---|---|---|---|---|---|---|---|---|"
L = ["# GOLDMINE: HN agent setups (regenerated from data)", "",
"Source: Ask HN, 'What's your current AI agentic setup?' (item 50366117), read 6 November 2026. Rubric v2: Priority = Impact × Fit × Confidence ÷ Effort (Effort = 6 − Ease). See `README.md`.", "",
"**Regeneration note (7 November 2026).** The original report was not committed. This version is rebuilt only from `data/projects_v2.json` by `tools/make_goldmine.py`. The camps, thread insights and quotes came from the synthesis step, which was not saved, so they are not here. For those see `routing-table.md` and `reddit-check.md`. Scores are from one Claude session; Codex has not scored blind.", "",
f"## Counts", "", "| Measure | Value |", "|---|---|", f"| Projects scored | {len(d)} |", f"| Ranked (Fit ≥ 2) | {len(ranked)} |", f"| Gated (Fit 1) | {len(gated)} |", ""]
cats = collections.Counter(p['category'] or 'Uncategorised' for p in d)
L += ["## By category", "", "| Category | Projects |", "|---|---|"] + [f"| {c} | {n} |" for c, n in cats.most_common()] + [""]
L += ["## Top 20 by priority", "", hdr] + [row(i, p) for i, p in enumerate(ranked[:20], 1)] + [""]
sup = [p for p in ranked if p['category'] in ('Orchestrators', 'Pipelines', 'Harnesses', 'Tickets')]
L += ["## Supervisory and orchestration projects (ranked)", "", hdr] + [row(i, p) for i, p in enumerate(sup, 1)] + [""]
L += ["## Gated: Fit 1, not ranked", "", "| Project | Category | What |", "|---|---|---|"] + [f"| [{p['name']}]({p['url']}) | {p['category'] or 'Uncategorised'} | {p['what'][:110]} |" for p in gated] + [""]
L += ["## Full ranking", "", hdr] + [row(i, p) for i, p in enumerate(ranked, 1)] + [""]
open(sys.argv[2], 'w').write("\n".join(L))
print(len(ranked), len(gated), len(sup))
