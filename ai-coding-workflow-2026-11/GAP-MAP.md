# Gap map: vaibhav-space/my-ai-coding-workflow

Source: [github.com/vaibhav-space/my-ai-coding-workflow](https://github.com/vaibhav-space/my-ai-coding-workflow) (README, CLAUDE.md and three prompts), read 14 November 2026. One author's personal setup, so every insight has Confidence 0.5. The repository has no licence file: ideas are adapted, no text is copied.

Scoring follows the HN gold mine v2: Priority = Impact × Fit × Confidence ÷ (6 − Ease).

## Merged (content-creation-pipeline [PR 485](https://github.com/jvmcauliffe/Content-Creation-Pipeline/pull/485), squash commit `c66493a` on `main`)

Merged on 15 November 2026 at 16:45 UTC as squash commit `c66493a9db1f7a21fc04ab4cee461f72f54d6992`. The reviewed head was `c1f6bef`: CLEAR in an independent exact-head review (PR 485 comment 6883379326), CI green, and John's own J2 confirmation (per Codex, ES PR 15 comment 6897860469). History: the first head, `08f4cba`, failed Codex's exact-head review (the checker passed an empty checklist); `56bc708` makes it fail closed; `e7cd5bf` adds the three skill packs; `76429d8` amends CLAUDE.md rule 17 on John's instruction (one fresh-context review per plan task, inside rule 15's ten calls); `08c67aa` adds an identity and use gate after the Nova Sprint lesson; `a01dbcf` makes it a script check (`scripts/check_plan_identity.py`); later heads up to `c1f6bef` harden the acceptance check against shell tricks that run local code.

Merged means the files below are on `main` and the plan gate runs in CI (`capability-tests.yml` runs `tests/test_check_plan_identity.py`, including `test_committed_plans_pass_the_gate`). It does not mean installed or measured: see Not done.

| # | Practice | Location on `main` | v2 | Working |
| --- | --- | --- | --- | --- |
| 1 | Diff review answers a fixed question list, not the author's summary | `docs/review/code-questions.md` (13 questions, CLEAR or DISCREPANCY), checked by `scripts/check_review_verdicts.py --checklist` | 10.0 | 4×5×0.5÷1 = 10.0 |
| 2 | Size the task first: spike, bounded, architectural | `skills/plan-and-diff-review` | 6.0 | 3×4×0.5÷1 = 6.0 |
| 3 | Simplest-first ladder and surgical edits | Same skill, stage 1; checklist Q1 and Q2 | 6.0 | 3×4×0.5÷1 = 6.0 |
| 4 | One-hypothesis failure loop | Same skill, "When a check fails"; second failure escalates under rule 11 | 6.0 | 3×4×0.5÷1 = 6.0 |
| 5 | Adversarial plan review in a fresh context | Same skill, stage 2; one delegated call under rule 15 | 4.0 | 4×4×0.5÷2 = 4.0 |
| 6 | Plan grounded in the code, one runnable check per requirement | Same skill, stage 1 | 3.0 | 3×4×0.5÷2 = 3.0 |
| 7 | Identity and use gate: pin the upstream tool and run it in the acceptance check, name the user and what it replaces, spike first | `scripts/check_plan_identity.py` on `docs/plans/`, run in CI; checklist Q12 and Q13 (added after two days went on Nova Sprint and a lookalike) | not scored | n/a |

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
| "Active mode" badge on line 1 of every reply | Adds tokens; rule 13 already reports the actual route |
| Global `~/.claude/CLAUDE.md` | Cloud containers are rebuilt each session; the repo CLAUDE.md is the durable carrier |
| Tenant-scoped tool identity | No multi-tenant tools in this harness |

## Accepted by John (14 November 2026)

The superpowers, ponytail and i-have-adhd packs were declined at first, then accepted by John. They are copied unmodified (MIT) into `skills/` and merged with PR 485. Hooks are not copied, and the packs are not installed (`scripts/install_skills.py` does not list them). `skills/ATTRIBUTION-third-party-skills.md` lists each conflict with the rules (merge, approvals, subagent counts, always-on loading, worktrees, hooks). Where they conflict, the rules win.

## Not done

- A pointer to the skill from CLAUDE.md rule 18 is governance text, which John edits himself (standing directives, HN decision J2).
- The `plan-and-diff-review` skill is merged but not listed in `scripts/install_skills.py`, so it is not installed, and it has not been measured against working without it.
