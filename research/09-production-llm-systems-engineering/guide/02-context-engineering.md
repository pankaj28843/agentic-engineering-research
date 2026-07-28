# 2. Context engineering: build the model’s working set

Context engineering is the runtime discipline of assembling the smallest
high-signal working set that lets a model act correctly now. It covers more
than prompt wording: instructions, user input, history, retrieved facts, tool
definitions, memory, intermediate results, and the policy that includes,
orders, compresses, or removes each item.

For a full-stack engineer, the nearest analogy is a query planner plus a
process working set. You would not load an entire data lake into one SQL query
or keep every heap object resident forever. A context assembler should be just
as selective.

## ELI5: pack a workbench, not a warehouse

A technician repairing a bicycle needs the correct manual page, the customer’s
symptom, a few tools, and the bike in front of them. Moving the entire
warehouse onto the workbench creates more searching, not more capability.

An LLM’s context window is that workbench. A larger bench helps, but irrelevant
parts can still hide the one washer that matters. Context engineering decides
what arrives, when it arrives, how it is labelled, and what leaves.

A **token** is the model's text unit, often a word fragment. A **context
window** is the maximum token working set available to one call. Where the
query-planner analogy breaks: context selection changes probabilistic model
behaviour; unlike a database plan, it cannot guarantee that selected evidence
will be used correctly.

[Anthropic, “Effective context engineering for AI agents”](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
states the governing heuristic clearly: seek the smallest set of high-signal
tokens that maximizes the chance of the desired result. It also describes
compaction, structured notes, just-in-time retrieval, and subagents for
long-horizon work. These are useful production patterns from a model vendor;
they are not evidence that one provider’s implementation is universally best.

## The context supply chain

Treat every context item as data with provenance:

```text
sources → candidates → policy/filter → ordering → token budget
        → model call → observation → next-turn context
```

Typical sources are:

- stable system and safety instructions;
- the current user request and product state;
- conversation turns and tool results;
- retrieved documents, code, database rows, or API objects;
- tool names, schemas, examples, and permission hints;
- short-term scratch state and durable memory;
- summaries or checkpoints from earlier work.

For each source, record four properties: **owner**, **freshness**, **trust
level**, and **tenant scope**. A retrieved web page is untrusted content, even
if it appears beside system instructions. A user preference may persist, but
not across users. A tool result can be authoritative at time *t* and stale at
time *t + 10 minutes*.

## Prompt engineering still matters

Prompt engineering defines how intent and constraints are expressed inside the
working set. Context engineering designs the system that produces the whole
working set.

The practical test is:

- **rewording** an instruction is mainly prompt engineering;
- **rewiring** retrieval, memory, ordering, filtering, or tool exposure is
  context engineering.

[Sourcegraph, “Context Engineering: A Practical Guide for AI Agents (2026)”](https://sourcegraph.com/blog/context-engineering)
uses the example of a coding agent drowning in broad repository search. Its
own benchmark numbers support Sourcegraph’s product and workload, so do not
generalize them blindly. The mechanism is credible: retrieval quality changes
which evidence the model can reason over, while raw context capacity does not
guarantee that the decisive file is present or salient.

## A six-layer assembly model

### Layer 1: invariant policy

Include the stable rules that genuinely apply to every call: identity,
authority boundaries, privacy constraints, and conflict resolution. Keep them
short, non-contradictory, and mechanically testable where possible.

### Layer 2: current task contract

State the requested outcome, scope, acceptance evidence, and stop conditions.
Separate facts from assumptions. A task contract should survive compaction
without changing meaning.

### Layer 3: situation state

Supply current application objects, user-visible state, and recent actions.
Prefer structured records with stable identifiers over prose transcripts.
Mark timestamps and versions.

### Layer 4: retrieved knowledge

Fetch on demand. Combine lexical, semantic, graph, SQL, or filesystem
retrieval as the domain requires. Deduplicate, rank, and preserve citations.
Do not let retrieved text impersonate system policy.

### Layer 5: tool surface

Expose only tools relevant to the current state and authority. Descriptions,
argument schemas, examples, and failure semantics all consume tokens; lazy
tool discovery can reduce noise, but it must not hide a required recovery
tool.

### Layer 6: working memory

Retain decisions, unresolved questions, and compact observations. Raw tool
output is usually poor memory. Store a reference plus the finding, then reload
the source if precision becomes necessary.

[LangChain, “Context Engineering”](https://www.langchain.com/blog/context-engineering-for-agents)
organizes related operations around writing, selecting, compressing, and
isolating context. Use that taxonomy as design vocabulary, not as a
requirement to adopt its framework.

## Compaction is lossy state migration

When a conversation exceeds its useful window, a summarizer migrates state
from a large representation into a small one. This resembles a database
migration with information loss.

A safe compaction record preserves:

- the goal and current definition of done;
- decisions plus their reasons;
- exact identifiers, versions, and paths;
- completed evidence and failed attempts;
- unresolved risks and the next action;
- authority limits and commitments made to a user.

Do not summarize secrets into a less protected store. Do not replace exact
error text or hashes when later verification depends on them. For critical
facts, keep references to immutable artifacts.

Test compaction by replay: give a fresh worker the compacted state and ask it
to continue. Compare decisions, duplicated work, policy violations, and task
completion with an uncompacted baseline.

## Long context is capacity, not relevance

Two different limits are easy to confuse:

1. **hard capacity:** the provider rejects or truncates a request beyond its
   token limit;
2. **effective attention:** the model fails to use a relevant fact even though
   it is technically present.

Anthropic’s article points to “context rot,” where recall can degrade as more
tokens enter the window. The exact degradation depends on model, location,
task, and distractors. Therefore, do not adopt a universal “safe token count.”
Build a local eval with your document shapes and important facts.

## Failure taxonomy

When a context-dependent task fails, classify the path:

| Failure | Diagnostic question | Likely intervention |
| --- | --- | --- |
| Missing | Was the necessary fact ever included? | Improve discovery or retrieval recall |
| Buried | Was it present but surrounded by noise? | Rerank, trim, or reorder |
| Stale | Was the selected fact obsolete? | Add version/freshness policy |
| Conflicting | Did two sources disagree without precedence? | Label authority and resolve conflicts |
| Poisoned | Did untrusted content alter instructions? | Separate data from policy; constrain effects |
| Cross-tenant | Did state come from another user? | Partition storage, cache keys, and traces |
| Compacted away | Did a summary drop a decision? | Strengthen the checkpoint schema |
| Tool overload | Were irrelevant contracts consuming attention? | Retrieve tools just in time |

“The model hallucinated” is an observation, not a root cause.

## Worked example: support agent for a subscription product

A user asks, “Why was I charged after cancelling?”

A poor assembler sends the entire conversation, a generic policy manual, fifty
tool definitions, and semantically similar support tickets. A better one:

1. binds the authenticated tenant and user;
2. retrieves the exact subscription, cancellation event, invoice, and payment
   attempt by stable ID;
3. loads the version of the cancellation policy effective on the event date;
4. exposes read-only billing tools first;
5. labels customer text and historic tickets as untrusted;
6. reserves context for evidence and a concise response;
7. requires a citation to each account fact;
8. exposes a refund proposal tool only if policy and authorization allow it.

If a record is missing, the correct degraded response is “I cannot verify this
yet,” not a plausible reconstruction.

## Instrument the assembler

For each model call, capture privacy-safe metadata:

- source IDs and versions selected;
- token count by context class;
- retrieval rank and score;
- items dropped and why;
- compaction generation;
- tool contracts exposed;
- cache eligibility;
- the output’s citations or claimed dependencies.

This makes it possible to ask whether a regression came from a model release,
retrieval change, stale memory, altered ordering, or prompt edit.

## Interview checkpoint

**Question:** “The model supports 1 million tokens. Why not include
everything?”

A strong answer separates capacity from utility. More context raises input
cost and prefill latency, can introduce irrelevant or conflicting evidence,
increases the prompt-injection surface, and makes provenance harder. The right
amount is empirically determined by task success, not the advertised maximum.
Use retrieval, compaction, external state, and replayable evals.

**Explain it back:** In your current system, which context elements are policy,
which are trusted data, and which are untrusted content?

## Field exercise

Take one production prompt and annotate every token block with source, owner,
freshness, trust, tenant, and reason for inclusion. Remove one low-signal block
at a time and replay a small **saved smoke set** of representative examples
with simple required and forbidden facts. Chapter 15 turns this provisional
set into a versioned, stratified golden set with release gates. For now, the
result is the beginning of a context budget, not merely a shorter prompt.

## Capstone increment

Turn that annotation into the assistant's context inventory. For every policy,
user input, retrieved chunk, conversation item, tool contract, and memory
record, capture provenance, owner, trust, tenant, freshness, token cost, and
inclusion reason. Reuse Chapter 1's control-loop diagram to show where the
assembler runs.

**Definition of done:** a replay report shows what was included and dropped,
why, and whether the representative examples still pass.

Next: [Prompt caching versus semantic caching](03-prompt-vs-semantic-caching.md)
shows why two optimizations with the word “cache” have different values,
invalidation rules, and security risks.
