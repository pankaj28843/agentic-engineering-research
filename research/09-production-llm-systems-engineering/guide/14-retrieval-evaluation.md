# 14. Retrieval evaluation: grade each runner in the relay

A RAG answer can fail because retrieval missed evidence, context lacked enough
evidence, generation ignored it, a claim was unsupported, or a citation named
the wrong source. These are different failure classes with different
denominators.

The most important evaluation rule is:

> never let one end-to-end score erase the stage that needs repair.

## ELI5: grade finding, using, and citing separately

A student writes a report.

1. Did they find the right books?
2. Did the books contain enough information?
3. Did the report state correct things from those books?
4. Does each footnote support the sentence beside it?
5. Did the report answer the assignment?

A polished report can fail question 4. A perfect set of books can still produce
a poor report. RAG needs the same separate marks.

## The evaluation ladder

```text
retrieval relevance
  → evidence coverage/sufficiency
  → answer correctness
  → claim faithfulness/support
  → citation attribution
  → task/user outcome
```

[Hao Yu and colleagues, “Evaluation of Retrieval-Augmented Generation: A Survey”](https://arxiv.org/html/2405.07437v2)
organizes retrieval and generation targets, datasets, and metrics through its
June 2024 literature cutoff. A survey maps the field; it does not validate one
metric or prove that RAG reduces hallucination in every setting.

## Build a useful golden query record

Each labelled case should include:

- user/task and tenant/access context;
- query and important variants;
- answerable, unanswerable, or ambiguous status;
- relevant source IDs and graded relevance;
- required evidence nuggets or subclaims;
- authoritative and disallowed sources;
- effective time and corpus snapshot;
- expected conflicts or multiple acceptable answers;
- consequence and slice labels;
- human label provenance and disagreement.

One “gold document” is often insufficient. A compliance answer might require
two clauses and a current exception. Recall should reflect all necessary
evidence.

Include realistic negatives: similar product names, stale versions, unauthorized
documents, adversarial content, and a corpus containing no answer.

## Classical retrieval metrics

For the first *k* results:

```text
Precision@k = relevant retrieved / k
Recall@k    = relevant retrieved / all relevant
```

- **Precision@k** captures context noise.
- **Recall@k** captures missed evidence.
- **MRR** emphasizes the reciprocal rank of the first relevant result.
- **MAP** accounts for multiple relevant items across ranks.
- **NDCG** supports graded relevance and discounts lower ranks.

[Pinecone, “RAG Evaluation: Don’t let customers tell you first”](https://www.pinecone.io/learn/series/vector-databases-in-production-for-busy-engineers/rag-evaluation/)
provides accessible definitions and examples. It is vendor education without
an independent comparison. Choose a metric from the task’s harm:

- one navigational answer may care about MRR;
- multi-evidence research may prioritize Recall@k and NDCG;
- a tight context budget makes Precision@k important.

Do not compare a reranker’s NDCG gain without its latency and cost.

## Evidence sufficiency

Relevance is not enough. A paragraph can be topically relevant while omitting
the fact needed to answer.

Represent the expected answer as evidence nuggets or sub-narratives. Measure
which are covered by the retrieved set. For a query with three required facts,
retrieving only one highly relevant document is insufficient even if
Precision@1 is perfect.

The
[TREC 2025 RAG Track overview by Shivani Upadhyay and colleagues](https://arxiv.org/html/2603.09891v1)
offers a rigorous current protocol: separate retrieval, generation
completeness, and citation support; decompose narratives into information
nuggets; use human assessment; and compare automatic judgments carefully. Its
web-search corpus and deep-research tasks do not directly represent
tenant-scoped enterprise retrieval, but its decomposition transfers well.

## Claim support

Split the answer into externally verifiable claims. For each claim:

1. identify its cited or supplied evidence;
2. classify full, partial, contradictory, or no support;
3. check whether the claim adds details absent from evidence;
4. preserve the **entailment** rationale—whether the evidence logically
   supports the claim—and reviewer identity.

This measures faithfulness to evidence, not whether the source itself is true.
Authority and source correctness are separate fields.

Use deterministic checks for citation syntax and resolvable IDs. Use trained
humans or calibrated semantic judges for entailment. Sample disagreements and
high-consequence claims for expert review.

## Citation attribution is stricter than topical support

A source may support a sentence but still be a poor citation if it copied an
original study, lacks authority, or only loosely matches the intended claim.

The browser-acquired text-layer paper
[Yee Man Choi and colleagues, “CiteGuard: Faithful Citation Attribution for LLMs via Retrieval-Augmented Validation”](https://arxiv.org/html/2510.17853v3)
treats citation as a search-and-attribution task rather than a binary judgment
over one supplied reference. On its CiteME benchmark, the best reported system
approaches reported human aggregate performance but remains wrong in roughly
one third of cases. The datasets are mainly scholarly and cross-domain samples
are small; do not transfer the percentage to enterprise documents.

The lesson is not “use CiteGuard.” It is that plausible citations require
verification, alternative valid sources can exist, and aggregate near-human
performance is not claim-level trust.

## Freeze one stage to test another

Use controlled experiments:

- **retriever test:** hold corpus/query labels fixed; compare candidate sets;
- **reranker test:** give identical candidates; compare ordering;
- **generator test:** give identical evidence; compare answers;
- **citation test:** give identical claims/sources; compare attribution;
- **pipeline test:** replay the whole versioned system.

Version parser, chunker, embedding, index snapshot, filters, retrieval
parameters, reranker, prompt, model, and judge. Without that lineage, a score
change cannot be explained.

## Automatic judges are measurement instruments

Validate an LLM judge against human labels on the task:

- agreement beyond chance;
- false support on adversarial and contradictory evidence;
- sensitivity to source order and answer verbosity;
- consistency across repeats;
- performance by domain, length, and consequence;
- drift after endpoint or prompt changes.

Do not ask the same model to generate an answer, select its evidence, and be
the only judge of its own grounding.

TREC reports that automatic judgments can be more stable in aggregate than on
individual narratives. Use them for scalable monitoring with manual
calibration, not as a magic ground truth.

## Online evaluation

Offline labels cannot cover changing sources and user intent. Add:

- no-result and low-score query rates;
- authorized candidate count;
- source/index staleness;
- citation click and source-open behavior;
- user correction, reformulation, and escalation;
- sampled expert claim-support review;
- incidents involving stale, forbidden, or missing evidence;
- business/task completion.

Clicks are ambiguous: a user may open a citation because the answer looks
wrong. Combine signals rather than optimizing one proxy.

## Worked evaluation: technical support RAG

Create slices for:

- exact error codes;
- conceptual symptoms;
- multi-document fixes;
- product/version conflicts;
- obsolete pages;
- unauthorized internal runbooks;
- unanswerable questions;
- malicious instructions inside documents.

For every index or model change:

1. gate ACL and deletion cases deterministically;
2. require retrieval recall floors on critical evidence;
3. compare precision/noise and reranking cost;
4. score answer correctness and abstention;
5. audit claim support and citation attribution;
6. shadow on recent traffic;
7. sample online failures into the golden set.

## Interview checkpoint

**Question:** “How would you evaluate a RAG system?”

A strong answer separates retrieval relevance, evidence sufficiency, answer
correctness, claim support, citation attribution, and product outcome. It
describes a versioned, stratified golden set; classical ranking metrics chosen
by harm; stage-freezing experiments; judge calibration; ACL/freshness cases;
and online feedback.

**Explain it back:** Give an example where Recall@k is perfect and the answer
is still unsafe.

## Capstone increment

Use the canonical [capstone fixture](lab-fixture.md) rather than creating a
second disconnected dataset. Start with its retrieval-relevant `e-01` through
`e-07` rows, then parameterize mutations for exact lookup, multi-document
evidence, stale source, unauthorized source, conflicting sources, unanswerable
requests, deletion, paraphrase, citation mismatch, and malicious document
text. Retain the same required and forbidden evidence IDs, answerability, and
consequence fields so later integrated cases remain joinable.

Run the Chapter 13 pipeline and calculate at least Recall@k plus claim-support
and citation-attribution outcomes. **Definition of done:** a failed answer can
be located at retrieval, evidence, generation, or citation rather than hidden
inside one RAG score.

Next: [Evaluation systems](15-evaluation-systems.md) expands the same
measurement discipline beyond retrieval into prompts, models, tools, agents,
and releases.
