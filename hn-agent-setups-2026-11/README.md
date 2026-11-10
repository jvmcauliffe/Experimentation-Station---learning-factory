# HN agent setups: what to take from 645 comments

- **Source:** "Ask HN: What's your current AI agentic setup?", https://news.ycombinator.com/item?id=50366117, read in full on 6 November 2026.
- **Prompted by:** the r/AI_Agents summary in `reddit/`, which is fact-checked in `reddit-check.md`.

| File | What it is |
|---|---|
| `VERIFICATION.md` | Verification of the remaining insights and the 60-comment coverage sample |
| `IMPLEMENTATION-PLAN.md` | Build sheets and the disposition of each insight |
| `verify/` | Thread snapshot and `integrity.py`, the check run on every pull request here |
| `GOLDMINE.md` | The full report: camps, top insights, recommendations, disagreements and quotes, all scored with rubric v2 |
| `agent-setups.html` | The same report as a page, with the 111-project screenshot gallery |
| `routing-table.md` | Draft table of which job goes to which model, for John's decision |
| `reddit-check.md` | The Reddit summary's 10 claims checked against the thread |
| `shots/` | Screenshots of 111 linked projects |
| `data/` | Project list, judgements and v2 scores; `synthesis_raw.json` (synthesis agent output), `synthesis_v2.json` (scored), `critic.json` (critic agent output) |
| `tools/` | Deterministic scripts: `hn_diff.py` lists thread comments not yet read, `score_v2.py` scores findings, `score_projects.py` scores projects, `build_goldmine.py` writes GOLDMINE.md and the page sections, `assemble_page.py` splices them into the page |

## Rubric v2

**Priority = Impact × Fit × Confidence ÷ Effort**

- **Effort** = 6 − Ease.
- **Confidence** is counted, not judged. It depends on how many distinct commenters back the item:

  | Commenters | Confidence |
  |---|---|
  | 3 or more | 1.0 |
  | 2 | 0.8 |
  | 1 | 0.5 |

  A commenter promoting their own project counts as half a commenter.
- **Gate:** items that need John's decision, or have Fit 1, are not ranked. They go on a "John decides" list instead.
- **Scorer:** Impact, Ease and Fit were judged by one Claude session. Codex has not done a blind second score yet.

## Process record

- **Exception:** John approved a one-day exception to rule 14 of the content-creation-pipeline working agreement on 6 November 2026 ("Make an exception today. I have a reset tomorrow."). That allowed one multi-agent workflow run.
- **Delegated model calls:**

  | Phase | Agents |
  |---|---|
  | Mine (one per comment chunk) | 8 |
  | Synthesise | 1 |
  | Critique | 1 |
  | **Total** | **10** |

- **Spend:** monetary usage is unknown.
- **Scope:** this is a research note in John's personal repository. It changes no harness policy. Every "proposed" item needs John's decision.
