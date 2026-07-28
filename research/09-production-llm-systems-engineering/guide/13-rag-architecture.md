# 13. RAG architecture: retrieval is a data product

Retrieval-augmented generation (RAG) gives a model selected external evidence
at inference time. The visible answer is the final stage of a longer data
system:

```text
sources → parse → normalize → chunk → enrich → index
query → authorize → retrieve → fuse → rerank → assemble
      → generate → validate → cite
```

Failures introduced before generation cannot reliably be repaired by a clever
prompt. Production RAG is source synchronization, search engineering,
authorization, evaluation, and lifecycle management with an LLM attached.

## ELI5: a librarian and a writer

A writer answers questions using a library.

If books arrive late, pages are shuffled, shelves mix public and private
collections, or the catalogue points to discarded editions, the writer gets
bad evidence. A brilliant writer can make that bad evidence sound polished,
which is worse than an obvious failure.

RAG engineering first makes the library trustworthy, then makes retrieval
measurable, then constrains the writer to the evidence.

## The ingestion plane

### Source identity and change capture

Each source needs a stable identity, owner, authority class, tenant/access
scope, effective time, version, and content hash. A connector should record
create, update, and delete events, not merely append embeddings.

A deletion tombstone must propagate through parsed artifacts, chunks, indexes,
caches, and generated-answer dependencies. Otherwise “right to delete” and
ordinary document removal become stale-answer bugs.

### Parsing and normalization

Parsing is semantic work. Preserve headings, reading order, lists, tables,
code, captions, page/section location, and links. Flattening a two-column PDF
or merging table cells corrupts facts before retrieval begins.

[Unstructured, “RAG Pipeline Challenges: From Data Ingestion to Retrieval”](https://unstructured.io/insights/rag-pipeline-challenges-from-data-ingestion-to-retrieval)
provides a strong operational taxonomy for parsing, chunking, stable IDs,
versions, hybrid retrieval, and observability. Unstructured sells ingestion
infrastructure, so its claim that failures concentrate upstream is vendor
experience rather than a population statistic. The described failure modes
are nevertheless concrete and testable.

### Chunking

A chunk is the unit that can be found and placed in context. There is no
universal size.

Trade-offs:

- small chunks improve specificity but can lose definitions and relations;
- large chunks preserve context but add noise and token cost;
- fixed character boundaries are simple and can split tables or procedures;
- structural chunks preserve documents but vary greatly in size;
- semantic chunks depend on a model and threshold that must be versioned.

Useful patterns include parent-child retrieval, small searchable chunks with a
larger display context, overlap for boundary continuity, and special handling
for tables/code. Preserve deterministic `(document, version, location,
chunker_version)` identity.

### Enrichment and indexing

Store metadata needed for both relevance and policy: title, section, time,
language, entity, product/version, authority, tenant, and ACL. Embeddings are
one index, not the source of truth. Keep original content and exact
provenance.

Changing an embedding model creates a new index generation. Support dual-read
or shadow comparison during migration and reconcile coverage before deleting
the old generation.

## Search vocabulary for application engineers

- **Lexical/BM25:** ranks exact and weighted terms; useful for identifiers and
  phrases.
- **Embedding/vector:** represents items numerically and searches for
  similarity; nearness does not imply truth, authority, or access.
- **Hybrid:** obtains candidates from multiple channels.
- **Fusion:** combines those candidate lists.
- **Reranker/cross-encoder:** a slower second-stage scorer that examines a
  query and candidate together.
- **Top-k:** the first `k` returned candidates.
- **Recall:** the share of required evidence that the candidate stage found.

These are pipeline roles, not a maturity ladder. An SQL lookup can be the right
retriever, and access control must constrain every candidate channel.

## The query plane

### Intent and decomposition

Normalize the question without erasing meaningful identifiers, negation,
units, or dates. Complex questions may require subqueries, but decomposition
can lose constraints. Preserve lineage from the original request to every
retrieval operation.

### Authorization before retrieval

Bind the authenticated principal and tenant at query time. Every candidate
channel—lexical, vector, graph, SQL, or federated search—must be
authorization-constrained before ranking and top-*k* inside a trusted
enforcement boundary. A later application filter is defense in depth, not a
substitute: it cannot restore authorized recall after forbidden candidates
consume the fixed budget, nor can it authorize retrieval-service caches, logs,
scores, counts, timing, or telemetry. The
[OWASP Foundation, “Retrieval-Augmented Generation (RAG) Security Cheat
Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html)
recommends per-chunk access metadata, retrieval-time enforcement, and tenant
isolation; treat its implementation patterns as a security baseline, not an
empirical guarantee.

Do not place confidential chunks in the prompt and ask the model not to
mention them.

### Choose retrieval by information shape

- **SQL/structured query:** live exact facts, joins, ranges, aggregations.
- **Lexical/BM25:** identifiers, names, error codes, exact phrases.
- **Dense/vector:** paraphrase and conceptual similarity.
- **Graph traversal:** explicit relationships and constrained paths.
- **Hybrid:** complementary candidate channels combined, often followed by
  reranking.

[Oracle Developers, “Production RAG Evaluation: Keyword, Vector, SQL, or Hybrid Search?”](https://blogs.oracle.com/developers/production-rag-evaluation-keyword-vector-sql-or-hybrid-search)
correctly emphasizes matching retrieval to data shape and evaluating it
separately. It supplies no independent effect sizes, and its placeholder
notebook numbers should not be treated as results.

Hybrid search is not automatically better. If channels return the same noise,
fusion adds latency and complexity. Reciprocal rank fusion can combine ranks
without comparable raw scores, but its parameters and candidate depths still
need evaluation.

### Reranking and evidence sufficiency

A cross-encoder or model reranker can examine query-document pairs more deeply
than the first-stage retriever. Rerank only a bounded candidate set and record
both original and final ranks.

Do not stop at “top five returned.” Ask whether the evidence set is sufficient:
does it cover every subquestion, required authority, date, and conflicting
source? Sometimes the right result is `insufficient_evidence`.

## Context assembly and generation

The assembler should:

- deduplicate overlapping chunks;
- retain source IDs, versions, and locations;
- group related evidence without hiding disagreement;
- rank authoritative/current sources above merely similar ones;
- keep untrusted source text separate from system instructions;
- impose a token budget and explicit omission record;
- instruct the model to abstain when evidence is insufficient.

Generation can produce an answer plus claim-to-source mappings. A later
validator should check those mappings. Merely placing citations in the prompt
does not prove they support the attached claims.

The preprint
[Fariba Afrin Irany and Sampson Akwafuo, “A Hybrid Retrieval and Reranking Framework for Evidence-Grounded RAG” (arXiv:2605.01664)](https://arxiv.org/html/2605.01664v1)
demonstrates a hybrid, reranking, and claim-checking pipeline in a small
biomedical pilot. Its reported perfect grounding judgment covers 200 claims
judged by an LLM, without independent expert validation. Treat it as a worked
architecture, not evidence that hybrid RAG is solved.

## Freshness is observable state

For each source and index generation, track:

- last successful scan;
- source high-water mark;
- documents discovered, parsed, indexed, and deleted;
- failed/dead-letter records;
- parser, chunker, embedding, and index versions;
- end-to-end update lag;
- query-time index generation;
- answer dependencies.

An index being “up” says nothing about freshness. Set a staleness objective by
domain and expose it to both routing and UX.

## Ingestion as a resumable state machine

Community discussion in
[Hacker News, “RAG at scale: Synchronizing and ingesting billions of text embeddings”](https://news.ycombinator.com/item?id=37824547)
contains practitioner reports about checkpoints, observability, and component
trade-offs. It is anecdotal and dated, but the failure hypothesis is durable:
a billion-item synchronization job must resume safely after partial failure.

A record can move through:

```text
discovered → fetched → parsed → chunked → embedded → indexed → verified
                    ↘ quarantined
deleted_source → tombstoned → removed → verified_absent
```

Each transition is idempotent and keyed by source/version. Reconciliation
compares source inventory with the serving index.

## Worked example: internal policy assistant

The corpus contains HR policy, local legal addenda, and team handbooks.

1. Classify authority: global policy, country addendum, informal guide.
2. Preserve effective dates and supersession links.
3. Partition by employee entitlement and geography.
4. Parse sections/tables and chunk by policy clause.
5. Route exact policy codes to lexical search; concepts to hybrid retrieval.
6. Rerank with jurisdiction and current-date features.
7. Require evidence for every eligibility claim and surface conflicts.
8. Abstain and create an HR handoff when current authoritative evidence is
   missing.
9. Re-run deletion, freshness, and answerability evals on every index change.

The
[Lukas Walter and Elliot One comment thread on “Most RAG systems fail before the LLM even runs”](https://www.linkedin.com/posts/elliotone_most-rag-systems-fail-before-the-llm-even-activity-7475503003295232000-OMrU)
is retained only as current practitioner signal: the native capture contains
their comments discussing chunking, metadata, authorization, freshness, and
telemetry, but not the root post body. It neither confirms the title's claim
nor supports a prevalence claim.

## Interview checkpoint

**Question:** “Design a production RAG system.”

A strong answer covers source authority, change/delete propagation, structural
parsing, versioned chunk identity, retrieval chosen by data shape, ACLs before
context, hybrid/reranking only when evaluated, evidence sufficiency,
claim-level citations, independent stage metrics, freshness, replay, and
abstention.

**Explain it back:** Why can increasing `top_k` simultaneously improve
retrieval recall and reduce final-answer quality?

## Capstone increment

Draw the assistant's ingestion and query planes using stable source/version/
chunk identities, provenance, authority, tenant ACLs, index generation, and
answer dependencies. Implement or simulate five lifecycle cases: create,
update, delete, unauthorized query, and insufficient evidence.

The input is Chapter 2's context inventory; the output is a resumable state
machine plus serving-path diagram. **Definition of done:** a tombstoned source
becomes verifiably absent from retrieval and dependent caches, while an
unauthorized item never enters model context.

Next: [Retrieval evaluation](14-retrieval-evaluation.md) gives each stage a
separate scorecard so the team can locate—not merely notice—failure.
