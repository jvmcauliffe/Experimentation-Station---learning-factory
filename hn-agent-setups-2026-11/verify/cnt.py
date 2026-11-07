import json,re,html,sys
t=json.load(open(sys.argv[1]))
T=[]
def w(n):
    if n.get('text'): T.append(re.sub(r'<[^>]+>',' ',html.unescape(n['text'])).lower())
    for c in n.get('children',[]): w(c)
w(t)
print('comments with text',len(T))
for name,rx in [('deepseek','deepseek|deep seek|\\bds\\s?v?4'),('qwen','qwen'),('kimi','kimi'),('gpt/codex','gpt|codex'),('opencode go','opencode go'),('glm','glm'),('hermes','hermes'),('herdr','herdr'),('pi','\\bpi\\b|pi\\.dev'),('opus','opus'),('sonnet','sonnet')]:
    print(name,sum(1 for x in T if re.search(rx,x)))
