## Role-to-model routing table (draft for John)

Why: the most-copied idea from the thread and the Reddit summary is to write down **which job goes to which model**. phillc73 #50367557 and ActionHank #50379104 both do this. Your routes (`bounded_extraction`, `standard_reasoning`, `highest_reasoning`) say *how hard* a job is. This table says *which job* goes to which provider and route. Rows marked **existing** restate your CLAUDE.md. Rows marked **proposed** need your decision.

| # | Role | Owner | Route | Escalate when | Status | Thread precedent |
|---|---|---|---|---|---|---|
| 0 | Monitoring, caps, lint, tests, hash checks | Scripts and hooks; no model | none | A check is missing or fails: stop, and never treat that as a pass | existing (rules 4, 7, 17) | phillc73 uses "mechanical gates… no remote git pushes without explicit prior approval" |
| 1 | Extraction: pulling facts, counting, summarising logs, first-pass tagging | GreenPT; its output is a candidate only | `bounded_extraction` | A deterministic check rejects the candidate: Claude, `standard_reasoning` | existing | quard8 #50377888 uses "a small qwen model… mostly searching and summarization" |
| 2 | Coordination: splitting tasks, routing packets, triage | Claude | `standard_reasoning` | Never above standard | existing. In the thread a cheap model does this; your rules keep planning with the strong owners, so GreenPT stays out | ActionHank uses "GLM 5.3 Flash for orchestration", and phillc73 uses "GLM5.3 Flash for… co-ordination" |
| 3 | Planning and architecture | Claude | `standard_reasoning` | Consequential or cross-repo: `highest_reasoning`, only after the explicit premium command | existing (rule 16) | Xonzo #50378776 uses "Sol 6.1 xHigh for planning/review" |
| 4 | Coding and implementation | Claude, as the single implementation owner | `standard_reasoning` | The same check fails twice: escalate, within the packet's retry limit | existing | phillc73 and ActionHank both use DeepSeek Flash for coding |
| 4b | Bulk mechanical edits by a cheap coder | Not yet assigned | `bounded_extraction` | n/a | **proposed: needs John** (it adds a fourth provider) | Same as row 4 |
| 5 | Adversarial and independent review | Codex: **always a different provider from the author** | `standard_reasoning` | Consequential: `highest_reasoning` after the premium command | **proposed: make "reviewer ≠ author's provider" a written rule for content work too.** Today it is only stated for implementation PRs | phillc73 uses "GLM5.3 for adversarial batteries", drbscl #50367676 uses one "mostly for review, second opinion", and ActionHank uses "Occasional call out to claude for a review" |
| 6 | Fact gate | Codex, or a Claude session that is not the author | `standard_reasoning` | n/a | existing (only when the consumer policy triggers it) | none |
| 7 | Documentation and handover (HANDOFF.md, receipts summary) | Claude drafts; GreenPT may draft boilerplate that is not private | `bounded_extraction` → `standard_reasoning` | Anything going to a consumer site: Claude | **proposed** | phillc73 uses GLM5.3 for "documentation" |
| 8 | Final approval, merge, publish, marking facts verified, raising caps | **John only** | n/a | n/a | existing | none |

**Guardrails that apply on top:** one route per packet (rule 16); nothing private is sent to GreenPT (`docs/private/`); GreenPT output stays a candidate; a stronger model is never used just to repeat unchanged evidence.

**How to adopt it:** paste this into `docs/standing-directives.md` as one packet with three decisions:
1. Approve rows 5 and 7 as written.
2. Say yes or no to row 4b.
3. Add a one-line check to the packet lint that rejects a packet whose reviewer provider matches its author provider.
