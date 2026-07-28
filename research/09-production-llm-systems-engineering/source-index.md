# Source index

This catalog reconciles all 102 durable records in [`sources.json`](sources.json)
with the rendered article corpus and source-native social captures. Titles are
the exact, recognizable page or paper titles wherever the extraction is
meaningful. Hacker News, X, LinkedIn, and Reddit entries retain their curated
identity-aware titles rather than generic browser headings.

Search-result snippets were discovery leads only. The boundary prefix in the
last column states how far each source can support a claim: research remains
study-specific; standards and security checklists are normative rather than
outcome evidence; first-party and vendor accounts carry product incentives;
implementation sources require version pinning; and community/social evidence
is anecdotal rather than representative.

## 01 — Harness engineering

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH01-S01` | [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) | OpenAI | `official-practitioner` | **First-party practice.** Primary production account defining harness engineering and the repository/environment feedback loop around coding agents. |
| `CH01-S02` | [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) | Birgitta Böckeler / Thoughtworks | `independent-practitioner` | **Practitioner synthesis.** Independent synthesis that sharpens the term and exposes where harness work differs from prompt work. |
| `CH01-S03` | [Hacker News: Harness engineering — Leveraging Codex in an agent-first world](https://news.ycombinator.com/item?id=48416264) | Hacker News community | `community-signal` | **Anecdotal community signal.** Practitioner discussion supplies skepticism, vocabulary disputes, and operational counterexamples. |
| `CH01-S04` | [@ghumare64: As an AI Engineer, please learn — 22 production disciplines](https://x.com/ghumare64/status/2062430351021015331) | Gaurav Humare | `native-social-signal` | **Bounded curriculum signal; intentionally uncited in technical prose.** The native root contains the 22-topic field-interest map; it supplies no technical validation. |

## 02 — Context engineering

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH02-S01` | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Anthropic | `official-practitioner` | **First-party practice.** Primary engineering guidance on selecting, compressing, and refreshing agent context. |
| `CH02-S02` | [Context Engineering: A Practical Guide for AI Agents (2026)](https://sourcegraph.com/blog/context-engineering) | Sourcegraph | `official-practitioner` | **First-party practice.** Production coding-agent perspective on context lifecycle and system boundaries. |
| `CH02-S03` | [Context Engineering](https://www.langchain.com/blog/context-engineering-for-agents) | LangChain | `vendor-practitioner` | **Commercially interested practice.** Concrete taxonomy of context types and agent-time context operations. |
| `CH02-S04` | [Hacker News: The new skill in AI is not prompting, it is context engineering](https://news.ycombinator.com/item?id=44427757) | Hacker News community | `community-signal` | **Bounded community counter-signal; intentionally uncited.** The native thread records rebrand and buzzword skepticism, not prevalence or a technical result. |

## 03 — Caching LLM work safely

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH03-S01` | [Optimize LLM response costs and latency with effective caching](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/) | Amazon Web Services | `official-practitioner` | **First-party practice.** Explains exact and semantic caching mechanisms, economics, and architecture choices. |
| `CH03-S02` | [SemanticALLI: Caching Reasoning, Not Just Responses, in Agentic Systems](https://arxiv.org/html/2601.16286v1) | Varun Chillara et al. | `primary-research` | **Study-specific.** Recent semantic-cache research provides algorithms, benchmarks, and limitations beyond vendor claims. |
| `CH03-S03` | [Semantic Caching Thresholds and Why They Matter](https://portkey.ai/blog/semantic-caching-thresholds) | Portkey | `vendor-practitioner` | **Commercially interested practice.** Operational treatment of similarity thresholds and the false-hit/false-miss tradeoff. |
| `CH03-S04` | [Semantic Caching for LLMs: TTLs, Confidence, and Cache Safety](https://pyimagesearch.com/2026/05/04/semantic-caching-for-llms-ttls-confidence-and-cache-safety/) | PyImageSearch | `independent-practitioner` | **Practitioner synthesis.** Recent implementation-oriented discussion of TTLs, confidence, invalidation, and cache safety. |

## Interlude 03a — Minimum model vocabulary

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH03A-S01` | [Attention Is All You Need](https://arxiv.org/html/1706.03762v7) | Ashish Vaswani et al. / Google Brain, Google Research, University of Toronto | `primary-research` | **Foundational, architecture-specific research.** Defines the original encoder-decoder Transformer, Q/K/V attention, and causal decoder masking; it does not describe every modern decoder-only serving implementation. |
| `CH03A-S02` | [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) | Alec Radford et al. / OpenAI | `primary-research` | **Foundational, model-specific research.** Grounds GPT-2's language-model and byte-level BPE design; it is not current serving-performance evidence. |
| `CH03A-S03` | [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://aclanthology.org/D19-1410/) | Nils Reimers and Iryna Gurevych / Association for Computational Linguistics | `primary-research` | **Foundational, task-specific research.** Demonstrates sentence embeddings and cosine-similarity retrieval; similarity does not establish truth, authorization, or tenant compatibility. |

## 04 — KV-cache systems

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH04-S01` | [Towards Efficient Large Language Model Serving: A Survey on System-Aware KV Cache Optimization](https://arxiv.org/html/2607.08057v1) | Jiantong Jiang et al. | `primary-research` | **Study-specific.** System-aware survey maps KV-cache reuse, compression, eviction, placement, and scheduling; the version was resolved from the rendered arXiv page. |
| `CH04-S02` | [Comparative Characterization of KV Cache Management Strategies for LLM Inference](https://arxiv.org/html/2604.05012v1) | Oteo Mamo et al. | `primary-research` | **Study-specific.** Comparative evidence distinguishes the real workloads and metrics behind KV-cache policies. |
| `CH04-S03` | [Agentic Inference](https://docs.nvidia.com/dynamo/dev/digest/agentic-inference) | NVIDIA | `official-documentation` | **Version-specific first-party docs.** Vendor architecture material connects long-running agent workloads to distributed KV-cache pressure. |
| `CH04-S04` | [r/LocalLLaMA: KV Cache is huge and bottlenecks LLM inference](https://www.reddit.com/r/LocalLLaMA/comments/1ap3bkt/kv_cache_is_huge_and_bottlenecks_llm_inference_we/) | Reddit / r/LocalLLaMA | `native-social-signal` | **Identity-confirmed social signal.** Hands-on discussion surfaces memory sizing confusion and deployment pain that polished docs omit. |
| `CH04-S05` | [Aanchal Karamchandani: Inside LLM inference — when the KV cache no longer fits](https://www.linkedin.com/posts/aanchalkaramchandani_inside-llm-inference-when-the-kv-cache-no-activity-7450945152912822273-YIpQ) | Aanchal Karamchandani | `native-social-signal` | **Capture gap; discovery-only and intentionally uncited.** The activity URL was found, but the root post/carousel body was not captured; it supports no KV-cache claim. |

## 05 — Prefill/decode disaggregation

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH05-S01` | [Towards High-Goodput LLM Serving with Prefill-decode Multiplexing](https://arxiv.org/html/2504.14489v3) | Yukang Chen et al. | `primary-research` | **Study-specific.** Primary goodput study explains prefill/decode interference and disaggregation decisions. |
| `CH05-S02` | [Disaggregated Prefilling (experimental)](https://docs.vllm.ai/en/latest/features/disagg_prefill/) | vLLM Project | `official-documentation` | **Version-specific first-party docs.** Implementation documentation states mechanics, constraints, and when disaggregated prefill is unsuitable. |
| `CH05-S03` | [DistServe Retro](https://haoailab.com/blogs/distserve-retro/) | Hao AI Lab | `independent-practitioner` | **Practitioner synthesis.** Retrospective gives design history and lessons from DistServe rather than only benchmark claims. |
| `CH05-S04` | [Disaggregated prefill and decode for LLM inference on SageMaker HyperPod](https://aws.amazon.com/blogs/machine-learning/disaggregated-prefill-and-decode-for-llm-inference-on-sagemaker-hyperpod/) | Amazon Web Services | `official-practitioner` | **First-party practice.** Production deployment view ties TTFT, inter-token latency, hardware, and operations together. |

## 06 — Continuous batching and serving engines

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH06-S01` | [Inside vLLM: Anatomy of a High-Throughput LLM Inference System](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm) | Aleksa Gordić / vLLM | `official-practitioner` | **First-party practice.** Engine anatomy explains scheduler, paged KV memory, batching, and request lifecycle as one system. |
| `CH06-S02` | [Continuous batching](https://huggingface.co/blog/continuous_batching) | Hugging Face | `official-practitioner` | **First-party practice.** First-principles explanation and runnable mental model for continuous batching. |
| `CH06-S03` | [Comparative Analysis of Large Language Model Inference Serving Systems: A Performance Study of vLLM and HuggingFace TGI](https://arxiv.org/html/2511.17593v1) | Saicharan Kolluru | `primary-research` | **Study-specific.** Comparative serving study provides throughput and latency evidence across vLLM and TGI. |
| `CH06-S04` | [vLLM: Easy, fast, and cheap LLM serving for everyone](https://github.com/vllm-project/vllm) | vLLM Project | `implementation-source` | **Implementation snapshot.** Trace mechanisms to a pinned revision; repository behavior changes over time. |
| `CH06-S05` | [Andrew Ng: New course on Serving LLMs Efficiently](https://www.linkedin.com/posts/andrewyng_new-course-on-serving-llms-efficiently-activity-7468342916764250112-8HxO) | Andrew Ng / DeepLearning.AI | `native-social-signal` | **Capture gap; discovery-only and intentionally uncited.** The retained body is a third-party comment rather than Andrew Ng's root post; attribute no adoption or technical claim to it. |

## 07 — Speculative decoding

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH07-S01` | [Speculative Decoding and Beyond: An In-Depth Review of Techniques](https://arxiv.org/html/2502.19732v1) | Yunhai Hu et al. | `primary-research` | **Study-specific.** Survey establishes speculative-decoding families, verification cost, acceptance, and system interactions. |
| `CH07-S02` | [An Introduction to Speculative Decoding for Reducing Latency in AI Inference](https://developer.nvidia.com/blog/an-introduction-to-speculative-decoding-for-reducing-latency-in-ai-inference/) | NVIDIA | `official-practitioner` | **First-party practice.** Clear implementation-oriented explanation of draft/verify latency mechanics and hardware concerns. |
| `CH07-S03` | [DistillSpec: Improving speculative decoding via knowledge distillation](https://research.google/pubs/distillspec-improving-speculative-decoding-via-knowledge-distillation/) | Google Research | `primary-research` | **Study-specific.** DistillSpec directly connects knowledge distillation to draft-model acceptance and serving speed. |
| `CH07-S04` | [Can Compressed LLMs Truly Act? An Empirical Evaluation of Agentic Capabilities in LLM Compression](https://icml.cc/virtual/2025/poster/43871) | Peijie Dong et al. | `primary-research` | **Study-specific.** Compression results depend on the evaluated tasks, models, and compression methods. |

## 08 — Quantization

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH08-S01` | [“Give Me BF16 or Give Me Death”? Accuracy-Performance Trade-Offs in LLM Quantization](https://arxiv.org/html/2411.02355v4) | Eldar Kurtić et al. | `primary-research` | **Study-specific.** Broad survey supplies definitions, method taxonomy, quality measures, and research limits. |
| `CH08-S02` | [Quantization concepts](https://huggingface.co/docs/transformers/en/quantization/concept_guide) | Hugging Face | `official-documentation` | **Version-specific first-party docs.** Definitions connect numeric formats and weight/activation choices to supported tooling. |
| `CH08-S03` | [Quantization for Inference: GPTQ, AWQ, SmoothQuant, and FP8](https://www.generalcompute.com/blog/quantization-for-inference-gptq-awq-smoothquant-fp8) | General Compute | `independent-practitioner` | **Practitioner synthesis.** Comparative explanation distinguishes algorithms from storage formats; benchmark independently. |
| `CH08-S04` | [r/LocalLLaMA: Quantization quality for AWQ, GPTQ, FP8, and NVFP4](https://www.reddit.com/r/LocalLLaMA/comments/1s9iyrw/has_anyone_tested_the_quantization_quality/) | Reddit / r/LocalLLaMA | `native-social-signal` | **Identity-confirmed social signal.** User testing and disagreement are useful hypotheses, not controlled quality estimates. |

## 09 — Structured outputs

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH09-S01` | [Introducing Structured Outputs in the API](https://openai.com/index/introducing-structured-outputs-in-the-api/) | OpenAI | `official-documentation` | **Version-specific first-party docs.** Provider contract establishes schema behavior, not semantic correctness. |
| `CH09-S02` | [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | Anthropic | `official-documentation` | **Version-specific first-party docs.** A second provider reveals portability differences, limitations, and error behavior. |
| `CH09-S03` | [Generating Structured Outputs from Language Models: Benchmark and Studies](https://arxiv.org/html/2501.10868v1) | Saibo Geng et al. | `primary-research` | **Study-specific.** Research taxonomy explains constrained-generation techniques and evaluation dimensions. |
| `CH09-S04` | [The Hidden Cost of Structure: How Constrained Decoding Affects Language Model Performance](https://aclanthology.org/2025.ranlp-1.124/) | Maximilian Schall and Gerard de Melo | `primary-research` | **Study-specific.** Empirical evidence tests quality changes rather than only format validity. |
| `CH09-S05` | [Structured outputs in production: lessons learned](https://cadence.withremote.ai/blog/structured-outputs-llm-production) | Harsh Shuddhalwar / Cadence | `independent-practitioner` | **Practitioner synthesis.** Production lessons cover validation, retries, repairs, and application-level failures. Published May 22, 2026; Cadence is a Remote product surface. |

## 10 — Tool use and function calling

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH10-S01` | [The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models](https://proceedings.mlr.press/v267/patil25a.html) | Shishir G. Patil et al. | `primary-research` | **Study-specific.** BFCL grounds reliability in measurable categories; results remain benchmark- and version-dependent. |
| `CH10-S02` | [ToolScan: A Benchmark for Characterizing Errors in Tool-Use LLMs](https://arxiv.org/html/2411.13547v2) | Shirley Kokane et al. | `primary-research` | **Study-specific.** ToolScan characterizes tool-selection and argument-generation errors. |
| `CH10-S03` | [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) | Anthropic | `official-practitioner` | **First-party practice.** Provider guidance covers discovery and contracts but is product-specific. |
| `CH10-S04` | [Self-Healing Agentic Orchestrators for Reliable Tool-Augmented Large Language Model Systems](https://arxiv.org/html/2606.01416v1) | Rahul Suresh Babu and Adarsh Agrawal | `primary-research` | **Study-specific.** Recovery evidence does not justify unbounded retries or universal reliability claims. |

## 11 — Runtime guardrails and behavioral contracts

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH11-S01` | [Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned](https://arxiv.org/html/2603.05344v1) | Nghi D. Q. Bui / OpenDev | `primary-research` | **Study-specific.** Terminal-agent evidence exposes safety and liveness issues in its studied harness. |
| `CH11-S02` | [Agent Behavioral Contracts: Formal Specification and Runtime Enforcement for Reliable Autonomous AI Agents](https://arxiv.org/html/2602.22302v1) | Varun Pratap Bhardwaj | `primary-research` | **Study-specific.** Formal vocabulary is useful; claimed enforcement remains implementation- and threat-model-dependent. |
| `CH11-S03` | [Runtime Budget Guardrails for Agentic AI](https://blogs.oracle.com/ai-and-datascience/runtime-budget-guardrails-agentic-ai) | Oracle | `vendor-practitioner` | **Commercially interested practice.** Concrete token, time, tool, and iteration budgets are patterns, not measured guarantees. |
| `CH11-S04` | [Hacker News: Do not let an LLM make decisions or execute business logic](https://news.ycombinator.com/item?id=43542259) | Hacker News community | `community-signal` | **Anecdotal community signal.** Debate surfaces authorization concerns but cannot measure prevalence. |

## 12 — Model routing

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH12-S01` | [A Unified Approach to Routing and Cascading for LLMs](https://arxiv.org/html/2410.10347v3) | Jasper Dekoninck et al. | `primary-research` | **Study-specific.** RouteLLM supplies algorithms and cost-quality assumptions that need workload validation. |
| `CH12-S02` | [RouterEval: A Comprehensive Benchmark for Routing LLMs to Explore Model-level Scaling Up in LLMs](https://arxiv.org/html/2503.10657) | Zhongzhan Huang et al. | `primary-research` | **Study-specific.** Benchmark tests generalization while exposing evaluation weaknesses. |
| `CH12-S03` | [Large Language Model Routing With Benchmark Datasets](https://research.ibm.com/publications/large-language-model-routing-with-benchmark-datasets) | IBM Research | `primary-research` | **Study-specific.** Industry research adds workload-aware routing evidence; the extracted landing page is abstract-level. |
| `CH12-S04` | [LLM routing in production: Choosing the right model for every request](https://blog.logrocket.com/llm-routing-right-model-for-requests/) | LogRocket | `independent-practitioner` | **Practitioner synthesis.** Application guide connects policy to fallbacks; cost examples are not audited evidence. |

## 13 — Production RAG pipelines

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH13-S01` | [A Hybrid Retrieval and Reranking Framework for Evidence-Grounded Retrieval-Augmented Generation](https://arxiv.org/html/2605.01664v1) | Fariba Afrin Irany and Sampson Akwafuo | `primary-research` | **Study-specific.** Architecture evidence is bounded to the reported datasets and evaluation. |
| `CH13-S02` | [RAG Pipeline Challenges: From Data Ingestion to Retrieval](https://unstructured.io/insights/rag-pipeline-challenges-from-data-ingestion-to-retrieval) | Unstructured | `vendor-practitioner` | **Commercially interested practice.** Pipeline account emphasizes pre-generation failure modes. |
| `CH13-S03` | [Production RAG Evaluation: Keyword, Vector, SQL, or Hybrid Search?](https://blogs.oracle.com/developers/production-rag-evaluation-keyword-vector-sql-or-hybrid-search) | Oracle | `vendor-practitioner` | **Commercially interested practice.** Concrete retrieval comparison requires independent workload validation. |
| `CH13-S04` | [Hacker News: RAG at scale — synchronizing and ingesting billions of embeddings](https://news.ycombinator.com/item?id=37824547) | Hacker News community | `community-signal` | **Anecdotal community signal.** Discussion contributes incidents and simpler alternatives, not prevalence. |
| `CH13-S05` | [LinkedIn comments on Elliot One: Most RAG systems fail before the LLM even runs](https://www.linkedin.com/posts/elliotone_most-rag-systems-fail-before-the-llm-even-activity-7475503003295232000-OMrU) | Lukas Walter and Elliot One | `native-social-signal` | **Comment-thread signal; root unavailable.** The captured comments name retrieval quality, chunking, metadata, authorization, freshness, and telemetry; they neither confirm the root-post title nor establish prevalence. |

## 14 — RAG and citation evaluation

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH14-S01` | [Evaluation of Retrieval-Augmented Generation: A Survey](https://arxiv.org/html/2405.07437v2) | Hao Yu et al. | `primary-research` | **Study-specific.** Survey organizes metrics and benchmarks; inherited claims remain secondary. |
| `CH14-S02` | [Overview of the TREC 2025 Retrieval Augmented Generation (RAG) Track](https://arxiv.org/html/2603.09891v1) | Shivani Upadhyay et al. | `primary-research` | **Study-specific.** TREC protocols are rigorous but bounded to track tasks and judgments. |
| `CH14-S03` | [CiteGuard: Faithful Citation Attribution for LLMs via Retrieval-Augmented Validation](https://arxiv.org/html/2510.17853v3) | Yee Man Choi et al. | `primary-research` | **Study-specific.** Separates citation presence from attribution; performance is benchmark-specific. |
| `CH14-S04` | [RAG Evaluation: Don’t let customers tell you first](https://www.pinecone.io/learn/series/vector-databases-in-production-for-busy-engineers/rag-evaluation/) | Pinecone | `vendor-practitioner` | **Commercially interested practice.** Useful iterative workflow, not neutral tool-comparison evidence. |

## 15 — Evaluation systems and LLM judges

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH15-S01` | [When Generic Prompt Improvements Hurt: Evaluation-Driven Iteration for LLM Applications](https://arxiv.org/html/2601.22025v2) | Daniel Commey | `primary-research` | **Study-specific.** Framework emphasizes regression-aware iteration; results remain task-specific. |
| `CH15-S02` | [Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias](https://arxiv.org/html/2606.19544v1) | Justin D. Norman et al. | `primary-research` | **Study-specific.** Judge agreement and consistency do not establish construct validity. |
| `CH15-S03` | [Evaluating Scoring Bias in LLM-as-a-Judge](https://arxiv.org/html/2506.22316v4) | Qingquan Li et al. | `primary-research` | **Study-specific.** Bias findings depend on the evaluated judges, prompts, and scoring design. |
| `CH15-S04` | [Evaluating the Evaluator: How to Test an LLM Judge with Microsoft Agent Framework](https://techcommunity.microsoft.com/blog/educatordeveloperblog/evaluating-the-evaluator-how-to-test-an-llm-judge-with-microsoft-agent-framework/4516639) | Microsoft | `official-practitioner` | **First-party practice.** Concrete meta-evaluation procedure is tied to Microsoft tooling. |
| `CH15-S05` | [Hacker News: About AI Evals](https://news.ycombinator.com/item?id=44430117) | Hacker News community | `community-signal` | **Anecdotal community signal.** Adds failures and disagreement, not representative outcome data. |
| `CH15-S06` | [@suraj_sharma14: Golden datasets and evaluation systems](https://x.com/suraj_sharma14/status/2081273315901964705) | Suraj Sharma | `native-social-signal` | **Identity-confirmed social signal.** Adoption advice is triangulated against evaluation research. |

## 16 — GenAI observability

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH16-S01` | [Gen AI semantic attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) | OpenTelemetry | `official-standard` | **Normative, not outcome evidence.** Defines interoperable trace and metric vocabulary; conventions can evolve. |
| `CH16-S02` | [Inside the LLM Call: GenAI Observability with OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/) | James Newton-King / OpenTelemetry | `official-practitioner` | **First-party practice.** Explains the emerging telemetry model without measuring incident outcomes. |
| `CH16-S03` | [Comprehensive observability for Amazon SageMaker AI LLM inference: From GPU utilization to LLM quality](https://aws.amazon.com/blogs/machine-learning/comprehensive-observability-for-amazon-sagemaker-ai-llm-inference-from-gpu-utilization-to-llm-quality/) | Amazon Web Services | `official-practitioner` | **First-party practice.** AWS-native architecture, not independent evidence of quality improvement. |
| `CH16-S04` | [Hacker News: You do not need to adopt new tools for LLM observability](https://news.ycombinator.com/item?id=39371297) | Hacker News community | `community-signal` | **Anecdotal community signal.** Tool criticism and integration reports cannot establish adoption or impact. |

## 17 — AI FinOps and unit economics

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH17-S01` | [FinOps for AI: Tools & Services Considerations](https://www.finops.org/wg/finops-for-ai-tools-services-considerations/) | FinOps Foundation | `official-standard` | **Normative, not outcome evidence.** Identifies allocation and usage-data requirements; savings ranges need workload proof. |
| `CH17-S02` | [Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/) | FinOps Foundation | `official-standard` | **Normative, not outcome evidence.** Grounds business units; example arithmetic is illustrative. |
| `CH17-S03` | [Optimizing GenAI Usage: A FinOps Perspective on Cost, Performance, and Efficiency](https://www.finops.org/wg/optimizing-genai-usage/) | FinOps Foundation | `official-practitioner` | **First-party practice.** Optimization guidance is not a universal savings benchmark. |
| `CH17-S04` | [Hacker News: Forecasting AI API costs for agent workflows](https://news.ycombinator.com/item?id=47332177) | Hacker News community | `community-signal` | **Anecdotal community signal.** Pricing surprises and heuristics include product-promotion conflicts. |

## 18 — Prompt injection, MCP, and RAG security

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH18-S01` | [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | OWASP | `security-authority` | **Security checklist/threat model.** Layered mitigations are recommendations, not efficacy measurements. |
| `CH18-S02` | [MCP (Model Context Protocol) Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html) | OWASP | `security-authority` | **Security checklist/threat model.** Covers permissions and supply chain; compliance does not prove safety. |
| `CH18-S03` | [Retrieval-Augmented Generation (RAG) Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html) | OWASP | `security-authority` | **Security checklist/threat model.** Covers the full pipeline; suggested defaults are heuristics. |
| `CH18-S04` | [SoK: The Attack Surface of Agentic AI — Tools, and Autonomy](https://arxiv.org/html/2603.22928v1) | Ali Dehghantanha and Sajad Homayoun | `primary-research` | **Study-specific.** Systematizes prior work rather than adding a new exploit population. |
| `CH18-S05` | [Exploiting Web Search Tools of AI Agents for Data Exfiltration](https://arxiv.org/html/2510.09093v2) | Dennis Rall et al. | `primary-research` | **Study-specific.** Attack rates are tied to the forced-page, single-run experimental setup. |

## 19 — Multi-tenancy and state isolation

The two KV-cache records are deliberately separate: `CH19-S06` is the
PromptPeek attack paper, while `CH19-S02` is the later SafeKV selective-sharing
defense. They were previously fused by a canonical-page repair and must not be
treated as one study.

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH19-S01` | [Multi-Tenant Application Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html) | OWASP | `security-authority` | **Security checklist/threat model.** General isolation patterns are normative, not incident-rate evidence. |
| `CH19-S02` | [Selective KV-Cache Sharing to Mitigate Timing Side-Channels in LLM Inference](https://arxiv.org/html/2508.08438v2) | Kexin Chu et al. | `primary-research` | **Study-specific defense.** SafeKV evaluates selective sharing under its detector and deployment assumptions. |
| `CH19-S06` | [I Know What You Asked: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/) | Guanlong Wu et al. | `primary-research` | **Study-specific attack.** PromptPeek demonstrates an API-visible timing channel; it is not the SafeKV paper. |
| `CH19-S03` | [Continuous Discovery of Vulnerabilities in LLM Serving Systems with Fuzzing](https://arxiv.org/html/2605.11202v1) | Yunze Zhao et al. | `primary-research` | **Study-specific.** Two-engine fuzzing discovers concrete bugs but cannot estimate ecosystem prevalence. |
| `CH19-S04` | [Confused ChatGPT: Cross-App Context Poisoning via First-Party APIs](https://arxiv.org/html/2606.00485v1) | Chao Wang, Somesh Jha, and Zhiqiang Lin | `primary-research` | **Study-specific.** Platform/version-specific reverse engineering; no observed third-party exploitation. |
| `CH19-S05` | [OWASP Agent Memory Guard](https://owasp.org/www-project-agent-memory-guard/) | OWASP | `security-authority` | **Design-stage project.** The captured roadmap does not yet provide efficacy evidence. |

## 20 — Prompting, RAG, and fine-tuning

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH20-S01` | [Fine-Tuning vs. RAG for Multi-Hop Question Answering with Novel Knowledge](https://arxiv.org/html/2601.07054v1) | Zhuoyi Yang et al. | `primary-research` | **Study-specific.** Controlled comparison is bounded to three 7B models and multiple-choice datasets. |
| `CH20-S02` | [Distilling Many-Shot In-Context Learning into a Cheat Sheet](https://arxiv.org/html/2509.20820v1) | Ukyo Honda, Soichiro Murakami, and Peinan Zhang | `primary-research` | **Study-specific.** Selected tasks favor settings where many-shot prompting already helped. |
| `CH20-S03` | [Finetune Vs Rag Vs Prompt](https://www.tmls.nyc/research/finetune-vs-rag-vs-prompt) | TMLS Research | `independent-practitioner` | **Practitioner synthesis.** Decision framework compiles external evidence; exact gains are secondary. |
| `CH20-S04` | [To fine-tune or not to fine-tune](https://ai.meta.com/blog/when-to-fine-tune-llms-vs-other-techniques/) | Meta AI | `official-practitioner` | **First-party practice.** Useful lifecycle tradeoffs with an open-model fine-tuning incentive. |

## 21 — Inference benchmarking and economics

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH21-S01` | [LLM Inference Benchmarking: Fundamental Concepts](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/) | NVIDIA | `official-practitioner` | **First-party practice.** Metric definitions are useful; tool formulas and vendor incentives must be disclosed. |
| `CH21-S02` | [LLM Inference Benchmarking: How Much Does Your LLM Inference Cost?](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/) | NVIDIA | `official-practitioner` | **First-party practice.** Sizing method is useful; hardware costs are illustrative, not market facts. |
| `CH21-S03` | [Economic Evaluation of LLMs](https://arxiv.org/html/2507.03834v1) | Michael J. Zellinger and Matt Thomson | `primary-research` | **Study-specific.** Economic conclusions depend on MATH tasks and assigned costs of error, latency, and abstention. |
| `CH21-S04` | [The LLM Inference Trilemma: Throughput, Latency, Cost](https://www.digitalocean.com/blog/llm-inference-tradeoffs) | DigitalOcean | `vendor-practitioner` | **Commercially interested practice.** Provider synthesis without a controlled cross-hardware benchmark. |
| `CH21-S05` | [Blink: CPU-Free LLM Inference by Delegating the Serving Stack to GPU and SmartNIC](https://arxiv.org/html/2604.07609v1) | Mohammad Siavashi et al. / KTH Royal Institute of Technology and RISE | `primary-research` | **Author-benchmarked preprint.** Versioned, matched-server comparison reports tail latency and goodput, but uses an additional DPU, disables unsupported baseline features, omits cancellation and cost, has unreleased code, and retains placeholder conference metadata. |

## 22 — Production failure and reliability

| ID | Searchable source | Author / organization | Class | Evidence use and boundary |
| --- | --- | --- | --- | --- |
| `CH22-S01` | [FailureAtlas: A Taxonomy of Failure Modes in Multi-Provider LLM Serving Infrastructure](https://arxiv.org/html/2607.17525v1) | Vishal Pandey and Gopal Singh / Metriqual | `primary-research` | **Study-specific.** Five catalog entries demonstrate mechanisms, not prevalence. |
| `CH22-S02` | [When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime](https://arxiv.org/html/2606.14589v1) | Wei Wu | `primary-research` | **Study-specific.** Single-system, eight-week postmortem corpus; frequencies do not generalize. |
| `CH22-S03` | [Characterizing Faults in Agentic AI: A Taxonomy of Types, Symptoms, and Root Causes](https://arxiv.org/html/2603.06847v1) | Mehil B. Shah et al. | `primary-research` | **Study-specific.** Repository and survey sampling favors popular Python projects; rendered 2009 date is corrupt. |
| `CH22-S04` | [Why your AI model performs great offline but fails in production](https://www.growthbook.io/insights/why-your-ai-model-performs-great-offline-but-fails-production) | GrowthBook | `vendor-practitioner` | **Vendor-authored synthesis.** Useful staged-evaluation and rollout checklist, not production-outcome evidence. |
| `CH22-S05` | [Hacker News: Agent design is still hard](https://news.ycombinator.com/item?id=46013935) | Hacker News community | `community-signal` | **Anecdotal community signal.** Supports design-churn discussion, not reliability measurement. |
