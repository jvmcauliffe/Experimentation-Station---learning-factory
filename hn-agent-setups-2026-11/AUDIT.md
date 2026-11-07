# Audit: what was copied, what was not, and why

Written 7 November 2026 against the 56 insights in `GOLDMINE.md`, the 10 ranked changes, the 6 John-decides items, the routing table, the B0 to B14 build sheets in `IMPLEMENTATION-PLAN.md` and the W0 and W1 loop pieces in `WHAT-IS-MISSING.md`. Checked against the code actually on `main` of jvmcauliffe/Content-Creation-Pipeline at commit `84075ef` (automate loop merged) and on `main` of jvmcauliffe/chauffeur-academy at `d846559`.

Plain words. Four verdicts only:

- **Done**: merged on main and tested.
- **Built, unproven**: merged, but it has not yet run a real packet to the end.
- **Not done**: nothing on main does it.
- **Left out**: deliberately not built, with the reason.

The measure is John's definition: a task typed at night is merged by morning and a post explains it, with John doing nothing in between.

## 1. The loop, piece by piece

| Piece | Verdict | What is on main | What is missing |
|---|---|---|---|
| W0-1 Executor fix | Built, unproven | PR 345 merged (turn cap); `claude.yml` passes the packet body as the prompt in agent mode. | No packet has completed end to end since the change. The first supervised night proves it or stops at needs-john. |
| W0-2 Scheduler | Done | `night-runner.yml`: cron every 30 minutes 20:00 to 07:59 UTC, plus a tick when `claude.yml` finishes, plus manual dispatch with `any_time` and `dry_run`. | Nothing. |
| W0-3 Runner | Done, with two gaps | `scripts/night_runner.py --tick`: reads `night:*` labels, lints, posts the trigger, dispatches, reads receipts, moves ready → running → review → fix → merge → done or needs-john. One transient retry. One run at a time. 566 tests green. | (a) A hard failure goes straight to needs-john; it does not escalate one tier (W1-4). (b) It dispatches only Claude packets; GreenPT and Codex packets are not in its state machine (W1-2, W1-3). |
| W0-4 Bot trigger origin | Half done | `github-actions[bot]` may start `claude.yml` through a runner-footer comment plus `workflow_dispatch`; receipts carry `trigger_origin: night-runner` with their own cap of 250 a month. | `greenpt-bridge.yml` and the PR 13 OpenAI receiver still refuse the bot. GreenPT and Codex cannot be started by the runner yet. |
| W0-5 Review hook | Built, unproven | Runner posts `@codex review` on the PR it finds for the packet and parses P1, P2, P3 tags on review comments at the head commit. | Unverified that the Codex app answers a comment posted with the Actions token, and that it tags findings P1 to P3 the way Chauffeur reviews do. The harness-side alternative (an `openai-report-v1` packet on PR 13) is not wired. |
| W0-6 Fix packet | Done | `open_fix_packet` writes a packet on the same branch with the P1 findings as evidence, labels it `night:ready`; round cap three, then needs-john. | After the cap it stops rather than escalating a route. |
| W0-7 Merge gate | Done | Checks green at the head (or the runner runs the unit suite itself when no check exists), Codex review at the head with no P1, no `docs/private/` path, no needs-john label, PR targets main, no conflict. Merges with a merge commit and closes the issue. | No budget line in the gate (money is `unknown` on receipts). Stacked PRs are not ordered bottom-up; the runner takes one packet at a time so stacks do not arise yet. |
| W0-8 Deploy | Not done | Chauffeur `cloudflare-deploy.yml` is still manual dispatch. | A `push` to main trigger with the probe, and a Chauffeur `night-runner.yml`. |
| W0-9 Morning post | Not done | `build_task_report.py` turns one receipt into a task report. | Nothing writes `reports/night-YYYY-MM-DD.md` from the night's receipts, merges and tests, and nothing opens the blog packet. |
| W1-1 Intake | Not done | A Claude chat session writes packets by hand. | A `task` label that the runner turns into a planning packet, whose output is a set of `night:ready` packets with dependencies. |
| W1-2 GreenPT first pass | Not done | GreenPT runs one call per issue when a session posts the trigger; private-path refusal (B2) is not merged. | Runner-started GreenPT extraction or draft, then the Claude authoring packet with the candidate attached. |
| W1-3 Codex implementer | Not done | Codex implements only from a PR 13 command posted by a person or a session. | Runner-started Codex packets, Claude reviewing them, same fix loop and gate. |
| W1-4 Escalation ladder | Not done | Rule on paper only (packet #317, untriggered). | Runner writes the next-tier packet bound to the failed receipt: GreenPT → Codex → Claude standard → Claude premium → needs-john. |
| W1-5 Quota switch | Not done | Caps are counted per receipt; nobody reads them to choose a provider. | Runner reads the month's counts and picks the route with room; stops the night and says so when every route is capped. |

Honest total for the loop: 5 of 14 pieces are on main, 2 of those unproven. The automate loop is the scheduler, the state machine, the fix loop and the merge gate. It is not the intake, not the other providers, not escalation, not deploy and not the morning post. That is why it is a gap-plug and not the imported capability.

## 2. The old plan, B0 to B14

| Build | Packet | Verdict | Why |
|---|---|---|---|
| B0 queue runner | none | Done | Subsumed by the automate loop. |
| B1 handover file at packet close | #305 | Not done | Wave 1 run failed before the executor fix. Packet is stale against the new main head and must be re-posted. |
| B2 private-path guard and GreenPT queue | #306 | Not done | Same. The private-path refusal is the one guard the loop must have before the runner ever starts GreenPT. |
| B3 spec-first packets with deliverable paths | #307 | Not done | Same. |
| B4 cost and quota board | #308 | Partly exists | `harness_report.py` already summarises a month of receipts. The GreenPT remainder, the two app-started counts and the `unknown` lines are B4's addition and are not merged. |
| B5 review question list, binary verdicts | #310 | Not done | Posted, never triggered. |
| B6 review stop rule | #316 | Partly done differently | The runner caps fix rounds at three in code. The written rule said two. Code wins until a packet changes it. |
| B7 escalation rule across routes | #317 | Not done | Posted, never triggered. The runner has no ladder, so the doc would describe nothing. |
| B8 routing table into docs | #315 | Not done | Posted, never triggered. Row 8 is now wrong (see section 4). |
| B9 needs-John digest | #309 | Not done | Posted, never triggered. The runner leaves one `[night-runner]` comment per stop; nothing collects them. |
| B10 packet schema v2 | none | Not done | Depends on B3, B5, B6. |
| B11 hook wiring | none | Not done | Depends on B1, B3, B6. |
| B12 packet generator | none | Not done | The runner has its own fix-packet writer; a general generator is still missing. |
| B13 monthly turn-sink review | none | Not done | Depends on B4. |
| B14 decisions roll-up | none | Not done | Depends on B1. |

Nothing from B1 to B14 is merged. All nine posted packets were written against an older main head and will need re-posting against the current one, which the runner can do once a generator exists (B12).

## 3. The 56 insights

Short names as in `GOLDMINE.md`. "Existing" means the harness already did it before this work.

| # | Insight | Verdict | Where, or why not |
|---|---|---|---|
| 1 | HANDOFF file instead of compaction | Done | Gap check 7 Nov: `docs/handover/README.md:3-5` (per-packet note, 4 KB cap, four headings) and `scripts/check_handover.py`. B1 failing did not remove it. |
| 2 | Main thread only coordinates | Done | The runner coordinates; chat sessions write issues. |
| 3 | Subagents burn limits | Existing | Rule 15 caps. |
| 4 | Cross-vendor review by default | Built, unproven | Runner posts `@codex review` on every PR it handles. |
| 5 | Plan strong, execute cheap | Not done | Routes exist per packet; nobody routes a plan to a cheaper implementer (W1-3). |
| 6 | Fixed PR-review question list | Done | `docs/review/questions.md` and `scripts/check_review_verdicts.py` on CCP main (checked 7 Nov). |
| 7 | Credential-injecting proxy | Existing | Cloud session proxy. |
| 8 | Escalate up tiers | Not done | W1-4. |
| 9 | ADRs as you go | Done | CCP #398 (db55814) adds the append-dated-rows rule to `docs/decisions.md`. |
| 10 | One usage and cost board | Partly | `harness_report.py` exists; B4 lines missing. |
| 11 | Private material only to private models | Done | `docs/private/` refusal in `greenpt_bridge.py` and `greenpt_packet.py` on CCP main (checked 7 Nov). |
| 12 | Close-out hints into AGENTS.md | Not done | B1. |
| 13 | Review always finds something: stop rule | Done differently | Runner round cap three. |
| 14 | Productivity porn | Done | CCP #396, `scripts/check_deliverables.py`. |
| 15 | Frequent prompts become skills | Not done | B12. |
| 16 | Attention caps parallelism | Existing | Rule 15. Runner runs one packet at a time. |
| 17 | Deterministic scripts, agents as fallback | Done | The runner is a script with no model call. |
| 18 | Models write poor prose | Existing | GreenPT output is a candidate. |
| 19 | Evaluate against vanilla | Left out | J1; no yes yet. |
| 20 | Cheap models cost little | Not done | B2 queue, W1-2. |
| 21 | Issues as planner-to-executor hand-off | Done | `night:ready` label plus runner. |
| 22 | 5.5-era models need fewer guardrails | Left out | J2; no yes yet. |
| 23 | Memory folder and state file | Done | Gap check 7 Nov: `scripts/harness_memory.py` (`closeout`, `rebuild`, `search`) writes committed `memory/records/<id>.md`. Task state stays in GitHub issues by design. |
| 24 | Spec-first | Done | CCP #396, `scripts/check_deliverables.py`. |
| 25 | Agents commit, host pushes | Changed | The runner now merges on the gate (owner decision 7 Nov). |
| 26 | Separate done and needs-you alerts | Half | Runner writes one needs-john comment per stop; no digest (B9), no morning post (W0-9). |
| 27 | Broad skills poison context | Left out | J2. |
| 28 | Cheap inter-agent channels | Done | Labels and receipts; no model-to-model chat. |
| 29 | Remote control everywhere | Done differently | Scheduler runs in Actions, no laptop needed. |
| 30 | Audit against 100 tips | Left out | This mining was the audit. |
| 31 | Vulcan tone line | Left out | J5, John's one-line edit. |
| 32 | Binary CLEAR or DISCREPANCY gates | Done | `scripts/check_review_verdicts.py` on CCP main (checked 7 Nov). |
| 33 | Tickets as the interface | Half | Packet issues are the interface; free-text intake (W1-1) is not. |
| 34 | pm-intake daily digest with auto-approved classes | Done differently or half | `scripts/needs_john.py` prints the digest with an Approve / Deny line; no auto-approved classes (checked 7 Nov). |
| 35 | Build the builder | Left out | Principle; J1 would measure it. |
| 36 | Mechanical gates | Done | Push hook, trigger lint, merge gate. |
| 37 | Parallelise across projects | Existing | One owner per path. |
| 38 | Kanban as files | Done | Seven `night:*` labels. |
| 39 | Overnight package to read in the morning | Not done | W0-9. |
| 40 | Burnout | Existing | Caps. |
| 41 | Implementer and reviewer loop until clean | Done | Review, fix, review, cap three. |
| 42 | Scoped temporary credentials | Existing | Session-scoped GitHub access; the runner uses only the Actions token. |
| 43 | Clean-up pass after fleet work | Left out | No fleets. |
| 44 | Push-to-talk voice | Left out | Tooling, not harness. |
| 45 | Turn token sinks into code | Not done | B13. |
| 46 | Persona dogfooding | Left out | J3; no yes yet. |
| 47 | AST-diff review reuse | Left out | Per-file hash reuse already exists. |
| 48 | Spend leftover capacity before reset | Not done | W1-5. |
| 49 | External sandbox | Existing | Cloud container and Actions. |
| 50 | Open model fallback for refusals | Left out | A refusal goes to John, not to a weaker judge. |
| 51 | Quota-aware provider switching | Not done | W1-5. |
| 52 | Free inter-session messaging is chaos | Existing | Message-only authority on PR 13. |
| 53 | Review pages for visual output | Existing | Artifacts. |
| 54 | Weaker models better aligned; top for review | Not done | Depends on W1-3 and W1-4. |
| 55 | Browser exploratory testing loop | Existing on Chauffeur | `make test` runs Playwright; the gate requires checks green. |
| 56 | Personal agents dwindle to a cronjob | Done | The runner is the cronjob. |

Counts: Done 10, Existing 11, Not done 16, Left out 11, Built unproven 1, Done differently or half 7. Working: 10 + 11 + 16 + 11 + 1 + 7 = 56. Rows 1, 9 and 23 corrected on 7 November after a gap check against the harness files; the other counts are unchanged. Independently recounted by Codex on 7 November: Existing includes one Existing on Chauffeur; Not done includes one Not done in code; the six partial/changed rows are two Done differently, two Half, one Partly and one Changed. These describe this audit's pinned historical baseline, not current harness main.

## 4. The 10 ranked changes and the 6 John-decides items

| Change | Verdict |
|---|---|
| 1 HANDOFF and DECISIONS at packet close | Not done (B1, B14) |
| 2 Question-list reviewer with binary verdicts | Not done (B5) |
| 3 Routing table in docs | Not done (B8); row 8 corrected here |
| 4 Keep width at two workers | Superseded: John raised it to four on 7 Nov; runner runs one packet at a time |
| 5 GreenPT bounded extraction queue | Not done (B2, W1-2) |
| 6 Cost and quota board from receipts | Partly (`harness_report.py`) |
| 7 Private-path guard before GreenPT | Not done in lint (B2); done in the merge gate |
| 8 Phone digest of the needs-John queue | Not done (B9, W0-9) |
| 9 Spec-first packets with deliverable-paths lint | Not done (B3) |
| 10 Monthly turn-sink review | Not done (B13) |

| John decides | Status |
|---|---|
| J1 bake-off against vanilla | Not asked, not built |
| J2 prune CLAUDE.md into hooks | Not asked, not built |
| J3 persona readers | Not asked, not built |
| J4 content-diff review reuse | Recommended decline; nothing built |
| J5 tone line | John's edit; nothing built |
| J6 routing rows 4b, 5, 7 | Row 5 (reviewer is never the author) is now true in practice because the runner always asks Codex; it is not linted. Rows 4b and 7 untouched. |
| J7 review round cap | Code says three, plan said two. Three stands until a packet changes it. |

Routing table row 8 said "Final approval, merge, publish, marking facts verified, raising caps: John only". John's instruction on 7 November 2026 ("You can merge. Take me out of the loop.") changes it to: the merge gate merges harness pull requests that meet its criteria; a Claude session may merge a harness PR it has reviewed; John keeps cap rises, public publication, marking facts verified, safety-critical consumer content and anything a consumer manifest reserves for him. `routing-table.md` and `IMPLEMENTATION-PLAN.md` are corrected in this commit. The harness `CLAUDE.md` closing paragraph and Chauffeur's `how-we-review.md` still carry the old words and are changed by the next harness packet, not by hand in a chat.

## 5. Why things were left out, in one list

1. **The wave 1 runs failed and nobody picked them up.** The executor could not finish a packet (turn cap, stripped prompt), and there was no runner. The runner now exists, so B1 to B9 can be re-posted and run by it.
2. **The first plan treated John as the bridge.** Digest without auto-approval, "John merges", "never merge" in the checklist. The owner decision reverses that and the merge gate implements it. The remaining John-as-bridge points are the intake (W1-1) and the morning post (W0-9).
3. **Other providers were never given a start button.** Only `claude.yml` accepts the runner. GreenPT and Codex workflows still demand a human or a session comment. That is W0-4's second half and W1-2 and W1-3.
4. **No escalation runs.** Every failure stops for John instead of trying the next tier. That is W1-4.
5. **Nothing is proven by a real night.** Three unverified items stand: Codex answering the Actions token, Codex tagging P1 to P3, and agent-mode `claude.yml` opening the PR.

## 6. The build from here, in order, no questions

Each line is one Claude task packet on Content-Creation-Pipeline unless it says Chauffeur. The runner dispatches it, Codex reviews it, the gate merges it. John does nothing.

1. **Supervised night one**: label #310 and #317 `night:ready` after re-posting them against `84075ef`. Proves W0-1, W0-5 and the gate. Any stop is a bug in the runner and gets a packet.
2. **W0-4 second half**: allow the runner's footer comment plus `workflow_dispatch` on `greenpt-bridge.yml` and the PR 13 receiver, each with its own origin counter on receipts.
3. **B2**: private-path lint refusal in `greenpt_bridge.py`. Must merge before step 5.
4. **W0-9**: `scripts/night_report.py` writes `reports/night-YYYY-MM-DD.md` from receipts, merged PRs, test lines and spend (estimate or reservation, period stated, `unknown` where missing); the runner opens a documentation packet that turns it into `blog/` and takes it through the gate. Public publication stays John's.
5. **W1-2**: runner starts GreenPT extraction or first draft for content packets, then opens the Claude authoring packet with the candidate attached.
6. **W1-3**: runner starts Codex implementation packets through PR 13 and treats the PR like a Claude one.
7. **W1-4**: runner writes the next-tier packet from a failed receipt; route order GreenPT, Codex, Claude standard, Claude premium, needs-john.
8. **W1-5**: runner reads month counts from receipts and picks the route with room.
9. **W1-1**: `task` label intake; runner opens a planning packet; planner output is a set of `night:ready` packets.
10. **Chauffeur**: its own `night-runner.yml` and gate criteria from `how-we-review.md`; `cloudflare-deploy.yml` on push to main with the probe (W0-8).
11. **B12** packet generator, then re-post B1, B3, B4, B5, B6, B8, B9 against the current head and let the runner run them, then B10, B11, B13, B14.
12. **J1 bake-off** as a report-only packet once ten packets have run through the loop, so the comparison has data.
