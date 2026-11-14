# Gap map: vaibhav-space/my-ai-coding-workflow

Source: [github.com/vaibhav-space/my-ai-coding-workflow](https://github.com/vaibhav-space/my-ai-coding-workflow) (README, CLAUDE.md and three prompts), read 14 November 2026. One author's personal setup, so every insight has Confidence 0.5. The repository has no licence file: ideas are adapted, no text is copied.

Scoring follows the HN gold mine v2: Priority = Impact × Fit × Confidence ÷ (6 − Ease).

## Proposed, in review (content-creation-pipeline [PR 485](https://github.com/jvmcauliffe/Content-Creation-Pipeline/pull/485), head `56bc708231f0767b300cc0209e0b1c28c6f1852c`)

Not merged. The first head, `08f4cba`, failed Codex's exact-head review (the checker passed an empty checklist); `56bc708` makes it fail closed and awaits re-review. Nothing below counts as built until PR 485 merges.

| # | Practice | Proposed location | v2 | Working |
| --- | --- | --- | --- | --- |
| 1 | Diff review answers a fixed question list, not the author's summary | `docs/review/code-questions.md` (11 questions, CLEAR or DISCREPANCY), checked by `scripts/check_review_verdicts.py --checklist` | 10.0 | 4×5×0.5÷1 = 10.0 |
| 2 | Size the task first: spike, bounded, architectural | `skills/plan-and-diff-review` | 6.0 | 3×4×0.5÷1 = 6.0 |
| 3 | Simplest-first ladder and surgical edits | Same skill, stage 1; checklist Q1 and Q2 | 6.0 | 3×4×0.5÷1 = 6.0 |
| 4 | One-hypothesis failure loop | Same skill, "When a check fails"; second failure escalates under rule 11 | 6.0 | 3×4×0.5÷1 = 6.0 |
| 5 | Adversarial plan review in a fresh context | Same skill, stage 2; one delegated call under rule 15 | 4.0 | 4×4×0.5÷2 = 4.0 |
| 6 | Plan grounded in the code, one runnable check per requirement | Same skill, stage 1 | 3.0 | 3×4×0.5÷2 = 3.0 |

## Already covered by the harness

| Practice | Existing rule |
| --- | --- |
| Evidence before claims | CLAUDE.md rule 5, rule 19 |
| Independent review, author never merges | CLAUDE.md rule 6 |
| Deterministic arithmetic | AGENTS.md rule 4; John's chat preference; checklist Q8 |
| Approval before risky changes | Task packets, rule 8, Reserved to John; checklist Q10 |
| Retry discipline | Rule 9 for model attempts; checklist Q7 now covers code |
| Short, answer-first replies | John's chat preferences |

## Declined

| Practice | Reason |
| --- | --- |
| Install superpowers, ponytail and i-have-adhd skill packs | Overlap the rules above; extra context every session; superpowers' branch-finishing step offers merge options that conflict with the rule 6 merge gate |
| "Active mode" badge on line 1 of every reply | Adds tokens; rule 13 already reports the actual route |
| Global `~/.claude/CLAUDE.md` | Cloud containers are rebuilt each session; the repo CLAUDE.md is the durable carrier |
| Tenant-scoped tool identity | No multi-tenant tools in this harness |

## Not done

- A pointer to the skill from CLAUDE.md rule 18 is governance text, which John edits himself (standing directives, HN decision J2).
- The skill is not listed in `scripts/install_skills.py` and has not been measured against working without it.
