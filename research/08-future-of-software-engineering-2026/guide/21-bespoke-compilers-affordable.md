# 21. Have bespoke compilers become affordable?

AI agents have plausibly made compiler prototypes, transliterators, and reverse-engineering experiments cheaper to attempt. The audited evidence does **not** establish that production-grade bespoke compilers or formal-method systems are now affordable for an average team.

That distinction matters because “it generated a compiler” can mean anything from translating a supported subset and passing a few examples to sustaining a language implementation with a documented grammar, runtime, debugger, interoperability layer, conformance suite, performance envelope, release process, and maintainers.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) gives striking anonymous examples: a TypeScript-to-.NET CLR compiler in four days, a COBOL compiler passing a NIST suite in three days for about $5,000 in tokens, and reverse engineering of an encrypted 1994-era binary format. These are valuable leads from a Chatham House event. No named repository, builder, supported-language definition, test manifest, labor record, or reproduction was located in the audited corpus. The duration and token-cost numbers therefore remain unverified.

## A plain-language model: the demo is the down payment

The cost of a bespoke language tool is not merely the cost of producing its source code:

> total cost = construction + validation + integration + human review + operation + maintenance + failure risk

Agents may sharply reduce **construction**, especially for parsers, boilerplate transformations, test generation, and experiments. But a lower first term does not settle the total. Compiler correctness is unusually demanding: one wrong transformation can remain syntactically valid, run successfully, and silently compute a different answer.

Affordability also depends on the claim’s unit. A one-off transliterator used on a frozen corpus is different from a compiler that must accept evolving programs. Reverse engineering enough of a file format to recover selected records is different from specifying every version and corruption mode. Adding an agent to an existing formal-verification workflow is different from creating proofs that cover a production system.

The useful question is therefore not “can an agent build it?” It is “what supported surface can the team validate and sustain, at what total cost, relative to the next-best migration path?”

## What adjacent evidence shows

Several audited studies demonstrate real technical leverage, but none reproduces the retreat’s examples.

A 2026 paper on [multi-semantic code translation](https://arxiv.org/html/2606.11863v1) evaluated 164 HumanEval-X functions. Its method combined several semantic views and increased executable success relative to the authors’ baseline; reported improvements varied substantially by model, including a rise from 46.95 to 71.34 for one configuration and from 14.02 to 31.10 for another. This is direct empirical evidence that richer feedback can improve function-level translation. It is not compiler construction: the benchmark contains short functions, not whole language runtimes, build systems, data formats, or operating procedures. The result cannot be read as a productivity or cost estimate.

[AgentModernize](https://arxiv.org/html/2605.17535v1) tested three models on eight modernization scenarios of roughly 100–310 lines. Reported errors ranged from 8.1% to 19.4%; iterative feedback sometimes repaired failures and sometimes introduced regressions. API spending below $15 sounds attractive, but it prices a tiny synthetic experiment, not the labor and assurance needed for a durable tool. It is useful evidence that cheap generation and reliable transformation are separate variables.

The translation study [*Articulate but Wrong*](https://arxiv.org/html/2605.21537v1) supplies the strongest warning about semantics. Eleven models translated 60 Python 2 snippets, producing 1,980 calls. Semantic drift was much more common than benign syntactic change, and same-model self-review missed 31.7% of the observed drift cases. The examples were at most ten lines, so the failure rate is not an enterprise forecast. The mechanism is relevant: generated output can look persuasive while changing meaning.

At repository scale, [RepoRescue](https://arxiv.org/html/2607.01213v1) found that environment access materially helped agents repair Python projects and that different agents’ successes were complementary. Yet manual audit reduced the set of seemingly successful unmaintained projects: regressions and scenario failures survived inherited tests. This study concerns compatibility repair, not compilers, but it shows why “passes the suite” is only as strong as the suite and the scenario audit around it.

Microsoft’s [COBOL modernization practice account](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/) reports hallucination, loss of context coherence, and the need for deterministic testing in a small module exercise. It also notes that batch behavior, file I/O, job-control language, and service-level constraints can require redesign. Those are precisely the surfaces omitted when a compiler story is reduced to its parser and code generator.

Anthropic’s [COBOL modernization article](https://claude.com/blog/how-ai-helps-break-cost-barrier-cobol-modernization) argues that AI can shorten discovery and mapping and enable incremental, side-by-side modernization with human oversight. As a vendor source it is useful for the proposed mechanism, but it does not document the retreat’s NIST-suite compiler, three-day duration, or token bill.

## The failed verification trail is evidence too

The audit followed the NIST lead to an [Otterkit COBOL issue](https://github.com/otterkit/otterkit-cobol/issues/6). The issue proposes work on a conformance suite and discusses scope, exclusions, compile outcomes, and runtime outputs. It does not document a completed AI-built compiler or the retreat’s time and cost. The repository was archived in February 2024. It must not be promoted into corroboration.

This negative result illustrates why a named suite is not enough. “Passes NIST” needs at least the suite name and version, included and excluded modules, expected failures, compiler flags, runtime platform, pass rule, and retained output. Conformance may cover language behavior while excluding interoperability, performance, diagnostics, operational support, security, or real application compatibility.

The audit also found no primary evidence for the TypeScript-to-CLR story, the binary-format story, or the broader statement about formal verification. Formal methods are especially easy to blur: agents can generate candidate specifications or proof scripts, but proof validity, specification adequacy, solver trust, review effort, and maintenance remain separate obligations.

## Where the economics may really have changed

There is still a meaningful, bounded hypothesis. Agents lower the cost of exploring narrow transformations because they can rapidly draft parsers, adapters, tests, and instrumentation, then use compiler errors and executable feedback as a harness. This can make previously rejected experiments worth a small discovery budget.

The most plausible near-term cases have:

- a frozen or tightly bounded source language subset;
- a finite corpus the team can inventory;
- a runnable reference implementation or trustworthy expected outputs;
- strong differential and conformance tests;
- limited nonfunctional requirements;
- a one-time migration objective rather than an indefinite language ecosystem;
- humans who understand both semantic domains;
- an exit plan for the generated tool.

The economics weaken when the input language is dynamic or poorly specified, the runtime is unavailable, undefined behavior matters, proprietary integrations dominate, or the tool becomes a long-lived product. Generated code may lower the entry price while creating a maintenance obligation no one budgeted.

## The compiler affordability dossier

Before repeating an “AI built this compiler” claim, require a one-page dossier and a reproducible evidence bundle.

### Scope

- Named source and target languages, versions, runtime, and platform.
- Grammar and semantic features supported; explicit exclusions.
- One-off corpus migration or ongoing compiler product.
- Number, size, and representativeness of real programs exercised.

### Correctness

- Conformance suite identity, version, selection, expected failures, and raw results.
- Compile success, runtime success, exact output comparison, and error behavior reported separately.
- Differential tests against the old runtime and checks for data, side effects, precision, ordering, and concurrency.
- Independent or human-written oracle, not only same-model review.
- Security, performance, reliability, and interoperability gates.

### Economics

- Agent and model versions; prompts, tools, retries, and compute.
- Token/API spending, including failed attempts.
- Human hours by role: language expert, platform engineer, reviewer, tester, operator.
- Existing assets reused, including grammar files, libraries, tests, and prior prototypes.
- Integration, parallel-run, incident, and opportunity costs.
- Expected maintenance horizon, owner, and upgrade plan.

### Reproducibility

- Repository and commit, build instructions, environment lockfile, and license.
- Retained logs and generated artifacts.
- A second run by someone outside the original team.
- A test against unseen real programs.

Score each row **shown**, **partly shown**, or **not shown**. Do not calculate a return estimate until the correctness and ownership rows clear a pre-agreed threshold. For the retreat’s two compiler stories, most rows currently remain “not shown.”

## Evidence judgment

- **Prototype economics:** moderate confidence that agents reduce the cost and time of bounded experiments.
- **Production compiler economics:** low confidence; the decisive validation, integration, and maintenance costs were not measured in the evidence found.
- **Retreat quantities:** unverified. The four-day, three-day, $5,000, and NIST claims have no auditable primary artifact in this corpus.
- **Formal-method affordability:** open. No audited source tested the broad proposition.
- **Generalizability:** highest for finite, well-specified transformations with executable oracles; lowest for open-ended language ecosystems and poorly observed legacy semantics.

The responsible conclusion is exciting but narrower than the headline: agents may turn “not worth prototyping” into “worth a disciplined experiment.” Only a complete dossier can turn that experiment into evidence that a bespoke compiler is affordable.

Podcast hook: A three-day compiler sounds miraculous until the invoice includes the grammar’s missing corners, the human reviewers, the parallel run, and ten years of maintenance.

Continue reading: [Chapter 20, “Port first, improve second”](20-port-first-improve-second.md), explains the sequencing discipline these tools need; [Chapter 22](22-board-legible-modernization.md) keeps technical possibility separate from portfolio economics.
