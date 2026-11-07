# Codex verification of the HN insight handover

Verified 7 November 2026 from Experimentation-Station main `ca5801e5bd5c5d1bd3eb822c2427ffb02e9fc7c8`. This is a source-fidelity and coverage review, not acceptance of the proposed harness changes or a benchmark of any product.

## Evidence and limits

Retained `verify/thread.json` SHA-256: `8086b4e2955adc1f4e238ad848c032d2499392fa67382016b78da3b4804a6458`; 677 text-bearing comments. A fresh Algolia request returned HTTP 403, so no live-snapshot claim is made. All cited texts for the remaining 30 insights were read without truncation. The prior `full.py` silently capped text at 2200 characters; that cap is removed. `check.py` now resolves GOLDMINE relative to itself rather than a different machine's home directory.

The 56 insight records cite **137 distinct comments**, not 216. The wider GOLDMINE cites 216 distinct IDs; that is a different denominator. Every wider ID exists in the retained snapshot. The regex quote/author checker produces false positives (ordinary words before IDs, paired table quotes, `[sic]`); its raw counts are not an independent quote-fidelity verdict.

## Remaining 30 insights: full-text findings

All 30 have source support as attributed reports or practices. That does not establish universal effectiveness, correctness, savings or safety. Existing scores and numbering are retained; this review does not independently re-score them.

| Insight | Full cited comments read | Finding |
|---|---|---|
| 3 | #50373445, #50373364, #50376279 | Supported as an attributed practice; no independent effectiveness claim. |
| 15 | #50384236, #50378336 | Supported as an attributed practice; no independent effectiveness claim. |
| 17 | #50378157, #50367326, #50367587 | Includes a self-promoting workflow report; resumability is claimed, not exercised here. |
| 18 | #50367589, #50373357, #50375084, #50376087 | All cited prose complaints read, including the entire long 50373357 comment. |
| 20 | #50381117, #50375427, #50385251, #50376778, #50377633, #50375326 | Cost figures are self-reports; cache/subscription allowances are not comparable cash prices. |
| 21 | #50373974, #50374380, #50374094 | Scheduled issue handoff is explicit in 50373974; other sources give related variants. |
| 23 | #50375274, #50377952 | Supported as an attributed practice; no independent effectiveness claim. |
| 26 | #50373796, #50378479 | Only 50373796 explicitly distinguishes done and needs-answer sounds. |
| 28 | #50373684, #50388928, #50373985, #50367876 | Transport examples support possibility, not guaranteed reliable delivery. |
| 29 | #50374380, #50377004, #50376177 | Supported as an attributed practice; no independent effectiveness claim. |
| 31 | #50380005 | One person reports effectiveness; replace universal "kills" with attributed experience. |
| 32 | #50380633 | One protocol author describes it; no independent quality benchmark. |
| 33 | #50376058, #50384746 | Supported as an attributed practice; no independent effectiveness claim. |
| 36 | #50367557 | Supported as an attributed practice; no independent effectiveness claim. |
| 37 | #50375921, #50377263, #50376262 | Advice/opinion, not a proven prohibition on within-project concurrency. |
| 39 | #50385812, #50380777 | Overnight research and a separate daily-blog example, not proof of this harness. |
| 40 | #50373236, #50390416, #50375890, #50378487 | Self-described concern and replies; no clinical conclusion. Uncited 50374646 supplies a counter-perspective. |
| 41 | #50379808 | Supported as an attributed practice; no independent effectiveness claim. |
| 43 | #50375606 | Fleet author reports a cleanup need; not a general defect-rate measurement. |
| 45 | #50374764 | Supported as an attributed practice; no independent effectiveness claim. |
| 46 | #50385555 | Vendor-affiliated source; returning-persona benefit is anecdotal. |
| 48 | #50380990 | Creator reports own capacity scheduler; no new spend or work authority. |
| 49 | #50380164, #50383403 | Two reported incidents; no controlled sandbox exploit reproduced. |
| 50 | #50374417, #50374455, #50374764, #50375312, #50376505 | Observed provider-switching practice, not a recommendation to bypass a refusal or existing policy. |
| 51 | #50378856, #50378737, #50374678, #50379150 | Supports switching; multiple cited authors promote their own products. |
| 52 | #50376476 | One user reports task drift; simple messaging itself is not prohibited. |
| 53 | #50382792 | Supported as an attributed practice; no independent effectiveness claim. |
| 54 | #50377284 | Single-user perception on their task mix, not a model-ranking result. |
| 55 | #50376216 | Explicit test-environment browser/fix iterations. |
| 56 | #50376601, #50377290, #50370886 | Three sources support reduced use; other comments report useful assistants. Not universal. |

## Are the 56 the right ones?

They are a useful, overlapping taxonomy, **not an exhaustive or uniquely optimal selection**. Six omissions/extensions were added as unranked insights 57–62 at John's direct request. Their structured records are in `data/coverage_insights.json`:

1. Observable completion criteria and plan-to-output checks (50367037, 50399014): extend 14/24. This is directly relevant to avoiding acknowledgement-only work.
2. Durable mechanical dispatch and ownership of unfinished work (50393739, 50375407): extend 17/23/38. Notifications and an enabled subscription alone do not finish tasks.
3. Recovery from agent damage with independent backups and VM snapshots (50378897): missing from isolation-only treatment; add as a candidate security/reliability practice, not a claim that a backup was tested here.
4. Stakeholder decision load and explainable data/RBAC rationale (50376110, 50377328): extend 16. Width is not the only human bottleneck; a new UI does not remove accountability.
5. Business-invariant modelling in a smaller domain language (50367941): an optional architecture experiment, distinct from prose instructions. One anecdote is insufficient for a top-ranked recommendation.
6. Provider continuity/account recovery (50376720 versus 50395473): record contested risk; neither comment verifies actual provider policy or ban probabilities.

No automatic new implementation, model purchase, cap change or reranking follows from adding these insights. Existing disagreements cover personal-agent usefulness, model cost and minimalism, but the headlines must retain those counterexamples. In particular 50373248, 50377455 and 50368640 contradict a universal reading of insight 56, and 50374646 qualifies the burnout framing.

### Reproducible coverage sample

`python3 -I verify/coverage.py verify/thread.json data/synthesis_v2.json` excludes the root and comments cited by any top insight, retains decoded plain text of at least 600 characters, and sorts by direct replies descending, practice-marker matches descending, character length descending, then ID ascending. Markers: `i have|my workflow|unlock|game changer|never|always` (case insensitive). There are 118 qualifying comments; the first 60 were read in full. This intentionally favours substantial, replied-to reports; it does not cover the remaining 58 substantial comments, all short comments, deleted text or later additions. It cannot prove exhaustive coverage. Dispositions and full-text hashes are in `verify/coverage-review.json`.

| Comment | Disposition | Reason |
|---|---|---|
| #50376720 (Animats) | gap | Provider continuity/account recovery risk; contested by 50395473, not a verified ban-rate claim. |
| #50367037 (thefourthchime) | extend 14,24 | Explicit observable completion criteria before work, not merely an implementation spec. |
| #50377492 (OSaMaBiNLoGiN) | covered 19,22,40 | Minimalism and professional identity; no new operational method. |
| #50380973 (vvilliamperez) | covered 29,55 | Remote phone workflow plus device testing. |
| #50373324 (jeswin) | covered 2,4,28 | Coordinator and cross-provider workers. |
| #50378366 (creativeSlumber) | covered 20; disagreement 4 | Cheap-provider claim with a quoted parent; not measured cost evidence. |
| #50378067 (eamonnsullivan) | covered 10,20 | Budget and provider flexibility; personal tool choice. |
| #50376110 (teekert) | extend 16; gap | Stakeholder decision load, visual schema/RBAC aids; also public-data automation and VLAN isolation. |
| #50377554 (jvidalv) | covered 29,53 | App/PR interface preference, no new repeatable harness invariant. |
| #50374090 (thefunnyman) | covered 25,42,49 | Least privilege and external microVM implementation. |
| #50367546 (dewey) | extend 28,37 | Explicit cross-repository dependency coordination. |
| #50375966 (mickeyp) | covered 22; local-model camp | Harness preference and local model. |
| #50378790 (Kuyawa) | out of scope | Language experiment; model claims about itself are not validation. |
| #50377286 (stinos) | covered 17,22 | Automate repetitive work with a minimal local setup. |
| #50376993 (walrus01) | covered 11; local-model camp | Local-only trust preference. |
| #50373698 (mgiampapa) | covered 39; personal-agent camp | Research and recordkeeping; financial outcome not independently verified. |
| #50373649 (keithnz) | covered 2,29 | Project manager/front door; no specific new control. |
| #50388891 (hosteur) | covered 5,19,20 | Good-enough model and task-fit question. |
| #50368640 (robgough) | covered 29,49; personal-agent camp | Remote availability and chores; reports of value counter universal dismissal. |
| #50380647 (bloppe) | extend 53,55 | Choose an inspectable, instrumentable UI substrate for browser automation. |
| #50377328 (teekert) | gap | Retain stakeholder-facing data/RBAC rationale; throughput does not remove accountable decisions. |
| #50393807 (glennfiedler) | covered 23,38 | Durable structured work graph, avoiding repeated API queries. |
| #50377449 (crisopolis) | covered 2,4,33 | Lead-mediated product/engineering teams. |
| #50376652 (gogoro) | covered 29,49 | Remote isolated compute. |
| #50370525 (warpspin) | covered 19,49 | Sandbox usability/reliability counter-evidence; not a new gate. |
| #50375873 (peepee1982) | covered 10,26,29,53 | Session UI, telemetry and diff navigation. |
| #50393739 (glennfiedler) | extend 17,23,38 | Mechanical durable dispatch prevents forgotten/half-started tasks; push notifications sustain work. |
| #50374261 (seanmcdirmid) | covered 5,19,24 | Spec-driven RPC orchestration and benchmarking. |
| #50379779 (lubonay) | extend 19,22 | Re-evaluate default tools periodically rather than preserving an obsolete verdict. |
| #50367571 (nkotov) | covered 5,22,56; disagreement 12 | Task-specific provider strengths; personal-agent failure report. |
| #50385840 (degrees57) | out of scope | One hardware-specific guided repair; no general harness practice. |
| #50367941 (sim04ful) | gap; optional | Domain-specific language/substrate enforces business invariants; different from adding prose rules. |
| #50367434 (CBLT) | covered 2,4 | One orchestrator owns cross-harness toil. |
| #50373956 (paustint) | covered 26,29,33,41,53 | Alerts, remote worktrees and addressed review findings. |
| #50377715 (thibsrn) | covered 16,20,40; disagreement 4 | Single-threaded mental model; preference for API/subscription is not a price benchmark. |
| #50378897 (Uptrenda) | gap | Recovery through independent backups and VM snapshots; isolation alone is insufficient. |
| #50373248 (Quibblingeek) | counter 56; disagreement 12 | Persistent personal agent described as useful; prevents universal digest-only claim. |
| #50375619 (ehostunreach) | covered 23,45 | Status history and proposed checkpointed trace retrieval; vendor affiliation disclosed. |
| #50376410 (FlyingSnake) | covered 5,11 | Hybrid local/cloud routing; numeric model split itself is inconsistent (75+35). |
| #50378086 (moezd) | covered 19,22 | Minimalism and remote availability. |
| #50368119 (patwolf) | covered 26,39; personal-agent camp | Morning information package. |
| #50374646 (dofm) | counter 40 | Automation may help with burnout/blank-page work; no health-effect proof. |
| #50378530 (nfriedly) | covered 29,55 | Remote/browser tool access. |
| #50384963 (egrm) | covered 51; disagreement 5 | Account switching and return to default apps; no authorisation to buy accounts. |
| #50378681 (Teyott) | out of scope | Non-use preference; no actionable harness method. |
| #50377455 (vekker) | covered 11,15,29; counter 56 | Private routing, reusable skills and useful personal assistant. |
| #50375407 (dgunay) | extend 2,33,41 | Chief-of-staff owns intake through reviewed PR; merge authority remains repository-specific. |
| #50377557 (tomburgs) | covered 15,20,56; disagreement 4 | PAYG/workflow UI preferences and cost caveat. |
| #50374449 (Zambyte) | covered 1,27,28 | Small prompts fit local context; ad hoc agent checks. |
| #50373432 (2001zhaozhao) | covered 4,24,33 | Main agent answers child questions and escalates only uncertainty. |
| #50395473 (mirmor23) | counter to sample 1 | Alternative account-risk account; neither side establishes provider policy or rates. |
| #50399014 (cpcdoy) | extend 14,24 | Expected output compared with plan/checks; vendor self-report, not adoption evidence. |
| #50377417 (hosteur) | covered 29,37,49 | Isolated worktree per task on remote VM. |
| #50367866 (x3haloed) | covered 21,22,33 | Add orchestration only after need; request-to-PR intake. |
| #50374746 (jauzeyimam) | covered 5,17,23 | Checked-in brain plus separate cron/watch structure. |
| #50367399 (marshalla) | covered 4,16; caution | Human review relay and timeouts; filler/cache belief is not billing evidence. |
| #50374806 (einhard) | covered 20,49 | Cheap model inside a container. |
| #50375205 (YuechenLi) | covered 5,19,22 | Per-task model preferences and anti-swarm counter-evidence. |
| #50380849 (alentred) | covered 29,49 | Disposable background VM, not laptop-dependent work. |
| #50376062 (TheArcane) | covered 20; disagreement 9 | Latency helps flow; self-reported correctness is not an eval. |

### Cross-check of synthesis sections

All 13 disagreement topics and 24 gold-quote entries were compared with the insight taxonomy. The disagreements are useful context, not independent supporting commenters. Gold quotes broadly repeat 1, 4, 6, 8, 13, 16–19, 22, 32, 35, 45–47 and 49. Two points are underweighted: explicit completion criteria (50367037), above, and **selection bias** (50375972: excited power users volunteer their setups). Therefore commenter counts are citation diversity, not prevalence, quality scores or representative adoption. Product self-promotion must stay attributed, including 50378157 and 50385555. External product links were not validated as part of this review.

## Five reported document defects

1. GOLDMINE routing: row 8 was already updated on merged #2, but reserved-human-gates row 8b was omitted from its embedded table. Copied the complete routing source including 8b.
2. AUDIT counts: the merged baseline already has 8 Done, 11 Existing, 19 Not done, 11 Left out, 1 Built unproven and 6 partial/changed. Independent recount matches; documented category grouping instead of reverting a correct line.
3. Quotes: merged #2 already preserves `GML5.3 [sic]`, removes the extra quoted “no”, and gives ActionHank's actual orchestration/coding/review wording. Checked against full comments 50367557 and 50379104; retained those corrections. “No remote push” remains an unquoted paraphrase of the mechanical gate.
4. Counts: reran term counts on the retained snapshot, added exact regexes/hash/method and updated both Reddit copies. The historical 645-comment query cannot be exactly reconstructed. Also corrected the table-label tally (8 true including the qualified minority, 1 partly true, 1 half wrong) and removed the unsupported assertion about John's cache lifetime.
5. Per-insight citations: added source links to every one of the 56 table rows and to the Markdown generator. Existing numbered details retain the same IDs.

## Coordination and SHA decisions

Connector repository listing succeeds. Root `HANDOVER-TO-CODEX.md` is the wrong path; the actual file is under `hn-agent-setups-2026-11/`. A root-path 404 did not establish lack of connector access.

`c00a51933226af71563d65da5bf5dd6ea7bc3bb1` is Experimentation-Station's prior main (merge #1). Its main is now `ca5801e5bd5c5d1bd3eb822c2427ffb02e9fc7c8` (merge #2), confirmed by fetch and ls-remote. `84075ef1114ba27d927074a8f6255cb1c39fc6c5` exists in the harness history and is an ancestor of harness main `4feda2da70003ff39a538500f5927d1af3df53a0` observed during this check. Thus the two hashes belong to different repository histories; there is no evidence here of contradictory heads for the same repository. The original shell invocation was not retained, so its precise cause cannot be proven.

Issue #352 receipt 6706126391, run 42367518885, records outcome success but delivery unknown, handover_command_observed false and verdict indeterminate. This is not proven delivery and its attempt remains spent. Do not rerun it. #366 already supplies the replacement allow-list implementation; do not create another competing issue/branch for the same change. Independent review of exact #366 head a24895adb7b23ea79503b1bda948652274e5d153 found no blockers; 660 tests passed locally and both GitHub test checks succeeded. Integration and post-merge receiver deployment are separate evidence.

No paid call or subagent was used in this verification. Interactive usage/cost is unknown. This report reviews source fidelity; historical AUDIT implementation-status rows were not re-audited against today's harness code.
