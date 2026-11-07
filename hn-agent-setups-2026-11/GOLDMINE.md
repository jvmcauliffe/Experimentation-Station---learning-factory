# GOLDMINE: HN agent setups (regenerated from data)

Source: Ask HN, 'What's your current AI agentic setup?' (item 50366117), read 6 November 2026. Rubric v2: Priority = Impact × Fit × Confidence ÷ Effort (Effort = 6 − Ease). See `README.md`.

**Regeneration note (7 November 2026).** The original report was not committed. This version is rebuilt only from `data/projects_v2.json` by `tools/make_goldmine.py`. The camps, thread insights and quotes came from the synthesis step, which was not saved, so they are not here. For those see `routing-table.md` and `reddit-check.md`. Scores are from one Claude session; Codex has not scored blind.

## Counts

| Measure | Value |
|---|---|
| Projects scored | 111 |
| Ranked (Fit ≥ 2) | 86 |
| Gated (Fit 1) | 25 |

## By category

| Category | Projects |
|---|---|
| Uncategorised | 71 |
| Sessions | 9 |
| Orchestrators | 7 |
| Pipelines | 4 |
| Harnesses | 4 |
| Context | 4 |
| Sandboxing | 4 |
| Tickets | 3 |
| Built with agents | 3 |
| Ops | 2 |

## Top 20 by priority

| # | Project | Category | Impact | Ease | Fit | Working | Priority | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | [Handy](https://handy.computer) | Ops | 3 | 5 | 3 | 3×3×1.0÷1 = 9.0 | 9.0 | phone dictation already covers most of it |
| 2 | [Agent patterns graphs](https://graphs.univerlab.org/patterns) | Pipelines | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | pattern catalogue to read |
| 3 | [eamonn](https://eamonnsullivan.co.uk/posts/2026-10-20-retirement/) | Uncategorised | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | clear write-up of a cheap multi-model setup |
| 4 | [mattpocock/skills](https://github.com/mattpocock/skills) | Harnesses | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | skill examples to copy |
| 5 | [techaddo](https://techaddo.com/posts/ai-agentic-setups) | Uncategorised | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | running digest of this thread |
| 6 | [Claude Code TPP](https://photostructure.com/coding/claude-code-tpp/) | Context | 4 | 4 | 5 | 4×5×0.5÷2 = 5.0 | 5.0 | same idea as HANDOFF.md |
| 7 | [kiro](https://kiro.dev/docs/specs/) | Uncategorised | 3 | 4 | 3 | 3×3×1.0÷2 = 4.5 | 4.5 | spec-driven docs |
| 8 | [LLM usage page](https://a.l3x.in/usage) | Ops | 4 | 4 | 4 | 4×4×0.5÷2 = 4.0 | 4.0 | one page of balances: the cost board |
| 9 | [skills-sdlc](https://github.com/gregwebs/skills-sdlc) | Pipelines | 4 | 4 | 4 | 4×4×0.5÷2 = 4.0 | 4.0 | SDLC skills to adapt into packets |
| 10 | [Agent Kitchen](https://stack.yiin.lt) | Context | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 | "Ideas, not a recipe." A menu of setup ingredients you pick from, rather than a framework. |
| 11 | [caudradecisions](https://caudra.ai/features/decisions/) | Uncategorised | 3 | 4 | 4 | 3×4×0.5÷2 = 3.0 | 3.0 | decision log: same idea as DECISIONS.md |
| 12 | [Follow the Money](https://helyn.com/follow-the-money) | Pipelines | 3 | 4 | 4 | 3×4×0.5÷2 = 3.0 | 3.0 | reproducible process spec for content work |
| 13 | [gistot](https://gist.github.com/ontouchstart/b6a08b068cf863f0523bbd8880c88cf4) | Uncategorised | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 | session log to learn from |
| 14 | [gistvk](https://gist.github.com/vkalintiris/3ad526e71a75bcba013aaadc9d9d0837) | Uncategorised | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 | full agent trace to learn from |
| 15 | [How I use agents for work](https://dcferreira.com/post/2026-10-how-i-use-agents/) | Context | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 | A grounded, minimalist write-up: a few parallel tasks, plain tools, careful review. |
| 16 | [l3xai](https://a.l3x.in/ai) | Uncategorised | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 |  |
| 17 | [melious](https://melious.ai) | Uncategorised | 3 | 4 | 2 | 3×2×1.0÷2 = 3.0 | 3.0 | phillc73 provider: 4th provider, John decides |
| 18 | [OpenSpec](https://openspec.dev) | Pipelines | 3 | 4 | 4 | 3×4×0.5÷2 = 3.0 | 3.0 | spec before build, like a packet |
| 19 | [claudeflow](https://github.com/common-pattern/claudeflow) | Tickets | 4 | 3 | 4 | 4×4×0.5÷3 = 2.7 | 2.7 | issue labels drive the agent: close to your packets |
| 20 | [deepinfra](https://deepinfra.com/) | Uncategorised | 3 | 4 | 2 | 3×2×0.8÷2 = 2.4 | 2.4 | provider: 4th provider, John decides |

## Supervisory and orchestration projects (ranked)

| # | Project | Category | Impact | Ease | Fit | Working | Priority | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | [Agent patterns graphs](https://graphs.univerlab.org/patterns) | Pipelines | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | pattern catalogue to read |
| 2 | [mattpocock/skills](https://github.com/mattpocock/skills) | Harnesses | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | skill examples to copy |
| 3 | [skills-sdlc](https://github.com/gregwebs/skills-sdlc) | Pipelines | 4 | 4 | 4 | 4×4×0.5÷2 = 4.0 | 4.0 | SDLC skills to adapt into packets |
| 4 | [Follow the Money](https://helyn.com/follow-the-money) | Pipelines | 3 | 4 | 4 | 3×4×0.5÷2 = 3.0 | 3.0 | reproducible process spec for content work |
| 5 | [OpenSpec](https://openspec.dev) | Pipelines | 3 | 4 | 4 | 3×4×0.5÷2 = 3.0 | 3.0 | spec before build, like a packet |
| 6 | [claudeflow](https://github.com/common-pattern/claudeflow) | Tickets | 4 | 3 | 4 | 4×4×0.5÷3 = 2.7 | 2.7 | issue labels drive the agent: close to your packets |
| 7 | [Kan](https://github.com/amterp/kan) | Tickets | 3 | 4 | 2 | 3×2×0.8÷2 = 2.4 | 2.4 | GitHub issues already do this |
| 8 | [maki](https://maki.sh) | Harnesses | 3 | 3 | 2 | 3×2×1.0÷3 = 2.0 | 2.0 | harness swap is a policy change |
| 9 | [Pi](https://pi.dev) | Harnesses | 3 | 3 | 2 | 3×2×1.0÷3 = 2.0 | 2.0 | harness swap is a policy change |
| 10 | [neal](https://github.com/navels/neal) | Orchestrators | 3 | 3 | 3 | 3×3×0.5÷3 = 1.5 | 1.5 | planner / executor / reviewer split |
| 11 | [nova-sprint live board](http://37.27.135.206) | Orchestrators | 3 | 3 | 3 | 3×3×0.5÷3 = 1.5 | 1.5 | tiered sprint board: idea for a packet dashboard |
| 12 | [Circus-Chief](https://github.com/ferrislucas/Circus-Chief) | Orchestrators | 3 | 2 | 3 | 3×3×0.5÷4 = 1.1 | 1.1 | multi-provider meta-harness |
| 13 | [nova-sprint repo](https://github.com/mas-bandwidth/nova-sprint) | Orchestrators | 3 | 2 | 3 | 3×3×0.5÷4 = 1.1 | 1.1 | tier escalation code |
| 14 | [jiraude](https://github.com/kuba97531/jiraude) | Tickets | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 | A ticketing system built for Claude Code sessions. |
| 15 | [remuda](https://github.com/yendo-eng/remuda) | Harnesses | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 | A CLI to make AI-assisted development low friction. |
| 16 | [Coterie](https://github.com/ASIXicle/Coterie) | Orchestrators | 2 | 2 | 2 | 2×2×0.5÷4 = 0.5 | 0.5 | Self-hosted team of persistent Claude Code agents, each with its own role. |
| 17 | [optio](https://github.com/jonwiggins/optio) | Orchestrators | 2 | 2 | 2 | 2×2×0.5÷4 = 0.5 | 0.5 | Workflow orchestration for AI agents, with issue-to-PR pipelines. |
| 18 | [spool](https://github.com/enes-alatas/spool) | Orchestrators | 2 | 2 | 2 | 2×2×0.5÷4 = 0.5 | 0.5 | A fleet of persistent Claude Code coworkers you talk to in Telegram and Slack. |

## Gated: Fit 1, not ranked

| Project | Category | What |
|---|---|---|
| [coolwalk](https://wooten-labs.com/coolwalk) | Uncategorised |  |
| [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi) | Uncategorised | pools free APIs: terms risk |
| [mas-bandwidth/fixed](https://github.com/mas-bandwidth/fixed) | Uncategorised |  |
| [muster](https://github.com/amterp/muster) | Sessions | A native macOS workspace for agents with tab splits and agent states. Mac only. |
| [tix](https://tix.im/) | Uncategorised |  |
| [svall](https://svall.dev/) | Uncategorised |  |
| [rolloutrhino](https://rolloutrhino.com/) | Uncategorised |  |
| [musterweb](https://muster.town/) | Uncategorised |  |
| [magenta](https://magenta.cryptograss.live/) | Uncategorised |  |
| [seanturner026/f](https://github.com/seanturner026/f) | Uncategorised |  |
| [regnull/openbot](https://github.com/regnull/openbot) | Uncategorised |  |
| [morluto/rea](https://github.com/morluto/rea) | Uncategorised |  |
| [mkornreich/llm-desktop-electron](https://github.com/mkornreich/llm-desktop-electron) | Uncategorised |  |
| [mickael-kerjean/filestash](https://github.com/mickael-kerjean/filestash) | Uncategorised |  |
| [mickael-kerjean/fdrive](https://github.com/mickael-kerjean/fdrive) | Uncategorised |  |
| [mas-bandwidth/schema](https://github.com/mas-bandwidth/schema) | Uncategorised |  |
| [mas-bandwidth/fixed3d](https://github.com/mas-bandwidth/fixed3d) | Uncategorised |  |
| [kuyawa/jobs-lang](https://github.com/kuyawa/jobs-lang) | Uncategorised |  |
| [getspur/SpurCode](https://github.com/getspur/SpurCode) | Uncategorised |  |
| [fluxmoot/fluximp](https://github.com/fluxmoot/fluximp) | Uncategorised |  |
| [containers/bubblewrap](https://github.com/containers/bubblewrap) | Uncategorised | cloud sandbox already covers it |
| [capocasa/3code](https://github.com/capocasa/3code) | Uncategorised |  |
| [8lamaster8/GIN](https://github.com/8lamaster8/GIN) | Uncategorised |  |
| [spurlab](https://getspur.dev/spurlab) | Uncategorised |  |
| [tensorninja/ninfer-4090](https://github.com/tensorninja/ninfer-4090) | Uncategorised | needs a local 4090 |

## Full ranking

| # | Project | Category | Impact | Ease | Fit | Working | Priority | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | [Handy](https://handy.computer) | Ops | 3 | 5 | 3 | 3×3×1.0÷1 = 9.0 | 9.0 | phone dictation already covers most of it |
| 2 | [Agent patterns graphs](https://graphs.univerlab.org/patterns) | Pipelines | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | pattern catalogue to read |
| 3 | [eamonn](https://eamonnsullivan.co.uk/posts/2026-10-20-retirement/) | Uncategorised | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | clear write-up of a cheap multi-model setup |
| 4 | [mattpocock/skills](https://github.com/mattpocock/skills) | Harnesses | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | skill examples to copy |
| 5 | [techaddo](https://techaddo.com/posts/ai-agentic-setups) | Uncategorised | 3 | 5 | 4 | 3×4×0.5÷1 = 6.0 | 6.0 | running digest of this thread |
| 6 | [Claude Code TPP](https://photostructure.com/coding/claude-code-tpp/) | Context | 4 | 4 | 5 | 4×5×0.5÷2 = 5.0 | 5.0 | same idea as HANDOFF.md |
| 7 | [kiro](https://kiro.dev/docs/specs/) | Uncategorised | 3 | 4 | 3 | 3×3×1.0÷2 = 4.5 | 4.5 | spec-driven docs |
| 8 | [LLM usage page](https://a.l3x.in/usage) | Ops | 4 | 4 | 4 | 4×4×0.5÷2 = 4.0 | 4.0 | one page of balances: the cost board |
| 9 | [skills-sdlc](https://github.com/gregwebs/skills-sdlc) | Pipelines | 4 | 4 | 4 | 4×4×0.5÷2 = 4.0 | 4.0 | SDLC skills to adapt into packets |
| 10 | [Agent Kitchen](https://stack.yiin.lt) | Context | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 | "Ideas, not a recipe." A menu of setup ingredients you pick from, rather than a framework. |
| 11 | [caudradecisions](https://caudra.ai/features/decisions/) | Uncategorised | 3 | 4 | 4 | 3×4×0.5÷2 = 3.0 | 3.0 | decision log: same idea as DECISIONS.md |
| 12 | [Follow the Money](https://helyn.com/follow-the-money) | Pipelines | 3 | 4 | 4 | 3×4×0.5÷2 = 3.0 | 3.0 | reproducible process spec for content work |
| 13 | [gistot](https://gist.github.com/ontouchstart/b6a08b068cf863f0523bbd8880c88cf4) | Uncategorised | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 | session log to learn from |
| 14 | [gistvk](https://gist.github.com/vkalintiris/3ad526e71a75bcba013aaadc9d9d0837) | Uncategorised | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 | full agent trace to learn from |
| 15 | [How I use agents for work](https://dcferreira.com/post/2026-10-how-i-use-agents/) | Context | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 | A grounded, minimalist write-up: a few parallel tasks, plain tools, careful review. |
| 16 | [l3xai](https://a.l3x.in/ai) | Uncategorised | 2 | 5 | 3 | 2×3×0.5÷1 = 3.0 | 3.0 |  |
| 17 | [melious](https://melious.ai) | Uncategorised | 3 | 4 | 2 | 3×2×1.0÷2 = 3.0 | 3.0 | phillc73 provider: 4th provider, John decides |
| 18 | [OpenSpec](https://openspec.dev) | Pipelines | 3 | 4 | 4 | 3×4×0.5÷2 = 3.0 | 3.0 | spec before build, like a packet |
| 19 | [claudeflow](https://github.com/common-pattern/claudeflow) | Tickets | 4 | 3 | 4 | 4×4×0.5÷3 = 2.7 | 2.7 | issue labels drive the agent: close to your packets |
| 20 | [deepinfra](https://deepinfra.com/) | Uncategorised | 3 | 4 | 2 | 3×2×0.8÷2 = 2.4 | 2.4 | provider: 4th provider, John decides |
| 21 | [Kan](https://github.com/amterp/kan) | Tickets | 3 | 4 | 2 | 3×2×0.8÷2 = 2.4 | 2.4 | GitHub issues already do this |
| 22 | [conductor](https://www.conductor.build/) | Uncategorised | 2 | 4 | 2 | 2×2×1.0÷2 = 2.0 | 2.0 | macOS app |
| 23 | [Herdr](https://herdr.dev) | Sessions | 2 | 4 | 2 | 2×2×1.0÷2 = 2.0 | 2.0 | terminal app; you work from a phone |
| 24 | [maki](https://maki.sh) | Harnesses | 3 | 3 | 2 | 3×2×1.0÷3 = 2.0 | 2.0 | harness swap is a policy change |
| 25 | [Pi](https://pi.dev) | Harnesses | 3 | 3 | 2 | 3×2×1.0÷3 = 2.0 | 2.0 | harness swap is a policy change |
| 26 | [shaftoe/awesome-pi-coding-agent](https://github.com/shaftoe/awesome-pi-coding-agent/) | Uncategorised | 2 | 5 | 2 | 2×2×0.5÷1 = 2.0 | 2.0 |  |
| 27 | [warp](https://www.warp.dev/) | Uncategorised | 2 | 4 | 2 | 2×2×0.8÷2 = 1.6 | 1.6 |  |
| 28 | [Wooten Labs](https://wooten-labs.com) | Built with agents | 1 | 5 | 2 | 1×2×0.8÷1 = 1.6 | 1.6 | A collection of small apps built with agents. Charming pixel-art landing page. |
| 29 | [entrim](https://entrim.ai) | Uncategorised | 3 | 4 | 2 | 3×2×0.5÷2 = 1.5 | 1.5 | phillc73 provider: 4th provider, John decides |
| 30 | [gregwebs/pi-quota-dispatcher](https://github.com/gregwebs/pi-quota-dispatcher) | Uncategorised | 3 | 3 | 3 | 3×3×0.5÷3 = 1.5 | 1.5 | switch provider when quota runs low |
| 31 | [gszr/lunar](https://github.com/gszr/lunar) | Uncategorised | 3 | 3 | 3 | 3×3×0.5÷3 = 1.5 | 1.5 | switch subscriptions mid-session |
| 32 | [Levels of agent use](https://virpo.io/levels) | Context | 1 | 5 | 3 | 1×3×0.5÷1 = 1.5 | 1.5 | A playful self-assessment of how far along you are with agents. Good for calibrating where |
| 33 | [mas-bandwidth/nova-tools](https://github.com/mas-bandwidth/nova-tools) | Uncategorised | 3 | 3 | 3 | 3×3×0.5÷3 = 1.5 | 1.5 | simple message bus: compare with the PR 13 inbox |
| 34 | [neal](https://github.com/navels/neal) | Orchestrators | 3 | 3 | 3 | 3×3×0.5÷3 = 1.5 | 1.5 | planner / executor / reviewer split |
| 35 | [nova-sprint live board](http://37.27.135.206) | Orchestrators | 3 | 3 | 3 | 3×3×0.5÷3 = 1.5 | 1.5 | tiered sprint board: idea for a packet dashboard |
| 36 | [opencodego](https://opencode.ai/console/go) | Uncategorised | 3 | 4 | 2 | 3×2×0.5÷2 = 1.5 | 1.5 | cheap model plan: 4th provider, John decides |
| 37 | [Sandboxes favor repo-native tooling](https://epiq.sh/blog/repo-native-tooling-for-sandboxes) | Sandboxing | 2 | 4 | 3 | 2×3×0.5÷2 = 1.5 | 1.5 | Argues for keeping tooling inside the repo so sandboxed agents need no host setup. Relevan |
| 38 | [toolscaled](https://app.toolscaled.com/docs/agents/how-agents-work/) | Uncategorised | 2 | 4 | 3 | 2×3×0.5÷2 = 1.5 | 1.5 |  |
| 39 | [goose](https://goose-docs.ai) | Uncategorised | 2 | 3 | 2 | 2×2×1.0÷3 = 1.3 | 1.3 |  |
| 40 | [kilo](https://kilo.ai) | Uncategorised | 2 | 3 | 2 | 2×2×1.0÷3 = 1.3 | 1.3 |  |
| 41 | [Orca](https://onorca.dev) | Sessions | 2 | 3 | 2 | 2×2×1.0÷3 = 1.3 | 1.3 | An agent IDE: parallel Claude Code and Codex sessions with worktrees and review panes. |
| 42 | [Paseo](https://paseo.sh) | Sessions | 2 | 3 | 2 | 2×2×1.0÷3 = 1.3 | 1.3 | An agentic development environment: many agents, one machine, phone access. |
| 43 | [T3 Code](https://t3.codes) | Sessions | 2 | 3 | 2 | 2×2×1.0÷3 = 1.3 | 1.3 | An open-source control plane for Claude Code, Codex, OpenCode and others. |
| 44 | [Circus-Chief](https://github.com/ferrislucas/Circus-Chief) | Orchestrators | 3 | 2 | 3 | 3×3×0.5÷4 = 1.1 | 1.1 | multi-provider meta-harness |
| 45 | [eca](https://eca.dev/) | Uncategorised | 2 | 3 | 2 | 2×2×0.8÷3 = 1.1 | 1.1 |  |
| 46 | [epiqhome](https://epiq.sh) | Uncategorised | 2 | 3 | 2 | 2×2×0.8÷3 = 1.1 | 1.1 |  |
| 47 | [juggler](https://github.com/juggler-ai/juggler) | Sessions | 2 | 3 | 2 | 2×2×0.8÷3 = 1.1 | 1.1 | A coding-agent app for juggling many parallel tasks. |
| 48 | [nodecode](https://nodecode.ai/) | Uncategorised | 2 | 3 | 2 | 2×2×0.8÷3 = 1.1 | 1.1 |  |
| 49 | [nova-sprint repo](https://github.com/mas-bandwidth/nova-sprint) | Orchestrators | 3 | 2 | 3 | 3×3×0.5÷4 = 1.1 | 1.1 | tier escalation code |
| 50 | [herdrtui](https://herdr.dev/tui/) | Uncategorised | 2 | 4 | 2 | 2×2×0.5÷2 = 1.0 | 1.0 |  |
| 51 | [pise](https://codeberg.org/dannyfritz/dotfiles/src/commit/f5d082d285ff40f35b4d140816f48e637f3c95ad/bin/pise) | Uncategorised | 2 | 4 | 2 | 2×2×0.5÷2 = 1.0 | 1.0 |  |
| 52 | [quarterdeck](https://github.com/oscscull/quarterdeck) | Built with agents | 1 | 5 | 2 | 1×2×0.5÷1 = 1.0 | 1.0 | A Tauri + Rust day scheduler built with agents. |
| 53 | [stonks](https://stonks.jettdigital.app) | Built with agents | 1 | 5 | 2 | 1×2×0.5÷1 = 1.0 | 1.0 | A portfolio leaderboard app built with agents, to show what one person can now ship. |
| 54 | [yoloai](https://github.com/kstenerud/yoloai) | Sandboxing | 3 | 3 | 2 | 3×2×0.5÷3 = 1.0 | 1.0 | cloud proxy already injects keys |
| 55 | [openhands](https://www.openhands.dev/) | Uncategorised | 2 | 2 | 2 | 2×2×0.8÷4 = 0.8 | 0.8 |  |
| 56 | [amp](https://ampcode.com/) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 57 | [belfry](https://belfry.robgough.net) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 58 | [bsklaroff/yaac](https://github.com/bsklaroff/yaac) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 59 | [codealong/codealong](https://github.com/codealong/codealong) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 60 | [ctlflow](https://www.ctlflow.com) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 61 | [devarch](https://devarch.ai/) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 62 | [Docker Sandboxes](https://www.docker.com/products/docker-sandboxes/) | Sandboxing | 1 | 3 | 2 | 1×2×1.0÷3 = 0.7 | 0.7 | MicroVM sandboxes for Claude Code, Codex and others, from local to cloud. |
| 63 | [droneship](https://www.droneship.run) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 64 | [filestashagents](https://www.filestash.app/agents/) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 65 | [gi-dellav/zerostack](https://github.com/gi-dellav/zerostack) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 66 | [GulDmitry/jagt](https://github.com/GulDmitry/jagt) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 67 | [hangar](https://github.com/jeffer1312/hangar) | Sessions | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 | All your coding agents in one place, across Claude Code, Codex and Cursor. |
| 68 | [jail](https://github.com/andrei-dubovik/jail) | Sandboxing | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 | cloud sandbox already covers it |
| 69 | [jiraude](https://github.com/kuba97531/jiraude) | Tickets | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 | A ticketing system built for Claude Code sessions. |
| 70 | [laughingmandev/loa](https://github.com/laughingmandev/loa) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 71 | [mhalstrom/maximizepm](https://github.com/mhalstrom/maximizepm) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 72 | [mitchellgordon95/miniclaw](https://github.com/mitchellgordon95/miniclaw) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 73 | [obeya](https://github.com/sadilek/obeya) | Sessions | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 | A spatial workspace for directing coding agents as you would an engineering team. |
| 74 | [PAndreew/pi_group](https://github.com/PAndreew/pi_group) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 75 | [remuda](https://github.com/yendo-eng/remuda) | Harnesses | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 | A CLI to make AI-assisted development low friction. |
| 76 | [resolveworks/key](https://github.com/resolveworks/key) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 77 | [sharkjets/iceghost](https://github.com/sharkjets/iceghost) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 78 | [usehax](https://usehax.dev/) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 79 | [vectorstep](https://vectorstep.io) | Uncategorised | 2 | 3 | 2 | 2×2×0.5÷3 = 0.7 | 0.7 |  |
| 80 | [agenta-ai/agenta](https://github.com/agenta-ai/agenta) | Uncategorised | 2 | 2 | 2 | 2×2×0.5÷4 = 0.5 | 0.5 |  |
| 81 | [caudra/caudra](https://github.com/caudra/caudra) | Uncategorised | 2 | 2 | 2 | 2×2×0.5÷4 = 0.5 | 0.5 |  |
| 82 | [Coterie](https://github.com/ASIXicle/Coterie) | Orchestrators | 2 | 2 | 2 | 2×2×0.5÷4 = 0.5 | 0.5 | Self-hosted team of persistent Claude Code agents, each with its own role. |
| 83 | [optio](https://github.com/jonwiggins/optio) | Orchestrators | 2 | 2 | 2 | 2×2×0.5÷4 = 0.5 | 0.5 | Workflow orchestration for AI agents, with issue-to-PR pipelines. |
| 84 | [sleeperservice](https://sleeperservice.io/) | Uncategorised | 2 | 2 | 2 | 2×2×0.5÷4 = 0.5 | 0.5 |  |
| 85 | [spool](https://github.com/enes-alatas/spool) | Orchestrators | 2 | 2 | 2 | 2×2×0.5÷4 = 0.5 | 0.5 | A fleet of persistent Claude Code coworkers you talk to in Telegram and Slack. |
| 86 | [humbug](https://github.com/m6r-ai/humbug) | Sessions | 1 | 2 | 2 | 1×2×0.5÷4 = 0.2 | 0.2 | An "operating system for human-AI collaboration" with its own editor and shell. |
