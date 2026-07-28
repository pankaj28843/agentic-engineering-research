# 20. Adaptation choices: prompt, retrieve, tune, or distil?

When an AI feature fails, teams often jump to a technique: “add RAG” or “fine-
tune it.” Start with the gap.

- Does the system lack current or private **knowledge**?
- Does it display the wrong stable **behaviour**?
- Does it need examples only for this request or tenant?
- Is a capable system too slow or expensive to run repeatedly?

Prompting, in-context learning, retrieval, fine-tuning, and distillation change
different parts of the system. They can be combined, but each adds a lifecycle
you must own.

## ELI5: instruction, open book, coaching, or apprentice

Suppose a skilled employee makes a mistake.

- Give a clearer instruction: **prompting**.
- Put worked examples on the desk: **in-context learning**.
- Let them consult the current handbook: **RAG**.
- Repeatedly coach a durable habit: **fine-tuning**.
- Ask them to turn a thick example binder into a study card: **context
  distillation**.
- Train a cheaper apprentice from an expert's demonstrations: **model
  distillation**.

You would not rebuild the employee's memory to update today's train timetable.
You would not hand them a new handbook if the problem is consistently using
the wrong response format.

Where the analogy breaks: the employee does not model cognition. Fine-tuning
statistically updates weights; ICL supplies request-time examples; RAG supplies
selected external evidence; and distillation creates a separately governed
artifact.

## Establish the baseline before adapting

Create a versioned evaluation set with:

- representative ordinary cases;
- the failure slice that motivated the change;
- hard and ambiguous cases;
- current/private-knowledge cases;
- refusal, authorization, and deletion cases;
- latency, cost, and reliability budgets.

Record the base model, prompt, decoding settings, tools, corpus, and judge or
human rubric. Keep a holdout. Without this baseline, each technique becomes a
demo rather than a decision.

Start with the least irreversible intervention that can test the hypothesis.
[TMLS Research, “Fine-tune vs RAG vs
Prompt”](https://www.tmls.nyc/research/finetune-vs-rag-vs-prompt)
frames the useful diagnosis as knowledge gap versus behaviour gap and recommends
prompting first with a held-out gate. It is a secondary synthesis whose author
and publication date were not visible in the capture, so its exact performance
claims are not primary evidence.

## Prompting: change the request contract

Prompting is appropriate when the model already has the capability and needs:

- a clearer task and audience;
- explicit constraints or acceptance criteria;
- decomposition or a checklist;
- a few stable output examples;
- tool and refusal instructions;
- a structured response contract.

Advantages:

- fast and reversible;
- no training pipeline;
- easy A/B comparison;
- can remain provider-portable.

Failure modes:

- brittle wording dependencies;
- prompt growth and context competition;
- hidden interactions with retrieved content;
- model-version regressions;
- no reliable way to inject changing private facts from nowhere.

Treat prompts as versioned code with tests, not incantations. A longer prompt is
not automatically a better specification; remove clauses that do not change
measured behaviour.

## In-context learning: adapt inside one request

In-context learning (ICL) supplies examples or demonstrations without changing
weights. It is useful when behaviour varies by task, tenant, language, or
session and examples can be selected at runtime.

Common forms:

- zero-shot instruction;
- fixed few-shot examples;
- retrieved examples similar to the current case;
- many-shot long-context demonstrations;
- summaries or rules distilled from many examples.

ICL is attractive because examples remain inspectable, replaceable, and
permission-scoped. Costs include repeated input tokens, longer prefill, context
crowding, example-order sensitivity, and leakage if examples cross tenant
boundaries.

Example selection is a retrieval problem. Measure whether similarity actually
predicts helpfulness; a superficially similar example may encode the wrong
policy or label boundary.

## RAG: keep changing knowledge outside the weights

Retrieval-augmented generation fits information that is:

- current or frequently updated;
- private or tenant-scoped;
- too broad to fit reliably in a prompt;
- attributable to a source;
- subject to permission, retention, correction, or deletion.

RAG keeps evidence inspectable and allows a source to be updated without
training. It also introduces parsing, chunking, indexing, retrieval,
reranking, authorization, citation, cache, and deletion failure modes.

[Zhuoyi Yang, Yurun Song, Iftekhar Ahmed, and Ian Harris, “Fine-Tuning vs. RAG
for Multi-Hop Question Answering with Novel
Knowledge”](https://arxiv.org/html/2601.07054v1)
compares continual pretraining, supervised fine-tuning, and RAG across three
open 7B models on QASC and more than 10,000 questions based on 2024 Wikipedia
events. RAG more than doubled multiple-choice accuracy on the novel-event set
in the tested setup, while supervised fine-tuning achieved the best overall
result across the authors' conditions. Three models and multiple-choice tasks
do not create a universal ranking; they illustrate that the answer depends on
whether the information is novel and what behaviour the training changes.

Use [Chapter 13](13-rag-architecture.md) and
[Chapter 14](14-retrieval-evaluation.md) to test retrieval separately from
answer generation.

## Fine-tuning: move a stable behaviour into weights

Fine-tuning can be a good fit for:

- consistent style, format, or classification boundaries;
- specialized task behaviour underrepresented in the base model;
- repeated tool-use patterns;
- stable domain language;
- moving strong-model behaviour into a smaller model;
- high-volume workloads where repeated examples are costly.

It is a poor first move when the real issue is a broken tool, missing
authorization filter, stale corpus, or current fact.

Fine-tuning creates new ownership:

- licensed and permissioned training data;
- deduplication, contamination, and train/validation split;
- training configuration and base-model version;
- artifact registry and reproducible lineage;
- broad capability and safety regressions;
- serving compatibility and rollback;
- data removal and retraining strategy;
- drift as the world or policy changes.

Parameter-efficient methods such as **LoRA** (train small low-rank adapter
matrices) and **QLoRA** (train adapters while the base model is quantized)
reduce trainable parameters and memory needs. They do not eliminate data
governance, evaluation, deployment, or forgetting risks.

[Meta AI, “To fine-tune or not to
fine-tune”](https://ai.meta.com/blog/when-to-fine-tune-llms-vs-other-techniques/)
positions ICL before tuning, retrieval for dynamic/reference-heavy knowledge,
and tuning for stable style, format, edge skills, and smaller-model economics.
It is vendor guidance with an incentive toward open-model adoption, not a
controlled head-to-head study.

## Distillation has two useful meanings

### Model distillation

A teacher model produces labels, rationales, preferences, or trajectories used
to train a smaller student. The goal may be lower latency and cost, local
deployment, or a specialised behaviour.

The student must be evaluated independently. It can imitate teacher mistakes,
lose rare capabilities, overfit synthetic phrasing, or fail outside the
teacher-generated distribution. Retain human-authored and difficult holdouts;
do not use the teacher as the only judge of its student.

See [Chapter 7](07-speculative-decoding-quantization-distillation.md) for the
distinction between changing the model, compressing numeric representation,
and changing the decoding algorithm.

### Context distillation

A capable model turns many demonstrations into a compact textual artifact—a
rule sheet, taxonomy, or “cheat sheet”—that is reused as context. The model
weights do not change, and the artifact remains inspectable and editable.

[Ukyo Honda, Soichiro Murakami, and Peinan Zhang, “Distilling Many-Shot
In-Context Learning into a Cheat
Sheet”](https://arxiv.org/html/2509.20820v1)
selects eight BIG-Bench Hard tasks where many-shot prompting had already beaten
eight-shot prompting. With mostly 150 demonstrations and 100 test items per
task, the compact cheat-sheet condition beats few-shot prompting on seven of
eight selected tasks and is competitive with several many-shot or retrieved-
example conditions. The selection criterion favours tasks where many-shot was
already useful, and eight benchmark tasks on proprietary models are not a
production guarantee.

Context distillation is worth testing when:

- a long stable example set repeatedly consumes context;
- the distilled rules can be reviewed and versioned;
- exact examples need not be reproduced;
- a fallback can retrieve originals for uncertain cases.

## A decision matrix

| Need | First candidate | Main strength | Main new failure |
|---|---|---|---|
| clarify task/format | prompt | cheapest reversible test | brittle or bloated instructions |
| adapt per request/tenant | ICL | inspectable runtime examples | context cost and example leakage |
| current/private/attributable facts | RAG | update, access, cite, delete | retrieval and corpus lifecycle |
| stable repeated behaviour | fine-tune | behaviour in weights | data/training/regression lifecycle |
| compress many stable examples | context distillation | short inspectable artifact | summary omits important exceptions |
| cheaper specialised model | model distillation | lower serving cost/latency | student loses tail capability |

This table selects a hypothesis, not a winner. Run it through the same held-out
quality and operational gate.

## Hybrid systems are often the honest answer

Useful combinations include:

- tuned small model for stable classification + retrieval for current policy;
- prompt contract + tenant-scoped retrieved examples;
- strong teacher creates training data + student retrieves source evidence;
- distilled cheat sheet for common rules + RAG fallback for detailed cases;
- tuned router + several unchanged specialist models;
- retrieval + fine-tuned citation or tool-use behaviour.

Keep the layers independently replaceable and observable. If a hybrid improves,
use ablations to learn which component caused the gain. Otherwise the system
accrues cost without knowledge.

## Governance changes the technical choice

Ask before moving information:

- Can the data be used for training?
- Must an individual record be corrected or deleted?
- Is access different by tenant or role?
- Must the answer cite a current authority?
- Can the model artifact leave a region?
- Could the training process memorize secrets?
- How quickly must a policy change take effect?

RAG often makes per-record access, provenance, and deletion more tractable.
Fine-tuning may be suitable for behaviour learned from properly governed data,
but weights are not a convenient record-level database. ICL can preserve
tenant-specific adaptation if examples are selected inside an authorization
boundary.

## Compare total system outcomes

For each candidate, measure:

- quality by task, consequence, and tail slice;
- retrieval recall and citation correctness where applicable;
- time to first token and end-to-end latency;
- input/output tokens and cost per accepted outcome;
- storage, training, indexing, and operational labour;
- update and rollback time;
- authorization, deletion, and privacy tests;
- robustness to model, corpus, and traffic drift.

Do not compare RAG token cost with fine-tuning training cost once and stop.
Model recurring inference, index maintenance, retraining cadence, evals, and
incident response over the expected product life.

## An escalation ladder

1. Reproduce and classify the failure.
2. Fix deterministic software, data, or tool defects first.
3. Establish a prompt-only baseline.
4. Add a few reviewed examples if behaviour is contextual.
5. Add retrieval if the missing evidence is external and governed.
6. Distil long demonstrations if their repeated cost is the bottleneck.
7. Fine-tune only for a measured, stable behaviour or economics gap.
8. Distil a student if a capable teacher meets quality but violates the serving
   envelope.
9. Keep the simpler baseline for rollback and compare continuously.

An intervention may legitimately start later in the ladder when constraints
are already proven. The discipline is to write down the evidence.

## Worked example: regulated support assistant

The assistant needs current policy, a mandated response template, and low
latency.

- A prompt specifies the template and refusal rules.
- Tenant- and role-scoped RAG supplies current policy with citations.
- Evals show that the base model repeatedly mishandles one stable structured
  workflow.
- Permissioned examples fine-tune a smaller model for that workflow.
- The tuned model still retrieves policy rather than memorizing it.
- Complex or low-confidence cases route to a stronger model or human.

The team can update policy immediately, inspect citations, and roll back the
adapter independently. “Fine-tune versus RAG” was the wrong product question.

## Field exercise: write an adaptation ADR

For one measured failure, document:

- knowledge gap, behaviour gap, or systems defect;
- simplest baseline;
- candidates and rejected alternatives;
- data and governance requirements;
- held-out quality and safety slices;
- lifecycle and rollback;
- latency and cost per accepted outcome;
- the threshold that justifies added complexity.

Then state what new failure surface your chosen technique introduces.

## Interview checkpoint

**Question:** “When would you use prompt engineering, RAG, fine-tuning, or
distillation?”

A strong answer diagnoses the gap first. It uses prompting for clear reversible
behaviour changes, ICL for request-scoped examples, RAG for current/private/
attributable and deletable knowledge, fine-tuning for stable repeated
behaviour, context distillation to compress demonstrations, and model
distillation to move capability into a cheaper student. It proposes a hybrid
when knowledge and behaviour differ, all behind one evaluation and governance
gate.

**Explain it back:** Why is fine-tuning a model on this week's policy documents
usually less governable than retrieving them?

## Capstone increment

Turn the field exercise into an adaptation ADR for one failure measured by the
Chapter 15 evaluation and located in a Chapter 16 trace. Compare prompt,
request-time examples, RAG, fine-tuning, context distillation, model
distillation, and a systems fix; reject candidates that target the wrong gap.

**Definition of done:** the ADR chooses the least irreversible intervention
that crosses a stated acceptance threshold, owns its data/artifact lifecycle,
and has an evaluated rollback.

Next: [Full-stack trade-offs](21-full-stack-tradeoffs.md) measures whether the
chosen system works within real latency, quality, cost, and reliability limits.
