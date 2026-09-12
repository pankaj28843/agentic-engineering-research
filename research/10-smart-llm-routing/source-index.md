# Source index: Smart LLM Routing

This index names the evidence retained for the theme. The URL in each row is
the canonical or source-native URL selected for the page. sources.json is the
machine-readable version, including stable IDs, chapter mapping, capture mode,
and the 2026-09-12 audit date.

The corpus contains 75 retained records: official and regulatory pages,
research papers, practitioner and vendor accounts, independent benchmarks, and
community signals. Source class describes how much weight a claim should
receive. A primary page can establish what its publisher documents; it cannot
establish that a route will work in this enterprise. A vendor measurement can
show a mechanism or local result; it cannot silently become a forecast. A
community page is an anecdote or failure hypothesis.

## Evidence accounting

- 81 URLs were selected after four reviewed Google passes. Each pass used
  headed Google, one result page, and bounded parallel extraction.
- The initial headed capture produced 78 page records: 71 passed the quality
  gate, seven failed it, and three collector errors were recorded.
- One timing-only retry of the seven quality failures recovered four pages.
  The final usable page corpus is 75 captures. No second retry was run.
- scripts/extract_theme_articles.py produced 70 clean article snapshots.
  Five selected pages remain unavailable for clean synthesis because their
  capture redirected to a generic or mismatched surface or showed a security
  or site-shell response. Their limitations are recorded in the research log.
- The native Hacker News collection is retained in
  tmp/agents/smart-routing/practitioner-social.md; its links are evidence
  leads and anecdotes, not prevalence estimates.

## Retained records
| ID | Source and canonical URL | Evidence class | Use | Chapters | Capture |
|---|---|---|---|---|---|
| S01 | [LLM model routing](https://neuraltrust.ai/blog/llm-model-routing) | vendor-practitioner | Routing taxonomy, cost-quality framing, and vendor-side implementation patterns. | 01, 02, 11 | initial-pass |
| S02 | [Routing and model selection research paper](https://arxiv.org/html/2601.07206v1) | primary-research | Recent research evidence for routing or model-selection behavior; interpret empirical claims with the paper's stated scope. | 02, 03, 09 | initial-pass |
| S03 | [LLM routing research paper](https://arxiv.org/html/2603.04445v3) | primary-research | Recent routing method and evaluation evidence. | 02, 08, 09 | initial-pass |
| S04 | [LLM routing research paper](https://arxiv.org/html/2608.14641v1) | primary-research | Recent routing method and evaluation evidence, retained with version-pinned URL. | 02, 08, 09 | initial-pass |
| S05 | [AI FinOps for the agentic era](https://further.ai/blog/ai-finopps-for-the-agentic-era) | vendor-practitioner | FinOps framing for agentic workloads, spend attribution, and optimization. | 04, 11 | initial-pass |
| S06 | [The AI token-maxxing PM interview](https://conceptsandbeyond.com/the-ai-token-maxxing-pm-interview/) | independent-practitioner | Practitioner discussion of token budgets and product incentives; treated as qualitative evidence. | 03, 04 | initial-pass |
| S07 | [OpenReview routing paper record](https://openreview.net/forum?id=ypRg1TvQaM) | primary-research | Peer-review record and paper identity for a routing result. | 02, 08 | initial-pass |
| S08 | [How to run open-source AI models](https://sidsaladi.substack.com/p/how-to-run-open-source-ai-models) | independent-practitioner | Practical local and open-weight serving considerations. | 05, 06 | initial-pass |
| S09 | [AI model routing for cost and quality](https://intuitionlabs.ai/articles/ai-model-routing-cost-quality) | vendor-practitioner | Cost-quality routing patterns and caveats from an implementation-oriented vendor source. | 01, 03, 11 | initial-pass |
| S10 | [AI Forum model-routing discussion](https://www.facebook.com/groups/theaiforum/posts/1351469050489803/) | community-signal | Community signal retained as bounded qualitative context; not used for model, price, or availability claims. | 01, 12 | initial-pass |
| S11 | [Smart LLM routing and AI-bill reduction](https://www.kosmoy.com/resources/blog/smart-llm-routing-how-to-cut-your-ai-bill-by-40/) | vendor-practitioner | Vendor cost-reduction claim used as a hypothesis and checked against primary economics. | 03, 04, 11 | initial-pass |
| S12 | [AI agent evaluation](https://mastra.ai/articles/ai-agent-evaluation) | vendor-practitioner | Agent evaluation taxonomy and operational testing patterns. | 08, 09 | initial-pass |
| S13 | [AI agent model routing](https://zylos.ai/research/2026-03-02-ai-agent-model-routing/) | independent-practitioner | Comparative routing discussion and implementation considerations. | 01, 02, 11 | initial-pass |
| S14 | [LLM model routing: cost, quality, and optimization](https://www.digitalapplied.com/blog/llm-model-routing-2026-cost-quality-optimization-engineering-guide) | independent-practitioner | Engineering guide used for patterns and counter-checks, not as primary product evidence. | 01, 03, 11 | initial-pass |
| S15 | [Cursor router](https://cursor.com/blog/router) | vendor-practitioner | Coding-agent vendor account of router behavior and model-selection tradeoffs. | 01, 02, 08 | initial-pass |
| S16 | [Dynamic LLM routing tools and frameworks](https://latitude.so/blog/dynamic-llm-routing-tools-and-frameworks) | vendor-practitioner | Framework and gateway comparison material. | 01, 06, 11 | initial-pass |
| S17 | [Enterprise LLM model scaling](https://medium.com/@kmesiab/enterprise-llm-model-scaling-ac2a8dd940c4) | independent-practitioner | Enterprise scaling patterns and operational observations. | 05, 06, 11 | initial-pass |
| S18 | [Model-routing strategies for cost-effective coding](https://www.developersdigest.tech/blog/model-routing-strategies-cost-effective-coding-2026) | independent-practitioner | Coding-agent routing strategies and practical cost-quality framing. | 01, 04, 09 | initial-pass |
| S19 | [Dynamic model routing with open models](https://www.snowflake.com/en/blog/dynamic-model-routing-open-models-cortex-ai/) | vendor-practitioner | Enterprise platform account of dynamic model routing and open-model integration. | 01, 05, 06 | initial-pass |
| S20 | [Intelligent model selection for LLM routing](https://zylos.ai/research/2026-01-29-llm-routing-intelligent-model-selection/) | independent-practitioner | Routing selection criteria and operational tradeoffs. | 01, 02, 09 | initial-pass |
| S21 | [LLM routing](https://blog.n8n.io/llm-routing/) | vendor-practitioner | Workflow-agent routing examples and product integration context. | 01, 06 | initial-pass |
| S22 | [RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/html/2406.18665) | primary-research | Named routing baseline using preference data; source for thresholding and cost-quality evaluation. | 02, 08, 09 | initial-pass |
| S23 | [FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](https://arxiv.org/html/2305.05176) | primary-research | Cascade and budget-aware baseline for cost-quality routing. | 01, 02, 03, 09 | initial-pass |
| S24 | [LLM routing benchmark research](https://arxiv.org/html/2410.10347v3) | primary-research | Benchmark evidence for comparing routing strategies. | 08, 09 | initial-pass |
| S25 | [LLM routing and model-selection research](https://arxiv.org/html/2503.10657) | primary-research | Recent research evidence on adaptive model selection. | 02, 08, 09 | initial-pass |
| S26 | [Large language model routing with benchmark datasets](https://research.ibm.com/publications/large-language-model-routing-with-benchmark-datasets) | primary-research | Benchmark dataset and evaluation framing for routing. | 08, 09 | initial-pass |
| S27 | [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) | official-primary | Primary hosted-model pricing reference; prices are treated as time-sensitive and audited on the capture date. | 03, 04, 11 | initial-pass |
| S28 | [Amazon Bedrock intelligent prompt routing](https://docs.aws.amazon.com/bedrock/latest/userguide/intelligent-prompt-routing.html) | official-primary | Primary documentation for a managed intelligent-routing capability and its scope. | 01, 06, 11 | initial-pass |
| S29 | [Amazon Bedrock model customization pricing](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-pricing.html) | official-primary | Primary documentation for customization cost categories. | 03, 04 | initial-pass |
| S30 | [Amazon Bedrock intelligent prompt routing announcement](https://aws.amazon.com/blogs/aws/amazon-bedrock-intelligent-prompt-routing/) | official-primary | Primary vendor announcement used to identify managed routing behavior and limits. | 01, 06 | initial-pass |
| S31 | [OpenAI API pricing](https://openai.com/api/pricing/) | official-primary | Primary current pricing reference for OpenAI API economics. | 03, 04, 11 | initial-pass |
| S32 | [OpenAI prompt caching guide](https://platform.openai.com/docs/guides/prompt-caching) | official-primary | Primary documentation for cache eligibility, key order, and cache economics. | 03, 04, 06 | initial-pass |
| S33 | [OpenAI Batch API guide](https://platform.openai.com/docs/guides/batch) | official-primary | Primary documentation for deferred batch work and its cost-latency tradeoff. | 03, 04, 11 | initial-pass |
| S34 | [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) | official-primary | Primary current pricing reference for Anthropic-hosted models. | 03, 04, 11 | initial-pass |
| S35 | [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) | official-primary | Primary documentation for prompt-cache behavior and pricing. | 03, 04, 06 | initial-pass |
| S36 | [Anthropic Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) | official-primary | Primary documentation for asynchronous batch processing and economics. | 03, 04, 11 | initial-pass |
| S37 | [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) | official-primary | Primary current pricing reference for Google Gemini API. | 03, 04, 11 | initial-pass |
| S38 | [Gemini context caching](https://ai.google.dev/gemini-api/docs/caching) | official-primary | Primary documentation for Gemini context-cache behavior and cost. | 03, 04, 06 | initial-pass |
| S39 | [Gemini Batch API](https://ai.google.dev/gemini-api/docs/batch-api) | official-primary | Primary documentation for asynchronous batch processing. | 03, 04, 11 | initial-pass |
| S40 | [DeepSeek API pricing](https://api-docs.deepseek.com/quick_start/pricing) | official-primary | Primary current pricing reference for DeepSeek API; capability labels require separate source confirmation. | 03, 04 | initial-pass |
| S41 | [Mistral technology](https://mistral.ai/technology/) | official-primary | Primary model and technology capability descriptions from Mistral. | 02, 05 | initial-pass |
| S42 | [Leanstral 1.5](https://mistral.ai/news/leanstral-1-5/) | official-primary | Primary model release and coding capability description. | 02, 05 | initial-pass |
| S43 | [Qwen3-Coder](https://qwenlm.github.io/blog/qwen3-coder/) | official-primary | Primary open-model coding capability and release description. | 02, 05 | initial-pass |
| S44 | [Kimi K2](https://moonshotai.github.io/Kimi-K2/) | official-primary | Primary open-model capability and deployment description. | 02, 05 | initial-pass |
| S45 | [DeepSeek news](https://deepseek.com/news) | official-primary | Primary release and capability news surface; individual claims need a dated release record. | 02, 05 | initial-pass |
| S46 | [Llama API](https://www.llama.com/products/llama-api/) | official-primary | Primary hosted access and model capability surface for Llama. | 02, 05, 06 | initial-pass |
| S47 | [Kimi K2.7 in GitHub Copilot](https://github.blog/changelog/2026-07-01-kimi-k2-7-is-now-available-in-github-copilot/) | official-product-changelog | Dated primary product availability record used for the Copilot migration comparison. | 02, 05, 11 | initial-pass |
| S48 | [Optimizing GenAI usage](https://www.finops.org/wg/optimizing-genai-usage/) | official-primary | FinOps guidance for allocation, measurement, and optimization of generative-AI spend. | 04, 11 | initial-pass |
| S49 | [GenAI observability](https://opentelemetry.io/blog/2026/genai-observability/) | official-primary | Primary observability conventions and telemetry framing for GenAI systems. | 07, 10 | initial-pass |
| S50 | [LLM inference benchmarking and cost](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/) | vendor-practitioner | Inference benchmarking methodology and cost drivers; vendor incentives are made explicit. | 03, 05, 07 | initial-pass |
| S51 | [vLLM metrics](https://docs.vllm.ai/en/latest/serving/metrics.html) | official-primary | Primary serving telemetry reference for local and self-hosted inference. | 05, 07, 10 | initial-pass |
| S52 | [vLLM engine arguments](https://docs.vllm.ai/en/latest/serving/engine_args.html) | official-primary | Primary configuration reference for open-weight serving and capacity controls. | 05, 06, 07 | initial-pass |
| S53 | [SGLang documentation](https://docs.sglang.ai/) | official-primary | Primary serving and runtime documentation for an open inference stack. | 05, 06, 07 | initial-pass |
| S54 | [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | official-primary | Risk-management vocabulary and governance reference for regulated deployment. | 10, 12 | initial-pass |
| S55 | [EU regulatory framework for AI](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) | official-primary | Primary regulatory framework reference; legal conclusions require jurisdiction-specific review. | 10, 12 | initial-pass |
| S56 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | official-practitioner | Primary engineering guidance on context selection, compression, and refresh for agents. | 02, 03, 06 | initial-pass |
| S57 | [Optimize LLM response costs and latency with effective caching](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/) | official-practitioner | Primary cloud-practitioner explanation of exact and semantic cache economics. | 03, 04, 06 | initial-pass |
| S58 | [LLM serving or routing research paper](https://arxiv.org/html/2507.03834v1) | primary-research | Recent empirical evidence for serving, routing, or evaluation tradeoffs. | 05, 08, 09 | initial-pass |
| S59 | [LLM serving or routing research paper](https://arxiv.org/html/2606.19544v1) | primary-research | Recent empirical evidence for routing, serving, or evaluation tradeoffs. | 05, 08, 09 | initial-pass |
| S60 | [LLM serving or routing research paper](https://arxiv.org/html/2607.17525v1) | primary-research | Recent empirical evidence for routing, serving, or evaluation tradeoffs. | 05, 08, 09 | initial-pass |
| S61 | [LLM serving or routing research paper](https://arxiv.org/html/2511.17593v1) | primary-research | Recent empirical evidence for routing, serving, or evaluation tradeoffs. | 05, 08, 09 | initial-pass |
| S62 | [LLM serving or routing research paper](https://arxiv.org/html/2509.18101v1) | primary-research | Recent empirical evidence for routing, serving, or evaluation tradeoffs. | 05, 08, 09 | initial-pass |
| S63 | [SWE-bench](https://www.swebench.com/) | benchmark-primary | Task benchmark and evaluation target for coding-agent model selection. | 08, 09 | initial-pass |
| S64 | [Aider leaderboards](https://aider.chat/docs/leaderboards/) | independent-benchmark | Coding benchmark results and methodology context; rankings are time-sensitive and task-specific. | 02, 08, 09 | initial-pass |
| S65 | [Artificial Analysis provider leaderboards](https://artificialanalysis.ai/leaderboards/providers) | independent-benchmark | Provider and model comparison signal; used as a comparison surface, not a universal quality oracle. | 02, 08, 09 | initial-pass |
| S66 | [OpenRouter state of AI](https://openrouter.ai/state-of-ai) | vendor-observatory | Provider and usage landscape signal with explicit vendor incentives. | 02, 04, 11 | initial-pass |
| S67 | [Dynamic model routing with open models](https://snowflake.com/en/blog/dynamic-model-routing-open-models-cortex-ai/) | vendor-practitioner | Canonical-host variant of Snowflake's routing account; retained as a distinct visited URL but treated as duplicate evidence. | 01, 05, 06 | initial-pass |
| S68 | [Cost and quality-aware model selection](https://truefoundry.com/blog/llm-routing-cost-quality-aware-model-selection) | vendor-practitioner | Routing cost-quality framing and implementation patterns from a successfully captured canonical article. | 01, 03, 11 | initial-pass |
| S69 | [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) | official-practitioner | Primary production account for harness feedback loops, repository context, and agent control surfaces. | 06, 09, 11 | initial-pass |
| S70 | [Harness engineering for coding-agent users](https://martinfowler.com/articles/harness-engineering.html) | independent-practitioner | Independent synthesis of harness engineering and the boundary between prompt and environment design. | 06, 09, 11 | initial-pass |
| S71 | [The zero-cost fallacy in the agentic era](https://www.thoughtworks.com/insights/blog/open-source/zero-cost-fallacy-agentic-era) | independent-practitioner | Counter-evidence on the operating cost of apparently free or open models. | 03, 04, 05, 11 | initial-pass |
| S72 | [The honest guide to LLM routing](https://seangeng.com/writing/the-honest-guide-to-llm-routing) | independent-practitioner | Skeptical practitioner account of routing limits and evaluation requirements; recovered by the single permitted retry. | 01, 02, 08 | retry-01 |
| S73 | [LLM routing and model cascades](https://tianpan.co/blog/2025/11/03/llm-routing-model-cascades) | independent-practitioner | Model-cascade design and cost-quality discussion; recovered by the single permitted retry. | 01, 02, 03 | retry-01 |
| S74 | [Klique platform technical deep dive](https://klique.ai/platform/technical-deep-dive/) | vendor-practitioner | Technical routing and platform architecture account; recovered by the single permitted retry. | 01, 06, 07 | retry-01 |
| S75 | [AI coding cost analysis and agent token spend](https://www.augmentcode.com/guides/ai-coding-cost-analysis-agent-token-spend) | vendor-practitioner | Coding-agent spend and token-economics account; recovered by the single permitted retry. | 03, 04, 11 | retry-01 |



## Unaccepted or bounded sources

The SSRN PDF was a security-verification page; the selected Facebook Financial
Times URL redirected to an unrelated video surface; and the Uptime Institute
URL produced a site shell. TrueFoundry's first URL and two LinkedIn URLs were
collector-error lanes; a successful canonical TrueFoundry page and a generic
Facebook group capture are separate records. AWS intelligent-prompt-routing
documentation, AWS model-customization pricing, Mistral technology, Llama API,
and the Thoughtworks zero-cost article remain in the raw selection ledger but
were not promoted to cleaned article evidence because the final page identity
was generic or mismatched. No claim in this packet depends on those five pages.

Reddit canonical pages, X pages, and LinkedIn evidence were not treated as
usable social proof when login, JavaScript-shell, or identity conditions
prevented a headed source read. The HN memo records this absence and the
selection bias of social evidence.

## Current-claim rule

Model names, prices, capabilities, availability, and dates are published only
with a dated primary URL. The official pricing pages in S27, S31, S34, S37,
and S40 are lookup points, not permanent values. The task labels Astra, OASIS,
DeepSeek Flash, GPT-5.6 Luna, and Fable remain unresolved and are excluded
from provider attribution.
