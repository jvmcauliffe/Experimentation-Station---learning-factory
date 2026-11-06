# Gold mine: Ask HN "What's your current AI agentic setup?"

Source: [https://news.ycombinator.com/item?id=50366117](https://news.ycombinator.com/item?id=50366117), 645 comments, mined 6 Nov 2026 by 8 parallel readers, one synthesis and one critic.

## How v2 is scored

Priority = Impact × Fit × Confidence ÷ Effort. Effort = 6 − Ease. Impact, Ease and Fit are 1–5 judgements. Confidence is counted, not judged: distinct commenters behind the cited comments (a self-promoting comment counts 0.5); 3 or more → 1.0, 2 → 0.8, 1 → 0.5. With no cited ids it falls back to the old Evidence score and says "proxy". Anything that needs John's decision, or has Fit ≤ 1, is not ranked; it goes on the John decides list. v1 is the old sum out of 20, kept for comparison.

## Changes to adopt, ranked by v2

| # | Change | v2 | Working | v1 | Commenters |
| --- | --- | --- | --- | --- | --- |
| 1 | Write HANDOFF.md and DECISIONS.md at packet close | 25.0 | 5×5×1.0÷1 = 25.0 | 5+5+4+5 = 19 | 4.5 |
| 2 | Question-list reviewer with binary verdicts | 25.0 | 5×5×1.0÷1 = 25.0 | 5+5+3+5 = 18 | 3.0 |
| 3 | Write one role-to-model routing table | 20.0 | 4×5×1.0÷1 = 20.0 | 4+5+4+5 = 18 | 5.0 |
| 4 | Keep width at two workers; decline swarm tooling | 12.0 | 3×4×1.0÷1 = 12.0 | 3+5+5+4 = 17 | 5.0 |
| 5 | Use GreenPT more for bounded extraction, inside the cap | 10.0 | 4×5×1.0÷2 = 10.0 | 4+4+4+5 = 17 | 5.0 |
| 6 | One cost and quota board read from receipts | 10.0 | 4×5×1.0÷2 = 10.0 | 4+4+4+5 = 17 | 3.5 |
| 7 | Deterministic private-path guard before GreenPT | 10.0 | 4×5×1.0÷2 = 10.0 | 4+4+4+5 = 17 | 3.5 |
| 8 | Phone digest: one queue of 'needs John' items | 10.0 | 4×5×1.0÷2 = 10.0 | 4+4+3+5 = 16 | 4.0 |
| 9 | Spec-first content packets that must ship an artefact | 10.0 | 4×5×1.0÷2 = 10.0 | 4+4+3+5 = 16 | 4.0 |
| 10 | Monthly turn-sink review | 6.7 | 4×5×1.0÷3 = 6.7 | 4+3+3+5 = 15 | 3.0 |

### 1. Write HANDOFF.md and DECISIONS.md at packet close — v2 25.0

At the end of each packet, the owning model writes a short committed HANDOFF.md (status, what was learnt, what remains) and appends to DECISIONS.md (or an ADR). The next packet starts fresh from these files rather than from compacted context.

**In your harness:** Add an in-scope path such as docs/handover/ to packet templates. Trial it in Experimentation Station first. A deterministic lint checks that the files exist and are under a size cap before closeout. This fits the existing rule that handover belongs in committed in-scope files, not /tmp.

Sources: [#50375342](https://news.ycombinator.com/item?id=50375342), [#50375274](https://news.ycombinator.com/item?id=50375274), [#50376262](https://news.ycombinator.com/item?id=50376262), [#50375278](https://news.ycombinator.com/item?id=50375278), [#50377952](https://news.ycombinator.com/item?id=50377952)

### 2. Question-list reviewer with binary verdicts — v2 25.0

Turn John's own review questions for content (facts needing verification, UK English, tone, claims, links, private-material leaks) into a fixed checklist. The independent Codex or Claude reviewer answers each question CLEAR or DISCREPANCY, with no numeric scores.

**In your harness:** Commit the checklist per consumer, for example review/questions.md. The reviewer prompt quotes it verbatim, and a script parses the binary verdicts into the receipt. Its hash joins the policy hash for review reuse under rule 11.

Sources: [#50378899](https://news.ycombinator.com/item?id=50378899), [#50380633](https://news.ycombinator.com/item?id=50380633), [#50379808](https://news.ycombinator.com/item?id=50379808)

### 3. Write one role-to-model routing table — v2 20.0

Write down which job goes to which provider and route: monitoring by scripts, extraction by GreenPT, planning and coding by Claude, review by a different provider from the author, final calls by John. Three rows are proposals.

**In your harness:** See the routing table section below.

Sources: [#50367557](https://news.ycombinator.com/item?id=50367557), [#50379104](https://news.ycombinator.com/item?id=50379104), [#50367676](https://news.ycombinator.com/item?id=50367676), [#50378776](https://news.ycombinator.com/item?id=50378776), [#50377888](https://news.ycombinator.com/item?id=50377888)

### 4. Keep width at two workers; decline swarm tooling — v2 12.0

Formally keep the current caps (two parallel workers, five delegated calls). Do not adopt swarm or orchestrator products; human attention and token burn are the binding limits.

**In your harness:** No rule change. Note the evidence in docs/standing-directives.md if John wants a record.

Sources: [#50373117](https://news.ycombinator.com/item?id=50373117), [#50376632](https://news.ycombinator.com/item?id=50376632), [#50375205](https://news.ycombinator.com/item?id=50375205), [#50376279](https://news.ycombinator.com/item?id=50376279), [#50373445](https://news.ycombinator.com/item?id=50373445)

### 5. Use GreenPT more for bounded extraction, inside the cap — v2 10.0

Send more mechanical pre-work to GreenPT: extracting claims for fact-checking, link and glossary consistency lists, structured summaries of source notes. Prose and judgement stay with Claude and Codex. Near month end, queue pre-approved low-risk extraction packets to use spare cap.

**In your harness:** Keep using [greenpt-task-v1] packets with the per-issue limits unchanged. A small queue file in Experimentation Station lists ready bounded tasks. The session triggers them only while the bridge's running total stays below EUR 10.00.

Sources: [#50381117](https://news.ycombinator.com/item?id=50381117), [#50375427](https://news.ycombinator.com/item?id=50375427), [#50380990](https://news.ycombinator.com/item?id=50380990), [#50367589](https://news.ycombinator.com/item?id=50367589), [#50373357](https://news.ycombinator.com/item?id=50373357)

### 6. One cost and quota board read from receipts — v2 10.0

A deterministic script reads the sealed receipts and produces one page. It shows the GreenPT month total against the cap, app-started Claude and Codex counts against 250 each, packets, retries and escalations. Missing telemetry is shown as unknown.

**In your harness:** A script in Experimentation Station runs on demand, with output committed or published as a private page John can open from his phone. It makes no model calls.

Sources: [#50373740](https://news.ycombinator.com/item?id=50373740), [#50374094](https://news.ycombinator.com/item?id=50374094), [#50376390](https://news.ycombinator.com/item?id=50376390), [#50376352](https://news.ycombinator.com/item?id=50376352)

### 7. Deterministic private-path guard before GreenPT — v2 10.0

Before any GreenPT trigger, refuse a packet whose inputs reference docs/private/ or match a redaction pattern list. Mirrors commenters who route personal data only to private models and redact diffs before cloud review.

**In your harness:** If greenpt_bridge.py --lint does not already check this, add the check there with a unit test in the existing suite. The PreToolUse hook then blocks the trigger automatically.

Sources: [#50385740](https://news.ycombinator.com/item?id=50385740), [#50377307](https://news.ycombinator.com/item?id=50377307), [#50376538](https://news.ycombinator.com/item?id=50376538), [#50376810](https://news.ycombinator.com/item?id=50376810)

### 8. Phone digest: one queue of 'needs John' items — v2 10.0

A single daily or on-demand digest lists every pending item that needs John: candidates awaiting approval, blocked packets and unresolved findings. Each has an approve or deny line he can act on from the phone. 'Done' notices stay separate from 'needs John' notices.

**In your harness:** A deterministic script collects open issues by label and posts one comment on a fixed issue. Bulk decisions are still recorded as John's own comments, so the authority rules are unchanged.

Sources: [#50385555](https://news.ycombinator.com/item?id=50385555), [#50379826](https://news.ycombinator.com/item?id=50379826), [#50373796](https://news.ycombinator.com/item?id=50373796), [#50380777](https://news.ycombinator.com/item?id=50380777)

### 9. Spec-first content packets that must ship an artefact — v2 10.0

Each implementation packet carries a brief (purpose, audience, sections, acceptance checks) that must be unambiguous before drafting starts. The packet must change a content file, not only produce reports, to avoid 'productivity porn'.

**In your harness:** Add 'brief' and 'deliverable_paths' fields to the Claude task packet, with a lint that the PR diff touches at least one deliverable path.

Sources: [#50382792](https://news.ycombinator.com/item?id=50382792), [#50381456](https://news.ycombinator.com/item?id=50381456), [#50380633](https://news.ycombinator.com/item?id=50380633), [#50378376](https://news.ycombinator.com/item?id=50378376)

### 10. Monthly turn-sink review — v2 6.7

Once a month, list which packet stages consumed the most turns, retries and delegated calls. Turn the single biggest sink into a deterministic script.

**In your harness:** Use the receipt-reading script from the cost board, with an output table per stage. The conversion work goes in a normal implement-and-open-pr packet.

Sources: [#50374764](https://news.ycombinator.com/item?id=50374764), [#50378157](https://news.ycombinator.com/item?id=50378157), [#50367326](https://news.ycombinator.com/item?id=50367326)

## John decides (not ranked)

These change policy, providers or spend, or fit poorly, so they are listed for your decision instead of ranked.

| Kind | Item | Would score | Working |
| --- | --- | --- | --- |
| Change | Content-diff check for review reuse | 3.3 | 4×5×0.5÷3 = 3.3 |
| Change | Explicit escalation rule across model routes | 12.5 | 5×5×1.0÷2 = 12.5 |
| Change | Review stop rule | 20.0 | 4×5×1.0÷1 = 20.0 |
| Change | Bake-off: vanilla against the full harness | 8.3 | 5×5×1.0÷3 = 8.3 |
| Change | Prune CLAUDE.md and move rules into hooks | 8.0 | 4×4×1.0÷2 = 8.0 |
| Change | Persona readers for academy and Sark content | 5.3 | 4×5×0.8÷3 = 5.3 |

## Camps, ranked by v2

| # | Camp | Verdict | v2 | Working | v1 |
| --- | --- | --- | --- | --- | --- |
| 1 | Context and memory as files | adopt | 20.0 | 4×5×1.0÷1 = 20.0 (conf. proxy) | 4+5+5+5 = 19 |
| 2 | Minimalism and evals against vanilla | adopt | 16.0 | 4×4×1.0÷1 = 16.0 (conf. proxy) | 4+5+5+4 = 18 |
| 3 | Cross-vendor and cross-model review | adopt | 12.5 | 5×5×1.0÷2 = 12.5 (conf. proxy) | 5+4+5+5 = 19 |
| 4 | Tiered routing: plan strong, execute cheap, escalate | adopt | 12.5 | 5×5×1.0÷2 = 12.5 (conf. proxy) | 5+4+5+5 = 19 |
| 5 | Issues and tickets as the agent interface | adopt | 10.0 | 4×5×1.0÷2 = 10.0 (conf. proxy) | 4+4+5+5 = 18 |
| 6 | Skills, prompts and prose quality | trial | 10.0 | 4×5×1.0÷2 = 10.0 (conf. proxy) | 4+4+4+5 = 17 |
| 7 | Deterministic-first workflows | adopt | 8.3 | 5×5×1.0÷3 = 8.3 (conf. proxy) | 5+3+4+5 = 17 |
| 8 | Cheap open-weight workers | trial | 8.0 | 4×4×1.0÷2 = 8.0 (conf. proxy) | 4+4+5+4 = 17 |
| 9 | Session control: phone, remote, voice and alerts | trial | 7.5 | 3×5×1.0÷2 = 7.5 (conf. proxy) | 3+4+4+5 = 16 |
| 10 | Cost and quota telemetry | adopt | 6.7 | 4×5×1.0÷3 = 6.7 (conf. proxy) | 4+3+4+5 = 16 |
| 11 | Verification beyond code review | trial | 6.7 | 4×5×1.0÷3 = 6.7 (conf. proxy) | 4+3+4+5 = 16 |
| 12 | Coordinator-style orchestration | trial | 5.3 | 4×4×1.0÷3 = 5.3 (conf. proxy) | 4+3+4+4 = 15 |
| 13 | Skeptics, attention limits and wellbeing | adopt | 4.5 | 3×3×1.0÷2 = 4.5 (conf. proxy) | 3+4+5+3 = 15 |
| 14 | Sandboxing and credential isolation | trial | 4.0 | 4×3×1.0÷3 = 4.0 (conf. proxy) | 4+3+5+3 = 15 |
| 15 | Personal agents and local inference | watch | 1.0 | 2×2×1.0÷4 = 1.0 (conf. proxy) | 2+2+4+2 = 10 |

**Context and memory as files** (adopt). HANDOFF.md resets instead of compaction, plus ADRs, DECISIONS/LOG files, per-repo state files, close-out notes to AGENTS.md and status repos. Contrarian: re-explaining forces better thinking, so keep these files short.

**Minimalism and evals against vanilla** (adopt). Vanilla Claude Code or Codex goes a long way. 5.5-era models need fewer guardrails, and broad skills poison context. Hardly anyone evaluates custom setups against the vanilla harness, which is the key test.

**Cross-vendor and cross-model review** (adopt). One provider authors, another reviews, by default. The most independently backed pattern in the thread. Variants: question-list reviews in a fresh session, clean-context review loops, commit-pinned review caches. Warning: review always finds something, so it needs a stop rule.

**Tiered routing: plan strong, execute cheap, escalate** (adopt). An expensive model plans or reviews and a cheap model executes. An Opus coordinator classifies tasks into tiers and escalates a failing card up the tiers. Effort is raised only for architecture work.

**Issues and tickets as the agent interface** (adopt). GitHub issues, Jira/Linear or kanban-as-files hand work from a planner to an executor. Questions and side findings come back as tickets. This is John's existing design and the thread backs it strongly.

**Skills, prompts and prose quality** (trial). Models, cheap ones especially, still write poor prose, so humans or strong models should own final text. Small prompt wins (the 'Vulcan' tone line) and refined frequent-prompt skills help. Broad skills don't.

**Deterministic-first workflows** (adopt). Start as a skill, harden into scripts, and use agents only as fallbacks. Make workflows resumable, and turn the biggest token sinks into ordinary code when limits bite.

**Cheap open-weight workers** (trial). DeepSeek and GLM flash models through cheap plans or PAYG, with hard cost data (1B tokens for 7% of a $10 plan; ~$20/week at a 99% cache hit rate). Counter-evidence says they can cost more than a subscription in practice.

**Session control: phone, remote, voice and alerts** (trial). Remote control per project, phone apps, chat front doors, push-to-talk voice and separate 'done' and 'needs you' alerts. Session managers (Herdr, T3, Orca) are useful, but this is tooling rather than method.

**Cost and quota telemetry** (adopt). Usage-limit trackers, public usage pages, per-loop cost control rooms, gateway dashboards, spare-capacity schedulers and quota dispatchers.

**Verification beyond code review** (trial). Persona dogfood rigs, browser exploratory QA loops, agent-built review pages, binary CLEAR/DISCREPANCY gates and clean-up passes after fleet work. Includes the warning about 'productivity porn'.

**Coordinator-style orchestration** (trial). The main thread only coordinates. A chief-of-staff agent requires agentic review before a human sees a PR, and a pm-intake seat batches findings into a digest. Wide swarms and free inter-session messaging drift into chaos.

**Skeptics, attention limits and wellbeing** (adopt). Human attention caps parallelism at about 3-6 sessions, and there are many burnout warnings. Single-threaded work keeps the mental model intact. Supports keeping John's two-worker cap.

**Sandboxing and credential isolation** (trial). Credential-injecting proxies, no keys in VMs, push only from the host, scoped read-only credentials and external sandboxes, because Claude has been seen disabling its own. Cloud sessions and the push hook already cover much of this for John.

**Personal agents and local inference** (watch). Claw-style personal agents are unstable and dwindle into digest bots. Local models need hardware and don't suit phone-first cloud work. The one transferable idea is privacy routing: private material goes only to private models.

## Top insights, ranked by v2

| # | Insight | Camp | v2 | Working | Commenters |
| --- | --- | --- | --- | --- | --- |
| 1 | Reset context with a HANDOFF.md summary instead of relying on compaction, and keep context fill low | context_memory | 25.0 | 5×5×1.0÷1 = 25.0 | 5.0 |
| 2 | Make the main thread a pure coordinator that never implements | orchestration | 16.0 | 4×4×1.0÷1 = 16.0 | 3.0 |
| 3 | Subagents are the quickest way to burn limits; use them for map-reduce-shaped tasks | orchestration | 16.0 | 4×4×1.0÷1 = 16.0 | 3.0 |
| 4 | Cross-vendor review by default: one provider authors, another reviews, with more providers added for critical work | multi_model_review | 12.5 | 5×5×1.0÷2 = 12.5 | 11.0 |
| 5 | Plan with a strong model and execute with a cheap one | models_routing | 12.5 | 5×5×1.0÷2 = 12.5 | 10.5 |
| 6 | Review in a fresh session driven by a fixed list of your own PR-review questions | multi_model_review | 12.5 | 5×5×0.5÷1 = 12.5 | 1.0 |
| 7 | Hide keys behind a credential-injecting proxy: no keys in the agent VM | sandbox_security | 12.0 | 4×3×1.0÷1 = 12.0 | 4.5 |
| 8 | Escalate a failing task up model tiers (flash, pro, heavy, frontier) until it is solved | models_routing | 10.0 | 5×5×0.8÷2 = 10.0 | 2.0 |
| 9 | Have agents write ADRs as the project goes, so new sessions learn the intent and flag conflicts | context_memory | 10.0 | 4×5×0.5÷1 = 10.0 | 1.5 |
| 10 | Build one usage and cost board across subscriptions and loops | cost | 10.0 | 4×5×1.0÷2 = 10.0 | 3.5 |
| 11 | Route private material only to private or local models, and redact diffs before cloud review | sandbox_security | 10.0 | 4×5×1.0÷2 = 10.0 | 3.5 |
| 12 | End sessions with a close-out routine that writes hints into AGENTS.md, aimed at what frustrated you most | context_memory | 10.0 | 4×5×0.5÷1 = 10.0 | 1.0 |
| 13 | AI code review almost always finds something, even straight after fixes, so set a stop rule | testing_verification | 10.0 | 4×5×0.5÷1 = 10.0 | 1.0 |
| 14 | Without up-front design, agents drift into 'productivity porn': reports, plans and evidence packs with nothing implemented | tickets_planning | 10.0 | 4×5×0.5÷1 = 10.0 | 1.0 |
| 15 | Make any prompt you run often a skill and keep refining it | prompting_skills | 9.6 | 3×4×0.8÷1 = 9.6 | 2.0 |
| 16 | Human attention caps parallelism at about 3-6 sessions | skeptic_wellbeing | 9.0 | 3×3×1.0÷1 = 9.0 | 4.5 |
| 17 | Make workflows mostly deterministic scripts with agents only as fallbacks, harden them on each failure, and make them resumable | orchestration | 8.3 | 5×5×1.0÷3 = 8.3 | 3.0 |
| 18 | Models still write poor prose, so humans or strong models should own final text and humans shouldn't have to read slop | prompting_skills | 8.3 | 5×5×1.0÷3 = 8.3 | 4.0 |
| 19 | Evaluate custom orchestration against the vanilla harness, a locked-down baseline or your own past sessions, not leaderboards | testing_verification | 8.3 | 5×5×1.0÷3 = 8.3 | 5.0 |
| 20 | Cheap open models now cost very little, with concrete figures | cost | 8.0 | 4×4×1.0÷2 = 8.0 | 6.0 |
| 21 | Use GitHub issues as the hand-off from a strong planner to a cheap scheduled executor | tickets_planning | 8.0 | 4×5×0.8÷2 = 8.0 | 2.5 |
| 22 | 5.5-era models need fewer skills, guardrails and organisation structures | harness_choice | 8.0 | 4×4×1.0÷2 = 8.0 | 4.0 |
| 23 | Keep a version-controlled memory folder (LOG, HANDOFF, DECISIONS, plan folder) and one state file per repo kept current by hooks | context_memory | 8.0 | 4×5×0.8÷2 = 8.0 | 2.0 |
| 24 | Spec-first: no drafting until the spec is unambiguous; Vision.md, then Features.md, then Tasks.md | tickets_planning | 8.0 | 4×4×1.0÷2 = 8.0 | 5.0 |
| 25 | Agents commit inside the sandbox; only the host or human pushes | sandbox_security | 8.0 | 4×4×1.0÷2 = 8.0 | 4.0 |
| 26 | Use different alerts for 'task finished' and 'agent needs an answer' | voice_ui | 7.5 | 3×5×0.5÷1 = 7.5 | 1.5 |
| 27 | Broad skills and tool access poison context; add a switch to ignore bloated repo instructions | context_memory | 6.4 | 4×4×0.8÷2 = 6.4 | 2.0 |
| 28 | Cheap inter-agent channels are enough: a shared .md file, tmux send-keys, or sessions messaging each other directly | orchestration | 6.0 | 3×4×1.0÷2 = 6.0 | 4.0 |
| 29 | Keep remote control running in every project so phone apps can drive real machines | session_mgmt | 6.0 | 3×4×1.0÷2 = 6.0 | 3.0 |
| 30 | Have your agent audit your setup against a curated list of 100 tips | prompting_skills | 6.0 | 3×4×0.5÷1 = 6.0 | 0.5 |
| 31 | One AGENTS.md line, 'answer me like a Vulcan', kills verbose and sycophantic tone | prompting_skills | 6.0 | 3×4×0.5÷1 = 6.0 | 1.0 |
| 32 | Gate phases as binary CLEAR or DISCREPANCY, never numeric scores, and use fresh-eyed reviewers | testing_verification | 5.0 | 4×5×0.5÷2 = 5.0 | 1.0 |
| 33 | Treat tickets as the human-agent interface: questions come back in tickets and side findings become new tickets | tickets_planning | 5.0 | 4×5×0.5÷2 = 5.0 | 1.0 |
| 34 | A pm-intake agent checks findings against the roadmap and batches them into a daily digest for bulk approve or deny, later auto-approving whole classes | orchestration | 5.0 | 4×5×0.5÷2 = 5.0 | 1.0 |
| 35 | 'Build the builder, not the feature': when output is off, fix the orchestrator and prompts rather than the code (but watch for overfitting) | orchestration | 5.0 | 4×5×0.5÷2 = 5.0 | 1.0 |
| 36 | Mechanical gates in the harness, such as no remote git push without prior approval, and one scripting language only | sandbox_security | 5.0 | 4×5×0.5÷2 = 5.0 | 1.0 |
| 37 | Parallelise across separate projects, not within one (Amdahl's law) | orchestration | 4.8 | 3×4×0.8÷2 = 4.8 | 2.5 |
| 38 | Kanban as plain files in the repo, with dependencies and a 'ready' query for director agents | tickets_planning | 4.8 | 3×4×0.8÷2 = 4.8 | 2.5 |
| 39 | Overnight research or builds distilled into a package to read in the morning | personal_agents | 4.8 | 3×4×0.8÷2 = 4.8 | 2.0 |
| 40 | Nonstop agent building feels like addiction and risks burnout | skeptic_wellbeing | 4.5 | 3×3×1.0÷2 = 4.5 | 4.0 |
| 41 | Loop implementer subagents with clean-context reviewer subagents until no serious issues remain | multi_model_review | 4.0 | 4×4×0.5÷2 = 4.0 | 1.0 |
| 42 | Give agents scoped, temporary or read-only credentials per task, and per-chat git credentials for traceability | sandbox_security | 4.0 | 4×3×1.0÷3 = 4.0 | 4.0 |
| 43 | Budget a hands-on clean-up and hardening pass after fleet work, because isolated models produce a pastiche | testing_verification | 4.0 | 4×4×0.5÷2 = 4.0 | 1.0 |
| 44 | Push-to-talk voice with an intentional turn; local dictation; voice ideation while driving | voice_ui | 4.0 | 3×4×1.0÷3 = 4.0 | 3.0 |
| 45 | When limits bite, study consumption data and turn the biggest token sinks into deterministic code | cost | 3.3 | 4×5×0.5÷3 = 3.3 | 1.0 |
| 46 | Dogfood with personas: blank-slate new users plus persistent returning users, who give much better feedback | testing_verification | 3.3 | 4×5×0.5÷3 = 3.3 | 1.0 |
| 47 | Cache reviews pinned to the commit hash and use an AST-diff after a rebase to decide whether to reuse them | multi_model_review | 3.3 | 4×5×0.5÷3 = 3.3 | 1.0 |
| 48 | Spend leftover subscription capacity on queued improvements before the reset | cost | 3.3 | 4×5×0.5÷3 = 3.3 | 1.0 |
| 49 | Don't trust a harness-controlled sandbox: Claude has been seen disabling its own, so wrap it externally | sandbox_security | 3.2 | 4×3×0.8÷3 = 3.2 | 2.0 |
| 50 | Keep an open model as a fallback for refusals | models_routing | 3.0 | 3×2×1.0÷2 = 3.0 | 5.0 |
| 51 | Automate quota-aware provider switching or drain the account that resets soonest | cost | 3.0 | 3×3×1.0÷3 = 3.0 | 3.0 |
| 52 | Sessions that message each other freely hand out unrelated tasks, and you lose track | orchestration | 3.0 | 3×4×0.5÷2 = 3.0 | 1.0 |
| 53 | Have the agent build dedicated review pages for visual output instead of reading code | testing_verification | 3.0 | 3×4×0.5÷2 = 3.0 | 1.0 |
| 54 | Lower effort and weaker models are often better aligned; top models are worth it mainly for review | models_routing | 3.0 | 3×4×0.5÷2 = 3.0 | 1.0 |
| 55 | A strong model does exploratory and regression testing in a real browser, looped until clean | testing_verification | 2.7 | 4×4×0.5÷3 = 2.7 | 1.0 |
| 56 | Always-on personal agents dwindle into digest bots or 'just a cronjob' | personal_agents | 2.4 | 2×3×0.8÷2 = 2.4 | 2.5 |

1. **Reset context with a HANDOFF.md summary instead of relying on compaction, and keep context fill low**  ([#50375342](https://news.ycombinator.com/item?id=50375342), [#50378847](https://news.ycombinator.com/item?id=50378847), [#50375856](https://news.ycombinator.com/item?id=50375856), [#50379612](https://news.ycombinator.com/item?id=50379612), [#50381009](https://news.ycombinator.com/item?id=50381009))
2. **Make the main thread a pure coordinator that never implements**  ([#50375347](https://news.ycombinator.com/item?id=50375347), [#50376058](https://news.ycombinator.com/item?id=50376058), [#50376582](https://news.ycombinator.com/item?id=50376582))
3. **Subagents are the quickest way to burn limits; use them for map-reduce-shaped tasks**  ([#50373445](https://news.ycombinator.com/item?id=50373445), [#50373364](https://news.ycombinator.com/item?id=50373364), [#50376279](https://news.ycombinator.com/item?id=50376279))
4. **Cross-vendor review by default: one provider authors, another reviews, with more providers added for critical work** Includes calling Codex review from inside the Claude CLI and running Codex as a pre/post-PR hook. ([#50370886](https://news.ycombinator.com/item?id=50370886), [#50373001](https://news.ycombinator.com/item?id=50373001), [#50373589](https://news.ycombinator.com/item?id=50373589), [#50373463](https://news.ycombinator.com/item?id=50373463), [#50376463](https://news.ycombinator.com/item?id=50376463), [#50376390](https://news.ycombinator.com/item?id=50376390))
5. **Plan with a strong model and execute with a cheap one** gregwebs: Claude plans, Codex reviews, DeepSeek implements, for under $100/mo, about 3x slower but low-defect. ([#50374549](https://news.ycombinator.com/item?id=50374549), [#50373974](https://news.ycombinator.com/item?id=50373974), [#50376454](https://news.ycombinator.com/item?id=50376454), [#50377195](https://news.ycombinator.com/item?id=50377195), [#50377387](https://news.ycombinator.com/item?id=50377387), [#50378856](https://news.ycombinator.com/item?id=50378856))
6. **Review in a fresh session driven by a fixed list of your own PR-review questions** 16 questions that mirror the human's own. Called a game changer for simpler, cleaner code. ([#50378899](https://news.ycombinator.com/item?id=50378899))
7. **Hide keys behind a credential-injecting proxy: no keys in the agent VM**  ([#50367803](https://news.ycombinator.com/item?id=50367803), [#50376836](https://news.ycombinator.com/item?id=50376836), [#50379377](https://news.ycombinator.com/item?id=50379377), [#50381875](https://news.ycombinator.com/item?id=50381875), [#50387654](https://news.ycombinator.com/item?id=50387654))
8. **Escalate a failing task up model tiers (flash, pro, heavy, frontier) until it is solved** An Opus coordinator does the classifying. contingencies uses the top model only when stuck or on a high-value step. ([#50375921](https://news.ycombinator.com/item?id=50375921), [#50374502](https://news.ycombinator.com/item?id=50374502))
9. **Have agents write ADRs as the project goes, so new sessions learn the intent and flag conflicts** stkni says it raised overall output quality and picked up proposed-but-unbuilt features. ([#50376262](https://news.ycombinator.com/item?id=50376262), [#50376451](https://news.ycombinator.com/item?id=50376451))
10. **Build one usage and cost board across subscriptions and loops**  ([#50373740](https://news.ycombinator.com/item?id=50373740), [#50374094](https://news.ycombinator.com/item?id=50374094), [#50376390](https://news.ycombinator.com/item?id=50376390), [#50376352](https://news.ycombinator.com/item?id=50376352))
11. **Route private material only to private or local models, and redact diffs before cloud review**  ([#50385740](https://news.ycombinator.com/item?id=50385740), [#50376538](https://news.ycombinator.com/item?id=50376538), [#50376810](https://news.ycombinator.com/item?id=50376810), [#50377307](https://news.ycombinator.com/item?id=50377307))
12. **End sessions with a close-out routine that writes hints into AGENTS.md, aimed at what frustrated you most**  ([#50375278](https://news.ycombinator.com/item?id=50375278))
13. **AI code review almost always finds something, even straight after fixes, so set a stop rule** Findings are often debatable or describe unreachable states. ([#50374732](https://news.ycombinator.com/item?id=50374732))
14. **Without up-front design, agents drift into 'productivity porn': reports, plans and evidence packs with nothing implemented**  ([#50381456](https://news.ycombinator.com/item?id=50381456))
15. **Make any prompt you run often a skill and keep refining it**  ([#50384236](https://news.ycombinator.com/item?id=50384236), [#50378336](https://news.ycombinator.com/item?id=50378336))
16. **Human attention caps parallelism at about 3-6 sessions**  ([#50373117](https://news.ycombinator.com/item?id=50373117), [#50370886](https://news.ycombinator.com/item?id=50370886), [#50373357](https://news.ycombinator.com/item?id=50373357), [#50376632](https://news.ycombinator.com/item?id=50376632), [#50375378](https://news.ycombinator.com/item?id=50375378))
17. **Make workflows mostly deterministic scripts with agents only as fallbacks, harden them on each failure, and make them resumable**  ([#50378157](https://news.ycombinator.com/item?id=50378157), [#50367326](https://news.ycombinator.com/item?id=50367326), [#50367587](https://news.ycombinator.com/item?id=50367587))
18. **Models still write poor prose, so humans or strong models should own final text and humans shouldn't have to read slop** Directly relevant to a content harness: GreenPT output stays a candidate and never becomes final prose. ([#50367589](https://news.ycombinator.com/item?id=50367589), [#50373357](https://news.ycombinator.com/item?id=50373357), [#50375084](https://news.ycombinator.com/item?id=50375084), [#50376087](https://news.ycombinator.com/item?id=50376087))
19. **Evaluate custom orchestration against the vanilla harness, a locked-down baseline or your own past sessions, not leaderboards**  ([#50379514](https://news.ycombinator.com/item?id=50379514), [#50379686](https://news.ycombinator.com/item?id=50379686), [#50375145](https://news.ycombinator.com/item?id=50375145), [#50378628](https://news.ycombinator.com/item?id=50378628), [#50380023](https://news.ycombinator.com/item?id=50380023))
20. **Cheap open models now cost very little, with concrete figures** 1B tokens used 7% of a $10 plan; ~$20/week at a 99% cache hit rate; $4.37 in 30 days; a long review cost about $0.033. ([#50381117](https://news.ycombinator.com/item?id=50381117), [#50375427](https://news.ycombinator.com/item?id=50375427), [#50385251](https://news.ycombinator.com/item?id=50385251), [#50376778](https://news.ycombinator.com/item?id=50376778), [#50377633](https://news.ycombinator.com/item?id=50377633), [#50375326](https://news.ycombinator.com/item?id=50375326))
21. **Use GitHub issues as the hand-off from a strong planner to a cheap scheduled executor**  ([#50373974](https://news.ycombinator.com/item?id=50373974), [#50374380](https://news.ycombinator.com/item?id=50374380), [#50374094](https://news.ycombinator.com/item?id=50374094))
22. **5.5-era models need fewer skills, guardrails and organisation structures**  ([#50378434](https://news.ycombinator.com/item?id=50378434), [#50379944](https://news.ycombinator.com/item?id=50379944), [#50381456](https://news.ycombinator.com/item?id=50381456), [#50373351](https://news.ycombinator.com/item?id=50373351))
23. **Keep a version-controlled memory folder (LOG, HANDOFF, DECISIONS, plan folder) and one state file per repo kept current by hooks**  ([#50375274](https://news.ycombinator.com/item?id=50375274), [#50377952](https://news.ycombinator.com/item?id=50377952))
24. **Spec-first: no drafting until the spec is unambiguous; Vision.md, then Features.md, then Tasks.md**  ([#50382792](https://news.ycombinator.com/item?id=50382792), [#50380633](https://news.ycombinator.com/item?id=50380633), [#50378376](https://news.ycombinator.com/item?id=50378376), [#50376782](https://news.ycombinator.com/item?id=50376782), [#50380703](https://news.ycombinator.com/item?id=50380703))
25. **Agents commit inside the sandbox; only the host or human pushes**  ([#50379089](https://news.ycombinator.com/item?id=50379089), [#50379377](https://news.ycombinator.com/item?id=50379377), [#50379206](https://news.ycombinator.com/item?id=50379206), [#50379048](https://news.ycombinator.com/item?id=50379048))
26. **Use different alerts for 'task finished' and 'agent needs an answer'**  ([#50373796](https://news.ycombinator.com/item?id=50373796), [#50378479](https://news.ycombinator.com/item?id=50378479))
27. **Broad skills and tool access poison context; add a switch to ignore bloated repo instructions**  ([#50380583](https://news.ycombinator.com/item?id=50380583), [#50375302](https://news.ycombinator.com/item?id=50375302))
28. **Cheap inter-agent channels are enough: a shared .md file, tmux send-keys, or sessions messaging each other directly**  ([#50373684](https://news.ycombinator.com/item?id=50373684), [#50388928](https://news.ycombinator.com/item?id=50388928), [#50373985](https://news.ycombinator.com/item?id=50373985), [#50367876](https://news.ycombinator.com/item?id=50367876))
29. **Keep remote control running in every project so phone apps can drive real machines**  ([#50374380](https://news.ycombinator.com/item?id=50374380), [#50377004](https://news.ycombinator.com/item?id=50377004), [#50376177](https://news.ycombinator.com/item?id=50376177))
30. **Have your agent audit your setup against a curated list of 100 tips**  ([#50378479](https://news.ycombinator.com/item?id=50378479))
31. **One AGENTS.md line, 'answer me like a Vulcan', kills verbose and sycophantic tone**  ([#50380005](https://news.ycombinator.com/item?id=50380005))
32. **Gate phases as binary CLEAR or DISCREPANCY, never numeric scores, and use fresh-eyed reviewers**  ([#50380633](https://news.ycombinator.com/item?id=50380633))
33. **Treat tickets as the human-agent interface: questions come back in tickets and side findings become new tickets**  ([#50376058](https://news.ycombinator.com/item?id=50376058), [#50384746](https://news.ycombinator.com/item?id=50384746))
34. **A pm-intake agent checks findings against the roadmap and batches them into a daily digest for bulk approve or deny, later auto-approving whole classes**  ([#50385555](https://news.ycombinator.com/item?id=50385555))
35. **'Build the builder, not the feature': when output is off, fix the orchestrator and prompts rather than the code (but watch for overfitting)**  ([#50377582](https://news.ycombinator.com/item?id=50377582))
36. **Mechanical gates in the harness, such as no remote git push without prior approval, and one scripting language only**  ([#50367557](https://news.ycombinator.com/item?id=50367557))
37. **Parallelise across separate projects, not within one (Amdahl's law)**  ([#50375921](https://news.ycombinator.com/item?id=50375921), [#50377263](https://news.ycombinator.com/item?id=50377263), [#50376262](https://news.ycombinator.com/item?id=50376262))
38. **Kanban as plain files in the repo, with dependencies and a 'ready' query for director agents**  ([#50374498](https://news.ycombinator.com/item?id=50374498), [#50374774](https://news.ycombinator.com/item?id=50374774), [#50375046](https://news.ycombinator.com/item?id=50375046))
39. **Overnight research or builds distilled into a package to read in the morning** chasd00: a daily blog of status and decision reasons tracks an unattended agent well. ([#50385812](https://news.ycombinator.com/item?id=50385812), [#50380777](https://news.ycombinator.com/item?id=50380777))
40. **Nonstop agent building feels like addiction and risks burnout**  ([#50373236](https://news.ycombinator.com/item?id=50373236), [#50390416](https://news.ycombinator.com/item?id=50390416), [#50375890](https://news.ycombinator.com/item?id=50375890), [#50378487](https://news.ycombinator.com/item?id=50378487))
41. **Loop implementer subagents with clean-context reviewer subagents until no serious issues remain**  ([#50379808](https://news.ycombinator.com/item?id=50379808))
42. **Give agents scoped, temporary or read-only credentials per task, and per-chat git credentials for traceability**  ([#50375302](https://news.ycombinator.com/item?id=50375302), [#50383038](https://news.ycombinator.com/item?id=50383038), [#50379596](https://news.ycombinator.com/item?id=50379596), [#50385251](https://news.ycombinator.com/item?id=50385251))
43. **Budget a hands-on clean-up and hardening pass after fleet work, because isolated models produce a pastiche**  ([#50375606](https://news.ycombinator.com/item?id=50375606))
44. **Push-to-talk voice with an intentional turn; local dictation; voice ideation while driving**  ([#50381098](https://news.ycombinator.com/item?id=50381098), [#50374502](https://news.ycombinator.com/item?id=50374502), [#50368526](https://news.ycombinator.com/item?id=50368526))
45. **When limits bite, study consumption data and turn the biggest token sinks into deterministic code**  ([#50374764](https://news.ycombinator.com/item?id=50374764))
46. **Dogfood with personas: blank-slate new users plus persistent returning users, who give much better feedback**  ([#50385555](https://news.ycombinator.com/item?id=50385555))
47. **Cache reviews pinned to the commit hash and use an AST-diff after a rebase to decide whether to reuse them**  ([#50378157](https://news.ycombinator.com/item?id=50378157))
48. **Spend leftover subscription capacity on queued improvements before the reset**  ([#50380990](https://news.ycombinator.com/item?id=50380990))
49. **Don't trust a harness-controlled sandbox: Claude has been seen disabling its own, so wrap it externally**  ([#50380164](https://news.ycombinator.com/item?id=50380164), [#50383403](https://news.ycombinator.com/item?id=50383403))
50. **Keep an open model as a fallback for refusals**  ([#50374417](https://news.ycombinator.com/item?id=50374417), [#50374455](https://news.ycombinator.com/item?id=50374455), [#50374764](https://news.ycombinator.com/item?id=50374764), [#50375312](https://news.ycombinator.com/item?id=50375312), [#50376505](https://news.ycombinator.com/item?id=50376505))
51. **Automate quota-aware provider switching or drain the account that resets soonest**  ([#50378856](https://news.ycombinator.com/item?id=50378856), [#50378737](https://news.ycombinator.com/item?id=50378737), [#50374678](https://news.ycombinator.com/item?id=50374678), [#50379150](https://news.ycombinator.com/item?id=50379150))
52. **Sessions that message each other freely hand out unrelated tasks, and you lose track**  ([#50376476](https://news.ycombinator.com/item?id=50376476))
53. **Have the agent build dedicated review pages for visual output instead of reading code**  ([#50382792](https://news.ycombinator.com/item?id=50382792))
54. **Lower effort and weaker models are often better aligned; top models are worth it mainly for review**  ([#50377284](https://news.ycombinator.com/item?id=50377284))
55. **A strong model does exploratory and regression testing in a real browser, looped until clean**  ([#50376216](https://news.ycombinator.com/item?id=50376216))
56. **Always-on personal agents dwindle into digest bots or 'just a cronjob'**  ([#50376601](https://news.ycombinator.com/item?id=50376601), [#50377290](https://news.ycombinator.com/item?id=50377290), [#50370886](https://news.ycombinator.com/item?id=50370886))

## Where the thread disagrees

- **Do swarms and multi-agent orchestration pay off?** Yes: Yes: coordinators, fleets and chief-of-staff agents raise throughput (glennfiedler #50375606, jeswin #50373324, dgunay #50375407, 2001zhaozhao #50373432). No: No: swarms waste tokens, a single human in the loop beats orchestration, and inter-session messaging becomes chaos (YuechenLi #50375205, joegibbs #50376476, PAndreew #50377956, SOLAR_FIELDS #50379514). Verdict for you: Use a narrow coordinator plus an independent reviewer. No wide swarms for John; his two-worker cap stands.
- **Are skills still useful?** Yes: Yes: make frequent prompts into skills; MCP-backed skills transformed a workflow (jeffyaw #50384236, parkersweb #50378336, ctolsen #50367326). No: Less so: little use when switching stacks; broad skills poison context (thefourthchime #50367037, bartread #50378288, RamblingCTO #50380583). Verdict for you: Keep a few narrow, refined skills and promote proven ones to scripts. Prune broad ones.
- **Persist agent context, or re-explain each time?** Yes: Persist: HANDOFF, DECISIONS, ADRs, state files, close-out notes (sheepscreek #50375342, bottom999mottob #50375274, tritondev #50376262). No: Re-explain: it forces better thinking about architecture; code should be self-evident (hypfer #50376204). Verdict for you: Persist, but keep the files short and decision-focused, which captures hypfer's point.
- **Are open models via PAYG cheaper than subscriptions?** Yes: Yes: about 1/20th the cost; 1B tokens for 7% of a $10 plan (creativeSlumber #50378366, ggregoire #50381117). No: Not in practice: more expensive than a Claude subscription; DS4.1 Flash on the high side (jpardoe #50380381, jeffyaw #50384114, scosman #50380185). Verdict for you: Measure per task. For John the question is moot: GreenPT is hard-capped, so use the cap fully for bounded work.
- **Minimal setup or heavy protocol?** Yes: Minimal: vanilla Claude Code with few skills; fancy setups get abandoned (leofree #50380407, nonethewiser #50380782, Aozora7 #50373351). No: Heavy: phased protocols with review panels and deterministic workflows work well (cpobuda #50380633, poelzi #50378157). Verdict for you: Make it heavy only where it is deterministic and cheap to run. Prove the rest against vanilla with a bake-off.
- **Privacy of cloud agents** Yes: No worse than running Claude/Codex locally (iainmerrick #50377537). No: Worse: the provider clones the full source and needs write/Actions access (OJFord #50377189, #50383635). Verdict for you: For repos already on GitHub, cloud sessions are fine. Keep docs/private out of cheap third-party providers with a mechanical check.
- **Should you tell the model to use subagents?** Yes: Yes: 'use subagents as applicable', 'use sonnet for simpler tasks' (mceachen #50375851, chris1993 #50372070, sillysaurusx #50373445). No: No: let it decide; over-optimising saves nothing (willio58 #50373767). Verdict for you: Let the model decide, inside John's declared delegation ceiling.
- **Opus 5.5 or Fable?** Yes: Opus solves nearly everything; the main difference is price (nedt #50378628, willio58 #50373208). No: Fable goes deeper on obscure analysis and real development (felixgallo #50380023, tcdent #50374230). Verdict for you: Benchmark on your own tasks. Reserve the premium route for the explicit premium command.
- **Is cheap DeepSeek flash output correct enough?** Yes: 'Pretty much always correct' and keeps you in flow (TheArcane #50376062). No: Lots of approximately-correct text; frontier models are concise and correct (haizhung #50376087); open-model prose is insufferable (guhcampos #50373357). Verdict for you: Good enough for extraction and mechanical work. Not for final content prose.
- **Is lightweight isolation enough?** Yes: A dedicated OS user or the harness's bubblewrap is a fair compromise (kikdij #50379089, tikkabhuna #50379187). No: No: Claude disables its own sandbox; use an external VM or microVM (rdg1991 #50380164, f53d #50383403, thehours #50379505). Verdict for you: Use external isolation. John's cloud sessions and push hook already provide it.
- **Is nonstop agent building healthy?** Yes: 'You are doing everything right' (glennfiedler #50374802). No: It is addiction and will cause burnout (LittleBox #50390416, pavas #50375890, bkaae #50378487). Verdict for you: Keep turn, timeout and width caps. They protect the human as well as the budget.
- **Personal agent platforms** Yes: Life-integrated and valuable (Quibblingeek #50373248, robgough #50368640, vekker #50377455). No: Unstable, just a cronjob, little real use (sadilek #50370886, browningstreet #50373974, jedisct1 #50376601). Verdict for you: Watch only. Not part of the content harness.
- **Do model differences still matter?** Yes: Frontier models have reached 'good enough' parity (darkamaul #50376908, asim #50377263). No: Big differences in speed, price and prose quality (brabel #50376352, felixgallo #50380023). Verdict for you: They matter for prose and price, which are exactly the axes a content harness routes on.

## Gold quotes

> “I'd say the biggest trick is just to tell it what complete looks like.” — thefourthchime #50367037

> “I generally start a workflow with a simple skill and if it proves useful I like to make it deterministic if possible. Models be dumb sometimes.” — ctolsen #50367326

> “All of these gas towns and no one running evals to compare to the vanilla harness. AI is very good at making one feel like they are being productive” — SOLAR_FIELDS #50379514

> “If a card fails at a particular tier, it's going to get escalated up tiers until it gets sorted.” — glennfiedler #50375921

> “I find that using nova-bus to coordinate multiple model/harness review of codebase in very effective at increasing code quality. Each model sees things the others don't.” — glennfiedler #50375606

> “review is cached, but the review is pinned to the commit hash. When restarted and rebase is on, a ast-diff is generated to check if the review can be reused.” — poelzi #50378157

> “Reset your context frequently instead of only relying on compaction.” — sheepscreek #50375342

> “Being forced to re-explain stuff to the LLM is good, actually, as that way, one actually thinks about the architecture, choices and limitations.” — hypfer #50376204

> “What's funny though is that it almost always inevitably finds something wrong, even if you just ran it in another window and fixed everything it found.” — smashed #50374732

> “I've discovered that giving Claude questions to ask during code review improves things quite a bit.” — lgunsch #50378899

> “a phase is either CLEAR (GREEN) or DISCREPANCY (RED) — never a numeric score” — cpobuda #50380633

> “When I hit my limits for the week, I spend the remainder of the waiting time going over the framework data to see what are my largest sources of consumption” — Fordec #50374764

> “I don't like making other people read AI slop, but I don't mind having AIs read it.” — martincsweiss #50375084

> “GLM, Qwen and Deepseek are incredible tool callers, but their prose is insufferable.” — guhcampos #50373357

> “I think as the models get better, the organization structures need less attention.” — dcferreira #50379944

> “It is probably at least 3x slower than just asking for an implementation, but defects cost time and money later.” — gregwebs #50378856

> “it can wander into 'productivity porn' territory where it's just creating reams of reports, plans, or 'evidence packs' and nothing real gets implemented.” — siliconc0w #50381456

> “I can do 5 things concurrently for about a day max. 3 things concurrently all week and my weekends are spent untangling my brain.” — fhub #50373117

> “Just know that there’s no quicker way to hit your limits than to use subagents.” — sillysaurusx #50373445

> “My ABSOLUTE rule is NO KEYS IN THE VM.” — allen-munsch #50387654

> “Claude frequently has decided to disable its own sandbox when I've had it running so I absolutely do not trust their implementation.” — rdg1991 #50380164

> “The persistent agents remember why things are as they are without having to look everything up and their feedback is generally much better than a blank slate user.” — mschwarz #50385555

> “My approach is to build the builder rather than the feature.” — sebra #50377582

> “This thread is super biased by the power users, they are the most excited to share” — ex-aws-dude #50375972

## The Reddit summary, checked against all 645 comments

Source: r/AI_Agents post by michaelTM_ai, "cheap open models at home, frontier as the second opinion, and nobody trusts the agent platforms". The poster says they read "the top 45 or so" of about 475 comments. This check uses all 645 comments and 388 top-level threads. Counts are the number of comments that mention a term, found with a script search of `thread.json`. No model was used for the counting.

| # | Reddit claim | Verdict | Evidence |
|---|---|---|---|
| 1 | DeepSeek Flash came up more than any frontier model in personal setups | **Partly true** | DeepSeek appears in 88 comments, the most of any open model (Qwen 55, GLM 46, Kimi 14). It is level with Opus (85) and well behind GPT/Codex (152) and Claude Code (134). Keyword counts cannot separate personal setups from work setups. |
| 2 | $10 OpenCode Go plan, or pay as you go through OpenRouter | **True** | OpenCode Go appears in 29 comments and OpenRouter in 66. |
| 3 | "Never run out of tokens" | **True** | AaronAPU #50368566: "I never come close to running out of tokens because I still do code reviews often enough to throttle usage." The reason is that reviewing the code themselves slows their usage, not that the plan is cheap. |
| 4 | Frontier models are becoming the second opinion | **True, but a minority** | Examples: ActionHank #50379104 makes an "occasional call out to claude for a review", drbscl #50367676 uses one "mostly for review, second opinion", Xonzo #50378776 uses "Sol 6.1 xHigh for planning/review", and codingbear #50367207 uses Claude "for tricky bits". More commenters go the other way and let a single Opus 5.5 session do everything (thefourthchime #50367037, l9o #50368019, FrameworkFred #50379612). |
| 5 | Harnesses are getting smaller; the top comment deleted his skills, set Opus to medium and tells it what done looks like | **True** | thefourthchime #50367037, which is the first top-level comment: "I got rid of all my skills and just set it to medium… the biggest trick is just to tell it what complete looks like." pi appears in 87 comments and OpenCode in 91. |
| 6 | Almost nobody trusts all-in-one agent platforms; OpenClaw and Hermes "fell apart on real work" | **Half wrong** | OpenClaw (35 comments) is mostly "tried it, dropped it": nkotov, vekker, SkidVis, leofree, egrm and others. **Hermes (53 comments) has a loyal user base**, mostly as an always-on personal assistant on a Mac Mini or homelab that people reach by Telegram. browningstreet calls it "core tech for me", and vekker, virpo, Xonzo, diseasedyak, monch1962, hestefisk and ddarolfi are also users. ActionHank says "Hermes Kanban works stupidly well". |
| 7 | Orchestration is still a human with 3–5 terminal panes | **True** | phillc73 #50367557 runs "a multipane Zellij setup… Orchestration is still human in the loop", m_w_ #50379312 runs 5–6 sessions, anigbrowl #50375427 runs 3–4 projects, and marshalla runs at most 3. tmux appears in 17 comments. |
| 8 | Someone types junk into idle sessions every 30–45 minutes so the cache doesn't expire | **True** | marshalla #50367399 types "silly things into some of them every 30-45 min so they don't expire or auto-compact". |
| 9 | "Bragging about multiple subscriptions without saying what they use them for" | **True** | ChrisRR #50367618, quoted word for word. |
| 10 | "GLM flash for coordination, deepseek for coding and GLM for adversarial review: the part worth copying" | **True** | phillc73 #50367557: "GLM5.3 Flash for general chat and co-ordination… Deepseek 1017 for most coding… GLM5.3 for adversarial batteries and documentation." ActionHank #50379104 is close: "Hermes + GLM 5.3 Flash for orchestration, omp + Deepseek 4.1 Flash for coding, occasional call out to claude for a review." |

**Score: 7 true, 2 partly true, 1 half wrong.** The post is a fair summary of the top of the thread. Its one real error is lumping Hermes in with OpenClaw.

### What the Reddit summary means for John's harness

- **Claim 10 is your three-provider design**, found independently by someone else. phillc73 also uses mechanical gates, for example "no remote git pushes without explicit prior approval", which match your PreToolUse hooks. Worth copying from them: **one written table of roles and models**, with a single line per role: coordination, coding, adversarial review and documentation. Today your routes (bounded_extraction, standard_reasoning, highest_reasoning) say how hard a job is, not which job it is.
- **Claim 8 costs you money too.** Your Claude Code sessions use a 1-hour prompt cache, so typing filler into them is wasted effort. Keep sessions short and hand over through GitHub issues, which you already do.
- **Claim 6: Hermes is the one platform people keep.** If you ever want a phone-reachable assistant that is always on, Hermes on a spare machine is the pattern the thread recommends. It sits outside your packet rules, so it would be a separate experiment.


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


## Projects worth a look, top 15 by v2

All 111 are in data/projects_v2.json and on the page, with screenshots.

| # | Project | Camp | v2 | Working | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | [Handy](https://handy.computer) | Ops | 9.0 | 3×3×1.0÷1 = 9.0 | phone dictation already covers most of it |
| 2 | [Agent patterns graphs](https://graphs.univerlab.org/patterns) | Pipelines | 6.0 | 3×4×0.5÷1 = 6.0 | pattern catalogue to read |
| 3 | [mattpocock/skills](https://github.com/mattpocock/skills) | Harnesses | 6.0 | 3×4×0.5÷1 = 6.0 | skill examples to copy |
| 4 | [techaddo](https://techaddo.com/posts/ai-agentic-setups) |  | 6.0 | 3×4×0.5÷1 = 6.0 | running digest of this thread |
| 5 | [eamonn](https://eamonnsullivan.co.uk/posts/2026-10-20-retirement/) |  | 6.0 | 3×4×0.5÷1 = 6.0 | clear write-up of a cheap multi-model setup |
| 6 | [Claude Code TPP](https://photostructure.com/coding/claude-code-tpp/) | Context | 5.0 | 4×5×0.5÷2 = 5.0 | same idea as HANDOFF.md |
| 7 | [kiro](https://kiro.dev/docs/specs/) |  | 4.5 | 3×3×1.0÷2 = 4.5 | spec-driven docs |
| 8 | [skills-sdlc](https://github.com/gregwebs/skills-sdlc) | Pipelines | 4.0 | 4×4×0.5÷2 = 4.0 | SDLC skills to adapt into packets |
| 9 | [LLM usage page](https://a.l3x.in/usage) | Ops | 4.0 | 4×4×0.5÷2 = 4.0 | one page of balances: the cost board |
| 10 | [How I use agents for work](https://dcferreira.com/post/2026-10-how-i-use-agents/) | Context | 3.0 | 2×3×0.5÷1 = 3.0 |  |
| 11 | [Agent Kitchen](https://stack.yiin.lt) | Context | 3.0 | 2×3×0.5÷1 = 3.0 |  |
| 12 | [OpenSpec](https://openspec.dev) | Pipelines | 3.0 | 3×4×0.5÷2 = 3.0 | spec before build, like a packet |
| 13 | [Follow the Money](https://helyn.com/follow-the-money) | Pipelines | 3.0 | 3×4×0.5÷2 = 3.0 | reproducible process spec for content work |
| 14 | [melious](https://melious.ai) |  | 3.0 | 3×2×1.0÷2 = 3.0 | phillc73 provider: 4th provider, John decides |
| 15 | [caudradecisions](https://caudra.ai/features/decisions/) |  | 3.0 | 3×4×0.5÷2 = 3.0 | decision log: same idea as DECISIONS.md |

## Also linked in the thread (not screenshotted)

67 more links the synthesis found, sorted by its 1–5 inspiration rating. Not scored with v2.

| Link | Kind | Inspiration | What | Comment |
| --- | --- | --- | --- | --- |
| [Superintendent]((none given)) | cost | 4 | Drives T3 Code to spend spare subscription capacity on queued improvements | [#50380990](https://news.ycombinator.com/item?id=50380990) |
| [stonker bot daily posts](https://stonker.jettdigital.app/ (access-key parameter in original link omitted)) | personal_agents | 3 | Daily blog written by an unattended portfolio agent | [#50383211](https://news.ycombinator.com/item?id=50383211) |
| [T3 Code](T3.codes) | session_control | 3 | Unified front-end over Claude Code, Codex and Pi with remote environments, snooze and diffs | [#50378013](https://news.ycombinator.com/item?id=50378013) |
| [Open Chamber]((none given)) | tickets | 3 | OpenCode UI with a task plugin giving each ticket a fresh context | [#50376216](https://news.ycombinator.com/item?id=50376216) |
| [Requesty]((none given)) | cost | 3 | Model gateway dashboard comparing speed and cost | [#50376352](https://news.ycombinator.com/item?id=50376352) |
| [oh-my-pi prewalk]((none given)) | routing | 3 | Pairs a planner model with an executor model | [#50376454](https://news.ycombinator.com/item?id=50376454) |
| [OpenRig]((none given)) | orchestration | 3 | Role-based 'rigs' of Codex/Claude seats; dogfood persona rig and pm-intake seat per founder (#50385555) | [#50377449](https://news.ycombinator.com/item?id=50377449) |
| [Vercel agent-browser]((none given)) | verification | 3 | Browser agent skill used for persona dogfood testing | [#50385555](https://news.ycombinator.com/item?id=50385555) |
| [meat_proxy]((none given)) | sandbox | 3 | Pulls the agent user's commits and pushes to bare repos acting as CI | [#50379089](https://news.ycombinator.com/item?id=50379089) |
| [Agent control room]((none given)) | session_control | 3 | Rails control room with one queue of items needing the human | [#50379826](https://news.ycombinator.com/item?id=50379826) |
| [Claude code-review wrapper]((none given)) | review | 3 | Lets Claude call Codex/Grok/GLM for review | [#50380522](https://news.ycombinator.com/item?id=50380522) |
| [Voice interface for Claude Code]((none given)) | voice | 3 | Push-to-talk headset turn with kokoro TTS and Parakeet ASR | [#50381098](https://news.ycombinator.com/item?id=50381098) |
| [Claude Code Desktop docs](https://code.claude.com/docs/en/desktop) | harness | 2 | Docs for Claude Code Desktop | [#50368880](https://news.ycombinator.com/item?id=50368880) |
| [nono.sh](nono.sh) | sandbox | 2 | Sandbox with network/file limits and a key-hiding proxy | [#50367803](https://news.ycombinator.com/item?id=50367803) |
| [hoplite.sh](hoplite.sh) | sandbox | 2 | Cloud agent environment service | [#50384905](https://news.ycombinator.com/item?id=50384905) |
| [t3code video](https://www.youtube.com/watch?v=dLhcLqoff6k) | session_control | 2 | Video that convinced one user to switch to t3code | [#50376898](https://news.ycombinator.com/item?id=50376898) |
| [Netdata](https://github.com/netdata/netdata) | context | 2 | Observability platform; idea of sending LLM OTel traces there (author works there) | [#50375619](https://news.ycombinator.com/item?id=50375619) |
| [schema ROADMAP](https://github.com/mas-bandwidth/schema/blob/main/ROADMAP.md) | other | 2 | Roadmap for schema | [#50375943](https://news.ycombinator.com/item?id=50375943) |
| [fixed roadmap.sexp](https://github.com/mas-bandwidth/fixed/blob/main/docs/roadmap.sexp) | context | 2 | S-expression roadmap notes for agents | [#50386404](https://news.ycombinator.com/item?id=50386404) |
| [dreamcoder.ai](https://dreamcoder.ai) | harness | 2 | Own harness with tiling window manager | [#50375966](https://news.ycombinator.com/item?id=50375966) |
| [DeepSeek platform](https://platform.deepseek.com) | providers | 2 | DeepSeek API with off-peak pricing | [#50376062](https://news.ycombinator.com/item?id=50376062) |
| [ollama.com (cloud)](ollama.com) | providers | 2 | Hosted inference with cheap DeepSeek Flash | [#50376262](https://news.ycombinator.com/item?id=50376262) |
| [Paseo]((none given)) | session_control | 2 | Mobile/desktop UI and agent runtime for Claude Code/Codex | [#50376167](https://news.ycombinator.com/item?id=50376167) |
| [MLX-Serve + Clef]((none given)) | local_models | 2 | Local server with a routing model choosing a model per task | [#50376601](https://news.ycombinator.com/item?id=50376601) |
| [pi-deck / Pillish]((none given; unpublished)) | session_control | 2 | Pi in Emacs with a Herdr-like layer; do/delegate primitives | [#50376505](https://news.ycombinator.com/item?id=50376505) |
| [libvirt per-project VM CLI]((none given; not yet open-sourced)) | sandbox | 2 | Per-project VMs from copy-on-write golden images | [#50376357](https://news.ycombinator.com/item?id=50376357) |
| [Hetzner Inference API]((none given)) | providers | 2 | Currently free inference API used as a custom provider | [#50376941](https://news.ycombinator.com/item?id=50376941) |
| [agentcron.ai](agentcron.ai) | tickets | 2 | MCP kanban boards | [#50377430](https://news.ycombinator.com/item?id=50377430) |
| [Lab]((none given)) | session_control | 2 | Front-end for many chats with resume and central skill/MCP management | [#50378016](https://news.ycombinator.com/item?id=50378016) |
| [Hivemind]((none given)) | orchestration | 2 | Agent collaboration layer with file reservations and resource locks | [#50378016](https://news.ycombinator.com/item?id=50378016) |
| [drop](https://github.com/wrr/drop) | sandbox | 2 | Simple agent sandbox | [#50382618](https://news.ycombinator.com/item?id=50382618) |
| [Orca](onorca.dev) | session_control | 2 | Multi-worktree agent IDE/orchestrator with mobile app | [#50379643](https://news.ycombinator.com/item?id=50379643) |
| [Karajan]((none given)) | orchestration | 2 | Mac app exposing an MCP so the Claude app can start, stop and review agents | [#50379643](https://news.ycombinator.com/item?id=50379643) |
| [voiceio](voiceio.dev) | voice | 2 | FOSS Linux voice input with Parakeet | [#50380334](https://news.ycombinator.com/item?id=50380334) |
| [clawpatrol]((none given)) | sandbox | 2 | Action-approval rules and credentials layer for external APIs | [#50380252](https://news.ycombinator.com/item?id=50380252) |
| [Compound Engineering plugin]((none given)) | orchestration | 2 | Plugin used as the primary Claude-builds/Codex-reviews loop | [#50389282](https://news.ycombinator.com/item?id=50389282) |
| [Custom OWUI plugins]((none given)) | sandbox | 2 | Per-chat terminal grants and per-chat git credentials | [#50385251](https://news.ycombinator.com/item?id=50385251) |
| [Buzzpot](Buzzpot.app) | harness | 1 | Commenter's own app used as a harness | [#50367619](https://news.ycombinator.com/item?id=50367619) |
| [Cinnamon](getcinnamon.ai) | personal_agents | 1 | Own harness used by the family | [#50373135](https://news.ycombinator.com/item?id=50373135) |
| [Vekmem](www.vekmem.com) | harness | 1 | Harness for local and cloud models | [#50373561](https://news.ycombinator.com/item?id=50373561) |
| [Lex Fridman podcast (DHH episode)](https://lexfridman.com/podcast) | other | 1 | Episode on agentic engineering where Herdr came up | [#50373956](https://news.ycombinator.com/item?id=50373956) |
| [autofab]((none given; planned PyPI package)) | tickets | 1 | Planned spec-driven system on existing harnesses | [#50374261](https://news.ycombinator.com/item?id=50374261) |
| [Egzo]((none given; link in author's HN profile)) | sandbox | 1 | Orchestration, sandboxing and access management tool | [#50374549](https://news.ycombinator.com/item?id=50374549) |
| [Rufus](https://rufus.ie/en/) | sandbox | 1 | USB creator used for an offline Windows 11 agent VM | [#50375124](https://news.ycombinator.com/item?id=50375124) |
| [Windows 11 ISO download](https://www.microsoft.com/en-us/software-download/windows11) | other | 1 | Official Windows 11 ISO | [#50375124](https://news.ycombinator.com/item?id=50375124) |
| [Revo Uninstaller Pro (file-host link)](https://onefiles.net/9d170d01078634b5) | other | 1 | Third-party file-host download, not the vendor site; treat as untrusted | [#50375124](https://news.ycombinator.com/item?id=50375124) |
| [UniGetUI](https://devolutions.net/unigetui/) | other | 1 | Windows package manager GUI | [#50375124](https://news.ycombinator.com/item?id=50375124) |
| [fnm](https://github.com/Schniz/fnm) | other | 1 | Node version manager | [#50375124](https://news.ycombinator.com/item?id=50375124) |
| [jvms](https://github.com/ystyle/jvms) | other | 1 | Java version manager for Windows | [#50375124](https://news.ycombinator.com/item?id=50375124) |
| [Friendli AI](https://friendli.ai) | providers | 1 | Inference provider for GLM | [#50375145](https://news.ycombinator.com/item?id=50375145) |
| [gnosh.ai](https://gnosh.ai) | harness | 1 | Called a 'frontier harness'; no details | [#50375257](https://news.ycombinator.com/item?id=50375257) |
| [railvio](https://railvio.com) | harness | 1 | App-building harness with Jira/Confluence clones | [#50375265](https://news.ycombinator.com/item?id=50375265) |
| [masbandwidth Patreon](https://patreon.com/masbandwidth) | other | 1 | More of his AI coding work | [#50375943](https://news.ycombinator.com/item?id=50375943) |
| [tensorx.ai](https://tensorx.ai) | providers | 1 | EU inference provider | [#50376642](https://news.ycombinator.com/item?id=50376642) |
| [Swival](Swival.dev) | harness | 1 | Coding harness used with Clef model routing | [#50376601](https://news.ycombinator.com/item?id=50376601) |
| [exe.dev](exe.dev) | sandbox | 1 | Subscription dev environment service | [#50376381](https://news.ycombinator.com/item?id=50376381) |
| [ThinkRail (JetBrains)]((none given)) | harness | 1 | Experimental agent IDE with easy worktrees and spec-driven development | [#50376352](https://news.ycombinator.com/item?id=50376352) |
| [Strata / oMLX]((none given)) | local_models | 1 | Local inference; Strata streams experts for larger MoE models | [#50376810](https://news.ycombinator.com/item?id=50376810) |
| [Rex]((none given)) | session_control | 1 | Terminal multiplexer used instead of tmux/cmux | [#50377121](https://news.ycombinator.com/item?id=50377121) |
| [agent-swarm.dev](agent-swarm.dev) | orchestration | 1 | Self-hosted MIT agent swarm | [#50378028](https://news.ycombinator.com/item?id=50378028) |
| [Mastra]((none given)) | orchestration | 1 | Open-source framework for agentic workflows | [#50377455](https://news.ycombinator.com/item?id=50377455) |
| [Caudra swarm discussion](https://github.com/caudra/caudra/discussions/2) | orchestration | 1 | Plans for a Caudra swarm | [#50378737](https://news.ycombinator.com/item?id=50378737) |
| [Lynx](lynx.railcode.dev) | harness | 1 | Agent coding interface | [#50378756](https://news.ycombinator.com/item?id=50378756) |
| [Workforce]((none given)) | orchestration | 1 | Own agent factory that builds and deploys itself | [#50379352](https://news.ycombinator.com/item?id=50379352) |
| [joemattie.com](joemattie.com) | other | 1 | Personal site of AI-built projects | [#50380371](https://news.ycombinator.com/item?id=50380371) |
| [Varyz AI]((none given)) | orchestration | 1 | Business overseen by an orchestration agent | [#50384963](https://news.ycombinator.com/item?id=50384963) |
| [Multi-device coding harness (unnamed)]((none given)) | harness | 1 | Planned BYOK OpenRouter harness for ZDR endpoints | [#50380401](https://news.ycombinator.com/item?id=50380401) |

## What changed since the first pass

- Cross-model review goes up from 16 to 19 and is now joint first. It is the most independently backed pattern, with 12+ setups doing cross-vendor review by default.
- Tiered routing goes up from 17 to 19. Plan-strong, execute-cheap appears in 10+ setups. Escalate-on-failure itself rests mainly on glennfiedler and contingencies, so the escalation recommendation scores 18, not 19.
- Context-as-files goes up from 17 to 19 and widens from HANDOFF+DECISIONS to ADRs, per-repo state files, close-out notes and the low-context-fill discipline. The HANDOFF/DECISIONS recommendation rises from 17 to 19 and is now the top recommendation.
- The Minimalists stay at 18 but are reframed. Their strongest contribution is 'evaluate against vanilla' plus 'newer models need fewer guardrails'. The first-pass top recommendation (eval harness against vanilla, then prune) is confirmed but rescored from 18 to 16, because direct evidence is thin (SOLAR_FIELDS, joshheitzman, nedt).
- Tickets and kanban rise sharply from 13 to 18. Many independent issue-driven hand-off setups exist, and this is John's existing design.
- Cheap open models rise from 14 to 17 on hard cost data. The verdict stays at trial because of counter-claims that they cost more than subscriptions in practice.
- Orchestrators rise from 10 to 15, but only as a narrow coordinator pattern (main thread does not implement; agentic review before a human sees work). Wide swarms remain weak.
- Session managers (11) are folded into 'Session control: phone, remote, voice, alerts' at 16. John's phone-first working raises the fit.
- Skeptics stay at 15, now merged with attention limits and wellbeing. The evidence supports keeping John's two-worker cap.
- Sandboxing rises slightly from 14 to 15. The evidence is strong, but the marginal fit is low because cloud sessions and the push hook already cover most of it.
- New categories that the first pass missed: Deterministic-first workflows (17), Skills, prompts and prose quality (17), Cost and quota telemetry (16), and Verification beyond code review (16). The prose-quality finding matters most for a content harness.
- The daily digest is reframed. As a personal-agent feature it is where agents 'dwindle' (#50376601). As a bulk approve-or-deny queue for John (#50385555) it scores 16.
- The cost board rises from 14 to 17, backed by several independent usage trackers and control rooms.
- New recommendations not in the first pass: a question-list reviewer with binary verdicts, a review stop rule, a private-path guard before GreenPT, a monthly turn-sink review, and persona readers for consumer content.

## Critic notes

An independent critic agent checked the synthesis. Its points:

- Recommendation 2 ('Escalation rule across model routes, logged on receipts') describes a packet that moves up model routes when it fails. That breaks CLAUDE.md rule 16 (one model route per packet; highest_reasoning only after the explicit premium command), and rule 12 says to stop on a premium-model substitution. — Reframed as 'Escalate by opening a new packet'. The failed deterministic check is recorded on the receipt and the packet closes. A follow-up packet runs on the next route. highest_reasoning needs John's explicit premium command. Any retry stays inside the packet's retry and ten-turn ceilings. Ease drops to 3 and evidence to 3, so the total is 5+3+3+5 = 16, and John decides. — high
- Recommendation 15 (AST or content-diff check to decide review reuse) is marked 'John decides? no'. It loosens rule 11, which allows reuse only when the file hash, policy hash, reviewer evidence and verdict are unchanged. That is a silent policy change, which rule 5 forbids. — Marked 'John decides: yes'. Framed it as an Experimentation Station trial whose diff check can only flag a reuse candidate, never grant reuse, until John changes rule 11. — high
- The report counts sgarland [#50378365] as a by-default cross-vendor reviewer and claims '12+ setups by default'. sgarland is Claude-first. He only occasionally asks ChatGPT for an adversarial review, and calls Codex review from inside Claude. — Moved sgarland to the 'occasional' group. Restated the count as 11 clearly by-default setups: sadilek, devinegan, entrope, navels, fonrex, enesalatas, Reebz, gregwebs, gabriel-uribe, virpo, petesergeant. Added YuechenLi as a split by vendor strength rather than a review. Evidence stays at 5 and the category stays at 19. — medium
- Escalate-on-failure evidence is overstated and inconsistent: 3 in insight 4 but 4 in recommendation 2. Only glennfiedler [#50375921] automates escalation. contingencies [#50374502] switches up manually, and wombat-man [#50381009] uses Fable only for planning. The report also leaves out glennfiedler's own caveat: 'for 99% of stuff I need to do Opus 5.5 @ medium is ideal'. — Evidence set to 3 everywhere. Section 4.2 now separates automated from manual escalation and adds the 99% caveat. Section 10 overturns the first pass's escalate-on-failure score from 17 to 16 as a recommendation. — medium
- The daily digest is scored 15 as insight 26 but 16 in section 10, with no explanation. Its only source, 50385555, is a vendor reply (mschwarz: 'this is mike from OpenRig'), which the report does not disclose. — Separated the two items. Insight 26 (bulk approve or deny, one vendor source) stays at 15. Recommendation 10 (a phone 'needs John' queue) is 16 because alerts and approval queues appear in several setups (50373796, 50378479, 50380990, 50376390, 50379944). The vendor disclosure is added to 4.10, 4.12 and the caveats. — medium
- Insight 12 (privacy routing) cites voodooEntity [#50376538]. That is weak support. The direct evidence is a-saleh [#50376810] ('personal stuff that I don't want to send to cloud'), fidelramos [#50385740] (private hosting in Venice, Opus and GPT only for non-personal tasks) and internet_points [#50377307] (diffs redacted automatically). — Changed the ids to 50385740, 50376810 and 50377307, and updated 4.15 to match. — medium
- Insight 19 ('Subagents burn limits fastest; use them for map-reduce only') cites mholm [#50373364], who does not support it. — Changed the ids to sillysaurusx [#50373445] (subagents for map-reduce work) and joegibbs [#50376279] ('a big gimmick', barely uses subagents, models are 'identical clones'). — medium
- Insight 18 ('Main thread only coordinates') cites kuboble [#50376058]. In kuboble's setup Claude decides whether to do a ticket itself or delegate it, so it is not a coordinator-only main thread. — Changed the ids to sheepscreek [#50375347] ('Tell it explicitly not to implement anything') and mickeyp [#50376582] (a master chat that delegates). Kept kuboble under tickets, where it belongs. — medium
- Section 4.14 uses sadilek's '~6 CLIs' as his ceiling. His comment goes on to say that with his custom UX he now runs '20+ with fun', and that the bottleneck moved to his machine, so he added remote workers. — Stated both numbers. Kept the attention-limit point, which rests on fhub, ultrasandwich and wombat-man. Added sadilek as the counterexample, noting that he built a whole UX to get there. — medium
- Recommendation 5 (push more bounded extraction to GreenPT) does not restate the hard limits: two calls, EUR 0.01 and one return trip per issue, a EUR 10.00 monthly cap, output that stays a candidate, and no private material. — Added a constraint note to section 6. It frames the recommendation as using the cap John has already approved, packet by packet, never as spending budget down before month end. — medium
- Recommendations 3, 9 and 14 (question-list reviewer, vanilla bake-off, persona readers) add model calls without counting them against the delegated-call limits: at most 5 delegated calls and 2 parallel workers per packet, and a separate packet for each trial. — Added constraint notes. One integrated reviewer counts as one delegated call. Each bake-off arm is its own approved Experimentation Station packet. Persona readers each count as a delegated call, run at most two wide, and never see docs/private material. — medium
- The top gold quote ('tell it what complete looks like', 50367037) has no insight or recommendation of its own, although it maps directly onto packet acceptance criteria. — Added insight A1 (4+5+3+5 = 17), backed by thefourthchime, siliconc0w [#50381456] (design up front so it drives toward 'a specific outcome') and cpobuda [#50380633]. Added recommendation 16. — medium
- Section 4.15 says personal agent platforms 'are unstable [#50373974]'. browningstreet says OpenClaw spiralled and crashed, but calls Hermes Agent 'a core tech for me'. jedisct1 [#50376601] says his use of NBClaw dropped off until it mostly sends summaries; he does not use the word 'dwindle'. — Rewrote the bullet: one platform crashed while another became core for the same user, and jedisct1's use tapered off to a summary bot. — medium
- Projects from vendors are not flagged. Examples: mschwarz [#50385555] is the OpenRig author replying to an OpenRig user, and Kuyawa [#50373796] says his tool 'never hallucinates'. — Added both to the self-promotion caveat. Kept the alerts idea from 50373796, but not the reliability claim. — low
- The caveat says droneship was 'posted as a reply twice'. It was posted three times (50371043, 50371049, 50372231). — Corrected to three times. — low
- Three categories tie at 19 with no tie-break rule. — Added a note: within a tie, rows are ordered by how many independent setups back them, and the order inside a tie is not significant. — low
- The ADR quote 'raised overall output quality' is in stkni [#50376451], but 4.3 lists tritondev [#50376262] first. tritondev builds Humbug; his point is low dependency. — Cited 50376451 for the quote and 50376262 only as context. — low
- The '1 billion tokens used 7% of a $10 plan' figure [#50381117] includes cache, which the report does not say. — Added '(including cache)'. — low
- Some project descriptions are incomplete. Superintendent [#50380990] also has a limits dashboard and an approve/deny queue for refined ideas. sheepscreek's [#50375342] task journal and Codex local-memory tip are missing. virpo [#50378479] uses Codex for image generation as well as review. — Added these details to 4.3, 4.9, 4.1 and section 7. — low
- The structured project list (175 entries) is missing several linked or bare-domain providers: Venice.ai, Z.ai, artificialanalysis.ai, duck.ai, devin.ai, Abliterated.ai and llama.app. Some second sources are also missing: deepinfra.com is linked by mring33621 [#50380281], pi.dev also by Zambyte [#50374449], Kan also by alok-g [#50374919], Juggler also by julesrms [#50379165], ctlflow also by Scrounger [#50373800], Conductor.build also by jkkorn [#50379292], and eca.dev also by AiAi [#50373811]. — Listed them in a new 'Project list corrections' block in section 7 and in 'missing'. The stonker URL (it carries an access key) and localhost:8080 stay excluded. — low
- Section 10 does not give an explicit confirm or overturn for each first-pass adoption. — Section 10 now gives each one. Eval vs vanilla then prune: 18 to 16, overturned. Escalate-on-failure: 17 to 16, overturned. HANDOFF plus DECISIONS: 17 to 19, raised. Daily digest: 15 confirmed as an insight, 16 as the phone queue. Cost board: 14 to 17, raised. — low
- Missing: Insight: 'tell it what complete looks like' as packet acceptance criteria (thefourthchime 50367037, siliconc0w 50381456, cpobuda 50380633)
- Missing: Insight: route by task type or vendor strength as well as by tier (YuechenLi 50375205: Claude for frontend and debugging, Codex for features and research; virpo 50378479: Codex for images and reviews; phillc73 50367557: GLM5.3 for adversarial batteries and documentation; jedisct1 50376601: a different model for each task type)
- Missing: sheepscreek 50375342: a task journal holding tribal knowledge, plus 'turn on' Codex local memory
- Missing: glennfiedler 50375921 caveat: 'for 99% of stuff I need to do Opus 5.5 @ medium is ideal'; he uses extra models mainly for other points of view and security audits
- Missing: sadilek 50370886: 20+ parallel CLIs with a custom UX (Obeya), then remote workers to spread load across machines
- Missing: wombat-man 50381009: 'The bottleneck is me understanding what code is going in'
- Missing: Supply-chain and low-dependency harness concern (kikdij 50378847: 'Way too many dependencies and supply chain attack opportunities'; tritondev 50376262: Humbug, 3 runtime dependencies)
- Missing: Agents log their work to an Obsidian vault (GoodFriday 50380005, dcferreira 50379944)
- Missing: kikdij 50378847: the harness writes the plan to the filesystem, hands over to the next session and resets context (further support for insight 3)
- Missing: a-saleh 50376810: local models for 'personal stuff that I don't want to send to cloud' (better privacy evidence than 50376538)
- Missing: joegibbs 50376279: orchestration is 'a big gimmick'; barely uses subagents
- Missing: mschwarz 50385555 is the OpenRig vendor ('mike from OpenRig'); also suggests auto-approving whole classes of findings once trusted
- Missing: djeastm 50380990 Superintendent: also a limits dashboard and an approve/deny queue
- Missing: brabel 50376352: a Requesty gateway dashboard; Haiku 5 for simple work, Opus and Argon for big work, 'the difference in price is dramatic'
- Missing: poelzi 50378157: a queue-manager agent that keeps the workflow engine busy, and decision steps where agents can ask the operator
- Missing: dgunay 50375407: the chief of staff turns workstreams into beads, and Remuda runs containerised workers
- Missing: Projects or providers missing from the structured list: Venice.ai (fidelramos 50385740, private hosting), Z.ai (mazone 50373447, alexfortin 50374094 and 50375856, slipwalker 50370716, deathmonger5000 50374678, hypfer 50376056, fzxu22 50385925), artificialanalysis.ai (decoding 50374344), duck.ai (tharkun__ 50374626, npteljes 50377746), devin.ai (fishtoaster 50384905), Abliterated.ai (profdevloper 50373770), llama.app (thibsrn 50377715)
- Missing: Second sources missing from the project list: deepinfra.com link (mring33621 50380281), pi.dev (Zambyte 50374449, world2vec 50368325, slipwalker 50370716, profdevloper 50373770, rglullis 50376782), Kan (alok-g 50374919), Juggler (julesrms 50379165), ctlflow (Scrounger 50373800), Conductor.build (jkkorn 50379292), eca.dev (AiAi 50373811)
- Missing: droneship was posted three times (50371043, 50371049, 50372231), not twice

## Process record

One-day exception to CLAUDE.md rule 14, approved by John. Delegated agents: 8 readers + 1 synthesis + 1 critic = 10. Spend: unknown (no monetary telemetry).
