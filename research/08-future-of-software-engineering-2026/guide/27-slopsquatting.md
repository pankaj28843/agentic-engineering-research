# 27. Slopsquatting and hallucinated dependencies

Package-name hallucination is real and measured. Targeted instructions can steer selected models toward a chosen nonexistent name in laboratory conditions. The audited evidence does **not** establish how often attackers publish those names, how often developers or agents install them, or whether slopsquatting has caused verified real-world compromise.

That narrower conclusion is still security-relevant. A repeated nonexistent name can create an opportunity for an attacker who registers it before a later user resolves the suggestion. But calling every hallucinated import an attack collapses possibility, preparation, exposure, and harm into one misleading statistic.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) describes malicious actors predicting hallucinated library names and publishing packages under them. This is an anonymous retreat warning, not an attributable incident report. The audit found strong evidence for the first stage and no completed chain to victim compromise.

## A plain-language model: seven links, not one event

Slopsquatting requires a sequence:

1. A model generates a package name that does not exist.
2. The same or a targetable name is likely to recur.
3. An attacker notices or predicts the name and registers it.
4. A developer or agent accepts the suggestion.
5. A package manager resolves and installs the attacker’s package.
6. Malicious behavior executes with useful access.
7. The action causes a verified security impact.

Evidence at link one cannot estimate link seven. Each link has a different denominator: generated references, unique names, registered names, accepted suggestions, installs, executions, and compromised victims.

Ordinary typosquatting starts from a human mistyping or confusing a name similar to a legitimate package. Slopsquatting starts from a model confidently proposing a nonexistent name. The attacker’s registration tactic may look similar, but the upstream predictor and prevention opportunities differ. The audited corpus does not provide a controlled prevalence comparison between the two.

## What the experiments show

The strongest Python/npm route is a USENIX `;login:` article by the study authors, [“We Have a Package for You!”](https://www.usenix.org/publications/loginonline/we-have-package-you-comprehensive-analysis-package-hallucinations-code). It summarizes peer-reviewed USENIX Security research that queried 16 models with roughly 19,000 prompts per model. The authors report a mean package-hallucination rate near 19.6%, 205,474 unique nonexistent names, and substantial recurrence across repeated trials. Tested commercial models hallucinated less often than open models.

Those values belong to the authors’ model versions, prompts, languages, and registry snapshots. The article tests whether generated package names existed; it does not publish malicious packages or observe installation, execution, or compromise. Once an attacker registers a name, a simple existence check can no longer classify it as hallucinated.

A separate Rust preprint, [“When LLMs Invent Rust Crates”](https://arxiv.org/html/2606.08444v1), evaluated 14 model variants from six families on 2,794 tasks, producing 16,764 snippets and 48,494 crate recommendations. Under its detector, 10,779 recommendations were hallucinated, for a reported 20.23% rate. Model-size, temperature, self-refinement, and retrieval changes produced limited or inconsistent improvements.

This is original preprint evidence about source-level Rust references, not `Cargo.toml` additions or downloads. The detector may misclassify aliases, private crates, or parser artifacts. The paper also contains unresolved numerical inconsistencies. Its rate must not be pooled with Python/npm or interpreted as attack prevalence.

The 2026 preprint [“Trust Me, Import This”](https://arxiv.org/html/2605.09594) tests a more adversarial mechanism. Persistent instruction artifacts steered five selected open models toward targeted nonexistent Python package names, including transfer to held-out prompts, models, and domains. Several evaluated skill scanners performed weakly in the bounded setup.

The authors withhold malicious payloads and explicitly measure target-name appearance, not registry publication or compromise. The main optimization gives target inclusion full weight while disabling some stealth and veto objectives, uses only ten optimization rounds, and samples one completion per request. This is valuable laboratory evidence that skills or rules can become supply-chain inputs; it is not a field incidence study.

A [Trend Micro slopsquatting repository](https://github.com/trendmicro/slopsquatting) exposes a small artifact around 100 web-development tasks and qualitatively suggests that reasoning or MCP configurations reduce but do not eliminate phantom dependencies. The rendered repository lacks a complete method, result table, registry snapshot, and compromise evidence. It remains a vendor-owned reproducibility lead rather than an outcome source.

## What is missing

No selected source supplied:

- a registry dataset identifying malicious packages chosen because models hallucinated their names;
- a method distinguishing attacker intent from ordinary package publication;
- downstream install or execution telemetry;
- confirmed victims and impact;
- exposure-normalized prevalence over time;
- a comparison with typosquatting under common definitions.

That gap should remain visible. A security team can justify preventive controls from a plausible chain and measured upstream failure without claiming the completed attack is common.

Even an eventual registry count would need careful interpretation. Researchers would have to preserve dated registry snapshots, show that each name was nonexistent when generated, identify a malicious registrant rather than an unrelated later publisher, and connect publication to an exposed model suggestion. Download counts would still mix scanners, mirrors, researchers, automated builds, and victims. A defensible prevalence study therefore needs both registry provenance and downstream outcome evidence; a count of suspicious names alone would measure opportunity, not compromise.

There are also countervailing mechanisms. A hallucinated name may never recur, be syntactically invalid, be caught during review, or refer to a private package unknown to the detector. An assistant can be constrained to approved dependencies, query a registry, or work from a lockfile. Yet a registry lookup alone fails after malicious registration, and a familiar-looking package can be compromised without any hallucination.

## A safe local threat-chain exercise

Do not publish packages or execute unknown dependencies. Use a disconnected or tightly isolated analysis environment.

### Capture

- Select representative internal coding prompts with no secrets.
- Record model, version, system instructions, tools, temperature, date, and repetitions.
- Extract proposed package names without installing them.
- Compare names with a dated public-registry snapshot and the organization’s approved catalog.
- Manually review aliases, private packages, parser errors, and ambiguous names.

### Classify

For each nonexistent name, record:

- first appearance and recurrence;
- language and task;
- whether a similar legitimate name exists;
- whether a tool or instruction artifact influenced it;
- whether current controls would block acceptance, resolution, install, execution, and production reach.

### Test controls

- Require explicit dependency declaration rather than accepting an import as authority.
- Test allowlist and vetted-registry behavior.
- Test an unknown-name denial with a useful remediation message.
- Verify that lockfiles and provenance checks survive agent-generated edits.
- Confirm isolation, credential separation, egress limits, and review on the installation path.

### Report honestly

Use separate counts for generated references, unique nonexistent names, recurring names, and blocked attempted additions. Do not call any of these “attacks.” A real incident requires evidence of registration, install, execution, and impact. Keep raw prompts only under an approved retention and privacy policy.

This exercise estimates local hallucination exposure and control coverage. It cannot estimate attacker behavior or industry prevalence.

## Evidence judgment

- **Package hallucination:** high confidence that it occurs under studied conditions; two substantial experiments in different ecosystems support the upstream failure.
- **Recurrence and targeted steering:** moderate confidence in bounded setups. Repeatability and adversarial instruction artifacts create a plausible opportunity.
- **Malicious publication prevalence:** unknown. No registry-level population study in the corpus identifies slopsquatting intent.
- **Observed compromise:** not established by the selected evidence.
- **Generalizability:** rates are model-, prompt-, language-, detector-, and date-specific. They cannot be pooled or carried into production without local measurement.
- **Key counterexample:** real supply-chain attacks also target legitimate packages and maintainers, so a hallucinated-name control covers only one path.

The evidence-safe statement is: models sometimes invent repeatable package names, and attackers may exploit that condition. Security policy should interrupt every link while keeping attack prevalence explicitly unknown.

Podcast hook: A model invents a confident package name, an attacker claims it, and a dashboard calls the threat common before anyone proves an install. The episode rebuilds the seven-link chain one denominator at a time.

Continue reading: [Chapter 28, “Delay, registries, microVMs, and internal zero trust”](28-layered-supply-chain-mitigations.md), compares the controls that can interrupt this chain; Chapter 53 operationalizes dependency screening.
