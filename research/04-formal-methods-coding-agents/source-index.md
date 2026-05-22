# Source Index: Formal Methods for Coding Agents

This index labels source quality and explains how each source was used. Browser captures and post-processed article snapshots are under `tmp/` and are not committed.

## Quality labels

- **official** — official project, language, or NASA documentation.
- **primary** — project/lab/workshop source closely tied to the work.
- **paper** — arXiv or formal paper source; peer-review status varies.
- **preprint** — non-peer-reviewed preprint; useful but lower confidence.
- **open-source** — GitHub repository or implementation.
- **practitioner** — practitioner essay or article.
- **community** — HN/community discussion; used as sentiment and skepticism, not proof.

## Sources

| # | Quality | Source | Role | Extracted words | Artifact |
|---:|---|---|---|---:|---|
| 1 | official | [What is Formal Methods?](https://shemesh.larc.nasa.gov/fm/fm-what.html) | NASA definition and baseline limits of formal methods | 704 | `tmp/research-web-critical/formal-methods-coding-agents/articles/shemesh-larc-nasa-gov-fm-fm-what-html/article.md` |
| 2 | official | [The Dafny Programming and Verification Language](https://dafny.org/) | Official Dafny language description | 289 | `tmp/research-web-critical/formal-methods-coding-agents/articles/dafny-org/article.md` |
| 3 | primary | [Dafny: A Language and Program Verifier for Functional Correctness](https://www.microsoft.com/en-us/research/project/dafny-a-language-and-program-verifier-for-functional-correctness/) | Microsoft Research project background for Dafny | 4861 | `tmp/research-web-critical/formal-methods-coding-agents/articles/www-microsoft-com-en-us-research-project-dafny-a-language-and-program-verifier-for-functio/article.md` |
| 4 | official | [Leslie Lamport's TLA+ Home Page](https://lamport.azurewebsites.net/tla/tla.html) | Official creator-maintained TLA+ overview | 300 | `tmp/research-web-critical/formal-methods-coding-agents/articles/lamport-azurewebsites-net-tla-tla-html/article.md` |
| 5 | official | [TLA+ Tools](https://lamport.azurewebsites.net/tla/tools.html) | Official tool overview for SANY, TLC, Apalache, TLAPS | 727 | `tmp/research-web-critical/formal-methods-coding-agents/articles/lamport-azurewebsites-net-tla-tools-html/article.md` |
| 6 | official | [Lean Programming Language and Proof Assistant](https://lean-lang.org/) | Official Lean overview | 1265 | `tmp/research-web-critical/formal-methods-coding-agents/articles/lean-lang-org/article.md` |
| 7 | paper | [DafnyBench: A Benchmark for Formal Software Verification](https://arxiv.org/html/2406.08467v1) | Benchmark for LLM-assisted Dafny verification | 10060 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2406-08467v1/article.md` |
| 8 | open-source | [sun-wendy/DafnyBench](https://github.com/sun-wendy/DafnyBench) | Benchmark repository | 2179 | `tmp/research-web-critical/formal-methods-coding-agents/articles/github-com-sun-wendy-dafnybench/article.md` |
| 9 | paper | [dafny-annotator: AI-Assisted Verification of Dafny Programs](https://arxiv.org/html/2411.15143v1) | LLM plus search for adding Dafny annotations | 5586 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2411-15143v1/article.md` |
| 10 | primary | [dafny-annotator blog post](https://dafny.org/blog/2025/06/21/dafny-annotator/) | Dafny ecosystem blog explanation of dafny-annotator | 2181 | `tmp/research-web-critical/formal-methods-coding-agents/articles/dafny-org-blog-2025-06-21-dafny-annotator/article.md` |
| 11 | open-source | [metareflection/dafny-annotator](https://github.com/metareflection/dafny-annotator) | Tool repository for AI-assisted Dafny verification | 4165 | `tmp/research-web-critical/formal-methods-coding-agents/articles/github-com-metareflection-dafny-annotator/article.md` |
| 12 | paper | [DafnyPro: LLM-Assisted Automated Verification for Dafny Programs](https://arxiv.org/html/2601.05385v1) | 2026 inference-time framework for Dafny annotations | 6584 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2601-05385v1/article.md` |
| 13 | primary | [DafnyPro at Dafny 2026](https://popl26.sigplan.org/details/dafny-2026-papers/12/DafnyPro-LLM-Assisted-Automated-Verification-for-Dafny-Programs) | Conference listing for DafnyPro | 1923 | `tmp/research-web-critical/formal-methods-coding-agents/articles/popl26-sigplan-org-details-dafny-2026-papers-12-dafnypro-llm-assisted-automated-verificati/article.md` |
| 14 | paper | [From Natural Language to Verified Code](https://arxiv.org/html/2604.22601v1) | 2026 natural-language-to-Dafny verified code study | 12781 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2604-22601v1/article.md` |
| 15 | paper | [Intent Formalization: A Grand Challenge for Reliable Coding in the Age of AI Agents](https://arxiv.org/html/2603.17150v1) | 2026 position/research agenda for formalizing user intent | 5621 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2603-17150v1/article.md` |
| 16 | primary | [Intent Formalization blog post](https://risemsr.github.io/blog/2026-03-05-shuvendu-intent-formalization/) | RiSE/MSR accessible version of the intent formalization argument | 5218 | `tmp/research-web-critical/formal-methods-coding-agents/articles/risemsr-github-io-blog-2026-03-05-shuvendu-intent-formalization/article.md` |
| 17 | practitioner | [Can LLMs model real-world systems in TLA+?](https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/) | 2026 SIGOPS article on LLM-generated TLA+ models and SysMoBench | 2501 | `tmp/research-web-critical/formal-methods-coding-agents/articles/www-sigops-org-2026-can-llms-model-real-world-systems-in-tla/article.md` |
| 18 | practitioner | [LLMs and Formal Methods](https://unalarming.com/llms-and-formal-methods) | Practitioner synthesis and provocation | 2568 | `tmp/research-web-critical/formal-methods-coding-agents/articles/unalarming-com-llms-and-formal-methods/article.md` |
| 19 | paper | [Designing Predictable LLM-Verifier Systems for Formal Method Guarantee](https://arxiv.org/abs/2512.02080) | Theoretical LLM-verifier convergence paper, with HN skepticism | 781 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-abs-2512-02080/article.md` |
| 20 | paper | [An In-Context Learning Agent for Formal Theorem-Proving](https://arxiv.org/html/2310.04353v4) | COPRA foundational theorem-proving agent | 13243 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2310-04353v4/article.md` |
| 21 | open-source | [trishullab/copra](https://github.com/trishullab/copra) | COPRA repository | 6230 | `tmp/research-web-critical/formal-methods-coding-agents/articles/github-com-trishullab-copra/article.md` |
| 22 | paper | [Prover Agent: An Agent-Based Framework for Formal Mathematical Proofs](https://arxiv.org/abs/2506.19923) | Agent framework for Lean formal mathematical proofs | 711 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-abs-2506-19923/article.md` |
| 23 | open-source | [kAIto47802/Prover-Agent](https://github.com/kAIto47802/Prover-Agent) | Prover Agent repository | 3515 | `tmp/research-web-critical/formal-methods-coding-agents/articles/github-com-kaito47802-prover-agent/article.md` |
| 24 | paper | [A Minimal Agent for Automated Theorem Proving](https://arxiv.org/html/2602.24273v1) | 2026 minimal theorem-proving agent baseline | 11207 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2602-24273v1/article.md` |
| 25 | paper | [AgentGuard: Runtime Verification of AI Agents](https://arxiv.org/html/2509.23864v1) | Runtime verification framework for agent behavior | 4354 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2509-23864v1/article.md` |
| 26 | open-source | [GoPlusSecurity/agentguard](https://github.com/GoPlusSecurity/agentguard) | Runtime security guard implementation for coding agents | 9299 | `tmp/research-web-critical/formal-methods-coding-agents/articles/github-com-goplussecurity-agentguard/article.md` |
| 27 | paper | [AgentRaft: Automated Detection of Data Over-Exposure in LLM Agents](https://arxiv.org/html/2603.07557v1) | Program-analysis and runtime taint approach to agent privacy/data-flow risk | 12813 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2603-07557v1/article.md` |
| 28 | paper | [SEVerA: Verified Self-Evolving Agents](https://arxiv.org/html/2603.25111v2) | 2026 formally guarded generative model approach for self-evolving agents | 18966 | `tmp/research-web-critical/formal-methods-coding-agents/articles/arxiv-org-html-2603-25111v2/article.md` |
| 29 | preprint | [AgentVerify: Compositional Formal Verification of AI Agent Safety Properties via LTL Model Checking](https://preprints.org/manuscript/202604.1029) | Non-peer-reviewed 2026 preprint on LTL model checking for agent safety | 23054 | `tmp/research-web-critical/formal-methods-coding-agents/articles/preprints-org-manuscript-202604-1029/article.md` |
| 30 | primary | [Bridging LLM Planning Agents and Formal Methods](https://conf.researchr.org/details/ase-2025/agenticse-2025-papers/12/Bridging-LLM-Planning-Agents-and-Formal-Methods-A-Case-Study-in-Plan-Verification) | ASE 2025 AgenticSE workshop case study listing | 1708 | `tmp/research-web-critical/formal-methods-coding-agents/articles/conf-researchr-org-details-ase-2025-agenticse-2025-papers-12-bridging-llm-planning-agents/article.md` |
| 31 | practitioner | [Prediction: AI will make formal verification go mainstream](https://simonwillison.net/2025/Dec/9/formal-verification/) | Practitioner signal about mainstreaming formal verification | 684 | `tmp/research-web-critical/formal-methods-coding-agents/articles/simonwillison-net-2025-dec-9-formal-verification/article.md` |
| 32 | community | [HN: Can LLMs model real-world systems in TLA+?](https://news.ycombinator.com/item?id=48065254) | Practitioner discussion of TLA+ modeling with LLMs | 2028 | `tmp/research-web-critical/formal-methods-coding-agents/articles/news-ycombinator-com-item-id-48065254/article.md` |
| 33 | community | [HN: Designing Predictable LLM-Verifier Systems for Formal Method Guarantee](https://news.ycombinator.com/item?id=46411539) | Skeptical practitioner discussion of theoretical LLM-verifier guarantee claims | 877 | `tmp/research-web-critical/formal-methods-coding-agents/articles/news-ycombinator-com-item-id-46411539/article.md` |
| 34 | community | [HN: Lean 4 and AI theorem proving](https://news.ycombinator.com/item?id=47047027) | Practitioner discussion of Lean as proof assistant for AI | 5912 | `tmp/research-web-critical/formal-methods-coding-agents/articles/news-ycombinator-com-item-id-47047027/article.md` |
| 35 | open-source | [Beneficial-AI-Foundation/dafny-autopilot](https://github.com/Beneficial-AI-Foundation/dafny-autopilot) | VS Code extension showing practical AI-assisted Dafny verification workflow | 3677 | `tmp/research-web-critical/formal-methods-coding-agents/articles/github-com-beneficial-ai-foundation-dafny-autopilot/article.md` |
| 36 | open-source | [RaghavRoy145/autocomplete-and-verify](https://github.com/RaghavRoy145/autocomplete-and-verify) | Small Emacs package for formally verified LLM code generation and correction | 2425 | `tmp/research-web-critical/formal-methods-coding-agents/articles/github-com-raghavroy145-autocomplete-and-verify/article.md` |

## Source-selection notes

- Official sources define the baseline vocabulary: NASA for formal methods, Dafny for verification-aware programming, TLA+ for model checking, and Lean for proof assistants.

- Papers were preferred for claims about benchmark size, success rates, and technical mechanisms. Vendor/project pages were used for adoption and tooling details.

- HN threads are cited only as community signal and skepticism. They are not treated as proof that a technical claim is true.

- Sources from the last six months are emphasized in the guide, especially Intent Formalization, DafnyPro, NL2VC, SysMoBench, AgentRaft, SEVerA, AgentVerify, and recent HN discussions. Older sources are included when foundational.

