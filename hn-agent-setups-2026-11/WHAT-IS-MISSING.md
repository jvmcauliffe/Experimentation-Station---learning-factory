# What is missing from the plan

Written 7 November 2026 against one definition of complete, John's words: "when I give you a task at night time, it's done in the morning, and you literally just write a blog and explain how it's successful. I don't want to be merging, I don't want to be babysitting, I don't want to be the bridge between different models."

## 1. The honest picture

IMPLEMENTATION-PLAN.md (B0 to B14) is fourteen pieces of policy, lint and reporting wrapped round an executor that has never finished a packet. It does not contain the automation. Measured against the night-to-morning loop, this is what exists and what does not.

| Step in the loop | What exists today | Gap |
|---|---|---|
| John types a task at night | A Claude chat session writes a packet issue by hand | No intake. If the session dies, nothing picks the task up. |
| Something starts the work without John | Every workflow starts from a comment by OWNER, MEMBER or COLLABORATOR, or a manual dispatch. No `schedule:` anywhere. `github-actions[bot]` is refused as a trigger author. | No scheduler. No bot is allowed to start anything. |
| GreenPT or Codex starts, implements and finishes | GreenPT: one API call, receipt posted, output left as a candidate. Codex: starts in its own cloud from a PR 13 command, posts a result back. Nothing in the repo reads either result. | Nothing chains. A model finishing is a dead end until a human or a chat session reads the receipt. |
| Claude implements | `claude.yml` has never completed a packet. The turn cap fix is on PR 345, unmerged. The trigger phrase is stripped so the executor is told "packet" and nothing else. | Executor unproven, prompt broken. |
| Another provider reviews | On Chauffeur this works: push, comment `@codex review`, inline findings pinned to the commit in seconds. In this harness it goes through the PR 13 inbox and a human relays it. | Nobody posts `@codex review` automatically and nobody reads the result automatically. |
| Fix the findings | A Claude session does it by hand when John asks. | No findings-to-fix-packet step. Rule 3 (one owner) and rule 15 (a second candidate needs its own packet) mean the fix needs a new packet nobody writes. |
| Merge | "Only John merges" (harness CLAUDE.md, Chauffeur how-we-review.md). Chauffeur PRs 125 to 127 were merged by John within minutes of each review. | John is the merge button. The plan keeps him there. |
| Deploy | Chauffeur `cloudflare-deploy.yml` is manual dispatch only. | Nothing deploys after a merge. |
| Retry, escalate, stop | Rules on paper (B6, B7). B0 would act on a receipt, but B0 is a single script that posts one trigger and stops. | No escalation ladder runs. Transient failure means the night ends. |
| Morning blog | `build_task_report.py` turns receipts into a task report. B9 is a digest for John to action, "without auto-approval". | Nothing writes a post. B9 makes John the bridge again. |
| Needs-John list | Everything. | Should be four things: safety-critical lessons, DVL, cap rises, public publication. |

The two worst findings:

1. The plan keeps John as the bridge by design. Insight 34 was dispositioned "without auto-approval", insight 41 "declined, B6 caps at two rounds", insight 51 declined, insight 29 declined. Every one of those was a vote for John doing the relaying.
2. Nothing in the plan is a loop. The thread's complete harnesses are loops: a runner that wakes, reads state, does the next deterministic thing, and goes back to sleep. B0 was added as an afterthought and still depends on a decision nobody has taken.

## 2. What the complete examples in the thread actually do

These are the setups from GOLDMINE.md that ran unattended end to end, and the part of each that this harness lacks.

| Thread example | What it does | What we take |
|---|---|---|
| gregwebs (insight 5, #50374549) | Claude plans, Codex reviews, a cheap model implements. Under $100 a month, 3x slower, low defects. | The role split. GreenPT is too small to implement code, so our cheap implementer for code is Codex, with GreenPT on extraction and first drafts of text. |
| Issue hand-off (insight 21, #50373974, #50374380, #50374094) | Strong model writes the ticket, a scheduled cheap executor picks it up later. | A `schedule:` cron runner and a `ready` state on issues. |
| Deterministic workflows (insight 17, #50378157) | Scripts do the control flow, agents only as fallbacks, resumable after any failure, hardened on each failure. | The runner is a script. Each night's run is resumable from receipts. |
| Escalation ladder (insight 8, #50375921) | Failing task goes up the tiers until solved. | GreenPT, then Codex, then Claude standard, then Claude premium, then needs-John. |
| Implementer and reviewer loop (insight 41, #50379808) | Implementer and clean-context reviewer loop until no serious issue remains. | Review, fix, review, up to a round cap, then escalate. Not "declined". |
| pm-intake digest (insight 34, #50385555) | Side findings batched daily; whole classes auto-approved once trusted. | Auto-approve the classes John has already approved by rule (tests, wording, docs regen). Digest only what is left. |
| Overnight package (insight 39, #50385812; stonker bot #50383211) | Unattended agent writes a daily blog of status and decision reasons. | The morning post, written from receipts, committed to the repo. |
| Quota switching (insight 51, #50378856) | Drain the account that resets soonest, switch provider when a quota bites. | The runner reads caps from receipts and picks the provider that still has room. |
| Cross-vendor review hook (insight 4, #50373589) | Codex runs as a post-PR hook automatically. | `@codex review` posted by the runner on every PR it opens, as on Chauffeur. |
| Kanban as files with a ready query (insight 38) | Director agents query what is ready. | Labels on issues: `ready`, `running`, `review`, `fix`, `merge`, `needs-john`, `done`. One label per state. |

## 3. What Chauffeur already proves

The Chauffeur patchwork is: `make test` on every push (`checks.yml`), `@codex review` on the PR, fix on the same branch, review again, merge criteria written down in `docs/how-we-review.md`, a HANDOFF file at session close, and a factbook gate on facts. That loop produced Modules 3 to 8. The only parts a human does are posting `@codex review`, reading the findings, and pressing merge. All three are mechanical once the criteria are checked by a script. The merge criteria already exist in words:

- no open P1 at the head commit
- full tests green on the merged result
- stacked PRs from the bottom up
- anything held for a human gate stays unmerged

Those are the merge gate. They need code, not more policy.

## 4. The build that closes the gap

In dependency order. Everything is a deterministic script or a workflow unless it says "model".

### Wave 0, the loop

| Piece | What it does | Replaces |
|---|---|---|
| W0-1 Executor fix | Merge PR 345. Pass the packet body as the prompt instead of the stripped word "packet". Prove one packet completes. | Nothing has ever run. |
| W0-2 Scheduler | `schedule:` cron in Content-Creation-Pipeline, every 30 minutes from 21:00 to 07:00 UK, and on `workflow_run` completion of any provider workflow. Runs `scripts/night_runner.py`. | John posting triggers. |
| W0-3 Runner | Reads open packet issues and their labels, picks the next `ready` packet whose dependencies are merged, lints it against main, posts the trigger for its route, moves the label to `running`, and exits. On a receipt it moves the state: `completed` with a PR goes to `review`; a clean review goes to `merge`; findings go to `fix`; a transient failure retries once; a hard failure escalates one tier; a cap or budget stop goes to `needs-john`. | John as the bridge. |
| W0-4 Bot trigger origin | Allow `github-actions[bot]` as a trigger author on `claude.yml`, `greenpt-bridge.yml` and the PR 13 receiver, counted under its own app-started cap on every receipt. | The author_association wall. |
| W0-5 Review hook | When a PR opens from a packet, the runner posts `@codex review` (Chauffeur) or the openai-report packet (harness). When the review lands it parses P1 and P2 findings bound to the head SHA. | John posting `@codex review`. |
| W0-6 Fix packet | On findings, the runner writes a fix packet from a template: same branch, same owner, findings as the evidence, head SHA as base, one retry. Posts `@claude run approved packet` on it. Round cap three, then escalate. | John asking Claude to fix. |
| W0-7 Merge gate | A workflow that merges when all hold at the head SHA: checks green, a cross-provider review receipt with no P1, no `docs/private/` path touched, no human-gate label, within budget. Merge commit, bottom of the stack first. | John pressing merge. |
| W0-8 Deploy | `cloudflare-deploy.yml` on `push` to main after the gate merges, with the probe. | Manual dispatch. |
| W0-9 Morning post | At 07:00 the runner builds `reports/night-YYYY-MM-DD.md` from receipts, merged PRs, test lines and spend (estimate or reservation, period stated; `unknown` where missing). One documentation-tier Claude packet turns it into a post under `blog/` and opens a PR that the merge gate takes. Public publication stays John's. | Nothing. |

### Wave 1, the other providers start

| Piece | What it does |
|---|---|
| W1-1 Intake | John writes one issue with the `task` label, any length. The runner opens a planning packet (standard reasoning). The plan comes back as packets with dependencies and `ready` labels. If the planner cannot make it fit rule 15, the task goes to `needs-john` with the decomposition. |
| W1-2 GreenPT first pass | For content tasks the runner starts GreenPT on extraction or a first draft inside the per-issue limit, then opens the Claude authoring packet with the candidate attached. Private-path guard runs first (B2). |
| W1-3 Codex implementer | Codex implementation packets through the PR 13 receiver, `implement-and-open-pr`. The runner treats the PR exactly like a Claude one: Claude reviews it, fix loop, gate. This is the multi-direction John asked for. |
| W1-4 Escalation ladder | Per packet: GreenPT (where allowed), Codex, Claude standard, Claude premium only after a receipt shows the lower tier failed on the same evidence. Each step is a new packet written by the runner, bound to the failed receipt. |
| W1-5 Quota switch | Runner reads the month's counts from receipts and picks the provider with room. Stops the night when every route is capped and says so in the post. |

### Wave 2, what the old plan had

B1 to B14 become hardening on a loop that works. B9 shrinks to the four needs-John classes. B0 is subsumed by W0-3.

## 5. Rules that change, stated not asked

John's instruction on 7 November 2026 changes these standing rules. The build writes them into CLAUDE.md, AGENTS.md and Chauffeur's how-we-review.md as owner decisions.

| Rule today | Rule after |
|---|---|
| Only John merges. | The merge gate merges on the written criteria. John keeps the human gates: safety-critical lessons, anything to DVL, cap rises, public publication. |
| Rule 14: no delegated work from a chat; triggers only from John, a Claude session, Codex or GreenPT within caps. | The scheduler is a trigger origin, with its own app-started cap on every receipt. |
| Rule 15: a second candidate needs its own packet. | Unchanged. The runner writes the packet. |
| B9 digest without auto-approval. | Classes John has approved by rule are auto-approved. The digest holds the rest. |
| Chauffeur: "The owner decides merges." | Same change as the first row. The operational reviewer gate stays. |

## 6. What this costs and what is unknown

- Claude runs: the app-started cap is 250 a month per starting app. A fix loop of three rounds on ten packets a night is well inside it.
- GreenPT: EUR 10.00 a month, two calls and EUR 0.01 per issue. Unchanged.
- Codex: the shared OpenAI app-started cap. Unchanged.
- Money per night: `unknown` until the first full night's receipts exist. The morning post reports it from then on.
- Unverified: that the Codex reviewer app's findings can be parsed by login and SHA. Chauffeur's reviews show it pins to the commit; the parser is written against that and tested on the first real review.

## 7. Order of work from here

1. W0-1 to W0-4, W0-7: one draft PR on Content-Creation-Pipeline, the loop. Codex reviews it.
2. W0-5, W0-6, W0-9: second PR, the review and fix loop plus the post.
3. First supervised night on the harness repo's own wave 2 packets (#310, #315, #316, #317).
4. W1 on Chauffeur, where the review loop already works.
