"""Emit reproducible substantial uncited comments for human/model coverage review.

This selects evidence; it does not decide whether an insight is supported.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('thread', type=Path)
parser.add_argument('synthesis', type=Path)
parser.add_argument('--limit', type=int, default=60)
args = parser.parse_args()
thread = json.loads(args.thread.read_text())
synthesis = json.loads(args.synthesis.read_text())
comments = {}

def walk(node):
    comments[node['id']] = node
    for child in node.get('children', []):
        walk(child)

walk(thread)
cited = {int(cid) for insight in synthesis['top_insights'] for cid in insight['comment_ids']}
rows = []
for cid, comment in comments.items():
    text = html.unescape(re.sub('<[^>]+>', ' ', comment.get('text') or ''))
    if cid == thread['id'] or cid in cited or len(text) < 600:
        continue
    rows.append(dict(id=cid, author=comment['author'], replies=len(comment.get('children', [])),
                     signals=len(re.findall(r'i have|my workflow|unlock|game changer|never|always', text, re.I)),
                     text=text))
rows.sort(key=lambda row: (-row['replies'], -row['signals'], -len(row['text']), row['id']))
print(json.dumps(dict(snapshot_sha256=hashlib.sha256(args.thread.read_bytes()).hexdigest(),
                     text_comments=sum(bool(c.get('text')) for c in comments.values()),
                     insight_cited_comments=len(cited), substantial_uncited=len(rows),
                     selected=rows[:args.limit]), ensure_ascii=False, indent=2))
