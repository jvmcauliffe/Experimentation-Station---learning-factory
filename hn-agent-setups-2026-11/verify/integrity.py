"""Check retained-source integrity, not semantic truth or live completeness."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise SystemExit(message)


thread_path = ROOT / 'verify/thread.json'
require(hashlib.sha256(thread_path.read_bytes()).hexdigest() ==
        '8086b4e2955adc1f4e238ad848c032d2499392fa67382016b78da3b4804a6458',
        'Retained snapshot changed; review the evidence baseline')
thread = json.loads(thread_path.read_text())
comments = {}


def walk(node):
    comments[node['id']] = node
    for child in node.get('children', []):
        walk(child)


walk(thread)
synthesis = json.loads((ROOT / 'data/synthesis_v2.json').read_text())
insights = synthesis['top_insights']
require(len(insights) == 56, 'Expected original 56 insight records')
goldmine = (ROOT / 'GOLDMINE.md').read_text()
for number, insight in enumerate(insights, 1):
    ids = {int(cid) for cid in insight['comment_ids']}
    require(ids <= comments.keys(), f'Unknown source in insight {number}')
    rows = [line for line in goldmine.splitlines()
            if line.startswith(f'| {number} |') and insight['claim'] in line]
    require(len(rows) == 1, f'Missing/duplicate insight table row {number}')
    linked = {int(cid) for cid in re.findall(r'item\?id=(\d+)', rows[0])}
    require(linked == ids, f'Table citations differ for insight {number}')

coverage = json.loads(subprocess.check_output([
    sys.executable, '-I', str(ROOT / 'verify/coverage.py'),
    str(thread_path), str(ROOT / 'data/synthesis_v2.json')], text=True))
require((coverage['text_comments'], coverage['insight_cited_comments'],
         coverage['substantial_uncited']) == (677, 137, 118), 'Coverage counts changed')
review = json.loads((ROOT / 'verify/coverage-review.json').read_text())
require(len(review) == 60, 'Expected 60 reviewed comments')
for selected, recorded in zip(coverage['selected'], review):
    for key in ('id', 'author', 'replies', 'signals'):
        require(selected[key] == recorded[key], f'Coverage {key} mismatch')
    require(len(selected['text']) == recorded['characters'], 'Length mismatch')
    require(hashlib.sha256(selected['text'].encode()).hexdigest() ==
            recorded['full_text_sha256'], 'Reviewed full-text hash mismatch')
    require(bool(recorded['disposition'] and recorded['note']), 'Missing disposition')
additions = json.loads((ROOT / 'data/coverage_insights.json').read_text())
require([item['id'] for item in additions] == list(range(57, 63)), 'Addition IDs changed')
for item in additions:
    require({int(cid) for cid in item['comment_ids']} <= comments.keys(),
            'Unknown candidate source')
    require(item['rank'] is None and bool(item['evidence_limit']),
            'Candidate ranking or evidence limit changed')
print('PASS: snapshot, 56 citation rows, 60 full-text hashes, six unranked candidates')
print('Semantic review and uncovered comments remain outside this mechanical check.')
