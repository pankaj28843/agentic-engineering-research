# Source Index

This catalog lists all 115 canonical URLs used by the edition. The
date is the source artifact date retained in the evidence ledger; contextual
sources may therefore precede the 1-22 July reporting window. Quality labels
describe evidence role, not truth, and every vendor or practitioner claim is
bounded again in the dated chapter that relies on it.

## How to use this index

- `primary-*` identifies the release, code, data, incident report, trace, or
  first-person account closest to the stated event.
- `independent-*`, `secondary-*`, and `practitioner-*` supply reproduction,
  context, correction, or a viewpoint outside the originating vendor.
- `community-*` is discussion evidence. It qualifies interpretation and
  records practitioner concerns; it never proves the underlying event.
- `inaccessible-primary` preserves an explicit missing-evidence state rather
  than pretending an access-gated artifact was inspected.

## Mix at a glance

- Primary sources and data: 57
- Community discussion: 46
- Independent sources: 3
- Practitioner analysis: 2
- Secondary reporting: 5
- Attributable social evidence: 1
- Inaccessible primary evidence: 1

## 2026-05-19 (context before the reporting window)

- [Does Code Cleanliness Affect Coding Agents?](https://arxiv.org/abs/2605.20049) - `primary-research-paper`. Primary evidence for the 660-trial minimal-pair study and its effort/pass-rate results.
  **Limits:** Confidence C; discovered July 6 Copenhagen time; independent reproduction not found.

## 2026-05-21 (context before the reporting window)

- [The Log is the Agent](https://arxiv.org/abs/2605.21997) - `primary-research-paper`. Primary architecture evidence for event-sourced agent state, replay, forks, and lineage.
  **Limits:** Confidence C; discovered July 5; no independent production evaluation.

## 2026-06-09 (context before the reporting window)

- [Fable 5 on Vending-Bench](https://andonlabs.com/blog/fable5-vending-bench) - `primary-operational-evaluation`. Direct experiment, transcript, and follow-up evidence for observed multi-agent behavior.
  **Limits:** Confidence A for measured behavior; reward-hacking and intent remain evaluator interpretation; discovered July 6.

## 2026-06-27 (context before the reporting window)

- [GPT-5.5 reasoning token clustering at 516](https://github.com/openai/codex/issues/30364) - `primary-practitioner-data`. Aggregate issue data and explicit limits for the reported response-length anomaly.
  **Limits:** Confidence B when combined with independent July 4 reproduction; issue creation 2026-06-27T14:40:18Z.

## 2026-06-30 (context before the reporting window)

- [Godot will no longer accept AI-authored code contributions](https://www.pcgamer.com/gaming-industry/open-source-game-engine-godot-will-no-longer-accept-ai-authored-code-contributions-we-cant-trust-heavy-users-of-ai-to-understand-their-code-enough-to-fix-it/) - `secondary-report`. Radar context for Godot's reported generated-code contribution policy.
  **Limits:** Confidence C; excluded as a July 1 story because discussion did not prove a new consequence.

## 2026-07-01

- [Anthropic export-controls announcement](https://twitter.com/AnthropicAI/status/2072106151890809341) - `inaccessible-primary`. Linked primary for the reported export-control reversal.
  **Limits:** Confidence D; headed CDP rendered only login/consent, so the announcement was not inspectable.
- [Content Independence Day: new AI crawler controls](https://blog.cloudflare.com/content-independence-day-ai-options/) - `primary-vendor-release`. Primary evidence for Cloudflare's crawler-purpose controls, BotBase, content-use signal, and planned defaults.
  **Limits:** Confidence C; product and rollout facts are first-party and not independently validated.
- [HN discussion: Claude export controls reportedly lifted](https://news.ycombinator.com/item?id=48740771) - `community-discussion`. Discovery timestamp, copied Commerce letter, and provider-dependency discussion.
  **Limits:** Discussion evidence only; DI 2; 2026-06-30T23:55:12Z maps to July 1 in Copenhagen.
- [HN discussion: Godot rejects AI-authored contributions](https://news.ycombinator.com/item?id=48743472) - `community-discussion`. Discussion evidence for maintainer trust, review burden, and the July 1 radar context.
  **Limits:** Discussion evidence only; the underlying report was published June 30, so this remains radar context rather than a July 1 event.
- [Kimi K2.7 is now available in GitHub Copilot](https://github.blog/changelog/2026-07-01-kimi-k2-7-is-now-available-in-github-copilot/) - `primary-distributor-release`. Primary distributor evidence for general availability, open-weight positioning, Azure hosting, and pricing position.
  **Limits:** Confidence C; July 1 publication controls the edition.

## 2026-07-02

- [HN discussion: Kimi K2.7 in GitHub Copilot](https://news.ycombinator.com/item?id=48756602) - `community-discussion`. Practitioner discussion of hosted versus local operation, context, determinism, and model lineage.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-02T04:32:41Z.
- [HN discussion: Senior SWE-Bench](https://news.ycombinator.com/item?id=48755928) - `community-discussion`. Methodological critique covering task generation, baselines, contamination, and comparability.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-02T02:55:16Z.
- [HN discussion: Short Leash method](https://news.ycombinator.com/item?id=48766026) - `community-discussion`. Practitioner discussion of context, supervision, and model explanations.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-02T19:11:57Z.
- [Leanstral 1.5](https://mistral.ai/news/leanstral-1-5/) - `primary-vendor-release`. Primary evidence for model architecture, Apache-2 license, evaluations, and reported repository bugs.
  **Limits:** Confidence C; vendor evaluation and bug findings were not independently reproduced.
- [Microsoft Frontier Company](https://blogs.microsoft.com/blog/2026/07/02/microsoft-frontier-company-ai-engineering-that-amplifies-and-protects-your-intelligence/) - `primary-vendor-announcement`. Primary evidence for the new unit, $2.5B investment, and 6,000 embedded experts.
  **Limits:** Confidence C; organizational facts are vendor-primary and outcomes are not independently measured.
- [Senior SWE-Bench](https://senior-swe-bench.snorkel.ai/) - `primary-benchmark`. Primary benchmark description, task design, validation process, and reported failure rate.
  **Limits:** Confidence C; publication instant was not rendered and results were not independently reproduced.
- [The Short Leash: a method for reliable AI-assisted coding](https://blog.okturtles.org/2026/07/short-leash-ai-method/) - `primary-practitioner-report`. Original description of bounded implementation, review permission, and commit cadence.
  **Limits:** Confidence C; comparative superiority claims were not independently supported.

## 2026-07-03

- [Alibaba reportedly restricts Claude Code at work](https://www.reuters.com/world/china/alibaba-ban-claude-code-workplace-over-alleged-backdoor-risks-source-says-2026-07-03/) - `secondary-wire-report`. Attributed report of the alleged restriction and stated security rationale.
  **Limits:** Confidence D for the event claim because Reuters relied on one unauthorized source.
- [HN discussion: Alibaba Claude Code restriction report](https://news.ycombinator.com/item?id=48772443) - `community-discussion`. Discussion of confidentiality, supply-chain trust, compliance, and local alternatives.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-03T08:31:37Z.
- [HN discussion: Leanstral 1.5](https://news.ycombinator.com/item?id=48780801) - `community-discussion`. Practitioner discussion of theorem-proving evaluation and proof-model utility.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-03T22:33:10Z.
- [HN discussion: running state-of-the-art LLMs locally](https://news.ycombinator.com/item?id=48775921) - `community-discussion`. Practitioner discussion of hardware cost, VRAM, quantization, throughput, and harness effects.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-03T15:03:43Z.
- [jamesob/local-llm](https://github.com/jamesob/local-llm) - `primary-open-source-code`. Direct operational repository evidence for local inference configurations and measured bandwidth.
  **Limits:** Confidence A for the executable artifact; creation timestamp 2026-07-03T13:06:03Z; README is a later mutable snapshot.

## 2026-07-04

- [Better Models: Worse Tools](https://lucumr.pocoo.org/2026/7/4/better-models-worse-tools/) - `primary-practitioner-reproduction`. Bounded direct operational evidence for a nested tool-schema regression.
  **Limits:** Confidence A for the documented harness/schema failure; broader prevalence is unknown.
- [HN discussion: apparent Claude response leakage](https://news.ycombinator.com/item?id=48785485) - `community-discussion`. Competing technical explanations involving provider infrastructure, hallucination, and local context.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-04T14:03:40Z.
- [HN discussion: Better Models: Worse Tools](https://news.ycombinator.com/item?id=48788599) - `community-discussion`. Practitioner discussion of strict validation, schema design, and harness mitigation.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-04T20:16:22Z.
- [HN discussion: GPT-5.5 Codex 516-token anomaly](https://news.ycombinator.com/item?id=48789428) - `independent-practitioner-reproduction`. Independent 10-run reproduction, answer-quality observation, hypothesis, and workaround.
  **Limits:** Distinct corroborating fact; combined GitHub and HN evidence gives DI 3; timestamp 2026-07-04T21:51:09Z.
- [Possible Claude session/cache leakage report](https://github.com/anthropics/claude-code/issues/74066) - `primary-user-issue`. Original Enterprise/ZDR user report and cross-device follow-up.
  **Limits:** Confidence C; unresolved and unconfirmed; issue creation 2026-07-04T02:04:31Z.

## 2026-07-05

- [HN discussion: The Log is the Agent](https://news.ycombinator.com/item?id=48790912) - `community-discussion`. Architecture discussion comparing event sourcing/CQRS and replay/tool-state tradeoffs.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-05T02:57:38Z.

## 2026-07-06

- [A global workspace in language models](https://www.anthropic.com/research/global-workspace) - `primary-vendor-research`. Primary evidence for J-space, J-lens, interventions, ablations, and reported open-weight replication.
  **Limits:** Confidence C; source date was not rendered and independent replication was not separately captured.
- [HN discussion: code cleanliness and coding agents](https://news.ycombinator.com/item?id=48798815) - `community-discussion`. Methods and engineering-practice discussion of the cleanliness result.
  **Limits:** Discussion evidence only; DI 2; 2026-07-05T23:03:55Z maps to July 6 in Copenhagen.
- [HN discussion: Fable 5 on Vending-Bench](https://news.ycombinator.com/item?id=48803762) - `community-discussion`. Practitioner discussion of model utility, quotas, evaluation, and alignment interpretation.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-06T12:38:13Z.
- [HN discussion: GLM-5.2 and AI margins](https://news.ycombinator.com/item?id=48809877) - `community-discussion`. Discussion of raw model cost, enterprise service moats, and commoditization.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-06T20:14:55Z.
- [HN discussion: global workspace in language models](https://news.ycombinator.com/item?id=48808002) - `community-discussion`. Discussion of mechanistic interpretation and what shared representations establish.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-06T17:44:08Z.
- [The upcoming AI margin collapse, part 1: GLM-5.2](https://martinalderson.com/posts/the-upcoming-ai-margin-collapse-part-1-glm-5-2/) - `primary-practitioner-analysis`. Disclosed practitioner evidence for pricing, workflow experience, limitations, and the margin thesis.
  **Limits:** Confidence C; price and disclosed experience are inspectable, industry-wide margin collapse is not established.

## 2026-07-07

- [AI Meets Cryptography: seven CIRCL bugs](https://blog.zksecurity.xyz/posts/circl-bugs/) - `primary-operational-security-report`. Direct evidence for seven human-validated findings, PoCs, upstream fixes, and bounties.
  **Limits:** Confidence A; authoritative fixes are linked from the report; severity framing remains bounded.
- [HN discussion: AI-assisted CIRCL audit](https://news.ycombinator.com/item?id=48821749) - `community-discussion`. Technical discussion of false positives, human validation, tests, and cryptographic numeric hazards.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-07T18:36:35Z.
- [HN discussion: Riddle on reMarkable](https://news.ycombinator.com/item?id=48811591) - `community-discussion`. Discussion of constrained-device engineering, interface design, and safety boundaries.
  **Limits:** Discussion evidence only; DI 2; 2026-07-06T23:00:24Z maps to July 7 in Copenhagen.
- [MaximeRivest/Riddle](https://github.com/MaximeRivest/Riddle) - `primary-open-source-code`. Inspectable current repository for the reMarkable pen-stroke-to-agent interface.
  **Limits:** Confidence C; date comes from Copenhagen-local HN discovery and repository state is mutable.

## 2026-07-08

- [Benchmarking Coding Agents on Databricks' Multi-Million-Line Codebase](https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase) - `primary-practitioner-benchmark`. Direct operational evidence for private-code benchmark design, model/harness tiers, and per-task costs.
  **Limits:** Confidence A for the measured internal benchmark; results should not be generalized beyond Databricks' reviewed tasks.
- [HN discussion: Databricks coding-agent benchmark](https://news.ycombinator.com/item?id=48837696) - `community-technical-discussion`. Practitioner interpretation of fixed-budget evaluation, harness effects, and cost per successful task.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-08T21:30:09Z.
- [HN discussion: GPT-Live](https://news.ycombinator.com/item?id=48834405) - `community-discussion-with-practitioner-report`. Attributable preview experience plus interpretation of voice interruption and background delegation.
  **Limits:** DI 1; exact thread timestamp 2026-07-08T17:03:19Z; counts had no evidentiary role.
- [HN discussion: Separating signal from noise in coding evaluations](https://news.ycombinator.com/item?id=48837396) - `community-technical-discussion`. Technical discussion of verifier design, hidden requirements, resource limits, and human review.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-08T21:03:51Z.
- [Introducing GPT-Live](https://openai.com/index/introducing-gpt-live/) - `primary-vendor-release`. Primary evidence for full-duplex voice behavior, background GPT-5.5 delegation, rollout, and API-soon state.
  **Limits:** Confidence B when combined with an attributable preview-user report; API availability remained prospective.
- [Separating Signal from Noise in Coding Evaluations](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) - `primary-authoritative-correction`. Primary audit evidence for broken SWE-Bench Pro public tasks, contamination, human review, and OpenAI's retracted recommendation.
  **Limits:** Confidence A; complete headed-CDP extraction. Roughly 30% is OpenAI's estimate from agent and five-reviewer human audits.

## 2026-07-09

- [GPT-5.6](https://openai.com/index/gpt-5-6/) - `primary-vendor-release`. Primary evidence for model tiers, ultra multi-agent coordination, availability, and prices.
  **Limits:** Confidence B for the merged item because Ploy supplied distinct production evidence; vendor benchmark claims remain attributed.
- [HN discussion: GPT-5.6](https://news.ycombinator.com/item?id=48849066) - `community-technical-discussion`. Prompt-migration and brevity interpretation only.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-09T17:04:14Z.
- [HN discussion: Muse Spark 1.1](https://news.ycombinator.com/item?id=48846184) - `community-inspectable-correction`. Distinct technical correction showing Meta's blanket Terminal-Bench resources differed from official task-specific limits.
  **Limits:** DI 2; exact thread timestamp 2026-07-09T14:10:22Z; correction narrows rather than validates vendor performance claims.
- [Introducing Muse Spark and the Meta Model API](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/) - `primary-vendor-release`. Primary evidence for public preview, long context, multi-agent orchestration, MCP, skills, and computer use.
  **Limits:** Complete article Markdown despite zero visible-text items; performance framing is constrained by a technical resource-limit correction.
- [Migrating a Production AI Agent to GPT-5.6](https://ploy.ai/blog/migrating-a-production-ai-agent-to-gpt-5-6) - `independent-production-measurement`. Production evidence for runtime, cost, token, visual-quality, tool-schema, and prompt-cache behavior.
  **Limits:** Distinct evidence satisfying the vendor-only lead safeguard; measurements remain workload-specific.
- [The Zero-Cost Fallacy: Open Source in the Agentic Era](https://www.thoughtworks.com/insights/blog/open-source/zero-cost-fallacy-open-source-agentic-era) - `practitioner-analysis`. Radar evidence for the argument that agent-generated contribution volume increases maintainer load and dependency ownership.
  **Limits:** Confidence C; opinion-led analysis without an empirical dataset.

## 2026-07-11

- [Old and New Apps, via Modern Coding Agents](https://terrytao.wordpress.com/2026/07/11/old-and-new-apps-via-modern-coding-agents/) - `primary-practitioner-report`. Direct operational evidence for porting mathematical applets and building a bounded visualization.
  **Limits:** Confidence A for the described expert-supervised work and linked artifacts; not evidence of autonomous mathematical correctness.

## 2026-07-12

- [Claude Code vs OpenCode: Token Overhead](https://systima.ai/blog/claude-code-vs-opencode-token-overhead) - `primary-practitioner-measurement`. Direct API-boundary evidence for fixed context, instruction, MCP, and subagent token overhead.
  **Limits:** Confidence A for the pinned versions and tested configurations; not permanent vendor behavior.
- [HN discussion: coding-agent token overhead](https://news.ycombinator.com/item?id=48883275) - `community-technical-discussion`. Practitioner reports on subagent budget burn and exploration-versus-cost tradeoffs.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-12T18:25:51Z.
- [HN discussion: Grok Build wire analysis](https://news.ycombinator.com/item?id=48877371) - `community-technical-discussion`. Concrete sandbox, root-filesystem, and selective-network mitigation patterns.
  **Limits:** Discussion evidence only; DI 2; July 14 incident update controls publication placement.
- [HN discussion: Old and new apps via coding agents](https://news.ycombinator.com/item?id=48880170) - `community-technical-discussion`. Discussion of visual, bounded, expert-reviewed agent work and its correctness limits.
  **Limits:** Discussion evidence only; DI 2; HN pickup does not move the July 11 source date.
- [Juggler Open-Source GUI Coding Agent](https://github.com/juggler-ai/juggler) - `primary-open-source-code`. Radar evidence for the visual workbench, branching session model, tool inspection, and plugin architecture.
  **Limits:** Confidence C; July 12 HN creator launch is the precise in-window publication marker for an older repository.
- [Zig Creator Calls Spade a Spade, Anthropic Blows Smoke](https://raymyers.org/post/zed-creator-calls-spade-a-spade/) - `secondary-practitioner-critique`. Radar evidence for battle-testing, alternative-remediation, attribution, and marketing-accountability concerns.
  **Limits:** Confidence C; present as a documented critique rather than a settled factual verdict.

## 2026-07-13

- [Apple SpeechAnalyzer API Benchmarked Against Whisper](https://get-inscribe.com/blog/apple-speech-api-benchmark.html) - `primary-practitioner-benchmark`. Direct benchmark evidence for English LibriSpeech word-error rates, M2 Pro speed, and released transcripts.
  **Limits:** Confidence A for the bounded test; newer comparators and multilingual workloads were omitted.
- [Attributable report of Grok CLI whole-home upload](https://twitter.com/a_green_being/status/2076598897779020159) - `attributable-social-claim`. Qualified escalation signal merged into the directly evidenced Grok upload incident.
  **Limits:** Confidence D alone; readable post timestamp derived from the tweet snowflake as 2026-07-13T09:25:33.229Z.
- [HN discussion: Apple SpeechAnalyzer benchmark](https://news.ycombinator.com/item?id=48894752) - `community-technical-discussion`. Specific correction context on missing newer comparators and multilingual limitations.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-13T16:06:08Z.

## 2026-07-14

- [Announcing Bonsai 27B](https://prismml.com/news/bonsai-27b) - `primary-vendor-release`. Radar evidence for low-bit weights, footprint, context, license, benchmarks, and deployment claims.
  **Limits:** Confidence C; phone demo used cached and prefilled image context and performance remains vendor-measured.
- [Cursor 0day: When Full Disclosure Becomes the Only Protection Left](https://mindgard.ai/blog/cursor-0day-when-full-disclosure-becomes-the-only-protection-left) - `primary-security-disclosure`. Direct reproduction, Process Monitor trace, disclosure timeline, affected-version state, and temporary mitigations.
  **Limits:** Confidence A; page metadata/display dates conflict, but the timeline and modified timestamp identify July 14 public disclosure.
- [HN discussion: Cursor workspace git.exe 0day](https://news.ycombinator.com/item?id=48910676) - `community-technical-discussion`. Discussion of disclosure chronology, bug-bounty triage pressure, and automated triage feasibility.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-14T17:58:35Z.
- [What xAI's Grok Build CLI Sends to xAI: A Wire-Level Analysis](https://gist.github.com/cereblab/dc9a40bc26120f4540e4e09b75ffb547) - `primary-security-trace`. Direct evidence for file and repository uploads plus the July 14 incident-state update.
  **Limits:** Confidence A for observed transfers. Server-side disablement and deletion commitment are attributed to the researcher's update.

## 2026-07-15

- [GPT-5.6 used a prompt to close a 30-year gap in convex optimization](https://old.reddit.com/r/math/comments/1uxj3cy/after_openais_cdc_proof_announcement_gpt56_used_a/) - `primary-practitioner-claim`. Original author disclosure linking the preprint and Lean artifact for the claimed convex-optimization result.
  **Limits:** Confidence C: not peer reviewed and no independent theorem audit was captured; Reddit says submitted July 15.
- [HN discussion: Grok Build is open source](https://news.ycombinator.com/item?id=48926590) - `community-discussion`. Code-level practitioner inspection of Grok Build implementation details and Unicode/CJK behavior.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-15T20:24:58Z and earliest exact public evidence for the edition assignment.
- [HN discussion: Thinking Machines releases Inkling](https://news.ycombinator.com/item?id=48924912) - `community-discussion`. Practitioner discussion of deployment paths, inference, procurement, and comparisons with other open-weight models.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-15T18:12:45Z.
- [Introducing Inkling, Our First Model](https://thinkingmachines.ai/news/introducing-inkling/) - `primary-vendor-release`. Primary evidence for Inkling's release, architecture, training scale, availability, and stated limitations.
  **Limits:** Confidence B for release facts and C for performance framing; headed CDP extraction in selected-pages/001-thinkingmachines-ai-news-introducing-inkling/.
- [Unlocking Self-Improvement for Robustness with GPT-Red](https://openai.com/index/unlocking-self-improvement-gpt-red/) - `primary-vendor-report`. Primary account of OpenAI's automated self-play red-teaming system and reported robustness measurements.
  **Limits:** Confidence C because the efficacy numbers are vendor-generated and not independently reproduced in this lane.
- [xai-org/grok-build](https://github.com/xai-org/grok-build) - `primary-open-source-code`. Inspectable repository evidence for xAI's terminal coding agent and its supported workflows.
  **Limits:** Confidence A for repository existence/features and B for publication date/maturity; GitHub UI labels the publication commit July 16.

## 2026-07-16

- [HN discussion: Kimi K3](https://news.ycombinator.com/item?id=48935342) - `community-discussion`. Practitioner discussion including one measured API run, pricing, benchmark skepticism, and agent-reviewer patterns.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-16T14:46:05Z.
- [HN discussion: LM Studio Bionic](https://news.ycombinator.com/item?id=48939662) - `community-discussion`. Practitioner and founder discussion of access, BYOK, provider visibility, retention, and local reasoning traces.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-16T20:18:15Z.
- [Introducing LM Studio Bionic](https://lmstudio.ai/blog/introducing-lm-studio-bionic) - `primary-vendor-release`. Primary product evidence for LM Studio's local and open-model agent.
  **Limits:** Confidence C; product and privacy/provider claims were not independently validated.
- [Kimi K3: Open Frontier Intelligence](https://www.kimi.com/blog/kimi-k3) - `primary-vendor-release`. Primary announcement for Kimi K3 architecture, scale, context length, and vendor-reported agent capabilities.
  **Limits:** Confidence C; full weights were scheduled for July 27, so July 16 is an announcement rather than a weight release.
- [Security incident disclosure - July 2026](https://huggingface.co/blog/security-incident-july-2026) - `primary-incident-report`. Detailed operational evidence for an autonomous-agent intrusion, containment, scope, and agent-assisted response.
  **Limits:** Confidence A for disclosed operational facts; assessment was still ongoing at publication.

## 2026-07-17

- [A Scorecard for the AI Age](https://openai.com/index/a-scorecard-for-the-ai-age/) - `primary-vendor-policy`. Primary evidence for OpenAI's proposed useful-intelligence-per-dollar policy metric.
  **Limits:** Confidence C; this is an advocacy position, not a government policy or independently validated causal model.
- [Claude Code: Anatomy of a Misfeature](https://www.olafalders.com/2026/07/17/claude-code-anatomy-of-a-misfeature/) - `primary-practitioner-report`. Versioned reproduction of Claude Code's question timeout and its human-in-the-loop consequences.
  **Limits:** Confidence A due to detailed operational reproduction and documented subsequent fix.
- [HN discussion: The State of Open Source AI](https://news.ycombinator.com/item?id=48947825) - `community-discussion`. Practitioner discussion of harness quality, open-weight economics, and open-source terminology.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-17T14:31:10Z.
- [The State of Open Source AI](https://stateofopensource.ai/) - `primary-sponsored-report`. Primary survey and market-report evidence for open-model adoption, capability gaps, and production deployment.
  **Limits:** Confidence C because top-line claims depend on sponsor methodology and vendor-defined categories; exact source day was not exposed, so the HN timestamp anchors this edition.

## 2026-07-18

- [Codex PR 33972: update supported models](https://github.com/openai/codex/pull/33972/files) - `primary-open-source-change`. Primary evidence for the merged Codex model-metadata update and changed metadata file.
  **Limits:** Confidence B for merge/file change and C for the exact 372k-to-272k usable-context claim because the rendered diff was lazy-loaded.
- [HalluSquatting Makes AI Coding Agents a Supply-Chain Threat](https://www.developersdigest.tech/blog/hallusquatting-ai-coding-agent-security) - `secondary-technical-report`. Detailed explanation of hallucinated dependency/resource identifiers, resolver risk, and proposed controls.
  **Limits:** Confidence B; links the primary paper/project, but the paper was not separately extracted in this lane.
- [HN discussion: GPT-5.6-assisted convex-optimization proof claim](https://news.ycombinator.com/item?id=48957779) - `community-discussion`. Second-community technical discussion of the claim, formalization, theorem framing, and research implications.
  **Limits:** Discussion evidence only; combined Reddit and HN discussion produces DI 3; HN timestamp 2026-07-18T13:00:52Z.

## 2026-07-19

- [Claude Code uses Bun written in Rust now](https://simonwillison.net/2026/Jul/19/claude-code-in-bun-in-rust/) - `primary-practitioner-reproduction`. Reproducible installed-binary inspection supporting Claude Code's transition to the Rust port of Bun.
  **Limits:** Confidence A; the source reports embedded Bun 1.4.0 and 563 Rust source paths.
- [Hidden prompts can plant false memories in AI agents](https://techxplore.com/news/2026-07-hidden-prompts-false-memories-ai.html) - `secondary-research-report`. Attributable coverage of the GhostWriter persistent-memory poisoning research and AM-Sentry mitigations.
  **Limits:** Confidence C; this is the only extracted report, and the linked arXiv:2607.06595 paper was not separately extracted.
- [HN discussion: Claude Code uses Bun written in Rust](https://news.ycombinator.com/item?id=48966569) - `community-discussion`. Technical discussion of Rust memory lifecycle, compiler guardrails, allocation, RSS, Zig, and robustness.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-19T10:03:23Z.
- [HN discussion: Codex context reduced from 372k to 272k](https://news.ycombinator.com/item?id=48965850) - `community-discussion`. Source for the exact numeric context claim and practitioner discussion of compaction, workarounds, and long-context tradeoffs.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-19T07:54:39Z. Story edition remains July 18 based on the primary merge.

## 2026-07-20

- [Agent Swarms and the New Model Economics](https://cursor.com/blog/agent-swarm-model-economics) - `primary-vendor-experiment`. Primary report of Cursor's swarm-coordination experiment, held-out grading, and model-mix costs.
  **Limits:** Confidence C overall because Cursor designed both the harness and evaluation and no independent reproduction was captured.
- [American AI is locked down and proprietary. It's losing.](https://werd.io/american-ai-is-locked-down-and-proprietary-its-losing/) - `practitioner-analysis`. Attributed synthesis of Chinese open-weight distribution strategy, export constraints, and ecosystem incentives.
  **Limits:** Confidence C; strategic conclusions are opinion and cited factual claims were not independently re-extracted in this lane.
- [Claude Is Not a Compiler](https://blog.exe.dev/claude-is-not-a-compiler) - `primary-practitioner-case-study`. First-person operational case using competing agent implementations to discover and refine a distributed-DNS specification.
  **Limits:** Confidence A for the reported workflow and outcome, C for broader generalization; story reassigned from July 21 using the source date.
- [HN discussion: AI-assisted WordPress RCE](https://news.ycombinator.com/item?id=48975665) - `community-discussion-correction`. Security-practitioner correction of the exploit-price comparison and discussion of target-specific pricing.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-20T08:13:36Z.
- [HN discussion: Chinese open-weights strategy](https://news.ycombinator.com/item?id=48979269) - `community-discussion`. Practitioner debate about sustainability, hardware incentives, state funding, inference economics, censorship, and terminology.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-20T14:21:47Z.
- [HN discussion: Cursor agent swarms and model economics](https://news.ycombinator.com/item?id=48982535) - `community-discussion`. Practitioner critique of commit-rate framing, custom VCS, human evaluation, memory, context, and supervision.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-20T18:06:13Z.
- [I found a WordPress RCE with GPT-5.6 and $25](https://slcyber.io/research-center/exploit-brokers-pay-500000-for-a-wordpress-rce-i-found-one-with-gpt5-6/) - `primary-practitioner-report`. Detailed first-person account of an AI-assisted WordPress vulnerability chain and research time/cost.
  **Limits:** Confidence B for the technical narrative and C for the unsupported $500,000 exploit-price comparator.

## 2026-07-21

- [Cisco Launches Low-Cost AI Models for Source Code Security](https://www.securityweek.com/cisco-launches-low-cost-ai-models-for-source-code-security/) - `independent-trade-report`. Attributable reporting of Cisco's Antares model release, vulnerability-localization benchmark, and vendor cost claims.
  **Limits:** Confidence C because the report carries Cisco claims and the model cards/benchmark were not separately extracted. Published 2026-07-21T17:44:00Z.
- [Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/) - `primary-vendor-release`. Primary release evidence for Google's Flash model lineup, pricing, throughput claims, and restricted cyber-model pilot.
  **Limits:** Confidence C overall; availability/pricing are directly stated, while benchmark and efficiency claims were not independently reproduced.
- [HN discussion: Claude Is Not a Compiler](https://news.ycombinator.com/item?id=48993059) - `community-discussion`. Practitioner stress test of the compiler analogy, co-evolving specifications, verification, and human validation burden.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-21T14:49:18Z. Story edition remains July 20.
- [HN discussion: Gemini Flash model family](https://news.ycombinator.com/item?id=48993414) - `community-discussion`. Early practitioner reports on extraction quality, speed, model position, and production pricing.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-21T15:17:16Z.
- [HN discussion: OpenAI and Hugging Face model-evaluation incident](https://news.ycombinator.com/item?id=48997548) - `community-technical-discussion`. Practitioner discussion of evaluation isolation, egress, reward hacking, marketing incentives, and comparable agent escape behavior.
  **Limits:** Discussion evidence only; DI 3; inspected during the completed-day refresh after 365 points and 221 comments were visible.
- [HN discussion: Qwen Image 3.0](https://news.ycombinator.com/item?id=48989701) - `community-discussion`. Early discussion of virtual try-on accuracy, seller manipulation, and buyer-side counter-models.
  **Limits:** Discussion evidence only; DI 2; exact thread timestamp 2026-07-21T08:44:23Z.
- [OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident/) - `primary-incident-report`. Primary evidence identifying the evaluated models, sandbox escape, package-cache zero-day, Hugging Face breach path, and remediation.
  **Limits:** Confidence C; OpenAI and Hugging Face are direct incident participants, but the investigation is preliminary and the vulnerabilities and model behavior were not independently reproduced.

- [Qwen-Image-3.0](https://qwen.ai/blog?id=qwen-image-3.0) - `primary-vendor-demonstration`. Primary launch demonstration for long instructions, dense layouts, small text, languages, styles, and connected retrieval.
  **Limits:** Confidence C; rendered page did not establish weights, license, pricing, or independent benchmarks.

## 2026-07-22

- [APIFlow-Bench](https://blog.postman.com/apiflow-bench/) - `primary-vendor-benchmark`. Primary evidence for the task bank, long-chain results, and failure analysis.
  **Limits:** Confidence B for the measurements and C for generalization; the tasks are generated, REST-only, span 13 worlds, and the full-chain result covers eleven 20-step chains. Claude Opus 4.8 served as the solvability oracle.
- [APIFlow-Bench transcripts](https://github.com/postmanlabs/apiflow-bench-transcripts) - `primary-benchmark-data`. Inspectable trial transcripts behind the reported results.
  **Limits:** The repository exposes 44,362 transcripts; 3 intended grid cells were not scored.
- [Introducing OpenAI Presence](https://openai.com/index/introducing-openai-presence/) - `primary-vendor-release`. Product evidence for limited availability, policies, evaluation, escalation, and claimed support outcomes.
  **Limits:** Confidence C; OpenAI's operational results were not independently verified.
- [HN discussion: OpenAI Presence](https://news.ycombinator.com/item?id=49008089) - `community-discussion`. Practitioner concerns about domain depth, consulting-led deployment, ownership, and lock-in.
  **Limits:** Discussion evidence only; DI 2; exact timestamp 2026-07-22T15:12:26Z.
- [Microsoft Agent Framework Harness release](https://devblogs.microsoft.com/agent-framework/the-microsoft-agent-framework-harness-is-now-released/) - `primary-framework-release`. Release evidence for the stable Python and .NET harness and its default runtime features.
  **Limits:** Confidence B for the interface; production-readiness language is Microsoft's characterization.
- [Microsoft harness documentation](https://learn.microsoft.com/agent-framework/agents/harness) - `primary-technical-documentation`. Detailed contract for persistence, compaction, planning, approvals, skills, background agents, and shell access.
  **Limits:** Mutable documentation; compaction is configurable, file-backed memory can be disabled, skills are optional, and background/file/loop/shell tools are opt-in or unreleased. The shell deny-list is not a security boundary.
- [CrucibleBench](https://cruciblebench.ai/) - `primary-practitioner-benchmark`. Proof-of-concept report for the persistent-world evaluation and judge-ablation result.
  **Limits:** Confidence B for measurements; rankings are exploratory and lack a human-rater baseline.
- [Can a MUD Evaluate LLMs?](https://doi.org/10.5281/zenodo.21386663) - `primary-benchmark-data`. Paper, transcripts, code, scoring logic, analysis, and billing record.
  **Limits:** The record's July 22 creation and HN launch anchor this edition despite an earlier publication field.
- [HN discussion: CrucibleBench](https://news.ycombinator.com/item?id=49008538) - `community-technical-discussion`. Discussion of evaluation cost, prompt sensitivity, token budgets, and artifact transparency.
  **Limits:** Discussion evidence only; the author supplied framing while commenters questioned cost, judge choice, token budgets, and prompt sensitivity. DI 2; exact timestamp 2026-07-22T15:39:01Z.
- [AMD and Anthropic strategic partnership](https://ir.amd.com/news-events/press-releases/detail/1292/amd-and-anthropic-announce-strategic-partnership-to-deploy-up-to-2-gigawatts-of-amd-instinct-mi450-series-gpus) - `primary-vendor-announcement`. Terms for planned capacity, engineering collaboration, and future equity investment.
  **Limits:** Confidence C; capacity and the up-to-$5-billion investment are commitments, not completed deployments.
- [Terence Tao's ChatGPT conversation](https://chatgpt.com/share/6a5fdc7a-d6f8-83e8-bbea-8deb42cfed56) - `primary-conversation-artifact`. Inspectable expert-directed representation changes, decomposition, calculations, and verification.
  **Limits:** Confidence C for interpretation; this is a human-guided workflow, not evidence of autonomous proof discovery.
- [HN discussion: Terence Tao's ChatGPT conversation](https://news.ycombinator.com/item?id=49010345) - `community-technical-discussion`. Practitioner interpretation of expert steering, verification, mathematical tooling, and autonomous-discovery claims.
  **Limits:** Discussion evidence only; DI 2; inspected after 260 points and 125 comments were visible.
- [GigaToken](https://github.com/marcelroed/gigatoken) - `primary-open-source-code`. Implementation, benchmarks, optimization notes, compatibility modes, and known limitations for CPU tokenization.
  **Limits:** Confidence C for broad speed claims because the benchmarks are project-authored; the repository validates outputs for the stated data and hardware.
- [HN discussion: GigaToken](https://news.ycombinator.com/item?id=49010167) - `community-technical-discussion`. Practitioner discussion of SIMD and cache techniques, inference-time limits, and training, routing, and rate-limiting uses.
  **Limits:** Discussion evidence only; DI 2; inspected after 151 points and 27 comments were visible.
