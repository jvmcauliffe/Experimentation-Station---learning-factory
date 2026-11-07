# Implementation plan: HN guide insights → harness builds

Written 7 Nov 2026 from `GOLDMINE.md` (56 insights, 10 ranked changes, 6 John-decides items) and the packets already posted on jvmcauliffe/content-creation-pipeline. This is the plan other chats follow. Each build is one Claude task packet. Nothing here enlarges a packet's authority; the issue is always the scope record.

> **Read WHAT-IS-MISSING.md first (7 November 2026).** Measured against John's definition of complete, this plan is hardening, not the automation. The loop that does the work is W0-1 to W0-9 and W1-1 to W1-5 in that file. B0 is subsumed by W0-3. B1 to B14 follow once the loop runs a night unattended.

## 0. Architecture, optimised

The 56 insights collapse into six components. Every insight that is built lands in exactly one of them, so no script is written twice and no path has two owners in the same wave.

| Component | Lives in | Owns | Builds |
| --- | --- | --- | --- |
| C1 Packet gate | `scripts/validate_claude_task.py` | every packet field and lint rule | B3, B10 |
| C2 Lifecycle scripts | `scripts/check_*.py`, `scripts/parse_review_verdicts.py` | deterministic checks at open, review and close | B1, B5, B6, B14 |
| C3 Receipt reader and reports | `scripts/harness_report.py`, `scripts/needs_john_digest.py` | one reader of sealed receipts; cost board, turn-sink table, needs-John digest | B4, B9, B13 |
| C4 Provider guards | `scripts/greenpt_bridge.py` | private-path refusal, bounded queue, cap arithmetic | B2 |
| C5 Policy docs | `docs/routing-table.md`, `docs/review/*.md`, `docs/escalation-rule.md`, `docs/standing-directives.md` | written rules the scripts enforce | B7, B8 |
| C6 Hook wiring | `.claude/hooks/pre_tool_checks.py` | calls C2 and C4 before push and trigger | B11, B12 |

Design rules that make this cheap to run:

1. Scripts first, model never. Every component except C5 is deterministic, no network, no model calls. Model work is only the authoring inside each packet.
2. One owner per path per wave. `validate_claude_task.py` and `pre_tool_checks.py` are the two contended files; each gets one packet per wave, run last in that wave.
3. Readers import, they do not re-parse. B9 and B13 import the reader from `harness_report.py` (importing is not editing, so it stays outside their in-scope paths).
4. Governance text stays with John. No packet touches `CLAUDE.md` or `AGENTS.md` (`scripts/prepare_claude_review.py` already excludes them). A build that needs a rule line produces the line in a docs file; John pastes it.
5. Trial in Experimentation Station only when the thing is content, not harness code. All scripts go to content-creation-pipeline because the hooks and tests live there.

### Waves and dependencies

```
Wave 1 (posted, triggered 7 Nov)   B1 #305   B2 #306   B3 #307   B4 #308
                                     │                    │         │
Wave 2 (posted, not triggered)     B5 #310 ─ B6 #316      │         B9 #309
                                   B7 #317 ─ B8 #315      │
                                     │        │           │
Wave 3 (packets to write)          B10 schema v2 ◄────────┘ (after B3, B5, B6 merge)
                                   B11 hook wiring (after B1, B3, B6 merge)
                                   B12 packet generator (independent)
                                   B13 turn-sink (after B4)     B14 decisions roll-up (after B1)
John decides                       J1 bake-off  J2 prune CLAUDE.md  J3 personas  J4 content-diff  J5 tone line  J6 routing rows  J7 round cap
```

Trigger order for wave 2: B5, B7, B6, B8, then B9 once the B4 PR is merged. Wave 3 packets are written only after their dependencies are merged, with the base commit re-read at that time.

Wave 1 status as of this plan: triggers were posted on #305, #306, #307 and #308 on 7 Nov. Their outcomes were not checked in this chat. An executing chat reads the receipt on the issue before starting anything that depends on it. A missing or failed receipt is indeterminate, not a pass.

## 1. Build sheets

Default packet figures (from the posted packets' template) unless a sheet says otherwise: authority `implement-and-open-pr`, route `standard_reasoning`, effort `medium`, reusable review receipts `none`, maximum turns 5, correction retries 1, run budget USD 0.50, work units 3, expected duration 10 minutes, maximum delegated model calls 0, parallel workers 1. Stop conditions and handover destination are the template's. Base commit is always the main head at packet time (was `02451da5cdfd16477192e41fab9cd9ff8491fb3d` on 7 Nov; re-read it).

### B0 Queue runner — new packet, wave 0, before any wave 2 trigger

Missing from the first draft of this plan: insight 21 was marked "Existing design" without checking that the executor had ever completed a packet. It had not (runs on #305–#308 all failed or were cancelled). Nothing picked the next packet, noticed a failure or retried.

- Deterministic script, no model call. Reads the receipts on open `[claude-task-v1]` issues, picks the next packet whose dependencies have merged, lints it against the current main head, posts the trigger, and stops.
- On a receipt showing a transient failure it posts the explicit transient-retry command, inside the packet's retry limit and the ten-turn ceiling. On a hard failure it posts a needs-John line and moves the packet to the B9 digest.
- Stops at the monthly app-started cap, at the declared run budget, and when any check is missing (rule 7).
- Depends on PR 345 (executor turn cap) and on John's decision: github-actions[bot] as an allowed trigger origin with its own cap, or a ready marker that a Claude session converts into the trigger.

### B1 Handover file at packet close — issue #305 (P1), wave 1

- Insights: 1, 9, 12, 23, 39. Change 1.
- Paths: `scripts/check_handover.py`, `tests/test_check_handover.py`, `docs/handover/README.md`, `docs/handover.md`.
- Build: `check_handover.py ISSUE` checks `docs/handover/ISSUE.md` exists, ≤ 4 KB, headings Done, Not done, Decisions, Next. Non-zero exit with plain-word problems. Tests for pass, missing, oversize, missing heading. README carries the four-heading template.
- Acceptance: unittest discovery green; script exits 0 on the template and non-zero on each failure case.
- Feeds: B10 (field), B11 (hook), B14 (roll-up).

### B2 Private-path guard and GreenPT queue — issue #306 (P4), wave 1

- Insights: 11, 18, 20, 48. Changes 5 and 7.
- Paths: `scripts/greenpt_bridge.py`, `tests/test_greenpt_bridge.py`, `docs/greenpt-queue.md`.
- Build: `--lint` refuses a `[greenpt-task-v1]` packet whose inputs name `docs/private/` or match a small redaction pattern list kept in the script. Queue doc lists ready bounded tasks (extraction, link lists, glossary consistency) that a session may trigger while the month total stays under EUR 10.00. Per-issue limits unchanged.
- Acceptance: unittest green; a packet naming `docs/private/x.md` fails lint with a plain-word reason; an ordinary packet lints as before.
- Feeds: the existing PreToolUse hook (it already lints before a trigger, so the guard is wired for free).

### B3 Spec-first packets that must ship an artefact — issue #307 (P6), wave 1

- Insights: 14, 24. Change 9.
- Paths: `scripts/validate_claude_task.py`, `scripts/check_deliverables.py`, `tests/test_check_deliverables.py`, `.github/ISSUE_TEMPLATE/claude-task.yml`.
- Build: optional packet fields `Brief` and `Deliverable paths`. `check_deliverables.py` takes the PR diff file list and the packet, exits non-zero when no deliverable path changed. A packet without the fields lints exactly as before.
- Acceptance: unittest green; lint parity test still passes.
- Feeds: B10, B11.

### B4 Cost and quota board — issue #308 (P5a), wave 1

- Insights: 10, 20, 48. Change 6.
- Paths: `scripts/harness_report.py`, `tests/test_harness_report.py`.
- Build: reads sealed receipts (from a local JSON export or the issue comments the packet names), writes one Markdown page: GreenPT month total against EUR 10.00 and the remainder; app-started Claude and Codex counts against 250 each; packets, retries, escalations; `unknown` wherever telemetry is missing. Exposes `load_receipts()` for B9 and B13. No model calls, no spend estimates presented as charges.
- Acceptance: unittest green on fixture receipts including one with missing telemetry.
- Feeds: B9, B13.

### B5 Review question list with binary verdicts — issue #310 (P2), wave 2

- Insights: 6, 32, 4. Change 2.
- Paths: `docs/review/questions.md`, `scripts/parse_review_verdicts.py`, `tests/test_parse_review_verdicts.py`.
- Build: fixed checklist for content review (facts needing verification, UK English, tone, claims, links, private-material leaks, UK legal or financial statements). Reviewer answers each CLEAR or DISCREPANCY with one line of evidence. Parser turns the reviewer's reply into receipt JSON and fails on any missing or non-binary answer. The checklist file's hash joins the policy hash for rule 11 reuse.
- Acceptance: unittest green; parser rejects a numeric score; accepts the sample reply in the doc.
- Feeds: B6, B10.

### B6 Review stop rule — issue #316 (P8), wave 2 (policy item 1, approved by John 7 Nov)

- Insight: 13. Decides J7's default.
- Paths: `docs/review/stop-rule.md`, `scripts/check_review_rounds.py`, `tests/test_check_review_rounds.py`.
- Build: rule text: two review rounds per candidate; after round two any remaining DISCREPANCY goes to John as a decision, not a third round. Script counts rounds from the receipt comments on an issue or PR and exits non-zero at the third.
- Acceptance: unittest green on fixtures with 0, 2 and 3 rounds.
- Feeds: B10, B11.

### B7 Escalation rule across routes — issue #317 (P9), wave 2 (policy item 3, approved by John 7 Nov)

- Insights: 5, 8, 54.
- Paths: `docs/escalation-rule.md`, `docs/roles.md` (routing line only).
- Build: a failing packet is not retried on a stronger model inside the same packet. Escalation is a new packet, one route up, citing the failed receipt, and `highest_reasoning` still needs the explicit premium command. A stronger model is never used to repeat unchanged evidence.
- Acceptance: the doc exists, the roles line links to it, no script change.
- Feeds: B8.

### B8 Role-to-model routing table — issue #315 (P3), wave 2

- Insights: 3, 5, 16, 18, 37, 54. Changes 3 and 4.
- Paths: `docs/routing-table.md`, `docs/standing-directives.md`.
- Build: commit the table in `hn-agent-setups-2026-11/routing-table.md` with its `existing` rows as written and the three `proposed` rows marked "awaiting John" (J6). Add a one-paragraph note to standing directives recording the two-worker cap evidence (change 4: no rule change). Link the escalate column to B7's doc.
- Acceptance: both docs render; proposed rows carry no rule text until John answers.

### B9 Needs-John digest — issue #309 (P5b), wave 2, after B4 merges

- Insights: 26, 34, 39. Change 8.
- Paths: `scripts/needs_john_digest.py`, `tests/test_needs_john_digest.py`.
- Build: collects open items by label (candidate awaiting approval, blocked packet, unresolved DISCREPANCY, cap or quota warning from B4) and writes one comment body for a fixed issue, one line per item with the decision John can type. Posts nothing itself; a session posts it through the GitHub comment tool. "Done" notices are not included, they stay as receipts, which is the two-alert split of insight 26. No auto-approval of any class.
- Acceptance: unittest green on fixtures; output is empty text when nothing needs John.

### B10 Packet schema v2 — new packet, wave 3, after B3, B5 and B6 merge

- Insights: 4, 13, 24. Implements J6 row 5 and J7 if John says yes.
- Paths: `scripts/validate_claude_task.py`, `tests/test_validate_claude_task.py`, `.github/ISSUE_TEMPLATE/claude-task.yml`, and the packet field documentation file (find it with `grep -rl "Maximum delegated model calls" docs/`).
- Build: three optional fields with lint rules: `Handover file` (default `docs/handover/ISSUE.md`; lint that the path is inside In-scope paths); `Reviewer provider` (lint: must differ from the authoring provider; Claude packets default to Codex); `Review rounds` (integer, lint ≤ 2 unless John has raised it in the packet). Packets without the fields lint as before.
- Acceptance: unittest green; parity test passes; one fixture per new rule.
- Figures: work units 4, expected duration 15.

### B11 Hook wiring — new packet, wave 3, after B1, B3 and B6 merge

- Insights: 17, 36.
- Paths: `.claude/hooks/pre_tool_checks.py`, `tests/test_pre_tool_checks.py`.
- Build: before `git push` on a packet branch the hook runs, in order, the unittest suite (existing), `check_deliverables.py`, `check_handover.py`, `check_review_rounds.py`; any non-zero blocks the push with the script's own message. No new policy; the hook only calls what the merged packets delivered.
- Acceptance: unittest green; one test per new block; existing trigger-lint tests unchanged.
- Figures: work units 4, expected duration 15.

### B12 Packet generator — new packet, wave 3, independent

- Insights: 15, 17.
- Paths: `scripts/new_claude_packet.py`, `tests/test_new_claude_packet.py`, `docs/claude-task-packets.md`.
- Build: turn the scratchpad `gen2.py` into a committed script: input is a small JSON spec (outcome, task items, in-scope paths, out-of-scope, acceptance, evidence, optional figure overrides); output is the packet Markdown and the lint event JSON, then it runs `validate_claude_task.py --lint` against the current main head. The doc describes the fields and the figure defaults from section 1.
- Acceptance: unittest green; generating this plan's B13 sheet produces a packet that lints clean.

### B13 Monthly turn-sink review — new packet, wave 3, after B4 merges

- Insights: 45. Change 10.
- Paths: `scripts/harness_report.py` (add `--by-stage`), `tests/test_harness_report.py`, `docs/reviews/turn-sink-YYYY-MM.md`.
- Build: table of turns, retries and delegated calls per packet stage from the receipts; the single biggest sink named at the top. The conversion of that sink into a script is a separate implement-and-open-pr packet each month.
- Acceptance: unittest green; report-only output for the month committed as the doc.
- Figures: authority `report-only` for the monthly run; the `--by-stage` addition is one implement-and-open-pr packet first.

### B14 Decisions roll-up — new packet, wave 3, after B1 merges

- Insights: 9, 23.
- Paths: `scripts/collect_decisions.py`, `tests/test_collect_decisions.py`, `docs/DECISIONS.md`.
- Build: reads every `docs/handover/*.md`, lifts the Decisions section of each into `docs/DECISIONS.md` newest first with the issue number. Deterministic; re-run at any packet close.
- Acceptance: unittest green on two fixture handover files; idempotent on a second run.

## 2. John decides (packet written only on a yes)

| Id | Item | Would score | What a yes produces | Recommendation |
| --- | --- | --- | --- | --- |
| J1 | Bake-off: vanilla against the full harness (insights 19, 22, 35) | 8.3 | report-only packet: re-run three closed packets in Experimentation Station with vanilla Claude Code, compare turns, defects found by Codex review, and time; one page | Yes, after wave 2, one packet, standard route |
| J2 | Prune CLAUDE.md and move rules into hooks (22, 27) | 8.0 | report-only packet listing each CLAUDE.md rule, whether a hook or script already enforces it after B11, and a shorter proposed text; John edits governance himself | Yes, after B11 |
| J3 | Persona readers for academy and Sark content (46) | 5.3 | `docs/review/personas.md` with two personas; reviewer answers the B5 checklist as each; adds one delegated call per review | Trial on one piece |
| J4 | Content-diff check for review reuse (47) | 3.3 | per-file hash reuse already exists (rule 11); this would add a semantic diff | Decline |
| J5 | Tone line in AGENTS.md (31) | not scored | one line, John's edit | John's call; no packet |
| J6 | Routing rows 4b (fourth provider), 5 (reviewer ≠ author as a written rule), 7 (GreenPT drafts non-private boilerplate) | from table | row 5 yes → B10 lint; row 7 yes → B8 row text; row 4b yes → a provider packet of its own | Yes to 5; no to 4b; 7 only inside the cap |
| J7 | Review round cap of two (B6 default) | 20.0 | confirms B6 and the B10 lint value | Yes |

## 3. Disposition of all 56 insights

| # | Insight (short) | Disposition |
| --- | --- | --- |
| 1 | HANDOFF.md instead of compaction | B1 |
| 2 | Main thread only coordinates | Superseded: the runner (W0-3) coordinates; a chat session only writes task issues |
| 3 | Subagents burn limits | Existing: five-call, two-worker caps |
| 4 | Cross-vendor review by default | W0-5: the runner posts the review on every PR it opens; B10 lints it |
| 5 | Plan strong, execute cheap | B7, B8 |
| 6 | Fixed PR-review question list | B5 |
| 7 | Credential-injecting proxy | Existing: cloud session proxy and request_credential |
| 8 | Escalate up tiers | W1-4 escalation ladder, run by the runner from the failed receipt |
| 9 | ADRs as you go | B1, B14 |
| 10 | One usage and cost board | B4 |
| 11 | Private material only to private models | B2 |
| 12 | Close-out hints into AGENTS.md | B1 Next heading; AGENTS.md edits stay with John |
| 13 | Review always finds something: stop rule | B6 |
| 14 | Productivity porn | B3 |
| 15 | Frequent prompts become skills | B12 |
| 16 | Attention caps parallelism | Existing cap; B8 records the evidence |
| 17 | Deterministic scripts, agents as fallback | W0-3 runner is the deterministic control flow; models only inside packets |
| 18 | Models write poor prose | Existing: GreenPT output is a candidate; B8 rows 1 and 7 |
| 19 | Evaluate against vanilla | J1 |
| 20 | Cheap models cost little | B2 queue, B4 remainder line |
| 21 | Issues as planner-to-executor hand-off | **Not existing.** W0-2 scheduler and W0-3 runner |
| 22 | 5.5-era models need fewer guardrails | J2 |
| 23 | Memory folder and state file | B1, B14 |
| 24 | Spec-first | B3 |
| 25 | Agents commit, host pushes | Changed 7 Nov: the runner's merge gate merges harness PRs on the written criteria; John keeps publication, caps, verified facts and consumer human gates |
| 26 | Separate done and needs-you alerts | B9 |
| 27 | Broad skills poison context | J2 |
| 28 | Cheap inter-agent channels | Labels and receipts read by the runner; PR 13 stays message-only for humans |
| 29 | Remote control everywhere | Covered differently: the scheduler runs in GitHub Actions, no local machine needed |
| 30 | Audit against 100 tips | Declined: this mining was the audit |
| 31 | Vulcan tone line | J5 |
| 32 | Binary CLEAR or DISCREPANCY gates | B5 |
| 33 | Tickets as the interface | W1-1 intake: one `task` issue is the whole interface |
| 34 | pm-intake daily digest | W0-9 morning post; rule-approved classes auto-approved; B9 holds only the four needs-John classes |
| 35 | Build the builder | J1 measures it; otherwise a principle |
| 36 | Mechanical gates | Existing hooks; B11 |
| 37 | Parallelise across projects | Existing: one owner per path |
| 38 | Kanban as files | Issue labels as states: ready, running, review, fix, merge, needs-john, done (W0-3) |
| 39 | Overnight package to read in the morning | W0-9 morning post, built from receipts and committed |
| 40 | Burnout | Existing caps; no build |
| 41 | Implementer and reviewer loop until clean | W0-6 fix loop: review, fix, review, round cap three, then escalate |
| 42 | Scoped temporary credentials | Existing: session-scoped GitHub access |
| 43 | Clean-up pass after fleet work | Not applicable: no fleets; B6 round two is the clean-up |
| 44 | Push-to-talk voice | Declined: tooling |
| 45 | Turn token sinks into code | B13 |
| 46 | Persona dogfooding | J3 |
| 47 | AST-diff review reuse | J4 |
| 48 | Spend leftover capacity before reset | B2 queue, B4 |
| 49 | External sandbox | Existing: cloud container |
| 50 | Open model fallback for refusals | Declined: refusals go to John, not a weaker judge |
| 51 | Quota-aware provider switching | W1-5: the runner picks the provider with room; rule 16 still holds inside a packet |
| 52 | Free inter-session messaging is chaos | Existing: message-only authority |
| 53 | Review pages for visual output | Existing practice: artifacts |
| 54 | Weaker models often better aligned; top for review | B7, B8 |
| 55 | Browser exploratory testing loop | Chauffeur already runs Playwright in `make test`; W0-7 gate requires it green |
| 56 | Personal agents dwindle | W0-2 plus W0-3 is 'just a cronjob' |

Counts: built or in flight 26 (B1–B14 cover insights 1, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20, 23, 24, 26, 32, 34, 36, 39, 45, 48, 54 and 16's record), existing with no build 15, John decides 7, declined or watch 10. Working: 26 + 15 + 7 + 10 = 58 because 16 and 18 appear in two rows; distinct insights 56.

## 4. Checklist for the executing chat

1. Startup order: `CLAUDE.md`, `AGENTS.md`, `docs/three-provider-bridge.md`, `docs/standing-directives.md`, the trial scoreboard. Then this plan's sheet for your build.
2. Read the main head. If it moved since the packet's Base commit, do not edit the approved packet; write a new one (B12 once merged, else `gen2.py` style) and post it.
3. Confirm no open branch or PR touches your in-scope paths. If one does, stop and report the collision.
4. Lint the packet: `python3 scripts/validate_claude_task.py --lint --event EVENT.json --head MAIN_SHA`. Post `@claude run approved packet` only through the GitHub comment tool, never from the shell.
5. Inside the run: at most five tool calls a turn, eight minutes a turn, the packet's turn and retry figures, one route. Run the unittest command as a single standalone invocation.
6. Close: draft PR left unmerged for Codex review; handover file under `docs/handover/` once B1 is merged; closing comment with branch, commit, files changed, commands and results, unresolved findings, route, retry count, usage (`unknown` where missing). Count delegated model calls honestly; zero only when none were made.
7. Never edit `CLAUDE.md` or `AGENTS.md`. Leave the PR for the automate loop's merge gate (or merge it yourself after a Codex review with no P1, owner decision 7 Nov). Never publish, raise a cap or mark a fact verified.
8. A cheaper model is enough to execute any sheet in section 1; they are mechanical once the sheet is read.
