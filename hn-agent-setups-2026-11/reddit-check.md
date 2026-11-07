## The Reddit summary, checked against the retained 677-comment snapshot

Source: r/AI_Agents post by michaelTM_ai, "cheap open models at home, frontier as the second opinion, and nobody trusts the agent platforms". The poster says they read "the top 45 or so" of about 475 comments. The original 645-comment count was not reproducible because its regexes and snapshot were not retained together. The counts below were rerun on 7 November 2026 against `verify/thread.json`: 677 comments with text, SHA-256 `8086b4e2955adc1f4e238ad848c032d2499392fa67382016b78da3b4804a6458`. They count comments containing a term, not unique people or measured adoption. HTML tags are stripped, entities decoded and text lowercased. Exact patterns are in `verify/cnt.py`; rerun with `python3 -I verify/cnt.py verify/thread.json`. A fresh Algolia fetch returned HTTP 403 in this environment, so these are retained-snapshot counts, not a live census.

| # | Reddit claim | Verdict | Evidence |
|---|---|---|---|
| 1 | DeepSeek Flash came up more than any frontier model in personal setups | **Partly true** | DeepSeek appears in 89 comments, the most of any open model (Qwen 55, GLM 47, Kimi 14). It is level with Opus (89) and well behind GPT/Codex (184) and Claude Code (138). Keyword counts cannot separate personal setups from work setups. |
| 2 | $10 OpenCode Go plan, or pay as you go through OpenRouter | **True** | OpenCode Go appears in 28 comments and OpenRouter in 67. |
| 3 | "Never run out of tokens" | **True** | AaronAPU #50368566: "I never come close to running out of tokens because I still do code reviews often enough to throttle usage." The reason is that reviewing the code themselves slows their usage, not that the plan is cheap. |
| 4 | Frontier models are becoming the second opinion | **True, but a minority** | Examples: ActionHank #50379104 makes an "Occasional call out to claude for a review on a large change", drbscl #50367676 uses one "mostly for review, second opinion", Xonzo #50378776 uses "Sol 6.1 xHigh for planning/review", and codingbear #50367207 uses Claude "for tricky bits". More commenters go the other way and let a single Opus 5.5 session do everything (thefourthchime #50367037, l9o #50368019, FrameworkFred #50379612). |
| 5 | Harnesses are getting smaller; the top comment deleted his skills, set Opus to medium and tells it what done looks like | **True** | thefourthchime #50367037, which is the first top-level comment: "I got rid of all my skills and just set it to medium… the biggest trick is just to tell it what complete looks like." pi appears in 89 comments and OpenCode in 94. |
| 6 | Almost nobody trusts all-in-one agent platforms; OpenClaw and Hermes "fell apart on real work" | **Half wrong** | OpenClaw (37 comments) is mostly "tried it, dropped it": nkotov, vekker, SkidVis, leofree, egrm and others. **Hermes (55 comments) has a loyal user base**, mostly as an always-on personal assistant on a Mac Mini or homelab that people reach by Telegram. browningstreet calls it "core tech for me", and vekker, virpo, Xonzo, diseasedyak, monch1962, hestefisk and ddarolfi are also users. ActionHank says "Hermes Kanban works stupidly well". |
| 7 | Orchestration is still a human with 3–5 terminal panes | **True** | phillc73 #50367557 runs "a multipane Zellij setup… Orchestration is still human in the loop", m_w_ #50379312 runs 5–6 sessions, anigbrowl #50375427 runs 3–4 projects, and marshalla runs at most 3. tmux appears in 18 comments. |
| 8 | Someone types junk into idle sessions every 30–45 minutes so the cache doesn't expire | **True** | marshalla #50367399 types "silly things into some of them every 30-45 min so they don't expire or auto-compact". |
| 9 | "Bragging about multiple subscriptions without saying what they use them for" | **True** | ChrisRR #50367618, quoted word for word. |
| 10 | "GLM flash for coordination, deepseek for coding and GLM for adversarial review: the part worth copying" | **True** | phillc73 #50367557: "GLM5.3 Flash for general chat and co-ordination… Deepseek 1017 for most coding… GML5.3 [sic] for adversarial batteries and documentation." ActionHank #50379104 is close: "Hermes + GLM 5.3 Flash for orchestration. omp + Deepseek 4.1 Flash for coding. Occasional call out to claude for a review on a large change." |

**Table labels: 8 true (including one qualified as a minority), 1 partly true, 1 half wrong.** The post is a fair summary of the top of the thread. Its one real error is lumping Hermes in with OpenClaw.

### What the Reddit summary means for John's harness

- **Claim 10 is your three-provider design**, found independently by someone else. phillc73 also uses mechanical gates, for example "remote git pushes without explicit prior approval", which match your PreToolUse hooks. Worth copying from them: **one written table of roles and models**, with a single line per role: coordination, coding, adversarial review and documentation. Today your routes (bounded_extraction, standard_reasoning, highest_reasoning) say how hard a job is, not which job it is.
- **Claim 8 costs you money too.** This comment does not establish the cache lifetime or billing of your sessions. Do not send filler simply to keep a cache warm; cache behaviour is provider- and product-specific. Keep sessions short and hand over through GitHub issues, which you already do.
- **Claim 6: Hermes is the one platform people keep.** If you ever want a phone-reachable assistant that is always on, Hermes on a spare machine is the pattern the thread recommends. It sits outside your packet rules, so it would be a separate experiment.


### Exact term patterns

One count per text-bearing comment per case-insensitive pattern after lowercasing. Literal substrings unless shown with a regex boundary:

| Term | Pattern | Count |
|---|---|---|
| DeepSeek (headline) | `deepseek` | 89 |
| DeepSeek (expanded) | `deepseek` or `deep seek` or regex `\bds\s?v?4` | 97 |
| Qwen / GLM / Kimi | `qwen` / `glm` / `kimi` | 55 / 47 / 14 |
| Opus / Claude Code | `opus` / `claude code` | 89 / 138 |
| GPT or Codex | `gpt` or `codex` | 184 |
| OpenCode Go / OpenRouter / OpenCode | `opencode go` / `openrouter` / `opencode` | 28 / 67 / 94 |
| OpenClaw / Hermes / tmux | `openclaw` / `hermes` / `tmux` | 37 / 55 / 18 |
| Pi | regex `\bpi\b` or `pi\.dev` | 89 |
