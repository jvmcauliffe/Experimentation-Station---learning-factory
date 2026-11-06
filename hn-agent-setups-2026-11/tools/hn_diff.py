#!/usr/bin/env python3
"""Find HN comments posted since the last check and say which scores they could move.

Usage: python3 tools/hn_diff.py [--update]
  Prints a JSON report of new comments, the tracked projects each one mentions,
  and links to projects we do not track yet. --update saves the new IDs as seen.
No model calls: this is the cheap first step of each monitoring run.
"""
import json, re, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SEEN = HERE / 'data' / 'seen_comments.json'
PROJECTS = HERE / 'data' / 'projects_v2.json'
URL = 'https://hn.algolia.com/api/v1/items/{}'


def walk(node, out):
    for c in node.get('children') or []:
        out.append(c)
        walk(c, out)
    return out


def text(c):
    t = re.sub(r'<[^>]+>', ' ', c.get('text') or '')
    return re.sub(r'\s+', ' ', t.replace('&#x2F;', '/').replace('&quot;', '"').replace('&#x27;', "'")).strip()


def main():
    seen = json.loads(SEEN.read_text())
    thread = json.load(urllib.request.urlopen(URL.format(seen['thread']), timeout=60))
    comments = walk(thread, [])
    old = set(seen['seen'])
    new = [c for c in comments if c['id'] not in old and c.get('text')]
    projects = json.loads(PROJECTS.read_text())
    keys = []
    for p in projects:
        host = re.sub(r'^https?://(www\.)?', '', p.get('url', '')).rstrip('/').lower()
        keys.append((p['key'], p['name'].lower(), host))
    hits, untracked, items = {}, set(), []
    for c in new:
        t = text(c)
        low = t.lower()
        found = [k for k, name, host in keys
                 if (host and host in low) or (len(name) > 4 and re.search(r'\b' + re.escape(name) + r'\b', low))]
        for k in found:
            hits.setdefault(k, set()).add(c.get('author'))
        for u in re.findall(r'https?://[^\s)"\]]+', t):
            h = re.sub(r'^https?://(www\.)?', '', u).rstrip('/.,').lower()
            if not any(host and host in h for _, _, host in keys) and 'news.ycombinator.com' not in h:
                untracked.add(h)
        items.append({'id': c['id'], 'author': c.get('author'), 'parent': c.get('parent_id'),
                      'mentions': found, 'text': t[:400]})
    report = {'thread': seen['thread'], 'total_now': len(comments), 'seen_before': len(old),
              'new': len(new),
              'project_mentions': {k: sorted(a for a in v if a) for k, v in sorted(hits.items())},
              'untracked_links': sorted(untracked), 'comments': items}
    print(json.dumps(report, indent=1))
    if '--update' in sys.argv:
        seen['seen'] = sorted(old | {c['id'] for c in comments})
        SEEN.write_text(json.dumps(seen))


if __name__ == '__main__':
    main()
